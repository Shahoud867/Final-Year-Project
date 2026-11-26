# Granite — Software Development Plan

*New document, closing the gap flagged in the proposal-defense audit. Restructured from [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) into the shape a Software Development Plan is expected to take — process, phases, work breakdown, milestones, environment, standards, integration and deployment strategy — rather than a renamed copy of that document. Where a fact below is already established elsewhere, it is cited, not restated with new numbers that could drift.*

---

## 1. Development methodology

**Iterative, gate-driven development**, matching the handbook's own required structure (2 iterations minimum in FYP-1, continuing into FYP-2) rather than a named commercial methodology (Scrum/XP) adopted wholesale. Each iteration:

1. Selects a small set of use cases/mechanisms from the frozen list (plan §7.0).
2. Designs and implements them against the SDS's component/schema/API contracts.
3. Produces a working, demoable increment — not partial code that only compiles.
4. Is tested (per [Test_Plan.md](Test_Plan.md)) before the next iteration starts on top of it.

**Why not a named agile framework verbatim:** the team is 3 people with individually owned, largely independent subsystems (plan §9) — daily standups and sprint ceremonies designed for larger, more interdependent teams would add process overhead without a corresponding coordination need. What's kept from agile practice: short iterations, working software as the measure of progress, and a backlog (the frozen mechanism list, plan §7.0) that is deliberately *not* re-litigated mid-project (§5.3's own change-control rule).

## 2. Development phases

| Phase | Weeks (FYP-1/2) | Content |
|---|---|---|
| **Exploration** | 1–3 | Problem exploration, CCP + contribution statement, risk register opened, one-page architecture sketch |
| **Proposal-stage POC** | 3–5 | 8 real spikes run (exceeding the 1-spike minimum by 8×) — reproduction, instrumentation, injection, silent-failure, controlled replay, cyclic-graph, preventive-classifier, repair-agent feasibility |
| **Gate 1 — Proposal defense** | 5–6 | Scope approved |
| **Requirements & design baseline** | 6–10 | SRS/SDS baselined (this document set), data/licensing cleared, riskiest subsystem (full ErrorProbe reproduction) prototyped, Tier 2 decision gates resolved |
| **Gates 2/3 — Mid-1** | ~10 | Requirements + design baseline reviewed |
| **Core build** | 10–16 | Per-owner build of the 10 foundational mechanisms (§4 below) |
| **Gate 4 — Final-1** | ~16 | Core functional demonstration |
| **FYP-2 continuation** | 1–14 (Sem. 2) | Extensions (13 items, priority-ordered, plan §7.0), non-functional testing, UAT window, documentation completion |
| **Gate 5 — Mid-2 / Final-2** | ~8, ~14–16 (Sem. 2) | Non-functional testing / full documentation + final packaging |

Full week-by-week detail: [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §12 (authoritative; not renumbered here to avoid two documents drifting on the same dates).

## 3. Work breakdown structure

Three lanes, matching committed ownership (plan §9) — each lane's WBS is its owner's subsystem, decomposed to the mechanism level already frozen in plan §7.0:

**Lane A — Data/Benchmark (Shahoud):** framework adapters (CrewAI, LangGraph hooks) → fault-injection operators → benchmark store with ground-truth labels → clean-control generation → benchmark scale-up to 500–1,000 → licensing/release packaging.

**Lane B — Diagnosis (Noor):** trace normalizer → execution graph builder → Semantic Error Diagnostic → backward causal tracer (Culprit Agent + Error Step Localization + Verification Agent) → ErrorProbe reproduction (Strategist/Investigator/Arbiter) → confidence scoring.

**Lane C — Platform (Saif):** Repair Agent → Verified Automatic Repair (controlled replay) → Recovery Controller (Tier 2) → Verified Repair Memory (Tier 2) → backend API → diagnosis record store → 3-screen dashboard → installable SDK → containerized deployment.

**Shared, not owned by any one lane:** architecture/integration decisions, cross-subsystem QA, the ethics/privacy commitments (plan §0.09, risk-register R16), and defense preparation.

## 4. Major milestones and deliverables

| Milestone | Deliverable |
|---|---|
| Gate 1 — Proposal defense | This document set (Project Vision, Use Case Model + diagram, SSDs, SRS, Test Plan, Software Development Plan, wireframes), 10-slide deck, 8 real spike outputs |
| Gate 2/3 — Mid-1 | Walking skeleton (end-to-end, thin), full ErrorProbe reproduction result (honest, whichever side of the acceptance band), Tier 2 gates resolved, benchmark v1 |
| Gate 4 — Final-1 | Core functional: all 8 Tier 1 mechanisms integrated and evaluated under the statistical protocol (plan §11) |
| Gate 5a — Mid-2 | Non-functional testing complete (latency, failure/recovery paths, deployment off the dev machine, threat model actually tested) |
| Gate 5b — Final-2 | UAT + human-baseline study + time-to-integrate measurement; full documentation (SRS, SDS, traceability matrix, handover plan); final packaging |

## 5. Responsibilities / team roles

See plan §9 for the full ownership table and the "if removed, what disappears" test each owner must survive. Restated in one line each: **Shahoud** — data/benchmark, deletion removes the entire cross-architecture evaluation; **Noor** — diagnosis engine, deletion removes the core attribution algorithm and the silent-failure claim; **Saif** — platform, deletion removes the installable product itself.

## 6. Technology stack

| Layer | Choice | Why |
|---|---|---|
| Backend | Python, FastAPI | Team familiarity, fast to build a REST contract against |
| Frontend | React + TypeScript | Already the `poc-demo/frontend` stack; static build serves from the single container |
| Database | PostgreSQL | Relational schema fits the `RUN`/`TRACE_NODE`/`DIAGNOSIS`/... shape exactly ([Software_Design_Specification.md](Software_Design_Specification.md) §6) |
| Orchestration frameworks instrumented | CrewAI, LangGraph | The two committed core architectures (plan §7.0) |
| LLM runtime | Ollama, local | Committed $0 model plan (`cost-estimate.md` §0) |
| Deployment | Docker, single container | Plan §13 — no orchestration platform, no message queue |
| CI | GitHub Actions | Free tier, sufficient at this scale |

## 7. Development environment

Each owner develops locally against Ollama (no shared paid infrastructure required, `cost-estimate.md` §0). A shared `docker-compose` topology mirrors the deployment target ([Software_Design_Specification.md](Software_Design_Specification.md) §10) so integration testing runs against the same container shape before any real deployment.

## 8. Version control, branching, and repository strategy

Single GitHub repository (`Shahoud867/Final-Year-Project`, private), trunk-based with short-lived feature branches per owner's lane, merged back frequently to avoid the multi-week divergence risk already observed once in this project's own history (a 6-commit divergence between two sessions, resolved by merge review rather than force-push — kept as a working example of the discipline this section commits to, not a hypothetical). Branch naming by owner/feature (e.g. `noor`, `saif-recovery-controller`); no direct pushes to the default branch bypassing review once more than one person is actively committing to a shared module.

## 9. Coding standards

Consistent with the guide's own C.14.1 ownership standard (each member must be able to explain, justify, predict breakage in, and modify their own subsystem): per-lane code style follows the language ecosystem default (PEP 8 for Python, the existing ESLint/TypeScript config already in `poc-demo/frontend` for the frontend), with docstrings/comments required on every module implementing a frozen mechanism (plan §7.0) so a reviewer — or a panel member — can trace code back to the requirement it implements without asking the owner first.

## 10. Documentation practices

This document set (Project Vision, Use Case Model, SSDs, SRS, this SDP, Test Plan) is the FYP-1 proposal-stage baseline; the SDS is the working Mid-1-track design reference; the Traceability Matrix ([markdowns/02-evidence-and-tracking/Traceability_Matrix.md](../../../archive/proposal-phase/tracking/Traceability_Matrix.md)) is checked and updated at every gate, not written once and left stale. `AI_Usage_Log.md` records every AI-assisted session per the handbook's own disclosure requirement — a documentation practice already running, not newly proposed.

## 11. Testing integration

Testing is not a phase bolted on after development — [Test_Plan.md](Test_Plan.md) §2's test-first discipline applies to the three modules carrying the actual research claim (SED, causal tracer, replay protocol) from their first iteration, and the regression-set CI check (extension #8) runs on every push once it exists, not only before a gate.

## 12. Integration strategy

Three lanes integrate at two explicit seams (plan §4, SDS §4): Lane A's benchmark output is Lane B's diagnosis input; Lane B's diagnosis output is Lane C's repair input. Each seam is integration-tested in isolation (mocked upstream/downstream) before whole-pipeline system testing, so a defect is localized to one seam rather than requiring all three lanes working simultaneously to debug anything.

## 13. Risk management

Full, live risk register: [risk-register.md](../../../docs/registers/risk-register.md) (37+ entries as of this document). Risk management is not a static section — every risk is dated, has a status, and material risks (backbone-confound in the reproduction, the two Tier 2 gates, dataset availability) carry a pre-registered fallback decided *before* the outcome is known, per §5.3's own discipline. The scope-band descope ladder (plan §7.2) is this plan's risk-management mechanism for schedule risk specifically: a fixed, pre-agreed order in which Advanced-band items are dropped if time runs short, with Core never dropping.

## 14. Dependency management

External dependencies are named and status-tracked in [resources.md](resources.md) and [datasets.md](../../../data/datasets.md), not assumed. The one dependency correction already made on the record: TracerTraj-2.5K was assumed released and confirmed otherwise by direct download attempt, downgrading it from a committed to a conditional dependency (risk-register R11) — kept as the standing example of why this section verifies a dependency directly rather than trusting a citation.

## 15. Deployment strategy

Single Docker container (frontend static build + FastAPI backend + Postgres), deployable to a cloud VM or on-prem host, no orchestration layer (plan §13, [Software_Design_Specification.md](Software_Design_Specification.md) §10). Config/credentials shipped separately from seed trace data. Deployment is exercised as part of Mid-2's non-functional testing gate (§4 above) — "deployment off the dev machine" is a named, tested requirement, not assumed to work because it worked locally.

## 16. Maintenance considerations

Post-FYP maintenance is explicitly out of the graded scope (this is a two-semester academic project, not a maintained product commitment) but the design decisions already taken support it without rework: the 0%-API components pass the replacement test (NFR-7) so a future LLM provider swap doesn't require touching the differentiating logic; the schema and API contract ([Software_Design_Specification.md](Software_Design_Specification.md) §6–7) are versioned artifacts a future maintainer can read without the original team; the benchmark's public release (MIT/CC BY 4.0, plan §14) is designed to outlive the project itself, as a resource other researchers can build on.

## 17. Project timeline

Full two-semester, gate-mapped timeline: [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §12 (authoritative — this document does not restate the week-by-week detail to avoid two copies drifting apart). Effort budget headline: ~1,130 plannable person-hours (FYP-1 ≈490h, FYP-2 ≈640h), full breakdown in `06_Expanded_Scope_and_Feasibility_Plan.md` §5.1.

---

*This document introduces no process, phase, or milestone beyond what [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) and [Software_Design_Specification.md](Software_Design_Specification.md) already commit to — it exists to present that commitment in Software-Development-Plan form for the proposal-defense package, not to add new scope.*
