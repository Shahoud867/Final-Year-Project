# ADR-012: Connect to Phoenix and Langfuse through a separate, dependency-free connectors package

| | |
|---|---|
| Status | proposed (implemented on branch `feat/fyp1-final-scope`, 2026-11-15) |
| Date | 2026-11-15 |
| Owner | to be assigned by the team |
| Reviewers | two other members, to be assigned |
| Related | `packages/granite_connectors/`, `apps/api/granite_api/services/connections.py`, [integrations strategy](../plan/integrations-strategy.md), ADR-001, ADR-009, change C-07, FR-INT-01 to 06 |

## Context

Teams that build agent workflows already send traces to an observability platform; Arize Phoenix and Langfuse are the two most used free and open-source ones. Change C-07 asked for one real round trip in FYP-1: a run captured by a platform, read by Granite, traced back, replay-verified, and the verdict visible back in the platform. Four design questions had to be settled: where the code lives, how it talks HTTP, where API keys are kept, and what an imported trace may be used for.

## Decision

1. **A fourth package, `granite_connectors`,** between the core and the API. It may import the standard library, pydantic and `granite_core`, nothing else (`scripts/check_architecture.py` enforces this). The core stays free of network code; the API stays free of platform details.
2. **One neutral record, `SpanRecord`.** Each platform module converts its own JSON to it (`phoenix.from_phoenix`, `langfuse.from_langfuse`) and back (`to_phoenix`, `to_ingestion`); a single mapper (`mapping.map_trace`) builds Granite Trace v1. Lineage comes from declared reads (`granite.reads`), then distinctive values found in a later step's input, then step order, and every edge records which.
3. **HTTP through `urllib`** with retries on 408/425/429/5xx and `Retry-After`, http and https only. A transport function can be swapped, so tests run against in-memory servers (`granite_connectors.testing`) that follow the platforms' request and response shapes.
4. **No secrets in the database.** A connection stores the URL, project and step profile; keys come from `GRANITE_PHOENIX_API_KEY`, `GRANITE_LANGFUSE_PUBLIC_KEY` and `GRANITE_LANGFUSE_SECRET_KEY`.
5. **Imported traces are analysed like Granite's own runs** when their steps match the connection's workflow; otherwise they are skipped with the reason. Because that workflow is one Granite can execute, findings on such traces can be replay-verified (integrations strategy, section 4.6, route 1).
6. **Write-back on request only** (a "Send verdict" button): a Phoenix span annotation named `granite.verdict` with identifier `granite`, or a Langfuse categorical score with a stable id, so writing again updates instead of duplicating.
7. **Endpoints chosen for reach:** Phoenix REST v1 (`/v1/projects/{p}/spans`, `/v1/span_annotations`), checked against the Phoenix 21.0.0 server source; Langfuse `/api/public/observations` (v1, page-numbered), which works on Langfuse Cloud and self-hosted v3, rather than the Cloud-only cursor-based v2.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| Put the connectors in the API package | Mixes platform formats with HTTP handlers; the mapper could not be reused by a CLI or a scheduled sync |
| `httpx` or the vendors' SDKs | New dependencies (the Langfuse and Phoenix SDKs pull in OpenTelemetry and more) for four endpoints; `urllib` keeps `pip-audit` and the Docker image unchanged |
| Encrypt keys in the database with Fernet (the strategy's first proposal) | Adds `cryptography` and a key that must itself live in the environment; storing nothing secret is simpler and safer for FYP-1. Cost: one Langfuse key pair per server |
| Send runs through OpenTelemetry (OTLP) | Needs an OTel SDK and exporter in the workflow; the REST create-span and ingestion endpoints give the same result for runs already stored |
| Import every trace, matching or not | Running the Refund Desk checks on another application's trace would open false findings |

## Consequences

- A Refund Desk run sent to Phoenix and read back is identical to the original, step by step (`scripts/check_connectors_live.py`); checks fail the same way, attribution and replay work unchanged, and the verdict appears on the origin span in Phoenix.
- Langfuse support is written against the documented API and tested against an in-memory server, not a real instance: no Langfuse project or keys were available when it was built. The live check script runs it as soon as keys exist.
- Traces from other applications import only through a profile that maps their span names to a workflow Granite knows; general third-party traces (with their own checks and V1-only findings) are FYP-2 work, as is scheduled sync.
- Value-matched lineage is a heuristic and has not been measured on real third-party traces.
