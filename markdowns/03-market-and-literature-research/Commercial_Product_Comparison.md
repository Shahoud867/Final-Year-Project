# Commercial Product Comparison — Granite vs. the Existing Agent-Observability Market

*Per the FAST guide's §10 requirement ("Product, Prior-FYP and Workflow Comparison") — comparison against real deployed products, not just academic papers. Compiled 2026-08-22 via direct research into each platform's current, documented feature set. Resolves risk-register.md's R9.*

---

## Verdict, upfront

The original risk-register assumption — "none of these platforms do algorithmic root-cause attribution, only human-driven trace inspection" — **is now out of date.** Two of the four platforms (LangSmith, Arize) shipped 2026 features (LangSmith Engine; Arize's "Alyx"/Signal) that market themselves as doing automated root-cause diagnosis and fix generation. This needed to be checked and corrected rather than left as a stale, comfortable assumption.

The corrected picture is more nuanced than either extreme: **not** "nobody automates this," and **not** "the market already does everything Granite claims." What's actually documented, publicly, for each platform is below.

---

## Comparison table

| Platform | Trace capture / multi-agent graph | Root-cause attribution | Counterfactual / fix-testing before applying | Silent-failure detection | Cross-framework generality |
|---|---|---|---|---|---|
| **LangSmith (core)** | Yes | Human-driven — the developer inspects the trace | No | No | Primarily LangChain/LangGraph-oriented |
| **LangSmith Engine** (Beta, 2026) | Yes | **Partial, real** — "diagnoses root causes against the live codebase" and drafts a fix as a pull request, in one automated pass. Mechanism for multi-agent *agent-level* attribution (as opposed to general code-level bug diagnosis) is not publicly documented | **Not confirmed** — no public documentation of testing a candidate fix via replay before it's proposed | Not confirmed | **Locked to LangSmith's own tracing/eval infrastructure** — built "on top of LangSmith's existing tracing and evaluation infrastructure," not framework-agnostic |
| **Langfuse** | Yes — agent graphs, nested spans, tool-call rendering | Human-driven — explicitly described in its own materials as leaving the developer "to determine which step was responsible, why, and how to repair the run" | No | No | Framework-agnostic, open-source (MIT), self-hostable — the strongest on trace-capture generality of the four |
| **Braintrust** | Yes — full span tree per run | Human-driven — explicit manual workflow: open the failed run, inspect the span tree, add a "root-cause label" by hand. Converts labeled failures into permanent regression test cases | No — turns failures into eval cases for future regression testing; does not test candidate fixes before applying | No | Framework-agnostic |
| **Arize Phoenix (core)** | Yes — OpenTelemetry-based | Human-driven, LLM-assisted evals | No | No | Framework-agnostic, open-source |
| **Arize "Alyx" / Signal** (2026) | Yes | **Marketing-stage, undocumented mechanism** — "uncovers root causes, generates review-ready fixes," but no public documentation of scope, mechanism, or whether it operates at multi-agent step-level specificity | Not confirmed | Not confirmed | Not confirmed |
| **Maxim AI** (added 2026-08-22) | Yes — full request-lifecycle trace graph | **Human-assisted, well-tooled** — "root cause debugging" re-runs simulations from any step to *reproduce* an issue, with spans auto-organized hierarchically for a human to drill down; own marketing says teams "use to identify failure modes and diagnose root causes" (human verb, not "Maxim identifies") | Not found — simulation re-run reproduces an issue, not confirmed to test a *corrected* step for recovery | **Partial, narrower** — "attribution tracking" flags outputs untraceable to a source document/tool call ("ungrounded claims"); this is RAG-groundedness checking specifically, not general task-constraint verification | Instruments whichever framework a customer uses; no publicized claim of tested generalization to a framework outside its own customer base |
| **Opik (Comet)** / **DeepEval** | Not yet researched in depth | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed — one-line vendor descriptions ("logging + evaluations," "evaluation infrastructure") suggest an eval-framework role closer to Braintrust/Arize than to LangSmith Engine/Alyx, but this is not verified |

---

## What none of the six confirm, publicly, as of this check

1. **Multi-agent agent-*and*-step-level attribution as a documented, specific mechanism** — as opposed to general-purpose "AI helps you debug" positioning. LangSmith Engine and Alyx both gesture at this; neither publishes how, or whether it's agent/step-specific versus general code-level diagnosis.
2. **Counterfactual replay of a candidate fix** — testing whether a proposed correction would actually have worked, with a measured recovery rate, before it's proposed or applied.
3. **Detection of silent, signal-free failures specifically** — outputs that look valid but are semantically wrong, with nothing to trigger investigation in the first place.
4. **Genuine cross-framework generality, evaluated** — every automated-diagnosis feature found (LangSmith Engine, Alyx) is built on and locked to its own vendor's tracing infrastructure, not demonstrated on frameworks outside that ecosystem.
5. **A rigorous, ground-truth-labeled evaluation of their own diagnostic accuracy** — none of the six platforms publish anything resembling the agent-accuracy/step-accuracy benchmarking the academic literature (Who&When, ErrorProbe, etc.) or this project's own POC do. Their diagnosis quality is asserted, not measured against a labeled benchmark.

---

## Positioning, corrected

**Old framing (no longer accurate as stated):** "None of these do algorithmic root-cause attribution — Granite would be the first."

**Corrected framing:** the market is *already moving* toward automated diagnosis (LangSmith Engine, Arize Alyx, both 2026) — this should be stated honestly in the proposal, not hidden, since a panel that's seen either product would otherwise catch the gap. Granite's differentiation from this commercial wave specifically:

- **Framework-agnostic by design and evaluation**, not locked to one vendor's own tracing stack — proven directly in the POC (CrewAI, a framework none of the six platforms' automated features are demonstrated on, none of the nine academic papers used).
- **Silent-failure detection as an explicit, benchmarked capability** — not claimed in marketing copy, measured against labeled ground truth.
- **Counterfactual replay as a quantified mechanism** — reporting a measured recovery rate, not just "here's a suggested fix."
- **A published, ground-truth-labeled benchmark** — none of these six platforms have one; this is the evaluation rigor gap between "an enterprise product with marketing claims" and "a measured research contribution."

**Practical implication for the product story (Supervisor_Briefing.md §6):** position Granite as a diagnosis layer that could, in principle, sit *alongside or feed into* platforms like Langfuse/Phoenix (which already do excellent trace capture and would benefit from an add-on doing the attribution/silent-failure/counterfactual layer none of them measure), rather than as a head-to-head competitor to LangSmith Engine or Arize Alyx on their own commercial home turf — a research-grade evaluation is not the same battle as a production-support-team's roadmap velocity, and claiming otherwise would be the over-claiming the guide explicitly warns against.

---

## A second market layer: orchestration frameworks (added 2026-08-24)

*Source: `Agentic_AI_Market_Survey_BS_FYP.docx`, reviewed 2026-08-24. This is a different layer than the seven platforms above — those are observability/eval tools that watch an agent system from the outside; this layer is the 7 orchestration frameworks that Granite actually instruments and generalizes across (OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI). Checking this layer independently strengthens the existing market-gap narrative above with a second source, rather than replacing anything already documented.*

The survey's own feature matrix, run across all 7 frameworks, converges on the same two gaps already established for the observability layer:

1. **No framework natively supports culprit-agent or error-step localization.** None of the 7 ship a first-class "which agent, which step" attribution mechanism — where diagnosis exists at all, it is left to the developer inspecting logs/traces by hand, the same human-driven pattern already documented for LangSmith, Langfuse, Braintrust, and Arize Phoenix above.
2. **No framework ships first-class automatic repair generation.** The survey rates "Automatically generate repair" as **Not native / Custom / Experimental** across all 7 frameworks — nobody treats *generating* a candidate correction (as opposed to merely retrying or failing) as a shipped, documented capability. This is the same gap identified from the commercial-platform layer (§ above: "Counterfactual replay of a candidate fix... not confirmed" for any of the 7 observability platforms), now confirmed independently from the framework-vendor side too.

**Why this matters for positioning:** the observability-platform comparison above already showed that trace-capture tools leave root-cause diagnosis to a human. This second, independent source shows the same gap holds one layer down, at the frameworks themselves — orchestration vendors are not quietly closing this gap in their own SDKs either. Two independent surveys (platform-side and framework-side) converging on the same absence is stronger evidence for the market gap than either alone.

**Direct implication for scope, on record:** the survey's own §7 ("Scope Control") recommends narrowing to a single framework (it suggests LangGraph) to keep a project like this achievable in one year. This advice was **explicitly considered and rejected** — see risk-register.md R19 — because it would eliminate cross-architecture generalization (RQ2), one of this project's two lead research questions, already partially tested (POC Spike 2, CrewAI instrumentation). The survey's market-gap finding is adopted; its scope-narrowing recommendation is not.

**Resolved positively, not just rejected — extension #8, added 2026-08-24:**

> **Framework Compatibility Layer** — draws capabilities and evidence from all 7 surveyed orchestration frameworks (OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI), not narrowed to a single one as the market survey's own §7 recommends (that recommendation was already rejected — see risk-register.md R19). Distinct from the foundational cross-architecture benchmark: the committed core's 2–3 frameworks (CrewAI, LangGraph, +1 via extension #2) get *full* fault-injection and benchmarked evaluation; this extension is deliberately lighter — confirming the diagnosis pipeline can instrument and parse execution traces from each of the remaining frameworks, without building a full fault-injection benchmark for each. Broad *compatibility*, not broad *benchmarking*. Gated behind the core, same as every other extension; no POC yet.

Total frozen feature count is now 20 (10 foundational + 8 extensions + 2 deprioritized), plan doc §7.0. See risk-register.md R20. **Same day, third pass:** Recovery Controller and Verified Repair Memory, briefly extensions #9–10 (the closed-loop's "resume from repaired point" and "remember successful repairs" steps this same survey's Table 1 recommends), were reclassified into the foundational core as items #9–10 — the survey's own Table 1 rates both "Core" for the Proposed FYP column, same as the other 6 already-foundational items, so leaving them as extensions was inconsistent with the survey's own classification.

**One genuinely new finding from this survey, already added to scope:** three of its four recommended pipeline modules ("Root-Cause Localizer," "Verification Agent," part of its closed repair loop) already exist in Granite's frozen feature list under matching or equivalent names — independent convergence, not new information. One did not exist yet: **Repair Agent**, the step that generates a candidate correction, now added as foundational item #6 (plan doc §7.0; risk-register.md R17). The existing Verified Automatic Repair only ever tested/verified a candidate assumed already given — this survey is what surfaced that nothing in the prior list actually produced that candidate value.

### Full platform write-ups (verbatim, from the market survey)

*Reproduced verbatim from `Agentic_AI_Market_Survey_BS_FYP.docx` (via [Agentic_AI_Market_Survey_Full_Content_and_Integration.md](Agentic_AI_Market_Survey_Full_Content_and_Integration.md)) so this file is self-contained and doesn't require jumping to the central survey document for the underlying platform-by-platform detail behind the table above.*

**3.1 OpenAI Agents SDK** — Provides multi-agent handoffs, tool integration, sessions, guardrails, tracing and evaluation-oriented instrumentation. Its tracing model can capture agent turns, model generations, tool calls, handoffs and guardrails. Tool guardrails can validate calls before and after execution. For this FYP, these features should be treated as infrastructure rather than novelty. The SDK does not natively perform causal attribution to identify the earlier agent/step that introduced a semantic failure, nor does it automatically repair and replay that component.

**3.2 LangGraph** — Particularly suitable for resilient workflows because it provides durable state, checkpointing, fault tolerance, retry policies, persistence and time-travel/replay. This makes it a strong implementation substrate for the proposed FYP. The student can reuse LangGraph for checkpoint/resume and focus on semantic diagnosis and verified repair. LangGraph can tell the system where execution failed, but causal semantic attribution to an earlier agent remains a separate research problem.

**3.3 CrewAI** — Provides multi-agent orchestration, tracing/observability and checkpoint-oriented execution features. Its recovery mechanisms can save state and resume a workflow rather than repeating all completed work. It therefore covers a large portion of operational fault tolerance. However, identifying the semantic root cause of a seemingly valid but wrong multi-agent trajectory and automatically repairing the responsible step remains custom logic.

**3.4 Google Agent Development Kit (ADK)** — Offers agent orchestration, plugins, callbacks, evaluation and retry-related mechanisms. Its evaluation tooling is relevant because it can assess final answers and trajectories/tool-use sequences. This reduces the novelty of simply adding an "agent evaluator." The proposed FYP should instead use evaluation as a verification signal and focus on causal localization plus targeted repair.

**3.5 Microsoft Agent Framework** — Provides graph-based multi-agent workflows, checkpointing, state management, human-in-the-loop mechanisms, middleware and telemetry. These are strong foundations for recovery and production engineering. The remaining gap is not basic recovery from an exception, but determining the semantic origin of a delayed failure and transforming that diagnosis into an automatically verified correction.

**3.6 Amazon Bedrock AgentCore** — Strongest at enterprise runtime, observability and evaluation. It provides logs, traces, metrics and production monitoring for agent workloads. This is highly useful for collecting evidence about failures, but observability alone does not solve semantic causal attribution. A workflow may complete successfully at the infrastructure level while still returning a semantically wrong result.

**3.7 BabyAGI** — Useful as conceptual inspiration because its function-centric architecture records execution details and explores experimental self-building capabilities. In principle, self-building allows a system to create or revise capabilities rather than only report an error. However, BabyAGI does not provide the same systematic, benchmarked culprit-agent and originating-step diagnosis studied by ERRORPROBE. For an FYP, its self-modification idea is more useful as inspiration for the Repair Agent than as a direct baseline for semantic attribution.

**3.8 ERRORPROBE (ACL Findings 2026)** — A research framework for semantic failure attribution in multi-agent systems. It takes a failed trace, uses structural decomposition and symptom-driven backward tracing, and employs a Strategist-Investigator-Arbiter team to identify the responsible agent and decisive error step. It also stores verified diagnostic patterns. Its main contribution is therefore diagnosis rather than closed-loop operational recovery: the framework improves the debugger, but it does not demonstrate a complete system that automatically repairs the responsible component, replays the workflow from a corrected state and retains verified repairs as executable recovery knowledge.
