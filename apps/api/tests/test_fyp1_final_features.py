"""FYP-1 Final features through the HTTP API: Investigate, regression export, Fault Lab batches, evaluation results."""

from __future__ import annotations

import io
import json
import zipfile

from tests.conftest import open_finding, start_run


class TestInvestigate:
    def test_confirms_the_origin_in_one_action_and_stores_each_attempt(self, client, example):
        finding = open_finding(client, example)
        r = client.post(f"/api/findings/{finding['id']}/investigations", json={})
        assert r.status_code == 202, r.text
        inv = client.get(f"/api/investigations/{r.json()['investigation_id']}").json()
        assert inv["status"] == "done" and inv["outcome"] == "confirmed" and inv["confirmed_step"] == "s2"
        assert inv["attempts"][0]["step_id"] == "s2" and inv["attempts"][0]["verdict"] == "confirmed"
        assert inv["replays_used"] == 7 <= inv["budget"]
        after = client.get(f"/api/findings/{finding['id']}").json()
        assert after["status"] == "confirmed" and after["verification_level"] == "V2"
        assert after["investigations"][0]["id"] == inv["id"] and after["can_export_regression"] is True
        exp = after["experiments"][0]
        assert exp["id"] == inv["attempts"][0]["experiment_id"]
        assert exp["intervention"]["source"] == "check" and exp["intervention"]["derived_from"] == ["CT-LOOKUP"]

    def test_refuses_an_impossible_budget_and_a_decided_finding(self, client, example):
        finding = open_finding(client, example)
        r = client.post(f"/api/findings/{finding['id']}/investigations", json={"n": 5, "m": 2, "budget": 5})
        assert r.status_code == 422
        client.post(f"/api/findings/{finding['id']}/investigations", json={})
        client.post(f"/api/findings/{finding['id']}/reviews", json={"decision": "accept"})
        again = client.post(f"/api/findings/{finding['id']}/investigations", json={})
        assert again.status_code == 409

    def test_unknown_finding_and_investigation(self, client):
        assert client.post("/api/findings/fnd_nope/investigations", json={}).status_code == 404
        assert client.get("/api/investigations/inv_nope").status_code == 404


class TestRegressionExport:
    def test_needs_a_confirmed_origin(self, client, example):
        finding = open_finding(client, example)
        r = client.get(f"/api/findings/{finding['id']}/regression")
        assert r.status_code == 409 and "confirmed" in r.json()["detail"]

    def test_zip_holds_case_test_and_readme(self, client, example):
        finding = open_finding(client, example)
        client.post(f"/api/findings/{finding['id']}/investigations", json={})
        r = client.get(f"/api/findings/{finding['id']}/regression")
        assert r.status_code == 200 and r.headers["content-type"] == "application/zip"
        assert "attachment" in r.headers["content-disposition"]
        names = zipfile.ZipFile(io.BytesIO(r.content)).namelist()
        stem = "test_granite_" + finding["id"]
        assert sorted(names) == sorted([f"{stem}.json", f"{stem}.py", "README.txt"])
        case = json.loads(zipfile.ZipFile(io.BytesIO(r.content)).read(f"{stem}.json"))
        assert case["origin_step"] == "s2" and case["target_checks"] == ["CHK-OUT-1"]
        assert case["workflow_module"] == "refund_desk" and case["failing_trace"]["steps"]


class TestBatches:
    def test_generates_every_pair_and_scores_by_condition(self, client):
        r = client.post("/api/batches", json={"faults": ["stale_price", "none"], "task_ids": ["#W1023987", "#W1052399"],
                                              "mode": "recorded"})
        assert r.status_code == 202, r.text
        batch = client.get(f"/api/batches/{r.json()['batch_id']}").json()
        assert batch["status"] == "done" and batch["task_count"] == 2 and len(batch["runs"]) == 4
        assert batch["groups"]["stale_price"] == {"runs": 2, "finished": 2, "completed": 2, "errored": 0,
                                                  "with_finding": 2}
        assert batch["groups"]["none"]["with_finding"] == 0
        assert client.get("/api/batches").json()[0]["id"] == batch["id"]

    def test_unrecorded_fault_errors_cleanly_and_the_batch_continues(self, client):
        r = client.post("/api/batches", json={"faults": ["dropped_item"], "task_ids": ["#W1023987"], "mode": "recorded",
                                              "seed": 424242})
        batch = client.get(f"/api/batches/{r.json()['batch_id']}").json()
        assert batch["status"] == "done" and batch["groups"]["dropped_item"]["errored"] == 1
        assert "never recorded" in batch["runs"][0]["error"]

    def test_validation(self, client):
        assert client.post("/api/batches", json={"faults": ["cosmic_ray"]}).status_code == 422
        assert client.post("/api/batches", json={"faults": ["none"], "task_ids": ["#W0000001"]}).status_code == 422
        assert client.post("/api/batches", json={"faults": []}).status_code == 422
        assert client.get("/api/batches/bat_nope").status_code == 404


class TestEvaluations:
    def test_lists_and_serves_result_files_only(self, make_client, tmp_path):
        results = tmp_path / "results"
        results.mkdir()
        body = {"meta": {"date": "2026-11-15", "mode": "live", "model": "m", "n_tasks": 1, "faults": ["f"]},
                "metrics": {"detection": {"k": 1, "n": 1}}, "rows": [{}, {}]}
        (results / "2026-11-15_benchmark-v0.json").write_text(json.dumps(body), encoding="utf-8")
        (results / "notes.json").write_text("{}", encoding="utf-8")
        client = make_client(eval_dir=results)
        listed = client.get("/api/evaluations").json()
        assert [e["id"] for e in listed] == ["2026-11-15_benchmark-v0"] and listed[0]["complete"] is True
        full = client.get("/api/evaluations/2026-11-15_benchmark-v0").json()
        assert full["metrics"]["detection"]["k"] == 1 and len(full["rows"]) == 2
        assert client.get("/api/evaluations/notes").status_code == 404
        assert client.get("/api/evaluations/..%2F..%2Fsecrets").status_code == 404

    def test_missing_directory_gives_an_empty_list(self, make_client, tmp_path):
        assert make_client(eval_dir=tmp_path / "absent").get("/api/evaluations").json() == []


def test_new_faults_are_offered_and_runnable_in_the_catalogue(client, example):
    wf = client.get("/api/workflows").json()[0]
    assert set(wf["faults"]) == {"stale_price", "dropped_item", "handoff_drift"}
    run = start_run(client, example, "stale_price")["run"]
    assert run["injected_fault"]["fault_type"] == "stale_price"
