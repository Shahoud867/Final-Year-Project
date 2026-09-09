# CCP Characteristics Not Shown on Slide 5

**Why this file exists:** slide 5 of `Granite_Proposal_Defense_v2.pptx` used to show all 9 Complex Computing Problem (Seoul Accord / OBE) characteristics. The slide now shows only characteristics **1, 2, 3, 6, 7, and 9** — the six the presenter's speaker notes actually name and plan to talk through live. Diagram 4 (Core Technical/Computational Pipeline) from the Architecture Atlas occupies the space the other 3 boxes used to fill.

Dropping a characteristic from the slide does **not** mean it isn't real or isn't argued — all 9 are still fully justified in `Granite_CCP_Justification_Seoul_Accord.docx` in this same folder. This file is the short, spoken-language version of the 3 that are off-slide, so the team has something to say if a panelist asks about one of them directly.

---

### 4 — Unfamiliar issues
**Delayed errors, non-determinism, cross-architecture generalization.** A silent failure by definition doesn't announce itself when it happens — it can surface steps later. LLM-based agents are non-deterministic, so identical inputs can produce different traces. And a method has to generalize across CrewAI and LangGraph, two structurally different frameworks. None of these are issues a standard course project has to confront.

### 5 — Beyond standard practice
**No existing framework does attribution + detection + recovery together.** Commercial platforms (LangSmith, Langfuse, Braintrust, Arize, Maxim, Opik) each do part of this — trace capture, evaluation, RCA — but none combine step-level attribution, general silent-failure detection, and verified counterfactual repair in one evaluated pipeline. Building the combination is what's beyond standard practice, not any single piece of it.

### 8 — Interdependence
**Failures propagate; the execution graph models this directly.** Because agents in a workflow pass state to each other, an error in one agent's output can corrupt every downstream agent's reasoning. The graph-based architecture exists specifically because attribution has to account for this propagation, not just look at the single step where the wrong answer finally appeared.

---

**If asked live and this file isn't in front of you:** the honest short answer is "yes, that characteristic is real — it's argued in our CCP justification doc, I just didn't put all nine on the slide to keep it readable; happy to walk through it." That is a complete, defensible answer — the guide's own standard is whether the team can explain and justify each one, not whether it's printed on a slide.
