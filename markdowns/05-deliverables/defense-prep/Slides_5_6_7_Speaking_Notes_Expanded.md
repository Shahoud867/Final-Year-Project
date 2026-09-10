# Slides 5, 6, 7 — Expanded Speaking Notes

**How to use this file:** each slide below has your **original script** (unchanged, exactly as it was in the deck's speaker notes) followed by **added coverage** — the extra points needed so every visible box, lane, and number on the slide has something you can say about it. Read the original first; the additions slot in around it, they don't replace it.

---

## Slide 5 — Complex Computing Challenge

### Original script
> This is the slide the panel uses to decide whether the project deserves capstone status. Concede up front that a trace-capture-plus-LLM-guess wrapper is a weekend's work, then name precisely what such a version would get wrong: no benchmark on unseen architectures, no way to tell a silent failure from a correct answer, no measured false-positive rate on clean controls, no evidence its fix works.

**Update:** the diagram is gone, and the grid now shows only the **5 strongest characteristics**, renumbered 1–5 with no gaps, laid out as full-width elegant rows (same style as slide 10). Badge 5 (Ill-defined cause) has three stacked unknowns — read its resolution aloud if pressed: whether/which/what's-correct, each resolved by a distinct pipeline stage (see `CCP_and_Spikes_Full_Reasoning.md`).

### Added coverage (all 5 boxes, badge order as on the slide)
- **Badge 1 — Conflicting requirements:** depth vs. latency is deeper graph/causal reasoning costing time a real-time repair loop can't always afford; privacy vs. completeness is capturing enough trace detail to diagnose correctly while not persisting data the operator doesn't want logged. Both are named trade-offs with a stated resolution, not hand-waved.
- **Badge 2 — No obvious solution:** say the number aloud — 59.5% is the best published step accuracy after 15 months and 7 papers of dedicated research. That absence of a known recipe is the whole justification for research-level effort.
- **Badge 3 — Depth of knowledge:** the diagnosis engine sits on graph algorithms (execution-graph construction), causal inference (backward causal tracing), and distributed-tracing concepts — not single-course material.
- **Badge 4 — Beyond standard practice:** no framework reviewed — academic or the 7 commercial platforms checked — combines attribution, general silent-failure detection, and verified repair together.
- **Badge 5 — Ill-defined cause:** covered above.

**Held back (not on-slide):** Unfamiliar issues, Diverse stakeholders, Significant consequences, Interdependence — none are weaker, they just aren't the 5 printed. Cover any of them only if asked; ready answers for each are in `CCP_and_Spikes_Full_Reasoning.md`.

Full reasoning and likely panel questions for all 9 (5 on-slide + 4 held back) are in `CCP_and_Spikes_Full_Reasoning.md` below.

---

## Slide 6 — Proposed Solution & Contribution

### Original script
> Say unprompted: 'controlled, not deterministic' — the replay protocol is deterministic, LLM-step variance is measured over N replays, never assumed away. Say unprompted: the Semantic Error Diagnostic abstains where no checkable constraint exists, and the abstention rate is reported as a metric, not hidden.
>
> If asked about scope: in scope is 10 committed mechanisms; out of scope is message queues, Kubernetes, full RBAC, DR infra, multi-tenant billing; deployment target is Docker + a pip-installable SDK, operable by someone who didn't build it.

### Added coverage (walk the diagram once, lane by lane, before questions)
- **Actors:** the Target System (CrewAI/LangGraph workflow) feeds a raw execution trace in; the Operator installs the SDK against it and later views the dashboard.
- **Lane A — Data/Benchmark:** Framework Adapters normalize CrewAI/LangGraph hooks → Fault Injection Operators inject labeled faults deterministically at 0% API cost → Benchmark Store persists traces plus ground truth.
- **Lane B — Diagnosis:** Trace Normalizer standardizes the schema → Execution Graph Builder turns it into a graph at 0% API → Semantic Error Diagnostic and Backward Causal Tracer run **in parallel, unconditionally** (not gated on an anomaly — this is the headline contribution).
- **Lane C — Platform:** Repair Agent proposes one atomic fix → Verified Automatic Repair checks it under controlled replay → FastAPI Backend serves the Dashboard.
- **LLM API box:** sits *outside* the system boundary on purpose — only ~15-20% of components ever call it, everything else is deterministic. That's the "core-assist" claim, made visible, not just asserted.
- **Tier 2 note** (Recovery Controller + Verified Repair Memory): explicitly gated on Mid-1 criteria, not claimed as delivered. Say so if the panel points at it.

---

## Slide 7 — POC / Feasibility Evidence

### Original script
> Lead with Spike 7's negative result and Spike 8's failure analysis — quote the guide's own words directly: a POC that disproved an assumption is more valuable than one that confirmed it. Every number on this slide is real and recomputable from files in the repository; offer to open one.
>
> In progress: full 3-stage reproduction, top FYP-1 priority. Planned: Recovery Controller + Verified Repair Memory Tier-2 gates, pre-registered Mid-1 criteria, not yet run. Prototype: 5 screens, mocked backend, dist-static/index.html.

### Added coverage
- **The 4 headline numbers:** 71.4% agent accuracy and 13.2% step accuracy are our **simplified single-stage** reproduction over 5 runs — not directly comparable to ErrorProbe's full 3-stage 59.5%, say so unprompted before a panelist notices the gap themselves. 4/6 is the Repair Agent's real success rate, both failures traced to one fixable cause. 8/8 means every spike has real, recomputable evidence, including the honest negative.
- **Spikes 1-6, one breath each, if asked:**
  1. ErrorProbe reproduction confirms the mechanism direction even simplified.
  2. CrewAI instrumentation proves a real 3-node execution graph was captured.
  3. Fault injection landed a labeled fault, with one self-correction kept as a finding, not hidden.
  4. Semantic Error Diagnostic caught a real near-miss ($20.00 vs $19.75) with zero false positives.
  5. Counterfactual replay is the **core novelty claim** — a corrupted 97.2 recovered to 108.0 under controlled replay.
  6. Cyclic graph handling hit its 10,000-step safety cap as designed, proving the failure mode is contained, not silent.

**Update:** the Operator Workflow diagram was removed from this slide (it repeated logic already on slide 5) — the prototype screenshot now spans the full slide width instead. If asked about the human-approval workflow, it's a verbal answer: install, review the diagnosis before anything is applied, approve or reject, then a verified replay confirms the fix actually worked. Nothing here is autonomous.
