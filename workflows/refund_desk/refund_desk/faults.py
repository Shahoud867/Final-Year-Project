"""Fault operators for Refund Desk. Faults are rule-based and deterministic: no LLM is involved.

Three types, one per place a silent failure can enter a multi-agent workflow:

==============  ======  =======================================================================================
fault           step    what goes wrong
==============  ======  =======================================================================================
stale_price     s2      a tool returns outdated data (Order Lookup reports an old price)
dropped_item    s1      an agent loses part of the request (Intake keeps one item name, drops the other)
handoff_drift   s4      a value is damaged in transit (Refund Calculator receives a price Policy never sent)
==============  ======  =======================================================================================

Each run still completes without an error. The ground truth is returned as a :class:`FaultRecord` and is never shown
to detection or attribution.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any

from granite_core.runner import Fault, FaultRecord

from .steps import _norm


@dataclass
class StalePriceFault:
    """FLT-STALE: the order-lookup tool returns an outdated price for one of the requested items.

    No error is raised anywhere; every later step behaves correctly on the bad input. That is what makes it
    a *silent* failure: the run completes with a fluent message that is simply wrong.
    """

    delta: float = 0.25
    fault_type: str = "stale_price"
    target_step: str = "s2"

    def apply(self, outputs: dict[str, Any], inputs: dict[str, Any]) -> tuple[dict[str, Any], FaultRecord]:
        """Lower the price of a requested item in the lookup result; return the fault record."""
        items = [dict(it) for it in outputs["items"]]
        wanted = {_norm(n) for n in inputs.get("s1.item_names", [])}
        idx = next((i for i, it in enumerate(items) if _norm(it["name"]) in wanted), 0)
        original = items[idx]["price"]
        items[idx]["price"] = round(max(original - self.delta, 0.01), 2)
        return {**outputs, "items": items}, FaultRecord(
            fault_type=self.fault_type, target_step=self.target_step, field_path=f"items[{idx}].price",
            original_value=original, injected_value=items[idx]["price"],
            note="the lookup tool returned an outdated cached price; no error was raised",
        )


@dataclass
class DroppedItemFault:
    """FLT-DROP: Intake keeps only the first item the customer named; the rest of the request is lost.

    Every later step is correct on what it is given, and the customer is told a correct refund for the wrong set of
    items. When the customer named a single item there is nothing to drop and the run is unaffected.
    """

    fault_type: str = "dropped_item"
    target_step: str = "s1"

    def apply(self, outputs: dict[str, Any], inputs: dict[str, Any]) -> tuple[dict[str, Any], FaultRecord]:
        """Keep the first item name and drop the others; return the fault record."""
        names = list(outputs.get("item_names", []))
        kept = names[:1]
        return {**outputs, "item_names": kept}, FaultRecord(
            fault_type=self.fault_type, target_step=self.target_step, field_path="item_names",
            original_value=names, injected_value=kept,
            note="Intake lost part of the request; no error was raised",
        )


@dataclass
class HandoffDriftFault:
    """FLT-HANDOFF: the item list Policy sends to the Refund Calculator arrives with one price changed.

    Policy's own output is correct; only the copy the Calculator receives is damaged (an input-stage fault). The
    Calculator then adds up the wrong price faithfully.
    """

    delta: float = 5.0
    fault_type: str = "handoff_drift"
    target_step: str = "s4"
    stage: str = "input"

    def apply(self, outputs: dict[str, Any], inputs: dict[str, Any]) -> tuple[dict[str, Any], FaultRecord]:
        """Raise the first item's price in what the Calculator receives (``outputs`` here is its resolved input)."""
        out = copy.deepcopy(outputs)
        items = out.get("s3.items_to_refund") or []
        if not items:  # nothing is handed over when the request is not eligible
            return out, FaultRecord(
                fault_type=self.fault_type, target_step=self.target_step, field_path="inputs.s3.items_to_refund",
                original_value=[], injected_value=[], note="nothing was handed over, so nothing could drift",
            )
        original = items[0]["price"]
        items[0]["price"] = round(original + self.delta, 2)
        return out, FaultRecord(
            fault_type=self.fault_type, target_step=self.target_step,
            field_path="inputs.s3.items_to_refund[0].price", original_value=original, injected_value=items[0]["price"],
            note="the item list was changed between Policy and the Refund Calculator; no error was raised",
        )


FAULT_TYPES: dict[str, type[StalePriceFault] | type[DroppedItemFault] | type[HandoffDriftFault]] = {
    "stale_price": StalePriceFault,
    "dropped_item": DroppedItemFault,
    "handoff_drift": HandoffDriftFault,
}


def make_fault(name: str | None) -> Fault | None:
    """Create a fault by name; None or 'none' means a clean run."""
    if not name or name == "none":
        return None
    if name not in FAULT_TYPES:
        raise ValueError(f"unknown fault '{name}'; available: {', '.join(sorted(FAULT_TYPES))}")
    return FAULT_TYPES[name]()
