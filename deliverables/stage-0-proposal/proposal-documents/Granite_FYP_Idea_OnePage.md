# The One-Page FYP Idea Description (Official Format)

*Per the FYP Handbook's own required format for floating an FYP idea (Handbook §"Final Year Project Offering", p.9) — the seven items below, in order, no more, no less.*

**1. Title of the project**
Granite — A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery (Project Code: F26-060-Granite). Stream A (research-derived).

**2. Expected level of difficulty / effort involved**
High. ~1,130 plannable person-hours across 3 students over two semesters (490h FYP-1, 640h FYP-2; 3 people × ~15h/week × ~28 weeks), line-by-line budgeted against named work. Checked honestly against the Seoul Accord's 9-point Complex Computing Problem checklist: clears 8 of 9 (the 9th — diverse stakeholder contact — is a stated, open gap, not hidden or faked to inflate the count). Builds on and extends a 2026 ACL Findings paper (ErrorProbe, 59.5% step accuracy — the current best published result) past its own two admitted limitations.

**3. General narrative description of the idea / tasks**
Multi-agent AI systems (teams of collaborating LLM agents — a planner, a researcher, a coder, a verifier) fail often, and when they do, current methods are wrong at least 4 times out of 10 about which agent and step caused it. Worse, every existing method — including the best published one — admits it cannot catch "silent failures": confident, well-formed, plausible-looking answers that are simply wrong, with no crash and no error signal. None has ever been tested on a multi-agent framework it wasn't specifically built and tuned on. Granite is an installable Python SDK and web platform that instruments a target multi-agent workflow (CrewAI or LangGraph), builds a dependency graph of what each agent did, runs a zero-LLM-call constraint verifier that catches silent failures unconditionally, traces backward through the graph to attribute the true culprit agent and step, generates a targeted repair, and — the genuinely new part — actually verifies that repair works via controlled counterfactual replay before anyone trusts it, rather than just proposing a fix and hoping. The system is evaluated both by reproducing the published baseline faithfully and by testing generalization on two frameworks (CrewAI, LangGraph) that none of the 9 papers reviewed in this literature ever used.

**4. References to a few resources**
Who&When (ICML 2025); AgenTracer (ICLR 2026); Scope Delineation Before Localization / SDBL (AAAI 2026); TraceElephant, ErrorProbe, AgentAsk, PROTEA (all ACL 2026 Findings) — 7 directly relevant papers read in full, plus two independent market surveys (7 commercial observability platforms; 7 agent-orchestration frameworks). Data: Who&When (184 real cases, MIT-licensed, in hand); GSM8K and tau-bench retail (task substrates for the project's own fault-injection benchmark, both MIT/CC-BY-licensed and verified against primary sources).

**5. A list of expected deliverables or outcomes**
An installable, framework-agnostic Python SDK; a cross-architecture fault-injection benchmark (500+ traces at Final-2, 15–20% deliberately clean controls); a containerized backend (FastAPI + PostgreSQL) and a 3-screen React dashboard; a full evaluation report against the reproduced baseline with bootstrap confidence intervals and ablation studies; a public, MIT/CC-BY-licensed benchmark release. Already in hand today, at proposal stage: **8 real proof-of-concept spikes, with output on disk**, including two honestly-reported negative results (a preventive classifier that came out near-random, and a repair generator that succeeded on 4 of 6 cases with the 2 failures root-caused).

**6. Any prerequisites or coursework for the project**
Standard BS(CS)/BS(SE) coursework: AI/ML fundamentals, software design and architecture, database systems. No coursework beyond the normal degree track is required; no specialized elective is a prerequisite.

**7. Any special hardware requirement**
None. Committed to a **$0 budget** for the entire project, including the full baseline reproduction and evaluation — every model call runs on a local, free, open-weight LLM (Ollama) on a standard development laptop. A paid-tier alternative was priced from measured token counts (≈$353 recommended / ≈$881 ceiling) and explicitly rejected in favor of the $0 path.
