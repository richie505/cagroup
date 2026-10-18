"""Checks data/structured/<folder>/NN.md against the notes format (prompts/notes-guide.md).

    python scripts/check_notes.py 2026-09        # one folder
    python scripts/check_notes.py                # all
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STRUCT = ROOT / "data" / "structured"
HEAD = re.compile(r"^=== TOPIC (\S+?):(\d\d) \| (.+)$")
PAGE = re.compile(r"^## (.+?)\s*\|\s*from:\s*(.+)$")
LINE = re.compile(r"^(# \d+\. .+|- .+|  - .+|\|.*\||\s*)$")


def parse(text: str):
    """-> (folder, nn, title, [(page title, [from], [lines])])"""
    lines = text.splitlines()
    m = HEAD.match(lines[0]) if lines else None
    if not m:
        raise ValueError("first line must be '=== TOPIC <folder>:<NN> | <title>'")
    pages = []
    for line in lines[1:]:
        if line.startswith("## "):
            p = PAGE.match(line)
            if not p:
                raise ValueError(f"bad page line: {line[:100]}")
            pages.append((p.group(1).strip(), [x.strip() for x in p.group(2).split(",") if x.strip()], []))
        elif pages:
            pages[-1][2].append(line)
        elif line.strip():
            raise ValueError(f"text before the first page: {line[:100]}")
    return m.group(1), m.group(2), m.group(3).strip(), pages


def problems(path: Path) -> list[str]:
    out = []
    try:
        folder, nn, _, pages = parse(path.read_text(encoding="utf-8"))
    except ValueError as e:
        return [f"{path.name}: {e}"]
    if folder != path.parent.name or nn != path.stem:
        out.append(f"{path.name}: header says {folder}:{nn}")
    seen = {}
    for title, frm, body in pages:
        where = f"{path.parent.name}/{path.name} [{title[:50]}]"
        if title.lower() in seen:
            out.append(f"{where}: duplicate page title")
        seen[title.lower()] = 1
        if not any(l.strip() for l in body):
            out.append(f"{where}: empty page")
        if body and body[0].strip() and not body[0].startswith("# "):
            first = next((l for l in body if l.strip()), "")
            if not first.startswith("# "):
                out.append(f"{where}: page must start with a '# 1. ...' heading")
        n = 0
        for line in body:
            if not LINE.match(line):
                out.append(f"{where}: odd line: {line[:90]}")
            m = re.match(r"# (\d+)\. ", line)
            if m:
                n += 1
                if int(m.group(1)) != n:
                    out.append(f"{where}: heading numbered {m.group(1)}, expected {n}")
        # tables: header + separator, same column count
        group = []
        for line in body + [""]:
            if line.startswith("|"):
                group.append(line)
                continue
            if group:
                cols = [len(r.strip().strip("|").split("|")) for r in group]
                if len(group) < 3 or not re.fullmatch(r"\|(\s*:?-{2,}:?\s*\|)+", group[1].replace(" ", "")):
                    out.append(f"{where}: table needs header row + |---| separator + rows")
                elif len(set(cols)) > 1:
                    out.append(f"{where}: table rows have different column counts {sorted(set(cols))}")
                group = []
        if re.search(r"https?://|www\.", "\n".join(body)):
            out.append(f"{where}: contains a link")
    return out


def main() -> None:
    folders = [STRUCT / a for a in sys.argv[1:]] or sorted(p for p in STRUCT.iterdir() if p.is_dir())
    bad, pages = [], 0
    for d in folders:
        for f in sorted(d.glob("*.md")):
            bad += problems(f)
            try:
                pages += len(parse(f.read_text(encoding="utf-8"))[3])
            except ValueError:
                pass
    for b in bad[:200]:
        print(b)
    print(f"{len(bad)} problems" if bad else f"OK ({pages} pages)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
