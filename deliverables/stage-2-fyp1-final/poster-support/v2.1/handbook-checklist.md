# Poster v2.1 — handbook and content audit

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
| Graphics, hierarchy and legibility | Exact project logo, prominent real refund comparison, five simple blocks with arrows, replay marks and two measured counts. The quiet Strata and Fault background uses the supplied paper tones, a narrow square stepped channel and a blue evidence thread. All copy and diagrams sit on opaque panels. No stock imagery, screenshots, decorative grid, gradients or unnecessary icons. High-contrast navy on warm white; blue for verification; red for the wrong output. Meaning is conveyed through labels and marks as well as colour. |
| Spelling, including capitalised terms | Copy manually reviewed, including FAST NUCES, BS (DS), Dr. Adil Majeed, FastAPI, TypeScript, Ollama, and the monetary/replay values. The team should confirm proper names and the registered title before sign-off. |
| Original PSD and JPEG | Native PSD with 65 live text layers, eleven embedded PDF vector smart objects and named groups. Full-resolution sRGB JPEG supplied. Native layer caches were recomposited and compared with the JPEG preview. |
| Photoshop/Corel recommendation | Photoshop was unavailable; the master was created programmatically in native PSD format. The handbook permits other tools with printing responsibility on the group. Open the PSD in Photoshop with the supplied fonts to check application compatibility before submission. |
| Supervisor approval / format acceptance | **Pending.** Delivering or publishing these files is not supervisor approval or university submission. |

## Source and honesty checks

- Implementation: `docs/plan/execution-status.md`, the feature catalogue, code and workflow definitions, and `docs/plan/fyp1-completion-plan.md`. Older deployment/test-count statements disagree across dated documents; neither a deployment claim nor a test-count badge is used in this poster.
- Example: the recorded Refund Desk run in the poster brief reports $662.00 versus the $662.23 catalogue total. Correcting Order Lookup gives 5/5 correct fix replays and 0/2 correct controls. The simplified caption calls this a corrected source value.
- Pilot counts: `research/eval/results/2026-10-07_refund-desk-feasibility.md` and its explanatory notes: 10/10 faulty runs detected, 9/10 origin steps confirmed. The poster expressly states the small scope and that four tasks were not blind. These are feasibility counts, not a general benchmark or a superiority claim.
- Tentative increments: grouped from the proposed FYP-1 features in `docs/plan/fyp1-completion-plan.md`, section 6. Imported traces do not imply general replay support; the existing replay capability belongs to the integrated Refund Desk workflow.
- Logo: exact primary horizontal Fault Line SVG from `docs/brand/granite-fault-line/svg/granite-horizontal-color.svg`, proportionally scaled. No outline, colour, font shape or internal spacing was redesigned.

## Final physical checks

Print `granite_poster-crop-tests_fyp1-final_v2.1.pdf` on A4 landscape at **Actual size / 100%**. Read from one metre. Confirm printer bleed and colour-profile requirements, then obtain supervisor approval. The delivered artwork is at the exact trim size, sRGB, with no unconfirmed bleed added.


## v2.1 background-only revision

The user selected the minimal v2 poster and delegated adaptations of the older background addendum to suit its layout. The light header and footer stay unchanged. All 65 native text records, including type data and transforms in the PSD, are identical to v2.0; copy remains 218 conservative tokens / 197 lexical words. The two old decorative full-width rules were removed from the production artwork; the local Figma updater hides them without deletion.

- Paper `#F3F1EC`, alternate stratum `#EFECE5`, channel `#E9E5DC`, thread `#0A66D6`, opaque panels `#FDFCFA`.
- Five 2070 px strata, with the right-hand edges raised 60 px; hard boundaries. Channel 60 px, thread 6 px, discs 24 px. No effects or added colours.
- Adapted to the v2 composition: channel centres x = 100 and 6650 px, header ends at y = 2208.33 px, horizontal step y = 5962.5 px, channel ends at y = 9769.58 px. Panel geometry and dot positions are recorded in `background-geometry.json`.
- The final two evidence dots are on the right-hand channel, as explicitly confirmed by the team.
- PSD bottom group **Background** contains separate **Base**, **Strata**, **Fault channel**, **Evidence thread** subgroups, each with its embedded vector source. **Content panels** sits above it and below all existing content groups.
- Every extracted PDF text bounding box is contained in an opaque panel. Navy body copy on the cards has measured contrast **15.24:1**. Suppressing the faint strata/channel cannot erase any copy, diagram or research information.
- Added `granite_poster-background-crops_fyp1-final_v2.1.pdf`: A4 portrait with one margin and one band-gap crop at actual physical size. **Printing this proof remains pending**; no physical print was made in this environment.

**Figma status:** the original frame 31:3 is **not updated**. The Figma direct editor returned the Starter-plan call-limit error; the alternative SVG upload was blocked by the environment proxy (CONNECT 403). No canvas mutation succeeded. A full font-independent vector import and an optional local plugin for updating the existing native-text frame are supplied. The plugin passed JavaScript syntax checking but has not been executed or visually checked in Figma.
