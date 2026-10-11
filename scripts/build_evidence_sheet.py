"""Build the one-page assessment evidence sheet (PDF) for the FYP-1 mid evaluation.

    python scripts/build_evidence_sheet.py     # needs: pip install reportlab

The sheet is an index, not a claim: every path printed on it must exist (the build fails otherwise), every block
must fit its area (the build fails on overflow), and the result must be exactly one page. Links are relative, so
they open when the PDF is viewed inside the repository folder. Edit the content tables below, not the PDF.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[1]
STAGE = "deliverables/stage-1-fyp1-mid"
OUT = ROOT / STAGE / "granite_evidence-sheet_fyp1-mid_v1.0.pdf"
DATE = "11 October 2026"

INK, MUTED, LINK, RULE, BAND = HexColor("#18212d"), HexColor("#5a6675"), HexColor("#1558b0"), HexColor("#d3dae3"), HexColor("#f1f4f8")
ACCENT = HexColor("#1f3a5f")
TONES = {  # label colour, background
    "MET": (HexColor("#17663d"), HexColor("#e2f3e9")), "DONE": (HexColor("#17663d"), HexColor("#e2f3e9")),
    "PARTLY": (HexColor("#8a5600"), HexColor("#fcefd2")),
    "WEAK": (HexColor("#a3241c"), HexColor("#fae3e1")), "OPEN": (HexColor("#a3241c"), HexColor("#fae3e1")),
}

# ---- content ------------------------------------------------------------------------------------------------
RUBRIC = [
    ("1", "Previous proposal actions addressed", "10", ["docs/registers/form-10-panel-actions.md"],
     "PARTLY", "4 actions done, 2 partly; each with evidence links"),
    ("2", "Iteration plan and work breakdown", "10", ["docs/registers/milestone-log.md"],
     "PARTLY", "Core slice done; 4 items late, with owner and date"),
    ("3", "Live prototype with core module demo", "25", ["docs/manuals/feature-catalogue.md", "docs/manuals/demo-runbook.md"],
     "MET", "8 features live, with failure cases; local, not hosted"),
    ("4", "Requirements and acceptance criteria", "10", ["docs/plan/requirements-trace.md", "docs/manuals/system-test-cases.md"],
     "PARTLY", "Traced to code and tests; one requirement not met"),
    ("5", "Design artefacts and design evolution", "15", [f"{STAGE}/granite_design-pack_fyp1-mid_v1.0.html", "docs/diagrams/design-pack.md"],
     "MET", "All Table 1a artefacts, generated from the code"),
    ("6", "Repository, milestone and member evidence", "10", ["evidence/repo/2026-10-11_repository-evidence.md", ".github/CONTRIBUTING.md"],
     "WEAK", "One account; no pull requests, tags or protection"),
    ("7", "Testing and early validation", "10", ["evidence/reports/2026-10-11_test-results.md", "docs/registers/defect-list.md"],
     "MET", "381 of 381 tests pass; failure cases at every level"),
    ("8", "Presentation, Q&A, team and tool ownership", "10", ["docs/manuals/code-walkthrough.md", "docs/registers/ai-usage-log.md"],
     "OPEN", "Material ready; understanding not yet demonstrated"),
]

DELIVERABLES = [
    ("Design: structure", "domain model, component, layer, structure chart", "docs/diagrams/architecture.md"),
    ("Design: behaviour", "flow, DFD, activity, interaction overview, call graph", "docs/diagrams/behaviour.md"),
    ("State machine and sequences", "", "docs/diagrams/finding-state-machine.md"),
    ("Data dictionary and ER schema", "", "docs/diagrams/data-dictionary.md"),
    ("Algorithm and data-structure design", "", "docs/diagrams/algorithm-design.md"),
    ("Development", "comments, naming, static analysis, unit tests", "docs/manuals/coding-standards.md"),
    ("CI (verified on GitHub) and CD (written, not run)", "", ".github/workflows/ci.yml"),
    ("System-level tests", "22 cases, black box over HTTP", "docs/manuals/system-test-cases.md"),
    ("Setup and tool manuals", "", "docs/manuals/setup-manual.md"),
    ("Deployment diagram", "verified and planned parts marked", "docs/diagrams/deployment-diagram.svg"),
    ("Demonstration", "script with expected values and failure cases", "docs/manuals/demo-runbook.md"),
    ("Working product: screenshots", "", "evidence/demos"),
]

PANEL = [
    ("\u201cUI/UX needs improvement.\u201d", "PARTLY",
     "Five task-oriented screens replace the PoC console; accessibility checks pass. No usability test with outside users yet.",
     "evidence/demos"),
    ("\u201cFeatures are not sufficiently clear.\u201d", "DONE",
     "Eight features in one fixed order, each with purpose, inputs and outputs; the same list is a page in the product.",
     "docs/manuals/feature-catalogue.md"),
    ("\u201cIt is unclear what inputs each feature will accept.\u201d", "DONE",
     "Every input has a type, a limit and a refusal message, enforced by the server and covered by tests.",
     "docs/diagrams/data-dictionary.md"),
    ("\u201cIt is unclear how identified flaws/issues will be verified and how verification results will be captured.\u201d", "DONE",
     "Replay with controls under the fixed rule VR-1; hashed evidence, levels V0 to V3, exportable report.",
     "docs/diagrams/verification-sequence.md"),
    ("\u201cThe overall project workflow must be redefined.\u201d", "DONE",
     "One workflow, enforced by a state machine and shown in the interface. Change record C-01 awaits signature.",
     "docs/diagrams/finding-state-machine.md"),
    ("Faculty requirement: core module with CI/CD on the live interface", "PARTLY",
     "Core module and CI verified. CD written but not run; nothing is deployed.",
     "docs/registers/deployment-record.md"),
]

STATS = [("381 / 381", "automated tests pass"), ("22", "system test cases"), ("21", "diagrams from the code"), ("0", "lint, type, security findings")]

OPEN_ITEMS = [
    "Nothing is deployed; the CD workflow has never run.",
    "One account made all implementation commits. No pull requests, tags or protected branch.",
    "Code written with AI assistance (disclosed); no member has yet shown file-level understanding.",
    "Work of 11 October is uncommitted, so CI on GitHub describes the previous commit.",
    "Personal data is not redacted before storage (FR-SEC-01); synthetic data only.",
]


# ---- drawing kit ---------------------------------------------------------------------------------------------
def fonts() -> tuple[str, str, str, str]:
    folder = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    try:
        for name, file in (("Sans", "segoeui.ttf"), ("Sans-Bold", "segoeuib.ttf"), ("Sans-Semi", "seguisb.ttf"), ("Mono", "consola.ttf")):
            pdfmetrics.registerFont(TTFont(name, str(folder / file)))
        return "Sans", "Sans-Bold", "Sans-Semi", "Mono"
    except Exception:  # any missing font falls back to the built-in ones
        return "Helvetica", "Helvetica-Bold", "Helvetica-Bold", "Courier"


class Sheet:
    def __init__(self) -> None:
        self.sans, self.bold, self.semi, self.mono = fonts()
        self.c = Canvas(str(OUT), pagesize=A4, invariant=1)
        self.w, self.h = A4
        self.problems: list[str] = []
        self.c.setTitle("Granite (F26-060): FYP-1 Mid assessment evidence sheet")
        self.c.setAuthor("Team Granite (F26-060), FAST-NUCES")
        self.c.setSubject("Where each FYP-1 mid rubric criterion and deliverable is evidenced")

    def y(self, top: float) -> float:
        """Convert a distance from the top edge into a PDF coordinate."""
        return self.h - top

    def wrap(self, s: str, font: str, size: float, width: float) -> list[str]:
        lines, line = [], ""
        for word in s.split():
            trial = f"{line} {word}".strip()
            if pdfmetrics.stringWidth(trial, font, size) <= width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        return lines + [line] if line else lines

    def text(self, x: float, top: float, s: str, font: str, size: float, colour=INK) -> float:
        self.c.setFont(font, size)
        self.c.setFillColor(colour)
        self.c.drawString(x, self.y(top), s)
        return pdfmetrics.stringWidth(s, font, size)

    def para(self, x: float, top: float, width: float, s: str, font: str, size: float, colour=INK, leading: float | None = None,
             max_lines: int = 9) -> float:
        """Draw wrapped text; return the distance from the top of the page to the line below it."""
        leading = leading or size * 1.32
        lines = self.wrap(s, font, size, width)
        if len(lines) > max_lines:
            self.problems.append(f"text does not fit in {max_lines} line(s): {s[:50]}...")
        for i, line in enumerate(lines):
            self.text(x, top + i * leading, line, font, size, colour)
        return top + len(lines) * leading

    def link(self, x: float, top: float, path: str, width: float, size: float = 7.1, show: str = "") -> None:
        """Print a repository path and make it a relative link from the PDF's own folder."""
        if not (ROOT / path).exists():
            self.problems.append(f"path does not exist: {path}")
        shown = show or path
        used = pdfmetrics.stringWidth(shown, self.mono, size)
        if used > width:
            self.problems.append(f"path too wide ({used:.0f} > {width:.0f}): {shown}")
        self.text(x, top, shown, self.mono, size, LINK)
        href = path[len(STAGE) + 1:] if path.startswith(STAGE + "/") else "../../" + path
        self.c.linkURL(href, (x - 1, self.y(top) - 2.5, x + used + 1, self.y(top) + size), relative=0, thickness=0)

    def chip(self, x: float, top: float, label: str, width: float = 38) -> None:
        fg, bg = TONES[label]
        self.c.setFillColor(bg)
        self.c.roundRect(x, self.y(top) - 3.2, width, 10.4, 3, stroke=0, fill=1)
        self.c.setFont(self.bold, 6.3)
        self.c.setFillColor(fg)
        self.c.drawCentredString(x + width / 2, self.y(top), label)

    def rule(self, x1: float, x2: float, top: float, colour=RULE, weight: float = 0.5) -> None:
        self.c.setStrokeColor(colour)
        self.c.setLineWidth(weight)
        self.c.line(x1, self.y(top), x2, self.y(top))

    def heading(self, x: float, top: float, letter: str, title: str, note: str = "") -> None:
        self.c.setFillColor(ACCENT)
        self.c.roundRect(x, self.y(top) - 3, 13, 12, 2.5, stroke=0, fill=1)
        self.c.setFont(self.bold, 8)
        self.c.setFillColor(HexColor("#ffffff"))
        self.c.drawCentredString(x + 6.5, self.y(top), letter)
        used = self.text(x + 19, top, title, self.semi, 9.6, ACCENT)
        if note:
            self.text(x + 19 + used + 8, top, note, self.sans, 7.3, MUTED)


def build() -> list[str]:  # noqa: C901 - one page, drawn top to bottom
    s = Sheet()
    left, right = 36.0, s.w - 36.0
    width = right - left

    # ---- header --------------------------------------------------------------------------------------------
    s.c.setFillColor(ACCENT)
    s.c.rect(0, s.y(86), s.w, 86, stroke=0, fill=1)
    s.text(left, 36, "Granite", s.bold, 21, HexColor("#ffffff"))
    s.text(left + 82, 36, "FYP-1 Mid: assessment evidence sheet", s.semi, 13.5, HexColor("#dbe6f5"))
    s.text(left, 53, "Project F26-060  \u00b7  Shahoud Shahid (23i-2515), Muhammad Noor (23i-2520), Saif Shahzad (23i-2634)  \u00b7  "
           "Supervisor: Dr. Adil Majeed", s.sans, 7.8, HexColor("#dbe6f5"))
    s.text(left, 66, f"Checked on {DATE}. Covers every mid-evaluation requirement other than the report. "
           "Paths are from the repository root.", s.sans, 7.8, HexColor("#dbe6f5"))
    s.text(left, 78, "Start here:", s.bold, 7.8, HexColor("#ffffff"))
    start = f"{STAGE}/README.md"
    s.text(left + 44, 78, start, s.mono, 7.6, HexColor("#ffffff"))
    s.c.linkURL("README.md", (left + 43, s.y(78) - 2.5, left + 44 + pdfmetrics.stringWidth(start, s.mono, 7.6), s.y(78) + 7.6), relative=0, thickness=0)
    if not (ROOT / start).exists():
        s.problems.append("the stage README is missing")

    # ---- A. rubric -----------------------------------------------------------------------------------------
    top = 106.0
    s.heading(left, top, "A", "Form 2 rubric: where each criterion is evidenced", "State describes the evidence. It is not a predicted mark.")
    top += 11
    col_ev, chip_x = left + 240, right - 44
    s.c.setFillColor(BAND)
    s.c.rect(left, s.y(top + 12.5), width, 12.5, stroke=0, fill=1)
    for x, label in ((left + 6, "CRITERION (MARKS) AND WHAT THE EVIDENCE SHOWS"), (col_ev, "WHERE THE EVIDENCE IS"), (chip_x, "STATE")):
        s.text(x, top + 9, label, s.bold, 6.2, MUTED)
    top += 12.5
    row_h = 24.0
    for number, name, marks, paths, state, note in RUBRIC:
        base = top + 10
        s.text(left + 6, base, number, s.bold, 8.2, ACCENT)
        used = s.text(left + 17, base, name, s.semi, 8.0)
        s.text(left + 17 + used + 3, base, f"({marks})", s.sans, 7.2, MUTED)
        if left + 17 + used + 22 > col_ev:
            s.problems.append(f"criterion name too wide: {name}")
        s.para(left + 17, base + 9.4, col_ev - left - 25, note, s.sans, 6.9, MUTED, max_lines=1)
        for i, path in enumerate(paths):
            show = path.rsplit("/", 1)[1] + "  (this folder)" if path.startswith(STAGE + "/") else ""
            s.link(col_ev, base + i * 9.4 + (0 if len(paths) > 1 else 4.6), path, chip_x - col_ev - 8, show=show)
        s.chip(chip_x, base + 4.2, state)
        top += row_h
        s.rule(left, right, top)

    # ---- B. deliverables and C. panel comments, side by side -------------------------------------------------
    top += 24
    gap = 22.0
    col_w = (width - gap) / 2
    bx, cx = left, left + col_w + gap
    s.heading(bx, top, "B", "Handbook Table 1a deliverables")
    s.heading(cx, top, "C", "Proposal-defense comments", "11 Sep 2026")
    block_top = top + 13

    y = block_top
    for label, detail, path in DELIVERABLES:
        used = s.text(bx, y + 8, label, s.semi, 7.8)
        if detail:
            if bx + used + 5 + pdfmetrics.stringWidth(detail, s.sans, 6.9) > bx + col_w:
                s.problems.append(f"deliverable line too wide: {label}")
            s.text(bx + used + 5, y + 8, detail, s.sans, 6.9, MUTED)
        s.link(bx, y + 17.4, path, col_w)
        y += 23.2
        s.rule(bx, bx + col_w, y - 1.6, HexColor("#e6eaf0"), 0.4)
    b_bottom = y

    y = block_top
    for quote, state, answer, path in PANEL:
        s.chip(cx + col_w - 38, y + 7.6, state)
        y2 = s.para(cx, y + 8, col_w - 46, quote, s.semi, 7.7, INK, leading=9.4, max_lines=3)
        y2 = s.para(cx, y2 + 0.6, col_w, answer, s.sans, 7.0, MUTED, leading=8.8, max_lines=2)
        s.link(cx, y2 + 0.8, path, col_w)
        y = y2 + 7.6
        s.rule(cx, cx + col_w, y - 1.6, HexColor("#e6eaf0"), 0.4)
    s.text(cx, y + 8, "Form 10 register:", s.semi, 7.2)
    s.link(cx + 66, y + 8, "docs/registers/form-10-panel-actions.md", col_w - 66)
    c_bottom = y + 12

    # ---- D. verified numbers and open items -------------------------------------------------------------------
    top = max(b_bottom, c_bottom) + 20
    s.heading(left, top, "D", f"Verified on {DATE}")
    s.heading(cx, top, "E", "Not met or open, stated plainly")
    band_top, band_h = top + 9, 97.0
    tile_w = (col_w - 3 * 6) / 4
    for i, (value, label) in enumerate(STATS):
        x = bx + i * (tile_w + 6)
        s.c.setFillColor(BAND)
        s.c.roundRect(x, s.y(band_top + band_h - 15), tile_w, band_h - 15, 4, stroke=0, fill=1)
        size = 15 if len(value) < 5 else 11.5
        s.c.setFont(s.bold, size)
        s.c.setFillColor(ACCENT)
        s.c.drawCentredString(x + tile_w / 2, s.y(band_top + 34), value)
        for j, line in enumerate(s.wrap(label, s.sans, 6.9, tile_w - 8)):
            s.c.setFont(s.sans, 6.9)
            s.c.setFillColor(MUTED)
            s.c.drawCentredString(x + tile_w / 2, s.y(band_top + 49 + j * 8.6), line)
    s.text(bx, band_top + band_h - 2.5, "Record:", s.semi, 7.2)
    s.link(bx + 30, band_top + band_h - 2.5, "evidence/reports/2026-10-11_test-results.md", col_w - 30)
    s.c.setFillColor(HexColor("#fdf3f2"))
    s.c.roundRect(cx, s.y(band_top + band_h), col_w, band_h, 4, stroke=0, fill=1)
    y = band_top + 3.5
    for item in OPEN_ITEMS:
        s.c.setFillColor(TONES["OPEN"][0])
        s.c.circle(cx + 8, s.y(y + 5.6), 1.3, stroke=0, fill=1)
        y = s.para(cx + 14, y + 8, col_w - 22, item, s.sans, 6.9, INK, leading=8.2, max_lines=2) - 4.3
    if y > band_top + band_h + 1:
        s.problems.append("the open-items box overflows")

    # ---- footer ----------------------------------------------------------------------------------------------
    foot = band_top + band_h + 17
    s.rule(left, right, foot - 9)
    s.text(left, foot, "Detail, verification log and what only the team can do:", s.sans, 7.1, MUTED)
    s.link(left + 172, foot, f"{STAGE}/granite_compliance-audit_fyp1-mid_v1.0.md", width - 172, 7.0)
    s.text(left, foot + 10, "Prepared with AI assistance, disclosed in docs/registers/ai-usage-log.md and Form 13. "
           "Links are relative: open this PDF from inside the repository folder (for example in a browser).", s.sans, 6.7, MUTED)
    if foot + 10 > s.h - 22:
        s.problems.append(f"content runs past the page: bottom at {foot + 10:.0f} of {s.h:.0f}")
    s.c.showPage()
    if not s.problems:
        s.c.save()
    return s.problems


def main() -> int:
    problems = build()
    for p in problems:
        print("PROBLEM:", p)
    if problems:
        print("evidence sheet not written")
        return 1
    print(f"wrote {OUT.relative_to(ROOT).as_posix()} ({OUT.stat().st_size // 1024} KB, 1 page)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
