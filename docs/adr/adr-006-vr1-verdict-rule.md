# ADR-006: Decide verification verdicts with a fixed, published rule (VR-1)

| | |
|---|---|
| Status | proposed (implemented) |
| Date | 2026-10-07 |
| Owner | to be assigned by the team |
| Reviewers | two other members, to be assigned |
| Related | `granite_core/verification.py`, `experiment.py`, master plan section 14.3 |

## Context

'We replayed it and it looked fixed' is not evidence. A fix can pass by luck when a model is random, and a replay can pass because the replay itself is easier. We need a rule decided before the data, that includes a control.

## Decision

Replay the run from the suspected step N times with the correct value in place and M times without it (controls), with a different seed each time. CONFIRMED if at least 80% of the N pass and at most 20% of the M controls pass; REFUTED if at most 20% of the N pass; otherwise INCONCLUSIVE; ERROR if any replay or control did not finish. A replay passes only if every originally failing target check now passes and no originally passing check stops passing (regression guard). Report the Wilson 95% interval. Limits: N at most 10, M at most 5.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| One replay | Cannot separate the fix from model randomness |
| Majority vote over replays, no controls | A step that is not the origin can still look fixed if the replay happens to pass |
| Statistical test (p-value) | Needs larger N than we can afford at about 15 seconds per local model call |

## Consequences

The 20-row decision table in the tests fixes the rule's behaviour at every boundary. Controls double the cost of an experiment. N=5, M=2 is a pragmatic default, not a power calculation: with so few replays the interval is wide and the report must say so. Revisit the thresholds only through a new rule version (VR-2), never by editing VR-1.

## Evidence of understanding (handbook C.14.1)

*To be written by the owner in their own words: explain the decision, justify it against the main alternative, predict what breaks if it changes, and say how you would modify it. This draft was prepared with AI assistance (see `docs/registers/ai-usage-log.md`) and is not evidence of understanding until the owner has written this section.*
