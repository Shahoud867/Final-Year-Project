# Claims, scope and official artwork

The poster distinguishes the implemented Refund Desk slice from intended completion capabilities. The completion plan is a **proposal pending team/supervisor agreement**; no delivery dates, scope approval, benchmark superiority or autonomous production repair is claimed.

| Printed element | Status and source |
|---|---|
| AI-agent investigation workbench | Current product, described in [feature catalogue](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/docs/manuals/feature-catalogue.md). |
| Five-stage illustrated error trail | Real declared workflow: Intake → Order Lookup → Policy → Refund Calculator → Writer. The diagram shortens the fourth display label to Calculator and omits secondary dependency edges. [Definition](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/workflows/refund_desk/refund_desk/definition.py). |
| Old price passes through Policy to calculation and reply without a run-time error | The implemented `StalePriceFault` changes lookup prices, leaving later steps to process their inputs. Policy carries item prices to the calculator; the Writer reads the calculated refund. [Fault operator](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/workflows/refund_desk/refund_desk/faults.py), [steps](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/workflows/refund_desk/refund_desk/steps.py). The visual expressly says simplified illustration, not screenshot or a new measurement. |
| Checks, tracing and controlled replay | Implemented features F2–F4. The independent catalogue is the truth source; ranking uses declared lineage and check results. [Feature catalogue](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/docs/manuals/feature-catalogue.md). |
| Source corrected 5/5; source unchanged 0/2 | The recorded example retained from the team's [poster brief](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/deliverables/stage-2-fyp1-final/granite_poster-brief_fyp1-final_draft.md), now shown as an experiment rather than a large monetary comparison. This is one recorded case, not a universal success rate. |
| Cause verified | The example satisfies the implemented VR-1 rule: at least 80% correction replays correct and at most 20% controls correct. [Verification](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/packages/granite_core/granite_core/verification.py). The poster makes no claim of general causal certainty beyond the tested workflow and intervention. |
| Human review; saved evidence | Implemented F5/F6: reviewer decisions and evidence records. A verified intervention in replay does not mean a fix was automatically deployed to production. |
| Early feasibility: 10/10 faulty runs detected; 9/10 origins verified | [7 October 2026 feasibility results](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/research/eval/results/2026-10-07_refund-desk-feasibility.md). The scope warning remains printed: ten tasks, one fault, one small model, four tasks not blind. |
| One-click investigation and check-derived fixes | **PLANNED**, rows 1 and 3 of the [FYP-1 completion proposal](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/docs/plan/fyp1-completion-plan.md). Current candidate replay relies on supplied repair rules. No arbitrary automatic repair is portrayed as already implemented. |
| Retail Agent, imports, regression-test export | **PLANNED**, rows 5–7 of that proposal. Imported traces do not imply arbitrary workflow replay support. |
| Faster diagnosis and reusable QA tests | Expressly a **Goal**, not a measured speed improvement or achieved quality guarantee. |
| Technology stack | Python packages; FastAPI in `apps/api/pyproject.toml`; React and TypeScript in `apps/web/package.json`; Ollama provider in `apps/api/granite_api/providers.py` and setup manual. No logo for an unimplemented framework adapter was added. |

## Brand artwork

The header uses the exact reversed Fault Line horizontal SVG from the repository brand kit. Its polygons, negative ring, disc location, wordmark outlines, Inter 4 optical-size/weight construction and proportions are preserved. Light-blue disc on the navy header follows the supplied reversed colourway. No extra mascot or project-logo variant was invented.

Technology marks are sourced from their owners. See `technology-logos/official-logo-provenance.json` for source URLs, hashes and treatment. React, TypeScript and Ollama are supplied unchanged. The Python emblem paths and FastAPI icon group are isolated from their official combined artwork without redrawing or altering component path geometry/colours. The Python mark retains its native vendor gradient; the poster background and illustrations have no added gradients or effects. Technology brand colours are confined to the technology row.

## Revision and review status

This substantial redesign replaces the previous cash-value hero with a causal visual, expands the completion vision, strengthens header hierarchy and adds official vector technology marks. It keeps the required academic identity, team order, DS degree, objective, project goals and outcome-based tentative FYP-1 plan.

Figma's direct editor is blocked by the account's Starter-plan tool-call limit. The v3.0 Figma import SVG and optional local native-text importer are prepared. **Neither has been imported and visually verified in the live Figma file by the assistant.** The import SVG is a standalone vector view with outlined text; the original SVG and PSD retain live text.
