# Granite — Independent Critical Audit and Verdict

*Prepared 2026-08-25 against the uploaded repository (HEAD `6cf2401`, 5 commits) and the full FAST FYP Idea Selection Guide (all 30 pages). The GitHub remote could not be accessed from this environment (auth required); nothing below is based on unverified remote content.*

---

## 1. Executive verdict

**Approvable, with six real vulnerabilities — one of them self-inflicted three days before the defense.**

The prompt asked for a "complete transformation." That framing is wrong for this repository. Granite is already one of the most guide-compliant proposal packages I have seen at undergraduate level: Stream A correctly declared, an evidence-based baseline selection with cross-paper numbers pulled from the papers' own tables, 8 of 9 Seoul Accord characteristics with genuine evidence, a research-to-decision table, a RAID register that records *negative* results instead of hiding them (Spike 7's 0.25 classifier, VRM's 0/8 memory commits), a maintained AI usage log, a specifiability section with 5 "shall" requirements and a measurable NFR, an external-component classification with per-component mechanism commitments, and 8 runnable PoC spikes with real JSON outputs where the guide requires one. The spike code was spot-checked: it is real, honest, and well-commented — including the parts that document its own limitations.

**The verdict is therefore not "rebuild it." It is: (a) fix six specific vulnerabilities, (b) walk into the defense with the question bank in deliverable 02, (c) execute the repo change plan in deliverable 05.** The residual rejection risks that no document can fix are listed in §7.

### The six vulnerabilities, ranked

1. **The evidence pyramid is inverted (self-inflicted, 2026-08-24).** The official title leads with "Self-Healing … Verified Repair and Recovery." The two components that make the title true — Recovery Controller (zero PoC) and Verified Repair Memory (one real test, which **failed**: 0/8 memory commits, agent accuracy regressed 75%→50%) — were moved from *extensions* into the *committed core* three days before defense, by explicit decision overriding the register's own evidence-based caution (R18→R22). Committed core is what the project is graded against at every subsequent gate (guide §5.3); committing the weakest-evidenced items under the strongest-claiming title hands the panel its best attack. **Fix (§4.1): keep all 10 items but present the core in two recorded tiers with pre-registered Mid-1 decision gates.** This is fully guide-compliant and converts the vulnerability into a demonstration of change-control discipline.

2. **Ownership is unassigned, and the plan's deadline for it is non-compliant.** The guide's Gate 1 row is explicit: proposal defense requires "committed scope separated from optional extensions, **with primary technical ownership allocated to each member**." The plan doc (§9) and R6 defer assignment to "before Mid-1." That is a hard requirement miss *at the defense itself*, not a later milestone. **Fix: assign Shahoud/Noor/Saif to Data-Benchmark / Diagnosis / Platform before Thursday, by skill fit, and put names on slide 10.** Thirty minutes of work; without it, slide 10 violates the guide it cites.

3. **"Deterministic re-execution" of an LLM workflow is not technically defensible as written.** FR4 and several documents promise deterministic replay. Spike 5 was deterministic only because its toy pipeline is pure arithmetic; real downstream steps involve LLM calls, which are not deterministic even at temperature 0 on most serving stacks. A sharp panelist ends the defense with this. **Fix: rename the mechanism "controlled counterfactual replay":** frozen upstream context, affected downstream steps re-executed at temperature 0 with pinned parameters, recovery rate reported over N replays with variance; "deterministic" applies to the replay protocol and non-LLM computation, never to model outputs. One wording change across FR4, the plan doc, and slide 6 — deliverable 05 lists the exact edits.

4. **The baseline may not be reproducible at its published number, and the cost of trying is unquantified.** Spike 1's simplified pipeline on a local 3B model reached, across 5 independent runs (2026-08-26), step accuracy of 0-25% (mean 13%) against ErrorProbe's published 59.5% (achieved with Claude 3.7 Sonnet + full 3-stage pipeline + memory). The gap is expected and honestly logged (R1), but the entire delta claim is measured against this baseline, and R5 (API cost) is still open with no number attached. **Fix: before defense, produce a one-page cost estimate** (184 Who&When cases × 3-stage pipeline ≈ tens of thousands of tokens per case; benchmark generation 500–1,000 traces is the dominant cost) **and a declared acceptance band + fallback**: reproduction within a stated tolerance on a comparable backbone, else "faithful reproduction with transparent reporting" (guide Annex A.2 explicitly blesses this) with both our measured number and the published number reported side-by-side.

5. **The Semantic Error Diagnostic's rule-based commitment needs its scope stated before the panel states it for you.** "Detect semantic errors with zero LLM calls" reads as either trivial (schema checks) or impossible (general semantics). The honest, strong position: the claim is scoped to **task-constraint verification where the task specification yields machine-checkable constraints** (GSM8K's numeric answers, tau-bench's policy rules and action sequences) — exactly the class of well-formed-but-wrong outputs that anomaly-gated pipelines like ErrorProbe admit they cannot see. On tasks with no checkable constraint, the module **abstains**, and abstention/coverage rate should be added as a reported metric. That last addition also pre-empts "your detector only works where the answer is already known" — coverage is measured, not hidden.

6. **Novelty crowding is real and the differentiation sentence must be word-perfect.** R9's own correction shows LangSmith Engine and Arize Alyx (both 2026) now claim automated root-cause diagnosis and fix drafting; DoVer-class preprints sit in counterfactual-attribution territory. The surviving differentiation is narrower but genuine: *benchmarked, framework-agnostic, step-level attribution with measured (verified) repair, on a public cross-architecture benchmark* — versus closed, stack-locked, unbenchmarked commercial features and unreviewed preprints. Memorize it; deliverable 02 gives the full defense.

---

## 2. Repository audit (what actually exists)

| Category | Contents | Assessment |
|---|---|---|
| **Team-authored PoC code** | `dev/spikes/poc/` — 9 scripts (spikes 1, 2, 3, 3b, 4, 5, 6, 7, 8) + JSON outputs | **Real and good.** Verified by reading spike 4 and spike 8: honest design notes, stated limitations, real Ollama calls, outputs consistent with the register's claims. One committed `__pycache__` (hygiene). |
| **Planning/record docs** | `markdowns/` — plan doc (69KB), risk register (39KB, R1–R22), AI usage log (40KB), defense package, registration answers, compliance audit | **The project's strongest asset.** Internally cross-referenced, versioned by date, corrections preserved rather than overwritten — exactly the traceability §5.3 demands. |
| **Research record** | 7 core papers (PDFs) + baseline selection + literature landscape + commercial comparison | Baseline choice is performance-justified with cross-paper numbers and an explicit backbone-confound caveat (R4). Solid. |
| **Third-party material** | `dev/datasets/` — 48MB: full vendored MetaGPT repo, Who&When repo, GAIA, GSM8K, MATH, MBPP+, tau-bench retail | **Hygiene and licensing problem.** Vendored repos and datasets do not belong in git (see change plan). **GAIA is a gated dataset — redistributing it in a public repo likely violates its access terms.** Must be resolved before the repo is ever public. |
| **What does not exist yet** | Any product code: no SDK, no diagnosis engine, no backend, no dashboard, no benchmark | **Correct for proposal stage.** The guide requires a PoC at Gate 1, not an MVP. But be plain about this at defense: 8 spikes, zero product code — the build starts after approval. |
| **Stale/inconsistent** | `dev/README.md` says "TraceCause," "4 real POC scripts," links to a nonexistent `../agent-autopsy/markdowns/`; defense package says "7 spikes" then describes 8 | Fix before defense — small, but a panel that opens the repo sees it first. |

Reconstruction in one paragraph, in plain language (per the prompt's §4): **Granite watches a team of AI agents do a job, and when the job goes wrong — including when the final answer *looks* fine but is wrong — it works out which agent made the first mistake and at which step, proposes a fix, tests the fix by re-running the rest of the job with the fix in place, and only then applies it and resumes, remembering fixes that worked.** "Semantic error" = well-formed but wrong content. "Self-healing" = the diagnose→repair→verify→resume→remember loop. "Verified repair" = no fix is trusted until replay shows it recovers the outcome. "Recovery" = resuming from a checkpoint instead of restarting. Multiple agents are necessary on the *subject* side by definition (the failures being diagnosed are multi-agent failures); on the *tool* side, the multi-stage diagnosis pipeline is inherited from ErrorProbe's published method, and the plan correctly keeps everything that can be deterministic (graph construction, tracing, scoring, constraint checks) out of the LLM.

---

## 3. FAST requirement compliance matrix (extracted from the guide, checked against the repo)

| Guide requirement | Where | Status |
|---|---|---|
| Six connected core elements (research-informed problem → CCP → deployed system → evaluation → documentation → ownership) | Core standard | ✅ all six addressed on paper; ownership traceability is the weak link (V2) |
| Stream declared at proposal | §1.1 | ✅ Stream A, defended against recorded pushback |
| Working deployable system by Final-2, target stated at proposal | §1.2 | ✅ plan §13; honest "not yet producible" flag on deployment evidence is correct |
| SDG/thematic alignment, bounded | §1.3 | ✅ SDG 9, one paragraph, boundary stated |
| CCP with Seoul Accord characteristics | §3 | ✅ 8 clear / 1 weak (stakeholders) — open item |
| Contribution statement in the §4 template | §4 | ✅ verbatim-template compliant |
| One coherent problem; per-member meaningful ownership | §5 | ⚠️ roles defined, **people unassigned** — Gate 1 requires allocation (V2) |
| Committed scope vs optional extensions | §5.1/5.3 | ⚠️ separated, but core inflated on 08-24 (V1) |
| Change control record | §5.3 | ✅ exemplary — reversals recorded, not smoothed |
| Specifiability: 5 FRs, ≥1 measurable NFR, actors, acceptance criterion, one-page architecture | §6 | ✅ all present (FR4 wording needs the V3 fix) |
| AI-resilience test answered | §7 | ✅ plan §5; strengthen with the "what a week-built version gets wrong" list (deliverable 02, Q30) |
| Level-2 AI-assisted development, usage log | §8 | ✅ log maintained and specific |
| Solution landscape incl. commercial products and prior FYPs | §10 | ⚠️ commercial ✅; **departmental prior-FYP check still open** (team-only task) |
| Research-to-decision table | §11 | ✅ |
| Demonstrated PoC at defense | §12 | ✅✅ 8 spikes vs the 1 required — including two honest negatives |
| Testing vs evaluation vs acceptance separated; UAT participants planned | §13/13.1 | ✅ separated; name proxy participants concretely at defense |
| External components classified; nothing core-replacement | §14 | ✅ strongest section of the plan; 15–20% API budget is a committed mechanism, not a label |
| Stakeholder evidence | §B.1 (applied to A via deployable claim) | ❌ **open — the one item nothing in the repo can close** |

---

## 4. The fixes, precisely

### 4.1 Restructure the committed core into two recorded tiers (fixes V1)

Present at defense, and record in the plan doc, as:

**Tier 1 — Diagnosis & verified-repair core (evidence-backed, unconditionally committed):** fault-injection harness · cross-architecture benchmark · Culprit Agent · Error Step Localization · Verification Agent · Semantic Error Diagnostic · Repair Agent · Verified Automatic Repair. Every item has a spike behind it (spikes 1–5, 8).

**Tier 2 — Closed-loop recovery core (committed with pre-registered gates):** Recovery Controller and Verified Repair Memory. Each carries a decision gate at Mid-1, written now, before results are known (which is exactly what §5.3 requires of evaluation-criteria changes):

- *Recovery Controller gate:* a checkpoint/resume PoC on LangGraph (whose native checkpointing makes this the natural first target) demonstrating resume-from-verified-repair-point on ≥1 real workflow by Mid-1; failing that, RC is re-scoped to "resume via controlled replay" (which Tier 1 already provides) and the change is recorded.
- *VRM gate:* re-test of the memory mechanism on a stronger backbone on the same 8 Who&When cases by Mid-1, with pass = ≥1 committed memory and no accuracy regression; failing that, VRM ships as an ablation study ("repair memory: off vs on, and why off won") — an *evaluation contribution* under §4's own table, not a dropped feature.

This is not scope reduction — all 10 items stay committed. It is the difference between a panel discovering the weak evidence and the team presenting it with a decision rule already attached. It also keeps the title honest: "self-healing" is delivered by Tier 1 + RC-as-replay even in the worst case.

### 4.2 Assign owners before Thursday (fixes V2)
Skill-fit inputs are already in the repo (R6). Any defensible mapping beats an empty slide. Record the decision per §5.3.

### 4.3 The wording fix for replay (fixes V3)
Global rename: "deterministic re-execution" → "controlled counterfactual replay." FR4 becomes: *"…the system shall re-execute the downstream portion of the trace under a controlled replay protocol (frozen upstream context; affected steps re-run with pinned decoding parameters) and report whether the corrected trace now succeeds, with recovery rate reported over N replays."* Exact file edits in deliverable 05.

### 4.4 Cost + reproduction band (fixes V4)
One page, before defense: per-case token estimate from Spike 1's real traces × 184 cases × 3 stages; benchmark generation cost at 500 and at 1,000 traces; model plan (cheap/free tier for high-volume generation — Gemini Flash free tier, Groq, student credits; a strong hosted model reserved for the evaluation runs only). Declared band: "reproduction accepted if within ±10 pts of 59.5% on a comparable-class backbone; otherwise both numbers reported, per Annex A.2."

### 4.5 Scope sentence for the Semantic Error Diagnostic (fixes V5)
Adopt verbatim: *"We do not claim to detect arbitrary semantic wrongness. We claim that where the task specification yields machine-checkable constraints — as it does for both of our active substrates — a deterministic verifier catches the well-formed-but-wrong outputs that every anomaly-gated method in this literature, by its own admission, cannot see; and we report the verifier's coverage (abstention rate) so the boundary of the claim is measured, not asserted."* Add **coverage/abstention rate** to the §11 metrics table.

### 4.6 Small consistency fixes
"7 spikes" → "8 spikes" in the defense package; dev/README rewrite; distinguish **Verified Repair Memory** (stores *repair* patterns — Granite's) from **Verified Episodic Memory** (stores *diagnosis* evidence — ErrorProbe's, reproduced only as baseline) everywhere both appear, because a panel that notices the name overlap will ask whether item #10 is just ErrorProbe's memory renamed.

---

## 5. Research-gap and novelty audit (validated, not repeated)

The two claimed gaps were checked against the repo's own literature record and hold:

1. **Cross-architecture generalization** — no paper in the 7-paper corpus evaluates on an architecture outside its own benchmark construction; confirmed at full-text level per the landscape analysis. This is a *real* gap, and it is the right kind for undergraduates: closing it is data engineering + evaluation design (slow, labor-shaped work), not an algorithmic race against labs (§15 of the plan doc argues this correctly).
2. **Silent failures** — ErrorProbe's own Limitations section names this; the gap is confessed, not inferred. The strongest possible provenance for a gap claim.

Novelty decomposition, honestly: **research novelty** = the cross-architecture generalization *measurement* and the silent-failure-augmented pipeline evaluation (moderate, genuine); **technical novelty** = low per-component and correctly disclaimed (plan §4.1 says so plainly — keep that section, it is the best paragraph in the repo); **product novelty** = the closed diagnose→repair→verify→resume loop as an installable SDK (real; the market survey's 7-framework matrix is independent evidence none ship it natively); **data novelty** = the public benchmark (real, and the most durable contribution); **integration novelty** = framework-agnostic instrumentation (real but the compat layer must stay light, as scoped).

Answer to the killer question — *"why can three undergraduates do what seven papers didn't?"* — already exists in the plan and just needs saying crisply: **the papers didn't fail to close these gaps; they didn't attempt them, because both gaps are closed by engineering labor (multi-framework instrumentation, benchmark construction, deployable packaging) rather than by algorithmic insight, and engineering labor is what a three-person year is made of.** The algorithmic core is deliberately *adopted* from the published SOTA, not invented.

---

## 6. Scorecard

| Dimension | Score | Basis |
|---|---|---|
| FAST alignment | **9/10** | Near-total; docked for unassigned ownership and open prior-FYP check |
| Problem significance | **8/10** | Production multi-agent adoption is real; consequence argument concrete |
| Research gap | **8/10** | One confessed gap, one full-text-confirmed gap; crowding risk logged (R7) |
| Novelty | **7/10** | Measurement + benchmark + closed loop; no algorithmic novelty (correctly disclaimed) |
| Technical depth | **8/10** | Graph modeling, causal tracing, replay protocol, evaluation design; docked for the determinism slip |
| Product value | **7/10** | Real category; adoption barrier (instrumentation effort) honestly stated |
| **Feasibility** | **5/10** | The binding constraint: 10-item core + 8 extensions + 2–3 frameworks + reproduction + SDK + dashboard for 3 people. Tiering (§4.1) and extension gating are what keep this from a 4 |
| Evaluation rigor | **8/10** | 9+ metrics incl. false-repair rate and ablations; add coverage metric |
| Dataset availability | **8/10** | Who&When in hand; TracerTraj correctly downgraded after direct check; GAIA redistribution flag |
| Cost | **6/10** | $0 so far (local models) but the strong-backbone reproduction and 500–1,000-trace generation are unpriced (R5 open) |
| Implementation risk | **5/10** | RC (no PoC) and VRM (failed test) in core; reproduction gap; mitigated by gates |
| Differentiation | **7/10** | Narrower than first drafted (LangSmith/Arize convergence) but precise and defensible |
| Presentation strength | **8/10** | After the six fixes; the record-keeping itself will impress a panel |
| Defense readiness | **7/10 → 9/10** | With deliverable 02 rehearsed and V1–V6 applied |

## 7. Residual risks no document can fix

1. **A panel that rejects "yet another LLM-agent project" categorically.** Mitigation is the 0%-API component table and the spikes — but taste risk is real.
2. **Stakeholder characteristic stays weak** if no real contact happens before Thursday. Two structured 20-minute conversations (a faculty member building agents; one local team using CrewAI/LangGraph) close it. This is the single highest-value action remaining.
3. **A team member who cannot explain their subsystem aloud** (§14.1's four questions). The repo cannot help; rehearsal can. Each member should be able to defend one spike end-to-end without notes.
4. **The field publishes past you** (R7). The standing gate-check instruction is the correct mitigation; if it happens, it is reported as a finding, and the benchmark + SDK survive it.

## 8. Prioritized change log

| # | Area | Current state | Change | Reason | Priority |
|---|---|---|---|---|---|
| 1 | Core structure | 10 flat core items incl. 2 with no/failed evidence | Two-tier core + pre-registered Mid-1 gates (§4.1) | Removes the panel's best attack; §5.3-compliant | **Essential** |
| 2 | Ownership | Roles unassigned | Assign names, update plan §9, sketch, slide 10 | Gate 1 hard requirement | **Essential** |
| 3 | Replay wording | "Deterministic re-execution" | "Controlled counterfactual replay" protocol (§4.3) | Technical defensibility | **Essential** |
| 4 | Stakeholders | Characteristic 6 weak | ≥2 recorded stakeholder conversations before defense | Only open CCP characteristic | **Essential** |
| 5 | Cost | R5 open, no number | One-page cost estimate + reproduction band + model plan | Feasibility question is guaranteed | **Strongly recommended** |
| 6 | SED scope | Rule-based claim unbounded | Scope sentence + coverage metric (§4.5) | Pre-empts the trivial-or-impossible attack | **Strongly recommended** |
| 7 | Consistency | 7-vs-8 spikes; stale dev/README; VEM/VRM name collision | Fix per deliverable 05 | Panel-visible polish | **Strongly recommended** |
| 8 | Repo hygiene | 48MB vendored deps; GAIA in git; `.pyc` committed | Datasets out of git; download scripts; licensing check | Legal + professionalism before repo is public | **Strongly recommended** (licensing part: essential before publishing) |
| 9 | Prior FYPs | Unchecked | Department archive check | Guide §10 | **Essential** (team-only) |
| 10 | Extensions | 8 extensions scheduled | No change — already gated correctly | — | Unnecessary to touch |
| 11 | SDK/plugin expansion | SDK is the product boundary | Do **not** add a plugin architecture | Right-sized already; expansion is scope creep | Unnecessary scope — avoid |
