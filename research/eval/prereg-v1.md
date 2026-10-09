# Pre-registration v1: Refund Desk feasibility validation

Written 2026-10-07, before any run of `research/eval/validate_refund_desk.py`. Scope: **feasibility validation for Mid-1**, not the full evaluation of master plan section 27.5 (no baselines yet, one workflow, one fault). It answers one question: does the Run, Check, Detect, Trace, Verify loop work on a real model, on data it was not tuned on?

## Setup (fixed in advance)

- System under test: Refund Desk (5 steps), model `llama3.2:3b` via local Ollama, temperatures as in `refund_desk/steps.py`, prompt version v1.
- Population: the 10 delivered-order example tasks from `RetailStore.example_tasks(12)` (the two not-eligible examples are excluded: they cannot carry a price fault).
- Runs: each task once clean and once with fault `stale_price` (price of a requested item reduced by 0.25 by the lookup tool, no error). Run seed 1. Verification experiments use N=5 replays, M=2 controls, base seed 1000, rule VR-1.
- Data: `data/seed/taubench_retail_v1` (synthetic; the same file feeds the workflow's tool and, separately, the checks' source of truth).
- Nothing in the prompts, checks, attribution weights or thresholds will be changed after seeing these results. Any change after the run is a new version of this document and a new run.

## Metrics and thresholds

| ID | Metric | Computed on | Pass threshold |
|---|---|---|---|
| M1 | Detection rate: a finding is opened by an outcome check | 10 faulty runs | at least 90% |
| M2 | Natural failures and false alarms: every finding on a clean run is inspected by a person; a finding is a *true natural failure* if the customer message really is wrong, a *false alarm* otherwise | 10 clean runs | false alarms: 0 |
| M3 | Attribution top-1: the first-ranked hypothesis is the injected step (s2); also top-3 | 10 faulty runs | top-1 at least 80% |
| M4 | Verification of the origin: VR-1 verdict CONFIRMED when replaying from the injected step | 10 faulty runs | at least 80% |
| M5 | Verification of an innocent step: VR-1 verdict REFUTED when replaying from the Refund Calculator (s4) | 10 faulty runs | at least 80% |
| M6 | Run completion: share of runs that finish without an infrastructure error (timeout, unreachable model) | all runs | at least 95% |

Report with each rate: the count, the Wilson 95% confidence interval, and the per-task table. With 10 tasks the intervals are wide; no claim beyond this workflow, fault and model is made.

## Not claimed

Generalisation to other workflows, faults, models or real production traffic; superiority over any baseline; the true natural failure rate of the model (10 clean runs only estimate it roughly); human-factors results (no user study here).

## Reporting rules

All runs are reported, including failures. Only infrastructure failures (timeouts, unreachable model) may be re-run, and each re-run is listed. Results are stored with the commit hash and a dirty-tree flag, the SHA-256 of this file, and the SHA-256 of the source files that define the system.
