# ADR-009: One versioned trace format for every run, replay and import

| | |
|---|---|
| Status | proposed (implemented) |
| Date | 2026-10-07 |
| Owner | to be assigned by the team |
| Reviewers | two other members, to be assigned |
| Related | `granite_core/trace.py`, `packages/granite_core/schema/granite-trace-v1.schema.json` |

## Context

Detection, attribution and replay all need the same facts about a run: which steps ran, what each read and produced, and which model call it made. A framework-specific format would tie the analysis to one framework.

## Decision

A trace is a JSON document with `schema_version: granite.trace/v1`, run metadata and at most 500 steps. Each step has an id, agent, kind (llm, tool, code, handoff), resolved inputs, outputs, declared reads of the form `step.field` or `task.field` that must point to an earlier step, model and parameters, prompt hash, error and timestamps. Unknown fields are rejected. The JSON Schema is exported from the pydantic model and a test fails if the committed file drifts.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| OpenTelemetry spans as the native format | Spans carry timing, not field-level data flow; kept as a possible import source |
| Store the framework's own objects | Not portable, not hashable in a stable way |

## Consequences

The `reads` declaration is what makes provenance possible, so a workflow author must declare them truthfully; an undeclared read makes attribution blind to that edge. Version 2 would need a migration for stored traces. Redaction exists in the core but is **not applied to stored traces** because replays need the original task input; the demo data is synthetic. This must be solved before real customer data is ever used.

## Evidence of understanding (handbook C.14.1)

*To be written by the owner in their own words: explain the decision, justify it against the main alternative, predict what breaks if it changes, and say how you would modify it. This draft was prepared with AI assistance (see `docs/registers/ai-usage-log.md`) and is not evidence of understanding until the owner has written this section.*
