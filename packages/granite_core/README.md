# granite_core

The framework-free heart of Granite: everything that decides *what is wrong, where it began, and whether a diagnosis is proven*. No web, database or network code (the only dependency is pydantic), so it is fast to test and could be offered as an SDK later. Rationale: [ADR-001](../../docs/adr/adr-001-modular-monolith.md).

| Module | Does | Decision |
|---|---|---|
| `trace.py` | Granite Trace v1: steps, declared reads, validation (JSON Schema in `schema/`) | [ADR-009](../../docs/adr/adr-009-trace-schema-v1.md) |
| `dsl.py`, `checks.py` | Check language (restricted syntax tree, never `eval`), check results, findings | [ADR-004](../../docs/adr/adr-004-ast-check-dsl.md) |
| `lineage.py`, `attribution.py` | Data-flow edges; ranked origin hypotheses | [ADR-005](../../docs/adr/adr-005-provenance-first-attribution.md) |
| `verification.py`, `experiment.py` | Interventions, replay planning, verdict rule VR-1, N replays plus M controls | [ADR-006](../../docs/adr/adr-006-vr1-verdict-rule.md) |
| `lifecycle.py` | Finding state machine; illegal transitions raise | [diagram](../../docs/diagrams/finding-state-machine.md) |
| `evidence.py` | Canonical JSON, SHA-256, tamper check | |
| `runner.py` | Runs a workflow, records inputs and reads, injects faults, replays from a step | [ADR-002](../../docs/adr/adr-002-own-runner-first.md) |
| `llm.py` | Provider interface, cassette (record and replay) | [ADR-008](../../docs/adr/adr-008-llm-provider-and-recorded-mode.md) |
| `redaction.py` | Masks e-mail, phone, CNIC and card-like numbers (tested; **not yet applied to stored traces**, see defect D-07) | |

```bash
pip install -e ".[dev]"
pytest --cov=granite_core      # 207 tests, about 10 seconds
ruff check . && mypy granite_core
```
