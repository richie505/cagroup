"""Write the CA Prep app's assets (Rocket Prep / APPSC Prep JSON format) from the structured CA notes.

    python scripts/build_ca_assets.py            # -> android/app/src/main/assets

Mapping (data/structured/<folder>/NN.md, format in prompts/notes-guide.md, parsed by check_notes.parse):
    Book    = a period, newest first ("Sep–Oct 2026" ... "Apr–Nov 2025"), then "Special topics" (folder special)
    Unit    = a month ("October 2026"), newest first; the Special topics book has one unit
    Topic   = a category file NN.md (row title = the file's category, e.g. "Andhra Pradesh")
    Section = a "## page" of the file: its blocks (structured_md.to_blocks) after a grey "Sources: ..." note
Only books with notes are written. Book ids are fixed per period (11..16), so a period keeps its id (and the
reader's progress) when others appear later; they are above APPSC Prep's subject ids 1-6, so the subject-specific
read-aloud rules (SpeechText) never apply to them, and Techniques.kt treats every book as current affairs.

There are no MCQs yet: each book gets an empty mcq<id>.json and the app hides MCQ practice when a topic has none.
plan.json is a revision plan from PLAN_START: latest month first, one month per 1-2 days by its pages, Special
topics last, a weekly review day after every six study days.

Re-runnable: it reads whatever folders/files exist now. A file that does not parse yet (being written) or has no
pages is skipped with a warning; format problems found by check_notes.problems are listed but do not stop the build.
Afterwards it runs build_key_terms.py on the assets.
"""
import calendar
import datetime as dt
import json
import math
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import structured_md  # noqa: E402
from check_notes import parse, problems  # noqa: E402

ROOT = HERE.parent
STRUCT = ROOT / "data" / "structured"
OUT = ROOT / "android" / "app" / "src" / "main" / "assets"
PLAN_START = dt.date(2026, 10, 19)
PAGES_PER_DAY = 45  # a month with more pages than this gets two days

# (id, first month, last month, title) newest first; months are "YYYY-MM"
PERIODS = [
    (11, "2026-09", "2026-10", "Sep–Oct 2026"),
    (12, "2026-06", "2026-08", "Jun–Aug 2026"),
    (13, "2026-03", "2026-05", "Mar–May 2026"),
    (14, "2025-12", "2026-02", "Dec 2025–Feb 2026"),
    (15, "2025-04", "2025-11", "Apr–Nov 2025"),
]
SPECIAL_ID = 16
KEEP = {"abbr.json", "acronyms.json", "india.json"}  # read-aloud short forms, checked full forms, dictionary glossary


def month_name(ym: str) -> str:
    y, m = int(ym[:4]), int(ym[5:])
    return f"{calendar.month_name[m]} {y}"


def short_month(ym: str) -> str:
    return f"{calendar.month_abbr[int(ym[5:])]} {ym[:4]}"


def human_sources(frm: list[str], folder: str) -> str:
    """["2026-10-12", "CARE-2026-10", "CA360-2026-10", "OL-2026-10"] -> "Daily 12 Oct · APPSC CARE monthly · CA-360 · One-liners".
    A monthly tag of another month than the folder's names its month."""
    days, other, topics = [], [], []

    def month_of(tag_month: str) -> str:
        return "" if tag_month == folder else f" ({short_month(tag_month)})"

    for t in frm:
        if re.fullmatch(r"\d{4}-\d\d-\d\d", t):
            d = dt.date.fromisoformat(t)
            days.append(f"{d.day} {calendar.month_abbr[d.month]}" + ("" if t[:7] == folder or folder == "special" else f" {d.year}"))
            continue
        m = re.fullmatch(r"(CARE|APCA|CA360|OL)-(\d{4}-\d\d)", t)
        if m:
            name = {"CARE": "APPSC CARE monthly", "APCA": "AP CA monthly", "CA360": "CA-360", "OL": "One-liners"}[m.group(1)]
            other.append(name + month_of(m.group(2)))
            continue
        if t.startswith("TOPIC-"):
            topics.append(t[6:].replace("-", " ").replace("_", " ").strip())
            continue
        other.append(t)
    parts = []
    if days:
        parts.append("Daily " + ", ".join(days))
    parts += list(dict.fromkeys(other))
    if topics:
        parts.append("Topic PDF: " + ", ".join(dict.fromkeys(topics)))
    return " · ".join(parts)


def load_file(path: Path):
    """(category title, [(page title, from, body lines)]) or None if the file cannot be used yet."""
    try:
        _, _, title, pages = parse(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        print(f"  skip {path.parent.name}/{path.name}: {e}")
        return None
    pages = [p for p in pages if any(l.strip() for l in p[2])]
    if not pages:
        return None
    for issue in problems(path)[:5]:
        print(f"  note: {issue}")
    return title, pages


def topic_row(folder: str, title: str, pages: list) -> dict:
    secs, all_from = [], []
    for ptitle, frm, body in pages:
        all_from += [f for f in frm if f not in all_from]
        src = human_sources(frm, folder)
        blocks = ([{"k": "n", "x": [["Sources: ", 1], [src, 0]]}] if src else []) + structured_md.to_blocks("\n".join(body), [])
        secs.append({"t": ptitle, "badges": [], "p": 0, "b": blocks})
    dates = sorted(f for f in all_from if re.fullmatch(r"\d{4}-\d\d-\d\d", f))
    src = human_sources([f for f in all_from if f not in dates], folder)
    if dates:
        a, b = dt.date.fromisoformat(dates[0]), dt.date.fromisoformat(dates[-1])
        span = f"{a.day} {calendar.month_abbr[a.month]}" + ("" if a == b else f" – {b.day} {calendar.month_abbr[b.month]}")
        src = f"Daily pages ({len(dates)}, {span})" + (" · " + src if src else "")
    return {"codes": [], "tag": "", "title": title, "sub": [], "pyq": "", "p1": 0, "p2": 0, "secs": secs,
            "src": [f"Sources: {src}"] if src else []}


def collect():
    """[(id, title, short, [(unit title, folder, [row])])] for the books that have notes."""
    months = sorted((d.name for d in STRUCT.iterdir() if d.is_dir() and re.fullmatch(r"\d{4}-\d\d", d.name)), reverse=True)
    books = []
    for bid, first, last, title in PERIODS:
        units = []
        for ym in (m for m in months if first <= m <= last):
            rows = [topic_row(ym, *f) for f in (load_file(p) for p in sorted((STRUCT / ym).glob("[0-9][0-9].md"))) if f]
            if rows:
                units.append((month_name(ym), ym, rows))
        if units:
            books.append((bid, f"Current Affairs · {title}", title, units))
    known = [m for m in months if any(a <= m <= b for _, a, b, _ in PERIODS)]
    for m in sorted(set(months) - set(known)):
        print(f"  warning: folder {m} is outside the periods in PERIODS - not in the app")
    sp = STRUCT / "special"
    if sp.is_dir():
        rows = [topic_row("special", *f) for f in (load_file(p) for p in sorted(sp.glob("[0-9][0-9].md"))) if f]
        if rows:
            books.append((SPECIAL_ID, "Special topics (budgets, awards, reports ...)", "Special topics", [("Special topics", "special", rows)]))
    return books


def page_count(rows) -> int:
    return sum(len(r["secs"]) for r in rows)


def build_plan(blocks: list) -> dict:
    """blocks: [(focus, [(book, row index, topic label, pages)])] in study order."""
    study = []  # (focus, rows) per study day
    for focus, rows in blocks:
        pages = sum(r[3] for r in rows)
        cap = 3 if focus == "Special topics" else 2
        n = max(1, min(cap, math.ceil(pages / PAGES_PER_DAY)))
        n = min(n, len(rows))
        if n == 1:
            study.append((focus, rows))
            continue
        # split the topics into n days of about equal pages, keeping their order
        target, cur, acc, part = pages / n, [], 0, 1
        for i, r in enumerate(rows):
            cur.append(r)
            acc += r[3]
            left_rows, left_days = len(rows) - i - 1, n - part
            if part < n and (acc >= target * part or left_rows == left_days):
                study.append((f"{focus} (part {part})", cur))
                cur, part = [], part + 1
        if cur:
            study.append((f"{focus} (part {part})", cur))
    days, week = [], []
    for focus, rows in study:
        days.append(("study", focus, rows))
        week += rows
        if len(days) % 7 == 6:
            days.append(("review", "", week))
            week = []
    if week:
        days.append(("review", "", week))
    total = len(days)
    out = []
    for n, (kind, focus, rows) in enumerate(days, 1):
        date = PLAN_START + dt.timedelta(days=n - 1)
        pages = sum(r[3] for r in rows)
        plan_rows = [{"codes": [], "topic": label, "p": "", "pyq": "", "pri": "", "ref": [b, ri]} for b, ri, label, _ in rows]
        if kind == "study":
            typ, phase = "study", "PHASE 1 FIRST PASS"
            brief = [f"Read: {focus} – {len(rows)} topics, {pages} pages.",
                     "Mark each page read; bookmark the ones to revise again."]
            tasks = [
                {"time": "07:00-09:30", "block": "Read 1", "task": "First half of today's topics: read each page, mark it read."},
                {"time": "10:00-12:30", "block": "Read 2", "task": "Second half of today's topics, same routine."},
                {"time": "17:00-18:00", "block": "Listen", "task": "Read aloud (headphones button) through today's pages once more."},
                {"time": "20:00-20:30", "block": "Recall", "task": "Close the app: recall each news item's who / what / where / numbers; reopen the ones you missed."},
            ]
        else:
            typ, phase, focus = "sunday", "WEEKLY REVIEW", ""
            brief = [f"This week's topics: {len(rows)} topics, {pages} pages.", "Re-read the bookmarked pages first, then the tables (awards, ranks, days)."]
            tasks = [
                {"time": "08:00-11:00", "block": "Re-read", "task": "Pages of this week's topics: bookmarked pages first."},
                {"time": "14:00-16:00", "block": "Tables", "task": "Award winners, index ranks, days and themes: say them from memory, check."},
                {"time": "17:00-18:00", "block": "Saved", "task": "Go through Saved pages once more."},
            ]
        left = total - n + 1
        out.append({
            "n": n, "date": date.isoformat(), "dow": date.strftime("%a"), "phase": phase, "focus": focus.upper(),
            "brief": brief, "left": f"{left} day{'s' if left != 1 else ''} left in plan", "type": typ,
            "rows": plan_rows, "tasks": tasks,
        })
    end = PLAN_START + dt.timedelta(days=total)
    # "exam" is only a date the format needs (the day after the plan); no exam date is shown
    return {"start": PLAN_START.isoformat(), "exam": end.isoformat(), "examLabel": "APPSC Group 2", "days": out, "buffer": []}


def save(name: str, obj) -> None:
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    books = collect()
    if not books:
        raise SystemExit("no notes found in data/structured")
    for old in OUT.glob("*.json"):
        if old.name not in KEEP:
            old.unlink()
    index_books, blocks = [], []
    for bid, title, short, units in books:
        book_units, idx_rows = [], []
        for ui, (utitle, folder, rows) in enumerate(units):
            book_units.append({"code": "", "title": utitle, "rows": rows})
            month_rows = []
            for r in rows:
                ri = len(idx_rows)
                idx_rows.append({"u": ui, "codes": [], "title": r["title"], "tag": "", "pyq": "", "p1": 0, "p2": 0,
                                 "n": len(r["secs"]), "q": 0})
                label = f"{utitle} · {r['title']}" if bid != SPECIAL_ID else r["title"]
                month_rows.append((bid, ri, label, len(r["secs"])))
            blocks.append((utitle, month_rows))
        pages = sum(r["n"] for r in idx_rows)
        save(f"book{bid}.json", {"id": bid, "title": title, "short": short, "pages": pages, "units": book_units})
        save(f"mcq{bid}.json", {"rows": {}, "units": {}, "subs": {}})
        index_books.append({"id": bid, "title": title, "short": short, "pages": pages,
                            "units": [{"code": "", "title": u[0]} for u in units], "rows": idx_rows, "uq": {}})
        print(f"book{bid} {short:18} {len(units):2} units {len(idx_rows):3} topics {pages:4} pages")
    save("index.json", {"books": index_books})
    plan = build_plan(blocks)
    save("plan.json", plan)
    print(f"plan: {len(plan['days'])} days from {plan['start']} "
          f"({sum(d['type'] == 'study' for d in plan['days'])} study, {sum(d['type'] == 'sunday' for d in plan['days'])} review)")
    subprocess.run([sys.executable, str(HERE / "build_key_terms.py"), str(OUT)], check=True)


if __name__ == "__main__":
    main()
