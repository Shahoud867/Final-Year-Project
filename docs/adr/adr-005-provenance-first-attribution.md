# ADR-005: Rank where a failure began from recorded data flow first, structure second

| | |
|---|---|
| Status | proposed (implemented, feasibility-tested) |
| Date | 2026-10-07 |
| Owner | to be assigned by the team |
| Reviewers | two other members, to be assigned |
| Related | `granite_core/attribution.py`, `lineage.py`, master plan section 21.4, `research/eval/prereg-v1.md` |

## Context

A final answer can be wrong because of an earlier step. The PoC attributed blame with a language model and an answer key, which cannot be shown to a user as evidence. Granite records which step read which field of which earlier step, so a failing value can be followed backwards.

## Decision

For a failing symptom step, walk the recorded read edges backwards. Score each ancestor by the strongest evidence on it: truth mismatch 1.0, contract failure 0.8, handoff drift 0.7, unknown 0.2, consistent 0.1, multiplied by 0.9 per hop. If no ancestor has origin evidence (score at least 0.7), fall back to a structural ranking (betweenness of the step on paths to the symptom). The attribution function never receives the injected-fault record, so it cannot cheat.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| Ask an LLM which step is to blame | Not reproducible, not checkable, and the PoC measured 0-25% step accuracy |
| Blame the first failing check in order | A downstream check can fail first when the origin check is missing |
| Structural centrality only | Ranks important steps, not guilty ones; kept only as the fallback |

## Consequences

Gives a ranking that can be explained field by field and re-computed. The weights are design choices, not learned; they are fixed before the feasibility run and must not be tuned on its results. Weak spot: if a step has no check, the method can only say 'unknown'. Results on 10 tasks will be in `research/eval/results/`.

## Evidence of understanding (handbook C.14.1)

*To be written by the owner in their own words: explain the decision, justify it against the main alternative, predict what breaks if it changes, and say how you would modify it. This draft was prepared with AI assistance (see `docs/registers/ai-usage-log.md`) and is not evidence of understanding until the owner has written this section.*
