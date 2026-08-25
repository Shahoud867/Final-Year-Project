# Granite — One-Page Architecture Sketch

*Supports [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §9 (ownership) and §13 (deployment). Built for FAST guide §16 slide 6 ("high-level architecture, major components, boundaries and intended deployment target") — sketchable at proposal stage, expected to change; this is not a final design.*

---

## The diagram

```
                          ┌─────────────────────────────┐
                          │   TARGET MULTI-AGENT SYSTEM   │
                          │   (user's own workflow, OR    │
                          │   CrewAI / LangGraph toy      │
                          │   workflow for evaluation)    │
                          └───────────────┬───────────────┘
                                          │ instrumented via
                                          ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │  DATA/BENCHMARK OWNER — FAULT INJECTION & BENCHMARK ENGINEERING   │
   │  ┌────────────────┐   ┌─────────────────┐   ┌──────────────────┐ │
   │  │ Framework SDK /  │──▶│ Fault-injection  │──▶│ Ground-truth      │ │
   │  │ instrumentation  │   │ operators        │   │ benchmark (traces │ │
   │  │ (CrewAI, LangGraph, opt. 3rd)           │   │ + labels, public) │ │
   │  └────────────────┘   └─────────────────┘   └──────────────────┘ │
   └──────────────────────────────┬───────────────────────────────────┘
                                  │ raw execution trace
                                  ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │  DIAGNOSIS OWNER — DIAGNOSIS ENGINE                               │
   │  ┌────────────────┐   ┌──────────────────┐   ┌──────────────────┐│
   │  │ Execution-graph  │──▶│ Semantic Error    │──▶│ Backward causal   ││
   │  │ construction     │   │ Diagnostic        │   │ tracing (repro-   ││
   │  │ (own work)       │   │ (own)             │   │ duces ErrorProbe) ││
   │  └────────────────┘   └──────────────────┘   └─────────┬────────┘│
   │                                                          │        │
   │              ┌───────────────────────────────────────────┘        │
   │              ▼                                                    │
   │    ┌───────────────────────┐        ┌─────────────────────────┐  │
   │    │  LLM API (Core-assist)│◀──────▶│ Diagnosis team reasoning │  │
   │    │  swappable — system    │        │ (Strategist/Investigator/│  │
   │    │  still functions if     │        │ Arbiter, ErrorProbe-style;│ │
   │    │  model changes          │        │ Verification Agent = the │ │
   │    │                         │        │ Investigator stage)      │  │
   │    └───────────────────────┘        └────────────┬────────────┘  │
   │                                                    │                │
   │                                                    ▼                │
   │                                       ┌─────────────────────────┐  │
   │                                       │ Repair Agent (own, new   │  │
   │                                       │ 2026-08-24) — generates  │  │
   │                                       │ candidate fix (prompt,   │  │
   │                                       │ tool arg, structured out,│  │
   │                                       │ or function logic).      │  │
   │                                       │ Spike 8: 0.667 (4/6) — R17│  │
   │                                       └────────────┬────────────┘  │
   └──────────────────────────────┬───────────────────────────────────┘
                                  │ diagnosis record + candidate fix
                                  │ (agent, step, confidence, propagation path)
                                  ▼
   ┌──────────────────────────────────────────────────────────────────┐
   │  PLATFORM OWNER — RECOVERY ENGINE & DEPLOYABLE PLATFORM           │
   │  ┌────────────────┐   ┌──────────────────┐   ┌──────────────────┐│
   │  │ Verified         │──▶│ Backend API +     │──▶│ Minimal dashboard ││
   │  │ Automatic Repair │   │ trace/diagnosis   │   │ (results, graph   ││
   │  │ (verifies+applies │   │ record store       │   │ view, report)     ││
   │  │ Repair Agent's fix)│  │                    │   │                    ││
   │  └────────────────┘   └──────────────────┘   └──────────────────┘│
   │                     containerized (Docker), deployed to a         │
   │                     cloud VM / on-prem target                     │
   └──────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
                     ┌─────────────────────────────┐
                     │   INSTALLABLE SDK — the       │
                     │   product boundary: what a    │
                     │   third-party team installs   │
                     │   against their own workflow  │
                     └─────────────────────────────┘
```

---

**Correction, 2026-08-23:** the three boxes above are labeled by *role* (Data/Benchmark, Diagnosis, Platform) — earlier drafts numbered them "Student 1/2/3" as if specific people were already assigned, which hasn't happened. Assign real owners before Mid-1 and update this diagram once decided.

## Component boundaries (per FAST guide §14 — what's owned vs. what's Core-assist)

| Boundary | What's inside |
|---|---|
| **Own work — full ownership, defensible under questioning** | Instrumentation/SDK, fault-injection operators, benchmark, execution-graph construction, Semantic Error Diagnostic, backward causal tracing (adapted from ErrorProbe's published method), Repair Agent (new 2026-08-24 — see risk-register.md R17; POC run same day, Spike 8: repair_success_rate 0.667, 4/6), Verified Automatic Repair, backend, dashboard |
| **Core-assist — used, not claimed as the contribution** | The LLM API — powers agent-under-test behavior and the diagnosis team's reasoning; system structurally survives if swapped (§6 of the plan doc) |
| **Explicitly out of scope for the graded system** | Multi-tenant auth/billing, hosted SaaS signup — deferred to §14 (post-FYP productization) |

## API-usage budget — committed mechanism per component (not just a label)

Locked in per plan doc §6, since "Own work" alone doesn't prove *how* — a component can be technically own-code while still just wrapping an LLM call. Target: **~15–20% API-dependent**, ~80–85% own logic.

| Component | Built as | Counts toward the 15–20%? |
|---|---|---|
| Fault-injection operators | Rule-based, deterministic (AgenTracer-style) | No |
| Execution-graph construction | Structural parsing of reference identifiers (GraphTracer-style), not LLM-asked | No |
| Backward causal tracing | Pure graph traversal (BFS) | No |
| Confidence scoring | Graph features (out-degree, betweenness centrality), not LLM-asked | No |
| **Semantic Error Diagnostic** | **Rule/schema-based checks against task-spec constraints — not an LLM judgment call.** This is the load-bearing commitment; the headline novel claim must not just be an LLM wrapper | No |
| SDK, backend, dashboard | Own code | No |
| Agent-under-test behavior | LLM (necessarily — it's the test fixture, not the contribution) | Yes, but not counted against the budget by §14's own logic |
| **Repair Agent** (new 2026-08-24) | LLM (necessarily — generating a candidate fix is a language/reasoning task, not a deterministic rule) | Yes |
| Verified Automatic Repair's re-execution step | LLM (necessarily — re-running the corrected step) | Yes |
| ErrorProbe baseline reproduction (Strategist/Investigator/Arbiter) | LLM-heavy, isolated to the baseline-comparison code path only | Yes, scoped to reproduction only |

## Data flow, one sentence per hop

1. Target system executes → instrumentation captures a raw trace.
2. Trace → execution graph (nodes = agent actions/tool calls, edges = dependencies).
3. Graph → Semantic Error Diagnostic check (task-constraint verification) + backward causal trace → candidate root cause with confidence.
4. Root cause → Repair Agent generates a candidate fix (prompt, tool argument, structured output, or function logic) — new 2026-08-24, POC run same day (Spike 8: repair_success_rate 0.667, 4/6, risk-register.md R17).
5. Candidate fix → Verified Automatic Repair deterministically re-executes downstream and reports a measured recovery rate → recovery suggestion, gated by confidence threshold.
6. Full diagnosis record → stored → surfaced on the dashboard / returned via the SDK.

## Deployment target (per plan doc §13)

Single containerized deployment (Docker) on a cloud VM or on-prem container target — stated and justified explicitly at proposal stage, not left implicit. No multi-tenant infrastructure in the graded scope (see boundary table above).
