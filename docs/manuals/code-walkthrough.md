# Code walkthrough

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-10-11 |
| Status | Study guide for the team. File names, function names and line counts were read from the code on this date |
| Purpose | The Mid-1 rubric (criterion 8) and the handbook ask each member to explain the code at file and function level, including code written with AI tools. This page is the map for that |

**Read this first.** Most of this code was written in AI-assisted sessions (see the [AI usage log](../registers/ai-usage-log.md) and [Form 13](../registers/form-13-genai-disclosure.md)). That is allowed only if the team can explain, justify and change it. Reading this page is not the same as understanding the code: open each file, run its tests, change one constant and predict which test fails. The last section says how.

## 1. The shape in one minute

```
apps/web  ──HTTP──►  apps/api/granite_api  ──calls──►  packages/granite_core   (pure: no web, no database, no network)
 React UI             FastAPI, database, jobs    │
                                                 └─────►  workflows/refund_desk  (the system being investigated)
```

Dependencies point one way. The core does not know that a database or a web server exists, which is why its 207 tests run in seconds and why its algorithms can be checked on their own. [`check_architecture.py`](../../scripts/check_architecture.py) fails the build if that rule is broken. Diagram: [layer diagram](../diagrams/architecture.md).

## 2. Follow one request through the code

**"Run workflow" is pressed** ([run sequence](../diagrams/behaviour.md)):

| # | File | Function | What happens |
|---|---|---|---|
| 1 | `apps/web/src/pages/NewRun.tsx` | `NewRun` | Form posts the task; field errors from the server are shown next to each field |
| 2 | `apps/api/granite_api/routes.py` | `create_run` | Checks the token and rate limit, hands over to the service, returns 202 with a job id |
| 3 | `apps/api/granite_api/services/runs.py` | `create_run`, `run_job` | Validates the task (`RefundTask` in `registry.py`), stores a queued run, starts a background job |
| 4 | `packages/granite_core/granite_core/runner.py` | `run_workflow` | Executes the five steps in order, records each step's inputs and outputs into a `TraceV1`, applies the fault if one was asked for |
| 5 | `workflows/refund_desk/refund_desk/steps.py` | `intake` … `writer` | The agents. Three call the language model through `LLMProvider`; order lookup is a tool call and policy is plain code |
| 6 | `apps/api/granite_api/services/analysis.py` | `persist_outcome` | Stores the trace and its hash, runs the checks, opens findings, ranks hypotheses, writes evidence |
| 7 | `packages/granite_core/granite_core/checks.py` | `evaluate_checks`, `derive_findings` | Each check is an expression evaluated by the safe language in `dsl.py`; a failed outcome check becomes a finding |
| 8 | `packages/granite_core/granite_core/attribution.py` | `attribute` | Walks the data flow backwards from the symptom and ranks suspect steps |

**"Verify" is pressed** ([verification sequence](../diagrams/verification-sequence.md)):

| # | File | Function | What happens |
|---|---|---|---|
| 1 | `apps/api/granite_api/services/experiments.py` | `create_experiment`, `experiment_job` | Checks that a repair rule exists for the step, stores the experiment, starts a job |
| 2 | `packages/granite_core/granite_core/verification.py` | `build_intervention`, `plan_replay` | Works out the corrected value (from the source of truth or the step's contract) and which steps to keep and which to re-run |
| 3 | `packages/granite_core/granite_core/experiment.py` | `run_experiment` | N replays with the correction, M controls without it, each with its own seed |
| 4 | `packages/granite_core/granite_core/verification.py` | `decide`, `wilson` | Rule VR-1 turns the counts into confirmed, refuted, inconclusive or error |
| 5 | `packages/granite_core/granite_core/lifecycle.py` | `transition` | The finding moves state only if the lifecycle allows that event; otherwise `IllegalTransition` |

## 3. Module by module

Line counts include comments and blank lines.

### `packages/granite_core` (the engine: 13 files, 207 tests)

| File | Lines | What it is | Be ready to explain |
|---|---|---|---|
| `trace.py` | 103 | `TraceV1`, `Step`, `RunInfo`: the record of a run. Everything else reads this | Why a step declares its `reads`; what `context()` returns |
| `runner.py` | 296 | Executes a `WorkflowDef`; re-executes from a step for replays | How a replay keeps upstream outputs fixed; where the fault is applied; what happens when a step raises |
| `dsl.py` | 475 | The check language: parser and evaluator over a whitelist of syntax nodes | Why `eval` is never used (ADR-004); the limits (500 characters, 150 nodes, depth 14); what a hostile expression does |
| `checks.py` | 178 | `CheckDef`, `evaluate_checks`, `derive_findings` | Pass, fail, abstain, error; why a missing field is "abstain" and not "fail" |
| `lineage.py` | 81 | Data-flow edges from the declared reads | `ancestors_with_distance`; why lineage is declared and not guessed |
| `attribution.py` | 179 | `attribute`: ranked origin hypotheses | The weights, the 0.7 origin threshold, the distance decay; what happens when no step has direct evidence |
| `verification.py` | 230 | `decide` (VR-1), `wilson`, `plan_replay` | Thresholds 0.8 and 0.2; why controls exist; the regression guard; why small N gives a wide interval |
| `experiment.py` | 93 | `run_experiment`: runs the N + M replays | Seeds; what "completed" means for a replay |
| `lifecycle.py` | 90 | Finding states and `TRANSITIONS` | Which events are legal from which state; the four verification levels |
| `evidence.py` | 55 | `make_evidence`, `verify_evidence`, canonical JSON, SHA-256 | Why the JSON is canonical before hashing; what "hash matches" in the UI checks |
| `llm.py` | 167 | `LLMProvider`, cassette, `RecordedProvider`, `RecordingProvider` | How the cassette key is built; why a missing answer raises instead of inventing one |
| `redaction.py` | 60 | `Redactor`: replaces personal data with stable tokens | **Written and tested but not applied to stored traces** (defect D-07). Say so |

### `workflows/refund_desk` (the system under investigation: 5 files, 49 tests)

| File | Lines | What it is | Be ready to explain |
|---|---|---|---|
| `definition.py` | 82 | `build_workflow`: steps, their reads, the seven checks, the repair rules | Why checks live with the workflow and not in the core |
| `steps.py` | 189 | The five agents | Which three use the model; how model output is parsed and what happens if it is not valid JSON |
| `faults.py` | 48 | `StalePriceFault` | That the fault is rule-based and its ground truth is hidden from the analysis |
| `store.py` | 146 | Orders and catalogue; the independent source of truth | Why the workflow's lookup and the source of truth are separate objects |

### `apps/api/granite_api` (HTTP, database, jobs: 20 files, 71 tests)

| File | Lines | What it is | Be ready to explain |
|---|---|---|---|
| `main.py` | 105 | `create_app`: wiring, middleware (body size, security headers) | What runs at start-up; `recover_interrupted` |
| `routes.py` | 301 | Sixteen endpoints, thin handlers | Status codes: 202 for jobs, 409 for an illegal transition, 422 for bad input, 429 for the rate limit |
| `schemas.py` | 209 | Request and response models | Where the input limits are declared |
| `models.py` | 235 | Twelve tables | Why evidence and audit rows have no update path; the [ER diagram](../diagrams/database-schema.md) |
| `services/*.py` | about 560 | One file per use case: runs, analysis, experiments, reviews, report | Transactions (`session_scope`); what is stored when |
| `jobs.py` | 88 | Thread pool plus a job row | What a restart does to a running job |
| `llm_factory.py`, `providers.py` | 164 | Live or recorded answers; Ollama and OpenAI-compatible clients | `auto` mode; the cached reachability probe (defect D-22) |
| `errors.py` | 66 | RFC 7807 problem responses | Why internal exception text never reaches the client |
| `views.py` | 154 | Rows to response objects; the graph | Derived fields such as `allowed_actions` |

### `apps/web/src` (React: 16 files, 32 tests)

| File | What it is |
|---|---|
| `App.tsx`, `hooks.ts` | Shell, hash routing (`useRoute`), data loading (`useLoad`), server status |
| `api.ts`, `types.ts` | One typed function per endpoint; errors become `ApiError` with per-field messages |
| `pages/Home.tsx`, `NewRun.tsx`, `RunDetail.tsx`, `FindingDetail.tsx`, `Guide.tsx` | The five screens |
| `components/Graph.tsx`, `Verify.tsx`, `Outcome.tsx`, `Filters.tsx`, `ui.tsx` | Pipeline graph (keyboard-operable SVG), verification table, verdict and review, search, small shared pieces |

## 4. Questions a supervisor may ask, and where the answer is

| Question | Short answer | Show |
|---|---|---|
| How do you know the outcome is wrong without an answer key? | A check compares the outcome with a source of truth the workflow does not control | `definition.py` (CHK-OUT-1), `store.py` |
| Why is the first hypothesis first? | Its own output contradicts the source of truth (weight 1.0), which outranks a broken contract (0.8) | `attribution.py` `WEIGHTS`; [algorithm design](../diagrams/algorithm-design.md) |
| What stops "confirmed" being luck? | Controls: the same replays without the correction must stay wrong (at most 20%) while the corrected ones are right (at least 80%) | `verification.py` `decide` |
| What if the model is down? | The run ends as "errored" with the reason, a finding is opened for it, and "Run again" is offered; recorded mode needs no model | `runner.py`, `services/runs.py`, tests `SYS-ERR-07` and `SYS-ERR-04` |
| Can a user run code through a check? | No. Expressions are parsed into a whitelist of nodes; names, calls and attribute access outside it are refused | `dsl.py`; `test_dsl.py` hostile cases |
| What if two people review at once, or someone rejects an accepted finding? | The lifecycle refuses the second event with 409 | `lifecycle.py` `TRANSITIONS`; test `SYS-ERR-03` |
| What is not finished? | Redaction before storage, a second workflow, import, a deployed URL, usability tests | [Defect list](../registers/defect-list.md), [execution status](../plan/execution-status.md) |
| The rank and the score disagree for the last three suspects. Why? | Rank orders by evidence strength, then upstream first; the score also decays with distance from the symptom. Within one evidence class they can differ. Known, logged as D-25 | the sort in `attribute`, `attribution.py` |

## 5. Who owns what

Ownership below is the **plan** (master plan section 34.1). The right-hand column is what the git history shows today, and it does not yet match.

| Area | Planned owner | Files | Visible in git history since 6 October |
|---|---|---|---|
| Workflows, runner, model providers, web shell | Shahoud Shahid | `runner.py`, `llm.py`, `workflows/refund_desk`, `apps/web` | All commits since 6 October are from one account (Shahoud) |
| Checks, check language, attribution, evaluation | Muhammad Noor | `dsl.py`, `checks.py`, `lineage.py`, `attribution.py`, `research/eval` | No commit yet |
| Verification, lifecycle, API, database, CI/CD | Saif Shahzad | `verification.py`, `experiment.py`, `lifecycle.py`, `apps/api`, `.github` | No commit yet |

This gap is the largest open risk for rubric criteria 6 and 8. It cannot be closed by writing documents. It closes when each owner makes real changes to their area through their own pull requests (see [CONTRIBUTING](../../.github/CONTRIBUTING.md)) and can pass the exercise below.

## 6. Proving you understand a module (do this before the meeting)

For each file you own:

1. **Explain** it aloud in two minutes without the screen.
2. **Predict:** change one constant (for example `CONFIRM_MIN_RATE` from 0.8 to 0.9 in `verification.py`), say which tests will fail, then run them.
3. **Break it:** remove one guard (for example the depth limit in `dsl.py`) and find the test that catches it.
4. **Extend it:** add one small thing through a pull request, with a test. Suggestions are in the [defect list](../registers/defect-list.md) (D-07 redaction, D-25 score order).
5. **Write** the "Evidence of understanding" paragraph at the end of the matching [ADR](../adr/) in your own words.
