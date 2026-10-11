# docs/manuals

The manuals the handbook requires, written so a person outside the team can install and operate Granite from a clean machine (handbook C.1.2):

| File | Content |
|---|---|
| `setup-manual.md` | configuration and setup: requirements, install, environment variables, first run, quality gates, Docker, deployment, continuous delivery |
| `tool-manual.md` | how to use the product: a first investigation, labels, inputs and limits, troubleshooting |
| `feature-catalogue.md` | every implemented feature with purpose, inputs, outputs, edge cases, code location and tests |
| `demo-runbook.md` | the Mid-1 demonstration, step by step, with expected values and failure cases |
| `coding-standards.md` | naming, comments, static analysis and test rules, each with the tool that enforces it |
| `code-walkthrough.md` | file and function level map of the code, likely questions, planned ownership |
| `system-test-cases.md` | generated catalogue of the system-level test cases (do not edit by hand) |
| `user-manual.md` | planned for FYP-1 final: how an end user performs the core journeys |
| `handover.md` | planned for FYP-2 final: source, build and run, dependencies, licences, credentials handling, known limits |

Each manual is tested by a non-owner before a milestone and linked from the report (implementation chapter). The rubric marks implementation documentation down if setup is not reproducible.
