# docs/report: report sources (LaTeX)

The prescribed FAST-NUCES report template (`fast-nuces-bs.cls`, `main.tex`, `chapters/`, `references/`), filled with the FYP-1 Mid report draft. The pristine copy as received is [`references/templates/fyp1-mid-report-template_latex.zip`](../../references/templates/fyp1-mid-report-template_latex.zip).

- **Status: first draft (13 Oct 2026).** Every template section has content, compiled from the registers, plan and evidence files with AI assistance (disclosed in the [AI usage log](../registers/ai-usage-log.md)). **Each author must rewrite their chapters in their own words before submission.** `\title{}` and `\projecttitle{}` in `main.tex` are still empty.
- **Build:** `pdflatex main`, `bibtex main`, `pdflatex main` twice (or upload the folder to Overleaf). Build output is git-ignored in this folder.
- **Template fixes** (rendering only, no style change): the class no longer prints the contents lists twice; `\projecttitle` and `\studentone` to `\studentthree` are defined in `main.tex`; `longtable` is loaded; the Students' Submission table starts on its own line. Packages the chapters need are added in one marked block in `main.tex`.
- **Figures** are in `figures/`: the diagrams of [`../diagrams/`](../diagrams/) converted from SVG to PDF (pdflatex cannot include SVG) and screenshots from [`../../evidence/`](../../evidence/). If a diagram changes, convert it again.

## Who writes what

Agreed split, about a third of the report each. Each author edits and commits only their own files, which doubles as per-member evidence.

| Author | Files in `chapters/` |
|---|---|
| Shahoud Shahid | `04_abstract`, `05_acknowledgments`, `06_executive_summary`, `07_abbreviations`, `chapter1_introduction`, `chapter3_iteration_plan`, `chapter10_fyp2_plan`, `conclusion`, `appendix_action_register`, `appendix_meetings` |
| Muhammad Noor Ul Haq | `chapter2_research`, `chapter4_requirements`, `chapter9_development_evidence`, `appendix_requirements`, `appendix_diagrams` |
| Saif Shahzad | `chapter5_design`, `chapter6_iteration1`, `chapter8_testing`, `appendix_test_cases`, `appendix_repository` |

File names follow the template; the rendered chapter numbers differ (`chapter8_testing` is Chapter 7, `chapter9_development_evidence` Chapter 8, `chapter10_fyp2_plan` Chapter 9).

- **Submitted PDFs** are exported to `deliverables/stage-N-*/` as `granite_report_<stage>_v<X.Y>.pdf` and never edited.
