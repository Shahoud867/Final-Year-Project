# Granite — Expanded Scope and Feasibility Plan

*Prepared 2026-08-25, as the continuation of the audit in [`01_Executive_Audit_and_Verdict.md`](01_Executive_Audit_and_Verdict.md). That audit scored feasibility **5/10** and named it the binding constraint. This document is the answer: a revised scope that raises ambition where ambition is cheap and durable — evaluation science, measured product claims, benchmark rigor — and raises feasibility everywhere, through an explicit effort budget, a four-band scope taxonomy, a pre-registered descope ladder, per-gate minimum demos, and fallback ladders on every high-risk component.*

***Governance note (§5.3 discipline):** the frozen 20-mechanism set (10 foundational + 8 extensions + 2 parked, plan doc §7.0) was explicitly reopened on 2026-08-25 for this revision and re-frozen the same day with **zero mechanisms added, removed, or renamed**. Every addition below is evaluation methodology, benchmark design, process engineering, or a measured claim over already-committed mechanisms. Recorded as risk-register.md R27.*

---

## 1. Where the current scope actually falls short

Honest inventory, dimension by dimension, before touching anything:

| Dimension | Audit score | The real limitation | Fixed by |
|---|---|---|---|
| **Feasibility / scope structure** | **5/10** | 10 core items + 8 extensions + reproduction + benchmark + SDK + dashboard for 3 people — with **no effort budget anywhere**, no per-gate minimum demo, no pre-registered descope order, and integration proven only at Final-1 (the classic FYP killer: three subsystems that first meet each other in the last month) | §4 taxonomy, §5.1 budget, §5.2 critical path, §5.3 MDP-per-gate, walking skeleton (§3.10) |
| **Technical depth** | 8/10 | Depth is *horizontal* (many mechanisms) not *vertical* (few mechanisms studied hard). Two design artifacts are owed but unscheduled: the real per-step hook interface (R2 flagged post-hoc timestamps) and the Recovery Controller's checkpoint-state schema | §6.2 — both scheduled as Mid-1 design artifacts |
| **Research depth** | 8/10 | RQ1–4 exist but carry no hypotheses, no pre-registered analysis plan, no statistical treatment (every number would ship as a bare point estimate), and no ablation matrix mapping components to the claims they isolate | §3.1, §3.4, §6.1 |
| **Evaluation rigor** | 8/10 | Every published benchmark in the corpus contains **only failing runs** — so the false-alarm behavior of the whole pipeline on *healthy* runs is unmeasured and unreported, here and in the literature we reviewed. No human baseline exists anywhere in the plan, even though the entire premise is "today a human reads the trace and guesses" — the human is the comparator the product story implies, and nobody measures them | §3.2 clean controls + FPR, §3.3 human baseline |
| **Product value** | 7/10 | The adoption barrier (integration effort) is honestly *stated* but never *measured*; the dashboard has no pinned scope (unbounded UI work is where FYP-2s die); the benchmark release is a data dump, not a reproducible artifact | §3.8 time-to-integrate, §6.5 dashboard pinned to 3 screens, §3.9 reproducibility kit |
| **Novelty durability** | 7/10 | The differentiation survives R9's correction but is defended only by the benchmark and the closed loop; the crowding risk (R7) is real. The cheap unclaimed territory adjacent to what we already build — false-alarm rates, human comparison, cost–accuracy frontiers, self-correction dynamics — is unoccupied in the corpus and widens the moat at near-zero mechanism cost | §3.2, §3.3, §3.6, §3.7 |
| **Implementation process** | — | CI arrives as extension #8 (late); integration is big-bang; no seed/split/contamination policy; GSM8K contamination (it is in every LLM's pretraining) is unaddressed and a sharp panelist will raise it | §3.10, §6.3, §6.4 |

**The one thing that is *not* a limitation:** the mechanism list. The audit's own change log (item 11) says expansion of the mechanism surface is scope creep, and it is right. Anyone proposing to fix a 5/10 feasibility score by *adding features* has misread the problem.

---

## 2. The expansion principle

**Ambition per unit of risk.** The scope expands only along axes where one of these is true: (a) the work is already scheduled and the addition is *doing it to a higher scientific standard*, (b) the data must be generated anyway and the addition is *an analysis that falls out of it*, or (c) the addition converts an honest verbal admission into a *measured number*. Nothing below adds a mechanism, an API surface, a framework, or a screen.

Every addition in §3 passes five tests, stated per item: **problem justification · user value · technical rationale · implementation path · evaluation method.**

**Expansions considered and explicitly rejected** (on record, so the discipline is visible):

| Rejected expansion | Why |
|---|---|
| Plugin architecture for the SDK | Audit change-log item 11: right-sized already; pure scope creep |
| 4th+ framework at full benchmark depth | R8 breadth-over-depth; roughly doubles harness work for a marginal claim |
| LLM-judge silent-failure detector as a comparison arm | Would blur the project's single most load-bearing commitment (SED is 0%-API); the literature already shows LLM judges do poorly here (AUROC ≤0.65, R7 triage) — reproducing that is not our contribution |
| Training a custom attribution model (AgenTracer-style 8B) | A different project; GPU budget and training-stability risk with no CCP gain |
| RL-based preventive classifier | Already deferred in the frozen list; stays deferred |
| "Beat ErrorProbe on Who&When" as a *commitment* | Overpromising against a backbone-confounded target; the commitment stays "reproduce within the band, report transparently" — beating it is an outcome, not a promise |
| Chaos testing / cross-domain transfer | Stay parked (Future) |
| Multi-tenant SaaS, billing, auth | Stays in post-FYP productization (plan §14) |

---

## 3. The additions — eleven items, none of them mechanisms

### 3.1 Pre-registered statistical protocol *(Core — methodology)*
- **Problem:** every headline number currently ships as a bare point estimate; a panel (or reviewer) can dismiss any cross-architecture delta as noise. The corpus itself mostly reports point estimates — rigor here is differentiation, not overhead.
- **User value:** claims a third party can trust; the benchmark's numbers mean something.
- **Technical rationale:** bootstrap 95% CIs over cases (non-parametric, no distributional assumption, trivial to compute); fixed seeds; N=5 replays with variance for every recovery-rate figure; per-backbone reporting exactly as ErrorProbe does.
- **Implementation path:** one shared `stats.py` used by every evaluation script; analysis plan written into plan §11 *before* Mid-1 results exist.
- **Evaluation:** every table in the final report carries CIs; the pre-registration is checkable against the dated git history.
- **Cost:** ~3 days. **Owner:** Noor.

### 3.2 Clean-control traces and a false-alarm study *(Core — benchmark design)*
- **Problem:** Who&When and every corpus benchmark contain only failures. A diagnosis pipeline's **false-positive rate on healthy runs** — the number that decides whether anyone can leave it switched on — is unreported in the literature we reviewed and unmeasured in our own plan. "What's your false-alarm rate?" is an obvious panel question with currently no answer.
- **User value:** an operator will not deploy a tool that cries wolf; FPR is the trust metric.
- **Technical rationale:** the fault-injection harness already generates traces; running it with injection *disabled* produces labeled-clean controls for free. Design decision: **15–20% of the benchmark (≥75 of 500 traces) are clean controls**, making FPR measurable by construction — and making our benchmark structurally richer than any in the corpus.
- **Implementation path:** a no-op injection mode in the harness (trivial); FPR computed per component (SED false alarms, spurious attributions) and pipeline-level.
- **Evaluation:** pipeline FPR and SED false-alarm rate reported with CIs; provisional target FPR < 5% on clean controls, finalized at Mid-1 pre-registration.
- **Cost:** ~1 week absorbed into scheduled benchmark work. **Owner:** Shahoud (generation), Noor (analysis).

### 3.3 Human-baseline micro-study *(Advanced)*
- **Problem:** the project's entire premise — slide 2, verbatim — is "a human reads the trace and guesses." That human is the *actual* baseline the product displaces, and nobody in the corpus measures human attribution accuracy under a realistic time budget (Who&When reports annotation *cost*, not human diagnostic accuracy on a benchmark).
- **User value:** the product claim becomes a measured sentence: *"humans found the culprit step in X% of cases taking a median Y minutes; Granite scores Z% in seconds."* Nothing else in the defense will land harder.
- **Technical rationale:** small-N descriptive comparison, not a psychology experiment — 6–10 participants (the same peers/faculty pool §13.1's UAT already commits to), 8–10 benchmark traces each, 5-minute cap per trace, accuracy + time recorded.
- **Implementation path:** runs inside the already-scheduled UAT window (FYP-2 weeks 8–14); consent per plan §0.09; traces drawn from the benchmark so ground truth is known. **Doubles as stakeholder-contact and acceptance-testing evidence** — one study, three guide requirements.
- **Evaluation:** human vs. Granite accuracy and time, with the honest caveat that N is small and the comparison is descriptive.
- **Cost:** ~30–40 team-hours + 6 participant-hours. **Owner:** whole team, Shahoud coordinating.

### 3.4 Ablation matrix *(Core — methodology)*
- **Problem:** "you just combined existing techniques" (Q5) is answered rhetorically today; an ablation matrix answers it experimentally by isolating what each component contributes.
- **Technical rationale / path:** a pre-declared table mapping each ablation to the claim it isolates: verification gate off → false-repair rate (already committed); memory on/off → VRM's contribution (already the R22 fallback); SED off → silent failures caught by the rest of the pipeline alone; graph-feature confidence vs. LLM-stated confidence → justifies the 0%-API scoring choice. The first two are already committed — this formalizes all four in one matrix.
- **Evaluation:** each ablation reported under the same statistical protocol.
- **Cost:** the runs are cheap (subset-scale); ~1 week analysis. **Owner:** Noor.

### 3.5 Benchmark datasheet, MAST alignment, and propagation labels *(Core — release quality)*
- **Problem:** a benchmark released as a directory of JSON is a data dump; the field cites benchmarks that document themselves.
- **Technical rationale / path:** a datasheet (datasheets-for-datasets style): generation protocol, fault taxonomy mapped to MAST categories where applicable, per-trace labels — including a **propagation label** (propagated / self-corrected / masked) that Spike 3 already proved necessary — license, splits, and an explicit **contamination statement**: GSM8K is in every LLM's pretraining, and our answer is structural — attribution ground truth derives from the *injection point in the trace*, not from the task's final answer, so a model "knowing" the answer does not leak the label. tau-bench's procedural policies are contamination-resistant by nature.
- **Evaluation:** datasheet ships with the release; the contamination argument is stated before a panelist raises it.
- **Cost:** ~1 week during scale-up. **Owner:** Shahoud.

### 3.6 Self-correction dynamics analysis *(Advanced — free research finding)*
- **Problem/rationale:** Spike 3's most interesting result was an *accident*: the agent silently repaired an injected fault. Once every benchmark trace carries a propagation label (§3.5), the benchmark yields a descriptive finding nobody in the corpus has published: **the self-correction rate of modern agent frameworks under controlled fault injection, by fault type and framework.** It costs nothing beyond the labels — the analysis falls out of data we must generate anyway.
- **User value:** operators learn which fault classes their frameworks absorb silently (itself a silent-failure risk: self-correction masks fragility).
- **Evaluation:** rates with CIs, by framework × fault type; reported as RQ2a.
- **Cost:** ~3 days of analysis. **Owner:** Shahoud.

### 3.7 Cost–latency–accuracy frontier *(Advanced)*
- **Problem:** extension #6 already commits two diagnosis modes (cheap single-pass vs. full pipeline); shipping the modes without measuring the trade-off wastes the research value. Adjacent context, cited honestly: StepFinder targets inference efficiency, FAMAS is noted as ~$1/run costly — the *deployment frontier* (accuracy per dollar and per second, across modes and backbones) is under-reported and is precisely what an adopting team needs.
- **Technical rationale / path:** we already log tokens and wall-clock everywhere (the NFR requires it); the frontier is a plot over runs we already make, at the three backbones the sensitivity check already covers.
- **Evaluation:** accuracy-vs-cost and accuracy-vs-latency curves, with the single-pass mode's retention of full-pipeline accuracy reported (provisional target: ≥80% of agent accuracy at ≤30% of cost — finalized at Mid-1).
- **Cost:** ~4 days. **Owner:** Saif (instrumentation), Noor (analysis).

### 3.8 Time-to-integrate metric *(Advanced — product)*
- **Problem:** the plan admits integration effort is the adoption barrier, then never measures it. An unmeasured barrier is a rumor.
- **Path / evaluation:** in each UAT session, measure minutes from `pip install` to first diagnosis on the participant's own workflow; target median **< 30 minutes** on CrewAI/LangGraph. Failures and friction points logged as product findings.
- **Cost:** free (instrumented into UAT). **Owner:** Saif.

### 3.9 Reproducibility kit *(Core — release quality)*
- **Problem:** "public benchmark" is only a real contribution if a stranger can rerun the headline table.
- **Path:** one `docker compose` + one script that regenerates the final report's headline table from raw traces (Docker is already committed in plan §13; this is packaging, not new infrastructure).
- **Evaluation:** acceptance test — a team member who didn't build it reruns the table on a clean machine; later, any leaderboard submission implicitly re-validates it.
- **Cost:** ~1 week. **Owner:** Saif.

### 3.10 Walking skeleton by Mid-1 *(Core — process; the single biggest feasibility fix)*
- **Problem:** the current timeline proves integration end-to-end at **Final-1** — meaning three separately-built subsystems meet for the first time with one gate left in the semester. This is the most common way three-person FYPs die, and no document currently defends against it.
- **Path:** by Mid-1, one thin thread runs end-to-end: toy CrewAI workflow → instrumented trace → graph → attribution (simplified) → SED check → replay → one dashboard row. Every interface exists and is exercised; every component behind it can then deepen independently against a working contract.
- **Evaluation:** the skeleton *is* the Mid-1 demo; interface breakage after Mid-1 is a recorded design change, not a discovery.
- **Cost:** ~55 h, already inside the FYP-1 budget (§5.1). **Owner:** all three (it is precisely the thing that forces the three lanes to agree on interfaces).

### 3.11 CI from week 1 of the build *(Core — process)*
- Plain engineering hygiene pulled forward from extension #8's *idea* (the extension itself — regression-gating on accuracy thresholds — stays an extension): tests + lint + the skeleton's smoke test on every push, GitHub Actions free tier. **Cost:** ~1 day. **Owner:** Saif.

---

## 4. The scope taxonomy — Core / Advanced / Stretch / Future

The frozen mechanism list is unchanged; this taxonomy is the **sequencing and grading layer over it**, plus the §3 additions. The bands are what the panel should grade against.

| Band | Contents | Rule |
|---|---|---|
| **CORE — mandatory for FYP success** | The 10 foundational mechanisms (Tier 1 unconditional; Tier 2 under its pre-registered Mid-1 gates) · full evaluation v1 under the statistical protocol (§3.1) with FPR/clean controls (§3.2), coverage, and the ablation matrix (§3.4) · benchmark ≥500 traces incl. clean controls, with datasheet (§3.5) · SDK + backend + 3-screen dashboard (§6.5) · containerized deployment · reproducibility kit (§3.9) · walking skeleton + CI (§3.10–3.11) | Never descoped. Failure here = project failure. Tier 2 items resolve via their gates, never by silent drop |
| **ADVANCED — strengthens the project significantly** | Human-baseline study (§3.3) · self-correction analysis (§3.6) · cost–latency frontier (§3.7) · time-to-integrate (§3.8) · ext #1 widen fault taxonomy to 3 · ext #3 cyclic-graph support · ext #4 confidence calibration | Planned and budgeted (§5.1); individually droppable **only** via the descope ladder, each drop recorded per §5.3 |
| **STRETCH — only if Core is done early** | ext #2 third architecture · ext #5 preventive classifier (contingent per R15 anyway) · ext #6 propagation map UI · ext #7 explainable confidence · ext #8 compatibility layer · static leaderboard page · webhook / NL incident report / trend chart (from the 13-item table) | **Unbudgeted.** Spend only surplus hours; starting any Stretch item before Core is integration-complete is a recorded violation |
| **FUTURE — explicitly outside the FYP** | Cross-domain transfer · chaos testing · RL classifier · full 7-framework benchmarking · multi-tenant SaaS/billing/auth · custom-model training · production-hardening | Named in the report's future-work section only; never on a slide as promised scope |

**Pre-registered descope ladder** — under schedule slippage, drops happen in exactly this order, each recorded:
1. All Stretch (unbudgeted anyway — this step costs nothing).
2. Time-to-integrate (§3.8) → self-correction analysis (§3.6) → frontier (§3.7) → calibration (ext #4).
3. Fault taxonomy 3 → 2 types (ext #1 partial).
4. Benchmark stretch target 1,000 → floor 500.
5. Cyclic support (ext #3) drops **last** among Advanced — LangGraph's own cyclic workflows make it claim-coupled, and Spike 6 already validated the mechanism, so its residual cost is integration only.
6. The human-baseline study and ablation matrix are protected next-to-last: they are the cheapest high-value items in the plan.
7. **Core never drops.** Tier 2 outcomes are decided by their gates, which have recorded fallbacks that still close the loop.

---

## 5. Feasibility engineering

### 5.1 The effort budget (the number that was missing)

Capacity: 3 members × ~15 h/week (honest for students carrying coursework) × ~28 remaining project weeks (≈12 post-defense in FYP-1 + ≈16 in FYP-2) = **1,260 nominal hours**, haircut ~10% for exams/holidays → **~1,130 plannable hours**.

**FYP-1 (post-defense, ~490 h):**

| Work | Hours | Lead |
|---|---|---|
| Full 3-stage ErrorProbe reproduction + iteration protocol (20-case dev subset, full runs at checkpoints) | 110 | Noor |
| Real per-step instrumentation hooks (CrewAI + LangGraph) + normalized trace schema v1 | 90 | Shahoud |
| Injection harness v2 (3 fault types incl. no-op/clean mode) + 50-trace pilot benchmark | 70 | Shahoud |
| Execution graph + backward tracing + graph-feature scoring | 70 | Noor |
| SED v1 + constraint schemas for GSM8K / tau-bench + abstention | 50 | Noor |
| Tier 2 gates: RC checkpoint PoC on LangGraph + VRM stronger-backbone re-test | 45 | Saif / Noor |
| **Walking skeleton + CI + integration glue** | 55 | all |
| **Subtotal** | **490** | |

**FYP-2 (~640 h):**

| Work | Hours | Lead |
|---|---|---|
| Benchmark scale-up to 500–1,000 incl. clean controls + datasheet + propagation labels | 90 | Shahoud |
| Replay engine hardening (N-replay variance) + Repair Agent atomic-field interface + closed-loop integration | 80 | Saif |
| SDK packaging + backend API + record store + deployment off dev machine | 100 | Saif |
| Dashboard (3 screens, pinned — §6.5) | 45 | Saif |
| Full evaluation: headline runs, ablation matrix, FPR study, CIs, frontier | 120 | Noor + Shahoud |
| Human baseline + UAT + time-to-integrate | 45 | all |
| Advanced band: calibration + cyclic integration + frontier extras | 60 | Noor / Saif |
| Report, documentation set, defense preparation | 100 | all |
| **Subtotal** | **640** | |

**Budgeted: ~1,130 of 1,130 plannable — with three safety layers on top:** Stretch is entirely unbudgeted (surplus-only); the descope ladder converts slippage into recorded scope decisions rather than quiet quality decay; and the scaffolding-heavy lines (SDK, backend, dashboard, CI) are estimated at Level-2 AI-assisted velocity — which the 8-spikes-in-3-days POC record demonstrates the team actually achieves. Without that assist those lines would run ~1.5×; that margin is a fourth, unstated buffer.

**Machine-time (distinct from person-time):** trace generation at ~10 LLM calls/trace runs 5–10 min/trace on the local 3B — 1,000 traces ≈ 80–170 machine-hours, i.e. nights and weekends on two laptops, or ≈ **$17.50** total on Haiku-class + Batch API with no wall-clock problem at all ([cost-estimate.md](../../../deliverables/stage-0-proposal/proposal-documents/cost-estimate.md)). "1,000 traces" is not a fantasy number; it is two idle weekends or eighteen dollars.

### 5.2 Critical path

**Reproduction → benchmark → evaluation → report.** That chain owns the calendar. Everything else — SDK, dashboard, RC/VRM gates, extensions — parallelizes off it. Two consequences, stated as rules: *the critical path never passes through the dashboard*, and any week the critical path slips, its owner takes hours **from** Advanced work, never the reverse.

### 5.3 Minimum Defensible Product per gate

What must demo **in the worst case** — defined now, so a bad month never improvises the gate story:

| Gate | MDP (worst-case demo) |
|---|---|
| **Mid-1** | Walking skeleton runs end-to-end live · full reproduction number + band verdict stated · both Tier 2 gates resolved with recorded outcomes · 50-trace pilot benchmark with clean controls · hook-interface + checkpoint-schema design docs baselined |
| **Final-1** | Core integrated on real workflows in both frameworks · benchmark ≥200 traces · SED + replay measured on the pilot · SDK installable by someone who didn't build it |
| **Mid-2** | Benchmark ≥500 incl. controls · evaluation v1 with CIs, FPR, ≥2 ablations · dashboard usable · deployed off the dev machine |
| **Final-2** | Full evaluation + human baseline + UAT + datasheet + reproducibility kit + public release |

### 5.4 Fallback ladders on the five riskiest components

| Risk | Fallback ladder (pre-registered) |
|---|---|
| ErrorProbe reproduction misses the ±10-pt band (R1) | Band verdict → transparent dual reporting per Annex A.2 → all cross-architecture and silent-failure claims ride on **our controlled implementation compared against itself across architectures**, which no reproduction gap invalidates |
| Recovery Controller gate fails (R21) | Re-scope to replay-based resumption (Tier 1 delivers it) — the loop still closes, the mechanism changes, the decision is recorded |
| VRM re-test fails again (R22) | Ships as memory-on/off ablation — an evaluation contribution under §4's own table |
| Benchmark scale stalls (generation quality or time) | 1,000 → 500 floor → **300 with the full statistical protocol beats 1,000 without it**; the CI-carrying claims survive at reduced N with wider intervals, honestly reported |
| UAT / human-study recruitment fails | §13.1 proxy rule already declared → fallback to 4 participants with the limitation stated → last resort: time-to-integrate self-measured by the non-building team member, labeled as such |

### 5.5 Why this is a full year even with AI-assisted development

The §7 resilience answer, upgraded with the budget's own numbers: of ~1,130 hours, at most ~300 (SDK, backend, dashboard, CI, scaffolding) are in categories AI assistance compresses — **and they are already budgeted at compressed velocity**. The remaining ~800 hours are categories no code generator shortens: supervising and validating 500–1,000 controlled generations, evaluation design and statistical analysis, human studies, cross-framework instrumentation debugging (spike 2's timestamp lesson), reproduction fidelity against a published number, and writing. A week-built AI version has no benchmark, no measured claims, no false-alarm story, no human comparison, and no verified repair — it demos well and is worth nothing at exactly the points this plan spends its hours.

---

## 6. Reassessment against the expanded scope

### 6.1 Research questions — now with hypotheses and decision rules

| RQ | Hypothesis (provisional targets; finalized in the Mid-1 pre-registration) | Metrics | Decision rule |
|---|---|---|---|
| RQ1 reproduction | Reproduction lands within ±10 pts of 59.5% on a Sonnet-class backbone | step/agent acc + CI | Band verdict; Annex A.2 dual reporting otherwise |
| RQ2 transfer | Out-of-ecosystem attribution degrades measurably (expect >10-pt step-acc drop) | acc + CI, home vs. transfer | Either direction is a finding; pre-registered so a null result is publishable, not embarrassing |
| RQ2a self-correction *(new)* | Self-correction rates differ by framework × fault type | rate + CI | Descriptive; feeds the benchmark datasheet |
| RQ3 silent failures | SED: recall ≥70% at precision ≥90% *within coverage*; FPR <5% on clean controls | P/R/coverage/FPR + CIs | Targets pre-registered at Mid-1; abstention reported, never hidden |
| RQ4 verified repair | Recovery >50% of previously-failed runs; false-repair <10% (gate ablation) | recovery, false-repair + CIs | Matches slide-8 success bands |
| RQ4a frontier *(new)* | Single-pass retains ≥80% of full-pipeline agent accuracy at ≤30% cost | acc/cost/latency curves | Reported as a frontier, not pass/fail |

### 6.2 Architecture — sufficient; two design artifacts now scheduled
No new components. Two contracts the sketch implies but never specifies become **Mid-1 baselined design docs**: the per-step hook interface (what exactly each adapter must emit — R2's post-hoc-timestamp lesson made this owed), and the Recovery Controller checkpoint-state schema (what state is saved, what gets patched on resume). Both are prerequisites of their subsystems, not additions.

### 6.3 Datasets — sufficient, with two policies added
GSM8K + tau-bench retail stand (GAIA stays out — [DOWNLOAD.md](../../../data/DOWNLOAD.md)). Added: a **split policy** (no workflow template appears in more than one of dev/test; memory-retrieval tests get temporally-ordered splits so VRM never "remembers" the future) and the **contamination statement** (§3.5) — injection-derived ground truth is structurally immune to the agent knowing GSM8K answers, and we say so before being asked.

### 6.4 Evaluation methodology — the largest upgrade
Was: a good metric list with point estimates on failing traces only. Now: statistical protocol (§3.1) + clean-control FPR (§3.2) + ablation matrix (§3.4) + human baseline (§3.3) + frontier (§3.7) + coverage (already added) + per-backbone reporting. This is the difference between *having metrics* and *having an evaluation science* — and it is where most of the new ambition lives, precisely because it is the kind of ambition that cannot rot into infeasibility.

### 6.5 Product design — pinned
Dashboard fixed at **three screens**: (1) runs & diagnoses list, (2) trace/graph view with propagation path + evidence, (3) repair & replay report (recovery rate, confidence, gate status). Anything further is Stretch (ext #6/#7). The SDK's developer-experience target is the measured time-to-integrate (§3.8). The benchmark release ships as data + datasheet + reproducibility kit + license — a citable artifact, not a folder.

---

## 7. Panel objections — both failure modes, answered

### 7a. "This is too thin" *(insufficient-scope attacks)*

| Objection | Answer |
|---|---|
| "AI tooling builds this in two weeks" | §5.5: the ~800 irreducible hours are data supervision, evaluation science, human studies, cross-framework debugging — named, budgeted, and demonstrably not generation tasks |
| "It's reproduction plus glue" | Four distinct claim types — transfer measurement, benchmark artifact, closed verified-repair loop, evaluation science — and the ablation matrix (§3.4) experimentally isolates what *our* components contribute |
| "Synthetic benchmark, self-graded exam" | A9 + clean controls (which no corpus benchmark has), MAST alignment, propagation labels, datasheet, contamination statement — our synthetic benchmark is more rigorously documented than the published ones |
| "GSM8K is memorized by every model" | §6.3: ground truth derives from the injection point in the trace, not the task answer — contamination cannot leak the label; disclosed proactively |
| "Where's the human in the loop?" | Measured (§3.3): the first human-vs-system attribution comparison on any benchmark in this corpus |

### 7b. "This is unrealistic" *(overreach attacks)*

| Objection | Answer |
|---|---|
| "Three projects, three students" (A2) | One pipeline (harness→benchmark→engine→SDK), now with an hour-by-hour budget (§5.1) summing inside capacity, a critical path that owns the calendar (§5.2), and Stretch spending only surplus |
| "10 core items is fantasy" | 8 of 10 already have running spikes; the 2 that don't sit behind gates with recorded fallbacks; the worst case still closes the loop |
| "1,000 traces is data-engineering fantasy" | Two idle weekends of local machine time or $17.50 on batch (§5.1); the floor is 500; ladder step 4 governs the retreat, and 300-with-CIs beats 1,000-without |
| "You'll integrate in the last month and die" | Walking skeleton at Mid-1 (§3.10) — integration risk is retired at the *first* gate, not the last |
| "The human study won't clear ethics/recruitment" | Proxy pool already declared in §13.1; consent per §0.09; 6 participant-hours total; the fallback ladder (§5.4) bottoms out at a labeled self-measurement |
| "Extensions will eat the core" | Advanced is budgeted at 60 h; Stretch is unbudgeted by rule; the descope ladder drops in pre-registered order, recorded per §5.3 |

---

## 8. The 11/10 case — and what stays honest

What "11/10" can legitimately mean here — **maximum meaningful scope at maximum credible feasibility** — and the case per dimension:

| Dimension | Before → case now | Why |
|---|---|---|
| Feasibility | **5 → 9** | Effort budget summing inside capacity; walking skeleton; MDP per gate; descope ladder; five fallback ladders; unbudgeted Stretch. The remaining point is reality: budgets are models |
| Evaluation rigor | 8 → **10** | CIs, clean-control FPR, ablation matrix, human baseline, frontier, coverage, pre-registration — a stronger evaluation section than several papers in the corpus |
| Research depth | 8 → 9 | Hypotheses + decision rules per RQ; two new sub-questions (self-correction, frontier) occupying genuinely unclaimed territory at near-zero cost |
| Technical depth | 8 → 9 | Two owed design artifacts scheduled; N-replay variance; checkpoint schema; the depth added is vertical, not horizontal |
| Product value | 7 → 8 | Time-to-integrate measured, dashboard pinned, reproducible release; the adoption barrier goes from admitted to quantified |
| Novelty durability | 7 → 8 | Four cheap adjacent claims (FPR, human baseline, self-correction, frontier) that no simultaneous preprint is likely to cover *together with* the benchmark and the loop |

Two things stay honestly outside our control, and the defense should say so if asked: **scores are the panel's to give, not ours** — this document is the strongest true case, not a self-grade; and the field may still publish into R7's watch list, in which case the standing gate-check reports it, and the benchmark + evaluation science survive it — well-measured descriptive artifacts are exactly the contributions simultaneous work does not delete.

## 9. Decision record (per §5.3)

**2026-08-25** — Scope reopened and re-frozen the same day. Added: eleven methodology/process/measurement commitments (§3), the four-band taxonomy + descope ladder (§4), the effort budget + MDP-per-gate + fallback ladders (§5), RQ hypotheses + sub-RQs 2a/4a (§6.1), split/contamination policies (§6.3), and the 3-screen dashboard pin (§6.5). **Zero mechanisms added, removed, or renamed** — the frozen 20 stand. Rejected expansions recorded in §2. Logged as risk-register.md R27; propagated to plan §7.2/§11/§12, defense package slide 9, and the question-bank addendum.
