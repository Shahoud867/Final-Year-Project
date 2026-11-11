# FYP-1 completion plan: from demonstration to product

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-11-11 |
| Status | Proposal from an AI-assisted assessment (see the [AI usage log](../registers/ai-usage-log.md)). **Not yet agreed by the team or the supervisor.** It refines [master plan section 31](master-plan.md); where the two disagree, this plan applies once the committed scope (section 6) is agreed with the supervisor and recorded as change C-05 |
| Basis | The repository at `main` `00e0c40` (14 October), the registers, the feasibility results, the datasets in `data/raw/`, and the final [handbook](../../references/university/bs-fyp-handbook-2026.pdf) (Appendix A stage 2; Forms 4 and 5) |
| Fixed dates | **Poster submission: 15 November 2026.** FYP-1 Final: **not confirmed**; by the handbook calendar (proposal defense on 11 September = week 4) week 15 falls around 27 November to 3 December |

## What FYP-1 Final is marked on

The panel marks the demo and defense (42.5 marks) on Form 4; the report (7.5 marks) is marked on Form 5. The largest items: **implementation progress, at least 60% of committed scope (25)**, quality and robustness of the live demo beyond the happy path (15), poster (10), previous actions addressed (10), testing (10), design evolution (10), code quality and integration readiness (10). Caps: undisclosed core GenAI use sets the tool-use item to 0; a member who cannot explain their module gets an individual adjustment; commit counts alone earn nothing.

Because the 25-mark item is measured against **committed** scope, the scope in section 6 must be agreed with the supervisor now.

## 1. Honest assessment

**Strong:** clean architecture (framework-free core, thin API, typed trace format); a real evidence chain (SHA-256 re-checked on display, append-only API, server-enforced lifecycle); the pre-registered rule VR-1; about 400 tests; CI/CD and a live Render deployment; honest registers; an interface that shows only real backend output.

**Weak:**

1. **Progress has stopped.** No commit on `main` since 14 October. Of the master plan's FYP-1 Final Must list, F10 to F13, F15 to F18 and F20 are not started. One workflow; one fault type (`FAULT_TYPES` holds only `stale_price`).
2. **The research result is circular.** We wrote the workflow, the fault, the step check that catches that fault, and the repair rule that undoes it. The [feasibility notes](../../research/eval/results/2026-10-07_refund-desk-feasibility-notes.md) say attribution is "easy by construction". Verification puts the source-of-truth value back and confirms that this fixes the output, which is close to a tautology.
3. **A trivial baseline ties us.** "Blame the earliest step whose check fails" gives Granite's answer on every Refund Desk task. On this benchmark the provenance ranking adds nothing measurable.
4. **"Robust to nondeterminism" is a claim, not a result.** Recorded mode is deterministic; controls were always 0/2; no experiment compares single-replay verification with VR-1.
5. **No baselines, 10 tasks, one 3B model;** four tasks not blind.
6. **Not usable as a product.** No import, SDK or adapter, so no one can bring their own agent system. Checks are Python inside the workflow definition; repair rules are hand-written per step.
7. **The demo is narrow.** The public instance runs only the 12 recorded tasks and its database resets on every deploy.
8. **Ownership.** Recent commits come from one account. The handbook adjusts individual marks when a member cannot explain the work.

**Readiness:** a well-built Iteration 1 with a thin Iteration 2. As it stands it would score well on design and testing and poorly on implementation progress and on whether the research adds anything.

## 2. The product

**Users:** developers and QA staff running LLM agent workflows that act on real data (support agents, back-office automation, tool-using assistants), whose failures are silent: the run succeeds and the answer is wrong.

**One sentence:** connect your agent workflow, declare what "correct" means, and Granite flags the runs that are wrong, finds the step where it went wrong, proves it with controlled replays, and turns it into a regression test.

**Minimum for a real product:** it works on a system whose failures we did not author; it works on traces from outside; it needs no hand-written repair rule per step; it gives the user something to keep (a regression case).

## 3. Competitors and the gap

From the [market comparison](../../research/market/commercial-product-comparison.md) and master plan section 10. Re-check vendor documentation before the panel; the comparison is dated 22 August 2026.

| Who | What they do | What their documentation does not show |
|---|---|---|
| LangSmith, Langfuse, Arize Phoenix, Braintrust | Trace capture, graphs, evaluations | Diagnosis by a person; no fix-testing by replay |
| LangSmith Engine (beta), Arize Alyx | Automated root cause and drafted fixes | Mechanism unpublished; tied to their platform; no controls |
| Raindrop, Percival, Galileo | Silent-failure detection judged by an LLM | No step-level causal attribution; SaaS only |
| Who&When, AgenTracer, ErrorProbe | Attribution research | LLM-judged; assume detectable anomalies; no verification |
| **DoVer** (closest prior work) | Intervene at the suspect step and re-execute | Single replay, flip rates; no controls or verdict rule; no executable checks |

**The gap to own:** *verified* attribution for silent failures: detection by executable checks against an independent oracle, verification that holds under nondeterminism (N fix replays against M controls), and one auditable record that ends in a regression test. It counts only if measured against the cheap alternatives. No superiority claim over any product or paper.

## 4. Novelty strategy: break the circularity

1. **Check-derived interventions.** When a source-of-truth check fails, its computation already holds the correct value: patch the step from it and remove the hand-written per-step repair rules. Answers "you wrote the fix yourselves".
2. **Verified attribution loop.** Rank suspects, verify them in order until one is confirmed, within a replay budget. Claim to test: verification raises top-1 accuracy over ranking alone when check coverage is incomplete.
3. **Check-coverage ablation (main experiment).** Remove step checks, including the origin's own, at 100%, 60% and 30% coverage. Compare: earliest failing check, last agent, an all-at-once LLM judge (as in Who&When), Granite's ranking alone, and Granite with verification. At full coverage the trivial baseline ties; the result that matters is below it.
4. **Nondeterminism ablation.** Live mode, temperature above 0: single-replay verification (DoVer style) against VR-1 (N=5, M=2). Metric: false confirmations on innocent steps.
5. **A system whose failures are natural.** `data/raw/taubench_retail/` holds the full tau-bench retail environment: 16 tools, the policy and 635 tasks with gold action sequences (Refund Desk data is already a subset). A **Retail Agent** (an LLM agent calling those tools) is judged against tau-bench's own gold end state of the database, an oracle we did not write. Small models fail on it without injected faults.

**External validity:** the 184 annotated Who&When traces are on disk (`data/raw/whowhen_full/`). Import them and run the baselines. Granite's deterministic ranking will likely be weak there (chat logs, no data flow, no checks); report that as the boundary of the method and the FYP-2 extension point (LLM opinion, F19).

## 5. Target architecture

Keep the modular monolith ([ADR-001](../adr/adr-001-modular-monolith.md)); add components, rewrite nothing.

```
Agent systems ──┐  Refund Desk (own runner)       Retail Agent (tau-bench tools, own runner)
                ├─ Trace import  POST /api/traces  (Granite Trace v1; Who&When converter)
                └─ SDK / LangGraph adapter (FYP-2: replay by forking a checkpoint)
                        │
granite_core:  checks ─ attribution ─ interventions (check-derived + rule) ─ verification (VR-1)
               lifecycle ─ evidence ─ NEW: investigation orchestrator (verify top-k within a budget)
                        │
apps/api:      runs · findings · experiments · NEW: imports, fault-lab batches, evaluations, auto-investigate
               jobs (thread pool) · Postgres on Neon (free) · SQLite locally
apps/web:      existing 6 screens + NEW: Import, Fault Lab / Benchmark, Evaluation, "Investigate" button
LLM:           Ollama locally (qwen2.5:7b if hardware allows) · OpenAI-compatible endpoint · recorded cassettes
research/eval: pre-registration v2 · harness (CLI = same code as the API) · results JSON -> Evaluation screen
```

## 6. Committed scope for FYP-1 Final (to agree with the supervisor)

| # | Feature | Priority | Backend | Frontend | Done when |
|---|---|---|---|---|---|
| 1 | Check-derived interventions | **Critical** | `build_intervention` falls back to the failed truth check's expected value; drop `s2` from `REPAIRS` | "Patched from check X" on the experiment | Refund Desk verifies Order Lookup with no repair rule; unit tests |
| 2 | Fault types 2 and 3 (handoff drift, dropped field) and Fault Lab batch | **Critical** | `faults.py`; batch job and endpoint | Fault Lab screen with progress | 3 faults × 12 tasks plus clean controls generated from the UI |
| 3 | Auto-investigate (verified attribution) | **Critical** | Orchestrator job: verify ranked suspects until confirmed or out of budget | "Investigate" button and sequential timeline | Finding reaches V2 in one click; budget respected; tests |
| 4 | Evaluation harness v0 with baselines and both ablations | **Critical** | `research/eval/` harness and `/api/evaluations` | Evaluation screen: metrics, Wilson intervals, baseline table | Pre-registered run reproduces from one command |
| 5 | Retail Agent (natural failures, gold oracle) | **High**, critical if the spike succeeds | New workflow: single-turn tool loop; generic checks (arguments exist in the database, policy rules, end-state diff) | Existing screens (the registry plugs it in) | 30 or more tau-bench tasks run live; failure rate and findings reported |
| 6 | Trace import and Who&When converter (F10) | **High** | `POST /api/traces`, schema validation, V1 evidence with replay marked unavailable | Import screen with validation report | 58 hand-crafted Who&When traces imported; attribution runs |
| 7 | Regression export (F17) | **High** | Confirmed finding → JSON case and a pytest file that replays it | "Export regression test" | Test fails on the faulty trace and passes on the fixed one |
| 8 | Durable deployment | **High** | Neon Postgres; the PostgreSQL test (D-08); live-model demo path | Instance panel shows the database | Data survives a redeploy; system tests pass on Postgres |
| 9 | Redaction before storage (D-07) | Optional | Token vault as designed in D-07 | Redaction marks in the inspector | FR-SEC-01 tests pass |
| 10 | SDK and LangGraph adapter with checkpoint-fork replay | FYP-2 | | | |
| 11 | Check suggestion validated on clean runs | FYP-2 | | | |
| 12 | LLM second opinion (F19), PDF export, CrewAI, OAuth | FYP-2 | | | |

**Changes against the master plan, for C-05:** F11 Math Crew is replaced by the Retail Agent (more realistic, reuses our data). F13 SDK and LangGraph adapter, F15 fix suggestion, F16 recovered run, F18 redaction and PDF export move to FYP-2 or become optional. Rows 1 to 8 are the committed FYP-1 Final scope.

## 7. User journey of the finished product

1. Connect the system: pick the Retail Agent, or import traces from another tool.
2. Run the panel's chosen task live, or a Fault Lab batch.
3. Checks flag a run that completed but is wrong.
4. **Investigate:** suspects ranked, the top ones replayed with controls, origin confirmed with an interval.
5. A reviewer accepts; the evidence is hashed.
6. Export a regression test that runs in CI.
7. The Evaluation screen shows how reliable this is in general: accuracy and false alarms against the baselines.

## 8. Roadmap

Owners follow master plan section 34.1. Every member opens their own pull requests throughout.

| Window | Shahoud (workflows and experience) | Noor (investigation engine) | Saif (verification and platform) | Gate |
|---|---|---|---|---|
| **12 to 15 Nov** | **Poster** (lead; supervisor approval before 15 Nov) | Pre-registration v2 written and committed before any run; start check-derived interventions (#1) | Fault types 2 and 3 (#2) | **Poster submitted 15 Nov** |
| **16 to 22 Nov** | Retail Agent spike on 5 tasks, then generic checks and the gold end-state oracle; record cassettes overnight | #1 merged; harness with baselines and the coverage ablation (#4); Who&When converter (#6) | Fault Lab batch (#2); Neon and the Postgres test (#8); start auto-investigate (#3) | #1, #2 merged; benchmark generation running overnight (120 or more runs, live model) |
| **23 Nov to the Final** | Fault Lab, Import and Evaluation screens; usability pilot with 3 peers; demo rehearsal | Run the evaluation; results and limitations into the report | #3 merged; regression export (#7); nondeterminism ablation; browser E2E test in CI; tag `v0.2.0` | Report v2.0 approved by the supervisor; code freeze 24 hours before the Final |

**Poster (due 15 Nov).** Portrait, 22.5" × 34.5", little text; submit the Photoshop or Corel source with a JPEG; supervisor approval first. Top left: title, members, supervisor. Top right: goals. Middle: the silent-failure contrast and the verification visual from the current interface (real screenshots). Bottom: the plan and the tentative FYP-1 Final deliverables (rows 1 to 8), labelled as planned, as the handbook's poster guidelines suggest.

## 9. Testing and evaluation

- **Functional:** current suites stay green; unit, API and system tests for every new feature; the scripted browser walk becomes a CI end-to-end test.
- **Performance:** time per run, per replay and per investigation; replay budget per investigation.
- **Research, pre-registered in `research/eval/prereg-v2.md` before any result exists:**

| Metric | Measures |
|---|---|
| Detection | Share of faulty runs caught |
| False alarms | Findings on clean runs |
| Top-1 attribution | At 100%, 60% and 30% check coverage |
| Verified top-1 | Accuracy after auto-investigate |
| False confirmations | Single replay against VR-1 on innocent steps |
| Retail Agent | Natural failure rate and investigation outcomes |
| Who&When | Agent- and step-level accuracy against the published baselines |

- **Baselines:** earliest failing check, last agent, an all-at-once LLM judge, single-replay verification.
- **Reporting:** Wilson intervals throughout; natural failures labelled blind by two members, with agreement (κ); negative results reported.

## 10. Final demonstration (15 minutes, live)

1. The panel chooses a tau-bench task; the Retail Agent runs it live on a local model and succeeds or fails naturally.
2. On a failure: **Investigate**, the ranking, sequential replays with controls, the confirmed origin; accept; export the regression test and run it in a terminal.
3. Edge cases: an imported Who&When trace reaches V1 with replay honestly unavailable; a clean run raises no false alarm; a model outage is handled; a review out of lifecycle order is refused (409).
4. Evaluation screen: real benchmark numbers against the baselines, including where Granite ties or loses.
5. Code walkthrough: each member explains the module they own.

Fallback: recorded mode and the deployed instance (warm it a minute before; the free tier sleeps).

## 11. Risks

| Risk | Mitigation |
|---|---|
| Time | Rows 1 to 4 are the critical path; the Retail Agent drops to 10 tasks or moves to FYP-2 Mid; scope agreed formally (C-05) |
| Local LLM speed (5 to 35 s per call) | Benchmark generation overnight on two laptops; small N; a free OpenAI-compatible endpoint is acceptable because the data is synthetic (disclose it in Form 13) |
| Retail Agent complexity | Single-turn instruction with a tool loop, no simulated user; generic checks only |
| Negative results | Fine when pre-registered and reported honestly |
| One person does the work | One track per member; pull requests from own accounts; the supervisor's weekly tracking form |
| Free-tier hosting resets | Neon Postgres; limits recorded in the deployment record |

## 12. First actions

1. Confirm the FYP-1 Final date and agree the committed scope (section 6) with the supervisor; record it as C-05 in the [change log](../registers/change-log.md).
2. Poster (Shahoud), approved by the supervisor before 15 November.
3. `research/eval/prereg-v2.md` (Noor), committed before any benchmark data is generated.
4. Check-derived interventions (Noor or Saif): small, unblocks auto-investigate, removes the circularity critique.
5. Fault types 2 and 3 and the batch job (Saif), so benchmark generation can start overnight.
6. Retail Agent spike on 5 tau-bench tasks (Shahoud), to measure the natural failure rate before committing to it.
7. One issue per row of section 6, with its owner.
