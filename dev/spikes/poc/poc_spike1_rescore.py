# -*- coding: utf-8 -*-
"""
Rescores the 5 already-collected real Spike 1 runs (poc_spike1_run{1..5}
_output.json) using the agent-name normalization fix in
poc_spike1_errorprobe_repro.py's normalize_agent(), then regenerates the
live output file and the multi-run aggregate.

Why rescoring, not re-running: the raw LLM predictions (pred_agent,
pred_step, hypotheses, everything) are untouched -- this only corrects
how "does the predicted agent match the ground-truth agent" is judged
for cases where the model answered with a compound role label
("Orchestrator (thought)") instead of the bare agent name ground truth
always uses. That is a pure scoring-logic question, fully determined by
data already on disk; re-running the LLM would burn ~4 more hours to
regenerate the identical raw predictions this script already has.

Only agent_correct / agent_accuracy change. step_accuracy is untouched
-- normalize_agent() has no bearing on step comparison.
"""
import json
from pathlib import Path

from poc_spike1_errorprobe_repro import normalize_agent

HERE = Path(__file__).parent
N_RUNS = 5


def rescore_file(fp: Path):
    data = json.loads(fp.read_text(encoding="utf-8"))
    correct = 0
    flips = []
    for r in data["results"]:
        if r["status"] != "ok":
            continue
        gt_n, pred_n = normalize_agent(r["gt_agent"]), normalize_agent(r["pred_agent"])
        new_ok = isinstance(pred_n, str) and pred_n.strip().lower() == gt_n.strip().lower()
        if new_ok != r["agent_correct"]:
            flips.append((r["case"], r["gt_agent"], r["pred_agent"], r["agent_correct"], new_ok))
        r["agent_correct"] = new_ok
        correct += int(new_ok)
    data["summary"]["agent_accuracy"] = round(correct / data["summary"]["n_scored"], 3) if data["summary"]["n_scored"] else None
    data["summary"]["note"] += " [Rescored 2026-08-26: agent-name comparison now normalizes turn-type suffixes like '(thought)' -- see normalize_agent() in poc_spike1_errorprobe_repro.py. Raw predictions unchanged.]"
    fp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return data["summary"]["agent_accuracy"], flips


def main():
    all_flips = []
    agent_accs = []
    for i in range(1, N_RUNS + 1):
        fp = HERE / f"poc_spike1_run{i}_output.json"
        acc, flips = rescore_file(fp)
        agent_accs.append(acc)
        all_flips.extend((i, *f) for f in flips)
        print(f"run{i}: agent_accuracy -> {acc}" + (f"  flips: {flips}" if flips else ""))

    # the "live" file mirrors whichever run was written last by the main
    # script (run 5) -- keep that convention, now rescored
    live = HERE / "poc_spike1_errorprobe_repro_output.json"
    live.write_text((HERE / f"poc_spike1_run{N_RUNS}_output.json").read_text(encoding="utf-8"), encoding="utf-8")

    # rebuild the multi-run aggregate with corrected agent_accuracy;
    # step_accuracy and per-case step consistency are untouched
    per_case = {}
    for i in range(1, N_RUNS + 1):
        d = json.loads((HERE / f"poc_spike1_run{i}_output.json").read_text(encoding="utf-8"))
        for r in d["results"]:
            if r["status"] != "ok":
                continue
            c = r["case"]
            per_case.setdefault(c, {"agent_correct_count": 0, "step_correct_count": 0, "n_runs": 0})
            per_case[c]["n_runs"] += 1
            per_case[c]["agent_correct_count"] += int(r["agent_correct"])
            per_case[c]["step_correct_count"] += int(r["step_correct"])

    step_accs = [json.loads((HERE / f"poc_spike1_run{i}_output.json").read_text(encoding="utf-8"))["summary"]["step_accuracy"] for i in range(1, N_RUNS + 1)]

    def stats(xs):
        n = len(xs)
        mean = sum(xs) / n if n else None
        return {"n_runs": n, "values": xs, "mean": round(mean, 3) if mean is not None else None, "min": min(xs) if xs else None, "max": max(xs) if xs else None}

    summary = {
        "n_runs_completed": N_RUNS,
        "n_runs_attempted": N_RUNS,
        "agent_accuracy": stats(agent_accs),
        "step_accuracy": stats(step_accs),
        "per_case_consistency": per_case,
        "note": (
            "Multiple independent LLM samples (temperature=0.2, llama3.2:3b local) of the same "
            "2-stage simplified reproduction on the same 8 Who&When-Hand cases, run 2026-08-26 after "
            "fixing the step_accuracy str/int comparison bug. Rescored 2026-08-26 (same day) for the "
            "agent-name normalization fix (turn-type suffixes like '(thought)' now stripped before "
            "comparison) -- raw LLM predictions unchanged, only the agent-match judgment corrected. "
            "Reported as a range, not a single point estimate, because run-to-run variance at n=8 is "
            "real and material (see agent_accuracy/step_accuracy min/max above)."
        ),
    }
    out_path = HERE / "poc_spike1_multirun_summary.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n=== RESCORED MULTI-RUN SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print(f"\nAll flips (case, gt, pred, old, new): {all_flips}")
    print(f"Written to {out_path}")


if __name__ == "__main__":
    main()
