"""Lists each month's source text files (daily pages, monthly compilations, CA-360, one-liners).

    python scripts/month_sources.py 2026-09
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "sources" / "text"
PDF = ROOT / "sources" / "pdf_text"
MON = {m: i + 1 for i, m in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"])}


def full(p: Path) -> Path:
    """The complete, watermark-free pdfplumber text (sources/pdf_text/*.full.txt) when there is one: Drive's
    export of the CA-360 magazines stops at PDF page 80."""
    f = p.with_name(p.stem + ".full.txt")
    return f if f.exists() else p


def sources(month: str) -> list[tuple[str, Path]]:
    out = [(p.stem[:10], p) for p in sorted((TEXT / month / "daily").glob("*.md"))]
    out += [(f"CARE-{month}" if "CARE" in p.name else f"APCA-{month}", p) for p in sorted((PDF / "monthly").glob(f"{month} - *.txt") if not p.name.endswith(".full.txt"))]
    y, m = int(month[:4]), int(month[5:])
    for p in sorted((PDF / "praveen").glob("*.txt")):
        if p.name.endswith(".full.txt"):
            continue
        n = p.name.upper()
        d = re.match(r"CA-(\d\d)-(\d\d)-(\d{4})", n)
        if d:
            if (int(d.group(3)), int(d.group(2))) == (y, m):
                out.append((f"{d.group(3)}-{d.group(2)}-{d.group(1)}", p))
            continue
        if "PRAVEEN" not in n or str(y) not in n:
            continue
        mm = next((v for k, v in MON.items() if re.search(rf"[-\s]{k}", n)), None)
        if mm == m:
            out.append((f"OL-{month}" if "ONELINER" in n or "ONLINER" in n else f"CA360-{month}", p))
    return [(tag, full(p)) for tag, p in out]


if __name__ == "__main__":
    for tag, p in sources(sys.argv[1]):
        print(f"{tag}\t{p.stat().st_size // 1000}K\t{p}")
