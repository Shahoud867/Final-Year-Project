# Supervisor Briefing — Granite

*A plain-language brief for the supervisor meeting. Full technical detail lives in [FYP_Scope_CCP_and_Implementation_Plan.md](../01-planning-and-scope/FYP_Scope_CCP_and_Implementation_Plan.md) and its supporting files — this is the condensed version to actually talk from.*

---

## 1. The one-minute version

Multi-agent AI systems (several LLM "agents" cooperating on a task — a planner, a researcher, a writer, etc.) fail often, and when they do, figuring out *which* agent caused it and *why* is still an open research problem. The strongest published method as of today (ErrorProbe, ACL 2026) only gets it right about 6 times out of 10 at best, admits it misses failures that "look fine but aren't," and has never been tested on an agent framework it wasn't specifically built and tuned for.

We're building a system that picks up where that leaves off: attribute the failure, trace *how* it spread through the other agents, catch the failures that leave no obvious error signal, and test whether a proposed fix would actually work — packaged as an installable tool a real team could point at their own system, not just a benchmark result in a paper.

---

## 2. What we found (the literature gap)

We read seven directly relevant papers in full (not abstracts) — Who&When (ICML 2025), AgenTracer (ICLR 2026), Scope Delineation Before Localization (AAAI 2026), TraceElephant, ErrorProbe, AgentAsk, and PROTEA (all ACL 2026) — spanning the entire recent history of this problem.

**The progression is real and verifiable:** Who&When's original baseline got 14.2% step-level accuracy (i.e., correctly identifying *which step* caused the failure). ErrorProbe, the current best, reaches 59.5% on the same benchmark. That's real progress — and still means it's wrong more than 4 times out of 10.

**What even the best current method (ErrorProbe) admits it can't do, in its own words:**
- Can't catch "silent failures" — outputs that look technically fine but are semantically wrong, because its whole pipeline only activates when something looks obviously anomalous.
- Has only ever been tested on the specific agent frameworks its own benchmark was built from (CaptainAgent, MagenticOne, and AgenTracer's 6-framework set) — never on an architecture outside that set.
- Finds *who* caused a failure, but never reconstructs *how* the mistake spread through the other agents downstream, and never tests whether a specific fix would have actually worked.

We confirmed, after reading all seven papers cover to cover, that none of them do propagation-path reconstruction with a real metric, or systematic "test the fix before you ship it" replay, or genuine testing on an unseen architecture. That's the gap.

---

## 3. Exactly what gap we're solving (one sentence for the supervisor)

> Detecting and explaining **why and how** a multi-agent AI system failed — including failures that leave no obvious error trace — and testing whether a specific fix would actually have worked, in a way that isn't limited to the specific agent frameworks it was built and tested on.

---

## 4. How it's feasible

- **Data is free and legally clear.** The two core benchmarks we build on are permissively licensed — Who&When is MIT, AgenTracer's TracerTraj is Apache 2.0 (both confirmed directly in-paper) — so there's no licensing risk, unlike some other candidate FYP ideas we looked at.
- **No need to train a large model from scratch.** The system runs on existing LLM APIs for agent behavior and reasoning; the one place we train anything of our own is a small, optional classifier that runs on a laptop or a free cloud notebook.
- **A real, working starting point already exists.** AgenTracer ships public code and a public, working 8B model — we can clone and run it in days, not weeks. That de-risks the proposal-stage proof-of-concept significantly.
- **Team fit is clean.** Three independently ownable subsystems map to three people: (1) benchmark/fault-injection engineering, (2) the diagnosis engine, (3) the recovery engine and deployable platform. Each is a defensible, demoable piece on its own — if any one person were removed, a real, distinct piece of the contribution disappears with them.
- **The two-semester plan is already mapped to all five official evaluation gates** (proposal defense, Mid-1, Final-1, Mid-2, Final-2), with a proof-of-concept (three small, specific test runs) plannable before the defense itself.

**Honest open items, not hidden:** the proof-of-concept hasn't been run yet, real stakeholders haven't been contacted yet, and we're actively double-checking whether any brand-new paper published in the last few weeks might already close part of the gap — this field moves roughly every 2–3 months, so that check is a standing routine, not a one-time thing.

---

## 5. Resources that support it

| Need | What we use | Cost/access |
|---|---|---|
| Core benchmarks | Who&When (MIT), TracerTraj/AgenTracer (Apache 2.0) | Free, public |
| Task sources for our own new benchmark | GAIA, MBPP+, GSM8K, MATH, tau-bench (retail) | Free, public, all downloaded and license-verified, 2026-08-22 |
| Frameworks to test generalization on | CrewAI, LangGraph — neither used by any of the seven papers | Free, open-source |
| Compute | LLM API calls (no local GPU training required for the core system) | Main budget line — sized once we have real per-call cost data from the POC |
| Deployment | Single containerized deployment (Docker) on a cloud VM or on-prem | Free/student tiers of major cloud providers are normally sufficient |
| Dev tooling | Python, a graph library, a backend API framework, GitHub Actions for CI | Free/open-source |

Nothing here requires paid infrastructure beyond ordinary LLM API usage.

---

## 6. What product comes out of this

Not just a benchmark number in a report — an installable SDK and backend service a real engineering team could point at their own multi-agent system: it captures execution traces, builds a dependency graph, flags likely failures (including the silent ones), explains how the error propagated between agents, tests whether a proposed fix would work, and reports all of it through a minimal dashboard. It runs in a container, outside the development machine, which is what the department requires — deployable, not just demoed locally.

Positioning: not a competitor to existing agent-observability platforms (LangSmith, Langfuse, and similar) — those already do trace capture and manual inspection well. This sits as a **diagnosis layer on top of that category** — the part where a human currently has to read the trace and guess; none of those platforms currently do automated root-cause attribution, silent-failure detection, or "test the fix before shipping it."

---

## 7. Who this is for, and what each feature is worth to them

| Feature (short) | What it does | Impact | Who specifically needs it |
|---|---|---|---|
| **Failure attribution** | Identifies which agent and which step caused a failure | Cuts manual debugging time — no more reading hundred-step logs by hand | Any team running a multi-agent pipeline in development or production |
| **Silent-failure detection** | Catches outputs that look fine but are actually wrong, with no obvious error signal | Prevents a wrong-but-plausible answer from silently reaching a real user | Teams in higher-stakes settings — customer-facing agents, coding agents that ship code, anything an end user trusts without double-checking |
| **Propagation-path reconstruction** | Shows *how* the original mistake spread through the other agents, not just where it started | Turns "something failed" into an explanation a human can actually act on | Engineers doing root-cause postmortems after an incident |
| **Counterfactual recovery testing** | Tests whether a proposed fix would actually have worked, before it's shipped | Removes the guesswork from "did that fix actually help" | Teams iterating on agent prompts, tools, or pipeline design |
| **Cross-architecture generalization** | Works on agent frameworks it wasn't specifically built or tuned for | Usable in the real world, not just on the exact frameworks used in academic papers | Any team not using precisely the same setup as the published research — i.e., almost everyone |
| **Deployable SDK** | Installable, runs against a team's real system, not just a fixed benchmark | Makes this a tool people can actually adopt, not just a paper result | Any engineering team evaluating or maintaining a multi-agent system |

---

## 8. Quick answers to likely supervisor questions

- **"Why this and not just a copy of an existing paper?"** — Because building a diagnosis engine that only matches one paper's published numbers is the "Developing" tier of ambition, not the committed one. We build our own attribution algorithm on ErrorProbe's published method, then extend it past its own admitted limits (silent failures, unseen architectures) into a real deployable product — the extension is what we're actually shipping, stated precisely enough that a panel can test whether we achieved it.
- **"Is this too big for one year?"** — No — the committed core is scoped to what three people can build and evaluate in two semesters, with everything beyond that explicitly labeled as an optional extension, gated behind the core being done first.
- **"What if someone publishes the exact same idea before we finish?"** — Real risk in a fast-moving field, tracked openly in our risk register, checked at every project gate. If it happens, we report it honestly as a finding — the benchmark and the deployable tool we build remain valuable either way, since neither is something a single competing paper is likely to fully replace.
- **"What's the actual proof this is feasible, not just planned?"** — Four small proof-of-concept runs before the defense: our diagnosis engine's attribution logic hitting real (if partial) accuracy on a small slice of Who&When, one toy workflow instrumented in a framework nobody else has tested on, one injected failure producing clean recoverable ground truth, and the silent-failure detector catching known-wrong values with zero false positives.
