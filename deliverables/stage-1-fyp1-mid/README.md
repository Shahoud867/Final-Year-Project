# Granite: FYP-1 mid evaluation deliverables (stage 1)

| | |
|---|---|
| Project | **Granite** (F26-060): an evidence-first investigation workbench for multi-agent AI workflows |
| Team | Shahoud Shahid (23i-2515), Muhammad Noor (23i-2520), Saif Shahzad (23i-2634) · Supervisor: Dr. Adil Majeed |
| Evaluation | FYP-1 mid (about week 8; supervisor only; Form 2 demo and Form 3 report) |
| This guide | Version 1.0, 2026-10-11. Every number and status below was checked on that date |
| Scope | Everything Form 2 and handbook Table 1a ask for **other than the report**. The report (`granite_report_fyp1-mid_v1.0.pdf`) is produced separately from [`docs/report/`](../../docs/report/) and is not covered here |

**Start here if you are assessing:** the one-page [evidence sheet (PDF)](granite_evidence-sheet_fyp1-mid_v1.0.pdf) points to the artefact behind each rubric criterion. The [compliance audit](granite_compliance-audit_fyp1-mid_v1.0.md) gives the detail, including what is not met.

## 1. What Granite does

A workflow of several AI agents can give an answer that looks complete and is wrong (a *silent failure*). Granite runs such a workflow, **checks** the answer against a source of truth, **traces back** to the step where the error began, **verifies** that by replaying the workflow with and without a correction, lets a person **review** the result, and **records** hashed evidence. The Mid-1 slice does this end to end on one workflow, a five-agent refund desk working on real retail order data.

## 2. What is in this folder

| File | What it is |
|---|---|
| [`README.md`](README.md) | This guide |
| [`granite_evidence-sheet_fyp1-mid_v1.0.pdf`](granite_evidence-sheet_fyp1-mid_v1.0.pdf) | One page: where each rubric criterion, design artefact, test result and panel action is evidenced |
| [`granite_compliance-audit_fyp1-mid_v1.0.md`](granite_compliance-audit_fyp1-mid_v1.0.md) | Requirement-by-requirement audit against the handbook, the Form 2 rubric, the faculty requirement and the panel comments, with the verification log |
| [`granite_design-pack_fyp1-mid_v1.0.html`](granite_design-pack_fyp1-mid_v1.0.html) | All 21 design diagrams in one self-contained interactive file (open in a browser: navigation, search, zoom, click a box to highlight its connections) |

Files here are **exports**. The design pack is rebuilt by `python scripts/build_design_pack.py` and the evidence sheet by `python scripts/build_evidence_sheet.py` (needs `pip install reportlab`; it refuses to write the PDF if a path on it does not exist or the page overflows). The living sources stay where the rest of the repository expects them, and this guide links to them instead of copying them:

```
Final-Year-Project/
├── apps/api/            HTTP API, database, background jobs        (71 tests)
├── apps/web/            React user interface                       (32 tests)
├── packages/granite_core/   the engine: trace, checks, attribution, verification   (207 tests)
├── workflows/refund_desk/   the workflow under investigation       (49 tests)
├── tests/system/        black-box tests over real HTTP             (22 cases)
├── docs/diagrams/       design artefacts (generated from the code)
├── docs/manuals/        setup, tool, features, demo, standards, walkthrough, test cases
├── docs/registers/      Form 10, milestone log, change log, defect list, AI log, Form 13
├── docs/adr/            ten architecture decision records
├── evidence/            screenshots, test results, CI and repository records
├── .github/             CI and CD workflows, contribution rules
└── deliverables/stage-1-fyp1-mid/   this folder
```

Still expected in this folder before the meeting, produced by the team: the report PDF, slides if used, and change record C-01 once signed.

## 3. Rubric mapping (Form 2)

Status is the state of the evidence, not a predicted mark.

| # | Criterion (marks) | Evidence | Status |
|---|---|---|---|
| 1 | Previous proposal actions addressed (10) | [Form 10 register](../../docs/registers/form-10-panel-actions.md) | 4 actions done, 2 partly (usability evidence; deployment) |
| 2 | Iteration plan and work breakdown (10) | [Milestone log and iteration plan](../../docs/registers/milestone-log.md) | Core slice done; 4 items late, each with owner and date |
| 3 | Live prototype with core module demo (25) | [Feature catalogue](../../docs/manuals/feature-catalogue.md), [demo runbook](../../docs/manuals/demo-runbook.md), [screenshots](../../evidence/demos/) | Works live, with failure cases; local only, not hosted |
| 4 | Requirements and acceptance criteria (10) | [Requirements trace](../../docs/plan/requirements-trace.md), [system test catalogue](../../docs/manuals/system-test-cases.md) | Traced to code and tests; one requirement openly not met |
| 5 | Design artefacts and evolution (15) | [Design pack](granite_design-pack_fyp1-mid_v1.0.html), [index](../../docs/diagrams/design-pack.md), [ADRs](../../docs/adr/), [change log](../../docs/registers/change-log.md) | All Table 1a artefacts; generated from the code |
| 6 | Repository, milestone and member evidence (10) | [Repository evidence](../../evidence/repo/2026-10-11_repository-evidence.md), [CONTRIBUTING](../../.github/CONTRIBUTING.md) | **Weak:** one account, no pull requests, tags or protection |
| 7 | Testing and early validation (10) | [Test results](../../evidence/reports/2026-10-11_test-results.md), [defect list](../../docs/registers/defect-list.md), [feasibility run](../../research/eval/results/2026-10-07_refund-desk-feasibility-notes.md) | 381 of 381 pass; failure cases at every level |
| 8 | Presentation, Q&A, team and tool ownership (10) | [Code walkthrough](../../docs/manuals/code-walkthrough.md), [AI usage log](../../docs/registers/ai-usage-log.md), [Form 13](../../docs/registers/form-13-genai-disclosure.md) | Study material ready; **understanding not yet demonstrated** |

## 4. Handbook Table 1a mapping

| Phase | Required | Where |
|---|---|---|
| Design: structure | Domain model, component, layer, structure chart | [Architecture page](../../docs/diagrams/architecture.md) |
| Design: behaviour | Flow, DFD (levels 0 and 1), activity, interaction overview, call graph | [Behaviour page](../../docs/diagrams/behaviour.md) |
| | State machine; graph | [Finding state machine](../../docs/diagrams/finding-state-machine.md); [lineage graph](../../docs/diagrams/refund-desk-dataflow.md) |
| | Sequence diagrams | [Run and verification sequences](../../docs/diagrams/verification-sequence.md) |
| | Data dictionary | [Data dictionary](../../docs/diagrams/data-dictionary.md) |
| Design: database | Schema / ER diagram | [Database schema](../../docs/diagrams/database-schema.md) |
| Design: algorithms | Data structures and algorithms | [Algorithm design](../../docs/diagrams/algorithm-design.md) |
| Development | Comments, naming, static analysis, unit tests | [Coding standards](../../docs/manuals/coding-standards.md), enforced in [`ci.yml`](../../.github/workflows/ci.yml) |
| Maintenance | CI/CD | [`ci.yml`](../../.github/workflows/ci.yml) (verified on GitHub), [`cd.yml`](../../.github/workflows/cd.yml) (written, not run) |
| | Deployment diagram | [Deployment diagram](../../docs/diagrams/deployment-diagram.svg) (verified and planned parts drawn differently) |
| | System-level tests | [`tests/system`](../../tests/system/), [catalogue](../../docs/manuals/system-test-cases.md) |
| | Setup and tool manuals | [Setup manual](../../docs/manuals/setup-manual.md), [tool manual](../../docs/manuals/tool-manual.md) |
| Working code and demo | | Sections 5 and 7 below |

No Table 1a artefact was left out. Diagrams are SVG, drawn by [`scripts/build_design_pack.py`](../../scripts/build_design_pack.py), which reads tables, states, data flow, call edges and thresholds from the code and fails in CI if a diagram is out of date or has a layout fault.

## 5. Implemented features

| # | Feature | Where in the product | Verified by |
|---|---|---|---|
| F1 | Run a workflow and record every step | New run; Run page | SYS-CORE-01, 02, 04; browser |
| F2 | Check the outcome and detect silent failures | Run page | SYS-CORE-01, 02; browser |
| F3 | Trace back to where the error began | Finding page | SYS-CORE-01, SYS-SEC-03; browser |
| F4 | Verify a hypothesis by controlled replay (rule VR-1) | Finding page | SYS-CORE-01, 03; browser |
| F5 | Review by a person, with an enforced lifecycle | Finding page | SYS-ERR-03; browser |
| F6 | Hashed evidence and a downloadable report | Finding page | SYS-SEC-02; HTTP API |
| F7 | Search and filter earlier findings | Investigations | SYS-CORE-05; HTTP API |
| F8 | In-app guide and generated API reference | How it works; `/docs` | SYS-CORE-06, 07; browser |

Purpose, inputs with limits, outputs, edge cases, code location and tests for each: [feature catalogue](../../docs/manuals/feature-catalogue.md).

## 6. Testing results (2026-10-11)

| Suite | Level | Tests | Passed | Line coverage |
|---|---|---|---|---|
| `packages/granite_core` | Unit, property | 207 | 207 | 97.5% |
| `workflows/refund_desk` | Unit, integration | 49 | 49 | 95.4% |
| `apps/api` | Integration | 71 | 71 | 96.8% |
| `tests/system` | System, black box over HTTP | 22 | 22 | n/a |
| `apps/web` | Component, accessibility | 32 | 32 | n/a |
| **Total** | | **381** | **381** | |

Record produced by running the suites: [`evidence/reports/2026-10-11_test-results.md`](../../evidence/reports/2026-10-11_test-results.md). Static analysis on the same day: ruff, mypy (strict), ESLint, `tsc`, bandit, pip-audit, npm audit and the architecture check all clean. Tests and code share an author; coverage shows the code does what was intended, not that the intent is right.

## 7. Set up, run and demonstrate

**Tools:** Python 3.11, Node.js 22 or newer, Git. Optional: Ollama with `llama3.2:3b` for live mode; Docker. No paid service and no API key is needed.

From the repository root (full detail and troubleshooting: [setup manual](../../docs/manuals/setup-manual.md)):

```bash
pip install -e "packages/granite_core[dev]" -e "workflows/refund_desk[dev]" -e "apps/api[dev]"
```

```bash
cd apps/web && npm ci && npm run build && cd ../..
```

```bash
cd apps/api && GRANITE_LLM_MODE=recorded GRANITE_STATIC_DIR=../web/dist uvicorn granite_api.main:app_from_env --factory --port 8000
```

Open <http://127.0.0.1:8000>. Recorded mode replays saved real model answers, so it works offline. To check the installation:

```bash
pytest tests/system
```

**Demonstration:** follow the [demo runbook](../../docs/manuals/demo-runbook.md): a six-minute investigation (run, detect, trace back, refute a wrong suspect, confirm the origin, review, export), then failure cases, then code and CI.

## 8. Panel feedback from the proposal defense

| Comment | Status | Resolution |
|---|---|---|
| "UI/UX needs improvement." | Partly | Five task-oriented screens replace the PoC console; states, themes, phone layout, automated accessibility checks. No usability test with outside users yet |
| "Features are not sufficiently clear." | Done | Eight features in one fixed order: [feature catalogue](../../docs/manuals/feature-catalogue.md) and the in-app guide |
| "It is unclear what inputs each feature will accept." | Done | Input tables with types, limits and refusal messages; server-side validation; a test keeps the guide equal to the server's rules |
| "It is unclear how identified flaws/issues will be verified and how verification results will be captured." | Done | Replay with controls and the fixed verdict rule VR-1; hashed evidence, verification levels V0 to V3, exportable report |
| "The overall project workflow must be redefined." | Done | One workflow enforced by a state machine and shown in the UI; change record C-01 awaits the supervisor's signature |
| Faculty requirement: core module with CI/CD on the live interface | Partly | Core module and CI done and verified; CD written but not run; nothing deployed |

Register in the handbook's Form 10 layout, with evidence links: [`form-10-panel-actions.md`](../../docs/registers/form-10-panel-actions.md).

## 9. Known limitations

| Limitation | Detail |
|---|---|
| Not deployed; CD never run | A Render blueprint and a delivery workflow are prepared. A team member must create the service ([deployment record](../../docs/registers/deployment-record.md)) |
| Repository history | All implementation commits come from one account in four days; no pull requests, tags or branch protection ([repository evidence](../../evidence/repo/2026-10-11_repository-evidence.md)) |
| Ownership of AI-assisted code | The implementation was produced with AI assistance and is disclosed. No member has yet demonstrated file-level understanding |
| Work of 2026-10-11 is uncommitted | CI results on GitHub describe the last pushed commit, not this day's changes |
| Personal data is not redacted before storage | Requirement FR-SEC-01 not met (defect D-07); only synthetic data is used |
| Narrow validation | One workflow, one fault type, ten evaluation tasks, one small model |
| Recorded mode by default | Only the example tasks have saved answers; other tasks need a local model |
| No usability evidence | No test with people outside the team |
| Setup not repeated by a non-author | The handbook asks for it |

All open defects: [defect list](../../docs/registers/defect-list.md). What only the team can do, in order: [compliance audit, section 10](granite_compliance-audit_fyp1-mid_v1.0.md).

---

Checklist for this stage: master plan sections 30.6 and 40.2. File names follow `granite_<artifact>_<stage>_v<X.Y>.<ext>` ([workspace guide](../../docs/workspace-guide.md), section 4.3). This folder is frozen after the evaluation; later fixes belong to stage 2.
