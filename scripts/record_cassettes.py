"""Record real model responses so the demo and the tests can run offline (Granite 'recorded mode').

Runs the Refund Desk against a local Ollama model, clean and with the stale-price fault, plus the verification
experiments for the faulty runs, and stores every model response in one cassette file. Takes ~15-20 minutes on a
CPU-only laptop; re-running refreshes the entries. Needs `ollama serve` and `ollama pull <model>`.

    python scripts/record_cassettes.py [--model llama3.2:3b] [--tasks 4]
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from granite_api.providers import OllamaProvider
from granite_core.checks import derive_findings, evaluate_checks
from granite_core.experiment import run_experiment
from granite_core.llm import Cassette, RecordingProvider
from granite_core.runner import run_workflow
from refund_desk import DEFAULT_MODEL, build_workflow, default_store, make_fault

ROOT = Path(__file__).resolve().parents[1]
RUN_SEED, EXPERIMENT_SEED = 1, 1000


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--tasks", type=int, default=4, help="how many example tasks get clean + faulty runs")
    ap.add_argument("--experiments", type=int, default=2, help="how many faulty runs also get verification replays")
    ap.add_argument("--out", default=str(ROOT / "data" / "cassettes" / "refund_desk_v1.json"))
    args = ap.parse_args()

    store = default_store()
    defn = build_workflow(store, args.model)
    cassette = Cassette(args.out)
    llm = RecordingProvider(OllamaProvider(), cassette)
    examples = store.example_tasks(12)
    eligible = [t for t in examples if "(delivered)" in t["label"]][: args.tasks]
    refused = [t for t in examples if "(delivered)" not in t["label"]]
    truth = defn.truth()
    t_start = time.time()

    def task_input(t: dict[str, str]) -> dict[str, str]:
        return {k: t[k] for k in ("message", "email", "order_id")}

    for i, t in enumerate([*eligible, *refused]):
        for fault_name in (None, "stale_price") if t in eligible else (None,):
            out = run_workflow(defn, task_input(t), llm, fault=make_fault(fault_name), seed=RUN_SEED)
            results = evaluate_checks(out.trace, defn.checks, truth)
            findings = derive_findings(out.trace, results)
            print(f"[{time.time() - t_start:5.0f}s] {t['label']} fault={fault_name} status={out.trace.run.status} "
                  f"failed={[r.check_id for r in results if r.status.value == 'fail']} findings={len(findings)}", flush=True)
            if fault_name and i < args.experiments and out.trace.run.status == "completed" and findings:
                targets = [r.check_id for r in results if r.scope == "outcome" and r.status.value == "fail"]
                for step_id in ("s2", "s4"):
                    exp = run_experiment(defn, out.trace, step_id, llm, 5, 2, targets, base_seed=EXPERIMENT_SEED)
                    print(f"[{time.time() - t_start:5.0f}s]   replay from {step_id}: {exp.summary.verdict.value} "
                          f"k={exp.summary.k_pass}/{exp.summary.n_completed} c={exp.summary.c_pass}/{exp.summary.m_completed}",
                          flush=True)
    print(f"done: {len(cassette)} recorded responses in {args.out} ({time.time() - t_start:.0f}s)")


if __name__ == "__main__":
    main()
