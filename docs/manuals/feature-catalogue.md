# Feature catalogue

| | |
|---|---|
| Version | 1.1 |
| Date | 2026-10-14 |
| Status | Describes what works today. Each feature was exercised in a browser against the running product on 2026-10-11, and by the automated tests named in its card. On 2026-10-14 the interface was redesigned (same features, same API); the screen names below were updated and the main journey was walked through again in a browser |
| Answers | Panel actions A2 ("features are not sufficiently clear") and A3 ("unclear what inputs each feature accepts"); rubric criterion 3 (live core module) |

Granite does one job: when a workflow of several AI agents gives an answer that looks fine but is wrong, find the step where the error began and show the proof. The job is done in a fixed order, and each step in that order is one feature:

**Run → Check → Detect → Trace back → Verify → Review → Record**, plus **Find** to come back to earlier work.

The same list, in shorter words, is inside the product on the **How it works** page (`#/guide`), and a test keeps the limits printed there equal to the ones the server enforces.

## Summary

| # | Feature | In the product | Status | System tests |
|---|---|---|---|---|
| F1 | Run a workflow and record every step | Task Studio (New run); Pipeline trace | Implemented, tested | SYS-CORE-01, 02, 04; SYS-ERR-01, 04, 07; SYS-REL-02, 03 |
| F2 | Check the outcome and detect silent failures | Pipeline trace: Outcome, Observed vs source of truth, Checks, Findings | Implemented, tested | SYS-CORE-01, 02 |
| F3 | Trace back to where it began | Verification lab (finding page): Where did it begin? | Implemented, tested | SYS-CORE-01; SYS-SEC-03 |
| F4 | Verify a hypothesis by controlled replay | Finding page: Verify, Verification results | Implemented, tested | SYS-CORE-01, 03; SYS-ERR-05, 06 |
| F5 | Review: a person decides | Finding page: Your decision, Review history | Implemented, tested | SYS-CORE-01; SYS-ERR-03 |
| F6 | Record evidence and export a report | Finding page: Evidence, Download report | Implemented, tested | SYS-CORE-01; SYS-SEC-02 |
| F7 | Find earlier runs and findings | Investigations | Implemented, tested | SYS-CORE-05 |
| F8 | Explain itself: guide and API reference | How it works; Evidence; `/docs` | Implemented, tested | SYS-CORE-06, 07 |

Not built yet (planned for Iteration 2, not claimed): importing traces from other tools, a second workflow, a check editor, fix suggestions, PDF export, redaction of stored personal data. See the [execution status](../plan/execution-status.md).

Screenshots of the redesigned interface (2026-10-14): [command center](../../evidence/demos/2026-10-14_command-center.png), [Task Studio](../../evidence/demos/2026-10-14_task-studio-scenarios.png), [pipeline trace](../../evidence/demos/2026-10-14_pipeline-trace-silent-failure.png), [step inspector](../../evidence/demos/2026-10-14_step-inspector-order-lookup.png), [verification lab](../../evidence/demos/2026-10-14_verification-lab-accepted.png), [guide](../../evidence/demos/2026-10-14_guide-features-vr1-explorer.png), [evidence page](../../evidence/demos/2026-10-14_evidence-delivery-comparison.png), [phone width](../../evidence/demos/2026-10-14_pipeline-trace-phone-390px.png). Earlier interface (2026-10-11): [guide](../../evidence/demos/2026-10-11_guide-features-inputs-outputs.png), [investigations](../../evidence/demos/2026-10-11_investigations-list-filters.png), [run](../../evidence/demos/2026-10-11_run-detail-checks-graph.png), [finding](../../evidence/demos/2026-10-11_finding-confirmed-reviewed-evidence.png), [errored run](../../evidence/demos/2026-10-11_run-errored-unrecorded-task.png), [phone width](../../evidence/demos/2026-10-11_guide-mobile-390px.png).

---

## F1. Run a workflow and record every step

**Purpose.** Execute the Refund Desk (five agents working on real retail orders) on one customer request and keep a complete record of what each agent received and produced.

| Input | Type and rule | Refused when |
|---|---|---|
| Customer message | Text, 3 to 2000 characters | Shorter or longer: "Enter at least 3 characters" |
| Customer e-mail | `name@example.com`, at most 190 characters | Wrong shape: "Must look like name@example.com" |
| Order number | `#W` and seven digits | Wrong shape: "Must look like #W1234567" |
| Fault to inject | `none` or `stale_price` (optional) | Unknown name: 422 with the list of available faults |
| Seed | Whole number, 0 to 2,000,000, default 1 | Out of range |
| Model | `recorded`, `live` or `auto` | Unknown value |
| Anything else | Not accepted | Unknown keys are refused |

**Output.** A run (`run_…`) with status queued, running, completed or errored; the trace of every step (Granite Trace v1, published as a [JSON Schema](../../packages/granite_core/schema/granite-trace-v1.schema.json)); a SHA-256 hash of the trace; a data-flow graph.

**Edge and failure cases that work.** Invalid input is refused per field. A task with no recorded answers ends as "errored" with the reason and a "Run again" button. A model that cannot be reached ends the same way, not as a crash. Six runs started at once all finish. The same task with the same seed gives the same trace hash.

**Where.** UI `apps/web/src/pages/NewRun.tsx`, `RunDetail.tsx` · API `POST /api/runs`, `GET /api/runs/{id}`, `GET /api/runs/{id}/graph` · code `services/runs.py`, `granite_core/runner.py`, `workflows/refund_desk/` · tests `test_runner.py`, `test_store_and_steps.py`, `apps/api/tests/test_journeys.py`, `test_platform.py`.

## F2. Check the outcome and detect silent failures

**Purpose.** Decide whether the answer is right without a prepared answer key, by testing it against rules and against a source of truth the workflow does not control. Runs automatically after every run.

| Input | Where it comes from |
|---|---|
| The trace | F1 |
| Checks | Defined with the workflow: 2 outcome checks, 5 step checks. Each is an expression in a restricted language (at most 500 characters, 150 syntax nodes, depth 14; no function calls outside a fixed list) |
| Source of truth | The order and catalogue data, read independently of the workflow |

**Output.** For each check: pass, fail, abstain (the data needed was missing) or error; the observed and expected values; the computation. A failed **outcome** check opens a **finding** with a title, severity and the step where the symptom appeared (verification level V0).

**Edge and failure cases that work.** A clean run opens no finding. A fault that does not change the outcome (a cancelled order is refused either way) fails a step check but opens no finding. Hostile expressions (attribute access, imports, very deep nesting) are refused by the parser.

**Where.** UI Run page · API part of `GET /api/runs/{id}` · code `granite_core/checks.py`, `dsl.py`, `refund_desk/definition.py` · tests `test_dsl.py`, `test_trace_and_checks.py`.

## F3. Trace back to where it began

**Purpose.** Point at the step where the wrong value most likely entered, with a reason a person can check.

| Input | Where it comes from |
|---|---|
| Data flow between steps | Each step declares what it reads |
| Step-level check results | F2 |
| The symptom step | The finding |

**Output.** Up to 5 hypotheses, ranked. Each has the step, the kind of evidence (output contradicts the source of truth; step broke its own contract; consistent with its inputs), a score and a sentence of explanation. The finding moves to "hypotheses ready" (V1).

**Edge cases.** When no step has direct evidence the ranking falls back to position in the data flow and says so in the explanation. The injected fault (the ground truth) is never an input to this step; a test checks that it does not appear in the evidence. Known limitation: inside one evidence class the score order can differ from the rank ([defect D-25](../registers/defect-list.md)).

**Where.** UI Finding page · API `GET /api/findings/{id}` · code `granite_core/attribution.py`, `lineage.py`, `services/analysis.py` · tests `test_attribution.py` · design [algorithm design](../diagrams/algorithm-design.md).

## F4. Verify a hypothesis by controlled replay

**Purpose.** Turn a suspicion into a tested claim: replay the workflow from the suspect step with its output corrected, and again without the correction, and compare.

| Input | Type and rule |
|---|---|
| Hypothesis | One of the ranked steps that has a repair rule |
| Fix replays N | 1 to 10, default 5 |
| Control replays M | 0 to 5, default 2 |
| Model | `recorded`, `live` or `auto` |

**Output.** A verdict under the fixed rule VR-1 ([ADR-006](../adr/adr-006-vr1-verdict-rule.md)): **confirmed** when at least 80% of the fix replays are correct and at most 20% of the controls are; **refuted** when at most 20% of the fix replays are correct; otherwise **inconclusive**. Also the counts, a 95% Wilson interval, every replay's output, and a diff of the original and fixed answers. Confirmed moves the finding to V2.

**Edge and failure cases that work.** A step with no repair rule is refused ("no automatic replay"), not guessed. N or M out of range is refused with 422. If replays cannot run (for example recorded mode has no saved answer for a control), the result is "error, no verdict", the reason is stated, and the finding stays open for another attempt. A fix that repairs the target check but breaks another check does not count as a pass (regression guard).

**Where.** UI `components/Verify.tsx`, `Outcome.tsx` · API `POST /api/hypotheses/{id}/experiments`, `GET /api/experiments/{id}` · code `granite_core/verification.py`, `experiment.py`, `services/experiments.py` · tests `test_verification.py`, `test_experiment.py`, `test_faults_and_verification.py`.

## F5. Review: a person decides

**Purpose.** Keep a human in charge. The software produces evidence; a named reviewer closes the finding.

| Input | Type and rule |
|---|---|
| Decision | accept, reject, ask for more information, resolve, will not fix |
| Comment | At most 2000 characters. Required (at least 5 characters) to reject, to close without fixing, to ask for information, or to accept an inconclusive finding |
| Reviewer name | 1 to 80 characters, default "analyst" |

**Output.** A review record (who, what, when, comment) and a new status, but only if the lifecycle allows it from the current status. Accepting a confirmed finding gives V3. "Ask for more information" records the question and leaves the status unchanged.

**Edge cases that work.** Accepting before any verification, or rejecting an accepted finding, is refused with 409 and a plain message. The buttons shown are exactly the actions the server allows.

**Where.** UI `components/Outcome.tsx` · API `POST /api/findings/{id}/reviews` · code `granite_core/lifecycle.py`, `services/reviews.py` · tests `test_lifecycle_evidence_redaction_llm.py`, `apps/web/tests/requirements.test.tsx` · design [state machine](../diagrams/finding-state-machine.md).

## F6. Record evidence and export a report

**Purpose.** Let someone else check the conclusion. This is the answer to "how are verification results captured?".

**Input.** Nothing typed. Evidence is written at each step above.

**Output.** Evidence items of nine types (step snapshot, check computation, provenance path, replay output, diff, verdict computation, reviewer note and others), each with a SHA-256 hash of its canonical JSON that is recomputed and shown as "hash matches" on display; an audit log of every action; a report for one finding as Markdown or JSON.

**Edge cases that work.** The API has no way to change or delete evidence (the methods are refused). Records survive a restart of the server.

**Where.** UI Finding page · API `GET /api/findings/{id}/report?format=md|json`, `GET /api/evidence/{id}` · code `granite_core/evidence.py`, `services/common.py`, `services/report.py` · tests `test_lifecycle_evidence_redaction_llm.py`, `apps/api/tests/test_requirements.py`.

## F7. Find earlier runs and findings

| Input | Type and rule |
|---|---|
| Search text | At most 100 characters, matched in the finding title |
| Severity | critical, high, medium, low |
| Verification level | V0, V1, V2, V3 |
| Page size, offset (API) | 1 to 100; 0 or more |

**Output.** The matching findings, newest first, and the recent runs. An empty result says so; Clear resets the filters.

**Where.** UI `pages/Home.tsx`, `components/Filters.tsx` · API `GET /api/findings`, `GET /api/runs` · tests `test_requirements.py`, `requirements.test.tsx`.

## F8. Explain itself

**Purpose.** A new user, or an examiner, can see every feature with its inputs and outputs without reading a document.

**Output.** The **How it works** page; the generated API reference at `/docs` (OpenAPI), where every endpoint has a description; the published trace schema.

**Where.** UI `pages/Guide.tsx` · tests `test_the_in_app_guide_states_the_limits_the_server_enforces` (API suite), `requirements.test.tsx`, `a11y.test.tsx`.

---

## Words used

| Word | Meaning |
|---|---|
| Run | One execution of a workflow on one task |
| Step | One agent's turn inside a run |
| Check | A rule that a run must satisfy, written as an expression |
| Silent failure | An answer that looks complete and plausible but is wrong |
| Finding | A recorded silent failure (or a run that stopped early) under investigation |
| Hypothesis | A suspected origin step, with the reason for suspecting it |
| Replay | Re-executing the workflow from one step, keeping earlier outputs fixed |
| Control | A replay without the correction, to show the correction is what changed the result |
| Verdict | Confirmed, refuted, inconclusive or error, decided by rule VR-1 |
| Evidence | A stored, hashed record that supports a claim |
| V0 to V3 | How sure a finding is: detected, evidence, replay-verified, human-confirmed |

Every stored field and every enumeration is defined in the [data dictionary](../diagrams/data-dictionary.md).
