# Granite — Traceability Matrix & Final Consistency Audit

*New document, closing the requirement (proposal-defense audit item #10): confirm use cases match requirements, requirements match architecture, SSDs match use cases, wireframes match functionality, architecture matches implementation, test cases map to requirements, the development plan matches scope, novelty claims match the research work, terminology is consistent everywhere, no document contradicts another, and no functionality is claimed outside the approved scope. Checked once, below, against the real document set — not asserted.*

---

## 1. Requirement → Use Case → Design → Test (full matrix)

| Requirement (SRS) | Use Case | Design element (SDS) | Test (Test Plan) | Tier |
|---|---|---|---|---|
| FR-1.1–1.4 (fault injection, clean controls) | UC-2 | §4 Lane A, §6 `BENCHMARK_CASE` | §4 fault injection, §14 excerpt | Tier 1 |
| FR-2.1–2.5 (attribution) | UC-4 | §4 Lane B, §6 `DIAGNOSIS`, §8 sequence | §4 attribution | Tier 1 |
| FR-3.1–3.5 (silent-failure detection) | UC-5 | §4 Lane B (SED), §6 `SED_VERDICT`, §5 (parallel/unconditional) | §4 SED, §14 excerpt | Tier 1 |
| FR-4.1 (repair generation) | UC-6 | §4 Lane C (Repair Agent), §7 `POST /api/runs/{id}/repair` | §4 repair generation | Tier 1 |
| FR-4.2–4.3 (controlled replay) | UC-7 | §4 Lane C (Verified Automatic Repair), §7 `POST /api/runs/{id}/replay`, §8 sequence | §4 controlled replay, §14 excerpt | Tier 1 |
| FR-4.5 (Recovery Controller) | UC-8 | §4 Lane C (RC, marked Tier 2), §7 `POST /api/runs/{id}/resume` | §4 Tier 2 — Recovery Controller, §14 excerpt | **Tier 2 — gated** |
| FR-4.6 (Verified Repair Memory) | UC-9 | §4 Lane C (VRM, marked Tier 2) | §4 Tier 2 — Verified Repair Memory | **Tier 2 — gated** |
| FR-5.1–5.3 (SDK) | UC-1 | §3 system context (SDK box), §7 API contract | §4 SDK, §5 usability (time-to-integrate) | Tier 1 / Advanced (5.3) |
| FR-6.1–6.4 (data handling, dashboard) | UC-11 | §6 full schema, §7 `GET` endpoints (real, built) | §4 dashboard, data handling | Tier 1 |
| FR-7.1–7.4 (error handling) | *(cross-cutting — all UCs' alt flows)* | §8 sequence `alt` branches, §11 security | §5 availability/failure handling | Tier 1 / Advanced (7.3–7.4) |
| NFR-1 (latency <50%) | — | §12 NFR measurement table | §5 performance | Must |
| NFR-3 / NFR-9 (privacy) | — | §11 security & privacy, §6 `content_redacted` | §6 security testing | Must |
| NFR-7 (replacement test) | — | plan §6 mechanism table | §5 maintainability | Must |

## 2. Use Case ↔ SSD cross-check

| Use case(s) | SSD |
|---|---|
| UC-3, UC-4, UC-5 | SSD-1 — Submit Trace and Receive Diagnosis |
| UC-6, UC-7, UC-8, UC-9, UC-10 | SSD-2 — Generate and Verify a Repair |
| UC-11 | SSD-3 — Review Diagnosis Dashboard |
| UC-1, UC-2 | *(not sequence-diagrammed — single-step setup actions, not multi-hop interactions; correctly out of SSD scope)* |

Every message name on the three SSDs (`submitTrace`, `attributeFailure`, `detectSilentFailure`, `generateCandidate`, `replay`, `resumeFromCheckpoint`, `GET /api/runs`, etc.) corresponds to a requirement above or an endpoint already contracted in the SDS §7 — confirmed by direct comparison, not asserted.

## 3. Wireframe ↔ functionality cross-check

| Wireframe screen | Backs which use case / requirement | Status |
|---|---|---|
| SDK Quick-Start | UC-1, FR-5.1 | **Gap** — genuine, matches SDS §7's own "the one gap that matters most" |
| Project Namespace / API Key | FR-6.3 | Gap, Could-priority (Advanced band) |
| Submit Execution Trace | UC-3, FR-5.2 | **Gap** |
| Diagnosis Running | SSD-1 | **Gap** (loading state for the gap above) |
| Overview (+ empty state) | UC-11, FR-6.4 | **Real, built** — `Overview.tsx` |
| Runs & Diagnoses (+ error state) | UC-11, FR-6.4 | **Real, built** — `RunsList.tsx`, `RunsAggregate.tsx` |
| Run Detail — Trace tab | UC-4, FR-2 | **Real, built** — `GraphView.tsx`, `EvidencePanel.tsx` |
| Run Detail — silent-failure verdict | UC-5, FR-3 | **Real, built** — part of `EvidencePanel.tsx` |
| Run Detail — Repair tab | UC-6, UC-7, FR-4 | **Real, built** — `RepairReplayReport.tsx` |
| Approve / Reject Suggested Repair | UC-10, FR-7.4 | **Gap** — extension #12, not yet built |
| Resume From Verified Repair Point | UC-8, FR-4.5 | **Gap, Tier 2 — gated**, correctly flagged as such |
| Repair Memory reuse/ablation | UC-9, FR-4.6 | **Gap, Tier 2 — gated**, correctly flagged as such |
| POC Evidence | *(supporting evidence, not a numbered use case)* | **Real, built** — `Evidence.tsx` |
| Product & Scope | *(supporting evidence, not a numbered use case)* | **Real, built** — `ProductVision.tsx` |

No wireframe claims a capability outside the SRS's requirement set or the frozen mechanism list (plan §7.0) — every Tier 2 screen carries its gated flag, matching the same discipline already applied everywhere else in this document set.

## 4. Architecture ↔ implementation cross-check

| Architecture element (SDS) | Real code today | Status |
|---|---|---|
| `GET /api/runs`, `/api/runs/{id}`, `/api/stats` | `poc-demo/backend/main.py` | **Real — built and verified** (SDS §7's own marking) |
| `POST /api/runs`, `/repair`, `/replay`, `/resume` | Not yet built | **Genuine gap** — same one the wireframes and use-case model both flag |
| `DiagnosisRun` schema shape | `poc-demo/backend/data_loader.py` | **Real** — the SDS §6 schema is grounded in this proven shape, not speculative |
| 3-screen dashboard (now 5 screens: Overview, Runs, Evidence, Product, Live Demo) | `poc-demo/frontend/src/pages/*` | **Real, built** — the SDS's "3-screen dashboard" language is the plan-doc's original commitment; the shipped console has grown to 5, all consistent with FR-6.4, not a scope violation (evidence and product/vision screens are supporting views, not new committed mechanisms) |

## 5. Novelty claim ↔ research work cross-check

The contribution statement (plan §3–4) claims: cross-architecture generalization (CrewAI + LangGraph, neither used by the 7 surveyed papers) and silent-failure detection via constraint verification. Both claims are the ones the Use Case Model's `«extend»`/`«include»` structure is built around (UC-4/UC-5 as the two `«include»`d, always-run paths; UC-6 extending from *either*), and both are the metrics the evaluation plan (plan §11) and this Test Plan actually measure — no novelty claim in the free-form pitch or slide deck introduces a mechanism absent from plan §7.0's frozen list.

## 6. Terminology consistency, checked

| Term | Used consistently as | Checked across |
|---|---|---|
| Culprit Agent / Error Step Localization / Verification Agent | The three attribution sub-stages (never merged back into one "core attribution algorithm" label, per the 2026-08-23 rename) | Plan §7.0, SDS §4/§8, SRS FR-2, Use Case Model UC-4, SSD-1 |
| Semantic Error Diagnostic (SED) | The constraint-based silent-failure verifier, never called an "anomaly detector" or "LLM judge" | Plan §7.0, SDS, SRS FR-3, Use Case Model UC-5, SSD-1, Wireframes |
| Verified Automatic Repair | The controlled-replay verification stage, distinct from "Repair Agent" (generation) | Plan §7.0, SDS, SRS FR-4.2–4.3, UC-7, SSD-2 |
| Tier 1 / Tier 2 | Evidence-backed-unconditional vs. gated-at-Mid-1, never used loosely as "core vs. extension" | Plan §7.0, SDS, SRS, Use Case Model, both diagrams, Wireframes |
| Verified Repair Memory vs. ErrorProbe's Verified Episodic Memory | Kept explicitly distinct (plan §7.0's own naming-caution note) — never conflated in any new document | SRS FR-4.6, Use Case Model UC-9 |

No document in this new set introduces a synonym or renamed variant for any of the above.

## 7. Scope boundary — no functionality claimed outside approved scope

Cross-checked against SDS §1's exclusion list (multi-tenant auth/billing, message queues, Kubernetes/multi-region, full RBAC, elaborate caching, DR infrastructure beyond stated failure handling) and plan §7.0's frozen mechanism list: **no use case, requirement, SSD, or wireframe in this new document set names a capability from either exclusion list**, and every capability named traces to one of the 10 frozen mechanisms or the extensions plan §7.0 already names (extension #4 namespacing, extension #12 confidence gate).

## 8. Outcome of this audit

Every cross-check above resolved cleanly — no contradiction found between the new documents (Project Vision, Use Case Model + diagram, System Sequence Diagrams ×3, SRS, Test Plan, Software Development Plan, Wireframes) and the existing authoritative set (plan doc, SDS, risk register, cost estimate). Two items are *named as gaps by design*, not found by this audit as defects: the live trace-submission endpoint (`POST /api/runs`) and its operator-facing screens, and the two Tier 2 mechanisms pending their Mid-1 gates — both already disclosed, dated, and fallback-planned everywhere else in this project's documentation.
