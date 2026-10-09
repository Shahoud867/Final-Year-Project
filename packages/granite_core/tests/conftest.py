"""Shared fixtures: a small refund-style trace built by hand (no LLM), with a tiny source of truth."""

from __future__ import annotations

import copy
from typing import Any

import pytest

from granite_core.checks import CheckDef
from granite_core.trace import RunInfo, Step, TraceV1

CATALOGUE = {"i1": 19.75, "i2": 23.50, "i3": 5.00}


def catalog_price(item_id: str) -> float:
    return CATALOGUE[item_id]


def catalog_total(item_ids: list[str]) -> float:
    return round(sum(CATALOGUE[i] for i in item_ids), 2)


def fix_prices(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{**it, "price": CATALOGUE[it["item_id"]]} for it in items]


TRUTH = {"catalog_price": catalog_price, "catalog_total": catalog_total, "fix_prices": fix_prices}

CHECKS = [
    CheckDef(
        id="CHK-OUT-1",
        name="Stated refund equals catalogue total",
        type="truth",
        scope="outcome",
        step="s5",
        expression="approx(number_in(s5.message), truth.catalog_total(pluck(s3.items_to_refund, 'item_id')))",
        severity="high",
    ),
    CheckDef(
        id="CT-LOOKUP",
        name="Lookup prices match catalogue",
        type="truth",
        scope="step",
        step="s2",
        expression="approx(sum(pluck(s2.items, 'price')), truth.catalog_total(pluck(s2.items, 'item_id')))",
        tolerance=0.005,
    ),
    CheckDef(
        id="CT-CALC",
        name="Refund equals sum of received prices",
        type="assert",
        scope="step",
        step="s4",
        expression="approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))",
    ),
    CheckDef(
        id="CT-WRITER",
        name="Message states the computed refund",
        type="assert",
        scope="step",
        step="s5",
        expression="approx(number_in(s5.message), s4.refund_amount)",
    ),
]


def make_trace(
    stale: bool = False,
    calc_slip: bool = False,
    message_slip: bool = False,
    agent_prefix: str = "",
    extra_step: bool = False,
    scale: float = 1.0,
) -> TraceV1:
    """Five steps: Intake -> Lookup -> Policy -> Calculator -> Writer. Two items are refunded."""
    price1 = round((CATALOGUE["i1"] - (0.25 if stale else 0.0)) * scale, 2)
    price2 = round(CATALOGUE["i2"] * scale, 2)
    refund = round(price1 + price2 + (1.0 if calc_slip else 0.0), 2)
    shown = round(refund + (2.0 if message_slip else 0.0), 2)
    items = [
        {"item_id": "i1", "price": price1},
        {"item_id": "i2", "price": price2},
        {"item_id": "i3", "price": 5.0},
    ]
    refunded = [{"item_id": "i1", "price": price1}, {"item_id": "i2", "price": price2}]
    steps = [
        Step(
            step_id="s1",
            agent=agent_prefix + "Intake",
            kind="llm",
            reads=["task.message"],
            inputs={"task.message": "return the lamp and the mug"},
            outputs={"item_names": ["lamp", "mug"]},
        ),
        Step(
            step_id="s2",
            agent=agent_prefix + "OrderLookup",
            kind="tool",
            reads=["s1.item_names"],
            inputs={"s1.item_names": ["lamp", "mug"]},
            outputs={"items": items, "status": "delivered"},
        ),
        Step(
            step_id="s3",
            agent=agent_prefix + "Policy",
            kind="code",
            reads=["s2.items", "s1.item_names"],
            inputs={"s2.items": copy.deepcopy(items), "s1.item_names": ["lamp", "mug"]},
            outputs={"items_to_refund": refunded, "eligible": True},
        ),
        Step(
            step_id="s4",
            agent=agent_prefix + "RefundCalculator",
            kind="llm",
            reads=["s3.items_to_refund"],
            inputs={"s3.items_to_refund": copy.deepcopy(refunded)},
            outputs={"refund_amount": refund},
        ),
        Step(
            step_id="s5",
            agent=agent_prefix + "Writer",
            kind="llm",
            reads=["s4.refund_amount"],
            inputs={"s4.refund_amount": refund},
            outputs={"message": f"Your refund of ${shown:.2f} is on its way."},
        ),
    ]
    if extra_step:  # an irrelevant step that reads nothing and is read by nothing
        steps.insert(1, Step(step_id="x1", agent="Logger", kind="code", outputs={"note": "hello"}))
    return TraceV1(
        run=RunInfo(
            workflow="refund_desk",
            status="completed",
            task_input={"message": "return the lamp and the mug"},
            final_output=steps[-1].outputs,
        ),
        steps=steps,
    )


@pytest.fixture
def truth() -> dict[str, Any]:
    return dict(TRUTH)


@pytest.fixture
def checks() -> list[CheckDef]:
    return [c.model_copy() for c in CHECKS]
