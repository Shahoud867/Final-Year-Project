# Granite v4.0 — exact poster layout brief

This coordinate addendum describes the existing v4.0 exports. The separately supplied `granite_poster-brief_fyp1-final_draft.md` is the original historical brief; its grid and band geometry describe an earlier composition and must not be combined with the v4.0 coordinates below. This addendum records the export, rather than changing the handbook or project scope.

## Canvas and units

- Trim: **22.5 × 34.5 inches, portrait**; 1620 × 2484 print points; 6750 × 10350 pixels at 300 ppi.
- Origin: top-left of the trimmed canvas. Coordinates use x, y, width, height.
- Conversion: 1 inch = 72 pt = 300 px; multiply points by 25/6 for 300-ppi pixels. Fractional pixel values are intentional for vector geometry.
- Safe text margin: 54 pt = 225 px. Common card: x = 54 pt, width = 1512 pt; right edge = 1566 pt (6525 px).
- v4.0 uses local alignment grids, not the original brief’s uniform 12-column grid.
- No unconfirmed bleed is included; printer approval is required before adding bleed.

## Content group bounds

These are layer/container bounds, including intervening space. They differ from the opaque panel rectangles below.

| Group | x, y, width, height (pt) | x, y, width, height (300-ppi px) |
|---|---|---|
| 01 Opening | 0, 0, 1620, 426 | 0, 0, 6750, 1775 |
| 02 Team | 0, 426, 1620, 172 | 0, 1775, 6750, 716.667 |
| 03 System architecture | 0, 598, 1620, 858 | 0, 2491.67, 6750, 3575 |
| 04 Replay and feasibility | 0, 1456, 1620, 360 | 0, 6066.67, 6750, 1500 |
| 05 Vision and plan | 0, 1816, 1620, 360 | 0, 7566.67, 6750, 1500 |
| 06 Categorized technologies | 0, 2176, 1620, 308 | 0, 9066.67, 6750, 1283.33 |

## Opaque panels

| Panel | x, y, width, height (pt) | x, y, width, height (300-ppi px) | Fill |
|---|---|---|---|
| Header | 0, 0, 1620, 414 | 0, 0, 6750, 1725 | #10243E |
| Team | 54, 438, 1512, 142 | 225, 1825, 6300, 591.667 | #FDFCFA |
| Architecture | 54, 616, 1512, 822 | 225, 2566.67, 6300, 3425 | #FDFCFA |
| Evidence | 54, 1474, 1512, 324 | 225, 6141.67, 6300, 1350 | #FDFCFA |
| Plan | 54, 1834, 1512, 324 | 225, 7641.67, 6300, 1350 | #FDFCFA |
| Technology footer | 0, 2194, 1620, 290 | 0, 9141.67, 6750, 1208.33 | #FDFCFA |

## Local grids and architecture

All coordinates in this section are print points. Multiply by 25/6 for pixels.

- Common left content inset: x = 78 (325 px).
- Team columns: x = 78, 446, 814; supervisor x = 1190. Names y = 494; roll numbers y = 534; section label y = 454; supervisor divider x = 1166. Preserve roll-number ordering and the supervisor’s academic title.
- Header university logo: x = 54, y = 54, width = 52, height = 51.28. Reversed Fault Line lockup: contain proportionally within x = 20, y = 102, width = 432, height = 164. Institution text x = 126, y = 66; right-aligned metadata anchor x = 1564, y = 66. Goals start x = 1120; bullet labels x = 1142.

| Architecture component | x, y, width, height (pt) |
|---|---|
| Workbench | 78, 820, 330, 112 |
| API / jobs | 510, 820, 600, 112 |
| Evidence store | 1212, 820, 330, 112 |
| Workflow parent | 78, 1006, 1110, 146 |
| Model adapter | 1290, 1014, 252, 138 |
| Retail snapshot | 78, 1268, 330, 116 |
| Check facts | 510, 1268, 292, 116 |
| Trace source | 858, 1268, 292, 116 |
| Replay test | 1206, 1268, 336, 116 |

- Five workflow nodes: x = 90, 312, 534, 756, 978; y = 1024; width = 194; height = 110. Labels: Intake (AI), Order Lookup (TOOL), Policy (CODE), Refund Calculator (AI), Writer (AI).
- Three plan cards: x = 78, 574, 1070; y = 1970; width = 472; height = 176. Horizontal gaps = 24 pt (100 px). Status/title/outcome/details y = 1984 / 2024 / 2070 / 2110.
- Four technology-column centres: x = 261, 627, 993, 1359; pitch = 366 pt. Category labels y = 2254; logos y = 2297 with 48 pt box height; names y = 2359; roles y = 2399. Dividers x = 444, 810, 1176.

## Strata and Fault background

Bottom group: **Background**; subgroups in stacking order: Base, Strata, Fault channel, Evidence thread. Content panels and text sit above it. Hard edges only; no added gradients, shadows, blur, texture or decorative accents.

| Property | pt | 300-ppi px |
|---|---|---|
| Channel begins below header | 414 | 1725 |
| Channel turn y | 1456 | 6066.67 |
| Channel end y | 2194 | 9141.67 |
| Left channel centre x | 24 | 100 |
| Right channel centre x | 1596 | 6650 |
| Channel width | 14.4 | 60 |
| Thread width | 1.44 | 6 |
| Stratum height | 496.8 | 2070 |
| Right-hand stratum displacement | -14.4 | -60 |

Thread follows the square-corner path (24,414) → (24,1456) → (1596,1456) → (1596,2194). Four solid discs have radius 2.88 pt / 12 px (24 px diameter), at the following centres:

| Disc | x, y (pt) | x, y (300-ppi px) |
|---|---|---|
| 1 | 24, 438 | 100, 1825 |
| 2 | 24, 616 | 100, 2566.67 |
| 3 | 1596, 1474 | 6650, 6141.67 |
| 4 | 1596, 1834 | 6650, 7641.67 |

The last two discs are on the right-hand channel, as requested. Strata alternate Paper #F3F1EC and #EFECE5 in five 496.8 pt / 2070 px bands; right-hand edges sit 14.4 pt / 60 px higher. Channel #E9E5DC; thread/discs #0A66D6. Opaque cards #FDFCFA; ink #10243E. No text or diagram depends on the faint strata being visible.

## Typography, identity and accuracy

- Live body/display fonts: Inter Medium/Bold; evidence numerals: JetBrains Mono Bold. Minimum live text size in this export: 26 pt. The exact styles and text coordinates are in the supplied layout JSON.
- Preserve the original Fault Line logo geometry, proportions and colours. Reversed disc is #7CC0FF on ink; never use #0A66D6 on ink.
- Preserve BS (DS), FAST NUCES, Islamabad Campus, team roll order and Dr. Adil Majeed’s title/name.
- Built and Planned statuses remain explicit. Keep recorded replay evidence separate from the limited feasibility pilot; preserve the printed caveats. Do not reintroduce the removed Early Feasibility date.
- Existing diagram SVGs are supplied unchanged as reference assets. They are not substitutes for the current poster’s simplified architecture or proof of every planned feature.

## Source and handoff

Exact per-text geometry and all diagram drawing paths: `poster-layout.json` (copied unchanged from the v4.0 poster support source). The v4.0 poster SVG remains the visual source for reconstruction.

The FAST-NUCES asset in this bundle is the existing 433 × 427 px repository JPG. A genuine SVG/vector PDF was not found in the repository; the university homepage also links to `/Content/images/NU-logo.jpg`. This bundle does not disguise a raster logo as vector artwork.

Physical proof printing, one-metre readability, printer settings and Photoshop/CorelDRAW application review remain separate final checks.
