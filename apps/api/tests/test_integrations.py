"""Phoenix and Langfuse integration through the HTTP API (F13): connect, send, import, verify, write back.

The platforms are in-memory servers that speak the same REST shapes (granite_connectors.testing); the live check
against a real Phoenix server is scripts/check_connectors_live.py.
"""

from __future__ import annotations

import pytest
from granite_connectors.testing import FakeLangfuse, FakePhoenix

from granite_api.services import connections as con_service
from tests.conftest import start_run


@pytest.fixture
def phoenix(monkeypatch):
    fake = FakePhoenix(page=3)
    monkeypatch.setattr(con_service, "TRANSPORT", fake)
    return fake


@pytest.fixture
def langfuse(monkeypatch):
    fake = FakeLangfuse(page=2)
    monkeypatch.setattr(con_service, "TRANSPORT", fake)
    return fake


def connect(client, kind="phoenix", **extra):
    body = {"kind": kind, "name": f"{kind} demo", "base_url": "http://localhost:6006", "project": "granite-demo",
            **extra}
    r = client.post("/api/connections", json=body)
    assert r.status_code == 201, r.text
    return r.json()


class TestPhoenix:
    def test_send_import_investigate_and_write_back_round_trip(self, client, example, phoenix):
        con = connect(client)
        original = start_run(client, example, "stale_price")["run"]
        sent = client.post(f"/api/runs/{original['id']}/export", json={"connection_id": con["id"]})
        assert sent.status_code == 200, sent.text
        assert sent.json()["spans_sent"] == 6 and "granite-demo" in phoenix.projects
        again = client.post(f"/api/runs/{original['id']}/export", json={"connection_id": con["id"]})
        assert again.json()["spans_sent"] == 0  # idempotent

        result = client.post(f"/api/connections/{con['id']}/import", json={"limit": 10})
        assert result.status_code == 200, result.text
        body = result.json()
        assert body["fetched"] == 1 and len(body["imported"]) == 1 and body["imported"][0]["lineage"] == ["declared"]
        run = client.get(f"/api/runs/{body['imported'][0]['run_id']}").json()
        assert run["llm_mode"] == "imported" and run["seed"] == original["seed"]
        assert run["trace"]["steps"] == original["trace"]["steps"]
        assert [f["title"] for f in run["findings"]] == [f["title"] for f in original["findings"]]

        finding_id = run["findings"][0]["id"]
        inv = client.post(f"/api/findings/{finding_id}/investigations", json={}).json()
        assert client.get(f"/api/investigations/{inv['investigation_id']}").json()["confirmed_step"] == "s2"
        wb = client.post(f"/api/findings/{finding_id}/writeback")
        assert wb.status_code == 200, wb.text
        out = wb.json()
        assert out["label"] == "confirmed" and out["step_id"] == "s2"
        links = client.get(f"/api/runs/{run['id']}/links").json()
        s2_span = links[0]["span_ids"]["s2"]
        assert out["written"][0]["span_id"] == s2_span
        ann = phoenix.annotations[(s2_span, "granite.verdict", "granite")]
        assert ann["result"]["label"] == "confirmed" and ann["result"]["score"] == 1.0
        assert ann["metadata"]["level"] == "V2" and "Order Lookup (s2)" in ann["result"]["explanation"]

        second = client.post(f"/api/connections/{con['id']}/import", json={}).json()
        assert second["imported"] == [] and second["skipped"][0]["reason"] == "already imported"
        listed = client.get("/api/connections").json()
        assert listed[0]["imported_runs"] == 1 and listed[0]["exported_runs"] == 1 and listed[0]["keys_configured"]

    def test_traces_that_do_not_match_the_workflow_are_skipped_with_a_reason(self, client, phoenix):
        con = connect(client)
        phoenix.projects["granite-demo"] = [{
            "name": "chat", "context": {"trace_id": "t" * 32, "span_id": "a" * 16}, "span_kind": "LLM",
            "parent_id": None, "start_time": "2026-11-15T09:00:00+00:00", "end_time": "2026-11-15T09:00:01+00:00",
            "status_code": "OK", "status_message": "", "attributes": {"input": {"value": "hi"}}, "events": [],
        }]
        body = client.post(f"/api/connections/{con['id']}/import", json={}).json()
        assert body["imported"] == [] and "s1, s2, s3" in body["skipped"][0]["reason"]

    def test_test_endpoint_explains_a_new_project_and_reports_an_unreachable_server(self, client, phoenix, monkeypatch):
        con = connect(client, project="nope")
        r = client.post(f"/api/connections/{con['id']}/test").json()
        assert r["ok"] is True and "created when the first run is sent" in r["detail"]["note"]

        def down(*a):
            raise OSError("connection refused")
        monkeypatch.setattr(con_service, "TRANSPORT", down)
        r = client.post(f"/api/connections/{con['id']}/test").json()
        assert r["ok"] is False and "could not reach" in r["detail"]["error"]

    def test_platform_errors_become_502_problems(self, client, phoenix):
        con = connect(client, project="missing")
        r = client.post(f"/api/connections/{con['id']}/import", json={})
        assert r.status_code == 502 and "Check the URL and project name" in r.json()["detail"]


class TestLangfuse:
    def test_needs_keys_in_the_environment(self, client, langfuse):
        con = connect(client, "langfuse", project="")
        assert con["keys_configured"] is False
        r = client.post(f"/api/connections/{con['id']}/test")
        assert r.status_code == 409 and "GRANITE_LANGFUSE_PUBLIC_KEY" in r.json()["detail"]

    def test_send_import_and_score_round_trip(self, make_client, example, langfuse):
        client = make_client(langfuse_public_key="pk-lf-test", langfuse_secret_key="sk-lf-test")
        con = connect(client, "langfuse", base_url="https://lf.example", project="refund-desk")
        assert client.post(f"/api/connections/{con['id']}/test").json()["ok"] is True
        original = start_run(client, example, "stale_price")["run"]
        sent = client.post(f"/api/runs/{original['id']}/export", json={"connection_id": con["id"]}).json()
        assert sent["spans_sent"] == 6 and next(iter(langfuse.traces.values()))["name"] == "refund-desk"
        body = client.post(f"/api/connections/{con['id']}/import", json={}).json()
        assert len(body["imported"]) == 1
        run_id = body["imported"][0]["run_id"]
        finding_id = client.get(f"/api/runs/{run_id}").json()["findings"][0]["id"]
        out = client.post(f"/api/findings/{finding_id}/writeback").json()
        assert out["label"] == "hypothesized" and len(out["written"]) == 1
        score = next(iter(langfuse.scores.values()))
        assert score["dataType"] == "CATEGORICAL" and score["value"] == "hypothesized" and score["name"] == "granite.verdict"


class TestValidation:
    def test_bad_connections_are_refused(self, client):
        base = {"kind": "phoenix", "name": "x", "base_url": "http://localhost:6006", "project": "p"}
        assert client.post("/api/connections", json={**base, "kind": "datadog"}).status_code == 422
        assert client.post("/api/connections", json={**base, "base_url": "ftp://host/x"}).status_code == 422
        assert client.post("/api/connections", json={**base, "project": ""}).status_code == 422
        assert client.post("/api/connections", json={**base, "workflow": "nope"}).status_code == 404
        assert client.post("/api/connections", json={**base, "steps": {"a": "bad id!"}}).status_code == 422

    def test_unknown_ids_and_unlinked_runs(self, client, example):
        assert client.post("/api/connections/con_nope/import", json={}).status_code == 404
        run = start_run(client, example, "stale_price")["run"]
        assert client.post(f"/api/runs/{run['id']}/export", json={"connection_id": "con_nope"}).status_code == 404
        r = client.post(f"/api/findings/{run['findings'][0]['id']}/writeback")
        assert r.status_code == 409 and "Import the run" in r.json()["detail"]
        assert client.get(f"/api/runs/{run['id']}/links").json() == []
