# Granite — Proposal-Defense PoC (Diagnosis Console)

A working, interactive product-vision prototype wired to your **real** proposal-stage spike outputs
(`dev/spikes/poc/*.json`). Nothing in this console is simulated data — every number, graph, verdict, and
repair result is read live from the files already committed as your guide §12 POC evidence.

**This supplements your POC evidence — it does not replace it.** The guide's actual proposal-stage
requirement (§12) is satisfied by the 8 spikes themselves. This console is the product-vision / architecture
demo for slide 6 and slide 9, built so it's honest rather than a mockup.

---

## What it is

- **Backend**: FastAPI (Python) — loads and normalizes all 8 spikes into a unified diagnosis-run schema,
  serves it over a small REST API. See `backend/data_loader.py`'s module docstring for exactly how each
  spike maps to the schema, and the one real data discrepancy this build surfaced.
- **Frontend**: React + TypeScript + Vite — three screens, matching the dashboard scope your own
  `06_Expanded_Scope_and_Feasibility_Plan.md` §6.5 already pinned:
  1. **Overview** — stat tiles (agent/step accuracy, repair success rate, recovery rate, cyclic-bound rate,
     preventive-classifier honest negative), computed live, plus the two honest findings led with, not buried.
  2. **Runs & diagnoses** — all 23 real diagnosis runs generated from the 8 spikes, filterable by spike and
     status, searchable.
  3. **Run detail** — tabbed: *Trace & graph view* (the real execution graph, culprit/fault node highlighted,
     evidence panel) and *Repair & replay report* (candidate fix, before/after replay numbers,
     recovery verdict).
  4. **POC evidence** — an index back to the 8 spikes, for "show, don't describe" during the defense.

## Run it locally

**Backend** (from `poc-demo/backend/`):
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend** (from `poc-demo/frontend/`, in a second terminal):
```bash
npm install
npm run dev
```

Open **http://localhost:5173**. The frontend proxies `/api/*` to the backend on port 8000 (see
`vite.config.ts`) — both must be running.

No database, no seed data, no environment variables. The data loader reads directly from
`dev/spikes/poc/*.json` relative to the repo root, so it always reflects whatever is actually on disk —
re-run a spike and refresh the browser to see updated numbers.

---

## What's real vs. what's illustrative (disclose this at the defense)

| Element | Status |
|---|---|
| All accuracy/precision/recall/recovery/repair numbers | **Real** — read directly from the 8 committed spike JSON files |
| The 23 execution graphs (trace/graph view) | **Real** — built from actual trace data (spike 2/3/3b) or actual Who&When case histories (spike 1), truncated for display the same way Spike 1's own script truncates prompts |
| The "self-corrected" and "repair failed" findings | **Real** — these are the actual honest/negative results from spikes 3 and 8, not curated to look good |
| The confidence gate on the Repair & Replay tab | **Illustrative** — visualizes extension #12's design (confidence-gated fix approval). Where a spike genuinely has no confidence score, it says "not measured," not a fabricated number |
| The overall product shell (sidebar, navigation, "install SDK" positioning) | **Illustrative** — no SDK exists yet; this is the product-vision layer the guide's §16 slide 6 asks for ("high-level architecture... intended deployment target"), not a claim that the SDK is built |

---

## Data discrepancy found while building this (read before the defense)

`poc_spike1_errorprobe_repro_output.json`'s own `summary.step_accuracy` field is **0.0** — every case's
`step_correct` flag is `false` in the raw file — while every other document in this repo (audit, slides,
question bank) states **12.5%**.

**Likely root cause**, visible in the raw data: ground-truth step indices are stored as strings
(e.g. `"5"`), predicted steps as ints (`5`). The scoring script's `pred_step == gt_step` comparison silently
returns `False` for a value that's numerically correct — visible directly in case 6:
`gt_step="5"`, `pred_step=5`.

This console computes and displays **both** numbers side by side (see the Overview page's flagged stat
tile and callout) rather than silently picking one. **Recommended fix before the defense:** patch
`poc_spike1_errorprobe_repro.py`'s scoring line to `pred_step == int(gt_step)` (or equivalent) and re-run
the spike so the committed JSON file itself says 12.5%, matching every document that already cites that
number. If a panelist opens the raw JSON on screen (which your own defense strategy explicitly plans to
do), it currently would not match your slides.
