#!/usr/bin/env python3
"""Build data/seed/taubench_retail_v1/ from the raw tau-bench retail data (deterministic).

Selection rule (so the snapshot can be rebuilt and audited):
  * the first 60 *delivered* orders (sorted by order id) with 2 to 4 items,
  * the first 10 *pending* and first 5 *cancelled* orders (for the "not eligible" paths),
  * every user who owns one of those orders, and every product those orders reference.

Source: tau-bench (Sierra), MIT licence, https://github.com/sierra-research/tau-bench . The licence text and
SHA-256 hashes of the three source files are copied into the snapshot folder.

Usage: python scripts/build_truth_snapshot.py
"""
from __future__ import annotations

import hashlib
import json
import os

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SRC = os.path.join(REPO, "data", "raw", "taubench_retail")
DST = os.path.join(REPO, "data", "seed", "taubench_retail_v1")


def load(name: str) -> dict:
    with open(os.path.join(SRC, "data", name), encoding="utf-8") as fh:
        return json.load(fh)


def sha(path: str) -> str:
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main() -> None:
    orders, users, products = load("orders.json"), load("users.json"), load("products.json")
    ids = sorted(orders)
    delivered = [i for i in ids if orders[i]["status"] == "delivered" and 2 <= len(orders[i]["items"]) <= 4][:60]
    pending = [i for i in ids if orders[i]["status"] == "pending"][:10]
    cancelled = [i for i in ids if orders[i]["status"] == "cancelled"][:5]
    chosen = delivered + pending + cancelled
    o = {i: orders[i] for i in chosen}
    u = {uid: users[uid] for uid in sorted({o[i]["user_id"] for i in o})}
    pids = sorted({it["product_id"] for i in o for it in o[i]["items"]})
    p = {pid: products[pid] for pid in pids}
    os.makedirs(DST, exist_ok=True)
    for name, obj in (("orders.json", o), ("users.json", u), ("products.json", p)):
        with open(os.path.join(DST, name), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(obj, fh, indent=1, sort_keys=True, ensure_ascii=False)
            fh.write("\n")
    with open(os.path.join(SRC, "LICENSE"), encoding="utf-8") as fh, open(
        os.path.join(DST, "LICENSE.txt"), "w", encoding="utf-8", newline="\n"
    ) as out:
        out.write(fh.read())
    src_hashes = {n: sha(os.path.join(SRC, "data", n)) for n in ("orders.json", "users.json", "products.json")}
    with open(os.path.join(DST, "README.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            "# taubench_retail_v1 (truth snapshot)\n\n"
            "A small, deterministic subset of the tau-bench retail data, used by the Refund Desk workflow as its "
            "**source of truth** (order owners and statuses, catalogue prices) and as its synthetic customer data. "
            "Everything in it is synthetic.\n\n"
            f"- orders: {len(o)} ({len(delivered)} delivered with 2-4 items, {len(pending)} pending, "
            f"{len(cancelled)} cancelled); users: {len(u)}; products: {len(p)}\n"
            "- selection rule and rebuild command: `scripts/build_truth_snapshot.py`\n"
            "- source: tau-bench (Sierra), MIT licence, see `LICENSE.txt`; modified only by selecting a subset\n\n"
            "Source file hashes (SHA-256) at build time:\n\n"
            + "".join(f"- `{n}`: `{h}`\n" for n, h in src_hashes.items())
        )
    print(f"snapshot: {len(o)} orders, {len(u)} users, {len(p)} products -> {os.path.relpath(DST, REPO)}")


if __name__ == "__main__":
    main()
