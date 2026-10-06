> **Superseded — kept intentionally, not to be updated.** This is the original, un-scoped ~10-layer pitch (observability platform + preventive clarification + counterfactual engine + dashboard + SDK + health scores + marketplace framing, all in one). The current, defensible scope is [FYP_Scope_CCP_and_Implementation_Plan.md](../../deliverables/stage-0-proposal/proposal-documents/FYP_Scope_CCP_and_Implementation_Plan.md), which deliberately trims this down to a committed core plus 13 explicitly-scheduled extensions. This file stays frozen on purpose — it's the "before" reference that shows why the current scope is narrower, not a document to sync forward.

# Granite / Agent Autopsy 2.0 / AgentTestLab — Pasted Pitch

*Verbatim content as pasted by the user in this session. Note: the original message was cut off by a 50,000-character limit partway through Section "10. AI Agent Health Score," so this file ends where the paste ended.*

---

Absolutely. Based on your requirements, I would **not** suggest a generic "AI chatbot," "disease prediction model," or simple dashboard. For a year-long FYP by **three AI & Data Science students**, the project should contain:

* a genuine research gap,
* a technically difficult AI problem,
* substantial data engineering,
* model development and evaluation,
* a deployable system,
* and enough separable components for all three members to have clear ownership.

I'm going to approach this as a **research-informed product proposal**, not just brainstorm random ideas. I'll compare recent research directions and look for ideas that can become both a **publishable research contribution** and a **real product**.

One direction is already standing out as particularly strong: **AI systems themselves are becoming a difficult object of research and engineering**.

Recent peer-reviewed work shows that identifying *which agent caused a multi-agent system to fail* and *at which exact step* remains surprisingly unsolved. A 2025 ICML paper reported only **53.5% accuracy for identifying the responsible agent and 14.2% for the decisive failure step** in its benchmark. A 2026 ACL paper further showed that full execution traces significantly improve attribution, while a 2026 AAAI paper still treats accurate failure localization as an open technical challenge. ([Proceedings of Machine Learning Research][1])

This is important because it suggests an FYP can target something deeper than "build an AI agent": **build the observability, diagnosis, and repair intelligence around AI agents**.

[1]: https://proceedings.mlr.press/v267/zhang25cq.html?utm_source=chatgpt.com "Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems"

# My strongest recommendation: **Agent Autopsy 2.0**

## An AI-powered observability, failure attribution, and recovery platform for multi-agent systems

After comparing the research landscape, **this is the idea I would seriously consider for your group**.

> **One-line FYP idea:**
> Build a system that observes an AI agent or multi-agent workflow, detects when and where a failure originated, identifies the responsible component, explains how the error propagated through the system, and recommends or tests possible recovery strategies.

Think of it as:

**Datadog / flight recorder / debugger — but specifically for AI agents.**

---

## 1. Why I think this is a strong FYP

Your requirements are actually a very good match for this problem.

| FYP Requirement           | How Agent Autopsy satisfies it                                               |
| ------------------------- | ---------------------------------------------------------------------------- |
| Research-informed problem | Based on recent ICML, ACL and AAAI research                                  |
| Complex computing problem | Root-cause analysis over long, dynamic, non-deterministic agent trajectories |
| Designed system           | Data collection + tracing + ML/LLM diagnosis + visualization + recovery      |
| Realistic deployment      | Can integrate with LangGraph, AutoGen, CrewAI-style or custom agent systems  |
| Systematic evaluation     | Benchmark against existing failure-attribution methods                       |
| Documentation             | Architecture, taxonomy, experiments, deployment and API docs                 |
| Individual ownership      | Natural separation into 3 substantial technical modules                      |

This is **not just another chatbot project**.

The product itself is useful, but there is also room for an actual research contribution.

---

# 2. The research evidence

This area is moving quickly, but importantly, **the problem is still not solved**.

### Baseline 1 — ICML 2025

The paper:

[Which Agent Causes Task Failures and When?](https://proceedings.mlr.press/v267/zhang25cq.html?utm_source=chatgpt.com)

introduced automated failure attribution for LLM multi-agent systems.

The researchers found that even strong methods struggled substantially: their best method achieved **53.5% agent-level attribution accuracy**, but only **14.2% accuracy for identifying the decisive failure step**. ([Proceedings of Machine Learning Research][1])

That is a massive signal that the problem remains difficult.

---

### Baseline 2 — ACL 2026

A newer paper:

[Seeing the Whole Elephant: TraceElephant](https://aclanthology.org/2026.acl-long.912/?utm_source=chatgpt.com)

argues that previous approaches were partly handicapped because debugging often used incomplete traces. Their benchmark uses fuller execution traces, and they report that full observability can improve attribution accuracy by up to **76.5%** relative to partial observation. ([ACL Anthology][2])

This creates an interesting FYP question:

> **Can better trace representation and causal reasoning improve failure diagnosis in realistic deployed agent systems?**

---

### Baseline 3 — AAAI 2026

The AAAI paper:

[Scope Delineation Before Localization](https://ojs.aaai.org/index.php/AAAI/article/view/40594?utm_source=chatgpt.com)

uses a two-stage strategy:

1. Identify the region where failure probably occurred.
2. Localize the exact failure.

It improved step-level attribution over prior methods, but it still demonstrates that precise localization is an active research problem rather than a solved engineering task. ([AAAI Publications][3])

---

### Baseline 4 — ACL Findings 2026

Another recent paper:

[Towards Self-Improving Error Diagnosis in Multi-Agent Systems](https://aclanthology.org/2026.findings-acl.98/?utm_source=chatgpt.com)

proposes ErrorProbe, using anomaly detection, backward tracing, multi-agent verification, and verified episodic memory. ([ACL Anthology][4])

So I want to be brutally honest:

## The original "Agent Autopsy" idea alone is no longer enough.

If your proposal is simply:

> "We will look at logs and tell which agent failed."

then **recent papers already do that**.

Your FYP needs a sharper contribution.

---

# 3. The improved idea: **Agent Autopsy 2.0**

I would position the project around something I think is more defensible:

## **Causal Failure Attribution and Failure Propagation Analysis for Multi-Agent AI Systems**

Most current work focuses primarily on:

> Which agent caused the failure?
> Which step was wrong?

Your system would go further:

> **What was the root cause, how did that error propagate through the agent network, how confident are we in that diagnosis, and what intervention would have prevented the final failure?**

That distinction is important.

---

# 4. Example

Imagine a research-agent workflow:

```text
User Query
    ↓
Planner Agent
    ↓
Research Agent
    ↓
Data Extraction Agent
    ↓
Analysis Agent
    ↓
Writer Agent
    ↓
Final Answer
```

The final answer is wrong.

A normal observability dashboard might say:

> ❌ Final answer incorrect.

A basic failure attribution system might say:

> Likely responsible agent: Research Agent
> Likely failure step: Step 4.

Your system would try to produce something like:

```text
ROOT CAUSE
──────────

Research Agent
Confidence: 0.84

Failure Type:
Unsupported source selection

Origin:
Step 4

Propagation Path:

Research Agent
       ↓
incorrect source
       ↓
Data Extraction Agent
extracts incorrect claim
       ↓
Analysis Agent
uses corrupted evidence
       ↓
Writer Agent
generates incorrect conclusion

Counterfactual Analysis:

If Step 4 had been replaced with
a verified source retrieval,
predicted task success probability:

0.31 → 0.79
```

That **failure propagation graph** and **counterfactual intervention analysis** could become your research contribution.

---

# 5. The core research question

A strong research question could be:

> **Can causal modeling of execution traces improve root-cause attribution and failure propagation analysis in LLM-based multi-agent systems compared with sequence-based and LLM-as-a-judge approaches?**

Possible sub-questions:

### RQ1

Can structured execution graphs outperform raw textual traces for failure localization?

### RQ2

Can causal dependency modeling identify the propagation path between an originating error and the final failure?

### RQ3

Can counterfactual interventions improve the reliability of root-cause explanations?

### RQ4

Can learned failure patterns transfer across different agent architectures?

This gives you an actual **AI + Data Science research problem**.

---

# 6. The proposed system architecture

I would build it as six major layers.

```text
                   AGENT AUTOPSY 2.0

┌──────────────────────────────────────────────┐
│              TARGET AGENT SYSTEM             │
│                                              │
│ Planner → Researcher → Analyst → Executor    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│            1. TRACE COLLECTION               │
│                                              │
│ • Agent inputs                               │
│ • Agent outputs                              │
│ • Tool calls                                 │
│ • Errors                                     │
│ • Execution timing                           │
│ • Intermediate state                         │
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│         2. TRACE → EXECUTION GRAPH           │
│                                              │
│ Nodes: agents / actions / artifacts          │
│ Edges: dependencies / information flow       │
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│       3. FAILURE DETECTION MODULE            │
│                                              │
│ • Task failure                               │
│ • Intermediate anomaly detection             │
│ • Consistency checking                       │
│ • Tool execution verification                │
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│      4. CAUSAL ROOT-CAUSE ANALYSIS           │
│                                              │
│ • Failure candidate generation               │
│ • Backward dependency tracing                │
│ • Causal ranking                             │
│ • Confidence estimation                      │
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│      5. COUNTERFACTUAL INTERVENTION          │
│                                              │
│ "What if this step were corrected?"          │
│                                              │
│ • Replay                                     │
│ • Step replacement                           │
│ • Alternative outputs                        │
│ • Success probability estimation             │
└──────────────────────┬───────────────────────┘
                       ▼
┌──────────────────────────────────────────────┐
│          6. AUTOPSY DASHBOARD                │
│                                              │
│ • Failure timeline                           │
│ • Agent dependency graph                     │
│ • Root cause                                 │
│ • Propagation path                           │
│ • Confidence                                 │
│ • Suggested recovery                         │
└──────────────────────────────────────────────┘
```

---

# 7. Where the actual complex computing problem is

This is crucial for your FYP proposal.

The complex computing problem is **not building the dashboard**.

The real problem is:

## Given a long, partially stochastic execution trace:

```text
T = {x₁, x₂, x₃, ..., xₙ}
```

determine:

```text
Root Cause
     ↓
Responsible Agent
     ↓
Responsible Action
     ↓
Failure Type
     ↓
Propagation Path
     ↓
Potential Intervention
```

The difficulty comes from:

### 1. Delayed error manifestation

The bad action may happen at:

```text
Step 3
```

but the failure may only appear at:

```text
Step 27
```

### 2. Error propagation

One agent may generate:

```text
Incorrect fact
```

Another agent:

```text
Uses it correctly
```

Another:

```text
Makes a perfectly logical conclusion
```

The final agent is not the real cause.

### 3. Non-determinism

The same workflow can behave differently on different executions.

### 4. Long-context reasoning

An agent may produce thousands of tokens and hundreds of tool interactions.

### 5. Inter-agent dependencies

The system isn't necessarily a simple sequence.

It may look like:

```text
        Planner
       /       \
Researcher    Database
     │            │
     └─────┬──────┘
           ↓
        Analyst
        /     \
    Critic   Writer
```

This becomes a **graph analysis and causal inference problem**, not merely an NLP classification task.

---

# 8. The AI/Data Science contribution

I recommend using a **hybrid approach**.

## Layer A — Failure taxonomy

Create or extend a taxonomy such as:

```text
Planning Failure
│
├── Missing decomposition
├── Wrong subtask
└── Incorrect dependency

Information Failure
│
├── Hallucination
├── Missing evidence
└── Source corruption

Tool Failure
│
├── Invalid parameters
├── Tool misuse
└── Execution failure

Communication Failure
│
├── Information loss
├── Context mismatch
└── Referential drift

Recovery Failure
│
├── Repeated error
├── Incorrect correction
└── Failure propagation
```

Recent ACL work also specifically highlights errors occurring at **agent-to-agent handoffs**, including categories such as data gaps, signal corruption, referential drift, and capability gaps. ([ACL Anthology][5])

You could expand this into a more operational taxonomy suitable for production tracing.

---

## Layer B — Execution graph

Convert raw logs into:

```text
G = (V, E)
```

Where:

* **V** = agent actions, messages, tool calls, artifacts
* **E** = dependency and information-flow relationships

Each node can contain features such as:

```text
Agent identity
Step number
Input embedding
Output embedding
Tool status
Latency
Token count
Error indicators
Semantic consistency score
```

---

## Layer C — Failure candidate scoring

Instead of asking an LLM:

> "Which step failed?"

generate candidate failure nodes.

For example:

```text
Node 17 → 0.12
Node 23 → 0.71
Node 24 → 0.82
Node 31 → 0.29
```

Use a combination of:

* anomaly detection,
* semantic inconsistency,
* dependency analysis,
* execution failure signals,
* graph features.

---

## Layer D — Causal propagation analysis

This could be your most interesting contribution.

Instead of:

```text
Bad Node → Final Failure
```

learn:

```text
Bad Node
    ↓
Intermediate corruption
    ↓
Dependency
    ↓
Downstream decision
    ↓
Final failure
```

Possible methods:

* graph neural networks,
* causal graphs,
* structural causal models,
* backward dependency tracing,
* counterfactual replay.

You don't necessarily need to invent a brand-new mathematical causal theory.

A strong undergraduate contribution could be:

> **A novel hybrid framework combining graph-based execution representation, semantic anomaly detection, and counterfactual replay for root-cause attribution.**

That is realistic.

---

# 9. The counterfactual engine

This is where I would differentiate your project.

Suppose:

```text
Step 14
Research Agent:
"The population of Pakistan is 120 million."
```

Later:

```text
Step 27
Analysis Agent:
calculates statistics using 120 million
```

Final:

```text
Step 41
Final answer fails validation
```

Your system asks:

> What happens if Step 14 is replaced?

Create interventions:

```text
do(Step14 = Corrected Output)
```

Then:

### Experiment A

```text
Original trace → Failure
```

### Experiment B

```text
Correct Step 14 → Replay downstream
```

### Experiment C

```text
Correct Step 20 → Replay downstream
```

Then estimate:

```text
Intervention Impact Score

Step 14 → +62%
Step 20 → +18%
Step 33 → +2%
```

The highest-impact upstream intervention is probably closer to the actual root cause.

This is much stronger than simply saying:

> "The LLM thinks Agent 2 made a mistake."

---

# 10. Product component

The research should become a usable product.

## Product name ideas

My favorites:

### **AgentAutopsy**

"Understand why your AI agents fail."

### **Granite**

"Find the cause, not just the error."

### **CausaAI**

"Causal debugging for AI agents."

### **AgentLens**

"Observability beyond logs."

My personal pick:

# **Granite**

It sounds more professional and scalable.

---

# 11. Dashboard

The dashboard could look like:

```text
┌───────────────────────────────────────────────────┐
│ Granite                       Run #1289         │
├───────────────────────────────────────────────────┤
│                                                   │
│ TASK STATUS                                       │
│ 🔴 FAILED                                         │
│                                                   │
│ ROOT CAUSE                                        │
│ Research Agent                                    │
│ Step 14                                           │
│ Confidence: 84%                                   │
│                                                   │
├───────────────────────────────────────────────────┤
│                                                   │
│ EXECUTION GRAPH                                   │
│                                                   │
│ Planner ─────► Researcher ─────► Analyst          │
│                  🔴                🟠             │
│                                    │              │
│                                    ▼              │
│                                  Writer           │
│                                    🔴             │
│                                                   │
├───────────────────────────────────────────────────┤
│ FAILURE PROPAGATION                               │
│                                                   │
│ Step 14 → Step 21 → Step 26 → Step 37             │
│                                                   │
├───────────────────────────────────────────────────┤
│ COUNTERFACTUAL TEST                               │
│                                                   │
│ Correct Step 14                                   │
│ Estimated success: 79%                            │
│                                                   │
└───────────────────────────────────────────────────┘
```

This makes for a very strong FYP demonstration.

---

# 12. Team division for three students

This is important because your department wants **traceable individual ownership**.

## Student 1 — AI & Failure Intelligence

### Ownership

* Failure taxonomy
* Failure detection
* Semantic anomaly detection
* LLM evaluation
* Attribution model

### Research contribution

```text
Which agent/step is suspicious?
```

---

## Student 2 — Graph + Causal Intelligence

### Ownership

* Trace normalization
* Execution graph construction
* Dependency modeling
* Failure propagation
* Counterfactual replay
* Root-cause ranking

### Research contribution

```text
How did the failure propagate?
What intervention would fix it?
```

---

## Student 3 — Systems + Data Engineering

### Ownership

* Trace ingestion SDK/API
* Agent framework integrations
* Database architecture
* Experiment pipeline
* Backend
* Visualization dashboard
* Deployment

### Engineering contribution

```text
How do we collect, store, process,
and visualize real agent executions?
```

This is much better than:

> Person 1 does frontend
> Person 2 trains model
> Person 3 makes backend.

Each member owns a **research or engineering subsystem**.

---

# 13. Evaluation methodology

You need a serious evaluation plan.

## Dataset/Benchmark 1

**Who&When**

Use it as an initial benchmark for:

* agent attribution,
* step attribution,
* failure classification.

[Who&When benchmark and ICML 2025 paper](https://proceedings.mlr.press/v267/zhang25cq.html?utm_source=chatgpt.com)

---

## Dataset/Benchmark 2

**TraceElephant**

A 2026 ACL benchmark emphasizing full execution traces and reproducible environments. ([ACL Anthology][2])

[TraceElephant ACL 2026](https://aclanthology.org/2026.acl-long.912/?utm_source=chatgpt.com)

---

## Dataset 3 — Your own benchmark

This is where your project becomes more valuable.

Build something like:

# **AgentProp**

A dataset containing:

```text
Task
Agent Architecture
Execution Trace
Failure
Root Cause Agent
Root Cause Step
Failure Type
Propagation Path
Recovery Intervention
```

For example:

```text
500–1,000 traces
```

across:

* research agents,
* coding agents,
* database agents,
* tool-using agents.

You can deliberately inject controlled failures:

```text
Wrong tool parameter
Hallucinated information
Missing context
Agent communication corruption
Incorrect plan
Tool failure
Repeated recovery failure
```

This allows you to know the actual ground truth.

That makes evaluation much more rigorous.

---

# 14. Metrics

Do not just report accuracy.

Use:

### Failure Detection

```text
Precision
Recall
F1
AUROC
```

### Root-Cause Attribution

```text
Top-1 Accuracy
Top-3 Accuracy
MRR
```

### Step Localization

```text
Exact Match
Mean Distance from True Step
Top-k Localization Accuracy
```

### Propagation Analysis

You can introduce:

```text
Propagation Path Precision
Propagation Path Recall
Path F1
```

Compare the predicted path:

```text
A → B → C
```

against the known ground truth.

### Counterfactual Evaluation

Measure:

```text
Recovery Success Rate

Task Success Before Intervention
vs
Task Success After Intervention
```

This is a very strong experimental section.

---

# 15. Baselines

You could compare against:

### Baseline A

Simple LLM-as-a-judge:

```text
Full trace → LLM → predicted failure
```

### Baseline B

ICML 2025 approaches from Who&When. ([Proceedings of Machine Learning Research][1])

### Baseline C

Two-stage scope-then-localization approaches from AAAI 2026. ([AAAI Publications][3])

### Baseline D

Recent self-improving diagnostic approaches such as ErrorProbe. ([ACL Anthology][4])

Your proposed model:

```text
Trace
 ↓
Structured Execution Graph
 ↓
Anomaly Detection
 ↓
Candidate Failure Nodes
 ↓
Backward Causal Tracing
 ↓
Counterfactual Replay
 ↓
Root Cause + Propagation Path
```

---

# 16. Why this is better than a typical healthcare FYP

Another strong direction would be multimodal healthcare AI. Recent reviews show that multimodal models can outperform unimodal approaches, but major challenges remain around missing modalities, alignment, interpretability, external validation, and real-world deployment. ([ScienceDirect][6])

However, for your team I would currently rank the agent-debugging idea higher because:

### Healthcare project risks

* dataset access problems,
* ethics concerns,
* medical validation difficulties,
* domain knowledge requirements,
* potentially expensive computing.

### Agent Autopsy advantages

* publicly available benchmarks,
* easy generation of additional data,
* realistic deployment possibilities,
* strong AI component,
* strong data engineering component,
* easier systematic experimentation.

---

# 17. My honest ranking of possible directions

| Rank | Idea                                    | Research Potential | FYP Feasibility | Product Potential |
| ---- | ---------------------------------------- | ------------------: | ---------------: | ------------------: |
| 🥇   | **Causal AI Agent Debugging**           |               9/10 |            9/10 |              9/10 |
| 🥈   | Multimodal Healthcare Anomaly Detection |               9/10 |            6/10 |              8/10 |
| 🥉   | Compression Robustness Analyzer         |             8.5/10 |            8/10 |              7/10 |
| 4    | Synthetic Data Quality Auditor          |               8/10 |            9/10 |              8/10 |
| 5    | Generic Multi-Agent Assistant           |               4/10 |           10/10 |              5/10 |

I would **not** recommend the generic multi-agent assistant because the market and research space are already overcrowded.

---

# 18. The exact FYP proposal I would take forward

## **Granite: A Causal Failure Attribution and Recovery Platform for LLM-Based Multi-Agent Systems**

### Problem

LLM-based multi-agent systems increasingly perform complex tasks, but debugging them is difficult because failures can originate in one agent and only become visible many steps later. Existing methods still struggle with accurate step-level attribution and often provide limited understanding of how errors propagate. ([Proceedings of Machine Learning Research][1])

### Proposed solution

Granite captures complete execution traces from multi-agent systems and transforms them into structured dependency graphs.

The system will:

1. detect anomalous execution,
2. identify likely failure candidates,
3. perform backward causal tracing,
4. identify the root-cause agent and step,
5. reconstruct the failure propagation path,
6. perform counterfactual interventions through selective replay,
7. recommend recovery strategies,
8. visualize the complete diagnosis.

### Research novelty

The proposed novelty is:

> **Combining structured execution graphs, semantic anomaly detection, backward causal tracing, and counterfactual replay for end-to-end failure attribution and propagation analysis.**

### Final output

A deployable platform containing:

* Python instrumentation SDK,
* backend API,
* trace database,
* failure diagnosis engine,
* causal analysis engine,
* experiment engine,
* interactive dashboard,
* benchmark dataset.

---

# 19. One warning

I want to be very honest with you because you previously asked me to be brutally honest about research gaps.

⚠️ **Do not claim that "failure attribution in multi-agent systems has never been studied."**

That claim is now clearly false.

The field is moving fast:

* ICML 2025 established automated failure attribution as a research problem. ([Proceedings of Machine Learning Research][1])
* AAAI 2026 improved localization with a two-stage strategy. ([AAAI Publications][3])
* ACL 2026 introduced full-trace benchmarking. ([ACL Anthology][2])
* ACL Findings 2026 introduced self-improving diagnosis with backward tracing and verified memory. ([ACL Anthology][4])
* Work is also emerging around workflow debugging and iterative refinement. ([ACL Anthology][7])

So the contribution needs to be more specific.

## The gap I would investigate is:

> **Current work mainly evaluates whether the responsible agent or failure step can be identified. A potentially valuable direction is to explicitly model the causal propagation chain and experimentally test counterfactual interventions to distinguish an early root cause from later downstream symptoms.**

That is a **research hypothesis**, not yet a guaranteed unexplored gap. Before locking the proposal, I would do a focused literature review specifically on **causal attribution, propagation graphs, and counterfactual debugging in LLM agent systems** to make sure the exact contribution is still novel.

---

## My recommendation

If I were in your group of three, with **one academic year**, I would seriously pursue **Granite / Agent Autopsy 2.0**.

It has the right combination of:

**AI research + Data Science + graph modeling + causal reasoning + software engineering + deployment + measurable experimentation.**

And unlike many FYP ideas, you can demonstrate it live:

> Run a multi-agent system → intentionally let it fail → Granite automatically analyzes the trace → identifies the root cause → shows how the failure propagated → tests a corrected intervention → reruns the workflow.

That would be a genuinely impressive FYP demo.

I can also take this one step further and turn it into a **full FYP research blueprint**: a literature-gap map, exact problem statement, novelty validation, system architecture, datasets, baselines, proposed methodology, semester-by-semester timeline, and a three-person work breakdown.

[1]: https://proceedings.mlr.press/v267/zhang25cq.html?utm_source=chatgpt.com "Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems"
[2]: https://aclanthology.org/2026.acl-long.912/?utm_source=chatgpt.com "Seeing the Whole Elephant: A Benchmark for Failure Attribution in LLM-based Multi-Agent Systems - ACL Anthology"
[3]: https://ojs.aaai.org/index.php/AAAI/article/view/40594?utm_source=chatgpt.com "Scope Delineation Before Localization: A Two-Stage Framework for Enhancing Failure Attribution in Multi-Agent Systems | Proceedings of the AAAI Conference on Artificial Intelligence"
[4]: https://aclanthology.org/2026.findings-acl.98/?utm_source=chatgpt.com "Towards Self-Improving Error Diagnosis in Multi-Agent Systems - ACL Anthology"
[5]: https://aclanthology.org/2026.acl-long.1294/?utm_source=chatgpt.com "AgentAsk: Multi-Agent Systems Need to Ask - ACL Anthology"
[6]: https://www.sciencedirect.com/science/article/pii/S1361841525001689?utm_source=chatgpt.com "Navigating the landscape of multimodal AI in medicine: A scoping review on technical challenges and clinical applications - ScienceDirect"
[7]: https://aclanthology.org/2026.acl-demo.3/?utm_source=chatgpt.com "PROTEA: Offline Evaluation and Iterative Refinement for Multi-Agent LLM Workflows - ACL Anthology"

Yes — and **this changes how I would design the FYP**.

If your university expects a **complete end-to-end product** and external API calls should contribute only around **15–20%**, then I would **not position Granite as just a dashboard or an API wrapper**.

The dashboard should be only the **visible interface**. The actual product should be a **complete AI Agent Testing, Failure Diagnosis, and Recovery Platform**.

# Better product vision: Granite as an AI Agent Testing Harness

Think of something closer to this:

```text
                    ┌──────────────────┐
                    │   Developer      │
                    │  / Researcher    │
                    └────────┬─────────┘
                             │
                    Upload / Configure
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│                    TRACECAUSE PLATFORM                  │
│                                                        │
│  1. Agent/Workflow Registration                        │
│                                                        │
│  2. Test Scenario Generator                            │
│                                                        │
│  3. Agent Execution Harness                            │
│                                                        │
│  4. Failure Injection Engine                           │
│                                                        │
│  5. Trace Collection                                   │
│                                                        │
│  6. Execution Graph Builder                            │
│                                                        │
│  7. Failure Detection Model                            │
│                                                        │
│  8. Root Cause Attribution Engine                      │
│                                                        │
│  9. Failure Propagation Analysis                       │
│                                                        │
│ 10. Counterfactual Recovery Engine                     │
│                                                        │
│ 11. Evaluation & Benchmarking Engine                   │
│                                                        │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
              ┌────────────────────┐
              │ Product Interface  │
              │                    │
              │ • Test Results     │
              │ • Trace Explorer   │
              │ • Failure Graph    │
              │ • Root Cause       │
              │ • Recovery Tests   │
              └────────────────────┘
```

## So the final product is:

# **A testing and debugging platform for multi-agent AI systems**

Not:

> "A dashboard that sends traces to GPT and asks why the agent failed."

That would indeed be weak and overly dependent on APIs.

---

# What the user actually does

Imagine a developer has built this workflow:

```text
User Question
      ↓
Planner Agent
      ↓
Research Agent
      ↓
Database Agent
      ↓
Analysis Agent
      ↓
Final Response
```

They connect their workflow to Granite using your SDK or interface.

For example:

```python
from tracecause import trace

@trace(agent="researcher")
def research(query):
    ...
```

Or through a visual workflow configuration.

Then they can create a **test suite**.

```text
Test Suite: Research Agent Reliability

Test 1
Question requiring multiple sources

Test 2
Conflicting information

Test 3
Missing tool response

Test 4
Invalid database result

Test 5
Long-context information

Test 6
Incorrect message passed between agents
```

Then they press:

# Run Evaluation

Your system executes the workflow and produces:

```text
RUN #142
──────────────────────────

Status: FAILED

Task Success Score: 0.42

Root Cause:
Research Agent

Origin Step:
14

Failure Type:
Information Corruption

Propagation:

Research Agent
        ↓
Database Agent
        ↓
Analysis Agent
        ↓
Final Response

Recovery Simulation:

Replace output at Step 14

Predicted Result:

SUCCESS PROBABILITY
0.31 → 0.78
```

**That is a complete product.**

---

# The important part: your own computation should dominate

I would design the project so roughly:

```text
┌─────────────────────────────────┐
│ Your Own System                 │
│                                 │
│ Data Processing        20%      │
│ Graph Construction     15%      │
│ Failure Detection      15%      │
│ Root Cause Analysis    15%      │
│ Failure Propagation    10%      │
│ Counterfactual Engine  10%      │
│ Testing/Benchmarking   10%      │
└─────────────────────────────────┘

External LLM/API
≈ 15–20% maximum
```

The exact percentages are illustrative, but the philosophy should be:

> **The API produces agent behavior; your system does the actual analysis.**

---

# What APIs should be used for

External APIs can be used only where they make sense.

For example:

```text
Agent Under Test
        │
        ▼
LLM API
(OpenAI / Gemini / local model)
```

But your own system should perform:

### Your code

* collecting traces,
* parsing traces,
* constructing dependency graphs,
* generating graph features,
* anomaly detection,
* failure classification,
* candidate ranking,
* backward tracing,
* propagation analysis,
* counterfactual testing,
* benchmark generation,
* evaluation metrics.

So even if you completely remove GPT from the **diagnosis engine**, the product should still work.

That is the design I would aim for.

---

# The strongest architecture: Harness + Intelligence + Dashboard

Instead of one product component, build **three layers**.

## Layer 1 — Granite Harness

This is the product's entry point.

The user can:

* register agents,
* define workflows,
* define tests,
* execute workflows,
* inject failures,
* collect traces.

For example:

```text
┌──────────────────────────────┐
│ AGENT TEST HARNESS           │
├──────────────────────────────┤
│                              │
│ Workflow:                    │
│                              │
│ [Planner]                    │
│     ↓                        │
│ [Researcher]                 │
│     ↓                        │
│ [Analyst]                    │
│     ↓                        │
│ [Writer]                     │
│                              │
│ Test Cases: 25               │
│                              │
│ [ RUN TEST SUITE ]           │
│                              │
└──────────────────────────────┘
```

This alone is a meaningful engineering component.

---

# Layer 2 — Your AI/Data Science engine

This is where the academic complexity lives.

The raw trace:

```text
Agent A
Input
Output

Agent B
Input
Output

Tool Call
Result

Agent C
Input
Output
```

gets converted into structured data.

```text
Node 1
Agent: Planner
Step: 1
Latency: 1.2 sec
Input Embedding: [...]
Output Embedding: [...]

Node 2
Agent: Researcher
Step: 2
Tool: Search
Status: Success

Node 3
Agent: Researcher
Step: 3
Output: [...]
```

Then construct:

```text
Execution Dependency Graph
```

For example:

```text
       Node 1
       Planner
          │
      ┌───┴────┐
      ▼        ▼
   Node 2    Node 3
 Research   Database
      │        │
      └───┬────┘
          ▼
        Node 4
        Analyst
          │
          ▼
        Node 5
        Writer
```

Now your model analyzes the graph.

---

# Layer 3 — Dashboard

The dashboard is simply the interface.

It should allow users to explore:

### Run History

```text
Run ID       Status
────────────────────
#142         ❌ Failed
#141         ✅ Passed
#140         ❌ Failed
#139         ⚠ Partial
```

### Failure Analytics

```text
Most Failure-Prone Agent

Research Agent
Failure Rate: 34%

Most Common Error:

Information Corruption
```

### Trace Explorer

Users click:

```text
Planner
   ↓
Researcher 🔴
   ↓
Analyst 🟠
   ↓
Writer
```

and inspect the exact failure.

So yes, there **will** be a dashboard.

But the dashboard is probably only **15–20% of the actual project**.

---

# I would add a very important component: Failure Injection

This makes your project much stronger.

Your harness deliberately introduces controlled failures.

For example:

## Communication corruption

Original:

```text
Pakistan GDP = X
```

Injected:

```text
Pakistan GDP = NULL
```

---

## Tool failure

```text
Database Query
        ↓
Timeout
```

---

## Context loss

```text
Agent receives only 40%
of previous information
```

---

## Incorrect tool result

```text
Correct Result

↓ Injection

Incorrect Result
```

---

## Agent hallucination

A controlled corrupted intermediate answer.

Why is this useful?

Because you now know:

```text
TRUE ROOT CAUSE = Step 14
```

Then your system predicts:

```text
PREDICTED ROOT CAUSE = Step 14
```

Now you can scientifically evaluate:

```text
Accuracy = ?
Precision = ?
Recall = ?
Propagation Path F1 = ?
```

This gives you a **controlled benchmark generation framework**.

That is much more academically defensible than manually saying:

> "We looked at the logs and think the model did well."

---

# The product could actually be called a "TestLab"

I think this positioning may be better than just calling it an observability platform.

## Possible final product:

# **AgentTestLab**

> **An intelligent testing, debugging, and failure analysis platform for AI agent workflows.**

The product lifecycle becomes:

```text
              DESIGN
                │
                ▼
          Register Workflow
                │
                ▼
            TEST
                │
                ▼
        Execute Test Suite
                │
                ▼
          INJECT FAILURES
                │
                ▼
          COLLECT TRACES
                │
                ▼
          ANALYZE FAILURE
                │
                ▼
        FIND ROOT CAUSE
                │
                ▼
        ANALYZE PROPAGATION
                │
                ▼
         TEST RECOVERY
                │
                ▼
           FINAL REPORT
```

Now you have a genuine **end-to-end product pipeline**.

---

# What the final deliverable could look like

The examiner sees:

## 1. Web Platform

The developer logs in.

Creates:

```text
Project:
Customer Support Agent
```

Registers:

```text
Planner
Retriever
Knowledge Agent
Response Agent
```

---

## 2. Workflow Integration

Your SDK:

```text
tracecause.start_run()

tracecause.log_agent_input()

tracecause.log_agent_output()

tracecause.log_tool_call()

tracecause.end_run()
```

Or automatic integration with selected frameworks.

---

## 3. Test Suite Builder

The user creates:

```text
Test Scenario A
Normal task

Test Scenario B
Missing information

Test Scenario C
Tool timeout

Test Scenario D
Contradictory data

Test Scenario E
Communication corruption
```

---

## 4. Execution Engine

Your backend runs:

```text
25 tests
×
5 repetitions
=
125 execution traces
```

---

## 5. AI Diagnosis

Your models perform:

```text
Trace
 ↓
Feature Extraction
 ↓
Graph Construction
 ↓
Anomaly Detection
 ↓
Failure Candidates
 ↓
Root Cause Ranking
 ↓
Propagation Analysis
```

---

## 6. Recovery Engine

The system can test:

```text
Fix Candidate 1

Fix Candidate 2

Fix Candidate 3
```

Then report:

```text
Recommended Intervention:

Replace Research Agent output
at Step 14

Expected Recovery Improvement:

+47%
```

---

# Three-person ownership becomes even cleaner

## Person 1 — Agent Testing Harness

**Major module:**

```text
AgentTest Harness
```

Responsible for:

* agent registration,
* workflow definition,
* execution environment,
* test case management,
* failure injection,
* trace collection.

This is a serious software engineering component.

---

## Person 2 — AI Failure Diagnosis

**Major module:**

```text
Failure Intelligence Engine
```

Responsible for:

* feature extraction,
* anomaly detection,
* failure classification,
* root cause prediction,
* agent/step ranking.

This is the strongest traditional AI/Data Science component.

---

## Person 3 — Causal Analysis & Product Platform

**Major module:**

```text
Causal Recovery Platform
```

Responsible for:

* execution graph,
* propagation modeling,
* counterfactual replay,
* evaluation pipeline,
* backend integration,
* dashboard.

---

# My revised recommendation

I would **not** submit the FYP as:

> "A dashboard for analyzing multi-agent failures."

That sounds too small.

I would submit it as:

# **AgentTestLab: An Intelligent Testing, Failure Attribution, and Recovery Framework for LLM-Based Multi-Agent Systems**

### The final product:

> A complete testing harness that allows developers to register AI agent workflows, automatically execute test scenarios, inject controlled failures, collect execution traces, identify root causes using graph-based and machine-learning techniques, analyze failure propagation, test corrective interventions, and visualize system reliability.

That sounds like a **full AI/Data Science product**, not an API project.

And most importantly:

**Even if you replace the LLM API with a local model or a dummy agent, your core FYP still exists and works.**

That is the test I would use. If removing the API destroys the project, then the project is too API-dependent. In this architecture, the API is merely one component used to generate or run agent behavior; **the intellectual and computational core is your own system**.

I can next help you **redesign this into a complete FYP proposal architecture with exact modules, technologies, datasets, algorithms, and a realistic one-year development timeline**, while explicitly keeping third-party API usage under the 20% contribution limit.

Yes. Think of the product from the **user's perspective** as an **AI Agent Testing & Debugging Platform**. The user should get much more than a dashboard.

# 🎯 AgentTestLab — User Features

## 1. Project & Agent Workflow Management

The user can create a project and register their AI system.

For example:

```text
Project: AI Research Assistant

Agents:

[Planner]
     ↓
[Researcher]
     ↓
[Data Analyst]
     ↓
[Writer]
```

The user can define:

* agents
* agent roles
* workflow sequence
* inputs and outputs
* tools used by agents
* dependencies between agents

### User benefit

> "I can see and manage how my AI system works."

---

# 2. Connect Their Existing Agent System

The user should not have to rebuild their entire agent system.

They integrate it with your platform using a lightweight SDK.

Conceptually:

```python
from agenttestlab import trace_agent

@trace_agent(name="Researcher")
def research(query):
    ...
```

The SDK captures:

* input
* output
* timestamps
* execution time
* tool calls
* errors
* parent/child dependencies

### User benefit

> "I can connect my existing AI agent workflow and observe it."

This is a product feature, but the API/SDK itself is **not the core intelligence** of your FYP.

---

# 3. Test Suite Builder 🧪

This should be one of the major product features.

The user can create test cases for their agent.

Example:

| Test | Scenario            | Expected Behaviour                    |
| ---- | -------------------- | -------------------------------------- |
| T01  | Normal query         | Successful answer                     |
| T02  | Missing information  | Agent asks/reports limitation         |
| T03  | Conflicting data      | Agent detects conflict                |
| T04  | Tool failure          | Agent recovers                        |
| T05  | Long context          | Agent maintains important information |

The user can either:

### Option A — Create manually

```text
Test Name:
Research with conflicting sources

Input:
Compare two contradictory reports.

Expected:
Detect contradiction.
```

### Option B — Automatically generate tests

Your own system can analyze the workflow and suggest test scenarios.

For example:

```text
Detected:

Research Agent
↓
External Search Tool

Suggested Tests:

✓ Empty search result
✓ Contradictory sources
✓ Invalid source
✓ Tool timeout
✓ Partial result
```

### User benefit

> "I can systematically test whether my AI agents actually work."

---

# 4. Automated Agent Evaluation

The user clicks:

# ▶ Run Test Suite

The system executes:

```text
50 Test Cases
       ×
3 Runs Each
       ↓
150 Agent Executions
```

Then produces:

```text
Overall Reliability: 78%

Passed: 117
Failed: 24
Partial Failure: 9
```

The user can compare different versions:

```text
Version 1.0 → 68%
Version 1.1 → 76%
Version 1.2 → 82%
```

### User benefit

> "I can measure whether changes actually improved my agent."

---

# 5. Failure Injection Engine 💥

This is a feature I think can make your FYP particularly interesting.

The user can intentionally test failures.

For example:

## Tool failure

```text
☑ Simulate timeout
☑ Simulate invalid response
☑ Simulate missing response
```

## Communication failure

```text
☑ Remove information
☑ Corrupt information
☑ Truncate context
☑ Send contradictory message
```

## Data failure

```text
☑ Missing data
☑ Incorrect data
☑ Noisy data
```

Then the system asks:

> **Does your agent system survive this failure?**

Example result:

```text
Test: Database Timeout

❌ System Failed

Root Cause:
No fallback mechanism

Affected Agents:
Database Agent
Analysis Agent
Writer
```

### User benefit

> "I can test my system before real failures happen."

This is similar to the idea of **stress testing** or **chaos testing**, but designed for AI agent workflows.

---

# 6. Full Execution Trace Explorer 🔍

Every execution becomes inspectable.

The user can see:

```text
RUN #247

Step 1
Planner
✓ Success

Step 2
Researcher
✓ Success

Step 3
Search Tool
⚠ Suspicious Result

Step 4
Researcher
🔴 Incorrect Information

Step 5
Analyst
🔴 Used Incorrect Information

Step 6
Writer
❌ Final Failure
```

The user can click on any step and inspect:

```text
INPUT
────────────

OUTPUT
────────────

TOOLS USED
────────────

EXECUTION TIME
────────────

DEPENDENCIES
────────────
```

### User benefit

> "I can inspect exactly what happened during execution."

---

# 7. Automatic Failure Detection 🤖

Instead of the user manually reading 500 steps, your system automatically flags suspicious behaviour.

For example:

```text
Run #247

⚠ Step 18

Anomaly Score: 0.87

Reason:

Output is semantically inconsistent
with information received from
previous agent.
```

The system could use your own models/algorithms for:

* anomaly detection
* semantic consistency checking
* abnormal execution detection
* unusual latency detection
* abnormal tool behaviour

### User benefit

> "The platform tells me where I should investigate."

---

# 8. Root Cause Analysis 🧠

This is the flagship feature.

The final answer may fail at:

```text
Step 40
```

But the actual problem started at:

```text
Step 12
```

The user gets:

```text
ROOT CAUSE REPORT

Responsible Agent:
Research Agent

Origin:
Step 12

Failure Type:
Incorrect information

Confidence:
87%

Evidence:

Step 12 introduced information
that conflicts with verified data.
```

Instead of simply saying:

> "Your workflow failed."

The product tells them:

> **Where, why, and who caused it.**

---

# 9. Failure Propagation Map 🕸️

This is one of the features I like most.

The user sees how an error moved through the system.

```text
Research Agent
       🔴
        │
        │ Incorrect Data
        ▼
Data Analyst
       🟠
        │
        │ Incorrect Analysis
        ▼
Writer Agent
       🔴
        │
        ▼
FINAL FAILURE
```

The user can click each connection and inspect:

```text
Information Passed:

Population = 120 Million

↓
Incorrect Information Used

↓
Incorrect Statistical Calculation
```

### User benefit

> "I understand how one mistake affected the whole system."

---

# 10. AI Agent Health Score 📊

For a deployed system, the user should get an overview like:

```text
SYSTEM HEALTH

████████░░ 82%

Reliability        84%
Recovery Ability   71%
Communication      78%
Tool Robustness    89%
```

Each agent also gets a profile.

```text
RESEARCH AGENT

Reliability: 72%

Common Failures:

1. Information Conflict
2. Missing Context
3. Tool Result Misinterpretation
```

Over time, the user sees trends:

```text
Agent Reliability

Week 1: 72%
Week 2: 76%
Week 3:
```

*(Message truncated here — exceeded the 50,000-character paste limit. Content ends mid-sentence in Section 10, "AI Agent Health Score.")*
