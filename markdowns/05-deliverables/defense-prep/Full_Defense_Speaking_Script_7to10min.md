# Full Defense Speaking Script — 7 to 10 Minutes

Written strictly from what's actually on each slide right now (checked against the built deck, not an old draft). Read it aloud once at a natural, unhurried pace before the real thing — this is timed to land around **8.5 minutes**, with slack built in on both ends (7 min if you move briskly, 10 min if you pause for emphasis or a slow breath). Time budgets are guides, not a stopwatch to watch mid-sentence.

**Total: ~1,100 words, ~8.5 min at a normal speaking pace (~130 wpm).**

---

## Slide 1 — Title (~20s)

> We're Granite — a self-healing multi-agent AI system for semantic error diagnosis, verified repair, and recovery. When a multi-agent AI system fails — including when the wrong answer looks completely right — no published method can reliably say which agent caused it, and none can verify a fix before trusting it. That's the problem we're solving. I'm Muhammad Noor, with Shahoud Shahid and Saif Shahzad, supervised by Dr. Adil Majeed.

---

## Slide 2 — Problem & Users (~45s)

> Who has this problem? Primarily engineering teams running multi-agent AI systems in or near production, plus downstream product teams and auditors who need traceable evidence. Today, without Granite, the workflow is: capture a trace with tools like LangSmith or Langfuse, have a human guess the root cause with no published accuracy, no check for silent failures, and no way to test a fix before shipping it. The field baseline is just 14.2% step accuracy. The consequence: the system ships a confident, wrong answer — no crash, no error, no signal anything went wrong. This maps to SDG 9 — reliability tooling as a new industrial category.

---

## Slide 3 — Existing Solutions & Prior FYP Comparison (~60s)

> We checked the existing landscape structurally. ErrorProbe, the best published method, gets 59.5% attribution accuracy but admits it can't detect silent failures. Commercial platforms — LangSmith Engine, Arize Alyx, Langfuse, Braintrust — do trace capture and evaluation, but none verify a fix actually works, and most are locked to one stack. We also checked all 660 titles across 12 cohorts since 2019 for a prior departmental FYP — the closest is S24-011, hallucination detection in a single LLM's text, which covers roughly one of our four pipeline stages. The real gap: no system combines attribution, silent-failure detection, verified repair, and cross-architecture generalization in one pipeline. That's what Granite does.

---

## Slide 4 — Research & Technical Basis (~45s)

> Four decisions the literature actually changed. We chose ErrorProbe as our baseline on performance, not recency. We committed to CrewAI and LangGraph — frameworks none of the seven papers we reviewed used. We chose constraint-based diagnosis over an LLM-judge, because LLM-judge approaches only reach 0.65 AUROC — barely above chance. And we rejected narrowing to a single framework, per the market survey's own advice. Across the published lineage, step-level accuracy climbs from 14.2% to just 59.5% — still wrong 40.5 points of the time, and none of these methods can see silent failures at all.

---

## Slide 5 — Complex Computing Challenge (~55s)

> Five characteristics make this a genuine complex computing challenge, not a course project. Conflicting requirements — depth versus latency, privacy versus completeness. No obvious solution — the best published result is 59.5% after 15 months and 7 papers. Depth of knowledge — graph modeling, causal reasoning, tracing. Beyond standard practice — no framework does attribution, detection, and recovery together. And an ill-defined cause — three unknowns stacked: whether a failure happened, which step caused it, and what the correct output should have been.

---

## Slide 6 — Proposed Solution & Contribution (~75s)

> Here's what we're building. The best method is 59.5% but untested on unseen architectures and misses silent failures — we build a cross-architecture benchmark and a diagnosis pipeline with constraint-based silent-failure verification, as a framework-agnostic SDK. Walking the diagram: a target CrewAI or LangGraph system feeds a trace in. Lane A adapts the framework and injects labeled faults into a benchmark store. Lane B normalizes the trace, builds an execution graph, and runs the Semantic Error Diagnostic and Backward Causal Tracer in parallel — unconditionally, not gated on an anomaly. Lane C proposes a repair, verifies it under controlled replay, and serves a dashboard through FastAPI. The LLM API sits outside the boundary on purpose — only 15 to 20% of components ever call it. Tier 2 — Recovery Controller and Verified Repair Memory — is explicitly gated on Mid-1 results, not claimed as delivered yet.

---

## Slide 7 — POC / Feasibility Evidence (~80s)

> This is proof it works, not just an idea. 71.4% agent accuracy and 13.2% step accuracy across 5 real runs — that's a simplified, single-stage reproduction, not directly comparable to ErrorProbe's full 59.5%. Four of six repair attempts succeeded, both failures traced to one fixable cause. And 8 out of 8 spikes have real, recomputable evidence — including an honest negative: our preventive classifier scored near-random, 0.25, and we're reporting that, not hiding it. The headline result is spike 5 — counterfactual replay recovered a corrupted value, 97.2, to the correct 108.0, under a controlled replay protocol. *[Gesture at the screenshot]* And here's the live, clickable prototype behind these numbers.

---

## Slide 8 — Evaluation Plan & Risks (~55s)

> Success and failure are defined before any result exists. We pre-registered an acceptance band — within 10 points of ErrorProbe's 59.5%. We measure agent and step accuracy, silent-failure precision and recall with false-positive rate on clean controls, and latency overhead under 50%. Success bands range from Acceptable — parity on Who&When — up to Exceptional — over 50% verified-repair recovery. Every top risk already has a stated fallback: missing the acceptance band means we report both numbers, not hide one; if the Tier-2 gates fail at Mid-1, Tier 1 alone still delivers the core contribution. And nothing we claim sits in core-replacement — the LLM is core-assist only.

---

## Slide 9 — Work Division & Iteration Plan (~45s)

> Scope is split three ways, each with a stated "if removed" consequence. Shahoud owns Data and Benchmark — framework instrumentation and fault injection; without it, there's no cross-architecture benchmark to test against. I own Diagnosis — the graph, the ErrorProbe reproduction, and the Semantic Error Diagnostic; without it, there's no attribution and no contribution. Saif owns Platform — replay, the SDK, FastAPI, Postgres, deployment; without it, nothing is installable outside our machines. Five milestones carry us from scope-locked through full evaluation across FYP-1 and FYP-2.

---

## Slide 10 — DEI, Ethics & Legal (~25s)

> Three commitments the panel can hold us to. DEI: open-source release, accessible color-and-text design, English-only claims stated honestly. Ethical: every repair is human-gated, advisory only, and negative results — like Spike 7 — are published, not buried. Legal: every dataset we use is MIT-licensed and verified against its actual LICENSE file, and AI usage is logged and disclosed every session.

---

## Delivery notes

- **Practice with a timer once** before assuming 8.5 min holds — reading speed varies person to person; adjust the 3 longest slides (6, 7, 3) first if you're over.
- **Slides 6 and 7 carry the most weight** — architecture and evidence are what a panel probes hardest. If you're short on time elsewhere, don't cut these; trim slide 4 or 10 instead.
- For deeper Q&A beyond this script, use `CCP_and_Spikes_Full_Reasoning.md` and `Literature_Review_Panel_Narrative.md` in this same folder.
