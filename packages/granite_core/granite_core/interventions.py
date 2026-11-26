"""Check-derived interventions: the correct value for a replay comes from the check that failed (ADR-011).

A step check that compares one of the step's own output fields with something it can compute, for example::

    s2.items == truth.catalog_items(s2.items)          (a source of truth)
    approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))   (the step's own contract)

already says what the field *should* have been. When such a check fails, the other side of the comparison is the
value to patch in for a replay. No per-step repair rule has to be written by hand: a workflow author writes
checks, and verification follows from them.

What is recognised, and nothing else (the rest of the check language is not invertible):

* ``<path> == <expr>`` or ``<expr> == <path>``;
* ``approx(<path>, <expr>)`` or ``approx(<expr>, <path>)``;
* either of the above as one conjunct of an ``and``: only the conjuncts that are false are patched, so a patch
  stays atomic (Spike 8 lesson).

``<path>`` must be a direct output field of the step under test (``s2.items``), never a nested value or another
step's field. Anything else gives no intervention, and the caller falls back to the workflow's repair rules or
reports that the step cannot be verified automatically.
"""

from __future__ import annotations

import ast
from collections.abc import Callable, Mapping
from typing import Any

from .checks import CheckDef, CheckResult, CheckStatus
from .dsl import DSLError, compile_expression
from .trace import TraceV1
from .verification import Intervention


def _field_of(node: ast.AST, step_id: str) -> str | None:
    """``s2.items`` -> ``items`` when the node is a direct output field of ``step_id``; otherwise None."""
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == step_id:
        return node.attr
    return None


def _pairs(node: ast.AST) -> list[tuple[ast.AST, ast.AST, ast.AST]]:
    """(conjunct, left, right) for every equality or approx() at the top level or inside a top-level ``and``."""
    parts = node.values if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And) else [node]
    out: list[tuple[ast.AST, ast.AST, ast.AST]] = []
    for part in parts:
        if (
            isinstance(part, ast.Compare)
            and len(part.ops) == 1
            and isinstance(part.ops[0], ast.Eq)
            and len(part.comparators) == 1
        ):
            out.append((part, part.left, part.comparators[0]))
        elif isinstance(part, ast.Call) and isinstance(part.func, ast.Name) and part.func.id == "approx":
            if len(part.args) >= 2:
                out.append((part, part.args[0], part.args[1]))
    return out


def derive_intervention(
    trace: TraceV1,
    step_id: str,
    checks: list[CheckDef],
    results: list[CheckResult],
    truth: Mapping[str, Callable[..., Any]] | None = None,
) -> Intervention | None:
    """Patch ``step_id`` with the values its failed checks expect; ``None`` when no failed check says what they are."""
    step = trace.step(step_id)
    if step is None:
        return None
    by_id = {c.id: c for c in checks}
    failed = [r for r in results if r.step == step_id and r.status is CheckStatus.FAIL and r.check_id in by_id]
    ctx = trace.context()
    patches: dict[str, Any] = {}
    sources: list[str] = []
    for result in failed:
        check = by_id[result.check_id]
        try:
            tree = ast.parse(check.expression, mode="eval").body
        except SyntaxError:
            continue
        for conjunct, left, right in _pairs(tree):
            field, other = _field_of(left, step_id), right
            if field is None:
                field, other = _field_of(right, step_id), left
            if field is None or field in patches or field not in step.outputs:
                continue
            try:
                holds = compile_expression(ast.unparse(conjunct)).evaluate(ctx, truth, check.tolerance).value
                if holds is True:
                    continue  # this part of the check is satisfied: nothing to correct
                value = compile_expression(ast.unparse(other)).evaluate(ctx, truth, check.tolerance).value
            except DSLError:
                continue
            patches[field] = value
            if check.id not in sources:
                sources.append(check.id)
    if not patches:
        return None
    names = ", ".join(patches)
    return Intervention(
        step_id=step_id,
        patches=patches,
        source="check",
        derived_from=sources,
        description=f"Set {step.agent}.{names} to the value check {', '.join(sources)} expects",
    )


__all__ = ["derive_intervention"]
