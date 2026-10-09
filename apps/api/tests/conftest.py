"""API test fixtures. Tests run in recorded mode on the committed cassette: deterministic, no model needed."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from typing import Any

import pytest
from fastapi.testclient import TestClient

from granite_api.config import REPO_ROOT, Settings
from granite_api.main import create_app

CASSETTE = REPO_ROOT / "data" / "cassettes" / "refund_desk_v1.json"


@pytest.fixture
def make_client(tmp_path) -> Callable[..., TestClient]:
    opened: list[TestClient] = []

    def factory(**overrides: Any) -> TestClient:
        base = Settings(
            db_url=f"sqlite:///{(tmp_path / 'test.db').as_posix()}", llm_mode="recorded", jobs_inline=True,
            cassette_path=CASSETTE, rate_limit_per_minute=0,
        )
        client = TestClient(create_app(replace(base, **overrides)))
        client.__enter__()
        opened.append(client)
        return client

    yield factory
    for c in opened:
        c.__exit__(None, None, None)


@pytest.fixture
def client(make_client) -> TestClient:
    return make_client()


@pytest.fixture(scope="session")
def example() -> dict[str, str]:
    """The first recorded example task (delivered order with two items)."""
    from refund_desk import default_store

    t = next(t for t in default_store().example_tasks(12) if "(delivered)" in t["label"])
    return {k: t[k] for k in ("message", "email", "order_id")}


def start_run(client: TestClient, task: dict[str, str], fault: str | None = None, **extra: Any) -> dict[str, Any]:
    r = client.post("/api/runs", json={"workflow": "refund_desk", "task_input": task, "fault": fault, **extra})
    assert r.status_code == 202, r.text
    body = r.json()
    run = client.get(f"/api/runs/{body['run_id']}")
    assert run.status_code == 200
    return {**body, "run": run.json()}


def open_finding(client: TestClient, task: dict[str, str]) -> dict[str, Any]:
    run = start_run(client, task, "stale_price")["run"]
    assert len(run["findings"]) == 1, run
    return client.get(f"/api/findings/{run['findings'][0]['id']}").json()


def hypothesis_for(finding: dict[str, Any], step_id: str) -> dict[str, Any]:
    return next(h for h in finding["hypotheses"] if h["step_id"] == step_id)


def verify(client: TestClient, hypothesis_id: str, n: int = 5, m: int = 2) -> dict[str, Any]:
    r = client.post(f"/api/hypotheses/{hypothesis_id}/experiments", json={"n": n, "m": m})
    assert r.status_code == 202, r.text
    return client.get(f"/api/experiments/{r.json()['experiment_id']}").json()
