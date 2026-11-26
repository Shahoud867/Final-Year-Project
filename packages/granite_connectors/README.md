# granite_connectors

Reads traces from Arize Phoenix and Langfuse into Granite Trace v1, sends Granite runs to them, and writes verdicts back. Depends on `granite_core`, pydantic and the standard library only (ADR-012).

| Module | What it does |
|---|---|
| `spans.py` | `SpanRecord`, the neutral span every platform is converted to; `Profile` (span name to step alias, workflow) |
| `mapping.py` | `map_trace`: spans of one trace to `TraceV1`, with lineage tier per edge (declared, value, order) |
| `export.py` | `trace_to_spans`: a Granite run as spans with stable ids and its reads declared |
| `phoenix.py` | `PhoenixClient`: list, create and annotate spans (REST v1, checked against Phoenix 21.0.0) |
| `langfuse.py` | `LangfuseClient`: traces, observations, ingestion, scores (public API, Basic auth) |
| `http.py` | JSON over `urllib` with retries and backoff; errors never contain credentials |
| `testing.py` | In-memory Phoenix and Langfuse servers for tests |

```python
from granite_connectors import PhoenixClient, Profile, map_trace

px = PhoenixClient("http://localhost:6006", "my-project")
for spans in px.traces(limit=10):
    mapped = map_trace(spans, Profile(name="my app", steps={"order lookup": "lookup"}), runtime="phoenix")
    print(mapped.trace.run.external_id, [e.tier for e in mapped.lineage])
```

Tests: `pytest` here (in-memory servers). Against real servers: `python scripts/check_connectors_live.py --phoenix http://localhost:6006`.
