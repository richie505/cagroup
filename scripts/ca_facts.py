"""Atomic facts of the structured CA notes, for MCQ generation and the coverage check.

Every "- " bullet, "  - " sub-bullet and table row of a page is one fact (a table row is written as
"Header: cell; Header: cell"). The page's "# N." heading is kept as context. Ids are stable per page:
"<folder>/<NN>/<page index>/F<k>", so MCQs can name the facts they test.

    python scripts/ca_facts.py            # -> data/facts/<folder>/<NN>.json, prints counts
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check_notes import parse  # noqa: E402

ROOT = HERE.parent
STRUCT = ROOT / "data" / "structured"
OUT = ROOT / "data" / "facts"


def plain(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def page_facts(body: list[str]) -> list[dict]:
    """[{id: "F1", text, head}] for one page."""
    facts, head, table_head, parent = [], "", None, ""
    for line in body + [""]:
        if line.startswith("|"):
            row = cells(line)
            if table_head is None:
                table_head = [plain(c) for c in row]
            elif not all(re.fullmatch(r":?-{2,}:?", c or "--") for c in row):
                pairs = [f"{h}: {plain(c)}" if h else plain(c) for h, c in zip(table_head, row) if plain(c) not in ("", "—", "-")]
                if len(pairs) > 1:
                    facts.append({"text": "; ".join(pairs), "head": head})
            continue
        table_head = None
        if line.startswith("# "):
            head = plain(re.sub(r"^# \d+\.\s*", "", line))
        elif line.startswith("- "):
            parent = plain(line[2:])
            facts.append({"text": parent, "head": head})
        elif line.startswith("  - "):
            label = re.match(r"\*\*(.+?)\*\*", parent)
            prefix = f"{plain(label.group(1)).rstrip(':')} — " if label else ""
            facts.append({"text": prefix + plain(line[4:]), "head": head})
    out = []
    for f in facts:
        if len(re.findall(r"[A-Za-z0-9]+", f["text"])) >= 3:  # drop empty labels
            out.append({"id": f"F{len(out) + 1}", **f})
    return out


def load(folder: str, nn: str) -> dict:
    """{"folder", "nn", "title", "pages": [{"i", "title", "from", "facts"}]} for one category file."""
    _, _, title, pages = parse((STRUCT / folder / f"{nn}.md").read_text(encoding="utf-8"))
    return {"folder": folder, "nn": nn, "title": title,
            "pages": [{"i": i, "title": t, "from": frm, "facts": page_facts(body)} for i, (t, frm, body) in enumerate(pages)]}


def all_files():
    for d in sorted(p for p in STRUCT.iterdir() if p.is_dir()):
        for f in sorted(d.glob("[0-9][0-9].md")):
            yield d.name, f.stem


def main() -> None:
    total_f = total_p = 0
    for folder, nn in all_files():
        data = load(folder, nn)
        out = OUT / folder / f"{nn}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        total_p += len(data["pages"])
        total_f += sum(len(p["facts"]) for p in data["pages"])
    print(f"{total_p} pages, {total_f} facts")


if __name__ == "__main__":
    main()
