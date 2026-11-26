# Refund Desk feasibility validation: results and how to read them

Run on 2026-10-07 with `research/eval/validate_refund_desk.py` under [`prereg-v1.md`](../prereg-v1.md) (SHA-256 `63fd0a25a5c1e1dd`). Raw data: [`2026-10-07_refund-desk-feasibility.json`](2026-10-07_refund-desk-feasibility.json) (SHA-256 `38407eba11cc4626`, repository HEAD `46a591165e` with an uncommitted working tree), generated summary: [`2026-10-07_refund-desk-feasibility.md`](2026-10-07_refund-desk-feasibility.md). Model `llama3.2:3b`, 10 tasks, each run clean and with the stale-price fault, seed 1; verification N=5 replays and M=2 controls. All 20 runs and 40 experiments completed; none had to be re-run.

## Results against the pre-registered thresholds

| Metric | Result (95% Wilson interval) | Threshold | Outcome |
|---|---|---|---|
| M1 detection of the injected fault | 10/10 (72% to 100%) | at least 90% | Met |
| M2 false alarms on clean runs | 0 of 10 (see below: 1 finding, a true failure) | 0 | Met |
| M3 attribution top-1 / top-3 | 10/10 and 10/10 (72% to 100%) | top-1 at least 80% | Met |
| M4 origin step CONFIRMED | 9/10 (60% to 98%) | at least 80% | Met, with one miss explained below |
| M5 innocent step REFUTED | 10/10 (72% to 100%) | at least 80% | Met |
| M6 runs completed | 20/20 (84% to 100%) | at least 95% | Met |

## Things you must know before quoting these numbers

1. **Not fully blind.** The model answers for the first four tasks were recorded, and some of their outcomes seen, while the demo recording was made *before* the pre-registration was written. The thresholds and the system were not changed afterwards, but those four tasks are not independent confirmation. On the six tasks that were fresh (tasks 5 to 10): detection 6/6, top-1 6/6, origin confirmed 5/6, innocent refuted 6/6, and the only clean-run finding and the only miss are both among them.
2. **M3 is easy by construction.** The lookup step has its own check against the catalogue (`CT-LOOKUP`), so the injected fault leaves direct, step-level evidence at the true origin and the ranking follows it. 10/10 shows the pipeline works when the origin step has a check; it says little about workflows where it has none (the method then falls back to structural ranking with modest scores, which is untested here).
3. **M5 is a weak test.** Fixing the calculator cannot repair a wrong price, so refutation is nearly guaranteed. It shows the rule can say no, not that it separates close calls.
4. **One workflow, one fault, one small model, synthetic data, 10 tasks.** The intervals are wide (the lower bound of M4 is 60%). Nothing here shows generalisation, and there is no baseline comparison.
5. **The plan's stricter acceptance criterion for FR-ATT-01** (origin ranked first in at least 95% of 20 runs) was **not** measured; this run used 10 tasks and an 80% threshold.

## M2: the one finding on a clean run (task #W1335809)

Inspected by hand as the pre-registration requires. The customer asked to return the Espresso Machine (2805.77) and Hiking Boots (241.90): the correct refund is 3047.67. The workflow told the customer **4047.67**, wrong by exactly 1000. The Refund Calculator step also failed its own check, and attribution would point there. So this is a **true natural failure of the model**, not a false alarm: Granite caught an error nobody injected.

## M4: the one miss (task #W1326557), explained

With the lookup fixed, verification replayed the later steps five times and the outcome was still wrong every time, so the origin was REFUTED (0/5). A post-hoc offline replay from the recorded answers (exploratory, not part of the metrics) shows why: the Refund Calculator adds 47.76 and 1018.68 as **1166.44** instead of 1066.44 in all five replays, a deterministic 100-unit slip of the 3B model on this input (on the clean run at seed 1 it happened to be right). So there were **two faults in the chain**: the injected stale price and a natural arithmetic error that the first masked. VR-1 requires the target checks to pass after the single intervention, so a single-point fix cannot be CONFIRMED while a second fault remains. That is a limitation of the one-step intervention, not a bug in the rule. Candidate remedies (not applied, because the protocol is frozen): an intervention that fixes several steps, or judging only the target step's own contract. Logged as defect D-19.

## What this supports for Mid-1

That the Run, Check, Detect, Trace, Verify loop works end to end on a real small model, on data from a published benchmark, with the failures that the model produces naturally (arithmetic slips) showing up in the same pipeline. It does not support any claim about accuracy in general, about harder faults, or about other workflows.

## Reproduce

`ollama pull llama3.2:3b`, `ollama serve`, then `python research/eval/validate_refund_desk.py`. Every model answer is also stored in `data/cassettes/refund_desk_v1.json`, so the analysis (not the model calls) can be re-run offline and gives identical results.
