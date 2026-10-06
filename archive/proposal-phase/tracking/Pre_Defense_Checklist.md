# Pre-Defense Checklist — Compiled from AI_Usage_Log.md

*Every item below is a "team must verify/decide" flag raised somewhere across the 19 dated sessions in `AI_Usage_Log.md`, deduplicated and checked against later sessions so anything already resolved is marked as such rather than repeated as if still open. Source session numbers are cited so you can go back to the original context for any item. Compiled 2026-09-07 — this is a point-in-time compilation; if the log gains new sessions, re-run this compilation rather than trust it as still current.*

*Updated 2026-09-07 with a real verification pass against the repo (not just re-reading this list): grepped for naming consistency, read `dev/datasets/DOWNLOAD.md`'s actual license table, read `Software_Design_Specification.md` §14 verbatim rather than paraphrasing. Two corrections came out of that pass — see the "correction" notes on items 4 and 13/16 below.*

---

## A. Must personally re-verify (facts/claims the log explicitly flags as AI-produced and unconfirmed)

1. **Independently re-read ErrorProbe and AgenTracer in full** — the two papers the entire contribution is measured against. *(Session 1)*
2. **Independently re-run at least one of the 8 PoC spike scripts yourself**, don't take the log's reported output on faith — especially Spike 7's negative result and Spike 1's reproduction. *(Sessions 1, 4)*
3. **Read ErrorProbe's Algorithm 1 and Section 4 directly** and confirm Spike 1's simplification (no tool-grounded Investigator, no Verified Episodic Memory) is accurately described as a simplification, not overstated. *(Session 1)*
4. **Confirm licensing claims.** ⚠️ **Correction after checking `dev/datasets/DOWNLOAD.md` directly:** Who&When and tau-bench are already marked "LICENSE present in-tree, verified" there — those two are genuinely done, not just claimed. **GSM8K is not** — its own row says "Permissive (MIT) — verify against the upstream repo before release." That's the one still-real gap in this item; MATH isn't tracked in that table at all (spot-check it too if it's still cited anywhere). *(Sessions 1, 2)*
5. **Spot-check `Commercial_Product_Comparison.md`'s claims** against at least one vendor's own current documentation (LangSmith, Langfuse, Braintrust, Arize, Maxim AI, Opik, or DeepEval) — vendor docs change fast. *(Sessions 1, 3)*
6. **Read and internalize `FYP_Scope_CCP_and_Implementation_Plan.md` §2 (CCP rating) and §3 (contribution statement)** — the two things most likely to be probed directly. Don't paraphrase from memory of the log. *(Session 1)*
7. **Be able to defend `ErrorProbe_Baseline_Selection.md`'s reasoning live**, not read it off a slide. *(Session 1)*
8. **Read the SDG alignment paragraph** (plan doc §0.05) and confirm you're comfortable defending it as written. *(Session 3)*
9. ~~Confirm the renamed feature labels and the "Granite" title/short-name read correctly in context~~ — **checked, genuinely clean**: grepped every `.md` in the repo for leftover "TraceCause" outside `AI_Usage_Log.md` and the archived-superseded folder. Every hit found is a properly-contextualized historical reference ("formerly TraceCause," explained rename records) — no accidental stale branding anywhere current-facing. *(Sessions 5, 7 — verified 2026-09-07)*
10. **Confirm the ownership mapping** (Shahoud–Data/Benchmark, Noor–Diagnosis, Saif–Platform) matches actual skill fit — the requirement is that ownership *is* allocated; the specific mapping is your call to keep or swap. *(Session 10)*
11. **Sanity-check the 15h/week capacity assumption and the per-line hour estimates** (`06_Expanded_Scope_and_Feasibility_Plan.md` §5.1) against your actual course loads this semester. If capacity is lower, the descope ladder is the pre-agreed adjustment — don't silently re-plan instead. *(Session 11)*
12. ~~Do one visual pass over the poc-demo console~~ — **done 2026-09-07**, by eye, for real: launched the actual dev server, drove headless Chrome against all 5 sections (Overview, Runs & diagnoses, POC evidence, Product & scope, Live demo), screenshotted each, checked the browser console for errors. All 5 pages loaded clean (zero console errors beyond a harmless missing-favicon 404).
    - **First-look finding, then self-corrected**: the Runs & diagnoses table's Status column looked clipped in the initial screenshot ("Agent correct, step off" cut off at the right edge). Checked before reporting it as a bug — it isn't one: the table wrapper has working `overflowX: auto` (confirmed programmatically: `scrollWidth 1200 > clientWidth 1142`, and scrolling right reveals the full label intact). No data or functionality is actually broken; there's just no visible affordance hinting that the table scrolls, which is a minor discoverability nit, not a defect. Recorded here so the same false alarm doesn't get raised again.
    - **One genuine, low-severity finding**: on the Live demo page's System Architecture view, the persistent floating hint chip (`#advanceHint2`, fixed to the viewport bottom) visually overlaps part of the "Diagnosis Engine" component-card row at the initial (unscrolled) view on a ~900px-tall viewport — because the view's content is taller than the viewport and the hint is fixed-position, not because anything is broken. Scrolling down moves the cards clear of it. The chip has its own background/border so it reads as an intentional floating element, not glitched rendering, and no content is permanently unreachable — a user can still click through after a small scroll. Low priority; not fixed this session since a UX-behavior change (auto-hide, repositioning) wasn't asked for and risks touching a file that's already reverted unexpectedly more than once.
    *(Session 19 — the item that raised this; closed this session, with one initial finding corrected in the same pass)*
13. **`Software_Design_Specification.md` §14's three items** (not urgent for the proposal defense itself — this is Mid-1-track):
    - ~~Reconcile the Case 6 `normalize_agent()` fix (R28) into the real Verification Agent's schema~~ — **done 2026-09-07**: SDS §6's `DIAGNOSIS` entity now carries both `culprit_agent` (normalized) and `culprit_agent_raw` (the model's literal output), with the reasoning and the still-owed implementation work (transcribing the actual logic; checking whether CrewAI/LangGraph need their own suffix rules beyond what Spike 1's AutoGen/Magentic-One traces surfaced) spelled out in §6 and §14. This closes the design-level gap; the code itself is correctly left for FYP-1 core build, not this document.
    - Still open: confirm the trace schema in SDS §6 against whatever the real CrewAI/LangGraph adapter output actually looks like, once real instrumentation hooks exist.
    - Still open: decide the actual retention window number for R16's time-bounded retention policy — the SDS names the mechanism, not a value. *(Session 17)*

## B. Team judgment calls still open (decisions, not verification)

14. **Decide what to do about Spike 7's near-random result (P/R/F1 = 0.25)** if you haven't already formally recorded the decision beyond "kept as a contingent extension" — test with larger/harness-generated data, improve features, or explicitly scope the preventive-clarification extension down/out. *(Session 4; the project's other docs suggest this was informally settled as "contingent, re-test owed by FYP-2" — confirm that's still the team's actual position.)*
15. **Decide whether to track the action-error-vs-judgment-error hypothesis explicitly** once real benchmark generation starts (Case 2's investigation, session 16) — a real, falsifiable, but n=8-sized finding. Not urgent for the proposal defense; worth deciding before FYP-1 core build.

## C. Already resolved — no action needed, listed only so nothing looks missed

- ~~Decide which figure to lead with after Spike 1's run-to-run variance~~ — **resolved**: mean + range, reported honestly (sessions 13–14).
- ~~Case 6 "Orchestrator" vs "Orchestrator (thought)" agent-name matching~~ — **fully resolved as of 2026-09-07**: POC-level scoring fix applied and verified conservative (session 15); real-system schema reconciliation closed the same day (item 13 above — SDS §6 now carries both the normalized and raw agent fields).
- ~~Verify the Spike 1 step_accuracy discrepancy and decide whether to patch/re-run~~ — **resolved**: bug found, fixed, spike re-run for real, propagated everywhere (sessions 12–14).
- ~~Spike 7 missing from the Runs & Diagnoses dropdown~~ — **resolved**: real bug found and fixed, verified live (session 18).
- ~~Replace `cost-estimate.md`'s 4-chars/token approximation with real token counts~~ — **resolved**: the $0 committed-budget decision (R37) was made from measured token counts across all 184 real cases, per later project state.

---

## How to use this before the defense

Items in **A** are the highest-value use of remaining prep time — they're specific, bounded, and each is the kind of thing a panelist can ask about directly ("have you read the paper you're measured against?"). Items in **B** need an actual team conversation, not more reading. Section **C** is just so a re-read of the log doesn't make you think something's still outstanding when it isn't.
