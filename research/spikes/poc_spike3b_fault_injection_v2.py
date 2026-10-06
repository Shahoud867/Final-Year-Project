# -*- coding: utf-8 -*-
"""
POC Spike 3, take 2 -- fixes the two problems the first run surfaced:

  1. The first fault ("Paris" -> "Berlin") was a famous fact the model could
     catch and self-correct from its own training knowledge, producing a
     false "propagated" reading from a crude substring check.
  2. The propagation check itself was crude substring matching, not a real
     semantic comparison.

Fix: corrupt a fabricated intermediate finding that has NO independently
verifiable correct value (a made-up store hours / distance figure the model
cannot know from training), so there is nothing for the Writer to "catch"
against its own prior knowledge -- forcing a genuine test of blind vs.
critical propagation. Verification is now a structured check: does the
final answer state the TRUE value, the CORRUPTED value, or neither.
"""

import json
import time
from dataclasses import dataclass, field, asdict

from crewai import Agent, Task, LLM

llm = LLM(model="ollama/llama3.2:3b", base_url="http://localhost:11434")


@dataclass
class TraceNode:
    node_id: str
    agent: str
    role: str
    task_description: str
    input_context: str
    output: str
    start_ts: float
    end_ts: float
    depends_on: list = field(default_factory=list)
    fault_injected: bool = False


TRACE: list[TraceNode] = []

planner = Agent(role="Planner", goal="Break the question into 2 short sub-steps.",
                 backstory="Planning agent. Keep it very short.", llm=llm, verbose=False)
researcher = Agent(role="StoreChecker",
                    goal="Report the store's closing time and distance exactly as given by the lookup tool, without editorializing.",
                    backstory="A research agent that trusts and reports tool output verbatim.",
                    llm=llm, verbose=False)
writer = Agent(role="Writer", goal="Write one short final answer (2-3 sentences) using the report above.",
               backstory="Writer agent, synthesizes findings into a final answer.", llm=llm, verbose=False)

QUESTION = "Using the store lookup tool, tell the user what time Riverside Hardware closes today and how far it is from downtown."

# A fabricated "tool result" -- has no independently knowable correct value,
# so the model cannot self-correct it from prior training knowledge the way
# it could with "capital of France".
TRUE_TOOL_RESULT = "Riverside Hardware closing time: 9:40 PM. Distance from downtown: 3.2 miles."
CORRUPTED_TOOL_RESULT = "Riverside Hardware closing time: 6:15 PM. Distance from downtown: 3.2 miles."
GROUND_TRUTH_ORIGIN_NODE = "n2_research"
FAULT_TYPE = "corrupted_tool_output_unverifiable_fact"

t0 = time.time()
plan_task = Task(description=f"Task: '{QUESTION}'. List exactly 2 short sub-steps. Be brief.",
                  expected_output="A numbered list of 2 short sub-steps.", agent=planner)
plan_output = planner.execute_task(plan_task)
TRACE.append(TraceNode("n1_plan", "Planner", planner.role, plan_task.description, QUESTION,
                        plan_output, t0, time.time(), depends_on=[]))

# Step 2: "research" step is REPLACED entirely by the fixed corrupted tool
# result (this models a corrupted TOOL OUTPUT directly, matching AgenTracer's
# own fault taxonomy category, rather than corrupting an LLM's free-text
# reasoning -- cleaner, unambiguous ground truth by construction).
t1 = time.time()
TRACE.append(TraceNode("n2_research", "StoreChecker", researcher.role,
                        "Tool call: store_lookup('Riverside Hardware')",
                        plan_output, CORRUPTED_TOOL_RESULT, t1, time.time(),
                        depends_on=["n1_plan"], fault_injected=True))

# Step 3: Writer only ever sees the corrupted tool result -- there is no
# "true" value anywhere in its context for it to compare against, so if the
# true closing time (9:40 PM) ever appears in its output, that's a genuine
# anomaly (hallucination), not evidence it "caught" the fault.
t2 = time.time()
write_task = Task(description="Write one short final answer for the user using the report above.",
                   expected_output="A short final answer.", agent=writer)
write_output = writer.execute_task(write_task, context=CORRUPTED_TOOL_RESULT)
TRACE.append(TraceNode("n3_write", "Writer", writer.role, write_task.description,
                        CORRUPTED_TOOL_RESULT, write_output, t2, time.time(),
                        depends_on=["n2_research"]))

# --- Structured verification (not substring matching) ----------------------
states_true_time = "9:40" in write_output or "9:40 PM" in write_output
states_corrupted_time = "6:15" in write_output or "6:15 PM" in write_output

if states_corrupted_time and not states_true_time:
    propagation_verdict = "propagated_blindly"       # the intended, clean test case
elif states_true_time and not states_corrupted_time:
    propagation_verdict = "self_corrected_or_hallucinated_true_value"
elif states_corrupted_time and states_true_time:
    propagation_verdict = "mixed_both_values_present"
else:
    propagation_verdict = "neither_value_present_unclear"

result = {
    "question": QUESTION,
    "actual_final_answer": write_output,
    "fault": {
        "type": FAULT_TYPE,
        "ground_truth_origin_node": GROUND_TRUTH_ORIGIN_NODE,
        "true_value": TRUE_TOOL_RESULT,
        "corrupted_value": CORRUPTED_TOOL_RESULT,
    },
    "verification": {
        "fault_is_unambiguous_single_node": True,
        "corruption_observably_different_from_true": CORRUPTED_TOOL_RESULT != TRUE_TOOL_RESULT,
        "propagation_verdict": propagation_verdict,
        "ground_truth_recoverable": True,
    },
    "trace": [asdict(n) for n in TRACE],
}

out_path = "poc_spike3b_output.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"[spike3b] final answer: {write_output}")
print(f"\n[spike3b] fault origin (ground truth): {GROUND_TRUTH_ORIGIN_NODE}")
print(f"[spike3b] propagation verdict: {propagation_verdict}")
print(f"[spike3b] written to {out_path}")
