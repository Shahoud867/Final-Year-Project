from __future__ import annotations

import json
import urllib.error
from datetime import UTC, datetime, timedelta

import pytest
from granite_core.trace import RunInfo, Step, TraceV1

from granite_connectors import (
    ConnectorError,
    HttpClient,
    LangfuseClient,
    PhoenixClient,
    Profile,
    SpanRecord,
    map_trace,
    trace_to_spans,
)
from granite_connectors.langfuse import from_langfuse, to_ingestion
from granite_connectors.mapping import as_dict, select_steps
from granite_connectors.phoenix import from_phoenix, to_phoenix
from granite_connectors.testing import FakeLangfuse, FakePhoenix

T0 = datetime(2026, 11, 15, 9, 0, tzinfo=UTC)


def sample_trace(status: str = "completed") -> TraceV1:
    task = {"order_id": "#W1234567", "message": "refund the lamp please"}
    steps = [
        Step(step_id="s1", agent="intake", kind="llm", inputs={"message": task["message"]},
             outputs={"order_id": "#W1234567", "item_names": ["Desk Lamp"]}, reads=["task.message"], model="m1"),
        Step(step_id="s2", agent="lookup", kind="tool", inputs={"order_id": "#W1234567"},
             outputs={"items": [{"name": "Desk Lamp", "price": 49.99}]}, reads=["s1.order_id"]),
        Step(step_id="s3", agent="policy", kind="code", inputs={"items": [{"name": "Desk Lamp", "price": 49.99}]},
             outputs={"refund": 49.99}, reads=["s2.items"],
             error="boom" if status == "errored" else None),
    ]
    return TraceV1(run=RunInfo(workflow="demo", status=status, task_input=task, final_output={"refund": 49.99},
                               started_at=T0), steps=steps)


def span(i: int, name: str, inp: object, out: object, **kw: object) -> SpanRecord:
    return SpanRecord(span_id=f"sp{i}", trace_id="t1", parent_id=kw.pop("parent", "root"), name=name,
                      start=T0 + timedelta(seconds=i), input=inp, output=out, **kw)  # type: ignore[arg-type]


ROOT = SpanRecord(span_id="root", trace_id="t1", name="agent run", kind="chain", start=T0,
                  input={"question": "where is order 42?"}, output="done")


# ---- mapping ------------------------------------------------------------------------------------------------------
def test_export_then_map_round_trips_steps_and_declared_lineage():
    trace = sample_trace()
    mapped = map_trace(trace_to_spans(trace, "run_1"), Profile(name="demo", workflow="demo"), runtime="phoenix")
    got = mapped.trace
    assert [s.step_id for s in got.steps] == ["s1", "s2", "s3"]
    assert [s.reads for s in got.steps] == [s.reads for s in trace.steps]
    assert [s.outputs for s in got.steps] == [s.outputs for s in trace.steps]
    assert [s.kind for s in got.steps] == ["llm", "tool", "code"]
    assert got.run.task_input == trace.run.task_input
    assert got.steps[0].model == "m1"
    assert {e.tier for e in mapped.lineage} == {"declared"}
    assert mapped.spans_total == 4 and mapped.spans_dropped == 1


def test_value_matching_finds_handoffs_when_nothing_is_declared():
    spans = [ROOT,
             span(1, "classify", "where is order 42?", {"order_ref": "ORD-000042-XYZ"}, kind="llm"),
             span(2, "fetch", {"q": "lookup ORD-000042-XYZ now"}, {"eta": "2026-11-20T10:00:00"}, kind="tool"),
             span(3, "answer", {"context": "ETA 2026-11-20T10:00:00"}, "It arrives on the 20th", kind="llm")]
    mapped = map_trace(spans, Profile(name="support"), runtime="langfuse")
    steps = mapped.trace.steps
    assert [s.step_id for s in steps] == ["classify", "fetch", "answer"]
    assert steps[1].reads == ["classify.order_ref"] and steps[2].reads == ["fetch.eta"]
    assert {e.tier for e in mapped.lineage} == {"value"}
    assert mapped.trace.run.task_input == {"question": "where is order 42?"}
    assert mapped.trace.run.final_output == {"value": "It arrives on the 20th"}


def test_numbers_rendered_in_text_count_as_a_handoff_but_short_values_do_not():
    spans = [ROOT, span(1, "price", {}, {"total": 1249.5, "ok": True, "code": "A1"}),
             span(2, "write", {"prompt": "Tell the user the total is 1249.50 dollars"}, "x")]
    steps = map_trace(spans, Profile(name="p"), runtime="x").trace.steps
    assert steps[1].reads == ["price.total"]


def test_order_is_the_fallback_and_profile_names_steps():
    spans = [ROOT, span(1, "Plan step", {}, {"plan": "a"}), span(2, "Act step", {"x": 1}, {"result": 2}),
             span(3, "noise", {}, {})]
    profile = Profile(name="p", steps={"Plan step": "plan", "Act step": "act"})
    mapped = map_trace(spans, profile, runtime="x")
    assert [s.step_id for s in mapped.trace.steps] == ["plan", "act"]
    assert mapped.trace.steps[1].reads == ["plan.plan"]
    assert mapped.lineage[0].tier == "order"


def test_leaf_spans_become_steps_and_duplicate_names_are_numbered():
    spans = [ROOT, span(1, "tool call!", {}, {"a": 1}), span(2, "tool call!", {}, {"b": 2}),
             span(3, "group", {}, {}, parent="root"), span(4, "inner", {}, {"c": 3}, parent="sp3")]
    chosen = select_steps(spans, Profile(name="p"))
    assert [s.span_id for s in chosen] == ["sp1", "sp2", "sp4"]
    ids = [s.step_id for s in map_trace(spans, Profile(name="p"), runtime="x").trace.steps]
    assert ids == ["tool_call", "tool_call_2", "inner"]


def test_errors_and_bad_input_are_reported():
    trace = map_trace(trace_to_spans(sample_trace("errored"), "r"), Profile(name="p"), runtime="x").trace
    assert trace.run.status == "errored" and trace.steps[2].error == "boom" and trace.run.final_output == {}
    with pytest.raises(ValueError, match="at least one"):
        map_trace([], Profile(name="p"), runtime="x")
    other = ROOT.model_copy(update={"trace_id": "t2", "span_id": "r2"})
    with pytest.raises(ValueError, match="more than one trace"):
        map_trace([ROOT, other], Profile(name="p"), runtime="x")


def test_declared_reads_of_unknown_steps_are_ignored():
    s = span(1, "a", {}, {"v": 1}, attributes={"granite.reads": '["ghost.x", "task.q", "bad"]'})
    assert map_trace([ROOT, s], Profile(name="p"), runtime="x").trace.steps[0].reads == ["task.q"]


def test_as_dict_parses_json_and_wraps_scalars():
    assert as_dict('{"a": 1}') == {"a": 1}
    assert as_dict("hello") == {"value": "hello"}
    assert as_dict([1, 2]) == {"value": [1, 2]}
    assert as_dict(None) == {}


def test_export_ids_are_stable_and_otel_shaped():
    a, b = trace_to_spans(sample_trace(), "run_1"), trace_to_spans(sample_trace(), "run_1")
    assert [s.span_id for s in a] == [s.span_id for s in b]
    assert len(a[0].trace_id) == 32 and all(len(s.span_id) == 16 for s in a)
    assert trace_to_spans(sample_trace(), "run_2")[0].trace_id != a[0].trace_id


# ---- http ---------------------------------------------------------------------------------------------------------
def test_http_retries_transient_failures_with_backoff():
    replies = [(503, {}, b""), (429, {"Retry-After": "2"}, b""), (200, {}, b'{"ok": true}')]
    waits: list[float] = []
    client = HttpClient("http://x", transport=lambda *a: replies.pop(0), sleep=waits.append)
    assert client.get("/p") == {"ok": True}
    assert waits == [0.5, 2.0]


def test_http_connection_errors_and_client_errors_become_connector_errors():
    def down(*a: object) -> tuple[int, dict[str, str], bytes]:
        raise urllib.error.URLError("refused")
    client = HttpClient("http://x", headers={"Authorization": "Basic SECRET"}, transport=down, retries=1,
                        sleep=lambda s: None)
    with pytest.raises(ConnectorError, match="could not reach http://x") as err:
        client.get("/p")
    assert "SECRET" not in str(err.value)
    bad = HttpClient("http://x", transport=lambda *a: (401, {}, b'{"message": "Invalid keys"}'))
    with pytest.raises(ConnectorError, match="HTTP 401: Invalid keys") as err2:
        bad.get("/p")
    assert err2.value.status == 401
    with pytest.raises(ConnectorError, match="did not return JSON"):
        HttpClient("http://x", transport=lambda *a: (200, {}, b"<html>")).get("/")
    assert HttpClient("http://x", transport=lambda *a: (204, {}, b"")).get("/") is None


def test_http_refuses_non_http_schemes():
    with pytest.raises(ConnectorError, match="only http and https"):
        HttpClient("file:///etc").get("/passwd")


def test_url_drops_empty_params_and_repeats_lists():
    c = HttpClient("http://x/", transport=lambda *a: (200, {}, b"{}"))
    assert c.url("/s", {"a": None, "b": "", "t": ["1", "2"]}) == "http://x/s?t=1&t=2"


# ---- phoenix ------------------------------------------------------------------------------------------------------
def test_phoenix_send_import_and_annotate_round_trip():
    fake = FakePhoenix(page=2)
    px = PhoenixClient("http://phoenix:6006", "granite-demo", api_key="k", transport=fake)
    px.ensure_project()
    spans = trace_to_spans(sample_trace(), "run_1")
    assert px.send(spans) == 4
    assert px.send(spans) == 0  # idempotent: Phoenix would reject duplicates, so nothing is re-sent
    traces = px.traces(limit=5)
    assert len(traces) == 1 and len(traces[0]) == 4  # paging (2 per page) reassembled the whole trace
    mapped = map_trace(traces[0], Profile(name="demo"), runtime="phoenix")
    assert [s.step_id for s in mapped.trace.steps] == ["s1", "s2", "s3"]
    assert mapped.trace.steps[2].reads == ["s2.items"]
    assert mapped.trace.run.external_id == spans[0].trace_id
    px.annotate(spans[2].span_id, "granite.verdict", label="confirmed", score=1.0, explanation="fix worked")
    px.annotate(spans[2].span_id, "granite.verdict", label="refuted", score=0.0, explanation="again")
    assert len(fake.annotations) == 1  # same name + identifier updates in place
    assert all(h.get("Authorization") == "Bearer k" for h in fake.headers)


def test_phoenix_conversion_keeps_openinference_fields():
    rec = trace_to_spans(sample_trace(), "r")[1]
    body = to_phoenix(rec)
    assert body["span_kind"] == "LLM" and json.loads(body["attributes"]["input.value"]) == rec.input
    back = from_phoenix({**body, "status_code": "ERROR", "status_message": "bad"})
    assert back.kind == "llm" and back.input == rec.input and back.status == "error" and back.error == "bad"
    meta = from_phoenix({**body, "attributes": {"metadata.granite.reads": '["task.q"]', "input.value": "hi",
                                                "input.mime_type": "text/plain"}})
    assert meta.attributes["granite.reads"] == '["task.q"]' and meta.input == "hi"


def test_phoenix_missing_project_is_a_404_connector_error():
    px = PhoenixClient("http://p", "nope", transport=FakePhoenix())
    with pytest.raises(ConnectorError) as err:
        px.ping()
    assert err.value.status == 404


# ---- langfuse -----------------------------------------------------------------------------------------------------
def test_langfuse_send_import_and_score_round_trip():
    fake = FakeLangfuse(page=2)
    lf = LangfuseClient("https://lf.example", "pk-lf-1", "sk-lf-1", transport=fake)
    assert lf.ping()["status"] == "OK"
    spans = trace_to_spans(sample_trace(), "run_1")
    assert lf.send(spans, "demo") == 4
    traces = lf.traces(limit=5)
    assert len(traces) == 1
    mapped = map_trace(traces[0], Profile(name="demo"), runtime="langfuse")
    assert [s.step_id for s in mapped.trace.steps] == ["s1", "s2", "s3"]
    assert mapped.trace.steps[1].reads == ["s1.order_id"]
    assert mapped.trace.run.task_input == sample_trace().run.task_input
    sid = lf.score(spans[0].trace_id, spans[3].span_id, "granite.verdict", label="confirmed", comment="c")
    assert lf.score(spans[0].trace_id, spans[3].span_id, "granite.verdict", label="refuted", comment="d") == sid
    assert len(fake.scores) == 1 and fake.scores[sid]["dataType"] == "CATEGORICAL"


def test_langfuse_ingestion_events_and_rejections():
    spans = trace_to_spans(sample_trace(), "r")
    events = to_ingestion(spans, "demo")
    assert [e["type"] for e in events] == ["trace-create", "generation-create", "span-create", "span-create"]
    assert events[1]["body"]["model"] == "m1" and "parentObservationId" not in events[1]["body"]
    fake = FakeLangfuse()
    fake.reject = "span-create"
    with pytest.raises(ConnectorError, match="400"):
        LangfuseClient("https://lf", "pk", "sk", transport=fake).send(spans, "demo")


def test_langfuse_observation_mapping_and_auth_failure():
    rec = from_langfuse({"id": "o1", "traceId": "t", "type": "GENERATION", "model": "gpt", "level": "ERROR",
                         "statusMessage": "rate limited", "metadata": {"granite.reads": ["task.q"]}})
    assert rec.kind == "llm" and rec.status == "error" and rec.error == "rate limited"
    assert rec.attributes["llm.model_name"] == "gpt" and rec.name == "generation"
    with pytest.raises(ConnectorError, match="401"):
        LangfuseClient("https://lf", "pk", "sk", transport=lambda *a: (401, {}, b"{}")).ping()


def test_langfuse_legacy_ingestion_and_read_paths():
    """Cover FakeLangfuse legacy endpoints (traces, observations, pagination)."""
    fake = FakeLangfuse(page=2)
    body = json.dumps({"batch": [
        {"id": "e1", "type": "trace-create", "timestamp": "2026-01-01T00:00:00Z",
         "body": {"id": "t1", "name": "demo", "timestamp": "2026-01-01T00:00:00Z"}},
        {"id": "e2", "type": "span-create", "timestamp": "2026-01-01T00:00:00Z",
         "body": {"id": "o1", "traceId": "t1", "name": "step1"}},
        {"id": "e3", "type": "generation-create", "timestamp": "2026-01-01T00:00:00Z",
         "body": {"id": "o2", "traceId": "t1", "name": "llm1"}},
    ]}).encode()
    auth = {"Authorization": "Basic cGs6c2s="}
    code, _, resp = fake("POST", "https://lf/api/public/ingestion", auth, body)
    assert code == 207
    data = json.loads(resp)
    assert len(data["successes"]) == 3
    code, _, resp = fake("GET", "https://lf/api/public/traces?name=demo", auth, None)
    assert code == 200 and len(json.loads(resp)["data"]) == 1
    code, _, resp = fake("GET", "https://lf/api/public/traces/t1", auth, None)
    assert code == 200 and json.loads(resp)["id"] == "t1"
    code, _, _ = fake("GET", "https://lf/api/public/traces/nonexistent", auth, None)
    assert code == 404
    code, _, resp = fake("GET", "https://lf/api/public/observations?traceId=t1&limit=1&page=1", auth, None)
    assert code == 200 and len(json.loads(resp)["data"]) == 1
    code, _, _ = fake("GET", "https://lf/api/public/unknown", auth, None)
    assert code == 404


def test_langfuse_v2_name_filter():
    """Cover the name filter branch in _v2_observations."""
    fake = FakeLangfuse()
    auth = {"Authorization": "Basic cGs6c2s="}
    body = json.dumps({"batch": [
        {"id": "e1", "type": "trace-create", "timestamp": "2026-01-01T00:00:00Z",
         "body": {"id": "t1", "name": "demo"}},
        {"id": "e2", "type": "span-create", "timestamp": "2026-01-01T00:00:00Z",
         "body": {"id": "o1", "traceId": "t1", "name": "alpha"}},
        {"id": "e3", "type": "span-create", "timestamp": "2026-01-01T00:00:00Z",
         "body": {"id": "o2", "traceId": "t1", "name": "beta"}},
    ]}).encode()
    fake("POST", "https://lf/api/public/ingestion", auth, body)
    code, _, resp = fake("GET", "https://lf/api/public/v2/observations?name=alpha", auth, None)
    assert code == 200
    data = json.loads(resp)["data"]
    assert len(data) == 1 and data[0]["name"] == "alpha"


def test_fake_phoenix_list_projects_and_edge_cases():
    """Cover FakePhoenix paths: list projects, missing project, project detail, duplicate spans."""
    fake = FakePhoenix()
    auth: dict[str, str] = {}
    fake("POST", "http://px/v1/projects", auth, json.dumps({"name": "p1"}).encode())
    code, _, resp = fake("GET", "http://px/v1/projects", auth, None)
    assert code == 200 and len(json.loads(resp)["data"]) == 1
    code, _, _ = fake("GET", "http://px/v1/projects/nonexistent/spans", auth, None)
    assert code == 404
    code, _, resp = fake("GET", "http://px/v1/projects/p1", auth, None)
    assert code == 200 and json.loads(resp)["data"]["name"] == "p1"
    code, _, _ = fake("GET", "http://px/v1/projects/p1/spans", auth, None)
    assert code == 200
    span = {"context": {"span_id": "s1", "trace_id": "t1"}, "attributes": {"a.b": 1}}
    fake("POST", "http://px/v1/projects/p1/spans", auth, json.dumps({"data": [span]}).encode())
    code, _, _ = fake("POST", "http://px/v1/projects/p1/spans", auth, json.dumps({"data": [span]}).encode())
    assert code == 400
    code, _, _ = fake("GET", "http://px/v1/unknown", auth, None)
    assert code == 404


def test_untimed_steps_are_placed_after_their_predecessor():
    trace = sample_trace()
    trace.steps[0].started_at, trace.steps[0].ended_at = T0 + timedelta(seconds=5), T0 + timedelta(seconds=6)
    spans = trace_to_spans(trace, "r")[1:]
    starts = [s.start for s in spans]
    assert starts == sorted(starts) and spans[1].start == T0 + timedelta(seconds=6)
    back = map_trace(trace_to_spans(trace, "r"), Profile(name="p"), runtime="x").trace
    assert back.steps[1].started_at is None and back.steps[0].started_at == T0 + timedelta(seconds=5)
