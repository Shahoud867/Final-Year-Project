"""
POC Spike 5 — Counterfactual replay engine (minimal mechanism test)

Gap this closes: of the 5 foundational frozen features (plan doc §7.0), the
counterfactual replay engine was the only one with zero POC evidence.

What this tests: NOT whether an LLM can correctly guess a fix (that needs a
real API call and is a separate, larger concern already tracked elsewhere).
This tests the narrower, purely mechanical question: if you correct one
step's output and deterministically re-execute everything downstream, does
the pipeline's final outcome actually flip from failure back to success?
That's the load-bearing assumption the whole counterfactual-replay
architecture depends on, and it had never been checked at all.

Design: a 3-step deterministic pipeline (no LLM), so the test isolates the
replay mechanism itself from LLM correctness.
"""

import json

def step1_extract_price():
    """Simulates an agent extracting a price. Ground truth: 100."""
    return {"price": 100}

def step1_extract_price_CORRUPTED():
    """Same step, but with an injected fault (matches spike 3's fault type)."""
    return {"price": 90}  # corrupted: should be 100

def step2_apply_tax(step1_output):
    """Downstream agent, depends on step1's output."""
    return {"total": round(step1_output["price"] * 1.08, 2)}

def step3_check_against_expected(step2_output, expected_total=108.0):
    """Final agent — this is where the failure becomes visible."""
    return {"pass": abs(step2_output["total"] - expected_total) < 0.01,
            "final_total": step2_output["total"]}


def run_pipeline(step1_fn):
    s1 = step1_fn()
    s2 = step2_apply_tax(s1)
    s3 = step3_check_against_expected(s2)
    return {"step1": s1, "step2": s2, "step3": s3}


def counterfactual_replay(original_trace, corrected_step1_output):
    """
    The mechanism under test: given the corrected output for the injected
    fault's step, re-execute every downstream step deterministically and
    report whether the final outcome recovers.
    """
    s1_corrected = corrected_step1_output
    s2_replayed = step2_apply_tax(s1_corrected)
    s3_replayed = step3_check_against_expected(s2_replayed)
    return {"step1": s1_corrected, "step2": s2_replayed, "step3": s3_replayed}


if __name__ == "__main__":
    results = {}

    original = run_pipeline(step1_extract_price)
    results["original_correct_trace"] = original
    assert original["step3"]["pass"] is True, "sanity check: correct trace should pass"

    corrupted = run_pipeline(step1_extract_price_CORRUPTED)
    results["corrupted_trace"] = corrupted
    assert corrupted["step3"]["pass"] is False, "sanity check: corrupted trace should fail"

    replayed = counterfactual_replay(corrupted, corrected_step1_output={"price": 100})
    results["counterfactual_replay"] = replayed
    recovery_success = replayed["step3"]["pass"] is True

    results["recovery_success"] = recovery_success
    results["summary"] = (
        f"Corrupted trace failed (final_total={corrupted['step3']['final_total']}, "
        f"expected 108.0). After counterfactual correction of step1 and deterministic "
        f"re-execution of steps 2-3, final_total={replayed['step3']['final_total']}, "
        f"recovery_success={recovery_success}."
    )

    print(json.dumps(results, indent=2))

    with open("poc_spike5_output.json", "w") as f:
        json.dump(results, f, indent=2)
