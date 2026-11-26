# docs/diagrams

Design artefacts for the product, as SVG plus Markdown pages that explain them. Start at [`design-pack.md`](design-pack.md): it maps every handbook Table 1a design item to its diagram.

- **Everything here except this file is generated** by `python scripts/build_design_pack.py` from the code (`scripts/design_pack/`). Do not edit an SVG or a page by hand; change the code or the generator and rebuild. `--check` runs in CI and fails if a file is out of date.
- One base name per diagram (`finding-state-machine.svg`), embedded in a page with 3 to 6 lines of project-specific explanation (rubric Form 3, criteria 5 and 6).
- Facts come from the code wherever possible: tables and keys, states and events, declared reads, call edges, thresholds and worked examples. Parts that are only planned are drawn dashed and labelled "planned".
- The interactive, single-file version is exported to [`deliverables/stage-1-fyp1-mid/`](../../deliverables/stage-1-fyp1-mid/).
- The Mermaid generator used before 2026-10-11 is in `archive/superseded/export-diagrams_v1.0_2026-10-11.py`.
