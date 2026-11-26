# Pre-registration v2: benchmark v0 on Refund Desk (three fault types, baselines, two ablations)

Written 2026-11-15, before any run of `research/eval/benchmark_v0.py`. The harness stores the SHA-256 of this file
with its results; a changed file means a new version and a new run. It is **not yet committed to git**: the hash in
the results file is the only proof of what was fixed in advance, so commit this file before quoting any result.

Written by the AI assistant at the request of Shahoud Shahid (see the AI usage log, twenty-sixth session). The team
has not yet reviewed it.

## Questions

| ID | Question |
|---|---|
| RQ0 | Does detection still work, and stay quiet on clean runs, with three kinds of silent failure instead of one? |
| RQ1 | Does VR-1 (5 replays with the fix, 2 without) confirm fewer innocent steps than a single replay with no control? |
| RQ2 | How does top-1 attribution change when step checks are missing, and does verification recover any of the loss? |

## Fixed setup

- **System:** Refund Desk, 5 steps, model `llama3.2:3b` through local Ollama, prompt version v1, temperatures as in
  `refund_desk/steps.py` (0.0 for Intake, 0.2 for the Calculator and the Writer). Checks as in
  `refund_desk/definition.py` on 2026-11-15: three outcome checks and five step checks (CT-INTAKE and CT-LOOKUP at
  version 2). No repair rules: every intervention is derived from a failed check (ADR-011).
- **Population:** the 10 delivered-order example tasks of `RetailStore.example_tasks(12)` (the same 10 as v1).
- **Conditions per task:** clean; `stale_price` (s2); `dropped_item` (s1); `handoff_drift` (s4, in transit from s3).
  40 runs, run seed 1. Every model answer is saved to `data/cassettes/refund_desk_v1.json`, so the whole study replays
  offline.
- **Ground truth:** the fault's target step. It is read only by the scoring code, never by detection, attribution or
  verification.
- **Verification:** N = 5, M = 2, base seed 1000, rule VR-1. Investigation budget 21 replays.

## Definitions

- **Detected:** the run completed and at least one outcome check failed.
- **False alarm:** a finding on a clean run. Reported as a raw count; a person then labels each one as a genuine model
  error or a false alarm, and both numbers are reported.
- **Symptom step:** the step of the first failed outcome check, in definition order.
- **Coverage:** the share of the five step checks kept. Levels: 100% (5 kept), 60% (3 kept), 40% (2 kept). At 60% and
  40%, three subsets per run are drawn with `random.Random("<order>|<fault>|<level>|<draw>")`. Outcome checks are
  always kept. The 30% level in the completion plan is not possible with five checks; 40% is the nearest.
- **Methods** (top-1 step, scored on detected faulty runs only):

| Method | Answer |
|---|---|
| `last_agent` | the symptom step |
| `earliest_check` | the earliest step, in run order, with a failed step check among those kept; else the symptom step |
| `llm_judge` | the step a single model call names when shown the whole trace (steps, inputs, outputs, no check results); full information only |
| `granite_rank` | the first hypothesis of `granite_core.attribution.attribute` on the kept checks |
| `granite_verified` | the step confirmed by `granite_core.investigation.investigate` over the ranking, with interventions derived from the kept checks only; if nothing is confirmed, the `granite_rank` answer |

- **Nondeterminism ablation (RQ1):** on every detected faulty run, a *placebo* experiment on one innocent step: the
  innocent ancestor of the symptom nearest to it, patched with its own unchanged output. Any confirmation there is
  luck. Compared: VR-1's verdict, against a single replay with no control that counts as "confirmed" if that one
  replay passes. The same comparison is made on the true origin where an experiment on it ran.

## Expectations, stated before the run

These are predictions, not pass thresholds. Every one is reported whether it holds or not.

| ID | Prediction |
|---|---|
| E1 | Detection of at least 90% of faulty runs |
| E2 | At most 1 of 10 clean runs with a finding (v1 found one genuine model error on #W1335809) |
| E3 | At 100% coverage, `granite_rank` and `earliest_check` tie at or near 100%: each fault is caught by its origin's own check, so the easy baseline is enough here |
| E4 | At 40% coverage, `granite_rank` falls below 100%, and `granite_verified` is no lower than `granite_rank` |
| E5 | VR-1 confirms no more innocent placebo steps than the single replay does |

## Reporting

Counts, Wilson 95% intervals and the per-run table, for every metric and method, including ties and losses. Only
infrastructure failures (model unreachable, timeouts) may be re-run, and each is listed. Results carry the git commit,
a dirty-tree flag, the SHA-256 of this file and of the source files that define the system.

## Not claimed

Anything beyond this workflow, these three faults (written by the team) and this model. In particular, the faults
and the checks that catch them were designed together; the coverage ablation exists to measure how much that matters.
No comparison with any product or paper.
