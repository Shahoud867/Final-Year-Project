# Granite — Repository Change and Commit Plan

*I could not push: the GitHub remote requires authentication unavailable in this environment, and I won't fabricate commits. Below is the exact, ordered change plan — file by file, with commit boundaries — for the team to execute under the sole author identity `Shahoud867`, per the stated rule. Nothing here deletes working functionality; every change is an edit, a record, or hygiene.*

---

## Commit 1 — `docs: restructure committed core into two evidence tiers with pre-registered Mid-1 gates`

**`markdowns/01-planning-and-scope/FYP_Scope_CCP_and_Implementation_Plan.md`**
- §7.0: keep all 10 foundational items; add a **Tier** column — Tier 1 (items 1–8, each citing its spike) / Tier 2 (items 9–10). Under Tier 2, add the two gate paragraphs verbatim from audit §4.1 (RC: LangGraph checkpoint-resume PoC by Mid-1, else re-scope to replay-based resumption, recorded; VRM: stronger-backbone re-test on the same 8 Who&When cases by Mid-1, pass = ≥1 committed memory + no accuracy regression, else ships as memory-on/off ablation).
- §5.3 cross-reference: note the tiering itself as a recorded scope-structure decision dated 2026-08-2x, motivated by evidence status, not by results (none exist yet — which is the point of pre-registration).

**`markdowns/02-evidence-and-tracking/risk-register.md`** — append to R21 and R22: "Gate criteria pre-registered [date], see plan §7.0 Tier 2." Do not soften the recorded failure in R18/R22.

## Commit 2 — `docs: assign primary technical ownership (guide Gate 1 requirement)`

The guide's Gate 1 row requires ownership *allocated to each member at proposal defense* — the current "before Mid-1" deferral is non-compliant.
- **`plan §9`**: replace the three unassigned role rows with named assignments (Shahoud / Noor / Saif ↔ Data-Benchmark / Diagnosis / Platform, by skill fit) and a dated decision note.
- **`markdowns/01-planning-and-scope/architecture-sketch.md`**: update the correction paragraph and lane labels with the names.
- **`markdowns/05-deliverables/Proposal_Defense_Package.md`** slide 10: names in.
- **`risk-register.md` R6**: status → Closed, decision recorded per §5.3.

## Commit 3 — `docs: rename deterministic re-execution to controlled counterfactual replay`

Global, because a panelist who greps will find stragglers:
- **`plan §0.07` FR4** → *"…the system shall re-execute the downstream portion of the trace under a controlled replay protocol (frozen upstream context; affected steps re-run with pinned decoding parameters) and report whether the corrected trace now succeeds, with recovery rate reported over N replays."*
- Same substitution in: plan §1 (Strong CCP statement: "test corrective interventions via controlled counterfactual replay"), §6 table row, §7.0 item 8's description; `architecture-sketch.md` data-flow step 5; `Proposal_Defense_Package.md` slides 6/9; `FYP_Registration_Form_Answers.md` scope paragraph. Add one sentence where item 8 is defined: deterministic applies to non-LLM computation and to the protocol; LLM-step variance is measured, never assumed away.

## Commit 4 — `docs: scope the Semantic Error Diagnostic claim and add coverage metric`
- **`plan §6`** SED row and **§7.0 item 7**: append the scope sentence (audit §4.5) — machine-checkable constraints; abstains elsewhere; coverage reported.
- **`plan §11` metrics row**: add **silent-failure coverage / abstention rate**.
- **`Proposal_Defense_Package.md`** slide 6/8 accordingly.

## Commit 5 — `docs: fix consistency issues before defense`
- **`Proposal_Defense_Package.md`** slide 7: "7 spikes" → "8 spikes"; fold the Spike-8 paragraph into the table as row 8.
- **`dev/README.md`**: title "TraceCause" → "Granite"; "4 real POC scripts" → "9 scripts (spikes 1, 2, 3, 3b, 4–8)"; fix every `../agent-autopsy/markdowns/...` link → `../markdowns/...`; remove the machine-specific `d:\fyp - research\...` and `E:\ai-workspace` paths from the repo-facing doc (move to a private note if needed — a public repo shouldn't map your disk).
- Everywhere both memories appear (plan §7.0 item 10, `04-poc-evidence`, defense package): one clarifying clause distinguishing **Verified Repair Memory (Granite: stores error→repair patterns)** from **Verified Episodic Memory (ErrorProbe's diagnosis memory, reproduced only inside the baseline)**.

## Commit 6 — `docs: add cost estimate and reproduction acceptance band (closes the open half of R1/R5)`
- New file **`markdowns/01-planning-and-scope/cost-estimate.md`**: per-case token math from Spike 1's real traces × 184 Who&When cases × 3 stages; benchmark generation at 500 and 1,000 traces on the chosen generation model; model plan (local/free-tier for volume, one strong hosted model for evaluation runs only); worst-case rupee/dollar figure. Link from plan §11 and resources.md §1.
- **`plan §11`** baseline row: add the declared band — "reproduction accepted within ±10 pts of 59.5% on a comparable-class backbone; otherwise both numbers reported per Annex A.2" — dated *before* any full-reproduction run, so the criterion is pre-registered (§5.3's own rule about not adjusting measures after seeing results).

## Commit 7 — `chore: repository hygiene and licensing (before the repo is ever public)`
- **Remove datasets and vendored repos from git history going forward**: add `dev/datasets/` to `.gitignore`; replace with **`dev/datasets/DOWNLOAD.md`** — per-dataset source URL, license, retrieval command, and checksum. Rationale: 48MB of third-party code/data in git is fragile and, in one case, a likely license violation:
  - **GAIA is a gated dataset** (access-agreement on Hugging Face). Redistributing `gaia_official/` in a public repository would breach its terms. Delete from the working tree; if the repo must go public with history intact, rewrite history for that path (`git filter-repo --path dev/datasets/gaia_official --invert-paths`) *before* publishing — history rewriting is destructive, so do it deliberately, once, with a backup.
  - MetaGPT (vendored whole) — MIT, legal but wrong: pin a commit hash in DOWNLOAD.md instead. Who&When (MIT), GSM8K/MATH/MBPP+/tau-bench (permissive) — legal, still belong outside git.
- Add `__pycache__/` and `*.pyc` to `.gitignore`; `git rm -r --cached dev/spikes/poc/__pycache__`.
- Keep `dev/spikes/poc/` **outputs** in git — they are PoC evidence, small, and load-bearing for the defense.

## Commit 8 (post-defense) — `docs: record proposal defense outcome and any panel-directed changes`
Per §5.3: whatever the panel changes, record it the day of, not reconstructed later.

---

## Explicitly *not* changed, and why
- **The title.** Registration answers are compiled; the two-tier core makes the title defensible without churn three days out.
- **The 8 extensions / 2 parked items.** Already correctly gated; touching them now is re-litigation the plan doc itself forbids ("no further feature brainstorming without explicitly reopening").
- **The 971KB `Granite_Full_Project_Explanation.md`.** Leave as the internal record it is; do not present from it. (Optional post-defense: mark it "internal narrative record, not a deliverable" in INDEX.md.)
- **PoC code.** It is evidence; editing evidence before a defense is exactly wrong. Spike 8's identified interface fix (pin the atomic corrected field) belongs in the *build*, not in a retrofitted spike.

## Execution order and deadline mapping (defense: Thu 28 Aug)
| When | Do |
|---|---|
| Today (Tue) | Commits 1–5 (all pure documentation, ~2–3 hours); assign owners (the only decision required); start stakeholder outreach (2 contacts) |
| Wed | Commit 6 (cost math needs Spike 1's token counts — half a day); rehearse deliverable 02 Part A aloud, each member takes their subsystem's questions; department prior-FYP archive check → fill slide 3's row |
| Wed night | Slide deck built from deliverable 03; dry run under 14 minutes |
| Thu | Defend. Commit 8 same day |
| After defense, before repo goes public | Commit 7 incl. the GAIA history rewrite |
