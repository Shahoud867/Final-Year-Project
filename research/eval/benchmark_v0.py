"""Benchmark v0 on Refund Desk: three fault types, four baselines, a coverage ablation and a nondeterminism ablation.

Protocol: research/eval/prereg-v2.md (read it first; its SHA-256 is stored with the results).

    python research/eval/benchmark_v0.py               # live: needs `ollama serve` and llama3.2:3b
    python research/eval/benchmark_v0.py --offline     # replays the saved answers only (reproduces a finished run)

Resumable: finished tasks are kept in the results file. Every model answer is saved to the shared cassette, so a
finished study replays offline byte for byte. Writes results/<date>_benchmark-v0.{json,md}.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import random
import re
import subprocess
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from granite_api.providers import OllamaProvider
from granite_core.attribution import attribute
from granite_core.checks import (
    CheckResult,
    CheckStatus,
    derive_findings,
    evaluate_checks,
)
from granite_core.experiment import plan_intervention, run_experiment
from granite_core.investigation import VerifyOutcome, investigate
from granite_core.lineage import ancestors_with_distance
from granite_core.llm import (
    Cassette,
    LLMProvider,
    LLMRequest,
    RecordedProvider,
    RecordingProvider,
)
from granite_core.runner import WorkflowDef, run_workflow
from granite_core.trace import TraceV1
from granite_core.verification import Intervention, ReplayUnavailable, Verdict, wilson
from refund_desk import DEFAULT_MODEL, build_workflow, default_store, make_fault

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DATE = "2026-11-15"
FAULTS = ["stale_price", "dropped_item", "handoff_drift"]
LEVELS = {"100": 5, "60": 3, "40": 2}  # step checks kept out of five
DRAWS = 3
N, M, BUDGET, BASE_SEED = 5, 2, 21, 1000
SOURCES = ["packages/granite_core/granite_core", "workflows/refund_desk/refund_desk"]
JUDGE_PROMPT = (
    "You are debugging a multi-step AI workflow. It finished without an error, but its final answer is wrong. "
    "Each step lists what it received and what it produced. Identify the single step that first introduced the "
    'error. Answer with JSON only: {"step_id": "<id>", "reason": "<one sentence>"}.'
)


# ---- provenance ----------------------------------------------------------------------------------------------------


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes() -> dict[str, str]:
    files = sorted(p for d in SOURCES for p in (ROOT / d).rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    return {str(p.relative_to(ROOT)).replace("\\", "/"): sha256_file(p) for p in files if p.suffix in {".py", ".md"}}


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False).stdout.strip()


# ---- one run and its scoring -----------------------------------------------------------------------------------------


def with_checks(defn: WorkflowDef, keep_step_checks: list[str]) -> WorkflowDef:
    """The workflow with every outcome check and only the named step checks."""
    checks = [c for c in defn.checks if c.scope == "outcome" or c.id in keep_step_checks]
    return dataclasses.replace(defn, checks=checks)


def step_check_ids(defn: WorkflowDef) -> list[str]:
    return [c.id for c in defn.checks if c.scope == "step"]


def subsets(defn: WorkflowDef, order_id: str, fault: str) -> dict[str, list[list[str]]]:
    """The kept step checks per coverage level (prereg: three seeded draws below 100%)."""
    ids = step_check_ids(defn)
    out: dict[str, list[list[str]]] = {"100": [ids]}
    for level, keep in LEVELS.items():
        if level == "100":
            continue
        out[level] = [sorted(random.Random(f"{order_id}|{fault}|{level}|{d}").sample(ids, keep)) for d in range(DRAWS)]
    return out


def symptom_of(results: list[CheckResult]) -> str | None:
    failed = [r for r in results if r.scope == "outcome" and r.status is CheckStatus.FAIL]
    return failed[0].step if failed else None


def earliest_check(trace: TraceV1, results: list[CheckResult], symptom: str) -> str:
    failed = {r.step for r in results if r.scope == "step" and r.status is CheckStatus.FAIL}
    return next((s.step_id for s in trace.steps if s.step_id in failed), symptom)


def make_verify(
    defn: WorkflowDef, trace: TraceV1, llm: LLMProvider, targets: list[str], log: list[dict[str, Any]]
) -> Callable[[str], VerifyOutcome]:
    def verify(step_id: str) -> VerifyOutcome:
        try:
            exp = run_experiment(defn, trace, step_id, llm, N, M, targets, BASE_SEED)
        except ReplayUnavailable as exc:
            return VerifyOutcome(verdict=None, reason=str(exc))
        log.append(experiment_row(step_id, exp))
        return VerifyOutcome(verdict=exp.summary.verdict, replays_used=N + M)

    return verify


def experiment_row(step_id: str, exp: Any, kind: str = "intervention") -> dict[str, Any]:
    first = next((r for r in exp.replays if r.kind == "intervention"), None)
    single = bool(first and first.completed and first.judgement and first.judgement.passed)
    return {
        "step_id": step_id, "kind": kind, "verdict": exp.summary.verdict.value, "k": exp.summary.k_pass,
        "c": exp.summary.c_pass, "n_done": exp.summary.n_completed, "m_done": exp.summary.m_completed,
        "single_replay_confirms": single, "intervention": exp.intervention.model_dump(mode="json"),
    }


def llm_judge(trace: TraceV1, llm: LLMProvider, model: str) -> dict[str, Any]:
    lines = [
        f"{s.step_id} ({s.agent}, {s.kind})\n  received: {json.dumps(s.inputs, default=str)[:600]}\n"
        f"  produced: {json.dumps(s.outputs, default=str)[:600]}"
        for s in trace.steps
    ]
    req = LLMRequest(
        messages=[{"role": "system", "content": JUDGE_PROMPT}, {"role": "user", "content": "\n".join(lines)}],
        model=model, temperature=0.0, max_tokens=120, json_mode=True, seed=1,
    )
    try:
        text = llm.complete(req).text
    except Exception as exc:  # noqa: BLE001 - the judge failing is reported as no answer, never as a right one
        return {"answer": None, "raw": f"{type(exc).__name__}: {exc}"}
    m = re.search(r'"step_id"\s*:\s*"(s\d)"', text)
    return {"answer": m.group(1) if m else None, "raw": text[:300]}


def placebo_step(trace: TraceV1, symptom: str, origin: str) -> str | None:
    dist, _ = ancestors_with_distance(trace, symptom)
    order = {s.step_id: i for i, s in enumerate(trace.steps)}
    innocent = [(d, -order[s], s) for s, d in dist.items() if s not in (symptom, origin) and d >= 1]
    return min(innocent)[2] if innocent else None


def placebo(defn: WorkflowDef, trace: TraceV1, step_id: str, llm: LLMProvider, targets: list[str]) -> dict[str, Any]:
    step = trace.step(step_id)
    assert step is not None and step.outputs
    field = next(iter(step.outputs))
    iv = Intervention(step_id=step_id, patches={field: step.outputs[field]}, source="user",
                      description=f"placebo: {step.agent}.{field} set to its own value")
    exp = run_experiment(defn, trace, step_id, llm, N, M, targets, BASE_SEED, intervention=iv)
    return experiment_row(step_id, exp, kind="placebo")


def study_run(defn: WorkflowDef, llm: LLMProvider, task: dict[str, Any], fault: str | None, model: str) -> dict[str, Any]:
    inp = {k: task[k] for k in ("message", "email", "order_id")}
    t0 = time.time()
    for attempt in (1, 2):  # only infrastructure failures may be re-run (prereg)
        out = run_workflow(defn, inp, llm, fault=make_fault(fault), seed=1)
        infra = out.trace.run.status == "errored" and any(
            k in (s.error or "") for s in out.trace.steps for k in ("unreachable", "too slow", "HTTP 5", "timed out")
        )
        if not infra:
            break
    truth = defn.truth()
    results = evaluate_checks(out.trace, defn.checks, truth)
    findings = derive_findings(out.trace, results)
    row: dict[str, Any] = {
        "order_id": task["order_id"], "fault": fault or "none", "status": out.trace.run.status, "attempts": attempt,
        "error": next((s.error for s in out.trace.steps if s.error), None),
        "findings": [f.check_id for f in findings],
        "failed_checks": [r.check_id for r in results if r.status is CheckStatus.FAIL],
        "final_output": out.trace.run.final_output,
        "ground_truth": None if out.fault is None else dataclasses.asdict(out.fault),
    }
    symptom = symptom_of(results)
    row["detected"] = out.trace.run.status == "completed" and symptom is not None
    if fault is None or not row["detected"]:
        row["seconds"] = round(time.time() - t0, 1)
        return row
    assert symptom is not None and out.fault is not None
    origin = out.fault.target_step
    row["symptom"], row["origin"] = symptom, origin
    targets = [r.check_id for r in results if r.scope == "outcome" and r.status is CheckStatus.FAIL]
    row["llm_judge"] = llm_judge(out.trace, llm, model)
    experiments: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []
    for level, draws in subsets(defn, task["order_id"], fault).items():
        for d, kept in enumerate(draws):
            sub = with_checks(defn, kept)
            res = evaluate_checks(out.trace, sub.checks, truth)
            ranked = [h.step_id for h in attribute(out.trace, res, symptom)]
            inv = investigate(ranked, make_verify(sub, out.trace, llm, targets, experiments), N + M, BUDGET)
            coverage.append({
                "level": level, "draw": d, "kept": kept, "origin_check_kept": any(
                    c.step == origin for c in sub.checks if c.scope == "step"),
                "ranking": ranked,
                "answers": {
                    "last_agent": symptom,
                    "earliest_check": earliest_check(out.trace, res, symptom),
                    "granite_rank": ranked[0] if ranked else None,
                    "granite_verified": inv.confirmed_step or (ranked[0] if ranked else None),
                },
                "investigation": inv.model_dump(mode="json"),
                "origin_patchable": plan_intervention(sub, out.trace, origin, res) is not None,
            })
    row["coverage"] = coverage
    row["experiments"] = experiments
    p = placebo_step(out.trace, symptom, origin)
    row["placebo"] = None if p is None else placebo(defn, out.trace, p, llm, targets)
    row["seconds"] = round(time.time() - t0, 1)
    return row


# ---- metrics ---------------------------------------------------------------------------------------------------------


def rate(k: int, n: int) -> dict[str, Any]:
    lo, hi = wilson(k, n) if n else (0.0, 1.0)
    return {"k": k, "n": n, "rate": round(k / n, 3) if n else None, "ci95": [round(lo, 3), round(hi, 3)]}


def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    clean = [r for r in rows if r["fault"] == "none"]
    faulty = [r for r in rows if r["fault"] != "none"]
    detected = [r for r in faulty if r["detected"]]
    out: dict[str, Any] = {
        "runs_completed": rate(sum(r["status"] == "completed" for r in rows), len(rows)),
        "detection": rate(len(detected), len(faulty)),
        "detection_by_fault": {f: rate(sum(r["detected"] for r in faulty if r["fault"] == f),
                                       sum(1 for r in faulty if r["fault"] == f)) for f in FAULTS},
        "clean_runs_with_finding": rate(sum(bool(r["findings"]) for r in clean), len(clean)),
    }
    methods = ["last_agent", "earliest_check", "granite_rank", "granite_verified"]
    top1: dict[str, dict[str, Any]] = {}
    for level in LEVELS:
        cells = [(r, c) for r in detected for c in r["coverage"] if c["level"] == level]
        top1[level] = {m: rate(sum(c["answers"][m] == r["origin"] for r, c in cells), len(cells)) for m in methods}
        top1[level]["by_fault"] = {
            f: {m: rate(sum(c["answers"][m] == r["origin"] for r, c in cells if r["fault"] == f),
                        sum(1 for r, _ in cells if r["fault"] == f)) for m in methods} for f in FAULTS
        }
    out["top1"] = top1
    out["llm_judge_top1"] = rate(sum(r["llm_judge"]["answer"] == r["origin"] for r in detected), len(detected))
    full = [c for r in detected for c in r["coverage"] if c["level"] == "100"]
    out["replays_per_investigation_full"] = round(sum(c["investigation"]["replays_used"] for c in full) / len(full), 2) \
        if full else None
    plac = [r["placebo"] for r in detected if r.get("placebo")]
    origin_exps = [e for r in detected for e in r["experiments"] if e["step_id"] == r["origin"]]
    out["nondeterminism"] = {
        "placebo_vr1_confirms": rate(sum(p["verdict"] == Verdict.CONFIRMED.value for p in plac), len(plac)),
        "placebo_single_replay_confirms": rate(sum(p["single_replay_confirms"] for p in plac), len(plac)),
        "origin_vr1_confirms": rate(sum(e["verdict"] == Verdict.CONFIRMED.value for e in origin_exps), len(origin_exps)),
        "origin_single_replay_confirms": rate(sum(e["single_replay_confirms"] for e in origin_exps), len(origin_exps)),
    }
    return out


def markdown(meta: dict[str, Any], rows: list[dict[str, Any]], m: dict[str, Any]) -> str:
    def cell(x: dict[str, Any]) -> str:
        if not x["n"]:
            return "n/a"
        return f"{x['k']}/{x['n']} ({x['rate']:.0%}, {x['ci95'][0]:.0%}-{x['ci95'][1]:.0%})"

    lines = [
        f"# Benchmark v0, Refund Desk ({meta['date']})", "",
        (f"Protocol: `research/eval/prereg-v2.md` (SHA-256 `{meta['prereg_sha256'][:16]}`). Model {meta['model']}. "
         f"HEAD `{meta['git_head'][:10]}`, working tree dirty: {meta['git_dirty']}. Mode: {meta['mode']}."), "",
        "| Metric | Result |", "|---|---|",
        f"| Runs completed | {cell(m['runs_completed'])} |",
        f"| Faulty runs detected | {cell(m['detection'])} |",
        *[f"| Detected, {f} | {cell(x)} |" for f, x in m["detection_by_fault"].items()],
        f"| Clean runs with a finding | {cell(m['clean_runs_with_finding'])} |",
        f"| LLM judge top-1 (full information) | {cell(m['llm_judge_top1'])} |",
        f"| Replays per investigation, full coverage | {m['replays_per_investigation_full']} |", "",
        "## Top-1 attribution by step-check coverage", "",
        "| Method | 100% | 60% | 40% |", "|---|---|---|---|",
    ]
    for meth in ["last_agent", "earliest_check", "granite_rank", "granite_verified"]:
        lines.append(f"| {meth} | " + " | ".join(cell(m["top1"][lv][meth]) for lv in LEVELS) + " |")
    nd = m["nondeterminism"]
    lines += [
        "", "## Nondeterminism: confirmations by VR-1 and by a single replay", "",
        "| Case | VR-1 confirms | Single replay confirms |", "|---|---|---|",
        (f"| Placebo on an innocent step (should be 0) | {cell(nd['placebo_vr1_confirms'])} | "
         f"{cell(nd['placebo_single_replay_confirms'])} |"),
        f"| True origin | {cell(nd['origin_vr1_confirms'])} | {cell(nd['origin_single_replay_confirms'])} |",
        "", "## Per run", "", "| Order | Fault | Status | Detected | Origin | Rank top-1 (100%) | Verified (100%) | Judge |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        full = next((c for c in r.get("coverage", []) if c["level"] == "100"), None)
        lines.append(
            f"| {r['order_id']} | {r['fault']} | {r['status']} | {r['detected']} | {r.get('origin', '')} | "
            f"{full['answers']['granite_rank'] if full else ''} | {full['answers']['granite_verified'] if full else ''} | "
            f"{(r.get('llm_judge') or {}).get('answer', '')} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--tasks", type=int, default=10)
    ap.add_argument("--offline", action="store_true", help="use only saved answers (no model needed)")
    args = ap.parse_args()
    store = default_store()
    defn = build_workflow(store, args.model)
    cassette = Cassette(ROOT / "data" / "cassettes" / "refund_desk_v1.json")
    llm: LLMProvider = RecordedProvider(cassette) if args.offline else RecordingProvider(
        OllamaProvider(timeout=240.0), cassette, reuse=True)
    tasks = [t for t in store.example_tasks(12) if "(delivered)" in t["label"]][: args.tasks]
    out_json = HERE / "results" / f"{DATE}_benchmark-v0{'-offline' if args.offline else ''}.json"
    state = json.loads(out_json.read_text("utf-8")) if out_json.exists() else {"rows": []}
    done = {(r["order_id"], r["fault"]) for r in state["rows"]}
    meta = {"date": DATE, "model": args.model, "mode": "recorded" if args.offline else "live",
            "prereg_sha256": sha256_file(HERE / "prereg-v2.md"), "git_head": git("rev-parse", "HEAD"),
            "git_dirty": bool(git("status", "--porcelain")), "source_sha256": source_hashes(), "n_tasks": len(tasks),
            "faults": FAULTS, "levels": LEVELS, "draws": DRAWS, "n": N, "m": M, "budget": BUDGET}
    t0 = time.time()
    for task in tasks:
        for fault in [None, *FAULTS]:
            if (task["order_id"], fault or "none") in done:
                continue
            row = study_run(defn, llm, task, fault, args.model)
            state["rows"].append(row)
            state.update(meta=meta, metrics=metrics(state["rows"]))
            out_json.write_text(json.dumps(state, indent=1, default=str), "utf-8")
            full = next((c for c in row.get("coverage", []) if c["level"] == "100"), None)
            print(f"[{time.time() - t0:6.0f}s] {task['order_id']} {row['fault']:13} {row['status']:9} "
                  f"detected={row['detected']} rank={full['answers']['granite_rank'] if full else '-'} "
                  f"verified={full['answers']['granite_verified'] if full else '-'} ({row['seconds']}s)", flush=True)
    state["metrics"] = metrics(state["rows"])
    out_json.write_text(json.dumps(state, indent=1, default=str), "utf-8")
    out_json.with_suffix(".md").write_text(markdown(meta, state["rows"], state["metrics"]), "utf-8")
    print(json.dumps(state["metrics"], indent=1))


if __name__ == "__main__":
    main()
