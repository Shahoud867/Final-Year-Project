"""The published Granite Trace v1 schema must match the model; example traces must validate against it."""

from __future__ import annotations

import json
from pathlib import Path

from granite_core.trace import TraceV1
from tests.conftest import make_trace

SCHEMA = Path(__file__).resolve().parents[1] / "schema" / "granite-trace-v1.schema.json"


def test_committed_schema_matches_the_model() -> None:
    committed = json.loads(SCHEMA.read_text(encoding="utf-8"))
    generated = TraceV1.model_json_schema()
    generated["$schema"], generated["$id"] = committed["$schema"], committed["$id"]
    assert committed == generated, "run: python scripts/export_trace_schema.py"


def test_schema_declares_the_version_and_the_documented_limits() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert schema["properties"]["schema_version"]["default"] == "granite.trace/v1"
    assert schema["properties"]["steps"]["maxItems"] == 500
    assert schema["$defs"]["Step"]["additionalProperties"] is False


def test_a_real_trace_round_trips_through_json() -> None:
    trace = make_trace()
    assert TraceV1.model_validate_json(trace.model_dump_json()) == trace
