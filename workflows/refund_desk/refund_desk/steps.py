"""The five Refund Desk steps. Each takes a :class:`StepContext` and returns the step's outputs.

    s1 Intake            (LLM)   message -> order id + item names
    s2 Order Lookup      (tool)  order id -> order details (this is where a stale price can enter)
    s3 Policy            (code)  eligibility + which items to refund
    s4 Refund Calculator (LLM)   items + prices -> refund amount
    s5 Writer            (LLM)   amount -> customer message
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from functools import lru_cache
from importlib import resources
from typing import Any

from granite_core.llm import LLMRequest
from granite_core.runner import StepContext, StepFailed

from .store import RetailStore

PROMPT_VERSION = "v1"
StepFn = Callable[[StepContext], dict[str, Any]]
_ORDER_ID = re.compile(r"^#W\d{3,12}$")


@lru_cache(maxsize=8)
def prompt(name: str) -> str:
    """Load a versioned prompt file from the package."""
    path = resources.files("refund_desk") / "prompts" / f"{name}_{PROMPT_VERSION}.md"
    return path.read_text(encoding="utf-8").strip()


def parse_json(text: str) -> dict[str, Any]:
    """Models sometimes wrap JSON in prose or code fences; take the first object, or fail the step."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.S)
        if not m:
            raise StepFailed("the model did not return JSON") from None
        try:
            data = json.loads(m.group(0))
        except json.JSONDecodeError:
            raise StepFailed("the model returned malformed JSON") from None
    if not isinstance(data, dict):
        raise StepFailed("the model returned JSON that is not an object")
    return data


def _norm(name: str) -> str:
    n = re.sub(r"^(the|a|an|my|your)\s+", "", name.strip().lower())
    return n[:-1] if n.endswith("s") and len(n) > 3 else n


def intake(model: str) -> StepFn:
    """Step s1: ask the model to extract the order id and item names from the message."""
    def run(ctx: StepContext) -> dict[str, Any]:
        out = ctx.ask(
            LLMRequest(
                messages=[
                    {"role": "system", "content": prompt("intake")},
                    {"role": "user", "content": str(ctx.inputs["task.message"])},
                ],
                model=model, temperature=0.0, max_tokens=120, json_mode=True,
            )
        )
        data = parse_json(out.text)
        order_id = str(data.get("order_id", "")).strip()
        names = data.get("item_names")
        if not _ORDER_ID.match(order_id):
            raise StepFailed(f"the model did not return a valid order id (got {order_id!r})")
        if not isinstance(names, list) or not names or not all(isinstance(n, str) and n.strip() for n in names):
            raise StepFailed("the model did not return a list of item names")
        return {"order_id": order_id, "item_names": [n.strip() for n in names][:8]}

    return run


def order_lookup(store: RetailStore) -> StepFn:
    """Step s2: read the order from the retail store (a tool call, no model)."""
    def run(ctx: StepContext) -> dict[str, Any]:
        order = store.order(str(ctx.inputs["s1.order_id"]))
        if order is None:
            raise StepFailed(f"order {ctx.inputs['s1.order_id']} not found")
        paid = [p for p in order.get("payment_history", []) if p.get("transaction_type") == "payment"]
        return {
            "order_id": order["order_id"],
            "user_id": order["user_id"],
            "status": order["status"],
            "payment_method": paid[0]["payment_method_id"] if paid else "",
            "items": [{"item_id": i["item_id"], "name": i["name"], "price": float(i["price"])} for i in order["items"]],
        }

    return run


def policy(store: RetailStore) -> StepFn:
    """Step s3: decide eligibility in code and select the items to refund."""
    def run(ctx: StepContext) -> dict[str, Any]:
        inp = ctx.inputs
        try:
            owner_ok = inp["s2.user_id"] == store.user_id_for_email(str(inp["task.email"]))
        except Exception:
            owner_ok = False
        delivered = inp["s2.status"] == "delivered"
        wanted = [_norm(n) for n in inp["s1.item_names"]]
        remaining = list(inp["s2.items"])
        refund: list[dict[str, Any]] = []
        for w in wanted:
            hit = next((it for it in remaining if _norm(it["name"]) == w), None)
            if hit:
                remaining.remove(hit)
                refund.append({"item_id": hit["item_id"], "name": hit["name"], "price": hit["price"]})
        if not owner_ok:
            eligible, reason = False, "the order does not belong to the customer who wrote in"
        elif not delivered:
            eligible, reason = False, f"the order is {inp['s2.status']}, and only delivered orders can be returned"
        elif not refund:
            eligible, reason = False, "none of the requested items is part of this order"
        else:
            eligible, reason = True, "delivered order owned by the customer"
        return {
            "eligible": eligible, "reason": reason, "items_to_refund": refund if eligible else [],
            "refund_method": inp["s2.payment_method"],
        }

    return run


def calculator(model: str) -> StepFn:
    """Step s4: ask the model to add up the prices of the items to refund."""
    def run(ctx: StepContext) -> dict[str, Any]:
        items = ctx.inputs["s3.items_to_refund"]
        if not items:
            return {"prices_used": [], "refund_amount": 0.0}
        lines = "\n".join(f"- {i['name']}: {i['price']}" for i in items)
        out = ctx.ask(
            LLMRequest(
                messages=[
                    {"role": "system", "content": prompt("calculator")},
                    {"role": "user", "content": f"Items to refund:\n{lines}"},
                ],
                model=model, temperature=0.2, max_tokens=120, json_mode=True,
            )
        )
        data = parse_json(out.text)
        used, amount = data.get("prices_used"), data.get("refund_amount")
        if not isinstance(used, list) or not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in used):
            raise StepFailed("the model returned non-numeric prices or amount")
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise StepFailed("the model returned non-numeric prices or amount")
        return {"prices_used": [float(x) for x in used], "refund_amount": round(float(amount), 2)}

    return run


def _method_label(method_id: str) -> str:
    for prefix, label in (("gift_card", "gift card"), ("credit_card", "credit card"), ("paypal", "PayPal")):
        if method_id.startswith(prefix):
            return label
    return "original payment method"


def writer(model: str) -> StepFn:
    """Step s5: ask the model to write the customer message."""
    def run(ctx: StepContext) -> dict[str, Any]:
        inp = ctx.inputs
        if inp["s3.eligible"]:
            body = (
                f"Refund amount: ${float(inp['s4.refund_amount']):.2f}\n"
                f"Payment method: {_method_label(str(inp['s3.refund_method']))}\nRefund possible: yes"
            )
        else:
            body = f"Refund possible: no\nReason: {inp['s3.reason']}"
        out = ctx.ask(
            LLMRequest(
                messages=[{"role": "system", "content": prompt("writer")}, {"role": "user", "content": body}],
                model=model, temperature=0.2, max_tokens=160,
            )
        )
        message = out.text.strip()
        if not message:
            raise StepFailed("the model returned an empty message")
        return {"message": message}

    return run
