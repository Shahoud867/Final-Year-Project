"""Structure design: domain model (class diagram) and structure chart."""

from __future__ import annotations

import dataclasses
from typing import Any

from granite_api import models as db_models
from granite_core import attribution, checks, evidence, experiment, runner, trace, verification

from . import Sheet
from .kit import Diagram


def _has(cls: Any, *names: str) -> None:
    """Fail the build if a field shown in the diagram no longer exists on the class."""
    if hasattr(cls, "model_fields"):
        known = set(cls.model_fields)
    elif dataclasses.is_dataclass(cls):
        known = {f.name for f in dataclasses.fields(cls)}
    else:
        known = {c.name for c in cls.__table__.columns}
    missing = [n for n in names if n not in known]
    if missing:
        raise SystemExit(f"domain model is out of date: {cls.__name__} has no field(s) {missing}")


def domain_model() -> Sheet:
    _has(runner.WorkflowDef, "key", "title", "steps", "checks", "repairs", "truth", "data_snapshot")
    _has(runner.StepDef, "step_id", "agent", "name", "kind", "reads", "fn")
    _has(trace.Step, "step_id", "agent", "kind", "inputs", "outputs", "reads", "model", "params", "prompt_hash", "error",
         "started_at", "ended_at")
    _has(trace.TraceV1, "schema_version", "run", "steps")
    _has(trace.RunInfo, "status", "task_input", "final_output")
    _has(runner.FaultRecord, "fault_type", "target_step", "field_path", "original_value", "injected_value", "note")
    _has(checks.CheckDef, "id", "name", "type", "scope", "step", "expression", "tolerance", "severity", "version")
    _has(checks.CheckResult, "check_id", "check_version", "scope", "step", "type", "severity", "status", "observed",
         "expected", "computation")
    _has(checks.FindingSpec, "kind", "severity", "title", "detail", "check_id", "symptom_step")
    _has(attribution.HypothesisSpec, "rank", "step_id", "agent", "method", "evidence_kind", "score", "rationale")
    _has(experiment.ExperimentRun, "intervention", "summary", "replays")
    _has(experiment.ReplayRecord, "kind", "index", "seed", "completed", "trace", "results", "judgement")
    _has(verification.ExperimentSummary, "rule_version", "k_pass", "n_completed", "c_pass", "m_completed", "ci_low",
         "ci_high", "verdict", "explanation")
    _has(verification.Intervention, "step_id", "patches", "source", "description")
    _has(verification.RepairRule, "field", "expression")
    _has(evidence.EvidenceRecord, "type", "payload", "sha256", "reproduce")
    _has(db_models.Review, "reviewer", "decision", "comment", "from_status", "to_status", "created_at")
    _has(db_models.Finding, "status")

    d = Diagram("domain-model", "Domain model (class diagram)", 1550, 930,
                "The concepts of an investigation and how they relate, from workflow definition to review.")
    c, w = [30, 340, 650, 960, 1270], 250
    r1, r2, r3, r4 = 70, 310, 560, 800
    wf = d.compartments("WorkflowDef", c[0], r1, w, "WorkflowDef",
                        ["key, title: str", "steps: list[StepDef]", "checks: list[CheckDef]",
                         "repairs: dict[step, RepairRule[]]", "truth(): source-of-truth funcs", "data_snapshot: str"],
                        "workflow", tip="granite_core.runner.WorkflowDef; built by refund_desk.build_workflow")
    sd = d.compartments("StepDef", c[1], r1, w, "StepDef",
                        ["step_id, agent, name: str", "kind: llm|tool|code|handoff", "reads: list['step.field']",
                         "fn(StepContext) -> outputs"], "workflow", tip="granite_core.runner.StepDef")
    st = d.compartments("Step", c[2], r1, w, "Step",
                        ["step_id, agent, kind", "inputs: dict  (resolved reads)", "outputs: dict", "reads: list[str]",
                         "model, params, prompt_hash", "error: str | None", "started_at, ended_at"],
                        "core", tip="granite_core.trace.Step: one recorded agent action")
    tr = d.compartments("TraceV1", c[3], r1, w, "TraceV1",
                        ["schema_version: granite.trace/v1", "run: RunInfo", "  status: completed|errored",
                         "  task_input, final_output", "steps: list[Step]  (max 500)"], "core",
                        tip="granite_core.trace.TraceV1; JSON Schema in packages/granite_core/schema")
    fr = d.compartments("FaultRecord", c[4], r1, w, "FaultRecord",
                        ["fault_type, target_step", "field_path", "original_value, injected_value", "note"],
                        "warn", tip="granite_core.runner.FaultRecord: ground truth of an injected fault")
    cd = d.compartments("CheckDef", c[0], r2, w, "CheckDef",
                        ["id, name: str", "type: assert|truth|policy|...", "scope: outcome|step", "step: str",
                         "expression: str  (DSL)", "tolerance, severity, version"], "workflow")
    cr = d.compartments("CheckResult", c[1], r2, w, "CheckResult",
                        ["check_id, check_version", "scope, step, type, severity", "status: PASS|FAIL|ABSTAIN|ERROR",
                         "observed, expected", "computation: dict"], "core")
    rr = d.compartments("ReplayRecord", c[3], r2, w, "ReplayRecord",
                        ["kind: intervention|control", "index, seed: int", "completed: bool", "trace: TraceV1",
                         "results: list[CheckResult]", "judgement: ReplayJudgement"], "core")
    es = d.compartments("ExperimentSummary", c[4], r2, w, "ExperimentSummary",
                        ["rule_version: VR-1", "k_pass / n_completed", "c_pass / m_completed",
                         "ci_low, ci_high  (Wilson 95%)", "verdict: CONFIRMED|REFUTED|", "  INCONCLUSIVE|ERROR",
                         "explanation: str"], "core")
    fi = d.compartments("Finding", c[1], r3, w, "Finding",
                        ["kind: silent_failure|", "      explicit_error", "severity, title, detail",
                         "check_id: str | None", "symptom_step: str", "status: FindingStatus (11)"], "core",
                        tip="core FindingSpec plus the stored lifecycle status (table findings)")
    hy = d.compartments("Hypothesis", c[2], r3, w, "Hypothesis",
                        ["rank: int  (1..5)", "step_id, agent", "method: provenance|structural", "evidence_kind: str",
                         "score: float", "rationale: str"], "core", tip="granite_core.attribution.HypothesisSpec")
    ex = d.compartments("Experiment", c[3], r3, w, "Experiment",
                        ["n, m: int  (replays, controls)", "intervention: Intervention", "summary: ExperimentSummary",
                         "replays: list[ReplayRecord]"], "core", tip="granite_core.experiment.ExperimentRun")
    iv = d.compartments("Intervention", c[4], r3, w, "Intervention",
                        ["step_id: str", "patches: dict[field, value]", "source: truth|contract|user",
                         "description: str"], "core")
    ev = d.compartments("EvidenceRecord", c[1], r4, w, "EvidenceRecord",
                        ["type: EvidenceType (9 kinds)", "payload: dict", "sha256: str  (canonical JSON)",
                         "reproduce: str"], "core")
    rv = d.compartments("Review", c[2], r4, w, "Review",
                        ["reviewer, decision, comment", "from_status, to_status", "created_at"], "api",
                        tip="granite_api.models.Review: a human decision on a finding")
    rp = d.compartments("RepairRule", c[4], r4, w, "RepairRule", ["field: str", "expression: str  (DSL)"], "workflow")

    # composition and association
    d.edge([wf.right(0.3), sd.left(0.4)], "1..*", "WorkflowDef", "StepDef", start="diamond", end="", label_dy=-6)
    d.edge([wf.bottom(), cd.top()], src="WorkflowDef", dst="CheckDef", start="diamond", end="")
    d.label(wf.cx + 12, 268, "checks  *", anchor="start")
    d.edge([sd.right(0.4), st.left(0.34)], "runs as", "StepDef", "Step", dashed=True, end="open", label_dy=-6)
    d.edge([tr.left(0.42), st.right(0.34)], "1..500", "TraceV1", "Step", start="diamond", end="", label_dy=-6)
    d.edge([tr.right(0.42), fr.left(0.42)], "0..1", "TraceV1", "FaultRecord", dashed=True, end="", label_dy=-6)
    d.edge([cd.right(0.45), cr.left(0.45)], "yields", "CheckDef", "CheckResult", end="open", label_dy=-6)
    d.edge([cr.bottom(), fi.top()], src="CheckResult", dst="Finding", end="open")
    d.label(cr.cx + 12, 505, "a failed outcome check opens", anchor="start")
    d.edge([fi.right(0.45), hy.left(0.45)], "1..5", "Finding", "Hypothesis", start="diamond", end="", label_dy=-6)
    d.edge([hy.top(), st.bottom()], src="Hypothesis", dst="Step", end="open")
    d.label(hy.cx + 12, 400, "blames (step_id)", anchor="start")
    d.edge([hy.right(0.45), ex.left(0.58)], "0..*", "Hypothesis", "Experiment", end="open", label_dy=-6)
    d.edge([ex.top(0.35), rr.bottom(0.35)], src="Experiment", dst="ReplayRecord", start="diamond", end="")
    d.label(ex.x + w * 0.35 - 12, 512, "N + M", anchor="end")
    d.edge([rr.top(0.5), tr.bottom(0.5)], src="ReplayRecord", dst="TraceV1", end="open")
    d.label(rr.cx + 12, 258, "has its own trace", anchor="start")
    d.edge([ex.top(0.85), (ex.x + w * 0.85, 514), (es.cx, 514), es.bottom()], src="Experiment", dst="ExperimentSummary",
           start="diamond", end="")
    d.edge([ex.right(0.58), iv.left(0.58)], "1", "Experiment", "Intervention", start="diamond", end="", label_dy=-6)
    d.edge([rp.top(), iv.bottom()], src="RepairRule", dst="Intervention", dashed=True, end="open")
    d.label(rp.cx + 12, 740, "evaluated to build", anchor="start")
    d.edge([fi.bottom(0.5), ev.top(0.5)], src="Finding", dst="EvidenceRecord", end="open")
    d.label(fi.cx - 12, 755, "supported by  *", anchor="end")
    d.edge([fi.bottom(0.82), (fi.x + w * 0.82, 748), (rv.cx, 748), rv.top()], "decided in  *", "Finding", "Review",
           end="open", label_at=(680, 742))
    d.note(c[4], 196, w, ["Ground truth, kept apart", "Recorded beside the trace for scoring.", "attribute() never receives it (a test",
                          "checks its signature)."], "warn", id="fault-note")
    d.legend(30, 560, [("workflow", "defined by a workflow"), ("core", "produced by granite_core"),
                       ("api", "stored by the API only"), ("warn", "evaluation ground truth"),
                       ("line:solid", "association (filled diamond = owns)"), ("line:dashed", "derived from / may exist")],
             col_w=262)
    return Sheet(
        d, "Structure", "Domain Model / Class Diagram",
        "Read it left to right. A workflow definition (yellow) declares steps, the reads between them, checks and "
        "repair rules. Running it produces a TraceV1 made of recorded Steps. Evaluating a CheckDef on a trace "
        "yields a CheckResult; a failed outcome check opens a Finding. Attribution attaches up to five ranked "
        "Hypotheses to the finding, each blaming one recorded step. An Experiment verifies one hypothesis: an "
        "Intervention (built from a RepairRule) patches that step, N+M ReplayRecords each carry their own trace, "
        "and the ExperimentSummary holds the VR-1 verdict. EvidenceRecords and Reviews hang off the finding. The "
        "FaultRecord is deliberately off to the side: it exists only to score the analysis.",
        ["packages/granite_core/granite_core/runner.py", "packages/granite_core/granite_core/trace.py",
         "packages/granite_core/granite_core/checks.py", "packages/granite_core/granite_core/attribution.py",
         "packages/granite_core/granite_core/verification.py", "packages/granite_core/granite_core/experiment.py",
         "packages/granite_core/granite_core/evidence.py", "apps/api/granite_api/models.py"],
        "Every field name shown is checked against the real class when the pack is built; a renamed or removed "
        "field fails the build. Relationships and layout are curated.",
    )


def structure_chart() -> Sheet:
    d = Diagram("structure-chart", "Structure chart", 1490, 640,
                "Functional decomposition of an investigation into modules, with the data passed down and up.")
    root = d.node("root", 545, 40, 400, 56, "Investigate a workflow run", ["granite_api.routes (HTTP entry points)"], "api")
    cols = [30, 320, 610, 900, 1190]
    level1 = [
        ("m-run", "1  Execute run", "services/runs.py: run_job", "api", "↓ task, fault, seed, mode", "↑ RunOutcome (trace)"),
        ("m-ana", "2  Analyse run", "services/analysis.py: persist_outcome", "api", "↓ trace, workflow checks", "↑ findings, hypotheses"),
        ("m-ver", "3  Verify hypothesis", "services/experiments.py: experiment_job", "api", "↓ trace, step, N, M", "↑ verdict, replays"),
        ("m-rev", "4  Review finding", "services/reviews.py: apply_review", "api", "↓ decision, comment", "↑ new status"),
        ("m-rep", "5  Report", "services/report.py: finding_report", "api", "↓ finding id", "↑ Markdown or JSON"),
    ]
    children = {
        "m-run": [("validate task", "registry.validate_task", "api"), ("choose model source", "llm_factory.build_provider", "api"),
                  ("run workflow", "runner.run_workflow", "core"), ("record steps and reads", "runner._execute_steps", "core")],
        "m-ana": [("evaluate checks", "checks.evaluate_checks → dsl", "core"), ("open findings", "checks.derive_findings", "core"),
                  ("rank origins", "attribution.attribute", "core"), ("hash evidence", "evidence.make_evidence", "core")],
        "m-ver": [("build the fix", "verification.build_intervention", "core"), ("plan the replay", "verification.plan_replay", "core"),
                  ("replay and judge", "experiment.run_experiment", "core"), ("decide the verdict", "verification.decide (VR-1)", "core")],
        "m-rev": [("check comment rule", "reviews.apply_review", "api"), ("change status", "lifecycle.transition", "core"),
                  ("write audit and note", "common.audit · add_evidence", "api")],
        "m-rep": [("collect records", "models: Finding, Evidence", "api"), ("render", "report.finding_report", "api")],
    }
    bus_y = 130
    d.edge([root.bottom(), (root.cx, bus_y)], src="root", dst="bus", end="")
    for x, (mid, title, where, kind, down, up) in zip(cols, level1, strict=True):
        m = d.node(mid, x, 196, 270, 60, title, [where], kind)
        d.edge([(root.cx, bus_y), (m.cx, bus_y), m.top()], src="root", dst=mid, end="")
        d.label(m.cx + 8, 158, down, anchor="start", size=10.5)
        d.label(m.cx + 8, 174, up, anchor="start", size=10.5)
        trunk_x = x + 18
        kids = children[mid]
        for i, (name, fn, k) in enumerate(kids):
            ky = 290 + i * 78
            kid = d.node(f"{mid}-{i}", x + 44, ky, 226, 58, name, [fn], k)
            d.edge([(trunk_x, m.y + 60 if i == 0 else 290 + (i - 1) * 78 + 29), (trunk_x, kid.cy), kid.left()],
                   src=mid, dst=kid.id, end="")
    d.legend(1190, 470, [("api", "application module"), ("core", "granite_core module")], title="Module belongs to", col_w=200)
    d.note(1190, 548, 270, ["Reading the chart", "Lines mean 'calls'. ↓ is data passed down,", "↑ is data returned. Order is left to right."],
           "plain", id="reading")
    return Sheet(
        d, "Structure", "Structure Chart",
        "The chart shows who calls whom at module level and what travels on each call. The API entry points do no "
        "work themselves: they hand a run to module 1, whose result (a trace) is the only input module 2 needs. "
        "Verification (module 3) starts again from the stored trace, not from the run, which is what makes a "
        "replay possible days later. Modules 1 to 3 each end in a call into granite_core (blue): the application "
        "modules only add validation, persistence and state changes around them.",
        ["apps/api/granite_api/services/runs.py", "apps/api/granite_api/services/analysis.py",
         "apps/api/granite_api/services/experiments.py", "apps/api/granite_api/services/reviews.py",
         "apps/api/granite_api/services/report.py"],
        "Curated; the function names are the real ones and are cross-checked by the generated call graph.",
    )
