# Granite — FYP Scope, CCP Rating, and Implementation Plan

**Official FYP Project Title** (adopted 2026-08-24, from `Agentic_AI_Market_Survey_BS_FYP.docx` §6): *A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery*. "Granite" remains the permanent short title / product brand — see `FYP_Registration_Form_Answers.md` for the full title decision record.

*Written against [FAST_FYP_Student_Idea_Selection_Guide_School_of_Computing.pdf](../../docs/FAST_FYP_Student_Idea_Selection_Guide_School_of_Computing%20%281%29.pdf) (all 30 pages read), using [ErrorProbe_Baseline_Selection.md](../03-market-and-literature-research/ErrorProbe_Baseline_Selection.md) as the baseline justification and [Full_Literature_Landscape_Analysis.md](../03-market-and-literature-research/Full_Literature_Landscape_Analysis.md) for the gap evidence. Stream: **A — research-derived** (starts from ErrorProbe, ACL 2026 Findings). See also: [datasets.md](datasets.md), [resources.md](resources.md), [architecture-sketch.md](architecture-sketch.md), [risk-register.md](../02-evidence-and-tracking/risk-register.md), [Proposal_Defense_Package.md](../05-deliverables/Proposal_Defense_Package.md), [Commercial_Product_Comparison.md](../03-market-and-literature-research/Commercial_Product_Comparison.md), [Guide_Compliance_Audit.md](../02-evidence-and-tracking/Guide_Compliance_Audit.md), [AI_Usage_Log.md](../02-evidence-and-tracking/AI_Usage_Log.md) — this file is the index; those are the supporting detail, kept in sync with it.*

---

## 0. One-line idea

> Build a failure-attribution and recovery system that generalizes to multi-agent architectures no prior paper has tested on, catches the "silent failures" the strongest existing method (ErrorProbe) admits it cannot detect, and ships as an installable, framework-agnostic testing product rather than a benchmark result in a paper.

This is a **deliberately narrower** scope than the original "AgentTestLab" pitch in [TraceCause_AgentTestLab_Pitch.md](../06-archive-superseded/TraceCause_AgentTestLab_Pitch.md) (that draft had ~10 layers, health scores, marketplace framing — too broad for Section 5's "one shared central problem" test and would trip the guide's explicit "feature accumulation" hazard). Everything trimmed from that draft is listed under §7 as an *optional extension*, not core.

---

## 0.05 SDG / thematic alignment (guide §1.3)

**Primary: SDG 9 — Industry, Innovation and Infrastructure**, target 9.5 (enhancing research and technological capabilities of industrial sectors).

> As multi-agent AI systems move from experimental prototypes into real production infrastructure (customer-support agents, coding assistants, research tools), the industry lacks reliable failure-diagnosis tooling for this new technology category — every commercial platform checked in [Commercial_Product_Comparison.md](../03-market-and-literature-research/Commercial_Product_Comparison.md) does trace *capture*, but none does automated, benchmarked failure attribution the way Granite does. Granite directly builds that missing piece of technical infrastructure, upgrading the reliability of a genuinely new industrial sector. The stakeholders are the engineering teams who need this infrastructure to scale AI adoption safely — exactly the risk CCP characteristic #7 (significant consequences, §2 below) already establishes as real and present.

Per the guide's own boundary (§1.3 box): this is context for the proposal, not a substitute for the CCP or contribution claim — kept to this one paragraph, not expanded or used to inflate the pitch.

## 0.06 Client (guide §5.2)

Stream A rule: *"The intended operator or user of the resulting system acts as the notional client. The scope of work states who would run the system and what they would need from it."*

**Notional client: an engineering team operating a multi-agent AI system in or near production**, grounded concretely (not abstractly) by the project's own active dataset choice — the benchmark's real build target is tau-bench retail, i.e. a customer-support/retail multi-agent workflow. What this client needs from the system: (1) pre-deployment fault testing against their own workflow before shipping it, (2) post-incident root-cause diagnosis when something breaks in production, (3) a way to test whether a proposed fix actually resolves the failure before redeploying. The system's committed core (§7) is scoped directly to those three needs — nothing in the core exists that this client wouldn't use.

## 0.07 Specifiability (guide §6)

**5 functional requirements, in the guide's required form:**

1. The system shall inject controlled, deterministic faults into a multi-agent workflow built on CrewAI or LangGraph and record the ground-truth agent and step responsible for each injected fault.
2. The system shall analyze a completed multi-agent execution trace and output a predicted responsible agent, step, and confidence score for an observed failure.
3. The system shall flag an output that passes standard error checks but violates the task's stated constraints (a silent failure), independent of whether any explicit error signal was raised elsewhere in the trace.
4. The system shall, given a candidate corrected value for a specific step, re-execute the downstream portion of the trace under a **controlled replay protocol** (frozen upstream context; affected steps re-run with pinned decoding parameters) and report whether the corrected trace now succeeds, with recovery rate reported over N replays.

> **Wording note, 2026-08-25 (risk-register.md R25) — read this before saying "deterministic" out loud.** FR4 previously promised *deterministic* re-execution. That is not defensible for a workflow whose steps are LLM calls: LLM outputs are not deterministic even at temperature 0 on most serving stacks. Spike 5 was genuinely deterministic only because its toy pipeline is pure arithmetic. What is deterministic here is the **protocol** — which steps re-run, with what frozen upstream context, under which pinned decoding parameters — and every non-LLM computation in the replay, which is bit-identical. LLM-step variance is **measured**: recovery rate is reported over N replays with its variance, never inferred from one lucky replay. "Verified" means the recovery rate was measured, which is precisely the correct response to a nondeterministic component, not a weaker claim than determinism.
5. The system shall be installable via a documented SDK against a user-supplied CrewAI or LangGraph workflow without requiring modification to the core diagnosis algorithm.

**1 measurable non-functional requirement:** diagnostic overhead (wall-clock time added by running the diagnosis pipeline after a trace completes) shall be measured and reported as a percentage of the original workflow's execution time, with a stated target of under 50% for the single-pass mode (extension #6/core adaptive-depth work).

**Actors and data:** primary actor is the engineering-team operator (the human running Granite); secondary actor is the multi-agent system under test (CrewAI/LangGraph agents, not human); data held is execution traces (agent actions, tool calls, messages), the ground-truth fault-injection benchmark, and diagnosis records (agent, step, confidence, propagation path).

**Acceptance criterion for the hardest requirement (#3, silent-failure detection):** a diagnosis record is accepted as correctly identifying a silent failure if the constraint-verification module flags the trace *and* the flagged step matches the fault-injection harness's recorded ground-truth injection point, within an agreed tolerance — verified directly against synthetic benchmark cases where ground truth is known by construction (per spike 4's already-run mechanism test).

**Architecture:** see [architecture-sketch.md](architecture-sketch.md) — one page, as required.

**What's most likely to change:** the exact silent-failure constraint schema (rule set) as real benchmark data is generated, and the specific choice of 3rd architecture (extension #2) once that decision is actually made.

## 0.08 Research-to-decision table (guide §11)

| Source | Main finding | Relevance / limitation | Decision influenced | Planned evidence |
|---|---|---|---|---|
| ErrorProbe (ACL 2026 Findings) | 59.5% step accuracy SOTA on Who&When-Algo; explicitly admits it fails on silent failures | Chosen baseline — strongest published method, with a named, admitted gap | Adopted as the paper this project improves on | POC spike 1 (partial) + full 3-stage reproduction still owed |
| AgenTracer (ICLR 2026) | Programmatic fault injection removes the 30-hr/annotator manual-labeling cost | Methodology template, not a baseline itself; TracerTraj-2.5K turned out unreleased on direct check | Adopted the same injection technique for this project's own benchmark | Spikes 2, 3, 5 |
| Full 7-paper corpus, read in full | No paper tests generalization to a multi-agent architecture absent from its own benchmark construction | The core confirmed gap this project targets | CrewAI + LangGraph chosen as the two committed core architectures | Spike 2 (CrewAI mapping proven) |
| Commercial platform research (LangSmith, Langfuse, Braintrust, Arize, Maxim, Opik, DeepEval) | Automated diagnosis is emerging (LangSmith Engine, Arize Alyx, 2026) but none confirm counterfactual fix-testing or general (non-RAG-specific) silent-failure detection | Sharpens, doesn't eliminate, the differentiation claim | Repositioned as a diagnosis layer complementary to these platforms, not a competing observability product | Commercial_Product_Comparison.md, kept current |
| R7 literature triage (DoVer, "From Confident Closing to Silent Failure," others) | Real, credible, unpublished preprints exist in adjacent territory (counterfactual attribution, silent-failure detection) | Novelty risk, explicitly accepted rather than chased | Decision recorded not to fully read every preprint — strategy is beating ErrorProbe (peer-reviewed), not pre-empting unpublished work | risk-register.md R7, decision logged 2026-08-22 |
| AgenTracer repo, direct inspection | TracerTraj-2.5K not actually released; only a 127-row sample and the pipeline are public | Baseline dataset assumption was wrong until checked directly | Reproduce against Who&When only; TracerTraj comparison scoped to the 127-row sample, labeled honestly | risk-register.md R11 |
| FAST guide §12 | POC must be demonstrated with evidence at defense, not described | Direct proposal requirement | Ran **8 spikes** before defense, exceeding the 1-minimum bar by 8× | risk-register.md R1-R3, R10, R13-R15, R17, all independently reproduced |

---

## 0.09 Ethical compliance (guide §16 slide 9, §17 item 21)

Distinct from R16's security/privacy threat model — this is the "ethical" line the guide names separately. Three considerations, stated plainly: (1) the diagnosis engine's output (root cause, confidence) is advisory, not autonomous — a human reviews before any fix is applied (already committed via extension #6, confidence-gated fix approval), so the system cannot silently take an action with real consequences. (2) Trace data from a real customer's system is handled per R16's redaction/namespacing/retention commitments, and involving any real user or organization's data in testing requires their informed consent, arranged before use, not assumed. (3) The benchmark's synthetic fault injection is applied only to the project's own toy/test workflows or to consenting pilot users' systems — never to a third party's production system without explicit permission. No new build work follows from this section; it's a stated position the team should be able to defend if asked, same standard as everything else in this document.

---

## 0.1 Problem statement

> No published failure-attribution method for multi-agent AI systems has been tested on an architecture it wasn't built and tuned for, and none integrates a check for "silent failures" — confident, well-formed outputs that are wrong but trigger no anomaly signal — into its diagnosis pipeline. This is a complex computing problem: it has **no obvious solution** (the best published method, ErrorProbe, still gets step-level attribution wrong more than 4 times in 10, after 15 months and seven papers of field effort); it involves **conflicting requirements** (diagnostic depth vs. latency, generalization vs. specialization, trace completeness vs. privacy); it spans **two normally separate skill areas** (data engineering — instrumenting real multi-agent frameworks — and causal-reasoning/evaluation method design); and it has **significant consequences** — multi-agent systems are moving into production (coding agents, customer-support agents, research assistants), and a silent failure that ships an incorrect answer with no error signal is precisely the failure mode current tools cannot catch.

This was previously scattered across §1 (CCP statement) and §3 (contribution statement) rather than stated once, standalone — added here since a panel expects this sentence first, not assembled from other sections.

---

## 1. The committed CCP problem statement (three-tier, per Annex C style)

| Level | Statement |
|---|---|
| Weak | Build a system that identifies which agent caused a multi-agent failure. |
| Developing | Build a failure-attribution system that identifies the responsible agent and step, evaluated against the Who&When and TracerTraj benchmarks. |
| **Strong (committed)** | Build a failure-attribution and recovery system that must **generalize to multi-agent architectures absent from any prior paper's benchmark construction**, **detect silent failures that produce no anomaly signal** (ErrorProbe's stated blind spot), **model the causal propagation path** through interdependent agents, **test corrective interventions via controlled counterfactual replay** under a stated diagnostic-latency budget, and **operate as an installable, framework-agnostic SDK** against a real user-supplied multi-agent workflow — while bounding trace-data privacy exposure and diagnostic overhead. |

Per the guide's own diagnostic test (§C.14): the Strong statement names competing objectives (generalization vs. specialization; diagnostic depth vs. latency; trace completeness vs. privacy) and a failure consequence (undiagnosed silent failures ship wrong output to end users). That is what distinguishes it from the Developing tier, which is just "reproduce and re-benchmark."

---

## 2. CCP rating against the Seoul Accord's 9 characteristics

Self-rated in the same format as Annex C.13 (`agent-autopsy/FAST_FYP_Student_Idea_Selection_Guide...pdf`, pp. 28–29). The guide requires "some or all," not all nine — its own worked "Strong" examples clear 6–9. This idea clears **8 clearly, 1 weakly** — ahead of most of the guide's own benchmark examples.

| # | Characteristic | Status | Evidence |
|---|---|---|---|
| 1 | Conflicting requirements | **Clear** | Diagnostic depth vs. latency; trace completeness vs. privacy; generalization vs. specialization to known architectures |
| 2 | No obvious solution / depth of analysis | **Clear** | Best published step accuracy is still 59.5% (ErrorProbe) after 15 months and 7 papers — not a solved, copyable problem |
| 3 | Depth of knowledge | **Clear** | Requires execution-graph modeling, causal/counterfactual reasoning, distributed tracing, LLM evaluation methodology |
| 4 | Unfamiliar issues | **Clear** | Delayed error manifestation, LLM non-determinism, cross-architecture generalization — not routine dev issues |
| 5 | Beyond standard practice | **Clear** | No off-the-shelf framework solves attribution + silent-failure detection + counterfactual recovery out of the box |
| 6 | Diverse stakeholders | Weak | Present (AI/ML engineers as operators, downstream product teams as consumers of the diagnosis, auditors needing traceable evidence) but under-argued — strengthen at proposal stage by naming real pilot stakeholders, per the guide's own note that this is "the most commonly missing characteristic" |
| 7 | Significant consequences | **Clear** | Multi-agent systems are moving into production (coding agents, customer support, research assistants); a missed silent failure ships an incorrect answer undetected |
| 8 | Interdependence | **Clear** | The entire problem is that failures propagate through interdependent agent sub-problems — this is what the execution graph exists to model |
| 9 | Ill-defined requirements or cause | **Clear** | See the resolution paragraph below — three specific unknowns are named, and the system's own pipeline is the mechanism that resolves them |

**Characteristic 9 — the fix, stated as the proposal paragraph to use verbatim:**

> At diagnosis time, three things are unknown and must be investigated, not assumed: (1) whether a given trace contains a failure at all — silent failures produce no explicit error signal, so their presence itself is uncertain; (2) which agent and step is the true origin, which may be many steps upstream of where the failure becomes visible; and (3) what the correct behavior would have been, which is not recorded anywhere in the trace and must be hypothesized and tested via controlled counterfactual replay. The system's three-stage pipeline — constraint-based silent-failure flagging → backward causal tracing → controlled counterfactual replay — is the mechanism by which this uncertainty is progressively resolved, and the proposal-stage POC (§10) is the first evidence that this resolution process works on a real, if small-scale, case.

This satisfies the guide's own instruction for row 9 ("students should show how research, stakeholder study, experiments or a POC will reduce this uncertainty") by naming the unknowns explicitly and tying their resolution to a concrete mechanism plus POC evidence, rather than leaving it implicit in the architecture.

**Action still open before proposal defense:** convert characteristic 6 from "weak" to "clear" by naming real stakeholders actually contacted (§B.1's stakeholder-contact evidence bar applies even though this is Stream A, since the deployable-system half of the claim is real) — this is the one remaining gap standing between 8/9 and a full 9/9.

---

## 3. Contribution statement (Section 4 template)

> **Existing failure-attribution methods (Who&When, AgenTracer, SDBL, ErrorProbe) achieve up to 59.5% step-level accuracy, but remain weak under two conditions: (1) none is evaluated on a multi-agent architecture absent from its own training or benchmark construction, and (2) the strongest method, ErrorProbe, explicitly fails on "silent failures" that produce no anomaly signal.**
> **We are building (a) a cross-architecture failure-attribution benchmark from controlled fault injection into multi-agent frameworks never used by any of the seven papers surveyed, and (b) a diagnosis pipeline that adds task-constraint verification to catch silent failures — packaged as a deployable, framework-agnostic testing SDK: a working product, not a research prototype.**
> **We validate it by building our diagnosis engine's core attribution algorithm on ErrorProbe's published method and measuring its real accuracy on Who&When and our own new cross-architecture benchmark: step/agent accuracy, propagation-path F1, silent-failure precision/recall, and diagnostic-latency overhead.**

*(Presentation note, 2026-08-22: wording above shifted from "reproduce ErrorProbe as our baseline" to "build our diagnosis engine on ErrorProbe's method" — same underlying work and numbers, panel-facing framing now leads with the product being built, not a paper being compared against. The guide's own Section 4 template and evaluation requirements are unchanged underneath; see §4 and §11 for the technical detail this still rests on.)*

This maps to two contribution types from Section 4's table: **Data/resource contribution** (the new benchmark) and **Method contribution at an identified gap** (silent-failure verification + cross-architecture generalization) — plus **System/architecture contribution** (the deployable SDK, which the guide notes is "in most Stream A projects... the largest and most defensible contribution," §A.3).

---

## 4. The delta from ErrorProbe (Section A.2 template)

> **ErrorProbe reports 59.5% step accuracy on Who&When-Algo and 44.4% on TracerTraj under the assumption that the test-time multi-agent architecture overlaps with architectures seen during its own benchmark construction (CaptainAgent, MagenticOne; TracerTraj's 6 frameworks), and that failures always trigger a detectable MAST-taxonomy anomaly. We are building our diagnosis engine's attribution algorithm on Who&When (fully available, 184 real cases downloaded and confirmed) — adapting ErrorProbe's published method as the algorithmic foundation — then extending it to architectures never used in any of the seven papers (e.g., CrewAI, native LangGraph), and to silent, anomaly-free failures via constraint-based output verification against task specifications, validated on our own newly constructed, ground-truth-labeled fault-injection benchmark.**

**Correction, 2026-08-22:** TracerTraj-2.5K, cited above and in earlier drafts as a second reproduction dataset, is **not actually publicly released** — confirmed by direct download attempt, not by re-reading AgenTracer's own citation of itself. AgenTracer's repo states data/weights are "committed to" release "upon acceptance of the paper," has no LICENSE file, and ships only a 127-row code-domain sample. The reproduction claim above is corrected to rest on Who&When alone until AgenTracer's actual release; the TracerTraj comparison point is downgraded from committed to conditional (see risk-register.md R11).

Delta type, per Annex A.2's table: primarily **"Integration into an operable system"** (largest, most defensible for Stream A) combined with **"Adaptation to a new context"** (new architectures) and **"Constraint-driven engineering"** (bounded diagnostic-latency overhead, stated as a number once measured in the POC).

### 4.1 Defense against "you just combined existing techniques"

Say this plainly before a panel makes us say it defensively: none of the individual mechanisms are new. Rule-based fault injection is AgenTracer's own technique. Structural graph parsing is GraphTracer's own technique. Schema/constraint checking against a task spec is standard software-engineering practice, not a research contribution on its own. The guide is explicit that this is fine — "external components are expected, not exceptional" (core standard) — the question is never *whether* established techniques are used, it's *what they're used to prove*.

The claim is not "we invented a new graph-parsing method" or "we invented rule-based fault injection." The claim is the specific measurement that combination is built to produce, which nobody else — not the seven core papers, not GraphTracer, not FALAT, not any commercial platform checked in §Commercial Landscape — has produced: **whether a diagnosis pipeline built this way holds up on an architecture it was never tuned for, and whether adding one deterministic check catches a failure class every anomaly-gated method in the literature admits it cannot see.** Strip away every individual technique and ask what's left: a number. Either the system generalizes past its training ecosystem or it doesn't; either the constraint check catches silent failures or it doesn't. That number is the contribution — not the parts used to produce it. If a panelist asks "why isn't this just gluing together other people's ideas," the answer is: the gluing isn't the claim, the measurement neither Who&When through ErrorProbe nor GraphTracer nor FALAT ever ran is.

---

## 5. Why this survives the AI-resilience test (Section 7)

> *"Could a strong student with AI assistance build a working version of this in a week?"*

**No.** What AI assistance can accelerate: boilerplate SDK scaffolding, a first pass at the execution-graph data model, test generation, documentation drafts. What it cannot shortcut:

- Standing up and correctly instrumenting multiple real multi-agent frameworks (CrewAI, LangGraph) end-to-end, including handling their differing message-passing and tool-call semantics.
- Running controlled fault injection at scale to produce a large, ground-truth-labeled benchmark — this is data engineering effort, not a generation task.
- Reproducing ErrorProbe faithfully enough that a head-to-head comparison is defensible (its full pipeline — Strategist/Investigator/Arbiter + Verified Episodic Memory — is non-trivial to reimplement correctly).
- Designing and validating the silent-failure constraint-verification logic against real task specifications, where the failure mode is precisely "looks fine, isn't."
- Measuring and defending trade-offs (latency vs. depth, generalization vs. specialization) under real deployment constraints.

Per Section 7's own test, the remaining difficulty sits in **data engineering, evaluation design, and deployment reality** — exactly where the guide says a defensible FYP's difficulty must live.

---

## 6. External component classification (Section 14)

**The weaker version of this section (superseded below) just claimed the LLM was "swappable" without committing to *how much* of the system's actual work depends on it. That's not sufficient — a system can pass a trivial replacement test while still being 50%+ API-dependent for anything that matters.** Every component below is committed to a specific implementation mechanism, not just an "own work" label, so the ~15–20% API-usage target is something the team can point to and defend, not assert.

| Component | Mechanism (committed) | API-dependent? |
|---|---|---|
| Fault-injection operators | Rule-based, deterministic corruption (matches AgenTracer's own perturbation-operator approach) | **0%** |
| Execution-graph construction | Structural parsing of message/reference identifiers (matches GraphTracer's approach: "parse references, extract unique identifiers"), not an LLM asked "what did this depend on" | **~0%** |
| Backward causal tracing | Pure graph traversal (BFS from the failure node through the dependency graph) | **0%** |
| Confidence scoring | Computed from graph features (out-degree, betweenness centrality — matches GraphTracer's own formula), not "ask the LLM how confident it is" | **0%** |
| **Semantic Error Diagnostic** — silent-failure constraint verification (the headline novel claim) | **Rule/schema-based**: checks output against task-spec constraints programmatically (value ranges, required fields, logical consistency with stated tool results) — **not** "ask an LLM if this seems semantically wrong." This is the single most important commitment in this table: if this module is LLM-judged instead, the project's actual differentiator becomes an API call wearing a system architecture. **Scoped** to specifications yielding machine-checkable constraints; **abstains** elsewhere, with coverage reported (§7.0 item 7, §11) | **0%** |
| SDK, backend, database, dashboard, deployment | Own code throughout | **0%** |
| Agent-under-test behavior (the target system being diagnosed) | Necessarily an LLM — this is the test fixture, not the contribution | Inherent, not counted against the 15–20% budget (per §14's own logic: it's what's being diagnosed, not what supplies the diagnosis) |
| Controlled counterfactual replay's re-execution step | Necessarily an LLM — re-running the corrected step to observe the outcome. The replay *protocol* around it (step selection, frozen upstream context, pinned decoding parameters, N-replay variance measurement) is own code and calls nothing | Inherent, small (N calls per candidate fix tested, N small) |
| ErrorProbe baseline reproduction (Strategist/Investigator/Arbiter) | Necessarily LLM-heavy — faithfully reproducing someone else's published method as a *baseline*, not claiming its reasoning style as Granite's own contribution | Inherent to reproduction, isolated to the baseline-comparison code path only |
| Natural-language incident report generation (extension #10) | LLM, thin layer over already-computed diagnosis data | Small, non-core |

**Estimated split, once built as committed above:** roughly 80–85% own logic (graph construction, tracing, scoring, constraint verification, SDK, benchmark), 15–20% necessarily API-dependent (agent-under-test behavior, counterfactual re-execution, ErrorProbe reproduction, thin NL reporting) — matching the guide's expectation. **This is a target the build must be held to, not a fact already true** — the risk is real if Diagnosis Owner takes the lazy path on the constraint-verification module specifically.

**Replacement test (Section 14's own check), now meaningful rather than trivial:** if the LLM API were swapped for a different model, every row marked 0% above is entirely unaffected — not just "still runs," but produces byte-identical output, because none of those components ever call the LLM in the first place.

---

## 7. Committed core vs. optional extensions (Section 5.3)

**Committed core (must exist by Final-2):**

1. Fault-injection harness across ≥2 previously-unused multi-agent frameworks
2. New cross-architecture benchmark (ground-truth labeled, public task sources)
3. Diagnosis engine's core attribution algorithm — built on ErrorProbe's published method, validated against its numbers on Who&When (or documented deviation)
4. Diagnosis pipeline with silent-failure constraint-verification extension
5. Controlled counterfactual replay / recovery-testing engine
6. Framework-agnostic SDK + deployable backend + minimal dashboard
7. Full evaluation: step/agent accuracy, propagation-path F1, silent-failure precision/recall **and coverage**, task completion rate, latency overhead, all vs. the ErrorProbe baseline

*The 7 lines above are the **outcome-level** summary of the committed core, kept because it reads well in one breath. The authoritative, mechanism-level breakdown is §7.0's 10 foundational items immediately below — the two lists describe the same scope at different granularities and must not drift apart. Where they disagree, §7.0 wins.*

### 7.0 FROZEN — the final 20-feature set (2026-08-22, renamed 2026-08-23, extended 2026-08-24 three times — Repair Agent, then Framework Compatibility Layer + Verified Repair Memory + Recovery Controller, then a same-day reclassification moving the latter two into foundational to match the market survey's own "Core" rating; **structured into two evidence tiers 2026-08-25**, no items added or removed)

After multiple rounds of CCP filtering, academic-overlap checking (9+ papers), and commercial-market checking (7 observability platforms + 7 orchestration frameworks, see below), this is the final, closed list of *mechanisms*. **No further feature brainstorming should be added on top of this without explicitly reopening it** — every prior candidate list (the original 13 extensions, the alternative 10+10, the 13-gap analysis, the 5 new ideas, GPT's 16 features, GPT's 17-screen UI vision, and now `Agentic_AI_Market_Survey_BS_FYP.docx`) has already been filtered into or out of this set.

**Renamed 2026-08-23, in response to supervisor feedback that the original framing read as "14 features that map to 1 feature."** The fix is not fewer mechanisms — it's naming each one by the distinct thing it actually does, instead of bundling three separate pipeline stages under one vague label ("core attribution algorithm"). "Core attribution algorithm" is what ErrorProbe's real 3-stage architecture (Strategist → Investigator → Arbiter) already does under the hood — it was never one mechanism, it just had one name. Splitting it into its 3 real stages, each independently demoable and independently defensible under questioning (Section 14.1), is what actually answers the supervisor's critique. Two further renames (Silent-failure verification → Semantic Error Diagnostic, Counterfactual replay engine → Verified Automatic Repair) are pure naming clarity, same mechanism, no scope change.

**Extended 2026-08-24, after reviewing `Agentic_AI_Market_Survey_BS_FYP.docx`** (a market survey of 7 orchestration frameworks — OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI — plus a fresh read of ErrorProbe). Three of its four recommended modules ("Root-Cause Localizer," "Verification Agent," part of its closed loop) already exist in this list under matching or equivalent names — independent convergence on the same architecture, not new information. One genuinely did not exist yet: **Repair Agent**, the step that *generates* a candidate correction. FR4 (§0.07) already assumes a candidate corrected value is *given* to the counterfactual engine ("given a candidate corrected value for a specific step...") — nothing in the prior 16 actually produced that value. This survey named the gap correctly, so it's added below as foundational item #6.

**10 foundational (was 5, then 7 after the 2026-08-23 split, then 8 with Repair Agent, now 10 — = committed core items 1,3,4,5 above, plus the generalization claim spanning 1+the 3rd-architecture extension). Reclassified 2026-08-24: the market survey's own Table 1 rates all 8 of its "Core" capability rows the same way for the Proposed FYP column — Detect semantic wrong answer, Find culprit agent, Find originating error step, Causal backward error tracing, Automatically generate repair, Verify repair before applying, Resume from repaired point, Remember successful repairs. This project already treated the first 6 as foundational; the last 2 (Recovery Controller, Verified Repair Memory) were initially added as extensions, which was inconsistent with the survey's own classification — moved here to match it:**

**Structured into two evidence tiers, 2026-08-25 (see the tier rationale and gate criteria below the list).** All 10 items remain committed core — this is not a scope reduction, and nothing moves back to "extension." The tiering records *what evidence each item already has*, so the two items carrying the weakest evidence carry an explicit, pre-registered decision rule instead of an implicit hope. Recorded as a scope-structure decision per §5.3.

---

#### Tier 1 — Diagnosis & verified-repair core (evidence-backed, unconditionally committed)

*Every item below has a POC spike behind it (spikes 1–5, 8). These are committed without conditions.*

1. **Fault-injection harness** — unchanged
2. **Cross-architecture benchmark** — unchanged
3. **Culprit Agent** *(renamed from "core attribution algorithm," agent-identification half)* — the Strategist-stage hypothesis of *which agent* is responsible
4. **Error Step Localization** *(renamed from "core attribution algorithm," step-identification half)* — the Strategist-stage hypothesis of *which step* is responsible
5. **Verification Agent** *(renamed from "core attribution algorithm," the tool-grounded verification half — this was always the Investigator stage, not a new mechanism; see plan §12's Mid-1 priority, "tool-grounded Investigator + Verified Episodic Memory")* — evidence-grounded confirmation of a hypothesis against the real trajectory before the Arbiter commits to it
6. **Repair Agent** *(new 2026-08-24, sourced from `Agentic_AI_Market_Survey_BS_FYP.docx` §6.1 step 5)* — generates a targeted correction (prompt, tool argument, structured output, or function logic) for the localized, verified failure. Feeds the candidate value FR4 already assumes exists. **POC run 2026-08-24 (Spike 8, `poc_spike8_repair_agent.py`): repair_success_rate 0.667 (4/6), local 3B model, real result chained into Spike 5's replay logic. Both failures traced to one precise, fixable root cause — see risk-register.md R17.**
7. **Semantic Error Diagnostic** *(renamed from "silent-failure verification")* — task-constraint verification catching outputs that are well-formed but semantically wrong. **Scope of the claim, stated before a panel states it for us (2026-08-25):** *We do not claim to detect arbitrary semantic wrongness. We claim that where the task specification yields machine-checkable constraints — as it does for both of our active substrates, GSM8K's numeric answers and tau-bench retail's policy rules and action sequences — a deterministic verifier catches the well-formed-but-wrong outputs that every anomaly-gated method in this literature, by its own admission, cannot see; and we report the verifier's coverage (abstention rate) so the boundary of the claim is measured, not asserted.* Where no checkable constraint exists, the module **abstains** rather than guessing, and the abstention rate is a reported metric (§11). This is what makes the claim neither trivial (it is not a schema check — Spike 4 caught a plausible-magnitude near-miss, $20.00 vs $19.75 true) nor impossible (it never claims to understand meaning in general)
8. **Verified Automatic Repair** *(renamed from "counterfactual replay engine")* — re-executes downstream with Repair Agent's candidate fix under a **controlled replay protocol** (frozen upstream context, pinned decoding parameters) and reports a measured recovery rate over N replays before the fix is trusted. **Determinism claim, stated precisely (R25):** the protocol and every non-LLM computation in it are deterministic and bit-identical across runs; LLM-step outputs are not, so their variance is measured and reported rather than assumed away. Spike 5 validated the mechanism on a pure-arithmetic toy pipeline (97.2 → 108.0 recovered), which is why that spike *was* fully deterministic and the real system's claim is deliberately narrower
---

#### Tier 2 — Closed-loop recovery core (committed, with pre-registered Mid-1 decision gates)

*Both items below are committed core. Both carry the weakest evidence in the list — one has no POC at all, the other has one real test that **failed**. Each therefore carries a decision gate whose pass/fail criteria are written **now, before the results exist**, which is precisely what §5.3 requires of evaluation-criteria changes: criteria are not adjusted after seeing the outcome. The honest status of each is stated in its own entry below and on defense slide 9 — led with, not discovered later.*

9. **Recovery Controller** *(new 2026-08-24, from `Agentic_AI_Market_Survey_BS_FYP.docx` §6.1 step 7; reclassified from extension to foundational the same day to match the survey's own "Core" rating)* — applies a verified repair and resumes execution from a safe checkpoint, instead of restarting the whole workflow. Formally resolves the "Checkpointing" item that sat open since 2026-08-23. Distinct from Verified Automatic Repair (which re-executes downstream under the controlled replay protocol — fully deterministic in the current POC, Spike 5, only because that toy pipeline is pure arithmetic) — needs checkpoint-based state saving/restoring, which nothing else in this list provides. **No POC yet — genuinely new mechanical work, not a rename of something already tested.**
10. **Verified Repair Memory** *(re-added 2026-08-24 by explicit user decision, then reclassified from extension to foundational the same day to match the survey's own "Core" rating)* — stores successful error→diagnosis→repair patterns and retrieves them for similar future failures. **Naming caution, added 2026-08-25 — do not let these two blur, because a panel that spots the overlap will ask whether item #10 is just ErrorProbe's memory renamed:** Granite's **Verified Repair *Memory*** stores *error→repair patterns*, sits *after* verification-gated repair, and exists to reuse fixes; ErrorProbe's **Verified Episodic Memory** stores *diagnosis evidence*, sits *inside* attribution, and is reproduced by us only as part of the **baseline**. Different content, different position in the pipeline, different purpose — not a rename. **Honest status, stated plainly because it's now foundational, not a peripheral extension: this is not a fresh, unproven idea — it already has one real test, and that test failed.** Built once as "Verified Episodic Memory" (2026-08-23, `poc_spike1b_full_pipeline.py`, since deleted), run on all 8 real Who&When cases: 0 of 8 ever committed anything to memory, all 24 hypothesis-verifications came back NOT_SUPPORTED on the local 3B backbone, and agent accuracy regressed (75%→50%) in that same run. Committed to the core anyway, on the explicit condition that a re-test on a stronger LLM backbone happens before Mid-1 — if the re-test also fails, this is a foundational-item gap the team must be ready to explain under questioning (Section 14.1), not a footnote. risk-register.md R18.

**Tier 2 decision gates — pre-registered 2026-08-25, before any result exists (§5.3):**

| Item | Gate (must pass by Mid-1) | Pass criterion | Recorded fallback if it fails |
|---|---|---|---|
| **#9 Recovery Controller** | A checkpoint/resume PoC on **LangGraph** — chosen first because its native checkpointing makes it the lowest-risk target of the two committed frameworks | Demonstrates resume-from-verified-repair-point on ≥1 real workflow | Re-scoped to **"resumption via controlled replay"** — a capability Tier 1 already delivers (item #8) — and the re-scope recorded per §5.3. The closed loop still closes; only the resumption *mechanism* changes |
| **#10 Verified Repair Memory** | Re-test the memory mechanism on a **stronger backbone**, on the same 8 Who&When cases the original test used, so the comparison is like-for-like | ≥1 committed memory **and** no agent-accuracy regression versus the memory-off run | Ships as a **memory-on vs memory-off ablation study** ("repair memory: off vs on, and why off won") — an *evaluation contribution* under §4's own contribution table, not a silently dropped feature |

**Why tiering rather than demotion:** demoting #9/#10 to extensions would contradict the market survey's own Core rating (the reason they were promoted on 08-24) and would weaken the title's "…Verified Repair and Recovery" claim. Keeping them core while attaching pre-registered decision rules preserves the claim *and* the evidence discipline. In the worst case where both gates fail, self-healing is still delivered end-to-end: repair generation (#6), verification (#8), and resumption-via-replay are all Tier 1, evidenced items — what the gates decide is *how* resumption and memory ship, not *whether* the loop closes.

**8 extensions that survive CCP + market + architecture-fit + non-redundancy + workload-fit filtering — build these, in this priority order, only after the 10 foundational items work:**
1. Widen fault taxonomy (3 total types)
2. 3rd architecture (extends the generalization claim)
3. Cyclic/dynamic graph support
4. Confidence calibration (published reliability diagram)
5. Preventive clarification classifier
6. Failure Propagation Map
7. Explainable Confidence Reasoning
8. **Framework Compatibility Layer** *(new 2026-08-24 — the honest, scoped answer to "use features of all products, not only from one")* — draws capabilities and evidence from all 7 surveyed orchestration frameworks (OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI), not narrowed to a single one as the market survey's own §7 recommends (that recommendation was already rejected, see below). Distinct from the foundational cross-architecture benchmark: the committed core's 2–3 frameworks (CrewAI, LangGraph, +1 via extension #2) get *full* fault-injection and benchmarked evaluation; this extension is deliberately lighter — confirming the diagnosis pipeline can instrument and parse execution traces from each of the remaining frameworks, without building a full fault-injection benchmark for each. Broad *compatibility*, not broad *benchmarking* — building full benchmarks on all 7 would roughly double the core's engineering workload for a one-year BS project (risk-register.md R8: breadth-over-depth). Gated behind the core, same as every other extension; no POC yet.

**2 explicitly deprioritized — not planned, not "if time allows," genuinely parked:** Cross-Domain Transfer Testing, Chaos Testing for Agents. Revisit only if FYP-2 is materially ahead of schedule; do not plan around them.

**Items considered and NOT added, on record rather than silently dropped:**
- **Automatic Retry** (2026-08-23) — unconditional auto-retry of a failed step contradicts an already-committed principle (extension #12: auto-suggested fixes are gated behind a confidence threshold, because "no team will trust an auto-remediation tool that silently applies fixes with no visibility into how sure it is"). The defensible version of this idea is not a new feature — it's Verified Automatic Repair (#8) and Confidence Calibration (extension #4) working together: retry only fires once a fix is already verified and confidence-gated. Documented as a *behavior* of two existing mechanisms, not a standalone item.
- **Single-framework scope narrowing** (2026-08-24, from `Agentic_AI_Market_Survey_BS_FYP.docx` §7) — the survey's own scope-control advice recommends building against one orchestration framework only (it suggests LangGraph). **Explicitly rejected** — this would eliminate RQ2 (cross-architecture generalization across CrewAI + LangGraph + a 3rd framework), one of this project's two lead research claims, already CCP-justified and partially tested (Spike 2). Good general advice for a differently-scoped FYP; incompatible with this one's already-committed novelty case. **Resolved positively, not just rejected**: extension #8, Framework Compatibility Layer (above) — draw from all 7 surveyed frameworks via lightweight compatibility checks, while keeping full benchmarked rigor on only the 2–3 core frameworks.

**Note on the two reversals above (Checkpointing, Verified Repair Memory):** both previously sat in this "not added" list; both are now **foundational items #9–10** above (briefly extensions #9–10 on 2026-08-24 before same-day reclassification), added by explicit user decision that overrides the earlier evidence-based caution. The caution itself is preserved, not deleted — each item's honest risk status (Verified Repair Memory's real test failure; Recovery Controller's total lack of any POC) is carried into its foundational entry above rather than smoothed over now that it's "in scope," and as of 2026-08-25 that caution is formalized as the Tier 2 decision gates rather than left as prose.

**Status as of 2026-08-25 (see [risk-register.md](../02-evidence-and-tracking/risk-register.md) for the evidence behind each):** only the fault-injection harness has fully met its target validation; the benchmark, Culprit Agent, Error Step Localization, Verification Agent, Semantic Error Diagnostic, Repair Agent, and Verified Automatic Repair have partial real evidence (POC spikes run under their prior names) — together these are Tier 1. Tier 2 is exactly the two items whose evidence is weakest: Recovery Controller (no POC) and Verified Repair Memory (one test, failed), which is why the gates above exist. The 8 extensions are unstarted. This is expected at this stage — the point of freezing the list is to stop re-litigating *which* mechanisms, so all remaining time goes into building them, not selecting them again.

**Two-track justification, stated explicitly so no feature's motivation is ambiguous:** the **committed core** above is justified entirely by the ErrorProbe delta (§3–4) — that is the research/CCP claim, and it is the only place a comparison-to-prior-work claim is actually evaluated. The **13 extensions** below are justified by real product use-case demand, built on top of the improved core — they make Granite a tool teams would actually adopt, which is a separate, product-track justification, not a second wave of "we improve paper X" claims. Where a paper (PROTEA, AgentAsk) is named below, it is cited as *context* showing the underlying need is real and independently recognized — never as a comparison, since we do not benchmark against either (neither has a public dataset/code to compare against).

**Optional extensions — 13 items, each stated as one exact, buildable mechanism (not a category label), owned and scheduled so they span the whole of FYP-2 rather than being crammed into "if there's time." Record these as extensions; do not let them displace the committed core above.**

| # | Exact feature | Owner | FYP-2 slot |
|---|---|---|---|
| 1 | Widen the fault taxonomy from the POC's single validated type (corrupted tool output) to 3 total distinct types by adding communication corruption (swap a passed value for a plausible-but-wrong one) and context truncation (drop the last N% of upstream context before the next agent) — each a distinct injection operator with its own ground-truth label. (Corrected from an earlier draft that double-counted "tool-response corruption" as a 4th type; it is the same family as the POC's corrupted-tool-output fault.) | Data/Benchmark Owner | Weeks 1–6 |
| 2 | Instrument a third previously-unused architecture (OpenAI Agents SDK, or a fully custom in-house framework), extending the generalization claim from 2 to 3 architectures spanning different orchestration paradigms | Data/Benchmark Owner | Weeks 1–6 |
| 3 | Extend the execution-graph data model from a DAG to a general directed graph with cycle detection; define a max-revisit bound so backward causal tracing terminates on a loop; validate on ≥1 benchmark trace containing a real loop. **Justification: not a borrowed feature — LangGraph (one of our own 2 committed core architectures) natively supports cyclic workflows (retry loops, iterative refinement), so without this, Granite's own cross-architecture claim would be incomplete on the very framework it commits to instrumenting.** (Context, not a comparison claim: PROTEA names static-DAG-only as its own future work — we are not evaluating against PROTEA, which has no public benchmark or code to compare against; this only means the gap is independently recognized elsewhere in the field, not that we claim to improve PROTEA.) | Diagnosis Owner | Weeks 1–6 |
| 4 | Trace/diagnosis-record namespacing by a single API key per project — no cross-project visibility, no auth/RBAC/billing system built | Platform Owner | Weeks 1–6 |
| 5 | Compute and report a reliability diagram + Brier score for the diagnosis engine's confidence output across the full benchmark; publish the calibration curve as an evaluation artifact | Diagnosis Owner | Weeks 6–8 |
| 6 | Two selectable diagnosis modes — a cheap single-pass mode and the full multi-stage pipeline — with the accuracy-vs-latency trade-off between them measured and exposed as an SDK configuration flag | Diagnosis Owner | Weeks 6–8 |
| 7 | A lightweight binary classifier (not RL) trained on labeled clean-vs-corrupted message-handoff pairs from the fault-injection benchmark, flagging "ask a clarifying question here" at each agent handoff; report precision/recall on catching corrupted handoffs before propagation. RL upgrade explicitly deferred, only-if-time-remains | Diagnosis Owner | Weeks 8–14 |
| 8 | One GitHub Action that runs the evaluation suite against a fixed regression set on every push to the diagnosis-engine codebase, failing the build if step accuracy drops below a stated threshold | Platform Owner | Weeks 8–14 |
| 9 | One webhook that fires when root-cause confidence crosses a stated threshold, posting a structured JSON payload (agent, step, failure type, confidence, propagation path) to a configurable URL, demoable against Slack's incoming-webhook format | Platform Owner | Weeks 8–14 |
| 10 | A template-filling function that turns a completed diagnosis record into a short natural-language incident report: root cause, propagation path, confidence, counterfactual engine's suggested fix | Platform Owner | Weeks 8–14 |
| 11 | A stored-query + chart over the diagnosis-record database, plotting failure-type distribution per agent-version tag across runs — built entirely from data the diagnosis engine already produces | Platform Owner | Weeks 8–14 |
| 12 | Before a counterfactual-suggested fix is reported as "recommended," gate it behind a confidence threshold: below threshold → "needs human review," above threshold → "high-confidence, auto-suggested." **Justification: real use-case need — no team will trust an auto-remediation tool that silently applies fixes with no visibility into how sure it is; this is a baseline trust requirement for the product, not something we're building specifically to compare against PROTEA (we don't evaluate against it — no public benchmark exists to do so).** | Platform Owner | Weeks 8–14 |
| 13 | Package the new cross-architecture benchmark with a license (MIT/CC BY 4.0) and a static leaderboard page that accepts a submitted results file and ranks it against the reproduced baselines (ErrorProbe, Who&When methods) | Data/Benchmark Owner | Weeks 8–14 |

Deliberately dropped from this list: a hosted multi-tenant SaaS signup/billing flow. Item 4 (per-project API-key namespacing) is the scoped-down, defensible version of "multi-tenancy" — real auth/billing infrastructure is generic SaaS plumbing that doesn't touch the CCP and belongs in §14's post-FYP productization notes, not the graded scope.

---

### 7.2 Scope bands and descope ladder (added 2026-08-25 — see `06_Expanded_Scope_and_Feasibility_Plan.md` at the repo root for the full analysis, effort budget, and rationale; risk-register.md R27)

The frozen mechanism list above is unchanged. This section adds the **grading and sequencing layer** over it, plus eleven methodology/process commitments (statistical protocol, clean-control false-alarm study, ablation matrix, benchmark datasheet with propagation labels, human-baseline micro-study, self-correction analysis, cost–latency frontier, time-to-integrate metric, reproducibility kit, walking skeleton by Mid-1, CI from week 1) — none of which is a mechanism.

| Band | Contents | Rule |
|---|---|---|
| **Core** (mandatory) | 10 foundational items (Tier 1 + gated Tier 2) · evaluation v1 under the statistical protocol with FPR/clean controls, coverage, and the ablation matrix · benchmark ≥500 incl. clean controls + datasheet · SDK + backend + 3-screen dashboard · deployment · reproducibility kit · walking skeleton + CI | Never descoped; Tier 2 resolves via its gates only |
| **Advanced** (strengthens significantly) | Human baseline · self-correction analysis · cost–latency frontier · time-to-integrate · ext #1 (taxonomy→3) · ext #3 (cyclic) · ext #4 (calibration) | Budgeted; droppable only via the ladder below, each drop recorded per §5.3 |
| **Stretch** (only if Core lands early) | ext #2 (3rd architecture) · ext #5 (preventive classifier) · ext #6–7 (map, explainable confidence) · ext #8 (compat layer) · leaderboard · webhook/report/chart items | Unbudgeted — spends surplus hours only |
| **Future** (outside the FYP) | Cross-domain · chaos · RL · 7-framework benchmarking · SaaS/auth/billing · custom-model training | Report future-work section only |

**Pre-registered descope ladder** (drops happen in exactly this order, recorded): all Stretch → time-to-integrate → self-correction analysis → frontier → calibration → taxonomy 3→2 → benchmark 1,000→500 → cyclic (last among Advanced; claim-coupled to LangGraph) → **Core never drops**.

**Effort budget headline** (full table in the 06 doc §5.1): ~1,130 plannable person-hours (3 × ~15 h/wk × ~28 weeks, minus a 10% exam haircut) against ~1,130 budgeted — FYP-1 ≈490 h, FYP-2 ≈640 h — with Stretch unbudgeted, the ladder governing slippage, and scaffolding lines priced at Level-2 AI-assisted velocity. **Minimum Defensible Product per gate** is defined in the 06 doc §5.3 and the timeline note under §12 below.

---

## 8. Datasets — public, and reused vs. newly built

| Purpose | Dataset | Public? | Size | Role |
|---|---|---|---|---|
| Baseline reproduction | **Who&When** (Algo + Hand splits) | Yes — MIT license, public repo | 127 systems / 184 annotated tasks | Reproduce ErrorProbe's and prior methods' reported numbers |
| Baseline reproduction | **TracerTraj-2.5K** (AgenTracer) | **Corrected 2026-08-22: not actually released** — no LICENSE file found, repo states data/weights are "committed to" release upon paper acceptance | Only 127 rows real (one code-domain sample) | Downgraded from committed to conditional — see [datasets.md](datasets.md) and [risk-register.md](../02-evidence-and-tracking/risk-register.md) R11 |
| Underlying public task sources for injection — **active** | **GSM8K** (cheap prototyping) + **tau-bench (retail)** (real benchmark-building pass) | Yes — both confirmed downloaded, 2026-08-22, license-verified against primary sources, not citations | GSM8K 8,792, tau-bench retail 635 (see [datasets.md](datasets.md) §6) | Narrowed from 5 candidates to 2, 2026-08-22, per the project's own "pick 1–2, not all six" principle. GSM8K: single-integer answers match POC Spike 4's already-validated numeric near-miss mechanism cleanly. tau-bench retail: richer ground truth (full correct action sequences + policy rules), matches the product's real deployment domain (customer support) |
| Underlying public task sources — **benched, not currently built against** | GAIA (466), MBPP+ (378), MATH (12,500) | Yes — all downloaded and verified, kept on disk as optional second-domain material | See [datasets.md](datasets.md) §2/§6 | MATH benched specifically because its answers (equations/sets/intervals) fit Spike 4's numeric-near-miss check worse than GSM8K's plain integers. GAIA/MBPP+ benched only because the 2-source active plan already exceeds the 500–1,000 trace target — reintroduce only if GSM8K+tau-bench proves too thin. HotpotQA/SWE-bench considered and deliberately never pursued — SWE-bench carries the same heavy multi-agent-workflow-per-task cost that made the AgenTracer self-generation attempt infeasible (§4, risk-register.md R11b) |
| **New contribution** | Our own cross-architecture fault-injection benchmark | Will be released publicly (recommend MIT/CC BY 4.0, matching the field's own norm) | Target 500–1,000 labeled traces (matches AgenTracer's and the original pitch's scale) | Directly tests the confirmed cross-paper gap: generalization to unseen architectures |

Building the new benchmark on top of existing public task sources (rather than authoring new tasks) keeps annotation cost bounded — ground truth comes from the injection operator, not manual labeling, the same trick AgenTracer used to remove its "30-hour-per-annotator" cost.

---

## 9. Team ownership (Section 5's "would a meaningful contribution disappear" test)

| Member | Owns | Contribution type | If removed, what disappears |
|---|---|---|---|
| **Shahoud Shahid (23i-2515)** — Data/Benchmark Owner | Multi-framework instrumentation (CrewAI, LangGraph), injection operators, ground-truth benchmark, licensing/release packaging | Data/resource contribution | The entire new benchmark — no cross-architecture evaluation is possible |
| **Muhammad Noor (23i-2520)** — Diagnosis Engine Owner | Execution-graph construction, ErrorProbe reproduction, Semantic Error Diagnostic, causal tracing | Method contribution | The core attribution algorithm and the silent-failure detection claim |
| **Saif Shahzad (23i-2634)** — Platform Owner | Controlled counterfactual replay engine, Recovery Controller, SDK, backend API, containerized deployment, dashboard | System/architecture contribution | The product itself — nothing would be installable or operable outside the dev machine |

**Shared across all three (not owned by any one member):** architecture and integration decisions, cross-subsystem QA, the ethics/privacy commitments in §0.09 and R16, and defense preparation.

**Decision recorded 2026-08-25 (per guide §5.3):** the three role areas above are now **assigned to specific people**, closing the gap flagged since 2026-08-23. This was moved ahead of its previous "before Mid-1" target because the guide's Gate 1 row requires committed scope separated from optional extensions *"with primary technical ownership allocated to each member"* — that is a **proposal-defense** requirement, not a Mid-1 one, so deferring it would have been a hard requirement miss at the defense itself. See risk-register.md R24 (supersedes R6). Assignment is by skill fit across the three genuinely different skillsets the roles need (data engineering / causal-graph and evaluation method / full-stack deployment); if the team's own skill-fit review disagrees with this mapping, swap the names and re-record the decision here — what the guide requires is that ownership *is* allocated and recorded, which it now is.

**Correction, 2026-08-23 (kept on record, now resolved):** earlier drafts of this document and others in this folder labeled these three roles "Data/Benchmark Owner/2/3" as if the team had already assigned specific people to them. At that point the assignment had not actually happened. It has now — see the decision note above; the correction stays here rather than being deleted, so the record shows the gap and its closure, not a smoothed-over version.

Each owns a subsystem that is independently defensible under Section 14.1's four questions (explain it, justify alternatives rejected, predict what breaks, modify it under questioning), and each is individually a legitimate contribution type from Section 4's table.

---

## 10. Proposal-stage POC / technical spike (Section 12 — mandatory before proposal defense)

Highest-risk assumptions to test **before**, not after, approval:

1. **Reproduction feasibility:** run ErrorProbe's published methodology on a small subset of Who&When-Algo; confirm results land within a reasonable range of its published 59.5% step accuracy (or document why not). This is the single highest risk — if ErrorProbe cannot be reproduced credibly, the whole baseline comparison collapses.
2. **Instrumentation feasibility:** instrument one toy multi-agent workflow in CrewAI (a framework none of the 7 papers used) with basic trace capture; confirm the execution-graph data model can represent it.
3. **Injection feasibility:** inject one controlled fault type (e.g., corrupted tool output) into that toy workflow and confirm the ground truth is recoverable and unambiguous.

Per Section 12: this must be *demonstrated with evidence* at the proposal defense (what was tested, what result, what it changed), not promised as future work.

---

## 11. Evaluation plan (Section 13)

| Question | Answer |
|---|---|
| Algorithmic foundation | Our diagnosis engine's attribution logic is built on ErrorProbe's published method (own implementation, since its license for code reuse is unconfirmed — see [Full_Literature_Landscape_Analysis.md §3](../03-market-and-literature-research/Full_Literature_Landscape_Analysis.md)); its published numbers are the point its real-world accuracy gets measured against |
| **Reproduction acceptance band (pre-registered 2026-08-25, before any full-reproduction run)** | The reproduction is **accepted** if it lands within **±10 points of ErrorProbe's published 59.5%** step accuracy on a comparable-class backbone. If it lands materially below that band, we do **not** quietly re-baseline: both our measured number and the published number are reported side by side, per the guide's Annex A.2, which names *"faithful reproduction with transparent reporting"* as a legitimate contribution in its own right — precisely because published numbers are often hard to reproduce. Declared **now**, ahead of the run, so the criterion cannot be adjusted to fit the result — §5.3's own rule. Either outcome is a result; only an unreported gap would be a failure. Cost of the run and the model plan behind "comparable-class backbone": [cost-estimate.md](cost-estimate.md) (risk-register.md R26) |
| **Statistical protocol (pre-registered, 2026-08-25)** | Bootstrap 95% CIs over cases for every headline metric; fixed seeds; recovery rates reported over N=5 replays with variance; per-backbone reporting (as ErrorProbe itself does). One shared stats module used by every evaluation script. The analysis plan is finalized at Mid-1, before results exist |
| **Negative controls / false-alarm rate (added 2026-08-25)** | 15–20% of the benchmark (≥75 of 500 traces) are **clean controls** (harness run with injection disabled) — every corpus benchmark contains only failures, so pipeline-level FPR on healthy runs is unreported in the literature we reviewed. Reported: pipeline FPR + SED false-alarm rate, with CIs; provisional target <5%, finalized at Mid-1 |
| **Human baseline + time-to-integrate (added 2026-08-25)** | Inside the §13.1 UAT window: 6–10 proxy participants attribute 8–10 benchmark traces each under a 5-min/trace cap (accuracy + time vs. Granite — doubles as stakeholder and acceptance evidence), and each session measures minutes from `pip install` to first diagnosis on the participant's own workflow (target median <30 min). Small-N, descriptive, stated as such |
| **Ablation matrix** | Four pre-declared ablations, each isolating one claim: verification gate off → false-repair rate; memory on/off → VRM contribution; SED off → silent failures caught without it; graph-feature vs. LLM-stated confidence → justifies the 0%-API scoring choice |
| Data / cases | Who&When (baseline reproduction — fully available, 184 cases confirmed in hand) + our new cross-architecture benchmark (novel-architecture generalization test). TracerTraj comparison is conditional on AgenTracer's actual data release, not committed (see risk-register.md R11) |
| Metrics | Top-1 agent accuracy, top-1 step accuracy, propagation-path F1, **silent-failure precision/recall** (corrected 2026-08-24 — precision was missing; recall alone can't distinguish a real detector from one that flags everything) **and silent-failure coverage / abstention rate** (added 2026-08-25 — the fraction of cases the Semantic Error Diagnostic is applicable to at all; without it, "high precision" could describe a verifier that abstains on almost everything, and the scope boundary of §7.0 item 7's claim would be asserted rather than measured), diagnostic latency overhead (%), recovery success rate (task success before vs. after counterfactual intervention, i.e. of *previously-failed* runs specifically), **task completion rate** (overall task success, baseline MAS vs. self-healing MAS, across *all* runs — distinct from recovery rate, added 2026-08-24 from `Agentic_AI_Market_Survey_BS_FYP.docx` Table 4, was missing from the first pass), **repair success rate** (% of Repair Agent's generated corrections that actually fix the task, with vs. without Verification Agent gating — added 2026-08-24, same source), **false repair rate** (incorrect repairs the system accepted, measured via a verification-gate ablation — same source; this is the metric that keeps "verified" in Verified Automatic Repair honest, not just asserted). **Deliberately still excluded**: re-execution cost and repair reuse benefit — both measure Checkpointing and Verified Repair Memory, neither of which is in scope; adding the metric before the feature exists would be premature, not an oversight |
| Failure cases that matter | Silent failures (valid-looking, semantically wrong outputs); failures on architectures never seen during development; failures under injected latency/cost budget pressure |
| What the evidence can and cannot support | Can support: "the system generalizes better than ErrorProbe to unseen architectures, and catches a class of failures ErrorProbe cannot." Cannot support: general claims about production-scale reliability beyond the tested frameworks and task domains — state this limitation explicitly, per Section 13's own warning against over-claiming from a demo. |

Testing / Evaluation / Acceptance are tracked separately, per Section 13.1:
- **Testing:** unit/integration tests on the SDK, graph builder, injection harness; edge cases (empty trace, single-agent trace, malformed tool output)
- **Evaluation:** the metrics table above, against the ErrorProbe baseline
- **Acceptance:** a small user-acceptance round with real or proxy users (e.g., peers/faculty who build multi-agent systems) integrating the SDK against their own workflow, recorded per Section 13's acceptance-testing table (method, participants, tasks/results, issues found, outcome)

---

## 12. Full two-semester timeline, mapped to the 5 gates

```
FYP-1 (Semester 1)
──────────────────
Weeks 1–3   Problem exploration, CCP + contribution statement drafted,
            risk register opened, architecture sketch (one page)
Weeks 3–5   Proposal-stage POC (§10) executed — **ahead of plan as of
            2026-08-24: 8 spikes run, not the original 3-4** (reproduction,
            instrumentation, injection, silent-failure, controlled
            replay, cyclic-graph, preventive-classifier, repair-agent — see
            risk-register.md R1-R3, R10, R13-R15, R17). All 8 Tier 1
            foundational items now have real evidence; the 2 Tier 2 items
            are exactly those that don't, and carry pre-registered gates.
            Two real findings carried forward, not hidden: spike 7
            (preventive classifier) shows near-random signal (0.25 precision/
            recall) with simple features; spike 8 (Repair Agent) succeeded
            4/6, with both failures traced to one fixable interface cause
            (R17) — flagged below, not swept aside.
Week  5–6   ▶ GATE 1 — Proposal defense (scope approved)
Weeks 6–10  Stakeholder-informed requirements, SRS/SDS baselined,
            data/licensing cleared, riskiest subsystem prototyped.
            **Top priority, per spike 1's own result (12.5% step accuracy,
            simplified pipeline, n=8, local 3B model)**: build the full
            3-stage ErrorProbe reproduction (tool-grounded Investigator +
            Verified Episodic Memory) on a stronger backbone — the
            simplified version is nowhere near 59.5% and a fair baseline
            comparison depends on closing that gap, not just noting it.
            Acceptance band for that run is pre-registered in §11; cost
            is quantified in cost-estimate.md.
            **▶ TIER 2 DECISION GATES resolve here (§7.0):**
              · Recovery Controller — LangGraph checkpoint/resume PoC,
                else re-scope to replay-based resumption (recorded)
              · Verified Repair Memory — stronger-backbone re-test on the
                same 8 cases, else ships as a memory-on/off ablation
            ▶ GATE 2/3 — Mid-1 (requirements + design baseline)
Weeks 10–16 Core build:
              Shahoud (Data/Benchmark) — injection harness + 2 frameworks
                          instrumented
              Noor (Diagnosis) — execution graph + ErrorProbe reproduction +
                          Semantic Error Diagnostic (v1)
              Saif (Platform) — controlled replay engine (v1) + SDK skeleton +
                          containerized deployment (first attempt)
Weeks 16–18 Integration path proven end-to-end against approved design
            ▶ GATE 3 — Final-1 (working core system, exit gate)

FYP-2 (Semester 2)
──────────────────
Weeks 1–6   Full integration: harness → diagnosis engine → counterfactual
            engine → dashboard (product build, not just data work). Scale
            new benchmark to 500–1,000 traces. Full evaluation run against
            ErrorProbe baseline (both original and new cross-architecture
            benchmark).
            §7.0 extensions #1 widen fault taxonomy, #2 3rd architecture
            (Data/Benchmark Owner) · #3 cyclic graph support (Diagnosis Owner)
Weeks 6–8   Non-functional testing: latency overhead measured, failure/
            recovery paths demonstrated, deployment tested outside the
            dev machine, trace-data privacy handling verified (R16 threat
            model becomes a tested behavior, not just a written paragraph).
            §7.0 extension #4 confidence calibration (Diagnosis Owner)
            ▶ GATE 4 — Mid-2 (release readiness)
Weeks 8–14  User acceptance testing with real/proxy users; iterate on
            findings. SDK polish, dashboard build-out (propagation map,
            confidence-evidence panel) — the product half of this block,
            not only extension work.
            §7.0 extension #5 preventive classifier (Diagnosis Owner) —
            **contingent, not automatic**: spike 7 showed near-random signal
            on hand-written data; before committing this slot, re-test with
            real labeled pairs from the fault-injection harness (built
            Weeks 1–6) and cheap local sentence-embedding features — if it
            still doesn't improve, drop it rather than ship a known-broken
            classifier. §7.0 extensions #6 failure propagation map, #7
            explainable confidence reasoning (Platform Owner) — only
            pursued if core is stable.
Weeks 14–16 Documentation set completed (SRS, SDS, traceability matrix,
            test/deployment/handover plan); final packaging.
            ▶ GATE 5 — Final-2 (deployed system + project report)
```

---

**Minimum Defensible Product per gate (added 2026-08-25 — the worst-case demo each gate must still deliver; full table in `06_Expanded_Scope_and_Feasibility_Plan.md` §5.3):** Mid-1 = walking skeleton end-to-end + full reproduction number with band verdict + both Tier-2 gate outcomes + 50-trace pilot with clean controls + the two baselined design docs (hook interface, checkpoint schema). Final-1 = core integrated on real workflows in both frameworks, benchmark ≥200, SDK installable by a non-builder. Mid-2 = benchmark ≥500 with controls, evaluation v1 with CIs/FPR/≥2 ablations, deployed off the dev machine. Final-2 = full evaluation + human baseline + UAT + datasheet + reproducibility kit + release.

---

## 13. Deployment plan (Section 1.2)

| Dimension | Plan |
|---|---|
| Runs outside dev machine | Containerized (Docker); installable via documented steps by someone who did not build it |
| Realistic operating environment | Cloud VM or on-prem container target, stated and justified at proposal stage |
| Configuration and data | Seed/sample multi-agent trace data shipped separately from credentials/config; no hard-coded secrets |
| Non-functional behavior | Diagnostic latency overhead, throughput (traces/hour), and trace-data privacy handling stated as measurable targets and tested, not asserted |
| Failure and recovery | Documented behavior when the LLM API is unavailable, when a trace is malformed, when the injected framework produces unexpected output shapes |
| Handover | Source, build/run instructions, dependencies, licenses (Who&When: MIT; TracerTraj: Apache 2.0; our benchmark: to be released MIT/CC BY 4.0), known limitations, future work |
| Adoption context | Intended users: teams building multi-agent systems who need pre-deployment failure testing; realistic barrier: integration effort to instrument an arbitrary third-party agent framework — state this honestly as a known limitation, not concealed |
| Evidence of deployment | **Not yet producible — this is explicitly a Final-2 requirement, not a proposal-stage one** (guide §1.2's table is headed "What should be true by Final-2"). At proposal stage the honest claim is: deployment target chosen and justified (above), actual deployment record (where it runs, how installed, who can access it, what it cost) to be produced once the system exists to deploy. Flagging this row explicitly rather than omitting it, per the guide's own warning: "A screenshot of a local build is not deployment evidence" |

## 14. Post-FYP productization (explicitly separate from the graded requirement)

Per the guide (§1.2 box): *"Deployability is required; commercial success is not."* The following is **context for later, not part of the graded deliverable** — it should not be presented as a requirement in the proposal, only as a stated future direction:

- The SDK + deployable backend built for FYP-2 is architected to be the core of a hosted product ("Granite" or similar) — pre-deployment testing for teams shipping multi-agent systems.
- Commercialization path: open-source the SDK + benchmark (drives adoption, matches the field's own norm of MIT/Apache 2.0 licensing), offer a hosted diagnosis/dashboard service as the paid layer — a standard open-core model.
- This framing should stay in the "future work" section of the project report, not the contribution or evaluation sections, to avoid the guide's explicit warning against over-claiming from a demo.

---

## 15. One-year defensibility — why this isn't shadowed by faster-moving industry work

The field publishes roughly every 2–3 months (Who&When → AgenTracer → {SDBL, TraceElephant, ErrorProbe, AgentAsk, PROTEA} across 15 months). A pure-algorithm contribution risks being outpaced before Final-2. The moat here is deliberately **not** "a cleverer attribution algorithm" — it's built from things that are slow to replicate regardless of how fast a research lab moves:

1. **The cross-architecture benchmark itself.** Standing up multiple real agent frameworks and running fault injection at scale is data-engineering labor, not an insight a competing paper can shortcut by being smarter.
2. **The framework-agnostic SDK.** No paper in the 7-paper corpus ships a general-purpose, installable instrumentation layer — PROTEA is the closest and it's closed, Sony-internal, DAG-only.
3. **Silent-failure detection via constraint verification.** This targets a gap ErrorProbe *itself* admits, in writing, that it cannot close (§ "Limitations" of ErrorProbe) — not a gap we inferred, a gap the strongest existing baseline confessed to.
4. **Automated counterfactual recovery testing.** We do not evaluate against PROTEA — it has no public benchmark or code, so no comparison claim is made. What matters here is only that PROTEA (Sony, ACL 2026 Demo) independently confirms this is a real, recognized gap in the field: its own tool does something adjacent but manually, with a human approving every fix and no automated confidence scoring. That's context showing the feature isn't speculative, not a claim that we improve PROTEA.

**Standing instruction:** re-check the literature at each of the 5 gates (a 15-minute "has anyone closed this gap yet" pass), and record the result in the risk register. If a new paper closes one of these gaps before Final-2, that's a finding to report honestly, not a reason to panic — the benchmark and the deployable SDK remain the load-bearing contribution either way.

---

## 16. Self-check against Section 17's readiness checklist (selected items)

- [x] Problem, users, gap, contribution statable in one minute (§3–4 above)
- [x] CCP characteristics identified and justified (§2) — 8/9 clear; only #6 (diverse stakeholders) remains "weak," to be strengthened before defense
- [x] Contribution meaningful even without new algorithmic novelty — data + integration + evaluation contribution (§3)
- [x] Proposal-stage POC — **8 spikes run with real output**, including the silent-failure detector added after a panel-review pass caught it missing, and two honest negatives kept on record (§10 + [risk-register.md](../02-evidence-and-tracking/risk-register.md) R1–R3, R10, R13–R15, R17)
- [x] Baseline, success criteria, evaluation evidence, failure cases defined (§11) — **reproduction acceptance band pre-registered 2026-08-25**
- [x] Every external component classified — none in Core-replacement, API-usage mechanism committed per-component (§6)
- [x] Committed scope separated from optional extensions (§7), **and the committed core itself tiered by evidence with pre-registered gates on the two weakest items** (§7.0)
- [x] API/compute cost estimated with a real number, not deferred — [cost-estimate.md](cost-estimate.md), built from measured token counts across all 184 Who&When cases (closes R5)
- [ ] Real stakeholders contacted — **still open** — the one item nothing here can close
- [x] Deployment target stated (§13)
- [x] AI usage log — maintained and current, see [AI_Usage_Log.md](../02-evidence-and-tracking/AI_Usage_Log.md)
- [x] Architecture sketchable on one page — see [architecture-sketch.md](architecture-sketch.md)
- [x] RAID register opened — see [risk-register.md](../02-evidence-and-tracking/risk-register.md)
- [x] SDG/thematic alignment stated (§0.05)
- [x] Client identified (§0.06)
- [x] Idea specifiable — 5 functional reqs, 1 measurable NFR, actors, acceptance criterion (§0.07)
- [x] Research-to-decision table (§0.08)
- [x] Proposal defense package assembled — see [Proposal_Defense_Package.md](../05-deliverables/Proposal_Defense_Package.md)
- [x] Team ownership roles assigned to actual people — **closed 2026-08-25**: Shahoud/Data-Benchmark, Noor/Diagnosis, Saif/Platform (§9, risk-register.md R24 supersedes R6). Moved ahead of its old "before Mid-1" target because the guide's Gate 1 row requires ownership allocated *at the proposal defense*
- [ ] Prior-departmental-FYP comparison — **cannot be completed externally**, needs the team to check their own department's FYP archive (guide §10, second half)
- [ ] Each team member explains their own owned subsystem out loud, no notes — **still open**, the one test no document substitutes for (guide §8.2)

---

## Appendix: Market Survey Reference — Evaluation Plan & Scope Control (full excerpt)

*This is the full source excerpt from `Agentic_AI_Market_Survey_BS_FYP.docx` backing the metrics already integrated into this doc's own §11 above. Reproduced verbatim from [Agentic_AI_Market_Survey_Full_Content_and_Integration.md](../03-market-and-literature-research/Agentic_AI_Market_Survey_Full_Content_and_Integration.md) so this plan doc is self-contained.*

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

### 7. Scope Control for a One-Year BS Project

The complete research vision can become too broad. For a realistic one-year implementation, the project should deliberately constrain the environment:
- Use one agent framework only (recommended: LangGraph, because checkpointing and replay are already available).
- Use one or two task domains, such as code/tool-use tasks and structured reasoning tasks.
- Limit the MAS to approximately 3–4 roles so causal traces remain understandable.
- Implement a small taxonomy of failure types rather than attempting every possible semantic failure.
- Treat repair as targeted modification of prompts, tool arguments, structured outputs or small code functions; do not attempt unrestricted rewriting of the entire agent architecture.
- Require verification before any generated repair is applied or added to memory.
