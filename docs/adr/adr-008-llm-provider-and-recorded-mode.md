# ADR-008: Language models sit behind one interface, and every answer can be recorded and replayed

| | |
|---|---|
| Status | proposed (implemented) |
| Date | 2026-10-07 |
| Owner | to be assigned by the team |
| Reviewers | two other members, to be assigned |
| Related | `granite_core/llm.py`, `apps/api/granite_api/providers.py`, `data/cassettes/` |

## Context

Replays and tests need identical inputs to give identical outputs, a local 3-billion-parameter model is slow (about 5 to 15 seconds per short call) and sometimes wrong, and the demo must work without a model or a key. The model must be replaceable (local, hosted, recorded) without touching the analysis.

## Decision

The core defines an `LLMProvider` protocol and a request whose hash (model, messages, parameters, seed) is the key of a cassette file. Providers: `OllamaProvider`, `OpenAICompatProvider` (Groq, Gemini compatibility endpoint, vLLM), `RecordingProvider` (live plus save) and `RecordedProvider` (answers only from the cassette; an unknown request raises a clear error). Network code lives in the API layer, never in the core. Only http(s) endpoints are accepted.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| Call a hosted API directly in each step | Not replayable offline, costs money, leaks task data |
| Mock the model in tests only | The demo and the evidence would then not show real model behaviour |
| Cache by prompt text only | A different seed or model would wrongly hit the cache |

## Consequences

The cassette holds 249 real answers of `llama3.2:3b`; the API tests and the container demo run on it with no model. Recorded mode cannot answer a task nobody recorded; the API says so in the run's error. A cassette is only valid for the exact prompts it was recorded with: **changing any prompt invalidates it** and requires re-recording (about 15 minutes). Check the model licence before redistributing recorded outputs (see the licence register).

## Evidence of understanding (handbook C.14.1)

*To be written by the owner in their own words: explain the decision, justify it against the main alternative, predict what breaks if it changes, and say how you would modify it. This draft was prepared with AI assistance (see `docs/registers/ai-usage-log.md`) and is not evidence of understanding until the owner has written this section.*
