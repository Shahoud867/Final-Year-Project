# Granite — Project Vision

*Standalone Project Vision document, closing the gap flagged in the proposal-defense audit (`07_Handbook_2026_Compliance_Audit_and_Response.md`): the vision existed scattered across §0–4 of [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md), the `poc-demo/frontend/src/pages/ProductVision.tsx` screen, and the archived [TraceCause_Product_Vision_UI.md](../../../archive/pre-granite/TraceCause_Product_Vision_UI.md), but had no single section a reader could point to. This document assembles it in one place — it cites the plan doc as the source of authority throughout and introduces no new decision.*

---

## 1. Problem

Multi-agent AI systems — several LLM-driven agents cooperating on a task (a planner, a researcher, a tool-caller, a writer) — fail often, and when they fail, no published method reliably explains *why*. The strongest published result as of 2026, ErrorProbe (ACL 2026 Findings), reaches 59.5% step-level attribution accuracy on its own benchmark — meaning it is still wrong more than four times in ten — and it names its own blind spot explicitly: it cannot catch **silent failures**, outputs that pass every check the pipeline runs but are semantically wrong. Every method surveyed (Who&When, AgenTracer, SDBL, ErrorProbe, and four adjacent 2026 papers) has also only ever been evaluated on the specific agent frameworks its own benchmark was built from — none has been tested on an architecture it wasn't tuned for.

Meanwhile, multi-agent systems are moving from research demos into production — coding agents, customer-support agents, research assistants. When one of these fails silently, a wrong answer ships with no error signal, and the team operating it has no tool built to catch it.

## 2. Motivation

Every commercial observability platform checked (LangSmith, Langfuse, Braintrust, Arize, Maxim, Opik, DeepEval — full comparison in [Commercial_Product_Comparison.md](../../../research/market/commercial-product-comparison.md)) captures execution traces well. As of 2026, two of them (LangSmith Engine, Arize Alyx) also claim automated root-cause diagnosis. **None of them publishes step-level attribution accuracy on any benchmark, detects general (non-RAG-specific) silent failures, or measures a recovery rate for a proposed fix before it ships** — and all are locked to their own tracing stack. The gap Granite closes sits precisely at that conjunction, not at any single missing feature (see the comparison table in [Proposal_Defense_Package.md](../proposal-deck/Proposal_Defense_Package.md) §3).

## 3. Target users

| User | What they need from Granite |
|---|---|
| **Primary — the engineering-team operator** running a multi-agent system in or near production (plan §0.06's notional client) | Pre-deployment fault testing against their own workflow before shipping; post-incident root-cause diagnosis when something breaks; a way to test a proposed fix before redeploying |
| **Secondary — product teams** consuming the diagnosis output | Confidence that a shipped answer was actually checked, not just logged |
| **Secondary — auditors / compliance reviewers** | Traceable evidence of what failed, why, and what was done about it |

Concretely grounded, not abstract: the project's own active benchmark substrate (tau-bench retail) is a customer-support multi-agent workflow — the same shape of system the primary user actually runs.

## 4. Proposed solution

Granite is a framework-agnostic diagnosis-and-repair layer that sits on top of a multi-agent system, not a replacement for existing trace-capture platforms. It:

1. **Attributes** a failure to the responsible agent and step (Culprit Agent, Error Step Localization), evidence-checked before being trusted (Verification Agent).
2. **Catches silent failures** other methods miss — outputs that look fine but violate the task's actual constraints — via a deterministic, rule-based verifier (Semantic Error Diagnostic), not an LLM asked to judge itself.
3. **Generates and tests a fix** (Repair Agent → Verified Automatic Repair) under a controlled replay protocol, reporting a *measured* recovery rate over repeated replays rather than asserting the fix works.
4. **Ships as an installable SDK** against a user's own CrewAI or LangGraph workflow, not just a benchmark result in a paper.

## 5. Product vision

A team running a multi-agent workflow installs Granite's SDK, points it at their own agents, and gets three things no single existing tool provides together: an attributed root cause, a flag for failures that produced no error signal at all, and a tested, measured-confidence fix — through a minimal dashboard and a documented API, deployed as a single container they control. Positioned as a **diagnosis layer**, complementary to (not competing with) the trace-capture platforms teams already use.

## 6. Research vision

Granite's diagnosis engine is built on ErrorProbe's published method as its algorithmic foundation, then measured on two axes no prior paper in this literature has measured together: does the pipeline generalize to an agent architecture (CrewAI, native LangGraph) absent from every reviewed paper's own benchmark construction, and does adding one deterministic constraint-check catch a failure class every anomaly-gated method in the corpus admits it cannot see. The research contribution is the **number that combination produces** — not the individual techniques used to produce it (each of which is already established practice; see [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §4.1's defense against "you just combined existing techniques").

## 7. Key objectives

1. Reproduce ErrorProbe's published method as a fair baseline, with the result reported honestly against a pre-registered acceptance band (±10 points of 59.5%), whichever way it lands.
2. Build and publicly release a new cross-architecture, ground-truth-labeled fault-injection benchmark (500–1,000 traces) on frameworks (CrewAI, LangGraph) no prior paper in the corpus used.
3. Add constraint-based silent-failure detection, with coverage/abstention reported as a first-class metric, not hidden behind a headline precision number.
4. Deliver a controlled counterfactual replay engine that measures a repair's recovery rate over repeated runs, rather than asserting a fix works.
5. Package the whole pipeline as an installable, framework-agnostic SDK plus a minimal operator dashboard, deployable as a single container.

## 8. Project boundaries

**In scope (committed core, [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §7.0):** the 8 Tier 1 mechanisms (evidence-backed via 8 real spikes) and 2 Tier 2 mechanisms (Recovery Controller, Verified Repair Memory — each behind a pre-registered Mid-1 pass/fail gate with a recorded fallback). Two committed architectures (CrewAI, LangGraph); a third only as a gated FYP-2 extension.

**Out of scope, named explicitly rather than left implicit** (full list, [Software_Design_Specification.md](Software_Design_Specification.md) §1): multi-tenant auth/billing/hosted SaaS signup; a message-queue/event-streaming layer; Kubernetes/multi-region/auto-scaling infrastructure; a caching layer (Redis/CDN); full RBAC; disaster-recovery infrastructure beyond the stated failure-handling commitments; any Tier 2 mechanism presented as already delivered before its gate resolves.

## 9. Expected outcomes

- A publicly released benchmark (MIT/CC BY 4.0) that any future paper in this space can evaluate against — the field currently has no cross-architecture, clean-control-included benchmark of this kind.
- A reproducible, honestly-reported ErrorProbe baseline number, whichever side of the acceptance band it lands on.
- A working, installable SDK a real team could point at their own CrewAI or LangGraph system — not a benchmark script.
- A measured answer, not an assumption, to: does this generalize past the frameworks it was tuned on, and does one deterministic check catch a failure class the field's anomaly-gated methods admit they cannot see.

## 10. Major capabilities

| Capability | What it does |
|---|---|
| Fault-injection harness | Deterministic, rule-based corruption of a multi-agent trace with recorded ground truth |
| Culprit Agent + Error Step Localization | Predicts the responsible agent and step for an observed failure |
| Verification Agent | Confirms a hypothesis against the real trajectory before it's trusted |
| Semantic Error Diagnostic | Catches well-formed-but-wrong ("silent") failures via constraint verification, abstaining (not guessing) where no checkable constraint exists |
| Repair Agent | Generates a targeted correction for a localized, verified failure |
| Verified Automatic Repair | Re-executes downstream under a controlled replay protocol and reports a measured recovery rate |
| Recovery Controller *(Tier 2, gated)* | Resumes execution from a verified repair point via checkpoint, or falls back to replay-based resumption |
| Verified Repair Memory *(Tier 2, gated)* | Stores and retrieves successful repair patterns, or ships as an honest memory-on/off ablation if the gate fails |
| SDK + backend + dashboard | Installable, framework-agnostic instrumentation with a 3-screen operator console |

## 11. Novelty / contribution

Three contribution types (guide §4's table, all claimed): a **data/resource contribution** (the new cross-architecture benchmark), a **method contribution at an identified gap** (silent-failure verification + cross-architecture generalization, measured together for the first time in this literature), and a **system/architecture contribution** (the deployable SDK — per the guide's own note, "in most Stream A projects... the largest and most defensible contribution"). Full contribution statement and delta-from-ErrorProbe: [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §3–4.

## 12. High-level future product

Beyond the FYP's committed core, the roadmap (13 named extensions, [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §7.0) points toward a product that: widens the fault taxonomy and architecture coverage; publishes a confidence-calibration curve; offers a cheap single-pass diagnosis mode alongside the full pipeline; gates auto-suggested fixes behind a confidence threshold before trusting them unsupervised; ships CI regression checks, webhook alerts, and natural-language incident reports; and packages the benchmark with a public leaderboard. Deliberately **not** on this roadmap, named so no reader has to infer its absence: multi-tenant SaaS billing, cross-domain transfer testing, chaos testing, an RL-trained classifier, and full custom-model training — all explicitly parked ([FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §7.0, "Future" band).

---

*This document introduces no scope, mechanism, or claim beyond what [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md), [Software_Design_Specification.md](Software_Design_Specification.md), and [risk-register.md](../../../docs/registers/risk-register.md) already commit to. Where a future revision needs to say something new, it belongs in those documents first, cited here second — the same discipline the SDS already applies to itself.*
