# Granite Workspace Guide

| Document control | |
|---|---|
| Purpose | The single source of truth for **where every artefact lives, how it is named, and how the layout is used from now until final submission** |
| Version / date | 1.0 / 2026-10-06 (created with the workspace reorganization; moves are mapped in [`archive/migration-map_2026-10-06.tsv`](../archive/migration-map_2026-10-06.tsv)) |
| Status | Canonical. Changing the layout means editing this file in the same pull request (section 9). |
| Companion files | [`README.md`](../README.md) (entry point), [`workspace-index.md`](workspace-index.md) (generated, one line per file), [`plan/master-plan.md`](plan/master-plan.md) (what to build and when) |

---

## 1. The one idea behind the tree: lifecycle state

Every top-level folder has exactly one **lifecycle state**. The state tells you whether you may edit what is inside, so you never have to ask "is this the current version?".

| State | Folders | May I edit? | Rule |
|---|---|---|---|
| **Active** | `docs/`, `research/`, `data/` (except `raw/`), `apps/`, `packages/`, `workflows/`, `tests/`, `scripts/` | Yes, through a pull request | The only places where current work happens |
| **Reference** | `references/`, `data/raw/` | No | Third-party material exactly as received. To update, add a new file; never edit |
| **Frozen record** | `deliverables/stage-N-*/` | Only the stage that is in progress | What was submitted or presented at an evaluation. Once the stage is over it is never edited |
| **Append-only** | `evidence/`, `docs/registers/ai-usage-log.md` | Add, never rewrite | Proof that something happened |
| **History** | `archive/` | No (move things in, never delete) | Superseded or obsolete work, kept so nothing is lost |

Everything else follows from this: **one canonical home per artefact, linked rather than copied**.

## 2. The tree (definitive)

```
Final-Year-Project/                      repo root, project F26-060-Granite
├── README.md                            entry point: what, where, start here
├── CLAUDE.md                            orientation for AI sessions (points here; repeats nothing)
├── .claude/launch.json                  preview-server configuration
├── .github/                             [created by the first CI pull request] workflows/, issue and PR templates, CODEOWNERS
│
├── docs/                                ACTIVE. Documents we write
│   ├── plan/master-plan.md              execution plan; the source of truth for scope, schedule, rubric mapping
│   ├── report/                          LaTeX report source (prescribed template); exported PDFs go to deliverables/
│   ├── diagrams/                        diagram sources and exports (Mermaid, PlantUML, draw.io)
│   ├── adr/                             architecture decision records: adr-NNN-slug.md
│   ├── manuals/                         setup/configuration, tool and user manuals
│   ├── meetings/                        weekly supervisor-meeting minutes: YYYY-MM-DD_supervisor-meeting.md
│   ├── registers/                       living registers: risk, AI usage, Form 13, panel actions, change log, milestone log, ...
│   ├── workspace-guide.md               this file
│   └── workspace-index.md               generated index of every file
│
├── research/                            ACTIVE. Knowledge and experimental evidence
│   ├── literature/                      paper notes, baseline selection, review sheet
│   ├── market/                          commercial-product and framework comparisons
│   ├── spikes/                          proposal-stage proof-of-concept experiments (scripts, outputs, inputs)
│   └── eval/                            pre-registrations, evaluation scripts and results (FYP-1 Final onward)
│
├── data/                                datasets
│   ├── raw/                             REFERENCE. Third-party datasets as downloaded
│   ├── seed/  benchmark/                [created on first use] small curated snapshots; generated Granite benchmark versions
│   ├── datasets.md                      dataset register: licences, active vs benched
│   └── DOWNLOAD.md                      retrieval commands for data/raw
│
├── apps/  packages/  workflows/         ACTIVE CODE. api + web, granite_core + granite_sdk, demo workflows
├── tests/  scripts/                     cross-cutting and end-to-end tests; repository tooling
│
├── references/                          REFERENCE. Read-only source material
│   ├── university/                      handbook, idea-selection guide, mid-assessment rubric
│   ├── templates/                       prescribed report templates (as received)
│   ├── papers/                          research papers (README lists citation and original filename)
│   └── market/                          market surveys and vendor material
│
├── deliverables/                        FROZEN RECORDS, one folder per evaluation stage
│   ├── stage-0-proposal/                proposal defense (11 Sep 2026): deck, proposal documents, PoC, briefing, prep
│   ├── stage-1-fyp1-mid/                FYP-1 mid (supervisor-only)
│   ├── stage-2-fyp1-final/              FYP-1 final: report v2, slides, poster
│   ├── stage-3-fyp2-mid/                FYP-2 mid / pre-job-fair, and the job fair
│   └── stage-4-fyp2-final/              FYP-2 final and the final-deliverables bundle
│
├── evidence/                            APPEND-ONLY. [subfolders created on first use] repo/, interviews/, uat/, demos/, reports/
│
└── archive/                             HISTORY
    ├── proposal-phase/                  audits, trackers and long-form explanations from Aug-Sep 2026
    ├── pre-granite/                     "TraceCause"-era drafts
    ├── superseded/                      earlier versions of active documents (master plan v1.0, ...)
    └── migration-map_2026-10-06.tsv     old path -> new path for every file moved in the reorganization
```

Folder stage codes mirror the handbook's evaluation stages (Appendix A): **0** proposal defense, **1** FYP-1 mid, **2** FYP-1 final, **3** FYP-2 mid / job fair, **4** FYP-2 final.

## 3. Where does X go?

| If you have... | It goes in... | Also do... |
|---|---|---|
| A report chapter, appendix or bibliography entry | `docs/report/` (LaTeX sources) | Commit only your own chapters (per-member evidence) |
| A diagram | `docs/diagrams/` (source and exported PDF/PNG side by side) | Reference it from the report with a relative path |
| A design decision | `docs/adr/adr-NNN-slug.md` (copy `adr-000-template.md`) | Link it from the report's design chapter |
| Supervisor meeting notes | `docs/meetings/YYYY-MM-DD_supervisor-meeting.md` | Record actions in the panel/action register |
| A register entry (risk, AI use, tool disclosure, change, milestone, defect) | `docs/registers/` | AI-use entries are appended, never rewritten |
| A setup, tool or user manual | `docs/manuals/` | Linked from the report (reproducibility criterion) |
| Application code | `apps/<name>/` | Tests next to the code |
| A reusable library | `packages/<name>/` | Python import name is snake_case (`granite_core`) |
| A demo or system-under-test workflow | `workflows/<name>/` | Prompts versioned inside it |
| A test that spans packages, or an end-to-end test | `tests/` | Mark requirement IDs (master plan 27.7) |
| A helper script for the repository | `scripts/` | Add one line to `scripts/README.md` |
| A paper PDF | `references/papers/` named `YYYY_venue_shortname.pdf` | Add a row to `references/papers/README.md` and a BibTeX entry in `docs/report/` |
| An official university document, rubric or template | `references/university/` or `references/templates/` | Keep the original as received |
| A third-party dataset | `data/raw/<name>/` | Add its source, licence and retrieval command to `data/datasets.md` and `data/DOWNLOAD.md` |
| A small curated data snapshot used by a workflow | `data/seed/` | Record provenance and licence |
| A generated Granite benchmark | `data/benchmark/vN/` | Add a datasheet beside it |
| A literature note or comparison | `research/literature/` or `research/market/` | Say which decision it influenced |
| An exploratory experiment | `research/spikes/` (`spikeN_slug.py`) | Add a row to the spikes README |
| A pre-registration, evaluation script or result | `research/eval/` | Pre-register before the run; commit the hash |
| A file submitted or presented at an evaluation | `deliverables/stage-N-*/` | Name it `granite_<artifact>_<stage>_v<X.Y>.<ext>` (section 4) |
| A screenshot, recording, UAT note, interview record or exported test report | `evidence/<type>/` | Name it `YYYY-MM-DD_slug.<ext>`; link it from the register that cites it |
| Something obsolete or replaced | `archive/<phase-or-superseded>/` | **Move, never delete.** Fix links with `scripts/check_links.py` |

## 4. Naming convention

### 4.1 Rules by kind

| Kind | Convention | Examples |
|---|---|---|
| Folders | `lowercase-kebab-case`, no spaces, at most three words, no dates. Importable Python packages and JS packages follow their language (`granite_core`) | `research/literature`, `stage-1-fyp1-mid` |
| Documents and notes | `lowercase-kebab-case.md` | `commercial-product-comparison.md` |
| Papers | `YYYY_venue_shortname.pdf`; venue in lowercase (`icml`, `iclr`, `aaai`, `acl-long`, `acl-findings`, `acl-demo`, `arxiv`) | `2026_acl-findings_errorprobe.pdf` |
| Dated records (minutes, evidence, interviews, snapshots) | `YYYY-MM-DD_slug.ext` (ISO date first, so listings sort chronologically) | `2026-10-14_supervisor-meeting.md` |
| ADRs | `adr-NNN-slug.md`, zero-padded, never renumbered | `adr-004-ast-check-dsl.md` |
| Spikes | `spikeN_slug.py` and `spikeN_slug_output.json`; N continues after the existing 8 | `spike9_replay-stability.py` |
| Datasets | as published by the source (not renamed, because retrieval scripts depend on it) | `data/raw/taubench_retail/` |
| Code | the language's norm: `snake_case.py`, `PascalCase.tsx`, `camelCase.ts` utilities (master plan 26.2) | `granite_core/checks/evaluator.py` |
| Meta files | conventional uppercase names are kept | `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `LICENSE`, `DOWNLOAD.md` |

Never use spaces, parentheses, `(1)`, `copy`, `new`, `final`, `latest` or version words such as `final_v2_REAL`.

### 4.2 Versions and status

- **Living documents** have **no version in the filename**. Git is the history; the document's own control block records version and date. Replacing one with a new generation moves the old file to `archive/superseded/` as `<name>_v<X.Y>_<YYYY-MM-DD>.<ext>` (see `master-plan_v1.0_2026-10-04.md`).
- **Binary or exported artefacts** carry the version, because git cannot diff them: `_v<MAJOR>.<MINOR>`. `v1.0` is the first submission; a corrected resubmission is `v1.1`; a rewritten one is `v2.0`.
- **Status is a suffix only where it matters:** `_draft` means "in progress, not yet submitted". Renaming `_draft` to `_vX.Y` is the act of submitting. Any other status (`review`, `approved`) belongs in the document header, not the filename.

### 4.3 Deliverable names

Inside `deliverables/stage-1-fyp1-mid/` and later:

```
granite_<artifact>_<stage>_v<X.Y>.<ext>        submitted and frozen
granite_<artifact>_<stage>_draft.<ext>         in progress (one draft per artefact)
```

`<artifact>` is one of `report`, `slides`, `poster`, `manual`, `forms`, `code` (release archive), `demo` (recording), `handover`, `design-pack` (the interactive design artefacts), `compliance-audit` (requirement-by-requirement audit), `evidence-sheet` (one-page index of evidence for the assessor). `<stage>` is `fyp1-mid`, `fyp1-final`, `fyp2-mid`, `fyp2-final`.
Examples: `granite_report_fyp1-mid_v1.0.pdf`, `granite_slides_fyp1-final_v1.0.pptx`, `granite_poster_fyp1-final_v1.0.jpg`. The handbook also requires the poster's original Photoshop/Corel file next to the JPEG.

### 4.4 Exceptions

1. **Frozen stage-0 files keep their original names** (`Granite_Proposal_Defense_v2.pptx`). They are history, and several are produced by generator scripts that would recreate the old name.
2. **Generated files keep the generator's output name.** To rename one, change the generator in the same pull request and commit the generator next to its output.
3. **`archive/` and `data/raw/` are exempt** (their names are historical or third-party).
4. **`research/spikes/` keeps its existing `poc_spike*` names**; the PoC console and documents reference them.
5. **`docs/report/` keeps the prescribed template's own file names** (`fast-nuces-bs.cls`, `ThesisFigs/FASTLogo.jpg`, `chapters/chapter1_introduction.tex`); the rubric grades template adherence.

`python scripts/check_workspace.py` enforces sections 4.1-4.3 outside the exempt areas. Code folders (`apps/`, `packages/`, `workflows/`, `tests/`, `scripts/`) follow their language's naming norms and are only checked for spaces and parentheses.

## 5. Indexing and retrieval

Finding anything should take one step for a person and one tool call for an AI assistant.

1. **Predictable paths.** Section 3 maps every artefact type to one folder, so a path can be guessed.
2. **A short `README.md` in each top-level folder and in the folders where work lands** (purpose, naming, owner). They are structural and contain **no file lists**, so they do not go stale.
3. **A generated index**, [`workspace-index.md`](workspace-index.md): one line per file (path and title). It is regenerated by `python scripts/build_index.py`, never edited by hand. Run it before each milestone and when many files change.
4. **A migration map**, [`archive/migration-map_2026-10-06.tsv`](../archive/migration-map_2026-10-06.tsv): any old name found in an old document, an email or chat history is found with one `grep` in this file.
5. **`CLAUDE.md`** at the root tells an AI session what to read first and what to ignore.
6. **Document control blocks** (version, date, status) at the top of the long-lived documents, so recency does not depend on file dates (OneDrive and git both change them).
7. **Link hygiene:** `python scripts/check_links.py` fails on any broken relative link. Wire it into CI (master plan 28.4) with `check_workspace.py`.

Search tips (humans and AI): look in `docs/` and `research/` first. Skip `archive/` unless history is the question, and **never grep `data/raw/`** (about 1,100 third-party files).

## 6. How the structure is used over the rest of the FYP

| When | What gets created and where | What gets frozen |
|---|---|---|
| **Now to Mid-1** (stage 1) | Report sources in `docs/report/`; diagrams in `docs/diagrams/`; ADR-001...010; first minutes in `docs/meetings/`; registers (panel actions, change log C-01, milestone log, dependency and licence register); first code in `apps/`, `packages/`, `workflows/`, `tests/`; CI in `.github/`; repository/CI screenshots in `evidence/repo/` | Export `granite_report_fyp1-mid_v1.0.pdf` (and slides, if used) to `deliverables/stage-1-fyp1-mid/` when submitted |
| **Mid-1 to FYP-1 Final** (stage 2) | Evaluation pre-registration and v0 results in `research/eval/`; benchmark v0 in `data/benchmark/v0/`; stakeholder interviews in `evidence/interviews/`; usability pilot in `evidence/uat/`; SDK in `packages/granite_sdk/`; manuals in `docs/manuals/` | Report v2.0, slides, poster (+ original design file) in `deliverables/stage-2-fyp1-final/` |
| **FYP-2 to Mid-2 / job fair** (stage 3) | Benchmark v1 in `data/benchmark/v1/` with a datasheet; evaluation v1 in `research/eval/`; system-test and NFR reports in `evidence/reports/`; UAT plan in `docs/manuals/`; job-fair booth kit | Updated poster and report, demo recording, job-fair material in `deliverables/stage-3-fyp2-mid/` |
| **FYP-2 UAT to Final-2** (stage 4) | UAT sessions, consent forms and recordings (recordings stay out of git) in `evidence/uat/`; final evaluation; handover in `docs/manuals/`; release tag | Final report, full presentation, references, complete code archive, executable with readme and user manual in `deliverables/stage-4-fyp2-final/` |
| **Every week** | Issue and PR work; Friday owner demos; meeting minutes; register updates | Nothing |

Rules that keep it stable:

1. **Do not create a new top-level folder.** If something does not fit section 3, change this guide first (section 9).
2. **A stage folder is closed when the stage is over.** Fixes after an evaluation go into the *next* stage's folder, with the panel action recorded in the register.
3. **Exports flow one way:** sources (`docs/`, `research/`, code) -> `deliverables/`. Never edit a deliverable; fix the source and export a new version.

## 7. Working rules

1. **One canonical home; link, don't copy.** If two files say the same thing, one of them is wrong soon.
2. **Move, never delete** tracked work. Replaced documents go to `archive/`. Truly regenerable artefacts (`node_modules`, caches, build output) are git-ignored and may be deleted.
3. **Secrets, personal data and proprietary client data never enter the repository** (handbook, industry-collaboration rule). `.env` is ignored; commit `.env.example`.
4. **Large files:** keep individual files small (about 25 MB or less). Video and screen recordings stay on OneDrive and are git-ignored in `evidence/`; list them in `evidence/README.md`.
5. **Third-party material** lives only in `references/` or `data/raw/`, with source and licence recorded.
6. **AI assistance is disclosed** in `docs/registers/ai-usage-log.md` and `form-13-genai-disclosure.md` as work happens (handbook C.8.4).

## 8. Housekeeping facts worth knowing

- The repository sits inside OneDrive. Do not keep `node_modules/`, virtual environments or build output there: they sync thousands of files. The proposal PoC's `node_modules/` was deleted for this reason (`npm ci` recreates it).
- The root `.gitignore` is deliberately untouched by the reorganization. Scoped `.gitignore` files in `docs/report/`, `evidence/` and the stage-0 deck folder carry the new rules.
- `data/raw/` is still tracked in git (about 46 MB, including a vendored upstream repository). The team's earlier decision to untrack it, and the GAIA redistribution concern, are unchanged and tracked in `data/DOWNLOAD.md`.
- Finishing the git side of the reorganization (committing the moves and merging `origin/noor`) is described in [`archive/README.md`](../archive/README.md).

## 9. Changing the structure

A structural change is a pull request that:

1. edits this guide (tree, section 3 and, if needed, the naming rules);
2. updates `scripts/check_workspace.py` if the set of top-level folders or the naming rules change;
3. moves files with `git mv` and runs `python scripts/check_links.py`;
4. regenerates the index with `python scripts/build_index.py`.

Structural changes are expected to be rare: the tree above was designed to hold every artefact the handbook and the master plan name, through FYP-2 final submission.
