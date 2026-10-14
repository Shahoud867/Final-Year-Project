"""Score attribution methods against the injected fault, and write one CSV per run (FR-EVA-01).

    python research/eval/score_attribution.py --tasks 10
    python research/eval/score_attribution.py --tasks 10 --out results/2026-10-15_attribution.csv

Granite's trace-back is compared with the two baselines in ``granite_core.baselines`` on the same
traces, scored by the same code, against the fault record as ground truth. The fault is read only
here, never by any method under test.

Recorded mode is the default, so the harness is deterministic and needs no model. It is the
measurement skeleton for the Iteration 2 benchmark, not the benchmark itself: one workflow and one
fault type, which is the honest limit of what Mid-1 can claim.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections.abc import Callable
from pathlib import Path

from granite_core.attribution import HypothesisSpec, attribute
from granite_core.baselines import last_agent, upstream_first
from granite_core.checks import derive_findings, evaluate_checks
from granite_core.llm import Cassette, RecordedProvider
from granite_core.runner import run_workflow
from granite_core.trace import TraceV1
from refund_desk import build_workflow, default_store, make_fault

ROOT = Path(__file__).resolve().parents[2]

Method = Callable[[TraceV1, str], list[HypothesisSpec]]


def methods(results: list) -> dict[str, Method]:
    """Every attributor under test, behind one signature so none is scored differently."""
    return {
        "granite": lambda t, s: attribute(t, results, s),
        "last_agent": last_agent,
        "upstream_first": upstream_first,
    }


def top_k(hyps: list[HypothesisSpec], truth_step: str, k: int) -> bool:
    return any(h.step_id == truth_step for h in hyps[:k])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tasks", type=int, default=10, help="how many example tasks to run")
    ap.add_argument("--out", default="", help="CSV path (default: results/attribution-scores.csv)")
    args = ap.parse_args()

    store = default_store()
    workflow = build_workflow(store)
    cassette = Cassette(ROOT / "data" / "cassettes" / "refund_desk_v1.json")
    provider = RecordedProvider(cassette)

    tasks = [t for t in store.example_tasks(12) if "(delivered)" in t["label"]][: args.tasks]
    if not tasks:
        print("no example tasks registered", file=sys.stderr)
        return 1

    rows: list[dict[str, object]] = []
    for task in tasks:
        fault = make_fault("stale_price")
        task_input = {k: task[k] for k in ("message", "email", "order_id")}
        outcome = run_workflow(workflow, task_input, provider, fault=fault, seed=1)
        trace = outcome.trace
        results = evaluate_checks(trace, workflow.checks, workflow.truth())
        findings = derive_findings(trace, results)
        if not findings:
            # a faulty run that no check caught is a miss for every method: record it as such
            rows.append({"task": task["order_id"], "method": "-", "detected": 0, "top1": 0, "top3": 0, "rank": ""})
            continue

        symptom = findings[0].symptom_step
        assert outcome.fault is not None
        truth_step = outcome.fault.target_step  # ground truth, read here and nowhere else
        for name, fn in methods(results).items():
            hyps = fn(trace, symptom)
            rank = next((h.rank for h in hyps if h.step_id == truth_step), None)
            rows.append({
                "task": task["order_id"],
                "method": name,
                "detected": 1,
                "top1": int(top_k(hyps, truth_step, 1)),
                "top3": int(top_k(hyps, truth_step, 3)),
                "rank": rank if rank is not None else "",
            })

    out = Path(args.out) if args.out else Path(__file__).parent / "results" / "attribution-scores.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["task", "method", "detected", "top1", "top3", "rank"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)} rows -> {out}")
    for name in methods([]):
        scored = [r for r in rows if r["method"] == name]
        if scored:
            hits = sum(int(r["top1"]) for r in scored)
            print(f"  {name:15} top-1 origin accuracy {hits}/{len(scored)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
