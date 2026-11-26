"""Refund Desk workflow definition: steps and their declared reads, checks, and repair rules."""

from __future__ import annotations

from granite_core.checks import CheckDef
from granite_core.runner import StepDef, WorkflowDef
from granite_core.verification import RepairRule

from . import steps
from .store import RetailStore, default_store

DEFAULT_MODEL = "llama3.2:3b"
WORKFLOW_KEY = "refund_desk"

CHECKS: list[CheckDef] = [
    CheckDef(
        id="CHK-OUT-1", name="Stated refund equals the catalogue total of the refunded items", type="truth",
        scope="outcome", step="s5", severity="high",
        expression="approx(number_in(s5.message), truth.catalog_total(pluck(s3.items_to_refund, 'item_id')))",
        description="The amount the customer is told must equal the sum of catalogue prices of the items refunded.",
    ),
    CheckDef(
        id="CHK-OUT-2", name="Refund decision follows policy (delivered order owned by the customer)", type="policy",
        scope="outcome", step="s3", severity="critical",
        expression="s3.eligible == truth.refund_allowed(task.order_id, task.email)",
        description="Only a delivered order that belongs to the identified customer may be refunded.",
    ),
    CheckDef(
        id="CHK-OUT-3", name="Every item the customer asked about is in the refund decision", type="truth",
        scope="outcome", step="s3", severity="high",
        expression=(
            "not s3.eligible or len(s3.items_to_refund) == len(truth.requested_items(task.order_id, task.message))"
        ),
        description="An eligible refund must cover each order item the customer's message names.",
    ),
    # Version 2 of the step checks (2026-11-15): each compares an output field with the value it should have, so a
    # failed check also says what to patch in for a replay (ADR-011). Version 1 compared totals only.
    CheckDef(
        id="CT-INTAKE", name="Intake kept the order id and the items the customer named", type="truth", scope="step",
        step="s1", severity="medium", version=2,
        expression=(
            "s1.order_id == task.order_id"
            " and s1.item_names == truth.requested_items(task.order_id, task.message, s1.item_names)"
        ),
    ),
    CheckDef(
        id="CT-LOOKUP", name="Lookup prices match the catalogue", type="truth", scope="step", step="s2",
        severity="high", version=2, expression="s2.items == truth.catalog_items(s2.items)",
    ),
    CheckDef(
        id="CT-POLICY", name="Refunded items carry the prices the lookup reported", type="assert", scope="step",
        step="s3", severity="medium", expression="truth.same_prices(s3.items_to_refund, s2.items)",
    ),
    CheckDef(
        id="CT-CALC", name="Refund equals the sum of the prices the calculator received", type="assert",
        scope="step", step="s4", severity="high",
        expression="approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))",
    ),
    CheckDef(
        id="CT-WRITER", name="Message states the computed refund", type="assert", scope="step", step="s5",
        severity="high", expression="approx(number_in(s5.message), s4.refund_amount)",
    ),
]

# Hand-written repair rules. Empty since 2026-11-15: every intervention is now derived from the failed check
# (granite_core.interventions, ADR-011). The mechanism stays for workflows whose checks cannot say the correct value.
REPAIRS: dict[str, list[RepairRule]] = {}


def build_workflow(store: RetailStore | None = None, model: str = DEFAULT_MODEL) -> WorkflowDef:
    """Assemble the Refund Desk: five steps with their reads, seven checks and the repair rules."""
    store = store or default_store()
    step_defs = [
        StepDef("s1", "Intake", "llm", "extract order and items", ["task.message"], steps.intake(model)),
        StepDef("s2", "Order Lookup", "tool", "get_order_details", ["s1.order_id"], steps.order_lookup(store)),
        StepDef(
            "s3", "Policy", "code", "decide eligibility",
            ["s2.status", "s2.user_id", "s2.items", "s2.payment_method", "s1.item_names", "task.email"],
            steps.policy(store),
        ),
        StepDef("s4", "Refund Calculator", "llm", "compute refund", ["s3.items_to_refund"], steps.calculator(model)),
        StepDef(
            "s5", "Writer", "llm", "write customer message",
            ["s4.refund_amount", "s3.refund_method", "s3.eligible", "s3.reason"], steps.writer(model),
        ),
    ]
    return WorkflowDef(
        key=WORKFLOW_KEY, title="Refund Desk", steps=step_defs, checks=[c.model_copy() for c in CHECKS],
        repairs=REPAIRS, truth=store.truth_functions,
        description="Customer-support refund requests on synthetic tau-bench retail data.",
        data_snapshot=store.version,
    )
