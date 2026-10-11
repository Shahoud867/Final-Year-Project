"""Retail data: the Refund Desk's customers/orders and, independently, Granite's source of truth.

Loaded from the licence-attributed snapshot ``data/seed/taubench_retail_v1`` (synthetic tau-bench data).
The workflow's *tool* step reads orders through :meth:`order`; the *checks* call the ``truth_functions``
below, which read the catalogue directly. The two paths are deliberately separate so that a stale or
corrupted tool answer is detectable.
"""

from __future__ import annotations

import json
import os
from collections.abc import Callable
from functools import lru_cache
from pathlib import Path
from typing import Any

from granite_core.dsl import MissingFieldError

SNAPSHOT = "taubench_retail_v1"


def find_seed_dir() -> Path:
    """GRANITE_SEED_DIR, else the nearest ``data/seed`` above this file or the working directory."""
    env = os.environ.get("GRANITE_SEED_DIR")
    if env:
        return Path(env)
    for start in (Path(__file__).resolve(), Path.cwd().resolve()):
        for parent in [start, *start.parents]:
            cand = parent / "data" / "seed"
            if (cand / SNAPSHOT).is_dir():
                return cand
    raise FileNotFoundError(
        f"cannot find data/seed/{SNAPSHOT}; set GRANITE_SEED_DIR (run scripts/build_truth_snapshot.py to create it)"
    )


class RetailStore:
    """Orders, customers and catalogue of the retail snapshot, and the checks' source of truth."""
    def __init__(
        self, orders: dict[str, Any], users: dict[str, Any], products: dict[str, Any], version: str = SNAPSHOT
    ) -> None:
        self.orders, self.users, self.products, self.version = orders, users, products, version
        self._email_to_user = {u["email"].lower(): uid for uid, u in users.items()}
        self._price: dict[str, float] = {}
        for p in products.values():
            for item_id, v in p["variants"].items():
                self._price[item_id] = float(v["price"])

    @classmethod
    def load(cls, seed_dir: Path | None = None) -> RetailStore:
        """Load the snapshot from the seed directory."""
        base = (seed_dir or find_seed_dir()) / SNAPSHOT

        def read(name: str) -> dict[str, Any]:
            with open(base / name, encoding="utf-8") as fh:
                data: dict[str, Any] = json.load(fh)
            return data

        return cls(read("orders.json"), read("users.json"), read("products.json"))

    # ---- what the workflow's tool step may call -----------------------------------------------------
    def order(self, order_id: str) -> dict[str, Any] | None:
        """The order as the workflow's lookup tool sees it, or None."""
        return self.orders.get(order_id)

    # ---- source of truth (called from check expressions as truth.<name>) -----------------------------
    def catalog_price(self, item_id: str) -> float:
        """Catalogue price of an item; an unknown item is reported as a missing field."""
        if item_id not in self._price:
            raise MissingFieldError(f"item '{item_id}' is not in the catalogue")
        return self._price[item_id]

    def catalog_total(self, item_ids: list[str]) -> float:
        """Sum of the catalogue prices of the given items, rounded to cents."""
        return round(sum(self.catalog_price(i) for i in item_ids), 2)

    def fix_prices(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Return the items with their prices replaced by catalogue prices."""
        return [{**it, "price": self.catalog_price(it["item_id"])} for it in items]

    def user_id_for_email(self, email: str) -> str:
        """Customer id for an e-mail address (case-insensitive)."""
        uid = self._email_to_user.get(str(email).lower())
        if uid is None:
            raise MissingFieldError("no customer has this e-mail address")
        return uid

    def refund_allowed(self, order_id: str, email: str) -> bool:
        """Policy: only a *delivered* order owned by the identified customer can be refunded."""
        order = self.orders.get(order_id)
        if order is None:
            raise MissingFieldError(f"order '{order_id}' does not exist")
        return bool(order["status"] == "delivered" and order["user_id"] == self.user_id_for_email(email))

    @staticmethod
    def same_prices(refunded: list[dict[str, Any]], items: list[dict[str, Any]]) -> bool:
        """Contract helper: every refunded item carries the price the lookup reported for that item."""
        by_id = {it["item_id"]: it["price"] for it in items}
        return all(r["item_id"] in by_id and abs(by_id[r["item_id"]] - r["price"]) < 1e-9 for r in refunded)

    def truth_functions(self) -> dict[str, Callable[..., Any]]:
        """The functions a check may call as ``truth.<name>``."""
        return {
            "catalog_price": self.catalog_price,
            "catalog_total": self.catalog_total,
            "fix_prices": self.fix_prices,
            "user_id_for_email": self.user_id_for_email,
            "refund_allowed": self.refund_allowed,
            "same_prices": self.same_prices,
        }

    # ---- examples for the UI ------------------------------------------------------------------------------
    def example_tasks(self, limit: int = 12) -> list[dict[str, Any]]:
        """Realistic, ready-to-run inputs: delivered orders with distinct item names, and two not-eligible cases."""
        out: list[dict[str, Any]] = []
        for oid in sorted(self.orders):
            o = self.orders[oid]
            names = [it["name"] for it in o["items"]]
            if o["status"] != "delivered" or len(set(names)) != len(names) or len(names) < 2:
                continue
            pick = names[:2]
            out.append(self._task(oid, o, pick, f"Please return the {pick[0]} and the {pick[1]} from order {oid}."))
            if len(out) >= limit - 2:
                break
        for status in ("pending", "cancelled"):
            found = next((i for i in sorted(self.orders) if self.orders[i]["status"] == status), None)
            if found:
                o = self.orders[found]
                n = o["items"][0]["name"]
                out.append(self._task(found, o, [n], f"I want to return the {n} from order {found}."))
        return out

    def _task(self, oid: str, o: dict[str, Any], names: list[str], message: str) -> dict[str, Any]:
        return {
            "order_id": oid,
            "email": self.users[o["user_id"]]["email"],
            "message": message,
            "label": f"{oid} ({o['status']}): {', '.join(names)}",
        }


@lru_cache(maxsize=1)
def default_store() -> RetailStore:
    """The snapshot store, loaded once per process."""
    return RetailStore.load()
