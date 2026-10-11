"""System-level test cases: the whole product through its HTTP interface, as a user or a script would reach it.

Each docstring is a test case specification (ID and title, requirement, steps, expected result).
`python scripts/build_test_docs.py` turns these docstrings into docs/manuals/system-test-cases.md, so the document
and the executable tests cannot disagree.
"""

from __future__ import annotations

import json
import threading
import time

import pytest

from .conftest import Client, ServerFactory

own_server = pytest.mark.own_server


# ---- SYS-CORE: the investigation journeys ---------------------------------------------------------------
def test_sys_core_01_silent_failure_is_detected_traced_verified_reviewed_and_reported(api: Client) -> None:
    """SYS-CORE-01 Full investigation of a silent failure (journey J1).

    Requirement: FR-RUN-01, FR-RUN-02, FR-CHK-04, FR-ATT-01, FR-VER-01, FR-VER-02, FR-REV-01, FR-REP-01
    Steps: run the first example with the stale-price fault; open its finding; verify the first-ranked step with 5 replays and 2 controls; accept; mark resolved; export the report as Markdown and JSON.
    Expected: the run completes with exactly one silent-failure finding; rank 1 is the Order Lookup step (s2); the verdict is CONFIRMED with 5 of 5 replays and 0 of 2 controls passing; the finding ends resolved at level V3; both reports contain every evidence hash.
    """
    run = api.run(api.example(), "stale_price")
    assert run["status"] == "completed" and run["fault_type"] == "stale_price"
    finding = api.finding_of(run)
    assert finding["kind"] == "silent_failure" and finding["status"] == "hypothesized"
    assert finding["hypotheses"][0]["step_id"] == "s2" == run["injected_fault"]["target_step"]
    exp = api.verify(finding, "s2")
    assert exp["verdict"] == "confirmed" and exp["rule_version"] == "VR-1"
    s = exp["summary"]
    assert (s["k_pass"], s["n_completed"], s["c_pass"], s["m_completed"]) == (5, 5, 0, 2)
    url = f"/api/findings/{finding['id']}"
    assert api.get(url).json()["verification_level"] == "V2"
    assert api.post(url + "/reviews", {"decision": "accept", "reviewer": "system-test"}).status == 201
    assert api.post(url + "/reviews", {"decision": "resolve", "comment": "lookup cache fixed"}).status == 201
    final = api.get(url).json()
    assert final["status"] == "resolved" and final["verification_level"] == "V3" and final["allowed_actions"] == []
    md = api.get(url + "/report").text
    doc = api.get(url + "/report?format=json").json()
    assert all(e["sha256"] in md and e["hash_valid"] for e in doc["finding"]["evidence"]) and len(doc["finding"]["evidence"]) >= 6


def test_sys_core_02_clean_run_opens_no_finding(api: Client) -> None:
    """SYS-CORE-02 A clean run raises no alarm (journey J2).

    Requirement: FR-CHK-01, FR-CHK-04, NFR-06
    Steps: run the first example without a fault.
    Expected: the run completes; all seven checks pass; no finding is opened; no injected-fault record exists.
    """
    run = api.run(api.example())
    assert run["status"] == "completed" and run["findings"] == [] and run["injected_fault"] is None
    assert len(run["check_results"]) == 7 and {c["status"] for c in run["check_results"]} == {"pass"}


def test_sys_core_03_innocent_step_is_refuted_then_the_origin_is_confirmed(api: Client) -> None:
    """SYS-CORE-03 Refute a wrong hypothesis, then confirm the right one.

    Requirement: FR-VER-01, FR-VER-02, FR-REV-02
    Steps: run the first example with the fault; verify the Refund Calculator step (s4); then verify the Order Lookup step (s2).
    Expected: s4 is REFUTED with 0 replays passing and the finding becomes 'refuted' but can still be verified; s2 is then CONFIRMED and the finding becomes 'confirmed'.
    """
    finding = api.finding_of(api.run(api.example(), "stale_price"))
    wrong = api.verify(finding, "s4")
    assert wrong["verdict"] == "refuted" and wrong["summary"]["k_pass"] == 0
    mid = api.get(f"/api/findings/{finding['id']}").json()
    assert mid["status"] == "refuted" and "verify" in mid["allowed_actions"]
    assert api.verify(mid, "s2")["verdict"] == "confirmed"
    assert api.get(f"/api/findings/{finding['id']}").json()["status"] == "confirmed"


def test_sys_core_04_run_graph_shows_where_checks_failed(api: Client) -> None:
    """SYS-CORE-04 The run graph marks the failing steps.

    Requirement: FR-RUN-01, FR-CHK-01
    Steps: run the first example with the fault; request the run graph.
    Expected: the graph has the task input and five steps; s2 is marked failed and s1 is ok; the edge s2 to s3 carries the field 'items'.
    """
    run = api.run(api.example(), "stale_price")
    g = api.get(f"/api/runs/{run['id']}/graph").json()
    status = {n["id"]: n["status"] for n in g["nodes"]}
    assert set(status) == {"task", "s1", "s2", "s3", "s4", "s5"} and status["s2"] == "failed" and status["s1"] == "ok"
    assert {"source": "s2", "target": "s3", "field": "items"} in g["edges"]


def test_sys_core_05_history_can_be_filtered_and_searched(api: Client) -> None:
    """SYS-CORE-05 Runs and findings can be found again.

    Requirement: FR-HIS-01
    Steps: create a faulty run; list runs filtered by fault and by text; list findings filtered by severity, level, run and text.
    Expected: each filter returns the new records; a filter that cannot match returns an empty list; page size is honoured.
    """
    task = api.example(1)
    run = api.run(task, "stale_price")
    assert any(r["id"] == run["id"] for r in api.get("/api/runs?fault=stale_price&limit=100").json())
    assert all(r["fault_type"] is None for r in api.get("/api/runs?fault=none&limit=100").json())
    assert any(r["id"] == run["id"] for r in api.get(f"/api/runs?q={task['order_id'][1:]}&limit=100").json())
    assert len(api.get("/api/runs?limit=1").json()) == 1
    assert len(api.get(f"/api/findings?run_id={run['id']}&severity=high&level=V1&q=refund").json()) == 1
    assert api.get(f"/api/findings?run_id={run['id']}&severity=low").json() == []
    assert api.get("/api/findings?q=no-such-text-anywhere").json() == []


def test_sys_core_06_api_documents_itself(api: Client) -> None:
    """SYS-CORE-06 The interface is documented by the running system.

    Requirement: panel action A3 (inputs of each feature)
    Steps: fetch the OpenAPI description and the interactive documentation page.
    Expected: the description lists the run, finding, experiment, review, evidence and job endpoints with a summary for each; the documentation page loads.
    """
    spec = api.get("/openapi.json").json()
    for path in ("/api/runs", "/api/findings/{finding_id}", "/api/hypotheses/{hypothesis_id}/experiments",
                 "/api/findings/{finding_id}/reviews", "/api/evidence/{evidence_id}", "/api/jobs/{job_id}"):
        assert path in spec["paths"], path
    described = [op.get("description") for item in spec["paths"].values() for op in item.values()]
    assert all(described), "every endpoint has a description"
    assert api.get("/docs").status == 200


def test_sys_core_07_web_ui_is_served_with_the_api(api: Client, has_ui: bool) -> None:
    """SYS-CORE-07 The web interface is delivered by the same server.

    Requirement: faculty requirement (core module on the live interface)
    Steps: request the root page, the script it references, and an application route.
    Expected: the page and its script load; an unknown application path falls back to the page (single-page routing).
    """
    if not has_ui:
        pytest.skip("this server was started without a built web UI (GRANITE_STATIC_DIR)")
    page = api.get("/").text
    script = page.split('src="', 1)[1].split('"', 1)[0]
    assert api.get(script).status == 200
    assert '<div id="root">' in api.get("/findings/anything").text


# ---- SYS-ERR: failure and edge cases --------------------------------------------------------------------
def test_sys_err_01_invalid_input_is_refused_field_by_field(api: Client) -> None:
    """SYS-ERR-01 Invalid input is refused with one message per field.

    Requirement: panel action A3, NFR-04
    Steps: submit a run with a malformed e-mail and order id; with an unknown key; with an unknown fault; with a message of 2001 characters.
    Expected: each is refused (422) in the RFC 7807 problem format with a request id; the first names both fields; nothing is stored.
    """
    task = api.example()
    before = len(api.get("/api/runs?limit=100").json())
    r = api.post("/api/runs", {"task_input": {**task, "email": "not-an-email", "order_id": "12"}})
    assert r.status == 422 and r.headers["content-type"].startswith("application/problem+json")
    assert {"email", "order_id"} <= {e["field"] for e in r.json()["errors"]} and r.json()["request_id"]
    assert api.post("/api/runs", {"task_input": {**task, "admin": True}}).status == 422
    assert api.post("/api/runs", {"task_input": task, "fault": "cosmic_ray"}).status == 422
    assert api.post("/api/runs", {"task_input": {**task, "message": "x" * 2001}}).status == 422
    assert len(api.get("/api/runs?limit=100").json()) == before


def test_sys_err_02_unknown_records_are_reported_cleanly(api: Client) -> None:
    """SYS-ERR-02 Asking for something that does not exist.

    Requirement: NFR-04
    Steps: request an unknown run, finding, experiment, evidence record and job.
    Expected: each answers 404 in the problem format, with no stack trace.
    """
    for path in ("/api/runs/run_missing", "/api/findings/fnd_missing", "/api/experiments/exp_missing",
                 "/api/evidence/ev_missing", "/api/jobs/job_missing"):
        r = api.get(path)
        assert r.status == 404 and r.json()["status"] == 404 and "Traceback" not in r.text, path


def test_sys_err_03_actions_out_of_order_are_refused(api: Client) -> None:
    """SYS-ERR-03 The lifecycle cannot be skipped.

    Requirement: FR-REV-02
    Steps: on a new finding, try to accept before any verification; verify and confirm; try to verify again; reject without a comment; reject with a comment; try to accept afterwards.
    Expected: accepting too early is refused (409); verifying after confirmation is refused (409); a reject without a reason is refused (422); after a valid reject no further action is allowed.
    """
    finding = api.finding_of(api.run(api.example(), "stale_price"))
    url = f"/api/findings/{finding['id']}/reviews"
    assert api.post(url, {"decision": "accept"}).status == 409
    api.verify(finding, "s2")
    hyp = next(h for h in finding["hypotheses"] if h["step_id"] == "s2")
    assert api.post(f"/api/hypotheses/{hyp['id']}/experiments", {"n": 5, "m": 2}).status == 409
    assert api.post(url, {"decision": "reject"}).status == 422
    assert api.post(url, {"decision": "reject", "comment": "the catalogue price was right"}).status == 201
    again = api.post(url, {"decision": "accept"})
    assert again.status == 409 and again.json()["allowed_actions"] == []


def test_sys_err_04_task_without_recorded_answers_fails_helpfully(api: Client) -> None:
    """SYS-ERR-04 Recorded mode cannot answer a task nobody recorded.

    Requirement: FR-RUN-03, FR-RUN-04
    Steps: in recorded mode, run a task whose message was never recorded.
    Expected: the run ends 'errored' (the server keeps working); the message says the request was never recorded and suggests live mode; an explicit-error finding is opened.
    """
    task = api.example()
    run = api.run({**task, "message": task["message"] + " Thank you very much."})
    assert run["status"] == "errored" and "never recorded" in run["error"] and "live mode" in run["error"]
    assert run["findings"][0]["kind"] == "explicit_error"
    assert api.get("/api/health").json()["status"] == "ok"


def test_sys_err_05_step_without_a_repair_rule_cannot_be_verified(api: Client) -> None:
    """SYS-ERR-05 A hypothesis that cannot be tested is refused, not guessed.

    Requirement: FR-VER-01
    Steps: on a new finding, ask to verify a hypothesis whose step has no repair rule (Policy or Writer).
    Expected: refused (422) with an explanation; the finding keeps its status.
    """
    finding = api.finding_of(api.run(api.example(), "stale_price"))
    blind = next(h for h in finding["hypotheses"] if not h["can_verify"])
    r = api.post(f"/api/hypotheses/{blind['id']}/experiments", {})
    assert r.status == 422 and "no repair" in r.json()["detail"]
    assert api.get(f"/api/findings/{finding['id']}").json()["status"] == "hypothesized"


def test_sys_err_06_oversized_and_out_of_range_requests_are_refused(api: Client) -> None:
    """SYS-ERR-06 Limits are enforced.

    Requirement: NFR-07
    Steps: send a request body just over the 256 kB limit; ask for 11 replays; ask for a page of 101 items.
    Expected: the oversized body is refused before it is parsed (413, or the server closes the connection while the client is still sending); 422 for the replay count and the page size; the server stays healthy.
    """
    before = len(api.get("/api/runs?limit=100").json())
    assert api.call("POST", "/api/runs", raw=b"{" + b" " * 257_000 + b"}").status in (413, 0)
    assert api.get("/api/health").json()["status"] == "ok" and len(api.get("/api/runs?limit=100").json()) == before
    finding = api.finding_of(api.run(api.example(), "stale_price"))
    hyp = finding["hypotheses"][0]["id"]
    assert api.post(f"/api/hypotheses/{hyp}/experiments", {"n": 11}).status == 422
    assert api.get("/api/runs?limit=101").status == 422


@own_server
def test_sys_err_07_unreachable_model_gives_an_errored_run_not_a_crash(start_server: ServerFactory) -> None:
    """SYS-ERR-07 The language model is down.

    Requirement: FR-RUN-04, NFR-04
    Steps: start a server in live mode pointing at a closed port; run a task; then ask the server for its health.
    Expected: the run ends 'errored' within 35 seconds with a message that the model endpoint is unreachable; an explicit-error finding is opened; the server stays healthy.
    """
    c = Client(start_server(GRANITE_LLM_MODE="live", GRANITE_OLLAMA_URL="http://127.0.0.1:9", GRANITE_LLM_TIMEOUT="2").base)
    t0 = time.monotonic()
    accepted = c.post("/api/runs", {"task_input": c.example(), "mode": "live"}).json()
    assert c.wait_job(accepted["job_id"])["status"] == "succeeded"
    run = c.get(f"/api/runs/{accepted['run_id']}").json()
    assert time.monotonic() - t0 < 35
    assert run["status"] == "errored" and "unreachable" in run["error"] and run["findings"][0]["kind"] == "explicit_error"
    assert c.get("/api/health").json()["status"] == "ok"


# ---- SYS-SEC: security --------------------------------------------------------------------------------
def test_sys_sec_01_security_headers_are_sent(api: Client) -> None:
    """SYS-SEC-01 Every response carries the security headers.

    Requirement: NFR-07
    Steps: request the health endpoint.
    Expected: X-Content-Type-Options, X-Frame-Options, Referrer-Policy, a Content-Security-Policy and a request id are present.
    """
    h = api.get("/api/health").headers
    assert h["x-content-type-options"] == "nosniff" and h["x-frame-options"] == "DENY" and h["referrer-policy"] == "no-referrer"
    assert "default-src 'self'" in h["content-security-policy"] and h["x-request-id"]


def test_sys_sec_02_evidence_cannot_be_changed_through_the_api(api: Client) -> None:
    """SYS-SEC-02 Evidence is append-only.

    Requirement: panel action A4 (how results are captured)
    Steps: take an evidence record of a finding; try to PUT, PATCH and DELETE it; read it again.
    Expected: each write is refused (405); the record is unchanged and its hash still matches.
    """
    finding = api.finding_of(api.run(api.example(), "stale_price"))
    ev = finding["evidence"][0]
    for method in ("PUT", "PATCH", "DELETE"):
        assert api.call(method, f"/api/evidence/{ev['id']}", {"payload": {}}).status == 405
    again = api.get(f"/api/evidence/{ev['id']}").json()
    assert again["sha256"] == ev["sha256"] and again["hash_valid"] is True


def test_sys_sec_03_injected_fault_is_not_part_of_the_analysis(api: Client) -> None:
    """SYS-SEC-03 Ground truth stays out of the evidence.

    Requirement: FR-RUN-02
    Steps: run with the fault; read the finding's hypotheses and evidence.
    Expected: the fault record is available on the run for scoring, but no hypothesis or evidence payload mentions the fault type or its note.
    """
    run = api.run(api.example(), "stale_price")
    finding = api.finding_of(run)
    blob = json.dumps([finding["hypotheses"], [e["payload"] for e in finding["evidence"]]])
    assert run["injected_fault"]["fault_type"] == "stale_price"
    assert "stale_price" not in blob and run["injected_fault"]["note"] not in blob


@own_server
def test_sys_sec_04_access_token_protects_the_api(start_server: ServerFactory) -> None:
    """SYS-SEC-04 With a token configured, nothing but health is public.

    Requirement: NFR-07
    Steps: start a server with an access token; call the API without a token, with a wrong token and with the right one.
    Expected: 401 without or with a wrong token; 200 with the right one; health stays open and reports that a token is required.
    """
    base = start_server(GRANITE_API_TOKEN="system-test-token").base
    assert Client(base).get("/api/health").json()["auth_required"] is True
    assert Client(base).get("/api/runs").status == 401
    assert Client(base, "wrong").post("/api/runs", {"task_input": {}}).status == 401
    assert Client(base, "system-test-token").get("/api/runs").status == 200


@own_server
def test_sys_sec_05_rate_limit_slows_down_a_flood_of_changes(start_server: ServerFactory) -> None:
    """SYS-SEC-05 Too many state-changing requests are throttled.

    Requirement: NFR-07
    Steps: start a server that allows 3 changes per minute; send 4 POST requests; then a GET.
    Expected: the fourth POST answers 429 with a Retry-After header; reading is not limited.
    """
    c = Client(start_server(GRANITE_RATE_LIMIT="3").base)
    codes = [c.post("/api/runs", {"task_input": {}}).status for _ in range(4)]
    assert codes == [422, 422, 422, 429]
    assert c.post("/api/runs", {"task_input": {}}).headers["retry-after"]
    assert c.get("/api/runs").status == 200


# ---- SYS-REL: reliability -------------------------------------------------------------------------------
@own_server
def test_sys_rel_01_data_survives_a_restart(start_server: ServerFactory, tmp_path_factory: pytest.TempPathFactory) -> None:
    """SYS-REL-01 A restart loses nothing.

    Requirement: NFR-04
    Steps: start a server; run with the fault and confirm the origin; stop the server; start a new one on the same database.
    Expected: the run, its trace hash, the finding, its status and its evidence are served unchanged by the new process.
    """
    db = tmp_path_factory.mktemp("restart") / "granite.db"
    first = start_server(db=db)
    c = Client(first.base)
    run = c.run(c.example(), "stale_price")
    finding = c.finding_of(run)
    c.verify(finding, "s2")
    first.stop()
    c2 = Client(start_server(db=db).base)
    again = c2.get(f"/api/runs/{run['id']}").json()
    f2 = c2.get(f"/api/findings/{finding['id']}").json()
    assert again["trace_sha256"] == run["trace_sha256"] and f2["status"] == "confirmed"
    assert all(e["hash_valid"] for e in f2["evidence"]) and len(f2["evidence"]) > len(finding["evidence"])


def test_sys_rel_02_several_runs_at_once_all_finish(api: Client) -> None:
    """SYS-REL-02 Concurrent work is not lost.

    Requirement: NFR-04
    Steps: submit six runs at the same time from six threads; wait for their jobs.
    Expected: every request is accepted, every job succeeds and every run completes with its own id.
    """
    tasks = [api.example(i % 4) for i in range(6)]
    accepted: list[dict] = []

    def submit(task: dict[str, str]) -> None:
        r = api.post("/api/runs", {"task_input": task, "fault": "stale_price", "mode": "recorded"})
        assert r.status == 202
        accepted.append(r.json())

    threads = [threading.Thread(target=submit, args=(t,)) for t in tasks]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len({a["run_id"] for a in accepted}) == 6
    assert all(api.wait_job(a["job_id"])["status"] == "succeeded" for a in accepted)
    assert all(api.get(f"/api/runs/{a['run_id']}").json()["status"] == "completed" for a in accepted)


def test_sys_rel_03_same_task_gives_the_same_result(api: Client) -> None:
    """SYS-REL-03 Recorded runs are reproducible.

    Requirement: FR-RUN-03, NFR-05
    Steps: run the same faulty task three times.
    Expected: the step outputs of the three runs are identical, and so are the ranked hypotheses.
    """
    runs = [api.run(api.example(), "stale_price") for _ in range(3)]
    outputs = [json.dumps([s["outputs"] for s in r["trace"]["steps"]], sort_keys=True) for r in runs]
    assert outputs[0] == outputs[1] == outputs[2]
    ranks = [[(h["step_id"], h["score"]) for h in api.finding_of(r)["hypotheses"]] for r in runs]
    assert ranks[0] == ranks[1] == ranks[2]
