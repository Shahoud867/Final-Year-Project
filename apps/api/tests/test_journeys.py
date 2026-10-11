"""End-to-end journeys through the HTTP API (SYS-CORE J1/J2): run, detect, trace, verify, review, report."""

from __future__ import annotations

from tests.conftest import hypothesis_for, open_finding, start_run, verify


def test_workflow_catalogue_and_examples(client):
    wf = client.get("/api/workflows").json()[0]
    assert wf["key"] == "refund_desk" and [s["id"] for s in wf["steps"]] == ["s1", "s2", "s3", "s4", "s5"]
    assert len(wf["checks"]) == 7 and wf["faults"] == ["stale_price"]
    examples = client.get("/api/workflows/refund_desk/examples").json()
    assert len(examples) == 12 and all("order_id" in e and "email" in e for e in examples)


def test_clean_run_has_no_findings_and_all_checks_pass(client, example):
    out = start_run(client, example)
    run = out["run"]
    assert run["status"] == "completed" and run["llm_mode"] == "recorded" and run["findings"] == []
    assert run["injected_fault"] is None and {c["status"] for c in run["check_results"]} == {"pass"}
    assert run["trace_sha256"] and len(run["trace"]["steps"]) == 5
    job = client.get(f"/api/jobs/{out['job_id']}").json()
    assert job["status"] == "succeeded" and job["progress_done"] == job["progress_total"] == 1


def test_graph_shows_steps_edges_and_failed_nodes(client, example):
    run_id = start_run(client, example, "stale_price")["run_id"]
    g = client.get(f"/api/runs/{run_id}/graph").json()
    status = {n["id"]: n["status"] for n in g["nodes"]}
    assert set(status) == {"task", "s1", "s2", "s3", "s4", "s5"}
    assert status["s2"] == "failed" and status["s1"] == "ok"
    assert {"source": "s2", "target": "s3", "field": "items"} in g["edges"]
    assert any(e["source"] == "task" and e["target"] == "s1" for e in g["edges"])


def test_stale_price_run_opens_one_silent_failure_with_ranked_hypotheses_and_hashed_evidence(client, example):
    run = start_run(client, example, "stale_price")["run"]
    assert run["status"] == "completed" and run["fault_type"] == "stale_price"
    assert run["injected_fault"]["target_step"] == "s2"  # ground truth is stored, but only for scoring
    finding = open_finding(client, example)
    assert finding["kind"] == "silent_failure" and finding["status"] == "hypothesized"
    assert finding["verification_level"] == "V1" and finding["check_id"] == "CHK-OUT-1"
    top = finding["hypotheses"][0]
    assert (top["rank"], top["step_id"], top["method"]) == (1, "s2", "provenance") and top["can_verify"]
    assert "verify" in finding["allowed_actions"]
    assert len(finding["evidence"]) >= 4 and all(e["hash_valid"] and len(e["sha256"]) == 64 for e in finding["evidence"])


def test_confirming_the_true_origin_gives_v2_and_controls_stay_broken(client, example):
    finding = open_finding(client, example)
    exp = verify(client, hypothesis_for(finding, "s2")["id"])
    assert exp["status"] == "done" and exp["verdict"] == "confirmed" and exp["rule_version"] == "VR-1"
    s = exp["summary"]
    assert (s["k_pass"], s["n_completed"], s["c_pass"], s["m_completed"]) == (5, 5, 0, 2)
    assert len(exp["replays"]) == 7 and {r["kind"] for r in exp["replays"]} == {"intervention", "control"}
    after = client.get(f"/api/findings/{finding['id']}").json()
    assert after["status"] == "confirmed" and after["verification_level"] == "V2"
    assert any(e["type"] == "verdict_computation" for e in after["evidence"])
    assert after["allowed_actions"] == ["accept", "reject", "request_info"]


def test_refuting_an_innocent_step_then_confirming_the_origin(client, example):  # SYS-CORE J2
    finding = open_finding(client, example)
    wrong = verify(client, hypothesis_for(finding, "s4")["id"])
    assert wrong["verdict"] == "refuted" and wrong["summary"]["k_pass"] == 0
    mid = client.get(f"/api/findings/{finding['id']}").json()
    assert mid["status"] == "refuted" and "verify" in mid["allowed_actions"]
    right = verify(client, hypothesis_for(mid, "s2")["id"])
    assert right["verdict"] == "confirmed"
    final = client.get(f"/api/findings/{finding['id']}").json()
    assert final["status"] == "confirmed"
    assert [h["status"] for h in final["hypotheses"] if h["step_id"] in ("s2", "s4")] == ["confirmed", "refuted"]


def test_review_workflow_accept_then_resolve_and_report(client, example):
    finding = open_finding(client, example)
    verify(client, hypothesis_for(finding, "s2")["id"])
    ok = client.post(f"/api/findings/{finding['id']}/reviews", json={"decision": "accept", "reviewer": "Shahoud"})
    assert ok.status_code == 201 and ok.json()["to_status"] == "accepted"
    done = client.post(f"/api/findings/{finding['id']}/reviews", json={"decision": "resolve", "comment": "price cache fixed"})
    assert done.json()["to_status"] == "resolved"
    final = client.get(f"/api/findings/{finding['id']}").json()
    assert final["status"] == "resolved" and final["verification_level"] == "V3" and final["allowed_actions"] == []
    assert [r["decision"] for r in final["reviews"]] == ["accept", "resolve"]
    report = client.get(f"/api/findings/{finding['id']}/report")
    assert report.status_code == 200 and report.headers["content-type"].startswith("text/markdown")
    for needle in (finding["id"], "confirmed", "VR-1", "price cache fixed", final["evidence"][0]["sha256"]):
        assert needle in report.text


def test_findings_can_be_listed_and_filtered(client, example):
    open_finding(client, example)
    start_run(client, example)  # clean run adds no finding
    assert len(client.get("/api/findings").json()) == 1
    assert len(client.get("/api/findings", params={"status": "hypothesized"}).json()) == 1
    assert client.get("/api/findings", params={"status": "resolved"}).json() == []
    assert client.get("/api/findings/summary").json() == {"hypothesized": 1}
    assert len(client.get("/api/runs").json()) == 2


def test_unrecorded_task_in_recorded_mode_fails_with_a_helpful_message(client, example):
    task = {**example, "message": "Please return the Luggage Set from order " + example["order_id"] + " today."}
    run = start_run(client, task)["run"]
    assert run["status"] == "errored" and "never recorded" in run["error"] and "live mode" in run["error"]
    assert run["findings"][0]["kind"] == "explicit_error"


def test_evidence_is_listed_in_the_order_an_investigation_unfolds(client, example):
    finding = open_finding(client, example)
    verify(client, hypothesis_for(finding, "s2")["id"])
    types = [e["type"] for e in client.get(f"/api/findings/{finding['id']}").json()["evidence"]]
    assert types[0] == "check_computation" and types[1] == "step_snapshot"
    assert types.index("provenance_path") < types.index("verdict_computation") < types.index("replay_output")
    assert types[-1] == "diff"


def test_a_replay_with_no_recorded_answer_gives_no_verdict_and_says_why(client, example):
    """Edge case found in a live walkthrough: recorded mode cannot run controls it never recorded.

    The product must not guess: the verdict is "error", the reason is stated, and the finding can be verified again.
    """
    finding = open_finding(client, example)
    intake = hypothesis_for(finding, "s1")
    exp = verify(client, intake["id"])
    assert exp["verdict"] == "error" and exp["summary"]["m_completed"] == 0
    assert "not in the recording" in exp["summary"]["explanation"]
    after = client.get(f"/api/findings/{finding['id']}").json()
    assert after["status"] == "hypothesized" and "verify" in after["allowed_actions"]
