# web

React and TypeScript front end (Vite). No UI library and no router library, to keep dependencies few. Light and dark themes follow the system setting; the pipeline graph and all forms are keyboard-operable.

| Screen | File |
|---|---|
| Investigations (findings and runs) | `src/pages/Home.tsx` |
| New run (example loader, fault, model mode, progress) | `src/pages/NewRun.tsx` |
| Run detail (pipeline graph, step inspector, checks, injected fault shown separately) | `src/pages/RunDetail.tsx` |
| Finding (stepper, ranked hypotheses with Verify, results, review, hashed evidence, report download) | `src/pages/FindingDetail.tsx` |

API client with readable errors: `src/api.ts`. Screenshots of the running system: [`evidence/demos/`](../../evidence/demos/).

```bash
npm ci
npm run dev        # http://localhost:5173, forwards /api to http://127.0.0.1:8000 (set GRANITE_API_URL to change)
npm test && npm run lint && npm run typecheck && npm run build
```
Accessibility: automated axe-core checks run in `npm test` and passed in a real browser (light, dark, phone width; record in [`evidence/reports/`](../../evidence/reports/2026-10-07_accessibility-audit.md)). Not done yet: manual and screen-reader audit, browser end-to-end tests, usability test.
