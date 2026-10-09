# Milestone log

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-10-07 |
| Status | Live. Planned dates come from the master plan; the Mid-1 date itself is **still unconfirmed** (plan decision A1, D7) |

| Date | Milestone | Planned | Actual | Note |
|---|---|---|---|---|
| 2026-10-06 | Master plan v1.1 (re-checked against the Mid-1 rubric and report template) | - | Done | `docs/plan/master-plan.md` |
| 2026-10-06 | Workspace reorganised, link and structure checks | - | Done | Committed to `main` by the team |
| 2026-10-06 | Core library (trace, checks language, attribution, verification, lifecycle, evidence) | Iteration 1 | Done | Tests and strict type checks pass |
| 2026-10-06 | Refund Desk workflow on real retail data, run against a real local model | Iteration 1 | Done | First real run recorded |
| 2026-10-07 | HTTP API, persistence, jobs; web UI | Iteration 1 | Done (works locally) | Driven end to end in a browser |
| 2026-10-07 | CI workflow and container definition written | Iteration 1 | Done; first GitHub run passed 2026-10-09 (all four jobs) | [CI run](../../evidence/repo/2026-10-09_ci-run-37924480165.md) |
| 2026-10-07 | Feasibility validation (10 tasks, pre-registered) | Iteration 1 | Done; all thresholds met, one explained miss | [Notes](../../research/eval/results/2026-10-07_refund-desk-feasibility-notes.md) |
| - | Deployed URL | Iteration 1 | **Not done** | Needs a decision on hosting (ADR-007) and someone to create the service |
| - | Release tag `v0.1.0-mid1` | Iteration 1 | **Not done** | CI is green; the team creates the tag when the Mid-1 state is final |
| - | Mid-1 report (LaTeX template) | Before the demo (assumed) | **Not started** | Must be written by the members in their own words |

## Delays and recovery

No delay can be stated yet because the Mid-1 date is unknown. The items that block a credible Mid-1 are, in order: confirm the date, create the GitHub-hosted CI evidence, deploy once, write the report.
