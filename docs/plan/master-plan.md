# Granite — FYP Master Execution Plan

**Project:** F26-060-Granite · *A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery*
**Team:** Shahoud Shahid (23i-2515) · Muhammad Noor (23i-2520) · Saif Shahzad (23i-2634) · **Supervisor:** Dr. Adil Majeed
**Stream:** A (research-derived) · **AI-assisted development level:** declared L2 (assisted, not AI-led — handbook C.8) in v1.1. **Needs re-declaring:** in the implementation phase (2026-10-06/07) an AI agent wrote the code, so L2 no longer describes it. The team and supervisor must decide the level and the contribution boundary; see [`ai-usage-log.md`](../registers/ai-usage-log.md) session 20 and [`form-13-genai-disclosure.md`](../registers/form-13-genai-disclosure.md)

| Document control | |
|---|---|
| Version | **1.1**: a revision of v1.0 (2026-10-04) against the official Mid-1 rubric and the prescribed report template |
| Date | 2026-10-06 (paths updated the same day to the reorganized workspace) |
| Status | DRAFT. It becomes the baseline once the supervisor approves change record **C-01** (§11.4) |
| Execution status | **Read [`execution-status.md`](execution-status.md) for what exists today** (2026-10-07). Implementation decisions that differ from this plan are recorded in [`change-log.md`](../registers/change-log.md) (C-02). Where this plan and the code disagree, the code and the status file describe reality |
| New inputs in v1.1 | `references/university/fyp1-mid-assessment-guidelines-and-rubrics.pdf` (official Form 2/Form 3 rubric with bands, gates and red flags; dated 5 Oct 2026). `references/templates/fyp1-mid-report-template_latex.zip` and its rendered `.pdf`: the prescribed chapter-wise LaTeX template, currently **unfilled**. |
| Supersedes | Scope, timeline and ownership sections of `deliverables/stage-0-proposal/proposal-documents/FYP_Scope_CCP_and_Implementation_Plan.md` (§7, §9, §12), `Software_Development_Plan.md` (§2, §8, same folder) and the UI in `deliverables/stage-0-proposal/poc-console/`. Research content (literature, CCP, DEI/ethics, datasets) is **retained** and referenced. |
| Change rule | Changes to scope, architecture, evaluation baseline/metrics, deployment target, NFR targets or ownership go through a recorded change entry (handbook C.5.3). No silent changes. |
| What changed since v1.0 | Appendix D (change log) |
| Workspace layout | Every path in this plan follows [`docs/workspace-guide.md`](../workspace-guide.md), the single source of truth for structure and naming. Pre-reorganization paths are in [`archive/migration-map_2026-10-06.tsv`](../../archive/migration-map_2026-10-06.tsv); v1.0 is preserved in `archive/superseded/`. |

### How to read this plan

- **§0 Mid-1 action card: start here.** The state on 6 Oct, what to do today, which track to follow.
- **Part A, §1–14: what and why.** Assessment, product definition, scope, workflow, and the input→verification model.
- **Part B, §15–29: how.** Requirements, UX, architecture, data, API, security, design artefacts, development, testing, CI/CD, deployment.
- **Part C, §30–37: when and who.** Mid-1 (rubric-aligned, with tracks), FYP-1, FYP-2, team, timeline, Definition of Done, risks.
- **Part D, §38–45: compliance and defense.** Cost, report mapping, handbook and rubric compliance, defense preparation, demo scripts, product strategy, checklist.
- **Appendices:** A (Feature→Verification→Test traceability), B (sample test cases), C (self-audit), D (change log v1.0 → v1.1).

### Mandatory vs recommended (tags used from v1.1)

| Tag | Meaning | Source |
|---|---|---|
| **[M-R]** | Mandatory: official Mid-1 rubric (Forms 2/3, gates, red flags) | `references/university/fyp1-mid-assessment-guidelines-and-rubrics.pdf` |
| **[M-H]** | Mandatory: FYP Handbook 2026 | `references/university/bs-fyp-handbook-2026-draft.pdf` |
| **[M-F]** | Mandatory: faculty statement. The core module must work with a CI/CD pipeline on the live/functional interface (or its improved version), using GitHub branching, CI and CD. | Faculty requirement relayed by the team |
| **[M-T]** | Mandatory: the prescribed report template | `references/templates/fyp1-mid-report-template_latex.zip` |
| **[Rec]** | Recommended: the team's engineering and academic judgement | This plan |

§0, §30, §39 and §40 carry explicit tags. In other sections, anything that cites the handbook, a Form or the rubric is mandatory; everything else is recommended.

### Assumptions and open decision points (resolve these first)

| ID | Item | What we assumed | Action / owner / by |
|---|---|---|---|
| **A1** | **Mid-1 date** (still unconfirmed in the workspace) | The rubric says "around Week 8". It was issued 5 Oct and the template 6 Oct. Together with the 11 Sep proposal defense in Week 3–4, this places Week 8 at **5–9 Oct or 12–16 Oct 2026**. | **Today:** Shahoud confirms the date and slot with the supervisor/coordinator, then chooses the track (§30.2) |
| A2 | Capacity | Each member gives about 15 h/week normally and about 25 h/week in crunch weeks. Sessional exams reduce some weeks. | Each member confirms today |
| A3 | Supervisor approval of the redefinition | The panel *asked* for a redefined workflow, so the change is mandated. It still needs a recorded approval. | Change record C-01 presented at Mid-1 |
| A4 | Free tiers | Render free web services, Neon free Postgres, GitHub Actions (private: 2,000 min/month; 3,000 with Student Pack), and a free hosted-LLM tier (Groq or Google AI Studio). Limits change, so treat these as **verify before relying on them**. | Saif verifies on D1. Fallbacks are in §29.6 |
| **D1** | Hosted LLM for the *public demo* instance | Default: Groq free tier (OpenAI-compatible). Fallback: Gemini free tier. Local Ollama remains the self-hosted/product default. | Shahoud, D1 |
| **D2** | Repository visibility | Private until Mid-1. Consider making it public (MIT) at Final-1 to unlock free CodeQL/SonarCloud and unlimited Actions minutes. This needs the dataset clean-up (§28.1) and supervisor consent. | Team + supervisor, by Final-1 |
| **D3** | Poster tool | The handbook recommends Photoshop/Corel (Corel/PSD file + JPEG). If we use another tool (Inkscape/GIMP/Figma), **we are responsible for printing**. | Shahoud, by FYP-1 Week 11 |
| **D4** | Ownership confirmation | Same three ownership areas as approved at the proposal, re-described around product modules (§34) | Team, today. Record it per C.5.3. |
| **D5** | **Report formatting: template vs handbook §8** | They differ. The template uses 12 pt Times, 3 cm side margins, footer page numbers and chapter/section running heads. Handbook §8 specifies TNR 11, Arial headings, L 2.0"/R 1.0", top-right numbers and title/chapter headers. The rubric grades "prescribed template followed" (F3-1). **Default: use the template as supplied and fix only its rendering defects** (§30.5, §39.3). | Shahoud asks the supervisor today whether §8 still applies at Final-1 |
| **D6** | Abstract length | Handbook §8 says 50–125 words. A commented-out, unrendered note in the template's `main.tex` says 150–200. **Default: the handbook's 50–125.** | Shahoud |
| **D7** | **Mid-1 logistics** | Not stated in the files: the report submission deadline and channel, whether the report is due before the demo, and how Form 2 and Form 3 combine within the 20%. | Shahoud confirms today. Plan the report as due **before** the demo until told otherwise. |

---

## 0. Mid-1 Action Card (v1.1: read this first)

### 0.1 Situation on Tue 6 Oct 2026 (re-inspected)

- **The official Mid-1 rubric is in hand.** Mid-1 is supervisor-only, formative, worth 20% of FYP-1, and held around Week 8. Two 100-mark instruments: **Form 2** (presentation and demo; 8 criteria) and **Form 3** (report; 8 criteria). Both have score caps, gates and six named red flags. [M-R]
- **The prescribed report template is in hand, and it is completely unfilled.** Every section is a placeholder ("Title of the Project here", "Student 1 19I-1234", "Replace this text…"). Its rendering also has three defects (§30.5). **Form 3, a separate 100-mark report form, is at 0%.** [M-T]
- **No product code exists yet.** There is no `apps/`, `packages/` or `.github/`. The repo is still mid-rebase and 5 commits behind `origin/noor`. **None of v1.0's Day-0 actions have been done.**
- **Consequence:** report writing and product building must run **in parallel from today**. v1.0 scheduled the report for the last day; that is withdrawn.

### 0.2 Today (≤ 4 hours)

1. Confirm the Mid-1 date and slot, the report deadline and channel, and the formatting rule (A1, D5, D7). Owner: Shahoud.
2. Choose the track by the confirmed date (§30.2): **T0** ≤ 1 working day · **T1** 2–4 working days · **T2** 5–8 working days.
3. Repo Day-0 hygiene (§28.1), including `.mailmap`, plus a CI skeleton. Owner: Saif.
4. Import the report template into `docs/report/`, apply the three rendering fixes, and fill the title page, names and supervisor. Owner: Shahoud.
5. Open the track's issues on the GitHub Project board, with owners. Owners: all.
6. Open the registers: Panel Action Register (A1–A6), milestone log, change record C-01. Owner: Shahoud.

### 0.3 Where the marks are (details in §30.1)

- **Form 2:** the live core module is 25 of 100 marks. Design matching the code is 15. Six other criteria are 10 each.
- **Form 3:** R&D, requirements, architecture, implementation documentation and testing/tool disclosure are 15 each. Vision/scope and data/behaviour design are 10 each. Format is 5.
- **Gates that zero or cap marks regardless of quality:**
  - tool/GenAI disclosure missing → that Form 3 item = 0
  - no repository evidence → process marks capped at 40%
  - diagrams-only design → design marks capped at 50%
  - no live system → demo marks capped

### 0.4 Six red flags we are exposed to (countermeasures in §30.8)

Sudden code volume · stagnant prototype momentum · generic or GenAI-written R&D text · uneven team contribution · dishonest milestone logging · ignored proposal panel actions. Our crunch build, AI-drafted document base and uneven commit history make the first, third and fourth real risks.

---

## 1. Executive Summary

**v1.1 update (6 Oct 2026).** v1.0's product direction, workflow, verification design and scope stand, because the official Mid-1 rubric rewards exactly these: a meaningful core module working live with failure cases, design artefacts that match the code, and executed tests. Five things changed:

1. **The mid report must use the prescribed LaTeX template**, which is still empty. Form 3 is a separate 100-mark form (its weight against Form 2 is not stated; D7), so report writing now starts on day one, in parallel with the build (§30.5).
2. **Two planning days passed with no Day-0 action**, so the Mid-1 plan is now three date-driven tracks (§30.2–30.3).
3. **Every Form 2 and Form 3 criterion now has an evidence plan and a target band** (§30.1, §40.0).
4. **The rubric's six red flags have named countermeasures.** They change how we commit, write and present (§30.8).
5. **The Mid-1 Definition of Done is calibrated per track**, with mandatory and recommended items tagged (§30.6).

The full list is in Appendix D.

**Verdict.** Granite has an approvable research idea, unusually honest evidence-keeping, and a strong document trail. **It has no product.** Every interface shown so far replays pre-recorded results:
- `deliverables/stage-0-proposal/poc-console/` (then `poc-demo/`) is a read-only console over spike JSON.
- Its "Live demo" page is a scripted animation with zero backend calls.
- The defense PoC is, in our own guide's words, "one self-contained HTML file… no backend… no model calls".

The panel's five comments (UI/UX, unclear features, unclear inputs, unclear verification and evidence capture, workflow to be redefined) all come from one root cause. **We designed mechanisms, not a user workflow.** There was no screen where a user gives Granite something and gets back a verified result.

**What changes:**

1. **Granite becomes a product with one clear job.** It is an *evidence-first failure-investigation workbench for multi-agent LLM workflows.* Tagline: **"Find the failure. Prove the cause. Verify the fix."** Its unit of value is the **Verified Finding**: a recorded failure with a symptom, a root-cause hypothesis, reproducible evidence, a replay-tested verdict, and a human decision.
2. **One canonical workflow, visible in the UI as a stepper:** Ingest → Check → Detect → Attribute → Verify → Review → Resolve → Record (§13). For every feature we define inputs, outputs, evidence, verification and what is stored (§14).
3. **Verification is made concrete.** It has four levels (V0 detected → V1 evidence-reproduced → V2 replay-verified → V3 human-confirmed). It uses a pre-registered verdict rule: N intervention replays **plus control replays**, giving CONFIRMED / REFUTED / INCONCLUSIVE. Every artefact is stored as hashed evidence (§14.3–14.5).
4. **Novelty is re-baselined honestly.** Since the proposal we found or confirmed close prior work:
   - **DoVer** (arXiv preprint 2512.06749, 2026) already does "intervene at the suspected step, re-execute, see if the failure flips".
   - Commercial tools (LangSmith Engine, Patronus Percival, Galileo Insights, Raindrop) already market root-cause diagnosis, fix suggestion and "silent failure" detection.
   - ErrorProbe's own limitations section names "test-time oracle feedbacks" as the future work for silent failures.

   Our defensible contribution is now:
   - **executable checks** (test-time oracles)
   - **deterministic value-provenance attribution**
   - a **controlled verification protocol robust to LLM nondeterminism**
   - measured false-alarm rates on clean controls
   - all **self-hostable at $0**

   We stop claiming "first", "nobody verifies fixes" and "commercial tools don't do root cause" (§10).
5. **Scope is cut so we can deliver it.**
   - The 10 mechanisms map 1:1 onto 7 user-facing product modules plus Fault Lab/Evaluation, so the core idea is preserved (§11.3).
   - The full ErrorProbe reproduction moves from "Mid-1 top priority" to an FYP-2 *Should* baseline track.
   - The benchmark target drops from 500–1,000 to **≥300 Must / 500 Should**.
   - 11 of the 13 extensions move to *Future*. The spike-7 classifier is dropped.
   - The Tier-2 gates are resolved by design: replay-based recovery, and a deterministic known-fix library.
6. **The Mid-1 target slice is "Refund Desk", built on tau-bench retail data (MIT).** It is delivered in full in Track T2 and scaled down in Tracks T0–T1 (§30.2). An evaluator opens the deployed URL and launches a 5-agent refund workflow, optionally with an injected fault. Granite flags a silent wrong refund, traces it back to the stale-price tool step, and verifies the hypothesis with 5 replays + 2 controls (CONFIRMED). A second hypothesis is REFUTED. A reviewer accepts the finding, and it appears in history with exportable evidence. A clean run produces no false alarm.
7. **Engineering becomes real:**
   - **Repository:** a monorepo with `main`/`develop`, protected branches, PR review and Conventional Commits.
   - **CI** on every push/PR: Ruff, mypy, pytest with coverage gate, ESLint/tsc/Vitest, Bandit, pip-audit, gitleaks, Docker build.
   - **CD:** auto-deploy to staging on merge to `develop`; production on tag; smoke + Playwright E2E against the live URL.
   - **Stack:** FastAPI + React + Postgres (Neon) on Render. Total cost **$0**.

**What does not change:**
- the problem: multi-agent LLM failures, especially silent ones
- Stream A
- the CCP
- the three ownership areas
- the use of Who&When / tau-bench / GSM8K
- the $0 commitment
- the research discipline: pre-registered thresholds and honest negatives

---

## 2. Current-State Assessment

### 2.1 What exists (inspected 2026-10-04; re-checked 2026-10-06)

| Area | What is in the repo | Evidence |
|---|---|---|
| Research | 7 papers read: Who&When, AgenTracer, SDBL, TraceElephant, ErrorProbe, AgentAsk, PROTEA. Plus a literature review, a baseline-selection memo, a 660-title prior-FYP archive check, and a commercial comparison. | `references/papers/`, `research/literature/`, `research/market/` |
| Planning docs | Project Vision, SRS (28 FRs), SDS, Use Case Model (11 UCs) + SVG, 3 SSDs, Test Plan, SDP, a RAID register (39 entries), Traceability Matrix, Form 13, AI usage log (19 sessions), DEI/ethics, SDG 9 | `deliverables/stage-0-proposal/proposal-documents/`, `docs/registers/` |
| Spikes | 9 real scripts on CrewAI + Ollama `llama3.2:3b`, all with outputs | `research/spikes/` |
| Spike results | **Spike 1:** agent accuracy 71.4% (range 62.5–85.7%), step accuracy 13.2% (0–25%), n=8, over 5 runs. **Spike 5:** toy deterministic replay 97.2→108.0. **Spike 8:** repair 4/6. **Spike 4:** 0 natural silent failures in 3 live cases; seeded mechanism test 3/3 caught. **Spike 7:** P/R = 0.25. | `poc_spike1_multirun_summary.json`, etc. |
| PoC app | FastAPI (3 GET endpoints over spike JSON) + React/Vite console (Overview, Runs, Run detail, POC evidence, Product & scope, Live demo) | `deliverables/stage-0-proposal/poc-console/` |
| Defense PoC | Single-file interactive HTML. Refund scenario: stale promo table → $20.00 instead of $19.75. Animation, comparison and scope tabs. | `deliverables/stage-0-proposal/poc-canvas/` |
| Data | Who&When (184 tasks), tau-bench retail (MIT: users/orders/products + 15 tools + policy wiki), GSM8K, MATH, MBPP+, GAIA (gated), AgenTracer sample | `data/raw/` (≈46 MB, still tracked in git) |
| Engineering | **No tests. No CI. No Dockerfile. No lint config. No `main` branch** (the default branch is the personal `noor`). | `find` / `ls .github`: none |
| Mid-1 rubric *(new, 6 Oct)* | Official Form 2/Form 3 rubric with score bands, gates and six red flags | `references/university/fyp1-mid-assessment-guidelines-and-rubrics.pdf` (dated 5 Oct 2026) |
| Mid report *(new, 6 Oct)* | Prescribed chapter-wise LaTeX template (`fast-nuces-bs.cls`, 10 chapters + 6 appendices). **All placeholders, no Granite content.** Three rendering defects (§30.5). | `references/templates/fyp1-mid-report-template_latex.zip` / `_rendered.pdf` |
| Progress since v1.0 (4 Oct) | None of the Day-0 actions are done: no CI, no `apps/` or `packages/`, and the repo is still mid-rebase and 5 commits behind | `git status`, 6 Oct |

### 2.2 Strengths to keep

- **Evidence honesty is excellent**: negative results kept, bugs disclosed, pre-registered bands. Panels reward this, and Mid-1 explicitly asks for honest milestone logs.
- **Real feasibility evidence**: CrewAI instrumentation, fault injection with clean propagation (Spike 3b), cycle bounding (Spike 6), and the repair-interface lesson from Spike 8 ("name one atomic field").
- **A strong compliance base**: DEI/ethics/SDG/Form 13/AI log/prior-FYP comparison already exist and only need updating, not writing from scratch.
- **The domain choice** (customer-support / retail refunds via tau-bench) is concrete, public, MIT-licensed, and comes with a policy document. That makes it ideal for executable checks.

### 2.3 Critical weaknesses (evidence-based)

| # | Weakness | Evidence | Consequence if not fixed |
|---|---|---|---|
| W1 | **No functional product.** Nothing accepts user input. | `deliverables/stage-0-proposal/poc-console/backend/main.py` has GET endpoints only. The SDS itself calls `POST /api/runs` "the actual gap". LiveDemo makes 0 `fetch` calls. The PoC guide §1.1 says "No backend… No model calls". | Form 2 "Live prototype with core module" (25 marks) capped. Score cap at 40% if no live system (Appendix B §2.2). |
| W2 | **The silent-failure detector uses an answer key.** | `poc_spike4_silent_failure_detector.py`: `rule_based_constraint_check(stated, case.correct_answer, tol)` | In production the correct answer is unknown, so as built the headline feature cannot run on real traces. A panel will ask "where does `correct_answer` come from?" |
| W3 | **Novelty claims are outdated or overstated.** | DoVer (arXiv preprint, 2026) does intervention + re-execution verification. PROTEA reruns after fixes. Raindrop markets silent-failure detection and replays traffic against proposed changes. LangSmith Engine runs a closed detect→diagnose→fix→evaluator loop. Percival suggests fixes. ErrorProbe's limitation treats "verifiable constraints" as *detectable* anomalies and names test-time oracles as future work. | "Nobody verifies a fix before trusting it" and "catches what ErrorProbe cannot" are false as worded. One informed question at Final-1 can collapse the contribution story. |
| W4 | **Scope inflation.** | 10 foundational + 8 + 13 extensions + 11 methodology commitments. The ~1,130 h budget is 100% allocated with no slack. ErrorProbe reproduction sits at 13% step accuracy on a 3B model. Benchmark target 500–1,000. 3 frameworks. | Breadth over depth: no polished core by Final-1 (handbook C.19.4 "feature accumulation"). |
| W5 | **No engineering hygiene** | No tests/CI/Docker/lint. The default branch is personal. 46 MB of datasets in git, including GAIA (redistribution problem). **The local clone is mid-rebase and 5 commits behind `origin/noor`.** | Fails the faculty's CI/CD requirement and Form 2 "Repository evidence" (cap 40%) |
| W6 | **Contribution visibility is imbalanced** | `git shortlog`: Noor 45 commits, Shahoud 24, **Saif 1** | Form 11 individual-contribution adjustment risk for Saif. "Commit count alone is not enough", but zero visible engineering work is a red flag. |
| W7 | **Document volume exceeds ownership** | ~40 long, AI-drafted, self-referential documents (a 976 KB "explanation", audits of audits) | Mid-1 asks each member to walk through the code "at file and function level". Panels cap design marks when diagrams lack reasoning (Appendix B §2.2). Heavy AI-written prose that members cannot defend is a liability. |
| W8 | **Timeline contradicts the handbook** | The SDP puts Mid-1 at "~Week 10". The handbook says Week 8. | A two-week planning error at the most time-critical gate |
| W9 | **The UI is research-facing** | The Overview shows accuracy tiles, the POC evidence index, the scope/tier/ladder page | The panel saw research dashboards, not a tool (exactly "UI/UX needs improvement") |
| W10 | **No stakeholder contact yet** | Plan §16 "Real stakeholders contacted — still open". CCP #6 rated weak. | Requirements are not validated. The UAT participant pool is undefined (C.13.1). |
| W11 | **Spike evidence is tiny** | n=1–8 per spike, all on one 3B model | Fine for a PoC. It is not evaluation evidence, and it must not be presented as such. |
| W12 | **The mid report is 0% written** | The template contains only placeholders | Form 3 (100 marks) is entirely the report. Leaving it to the last day (v1.0's sequencing) risks the format, SRS, design and tool-disclosure gates. |
| W13 | **Red-flag exposure under the official rubric** | A large AI-drafted document base; a commit history dominated by one member; a crunch build that invites "sudden code volume" | Mark caps, mandatory rewrites, Form 11 adjustments (rubric "Red Flags and Supervisory Action") |
| W14 | **Two planning days lost** | v1.0's Day-0 actions had not started by 6 Oct | The Mid-1 scope now depends on the confirmed date (§30.2) |

### 2.4 Bottom line

Granite's *research* is ahead of most FYPs. Its *product* is at zero. With Mid-1 days away, the highest-value move is **one thin, real, deployed vertical slice** wired to the mechanisms the spikes already proved. It must be backed by real CI/CD and documented in a concise report that the team can defend line by line.

---

## 3. Panel Feedback → Required Corrections

(This is also traceability matrix #2: *Panel criticism → root cause → corrective action → implementation → verification evidence*. It is carried into the Form 10 Panel Action Register.)

| ID | Panel criticism | Root cause | Corrective action | Implementation (where) | Verification evidence | Due |
|---|---|---|---|---|---|---|
| A1 | UI/UX needs improvement | The UI was organised around research artefacts (spikes, tiers, metrics), not user tasks. No input surfaces. | Redesign the information architecture around the investigation workflow. Add task-oriented screens, an investigation stepper, empty/loading/error states, and WCAG 2.2 AA. | §17–18. `apps/web` screens S0, S4, S6, S8, S9, S10 (Mid-1). Full set by Final-1. | Deployed URL. Before/after screenshots in report. Usability test with 3 peers (task success, SUS) by Final-1. Playwright E2E on the core journey. | Mid-1 (core), Final-1 (full) |
| A2 | Features not sufficiently clear | 10 mechanism names (Culprit Agent, SED, VAR…) are not user-meaningful. 20+ features listed. | Collapse into **7 user-facing modules** with plain names (Run, Import, Check, Trace back, Verify, Review & Resolve, Report) plus Fault Lab/Evaluation. Map old names 1:1 (§11.3). | §11–12. In-app glossary and "How Granite works" page (S16). | Feature list in report Ch. 4.1, each with I/O card (§14). Supervisor can name the 7 modules after the demo. | Mid-1 |
| A3 | Unclear what inputs each feature accepts | No input contracts existed: the PoC had no inputs at all. | Define an input contract per feature: format, schema, limits, validation, error messages. Publish **Granite Trace v1** JSON schema and the **Check** definition format. | §14.2 (per-feature cards), §22.4 (schema), §23 (API). Pydantic models enforce them. | OpenAPI docs at `/docs`. Validation tests (malformed/oversize/missing-field). Input table in SRS. | Mid-1 (Run, Check), Final-1 (Import, SDK) |
| A4 | Unclear how flaws are verified and how results are captured | Verification was a mechanism ("replay"), not a protocol with a decision rule and records. The detector relied on an answer key (W2). | Define verification levels V0–V3, the replay protocol with **controls**, the pre-registered verdict rule, the Wilson CI and the regression guard. Define the Evidence record (typed, hashed, reproducible) and the Review record. Replace the answer-key detector with executable checks against trace evidence and sources of truth. | §14.3–14.6. `granite_core.verification`, `granite_core.checks`. Tables `experiment`, `evidence`, `review`, `audit_log`. | Finding page shows the evidence chain. Exported Finding Report (MD/JSON). Unit tests on the verdict rule. Benchmark verdict precision (Final-1 v0). | Mid-1 |
| A5 | Overall workflow must be redefined | Workflow existed only as an internal pipeline diagram (SDS §5). There was no operator journey. | One canonical 9-stage workflow (§13), shown for three audiences. Enforced by the finding state machine (§13.3). Shown as a stepper in the UI. | §13. State machine in `finding.status`. Activity, state and sequence diagrams in the report. | Demo follows the stepper end to end. State-transition unit tests. Audit log. | Mid-1 |
| A6 *(implicit)* | PoC demonstrated research, not the product | Proposal effort went into documentation and spikes. | The Mid-1 vertical slice on a deployed URL with CI/CD (§30). Each later milestone adds working features, not documents. | §30–32 | Live demo on the deployed URL. GitHub Actions history. Tag `v0.1.0-mid1`. | Mid-1 |


**Register format [M-R][M-T].** The register appears in the template's §3.2 table (No · Feedback / Required change · Action taken · Status · Evidence) and in full in Appendix A. The rubric requires three things:
- each row carries a **live evidence link** (deployed URL, PR, commit, test run or screenshot)
- the register is **opened during the Mid-1 session**
- no row is marked "Done" without demonstrable proof (red flags "Ignored proposal panel actions" and "Dishonest milestone logging")

---

## 4. Product Vision

**Vision statement.** When a multi-agent AI workflow produces a wrong result, even one that raises no error, Granite tells the team **where it went wrong, proves it, and shows whether a fix actually works**, on infrastructure the team controls.

**Product positioning (elevator):**
- *For* developers and QA reviewers of multi-agent LLM workflows (CrewAI, LangGraph or plain Python)
- *who* need to know why a run produced a wrong result and whether a fix is real
- *Granite* is a self-hostable investigation workbench. It turns each suspected failure into a **verified finding**: the originating step, reproducible evidence, a replay-tested verdict, and a recorded human decision.
- *Unlike* debuggers whose diagnosis is mainly an LLM's opinion over logs, Granite's findings rest on **executable checks and controlled re-execution with controls**.
- It runs at **$0 on local or free models**, so sensitive traces need not leave the team.

**Product principles (they drive design decisions):**
1. **Evidence before opinion.** An LLM may *suggest*. Only checks and replays can *verify*.
2. **Every finding is a record.** Nothing is shown that is not stored, and nothing is stored that cannot be re-checked.
3. **Say "inconclusive" when it is.** Nondeterminism is measured, not hidden.
4. **Human decides.** Granite never auto-applies a fix to production. It produces a verified recommendation.
5. **Works offline.** Every core path runs with local models or recorded responses.

---

## 5. Problem Definition

**Concrete scenario (runs in the Mid-1 demo).** A customer asks a retail support agent team to return two delivered items. Five agents cooperate:
- **Intake** parses the request.
- **Order Lookup** (tool) fetches the order and item prices.
- **Policy** decides eligibility.
- **Refund Calculator** computes the refund.
- **Writer** answers the customer.

The Order Lookup tool returns a **stale price** for one item, so the refund is $0.25 short. Every agent then behaves "correctly" on bad input. The run finishes with status `completed`, a fluent message and **no error anywhere**. That is a silent failure. The symptom is visible only at the end (the stated refund ≠ catalogue value). The origin is three steps upstream.

**How teams handle this today** (based on our product survey; to be validated in interviews, W10):
1. Someone notices, often a customer complaint.
2. A developer opens raw logs or a tracing UI (LangSmith/Langfuse/console prints) and reads every step manually.
3. They guess the culprit, often the step where the wrong value *surfaced* (the Calculator), not where it *originated*.
4. They edit a prompt or code and re-run once.
5. If the single re-run passes, they ship. LLM nondeterminism makes one re-run weak evidence.
6. Nothing records why the conclusion was reached.

**The problem, stated for evaluation (CCP, product terms).** Build a failure-investigation product for multi-agent LLM workflows that must:
- localize the **origin** of failures that may surface several steps later and raise no error
- **distinguish genuine causes from LLM nondeterminism** when verifying hypotheses by re-execution
- **control false alarms** and **replay cost** on limited (local/free) compute
- keep trace data **private** (PII redaction, self-hosting)
- present **auditable evidence** that a non-specialist reviewer can accept or reject

**Seoul Accord characteristics:**

| Characteristic | Status | Evidence in Granite |
|---|---|---|
| 1 Conflicting requirements | Clear | Verification confidence vs replay cost and latency; privacy (local model) vs model quality; detection sensitivity vs false alarms |
| 2 No obvious solution | Clear | Published attribution is ~60% step accuracy at best. Single-replay verification is unreliable under nondeterminism. |
| 3 Depth of knowledge | Clear | Graph/provenance algorithms; statistics (interval estimates, controls); LLM behaviour; sandboxed evaluation |
| 4 Unfamiliar issues | Clear | Nondeterministic re-execution; delayed manifestation |
| 5 Beyond standard practice | Clear | Not solvable with a tracing library or CRUD |
| 6 Diverse stakeholders | **Weak → to strengthen** | Developer, reviewer/QA, end customer, auditor, privacy officer. Needs interviews (§30, §31). |
| 7 Significant consequences | Clear | Wrong refunds, wrong advice, money moved on wrong numbers |
| 8 Interdependence | Clear | Failures propagate through dependent agents and steps |
| 9 Ill-defined cause | Clear | Whether a failure exists, its origin and the correct value are all unknown at diagnosis time |

**SDG/theme (context only, not the contribution):** SDG 9.5. This is kept from the proposal.

---

## 6. Target Users & Stakeholders

### 6.1 Personas (the UAT plan recruits real people matching these)

| Persona | Context | Goal with Granite | Key need |
|---|---|---|---|
| **P1 — Agent Developer** ("Hamza", backend/AI developer at a local software house building a support agent for a foreign client) | Builds CrewAI/LangGraph/plain-Python agent workflows. Cannot send client traces to US SaaS. Small budget. | Find why a run went wrong. Prove a fix before shipping. | Fast localisation, trustworthy verification, self-hosting |
| **P2 — QA / Reliability Reviewer** (QA engineer or team lead) | Reviews incidents. Signs off fixes. | Decide accept/reject on clear evidence | Plain-language evidence, verdicts, an audit trail |
| **P3 — Student / Researcher building agents** (FAST AI-course students, FYP teams) | Builds multi-agent projects. Has no paid tools. | Learn why agents fail. Test robustness with Fault Lab. | Free, local, explains failure modes |
| P4 — Auditor / Client representative *(secondary)* | Receives incident reports | Proof of what failed and what was done | Exportable, tamper-evident reports |

### 6.2 Stakeholder map

| Stakeholder | Interest | Influence on requirements |
|---|---|---|
| Agent developers (P1, P3) | Productivity, correctness | Inputs (SDK, import), speed, local models |
| Reviewers (P2) | Trustworthy decisions | Verdict semantics, evidence, review flow |
| End customers of the agent system (indirect) | Correct outcomes | Severity model, checks on customer-facing outputs |
| Privacy/compliance (P4) | Data protection | Redaction, retention, self-hosting |
| Supervisor and panel | Academic standard, CCP, evaluation | Traceability, evaluation design |
| Team (3 owners) | Defensible individual ownership | Module boundaries (§34) |
| External: LLM providers, framework maintainers | Licences, rate limits | Provider abstraction, adapters |

**Stakeholder validation plan** (closes W10, strengthens CCP #6). We interview **4–6 practitioners**: FAST alumni at Islamabad/Lahore software houses, an AI-course TA, and two FYP teams building agents. We use a 30-minute script (current workflow, pain, time per incident, privacy constraints, reaction to the Mid-1 slice). We record who, when and what was learned, and which requirement changed as a result. Owner: Shahoud. Done by **FYP-1 Week 12**. The same contacts form the UAT pool.

---

## 7. Product Value Proposition

| User pain | Granite capability | Measurable value (target, validated in UAT/evaluation) |
|---|---|---|
| "Run looks fine but is wrong" | Executable checks on every run → silent-failure findings | Detection recall ≥ 90% on injected faults within check coverage. False-alarm rate ≤ 5% on clean controls. |
| "I blamed the wrong agent" | Value-provenance trace-back to the *origin*, not the symptom | Top-1 origin-step accuracy ≥ 70% on the benchmark vs a last-agent baseline (reported, not assumed) |
| "Re-ran once, it passed, shipped, broke again" | Controlled replay: N=5 + 2 controls → verdict with a CI | Verdict precision ≥ 85%. INCONCLUSIVE reported, never hidden. |
| "Nobody knows why we decided that" | Evidence records + reviews + exportable report | 100% of findings carry ≥ 1 reproducible evidence item and a full audit trail |
| "Same bug came back" | Regression-test export; known-fix library (FYP-2) | Every resolved finding yields a runnable regression case |
| "Cannot send client data to SaaS / no budget" | Self-hosted Docker Compose + Ollama; PII redaction; $0 | Runs fully offline (recorded/local mode). Install-to-first-finding median < 30 min (UAT). |

---

## 8. Existing Work Audit — Retain / Modify / Replace / Remove

| Artefact | Decision | Reason / action |
|---|---|---|
| Literature review, 7 papers, `Full_Literature_Landscape_Analysis.md` | **Modify** | Add DoVer, MAST taxonomy, TRAIL, PROTEA rerun facts, and the commercial wave. Correct the overstatements (§10). |
| `Commercial_Product_Comparison.md` | **Modify** | Add Percival, Galileo Insights, Raindrop, Invariant, LangSmith Engine closed loop. Re-do the positioning. |
| Prior-FYP comparison (660 titles) | **Retain** | Strong. Cite as-is. |
| CCP justification, SDG, DEI, ethics | **Modify** | Restate in product terms (§5). DEI/ethics mostly retained. Add the UAT consent text. |
| Project Vision | **Replace** | Rewrite from §4–7 (≈2 pages) |
| SRS | **Replace** | Restructure by product module, with I/O contracts and acceptance criteria (§15–16) |
| Use Case Model + diagram, 3 SSDs | **Replace** | New actors/UCs (§15.1). Redraw SSDs for UC-03, UC-08, UC-09. |
| SDS | **Replace** | New architecture/ERD/API (§19–23). Keep the redaction and namespacing ideas. |
| Test Plan | **Replace** | Concrete cases, flaw-validity testing, tooling (§27). Keep the testing/evaluation/acceptance split. |
| Software Development Plan | **Replace** | Fix Week-8 Mid-1. Real branching/CI (§26, §28). |
| Risk register (R1–R39) | **Modify** | Archive closed risks. Re-baseline to §37. Keep the format. |
| AI usage log, Form 13 | **Retain + update** | Switch to short per-PR entries. Add new tools (Groq/Gemini, Render, Neon). |
| Traceability matrix | **Replace** | Generate from test markers (§27.7) |
| Spikes 1–8 + outputs | **Retain as research evidence** | Moved to `research/spikes/` (2026-10-06). **Port:** Spike 2 trace dataclass → trace schema; 3b injection → Fault Lab operator; 5 replay → replay engine; 6 cycle bound → graph util; 8 repair lesson → fix-suggestion interface; 1 → FYP-2 baseline harness. |
| Spike 4 detector | **Replace** | Answer-key comparison becomes the `answer_key` check type (evaluation only). Production detection uses trace-evidence and source-of-truth checks. |
| Spike 7 classifier | **Remove** | Near-random signal. Not on the product path. Keep as a reported negative. |
| `deliverables/stage-0-proposal/poc-console/frontend` | **Modify/reuse** | Copy CSS tokens, `StatusBadge`, `States` (loading/error/empty) and the layout shell into `apps/web`; replace pages and IA. The original stays frozen in `deliverables/`. |
| `deliverables/stage-0-proposal/poc-console/backend` (read-only loader) | **Remove from the product path** | Superseded by `apps/api`; stays as the frozen stage-0 artefact. |
| Defense interactive PoC HTML | **Freeze; reuse narrative** | Frozen in `deliverables/stage-0-proposal/poc-canvas/`. Its refund story becomes the real Mid-1 workflow |
| Wireframes v1/v2, Architecture Atlas | **Freeze** | Frozen in `deliverables/stage-0-proposal/design-visuals/`. Replace with new wireframes from §18 |
| Proposal decks, defense prep, root audit docs `01_…07_` | **Freeze / archive** | Decks and defense prep stay as frozen records in `deliverables/stage-0-proposal/`; the audit documents moved to `archive/proposal-phase/audits/` |
| `explanation.md`, 976 KB full explanation | **Archive** | Moved to `archive/proposal-phase/explanations/`. Not a deliverable. Do not present from it. |
| `data/raw/` (was `dev/datasets/`; 46 MB, incl. GAIA) | **Remove from git** | Keep `DOWNLOAD.md` + a fetch script. GAIA must not be redistributed. tau-bench retail data needed at runtime goes in as a small, licence-attributed seed subset. |

---

## 9. Research vs Product Boundary

| Dimension | Research contribution | Engineering contribution | Product contribution |
|---|---|---|---|
| What | (R1) Controlled verification protocol for root-cause hypotheses under LLM nondeterminism: N intervention replays + control replays + verdict rule. (R2) Deterministic value-provenance attribution vs LLM-judge attribution. (R3) A labelled fault-injection benchmark **with clean controls** (≥300 runs, 2 workflows, ≥2 runtimes). | Trace schema + adapters, sandboxed check DSL, replay engine with frozen upstream, job system, evidence store, CI/CD, deployment | Investigation workflow, Finding/Verification/Review UX, reports, regression export, self-hosting, Fault Lab |
| Evidence | Evaluation report with CIs, ablations (no controls; N=1 vs 5; no provenance), baseline comparison | Tests, coverage, CI logs, deployment record, NFR measurements | Deployed URL, UAT (SUS, task success, time-to-first-finding), stakeholder interviews |
| Where it lives | `research/eval/`, Evaluation screen (S14), report chapter | `packages/`, `apps/`, `.github/` | `apps/web`, user manual |
| Novelty status | Narrow and defensible (§10.4) | Engineering, not claimed as novelty | Value, not novelty |

**Rule:** research justifies product decisions and is reported in the Evaluation chapter. It never becomes a screen of research metrics in the operator UI (the only exception is S14 Evaluation).

---

## 10. Gap & Competitive Analysis

### 10.1 What already exists (verified 2026-10-04; the team re-checks vendor docs before each gate)

| Solution | Type | What it does that overlaps Granite | What it does **not** do (per public docs) |
|---|---|---|---|
| **DoVer** (Microsoft; arXiv preprint 2512.06749, 2026) | Research | Validates failure hypotheses by intervening at the suspected step and re-executing from there, three runs per intervention, validated if at least 2 of 3 succeed. Flips 18–28% of failed trials on GAIA/AssistantBench (Magentic-One) and recovers 49% on GSMPlus (AG2). | Not a product. Intervention verification is reported as flip rates. Repeats each intervention but runs no unfixed control replays; no control-replay protocol is part of an operator workflow, and no executable-check detection of silent failures. **Our closest prior work: cite it and compare against it.** |
| **ErrorProbe** (ACL 2026 Findings) | Research | Strategist–Investigator–Arbiter attribution with tool-grounded verification. ~59.5% step accuracy (per our lit review). | Depends on detectable anomalies. Silent failures are named as a limitation, with "test-time oracle feedbacks" as future work. No repair loop. |
| Who&When, AgenTracer, SDBL, TraceElephant | Research | Attribution benchmarks and methods | Attribution only. Benchmarks contain only failures (no clean controls). |
| **PROTEA** (Sony; ACL 2026 Demo) | Research tool | Node-level evaluation. Suggests prompt revisions. **Automatically reruns and re-evaluates** after the developer adopts a fix. | Human-steered prompt refinement. No attribution protocol, no controls/verdicts. Closed. |
| **LangSmith Engine** (2026) | Commercial | Clusters production failures, diagnoses root cause against code, drafts fix PRs and evaluators, reopens issues on regression | Locked to LangSmith. Mechanism and accuracy not published. SaaS. |
| **Patronus Percival** | Commercial | Detects 20+ failure modes in agent traces. Clusters errors. Suggests prompt fixes. | LLM-judged. No replay verification documented. SaaS. |
| **Galileo Insights Engine** | Commercial | Identifies failure modes, root causes and solutions. Links to the exact span. | LLM/eval-model based. SaaS. |
| **Raindrop** (≈$50M raised) | Commercial | Markets **silent-failure** detection in production agents. "Experiments" validates fixes. "Simulations" replays traffic against proposed changes. | Conversation-signal based (frustration etc.). Not step-level causal attribution. SaaS. |
| **Invariant Labs analyzer** (OSS; acquired by Snyk 2025) | OSS | **Rule-based checks over agent traces** (policy language, information-flow) | Security/policy focus. No attribution or verification loop. |
| Langfuse, Arize Phoenix, Braintrust, W&B Weave, Opik | OSS/commercial | Trace capture, graph visualization, evals, datasets | Human-driven diagnosis |
| CrewAI / LangGraph built-ins | Frameworks | Tracing, checkpoints, time-travel/replay (LangGraph) | No attribution, no verdicts |
| S24-011-D-HDLM (closest prior FYP) | Prior FYP | Hallucination detection in single-LLM output | Single model. No multi-agent attribution or verification. |

### 10.2 Commodity features: build them, do not market them as novelty

Trace capture and graph view · dashboards · LLM-as-judge scoring · prompt-fix suggestions · retry · framework adapters · report export · rule checks on traces (Invariant) · "silent failure" as a phrase (Raindrop) · auth/projects.

### 10.3 Claims to retire (must be removed from all docs and slides by Mid-1)

| Old claim | Why it fails | Replacement wording |
|---|---|---|
| "Catches silent failures ErrorProbe admits it cannot see" | ErrorProbe counts verifiable constraints as detectable signals. Silent = no signal. | "Implements the **test-time oracles** ErrorProbe names as future work: operator-declared executable checks that turn silent failures into detectable ones." |
| "Nobody verifies a fix before trusting it" | DoVer, PROTEA, Raindrop, LangSmith Engine | "Verification that is **robust to nondeterminism**: N intervention replays + control replays + pre-registered verdict rule, with all artefacts recorded." |
| "Commercial tools only capture traces; diagnosis is manual" | Outdated in 2026 | "Commercial diagnosis is LLM-judged, SaaS-hosted, and does not publish accuracy. Granite is evidence-first, self-hosted, and measured on a labelled benchmark with clean controls." |
| "First cross-architecture benchmark" | Unprovable; TRAIL/MAST/Who&When/TracerTraj exist | "A small labelled benchmark with injected-fault ground truth **and clean controls**, on ≥2 runtimes." |
| "Framework-agnostic" as a differentiator | OpenTelemetry/Langfuse already are | Keep as a requirement, not a claim |

### 10.4 Defensible differentiation (what remains, and how it is proven)

1. **Executable-check detection + deterministic provenance attribution.** No LLM is needed for the core findings. *Proof:* origin accuracy and false-alarm rate vs last-agent and LLM-judge baselines on the benchmark.
2. **Verification protocol with controls and explicit uncertainty** (CONFIRMED/REFUTED/INCONCLUSIVE + CI). *Proof:* ablation showing single-replay verification produces more false confirmations than N=5 + controls; verdict precision.
3. **Evidence-first records + human review + regression export** as one workflow. *Proof:* UAT task success, and a reviewer's ability to decide from the report alone.
4. **Self-hosted, $0, local-model capable.** *Proof:* offline run from Docker Compose. This is an adoption constraint that shapes the architecture (deterministic core, small models), not a "local version" claim.

### 10.5 Contribution statement (handbook C.4 template)

> Existing multi-agent failure-attribution methods (Who&When, AgenTracer, ErrorProbe) and commercial agent debuggers (LangSmith Engine, Percival, Galileo) produce root-cause hypotheses mainly from LLM judgement over logs. DoVer showed that re-executing from an intervention point can validate such hypotheses. These approaches remain weak when (a) a failure raises no error signal, (b) re-execution is nondeterministic, so a single replay can mislead, and (c) teams cannot send traces to external services.
>
> **We contribute Granite**, a self-hostable investigation product that:
> 1. detects silent failures with operator-declared executable checks (test-time oracles)
> 2. localizes their origin with deterministic value-provenance tracing
> 3. verifies each hypothesis with a controlled replay protocol: N intervention replays and M control replays under a pre-registered verdict rule, with every artefact recorded as evidence.
>
> **We evaluate it** on a labelled fault-injection benchmark with clean controls against last-agent and LLM-judge attribution baselines. We measure origin accuracy, false-alarm rate, verdict precision and recovery rate.

**Stream-A delta sentence (C.18.2):**

> ErrorProbe reports up to 59.5% step accuracy on Who&When (about 43% averaged across benchmarks) under the assumption that failures emit detectable anomalies. DoVer reports 18–28% flip rates on GAIA/AssistantBench and 49% on GSMPlus, using three re-executions per intervention (2-of-3 rule) on frontier models, without control replays. We extend this to workflows where failures are silent and models are small and nondeterministic. We evaluate on our clean-control benchmark using origin accuracy, false-alarm rate and verdict precision.

---

## 11. Final Product Scope

### 11.1 Product modules (user-facing names)

| Module | User-facing name | One-line job |
|---|---|---|
| M1 | **Run** (Workflow Runner) | Execute a registered multi-agent workflow on user input, optionally with an injected fault. Record a full trace. |
| M2 | **Import** (Trace Import / SDK) | Bring traces from elsewhere: JSON upload (Final-1), Python SDK + LangGraph/CrewAI adapters (Final-1/Mid-2) |
| M3 | **Check** (Checks Engine) | Evaluate executable checks on every run. Silent failures become findings. |
| M4 | **Trace back** (Root-Cause Attribution) | Rank origin hypotheses by value provenance. Optional LLM second opinion (labelled unverified). |
| M5 | **Verify** (Verification Lab) | Test a hypothesis or proposed fix by controlled replay with controls → verdict + evidence |
| M6 | **Review & Resolve** | Human decision, fix suggestion (Repair), recovered run, known-fix library |
| M7 | **Report** | Finding report (MD/JSON/PDF), regression-test export, history and search |
| M8 | **Fault Lab & Evaluation** (research/QA) | Batch-generate labelled runs (with clean controls). Compute metrics vs baselines. |

### 11.2 Explicitly out of scope (whole FYP)

- Multi-tenant SaaS, billing, RBAC beyond a single reviewer identity
- Kubernetes or message queues
- Auto-applying fixes to a user's production system
- Training custom models or RL
- Full benchmarking on 7 frameworks
- Preventive classifier
- Real customer data on the public demo instance

### 11.3 Mapping approved mechanisms → product modules (proves the core idea is preserved)

| Approved mechanism (proposal §7.0) | New home | Change |
|---|---|---|
| 1 Fault-injection harness | M1 fault toggle (Mid-1) → M8 Fault Lab (Final-1) | Same mechanism, given a UI |
| 2 Cross-architecture benchmark | M8 | Target 500–1,000 → ≥300 Must / 500 Should. Clean controls kept. |
| 3 Culprit Agent · 4 Error Step Localization | M4 | Provenance-first (deterministic). The LLM path (ErrorProbe-style) becomes "second opinion" and baseline. |
| 5 Verification Agent | M3 evidence re-check (V1) + M5 (V2) | Made concrete as verification levels |
| 6 Repair Agent | M6 "Suggest fix" (LLM; atomic-field interface from Spike 8) | Final-1 |
| 7 Semantic Error Diagnostic | M3 Checks Engine | **Reframed:** test-time oracles over trace evidence and sources of truth, not an answer key |
| 8 Verified Automatic Repair | M5 | Adds control replays, verdict rule, regression guard |
| 9 Recovery Controller (Tier 2) | M6 "Recovered run" = replay-to-completion with the verified fix | Tier-2 gate resolved by design: the pre-registered fallback (replay-based resumption) becomes the design. Recorded in C-01. |
| 10 Verified Repair Memory (Tier 2) | M6 Known-fix library (deterministic signature match) | FYP-2 Should. Memory on/off ablation retained as evaluation. |
| SDK + backend + dashboard | M2 + platform + all screens | SDK at Final-1 |
| ErrorProbe reproduction (proposal top priority) | M8 baseline track (FYP-2, Should) | Demoted. Reported honestly; not on the Mid-1 path. |

### 11.4 Change record C-01 (to be signed by the supervisor)

| Field | Content |
|---|---|
| What changed | Workflow redefined around the Verified Finding. Modules renamed. Mechanisms remapped (§11.3). Evaluation baseline set changed from "ErrorProbe reproduction ±10 pts" to "last-agent + LLM-judge (Who&When all-at-once) + ErrorProbe-lite as reference". Benchmark ≥300/500. Tier-2 gates resolved by design. Deployment target = Render + Neon (public demo) + Docker Compose (self-hosted). Hosted free LLM for the public demo. |
| Why | Panel decision (A1–A5). Feasibility (W4). Novelty re-baselining (W3). The free-tier change in HF Spaces. |
| Evidence prompting it | Panel comments. `git`/code inspection. DoVer/commercial evidence (§10.1). Spike 1 (13% step accuracy on a 3B model). |
| Affects | CCP wording (product terms; same characteristics), contribution statement, SRS/SDS/test plan, timeline |
| Not affected | Problem, Stream A, ownership areas, datasets, $0, ethics/DEI |
| Made before results? | Yes. No evaluation results exist yet, so the metric/baseline change is legitimate under C.5.3. |
| Approved by / date | Dr. Adil Majeed / ______ |

---

## 12. Feature Prioritization (MoSCoW × milestone)

Legend: **M** = Must, **S** = Should, **C** = Could, **—** = not in this milestone, **F** = Future (outside FYP).

*v1.1:* the Mid-1 column is the **Track T2** target. Tracks T0 and T1 cut the items listed in §30.2 and §30.4. Those items move to the first days of Iteration 2 (§31).

| Feature | Mid-1 | Final-1 | Mid-2 | Final-2 |
|---|---|---|---|---|
| F1 Run Refund Desk workflow from UI (live/recorded LLM, fault toggle) | **M** | M | M | M |
| F2 Trace store + Run detail (steps list, graph, step inspector) | **M** | M | M | M |
| F3 Checks engine (assert / truth / policy / schema) + findings | **M** (4 checks) | M (+check editor) | M | M |
| F4 Provenance attribution (ranked hypotheses + evidence) | **M** | M | M | M |
| F5 Verification: replay N + controls → verdict + evidence | **M** | M | M | M |
| F6 Review (accept/reject/needs-info + comment) + finding states | **M** | M | M | M |
| F7 History: runs/findings lists, filters, search | **M** (basic) | M | M | M |
| F8 Finding report export (MD/JSON) | S | **M** (+PDF) | M | M |
| F9 Graceful errors (LLM down, malformed input, ABSTAIN) | **M** (1 shown live) | M | M | M |
| F10 Trace import (Granite Trace v1 JSON; Who&When converter) | C | **M** | M | M |
| F11 Second workflow: Math Crew (GSM8K) | — | **M** | M | M |
| F12 Fault Lab: 3 fault types + clean controls, batch generation | 1 type | **M** (3 types) | M | M |
| F13 Python SDK + LangGraph adapter | — | **M** | M | M |
| F14 CrewAI adapter | — | S | **M** | M |
| F15 Fix suggestion (LLM Repair Agent, atomic field / prompt patch) → verified as a fix experiment | — | **M** | M | M |
| F16 Recovered run (apply verified fix → completed run) | — | **M** | M | M |
| F17 Regression-test export (JSON case + pytest) | — | **M** | M | M |
| F18 PII redaction before storage | S | **M** | M | M |
| F19 LLM second-opinion hypothesis (ErrorProbe-lite) | — | S | **M** | M |
| F20 Evaluation module + screen (metrics vs baselines, CIs, ablations) | — | v0 (**M**) | **M** v1 | M |
| F21 Known-fix library (verified repair memory) | — | — | S | S |
| F22 Login (GitHub OAuth) + reviewer identity; API keys for SDK ingest | — | C | **S** | S |
| F23 Retention policy + delete run | — | C | S | S |
| F24 Webhook/Slack notification on confirmed finding | — | — | C | C |
| F25 3rd framework, compatibility layer for 7 frameworks, calibration curves, leaderboard, chaos testing | — | — | — | F |

---

## 13. End-to-End Product Workflow

### 13.1 The canonical workflow

```mermaid
flowchart LR
  A["1 Ingest<br/>run a workflow or import a trace"] --> B["2 Normalize<br/>validate, redact PII, build graph"]
  B --> C["3 Check<br/>evaluate executable checks"]
  C -->|all checks pass| P["Run passed<br/>stored, no finding"]
  C -->|a check fails| D["4 Detect<br/>Finding with symptom"]
  D --> E["5 Trace back<br/>ranked root-cause hypotheses"]
  E --> F["6 Verify<br/>replay with intervention plus controls"]
  F --> G{"Verdict"}
  G -->|confirmed| H["7 Review<br/>human accepts or rejects"]
  G -->|refuted| E
  G -->|inconclusive| H
  H --> I["8 Resolve<br/>fix verified, recovered run, regression test"]
  I --> J["9 Record and report<br/>evidence, audit log, export"]
```

### 13.2 The same workflow for three audiences

| Stage | For a non-technical evaluator | For an end user (developer/reviewer) | For a technical developer |
|---|---|---|---|
| 1 Ingest | "Granite runs the AI team on a request, or reads a log of a past run." | Click **New run** and fill the form, or **Import trace** and upload a JSON. | `POST /projects/{id}/runs` or `POST /runs:import` → job → `run`, `step`, `step_edge` rows |
| 2 Normalize | "It tidies the log and hides personal data." | Wait about 1 s. | Pydantic validation, regex PII redaction, lineage edges from `reads` or value matching, cycle bound |
| 3 Check | "It runs automatic tests on the answer and on each step." | Checks tab shows PASS/FAIL/ABSTAIN. | Sandboxed expression evaluator over step fields + source-of-truth functions → `check_result` |
| 4 Detect | "A failed test that raised no error is a *silent failure*. Granite opens a case." | A finding appears with a severity badge. | `finding` row, kind = silent_failure if run.status = completed |
| 5 Trace back | "It follows the wrong number backwards to where it first went wrong." | See ranked suspects with reasons. | Provenance BFS over lineage; per-step contract checks; truth mismatches; ranking |
| 6 Verify | "It re-runs the rest of the process with the suspect corrected, several times, plus runs without the correction for comparison." | Click **Verify**, choose N, watch progress, read the verdict. | Replay engine: freeze upstream, patch origin, re-execute downstream with pinned params; N + M replays; verdict rule; Wilson CI |
| 7 Review | "A person reads the evidence and signs off." | Accept, reject or ask for more information, with a comment. | `review` row, finding state transition, `audit_log` |
| 8 Resolve | "The fix is proven and kept as a test so the bug can't silently return." | Apply verified fix → recovered run. Export regression test. | Fix experiment (kind = fix), recovered run promotion, regression case export |
| 9 Record | "Everything is saved and can be printed as a report." | History pages; **Export report**. | Hashed `evidence`, `report` artefacts, OpenAPI-exposed records |

### 13.3 Finding lifecycle (state machine, enforced in code)

```mermaid
stateDiagram-v2
  [*] --> Open: outcome check fails
  Open --> Hypothesized: trace-back produced hypotheses
  Hypothesized --> Verifying: verification started
  Hypothesized --> EvidenceSupported: strong provenance evidence but no replay is defined for that step (set automatically)
  Verifying --> Confirmed: verdict confirmed
  Verifying --> Refuted: verdict refuted
  Verifying --> Inconclusive: verdict inconclusive
  Verifying --> Hypothesized: experiment error
  Refuted --> Verifying: verify next hypothesis
  Inconclusive --> Verifying: run more replays (added 2026-10-07, change C-02a)
  Confirmed --> Accepted: reviewer accepts
  Confirmed --> Rejected: reviewer rejects
  Inconclusive --> Accepted: reviewer accepts with note
  Inconclusive --> Rejected: reviewer rejects
  EvidenceSupported --> Accepted: reviewer accepts
  EvidenceSupported --> Rejected: reviewer rejects
  Accepted --> Resolved: fix verified and regression case passes
  Accepted --> WontFix: reviewer decision
  Rejected --> [*]
  Resolved --> [*]
  WontFix --> [*]
```

**Run lifecycle:** `queued → running → completed | errored → analyzed`. Replay runs carry `source=replay` and `experiment_id`.

**Invariant:** illegal transitions raise errors. Unit tests cover every edge, plus at least 3 illegal ones.

*Implementation note (2026-10-07):* the diagram generated from the code is [`docs/diagrams/finding-state-machine.md`](../diagrams/finding-state-machine.md); a CI step fails if it drifts from `granite_core.lifecycle`. The two lines above marked as added or changed are the only differences from the original plan.

---

## 14. Detailed Input → Processing → Output → Verification Model

### 14.1 Core vocabulary (used identically in UI, API, DB, report)

| Term | Definition |
|---|---|
| **Project** | A workflow under investigation plus its checks and settings |
| **Run** | One execution (or imported record) of a workflow: ordered **steps** with inputs/outputs |
| **Step** | One agent action: `llm`, `tool`, `code` or `handoff`. Has structured `inputs`, `outputs`, `reads` (lineage). |
| **Check** | An executable rule returning PASS / FAIL / ABSTAIN / ERROR. **Scope:** `outcome` (end-to-end) or `step` (a *contract* of one step). |
| **Silent failure** | A run that completed with no error, where ≥ 1 outcome check FAILs |
| **Finding** | The case opened for a failed outcome check (or an explicit error) |
| **Hypothesis** | "Step X (agent Y) is the origin", with method, score and rationale |
| **Evidence** | An immutable, typed, SHA-256-hashed artefact supporting or refuting a hypothesis |
| **Experiment** | A verification run of a hypothesis (causal) or of a proposed fix (fix), made of replays |
| **Verdict** | CONFIRMED / REFUTED / INCONCLUSIVE / ERROR, decided by the pre-registered rule |
| **Review** | A human decision on a finding |

### 14.2 Per-feature I/O cards

Each card follows the panel's chain: **Input → Processing → Output → Issue → Evidence → Verification → Result → Record → User action.**

#### F1 — Run a workflow (M1)

| Element | Specification |
|---|---|
| User provides | Project (e.g. *Refund Desk*); customer message (text, 1–2,000 chars); customer e-mail (seeded tau-bench users, select or type); order ID (select from seeded orders); **fault** (none / stale tool data / corrupted handoff / dropped instruction — only "stale tool data" at Mid-1); **LLM mode** (live / recorded); replay defaults |
| System accepts | JSON body validated by Pydantic. Unknown order/e-mail → 422 with a field-level message. Live mode is rate-limited (e.g. 10 runs/hour per IP on the public demo). |
| Preprocessing | Seed DB snapshot pinned (tau-bench subset). Fault plan created (`fault_injection` row with ground-truth origin) *before* execution. |
| Processing | The runner executes 5 steps in topological order: Intake (LLM, JSON) → Order Lookup (tool) → Policy (LLM, JSON) → Refund Calculator (LLM, JSON) → Writer (LLM, text). Every step's inputs, outputs, prompt hash, model, params and timings are recorded. |
| Output | Run with status and a final customer message. Analysis (F3, F4) starts automatically. |
| Issue identified | None at this stage. Errors (LLM timeout, tool failure) become run status `errored` + finding kind `explicit_error`. |
| Evidence | Step snapshots (`STEP_SNAPSHOT`), fault-injection record (hidden from the attribution engine) |
| Verification | — (input to F3/F4) |
| Persisted | `run`, `step`, `step_edge`, `fault_injection`, `job` |
| User action | Open the run; re-run with the same inputs; run without the fault |
| Failure states | LLM provider unavailable → run `errored`, banner "LLM provider unreachable — try Recorded mode", retry button; tool exception → step error shown |

#### F2 — Import a trace (M2, Final-1)

| Element | Specification |
|---|---|
| User provides | `.json` file ≤ 5 MB, ≤ 500 steps, in **Granite Trace v1** (§22.4) or **Who&When** format (auto-detected); target project |
| System accepts | Schema-validated. The validation report lists the exact JSON path of each error. Duplicate `step_id`, dangling `reads` or a lineage cycle beyond the bound produce errors. |
| Preprocessing | Format conversion (Who&When → Granite) and PII redaction |
| Processing | Same as F3/F4. **No replay**: there is no runnable workflow. |
| Output | Run with `source=import`, findings, hypotheses |
| Verification available | **V1 only** (evidence re-check: recompute contracts; re-query source-of-truth if the project defines one). The UI shows "Replay unavailable — trace has no runnable workflow attached". |
| Persisted | Original file hash (`sha256`), normalized run |
| User action | Fix the file using the validation report; attach to a project with checks |

#### F3 — Checks and silent-failure detection (M3)

| Element | Specification |
|---|---|
| User provides | Check definitions (YAML/JSON or form). Mid-1 uses seeded checks; the editor arrives at Final-1. Fields: `id, name, type (assert/truth/policy/schema/answer_key), scope (outcome/step), step, expression, tolerance, severity, enabled`. |
| System accepts | The expression must parse under the **whitelisted DSL**: field refs `step.field`, arithmetic, comparisons, `and/or/not`, functions `approx, sum, len, round, contains, number_in(text)`, `truth.<registered_fn>(…)`. **No Python `eval`.** Dry-run against a sample run before saving. |
| Processing | For each run, evaluate all enabled checks. Missing field → **ABSTAIN** (counts towards coverage). Evaluator exception → **ERROR** (never silently PASS). |
| Output | `check_result` per check: status, observed vs expected values, message |
| Issue identified | Outcome check FAIL → Finding (`silent_failure` if the run completed, else `explicit_error`). Step-contract FAIL → evidence for attribution (and a finding if severity ≥ high). |
| Evidence | `CHECK_COMPUTATION`: expression, resolved inputs, computed value, tolerance, result. `SOURCE_OF_TRUTH_QUERY`: function, arguments, returned value, timestamp. |
| Verification | V1: anyone can re-evaluate the stored computation (`POST /check-results/{id}:reevaluate`) and get an identical result. Byte-identical by design: deterministic, no LLM. |
| Persisted | `check`, `check_result`, `finding`, `evidence` |
| User action | Open the finding; disable or edit a noisy check (versioned; old results keep their `check_version`) |

**Mid-1 seeded checks (Refund Desk):**

| ID | Scope | Type | Rule (plain language) |
|---|---|---|---|
| CHK-OUT-1 | outcome | truth | The amount stated to the customer = sum of current catalogue prices of the eligible returned items (±0.01) |
| CHK-OUT-2 | outcome | policy | Refund only for orders with status `delivered` owned by the identified user |
| CT-LOOKUP | step (Order Lookup) | truth | Each item price returned by the tool = catalogue price |
| CT-CALC | step (Calculator) | assert | Refund = sum of the prices the Calculator received (±0.01) |
| CT-WRITER | step (Writer) | assert | The number in the message = Calculator's refund |

#### F4 — Trace back to the root cause (M4)

| Element | Specification |
|---|---|
| Input | A finding (failed outcome check + its referenced fields), run graph with lineage, step-contract results, truth-query results |
| Processing (deterministic) | §21.4 algorithm: walk lineage backwards from the symptom fields. Classify each contributing step as **consistent propagator** (its contract passes on its own inputs) or **inconsistent** (contract fails / truth mismatch / input ≠ upstream output, i.e. handoff corruption). Origin candidates = earliest inconsistent steps. Rank by evidence strength (truth mismatch > contract violation > handoff drift > structural only), then by topological order. |
| Optional | "Ask LLM for a second opinion" (Final-1 S / Mid-2 M) produces a hypothesis with `method=llm_opinion`, labelled **Unverified opinion**. |
| Output | 1–5 ranked hypotheses: origin step/agent, score (0–1, from evidence weights, never self-reported by an LLM), rationale in plain language, linked evidence |
| Evidence | `PROVENANCE_PATH` (the backward path with values at each hop), contract and truth evidence |
| Verification | Hypotheses are *claims*. They are verified only by F5 (or V1 for trace-only runs). |
| Persisted | `hypothesis`, `evidence` |
| User action | Verify H1 (default), verify another, or add a manual hypothesis |

#### F5 — Verify a hypothesis or fix (M5): the core of the panel's question

| Element | Specification |
|---|---|
| User provides | Hypothesis (or proposed fix); **intervention** (auto-proposed: "replace `lookup.items[1].price` 19.50 → 19.75 (source of truth)"; or a user-entered value; or an LLM-suggested prompt patch at Final-1); N (default 5, 1–10); controls M (default 2, 0–5) |
| System accepts | The intervention must name **one atomic field** or one prompt (Spike 8 lesson). The target step must be in the run. The workflow must be runnable (else 409 "replay unavailable"). |
| Processing | Replay protocol §14.4 |
| Output | Experiment: k/N intervention passes, c/M control passes, pass rate, Wilson 95% CI, verdict, duration, LLM calls/tokens, per-replay table |
| Issue identified | Confirms or refutes the causal claim. Also catches **regressions**: a replay in which a previously passing check now FAILs. |
| Evidence | Each replay is a full run (`source=replay`). `REPLAY_OUTPUT`, `DIFF` (original vs replay step outputs), `VERDICT_COMPUTATION` (inputs to the rule + rule version) |
| Result handling | CONFIRMED → finding `Confirmed`, offer "Review". REFUTED → hypothesis marked refuted, offer "Verify next hypothesis". INCONCLUSIVE → offer "Increase N" or "Review with note". ERROR (LLM down mid-way) → partial results kept, finding returns to `Hypothesized`, retry button. |
| Persisted | `experiment`, replay `run`s, `evidence`, `audit_log` |
| User action | Review; increase N; verify another hypothesis; export |

#### F6 — Review and resolve (M6)

| Element | Specification |
|---|---|
| Input | Finding in Confirmed / Inconclusive / EvidenceSupported. Reviewer name (Mid-1: from a local profile; FYP-2: OAuth identity). Decision (accept / reject / needs-info). Comment (required for reject and for accepting an inconclusive finding). |
| Processing | State transition + audit log. On *accept* at Final-1+: "Suggest fix" (LLM Repair Agent, F15) or "Use verified intervention as fix" → fix experiment (F5 with `kind=fix`) → if CONFIRMED, **recovered run** = best replay promoted, plus a **regression case** generated |
| Output | Finding `Accepted` / `Rejected` / `Resolved` / `WontFix`; recovered run; regression case |
| Persisted | `review`, `fix`, `audit_log`, `report` |

#### F7 — Report and history (M7)

| Element | Specification |
|---|---|
| Input | Finding ID; format (Markdown, JSON; PDF at Final-1) |
| Output | A report with: summary (symptom → origin → verdict → decision), run metadata (model, params, versions), check computations, provenance path, experiment table, evidence hashes, review trail, and how to reproduce (API calls) |
| Verification | The report embeds evidence hashes. `GET /evidence/{id}` re-serves the artefact, so anyone can confirm the hash. |
| Regression export | JSON case (inputs + fault + expected check outcomes) + generated `pytest` file. Runs in CI in recorded mode. |

#### F8 — Fault Lab and Evaluation (M8; Final-1 v0, Mid-2 v1)

| Element | Specification |
|---|---|
| Input | Workflow(s), runtime(s) (Granite runner, LangGraph, CrewAI), fault types × count, clean-control % (default 20%), seed, LLM mode |
| Processing | Batch job generates runs with ground-truth labels. Runs the full analysis (+ optional verification) on each. Computes metrics with bootstrap CIs. Runs baselines on the same runs. |
| Output | Benchmark table; metrics dashboard (S14); downloadable CSV; datasheet |
| Verification of the verifier | Compare findings/hypotheses/verdicts with ground truth (§27.5) |

### 14.3 Verification levels (shown as a badge on every finding)

| Level | Name | Meaning | How it is achieved | Available for |
|---|---|---|---|---|
| **V0** | Detected | A check failed | Checks engine | All runs |
| **V1** | Evidence-reproduced | The failing computation and the origin evidence re-evaluate identically from stored data, and source-of-truth mismatches re-query identically | Deterministic re-evaluation | All runs (incl. imported) |
| **V2** | Replay-verified | Intervention at the hypothesized origin flips the outcome reliably, and controls do not flip | Replay protocol §14.4 | Runnable workflows |
| **V3** | Human-confirmed | Reviewer accepted after reading the evidence | Review | All |

### 14.4 Controlled replay protocol (pre-registered, version `VR-1`)

1. **Plan.** From the original run, take the topological order. Steps *before* the intervention step are **frozen**: their recorded outputs are reused verbatim, with no LLM call.
2. **Intervene.** At the target step, apply the intervention:
   - **causal:** set the field to the source-of-truth or user value
   - **fix:** apply a patched prompt or parameter and re-execute that step
3. **Re-execute downstream.** Run all downstream steps with the **recorded model, temperature and max-tokens**, plus a seed where the provider supports one. Repeat **N** times.
4. **Controls.** Re-execute the same downstream steps **M** times *without* the intervention. This separates "the fix worked" from "the LLM just answered differently this time".
5. **Judge each replay.**
   - A replay **passes** if every outcome check that failed in the original now PASSes, **and no check that passed in the original now FAILs** (regression guard).
   - An ABSTAIN counts as not-pass.
6. **Verdict (VR-1 thresholds):**
   - **CONFIRMED** if k/N ≥ 0.8 **and** c/M ≤ 0.2 (when M > 0)
   - **REFUTED** if k/N ≤ 0.2
   - **INCONCLUSIVE** otherwise (including k/N ≥ 0.8 with c/M > 0.2, meaning the failure is not stable)
   - **ERROR** if fewer than N replays finished
7. **Report.** k, N, c, M, Wilson 95% CI on k/N, duration, LLM calls, tokens, rule version.

*Thresholds are fixed before any evaluation result exists (C.5.3). An ablation reports how verdicts change with N ∈ {1, 3, 5} and with M = 0.*

**Why the controls matter (say this at every evaluation).** A single re-run that passes may only reflect sampling luck. If the uncorrected controls also pass, the "fix" proved nothing. DoVer repeats each intervention three times (2-of-3 rule), which reduces luck but runs no uncorrected controls, so it does not separate these two cases. Our protocol does.

### 14.5 Evidence model (what is captured, exactly)

| Evidence type | Payload | Reproducible? | Created by |
|---|---|---|---|
| `STEP_SNAPSHOT` | Step inputs/outputs (redacted), prompt hash, model, params, timings | Yes (stored) | Runner/import |
| `CHECK_COMPUTATION` | Expression, resolved field values, computed value, tolerance, status, check version | Yes: deterministic re-evaluation | Checks engine |
| `SOURCE_OF_TRUTH_QUERY` | Function, arguments, returned value, data snapshot version | Yes, against the pinned snapshot | Checks engine |
| `PROVENANCE_PATH` | Ordered hops (step, field, value, consistency verdict) | Yes, deterministic | Attribution |
| `REPLAY_OUTPUT` | Replay run ID, per-check results | Statistically (that is the point of N/M) | Verification |
| `DIFF` | Field-level diff original vs replay | Yes | Verification |
| `VERDICT_COMPUTATION` | k, N, c, M, CI, thresholds, rule version, verdict | Yes, deterministic given the counts | Verification |
| `LLM_OPINION` | Prompt hash, model, raw text, parsed hypothesis | No (labelled unverified) | Attribution (optional) |
| `REVIEWER_NOTE` | Decision, comment, reviewer, time | N/A | Review |

**Every evidence row** stores `sha256(canonical_json(payload))`, `created_at`, `created_by` and `reproduce` (an API call or CLI command). Evidence is **append-only**: corrections create new rows.

### 14.6 "Are the flaws real?" Validating the validator

| Question | Method | Metric / target |
|---|---|---|
| Does Granite find real failures? | Fault Lab ground truth (injected origin known by construction) | Detection recall ≥ 0.90 within check coverage |
| Does it cry wolf? | 20% clean-control runs (no injection) | False-alarm rate ≤ 5% (95% CI reported) |
| What about natural failures (LLM slips)? | Two members independently label 50 natural findings as true/false. Cohen's κ. Disagreements adjudicated. | Precision ≥ 0.85; κ ≥ 0.6 |
| Is the origin right? | Compare top-1 hypothesis with ground-truth origin | Top-1 origin-step accuracy ≥ 0.70 (vs last-agent and LLM-judge baselines) |
| Are verdicts right? | CONFIRMED on a true origin = correct; CONFIRMED on a wrong origin = false confirmation | Verdict precision ≥ 0.85; false-confirmation rate ≤ 0.10 |
| Does coverage limit claims? | Report ABSTAIN rate per check and per workflow | Reported, no target (honest boundary) |

---

## 15. Functional Requirements

### 15.1 Actors and use cases (replace the proposal UC model)

**Actors:**
- **Developer** (primary)
- **Reviewer** (primary; may be the same person in a small team)
- **Administrator** (self-host operator, FYP-2)
- **LLM Provider** (external system)
- **Instrumented Workflow** (external system via SDK)

| UC | Name | Actor | Milestone |
|---|---|---|---|
| UC-01 | Configure project (workflow, settings) | Developer | Mid-1 (seeded, read-only); Final-1 (edit) |
| UC-02 | Define / edit / dry-run checks | Developer | Final-1 |
| UC-03 | Run workflow with input (optional fault) | Developer | **Mid-1** |
| UC-04 | Import trace file | Developer | Final-1 |
| UC-05 | Inspect run trace (graph, steps, checks) | Developer, Reviewer | **Mid-1** |
| UC-06 | Analyze run (checks → findings → hypotheses) | system, «include» from UC-03/04 | **Mid-1** |
| UC-07 | Investigate finding | Developer, Reviewer | **Mid-1** |
| UC-08 | Verify hypothesis by controlled replay | Developer, LLM Provider | **Mid-1** |
| UC-09 | Review finding (accept/reject/needs-info) | Reviewer | **Mid-1** |
| UC-10 | Suggest and verify a fix; produce recovered run | Developer, LLM Provider | Final-1 |
| UC-11 | Export report / regression test | Developer, Reviewer | Final-1 (S at Mid-1) |
| UC-12 | Browse and search history | Developer, Reviewer | **Mid-1** |
| UC-13 | Generate labelled benchmark (Fault Lab) | Developer | Final-1 |
| UC-14 | Run evaluation against baselines | Developer (research) | Final-1 v0 / Mid-2 |
| UC-15 | Instrument own workflow via SDK | Developer, Instrumented Workflow | Final-1 (LangGraph), Mid-2 (CrewAI) |
| UC-16 | Reuse a known verified fix | Developer | Mid-2 (S) |
| UC-17 | Manage API keys, retention, delete data | Administrator | Mid-2 (S) |

### 15.2 Functional requirements (testable)

Format: ID · requirement · priority · milestone · acceptance criterion (AC).

**Run / Import**
- **FR-RUN-01** The system shall execute the Refund Desk workflow from a validated input form and record every step's inputs, outputs, model, parameters and timings. · M · Mid-1 · *AC:* a run with valid input yields 5 steps with non-null `inputs/outputs/started_at/ended_at`, and the UI shows the run within 3 s of completion.
- **FR-RUN-02** The system shall let the user enable a named fault before the run, and record its ground truth (target step, field, original, injected value) without exposing it to attribution. · M · Mid-1 · *AC:* `fault_injection` row exists; the attribution module has no read path to it (enforced by a test).
- **FR-RUN-03** The system shall support LLM modes `live` and `recorded`. Recorded mode replays cached responses keyed by (prompt hash, model, params, replay index). · M · Mid-1 · *AC:* the same input in recorded mode produces byte-identical step outputs across 3 runs.
- **FR-RUN-04** The system shall mark a run `errored` and show an actionable message when the LLM provider is unreachable or times out (default 30 s per call). · M · Mid-1 · *AC:* with the provider URL pointed to a closed port, the run ends `errored` within 35 s, and the UI shows the banner and retry.
- **FR-IMP-01** The system shall import Granite Trace v1 and Who&When JSON files ≤ 5 MB and ≤ 500 steps, and return a validation report with JSON paths for every error. · M · Final-1 · *AC:* the 6 malformed fixture files each yield the expected error path; 3 valid fixtures import.
- **FR-IMP-02** Imported runs shall be marked non-replayable, with V1 verification only. · M · Final-1.
- **FR-SDK-01** The Python SDK shall capture a LangGraph workflow's node inputs and outputs into Granite Trace v1 and submit them to the API with an API key, without modifying the user's node functions beyond adding a decorator/callback. · M · Final-1 · *AC:* the sample LangGraph app produces a run in Granite with all nodes; time-to-first-finding in the pilot < 30 min.
- **FR-SDK-02** CrewAI adapter (same AC). · M · Mid-2.

**Check**
- **FR-CHK-01** The system shall evaluate all enabled checks on every run and store PASS/FAIL/ABSTAIN/ERROR with observed and expected values. · M · Mid-1.
- **FR-CHK-02** Check expressions shall be evaluated by a whitelisted AST evaluator. Any disallowed construct (attribute access outside refs, imports, comprehensions, lambdas, calls to non-whitelisted functions) shall be rejected at save time. · M · Mid-1 · *AC:* the 15 malicious expressions in the test suite are rejected.
- **FR-CHK-03** Missing referenced fields shall yield ABSTAIN, never PASS. · M · Mid-1.
- **FR-CHK-04** A completed run with ≥ 1 failing outcome check shall create a finding of kind `silent_failure` with severity = max severity of the failing checks. · M · Mid-1.
- **FR-CHK-05** Users shall create, edit (versioned), dry-run and disable checks from the UI. · M · Final-1.
- **FR-CHK-06** `truth` checks shall query registered source-of-truth functions against a pinned data snapshot and store the query and response as evidence. · M · Mid-1.

**Trace back**
- **FR-ATT-01** For each finding, the system shall produce 1–5 ranked origin hypotheses using the provenance algorithm, each with a score, rationale and linked evidence. · M · Mid-1 · *AC:* on the stale-price fault, H1 = Order Lookup step in ≥ 95% of 20 runs.
- **FR-ATT-02** Hypothesis scores shall be computed from evidence weights and graph position, never from an LLM self-report. · M · Mid-1.
- **FR-ATT-03** Tracing shall terminate on cyclic lineage within a max-revisit bound (default 3). · M · Mid-1 · *AC:* the cyclic fixture terminates and returns hypotheses. Brought forward: the bound existed but was untested, and the structural fallback raised KeyError on a cyclic trace.
- **FR-ATT-04** The system shall optionally request an LLM "second opinion" hypothesis labelled `llm_opinion`/Unverified. · S · Final-1 (M at Mid-2).

**Verify**
- **FR-VER-01** The system shall run a verification experiment under protocol VR-1: freeze upstream, apply one atomic intervention, re-execute downstream N times, plus M control replays. · M · Mid-1.
- **FR-VER-02** The system shall compute the verdict with the VR-1 rule and a Wilson 95% CI, and store the rule version. · M · Mid-1 · *AC:* the table-driven unit test over 20 (k, N, c, M) combinations matches the expected verdicts.
- **FR-VER-03** A replay that introduces a new failing check shall count as not-passing (regression guard). · M · Mid-1.
- **FR-VER-04** Verification shall be refused (HTTP 409 + UI message) for non-replayable runs. · M · Final-1.
- **FR-VER-05** Partial experiments (provider failure) shall keep completed replays, set verdict ERROR and allow resume. · M · Final-1 (Mid-1: verdict ERROR + retry).

**Review / Resolve**
- **FR-REV-01** Reviewers shall accept, reject or request info, with comments (mandatory for reject and for accepting an inconclusive finding). Each decision is stored with reviewer and timestamp. · M · Mid-1.
- **FR-REV-02** Finding state transitions shall follow §13.3. Illegal transitions are rejected and every transition is written to `audit_log`. · M · Mid-1.
- **FR-FIX-01** The system shall suggest a fix via the LLM Repair Agent as one atomic field value or one prompt patch, then verify it as a `fix` experiment before it is labelled "verified fix". · M · Final-1.
- **FR-FIX-02** On a CONFIRMED fix experiment, the system shall promote a passing replay to a **recovered run** linked to the original. · M · Final-1.
- **FR-FIX-03** The system shall store verified fixes with a finding signature (check ID + origin step key + field) and suggest them for new findings with the same signature. · S · Mid-2.

**Report / History**
- **FR-REP-01** The system shall export a finding report in Markdown and JSON (PDF at Final-1) containing the elements in §14.2-F7 and evidence hashes. · S Mid-1 / M Final-1.
- **FR-REP-02** The system shall export a regression case (JSON + pytest) for resolved findings, runnable in recorded mode in CI. · M · Final-1.
- **FR-HIS-01** The system shall list runs and findings with filters (status, severity, verification level, project, date) and text search, paginated (25/page). · M · Mid-1 (basic).

**Fault Lab / Evaluation**
- **FR-LAB-01** The system shall batch-generate labelled runs over {workflow × runtime × fault type} with a configurable clean-control share (default 20%) and a seed. · M · Final-1.
- **FR-EVA-01** The system shall compute detection recall, false-alarm rate, top-1/top-3 origin accuracy, verdict precision and recovery rate with bootstrap 95% CIs, and baselines (last-agent; LLM-judge all-at-once) on the same runs. · M · Final-1 v0 / Mid-2 v1.

**Platform**
- **FR-SEC-01** PII (e-mail, phone, CNIC `\d{5}-\d{7}-\d`, card-like numbers) shall be redacted before persistence in step inputs/outputs. · S Mid-1 / M Final-1.
- **FR-AUTH-01** Users shall sign in with GitHub OAuth, and reviews shall record the authenticated identity. · S · Mid-2.
- **FR-ADM-01** An administrator shall delete a run and all its derived records, and configure a retention period. · S · Mid-2.

---

## 16. Non-Functional Requirements

| ID | Quality | Requirement (measurable) | How measured | Milestone |
|---|---|---|---|---|
| NFR-01 | Performance (analysis) | Checks + attribution for a run ≤ 50 steps completes in **p95 ≤ 2 s** on the deployed instance | `analysis_ms` timer per run; report p50/p95 over the benchmark | Mid-1 measured, Final-1 met |
| NFR-02 | Performance (verification) | VR-1 with N=5, M=2 on Refund Desk completes **≤ 3 min** with the hosted free LLM; local 3B is reported, not targeted | Experiment duration field | Final-1 |
| NFR-03 | UI responsiveness | First contentful paint ≤ 3 s on a cold-loaded page (after server wake); interactions ≤ 200 ms | Lighthouse in CI on staging | Final-1 |
| NFR-04 | Reliability | No unhandled exception reaches the user. All 6 named failure modes (LLM down, LLM timeout, malformed import, check ERROR, DB unavailable, replay partial) produce a documented state. | System test suite SYS-ERR-* | Mid-1 (3), Final-1 (6) |
| NFR-05 | Correctness / determinism | Deterministic components (checks, provenance, verdict) give byte-identical output on re-evaluation and **across LLM providers** (replacement test) | Golden-file tests; provider swap test | Mid-1 |
| NFR-06 | Accuracy (evaluation) | False-alarm rate ≤ 5% on clean controls; detection recall ≥ 90% within coverage; verdict precision ≥ 85% | Evaluation module | Final-1 v0, Mid-2 v1 |
| NFR-07 | Security | 0 high/critical findings from Bandit, pip-audit, npm audit, gitleaks on `main`. DSL rejects 100% of the malicious test set. Upload limits enforced. | CI security job | Mid-1 |
| NFR-08 | Privacy | 0 unredacted seeded PII patterns in the DB after a run (scan test). Public demo contains synthetic data only. | Redaction scan test | Final-1 |
| NFR-09 | Usability | SUS ≥ 68 (n ≥ 5). Core-journey task success ≥ 80% without help. Median install-to-first-finding < 30 min (SDK path). | UAT protocol | Final-1 (pilot n=3), Final-2 |
| NFR-10 | Accessibility | WCAG 2.2 AA: contrast ≥ 4.5:1, full keyboard path for the core journey, status never by colour alone, `aria-live` progress | axe-core in Playwright; manual keyboard test | Final-1 |
| NFR-11 | Maintainability | `granite_core` coverage ≥ 80% lines (≥ 70% overall backend). Ruff clean. mypy strict on core. Cyclomatic complexity ≤ 10 per function (Ruff C901). | CI gates | Mid-1: reported (≥ 70% core is a gate only in Track T2, §30.6); Final-1: gated |
| NFR-12 | Portability / deployability | `docker compose up` on a clean machine reaches a working UI in ≤ 15 min following the setup manual. Verified by someone outside the module owner (then outside the team, by Final-2). | Install test record | Final-1 / Final-2 |
| NFR-13 | Availability (demo) | Staging/production health checks green at evaluation time. Warm-up done 10 min before demos (free tier sleeps). | Uptime log in Actions | Each gate |
| NFR-14 | Cost | $0 recurring. Every service on free tiers or local. | Cost table in deployment record | Always |
| NFR-15 | Scalability (stated scope) | Handles a 500-run benchmark and 10k steps in DB without schema change. No concurrency target beyond a 3-user team. | Benchmark load test | Mid-2 |

---

## 17. Complete UI/UX Architecture

### 17.1 Information architecture

```
Granite
├── Home (needs-attention dashboard)
├── Runs
│   ├── New run (launcher)               ← primary action, also top bar
│   ├── Import trace (wizard)            [Final-1]
│   └── Run detail  ─ tabs: Overview · Steps & graph · Checks · Findings
│        └── Step inspector (drawer)
├── Findings (inbox)
│   └── Finding detail  ─ investigation stepper:
│        Symptom → Evidence → Root cause → Verification → Decision → Resolution
│        └── Verification experiment (dialog + results)
├── Projects
│   └── Project detail ─ tabs: Workflow · Checks [editor at Final-1] · Settings
├── Fault Lab            [Final-1]
├── Evaluation           [Final-1 v0]
├── Settings (LLM provider, replay defaults, profile, API keys [Mid-2])
└── Help (How Granite works · Glossary · Input formats · Status/verdict legend)
```

**Global layout:** left sidebar (the sections above, icon + label); top bar (project switcher, **New run** primary button, **Import** button, LLM-mode indicator, environment badge `staging`/`demo`); main content. Breadcrumbs on detail pages.

### 17.2 Primary user journeys

| Journey | Steps (screens) | Success measure |
|---|---|---|
| J1 Investigate a silent failure (core, Mid-1) | Home → New run (S4) → Run detail (S6) → Finding (S9) → Verify (S10) → Review (S9) → Export (S12) | Completed by a first-time user in ≤ 8 min without help |
| J2 Confirm no false alarm | New run without fault → Run detail shows "All checks passed · no findings" | Clear passed state |
| J3 Investigate an imported trace (Final-1) | Import (S11) → validation report → Run detail → Finding → V1 evidence → Review | Clear explanation of why replay is unavailable |
| J4 Prove a fix (Final-1) | Finding (Accepted) → Suggest fix → Verify fix → Recovered run → Regression export | Recovered run linked; regression file downloaded |
| J5 Build a benchmark (Final-1) | Fault Lab (S13) → configure batch → progress → Evaluation (S14) | Metrics with CIs displayed |
| J6 Instrument own workflow (Final-1/Mid-2) | Help → SDK quickstart → code → run → Runs list shows `source=sdk` | Time-to-first-finding < 30 min |

### 17.3 State design rules (every data view)

| State | Rule | Example copy |
|---|---|---|
| Empty | Explain what the area is for and give the one action that fills it | "No findings yet. Findings appear when a check fails on a run. **Start a run**" |
| Loading | Skeletons ≥ 300 ms. Long jobs show a step-wise progress list with `aria-live`. | "Replaying 3 of 7…" |
| Partial | Show what is complete and mark the rest | "4 of 5 replays finished; provider timed out" |
| Error | Plain cause, consequence and action. Never a stack trace. | "The LLM provider did not respond in 30 s. Your run is saved as *errored*. **Retry** or switch to **Recorded mode**." |
| Success | Confirm the outcome and suggest the next step | "Verdict: CONFIRMED (5/5, controls 0/2). **Review finding →**" |
| Unavailable | Explain why a capability is disabled for this input | "Replay unavailable: imported traces have no runnable workflow. V1 evidence checks were run instead." |

### 17.4 Visual and interaction design

- **Design tokens:** reuse the `poc-console` palette and type, but **ship a light theme by default** (projectors) plus dark. Status colours are always paired with an icon and text (✓ PASS, ✕ FAIL, ○ ABSTAIN, ! ERROR). Verdict chips: CONFIRMED (green, check icon), REFUTED (grey, strike icon), INCONCLUSIVE (amber, question icon).
- **Investigation stepper** on Finding detail: 6 numbered stages with completion ticks. This is the panel's "workflow" made visible.
- **Graph view:** React Flow DAG (left to right). Symptom node outlined red; origin hypothesis dashed amber; confirmed origin solid. **Accessible alternative:** the Steps table carries identical information.
- **Microcopy:** plain verbs (Run, Check, Trace back, Verify, Review). Technical terms get an inline "?" tooltip linking to the glossary.
- **Forms:** inline validation, defaults pre-filled, "Load example" button on every input form (evaluators can complete J1 in one minute).

### 17.5 Accessibility and usability commitments

WCAG 2.2 AA:
- keyboard-only completion of J1
- visible focus
- skip-to-content link
- label for every input
- `aria-live` for job progress
- no colour-only meaning
- `prefers-reduced-motion` respected
- tables have headers
- minimum touch target 24×24 px

Tested with axe-core in Playwright, plus one manual keyboard pass per milestone.

**Usability evaluation:**
- Final-1: 3 peers × J1/J2 (think-aloud, SUS)
- Final-2: 5–8 UAT participants × J1/J3/J4/J6

---

## 18. Screen-by-Screen Specification

(The wireframes for Report v1.0 are drawn from this table. Screens marked ★ are in the Mid-1 slice.)

| ID | Screen | Purpose | User | Entry point | Inputs | Actions | Outputs / data displayed | Backend | Success state | Failure state |
|---|---|---|---|---|---|---|---|---|---|---|
| S0 ★ | **Home** | What needs attention now | Dev, Reviewer | App root | — | New run; open finding; open run | Open findings by severity; findings awaiting review; recent runs (status, findings count, verdicts); quick links | `GET /findings?status=open,confirmed`, `GET /runs?limit=10` | Lists populated | Empty state with "Start a run" / API error banner + retry |
| S4 ★ | **New run** | Launch a workflow on realistic input | Dev | Top-bar button, Home, Project | Project; message; e-mail; order; fault; LLM mode; "Load example" | Run; reset | Live progress (5 steps with ticks) then redirect to S6 | `POST /projects/{id}/runs` → 202; poll `GET /jobs/{id}` | Run detail opens with analysis complete | Field errors inline; rate-limit message; provider-down banner with Recorded-mode switch |
| S6 ★ | **Run detail** | See what happened in a run | Dev, Reviewer | S0, S8, runs list | Tab selection | Re-run; run without fault; open step; open finding; export trace JSON | Header (status, duration, model, mode, fault badge visible to Fault-Lab/admin only); **Steps & graph**; **Checks** (PASS/FAIL/ABSTAIN with observed/expected); **Findings** | `GET /runs/{id}`, `/graph`, `/check-results`, `/findings` | Clear "All checks passed" or findings list | Errored run shows the failing step + error + retry |
| S7 ★ | **Step inspector** (drawer) | Inspect one step precisely | Dev | Click a step/node | — | Copy JSON; jump to upstream/downstream | Inputs/outputs (pretty JSON, redacted marks), prompt hash, model/params, timings, contract checks, lineage (reads) | `GET /runs/{id}/steps/{sid}` | Drawer renders | "Step data unavailable" message |
| S8 ★ | **Findings inbox** | Triage all cases | Dev, Reviewer | Sidebar | Filters (status, severity, level, project), search | Open; bulk export (Final-1) | Table: ID, title, severity, verification level V0–V3, verdict, status, run, age | `GET /findings?...` (paginated) | Filtered list | Empty filter result explains which filter removed items |
| S9 ★ | **Finding detail** | Investigate one failure end to end | Dev, Reviewer | S8, S6, S0 | Stepper navigation; review form | Verify H*; add hypothesis; review; export; (Final-1) suggest fix, apply fix, export regression | 1 Symptom (failed check, expected vs observed, "no error raised" flag); 2 Evidence (computations, truth queries, hashes); 3 Root cause (ranked hypotheses, provenance path highlighted on a mini graph); 4 Verification (experiments + verdicts); 5 Decision (reviews); 6 Resolution (fix, recovered run, regression case) | `GET /findings/{id}` (+ hypotheses, experiments, evidence, reviews) | All sections filled; next action highlighted | Section-level errors without breaking the page |
| S10 ★ | **Verify dialog + results** | Run and read a verification experiment | Dev | S9 "Verify" | Intervention (pre-filled), N, M, mode | Start; cancel; increase N; verify next | Plan preview (frozen steps greyed, intervention step highlighted, replayed steps listed); progress; results table per replay (pass/fail per check); controls; k/N, c/M, CI; verdict with plain-language explanation; diff viewer | `POST /hypotheses/{id}/experiments`; `GET /experiments/{id}` | Verdict + "what this means" sentence | 409 replay unavailable; partial ERROR with resume; validation errors on N/M |
| S2 | **Project detail** | Understand the workflow and its rules | Dev | Projects | — (Final-1: edits) | View workflow diagram; open checks | Agents/steps with reads/writes; checks list (type, scope, severity, enabled); settings | `GET /projects/{id}`, `/checks` | Rendered | Missing project → 404 page |
| S3 | **Check editor** (Final-1) | Create/edit checks safely | Dev | S2 | Name, type, scope, step, expression (with field autocomplete), tolerance, severity | Validate; dry-run on a chosen run; save (new version); disable | Parse result; dry-run result table | `POST /checks:validate`, `POST /checks`, `PUT /checks/{id}` | Saved v+1 | DSL error with position underline |
| S11 | **Import trace** (Final-1) | Bring external traces | Dev | Top bar | File; project; format (auto) | Upload; fix and retry | Validation report (errors with JSON path); preview of steps; import result | `POST /runs:import` | Redirect to S6 | Report lists errors; nothing persisted |
| S12 | **Report preview** | Produce a shareable record | Dev, Reviewer, Auditor | S9 Export | Format | Download MD/JSON/PDF; copy link | Rendered report | `GET /findings/{id}/report?format=` | File downloaded | Generation error with retry |
| S13 | **Fault Lab** (Final-1) | Generate labelled runs | Dev (research/QA) | Sidebar | Workflow(s), runtime(s), faults × count, clean %, seed, mode | Start batch; cancel | Batch progress; table of generated runs with ground truth (visible only here) | `POST /fault-lab/batches`, `GET /fault-lab/batches/{id}` | Batch complete | Partial batch report |
| S14 | **Evaluation** (Final-1 v0) | Show measured quality vs baselines | Supervisor, panel, team | Sidebar | Benchmark selection; methods | Run evaluation; download CSV | Metric cards with CIs; comparison table; ablation table; confusion of origin predictions | `POST /evaluations`, `GET /evaluations/{id}` | Metrics displayed | "Insufficient runs (n<30)" warning |
| S15 | **Settings** | Configure environment | Dev, Admin | Sidebar | Provider, model, base URL (env-backed), default N/M, reviewer name; (Mid-2) API keys, retention | Save; test provider connection | Current config (secrets masked) | `GET/PUT /settings`, `POST /settings:test-llm` | "Connection OK (model, latency)" | Connection failure details |
| S16 | **Help** | Make the workflow understandable to anyone | All | Sidebar, "?" tooltips | — | — | "How Granite works" (the §13 diagram + 3-audience table), glossary, input formats (schemas), verdict legend, SDK quickstart | static | — | — |

---

## 19. System Architecture

### 19.1 Style and rationale

A **modular monolith**:
- one deployable container: FastAPI serves the API and the built React app
- one PostgreSQL database
- an **in-process job runner** (DB-backed job table, FastAPI background workers)
- a **pure-Python core library** (`granite_core`) with no web dependencies

**Why:**
- 3 developers
- free hosting (one small instance)
- request/response plus a few long jobs (replays take ≤ 3 min)
- the core must be unit-testable and reusable by the SDK and the evaluation scripts

**Rejected alternatives** (recorded as ADRs):
- microservices: operational cost with no scaling need
- Celery/Redis queue: extra paid or managed service; the job table suffices at our scale
- Kubernetes
- a separate graph DB: graphs are small, so adjacency lists suffice
- running Ollama on the public host: the free tier lacks RAM

### 19.2 Layers

| Layer | Contents | Depends on |
|---|---|---|
| L1 Presentation | React SPA (`apps/web`) | L2 over HTTP only |
| L2 API | FastAPI routers, request/response schemas, auth, rate limiting, error mapping (`apps/api/routers`) | L3 |
| L3 Application services | Use-case orchestration: RunService, AnalysisService, VerificationService, ReviewService, ReportService, JobRunner (`apps/api/services`) | L4, L5 |
| L4 Domain core | `granite_core`: trace schema, graph and lineage, checks DSL and evaluator, attribution, replay planning, verdict rule, redaction, evidence hashing | Nothing outside the stdlib, pydantic and networkx |
| L5 Infrastructure | SQLAlchemy repositories, Alembic migrations, LLM provider adapters (Ollama, OpenAI-compatible, Recorded), workflow runner and adapters, source-of-truth data snapshot | External systems |

**Dependency rule:** inner layers never import outer layers. CI enforces it with `import-linter` contracts (free).

### 19.3 Component diagram

```mermaid
flowchart TB
  subgraph Browser
    UI["React SPA<br/>Runs, Findings, Verify, Review, Reports"]
  end
  subgraph Container["Granite container"]
    API["FastAPI REST /api/v1<br/>validation, errors, rate limit"]
    SVC["Application services<br/>Run, Analysis, Verification, Review, Report"]
    JOBS["Job runner<br/>DB-backed queue"]
    subgraph Core["granite_core library"]
      SCHEMA["Trace schema v1"]
      GRAPH["Graph + lineage"]
      CHECKS["Checks DSL evaluator"]
      ATTR["Provenance attribution"]
      VER["Replay planner + verdict rule"]
      RED["PII redaction + evidence hashing"]
    end
    RUNNER["Workflow runner<br/>Refund Desk, Math Crew<br/>adapters: LangGraph, CrewAI"]
    LLMP["LLM provider layer<br/>Ollama, OpenAI-compatible, Recorded"]
    TRUTH["Source-of-truth snapshot<br/>tau-bench retail subset"]
  end
  DB[("PostgreSQL")]
  LLM["LLM endpoint"]
  SDK["Granite SDK in a user workflow"]
  UI --> API --> SVC
  SVC --> JOBS
  SVC --> Core
  JOBS --> RUNNER
  VER --> RUNNER
  CHECKS --> TRUTH
  RUNNER --> TRUTH
  RUNNER --> LLMP --> LLM
  SVC --> DB
  JOBS --> DB
  SDK -.->|"Final-1 onward"| API
```

### 19.4 Key interfaces (contracts between owners)

| Interface | Producer → consumer | Contract |
|---|---|---|
| `TraceV1` (pydantic) | Runner / Import / SDK → Core | §22.4 schema; versioned `schema_version` |
| `Runner.execute(plan, overrides) -> TraceV1` | Shahoud → Saif (replay) | Runs a workflow from a `ReplayPlan`: frozen step outputs + intervention + pinned params |
| `evaluate_checks(trace, checks, truth) -> list[CheckResult]` | Noor → services | Pure function; deterministic |
| `attribute(trace, finding, check_results) -> list[Hypothesis]` | Noor → services | Pure function; deterministic |
| `plan_replay(trace, hypothesis, intervention) -> ReplayPlan` / `decide(results, rule="VR-1") -> Verdict` | Saif → services | Pure functions |
| `LLMProvider.complete(messages, params) -> Completion` | Shahoud → runner | Supports `seed`, `temperature`, `json_schema`; returns tokens and latency |

### 19.5 Key interaction: verify a hypothesis (sequence)

```mermaid
sequenceDiagram
  actor Dev as Developer
  participant UI as Web UI
  participant API as API
  participant J as Job runner
  participant V as Verification core
  participant R as Workflow runner
  participant L as LLM provider
  participant DB as Database
  Dev->>UI: Verify H1 (N=5, controls=2)
  UI->>API: POST /hypotheses/H1/experiments
  API->>DB: insert experiment (queued)
  API-->>UI: 202 + experiment id
  API->>J: enqueue experiment
  loop N intervention replays + M control replays
    J->>V: plan replay (freeze upstream, patch origin or not)
    V->>R: re-execute downstream steps
    R->>L: LLM calls with pinned params
    L-->>R: outputs
    R-->>V: replay trace
    V->>V: re-evaluate all checks (regression guard)
    V->>DB: store replay run + REPLAY_OUTPUT / DIFF evidence
  end
  V->>V: verdict = VR-1(k/N, c/M), Wilson CI
  V->>DB: update experiment, hypothesis, finding status, audit log
  UI->>API: GET /experiments/{id} (polling)
  API-->>UI: verdict + evidence
```

---

## 20. Technology Stack

| Concern | Choice | Why | Alternatives rejected |
|---|---|---|---|
| Language (backend/core) | Python 3.11 | Team skill; LLM/agent ecosystem; existing spikes | — |
| API | FastAPI + Pydantic v2 | Typed contracts → automatic OpenAPI (answers "what inputs") | Django (heavier), Flask (no typing) |
| ORM / migrations | SQLAlchemy 2.0 + Alembic | Mature; migrations give schema evolution evidence | Raw SQL |
| DB | PostgreSQL 16 (Neon free; local Docker); SQLite only for unit tests | JSONB for payloads; free managed option | MongoDB (relational links matter), Render Postgres free (expires after 30 days) |
| Graph | networkx (already in Spike 6) | Topological sort, BFS, betweenness | Graph DB |
| Check DSL | Python `ast` with a node whitelist (own code, ~150 lines) | Security plus ownership. It is CCP-relevant code we can defend. | `eval` (unsafe); `simpleeval` (acceptable fallback, MIT) |
| Agent frameworks | Own lightweight runner (Mid-1); LangGraph (Final-1); CrewAI (Mid-2) | Runner gives deterministic replay control quickly. Frameworks prove generality. | Starting with CrewAI (harder replay hooks) |
| LLM | Provider abstraction: **Ollama** (local/self-host: `llama3.2:3b`, `qwen2.5:3b`; 7–8B if hardware allows), **OpenAI-compatible free hosted tier** (Groq or Gemini; public demo), **Recorded** (CI/offline) | $0; privacy option; deterministic tests | Paid APIs (violates $0 decision R37) |
| Frontend | React 18 + TypeScript + Vite (existing); React Router; TanStack Query (polling and cache); **React Flow** (graph, MIT) | Reuses the PoC stack and team skill | Next.js (SSR unnecessary) |
| UI styling | Existing CSS tokens + a small component set; Radix primitives where accessibility is hard (dialog, tabs) | Accessible primitives, low weight | Heavy UI kits |
| Tests | pytest, pytest-cov, hypothesis (property tests for the DSL); Vitest + Testing Library; Playwright + axe-core | Standard, free | — |
| Static analysis | Ruff (lint, format, complexity), mypy (strict on core), Bandit, pip-audit, ESLint, `tsc --noEmit`, npm audit, gitleaks, import-linter | Free; CI-enforced | SonarCloud/CodeQL only if the repo goes public (D2) |
| Packaging | Docker (multi-stage), Docker Compose | Reproducible; handbook "runs outside dev machine" | — |
| CI/CD | GitHub Actions; Render deploy hooks; GHCR for release images | Required by faculty; free | Jenkins (self-host burden) |
| Hosting | Render free web services (staging, production) + Neon Postgres free (branches: `main`, `staging`) | $0. HF Docker Spaces now require a paid plan (checked 2026-10-04). | HF Spaces, Fly.io, Railway (not free) |
| Docs | **Reports: the prescribed LaTeX template** (`fast-nuces-bs.cls`) kept in `docs/report/`, built with pdflatex + bibtex (MiKTeX/TeX Live; optional CI build). Internal docs (registers, ADRs, manuals) in Markdown. Diagrams as code (Mermaid/PlantUML) + draw.io, exported to PDF/PNG for LaTeX. TikZ-UML ships with the template but is optional. | The rubric grades "prescribed template followed". Versioned sources give per-member commit evidence. | Markdown → pandoc → Word (v1.0's choice; withdrawn because it conflicts with the prescribed template) |
| Design | Penpot (OSS) or Figma Education (free) for wireframes | Free | — |

---

## 21. AI/ML/Agent Architecture

### 21.1 Where AI is used, and where it deliberately is not

| Component | Uses an LLM? | Role | Handbook C.14 class |
|---|---|---|---|
| Demo workflow agents (Intake, Policy, Calculator, Writer) | Yes | **System under test.** Failures are the subject matter. | Support (test fixture) |
| Checks engine, provenance attribution, verdict rule, redaction, evidence | **No** | The contribution | Own work |
| Replay of downstream LLM steps | Yes (re-execution) | The protocol is ours; the LLM is the fixture being re-run | Core-assist (fixture) |
| Fix suggestion (Repair Agent) | Yes | Proposes a candidate. **Never trusted until verified.** | Core-assist |
| Second-opinion hypothesis (ErrorProbe-lite) | Yes | Optional; labelled unverified; also an evaluation baseline | Core-assist |
| LLM-judge baseline (Who&When all-at-once) | Yes | Evaluation comparator only | Support (baseline) |

**Replacement test:** if the LLM provider is swapped, every deterministic component produces byte-identical output on the same trace (NFR-05). This is the answer to "is this just an AI wrapper?". The LLM is the *patient*, not the *doctor*.

### 21.2 LLM provider layer

- **Interface:** `complete(messages, *, model, temperature, max_tokens, seed=None, json_schema=None) -> Completion(text, parsed, tokens_in, tokens_out, latency_ms, provider, model)`.
- **Implementations:** `OllamaProvider`, `OpenAICompatibleProvider` (Groq/Gemini/any), `RecordedProvider`.
- **RecordedProvider:** keyed by `sha256(provider|model|params|messages|replay_index)`. Stored in `tests/cassettes/` and the DB. It powers CI, offline demos and exact reproducibility.
- **Timeouts and retries:** 30 s per call; 1 retry with backoff on 429/5xx; then a typed `ProviderUnavailable` error mapped to the run's `errored` state.
- **Determinism controls:** temperature recorded per step (default 0.2 for agents); seed passed where supported; prompts versioned (`prompts/<agent>/<version>.md`); prompt hash stored per step.
- **Structured outputs:** JSON-schema-constrained responses for Intake/Policy/Calculator. Validation failure counts as a step-level `schema` check FAIL (itself a detectable failure class), not a crash.

### 21.3 Demo workflows (systems under test)

**Refund Desk (Mid-1).** Built on the tau-bench retail data snapshot and policy (MIT licence, attributed).

| Step | Agent | Kind | Reads | Writes (structured) |
|---|---|---|---|---|
| s1 | Intake | llm | task.message, task.email | `order_id`, `item_ids[]`, `reason` |
| s2 | Order Lookup | tool | s1.order_id, s1.item_ids | `user_id`, `status`, `items[{item_id, price}]`, `payment_method` |
| s3 | Policy | llm | s2.*, s1.item_ids | `eligible`, `items_to_refund[]`, `refund_method` |
| s4 | Refund Calculator | llm | s3.items_to_refund, s2.items | `prices_used[]`, `refund_amount` |
| s5 | Writer | llm | s4.refund_amount, s3.refund_method | `message` (text) |

**Faults:**
- **FLT-STALE:** s2 returns one price shifted by a plausible delta (e.g. −0.25). Mid-1.
- **FLT-HANDOFF:** s1→s3 item-id swap. Final-1.
- **FLT-DROP:** Policy prompt loses the ownership rule. Final-1.

**Natural failures:** small-model arithmetic slips at s4, and amount mismatches at s5.

**Math Crew (Final-1).** GSM8K: Planner → Solver (shows equation steps as structured `operations[]`) → Checker → Answerer.
- **Checks:** recompute each operation (`assert`); final answer = last operation result.
- **`answer_key`** only in Fault Lab/evaluation, never as a production check.

### 21.4 Algorithm: value-provenance attribution (deterministic; owner Noor)

```
Input : run R (steps S, lineage edges E with field labels), failed outcome check c
        contract results C[s], truth results T[s] (may be empty)
Output: ranked hypotheses H

1  F  ← fields referenced by c; symptom ← step owning the asserted field
2  Q  ← queue[(symptom, F)] ; visited ← {} ; cand ← []
3  while Q not empty:
4     (s, fields) ← pop(Q); if visits[s] > MAX_REVISIT: continue      # cycle bound (Spike 6)
5     e ← evidence(s):
6          truth_mismatch  if T[s] has FAIL on any f in fields        (weight 1.0)
7          contract_fail   if C[s] has FAIL                            (weight 0.8)
8          handoff_drift   if s.inputs[f] ≠ upstream.outputs[f] for some f (weight 0.7)
9          consistent      if C[s] PASS (propagated faithfully)        (weight 0)
10         unknown         if no contract / truth defined              (weight 0.2)
11    if e ≠ consistent: cand.append((s, e))
12    for each upstream u with edge (u → s) carrying any f in fields:
13         push(Q, (u, fields_carried(u → s)))
14 origin candidates ← cand sorted by (weight desc, topological index asc)
15 score(h) ← weight(e) × decay^(distance(h, symptom)) normalised to [0,1]
16 if no candidate has weight ≥ 0.7: label all "structural only — needs verification",
        rank by betweenness centrality on the contributing subgraph
17 return top-5 with PROVENANCE_PATH evidence
```

**Complexity:** O((V + E)·k), where k ≤ MAX_REVISIT. Runs are ≤ 500 steps, so it takes milliseconds.

**Handoff drift for free text:** numbers and entities are extracted with regex; if nothing can be extracted, the result is `unknown`.

**Evaluated against:**
- (a) **last-agent**: blame the symptom step
- (b) **LLM-judge all-at-once** (Who&When method) on the same model
- (c) **ErrorProbe-lite** (Mid-2)

### 21.5 Algorithm: verdict rule VR-1 (owner Saif)

```
decide(k, N, c, M):
   if completed_replays < N: return ERROR
   p ← k/N ; q ← c/M if M>0 else 0
   if p ≥ 0.8 and q ≤ 0.2: return CONFIRMED
   if p ≤ 0.2:             return REFUTED
   return INCONCLUSIVE
wilson(k, N, z=1.96) → (low, high)   # reported, not used for the decision at N=5
```

Thresholds are versioned (`VR-1`). Any change creates `VR-2`. The old verdicts keep their rule version.

### 21.6 Guarding and evaluating the LLM parts

| Concern | Guard / test |
|---|---|
| Repair suggestion names a derived value instead of the parameter (Spike 8 failure) | The schema requires `{target_step, field_path, new_value}`; `field_path` must exist in the step outputs; the suggestion is verified before trust |
| Hallucinated hypothesis | LLM opinions are labelled and must go through V1/V2 like any other hypothesis |
| Prompt drift breaks demos | Prompt files versioned; recorded cassettes per version; nightly regression in recorded mode |
| Small-model unreliability | Measured, not hidden: natural failure rate per agent reported in evaluation |
| Metamorphic tests | Renaming agents, inserting an irrelevant step, or scaling all prices by 10 must not change the identified origin (deterministic core) |

---

## 22. Database & Data Architecture

### 22.1 ER diagram (core; Mid-1 entities in bold in the dictionary)

```mermaid
erDiagram
  PROJECT ||--o{ WORKFLOW_VERSION : has
  PROJECT ||--o{ CHECK : defines
  PROJECT ||--o{ RUN : owns
  WORKFLOW_VERSION ||--o{ RUN : executes
  RUN ||--o{ STEP : contains
  RUN ||--o{ STEP_EDGE : contains
  RUN ||--o{ CHECK_RESULT : produces
  CHECK ||--o{ CHECK_RESULT : "evaluated as"
  RUN ||--o| FAULT_INJECTION : "labelled by"
  CHECK_RESULT ||--o| FINDING : raises
  FINDING ||--o{ HYPOTHESIS : explains
  HYPOTHESIS ||--o{ EXPERIMENT : "tested by"
  EXPERIMENT ||--o{ RUN : "replays as"
  FINDING ||--o{ EVIDENCE : supports
  FINDING ||--o{ REVIEW : "decided by"
  FINDING ||--o{ FIX : "resolved by"
  FINDING ||--o{ REPORT : "exported as"
  RUN {
    uuid id PK
    uuid project_id FK
    string source
    uuid parent_run_id
    uuid experiment_id
    string status
    jsonb task_input
    jsonb final_output
    string llm_provider
    string llm_model
  }
  FINDING {
    uuid id PK
    uuid run_id FK
    string kind
    string severity
    string status
    string verification_level
    string signature_hash
  }
  EXPERIMENT {
    uuid id PK
    uuid hypothesis_id FK
    string kind
    jsonb intervention
    int n_replays
    int n_controls
    int k_pass
    int c_pass
    string verdict
    string rule_version
  }
  EVIDENCE {
    uuid id PK
    uuid finding_id FK
    string type
    jsonb payload
    string sha256
    string reproduce
  }
```

### 22.2 Data dictionary (abridged; the full version goes in Report §6.x)

| Entity | Key attributes (type) | Notes |
|---|---|---|
| **project** | id (uuid), name, slug (unique), workflow_key, settings (jsonb: default N, M, provider) | Seeded: `refund-desk` |
| workflow_version | id, project_id, version (int), definition (jsonb: steps, reads, writes, contracts), code_ref (git sha) | Mid-1: one version, seeded |
| **check** | id, project_id, key, name, type ∈ {assert, truth, policy, schema, answer_key}, scope ∈ {outcome, step}, step_key, expression (text), tolerance (numeric), severity ∈ {critical, high, medium, low}, enabled (bool), version (int) | (key, version) unique; old versions immutable |
| **run** | id, project_id, workflow_version_id, source ∈ {live, recorded, import, sdk, replay, fault_lab}, parent_run_id, experiment_id, status ∈ {queued, running, completed, errored, analyzed}, task_input, final_output, llm_provider, llm_model, llm_params (jsonb), started_at, ended_at, analysis_ms | Index (project_id, created_at), (status) |
| **step** | id, run_id, step_key, ordinal, agent, kind ∈ {llm, tool, code, handoff}, inputs (jsonb, redacted), outputs (jsonb, redacted), reads (text[]), prompt_hash, error (text), started_at, ended_at, frozen (bool), replayed (bool) | (run_id, step_key) unique |
| **step_edge** | id, run_id, from_step_id, to_step_id, field | Lineage |
| **check_result** | id, run_id, check_id, check_version, status ∈ {pass, fail, abstain, error}, observed (jsonb), expected (jsonb), message | Index (run_id) |
| **fault_injection** | id, run_id, fault_type, target_step_key, field_path, original_value, injected_value | **Hidden from attribution** (service-level access rule + test) |
| **finding** | id, run_id, check_result_id, title, kind ∈ {silent_failure, explicit_error, policy_violation}, severity, symptom_step_id, status (§13.3), verification_level ∈ {V0..V3}, signature_hash | Index (status, severity) |
| **hypothesis** | id, finding_id, origin_step_id, origin_agent, rank, method ∈ {provenance, structural, llm_opinion, manual}, score (0–1), rationale, state ∈ {open, confirmed, refuted, inconclusive} | — |
| **experiment** | id, hypothesis_id, kind ∈ {causal, fix}, intervention (jsonb), n_replays, n_controls, k_pass, c_pass, ci_low, ci_high, verdict, rule_version, status, llm_calls, tokens, duration_ms | — |
| **evidence** | id, finding_id, hypothesis_id?, experiment_id?, type (§14.5), payload (jsonb), sha256, reproduce, created_by, created_at | Append-only (no UPDATE grant in app role) |
| **review** | id, finding_id, reviewer, decision ∈ {accept, reject, needs_info}, comment, created_at | — |
| fix | id, finding_id, intervention, source ∈ {truth, user, llm}, experiment_id, status | Final-1 |
| known_fix | id, signature_hash, fix_template, verified_count, last_verified_at | Mid-2 |
| report | id, finding_id, format, sha256, content (bytea/text), created_at | Final-1 |
| **job** | id, type, status, progress (0–100), error, payload, created_at, updated_at | Polling target |
| **audit_log** | id, entity, entity_id, action, from_state, to_state, actor, at | Every state transition |

### 22.3 Data management

- **Seed data:** a tau-bench retail subset of about 50 users, 100 orders and 200 products, as a versioned JSON snapshot `truth_snapshot_v1` (licence file included). Truth queries record the snapshot version.
- **Migrations:** Alembic, one migration per PR that changes the schema. Expand/contract for backward compatibility.
- **Redaction:** before insert, applied to step inputs/outputs: e-mail, phone, CNIC, 13–19-digit card numbers. Tokens look like `«EMAIL_1»`. The mapping is not stored.
- **Retention:** default 90 days for runs on the public demo (FYP-2 job). Evidence of findings in reports is kept until the report is deleted.
- **Backups:** nightly `pg_dump` of production via Actions (7-day artefact retention).

### 22.4 Granite Trace v1 (input contract for import and SDK)

```json
{
  "schema_version": "granite.trace/v1",
  "run": {
    "external_id": "W-2041", "workflow": "refund_desk", "runtime": "langgraph",
    "status": "completed",
    "task_input": {"message": "Please return the lamp and the mug from order #W2041"},
    "final_output": {"message": "Your refund of $43.25 will go to your card."},
    "started_at": "2026-10-05T10:00:00Z", "ended_at": "2026-10-05T10:00:09Z"
  },
  "steps": [
    {"step_id": "s2", "agent": "OrderLookup", "kind": "tool", "name": "get_order_details",
     "inputs": {"order_id": "#W2041"},
     "outputs": {"status": "delivered", "items": [{"item_id": "1001", "price": 19.50}]},
     "reads": ["s1.order_id"], "started_at": "…", "ended_at": "…", "error": null,
     "model": null, "params": null}
  ]
}
```

**Validation rules:**
- unique `step_id`
- every `reads` entry references an earlier `step_id.field`
- timestamps ISO-8601
- `kind` ∈ enum
- size ≤ 5 MB
- ≤ 500 steps

---

## 23. API Architecture

**Conventions:**
- REST under `/api/v1`, JSON only.
- Errors use **RFC 7807** `application/problem+json` (`type, title, status, detail, errors[]` with JSON paths).
- Long operations return **202 + job/experiment ID** and are polled every 1–2 s.
- Pagination: `?page=&page_size=` (≤ 100).
- OpenAPI at `/docs` is the input contract the panel asked for.
- Rate limit on run/experiment creation in the public demo.

| Method | Path | Purpose | Request → Response | Milestone |
|---|---|---|---|---|
| GET | `/health` | Liveness + version | → `{status, version, git_sha, db, llm}` | Mid-1 |
| GET | `/projects`, `/projects/{id}` | Projects + workflow definition | → list / detail | Mid-1 |
| GET | `/projects/{id}/checks` | Checks | → list | Mid-1 |
| POST | `/checks:validate` | Parse + dry-run expression | `{expression, run_id?}` → `{ok, errors[], result?}` | Final-1 |
| POST/PUT/DELETE | `/projects/{id}/checks`, `/checks/{id}` | Manage checks (versioned) | check body → check | Final-1 |
| POST | `/projects/{id}/runs` | Launch run | `{inputs, fault?, llm_mode}` → 202 `{run_id, job_id}` | Mid-1 |
| POST | `/runs:import` | Import trace file (multipart) | file + project_id → 201 run / 422 validation report | Final-1 |
| POST | `/ingest/traces` | SDK ingestion (API key) | TraceV1 → 202 | Final-1 |
| GET | `/runs`, `/runs/{id}` | History + detail | filters → page / run | Mid-1 |
| GET | `/runs/{id}/graph`, `/runs/{id}/steps/{step_key}`, `/runs/{id}/check-results` | Trace views | → graph / step / results | Mid-1 |
| POST | `/runs/{id}:analyze` | Re-run analysis (after a check change) | → 202 | Final-1 |
| GET | `/findings`, `/findings/{id}` | Inbox + detail (with hypotheses, experiments, evidence, reviews) | → page / finding | Mid-1 |
| POST | `/findings/{id}/hypotheses` | Manual or LLM second opinion | `{origin_step_key, rationale}` or `{method:"llm_opinion"}` | Final-1 |
| POST | `/hypotheses/{id}/experiments` | Verify | `{kind, intervention, n_replays, n_controls}` → 202 experiment | Mid-1 |
| GET | `/experiments/{id}` | Status + verdict + replays | → experiment | Mid-1 |
| POST | `/findings/{id}/reviews` | Decision | `{decision, comment}` → review; 409 on illegal transition | Mid-1 |
| POST | `/findings/{id}/fix-suggestions` | Repair Agent | → suggestion (unverified) | Final-1 |
| POST | `/findings/{id}/recovered-run` | Promote passing replay | → run | Final-1 |
| GET | `/findings/{id}/report?format=md\|json\|pdf` | Report | → file | S Mid-1 / M Final-1 |
| GET | `/findings/{id}/regression-case` | Regression export | → zip (json + pytest) | Final-1 |
| GET | `/evidence/{id}` | Evidence + hash | → evidence | Mid-1 |
| GET | `/jobs/{id}` | Job progress | → job | Mid-1 |
| POST/GET | `/fault-lab/batches`, `/evaluations` | Research | → 202 / results | Final-1 |
| GET/PUT | `/settings`; POST `/settings:test-llm` | Configuration | — | Final-1 |

---

## 24. Security & Privacy

| Threat (STRIDE-lite) | Asset | Control | Test |
|---|---|---|---|
| Code injection via check expressions (E) | Server | AST whitelist evaluator; no `eval`/`exec`; recursion/size limits; 50 ms CPU timeout per check | 15 malicious expressions rejected (TC-CHK-SEC) |
| Malicious/oversized upload (D, T) | API | 5 MB limit; streaming parse; schema validation; ≤ 500 steps; JSON only | Fuzz/oversize tests |
| PII leakage from traces (I) | Users' customers | Redaction before persistence; synthetic data only on the public demo; minimum context sent to the LLM; self-host option | Redaction scan test |
| Secret leakage (I) | API keys | Secrets only in GitHub Environments / Render env; `.env` ignored; gitleaks in CI; masked in UI | gitleaks job |
| Abuse of the public demo / free-tier exhaustion (D) | LLM quota | IP rate limit; recorded mode default on the public demo; max N=10 | Rate-limit test |
| Tampering with evidence (T) | Findings | Append-only evidence; SHA-256 hashes in reports; audit log | Hash verification test |
| Spoofed reviewer (S) | Reviews | Mid-1: honest "unauthenticated demo" label. Mid-2: GitHub OAuth identity. | Auth tests (Mid-2) |
| Vulnerable dependencies | Supply chain | pip-audit, npm audit, Dependabot weekly; pinned versions | CI security job |
| CORS/CSRF | API | Same-origin deploy (SPA served by API); strict CORS allowlist for dev | Config test |

**Ethics and legal (carried from the proposal, updated):**
- fault injection only on our own workflows or consenting UAT participants' workflows
- UAT consent form (recording, data use, withdrawal)
- dataset licences recorded (tau-bench MIT, GSM8K MIT, Who&When — verify the licence file; GAIA not redistributed)
- LLM provider terms checked for the hosted demo (no personal data sent)
- findings are advisory, and a human decides (no autonomous changes to production)

---

## 25. Design-Phase Deliverables (Iteration 1 → evolved each iteration)

The handbook says "select the design appropriate for your project". Every diagram must match the code in the tagged release it ships with. Sources live in `docs/diagrams/` (Mermaid/PlantUML), so changes are visible in git (design-evolution evidence, Form 2/4).

| Artefact | Selected? | Why / what it shows | Owner | Mid-1 | Final-1 |
|---|---|---|---|---|---|
| Domain model / class diagram | **Yes** | Project, Run, Step, Check, Finding, Hypothesis, Experiment, Evidence, Review and their relations; `granite_core` classes | Noor | v1 | updated |
| Component diagram | **Yes** | §19.3 | Saif | v1 | updated |
| Layer diagram | **Yes** | §19.2 + import-linter contracts | Saif | v1 | updated |
| Structure chart | Light | Module call hierarchy of `granite_core` (analysis pipeline); useful for the procedural core only | Noor | — | v1 |
| Flow diagram (workflow) | **Yes** | §13.1 | Shahoud | v1 | updated |
| DFD L0 + L1 | **Yes** | External entities (Developer, Reviewer, LLM, Workflow); processes Ingest, Check, Attribute, Verify, Review, Report; stores Runs, Findings, Evidence | Shahoud | v1 | updated |
| Data dictionary | **Yes** | §22.2 | Saif | v1 | full |
| Activity diagram | **Yes** | Investigation workflow with decision nodes (verdict branches, trace-only path) | Shahoud | v1 | updated |
| State machine | **Yes** | Finding lifecycle (§13.3), Run lifecycle, Experiment lifecycle | Saif | v1 | updated |
| Sequence diagrams | **Yes** | (a) Launch + analyze run; (b) Verify hypothesis (§19.5); (c) Review + export | Noor (a), Saif (b), Shahoud (c) | a, b | + c, SDK ingest |
| Interaction overview | Yes (one) | Ties the three sequences into the end-to-end journey | Shahoud | — | v1 |
| Call graph | No | Sequence diagrams cover the behaviour. Avoids an auto-generated diagram without reasoning (Appendix B cap). | — | — | — |
| Network automata / graph | Covered | State machines + the execution-graph model | — | — | — |
| ER diagram + schema | **Yes** | §22.1 + Alembic-generated DDL | Saif | v1 | updated |
| Data structure & algorithm design | **Yes** | Provenance BFS (§21.4), verdict rule (§21.5), DSL evaluator (AST whitelist), replay planner | Noor, Saif | v1 | updated |
| Deployment diagram | **Yes** | §29.2 | Saif | v1 | updated |
| Package diagram | Yes (FYP-2 Final requirement) | Monorepo packages and dependencies | Saif | — | v1 (Final-2 required) |
| Wireframes + UI screens | **Yes** | §18. Wireframes (Penpot) plus **real screenshots** of implemented screens. | Shahoud (lead), each owner for their screens | S0–S10 | all |
| Use case diagram + SSDs | **Yes** | §15.1; SSDs for UC-03, UC-08, UC-09 | Shahoud | v1 | + UC-04, UC-15 |
| ADRs | **Yes** | ADR-001 modular monolith · 002 own runner first · 003 Postgres/Neon · 004 AST DSL · 005 provenance-first attribution · 006 VR-1 verdict rule · 007 Render free hosting · 008 LLM provider abstraction + recorded mode · 009 trace schema v1 · 010 Git branching | Each decision's owner | 001–010 | + new |


**Rubric alignment [M-R F2-5, F3-5, F3-6]:**
- **Match the code.** Diagrams must match the code at the tagged Mid-1 commit. Draw first drafts from this plan on D0–D1, then redraw or adjust them from the actual code on freeze day. Any diagram showing an unbuilt part is labelled "planned (Iteration 2)".
- **Explain each diagram.** Every diagram gets 3–6 lines of project-specific text: what it shows, and one decision it reflects. F3-6's top band requires models "thoroughly explained in text".
- **Show the evolution.** A **design-evolution table** (proposal artefact → current artefact → reason → evidence) goes in Report §5.5.
- **No diagrams without reasoning.** A diagram set without reasoning is capped at 50%.

---

## 26. Development Plan

### 26.1 Iterations (handbook: ≥ 2 iterations in FYP-1, each a working, demonstrable product)

| Iteration | Window | Use cases | Release |
|---|---|---|---|
| It-0 Setup | Mid-1 Day 0–1 | Repo, CI, deploy skeleton, schema | — |
| **It-1 Core investigation slice** | → Mid-1 (Week 8) | UC-03, 05, 06, 07, 08, 09, 12 (+ UC-11 S) | `v0.1.0` |
| **It-2 Breadth and inputs** | Weeks 9–15 | UC-01, 02, 04, 10, 11, 13, 14 v0, 15 (LangGraph) | `v0.2.0` (Final-1) |
| It-3 Integration and evaluation | FYP-2 Weeks 1–8 | UC-15 (CrewAI), 16, 17, 14 v1 | `v0.5.0` (Mid-2) |
| It-4 Hardening and UAT | FYP-2 Weeks 9–15 | UAT fixes, handover | `v1.0.0` (Final-2) |

### 26.2 Coding standards and naming conventions

| Item | Python | TypeScript/React |
|---|---|---|
| Style/format | Ruff (PEP 8, line 120), `ruff format` | ESLint (typescript-eslint, react-hooks), Prettier |
| Naming | `snake_case` functions/vars, `PascalCase` classes, `UPPER_CASE` constants, modules `snake_case` | `camelCase` vars/functions, `PascalCase` components/types, `useX` hooks, files `PascalCase.tsx` for components |
| Domain names | Use the §14.1 vocabulary exactly (`Finding`, `Hypothesis`, `Experiment`, `Evidence`). No synonyms ("issue", "bug", "case") in code. | Same |
| Types | Type hints everywhere; `mypy --strict` on `granite_core` | `strict: true` |
| Docstrings/comments | Google-style docstrings on every public function in core. Each algorithmic function cites its design section (e.g. "Implements §21.4 step 5"). Comments explain *why*, not *what*. | TSDoc on exported functions/components with non-obvious behaviour |
| Errors | Typed domain exceptions (`ProviderUnavailable`, `IllegalTransition`, `ReplayUnavailable`) mapped to RFC 7807 | Error boundaries per page section |
| Complexity | Ruff C901 ≤ 10 | ESLint `complexity` ≤ 10 |
| Tests | `test_<unit>_<behaviour>()`; requirement marker `@pytest.mark.req("FR-VER-02")` | `describe(component) / it(behaviour)` |

### 26.3 Working agreements

- **Definition of Ready (for an issue):** user story or task, acceptance criteria, requirement ID, owner, estimate ≤ 2 days (split if larger).
- **WIP:** ≤ 2 items in progress per person.
- **Pairing:** each seam (runner↔replay, attribution↔verification, schema↔lineage) is built by its two owners together for at least one session.
- **Weekly rhythm:**
  - Monday 20-min planning
  - Wednesday 15-min sync
  - Friday 30-min **owner demo**: each member demos their own increment to the others, from their own laptop (this is the C.14.1 rehearsal)
  - Weekly supervisor meeting (handbook: at least once a week) with minutes in `docs/meetings/`
- **AI-assisted development (L2) rules:**
  1. Generated code must be read, run and tested by its owner before the PR.
  2. The PR template's "AI assistance" section records the tool, what was generated and how it was verified. It feeds `docs/registers/ai-usage-log.md` and Form 13.
  3. For CCP-relevant code (checks, attribution, verification), the owner must pass the four C.14.1 questions in the Friday demo (explain, alternative, what breaks, modify live).


**Rubric-driven engineering hygiene (v1.1) [M-R red flags; Rec for the thresholds]:**
- **Small, explainable PRs:** about 300 changed lines or fewer of hand-reviewed code per PR. Each PR description says what the code does, the alternative rejected, and **what happens if it is removed** (the rubric's own probe). Generated or boilerplate files are listed separately.
- **Owner-authored code and tests.** Each member commits their own modules and chapters from their own account. No one bulk-commits another member's work.
- **Daily 10-minute walkthrough during crunch weeks.** Each member explains one function they changed that day, at line level, to another member.
- **Honest status.** An item is "Done" only with a demonstrable artefact link. Partial work is logged as partial.

---

## 27. Testing & Validation Strategy

### 27.1 Testing, evaluation and acceptance (handbook C.13.1, three separate questions)

- **Testing:** does it behave as specified? (§27.2–27.4)
- **Evaluation:** is it any good vs baselines? (§14.6, §27.5)
- **Acceptance:** will real users use it? (§27.6)

### 27.2 Test levels

| Level | Scope | Tools | Owner | Target / gate |
|---|---|---|---|---|
| Unit | `granite_core` (DSL, checks, provenance, verdict, redaction, schema), services, React components | pytest, hypothesis, Vitest | Module owner | Core coverage reported at Mid-1 (≥ 70% gate in Track T2), ≥ 80% gated at Final-1; all green on PR |
| Integration | API + DB (Postgres service container), runner + recorded provider, job runner | pytest + httpx TestClient | Saif (harness), owners (cases) | Every endpoint has ≥ 1 success and ≥ 1 failure test |
| API contract | OpenAPI schema snapshot; RFC 7807 shape | schemathesis (optional, free) | Saif | No undocumented breaking changes |
| UI | Component tests; accessibility | Vitest + Testing Library; axe-core | Screen owner | Core components tested |
| E2E / system | Journeys J1, J2 (Mid-1); J3–J6 (later) against the **deployed staging URL** in recorded mode | Playwright | Shahoud | J1 and J2 green on every staging deploy |
| AI/ML | Golden traces; recorded cassettes; metamorphic tests; provider-swap determinism; prompt regression | pytest | Noor (core), Shahoud (prompts) | Nightly green |
| Regression | All above on PR; nightly mini-benchmark (recorded) with metric thresholds | Actions | Saif | Fail build if origin accuracy drops > 5 pts |
| Performance | NFR-01/02/03 | pytest-benchmark, timing fields, Lighthouse CI | Saif | Targets in §16 |
| Security | DSL attack set, upload fuzz, secrets, dependency audit, redaction scan | pytest, Bandit, pip-audit, gitleaks | Saif | 0 high/critical |
| Usability/UAT | Think-aloud, SUS, task success, time-to-first-finding | Protocol in §27.6 | Shahoud | §16 NFR-09 |

### 27.3 Techniques (where each is used)

- **Equivalence partitioning:** check statuses; fault types; input validity classes.
- **Boundary values:** verdict thresholds at k/N = 0.2, 0.8; c/M = 0.2; N ∈ {1, 10}; file size 5 MB ± 1 byte; 500/501 steps.
- **Decision tables:** VR-1 (20 rows).
- **State-transition testing:** every legal and ≥ 3 illegal finding transitions.
- **Property-based testing (hypothesis):** the DSL evaluator never raises on generated valid expressions and never accepts generated forbidden nodes; redaction is idempotent.
- **Metamorphic testing:** provenance invariances (§21.6).
- **Error guessing:** LLM returns non-JSON; empty steps; duplicate step IDs.
- **Mutation-style negative tests:** clean controls must yield no findings.

### 27.4 System-level test suites

| Suite | Contents | First at |
|---|---|---|
| SYS-CORE | J1 end to end (fault → finding → H1 → CONFIRMED → accept → history); J2 clean run → no finding; H2 verification → REFUTED | Mid-1 |
| SYS-ERR | LLM down at run start; LLM down mid-experiment (ERROR + partial); malformed import; check ERROR; replay unavailable (409); DB unavailable (503 problem) | Mid-1 (first 3), Final-1 |
| SYS-SEC | DSL attacks; oversize/malformed upload; rate limit; secrets scan | Mid-1 (DSL), Final-1 |
| SYS-PERF | Analysis p95; verification duration; FCP | Final-1 |
| SYS-A11Y | axe on S0–S10; keyboard-only J1 | Final-1 |
| SYS-DEPLOY | Clean-machine `docker compose up` following the manual, by a non-owner | Final-1 (team), Final-2 (outsider) |

### 27.5 Evaluation protocol (research track)

- **Data:** benchmark v0 (Final-1, ≥120 runs), v1 (Mid-2, ≥300 runs), v2 (Final-2, S: 500). Each has 20% clean controls, 3 fault types, 2 workflows, ≥2 runtimes. Plus a 50-finding natural-failure set labelled by two members (κ). Plus a Who&When subset (≥30 cases) for the LLM-attribution track.
- **Methods:**
  - Granite provenance
  - last-agent
  - LLM-judge all-at-once (same local model)
  - ErrorProbe-lite (Mid-2, S)
  - verification ablations: N=1 vs 3 vs 5; M=0 vs 2; no regression guard
- **Metrics:** §14.6, plus recovery rate for confirmed fixes and LLM calls per verdict. Bootstrap 95% CIs; fixed seeds; the analysis script frozen before running (pre-registration file committed with a date).
- **Honest-limits statement:**
  - injected-fault accuracy is an upper bound
  - coverage limits detection
  - small models inflate natural failure rates
  - the Who&When comparison is backbone-confounded

### 27.6 User acceptance testing plan (plan due by Mid-2, evidence by Final-2)

- **Participants:** 5–8 proxies matching P1–P3 (alumni developers, AI-course students, an FYP team). Declared as proxies.
- **Method:** supervised 45-min sessions (remote or in person) with consent; tasks J1, J3, J4, J6.
- **Measures:** completion, time, errors, assistance needed, SUS, time-to-first-finding (SDK), verbatim acceptance statement.
- **Recording:** short consented screen recordings.
- **Issues log:** each issue → fixed / deferred, with reason.
- **Acceptance decision:** recorded in the participant's words.
- **Pilot:** 3 peers at Final-1.

### 27.7 Defect management and traceability

- **Severity:**
  - **Critical:** wrong verdict or data loss/corruption, security hole, or the core journey is blocked.
  - **High:** a Must requirement fails, with a workaround.
  - **Medium:** a Should requirement fails, or degraded UX.
  - **Low:** cosmetic.
- **Rules:**
  - no open Critical at any release tag
  - every open High has a recorded disposition at Mid-2 (handbook Gate 4)
  - defects are GitHub issues labelled `severity:*`
- **Traceability:** pytest `req` markers + Vitest tags → `scripts/build_traceability.py` produces a matrix (FR → tests → last result → code module), published as a CI artefact and pasted into the report. This is the "traceability matrix opened at Mid-1" (C.5.1) at almost no cost.

---

## 28. CI/CD & GitHub Strategy

### 28.1 Repository structure (done on disk 2026-10-06; commit it as one pure-move chore PR)

The full layout, naming rules and placement table are in [`docs/workspace-guide.md`](../workspace-guide.md); the tree is deliberately not copied here, so it cannot drift. The implementation-specific parts:

```
apps/
├── api/                     FastAPI app: routers/, services/, db/ (models, repositories, migrations/)
└── web/                     React + Vite app (shell evolved from the stage-0 proposal console)
packages/
├── granite_core/            pure library: schema, graph, checks, attribution, verification, redaction
└── granite_sdk/             (Final-1) tracer + adapters: langgraph/, crewai/
workflows/                   demo workflows: refund_desk/, math_crew/ (+ prompts/; seed data from data/seed/)
tests/e2e/                   Playwright (unit tests live next to the code)
scripts/                     wait_for_version.sh, build_traceability.py, fetch_datasets.sh (see scripts/README.md)
.github/                     workflows/, ISSUE_TEMPLATE/, pull_request_template.md, CODEOWNERS, dependabot.yml
repository root              Dockerfile, docker-compose.yml, pyproject.toml, .env.example, CHANGELOG.md, LICENSE
```

**Day-0 repo hygiene (before anything else):**
1. Back up the working folder (done: `../_backup_pre-reorg_2026-10-06.zip`, outside the repository).
2. Clear the stale rebase state, commit the reorganization on a branch, then merge `origin/noor` (order and commands in [`archive/README.md`](../../archive/README.md)). The layout was moved on disk first, so committing it comes before the merge. The modified `.pptx` and the formerly untracked CCP files (now under `deliverables/stage-0-proposal/ccp-justification/`) are committed in the same step.
3. Tag the defense state `proposal-defense-2026-09-11`.
4. Create `main` from it and set `main` as the default branch.
5. Create `develop`.
6. Untrack `data/raw/` (keep `data/DOWNLOAD.md` + a fetch script).
7. Add a `.mailmap` so Noor's two commit identities (`Muhammad Noor`, `MuhammadNoor7`) count as one person in contribution graphs and `git shortlog`.
8. Import the report template into `docs/report/` (Shahoud) and apply the three rendering fixes (§30.5).
9. The folder restructure is a **pure-move chore PR** (moves and link fixes only, no logic changes), clearly labelled, with the move map in `archive/migration-map_2026-10-06.tsv`. That way it is not read as a "sudden code volume" (rubric red flag).

### 28.2 Branching strategy (Git-flow-lite, mapped to academic releases)

| Branch | Purpose | Rules |
|---|---|---|
| `main` | What is in production; every commit is a tagged release | Protected. PR from `develop` (release PR) or `hotfix/*` only. 1 approval from a non-author. All checks green. Squash/merge commit. No force push. |
| `develop` | Integration; auto-deploys to **staging** | Protected. PR only. 1 non-author approval. Checks green. Squash merge. Linear history. |
| `feature/<issue>-<slug>` | One issue, ≤ 2–3 days | From `develop`. Delete after merge. |
| `fix/<issue>-<slug>`, `docs/<slug>`, `chore/<slug>`, `test/<slug>` | Same | Same |
| `hotfix/<slug>` | Urgent production fix | From `main`. PR to `main`, then back-merge to `develop`. |

### 28.3 Conventions

- **Commits / PR titles:** Conventional Commits with scope, e.g. `feat(verify): add control replays (#42)`. The PR title is linted (squash uses it). Scopes: `run, check, attr, verify, review, report, ui, api, db, sdk, lab, eval, ci, docs`.
- **PR template:** linked issue; what/why; requirement IDs; how tested; screenshots/GIF for UI; **AI assistance** (tool / what / how verified); checklist (tests, docs, migration, no secrets).
- **Issue templates:** Feature (user story + AC + FR ID), Bug (steps / expected / actual / severity / env), Task.
- **Labels:** `type:*`, `area:*`, `priority:P0–P3`, `severity:*`, `good-first-review`.
- **GitHub Project board:** Backlog → Ready → In progress → In review → Done. Milestones = Mid-1, Final-1, Mid-2, Job-Fair, Final-2.
- **CODEOWNERS:** routes reviews (§34).
- **Versioning:** SemVer. `v0.1.0` Mid-1, `v0.2.0` Final-1, `v0.5.0` Mid-2, `v0.6.x` job fair, `v1.0.0` Final-2. Release notes generated per tag. `CHANGELOG.md` kept.

### 28.4 What runs when

| Event | Workflow | Jobs | Purpose |
|---|---|---|---|
| Push to any non-`main` branch | `ci.yml` | backend (ruff, mypy, bandit, pip-audit, pytest + coverage gate, Postgres service); frontend (eslint, tsc, vitest, build, npm audit); secrets (gitleaks); docker build | Fast feedback |
| Pull request → `develop`/`main` | `ci.yml` + `pr-title.yml` + `import-linter` | Same + PR title lint + layer contracts; coverage summary comment | Merge gate (required checks) |
| Merge to `develop` | `deploy-staging.yml` (after `ci` succeeds) | Render staging deploy hook → wait until `/health.git_sha` matches → Playwright smoke (J1, J2) + axe on staging | Continuous delivery to staging |
| Tag `v*.*.*` on `main` | `release.yml` | Build + push image to GHCR (lowercased name) → production deploy hook → health/sha wait → smoke → GitHub Release with generated notes + evaluation/traceability artefacts | Controlled production release |
| Nightly (cron) + manual | `nightly.yml` | Mini-benchmark in recorded mode; metric thresholds; traceability matrix; DB backup (prod) | Regression of the *research claims*, not only code |
| Weekly | Dependabot | pip/npm/actions updates | Supply-chain hygiene |

### 28.5 Pipeline diagram

```mermaid
flowchart LR
  FB["feature branch"] -->|push| CI1["CI: lint, types, unit and integration tests, security, build"]
  FB -->|PR to develop| GATE["Required checks plus 1 non-author review"]
  GATE -->|squash merge| DEV["develop"]
  DEV --> STG["Deploy staging on Render, DB on Neon staging branch"]
  STG --> E2E["Smoke and E2E plus accessibility on staging URL"]
  DEV -->|release PR| MAIN["main"]
  MAIN -->|tag vX.Y.Z| REL["Release: image to GHCR, deploy production, smoke, GitHub Release"]
  NIGHT["Nightly"] --> BENCH["Mini benchmark with metric thresholds"]
```

### 28.6 Workflow skeletons (adapt, but keep the gates)

```yaml
# .github/workflows/ci.yml
name: ci
on:
  push:
    branches-ignore: [main]
  pull_request:
    branches: [develop, main]
concurrency: { group: "ci-${{ github.ref }}", cancel-in-progress: true }
jobs:
  backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_PASSWORD: postgres, POSTGRES_DB: granite_test }
        ports: ["5432:5432"]
        options: --health-cmd pg_isready --health-interval 5s --health-retries 10
    env:
      DATABASE_URL: postgresql+psycopg://postgres:postgres@localhost:5432/granite_test
      GRANITE_LLM_MODE: recorded
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11", cache: pip }
      - run: pip install -e "packages/granite_core[dev]" -e "apps/api[dev]"
      - run: ruff check . && ruff format --check .
      - run: mypy packages/granite_core
      - run: bandit -q -r packages apps/api
      - run: pip-audit
      - run: lint-imports
      - run: pytest --cov --cov-report=xml --cov-fail-under=70   # T0/T1: start at 0 and raise to 70 once core tests exist (§30.6)
      - uses: actions/upload-artifact@v4
        with: { name: coverage-backend, path: coverage.xml }
  frontend:
    runs-on: ubuntu-latest
    defaults: { run: { working-directory: apps/web } }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm, cache-dependency-path: apps/web/package-lock.json }
      - run: npm ci
      - run: npm run lint && npm run typecheck && npm test -- --coverage && npm run build
      - run: npm audit --audit-level=high
  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: gitleaks/gitleaks-action@v2
        env: { GITHUB_TOKEN: "${{ secrets.GITHUB_TOKEN }}" }
  docker:
    needs: [backend, frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build --build-arg GIT_SHA=${{ github.sha }} -t granite:ci .
```

```yaml
# .github/workflows/deploy-staging.yml
name: deploy-staging
on:
  workflow_run: { workflows: [ci], types: [completed], branches: [develop] }
jobs:
  deploy:
    if: github.event.workflow_run.conclusion == 'success' && github.event.workflow_run.event == 'push'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
        with: { ref: "${{ github.event.workflow_run.head_sha }}" }
      - run: curl -fsS -X POST "${{ secrets.RENDER_DEPLOY_HOOK }}"
      - run: ./scripts/wait_for_version.sh "${{ vars.APP_URL }}" "${{ github.event.workflow_run.head_sha }}"
      - run: cd tests/e2e && npm ci && npx playwright install --with-deps chromium && BASE_URL="${{ vars.APP_URL }}" npx playwright test --grep @smoke
```

```yaml
# .github/workflows/release.yml (abridged)
on: { push: { tags: ["v*.*.*"] } }
jobs:
  release:
    runs-on: ubuntu-latest
    environment: production
    permissions: { contents: write, packages: write }
    steps:
      - uses: actions/checkout@v4
      - run: |
          IMAGE="ghcr.io/${GITHUB_REPOSITORY,,}:${GITHUB_REF_NAME}"
          echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u "${{ github.actor }}" --password-stdin
          docker build --build-arg GIT_SHA=${{ github.sha }} -t "$IMAGE" . && docker push "$IMAGE"
      - run: curl -fsS -X POST "${{ secrets.RENDER_DEPLOY_HOOK }}"
      - run: ./scripts/wait_for_version.sh "${{ vars.APP_URL }}" "${{ github.sha }}"
      - run: gh release create "$GITHUB_REF_NAME" --generate-notes
        env: { GH_TOKEN: "${{ secrets.GITHUB_TOKEN }}" }
```

### 28.7 Configuration and secrets

- **Config library:** `pydantic-settings`. Every setting comes from env vars with typed defaults. `.env.example` is committed; `.env` is ignored.
- **GitHub Environments:**
  - `staging` and `production`, each holding the secret `RENDER_DEPLOY_HOOK` and the variable `APP_URL`
  - `production` requires a manual approval by a second member (a meaningful control)
- **Render env:** `DATABASE_URL` (Neon branch), `GRANITE_ENV`, `GRANITE_LLM_PROVIDER`, `GRANITE_LLM_BASE_URL`, `GRANITE_LLM_MODEL`, `GRANITE_LLM_API_KEY` (secret), `GRANITE_PUBLIC_DEMO=true`, `GRANITE_RATE_LIMIT`.
- **Never** commit keys, real traces or datasets with restrictive licences.

---

## 29. Deployment Strategy

### 29.1 Environments

| Env | Where | Data | LLM | Deployed by |
|---|---|---|---|---|
| Local dev | Docker Compose (`granite` + `postgres` + optional `ollama` profile) | Seed snapshot | Ollama or recorded | Developer |
| CI | GitHub runner | Ephemeral Postgres | Recorded | `ci.yml` |
| **Staging** | Render free web service `granite-staging` (linked to `develop`, auto-deploy off; hook-triggered) | Neon branch `staging` | Hosted free tier / recorded | `deploy-staging.yml` |
| **Production (public demo)** | Render free web service `granite` (linked to `main`, auto-deploy off) | Neon branch `main` | Hosted free tier; recorded fallback toggle | `release.yml` + manual approval |
| **Self-hosted (product)** | Any machine: `docker compose up` | User's | Ollama local | User, via the setup manual |

### 29.2 Deployment diagram

```mermaid
flowchart TB
  subgraph GH["GitHub"]
    REPO["Repository and Actions"]
    GHCR["Container registry"]
  end
  subgraph Render["Render free web services"]
    STG["granite-staging container<br/>FastAPI plus built React"]
    PRD["granite container<br/>FastAPI plus built React"]
  end
  subgraph Neon["Neon Postgres free"]
    DBS[("branch staging")]
    DBP[("branch main")]
  end
  LLMAPI["Hosted LLM free tier"]
  USER["Evaluator browser"] -->|HTTPS| PRD
  REPO -->|"deploy hook on develop"| STG
  REPO -->|"deploy hook on tag"| PRD
  REPO --> GHCR
  STG --> DBS
  PRD --> DBP
  STG --> LLMAPI
  PRD --> LLMAPI
  subgraph SELF["Self-hosted, docker compose"]
    LAPP["granite"] --> LPG[("postgres")]
    LAPP --> OLL["Ollama local model"]
  end
```

### 29.3 Container design

**Multi-stage Dockerfile:**
1. A Node stage builds `apps/web`.
2. A Python 3.11-slim stage installs `granite_core` and `apps/api`, then copies the built `dist/` to be served by FastAPI.

**Runtime:**
- Entrypoint runs `alembic upgrade head`, then `uvicorn`.
- Non-root user.
- `GIT_SHA` build arg exposed on `/health`.
- Image ≤ 400 MB (target).

### 29.4 Operations

- **Cold start:** Render free sleeps after 15 min idle and takes about 1 min to wake. Hit `/health` 10 min before any evaluation. Never rely on a cold instance live.
- **Hours budget:** 750 free hours per workspace per month. Two services that sleep stay within it. Do not keep-alive both.
- **Rollback:**
  - re-run `release.yml` on the previous tag, or use Render's rollback
  - migrations are written expand/contract, so one-version rollback is safe
- **Monitoring:**
  - structured JSON logs (request ID, run ID, duration)
  - Render log viewer
  - an `/metrics`-style JSON endpoint (counts, durations)
  - the nightly workflow records health
- **Deployment record (handbook C.1.2 evidence):** `docs/registers/deployment-record.md`, updated per release. It records:
  - where it runs (URLs)
  - how it was installed (workflow run link)
  - who can access it
  - cost ($0)
  - known limits (sleep, rate limits)
  - "installed by non-owner" entries

### 29.5 Demo-day contingency (every evaluation)

1. Primary: production URL, warmed, with the hosted LLM.
2. If the LLM quota or provider fails: switch the instance to **Recorded mode** (settings toggle). The same pipeline runs on recorded responses, and we say so openly.
3. If Render or Neon fails: a laptop runs `docker compose up` in recorded mode (rehearsed).
4. Last resort: recorded screencast. Show it only alongside the code walkthrough. A video alone is not acceptable as a demo (Form 2/7).

### 29.6 Fallbacks if a free tier changes

| Service | Fallbacks (in order) |
|---|---|
| Render | Koyeb free instance, then Azure for Students credits (no card; verify), then a laptop + Cloudflare Tunnel |
| Neon | Supabase free (pauses when idle) |
| Hosted LLM | The other provider (Groq ↔ Gemini), then Ollama on a team laptop via tunnel, then recorded mode |

---

## 30. Mid-1 Implementation Plan (Iteration 1: the real product slice; rubric-aligned in v1.1)

### 30.1 What Mid-1 assesses, and where our marks come from [M-R]

The official guide defines Mid-1 as a formative, supervisor-only checkpoint around Week 8, worth 20% of FYP-1. It uses **Form 2** (presentation and demo, 100 marks) and **Form 3** (report, 100 marks). The guide does not say how the two combine inside the 20% (D7).

Target bands below are planning targets, not predictions. T0/T1/T2 are the tracks in §30.2.

**Form 2: presentation and demo**

| # | Criterion (CLO, marks) | Top band requires (rubric) | Our evidence | Target T0 · T1 · T2 | Owner |
|---|---|---|---|---|---|
| F2-1 | Previous proposal actions addressed (CLO6, 10) | All actions fully addressed with verifiable live evidence | Register A1–A6 with live links, opened in the session (§3) | 7–8 · 9–10 · 9–10 | Shahoud |
| F2-2 | Iteration plan and work breakdown progress (CLO2, 10) | On or ahead of plan, with justified delays and buffers | Milestone log (planned vs actual), board, owner-assigned recovery plan. **Honest:** code started on 6 Oct, so "minor slip with clear recovery plan" (7–8) is the realistic ceiling. | 5–6 · 7–8 · 7–8 | Shahoud |
| F2-3 | Live prototype with core module (CLO4, **25**) | Meaningful core module working live, with edge/failure cases. Screenshots or video do not count. "Noticeable hardcoded scaffolding" drops it to 11–15. | Refund Desk slice on **supervisor-chosen input**: run → outcome check FAIL → provenance H1 → CONFIRMED. Also H2 → REFUTED, a clean run with no finding, and provider-down handled gracefully. | 6–10 · 16–20 (21+ if failure cases run smoothly) · 21–25 | All |
| F2-4 | Requirements and acceptance criteria (CLO2, 10) | Precise, testable FRs/NFRs connected directly to the implementation | FR ID ↔ acceptance check ↔ test ID ↔ file | 7–8 · 7–8 · 9–10 | Noor |
| F2-5 | Design artefacts and design evolution (CLO3, 15) | Artefacts match the current code; architectural changes explained | Diagrams redrawn from the tagged code; design-evolution table | 7–9 · 10–12 · 13–15 | Saif |
| F2-6 | Repository, milestone and member evidence (CLO6, 10) | Regular, incremental commits from all members with meaningful messages; tagged code; task log | Tag, per-member PRs from own accounts, board, CI/CD runs, `.mailmap`. The pre-October history is uneven and cannot be rewritten; show the change honestly. | 4–6 · 5–8 · 7–8 | Saif |
| F2-7 | Testing and early validation (CLO4, 10) | Systematic unit/module tests executed; failure case actively discussed | pytest run (live or in CI), edge/failure tests, a fixed-bug PR; T2 adds the mini-validation table | 3–6 · 7–8 · 9–10 | Saif + owners |
| F2-8 | Presentation, Q&A, team and tool ownership (CLO5, 10) | Confident, balanced defence; tool usage fully owned and explained | Each member presents their own module and chapters, walks through their own code, and reads their own Form 13 rows | 7–8 · 9–10 · 9–10 | All |

**Form 3: report** (the targets assume the report plan in §30.5 is followed; only F3-7 depends on the track)

| # | Criterion (CLO, marks) | Top band requires (rubric) | Our evidence (report location) | Target | Owner |
|---|---|---|---|---|---|
| F3-1 | Report format and artefacts present (CLO2, 5) | Strict template adherence; all mandatory sections, signatures and artefacts | Filled template, defects fixed, signatures (front matter) | 4.5–5 | Shahoud |
| F3-2 | Problem formulation, R&D and gap analysis (CLO1, 15) | Rigorous literature synthesis that isolates the gap and the complex computing challenge | Ch2 in own words: research systems incl. DoVer, products, prior FYPs, comparison table, gaps, CCP, research → decision table | 10.5–12.5, aiming for 13+ | Noor |
| F3-3 | Project vision, scope and success criteria (CLO2, 10) | Crystal-clear scope, modular breakdown, testable success metrics, **consistent with the proposal** | Ch1 + **Scope Table** + mapping to the approved mechanisms (§11.3) + C-01 | 9–10 | Shahoud |
| F3-4 | Requirements and acceptance criteria (CLO2, 15) | Precise, numbered FRs/NFRs with verifiable acceptance checks | Ch4 + App. B: FR/NFR tables, acceptance table, traceability | 13–15 | Noor (+Shahoud for UCs) |
| F3-5 | Architecture and component/interface design (CLO3, 15) | Detailed architecture with layer separation and interface contracts | Ch5: layers, components, contracts (§19.4), API (§23), ADRs | 13–15 | Saif |
| F3-6 | Data/process/behaviour design (CLO3, 10) | Project-specific models, thoroughly explained in text | Ch5: ERD + data dictionary, state machine, verification sequence, activity/DFD, each with explanation | 9–10 | Saif, Shahoud |
| F3-7 | Implementation documentation (CLO4, 15) | Setup, classes, algorithms and trade-offs clear; reproducible | Ch6: per-owner files/classes/functions, algorithms (§21.4–21.5), reproducible setup steps | T0 7.5–10 · T1 10.5–12.5 · T2 13–15 | All |
| F3-8 | Testing plan and tool/risk disclosure (CLO5, 15) | Thorough test plan; full disclosure of external/GenAI tools, risks and privacy | Ch7 + Ch8.7–8.10 + Form 13 + AI usage log summary, **including GenAI help with planning and report language** | 13–15 | Saif (tests), Shahoud (disclosure) |

**Reading the tables:**
- F2-3 (25) is the single largest item in Form 2. Form 3 is a separate 100-mark form, so report quality cannot be traded off against the demo; their relative weight is not stated (D7).
- Hours go first to the live slice and to the 15-mark report chapters.
- The gates (tool disclosure = 0 if missing; repository evidence capped at 40%; diagrams-only design capped at 50%; no live system → demo capped) apply to every track, so their evidence is non-negotiable.

### 30.2 Choose the track by the confirmed Mid-1 date [Rec, driven by M-R/M-F]

**Status on Tue 6 Oct:** no product code; report template empty; Day-0 not done. D0 is the day the track is chosen.

| Track | Use when | Product at Mid-1 | Report at Mid-1 | Honest expectation |
|---|---|---|---|---|
| **T0** | Mid-1 within 1 working day | CI skeleton and repo hygiene if time allows. **Run the real spike code live:** 3b fault injection (needs CrewAI + Ollama), 4b check mechanism and 5 replay (no LLM needed). Present the redesigned workflow (§13) and screens (§18) as wireframes. | Every chapter filled from existing work, in our own words. Ch6 documents the spike code honestly as proposal-stage code. | F2-3 in the 6–10 band ("barely beyond POC-lite"). Recover with the rubric's own remedy: three specific, weekly, demonstrable milestones agreed at Mid-1 (§30.6). |
| **T1** | 2–4 working days | Core slice live through a **minimal UI evolved from the existing PoC console** (the faculty statement allows "the live/functional interface (or its improved version) that was shown as a POC"). Three screens: New run, Run detail (steps, checks, findings), Finding (hypotheses, Verify, Review). Live LLM with recorded fallback. CI green. Deployed if CD works by the last day's noon; otherwise run locally and say so. | Full report. Ch6 documents the slice. | F2-3 16–20 (21+ if failure cases run smoothly) |
| **T2** | 5–8 working days (e.g. Mid-1 on 12–16 Oct) | The full §30.4 scope: CD to staging, findings inbox, graph view, Markdown export, Playwright smoke, mini-validation (20 fault + 10 clean runs) | Full report, including the validation table | F2-3 21–25 |

**Allowed simplifications in T0/T1 [Rec]:**
- The Policy step is deterministic rules (code), not an LLM agent. Fewer flaky calls; it can become an LLM agent in Iteration 2 if useful.
- SQLite instead of Postgres when not deploying.
- A steps list instead of the graph library.
- No PII redaction yet (synthetic data only, disclosed).

### 30.3 Day-by-day plan (D0 = today; the report runs in parallel from D0)

**Track T1** (Mid-1 on D3 or D4; about 75–90 team-hours, about 35% of them on the report)

| Day | Shahoud | Noor | Saif | End-of-day evidence |
|---|---|---|---|---|
| D0 (3–4 h each) | Confirm A1/D5/D7. Template into `docs/report/` with the three fixes; title page, names, roll numbers, supervisor. Register rows A1–A6 drafted. | `granite_core` package; check DSL evaluator (AST whitelist) + ≥ 8 tests. Ch2 outline. | Day-0 hygiene (§28.1) incl. `.mailmap`; CI (ruff + pytest) green | Template compiles. CI green on `develop`. |
| D1 | `TraceV1` schema; Refund Desk runner (Intake LLM, Lookup tool, Policy rules, Calculator LLM, Writer LLM); provider layer (Ollama / OpenAI-compatible / Recorded); FLT-STALE. Report: Ch1 (with Scope Table), Ch3. | Seeded checks + truth functions; provenance attribution + tests (fault, clean, H2). Report: Ch2. | FastAPI app, models (SQLite), run/finding/job endpoints, background job runner; Dockerfile. Report: Ch5 skeleton. | A run launched through the API produces findings and hypotheses |
| D2 | Pair with Saif on `Runner.execute(plan)`. UI: shell + New run (evolve the stage-0 `poc-console`). Report: Ch4 use cases + diagram. | UI: Run detail (steps, checks, findings). Report: Ch4 FR/NFR + acceptance table. | Replay planner + VR-1 verdict + experiments endpoint + tests; review state machine + audit log; UI: Finding (Verify, Review). Report: Ch7 plan. | The full loop works end to end locally |
| D3 | **Morning:** failure cases (clean run, H2 REFUTED, provider down); bug fixes. **Afternoon:** Ch8 contribution table + tool disclosure; Ch9; Ch10; front matter; App. A and F. | **Morning:** fixes and tests. **Afternoon:** Ch6 for own modules; own-module diagrams from the code; bibliography; App. B. | **Morning:** tag `v0.1.0-mid1`; deploy if CD is ready by noon (otherwise disclose the local run). **Afternoon:** Ch5 diagrams from code; Ch6 for own modules; Ch7 results; App. C and D. | Compiled report PDF; tag; two rehearsals; paragraph-defense drill |

**Track T2** (Mid-1 on D7–D8). D0–D3 as in T1, then:

| Day | Shahoud | Noor | Saif |
|---|---|---|---|
| D4 | Findings inbox; empty/loading/error states; graph view (React Flow) | Metamorphic and property tests; attribution edge cases | CD to Render staging (deploy hook + health/sha wait); Neon |
| D5 | Playwright smoke J1/J2; provider-down banner; PII redaction | Mini-validation harness (20 fault + 10 clean runs: detection recall, false alarms, H1 accuracy, verdicts) | Markdown export; SYS-ERR cases; coverage gate |
| D6 | Run the mini-validation; Ch6/Ch7 results | Ch2/Ch4 polish; validation table | Diagrams from code; Ch5 |
| D7 | Freeze at noon; tag; compile the report; two rehearsals | ← same | ← same |

**Track T0** (Mid-1 tomorrow), D0:
- Register with evidence links; milestone log.
- **Recovery plan with three weekly, demonstrable milestones**, each with an owner and date. Week 1 = T1 slice; week 2 = T2 additions; week 3 = Iteration-2 start.
- Fill the report chapters from existing material in our own words. Priority: Ch1, Ch2, Ch4, Ch5, Ch7, Ch8.
- Rehearse running spikes 3b, 4b and 5 live.
- Saif does repo hygiene and a CI skeleton if time allows.
- Disclose everything.

### 30.4 Mid-1 backlog (GitHub issues, with the track each belongs to)

| # | Issue | Owner | Est. | Track | Req |
|---|---|---|---|---|---|
| 1 | Repo hygiene (commit the on-disk restructure per `archive/README.md`) + `main`/`develop` + protections + `.mailmap` | Saif (+Shahoud) | 4 h | T0 T1 T2 | — |
| 2 | CI workflow (backend/frontend/secrets; docker build in T2) | Saif | 3–4 h | T0* T1 T2 | NFR-07/11 [M-F] |
| 3 | Dockerfile + `/health` + Render staging + Neon + deploy workflow | Saif | 5 h | T2 (T1 stretch) | NFR-12/13 [M-F CD] |
| 4 | `TraceV1` pydantic schema + fixtures | Shahoud | 3 h | T1 T2 | FR-IMP-01 (base) |
| 5 | Truth snapshot (tau-bench subset) + licence attribution | Shahoud | 2 h | T1 T2 | FR-CHK-06 |
| 6 | Workflow runner + Refund Desk (5 steps, prompts v1; Policy as rules in T1) | Shahoud | 8 h | T1 T2 | FR-RUN-01 |
| 7 | LLM provider layer (Ollama, OpenAI-compatible, Recorded) | Shahoud | 5 h | T1 T2 | FR-RUN-03/04 |
| 8 | Fault FLT-STALE + `fault_injection` record | Shahoud | 2 h | T1 T2 | FR-RUN-02 |
| 9 | Check DSL evaluator + security tests | Noor | 6 h | T1 T2 | FR-CHK-01/02/03 |
| 10 | Seed 5 checks + truth functions | Noor | 2 h | T1 T2 | FR-CHK-06 |
| 11 | Graph + lineage builder | Noor | 3 h | T1 T2 | FR-ATT-01 |
| 12 | Provenance attribution + ranking + evidence | Noor | 8 h | T1 T2 | FR-ATT-01/02 |
| 13 | DB models + migrations + repositories (SQLite in T1) | Saif | 4–5 h | T1 T2 | §22 |
| 14 | Job runner + run/finding/job endpoints | Saif | 6 h | T1 T2 | §23 |
| 15 | Replay planner + `Runner.execute(plan)` integration | Saif + Shahoud | 6 h | T1 T2 | FR-VER-01 |
| 16 | VR-1 verdict + Wilson CI + experiment endpoint + tests | Saif | 5 h | T1 T2 | FR-VER-02/03 |
| 17 | Finding state machine + review endpoint + audit log | Saif | 4 h | T1 T2 | FR-REV-01/02 |
| 18 | Web: shell + S4 New run (S0 Home in T2) | Shahoud | 4–6 h | T1 T2 | §18 |
| 19 | Web: S6 Run detail (S7 inspector, S8 inbox in T2) | Noor | 4–7 h | T1 T2 | §18 |
| 20 | Web: S9 Finding + S10 Verify + review form | Saif | 6–7 h | T1 T2 | §18 |
| 21 | Playwright J1/J2 smoke (T1: a manual, scripted check instead) | Shahoud | 3 h | T2 | SYS-CORE |
| 22 | Error state: provider down | Shahoud | 2 h | T1 T2 | FR-RUN-04 |
| 23 | Report chapters (§30.5) | All | about 8–10 h each | T0 T1 T2 | [M-R Form 3] |
| 24 | Registers: Form 10, Form 13, AI log, dependency/licence, milestone log, C-01 | Shahoud (collate), all (inputs) | 3 h | T0 T1 T2 | [M-R F2-1/2, F3-8] |
| 25 | Report template setup + three rendering fixes + title data | Shahoud | 2 h | T0 T1 T2 | [M-T][M-R F3-1] |
| 26 | Mini-validation run (20 fault + 10 clean) + results table | Noor | 5 h | T2 | [Rec] strengthens F2-7/F3-8 |

### 30.5 Mid report (Form 3) in the prescribed LaTeX template [M-T][M-R]

**Template facts (from the zip):**
- Class `fast-nuces-bs.cls` v0.3: `book`, 12 pt, A4, Times via `mathptmx`, margins 3 cm left/right and 2.5 cm top/bottom, line spread 1.15, footer page numbers, chapter/section running heads.
- Ten chapters plus Appendices A–F; IEEEtran BibTeX.
- The README states it is "aligned with Form 2 and Form 3 evaluation criteria".
- The chapter files are named `chapter8_testing`, `chapter9_…` and `chapter10_…`, but LaTeX numbers them Ch7, Ch8 and Ch9. This plan uses the **rendered** numbers.

**Three rendering defects (visible in the supplied PDF, traced to the source; fix before writing; rendering only, no style change):**

| # | Symptom in the supplied PDF | Cause | Fix |
|---|---|---|---|
| 1 | "Contents", "List of Figures" and "List of Tables" appear twice; front-matter page numbers break (List of Tables shows page 0) | The class's `\maketitle` already prints the TOC, LoF and LoT and resets numbering to arabic 0. `main.tex` prints them again after the Executive Summary. | Delete the `\tableofcontents`, `\listoffigures`, `\listoftables`, `\pagenumbering{arabic}` and `\setcounter{page}{0}` lines from `\maketitle` in the class. `main.tex`'s order already matches the handbook's front-matter order. |
| 2 | "…for the project titled ." and student lines without names | `\projecttitle`, `\studentone`, `\studenttwo` and `\studentthree` are used in `01_students_submission.tex` but defined nowhere | Define them in `main.tex`, e.g. `\newcommand{\studentone}{Shahoud Shahid (23i-2515)}` |
| 3 | The Proposal Action Register prints "p0.06p0.28p0.25p0.14p0.17" instead of a table | `longtable` and `booktabs` are not loaded | Add `\usepackage{longtable,booktabs}` to `main.tex` |

**Fill-ins:**
- `\title`
- the three authors and roll numbers (23i-2515, 23i-2520, 23i-2634)
- `\supervisor{Dr. Adil Majeed}`
- comment out `\cosupervisor` if not applicable (the class prints the co-supervisor block whenever the macro is defined)
- `\sessionduration{2023-2027}`
- `\degreename{Data Science}` (not rendered on the Mid template, but must be correct)
- the HoD, Dean and coordinator macros (not rendered; fill with correct names only if known)
- signatures on Students' Submission
- a real `references.bib` (§39.4)

After fixing, compile and confirm all three symptoms are gone. Mention the fixes in one line in App. D so they are not mistaken for altering the template.

**Chapter map: what goes where, who writes it, and which criterion it earns**

| Rendered chapter (file) | Granite-specific content | Plan source | Rubric | Owner | Guide length |
|---|---|---|---|---|---|
| Front matter: Students' Submission, Anti-Plagiarism, Authors' Declaration, Abstract, Acknowledgments, Executive Summary, Abbreviations | Real names, rolls and signatures; abstract 50–125 words (D6); 1–2-page executive summary; abbreviations (MAS, LLM, CCP, VR-1, CI/CD, ERD, DFD, FR/NFR, UAT…) | §1 | F3-1 | Shahoud | 4–5 pp |
| Ch1 Introduction and Project Vision (1.1–1.11) | Overview; problem statement; context (refund scenario); vision; measurable objectives; **Scope Table** (module · in/out · proposal origin (§11.3) · Mid-1 status · Final-1 target · success metric); modules (7 user-facing + Fault Lab/Evaluation); stakeholders and personas; success criteria (§7, §14.6, §16); constraints and assumptions ($0, local models, free tiers); ethics, legal and DEI | §4–7, §11, §16, §24 | **F3-3** | Shahoud | 5–7 pp |
| Ch2 Research and Existing Solutions (2.1–2.8) | Method: papers read, product docs checked, 660-title prior-FYP archive. Research systems: Who&When, AgenTracer, SDBL, TraceElephant, ErrorProbe, AgentAsk, PROTEA, DoVer. Products: LangSmith Engine, Percival, Galileo, Raindrop, Invariant, Langfuse/Phoenix. Comparison table; gaps; proposed solution; CCP characteristics table; technical challenges; research → decision table. | §5, §10 + the existing literature review, **rewritten** | **F3-2** | Noor | 6–8 pp |
| Ch3 Proposal Feedback and Iteration Plan (3.1–3.8) | The five panel comments verbatim; register A1–A6 (template longtable with an Evidence link per row); iteration strategy; It-1 and It-2 plans; work breakdown; progress vs plan; delays and recovery plan (honest: implementation began 6 Oct, because post-defense time went into redefining the workflow) | §3, §26.1, §30–31, §34 | F2-1, F2-2, F3-3 | Shahoud | 3–4 pp |
| Ch4 Software Requirements (4.1–4.7) | Actors and UCs; UC diagram; 3–4 detailed UCs (UC-03, 07, 08, 09). FRs by module: the template's "Module 1/2" subsections become one subsection per module. NFRs: the template's Reliability, Usability, Performance and Security headings, plus others from §16. Acceptance-criteria table; traceability (FR → design → file → test). | §14.2, §15, §16, §27.7 | **F3-4**, F2-4 | Noor (FR/NFR/acceptance), Shahoud (UC/diagram) | 7–9 pp |
| Ch5 System Design (5.1–5.8) | Layered architecture; components; interfaces and dependencies (contracts, API table, external services); ADRs with rejected alternatives; **design evolution** (proposal → now, with reasons); domain model; data design (ERD + data-dictionary excerpt); behaviour (state machine, verification sequence, activity/DFD); deployment diagram | §19–25, §29.2 | **F3-5**, **F3-6**, F2-5 | Saif (architecture, interfaces, ERD, state, sequence, deployment), Noor (domain model), Shahoud (activity, DFD) | 8–10 pp |
| Ch6 Iteration 1: Design and Implementation (6.1–6.10) | Objectives; selected UCs; design specifics; implementation per module (each owner: files, classes, functions, algorithm, trade-offs); algorithms (provenance §21.4, VR-1 §21.5, DSL whitelist); tools; **reproducible setup steps**; demonstration evidence (screenshots of the live slice + tag/URL; wireframes for unbuilt screens, labelled as such); outcome vs plan | §21, §26, §28, the code | **F3-7**, F2-3 | Each owner for their module; Saif collates | 6–9 pp |
| Ch7 Testing and Early Validation (`chapter8_testing.tex`) | Strategy (testing/evaluation/acceptance split); levels and techniques; test cases (IDs from App. B of this plan); results (CI run, counts, coverage); acceptance/validation (T2: mini-validation; T0/T1: what exists, stated honestly); edge and failure cases; defects and fixes (issue/PR links); status | §27, App. B | **F3-8**, F2-7 | Saif (+ each owner's cases) | 4–6 pp |
| Ch8 Project Management and Development Evidence (`chapter9_development_evidence.tex`) | Work completed and remaining; responsibilities; **each member's contribution** (honest, including history); repository evidence (branches, protections, PRs, CI/CD); milestones and commits (tags, log); **tools and tool-assisted development** (Form 13 table + AI-log summary, including GenAI help with planning and report language); external components and licences; top risks (§37); security and privacy (§24); limitations | §24, §28, §34, §37, §38 | **F3-8**, F2-6 | Saif (repo/CI), Shahoud (contribution, tools), Noor (risks) | 4–6 pp |
| Ch9 Remaining FYP Plan (`chapter10_fyp2_plan.tex`) | Remaining scope and modules; iterations 2–4; implementation, testing and deployment plans; timeline; final deliverables | §31–32, §35 | F3-3, F2-2 | Shahoud | 3–4 pp |
| Ch10 Conclusion | One page; no new claims | — | — | Shahoud | 1 p |
| App. A Proposal Action Register | Full register + evidence (links, screenshots) | §3 | F2-1 | Shahoud | — |
| App. B Detailed Requirements | Full FR/NFR tables, detailed UCs, traceability matrix | §15–16 | F3-4 | Noor | — |
| App. C Detailed Test Cases | Test-case table: inputs, expected, actual, status | App. B | F3-8 | Saif | — |
| App. D Repository and Contribution Evidence | Screenshots: branches/protections, PRs per member, Actions runs, tags, board; contribution table; the one-line note on the template fixes | §28 | F2-6 | Saif | — |
| App. E Additional Design Diagrams | Full-size diagrams | §25 | F3-5/6 | All | — |
| App. F Meeting and Progress Evidence | **Real meeting records only** (date, attendees, decisions, actions) from emails, calendars and minutes; milestone log | §39.5 | F2-2 | Shahoud | — |

**Handbook Table 1a items without a dedicated template section [M-H]: where they go**

| Table 1a item | Location in the template |
|---|---|
| Project Vision · DEI and ethical/legal statements | Ch1 (1.4, 1.11) |
| Research on related ideas/products | Ch2 |
| Use cases, use-case diagram, SSD | Ch4.1–4.3 (SSDs for UC-03/08/09 in 4.3 or App. E) |
| SRS | Ch4 + App. B |
| Test plan (levels, techniques) | Ch7.1–7.2 |
| Software Development Plan | Ch3.3–3.6 + Ch9 |
| Wireframes · UI screens | Ch6.9 (screens of the built slice); App. E (wireframes of remaining screens) |
| Structure, behaviour and DB design · algorithm design | Ch5 · Ch6.7 |
| Comments, naming conventions · static analysis · unit tests | Ch6.6 (standards) · Ch7.3–7.4 (static-analysis and unit-test results) |
| CI/CD | Ch8.5 |
| Deployment diagram | Ch5 (with the architecture) and Ch9.6 |
| System-level test suites | Ch7.3–7.4 |
| Configuration/setup and tool manual | Ch6.6 (setup steps, reproducibility) + full manuals in `docs/manuals/`, linked from App. D |

**Writing rules (rubric red flag "Generic/GenAI R&D text") [M-R]:**
1. **Own words, own evidence.** Each section is written by its owner from project evidence. Do not paste text from this plan or from the archived proposal-phase documents; both are heavily AI-drafted. GenAI may be used for language polishing only, and that use is disclosed in Ch8.7.
2. **Every claim points at evidence:** a paper (BibTeX key), a spike output file, a test ID, a commit/PR or the deployed URL.
3. **Paragraph-defense drill.** Before submission, each member picks two random paragraphs from another member's chapter. The owner explains each one without reading it.
4. **Report the system that exists.** Anything planned is labelled "planned (Iteration 2)". Never present wireframes as built screens.

**Build and submit [M-T][Rec]:**
- Compile `pdflatex main` → `bibtex main` → `pdflatex main` ×2 (template README) on MiKTeX/TeX Live.
- Sources live in the repo; each owner commits their own chapter files (per-member evidence).
- Optional CI action builds the PDF on PRs.
- Name the PDF and submit through the channel confirmed under D7.

### 30.6 Mid-1 Definition of Done (per track; objective)

**Common to all tracks:**
- [ ] Report compiled from the prescribed template: defects fixed, every chapter and appendix with real content, signatures, abstract 50–125 words. Submitted on time through the confirmed channel. [M-R F3-1][M-T][M-H]
- [ ] Panel Action Register A1–A6 in Ch3.2 + App. A, each row with action, status and a working evidence link; **opened during the session**. [M-R F2-1]
- [ ] Milestone log (planned vs actual) and an owner-assigned recovery plan with dates. [M-R F2-2]
- [ ] Full tool/GenAI disclosure (Form 13 + AI usage log), covering code, report language and planning assistance. [M-R F3-8 gate][M-H]
- [ ] Each member presents their own module and chapters, walks through their own code or artefact at function level, and answers "what happens if it is removed". [M-R F2-8, red flags]
- [ ] Change record C-01 presented for signature. [M-H C.5.3]
- [ ] Old novelty claims (§10.3) removed from the report and slides. [Rec]
- [ ] Tag on the demonstrated commit (`v0.1.0-mid1`; in T0, `v0.0.x` on the skeleton). [M-R F2-6 "tagged code"]

**T1 adds:**
- [ ] Live slice on **supervisor-chosen input**: fault run → outcome check FAIL → provenance H1 → CONFIRMED. Also H2 → REFUTED, clean run → no finding, provider down → graceful errored state. [M-R F2-3]
- [ ] ≥ 20 unit tests, including ≥ 6 edge/failure cases; CI green on `main`. [M-R F2-7][M-F]
- [ ] ≥ 2 code PRs authored by each member, each reviewed by another member. [M-R F2-6; counts are Rec]
- [ ] CI on GitHub Actions. CD to staging if ready; otherwise it is disclosed as an Iteration-2 item with a date. [M-F]
- [ ] Ch5/Ch6 diagrams and text match the tagged code. [M-R F2-5]

**T2 adds:**
- [ ] CD to Render staging with a health/sha check and Playwright smoke. [M-F][Rec]
- [ ] Findings inbox, graph view, Markdown export. [Rec]
- [ ] Mini-validation table (20 fault + 10 clean runs) in Ch7. [Rec: strengthens F2-7/F3-8]
- [ ] Coverage gate ≥ 70% on `granite_core`. [Rec]

**T0 adds:**
- [ ] Spike code run live (3b, 4b, 5), with an honest account of what is proposal-stage and what is new. [M-R F2-3 honesty]
- [ ] Repo hygiene + CI skeleton if time permits. [M-F]
- [ ] Three specific, weekly, demonstrable milestones agreed with the supervisor and recorded in the log. [M-R supervisory action]

*Counts are minimum evidence thresholds, not targets to inflate. Rubric red flags penalise artificial activity.*

### 30.7 Do NOT attempt before Mid-1

SDK, LangGraph/CrewAI adapters, Math Crew, Fault Lab batches, benchmark generation, ErrorProbe reproduction, LLM second opinion, fix suggestion, auth, check editor, PDF reports, any new research spike, rewriting the archived documents.

**Also do not:**
- create PRs or commits to inflate counts
- bulk-commit generated code a member cannot explain
- mark an item "Done" without a demonstrable artefact

### 30.8 Rubric red flags → countermeasures [M-R]

| Red flag (rubric) | How it could hit us | Countermeasure | Owner |
|---|---|---|---|
| Sudden code volumes | A slice built in days with AI help means a lot of code appearing between meetings | Small PRs (§26.3); each PR states what it does, the alternative rejected and what breaks if removed; owner-written tests; daily 10-minute walkthroughs; the restructure isolated as a pure-move PR | All |
| Stagnant prototype momentum | "What new core business logic has been added since the proposal defense?" | A "since-proposal delta" slide: new modules with file paths and tests, then run them live | Shahoud |
| Generic/GenAI R&D text | The existing document base and this plan are AI-drafted | Own-words rewrite; evidence-backed claims; paragraph-defense drill | Noor (Ch2), all |
| Uneven team contribution | History so far: Noor 45 commits, Shahoud 24, Saif 1 | Every member authors code PRs from their own account; `.mailmap`; an honest contribution table; quieter-member rehearsal of their own module | All |
| Dishonest milestone logging | Claiming items done that cannot be demonstrated | "Done" only with an artefact link; partial work logged as partial; every claimed milestone demonstrable live | Shahoud |
| Ignored proposal panel actions | Register missing or without evidence | Register opened in the session; each row has a live link | Shahoud |

### 30.9 Mid-1 day checklist

- **1 hour before:**
  - instance warmed, or local stack started and smoke-tested
  - recorded-mode fallback ready
  - provider key checked
- **Tabs open:**
  - Panel Action Register
  - GitHub (PR list, Actions, tags, board)
  - test command ready to run
  - each member's walkthrough files
- **Backups:**
  - compiled report PDF (offline copy)
  - the "since-proposal delta" slide
- **After the session:**
  - record the supervisor's actions in the register and meeting log
  - any Form 12 controlled change becomes an issue with an owner and date

---

## 31. FYP-1 Completion Plan (Iteration 2: Mid-1 → Final-1)

**Goal at Final-1** (handbook "integration readiness gate"):
- about 45–50% of the committed effort implemented
- the core scenario working end to end on **real inputs from two sources** (live run + import/SDK)
- the comparison **baseline measured**
- the deployment target live, with an install by a non-owner
- traceability populated
- the FYP-2 evaluation plan written

**If Mid-1 ran on Track T0 or T1:** Week 9 first finishes the Mid-1 cut items (CD to staging, findings inbox, graph view, Markdown export, mini-validation) and the milestones agreed at Mid-1. Only then does it start the Week-9 row below.

| Week | Shahoud (Workflows & Experience) | Noor (Investigation Engine) | Saif (Verification & Platform) | Shared / documentation |
|---|---|---|---|---|
| W9 | Trace import (F10) + validation report UI (S11) | Check editor backend (versioning, dry-run) | Experiment resume (FR-VER-05); 409 for non-replayable | Act on Mid-1 feedback; update Form 10. **Stakeholder interviews start (2).** |
| W10 | Faults FLT-HANDOFF, FLT-DROP; PII redaction (F18) | Check editor UI (S3); cycle bound (FR-ATT-03) | Fix suggestion (Repair Agent, atomic field) + fix experiment (F15) | Sessional-exam buffer: lighter week (verify the exam calendar) |
| W11 | **SDK v0.1 + LangGraph adapter** (Refund Desk on LangGraph) | Math Crew checks + metamorphic tests | Recovered run (F16) + regression-case export (F17) | Poster draft (Shahoud lead). Interviews (2 more). |
| W12 | Fault Lab batch UI/API (F12) | Evaluation harness v0: last-agent + LLM-judge baselines; metrics + CIs | Report export MD/PDF (F8); production release pipeline + approval | Supervisor approves poster |
| W13 | Benchmark v0 generation (≥ 120 runs, 20% clean, 2 workflows, 2 runtimes) | Run evaluation v0; natural-failure labelling (50, κ) | Performance measurement (NFR-01/02/03); SYS-ERR complete; axe pass | **Poster submission (W13)**. Usability pilot (3 peers). |
| W14 | Help/How-it-works (S16); SDK quickstart; UI polish from the pilot | Evaluation screen v0 (S14) | Non-owner install test (SYS-DEPLOY); deployment record; rollback test | **Report v2.0** drafted (iterations 1–2, FYP-2 plan, evaluation plan, test/deployment/rollback/handover plan draft, defect severity + release criteria) |
| W15 | Final-1 rehearsals | Final-1 rehearsals | Tag `v0.2.0` | **Final-1 + poster evaluation**. Report v2.0 submitted after supervisor approval. |

**Final-1 Must checklist:**
- F1–F7, F9, F10, F11, F12 (3 faults), F13 (LangGraph), F15, F16, F17, F18, F20 v0
- PDF export
- benchmark v0 + evaluation v0 *with* baselines measured
- SUS pilot
- 4–6 interviews documented
- deployment record with a non-owner install

**Explicitly deferred to FYP-2:**
- CrewAI adapter
- known-fix library
- OAuth/API keys
- benchmark ≥ 300
- ErrorProbe-lite
- full UAT

---

## 32. FYP-2 Roadmap (Iterations 3–4)

| Weeks | Focus | Deliverables | Owner leads |
|---|---|---|---|
| Winter break (optional) | Buffer only | Benchmark generation in the background on local machines; dependency updates | Shahoud |
| W1–2 | Act on the Final-1 register; CrewAI adapter (F14) | CrewAI Refund Desk; adapters documented | Shahoud |
| W1–3 | Evaluation v1 design frozen (pre-registration committed) | `research/eval/prereg-v1.md` | Noor |
| W2–4 | Known-fix library (F21); OAuth + reviewer identity (F22); SDK API keys + `/ingest/traces` | Releases `v0.3.x` | Saif |
| W3–5 | LLM second opinion (F19) + ErrorProbe-lite on a Who&When subset (≥ 30 cases, local 7–8B if hardware allows) | Hypothesis method `llm_opinion`; baseline table | Noor |
| W4–6 | Benchmark v1 ≥ 300 runs (3 runtimes × 2 workflows × 3 faults + 20% clean) + datasheet | `data/benchmark/v1/` + datasheet (scripts and results in `research/eval/`) | Shahoud |
| W5–7 | Evaluation v1: all metrics with CIs; ablations (N, M, guard, provenance vs LLM); NFR measurement; system test report; defect list by severity; security scan report; **UAT plan finalized** | Evaluation report v1; system test report | Noor (eval), Saif (system/NFR), Shahoud (UAT plan) |
| **W8** | **Mid-2 / Pre-Job-Fair** | `v0.5.0`. Updated poster. Updated report. Demo. No open Critical; every High dispositioned. | All |
| W9 | Re-evaluation window if needed; fixes | — | All |
| W9–11 | **UAT sessions (5–8 participants)**, consented recordings; fix the top issues | UAT report | Shahoud |
| W10–11 | Retention/delete (F23); hardening; job-fair 3-minute demo; Graduate Directory materials (CVs, FYP description, pictures, poster) | `v0.6.x` | All |
| **W12–14** | **Job Fair** | Booth demo (warm instance + offline fallback); one-page handout with QR code to the demo and repo | All |
| W13–14 | Final evaluation (benchmark v2 = 500 if Should achieved); limitations; handover package (source, build/run, dependencies, licences, credentials handling, known limits, future work); package + deployment diagrams; signed punch list | Final report v3 | All |
| **W15** | **Final-2** (supervisor) | `v1.0.0`. Final report signed by the supervisor. | All |
| W17–18 | Final deliverables to the committee | Report (soft copy) + full PPT + references + complete code + executable/readme/user manual. Plagiarism check passed. | Shahoud (collate) |

---

## 33. Final Product Roadmap (beyond the FYP; context only, not graded scope)

| Horizon | Item |
|---|---|
| v1.1 | OpenTelemetry (OTLP GenAI semantic conventions) ingestion; import from Langfuse/Phoenix exports |
| v1.2 | Check library for common agent failure classes (MAST-informed); GitHub Action `granite-verify` that replays regression cases in user CI |
| v1.3 | Multi-project teams, SSO, role separation (developer/reviewer) |
| v2 | Hosted "team edition" (optional), webhooks/Slack, cost-aware replay budgets, calibration of attribution scores |

---

## 34. Team Responsibilities

### 34.1 Primary ownership (continuity with the approved proposal, re-described around modules)

| Member | Ownership area (unchanged from proposal) | Product modules owned | CCP-relevant code they must defend (C.14.1) | Screens owned | Docs owned | Secondary (backup for) |
|---|---|---|---|---|---|---|
| **Shahoud Shahid** | Data / Benchmark → **Workflows, Data & Experience** | M1 Run, M2 Import/SDK/adapters, M8 Fault Lab + benchmark, LLM provider layer, PII redaction | Fault injection operators + ground-truth labelling; replay re-execution in the runner; SDK lineage capture | Shell/design system, S0, S4, S11, S13, S16 | Vision, use cases/SSDs, wireframes/UI, DFD/activity, user manual, UAT, poster, report editor | Noor (lineage) |
| **Muhammad Noor** | Diagnosis Engine → **Investigation Engine** | M3 Check (DSL), M4 Trace back, evaluation harness + baselines | DSL evaluator security; provenance attribution algorithm; metrics/CIs | S2, S3, S6, S7, S8, S14 | Literature/products, FR/NFR, domain model, algorithm design, evaluation chapter | Saif (verification) |
| **Saif Shahzad** | Platform → **Verification & Platform** | M5 Verify, M6 Review/Resolve, M7 Report, API/DB/jobs, CI/CD, deployment, security | Replay planner + VR-1 verdict + regression guard; state machine; release pipeline | S9, S10, S12, S15 | Architecture/component/layer, ERD/data dictionary, state/sequence, test plan, SDP, CI/CD, deployment, setup/tool manuals | Shahoud (runner) |

**Shared:** architecture decisions (ADRs need 2 approvals), integration testing, code reviews (round-robin: every PR is reviewed by a *different* member than last time), the ethics/privacy commitments, defense preparation. Every member must be able to demo the full J1 journey alone.

**Visibility safeguard (W6).** Saif's Mid-1 issues (#1–3, #13–17, #20) are on the critical path and visible in Actions. All members open their own PRs from their own GitHub accounts. If any member's work stalls for more than 1 week, the team raises it at the weekly supervisor meeting (handbook: supervisor reports non-functioning). We do not silently absorb the work.

**Report chapter ownership:** §30.5. Each owner commits their own chapter files and module code from their own GitHub account. `.mailmap` consolidates Noor's two commit identities.

### 34.2 RACI (R = responsible, A = accountable, C = consulted, I = informed)

| Deliverable | Shahoud | Noor | Saif |
|---|---|---|---|
| Runner, workflows, faults, SDK | R/A | C | C |
| Checks, attribution, evaluation | C | R/A | C |
| Verification, review, API/DB, CI/CD, deployment | C | C | R/A |
| UI consistency / design system | R/A | R | R |
| Report integration / formatting | R/A | R | R |
| Weekly supervisor minutes, Form 10, milestone log | R/A | I | I |
| Form 13 + AI log | R | R | R/A (collates per release) |
| Release tagging | C | C | R/A |

**CODEOWNERS:**
- `packages/granite_core/checks|attribution` → Noor
- `packages/granite_core/verification`, `apps/api`, `.github` → Saif
- `workflows/`, `packages/granite_sdk`, `apps/web/src/shell` → Shahoud

---

## 35. Detailed Timeline / Milestones

**Calendar mapping is an estimate (A1).** Confirm it on 5 Oct and update this table.

| Semester week | Scenario A dates (W1 = 17 Aug) | Scenario B dates (W1 = 24 Aug) | Milestone / focus |
|---|---|---|---|
| FYP-1 W5–7 | 14 Sep – 2 Oct | 21 Sep – 9 Oct | (Past) post-defense; feedback received |
| **W8** | **5–9 Oct** | **12–16 Oct** | **Mid-1** (supervisor; Forms 2 and 3 per the official rubric issued 5 Oct); track per §30.2; tag `v0.1.0-mid1` |
| W9 | 12–16 Oct | 19–23 Oct | Import, faults, check editor start; interviews |
| W10 | 19–23 Oct | 26–30 Oct | Redaction, fix suggestion, check editor UI |
| W11 | 26–30 Oct | 2–6 Nov | SDK + LangGraph; recovered run; poster draft |
| W12 | 2–6 Nov | 9–13 Nov | Fault Lab, evaluation v0 harness, PDF export |
| **W13** | **9–13 Nov** | **16–20 Nov** | **Poster submission**; benchmark v0; usability pilot |
| W14 | 16–20 Nov | 23–27 Nov | Report v2.0; non-owner install; evaluation screen |
| **W15** | **23–27 Nov** | **30 Nov – 4 Dec** | **FYP-1 Final + poster evaluation**, `v0.2.0` |
| FYP-2 W1–7 | Spring 2027 (dates announced at semester start) | — | CrewAI, OAuth, benchmark v1, evaluation v1, UAT plan |
| **FYP-2 W8** | — | — | **Mid-2 / Pre-Job-Fair** (Form 7), `v0.5.0` |
| W9 | — | — | Re-evaluation window (if needed) |
| **W12–14** | — | — | **Job Fair** |
| **W15** | — | — | **Final-2** (Forms 8/9), `v1.0.0` |
| **W17–18** | — | — | **Final deliverables** submission |

**Internal deadlines** (handbook: teams set internal deadlines ahead of external ones):
- code freeze 24 h before every evaluation
- report draft to the supervisor ≥ 5 days before every report deadline
- poster to the supervisor ≥ 5 days before W13
- mid report: a complete compiled draft 24 h before submission. Confirm the deadline and channel first (D7); assume it is due before the demo.

---

## 36. Definition of Done

### 36.1 Per issue/PR (always)

1. Acceptance criteria met and demonstrated.
2. Tests added: unit, plus integration if it crosses a boundary. Requirement marker present.
3. CI green. Coverage not reduced.
4. Reviewed and approved by a non-author.
5. Docs/diagrams updated if behaviour or design changed.
6. The PR's AI-assistance section is filled in.
7. Deployed to staging and smoke-tested (if user-facing).

### 36.2 Per module (first "done" milestone)

| Module | Done when |
|---|---|
| M1 Run | J1 launch works live and recorded; recorded mode is byte-identical ×3; provider-down → `errored` in ≤ 35 s; 5 step snapshots complete |
| M2 Import/SDK | 3 valid + 6 malformed fixtures behave; the LangGraph sample app produces a run via the SDK; quickstart followed by a non-owner in < 30 min |
| M3 Check | 15 malicious expressions rejected; ABSTAIN on missing fields; property tests pass; editor versioning works |
| M4 Trace back | H1 = true origin in ≥ 95% of 20 FLT-STALE runs; clean runs produce no hypotheses; metamorphic tests pass |
| M5 Verify | The 20-row VR-1 decision table passes; CONFIRMED and REFUTED demonstrated; regression guard test; partial-failure resume |
| M6 Review/Resolve | All legal/illegal transitions tested; audit log complete; recovered run and regression case produced for a confirmed fix |
| M7 Report | MD/JSON/PDF contain all §14.2-F7 elements; hashes verify against `/evidence/{id}` |
| M8 Lab/Eval | Benchmark generated with ground truth + clean controls; metrics with CIs; baselines computed on identical runs |

### 36.3 Per milestone

| Milestone | Objective completion criteria |
|---|---|
| **Mid-1** | §30.6: the common checklist plus the confirmed track's additions (T0/T1/T2) |
| **Final-1** | §31 Must checklist. Coverage ≥ 80% core. SYS-CORE/ERR/SEC/PERF/A11Y suites green. Baseline measured (numbers in report). Non-owner install recorded. Poster submitted and approved. Report v2.0 approved by the supervisor. `v0.2.0` tagged. |
| **Mid-2** | All Must features integrated across 2 frameworks + runner. Benchmark ≥ 300. Evaluation v1 with CIs + ≥ 3 ablations. NFRs measured vs targets. System test report. **0 open Critical**; every High dispositioned. UAT plan approved. `v0.5.0`. |
| **Job Fair** | 3-minute pitch rehearsed by every member. Offline fallback rehearsed. Handout + QR. Graduate Directory materials submitted. |
| **Final-2** | UAT done (5–8 participants, recordings, acceptance statements). Final evaluation + limitations. Handover package. Package/deployment diagrams. Final report signed. `v1.0.0`. Final deliverables submitted by W17–18. |

---

## 37. Risk Register

(Probability/Impact: H/M/L. Review weekly; the full register lives in `docs/registers/risk-register.md`.)

| ID | Category | Risk | P | I | Early warning sign | Mitigation | Contingency |
|---|---|---|---|---|---|---|---|
| K1 | Timeline/academic | Mid-1 within days with no product code and an empty report (two days lost after v1.0) | H | H | Date confirmation on 6 Oct | Track system (§30.2); report in parallel from D0; cut list pre-agreed | Track T0: honest status, spikes run live, recovery plan with three weekly milestones (the rubric's own remedy) |
| K2 | Technical | Replay of LLM steps is unstable, so verdicts come out INCONCLUSIVE too often | M | H | Control replays pass > 20% on fault runs | Temperature 0–0.2; JSON-constrained outputs; deterministic tool steps; report INCONCLUSIVE honestly | Increase N; use recorded cassettes for the demo; analyse instability as a finding |
| K3 | AI/ML | Small/free models are too weak (agents fail everywhere, so noise) | M | M | > 30% of clean runs fail checks | Prompt tuning; structured outputs; 7–8B locally if hardware allows; hosted free tier | Report the natural failure rate; restrict evaluation to deterministic faults |
| K4 | External | Free hosted LLM rate limits or terms change | M | M | 429s in staging; quota warnings | Recorded mode default on the public demo; rate limit; switch provider | Ollama via tunnel; recorded-only demo |
| K5 | Deployment | Render/Neon free tier changes or sleeps during the demo | M | H | Cold-start > 60 s; policy emails | Warm-up 10 min before; health checks | Laptop `docker compose`; fallback hosts (§29.6) |
| K6 | Novelty | Reviewer cites DoVer/Percival/LangSmith Engine: "already exists" | H | H | — | §10 honest comparison; contribution = protocol with controls + executable checks + evidence + self-host; DoVer cited as closest work | Present the ablation (single replay vs N + controls) as the measured delta |
| K7 | Novelty | A new paper or product does exactly our protocol before Final-2 | M | M | Literature check at each gate | 15-minute literature re-check per gate (kept from the proposal) | Reposition the delta as evaluation + product; report the overlap honestly |
| K8 | Scope | Feature creep (the old 20+ items return) | M | H | New items appear without a change record | §12 MoSCoW frozen; changes need C.5.3 records; Form 12 for supervisor requests | Descope ladder: S items → C → F |
| K9 | Team | Uneven contribution / a member inactive (W6) | M | H | No PRs from a member in a week | Visible per-owner issues; Friday owner demos; pairing | Raise with the supervisor; Form 11; reassign with a record |
| K10 | Academic | A member cannot explain AI-generated code | M | H | Struggles in Friday demos | L2 rules; owner writes tests; four-question drill | Simplify the code; re-implement the critical parts by hand |
| K11 | Integration | Runner ↔ replay interface mismatch (two owners) | M | H | Replay tests failing at a seam | Interface frozen Day 1 (§19.4); pair sessions | Saif temporarily owns both until stable |
| K12 | Data | tau-bench snapshot or licence issues; GAIA redistribution | L | M | — | MIT attribution; GAIA removed from git | Use synthetic retail data generated by our script |
| K13 | Data | Benchmark generation too slow on local hardware | M | M | < 20 runs/hour | Recorded tool steps; run overnight; hosted free tier for generation | Reduce to ≥ 120 (Final-1) / ≥ 300 (Mid-2) Must; 500 stays Should |
| K14 | Testing | Tests too shallow (happy path only) | M | M | Coverage OK but no failure tests | DoD requires failure tests; SYS-ERR suite; property/metamorphic tests | Dedicated "bug bash" day before each gate |
| K15 | Security | DSL sandbox escape | L | H | — | AST whitelist + timeouts + attack set + Bandit | Disable custom checks on the public demo (seeded only) |
| K16 | Privacy | Real PII uploaded to the public demo | L | H | — | Banner "synthetic data only"; redaction; upload limit; retention | Delete endpoint; purge job |
| K17 | CI/CD | Actions minutes exhausted (private repo) | L | M | Usage > 70% mid-month | Concurrency cancel; path filters; Student Pack (3,000 min) | Make the repo public (D2) |
| K18 | Documentation | Report diverges from the implemented system | M | H | Diagrams not updated in PRs | Diagrams as code in the same PRs; traceability generated from tests | Pre-gate audit day comparing report vs code |
| K19 | Academic | Handbook process items missed (Form 10/13, minutes, poster format) | M | M | Missing artefacts at T-5 days | §40 matrix reviewed weekly | Emergency completion; disclose late items |
| K20 | Stakeholders | Cannot recruit UAT participants or interviewees | M | M | < 3 confirmed by FYP-1 W11 | Start interviews W9; use alumni/AI-course networks | Declared proxies (classmates in AI courses) with stated limitations (C.13.1) |
| K21 | Timeline | Exams/other courses reduce capacity | H | M | Velocity drops | Lighter weeks planned (W10); buffer in each iteration | Cut S items |
| K22 | Repo | The in-progress rebase or history mess loses work | M | M | `git status` shows a rebase | Back up; resolve on Day 0; protected branches | Restore from `origin/noor` + backup |
| K23 | Evaluation | Evaluation results look weak (accuracy below targets) | M | M | v0 numbers below target | Targets are reporting goals, not claims; analyse failures | Report honestly with error analysis (the handbook values this) |
| K24 | Usability | Evaluators still find the UI unclear | M | H | The pilot SUS < 68 or task failures | Stepper, plain copy, Help page, pilot at W13 | Iterate on the top 3 issues before Final-1 |
| K25 | Report | Template rendering defects (duplicate contents, undefined macros, broken longtable) cost F3-1 format marks | M | M | Raw "p0.06p0.28…" text or blank names in the PDF | Apply the three fixes on D0; compile after every merge | Ask the supervisor/coordinator for a corrected template |
| K26 | Academic (red flag) | "Sudden code volumes": crunch-built, AI-assisted code the owner cannot explain line by line | H | H | PRs over about 300 lines; owner hesitates in a daily walkthrough | Small PRs, owner-written tests, a "what if removed" note, daily walkthroughs | Cut the code to what is understood; accept the rubric's re-demo session before Final-1 |
| K27 | Academic (red flag) | R&D chapter judged generic/GenAI text → mandatory rewrite | M | H | A member cannot explain a paragraph without reading it | Own-words rewrite; paragraph-defense drill; project-specific evidence | Rewrite before Final-1; record in the register |
| K28 | Academic (red flag) | Uneven contribution visible in the repo and the Q&A → Form 11 | H | H | One member answers for others; no PRs from a member | Each member owns a code module and chapters; one-to-one rehearsal for the quieter member | The rubric's supervisor action: a two-week individual milestone |
| K29 | Demo | Recorded LLM mode looks like hardcoded scaffolding (F2-3 "Developing" band) | M | M | — | Live mode by default; the supervisor chooses the input; show that changing a check tolerance changes the result | Present recorded mode as a disclosed fallback; show a live run afterwards |
| K30 | Logistics | Report due before the demo, or through an unknown channel | M | M | — | Confirm D7 today; plan the report as due first | Submit the best compiled version on time (the handbook penalises late submissions) |

---

## 38. Cost-Free Development Strategy

| Need | Free choice | Limit to watch (verify) | Fallback |
|---|---|---|---|
| Source + CI/CD | GitHub (private) + Actions; Student Developer Pack (GitHub Pro) | 2,000 min/month (Free) or 3,000 (Pro); private package storage | Public repo (unlimited minutes, CodeQL) |
| App hosting | Render free web services ×2 | Sleeps after 15 min; ~1 min wake; 750 h/workspace/month | Koyeb free; Azure for Students; laptop + Cloudflare Tunnel |
| Database | Neon free Postgres (branches for staging/main) | Storage/compute caps | Supabase free; local Postgres |
| Container registry | GHCR | Private storage quota | Render builds from the Dockerfile directly |
| LLM (public demo) | Groq or Google AI Studio free tier (OpenAI-compatible) | Rate limits / daily tokens; terms | The other provider → Ollama → recorded |
| LLM (self-host, dev, evaluation) | Ollama: `llama3.2:3b`, `qwen2.5:3b/7b`, `llama3.1:8b` | Laptop RAM/CPU speed | Recorded cassettes |
| Datasets | tau-bench retail (MIT), GSM8K (MIT), Who&When | Licence attribution | Synthetic retail generator |
| Design/diagrams | Penpot (OSS) / Figma Education; draw.io; Mermaid; PlantUML | — | — |
| Docs/report | Prescribed LaTeX template; MiKTeX (already on the team laptop) or TeX Live; optional CI PDF build | — | Overleaf free (check the free plan's collaborator limit) |
| Testing/quality | pytest, Vitest, Playwright, axe-core, Ruff, mypy, Bandit, pip-audit, gitleaks, import-linter | — | — |
| Project management | GitHub Projects, Issues, Milestones | — | — |
| Poster | Inkscape/GIMP (free) **or** Photoshop/Corel (handbook-recommended; university labs) | Handbook: other tools = group arranges printing | Decision D3 |

**Total committed recurring spend: $0** (consistent with R37). Any spend proposal needs a change record and supervisor approval (handbook: purchase requests via the committee).

---

## 39. Documentation & FYP Report Mapping

### 39.1 Report structures by milestone

| Report | Structure to follow | Status (6 Oct) |
|---|---|---|
| FYP-1 Mid report (v1.0) | **The prescribed chapter-wise LaTeX template.** Chapter map, fixes and owners are in §30.5. [M-T][M-R F3-1] | Template received 6 Oct; 0% filled |
| FYP-1 Final report (v2.0) | Handbook §9 contents (incl. Iteration 1, Iteration 2, Implementation Details, User Manual) **inside whichever template the coordinator issues for Final-1**. Until one is issued: extend the Mid template (keep Ch1–5; Ch6 becomes "Iteration 1"; add "Iteration 2", "Implementation Details" and "User Manual"; refresh Ch7–9). [M-H §9, Table 1a] | Decide by W12 (D5) |
| FYP-2 reports | Handbook §9 + Table 1b items (package and deployment diagrams, GitHub, setup and tool manual) + Form 9 items (traceability, evaluation, limitations, individual accounts) [M-H] | FYP-2 |

### 39.2 Handbook §9 contents → our sources (Final-1 and FYP-2 reports; the Mid map is in §30.5)

| Handbook §9 section | Our content source | Report version |
|---|---|---|
| 1 Introduction | §1, §5 | v1.0 → |
| 2 Research on existing ideas/products | §10 + updated literature/product comparisons + research-to-decision table | v1.0 → |
| 3 Project Vision: 3.1 Problem · 3.2 Business opportunity · 3.3 Objectives · 3.4 Scope · 3.5 Constraints · 3.6 Stakeholders (summary, goals and problems) · 3.7 DEI and ethical/legal | §4–7, §11, §43 (opportunity), §24 (ethics), the proposal's DEI | v1.0 → |
| 4 SRS: 4.1 List of features · 4.2 FRs · 4.3 NFRs | §11–12, §15, §16 (+ use cases, SSDs, I/O cards §14.2) | v1.0 → |
| 5 Iteration plan | §26.1, §35 | v1.0 → |
| 6 Iteration 1 (all Table 1a artefacts) | §19–29 + implemented slice | v1.0 → |
| 7 Iteration 2 | Final-1 work | v2.0 |
| 8 Implementation details (algorithms and procedures) | §21.4, §21.5, DSL evaluator, replay planner | v1.0 (partial) → v2.0 |
| 9 User manual | `docs/manuals/user-manual.md` | v2.0 → final |
| References / Appendices | Bibliography; registers; test reports; UAT; evaluation | All |

### 39.3 Formatting: prescribed template vs handbook §8 (contradiction resolved)

| Aspect | Template (`fast-nuces-bs.cls` + `main.tex`) | Handbook §8 | Rule we follow |
|---|---|---|---|
| Body font and size | Times (`mathptmx`), 12 pt | Times New Roman 11 | Template [M-T] |
| Headings | Class-defined bold small-caps chapter heads | Arial 16 / 14 / 13 | Template |
| Margins | 3 cm left/right, 2.5 cm top/bottom | T 1.5", B 1.0", L 2.0", R 1.0" | Template |
| Line spacing | 1.15 | 1.5 | Template |
| Page numbers | Footer centre; roman front matter, arabic body | Top right; roman front matter | Template |
| Running heads | Chapter (even) / section (odd) | Report title (odd) / chapter (even) | Template |
| Front-matter order | Submission → anti-plagiarism → authors' declaration → abstract → acknowledgments → executive summary → contents/figures/tables → abbreviations | Title → blank → declarations → abstract → acknowledgments → executive summary → contents | Same order; keep |
| Abstract length | Commented legacy note: 150–200 words (not rendered) | 50–125 words | Handbook [M-H] (D6) |
| References | IEEEtran BibTeX | Bibliography/endnote guidance | Template (IEEEtran) |

**Why the template wins for Mid-1:**
- The official rubric grades "prescribed template followed" (Form 3 C1).
- The handbook itself says a "specific and tailored format… is suggested by a supervisor" (§9).
- Ask the supervisor (D5) whether §8 applies at Final-1.
- Do **not** restyle the class on our own initiative.
- Fix only the three rendering defects listed in §30.5.

### 39.4 Report build pipeline [Rec]

- **Sources:** `docs/report/` (the template tree). Each chapter owner edits their own `chapters/*.tex` through PRs, which also serves as per-member commit evidence (F2-6).
- **Build:** `pdflatex main` → `bibtex main` → `pdflatex main` ×2, per the template README. MiKTeX is already on the team laptop; TeX Live also works.
- **Optional CI:** a GitHub Action compiles the PDF on PRs that touch `docs/report/` and uploads it as an artefact.
- **Diagrams:** draw.io, PlantUML or Mermaid sources, with their PDF/PNG exports, in `docs/diagrams/`; the report references them (`\graphicspath`). TikZ-UML (bundled) only if someone is already fluent.
- **BibTeX:** replace the placeholder `references.bib` with entries for:
  - Who&When (ICML 2025)
  - AgenTracer (ICLR 2026)
  - SDBL (AAAI 2026)
  - TraceElephant
  - ErrorProbe (ACL 2026 Findings)
  - AgentAsk (ACL 2026)
  - PROTEA (ACL 2026 Demo)
  - DoVer (arXiv preprint 2512.06749, 2026)
  - tau-bench and GSM8K
  - product documentation pages, with access dates

### 39.5 Registers kept current (in `docs/registers/`)

- Form 10 Panel Action Register
- change log (C-01…)
- Form 13 disclosure sheet
- AI usage log (per PR; supervisor countersigns before each evaluation)
- risk register (§37)
- dependency and licence register
- milestone log (planned vs actual, delays + recovery)
- deployment record
- defect list
- meeting minutes and supervisor tracking form

---

## 40. Handbook Compliance Matrix (traceability matrix #1)

*Handbook requirement → FYP phase → Granite feature/deliverable → responsible member → evidence → deadline → completion status (as of 2026-10-06).* Status values: Done · Partial · Not started · Ongoing · Future · N/A.

**Owners:** Sh = Shahoud · No = Noor · Sa = Saif · All = all three.

**Deadlines:**
- W8 = Mid-1
- W13 = poster
- W15 = Final-1
- F2-W8 = Mid-2
- F2-W12 = Job Fair
- F2-W15 = Final-2
- F2-W17 = final deliverables

### 40.0 Official Mid-1 rubric (Forms 2 and 3, issued 5 Oct 2026) [M-R]

| ID | Criterion (CLO, marks) | Evidence we will show | Owner | Status (6 Oct) |
|---|---|---|---|---|
| RB-F2-1 | Previous proposal actions addressed (CLO6, 10) | Register A1–A6 with live links, opened in the session | Sh | Not started |
| RB-F2-2 | Iteration plan and work-breakdown progress (CLO2, 10) | Milestone log, board, recovery plan with owners and dates | Sh | Not started |
| RB-F2-3 | Live prototype with core module (CLO4, 25) | Track slice live, including edge/failure cases | All | Not started |
| RB-F2-4 | Requirements and acceptance-criteria quality (CLO2, 10) | FR/NFR ↔ acceptance ↔ test IDs | No | Partial (old SRS) |
| RB-F2-5 | Design artefacts and design evolution (CLO3, 15) | Diagrams matching the tagged code + evolution table | Sa | Not started |
| RB-F2-6 | Repository, milestone and member evidence (CLO6, 10) | Tags, per-member PRs, board, CI runs | Sa | Partial (history uneven) |
| RB-F2-7 | Testing and early validation (CLO4, 10) | Executed tests, edge/failure case, CI | Sa | Not started |
| RB-F2-8 | Presentation, Q&A, team and tool ownership (CLO5, 10) | Each member's walkthrough + their Form 13 rows | All | Not started |
| RB-F3-1 | Report format and artefacts (CLO2, 5) | Filled template, defects fixed, signatures | Sh | Not started (template empty) |
| RB-F3-2 | Problem formulation, R&D and gap (CLO1, 15) | Ch2: own-words synthesis incl. DoVer and products; CCP | No | Partial (material exists; must be rewritten) |
| RB-F3-3 | Vision, scope and success criteria (CLO2, 10) | Ch1 + Scope Table + proposal mapping + C-01 | Sh | Partial |
| RB-F3-4 | Requirements and acceptance (CLO2, 15) | Ch4: numbered FRs/NFRs + acceptance checks | No | Partial |
| RB-F3-5 | Architecture and component/interface design (CLO3, 15) | Ch5: layers, components, contracts, ADRs | Sa | Partial (designed in this plan, not yet in the report) |
| RB-F3-6 | Data/process/behaviour design (CLO3, 10) | ERD, state, sequence, activity/DFD, each explained | Sa/Sh | Partial |
| RB-F3-7 | Implementation documentation (CLO4, 15) | Ch6: per-owner files, classes, algorithms + setup | All | Not started |
| RB-F3-8 | Testing plan and tool/risk disclosure (CLO5, 15) | Ch7 + Ch8.7–8.10 + Form 13 + AI log | Sa/Sh | Partial |
| RB-RF | Six red flags: sudden code volume, stagnant prototype, generic GenAI R&D, uneven contribution, dishonest milestone log, ignored panel actions | §30.8 countermeasures | All | Ongoing |

### 40.1 Process and cross-cutting

| ID | Handbook requirement (source) | Phase | Granite deliverable | Owner | Evidence | Deadline | Status |
|---|---|---|---|---|---|---|---|
| R-01 | Group of 2–3 registered; title, 8–10 features, SDG, supervisor, category/tech, CCP evidence (§2 Step 1) | Registration | `FYP_Registration_Form_Answers.md`; features updated via C-01 | Sh | Form copy | Done (feature list to update) | Partial |
| R-02 | Registered on Flex (§2 note) | Registration | — | All | Flex screenshot | Done (confirm) | Done* |
| R-03 | Proposal defense with POC-lite (Form 1) | Proposal | Defense deck + spikes | All | Approval decision | 11 Sep 2026 | Done |
| R-04 | Weekly supervisor meeting; supervisor tracking form; attendance (§3, §2) | All | `docs/meetings/` minutes; tracking form | Sh | Signed minutes | Weekly | Not started → start W8 |
| R-05 | Iterative process; ≥ 2 iterations in FYP-1; each a working, demonstrable product (§5.1–5.2) | FYP-1 | It-1 (`v0.1.0`), It-2 (`v0.2.0`) | All | Tags + demos | W8, W15 | Not started |
| R-06 | Changes after approval recorded and approved; no silent change (C.5.3) | All | Change record C-01 (+ later) | Sh | Signed record | W8 | Not started |
| R-07 | Form 12 controlled change (if issued at Mid-1/Final-1/Mid-2) answered with the stated evidence | FYP-1/2 | Issue + PR linked to Form 12 | Owner named | Acceptance test result | As issued | N/A yet |
| R-08 | Document control block; versioned docs, draft → approved (C.5.1) | All | Block on every doc; tags | All | Doc headers | W8 | Partial |
| R-09 | Form 10 Panel Action Register updated before every evaluation (App. B) | All | `docs/registers/form-10-panel-actions.md` (A1–A6 + later) | Sh | Register with evidence links | W8 and each gate | Not started |
| R-10 | Form 13 disclosure updated before every evaluation (App. B) | All | Updated Form 13 (§21.1 classes, new services) | Sa | Signed sheet | W8 and each gate | Partial |
| R-11 | AI usage log maintained, countersigned by the supervisor (C.8.4) | All | Per-PR log entries → `docs/registers/ai-usage-log.md` | All (Sa collates) | Countersigned log | Each gate | Partial |
| R-12 | Stream declared (C.1.1) | Proposal | Stream A | — | Plan | Done | Done |
| R-13 | SDG/thematic alignment, with the boundary stated (C.1.3) | Proposal+ | SDG 9.5 paragraph | Sh | Report 3.x | W8 | Done |
| R-14 | CCP central; characteristics evidenced (C.3) | All | §5 table; #6 strengthened by interviews | No | Report + interview notes | W8 (text), W12 (#6) | Partial |
| R-15 | Contribution statement in the C.4 form; Stream-A delta sentence (C.18.2) | All | §10.5 | No | Report 2/3 | W8 | Partial (needs C-01) |
| R-16 | Product, prior-FYP and workflow comparison, structural (C.10) | All | §10.1 + prior-FYP analysis | No | Report Ch. 2 | W8 | Partial (update) |
| R-17 | Research-to-decision table (C.11) | All | Updated table incl. DoVer → controls decision | No | Report Ch. 2 | W8 | Partial |
| R-18 | External components classified; nothing core-replacement (C.14) | All | §21.1, Form 13 | Sa | Form 13 | W8 | Partial |
| R-19 | AI-assisted development level named (L2) (C.8) | All | Plan header, SDP | — | Report | Done | Done |
| R-20 | Each member meets the four C.14.1 abilities for CCP-relevant work | All | Friday owner demos; walkthrough prep §41.3 | All | Demo notes, Q&A | W8+ | Ongoing |
| R-21 | No proprietary data/keys in repos (App. B industry rule; good practice) | All | gitleaks; `.env.example` | Sa | CI logs | W8 | Not started |
| R-22 | Licensing/copyright compliance for datasets/code (policy note) | All | Licence register; GAIA removed from git | Sh | Register | W8 | Partial |
| R-23 | Form 6 Startup evaluation (optional) | FYP-1 | §43 if the team opts in | Sh | Form | Optional (decide W12) | N/A |

### 40.2 Mid-1 (Week 8): Table 1a, Forms 2/3, Gate 2/3

| ID | Requirement | Granite deliverable | Owner | Evidence | Status |
|---|---|---|---|---|---|
| R-M1-01 | Report v1.0: Project Vision | Report Ch. 3 (§4–7) | Sh | Report | Partial (rewrite) |
| R-M1-02 | Research on related/existing ideas/products | Report Ch. 2 (§10) | No | Report | Partial (update) |
| R-M1-03 | Use cases + use case diagram | §15.1, new diagram | Sh | Report + SVG | Partial (redo) |
| R-M1-04 | SSD | SSDs for UC-03/08/09 | Sh | Report | Partial (redo) |
| R-M1-05 | SRS: FRs/NFRs uniquely identified, testable, prioritised; ≥ 1 measurable NFR per quality attribute (Gate 2) | §15–16 | No (+Sh) | Report Ch. 4 | Partial (rewrite) |
| R-M1-06 | Test Plan: levels, techniques | §27 | Sa | Report Ch. 5 | Partial (rewrite) |
| R-M1-07 | Software Development Plan (fix Mid-1 = W8) | §26, §28, §35 | Sa | Report Ch. 5 | Partial |
| R-M1-08 | Wireframes | From §18 (Penpot) | Sh | Report | Partial (replace) |
| R-M1-09 | UI screens | Screenshots of the deployed slice | Sh (+owners) | Report + live | Not started |
| R-M1-10 | DEI statement | Updated from the proposal (access equity; accessibility; English-only limit) | Sh | Report 3.7 | Done (update) |
| R-M1-11 | Ethical/legal statements | §24 ethics + licences + consent | Sh | Report 3.7 | Done (update) |
| R-M1-12 | Structure design: domain/class, component, layer, (structure chart) | §25 | No/Sa | Report Ch. 6 | Not started |
| R-M1-13 | Behaviour design: flow, DFD, data dictionary, activity, state machine, sequence, interaction overview | §25 | Sh/Sa/No | Report Ch. 6 | Not started |
| R-M1-14 | Schema design / ER diagram | §22 | Sa | Report + migrations | Partial (redo) |
| R-M1-15 | Data structure and algorithm design | §21.4–21.5 + DSL design | No/Sa | Report Ch. 6/8 | Not started |
| R-M1-16 | Development: comments, naming conventions | §26.2 enforced | All | Code + lint config | Not started |
| R-M1-17 | Static analysis of code | Ruff/mypy/Bandit/ESLint in CI; report excerpt | Sa | CI logs | Not started |
| R-M1-18 | Unit test suites / test cases | ≥ 30 tests incl. failure cases | All | Coverage report | Not started |
| R-M1-19 | Maintenance: CI/CD (GitHub) | §28 pipelines | Sa | Actions history | Not started |
| R-M1-20 | Deployment diagram | §29.2 | Sa | Report | Partial (redo) |
| R-M1-21 | System-level test suites / test cases (validation and testing) | SYS-CORE, SYS-ERR (3) | Sh/Sa | Playwright report | Not started |
| R-M1-22 | Configuration/setup manual and tool manual | `docs/manuals/setup-manual.md`, `tool-manual.md` | Sa | Manuals | Not started |
| R-M1-23 | Working code + demonstration (live module beyond POC-lite) | Mid-1 slice (§30) | All | Live demo, tag `v0.1.0` | Not started |
| R-M1-24 | Faculty: core module + CI/CD on the live interface | Same + staging deploy pipeline | All | URL + Actions | Not started |
| R-M1-25 | Mid-term report (soft form) submitted, in the prescribed template | Filled LaTeX template (§30.5) → PDF | Sh | Submission receipt | Not started (template received 6 Oct, 0% filled) |
| R-M1-26 | Form 2: previous proposal actions addressed | Form 10 (A1–A6) | Sh | Register | Not started |
| R-M1-27 | Form 2: milestone log honest; recovery plan for misses | Milestone log | Sh | Log | Not started |
| R-M1-28 | Stage 1: code walkthrough at file/function level by each member | §41.3 drill | All | Supervisor observation | Not started |
| R-M1-29 | Stage 1: ≥ 1 module validated beyond the happy path | Clean run, REFUTED verdict, provider-down, ABSTAIN tests | All | Tests + demo | Not started |
| R-M1-30 | Form 2: repository evidence: tagged code, commit timeline, task log, member ownership | Protected branches, PRs, Project board, CODEOWNERS | Sa | GitHub | Partial |
| R-M1-31 | Gate 2: requirements baselined with stakeholders | SRS v1 + interview plan (interviews by W12) | Sh | SRS + interview log | Partial |
| R-M1-32 | Gate 3: architecture justified vs alternatives; decisions recorded | ADR-001…010 | Sa (+owners) | `docs/adr/` | Not started |
| R-M1-33 | Gate 2/3: data, access, licences, ethical clearance secured | Licence register; consent template; synthetic-only demo policy | Sh | Register | Partial |
| R-M1-34 | SDS covering components, data, interfaces, security, deployment, failure handling | Report Ch. 6 (§19–24, §29) | Sa | Report | Partial (redo) |
| R-M1-35 | Traceability matrix opened | Generated matrix (§27.7) | No | CI artefact | Partial (old) |
| R-M1-36 | API and third-party dependency register started | `dependency-register.md` | Sa | Register | Not started |
| R-M1-37 | Form 3: implementation documentation of the completed module (setup, files/classes/functions, decisions) | Report Ch. 7 | All | Report | Not started |
| R-M1-38 | Form 3: risk/security/privacy and limitations documented | §24, §37 | Sa | Report | Partial |
| R-M1-39 | Prescribed template followed; rendering defects fixed; signatures on Students' Submission (rubric F3-1) [M-R][M-T] | §30.5 | Sh | Compiled PDF | Not started |
| R-M1-40 | Scope Table, consistent with the proposal (rubric F3-3 and its red-flag gate) [M-R] | Report §1.6–1.7 + mapping §11.3 + C-01 | Sh | Report | Not started |
| R-M1-41 | Proposal Action Register with live evidence links, opened during the session (rubric F2-1 and red flag) [M-R] | Report §3.2 + App. A | Sh | Register | Not started |
| R-M1-42 | Meeting and progress evidence; real records only (template App. F) [M-T] | Minutes, emails, calendar entries | Sh | App. F | Not started |
| R-M1-43 | Bibliography (IEEEtran BibTeX): the 7 core papers, DoVer and the cited products [M-T] | `references.bib` | No | Report | Not started |

### 40.3 FYP-1 Final (Week 15) and poster (Week 13)

| ID | Requirement | Granite deliverable | Owner | Evidence | Deadline | Status |
|---|---|---|---|---|---|---|
| R-F1-01 | About 45% implementation; ≥ 2 iterations (§5, Stage 2) | §31 Must list | All | Live demo, burn-up chart | W15 | Not started |
| R-F1-02 | Report v2.0 with corrections + subsequent iterations + FYP-2 plan (Table 1a, Step 5) | Report v2.0 | Sh | Approved PDF | W15 | Not started |
| R-F1-03 | Demo works beyond the happy path; stable (Form 4) | SYS suites green | All | Demo + test report | W15 | Not started |
| R-F1-04 | Testing evidence: inputs, expected/actual, bugs/fixes, edge cases (Form 5) | Test report + defect list | Sa | Report appendix | W15 | Not started |
| R-F1-05 | Code modular, readable, buildable without the original developer (Stage 2, Form 4) | Non-owner install (SYS-DEPLOY) | Sa | Install record | W14 | Not started |
| R-F1-06 | FYP-2 evaluation plan: baseline, user testing, benchmark, metrics (Stage 2, Form 5) | §27.5–27.6 | No | Report | W15 | Partial |
| R-F1-07 | Gate: comparison baseline measured | Evaluation v0 (last-agent, LLM-judge) | No | Metrics table | W14 | Not started |
| R-F1-08 | Gate: deployment target selected; first deployment attempted | Render/Neon production + record | Sa | Deployment record | W8 (staging) / W15 | Not started |
| R-F1-09 | Gate: traceability matrix populated (requirement → design → test) | Generated matrix | No | Report appendix | W15 | Not started |
| R-F1-10 | Gate: test, deployment, rollback and handover plan drafted; defect severity definitions; release criteria | §27.7, §29.4 + handover draft | Sa | Report | W15 | Not started |
| R-F1-11 | Gate: timeline revised vs actual; scope changes processed | Milestone log + change records | Sh | Registers | W15 | Not started |
| R-F1-12 | Design evolution justified; artefacts updated (Form 4/5) | Diagram diffs in git; change notes | All | Report "design evolution" section | W15 | Not started |
| R-F1-13 | Responsible tool/API/GenAI ownership defense (Form 4/5) | Form 13 + AI log + walkthroughs | All | Q&A | W15 | Partial |
| R-F1-14 | Poster submitted W13, after supervisor approval: 22.5"×34.5" portrait; title/names/supervisor top-left; goals top-right; plan/deliverables bottom; large font; original PSD/Corel + JPEG (§7) | Poster | Sh (+all) | Files + approval | W13 | Not started |
| R-F1-15 | Poster evaluation (Form 4: 10 marks) | Displayed poster | All | — | W15 | Not started |
| R-F1-16 | Report format rules (§8), or the supervisor-prescribed template where one is issued (D5) | LaTeX template; §8 applied only if the supervisor confirms it | Sh | Formatted report | W8 / W15 | Not started |
| R-F1-17 | Report approved by the supervisor before submission; on-time submission (Step 5–6; late penalty) | Internal deadline T-5 days | Sh | Approval email | W15 | Process |

### 40.4 FYP-2 and final submission

| ID | Requirement | Granite deliverable | Owner | Evidence | Deadline | Status |
|---|---|---|---|---|---|---|
| R-F2-01 | FYP-2 registered consecutively (no frozen semester) | — | All | Flex | F2-W1 | Future |
| R-M2-01 | Integrated live system; modules connected; no video-only demo (Form 7) | `v0.5.0` | All | Live demo | F2-W8 | Future |
| R-M2-02 | Realistic scenarios; graceful failure; honest limitations (Stage 3) | SYS-ERR; limitations list | All | Demo | F2-W8 | Future |
| R-M2-03 | Integration tests; known bugs + mitigation; preliminary baseline comparison (Stage 3, Form 7) | Evaluation v1; defect list | No/Sa | Reports | F2-W8 | Future |
| R-M2-04 | Gate 4: system test report; defect list by severity, no open Critical, Highs dispositioned; NFRs measured vs targets; deployment and rollback plans approved and rehearsed; edge cases exercised | System test report; rollback drill | Sa | Report + drill log | F2-W8 | Future |
| R-M2-05 | UAT plan exists by FYP-2 Mid (C.13.1) | §27.6 finalized | Sh | Plan | F2-W8 | Future |
| R-M2-06 | Updated poster, demos, updated report (Table 1b) | Poster v2, report v2.5 | Sh | Files | F2-W8 | Future |
| R-JF-01 | Job fair: working system by W12; CVs, FYP description, pictures, posters for the Graduate Directory (Table 1b) | Booth kit | All | Submissions | F2-W12 | Future |
| R-F2F-01 | Final-2: works as at Mid-2 + improvements; no regression (Stage 4, Form 8) | `v1.0.0`; regression suite | All | Demo | F2-W15 | Future |
| R-F2F-02 | Testing, validation and evaluation vs baselines/success criteria (Form 8/9) | Final evaluation report | No | Report | F2-W15 | Future |
| R-F2F-03 | UAT evidence: method, participants, tasks/results, issues, acceptance outcome, consented recording (C.13.1) | UAT report + videos | Sh | Report | F2-W15 | Future |
| R-F2F-04 | Deployment evidence; operated by someone outside the team (C.1.2, Gate 5) | Deployment record; outsider install | Sa | Record | F2-W15 | Future |
| R-F2F-05 | Package and deployment diagrams; GitHub; config/setup and tool manual (Table 1b) | Report + manuals | Sa | Report | F2-W15 | Future |
| R-F2F-06 | Handover package: source, build/run, dependencies, licences, credentials handling, known limitations, future work; signed punch list; acceptance matrix signed off (Gate 5) | `HANDOVER.md` + punch list | Sa | Signed docs | F2-W15 | Future |
| R-F2F-07 | Final report faithful; traceability; substantive limitations; individual reflective accounts (Stage 4, Form 9) | Final report | All | Report | F2-W15 | Future |
| R-FD-01 | Final deliverables: report soft copy + complete PPT; references; complete code; executable + readme (sw/hw requirements, run steps) / user manual (§5 FYP-2 item 7) | Submission bundle | Sh | Receipt | F2-W17/18 | Future |
| R-FD-02 | Plagiarism check passed; supervisor approval; on time (Step 10–11; rule 7) | Similarity report | Sh | Report | F2-W17 | Future |

---

## 41. Evaluation / Defense Preparation

### 41.1 Rehearsal cadence

- **Each gate:** 2 full rehearsals (T-3 and T-1 days) with a timer and a mock Q&A: one member plays the panel, using §41.2 and the handbook's Sample Evaluator Question Bank.
- **Every Friday:** owner demos.
- **T-1:** code freeze; warm-up checklist printed.

### 41.2 New question bank (answers ≤ 30 s; rehearse aloud)

| Question | Answer |
|---|---|
| "DoVer already re-executes from an intervention point. What's yours?" | "DoVer showed intervention works as a research method, with three runs per intervention. We make it an operator protocol that is robust to nondeterminism: N intervention replays *plus control replays* and a pre-registered verdict rule, so a lucky re-run can't confirm a wrong cause. Every replay is stored as evidence. We measure the difference: single-replay vs our protocol, on labelled faults." |
| "LangSmith Engine / Percival already find root causes." | "They do, mainly with LLM judgement inside their SaaS, and they don't publish accuracy. Our core findings need no LLM: executable checks and value provenance. We publish accuracy and false-alarm rates on a labelled benchmark with clean controls. And it runs self-hosted at $0." |
| "Where does the 'correct value' come from? Isn't that cheating?" | "Never from an answer key in production. Expected values come from (1) the trace's own evidence, e.g. the Calculator's inputs; (2) a source of truth the operator registers, e.g. the catalogue; (3) policy rules. Answer-key checks exist only in Fault Lab, for evaluation, and are labelled as such." |
| "What if the user defines no checks?" | "Then Granite can only detect explicit errors, and it says so. Coverage, meaning the share of runs with an applicable check, is a reported metric. That boundary is honest, and it's ErrorProbe's own limitation, which our oracles address." |
| "Is this just an AI wrapper?" | "Swap the LLM provider and every finding, root cause and verdict computation is byte-identical: we test that. The LLM is the system under test, plus an optional suggester whose output must pass verification." |
| "Show one failed test / edge case." | Show the REFUTED H2, the provider-down run, the ABSTAIN check, and a failing test from the CI history with the fixing PR. |
| "Why your own runner before LangGraph/CrewAI?" | "Replay needs exact control over which steps are frozen. We built that first (ADR-002), then adapters map framework traces into the same schema. LangGraph at Final-1, CrewAI at Mid-2." |
| "Why Render/Neon and not AWS?" | "$0, no credit card, and enough for a demo. The product itself is self-hosted with Docker Compose. Hugging Face Docker Spaces now need a paid plan, so we documented the decision in ADR-007." |
| "How do you know a CONFIRMED verdict is right?" | "On Fault Lab runs the true origin is known by construction, so we measure verdict precision and false-confirmation rate. Clean controls give the false-alarm rate." |
| "What changed since the proposal, and why?" | Walk through Form 10 (A1–A6) and change record C-01. Same problem, same mechanisms, product workflow, scope cut with reasons. |
| "What did the AI tools do, and what did you do?" | Read your own Form 13 rows and one AI-log entry for your module, including how you verified it. |
| "What breaks if the provider is down mid-verification?" | "Completed replays are kept, the verdict is ERROR, the finding returns to Hypothesized, and resume continues from where it stopped (FR-VER-05)." |
| "Is 5 replays enough?" | "For a decision rule with controls, yes for clear cases. Borderline cases come out INCONCLUSIVE, and the user can raise N. We report Wilson intervals and an N ablation." |
| "Who are your users really? Did you talk to any?" | Interview log (names/roles with consent, dates, what changed). |
| "What are the limitations?" | Check coverage; injected-fault accuracy is an upper bound; small models; replay needs a runnable workflow; English-only traces; demo data synthetic. |
| "What new core business logic has been added since the proposal defense?" (rubric probe) | Show the since-proposal delta slide (modules + file paths + tests), then run it live. |
| "What happens if this function is removed?" (rubric probe) | The owner answers from the walkthrough prep (§41.3, last column). |
| "Explain this paragraph of your R&D chapter without reading it." (rubric probe) | The chapter owner answers in their own words and names the paper or spike behind it. |
| "Your commit history is dominated by one member. Why?" | Be honest: proposal-phase documentation was mostly committed by one member. Then show the per-member PRs since 6 Oct and the ownership table. |

### 41.3 Code-walkthrough drill (each member prepares three functions)

| Member | Function 1 | Function 2 | Function 3 | For each: explain · alternative rejected · what breaks if… · what happens if it is removed (rubric probe) · live modification |
|---|---|---|---|---|
| Shahoud | `Runner.execute(plan)` | `inject_fault(run_plan, fault)` | `RecordedProvider.complete()` | e.g. modify: add a new fault type live |
| Noor | `evaluate_expression()` (AST whitelist) | `attribute()` provenance BFS | `bootstrap_ci()` | e.g. modify: change a ranking weight and show the test impact |
| Saif | `plan_replay()` | `decide_verdict()` (VR-1) | `FindingStateMachine.transition()` | e.g. modify: change a threshold to VR-2 and show the versioning |

---

## 42. Demo Scripts

### 42.1 Mid-1 (about 15 min, supervisor; ordered to follow the Form 2 criteria)

| Time | Form 2 criterion | Content | Presenter |
|---|---|---|---|
| 0:00–2:00 | F2-1 Proposal actions | Open the Panel Action Register (report §3.2) and click through each row's live evidence link | Shahoud |
| 2:00–3:00 | F2-2 Iteration progress | Milestone log: planned vs actual. Honest slip (implementation started 6 Oct) and the owner-assigned recovery plan. | Shahoud |
| 3:00–4:00 | F2-4 Requirements | Two FRs, their acceptance checks, and the matching test IDs and files | Noor |
| 4:00–10:00 | F2-3 Live core module | **The supervisor picks the order, items and fault.** Run → silent failure → H1/H2 → CONFIRMED / REFUTED → review → history. Clean run: no finding. Failure case: provider down → graceful state. *(T0: run spikes 3b, 4b and 5 live, then walk through the wireframed workflow.)* | Shahoud drives; Noor explains the root cause; Saif explains the verdict |
| 10:00–11:00 | F2-7 Testing | Run the test suite (or open the latest CI run). Show one edge-case test and one bug fixed through a PR. | Saif |
| 11:00–12:30 | F2-5 Design evolution | Architecture and ERD/state diagram next to the code; the design-evolution table (proposal → now, with reasons) | Saif |
| 12:30–13:30 | F2-6 Repository | Tags, PRs by each member, board, CI/CD runs; the contribution table (honest about the history) | Saif |
| 13:30–14:30 | F2-8 Ownership | Each member: one owned function, "what happens if it is removed", and their own Form 13 rows | All |
| 14:30–15:00 | Asks | Approve C-01; confirm Final-1 expectations; agree three weekly milestones if behind | Shahoud |

### 42.2 Final demo script (FYP-2 Final / Mid-2 panel, 12 min; job-fair version in brackets)

1. **Hook (0:45).** "A support agent team refunded a customer the wrong amount. No error, fluent answer. Today you'll watch Granite find where it went wrong, prove it, and prove the fix." [Job fair: 20 s]
2. **Instrumented workflow (1:30).** Show a LangGraph (or CrewAI) Refund Desk instrumented with the 3-line SDK snippet. Run it on a request with an injected stale-price fault. The run arrives in Granite (`source=sdk`).
3. **Detection (1:00).** Checks tab: the outcome check FAILs, step contracts point upstream. The finding is a *silent failure*.
4. **Trace back (1:30).** The provenance path animates on the graph: Writer ← Calculator (consistent) ← Policy (consistent) ← Order Lookup (truth mismatch). H1 = Order Lookup.
5. **Verify (2:00).** N=5 + 2 controls → CONFIRMED (5/5 vs 0/2, CI shown). Then verify the LLM's second opinion (blames the Calculator) → REFUTED. "The LLM guessed; the replay decided."
6. **Fix and recover (1:30).** Suggest fix → verify the fix → recovered run (correct refund) → export the regression case and show it passing in CI.
7. **Report and review (1:00).** Reviewer accepts; the exported report shows the evidence hashes.
8. **Does it work in general? (1:30).** Evaluation screen: origin accuracy vs last-agent and LLM-judge, false-alarm rate on clean controls, verdict precision, N/controls ablation, with CIs. One honest limitation.
9. **Real users (0:45).** UAT: participants, SUS, time-to-first-finding, one acceptance quote.
10. **Close (0:30).** "Find the failure. Prove the cause. Verify the fix. Self-hosted, open, $0." Repo and QR. [Job fair: steps 1, 3, 4, 5, 10 only = 3 min]

**Fallback order:** warmed production → recorded mode → laptop Compose → screencast + code.

---

## 43. Productization & Monetization Strategy (honest)

| Dimension | Assessment |
|---|---|
| Target users | Developers and QA of multi-agent LLM workflows; agent-building students and researchers |
| Target organisations | Small/medium software houses and AI agencies (including Pakistan's IT export sector) building support/ops agents for clients; university labs |
| Pain | Silent wrong outputs; slow manual diagnosis; unverified fixes; client data-residency constraints; SaaS cost in USD |
| Value proposition | Verified findings with evidence; self-hosted; $0 core |
| Competitive advantage (realistic) | Evidence-first verification protocol; offline/local-model capability; open source. **Not** breadth, scale or polish versus funded vendors (LangChain, Arize, Galileo, Patronus, Raindrop) |
| SaaS potential | Low to moderate for a student team: a crowded, well-funded market. Do not plan revenue around head-to-head SaaS. |
| Most credible path | (1) **Open-source project** (MIT) for adoption and portfolio. (2) **Services:** "agent reliability audit" engagements for local software houses using Granite (Fault Lab + checks + report). (3) **Education:** a teaching lab for agent-failure courses. |
| Illustrative pricing (only if pursued) | OSS core free. Audit engagement priced per workflow. Optional "team edition" (hosted, SSO, retention) later. No numbers are claimed until interviews validate willingness to pay. |
| Free tier | The whole self-hosted product |
| Enterprise potential | Self-hosted install + support contracts. Needs SSO, RBAC and retention (FYP-2 Should/Future). |
| Pakistan applicability | Strong fit for cost sensitivity and for foreign-client data constraints that favour self-hosting. Validate in the interviews (§6.2). |
| International applicability | OSS community; integrations (OTLP, Langfuse import) are the adoption levers |
| Scalability | Modular monolith scales to team workloads. For multi-team use, replace the job runner with a queue and use Postgres partitioning (Future). |

**Handbook position:** "Deployability is required; commercial success is not." This section is context for Report §3.2 (Business Opportunity), not a graded claim. Form 6 (startup evaluation) is optional. Opt in only if the interviews show real demand.

---

## 44. Future Extensions (post-FYP or only if far ahead; never displacing Musts)

- OTLP/OpenTelemetry GenAI ingestion; Langfuse/Phoenix import
- Check library informed by the MAST failure taxonomy; check suggestions mined from past findings
- GitHub Action `granite-verify` (regression cases in user CI)
- 3rd framework adapter (OpenAI Agents SDK / AutoGen)
- calibration of attribution scores (reliability diagram)
- Slack/webhook alerts
- multi-tenant teams/SSO/RBAC
- cost-aware adaptive N (sequential testing to stop early)
- leaderboard for the benchmark
- Urdu/Roman-Urdu agent traces (DEI/language extension)
- preventive checks at handoffs (revisit only with real labelled data)

---

## 45. Final Master Checklist

### Day 0 (today, Tue 6 Oct; v1.0 had scheduled this for Mon 5 Oct)

- [ ] Confirm the Mid-1 date and slot, the report deadline and channel, and the formatting rule (A1, D5, D7). Choose track T0, T1 or T2 (§30.2).
- [ ] Import the report template into `docs/report/`, apply the three fixes, fill the title data (§30.5).
- [ ] Team meeting (90 min): agree this plan, the ownership (D4), the hosted LLM (D1) and the Mid-1 backlog (§30.4).
- [ ] Repo hygiene (§28.1): clear the stale rebase, commit the reorganization, merge `origin/noor` (order in `archive/README.md`), tag the defense state, `main`/`develop`, protections, untrack datasets.
- [ ] Create the GitHub Project, milestones, labels, templates, CODEOWNERS.
- [ ] Accounts: Render, Neon, LLM free tier, GitHub Student Pack. Secrets stored in GitHub Environments only.
- [ ] Start the registers: Form 10 (A1–A6), C-01, milestone log, dependency/licence register, meeting minutes.

### Mid-1 (W8)

- [ ] §30.6 common DoD plus the chosen track's DoD ticked.
- [ ] Report compiled from the prescribed template (defects fixed, signatures, abstract 50–125 words) and submitted through the confirmed channel.
- [ ] Red-flag countermeasures rehearsed (§30.8): paragraph-defense drill, per-member walkthroughs, live register links.
- [ ] Report v1.0 submitted (soft form), with all R-M1 rows.
- [ ] Form 10 + Form 13 + AI log (countersigned) + C-01 presented.
- [ ] Two rehearsals done; warm-up checklist executed.

### Final-1 (W15)

- [ ] §31 Must list implemented; `v0.2.0` tagged and deployed to production.
- [ ] Evaluation v0 with baselines measured; benchmark v0 ≥ 120 runs.
- [ ] 4–6 stakeholder interviews logged; usability pilot (3) with SUS.
- [ ] Non-owner install recorded; deployment record updated.
- [ ] Poster submitted W13 (format compliant, supervisor-approved).
- [ ] Report v2.0 (format compliant) approved and submitted; traceability populated; handover/rollback/test plan drafted.
- [ ] Form 10 updated with the Mid-1 actions.

### Mid-2 (FYP-2 W8)

- [ ] CrewAI + LangGraph + runner integrated; benchmark ≥ 300; evaluation v1 with CIs + ablations.
- [ ] System test report; defect list (0 Critical, Highs dispositioned); NFRs measured.
- [ ] UAT plan approved; updated poster/report; `v0.5.0`.

### Job Fair (W12–14)

- [ ] Booth kit: warmed instance, offline fallback, 3-minute script, handout + QR.
- [ ] Graduate Directory materials submitted.

### Final-2 (W15) and final deliverables (W17–18)

- [ ] UAT completed and recorded; acceptance statements.
- [ ] Final evaluation + limitations; handover package; signed punch list; package + deployment diagrams.
- [ ] `v1.0.0`; outsider install; final report signed; plagiarism check passed.
- [ ] Submission bundle: report + PPT + references + code + executable/readme/user manual.

---

## Appendix A: Feature → User → Input → Processing → Output → Verification → Stored Evidence → Test Case (traceability matrix #3)

| Feature | User | Input | Processing | Output | Verification | Stored evidence | Test cases |
|---|---|---|---|---|---|---|---|
| F1 Run workflow | Developer | Message, e-mail, order, fault, LLM mode | Validate → fault plan → 5-step runner → record | Run + steps | Recorded-mode byte-identity; provider-down handling | `STEP_SNAPSHOT`, `fault_injection` | TC-RUN-01..04 |
| F2 Run detail | Dev, Reviewer | Run ID | Graph/lineage build | Steps, graph, checks, findings | Lineage matches `reads`; graph = table | — | TC-RUN-05, TC-UI-02 |
| F3 Checks / silent failure | Developer | Check defs + run | AST-safe evaluation; truth queries | PASS/FAIL/ABSTAIN/ERROR; findings | V1 re-evaluation identical | `CHECK_COMPUTATION`, `SOURCE_OF_TRUTH_QUERY` | TC-CHK-01..06 |
| F4 Trace back | Dev, Reviewer | Finding + graph + contract/truth results | Provenance BFS + ranking | Ranked hypotheses | Metamorphic invariance; ground-truth accuracy (Fault Lab) | `PROVENANCE_PATH` | TC-ATT-01..05 |
| F5 Verify | Developer | Hypothesis, intervention, N, M | Freeze upstream → patch → N + M replays → judge → VR-1 | Verdict + CI + replay table | Decision-table test; verdict precision in evaluation | `REPLAY_OUTPUT`, `DIFF`, `VERDICT_COMPUTATION` | TC-VER-01..06 |
| F6 Review / resolve | Reviewer | Decision + comment | State machine + audit | Status, recovered run, regression case | Transition tests; regression case passes in CI | `REVIEWER_NOTE`, `audit_log`, `fix` | TC-REV-01..03, TC-FIX-01..02 |
| F7 Report / history | Dev, Reviewer, Auditor | Finding ID, format; filters | Render report; query | MD/JSON/PDF; lists | Hash check vs `/evidence/{id}` | `report` (sha256) | TC-REP-01..02, TC-HIS-01 |
| F10 Import | Developer | JSON ≤ 5 MB | Schema validation → convert → redact → analyse | Run (non-replayable) | V1 only; 409 on replay | Original file hash | TC-IMP-01..04 |
| F12 Fault Lab | Developer (QA/research) | Matrix of workflows × runtimes × faults; clean % | Batch generation with labels | Benchmark | Ground truth by construction | `fault_injection` | TC-LAB-01..02 |
| F13/14 SDK + adapters | Developer | Decorated LangGraph/CrewAI app + API key | Capture → TraceV1 → ingest | Run (`source=sdk`) | Sample app parity test | `STEP_SNAPSHOT` | TC-SDK-01..03 |
| F15 Fix suggestion | Developer | Accepted finding | LLM Repair Agent (atomic field / prompt) | Candidate fix (unverified) | Must pass a `fix` experiment | `LLM_OPINION` + experiment | TC-FIX-03 |
| F18 Redaction | System | Step payloads | Regex redaction pre-insert | Redacted payloads | DB scan finds 0 patterns | — | TC-SEC-03 |
| F20 Evaluation | Team, panel | Benchmark + methods | Metrics + bootstrap CIs + baselines | Tables/charts | Pre-registration; fixed seeds | Results CSV + commit hash | TC-EVA-01..02 |

## Appendix B: Sample Test Cases (seed of the test suite)

| ID | Req | Level | Input / setup | Expected result |
|---|---|---|---|---|
| TC-RUN-01 | FR-RUN-01 | Integration | Valid Refund Desk input, recorded mode | Run `completed`, 5 steps, all with inputs/outputs/timestamps |
| TC-RUN-02 | FR-RUN-03 | Integration | Same input ×3, recorded | Step outputs byte-identical across runs |
| TC-RUN-03 | FR-RUN-04 | System | Provider base URL → closed port | Run `errored` ≤ 35 s; problem+json; UI banner |
| TC-RUN-04 | FR-RUN-02 | Unit | FLT-STALE on item 2 | `fault_injection` row; attribution module cannot import it (import-linter contract) |
| TC-CHK-01 | FR-CHK-01 | Unit | Outcome check with stated 43.00, truth 43.25, tol 0.01 | FAIL, observed 43.00, expected 43.25 |
| TC-CHK-02 | FR-CHK-01 | Unit | Same with stated 43.25 | PASS |
| TC-CHK-03 | FR-CHK-03 | Unit | Expression references a missing field | ABSTAIN (never PASS) |
| TC-CHK-04 | FR-CHK-02 | Unit/security | `__import__('os').system('x')`, `().__class__`, lambda, comprehension, attribute escape, 10⁶-length expression … (15 cases) | All rejected at validation |
| TC-CHK-05 | FR-CHK-04 | Integration | Completed run with a failing outcome check | Finding `silent_failure`, severity = max |
| TC-CHK-06 | NFR-05 | Unit | Re-evaluate a stored computation | Identical result + hash |
| TC-ATT-01 | FR-ATT-01 | Unit | Golden FLT-STALE trace | H1 = s2 Order Lookup, evidence `truth_mismatch` |
| TC-ATT-02 | FR-ATT-01 | Unit | Calculator arithmetic slip (natural) trace | H1 = s4, evidence `contract_fail` |
| TC-ATT-03 | FR-ATT-01 | Unit | Clean trace | No findings → no hypotheses |
| TC-ATT-04 | Metamorphic | Unit | Rename agents; insert an irrelevant step; scale prices ×10 | Same origin step key |
| TC-ATT-05 | FR-ATT-03 | Unit | Cyclic lineage fixture | Terminates; returns hypotheses |
| TC-VER-01 | FR-VER-02 | Unit | Decision table (k, N, c, M): (5, 5, 0, 2) → CONFIRMED; (4, 5, 0, 2) → CONFIRMED; (4, 5, 1, 2) → INCONCLUSIVE; (1, 5, 0, 2) → REFUTED; (3, 5, 0, 2) → INCONCLUSIVE; (5, 5, 2, 2) → INCONCLUSIVE; only 4 of N = 5 replays completed → ERROR … (20 rows) | Matches the expected verdicts |
| TC-VER-02 | FR-VER-03 | Unit | A replay fixes the target check but breaks CT-WRITER | Replay counted as not-pass |
| TC-VER-03 | FR-VER-01 | Integration | Verify H1 on the FLT-STALE run (recorded) | s1–s2 frozen (no LLM calls), s3–s5 replayed ×7; verdict CONFIRMED |
| TC-VER-04 | FR-VER-01 | Integration | Verify H2 | REFUTED |
| TC-VER-05 | FR-VER-05 | System | Provider dies after 3 replays | Verdict ERROR, 3 replays kept, resume completes |
| TC-VER-06 | FR-VER-04 | API | Verify on an imported run | 409 problem+json "replay unavailable" |
| TC-REV-01 | FR-REV-02 | Unit | All legal transitions; Open → Accepted (illegal) | Legal OK; illegal raises `IllegalTransition`; audit rows written |
| TC-REV-02 | FR-REV-01 | API | Reject without a comment | 422 |
| TC-IMP-01 | FR-IMP-01 | Integration | 6 malformed files (missing steps, duplicate IDs, dangling reads, bad timestamp, > 5 MB, > 500 steps) | Each returns the expected JSON-path error; nothing persisted |
| TC-SEC-03 | FR-SEC-01 | Integration | Run containing an e-mail, phone, CNIC 12345-1234567-1 and a card number | None present in the DB; tokens present |
| TC-UI-01 | J1 | E2E (Playwright) | Staging, recorded mode | Journey completes; verdict CONFIRMED visible; axe: 0 serious violations |
| TC-UI-02 | J2 | E2E | Clean run | "All checks passed. No findings." |

## Appendix C: Self-Audit (performed before issuing this plan)

| # | Question | Answer | Where |
|---|---|---|---|
| 1 | Every panel criticism addressed? | **Yes.** A1–A5 + the implicit A6, each with root cause, action, implementation and evidence. | §3 |
| 2 | All available Granite materials inspected? | **Yes, with stated depth.** Read in full: handbook (85 pp), vision, scope plan, SRS, SDS, use cases, test plan, SDP, commercial comparison, PoC code (backend, frontend shell, live-demo page), spike scripts/outputs (1, 2, 3b, 4, 4b, 5, 8), risk-register index, team actions, wireframe annotations, the remote-only newer guides (outlines + key sections), git history. Skimmed or used through summaries: the 976 KB explanation, the 81 KB handbook audit, the market-survey docx (via its .md), decks/PDFs, papers (title pages + ErrorProbe limitations + PROTEA rerun text). | §2 |
| 3 | Handbook inspected? | **Yes, all 85 pages**, including Appendices A–C, all forms (1–13), report format, poster rules and the C.5.1 gate table | §40 |
| 4 | Every applicable handbook requirement accounted for? | **Yes**, in 100 handbook rows (v1.1 added 5) plus 16 rubric rows (§40.0), across process, Mid-1, Final-1/poster, FYP-2, job fair and final deliverables. Optional/N/A items marked. | §40 |
| 5 | Functional Mid-1 core module defined? | **Yes.** A deployed vertical slice with real checks, attribution and replay verification, with per-track variants T0/T1/T2 (v1.1). | §30 |
| 6 | End-to-end workflow defined? | **Yes**, for three audiences, with a state machine | §13 |
| 7 | Inputs/outputs/verification explicit per feature? | **Yes.** I/O cards plus traceability matrix #3. | §14.2, App. A |
| 8 | How verification evidence is captured? | **Yes.** Levels V0–V3, protocol VR-1, typed hashed evidence, review and audit records. | §14.3–14.5, §22 |
| 9 | UI/UX, architecture, development, testing, deployment, CI/CD, documentation, defense covered? | **Yes** | §17–29, §39, §41–42 |
| 10 | Scope realistic for 3 undergraduates? | **Yes, after cuts:** 7 user-facing modules + Fault Lab; ErrorProbe repro demoted; benchmark ≥ 300; extensions → Future; hour estimate for Mid-1 ≈ 145 h with a cut variant | §11–12, §30.4 |
| 11 | Development cost minimized? | **Yes.** $0 stack with fallbacks; HF Spaces rejected after checking current terms. | §38 |
| 12 | Unsupported novelty claims avoided? | **Yes.** Retired 5 claims; DoVer, Percival, LangSmith Engine, Raindrop, Invariant and Galileo cited; contribution narrowed and tied to measurements. | §10 |
| 13 | Granite's original idea preserved? | **Yes.** All 10 approved mechanisms map to modules; same problem, stream, CCP, ownership areas, datasets. | §11.3 |
| 14 | Measurable definitions of done? | **Yes.** Per PR, per module, per milestone. | §36 |
| 15 | Can the team follow this to the end without redesigning? | **Yes, provided** A1 (Mid-1 date) is confirmed and C-01 is approved. Later changes go through C.5.3 records, not redesigns. | Header, §11.4 |
| 16 | *(v1.1)* Are the official rubric's criteria, gates and red flags all mapped to actions? | **Yes.** 16 criteria with evidence, owners and target bands (§30.1, §40.0); 6 red flags with countermeasures (§30.8). | §30, §40.0 |
| 17 | *(v1.1)* Does the report plan follow the prescribed template? | **Yes.** A chapter-by-chapter map with owners and rubric criteria; three template defects identified with fixes; Table 1a items placed; the template-vs-§8 formatting conflict resolved as a decision point (D5). | §30.5, §39 |
| 18 | *(v1.1)* Is the Mid-1 plan feasible from the actual state on 6 Oct? | **Yes, by track.** T0/T1/T2 by confirmed date; the report from D0; cuts named. Honest expectations are stated per track. | §30.2–30.3 |
| 19 | *(v1.1)* Are mandatory and recommended items distinguished? | **Yes.** Tags [M-R]/[M-H]/[M-F]/[M-T]/[Rec] in §0, §30, §39 and §40. | Header |
| 20 | *(v1.1)* Was any requirement invented? | **No.** Mandatory tags cite the rubric, handbook, template or faculty statement; everything else is [Rec]. Unknowns (date, report deadline and channel, Form 2/3 weighting, template-vs-§8 formatting) are decision points, not presented as facts. | Header |

**Known limits of this plan:**
- Semester dates are estimated.
- Free-tier terms must be re-verified.
- Commercial-competitor capabilities are taken from public docs (2026-10-04) and should be re-checked before each gate.
- The Mid-1 date, the report deadline and channel, and the weighting of Form 2 vs Form 3 are not stated in the provided files (A1, D7).
- The template defects were identified from the source and the supplied PDF. Confirm the fixes by compiling.
- Interview outcomes may change the requirements; that is expected and recorded.

---

## Appendix D: Change Log, v1.0 (2026-10-04) → v1.1 (2026-10-06)

| # | Change | Where | Evidence / reason |
|---|---|---|---|
| 1 | Added §0 (Mid-1 action card) and the mandatory/recommended tag legend | Header, §0 | A single starting point for the next days; the requirement to separate mandatory from recommended items |
| 2 | **Report pipeline changed** from Markdown → pandoc → Word (handbook-styled) to the **prescribed LaTeX template** | §20, §28.1, §30.5, §38, §39 | The template README says it is "aligned with Form 2 and Form 3"; rubric F3-1 grades "prescribed template followed" |
| 3 | **Report written in parallel from D0**, not on the day before Mid-1 | §0, §30.3 | Form 3 = 100 marks; the template was 0% filled on 6 Oct |
| 4 | Variant A/B (5 and 10 days) replaced by **Tracks T0/T1/T2**, re-based on the real 6 Oct state | A1, §30.2–30.3, §45 | No Day-0 action since 4 Oct; the rubric issued 5 Oct suggests Week 8 is now or next week |
| 5 | Rubric targeting: each criterion mapped to evidence, owner and target band per track | §30.1, §40.0 | Official bands, gates and caps |
| 6 | Red-flag countermeasures (small PRs, "what if removed" notes, own-words writing, per-member code, honest logs, live register) | §26.3, §30.8, §41.2 | Rubric "Red Flags and Supervisory Action" |
| 7 | Mid-1 DoD **recalibrated per track**. v1.0's "≥ 15 merged PRs, ≥ 30 tests, 70% coverage gate, Playwright on staging" now applies only to T2; T1 thresholds lowered and marked as minimum evidence. | §30.6, §36.3 | Infeasible from zero code in ≤ 4 days; inflating counts would itself trigger red flags |
| 8 | Three template defects documented with fixes. Formatting conflict (template vs handbook §8) resolved in favour of the template for Mid-1, pending supervisor confirmation. Abstract-length conflict resolved per the handbook. | §30.5, §39.3, D5, D6 | `fast-nuces-bs.cls` (`\maketitle` prints the TOC), `main.tex` (prints it again; no `longtable`/`booktabs`), `01_students_submission.tex` (undefined macros); symptoms visible in the supplied PDF |
| 9 | Handbook Table 1a items placed into the template's chapters | §30.5 | The template has no dedicated sections for wireframes, deployment diagram, setup/tool manual, CI/CD or static analysis |
| 10 | **Scope Table** made an explicit report artefact, tied to the proposal mapping | §30.5, §40 (R-M1-40) | Rubric F3-3 requires consistency with the proposal; its red-flag gate names a mandatory Scope Table |
| 11 | T0/T1 simplifications (Policy as rules, SQLite, steps list, no redaction yet); UI built by **evolving the existing PoC console** | §30.2, §30.4 | Time available. The faculty statement explicitly allows "the live/functional interface (or its improved version) that was shown as a POC". |
| 12 | `.mailmap` for Noor's two commit identities; the restructure done as a pure-move PR | §28.1 | Rubric F2-6 (member evidence) and the "sudden code volume" red flag |
| 13 | K1 re-rated; new risks K25–K30 | §37 | Rubric red flags, template defects, logistics unknowns |
| 14 | Compliance matrix: +16 rubric rows (§40.0), +5 template/report rows (R-M1-39–43); R-M1-25 and R-F1-16 corrected; status date moved to 6 Oct | §40 | New official files |
| 15 | Mid-1 demo script re-ordered to follow the Form 2 criteria; supervisor-chosen input added | §42.1 | Rubric Form 2; "hardcoded scaffolding" band in F2-3 |
| 16 | **Workspace reorganized the same day.** Paths in this plan updated; section 28.1's tree replaced by a pointer to `docs/workspace-guide.md`; benchmark data now `data/benchmark/` (scripts and results stay in `research/eval/`); register and manual file names aligned with `docs/registers/README.md` and `docs/manuals/README.md`; Day-0 git order revised (commit the reorganization before merging `origin/noor`) | sections 2, 8, 28.1, 32, 39, 40 and the header | `docs/workspace-guide.md`; `archive/migration-map_2026-10-06.tsv` |
| 17 | **Deliberately unchanged:** product direction, workflow, verification protocol (VR-1), architecture, stack, scope bands, Final-1 and FYP-2 roadmaps, novelty re-baselining | — | The rubric rewards exactly these, and no new evidence contradicts them |
