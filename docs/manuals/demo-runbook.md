# Demo runbook: Mid-1 supervisory meeting

| | |
|---|---|
| Version | 1.1 |
| Date | 2026-10-14 |
| Status | Screen names and steps were updated for the redesigned interface on 2026-10-14; Part A and cases B1, B2, B3, B6 and B8 were walked through in a browser on that date, the other rows keep their check of 2026-10-11. Every step and every expected value below was checked against the product in recorded mode (saved real answers of `llama3.2:3b`): in a browser, through the HTTP API of the same running server, or by the system test named in the row. Live mode is optional and depends on a local model |
| Length | 12 minutes of demo, 3 minutes of code |
| Rubric | Criterion 3 asks for a live core module **with edge or failure cases shown**; a happy path alone is capped at 16 to 20 of 25. Part B is not optional |

## Before the meeting

| When | Do | Expect |
|---|---|---|
| Day before | `git pull`; follow the [setup manual](setup-manual.md) sections 2 and 3 on the demo laptop | Server starts; <http://127.0.0.1:8000> shows "Server online" and "Recorded cassette" in the sidebar |
| Day before | `pytest tests/system` | 22 passed |
| Day before | Each member runs Part A alone once (the plan requires every member to be able to) | About 4 minutes |
| 10 minutes before | Start the server with a fresh database (delete `apps/api/.granite/granite.db`, or set `GRANITE_DB_URL` to a new file) | Empty lists |
| 10 minutes before | Open three tabs: the product, `/docs`, and the [design pack](../../deliverables/stage-1-fyp1-mid/granite_design-pack_fyp1-mid_v1.0.html) | |
| If the laptop fails | Use the deployed URL (see the [deployment record](../registers/deployment-record.md)); otherwise a second laptop set up the day before | The public demo shows the interface of the last deployed commit; **Evidence** in the product shows which commit that is |

Recorded mode needs no network and no model (only the CI/CD panel on the Evidence page reads GitHub, and it says "status unknown" when offline). Do not switch to "Live model" in the meeting unless Ollama is running and was tested that morning.

## Part A. The investigation (6 minutes)

Say first, in one sentence: *"A refund workflow of five AI agents gives an answer that looks fine and is wrong by 23 cents. Granite finds which agent introduced the error and proves it."*

| # | Do | Expected on screen | Say |
|---|---|---|---|
| 1 | **How it works** | The seven-step flow, eight cards with "What it accepts" and "What you get" (F1 to F7) and the F8 card | This answers the panel's comments on unclear features and inputs. The limits printed here are tested against the server |
| 2 | **Task Studio** → scenario **Silent price discrepancy** (`#W1023987`, Luggage Set and Pet Bed; fault *Stale price*). Execution mode: *Recorded cassette*. **Run workflow** | Pipeline trace, status *completed*. The reply promises a refund of **$662.00**. "Output monitoring sees" three green rows; a red **Silent failure** notice | The answer looks complete and polite. Nothing crashed. This is what ordinary monitoring would report as healthy |
| 3 | Look at **Pipeline**, **Observed vs source of truth** and **Checks**; select Order Lookup to open the step inspector | Order Lookup, Refund Calculator and Writer are red. `CHK-OUT-1` fails: observed 662, expected **662.23**. The inspector shows that `truth.catalog_total` returned 662.23 | The check compares the refund with the catalogue, which the workflow does not control. No answer key |
| 4 | **Investigate** | *Hypotheses ready*, **V1**. The decision card is locked. Five ranked suspects with the causal map above them. First: **Order Lookup**, score 0.81, "output contradicts the source of truth: 661.98 against 662.23". Second: Refund Calculator, 0.72 | The ranking comes from the recorded data flow and the step checks. The injected fault is hidden from it |
| 5 | **Verify** on Refund Calculator (row 2) | **Refuted**: 0 of 5 fix replays correct | Fixing the calculator alone does not fix the answer, so it is not the origin. A wrong guess is rejected by evidence |
| 6 | **Verify** on Order Lookup (row 1) | **Confirmed**, **V2**: 5/5 correct with the fix, 0/2 in the controls, interval 57% to 100%, shown as replay marks, a rate axis and the rule's conditions | Rule VR-1: at least 80% with the fix, at most 20% without. The controls show it was the fix, not luck. Five replays give a wide interval; we state it |
| 7 | **Your decision** → Accept | *Accepted*, **V3**. Review history shows who and when | A person closes the finding, never the software |
| 8 | **Evidence** → **View** on one item; **Download report (.md)** | Each record shows "hash matches" and its SHA-256; a Markdown report downloads | Every claim on this page can be re-checked from stored, hashed records |

## Part B. Edge and failure cases (4 minutes)

Pick at least three. All were verified on 2026-10-11.

| # | Case | Do | Expected | Test |
|---|---|---|---|---|
| B1 | Invalid input | Task Studio: message `hi`, order number `12`, **Run workflow** | Nothing is sent to the workflow (the form refuses it first; the server refuses the same input with the same words). "Enter at least 3 characters" and "Must look like #W1234567" appear under the fields | SYS-ERR-01 |
| B2 | Clean run, no false alarm | Scenario **Clean baseline** | Completed, refund **$662.23**, all checks pass, **no finding** | SYS-CORE-02 |
| B3 | The model has no answer | Task Studio: choose a scenario, change the message to any other sentence, recorded mode | Run *errored* at Intake with the reason ("this exact request was never recorded") and **Run again** / **Change the task** buttons. The server keeps working | SYS-ERR-04 |
| B4 | Verification that cannot be completed | On the finding from Part A, **Verify** on Intake (row 3) | *error, no verdict*: "2 replay(s) needed model answers that are not in the recording". The finding stays open. The product does not guess | API test `test_a_replay_with_no_recorded_answer…` |
| B5 | Skipping the process | On a **new** finding (run the second example with the fault), there is no Accept button before verification. In `/docs`, `POST /api/findings/{id}/reviews` with `accept` | 409 "Action not allowed in this state" | SYS-ERR-03 |
| B6 | A fault that changes nothing | Scenario **Cancelled-order edge case** (`#W1106948`) | The refund is refused either way: one step check fails, the outcome is right, **no finding**. Granite reports silent failures, not every deviation | Verified by hand 2026-10-11 and 2026-10-14 |
| B7 | Restart | Stop the server (Ctrl+C), start it again, reload | The finding, its evidence and its hashes are still there | SYS-REL-01 |
| B8 | Phone width | Narrow the browser to about 390 px | Every screen reflows with no sideways scroll; the pipeline graph turns vertical (defect D-14, fixed 2026-10-14); navigation moves to a bar at the bottom | [screenshot](../../evidence/demos/2026-10-14_pipeline-trace-phone-390px.png) |

**If asked "what does not work?"** answer directly: one workflow and one fault type; personal data is not redacted before storage (D-07, synthetic data only); no usability test with real users; the feasibility run is 10 tasks. The list is in the [defect list](../registers/defect-list.md).

## Part C. Code and process (3 minutes)

| Show | Where | Point |
|---|---|---|
| The verdict rule | `packages/granite_core/granite_core/verification.py`, function `decide` | A short function; thresholds are named constants; the decision table is tested case by case |
| One test failing on purpose | Change `CONFIRM_MIN_RATE` to `0.9`... then `pytest packages/granite_core/tests/test_verification.py` | Four tests fail and name the decision-table rows (checked 2026-10-11). Put it back |
| Design matches code | [Design pack](../../deliverables/stage-1-fyp1-mid/granite_design-pack_fyp1-mid_v1.0.html) → Finding state machine; then `lifecycle.py` `TRANSITIONS` | The diagram is generated from that table; CI fails if they differ |
| CI | **Evidence** in the product (Delivery pipeline), then GitHub → Actions → latest run | The page reads the latest CI and CD runs from GitHub live. Lint, types, tests, security, container smoke test. State which run is green and what has changed since |
| Panel actions | [Form 10 register](../registers/form-10-panel-actions.md) | Each action, status, evidence link |

## Questions to expect

The [code walkthrough](code-walkthrough.md) section 4 lists likely questions with the file that answers each. Two to prepare in your own words, because the rubric marks them directly:

1. **"Who wrote this?"** Most code came from AI-assisted sessions, logged in the [AI usage log](../registers/ai-usage-log.md) and Form 13. Then explain the module you own without the screen.
2. **"Why does one account have all the recent commits?"** Say what happened and what changes from now (branches and pull requests per member, [CONTRIBUTING](../../.github/CONTRIBUTING.md)). Do not explain it away.
