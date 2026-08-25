# Granite — dev

Development artifacts only: POC code and datasets. The research/planning record (CCP statement, contribution statement, literature review, risk register) lives in [`../markdowns/`](../markdowns/) and is not duplicated here — this file links to it instead of copying it, so there's one source of truth.

*Renamed from "TraceCause" to **Granite** (2026-08-24). The official full project title is *A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery*; "Granite" is the permanent short title / product brand.*

---

## What's actually in this folder

| Path | What it is |
|---|---|
| `spikes/poc/` | **9 scripts (spikes 1, 2, 3, 3b, 4, 5, 6, 7, 8)** + their output JSON — reproduction, CrewAI instrumentation, fault injection (v1 + v2), Semantic Error Diagnostic, controlled counterfactual replay, cyclic graphs, preventive classifier, Repair Agent |
| `spikes/poc/whowhen_data/` | The 8 Who&When cases spike 1 runs against |
| `datasets/` | Downloaded/verified datasets + one abandoned build attempt's leftovers (see below) |

**The output JSON files are proposal-defense evidence** (guide §12 requires evidence *shown*, not described) — they are deliberately kept in git alongside the scripts. Full write-up of every spike and what its number means: [`../markdowns/04-poc-evidence/POC_Spike_Outputs_Full.md`](../markdowns/04-poc-evidence/POC_Spike_Outputs_Full.md).

---

## Scope: what from `../markdowns/` actually drives development

Not every doc in there is a build reference. Split by relevance:

**Primary build references — read these when building:**
- [`../markdowns/01-planning-and-scope/architecture-sketch.md`](../markdowns/01-planning-and-scope/architecture-sketch.md) — the actual blueprint
- [`../markdowns/01-planning-and-scope/datasets.md`](../markdowns/01-planning-and-scope/datasets.md) — which datasets are active vs. benched, and why (§6 — don't build against everything downloaded, only GSM8K + tau-bench retail are active)
- [`../markdowns/01-planning-and-scope/FYP_Scope_CCP_and_Implementation_Plan.md`](../markdowns/01-planning-and-scope/FYP_Scope_CCP_and_Implementation_Plan.md) — specifically:
  - §6 (external component classification — which mechanisms must stay rule-based/graph-traversal, not LLM-judged, to hold the 15–20% API-usage budget)
  - §7.0 (committed core vs. optional extensions — **build Tier 1 first**; Tier 2 carries pre-registered Mid-1 decision gates; extensions are explicitly gated behind the whole core)
  - §9 (team ownership — who owns which subsystem)
  - §11 (evaluation plan — metrics the build needs to actually produce, including the silent-failure **coverage/abstention rate**)
  - §13 (deployment plan)
- [`../markdowns/01-planning-and-scope/cost-estimate.md`](../markdowns/01-planning-and-scope/cost-estimate.md) — the model plan the build must actually spend against (cheap/local for volume, strong backbone reserved for evaluation runs)

**Keep checking as you go, not one-time reads:**
- [`../markdowns/02-evidence-and-tracking/risk-register.md`](../markdowns/02-evidence-and-tracking/risk-register.md) — living document, update when a build decision changes scope or a risk resolves
- [`../markdowns/02-evidence-and-tracking/AI_Usage_Log.md`](../markdowns/02-evidence-and-tracking/AI_Usage_Log.md) — log AI-assisted dev work here as it happens, per FAST guide §8.4 — don't let it go stale

**Background/context only — not needed day-to-day during build:**
- [`Full_Literature_Landscape_Analysis.md`](../markdowns/03-market-and-literature-research/Full_Literature_Landscape_Analysis.md), [`ErrorProbe_Baseline_Selection.md`](../markdowns/03-market-and-literature-research/ErrorProbe_Baseline_Selection.md), [`AgenTracer_vs_WhoWhen_Analysis.md`](../markdowns/03-market-and-literature-research/AgenTracer_vs_WhoWhen_Analysis.md), [`Paper_Release_Timeline.md`](../markdowns/03-market-and-literature-research/Paper_Release_Timeline.md) — the research case for *why* this project exists, not *how* to build it
- [`Commercial_Product_Comparison.md`](../markdowns/03-market-and-literature-research/Commercial_Product_Comparison.md) — market/competitive positioning, relevant for the report and defense, not for writing code
- [`../markdowns/06-archive-superseded/`](../markdowns/06-archive-superseded/), [`Supervisor_Briefing.md`](../markdowns/05-deliverables/Supervisor_Briefing.md) — superseded drafts and external-facing summaries

---

## Two interface notes the build must not lose

Both came out of the spikes and are easy to forget once coding starts:

1. **Repair Agent's `corrected_value` must name one atomic field.** Spike 8's only two failures (4/6) shared a single cause: given evidence like "15% loyalty discount," the model returned the *derived result* ($6.75) instead of the *corrected parameter* (15). The real interface must pin down exactly which atomic field is being corrected — the same way Error Step Localization already pins down a specific step index — rather than leaving "the corrected value" ambiguous. See risk-register.md R17.
2. **Spike 2's timestamps were captured post-hoc, not via real per-step hooks.** Fine for validating graph structure; *not* trustworthy for latency metrics. The NFR in plan §0.07 (<50% diagnostic overhead) needs real per-step instrumentation hooks. See risk-register.md R2.

---

## Explicitly out of scope — don't pull these in

- An unrelated FYP project (reshield-fyp + other ideas) that sits elsewhere on the original author's machine. Nothing from there belongs in Granite.
- An orphaned duplicate of `datasets/agentracer_full/` from before consolidation — redundant, not a second source.
- A stale pre-session zip backup, not a working copy.

*(Machine-specific absolute paths for the three items above were removed from this file on 2026-08-25 — a repo-facing doc shouldn't map anyone's local disk layout. They're recorded in the risk register and AI usage log where they belong.)*

---

## External dependency note

The abandoned TracerTraj self-generation attempt (see `datasets.md` §5, risk-register.md R11b) left a Python 3.11 venv + MetaGPT install **outside this project folder** on the original author's machine — installed there to work around the disk-space constraint logged in `AI_Usage_Log.md`. It is not needed for the active build plan (GSM8K + tau-bench retail via CrewAI/LangGraph, not MetaGPT), but it exists if that path is ever revisited.

## Dataset provenance and licensing

`datasets/` currently vendors third-party datasets and one full upstream repo. Before this repository is made public, read [`datasets/DOWNLOAD.md`](datasets/DOWNLOAD.md) — it records each dataset's source, license, and retrieval command, and flags the one item (**GAIA**) whose access terms make redistribution a problem.
