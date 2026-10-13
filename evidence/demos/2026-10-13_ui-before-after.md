# UI before and after (panel action A1), 2026-10-13

The proposal panel's first comment was "UI/UX needs improvement" ([Form 10](../../docs/registers/form-10-panel-actions.md), A1). This record compares what was shown at the proposal defense with the product at Mid-1. Slide-ready image: [2026-10-13_ui-before-after.png](2026-10-13_ui-before-after.png).

| | Before (proposal defense, 11 Sep 2026) | After (Mid-1, October 2026) |
|---|---|---|
| Screens | [Diagnosis console](2026-10-13_before-poc-console.png) and [interactive PoC page](2026-10-13_before-poc-canvas.png), frozen in [`deliverables/stage-0-proposal/`](../../deliverables/stage-0-proposal/) | [Run page](2026-10-11_run-detail-checks-graph.png), [finding page](2026-10-11_finding-confirmed-reviewed-evidence.png), [investigations](2026-10-11_investigations-list-filters.png), [guide](2026-10-11_guide-features-inputs-outputs.png), [error state](2026-10-11_run-errored-unrecorded-task.png), [phone](2026-10-11_guide-mobile-390px.png) |
| Organised around | Research results: spike accuracies, "POC evidence", tiers | One user task: investigate a failure (Run, Check, Trace back, Verify, Review, Record) |
| Input | None. The console read the committed spike output files; the PoC page was a single HTML file with no backend calls | A validated form (message, e-mail, order number, fault, seed), with one plain message per invalid field |
| What the user can do | Read metrics | Run a five-agent workflow, see which checks failed, see where the error began, verify it by replay, accept or reject with a comment, download a report |
| Navigation | Overview, Runs & diagnoses, POC evidence, Product & scope, Live demo (scripted) | Investigations, New run, How it works; a four-stage stepper on each finding (Detected, Traced, Verified, Reviewed) |
| Explanations | Research vocabulary (step accuracy, culprit agent, SED) | Plain sentences: "Why this was flagged", "Where did it begin?", "the fix, not luck, changed the result" |
| Feedback states | None needed (static data) | Loading, empty and error states; live job progress; a failed model call ends as "errored" with the reason and a "Run again" button |
| Evidence and decisions | None | Hashed evidence table with integrity status; review history; Markdown and JSON report |
| Accessibility and devices | Not checked | Automated axe-core checks on every screen, light and dark; keyboard-operable graph; phone layout ([audit](../reports/2026-10-07_accessibility-audit.md)) |

**What this shows:** the interface was rebuilt around the user's task, not restyled. **What it does not show:** that people outside the team find the new interface easy to use. That is measured by the usability check in [`docs/manuals/usability-check-protocol.md`](../../docs/manuals/usability-check-protocol.md), with results recorded in `evidence/uat/`.

How the "before" screenshots were made: headless Chrome at 1440 × 900 on the frozen files `deliverables/stage-0-proposal/poc-console/index.html` and `poc-canvas/Granite_Interactive_PoC.html`. The "after" screenshots are the browser walkthrough of 2026-10-11.
