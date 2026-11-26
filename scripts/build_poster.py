"""Build the FYP poster (22.5 x 34.5 in, portrait) from docs/poster/granite-poster.html.

Prints a vector PDF with headless Chrome and exports the full-resolution JPEG the handbook asks for.
Usage: python scripts/build_poster.py [--stage fyp1-final] [--version draft]
Needs PyMuPDF and Google Chrome; fonts load from Google Fonts, so the machine must be online.
"""
import argparse
import re
import subprocess
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "poster"
CHROME = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
TECH = re.compile(r"\{\{tech:(\w+):(#[0-9A-Fa-f]{6}):([^}]+)\}\}")


def _tech(m: re.Match) -> str:
    name, color, label = m.groups()
    svg = (SRC / "assets" / "icons" / f"{name}.svg").read_text(encoding="utf-8")
    path = re.search(r'<path d="([^"]+)"', svg).group(1)
    return (f'<div class="tech"><svg viewBox="0 0 24 24" role="img" aria-label="{label}">'
            f'<path d="{path}" fill="{color}"/></svg>{label}</div>')


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="fyp1-final")
    ap.add_argument("--version", default="draft", help="'draft' or vX.Y")
    ap.add_argument("--dpi", type=int, default=300)
    a = ap.parse_args()
    out_dir = ROOT / "deliverables" / "stage-2-fyp1-final"
    stem = f"granite_poster_{a.stage}_{a.version}"
    built = SRC / "_built.html"
    built.write_text(TECH.sub(_tech, (SRC / "granite-poster.html").read_text(encoding="utf-8")), encoding="utf-8")
    pdf = out_dir / f"{stem}.pdf"
    try:
        subprocess.run([str(CHROME), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--run-all-compositor-stages-before-draw", "--virtual-time-budget=15000",
                        f"--print-to-pdf={pdf}", built.as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        built.unlink(missing_ok=True)
    page = pymupdf.open(pdf)[0]
    w, h = page.rect.width / 72, page.rect.height / 72
    assert (round(w, 2), round(h, 2)) == (22.5, 34.5), f"wrong size {w} x {h} in"
    page.get_pixmap(dpi=a.dpi).save(out_dir / f"{stem}.jpg", jpg_quality=92)
    print(f"{pdf.name}: {w} x {h} in; {stem}.jpg at {a.dpi} dpi")


if __name__ == "__main__":
    main()
