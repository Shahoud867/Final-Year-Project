# Granite — FYP Registration Form Answers

*Compiled 2026-08-24 from the session working through the FAST FYP registration form. Reference this before submitting, and update it if any answer changes.*

---

## Project Title

**A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery**

Chosen 2026-08-24 — the market survey's own recommended title (`Agentic_AI_Market_Survey_BS_FYP.docx` §6, "Recommended BS Final Year Project"), adopted as the official title. "Granite" remains the permanent short title/product brand (unchanged, see below) — this title is the formal, full name for the registration form and defense documents.

Earlier candidates, kept on record, superseded by this decision:
- *Granite: Cross-Architecture Failure Attribution and Silent-Failure Detection for Multi-Agent AI Systems* (the prior recommendation, before the survey's title was adopted)
- *Granite: A Framework-Agnostic System for Diagnosing and Recovering from Multi-Agent AI Failures* (product-facing)
- *Detecting Silent Failures and Verifying Recovery in Multi-Agent AI Systems Across Architectures* (no brand name, plain technical)
- *Granite: Failure Attribution, Silent-Failure Verification, and Counterfactual Recovery Testing for Multi-Agent LLM Systems* (most complete, longest)

## Project Short Title

**Granite**

One word, permanent — chosen specifically because it won't need to change even if scope shifts. Considered and rejected alternatives (for the record, in case revisited): Causeway, Rootcast, Autopsy, Undertow, Culprit, Ripple, Recon, Triage, Fathom, Vigil, Halcyon, Meridian, Zenith, Astra, Solstice, Vantage, Zephyr, Steady, Clarity, Sure, True, Keen, Solid, Whole, Actual, Proof, Level, Given, Behold.

---

## Category of the Project

**Check: Generative AI** (primary) **+ Natural Processing Language / NLP** (secondary, if multi-select allowed)

- **Generative AI**: the entire subject matter is multi-agent systems built on generative LLMs (CrewAI, LangGraph); Granite's own attribution pipeline (Culprit Agent, Error Step Localization, Verification Agent) generates and verifies hypotheses via LLM calls, so the tool is partially generative itself, not just an observer; positioned directly in the GenAI observability market (LangSmith, Arize, Langfuse, Maxim, Opik all self-classify this way).
- **NLP**: every input processed is natural language (agent messages, tool outputs, trajectory excerpts); Semantic Error Diagnostic is a semantics-verification task; Verification Agent does evidence-quote extraction from text; Cross-Agent Consistency Verification extracts typed facts from natural-language agent messages.

**"Other:" field** — keep **"Agentic AI"**, optionally extend to **"Agentic AI / AI Observability"** — the latter is the actual industry category name (how LangSmith/Arize/Langfuse describe themselves, and the category Granite is benchmarked against). Other legitimate options if swapping: Multi-Agent Systems (MAS), Explainable AI (XAI), LLMOps / AI Testing & QA.

---

## Technologies (Select all that apply)

**Tick: Python, Postgres, JavaScript Fullstack (MERN), one of AWS Development / Azure Development**

| Item | Tick? | Why |
|---|---|---|
| Python | ✅ | Backend, diagnosis engine (all 5 renamed foundational features), SDK, all POC spikes |
| Postgres | ✅ | Trace/diagnosis-record database — open-source, matches $0-cost commitment |
| JavaScript Fullstack (MERN) | ✅ | Closest available checkbox for the React frontend the web dashboard needs (Failure Propagation Map visualization, confidence-evidence panel); note backend is actually Python, not Node — MERN is an approximation, not literal |
| AWS Development *or* Azure Development (pick one) | ✅ (pick one) | Architecture is cloud-agnostic (Docker + any host); pick whichever you have free student credits for — a hosting decision, not an architectural requirement |
| Selenium | ⚪ optional | Only if committing to automated dashboard UI testing (fits plan doc §13.1's testing commitment) |
| Redis / ElasticSearch AWS | ⚪ optional | Not needed at target scale (500–1,000 traces); reasonable for "real product" positioning only |
| Everything else (MEAN, C#/.NET, React Native, Android-JAVA, PHP, iOS, JAVA, Microsoft SQL, Unity, Flutter, Ruby on Rails, Salesforce) | ❌ | None touch any part of the committed scope |

**"Other:" field** — add: **Docker** (containerized deployment, explicitly committed in architecture-sketch.md, not covered by any checkbox), **FastAPI** (the actual Python backend framework), **CrewAI / LangGraph** (the two multi-agent frameworks the product instruments), **Ollama** (local LLM serving — the actual $0-cost inference layer all 7 POC spikes ran on). Lower priority if space is limited: NetworkX (graph library, Spike 6), Pydantic (schema/type enforcement for the silent-failure module).

---

## Project Scope (one paragraph)

**Re-answered 2026-08-24** — the version below supersedes an earlier draft (kept at the bottom of this section for the record) that predated Repair Agent, Recovery Controller, and Verified Repair Memory. That earlier draft omitted 3 of what are now 10 core items — an accurate scope answer can't skip 30% of the core.

> Granite is a deployable SDK and diagnosis platform that identifies why multi-agent AI systems fail — including which agent and which step caused it — catches failures that look correct but aren't (silent failures with no detectable error signal), and closes the loop by generating a candidate fix, verifying it through controlled counterfactual replay — frozen upstream context and pinned decoding parameters, with recovery rate measured over N replays — resuming the workflow from the verified repair point, and retaining successful repairs for reuse on similar future failures. The system generalizes across multi-agent architectures (CrewAI, LangGraph, and a third framework) that no prior published method or commercial observability platform has been evaluated against, closing two gaps ErrorProbe (ACL 2026), the strongest published baseline, admits it does not close. Scope is bounded to a fixed, non-negotiable 10-item foundational core — a fault-injection harness, a new cross-architecture benchmark, three-stage evidence-grounded failure attribution, silent-failure verification, and a full four-stage repair pipeline (generate, verify, resume, remember) — evaluated against the ErrorProbe baseline, followed by 8 product-facing extensions (confidence calibration, preventive failure warnings, failure-propagation visualization, cyclic-graph support, cross-framework compatibility) built only after the core is proven. The deliverable is a full-stack build: a public benchmark, a diagnosis engine, and an installable backend/dashboard — not a single research script. The 10-item core is structured into two evidence tiers: eight Tier 1 items each have a proof-of-concept spike behind them, while the two closed-loop items — Recovery Controller and Verified Repair Memory — are committed with pre-registered Mid-1 decision gates and recorded fallbacks, stated honestly rather than hidden: Recovery Controller has no POC yet, and Verified Repair Memory's one real test failed on the free local backbone and needs re-validation on a stronger model before Mid-1.

**Scope type: Moderate** — narrow, tightly-bounded mandatory core (one baseline, two frameworks, one primary benchmark); broader total ambition across both semesters, controlled by gating extensions behind the core rather than building in parallel (risk-register.md R8).

## 8–10 Key Features

The 10 foundational items, most-important-first — no merging or cherry-picking needed to fit the 8–10 cap, since there are exactly 10:

1. **Culprit Agent** — identifies which agent in a multi-agent trace is responsible for a failure
2. **Error Step Localization** — pinpoints the exact step where the failure originated
3. **Verification Agent** — confirms a diagnosis against real trajectory evidence before it's trusted
4. **Repair Agent** — generates a targeted correction for the diagnosed failure
5. **Verified Automatic Repair** — re-executes the corrected trace and reports a measured recovery rate before the fix is trusted
6. **Recovery Controller** — resumes the workflow from the verified repair point instead of restarting *(**Tier 2**: no POC yet; pre-registered Mid-1 gate — LangGraph checkpoint/resume PoC, else re-scoped to replay-based resumption, which Tier 1 already delivers)*
7. **Verified Repair Memory** — retains successful fixes for reuse on similar future failures *(**Tier 2**, honest flag: one real test already run, and it failed — 0/8 commits and a 75%→50% accuracy regression on the free local backbone; pre-registered Mid-1 gate — stronger-backbone re-test on the same 8 cases, else ships as a memory-on/off ablation study)*
8. **Semantic Error Diagnostic** — catches silent failures: outputs that look valid but are semantically wrong, with no error signal
9. **Fault-injection harness** — controlled fault injection across ≥2 multi-agent frameworks for benchmark construction
10. **Cross-architecture benchmark** — the generalization claim itself, proven on frameworks no prior published method or platform has been evaluated against

*The 8 extensions (confidence calibration, preventive clarification classifier, cyclic/dynamic graph support, failure propagation map, explainable confidence reasoning, widened fault taxonomy, a 3rd architecture, and Framework Compatibility Layer — lightweight instrumentation-compatibility across all 7 surveyed frameworks, the scoped answer to "use features of all products, not only from one") are gated behind this core and not part of the capped 8–10 list, matching `FYP_Scope_CCP_and_Implementation_Plan.md` §7.0's full 20-item breakdown (10 foundational + 8 extensions + 2 deprioritized).*

---

**Earlier draft, superseded 2026-08-24, kept for the record:**

> Granite is a deployable SDK and diagnosis platform that identifies why multi-agent AI systems fail, catches failures that look correct but aren't (silent failures with no detectable error signal), and verifies whether a proposed fix would actually work — via deterministic counterfactual re-execution — before it is trusted. The system generalizes across multi-agent architectures (CrewAI, LangGraph, and a third framework) that no prior published method or commercial observability platform has been evaluated against, closing two gaps ErrorProbe (ACL 2026), the strongest published baseline, admits it does not close. Scope is bounded to a fixed, non-negotiable foundational core — a fault-injection harness, a new cross-architecture benchmark, three-stage evidence-grounded failure attribution, silent-failure verification, and verified automatic repair — evaluated against the ErrorProbe baseline, followed by product-facing extensions (confidence calibration, preventive failure warnings, failure-propagation visualization, cyclic-graph support) built only after the core is proven. The deliverable is a full-stack build: a public benchmark, a diagnosis engine, and an installable backend/dashboard — not a single research script.

---

## Complex Computing Problem (Seoul Accord D.4.1)

Full 9-characteristic justification, with tiered-option selections and evidence-based reasoning for each, delivered separately as **`Granite_CCP_Justification.docx`** (same folder). Headline result: **8 of 9 characteristics rated at the top ("Complex") tier**; characteristic #6 (stakeholder involvement) honestly held at the middle tier pending real stakeholder contact — the single highest-priority open item before defense.

---

## Related files in this folder

- `FYP_Scope_CCP_and_Implementation_Plan.md` — the full plan doc, source of truth for the 20-feature breakdown (10 foundational + 8 extensions + 2 deprioritized)
- `Granite_Supervisor_Briefing.pdf` — full supervisor-shareable briefing (12 sections: problem, CCP, RQs, POC, scope, features, use cases, CCP↔feature↔beneficiary map, architecture, feasibility, team, open items)
- `Granite_CCP_Justification.docx` — the Seoul Accord D.4.1 form answers in full
- Published artifact: https://claude.ai/code/artifact/dcdc20b3-8dc5-4bc7-8244-54cac60617f7 — same content as the PDF, web-native
- `../Agentic_AI_Market_Survey_BS_FYP.docx` — second-layer market survey (7 orchestration frameworks), reviewed 2026-08-24; source of the Repair Agent feature addition
- `Agentic_AI_Market_Survey_Full_Content_and_Integration.md` — the survey's full content preserved in markdown, plus a section-by-section audit of exactly where every piece of it landed (or explicitly didn't) in Granite's docs
- `risk-register.md`, `AI_Usage_Log.md`, `architecture-sketch.md`, `Commercial_Product_Comparison.md`, `Silent_Failure_Detection_and_Testing_Strategies.md`, `Guide_Compliance_Audit.md`, `Proposal_Defense_Package.md` — supporting evidence and audits referenced throughout the answers above
