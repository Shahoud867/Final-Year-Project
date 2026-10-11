# Milestone log and iteration plan

| | |
|---|---|
| Version | 2.0 |
| Date | 2026-10-11 |
| Status | Live. Version 1.0 of 2026-10-07 is in the git history; its entries are kept at the end. Planned items and owners come from the master plan (sections 26.1, 34.1, 35). "Actual" is what can be shown on this date. The Mid-1 date is **still unconfirmed**; this log assumes the week of 12 to 16 October (the plan's scenario B) |
| Rubric | Criterion 2: planned milestone completed, or the delay justified with an owner-assigned recovery plan |

Status words: **Done** (can be shown today), **Partly**, **Late**, **Not started**. "Planned owner" is the plan's owner; "done by" says who actually produced it, because the two differ and the rubric asks about both.

## Iteration 1: core investigation slice (target: Mid-1, release `v0.1.0`)

| # | Work item | Planned owner | Planned for | Actual | Status | Evidence |
|---|---|---|---|---|---|---|
| 1 | Master plan re-checked against the Mid-1 rubric | Shahoud | 5 Oct | 6 Oct | Done | [`master-plan.md`](../plan/master-plan.md) |
| 2 | Workspace reorganised; structure and link checks | Shahoud | 5 Oct | 6 Oct | Done | [`check_workspace.py`](../../scripts/check_workspace.py) |
| 3 | Core library: trace, runner, check language, checks | Noor (checks), Shahoud (runner) | Week 8 | 6 Oct | Done | 207 tests; [`packages/granite_core`](../../packages/granite_core/) |
| 4 | Attribution (trace back) | Noor | Week 8 | 6 Oct | Done | [`attribution.py`](../../packages/granite_core/granite_core/attribution.py) |
| 5 | Verification by replay, rule VR-1, lifecycle | Saif | Week 8 | 6 Oct | Done | [`verification.py`](../../packages/granite_core/granite_core/verification.py), [`lifecycle.py`](../../packages/granite_core/granite_core/lifecycle.py) |
| 6 | Refund Desk workflow on real retail data, recorded against a real local model | Shahoud | Week 8 | 6 to 7 Oct | Done | 49 tests; 249 recorded answers |
| 7 | API, database, background jobs | Saif | Week 8 | 7 Oct | Done | 71 tests; [`apps/api`](../../apps/api/) |
| 8 | Web UI (improved interface) | Shahoud; all for their screens | Week 8 | 7 Oct; guide page 11 Oct | Done | 32 tests; [screenshots](../../evidence/demos/) |
| 9 | Feasibility validation, pre-registered | Noor | Week 8 | 7 Oct | Done | [Results](../../research/eval/results/2026-10-07_refund-desk-feasibility-notes.md) |
| 10 | CI on GitHub Actions | Saif | Day 0 to 1 | Written 7 Oct, first green run 9 Oct | Done | [CI record](../../evidence/repo/2026-10-09_ci-run-37924480165.md) |
| 11 | Design artefacts (handbook Table 1a) | Saif, Noor, Shahoud | Week 8 | 11 Oct | Done | [Design pack](../diagrams/design-pack.md): 21 diagrams generated from the code |
| 12 | System-level tests, setup and tool manuals | Saif | Week 8 | 11 Oct | Done | [Test catalogue](../manuals/system-test-cases.md); [manuals](../manuals/) |
| 13 | Panel action register with evidence | Shahoud | Week 8 | 11 Oct | Done | [Form 10](form-10-panel-actions.md) |
| 14 | CD and a deployed URL | Saif | Day 0 to 1 | Workflow and Render blueprint written; **not run, nothing deployed** | **Late** | [Deployment record](deployment-record.md) |
| 15 | Protected `main`, pull requests per member, tag `v0.1.0-mid1` | Saif; all | Day 0 onward | **None of it exists** | **Late** | [Repository evidence](../../evidence/repo/2026-10-11_repository-evidence.md) |
| 16 | Redaction of personal data before storage (FR-SEC-01, "should" for Mid-1) | Shahoud | Week 8 | Redactor written and tested, not applied | **Partly**, moved to Iteration 2 | Defect D-07 |
| 17 | Usability check with three people outside the team | Shahoud | Week 8 | Not done | **Not started** | Form 10, action A1 |
| 18 | Mid-1 report on the LaTeX template | All | Before the demo | Tracked separately | See the report folder | [`docs/report`](../report/) |
| 19 | Each member explains their module (handbook walkthrough) | All | Before the demo | Not demonstrated | **Not started** | [Code walkthrough](../manuals/code-walkthrough.md), section 6 |

**Done by.** Items 1 to 13 were produced in AI-assisted sessions run by Shahoud between 6 and 11 October and are logged in the [AI usage log](ai-usage-log.md). No item was produced by its planned owner where that owner is Noor or Saif. This is the main slippage, and it is a people-and-process slippage, not a feature one.

## Delays and recovery plan

| Delay | Cause | Recovery action | Owner | By |
|---|---|---|---|---|
| Work is not committed by its owners; history is one account in large batches (items 3 to 13, 15) | Three weeks without commits after the defense, then a compressed AI-assisted build on one machine | Commit the pending work in small commits by area, each owner from their own account after reading their area; from then on, branches and pull requests only ([CONTRIBUTING](../../.github/CONTRIBUTING.md)) | All; Shahoud coordinates | Before the Mid-1 meeting |
| No member has shown they understand the code (item 19) | Same | Each owner does the five-step exercise in the code walkthrough for their module and writes the "evidence of understanding" paragraph in the matching ADR | Noor: checks and attribution. Saif: verification, lifecycle, API. Shahoud: runner, workflow, UI | Before the Mid-1 meeting |
| No deployed URL, CD not run (item 14) | Needs a Render account, which only a member can create | Create the service from `render.yaml`, add the deploy hook secret and URL variable, push, save the run and the smoke-test line in `evidence/repo/` | Saif | Within 2 days of the push |
| `main` unprotected, no tag (item 15) | Never set up; protection on a private repository needs GitHub Pro (free for students) or a public repository | Decide Pro or public; add the rule; tag `v0.1.0-mid1` on the demonstrated commit | Saif | Before the Mid-1 meeting |
| Redaction not applied (item 16) | Redacting the stored trace breaks recorded replays; needs a token vault | Design recorded in D-07; build in Iteration 2 with tests | Shahoud | Week 10 |
| No usability evidence (item 17) | Not scheduled | Five tasks, three participants, task success and SUS; consent forms | Shahoud | Week 9 |
| Change record C-01 unsigned | Not yet presented | Bring it to the Mid-1 meeting for signature | Shahoud | Mid-1 meeting |

If the first two rows are not done before the meeting, say so in the meeting. The rubric scores "behind schedule but aware and tracking tasks" at 5 to 6 of 10 and "no credible recovery plan" at 3 to 4; dishonest milestone logging is a named red flag.

## Iteration 2: breadth and inputs (Mid-1 to FYP-1 final, release `v0.2.0`)

From the master plan, sections 26.1 and 35. Dates are semester weeks because the calendar mapping is unconfirmed.

| Week | Work | Owner | Buffer or risk |
|---|---|---|---|
| 9 | Trace import (JSON upload) with validation against the trace schema; second fault type; usability check | Shahoud | Import is new surface: budget two days for hostile-file tests |
| 9 to 10 | Check editor (create and test a check in the UI); fix D-25 (rank and score) | Noor | Depends on the check language limits, which exist |
| 10 | Redaction with a token vault (D-07); fix suggestion on a confirmed finding | Shahoud, Saif | Re-record the cassette if any prompt changes (about 15 minutes with a local model) |
| 11 | Python SDK and one LangGraph adapter; recovered run | Shahoud | Highest technical risk; cut to "SDK only" if late |
| 12 | Fault Lab batch runs; evaluation harness v0; PDF export | Noor, Saif | PostgreSQL has never been run (D-08): test it this week |
| 13 | Poster; benchmark v0 (more tasks, a baseline) | All; Noor leads the benchmark | Poster is a fixed external date |
| 14 | Report v2.0; install by a non-owner from the setup manual | All | One week of buffer before the final |
| 15 | FYP-1 final and poster evaluation | All | Code freeze 24 hours before |

## Earlier entries (kept from version 1.0)

| Date | Milestone | Note |
|---|---|---|
| 2026-09-11 | Proposal defense: approved, with five panel comments | [Form 10](form-10-panel-actions.md) |
| 2026-10-06 | Master plan v1.1; workspace reorganised; core library and Refund Desk working | Committed to `main` |
| 2026-10-07 | API, web UI, CI definition, feasibility run | Driven end to end in a browser |
| 2026-10-09 | First green CI run on GitHub, including the container build and smoke test | [CI record](../../evidence/repo/2026-10-09_ci-run-37924480165.md) |
| 2026-10-11 | Design pack, system tests, coding standards enforced, guide page, registers re-checked | Not yet committed |
