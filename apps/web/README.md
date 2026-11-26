# web

React and TypeScript front end (Vite): an investigation workbench for the Granite API. Hash routing, no router library and no component library. Three small runtime packages besides React: `lucide-react` (icons) and two self-hosted fonts (Inter, JetBrains Mono), listed in the [dependency register](../../docs/registers/dependency-licence-register.md). Light theme by default (it suits projectors); the moon button switches to a dark theme.

| Screen | Route | File |
|---|---|---|
| Inbox: totals in one line, findings by who acts next (Needs you, Verifying, Decided, All) with lead suspect, evidence ladder and verdict, a quick look, recent runs | `#/` | `src/pages/Home.tsx`, `src/components/QuickLook.tsx` |
| Runs: every run with server-side filters and a quick look | `#/runs` | `src/pages/Runs.tsx` |
| New run (top-bar button): three scenarios, form or JSON input, fault and execution mode, pipeline preview | `#/new` | `src/pages/NewRun.tsx`, `src/components/StudioPreview.tsx` |
| Run: outcome contrast, then tabs Trace (graph, steps with their checks under each name, step inspector), Checks (outcome and step groups, failures first) and Data (raw trace) | `#/runs/{id}` | `src/pages/RunDetail.tsx`, `src/components/StepInspector.tsx`, `CheckDetail.tsx` |
| Case file: section links, sticky rail (verdict with replay counts and interval, next step, exports, record), lifecycle, symptom, origin with Investigate, verification results, decision, evidence | `#/findings/{id}` | `src/pages/FindingDetail.tsx`, `src/components/Verify.tsx`, `Outcome.tsx`, `EvidenceLedger.tsx`, `Replay.tsx` |
| Style guide: every component in every state (development builds, or `VITE_STYLEGUIDE=1`) | `#/styleguide` | `src/pages/StyleGuide.tsx` |
| Fault Lab: generate runs over chosen faults and clean runs on chosen tasks; detection per condition | `#/lab` | `src/pages/Lab.tsx` |
| Evaluation: benchmark results with Wilson intervals, baselines, coverage and nondeterminism ablations | `#/evaluation` | `src/pages/Evaluation.tsx` |
| How it works: features F1 to F8 with inputs and outputs, levels, rule VR-1 explorer, lifecycle rules | `#/guide` | `src/pages/Guide.tsx`, `src/components/Vr1Explorer.tsx` |
| Why Granite (was Evidence): silent-failure contrast, mechanisms, comparison, built and planned, CI/CD status | `#/evidence` | `src/pages/Evidence.tsx`, `src/delivery.ts` |

## How it is put together

| Part | Where | Note |
|---|---|---|
| Design tokens and shared styles | `src/styles/` (`tokens.css` first), entry `src/styles.css` | Colours only through tokens. Each page has its own file in `src/styles/pages/` |
| Components | `src/components/ui.tsx` | Badge, Card, Tabs, Drawer, JsonView, Compare and the rest. Status is always an icon and a word, never colour alone |
| Pipeline graph | `src/components/Graph.tsx` | Inline SVG drawn at real pixel size: left to right when the container is wide enough, top to bottom otherwise. Linear workflows only; a graph for branching workflows is planned for FYP-2 |
| API client and types | `src/api.ts`, `src/types.ts` | Errors arrive as readable sentences (RFC 7807 problem bodies) |
| Rule VR-1 and the lifecycle, as drawn | `src/lib/vr1.ts`, `src/lib/lifecycle.ts` | Copies for explanation only: verdicts and allowed actions always come from the server. Two server tests fail if these copies drift (`apps/api/tests/test_platform.py`) |
| Delivery evidence | `src/delivery.ts` | Build stamp written by `vite.config.ts`; workflow runs read from GitHub's public API with no credentials. Unreachable means "unknown", never "passed" |

Rules the interface keeps: every number, verdict, hash and interval on screen comes from the API; nothing is animated as progress unless the server reported it; a recorded cassette, a live model and an injected fault are always labelled; planned features are marked "Planned".

```bash
npm ci
npm run dev        # http://localhost:5173, forwards /api to http://127.0.0.1:8000 (set GRANITE_API_URL to change)
npm test && npm run lint && npm run typecheck && npm run build
GRANITE_PYTHON=<python with the Granite packages> npm run e2e   # after a build: browser journey against the real API
```

Tests (`tests/`, Vitest and Testing Library) use real API payloads captured from a recorded run (`tests/fixtures.ts`). Accessibility: axe-core runs on every screen in `tests/a11y.test.tsx`, with both sparse and full payloads. The browser journey (`e2e/journey.e2e.ts`, Playwright) starts the API in recorded mode, serves the built interface, walks a silent failure from New run to an accepted case at desktop and phone width, and measures colour contrast in the real browser in both themes; locally it uses the installed Chrome, in CI Playwright's Chromium. Screenshots of the running system: [`evidence/demos/`](../../evidence/demos/).

Not done yet: a manual screen-reader pass and a 200% zoom check, the browser journey's first run on GitHub, and a usability test with people outside the team ([protocol](../../docs/manuals/usability-check-protocol.md)).
