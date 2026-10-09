# Setup manual

| | |
|---|---|
| Version | 0.9 draft |
| Date | 2026-10-07 |
| Status | Written by the author of the code and checked on one Windows machine. **It has not yet been followed by a second person on a clean machine**; the handbook asks for that (record the result in `docs/registers/deployment-record.md`) |

Everything below is free of charge and needs no account or key. Two ways to run Granite: from source (developers) or in a container (anyone, once the image has been built; see the note under "Docker").

## 1. What you need

| Tool | Version | Needed for |
|---|---|---|
| Python | 3.11 | API, core library, tests |
| Node.js and npm | 22 or newer | Web UI build and tests |
| Git | any recent | getting the code |
| Ollama and the model `llama3.2:3b` | optional | *live* mode only. Without it Granite runs in *recorded* mode on saved real answers |
| Docker | optional | container run |

## 2. Install from source

```bash
git clone <repository-url> && cd Final-Year-Project
python -m venv .venv
# Windows PowerShell:  .venv\Scripts\Activate.ps1      macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -e "packages/granite_core[dev]" -e "workflows/refund_desk[dev]" -e "apps/api[dev]"
cd apps/web && npm ci && npm run build && cd ../..
```

Keep the virtual environment **outside OneDrive-synced folders** if you can: OneDrive slows installs and can lock files.

## 3. Start Granite

```bash
cd apps/api
GRANITE_LLM_MODE=recorded GRANITE_STATIC_DIR=../web/dist uvicorn granite_api.main:app_from_env --factory --port 8000
```

PowerShell: set the two variables first with `$env:GRANITE_LLM_MODE="recorded"; $env:GRANITE_STATIC_DIR="../web/dist"`.

Open <http://127.0.0.1:8000>. The API documentation is at <http://127.0.0.1:8000/docs>. The database is created on first start in `apps/api/.granite/granite.db`.

For UI development run the API as above on port 8000, and in another terminal `cd apps/web && npm run dev` (port 5173; requests to `/api` are forwarded to port 8000). Open it as `http://localhost:5173`; on some machines `127.0.0.1` does not reach the Vite server. To forward elsewhere set `GRANITE_API_URL`.

## 4. Modes and settings

| Variable | Default | Meaning |
|---|---|---|
| `GRANITE_LLM_MODE` | `auto` | `recorded` answers only from the saved cassette (works offline, only for the 12 example tasks); `live` calls the model; `auto` uses live if Ollama answers, else recorded |
| `GRANITE_MODEL` | `llama3.2:3b` | Ollama model name |
| `GRANITE_OLLAMA_URL` | `http://127.0.0.1:11434` | Ollama address (http or https only) |
| `GRANITE_OPENAI_BASE_URL`, `GRANITE_OPENAI_API_KEY` | empty | Use a hosted OpenAI-compatible endpoint instead (set both). **Never commit the key**; use a `.env` file (git-ignored) or the host's secret store |
| `GRANITE_DB_URL` | SQLite file | Any SQLAlchemy URL. Only SQLite has been tested |
| `GRANITE_API_TOKEN` | empty | If set, every `/api` call needs `Authorization: Bearer <token>`; the UI shows a token box |
| `GRANITE_RECORD` | off | `1` also saves live answers into the cassette |
| `GRANITE_RATE_LIMIT` | 120 | State-changing requests per minute per client; 0 turns it off |

See `.env.example` for the full list.

### Live mode

```bash
ollama serve            # once; leave it running
ollama pull llama3.2:3b
```

In the UI use "Test model" (top right). Expect 5 to 15 seconds per model call on a laptop CPU, so one run takes about a minute and a verification about three.

## 5. Check that it works

```bash
bash scripts/smoke-test.sh http://127.0.0.1:8000
```

It checks health, the UI, and a recorded run that must open one finding. Expected last line: `OK: run run_... completed with finding fnd_... hypothesized`. If your default `python3` is broken, run it as `PYTHON=/path/to/python bash scripts/smoke-test.sh ...`.

## 6. Run the quality gates

```bash
(cd packages/granite_core && pytest --cov=granite_core && ruff check . && mypy granite_core)
(cd workflows/refund_desk && pytest && ruff check . && mypy refund_desk)
(cd apps/api && pytest --cov=granite_api && ruff check . && mypy granite_api)
(cd apps/web && npm test && npm run lint && npm run typecheck)
bandit -q -r packages/granite_core/granite_core workflows/refund_desk/refund_desk apps/api/granite_api -ll
python scripts/check_workspace.py && python scripts/check_links.py
python scripts/export_trace_schema.py --check && python scripts/export_diagrams.py --check
python scripts/check_traceability.py --check
```

## 7. Re-record the model answers

Needed after **any** change to a prompt or a step (recorded mode fails otherwise):

```bash
python scripts/record_cassettes.py            # about 15 minutes, needs Ollama
```

## Docker

```bash
docker compose up --build        # then open http://localhost:8000
```

**Status on 2026-10-07:** the Dockerfile has not been built yet (the Docker daemon was off on the authoring machine) and the CI container job has not run. Treat this section as untested until it has.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Run ends with "this exact request was never recorded" | Recorded mode with your own task or after a prompt change. Use an example task, switch to live, or re-record |
| Run ends with "model endpoint unreachable or too slow" | Ollama is not running or the model is not pulled. `ollama serve`, `ollama pull llama3.2:3b`, then "Test model" |
| UI shows "Cannot reach the Granite server" | The API is not running on the port the UI expects (dev server forwards to 8000) |
| `ModuleNotFoundError: granite_core` | The packages were not installed into the active virtual environment (step 2) |
| 401 on every call | `GRANITE_API_TOKEN` is set; paste the token into the box in the UI header |
| Port already in use | Choose another with `--port` |
