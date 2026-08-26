# -*- coding: utf-8 -*-
"""
POC Spike 1 -- reproduce ErrorProbe's methodology (simplified) against a small
Who&When-Hand-Crafted slice, and check whether the reproduction lands anywhere
near defensible territory before committing months of work to it as the
project's accuracy baseline.

Honest scope of this reproduction (documented, not hidden):
  - ErrorProbe's real pipeline is 3 stages: MAST-guided structural
    decomposition, symptom-driven backward tracing, and a 3-agent
    Strategist/Investigator/Arbiter team where the Investigator does
    TOOL-GROUNDED verification (re-running code in a sandbox, checking
    pre/post-conditions).
  - Who&When's Hand-Crafted cases are web-browsing / file-task trajectories,
    not executable code -- there is no sandbox to re-run them in. So this
    spike implements a 2-stage simplification: Strategist (hypothesis
    generation from the full labelled trajectory) -> Arbiter (final pick +
    confidence). No Investigator tool-grounding, no Verified Episodic Memory.
    This is a deliberate, stated scope cut for a POC, not an attempt to claim
    full fidelity to the paper.
  - Backbone: local llama3.2:3b via Ollama (free, CPU). ErrorProbe's own paper
    used Claude 3.7 Sonnet / GPT-OSS-120B / Qwen3-32B. Results here test
    whether the *pipeline logic* works at all -- they are NOT a fair
    apples-to-apples comparison to the paper's reported 59.5% step accuracy.

Ground truth schema (confirmed by inspecting the real downloaded files):
  case["mistake_agent"]  -- the culprit agent name (string)
  case["mistake_step"]   -- 0-indexed position directly into case["history"]
  case["history"]        -- list of {"role": ..., "content": ...}
"""

import json
import re
import sys
import time
from pathlib import Path

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"
DATA_DIR = Path(__file__).parent / "whowhen_data"
MAX_CONTENT_CHARS = 220  # per-step truncation, keeps prompt size sane for a 3B model on CPU


def ollama_generate(prompt: str, max_tokens: int = 500) -> str:
    # Timeout raised 300s -> 900s on 2026-08-26 re-run: the original 300s
    # client-side timeout killed a genuinely in-progress (not hung) local
    # CPU generation on case 2, after case 1 alone took 242s cold-start.
    # This is a network-robustness change only -- prompt, model, and
    # temperature are unchanged, so it does not affect scoring.
    resp = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": max_tokens, "temperature": 0.2},
    }, timeout=900)
    resp.raise_for_status()
    return resp.json().get("response", "")


def extract_json(text: str):
    """Best-effort JSON extraction from an LLM response that may wrap JSON in prose/fences."""
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def as_int(v):
    """Robust int coercion for step-index comparison.

    Bug fixed 2026-08-26: case["mistake_step"] is stored as a STRING in the
    Who&When data files (e.g. "5"), while the Arbiter's parsed JSON step is
    an int (5). The original `pred_step == gt_step` therefore silently
    returned False even when the values were numerically identical -- e.g.
    case 6, gt_step="5" vs pred_step=5 -- which drove step_accuracy to a
    reported 0.0 instead of the actual 12.5% (1/8). Coercing both sides to
    int before comparing fixes this without masking genuine mismatches:
    a real disagreement (e.g. "5" vs 20) still scores as incorrect.
    """
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return None


def build_numbered_trajectory(history: list) -> str:
    lines = []
    for i, turn in enumerate(history):
        role = turn.get("role", "?")
        content = str(turn.get("content", "")).replace("\n", " ").strip()
        if len(content) > MAX_CONTENT_CHARS:
            content = content[:MAX_CONTENT_CHARS] + "..."
        lines.append(f"[step {i}] ({role}): {content}")
    return "\n".join(lines)


def run_strategist(question: str, traj_text: str) -> dict:
    prompt = f"""You are diagnosing a FAILED multi-agent trajectory. The task below was NOT completed correctly.

TASK: {question}

NUMBERED TRAJECTORY (each line is one step, format [step N] (agent): content):
{traj_text}

Propose the 3 most likely (agent, step) hypotheses for which step and which agent is most responsible for the eventual failure. The responsible step is usually where a wrong action, wrong click, wrong conclusion, or missed detail was FIRST introduced -- not necessarily the last step.

Respond with ONLY this JSON, no other text:
{{"hypotheses": [{{"step": <int>, "agent": "<name>", "reason": "<short reason>"}}, {{"step": <int>, "agent": "<name>", "reason": "<short reason>"}}, {{"step": <int>, "agent": "<name>", "reason": "<short reason>"}}]}}
"""
    raw = ollama_generate(prompt, max_tokens=400)
    parsed = extract_json(raw)
    return {"raw": raw, "parsed": parsed}


def run_arbiter(question: str, hypotheses: dict) -> dict:
    prompt = f"""You are the final decision-maker for a failure-attribution diagnosis.

TASK: {question}

CANDIDATE HYPOTHESES from an investigator:
{json.dumps(hypotheses, indent=2)}

Pick the SINGLE most likely (agent, step) as the true root cause, with a confidence 0.0-1.0.

Respond with ONLY this JSON, no other text:
{{"agent": "<name>", "step": <int>, "confidence": <float 0-1>}}
"""
    raw = ollama_generate(prompt, max_tokens=150)
    parsed = extract_json(raw)
    return {"raw": raw, "parsed": parsed}


def main():
    files = sorted(DATA_DIR.glob("*.json"), key=lambda p: int(p.stem))
    results = []
    agent_correct = 0
    step_correct = 0
    parse_failures = 0

    for fp in files:
        case = json.loads(fp.read_text(encoding="utf-8"))
        gt_agent = case["mistake_agent"]
        gt_step = case["mistake_step"]
        question = case["question"]
        traj_text = build_numbered_trajectory(case["history"])

        t0 = time.time()
        strat = run_strategist(question, traj_text)
        if strat["parsed"] is None:
            parse_failures += 1
            results.append({"case": fp.name, "status": "strategist_parse_failed",
                             "gt_agent": gt_agent, "gt_step": gt_step,
                             "raw_strategist": strat["raw"][:400]})
            continue

        arb = run_arbiter(question, strat["parsed"])
        elapsed = time.time() - t0
        if arb["parsed"] is None:
            parse_failures += 1
            results.append({"case": fp.name, "status": "arbiter_parse_failed",
                             "gt_agent": gt_agent, "gt_step": gt_step,
                             "raw_arbiter": arb["raw"][:400]})
            continue

        pred_agent = arb["parsed"].get("agent")
        pred_step = arb["parsed"].get("step")
        a_ok = isinstance(pred_agent, str) and pred_agent.strip().lower() == gt_agent.strip().lower()
        gt_step_int, pred_step_int = as_int(gt_step), as_int(pred_step)
        s_ok = gt_step_int is not None and pred_step_int is not None and gt_step_int == pred_step_int
        agent_correct += int(a_ok)
        step_correct += int(s_ok)

        results.append({
            "case": fp.name, "status": "ok",
            "question": question,
            "gt_agent": gt_agent, "gt_step": gt_step,
            "pred_agent": pred_agent, "pred_step": pred_step,
            "confidence": arb["parsed"].get("confidence"),
            "agent_correct": a_ok, "step_correct": s_ok,
            "elapsed_sec": round(elapsed, 1),
            "strategist_hypotheses": strat["parsed"],
        })
        print(f"[{fp.name}] gt=({gt_agent},{gt_step}) pred=({pred_agent},{pred_step}) "
              f"agent_ok={a_ok} step_ok={s_ok} ({elapsed:.1f}s)", flush=True)

    n = len(files)
    n_scored = n - parse_failures
    summary = {
        "n_cases": n,
        "n_parse_failures": parse_failures,
        "n_scored": n_scored,
        "agent_accuracy": round(agent_correct / n_scored, 3) if n_scored else None,
        "step_accuracy": round(step_correct / n_scored, 3) if n_scored else None,
        "note": "2-stage simplified reproduction (Strategist->Arbiter, no tool-grounded "
                "Investigator, no memory), backbone=llama3.2:3b local, NOT directly "
                "comparable to ErrorProbe's own reported 59.5% (stronger backbones, full pipeline).",
    }

    out = {"summary": summary, "results": results}
    out_path = Path(__file__).parent / "poc_spike1_errorprobe_repro_output.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n=== SPIKE 1 SUMMARY ===")
    print(json.dumps(summary, indent=2))
    print(f"\nFull results written to {out_path}")


if __name__ == "__main__":
    main()
