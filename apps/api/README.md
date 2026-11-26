# granite_api

Application layer: HTTP API (FastAPI), persistence (SQLAlchemy, SQLite by default), background jobs, model providers. It wires `granite_core` and the workflow together and adds nothing to their logic.

| Part | File |
|---|---|
| App factory, middleware (request id, security headers, rate limit, body limit, CORS), static UI | `granite_api/main.py` |
| Endpoints | `routes.py` (interactive reference at `/docs` on a running server) |
| Errors (RFC 7807 problem responses) | `errors.py` |
| Tables ([ER diagram](../../docs/diagrams/database-schema.md)) | `models.py` |
| Run, analysis, experiment, review, report services | `services/` |
| Job runner with crash recovery | `jobs.py` |
| Live providers (Ollama, OpenAI-compatible) and mode choice | `providers.py`, `llm_factory.py` |
| Settings from environment variables | `config.py` |

Journey: `POST /api/runs` returns a job id; poll `GET /api/jobs/{id}`; `GET /api/runs/{id}` then shows findings; `POST /api/hypotheses/{id}/experiments` starts a verification; `POST /api/findings/{id}/reviews` records a decision; `GET /api/findings/{id}/report` downloads the report.

```bash
pip install -e ../../packages/granite_core -e ../../workflows/refund_desk -e ".[dev]"
pytest --cov=granite_api       # 67 tests; run in recorded mode, no model needed
```
Setup and settings: [`docs/manuals/setup-manual.md`](../../docs/manuals/setup-manual.md).
