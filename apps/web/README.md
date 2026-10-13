# web

React and TypeScript front end (Vite): an investigation workbench for the Granite API. Hash routing, no router library and no component library. Three small runtime packages besides React: `lucide-react` (icons) and two self-hosted fonts (Inter, JetBrains Mono), listed in the [dependency register](../../docs/registers/dependency-licence-register.md). Dark theme by default; the sun button switches to a light theme for projectors.

| Screen | Route | File |
|---|---|---|
| Investigations: telemetry, findings and runs, trace inspector | `#/` | `src/pages/Home.tsx` |
| Task Studio: three scenarios, form or JSON input, fault and execution mode, pipeline preview | `#/new` | `src/pages/NewRun.tsx`, `src/components/StudioPreview.tsx` |
| Pipeline trace: outcome, pipeline graph, step inspector, observed vs source of truth, checks | `#/runs/{id}` | `src/pages/RunDetail.tsx`, `src/components/StepInspector.tsx`, `CheckDetail.tsx` |
| Verification lab: lifecycle, ranked hypotheses and causal map, experiments, decision, evidence | `#/findings/{id}` | `src/pages/FindingDetail.tsx`, `src/components/Verify.tsx`, `Outcome.tsx`, `EvidenceLedger.tsx`, `Replay.tsx` |
| How it works: features F1 to F8 with inputs and outputs, levels, rule VR-1 explorer, lifecycle rules | `#/guide` | `src/pages/Guide.tsx`, `src/components/Vr1Explorer.tsx` |
| Evidence: silent-failure contrast, mechanisms, comparison, built and planned, CI/CD status | `#/evidence` | `src/pages/Evidence.tsx`, `src/delivery.ts` |

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
```

Tests (`tests/`, Vitest and Testing Library) use real API payloads captured from a recorded run (`tests/fixtures.ts`). Accessibility: axe-core runs on every screen in `tests/a11y.test.tsx`, with both sparse and full payloads. Screenshots of the running system: [`evidence/demos/`](../../evidence/demos/).

Not done yet: colour contrast measured in a real browser for the new palette, a manual screen-reader pass, browser end-to-end tests in CI, and a usability test with people outside the team ([protocol](../../docs/manuals/usability-check-protocol.md)).
