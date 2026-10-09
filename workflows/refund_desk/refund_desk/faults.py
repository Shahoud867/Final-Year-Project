"""Fault operators for Refund Desk. Faults are rule-based and deterministic: no LLM is involved."""

from __future__ import annotations

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


FAULT_TYPES: dict[str, type[StalePriceFault]] = {"stale_price": StalePriceFault}


def make_fault(name: str | None) -> Fault | None:
    if not name or name == "none":
        return None
    if name not in FAULT_TYPES:
        raise ValueError(f"unknown fault '{name}'; available: {', '.join(sorted(FAULT_TYPES))}")
    return FAULT_TYPES[name]()
