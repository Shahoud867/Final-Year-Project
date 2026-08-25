# Granite — Proposal Defense Package (Guide §16)

*Content for the 10 required slides, assembled from the plan doc and its supporting files. This is ready-to-slide content, not a formatted deck — turn each section below into one slide.*

---

## Slide 1 — Title and one-line problem

**A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery**
*(short title: Granite — adopted 2026-08-24, from `Agentic_AI_Market_Survey_BS_FYP.docx` §6)*

Stream: A (research-derived) | Members: [names] | Supervisor: [name]

> Build a failure-attribution and recovery system that generalizes to multi-agent architectures no prior paper has tested on, catches the "silent failures" the strongest existing method (ErrorProbe) admits it cannot detect, and ships as an installable, framework-agnostic testing product.

## Slide 2 — Stakeholders and current workflow

**Notional client (guide §5.2):** an engineering team operating a multi-agent AI system in or near production — concretely grounded in a customer-support/retail workflow (the project's active benchmark target, tau-bench retail).

**Current workflow without this system:** teams use observability platforms (LangSmith, Langfuse, Braintrust, Arize) to *capture* traces, then a human manually inspects them to guess the root cause — no automated attribution, no systematic silent-failure check, no way to test a fix before redeploying.

**SDG/thematic alignment:** SDG 9, Industry Innovation and Infrastructure — building the missing reliability-testing infrastructure layer for a genuinely new industrial category (production multi-agent AI).

## Slide 3 — Existing solutions and prior FYPs

| Solution | Core approach | Strong feature | Evidence-based limitation |
|---|---|---|---|
| ErrorProbe (ACL 2026) | 3-stage LLM diagnosis team + verified memory | Best published step accuracy (59.5%) | Admits failing on silent failures; not tested on unseen architectures |
| AgenTracer (ICLR 2026) | Programmatic fault injection + trained small model | Removed manual annotation cost | TracerTraj-2.5K unreleased (confirmed by direct repo check) |
| LangSmith Engine / Arize Alyx (2026, commercial) | Automated root-cause diagnosis + fix drafting | Real, shipped, funded | Locked to their own tracing stack; no counterfactual fix-testing with measured recovery; no general silent-failure detection |
| Langfuse / Braintrust / Arize Phoenix / Maxim / Opik / DeepEval (commercial) | Trace capture, evaluation, CI-style testing | Mature, well-adopted | All human-driven root-cause investigation, or narrower silent-failure signal (RAG-groundedness only) |
| Closest prior FYP | *[team to fill in from department archive — guide §10, cannot be completed externally]* | | |
| Current manual workflow | Human reads the trace, guesses | Flexible | Slow, unscalable, no measured accuracy |

Full detail: [Full_Literature_Landscape_Analysis.md](../03-market-and-literature-research/Full_Literature_Landscape_Analysis.md), [Commercial_Product_Comparison.md](../03-market-and-literature-research/Commercial_Product_Comparison.md).

## Slide 4 — Research and technical basis

9+ papers read in full (Who&When, AgenTracer, SDBL, TraceElephant, ErrorProbe, AgentAsk, PROTEA, plus GraphTracer/FALAT/DoVer triaged), 7 commercial platforms researched directly (not from marketing summaries). Full decision trail: [FYP_Scope_CCP_and_Implementation_Plan.md §0.08](../01-planning-and-scope/FYP_Scope_CCP_and_Implementation_Plan.md) (research-to-decision table).

## Slide 5 — CCP / complex activity justification

**8 of 9 Seoul Accord characteristics clear** (plan doc §2): conflicting requirements (depth vs. latency, generalization vs. specialization), no obvious solution (59.5% best-in-field after 15 months), depth of knowledge, unfamiliar issues, beyond standard practice, significant consequences, interdependence, ill-defined cause. Only diverse stakeholders (#6) remains open, pending real stakeholder contact.

## Slide 6 — Proposed contribution and solution

> Existing methods achieve up to 59.5% step accuracy but remain weak under two conditions: none is evaluated on an architecture absent from its own benchmark construction, and the strongest method explicitly fails on silent failures. We contribute a cross-architecture fault-injection benchmark, a diagnosis pipeline with task-constraint Semantic Error Diagnostic, a Repair Agent that generates candidate fixes (a gap confirmed by an independent 7-framework market survey — none ship this natively), and a Verified Automatic Repair engine that verifies and applies them — packaged as a framework-agnostic SDK.

Architecture: [architecture-sketch.md](../01-planning-and-scope/architecture-sketch.md). External components correctly classified (LLM = Core-assist, not the contribution) with a committed ~15-20% API-dependency budget.

## Slide 7 — POC / technical spike (mandatory, guide §12)

**7 spikes run, independently reproduced — exceeds the 1-spike minimum:**

| Spike | Result |
|---|---|
| 1. ErrorProbe reproduction | 75% agent / 12.5% step accuracy (simplified pipeline, n=8) — real signal, full version still needed |
| 2. CrewAI instrumentation | Traced cleanly, resolved |
| 3. Fault injection | Ground truth recoverable, resolved |
| 4. Silent-failure detector | Zero false positives on known-wrong values (n=3 live cases, no natural failure observed yet) |
| 5. Counterfactual replay | Recovery mechanism confirmed (`recovery_success: true`) |
| 6. Cyclic graph handling | Terminates correctly on a true cycle; control case proves the safety bound is load-bearing |
| 7. Preventive classifier | **Honest negative result**: precision/recall/f1 = 0.25 with simple features — real finding, mitigation plan in risk-register.md R15 |

**Every foundational item now has a spike, including the newest.** Repair Agent (added 2026-08-24, plan doc §7.0 item #6) — the candidate-fix-generation step, distinct from Verified Automatic Repair's already-spiked verify/replay step — was run same-day as Spike 8: repair_success_rate 0.667 (4/6), n=6, chained into Spike 5's replay logic. Both failures traced to one precise, fixable interface-specification issue (model returns a computed result instead of the specific corrected parameter), not a reasoning gap. See risk-register.md R17.

## Slide 8 — Evaluation plan

Baseline: ErrorProbe, reproduced from its published methodology. Data: Who&When (184 real cases, MIT), plus the project's own new cross-architecture benchmark. Metrics: agent/step accuracy, propagation-path F1, silent-failure precision/recall, task completion rate, diagnostic latency overhead, counterfactual recovery rate, repair success rate, false repair rate. Full plan: plan doc §11.

## Slide 9 — Scope, risks and dependencies

**Committed core:** 10 items (plan doc §7.0, extended 2026-08-24 three times) — fault-injection harness, cross-architecture benchmark, Culprit Agent, Error Step Localization, Verification Agent, **Repair Agent** (new — generates the candidate fix; a gap surfaced by `Agentic_AI_Market_Survey_BS_FYP.docx`'s own feature matrix, which rates automatic repair generation Not native / Custom / Experimental across all 7 surveyed frameworks; POC run same-day, Spike 8: repair_success_rate 0.667 (4/6), risk-register.md R17), Semantic Error Diagnostic, Verified Automatic Repair, **Recovery Controller** (new, no POC yet — applies a verified repair and resumes from a safe checkpoint instead of restarting the whole workflow), and **Verified Repair Memory** (re-added by explicit user decision after one real prior test failed — 0/8 commits, local 3B backbone). The last two were briefly extensions #9–10, then reclassified into the foundational core the same day (2026-08-24) because the market survey's own Table 1 rates both "Core" for the Proposed FYP column, same as the other 6 foundational items.
**8 extensions**, filtered for CCP strength + market novelty + architectural fit: fault-taxonomy widening, 3rd architecture, cyclic-graph support, confidence calibration, preventive classifier, propagation map, explainable confidence reasoning, and **Framework Compatibility Layer** (new 2026-08-24):

> **Framework Compatibility Layer** — draws capabilities and evidence from all 7 surveyed orchestration frameworks (OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI), not narrowed to a single one as the market survey's own §7 recommends (that recommendation was already rejected — see risk-register.md R19). Distinct from the foundational cross-architecture benchmark: the committed core's 2–3 frameworks (CrewAI, LangGraph, +1 via extension #2) get *full* fault-injection and benchmarked evaluation; this extension is deliberately lighter — confirming the diagnosis pipeline can instrument and parse execution traces from each of the remaining frameworks, without building a full fault-injection benchmark for each. Broad *compatibility*, not broad *benchmarking*. Gated behind the core, same as every other extension; no POC yet.

**2 explicitly deprioritized**, not planned: cross-domain transfer testing, chaos testing.
**Total frozen feature count: 20** (10 foundational + 8 extensions + 2 deprioritized), plan doc §7.0.
**Top risks** (full register: [risk-register.md](../02-evidence-and-tracking/risk-register.md)): R1 (reproduction gap to 59.5%), R7 (literature-crowding, accepted risk, documented), R15 (preventive classifier's weak first result), R16 (security/privacy, resolved with a threat model), R17 (Repair Agent — Spike 8 run, 4/6 success, one fixable cause identified for the 2 failures), R18 (Verified Repair Memory — built and tested once 2026-08-23, real negative result; re-added and reclassified 2026-08-24 as foundational item #10 by explicit user decision, on the explicit condition that a re-test on a stronger backbone happens before Mid-1), R19 (single-framework scope-narrowing advice, rejected, resolved positively via extension #8), R20 (Framework Compatibility Layer itself — no POC yet, gated behind the core).
**Professional and ethical compliance:** advisory-only diagnosis output with human-gated fix approval (extension #6), informed consent required before using any real user's trace data, synthetic fault injection restricted to own/consenting systems only — full statement: plan doc §0.09.

## Slide 10 — Team responsibilities and iterations

Three role areas defined (plan doc §9): Data/Benchmark Owner, Diagnosis Owner, Platform Owner — **assignment to specific team members still pending** (risk-register.md R6), to be resolved before Mid-1. Two-semester timeline mapped to all 5 gates: plan doc §12.

---

## Appendix: Market Survey — Executive Summary & Claims Discipline (full excerpt)

*Useful direct source material for defense talking points. Reproduced verbatim from `Agentic_AI_Market_Survey_BS_FYP.docx` (via [Agentic_AI_Market_Survey_Full_Content_and_Integration.md](../03-market-and-literature-research/Agentic_AI_Market_Survey_Full_Content_and_Integration.md)) so this defense package is self-contained.*

### Executive Summary

**Purpose.** This survey compares major agentic AI frameworks and platforms against the capabilities required for a proposed self-healing multi-agent system. The analysis distinguishes ordinary operational error handling (exceptions, retries, checkpoints and tracing) from semantic root-cause diagnosis (which agent introduced the error and at which earlier step), and from closed-loop recovery (repair, verification, resumption and learning).

**Key finding.** The market is mature for orchestration, tool calling, traces, retries, guardrails, memory and checkpoint-based recovery. However, the surveyed products do not natively provide the complete closed loop of: semantic failure detection → culprit-agent attribution → originating-step localisation → targeted repair → verification → resume from a corrected state → retain the successful repair for future use.

**Recommended FYP position.** Use an existing framework such as LangGraph, Google ADK, CrewAI or Microsoft Agent Framework for commodity orchestration and persistence. Concentrate the student contribution on four modules: Root-Cause Localizer, Repair Agent, Verification Agent and Verified Repair Memory.

**Core research gap:** Existing SDKs can observe, retry and resume workflows; ERRORPROBE can attribute semantic failures; the missing integration is to turn a verified diagnosis into a verified repair and resume execution from the corrected state.

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
