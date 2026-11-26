# ADR-011: Take the corrected value for a replay from the failed check, not from a hand-written repair rule

| | |
|---|---|
| Status | proposed (implemented on branch `feat/fyp1-final-scope`, 2026-11-15) |
| Date | 2026-11-15 |
| Owner | to be assigned by the team (the completion plan proposes Noor) |
| Reviewers | two other members, to be assigned |
| Related | `granite_core/interventions.py`, `experiment.py` (`plan_intervention`), `refund_desk/definition.py`, ADR-004, ADR-006, change C-06 |

## Context

Verification (ADR-006) replays a run with the suspect step's output corrected. Until now the corrected value came from a repair rule the workflow author wrote by hand for each step (`REPAIRS` in `refund_desk/definition.py`). Two problems followed:

1. **Circularity.** The team wrote the fault, the check that catches it and the rule that undoes it. A panel can fairly say the confirmation proves only that our rule reverses our fault.
2. **Cost for a real user.** Nobody adopting Granite would write a repair expression for every step of their workflow before they can verify anything.

Yet a check that compares a step's output field with what it should be already contains the correct value: in `approx(s4.refund_amount, sum(pluck(s3.items_to_refund, 'price')))` the right-hand side is what `s4.refund_amount` should have been.

## Decision

When a step check fails, derive the intervention from it (`granite_core.interventions.derive_intervention`):

- recognise `<path> == <expr>` and `approx(<path>, <expr>)`, either way round, at the top level or as a conjunct of `and`;
- `<path>` must be a direct output field of the step under test;
- patch only conjuncts that are false, so a patch stays atomic;
- record the source as `check` and the ids of the checks used (`derived_from`).

Fall back to a workflow's repair rules only when no failed check names a value. Refund Desk now has no repair rules. Two of its step checks were rewritten (version 2) so they compare a field with its expected value instead of comparing totals: CT-LOOKUP (`s2.items == truth.catalog_items(s2.items)`) and CT-INTAKE (also compares the item names with the ones the message mentions). An outcome check, CHK-OUT-3, was added for requests that lose an item.

## Alternatives considered

| Alternative | Why rejected |
|---|---|
| Keep hand-written repair rules | The circularity objection stands, and a real user would have to write one per step |
| Ask an LLM for the corrected value | An unverified value would be tested by replay against itself; the master plan reserves model opinions for suggestions (product principle 1) |
| Invert any check expression symbolically | Not possible in general (`sum(...)`, `len(...)` lose information); the recognised forms cover the checks we write and fail safely on the rest |

## Consequences

- A step whose checks pass cannot be replayed: there is nothing to correct. The interface says "no automatic replay" and the API refuses with 422. Before, a no-op repair rule let such a step be replayed and refuted; a deliberate placebo intervention (`source: user`) now does that in tests and in the benchmark.
- Verification is only as good as check coverage: remove the origin's own check and its correct value is gone too. The benchmark's coverage ablation measures this (research/eval/prereg-v2.md).
- Check results for CT-LOOKUP now show lists of items instead of two totals, which is less compact on screen.
- The circularity is reduced, not removed: the team still writes the faults and the checks. The step towards removing it is a system with failures we did not author (the tau-bench Retail Agent, planned for FYP-2).

## Evidence of understanding

To be written by the owner after the code walkthrough.
