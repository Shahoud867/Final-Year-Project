"""System-test fixtures: a real Granite server in its own process, driven only through HTTP.

By default each session starts `uvicorn` on a free port with a temporary database, in recorded mode (saved real
model answers), so the suite needs no model and no network. Set GRANITE_SYSTEM_BASE_URL to run the same tests
against a server that is already running (the Docker container in CI, or a deployed instance); tests that need
to control the server's configuration are then skipped.
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]
EXTERNAL = os.environ.get("GRANITE_SYSTEM_BASE_URL", "").rstrip("/")


@dataclass
class Response:
    status: int
    headers: dict[str, str]
    text: str

    def json(self) -> Any:
        return json.loads(self.text)


class Client:
    """A minimal HTTP client (standard library only), so the tests depend on nothing the product ships."""

    def __init__(self, base: str, token: str = "") -> None:
        self.base, self.token = base, token

    def call(self, method: str, path: str, body: Any = None, headers: dict[str, str] | None = None, raw: bytes | None = None) -> Response:
        data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
        req = urllib.request.Request(self.base + path, data=data, method=method)  # noqa: S310 - local test server
        if data is not None:
            req.add_header("Content-Type", "application/json")
        if self.token:
            req.add_header("Authorization", f"Bearer {self.token}")
        for k, v in (headers or {}).items():
            req.add_header(k, v)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
                return Response(resp.status, {k.lower(): v for k, v in resp.headers.items()}, resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            try:
                text = e.read().decode("utf-8", "replace")
            except OSError:
                text = ""  # the status arrived, then the server closed the connection before the body was read
            return Response(e.code, {k.lower(): v for k, v in e.headers.items()}, text)
        except (OSError, urllib.error.URLError) as e:
            # A server may refuse an upload and close the connection before the client has finished sending it.
            return Response(0, {}, f"connection closed by the server: {e}")

    def get(self, path: str, **kw: Any) -> Response:
        return self.call("GET", path, **kw)

    def post(self, path: str, body: Any = None, **kw: Any) -> Response:
        return self.call("POST", path, body if body is not None else {}, **kw)

    # ---- journeys used by several tests ---------------------------------------------------------------
    def wait_job(self, job_id: str, seconds: float = 60) -> dict[str, Any]:
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            job = self.get(f"/api/jobs/{job_id}").json()
            if job["status"] in ("succeeded", "failed"):
                return job
            time.sleep(0.15)
        raise AssertionError(f"job {job_id} did not finish in {seconds} s")

    def example(self, index: int = 0) -> dict[str, str]:
        ex = self.get("/api/workflows/refund_desk/examples").json()[index]
        return {k: ex[k] for k in ("message", "email", "order_id")}

    def run(self, task: dict[str, str], fault: str | None = None, **extra: Any) -> dict[str, Any]:
        r = self.post("/api/runs", {"workflow": "refund_desk", "task_input": task, "fault": fault, "mode": "recorded", **extra})
        assert r.status == 202, r.text
        accepted = r.json()
        job = self.wait_job(accepted["job_id"])
        assert job["status"] == "succeeded", job
        return self.get(f"/api/runs/{accepted['run_id']}").json()

    def finding_of(self, run: dict[str, Any]) -> dict[str, Any]:
        assert len(run["findings"]) == 1, run["findings"]
        return self.get(f"/api/findings/{run['findings'][0]['id']}").json()

    def verify(self, finding: dict[str, Any], step_id: str, n: int = 5, m: int = 2) -> dict[str, Any]:
        hyp = next(h for h in finding["hypotheses"] if h["step_id"] == step_id)
        r = self.post(f"/api/hypotheses/{hyp['id']}/experiments", {"n": n, "m": m, "mode": "recorded"})
        assert r.status == 202, r.text
        accepted = r.json()
        self.wait_job(accepted["job_id"])
        return self.get(f"/api/experiments/{accepted['experiment_id']}").json()


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


@dataclass
class Server:
    base: str
    process: subprocess.Popen[bytes]
    env: dict[str, str]
    port: int

    def stop(self) -> None:
        self.process.terminate()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.kill()


def _start(env_overrides: dict[str, str], db: Path, port: int | None = None) -> Server:
    port = port or _free_port()
    env = {**os.environ, "GRANITE_LLM_MODE": "recorded", "GRANITE_DB_URL": f"sqlite:///{db.as_posix()}",
           "GRANITE_RATE_LIMIT": "0", **env_overrides}
    dist = ROOT / "apps" / "web" / "dist"
    if (dist / "index.html").exists():
        env.setdefault("GRANITE_STATIC_DIR", str(dist))
    proc = subprocess.Popen(  # noqa: S603 - fixed command, our own interpreter
        [sys.executable, "-m", "uvicorn", "granite_api.main:app_from_env", "--factory", "--host", "127.0.0.1",
         "--port", str(port), "--log-level", "warning"],
        cwd=ROOT / "apps" / "api", env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    base = f"http://127.0.0.1:{port}"
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"server exited with code {proc.returncode} while starting")
        try:
            with urllib.request.urlopen(base + "/api/health", timeout=5):  # noqa: S310
                return Server(base, proc, env, port)
        except OSError:
            time.sleep(0.2)
    proc.kill()
    raise RuntimeError("server did not become healthy in 30 s")


ServerFactory = Callable[..., Server]


@pytest.fixture(scope="session")
def start_server(tmp_path_factory: pytest.TempPathFactory) -> Iterator[ServerFactory]:
    """Start extra servers with their own configuration (token, rate limit, unreachable model, shared database)."""
    started: list[Server] = []

    def factory(db: Path | None = None, port: int | None = None, **env: str) -> Server:
        if EXTERNAL:
            pytest.skip("needs to configure its own server; skipped when GRANITE_SYSTEM_BASE_URL is set")
        server = _start(env, db or tmp_path_factory.mktemp("granite") / "system.db", port)
        started.append(server)
        return server

    yield factory
    for s in started:
        s.stop()


@pytest.fixture(scope="session")
def api(start_server: ServerFactory) -> Client:
    """The system under test: an external server if configured, else a fresh local one."""
    if EXTERNAL:
        return Client(EXTERNAL, os.environ.get("GRANITE_SYSTEM_TOKEN", ""))
    return Client(start_server().base)


@pytest.fixture(scope="session")
def has_ui(api: Client) -> bool:
    r = api.get("/")
    return r.status == 200 and "<div id=\"root\">" in r.text
