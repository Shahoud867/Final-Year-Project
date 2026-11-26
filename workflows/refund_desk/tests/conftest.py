"""A deterministic stand-in for the language model that reads the three Refund Desk prompts."""

from __future__ import annotations

import json
import re

import pytest
from granite_core.llm import Completion, LLMRequest, ProviderUnavailable

from refund_desk import build_workflow, default_store


class FakeModel:
    """Behaves like a competent model unless told otherwise. Flags reproduce the slips a small model makes."""

    name = "fake"

    def __init__(self, calc_slip: float = 0.0, message_slip: bool = False, intake_reply: str | None = None,
                 fail_after: int | None = None) -> None:
        self.calc_slip, self.message_slip, self.intake_reply = calc_slip, message_slip, intake_reply
        self.fail_after, self.calls = fail_after, 0

    def complete(self, request: LLMRequest) -> Completion:
        self.calls += 1
        if self.fail_after is not None and self.calls > self.fail_after:
            raise ProviderUnavailable("endpoint unreachable")
        system, user = request.messages[0]["content"], request.messages[-1]["content"]
        if system.startswith("You extract"):
            text = self.intake_reply if self.intake_reply is not None else self._intake(user)
        elif system.startswith("You are a refund calculator"):
            text = self._calc(user)
        else:
            text = self._write(user)
        return Completion(text=text, model=request.model, provider="fake", tokens_in=5, tokens_out=5)

    @staticmethod
    def _intake(message: str) -> str:
        order = re.search(r"#W\d+", message)
        names = re.search(r"return the (.+?) from order", message)
        items = re.split(r" and the ", names.group(1)) if names else []
        return json.dumps({"order_id": order.group(0) if order else "", "item_names": items})

    def _calc(self, user: str) -> str:
        prices = [float(p) for p in re.findall(r": ([0-9.]+)$", user, re.M)]
        return json.dumps({"prices_used": prices, "refund_amount": round(sum(prices) + self.calc_slip, 2)})

    def _write(self, user: str) -> str:
        amount = re.search(r"[$]([0-9.]+)", user)
        if amount:
            shown = float(amount.group(1)) + (0.5 if self.message_slip else 0.0)
            return f"Your refund of ${shown:.2f} will be returned to your original payment method."
        reason = re.search(r"Reason: (.*)", user)
        return f"We are sorry, we cannot refund this order because {reason.group(1) if reason else 'of policy'}."


@pytest.fixture(scope="session")
def store():
    return default_store()


@pytest.fixture(scope="session")
def defn(store):
    return build_workflow(store)


@pytest.fixture(scope="session")
def tasks(store):
    return store.example_tasks(12)


@pytest.fixture
def task(tasks):
    """First delivered-order example: ready-to-run task input."""
    t = next(t for t in tasks if "(delivered)" in t["label"])
    return {k: t[k] for k in ("message", "email", "order_id")}
