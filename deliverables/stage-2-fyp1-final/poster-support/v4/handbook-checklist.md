# Granite v4.0 — handbook and design checks

Reference: final FYP handbook §7 p.17, approval process p.7, schedule pp.11/13, Form 4 p.39, plus the expanded user checklist. The attached competitor/workflow samples were references rather than instructions.

| Requirement | Evidence / result |
|---|---|
| Exact portrait trim | 22.5 × 34.5 inches; PDF 1620 × 2484 pt; JPEG/PSD 6750 × 10350 px, 300 ppi, sRGB. Verified. |
| Project name, logo and objective | Exact reversed Fault Line combination logo, registered full title and Find why AI agents fail. |
| Team and supervisor | Three aligned name/roll columns in ascending order; separate Dr. Adil Majeed block. BS (DS), project ID and FAST NUCES, Islamabad Campus retained. |
| Goals | Detect silent failures, locate their source, verify proposed fixes in the upper-right header. |
| Architecture / problem overview | Main component-level diagram: Workbench ↔ API/jobs ↔ evidence store; Refund Desk AI/tool/code steps; model request/response; orders and independent catalogue truth; check → trace → replay and suspect-step loop. |
| Technical accuracy | Diagram checked against code. SQLite/SQLAlchemy persistence is separate from the local retail snapshot. Only Intake, Refund Calculator and Writer call the model adapter. API owns persistence/model I/O; core is framework-free. Supplied repairs and human review remain explicit. |
| Supporting evidence | A common trace branches into corrected/unchanged replays: recorded 5/5 and 0/2. Pilot 10/10 detected and 9/10 origins verified remains separate with ten-task / one-fault / one-small-model / four-not-blind caveats. Early Feasibility display date stays removed. |
| Plan and completed-system vision | Three outcome-based tentative FYP-1 increments. Built investigation; planned guided repair and wider coverage/regression export. No unapproved dates or general automated repair/deployment claim. |
| Technology section | Official Python, FastAPI, React, TypeScript, Ollama vector marks and names organized by Engine, API, Interface and Models with actual roles. Sources/hashes supplied. |
| Co-supervisor / industry partner | None identified in available records; no invented person or partner. |
| Concise, visual communication | 297 conservative copy tokens / 265 lexical words; labels, purposeful connections and proof marks replace paragraphs. |
| Type and spacing | Minimum 26 pt; body/diagram labels 26–32 pt; major headings 44–54 pt; evidence figures 32/50 pt. Inter Medium/Bold and JetBrains Mono Bold match the embedded PDF fonts and live source. Text remains within a 0.75-inch safe margin and on opaque panels. |
| Visibility / consistency / attention / perception | Organized team strip, large central architecture, distinct evidence sources, consistent connectors and role-based stack. Native type and vector diagram structure verified; visual composition reviewed. |
| Contrast | Navy/card 15.24:1; secondary/card 10.68:1; white/navy 15.63:1; light-blue/navy 8.07:1. Semantic blue status text is large/bold. |
| Spelling | Names, technical terms, roles, results and capitalized labels reviewed. |
| Original source plus JPEG | Native PSD with 110 live text layers and 11 embedded vector smart objects, full-resolution JPEG, vector PDF and live-text SVG. University seal is the only raster image in the main PDF. |
| Reusable Background | Bottom group with Base, Strata, Fault channel, Evidence thread. Five original strata, 60-px displacement/channel, 6-px thread and 24-px dots. Final two dots on the right. Channel geometry adapted to the new section gaps. |
| Editable section outputs | Opening/team, architecture, evidence and tools each supplied as live-text SVG, vector PDF and PNG preview. Standalone architecture also linked beside the poster. |

## Requirements that still need physical or institutional completion

Print the actual-size crop PDFs at 100% and read from one metre; check the quiet margin and gap on the actual printer. Open the PSD in Photoshop with the supplied fonts and check the live-text SVG in CorelDRAW before submission. Digital structure/rendering passed, but those application open tests were not performed here. Confirm bleed/profile settings, obtain supervisor approval and submit the source plus JPEG to the committee through its announced channel. No unconfirmed bleed was added.

The handbook does not specify numerical poster font sizes, line spacing, margins, word count, bleed, DPI or CMYK. The p.22 report formatting rules apply to the report. Table 1a p.11 lists W13 submission/W15 evaluation; p.13 allows W13 or final evaluation, so use the coordinator's actual schedule. Form 4 p.39 allocates 10 marks for poster format/layout/style/content. An updated poster is required for the FYP-2 pre-job-fair evaluation.

The live Figma file remains at the older revision after prior tool-limit/upload blockers. The v4.0 outlined import and optional local native-text importer are prepared; the importer was syntax-checked but not run or visually checked in Figma. This is version synchronization, separate from handbook submission compliance.
