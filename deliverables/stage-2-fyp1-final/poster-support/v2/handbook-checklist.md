# Poster v2.0 — handbook and content audit

Reference: `references/university/bs-fyp-handbook-2026.pdf`, section 7, page 17; acceptance process on page 7. Also checked against the expanded poster-content/design checklist supplied by the team in this conversation.

The latest request replaces the earlier six-band design brief with a simpler research poster. This is the actual redesigned artwork, not another design specification.

| Requirement | Evidence / status |
|---|---|
| 22.5 × 34.5 inches, portrait | PDF 1620 × 2484 points; JPEG 6750 × 10350 pixels at 300 ppi. Verified. |
| Concise, focused content and bullets | 218 conservative whitespace tokens, including the outlined Granite name; 197 lexical words. The previous poster had 479 tokens. Three short goal bullets, one five-block architecture, two pilot metrics and three iteration cards replace the dense panels. |
| Text readable from a metre | Designed for distance: 26 pt minimum, 28–32 pt supporting labels, 32–36 pt primary body/outcomes, 48–80 pt headings and 104 pt hero values. Actual PDF font sizes and safe margins checked. **The physical one-metre print test remains pending.** |
| Project title and team at top-left | Exact Fault Line combination logo and registered title, all members and supervisor in the header. Registered title is explicitly labelled to distinguish it from implementation status. |
| Team ordering and degree | Shahoud Shahid (23i-2515), Muhammad Noor Ul Haq (23i-2520), Saif Shahzad (23i-2634). Supervisor is Dr. Adil Majeed. BS (DS) retained. |
| Goals at top-right | Detect wrong answers; locate their source; verify proposed fixes. Intended users: engineers and QA teams. |
| One concise objective | “Find the source of silent AI failures.” |
| Institutional name and logo | FAST NUCES, Islamabad Campus, with the repository university logo. The 433 × 427 px source is displayed at 52 pt wide, about 0.72 inches / 217 pixels at 300 ppi. No oversized logo stretch. |
| High-level architecture | AI workflow → Check → Trace → Replay → Human review. Components are working capabilities of the existing Refund Desk slice; the figure is labelled Implemented. |
| Planned work distinguishable | Future iteration cards say Planned and have dashed outlines; the existing workbench says Built and uses a solid outline. Automatic fix derivation/orchestration is not presented as currently implemented. |
| Project plan / tentative FYP-1 deliverables at bottom | Three working increments: existing Refund Desk workbench; proposed one-click investigations, check-derived fixes and Fault Lab; proposed Retail Agent/trace imports plus baseline evaluation and regression-test export. All are within the FYP-1 completion-plan proposal; no FYP-2 content is inserted. |
| Iterative timeline | Numbered, connected iterations, each named by a developed product outcome. No unconfirmed calendar dates were invented. The grouping is a tentative communication of the proposed scope, not an approved delivery commitment. |
| Tools and technologies | Python, FastAPI, React, TypeScript, Ollama in the footer. |
| Co-supervisor / industry partner if applicable | None was identified in the supplied project materials, so no person or partner was invented. |
| Graphics, hierarchy and legibility | Exact project logo, prominent real refund comparison, five simple blocks with arrows, replay marks and two measured counts. No stock imagery, screenshots, decorative grid, gradients or unnecessary icons. High-contrast navy on warm white; blue for verification; red for the wrong output. Meaning is conveyed through labels and marks as well as colour. |
| Spelling, including capitalised terms | Copy manually reviewed, including FAST NUCES, BS (DS), Dr. Adil Majeed, FastAPI, TypeScript, Ollama, and the monetary/replay values. The team should confirm proper names and the registered title before sign-off. |
| Original PSD and JPEG | Native PSD with 65 live text layers, six embedded PDF vector smart objects and named groups. Full-resolution sRGB JPEG supplied. Native layer caches were recomposited and compared with the JPEG preview. |
| Photoshop/Corel recommendation | Photoshop was unavailable; the master was created programmatically in native PSD format. The handbook permits other tools with printing responsibility on the group. Open the PSD in Photoshop with the supplied fonts to check application compatibility before submission. |
| Supervisor approval / format acceptance | **Pending.** Delivering or publishing these files is not supervisor approval or university submission. |

## Source and honesty checks

- Implementation: `docs/plan/execution-status.md`, the feature catalogue, code and workflow definitions, and `docs/plan/fyp1-completion-plan.md`. Older deployment/test-count statements disagree across dated documents; neither a deployment claim nor a test-count badge is used in this poster.
- Example: the recorded Refund Desk run in the poster brief reports $662.00 versus the $662.23 catalogue total. Correcting Order Lookup gives 5/5 correct fix replays and 0/2 correct controls. The simplified caption calls this a corrected source value.
- Pilot counts: `research/eval/results/2026-10-07_refund-desk-feasibility.md` and its explanatory notes: 10/10 faulty runs detected, 9/10 origin steps confirmed. The poster expressly states the small scope and that four tasks were not blind. These are feasibility counts, not a general benchmark or a superiority claim.
- Tentative increments: grouped from the proposed FYP-1 features in `docs/plan/fyp1-completion-plan.md`, section 6. Imported traces do not imply general replay support; the existing replay capability belongs to the integrated Refund Desk workflow.
- Logo: exact primary horizontal Fault Line SVG from `docs/brand/granite-fault-line/svg/granite-horizontal-color.svg`, proportionally scaled. No outline, colour, font shape or internal spacing was redesigned.

## Final physical checks

Print `granite_poster-crop-tests_fyp1-final_v2.0.pdf` on A4 landscape at **Actual size / 100%**. Read from one metre. Confirm printer bleed and colour-profile requirements, then obtain supervisor approval. The delivered artwork is at the exact trim size, sRGB, with no unconfirmed bleed added.
