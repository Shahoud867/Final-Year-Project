# -*- coding: utf-8 -*-
"""
Runs poc_spike1_errorprobe_repro.py N more times (as a subprocess, unmodified),
archiving each run's output as poc_spike1_run{k}_output.json so multiple real
LLM samples can be compared instead of reporting one point estimate.

Why this exists: a fresh 2026-08-26 re-run (after fixing the step_accuracy
str/int comparison bug) produced materially different numbers from the
cached run every doc in this repo cites (agent 50% vs 75%, step 0% vs
12.5%) -- pure LLM sampling variance at temperature=0.2 on n=8 cases, not
a bug. Rather than pick one run as "the" number, this collects several
real runs and reports the range, per the statistical-rigor commitments
already added in 06_Expanded_Scope_and_Feasibility_Plan.md.

Run 1 is the fresh run already completed and archived by hand as
poc_spike1_run1_output.json before this script starts. This script adds
runs 2..N_TOTAL.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
SCRIPT = HERE / "poc_spike1_errorprobe_repro.py"
LIVE_OUTPUT = HERE / "poc_spike1_errorprobe_repro_output.json"
PYTHON = sys.executable
N_TOTAL = 5  # run 1 already done by hand; this adds runs 2..5


def run_one(run_idx: int):
    print(f"\n=== starting run {run_idx}/{N_TOTAL} ===", flush=True)
    result = subprocess.run([PYTHON, str(SCRIPT)], cwd=str(HERE))
    if result.returncode != 0:
        print(f"=== run {run_idx} FAILED (exit {result.returncode}) -- leaving no archive for this run ===", flush=True)
        return False
    dest = HERE / f"poc_spike1_run{run_idx}_output.json"
    shutil.copy(LIVE_OUTPUT, dest)
    data = json.loads(dest.read_text(encoding="utf-8"))
    s = data["summary"]
    print(f"=== run {run_idx} done: agent_accuracy={s['agent_accuracy']} step_accuracy={s['step_accuracy']} ===", flush=True)
    return True


def aggregate():
    runs = []
    for i in range(1, N_TOTAL + 1):
        fp = HERE / f"poc_spike1_run{i}_output.json"
        if fp.exists():
            runs.append((i, json.loads(fp.read_text(encoding="utf-8"))))

    agent_accs = [d["summary"]["agent_accuracy"] for _, d in runs]
    step_accs = [d["summary"]["step_accuracy"] for _, d in runs]

    # per-case consistency: how often each case was scored correct across runs
    per_case = {}
    for run_idx, d in runs:
        for r in d["results"]:
            if r["status"] != "ok":
                continue
            case = r["case"]
            per_case.setdefault(case, {"agent_correct_count": 0, "step_correct_count": 0, "n_runs": 0})
            per_case[case]["n_runs"] += 1
            per_case[case]["agent_correct_count"] += int(r["agent_correct"])
            per_case[case]["step_correct_count"] += int(r["step_correct"])

    def stats(xs):
        n = len(xs)
        mean = sum(xs) / n if n else None
        return {"n_runs": n, "values": xs, "mean": round(mean, 3) if mean is not None else None,
                "min": min(xs) if xs else None, "max": max(xs) if xs else None}

    summary = {
        "n_runs_completed": len(runs),
        "n_runs_attempted": N_TOTAL,
        "agent_accuracy": stats(agent_accs),
        "step_accuracy": stats(step_accs),
        "per_case_consistency": per_case,
        "note": (
            "Multiple independent LLM samples (temperature=0.2, llama3.2:3b local) of the same "
            "2-stage simplified reproduction on the same 8 Who&When-Hand cases, run 2026-08-26 after "
            "fixing the step_accuracy str/int comparison bug (see poc_spike1_errorprobe_repro.py "
            "as_int()). Reported as a range, not a single point estimate, because run-to-run variance "
            "at n=8 is real and material (see agent_accuracy/step_accuracy min/max above)."
        ),
    }
    out_path = HERE / "poc_spike1_multirun_summary.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n=== MULTI-RUN SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print(f"\nWritten to {out_path}")


def main():
    for i in range(2, N_TOTAL + 1):
        run_one(i)
    aggregate()


if __name__ == "__main__":
    main()
