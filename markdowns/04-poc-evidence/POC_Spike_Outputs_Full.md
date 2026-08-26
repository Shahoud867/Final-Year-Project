# Granite — Full POC Spike Outputs, With Reasoning

*All 8 spikes, real output pulled directly from the JSON files on disk (`dev/spikes/poc/`), not summarized from memory. For sharing with teammates who need to understand what was actually run and why the result means what it means.*

---

## Spike 1 — ErrorProbe Reproduction

**What it tests:** can our diagnosis engine's core algorithm, a simplified reproduction of ErrorProbe's method, identify the responsible agent and step on real Who&When cases?

**Setup:** 2-stage pipeline (Strategist → Arbiter only — no tool-grounded Investigator, no Verified Episodic Memory), backbone = local `llama3.2:3b` via Ollama (free), n=8 real Who&When-Hand-Crafted cases.

**Bug found and fixed, 2026-08-26:** an earlier version of this write-up flagged case 6 as a likely scorer type-mismatch (predicted step matched ground truth exactly, yet `step_accuracy` read 0.0) — that flag was correct. The scoring script compared `gt_step` (a string in the Who&When data, e.g. `"5"`) against `pred_step` (an int from the LLM's JSON, e.g. `5`) with `==`, which silently returns `False` for numerically-identical values. Fixed in `poc_spike1_errorprobe_repro.py` with a robust `as_int()` coercion — a genuine mismatch still scores as wrong, only the false negatives from type mismatch are fixed.

**Real re-run, 5 independent samples, 2026-08-26 (not a rescore — 5 fresh runs against local Ollama, ~45–50 min each):**

| Run | n scored | Agent accuracy | Step accuracy |
|---|---|---|---|
| 1 | 8/8 | 50.0% | 0.0% |
| 2 | 8/8 | 62.5% | 25.0% |
| 3 | 7/8 (1 parse failure) | 71.4% | 14.3% |
| 4 | 8/8 | 50.0% | 12.5% |
| 5 | 7/8 (1 parse failure) | 71.4% | 14.3% |
| **Mean** | — | **61.1%** | **13.2%** |
| **Range** | — | **50.0–71.4%** | **0.0–25.0%** |

Full data: `poc_spike1_run{1..5}_output.json` + aggregated `poc_spike1_multirun_summary.json`.

**Per-case consistency across the 5 runs — a real, stable pattern, not noise:**

| Case | Question (shortened) | Agent correct (of 5 runs) | Step correct (of 5 runs) |
|---|---|---|---|
| 1 | Martial arts classes near NYSE | 5/5 | 0/5 |
| 2 | Worst-rated Ted Danson series | 0/5 | 0/5 |
| 3 | Chicago landmark architect firm | 4/5 | 0/5 |
| 4 | Wheelchair-accessible Yosemite trails | 4/5 | 0/5 |
| 5 | MJ fifth single, last word before chorus | 1/5 | 3/5 |
| 6 | Mission Bay high-rise sale price | 0/4 scored | 2/4 scored |
| 7 | Bird species in YouTube video | 5/5 | 0/5 |
| 8 | monday.com C-suite at IPO | 4/4 scored | 0/4 scored |

**Reasoning:** across 5 independent samples, the model reliably identifies *who* (cases 1, 3, 4, 7 hit agent-correct in 4–5 of 5 runs) but essentially never pins down *exactly which step* — those same four cases score 0/5 on step accuracy every time, not sometimes. That is a stable, real pattern, not sampling noise: the model consistently predicts steps much later than the true origin (case 8 alone: predicted steps 95–109 across runs vs. true step 8). This matches the field-wide pattern every paper in this space reports — agent-level attribution is the easier half, step-level is where everything breaks down. Case 6 is the one interesting exception: agent accuracy is *low* there (0/4) because the model consistently answers "Orchestrator (thought)" rather than the ground truth's plain "Orchestrator" — an exact-string-match artifact of the trajectory format's role labels, worth a team decision on whether to normalize before Mid-1, not silently patched here. Case 2 is the cleanest failure: 0/5 on both agent and step, every run — a genuinely hard case for this simplified pipeline, not a fluke.

A mean of 13.2% step accuracy on a 2-stage simplified pipeline, free local 3B model, is a genuinely encouraging floor — it means the *approach* produces signal, not that it's close to ErrorProbe's reported 59.5%. The full 3-stage pipeline (tool-grounded Investigator + memory) on a stronger backbone is what's needed to approach that number, and the acceptance band in plan §11 (±10 points, comparable-class backbone) is judged against that full run, not this simplified spike.

---

## Spike 2 — CrewAI Instrumentation

**What it tests:** does trace capture map cleanly onto our execution-graph data model for a framework (CrewAI) none of the 7 original papers ever used?

**Setup:** toy 3-agent workflow — Planner → Researcher → Writer, task: "What is the capital of France, and roughly what is its population?"

**Output (real trace):**
- `n1_plan` (Planner): produces 2 sub-steps
- `n2_research` (Researcher): answers Paris + ~67.2 million population
- `n3_write` (Writer): combines into final answer

**Execution graph produced:** 3 nodes, 2 edges (`n1→n2`, `n2→n3`), correctly ordered by `depends_on`.

**Reasoning:** the graph structure came out exactly as expected — linear, correctly dependency-ordered, no missing or extra nodes. This confirms the execution-graph data model can represent a real CrewAI run without modification. Resolved — no further testing needed on this specific question (though real per-step timing hooks are still owed; the current timestamps were captured post-hoc, not from real hooks).

---

## Spike 3 — Fault Injection (two attempts, both kept as findings)

**What it tests:** if we inject a known fault at a known node, is the ground truth recoverable and unambiguous?

### Attempt 1 — famous-fact corruption (self-corrected, a real finding)
Injected: swapped "Paris" → "Berlin" as the capital of France at `n2_research`.
**What happened:** the Writer agent (`n3_write`) caught it — final output reads *"I can't fulfill your request. Berlin is not the capital of France. The capital of France is actually Paris..."*
**Reasoning:** this is a genuine, useful negative result — a well-known fact is exactly the kind of corruption a capable downstream agent can self-correct, which means the substring-matching propagation check used in this attempt was too crude (it doesn't know the fault got fixed downstream). This is real evidence the benchmark needs both self-correcting and blind-propagating fault cases represented, not just one type.

### Attempt 2 — unverifiable fabricated fact (clean propagation)
Task: "tell the user what time Riverside Hardware closes today and how far it is from downtown."
Injected: true value "closes 9:40 PM" corrupted to "closes 6:15 PM" at the `StoreChecker` tool-call node.
**What happened:** propagated blindly all the way to the final answer — *"Riverside Hardware's closing time is 6:15 PM... 33 minutes before the end of the business day..."* (the Writer even fabricated a plausible-sounding elaboration on top of the wrong time).
**Verification block confirms:** `fault_is_unambiguous_single_node: true`, `propagation_verdict: "propagated_blindly"`, `ground_truth_recoverable: true`.

**Reasoning:** because the fabricated store hours can't be independently verified by the downstream agent (unlike "capital of France," which is common knowledge), the fault propagated cleanly and unambiguously — exactly the clean, recoverable ground-truth case the benchmark needs. This is also a genuinely useful design insight for the real benchmark build: injecting corruptions into *unverifiable* facts (not well-known ones) produces more reliable, unambiguous ground truth than injecting into facts a capable agent might catch on its own.

---

## Spike 4 — Silent-Failure Detector

**What it tests:** two things — (1) does a natural, un-injected task produce a real silent failure to test detection on, and (2) does the rule-based checker itself correctly catch known-wrong values.

**Setup:** n=3 real math word-problems run live through the local model, each requiring the model to state a final numeric answer.

| Case | Correct answer | Model's stated answer | Model actually wrong? | Detector verdict |
|---|---|---|---|---|
| gift_card | $19.75 | $19.75 | No | PASS |
| discount_then_tax | $73.44 | $73.44 | No | PASS |
| compound_trip | 1.6833 hrs | 1.68 hrs | No (rounding-correct) | PASS |

**Reasoning:** the model got all 3 cases right, so there was no naturally-occurring silent failure to test the detector against — `n_true_silent_failure_cases: 0`. This is an honest limitation, not a hidden one: it tells you nothing about how often silent failures occur "in the wild." **What it does confirm** (from the separately-run direct mechanism test, not shown in this specific output file but recorded in risk-register.md R10): when fed known-wrong values — including a plausible near-miss like $20.00 vs. the true $19.75 — the rule-based checker correctly flagged every one, with zero false positives on the correct cases above. The mechanism works; what's still needed is a larger sample with real injected near-misses to measure detection rate at any meaningful scale.

---

## Spike 5 — Controlled Counterfactual Replay

**What it tests:** if you correct one step's output and deterministically re-execute downstream, does the pipeline's final outcome actually flip from failure back to success?

**Setup:** 3-step deterministic pipeline (no LLM) — extract price → apply 8% tax → check against expected total ($108.00).

**Output:**
```
Original correct trace:  price=100 → total=108.0  → PASS
Corrupted trace:         price=90  → total=97.2   → FAIL
Counterfactual replay:   price corrected to 100 → total=108.0 → PASS
recovery_success: true
```

**Reasoning:** this confirms the *mechanism* — correcting a step and re-computing downstream really does recover the correct final answer. It's intentionally narrow: it tests only the replay logic, not whether an LLM can correctly *guess* the right correction on a real failure. That's a separate, still-open question. But the architectural assumption the whole replay feature depends on — "if we fix the right thing, does re-computation actually produce the right answer" — is now proven, not assumed.

**Scope note on the word "deterministic" (added 2026-08-25, risk-register.md R25):** this spike was genuinely, fully deterministic — but *only because its 3-step pipeline is pure arithmetic with no LLM in it*. That does **not** generalize to real workflows whose steps are LLM calls, which are not deterministic even at temperature 0 on most serving stacks. The committed feature is therefore **controlled counterfactual replay**, not deterministic re-execution: the *protocol* is deterministic (which steps re-run, frozen upstream context, pinned decoding parameters) and all non-LLM computation is bit-identical, while LLM-step variance is measured — recovery rate over N replays, reported with its variance. Stating the boundary here, in the evidence file itself, so nobody reads this spike's clean `recovery_success: true` as proof of something broader than it tested.

---

## Spike 6 — Cyclic Graph Handling

**What it tests:** does backward causal tracing terminate correctly on a real cycle instead of looping forever, given LangGraph natively supports retry loops?

**Three cases run:**
1. **Unrolled retry loop** (Planner→Researcher→Critic→Researcher→Critic→Writer→FAILURE, no true cycle): traversal terminated cleanly, all 7 nodes reached.
2. **True cycle** (Researcher ↔ Critic, a real back-edge): traversal terminated cleanly with a revisit bound of 3, all 5 nodes reached — Researcher visited 3×, Critic visited 4×.
3. **Control — same true-cycle graph, revisit bound disabled:** traversal did **not** terminate cleanly — hit the 10,000-step safety cap.

**Reasoning:** case 3 is the important one — it's the negative control proving the revisit bound is actually doing real work, not just happening to pass by coincidence. Without the bound, the exact same graph hangs; with it, it terminates correctly and still visits every node. This is solid, complete evidence the mechanism works as designed.

---

## Spike 7 — Preventive Classifier

**What it tests:** does a cheap TF-IDF + logistic regression classifier get any real signal distinguishing clean vs. corrupted agent-handoff messages?

**Setup:** n=20 hand-written examples (10 clean, 10 corrupted — corrupted ones have swapped values, missing context, contradictory statements), 60/40 train/test split, `random_state=42`.

**Output:** `precision: 0.25` · `recall: 0.25` · `f1: 0.25`

**Reasoning:** this is an honest negative result, not hidden or softened. Near-random performance on n=20 hand-written examples means one of two things: the sample is too small and unrepresentative of real corruption patterns (most likely — 8 test examples is nowhere near enough to learn from, and hand-authored examples don't match what the real fault-injection harness will produce), or plain bag-of-words features are genuinely too weak for this task. **Before dropping this extension**, the next step is re-testing with real labeled pairs generated by the fault-injection harness (not hand-written) and, if that still doesn't work, trying cheap local sentence-embedding features instead of raw TF-IDF. Re-run twice, byte-identical results both times — this is a real, reproducible finding, not noise.

---

## Spike 8 — Repair Agent

**What it tests:** given a diagnosed, wrong step value plus unambiguous supporting evidence, can the local model *generate* a usable corrected value — the one foundational feature (added 2026-08-24, sourced from `Agentic_AI_Market_Survey_BS_FYP.docx`) that had zero POC evidence until this spike. Chains straight into Spike 5's replay logic: each generated value is fed downstream and checked for a passing final result, matching the market survey's own Table 4 definition of "repair success rate."

**Setup:** n=6 synthetic single-step correction cases (tax total, loyalty discount, stock count, notebook order, connecting flight, budget check), local `llama3.2:3b` via Ollama, free, same backbone as every other spike.

**Output:** `repair_success_rate: 0.667` (4/6) · `exact_match_rate: 0.667` (4/6, same 4 cases) · `n_parse_failures: 0`

| Case | True value | Generated value | Exact match? | Repair success? |
|---|---|---|---|---|
| tax_total | 100.0 | 100.0 | ✅ | ✅ |
| loyalty_discount | 15.0 (%) | 6.75 | ❌ | ❌ |
| stock_count | 21.0 | 21.0 | ✅ | ✅ |
| notebook_order | 7.0 | 28.0 | ❌ | ❌ |
| connecting_flight | 14.0 | 14.0 | ✅ | ✅ |
| budget_check | 420.0 | 420.0 | ✅ | ✅ |

**Reasoning:** the 2 failures share one precise root cause, not two unrelated ones — in both `loyalty_discount` and `notebook_order`, the model correctly extracted the right underlying fact from the evidence (15% discount, 7 notebooks) but returned the *downstream computed result* ($6.75, $28.00) instead of the *specific atomic parameter* the pipeline actually needed (15, 7). That's a specification/interface ambiguity in what "corrected_value" means, not a reasoning failure — the model never got the underlying fact wrong. This is a genuinely useful, actionable finding for the real build: Repair Agent's interface needs to pin down exactly which field is being corrected, the same way Error Step Localization already pins down a specific step index, rather than leaving "the corrected value" open to being read as either a parameter or a computed answer. A real, working mechanism on a free local model with a precise fix identified — not a clean pass, and reported exactly as found.

---

## One-line summary per spike, for a quick read

1. **ErrorProbe repro** — agent-level attribution works (50–71% across 5 runs, mean 61%), step-level needs the full pipeline (0–25%, mean 13%)
2. **CrewAI mapping** — clean, resolved
3. **Fault injection** — works, and taught us to prefer unverifiable-fact corruptions over well-known-fact ones
4. **Silent-failure detector** — mechanism proven, real-world frequency still unmeasured
5. **Controlled counterfactual replay** — mechanism proven, recovery confirmed (on a pure-arithmetic pipeline; the LLM-step variance claim is measured, not inherited from this spike)
6. **Cyclic graph handling** — proven, including proof the safety bound is load-bearing
7. **Preventive classifier** — honest failure, mitigation plan identified, not yet fixed
8. **Repair Agent** — works 4/6, both failures traced to one fixable interface-specification issue, not a reasoning gap

---

## Appendix: Market Survey — Recommended System Flow & Evaluation Metrics (full excerpt)

*Spike 8 above tested step 5 of this flow (Repair Agent) specifically. Reproduced verbatim from `Agentic_AI_Market_Survey_BS_FYP.docx` (via [Agentic_AI_Market_Survey_Full_Content_and_Integration.md](../03-market-and-literature-research/Agentic_AI_Market_Survey_Full_Content_and_Integration.md)) so this spike-output file is self-contained.*

### 6.1 Recommended System Flow

*(Figure 1: Execute MAS → Detect Failure → Localise Cause → Generate Repair → Verify Repair → Resume Workflow → Store Repair)*

1. **Multi-Agent Runtime:** Use an existing framework for Planner/Worker/Reviewer or similar agents.
2. **Trace Collector:** Store agent messages, tool calls, outputs, exceptions and checkpoint identifiers.
3. **Semantic Failure Detector:** Identify failures that may not be ordinary runtime exceptions, using constraints, evaluator signals or task-specific checks.
4. **Root-Cause Localizer:** Estimate the culprit agent and originating error step using backward dependency/trace reasoning.
5. **Repair Agent:** Generate a targeted correction to the prompt, tool arguments, structured output or function logic associated with the localized failure.
6. **Verification Agent:** Test candidate repairs using deterministic checks, sandbox execution, test cases or evaluator constraints.
7. **Recovery Controller:** Apply only verified repairs and resume execution from a safe checkpoint instead of restarting the entire workflow.
8. **Verified Repair Memory:** Store successful error → diagnosis → repair patterns and retrieve them for similar future failures.
9. **Dashboard:** Visualize the workflow, failed agent, originating step, repair attempt, verification result and final recovered execution.

### 8. Evaluation Plan

*Table 4. Recommended quantitative evaluation metrics for the FYP.*

| Metric | What It Measures | Suggested Comparison |
|---|---|---|
| Task completion rate | Whether the full task succeeds | Baseline MAS vs. self-healing MAS |
| Failure detection precision/recall | Quality of semantic failure detection | Detector variants |
| Culprit-agent accuracy | Correct responsible agent | Root-cause module vs. simple last-error baseline |
| Error-step accuracy | Correct originating step | Backward tracing vs. full-trace judge |
| Repair success rate | Percentage of generated repairs that fix the task | With vs. without verification |
| Recovery rate | Failed runs converted into successful runs | Baseline retry vs. targeted repair |
| Re-execution cost | Tokens/tool calls/time after failure | Restart-from-zero vs. checkpoint resume |
| Repair reuse benefit | Improvement when verified memory is enabled | Memory off vs. memory on |
| False repair rate | Incorrect repairs accepted by system | Verification ablation |
