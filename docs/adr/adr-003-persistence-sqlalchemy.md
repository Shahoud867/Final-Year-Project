# ADR-003: SQLAlchemy with SQLite by default and PostgreSQL by connection string

| | |
|---|---|
| Status | proposed (partly implemented) |
| Date | 2026-10-07 |
| Owner | to be assigned by the team |
| Reviewers | two other members, to be assigned |
| Related | `apps/api/granite_api/models.py`, master plan section 22.5 |

## Context

The demo must run with zero setup and zero cost; a hosted instance would want PostgreSQL (the plan names Neon's free tier). Evidence rows must be append-only and findings must survive restarts.

## Decision

All persistence goes through SQLAlchemy 2 models (12 tables). SQLite with write-ahead logging is the default; any SQLAlchemy URL can be set in `GRANITE_DB_URL`. The canonical trace of a run is one JSON document on the run row; steps and graph edges are derived on read.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| PostgreSQL only | Adds a service to install before anything runs |
| Document store | Findings, hypotheses, experiments and reviews are relational and queried by status |
| Separate step and edge tables now | Duplicates the hashed trace; one document keeps a single source for replay and hashing |

## Consequences

**Only SQLite is tested.** A PostgreSQL run has not been performed; the claim 'PostgreSQL works' must wait for a test against a real instance (open item). Tables are created with `create_all`; there is no migration tool yet, so a schema change needs a new database or a hand migration. Alembic is the next step before any shared deployment.

## Evidence of understanding (handbook C.14.1)

*To be written by the owner in their own words: explain the decision, justify it against the main alternative, predict what breaks if it changes, and say how you would modify it. This draft was prepared with AI assistance (see `docs/registers/ai-usage-log.md`) and is not evidence of understanding until the owner has written this section.*
