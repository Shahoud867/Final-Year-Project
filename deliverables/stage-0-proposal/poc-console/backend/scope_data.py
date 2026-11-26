# -*- coding: utf-8 -*-
"""
Scope, status, and product-journey data for the Granite PoC console.

EVERY entry here is transcribed from a committed project document, with the
source cited per item. Nothing is invented, and nothing is upgraded in
status: an item with no POC says so, and the two Tier 2 items carry their
real gate criteria and their real (in one case, failed) evidence.

Sources:
  - Frozen mechanism list, two-tier core, gate criteria:
    markdowns/01-planning-and-scope/FYP_Scope_CCP_and_Implementation_Plan.md §7.0, §7.2
  - Scope bands (Core/Advanced/Stretch/Future), descope ladder:
    06_Expanded_Scope_and_Feasibility_Plan.md §4
  - Gate status and evidence:
    markdowns/02-evidence-and-tracking/risk-register.md R17, R21, R22, R28
  - SDK design (callback/hook per framework adapter, normalized trace schema):
    02_Panel_Defense_Question_Bank.md Q16; plan doc §0.07 FR5

The SDK journey below is explicitly marked illustrative=True at the API
boundary and rendered with a persistent "not yet built" banner in the UI.
No SDK exists yet -- zero lines written. It is included because the
project's own one-line pitch ends "ships as an installable SDK," and a
panel needs to see what that means; it is NOT included as a claim that
any of it works.
"""

# --- The 10 committed foundational mechanisms (plan doc §7.0) ---------------

TIER_1 = [
    {
        "n": 1, "name": "Fault-injection harness",
        "what": "Deterministic, rule-based corruption of a chosen step, so the true culprit is known by construction",
        "evidence": "Spikes 3 + 3b — unambiguous ground truth; v1 was self-corrected by the agent and kept as a finding",
        "spike": "Spike 3",
    },
    {
        "n": 2, "name": "Cross-architecture benchmark",
        "what": "Ground-truth-labelled traces from CrewAI/LangGraph — frameworks absent from every prior paper's benchmark",
        "evidence": "Partial — Spike 2 proved a CrewAI workflow maps cleanly to the graph model. Scale-up (500-1,000 traces) is FYP-2 work",
        "spike": "Spike 2",
    },
    {
        "n": 3, "name": "Culprit Agent",
        "what": "Identifies which agent in a failed trace is responsible (Strategist-stage hypothesis)",
        "evidence": "Spike 1 — agent accuracy 62.5-85.7% across 5 independent runs (mean 71.4%)",
        "spike": "Spike 1",
    },
    {
        "n": 4, "name": "Error Step Localization",
        "what": "Pinpoints the exact step where the failure originated",
        "evidence": "Spike 1 — step accuracy 0-25% across 5 runs (mean 13.2%). Honest floor: this is the hard half, and the simplified 2-stage pipeline shows it",
        "spike": "Spike 1",
    },
    {
        "n": 5, "name": "Verification Agent",
        "what": "Evidence-grounded confirmation of a hypothesis against the real trajectory before the Arbiter commits",
        "evidence": "Partial — the tool-grounded Investigator stage is deliberately NOT in the simplified spike-1 pipeline. Full 3-stage reproduction is FYP-1 core work",
        "spike": None,
    },
    {
        "n": 6, "name": "Repair Agent",
        "what": "Generates a targeted correction (prompt, tool argument, structured output, or small function)",
        "evidence": "Spike 8 — repair_success_rate 0.667 (4/6). Both failures share one fixable interface cause (R17)",
        "spike": "Spike 8",
    },
    {
        "n": 7, "name": "Semantic Error Diagnostic",
        "what": "Deterministic task-constraint verification catching well-formed-but-wrong outputs. Zero LLM calls; abstains and reports coverage where no checkable constraint exists",
        "evidence": "Spike 4 — catches known-wrong values incl. a $20.00-vs-$19.75 near-miss, zero false positives",
        "spike": "Spike 4",
    },
    {
        "n": 8, "name": "Verified Automatic Repair",
        "what": "Re-executes downstream under a controlled replay protocol and reports a measured recovery rate before any fix is trusted",
        "evidence": "Spike 5 — corrupted trace 97.2 recovered to 108.0 (recovery_success: true)",
        "spike": "Spike 5",
    },
]

TIER_2 = [
    {
        "n": 9, "name": "Recovery Controller",
        "what": "Applies a verified repair and resumes from a safe checkpoint instead of restarting the whole workflow",
        "status": "No POC yet — genuinely new mechanical work, not a rename of anything already tested",
        "gate": "LangGraph checkpoint/resume PoC demonstrating resume-from-verified-repair-point on at least one real workflow, by Mid-1",
        "fallback": "Re-scope to resumption via controlled replay, which Tier 1 item #8 already delivers. The loop still closes; only the mechanism changes. Recorded per §5.3",
        "risk": "R21",
    },
    {
        "n": 10, "name": "Verified Repair Memory",
        "what": "Stores successful error-to-repair patterns and retrieves them for similar future failures",
        "status": "One real test, and it FAILED — 0 of 8 Who&When cases ever committed to memory; agent accuracy regressed 75%->50% on a 3B backbone",
        "gate": "Re-test on a stronger backbone against the same 8 cases. Pass = at least one committed memory AND no accuracy regression vs. the memory-off run",
        "fallback": "Ships as a memory-on/memory-off ablation study — an evaluation contribution under §4's own table, not a dropped feature",
        "risk": "R22",
    },
]

# --- Scope bands (06 doc §4) ------------------------------------------------

BANDS = [
    {
        "band": "Core",
        "rule": "Mandatory for FYP success. Never descoped — Tier 2 items resolve via their gates, never by silent drop.",
        "tone": "core",
        "items": [
            "All 10 foundational mechanisms (Tier 1 unconditional, Tier 2 gated)",
            "Evaluation v1: statistical protocol with bootstrap CIs, clean-control false-alarm rate, coverage, 4-item ablation matrix",
            "Benchmark >=500 traces incl. 15-20% clean controls, with datasheet",
            "SDK + backend + 3-screen dashboard + containerized deployment",
            "Reproducibility kit, walking skeleton by Mid-1, CI from week 1",
        ],
    },
    {
        "band": "Advanced",
        "rule": "Budgeted (60h). Droppable only via the pre-registered descope ladder, each drop recorded per §5.3.",
        "tone": "advanced",
        "items": [
            "Human-baseline micro-study (6-10 proxy participants, inside the UAT window)",
            "Self-correction dynamics analysis (RQ2a)",
            "Cost-latency-accuracy frontier (RQ4a)",
            "Time-to-integrate metric (target median <30 min)",
            "Ext #1 — widen fault taxonomy to 3 types",
            "Ext #3 — cyclic/dynamic graph support (mechanism already validated by Spike 6)",
            "Ext #4 — confidence calibration (reliability diagram + Brier score)",
        ],
    },
    {
        "band": "Stretch",
        "rule": "Unbudgeted by rule — spends surplus hours only. Starting any Stretch item before Core is integration-complete is a recorded violation.",
        "tone": "stretch",
        "items": [
            "Ext #2 — 3rd architecture (OpenAI Agents SDK or custom)",
            "Ext #5 — preventive clarification classifier (contingent: Spike 7 came out near-random at 0.25)",
            "Ext #6 — failure propagation map UI",
            "Ext #7 — explainable confidence reasoning",
            "Ext #8 — framework compatibility layer (lightweight, across all 7 surveyed frameworks)",
            "Static leaderboard page; webhook / NL incident report / trend chart",
        ],
    },
    {
        "band": "Future",
        "rule": "Explicitly outside the FYP. Named in the report's future-work section only; never presented as promised scope.",
        "tone": "future",
        "items": [
            "Cross-domain transfer testing; chaos testing for agents (both explicitly parked)",
            "RL-based classifier upgrade",
            "Full benchmarking of all 7 frameworks",
            "Multi-tenant SaaS, auth, billing",
            "Custom attribution-model training (AgenTracer-style)",
        ],
    },
]

DESCOPE_LADDER = [
    "All Stretch (unbudgeted anyway — this step costs nothing)",
    "Time-to-integrate -> self-correction analysis -> frontier -> calibration",
    "Fault taxonomy 3 -> 2 types",
    "Benchmark stretch target 1,000 -> floor 500",
    "Cyclic support drops LAST among Advanced (claim-coupled to LangGraph)",
    "Human-baseline study and ablation matrix protected next-to-last",
    "Core never drops",
]

# --- SDK adoption journey (ILLUSTRATIVE — nothing here is built) ------------
# Design source: Q16 in the question bank + FR5. Callback/hook instrumentation
# per framework adapter, emitting a normalized trace schema; the diagnosis
# engine consumes only the schema, so FR5's "no modification to the core
# algorithm" holds.

SDK_JOURNEY = [
    {
        "step": 1,
        "title": "Install",
        "detail": "One pip install. No account, no cloud dependency — the backend runs in your own container (plan §13).",
        "code": "pip install granite-sdk",
        "lang": "bash",
    },
    {
        "step": 2,
        "title": "Wrap your existing workflow",
        "detail": "A callback/hook per framework adapter. Your agent code is not rewritten — FR5 requires the diagnosis engine consume only the normalized trace schema, so instrumenting is additive.",
        "code": (
            "from granite import instrument\n\n"
            "# your existing CrewAI crew, unchanged\n"
            "crew = Crew(agents=[planner, researcher, writer], tasks=[...])\n\n"
            "# one wrap -> emits the normalized trace schema\n"
            "crew = instrument(crew, project=\"support-bot\")"
        ),
        "lang": "python",
    },
    {
        "step": 3,
        "title": "Run as you normally would",
        "detail": "Every execution emits a trace: agent actions, tool calls, and the reference identifiers the execution graph is built from. PII-shaped fields are redacted before storage (R16).",
        "code": "result = crew.kickoff(inputs={\"ticket\": \"refund request #4821\"})",
        "lang": "python",
    },
    {
        "step": 4,
        "title": "Diagnoses appear in this console",
        "detail": "The pipeline runs automatically on each captured trace: graph -> Semantic Error Diagnostic -> attribution -> Repair Agent -> verified replay. Results land in Runs & Diagnoses, exactly as the real spike data does today.",
        "code": None,
        "lang": None,
    },
]


def get_scope():
    return {
        "tier_1": TIER_1,
        "tier_2": TIER_2,
        "bands": BANDS,
        "descope_ladder": DESCOPE_LADDER,
        "sdk_journey": SDK_JOURNEY,
        "sdk_illustrative": True,
        "sdk_disclaimer": (
            "Illustrative concept — NOT built. Zero lines of the SDK exist today. "
            "This is the product-adoption story the project's own one-line pitch implies "
            "(\"ships as an installable SDK\"), shown so the intended product is legible. "
            "Everything else in this console is real data from the 8 committed spikes; "
            "this one screen is the exception, and is labelled as such."
        ),
    }
