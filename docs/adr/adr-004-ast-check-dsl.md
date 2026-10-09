# ADR-004: Checks are written in a small expression language evaluated over a restricted syntax tree

| | |
|---|---|
| Status | proposed (implemented) |
| Date | 2026-10-07 |
| Owner | to be assigned by the team |
| Reviewers | two other members, to be assigned |
| Related | `granite_core/dsl.py`, `checks.py`, master plan section 21.2 |

## Context

A user must be able to state what correct looks like (for example 'the refund in the message equals the catalogue total of the refunded items') without writing code, and the system must run that statement on data it did not write. Running user text with `eval` would let a check read files or run commands.

## Decision

Check expressions are parsed with Python's `ast` module and only a whitelist of node types is accepted: arithmetic, comparisons, boolean logic, field paths such as `s3.items_to_refund`, and a fixed set of functions (approx, sum, len, round, abs, min, max, contains, number_in, pluck, all, any, and `truth.<name>` calls into the workflow's source of truth). Limits: 500 characters, 150 nodes, depth 14. Anything else is rejected when the check is saved. A missing field gives ABSTAIN (not a failure); a runtime error gives ERROR.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| `eval` with restricted globals | Known sandbox escapes; cannot be made safe by filtering |
| JSONLogic or a rule engine | Another dependency with its own semantics; still needs custom functions such as `number_in` |
| Checks as Python functions | Cannot be edited in the UI; code review is the only safety net |
| An LLM as the judge | Not reproducible, and it shares the failure modes we are detecting |

## Consequences

25 hostile expressions (attribute access, calls to unknown names, dict literals, comprehensions, lambdas, f-strings, slices, exponentiation) are rejected in tests, and a property test shows arithmetic agrees with Python up to floating-point error. Arithmetic is IEEE double by design, so money is compared with a tolerance. The language cannot express loops or state; some checks may need a new `truth` function written in Python by a developer.

## Evidence of understanding (handbook C.14.1)

*To be written by the owner in their own words: explain the decision, justify it against the main alternative, predict what breaks if it changes, and say how you would modify it. This draft was prepared with AI assistance (see `docs/registers/ai-usage-log.md`) and is not evidence of understanding until the owner has written this section.*
