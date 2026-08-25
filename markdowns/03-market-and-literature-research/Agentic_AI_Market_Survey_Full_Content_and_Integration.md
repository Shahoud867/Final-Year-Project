# Agentic AI Market Survey — Full Content, and Integration Audit

*Source: `Agentic_AI_Market_Survey_BS_FYP.docx` (project root, `agent-autopsy/`). Reviewed 2026-08-24. Full content reproduced below verbatim (tables converted to markdown), with a section-by-section integration audit at the end showing exactly where each piece landed in Granite's own docs — so nothing from this source is lost or un-tracked, matching this project's existing practice for pasted external material (see `Silent_Failure_Detection_and_Testing_Strategies.md` for the same pattern).*

---

## MARKET SURVEY — Agentic AI Frameworks for Self-Healing Multi-Agent Systems

*Feature Comparison, Technology Gap Analysis, and Recommended BS Final Year Project Scope*

Technology landscape reviewed: August 2026. Primary focus: error handling, semantic failure diagnosis, repair, recovery, and self-improvement. Prepared as a BS-level FYP market and technology survey.

### Executive Summary

**Purpose.** This survey compares major agentic AI frameworks and platforms against the capabilities required for a proposed self-healing multi-agent system. The analysis distinguishes ordinary operational error handling (exceptions, retries, checkpoints and tracing) from semantic root-cause diagnosis (which agent introduced the error and at which earlier step), and from closed-loop recovery (repair, verification, resumption and learning).

**Key finding.** The market is mature for orchestration, tool calling, traces, retries, guardrails, memory and checkpoint-based recovery. However, the surveyed products do not natively provide the complete closed loop of: semantic failure detection → culprit-agent attribution → originating-step localisation → targeted repair → verification → resume from a corrected state → retain the successful repair for future use.

**Recommended FYP position.** Use an existing framework such as LangGraph, Google ADK, CrewAI or Microsoft Agent Framework for commodity orchestration and persistence. Concentrate the student contribution on four modules: Root-Cause Localizer, Repair Agent, Verification Agent and Verified Repair Memory.

**Core research gap:** Existing SDKs can observe, retry and resume workflows; ERRORPROBE can attribute semantic failures; the missing integration is to turn a verified diagnosis into a verified repair and resume execution from the corrected state.

### 1. Scope and Evaluation Criteria

The survey evaluates frameworks at three layers:
- **Operational robustness:** runtime errors, tool failures, retries, guardrails, tracing and checkpoints.
- **Semantic diagnosis:** identifying that an apparently valid result is wrong, locating the responsible agent and finding the originating interaction step.
- **Self-healing recovery:** generating a targeted correction, verifying it, resuming execution and reusing verified repairs in future failures.

**Interpretation of symbols.** Built-in/strong support = native or first-class capability; Partial/custom = feasible through developer logic or ecosystem extensions; Experimental = available but not mature; Not native = not provided as a first-class capability by the framework.

### 2. Comparative Feature Matrix

*Table 1. Market comparison of agentic AI platforms against the proposed self-healing FYP.*

| Feature | OpenAI Agents SDK | LangGraph | CrewAI | Google ADK | Microsoft Agent Framework | Amazon AgentCore | BabyAGI | Proposed FYP |
|---|---|---|---|---|---|---|---|---|
| Multi-agent orchestration | Strong | Strong | Strong | Strong | Strong | Platform/runtime | Partial | Strong |
| Tool calling | Strong | Strong | Strong | Strong | Strong | Strong | Strong | Strong |
| Execution tracing | Strong | Strong ecosystem | Strong | Strong | Strong | Strong | Strong logs | Strong |
| Runtime-error detection | Strong | Strong | Strong | Strong | Strong | Strong | Strong logs | Strong |
| Automatic retry | Partial/custom | Strong | Partial/custom | Strong | Strong/custom | Operational retries | Partial | Strong |
| Guardrails / validation | Strong | Partial/custom | Strong | Strong | Strong | Strong | Limited | Strong |
| Persistent memory | Strong | Strong | Strong | Strong | Strong | Strong | Strong | Strong |
| Checkpoint / resume | Partial | Strong | Strong | Workflow support | Strong | Runtime-oriented | Limited | Strong |
| Workflow replay / fork | Partial | Strong | Strong | Evaluation/replay | Strong | Partial | Not native | Strong |
| Agent evaluation | Strong | Ecosystem | Strong | Strong | Strong | Strong | Limited | Strong |
| Detect semantic wrong answer | Partial via eval/guardrail | Partial/custom | Partial/custom | Evaluation support | Partial/custom | Evaluation support | Limited | **Core** |
| Find culprit agent | Not native | Not native | Not native | Not native | Not native | Not native | Not native | **Core** |
| Find originating error step | Not native | Not native | Not native | Not native | Not native | Not native | Not native | **Core** |
| Causal backward error tracing | Not native | Not native | Not native | Not native | Not native | Not native | Not native | **Core** |
| Automatically generate repair | Not native | Custom | Custom | Custom | Custom | Custom | Experimental self-building | **Core** |
| Verify repair before applying | Custom | Custom | Custom | Via evaluation/custom | Custom | Via evaluation/custom | Limited | **Core** |
| Resume from repaired point | Not native | Checkpoint-based | Checkpoint-based | Partial | Checkpoint-based | Partial | Not native | **Core** |
| Remember successful repairs | Not native | Custom | Custom | Custom | Custom | Custom | Experimental | **Core** |
| Self-improve from prior failures | Not native | Partial/custom | Partial/custom | Partial/custom | Partial/custom | Partial/custom | Experimental | Verified/controlled |

**Reading the table correctly:** A "Not native" rating does not mean a capability is impossible to implement; it means the framework does not provide it as a first-class, built-in feature. This distinction is important because the proposed project should not claim novelty for functionality that can simply be assembled through standard framework hooks.

### 3. Platform and Framework Survey

**3.1 OpenAI Agents SDK** — Provides multi-agent handoffs, tool integration, sessions, guardrails, tracing and evaluation-oriented instrumentation. Its tracing model can capture agent turns, model generations, tool calls, handoffs and guardrails. Tool guardrails can validate calls before and after execution. For this FYP, these features should be treated as infrastructure rather than novelty. The SDK does not natively perform causal attribution to identify the earlier agent/step that introduced a semantic failure, nor does it automatically repair and replay that component.

**3.2 LangGraph** — Particularly suitable for resilient workflows because it provides durable state, checkpointing, fault tolerance, retry policies, persistence and time-travel/replay. This makes it a strong implementation substrate for the proposed FYP. The student can reuse LangGraph for checkpoint/resume and focus on semantic diagnosis and verified repair. LangGraph can tell the system where execution failed, but causal semantic attribution to an earlier agent remains a separate research problem.

**3.3 CrewAI** — Provides multi-agent orchestration, tracing/observability and checkpoint-oriented execution features. Its recovery mechanisms can save state and resume a workflow rather than repeating all completed work. It therefore covers a large portion of operational fault tolerance. However, identifying the semantic root cause of a seemingly valid but wrong multi-agent trajectory and automatically repairing the responsible step remains custom logic.

**3.4 Google Agent Development Kit (ADK)** — Offers agent orchestration, plugins, callbacks, evaluation and retry-related mechanisms. Its evaluation tooling is relevant because it can assess final answers and trajectories/tool-use sequences. This reduces the novelty of simply adding an "agent evaluator." The proposed FYP should instead use evaluation as a verification signal and focus on causal localization plus targeted repair.

**3.5 Microsoft Agent Framework** — Provides graph-based multi-agent workflows, checkpointing, state management, human-in-the-loop mechanisms, middleware and telemetry. These are strong foundations for recovery and production engineering. The remaining gap is not basic recovery from an exception, but determining the semantic origin of a delayed failure and transforming that diagnosis into an automatically verified correction.

**3.6 Amazon Bedrock AgentCore** — Strongest at enterprise runtime, observability and evaluation. It provides logs, traces, metrics and production monitoring for agent workloads. This is highly useful for collecting evidence about failures, but observability alone does not solve semantic causal attribution. A workflow may complete successfully at the infrastructure level while still returning a semantically wrong result.

**3.7 BabyAGI** — Useful as conceptual inspiration because its function-centric architecture records execution details and explores experimental self-building capabilities. In principle, self-building allows a system to create or revise capabilities rather than only report an error. However, BabyAGI does not provide the same systematic, benchmarked culprit-agent and originating-step diagnosis studied by ERRORPROBE. For an FYP, its self-modification idea is more useful as inspiration for the Repair Agent than as a direct baseline for semantic attribution.

**3.8 ERRORPROBE (ACL Findings 2026)** — A research framework for semantic failure attribution in multi-agent systems. It takes a failed trace, uses structural decomposition and symptom-driven backward tracing, and employs a Strategist-Investigator-Arbiter team to identify the responsible agent and decisive error step. It also stores verified diagnostic patterns. Its main contribution is therefore diagnosis rather than closed-loop operational recovery: the framework improves the debugger, but it does not demonstrate a complete system that automatically repairs the responsible component, replays the workflow from a corrected state and retains verified repairs as executable recovery knowledge.

### 4. Error-Handling Layers: Why the Systems Are Complementary

*Table 2. Five layers of agentic error handling and the location of the proposed project gap.*

| Layer | Typical Question | Strong Existing Solutions | Remaining Gap |
|---|---|---|---|
| 1. Runtime handling | Did a tool/API/node fail? | Agent SDKs, LangGraph, AgentCore, ADK, CrewAI | Mostly mature |
| 2. Workflow recovery | Can execution retry/resume? | LangGraph, CrewAI, Microsoft Agent Framework | Mostly mature |
| 3. Semantic diagnosis | Which agent introduced the wrong reasoning and where? | ERRORPROBE; research prototypes | Still under-served |
| 4. Targeted repair | Can the responsible component be corrected automatically? | Custom logic; experimental self-building | Major gap |
| 5. Verified self-healing | Can the fix be tested, replayed and remembered safely? | Partial/custom across frameworks | Strong FYP opportunity |

### 5. Market Gap Analysis

*Table 3. Market saturation versus potential FYP contribution.*

| Capability | Market Status | FYP Value |
|---|---|---|
| Agent orchestration | Saturated | Reuse existing framework |
| Tool integration | Saturated | Reuse |
| Logging/tracing | Saturated | Reuse |
| Exception detection | Saturated | Reuse |
| Automatic retries | Saturated | Reuse |
| Memory | Saturated | Reuse |
| Checkpoint/resume | Strong existing solutions | Reuse |
| Guardrails | Strong existing solutions | Reuse |
| Agent evaluation | Rapidly maturing | Reuse/adapt |
| Semantic failure detection | Partial | Useful component |
| Culprit-agent attribution | Research-level / under-served | Strong feature |
| Originating-step localisation | Research-level / under-served | Strong feature |
| Automatic targeted repair | Major gap | Excellent feature |
| Verification of generated repair | Partial/custom | Excellent feature |
| Resume after verified repair | Integration gap | Excellent feature |
| Verified repair memory | Under-served | Excellent feature |

**Gap statement suitable for the proposal:** Existing agent SDKs provide mechanisms for observing, retrying and resuming failed workflows, while recent research such as ERRORPROBE addresses semantic failure attribution. A practical gap remains in automatically transforming root-cause diagnosis into a verified repair, resuming execution from the corrected state, and retaining successful repair knowledge for future failures.

### 6. Recommended BS Final Year Project

**Proposed Title:** *A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery*

**6.1 Recommended System Flow** *(Figure 1: Execute MAS → Detect Failure → Localise Cause → Generate Repair → Verify Repair → Resume Workflow → Store Repair)*

1. **Multi-Agent Runtime:** Use an existing framework for Planner/Worker/Reviewer or similar agents.
2. **Trace Collector:** Store agent messages, tool calls, outputs, exceptions and checkpoint identifiers.
3. **Semantic Failure Detector:** Identify failures that may not be ordinary runtime exceptions, using constraints, evaluator signals or task-specific checks.
4. **Root-Cause Localizer:** Estimate the culprit agent and originating error step using backward dependency/trace reasoning.
5. **Repair Agent:** Generate a targeted correction to the prompt, tool arguments, structured output or function logic associated with the localized failure.
6. **Verification Agent:** Test candidate repairs using deterministic checks, sandbox execution, test cases or evaluator constraints.
7. **Recovery Controller:** Apply only verified repairs and resume execution from a safe checkpoint instead of restarting the entire workflow.
8. **Verified Repair Memory:** Store successful error → diagnosis → repair patterns and retrieve them for similar future failures.
9. **Dashboard:** Visualize the workflow, failed agent, originating step, repair attempt, verification result and final recovered execution.

### 7. Scope Control for a One-Year BS Project

The complete research vision can become too broad. For a realistic one-year implementation, the project should deliberately constrain the environment:
- Use one agent framework only (recommended: LangGraph, because checkpointing and replay are already available).
- Use one or two task domains, such as code/tool-use tasks and structured reasoning tasks.
- Limit the MAS to approximately 3–4 roles so causal traces remain understandable.
- Implement a small taxonomy of failure types rather than attempting every possible semantic failure.
- Treat repair as targeted modification of prompts, tool arguments, structured outputs or small code functions; do not attempt unrestricted rewriting of the entire agent architecture.
- Require verification before any generated repair is applied or added to memory.

### 8. Evaluation Plan

*Table 4. Recommended quantitative evaluation metrics for the FYP.*

| Metric | What It Measures | Suggested Comparison |
|---|---|---|
| Task completion rate | Whether the full task succeeds | Baseline MAS vs. self-healing MAS |
| Failure detection precision/recall | Quality of semantic failure detection | Detector variants |
| Culprit-agent accuracy | Correct responsible agent | Root-cause module vs. simple last-error baseline |
| Error-step accuracy | Correct originating step | Backward tracing vs. full-trace judge |
| Repair success rate | Percentage of generated repairs that fix the task | With vs. without verification |
| Recovery rate | Failed runs converted into successful runs | Baseline retry vs. targeted repair |
| Re-execution cost | Tokens/tool calls/time after failure | Restart-from-zero vs. checkpoint resume |
| Repair reuse benefit | Improvement when verified memory is enabled | Memory off vs. memory on |
| False repair rate | Incorrect repairs accepted by system | Verification ablation |

### 9. What the Students Should and Should Not Claim

**Strong, defensible contribution:**
- Integration of semantic root-cause localization with automatic targeted repair.
- Verification-gated repair acceptance rather than unconstrained LLM self-modification.
- Checkpoint-based recovery from the corrected state.
- A verified repair memory evaluated for reuse across repeated/similar failure patterns.

**Claims to avoid:**
- "First agent system with retries, tracing or memory." These are already common capabilities.
- "BabyAGI/AgentCore/LangGraph cannot handle errors." They handle many operational errors well; the gap is semantic causal diagnosis and closed-loop repair.
- "The system solves all hallucinations." Silent semantic failures remain a difficult open problem.
- "The FYP outperforms ERRORPROBE" unless the students reproduce a fair benchmark comparison.

### 10. Conclusion

The agentic AI market already provides mature building blocks for orchestration, tools, observability, retries, guardrails, persistent state and checkpoint-based recovery. A BS project should therefore avoid rebuilding those features. The strongest remaining FYP opportunity is the integration between semantic diagnosis and recovery: identify the real originating agent/step, generate a targeted repair, verify that repair, resume from a safe checkpoint and remember only successful repairs. This produces a technically meaningful "self-healing" contribution while keeping the project achievable within one academic year.

### References and Official Technical Sources

- Li, J., Yilmaz, E., Chen, B. and Le, D.-T. (2026). "Towards Self-Improving Error Diagnosis in Multi-Agent Systems." *Findings of the Association for Computational Linguistics: ACL 2026*, pp. 2063–2077. https://aclanthology.org/2026.findings-acl.98/
- OpenAI. Agents SDK documentation: Agents, tracing and guardrails. https://openai.github.io/openai-agents-python/
- LangChain. LangGraph documentation: Persistence, checkpointing and fault tolerance. https://docs.langchain.com/oss/python/langgraph/persistence
- LangChain. LangGraph RetryPolicy reference. https://reference.langchain.com/python/langgraph/types/RetryPolicy
- CrewAI. Documentation: Checkpointing and Observability. https://docs.crewai.com/en/concepts/checkpointing
- Google. Agent Development Kit documentation: Plugins and evaluation. https://google.github.io/adk-docs/
- Microsoft. Agent Framework documentation: Workflows and checkpoints. https://learn.microsoft.com/en-us/agent-framework/workflows/
- Amazon Web Services. Amazon Bedrock AgentCore documentation: Observability and evaluations. https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/
- Nakajima, Y. BabyAGI repository and documentation. https://github.com/yoheinakajima/babyagi

*Source note: The ERRORPROBE analysis in this report is grounded in the ACL 2026 paper supplied for the discussion. Product/framework capabilities are summarized from their official documentation and repositories. Feature ratings represent whether a capability is native/first-class versus requiring custom implementation, not whether it is theoretically possible.*

---

## Integration audit — where every piece of this document landed in Granite's own docs

*This is the part that matters for defense: not "we read an interesting survey," but a traceable map from every claim above to what Granite actually did with it.*

| Survey content | Integration status | Where |
|---|---|---|
| **4 recommended modules** (Root-Cause Localizer, Repair Agent, Verification Agent, Verified Repair Memory) | Root-Cause Localizer = already existed (Culprit Agent + Error Step Localization). Verification Agent = already existed under the *same name* — independent convergence. **Repair Agent = genuinely new, added, and now POC-tested (Spike 8, 2026-08-24): repair_success_rate 0.667 (4/6), both failures traced to one fixable interface-specification issue.** Verified Repair Memory = already built once, already reverted; **re-added the same day (2026-08-24) by explicit user decision, then reclassified into the foundational core as item #10** — the one real test's failure result carries forward unchanged, not softened by the reclassification | `FYP_Scope_CCP_and_Implementation_Plan.md` §7.0; risk-register.md R17 (Repair Agent, Spike 8 result), R18 (Verified Repair Memory history), R22 (re-add + reclassification decision); `POC_Spike_Outputs_Full.md` Spike 8 section; `dev/spikes/poc/poc_spike8_repair_agent.py` + `poc_spike8_output.json` |
| **Table 1, "Find culprit agent" / "Find originating error step" / "Automatically generate repair" rows** — Not native across all 7 frameworks | Cited as direct precedent evidence for Culprit Agent, Error Step Localization, and Repair Agent's novelty claims | PDF §6a, artifact Features section, `Commercial_Product_Comparison.md` new section |
| **Table 2, 5-layer framework** (runtime handling → workflow recovery → semantic diagnosis → targeted repair → verified self-healing) | **Now reproduced directly in both the PDF (§6e) and the artifact (Commercial Landscape section)** — with Granite's own features mapped onto each layer, including Repair Agent's Spike 8 result at layer 4 | PDF §6e, artifact landscape section, plus the full version here |
| **Table 3, market saturation vs. FYP value** | Same substance as the existing `Commercial_Product_Comparison.md` gap table, now with the framework-layer confirmation added alongside the platform-layer one | `Commercial_Product_Comparison.md` |
| **§6.1 Recommended System Flow (9 steps)** | Steps 1–4 and 6 map directly onto Granite's existing pipeline (Execute → Capture Trace → Build Graph → Diagnose). Step 5 (Repair Agent) = the new addition, foundational item #6. Step 7 (Recovery Controller: resume from a safe checkpoint) — **added the same day as extension #9, then reclassified into the foundational core as item #9**, resolving the "Checkpointing" item that had sat in "considered, not added" since 2026-08-23; no POC yet, genuinely new mechanical work. Step 8 (Verified Repair Memory) — see above, foundational item #10. Step 9 (Dashboard) already committed core item 6 | `FYP_Scope_CCP_and_Implementation_Plan.md` §7.0 foundational items #9–10; risk-register.md R21 (Recovery Controller), R22 (Verified Repair Memory reclassification); architecture-sketch.md pipeline diagram |
| **§7 Scope Control** — one framework only, 1–2 task domains, 3–4 agent roles, small failure taxonomy, targeted (not unrestricted) repair, verification-gated | "One framework only" **explicitly rejected** (kills RQ2). "1–2 task domains" already satisfied independently (GSM8K + tau-bench retail, `datasets.md` §6, decided before this survey existed). "Small failure taxonomy" already satisfied (extension #1, 3 fault types). "Targeted, not unrestricted, repair" — adopted as Repair Agent's explicit scope boundary. "Verification-gated" — already the project's standing principle (extension #12, confidence-gating) | risk-register.md R19; plan doc §7.0 foundational item #6 description |
| **§8 Evaluation Plan, 9 metrics** | Culprit-agent accuracy / error-step accuracy / recovery rate already had direct equivalents in Granite's evaluation plan. **Repair success rate and false repair rate were genuinely missing — added.** Re-execution cost and repair reuse benefit deliberately **not** added yet — they measure Checkpointing and Verified Repair Memory, neither of which is in scope, so adding the metric before the feature would be premature | `FYP_Scope_CCP_and_Implementation_Plan.md` §11 |
| **§9 Claims to avoid** | Cross-checked against everything written into `Commercial_Product_Comparison.md`'s new section and the PDF/artifact use cases — confirmed no instance of "frameworks can't handle errors" overclaiming exists; the wording throughout correctly scopes claims to "no native culprit/step localization" and "no first-class repair generation" | Verified, no edit needed — checked directly against `Commercial_Product_Comparison.md` §"second market layer" |
| **10 references** (ErrorProbe ACL 2026, 7 framework doc links, BabyAGI repo) | ErrorProbe already Granite's chosen baseline throughout the whole project (`ErrorProbe_Baseline_Selection.md`). The 7 framework documentation links are new citable sources — not yet added to any Granite bibliography/references section, since this project doesn't currently maintain one central references file | **Open — no dedicated references file exists in this project to add them to; flagging rather than inventing one unprompted** |

### Honest answer to "is this a big boost"

Yes, genuinely — but precisely, not broadly. An independent BS-level survey arriving at the same 3-stage attribution architecture (matching ErrorProbe's own Strategist/Investigator/Arbiter, which Granite already reproduces) and the same "verification before trust" principle (which Granite already committed to via extension #12) is real corroborating evidence that the direction is sound — not a hunch, a second source converging on it independently. The genuine addition it produced — Repair Agent — closes a real, previously-unnoticed gap (FR4 assumed a candidate fix existed; nothing generated one). What it does **not** do is validate a pivot to its own recommended framing ("A Self-Healing Multi-Agent System") or its single-framework scope-narrowing advice — both were considered and explicitly not adopted, for reasons already on record (risk-register.md R19; this project's RQ2 commitment predates this survey and outranks it).
