"""Checks engine: executable rules over a trace (FR-CHK-01..06).

A check is a small expression (see :mod:`granite_core.dsl`) with a *scope*:

* ``outcome``: a property the run's end result must satisfy (e.g. the stated refund equals the
  catalogue total). A failed outcome check on a run that *completed* without error is a silent failure.
* ``step``: a *contract* of one step (e.g. the Calculator's refund equals the sum of the prices it
  received). Step contracts are the evidence attribution uses to tell the origin of a wrong value
  from a step that merely passed it on faithfully.

Every result carries its own computation (expression, values actually read, truth-source queries,
tolerance), so anyone can re-evaluate it from stored data and obtain the same answer.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .dsl import DSLError, DSLRuntimeError, DSLSyntaxError, MissingFieldError, compile_expression
from .trace import TraceV1

Severity = Literal["critical", "high", "medium", "low"]
CheckType = Literal["assert", "truth", "policy", "schema", "answer_key"]
Scope = Literal["outcome", "step"]
SEVERITY_ORDER: dict[str, int] = {"low": 0, "medium": 1, "high": 2, "critical": 3}


class CheckStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    ABSTAIN = "abstain"  # the data needed to decide is not there; never counted as a pass
    ERROR = "error"  # the check itself could not be evaluated; never counted as a pass


class CheckDef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
    name: str
    type: CheckType = "assert"
    scope: Scope
    step: str = Field(description="step the check is about: the symptom step for outcome checks")
    expression: str
    tolerance: float = Field(default=0.01, ge=0, le=1e6)
    severity: Severity = "high"
    enabled: bool = True
    version: int = Field(default=1, ge=1)
    description: str = ""


class CheckResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    check_id: str
    check_version: int
    scope: Scope
    step: str
    type: CheckType
    severity: Severity
    status: CheckStatus
    observed: Any = None
    expected: Any = None
    message: str = ""
    computation: dict[str, Any] = Field(default_factory=dict)


def validate_expression(expression: str) -> None:
    """Raise :class:`DSLSyntaxError` if the expression is not allowed (used at save time)."""
    compile_expression(expression)


def evaluate_check(
    check: CheckDef,
    trace: TraceV1,
    truth: Mapping[str, Callable[..., Any]] | None = None,
) -> CheckResult:
    base = {
        "check_id": check.id,
        "check_version": check.version,
        "scope": check.scope,
        "step": check.step,
        "type": check.type,
        "severity": check.severity,
    }
    comp: dict[str, Any] = {"expression": check.expression, "tolerance": check.tolerance}
    if trace.step(check.step) is None:
        return CheckResult(
            **base,
            status=CheckStatus.ABSTAIN,
            computation=comp,
            message=f"step '{check.step}' is not in this trace",
        )
    try:
        expr = compile_expression(check.expression)
        out = expr.evaluate(trace.context(), truth, check.tolerance)
    except MissingFieldError as e:
        return CheckResult(**base, status=CheckStatus.ABSTAIN, computation=comp, message=str(e))
    except DSLSyntaxError as e:
        return CheckResult(**base, status=CheckStatus.ERROR, computation=comp, message=f"invalid check: {e}")
    except DSLRuntimeError as e:
        return CheckResult(**base, status=CheckStatus.ERROR, computation=comp, message=str(e))
    except DSLError as e:  # pragma: no cover - future subclasses
        return CheckResult(**base, status=CheckStatus.ERROR, computation=comp, message=str(e))
    comp.update(value=out.value, resolved=out.resolved, truth_calls=out.truth_calls, operands=out.operands)
    if not isinstance(out.value, bool):
        return CheckResult(
            **base,
            status=CheckStatus.ERROR,
            computation=comp,
            message="a check expression must evaluate to true or false",
        )
    observed = expected = None
    if out.operands:
        observed, expected = out.operands[0], out.operands[1]
    status = CheckStatus.PASS if out.value else CheckStatus.FAIL
    msg = check.name if status is CheckStatus.PASS else f"{check.name}: observed {observed!r}, expected {expected!r}"
    return CheckResult(**base, status=status, observed=observed, expected=expected, message=msg, computation=comp)


def evaluate_checks(
    trace: TraceV1,
    checks: list[CheckDef],
    truth: Mapping[str, Callable[..., Any]] | None = None,
) -> list[CheckResult]:
    return [evaluate_check(c, trace, truth) for c in checks if c.enabled]


class FindingSpec(BaseModel):
    """What the engine decides to open a finding about (persisted by the application layer)."""

    kind: Literal["silent_failure", "explicit_error"]
    severity: Severity
    title: str
    check_id: str | None
    symptom_step: str
    detail: str = ""


def derive_findings(trace: TraceV1, results: list[CheckResult]) -> list[FindingSpec]:
    """FR-CHK-04: failed outcome checks open findings; a completed run makes them *silent* failures."""
    failing = [r for r in results if r.scope == "outcome" and r.status is CheckStatus.FAIL]
    specs: list[FindingSpec] = []
    kind: Literal["silent_failure", "explicit_error"] = (
        "silent_failure" if trace.run.status == "completed" else "explicit_error"
    )
    for r in failing:
        specs.append(
            FindingSpec(
                kind=kind,
                severity=r.severity,
                title=r.message[:140],
                check_id=r.check_id,
                symptom_step=r.step,
                detail=r.message,
            )
        )
    if trace.run.status == "errored" and not failing:
        bad = next((s for s in trace.steps if s.error), None)
        specs.append(
            FindingSpec(
                kind="explicit_error",
                severity="high",
                title=f"Run errored at {bad.agent if bad else 'unknown step'}",
                check_id=None,
                symptom_step=bad.step_id if bad else (trace.steps[-1].step_id if trace.steps else ""),
                detail=(bad.error or "") if bad else "",
            )
        )
    return specs
