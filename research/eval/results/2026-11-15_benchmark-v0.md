# Benchmark v0, Refund Desk (2026-11-15)

Protocol: `research/eval/prereg-v2.md` (SHA-256 `aa090b75e7fc916f`). Model llama3.2:3b. HEAD `21eba51448`, working tree dirty: True. Mode: live.

| Metric | Result |
|---|---|
| Runs completed | 40/40 (100%, 91%-100%) |
| Faulty runs detected | 30/30 (100%, 89%-100%) |
| Detected, stale_price | 10/10 (100%, 72%-100%) |
| Detected, dropped_item | 10/10 (100%, 72%-100%) |
| Detected, handoff_drift | 10/10 (100%, 72%-100%) |
| Clean runs with a finding | 1/10 (10%, 2%-40%) |
| LLM judge top-1 (full information) | 10/30 (33%, 19%-51%) |
| Replays per investigation, full coverage | 7.0 |

## Top-1 attribution by step-check coverage

| Method | 100% | 60% | 40% |
|---|---|---|---|
| last_agent | 0/30 (0%, 0%-11%) | 0/90 (0%, 0%-4%) | 0/90 (0%, 0%-4%) |
| earliest_check | 30/30 (100%, 89%-100%) | 58/90 (64%, 54%-74%) | 40/90 (44%, 35%-55%) |
| granite_rank | 30/30 (100%, 89%-100%) | 81/90 (90%, 82%-95%) | 74/90 (82%, 73%-89%) |
| granite_verified | 30/30 (100%, 89%-100%) | 81/90 (90%, 82%-95%) | 74/90 (82%, 73%-89%) |

## Nondeterminism: confirmations by VR-1 and by a single replay

| Case | VR-1 confirms | Single replay confirms |
|---|---|---|
| Placebo on an innocent step (should be 0) | 0/30 (0%, 0%-11%) | 9/30 (30%, 17%-48%) |
| True origin | 121/128 (94%, 89%-97%) | 121/128 (94%, 89%-97%) |

## Per run

| Order | Fault | Status | Detected | Origin | Rank top-1 (100%) | Verified (100%) | Judge |
|---|---|---|---|---|---|---|---|
| #W1023987 | none | completed | False |  |  |  |  |
| #W1023987 | stale_price | completed | True | s2 | s2 | s2 | s4 |
| #W1023987 | dropped_item | completed | True | s1 | s1 | s1 | s4 |
| #W1023987 | handoff_drift | completed | True | s4 | s4 | s4 | s4 |
| #W1052399 | none | completed | False |  |  |  |  |
| #W1052399 | stale_price | completed | True | s2 | s2 | s2 | s3 |
| #W1052399 | dropped_item | completed | True | s1 | s1 | s1 | s4 |
| #W1052399 | handoff_drift | completed | True | s4 | s4 | s4 | s4 |
| #W1067251 | none | completed | False |  |  |  |  |
| #W1067251 | stale_price | completed | True | s2 | s2 | s2 | s4 |
| #W1067251 | dropped_item | completed | True | s1 | s1 | s1 | s3 |
| #W1067251 | handoff_drift | completed | True | s4 | s4 | s4 | s4 |
| #W1166549 | none | completed | False |  |  |  |  |
| #W1166549 | stale_price | completed | True | s2 | s2 | s2 | s3 |
| #W1166549 | dropped_item | completed | True | s1 | s1 | s1 | s4 |
| #W1166549 | handoff_drift | completed | True | s4 | s4 | s4 | s4 |
| #W1326557 | none | completed | False |  |  |  |  |
| #W1326557 | stale_price | completed | True | s2 | s2 | s2 | s3 |
| #W1326557 | dropped_item | completed | True | s1 | s1 | s1 | s3 |
| #W1326557 | handoff_drift | completed | True | s4 | s4 | s4 | s4 |
| #W1335809 | none | completed | True |  |  |  |  |
| #W1335809 | stale_price | completed | True | s2 | s2 | s2 | s3 |
| #W1335809 | dropped_item | completed | True | s1 | s1 | s1 | s4 |
| #W1335809 | handoff_drift | completed | True | s4 | s4 | s4 | s4 |
| #W1341845 | none | completed | False |  |  |  |  |
| #W1341845 | stale_price | completed | True | s2 | s2 | s2 | s3 |
| #W1341845 | dropped_item | completed | True | s1 | s1 | s1 | s4 |
| #W1341845 | handoff_drift | completed | True | s4 | s4 | s4 | s4 |
| #W1504875 | none | completed | False |  |  |  |  |
| #W1504875 | stale_price | completed | True | s2 | s2 | s2 | s4 |
| #W1504875 | dropped_item | completed | True | s1 | s1 | s1 | s4 |
| #W1504875 | handoff_drift | completed | True | s4 | s4 | s4 | s4 |
| #W1519594 | none | completed | False |  |  |  |  |
| #W1519594 | stale_price | completed | True | s2 | s2 | s2 | s3 |
| #W1519594 | dropped_item | completed | True | s1 | s1 | s1 | s4 |
| #W1519594 | handoff_drift | completed | True | s4 | s4 | s4 | s4 |
| #W1523776 | none | completed | False |  |  |  |  |
| #W1523776 | stale_price | completed | True | s2 | s2 | s2 | s3 |
| #W1523776 | dropped_item | completed | True | s1 | s1 | s1 | s4 |
| #W1523776 | handoff_drift | completed | True | s4 | s4 | s4 | s4 |
