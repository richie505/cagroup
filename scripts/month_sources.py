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


def sources(month: str) -> list[tuple[str, Path]]:
    out = [(p.stem[:10], p) for p in sorted((TEXT / month / "daily").glob("*.md"))]
    out += [(f"CARE-{month}" if "CARE" in p.name else f"APCA-{month}", p) for p in sorted((PDF / "monthly").glob(f"{month} - *.txt"))]
    y, m = int(month[:4]), int(month[5:])
    for p in sorted((PDF / "praveen").glob("*.txt")):
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
    return out


if __name__ == "__main__":
    for tag, p in sources(sys.argv[1]):
        print(f"{tag}\t{p.stat().st_size // 1000}K\t{p}")
