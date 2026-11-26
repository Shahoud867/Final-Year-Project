# Accessibility audit, 2026-10-07

Scope: the four screens of the web UI (Investigations, New run, Run detail, Finding) with real data from a recorded run and a verified finding. Tool: axe-core 4.14.0 (Deque; MPL-2.0), run inside the built-in browser against the served production build.

Rule sets: WCAG 2.0 A and AA, 2.1 A and AA, 2.2 AA and axe best practices (desktop); WCAG 2.0 A/AA, 2.1 AA, 2.2 AA (phone width).

| Check | Light theme | Dark theme | Phone width 375 px |
|---|---|---|---|
| Investigations | 0 violations (33 rules passed) | 0 violations (33) | not rerun in axe; no page overflow |
| New run | 0 violations (34) | 0 violations (34) | no page overflow |
| Run detail | 0 violations (41); 1 rule "incomplete" (see below) | 0 violations (41); same incomplete | no page overflow |
| Finding | 0 violations (40) | 0 violations (40) | 0 page overflow |

**The one incomplete check (colour contrast on the pipeline graph's text).** axe cannot determine the background of SVG text drawn over shapes. The ratio was computed directly from the browser's computed colours for all 12 text elements: lowest 13.31:1 in the light theme and 11.94:1 in the dark theme (AA requires 4.5:1 for this text size). So this is a measured pass, not an axe pass.

**Defects this work found and fixed** (also in `docs/registers/defect-list.md`, found by the automated tests that now guard them in `apps/web/tests/a11y.test.tsx`): an empty table header in the Verify table (axe `empty-table-header`), and the graph exposed as an image while containing focusable steps (axe `nested-interactive`).

## Not covered (do not claim)

- No screen reader was used; no manual keyboard-only walkthrough was recorded beyond the graph test (Enter selects a step) and the form tests.
- WCAG criteria that need human judgement (meaningful link text in context, reading order, error identification quality, timing) are unchecked.
- Zoom to 400 percent and text-spacing overrides were not tested.
- Only the Chromium-based pane was used.
- axe finds roughly a third to half of WCAG failures automatically; passing it is evidence, not conformance.

Reproduce: serve the build (`GRANITE_STATIC_DIR=apps/web/dist`), copy `apps/web/node_modules/axe-core/axe.min.js` next to `index.html`, open each route, inject the script and call `axe.run()`. The jsdom version of the structural checks runs in `npm test`.
