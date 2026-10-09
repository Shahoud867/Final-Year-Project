# Execution status

| | |
|---|---|
| Date | 2026-10-07 |
| Companion to | [`master-plan.md`](master-plan.md) (the roadmap) and the Mid-1 rubric (`references/university/`) |
| Rule | A row says **Done** only if it can be shown today by a command or a file. Everything else says what is missing |
| Written by | The AI assistant that did the implementation (see [`ai-usage-log.md`](../registers/ai-usage-log.md)); not yet reviewed by the team |

## 1. Bottom line

A working vertical slice exists and runs on the author's machine: run a five-step multi-agent workflow on real retail data with a real local model, detect a silent failure with executable checks, rank where it began, prove it by replays with controls, record a human decision, and export a report. It is covered by automated tests and was driven end to end in a browser.

**Since 2026-10-09:** the code is on GitHub and CI passed there, including the container build and an end-to-end smoke test inside the container ([CI run 37924480165](../../evidence/repo/2026-10-09_ci-run-37924480165.md)).

**Not yet true, and the panel will ask about each:** nothing is deployed (a Render blueprint is ready, see the setup manual); `main` is not protected and there is no release tag; no member has demonstrated understanding of the code (the handbook's walkthrough); no report text exists; per-member pull-request evidence does not exist; the Mid-1 date is unknown.

## 2. Measured today (2026-10-07)

| Gate | Result | How to reproduce |
|---|---|---|
| Core library tests | 207 passed, 98% line coverage | `cd packages/granite_core && pytest --cov=granite_core` |
| Refund Desk tests | 49 passed, 95% | `cd workflows/refund_desk && pytest --cov=refund_desk` |
| API tests | 67 passed, 97% | `cd apps/api && pytest --cov=granite_api` |
| Web tests | 29 passed (includes automated accessibility checks) | `cd apps/web && npm test` |
| **Total** | **352 tests**, all passing, including failure cases (hostile expressions, provider down, illegal transitions, tampered evidence, rate limit, restart recovery) | |
| Lint | ruff clean on all Python; ESLint clean on the web app | `ruff check .`, `npm run lint` |
| Types | mypy strict clean (three packages); `tsc --noEmit` clean | `mypy granite_core` etc. |
| Security scan | bandit: no medium or high findings; `pip-audit` and `npm audit`: no known vulnerabilities | see the setup manual, section 6 |
| Generated files in step with code | trace JSON Schema, state machine, data flow and ER diagrams | `python scripts/export_trace_schema.py --check`, `python scripts/export_diagrams.py --check` |
| Workspace hygiene | 0 structure problems; 0 broken links | `python scripts/check_workspace.py`, `python scripts/check_links.py` |
| Smoke test on a live server | passed (run completes with one finding) | `bash scripts/smoke-test.sh <url>` |
| Clean install check | three packages installed non-editable in a fresh environment with container-style settings: UI served, run completed | repeated by hand; not automated |
| Real-model recording | 249 real answers of `llama3.2:3b` saved in `data/cassettes/refund_desk_v1.json` | `scripts/record_cassettes.py` |

Coverage and test counts include tests written by the same assistant that wrote the code; they show the code does what its author intended, not that the intent is right. The feasibility run below is the first check against something the code was not tuned on.

Functional requirements for Mid-1 (19 in the plan): see [requirements-trace.md](requirements-trace.md) for the status of each (done, partly met, not met) with implementation and tests. Two deviations from the plan's wording are recorded as change C-02g and C-02h in the [change log](../registers/change-log.md).

## 3. Feasibility validation (pre-registered)

Protocol: [`research/eval/prereg-v1.md`](../../research/eval/prereg-v1.md) (10 tasks, one fault, one small model, thresholds fixed before the run). Results and how to read them: [`research/eval/results/2026-10-07_refund-desk-feasibility-notes.md`](../../research/eval/results/2026-10-07_refund-desk-feasibility-notes.md).

| Metric | Result | Threshold |
|---|---|---|
| M1 detection | 10/10 | at least 90%: met |
| M2 false alarms on clean runs | 0 (one finding was a true natural failure) | 0: met |
| M3 top-1 attribution | 10/10 | at least 80%: met |
| M4 origin CONFIRMED | 9/10 (one miss: a second, masked fault) | at least 80%: met |
| M5 innocent step REFUTED | 10/10 | at least 80%: met |
| M6 runs completed | 20/20 | at least 95%: met |

Read the caveats before quoting: ten tasks, one fault, one small model; four tasks were not blind; the attribution test is easy by construction because the origin step has its own check; the plan's stricter criterion (95% over 20 runs) was not measured.

## 4. Mid-1 rubric rows (plan section 26 traceability, R-M1-xx)

| Rows | Requirement | Status | Evidence or gap |
|---|---|---|---|
| 09 | UI screens | Partly | Screens exist, checked in a browser at desktop and phone width, light and dark; automated accessibility audit passed ([record](../../evidence/reports/2026-10-07_accessibility-audit.md)); screenshots in [evidence/demos](../../evidence/demos/). No deployed slice, no manual accessibility or usability test |
| 12 | Structure design | Partly | [Architecture](../diagrams/architecture.md). No class or component diagram in a report |
| 13 | Behaviour design | Partly | [State machine](../diagrams/finding-state-machine.md), [data flow](../diagrams/refund-desk-dataflow.md), [sequence](../diagrams/verification-sequence.md). No activity diagram, DFD levels or data dictionary |
| 14 | Schema and ER | Partly | [ER diagram](../diagrams/database-schema.md) generated from the real tables. No migration history |
| 15 | Data structure and algorithm design | Partly | [ADR-004](../adr/adr-004-ast-check-dsl.md), [005](../adr/adr-005-provenance-first-attribution.md), [006](../adr/adr-006-vr1-verdict-rule.md). Not yet written up in report form |
| 16 | Comments and naming | Partly | Lint rules enforced (ruff E, F, I, B, C90, UP; mypy strict). The conventions are not extracted into one page |
| 17 | Static analysis | **Done** | ruff, mypy strict, bandit, pip-audit, ESLint, tsc, npm audit run on every push; [CI run 37924480165](../../evidence/repo/2026-10-09_ci-run-37924480165.md) |
| 18 | Unit tests (at least 30 including failures) | **Done** | 352 tests |
| 19 | CI/CD on GitHub | Partly | CI: **done**, four jobs green on GitHub including Docker build and smoke test ([CI run 37924480165](../../evidence/repo/2026-10-09_ci-run-37924480165.md)). CD: not yet; no hosted service, `main` not protected |
| 20 | Deployment diagram | Partly | In [architecture](../diagrams/architecture.md); two of three targets do not exist yet |
| 21 | System-level tests | Partly | Journey and error tests through the HTTP API ([`test_journeys.py`](../../apps/api/tests/test_journeys.py), [`test_platform.py`](../../apps/api/tests/test_platform.py)). No Playwright browser tests |
| 22 | Setup and tool manuals | Partly | [Setup](../manuals/setup-manual.md), [tool](../manuals/tool-manual.md) written. Not yet followed by a second person |
| 23, 24 | Working code and demo; core module with CI/CD on a live interface | Partly | Works locally; **no live URL, no tag** |
| 26 | Previous actions addressed (A1 to A6) | Drafted | [Panel action register](../registers/form-10-panel-actions.md), with the open gaps |
| 27 | Milestone log, recovery plan | Drafted | [Milestone log](../registers/milestone-log.md) |
| 28 | Code walkthrough by each member | **Not started** | Must be done by the members; this cannot be produced for them |
| 29 | A module validated beyond the happy path | **Done** | Clean run, REFUTED verdict, provider down, unrecorded task, illegal transitions: tests and the browser run |
| 30 | Repository evidence (tags, timeline, tasks, ownership) | **Not started** | Needs the members' own commits and pull requests |
| 32 | ADRs 001 to 010 | Drafted | [`docs/adr/`](../adr/). Owners and reviewers unassigned; "evidence of understanding" sections intentionally blank |
| 33 | Licences, data, ethics secured | Partly | [Licence register](../registers/dependency-licence-register.md) drafted; open items listed there. No consent template |
| 35 | Traceability matrix | Partly | [Functional requirements to code and tests](requirements-trace.md), generated and checked in CI (a missing Mid-1 requirement, a missing file or a missing test fails the check). Rubric rows are mapped by hand in this table; non-functional requirements are not traced yet |
| 36 | Dependency register | Drafted | [Register](../registers/dependency-licence-register.md) |
| 38 | Risk, security, privacy, limitations | Partly | [Defect list](../registers/defect-list.md) records open gaps. **FR-SEC-01 (redaction before storing) is not met** |
| 01 to 08, 25, 37, 39 to 43 | Report chapters, template, bibliography, meeting records | **Not started** | Must be written by the members in their own words in the prescribed LaTeX template. The documents above can serve as input, not as the text |
| 31 | Requirements baselined with stakeholders | **Not started** | No interviews recorded |
