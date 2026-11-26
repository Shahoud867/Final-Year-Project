"""
POC Spike 2 — instrument one toy multi-agent workflow in CrewAI.

CrewAI is not used by any of the 7-9 papers in the literature review (they use
MetaGPT, AutoGen, Smolagents, AgentPrune, AFlow, OWL-Workforce, CaptainAgent/AG2,
MagenticOne). This is the point: prove the execution-graph trace model can
represent a genuinely unseen framework before spending real time on it in FYP-2.

Goal (per FYP_Scope_CCP_and_Implementation_Plan.md §10, spike 2):
  "Instrument one toy multi-agent workflow in CrewAI ... confirm the
  execution-graph data model can represent it."

This does NOT attempt to reproduce ErrorProbe (that's spike 1) or inject a
fault (that's spike 3, built on top of this trace). It only proves: can we
capture a clean, structured trace from a CrewAI run and turn it into a
dependency graph.
"""

import json
import time
from dataclasses import dataclass, field, asdict

from crewai import Agent, Task, Crew, Process, LLM


# ---------------------------------------------------------------------------
# 1. Trace capture — the data model this spike is actually testing
# ---------------------------------------------------------------------------

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
    depends_on: list = field(default_factory=list)  # node_ids this node consumed


TRACE: list[TraceNode] = []


def capture(node_id, agent_name, role, task_description, input_context, output, start_ts, depends_on):
    TRACE.append(TraceNode(
        node_id=node_id,
        agent=agent_name,
        role=role,
        task_description=task_description,
        input_context=input_context,
        output=str(output),
        start_ts=start_ts,
        end_ts=time.time(),
        depends_on=depends_on,
    ))


# ---------------------------------------------------------------------------
# 2. The toy multi-agent workflow: Planner -> Researcher -> Writer
# ---------------------------------------------------------------------------

llm = LLM(model="ollama/llama3.2:3b", base_url="http://localhost:11434")

planner = Agent(
    role="Planner",
    goal="Break the user question into 2 short sub-steps a researcher should answer.",
    backstory="A planning agent that decomposes tasks. Keep it very short.",
    llm=llm,
    verbose=False,
)

researcher = Agent(
    role="Researcher",
    goal="Answer the sub-steps factually and briefly, using only general knowledge.",
    backstory="A researcher agent that answers factual sub-questions concisely.",
    llm=llm,
    verbose=False,
)

writer = Agent(
    role="Writer",
    goal="Combine the research into one short, clear final answer (2-3 sentences).",
    backstory="A writer agent that synthesizes prior findings into a final answer.",
    llm=llm,
    verbose=False,
)

QUESTION = "What is the capital of France, and roughly what is its population?"

t0 = time.time()
plan_task = Task(
    description=f"User question: '{QUESTION}'. List exactly 2 short sub-steps to answer it. Be brief.",
    expected_output="A numbered list of 2 short sub-steps.",
    agent=planner,
)

t1 = time.time()
research_task = Task(
    description="Using the plan above, answer each sub-step briefly and factually.",
    expected_output="Short factual answers to each sub-step.",
    agent=researcher,
    context=[plan_task],
)

t2 = time.time()
write_task = Task(
    description="Combine the research above into one final answer, 2-3 sentences.",
    expected_output="A short final answer.",
    agent=writer,
    context=[research_task],
)

crew = Crew(
    agents=[planner, researcher, writer],
    tasks=[plan_task, research_task, write_task],
    process=Process.sequential,
    verbose=False,
)

print(f"[spike2] running toy CrewAI workflow on {QUESTION!r} via ollama/llama3.2:3b ...")
result = crew.kickoff()
print("[spike2] crew finished.")

# ---------------------------------------------------------------------------
# 3. Build the trace from CrewAI's own task outputs (post-hoc capture —
#    proves we can reconstruct a structured trace even without hooking
#    CrewAI's internals, which is the realistic instrumentation path for
#    an unfamiliar third-party framework)
# ---------------------------------------------------------------------------

capture("n1_plan", "Planner", planner.role, plan_task.description, QUESTION,
        plan_task.output.raw if plan_task.output else None, t0, depends_on=[])

capture("n2_research", "Researcher", researcher.role, research_task.description,
        str(plan_task.output.raw if plan_task.output else ""),
        research_task.output.raw if research_task.output else None, t1, depends_on=["n1_plan"])

capture("n3_write", "Writer", writer.role, write_task.description,
        str(research_task.output.raw if research_task.output else ""),
        write_task.output.raw if write_task.output else None, t2, depends_on=["n2_research"])

trace_out = [asdict(n) for n in TRACE]

# ---------------------------------------------------------------------------
# 4. Derive the execution graph (nodes = agent actions, edges = dependencies)
#    — this is the exact data model architecture-sketch.md's "execution-graph
#    construction" component needs to be able to build from a raw trace.
# ---------------------------------------------------------------------------

graph = {
    "nodes": [{"id": n["node_id"], "agent": n["agent"], "role": n["role"]} for n in trace_out],
    "edges": [
        {"from": dep, "to": n["node_id"]}
        for n in trace_out for dep in n["depends_on"]
    ],
}

out_path = "poc_spike2_trace_output.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"question": QUESTION, "final_answer": str(result), "trace": trace_out, "execution_graph": graph}, f, indent=2)

print(f"\n[spike2] final answer: {result}")
print(f"\n[spike2] execution graph: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges")
for e in graph["edges"]:
    print(f"  {e['from']} -> {e['to']}")
print(f"\n[spike2] full trace + graph written to {out_path}")
