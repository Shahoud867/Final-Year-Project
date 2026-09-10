# CCP, Spikes & Contribution — Full Panel-Defense Reasoning

This is the deep version behind slides 5, 6 and 7 — not what's on the slide, but the reasoning underneath it, written so you can answer a follow-up question the slide itself doesn't spell out. Organized as: statement → why it's true → likely panel question → model answer.

---

## Part 1 — CCP characteristics (5 on-slide + 4 held back)

**Numbering note:** headings below follow the on-slide badge order (1–5) exactly as it now appears on slide 5 — the 5 strongest, most classic CCP arguments. Badges 1–5 line up with real characteristics 1, 2, 3, 5, 9 respectively (noted per section). The other 4 real characteristics (4, 6, 7, 8) are held back in full below the on-slide five — not weaker arguments, just not the ones printed, so ready if a panelist asks about any of them.

### 1. Conflicting requirements
**Why it's true:** Two real trade-offs, not one. (a) Depth vs. latency — deeper causal/graph reasoning gives better attribution but costs time a production repair loop can't always spend. (b) Privacy vs. completeness — diagnosing well needs a rich trace, but the operator may not want every field of that trace persisted or logged.

**Likely question:** *"How do you actually resolve privacy vs. completeness — isn't that just a trade-off you're leaving unsolved?"*
**Model answer:** "We don't claim to resolve it universally — we make it a configurable boundary, not a hidden default. The SDK captures what's needed for attribution (agent id, step, inputs/outputs relevant to the constraint being checked), and what gets persisted to the Benchmark Store vs. discarded after diagnosis is an operator-set policy, not baked into the pipeline. The trade-off is real and stays visible — that's the design decision, not a silent compromise."

**Likely question:** *"And depth vs. latency — what's your actual answer?"*
**Model answer:** "Our NFR target is under 50% latency overhead versus the uninstrumented baseline. Where deeper causal tracing would blow that budget, the Semantic Error Diagnostic is deliberately the fast, 0%-API, deterministic path that runs unconditionally — the heavier LLM-based verification (Investigator stage) only runs when the cheap check can't resolve it. That's the actual trade-off resolution: cheap-first, escalate-only-when-needed."

---

### 2. No obvious solution
**Why it's true:** Best published step-level accuracy is 59.5% (ErrorProbe), after 15 months and 7 papers across ICML/ICLR/AAAI/ACL. If there were an obvious solution, someone in that lineage would already have it.

**Likely question:** *"Why should a proposal-stage FYP succeed where 7 papers didn't?"*
**Model answer:** "We're not claiming to out-attribute ErrorProbe — we adopt its algorithm as our baseline. The contribution is the three things none of those 7 papers do together: general silent-failure detection (not anomaly-gated), verified counterfactual repair, and cross-architecture generalization to frameworks none of them tested. We're not solving attribution better; we're solving the combination none of them attempted."

---

### 3. Depth of knowledge
**Why it's true:** Requires graph modeling (execution-graph construction), causal reasoning (backward causal tracing to localize root cause), and distributed-systems tracing concepts — a genuine cross-topic synthesis, not one course's syllabus.

**Likely question:** *"Isn't this just calling an LLM API — where's the depth?"*
**Model answer:** "The LLM is core-assist only — 15-20% of components. The actual attribution logic (Culprit Agent, Error Step Localization) runs on graph features at 0% API cost. The depth is in the graph construction, the causal-tracing algorithm, and the constraint-verification logic in the Semantic Error Diagnostic — none of that is an LLM call."

---

### 4. Beyond standard practice *(real characteristic 5)*
**Why it's true:** No existing framework — academic or the 7 commercial platforms checked (LangSmith, Langfuse, Braintrust, Arize, Maxim, Opik, DeepEval) — combines step-level attribution, general silent-failure detection, and verified counterfactual repair in one evaluated pipeline.

**Likely question:** *"Arize/LangSmith already do RCA — what's actually new?"*
**Model answer:** "They do parts of this — trace capture, evaluation, some RCA. None of them, per our own literature and market check, do all three together: attribution + general silent-failure detection (not just RAG-groundedness) + verified repair with a measured recovery rate. That combination, evaluated as one pipeline, is the gap — not any single piece of it."

---

### 5. Ill-defined cause *(real characteristic 9)*
**Why it's true:** Three unknowns stacked together — *whether* a failure happened at all (silent failures give no signal), *which* step caused it, and *what* the correct output should have been. None of the three is given.

**Likely question:** *"How can you claim to solve an 'ill-defined' problem — doesn't that mean it's unsolvable?"*
**Model answer:** "Ill-defined doesn't mean unsolvable — it means each unknown needs its own resolution, which is exactly the pipeline: the Semantic Error Diagnostic resolves *whether* (via constraint verification, abstaining when it can't tell — the abstention rate is reported, not hidden); the Backward Causal Tracer resolves *which* step; and the Repair Agent's proposed correction, verified by replay, resolves *what* the correct output should have been. Three unknowns, three distinct mechanisms, each measured separately."

---

### Held back — 4 characteristics not on the slide

These are real, argued in `Granite_CCP_Justification_Seoul_Accord.docx`, and not weaker — they just aren't the 5 printed on slide 5. Cover any of them if asked directly.

**Unfamiliar issues** *(real characteristic 4)* — Delayed errors (a silent failure can surface steps later), non-determinism (identical inputs can produce different agent traces), and cross-architecture generalization (CrewAI and LangGraph are structurally different) — none of these are issues a standard course project has to confront.
*If asked about non-determinism:* "We don't assume it away — we measure it. The Verified Automatic Repair protocol is deterministic in its own steps (frozen upstream context, pinned decoding parameters), and LLM-step variance is measured over N replays rather than a single point estimate — exactly what Spike 5 demonstrates."

**Diverse stakeholders** *(real characteristic 6 — the weakest of the 9)* — the other named stakeholders (engineering team, downstream product teams, auditors) are supported by literature + a 7-vendor survey, but live contact with a real stakeholder is only scheduled for Mid-2.
*If asked:* "It's real, just not shown — we don't have a working system to show a stakeholder yet. It's scheduled for Mid-2, when there's something real to react to."

**Significant consequences** *(real characteristic 7)* — a missed silent failure isn't a crash — it's a confidently wrong output a downstream system or person acts on, undetected.
*If asked for a concrete example:* "The near-miss from our mechanism test: a stated $20.00 against a true $19.75. In a real refund or billing pipeline, that's money moving on a wrong number with no crash, no exception, no log line flagging it."
*If they press on where that number comes from — answer it straight:* it is from the **seeded** mechanism test (`dev/spikes/poc/poc_spike4b_mechanism_output.json`), which feeds known-wrong values directly to the rule-based checker. It is **not** from the live n=3 run — that run produced zero natural silent failures, so recall in the wild is unmeasured. Say this before they find it; the distinction is the whole credibility of the claim.

**Interdependence** *(real characteristic 8 — the "dependency" question)* — agents in a workflow pass state to each other; an error in one agent's output can corrupt every downstream agent's reasoning.
*If asked how a dependency is actually shown:* "The execution graph is the proof — nodes are actions, edges are dependencies, built directly from the real trace, not inferred. The Backward Causal Tracer walks those edges backward from the visible symptom to find where the error originated. Spike 2 demonstrates this concretely: a real 3-node graph with 2 clean edges captured from an actual CrewAI run."

---

## Part 2 — All 8 spikes, full reasoning

| # | Spike | Why it matters beyond the one-line result |
|---|---|---|
| 1 | ErrorProbe reproduction (simplified) | Proves the mechanism *direction* is right even at 1-stage instead of ErrorProbe's full 3-stage — the range (62.5–85.7% agent, 0–25% step) across 5 real runs is reported honestly as a range, not cherry-picked. |
| 2 | CrewAI instrumentation | Proves trace capture actually works on a real framework, not a mock — 3 real nodes, 2 clean edges, from an actual run. |
| 3/3b | Fault injection | Proves we can deterministically inject a labeled fault — the ground truth *is* the injection operator, so no manual annotation cost (this is the AgenTracer idea we reuse). One case self-corrected; kept and reported as a finding, not hidden, because it's evidence the system doesn't always behave as expected and we say so. |
| 4 / 4b | Semantic Error Diagnostic | The headline mechanism, and the one to state in two halves. **Live n=3 run (spike 4):** the model got all three tasks right, so there were zero natural silent failures — `detector_recall_on_silent_failures: null`, unmeasured, with zero false positives. **Seeded mechanism test (spike 4b):** 3 of 3 known-wrong values caught, including the $20.00-vs-$19.75 near-miss that a "close enough" check would wave through, and 0 of 3 correct values flagged — including one differing only by legitimate rounding. The mechanism works; its hit rate on natural failures does not yet have a number. Volunteering that split is stronger than being caught by it. |
| 5 | Controlled counterfactual replay | The **core novelty claim** — a corrupted value (97.2) recovered to the correct value (108.0) under a controlled replay protocol, with `recovery_success = true` recomputable from the repo. This is the one no other reviewed method demonstrates. |
| 6 | Cyclic graph handling | Proves failure containment, not silent hangs — disabling cyclic support correctly hits the 10,000-step safety cap rather than looping forever undetected. |
| 7 | Preventive classifier | The **honest negative** — precision/recall/F1 = 0.25, near-random. Reported because the handbook's own guidance says a POC that disproves an assumption is more valuable than one that confirms it. This is the strongest credibility signal on the whole slide — it shows we test our own assumptions and report failure. |
| 8 | Repair Agent | 4/6 real success rate; both failures traced to one shared, fixable cause (not two unrelated bugs) — proves the failure mode is understood, not mysterious. |

**If asked "why include a failed spike (7) at all":** quote the guide directly — a POC that disproves an assumption is more valuable than one that confirms it. Spike 7 tells us *not* to rely on a preventive classifier and to invest in the reactive Semantic Error Diagnostic instead — that's a real design decision the negative result produced.

---

## Part 3 — Proposed Solution & Contribution (slide 6) reasoning

**Why ErrorProbe as the baseline, not the newest paper:** chosen on performance (59.5%, beats both its ancestors on their own benchmarks), not recency — it isn't even the newest of the four ACL 2026 papers reviewed.

**Why CrewAI + LangGraph specifically:** neither framework was used by any of the 7 papers reviewed. That's the actual generalization test — none of the literature tests transfer to an architecture unseen during benchmark construction; committing to two frameworks nobody else tested is the point, not a convenience choice.

**Why constraint-based Semantic Error Diagnostic, not an LLM-judge:** literature shows LLM-judge approaches cap out at AUROC ≤ 0.65 — barely above chance. A deterministic, rule/schema-based check is both cheaper (0% API) and more reliable for the specific failure mode (semantically wrong but structurally valid output) than another LLM judging an LLM.

**Why the LLM is core-assist only (15-20%):** the swap test — if the LLM API were replaced, the contribution (graph-based attribution, constraint verification, replay-based repair verification) survives. Only the Investigator-stage verification and repair-candidate generation actually call it.

**Why Docker + pip-installable SDK as the deployment target:** operability by someone who didn't build it is the actual bar — a system only the authors can run isn't a deliverable, it's a demo.

**Why Tier 2 (Recovery Controller / Verified Repair Memory) is explicitly gated:** these depend on Mid-1 reproduction results; committing to them unconditionally before that gate would be promising something not yet earned. The gate structure is the honest way to commit scope without overpromising.
