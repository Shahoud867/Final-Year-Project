# ADR-010: Work on short-lived branches, review every change, release from main

| | |
|---|---|
| Status | proposed (the plan's model; actual repository settings not verified) |
| Date | 2026-10-07 |
| Owner | to be assigned by the team |
| Reviewers | two other members, to be assigned |
| Related | master plan section on branching, `.github/workflows/ci.yml` |

## Context

Three people commit to one repository; the faculty guidance asks for evidence of CI/CD and of collaboration (pull requests, reviews). Evidence only exists if the workflow is used and not just described.

## Decision

As written in the plan: protected `main` (releases, tagged) and `develop` (integration), feature branches, pull requests with one approval from a non-author, squash merge, Conventional Commits such as `feat(verify): add control replays`. CI must pass before merge.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| Everyone pushes to main | No review trail; the rubric asks for per-member pull-request evidence |
| Long-lived personal branches | Painful merges; the repository already shows a long-lived `noor` branch |

## Consequences

At the time of writing the repository has branches `main` and `noor` and no `develop`; checked on 2026-10-09: `main` is **not protected**, there are no tags, and CI passed on its first GitHub run. Per-member pull-request evidence cannot be produced by an assistant; it must come from the members' own work. Record screenshots in `evidence/repo/` once the settings exist.

## Evidence of understanding (handbook C.14.1)

*To be written by the owner in their own words: explain the decision, justify it against the main alternative, predict what breaks if it changes, and say how you would modify it. This draft was prepared with AI assistance (see `docs/registers/ai-usage-log.md`) and is not evidence of understanding until the owner has written this section.*
