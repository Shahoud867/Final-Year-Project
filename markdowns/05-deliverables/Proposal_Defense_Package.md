# Granite — Proposal Defense Package (Guide §16)

*Content for the 10 required slides, assembled from the plan doc and its supporting files. This is ready-to-slide content, not a formatted deck — turn each section below into one slide.*

---

## Slide 1 — Title and one-line problem

**A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery**
*(short title: Granite — adopted 2026-08-24, from `Agentic_AI_Market_Survey_BS_FYP.docx` §6)*

Stream: A (research-derived) | Members: Shahoud Shahid (23i-2515), Muhammad Noor (23i-2520), Saif Shahzad (23i-2634) | Supervisor: Dr. Adil Majeed | Project code: F26-060-Granite

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
| Closest prior FYP | None targets this problem (checked against **all 660 titles, Spring-2019–Fall-2025, the department's complete published archive**) | Several use "multi-agent" as an application pattern (e.g. PropPal, LawSphere, PitchPerfect, CampusHive) — the agent team *is* the product; earlier years' nearest analogs (PilotBuddy, Hallucination Detection, NeuraSight) are anomaly/fault detectors in unrelated domains | None diagnoses *other* multi-agent systems; closest structural analog is AutoVulRepair (detect+patch, but fuzzing-based C/C++ vulnerability repair, unrelated mechanism/domain) |
| Current manual workflow | Human reads the trace, guesses | Flexible | Slow, unscalable, no measured accuracy |

Full detail: [Full_Literature_Landscape_Analysis.md](../03-market-and-literature-research/Full_Literature_Landscape_Analysis.md), [Commercial_Product_Comparison.md](../03-market-and-literature-research/Commercial_Product_Comparison.md), [FYP_Scope_CCP_and_Implementation_Plan.md §0.095](../01-planning-and-scope/FYP_Scope_CCP_and_Implementation_Plan.md) (full prior-FYP comparison across the entire Spring-2019–Fall-2025 published archive, added 2026-09-07).

## Slide 4 — Research and technical basis

9+ papers read in full (Who&When, AgenTracer, SDBL, TraceElephant, ErrorProbe, AgentAsk, PROTEA, plus GraphTracer/FALAT/DoVer triaged), 7 commercial platforms researched directly (not from marketing summaries). Full decision trail: [FYP_Scope_CCP_and_Implementation_Plan.md §0.08](../01-planning-and-scope/FYP_Scope_CCP_and_Implementation_Plan.md) (research-to-decision table).

## Slide 5 — CCP / complex activity justification

**8 of 9 Seoul Accord characteristics clear** (plan doc §2): conflicting requirements (depth vs. latency, generalization vs. specialization), no obvious solution (59.5% best-in-field after 15 months), depth of knowledge, unfamiliar issues, beyond standard practice, significant consequences, interdependence, ill-defined cause. Only diverse stakeholders (#6) remains open, pending real stakeholder contact.

## Slide 6 — Proposed contribution and solution

> Existing methods achieve up to 59.5% step accuracy but remain weak under two conditions: none is evaluated on an architecture absent from its own benchmark construction, and the strongest method explicitly fails on silent failures. We contribute a cross-architecture fault-injection benchmark, a diagnosis pipeline with task-constraint Semantic Error Diagnostic, a Repair Agent that generates candidate fixes (a gap confirmed by an independent 7-framework market survey — none ship this natively), and a Verified Automatic Repair engine that verifies and applies them — packaged as a framework-agnostic SDK.

**The pipeline in one line:** trace → execution graph → **Semantic Error Diagnostic** (deterministic; scoped to machine-checkable task constraints, *abstains and reports coverage* where none exist) → backward causal tracing (ErrorProbe method) → **Repair Agent** (candidate fix) → **controlled counterfactual replay** (recovery rate measured over N replays, decoding parameters pinned) → confidence-gated recommendation.

**Two things to say unprompted on this slide** — each closes an attack before it opens:
1. *"Controlled, not deterministic."* The replay **protocol** is deterministic and every non-LLM computation is bit-identical; LLM-step variance is measured over N replays, not assumed away. A panelist who knows LLMs aren't deterministic at temperature 0 is right, and we've already said so (R25).
2. *"We do not claim to detect arbitrary semantic wrongness."* The Semantic Error Diagnostic is scoped to task specifications that yield machine-checkable constraints — true for both active substrates — and **abstains** elsewhere, with abstention/coverage reported as a metric so the boundary is measured, not asserted.

Architecture: [architecture-sketch.md](../01-planning-and-scope/architecture-sketch.md). External components correctly classified (LLM = Core-assist, not the contribution) with a committed ~15-20% API-dependency budget — 80–85% of components never call a model at all, by committed mechanism, not by label.

## Slide 7 — POC / technical spike (mandatory, guide §12)

**8 spikes run, independently reproduced — exceeds the 1-spike minimum by 8×.** Guide §12 requires evidence *shown*, not described: put the JSON outputs or a live terminal on screen, don't just read this table.

| Spike | Result |
|---|---|
| 1. ErrorProbe reproduction | agent 62.5-85.7% / step 0-25% (means 71%/13%), simplified 2-stage pipeline, local 3B model, n=8 cases × 5 independent runs — range reported, not a single point estimate; real signal the approach works, full version still needed |
| 2. CrewAI instrumentation | Traced cleanly into 3 nodes / 2 correctly-ordered edges, resolved |
| 3 + 3b. Fault injection | Ground truth recoverable and unambiguous; first attempt was *self-corrected* by the agent — kept as a finding, so the benchmark records both propagation and self-correction |
| 4. Semantic Error Diagnostic | Catches known-wrong values including a plausible-magnitude near-miss ($20.00 vs $19.75 true), zero false positives |
| 5. Controlled counterfactual replay | Corrupted trace 97.2 → recovered 108.0 (`recovery_success: true`) |
| 6. Cyclic graph handling | Terminates correctly on a true cycle; control case with the bound disabled hit the 10,000-step cap — proves the safety bound is load-bearing, not a no-op |
| 7. Preventive classifier | **Honest negative result**: precision/recall/f1 = 0.25 with simple features — real finding, mitigation plan in risk-register.md R15 |
| 8. Repair Agent | **repair_success_rate 0.667 (4/6)**, n=6, chained into Spike 5's replay logic. Both failures share **one** fixable interface cause (model returned the derived result instead of the corrected parameter) — risk-register.md R17 |

**Lead with the two honest negatives, don't bury them:** spike 7's near-random classifier and spike 8's two failures are the most credible things on this slide. The guide's own words — *"a POC that disproved the assumption is usually more valuable"* — are worth quoting here.

**Every Tier 1 foundational item has a spike behind it.** The two Tier 2 items are exactly the two without passing evidence, which is why they carry pre-registered decision gates (slide 9) rather than assurances.

## Slide 8 — Evaluation plan

**Baseline:** ErrorProbe, reproduced from its published methodology — with a **pre-registered acceptance band**: accepted within ±10 points of the published 59.5% on a comparable-class backbone; otherwise both numbers are reported side by side per guide Annex A.2 ("faithful reproduction with transparent reporting" is itself a named contribution). Declared before the run, so the criterion can't be adjusted to fit the result.

**Data:** Who&When (184 real cases, MIT, in hand) + our own new cross-architecture benchmark (floor 500 / stretch 1,000 traces; TracerTraj conditional and on record, R11).

**Metrics:** agent/step accuracy · propagation-path F1 · silent-failure precision/recall **and coverage (abstention rate)** · task completion rate · diagnostic latency overhead (<50%, the measurable NFR) · recovery rate · repair success rate · **false repair rate** (via verification-gate ablation — the metric that keeps "verified" honest rather than asserted). Full plan: plan doc §11.

**What this evidence cannot support** — stated up front, not extracted: production-scale reliability claims beyond the tested frameworks and task domains.

**Success bands, if asked "what counts as success":** *failure* = no measurable improvement over baseline anywhere; *acceptable* = parity on Who&When + any measured cross-architecture result + silent-failure detection at nonzero coverage with high precision; *strong* = beats baseline on unseen architectures and >70% silent-failure recall at that precision; *exceptional* = strong, plus verified-repair recovery on >50% of previously-failed runs at a low false-repair rate.

## Slide 9 — Scope, risks and dependencies

**Committed core: 10 items, structured into two evidence tiers** (plan doc §7.0). All 10 are committed — the tiering records what evidence each already has, and attaches a decision rule where that evidence is weakest.

**Tier 1 — evidence-backed, unconditionally committed (8 items, every one with a spike behind it):** fault-injection harness · cross-architecture benchmark · Culprit Agent · Error Step Localization · Verification Agent · **Repair Agent** (generates the candidate fix — a gap surfaced by the market survey's own feature matrix, which rates automatic repair generation Not native / Custom / Experimental across all 7 surveyed frameworks; Spike 8: 4/6, R17) · Semantic Error Diagnostic · Verified Automatic Repair.

**Tier 2 — committed, with pre-registered Mid-1 decision gates (criteria written now, before any result exists):**

| Item | Honest status | Gate by Mid-1 | Recorded fallback |
|---|---|---|---|
| **Recovery Controller** | **No POC yet** — genuinely new mechanical work | LangGraph checkpoint/resume PoC, resume-from-verified-repair-point on ≥1 real workflow | Re-scope to resumption via controlled replay (Tier 1 already delivers it), recorded per §5.3 |
| **Verified Repair Memory** | **One real test, and it failed** — 0/8 memory commits, agent accuracy regressed 75%→50% on a 3B backbone | Re-test on a stronger backbone, same 8 Who&When cases | Ships as a memory-on/off **ablation study** — an evaluation contribution under §4's table, not a dropped feature |

*Say this as confidence, not confession: we pre-registered the decision rules before the results exist, which is exactly what §5.3 asks. In the worst case where both gates fail, self-healing still ships — repair, verification and replay-based resumption are all Tier 1.*

**Scope bands + feasibility engineering (2026-08-25, plan §7.2 + `06_Expanded_Scope_and_Feasibility_Plan.md`):** the whole scope is graded in four bands — Core (never descoped) / Advanced (budgeted, droppable only via a pre-registered ladder) / Stretch (unbudgeted, surplus-only) / Future (outside the FYP) — backed by an hour-by-hour effort budget (~1,130 plannable person-hours vs. ~1,130 budgeted), a walking-skeleton integration milestone at Mid-1, and a worst-case Minimum Defensible Product defined for every gate. If feasibility is challenged, the budget table is the answer, not reassurance.
**8 extensions**, filtered for CCP strength + market novelty + architectural fit: fault-taxonomy widening, 3rd architecture, cyclic-graph support, confidence calibration, preventive classifier, propagation map, explainable confidence reasoning, and **Framework Compatibility Layer** (new 2026-08-24):

> **Framework Compatibility Layer** — draws capabilities and evidence from all 7 surveyed orchestration frameworks (OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI), not narrowed to a single one as the market survey's own §7 recommends (that recommendation was already rejected — see risk-register.md R19). Distinct from the foundational cross-architecture benchmark: the committed core's 2–3 frameworks (CrewAI, LangGraph, +1 via extension #2) get *full* fault-injection and benchmarked evaluation; this extension is deliberately lighter — confirming the diagnosis pipeline can instrument and parse execution traces from each of the remaining frameworks, without building a full fault-injection benchmark for each. Broad *compatibility*, not broad *benchmarking*. Gated behind the core, same as every other extension; no POC yet.

**2 explicitly deprioritized**, not planned: cross-domain transfer testing, chaos testing.
**Total frozen feature count: 20** (10 foundational + 8 extensions + 2 deprioritized), plan doc §7.0.
**Top risks** (full register: [risk-register.md](../02-evidence-and-tracking/risk-register.md)): R1 (reproduction gap to 59.5% — **acceptance band now declared and pre-registered**, Annex A.2 fallback recorded), R5 (**cost — closed, quantified**, see the cost line below), R7 (literature-crowding, accepted risk, documented, standing gate-check), R15 (preventive classifier's weak first result), R16 (security/privacy, resolved with a threat model), R17 (Repair Agent — Spike 8, 4/6, one fixable cause behind both failures), R21/R22 (the two Tier 2 items — **gate criteria pre-registered 2026-08-25**), R23–R26 (this pre-defense audit's own decisions, recorded).

**Cost: $0, committed** (R37, 2026-09-04 decision) — every model call, including the reproduction and evaluation, runs on local Ollama, the same free backbone as all 8 real spikes to date (also $0). The paid-tier alternative was priced from measured token counts, not estimated, then explicitly rejected: a comparable-class backbone (Sonnet 5) for the reproduction alone would have cost ≈$353 recommended / ≈$881 pessimistic ceiling. One accepted tradeoff follows: the reproduction is now expected to land outside the pre-registered ±10-point acceptance band on backbone strength alone — reported honestly via Annex A.2 dual-reporting, not treated as a failure. Full working: [cost-estimate.md](../01-planning-and-scope/cost-estimate.md) §0.
**Professional and ethical compliance:** advisory-only diagnosis output with human-gated fix approval (extension #6), informed consent required before using any real user's trace data, synthetic fault injection restricted to own/consenting systems only — full statement: plan doc §0.09.

## Slide 10 — Team responsibilities and iterations

**Named ownership, assigned 2026-08-25 and recorded per guide §5.3** (plan doc §9, risk-register.md R24 — supersedes R6):

| Member | Owns | If removed, what disappears |
|---|---|---|
| **Shahoud Shahid** (23i-2515) | Data/Benchmark — instrumentation (CrewAI, LangGraph), injection operators, benchmark, licensing/release | The entire new benchmark; no cross-architecture evaluation is possible |
| **Muhammad Noor** (23i-2520) | Diagnosis — execution graph, ErrorProbe reproduction, Semantic Error Diagnostic, causal tracing | The attribution algorithm and the silent-failure detection claim |
| **Saif Shahzad** (23i-2634) | Platform — controlled replay/recovery engine, SDK, backend, dashboard, deployment | The product itself — nothing installable outside the dev machine |

Shared: architecture and integration, cross-subsystem QA, ethics/privacy commitments, defense preparation. Each member states their own subsystem aloud from this slide — the panel is applying guide §14.1's four ownership questions, and hearing three voices sets that tone early.

**DEI and ethical/legal (guide C.16 slide 10, added 2026-09-04 — plan doc §0.09):** DEI — the benchmark/SDK are planned open-source (MIT/CC BY 4.0), putting enterprise-grade diagnostic tooling within reach of resource-constrained teams, not just well-funded ones; the dashboard's status indicators pair color with text labels (not color alone), with a WCAG contrast check owed by Final-1; accuracy claims are stated as English-only (GSM8K, tau-bench), not silently generalized. Ethical/legal — advisory-only diagnosis output with human-gated fix approval, informed consent before using any real user's trace data, synthetic fault injection restricted to own/consenting systems only.

**AI-assisted development level (guide §C.8, added 2026-09-07 — named and justified as required "at this stage"):** developed at **Level 2 — AI-Assisted**, per the guide's own three-level maturity framework (Traditional / AI-Assisted / AI-DLC). Problem formulation, the CCP claim, architecture and baseline-selection decisions, evaluation design, and defense of every CCP-relevant component are the team's own judgment; AI assisted with isolated implementation tasks (PoC spike scripts, boilerplate, documentation), each disclosed with its verification status in `AI_Usage_Log.md` and condensed into the guide's own Form 13 format in `Form13_GenAI_Disclosure_Sheet.md`.

Two-semester timeline mapped to all 5 gates: plan doc §12, with the two Tier-2 decision gates and the full-reproduction milestone marked at Mid-1.

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
