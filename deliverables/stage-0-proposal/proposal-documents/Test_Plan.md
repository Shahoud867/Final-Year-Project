# Granite — Test Plan

*New document, closing the gap flagged in the proposal-defense audit. Distinct from — and consistent with — [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §11's evaluation plan: that section answers "is the diagnosis engine any good against ErrorProbe" (an **evaluation** question, per the handbook's C.13.1 three-way split already logged in that section); this document answers "does the implemented system behave as specified" (a **testing** question) — and separately names the **acceptance** track, so all three of C.13.1's questions have their own evidence plan rather than one document standing in for all three.*

---

## 1. Testing objectives

1. Verify every **Must**-priority functional requirement in [Software_Requirements_Specification.md](Software_Requirements_Specification.md) §3 behaves as specified, including at its stated edge and failure cases.
2. Verify the non-functional requirements (§4 of the SRS) that are testable pre-deployment (latency overhead, recovery-rate variance reporting, redaction, the 0%-API replacement test).
3. Produce a defect record with severity, not just a pass/fail count — so the panel and the team can see *what kind* of problems were found, not only how many.
4. Demonstrate that the project is **measurably evaluated**, not merely demonstrated — every metric in the evaluation plan (plan §11) has a corresponding test or measurement procedure named here, not left implicit.

## 2. Testing strategy

A layered strategy matching the system's own layering ([Software_Design_Specification.md](Software_Design_Specification.md) §4's three owner lanes): unit tests inside each lane, integration tests across lane boundaries (the points where Lane 1's benchmark feeds Lane 2's diagnosis, and Lane 2's diagnosis feeds Lane 3's repair), system tests against the full pipeline end-to-end, and acceptance testing with real or proxy users — tracked as a separate track per §13.1, not folded into system testing.

**Test-first discipline, scoped honestly:** given the project's effort budget (plan §7.2, ~1,130 person-hours across two semesters), test-driven development is not committed for every module; it *is* committed for the three modules whose correctness is the actual research claim — the Semantic Error Diagnostic's constraint checker, the backward causal tracer, and the controlled-replay protocol's step-selection logic — because a bug in any of these three silently invalidates a headline metric rather than crashing visibly.

## 3. Test levels

| Level | Scope | Owner |
|---|---|---|
| **Unit** | Individual functions/classes: graph-construction parser, SED constraint checker, confidence-scoring formula, fault-injection operators, SDK trace-normalizer | Whichever lane owns the module (plan §9) |
| **Integration** | Lane boundaries: benchmark → diagnosis input; diagnosis output → repair input; repair/replay output → record store; record store → dashboard | Cross-lane, shared responsibility (plan §9 "shared across all three") |
| **System** | Full pipeline, SSD-1/SSD-2/SSD-3 scenarios end-to-end ([System_Sequence_Diagrams.md](System_Sequence_Diagrams.md)) against real and synthetic traces | Whole team |
| **End-to-end** | SDK install → submit trace → diagnosis → repair → replay → dashboard, on a workflow neither owner has seen before (dogfooding one another's frameworks) | Whole team, before each gate |
| **Acceptance** | Real/proxy operator installs the SDK against their own workflow (plan §11 UAT window) | Whole team, Mid-2 plan / Final-2 evidence, per C.13.1 |

## 4. Functional testing

| Test area | What's checked | Requirement(s) |
|---|---|---|
| Fault injection | Injected fault matches the declared operator; ground truth recorded before diagnosis runs; clean-control generation actually disables injection | FR-1.1–1.3 |
| Attribution | Predicted agent/step returned for every submitted trace with a failure; confidence computed from graph features, never from an LLM self-report | FR-2.1–2.3 |
| Verification Agent | A hypothesis that contradicts real trajectory evidence is rejected, not passed through | FR-2.4 |
| Semantic Error Diagnostic | A known-wrong value (including the plausible near-miss case, $20.00 vs $19.75, already validated in Spike 4) is flagged; a case with no checkable constraint is abstained, not guessed | FR-3.1–3.5 |
| Repair generation | A candidate is produced for a localized, verified failure; no candidate is generated for a clean-control trace | FR-4.1 |
| Controlled replay | Recovery rate reported over exactly N=5 replays with variance, never a single-run point estimate; non-LLM computation in the replay is bit-identical across runs (R25) | FR-4.2–4.3 |
| Tier 2 — Recovery Controller | Resume-from-checkpoint demonstrated on ≥1 real LangGraph workflow, **or** the recorded replay-based fallback is exercised instead | FR-4.5, plan §7.0 gate |
| Tier 2 — Verified Repair Memory | Re-test on stronger backbone commits ≥1 memory entry with no accuracy regression, **or** the memory-on/off ablation is exercised instead | FR-4.6, plan §7.0 gate |
| SDK | Installs against a CrewAI *and* a LangGraph workflow without modification to the diagnosis algorithm; normalizes a raw trace correctly | FR-5.1–5.2 |
| Data handling | PII redaction applied before any persistence; no code path stores unredacted content | FR-6.2 |
| Dashboard | Overview/Runs/Product screens render live data from `/api/stats`, `/api/runs`, `/api/runs/{id}` | FR-6.4 |
| Error handling | Explicit, distinguishable responses for: LLM unavailable, malformed trace, cyclic graph past its bound, low-confidence repair routed to human review | FR-7.1–7.4 |

## 5. Non-functional testing

| NFR | Test approach |
|---|---|
| **Performance (NFR-1)** — diagnostic latency overhead <50% | Timestamp wrapped around the full diagnosis pipeline call; measured as a percentage of the target workflow's own execution time, across the benchmark set, reported with a distribution not a single number |
| **Reliability (NFR-2)** — recovery-rate variance reported | Assert every replay report includes N, mean, and variance/CI fields — a test that fails loudly if a future change silently drops the variance report back to a point estimate |
| **Security / privacy (NFR-3)** | Static check: no code path writes `TRACE_NODE` without passing through the redaction function first; a test trace containing a synthetic email/phone pattern is confirmed absent from the persisted record |
| **Scalability (NFR-4)** | Load the full 500–1,000-trace benchmark through the pipeline once per evaluation checkpoint; confirm no architectural failure at that scale (not a formal load-test against concurrent users — out of scope at FYP deployment scale) |
| **Usability (NFR-5)** | WCAG contrast check on dashboard status colors (owed by Final-1, plan §0.09); time-to-integrate measured directly during the UAT window (target median <30 min) |
| **Availability / failure handling (NFR-6)** | Fault-inject the *test harness itself*: kill the LLM API mid-call, submit a deliberately truncated trace, submit a trace from an unexpected framework shape — confirm each produces the documented error state, not a stack trace to the operator |
| **Maintainability / replacement test (NFR-7)** | Swap the configured LLM provider/model and re-run every 0%-API component (graph construction, SED, causal tracing, confidence scoring); assert byte-identical output — this is the literal test of plan §6's "replacement test," not just an architectural claim |
| **Compatibility (NFR-8)** | SDK installed against both committed frameworks (CrewAI, LangGraph) in CI; extension #8's compatibility layer tested for successful trace parsing (not full benchmarking) against the remaining 5 surveyed frameworks, if reached |
| **Cost (NFR-10)** | Confirm the full evaluation run completes on local Ollama with $0 spend recorded, per `cost-estimate.md` §0 |

## 6. Security testing

Scoped to what's actually committed (no auth/RBAC/billing system is built, [Software_Design_Specification.md](Software_Design_Specification.md) §1): (1) redaction-before-storage verified as above; (2) per-project namespacing (extension #4) tested for cross-namespace leakage — a query scoped to project A must never return project B's runs; (3) no hard-coded secrets — a CI grep step fails the build on a committed API key pattern. Full threat model: risk-register.md R16.

## 7. Performance testing

Diagnostic latency overhead (NFR-1) is the one measurable NFR the handbook requires (plan §0.07) and is measured as described in §5 above. A cost–latency frontier (Advanced band, plan §7.2) plots this trade-off across the single-pass vs. full-pipeline diagnosis modes (extension #6), reported if that extension is reached.

## 8. Usability testing

Folded into the acceptance track (§10 below) rather than duplicated — usability is measured *on real or proxy users*, not asserted from internal review, per the handbook's own distinction between testing and acceptance (C.13.1).

## 9. Testing techniques

| Technique | Where used |
|---|---|
| Black-box / specification-based | Every functional requirement in §4 above — tested against its stated input/output, not its implementation |
| White-box / structural | The three test-first modules named in §2 (SED, causal tracer, replay protocol) — branch and constraint coverage inside the module |
| Boundary-value analysis | Confidence-score thresholds (extension #12's approve/reject gate), the ±10-point reproduction acceptance band, the 5-minute-per-trace UAT cap |
| Equivalence partitioning | Fault types (corrupted tool output, communication corruption, context truncation) each tested as one representative case per partition, not exhaustively |
| Regression testing | One GitHub Action (extension #8) re-runs the evaluation suite against a fixed regression set on every push, failing the build if step accuracy drops below a stated threshold |
| Mutation / negative testing | Clean-control traces (fault injection disabled) used specifically to measure false-positive rate — the literature's own blind spot this project measures where others don't (plan §11) |

## 10. Test environments

| Environment | Purpose |
|---|---|
| **Local development** | Each owner's machine, running local Ollama — $0, matches the committed model plan (`cost-estimate.md` §0) |
| **CI (GitHub Actions)** | Runs unit + integration tests and the regression-set evaluation on every push (extension #8) |
| **Staging / single-container** | The actual deployment target topology (Docker, one container, [Software_Design_Specification.md](Software_Design_Specification.md) §10) — used for system and end-to-end tests before any UAT session |
| **UAT session environment** | A proxy participant's own machine, installing the SDK fresh — deliberately *not* a pre-configured dev environment, since time-to-integrate is itself the metric being measured |

## 11. Test data

- **Who&When** (184 real cases, MIT license, in hand) — baseline reproduction and regression testing.
- **The project's own cross-architecture benchmark** (target 500–1,000 traces, 15–20% clean controls) — the primary system/functional test corpus once generated.
- **8 real POC spike outputs** (already on disk, `dev/spikes/poc/`) — used as a known-good regression fixture: any future change that alters these specific recorded outcomes without an explained reason is a signal worth investigating, not proof of a regression by itself (spike outputs are real single/few-run results, not a guaranteed-stable oracle).
- **Synthetic edge-case traces**, authored specifically for this test plan: empty trace, single-agent trace, malformed tool output, a cyclic graph past the max-revisit bound, a trace from an unexpected framework shape.

## 12. Entry / exit criteria

| Gate | Entry criterion | Exit criterion |
|---|---|---|
| Unit testing | Module compiles/runs standalone | All Must-priority requirements for that module pass; defects triaged (§13) |
| Integration testing | Both sides of a lane boundary have passing unit tests | Data crosses the boundary in the schema-contracted shape ([Software_Design_Specification.md](Software_Design_Specification.md) §6/§7) with no silent field loss |
| System testing | All three lanes integrate without a build failure | SSD-1/SSD-2/SSD-3 scenarios each complete end-to-end, including their alternative/error flows |
| Mid-1 (Gate 2/3) | Walking skeleton exists (plan §7.2) | Tier 2 decision gates resolved one way or the other (plan §7.0), each with real evidence, not a promise |
| UAT / acceptance | System testing exit criteria met | Acceptance round completed with named participants, method, tasks, issues, and a recorded outcome (§13's acceptance table format) |

## 13. Defect handling

Every defect recorded with: severity (**Blocker** — breaks a Must-priority requirement or corrupts data; **Major** — breaks a Should-priority requirement or a non-crashing but wrong result; **Minor** — cosmetic or Could-priority), the requirement ID it violates, reproduction steps, and status (open/in-progress/fixed/deferred with reason). Blockers must be resolved before the next gate; Majors are triaged at each gate review; Minors may be deferred to FYP-2 if named explicitly, never silently dropped.

## 14. Requirement → test traceability (excerpt)

*Full matrix: [Traceability_Matrix.md](../../../archive/proposal-phase/tracking/Traceability_Matrix.md). Sample below shows the mapping pattern.*

| Requirement | Test(s) | Level |
|---|---|---|
| FR-3.1 (silent-failure flagging) | Known-wrong-value case (incl. $20.00/$19.75 near-miss); clean-control case (must NOT flag) | Unit + system |
| FR-4.3 (recovery rate over N replays) | Assert N=5, variance field present; Spike 5's 97.2→108.0 case re-run as a regression fixture | Unit + regression |
| NFR-7 (replacement test) | LLM-swap test across all 0%-API components, byte-identical output assertion | Integration |
| FR-4.5 (Tier 2 — Recovery Controller) | LangGraph checkpoint/resume PoC (pass) OR replay-fallback exercised (fail path) | System, gated at Mid-1 |

## 15. Evaluation metrics and expected evidence (cross-reference, not a duplicate)

The metrics that answer "is the diagnosis engine any good" (agent/step accuracy, propagation-path F1, silent-failure precision/recall/coverage, recovery rate, task completion rate, repair success rate, false repair rate) belong to the **evaluation** track, already fully specified in [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §11 — restated here only as a pointer, per this document's own discipline against duplicating a document that already has one authoritative version. What this Test Plan adds on top: the **pass/fail testing criteria** (does the system compute and report these metrics correctly, with the required N/variance/coverage fields present) — a testing question, distinct from whether the resulting numbers are *good*.

---

*Consistent with plan §11's own three-way split (Testing / Evaluation / Acceptance, per handbook C.13.1): this document is the Testing track in full; Evaluation is plan §11; Acceptance is the UAT protocol already named there and restated in §10 above as a distinct test environment, not folded into system testing.*
