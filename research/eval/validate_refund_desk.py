"""Mid-1 feasibility validation of Granite on Refund Desk. Protocol: research/eval/prereg-v1.md (read it first).

    python research/eval/validate_refund_desk.py            # needs `ollama serve` and the model pulled

Resumable: finished tasks are kept in the results file. Every model answer is also recorded in the shared cassette,
so the whole study can be replayed offline. Writes results/<date>_refund-desk-feasibility.{json,md}.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

from granite_api.providers import OllamaProvider
from granite_core.attribution import attribute
from granite_core.checks import derive_findings, evaluate_checks
from granite_core.experiment import run_experiment
from granite_core.llm import Cassette, RecordingProvider
from granite_core.runner import run_workflow
from granite_core.verification import wilson
from refund_desk import DEFAULT_MODEL, build_workflow, default_store, make_fault

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATE = "2026-10-07"
SOURCES = ["packages/granite_core/granite_core", "workflows/refund_desk/refund_desk"]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes() -> dict[str, str]:
    files = sorted(p for d in SOURCES for p in (ROOT / d).rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    return {str(p.relative_to(ROOT)).replace("\\", "/"): sha256_file(p) for p in files if p.suffix in {".py", ".md"}}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False).stdout.strip()


def run_one(defn, llm, task, fault_name):  # type: ignore[no-untyped-def]
    t0 = time.time()
    for attempt in (1, 2):  # only infrastructure failures may be re-run (prereg)
        out = run_workflow(defn, task, llm, fault=make_fault(fault_name), seed=1)
        infra = out.trace.run.status == "errored" and any(
            k in (s.error or "") for s in out.trace.steps for k in ("unreachable", "too slow", "HTTP 5")
        )
        if not infra:
            break
    return out, attempt, round(time.time() - t0, 1)


def study_task(defn, llm, truth, task):  # type: ignore[no-untyped-def]
    inp = {k: task[k] for k in ("message", "email", "order_id")}
    row: dict = {"order_id": task["order_id"], "label": task["label"]}
    out, tries, secs = run_one(defn, llm, inp, None)
    results = evaluate_checks(out.trace, defn.checks, truth)
    row["clean"] = {
        "status": out.trace.run.status, "attempts": tries, "seconds": secs,
        "failed_checks": [r.check_id for r in results if r.status.value == "fail"],
        "findings": [f.title for f in derive_findings(out.trace, results)],
        "message": out.trace.run.final_output.get("message", ""),
    }
    out, tries, secs = run_one(defn, llm, inp, "stale_price")
    results = evaluate_checks(out.trace, defn.checks, truth)
    findings = derive_findings(out.trace, results)
    faulty: dict = {"status": out.trace.run.status, "attempts": tries, "seconds": secs, "findings": len(findings),
                    "failed_checks": [r.check_id for r in results if r.status.value == "fail"],
                    "injected_step": out.fault.target_step if out.fault else None}
    if findings and out.trace.run.status == "completed":
        hyps = attribute(out.trace, results, findings[0].symptom_step)
        faulty["ranking"] = [h.step_id for h in hyps]
        targets = [r.check_id for r in results if r.scope == "outcome" and r.status.value == "fail"]
        for label, step in (("origin", "s2"), ("innocent", "s4")):
            exp = run_experiment(defn, out.trace, step, llm, 5, 2, targets, base_seed=1000)
            s = exp.summary
            faulty[label] = {"step": step, "verdict": s.verdict.value, "k": s.k_pass, "n": s.n_completed,
                             "c": s.c_pass, "m": s.m_completed}
    row["faulty"] = faulty
    return row


def rate(k: int, n: int) -> dict:
    lo, hi = wilson(k, n) if n else (0.0, 1.0)
    return {"k": k, "n": n, "rate": round(k / n, 3) if n else None, "ci95": [round(lo, 3), round(hi, 3)]}


def metrics(rows: list[dict]) -> dict:
    f = [r["faulty"] for r in rows]
    everything = [r["clean"] for r in rows] + f
    done = [x for x in f if x["status"] == "completed"]
    return {
        "M1_detection": rate(sum(1 for x in f if x["findings"] > 0), len(f)),
        "M2_clean_runs_with_findings": rate(sum(1 for r in rows if r["clean"]["findings"]), len(rows)),
        "M3_top1": rate(sum(1 for x in done if x.get("ranking", [""])[0] == x["injected_step"]), len(f)),
        "M3_top3": rate(sum(1 for x in done if x["injected_step"] in x.get("ranking", [])[:3]), len(f)),
        "M4_origin_confirmed": rate(sum(1 for x in done if x.get("origin", {}).get("verdict") == "confirmed"), len(f)),
        "M5_innocent_refuted": rate(sum(1 for x in done if x.get("innocent", {}).get("verdict") == "refuted"), len(f)),
        "M6_completion": rate(sum(1 for x in everything if x["status"] == "completed"), len(everything)),
    }


def markdown(meta: dict, rows: list[dict], m: dict) -> str:
    def cell(x: dict) -> str:
        return f"{x['k']}/{x['n']} ({x['rate']:.0%}, 95% CI {x['ci95'][0]:.0%}-{x['ci95'][1]:.0%})"

    lines = [f"# Refund Desk feasibility validation, {DATE}", "",
             f"Protocol: `research/eval/prereg-v1.md` (SHA-256 `{meta['prereg_sha256'][:16]}`). Model {meta['model']}. "
             f"HEAD `{meta['git_head'][:10]}`, working tree dirty: {meta['git_dirty']}.", "",
             "| Metric | Result |", "|---|---|"]
    names = {"M1_detection": "M1 detection (faulty runs)", "M2_clean_runs_with_findings": "M2 clean runs with a finding",
             "M3_top1": "M3 attribution top-1", "M3_top3": "M3 attribution top-3",
             "M4_origin_confirmed": "M4 origin CONFIRMED", "M5_innocent_refuted": "M5 innocent step REFUTED",
             "M6_completion": "M6 runs completed"}
    lines += [f"| {names[k]} | {cell(v)} |" for k, v in m.items()]
    lines += ["", "## Per task", "", "| Order | Clean run findings | Faulty: ranking | Origin verdict | Innocent verdict |",
              "|---|---|---|---|---|"]
    for r in rows:
        f = r["faulty"]
        lines.append(
            f"| {r['order_id']} | {len(r['clean']['findings'])} | {', '.join(f.get('ranking', []))} | "
            f"{f.get('origin', {}).get('verdict', '-')} {f.get('origin', {}).get('k', '')}/{f.get('origin', {}).get('n', '')} | "
            f"{f.get('innocent', {}).get('verdict', '-')} {f.get('innocent', {}).get('k', '')}/{f.get('innocent', {}).get('n', '')} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--tasks", type=int, default=10)
    args = ap.parse_args()
    store, out_json = default_store(), HERE / "results" / f"{DATE}_refund-desk-feasibility.json"
    defn = build_workflow(store, args.model)
    llm = RecordingProvider(OllamaProvider(timeout=240.0), Cassette(ROOT / "data" / "cassettes" / "refund_desk_v1.json"),
                            reuse=True)
    tasks = [t for t in store.example_tasks(12) if "(delivered)" in t["label"]][: args.tasks]
    state = json.loads(out_json.read_text("utf-8")) if out_json.exists() else {"rows": []}
    done = {r["order_id"] for r in state["rows"]}
    meta = {"date": DATE, "model": args.model, "prereg_sha256": sha256_file(HERE / "prereg-v1.md"),
            "git_head": git("rev-parse", "HEAD"), "git_dirty": bool(git("status", "--porcelain")),
            "source_sha256": source_hashes(), "n_tasks": len(tasks)}
    t0 = time.time()
    for task in tasks:
        if task["order_id"] in done:
            continue
        row = study_task(defn, llm, defn.truth(), task)
        state["rows"].append(row)
        state.update(meta=meta, metrics=metrics(state["rows"]))
        out_json.write_text(json.dumps(state, indent=1), "utf-8")
        print(f"[{time.time() - t0:5.0f}s] {task['order_id']} clean-findings={len(row['clean']['findings'])} "
              f"rank={row['faulty'].get('ranking')} origin={row['faulty'].get('origin', {}).get('verdict')} "
              f"innocent={row['faulty'].get('innocent', {}).get('verdict')}", flush=True)
    state["metrics"] = metrics(state["rows"])
    out_json.write_text(json.dumps(state, indent=1), "utf-8")
    out_json.with_suffix(".md").write_text(markdown(meta, state["rows"], state["metrics"]), "utf-8")
    print(json.dumps(state["metrics"], indent=1))


if __name__ == "__main__":
    main()
