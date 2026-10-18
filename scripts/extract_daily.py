"""Daily KPIAS "APPSC CARE" pages (sources/daily_html) -> clean markdown text per month.

    python scripts/extract_daily.py      # -> sources/text/YYYY-MM/daily/<date> - <title>.md
"""
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "daily_html"
OUT = ROOT / "sources" / "text"
SELECTORS = ["div.elementor-widget-theme-post-content", "div.entry-content", "article .post-content", "main"]


def to_md(el) -> str:
    lines = []
    for node in el.find_all(["h1", "h2", "h3", "h4", "h5", "p", "li", "tr"]):
        if node.find_parent(["li", "tr"]) is not None and node.name in ("p", "li"):
            continue  # nested: taken with its parent
        text = re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip(" ·")
        if not text:
            continue
        if node.name in ("h1", "h2", "h3", "h4", "h5"):
            lines.append("\n" + "#" * min(int(node.name[1]), 4) + " " + text)
        elif node.name == "li":
            lines.append("- " + text)
        elif node.name == "tr":
            lines.append("| " + " | ".join(re.sub(r"\s+", " ", c.get_text(" ", strip=True)) for c in node.find_all(["td", "th"])) + " |")
        else:
            lines.append(text)
    return "\n".join(lines).strip()


def main() -> None:
    n = 0
    for f in sorted(SRC.glob("*.html")):
        soup = BeautifulSoup(f.read_text(encoding="utf-8", errors="ignore"), "lxml")
        el = next((e for s in SELECTORS if (e := soup.select_one(s)) and len(e.get_text()) > 2000), None)
        if el is None:
            print("no content:", f.name, file=sys.stderr)
            continue
        md = to_md(el)
        # trailing prev/next post links
        md = re.sub(r"(\n(APPSC|KPIAS)[^\n]{0,80}Current Affairs[^\n]{0,40}){1,3}\s*$", "", md)
        month = f.name[:7]
        out = OUT / month / "daily" / (f.stem + ".md")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f"<!-- {f.stem} -->\n" + md + "\n", encoding="utf-8")
        n += 1
    print(n, "pages")


if __name__ == "__main__":
    main()
