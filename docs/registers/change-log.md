# Change log

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-10-07 |
| Status | C-01 drafted; **not yet approved** by the supervisor |
| Rule | Entries are appended, never edited after approval (handbook C.5.3). Record a change *before* its results are known |

## C-01: Workflow redefined around the verified finding

The full record, as drafted in the plan, is in `docs/plan/master-plan.md` section 11.4. In short: modules renamed, mechanisms remapped, evaluation baseline set changed, Tier-2 gates resolved by design, deployment target Render plus Docker Compose.

| Field | Content |
|---|---|
| Approved by / date | Dr. Adil Majeed / **not yet signed** |
| Made before results? | The baseline change was made before any evaluation result existed. Since then (2026-10-07) one pre-registered feasibility run has been executed (`research/eval/prereg-v1.md`); it does not change C-01 |
| Status | Open until signed |

## C-02: Implementation decisions taken during execution (for the supervisor to note)

| # | Change from the plan | Why | Effect |
|---|---|---|---|
| a | Finding lifecycle gains two transitions: Inconclusive to Verifying, and Refuted to Verifying | An inconclusive verdict is resolved by running more replays, and a refuted hypothesis is followed by verifying the next one; without these the review workflow dead-ends | State machine in master plan 13.3 updated |
| b | Trace stored as one JSON document per run; steps and edges derived on read | One source for hashing and replay; fewer tables to keep consistent | Plan's step and step_edge tables not created ([ADR-003](../adr/adr-003-persistence-sqlalchemy.md)) |
| c | Ruff line length 120 (plan said 100) | Readability of the DSL and check text | None |
| d | Mid-1 check set is 7 checks (plan: at least 4) | Two outcome checks and five step contracts are needed to give attribution evidence at every step | More coverage than planned |
| e | Persistence redaction (FR-SEC-01) not applied to stored traces | Replays need the original task input; the demo data is synthetic | **Open requirement gap**, logged in [`defect-list.md`](defect-list.md) |
| f | Refund Desk's policy step is deterministic code, not a language model | Plan allows this simplification; it keeps the policy a reliable reference | None |
| g | Model-call timeout: 30 s for hosted endpoints (as FR-RUN-04), **120 s for local Ollama** | A CPU-only 3B model needs 5 to 35 s per call under load; a 30 s limit would fail runs that are only slow. Configurable with `GRANITE_LLM_TIMEOUT` | Deviation from FR-RUN-04 for the local default |
| h | One finding per failing outcome check, each with its own severity | Different outcome checks fail at different steps, so each needs its own symptom and hypotheses. FR-CHK-04 words it as one finding with the maximum severity | Deviation from FR-CHK-04; the supervisor should say which reading is wanted |
| i | Reviewer decision `request_info` is recorded but leaves the finding status unchanged | The plan's state machine (13.3) has no needs-info state | FR-REV-01 met without changing the state machine |
| j | Findings list filters in the API: status, severity, level, date range, text; the page offers text, severity and level; 25 per page | FR-HIS-01 basic | No project filter (one project exists) |
| k | Finding report as Markdown and JSON | FR-REP-01 (PDF stays Final-1) | None |

Items g to k came from reading the plan's acceptance criteria against the first implementation on 2026-10-07; the traceability file [`docs/plan/requirements-trace.md`](../plan/requirements-trace.md) lists the state of every requirement.

## C-03: Design and process changes made on 2026-10-11 (for the supervisor to note)

| # | Change | Why | Effect |
|---|---|---|---|
| a | The diagrams are now generated from the code by `scripts/build_design_pack.py` (21 diagrams, a data dictionary, one interactive file) and replace the hand-written Mermaid pages | A hand-drawn diagram drifts from the code; the rubric gives 4 to 6 of 15 when diagrams conflict with the implementation. Tables, states, data flow, call edges, thresholds and the worked examples are read from the code, and CI fails if a diagram is out of date | Old exporter archived; `docs/diagrams/` regenerated |
| b | Branching simplified to short-lived branches into `main` (no `develop`) | See ADR-010, revision of this date | `.github/CONTRIBUTING.md`, pull request template |
| c | A system test level added (`tests/system`, 22 black-box cases over real HTTP), with a catalogue generated from the tests | The handbook's maintenance phase asks for system-level test suites; unit and integration tests alone do not show that the assembled product works | Two product defects found and fixed (D-22, D-23) |
| d | Delivery workflow added: image to the GitHub Container Registry after CI, deploy to Render through a hook, release on tag | The faculty requirement asks for CI/CD; `autoDeploy` on Render would deploy commits that had not passed CI | Written, **not yet run** |
| e | Cyclomatic complexity limit is 12 (plan: 10) | Two functions, the expression evaluator and the attribution ranking, are clearer whole than split | Recorded in the coding standards |
| f | The architecture rule is checked by a small script (`scripts/check_architecture.py`), not by import-linter as planned | Same guarantee with no extra dependency | In CI |
| g | An in-app guide page lists each feature with its inputs and outputs | Panel actions A2 and A3 asked for exactly this; a document would not be seen in a demo | `apps/web/src/pages/Guide.tsx`, kept equal to the server's limits by a test |
| h | Docstrings are required on every public module, class, method and function (ruff `D100` to `D104`), and PEP 8 naming is linted (`N`) | The handbook's development phase lists comments and naming conventions; a rule that is not enforced decays | 167 docstrings added |

