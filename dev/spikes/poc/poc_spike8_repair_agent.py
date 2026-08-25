# -*- coding: utf-8 -*-
"""
POC Spike 8 -- Repair Agent (minimal generation test)

Gap this closes: Repair Agent (plan doc S7.0, foundational item #6, added
2026-08-24 after reviewing Agentic_AI_Market_Survey_BS_FYP.docx) is the one
foundational feature with zero POC evidence -- risk-register.md R17.

What this tests: Spike 5 (counterfactual replay) deliberately tested only
the MECHANICAL question -- given a corrected value, does replaying downstream
recover the outcome -- and explicitly deferred "can an LLM generate the
correction" as a separate concern. This spike is that separate concern:
given a task, a wrong step output, and surrounding evidence, can the local
model GENERATE a usable corrected value? Then each generated value is fed
through a spike5-style deterministic downstream replay to see whether the
generated fix actually recovers a passing outcome -- chaining Repair Agent
into Verified Automatic Repair, matching the real intended pipeline.

Design choices, stated up front:
  - 6 synthetic cases, each a small single-step numeric correction embedded
    in a 2-step pipeline (extract/correct -> compute -> check), matching the
    GSM8K/tau-bench-style numeric domain already validated in Spike 4.
  - Backbone: local llama3.2:3b via Ollama (free), same as every other spike.
  - Evidence given to the model is unambiguous by design (a specific quoted
    fact that pins down the correct value) -- this tests whether Repair
    Agent can use given evidence to generate a fix, not whether it can also
    independently rediscover evidence Verification Agent would have surfaced.
  - Two metrics, matching the market survey's own Table 4 definitions:
    repair_success_rate (does the generated fix, once replayed downstream,
    produce a PASSING final result -- doesn't require exact match) and
    exact_match_rate (does the generated value exactly equal ground truth --
    stricter, reported separately, not conflated with repair_success_rate).
"""

import json
import re
import time

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


def ollama_generate(prompt: str, max_retries: int = 2) -> str:
    for attempt in range(max_retries + 1):
        try:
            resp = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "prompt": prompt, "stream": False,
                      "options": {"temperature": 0.2}},
                timeout=120,
            )
            resp.raise_for_status()
            return resp.json()["response"]
        except Exception as e:
            if attempt == max_retries:
                raise
            time.sleep(2)
    return ""


def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


REPAIR_PROMPT_TEMPLATE = """You are a Repair Agent in a multi-agent AI diagnosis system.
An earlier agent in a pipeline produced a value that has been diagnosed as WRONG.
Your job: generate the corrected value, using ONLY the evidence given below.

Task the pipeline was performing:
{task}

The wrong value an earlier agent produced:
{wrong_value}

Evidence that pins down the correct value:
{evidence}

Respond with ONLY a JSON object of the form:
{{"corrected_value": <number>, "reasoning": "<one short sentence>"}}
No other text.
"""

# Each case: task context, the injected-wrong value, the evidence Repair
# Agent is given, the true corrected value, and a downstream fn that takes
# the (possibly-generated) corrected value and returns whether the final
# pipeline outcome now passes -- mirrors Spike 5's replay-and-check pattern.
CASES = [
    {
        "id": "tax_total",
        "task": "Compute the total price including 8% tax for an item.",
        "wrong_value": "price = $90.00",
        "evidence": "The customer's original receipt, quoted verbatim in the trace, states: 'Item list price: $100.00.'",
        "true_value": 100.0,
        "downstream": lambda price: {"final_total": round(price * 1.08, 2), "expected": 108.0},
    },
    {
        "id": "loyalty_discount",
        "task": "Compute a refund: subtotal $45.00 minus the customer's loyalty discount.",
        "wrong_value": "discount = 5%",
        "evidence": "The customer's message, quoted in the trace, states: 'I have the 15% loyalty discount on my account.'",
        "true_value": 15.0,
        "downstream": lambda pct: {"final_total": round(45.00 * (1 - pct / 100), 2), "expected": 38.25},
    },
    {
        "id": "stock_count",
        "task": "Determine whether an order for 15 units can be fulfilled from current stock.",
        "wrong_value": "stock = 12 units",
        "evidence": "The warehouse inventory document, quoted verbatim in the trace, states: 'On-hand quantity: 21 units.'",
        "true_value": 21.0,
        "downstream": lambda stock: {"final_total": stock, "expected": 21.0},
    },
    {
        "id": "notebook_order",
        "task": "A store sells notebooks for $4 each. Compute the total cost of the customer's order.",
        "wrong_value": "quantity = 5 notebooks, so total = $20.00",
        "evidence": "The customer's message, quoted verbatim in the trace, states: 'I would like 7 notebooks please.'",
        "true_value": 7.0,
        "downstream": lambda qty: {"final_total": round(qty * 4, 2), "expected": 28.0},
    },
    {
        "id": "connecting_flight",
        "task": "A flight departs at hour 14 (24-hour clock). Compute the departure hour of the connecting flight, which leaves exactly 2 hours after arrival.",
        "wrong_value": "arrival hour = 13",
        "evidence": "The airline's official schedule, quoted verbatim in the trace, states: 'Flight 204 arrives at 14:00.'",
        "true_value": 14.0,
        "downstream": lambda hour: {"final_total": hour + 2, "expected": 16.0},
    },
    {
        "id": "budget_check",
        "task": "Determine whether an item is within a $500 budget.",
        "wrong_value": "item cost = $240.00",
        "evidence": "The vendor invoice, quoted verbatim in the trace, states: 'Total due: $420.00.'",
        "true_value": 420.0,
        "downstream": lambda cost: {"final_total": cost, "expected": 420.0},
    },
]


def run_case(case: dict) -> dict:
    prompt = REPAIR_PROMPT_TEMPLATE.format(
        task=case["task"], wrong_value=case["wrong_value"], evidence=case["evidence"]
    )
    raw = ollama_generate(prompt)
    parsed = extract_json(raw)

    result = {
        "case_id": case["id"],
        "true_value": case["true_value"],
        "raw_model_output": raw.strip(),
        "parsed": parsed,
    }

    if parsed is None or "corrected_value" not in parsed:
        result["parse_failure"] = True
        result["exact_match"] = False
        result["repair_success"] = False
        return result

    try:
        generated_value = float(parsed["corrected_value"])
    except (TypeError, ValueError):
        result["parse_failure"] = True
        result["exact_match"] = False
        result["repair_success"] = False
        return result

    result["parse_failure"] = False
    result["generated_value"] = generated_value
    result["exact_match"] = abs(generated_value - case["true_value"]) < 0.01

    replayed = case["downstream"](generated_value)
    result["replayed_downstream"] = replayed
    result["repair_success"] = abs(replayed["final_total"] - replayed["expected"]) < 0.01

    return result


if __name__ == "__main__":
    case_results = []
    for i, case in enumerate(CASES, 1):
        print(f"[{i}/{len(CASES)}] running case: {case['id']}", flush=True)
        case_results.append(run_case(case))

    n = len(case_results)
    n_parse_failures = sum(1 for r in case_results if r["parse_failure"])
    n_exact_match = sum(1 for r in case_results if r.get("exact_match"))
    n_repair_success = sum(1 for r in case_results if r.get("repair_success"))

    summary = {
        "n_cases": n,
        "n_parse_failures": n_parse_failures,
        "exact_match_rate": round(n_exact_match / n, 3),
        "repair_success_rate": round(n_repair_success / n, 3),
        "note": (
            "repair_success_rate follows the market survey's own Table 4 definition: "
            "does the generated fix, once replayed downstream, produce a passing "
            "final result -- it does not require an exact match to ground truth. "
            "exact_match_rate is reported separately, stricter, not conflated."
        ),
    }

    output = {"summary": summary, "cases": case_results}
    print(json.dumps(summary, indent=2))

    with open("poc_spike8_output.json", "w") as f:
        json.dump(output, f, indent=2)
