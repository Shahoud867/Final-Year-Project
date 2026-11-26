# Granite — Software Requirements Specification (SRS)

*New document, closing the gap flagged in the proposal-defense audit: [Software_Design_Specification.md](Software_Design_Specification.md) is a **design** document (components, schema, API, sequence/state detail) — it explains **how** Granite will be built. This SRS defines **what** the system must do, and is written so nothing here duplicates the SDS unnecessarily: where the SDS already commits to a mechanism, this document requires its observable behavior and cites the SDS for how it's realized.*

*Source of authority for everything below: [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §0.07 (the 5 handbook-format FRs), §7.0 (frozen mechanism list), §11 (evaluation plan); [Software_Design_Specification.md](Software_Design_Specification.md) (component/API/schema detail); [risk-register.md](../../../docs/registers/risk-register.md) (R16 privacy/security). Where this document disagrees with any of those, they win — this SRS restates their content in requirements form, it does not supersede them.*

---

## 1. Introduction

### 1.1 Purpose
Defines the functional and non-functional requirements for Granite, a self-healing multi-agent diagnosis, repair, and recovery system, at the fidelity expected of an FYP proposal-defense SRS. Every requirement below is traceable to a use case ([Use_Case_Model.md](Use_Case_Model.md)), a test ([Test_Plan.md](Test_Plan.md)), and a design element ([Software_Design_Specification.md](Software_Design_Specification.md)).

### 1.2 Scope
Granite instruments a multi-agent workflow (built on CrewAI or LangGraph), captures its execution trace, diagnoses failures — including silent failures that trigger no anomaly signal — attributes them to a responsible agent and step, generates and verifies a repair via controlled counterfactual replay, and surfaces the result through an SDK, a backend API, and a 3-screen operator dashboard. It is a **diagnosis and repair layer**, not a replacement for the multi-agent framework itself or for existing trace-capture platforms.

### 1.3 Definitions and acronyms

| Term | Meaning |
|---|---|
| **Silent failure** | An output that passes standard error checks but violates the task's actual constraints — produces no anomaly signal |
| **SED** | Semantic Error Diagnostic — the constraint-based silent-failure verifier |
| **Culprit Agent / Error Step Localization** | The predicted responsible agent / step for an observed failure |
| **Controlled replay protocol** | Re-execution of the downstream portion of a trace with frozen upstream context and pinned decoding parameters; only the LLM step's output is non-deterministic, and its variance is measured, not assumed away (R25) |
| **Recovery rate** | Fraction of replays, over N repeated replays, in which a candidate repair resolves the original failure |
| **Tier 1 / Tier 2** | Tier 1 mechanisms are evidence-backed (real spike behind each) and unconditionally committed; Tier 2 mechanisms carry a pre-registered Mid-1 pass/fail gate and a recorded fallback if the gate fails (plan §7.0) |
| **Clean control** | A benchmark trace run with fault injection disabled, used to measure false-positive rate on healthy runs |

### 1.4 References
[FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) · [Software_Design_Specification.md](Software_Design_Specification.md) · [Use_Case_Model.md](Use_Case_Model.md) · [Test_Plan.md](Test_Plan.md) · [risk-register.md](../../../docs/registers/risk-register.md) · [cost-estimate.md](cost-estimate.md) · [resources.md](resources.md)

---

## 2. Overall description

### 2.1 Stakeholders

*A stakeholder is any individual, group, or organization with an interest in, or affected by, Granite's outcomes — not only its direct users.*

| Stakeholder | Interest |
|---|---|
| **Engineering-team operator** (primary actor, §2.2) | Needs pre-deployment fault testing, post-incident diagnosis, and pre-redeploy fix verification for their own multi-agent system |
| **Product / downstream teams** | Depend on the operator's system shipping correct output; indirectly affected by every silent failure Granite does or doesn't catch |
| **Auditors / compliance reviewers** | Need traceable evidence of what failed, why, and what corrective action was taken |
| **Academic evaluators (FYP panel, supervisor)** | Assess whether the system meets its committed CCP, evaluation plan, and evidence bar |
| **Future researchers** | Consumers of the publicly released benchmark and its ground-truth labels |
| **The three student owners** (Shahoud, Noor, Saif) | Individually accountable for one subsystem each (plan §9); each stakeholder's interest is that their owned subsystem is a real, defensible, independent contribution |
| **The target multi-agent system itself** | A *secondary actor*, not a stakeholder with interests — but its behavior (message formats, tool-call semantics) constrains every requirement below |

### 2.2 Actors

| Actor | Type | Role |
|---|---|---|
| **Engineering-team operator** | Primary, human | Installs the SDK, submits/reviews traces, reviews diagnoses, approves or rejects a suggested repair, browses the dashboard |
| **Multi-agent system under test** (CrewAI / LangGraph workflow) | Secondary, non-human | Produces the raw execution trace Granite instruments; is never itself a user of Granite |
| **LLM API** | External system, Core-assist only (plan §6) | Supplies agent-under-test behavior, Repair Agent generation, and controlled-replay re-execution; every component carrying Granite's actual differentiating claim (graph construction, SED, causal tracing, confidence scoring) is 0%-API and unaffected if this were swapped |
| **Fault-injection harness (self)** | System-internal actor | Not a human actor — included because it originates ground-truth data other requirements depend on |

### 2.3 System scope

**Inside the boundary:** instrumentation SDK, fault-injection harness, execution-graph builder, Culprit Agent, Error Step Localization, Verification Agent, Semantic Error Diagnostic, Repair Agent, Verified Automatic Repair, Recovery Controller (Tier 2), Verified Repair Memory (Tier 2), backend API, diagnosis record store, 3-screen dashboard, single-container deployment.

**Outside the boundary:** the multi-agent framework itself (CrewAI/LangGraph internals), the LLM provider's infrastructure, any existing trace-capture platform the operator already uses (Granite is complementary, not a replacement), multi-tenant auth/billing, message-queue infrastructure, Kubernetes/multi-region orchestration, a caching layer, full RBAC, disaster-recovery infrastructure beyond the stated failure-handling requirements (NFR-6). Full exclusion list and rationale: [Software_Design_Specification.md](Software_Design_Specification.md) §1.

### 2.4 Assumptions

- A2.4.1 — The multi-agent system under test is built on CrewAI or LangGraph (or, via extension #8, a framework Granite can at least parse traces from).
- A2.4.2 — The operator has permission to instrument and inject faults into the system under test; no third party's production system is touched without explicit consent (plan §0.09).
- A2.4.3 — Traces are English-language (accuracy claims do not extend to non-English agent traces — stated as a scope limitation, plan §0.09).
- A2.4.4 — An LLM API (local or hosted) is reachable at diagnosis and repair time; graceful degradation applies if it is not (NFR-6.3).
- A2.4.5 — The task specification for a given workflow yields at least some machine-checkable constraints (numeric ranges, required fields, policy rules) for SED to verify against; where it does not, SED abstains rather than guessing (FR-3, coverage measured).

### 2.5 Constraints

- C2.5.1 — Single-container deployment only (Docker); no Kubernetes/multi-region orchestration (plan §13).
- C2.5.2 — Committed core ships on ≤2 architectures full-benchmarked (CrewAI, LangGraph); a 3rd is a gated extension only (plan §7.0 ext #2).
- C2.5.3 — Zero budgeted spend — the entire reproduction and evaluation runs on local Ollama, not a paid API tier (`cost-estimate.md` §0, R37); a reproduction landing outside the pre-registered ±10-point acceptance band on backbone strength alone is the anticipated, not a failure, outcome.
- C2.5.4 — Tier 2 mechanisms (Recovery Controller, Verified Repair Memory) ship conditionally on their Mid-1 gate outcome; each has a pre-registered fallback if its gate fails (plan §7.0).
- C2.5.5 — SED is scoped to specifications yielding machine-checkable constraints; it does not claim to detect arbitrary semantic wrongness, and abstains where no such constraint exists (plan §7.0 item 7).

### 2.6 Dependencies

| Dependency | Type | Status |
|---|---|---|
| Who&When benchmark (MIT) | Data | In hand, 184 cases verified |
| GSM8K, tau-bench retail | Data (task sources for the new benchmark) | In hand, license-verified |
| TracerTraj-2.5K (AgenTracer) | Data (conditional) | **Not actually released** — downgraded from committed to conditional (risk-register R11) |
| CrewAI, LangGraph | Framework | Open-source, in hand |
| Local Ollama backbone | Compute | In hand, $0 (`cost-estimate.md` §0) |
| An LLM API reachable at runtime | External system | Core-assist only — system must degrade gracefully if unavailable (NFR-6.3) |

### 2.7 External interfaces

| Interface | Direction | Description |
|---|---|---|
| Instrumentation SDK → target system | Inbound to Granite | Captures raw execution trace from the operator's CrewAI/LangGraph workflow |
| Backend REST API (`/api/runs`, `/api/runs/{id}`, `/api/runs/{id}/repair`, `/api/runs/{id}/replay`, `/api/runs/{id}/resume`, `/api/benchmark/generate`) | Bidirectional | Full contract: [Software_Design_Specification.md](Software_Design_Specification.md) §7 |
| LLM API | Outbound | Agent-under-test behavior, Repair Agent generation, controlled-replay re-execution only — never for graph construction, SED, causal tracing, or confidence scoring (plan §6) |
| Operator dashboard | Outbound (to operator's browser) | HTTPS, single-container frontend |

### 2.8 Hardware / software requirements

| Item | Requirement |
|---|---|
| Deployment target | Single Docker container, cloud VM or on-prem host (plan §13) |
| Backend | Python, FastAPI |
| Frontend | React/TypeScript, static build served over HTTPS |
| Database | PostgreSQL |
| Local model runtime | Ollama (committed $0 backbone, `cost-estimate.md` §0) |
| Orchestration frameworks instrumented | CrewAI, LangGraph |
| CI | GitHub Actions |
| Development machine (per operator, not end-deployment) | Any machine capable of running Docker + Ollama locally — no GPU training required for the core system |

---

## 3. Functional requirements

*Identifiers follow `FR-<plan-FR-number>.<sub-item>` so every requirement below traces directly to the 5 handbook-format functional requirements already declared and CCP-justified in [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §0.07 — this SRS decomposes them into testable sub-requirements, it does not add new ones.*

### FR-1 — Fault injection and benchmark generation

| ID | Requirement | Priority | Tier |
|---|---|---|---|
| FR-1.1 | The system **shall** inject a controlled, deterministic fault into a multi-agent workflow built on CrewAI or LangGraph, selecting from a named fault-injection operator (corrupted tool output at proposal stage; communication corruption and context truncation added as extension #1). | Must | Tier 1 |
| FR-1.2 | The system **shall** record, for every injected fault, the ground-truth responsible agent and step at injection time, before any diagnosis runs. | Must | Tier 1 |
| FR-1.3 | The system **shall** support generating benchmark traces with fault injection *disabled* ("clean controls"), comprising 15–20% of the total benchmark, to support false-positive-rate measurement (plan §11). | Must | Tier 1 |
| FR-1.4 | The system **shall** label each generated trace with a propagation outcome (`propagated` / `self_corrected`) once observed, per the schema's `BENCHMARK_CASE.propagation_label` field. | Should | Tier 1 |

### FR-2 — Attribution (Culprit Agent, Error Step Localization, Verification Agent)

| ID | Requirement | Priority | Tier |
|---|---|---|---|
| FR-2.1 | The system **shall** analyze a completed multi-agent execution trace and output a predicted responsible agent for an observed failure. | Must | Tier 1 |
| FR-2.2 | The system **shall** output a predicted responsible step, distinct from the agent-level prediction, for the same observed failure. | Must | Tier 1 |
| FR-2.3 | The system **shall** output a confidence score for each attribution, computed from execution-graph features (out-degree, betweenness centrality) — never by asking the LLM to self-report confidence (plan §6). | Must | Tier 1 |
| FR-2.4 | The system **shall** verify an attribution hypothesis against the real trajectory's evidence (tool outputs, intermediate results) before it is reported as final, via the Verification Agent stage. | Must | Tier 1 |
| FR-2.5 | The system **shall** construct an execution graph from a raw trace via structural parsing of message/reference identifiers — not by asking an LLM what a step depended on. | Must | Tier 1 |

### FR-3 — Silent-failure detection (Semantic Error Diagnostic)

| ID | Requirement | Priority | Tier |
|---|---|---|---|
| FR-3.1 | The system **shall** flag an output that passes standard error checks but violates the task's stated constraints (a silent failure), independent of whether any explicit error signal was raised elsewhere in the trace. | Must | Tier 1 |
| FR-3.2 | The Semantic Error Diagnostic **shall** run unconditionally, in parallel with the attribution path, not gated on the attribution path's output (per [Software_Design_Specification.md](Software_Design_Specification.md) §5's FR3 clarification). | Must | Tier 1 |
| FR-3.3 | The system **shall** verify constraints via deterministic, rule/schema-based checking (value ranges, required fields, logical consistency with stated tool results) — not by asking an LLM whether the output "seems" semantically wrong. | Must | Tier 1 |
| FR-3.4 | Where the task specification yields no machine-checkable constraint, the system **shall abstain** rather than produce a guess, and **shall** report this abstention as a first-class coverage metric. | Must | Tier 1 |
| FR-3.5 | A diagnosis record **shall** be accepted as correctly identifying a silent failure only if the constraint-verification module flags the trace *and* the flagged step matches the fault-injection harness's recorded ground-truth injection point, within an agreed tolerance (acceptance criterion, plan §0.07). | Must | Tier 1 |

### FR-4 — Repair generation and verified counterfactual replay

| ID | Requirement | Priority | Tier |
|---|---|---|---|
| FR-4.1 | The system **shall** generate a targeted candidate correction (prompt, tool argument, structured output, or function-logic change) for a localized, verified failure. | Must | Tier 1 |
| FR-4.2 | Given a candidate corrected value for a specific step, the system **shall** re-execute the downstream portion of the trace under a controlled replay protocol: frozen upstream context, affected steps re-run with pinned decoding parameters. | Must | Tier 1 |
| FR-4.3 | The system **shall** report whether the corrected trace succeeds, with recovery rate measured and reported over N replays — never inferred from a single replay (R25). | Must | Tier 1 |
| FR-4.4 | The system **shall** gate a candidate repair behind the Verification Agent and Verified Automatic Repair stages before it is reported as validated — an unverified candidate is never surfaced as "the fix." | Must | Tier 1 |
| FR-4.5 *(Tier 2, gated)* | Where the Recovery Controller's Mid-1 gate passes, the system **shall** resume execution from a verified repair point via checkpoint. Where the gate fails, the system **shall** fall back to resumption via the controlled replay protocol already delivered under FR-4.2 (recorded fallback, plan §7.0). | Must (mechanism conditional) | Tier 2 |
| FR-4.6 *(Tier 2, gated)* | Where the Verified Repair Memory's Mid-1 re-test passes (≥1 committed memory entry, no agent-accuracy regression vs. memory-off), the system **shall** store and retrieve successful error→diagnosis→repair patterns for similar future failures. Where the re-test fails, the system **shall** ship a memory-on/memory-off ablation study instead of a silently dropped feature (recorded fallback, plan §7.0). | Must (mechanism conditional) | Tier 2 |

### FR-5 — Installable SDK

| ID | Requirement | Priority | Tier |
|---|---|---|---|
| FR-5.1 | The system **shall** be installable via a documented SDK against a user-supplied CrewAI or LangGraph workflow without requiring modification to the core diagnosis algorithm. | Must | Tier 1 |
| FR-5.2 | The SDK **shall** normalize a captured raw trace into the execution-graph input format before submission to the backend (`POST /api/runs`). | Must | Tier 1 |
| FR-5.3 | The SDK **shall** be measurable for time-to-integrate: minutes from `pip install` to first diagnosis on the participant's own workflow (target median <30 min, plan §11 UAT window). | Should | Advanced |

### FR-6 — Data handling, records, and outputs

| ID | Requirement | Priority | Tier |
|---|---|---|---|
| FR-6.1 | The system **shall** persist every diagnosis run's execution graph, attribution, SED verdict, repair candidate, and replay result as a structured diagnosis record (`RUN`/`TRACE_NODE`/`TRACE_EDGE`/`DIAGNOSIS`/`SED_VERDICT`/`REPAIR_CANDIDATE`/`REPLAY_RESULT`, [Software_Design_Specification.md](Software_Design_Specification.md) §6). | Must | Tier 1 |
| FR-6.2 | The system **shall** redact trace content via regex PII redaction *before* storage — no code path stores unredacted trace content (R16). | Must | Tier 1 |
| FR-6.3 | The system **shall** namespace runs by project (per-API-key), preventing cross-project visibility, without building a full auth/RBAC/billing system (extension #4, out of committed core). | Could | Advanced |
| FR-6.4 | The system **shall** surface diagnosis records, run status, and aggregate metrics through a 3-screen dashboard (Overview, Runs & diagnoses, Product & scope, per the built `poc-demo` console's actual navigation). | Must | Tier 1 |

### FR-7 — Error handling

| ID | Requirement | Priority | Tier |
|---|---|---|---|
| FR-7.1 | The system **shall** define and report an explicit degraded state when the LLM API is unavailable at diagnosis or repair time, rather than crashing or silently returning an empty result. | Must | Tier 1 |
| FR-7.2 | The system **shall** define and report an explicit error state for a malformed trace (missing required fields, unparseable structure). | Must | Tier 1 |
| FR-7.3 | The system **shall** terminate backward causal tracing on a cyclic execution graph within a stated max-revisit bound, rather than looping indefinitely (extension #3, validated by Spike 6's control-run evidence that the bound is load-bearing). | Should | Advanced |
| FR-7.4 | Where a proposed repair's recovery rate falls below a confidence threshold, the system **shall** report the result as "needs human review" rather than auto-applying it (extension #12, confidence-gated fix approval — ties directly to the ethical commitment in plan §0.09 that diagnosis output is advisory, never autonomous). | Should | Advanced |

---

## 4. Non-functional requirements

| ID | Category | Requirement | Target / measurement |
|---|---|---|---|
| NFR-1 | **Performance** | Diagnostic latency overhead (wall-clock time added by running the diagnosis pipeline after a trace completes) shall be measured and reported as a percentage of the original workflow's execution time. | <50% for single-pass mode (plan §0.07's one measurable NFR); measured at the Backend API request boundary ([Software_Design_Specification.md](Software_Design_Specification.md) §8) |
| NFR-2 | **Reliability** | The Verified Automatic Repair stage shall report recovery rate with its variance over repeated replays, not a single-run point estimate. | N=5 replays minimum, bootstrap 95% CI (plan §11 statistical protocol) |
| NFR-3 | **Security / privacy** | Trace content shall be redacted (regex PII removal) before persistence; only the relevant node's content shall be sent to the LLM per call, never the full trace in bulk. | Enforced at schema level (`TRACE_NODE.content_redacted`) and at call sites (R16) |
| NFR-4 | **Scalability** | The system shall support a benchmark of 500–1,000 labeled traces without architectural change (message-queue/orchestration infrastructure explicitly out of scope at this scale). | Target scale stated in plan §7.2; single-container deployment sufficient |
| NFR-5 | **Usability** | The dashboard shall not encode meaning by color alone (status badges pair color with text labels); time-to-integrate for a new user shall be measured, not assumed. | WCAG contrast check owed by Final-1 (plan §0.09); time-to-integrate target <30 min median (FR-5.3) |
| NFR-6 | **Availability / failure handling** | The system shall define explicit behavior for three named failure modes: (6.1) LLM API unavailable, (6.2) malformed trace, (6.3) unexpected framework output shape — documented, not merely implied. | [Software_Design_Specification.md](Software_Design_Specification.md) §8 sequence diagram's `alt`/error branches |
| NFR-7 | **Maintainability** | 0%-API components (fault injection, graph construction, causal tracing, confidence scoring, SED) shall remain fully functional if the LLM API is swapped for a different provider/model — the "replacement test" (plan §6). | Verified by producing byte-identical output across an LLM swap for every 0%-API component |
| NFR-8 | **Compatibility** | The SDK shall instrument CrewAI and LangGraph without requiring modification to either framework's core, and shall not require modification to Granite's own diagnosis algorithm per target workflow. | FR-5.1; extension #8 (Framework Compatibility Layer) extends parsing to 5 further frameworks without full benchmarking |
| NFR-9 | **Privacy / ethical constraint** | Fault injection shall be applied only to the project's own toy/test workflows or to consenting pilot users' systems — never to a third party's production system without explicit informed consent. | Plan §0.09 ethical statement; enforced procedurally, not by a technical control |
| NFR-10 | **Cost** | The full project (development, reproduction, evaluation) shall run at $0 committed spend, on local Ollama throughout. | `cost-estimate.md` §0 (R37) |

---

## 5. Requirement priorities — summary

| Priority | Meaning | Count |
|---|---|---|
| **Must** | Required for the committed core to be considered delivered; failure to meet blocks the Tier 1 claim | 22 |
| **Should** | Strengthens the claim significantly; droppable only via the pre-registered descope ladder (plan §7.2) | 5 |
| **Could** | Advanced-band, budgeted but not core-blocking | 1 |

Tier 2 requirements (FR-4.5, FR-4.6) are marked **Must (mechanism conditional)** — the *capability* (resumption, memory) is committed core either way; which *mechanism* delivers it is what the Mid-1 gate decides, per the pre-registered fallback already on record (plan §7.0).

---

## 6. What this document does not do

Consistent with [Software_Design_Specification.md](Software_Design_Specification.md) §0's own discipline: this SRS does not repeat the CCP justification, the literature gap analysis, the 12-month roadmap, or the team-ownership table — each has one source of truth already, cited above, not duplicated. It also does not specify *how* any requirement is implemented (schema fields, endpoint paths, sequence of internal calls) — that is the SDS's job. Where a requirement here and a diagram in the SDS appear to disagree, the SDS's mechanism-level detail is authoritative for *how*, and this document is authoritative for *what must be observably true* — [Traceability_Matrix.md](../../../archive/proposal-phase/tracking/Traceability_Matrix.md) cross-checks that the two never actually conflict.
