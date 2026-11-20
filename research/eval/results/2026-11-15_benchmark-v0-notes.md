# Benchmark v0, 2026-11-15: how to read the results

Protocol: [`prereg-v2.md`](../prereg-v2.md), SHA-256 `aa090b75e7fc916f…` (stored in the results file). Numbers:
[`2026-11-15_benchmark-v0.md`](2026-11-15_benchmark-v0.md) and the full per-run record in the JSON beside it.

Written by the AI assistant that ran the study (AI usage log, twenty-sixth session). Not yet reviewed by the team.

## What was run

10 delivered-order tasks × {clean, stale_price, dropped_item, handoff_drift} = 40 runs, live on `llama3.2:3b`
through local Ollama, every answer saved to `data/cassettes/refund_desk_v1.json`. Wall time about 96 minutes on
one laptop. `python research/eval/benchmark_v0.py --offline` reproduces every metric from the recording alone (checked
on 2026-11-15: identical metrics in 4 seconds).

## Results against the predictions

| ID | Prediction | Result | Held? |
|---|---|---|---|
| E1 | Detection ≥ 90% | 30/30 (Wilson 89–100%); 10/10 for each fault | Yes |
| E2 | At most 1 of 10 clean runs flagged | 1/10: #W1335809, the same genuine model error found in v1 (the Calculator returns a wrong total) | Yes |
| E3 | At 100% coverage, Granite and the earliest-failing-check baseline tie near 100% | Both 30/30 | Yes |
| E4 | At 40% coverage Granite's ranking falls below 100%, and verification is no lower | Ranking 74/90 (82%); verification 74/90 (82%): equal, it recovered nothing | Yes, with no gain from verification |
| E5 | VR-1 confirms no more placebo steps than a single replay | VR-1 0/30; single replay 9/30 | Yes |

## What the numbers support

1. **Granite's ranking degrades more slowly than the simple baseline when checks are missing.** At 60% coverage 90%
   against 64%; at 40%, 82% against 44%. Intervals do not overlap at 40% (73–89% against 35–55%).
2. **Controls prevent false confirmations that a single replay makes.** On innocent steps patched with their own
   unchanged value, one replay "confirmed" 9 of 30, VR-1 none.
3. **Detection by executable checks against an independent source of truth caught all 30 injected failures**, with one
   flag on a clean run that is a real error, not a false alarm.

## What they do not support, and why

1. **Every faulty-run miss is the same case.** All 25 misses at reduced coverage are stale-price runs whose own check
   (CT-LOOKUP) was removed. With the origin unchecked, nothing in the trace marks Order Lookup as wrong.
2. **Dropped item stays at 100% partly by structure.** The symptom (CHK-OUT-3 at Policy) has two upstream steps; with
   Intake's check removed both are unchecked, and the earlier step wins the tie. That is a property of this workflow's
   shape, not evidence about the method.
3. **Handoff drift stays at 100% for a real reason.** The Calculator's recorded input differs from what Policy
   produced, and attribution reads that difference (`handoff_drift` evidence) even without the Calculator's check.
4. **Verification added nothing on top of ranking.** Interventions come from failed checks (ADR-011); removing the
   origin's check also removes the value a replay would need. Verification can confirm the ranking but cannot repair
   it when coverage is missing.
5. **All nine false confirmations come from one fault type.** In `handoff_drift` the damage happens in transit;
   replaying from Policy re-sends clean data, so the outcome is right whatever the patch. That is exactly the case
   controls exist for (a transient fault), but the 9/30 depends on how the fault was built.
6. **The LLM judge baseline is weak here** (10/30): it named the Calculator or Policy every time and was right only
   when the origin was the Calculator. A 3B model is a small judge; a larger one may do much better.
7. **The faults and the checks were written by the same team.** The coverage ablation measures how much that helps,
   but a system whose failures we did not author is still needed (the tau-bench Retail Agent, FYP-2).
8. **Ten tasks, one workflow, one model.** These are early numbers, not a benchmark.

## Deviations from the protocol

- The harness file was edited during the run for lint only (import order, two parentheses, one comment); the running
  process had already loaded it, and the edit changes no behaviour.
- The live run wiped the cassette's prompt fingerprint (the `Cassette` writer dropped unknown fields; fixed on
  2026-11-15 in `granite_core/llm.py`). It was restored with `scripts/check_cassette_prompts.py --write`; the prompts
  did not change.
- The pre-registration was hashed into the results before the run but is not yet committed to git. Commit it with the
  results before quoting them.
