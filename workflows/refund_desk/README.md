# refund_desk

Granite's first system under test: a five-step customer-support refund workflow on a synthetic retail snapshot. The *workflow* and the *source of truth used by the checks* read the same data through two separate paths on purpose, so a corrupted tool answer can be detected.

| Step | Kind | Does |
|---|---|---|
| s1 Intake | language model | Reads the message, returns the order id and item names |
| s2 Order Lookup | tool | Reads the order (the fault enters here) |
| s3 Policy | code | Eligible if the order is delivered and belongs to the customer; picks the items |
| s4 Refund Calculator | language model | Adds the prices |
| s5 Writer | language model | Writes the customer message |

Data flow and checks: [`docs/diagrams/refund-desk-dataflow.md`](../../docs/diagrams/refund-desk-dataflow.md). Code: `definition.py` (steps, 7 checks, repair rules), `steps.py`, `faults.py` (stale price), `store.py` (data, source of truth), `prompts/` (versioned; **editing a prompt invalidates the recorded cassette**).

Data: [`data/seed/taubench_retail_v1`](../../data/seed/taubench_retail_v1/) (75 orders; MIT-licensed tau-bench subset, rebuilt by `scripts/build_truth_snapshot.py`).

```bash
pip install -e ../../packages/granite_core -e ".[dev]"
pytest --cov=refund_desk       # 49 tests
```
