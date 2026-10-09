# Tool manual: using Granite

| | |
|---|---|
| Version | 0.9 draft |
| Date | 2026-10-07 |
| Status | Written from the working system (screens in `evidence/demos/`). Not yet tried by a person who did not build it |

Granite helps you find out **where** a multi-agent workflow went wrong when nothing crashed. It runs a workflow, checks the result against what is known to be true, follows the wrong value back to the step where it first appeared, proves the diagnosis by replaying, and records your decision. Setup is in [`setup-manual.md`](setup-manual.md).

## The example workflow: Refund Desk

A customer writes in to return items. Five steps handle it: **Intake** (a language model reads the message), **Order Lookup** (a tool reads the order), **Policy** (code decides eligibility), **Refund Calculator** (a language model adds up the prices), **Writer** (a language model writes the reply). The data are synthetic retail orders.

The built-in fault, **stale price**, makes the lookup tool report a price 0.25 too low for a requested item, without any error. Everything after it behaves correctly on the wrong input, so the customer receives a polite message with the wrong amount. That is a *silent failure*.

## A first investigation (about two minutes in recorded mode)

1. Open **New run**. Under "Load an example" choose the first entry; the form fills in. Leave "Inject a fault" on *stale price* and "Language model" on *Automatic*. Press **Run workflow**.
2. The **run page** shows what the customer asked, what the workflow replied and the pipeline. Red steps failed a check. Click a step to see exactly what it received and produced. Below, **Checks** lists each check with its result.
3. Open the finding under "Findings from this run". The page header shows the status (for example *Hypotheses ready*) and a level **V0 to V3** (below).
4. Under **Where did it begin?** the steps are ranked, each with the reason (for example "Order Lookup's output contradicts the source of truth: observed 661.98, expected 662.23"). Press **Verify** on a row. Granite replays the run from that step with the correct value (N times) and without it (M controls). The page shows progress, then a result card.
5. A step that is **not** the origin is *Refuted* (fixing it changed nothing); try the second row to see it. The true origin is *Confirmed*: with the fix the outcome was right in all replays and without it in none.
6. Under **Your decision** enter your name and press **Accept**, **Reject**, or **Ask for more information**. A comment is required to reject, to ask for information, to close without fixing, and to accept a finding whose verdict was *Inconclusive*. Asking for information is recorded but does not change the status. After accepting you can mark the finding **Resolved** or close it without fixing.
7. Under **Evidence** every record shows a SHA-256 and "hash matches". **Download report (.md)** saves the whole investigation as a text file. Tools can fetch the same report as JSON from `/api/findings/{id}/report?format=json`.

On the **Investigations** page the findings list can be searched by title and filtered by severity and verification level (press Search); it shows 25 at a time with **Show more**. If a run stops early, the run page shows the reason with **Run again**.

## What the labels mean

| Term | Meaning |
|---|---|
| Run | One execution of the workflow on one task, with every step's inputs and outputs recorded |
| Check | A statement of what correct looks like, evaluated on the run. Outcome checks look at the final result; step checks look at one step |
| Finding | An outcome check failed. *Silent failure*: the run completed. *Explicit error*: the run stopped |
| Hypothesis | A step that might be where the failure began, ranked from the recorded data flow |
| Replay and control | A re-run from a step. With the fix = replay; without = control. Controls show the fix, not luck, made the difference |
| Verdict | *Confirmed*, *Refuted*, *Inconclusive* (not clear; run more replays) or *Error* (replays could not finish), by the fixed rule VR-1 |
| V0 | Detected by a check, not yet reproduced |
| V1 | Supported by evidence, not replay-verified |
| V2 | Verified by controlled replays |
| V3 | Confirmed by a human reviewer |
| Evidence | A stored, hashed record behind a claim. Records are never edited |

## Inputs and limits

| Field | Rule |
|---|---|
| Customer message | 3 to 2000 characters |
| Customer e-mail | must look like name@example.com |
| Order id | must look like #W1234567 |
| Replays with fix (N) | 1 to 10; default 5 |
| Controls (M) | 0 to 5; default 2 |

Recorded mode can only run the 12 example tasks (the answers were saved for those exact messages). To try your own message, start Ollama and choose *Live model*.

## When something goes wrong

| Message | What it means | What to do |
|---|---|---|
| "Cannot reach the Granite server" | The API is not running | Start it (setup manual, section 3) |
| "Please fix the highlighted fields" | An input is invalid | Read the message under each field |
| "...never recorded... use live mode" | Recorded mode with a task nobody recorded | Choose an example, or use live mode |
| "model endpoint unreachable or too slow" | Ollama is down or slow | `ollama serve`; try **Test model** |
| "Cannot be verified automatically" | The workflow defines no repair for that step | Judge from the evidence; Policy and Writer have no automatic replay |
| "Action not allowed in this state" | The finding's status does not permit it (for example accepting before any verification) | The page offers only allowed actions |
| Verdict *Inconclusive* | Replays were not clear-cut | Verify again with more replays |

## For developers

The same functions are available over HTTP; the interactive reference is at `/docs` on the running server. Errors follow RFC 7807 (`application/problem+json`) and always include a `request_id`.
