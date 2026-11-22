# Change log

| | |
|---|---|
| Version | 1.1 |
| Date | 2026-10-14 |
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

## C-04: Interface redesign of 2026-10-14 (for the supervisor to note)

Scope: the web interface only. No feature was added or removed, no API endpoint or response changed, and the finding state machine, the checks, attribution and rule VR-1 are untouched. Made on branch `feat/web-workbench-redesign`; not merged or deployed when this entry was written.

| # | Change | Why | Effect |
|---|---|---|---|
| a | The five screens were rebuilt as one workbench: Investigations (telemetry and trace inspector), Task Studio, Pipeline trace with a step inspector, Verification lab, How it works; a sixth screen, Evidence, was added | Panel action A1 ("UI/UX needs improvement") and the Mid-1 criterion for a live core module: the earlier screens worked but read as a developer console | `apps/web/src`; screenshots in `evidence/demos/` dated 2026-10-14. "Improved" remains a claim until the usability check is run |
| b | Dark theme is the default; a light theme is one click away | The plan (17.4) said light by default for projectors. The redesign brief specified a dark observability palette; the light theme is kept for projection | Both themes are in `src/styles/tokens.css` |
| c | Three runtime packages were added to the web app: `lucide-react` (icons), `@fontsource-variable/inter` and `@fontsource-variable/jetbrains-mono` (fonts served from our own origin) | The web README had said "no UI library, to keep dependencies few". Icons and two fonts are needed for a professional interface; a component library was still not adopted | Recorded in the [dependency register](dependency-licence-register.md); `npm audit` reports no known vulnerability |
| d | The pipeline graph stays a linear SVG and is now drawn responsively (vertical on narrow screens). A graph library for branching workflows was not adopted | The only workflow is linear; a graph library would add risk without use before FYP-2 | Defect D-14 closed. Branching graphs are listed as planned for FYP-2 on the Evidence screen |
| e | The server's content-security policy now allows requests to `https://api.github.com` and names `font-src 'self'` | The Evidence screen reads the public status of the CI and CD workflows from GitHub so that delivery can be shown live, not claimed | One line in `apps/api/granite_api/main.py`; the browser sends no credentials to GitHub; when GitHub is unreachable the screen says "status unknown" |
| f | The container build records the commit it was built from and the interface shows it | So the running instance can be tied to a commit that passed CI | `Dockerfile` build arguments, one line in `cd.yml`, `apps/web/vite.config.ts`. Without the argument the interface says "no build stamp" |
| g | The interface carries its own copy of rule VR-1's thresholds and of the lifecycle table, used only to explain a verdict and to draw the rules | A verdict must be explained next to its numbers; fetching the rule at run time would add an endpoint | Two server tests fail if the copies differ from `verification.py` and `lifecycle.py` (`apps/api/tests/test_platform.py`). Verdicts and allowed actions still come only from the server |
| h | The form validates a task before sending it, with the server's own wording | Faster feedback; the server remains the authority and refuses the same input | Defect D-12 closed for the replay counts as well |

## C-05 (proposed on 2026-11-14, not approved): committed scope for the FYP-1 Final and the FYP-2 baseline

Drafted by the AI assistant for the team to take to the supervisor (handbook C.5.3: a change to scope is recorded and approved before it is acted on). The full table is in the [completion plan](../plan/fyp1-completion-plan.md), section 3. Nothing in this entry is in force until it is signed.

| Field | Content |
|---|---|
| What changes | The project scope is restated as 21 capabilities. Nine are built. Five are committed for the FYP-1 Final: corrections derived from the failed check; three fault types with batch generation; verified attribution in one action; an evaluation harness with baselines and two ablations; regression-test export. Seven move to FYP-2: trace import, a tau-bench Retail Agent (replacing the Math Crew, F11), a LangGraph adapter, redaction before storage, a durable hosted database, reviewer login, and the LLM second opinion with the Who&When boundary study |
| What is removed | CrewAI adapter (F14), known-fix library (F21), the LLM fix-suggestion agent (F15, replaced by check-derived corrections), PDF export, webhooks (F24), the seven-framework compatibility layer (F25) |
| Why | No product code has changed since 14 October and about three weeks remain. The master plan's Final-1 list cannot be finished, and the handbook measures progress against committed scope "unless scope formally revised". The five committed items are the ones that remove the weakness recorded in the feasibility notes: fault, check and repair rule all written by the team |
| Evidence that prompted it | [Execution status](../plan/execution-status.md), update of 2026-11-14; [feasibility notes](../../research/eval/results/2026-10-07_refund-desk-feasibility-notes.md); the vendor and paper check in the [product strategy](../plan/product-strategy.md), section 2 |
| What it affects | Master plan sections 12, 31 and 32; the FYP-2 milestone register; the report's requirements and FYP-2 plan chapters. The registered title is unchanged; the report states that repair means a corrected value verified by replay and applied only by a person |
| Made before results? | Yes. No evaluation beyond the feasibility run of 2026-10-07 exists |
| Approved by / date | Dr. Adil Majeed / **not yet signed** |
| Status | Proposed. The team has not yet discussed it |


## C-06 (recorded on 2026-11-15, not approved): how the C-05 scope was implemented

Made by the AI assistant at Shahoud Shahid's request, on branch `feat/fyp1-final-scope`, uncommitted. **Acted on before C-05 was approved**, which the handbook (C.5.3) asks teams not to do; the branch should be merged only after the supervisor signs C-05 and this entry.

| # | Change | Why | Effect |
|---|---|---|---|
| a | Interventions are derived from the failed check; Refund Desk's hand-written repair rules are removed ([ADR-011](../adr/adr-011-check-derived-interventions.md)) | Removes the "you wrote the fix yourselves" objection and a per-step cost no user would pay | A step whose own checks pass can no longer be replayed (422 "No failed check..."). Two API tests, one workflow test and two system tests were changed to say so |
| b | CT-LOOKUP and CT-INTAKE rewritten (version 2) to compare a field with its expected value; outcome check CHK-OUT-3 added (eight checks, was seven) | Needed for (a), and to detect a request that loses an item | CT-LOOKUP's observed and expected values are now item lists, not totals |
| c | Two fault types: `dropped_item` (s1), `handoff_drift` (s4); the runner supports a fault on a step's inputs (in transit) | Committed item 11 | `granite_core/runner.py`, `refund_desk/faults.py` |
| d | New tables `investigations`, `batches`, `batch_runs`; no existing table changed | Items 11 and 12; existing databases keep working (new tables are created on start) | ER diagram and data dictionary regenerated |
| e | Regression export allowed for confirmed (V2) findings, not only resolved ones (FR-REP-02 says "resolved") | So a reviewer can keep the test before closing the finding | Recorded in the traceability note |
| f | Navigation: Task Studio renamed New run; Evidence renamed Why Granite; Fault Lab and Evaluation added | New screens; names that say what the page is (frontend roadmap) | `apps/web/src/App.tsx` |
| g | `scripts/build_design_pack.py` writes the interactive pack to `deliverables/stage-2-fyp1-final/..._draft.html` instead of the frozen stage-1 file | The generator was overwriting a frozen deliverable | Stage-1 copy unchanged |
| h | `Cassette` keeps unknown top-level fields when it writes | A live recording had erased the prompt fingerprint (D-10 guard) | `granite_core/llm.py` |
| i | The Docker image includes benchmark result files (`GRANITE_EVAL_DIR`) | So the hosted Evaluation page has data | `Dockerfile`, `.dockerignore` |

| Field | Content |
|---|---|
| Made before results? | Items a to d were built and tested before the benchmark ran; the benchmark protocol was hashed before the run |
| Approved by / date | Dr. Adil Majeed / **not yet signed** |

## C-07 (proposed on 2026-11-15, not approved): integrations with Langfuse and Arize Phoenix

Drafted by the AI assistant for the team to take to the supervisor. Design and evidence: [integrations strategy](../plan/integrations-strategy.md).

| Field | Content |
|---|---|
| What changes | **FYP-1 Final (optional stretch):** one real round trip with Langfuse Cloud (FR-INT-01 to 03), replacing the earlier stretch item "JSON trace import". **FYP-2:** Langfuse connector with profiles and scheduled sync, Phoenix connector (FR-INT-04), encrypted credentials (FR-INT-05), inferred lineage and its evaluation, truth providers, replay hook. Redaction before storage (FR-SEC-01) moves to the first FYP-2 milestone as a prerequisite for real production data |
| What does not change | The five committed FYP-1 items (C-05); the core's contract (Granite Trace v1); rule VR-1 |
| Why | Teams already capture traces in these tools; reading them makes Granite usable on real applications without re-instrumenting, and writing verdicts back puts them where teams already look |
| Limits stated up front | Imported traces carry no declared data flow (it is inferred, with lower confidence) and cannot be replayed without a hook, so imported findings stop at V1 unless the application offers replay |
| Approved by / date | Dr. Adil Majeed / **not yet signed** |
| Status | Proposed; **implemented on branch `feat/fyp1-final-scope` on 2026-11-15** at Shahoud's request, with supervisor matters treated as already handled by the team (his instruction). The approval fields above are left for the team to complete; nothing is merged |
| Implemented as | Phoenix and Langfuse connectors (FR-INT-01 to 06 added to master plan section 15.2), [ADR-012](../adr/adr-012-observability-connectors.md). Departures from the strategy: Phoenix was brought forward from FYP-2 and is the platform verified live (a local Phoenix server needs no account); keys are kept in environment variables instead of encrypted in the database; HTTP uses the standard library instead of `httpx`; Langfuse reads use the v1 observations endpoint, which also works on self-hosted v3. Langfuse has only been tested against an in-memory server |
