# Granite — Proposal Defense Deck (10 slides, guide §16 order)

*This upgrades the existing `Proposal_Defense_Package.md` with the six audit fixes applied (two-tier core, named owners, controlled-replay wording, SED scope sentence, 8-spike count, cost line) **and** the 2026-08-25 scope-expansion pass (`06_Expanded_Scope_and_Feasibility_Plan.md`): scope bands, effort budget, walking skeleton, clean-control evaluation, human baseline, ablation matrix. Each slide: exact content → visual → speaker notes → the question this slide triggers, with the answer's location in deliverable 02.*

---

## Slide 1 — Title and one-line problem
**Content:**
- **A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery** — short title **Granite**
- Stream **A (research-derived)** · Shahoud Shahid 23i-2515 · Muhammad Noor 23i-2520 · Saif Shahzad 23i-2634 · Supervisor: [name — fill before Thursday]
- One sentence: *When a team of AI agents fails — including when the answer looks right but isn't — no published method can reliably say which agent went wrong at which step, and none can test a fix before it's trusted. Granite diagnoses, repairs, verifies, and recovers — and ships as an installable SDK.*

**Visual:** none beyond the title block. **Speaker notes:** 20 seconds; do not explain the title word-by-word — slide 6 does. **Triggers:** "self-healing? show me" → A1.

## Slide 2 — Stakeholders and current workflow
**Content:**
- Client (guide §5.2, Stream A rule): the engineering team operating a multi-agent system near production — grounded in a customer-support/retail workflow (tau-bench retail, our active substrate)
- Stakeholders actually consulted: **[two names/roles + dates — must be filled before Thursday; this is the single highest-priority open item in the entire project]**; what changed in requirements as a result: [one line]
- Today's workflow: observability platform captures the trace → a human reads it and guesses → no measured accuracy, no silent-failure check, no way to test a fix before redeploy — and as of the 06-doc addition, this human is no longer just described: a **human-baseline micro-study** measures them directly (accuracy + time, inside the already-scheduled UAT window)
- SDG 9 (target 9.5) — context, not the contribution

**Visual:** 3-step "current workflow" strip (capture → human reads → guess), with a red "unmeasured" tag on step 3 — retitled "now measured" once the human baseline runs. **Speaker notes:** the stakeholder line is what converts CCP characteristic 6 from weak to clear — say who, when, what you learned. If genuinely still open at delivery time, say so plainly and name the date it will close; do not imply contact happened if it hasn't. **Triggers:** Q1–Q2.

## Slide 3 — Existing solutions and the evidence-based gap
**Content:** keep the existing comparison table (ErrorProbe / AgenTracer / LangSmith Engine + Arize Alyx / other platforms / closest prior FYP / manual workflow) with two edits: fill the **prior-FYP row from the department archive**, and phrase the commercial row as the *corrected* claim: "automated RCA is emerging (2026) — but no documented step-level attribution accuracy, no counterfactual fix-testing, no general silent-failure detection, all stack-locked." Add one line the 06 pass surfaced: **none of the six platforms checked publish a false-alarm rate or any benchmark of their own diagnostic accuracy — ours will.**

**Visual:** the table itself. **Speaker notes:** volunteer the correction story — "our first draft said 'nobody automates this'; direct vendor checks proved that stale and we corrected it, on record (R9)." Panels reward self-correction they didn't have to extract. **Triggers:** A5, Q21.

## Slide 4 — Research and technical basis
**Content:**
- 7 core papers read full-text (Who&When → AgenTracer → SDBL, TraceElephant, ErrorProbe, AgentAsk, PROTEA) + triage of GraphTracer/FALAT/DoVer; 7 commercial platforms checked directly
- The lineage chart: Who&When 14.2% → AgenTracer ~37–43% → **ErrorProbe 59.5%** step accuracy — baseline chosen on performance, not recency
- Two gaps that survive full-text reading: **no paper tests an architecture outside its own benchmark construction**; **ErrorProbe's own Limitations section confesses silent failures**
- Research questions now carry **pre-registered hypotheses and decision rules** (06 doc §6.1), not just questions — RQ2a (self-correction rates by framework × fault type) and RQ4a (cost–latency–accuracy frontier) added as free analyses over data already being generated

**Visual:** the lineage/accuracy ladder (three bars rising to 59.5%, with a shaded "40.5% still wrong" cap). **Speaker notes:** one sentence on the backbone-confound caveat (R4) — saying it before they do defuses Q6. **Triggers:** Q6, Q7.

## Slide 5 — CCP justification
**Content:** 9-characteristic table, now **9/9 with stakeholder contact done** (else keep 8+1 honest): conflicting requirements (depth vs latency, completeness vs privacy, generalization vs specialization) · no obvious solution (59.5% after 15 months, 7 papers) · depth of knowledge · unfamiliar issues (delayed manifestation, non-determinism) · beyond standard practice · diverse stakeholders (operators / product teams / auditors — now evidenced) · significant consequences · interdependence (the propagation graph *is* the problem) · ill-defined cause (the three-unknowns paragraph, verbatim from plan §2).

**Visual:** compact 9-row checklist. **Speaker notes:** read the characteristic-9 paragraph aloud — it is the strongest prose in the plan and directly answers "why is this complex." **Triggers:** "aren't you claiming too many characteristics?" → "the guide's own strong examples clear 6–9; we evidence each and hold #6 to what the contacts actually support."

## Slide 6 — Contribution and solution (the architecture slide)
**Content:**
- Contribution statement (§4 template, verbatim from plan §3)
- Architecture: the one-page sketch, three owner-labeled lanes → **Shahoud (Data/Benchmark) · Noor (Diagnosis) · Saif (Platform)**
- The pipeline in one line: trace → execution graph → **Semantic Error Diagnostic** (deterministic, scoped: *machine-checkable task constraints; abstains and reports coverage where none exist*) → backward causal tracing (ErrorProbe-method) → **Repair Agent** (candidate fix) → **controlled counterfactual replay** (recovery rate measured, N=5 replays with variance, decoding parameters pinned) → confidence-gated recommendation
- External components: LLM = **core-assist**, 80–85% of components 0%-API by committed mechanism

**Visual:** the architecture sketch, simplified to one screen. **Speaker notes:** say "controlled, not deterministic — the protocol is deterministic, model outputs are variance-measured" unprompted; it closes A7 before it opens. **Triggers:** A4, A6, A7, Q13–Q14.

## Slide 7 — POC evidence (mandatory, guide §12) — *show, don't describe*
**Content:** **8 spikes**, one row each with its real number:
1 ErrorProbe repro (simplified, 3B, n=8): 75% agent / 12.5% step — signal, not the full pipeline · 2 CrewAI instrumentation: clean 3-node/2-edge trace · 3+3b fault injection: unambiguous ground truth; self-correction case kept as a finding — the same finding that seeds the 06-doc's new self-correction-rate analysis (RQ2a) · 4 Semantic Error Diagnostic: catches known-wrong incl. near-miss, 0 false positives · 5 controlled counterfactual replay: corrupted 97.2 → recovered 108.0 · 6 cyclic graphs: bound proven load-bearing by control run · 7 preventive classifier: **honest negative, 0.25 across the board** — mitigation planned · 8 Repair Agent: **4/6 repair success**, both failures one fixable interface cause (R17)

**Visual:** live terminal or the JSON outputs on screen — the guide says evidence shown, not described. **Speaker notes:** lead with spikes 7's negative and 8's failure analysis; "a POC that disproved the assumption is usually more valuable" is the guide's own sentence — quote it. **Triggers:** A3 (the 12.5%), A10.

## Slide 8 — Evaluation plan
**Content:** baseline = reproduced ErrorProbe (**pre-registered ±10-point acceptance band vs. 59.5% on a comparable-class backbone**; Annex A.2 fallback recorded) · data = Who&When (184, in hand, MIT) + our benchmark (floor 500 / stretch 1,000 traces, **15–20% deliberately clean controls** — no paper in the corpus has these; TracerTraj conditional, on record R11) · metrics = agent/step accuracy, path-F1, silent-failure precision/recall **+ coverage**, **pipeline false-positive rate on clean controls** (a measurement absent from the entire corpus we reviewed), task completion, recovery rate, repair success, **false repair rate** (verification-gate ablation), latency overhead (<50% target, the NFR) · **every headline number carries a bootstrap 95% CI**, fixed seeds, N=5 replay variance, per-backbone reporting · **four-item ablation matrix** isolating what each component contributes (verification gate, memory, SED, graph-vs-LLM confidence) · **human-baseline comparison** (accuracy + time, 6–10 proxy participants, inside the UAT window) · failure cases that matter: silent failures, unseen architectures, budget pressure · what the evidence cannot support: production-scale claims — stated up front.

**Visual:** metrics-to-claims mapping (each RQ → its metrics), with the clean-control / FPR row visually distinguished as the addition no competing product or corpus paper reports. **Speaker notes:** give the success bands from deliverable 02 Q18 if asked "what counts as success." If asked why the evaluation grew three days before the defense: "the mechanisms didn't change — the rigor did; the frozen 20-item feature list is untouched (R27)." **Triggers:** Q18–Q19, A9, Q25 (new).

## Slide 9 — Scope, risks, dependencies
**Content:**
- **Committed core — two tiers, 10 items:** Tier 1 (evidence-backed): harness, benchmark, Culprit Agent, Error Step Localization, Verification Agent, Semantic Error Diagnostic, Repair Agent, Verified Automatic Repair. Tier 2 (committed with pre-registered Mid-1 gates, criteria written now): Recovery Controller (checkpoint-resume PoC on LangGraph, else re-scoped to replay-based resumption, recorded) · Verified Repair Memory (stronger-backbone re-test; its one prior test failed — 0/8 — stated here, not discovered later; else ships as a memory-on/off ablation study)
- **Scope bands, added 2026-08-25 (plan §7.2):** Core (never descoped) → Advanced (budgeted, droppable only via a pre-registered ladder: human study, self-correction analysis, frontier, calibration, taxonomy, benchmark scale, cyclic support — in that order) → Stretch (unbudgeted, surplus-only: 3rd architecture, preventive classifier, propagation map, explainable confidence, compat layer) → Future (out of scope: cross-domain, chaos testing, SaaS/billing)
- **The effort budget:** ~1,130 plannable person-hours (3 × ~15 h/wk × ~28 weeks, minus exam haircut) budgeted line-by-line against ~1,130 — FYP-1 ≈490 h, FYP-2 ≈640 h, named owners per line. Stretch spends only surplus.
- **Walking skeleton at Mid-1:** one thin thread, instrumented trace → graph → attribution → SED → replay → dashboard row, running end-to-end before Final-1 — retires integration risk at the *first* gate, not the last
- Top risks with status: R1 reproduction gap (band + fallback declared) · R5 cost (closed, quantified: ≈$353 recommended / $881 ceiling) · R7 literature crowding (gate-check standing order) · R21/R22 Tier-2 gates (criteria pre-registered) · R27 (scope-expansion decision, recorded)
- **Cost line:** ≈$353 recommended total (benchmark generation on cheap-tier batch ≈$18; ErrorProbe reproduction across ~20 dev iterations ≈$224; 10 full evaluation runs ≈$112); ≈$881 pessimistic ceiling. All 8 spikes to date: $0
- Ethics: advisory-only output, consent for real trace data, injection only on own/consenting systems

**Visual:** two-tier core diagram with gate icons on Tier 2, plus a four-band scope funnel (Core/Advanced/Stretch/Future) and a one-line effort-budget bar chart (FYP-1 490h / FYP-2 640h against capacity). **Speaker notes:** this slide *is* the A1/A2 defense — deliver it as confidence, not confession: "we pre-registered the decision rules before the results exist, which is what §5.3 asks of us, and the same discipline now covers the whole scope, not just the two Tier-2 items." If feasibility is pressed, this is the slide with the numbers — point at the budget table, don't just reassure. **Triggers:** A1, A2, Q9–Q11, Q24, addendum Q25.

## Slide 10 — Team responsibilities and timeline
**Content:**
- **Named ownership** (assigned 2026-08-25, recorded per §5.3, R24): **Shahoud Shahid** — Data/Benchmark (harness, instrumentation, benchmark, release) · **Muhammad Noor** — Diagnosis (graph, reproduction, SED, tracing) · **Saif Shahzad** — Platform (replay/recovery, SDK, backend, dashboard, deployment). Shared: architecture, integration, QA, ethics, defense.
- Five-gate timeline (plan §12) with the two Mid-1 decision gates, the full-reproduction milestone, and the **walking-skeleton milestone** all marked at Mid-1
- **Minimum Defensible Product per gate** (06 doc §5.3): Mid-1 = skeleton + reproduction verdict + both Tier-2 gates resolved + 50-trace pilot with clean controls. Final-1 = core integrated on real workflows, benchmark ≥200. Mid-2 = benchmark ≥500 with controls, evaluation v1 with CIs/FPR. Final-2 = full evaluation + human baseline + UAT + release — the worst-case demo is defined for every gate, not improvised

**Visual:** the gate timeline with three colored ownership lanes, the walking-skeleton diamond at Mid-1, and one MDP line per gate underneath. **Speaker notes:** each member states their own subsystem in one sentence, aloud, from this slide — the panel is checking §14.1, and hearing three voices early sets that tone. **Triggers:** Q12, Q23.

---

**Story spine check (Problem → Evidence → Gap → Solution → Novelty → Architecture → Research → Evaluation → Feasibility → Ownership):** slides 1-2 problem, 3-4 evidence+gap, 5 why it's capstone-level, 6 solution+novelty+architecture, 7 feasibility evidence, 8 proof plan (now with clean controls, CIs, human baseline), 9 scope discipline (now with bands, budget, skeleton), 10 people + MDP-per-gate. Total talk time target: 12–14 minutes, leaving the panel maximum questioning time — which this package is built to want.
