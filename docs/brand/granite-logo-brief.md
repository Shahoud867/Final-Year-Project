# Granite logo: analysis, concepts and master design prompt

| | |
|---|---|
| Version | 0.1 draft |
| Date | 2026-11-13 |
| Status | Proposal from an AI-assisted session, **not yet agreed by the team**. The mark was built and rendered as SVG (see [`granite-mark-concept.svg`](granite-mark-concept.svg)); it is a concept to refine, not a finished logo |
| Not checked | Current competitor logos could not be loaded in this session (no web access), so section 4 rests on general knowledge. **Run a trademark and look-alike search before adopting any mark.** The "Granite" name meaning in section 1 is a proposed story: the repository records only that the name was chosen to be permanent |

## 1. Project and brand identity (from the repository)

**What the product is.** Granite is an investigation workbench for multi-agent LLM workflows: *find the failure, prove the cause, verify the fix.* When agents finish a run that looks fine but is wrong (a silent failure), it checks the outcome against an independent source of truth, ranks the step where the error began from the recorded data flow, tests that suspect by replaying the workflow with and without the fix under a pre-registered rule, and records everything as hashed evidence that a person accepts or rejects.

**Who uses it.** Engineers and QA staff running agent workflows on real data (support agents, back-office automation), plus reviewers and auditors who need traceable evidence (Project Vision, section 3).

**What makes it different.** It proves a cause instead of suggesting one: executable checks, deterministic tracing, controlled replay with controls, a person who decides, and evidence that cannot be edited.

**The name.** The proposal documents say only that "Granite" was chosen as a permanent short title. A fitting meaning, to be agreed: granite is bedrock, hard, crystalline and long-lasting, which matches the *source of truth* the checks are judged against and the evidence you can build on. A second reading: geologists drill core samples to trace layers back to where something changed, which is what the product does to a run.

**Personality to express.** Precise, forensic, calm, trustworthy, quietly confident. Not playful, not futuristic, not "AI magic". It should look like a tool an engineer would trust with an incident.

**What to avoid.** The current in-app mark is a stock icon (a mountain from the Lucide library, on a slate tile) and the earlier Stage-0 mockups used a plain "G" tile. Neither is distinctive; both should be replaced once a mark is chosen.

## 2. Three concepts

| | Concept | Idea | What it shows |
|---|---|---|---|
| A | **Fault Line** | A faceted stone block split by one stepped gap; the right half sits higher than the left; a ring with a coloured disc sits in the left half | The gap is the **trace path** (it steps down, across, down, like a data flow). The raised half is where the failure **showed up**. The disc upstream is the **origin** the trace finds. A fault is also a geological term, so the stone reads as granite |
| B | **Core Sample** | A horizontal cylinder cut into five strata, one slightly shifted and hollow | Five agents as layers; the shifted layer is the origin. **Risk:** reads as a battery, a progress bar or a "layers" icon |
| C | **Crystal G** | A letter G built from faceted planes with a stepped notch and a dot | Spells the name and suggests crystal. **Risk:** faceted gems and monograms are everywhere in AI branding, and it needs more detail to work |

**Comparison (1 = weak, 5 = strong; the author's judgement, not test results):**

| Criterion | A Fault Line | B Core Sample | C Crystal G |
|---|---|---|---|
| Meaning tied to what the product does | 5 | 3 | 2 |
| Simplicity (two shapes and a disc) | 5 | 4 | 2 |
| Holds up at 16 px | 4 | 3 | 2 |
| Originality in this domain | 4 | 2 | 2 |
| Works in one colour | 4 | 4 | 3 |
| Pairs with a plain wordmark | 5 | 4 | 3 |

**Selected: A, Fault Line.** It carries the product's whole story in one silhouette (a failure that shows downstream, a trace that leads back, a located origin) without a magnifier, an eye, a network graph or a gradient.

**Honest weaknesses of A.** It is not a letter, so recognition depends on repeated use. Rendered at a small size without the ring, the disc can look like a "record" button; in one colour the ring reads a little like a radio button; and, like any split rectangle, it could be mistaken for a page or bookmark. A first version with rounded corners was rejected because it looked like an app icon, not stone; the chamfered corners below fixed that.

## 3. Construction of the selected mark (geometry verified by rendering)

Work in a **96 × 96 unit grid**. The mark occupies **x 8 to 88, y 6 to 90**, so it is 80 wide and 84 high, centred on (48, 48). All coordinates are exact; the files [`granite-mark-concept.svg`](granite-mark-concept.svg), [`granite-mark-concept-mono.svg`](granite-mark-concept-mono.svg) and [`granite-favicon-concept.svg`](granite-favicon-concept.svg) contain them.

**Left piece (upstream, lower).** A polygon with points: (20,14) → (41,14) → (41,50) → (63,50) → (63,90) → (20,90) → (8,78) → (8,26) → close. The two outer left corners are **45° chamfers of 12 units**; every other corner is sharp (no rounding).

**Right piece (downstream, raised by 8).** Points: (47,6) → (76,6) → (88,18) → (88,70) → (76,82) → (69,82) → (69,44) → (47,44) → close. The two outer right corners are 12-unit 45° chamfers.

**The gap.** The pieces never touch. The gap is **6 units wide at every point**: 41 to 47 (first vertical run), 44 to 50 (horizontal run), 63 to 69 (second vertical run). It starts at the top edge, steps down, across and down, and ends at the bottom edge, so it reads as one continuous line. The raised right piece is the **fault displacement**: its top is 8 units above the left piece's top and its bottom is 8 units above the left piece's bottom.

**Origin marker.** A ring cut into the left piece (outer circle radius 10, centred (28,69), cut out of the piece) containing a solid disc (radius 7, same centre). The 3-unit ring of background around the disc is essential: it separates the disc from the stone. The disc is the **only coloured element**.

**Optical rules.** The disc sits in the upstream (left) piece on purpose: *the cause is upstream, the symptom shows downstream*. Do not move it into the right piece, centre it, or add a second marker. Keep the three gap segments the same width. Do not round the corners, add shadows or gradients.

**Small-size version (below 24 px, and for favicons).** Same pieces with a **10-unit gap**: left piece (20,14) → (39,14) → (39,52) → (61,52) → (61,90) → (20,90) → (8,78) → (8,26); right piece (49,6) → (76,6) → (88,18) → (88,70) → (76,82) → (71,82) → (71,42) → (49,42). A **solid disc of radius 12** at (26,70), **no ring**. Place it on an ink tile (96 × 96, corner radius 20) with the pieces in white scaled to 76% and centred, disc in light blue; this reads on light and dark browser tabs (rendered and checked at 16 and 32 px).

## 4. Competitors and originality

From general knowledge, **not re-checked today**: observability and agent-tooling brands commonly use animals or mythic birds (for example a phoenix or a dog), eyes and lenses, nodes-and-edges graphs, hexagons, stacked-layer icons, gradient orbs and sparkles (often purple to blue), circuit lines and brains. A mountain, the current in-app icon, is also a very common stock symbol.

**Avoid all of these.** The proposed mark uses none of them: no creature, no eye, no graph, no gradient, no stack of bars.

**Name collision to check.** IBM uses "Granite" for a family of AI models. That is a different product category, but search for it, and consider a descriptor in formal uses ("Granite, agent investigation workbench"). The team should decide whether this matters before any public use; the registered project name is unchanged here.

## 5. Typography and wordmark

- **Lockup type:** combination mark: the symbol plus the word **Granite**, sentence case (capital G only).
- **Typeface:** **Inter 4 variable** (free, SIL Open Font License, already used by the product), **optical size 32** (Display cut), **weight 640**, letter-spacing **−1% of the font size**, default kerning.
- **No custom lettering by default.** The mark carries the distinctiveness; a plain wordmark keeps the identity simple. *Optional variant:* replace the dot of the "i" with a disc of the same blue and diameter 0.15 em; use it only if the team wants a stronger link to the symbol (in rendering it looked fussy and the dot must be aligned by hand).
- **Proportions of the horizontal lockup (in grid units, symbol height 84):** wordmark cap height **40** (font size 55), gap between symbol and wordmark **28**, wordmark centred vertically on the symbol (cap top y = 28, baseline y = 68). The full lockup is about 3.4 times as wide as it is high.
- **Vertical lockup:** symbol centred above the wordmark; gap **24**; wordmark cap height **24**.

## 6. Colour

| Role | Name | HEX | Notes |
|---|---|---|---|
| Primary | Ink | `#10243E` | The stone. 13.8:1 on Paper, 15.6:1 on white |
| Accent | Origin blue | `#0A66D6` | The origin disc only. 4.8:1 on Paper, 5.4:1 on white. **Never on Ink** (2.9:1) |
| Light surface | Paper | `#F3F1EC` | The product's page colour |
| Reversed | White / Light blue | `#FFFFFF` / `#7CC0FF` | Stone white, disc light blue on Ink: 8.1:1 |
| One colour | Black, or Ink | | Whole mark including the disc in one colour |

Colour meaning: ink is the evidence, the single blue point is the located origin. They match the poster and the product interface (same tokens).

**Variations:** (1) primary, full colour on light; (2) reversed on Ink; (3) one colour, dark; (4) one colour, white, on photographs or dark; (5) icon only; (6) horizontal lockup; (7) vertical lockup; (8) small-size favicon tile (section 3).

## 7. Clear space and minimum size

- **Clear space:** 14 units (the diameter of the origin disc) on every side of the symbol; 20 units around a lockup.
- **Minimum sizes:** symbol alone 16 px / 5 mm using the small-size version; the standard symbol from 24 px / 8 mm; the horizontal lockup from 96 px wide / 25 mm.
- **Backgrounds:** Paper, white, Ink, and plain mid-tones. Not on busy images or gradients.

## 8. Export requirements

Editable **SVG** (outlined, one layer per piece, named "left", "right", "ring", "disc"), **vector PDF**, **transparent PNG** at 512, 1024 and 2048 px, a **favicon set** (SVG, 32 px PNG, 180 px apple-touch PNG, ICO with 16 and 32), a **social avatar** (1024 px, symbol on an Ink tile), and a **one-page usage sheet**. Convert text to outlines in the exported files and keep the live-text master. Check one-colour and 16 px renderings before sign-off.

## 9. Quality-control checklist

| # | Check | Done |
|---|---|---|
| 1 | Coordinates match section 3; the gap is 6 units wide at all three runs | ☐ |
| 2 | Chamfers are 12 units at 45°; no other corner is rounded | ☐ |
| 3 | Exactly one coloured element (the disc); ring is transparent or background-coloured | ☐ |
| 4 | Disc is in the left (upstream) piece | ☐ |
| 5 | Legible and recognisable at 16 px using the small-size version | ☐ |
| 6 | One-colour and reversed versions render correctly; origin blue never on Ink | ☐ |
| 7 | No eye, magnifier, graph, hexagon, bird, gradient, glow, shadow or sparkle | ☐ |
| 8 | Wordmark is Inter 640, opsz 32, −1% tracking, sentence case | ☐ |
| 9 | Clear space and minimum sizes respected in every lockup | ☐ |
| 10 | Trademark and look-alike search done; name collision decision recorded | ☐ |
| 11 | The team agrees the meaning of the name and the mark | ☐ |
| 12 | Old mark (Lucide mountain) replaced in the app, favicon, poster and report only after sign-off | ☐ |

## 10. Master prompt (give this to a designer or AI design tool)

> **Task.** Design the logo for **Granite**, an investigation workbench for multi-agent AI workflows (*find the failure, prove the cause, verify the fix*), for engineers and QA staff who debug AI agents that fail silently. Deliver a vector mark and a combination logo. Personality: precise, forensic, calm, trustworthy. Not playful, not futuristic.
>
> **Concept: "Fault Line".** One faceted stone block, split by a single stepped gap, drawn on a 96 × 96 grid. Left piece (upstream): polygon (20,14) (41,14) (41,50) (63,50) (63,90) (20,90) (8,78) (8,26). Right piece (downstream, raised 8 units): polygon (47,6) (76,6) (88,18) (88,70) (76,82) (69,82) (69,44) (47,44). The two outer corners on each side are 45° chamfers of 12 units; all other corners are sharp. The pieces never touch; the gap is exactly 6 units wide along its whole stepped path and runs from the top edge to the bottom edge. The gap represents the trace path of a data flow; the raised right piece represents where the failure shows up. In the left piece, cut a ring (outer radius 10, centre (28,69)) and place a solid disc (radius 7, same centre) inside it: the located origin of the failure. The disc is the only coloured element and must stay in the left piece.
>
> **Colour.** Stone `#10243E`; disc `#0A66D6`. Reversed on `#10243E`: stone `#FFFFFF`, disc `#7CC0FF`. Also one-colour black and one-colour white. Never put `#0A66D6` on `#10243E`.
>
> **Wordmark.** "Granite", sentence case, Inter 4 variable, optical size 32, weight 640, letter-spacing −1%, colour `#10243E`. Horizontal lockup: symbol height 84 units, wordmark cap height 40, gap 28, wordmark centred vertically on the symbol. Vertical lockup: gap 24, cap height 24.
>
> **Small-size version.** Gap 10 units, solid disc radius 12 at (26,70) with no ring, white pieces at 76% on an ink tile (96 × 96, corner radius 20), disc `#7CC0FF`.
>
> **Clear space and size.** Clear space of 14 units around the symbol, 20 around a lockup. Minimum: 16 px (small-size version), 24 px (standard symbol), 96 px wide (horizontal lockup).
>
> **Avoid.** Eyes, magnifying glasses, nodes-and-edges graphs, hexagons, birds or other animals, mountains, stacked-layer icons, gradients, glows, shadows, sparkles, circuit lines, brains, rounded app-icon corners, and any second accent colour.
>
> **Deliver.** Editable SVG (named layers left, right, ring, disc), vector PDF, transparent PNG at 512 / 1024 / 2048 px, favicon set, 1024 px avatar, and a one-page usage sheet showing all variations, clear space and minimum sizes. Build from the supplied SVG geometry; do not redraw freehand. Check the 16 px, one-colour and reversed versions before delivering.
