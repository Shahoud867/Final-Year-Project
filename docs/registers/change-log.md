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
