# Granite poster compliance audit

Reviewed 13 November 2026 against the latest **v4.0 print exports**, the team's expanded poster checklist in chat, and `bs-fyp-handbook-2026.pdf`. The complete 86-page handbook was searched for poster references; relevant text and tables on pages 7, 11–13, 17, 22, 25 and 39 were reviewed. The actual poster preview and exported PDF/JPEG/PSD were inspected again.

**Finding:** no mandatory poster content is missing from the supplied checklist. The digital dimensions and required source/image formats are present. The complete submission process cannot yet be marked finished: physical one-metre readability, Photoshop application compatibility, printer coordination, supervisor approval and submission to the committee remain unverified. The live Figma revision has not been re-verified or updated by the assistant for v4.0; the complete v4.0 system poster is available in the exported files.

## Requirement-by-requirement findings

| Requirement | Evidence in v4.0 | Finding |
|---|---|---|
| 22.5 × 34.5 inches | Main PDF is 1620 × 2484 points; JPEG and PSD are 6750 × 10350 pixels, 300 ppi. | Verified. |
| Portrait | Height exceeds width in every primary print export. | Verified. |
| Condensed, concise representation | 297 conservative whitespace tokens including the outlined project name; 265 lexical words. Short phrases, three goal bullets and diagrams replace paragraphs. | Present; no handbook numerical word limit. |
| Project name and original logo | Granite title with the supplied Fault Line combination logo. Registered full title is also shown. | Present. |
| Concise objective | “Find why AI agents fail.” Goals explain detection, source location and fix verification. | Present. |
| Architecture or visual problem overview | Full Granite component diagram with workbench/API/jobs/store, Refund Desk under test, model adapter, separate retail snapshot, check/trace/replay and a suspect-step replay loop. A correction/control experiment supports the diagram. | Both are present. |
| Plan and tentative deliverables | Investigate → Guide repairs → Extend, with concrete workbench, one-click investigation, check-derived correction, import and regression-test outcomes. | Present at the bottom. |
| Iterative timeline | Three numbered, connected increments, each producing a developed outcome. Built and Planned labels distinguish status. | Present as an ordered iteration sequence; §7 does not require calendar dates or a Gantt chart. |
| Team and supervisor | Shahoud Shahid (23i-2515), Muhammad Noor Ul Haq (23i-2520), Saif Shahzad (23i-2634); Dr. Adil Majeed. | All present; ascending roll-number order; professional title, no “Sir” or “ma’am”. |
| Co-supervisor / industry partner if applicable | Neither is identified in available project records. | Conditional; no person or partner invented. |
| University name and logo | FAST NUCES, Islamabad Campus and the repository university logo. | Present. |
| Degree identification | BS (DS). | Verified; no BS (CS) in extracted poster text. |
| Tools and technologies | Python, FastAPI, React, TypeScript, Ollama, with official vector marks and names. | Present in footer; original source URLs, hashes and exact geometry treatments are recorded in the v4.0 support files. |
| Recommended placement | Title/registered title in the upper-left, goals upper-right, organized team/supervisor strip in the top area, and plan/deliverables at the bottom. | Present. The handbook uses “may” for these placements; the poster follows them. |
| Text large enough at one metre | PDF minimum 26 pt, main labels 28–36 pt, headings 44–54 pt, supporting evidence figures 32–50 pt. Inter Medium/Bold and JetBrains Mono Bold are embedded in the PDF and match the live-type source faces. | Digital sizes verified; actual viewing-distance test pending. |
| Spacing and alignment | All PDF text remains within a 0.75-inch text-safe margin; every text bounding box is on an opaque panel. Consistent alignment and open section gaps. | Digitally verified / visually reviewed. §7 gives no numerical spacing rule. |
| Illustrations and original graphics | Exact reversed project logo, component-level architecture, model request/response bus, separate data paths, forked replay proof and categorized official technology marks. | Present; screenshots are examples in §7, not a required poster element. |
| Spelling and capitalised terms | Copy visually reviewed, including proper names, FAST NUCES, BS (DS), FastAPI, TypeScript, Ollama and the workflow/technology terms and results values. | No spelling error found in this review; team confirmation of personal names remains part of sign-off. |
| Visibility | Prominent problem statement and illustrated error trail; content grouped on opaque panels with spacing. | Design review passed; final evaluation remains the faculty panel's judgement. |
| Consistency | Shared fonts, alignment, label sizes, colour meanings and block/arrow conventions. | Design review passed. |
| Attention | Clear title → problem → workflow → evidence → plan hierarchy, with restrained colour emphasis. | Design review passed. Animations are not necessary for a printed poster. |
| Perception / legibility | Plain block labels; check/cross marks and text reinforce colour; body copy is separated from the background. Navy body text on the opaque card has measured contrast 15.24:1. | Digital review passed; print test pending. |
| Original Photoshop/Corel file plus JPEG | Native PSD contains 110 live text layers and 11 embedded vector smart objects; full-resolution JPEG is supplied. | Files and structure verified; opening and inspecting the PSD in Photoshop remains pending. |
| Other authoring tools and printing | Figma/SVG/programmatic PSD workflow used. | Permitted by §7 with printing responsibility on the group. Arrange printer handling accordingly. |
| Supervisor approval before acceptance | Handbook p.7 expressly requires approval before committee acceptance. | Approval not evidenced; university submission is not evidenced. |

## Typography and spacing clarification

Handbook §7 (p.17) specifies readability from one metre. It does **not** prescribe a numerical poster font size, font family, line spacing, paragraph spacing, margin width, word count, 300-ppi resolution, bleed or CMYK profile. These are production choices or printer requirements.

The Times New Roman 11 pt body, Arial headings, 1.5 line spacing, 6 pt paragraph spacing and asymmetric margins on p.22 belong to **§8, FYP Report Format**. They are not poster formatting requirements. The selected poster fonts are Inter and JetBrains Mono; the supplied logo retains its exact brand wordmark.

## Further handbook information

- **p.7:** the committee verifies format; posters are accepted only after supervisor approval. It coordinates printing/display with the university printer. Poster evaluation may run alongside the final FYP-1 evaluation.
- **p.11, Table 1a:** poster submission in Week 13 and evaluation in Week 15, potentially at final evaluation.
- **p.13:** separately describes poster evaluation in Week 13 or at the FYP-1 final evaluation. This timing differs from Table 1a; the coordinator's announced schedule must settle the actual date. The handbook does not establish a single midterm-only poster evaluation date.
- **p.39, Form 4:** Poster carries **10 marks** within the FYP-1 Final presentation/demo evaluation rubric, assessing “format, layout, style, contents”. Visual quality remains a graded judgement even when a checklist is satisfied.
- **p.12, Table 1b:** updated posters are required for the FYP-2 Pre–Job Fair evaluation in Week 8; poster material is also needed for the Graduate Directory/job fair and final deliverables.
- The repository's [completion-plan proposal](fyp1-completion-plan.md) records **15 November 2026** as the poster deadline supplied by the team. That calendar date comes from the project record, not a date printed in handbook §7.

## Remaining completion steps

1. Print the [text-legibility crops](../../deliverables/stage-2-fyp1-final/granite_poster-crop-tests_fyp1-final_v4.0.pdf) at **Actual size / 100%** and read them from one metre. Correct any labels that fail this physical test.
2. Print the [margin and band-gap proof](../../deliverables/stage-2-fyp1-final/granite_poster-background-crops_fyp1-final_v4.0.pdf) at **100%**. Check the faint background and thread on the chosen printer.
3. Open the original PSD in Photoshop with the supplied fonts and confirm that live text, vectors and colour render correctly. Structural checks and cached previews have passed; an application open test has not been performed.
4. Confirm printer bleed, colour profile and delivery settings. The supplied artwork is exact trim size with no unconfirmed bleed.
5. Obtain supervisor approval and submit the required source file plus JPEG through the committee's announced channel and deadline.
6. Apply and visually verify the v4.0 system poster in Figma before treating that file as the same revision as the exports. This is version synchronization, not an additional handbook requirement. The previous direct edit was blocked by Figma's Starter-plan tool-call limit, and the fallback upload was blocked by the environment.

## Evidence

- [Handbook source](../../references/university/bs-fyp-handbook-2026.pdf), especially §7 p.17, acceptance p.7 and Form 4 p.39.
- [Latest poster preview](../../deliverables/stage-2-fyp1-final/granite_poster-preview_fyp1-final_v4.0.jpg).
- [Print PDF](../../deliverables/stage-2-fyp1-final/granite_poster_fyp1-final_v4.0.pdf).
- [Delivery files and Figma status](../../deliverables/stage-2-fyp1-final/README.md).
- [Production checks and geometry](../../deliverables/stage-2-fyp1-final/poster-support/v4/poster-production-checks.json).

This audit accompanies the substantial v3.0 exhibition redesign. The composition, visual narrative and typography were updated at the team’s request. Implementation status, scope approval, delivery dates and supervisor approval were not changed. The earlier v2.1 exports and their original audit remain available in the versioned support files and Git history.


## v3.0 claims and artwork review

The new illustration replaces the large monetary example with the actual stale-price fault’s route through the declared Refund Desk steps. Its caption identifies it as a simplified illustration. The recorded 5/5 corrected and 0/2 control result is kept separate from the small 10-task feasibility pilot. Faster diagnosis is explicitly a goal. One-click investigation, check-derived fixes, Retail Agent, imports and regression-test export are labelled PLANNED. See the versioned [claim sources](../../deliverables/stage-2-fyp1-final/poster-support/v4/claim-sources.md).

Official technology marks were obtained from Python’s website and the FastAPI, React, Microsoft TypeScript and Ollama repositories. Python’s emblem paths and FastAPI’s icon group were isolated without redrawing; the other marks retain their supplied SVG bytes. Original vendor colours are retained in the technology row; Python’s own native gradient is retained as part of that official mark. The poster background and illustrations have no added gradients, shadows or effects. See [logo provenance](../../deliverables/stage-2-fyp1-final/poster-support/v4/technology-logos/official-logo-provenance.json).


## v3.1 display-date correction

At the team’s request, removed only “· 7 OCT 2026” from the Early Feasibility heading. All result counts, limitations, type styles, coordinates and graphics match v3.0. Historical study dates and citations remain in the support records. The PDF/JPEG/PSD/SVG, preview, Figma import files and print proofs were updated together. Figma live application remains blocked as previously recorded.


## v4.0 system-architecture redesign

At the team’s request, reviewed the attached competitor PDF and workflow sample as references rather than instructions. Rebuilt the opening/team strip, central architecture, replay/pilot evidence panel and role-based technology section. Code review distinguishes the actual three AI steps, tool/code steps, model adapter, local retail snapshot and separate investigation store; the replay loop starts from a suspect step and the API retains verdicts/evidence/reviews. Planned extensions remain dashed and labelled. No reference branding/content, performance figures, deployment claim or integration was adopted. The source PDF is not redistributed. See the [reference analysis](../../deliverables/stage-2-fyp1-final/poster-support/v4/reference-review.md) and [architecture notes](../../deliverables/stage-2-fyp1-final/poster-support/v4/architecture-notes.md).

The v4.0 master has 110 live PSD text layers, 11 vector smart objects, 26 pt minimum type and 297 conservative tokens. Four standalone editable section sets are supplied. The display date remains removed. Physical proof, Photoshop/Corel application review, Figma synchronization and university approval/submission remain pending.
