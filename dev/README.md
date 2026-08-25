# TraceCause — dev

Development artifacts only: POC code and datasets. The research/planning record (CCP statement, contribution statement, literature review, risk register) lives in `../agent-autopsy/markdowns/` and is not duplicated here — this file links to it instead of copying it, so there's one source of truth.

---

## What's actually in this folder

| Path | What it is |
|---|---|
| `spikes/poc/` | 4 real POC scripts + their output JSON — reproduction, CrewAI instrumentation, fault injection (v1 + v2), silent-failure detector |
| `datasets/` | Downloaded/verified datasets + one abandoned build attempt's leftovers (see below) |

---

## Scope: what from `agent-autopsy/markdowns/` actually drives development

Not every doc in there is a build reference. Split by relevance:

**Primary build references — read these when building:**
- [`../agent-autopsy/markdowns/architecture-sketch.md`](../agent-autopsy/markdowns/architecture-sketch.md) — the actual blueprint
- [`../agent-autopsy/markdowns/datasets.md`](../agent-autopsy/markdowns/datasets.md) — which datasets are active vs. benched, and why (§6 — don't build against everything downloaded, only GSM8K + tau-bench retail are active)
- [`../agent-autopsy/markdowns/FYP_Scope_CCP_and_Implementation_Plan.md`](../agent-autopsy/markdowns/FYP_Scope_CCP_and_Implementation_Plan.md) — specifically:
  - §6 (external component classification — which mechanisms must stay rule-based/graph-traversal, not LLM-judged, to hold the 15–20% API-usage budget)
  - §7 (committed core vs. optional extensions — build the core first, extensions are explicitly gated)
  - §9 (team ownership — who owns which subsystem)
  - §11 (evaluation plan — metrics the build needs to actually produce)
  - §13 (deployment plan)

**Keep checking as you go, not one-time reads:**
- [`../agent-autopsy/markdowns/risk-register.md`](../agent-autopsy/markdowns/risk-register.md) — living document, update when a build decision changes scope or a risk resolves
- [`../agent-autopsy/markdowns/AI_Usage_Log.md`](../agent-autopsy/markdowns/AI_Usage_Log.md) — log AI-assisted dev work here as it happens, per FAST guide §8.4 — don't let it go stale

**Background/context only — not needed day-to-day during build:**
- `Full_Literature_Landscape_Analysis.md`, `ErrorProbe_Baseline_Selection.md`, `AgenTracer_vs_WhoWhen_Analysis.md`, `Paper_Release_Timeline.md` — the research case for *why* this project exists, not *how* to build it
- `Commercial_Product_Comparison.md` — market/competitive positioning, relevant for the report and defense, not for writing code
- `TraceCause_AgentTestLab_Pitch.md`, `Supervisor_Briefing.md` — external-facing summaries

---

## Explicitly out of scope — don't pull these in

- `d:\fyp - research\other\` — a **different, unrelated FYP project** (reshield-fyp + other ideas). Nothing from there belongs in TraceCause.
- `d:\fyp - research\AgenTracer\` — an orphaned duplicate of `datasets/agentracer_full/` from before consolidation. Redundant, not a second source — flagged for deletion, not yet removed as of 2026-08-22.
- `d:\fyp - research\agent-autopsy.zip` — a stale pre-session backup, not a working copy.

---

## External dependency note

The abandoned TracerTraj self-generation attempt (see `datasets.md` §5, risk-register.md R11b) left a Python 3.11 venv + MetaGPT install on `E:\ai-workspace\` (not under this project folder — installed there to avoid the C:/D: disk-space crisis logged in `AI_Usage_Log.md`). It's not needed for the active build plan (GSM8K + tau-bench retail via CrewAI/LangGraph, not MetaGPT), but it's there if that path gets revisited.
