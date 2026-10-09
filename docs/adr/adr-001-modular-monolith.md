# ADR-001: One repository, a framework-free core library and thin application layers

| | |
|---|---|
| Status | proposed (implemented) |
| Date | 2026-10-07 |
| Owner | to be assigned by the team |
| Reviewers | two other members, to be assigned |
| Related | master plan sections 22-23; `packages/granite_core`, `workflows/refund_desk`, `apps/api`, `apps/web` |

## Context

Three students, one semester, no operations budget. The product has one hard idea (find where a silent failure began, then prove it) and a lot of ordinary web plumbing. Plumbing must not be able to change the meaning of the hard idea, and the hard idea must be testable without a database, a web server or a language model.

## Decision

A single repository with four packages and one dependency direction: `granite_core` (pure Python, no web, database or network) <- `refund_desk` (a workflow) <- `granite_api` (HTTP, SQLite or PostgreSQL, background jobs) <- `apps/web`. One deployable image serves the API and the built UI.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| Microservices (runner, analysis, UI) | Three people cannot operate or debug them; every network hop adds failure modes that would obscure the ones we study |
| One flat application | Core logic would import web and database code, so the verdict rule and the attribution could not be unit-tested in isolation, and could not later be offered as an SDK |
| Notebook-only prototype | No input validation, no persistence, no review workflow; the panel asked for a product |

## Consequences

Easier: the core runs 204 tests in about 2 seconds with no I/O, at 98% coverage. Harder: values must be passed explicitly across layers (for example the harness view given to faults). Revisit if a second team needs to deploy the analysis separately from the API.

## Evidence of understanding (handbook C.14.1)

*To be written by the owner in their own words: explain the decision, justify it against the main alternative, predict what breaks if it changes, and say how you would modify it. This draft was prepared with AI assistance (see `docs/registers/ai-usage-log.md`) and is not evidence of understanding until the owner has written this section.*
