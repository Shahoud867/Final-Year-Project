# Interface redesign into an investigation workbench, 2026-10-14

What was checked, how, and what was not. Answers panel action A1 ("UI/UX needs improvement") together with the [before/after record of 2026-10-13](2026-10-13_ui-before-after.md); the change itself is recorded as [C-04](../../docs/registers/change-log.md).

| | |
|---|---|
| State of the code | Branch `feat/web-workbench-redesign`, based on commit `336ca55`, **uncommitted** when these checks ran. Not merged, not deployed: the public demo still shows the earlier interface |
| Server | Local, recorded mode (saved answers of `llama3.2:3b`), a fresh SQLite database; the web app as a production build served by the API with its content-security policy |
| Browser | Headless Chrome driven over the DevTools protocol, viewport 1440 x 900 unless stated |
| Who | The AI assistant, in the session logged in the [AI usage log](../../docs/registers/ai-usage-log.md) (twenty-third session). No team member has repeated these checks yet |

## Screens

| Screen | Screenshot |
|---|---|
| Investigations (command center): telemetry, findings and runs, trace inspector | [2026-10-14_command-center.png](2026-10-14_command-center.png) |
| Task Studio: three scenarios, form or JSON, fault, execution mode, pipeline preview | [2026-10-14_task-studio-scenarios.png](2026-10-14_task-studio-scenarios.png) |
| Pipeline trace of the stale-price run: outcome contrast, pipeline, observed vs source of truth, checks | [2026-10-14_pipeline-trace-silent-failure.png](2026-10-14_pipeline-trace-silent-failure.png) |
| Step inspector for Order Lookup | [2026-10-14_step-inspector-order-lookup.png](2026-10-14_step-inspector-order-lookup.png) |
| Verification lab after two experiments and an accepted review | [2026-10-14_verification-lab-accepted.png](2026-10-14_verification-lab-accepted.png) |
| How it works: flow, features F1 to F8, rule VR-1 explorer, lifecycle rules | [2026-10-14_guide-features-vr1-explorer.png](2026-10-14_guide-features-vr1-explorer.png) |
| Evidence: silent-failure contrast, mechanisms, comparison, built and planned, CI/CD status | [2026-10-14_evidence-delivery-comparison.png](2026-10-14_evidence-delivery-comparison.png) |
| Phone width (390 px): verification lab, pipeline trace | [lab](2026-10-14_verification-lab-phone-390px.png), [trace](2026-10-14_pipeline-trace-phone-390px.png) |
| Light theme | [2026-10-14_verification-lab-light-theme.png](2026-10-14_verification-lab-light-theme.png) |

## Walk through the production build (all steps passed)

One scripted walk in the browser, each step asserted on what the page showed:

| Step | Result on screen |
|---|---|
| Task Studio, scenario "Silent price discrepancy", recorded mode, Run workflow | Order `#W1023987`, fault stale price; the pipeline trace opened with the "Silent failure" notice |
| Pipeline | Order Lookup marked as first-ranked suspect; its step inspector showed observed 661.98 |
| Investigate | Five suspects in the order Order Lookup, Refund Calculator, Intake, Policy, Writer; the decision card locked ("Available after a verification verdict") |
| Verify Refund Calculator | Refuted: "Fixing this step did not change the outcome (0/5 replays passed): it is not the origin." |
| Verify Order Lookup | Confirmed: fix replays correct 100%, controls correct 0%, 95% interval 57% to 100% |
| Reject with no reason | Refused in the form: "Please say why (at least 5 characters)." |
| Accept with a name and a comment | Status Accepted, level V3 |
| Evidence | 14 records, 14 hashes verified |
| Investigations | The tiles counted the new run and the reviewed finding |
| Evidence screen | Latest CI and CD runs on `main` and the release tag `v0.1.0-mid1` read from GitHub, all "success" at that moment |
| Console | No error, exception or blocked request. (A first walk found one: an inlined font blocked by the content-security policy, defect D-28, fixed before this one) |

## Other checks

| Check | Result |
|---|---|
| Sideways scroll, six screens at 390, 768 and 1024 px | 0 px on all 18 |
| Web tests (`npm test`) | 112 passed in 13 files, including axe-core on every screen with sparse and with real payloads |
| Lint, types, production build, `npm audit` | Clean; build 377 kB script (114 kB gzip), 55 kB styles; no known vulnerability |
| Python suites with the two new anti-drift tests; system tests against the new build | Core, Refund Desk and API suites passed (API coverage 96.8%); 22 system tests passed |
| ruff, mypy strict, bandit, architecture rule, generated-file checks, traceability | Clean |

## Not checked

- No person outside the team has used the redesigned interface. The [usability protocol](../../docs/manuals/usability-check-protocol.md) has not been run, so "improved" is still a claim.
- Colour contrast of the new palette was not measured in a browser (the automated accessibility tests run without layout). The token values were chosen to meet WCAG AA by calculation only.
- No manual screen-reader pass.
- Live-model mode was not exercised (no local model was running); only recorded mode.
- The container image was not built locally, so the build stamp passed by `cd.yml` and by Render is untested there. A local build showed the stamp `336ca55`.
- Nothing was run on GitHub Actions for this branch.
