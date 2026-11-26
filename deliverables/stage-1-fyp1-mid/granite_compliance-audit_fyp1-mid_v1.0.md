# Granite (F26-060): FYP-1 Mid compliance audit

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-10-11 |
| Scope | Every FYP-1 mid requirement **except the report** (the report and Form 3 are a separate deliverable and are not audited here) |
| Authorities, in order | 1. BS FYP Handbook 2026 (Table 1a, page 11; "what good looks like", page 27; Form 10, page 45). 2. FYP-1 Mid Evaluation Guidelines and Rubrics (Form 2 and its red flags). 3. The faculty requirement for the mid evaluation. 4. The panel comments from the proposal defense. All four are in [`references/university/`](../../references/university/) or quoted in the [master plan](../../docs/plan/master-plan.md) |
| Method | Each requirement was matched to an artefact, the artefact was opened or executed on this date, and the result is written next to it. "Verified" means a command was run or a screen was operated today; anything else says "written, not run" or "not done" |
| Prepared with | AI assistance (see the [AI usage log](../../docs/registers/ai-usage-log.md)). The team must read, check and own it before presenting it |

**This audit does not predict marks.** It shows where each criterion is met, where it is not, and what limits it.

## 1. Result at a glance

| Area | State |
|---|---|
| Working product, core module, edge cases | **Met and verified.** Eight features, 381 automated tests passing, browser walkthrough done today |
| Design artefacts (Table 1a) | **Met.** All listed artefacts provided, generated from the code, CI-checked |
| Development phase (comments, naming, static analysis, unit tests) | **Met and enforced** by lint and type rules in CI |
| Testing, including system level | **Met and verified** locally |
| CI | **Met**, green on GitHub for the last pushed commit; today's additions are not pushed |
| CD and deployment | **Not met.** Written, never run; nothing is deployed |
| Panel actions | Four of five panel comments done with evidence; UI/UX partly (no usability evidence); faculty CI/CD requirement partly |
| Repository and member evidence | **Weak.** One account produced all implementation commits; no pull requests, tags or protected branch |
| Team ownership of AI-assisted code | **Not demonstrated.** Study material is provided; only the members can close this |

## 2. Form 2 rubric, criterion by criterion

| # | Criterion (marks) | What the rubric looks for | Where it is satisfied | Changed in this pass | Verified how, and result | What still limits it |
|---|---|---|---|---|---|---|
| 1 | Previous proposal actions addressed (10) | Register with each required change, status and live evidence link | [Form 10 register](../../docs/registers/form-10-panel-actions.md) | Rebuilt on the handbook's Form 10 columns; every status re-checked; evidence links added | Each link opened by the link checker; each "Done" exercised in the product today | A1 (UI/UX) is Partly: no usability test. A6 (CI/CD) is Partly: nothing deployed. Change record C-01 is unsigned |
| 2 | Iteration plan and work breakdown progress (10) | Planned milestone completed, or delay justified with an owner-assigned recovery plan | [Milestone log and iteration plan](../../docs/registers/milestone-log.md) | Work breakdown with planned owner, planned and actual dates; delays with cause, action, owner and date; Iteration 2 plan with risks | Compared with the repository state today | Four items late (CD, deployment, branch protection and pull requests, walkthroughs). The Mid-1 date is unconfirmed |
| 3 | Live prototype with core module demo (25) | Meaningful core module works live, not screenshots; edge and failure cases shown | The product: [`apps/`](../../apps/), [`packages/`](../../packages/), [`workflows/`](../../workflows/). [Feature catalogue](../../docs/manuals/feature-catalogue.md), [demo runbook](../../docs/manuals/demo-runbook.md) | Guide page; plain validation messages; explanation when a verification cannot run; faster health check; runbook with eight failure cases | Exercised today on the running product. In a browser: guide, invalid input, run, checks and graph, finding, verify (confirmed; and no verdict, with the reason), review (comment guard, ask for information, accept). Through its HTTP API on the same server: clean run, unrecorded task, unreachable model, unknown fault, cancelled order, illegal transition, filters, JSON report. [Screenshots](../../evidence/demos/). 22 system tests pass | One workflow, one fault type. Recorded model answers by default; live mode needs a local model and was not exercised today. No deployed instance |
| 4 | Requirements and acceptance criteria quality (10) | Precise, testable FRs and NFRs connected to the implementation | [Requirements trace](../../docs/plan/requirements-trace.md) (requirement, status, code, test); [system test catalogue](../../docs/manuals/system-test-cases.md) (each case names its requirement); input rules in the [data dictionary](../../docs/diagrams/data-dictionary.md) | System cases carry requirement ids, steps and expected results, generated from the tests | `check_traceability.py --check` passes; `build_test_docs.py --check` passes | FR-SEC-01 (redaction before storage) is **not met** and says so. The SRS text itself belongs to the report |
| 5 | Design artefacts and design evolution (15) | Architecture, data, process and behaviour artefacts match the code; changes justified | [Design pack index](../../docs/diagrams/design-pack.md); [interactive pack](granite_design-pack_fyp1-mid_v1.0.html); [ADRs](../../docs/adr/); [change log](../../docs/registers/change-log.md) C-01 to C-03 | 21 diagrams and a data dictionary generated from the code; old hand-written diagrams archived; C-03 records the evolution | `build_design_pack.py --check` passes (fails on any drift or layout fault); `check_architecture.py`: 0 violations; every diagram was looked at | Most layouts are arranged by hand (the facts in them are checked against the code, the arrangement is not). The members must be able to explain each diagram, or the rubric's "generated without understanding" band applies |
| 6 | Repository, milestone and member evidence (10) | Tagged code, commit timeline, task log, member ownership visible in the repository | [Repository evidence](../../evidence/repo/2026-10-11_repository-evidence.md); [CONTRIBUTING](../../.github/CONTRIBUTING.md); [pull request template](../../.github/pull_request_template.md); [ADR-010](../../docs/adr/adr-010-git-branching.md) | Honest timeline per member; working method written; recovery steps | Read with `git` and `gh` today | **The weakest criterion.** No tags, no pull requests, `main` unprotected; all nine implementation commits from one account in four days; today's work uncommitted |
| 7 | Testing and early validation (10) | Tests exist for the current module; a failure or edge case is discussed | [Test results, 2026-10-11](../../evidence/reports/2026-10-11_test-results.md); [system test catalogue](../../docs/manuals/system-test-cases.md); [feasibility run](../../research/eval/results/2026-10-07_refund-desk-feasibility-notes.md); [defect list](../../docs/registers/defect-list.md) | System test level added (22 cases); results record generated by running the suites; 5 defects logged, 4 fixed | 381 of 381 pass: core 207 (97.5% lines), workflow 49 (95.4%), API 71 (96.8%), system 22, web 32 | Tests and code share an author. Validation is 10 tasks, one fault, one small model. No test with a live model in CI |
| 8 | Presentation, Q&A, team and tool ownership (10) | Coordination clear; tool-assisted output defended and understood | [Code walkthrough](../../docs/manuals/code-walkthrough.md); [AI usage log](../../docs/registers/ai-usage-log.md); [Form 13](../../docs/registers/form-13-genai-disclosure.md); [demo runbook](../../docs/manuals/demo-runbook.md) | File and function map, likely questions, an exercise to prove understanding, disclosure updated | Function names and paths checked against the code; the "change a threshold" exercise was run (4 tests fail as described) | **Cannot be satisfied by documents.** No member has yet demonstrated understanding. This is a person-by-person result on the day |

## 3. Handbook Table 1a, artefact by artefact

"Select the design that is appropriate for your project": none was judged not applicable; where the handbook offers a choice, both are provided.

### Design phase

| Table 1a artefact | Provided as | How it is kept true to the code |
|---|---|---|
| Domain model / class diagram | [`domain-model.svg`](../../docs/diagrams/domain-model.svg) | Field names checked against the classes at build time |
| Component diagram | [`component-diagram.svg`](../../docs/diagrams/component-diagram.svg) | Arrows correspond to imports shown in the generated call graph |
| Layer diagram | [`layer-diagram.svg`](../../docs/diagrams/layer-diagram.svg) | The dependency rule is enforced by `check_architecture.py` |
| Structure chart | [`structure-chart.svg`](../../docs/diagrams/structure-chart.svg) | Real function names, cross-checked by the call graph |
| Flow diagram | [`investigation-flow.svg`](../../docs/diagrams/investigation-flow.svg) | Statuses are the states of the generated state machine |
| Data flow diagrams | [`dfd-context.svg`](../../docs/diagrams/dfd-context.svg), [`dfd-level-1.svg`](../../docs/diagrams/dfd-level-1.svg) | Stores are the tables of the ER diagram |
| Data dictionary | [`data-dictionary.md`](../../docs/diagrams/data-dictionary.md) | Generated: 12 tables and 120 columns from the database models; a column without a meaning fails the build |
| Activity diagram | [`activity-investigation.svg`](../../docs/diagrams/activity-investigation.svg) | Five swimlanes; activities are the modules of the structure chart |
| State machine; graph | [`finding-state-machine.svg`](../../docs/diagrams/finding-state-machine.svg); [`refund-desk-dataflow.svg`](../../docs/diagrams/refund-desk-dataflow.svg) | States and transitions read from `lifecycle.TRANSITIONS`; the lineage graph is fully generated from the workflow definition |
| Call graph; sequence diagrams | [`call-graph.svg`](../../docs/diagrams/call-graph.svg); [`run-sequence.svg`](../../docs/diagrams/run-sequence.svg), [`verification-sequence.svg`](../../docs/diagrams/verification-sequence.svg) | Call graph computed from the source (38 functions, 49 calls) |
| Interaction overview diagram | [`interaction-overview.svg`](../../docs/diagrams/interaction-overview.svg) | Each reference names a sequence diagram of the pack |
| Schema design / ER diagram | [`database-schema.svg`](../../docs/diagrams/database-schema.svg) | Tables, columns and keys read from the SQLAlchemy models |
| Data structure and algorithm design | [`algorithm-design.md`](../../docs/diagrams/algorithm-design.md) with four diagrams (check language, attribution, verdict rule, replay plan) | Thresholds and worked examples computed by calling the real functions on a recorded run |
| Use-case diagram (report item, provided for completeness) | [`use-case-diagram.svg`](../../docs/diagrams/use-case-diagram.svg) | Implemented and planned use cases are drawn differently |

### Development phase

| Table 1a item | Where | Evidence it is in the code, not only described |
|---|---|---|
| Comments | [Coding standards](../../docs/manuals/coding-standards.md), section 2 | ruff `D100` to `D104`: 0 missing docstrings on public modules, classes, methods, functions |
| Naming conventions | Coding standards, section 1 | ruff `N` (PEP 8 naming) and typescript-eslint: 0 findings; one documented exception |
| Static analysis | Coding standards, section 3; [`ci.yml`](../../.github/workflows/ci.yml) | Today: ruff clean; mypy strict clean (38 files); bandit clean; pip-audit and npm audit: no known vulnerabilities; ESLint and `tsc` clean; architecture check: 0 violations |
| Unit test suites and test cases | `packages/*/tests`, `workflows/*/tests`, `apps/api/tests`, `apps/web/tests` | 359 unit, integration and component tests pass; coverage gates of 90% in CI |

### Maintenance phase

| Table 1a item | Where | State |
|---|---|---|
| CI/CD | [`ci.yml`](../../.github/workflows/ci.yml), [`cd.yml`](../../.github/workflows/cd.yml) | **CI: implemented and verified** on GitHub ([record](../../evidence/repo/2026-10-09_ci-run-37924480165.md)). Steps added today (system tests, architecture check, test catalogue check) are **not yet run on GitHub**. **CD: written, not run** |
| Deployment diagram | [`deployment-diagram.svg`](../../docs/diagrams/deployment-diagram.svg) | Shows what is verified (laptop, CI) and what is planned (hosting) with different line styles |
| System-level test suites and test cases | [`tests/system`](../../tests/system/), [catalogue](../../docs/manuals/system-test-cases.md) | **Implemented and verified:** 22 of 22 pass against a real server process; 18 pass and 4 are skipped by design against an already-running server |
| Configuration / setup and tool manual | [Setup manual](../../docs/manuals/setup-manual.md), [tool manual](../../docs/manuals/tool-manual.md) | Setup steps were followed on the authoring machine. **Not yet followed by a person who is not the author** (the handbook asks for that) |

### Working code and demonstration

| Item | Where | State |
|---|---|---|
| Working code | Repository; start commands in the setup manual, section 3 | Verified today in recorded mode |
| Demonstration | [Demo runbook](../../docs/manuals/demo-runbook.md) | Scripted, and each step checked on the running product today; **not yet rehearsed by the members** |
| At least three meaningful features | [Feature catalogue](../../docs/manuals/feature-catalogue.md) | Eight, each with purpose, location and tests |

## 4. Faculty requirement for the mid evaluation

| Part of the requirement | State | Evidence or gap |
|---|---|---|
| Core module implemented | Met | Feature catalogue; test results |
| On the live interface shown at the proposal, or its improved version | Met locally | The web UI replaces the PoC console; [screenshots](../../evidence/demos/). Not hosted |
| CI pipeline, automated testing | Met | CI record; `ci.yml` |
| CD / automated deployment "where appropriate" | **Not met** | `cd.yml` and `render.yaml` are prepared; a member must create the hosting service and push |
| Meaningful branching strategy | **Documented, not practised** | CONTRIBUTING, ADR-010; the history shows direct pushes to `main` |
| Industry-style practices | Partly | Present: lint, strict types, coverage gates, security and secret scans, generated-file checks, ADRs, change log, defect list. Absent: code review, protected branch, releases |

## 5. Panel comments from the proposal defense

Full register with evidence links: [Form 10](../../docs/registers/form-10-panel-actions.md).

| Comment | Status | Main evidence | Outstanding |
|---|---|---|---|
| "UI/UX needs improvement." | Partly | Five redesigned screens, states, accessibility checks, [screenshots](../../evidence/demos/) | Usability test with outside users |
| "Features are not sufficiently clear." | Done | [Feature catalogue](../../docs/manuals/feature-catalogue.md); in-app guide | Report section |
| "It is unclear what inputs each feature will accept." | Done | Input tables; [data dictionary](../../docs/diagrams/data-dictionary.md); validation tests; a test tying the guide to the server's limits | Inputs of features not yet built |
| "It is unclear how identified flaws/issues will be verified and how verification results will be captured." | Done | Replay with controls and rule VR-1; hashed evidence, levels V0 to V3, report | Larger evaluation |
| "The overall project workflow must be redefined." | Done | One enforced workflow; [state machine](../../docs/diagrams/finding-state-machine.md); flow and activity diagrams | Supervisor's signature on change record C-01 |

## 6. Rubric red flags

| Red flag | Does it apply? | Note |
|---|---|---|
| Sudden code volumes | **Yes** | Three weeks without commits, then the product in four days. Mitigation offered: the code walkthrough and small per-owner commits from now on |
| Stagnant prototype | No | The PoC console was replaced by a working product |
| Generic GenAI R&D text | Out of scope here (report) | |
| Uneven contribution | **Yes** | See the repository evidence |
| Dishonest milestone logging | No | The log states what is late and who actually did the work |
| Ignored panel actions | No | Each is answered in Form 10 |

## 7. Handbook page 27, "what good looks like"

| Statement | State |
|---|---|
| Live module beyond PoC-lite | Met |
| Design artefacts evolved since the proposal | Met; evolution recorded in change log C-02 and C-03 |
| File and function level walkthrough showing AI-assisted output is understood | **Material ready, not demonstrated** |
| Honest milestone log with a recovery plan | Met |
| At least one module validated beyond the happy path | Met: failure cases in every suite; feasibility run with a recorded miss |

## 8. Verification log, 2026-10-11

Run on Windows 11, Python 3.11.4, Node 24, on commit `5099243` plus the uncommitted working tree.

| Check | Command | Result |
|---|---|---|
| All test suites | `python scripts/build_test_docs.py --run` | 381 of 381 passed ([record](../../evidence/reports/2026-10-11_test-results.md)) |
| System tests against a running server | `GRANITE_SYSTEM_BASE_URL=http://127.0.0.1:8791 pytest tests/system` | 18 passed, 4 skipped by design |
| Lint | `ruff check packages/granite_core workflows/refund_desk apps/api scripts tests` | Clean |
| Types | `mypy` (strict) on three packages; `tsc --noEmit` | Clean |
| Web lint, tests, build | `npm run lint`, `npm test`, `npm run build` | Clean; 32 passed; built |
| Security | `bandit -ll`; `pip-audit`; `npm audit --audit-level=high` | No findings |
| Architecture rule | `python scripts/check_architecture.py` | 0 violations in 18 files |
| Generated files | `export_trace_schema.py`, `build_design_pack.py`, `build_test_docs.py`, `check_traceability.py`, each with `--check` | Up to date |
| Workspace and links | `check_workspace.py`, `check_links.py` | See the README in this folder for the final run |
| Live walkthrough | Product started locally in recorded mode; operated in a browser, and through its HTTP API for the remaining failure cases | Behaved as the demo runbook states; two rough edges found and fixed (D-23, D-24) |

**Failures met during this pass and what was done:** the system suite first failed because the health endpoint took two seconds (fixed, D-22); one case failed with a connection reset on a refused upload (the test client now treats a closed connection as a refusal); two cases failed when the suite was repeated quickly against one server because the rate limit of 120 changes per minute was reached (expected behaviour; passes on a fresh window); a verification ended with no reason given (fixed, D-23).

## 9. Not verified, and why

| Item | Why |
|---|---|
| Today's CI changes and the CD workflow on GitHub | The team chose to commit and push themselves; nothing was pushed |
| Container build on a laptop | The Docker daemon was not running; CI built it on 9 October |
| Live model mode | No local model was running today; the recorded answers are real answers of `llama3.2:3b` |
| Deployment | No hosting account exists; creating one is the team's action |
| Setup by a non-author | Needs a second person |
| Member understanding | Needs the members |

## 10. Actions only the team can take, in order

1. **Read and commit** the pending work in small commits, each member their own area, then push and confirm that CI is green.
2. **Each member** does the understanding exercise for their module (code walkthrough, section 6) and rehearses the demo alone.
3. **Create the Render service**, add the deploy hook and URL, confirm the CD run, record it.
4. **Protect `main`**, open one pull request each, tag `v0.1.0-mid1`.
5. **Confirm the Mid-1 date** and bring change record C-01 for signature.
6. **Usability check** with three outside users.
