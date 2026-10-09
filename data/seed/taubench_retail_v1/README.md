# taubench_retail_v1 (truth snapshot)

A small, deterministic subset of the tau-bench retail data, used by the Refund Desk workflow as its **source of truth** (order owners and statuses, catalogue prices) and as its synthetic customer data. Everything in it is synthetic.

- orders: 75 (60 delivered with 2-4 items, 10 pending, 5 cancelled); users: 72; products: 47
- selection rule and rebuild command: `scripts/build_truth_snapshot.py`
- source: tau-bench (Sierra), MIT licence, see `LICENSE.txt`; modified only by selecting a subset

Source file hashes (SHA-256) at build time:

- `orders.json`: `81595d5cb28171e01133b52714b456003a9cd733cfd013c1d9d397ac0a7484c4`
- `users.json`: `351c93bce10ce26ba2c9f6a048665d7e002ccff2c1c42a9d628680e73acc5342`
- `products.json`: `9ee1541a51eaa14222bd418d2981eb4527ca42420e977ecfb36f72cab15ef64e`
