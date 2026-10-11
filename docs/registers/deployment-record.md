# Deployment record

| | |
|---|---|
| Version | 1.2 |
| Date | 2026-10-11 |
| Status | **Deployed** on Render since 2026-10-11 (public demo, recorded mode). Releases are listed at the end |

## Where it runs today

| Item | State |
|---|---|
| Public URL | https://granite-demo.onrender.com, live since 2026-10-11 ([record](../../evidence/repo/2026-10-11_render-deployment.md)) |
| Local run | `uvicorn granite_api.main:app_from_env --factory` serves the API and, with `GRANITE_STATIC_DIR` set to the built web app, the UI. Verified on this machine on 2026-10-07 |
| Container | Built and smoke-tested by GitHub Actions on 2026-10-09 ([run 37924480165](../../evidence/repo/2026-10-09_ci-run-37924480165.md)); not yet built on a team laptop |
| CI | Runs on every push; first run on GitHub passed on 2026-10-09 |
| CD | Workflow written on 2026-10-11 ([`cd.yml`](../../.github/workflows/cd.yml)): after CI passes on `main` it publishes the image to the GitHub Container Registry and, when the deploy hook is configured, deploys to Render and smoke-tests the URL. First run on 2026-10-11 ([run 38137856992](https://github.com/Shahoud867/Final-Year-Project/actions/runs/38137856992)): image published, **deploy step skipped** because the secret `RENDER_DEPLOY_HOOK_URL` and the variable `GRANITE_DEMO_URL` are not set yet (a repository admin must add them; the Render service now exists) |
| Hosting definition | [`render.yaml`](../../render.yaml) (free plan, recorded mode, `autoDeploy: false`). Service `granite-demo` created from it on 2026-10-11 by Muhammad Noor |
| System tests against a running server | Verified locally on 2026-10-11: `GRANITE_SYSTEM_BASE_URL=... pytest tests/system` gave 18 passed, 4 skipped (the skipped cases configure their own server). The same command is wired into the CI container job |
| Cost | $0 so far |

## Install check from a clean environment (not a deployment)

On 2026-10-07 the three Python packages were installed non-editable into a fresh virtual environment, started from an unrelated directory with the container's environment variables, and a recorded run completed with one finding and the UI was served. This checks the packaging; it is not evidence of a hosted deployment.

## Entries to add per release

URL, how it was installed (link to the workflow run), who can access it, cost, known limits (idle sleep, rate limits), and an "installed by a person who is not the owner" entry (handbook C.1.2 asks for it).

## Releases

| Date | Commit | URL | Installed by | How | Verified | Known limits |
|---|---|---|---|---|---|---|
| 2026-10-11 | `89bcd8a` | https://granite-demo.onrender.com | Muhammad Noor (not the owner of the deployment code) | Render Blueprint from `render.yaml`, manual first deploy | Smoke test `OK: run run_31642431598b completed with finding fnd_365dc3abe0bc hypothesized`; system suite 18 passed, 4 skipped by design ([record](../../evidence/repo/2026-10-11_render-deployment.md)) | Idle spin-down (about 50 s first request); database reset on every deploy or restart; CD hook not yet configured |
