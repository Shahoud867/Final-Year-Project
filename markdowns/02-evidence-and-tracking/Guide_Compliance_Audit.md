# Granite — Full Sub-Part Compliance Audit vs. FAST FYP Guide (all 30 pages, all 17 sections + Annex A/C)

*Deeper pass than the section-level check in the plan doc — this goes into each section's own sub-tables and sub-bullets, not just the top-level heading. New gaps found in this pass are marked **NEW**.*

---

## §1.1 Two Entry Points

Stream A declared (plan doc header). Per the guide's own table: starting point = published research (ErrorProbe) ✓; where the gap comes from = a stated limitation in published work (ErrorProbe's own admitted silent-failure blind spot, plus the confirmed cross-paper generalization gap) ✓; primary risk = "can it be reproduced within our resources" — tested directly via spike 1, real number in hand ✓.

## §1.2 Working, Deployable System — sub-table, item by item

| Sub-item | Status |
|---|---|
| Runs outside dev machine | Planned (architecture-sketch.md), not yet built — expected pre-Final-1 |
| Realistic operating environment | Stated: containerized, cloud VM or on-prem (plan doc §13) |
| Configuration and data | Planned: seed data separate from secrets |
| Non-functional behavior | 1 measurable NFR now stated (§0.07): diagnostic overhead % |
| Failure and recovery | Planned: LLM API down, malformed trace behavior documented in §13 |
| Handover | Planned: licenses, limitations, future work listed in §13 |
| Adoption context | Stated: client identified §0.06, honest barrier (integration effort) already disclosed |
| **Evidence of deployment** | ❌ **Not possible yet — nothing is deployed.** Expected at this stage, not a current gap, but flag for Final-1: a screenshot/record of an actual running deployment is owed, not just the plan |

## §1.3 SDG/Thematic Alignment
Done — §0.05, SDG 9, one paragraph, not expanded beyond context. ✓

## §2 R&D Embedded — sub-table

Solution landscape ✓ (Full_Literature_Landscape_Analysis.md + Commercial_Product_Comparison.md). Technical foundation ✓ (7 papers read in full, 3 more triaged). Reproduction/adaptation/experimentation ✓ (8 spikes). Evaluation and learning ✓ (§11 evaluation plan). All four R&D elements have proposal-stage evidence, not just assertions.

## §3 CCP — all 9 characteristics
8/9 clear, #6 (diverse stakeholders) open pending real contact. Unchanged from prior checks, still accurate.

## §4 Contribution — type + statement
Contribution types mapped: data/resource (benchmark), method (silent-failure + generalization), system/architecture (SDK) — §3 of plan doc. Contribution statement follows the guide's exact template ("Existing approaches perform X... we will contribute Z... evaluate using B"). ✓

## §5 Scope — sub-table + scope sufficiency questions

| Scope principle | Status |
|---|---|
| One shared central problem | ✓ — all 3 roles trace back to the same ErrorProbe delta |
| Meaningful primary ownership | ✅ **Closed 2026-08-25 — assigned and recorded** (R24, supersedes R6): Shahoud Shahid — Data/Benchmark, Muhammad Noor — Diagnosis Engine, Saif Shahzad — Platform. Moved ahead of its old "before Mid-1" target because the guide's Gate 1 row requires ownership allocated to each member *at the proposal defense*, making the deferral a hard requirement miss at the defense itself |
| Interdependent work | ✓ — pipeline hops are sequential/dependent (architecture-sketch.md) |
| Shared engineering responsibilities | ✓ — evaluation (core item 7) is explicitly collective |
| Balanced depth, not identical tasks | ✓ — 3 distinctly different subsystems |
| Evolving division of work | Not yet tested — no reallocation has happened, nothing to evolve yet |

**Scope sufficiency questions** (6): **all six now answerable.** The previously-failing one — *"does each member have a defensible technical role"* — was undermined only by the missing ownership assignment, which closed on 2026-08-25 (R24). Each named owner's lane maps to a distinct contribution type and to spikes they can walk through; what remains is rehearsal, not a documentation gap.

### §5.1 Five gates — done, plan doc §12, updated with real evidence
### §5.2 Client — done, §0.06
### §5.3 Change control table — actively demonstrated (R7 decision, GraphTracer/FALAT correction, AgentRx removal) — genuinely the strongest-evidenced sub-section in the whole project

## §6 Specifiability — sub-table
5 functional reqs ✓, 1 measurable NFR ✓, actors/data ✓, acceptance criterion for hardest req ✓, architecture on one page ✓ (§0.07 + architecture-sketch.md). **Minor, cosmetic gap**: the guide's exact "one-sentence vagueness test" format (*"The system shall X for actor Y, and we will know it works when Z"*) wasn't used verbatim — the content exists but not fused into that single compound sentence. Not worth a full section, but easy to tighten: *"The system shall flag a silent failure for the operating engineer, and we will know it works when the flagged step matches the fault-injection harness's ground-truth injection point."*

## §7 AI-Resilience Test — done, plan doc §5
## §8 AI-Assisted Development — 8.1-8.4, all sub-parts
Own-vs-assist boundary respected throughout (architecture-sketch.md's API-usage budget table is the concrete enforcement mechanism). AI_Usage_Log.md covers ideation, coding, debugging, documentation, with per-entry verification status — this is the most thoroughly executed section in the whole audit. ✓✓

## §9 Disciplined Idea-Discovery — all 11 steps
Every step has a corresponding artifact (literature review, gap verification, CCP formulation, contribution definition, technical-approach comparison, POC, evaluation definition, scope/ownership shaping, stress-testing via commercial comparison, SDG check). ✓

## §10 Product/Prior-FYP/Workflow Comparison
Commercial half ✓✓ (Commercial_Product_Comparison.md §1–3, 7 platforms). **Prior-FYP half closed 2026-09-06** (R39, Commercial_Product_Comparison.md §4) — closest match `S24-011-D-HDLM` ("Hallucination Detection in Language Model Textual Responses," Spring 2024), found via a full scan of the department's own FYP archive. Current-workflow comparison ✓ (Slide 2 of defense package). The guide's warning that platform/language/UI changes alone don't constitute differentiation — correctly not relied upon; the differentiation is substantive (silent-failure detection + counterfactual testing + proven generalization), and the prior-FYP comparison itself makes the "single LLM vs. multi-agent system" distinction explicit, per that same warning.

## §11 Research-to-Decision Table — done, §0.08

## §12 Proposal-Stage POC — sub-table, checked against actual risk categories

| Guide's risk category | Covered? |
|---|---|
| Data availability/quality | ✓ — Who&When, MBPP+, GSM8K, tau-bench all directly verified |
| Algorithm/model feasibility | ✓✓ — spikes 1, 4, 5, 6, 7 |
| System/integration feasibility | ✓ — spike 2 |
| Hardware/IoT feasibility | N/A — not an IoT project |
| **Security/privacy feasibility** | ✅ **Resolved 2026-08-23** — threat model written and logged in risk-register.md R16: 3 data categories identified, minimum-context-per-call to the LLM API, 3 committed mitigations (redaction, namespacing, retention limits). Not yet independently reviewed by the team. |
| Human/workflow feasibility | ⚠️ Partial — this is effectively what stakeholder contact (I2) would provide, still open |
| Deployment feasibility | ⚠️ Partial — target stated, not yet tested |

**This is the one real, substantive gap this deeper pass surfaced that the section-level check missed.** Recommend at minimum a one-paragraph threat model before defense: what data the SDK touches, what's sent to the LLM API, what's stored, and the one obvious risk (trace data potentially containing customer PII from the retail scenario) with a stated mitigation (e.g., no PII fields retained beyond the diagnosis window, or a redaction step before storage).

## §13 Evaluation Plan — sub-table + 13.1
Evaluation question table ✓ (plan doc §11). 13.1's three-way split (testing/evaluation/acceptance) explicitly maintained. User acceptance testing plan exists; execution is correctly FYP-2 work, not expected now.

## §14 External Components — sub-table + 14.1 + dependency questions
Category table ✓✓ (architecture-sketch.md, unusually rigorous with the API-usage budget). 14.1's four-part ownership test — **still the open "explain out loud" item**, same as before, not new. Dependency questions (5): 4 of 5 answered; "can the group explain and modify the surrounding design" is pending the same team verification.

## §15 Weak Idea Patterns — spot-checked against all 11 rows
No pattern present: not a routine CRUD portal, not a bare chatbot wrapper, has a real evaluated baseline (not model-training-with-no-baseline), not a local copy, understanding is demonstrated (not blind reproduction), integration is coherent (not independent weak modules), academic rigor exists alongside product framing (not industry-delivery-only), SDG is connected not decorative, difficulty isn't just code volume, has a real system not just a notebook, has research basis not just an app, deployment is planned not dev-machine-only. ✓ Clean across all 11.

## §16 Proposal Defense Package — done, separate file
## §17 Final Checklist — done, plan doc's closing section, includes the honest opens

---

## Net new findings from this deeper pass

1. **Security/privacy feasibility (§12) — genuinely missing, not previously flagged.** The most substantive finding in this audit. *(Since resolved — threat model written 2026-08-23, risk-register R16.)*
2. **§6's one-sentence vagueness-test format** — cosmetic, content exists but not fused into the guide's exact compound-sentence form.
3. Everything else confirms or restates already-known opens (stakeholder contact, role assignment, explain-out-loud) — no other new gaps at this finer granularity. Prior-FYP check closed 2026-09-06 (R39), no longer on this list.

---

## Re-audit, 2026-08-25 — independent pre-defense pass

*A second, independent audit against the full guide was run three days before the defense; its verdict and full working are in [`01_Executive_Audit_and_Verdict.md`](../../01_Executive_Audit_and_Verdict.md) at the repository root. It found six vulnerabilities, all now applied and recorded in risk-register.md R23–R26. What changed against the rows above:*

| Item | Was | Now |
|---|---|---|
| Meaningful primary ownership (§5) | ⚠️ Roles defined, nobody assigned (R6) | ✅ **Closed** — assigned and recorded (R24). This was the audit's most concrete compliance finding: the guide's Gate 1 row requires ownership allocated *at the proposal defense*, so "before Mid-1" was a hard miss, not a pending task |
| Committed scope vs. extensions (§5.3) | ✅ Separated | ✅ Separated **and tiered by evidence**, with pre-registered Mid-1 gates on the two items carrying the weakest evidence (R23) |
| Specifiability — FR4 (§6) | ✅ Present, but promised *deterministic* re-execution of an LLM workflow | ✅ Corrected to **controlled counterfactual replay** (R25) — the protocol is deterministic, LLM-step variance is measured. The prior wording was technically indefensible |
| Evaluation plan (§13) | ✅ Metrics defined | ✅ Plus **silent-failure coverage/abstention rate**, and a **pre-registered reproduction acceptance band** with an Annex A.2 fallback |
| Feasibility — cost (§12) | ⚠️ R5 open, no number attached | ✅ **Quantified** from measured token counts across all 184 Who&When cases — cost-estimate.md (R26) |
| POC count (§12) | Recorded inconsistently as 4 / 7 / 8 across documents | ✅ **8 spikes**, stated consistently everywhere |

**Still open after this pass, and not closeable by any document** — these are the honest residuals to state at the defense rather than paper over:

1. **Real stakeholder contact** (I2) — CCP characteristic #6 stays at 8/9 until it happens. The single highest-value remaining action.
2. ~~**Prior-departmental-FYP comparison**~~ — **Closed 2026-09-06** (R39): closest match `S24-011-D-HDLM` (Spring 2024), found via the department's own archive. `Commercial_Product_Comparison.md` §4.
3. **"Explain your subsystem out loud, no notes"** (§14.1) — rehearsal, not documentation. Each owner should be able to walk one spike end-to-end unaided.
4. **Deployment evidence** (§1.2) — correctly not producible at proposal stage; owed by Final-2.
