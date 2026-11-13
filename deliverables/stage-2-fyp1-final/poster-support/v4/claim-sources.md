# Claims, scope and official artwork

The poster distinguishes the implemented Refund Desk slice from intended completion capabilities. The completion plan is a **proposal pending team/supervisor agreement**; no delivery dates, scope approval, benchmark superiority or autonomous production repair is claimed.

| Printed element | Status and source |
|---|---|
| AI-agent investigation workbench | Current product, described in [feature catalogue](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/docs/manuals/feature-catalogue.md). |
| Refund Desk under investigation | Real declared workflow: Intake → Order Lookup → Policy → Refund Calculator → Writer. The five named steps are retained with AI/TOOL/CODE badges; secondary lineage edges are omitted for clarity. [Definition](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/workflows/refund_desk/refund_desk/definition.py). |
| Orders and catalogue truth use separate read paths | Order Lookup reads the local retail orders; executable checks and supplied price repairs independently consult catalogue truth. The investigation database is a separate SQLite/SQLAlchemy store. See [architecture notes](architecture-notes.md) for code sources. |
| Checks, tracing and controlled replay | Implemented features F2–F4. The independent catalogue is the truth source; ranking uses declared lineage and check results. [Feature catalogue](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/docs/manuals/feature-catalogue.md). |
| Source corrected 5/5; source unchanged 0/2 | The recorded example retained from the team's [poster brief](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/deliverables/stage-2-fyp1-final/granite_poster-brief_fyp1-final_draft.md), shown as a fork from the same retained trace into correction and control arms. This is one recorded case, not a universal success rate. |
| Source confirmed | The example satisfies the implemented VR-1 rule: at least 80% correction replays correct and at most 20% controls correct. [Verification](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/packages/granite_core/granite_core/verification.py). The poster makes no claim of general causal certainty beyond the tested workflow and intervention. |
| Human review; saved evidence | Implemented F5/F6: reviewer decisions and evidence records. A verified intervention in replay does not mean a fix was automatically deployed to production. |
| Early feasibility: 10/10 faulty runs detected; 9/10 origins verified | [7 October 2026 feasibility results](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/research/eval/results/2026-10-07_refund-desk-feasibility.md). The scope warning remains printed: ten tasks, one fault, one small model, four tasks not blind. |
| One-click investigation and check-derived fixes | **PLANNED**, rows 1 and 3 of the [FYP-1 completion proposal](https://github.com/Shahoud867/Final-Year-Project/blob/poster-ds-figma-v1.1/docs/plan/fyp1-completion-plan.md). Current candidate replay relies on supplied repair rules. No arbitrary automatic repair is portrayed as already implemented. |
| Retail Agent, imports, regression-test export | **PLANNED**, rows 5–7 of that proposal. Imported traces do not imply arbitrary workflow replay support. |
| Lasting regression-test vision | The outcome-based plan labels regression-test export **PLANNED**. No measured speed or superiority claim is printed. |
| Technology stack | Python packages; FastAPI in `apps/api/pyproject.toml`; React and TypeScript in `apps/web/package.json`; Ollama provider in `apps/api/granite_api/providers.py` and setup manual. No logo for an unimplemented framework adapter was added. |

## Brand artwork

The header uses the exact reversed Fault Line horizontal SVG from the repository brand kit. Its polygons, negative ring, disc location, wordmark outlines, Inter 4 optical-size/weight construction and proportions are preserved. Light-blue disc on the navy header follows the supplied reversed colourway. No extra mascot or project-logo variant was invented.

Technology marks are sourced from their owners. See `technology-logos/official-logo-provenance.json` for source URLs, hashes and treatment. React, TypeScript and Ollama are supplied unchanged. The Python emblem paths and FastAPI icon group are isolated from their official combined artwork without redrawing or altering component path geometry/colours. The Python mark retains its native vendor gradient; the poster background and illustrations have no added gradients or effects. Technology brand colours are confined to the technology row.

## Revision and review status

This revision replaces the limited example graphic with the full component-level system, reorganizes team and technology information, and combines the recorded replay and scoped pilot in a divided evidence panel. It keeps the required academic identity, team order, DS degree, objective, project goals and outcome-based tentative FYP-1 plan.

Previous direct Figma edits were blocked by the account's Starter-plan tool-call limit. The v4.0 Figma import SVG and optional local native-text importer are prepared. **Neither has been imported and visually verified in the live Figma file by the assistant.** The import SVG is a standalone vector view with outlined text; the original SVG and PSD retain live text.


## Full-system architecture in v4.0

The new figure shows the browser/API/jobs/store as well as the actual workflow and core. It keeps orders/catalogue truth separate from investigation persistence, and distinguishes three AI steps from the tool and code steps. Model links show requests/responses. The blue loop says Replay from suspect; the caption states that the API saves verdicts, evidence and human reviews, with supplied repairs only. This is a component view of one application, not a microservice or hosted-deployment claim. See `architecture-notes.md` for implementation sources and limits.

The attached competitor poster and separate workflow illustration were reviewed as design benchmarks. Their instructions, logos, domain components, performance figures and distinctive styling were not adopted. The reference PDF itself is not redistributed in this public package.
