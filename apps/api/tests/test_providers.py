"""Live model providers against a local stub server (no real model needed)."""

from __future__ import annotations

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest
from granite_core.llm import LLMRequest, ProviderUnavailable

from granite_api.providers import OllamaProvider, OpenAICompatProvider

REQ = LLMRequest(messages=[{"role": "user", "content": "hi"}], model="m", seed=7, json_mode=True)


class Stub(BaseHTTPRequestHandler):
    seen: list[dict] = []
    mode = "ok"

    def do_POST(self):  # noqa: N802
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        Stub.seen.append({"path": self.path, "auth": self.headers.get("Authorization"), "body": body})
        if Stub.mode == "slow":
            time.sleep(1.5)
        code, payload = 200, self.reply()
        if Stub.mode == "http500":
            code, payload = 500, b"boom"
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    def reply(self) -> bytes:
        if Stub.mode == "notjson":
            return b"<html>"
        if Stub.mode == "badshape":
            return b"{}"
        if self.path.endswith("/api/chat"):
            return json.dumps({"message": {"content": "pong"}, "prompt_eval_count": 3, "eval_count": 2}).encode()
        usage = {"prompt_tokens": 4, "completion_tokens": 5}
        return json.dumps({"choices": [{"message": {"content": "pong"}}], "usage": usage}).encode()

    def log_message(self, *args):
        pass


@pytest.fixture
def stub():
    server = HTTPServer(("127.0.0.1", 0), Stub)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    Stub.seen, Stub.mode = [], "ok"
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


def test_ollama_sends_options_and_parses_the_answer(stub):
    out = OllamaProvider(stub).complete(REQ)
    sent = Stub.seen[0]
    assert (out.text, out.tokens_in, out.tokens_out, out.provider) == ("pong", 3, 2, "ollama")
    assert sent["path"] == "/api/chat" and sent["body"]["format"] == "json" and sent["body"]["stream"] is False
    assert sent["body"]["options"]["seed"] == 7 and sent["body"]["options"]["temperature"] == 0.2


def test_openai_compatible_sends_bearer_key_and_json_mode(stub):
    out = OpenAICompatProvider(stub, api_key="k-test").complete(REQ)
    sent = Stub.seen[0]
    assert (out.text, out.tokens_in, out.tokens_out) == ("pong", 4, 5)
    assert sent["path"] == "/chat/completions" and sent["auth"] == "Bearer k-test"
    assert sent["body"]["response_format"] == {"type": "json_object"} and sent["body"]["seed"] == 7


@pytest.mark.parametrize("provider_cls", [OllamaProvider, OpenAICompatProvider])
@pytest.mark.parametrize(
    ("mode", "message"),
    [("http500", "HTTP 500"), ("notjson", "not JSON"), ("badshape", "")],
)
def test_bad_endpoint_behaviour_becomes_provider_unavailable(stub, provider_cls, mode, message):
    Stub.mode = mode
    provider = provider_cls(stub) if provider_cls is OllamaProvider else provider_cls(stub, "k")
    with pytest.raises(ProviderUnavailable, match=message or "."):
        provider.complete(REQ)


def test_timeout_and_unreachable_are_clear_errors(stub):
    Stub.mode = "slow"
    with pytest.raises(ProviderUnavailable, match="unreachable or too slow"):
        OllamaProvider(stub, timeout=0.3).complete(REQ)
    with pytest.raises(ProviderUnavailable, match="unreachable or too slow"):
        OllamaProvider("http://127.0.0.1:9", timeout=0.5).complete(REQ)


@pytest.mark.parametrize("url", ["file:///etc/passwd", "ftp://example.com/x", "gopher://x", "javascript:alert(1)", ""])
def test_only_http_endpoints_are_ever_contacted(url):
    from granite_api.providers import check_endpoint

    with pytest.raises(ProviderUnavailable, match="http"):
        check_endpoint(url)
    with pytest.raises(ProviderUnavailable, match="http"):
        OllamaProvider(url).complete(REQ)


def test_config_rejects_non_http_model_urls():
    from granite_api.config import Settings

    with pytest.raises(ValueError, match="GRANITE_OLLAMA_URL"):
        Settings(ollama_url="file:///tmp/x").validate()
    with pytest.raises(ValueError, match="GRANITE_OPENAI_BASE_URL"):
        Settings(openai_base_url="ftp://x", openai_api_key="k").validate()
    Settings(ollama_url="https://models.example.org").validate()
