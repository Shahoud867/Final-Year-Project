# Granite FYP-1 poster: master design prompt

| | |
|---|---|
| Status | Draft v2 for the team and the supervisor (11 November 2026). Revised after a line-by-line check against handbook section 7: Band 6 now holds FYP-1 Final deliverables only, the problem statement is bullets, the copy was cut to 460 counted words, the type floor is one value (22 pt), and the screenshot requirement was removed (the handbook only suggests "screen captures" as an example). Items marked **[CONFIRM]** must be checked before printing |
| Not done yet | **No poster file exists.** This is a specification. The handbook's deliverables (the Photoshop/Corel file and a JPEG) have not been produced |
| Deadline | Poster submission **15 November 2026** (supervisor approval first) |
| Handbook | `references/university/bs-fyp-handbook-2026.pdf`, section 7 (p. 17), Step 4 (p. 7), FYP-1 Process Step 4 (p. 13), Form 4 (p. 39) |

Give everything from "MASTER PROMPT" to the end to the designer or AI design tool, together with the asset files listed in section 6.

---

## MASTER PROMPT

### 1. Project context and poster objective

Design the FYP-1 academic poster for **Granite**, a final-year project at FAST School of Computing, National University of Computer and Emerging Sciences (NUCES), Islamabad.

**What Granite is (verified, implemented):** an investigation workbench for multi-agent LLM workflows. Tagline: *find the failure, prove the cause, verify the fix.* When a workflow of several AI agents finishes "successfully" but gives a wrong answer (a **silent failure**), Granite:

1. **Runs** the workflow and records every agent step (Granite Trace v1).
2. **Checks** the outcome and each step with executable rules against an independent source of truth, so no answer key is needed.
3. **Detects** the silent failure and opens a finding.
4. **Traces back** along the recorded data flow and ranks the steps where the wrong value most likely began, without asking an LLM.
5. **Verifies** a suspect by controlled replay: the workflow is re-run from that step with the step corrected (N = 5 fix replays) and without the correction (M = 2 control replays), and the pre-registered rule **VR-1** decides *confirmed*, *refuted* or *inconclusive* with a 95% Wilson interval.
6. **Reviews:** a named person accepts or rejects the finding; the software never closes it.
7. **Records** every artefact as evidence with a SHA-256 hash that is re-checked on display, and exports a report.

**The running example (real, from the recorded system):** the Refund Desk, five agents (Intake, Order Lookup, Policy, Refund Calculator, Writer) handling a retail refund on tau-bench retail data. A stale price from the Order Lookup tool makes the Writer tell the customer **$662.00** when the catalogue total is **$662.23**. No error is raised anywhere. Granite's outcome check catches it, ranks **Order Lookup** first, confirms it with **5/5 fix replays correct and 0/2 controls correct (95% interval 57% to 100%)**, and refutes the innocent Refund Calculator (0/5).

**Poster objective, in priority order:**

1. In 10 seconds a passer-by understands the problem: *agents can fail silently, and the visible symptom is not where the error began.*
2. In 60 seconds a faculty panel sees the method, the verification rule and real results.
3. The poster reads as a product, but it is honest about what is built and what is planned.

**Audience:** the FYP faculty panel (Form 4: "poster format, layout, style, contents", 10 marks) and visitors at an open display, viewing at about 1 metre.

### 2. Mandatory handbook compliance (bs-fyp-handbook-2026.pdf)

These override every creative choice.

| # | Requirement (handbook wording or paraphrase) | Where | How this design meets it |
|---|---|---|---|
| H1 | **Poster size must be 22.5" × 34.5"** | §7 | Canvas 22.5 × 34.5 in (571.5 × 876.3 mm) |
| H2 | **Orientation should be Portrait** | §7 | Portrait; 22.5 in wide |
| H3 | Don't use too much text; highlight major points; use bullets | §7 | Hard word budget: **at most 480 words in total** (the copy in section 5 counts 460; recount the real file). Every list is a bullet list; the only prose lines are titles, captions and one-line labels |
| H4 | Font large enough to read from **a metre away** | §7 | Body 32 pt; **no text under 22 pt anywhere** (section 7 table, section 11 and Q9 all use this one value) |
| H5 | Use illustrations: maps, pictures, photos, design drawings, diagrams, tables, charts, graphs, screen captures | §7 | Diagrams (the investigation flow and the pipeline), one chart (the replay results and rate axis), the $662.00 vs $662.23 comparison, icons. Screen captures are optional and not used |
| H6 | Spell check, including capitalised words that spell checkers skip | §7 | QC checklist item Q3 |
| H7 | **Top-left:** title of the project, names of the group members and the supervisor(s) | §7 | Header, left block |
| H8 | **Top-right:** project goals | §7 | Header, right block "Project goals" |
| H9 | **Bottom:** project plan and list of tentative deliverables **for the final FYP-1 evaluation** | §7 | Band 6 lists the FYP-1 Final deliverables only. **No FYP-2 content appears in the bottom band** (the FYP-2 poster is a separate, updated version: handbook Table 1b, week 8) |
| H10 | Creativity allowed within the guidelines: fonts, colours, backgrounds, graphics | §7 | Section 4 |
| H11 | Don't include too much information; rely on answering questions | §7 | One message per band; at most 480 words; the header carries only what H7 and H8 name; detail is left to the demo |
| H12 | **Submit the original Photoshop/Corel file together with a JPEG image** | §7 | Deliverables: `.psd` (or `.cdr`) and `.jpg` (section 10) |
| H13 | Recommended tools: Adobe Photoshop or Corel Draw. **A group using another tool is responsible for printing the poster itself** | §7 | Build the final file in Photoshop (section 10) |
| H14 | Posters are accepted **only after supervisor approval**; the committee verifies the format | p. 7 Step 4; p. 13 | QC item Q1 |
| H15 | Poster evaluation in week 13 on open display, or at the FYP-1 final evaluation | p. 13 | The poster must stand alone without a presenter |

**Points the handbook does not settle (flagged, do not assume):**

- **F1 [CONFIRM] Logo and branding.** The handbook sets no rule for logos, colours or a university template on posters. The design places the FAST/NUCES logo in the header. Ask the FYP coordinators whether an official template or logo placement exists. The only logo in the repository (`docs/report/ThesisFigs/FASTLogo.jpg`) is **433 × 427 px**, which is about 1.4 in at 300 dpi. Obtain a high-resolution or vector logo, or keep it at most 1.4 in wide.
- **F2 [CONFIRM] Bleed and print resolution.** The handbook names no bleed, colour mode or resolution. Ask the university printer. This prompt assumes 300 dpi, a 0.125 in bleed on every side and a 0.75 in safe margin.
- **F3 [CONFIRM] "Tentative deliverables for the final FYP-1 evaluation"** (H9). The seven deliverables in Band 6 come from `docs/plan/fyp1-completion-plan.md`, which the supervisor has **not yet agreed**. Confirm the list, and cut any item the team does not expect to show at the Final, before printing. A longer list than the team can deliver is worse than a shorter honest one.
- **F4 [CONFIRM] Registered title vs built scope.** The registered title is *"A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery"*. Automatic repair and recovery are **not yet implemented** (planned). The title must appear as registered. Nothing else on the poster may imply that self-healing or automatic repair works today. Ask the supervisor whether the title should be revised.
- **F5 [CONFIRM] SDG.** The proposal documents name **SDG 9, Industry, Innovation and Infrastructure (target 9.5)**. Confirm that this is what was registered.
- **F6 [CONFIRM] Test count.** 451 automated tests were **collected** on `main` on 11 November 2026: 209 core, 49 workflow, 73 API, 22 system and 98 web. State the number only if CI on `main` is green on the print date.

### 3. Poster specifications

| Item | Value |
|---|---|
| Trim size | 22.5 × 34.5 in, portrait (571.5 × 876.3 mm) |
| Canvas at 300 dpi | **6750 × 10350 px** (trim). With 0.125 in bleed: 6825 × 10425 px [CONFIRM bleed, F2] |
| Safe margin | 0.75 in = **225 px** from trim on every side; no text or logo outside it |
| Grid | 12 columns, column 415 px, gutter 120 px; column *n* starts at x = 225 + (n − 1) × 535 (col 1: 225, col 5: 2365, col 6: 2900, col 8: 3970, col 9: 4505, col 12 ends at 6525) |
| Baseline unit | 40 px (0.133 in); every vertical space is a multiple of 40 |
| Band gap | 120 px between bands |
| Colour mode | Design in RGB (sRGB); soft-proof and export as the printer requires [CONFIRM F2] |

### 4. Creative direction and visual identity

**Concept: "The evidence board."** A forensic investigation laid out on clean paper. Six bands read top to bottom, like a case file:

> symptom → method → proof → product → plan.

One thin **evidence thread**, a 6 px blue line with small node dots, runs down the left edge from band 2 to band 5. It connects the bands and echoes the "trace back" idea.

**Impression to create:** a credible engineering tool from a serious team. Calm, precise and data-led, like a well-designed observability product page, not a marketing flyer.

**Visual language:** the poster uses the **same palette, fonts and status colours as the product interface** (`apps/web/src/styles/tokens.css`, light theme), so the poster and the product look like one system. Colour always carries a meaning:

| Role | Name | HEX | Use only for |
|---|---|---|---|
| Background | Paper | `#F3F1EC` | Whole poster background |
| Panel | Card | `#FDFCFA` | Section cards, with a 2 px `#DED9CF` border and 24 px corner radius |
| Sunken | Well | `#E9E5DC` | Diagram wells and the metric tiles |
| Header | Deep ink | `#10243E` | Header band background only (white text on it, contrast 15:1) |
| Ink | Text | `#1C1A17` | Headings and body |
| Ink 2 | Secondary | `#403C36` | Captions, labels |
| Rule | Line | `#DED9CF` | Dividers, borders |
| Verification | Replay blue | `#0A66D6` | Replays, VR-1, the evidence thread, links; "origin confirmed" |
| Failure | Signal red | `#D12B1F` | Failed check, symptom, the wrong value ($662.00), the "✕" marks |
| Suspect | Amber | `#B26A00` | Suspected origin, injected fault |
| Passed | Green | `#1A8C3C` | Checks passed, "✓" marks, the correct value ($662.23), a confirmed verdict |
| Soft tints | 10 to 16% of the colour above on Card | | Backgrounds of status chips and diagram zones |

Contrast: body text `#1C1A17` on `#FDFCFA` is about 16:1; `#403C36` on `#FDFCFA` is about 10:1. Status colours appear as text only at 32 pt bold or larger, and always next to an icon or a word, never as colour alone.

**Typography (free, OFL licence):**

- **Inter** (variable) for every heading and body text.
- **JetBrains Mono** for numbers, IDs, check names (CHK-OUT-1), money values and code-like labels.
- Install both in Photoshop before starting. Use no other typeface.

**Background:** flat Paper `#F3F1EC`. One very faint dot grid (2 px dots, `#DED9CF`, 80 px pitch) appears only behind Band 3. No photographs, gradients, glass, glow, bevels or drop shadows other than the card shadow: 0 8 px 24 px, `#1C1A17` at 8%.

**Iconography:** line icons in the style of Lucide (the product uses Lucide): 6 px stroke at poster scale, rounded caps, in the colour of their meaning. Icons needed: play (Run), list-checks (Check), siren (Detect), route (Trace back), flask (Verify), gavel (Review), fingerprint (Record), check-circle, x-circle, lock (frozen step), wrench (patched step), repeat (re-run step), shield-check, database (source of truth).

### 5. Section-by-section layout (reading order) and exact content

Word budget for the whole poster: **at most 480 words, target 450**. The copy below is the final wording. Counted by script over every printed string (including diagram labels and chart captions): header 49, goals 33, Band 2 85, Band 3 85, Band 4 78, Band 5 77, Band 6 42, footer 11, **460 words** in total. That is 20 under the cap, so there is room for corrections but not for new content. Re-count in the real file, and cut before adding anything. y values are pixels from the top of the trim at 300 dpi.

---

#### Band 1. Header (y 0 to 1500; full width, background Deep ink `#10243E`)

**Left block (cols 1 to 8, x 225 to 4385), top to bottom (handbook H7):**

- **Logo row:** the FAST/NUCES logo at most 1.4 in tall (F1), 225 px from the left and top trim. Beside it, in white Inter 600 at 36 pt, one line: "FAST School of Computing, NUCES Islamabad".
- **Wordmark:** "Granite" in Inter 800, 150 pt, white. Directly under it, the tagline in Inter 500, 44 pt, `#9CC4F5`: "find the failure · prove the cause · verify the fix".
- **Registered title** in Inter 600, 54 pt, white, at most 2 lines: "A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery" (F4).
- **Team line** in Inter 500, 32 pt, white at 85%: "Shahoud Shahid (23i-2515) · Muhammad Noor Ul Haq (23i-2520) · Saif Shahzad (23i-2634)".
- **Supervisor line**, same style: "Supervisor: Dr. Adil Majeed · Project F26-060 · BS (CS) FYP 2026" [CONFIRM degree label].

**Right block, "Project goals" (cols 9 to 12, x 4505 to 6525; handbook H8):** a white-outlined panel (2 px white at 40%, radius 24 px, inner padding 80 px) headed "PROJECT GOALS" in Inter 700, 30 pt, letter-spacing +8%. Four goals, each a numbered line of up to 9 words in Inter 500, 32 pt, white:

1. Detect silent failures in agent workflows
2. Locate where the error began
3. Prove the cause by controlled replay
4. Keep a person in charge, with evidence

Below the goals, the chip "UN SDG 9 · Industry, Innovation and Infrastructure" (F5): white outline, 26 pt.

The header holds only what handbook H7 and H8 name, plus the logo. Leave at least 120 px of space between the wordmark, the registered title and the team line so six stacked items do not read as a block of text.

---

#### Band 2. The problem: "It looked fine. It was wrong." (y 1620 to 3420; card, full width)

- **Kicker** "01 · THE PROBLEM": Inter 700, 28 pt, `#0A66D6`, letter-spacing +8%.
- **Heading** "It looked fine. It was wrong.": Inter 800, 72 pt.

**Left (cols 1 to 5):** four bullets, Inter 400, 32 pt, each with a small red or amber dot icon (never a prose paragraph):

- Agents pass a wrong value along silently
- The run completes; no error is raised
- Blame lands where it showed, not where it began
- One lucky re-run can pass a wrong fix

**Right (cols 6 to 12): the hero visual "Two views of the same run".** Two side-by-side panels joined by an arrow:

- **Panel A, "What output monitoring sees":** a Well panel listing three rows, each a green check-circle and 32 pt text: "Run status: completed", "Errors raised: none", "Reply: refund of $662.00". Footer chip: green "Looks healthy".
- **Arrow** (Replay blue, 8 px) labelled "Checked against the catalogue" (26 pt).
- **Panel B, "What Granite's check sees":** a red-outlined card holding a two-cell comparison:
  - "Told to the customer": **$662.00** in JetBrains Mono 600, 120 pt, Signal red.
  - "Catalogue total": **$662.23** in JetBrains Mono 600, 120 pt, Green.
  - Under it: "Difference −0.23 · CHK-OUT-1 failed" (JetBrains Mono, 32 pt).
  - Footer chip: red "Silent failure found".
- **Caption** (24 pt, `#403C36`): "Real Refund Desk run, recorded mode."

This band is the **primary focal point**: the largest numbers on the poster appear here.

---

#### Band 3. How Granite works (y 3540 to 5640; dot-grid background, no card)

- **Kicker** "02 · THE METHOD". **Heading** "Seven steps, four stages, one record" (72 pt).

**Top row (full width, height 520 px): the investigation flow.** Seven rounded-rectangle nodes (radius 20 px, Card fill, 2 px Line border), each with an icon above a 32 pt label: Run → Check → Detect → Trace back → Verify → Review → Record. They are connected by 6 px Replay-blue arrows and grouped under four stage brackets, each with a level badge in JetBrains Mono:

| Stage | Steps | Level badge |
|---|---|---|
| Detected | Run, Check, Detect | V0 |
| Traced | Trace back | V1 |
| Verified | Verify | V2 |
| Reviewed | Review, Record | V3 |

**Bottom-left (cols 1 to 8, height about 1300 px): "Where did it begin?" pipeline diagram.** Redraw from `docs/diagrams/refund-desk-dataflow.svg` in this palette.

- Six nodes left to right: Task input (dashed), Intake (LLM), Order Lookup (Tool), Policy (Code), Refund Calculator (LLM), Writer (LLM). Each node shows a small kind label (LLM / TOOL / CODE) in JetBrains Mono 22 pt above the agent name in Inter 600, 32 pt.
- **Order Lookup:** amber dashed ring plus the tag "SUSPECT → ORIGIN CONFIRMED" in Replay blue.
- **Writer:** red ring plus the tag "SYMPTOM".
- **Path:** draw Order Lookup → Policy → Writer as a thick 8 px Replay-blue path; other edges are 3 px `#BDB6A8`.
- **Failed-check marks:** red ✕ glyphs on Order Lookup, Refund Calculator and Writer; green ✓ on Intake and Policy.
- **Caption** (24 pt): "Symptom at Writer; error began at Order Lookup."

**Bottom-right (cols 9 to 12): "Three ideas".** Three stacked mini-cards, each with an icon, a title (Inter 700, 36 pt) and one sentence (32 pt, at most 9 words):

1. **Executable checks** (database icon): "Rules test each step against a trusted source."
2. **Deterministic attribution** (route icon): "Suspects ranked from the recorded data flow."
3. **Controlled replay** (flask icon): "Fix replays vs control replays, under a fixed rule."

---

#### Band 4. Proving the cause: rule VR-1 (y 5760 to 7560; card, full width)

- **Kicker** "03 · THE PROOF". **Heading** "One re-run proves nothing. Controls do." (72 pt).

**Left (cols 1 to 7): the replay experiment chart.** Two experiment rows, drawn from the real stored results:

- **Row 1, label "Order Lookup → CONFIRMED"** (green verdict chip):
  - "With the fix": five 64 px circles with green ✓ and the count "5/5 correct" (JetBrains Mono, 40 pt).
  - "Control, no fix": two 64 px rounded squares with red ✕ and "0/2 correct".
- **Row 2, label "Refund Calculator → REFUTED"** (grey verdict chip):
  - "With the fix": five red ✕, "0/5 correct".
  - "Control": two red ✕, "0/2 correct".
- **Rate axis under Row 1** (full chart width, 80 px tall, Well fill):
  - Ticks at 0%, 20%, 80% and 100% (JetBrains Mono, 24 pt).
  - A grey zone from 0 to 20% labelled "refute zone"; a green-tint zone from 80 to 100% labelled "confirm zone"; dashed lines at 20% and 80%.
  - A Replay-blue bar from 57% to 100% labelled "95% Wilson interval 57%–100%".
  - A blue dot at 100% for the fix rate and a grey diamond at 0% for the control rate.
- **Caption** (24 pt): "Real experiment: 5 fix replays, 2 controls."

**Right (cols 8 to 12): "Rule VR-1" box** (Replay-blue 3 px border):

- Three rule bullets with icons, 32 pt:
  - "Confirmed: ≥ 80% fix correct, ≤ 20% controls correct"
  - "Refuted: ≤ 20% fix correct"
  - "Otherwise: inconclusive"
- Then: "Rule fixed before any result" (28 pt).
- Under the box, two small trust badges side by side (26 pt, with icons):
  - **fingerprint** "SHA-256 hashed evidence"
  - **gavel** "A person decides"

---

#### Band 5. The product and what it achieved (y 7680 to 8880)

- **Kicker** "04 · BUILT AND MEASURED". **Heading** "A working product, measured honestly" (72 pt).

**No screenshots are required.** The handbook only lists "screen captures" as one example of an illustration (section 7), so Band 5 is built from the numbers alone. The page already has its visuals in Bands 2, 3 and 4. If the team later wants a screenshot (for example one cropped pipeline trace in the free space beside the engineering list), it is optional, and must come from the current light interface on `main`.

**Left (cols 1 to 8): "Pre-registered feasibility run (7 Oct 2026)":** a 3 × 2 grid of metric tiles. Each tile has the value in JetBrains Mono 600, 72 pt, and the label in Inter 500, 26 pt:

| Value | Label |
|---|---|
| 10/10 | faulty runs detected |
| 0 | false alarms on clean runs* |
| 10/10 | origin ranked first |
| 9/10 | origin confirmed by replay |
| 10/10 | innocent step refuted |
| 20/20 | runs completed |

Footnote (22 pt, `#403C36`): "*A genuine model error, not injected. 10 tasks, 1 fault type, 1 small model: a first test, not a benchmark."

**Right (cols 9 to 12): "Engineering":** four bullets with icons, 32 pt:

- "451 automated tests" (F6)
- "CI/CD on GitHub Actions"
- "Live on Render"
- "21 diagrams from the code"

---

#### Band 6. Plan and tentative deliverables (y 9000 to 9825; card, full width; handbook H9)

- **Kicker** "05 · PLAN". **Heading** "Plan to the FYP-1 final evaluation" (64 pt), followed by a dashed-outline chip "Planned" (26 pt) [CONFIRM F3].
- **Content: the tentative deliverables for the FYP-1 Final, as one bullet list in two columns** (cols 1 to 4 and cols 5 to 8; dashed 3 px outline around the list, hollow bullet dots because none of it is finished yet), 32 pt:
  - Fix values derived from failed checks
  - One-click verified investigation
  - Three fault types and a batch Fault Lab
  - Evaluation against baselines
  - Trace import
  - Regression-test export
  - Retail Agent on tau-bench tasks
- **Nothing about FYP-2 appears in this band.** The FYP-2 poster is an updated version of this file (handbook Table 1b, week 8), so build the PSD with named layers and a separate "Plan" group that can be swapped later. "What is done" is already shown in Band 5, so it is not repeated here.
- **Right end of the band (cols 9 to 12):** two QR codes, each 1.6 in with a 24 pt label: "Live demo" and "Source code". [CONFIRM that the repository should be public on the poster; the demo URL may not exist after graduation. QR codes are optional.]

---

#### Footer (y 9885 to 10125; full width, Deep ink strip of 240 px)

In white at 24 pt, centred: "F26-060 · BS Final Year Project 2026 · Python, FastAPI, React, TypeScript, Ollama" (the school and university are already in the header).

---

### 6. Visual assets (exact files)

| Asset | File | Use | Notes |
|---|---|---|---|
| University logo | `docs/report/ThesisFigs/FASTLogo.jpg` (433 × 427 px) | Header | Too small for large print; replace with the official high-resolution logo (F1) |
| Pipeline diagram source | `docs/diagrams/refund-desk-dataflow.svg` (vector) | Band 3 reference | Redraw in the poster palette |
| Investigation flow source | `docs/diagrams/investigation-flow.svg` | Band 3 reference | Redraw as the seven-node strip |
| VR-1 decision source | `docs/diagrams/vr1-decision.svg` | Band 4 reference | Thresholds must match: 80% / 20% / 20% |
| Replay plan source | `docs/diagrams/replay-plan.svg` | Optional inset in Band 4 | Frozen → patched → re-run |
| Screenshots | **None required** (handbook section 7 only lists screen captures as an example illustration) | none | If one is added anyway, capture it fresh from current `main` (light theme) at 3× scale. **Do not use** `evidence/demos/2026-10-14_*.png`: those show an earlier dark design |
| Numbers | `research/eval/results/2026-10-07_refund-desk-feasibility.md`; the stored experiment for the example run | Bands 2, 4, 5 | Copy exactly; no rounding beyond what is shown above |

### 7. Typography scale (at 100% print size)

| Element | Font | Weight | Size | Leading | Colour |
|---|---|---|---|---|---|
| Wordmark "Granite" | Inter | 800 | 150 pt | 1.0 | White |
| Registered title | Inter | 600 | 54 pt | 1.15 | White |
| Tagline | Inter | 500 | 44 pt | 1.2 | `#9CC4F5` |
| Section kicker | Inter | 700 | 28 pt, caps, +8% tracking | 1.2 | `#0A66D6` |
| Section heading | Inter | 800 | 72 pt (Band 6: 64 pt) | 1.1 | `#1C1A17` |
| Card title | Inter | 700 | 36 pt | 1.2 | `#1C1A17` |
| Body | Inter | 400 | 32 pt (never under 28 pt) | 1.35 | `#1C1A17` |
| Labels, captions | Inter | 500 | 24 to 26 pt (never under 22 pt) | 1.3 | `#403C36` |
| Hero values | JetBrains Mono | 600 | 120 pt | 1.0 | Red / Green |
| Metric values | JetBrains Mono | 600 | 72 pt | 1.0 | `#1C1A17` |
| IDs, check names | JetBrains Mono | 500 | 28 to 32 pt | 1.2 | `#403C36` |

Use sentence case everywhere except kickers. Left-align body text; never justify. Lines are at most 60 characters.

### 8. Diagram and chart rules

- Every diagram flows **left to right** (time and data flow) and every band **top to bottom**.
- Status meaning is always icon **plus** colour **plus** word: ✓ green "correct/passed", ✕ red "failed/still wrong", dashed amber "suspect", solid blue "origin confirmed", grey "refuted".
- Arrows are 6 to 8 px with a solid triangular head. Connectors never cross text.
- No screenshots are required. If one is added anyway, it comes from the current light interface on `main`, is cropped to one idea with no browser chrome, and its text stays readable at 1 m.
- **Charts show real values only:** 5/5, 0/2, 0/5, 57% to 100%, and the six feasibility metrics. Do not draw illustrative data.

### 9. Composition principles applied

- **Focal points:** primary, the $662.00 vs $662.23 comparison (Band 2); secondary, the replay marks and rate axis (Band 4); tertiary, the six feasibility numbers (Band 5).
- **Hierarchy:** wordmark, then section headings, then hero numbers, then body, then captions, in five clear size steps.
- **Gestalt:**
  - *Proximity:* each label within 40 px of its object.
  - *Similarity:* the same status colours and icons as the product.
  - *Continuity:* the evidence thread and the left-to-right flows.
  - *Common region:* cards group each idea.
- **Balance:** the left column is text-light and visual-heavy in Bands 2 and 4, alternating with right-heavy Bands 3 and 5 for a Z-rhythm.
- **Negative space:** at least 120 px between bands and 80 px of padding inside cards. The goal is about 35% empty area.
- **Cognitive load:** one message per band, stated in its heading; a reader can understand the poster from the headings and numbers alone.
- **Accessibility:** contrast at least 7:1 for body text; nothing is told by colour alone; no red/green pair without icons and words.

### 10. Print and export

1. Build the master in **Adobe Photoshop** (handbook H13). Use RGB, 300 ppi, 6750 × 10350 px trim, plus bleed if the printer confirms it (F2). Keep text as live type layers and import diagrams as vector smart objects.
2. Name the layers by band ("01 Header", "02 Problem" and so on) for review.
3. Soft-proof with the printer's CMYK profile [CONFIRM F2]. Blues `#0A66D6`/`#10243E` and green `#1A8C3C` shift most, so check them on screen against the proof.
4. **Deliverables (H12):**
   - `granite_poster_fyp1-final_v1.0.psd`
   - `granite_poster_fyp1-final_v1.0.jpg` (maximum quality, sRGB, full resolution)
   - a 1600 px-wide JPEG preview for the supervisor's review.

   Save them in `deliverables/stage-2-fyp1-final/`.
5. Print a **100% scale crop test** (an A4 section of Band 2 and Band 4) and read it at 1 m before ordering the full print.

### 11. Strict constraints and prohibited mistakes

- No landscape layout, and no size other than 22.5 × 34.5 in.
- No more than 480 words. No prose paragraph at all: lists are bullets, everything else is a title, caption or one-line label. No text under 22 pt.
- **No FYP-2 content in the bottom band** (handbook H9 says "for the final FYP-1 evaluation").
- **Content:**
  - No invented features, numbers or claims.
  - Nothing that implies automatic repair, recovery or "self-healing" already works (F4).
  - No "first", "best" or "outperforms" wording.
  - No comparison chart against named commercial products.
  - No competitor logos.
- **Visuals:**
  - No simulated UI, and no screenshots of the old dark interface (screenshots are optional).
  - No stock photos, robot or brain imagery, or AI-art illustrations.
  - No emoji, glassmorphism, neon glow, heavy gradients, gradient text or 3D effects.
  - No colour used for meaning other than as listed in section 4.
  - No low-resolution logo stretched beyond 1.4 in.
- **Process:** do not submit without the supervisor's approval (H14) and without both the PSD and the JPEG (H12).

### 12. Final quality-control checklist

| # | Check | Done |
|---|---|---|
| Q1 | Supervisor approved the final PDF/JPEG preview (H14) | ☐ |
| Q2 | Size 22.5 × 34.5 in, portrait; bleed as confirmed by the printer | ☐ |
| Q3 | Spell check passed, including capitalised words (CHK-OUT-1, VR-1, tau-bench, LangGraph, NUCES) | ☐ |
| Q4 | Top-left: title, all three members with roll numbers, supervisor. Top-right: goals. Bottom: plan and tentative deliverables (H7–H9) | ☐ |
| Q5 | Every number matches its source: $662.00, $662.23, 5/5, 0/2, 0/5, 57%–100%, M1–M6 | ☐ |
| Q6 | Planned items are labelled "Planned" and visually dashed; nothing planned looks finished | ☐ |
| Q7 | All [CONFIRM] items F1–F6 resolved | ☐ |
| Q8 | Word count counted in the real file: at most 480 | ☐ |
| Q8a | Band 6 lists FYP-1 Final deliverables only, each one the team expects to show; no FYP-2 content | ☐ |
| Q8b | No prose paragraph; every list is bullets | ☐ |
| Q9 | Body text 32 pt or more; nothing under 22 pt; readable at 1 m in the crop test | ☐ |
| Q10 | Every status shown with icon + word + colour | ☐ |
| Q11 | If any screenshot is used (optional): from the current light interface on `main`, at least 3× resolution, cropped to one idea | ☐ |
| Q12 | Logo is official and high resolution, or at most 1.4 in wide | ☐ |
| Q13 | PSD with live layers and full-resolution JPEG exported, named and saved in `deliverables/stage-2-fyp1-final/` | ☐ |
| Q14 | QR codes scan correctly from 1 m (if used) | ☐ |
| Q15 | Each member can explain every element on the poster | ☐ |
