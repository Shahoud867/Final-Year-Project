# ADR-002: Build a small workflow runner before adopting an agent framework

| | |
|---|---|
| Status | proposed (implemented) |
| Date | 2026-10-07 |
| Owner | to be assigned by the team |
| Reviewers | two other members, to be assigned |
| Related | `granite_core/runner.py`, master plan section 22 |

## Context

Verification replays a run from step k with a value changed and the earlier steps frozen. That needs exact control over which steps execute, with which inputs and which random seed. Frameworks such as LangGraph or CrewAI hide scheduling and state behind their own abstractions.

## Decision

A runner of about 250 lines that executes declared steps in order, records every step's resolved inputs, outputs, reads and model call, injects faults after a chosen step, and re-executes only the steps after an intervention (`execute_replay`). Framework adapters will map their traces into the same Granite Trace v1 later.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| Build directly on LangGraph | Freezing steps and capturing exact inputs would mean working around the framework before the first result |
| Instrument only, never run | Replay with controls is the project's core claim; it needs execution |

## Consequences

We can promise exactly what a replay does (frozen steps cost no model call; verified by a test that counts calls). We do not yet prove the idea works on framework traces; that is future work and must not be claimed now. Revisit when the first adapter is attempted.

## Evidence of understanding (handbook C.14.1)

*To be written by the owner in their own words: explain the decision, justify it against the main alternative, predict what breaks if it changes, and say how you would modify it. This draft was prepared with AI assistance (see `docs/registers/ai-usage-log.md`) and is not evidence of understanding until the owner has written this section.*
