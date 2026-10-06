# docs/report: report sources (LaTeX)

The prescribed FAST-NUCES report template (`fast-nuces-bs.cls`, `main.tex`, `chapters/`, `references/`) belongs here as source. The pristine copy as received is [`references/templates/fyp1-mid-report-template_latex.zip`](../../references/templates/fyp1-mid-report-template_latex.zip).

- **Not imported yet.** Import it unmodified, apply the three rendering fixes in [`master-plan.md`](../plan/master-plan.md) section 30.5, and compile before writing.
- **Build:** `pdflatex main`, `bibtex main`, `pdflatex main` twice. Build output is git-ignored in this folder.
- **Ownership:** each author edits and commits only their own chapter files (chapter map in master plan 30.5), which doubles as per-member evidence.
- **Figures** come from [`../diagrams/`](../diagrams/) (set `\graphicspath`); do not copy images in here.
- **Submitted PDFs** are exported to `deliverables/stage-N-*/` as `granite_report_<stage>_v<X.Y>.pdf` and never edited.
