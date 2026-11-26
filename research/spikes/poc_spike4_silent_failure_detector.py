# -*- coding: utf-8 -*-
"""
POC Spike 4 -- the one that was actually missing: does a rule-based
constraint-verification module catch a SILENT failure at all?

This is a different test from Spike 3. Spike 3 proved an INJECTED, KNOWN
fault propagates observably through a trace. This spike tests the opposite
and harder thing: can a naturally-occurring reasoning mistake -- one with no
injected corruption, no anomaly signal, nothing structurally wrong about the
step -- be caught by checking the output against an independently computed
constraint from the task itself?

No fault is injected here. The model is simply given a task tricky enough
that a small model may genuinely get it wrong on its own, and the detector's
job is to catch that on its own merits -- exactly what RQ3 claims is
possible and what, before this spike, had never actually been tried.

Per the API-usage architecture commitment (plan doc SS6): the detector itself
is rule-based -- it recomputes the correct answer from the task spec and
compares against the model's stated answer. Zero LLM calls in the detector.
"""

import json
import re
import time
from dataclasses import dataclass

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


@dataclass
class TaskCase:
    case_id: str
    prompt: str
    correct_answer: float
    tolerance: float = 0.01


# Tasks chosen to be genuinely error-prone for a small model (multi-step,
# with a step that's easy to skip or misapply -- not adversarial, just
# realistically tricky), NOT rigged to fail.
CASES = [
    TaskCase(
        "gift_card",
        "A store sells notebooks for $4.25 each. A customer buys 7 notebooks "
        "and pays using a $10 gift card first, then cash for the rest. "
        "How much cash, in dollars, does the customer still owe? "
        "End your answer with the exact line: FINAL ANSWER: $<number>",
        correct_answer=7 * 4.25 - 10,  # 19.75
    ),
    TaskCase(
        "discount_then_tax",
        "An item costs $80. It is first discounted by 15%, and then 8% sales "
        "tax is applied to the discounted price. What is the final price, in "
        "dollars? End your answer with the exact line: FINAL ANSWER: $<number>",
        correct_answer=80 * 0.85 * 1.08,  # 73.44
    ),
    TaskCase(
        "compound_trip",
        "A delivery van drives 45 miles at 60 mph, then stops for a 20-minute "
        "break, then drives another 30 miles at 50 mph. How many total hours, "
        "including the break, does the trip take? Round to two decimal places. "
        "End your answer with the exact line: FINAL ANSWER: <number> hours",
        correct_answer=45 / 60 + 20 / 60 + 30 / 50,  # 1.6333...
    ),
]


def ollama_generate(prompt: str) -> str:
    resp = requests.post(OLLAMA_URL, json={
        "model": MODEL, "prompt": prompt, "stream": False,
        "options": {"num_predict": 350, "temperature": 0.4},
    }, timeout=180)
    resp.raise_for_status()
    return resp.json().get("response", "")


def extract_final_number(text: str):
    """Rule-based extraction -- no LLM involved in checking the answer."""
    m = re.search(r"FINAL ANSWER:\s*\$?\s*(-?\d+(?:\.\d+)?)", text, re.IGNORECASE)
    if m:
        return float(m.group(1))
    # fallback: last number in the text
    nums = re.findall(r"-?\d+\.\d+|-?\d+", text)
    return float(nums[-1]) if nums else None


def rule_based_constraint_check(stated_answer, correct_answer, tolerance):
    """The actual silent-failure detector: recompute the constraint
    independently from the task spec and compare. Zero LLM calls."""
    if stated_answer is None:
        return {"verdict": "UNPARSEABLE", "matches_constraint": None}
    diff = abs(stated_answer - correct_answer)
    matches = diff <= tolerance
    return {
        "verdict": "PASS (no silent failure detected)" if matches else "FLAGGED (silent failure caught)",
        "matches_constraint": matches,
        "stated": stated_answer,
        "correct": round(correct_answer, 4),
        "diff": round(diff, 4),
    }


def main():
    results = []
    for case in CASES:
        t0 = time.time()
        raw_output = ollama_generate(case.prompt)
        elapsed = time.time() - t0

        stated = extract_final_number(raw_output)
        check = rule_based_constraint_check(stated, case.correct_answer, case.tolerance)

        # This is the case that actually matters for RQ3: the model gave a
        # confident, well-formed, structurally normal answer that happens to
        # be wrong -- no corruption, no anomaly, nothing an anomaly-gated
        # detector (like ErrorProbe's) would ever look twice at.
        looks_confident_and_normal = "FINAL ANSWER" in raw_output.upper() and len(raw_output) < 1200

        entry = {
            "case_id": case.case_id,
            "prompt": case.prompt,
            "correct_answer": round(case.correct_answer, 4),
            "raw_model_output": raw_output,
            "stated_answer": stated,
            "detector_verdict": check["verdict"],
            "model_was_actually_wrong": check["matches_constraint"] is False,
            "output_looked_structurally_normal": looks_confident_and_normal,
            "this_is_a_true_silent_failure_case": (
                check["matches_constraint"] is False and looks_confident_and_normal
            ),
            "elapsed_sec": round(elapsed, 1),
        }
        results.append(entry)
        print(f"[{case.case_id}] stated={stated} correct={round(case.correct_answer,4)} "
              f"-> {check['verdict']} ({elapsed:.1f}s)", flush=True)

    n_wrong = sum(1 for r in results if r["model_was_actually_wrong"])
    n_true_silent = sum(1 for r in results if r["this_is_a_true_silent_failure_case"])
    n_caught = sum(1 for r in results if r["this_is_a_true_silent_failure_case"]
                   and "FLAGGED" in r["detector_verdict"])

    summary = {
        "n_cases": len(CASES),
        "n_model_actually_wrong": n_wrong,
        "n_true_silent_failure_cases": n_true_silent,
        "n_caught_by_rule_based_detector": n_caught,
        "detector_recall_on_silent_failures": (
            round(n_caught / n_true_silent, 3) if n_true_silent else None
        ),
        "note": (
            "This is spike 4, not run before this pass. Tests the specific claim "
            "underlying RQ3: can a rule-based constraint check (zero LLM calls in "
            "the checker itself) catch a naturally-occurring, structurally-normal "
            "wrong answer with no injected corruption. n=3, first real data point "
            "on this claim -- not statistically meaningful, but no longer zero."
        ),
    }

    out = {"summary": summary, "results": results}
    with open("poc_spike4_silent_failure_output.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print("\n=== SPIKE 4 SUMMARY ===")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
