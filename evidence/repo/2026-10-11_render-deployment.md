# First public deployment on Render, 2026-10-11

URL: https://granite-demo.onrender.com (public, no login; recorded mode, so no model server or API key is involved)

| | |
|---|---|
| Service | `granite-demo` (Render web service, Docker runtime, free plan), created from the Blueprint [`render.yaml`](../../render.yaml) |
| Deployed commit | `89bcd8a` on `main` ("docs(deliverables): finalize FYP-1 mid evaluation deliverables, evidence, and registers"); build and deploy took 1 min 4 s |
| Installed by | Muhammad Noor, who is not the owner of the deployment code (handbook C.1.2) |
| Screenshots | [Render dashboard, service live](2026-10-11_render-service-live.png); [the application at the public URL](2026-10-11_render-app-home.png) (header shows "server ok · recorded") |

## Checks run against the public URL (from Noor's laptop, Windows 11, Python 3.11.9)

| Check | Command | Result |
|---|---|---|
| Smoke test, 13:59 UTC | `bash scripts/smoke-test.sh https://granite-demo.onrender.com` | `OK: run run_31642431598b completed with finding fnd_365dc3abe0bc hypothesized` |
| System test suite | `GRANITE_SYSTEM_BASE_URL=https://granite-demo.onrender.com pytest tests/system` | 18 passed, 4 skipped (the skipped cases start and configure their own server, so they cannot run against a hosted one), 144 s |

## Known limits of this deployment

- Free instances spin down when idle; the first request after a pause can take about 50 seconds. Open the URL a minute before a demo.
- The disk is temporary: the SQLite database, and with it every run and finding, is reset on each deploy or restart.
- `autoDeploy` is off. A new commit is deployed only by the CD workflow, once the repository secret `RENDER_DEPLOY_HOOK_URL` and the variable `GRANITE_DEMO_URL` are set by a repository admin, or by "Manual Deploy" in the Render dashboard.
- Render's announced maintenance window: 14 October 2026, 06:00 PKT (01:00 UTC).
