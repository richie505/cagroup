"""MCQs for the CA notes with the OpenAI API — generate, verify with a second reader, fill coverage gaps, build.

Built to avoid every MCQ problem of the earlier apps (Rocket Prep / APPSC Prep):
  - "according to the notes" in stems          -> prompt rule + LEAK regex, item dropped
  - facts left untested                         -> each MCQ names the fact ids it tests; `cover` writes MCQs for
                                                   facts no kept MCQ tests (one more try per fact), report lists the rest
  - repeated questions (also across months)     -> ALREADY ASKED list in the prompt + global near-duplicate check
                                                   (same normalised stem, or content words of stem+answer overlap)
  - questions not from the notes / invented     -> only the page's numbered facts are given; every number in the
    numbers                                        answer option and explanation must occur in the cited facts
  - wrong keys, two correct options, garbled    -> `verify`: a second, independent API call answers each MCQ from
                                                   the facts WITHOUT the key; kept only if it picks the same option,
                                                   says exactly one option is correct and finds no flaw
  - answer mostly B                             -> deterministic re-placement of the answer (hash of the stem),
                                                   except formats whose options have a fixed order
  - explanation contradicting the key           -> explanation written with the item and re-checked in `verify`
  - API credits running out mid-run             -> one file per API call (resumable, never paid twice); stops at
                                                   once on 401/403/insufficient_quota, backs off on 429/5xx
  - truncated sources                           -> facts come from data/structured (checked by check_notes.py)

    export OPENAI_API_KEY=...                   # never committed; OPENAI_MODEL optional
    python scripts/ca_facts.py                  # data/facts
    python scripts/ca_mcqs.py models            # check the key and list the models it can use
    python scripts/ca_mcqs.py generate [--folders 2026-10 ...] [--max-calls N] [--workers 6]
    python scripts/ca_mcqs.py verify   [...]
    python scripts/ca_mcqs.py cover    [...]    # then verify again
    python scripts/ca_mcqs.py build             # data/mcqs/<folder>/<NN>.json + out/mcq-report.md
    python scripts/ca_mcqs.py dry --folders 2026-10   # print the first prompt, no API call

Files: data/mcq_raw/gen/<folder>/<NN>/<chunk>.json (one per generate/cover call),
       data/mcq_raw/ver/<folder>/<NN>/<chunk>.json (one per verify call), data/mcqs/<folder>/<NN>.json (kept MCQs).
"""
import argparse
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Event, Lock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ca_facts  # noqa: E402

ROOT = HERE.parent
RAW = ROOT / "data" / "mcq_raw"
MCQS = ROOT / "data" / "mcqs"
REPORT = ROOT / "out" / "mcq-report.md"
API = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.6-luna")
CHUNK_FACTS = 36  # facts per generate call (small pages are grouped up to this)
VERIFY_BATCH = 12  # MCQs per verify call
COVER_TRIES = 3  # coverage calls per news page that still has no question
VERIFY_VERSION = 2  # bump when VERIFY_SYSTEM changes: older verdicts are ignored and items are verified again

FORMATS = [
    "Direct Recall",
    "Negative / Incorrect Statement",
    "Assertion-Reason",
    "Statement-Based (A/B)",
    "Multi-Statement Correctness",
    "Chronological Ordering",
    "List-Matching",
    "Count-Based",
]
FIXED_OPTION_FORMATS = {"Assertion-Reason", "Statement-Based (A/B)", "Count-Based"}
AR_OPTIONS = [
    "Both A and R are true, and R is the correct explanation of A",
    "Both A and R are true, but R is NOT the correct explanation of A",
    "A is true, but R is false",
    "A is false, but R is true",
]
AB_OPTIONS = [
    "Both Statement A and Statement B are true",
    "Both Statement A and Statement B are false",
    "Statement A is true, Statement B is false",
    "Statement A is false, Statement B is true",
]
LEAK = re.compile(r"\b(notes?|sheet|the (given|above|following) (text|passage|facts?)|according to the (text|passage|source|facts?)"
                  r"|as (given|stated|per the source)|fact (list|id)|F\d+)\b", re.I)
ALL_NONE = re.compile(r"\b(all|none|both) of the (above|these)\b", re.I)
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
STOP = set("""a an the of in on at to for by with from and or as is are was were be been being this that these those it its
which who whom what when where why how than then also only into over under about after before during between among
following statement statements correct incorrect true false consider given select code codes below above not""".split())

SYSTEM = """You are an APPSC Group 1 / Group 2 exam paper setter for CURRENT AFFAIRS (news of {period}).
You get one or more pages of revision notes as NUMBERED FACTS (ids like P2.F7) and write exam-standard MCQs.

Hard rules — an item that breaks one is thrown away:
1. Use ONLY the given facts. Never add a name, number, date, place or claim from memory. If the facts are too thin
   for the requested count, return FEWER questions.
2. Each MCQ lists in "fact_ids" every fact id it relies on (1–4 ids). The correct option and the explanation may
   only contain numbers that appear in those facts.
3. Exactly ONE option is correct; the other three are clearly wrong by the facts, yet plausible (adjacent year,
   neighbouring state/district, a related scheme/organisation/person — ideally another entry from the same facts).
   Four distinct options. Never "All/None/Both of the above".
4. Write like a real exam paper: never mention notes, facts, fact ids, sheet, passage, "given text" or "source",
   and never write the format name ("Direct Recall", "[Multi-Statement Correctness]" …) in the question.
5. Current-affairs stems must stand alone: name the event/scheme/report/place so a candidate who read the news
   knows exactly what is asked (e.g. "Which State topped the India Electric Mobility Index released in September
   2026?"). Never ask "Which of the following is true?" without context.
6. Write exactly the number of questions asked for each PAGE (each page is one news item). Test the news item's
   headline fact first (what happened / who / where / launched by / rank / winner / theme), then its most
   exam-worthy detail (a first, a key number, the organisation, the place). Skip minor details and trivia — a
   current-affairs paper asks 1–3 questions per news item, not one per fact. Do not test the same fact twice and
   do not repeat anything in ALREADY ASKED.
7. Mix formats (use the exact format names): about 40% Direct Recall, 15% Negative / Incorrect Statement,
   12% Multi-Statement Correctness, 10% List-Matching, 8% Assertion-Reason, 8% Statement-Based (A/B),
   3% Chronological Ordering, 4% Count-Based. Use a format only when the facts truly support it; for a page with
   one question prefer Direct Recall or Multi-Statement on its headline facts.
   - Assertion-Reason: question "Assertion (A): …\\nReason (R): …"; options EXACTLY, in this order: {ar}
   - Statement-Based (A/B): question "Consider the following statements:\\nStatement A: …\\nStatement B: …";
     options EXACTLY, in this order: {ab}
   - Multi-Statement Correctness: statements numbered 1., 2., 3. on separate lines; options like "1 and 2 only",
     "2 only", "1 and 3 only", "1, 2 and 3".
   - List-Matching: "List-I" a–d and "List-II" i–iv on separate lines; options are codes "a-iii, b-iv, c-ii, d-i";
     exactly one code fully correct.
   - Negative / Incorrect Statement: four statements as options; exactly one is false, made by changing ONE
     detail of a true fact; the explanation names the changed detail and its correct value.
   - Count-Based: "How many of the above …?" with a numbered list; options "Only one", "Only two", "Only three",
     "All four" (or the right series).
   - Chronological Ordering: only when the facts give dates for every item.
8. "explanation": 2–4 sentences that stand alone: the correct answer and why (with the key fact), then the trap —
   why the most tempting wrong option is wrong. For List-Matching give the correct pairs. No "the notes say".
9. "keyword": the exam angle tested, e.g. "Rank in index", "Launched by", "Venue/host", "First/only", "Theme",
   "HQ/publisher", "Scheme objective", "Number/amount", "Place in news", "Appointment".
10. Every page gets its questions; do not spend a page's questions on another page.
"""

USER = """Period: {period}. Category: {category}.
Write {count} MCQs from the facts below.{only}{keys}{asked}

{facts}
"""

VERIFY_SYSTEM = """You check exam MCQs against facts. For each MCQ, answer it using ONLY the facts given with it
(not memory), then judge the item. Be strict:
- "answer_index": the option the facts make correct (0-3), or -1 if none is.
- "exactly_one_correct": true if the facts establish exactly one option as the answer to the question asked.
  For "which/what/where/who" questions the facts naming the answer is enough: the other options are wrong because the
  facts give a different answer — they need not be refuted one by one. For "incorrect statement" questions the key
  statement must be contradicted by the facts and the other three supported by them. For statement / count /
  matching questions every statement or pair must be decidable from the facts. For Assertion-Reason, judge whether
  R explains A with ordinary reasoning from the facts.
- "issue": "none", or one of: "two_correct" (two options can be defended), "none_correct", "not_in_facts" (the KEY
  or a statement needs knowledge the facts do not give), "ambiguous_stem", "garbled", "explanation_contradicts"
  (the explanation disagrees with the key or the facts), "trivial" (no exam value).
- "note": one short sentence when issue is not "none".
Return one verdict per MCQ, in order, with its "qid"."""


# ------------------------------------------------------------------ API

class Stop(Exception):
    """The run must stop: bad key or no credits left."""


STOP_ALL = Event()
LOCK = Lock()
CALLS = {"n": 0, "in": 0, "out": 0}


def api(system: str, user: str, schema: dict, name: str, retries: int = 6) -> dict:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise Stop("OPENAI_API_KEY is not set")
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "response_format": {"type": "json_schema", "json_schema": {"name": name, "strict": True, "schema": schema}},
    }).encode()
    for attempt in range(retries):
        if STOP_ALL.is_set():
            raise Stop("stopped")
        req = urllib.request.Request(f"{API}/chat/completions", data=body,
                                     headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.loads(r.read())
            u = data.get("usage", {})
            with LOCK:
                CALLS["n"] += 1
                CALLS["in"] += u.get("prompt_tokens", 0)
                CALLS["out"] += u.get("completion_tokens", 0)
            msg = data["choices"][0]["message"]
            if msg.get("refusal"):
                raise ValueError(f"refusal: {msg['refusal'][:200]}")
            return json.loads(msg["content"])
        except urllib.error.HTTPError as e:
            text = e.read().decode(errors="ignore")[:500]
            if e.code in (401, 403) or "insufficient_quota" in text or "billing" in text.lower():
                STOP_ALL.set()
                raise Stop(f"HTTP {e.code}: {text}")
            if e.code == 404 and "model" in text:
                STOP_ALL.set()
                raise Stop(f"model {MODEL!r} not available: {text}")
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(min(90, 5 * 2 ** attempt))
                continue
            raise RuntimeError(f"HTTP {e.code}: {text}")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            time.sleep(min(60, 5 * 2 ** attempt))
    raise RuntimeError(f"gave up after {retries} tries")


def gen_schema() -> dict:
    return {
        "type": "object", "additionalProperties": False, "required": ["mcqs"],
        "properties": {"mcqs": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["format", "keyword", "question", "options", "answer_index", "fact_ids", "explanation"],
            "properties": {
                "format": {"type": "string", "enum": FORMATS},
                "keyword": {"type": "string"},
                "question": {"type": "string"},
                "options": {"type": "array", "items": {"type": "string"}},
                "answer_index": {"type": "integer"},
                "fact_ids": {"type": "array", "items": {"type": "string"}},
                "explanation": {"type": "string"},
            }}}},
    }


def ver_schema() -> dict:
    return {
        "type": "object", "additionalProperties": False, "required": ["verdicts"],
        "properties": {"verdicts": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["qid", "answer_index", "exactly_one_correct", "issue", "note"],
            "properties": {
                "qid": {"type": "string"},
                "answer_index": {"type": "integer"},
                "exactly_one_correct": {"type": "boolean"},
                "issue": {"type": "string", "enum": ["none", "two_correct", "none_correct", "not_in_facts", "ambiguous_stem",
                                                     "garbled", "explanation_contradicts", "trivial"]},
                "note": {"type": "string"},
            }}}},
    }


# ------------------------------------------------------------------ facts and chunks

def period_of(folder: str) -> str:
    if folder == "special":
        return "2025–2026 (special topics: budgets, awards, reports)"
    import calendar
    y, m = folder.split("-")
    return f"{calendar.month_name[int(m)]} {y}"


def chunks(data: dict) -> list[list[dict]]:
    """Pages of one category file grouped into calls of at most CHUNK_FACTS facts (a big page is its own call)."""
    out, cur, n = [], [], 0
    for p in data["pages"]:
        if not p["facts"]:
            continue
        if cur and n + len(p["facts"]) > CHUNK_FACTS:
            out.append(cur)
            cur, n = [], 0
        cur.append(p)
        n += len(p["facts"])
    if cur:
        out.append(cur)
    return out


def quota(page: dict) -> int:
    """Questions a news page gets: 1 for a short item, 2 for a medium one, 3 for a big one. Current affairs is
    tested a few questions per news item, not one per fact (the pilot's ~0.6 MCQs per fact was far too heavy)."""
    n = len(page["facts"])
    return 0 if n == 0 else 1 if n <= 6 else 2 if n <= 14 else 3


def fid(page: dict, f: dict) -> str:
    return f"P{page['i']}.{f['id']}"


def facts_text(pages: list[dict], only: set | None = None) -> str:
    parts = []
    for p in pages:
        lines = [f"PAGE P{p['i']} — write {quota(p)} question{'s' if quota(p) > 1 else ''}: {p['title']}"]
        for f in p["facts"]:
            head = f" [{f['head']}]" if f["head"] else ""
            mark = "" if only is None or fid(p, f) in only else " (already tested)"
            lines.append(f"{fid(p, f)}{head}: {f['text']}{mark}")
        parts.append("\n".join(lines))
    return "\n\n".join(parts)


def all_fact_text(data: dict) -> dict:
    return {fid(p, f): f["text"] for p in data["pages"] for f in p["facts"]}


# ------------------------------------------------------------------ validation

def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def content_words(s: str) -> set:
    return {w for w in norm(s).split() if w not in STOP and len(w) > 1}


def nums(s: str) -> set:
    return {n.replace(",", "").rstrip(".") for n in NUM.findall(s)}


def problems_of(q: dict, facts: dict) -> list[str]:
    """Code checks on one generated MCQ (facts: id -> text of its file)."""
    out = []
    opts = q.get("options", [])
    if len(opts) != 4 or any(not o.strip() for o in opts):
        out.append("needs 4 non-empty options")
    elif len({norm(o) for o in opts}) != 4:
        out.append("duplicate options")
    if not 0 <= q.get("answer_index", -1) < len(opts):
        out.append("bad answer_index")
    if q["format"] == "Assertion-Reason" and opts != AR_OPTIONS:
        out.append("A-R options altered")
    if q["format"] == "Statement-Based (A/B)" and opts != AB_OPTIONS:
        out.append("A/B options altered")
    text = q["question"] + " " + " ".join(opts)
    if LEAK.search(text):
        out.append(f"mentions the source: {LEAK.search(text).group(0)!r}")
    if LEAK.search(q["explanation"]):
        out.append("explanation mentions the source")
    if ALL_NONE.search(text):
        out.append("all/none of the above")
    ids = q.get("fact_ids", [])
    if not ids or any(i not in facts for i in ids):
        out.append(f"unknown fact ids {ids}")
    elif not out:
        known = set().union(*(nums(facts[i]) for i in ids))
        answer = opts[q["answer_index"]]
        checked = q["explanation"] + ("" if q["format"] in ("Negative / Incorrect Statement",) else " " + answer)
        # years/counts in A-R / A/B / count / code options are not facts; the stem's statements are checked by verify
        if q["format"] in ("Direct Recall",):
            extra = nums(checked) - known - nums(q["question"])
        else:
            extra = nums(q["explanation"]) - known - nums(q["question"]) - set().union(*(nums(o) for o in opts))
        extra = {n for n in extra if not (len(n) == 1 and n in "1234")}
        if extra:
            out.append(f"numbers not in the cited facts: {sorted(extra)[:5]}")
    if not out and q["format"] == "Direct Recall":
        # the stem gives the answer away: a number (year, amount) shared by the stem and the key but no distractor
        others = set().union(*(nums(o) for i, o in enumerate(opts) if i != q["answer_index"]))
        given = {n for n in nums(opts[q["answer_index"]]) & nums(q["question"]) if len(n) > 1} - others
        if given:
            out.append(f"stem gives the answer away: {sorted(given)}")
    if len(q["explanation"].split()) < 8:
        out.append("explanation too short")
    return out


FORMAT_PREFIX = re.compile(r"^\s*[\[(]?\s*(?:" + "|".join(re.escape(f) for f in FORMATS) + r")\s*[\])]?\s*[:.\-–]?\s*", re.I)


def clean(q: dict) -> dict:
    """Drops a format label the model put in front of the stem."""
    return {**q, "question": FORMAT_PREFIX.sub("", q["question"], count=1).strip()}


def dup_key(q: dict) -> tuple[str, set]:
    stem = norm(q["question"])
    return stem, content_words(q["question"] + " " + q["options"][q["answer_index"]])


class Bank:
    """All kept MCQs so far, for the near-duplicate check (same stem, or ≥60% shared content words)."""

    def __init__(self):
        self.stems, self.words = set(), []

    def is_dup(self, q: dict) -> bool:
        stem, words = dup_key(q)
        if stem in self.stems:
            return True
        for w in self.words:
            if words and w and len(words & w) / len(words | w) >= 0.6:
                return True
        return False

    def add(self, q: dict) -> None:
        stem, words = dup_key(q)
        self.stems.add(stem)
        self.words.append(words)


def place_answer(q: dict, qid: str) -> dict:
    """Move the answer to a position chosen by a hash of the id (balanced A-D), for formats without fixed order."""
    if q["format"] in FIXED_OPTION_FORMATS:
        return q
    opts = list(q["options"])
    target = int(hashlib.sha1(qid.encode()).hexdigest(), 16) % 4
    a = q["answer_index"]
    if a != target:
        opts[a], opts[target] = opts[target], opts[a]
    return {**q, "options": opts, "answer_index": target}


# ------------------------------------------------------------------ steps

def files(args) -> list[tuple[str, str]]:
    want = set(args.folders or [])
    return [(f, n) for f, n in ca_facts.all_files() if not want or f in want]


def raw_path(kind: str, folder: str, nn: str, k) -> Path:
    return RAW / kind / folder / nn / f"{k}.json"


def load_raw(kind: str, folder: str, nn: str) -> dict:
    d = RAW / kind / folder / nn
    return {p.stem: json.loads(p.read_text()) for p in sorted(d.glob("*.json"))} if d.exists() else {}


def asked_list(qs: list[dict], limit: int = 60) -> str:
    if not qs:
        return ""
    return ("\n\nALREADY ASKED — do not repeat these or re-test their facts:\n"
            + "\n".join("- " + q["question"][:150].replace("\n", " / ") for q in qs[-limit:]))


KEY_PLANS = {
    "Statement-Based (A/B)": AB_OPTIONS,
    "Assertion-Reason": AR_OPTIONS,
    "Multi-Statement Correctness": ["exactly one statement is correct", "exactly two statements are correct",
                                    "all statements are correct", "exactly two statements are correct"],
    "Count-Based": ["Only one", "Only two", "Only three", "Only two"],
}


def key_plan(seed: str) -> str:
    """Which answer each fixed-order format must have in this call, rotated by a hash of the call, so that
    "both true", "all of them" and option A do not become a pattern a candidate can guess."""
    h = int(hashlib.sha1(seed.encode()).hexdigest(), 16)
    how = {"Assertion-Reason": "choose A and R from the facts so that this is right; a false A or R changes one detail of a true fact"}
    lines = [f"- {fmt}: make the correct answer \"{opts[(h >> (3 * i)) % len(opts)]}\" ("
             + how.get(fmt, "a false statement changes one detail of a true fact") + ")"
             for i, (fmt, opts) in enumerate(KEY_PLANS.items())]
    return ("\n\nANSWER PLAN for this call — if you write one of these formats, its correct answer MUST be as below "
            "(a second one of the same format may use any other answer):\n" + "\n".join(lines))


def gen_job(folder: str, nn: str, key: str, pages: list[dict], count: int, only: set | None, asked: list[dict], title: str):
    path = raw_path("gen", folder, nn, key)
    if path.exists():
        return 0
    user = USER.format(period=period_of(folder), category=title, count=count,
                       only=("\nThese news pages have no question yet: write ONE question for each page, on its headline fact."
                             if only else ""),
                       keys=key_plan(f"{folder}/{nn}/{key}"), asked=asked_list(asked), facts=facts_text(pages, only))
    system = SYSTEM.format(period=period_of(folder), ar=" | ".join(AR_OPTIONS), ab=" | ".join(AB_OPTIONS))
    res = api(system, user, gen_schema(), "ca_mcqs")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"model": MODEL, "pages": [p["i"] for p in pages], "only": sorted(only) if only else None,
                                "mcqs": res["mcqs"]}, ensure_ascii=False, indent=1))
    return len(res["mcqs"])


def run(jobs, workers: int, max_calls: int | None):
    jobs = jobs[:max_calls] if max_calls else jobs
    done = made = 0
    with ThreadPoolExecutor(workers) as ex:
        futs = [ex.submit(*j) for j in jobs]
        for f in as_completed(futs):
            try:
                made += f.result() or 0
                done += 1
            except Stop as e:
                STOP_ALL.set()
                print(f"STOPPED: {e}", flush=True)
            except Exception as e:  # noqa: BLE001
                print(f"  error: {e}", flush=True)
            if done and done % 25 == 0:
                print(f"  {done}/{len(jobs)} calls, {made} items, tokens in {CALLS['in']:,} out {CALLS['out']:,}", flush=True)
    print(f"done {done}/{len(jobs)} calls, {made} items; tokens in {CALLS['in']:,} out {CALLS['out']:,}")
    if STOP_ALL.is_set():
        sys.exit(2)


def cmd_generate(args):
    jobs = []
    for folder, nn in files(args):
        data = ca_facts.load(folder, nn)
        for k, pages in enumerate(chunks(data)):
            nf = sum(len(p["facts"]) for p in pages)
            count = sum(quota(p) for p in pages)
            jobs.append((gen_job, folder, nn, f"c{k:03d}", pages, count, None, [], data["title"]))
    print(f"{len(jobs)} generate calls to make (finished ones are skipped)")
    run(jobs, args.workers, args.max_calls)


def candidates(folder: str, nn: str) -> list[dict]:
    """Every generated item of a file with its stable qid ("<folder>/<NN>/<call>#<k>")."""
    out = []
    for key, rec in load_raw("gen", folder, nn).items():
        for k, q in enumerate(rec["mcqs"]):
            out.append({**clean(q), "qid": f"{folder}/{nn}/{key}#{k}"})
    return out


def ver_job(folder: str, nn: str, key: str, items: list[dict], facts: dict):
    path = raw_path("ver", folder, nn, key)
    if path.exists():
        return 0
    blocks = []
    for q in items:
        ids = q["fact_ids"]
        fl = "\n".join(f"  - {facts[i]}" for i in ids if i in facts)
        ol = "\n".join(f"  {i}. {o}" for i, o in enumerate(q["options"]))
        blocks.append(f"qid: {q['qid']}\nFACTS:\n{fl}\nQUESTION ({q['format']}):\n{q['question']}\nOPTIONS:\n{ol}\n"
                      f"EXPLANATION GIVEN: {q['explanation']}")
    res = api(VERIFY_SYSTEM, "\n\n---\n\n".join(blocks), ver_schema(), "ca_verify")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"model": MODEL, "verdicts": res["verdicts"]}, ensure_ascii=False, indent=1))
    return len(res["verdicts"])


def verdicts(folder: str, nn: str) -> dict:
    out = {}
    for name, rec in load_raw("ver", folder, nn).items():
        if not name.startswith(f"v{VERIFY_VERSION}-"):
            continue  # made with an older verify prompt
        for v in rec["verdicts"]:
            out[v["qid"]] = v
    return out


def cmd_verify(args):
    jobs = []
    for folder, nn in files(args):
        data = ca_facts.load(folder, nn)
        facts = all_fact_text(data)
        seen = verdicts(folder, nn)
        todo = [q for q in candidates(folder, nn) if q["qid"] not in seen and not problems_of(q, facts)]
        done_keys = set(load_raw("ver", folder, nn))
        for b in range(0, len(todo), VERIFY_BATCH):
            items = todo[b:b + VERIFY_BATCH]
            key = f"v{VERIFY_VERSION}-" + hashlib.sha1("|".join(q["qid"] for q in items).encode()).hexdigest()[:12]
            if key not in done_keys:
                jobs.append((ver_job, folder, nn, key, items, facts))
    print(f"{len(jobs)} verify calls to make")
    run(jobs, args.workers, args.max_calls)


def page_of(q: dict) -> int:
    """The page (news item) an MCQ belongs to: the page most of its facts come from."""
    pages = [int(re.match(r"P(\d+)\.", f).group(1)) for f in q["fact_ids"]]
    return max(set(pages), key=pages.count)


def kept(folder: str, nn: str, facts: dict, bank: Bank, log: list) -> list[dict]:
    """The file's MCQs that pass the code checks, the second reader and the duplicate check — at most the page's
    quota per news page (the first ones generated win)."""
    ver = verdicts(folder, nn)
    quotas = {p["i"]: quota(p) for p in ca_facts.load(folder, nn)["pages"]}
    per_page = {}
    out = []
    for q in candidates(folder, nn):
        p = problems_of(q, facts)
        v = ver.get(q["qid"])
        if p:
            log.append((q, "code: " + "; ".join(p)))
            continue
        if v is None:
            log.append((q, "not verified yet"))
            continue
        if v["answer_index"] != q["answer_index"] or not v["exactly_one_correct"] or v["issue"] != "none":
            why = v["issue"] if v["issue"] != "none" else ("second reader picked option %d, key %d" % (v["answer_index"], q["answer_index"])
                                                           if v["answer_index"] != q["answer_index"] else "not exactly one correct")
            log.append((q, f"verify: {why} — {v['note']}"))
            continue
        pg = page_of(q)
        if per_page.get(pg, 0) >= quotas.get(pg, 1):
            log.append((q, "over the page's quota"))
            continue
        if bank.is_dup(q):
            log.append((q, "duplicate"))
            continue
        per_page[pg] = per_page.get(pg, 0) + 1
        bank.add(q)
        out.append(place_answer(q, q["qid"]))
    return out


def ordered_files(fs):
    """Newest month first, special last — the order of the app; duplicates are dropped from older months."""
    return sorted(fs, key=lambda x: ("0" if x[0] != "special" else "1", "".join(chr(255 - ord(c)) for c in x[0]), x[1]))


def cmd_cover(args):
    bank, log, jobs = Bank(), [], []
    for folder, nn in ordered_files(files(args)):
        data = ca_facts.load(folder, nn)
        facts = all_fact_text(data)
        qs = kept(folder, nn, facts, bank, log)
        hit = {page_of(q) for q in qs}
        gens = load_raw("gen", folder, nn)
        tries = {}  # page -> coverage calls already made for it
        for rec in gens.values():
            if rec.get("only"):
                for pg in {int(re.match(r"P(\d+)\.", i).group(1)) for i in rec["only"]}:
                    tries[pg] = tries.get(pg, 0) + 1
        for k, pages in enumerate(chunks(data)):
            empty = [p for p in pages if p["facts"] and p["i"] not in hit and tries.get(p["i"], 0) < COVER_TRIES]
            if empty:
                gap = {fid(p, f) for p in empty for f in p["facts"]}
                asked = [q for q in qs if page_of(q) in {p["i"] for p in pages}]
                rnd = max(tries.get(p["i"], 0) for p in empty)
                key = f"g{k:03d}" + (f"r{rnd + 1}" if rnd else "")
                jobs.append((gen_job, folder, nn, key, empty, len(empty), gap, asked, data["title"]))
    print(f"{len(jobs)} coverage calls to make (one question for each news page that has none; up to {COVER_TRIES} tries)")
    run(jobs, args.workers, args.max_calls)


def cmd_build(args):
    bank, log = Bank(), []
    total = covered = nfacts = 0
    pages_all = pages_hit = 0
    per = []
    for folder, nn in ordered_files(files(args)):
        data = ca_facts.load(folder, nn)
        facts = all_fact_text(data)
        qs = kept(folder, nn, facts, bank, log)
        tested = {i for q in qs for i in q["fact_ids"]}
        pages_all += sum(1 for p in data["pages"] if p["facts"])
        pages_hit += len({page_of(q) for q in qs})
        nfacts += len(facts)
        covered += len(tested)
        total += len(qs)
        per.append((folder, nn, data["title"], len(qs), len(tested), len(facts)))
        out = MCQS / folder / f"{nn}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"folder": folder, "nn": nn, "mcqs": [
            {"id": q["qid"], "format": q["format"], "keyword": q["keyword"], "question": q["question"], "options": q["options"],
             "answer": q["answer_index"], "explanation": q["explanation"], "facts": q["fact_ids"]} for q in qs]},
            ensure_ascii=False, indent=1), encoding="utf-8")
    write_report(per, log, total, covered, nfacts, pages_hit, pages_all)
    print(f"{total} MCQs kept; news pages with a question {pages_hit}/{pages_all}; facts tested {covered}/{nfacts} "
          f"({covered / max(1, nfacts):.1%}); report {REPORT}")


def write_report(per, log, total, covered, nfacts, pages_hit=0, pages_all=0):
    from collections import Counter
    reasons = Counter(r.split(" — ")[0].split(":")[0] + (":" + r.split(":")[1].split("—")[0].strip() if r.startswith("verify") else "")
                      for _, r in log)
    pos, fpos = Counter(), Counter()
    for folder, nn, *_ in per:
        for q in json.loads((MCQS / folder / f"{nn}.json").read_text())["mcqs"]:
            pos["ABCD"[q["answer"]]] += 1
            fpos[(q["format"], "ABCD"[q["answer"]])] += 1
    lines = [f"# CA MCQ report", "", f"- MCQs kept: **{total}**",
             f"- News pages with at least one question: **{pages_hit} / {pages_all}**", f"- Facts tested: **{covered} / {nfacts}** ({covered / max(1, nfacts):.1%})",
             f"- Answer positions: " + ", ".join(f"{k} {pos[k]}" for k in "ABCD"), "",
             "| Format | A | B | C | D |", "|---|---|---|---|---|"] + [
             f"| {f} | " + " | ".join(str(fpos[(f, k)]) for k in "ABCD") + " |" for f in FORMATS] + [
             "", "## Dropped items by reason", "",
             "| Reason | Items |", "|---|---|"] + [f"| {r} | {n} |" for r, n in reasons.most_common()] + [
             "", "## Per file", "", "| File | Category | MCQs | Facts tested |", "|---|---|---|---|"] + [
             f"| {f}/{n} | {t} | {q} | {c}/{a} |" for f, n, t, q, c, a in per] + [
             "", "## Dropped by the second reader (for human review)", ""]
    for q, r in log:
        if r.startswith("verify"):
            lines.append(f"- `{q['qid']}` {r}\n  - Q: {q['question'][:200].replace(chr(10), ' / ')}\n  - Key: {q['options'][q['answer_index']][:120]}")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_models(args):
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY is not set")
    req = urllib.request.Request(f"{API}/models", headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        ids = sorted(m["id"] for m in json.loads(r.read())["data"])
    print("\n".join(ids))
    print(f"\nconfigured model: {MODEL} ({'available' if MODEL in ids else 'NOT in the list'})")


def cmd_dry(args):
    folder, nn = files(args)[0]
    data = ca_facts.load(folder, nn)
    pages = chunks(data)[0]
    print(SYSTEM.format(period=period_of(folder), ar=" | ".join(AR_OPTIONS), ab=" | ".join(AB_OPTIONS)))
    print("=" * 60)
    nf = sum(len(p["facts"]) for p in pages)
    print(USER.format(period=period_of(folder), category=data["title"], count=sum(quota(p) for p in pages), only="",
                      keys=key_plan(f"{folder}/{nn}/c000"), asked="", facts=facts_text(pages)))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["models", "generate", "verify", "cover", "build", "dry"])
    ap.add_argument("--folders", nargs="*")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--max-calls", type=int)
    args = ap.parse_args()
    {"models": cmd_models, "generate": cmd_generate, "verify": cmd_verify, "cover": cmd_cover, "build": cmd_build,
     "dry": cmd_dry}[args.cmd](args)


if __name__ == "__main__":
    main()
