# Defect list

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-10-07 |
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

## Open

| ID | Severity | Defect or gap | Plan |
|---|---|---|---|
| D-19 | medium | **Design limitation found by the feasibility run:** a one-step intervention cannot be CONFIRMED when a second fault sits downstream. With the stale price fixed, the 3B calculator still added 47.76 + 1018.68 wrongly in all 5 replays, so the true origin was REFUTED (task #W1326557) | Feasibility run, M4 | Not fixed (the protocol is frozen); options: multi-step interventions, or judging the target step own contract. Needs a new rule version and a new run |
| D-20 | low | The small model makes large-sum arithmetic slips (off by 100 or 1000); about 1 in 10 clean runs produced a wrong refund | Feasibility run, M2 | Not a Granite defect; it is the natural failure the system is meant to catch. Prompt v1 is frozen with the recordings |
| D-07 | medium | **FR-SEC-01 not met:** personal data is not redacted before traces are stored. A redactor exists and is tested, but replays need the original task input | Decide: store redacted copies for display and keep the raw input encrypted or out of the demo; until then use only synthetic data |
| D-08 | medium | PostgreSQL has never been run; there is no migration tool (tables are created on start) | Run the API tests against a PostgreSQL container; add Alembic before any shared deployment |
| D-09 | medium | The Docker image has not been built and the CI workflow has not run on GitHub | Build locally once the Docker daemon is running; push a branch and record the run |
| D-10 | medium | A recorded cassette is valid only for the exact prompts it was made with; any prompt edit makes recorded mode fail for every task | Re-record with `scripts/record_cassettes.py` after any prompt change; CI smoke test would catch it |
| D-11 | low | The rate limiter is in memory and per process, keyed by client address; behind a proxy all users share one address | Acceptable for a demo; move to the reverse proxy for a shared deployment |
| D-12 | low | The Verify panel accepts out-of-range counts in the form; the server refuses them and the message is shown | Clamp in the form |
| D-13 | low | The stage-0 PoC console lists no scikit-learn in its requirements (pre-existing; folder is frozen) | Leave; note in the report if the PoC is demoed |
| D-14 | low | The pipeline graph is horizontal and needs a minimum width of 640 px, so on a phone it scrolls sideways | Accept for now; a vertical layout is a later improvement |
