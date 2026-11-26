# -*- coding: utf-8 -*-
"""
POC Spike 4b -- the direct mechanism test, committed.

Why this file exists
--------------------
Spike 4 ran an n=3 live LLM task run. The model happened to get all three
tasks right, so that run contains ZERO naturally-occurring silent failures
and therefore says nothing about whether the detector catches one:
`n_true_silent_failure_cases: 0`, `detector_recall_on_silent_failures: null`.

A second, direct mechanism test WAS run at the time -- feeding the rule-based
checker known-wrong values, including a plausible-magnitude near-miss of a
stated $20.00 against a true $19.75 -- and it is described in
`markdowns/02-evidence-and-tracking/risk-register.md` (R10) and in
`AI_Usage_Log.md`. But neither its code nor its output was ever committed.

That left a claim appearing on the proposal deck ("catches a near-miss,
$20.00 vs $19.75") whose only cited source was a JSON file that does not
contain it. The claim is true -- it follows directly from the committed
checker -- but a panel member who opened the cited file would not find it.

This script closes that gap. It imports the EXACT checker function from
spike 4 (it does not reimplement it) and exercises it against seeded
known-wrong and known-correct values, writing a committed artifact.

What this does and does not establish
-------------------------------------
DOES: the rule-based checker, given a value that violates an independently
recomputed constraint, flags it -- including at near-miss magnitude, where a
naive "close enough" check would let it through. And it does not flag values
that are correct, including one that differs only by legitimate rounding.

DOES NOT: say anything about how often silent failures occur in the wild, or
what the detector's recall is on natural failures. That is still unmeasured,
and spike 4's n=3 run is why. Seeded inputs measure the mechanism, not the
phenomenon.

No LLM calls. No network. Deterministic.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# The same function the live spike uses -- imported, never re-implemented, so
# this test cannot drift from the detector it claims to be testing.
from poc_spike4_silent_failure_detector import rule_based_constraint_check  # noqa: E402

TOLERANCE = 0.01

# Each case: (id, stated, correct, should_flag, why this case is here)
CASES = [
    (
        "near_miss_gift_card",
        20.00, 19.75, True,
        "The case named in R10. 7 notebooks @ $4.25 less a $10 gift card is "
        "$19.75; $20.00 is plausible-magnitude wrong -- the exact shape a "
        "'close enough' check would wave through.",
    ),
    (
        "clean_control_gift_card",
        19.75, 19.75, False,
        "Same task, correct answer. Must not flag.",
    ),
    (
        "gross_error_gift_card",
        29.75, 19.75, True,
        "Gift card never subtracted. Easy case -- included so the near-miss "
        "result cannot be explained away as the checker flagging everything.",
    ),
    (
        "legit_rounding_compound_trip",
        1.68, 1.6833, False,
        "Differs by 0.0033, inside tolerance. A correct answer with rounding. "
        "Must not flag -- this is the false-positive boundary.",
    ),
    (
        "near_miss_discount_then_tax",
        68.00, 73.44, True,
        "$80 less 15% is $68.00, but 8% tax was never applied. Stopping one "
        "step early -- a well-formed, confident, wrong answer.",
    ),
    (
        "clean_control_discount_then_tax",
        73.44, 73.44, False,
        "Same task, correct answer. Must not flag.",
    ),
]


def main():
    results = []
    for case_id, stated, correct, should_flag, rationale in CASES:
        check = rule_based_constraint_check(stated, correct, TOLERANCE)
        flagged = check["matches_constraint"] is False
        results.append({
            "case_id": case_id,
            "stated_answer": stated,
            "correct_answer": correct,
            "tolerance": TOLERANCE,
            "detector_verdict": check["verdict"],
            "diff": check["diff"],
            "should_flag": should_flag,
            "detector_flagged": flagged,
            "correct_behaviour": flagged == should_flag,
            "why_this_case": rationale,
        })

    n_wrong = sum(1 for c in CASES if c[3])
    n_correct_vals = len(CASES) - n_wrong
    caught = sum(1 for r in results if r["should_flag"] and r["detector_flagged"])
    false_pos = sum(1 for r in results if not r["should_flag"] and r["detector_flagged"])

    summary = {
        "what_this_is": "Direct mechanism test of the spike 4 rule-based checker on seeded values. Not a live LLM run.",
        "n_cases": len(CASES),
        "n_known_wrong_values": n_wrong,
        "n_known_correct_values": n_correct_vals,
        "n_wrong_values_caught": caught,
        "n_false_positives": false_pos,
        "recall_on_seeded_wrong_values": round(caught / n_wrong, 4) if n_wrong else None,
        "precision_on_seeded_values": round(caught / (caught + false_pos), 4) if (caught + false_pos) else None,
        "near_miss_case_caught": next(
            r["detector_flagged"] for r in results if r["case_id"] == "near_miss_gift_card"
        ),
        "all_cases_behaved_correctly": all(r["correct_behaviour"] for r in results),
        "llm_calls": 0,
        "scope_note": (
            "These are SEEDED values, not naturally-occurring model errors. This "
            "measures the mechanism, not the phenomenon. Recall on natural silent "
            "failures remains unmeasured -- spike 4's live n=3 run produced zero "
            "natural failures to measure it on."
        ),
        "supersedes": (
            "The prose-only record of this test in risk-register.md R10 and "
            "AI_Usage_Log.md, which had no committed code or output artifact."
        ),
    }

    out = {"summary": summary, "results": results}
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "poc_spike4b_mechanism_output.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print("\n=== SPIKE 4b SUMMARY ===")
    print(json.dumps(summary, indent=2))
    for r in results:
        mark = "ok " if r["correct_behaviour"] else "BAD"
        print(f"  [{mark}] {r['case_id']:<32} stated={r['stated_answer']:<8} "
              f"true={r['correct_answer']:<8} -> {r['detector_verdict']}")


if __name__ == "__main__":
    main()
