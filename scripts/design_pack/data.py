"""Database design: ER diagram and data dictionary, both generated from the real tables and models."""

from __future__ import annotations

from typing import Any, get_args

from granite_api import (
    models,  # noqa: F401  (registers the tables)
    schemas,
)
from granite_api.db import Base
from granite_api.registry import RefundTask
from granite_core import checks, evidence, lifecycle, trace, verification

from . import Sheet
from .kit import Diagram

# table.column -> meaning. The build fails if a column has no entry here or an entry has no column.
MEANING: dict[str, str] = {
    "projects.id": "`prj_` plus the workflow key",
    "projects.name": "Display name",
    "projects.workflow_key": "Which registered workflow the project runs",
    "projects.description": "Free text",
    "projects.created_at": "Creation time (UTC)",
    "runs.id": "`run_` plus 12 hex characters",
    "runs.project_id": "Project the run belongs to",
    "runs.workflow_key": "Workflow that was executed",
    "runs.status": "`queued`, `running`, `completed` or `errored`",
    "runs.llm_mode": "What actually answered: `live` or `recorded`",
    "runs.model": "Model name, for example `llama3.2:3b`",
    "runs.seed": "Random seed passed to the model",
    "runs.fault_type": "Name of the injected fault; null for a clean run",
    "runs.task_input": "The validated task as submitted (kept as submitted because replays need it)",
    "runs.trace": "Granite Trace v1 document of the run: the single source for hashing and replay",
    "runs.trace_sha256": "SHA-256 of the trace document",
    "runs.error": "Why the run stopped; empty if it completed",
    "runs.created_at": "When the run was requested",
    "runs.finished_at": "When execution and analysis ended",
    "fault_injections.run_id": "Run the fault was injected into; also the primary key, so at most one per run",
    "fault_injections.fault_type": "For example `stale_price`",
    "fault_injections.target_step": "Step whose output was changed",
    "fault_injections.field_path": "Which output field, for example `items[0].price`",
    "fault_injections.original_value": "Value before the fault",
    "fault_injections.injected_value": "Value after the fault",
    "fault_injections.note": "Plain-language description; ground truth used only to score the analysis",
    "check_results.id": "Sequence number",
    "check_results.run_id": "Run the check was evaluated on",
    "check_results.check_id": "Check identifier, for example `CHK-OUT-1`",
    "check_results.check_version": "Version of the check definition",
    "check_results.scope": "`outcome` (final result) or `step` (one step's contract)",
    "check_results.step": "Step the check is attached to",
    "check_results.type": "`assert`, `truth`, `policy`, `schema` or `answer_key`",
    "check_results.severity": "`critical`, `high`, `medium` or `low`",
    "check_results.status": "`pass`, `fail`, `abstain` (data missing) or `error` (check could not run)",
    "check_results.observed": "Value found in the run",
    "check_results.expected": "Value it should have had",
    "check_results.message": "One-line explanation shown to the user",
    "check_results.computation": "Expression, resolved operands and source-of-truth calls, kept for reproduction",
    "findings.id": "`fnd_` plus 12 hex characters",
    "findings.run_id": "Run in which the problem was found",
    "findings.kind": "`silent_failure` (run completed, outcome wrong) or `explicit_error` (run stopped)",
    "findings.severity": "Severity of the failed check",
    "findings.title": "Short statement of what is wrong",
    "findings.detail": "Full message with observed and expected values",
    "findings.check_id": "Outcome check that failed; null for an explicit error",
    "findings.symptom_step": "Step where the problem became visible",
    "findings.status": "One of the 11 lifecycle states (see the state machine)",
    "findings.created_at": "When the finding was opened",
    "findings.updated_at": "Last status change",
    "hypotheses.id": "`hyp_` plus 12 hex characters",
    "hypotheses.finding_id": "Finding it tries to explain",
    "hypotheses.rank": "1 is the most likely origin; at most 5 per finding",
    "hypotheses.step_id": "Step blamed",
    "hypotheses.agent": "Name of that step's agent",
    "hypotheses.method": "`provenance` (evidence on the data path) or `structural` (fallback)",
    "hypotheses.evidence_kind": "Strongest evidence on the step: `truth_mismatch`, `contract_fail`, `handoff_drift`, `unknown`, `consistent`",
    "hypotheses.score": "Evidence weight multiplied by 0.9 for every hop from the symptom",
    "hypotheses.rationale": "Sentence shown to the user",
    "hypotheses.evidence": "Supporting facts as JSON",
    "hypotheses.status": "`open`, `confirmed`, `refuted`, `inconclusive` or `error`",
    "experiments.id": "`exp_` plus 12 hex characters",
    "experiments.hypothesis_id": "Hypothesis being verified",
    "experiments.finding_id": "Finding it belongs to (repeated for quick lookup)",
    "experiments.status": "`queued`, `running`, `done` or `error`",
    "experiments.llm_mode": "`live` or `recorded`",
    "experiments.n": "Replays with the fix applied (1 to 10)",
    "experiments.m": "Control replays without it (0 to 5)",
    "experiments.base_seed": "Replay i uses base_seed + i; control j uses base_seed + 500 + j",
    "experiments.rule_version": "Verdict rule used: `VR-1`",
    "experiments.intervention": "The patch applied to the suspected step",
    "experiments.summary": "Counts, Wilson interval, verdict and explanation",
    "experiments.verdict": "`confirmed`, `refuted`, `inconclusive` or `error`",
    "experiments.error": "Why the experiment could not run; empty otherwise",
    "experiments.created_at": "When it was requested",
    "experiments.finished_at": "When the verdict was stored",
    "replays.id": "Sequence number",
    "replays.experiment_id": "Experiment the replay belongs to",
    "replays.kind": "`intervention` (fix applied) or `control` (no fix)",
    "replays.idx": "Position within its kind, from 0",
    "replays.seed": "Seed used for this replay",
    "replays.completed": "False if the replay could not finish",
    "replays.passed": "True if every target check passed and nothing regressed; null if unfinished",
    "replays.judgement": "Which checks were fixed, still failing or regressed",
    "replays.results": "Check results of the replay",
    "replays.final_output": "What the replayed workflow answered",
    "evidence.id": "`ev_` plus 12 hex characters",
    "evidence.run_id": "Run it belongs to (reference by id, no constraint)",
    "evidence.finding_id": "Finding it supports, if any (reference by id, no constraint)",
    "evidence.type": "One of nine evidence types, for example `check_computation`",
    "evidence.title": "Short label",
    "evidence.payload": "The evidence itself; written once and never updated",
    "evidence.sha256": "SHA-256 of the canonical JSON of the payload; recomputed on every read to detect tampering",
    "evidence.reproduce": "How to regenerate the evidence",
    "evidence.created_at": "When it was recorded",
    "reviews.id": "`rev_` plus 12 hex characters",
    "reviews.finding_id": "Finding that was reviewed",
    "reviews.reviewer": "Name typed by the reviewer",
    "reviews.decision": "`accept`, `reject`, `resolve`, `wont_fix` or `request_info`",
    "reviews.comment": "Reason; mandatory to reject, close, ask, or accept an inconclusive finding",
    "reviews.from_status": "Finding status before the decision",
    "reviews.to_status": "Finding status after it (unchanged for `request_info`)",
    "reviews.created_at": "When the decision was recorded",
    "jobs.id": "`job_` plus 12 hex characters",
    "jobs.kind": "`run` or `experiment`",
    "jobs.target_id": "Id of the run or experiment being executed",
    "jobs.status": "`queued`, `running`, `succeeded` or `failed`",
    "jobs.progress_done": "Units finished (replays, for an experiment)",
    "jobs.progress_total": "Units planned",
    "jobs.message": "Latest progress text, or the failure reason",
    "jobs.created_at": "When the job was queued",
    "jobs.started_at": "When a worker picked it up",
    "jobs.finished_at": "When it ended",
    "audit_log.id": "Sequence number",
    "audit_log.ts": "When the action happened (UTC)",
    "audit_log.actor": "`system`, `analyst` or the reviewer's name",
    "audit_log.action": "For example `run_created`, `finding_transition`, `experiment_finished`, `review`",
    "audit_log.entity_type": "`run`, `finding` or `experiment`",
    "audit_log.entity_id": "Id of the record concerned",
    "audit_log.detail": "Action-specific facts; for a transition: event, from_status, to_status",
}

TRACE_MEANING: dict[str, str] = {
    "TraceV1.schema_version": "Always `granite.trace/v1`",
    "TraceV1.run": "Facts about the whole run",
    "TraceV1.steps": "Recorded steps in execution order (at most 500)",
    "RunInfo.external_id": "Id given by the caller (the API uses the run id)",
    "RunInfo.workflow": "Workflow key",
    "RunInfo.runtime": "Which runner produced the trace (`granite`)",
    "RunInfo.status": "`completed` or `errored`",
    "RunInfo.task_input": "The task the workflow was given",
    "RunInfo.final_output": "Outputs of the last step; empty if the run errored",
    "RunInfo.started_at": "Start of execution",
    "RunInfo.ended_at": "End of execution",
    "Step.step_id": "Identifier unique within the trace, for example `s2`",
    "Step.agent": "Human-readable name of the agent or tool",
    "Step.kind": "`llm`, `tool`, `code` or `handoff`",
    "Step.name": "What the step does",
    "Step.inputs": "The values the step actually received, keyed by the read that supplied them",
    "Step.outputs": "The values the step produced",
    "Step.reads": "Declared data dependencies, each `step.field` of an earlier step or `task.field`",
    "Step.model": "Model used (llm steps)",
    "Step.params": "Model parameters, token counts and whether the answer was recorded",
    "Step.prompt_hash": "Hash of the request, which is also the key of the recorded answer",
    "Step.error": "Why the step failed; null if it succeeded",
    "Step.started_at": "Start of the step",
    "Step.ended_at": "End of the step",
}

_POS = {
    "projects": (30, 60), "jobs": (30, 250), "audit_log": (30, 520),
    "runs": (340, 60), "fault_injections": (340, 390),
    "check_results": (650, 60), "findings": (650, 370), "reviews": (650, 650),
    "hypotheses": (960, 370), "evidence": (960, 650),
    "experiments": (1270, 370), "replays": (1270, 700),
}


def _columns() -> dict[str, list[Any]]:
    tables = {t.name: list(t.columns) for t in Base.metadata.sorted_tables}
    have = {f"{t}.{c.name}" for t, cols in tables.items() for c in cols}
    if have != set(MEANING):
        raise SystemExit(f"data dictionary is out of date; fix MEANING in design_pack/data.py: {sorted(have ^ set(MEANING))}")
    if set(tables) != set(_POS):
        raise SystemExit(f"ER diagram is out of date; tables changed: {sorted(set(tables) ^ set(_POS))}")
    return tables


def er_diagram() -> Sheet:
    tables = _columns()
    d = Diagram("database-schema", "Database schema (ER diagram)", 1550, 930,
                "The twelve tables, their keys and the relationships between them.")
    boxes = {}
    for name, cols in tables.items():
        rows = []
        for c in cols:
            tag = "PK" if c.primary_key else ("FK" if c.foreign_keys else "  ")
            rows.append(f"{tag} {c.name}: {c.type}{'?' if c.nullable and not c.primary_key else ''}")
        x, y = _POS[name]
        kind = "warn" if name == "fault_injections" else ("store" if name in ("jobs", "audit_log", "projects") else "api")
        boxes[name] = d.compartments(name, x, y, 250, name, rows, kind, tip=f"table {name}: {len(cols)} columns")
    b = boxes
    fks = {(next(iter(c.foreign_keys)).column.table.name, t) for t, cols in tables.items() for c in cols if c.foreign_keys}
    routes = {
        ("projects", "runs"): [b["projects"].right(0.4), (340, b["projects"].y + b["projects"].h * 0.4)],
        ("runs", "check_results"): [(590, 120), (650, 120)],
        ("runs", "fault_injections"): [b["runs"].bottom(), b["fault_injections"].top()],
        ("runs", "findings"): [(590, 290), (620, 290), (620, 420), (650, 420)],
        ("findings", "hypotheses"): [(900, 420), (960, 420)],
        ("findings", "reviews"): [b["findings"].bottom(), b["reviews"].top()],
        ("hypotheses", "experiments"): [(1210, 420), (1270, 420)],
        ("experiments", "replays"): [b["experiments"].bottom(), b["replays"].top()],
    }
    if fks != set(routes):
        raise SystemExit(f"ER diagram is out of date; foreign keys changed: {sorted(fks ^ set(routes))}")
    for (parent, child), pts in routes.items():
        d.edge(pts, src=parent, dst=child, start="one", end="one" if child == "fault_injections" else "many",
               tip=f"one {parent} row, {'at most one' if child == 'fault_injections' else 'many'} {child} rows")
    d.edge([b["evidence"].top(0.2), (1010, 615), (930, 615), (930, 540), (900, 540)], "finding_id", "evidence", "findings",
           dashed=True, end="open", label_at=(970, 609))
    d.edge([b["jobs"].right(0.2), (310, b["jobs"].y + b["jobs"].h * 0.2), (310, 250), (340, 250)], src="jobs", dst="runs",
           dashed=True, end="open", tip="jobs.target_id names a run or an experiment")
    d.legend(960, 60, [("api", "investigation data"), ("store", "housekeeping"), ("warn", "evaluation ground truth"),
                       ("line:solid", "foreign key (bar = one, fork = many)"), ("line:dashed", "reference by id, no constraint")],
             col_w=270)
    d.note(1270, 60, 250, ["Design choices", "The trace of a run is one JSON column", "(runs.trace); steps and edges are derived",
                           "from it on read. evidence and audit_log", "have no update or delete route, and", "refer to other rows by id only, so they",
                           "outlive what they describe.", "? marks a nullable column."], "plain", id="choices")
    return Sheet(
        d, "Data", "Schema Design / ER Diagram",
        "Read it as a chain: a project has runs; a run has check results, at most one injected-fault record, and "
        "findings; a finding has ranked hypotheses and reviews; a hypothesis has experiments; an experiment has "
        "replays. Evidence hangs off findings by id without a foreign key on purpose: evidence and the audit log "
        "are append-only and must survive the rows they describe. The fault record (yellow) is kept in its own "
        "table so that no analysis query can read it by accident. The full column meanings are in the data "
        "dictionary.",
        ["apps/api/granite_api/models.py", "apps/api/granite_api/db.py", "docs/adr/adr-003-persistence-sqlalchemy.md"],
        "Tables, columns, types, nullability, keys and foreign keys are read from the SQLAlchemy metadata when the "
        "pack is built; a new table, column or foreign key fails the build until the drawing and dictionary are updated.",
    )


def _type_text(annotation: Any) -> str:
    text = str(annotation).replace("typing.", "").replace("granite_core.trace.", "").replace("<class '", "").replace("'>", "")
    return text.replace("datetime.datetime", "datetime").replace("NoneType", "None")


def _constraints(info: Any) -> str:
    parts = []
    for meta in info.metadata:
        for attr, label in (("min_length", "min length"), ("max_length", "max length"), ("ge", "at least"), ("le", "at most")):
            value = getattr(meta, attr, None)
            if value is not None:
                parts.append(f"{label} {value}")
    if not info.is_required():
        parts.append(f"default `{info.default!r}`" if info.default is not None else "optional")
    return "; ".join(parts) or "required"


def data_dictionary() -> str:
    tables = _columns()
    out = [
        "# Data dictionary", "",
        "Generated by `python scripts/build_design_pack.py` from the SQLAlchemy tables, the trace models and the "
        "request models. Types, keys, nullability, limits and enumerations are read from the code; the meanings "
        "are maintained in `scripts/design_pack/data.py`, and the build fails if a column has no meaning. Do not "
        "edit by hand.", "",
        "Contents: [stored data](#1-stored-data-12-tables) · [trace document](#2-trace-document-granite-trace-v1) · "
        "[request inputs](#3-request-inputs) · [enumerations](#4-enumerations) · [identifiers and hashes](#5-identifiers-and-hashes)", "",
        "## 1. Stored data (12 tables)", "",
    ]
    for name, cols in tables.items():
        out += [f"### {name}", "", "| Column | Type | Null | Key | Meaning |", "|---|---|---|---|---|"]
        for c in cols:
            key = "PK" if c.primary_key else (f"FK to {next(iter(c.foreign_keys)).column.table.name}" if c.foreign_keys else "")
            null = "yes" if c.nullable and not c.primary_key else "no"
            out.append(f"| `{c.name}` | {c.type} | {null} | {key} | {MEANING[f'{name}.{c.name}']} |")
        out.append("")
    out += ["## 2. Trace document (Granite Trace v1)", "",
            "The JSON document stored in `runs.trace`. JSON Schema: `packages/granite_core/schema/granite-trace-v1.schema.json`.", ""]
    seen = set()
    for cls in (trace.TraceV1, trace.RunInfo, trace.Step):
        out += [f"### {cls.__name__}", "", "| Field | Type | Meaning |", "|---|---|---|"]
        for fname, info in cls.model_fields.items():
            key = f"{cls.__name__}.{fname}"
            seen.add(key)
            if key not in TRACE_MEANING:
                raise SystemExit(f"data dictionary is out of date: no meaning for {key}")
            out.append(f"| `{fname}` | `{_type_text(info.annotation)}` | {TRACE_MEANING[key]} |")
        out.append("")
    if seen != set(TRACE_MEANING):
        raise SystemExit(f"data dictionary is out of date: {sorted(seen ^ set(TRACE_MEANING))}")
    out += ["## 3. Request inputs", "", "Validated by pydantic before anything is stored; unknown keys are refused.", ""]
    for title, cls in (("Task for the Refund Desk (`task_input`)", RefundTask), ("POST /api/runs", schemas.RunCreate),
                       ("POST /api/hypotheses/{id}/experiments", schemas.ExperimentCreate),
                       ("POST /api/findings/{id}/reviews", schemas.ReviewCreate)):
        out += [f"### {title}", "", "| Field | Type | Rule |", "|---|---|---|"]
        for fname, info in cls.model_fields.items():
            extra = {"email": "; must look like name@example.com", "order_id": "; must look like #W1234567"}.get(fname, "") if cls is RefundTask else ""
            out.append(f"| `{fname}` | `{_type_text(info.annotation)}` | {_constraints(info)}{extra} |")
        out.append("")
    out += ["## 4. Enumerations", "", "| Name | Values | Defined in |", "|---|---|---|"]
    enums = [
        ("Finding status", [s.value for s in lifecycle.FindingStatus], "granite_core.lifecycle.FindingStatus"),
        ("Lifecycle event", [e.value for e in lifecycle.Event], "granite_core.lifecycle.Event"),
        ("Check status", [s.value for s in checks.CheckStatus], "granite_core.checks.CheckStatus"),
        ("Verdict", [v.value for v in verification.Verdict], "granite_core.verification.Verdict"),
        ("Evidence type", [t.value for t in evidence.EvidenceType], "granite_core.evidence.EvidenceType"),
        ("Step kind", list(get_args(trace.Step.model_fields["kind"].annotation)), "granite_core.trace.Step.kind"),
        ("Check type", list(get_args(checks.CheckDef.model_fields["type"].annotation)), "granite_core.checks.CheckDef.type"),
        ("Check scope", list(get_args(checks.CheckDef.model_fields["scope"].annotation)), "granite_core.checks.CheckDef.scope"),
        ("Severity", list(get_args(checks.CheckDef.model_fields["severity"].annotation)), "granite_core.checks.CheckDef.severity"),
        ("Intervention source", list(get_args(verification.Intervention.model_fields["source"].annotation)), "granite_core.verification.Intervention.source"),
        ("Review decision", list(get_args(schemas.ReviewCreate.model_fields["decision"].annotation)), "granite_api.schemas.ReviewCreate"),
    ]
    for name, values, where in enums:
        out.append(f"| {name} | {', '.join(f'`{v}`' for v in values)} | `{where}` |")
    out += ["", "## 5. Identifiers and hashes", "",
            "| Item | Format |", "|---|---|",
            "| Record ids | a prefix (`run_`, `fnd_`, `hyp_`, `exp_`, `ev_`, `rev_`, `job_`) and 12 hexadecimal characters from a random UUID |",
            "| Step ids | letters, digits, `_` and `-`; unique within a trace |",
            "| Read reference | `step.field` of an earlier step, or `task.field` |",
            f"| Trace version | `{trace.SCHEMA_VERSION}` |",
            "| Evidence and trace hash | SHA-256 of canonical JSON (sorted keys, no extra whitespace, UTF-8) |",
            "| Recorded answer key | SHA-256 of model, messages, parameters and seed |", ""]
    return "\n".join(out)
