# FYP-1 completion plan

| | |
|---|---|
| Version | 1.1 (v1.0 of 2026-11-11 is in the git history) |
| Date | 2026-11-14 |
| Status | Proposal from an AI-assisted assessment (see the [AI usage log](../registers/ai-usage-log.md)). **Not yet agreed by the team or the supervisor.** It applies once the supervisor approves change C-05 in the [change log](../registers/change-log.md); until then master plan section 31 stands |
| Job of this document | What to do between today and the FYP-1 Final, by whom and by when. Why the product is shaped this way is in [`product-strategy.md`](product-strategy.md) |
| What changed in 1.1 | Committed scope cut from eight items to five; day-level schedule; CI repair added as the first task; the market and architecture sections moved to the strategy document |
| Fixed dates | **Poster submission: 15 November 2026.** FYP-1 Final: **not confirmed**; the handbook calendar puts week 15 around 27 November to 3 December |
| Progress | Section 0 (updated 2026-11-15) |

## 0. Implementation checklist (2026-11-15)

All feature work below was written in one AI-assisted session on branch `feat/fyp1-final-scope` at Shahoud's request, **before the supervisor approved C-05** and **not committed**. The handbook (C.5.3) asks for approval before a scope change is acted on: merge only after C-05 is signed. Section 4 assigned these items to Noor and Saif; each owner must now read, change if needed, and be able to explain their item (walkthrough).

| Item | State | Evidence |
|---|---|---|
| CI green (web dependency audit) | **Done** on the branch: `npm audit fix`; no high advisory left | `npm audit --audit-level=high` exits 0 |
| 10. Check-derived interventions | **Done.** No repair rules remain in Refund Desk; CT-LOOKUP and CT-INTAKE at version 2; [ADR-011](../adr/adr-011-check-derived-interventions.md) | `granite_core/interventions.py`; 7 unit tests; SYS-CORE-08 |
| 11. Fault types 2 and 3, batch | **Done.** `dropped_item` (s1), `handoff_drift` (s4, in transit); outcome check CHK-OUT-3; Fault Lab API and screen | `refund_desk/faults.py`; `services/batches.py`; `pages/Lab.tsx`; SYS-CORE-09 |
| 12. Investigate | **Done.** Verifies suspects in rank order within a replay budget; each attempt is a stored experiment | `granite_core/investigation.py`; `services/investigations.py`; Investigate in `Verify.tsx`; SYS-CORE-08 |
| 13. Evaluation harness v0 | **Done and run.** Pre-registered (`research/eval/prereg-v2.md`, hashed, not yet committed); 40 live runs; baselines; both ablations; Evaluation screen | [results](../../research/eval/results/2026-11-15_benchmark-v0.md), [notes](../../research/eval/results/2026-11-15_benchmark-v0-notes.md) |
| 14. Regression export | **Done.** Zip with case JSON, pytest file, README | `granite_core/regression.py`; `test_regression_export.py`; SYS-CORE-08 |
| Pre-registration v2 | Written and hashed before the run; **commit it** | `research/eval/prereg-v2.md` |
| Design pack, test catalogue, traceability regenerated | **Done.** The interactive pack now goes to the stage-2 draft; the stage-1 copy stays frozen | `--check` scripts pass |
| Tests | **559 passing:** core 221, connectors 20, Refund Desk 61, API 93, system 24, web 140, plus a Playwright browser journey at desktop and phone width. Coverage core 93%, connectors 93%, API 96%. ruff, mypy strict, bandit, ESLint, tsc clean | commands in the [execution status](execution-status.md) |
| Interface redesign (frontend roadmap P0 and P1) | **Done** on the branch; no person has used it yet | [roadmap section 10.1](../../apps/web/FRONTEND_DESIGN_ROADMAP.md) |
| Browser check | Done by the assistant in headless Chrome, recorded mode; no person yet | `evidence/demos/2026-11-15_*.png` |
| Supervisor meeting, C-05 signed, minutes | **Not done** | |
| GitHub issues per item | **Not done** | |
| Retail Agent spike | **Not done** (FYP-2 go/no-go) | |
| Code walkthrough by each member | **Not done** | |
| Usability check with three people (A1) | **Not done** | |
| Report v2.0 | **Not done** | |
| Commit, pull requests from members' own accounts, tag `v0.2.0`, deploy | **Not done**; the deployed demo still runs the October version | |
| Stretch (C-07): Phoenix and Langfuse round trip | **Done** for Phoenix, verified live against a local Phoenix 21.0.0 server; Langfuse built and tested against an in-memory server only (no instance or keys available). Connections screen, send run, import, write verdict back. [ADR-012](../adr/adr-012-observability-connectors.md), FR-INT-01 to 06 | `packages/granite_connectors/`; `services/connections.py`; `pages/Connections.tsx`; `scripts/check_connectors_live.py`; [live report](../../evidence/demos/2026-11-15_phoenix-live-check.json) |
| Stretch: hosted Postgres | Not started (FYP-2 first milestone) | |

## 1. What the Final is marked on

From the handbook, Forms 4 and 5.

| Form 4 item (demo and defence, 42.5 marks) | Max | What decides it here |
|---|---|---|
| Implementation progress against approved scope | 25 | At least 60% of committed work, "unless scope formally revised". Section 3 is that revision |
| Quality and robustness of the live demo | 15 | Works beyond the happy path; not hardcoded |
| Poster | 10 | Format and content |
| Previous actions addressed | 10 | Form 10: A1 and A6 are still "Partly" |
| Testing on completed modules | 10 | Tests run and explained by their owner |
| Design evolution and updated artefacts | 10 | Diagrams regenerated after the new modules land |
| Code quality and integration readiness | 10 | Buildable without the original developer; green CI |
| Tool and GenAI ownership defence | 5 | Each member explains what was generated and how it was checked |
| Presentation and questions | 5 | Balanced participation |

Form 5 (report, 7.5 marks) asks that the report match the demonstrated system and contain the FYP-2 evaluation plan. Caps apply: undisclosed core GenAI use sets the tool item to zero, and a member who cannot explain their module gets an individual adjustment.

## 2. The four things that would cost the most marks today

1. **No agreed scope.** The 25-mark item is measured against committed scope, and the change log records no approved change, not even C-01. Against the master plan's Final-1 Must list the project is below 60%.
2. **A red build.** CI on `main` has failed since 11 November on the web dependency audit. A panel member who opens the Actions tab sees failures.
3. **Ownership.** No member has done the code walkthrough, and Saif has eight commits. The handbook says the panel may ask any member to show any part of the code.
4. **A result that proves little.** One fault that we wrote, caught by a check that we wrote. See the [strategy](product-strategy.md), section 6.

## 3. Scope proposed for change C-05

The whole-project scope, restated as 21 capabilities so the 60% rule can be counted. The count is this plan's proposal; the supervisor decides.

| # | Capability | State | Target |
|---|---|---|---|
| 1 to 9 | Run a workflow (F1), trace store and inspector (F2), checks and findings (F3), attribution (F4), verification by controlled replay (F5), review and lifecycle (F6), history (F7), report export in Markdown and JSON (F8), graceful errors (F9) | **Built** | Keep green |
| 10 | Corrections derived from the failed check | Not built | **FYP-1 Final** |
| 11 | Three fault types and batch generation (F12) | One type | **FYP-1 Final** |
| 12 | Verified attribution in one action ("Investigate") | Not built | **FYP-1 Final** |
| 13 | Evaluation harness with baselines and the two ablations (F20 v0) | Not built | **FYP-1 Final** |
| 14 | Regression-test export (F17) | Not built | **FYP-1 Final** |
| 15 | Trace import and Who&When converter (F10) | Not built | FYP-2, first milestone. Stretch for the Final |
| 16 | A system with natural failures: Retail Agent on tau-bench (replaces F11 Math Crew) | Not built | FYP-2. A five-task spike before the Final decides feasibility |
| 17 | LangGraph adapter with checkpoint-fork replay (F13) | Not built | FYP-2 |
| 18 | Redaction before storage (F18, defect D-07) | Not built | FYP-2, first milestone |
| 19 | Durable hosted database with migrations (D-08) | Not built | FYP-2, first milestone |
| 20 | Reviewer login and API keys (F22) | Not built | FYP-2 |
| 21 | LLM second opinion and the Who&When boundary study (F19) | Not built | FYP-2 |

Nine of 21 are built (43%). With items 10 to 14 the count is 14 of 21 (67%).

**Removed, to be recorded in C-05 with reasons:** the CrewAI adapter (F14), the known-fix library (F21), the fix-suggestion agent as an LLM component (F15, replaced by item 10), PDF export, webhooks (F24) and the seven-framework compatibility layer (F25).

**The registered title.** "Verified Repair and Recovery" is met in this sense and no further: Granite derives a corrected value for the suspect step (item 10), verifies by replay that it fixes the outcome (F5), and shows the corrected run that the replay produced. A person decides whether to apply it. Nothing repairs itself. Say this in the report and in C-05 so the panel does not find it for themselves.

## 4. The five committed items

| # | Item | Owner | Backend | Interface | Done when | Days |
|---|---|---|---|---|---|---|
| 10 | Check-derived interventions | Noor | `build_intervention` takes the expected value from the failed source-of-truth check; remove `s2` from `REPAIRS` | "Patched from check CT-LOOKUP" on the experiment | Refund Desk verifies Order Lookup with no repair rule; unit tests; ADR-006 updated | 1.5 |
| 11 | Fault types 2 and 3 (handoff drift, dropped field) and batch runs | Saif | `faults.py`; a batch job and endpoint; ground truth stored apart from the trace | Fault Lab: choose faults and tasks, watch progress | 3 faults × 12 tasks plus clean controls generated in one action | 3.5 |
| 12 | Investigate | Saif | Orchestrator job: verify ranked suspects in order until one is confirmed or the replay budget is spent | One button; a timeline of the suspects tried | A finding reaches V2 in one action; the budget is respected; tests | 3 |
| 13 | Evaluation harness v0 | Noor | `research/eval/` harness calling the core; baselines; coverage and nondeterminism ablations; results as JSON | Evaluation screen: one table with intervals, including ties and losses | A pre-registered run reproduces from one command | 4 |
| 14 | Regression export | Shahoud | Confirmed finding to a JSON case and a pytest file that replays it | "Export regression test" | The test fails on the faulty trace and passes on the corrected one | 2 |

**If time runs out, cut in this order:** the Evaluation screen (keep the command and put the table in the report), the Fault Lab screen (keep the endpoint and a command), then item 14. Items 10, 11 without its screen, 12 and 13 are the minimum that removes the circularity objection.

**Stretch, only after the five are merged, the walkthrough is done and report v2.0 is drafted:** one real Langfuse round trip (Refund Desk runs sent to a free Langfuse Cloud project, read back by Granite, verdict written back as Langfuse scores; about 5.5 days; [integrations strategy](integrations-strategy.md), section 5.1, needs change C-07). It replaces the earlier stretch item, a plain JSON trace import. Hosted Postgres on Neon (item 19) stays a stretch item.

## 5. Work that is not a feature and is still required

| Task | Owner | Evidence |
|---|---|---|
| Make CI green: `cd apps/web && npm audit fix`, run the web tests and build, open a pull request | Saif | Green run on `main` |
| Meet the supervisor: confirm the Final date, approve C-05, sign the poster; write the minutes | Shahoud | `docs/meetings/2026-11-NN_supervisor-meeting.md`; C-05 marked approved |
| One GitHub issue per item in sections 4 and 5, assigned | Shahoud | Issue list |
| Pre-registration v2, committed before any benchmark run | Noor | `research/eval/prereg-v2.md` and its hash |
| Retail Agent spike on five tau-bench tasks, two days at most | Shahoud | A spike note with the natural failure rate and a go or no-go for FYP-2 |
| Code walkthrough: each member explains their module to the other two, then fills in "evidence of understanding" in the ADRs they own | All | [Walkthrough](../manuals/code-walkthrough.md) section 6 completed |
| Usability check with three people outside the team (closes panel action A1) | Noor | `evidence/uat/` record |
| Report v2.0 in the prescribed template, each member writing their own chapters | All; Shahoud edits | `deliverables/stage-2-fyp1-final/granite_report_fyp1-final_v2.0.pdf` |
| Regenerate the design pack, traceability and index after the last merge | Saif | The `--check` scripts pass in CI |
| Form 13 and the AI usage log brought up to date | Saif collates | [Form 13](../registers/form-13-genai-disclosure.md) |
| Poster: one JPEG and one original design file in `deliverables/stage-2-fyp1-final/`; close pull request #12 without merging its six versions | Shahoud | Two files in the stage folder |

## 6. Schedule

Dates assume the Final falls between 27 November and 3 December. If it is earlier, apply the cut order in section 4.

| Dates | Shahoud | Noor | Saif | Gate |
|---|---|---|---|---|
| **Sat 14 to Sun 15 Nov** | Poster approved and submitted; request the supervisor meeting; open the issues | Pre-registration v2 drafted | CI green | **Poster submitted; CI green** |
| **Mon 16 to Thu 19 Nov** | Retail Agent spike (two days), then start item 14 | Pre-registration committed (Mon); item 10 merged (Wed); start the harness | Fault types 2 and 3 merged (Wed); batch endpoint | **C-05 approved; items 10 and 11 (faults) merged** |
| **Fri 20 to Tue 24 Nov** | Item 14 merged; Fault Lab screen | Harness with baselines and the coverage ablation; benchmark generation overnight on two laptops | Item 12 merged; "Investigate" in the interface | **Benchmark generated; items 12 and 14 merged** |
| **Wed 25 to Fri 27 Nov** | Report chapters; demo script; Evaluation screen | Run the evaluation; nondeterminism ablation; results and limitations chapter | Design pack regenerated; browser end-to-end test; tag `v0.2.0` | **Evaluation results exist; walkthrough done; report draft to the supervisor** |
| **Sat 28 Nov to the Final** | Rehearsal; stretch items | Usability check; rehearsal | Code freeze 24 hours before; warm the hosted instance | **Report v2.0 approved** |

Estimated effort is 14 person-days of features and about 9 of report and evidence, against roughly 18 available if each member gives half of each day. It fits only with the cut order ready and no further time spent on the poster or the interface.

## 7. Evaluation to run before the Final

Pre-registered in `research/eval/prereg-v2.md` before any result exists. Design and reasons: [strategy](product-strategy.md), section 6.

| Metric | Measures |
|---|---|
| Detection and false alarms | Faulty runs caught; findings on clean runs, across three fault types |
| Top-1 attribution at 100%, 60% and 30% check coverage | Granite's ranking against the earliest failing check, the last agent and an all-at-once LLM judge |
| Verified top-1 | Accuracy after "Investigate", and replays spent per confirmed origin |
| False confirmations | Single replay against VR-1 on innocent steps, live model, temperature above 0 |

Wilson intervals throughout. Report ties and losses.

## 8. Demonstration (15 minutes, live)

1. A faulty run completes with no error. The checks open a finding.
2. **Investigate:** the ranking, the replays with controls, the confirmed origin patched from the check; a reviewer accepts.
3. Export the regression test and run it in a terminal: it fails on the faulty trace and passes on the corrected one.
4. Beyond the happy path: a clean run raises no finding; an innocent suspect is refuted; the model is unavailable and the run fails cleanly; a review out of order is refused.
5. Evaluation: the real table against the baselines, including where Granite ties.
6. Each member explains the module they own.

Fallback: recorded mode on a laptop. The hosted instance sleeps; wake it a minute before.

## 9. Risks

| Risk | Response |
|---|---|
| The Final is earlier than assumed | Confirm the date on Monday; the cut order in section 4 |
| The supervisor does not approve C-05 | The master plan's list stands and the 60% count fails; raise it at the first meeting and bring section 3 on one page |
| A member does not deliver | One track per member; raise a stall of more than three days with the supervisor, as the master plan (34.1) already says |
| Local model too slow for the benchmark | Generate overnight on two laptops; a free hosted endpoint for synthetic data, disclosed in Form 13 |
| The evaluation shows no advantage over the trivial baseline | Report it. A pre-registered negative result with the coverage ablation is a defensible FYP-1 finding and sets up FYP-2 |
| Members cannot explain AI-generated code | The walkthrough is scheduled, not optional; new code in this plan is written by its owner |
