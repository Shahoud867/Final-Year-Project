# -*- coding: utf-8 -*-
"""
Granite proposal-defense PoC backend.

Serves REAL data from the 8 committed proposal-stage spikes
(dev/spikes/poc/*.json) through a small REST API the frontend consumes.
No diagnosis result, accuracy number, or repair outcome here is
fabricated -- see data_loader.py's module docstring for the one honest
data discrepancy this build surfaced and how it's handled.

Run: uvicorn main:app --reload --port 8000
"""
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from data_loader import load_all

app = FastAPI(title="Granite POC Demo API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

RUNS, FINDINGS = load_all()
RUNS_BY_ID = {r["id"]: r for r in RUNS}


def _spike_meta():
    return [
        {"id": "spike1", "name": "Spike 1 -- ErrorProbe Reproduction", "n_cases": 8,
          "result": (
              f"agent {FINDINGS['spike1_multirun']['agent_accuracy']['min']*100:.0f}-{FINDINGS['spike1_multirun']['agent_accuracy']['max']*100:.0f}% "
              f"/ step {FINDINGS['spike1_multirun']['step_accuracy']['min']*100:.0f}-{FINDINGS['spike1_multirun']['step_accuracy']['max']*100:.0f}% "
              f"(5 runs, means {FINDINGS['spike1_multirun']['agent_accuracy']['mean']*100:.0f}%/{FINDINGS['spike1_multirun']['step_accuracy']['mean']*100:.0f}%)"
          ) if FINDINGS.get("spike1_multirun") else f"agent {FINDINGS['spike1_agent_accuracy']*100:.0f}%"},
        {"id": "spike2", "name": "Spike 2 -- CrewAI Instrumentation", "n_cases": 1, "result": "Clean 3-node / 2-edge trace"},
        {"id": "spike3", "name": "Spike 3 -- Fault Injection v1", "n_cases": 1, "result": "Self-corrected by the agent (kept as a finding)"},
        {"id": "spike3b", "name": "Spike 3b -- Fault Injection v2", "n_cases": 1, "result": "Unambiguous blind propagation"},
        {"id": "spike4", "name": "Spike 4 -- Semantic Error Diagnostic", "n_cases": 3,
          "result": f"{FINDINGS['spike4_summary']['n_caught_by_rule_based_detector']}/{FINDINGS['spike4_summary']['n_true_silent_failure_cases']} on natural failures observed (n=3, none occurred)"},
        {"id": "spike5", "name": "Spike 5 -- Controlled Counterfactual Replay", "n_cases": 1, "result": "97.2 -> 108.0 recovered"},
        {"id": "spike6", "name": "Spike 6 -- Cyclic Graph Handling", "n_cases": 2, "result": "Bound proven load-bearing by control run"},
        {"id": "spike7", "name": "Spike 7 -- Preventive Classifier", "n_cases": FINDINGS["spike7_preventive_classifier"]["n_test"],
          "result": f"Honest negative: P/R/F1 = {FINDINGS['spike7_preventive_classifier']['precision']}"},
        {"id": "spike8", "name": "Spike 8 -- Repair Agent", "n_cases": 6,
          "result": f"repair_success_rate = {FINDINGS['spike8_summary']['repair_success_rate']}"},
    ]


@app.get("/api/stats")
def get_stats():
    s1 = FINDINGS["spike1_summary"]
    s4 = FINDINGS["spike4_summary"]
    s8 = FINDINGS["spike8_summary"]
    multirun = FINDINGS.get("spike1_multirun")
    return {
        # Headline reproduction numbers now come from the 5-run aggregate,
        # not a single run's snapshot -- see poc_spike1_multirun_summary.json.
        "agent_accuracy_mean": multirun["agent_accuracy"]["mean"] if multirun else FINDINGS["spike1_agent_accuracy"],
        "agent_accuracy_min": multirun["agent_accuracy"]["min"] if multirun else None,
        "agent_accuracy_max": multirun["agent_accuracy"]["max"] if multirun else None,
        "step_accuracy_mean": multirun["step_accuracy"]["mean"] if multirun else FINDINGS["spike1_step_accuracy_type_safe"],
        "step_accuracy_min": multirun["step_accuracy"]["min"] if multirun else None,
        "step_accuracy_max": multirun["step_accuracy"]["max"] if multirun else None,
        "n_reproduction_runs": multirun["n_runs_completed"] if multirun else 1,
        "reproduction_bug_fixed": True,
        "reproduction_bug_note": (
            "poc_spike1_errorprobe_repro.py's step-index comparison originally compared a string "
            "ground-truth step against an int predicted step, silently scoring numeric matches as wrong. "
            "Fixed 2026-08-26, then re-run 5 independent times because the first bug-free run differed "
            "materially from the old cached number -- real LLM sampling variance at n=8, not a bug."
        ),
        # kept for backward compatibility with any caller still reading the old single-run fields
        "agent_accuracy": FINDINGS["spike1_agent_accuracy"],
        "step_accuracy_raw": FINDINGS["spike1_step_accuracy_raw"],
        "step_accuracy_type_safe": FINDINGS["spike1_step_accuracy_type_safe"],
        "step_accuracy_discrepancy_flag": False,
        "n_reproduction_cases": s1["n_cases"],
        "sed_natural_failures_observed": s4["n_true_silent_failure_cases"],
        "sed_note": s4["note"],
        "recovery_rate_n": 1,
        "recovery_success": True,
        "repair_success_rate": s8["repair_success_rate"],
        "repair_exact_match_rate": s8["exact_match_rate"],
        "repair_n_cases": s8["n_cases"],
        "cyclic_cases_bounded": 2,
        "cyclic_cases_total": 2,
        "preventive_classifier": FINDINGS["spike7_preventive_classifier"],
        "total_runs": len(RUNS),
        "n_spikes": 8,
        "spikes": _spike_meta(),
    }


@app.get("/api/runs")
def list_runs(status: Optional[str] = None, spike: Optional[str] = None, q: Optional[str] = None):
    out = RUNS
    if status:
        out = [r for r in out if r["status"] == status]
    if spike:
        out = [r for r in out if r["spike"].lower().replace(" ", "") == spike.lower().replace(" ", "")]
    if q:
        ql = q.lower()
        out = [r for r in out if ql in r["question"].lower() or ql in r["scenario"].lower()]
    # summary shape for the table -- omit heavy graph payload
    return [
        {
            "id": r["id"], "spike": r["spike"], "scenario": r["scenario"], "framework": r["framework"],
            "question": r["question"], "status": r["status"],
            "confidence": (r["attribution"] or {}).get("confidence"),
            "has_fault": r["fault"] is not None,
            "has_repair": r["repair"] is not None,
            "has_sed": r["sed"] is not None,
            "has_classifier": r.get("classifier") is not None,
        }
        for r in out
    ]


@app.get("/api/runs/{run_id}")
def get_run(run_id: str):
    run = RUNS_BY_ID.get(run_id)
    if not run:
        raise HTTPException(404, f"No run with id '{run_id}'")
    return run


@app.get("/")
def root():
    return {"service": "Granite POC Demo API", "runs": len(RUNS), "docs": "/docs"}
