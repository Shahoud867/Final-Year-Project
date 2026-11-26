# Test results, 2026-10-11

Produced by `python scripts/build_test_docs.py --run`, which executes every suite and parses the JUnit and coverage output. Nothing in this file is typed by hand.

| | |
|---|---|
| Commit | `5099243` on `main` **plus uncommitted changes in the working tree** |
| Python | 3.11.4 on win32 |
| Result | **381 of 381 tests passed** |

## Suites

| Suite (level) | Location | Tests | Passed | Failed | Skipped | Line coverage | Time |
|---|---|---|---|---|---|---|---|
| Core library (unit, property) | `tests` in `packages/granite_core` | 207 | 207 | 0 | 0 | 97.5% | 4.2 s |
| Refund Desk workflow (unit, integration) | `tests` in `workflows/refund_desk` | 49 | 49 | 0 | 0 | 95.4% | 0.6 s |
| API (integration, recorded model) | `tests` in `apps/api` | 71 | 71 | 0 | 0 | 96.8% | 23.5 s |
| System (black box over HTTP) | `tests/system` in `.` | 22 | 22 | 0 | 0 | n/a | 23.2 s |
| Web UI (component, accessibility) | `tests` in `apps/web` | 32 | 32 | 0 | 0 | n/a | n/a |

Coverage is line coverage of the package under test, measured by its own suite. Tests and code were written by the same author, so coverage shows the code does what was intended, not that the intent is right.

## System test cases

| ID | Test case | Result |
|---|---|---|
| SYS-CORE-01 | Full investigation of a silent failure (journey J1) | pass |
| SYS-CORE-02 | A clean run raises no alarm (journey J2) | pass |
| SYS-CORE-03 | Refute a wrong hypothesis, then confirm the right one | pass |
| SYS-CORE-04 | The run graph marks the failing steps | pass |
| SYS-CORE-05 | Runs and findings can be found again | pass |
| SYS-CORE-06 | The interface is documented by the running system | pass |
| SYS-CORE-07 | The web interface is delivered by the same server | pass |
| SYS-ERR-01 | Invalid input is refused with one message per field | pass |
| SYS-ERR-02 | Asking for something that does not exist | pass |
| SYS-ERR-03 | The lifecycle cannot be skipped | pass |
| SYS-ERR-04 | Recorded mode cannot answer a task nobody recorded | pass |
| SYS-ERR-05 | A hypothesis that cannot be tested is refused, not guessed | pass |
| SYS-ERR-06 | Limits are enforced | pass |
| SYS-ERR-07 | The language model is down | pass |
| SYS-SEC-01 | Every response carries the security headers | pass |
| SYS-SEC-02 | Evidence is append-only | pass |
| SYS-SEC-03 | Ground truth stays out of the evidence | pass |
| SYS-SEC-04 | With a token configured, nothing but health is public | pass |
| SYS-SEC-05 | Too many state-changing requests are throttled | pass |
| SYS-REL-01 | A restart loses nothing | pass |
| SYS-REL-02 | Concurrent work is not lost | pass |
| SYS-REL-03 | Recorded runs are reproducible | pass |

Specifications of these cases (steps and expected results): [`docs/manuals/system-test-cases.md`](../../docs/manuals/system-test-cases.md).
