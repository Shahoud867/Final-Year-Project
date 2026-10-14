# Defect list

| | |
|---|---|
| Version | 1.1 |
| Date | 2026-10-11 |
| Status | Live. Defects found by tests or by use are recorded here with how they were found; fixed ones stay listed |
| Severity | high: wrong result or data loss; medium: wrong behaviour with a workaround, or a requirement not met; low: cosmetic or process |

## Fixed

| ID | Severity | Defect | Found by | Fix |
|---|---|---|---|---|
| D-01 | medium | The stale-price fault always hit the first item of the order instead of the item the customer asked to return, because the runner gave a fault only the step's declared reads | A workflow test that requests the third item | The runner now gives faults the full harness view (task and all earlier outputs); regression test added |
| D-02 | medium | On a clean run, steps whose checks had passed could outrank unchecked steps in the structural ranking | Property-style test on a clean trace | Structural score is scaled by the evidence weight; test updated |
| D-03 | medium | Run detail returned an error because a derived field (`verification_level`) was required by the response schema but is not a database column | First API test run | Field given a default and filled by the serializer |
| D-04 | low | A property test compared DSL arithmetic to Python integers exactly, which fails above 2^53 (the DSL uses double precision on purpose) | Hypothesis found a counter-example on a later run | Test compares with a relative tolerance; the counter-example is pinned as a fixed case |
| D-05 | low | Evidence in a finding was listed in arbitrary order | Looking at the running UI | Sorted by investigation stage; test added |
| D-06 | low | The generic server-error test failed because the test client re-raised the server exception | Test run | Test uses a non-raising client |
| D-15 | medium | A request header with a non-ASCII character in the access token made the token comparison raise, giving a server error instead of 401 | Self-review of the security-sensitive code | Compare as bytes; test added |
| D-16 | medium | No limit on request body size: an oversized POST would be read into memory | Self-review | Bodies over 256 KB refused with 413 before parsing (declared length only; chunked uploads without a length are not covered, acceptable for a demo behind a proxy); test added |
| D-17 | low | Empty column header in the Verify table (screen readers announce a nameless column) | axe-core test | Visually hidden header text "Action"; test added |
| D-18 | low | The run graph was exposed as an image although its steps are focusable buttons (invalid nesting for assistive technology) | axe-core test | Container role changed to group; test updated |
| D-21 | low | Build output (`build/lib/...`, 42 files in three packages) had been committed after a clean-install check, so linting reported the same problems twice and stale copies of the code sat in the repository | ruff run with the docstring rules, 2026-10-11 | Folders removed; a `.gitignore` in each package now excludes `build/`, `dist/` and caches |
| D-22 | medium | `/api/health` took about 2 seconds on a machine without a local model, because every call probed the model endpoint and a refused connection is slow on Windows. Pages felt slow and the system-test server looked unhealthy | System test suite (server start timed out), 2026-10-11 | The probe result is cached for 15 seconds with a 0.6 second timeout (`llm_factory.live_available`); test `test_model_probe_is_cached_so_health_checks_stay_fast` |
| D-23 | medium | Verifying a suspect whose control replays were never recorded (for example Intake, in recorded mode) ended with "no verdict" and no reason, which reads like a malfunction | Live walkthrough in a browser, 2026-10-11 | The verdict text now says that the replays needed answers that are not in the recording and that a live model is required; the finding stays open for another attempt. Test `test_a_replay_with_no_recorded_answer_gives_no_verdict_and_says_why` |
| D-24 | low | Field errors showed the validator's internal wording ("Value error, must look like ...", "String should have at least 3 characters"); the review history showed the raw value `request_info`; a verdict with no finished control read "0/0 correct" | Live walkthrough in a browser, 2026-10-11 | Plain sentences ("Enter at least 3 characters", "Must look like #W1234567"), readable decision names, "no control finished". Test `test_field_messages_are_plain_sentences` |
| D-26 | medium | A review decision answered 201 before it was saved: the route relied on the session dependency to commit, and FastAPI (0.143) runs a dependency's exit code after the response is sent. A request sent straight after a reject could still see the finding as confirmed and accept it. System test SYS-ERR-03 failed intermittently (2 of 7 runs) | Repeated system-test runs on a second machine (Noor), 2026-10-11 | `post_review` commits before responding, like the run and experiment routes; SYS-ERR-03 then passed 15 of 15 repeated runs |

## Open

| ID | Severity | Defect or gap | Plan |
|---|---|---|---|
| D-19 | medium | **Design limitation found by the feasibility run:** a one-step intervention cannot be CONFIRMED when a second fault sits downstream. With the stale price fixed, the 3B calculator still added 47.76 + 1018.68 wrongly in all 5 replays, so the true origin was REFUTED (task #W1326557) | Feasibility run, M4 | Not fixed (the protocol is frozen); options: multi-step interventions, or judging the target step own contract. Needs a new rule version and a new run |
| D-20 | low | The small model makes large-sum arithmetic slips (off by 100 or 1000); about 1 in 10 clean runs produced a wrong refund | Feasibility run, M2 | Not a Granite defect; it is the natural failure the system is meant to catch. Prompt v1 is frozen with the recordings |
| D-07 | medium | **FR-SEC-01 not met:** personal data is not redacted before traces are stored. A redactor exists and is tested, but replays need the original task input | Decide: store redacted copies for display and keep the raw input encrypted or out of the demo; until then use only synthetic data **Decision 2026-10-11:** not done for Mid-1 (the plan rates it "should" for Mid-1 and "must" for Final-1). Redacting the stored trace alone would break replays in recorded mode, because the recorded answers are keyed by the exact prompt. Design for Iteration 2: tokens in stored step inputs and outputs, check results and evidence, plus a separate vault of original values that only the replay planner reads; an allow-list so order and item numbers are not taken for card or phone numbers. Owner: Shahoud |
| D-08 | medium | PostgreSQL has never been run; there is no migration tool (tables are created on start) | Run the API tests against a PostgreSQL container; add Alembic before any shared deployment |
| D-09 | low | **Mostly resolved 2026-10-09:** CI ran on GitHub and built and smoke-tested the image (evidence/repo). Still open: no local build on a team laptop; CI actions use Node-20 versions that GitHub now warns about | Build once with `docker compose up --build` before the demo; bump action versions when convenient |
| D-10 | medium | A recorded cassette is valid only for the exact prompts it was made with; any prompt edit makes recorded mode fail for every task | Re-record with `scripts/record_cassettes.py` after any prompt change; CI smoke test would catch it |
| D-11 | low | The rate limiter is in memory and per process, keyed by client address; behind a proxy all users share one address | Acceptable for a demo; move to the reverse proxy for a shared deployment |
| D-12 | low | The Verify panel accepts out-of-range counts in the form; the server refuses them and the message is shown | Clamp in the form |
| D-13 | low | The stage-0 PoC console lists no scikit-learn in its requirements (pre-existing; folder is frozen) | Leave; note in the report if the PoC is demoed |
| D-14 | low | The pipeline graph is horizontal and needs a minimum width of 640 px, so on a phone it scrolls sideways | Accept for now; a vertical layout is a later improvement |
| D-25 | low | In the hypothesis table the rank and the score can disagree inside one evidence class: rank ordered by evidence strength and then upstream first, while the displayed score also decays with distance from the symptom (Intake 0.066 was ranked above Writer 0.100). The top ranks, which carry direct evidence, were not affected | Fixed: ranking now sorts by the same value the table shows, so the two can no longer disagree (`attribution.py::ranking_score`), guarded by `test_rank_and_score_agree_so_the_table_reads_in_one_order` |
