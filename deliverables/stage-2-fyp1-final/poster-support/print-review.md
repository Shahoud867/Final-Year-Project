# Granite FYP-1 poster — production handoff

Review draft v1.1 · 13 November 2026
Source: Shahoud867/Final-Year-Project, main at 21eba51448b987f6583f834d824ccac9103380b1.
Brief: deliverables/stage-2-fyp1-final/granite_poster-brief_fyp1-final_draft.md (Draft v2).

## Files

- granite_poster_fyp1-final_v1.1.psd — native layered Photoshop-compatible master: live type, embedded PDF vector smart objects, named section groups and a separate Plan group.
- granite_poster_fyp1-final_v1.1.jpg — 6750 × 10350 pixels, 300 ppi, maximum-quality sRGB JPEG.
- granite_poster-preview_fyp1-final_v1.1.jpg — 1600-pixel-wide review JPEG.
- granite_poster_fyp1-final_v1.1.pdf — vector PDF, 22.5 × 34.5 inches, embedded fonts.
- granite_poster_fyp1-final_v1.1.svg — editable vector source; physical dimensions are set in inches. Install the supplied fonts before opening it.
- granite_poster-crop-tests_fyp1-final_v1.1.pdf — two A4 pages of actual-size sections of Bands 2 and 4. Print at **100% / Actual size**, without Fit or Shrink. Read from 1 metre.
- fonts/ — exact static Inter and JetBrains Mono fonts used in the master, with OFL licences.
- poster-production-checks.json — measured dimensions, font floor, word count and PSD structure checks.

## Important: this is a review draft, not a claim of literal compliance

The brief contains mutually incompatible layout and type requirements. For example:

- Its 1500-pixel header is only 360 points tall. The specified 150-point wordmark, title, logo row, team, supervisor, tagline and 120-pixel separations cannot all fit in that height.
- Two $662.xx values at 120 pt in JetBrains Mono need about 1008 points before any padding. The specified seven-column hero region is about 870 points wide, and also needs an output-monitoring panel and an arrow.
- Band 5's two metric rows at 72 pt, their labels, a 72 pt heading, a subheading and the footnote exceed its specified 288-point height.

To make a usable full-size poster, the design retains the required 22.5 × 34.5-inch trim, portrait orientation, all substantive project content, six-band reading order, product palette, exact evidence values and a 22-point minimum. **It changes the specified band heights, point sizes, spacing and some diagram geometry.** It therefore does not meet the brief's exact 32 pt body / 72 pt heading / 120 pt hero / 150 pt wordmark scale or every listed pixel coordinate.

Actual key sizes: wordmark 100 pt; registered title 28 pt; tagline 28 pt; section headings 46–52 pt; hero amounts 68 pt; metric values 42 pt; body and labels 22–32 pt. No printed text is below 22 pt. Some status text is below the brief's 32 pt status-colour rule; icons and explicit labels accompany the status information.

The proof uses a single horizontal rate axis for the confirmed experiment and puts both replay conditions beside one another. The seven-step flow and the six-node Refund Desk pipeline are redrawn as editable vector artwork. All nodes flow left to right. No screenshots, invented UI, stock images or generated AI artwork are used. Optional QR codes are omitted.

Tiny copy edits keep even the stricter whitespace-token count below 480: “Two views of the same run” becomes “Two views, same run”; “Real Refund Desk run…” becomes “Refund Desk run…”; “Real experiment…” becomes “Experiment…”. Names, registered title, goals, values, rules, limitations and all seven tentative deliverables are retained. The final count is in poster-production-checks.json.

## Confirm before submission or printing

These are the brief's own F1–F6/Q1 requirements, not additional approval requirements introduced by the designer.

1. **Supervisor approval:** obtain approval of the final preview. No approval or submission has been made on your behalf.
2. **F1 / logo:** confirm official template and placement with the FYP coordinators. The repository logo is used at 0.861 inches wide, safely below its 1.4-inch limit; it has not been enlarged beyond source resolution.
3. **F2 / printer:** confirm bleed, colour profile and resolution with the printer. Delivered files have the exact trim size, sRGB and 300 ppi; no unconfirmed bleed or CMYK conversion has been applied. Soft-proof against the printer's ICC profile before printing, especially blue and green.
4. **F3 / plan:** confirm that the team expects to show all seven proposed FYP-1 Final deliverables. They are labelled Planned with a dashed region and hollow bullets. No FYP-2 deliverables appear in the plan.
5. **F4 / registered title:** the registered title is reproduced as requested. Automatic repair and recovery are not presented as existing product features. The degree label is BS (DS), corrected per the team on 13 November 2026. Confirm the registered title, names and roll numbers with the supervisor.
6. **F5 / SDG:** SDG 9 is reproduced from the brief/proposal; confirm the registered SDG and target.
7. **F6 / test count:** the latest CI run on main at the reviewed commit was a failure, so “451” is deliberately omitted. The poster says “Automated tests”. Reintroduce a count only after the brief's green-CI condition is met and the current count is verified.
8. **Physical legibility:** perform the supplied 100% A4 crop test at 1 metre. This physical check has not been performed by the designer.

CI evidence: https://github.com/Shahoud867/Final-Year-Project/actions/runs/43069207241 (main; failure, checked 11 November 2026).

## Photoshop and printing process limitation

Photoshop/Corel was not available in this environment. The native PSD was authored programmatically and checked with psd-tools. It contains actual TySh live text layers, embedded PDF vector smart objects and a full-resolution merged preview; it is not a flattened JPEG renamed to .psd. **It was not built or opened in Adobe Photoshop**, so the brief's Photoshop-authoring process requirement has not been completed. Before committee submission, install the supplied fonts, open the PSD in Photoshop, inspect text reflow and smart-object placement, and save/review the master there. Photoshop compatibility has been checked structurally, not through Photoshop's application UI. The handbook says teams using another tool are responsible for printing their poster themselves.

## Evidence checked

- Refund Desk example: brief's $662.00 vs $662.23 and CHK-OUT-1 failure.
- Verification: 5/5 fix replays, 0/2 controls, innocent step 0/5; 95% Wilson interval 57%–100%; VR-1 thresholds 80% / 20% / 20%.
- Feasibility: research/eval/results/2026-10-07_refund-desk-feasibility.md and its accompanying notes; the clean-run finding was a genuine natural model error, so zero false alarms is retained with the limitation footnote.
- Workflow/data flow: docs/diagrams/refund-desk-dataflow.svg and the investigation/verification source diagrams.
- Handbook section 7, pages 7 and 13: original PSD/JPEG, size, portrait, content placement and supervisor approval.

AI assistance: poster composition, diagram redrawing, copy fitting, native PSD assembly, exports and file-level verification were performed with Codex. The user subsequently authorized pushing the corrected files to GitHub on 13 November 2026. No university submission or supervisor approval has been made.

## Revision v1.1, 13 November 2026

- Corrected BS (CS) to **BS (DS)** at the team’s request.
- Regenerated and checked the native PSD, full JPEG, PDF, preview and crop tests.
- Created an editable Figma version: https://www.figma.com/design/0OR9RnQzzZCGVfZWOulZ73?node-id=3-2
- Publication to GitHub is authorized by the user; the publication does not constitute supervisor approval or university submission.
