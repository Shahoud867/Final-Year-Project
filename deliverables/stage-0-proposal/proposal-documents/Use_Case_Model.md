# Granite — Use Case Model

*New document, closing the gap flagged in the proposal-defense audit. Every use case below traces to a functional requirement in [Software_Requirements_Specification.md](Software_Requirements_Specification.md); every actor and mechanism traces to [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §0.07/§6/§7.0. Diagram: [Use_Case_Diagram.svg](diagrams/Use_Case_Diagram.svg).*

---

## 1. Actors

| Actor | Kind | Description |
|---|---|---|
| **Engineering-Team Operator** | Primary, human | The system's notional client (plan §0.06): the person running Granite against their own multi-agent system — installs the SDK, submits traces, reviews diagnoses, approves or rejects suggested repairs, browses the dashboard |
| **Multi-Agent System Under Test** | Secondary, non-human | The CrewAI or LangGraph workflow being instrumented and diagnosed. It never *uses* Granite — it is the subject Granite observes |
| **LLM API** | External system, Core-assist only | Supplies agent-under-test behavior, Repair Agent generation, and controlled-replay re-execution. Deliberately excluded from every use case that carries Granite's actual differentiating claim — the diagram's clean separation of which use cases touch this actor and which don't *is* a visual proof of the 15–20% API-dependence budget (plan §6) |

## 2. System boundary

Everything inside the "Granite" boundary in the diagram is delivered by this project. The target multi-agent system's own internals, the LLM provider's infrastructure, and any trace-capture platform the operator already runs (LangSmith, Langfuse, etc.) are explicitly outside the boundary — Granite is a diagnosis layer that sits on top of that category, not a replacement for it (per the positioning already established in `Commercial_Product_Comparison.md`).

## 3. Use cases

| ID | Use case | Actor(s) | Requirement | Tier |
|---|---|---|---|---|
| UC-1 | Install SDK Against Target Workflow | Operator | FR-5.1 | Tier 1 |
| UC-2 | Generate Fault-Injection Benchmark | Operator, Multi-Agent System Under Test | FR-1.1–1.4 | Tier 1 |
| UC-3 | Submit Execution Trace for Diagnosis | Operator, Multi-Agent System Under Test | FR-5.2 | Tier 1 |
| UC-4 | Attribute Failure (Culprit Agent + Error Step Localization + Verification Agent) | *(system-internal, invoked via UC-3)* | FR-2 | Tier 1 |
| UC-5 | Detect Silent Failure (Semantic Error Diagnostic) | *(system-internal, invoked via UC-3)* | FR-3 | Tier 1 |
| UC-6 | Generate Candidate Repair | LLM API | FR-4.1 | Tier 1 |
| UC-7 | Verify Repair via Controlled Replay | LLM API | FR-4.2–4.3 | Tier 1 |
| UC-8 | Resume From Verified Repair Point | *(system-internal)* | FR-4.5 | **Tier 2 — gated** |
| UC-9 | Reuse Stored Repair Pattern | *(system-internal)* | FR-4.6 | **Tier 2 — gated** |
| UC-10 | Approve / Reject Suggested Repair | Operator | FR-7.4 | Advanced (ext #12) |
| UC-11 | Review Diagnosis Dashboard | Operator | FR-6.4 | Tier 1 |

## 4. Use case descriptions

**UC-1 — Install SDK Against Target Workflow**
*Actor:* Operator. *Precondition:* the operator has a CrewAI or LangGraph workflow and permission to instrument it. *Main flow:* operator installs the documented SDK; SDK hooks into the target workflow's execution without requiring modification to Granite's own diagnosis algorithm. *Postcondition:* the workflow is instrumented and ready to submit traces.

**UC-2 — Generate Fault-Injection Benchmark**
*Actors:* Operator (triggers), Multi-Agent System Under Test (executes the task under injection). *Main flow:* operator selects a fault-injection operator (e.g., corrupted tool output); harness runs the target workflow, injects the fault deterministically, records ground-truth agent/step at injection time. *Alternative flow:* injection disabled → produces a "clean control" trace instead, for false-positive-rate measurement (FR-1.3). *Mechanism:* 0% API — rule-based, deterministic corruption (plan §6).

**UC-3 — Submit Execution Trace for Diagnosis**
*Actors:* Operator (triggers via SDK), Multi-Agent System Under Test (produces the raw trace). *Main flow:* SDK normalizes the raw trace and submits it (`POST /api/runs`); this **always** invokes UC-4 and UC-5 (`«include»`) — both run on every submitted trace, in parallel, per FR-3.2's "unconditional" requirement.

**UC-4 — Attribute Failure**
*Included by UC-3.* Builds the execution graph (structural parsing, 0% API), runs the Strategist-stage hypothesis of which agent/step is responsible, and confirms it against real trajectory evidence before it's trusted (Verification Agent). *Output:* culprit agent + step + confidence score, computed from graph features, never from an LLM asked to self-report confidence.

**UC-5 — Detect Silent Failure**
*Included by UC-3, runs in parallel with UC-4.* Checks the output against the task's machine-checkable constraints; flags a well-formed-but-wrong output even where no explicit anomaly signal exists. *Abstains* rather than guesses where no checkable constraint exists, reporting the abstention as a coverage metric (FR-3.4).

**UC-6 — Generate Candidate Repair**
*Extends UC-4* (extension point: a failure was attributed) *and extends UC-5* (extension point: a silent failure was flagged) — repair generation fires from either trigger, not only the attribution path. *Actor:* LLM API (repair-candidate generation is one of the two genuinely API-dependent stages, plan §6). *Extended by UC-9* when a matching pattern already exists in the Verified Repair Memory (Tier 2) and its Mid-1 gate has passed.

**UC-7 — Verify Repair via Controlled Replay**
*Sequential flow from UC-6* (a candidate must exist before it can be verified — a plain pipeline dependency, not a UML include/extend, since verification is not optional once a candidate exists — see §5's note on why this isn't stereotyped). *Actor:* LLM API (re-execution of the corrected step). Re-executes the downstream trace under a controlled replay protocol (frozen upstream context, pinned decoding parameters) and reports recovery rate over N replays — never inferred from one replay (R25). *Extended by UC-8* when the repair succeeds and the Recovery Controller's gate has passed. *Extended by UC-10* when the recovery rate falls below the confidence threshold.

**UC-8 — Resume From Verified Repair Point** *(Tier 2 — gated)*
*Extends UC-7.* Resumes execution from a checkpoint at the verified repair point, rather than restarting the whole workflow. **Gate status (plan §7.0):** demonstrated only if the Mid-1 LangGraph checkpoint/resume PoC passes; if it fails, the recorded fallback is resumption via the controlled replay protocol UC-7 already delivers — the closed loop still closes, only the *mechanism* changes.

**UC-9 — Reuse Stored Repair Pattern** *(Tier 2 — gated)*
*Extends UC-6.* Stores and retrieves successful error→diagnosis→repair patterns for similar future failures. **Gate status (plan §7.0):** demonstrated only if the Mid-1 stronger-backbone re-test commits ≥1 memory entry with no agent-accuracy regression; the one real prior test **failed** (0/8 cases committed, accuracy regressed 75%→50%) — if the re-test fails again, the recorded fallback is a memory-on/memory-off ablation study, reported as a legitimate evaluation contribution rather than a silently dropped feature.

**UC-10 — Approve / Reject Suggested Repair**
*Actor:* Operator. *Extends UC-7* (extension point: recovery rate is below the confidence threshold, extension #12). Diagnosis output is advisory, never autonomous (plan §0.09's ethical commitment) — a human reviews before any fix with real consequences is applied.

**UC-11 — Review Diagnosis Dashboard**
*Actor:* Operator. *Sequential flow from UC-7* (a diagnosis record is persisted once the pipeline completes, then surfaced here). Surfaces run status, aggregate metrics, and POC evidence through the built 3-screen console (Overview, Runs & diagnoses, Product & scope — the real navigation structure already shipped in `poc-demo/frontend/src/components/Sidebar.tsx`).

## 5. Relationship rationale — why each `«include»`/`«extend»` was chosen, and why one pair deliberately isn't stereotyped

**`«include»` used for UC-3→UC-4 and UC-3→UC-5** because both always run as part of submitting a trace — there is no submitted trace for which attribution and silent-failure checking are optional. This is the textbook case for `«include»`: mandatory, reused behavior factored out of the base use case.

**`«extend»` used for UC-6→UC-4, UC-6→UC-5, UC-9→UC-6, UC-8→UC-7, UC-10→UC-7** because each fires only under a named, conditional extension point (a failure was actually attributed; a silent failure was actually flagged; a matching memory pattern exists and its gate passed; the repair succeeded and its gate passed; the recovery rate fell below threshold). This is the textbook case for `«extend»`: optional behavior that depends on a condition evaluated at the base use case's extension point.

**UC-6→UC-7 is deliberately drawn as a plain sequential-flow arrow, not a stereotyped relationship**, because forcing every pipeline step into `«include»`/`«extend»` is a common use-case-diagram mistake this model avoids on purpose: verification isn't an optional variant of generation, nor a reusable sub-behavior shared by multiple use cases — it's simply the next stage of one linear pipeline (FR-4.4: an unverified candidate is never surfaced as "the fix"). The System Sequence Diagrams ([System_Sequence_Diagrams.md](System_Sequence_Diagrams.md)) capture this ordering precisely; the use-case diagram's job is actor-facing goals and genuine variability, not restating the pipeline's internal sequence a second time.

## 6. Consistency check

Every use case here maps to exactly one functional requirement group in [Software_Requirements_Specification.md](Software_Requirements_Specification.md) §3, and every mechanism named (Culprit Agent, Error Step Localization, Verification Agent, Semantic Error Diagnostic, Repair Agent, Verified Automatic Repair, Recovery Controller, Verified Repair Memory) is drawn directly from the frozen 10-item mechanism list in [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §7.0 — no use case introduces a capability outside that list. Full cross-document traceability: [Traceability_Matrix.md](../../../archive/proposal-phase/tracking/Traceability_Matrix.md).
