# Dependency and licence register

| | |
|---|---|
| Version | 1.1 |
| Date | 2026-10-14 |
| Status | Draft. Generated from installed package metadata on 2026-10-07; the three web packages added on 2026-10-14 were read from their `package.json` on that date. Not yet reviewed by the team. |
| Owner | Saif (to confirm) |
| Refresh | Re-run the commands under "How this was produced" whenever a dependency is added or upgraded; the CI jobs `pip-audit` and `npm audit` report known vulnerabilities on every push. |

Only direct dependencies are listed; their own dependencies carry compatible permissive licences but are not enumerated here. "Distributed" means shipped inside the Docker image or the web bundle.

## Python (runtime, distributed)

| Package | Version | Licence | Used for |
|---|---|---|---|
| pydantic | 2.13.5 | MIT | Trace schema, request and response validation |
| fastapi | 0.142.2 | MIT | HTTP API |
| uvicorn | 0.54.0 | BSD-3-Clause | ASGI server |
| SQLAlchemy | 2.1.3 | MIT | Persistence (SQLite or PostgreSQL) |

## Python (development and test, not distributed)

| Package | Version | Licence | Used for |
|---|---|---|---|
| pytest, pytest-cov | 9.1.1, 7.1.0 | MIT | Tests and coverage |
| hypothesis | 6.168.5 | MPL-2.0 | Property-based tests (file-level copyleft; we use it unmodified and do not redistribute it) |
| httpx | 0.28.1 | BSD-3-Clause | FastAPI test client |
| ruff | 0.16.10 | MIT | Lint |
| mypy | 2.4.0 | MIT | Strict type checks |
| bandit | 1.9.4 | Apache-2.0 | Static security scan |
| pip-audit | 2.10.1 | Apache-2.0 | Known-vulnerability scan |

## Web (distributed: react, react-dom, the icons that are imported and the two fonts; everything else is build or test only)

| Package | Version | Licence |
|---|---|---|
| react, react-dom | 19.3.0 | MIT |
| lucide-react (icons; only the icons the code imports end up in the bundle) | 1.56.0 | ISC |
| @fontsource-variable/inter, @fontsource-variable/jetbrains-mono (Inter and JetBrains Mono, served from our own origin; no request to a font service) | 5.3.0, 5.3.0 | OFL-1.1 (SIL Open Font License: fonts may be bundled and redistributed with software; they may not be sold on their own) |
| vite, @vitejs/plugin-react | 8.3.3, 6.1.2 | MIT |
| typescript | 6.0.3 | Apache-2.0 |
| vitest, jsdom | 5.0.3, 30.1.2 | MIT |
| @testing-library/react, jest-dom, user-event | 16.3.3, 7.0.1, 14.6.7 | MIT |
| eslint, @eslint/js, typescript-eslint, eslint-plugin-react-hooks, globals | 10.12.0, 10.0.1, 8.71.1, 7.1.1, 17.13.0 | MIT |
| @types/node, @types/react, @types/react-dom | 26.6.4, 19.3.0, 19.3.0 | MIT |
| axe-core (accessibility tests only) | 4.14.0 | MPL-2.0 |

## Data, models and services

| Item | Licence or terms | How we use it | Note |
|---|---|---|---|
| tau-bench retail data (Sierra) | MIT, copyright 2024 Sierra. Text in `data/seed/taubench_retail_v1/LICENSE.txt` | A 75-order subset is the Refund Desk's customers, orders and catalogue, and the checks' source of truth. Synthetic data. Selection rule: `scripts/build_truth_snapshot.py` | Modified only by selecting a subset. The full upstream copy under `data/raw/` is third-party and is not part of the Docker image |
| Ollama | MIT | Local model server for live mode | Not distributed with Granite; the user installs it |
| Llama 3.2 3B (`llama3.2:3b`) | Llama 3.2 Community License (Meta). Confirm the current terms on the model card before any redistribution | Model behind the Refund Desk's three language-model steps in live mode | Weights are pulled by Ollama on the user's machine. We distribute only recorded *answers* of the model (`data/cassettes/refund_desk_v1.json`); **check with the supervisor that redistributing recorded outputs is acceptable under the licence before the repository is made public** |
| GitHub Actions: actions/checkout, setup-python, setup-node | MIT | CI | Pinned to major versions |
| gitleaks/gitleaks-action | MIT (the action itself) | Secret scan in CI | The action may require a licence key for repositories owned by an organisation; a personal repository is fine. Verify when the repository is created |

## Open items

1. Licence of `hypothesis` (MPL-2.0) is acceptable for dev-only use; confirm nothing under `tests/` is shipped in the image (the Dockerfile removes the `tests/` folders).
2. Decide the licence of Granite itself (no `LICENSE` file exists at the repository root yet). Until then the repository is "all rights reserved" by default.
3. Confirm the Llama 3.2 redistribution question above.

## How this was produced

```bash
python -c "from importlib import metadata; print(metadata.metadata('pydantic')['License-Expression'])"   # per package
node -e "console.log(require('./apps/web/node_modules/react/package.json').license)"                       # per package
pip-audit --skip-editable ; (cd apps/web && npm audit --audit-level=high)                                  # vulnerabilities
```
