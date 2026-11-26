# Research: proposal-stage spikes

Eight proof-of-concept spikes (nine scripts) run before the proposal defense, with their outputs and input cases. They are the **POC evidence** the handbook asks to be *shown, not described* (C.12), and they are the starting point for the master plan's research track.

*Moved here from `dev/spikes/poc/` on 2026-10-06; the old `dev/` folder no longer exists (`archive/migration-map_2026-10-06.tsv` maps every old path). "Granite" is the permanent short title for *A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery* (renamed from "TraceCause", 2026-08-24).*

---

## What is in this folder

| Path | What it is |
|---|---|
| `poc_spike1_*` (script, runner, rescore, 5 run outputs, summary) | ErrorProbe reproduction on Who&When: agent 71.4% (62.5-85.7), step 13.2% (0-25), n=8, local 3B model |
| `poc_spike2_*`, `poc_spike3_*`, `poc_spike3b_*` | CrewAI instrumentation and fault injection (v1 self-corrected; v2 propagated blindly) |
| `poc_spike4_*`, `poc_spike4b_*` | Silent-failure detector: live n=3 found no natural failure; seeded mechanism test caught 3/3 |
| `poc_spike5_*`, `poc_spike6_*`, `poc_spike7_*`, `poc_spike8_*` | Controlled replay, cyclic-graph bound, preventive classifier (near-random), Repair Agent (4/6) |
| `whowhen_data/` | The 8 Who&When cases spike 1 runs against (a copy of the cases, so the spike does not depend on `data/raw/`) |
| `poc-spike-outputs-full.md` | Full write-up of every spike and what its number means |
| `silent-failure-detection-strategies.md` | Research notes behind spike 4 and the check design |

## Rules for this folder

1. **Keep scripts, outputs and `whowhen_data/` together.** The scripts resolve their files relative to themselves; the stage-0 PoC console (`deliverables/stage-0-proposal/poc-console`) reads these JSON files by exact name.
2. **Do not rename or edit existing outputs.** They are evidence. The only duplicate on disk is deliberate: `poc_spike1_errorprobe_repro_output.json` is identical to `poc_spike1_run5_output.json` (the live output is the last run).
3. **New exploratory spikes** continue the numbering: `spike9_<slug>.py` and `spike9_<slug>_output.json`, plus a row in the table above. Pre-registered evaluation runs do **not** go here; they go to `research/eval/`.
4. **Third-party data is not stored here.** Datasets live in `data/raw/` (see `data/datasets.md`).

## Where the references moved

The planning record that used to sit in `markdowns/` is now split by lifecycle state:

| Need | Location |
|---|---|
| What to do and build now (single source of truth) | [`docs/plan/master-plan.md`](../../docs/plan/master-plan.md) |
| Approved proposal baseline (scope/CCP plan, SRS, SDS, architecture sketch, cost estimate) | [`deliverables/stage-0-proposal/proposal-documents/`](../../deliverables/stage-0-proposal/proposal-documents/) |
| Dataset register and retrieval | [`data/datasets.md`](../../data/datasets.md), [`data/DOWNLOAD.md`](../../data/DOWNLOAD.md) |
| Risk register, AI usage log, Form 13 (living) | [`docs/registers/`](../../docs/registers/) |
| Literature and market notes | [`research/literature/`](../literature/), [`research/market/`](../market/) |

---

## Two interface notes the build must not lose

Both came out of the spikes and are easy to forget once coding starts:

1. **Repair Agent's `corrected_value` must name one atomic field.** Spike 8's only two failures (4/6) shared a single cause: given evidence like "15% loyalty discount," the model returned the *derived result* ($6.75) instead of the *corrected parameter* (15). The real interface must pin down exactly which atomic field is being corrected — the same way Error Step Localization already pins down a specific step index — rather than leaving "the corrected value" ambiguous. See risk-register.md R17.
2. **Spike 2's timestamps were captured post-hoc, not via real per-step hooks.** Fine for validating graph structure; *not* trustworthy for latency metrics. The NFR in plan §0.07 (<50% diagnostic overhead) needs real per-step instrumentation hooks. See risk-register.md R2.

---

---

## Explicitly out of scope — don't pull these in

- An unrelated FYP project (reshield-fyp + other ideas) that sits elsewhere on the original author's machine. Nothing from there belongs in Granite.
- An orphaned duplicate of `datasets/agentracer_full/` from before consolidation — redundant, not a second source.
- A stale pre-session zip backup, not a working copy.

*(Machine-specific absolute paths for the three items above were removed from this file on 2026-08-25 — a repo-facing doc shouldn't map anyone's local disk layout. They're recorded in the risk register and AI usage log where they belong.)*

---

---

## External dependency note

The abandoned TracerTraj self-generation attempt (see `datasets.md` §5, risk-register.md R11b) left a Python 3.11 venv + MetaGPT install **outside this project folder** on the original author's machine — installed there to work around the disk-space constraint logged in `AI_Usage_Log.md`. It is not needed for the active build plan (GSM8K + tau-bench retail via CrewAI/LangGraph, not MetaGPT), but it exists if that path is ever revisited.

## Dataset provenance and licensing

Third-party datasets are in [`data/raw/`](../../data/raw/). Before this repository is made public, read [`data/DOWNLOAD.md`](../../data/DOWNLOAD.md): it records each dataset's source, licence and retrieval command, and flags the one item (**GAIA**) whose access terms make redistribution a problem.
