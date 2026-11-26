"""Acceptance criteria of the Mid-1 functional requirements (master plan section 15), one test per requirement.

The FR id is in each test name so scripts/check_traceability.py can link requirement to test.
"""

from __future__ import annotations

import inspect
import json
import time

from granite_core.attribution import attribute
from granite_core.checks import evaluate_checks
from granite_core.trace import TraceV1

from granite_api.config import Settings
from granite_api.db import make_session_factory, session_scope
from granite_api.llm_factory import build_provider
from granite_api.models import AuditLog, Finding
from granite_api.registry import WORKFLOWS
from tests.conftest import hypothesis_for, open_finding, start_run, verify


def db_of(client):
    return make_session_factory(client.app.state.session_factory.kw["bind"])


def test_fr_run_02_hypotheses_are_reproducible_without_the_fault_record(client, example):
    finding = open_finding(client, example)
    assert set(inspect.signature(attribute).parameters) == {"trace", "results", "symptom_step"}  # no way to pass a fault
    run = client.get(f"/api/runs/{finding['run_id']}").json()
    defn = WORKFLOWS["refund_desk"].build(run["model"])
    trace = TraceV1.model_validate(run["trace"])
    ranked = attribute(trace, evaluate_checks(trace, defn.checks, defn.truth()), finding["symptom_step"])
    assert [h.step_id for h in ranked] == [h["step_id"] for h in finding["hypotheses"]]
    assert run["injected_fault"]["target_step"] == "s2"  # ground truth stored, separately


def test_fr_run_03_recorded_mode_gives_byte_identical_step_outputs_across_three_runs(client, example):
    dumps = []
    for _ in range(3):
        run = start_run(client, example, "stale_price")["run"]
        dumps.append(json.dumps([s["outputs"] for s in run["trace"]["steps"]], sort_keys=True))
    assert dumps[0] == dumps[1] == dumps[2]


def test_fr_run_04_unreachable_model_ends_errored_within_35_seconds_and_defaults_are_set(make_client, example):
    c = make_client(llm_mode="live", ollama_url="http://127.0.0.1:9")
    t0 = time.monotonic()
    run = start_run(c, example)["run"]
    assert time.monotonic() - t0 < 35
    assert run["status"] == "errored" and "unreachable" in run["error"]
    assert build_provider(Settings(), "live").timeout == 120.0  # local CPU model: slow calls are normal
    hosted = build_provider(Settings(openai_base_url="http://x", openai_api_key="k"), "live")
    assert hosted.timeout == 30.0  # the plan's default per call


def test_fr_chk_06_truth_evidence_stores_query_response_and_data_snapshot(client, example):
    finding = open_finding(client, example)
    ev = next(e for e in finding["evidence"] if e["type"] == "check_computation")
    call = ev["payload"]["computation"]["truth_calls"][0]
    assert call["function"] == "catalog_total" and call["returned"] == ev["payload"]["expected"]
    assert ev["payload"]["data_snapshot"] == "taubench_retail_v1"


def test_fr_rev_01_request_info_and_accepting_an_inconclusive_finding_need_a_comment(client, example):
    finding = open_finding(client, example)
    url = f"/api/findings/{finding['id']}/reviews"
    assert client.post(url, json={"decision": "request_info", "comment": "Please explain more"}).status_code == 409  # not yet verified
    verify(client, hypothesis_for(finding, "s2")["id"])
    assert client.post(url, json={"decision": "request_info"}).status_code == 422
    ok = client.post(url, json={"decision": "request_info", "comment": "Which catalogue version was used?"})
    assert ok.status_code == 201 and ok.json()["from_status"] == ok.json()["to_status"] == "confirmed"
    assert "accept" in client.get(f"/api/findings/{finding['id']}").json()["allowed_actions"]
    with session_scope(db_of(client)) as s:
        s.get(Finding, finding["id"]).status = "inconclusive"
    assert client.post(url, json={"decision": "accept"}).status_code == 422
    done = client.post(url, json={"decision": "accept", "comment": "Replays were close to the threshold; accepting."})
    assert done.status_code == 201 and done.json()["to_status"] == "accepted"


def test_fr_rev_02_every_transition_is_written_to_the_audit_log(client, example):
    finding = open_finding(client, example)
    verify(client, hypothesis_for(finding, "s2")["id"])
    client.post(f"/api/findings/{finding['id']}/reviews", json={"decision": "accept", "reviewer": "Shahoud"})
    with session_scope(db_of(client)) as s:
        rows = s.query(AuditLog).filter_by(entity_id=finding["id"], action="finding_transition").order_by(AuditLog.id).all()
        events = [(r.detail["event"], r.actor) for r in rows]
    assert [e for e, _ in events] == ["hypotheses_ready", "verify_started", "verdict_confirmed", "review_accept"]
    assert events[-1][1] == "Shahoud"


def test_fr_rep_01_report_is_available_as_markdown_and_json_with_evidence_hashes(client, example):
    finding = open_finding(client, example)
    verify(client, hypothesis_for(finding, "s2")["id"])
    doc = client.get(f"/api/findings/{finding['id']}/report", params={"format": "json"}).json()
    md = client.get(f"/api/findings/{finding['id']}/report").text
    run = client.get(f"/api/runs/{finding['run_id']}").json()
    assert doc["run"]["trace_sha256"] == run["trace_sha256"] and doc["finding"]["status"] == "confirmed"
    for ev in doc["finding"]["evidence"]:
        assert client.get(f"/api/evidence/{ev['id']}").json()["sha256"] == ev["sha256"] and ev["sha256"] in md
    assert client.get(f"/api/findings/{finding['id']}/report", params={"format": "pdf"}).status_code == 422


def test_fr_his_01_runs_and_findings_can_be_filtered_searched_and_paged(client, example):
    start_run(client, example)
    a = start_run(client, example, "stale_price")["run"]
    assert len(client.get("/api/runs", params={"fault": "none"}).json()) == 1
    assert len(client.get("/api/runs", params={"fault": "stale_price"}).json()) == 1
    assert len(client.get("/api/runs", params={"q": example["order_id"].lower()}).json()) == 2
    assert client.get("/api/runs", params={"q": "no-such-order"}).json() == []
    assert len(client.get("/api/runs", params={"limit": 1}).json()) == 1
    f = lambda **p: client.get("/api/findings", params=p).json()  # noqa: E731
    assert len(f(severity="high")) == 1 and f(severity="low") == [] and len(f(level="V1")) == 1 and f(level="V2") == []
    assert len(f(q="stated refund")) == 1 and f(q="zzz") == [] and len(f(run_id=a["id"])) == 1
    assert f(created_after="2999-01-01T00:00:00Z") == [] and len(f(created_before="2999-01-01T00:00:00Z")) == 1
    limit = next(p for p in client.get("/openapi.json").json()["paths"]["/api/findings"]["get"]["parameters"] if p["name"] == "limit")
    assert limit["schema"]["default"] == 25
