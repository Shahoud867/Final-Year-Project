"""Regression export: turn a confirmed finding into a test that fails until its cause is fixed (FR-EXP-01, F17).

A *case* holds what is needed to re-check the failure without Granite's database: the workflow and task that failed,
the seed and model, the outcome checks that failed, the confirmed origin and the intervention that fixed it, and the
recorded trace of the failing run. The exported pytest file does two things:

* ``test_recorded_failure_is_still_caught`` re-evaluates the checks on the stored failing trace. It protects the
  checks: if someone weakens a check so that it no longer catches this failure, the test fails.
* ``test_outcome_is_correct_now`` runs the workflow on the same task and asserts that the failed checks now pass.
  While the cause is still present it fails; once the cause is fixed it passes. For a fault that Granite injected,
  ``GRANITE_REGRESSION_FAULT=<fault>`` puts the fault back to show the test failing.

Model answers come from the recording by default (``GRANITE_CASSETTE``), so the test runs in CI without a model.
"""

from __future__ import annotations

import importlib
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from .checks import CheckResult, evaluate_checks
from .llm import Cassette, LLMProvider, RecordedProvider
from .runner import WorkflowDef, run_workflow
from .trace import TraceV1

CASE_FORMAT: Literal["granite.regression/v1"] = "granite.regression/v1"


class RegressionCase(BaseModel):
    """Everything a regression test needs, written once from a confirmed finding."""

    model_config = ConfigDict(extra="forbid")

    format: Literal["granite.regression/v1"] = CASE_FORMAT
    finding_id: str
    title: str
    workflow: str
    workflow_module: str
    model: str
    seed: int
    task_input: dict[str, Any]
    target_checks: list[str]
    origin_step: str
    origin_agent: str
    intervention: dict[str, Any]
    verdict: dict[str, Any]
    trace_sha256: str
    failing_trace: dict[str, Any]


def safe_name(finding_id: str) -> str:
    """A file-name stem from a finding id (letters, digits and underscores only)."""
    return "".join(ch if ch.isalnum() else "_" for ch in finding_id)


def load_workflow(case: RegressionCase) -> tuple[WorkflowDef, Any]:
    """Import the workflow package named in the case and build it with the case's model."""
    module = importlib.import_module(case.workflow_module)
    build: Callable[..., WorkflowDef] = module.build_workflow
    return build(model=case.model), module


def default_provider() -> LLMProvider:
    """Recorded answers from ``GRANITE_CASSETTE`` (the repository's cassette by default)."""
    path = os.environ.get("GRANITE_CASSETTE")
    if not path:
        here = Path(__file__).resolve()
        candidates = [p / "data" / "cassettes" / "refund_desk_v1.json" for p in here.parents]
        path = str(next((c for c in candidates if c.exists()), candidates[0]))
    return RecordedProvider(Cassette(path))


def evaluate_case(case: RegressionCase, trace: dict[str, Any] | TraceV1) -> list[CheckResult]:
    """The case's target checks evaluated on a trace."""
    defn, _ = load_workflow(case)
    parsed = trace if isinstance(trace, TraceV1) else TraceV1.model_validate(trace)
    checks = [c for c in defn.checks if c.id in case.target_checks]
    return evaluate_checks(parsed, checks, defn.truth())


def run_case(case: RegressionCase, llm: LLMProvider | None = None, fault: str | None = None) -> list[CheckResult]:
    """Run the workflow on the case's task and evaluate the case's target checks on the new trace.

    ``fault`` (or the ``GRANITE_REGRESSION_FAULT`` variable) re-injects a fault the workflow package defines.
    """
    defn, module = load_workflow(case)
    name = fault if fault is not None else os.environ.get("GRANITE_REGRESSION_FAULT") or None
    make_fault = getattr(module, "make_fault", None)
    injected = make_fault(name) if (name and make_fault) else None
    outcome = run_workflow(defn, case.task_input, llm or default_provider(), fault=injected, seed=case.seed)
    if outcome.trace.run.status != "completed":
        err = next((s.error for s in outcome.trace.steps if s.error), "unknown error")
        raise AssertionError(f"the workflow did not complete: {err}")
    checks = [c for c in defn.checks if c.id in case.target_checks]
    return evaluate_checks(outcome.trace, checks, defn.truth())


def _docsafe(text: str) -> str:
    """Text that cannot end or break the generated module's docstring."""
    return text.replace("\\", "/").replace('"""', "'''").replace("\n", " ")[:200]


def render_pytest(case: RegressionCase) -> str:
    """The pytest module exported next to ``<stem>.json``."""
    patches = ", ".join(f"{k}" for k in case.intervention.get("patches", {}))
    return f'''"""Regression test exported by Granite from finding {case.finding_id}.

Failure: {_docsafe(case.title)}
Confirmed origin: {case.origin_agent} ({case.origin_step}); replaying with {patches} corrected fixed the outcome
({case.verdict.get("k_pass")}/{case.verdict.get("n_planned")} with the fix, {case.verdict.get("c_pass")}/\
{case.verdict.get("m_planned")} without, rule {case.verdict.get("rule_version")}).

Run:  pytest {safe_name("test_granite_" + case.finding_id)}.py
Show it failing while the cause is present:  GRANITE_REGRESSION_FAULT=<fault> pytest ...
Model answers come from GRANITE_CASSETTE (the repository's recording by default).
"""

from pathlib import Path

from granite_core.checks import CheckStatus
from granite_core.regression import RegressionCase, evaluate_case, run_case

CASE = RegressionCase.model_validate_json(Path(__file__).with_suffix(".json").read_text(encoding="utf-8"))


def test_recorded_failure_is_still_caught() -> None:
    """The stored failing run must still fail its checks: this guards the checks themselves."""
    results = evaluate_case(CASE, CASE.failing_trace)
    assert any(r.status is CheckStatus.FAIL for r in results), "the checks no longer catch the recorded failure"


def test_outcome_is_correct_now() -> None:
    """Run the workflow on the task that failed: the failed checks must now pass."""
    results = run_case(CASE)
    failing = [f"{{r.check_id}}: {{r.message}}" for r in results if r.status is not CheckStatus.PASS]
    assert not failing, "still failing: " + "; ".join(failing)
'''


__all__ = [
    "CASE_FORMAT", "RegressionCase", "default_provider", "evaluate_case", "load_workflow", "render_pytest",
    "run_case", "safe_name",
]
