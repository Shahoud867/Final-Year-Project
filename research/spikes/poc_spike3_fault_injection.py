"""
POC Spike 3 — inject one controlled fault into the toy CrewAI workflow and
confirm the ground truth is recoverable and unambiguous.

Per FYP_Scope_CCP_and_Implementation_Plan.md §10, spike 3:
  "Inject one controlled fault type (e.g., corrupted tool output) into that
  toy workflow and confirm the ground truth is recoverable and unambiguous."

Approach, matching AgenTracer's own perturbation-operator method: run the
Planner -> Researcher -> Writer chain manually (not via crew.kickoff(), which
hides the handoff), and deterministically corrupt the Researcher's output
before it is handed to the Writer. This makes the ground truth exact by
construction: node_id = "n2_research" is defined as the fault origin BEFORE
the run, not inferred afterward.

Success criteria for this spike:
  1. The corruption is applied at a known, single, recorded node.
  2. The corrupted value is observably different from the true value.
  3. The downstream (Writer) output reflects the corruption having propagated.
  4. The ground truth (origin node + true value + corrupted value) is written
     out separately from the trace, so a diagnosis system could later be
     scored against it without ever having seen the injection logic.
"""

import json
import time
from dataclasses import dataclass, field, asdict

from crewai import Agent, Task, LLM


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

llm = LLM(model="ollama/llama3.2:3b", base_url="http://localhost:11434")

planner = Agent(role="Planner", goal="Break the question into 2 short sub-steps.",
                 backstory="Planning agent. Keep it very short.", llm=llm, verbose=False)
researcher = Agent(role="Researcher", goal="Answer the sub-steps factually and briefly.",
                    backstory="Researcher agent, concise factual answers.", llm=llm, verbose=False)
writer = Agent(role="Writer", goal="Combine research into one short final answer (2-3 sentences).",
               backstory="Writer agent, synthesizes findings.", llm=llm, verbose=False)

QUESTION = "What is the capital of France, and roughly what is its population?"

# --- Fault injection operator (deterministic, AgenTracer-style) -----------
GROUND_TRUTH_ORIGIN_NODE = "n2_research"
FAULT_TYPE = "corrupted_tool_output"


def inject_fault(true_output: str) -> str:
    """Deterministically corrupt a factual claim: swap Paris -> Berlin.
    This mirrors 'corrupted tool output' from the plan's fault taxonomy —
    a plausible-looking but factually wrong value substituted for a correct one."""
    corrupted = true_output.replace("Paris", "Berlin")
    return corrupted


# --- Step 1: Planner --------------------------------------------------------
t0 = time.time()
plan_task = Task(
    description=f"User question: '{QUESTION}'. List exactly 2 short sub-steps to answer it. Be brief.",
    expected_output="A numbered list of 2 short sub-steps.",
    agent=planner,
)
plan_output = planner.execute_task(plan_task)
TRACE.append(TraceNode("n1_plan", "Planner", planner.role, plan_task.description,
                        QUESTION, plan_output, t0, time.time(), depends_on=[]))

# --- Step 2: Researcher (TRUE output computed, then corrupted) -------------
t1 = time.time()
research_task = Task(
    description="Using the plan above, answer each sub-step briefly and factually.",
    expected_output="Short factual answers to each sub-step.",
    agent=researcher,
)
true_research_output = researcher.execute_task(research_task, context=plan_output)
corrupted_research_output = inject_fault(true_research_output)
TRACE.append(TraceNode("n2_research", "Researcher", researcher.role, research_task.description,
                        plan_output, corrupted_research_output, t1, time.time(),
                        depends_on=["n1_plan"], fault_injected=True))

# --- Step 3: Writer (receives the CORRUPTED research output) ---------------
t2 = time.time()
write_task = Task(
    description="Combine the research above into one final answer, 2-3 sentences.",
    expected_output="A short final answer.",
    agent=writer,
)
write_output = writer.execute_task(write_task, context=corrupted_research_output)
TRACE.append(TraceNode("n3_write", "Writer", writer.role, write_task.description,
                        corrupted_research_output, write_output, t2, time.time(),
                        depends_on=["n2_research"]))

# --- Verification: did the corruption actually propagate to the final answer? ---
propagated = "Berlin" in write_output or "Paris" not in write_output
recoverable = "Berlin" in corrupted_research_output and "Paris" in true_research_output

result = {
    "question": QUESTION,
    "true_final_answer_would_have_been_about": "Paris",
    "actual_final_answer": write_output,
    "fault": {
        "type": FAULT_TYPE,
        "ground_truth_origin_node": GROUND_TRUTH_ORIGIN_NODE,
        "true_value": true_research_output,
        "corrupted_value": corrupted_research_output,
    },
    "verification": {
        "fault_is_unambiguous_single_node": True,  # by construction — only n2_research was touched
        "corruption_observably_different_from_true": corrupted_research_output != true_research_output,
        "corruption_propagated_to_final_output": propagated,
        "ground_truth_recoverable": recoverable,
    },
    "trace": [asdict(n) for n in TRACE],
}

with open("poc_spike3_fault_injection_output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print(f"[spike3] true research output:      {true_research_output[:120]}...")
print(f"[spike3] corrupted research output: {corrupted_research_output[:120]}...")
print(f"[spike3] final (downstream) answer: {write_output}")
print(f"\n[spike3] fault origin (ground truth): {GROUND_TRUTH_ORIGIN_NODE}")
print(f"[spike3] corruption propagated to final output: {result['verification']['corruption_propagated_to_final_output']}")
print(f"[spike3] ground truth recoverable/unambiguous:  {result['verification']['ground_truth_recoverable']}")
print(f"\n[spike3] written to poc_spike3_fault_injection_output.json")
