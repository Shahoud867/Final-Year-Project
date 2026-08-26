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

- **Data is free and legally clear — with one correction we made ourselves.** Who&When is MIT-licensed and fully in hand (184 real cases, downloaded and verified). We originally wrote that AgenTracer's TracerTraj was "Apache 2.0, confirmed in-paper" — **that was wrong, and we found it by trying to download the data rather than by re-reading the citation.** TracerTraj-2.5K is not actually released: no LICENSE file exists, the repo says data will be released "upon acceptance," and only a 127-row sample is real. The reproduction plan now rests on Who&When alone, and the TracerTraj comparison is downgraded from committed to conditional (risk-register R11).
- **No need to train a large model from scratch.** The system runs on existing LLM APIs for agent behavior and reasoning; the one place we train anything of our own is a small, optional classifier that runs on a laptop or a free cloud notebook.
- **The cost is now a real number, not a hope.** Measured from token counts across all 184 real Who&When cases: **≈ $353 for the whole project, ≈ $881 worst case** (cost-estimate.md). All eight proof-of-concept spikes so far cost **$0**, run on a free local model. We also tried AgenTracer's own generation pipeline to build extra data and **abandoned it after a real pilot run** — one task took 10+ minutes on the local model, extrapolating to days of continuous compute (R11b). Recorded as a tested dead end, not left as an assumption.
- **Team fit is clean, and now assigned.** Three independently ownable subsystems map to three named people: **Shahoud Shahid** — benchmark/fault-injection engineering; **Muhammad Noor** — the diagnosis engine; **Saif Shahzad** — the recovery engine and deployable platform. Each is a defensible, demoable piece on its own — remove any one person and a real, distinct piece of the contribution disappears with them.
- **The two-semester plan is already mapped to all five official evaluation gates** (proposal defense, Mid-1, Final-1, Mid-2, Final-2), and the proof-of-concept is **done, not planned** — see below.

**Honest open items, not hidden:** real stakeholders still haven't been contacted (the single highest-priority item before the defense, and the one thing no document can close for us); two committed features — resuming from a checkpoint, and remembering successful repairs — carry the weakest evidence, so both now sit behind written pass/fail gates at Mid-1 with a recorded fallback each, rather than an assurance; and we're actively re-checking whether any brand-new paper closes part of the gap — this field moves roughly every 2–3 months, so that check is a standing routine at every gate, not a one-time thing.

---

## 5. Resources that support it

| Need | What we use | Cost/access |
|---|---|---|
| Core benchmark | **Who&When (MIT)** — 184 cases, downloaded and in hand | Free, public |
| ~~TracerTraj / AgenTracer~~ | **Corrected:** not actually released — only a 127-row sample is real (R11) | Conditional, not committed |
| Task sources for our own new benchmark — **active** | **GSM8K + tau-bench retail** (narrowed from five candidates to two) | Free, public, licenses verified against primary sources |
| Task sources — benched, not built against | MBPP+, MATH, GAIA | Downloaded; **GAIA is access-gated and must not be redistributed** — flagged before the repo goes public (dev/datasets/DOWNLOAD.md) |
| Frameworks to test generalization on | CrewAI, LangGraph — neither used by any of the seven papers | Free, open-source |
| Compute | LLM API calls (no local GPU training required for the core system) | **Sized: ≈ $353 recommended, ≈ $881 ceiling** — measured, not projected (cost-estimate.md) |
| Deployment | Single containerized deployment (Docker) on a cloud VM or on-prem | Free/student tiers of major cloud providers are normally sufficient |
| Dev tooling | Python, a graph library, a backend API framework, GitHub Actions for CI | Free/open-source |

Nothing here requires paid infrastructure beyond ordinary LLM API usage.

---

## 6. What product comes out of this

Not just a benchmark number in a report — an installable SDK and backend service a real engineering team could point at their own multi-agent system: it captures execution traces, builds a dependency graph, flags likely failures (including the silent ones), explains how the error propagated between agents, tests whether a proposed fix would work, and reports all of it through a minimal dashboard. It runs in a container, outside the development machine, which is what the department requires — deployable, not just demoed locally.

Positioning: not a competitor to existing agent-observability platforms (LangSmith, Langfuse, and similar) — those already do trace capture and manual inspection well. This sits as a **diagnosis layer on top of that category** — the part where a human currently has to read the trace and guess.

**Correction we made ourselves, 2026-08-22 (R9):** an earlier version of this paragraph said "none of those platforms currently do automated root-cause attribution." Checking the vendors directly rather than trusting that assumption proved it stale — **LangSmith Engine and Arize's Alyx (both 2026) do claim automated root-cause diagnosis and fix drafting.** The differentiation is narrower than we first wrote, and it is this: none of them documents **step-level attribution accuracy on any benchmark**, general (non-RAG-specific) silent-failure detection, or counterfactual fix-testing with a **measured recovery rate** — and all are locked to their own tracing stack, whereas ours is framework-agnostic and its numbers are published on a public benchmark. We corrected our own positioning rather than waiting for a panel to correct it.

---

## 7. Who this is for, and what each feature is worth to them

| Feature (short) | What it does | Impact | Who specifically needs it |
|---|---|---|---|
| **Failure attribution** | Identifies which agent and which step caused a failure | Cuts manual debugging time — no more reading hundred-step logs by hand | Any team running a multi-agent pipeline in development or production |
| **Silent-failure detection** | Catches outputs that look fine but are actually wrong, with no obvious error signal | Prevents a wrong-but-plausible answer from silently reaching a real user | Teams in higher-stakes settings — customer-facing agents, coding agents that ship code, anything an end user trusts without double-checking |
| **Propagation-path reconstruction** | Shows *how* the original mistake spread through the other agents, not just where it started | Turns "something failed" into an explanation a human can actually act on | Engineers doing root-cause postmortems after an incident |
| **Controlled counterfactual recovery testing** | Re-runs the workflow with a proposed fix in place — frozen upstream context, pinned settings — and reports a **measured** recovery rate before the fix is shipped | Removes the guesswork from "did that fix actually help" | Teams iterating on agent prompts, tools, or pipeline design |
| **Cross-architecture generalization** | Works on agent frameworks it wasn't specifically built or tuned for | Usable in the real world, not just on the exact frameworks used in academic papers | Any team not using precisely the same setup as the published research — i.e., almost everyone |
| **Deployable SDK** | Installable, runs against a team's real system, not just a fixed benchmark | Makes this a tool people can actually adopt, not just a paper result | Any engineering team evaluating or maintaining a multi-agent system |

---

## 8. Quick answers to likely supervisor questions

- **"Why this and not just a copy of an existing paper?"** — Because building a diagnosis engine that only matches one paper's published numbers is the "Developing" tier of ambition, not the committed one. We build our own attribution algorithm on ErrorProbe's published method, then extend it past its own admitted limits (silent failures, unseen architectures) into a real deployable product — the extension is what we're actually shipping, stated precisely enough that a panel can test whether we achieved it.
- **"Is this too big for one year?"** — No — the committed core is scoped to what three people can build and evaluate in two semesters, with everything beyond that explicitly labeled as an optional extension, gated behind the core being done first.
- **"What if someone publishes the exact same idea before we finish?"** — Real risk in a fast-moving field, tracked openly in our risk register, checked at every project gate. If it happens, we report it honestly as a finding — the benchmark and the deployable tool we build remain valuable either way, since neither is something a single competing paper is likely to fully replace.
- **"What's the actual proof this is feasible, not just planned?"** — **Eight proof-of-concept runs, already done, with real output on disk** (the department requires one). Attribution logic hitting agent 62.5-85.7% / step 0-25% accuracy (means 71%/13%) across 5 independent runs on a real Who&When slice — reported as a range because run-to-run LLM variance at n=8 is real, not hidden behind one favorable run; a toy workflow instrumented in a framework nobody else has tested on; an injected failure producing clean recoverable ground truth; the silent-failure detector catching known-wrong values — including a plausible near-miss ($20.00 vs $19.75) — with zero false positives; a corrupted trace recovered from 97.2 back to 108.0 by replay; cyclic graphs terminating under a bound, with a control run proving the bound is load-bearing; a preventive classifier that came out **near-random (0.25)**; and a repair generator succeeding **4 out of 6**. The last two are negative or partial results and we lead with them — a spike that disproves an assumption is worth more than one that confirms what we already believed.
- **"Which of your committed features is weakest?"** — Two, named without being asked: **Recovery Controller** has no proof-of-concept at all, and **Verified Repair Memory** has exactly one real test, which **failed** (0 of 8 cases committed anything to memory, and accuracy regressed 75%→50% on a free 3B model). Both stay committed, but each now carries a written pass/fail gate at Mid-1 with a recorded fallback, decided *before* the results exist. If the memory re-test fails again, it ships as a memory-on/memory-off comparison study — which is still a legitimate evaluation contribution, not a quietly dropped feature.
