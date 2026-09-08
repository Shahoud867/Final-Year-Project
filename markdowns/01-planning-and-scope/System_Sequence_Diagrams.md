# Granite — System Sequence Diagrams (SSDs)

*New document, closing the gap flagged in the proposal-defense audit. These are genuine **black-box** System Sequence Diagrams — Larman's sense: one actor lifeline plus one `:Granite` **system-boundary** lifeline, with the system treated as a single unit receiving "system operations" and returning results. This is deliberately a different abstraction level from [Software_Design_Specification.md](Software_Design_Specification.md) §8's sequence diagram, which opens the box and shows the internal components (SDK, Graph Builder, SED, Tracer, Repair Agent, Recovery Controller, DB) talking to each other. Both are needed and both are consistent — the SDS's diagram is what's inside the single `:Granite` lifeline drawn here.*

One SSD per most-important end-to-end scenario, per the proposal-defense guidance to avoid forcing every interaction into one unreadable diagram.

---

## SSD-1 — Submit Trace and Receive Diagnosis

**Diagram:** [SSD1_Submit_Trace_and_Diagnose.svg](diagrams/SSD1_Submit_Trace_and_Diagnose.svg)

**Covers:** UC-3 (Submit Execution Trace), UC-4 (Attribute Failure), UC-5 (Detect Silent Failure) — FR-2, FR-3, FR-5.2.

**Why this scenario first:** it is the system operation everything else depends on — no repair, no dashboard entry, no evaluation metric exists until a trace has been submitted and diagnosed. It is also the cleanest demonstration of the 0%-API claim (plan §6): every message on this SSD, including both the attribution path and the silent-failure check, is served without a single call to the external LLM API.

**Sequence:** operator submits a raw trace → system builds the execution graph (structural parsing) → system acknowledges receipt → system runs failure attribution and silent-failure detection **in parallel**, the second unconditionally (FR-3.2 — it never waits to see whether the first path found anything) → system returns the combined diagnosis (culprit agent, step, confidence, SED verdict, and the coverage/abstention flag that keeps the SED's claim bounded rather than asserted).

**Alternative flows shown:**
- **Malformed trace** (NFR-6.2) → the system reports an explicit error rather than crashing or silently discarding the submission.
- **Clean control, no fault present** (FR-1.3) → the system reports a `clean_no_fault` status, the path that makes false-positive-rate measurement on healthy runs possible at all — a metric the reviewed literature does not report anywhere.

---

## SSD-2 — Generate and Verify a Repair

**Diagram:** [SSD2_Generate_and_Verify_Repair.svg](diagrams/SSD2_Generate_and_Verify_Repair.svg)

**Covers:** UC-6 (Generate Candidate Repair), UC-7 (Verify Repair via Controlled Replay), UC-8 (Resume From Verified Repair Point, Tier 2), UC-9 (Reuse Stored Repair Pattern, Tier 2), UC-10 (Approve/Reject Suggested Repair) — FR-4.1–4.6.

**Why this scenario second:** it is the one place the two genuinely API-dependent stages of the entire system live (repair-candidate generation, controlled-replay re-execution, plan §6) — and it is the scenario carrying the two Tier 2, gated mechanisms, so the diagram is drawn to make their conditional status visible rather than implied.

**Sequence:** operator requests a repair for an already-diagnosed run → system asks the LLM API for a candidate correction *(or, per the `«extend»` note on the diagram, retrieves one from Verified Repair Memory instead, if a matching pattern exists and that Tier 2 gate has passed)* → system asks the LLM API to replay the candidate under the controlled protocol (frozen upstream context, pinned decoding parameters, N=5 replays) → system computes the recovery rate itself (0% API from this point on) → **three-way branch**, drawn as a single `alt` frame rather than three separate diagrams because the branch condition is what the whole loop's honesty depends on:

1. **Recovery succeeded and the Recovery Controller's Mid-1 gate passed** → resumes from a verified checkpoint (Tier 2 mechanism, as committed).
2. **Recovery succeeded but the gate failed** → resumes via the controlled replay protocol already delivered under Tier 1 — the recorded fallback (plan §7.0), drawn on the diagram itself rather than left to a footnote, so a reader sees the closed loop still closes either way.
3. **Recovery rate below the confidence threshold** → routed to human review (extension #12) rather than auto-applied, with an explicit approve/reject step — the architectural expression of the ethical commitment that diagnosis output is advisory, never autonomous (plan §0.09).

**Alternative flow shown:** LLM API unavailable at either call site → an explicit degraded-state error (NFR-6.1), not a crash.

---

## SSD-3 — Review Diagnosis Dashboard

**Diagram:** [SSD3_Review_Diagnosis_Dashboard.svg](diagrams/SSD3_Review_Diagnosis_Dashboard.svg)

**Covers:** UC-11 (Review Diagnosis Dashboard) — FR-6.4.

**Why this scenario third:** it is the only SSD grounded entirely in already-built, already-verified code — the three system operations shown (`GET /api/stats`, `GET /api/runs`, `GET /api/runs/{id}`) are marked **"Real — built and verified"** in [Software_Design_Specification.md](Software_Design_Specification.md) §7's API contract, not aspirational. Included specifically so the SSD set isn't entirely about not-yet-built repair/recovery mechanisms — the panel should see at least one end-to-end path that is running code today.

**Sequence:** operator opens the dashboard (Overview) → browses filtered runs (Runs & Diagnoses, with the live aggregate across N reproduction runs) → drills into one run's full detail, rendered as the actual shipped components (`GraphView`, `EvidencePanel`, `RepairReplayReport` with its trace/repair tabs).

**Alternative flow shown:** requested run not found → explicit error state with retry, not a blank screen.

---

## Consistency note

Every message name on these three diagrams (`submitTrace`, `attributeFailure`, `detectSilentFailure`, `generateCandidate`, `replay`, `resumeFromCheckpoint`, `GET /api/runs`, etc.) corresponds either to a functional requirement in [Software_Requirements_Specification.md](Software_Requirements_Specification.md) or an endpoint already contracted in [Software_Design_Specification.md](Software_Design_Specification.md) §7 — no message here invents a capability the SRS or SDS doesn't already commit to. Cross-checked in [Traceability_Matrix.md](../02-evidence-and-tracking/Traceability_Matrix.md).
