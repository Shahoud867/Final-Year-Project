# ADR-007: Host the public demo on a free web-service tier

| | |
|---|---|
| Status | proposed (NOT decided, NOT verified, nothing deployed) |
| Date | 2026-10-07 |
| Owner | to be assigned by the team |
| Reviewers | two other members, to be assigned |
| Related | master plan decisions D1 and A4; `Dockerfile`, `.github/workflows/ci.yml` |

## Context

Mid-1 expects a working system, preferably on a URL a supervisor can open. Budget is zero and no payment card should be needed. Free tiers change their limits and sleep policies, so any claim about them must be checked on the day.

## Decision

Proposal: build one Docker image (done, see ADR-001) and deploy that image to a free web-service host such as Render, with recorded mode as the default so the public instance needs no language-model key. The self-hosted product path is `docker compose up`. This ADR stays *proposed* until someone has created the service, deployed it and recorded the URL in `docs/registers/deployment-record.md`.

## Alternatives considered

| Alternative | Why rejected or open |
|---|---|
| AWS, Azure, GCP | Need a card and add operations work out of proportion to the claim |
| Hugging Face Docker Space | The plan records that it needs a paid plan now (verify) |
| Run only on a laptop | Acceptable fallback for the demo, but gives the panel nothing to open and no deployment evidence |

## Consequences

The Dockerfile has **not been built** on this machine (the Docker daemon was not running) and the CI container job has not run, so the image is unverified. A clean non-editable install with the same environment variables was verified locally and served the UI and a recorded run. Free instances sleep when idle, so the first request can take about a minute; say so in the demo script. Decide the hosted-model question (D1) separately; recorded mode avoids it for the demo.

## Evidence of understanding (handbook C.14.1)

*To be written by the owner in their own words: explain the decision, justify it against the main alternative, predict what breaks if it changes, and say how you would modify it. This draft was prepared with AI assistance (see `docs/registers/ai-usage-log.md`) and is not evidence of understanding until the owner has written this section.*
