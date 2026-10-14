"""Validation, errors, security, resilience (SYS-ERR, NFR-SEC, NFR-REL)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from granite_api.config import Settings
from granite_api.db import Base, make_engine, make_session_factory, session_scope
from granite_api.jobs import recover_interrupted
from granite_api.models import Evidence, Experiment, Finding, Job, Project, Run
from tests.conftest import hypothesis_for, open_finding, start_run, verify


def post_run(client, body):
    return client.post("/api/runs", json=body)


def factory_of(client):
    return make_session_factory(client.app.state.session_factory.kw["bind"])


class TestValidation:
    def test_bad_email_and_order_id_are_reported_per_field(self, client, example):
        r = post_run(client, {"task_input": {**example, "email": "not-an-email", "order_id": "12"}})
        assert r.status_code == 422 and r.headers["content-type"].startswith("application/problem+json")
        fields = {e["field"] for e in r.json()["errors"]}
        assert {"email", "order_id"} <= fields

    def test_empty_message_and_extra_keys_are_rejected(self, client, example):
        assert post_run(client, {"task_input": {**example, "message": ""}}).status_code == 422
        assert post_run(client, {"task_input": {**example, "admin": True}}).status_code == 422
        assert post_run(client, {"task_input": example, "surprise": 1}).status_code == 422

    def test_oversized_message_is_rejected(self, client, example):
        assert post_run(client, {"task_input": {**example, "message": "x" * 2001}}).status_code == 422

    def test_unknown_workflow_and_fault(self, client, example):
        assert post_run(client, {"workflow": "nope", "task_input": example}).status_code == 404
        r = post_run(client, {"task_input": example, "fault": "cosmic_ray"})
        assert r.status_code == 422 and "stale_price" in r.json()["detail"]

    @pytest.mark.parametrize("body", [{"n": 0}, {"n": 11}, {"m": 6}, {"m": -1}, {"n": "five"}])
    def test_experiment_limits(self, client, example, body):
        finding = open_finding(client, example)
        hyp = hypothesis_for(finding, "s2")["id"]
        assert client.post(f"/api/hypotheses/{hyp}/experiments", json=body).status_code == 422

    def test_pagination_bounds(self, client):
        assert client.get("/api/runs", params={"limit": 101}).status_code == 422
        assert client.get("/api/runs", params={"offset": -1}).status_code == 422


class TestNotFoundAndState:
    @pytest.mark.parametrize(
        "path",
        ["runs/run_x", "runs/run_x/graph", "findings/fnd_x", "findings/fnd_x/report", "experiments/exp_x",
         "evidence/ev_x", "jobs/job_x"],
    )
    def test_unknown_ids_are_404_problems_with_request_id(self, client, path):
        r = client.get(f"/api/{path}")
        body = r.json()
        assert r.status_code == 404 and body["status"] == 404 and body["request_id"]
        assert body["instance"].endswith(path)

    def test_unknown_hypothesis_and_finding_for_writes(self, client):
        assert client.post("/api/hypotheses/hyp_x/experiments", json={}).status_code == 404
        assert client.post("/api/findings/fnd_x/reviews", json={"decision": "accept"}).status_code == 404

    def test_review_rules(self, client, example):
        finding = open_finding(client, example)
        fid = finding["id"]
        url = f"/api/findings/{fid}/reviews"
        assert client.post(url, json={"decision": "accept"}).status_code == 409  # nothing verified yet
        verify(client, hypothesis_for(finding, "s2")["id"])
        assert client.post(url, json={"decision": "reject"}).status_code == 422
        assert client.post(url, json={"decision": "reject", "comment": "no"}).status_code == 422
        rejected = client.post(url, json={"decision": "reject", "comment": "price is correct"})
        assert rejected.status_code == 201 and rejected.json()["to_status"] == "rejected"
        again = client.post(url, json={"decision": "accept"})
        assert again.status_code == 409 and again.json()["allowed_actions"] == []
        assert client.post(url, json={"decision": "bogus"}).status_code == 422

    def test_cannot_verify_again_after_confirmation(self, client, example):
        finding = open_finding(client, example)
        hyp = hypothesis_for(finding, "s2")["id"]
        verify(client, hyp)
        again = client.post(f"/api/hypotheses/{hyp}/experiments", json={})
        assert again.status_code == 409 and "confirmed" in again.json()["detail"]

    def test_step_without_a_repair_cannot_be_verified(self, client, example):
        finding = open_finding(client, example)
        blind = next(h for h in finding["hypotheses"] if not h["can_verify"])
        r = client.post(f"/api/hypotheses/{blind['id']}/experiments", json={})
        assert r.status_code == 422 and "no repair" in r.json()["detail"]
        assert client.get(f"/api/findings/{finding['id']}").json()["status"] == "hypothesized"


class TestSecurity:
    def test_security_headers_and_request_id(self, client):
        r = client.get("/api/health")
        assert r.headers["x-content-type-options"] == "nosniff" and r.headers["x-frame-options"] == "DENY"
        assert "default-src" in r.headers["content-security-policy"] and r.headers["x-request-id"]

    def test_token_protects_everything_except_health(self, make_client, example):
        c = make_client(api_token="s3cret-token")
        assert c.get("/api/health").json()["auth_required"] is True
        for method, path in (("get", "/api/runs"), ("get", "/api/workflows"), ("post", "/api/runs")):
            r = getattr(c, method)(path)
            assert r.status_code == 401 and r.headers["content-type"].startswith("application/problem+json")
        assert c.get("/api/runs", headers={"Authorization": "Bearer wrong"}).status_code == 401
        good = {"Authorization": "Bearer s3cret-token"}
        assert c.get("/api/runs", headers=good).status_code == 200
        assert c.post("/api/runs", json={"task_input": example}, headers=good).status_code == 202

    def test_non_ascii_credentials_are_rejected_not_a_server_error(self, make_client):
        c = make_client(api_token="s3cret-token")
        bad = b"Bearer s3cr" + bytes([0xE9]) + b"t"  # a non-ASCII byte in the header
        r = c.get("/api/runs", headers={"Authorization": bad})
        assert r.status_code == 401

    def test_oversized_request_bodies_are_refused_before_parsing(self, client, example):
        r = client.post("/api/runs", content=b"{" + b" " * 300_000 + b"}", headers={"Content-Type": "application/json"})
        assert r.status_code == 413 and r.json()["title"] == "Request too large"

    def test_rate_limit_applies_to_changes_not_reads(self, make_client, example):
        c = make_client(rate_limit_per_minute=3)
        codes = [post_run(c, {"task_input": {**example, "email": "bad"}}).status_code for _ in range(4)]
        assert codes == [422, 422, 422, 429]
        limited = post_run(c, {"task_input": example})
        assert limited.headers["retry-after"] and limited.json()["title"] == "Too many requests"
        assert c.get("/api/runs").status_code == 200

    def test_evidence_has_no_write_endpoints_and_tampering_is_detected(self, client, example):
        finding = open_finding(client, example)
        ev = finding["evidence"][0]
        for method in ("put", "patch", "delete"):
            assert getattr(client, method)(f"/api/evidence/{ev['id']}").status_code == 405
        with session_scope(factory_of(client)) as s:
            row = s.get(Evidence, ev["id"])
            row.payload = {**row.payload, "tampered": True}
        assert client.get(f"/api/evidence/{ev['id']}").json()["hash_valid"] is False
        rest = [e for e in client.get(f"/api/findings/{finding['id']}").json()["evidence"] if e["id"] != ev["id"]]
        assert all(e["hash_valid"] for e in rest)

    def test_unexpected_errors_do_not_leak_internals(self, client):
        quiet = TestClient(client.app, raise_server_exceptions=False)
        client.app.state.session_factory = None  # break the app on purpose
        r = quiet.get("/api/runs")
        assert r.status_code == 500 and r.json()["title"] == "Internal error"
        assert "Traceback" not in r.text and "NoneType" not in r.text


class TestResilience:
    def test_model_endpoint_down_gives_an_errored_run_and_a_finding_not_a_crash(self, make_client, example):
        c = make_client(llm_mode="live", ollama_url="http://127.0.0.1:9", llm_timeout_s=1.0)
        out = start_run(c, example)
        assert out["run"]["status"] == "errored" and "unreachable" in out["run"]["error"]
        assert out["run"]["findings"][0]["kind"] == "explicit_error"
        assert c.get(f"/api/jobs/{out['job_id']}").json()["status"] == "succeeded"

    def test_test_llm_endpoint_reports_both_modes(self, make_client):
        assert make_client().post("/api/settings/test-llm").json()["mode"] == "recorded"
        down = make_client(llm_mode="live", ollama_url="http://127.0.0.1:9", llm_timeout_s=1.0)
        r = down.post("/api/settings/test-llm").json()
        assert r["ok"] is False and "unreachable" in r["message"]

    def test_restart_closes_dangling_jobs_and_runs(self, tmp_path):
        engine = make_engine(f"sqlite:///{(tmp_path / 'r.db').as_posix()}")
        Base.metadata.create_all(engine)
        factory = make_session_factory(engine)
        with session_scope(factory) as s:
            s.add(Project(id="prj_refund_desk", name="p", workflow_key="refund_desk"))
            s.add(Run(id="run_1", project_id="prj_refund_desk", workflow_key="refund_desk", status="running",
                      task_input={}))
            s.add(Job(id="job_1", kind="run", target_id="run_1", status="running"))
        assert recover_interrupted(factory) == 1
        with session_scope(factory) as s:
            assert s.get(Run, "run_1").status == "errored" and "restart" in s.get(Run, "run_1").error
            assert s.get(Job, "job_1").status == "failed"

    def test_restart_returns_a_verifying_finding_to_hypothesized(self, client, example):
        finding = open_finding(client, example)
        factory = factory_of(client)
        with session_scope(factory) as s:
            s.get(Finding, finding["id"]).status = "verifying"
            s.add(Experiment(id="exp_1", hypothesis_id=finding["hypotheses"][0]["id"], finding_id=finding["id"],
                             status="running", n=5, m=2))
        recover_interrupted(factory)
        assert client.get(f"/api/findings/{finding['id']}").json()["status"] == "hypothesized"

    def test_same_request_gives_same_step_outputs(self, client, example):
        a = start_run(client, example, "stale_price")["run"]
        b = start_run(client, example, "stale_price")["run"]
        assert [s["outputs"] for s in a["trace"]["steps"]] == [s["outputs"] for s in b["trace"]["steps"]]

    def test_settings_validation(self):
        with pytest.raises(ValueError, match="GRANITE_LLM_MODE"):
            Settings(llm_mode="turbo").validate()
        with pytest.raises(ValueError, match="both"):
            Settings(openai_base_url="http://x").validate()

    def test_model_probe_is_cached_so_health_checks_stay_fast(self, monkeypatch):
        import time

        from granite_api import llm_factory

        calls = []

        def slow_refusal(url, timeout):
            calls.append(timeout)
            raise OSError("refused")

        monkeypatch.setattr(llm_factory.urllib.request, "urlopen", slow_refusal)
        llm_factory._probe_cache.clear()
        settings = Settings(ollama_url="http://127.0.0.1:9")
        t0 = time.monotonic()
        assert [llm_factory.live_available(settings) for _ in range(50)] == [False] * 50
        assert len(calls) == 1 and calls[0] <= 1.0 and time.monotonic() - t0 < 0.5
        assert llm_factory.live_available(settings, max_age=0) is False and len(calls) == 2  # an expired entry probes again
        assert llm_factory.live_available(Settings(openai_base_url="http://x", openai_api_key="k")) is True


def test_the_in_app_guide_states_the_limits_the_server_enforces():
    """Panel action A3: the inputs explained to the user are the ones that are validated (no drift)."""
    from pathlib import Path

    from granite_core.attribution import MAX_HYPOTHESES

    from granite_api.registry import RefundTask as TaskInput
    from granite_api.schemas import ExperimentCreate, ReviewCreate, RunCreate

    guide = (Path(__file__).resolve().parents[3] / "apps" / "web" / "src" / "pages" / "Guide.tsx").read_text(encoding="utf-8")

    def limit(model, field, name):
        return next(getattr(m, name) for m in model.model_fields[field].metadata if hasattr(m, name))

    expected = [
        f"{limit(TaskInput, 'message', 'min_length')} to {limit(TaskInput, 'message', 'max_length')} characters",
        f"at most {limit(TaskInput, 'email', 'max_length')} characters",
        f"0 to {limit(RunCreate, 'seed', 'le'):,}",
        f"N: {limit(ExperimentCreate, 'n', 'ge')} to {limit(ExperimentCreate, 'n', 'le')} (default {ExperimentCreate().n})",
        f"M: {limit(ExperimentCreate, 'm', 'ge')} to {limit(ExperimentCreate, 'm', 'le')} (default {ExperimentCreate().m})",
        f"Comment: at most {limit(ReviewCreate, 'comment', 'max_length')} characters",
        f"{limit(ReviewCreate, 'reviewer', 'min_length')} to {limit(ReviewCreate, 'reviewer', 'max_length')} characters",
        f"Up to {MAX_HYPOTHESES} ranked hypotheses",
    ]
    missing = [text for text in expected if text not in guide]
    assert not missing, f"Guide.tsx no longer matches the server's rules: {missing}"


def _web_source(*parts: str) -> str:
    from pathlib import Path

    return (Path(__file__).resolve().parents[3] / "apps" / "web" / "src").joinpath(*parts).read_text(encoding="utf-8")


def test_the_interface_explains_rule_vr1_with_the_servers_thresholds():
    """Panel action A4: the rule drawn next to a verdict is the rule that decided it (no drift)."""
    import re

    from granite_core import verification as v

    from granite_api.schemas import ExperimentCreate

    source = _web_source("lib", "vr1.ts")

    def constant(name: str) -> str:
        found = re.search(rf"export const {name} = ([^;]+);", source)
        assert found, f"lib/vr1.ts no longer exports {name}"
        return found.group(1).strip().strip('"')

    assert constant("RULE_VERSION") == v.RULE_VERSION
    assert float(constant("CONFIRM_MIN_RATE")) == v.CONFIRM_MIN_RATE
    assert float(constant("CONTROL_MAX_RATE")) == v.CONTROL_MAX_RATE
    assert float(constant("REFUTE_MAX_RATE")) == v.REFUTE_MAX_RATE
    assert int(constant("MAX_REPLAYS")) == v.MAX_REPLAYS and int(constant("MAX_CONTROLS")) == v.MAX_CONTROLS
    assert int(constant("DEFAULT_REPLAYS")) == ExperimentCreate().n and int(constant("DEFAULT_CONTROLS")) == ExperimentCreate().m


def test_the_interface_draws_the_lifecycle_the_server_enforces():
    """Panel action A5: the workflow shown to the user is the state machine in the code (no drift)."""
    import re

    from granite_core.lifecycle import TERMINAL, TRANSITIONS

    from granite_api.services.reviews import AWAITING_REVIEW

    source = _web_source("lib", "lifecycle.ts")
    table = source.split("export const TRANSITIONS", 1)[1].split("];", 1)[0]
    shown = {tuple(row) for row in re.findall(r'\["(\w+)", "(\w+)", "(\w+)"\]', table)}
    assert shown == {(s.value, e.value, to.value) for (s, e), to in TRANSITIONS.items()}

    def names(constant: str) -> set[str]:
        found = re.search(rf"export const {constant} = \[([^\]]*)\];", source)
        assert found, f"lib/lifecycle.ts no longer exports {constant}"
        return set(re.findall(r'"(\w+)"', found.group(1)))

    assert names("AWAITING_REVIEW") == set(AWAITING_REVIEW)
    assert names("TERMINAL") == {s.value for s in TERMINAL}


def test_field_messages_are_plain_sentences(client, example):
    """Panel action A1: the form shows a readable sentence next to the field, not a validator's internal wording."""
    r = post_run(client, {"task_input": {**example, "message": "hi", "order_id": "12"}})
    messages = {e["field"]: e["message"] for e in r.json()["errors"]}
    assert messages == {"message": "Enter at least 3 characters", "order_id": "Must look like #W1234567"}
