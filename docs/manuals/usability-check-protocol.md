# Usability check protocol (panel action A1)

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-10-13 |
| Purpose | Measure whether people outside the team can use Granite without help. Closes the gap in [Form 10](../registers/form-10-panel-actions.md), action A1: "no usability test with people outside the team" |
| Scope | The Mid-1 product (Refund Desk workflow, recorded mode). A small pilot, not the full acceptance test planned for FYP-2 (master plan 27.6) |
| Results | One file per session set in `evidence/uat/`, named `YYYY-MM-DD_usability-check-results.csv`, plus the summary printed by `python scripts/score_usability.py <file>` |

## 1. Thresholds, fixed before any session

Written down now so the result cannot be bent to fit afterwards (the same rule as the feasibility run).

| Measure | Threshold | Why this number |
|---|---|---|
| Tasks completed without help | at least 80% of all task attempts | A common pass mark for a first usability test |
| Mean SUS score | at least 68 | 68 is the published average across many SUS studies; above it means "better than average usability" |
| Task 3 ("where did it begin?") completed without help | at least 2 of 3 participants | This is Granite's core idea; if people cannot find the cause, the main screen needs rework |

A result below a threshold is reported as it is, with the screens to fix. It is still evidence.

## 2. Participants

- **Three people outside the team**, for example classmates in BS(CS) or BS(SE) who have not worked on Granite. Not the supervisor.
- They are **proxies** for the target users (developers and reviewers of AI workflows). Say so in the report.
- Record each one only as **P1, P2, P3** with a one-line role ("BS(CS) 7th semester, has used ChatGPT APIs"). No names, no recordings in git.

## 3. Setup (before each session)

1. Open https://granite-demo.onrender.com a minute early so the free server is awake, or run it locally (setup manual, section 3).
2. Start from the **Investigations** page in a fresh browser tab. Do not leave a finding open from the last participant.
3. Have a timer (phone stopwatch), this sheet and the results CSV ready.
4. One team member moderates and does not help; a second (optional) writes notes.

## 4. Consent (read aloud, then ask "Do you agree?")

> "We are testing our final-year project, not you. You will do five short tasks on a website while saying what you think. If you get stuck, that tells us what to fix. It takes about 15 minutes. We will write down whether each task worked, how long it took, and your comments, under a code like P1 with no name. Nothing is recorded on video. You can stop at any time."

Write "consent given" and the date in the CSV.

## 5. Moderator script

> "Granite is a tool for checking the work of a team of AI agents. In this example, five AI agents handle a customer who wants a refund. Sometimes they give a wrong answer that looks right. Please think aloud as you work. I can't help during the tasks, but you can say 'I give up' at any time."

Read each task exactly as written. Start the timer when you finish reading; stop it when the participant says they are done or gives up. Give **no hints** unless the participant has been stuck for 2 minutes; if you hint, the outcome is **A** (assisted).

## 6. Tasks

| # | Read this to the participant | Success means (do not read this out) |
|---|---|---|
| T1 | "Start a new check using the first example customer request (order W1023987), with the fault called 'stale price' switched on, and wait until it finishes." | A run reaches status *completed* (checked on 2026-10-13: this example gives one finding, Order Lookup ranked first, verdict Confirmed) |
| T2 | "The agents finished without any error. Is their answer to the customer correct? How can you tell?" | Says the refund amount is wrong, pointing at a failed check or the finding (not "it's fine because it completed") |
| T3 | "Find out which agent caused the problem." | Names **Order Lookup** (the first-ranked step on the finding page) |
| T4 | "Prove that this agent really is the cause, and tell me what the result means." | Starts verification on Order Lookup and explains the *Confirmed* result in their own words (fixing that step made the answer correct) |
| T5 | "You agree with the finding. Record your decision and download a report of it." | Finding status becomes *accepted* and the report file is downloaded |

Outcome codes per task: **S** success without help, **A** success after a hint, **F** failed or gave up. Also write down the **seconds** taken and anything they said that shows confusion (exact words are best).

## 7. SUS questionnaire (after the tasks)

Ask the participant to rate each statement from **1 (strongly disagree) to 5 (strongly agree)**. Read them in this order, without explaining them. This is the standard System Usability Scale; "system" means Granite.

1. I think that I would like to use this system frequently.
2. I found the system unnecessarily complex.
3. I thought the system was easy to use.
4. I think that I would need the support of a technical person to be able to use this system.
5. I found the various functions in this system were well integrated.
6. I thought there was too much inconsistency in this system.
7. I would imagine that most people would learn to use this system very quickly.
8. I found the system very cumbersome to use.
9. I felt very confident using the system.
10. I needed to learn a lot of things before I could get going with this system.

**Scoring** (done by the script): for odd items take (answer − 1), for even items take (5 − answer); add the ten values and multiply by 2.5. The result is 0 to 100.

Finish with two open questions and write the answers down word for word: "What was the most confusing part?" and "What one thing would you change?"

## 8. Recording the results

Copy [`usability-results-template.csv`](usability-results-template.csv) to `evidence/uat/YYYY-MM-DD_usability-check-results.csv` and fill one row per participant. Then:

```bash
python scripts/score_usability.py evidence/uat/YYYY-MM-DD_usability-check-results.csv
```

It prints a Markdown summary (task success, times, SUS per participant and mean, each threshold met or not). Save that output as `evidence/uat/YYYY-MM-DD_usability-check-summary.md`, add the three most important confusions with the screen to fix, and update Form 10 A1 and the milestone log (item 17) with a link to it.

## 9. Limits to state in the report

Three participants find the most common problems but give wide uncertainty on any number; they are proxies, not real users; the moderator is a team member; the tasks follow the happy path of one workflow. The full acceptance test with 5 to 8 participants is planned for FYP-2.
