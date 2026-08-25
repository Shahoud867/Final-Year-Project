> **Superseded — kept for history only.** This was the first, abstract-level pass covering only 2 of the 7 papers now in scope. It has been fully replaced by [Full_Literature_Landscape_Analysis.md](Full_Literature_Landscape_Analysis.md) (all 7 papers, read in full) and, for the baseline decision specifically, by [ErrorProbe_Baseline_Selection.md](ErrorProbe_Baseline_Selection.md). Do not cite conclusions from this file without checking they still hold in those two.

# Who&When vs. AgenTracer — Overlap, Novelty, and FYP Feasibility Analysis

*Papers analyzed (both read in full from `agent-autopsy/`):*
- *Zhang, Yin, Zhang, Liu, Han, Zhang, Li, Wang, Wang, Chen, Wu — "Which Agent Causes Task Failures and When? On Automated Failure Attribution of LLM Multi-Agent Systems." ICML 2025. (`zhang25cq (2).pdf`) — referred to below as **Who&When**.*
- *Zhang, Wang, Chen, Zhou, Wang, Yan — "AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?" ICLR 2026. (`ICLR-2026-agentracer-...pdf`) — referred to below as **AgenTracer**.*

---

## 1 & 6. Which paper improves the other / does either solve the other?

**AgenTracer (ICLR 2026) directly builds on and improves Who&When (ICML 2025)** — this isn't inference, it's explicit in the text. AgenTracer's Related Works section states outright that it "advances the field" from where Who&When left off. AgenTracer also evaluates directly **on** Who&When's own benchmark (Table 1) and reuses its exact problem formulation (the "decisive error" (i\*, t\*) tuple, agent-level/step-level accuracy metrics) almost verbatim.

**Does AgenTracer fully solve Who&When, leaving nothing open? No.** It solves Who&When's two specific, stated pain points substantially but not completely:

- **Manual annotation cost** — Who&When needed three human experts, 30+ hours each, to annotate 184 tasks. AgenTracer automates this via counterfactual replay + programmatic fault injection, scaling to 2,000+ trajectories with no human labor. This is close to fully solved.
- **Poor attribution accuracy** — Who&When's best off-the-shelf-LLM method hit only ~53–57% agent-level / ~4–14% step-level accuracy, and even o1/DeepSeek-R1 "fail to achieve practical usability." AgenTracer-8B, a purpose-trained 8B model, beats giant proprietary LLMs (Gemini-2.5-Pro, Claude-4-Sonnet) by up to 18%. Real improvement, but **step-level accuracy is still modest** — even AgenTracer-8B tops out around 37–43% step-level on Who&When, far from solved.

**So:** AgenTracer is a genuine, substantial successor — but the underlying problem (accurate step-level failure attribution) remains open even after it.

---

## 2. Overlap

Yes, heavy and direct: same task definition, same core metrics, same benchmark (Who&When), same "decisive error" formalism. AgenTracer even explicitly adopts a finding from Who&When (that "all-at-once" context framing is the most stable evaluation setting) and cites it as justification. This is about as clean a "paper 2 supersedes paper 1" relationship as you'll find — which matters for an FYP: **if you build on this pair, your reference paper is AgenTracer, not Who&When**, per the FAST FYP guide's Annex A.1 ("prefer current... work" — AgenTracer is the more recent, stronger, more reproducible one, and it already has public code at `github.com/bingreeky/AgenTracer`).

---

## 4. What novelty actually remains

Two concrete gaps neither paper touches:

- **Cross-domain generalization is untested in both.** Who&When only covers its own 127 systems; AgenTracer only trains/evaluates on 6 specific frameworks (MetaGPT, AutoGen, Smolagents, AgentPrune, AFlow, OWL-Workforce) across coding/math/general-agentic tasks. Neither paper tests whether the attributor generalizes to a genuinely new, unseen multi-agent architecture or domain.
- **Self-repair is shallow in AgenTracer, and that's explicitly where it stops.** Its "self-evolution" demo (§5.3, Figure 3) only feeds attribution output back as generic textual reflection — the same category as the Self-Refine/CRITIC baselines it compares against. It never uses the structured (agent, step) output to drive a targeted intervention (e.g., re-executing only the specific failing agent's specific step). That's a real, unaddressed mechanism gap, not a buzzword one.

**Delta-sentence test** (per the FAST guide's Annex A.2): *"AgenTracer-8B reports [X]% step-level accuracy on its own 6-framework training mix, and only demonstrates generic reflective-feedback self-correction (4.8–14.2% gains). We will test its generalization to unseen multi-agent frameworks, and build a targeted attribution-driven repair mechanism instead of generic reflection, evaluated on held-out cross-domain trajectories using repair-success rate and cost-per-repair."* — this sentence completes cleanly, which is the guide's own bar for "has this been understood well enough to build on."

---

## 3. Feasibility per the FAST FYP Selection Guide (30 pages)

Strong fit, with one scoping decision that matters:

- **§12 POC** — excellent here, better than either RedShield or FinSynth's starting position. AgenTracer's trained 8B checkpoint is public. A team can clone it and run it against a small multi-agent system they build themselves within days — real, demonstrable feasibility evidence at proposal stage, exactly what §12 requires.
- **§14 external-component risk** — classify AgenTracer-8B as **Core-assist**, not Core-replacement: the team should *not* retrain it from scratch (the original RL training used 8×H100 — infeasible for a student budget). Use the released checkpoint as a fixed component; the team's own contribution is the generalization-evaluation harness and the repair mechanism built on top of its output. Test: if AgenTracer-8B were swapped for a different attributor, would the repair mechanism and evaluation methodology still be the team's own work? Yes — passes cleanly.
- **§3 CCP** — clears comfortably: real conflicting requirements (accuracy vs. inference cost; repair benefit vs. risk of a bad repair making things worse), no obvious solution (step-level attribution genuinely unsolved per both papers' own numbers), real depth (RL/reward design, multi-agent internals, credit assignment — which AgenTracer's own Related Works calls "a long-standing topic... yet remains largely unexplored in LLM agentic systems"), significant consequences (a wrong auto-repair in a coding/finance agent pipeline is a real failure mode worth naming explicitly), interdependence (attributor + repair mechanism + eval harness). Watch **characteristic 6 (diverse stakeholders)** — per Annex C.13 this is the most commonly under-stated characteristic; name explicitly who benefits differently (agent-framework developers vs. downstream product teams relying on agent reliability).
- **§7 AI-resilience** — the naive version ("wire a pretrained model to a re-prompt loop") is a weekend project. The real difficulty — rigorously proving/disproving generalization with proper held-out systems, and designing a repair mechanism that doesn't just as often make things worse — is genuine and worth stating explicitly in the proposal to preempt this exact objection.

---

## 5. Doable in 12 months with 3 students?

Yes, and arguably **lower infrastructure risk than RedShield** since there's already a working, released, pretrained model to start from — no need to build an attacker/defender pair from zero before any results exist.

- **Semester 1**: reproduce AgenTracer-8B inference on Who&When (the POC), build 1-2 new small multi-agent test systems outside its training mix, run the cross-domain generalization evaluation — this alone is a legitimate Final-1 "working core system."
- **Semester 2**: design and build the targeted, attribution-driven repair mechanism, benchmark against Self-Refine/CRITIC (a ready-made comparison protocol straight from AgenTracer's own paper), package as a deployable "agent debugging middleware" tool, run UAT with peer developer proxies.
- **Team split**: Person A — generalization harness + new test systems; Person B — targeted-repair mechanism; Person C — evaluation/cost/reporting pipeline. Mirrors the clean attacker/defender/evaluator pattern RedShield already uses, and each role passes the "if removed, does a real contribution disappear" test.

**Bottom line:** this pair is a genuinely strong Stream A candidate — arguably the most immediately de-risked of the three ideas now on the table, precisely because AgenTracer ships working code and a trained model, so your POC is a clone-and-run away rather than something you have to build from scratch.

---

## Citation anchors — where AgenTracer states it builds on Who&When

**Primary citation — Section 2 ("Related Works"), subsection "Failure Attribution for Agents", page 3:**

> "MAST (Cemri et al., 2025) was the first to alarmingly characterize this issue, identifying fourteen prevalent failure patterns ranging from task disobedience to reasoning-action mismatches. **Building upon this, Who&When (Zhang et al., 2025c) explored the feasibility of automating failure attribution, only to reveal that even giant reasoning models like DeepSeek-R1 fail catastrophically. AgenTracer advances the field by introducing both a scalable data synthesis pipeline and a lightweight, high-accuracy failure attributor.**"

**Two further confirming anchors:**

- **Section 3 ("Preliminary"), "Objective Formulation" paragraph, page 4** — AgenTracer adopts Who&When's own formalism directly: *"Following (Zhang et al., 2025c), we formalize this objective as..."* — this is where AgenTracer reuses Who&When's exact "decisive error" definition (the (i\*, t\*) tuple).
- **Section 5.1 ("Experimental Setup"), "Benchmarks & Evaluation" paragraph, page 7** — AgenTracer adopts a specific finding from Who&When as its own evaluation protocol: *"We follow the 'all-at-once' setting introduced in MAST... As Zhang et al. (2025c) has demonstrated this to be the most stable and effective."*

("Zhang et al., 2025c" is the reference-list entry for the Who&When paper — confirmed in AgenTracer's bibliography, page 15: *"Shaokun Zhang, Ming Yin, Jieyu Zhang... Which agent causes task failures and when? on automated failure attribution of llm multi-agent systems. arXiv preprint arXiv:2505.00212, 2025c."*)
