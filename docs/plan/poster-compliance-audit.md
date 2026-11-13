# Granite poster compliance audit

Reviewed 13 November 2026 against the latest **v2.1 print exports**, the team's expanded poster checklist in chat, and `bs-fyp-handbook-2026.pdf`. The complete 86-page handbook was searched for poster references; relevant text and tables on pages 7, 11–13, 17, 22, 25 and 39 were reviewed. The actual poster preview and exported PDF/JPEG/PSD were inspected again.

**Finding:** no mandatory poster content is missing from the supplied checklist. The digital dimensions and required source/image formats are present. The complete submission process cannot yet be marked finished: physical one-metre readability, Photoshop application compatibility, printer coordination, supervisor approval and submission to the committee remain unverified. The linked Figma frame still shows v2.0; the v2.1 background is available in the exported files.

## Requirement-by-requirement findings

| Requirement | Evidence in v2.1 | Finding |
|---|---|---|
| 22.5 × 34.5 inches | Main PDF is 1620 × 2484 points; JPEG and PSD are 6750 × 10350 pixels, 300 ppi. | Verified. |
| Portrait | Height exceeds width in every primary print export. | Verified. |
| Condensed, concise representation | 218 conservative whitespace tokens including the outlined project name; 197 lexical words. Short phrases, three goal bullets and diagrams replace paragraphs. | Present; no handbook numerical word limit. |
| Project name and original logo | Granite title with the supplied Fault Line combination logo. Registered full title is also shown. | Present. |
| Concise objective | “Find the source of silent AI failures.” Goals explain detection, source location and fix verification. | Present. |
| Architecture or visual problem overview | Wrong refund versus catalogue total; AI workflow → Check → Trace → Replay → Human review. | Both are present. |
| Plan and tentative deliverables | Investigate → Guide repairs → Extend, with concrete workbench, investigation, import and evaluation outcomes. | Present at the bottom. |
| Iterative timeline | Three numbered, connected increments, each producing a developed outcome. Built and Planned labels distinguish status. | Present as an ordered iteration sequence; §7 does not require calendar dates or a Gantt chart. |
| Team and supervisor | Shahoud Shahid (23i-2515), Muhammad Noor Ul Haq (23i-2520), Saif Shahzad (23i-2634); Dr. Adil Majeed. | All present; ascending roll-number order; professional title, no “Sir” or “ma’am”. |
| Co-supervisor / industry partner if applicable | Neither is identified in available project records. | Conditional; no person or partner invented. |
| University name and logo | FAST NUCES, Islamabad Campus and the repository university logo. | Present. |
| Degree identification | BS (DS). | Verified; no BS (CS) in extracted poster text. |
| Tools and technologies | Python, FastAPI, React, TypeScript, Ollama. | Present in footer. |
| Recommended placement | Title, registered title, team and supervisor at top-left; goals at top-right; plan and tentative deliverables at bottom. | Present. The handbook uses “may” for these placements; the poster follows them. |
| Text large enough at one metre | PDF minimum 26 pt, body labels mainly 28–36 pt, headings 48–80 pt, hero monetary figures 104 pt. | Digital sizes verified; actual viewing-distance test pending. |
| Spacing and alignment | All PDF text remains within a 0.75-inch text-safe margin; every text bounding box is on an opaque panel. Consistent alignment and open section gaps. | Digitally verified / visually reviewed. §7 gives no numerical spacing rule. |
| Illustrations and original graphics | Exact project logo, five-block workflow, refund comparison and replay-result marks. | Present; screenshots are examples in §7, not a required poster element. |
| Spelling and capitalised terms | Copy visually reviewed, including proper names, FAST NUCES, BS (DS), FastAPI, TypeScript, Ollama and the monetary/results values. | No spelling error found in this review; team confirmation of personal names remains part of sign-off. |
| Visibility | Prominent problem statement and values; content grouped on opaque panels with spacing. | Design review passed; final evaluation remains the faculty panel's judgement. |
| Consistency | Shared fonts, alignment, label sizes, colour meanings and block/arrow conventions. | Design review passed. |
| Attention | Clear title → problem → workflow → evidence → plan hierarchy, with restrained colour emphasis. | Design review passed. Animations are not necessary for a printed poster. |
| Perception / legibility | Plain block labels; check/cross marks and text reinforce colour; body copy is separated from the background. Navy body text on the opaque card has measured contrast 15.24:1. | Digital review passed; print test pending. |
| Original Photoshop/Corel file plus JPEG | Native PSD contains 65 live text layers and 11 embedded vector smart objects; full-resolution JPEG is supplied. | Files and structure verified; opening and inspecting the PSD in Photoshop remains pending. |
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

1. Print the [text-legibility crops](../../deliverables/stage-2-fyp1-final/granite_poster-crop-tests_fyp1-final_v2.1.pdf) at **Actual size / 100%** and read them from one metre. Correct any labels that fail this physical test.
2. Print the [margin and band-gap proof](../../deliverables/stage-2-fyp1-final/granite_poster-background-crops_fyp1-final_v2.1.pdf) at **100%**. Check the faint background and thread on the chosen printer.
3. Open the original PSD in Photoshop with the supplied fonts and confirm that live text, vectors and colour render correctly. Structural checks and cached previews have passed; an application open test has not been performed.
4. Confirm printer bleed, colour profile and delivery settings. The supplied artwork is exact trim size with no unconfirmed bleed.
5. Obtain supervisor approval and submit the required source file plus JPEG through the committee's announced channel and deadline.
6. Apply and visually verify the background in Figma before treating that file as the same revision as v2.1. This is version synchronization, not an additional handbook requirement. The previous direct edit was blocked by Figma's Starter-plan tool-call limit, and the fallback upload was blocked by the environment.

## Evidence

- [Handbook source](../../references/university/bs-fyp-handbook-2026.pdf), especially §7 p.17, acceptance p.7 and Form 4 p.39.
- [Latest poster preview](../../deliverables/stage-2-fyp1-final/granite_poster-preview_fyp1-final_v2.1.jpg).
- [Print PDF](../../deliverables/stage-2-fyp1-final/granite_poster_fyp1-final_v2.1.pdf).
- [Delivery files and Figma status](../../deliverables/stage-2-fyp1-final/README.md).
- [Production checks and geometry](../../deliverables/stage-2-fyp1-final/poster-support/v2.1/poster-production-checks.json).

No poster content, typography, implementation claim, schedule or approval status was changed during this compliance review.
