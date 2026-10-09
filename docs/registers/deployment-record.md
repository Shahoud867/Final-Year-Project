# Deployment record

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-10-07 |
| Status | **Nothing is deployed.** This file will record each release once something is |

## Where it runs today

| Item | State |
|---|---|
| Public URL | None |
| Local run | `uvicorn granite_api.main:app_from_env --factory` serves the API and, with `GRANITE_STATIC_DIR` set to the built web app, the UI. Verified on this machine on 2026-10-07 |
| Container | Built and smoke-tested by GitHub Actions on 2026-10-09 ([run 37924480165](../../evidence/repo/2026-10-09_ci-run-37924480165.md)); not yet built on a team laptop |
| CI | Runs on every push; first run on GitHub passed on 2026-10-09 |
| Cost | $0 so far |

## Install check from a clean environment (not a deployment)

On 2026-10-07 the three Python packages were installed non-editable into a fresh virtual environment, started from an unrelated directory with the container's environment variables, and a recorded run completed with one finding and the UI was served. This checks the packaging; it is not evidence of a hosted deployment.

## Entries to add per release

URL, how it was installed (link to the workflow run), who can access it, cost, known limits (idle sleep, rate limits), and an "installed by a person who is not the owner" entry (handbook C.1.2 asks for it).
