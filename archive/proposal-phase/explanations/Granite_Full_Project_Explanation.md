# Granite — Full Project Explanation

*A complete What/How/Why walkthrough of the entire Granite FYP project — every heading, every feature, every spike, every decision, explained from first principles. Compiled 2026-08-24/25 from all project source documents. If any number here ever disagrees with the plan doc, risk register, PDF, or artifact, those are the source of truth — this file is a teaching document built from them, not a second source of truth.*

> **⚠️ Status: internal narrative record, not a deliverable — and a point-in-time snapshot.** Do not present from this file, and do not treat it as spec. It was compiled *before* the 2026-08-25 pre-defense audit, so several passages below are **knowingly stale** — most notably it discusses team ownership (R6) as unassigned, the committed core as a flat 10-item list, and FR4 as promising *deterministic* re-execution. All three have since changed: ownership is assigned (R24), the core is tiered with pre-registered Mid-1 gates (R23), and the replay claim is now "controlled counterfactual replay" (R25). Those passages are deliberately left unedited so this file remains a faithful record of what was true when it was written; go to the plan doc and risk register for current state.

---

# READ THIS FIRST — Granite in Plain English

*Everything below this point (Parts 1–11) is the deep, exhaustive technical reference — every feature, every spike, every risk entry, argued in full academic detail. This section exists separately because density and understanding pull in opposite directions: nobody grasps a 4,000-line document by reading it top to bottom in one sitting. Read this section first, in order, and you will actually understand the whole project. Then dip into the detailed Parts below only for whichever piece you need to go deeper on — a specific spike, a specific risk, a specific CCP characteristic.*

## The problem, in one story

Imagine a team of AI assistants working together on a task — one plans, one searches the web, one writes code, one checks the answer. This is called a "multi-agent system," and companies are starting to build real products this way (customer support bots, coding assistants, research tools).

Sometimes these teams of AI agents get the final answer wrong. When that happens, you want to know: **which agent messed up, and at which exact step?** That's surprisingly hard — even the best published research method in the world (called ErrorProbe, from a 2026 research paper) only gets this right about 6 times out of 10 (59.5%).

There's a worse version of this problem too: sometimes the AI team's answer *looks* completely fine — no error message, no crash, nothing obviously wrong — but it's actually incorrect. Imagine a customer-support AI that confidently tells a customer their refund is $58 when it should be $61.75. Nothing "broke." Nobody would notice unless they checked the math by hand. This is called a **silent failure**, and right now, nothing on the market reliably catches it.

**Granite is a tool that solves both problems.** Point it at your multi-agent AI system, and it will: (1) tell you which agent and which step caused a failure, (2) catch the silent, no-error-message failures too, and (3) — this is the genuinely new part — actually *test* whether a proposed fix would work before you trust it, by re-running the fixed version and checking if it now gets the right answer.

## Why this counts as a real, hard research problem (not just an app idea)

Universities require Final Year Projects in "Stream A" (research-based, as opposed to Stream B, which is just building an app) to tackle something called a **Complex Computing Problem** — a problem that's genuinely hard, not just time-consuming. There's an official 9-point checklist for this (from something called the Seoul Accord), and Granite was checked against every single point, honestly, not just assumed to qualify. It clears **8 of the 9** — the 9th (needing real feedback from actual industry people who'd use this) is honestly marked as "not done yet," because it genuinely hasn't been done yet. No point was faked to make the count look better.

The strongest single piece of evidence for "this is genuinely hard": the best published method in the entire field, after over a year of dedicated research by multiple teams, still only gets the right answer 59.5% of the time. If this were an easy problem, someone would have solved it by now.

## What already exists, and why it's not enough (the market research)

Before building anything, the team checked whether some existing tool already does this. Two rounds of checking happened:

1. **Round 1 — AI "observability" tools** (LangSmith, Langfuse, Braintrust, Arize, Maxim AI, Opik, DeepEval — 7 platforms people actually pay for today). These are good at showing you *what happened* in a trace, but none of them reliably tell you *who's to blame* or *test a fix before trusting it*.
2. **Round 2 — a second, independent market survey** covering 7 different products — the actual frameworks used to *build* multi-agent AI systems in the first place (OpenAI's Agents SDK, LangGraph, CrewAI, Google's ADK, Microsoft's Agent Framework, Amazon's AgentCore, and an older project called BabyAGI). This survey confirmed the exact same gap from a completely different angle: none of these 7 frameworks can tell you which agent or step caused a failure either, and none of them can generate a fix and verify it works.

Two independent surveys, checking two different layers of the market, landing on the same conclusion — that's much stronger evidence than either survey alone.

## What Granite actually is (the product)

A downloadable software toolkit (an "SDK") that a development team installs and points at their own multi-agent AI system. Once installed, it:
1. Watches the AI system run and records what each agent did (a "trace").
2. If something goes wrong, figures out which agent and which step caused it.
3. Double-checks that answer against the actual evidence in the trace before trusting it (so it's not just guessing).
4. Separately checks for silent failures — cases where nothing crashed but the answer is still wrong.
5. If a failure is confirmed, proposes a fix, and then actually **tests the fix** by re-running things — not just suggesting a fix and hoping it works.
6. Shows all of this on a simple dashboard.

This is a real, buildable, installable piece of software — not just a research paper idea.

## The 10 must-have pieces (the "foundational core")

These 10 things are non-negotiable — the project isn't done without all 10, and 8 of them have already been built and tested in small proof-of-concept form:

1. **Fault-injection harness** — a tool that deliberately breaks a multi-agent system in a controlled way, so there's a known "right answer" to test against. ✅ tested
2. **Cross-architecture benchmark** — a test set built from multiple different AI-agent frameworks, so the tool proves it isn't just tuned for one specific setup. ✅ partially tested
3. **Culprit Agent** — figures out *which agent* caused the failure. ✅ tested (75% correct)
4. **Error Step Localization** — figures out *which exact step* caused it. ✅ tested
5. **Verification Agent** — double-checks a guess against real evidence before trusting it (this is what separates Granite from a tool that just guesses).
6. **Repair Agent** — proposes an actual fix. ✅ tested (got it right 4 times out of 6, and the 2 misses have a clearly understood, fixable cause — explained below)
7. **Semantic Error Diagnostic** — catches the silent, no-crash failures. ✅ tested
8. **Verified Automatic Repair** — actually re-runs the fixed version to *prove* the fix works, instead of just hoping. ✅ tested (worked)
9. **Recovery Controller** — resumes the AI system's work from the point where it was fixed, instead of starting over from scratch. ⚠️ **not built or tested yet — this is an honest, open gap, stated plainly, not hidden.**
10. **Verified Repair Memory** — remembers successful fixes so the same mistake gets caught and corrected automatically next time. ⚠️ **built once already, tested once, and it failed** (it never once successfully remembered a fix in the test). Kept in the plan anyway, on the condition that it gets tested again on stronger AI hardware before anyone claims it works.

**Why include two things that don't work yet?** Because hiding a failure is worse than reporting it honestly. This project's entire discipline, top to bottom, is: report what was actually tested, report real numbers, and never claim something works when it hasn't been proven. A panel or supervisor asking "does X work?" gets a true answer either way.

## What's proven, with real evidence (the 8 experiments)

Every one of these was actually run — not just planned — using a completely free AI model running on a normal laptop (no expensive paid API needed):

| # | What was tested | Result |
|---|---|---|
| 1 | Can we reproduce the best published method? | 75% correct on "who did it," but the exact step number was harder |
| 2 | Can we track a real multi-agent system's actions? | Yes, worked cleanly |
| 3 | If we break something on purpose, can we tell exactly what broke? | Yes, with a useful lesson learned along the way |
| 4 | Can we catch a "looks right but isn't" failure? | Yes, the detector worked correctly every time it was tested |
| 5 | If we fix one wrong step, does re-running actually fix the final answer? | Yes |
| 6 | Does the system get stuck in an infinite loop if the AI agents retry each other in a circle? | No — proven not to, including a deliberate test where the safety mechanism was turned off just to confirm it was actually doing something |
| 7 | Can a cheap, simple method flag a risky handoff between agents before it becomes a real failure? | No — this one genuinely didn't work (near-random guessing). Reported honestly as a failure, not hidden. |
| 8 | Can the AI actually propose a correct fix, not just detect the problem? | Mostly — 4 out of 6 test cases worked, and the 2 misses turned out to share one exact, fixable cause: the AI sometimes handed back a *calculated result* when it should have handed back the *specific corrected number* |

## Walking through it with three realistic examples

Everything above is described in the abstract. Here's what it actually looks like on real, specific cases — the same kind of cases used in the real proof-of-concept experiments (Spike 4, Spike 5, Spike 8), not made-up ones.

### Example 1 — a silent failure that no crash would ever catch

**The setup.** A retail-support multi-agent system (built on the tau-bench retail dataset, the same one Granite's benchmark uses) is asked to process a customer refund. One agent looks up the order, a second agent calculates the refund amount (item price minus a loyalty discount), and a third agent issues the refund.

**What goes wrong.** The calculating agent reads the customer's loyalty discount correctly from the account record, but a subtle formatting bug causes it to apply a flat percentage instead of the tiered rate the account actually qualifies for. The refund is issued. Nothing crashes. No tool call fails. No agent raises an error. The system reports success — and the customer gets the wrong amount of money back.

**Why this matters:** a normal error-monitoring dashboard would show this run as 100% successful, because "successful" to a normal dashboard just means "nothing threw an exception." This is exactly the class of failure Granite's Semantic Error Diagnostic exists for — the plan doc's own phrase for it is a "silent failure: no crash, no error signal, but the wrong output."

**What Granite does about it, step by step:**
1. **Semantic Error Diagnostic** compares the calculating agent's output against a numeric consistency check (does the discount actually match the tier the account record shows?) and flags a mismatch — this is the same mechanism validated in Spike 4, which caught every deliberately-injected silent failure it was tested against.
2. **Culprit Agent** is handed the full trace and asked which agent is responsible. It correctly names the calculating agent, not the lookup agent or the refund-issuing agent — the same task Spike 1 measured at 75% accuracy.
3. **Error Step Localization** narrows it further, to the exact step where the discount tier was applied, not just "somewhere in this agent's turn."
4. **Verification Agent** checks this diagnosis against the actual trace evidence (the account record really does show a tiered rate; the output really does show a flat rate) before anything downstream is allowed to trust it. This is the step that stops Granite from ever acting on an unverified guess.
5. **Repair Agent** proposes the correction: replace the flat-rate discount value with the correct tiered-rate value.
6. **Verified Automatic Repair** doesn't just accept that proposed fix — it re-runs the refund calculation with the corrected value and checks whether the final refund amount now matches what it should be. Only if the re-run actually produces the right answer does Granite report the failure as fixed.
7. **Recovery Controller** (still unbuilt — one of the two honest gaps) would, once built, resume the workflow from that repair point — the refund-issuing agent wouldn't need to redo the order lookup from scratch, just pick up with the corrected number.
8. **Verified Repair Memory** (also unbuilt/failed once) would, if it worked, remember "loyalty-discount tier mismatches get fixed this way" so the next time the same class of bug shows up, Granite applies the fix automatically instead of re-diagnosing from zero.

### Example 2 — proving it isn't just tuned for one framework

**The setup.** The same refund-calculation bug from Example 1 is deliberately, artificially introduced (not naturally occurring) into two different multi-agent systems: one built with CrewAI, one built with LangGraph — this is exactly what the fault-injection harness (must-have piece #1) and the cross-architecture benchmark (must-have piece #2) are for.

**Why this is necessary, not just nice-to-have:** a diagnosis tool that only works on CrewAI traces because it was accidentally tuned to CrewAI's specific message format wouldn't be a real contribution — it would be a demo that happens to work once. The market survey's own comparison table shows every major commercial platform (LangSmith, Langfuse, Braintrust, Arize, and the rest) is evaluated on, at most, one or two frameworks. Nobody has published a method proven to generalize across architectures the way Granite's benchmark is designed to test.

**What actually happens:** the fault-injection harness corrupts the same logical value (the loyalty-discount tier) in both systems, using the same corruption mechanism (a deterministic, rule-based operator — not an LLM guessing what a "realistic" bug looks like, which is the specific design decision recorded in the plan doc's external-component classification table). Granite's diagnosis pipeline is then run against both traces without any framework-specific tuning. The benchmark records, for each framework separately, whether Culprit Agent and Error Step Localization still got the right answer. A result that holds up on both is real evidence of generalization; a result that only holds on one is evidence of the opposite, and would be reported as such — the same honesty discipline visible everywhere else in this document.

### Example 3 — the Repair Agent's real, documented failure mode

**The setup.** This one isn't hypothetical — it's the two actual test cases Spike 8 got wrong, reported here exactly as they happened, because pretending Repair Agent is flawless would misrepresent the real result (4 out of 6, not 6 out of 6).

**The case (`loyalty_discount`).** The Repair Agent was shown evidence that a customer's account qualifies for a 15% loyalty discount, and the task was to correct a wrong discount value used earlier in the trace. Instead of returning `0.15` — the specific, atomic, corrected value the downstream code was expecting — the model returned the *final discounted price* (i.e., it did the multiplication itself and handed back a computed result). The re-execution check then failed, not because the model didn't understand the evidence, but because it answered a different question than the one asked: "what's the corrected discount rate" versus "what's the final price."

**The other case (`notebook_order`)** failed for the identical reason: given evidence of the correct item quantity, the model returned the correct *total cost* instead of the raw corrected quantity.

**Why this is a genuinely useful negative result, not just a failure:** both misses share one exact, nameable cause — an interface-specification problem, not a reasoning problem. The model *found the right fact* both times; it just packaged the answer at the wrong level (a computed downstream value instead of the specific atomic parameter the pipeline needed back). That's a fixable, well-understood category of bug (tighten the prompt's output contract, or add a schema-validation step that rejects a "repair" whose type/shape doesn't match the parameter being corrected) — which is exactly why Repair Agent stays in the committed core with its real 4-of-6 result stated plainly, rather than being quietly dropped or reported as "it works" without the caveat.

**The connection to Verified Repair Memory's failure.** This same mismatch is part of why the memory-reuse experiment (must-have piece #10) failed its one real test (0 of 8 stored commits reused correctly, accuracy actually dropped from 75% to 50%): if a stored "successful" repair was itself a slightly-off computed value rather than the clean atomic correction, reusing it on a superficially similar future case reliably produces the wrong answer instead of the right one. The two results aren't a coincidence — they're the same root issue showing up in two different experiments, which is the kind of cross-checking honest evidence is supposed to produce.

## The honest risks — read this, don't skip it

- **Real people haven't been talked to yet.** The one weak point in the "is this hard enough" checklist.
- **Nobody has actually been assigned to build which part yet.** Three job areas exist on paper (data/benchmarks, the diagnosis brain, the deployable product) but no specific person owns any of them yet.
- **Two of the 10 must-have pieces are unfinished or already known to have failed once** (Recovery Controller, Verified Repair Memory) — explained above, not hidden.
- **The "remember successful fixes" idea (again) has one real failed test behind it already**, and needs a stronger AI model before anyone can say it works.

## How the name and title changed (so nobody's confused seeing old names)

The project was called **"TraceCause"** for most of its life. On 2026-08-24 the short name was changed to **"Granite"**, and the official, full project title became **"A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery"** — a title taken directly from the second market survey's own recommendation, since it precisely describes what the product does. Old documents/logs that were written before this date correctly still say "TraceCause" — that's not a mistake, it's an honest historical record of what the project was called at the time.

## What's actually delivered right now

- A full planning document with the CCP justification, requirements, and evaluation plan
- A risk register tracking 22+ real, evidence-backed risks and decisions
- A 12-slide (now longer) supervisor briefing PDF
- A CCP justification document answering all 9 official checklist questions with real evidence
- A published, shareable web summary (the "artifact")
- 8 real, working proof-of-concept experiments with code and results saved on disk
- This document — the plain-English explanation you just read, plus the full technical depth below it

## Update — 2026-09-06: the poc-demo frontend grew a real "Live demo" experience

*Appended rather than rewritten in place, per this file's own stated discipline (see the status callout at the top) — the passages above stay a faithful snapshot of 2026-08-24/25; what follows is new, dated content, not a correction of old content.*

The `poc-demo/frontend` React console (Overview, Runs & Diagnoses, POC Evidence, Product & Scope) gained a fifth section, **Live demo**, built as a standalone interactive HTML page (`poc-demo/frontend/public/onclick-demo/index.html`) rather than a React page, so it can be opened and driven independently of the backend. It has five views:

1. **System Architecture** — all 11 real pipeline components (SDK adapters, PII redaction, execution-graph builder, Semantic Error Diagnostic, backward causal tracer, Repair Agent, Verified Automatic Repair, Recovery Controller, Verified Repair Memory, backend API, React dashboard), grouped under their three owners, each clickable for purpose/input/output/tech/evidence. Every node carries an honest status badge: **● REAL** (has a proof-of-concept spike behind it), **◐ SIMULATED** (deterministic playback of a designed-but-unbuilt piece), or **○ PLANNED** (not yet built at all).
2. **SDK Showcase** — the installable Python SDK's designed interface (quickstart, config YAML, the 5-method core API, example JSON output), explicitly marked **illustrative — no SDK code exists yet**, matching the same disclosure `ProductVision.tsx` already uses. A "run this snippet" button plays a deterministic, pre-scripted terminal transcript — never claimed as a live process.
3. **Run Pipeline** — the one-click diagnosis walkthrough (the same chained Spike 5 + Spike 8 "tax_total" scenario used elsewhere in this project: PriceExtractor silently corrupts $100.00→$90.00, Semantic Error Diagnostic flags the mismatch, backward causal tracing localizes the culprit, Repair Agent proposes the fix, Verified Automatic Repair replays it back to $108.00), now paired with a live architecture-map sidebar (highlighting which real component is "active" per stage) and a backend-log panel streaming real field/function names, so the backend is visibly doing something rather than hidden behind a spinner.
4. **Research Novelty** — the same trace processed two ways, side by side: an anomaly-gated pipeline (what ErrorProbe-class methods do) reports it `HEALTHY` because nothing crashed; Granite's Semantic Error Diagnostic reports `FLAG` because the task-spec constraint (`total == price × 1.08`) is directly violated. Paired with the real accuracy bars (Who&When 14.2% → ErrorProbe 59.5% published → Granite's own reproduction spike, 71% agent / 13% step mean, n=8, 5 runs).
5. **Evaluation & Results** — metric tiles, the four pre-registered success bands (failure/acceptable/strong/exceptional), and the full 8-spike evidence table, both honest negatives (Spike 7's near-random preventive classifier, Verified Repair Memory's failed test) included and labeled, not hidden.

**A 10-slide animated HTML deck was also built and then deliberately removed.** For a period this session, `poc-demo/frontend/public/slides/index.html` held a drag/swipe-navigable, 10-exhibit animated proposal-defense deck (mirroring `Proposal_Defense_Slide_Content_Spec.md`), reachable via a sixth sidebar section, "Animated slides." Static `.pptx` counterparts (`Granite_Proposal_Defense_3Slide.pptx`, `_10Slide.pptx`) were also generated via a scripted `pptxgenjs` pipeline, with native PowerPoint slide transitions injected as a post-process and verified (every XML part in the resulting package checked well-formed). All of it — the HTML deck, both pptx variants, and their generator scripts — was later removed by team decision in favor of the pre-existing `Granite_Proposal_Defense.pptx` and the Live demo section above; nothing described in this paragraph exists in the repository any more, it's recorded here only so the history isn't a silent gap.

**A separate, independent full-project synthesis document was also added at the repository root**, `explanation.md` — a 1,017-line teaching document (big picture, objectives, requirements, architecture diagrams, dev plan, milestones, risks, a full defense question bank) authored separately from this file. The two documents overlap in places and were not reconciled against each other; where they disagree, treat both as independent narrative snapshots the way this file's own opening disclaimer already asks you to, not as competing sources of truth — `FYP_Scope_CCP_and_Implementation_Plan.md` and `risk-register.md` remain the actual source of truth for either.

---

*Now proceed to Part 1 below for the full, detailed, academic-depth version of everything summarized above.*

---

## Parts 1–3: Identity, Research Baseline, and CCP Justification

*Every claim, number, and quotation below is drawn directly from the project's own working documents — principally `FYP_Scope_CCP_and_Implementation_Plan.md`, `AI_Usage_Log.md` (all nine sessions), `Guide_Compliance_Audit.md`, `ErrorProbe_Baseline_Selection.md`, `Full_Literature_Landscape_Analysis.md`, `AgenTracer_vs_WhoWhen_Analysis.md`, `Paper_Release_Timeline.md`, `generate_ccp_docx.py`, `FYP_Registration_Form_Answers.md`, `risk-register.md`, and `architecture-sketch.md`. Where the reasoning below goes beyond a direct quote — connecting a decision to its consequences, working through why an alternative failed, or grouping related facts into a pattern — that reasoning is offered as interpretation grounded in the cited evidence, and is flagged as such rather than presented as an independently documented fact. Nothing below is invented: no number, no quotation, and no named justification exists that isn't traceable to one of the files above. Where a piece of context named in the assignment brief for this document (a specific named teammate's pushback conversation) could not be located in the source logs after a direct search, that gap is stated honestly in place, rather than fabricated to fill the outline.*

---

# PART 1 — PROJECT IDENTITY

## 1.0 Why identity matters as its own Part

Before any research gap or CCP characteristic can be argued, a panel or reader needs to know exactly what is being defended: what the project is officially called, what stream of the FAST guide it falls under, what one-line idea it reduces to, which UN Sustainable Development Goal it aligns with, who its client is, and what makes it specifiable rather than a vague aspiration. This is not paperwork sitting outside the technical argument — the FAST guide treats identity, scope declaration, and client framing as gating requirements (§1.1, §1.3, §5.2, §6) that a proposal must clear before the CCP argument is even evaluated. Getting identity wrong — an unstable title, an ill-defined client, a stream declaration that keeps needing defending — costs credibility on every later argument, because a panel that catches an inconsistency in the framing will read the rest of the proposal looking for more.

Granite's own history shows this played out concretely: the project title was rewritten at least four times before landing on its current, adopted form; the short name went through nearly thirty candidates before settling on "Granite"; and the Stream A declaration required defending against a specific, recorded piece of external advice that would have collapsed one of the project's two lead research claims if followed. Part 1 walks through all of this in full, not because naming trivia deserves 900 lines on its own merits, but because the *reasoning process* behind each decision — what was tried, why it didn't survive scrutiny, what finally did and why — is itself evidence of the disciplined, iterative process the FAST guide's §9 ("Disciplined Idea-Discovery," all 11 steps) asks a team to demonstrate.

---

## 1.1 Project Title

### 1.1.1 What it is now

The official, adopted FYP registration title is:

> **A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery**

This is recorded verbatim, and identically, in three places: the header of `FYP_Scope_CCP_and_Implementation_Plan.md` ("*Official FYP Project Title* (adopted 2026-08-24, from `Agentic_AI_Market_Survey_BS_FYP.docx` §6): *A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery*"), the top of `FYP_Registration_Form_Answers.md`, and the seventh session entry of `AI_Usage_Log.md` ("Project Title officially set..."). Three independent files agreeing on the exact same string, word for word, is itself a small but real piece of evidence that the adoption was a deliberate, propagated decision rather than a draft that happened to survive — the same propagation discipline the log applies to every other cross-cutting change in the project (see §1.2.6 below on how renames are tracked).

"Granite" is explicitly retained as the permanent short title and product brand underneath this longer formal title — the plan doc's own header states this directly: *"'Granite' remains the permanent short title / product brand — see `FYP_Registration_Form_Answers.md` for the full title decision record."* The two names are not competitors; they serve different functions. The long title is the formal, defensible, technically-precise name a registration form or academic panel expects — it names every one of the project's headline mechanisms (self-healing, semantic error diagnosis, verified repair, recovery) inside the title itself. The short title is the name a person says out loud, writes on a slide header, or uses as a product brand if the post-FYP productization path (Part 1's own §1.5 references this, and the plan doc's §14 states it explicitly as future-work-only) is ever pursued.

### 1.1.2 How it was chosen

The title was not authored fresh by the team. It is, verbatim, **the market survey's own §6 "Recommended BS Final Year Project" title** — the phrase comes directly from `Agentic_AI_Market_Survey_BS_FYP.docx`, an external document the team read in full during the sixth AI-assisted session (2026-08-24), and it was adopted as-is rather than paraphrased. This detail matters for two reasons. First, it is an example of exactly the kind of external validation the project leans on elsewhere: a document written independently of the team's own scope decisions — a market survey of seven agentic-AI orchestration frameworks — happened to converge on nearly the identical framing the team had already been building toward (three of the survey's four recommended architectural modules already existed in Granite's frozen feature list under matching or equivalent names before the survey was even read; see Part 2 for the full account of this convergence). Second, adopting the survey's own recommended title rather than continuing to iterate on a team-authored one is a small discipline move: rather than defending yet another self-generated title against the panel's scrutiny, the team can point to an independent source recommending the same framing, which is a stronger footing than "we thought this sounded right."

The adoption date, 2026-08-24, sits inside the same working session (the sixth, per the AI usage log) that also added Repair Agent to the foundational feature list and rejected the market survey's own single-framework scope-narrowing advice (see §1.3.4 below) — i.e., the title decision did not happen in isolation; it happened as part of a broader session where the market survey was read cover-to-cover and every one of its recommendations was individually accepted, adapted, or rejected on its own merits, not adopted wholesale.

### 1.1.3 Why this title over the four earlier candidates

`FYP_Registration_Form_Answers.md` records, explicitly and without deleting the history, four earlier full-title candidates that were drafted and then superseded:

1. **"Granite: Cross-Architecture Failure Attribution and Silent-Failure Detection for Multi-Agent AI Systems"** — described as "the prior recommendation, before the survey's title was adopted." This was the team's own best full-title draft immediately before the market survey was read. It leads with the brand name ("Granite:"), which is a defensible convention (many product-facing academic systems title themselves this way), and it names the two headline research claims directly: cross-architecture attribution and silent-failure detection. Its weakness, relative to the adopted title, is that it names only two of what are now four headline mechanisms (diagnosis, repair, recovery, and the self-healing framing that ties them together) — by the time the ninth AI-usage-log session had reclassified Recovery Controller and Verified Repair Memory into the foundational core (2026-08-24, same day), a title that stopped at "detection" no longer covered the full committed scope. A title that undersells the scope of a project's own committed core is a real liability at defense, since a panelist reading only the title would reasonably ask why "repair" and "recovery" aren't mentioned if they're core deliverables.

2. **"Granite: A Framework-Agnostic System for Diagnosing and Recovering from Multi-Agent AI Failures"** — labeled "product-facing." This candidate leans toward the deployable-SDK half of the project's dual research/product framing (see Part 1's §1.5 client discussion) — "framework-agnostic system" reads like a product pitch, not an academic contribution statement. It captures "diagnosing" and "recovering" but drops the specific, defensible technical vocabulary ("semantic error diagnosis," "verified repair") that ties the title directly to the project's own named mechanisms and to the specific gap in ErrorProbe the project targets. A title this generic risks reading as a re-skin of any existing observability platform's own marketing copy — exactly the failure pattern the FAST guide's §10 warns against (platform/language/UI changes alone do not constitute differentiation), and a title should not accidentally suggest that failure pattern even if the underlying project avoids it.

3. **"Detecting Silent Failures and Verifying Recovery in Multi-Agent AI Systems Across Architectures"** — labeled "no brand name, plain technical." This candidate drops "Granite" entirely and reads as a pure academic paper title. Its strength is precision: it names silent-failure detection, verified recovery, and cross-architecture generalization — three of the project's genuine headline claims — in a single sentence with no brand-name distraction. Its weakness is that dropping the brand name loses the connective tissue between the formal academic title and the short title used everywhere else in the project's documentation, the registration form's "short title" field, the supervisor briefing, and the eventual post-FYP productization framing. A title with no product identity at all makes the eventual "Granite" references throughout the rest of the documentation feel disconnected from the formal title, rather than a clean abbreviation of it.

4. **"Granite: Failure Attribution, Silent-Failure Verification, and Counterfactual Recovery Testing for Multi-Agent LLM Systems"** — labeled "most complete, longest." This was the most exhaustive of the four drafts, naming failure attribution, silent-failure verification, and counterfactual recovery testing all in one title, plus specifying "LLM Systems" for precision. Its problem is exactly its own label: length. A title this long is unwieldy on a registration form, a slide header, or a citation, and by trying to name every mechanism explicitly it reads as a list rather than a single coherent framing — three coordinate noun phrases joined by commas is a structurally weaker title than one that expresses a single unifying idea ("self-healing") with supporting detail trailing after it.

**Why the adopted title wins over all four**, read as a single reasoning chain: it uses "Self-Healing" as the unifying frame — a single, memorable concept that subsumes diagnosis, repair, and recovery as its constituent stages, rather than listing them as three separate coordinate claims the way candidate 4 does. It retains full technical precision ("Semantic Error Diagnosis, Verified Repair and Recovery" — three specific, already-named pipeline stages, not vague verbs). It is exactly the length of a normal academic-systems paper title, comparable to the four ACL/AAAI/ICML/ICLR papers already in the project's own literature corpus (e.g., "Towards Self-Improving Error Diagnosis in Multi-Agent Systems" — ErrorProbe's own title uses nearly identical structural framing: adjective + domain noun + colon-free technical descriptor). And it arrived with independent, external validation rather than being one more internally-generated draft — the market survey recommended almost exactly this framing on its own, without having seen any of the four prior candidates.

### 1.1.4 What the title claims, read closely

Each word in the adopted title maps to a specific, already-committed piece of the project, not a decorative flourish:

- **"Self-Healing"** — the unifying frame. This is not marketing language layered on top of an otherwise ordinary diagnosis tool; it is a literal description of the closed loop the ten foundational items (Part 2, Part 5 of the eventual full document) implement: diagnose → generate a candidate fix (Repair Agent) → verify it (Verified Automatic Repair) → resume execution from the verified point (Recovery Controller) → remember the successful pattern for next time (Verified Repair Memory). A system that only diagnosed and reported would not earn "self-healing" in its title; Granite's committed core goes further, closing the loop back to a working system state.
- **"Multi-Agent System"** — names the subject matter precisely: this is not a single-agent LLM tool, and not a generic software system; the entire causal-graph, backward-tracing, and interdependence argument in Part 3's CCP characteristic #8 depends on the target being a genuinely multi-agent architecture where failures propagate through interdependent sub-agents.
- **"Semantic Error Diagnosis"** — the renamed (2026-08-23) label for what was originally called "silent-failure verification." This phrase is deliberately chosen over "error detection" because the project's second headline novelty claim is specifically about *semantic* correctness — an output can be syntactically valid, pass every schema check, and still be wrong in a way no anomaly detector catches. "Semantic" is the load-bearing word here.
- **"Verified Repair"** — not just "repair." The word "verified" is doing real work: it distinguishes Granite's approach from an unconditional auto-fix tool (explicitly rejected as a standalone feature — see Part 2's account of the "Automatic Retry" idea that was considered and not added, precisely because unconditional auto-remediation without verification is a trust failure the team explicitly designed against). Every repair candidate is deterministically re-executed and its recovery rate measured before it is trusted (Verified Automatic Repair, foundational item #5).
- **"and Recovery"** — names the final stage, Recovery Controller (foundational item #9), which resumes execution from a safe checkpoint rather than restarting the whole workflow — the newest and, as of the ninth AI-usage-log session, still entirely un-piloted (no POC evidence at all) piece of the committed core, honestly acknowledged as such rather than hidden behind the confident-sounding title.

---

## 1.2 Short Title — "Granite" — the Full Naming Journey

### 1.2.1 Why a naming journey belongs in a technical document at all

A reader might reasonably ask why nearly thirty rejected candidate names deserve real space in a document about a complex computing problem. The answer is that the naming process is itself a recorded instance of the project's own standing discipline: nothing gets adopted without being weighed against alternatives, and nothing gets silently dropped — every rejected candidate stays on record "in case revisited," in the exact words of `FYP_Registration_Form_Answers.md`. That habit — record the rejected alternative, don't erase it — is the same discipline visible in the risk register's treatment of failed POC results (Verified Repair Memory's 0-of-8 failure, Spike 7's near-random classifier) and in the AI usage log's treatment of corrected claims (the GraphTracer/FALaT reversion, the AgentRx removal, the TracerTraj licensing correction). The naming history is a small, low-stakes example of a habit that shows up in much higher-stakes places later in the project, and walking through it in full is itself evidence that the habit is genuine and consistently applied, not a discipline invoked only when it's convenient.

### 1.2.2 "TraceCause" — the name for most of the project's life

Before "Granite" existed at all, the project's short title was **TraceCause**, and it held that name for the overwhelming majority of the project's documented history — every one of the first six AI-usage-log sessions (spanning the initial ideation, literature review, all eight proof-of-concept spikes, the feature-narrowing and market-research passes, and the initial 16-to-17-item feature-list growth) is titled, in the log's own heading, **"AI Usage Log — TraceCause."** The log's own seventh-session entry is explicit and precise about the scope of the change: *"Short title renamed: TraceCause → Granite. Propagated across every current-state file... via a scripted regex replace (`TraceCause` not immediately followed by `_`, so actual filenames like `Granite_Supervisor_Briefing.pdf` and `Granite_CCP_Justification.docx` were deliberately left unrenamed on disk — only the brand text inside documents changed, not the physical file names, to avoid breaking cross-references)."*

Two things are worth drawing out from that one sentence. First, the rename was executed as a scripted, auditable operation — a regex replace with a documented exclusion rule — not a manual, ad hoc find-and-replace that risks missing files or corrupting adjacent text (the exclusion of `TraceCause_` as a prefix specifically protects filenames like `TraceCause_AgentTestLab_Pitch.md`, which is an archived document deliberately *not* renamed because it describes a superseded, wider-scoped pitch, not the current project). Second, and stated explicitly in the same entry: *"This log's own prior entries (first through sixth sessions, above) intentionally keep 'TraceCause' as originally written — same standing practice as the 2026-08-23 feature rename: past entries describe what was actually built and named at the time, this entry records the rename decision, it does not retroactively correct history."* This is a genuinely important documentation principle that recurs at least twice in the log (once for the 2026-08-23 foundational-feature renaming, again here for the brand rename): a log is a historical record, and a historical record that gets silently rewritten every time a name changes stops being trustworthy as a record of what actually happened when. Every POC spike, every risk-register entry, every architecture decision made under the name "TraceCause" is described in this document, where relevant, using the name that was actually in use at the time that work happened, with the rename noted explicitly rather than smoothed over.

### 1.2.3 The rejected candidates — full list

`FYP_Registration_Form_Answers.md` records the full set of names considered and rejected before "Granite" was chosen, in one deliberate list, described as kept "for the record, in case revisited":

> Causeway, Rootcast, Autopsy, Undertow, Culprit, Ripple, Recon, Triage, Fathom, Vigil, Halcyon, Meridian, Zenith, Astra, Solstice, Vantage, Zephyr, Steady, Clarity, Sure, True, Keen, Solid, Whole, Actual, Proof, Level, Given, Behold.

That is twenty-nine distinct rejected candidates plus TraceCause itself — one of the more thoroughly documented naming processes recorded anywhere in this project's files. The source document does not attach an individually-recorded rationale to each of the twenty-nine names; what it records is the single design principle that ultimately decided the matter: *"One word, permanent — chosen specifically because it won't need to change even if scope shifts."* Everything below in §1.2.4 is the document's own interpretive grouping of these twenty-nine names into plausible reasoning clusters, offered as analysis of the pattern visible in the list itself — the causal-diagnosis words, the domain-generic words, the abstract-value words — not as a claim that each cluster's rejection reason was separately documented in the source. Where the source gives a directly stated reason (the "won't need to change even if scope shifts" principle, and the folder-name evidence discussed in §1.2.5), that is marked as such.

### 1.2.4 Grouping the rejected names into reasoning eras

**Cluster 1 — causal-diagnosis / forensic vocabulary: Rootcast, Autopsy, Undertow, Culprit, Recon, Triage, Fathom.**

This cluster reads as the most literal, most on-the-nose attempt at naming: each word describes almost exactly what the system does. "Autopsy" names a post-mortem examination of a failure — which is precisely what backward causal tracing through an execution graph is. "Culprit" names the responsible party — which is literally the output of the Culprit Agent stage. "Triage" names the act of sorting failures by severity — a recognizable, medically-derived metaphor for the confidence-scoring and prioritization the diagnosis pipeline performs. "Recon" (reconnaissance) and "Fathom" (to measure the depth of, to understand fully) both gesture at investigation. "Rootcast" appears to be a portmanteau of "root cause" and "broadcast" or "forecast." "Undertow" is the odd one in this cluster — it evokes a hidden, dangerous current beneath a calm surface, which maps metaphorically to a *silent* failure: something wrong happening beneath an output that looks fine on the surface.

The interesting piece of independent evidence for this cluster is that it clearly won at least one internal round: the project's own top-level working folder on disk is named **`agent-autopsy`** — visible in every file path referenced throughout this document and every other file in the project (`d:\fyp - research\agent-autopsy\...`). That folder name was set at some point during the project's life and has never been renamed, even after the short title moved through TraceCause and then to Granite. This is a small but genuine artifact: it shows that "Autopsy," specifically, was seriously enough in contention at some point to become the literal filesystem name of the whole project — and that once a folder name is set and referenced by every relative link in dozens of interlinked markdown files, renaming it becomes its own costly propagation exercise (exactly the kind of costly, error-prone bulk rename the seventh AI-usage-log session had to execute carefully, with a scripted regex and an explicit exclusion rule, just for the brand text inside documents — doing the same for a folder name touching every cross-reference in the project would be a considerably larger undertaking). The folder name is a fossil of an earlier naming era that the team chose not to disturb, which is itself informative: it shows the team distinguishes between costs worth paying (rebranding visible, reader-facing text) and costs not worth paying (renaming an internal folder structure that only the team itself ever sees).

Why this whole cluster was ultimately rejected as a group, read against the "won't need to change even if scope shifts" principle: every one of these words describes a *specific mechanism* — diagnosis, root-cause identification, triage — rather than the *product itself*. A name that describes one pipeline stage risks becoming misleading or narrow if the project's scope moves (which it did, repeatedly and substantially: from 14 to 16 to 17 to 18 to 20 total frozen features across the AI usage log's later sessions, with entire new pipeline stages — Repair Agent, Recovery Controller, Verified Repair Memory — added after the original core was frozen). "Autopsy" specifically describes a *post-mortem*, i.e., examining something already dead/failed — but Granite's committed core also includes Repair Agent, Recovery Controller, and Verified Automatic Repair, which are about *reviving* a failed run, not just examining its corpse. A name anchored in the diagnosis half of the system stops fitting once the repair half becomes equally or more central to the committed scope.

**Cluster 2 — natural/elemental permanence words: Ripple, Vigil, Halcyon, Meridian, Zenith, Astra, Solstice, Vantage, Zephyr.**

This cluster reads as an attempt to move away from literal mechanism-description and toward something more abstract, evocative, and durable — words drawn from nature, astronomy, and mythology that don't describe *what the system does* so much as *evoke a quality* (watchfulness — "Vigil"; a high vantage point — "Vantage," "Zenith," "Meridian"; a moment of stillness or calm after storm — "Halcyon," "Solstice"; a light touch — "Zephyr," "Ripple"). This is plausibly the "permanence-focused" reasoning era named in the task brief: names chosen because they carry a durable, evocative connotation rather than a literal functional description, similar in spirit to how many real technology products (cloud platforms, security tools, observability products) are named after weather phenomena, celestial bodies, or abstract states rather than their literal function. "Granite" itself belongs to exactly this naming family — a hard, permanent, geologically stable rock, chosen (per the explicit stated principle) because a single, permanent word "won't need to change even if scope shifts." Reading the surviving winner against this whole rejected cluster, Granite is best understood as the version of this same naming strategy that worked: like "Vantage" or "Zenith," it evokes permanence and solidity rather than describing a mechanism, but unlike words drawn from weather or light (which can read as insubstantial, transient, ironically the opposite of the desired permanence), a rock is about as literal a symbol of stability and unchanging solidity as language offers — which fits a project whose own working principle for the short name was explicitly permanence under scope change.

**Cluster 3 — plain, layman-understandable abstract-value words: Steady, Clarity, Sure, True, Keen, Solid, Whole, Actual, Proof, Level, Given, Behold.**

This is the largest single cluster and reads as a distinct, later-stage reasoning attempt: short, common, single-syllable-or-near-single-syllable English words naming a value or quality directly, with no metaphor layer at all — plain, everyday vocabulary a non-technical reader (a "layman," in the task brief's own framing) would immediately understand without needing the mechanism explained first. "Clarity" and "Sure" and "True" all gesture at trustworthiness and correctness — the antonym-space of "silent failure" (an output that looks fine but is quietly, invisibly wrong). "Solid" and "Steady" and "Whole" gesture at completeness and reliability — a system that doesn't leave a workflow broken. "Proof" gestures directly at verification — matching "Verified" in the eventual full title. "Behold" is the outlier here, an imperative rather than a quality-word, closer to a product-launch flourish than a description.

This cluster plausibly represents the most heavily filtered, most "product-brand-ready" round of naming attempts — words chosen for how they'd sound as a one-word product name on a landing page or pitch deck, tested against pure readability and trust-signaling rather than technical precision. Its weakness, and the likely reason none of these twelve survived, is genericness: nearly every one of these words is already heavily used across the software industry as a product or company name (there are commercial products, real ones, named "Clarity," "Proof," "Solid," and "True" in adjacent spaces — security, analytics, fintech). A one-word abstract-value name in this register risks name collision, trademark ambiguity, or simply blending into an undifferentiated crowd of similarly-named SaaS products, which directly works against the "won't need to change even if scope shifts" durability goal: a name that's already crowded in its category space is a name a team might need to abandon later anyway, for reasons entirely outside their control (a naming conflict, a search-visibility problem), which defeats the entire point of choosing a name specifically to avoid ever needing to change it again.

**Why Granite specifically stuck, read against all three clusters together:** it is single-word (satisfying the plain-English/layman-accessibility goal shared with cluster 3, without cluster 3's genericness risk); it evokes permanence and stability directly and literally rather than through weather/celestial metaphor (satisfying cluster 2's permanence goal more directly than any of cluster 2's own candidates); and — unlike cluster 1 — it does not describe a specific mechanism or pipeline stage, so it does not become stale or misleading as the committed feature set kept growing across the AI usage log's later sessions. It is also, plausibly, distinctive in the sense the task brief calls "out of the universe" — a rock name is an unusual category for a software-diagnosis product to draw from, which gives it more room to become a distinctive, ownable brand than a word already crowded by cluster 3's more conventional choices.

### 1.2.5 What is honestly not documented

In the interest of the same honesty discipline this project applies elsewhere: the source files do not record a session-by-session, name-by-name rejection rationale for all twenty-nine candidates the way they do for, say, each POC spike's result or each CCP characteristic's justification. What is documented, precisely, is: the final list of rejected names (verbatim, quoted in §1.2.3), the one stated design principle that decided the winner ("chosen specifically because it won't need to change even if scope shifts"), the exact rename mechanics and propagation record for TraceCause → Granite (§1.2.2), and the physical fossil evidence of the `agent-autopsy` folder name (§1.2.4, Cluster 1). The three-cluster grouping above is this document's own organizing analysis of the pattern visible in the list, offered because it is genuinely informative about how naming decisions like this tend to unfold and because it is consistent with everything else documented about the decision — but a reader should treat the specific cluster-by-cluster rejection reasoning as interpretation, not as an independently sourced fact, and the two directly-sourced pieces of evidence (the stated principle, and the folder-name fossil) as the load-bearing facts underneath it.

### 1.2.6 The propagation discipline, generalized

The TraceCause → Granite rename is one instance of a pattern that recurs constantly throughout the project's documented history, and it is worth naming explicitly here because it will come up again in Parts 2 and 3: **every cross-cutting change gets propagated to every affected file in the same session it is decided, and the propagation itself gets logged as a separate, auditable action.** The seventh session's rename entry lists eleven separate files it touched (plan doc, risk register, PDF, artifact, architecture sketch, Commercial_Product_Comparison, Proposal_Defense_Package, Silent_Failure_Detection doc, datasets/resources/Guide_Compliance_Audit, FYP_Registration_Form_Answers, and the market-survey full-content file) plus two files it deliberately did *not* rename on disk. The eighth and ninth sessions repeat this same discipline for the Framework Compatibility Layer addition and the Recovery Controller / Verified Repair Memory reclassification respectively, each listing the specific files updated and — critically — each ending with the same honest caveat: *"Not yet independently reviewed by the team — confirm the new entries read correctly in context before citing them at defense, don't take this log's word for it."* That caveat, repeated verbatim or near-verbatim after almost every propagation entry across all nine sessions, is itself a recurring piece of evidence about how this project treats AI-assisted work: propagation is logged, but logged propagation is explicitly not treated as equivalent to human verification, and the log says so every single time rather than only when convenient.

---

## 1.3 Stream Classification — Stream A vs. Stream B

### 1.3.1 What the distinction means per the FAST guide

The FAST FYP Student Idea Selection Guide's §1.1 sets out "Two Entry Points" for how a project's core problem can originate. Per the Guide Compliance Audit's own summary of this section: *"Stream A declared... Per the guide's own table: starting point = published research (ErrorProbe) ✓; where the gap comes from = a stated limitation in published work (ErrorProbe's own admitted silent-failure blind spot, plus the confirmed cross-paper generalization gap) ✓; primary risk = 'can it be reproduced within our resources' — tested directly via spike 1, real number in hand ✓."*

Read in full, this is the guide's own three-row comparison test: a Stream A project's starting point is a piece of published academic research, its gap is derived from that research's own stated limitations rather than from a market or workflow observation, and its primary early risk is reproduction feasibility — can the team actually get the published method running well enough to compare against. Stream B, by contrast (not directly quoted in the audit but implied by the contrast structure), would start from an observed workflow or market gap rather than a paper, and its primary risk would be closer to "does a real client/user actually need this," not "can we reproduce a paper's numbers."

### 1.3.2 Why Stream A was chosen

Every one of the three defining criteria in the guide's own table is satisfied concretely, not asserted:

- **Starting point = published research.** The project's entire origin, as recorded from the very first AI-usage-log session, is a literature review across a specific corpus of academic papers (Who&When, AgenTracer, SDBL, TraceElephant, ErrorProbe, AgentAsk, PROTEA — all seven read in full, not abstract-level, per the log's own note: *"Literature-gap identification across Who&When, AgenTracer, SDBL, TraceElephant, ErrorProbe, AgentAsk, PROTEA... All 7 papers read in full (not abstracts), cross-checked against each paper's own stated limitations section."*) ErrorProbe specifically was then selected as the baseline the project measures itself against — not because it's the newest (it is not; see Part 2's discussion of the recency-vs-performance argument in `ErrorProbe_Baseline_Selection.md`), but because it is the strongest published performer on every benchmark where a same-benchmark comparison against other papers is possible.
- **The gap comes from a stated limitation in published work, not an inferred or market-observed one.** ErrorProbe's own "Limitations" section — read directly, not paraphrased from a secondary source — states in writing that its pipeline fails on "silent failures": technically valid but semantically wrong outputs that trigger no detectable MAST-taxonomy anomaly signal. This is the single most load-bearing sentence in the entire project's gap justification, because it means the project's second headline novelty claim (Semantic Error Diagnostic / RQ3) is not a gap the team inferred by studying the field from outside — it is a gap the strongest existing baseline *confesses to, in its own words, in its own paper*. The Full Literature Landscape Analysis is explicit about this: *"a gap the strongest existing baseline confessed to."* The cross-architecture generalization gap (RQ2) is slightly different in character — it is a confirmed absence across all seven papers (none tests transfer to an architecture unseen during its own benchmark construction) rather than a single sentence any one paper states about itself — but it too is derived directly from full-text reading of the published corpus, not from a market survey or a client interview.
- **Primary risk = reproduction feasibility, tested directly.** POC Spike 1 (`poc_spike1_errorprobe_repro.py`) ran a simplified two-stage reproduction of ErrorProbe's methodology against eight real, downloaded Who&When-Hand-Crafted cases and produced a real number — 75% agent accuracy, 12.5% step accuracy after a scoring-bug fix — before the proposal defense, exactly matching the guide's own described primary risk category for Stream A. Risk-register entry R1 names this explicitly as *"the single highest initial risk"* and records it as *"Partially tested, 2026-08-22... Real signal the approach works, not proof the full pipeline hits 59.5%."*

### 1.3.3 What the guide's own comparison table says, applied row by row

Beyond the three headline criteria above, the guide's Annex A.1 (referenced directly in `AgenTracer_vs_WhoWhen_Analysis.md`, an earlier, now-superseded analysis pass) states a preference principle relevant to Stream A projects specifically: *"prefer current... work."* This is why the project's baseline selection process (fully documented in Part 2) explicitly rejected a recency-only framing in favor of a performance-based one, while still confirming that ErrorProbe sits comfortably within the "current" window (arXiv preprint dated 19 April 2026, tied for ACL 2026 conference presentation with three of its closest competitors) rather than being a stale, superseded starting point.

### 1.3.4 Defending Stream A against real, recorded pushback

The task brief for this document specifically asks for an account of "teammate 'shahoud' pushback conversations logged in AI_Usage_Log.md." A direct search of every session in `AI_Usage_Log.md` for that name, and for close variants, found no match — no teammate by that name, and no pushback conversation attributed to that name, appears anywhere in the log as read. Rather than invent a conversation that isn't in the source record, this section documents the actual, real pushback against the project's committed scope that *is* recorded — which is substantively the same kind of challenge (an argument that the project's ambition should be narrowed) and was defended with exactly the rigor the task brief is asking to see demonstrated.

The real, recorded pushback is **risk-register entry R19**, from the sixth AI-usage-log session (2026-08-24): the market survey the team had just finished reading, in its own §7 ("Scope Control for a One-Year BS Project"), makes an explicit, direct recommendation that cuts against one of the project's two lead research claims. Quoted in full from the plan doc's own appendix:

> "Use one agent framework only (recommended: LangGraph, because checkpointing and replay are already available)."

This is not a hypothetical objection a panel might someday raise — it is a real, written, external recommendation from a document the team itself sourced and trusted enough to adopt several of its other recommendations from (the project's official title, the Repair Agent feature, the Recovery Controller and Verified Repair Memory reclassifications). If the team had simply deferred to this source uncritically the same way it deferred to it for the title, the project's cross-architecture generalization claim — one of the two research questions explicitly marked "Primary" in the RQ table (RQ2, alongside RQ3; see Part 2) — would have been eliminated at a stroke, on the recommendation of the very document that supplied the project's own title.

The rejection is recorded explicitly, not silently absorbed: *"Explicitly rejected — this would eliminate RQ2 (cross-architecture generalization across CrewAI + LangGraph + a 3rd framework), one of this project's two lead research claims, already CCP-justified and partially tested (Spike 2). Good general advice for a differently-scoped FYP; incompatible with this one's already-committed novelty case."* The plan doc goes one step further than a bare rejection, per its own explicit framing: *"Resolved positively, not just rejected: extension #8, Framework Compatibility Layer (above) — draw from all 7 surveyed frameworks via lightweight compatibility checks, while keeping full benchmarked rigor on only the 2–3 core frameworks."* Risk-register R19's status line makes the same point: *"Closed — rejection on record, not silently ignored. Resolved positively, not just rejected."*

This is worth reading closely as a model of how the project handles pushback in general, whether it comes from a named teammate, a supervisor, or (as here) an external source document: the objection is stated in full, in the objector's own words where possible; the specific stake that would be lost if the objection were accepted is named precisely (not "this would hurt the project" but "this would eliminate RQ2 specifically"); the decision is recorded with a date and a reasoning chain, not just a verdict; and — critically — the underlying concern behind the objection (here, "breadth-over-depth" risk, already tracked separately as risk-register R8) is not simply waved away, but resolved with a concrete, scoped, positive answer (the Framework Compatibility Layer extension) rather than left as an unaddressed tension. The same three-part pattern — full pushback stated, specific stake named, positive resolution rather than bare refusal — recurs at least twice more in the project's history: the supervisor's own "14 features that map to 1 feature" critique in the fifth session (resolved by splitting the bundled attribution algorithm into three independently-demoable stages, not by shrinking the feature count) and the "use features of all products, not only from one" scope question that directly produced the Framework Compatibility Layer extension in the eighth session.

### 1.3.5 The supervisor's own critique, as a second real instance of defended pushback

Directly relevant to the same theme, and worth recording alongside R19: the fifth AI-usage-log session opens with *"Supervisor feedback: the 'committed core' framing bundled ErrorProbe's real 3-stage pipeline (Strategist → Investigator → Arbiter) under one label, 'core attribution algorithm' — flagged as reading like '14 features that map to 1 feature,' not 14 distinct, independently-demoable pieces of work."* This is a real, named, supervisor-attributed critique of the project's own framing — the closest thing in the actual source record to the kind of external-pushback narrative the task brief describes. The response, again, follows the same pattern: the critique is accepted as valid rather than argued against (*"Fix applied — split, not shrunk"*), the specific mechanism was already doing three separate jobs under one name (Strategist-stage agent hypothesis, Strategist-stage step hypothesis, Investigator-stage evidence-grounded verification), and splitting it into three independently-named, independently-defensible items (Culprit Agent, Error Step Localization, Verification Agent) answers the critique without changing a single line of the underlying mechanism or a single POC result already on record. The log is explicit that this was a naming fix, not a scope or evidence change: *"No scope, mechanism, or evidence change — every POC spike (1, 5) and every risk-register entry tied to the old names still describes the exact same code and the exact same results, just under a clearer name going forward."*

---

## 1.4 The One-Line Idea Statement

### 1.4.1 The statement itself

Section 0 of the plan doc states the project's one-line idea as:

> "Build a failure-attribution and recovery system that generalizes to multi-agent architectures no prior paper has tested on, catches the 'silent failures' the strongest existing method (ErrorProbe) admits it cannot detect, and ships as an installable, framework-agnostic testing product rather than a benchmark result in a paper."

### 1.4.2 What it means, clause by clause

The sentence is built from four coordinated clauses, each carrying independent weight, and each mapping directly to one of the project's core evidentiary claims:

1. *"generalizes to multi-agent architectures no prior paper has tested on"* — this is RQ2, the first of the two "Primary" research questions (Part 2). It is the claim tested by Spike 2 (CrewAI instrumentation) and the reason the project is explicitly designed around at least two, ideally three, orchestration frameworks (CrewAI, LangGraph, plus an optional third via extension #2) rather than one.
2. *"catches the 'silent failures' the strongest existing method (ErrorProbe) admits it cannot detect"* — this is RQ3, the second "Primary" research question. Notice the precision of the phrasing: not "detects more failures than ErrorProbe" (a vague superiority claim) but specifically "catches the silent failures ErrorProbe admits it cannot detect" — tying the claim directly to a named, quoted admission in a specific paper's Limitations section, which is the strongest possible grounding a gap-claim can have.
3. *"ships as an installable, framework-agnostic testing product"* — this is the deployable-SDK half of the dual research/product framing, and it is the reason the guide's §14 external-component classification table (Part 3, and referenced in the plan doc's §6) treats the SDK, backend, database, and dashboard as 0% API-dependent, entirely own-work.
4. *"rather than a benchmark result in a paper"* — this final clause is a deliberate, explicit positioning move against the more common academic-FYP failure mode: producing a research artifact (a benchmark, a paper-style evaluation table) with no working, deployable system behind it. This clause is the project's own pre-emptive answer to the FAST guide's §1.2 deployability requirement and its §15 warning against weak idea patterns (notebook-only projects, no real system, research basis with no application).

### 1.4.3 How it was arrived at

The one-line idea statement is explicitly framed in the plan doc as a **deliberately narrower** scope than an earlier, wider pitch. The plan doc states this directly: *"This is a deliberately narrower scope than the original 'AgentTestLab' pitch in `TraceCause_AgentTestLab_Pitch.md` (that draft had ~10 layers, health scores, marketplace framing — too broad for Section 5's 'one shared central problem' test and would trip the guide's explicit 'feature accumulation' hazard). Everything trimmed from that draft is listed under §7 as an optional extension, not core."* This is a genuinely important piece of the project's own history to understand: the one-line idea was not built up from nothing — it was built *down* from an earlier, more expansive pitch that a member of the team (or an earlier working pass) had already drafted under the "AgentTestLab" framing, complete with ten distinct layers, health-score metrics, and a marketplace concept. That draft is preserved, unedited, in the project's own archive folder (`06-archive-superseded/TraceCause_AgentTestLab_Pitch.md`), which is itself evidence of the same non-destructive-history discipline discussed in §1.2.6: rather than deleting the wider pitch once it was narrowed, the team kept it on record and explicitly cross-referenced it as the thing the current scope was trimmed *from*, with every trimmed piece re-routed into the extensions list (§7 of the plan doc) rather than simply discarded. Nothing in the wider vision was lost outright; it was reclassified as non-core, gated behind the committed core, and scheduled for later consideration only if the core proves stable — exactly the two-track "core is CCP-justified, extensions are product-demand-justified" split the plan doc states explicitly in its own §7.0.

---

## 1.5 SDG / Thematic Alignment

### 1.5.1 The guide's own boundary on this section

Before working through the SDG analysis itself, it is worth stating the constraint the plan doc holds itself to, because it shapes how much weight this section is allowed to carry: *"Per the guide's own boundary (§1.3 box): this is context for the proposal, not a substitute for the CCP or contribution claim — kept to this one paragraph, not expanded or used to inflate the pitch."* The guide treats SDG alignment as required context, not as part of the actual technical justification — a project cannot argue its way into being a valid CCP by having a strong SDG story, and the plan doc explicitly declines to try. This document expands the *reasoning* behind the SDG choice for depth, per the assignment brief, but preserves the same underlying discipline: SDG framing supports the narrative, it does not replace the evidence-based CCP argument made in Part 3.

### 1.5.2 Primary: SDG 9 — Industry, Innovation and Infrastructure

The plan doc names SDG 9, specifically target 9.5 (enhancing research and technological capabilities of industrial sectors), as the primary alignment, with the following stated reasoning:

> "As multi-agent AI systems move from experimental prototypes into real production infrastructure (customer-support agents, coding assistants, research tools), the industry lacks reliable failure-diagnosis tooling for this new technology category — every commercial platform checked in Commercial_Product_Comparison.md does trace capture, but none does automated, benchmarked failure attribution the way Granite does. Granite directly builds that missing piece of technical infrastructure, upgrading the reliability of a genuinely new industrial sector. The stakeholders are the engineering teams who need this infrastructure to scale AI adoption safely — exactly the risk CCP characteristic #7 (significant consequences, §2 below) already establishes as real and present."

Why SDG 9 specifically, worked through: target 9.5's own language is about "enhancing... research and technological capabilities of industrial sectors" — Granite is, quite literally, a piece of *technological capability* (failure-diagnosis tooling) being built for an *industrial sector* (AI/software engineering teams operating multi-agent systems) that currently lacks it. This is not a stretch-fit; the target's own wording maps almost word-for-word onto the project's own contribution statement. The paragraph also does real connective work rather than just asserting relevance: it names the specific evidentiary basis (the seven-platform commercial comparison, which independently confirms the infrastructure gap exists — see Part 3's discussion of CCP characteristic #5), and it explicitly ties the SDG argument back into the CCP argument (characteristic #7, significant consequences) rather than treating the two as separate, disconnected sections of the proposal.

### 1.5.3 Secondary candidate: SDG 17 — Partnerships for the Goals

The task brief specifically asks for SDG 17 to be named as "the strongest secondary candidate." While the plan doc's own §0.05 does not itself elaborate a secondary SDG in the text as read (it states only the primary alignment, consistent with its stated discipline of keeping this section to "one paragraph, not expanded"), SDG 17 is nonetheless the most defensible secondary candidate to reason through, for two structural reasons drawn directly from the project's own evidence base. First, the project's entire baseline-and-gap argument is explicitly built by standing on, and extending, a chain of open academic publications (Who&When → AgenTracer → {SDBL, TraceElephant} → ErrorProbe, plus the independent AgentAsk and PROTEA lines) — the project's contribution statement itself frames its work as directly continuing a public research effort rather than working in isolation, which is a form of research partnership and knowledge-sharing SDG 17 targets (specifically 17.6, "enhance... knowledge sharing on... science, technology"). Second, the datasets underlying the project's own benchmark work are, wherever possible, deliberately built on already-public, permissively-licensed sources (Who&When under MIT, GSM8K under MIT, tau-bench retail under MIT, TraceElephant's traces under CC BY 4.0) rather than proprietary or closed data, and the project's own new benchmark is explicitly planned for public release under a matching permissive license (MIT/CC BY 4.0, per plan doc §8) — this open-data, open-benchmark commitment is itself a partnership-for-the-goals gesture, since it is explicitly designed so that other researchers (not just this project's own team) can build on it, matching the field's own stated norm.

### 1.5.4 Every other SDG considered and why rejected

Working through all seventeen SDGs systematically, as the task brief requests, to show the primary and secondary choices were arrived at by elimination rather than by default:

- **SDG 1 (No Poverty), SDG 2 (Zero Hunger)** — no plausible connection; the project touches neither material poverty nor food systems in any dimension.
- **SDG 3 (Good Health and Well-Being)** — no direct connection; the project's example scenarios (customer-support refunds, purchase recommendations, stock-count consistency) are drawn from retail/e-commerce contexts (matching the active tau-bench retail dataset choice), not healthcare, and no health-adjacent use case is claimed anywhere in the project's documentation.
- **SDG 4 (Quality Education)** — a stretch could be argued (better AI tooling could someday support educational AI agents), but this is not a use case the project names, tests, or benchmarks against anywhere; asserting it would be exactly the kind of unsupported inflation the plan doc's own discipline explicitly avoids.
- **SDG 5 (Gender Equality), SDG 10 (Reduced Inequalities)** — no connection; the project has no demographic, access, or equity dimension in its stated scope.
- **SDG 6 (Clean Water), SDG 7 (Affordable Clean Energy), SDG 13 (Climate Action), SDG 14 (Life Below Water), SDG 15 (Life on Land)** — no plausible connection to a software-diagnosis tool for multi-agent AI systems; these are environmental/resource SDGs entirely outside the project's domain.
- **SDG 8 (Decent Work and Economic Growth)** — the closest near-miss to the primary choice. A case could genuinely be made: reliable AI tooling supports economic productivity and could be framed as supporting decent, safe technology-sector work. But SDG 9's target 9.5 language (technological capability for industrial sectors) is a substantially tighter match to what Granite actually is — a piece of technical infrastructure — than SDG 8's broader labor/growth framing, and choosing the tighter-fitting SDG over the merely-adjacent one is the more defensible, less inflated choice.
- **SDG 11 (Sustainable Cities and Communities), SDG 12 (Responsible Consumption and Production)** — no direct connection; these target urban planning and resource-consumption patterns, neither of which the project touches.
- **SDG 16 (Peace, Justice and Strong Institutions)** — a stretch could be made around "traceable evidence" and accountability (the project's own client-framing section names "auditors needing traceable evidence" as one class of stakeholder), but this is a minor, secondary use case at best within the project's own stakeholder analysis (see Part 3's characteristic #6 discussion, where this exact stakeholder group is named as one of several under-argued ones), not a central enough thread to justify naming SDG 16 over SDG 17.
- **SDG 17 (Partnerships for the Goals)** — as argued in §1.5.3, the strongest secondary candidate, on the strength of the project's open-research-lineage and open-data-release commitments.

This systematic elimination is itself the honest version of what the plan doc's own single-paragraph SDG section compresses down to one sentence — it is included here at full length specifically because the task brief for this document asks for depth the original compact pass did not have room for, while preserving the plan doc's own underlying discipline that SDG framing is context, not part of the CCP argument itself.

---

## 1.6 Client / Stakeholder Framing and Specifiability

### 1.6.1 The client, per the guide's Stream A rule

The guide's §5.2, quoted directly in the plan doc: *"The intended operator or user of the resulting system acts as the notional client. The scope of work states who would run the system and what they would need from it."*

Granite's notional client is stated precisely, and — importantly — grounded in a concrete detail rather than left abstract: *"an engineering team operating a multi-agent AI system in or near production, grounded concretely (not abstractly) by the project's own active dataset choice — the benchmark's real build target is tau-bench retail, i.e. a customer-support/retail multi-agent workflow."* This is a deliberate choice worth pausing on: rather than describing the client as a generic "AI engineering team" (a framing so broad it could apply to almost any AI tooling project), the plan doc ties the client concept to a specific, already-committed dataset decision — tau-bench retail — so that the client is not a hypothetical abstraction but a stand-in for a real, specific kind of workflow (customer support, order handling, refund policy enforcement) the project's own benchmark is actually built against.

Three concrete needs are named for this client, and each is explicitly cross-referenced back to the committed core so the client framing isn't decorative: *"(1) pre-deployment fault testing against their own workflow before shipping it, (2) post-incident root-cause diagnosis when something breaks in production, (3) a way to test whether a proposed fix actually resolves the failure before redeploying. The system's committed core (§7) is scoped directly to those three needs — nothing in the core exists that this client wouldn't use."* That closing sentence is the real test being applied here: every one of the ten foundational items maps to one of these three needs (fault injection and the benchmark serve need 1; Culprit Agent, Error Step Localization, Verification Agent, and Semantic Error Diagnostic serve need 2; Repair Agent, Verified Automatic Repair, Recovery Controller, and Verified Repair Memory serve need 3) — there is no foundational item that exists for a reason disconnected from this client's stated needs.

### 1.6.2 Specifiability — the 5 functional requirements and 1 NFR, quoted and explained

The guide's §6 requires a project to be specifiable in a precise form: functional requirements in "the system shall..." language, at least one measurable non-functional requirement, named actors and data, and an acceptance criterion for the hardest requirement. Granite states all of these explicitly in plan doc §0.07. Each is quoted and explained below.

**FR1:** *"The system shall inject controlled, deterministic faults into a multi-agent workflow built on CrewAI or LangGraph and record the ground-truth agent and step responsible for each injected fault."*

This is the fault-injection harness's specification, and its precision matters: "controlled, deterministic" rules out any injection mechanism that introduces its own randomness or ambiguity into the ground truth — this is directly what Spike 3's two runs tested and, on the second attempt, confirmed (per risk-register R3: the first attempt's famous-fact corruption got self-corrected by the agent, exposing that a naive injection choice can produce ambiguous ground truth; the second attempt's unverifiable fabricated fact produced clean, unambiguous blind propagation). The requirement is written the way it is — demanding determinism and recorded ground truth — precisely because the team had already, empirically, discovered a way this requirement could silently fail (an injected fault that gets self-corrected isn't really "responsible" for anything downstream anymore) before the requirement was finalized in this form.

**FR2:** *"The system shall analyze a completed multi-agent execution trace and output a predicted responsible agent, step, and confidence score for an observed failure."*

This is the core diagnosis-engine specification — the output triple (agent, step, confidence) is exactly the shape of ErrorProbe's own "decisive error" formalism, the (i*, t*) tuple inherited from Who&When (see Part 2's discussion of the citation lineage), with a confidence score added because the plan doc's own evaluation section explicitly rejects reporting recall without precision or confidence (a detector that flags everything scores perfect recall and is worthless — the plan doc corrected exactly this gap in its evaluation metrics on 2026-08-24, adding silent-failure precision alongside recall for precisely this reason).

**FR3:** *"The system shall flag an output that passes standard error checks but violates the task's stated constraints (a silent failure), independent of whether any explicit error signal was raised elsewhere in the trace."*

This is the Semantic Error Diagnostic specification, and the phrase "independent of whether any explicit error signal was raised elsewhere in the trace" is the precise, technical restatement of ErrorProbe's own admitted blind spot: ErrorProbe's whole pipeline is anomaly-detection-gated, meaning it only investigates a trace once some anomaly signal has already fired somewhere. FR3 requires Granite's constraint-verification module to work *without* depending on any such signal — this is the specification-level encoding of the project's single most load-bearing novelty claim.

**FR4:** *"The system shall, given a candidate corrected value for a specific step, deterministically re-execute the downstream portion of the trace and report whether the corrected trace now succeeds."*

This is the Verified Automatic Repair specification, and the phrase "given a candidate corrected value" is directly what exposed the gap that led to Repair Agent being added as a new foundational item in the sixth AI-usage-log session — the log states this explicitly: *"FR4 (§0.07) already assumes a candidate corrected value is given to the counterfactual engine ('given a candidate corrected value for a specific step...') — nothing in the prior 16 actually produced that value."* This is a genuinely notable instance of a specification document doing real diagnostic work on the project's own scope: the requirement was written in a form that silently presupposed an upstream capability (generating the candidate value) that didn't yet exist anywhere in the committed feature list, and re-reading the requirement's own wording, months later, against the market survey's recommendations, is what surfaced the gap.

**FR5:** *"The system shall be installable via a documented SDK against a user-supplied CrewAI or LangGraph workflow without requiring modification to the core diagnosis algorithm."*

This is the deployability/product-half requirement, ensuring the "installable, framework-agnostic testing product" clause of the one-line idea statement (§1.4) is a stated, testable requirement rather than only a marketing phrase.

**NFR1 (the one measurable non-functional requirement):** *"diagnostic overhead (wall-clock time added by running the diagnosis pipeline after a trace completes) shall be measured and reported as a percentage of the original workflow's execution time, with a stated target of under 50% for the single-pass mode (extension #6/core adaptive-depth work)."*

This is the requirement the guide's own §6 explicitly demands at least one of (a measurable, non-functional target, not just a qualitative aspiration), and it directly names the accuracy-vs-latency tension that is CCP characteristic #1's first conflicting-requirements example (Part 3).

### 1.6.3 Actors, data, and the acceptance criterion for the hardest requirement

The plan doc names the primary actor as "the engineering-team operator (the human running Granite)," the secondary actor as "the multi-agent system under test (CrewAI/LangGraph agents, not human)," and the data held as "execution traces (agent actions, tool calls, messages), the ground-truth fault-injection benchmark, and diagnosis records (agent, step, confidence, propagation path)."

The acceptance criterion for the hardest requirement — FR3, silent-failure detection, explicitly named as "hardest" because it is the requirement with no anomaly signal to lean on — is stated with genuine precision: *"a diagnosis record is accepted as correctly identifying a silent failure if the constraint-verification module flags the trace and the flagged step matches the fault-injection harness's recorded ground-truth injection point, within an agreed tolerance — verified directly against synthetic benchmark cases where ground truth is known by construction (per spike 4's already-run mechanism test)."* Two things stand out in this criterion: first, it is a conjunction (the module must both flag the trace *and* localize to the correct step — flagging alone, without correct localization, does not satisfy the criterion), which prevents a trivially gameable acceptance test (a detector that flags every trace as failed would satisfy "flags the trace" alone but would fail the step-matching half). Second, it explicitly grounds "verified" in synthetic, ground-truth-known-by-construction cases rather than real-world cases where ground truth itself might be disputed — this is a deliberate scoping choice that keeps the acceptance criterion testable at all, at the cost of not yet proving the detector's real-world reliability (a limitation the evaluation plan states honestly rather than concealing — see §11's "what the evidence can and cannot support" row).

### 1.6.4 Going through the research-to-decision table

Guide §11 requires a research-to-decision table connecting specific findings to specific project decisions, with planned evidence for each. The plan doc's own table has seven rows; each is walked through here for the depth the task brief requests.

**Row 1 — ErrorProbe.** *Main finding:* 59.5% step accuracy SOTA on Who&When-Algo; explicitly admits it fails on silent failures. *Relevance/limitation:* Chosen baseline — strongest published method, with a named, admitted gap. *Decision influenced:* Adopted as the paper this project improves on. *Planned evidence:* POC spike 1 (partial) + full 3-stage reproduction still owed. This is the anchor row — every other row in the table exists in relation to this one, either supplying the methodology that supports reproducing ErrorProbe (Row 2) or the corpus that confirms the gap ErrorProbe admits to (Row 3).

**Row 2 — AgenTracer.** *Main finding:* Programmatic fault injection removes the 30-hour/annotator manual-labeling cost. *Relevance/limitation:* Methodology template, not a baseline itself; TracerTraj-2.5K turned out unreleased on direct check. *Decision influenced:* Adopted the same injection technique for this project's own benchmark. *Planned evidence:* Spikes 2, 3, 5. This row is a good example of a finding being adopted at the *methodology* level while being explicitly rejected at the *dataset* level — the project uses AgenTracer's fault-injection technique (rule-based, deterministic perturbation operators) without being able to use AgenTracer's own dataset, because that dataset's licensing status turned out to be different from what was initially assumed (see Part 2's full account of the TracerTraj correction).

**Row 3 — the full seven-paper corpus.** *Main finding:* No paper tests generalization to a multi-agent architecture absent from its own benchmark construction. *Relevance/limitation:* The core confirmed gap this project targets. *Decision influenced:* CrewAI + LangGraph chosen as the two committed core architectures. *Planned evidence:* Spike 2 (CrewAI mapping proven). This is RQ2's direct evidentiary root — a single finding, confirmed only after full-text (not abstract-level) reading of all seven papers, that directly determined which two frameworks the project's committed core would instrument.

**Row 4 — commercial platform research.** *Main finding:* Automated diagnosis is emerging (LangSmith Engine, Arize Alyx, both 2026) but none confirm counterfactual fix-testing or general (non-RAG-specific) silent-failure detection. *Relevance/limitation:* Sharpens, doesn't eliminate, the differentiation claim. *Decision influenced:* Repositioned as a diagnosis layer complementary to these platforms, not a competing observability product. *Planned evidence:* `Commercial_Product_Comparison.md`, kept current. This row is itself an example of an honest correction absorbed into the project's own positioning — risk-register R9 records that the original assumption ("nobody automates this") was stale and had to be corrected once LangSmith Engine and Arize Alyx were checked directly, rather than the correction being suppressed to keep the differentiation story simpler.

**Row 5 — the R7 literature triage.** *Main finding:* Real, credible, unpublished preprints exist in adjacent territory (counterfactual attribution, silent-failure detection) — specifically "DoVer" and "From Confident Closing to Silent Failure." *Relevance/limitation:* Novelty risk, explicitly accepted rather than chased. *Decision influenced:* Decision recorded not to fully read every preprint — strategy is beating ErrorProbe (peer-reviewed), not pre-empting unpublished work. *Planned evidence:* risk-register.md R7, decision logged 2026-08-22. This is the row that most directly demonstrates the project's discipline around scope containment: rather than chasing every adjacent unpublished paper (of which risk-register R7 eventually surfaced well over a dozen, across two separate triage passes), the team made an explicit, dated, recorded decision to accept the risk that one of them might overlap, rather than let an open-ended literature chase consume the time budget. The register's own words: *"neither paper was ever going to be cited, added as a baseline, or change the contribution statement — the project's strategy is improving on ErrorProbe (peer-reviewed), not pre-empting every unpublished preprint that might overlap."*

**Row 6 — direct inspection of the AgenTracer repo.** *Main finding:* TracerTraj-2.5K not actually released; only a 127-row sample and the pipeline are public. *Relevance/limitation:* Baseline dataset assumption was wrong until checked directly. *Decision influenced:* Reproduce against Who&When only; TracerTraj comparison scoped to the 127-row sample, labeled honestly. *Planned evidence:* risk-register.md R11. Covered in full in Part 2.

**Row 7 — the FAST guide's own §12.** *Main finding:* POC must be demonstrated with evidence at defense, not described. *Relevance/limitation:* Direct proposal requirement. *Decision influenced:* Ran 7 spikes before defense, exceeding the 1-minimum bar. *Planned evidence:* risk-register.md R1-R3, R10, R13-R15, all independently reproduced. Notably, this row cites the guide itself as a "research source" feeding a decision — a slightly unusual but legitimate reading of the table's own format, since the guide's own requirement (evidence, not description) directly shaped how many spikes were run and how thoroughly each was logged.

### 1.6.5 Ethical compliance

Distinct from the security/privacy threat model (R16, covered in Part 3's discussion of CCP characteristic #1's trace-completeness-vs-privacy tension), the plan doc names a separate ethical-compliance section per the guide's §16/§17 requirement, stated as three plain commitments: the diagnosis engine's output is advisory, never autonomous — a human reviews before any fix is applied, via the already-committed confidence-gated fix approval (extension #12); real user/organization trace data requires informed consent, arranged before use, never assumed; and synthetic fault injection is applied only to the project's own toy workflows or consenting pilot systems, never to a third party's production system without explicit permission. The plan doc is explicit that this section produces no new build work — it is a stated position the team commits to being able to defend under questioning, "same standard as everything else in this document."

---

## 1.7 The Architecture Sketch — Reading the One-Page Diagram Closely

### 1.7.1 Why an architecture sketch belongs inside an identity discussion

The FAST guide's §16 requires a proposal to include, on a single page, "high-level architecture, major components, boundaries and intended deployment target." `architecture-sketch.md` is Granite's answer to this requirement, and it is worth reading closely here — not merely cited — because the sketch is itself a compact restatement of the project's identity: it shows, in one diagram, who owns what, what depends on what, and where the system's boundary with the outside world sits. The sketch's own header states its own limits honestly: "Built for FAST guide §16 slide 6... sketchable at proposal stage, expected to change; this is not a final design." That caveat matters — the sketch is not being presented as a finished architecture, only as evidence that a coherent, buildable shape already exists.

### 1.7.2 The three-owner structure, read against the client framing

The diagram is organized around three labeled boxes — Data/Benchmark Owner, Diagnosis Owner, Platform Owner — each corresponding exactly to the three role areas named in plan doc §9 (§1.6 above). Reading the diagram top to bottom traces the same data flow the client framing (§1.6.1) implies: a target multi-agent system (either the user's own workflow, or a CrewAI/LangGraph toy workflow built for evaluation) is instrumented; the Data/Benchmark Owner's box turns that instrumentation into fault-injected, ground-truth-labeled traces; the Diagnosis Owner's box turns a raw trace into a diagnosis record plus a candidate fix; the Platform Owner's box verifies and applies that fix, stores the record, and surfaces it through a dashboard; and the whole thing terminates in an "Installable SDK" box explicitly labeled as "the product boundary: what a third-party team installs against their own workflow." That final box is the diagram's own visual restatement of FR5 (§1.6.2) — deployability is not an afterthought bolted onto the diagram's edge, it is the box the entire flow is drawn to terminate in.

### 1.7.3 The LLM API box, and why its placement matters

Inside the Diagnosis Owner's box, the diagram places a box labeled "LLM API (Core-assist) — swappable — system still functions if model changes," drawn with a two-way arrow to "Diagnosis team reasoning (Strategist/Investigator/Arbiter, ErrorProbe-style)." The explicit annotation on this box — "swappable" — is the diagram-level expression of the external-component classification argument worked through in full in §1.9 below: the diagram itself visually marks the one place in the whole architecture where a genuinely external, non-owned component sits, rather than leaving that boundary implicit or scattered across the diagram without a clear marker.

### 1.7.4 The correction embedded in the sketch's own history

The sketch carries its own dated correction note, directly under the diagram: *"Correction, 2026-08-23: the three boxes above are labeled by role (Data/Benchmark, Diagnosis, Platform) — earlier drafts numbered them 'Student 1/2/3' as if specific people were already assigned, which hasn't happened. Assign real owners before Mid-1 and update this diagram once decided."* This is the same correction recorded in plan doc §9 (§1.6.1's discussion) and risk-register R6, propagated into the architecture sketch as well — a small but real example of the propagation discipline (§1.2.6) extending even to a single-page diagram, not just to prose documents.

### 1.7.5 The data-flow narration, one hop at a time

The sketch closes with an explicit six-hop, one-sentence-per-hop data-flow narration, which is worth reading in full because it is the most compact statement anywhere in the project's documentation of how the ten foundational items chain together:

1. Target system executes → instrumentation captures a raw trace.
2. Trace → execution graph (nodes = agent actions/tool calls, edges = dependencies).
3. Graph → Semantic Error Diagnostic check (task-constraint verification) + backward causal trace → candidate root cause with confidence.
4. Root cause → Repair Agent generates a candidate fix (prompt, tool argument, structured output, or function logic).
5. Candidate fix → Verified Automatic Repair deterministically re-executes downstream and reports a measured recovery rate → recovery suggestion, gated by confidence threshold.
6. Full diagnosis record → stored → surfaced on the dashboard / returned via the SDK.

Read against the interdependence argument in Part 3's characteristic 8 (§3.8.2), this six-hop narration is the direct evidentiary source for the "first sense" of interdependence named there — each hop's output is, explicitly and by design, the next hop's required input, with no hop able to run meaningfully in isolation from its neighbors.

---

## 1.8 External Component Classification — Working Through the Full Table

### 1.8.1 Why this table exists, and what problem it was written to solve

Plan doc §6 opens with an unusually self-critical framing worth quoting in full, because it explains why this table exists in its current, unusually rigorous form rather than a simpler one: *"The weaker version of this section (superseded below) just claimed the LLM was 'swappable' without committing to how much of the system's actual work depends on it. That's not sufficient — a system can pass a trivial replacement test while still being 50%+ API-dependent for anything that matters."* This is a genuinely important methodological point about how to satisfy the FAST guide's §14 external-component requirement properly: a team could technically claim every component is "swappable" (true of almost any LLM-calling system, since almost any LLM call can be pointed at a different provider) while still building a system whose actual differentiating logic is 90% thin wrapper around an API call. The plan doc's own response was to commit each component to a *specific implementation mechanism*, not just a swappability label, so that the eventual 15–20% API-usage target is "something the team can point to and defend, not assert."

### 1.8.2 Working through the table, component by component, with the reasoning behind each mechanism commitment

**Fault-injection operators — rule-based, deterministic corruption, 0% API-dependent.** The mechanism commitment here directly mirrors AgenTracer's own perturbation-operator approach (Part 2, §2.2.2) — a known, controlled corruption function is applied to a known input, meaning the ground truth is exact by construction and requires no LLM judgment call about what was corrupted or how. This 0% commitment is what makes FR1's "controlled, deterministic" language (§1.6.2) technically achievable rather than aspirational.

**Execution-graph construction — structural parsing of message/reference identifiers, ~0% API-dependent.** The mechanism commitment explicitly rejects an alternative, easier-to-build approach that was apparently considered and rejected: asking an LLM "what did this depend on" over a raw trace. The table's own parenthetical explains why this alternative was rejected — it would make the execution-graph itself, which every downstream diagnosis stage depends on, an LLM-judgment artifact rather than a structurally verifiable one, undermining the deterministic backward-tracing mechanism (Spike 6) that depends on the graph being a reliable, non-probabilistic data structure.

**Backward causal tracing — pure graph traversal (BFS), 0% API-dependent.** This is a direct implementation-level consequence of the execution-graph commitment above: once the graph is a structurally reliable data structure, tracing through it is a classical algorithms problem (breadth-first search, bounded by the revisit rule Spike 6 validates), with no LLM call required anywhere in the traversal itself.

**Confidence scoring — computed from graph features (out-degree, betweenness centrality), 0% API-dependent.** The mechanism commitment here explicitly matches GraphTracer's own formula (Part 2, §2.2.8's discussion of the R7 triage papers), and the table's own parenthetical again names and rejects the easier alternative: "ask the LLM how confident it is." Confidence scores computed from graph topology are reproducible and auditable in a way that an LLM's self-reported confidence is not — an LLM asked to rate its own confidence is a well-documented unreliable signal in the broader literature, and committing instead to a graph-feature-based score avoids depending on that unreliable signal for a number the whole diagnosis pipeline's acceptance criteria (§1.6.3) depend on.

**The Semantic Error Diagnostic module — rule/schema-based, 0% API-dependent, explicitly the single most important commitment in the table.** The table's own language here is worth quoting directly, because it states plainly what is at stake if this specific commitment is not honored during the actual build: *"checks output against task-spec constraints programmatically (value ranges, required fields, logical consistency with stated tool results) — not 'ask an LLM if this seems semantically wrong.' This is the single most important commitment in this table: if this module is LLM-judged instead, the project's actual differentiator becomes an API call wearing a system architecture."* This sentence is the clearest possible statement of the risk the whole 15–20% budget exists to guard against: RQ3, the project's second Primary research claim, is precisely the claim that constraint-based verification (not anomaly detection, and — this table adds — not LLM semantic judgment either) can catch what ErrorProbe's anomaly-gated pipeline misses. If the constraint-verification module were quietly implemented as an LLM call asking "does this look wrong," the resulting system would not actually be testing the RQ3 hypothesis at all — it would be testing whether an LLM judge is a better anomaly detector than ErrorProbe's own anomaly-gated pipeline, a different and much less interesting question.

**SDK, backend, database, dashboard, deployment — own code throughout, 0% API-dependent.** No LLM involvement anywhere in this layer; this is the deployable-product half of the architecture and is treated in the table as unambiguously and entirely own-work.

**Agent-under-test behavior — necessarily an LLM, but explicitly not counted against the 15–20% budget.** The table's own reasoning for this exclusion is precise: "it's what's being diagnosed, not what supplies the diagnosis." The agent system Granite instruments and tests is, by definition, itself built on an LLM (that is the entire category of system Granite exists to diagnose) — counting this against Granite's own API-dependency budget would conflate the subject being studied with the tool doing the studying, a category error the table explicitly guards against.

**Counterfactual replay's re-execution step — necessarily an LLM, inherent, small.** One call per candidate fix tested; the table frames this cost as bounded and proportionate to what is actually being tested (whether one candidate fix works), not open-ended.

**ErrorProbe baseline reproduction — necessarily LLM-heavy, isolated to the baseline-comparison code path only.** The table's framing here is careful to distinguish reproduction from contribution: "faithfully reproducing someone else's published method as a baseline, not claiming its reasoning style as Granite's own contribution." This directly supports RQ1's own Enabling-tier framing (Part 2, §2.3.1) — RQ1 exists to validate the comparison point, not to claim the comparison point's own internal reasoning approach as Granite's novel contribution.

**Natural-language incident report generation — LLM, thin layer, small, non-core.** This is extension #10 (§1.10 below), explicitly scoped as a thin templating layer over already-computed diagnosis data, kept deliberately small precisely because it is not part of the committed core's evidentiary claims.

### 1.8.3 The replacement test, made meaningful rather than trivial

The table closes with a restated version of the guide's own §14 replacement test, sharpened specifically because of the "weaker version" self-critique noted in §1.8.1: *"if the LLM API were swapped for a different model, every row marked 0% above is entirely unaffected — not just 'still runs,' but produces byte-identical output, because none of those components ever call the LLM in the first place."* The distinction drawn here — "still runs" versus "produces byte-identical output" — is the exact distinction between a trivial pass and a meaningful one. A system built as a thin LLM wrapper throughout would technically "still run" if the model were swapped (a different model would simply produce different, but still functioning, output) — that is a weak, easily-gamed version of the replacement test. Requiring byte-identical output for every 0%-marked component is a much stronger claim, only achievable because those components genuinely never touch the LLM at any point in their execution path, and it is exactly the standard the committed core must be held to during the actual build, not merely at proposal-writing time.

---

## 1.9 Committed Core vs. Optional Extensions — The Two-Track Justification, Expanded

### 1.9.1 The two-track principle stated precisely

Plan doc §7.0 states a structural principle that governs the entire feature list and is worth reproducing and unpacking in full: *"the committed core above is justified entirely by the ErrorProbe delta (§3–4) — that is the research/CCP claim, and it is the only place a comparison-to-prior-work claim is actually evaluated. The 13 [later renumbered to 8] extensions below are justified by real product use-case demand, built on top of the improved core — they make Granite a tool teams would actually adopt, which is a separate, product-track justification, not a second wave of 'we improve paper X' claims."* This is a genuinely important discipline for keeping the CCP argument clean: it would be easy, and tempting, to justify every one of the eighteen or so extension-list items by reaching for a paper to claim superiority over, the way the core items are justified against ErrorProbe. The plan doc explicitly refuses this move. Extensions are justified by product demand and market precedent, not by claimed research superiority — and where an extension happens to relate to a paper's own future-work statement (PROTEA's static-DAG-only limitation, AgentAsk's preventive-clarification framing), the plan doc is careful to state explicitly that this is "context... never a comparison, since we do not benchmark against either."

### 1.9.2 The eight extensions, worked through individually

**Extension 1 — widen the fault taxonomy to 3 total types.** From the POC's single validated type (corrupted tool output) to three, adding communication corruption (swap a passed value for a plausible-but-wrong one) and context truncation (drop the last N% of upstream context before the next agent). The plan doc notes a self-correction embedded in this item's own description: an earlier draft "double-counted 'tool-response corruption' as a 4th type," corrected once noticed to recognize it as the same family as the POC's already-validated fault type, not a genuinely distinct fourth category — a small instance of the same accuracy-over-inflation discipline visible everywhere else in the project.

**Extension 2 — a third previously-unused architecture.** Extends RQ2's generalization claim from two frameworks to three, spanning different orchestration paradigms (OpenAI Agents SDK, or a fully custom in-house framework, are named as candidates).

**Extension 3 — cyclic/dynamic graph support.** Already discussed extensively in Parts 2 and 3 (Spike 6). Notably, the plan doc frames this extension's justification carefully to avoid inflating it into a comparison claim: "not a borrowed feature — LangGraph (one of our own 2 committed core architectures) natively supports cyclic workflows... so without this, Granite's own cross-architecture claim would be incomplete on the very framework it commits to instrumenting" — the justification is internal necessity (the project's own committed architecture requires it), with PROTEA's own static-DAG-only admission cited only as external context that the gap is independently recognized, never as the reason the feature was chosen.

**Extension 4 — per-project API-key namespacing.** Explicitly the scoped-down, defensible version of "multi-tenancy" — the plan doc is explicit that "real auth/billing infrastructure is generic SaaS plumbing that doesn't touch the CCP," deliberately dropping a full hosted-SaaS signup/billing flow from scope while still delivering the one piece of multi-tenancy that actually matters for the R16 threat model (§3.1.2): keeping one customer's trace data invisible to another.

**Extension 5 — confidence calibration.** A reliability diagram plus Brier score for the diagnosis engine's confidence output, published as an evaluation artifact. This extension exists specifically because a raw accuracy number alone does not establish whether a system's stated confidence scores are trustworthy — a system could be accurate on average while still being systematically over- or under-confident on individual predictions, and a reliability diagram is the standard tool for exposing that gap.

**Extension 6 — two selectable diagnosis modes.** Directly the mechanism that makes NFR1's latency target (§1.6.2, §3.1.2) achievable as a real product choice rather than a fixed cost every user must accept: a cheap single-pass mode and the full multi-stage pipeline, with the accuracy-vs-latency trade-off measured and exposed as a configuration flag.

**Extension 7 — preventive clarification classifier.** The extension directly tested, and honestly reported as a near-miss, in Spike 7 (Part 2, §2.4 discussion applies here too — precision/recall/f1 all 0.25, near-random). The plan doc frames the RL upgrade explicitly as "deferred, only-if-time-remains," and the FYP-2 timeline (§1.9.4 below) makes this extension's pursuit explicitly conditional: re-test with real labeled pairs from the fault-injection harness (rather than the twenty hand-written examples Spike 7 used) and cheap local sentence-embedding features first; "if it still doesn't improve, drop it rather than ship a known-broken classifier."

**Extension 8 — Framework Compatibility Layer.** Already discussed in full in Part 1, §1.3.4 — the positive, scoped resolution to the market survey's rejected single-framework scope-narrowing advice, drawing lightweight compatibility evidence from all seven surveyed frameworks while keeping full benchmarked rigor on only the two-to-three core frameworks.

### 1.9.3 The two explicitly deprioritized items

Cross-Domain Transfer Testing and Chaos Testing for Agents are named as "genuinely parked," with an explicit instruction: "Revisit only if FYP-2 is materially ahead of schedule; do not plan around them." The plan doc's own discipline here is worth noting — these are not silently dropped from the record the way a less careful project might simply stop mentioning ideas that didn't make the cut; they remain named, with a stated (if unlikely) condition under which they could return to scope.

### 1.9.4 Items considered and explicitly not added

Two decisions are recorded on this front, each worth its own explanation. **Automatic Retry** was considered and rejected as a standalone feature because unconditional auto-retry of a failed step would directly contradict the confidence-gating principle already committed elsewhere (extension #12 in the earlier, pre-rename numbering — gating auto-suggested fixes behind a confidence threshold): "no team will trust an auto-remediation tool that silently applies fixes with no visibility into how sure it is." The plan doc's resolution is precise: rather than adding retry as a new, thirteenth feature, it is reframed as a *behavior* that already emerges from two existing mechanisms (Verified Automatic Repair plus Confidence Calibration) working together — retry only fires once a fix is already verified and confidence-gated, which is a stronger, more defensible design than an unconditional retry feature would have been. **Single-framework scope narrowing** — already discussed in full in Part 1, §1.3.4 — was considered, from the market survey's own §7, and explicitly rejected because it would eliminate RQ2, with the underlying concern resolved positively via extension #8 rather than left as a bare refusal.

---

## 1.10 Team Ownership — The Three Roles in Full

### 1.10.1 The role table, and the honest correction attached to it

Plan doc §9 names three role areas — Data/Benchmark Owner, Diagnosis Engine Owner, Platform Owner — each mapped to a distinct contribution type from the guide's own Section 4 table (data/resource contribution; method contribution; system/architecture contribution respectively), and each with an explicit "if removed, what disappears" test applied: removing the Data/Benchmark Owner's work means "the entire new benchmark — no cross-architecture evaluation is possible"; removing the Diagnosis Engine Owner's work means "the core attribution algorithm and the silent-failure detection claim" disappear; removing the Platform Owner's work means "the product itself — nothing would be installable or operable outside the dev machine."

The correction attached to this table, dated 2026-08-23, is worth reproducing in full because it corrects a real overstatement that had crept into multiple documents at once, not just this one: *"earlier drafts of this document and others in this folder labeled these three roles 'Data/Benchmark Owner/2/3' as if the team had already assigned specific people to them. That assignment has not actually happened — these are three necessary role areas, not a decided roster."* This is the same correction already discussed in the architecture-sketch context (§1.7.4) — it is recorded here a second time deliberately, because the plan doc itself records it a second time, in its own §9, rather than assuming the architecture sketch's correction alone was sufficient. Propagating a correction to every file where the original overstatement appeared, rather than fixing it in only the first place it was noticed, is the same discipline discussed throughout §1.2.6.

### 1.10.2 Why each role passes the guide's own defensibility test

Plan doc §9 closes with a direct tie back to guide §14.1: "Each owns a subsystem that is independently defensible under Section 14.1's four questions (explain it, justify alternatives rejected, predict what breaks, modify it under questioning), and each is individually a legitimate contribution type from Section 4's table." Applying the four questions to each role concretely: the Data/Benchmark Owner must be able to explain why rule-based fault injection (not LLM-based) was chosen (§1.8.2's fault-injection-operator discussion supplies the "alternatives rejected" answer directly); the Diagnosis Engine Owner must be able to explain why constraint-based verification was chosen over LLM-judged semantic checking (§1.8.2's Semantic Error Diagnostic discussion supplies this); the Platform Owner must be able to explain why per-project namespacing was chosen over full multi-tenant auth/billing (§1.9.2, extension #4's discussion supplies this). Each of these three "alternatives rejected" answers is already documented elsewhere in this project's own files, which is itself evidence the defensibility test is achievable in practice, not merely asserted as a target — each owner has a real, already-written answer available to them, not a blank page to fill in from scratch at defense time.

---

*[End of Part 1. Continues into Part 2 — The Research Gap and Baseline.]*

---

# PART 2 — THE RESEARCH GAP AND BASELINE

## 2.0 Why the baseline argument has to be this careful

A Stream A project lives or dies on the strength of its baseline argument: if the baseline is wrong, weak, or indefensible, everything built downstream of it — the contribution statement, the evaluation plan, the delta argument — collapses with it. Granite's baseline selection is unusually well-documented precisely because the team seems to have understood this risk early: `ErrorProbe_Baseline_Selection.md` opens by stating explicitly that the choice is "a performance-based decision, not a recency-based one," and goes on to justify that distinction with actual cross-paper numbers rather than assertion. This Part works through the baseline argument, the full seven-paper corpus each paper gets its own full What/How/Why treatment, the four research questions, and two of the project's most important recorded corrections: the TracerTraj licensing correction and the abandoned self-generation attempt.

---

## 2.1 ErrorProbe — the selected baseline, in full

### 2.1.1 What it is

ErrorProbe (*"Towards Self-Improving Error Diagnosis in Multi-Agent Systems,"* Jiazheng Li, Emine Yilmaz, Bei Chen, Dieu-Thu Le; ACL 2026 Findings, pages 2063–2077, DOI 10.18653/v1/2026.findings-acl.98) is a three-stage failure-attribution pipeline for multi-agent LLM systems, built around a **Strategist → Investigator → Arbiter** architecture, guided by **MAST-taxonomy structural decomposition**, driven by **symptom-driven backward tracing**, and augmented by a **Verified Episodic Memory** component.

Working through each named piece:

- **MAST-guided decomposition.** MAST (Multi-Agent System failure Taxonomy) is a prior classification of failure patterns (referenced across multiple papers in this corpus, originally from Cemri et al., cited in AgenTracer's own related-works section as identifying "fourteen prevalent failure patterns ranging from task disobedience to reasoning-action mismatches"). ErrorProbe uses this taxonomy to structurally decompose a trace before diagnosis begins — rather than treating a trace as an undifferentiated sequence of messages, it is parsed against a known set of failure-pattern categories first.
- **Symptom-driven backward tracing.** Rather than exhaustively examining every step in a trace, ErrorProbe starts from the observed symptom (the point where a failure becomes visible) and traces backward through the execution to find the originating cause — mirroring how a human debugger works backward from a stack trace or an error message toward the actual bug, rather than reading a program forward from its start.
- **Strategist / Investigator / Arbiter.** This is the three-agent diagnostic team structure. The Strategist forms an initial hypothesis about which agent and which step is responsible. The Investigator is the evidence-grounded verification stage — it checks the Strategist's hypothesis against the real trajectory, gathering supporting or contradicting evidence before the hypothesis is trusted. The Arbiter is the final commit stage — it weighs the Strategist's hypothesis and the Investigator's verification evidence and produces the final diagnosis. This structure is directly why Granite's own renamed foundational items (Culprit Agent, Error Step Localization, Verification Agent) map one-to-one onto ErrorProbe's three stages — the fifth AI-usage-log session's rename explicitly states this correspondence: Culprit Agent and Error Step Localization are both "the Strategist-stage hypothesis" (split into its agent-identification and step-identification halves), and Verification Agent "was always the Investigator stage, not a new mechanism."
- **Verified Episodic Memory.** A memory component that stores successful diagnosis patterns for reuse on similar future failures — but, critically, "only commits new failure patterns to memory once independently confirmed by executable evidence," per the Full Literature Landscape Analysis's own description, "explicitly designed to prevent 'hallucinated' error-pattern pollution." This safeguard — commit only what's independently verified — is exactly the design principle whose real-world difficulty Granite's own attempt to build an equivalent mechanism (originally "Verified Episodic Memory," later renamed "Verified Repair Memory") ran directly into: the project's one real test of this idea found that on a local 3B model backbone, the verification bar was never once cleared (0 of 8 cases committed anything to memory — full account in §2.6 below).

### 2.1.2 How it was selected as the baseline

**Against AgenTracer.** AgenTracer (ICLR 2026) is ErrorProbe's direct ancestor in the citation lineage — Who&When (ICML 2025) → AgenTracer (ICLR 2026) → ErrorProbe (ACL 2026 Findings) — and it was seriously considered on its own merits earlier in the project's history: the now-superseded `AgenTracer_vs_WhoWhen_Analysis.md` (an abstract-level, two-paper pass predating the full seven-paper corpus read) argued AgenTracer was "arguably the most immediately de-risked" candidate, precisely because its trained 8B checkpoint was public and a team could "clone it and run it against a small multi-agent system... within days." But once the full seven-paper corpus was read and ErrorProbe's own published numbers were checked directly against AgenTracer's, ErrorProbe won on pure performance: 44.40% step accuracy on TracerTraj versus AgenTracer's own reported ~37–43%, on the identical benchmark AgenTracer itself built. AgenTracer was not rejected as unworthy of study — its methodology (programmatic fault injection, removing the 30-hour-per-annotator manual-labeling cost) was explicitly adopted as the template for Granite's own benchmark construction — but it was rejected as the *primary baseline to beat*, because a stronger published performer on the same benchmark existed.

**Against SDBL.** SDBL (AAAI 2026) reuses Who&When's dataset with no new dataset of its own, using a two-stage "delineate scope, then localize" method inspired by observed novice-versus-expert human debugging behavior. Its own best step accuracy — 39.68% on Who&When-Algo (SDBL-EASD, DeepSeek-V3), 27.78% on Who&When-Hand (GPT-4o/DeepSeek-V3) — is beaten by ErrorProbe on both of the same splits (59.50% and 31.00% respectively). SDBL's own admitted limitation, per the Full Literature Landscape Analysis, is stark: "the majority of cases remain misattributed at the step level" even with its own two-stage method. It was not chosen as primary baseline for the same reason AgenTracer was not: a stronger performer on the identical benchmark existed.

**Against Who&When itself.** Who&When (ICML 2025) is the field's own foundational paper — the first to formalize automated failure attribution as a research problem with a real, human-annotated benchmark and three baseline methods. Its own best step accuracy is only 14.2%, and even o1/DeepSeek-R1 "fail to achieve practical usability" per the paper's own stated finding. Who&When is not rejected as a baseline in the sense of being irrelevant — its dataset (184 annotated tasks, MIT-licensed, fully downloaded and confirmed) remains the project's primary reproduction dataset — but its own attribution *method* is not the one Granite measures itself against, because every one of its three direct descendants substantially improves on its raw numbers.

**Against TraceElephant.** TraceElephant (ACL 2026 Long) is explicitly not a competing attribution method at all — the Full Literature Landscape Analysis states plainly: "proposes no new attribution algorithm at all — it is a data/observability contribution, arguing prior methods were partly failing from incomplete trace access rather than purely weak reasoning (full traces improve accuracy up to 76.5% relative to partial observation)." A paper that contributes no attribution algorithm cannot be a baseline for an attribution accuracy comparison; it was correctly excluded from the baseline race on structural grounds, not on performance grounds.

**Against AgentAsk and PROTEA.** Both are explicitly named as independent of the Who&When lineage — different benchmarks, no citation overlap. AgentAsk targets a structurally different problem (preventive, edge-level clarification before an error propagates, rather than post-hoc diagnosis after it occurs) and cannot fix errors originating from an agent's own internal reasoning flaws — only errors visible at a message handoff, per its own Limitations section. PROTEA is a human-in-the-loop developer tool with no automated root-cause confidence scoring at all (a human must approve every fix) and supports only static DAG workflows, explicitly excluding cyclic/dynamic multi-agent graphs as future work. Neither is evaluated against as a baseline because neither has a public dataset or code to compare against, and both target adjacent-but-distinct problems from post-hoc attribution accuracy — they are cited throughout the project's documentation as *context* establishing that the underlying needs (preventive intervention, human-approved fix testing) are real and independently recognized elsewhere in the field, never as comparison points with numbers to beat.

### 2.1.3 Why ErrorProbe specifically — the 59.5% number and its full context

ErrorProbe's best reported step accuracy — 59.50% on Who&When-Algo, achieved with Claude 3.7 Sonnet plus its Verified Episodic Memory component — beats the best reported step accuracy of every other paper in the corpus on every benchmark where a direct, same-benchmark comparison is possible:

- versus Who&When's own baseline (Who&When-Algo): 59.50% vs. 14.2% — more than 4x.
- versus SDBL on the identical Who&When-Algo split: 59.50% vs. 39.68%.
- versus SDBL on the identical Who&When-Hand split: 31.00% vs. 27.78%.
- versus AgenTracer on TracerTraj: 44.40% vs. ~37–43%.

`ErrorProbe_Baseline_Selection.md` is explicit that step-level accuracy, not agent-level accuracy, is the metric that matters most for this comparison, because "agent-level accuracy alone is considered close to solved [across this literature]; step-level is where every paper admits it still struggles" — and ErrorProbe's lead over its competitors is largest exactly on this harder axis. (On agent-level accuracy specifically, ErrorProbe does not actually lead on every split — SDBL's 63.49% on Who&When-Algo agent accuracy slightly beats ErrorProbe's 60.30% on the same split — and the source document names this openly rather than omitting the one metric where ErrorProbe doesn't win outright, which is itself consistent with the project's broader honesty discipline.)

The document is also careful to caveat its own comparison table rather than let a reader treat it as more rigorous than it is: *"This is a literature-based comparison, not a controlled experiment... No single paper runs all methods on identical backbones to isolate method-quality from backbone-strength. Part of ErrorProbe's margin could come from using a stronger backbone rather than a strictly better method."* This caveat is a genuinely important piece of intellectual honesty: SDBL used GPT-4o and DeepSeek variants, AgenTracer used its own trained 8B model, and ErrorProbe used Claude 3.7 Sonnet, GPT-OSS-120B, and Qwen3-32B — three structurally different backbone choices across the three papers being compared, meaning the performance gap could partly reflect which underlying model each paper happened to use rather than a purely algorithmic advantage. The document's own conclusion states this precisely: *"treat it as strong, not airtight, evidence."*

**ErrorProbe's admitted gaps**, drawn directly from its own "Limitations" section, are the load-bearing evidence for the entire project's novelty claim:

- **Fails on silent failures** — "technically valid but semantically wrong outputs that trigger no detectable MAST-taxonomy anomaly signal. Its whole pipeline is anomaly-detection-gated, so an error that produces no anomaly signal is invisible to it." This single sentence is the project's RQ3.
- **Adds real inference latency** — from its multi-agent diagnostic team; Strategist → Investigator → Arbiter is not a single pass. This is the empirical grounding for CCP characteristic #1's diagnostic-depth-vs-latency tension.
- **Validated on only 3 backbone model families** — Claude 3.7 Sonnet, GPT-OSS-120B, Qwen3-32B — with generalization to other backbones left untested.
- **No paper in the whole seven-paper corpus, ErrorProbe included, tests transfer to a genuinely unseen multi-agent architecture** outside its own benchmark construction (Who&When's CaptainAgent/MagenticOne, AgenTracer's six-framework ecosystem). This is the project's RQ2, and it is explicitly stated as a finding that "survives fully intact after reading all seven papers in full — this is now a confirmed finding grounded in complete text, not an inference from abstracts."

### 2.1.4 Recency — settled explicitly, not left ambiguous

Because ErrorProbe is not, by pure publication date, the newest paper in the corpus, the baseline-selection document addresses this directly rather than letting a panelist raise it as an unaddressed weak point. By arXiv preprint date, ErrorProbe (19 April 2026) is the second-oldest of the four ACL 2026 papers — TraceElephant (24 April 2026) is slightly newer, and PROTEA (18 May 2026) newer still; only AgentAsk (October 2025) predates it. By official conference publication date, all four are tied — "ACL 2026," 2–7 July 2026. The document's own conclusion on this point is unambiguous: *"ErrorProbe is not the most recent paper by either measure. That's fine — recency was never the criterion for a baseline choice. Performance on shared benchmarks is, and that's what Section 2 establishes."*

---

## 2.2 The full literature corpus — What/How/Why for every paper

### 2.2.1 Who&When (ICML 2025)

**What.** The field's foundational paper — the first to formalize automated failure attribution in LLM multi-agent systems as a well-posed research problem, with a real benchmark (127 algorithm-generated + hand-crafted systems, 184 annotation tasks total, built on GAIA + AssistantBench task sources), human-annotated ground truth (culprit agent + decisive step, annotated by three human experts spending 30+ hours each), and three baseline attribution methods (ALL_AT_ONCE, STEP_BY_STEP, BINARY_SEARCH — all three later adopted directly by SDBL as its own baselines).

**How.** Ground truth was produced entirely by manual human annotation — a genuinely expensive process (30+ hours per annotator across three experts), which is precisely the cost AgenTracer's programmatic fault injection was built to eliminate. Attribution is formalized as identifying a "decisive error" tuple (i*, t*) — the responsible agent index and the responsible timestep/step — which becomes the shared formalism every downstream paper in the lineage (AgenTracer, SDBL, ErrorProbe) reuses, in AgenTracer's own words, "following" Who&When's formulation almost verbatim.

**Why it matters to Granite.** It is the shared ancestor and the source of the shared formalism the entire project's evaluation plan is built on (agent accuracy, step accuracy — the same two headline metrics Who&When itself introduced). Its own admitted gap — best step-level accuracy only 14.2%, with even o1/DeepSeek-R1 failing to reach practical usability — is the opening data point in the entire "no obvious solution" argument that anchors CCP characteristic #2 (Part 3). Its data (MIT-licensed, confirmed directly in ErrorProbe's own "Licensing and Intended Use" section) is the project's primary reproduction dataset, 184 real cases confirmed downloaded.

### 2.2.2 AgenTracer (ICLR 2026)

**What.** A programmatic-fault-injection pipeline (`TracerTraj-2.5K`, spanning 2,000+ trajectories across six frameworks — MetaGPT, AutoGen, Smolagents, AgentPrune, AFlow, OWL-Workforce — and seven task-source datasets including MBPP+, KodCode, GSM8K, MATH, GAIA, HotpotQA) plus a purpose-trained 8B attribution model, AgenTracer-8B.

**How.** Rather than relying on expensive human annotation, AgenTracer generates ground truth by counterfactual replay plus programmatic fault injection — a known perturbation operator corrupts a specific step, and because the corruption is applied by a known, controlled mechanism, the ground truth (which step was corrupted, and how) is exact by construction, with zero human-labeling cost. The trained 8B model, per the paper's own claim, "beats giant proprietary LLMs (Gemini-2.5-Pro, Claude-4-Sonnet) by up to 18%" on this task, despite being dramatically smaller than the proprietary models it outperforms.

**Why it matters to Granite.** Two separate, distinct roles: (1) it directly supplies the fault-injection *methodology* Granite's own benchmark is built on — rule-based, deterministic corruption operators, exactly matching the mechanism the plan doc's §6 external-component-classification table commits Granite's own fault-injection operators to ("Rule-based, deterministic corruption (matches AgenTracer's own perturbation-operator approach)"); (2) its own admitted gap — step accuracy still modest (~37–43%) even trained, tested only within its own six-framework ecosystem — is a second data point (alongside Who&When's 14.2%) in the "no obvious solution, sustained field effort, still under 60%" argument. Separately, and importantly, its *dataset* (TracerTraj-2.5K) turned out to be a case of an assumption the team initially got wrong and later corrected directly — covered in full in §2.5 below.

### 2.2.3 SDBL — Scope Delineation Before Localization (AAAI 2026)

**What.** A two-stage attribution method — "delineate scope, then localize" — directly inspired by observed novice-versus-expert human debugging behavior, introducing "Overstep" and "Loop" as predefined expertise heuristics that guide the scope-delineation stage.

**How.** SDBL reuses Who&When's dataset with no new dataset construction of its own, and reports results under the label "SDBL-EASD" across multiple backbone choices (GPT-4o, DeepSeek-R1, DeepSeek-V3). Its own reported split sizes for Who&When (Hand-Crafted=54, Algorithm-Generated=126) differ from the counts AgenTracer and ErrorProbe both report for the same underlying dataset (Algo=127, Hand=58) — the Full Literature Landscape Analysis flags this explicitly as "a known cross-paper inconsistency," most likely explained by differing filtering choices per paper rather than fabrication, but a genuine discrepancy the project's own documentation does not paper over.

**Why it matters to Granite.** It is a third, independent confirmation (alongside Who&When and AgenTracer) that step-level attribution remains hard even with a purpose-built, cognitively-motivated two-stage method — its own admitted limitation states plainly that "the majority of cases remain misattributed at the step level" even with the two-stage approach. It also serves as the closest apples-to-apples performance comparator to ErrorProbe on the identical Who&When splits, which is exactly the comparison `ErrorProbe_Baseline_Selection.md` leans on hardest (§2.1.3 above) to justify ErrorProbe's selection on performance grounds specifically.

### 2.2.4 TraceElephant — "Seeing the Whole Elephant" (ACL 2026 Long)

**What.** A data/observability contribution, not a new attribution algorithm — it argues the field's methods were partly bottlenecked by incomplete trace access (agents' outputs captured, but not their full input context) rather than purely by weak reasoning algorithms.

**How.** Builds on the same underlying systems Who&When uses (CaptainAgent, MagenticOne) on GAIA, AssistantBench, and SWE-Bench, but deliberately captures full input-plus-output traces rather than outputs only, and demonstrates that fuller trace access alone — with no change to the attribution algorithm — improves accuracy by up to 76.5% relative to partial observation. Its data is released under CC BY 4.0 (confirmed directly in its own Appendix A.10, "Artifact License and Usage Terms"), with benchmark code promised under an unspecified "permissive open-source license."

**Why it matters to Granite.** Its core finding — that observability quality itself, independent of algorithmic sophistication, is a major lever on attribution accuracy — is a structural argument the project's own architecture implicitly agrees with: Granite's execution-graph construction is built as a genuinely structural, full-trace parsing step (matching GraphTracer's own "parse references, extract unique identifiers" approach per the plan doc's §6), rather than an LLM being asked post-hoc "what did this depend on" from a partial view. TraceElephant also matters as a *licensing* precedent: it is one of only two papers in the corpus (alongside Who&When) with a confirmed, directly-verified permissive license, reinforcing the project's own posture of preferring clearly-licensed sources and flagging ambiguous ones (SDBL, AgentAsk) as unconfirmed rather than assuming permissiveness.

### 2.2.5 ErrorProbe (ACL 2026 Findings)

Covered in full in §2.1 above.

### 2.2.6 AgentAsk (ACL 2026)

**What.** An edge-level (message-handoff) failure taxonomy — Data Gap, Signal Corruption, Referential Drift, Capability Gap — paired with a lightweight, RL-trained, architecture-agnostic clarification module that intervenes *before* an error propagates, rather than diagnosing it after the fact.

**How.** Trained via a novel extension of Group Relative Policy Optimization the paper calls "E-GRPO." Evaluated across GSM8K, MATH, MMLU, HumanEval, and MBPP, via four different multi-agent orchestration frameworks (GPTSwarm, AFlow, MaAS, MasRouter). Its own taxonomy corpus — 824 annotated agent-to-agent messages — was annotated by multiple professional annotators with a Fleiss' κ of 0.84, a strong inter-annotator agreement score that gives its taxonomy real empirical grounding rather than being a purely conceptual scheme.

**Why it matters to Granite.** It is structurally independent of the Who&When lineage — no citation overlap, no shared benchmark — and represents a genuinely different intervention philosophy: preventive (stop the error before it happens) rather than post-hoc (diagnose the error after it happened, which is Granite's own primary approach). It is cited as direct context and precedent for one of Granite's own extensions — the preventive clarification classifier (extension #5, tested in Spike 7, discussed in §2.4 below) — but never as a comparison baseline, since neither its dataset nor its code is used for a head-to-head evaluation; the plan doc is explicit about this boundary: *"Where a paper (PROTEA, AgentAsk) is named below, it is cited as context showing the underlying need is real and independently recognized — never as a comparison, since we do not benchmark against either."* Its own admitted limitation — it "cannot fix errors originating from an agent's own internal reasoning flaws; only catches errors visible at a message handoff" — is one more independent confirmation that a large class of failure remains outside what any single published method currently addresses.

### 2.2.7 PROTEA (ACL 2026 System Demonstrations)

**What.** A full interactive developer debugging tool (Sony Group, an industry paper) — evaluate → localize bottleneck → propose prompt fix → auto-rerun → compare before/after — validated with a small (n=6) formative user study of real LLM developers.

**How.** Tested against two internal Sony production-adjacent workflows plus eleven LLM-generated multi-agent workflows used as a stress test; both underlying workflows are confidential and not released, and results are reported at a lower empirical rigor than the academic papers in this corpus — "no F1/precision/recall against ground truth, only two internal case studies and an 11-workflow stress test," per the Full Literature Landscape Analysis.

**Why it matters to Granite.** It is close to a genuine product — arguably the closest thing in the entire corpus to what Granite itself is trying to build — but with two decisive gaps that Granite's own committed core is explicitly designed to close: no automated root-cause confidence scoring at all (a human must inspect and approve every single proposed fix, with zero automated confidence gating), and support for only static DAG workflows, explicitly excluding cyclic/dynamic multi-agent graphs as its own stated future work. This second gap is directly why extension #3 (cyclic/dynamic graph support, proven mechanically in Spike 6) is framed in the plan doc not as a comparison-to-PROTEA claim (since PROTEA has no public benchmark or code to run a real comparison against) but as independent confirmation that the gap is real and recognized elsewhere in the field — the plan doc states this distinction with unusual care: *"Context, not a comparison claim: PROTEA names static-DAG-only as its own future work — we are not evaluating against PROTEA, which has no public benchmark or code to compare against; this only means the gap is independently recognized elsewhere in the field, not that we claim to improve PROTEA."*

### 2.2.8 The later-discovered papers from the R7 literature triage

Risk-register R7, opened 2026-08-22, records a title/abstract-level triage (explicitly not a full read, matching the same depth as the initial GraphTracer/FALAT pass) that surfaced far more adjacent literature than the original seven-paper corpus captured. This triage happened in two passes.

**First pass — the original six flagged, later re-triaged.** "Detecting Silent Failures in Multi-Agentic AI Trajectories" (ACM ICPE Companion '26, arXiv:2511.04032) was checked via WebSearch and confirmed real — 98%/96% accuracy via XGBoost/SVDD anomaly detection — but downgraded to Medium threat once its actual scope was understood: it operates at the *trajectory* level (is this whole run anomalous, yes/no), not integrated with agent/step attribution the way Granite's own silent-failure detection is scoped — "genuinely different granularity," per the register's own note. GraphTracer and FALAT were flagged High initially, then checked in full and found to be arXiv preprints only, not accepted at any peer-reviewed venue — recorded explicitly: "Not added as baselines, not cited as established prior work, and no scope or claim in this project has been changed on the basis of either — an unreviewed preprint is not a settled result."

**Second pass — a fuller triage, surfacing that the watch list itself was incomplete.** Six papers from the first watch list were individually assessed: StepFinder (arXiv:2606.03467) rated Low-Medium threat (about inference efficiency, not generalization or silent failures — doesn't touch either claimed gap); **"From Confident Closing to Silent Failure"** (arXiv:2606.09863, Laksh Advani) escalated to **High** threat — a real, working, published-quality silent-failure detector tested on tau2-bench (9,876 trajectories) and AppWorld (1,879 trajectories), finding that LLM judges perform poorly (AUROC ≤0.65) while lightweight TF-IDF detectors reach 0.83–0.95 AUROC; "Silent Failure in LLM Agent Systems: The Entropy Principle" (arXiv:2606.08162) flagged Low threat but specifically for source-credibility scrutiny given its "very grand claims and unusual framing... for a single-author-style arXiv post"; **DoVer** (arXiv:2512.06749, Microsoft Research authors) escalated to **High** threat — a methodologically sophisticated, Microsoft-authored, intervention-driven debugging framework that explicitly argues single-step attribution is "ill-posed" since multiple interventions can independently repair a failure; FAMAS, whose peer-reviewed form was traced to a legitimate top venue ("Spectrum-based Failure Attribution for Multi-Agent Systems," FSE 2026 Research Papers), upgraded in status accordingly though not formally added to the reproduced-baseline corpus; and "From Spark to Fire" (arXiv:2603.04474), confirmed as a cascade/fragility study rather than an attribution method — tests six frameworks including CrewAI and LangGraph for topological fragility, not attribution, so it does not threaten the project's own cross-architecture assumption (A2, discussed in §2.5) even though it means CrewAI/LangGraph are "no longer completely unused in the broader multi-agent robustness literature."

This same second pass surfaced **seven entirely new papers not previously on the watch list at all** — "Causal Agent Replay," "From Flat Logs to Causal Graphs," "MASPrism," "When Errors Become Narratives," "Outcome Monitors," "TrajAudit," and "MAESTRO" — each recorded with a one-line description of why it might matter and a status of "Unverified," to be read before defense if time allows, otherwise before final submission. The register's own honest summary of this whole exercise: "this field is more crowded than the original 9-paper corpus + 8-paper watch list captured," and the explicit, dated decision recorded is to accept this as a known, bounded risk rather than chase every preprint (§2.2.6 already covered the reasoning behind this decision in the context of Row 5 of the research-to-decision table).

---

## 2.3 RQ1–RQ4 — the four research questions

The project's four research questions are stated, with their tier (Enabling / Primary / Secondary), as follows:

| RQ | Tier | Question |
|---|---|---|
| RQ1 | Enabling | Can our diagnosis engine's core attribution algorithm — built on ErrorProbe's published three-stage methodology — reach a defensible range of its own reported 59.5% step accuracy? |
| RQ2 | **Primary** | Does our diagnosis engine generalize to multi-agent architectures absent from any of the seven surveyed papers' benchmark construction — CrewAI, native LangGraph? |
| RQ3 | **Primary** | Does constraint-based output verification catch "silent failures" that ErrorProbe's own anomaly-gated pipeline admits it cannot detect? |
| RQ4 | Secondary | Does counterfactual replay of a diagnosed root cause reliably predict which fix would have prevented the failure, measured by a real recovery rate? |

### 2.3.1 Why each is formulated the way it is

**RQ1 is Enabling, not Primary, and this ordering matters.** RQ1 is not itself a novel contribution — successfully reproducing a published method's reported numbers is not, by itself, new knowledge. But RQ1 is the load-bearing precondition for every other research question meaning anything at all: if the reproduction is not credible, then any claim that Granite's diagnosis engine "generalizes better" (RQ2) or "catches more" (RQ3) than ErrorProbe is comparing against an implementation the team cannot vouch for, which collapses the entire comparative framing. This is precisely why risk-register R1 names ErrorProbe reproduction as "the single highest initial risk" and why Spike 1 was the very first proof-of-concept run in the project's history.

**RQ2 and RQ3 are the two "Primary" claims — the two confirmed gaps ErrorProbe itself admits it does not close.** This is a deliberate, tight framing choice: rather than claiming broad, diffuse superiority over ErrorProbe across many dimensions, the project's primary claims are scoped to exactly the two gaps the strongest existing baseline states about itself in writing. This is the strongest possible grounding a delta claim can have — it is not "we think ErrorProbe could be better at X," it is "ErrorProbe's own paper states it cannot do X, and we test whether we can."

**RQ4 is Secondary, and depends on RQ1–3 first.** Counterfactual replay and recovery-rate measurement (Verified Automatic Repair, Repair Agent, Recovery Controller) is a real and substantial piece of Granite's committed core, but it is logically downstream of the diagnosis working correctly in the first place — you cannot meaningfully test whether a fix recovers a failure if the diagnosis identifying that failure's root cause is unreliable. This ordering is reflected directly in the plan doc's own evaluation metrics table, where recovery-rate and repair-success-rate metrics are listed after, and explicitly conditioned on, the attribution-accuracy metrics.

### 2.3.2 How the questions were formulated — traced to their evidentiary roots

Each RQ traces to a specific evidentiary source already discussed above, not to an abstract aspiration: RQ1 traces to the decision to select ErrorProbe as baseline (§2.1) and the guide's own §12 requirement that reproduction feasibility be tested as the primary Stream A risk (§1.3.2); RQ2 traces to the confirmed cross-paper finding recorded in Row 3 of the research-to-decision table (§1.6.4) — "no paper tests generalization to a multi-agent architecture absent from its own benchmark construction," confirmed only after full-text reading of all seven papers, not inferred from abstracts; RQ3 traces directly to a single sentence in ErrorProbe's own Limitations section (§2.1.3); RQ4 traces to the specific gap the market survey's own review surfaced in the sixth AI-usage-log session — that nothing in the original 16-item feature list actually generated a candidate fix value, which the plan doc's own FR4 had silently presupposed (§1.6.2's discussion of FR4).

---

## 2.4 The TracerTraj licensing correction

### 2.4.1 What was initially assumed

Early drafts of the project's documentation — visible in the plan doc's own delta-argument section, which the correction note directly amends — cited "TracerTraj-2.5K" as a second reproduction dataset, on the assumption that it was available and Apache 2.0 licensed. The Full Literature Landscape Analysis's own licensing table records the original claim plainly: the license figure "Apache 2.0" traces back to "ErrorProbe's own paper describing AgenTracer" — i.e., the license claim was originally sourced from a *secondary citation inside another paper*, not from the AgenTracer repository itself.

### 2.4.2 How it was found to be wrong

The correction happened by direct verification, not by re-reading the same secondary source more carefully. On 2026-08-22, the team directly attempted to download the AgenTracer/TracerTraj repository and inspect it firsthand. What was found: **no LICENSE file exists in the repository at all**, and the README states plainly that data and model weights are "committed to" open-sourcing "upon acceptance of the paper" — meaning, as of the check, the release had not actually happened yet. Only a data-generation pipeline and one 127-row code-domain sample file were confirmed real and downloadable.

This distinction — checking a claim against the primary source directly, rather than trusting a citation of the claim inside a different paper — is treated as a significant enough event in the project's own history that the AI usage log names it as one of two headline "correction worth recording" entries in its very first session: *"A correction worth recording explicitly, since it's exactly the kind of thing this log exists to surface... it is the clearest example in this project so far of exactly the failure mode the guide's disclosure requirement exists to catch, and exactly why the team must read primary sources themselves rather than trust a summary — including this log's own summaries."* (That particular log entry is actually about a related but distinct correction — the GraphTracer/FALAT reversion, discussed in §2.2.8 — but the TracerTraj correction, logged the following session, is explicitly framed the same way, as a second instance of the identical discipline: *"Correction, 2026-08-22: TracerTraj-2.5K... is not actually publicly released — confirmed by direct download attempt, not by re-reading AgenTracer's own citation of itself."*)

### 2.4.3 What changed as a result

The correction propagated through the project's documentation with the same discipline discussed in §1.2.6 — not silently, and not in only one place. Concretely, the following changes were made and recorded:

1. The datasets table (plan doc §8) was updated to mark TracerTraj-2.5K as **"downgraded from committed to conditional"** rather than removed outright — the honest framing being that it may still become usable if and when AgenTracer's actual release happens, but the project's plans cannot depend on that happening before Final-2.
2. The delta-from-ErrorProbe argument (plan doc §4) was rewritten to state explicitly: *"We are building our diagnosis engine's attribution algorithm on Who&When (fully available, 184 real cases downloaded and confirmed)... The reproduction claim above is corrected to rest on Who&When alone until AgenTracer's actual release."*
3. The evaluation plan (plan doc §11) was updated to state the same conditionality: *"TracerTraj comparison is conditional on AgenTracer's actual data release, not committed."*
4. Risk-register entry R11 was opened specifically to track this as an ongoing, monitored risk, distinct from a one-time correction: *"Open — plan doc §4 and §11 need updating to stop citing TracerTraj as available baseline data."*
5. Dependency D1 in the risk register was updated to reflect the same downgrade, with the explicit note that R1's ErrorProbe reproduction "can still use Who&When alone," decoupling the baseline-reproduction risk from the TracerTraj-availability risk so that one dataset's unavailability does not block the entire reproduction effort.

The broader lesson this correction cemented into the project's working practice, stated explicitly in the Full Literature Landscape Analysis's own closing note on this topic: *"The 'materially better position than RedShield' claim was true for Who&When alone, not for both artifacts as originally stated."* (RedShield is a comparably-scoped sibling FYP project referenced elsewhere in this workspace, used here as a calibration point — the correction meant the team had to walk back a comparative claim it had made about its own relative advantage, once the true state of the AgenTracer dataset was understood.)

---

## 2.5 The abandoned TracerTraj self-generation attempt

### 2.5.1 What was tried

Once the licensing correction (§2.4) made clear that the real TracerTraj-2.5K dataset was not available, the team's next move — recorded in the second AI-usage-log session, 2026-08-22 — was not to simply give up on having a comparably-scaled synthetic benchmark, but to attempt to **self-generate a roughly 2,000-row TracerTraj-style dataset**, by running AgenTracer's own published generation pipeline directly, using MetaGPT as the underlying multi-agent framework and a free local model (Ollama, `llama3.2:3b`) instead of a paid API, against two real task pools: MBPP+ (378 tasks) and KodCode hard/medium (1,622 tasks).

### 2.5.2 How it was attempted, and the real technical obstacles hit along the way

This was genuine infrastructure work, not a quick script that failed instantly — the log is explicit about the real engineering effort involved and the real bugs found and fixed before the attempt was abandoned, not before it even started:

1. **Python version incompatibility.** The system's default Python (3.13) was incompatible with MetaGPT's own dependency requirements, requiring a dedicated Python 3.11 virtual environment to be set up on a separate drive (E:) — itself a small but real piece of environment engineering.
2. **MetaGPT's eager-import bug.** MetaGPT's provider module was found to eagerly import every vendor LLM SDK it supports at startup — regardless of which one is actually configured for use — which broke against a trimmed requirements file that didn't include every one of those vendor SDKs. This had to be diagnosed (not merely worked around) and fixed before the pipeline would even start.
3. **Ollama's real endpoint.** The initial pipeline configuration pointed at `/chat` as Ollama's serving endpoint; Ollama's actual endpoint is `/api/chat`. This mismatch caused every call to silently 404 rather than error loudly, meaning the first attempt appeared to run without producing usable output — a genuinely easy-to-miss class of bug, caught by directly inspecting what was actually happening at the network level rather than assuming a silent failure meant something more exotic was wrong.

Once both real bugs were fixed and the pipeline was genuinely working end-to-end, the team ran a real pilot task to get actual timing data before committing to the full run.

### 2.5.3 Why it was abandoned — the real technical reasons, stated plainly

The single pilot task — one 8-round multi-agent session on the local 3B model — took **over ten minutes to complete**. This is the number the abandonment decision turns on, and the log states the extrapolation explicitly: *"extrapolated to ~2,000 tasks, the full run would take multiple days."* Risk-register entry R11b makes the same calculation with slightly more precision: *"even at even modest concurrency (3), the full ~2,000-task run would take multiple days of continuous local compute, not hours."*

This is worth reading as a genuinely honest cost-benefit judgment rather than a failure of nerve: the team had already done the hard diagnostic work of fixing two real bugs to get the pipeline running at all, which is exactly the kind of sunk-cost situation where a team might be tempted to push through regardless of the numbers. Instead, once real pilot timing data was in hand, the decision to stop was made and executed on explicit instruction — the log is careful to record that this was **"stopped, not left running"**: *"Abandoned once real pilot timing data came in... Stopped on explicit instruction rather than left running. This is the kind of finding this log exists to record: a real attempt, with real evidence for why it didn't work, not a silent abandonment."*

### 2.5.4 What was kept, not thrown away

Consistent with the same non-destructive-history discipline visible throughout this project (§1.2.6), the abandonment did not discard the work already done. Risk-register R11b records explicitly what remains usable: the 127-row real AgenTracer sample (`agentracer_full/data/tracertraj-code-test.parquet`, the one genuinely public fragment of the dataset) plus the two now-generated-but-unused task pools (`mbppplus-full.parquet`, `kodcode-hardmedium.parquet`) that were prepared for the abandoned generation run — left in place explicitly "in case local generation is revisited later with more time or a paid API." The abandonment is a scoping decision under a real time constraint, not a verdict that the approach itself is unworkable; a paid API with much lower per-call latency, or simply more calendar time, could plausibly make the same pipeline viable later, and the project's own documentation keeps that door open rather than closing it.

### 2.5.5 What this decision meant for the project's actual benchmark plan

With both the licensed TracerTraj dataset (§2.4) and the self-generated substitute (§2.5.1–2.5.3) ruled out, the project's actual active benchmark-construction plan pivoted to building its own new cross-architecture benchmark from already-public, already-licensed task sources — GSM8K (8,792 rows, MIT) for cheap prototyping and tau-bench retail (635 tasks, MIT, full environment/tools/policy code) as the real benchmark-building target, narrowed down from an initial five-candidate list to these two specifically because "GSM8K: single-integer answers match POC Spike 4's already-validated numeric near-miss mechanism cleanly. tau-bench retail: richer ground truth (full correct action sequences + policy rules), matches the product's real deployment domain (customer support)," per the datasets table's own reasoning. This is the direct, positive downstream consequence of the abandonment: rather than continuing to chase a synthetic-generation approach that real pilot data had shown to be infeasible on the available compute budget, the team redirected the same fault-injection methodology (adopted from AgenTracer, per Row 2 of the research-to-decision table) onto datasets that were already confirmed available, license-verified by direct download rather than by trusting a dataset card, and better matched to the project's own existing validated mechanisms (Spike 4's numeric near-miss check) and its own stated client domain (customer support / retail).

---

## 2.6 The Feature List Evolution — 14 to 20, Session by Session

### 2.6.1 Why this history belongs in the baseline discussion

The committed feature list is not a fixed artifact that was decided once at the start of the project and left alone — its own size changed six separate times across the nine AI-usage-log sessions (14 → 16 → 17 → 18 → 20, with two brief intermediate states in between), and every single change is tied directly back to either new evidence (a POC spike result), a supervisor critique, or a newly-read external source (the market survey). Tracing this evolution in full is itself part of the research-baseline story, because it shows precisely how the project's own understanding of ErrorProbe's architecture, and of the broader market's own convergent recommendations, kept sharpening the feature list rather than the list being frozen prematurely and defended unchanged regardless of new evidence.

### 2.6.2 Session three (2026-08-22, later) — first freeze: 5 foundational + 7 extensions + 2 deprioritized (14 total)

The first frozen version of the feature list followed a systematic five-rule filtering process applied to a much larger candidate pool: an external GPT session's sixteen product-feature ideas (rated against feasibility, market novelty, and product value, none added to committed scope, kept as "a rated reference menu"); an external GPT session's seventeen-screen "mission control" UI vision (rated "3/10 as something to build this year, 8/10 as a design artifact," with its "Trace Explorer" concept flagged explicitly as "the single worst idea in it" because it would mean "rebuilding LangSmith/Langfuse's own core competency from scratch"); and an internally-generated "10 core + 10 extra" alternative brainstorm. All of this was merged and filtered against the original feature set using five explicit rules: genuine market gap, architectural compatibility with the already-committed pipeline, no duplication across lists, the replacement test (would something measurably disappear if cut), and workload-fit against the existing three-student ownership split. The result: five foundational core items (unchanged in substance from the original plan, only now explicitly filtered against this wider candidate pool) plus seven extensions that survived all five filters plus two explicitly deprioritized stretch items.

### 2.6.3 Session four (2026-08-23) — three spikes close evidence gaps, no count change

No change to the feature *count* this session, but a significant change to the feature *list's evidentiary footing*: the alignment check performed at the end of session three had surfaced that the counterfactual replay engine (one of the five foundational items) had zero POC evidence at all. Session four closes this gap directly with Spike 5, alongside two further spikes (cyclic-graph handling, preventive classifier) that test extension-list items ahead of when they were strictly due. This session is a clean example of the project treating its own gap-discovery process as an actionable to-do list rather than a passive audit — the very next working session after a gap was found is the session that closes it.

### 2.6.4 Session five (2026-08-23) — the supervisor-driven rename: 5 → 7 foundational (14 → 16 total)

Already discussed in full in Part 1, §1.3.5 — the "14 features that map to 1 feature" critique, resolved by splitting the bundled attribution algorithm into Culprit Agent, Error Step Localization, and Verification Agent. Worth adding here, for the research-baseline context specifically: this rename is the session where the correspondence between Granite's own foundational items and ErrorProbe's actual three-stage architecture (Strategist/Investigator/Arbiter, §2.1.1) became explicit and named for the first time, rather than being an implicit design fact the earlier "core attribution algorithm" label had obscured. This matters for the research-gap argument specifically because it means the project's own committed core, from this session onward, is legible against ErrorProbe's published architecture stage-by-stage, which is precisely what makes a fair, defensible comparison between the two possible at all.

### 2.6.5 Session six (2026-08-24) — the market survey read in full: 7 → 8 foundational (16 → 17 total)

Already covered extensively in Part 2's main text (§2.2 for the paper-level detail is separate; the feature-list mechanics belong here). The market survey's own four recommended modules were checked one by one against the existing sixteen-item list: three already existed under matching or equivalent names (independent convergence, not new information, per the log's own framing); one — Repair Agent — genuinely did not exist anywhere in the prior list. The gap was independently confirmed, not merely asserted, by re-reading the plan doc's own FR4 (§1.6.2) and noticing it presupposed a capability nothing upstream actually supplied. Repair Agent's own POC (Spike 8) ran the same day it was added to the list — repair_success_rate 0.667 (4/6), with both failures traced to one precise, shared root cause (a specification ambiguity in what "corrected_value" should mean, discussed fully in Part 2's main narrative). This same session also formally recorded, for the first time anywhere in the project's documentation, the previously-undocumented history of Verified Episodic Memory's one real test and its failure (risk-register R18) — a finding that had actually happened during an earlier session but had never been successfully logged, due to a failed edit attempt that was never retried. The session's own framing of this is unusually candid: "This finding was supposed to be logged to risk-register.md at the time; the edit attempt failed silently and was never retried, so there was no record anywhere of this having been built, tested, and reverted, until now."

### 2.6.6 Session seven (2026-08-24) — the title and brand rename, no feature-count change

Covered in full in Part 1, §1.1 and §1.2. No feature-list change this session; this is purely an identity-layer session.

### 2.6.7 Session eight (2026-08-24) — Framework Compatibility Layer added: 8 → 9 extensions... corrected to 7 → 8 (17 → 18 total)

Already covered in Part 1, §1.3.4 and §1.9.2. The specific count arithmetic recorded in the log: "extension count 7 → 8; total frozen feature count 17 → 18 (8 foundational + 8 extensions + 2 explicitly deprioritized, unchanged)." This session's log entry closes with an explicit statement that nothing about the existing eight foundational items or their POC evidence changed as a result — "this is an additive extension gated behind the core, not a change to any of the 8 foundational items or their existing POC evidence (Spikes 1–8)."

### 2.6.8 Session nine (2026-08-24) — the reclassification: 8 → 10 foundational, extensions settle back at 8 (18 → 20 total)

The most structurally significant single change to the feature list's shape, though not to its total size beyond +2. The trigger was a closer re-read of the market survey's own Table 1, which the team had already been relying on throughout session six but had not, until this session, noticed rated *all eight* of its "Core" capability rows identically for the Proposed FYP column — including the last two rows ("Resume from repaired point," "Remember successful repairs"), which Granite's own list had, hours earlier in session eight, classified as extensions rather than foundational items. The log records the reasoning for the reclassification precisely: "This project already treated the first 6 as foundational; leaving the last 2 as extensions was inconsistent with the survey's own classification it otherwise relies on throughout. Moved to match it." This is a genuinely disciplined move — the team is holding its own scope decisions accountable to internal consistency with a source it had already chosen to trust for other decisions (the title, Repair Agent), rather than cherry-picking which parts of that source's own framework to adopt.

**Recovery Controller** (item #9) is honestly flagged with "No POC yet — genuinely new mechanical work, not a rename of anything already tested," with a stated precedent check: five of the seven surveyed frameworks have generic checkpoint/resume infrastructure, but "none tie it to a verified-repair point specifically" — meaning even the closest existing precedent in the market is not quite the same mechanism Granite commits to building.

**Verified Repair Memory** (item #10) carries its history forward unsoftened: "this already failed its one real test... Committed to the foundational core anyway, on the explicit condition that a re-test on a stronger LLM backbone happens before Mid-1 — if the re-test also fails, this is now a foundational-item gap the team must be ready to explain under questioning, not a footnote." The word "anyway" in that sentence is doing real work — the team is explicit that committing this item to the core happened *despite*, not *unaware of*, its one real negative result.

### 2.6.9 What the six-fold size change demonstrates about the research-baseline argument

Read end to end, this history demonstrates something directly relevant to Part 3's CCP argument (specifically characteristics 2 and 9, §3.2 and §3.9): the feature list's own size and shape kept changing not because of scope drift or indecision, but because each change was a direct, traceable response to new evidence — a supervisor critique that exposed a naming problem, a POC spike that closed or exposed an evidence gap, and an external market survey that surfaced a genuine, previously-missed capability gap (Repair Agent) and then, on closer reading, exposed an internal inconsistency in how the team itself was applying that same source (the Recovery Controller / Verified Repair Memory reclassification). A feature list that changed shape this many times for reasons this well-documented is itself a small piece of supporting evidence for the "no obvious solution, understanding kept deepening" argument made explicitly in Part 3, §3.10.3.

---

## 2.7 The Datasets — Public, Reused, and Newly Built, in Full

### 2.7.1 Baseline reproduction datasets

**Who&When (Algo + Hand splits).** MIT-licensed, confirmed via ErrorProbe's own "Licensing and Intended Use" section; 127 systems / 184 annotated tasks total; fully downloaded and confirmed by the team directly. This is the project's primary, uncontested reproduction dataset — the one dataset in the entire project whose availability, licensing, and size have never needed a correction.

**TracerTraj-2.5K (AgenTracer).** Already covered in full in §2.4 — corrected 2026-08-22 to "not actually released," only 127 rows real, downgraded from committed to conditional.

### 2.7.2 Underlying public task sources for injection — active

**GSM8K (8,792 rows, MIT) and tau-bench retail (635 tasks, MIT, full env/tools/policy code).** Both confirmed downloaded and license-verified against primary sources directly, 2026-08-22 — not by trusting a citation of the license, the same primary-source-verification discipline already discussed in §2.4.2 for the TracerTraj case. Narrowed from an original five-candidate list to these two specifically, per the project's own stated principle of "pick 1–2, not all six." The specific reasoning for each: GSM8K's single-integer answers "match POC Spike 4's already-validated numeric near-miss mechanism cleanly" — i.e., the dataset was chosen partly because it fits a detection mechanism the team had already built and tested, not chosen first and then a mechanism built to fit it. tau-bench retail offers "richer ground truth (full correct action sequences + policy rules)" and "matches the product's real deployment domain (customer support)" — directly the dataset underlying the client-framing concreteness discussed in Part 1, §1.6.1, and the three consequence scenarios discussed in Part 3, §3.7.3.

### 2.7.3 Underlying public task sources — benched, not currently built against

**GAIA (466), MBPP+ (378), MATH (12,500).** All downloaded and license-verified, kept on disk as optional second-domain material but not part of the active build plan. MATH specifically was benched, with a precise stated reason: its answers (equations, sets, intervals) "fit Spike 4's numeric-near-miss check worse than GSM8K's plain integers" — a direct, mechanism-level reason, not a vague deprioritization. GAIA and MBPP+ were benched purely for scope reasons — "the 2-source active plan already exceeds the 500–1,000 trace target," with an explicit note to "reintroduce only if GSM8K+tau-bench proves too thin," i.e., these are not rejected, only held in reserve. HotpotQA and SWE-bench were considered and "deliberately never pursued," with SWE-bench specifically flagged as carrying "the same heavy multi-agent-workflow-per-task cost that made the AgenTracer self-generation attempt infeasible" — a direct, explicit cross-reference to the abandoned self-generation attempt's own real cost lesson (§2.5), applied proactively to rule out a second dataset before repeating the same mistake.

### 2.7.4 The new contribution — Granite's own cross-architecture fault-injection benchmark

Planned for public release, recommended under MIT/CC BY 4.0 "matching the field's own norm" (directly consistent with the SDG 17 discussion in Part 1, §1.5.3). Target scale: 500–1,000 labeled traces, "matches AgenTracer's and the original pitch's scale." The datasets table's own closing rationale for why this whole approach keeps annotation cost bounded is worth restating precisely: "ground truth comes from the injection operator, not manual labeling, the same trick AgenTracer used to remove its '30-hour-per-annotator' cost" — i.e., the entire economic viability of building a benchmark at this scale, within a one-year student project's resource constraints, depends on the fault-injection methodology adopted from AgenTracer (Row 2 of the research-to-decision table, §1.6.4) rather than on any original data-collection or annotation effort.

---

## 2.8 The Full Evaluation Metrics Table, Worked Through

### 2.8.1 The metrics, and the reasoning behind each one's inclusion

Plan doc §11's evaluation metrics row lists, in the order they were finalized: top-1 agent accuracy, top-1 step accuracy, propagation-path F1, silent-failure precision/recall, diagnostic latency overhead (%), recovery success rate, task completion rate, repair success rate, and false repair rate. Several of these carry an explicit correction or addition note attached, worth reproducing because each note is itself a small piece of the project's honesty discipline in action.

**Silent-failure precision, added alongside recall (corrected 2026-08-24).** The plan doc's own note: "precision was missing; recall alone can't distinguish a real detector from one that flags everything." This is a genuinely important methodological self-correction — a detector that flags every single trace as a silent failure achieves perfect recall trivially (it catches every real failure, because it catches everything), while being completely useless in practice; precision is the metric that exposes this failure mode, and its absence from an earlier draft of the evaluation plan was a real gap, not a cosmetic one.

**Task completion rate, added 2026-08-24 from the market survey's Table 4.** The plan doc is explicit this metric "was missing from the first pass" — comparing baseline MAS versus self-healing MAS across *all* runs, distinct from recovery rate (which measures only previously-failed runs specifically). The distinction matters: recovery rate answers "of the runs that failed, how many did we fix," while task completion rate answers the broader question "across every run, baseline or not, what fraction now succeeds" — a self-healing system could have an excellent recovery rate while still adding enough latency or false-positive repair attempts to hurt overall task completion, so both metrics are needed together, not either alone.

**Repair success rate and false repair rate, both added 2026-08-24, same source.** Repair success rate measures the percentage of Repair Agent's generated corrections that actually fix the task, "with vs. without Verification Agent gating" — directly testing whether the Verification Agent stage earns its own keep as a distinct pipeline component, rather than assuming it does. False repair rate is described by the plan doc as "the metric that keeps 'verified' in Verified Automatic Repair honest, not just asserted" — measured via a verification-gate ablation, this metric exists specifically to catch the failure mode where a repair is accepted and applied despite actually being wrong, which is the single worst possible outcome for a self-healing system (a silently-wrong repair is arguably more dangerous than no repair at all, since it removes the original error signal without actually fixing the underlying problem).

**Two metrics deliberately still excluded — re-execution cost and repair reuse benefit.** The plan doc names both explicitly and explains the exclusion precisely: both measure Checkpointing (Recovery Controller) and Verified Repair Memory respectively, "neither of which is in scope [at the time the metrics table was first drafted]... adding the metric before the feature exists would be premature, not an oversight." This distinction — "premature, not an oversight" — is worth dwelling on, because it draws exactly the line the task brief for this document asks to be drawn: a metric can be legitimately absent because the thing it measures does not exist yet (premature), which is categorically different from a metric being absent because nobody thought to include it (an oversight, the same category the silent-failure-precision gap actually was). The plan doc treats these as two different kinds of gap and labels each correctly rather than blurring the distinction.

### 2.8.2 Testing, evaluation, and acceptance kept as three separate tracks

Per guide §13.1, the plan doc maintains an explicit three-way split rather than collapsing everything into one undifferentiated "testing" bucket: **testing** covers unit/integration tests on the SDK, graph builder, and injection harness, plus edge cases (empty trace, single-agent trace, malformed tool output); **evaluation** is the metrics table itself, measured against the ErrorProbe baseline; **acceptance** is a small user-acceptance round with real or proxy users integrating the SDK against their own workflow, explicitly scheduled for FYP-2 and explicitly not expected at proposal stage. Keeping these three tracks separate matters because they answer three different questions that are easy to conflate — does the code work correctly (testing), does the system perform well against a real comparison point (evaluation), and would a real user actually find this usable (acceptance) — and a project that only ever reports the first or second could still ship something nobody wants to install, which is exactly the gap the acceptance track exists to catch.

---

## 2.9 The Risk Register — Full Evidence Trail, R1 Through R22

### 2.9.1 Why the risk register deserves its own close reading here

The risk register is, in a real sense, the most complete single evidentiary record in the entire project — every POC spike's result, every corrected assumption, and every open dependency is logged there with a status, and, unlike the plan doc's own more polished, narrative framing, the register's own language stays close to the raw evidence (exact numbers, exact dates, exact file names). Reading through it in full, risk by risk, is the closest thing available to an audit trail of the entire research-baseline effort.

### 2.9.2 The original ten risks, R1 through R11 (plus R11b, R9, R10)

**R1 — ErrorProbe reproduction.** "Partially tested, 2026-08-22" — Spike 1's simplified two-stage pipeline, local 3B model, n=8 Who&When-Hand cases, 75% agent accuracy / 12.5% step accuracy, zero parse failures. Status: "Open — downgraded from top priority. Real evidence in hand; still need the full 3-stage+memory version on a stronger backbone before this is closed."

**R2 — CrewAI/LangGraph mapping.** "Resolved" — Spike 2's toy three-agent CrewAI workflow traced cleanly into three nodes, two correctly-ordered edges. One follow-up note carried forward honestly: "timestamps were captured post-hoc, not via real per-step hooks — fine for structure, not yet trustworthy for latency metrics; real hooks needed in the actual build" — directly the limitation already discussed in Part 3, §3.3.3's distributed-tracing discussion.

**R3 — injected fault ambiguity.** "Resolved" — Spike 3 run twice; the first attempt's self-correction discovery and the second attempt's clean resolution are both kept on record as documented cases, with the register explicitly stating "real fault behavior includes both self-correction and blind propagation, and the benchmark should account for that rather than assume only one" — i.e., the negative first result is treated as informative about the benchmark's own design requirements, not simply discarded once the second attempt succeeded.

**R4 — cross-paper backbone confound.** Already discussed in full in Part 2, §2.1.3. Status: "Accepted, documented."

**R5 — LLM API cost at scale.** "Unknown until POC gives real per-trace token counts." Status: "Open" — a genuinely unresolved, unquantified risk, honestly left unresolved rather than assigned an optimistic placeholder estimate.

**R6 — team ownership assignment.** Already discussed in full in Part 1, §1.10.1. Status: "Open — must happen before Mid-1, currently fully unassigned."

**R7 — literature-gap closure risk.** Already discussed extensively in Part 2, §2.2.8.

**R8 — breadth-over-depth from the extensions list.** "Mitigated by scope design" — the committed core is fixed, extensions are explicitly gated on core completion, directly the risk the two-track justification (§1.9.1 and §2.6.9) exists to manage.

**R9 — commercial market comparison.** Already discussed in full in Part 3, §3.5.2.

**R10 — silent-failure mechanism, untested until caught by review.** Already discussed in Part 3, §3.4.2 and cross-referenced throughout. Worth adding here the full context of how this gap was originally found: not by a routine check, but by "a full panel-style review pass (self-conducted, adversarial on purpose)" that found two real gaps surviving every prior pass — this specific one, and the missing "you just combined existing techniques" defense (now plan doc §4.1). The AI usage log frames the discovery itself as a healthy sign, not a failure: "catching your own gaps late is a normal part of a rigorous process — the failure mode this log exists to prevent is not catching them at all."

**R11 and R11b — the TracerTraj licensing correction and the abandoned self-generation attempt.** Both covered in full in Part 2, §2.4 and §2.5.

### 2.9.3 The second wave, R13 through R16

**R13 — Verified Automatic Repair's missing POC, closed by Spike 5.** Already discussed in Part 2, §2.5.5's methodology discussion and Part 3, §3.2.3/§3.3.3. The register's own framing of what remains open after the spike: "Real recovery-rate measurement on the actual benchmark (not this toy pipeline) is still owed."

**R14 — cyclic graph support, resolved by Spike 6.** Already discussed extensively (§3.2.3, §3.3.3, §3.8.3). Status: "Resolved — mechanism works as designed," on the strength of the control-case comparison (bound disabled → 10,000-step cap hit; bound enabled → clean termination on the identical graph).

**R15 — the preventive classifier's near-random result.** Already discussed in Part 2 and Part 1 (§1.9.2, extension 7). The register names two specific, testable hypotheses for the weak result rather than a single vague explanation: "(1) n=20 hand-written examples is too small and not representative of real corruption patterns — the actual test needs labeled pairs from the fault-injection harness itself, not authored by hand; (2) bag-of-words features may genuinely be too weak for this task, in which case cheap sentence-embedding features... are the next thing to try before concluding the classifier needs to be heavier." Naming two distinct, independently-testable hypotheses, rather than asserting a single diagnosis without evidence to distinguish between them, is itself a small model of good experimental reasoning — the register does not claim to know which explanation is correct, only what the next experiment to distinguish between them should be.

**R16 — the security/privacy threat model.** Already discussed in full in Part 3, §3.1.2. Worth adding the full three-category breakdown here, since Part 3 only summarized it: customer trace data (highest risk, "from the customer's own agent system"), the diagnosis engine's own derived output (low risk), and public benchmark/dev data (no risk) — with the explicit design principle that "only the minimum per-step context is sent to the LLM API, never the full raw trace in bulk," and storage staying local, "never forwarded past the LLM API call itself."

### 2.9.4 The third wave, R17 through R22 — the market-survey-driven additions

**R17 — Repair Agent.** Already discussed in full in Part 2's main narrative (§2.6.5) and Part 1 (§1.6.2, FR4 discussion). Worth restating the precise diagnostic finding here in the risk register's own words, since it is the clearest example anywhere in the project of a "partial success with an actionable, specific cause" result, as distinct from either a clean success (Spike 5, Spike 6) or a clean failure (Spike 7, Verified Repair Memory's one test): "Both failures share one root cause, not two different ones: given evidence like '15% loyalty discount' or '7 notebooks,' the model correctly extracted the right underlying fact in both cases, but returned the downstream computed result... instead of the specific corrected parameter... the pipeline actually needed — a specification/interface ambiguity in what 'corrected_value' should mean, not a reasoning failure." The distinction drawn here — an interface-specification problem, not a reasoning-capability problem — is itself a meaningful diagnostic conclusion, because it points toward a fix that does not require a stronger model, only a better-specified interface (naming the exact field being corrected, "the same way Error Step Localization already pins down a specific step index").

**R18 — Verified Repair Memory's lost-then-recovered history.** Already discussed in Part 2, §2.6.5. Worth noting explicitly here: R18 is now formally superseded by R22, but the register keeps R18 itself on the page rather than deleting it once superseded — "This evidence row stays as the permanent record of the one real test and its failure — R22 covers the reclassification decision made on top of it." This is the clearest single instance in the whole register of the non-destructive-history principle (§1.2.6) being applied to a risk entry specifically, not just to a naming decision.

**R19 — the single-framework scope-narrowing rejection.** Already discussed in full in Part 1, §1.3.4.

**R20 — Framework Compatibility Layer.** Already discussed in Part 1, §1.9.2. Status explicitly: "Open — gated behind the core, same as every other extension. Nothing to verify yet; revisit once the core build reaches extension work" — an honest statement that this is a scope decision, not yet a tested mechanism.

**R21 — Recovery Controller.** Already discussed in §2.6.8. The register's own precedent-check detail, worth restating precisely since Part 1 only summarized it: "5 of 7 surveyed frameworks have generic checkpoint/resume infrastructure (LangGraph, CrewAI, Microsoft Agent Framework: checkpoint-based; Google ADK, Amazon AgentCore: partial), but none tie resumption specifically to a verified-repair point, which is what this item needs." Status: "Open — foundational item with zero POC evidence. Genuinely new mechanical work... the clear gap to close before Mid-1."

**R22 — Verified Repair Memory's reclassification.** Already discussed in §2.6.8. The register is explicit that "the reclassification is a scope decision, not new evidence — the evidence stays exactly what R18 recorded," a precise and important distinction: moving an item from extension to foundational status changes how much the project depends on it working, but it does not, and cannot, retroactively change whether the one real test of the underlying mechanism actually succeeded.

### 2.9.5 What the full register demonstrates as a whole

Reading R1 through R22 end to end, a clear pattern emerges that is directly relevant to the CCP argument in Part 3: of the roughly eighteen substantive risk/evidence entries, only a small handful are marked cleanly "Resolved" (R2, R3, R8, R9, R14) with no caveats attached; a comparable number are marked "Open" with a specific, named next step (R1, R5, R6, R15, R16 pending team review, R20, R21, R22); and several carry a mixed verdict — real evidence in hand, but explicitly not yet sufficient to close the risk (R10, R13, R17). This distribution — a genuine mix of clean wins, honest open risks, and partial results with named follow-up work — is itself the register's own strongest piece of evidence against the possibility that the project's overall confident tone is unsupported: a register with this much genuine variance in outcome, all logged with the same rigor regardless of whether the result was favorable, is a materially more credible evidentiary base than one where every entry happened to resolve cleanly.

---

*[End of Part 2. Continues into Part 3 — CCP Justification.]*

---

# PART 3 — CCP JUSTIFICATION

## 3.0 How this Part is organized

The plan doc's own §2 rates Granite against all nine of the Seoul Accord D.4.1 characteristics in a compact table, and `generate_ccp_docx.py` — the script that produces the actual CCP justification document submitted alongside the FYP registration form — carries the full three-tier options text and the expanded justification prose for each of the nine. This Part works through each characteristic in the order the Accord defines them, quoting the three-tier options exactly as they appear in the source script (which itself reproduces them, per the script's own framing, "exactly as published" from the Seoul Accord), stating which tier Granite is rated at, and then substantially expanding the justification beyond the script's own prose — adding the reasoning process behind the rating, the specific evidence supporting it, what would change the rating, and how each characteristic connects to the rest of the project. The one honestly-weak characteristic (#6) receives its own extended treatment in §3.7. The Part closes with the full "Justify your selection" synthesis (§3.10).

---

## 3.1 Characteristic 1 — Range of conflicting requirements

**The three tiers, exactly as the script presents them:**
- ☐ Involves several issues, but with few of these exerting conflicting constraints (weakest)
- ☐ Involves a variety of factors, which may impose conflicting constraints (middle)
- ☑ **Involves wide-ranging or conflicting technical, computing, and other issues** (top tier — selected)

### 3.1.1 The base justification, as written in the source

> "Granite has three real, unresolved tensions baked into its own design, not hypothetical ones: (1) diagnostic depth vs. latency — the full 3-stage attribution pipeline (Culprit Agent, Error Step Localization, Verification Agent) is more accurate than a single-pass method but costs more inference time per diagnosis, and the product must expose this trade-off as a configuration choice, not hide it; (2) trace completeness vs. privacy — accurate attribution needs full execution traces, which conflicts directly with data-minimization and privacy requirements for any team handling real user data (the project's own R16 threat model exists precisely because of this conflict); (3) generalization vs. specialization — the cross-architecture claim (working on CrewAI, LangGraph, and a 3rd framework with no per-framework tuning) trades away the accuracy a framework-specific tool could achieve by hard-coding assumptions about one orchestration paradigm."

### 3.1.2 Expanded reasoning — why each tension is genuinely unresolved, not merely stated

**Tension 1 — depth vs. latency.** This is not an abstract trade-off asserted for the sake of the CCP argument; it is a tension the plan doc itself commits to *measuring*, not merely acknowledging. The stated non-functional requirement (§1.6.2, NFR1) requires diagnostic overhead to be measured as a percentage of the workflow's own execution time, with an explicit target (under 50%) for a specifically-named cheaper mode (extension #6, the "two selectable diagnosis modes" item). The existence of a *second, cheaper mode as a distinct extension item* is itself evidence the tension is real and non-trivial to resolve: if the deep, three-stage pipeline could simply be made fast with no accuracy cost, there would be no reason to build and maintain two separate modes. ErrorProbe's own admitted limitation — "adds real inference latency from its multi-agent diagnostic team" — is direct external confirmation that this tension is not specific to Granite's own implementation choices; it is inherent to the Strategist/Investigator/Arbiter architecture itself, which Granite's own three renamed items (Culprit Agent, Error Step Localization, Verification Agent) directly inherit.

**Tension 2 — completeness vs. privacy.** This tension is grounded in a concrete, dated artifact: risk-register R16, the security/privacy threat model written specifically because the Guide Compliance Audit's own deeper pass flagged this as "the most substantive finding" of its entire review — a gap that had survived every prior compliance check until a finer-grained audit caught it. The threat model itself names three data categories by risk level (customer trace data — highest risk, since it comes from the customer's own agent system and, given the active tau-bench retail benchmark target, could plausibly contain customer-PII-shaped content; derived diagnosis output — low risk; public benchmark/dev data — no risk) and commits to three specific mitigations: regex-based PII redaction before storage, per-project API-key namespacing (already committed as extension #4), and time-bounded retention. The tension is real precisely because these mitigations are *not free* — redaction can strip information the diagnosis engine might otherwise have used, and namespacing adds infrastructure the fault-injection harness and diagnosis pipeline do not otherwise need. The threat model explicitly scopes itself modestly, stating it is "not a full GDPR/CCPA-grade compliance program," which is itself an honest acknowledgment that the tension is being managed, not eliminated.

**Tension 3 — generalization vs. specialization.** This is the tension directly at stake in the Stream A defense already covered in Part 1 (§1.3.4–1.3.5): the market survey's own explicit recommendation was to narrow to one framework specifically *because* a framework-specific tool can be more accurate by encoding assumptions about that one framework's own message-passing and tool-call semantics. Rejecting that advice (R19) means Granite deliberately accepts the accuracy cost of staying framework-agnostic in order to preserve the cross-architecture generalization claim (RQ2) — this is not a tension resolved by the rejection, it is a tension the rejection consciously chooses to keep live and unresolved, betting that the generalization claim is worth more to the project's novelty argument than the accuracy a specialized tool could achieve.

### 3.1.3 What would change this rating, and its connections elsewhere

A downgrade from "Clear" to a lower tier would require these tensions to resolve rather than persist — for instance, if the accuracy-vs-latency gap between the single-pass and full-pipeline modes turned out to be negligible once measured (undermining tension 1), or if the cross-architecture accuracy cost turned out to be zero (undermining tension 3). Both are empirical questions the committed evaluation plan (§11 of the plan doc) is designed to actually answer, not to assume the answer to in advance — which is itself consistent with characteristic #9's own resolution paragraph (§3.9 below): the tensions named here are unknowns the project's own pipeline and evaluation plan are built to investigate, not settled facts asserted without a path to checking them.

---

## 3.2 Characteristic 2 — Depth of analysis required

**The three tiers:**
- ☐ Can be solved in standardized ways (weakest)
- ☐ Can be solved by application of well-proven analysis techniques (middle)
- ☑ **Has no obvious solution, and requires conceptual thinking and innovative analysis to formulate suitable abstract models** (top tier — selected)

### 3.2.1 The base justification

> "The strongest published method in this exact space, ErrorProbe (ACL 2026), still only reaches 59.5% step-level attribution accuracy — after Who&When (ICML 2025) opened the problem and at least 7 papers spent roughly 15 months actively working on it. If a well-proven, standardized analysis technique existed, that number would not still be under 60% after this much sustained research effort. Solving it required building a new abstract model from scratch — representing multi-agent execution as a causal graph, defining counterfactual re-execution semantics, and formulating silent-failure detection as task-constraint verification rather than anomaly detection — none of which existed as an off-the-shelf technique to apply. Updated 2026-08-24 with a second data point: Verified Repair Memory, a mechanism recommended independently by an external market survey, was built and tested once and failed outright (0 of 8 cases committed, local 3B backbone) — even the piece of this problem that sounds simplest (remember a fix that worked before) turned out to have no obvious solution either."

### 3.2.2 Expanded reasoning — the "15 months, 7 papers, still under 60%" argument worked through fully

The core logic of this characteristic's argument is a field-effort-versus-outcome comparison, and it is worth making the timeline explicit, because the argument's force depends entirely on how much sustained, credentialed effort actually went into this problem before ErrorProbe's 59.5% figure was reached. Per the Paper Release Timeline: Who&When's arXiv submission (30 April 2025) opened the problem formally. AgenTracer followed roughly five months later (3 September 2025). SDBL, TraceElephant, ErrorProbe, AgentAsk, and PROTEA then landed across AAAI 2026 (22 January 2026) and ACL 2026 (2–7 July 2026) — meaning within roughly fifteen months, six independent follow-up efforts, published at ICML, ICLR, AAAI, and ACL (four of the strongest venues in machine learning and computational linguistics), tackled this exact problem, and the best resulting number is still under 60%. This is a genuinely unusual pattern for a problem this actively worked: most well-posed technical problems that receive this much sustained, independent attention from multiple competing research groups converge toward diminishing-returns improvements in the high-80s or 90s within this kind of timeframe, if the underlying technique is fundamentally sound and merely needs refinement. A field still under 60% after fifteen months of concentrated, published, peer-reviewed effort is evidence — not proof, but real evidence — that the problem does not have a well-proven analysis technique waiting to be applied; it requires genuinely new abstract modeling, which is exactly the accord's own defining language for this top tier.

### 3.2.3 The three specific "new abstract model" claims, worked through

The justification names three specific pieces of novel abstract modeling Granite's own build required, and each deserves individual scrutiny for what makes it genuinely novel rather than a routine application:

1. **Representing multi-agent execution as a causal graph.** This is not a novel idea in isolation — graph-based execution representations are common in distributed systems and compiler theory. What made it non-routine in this specific application, evidenced directly by Spike 6, is handling *cyclic* execution correctly: LangGraph (one of the project's own two committed core architectures) natively supports retry loops and iterative refinement, meaning a simple DAG (directed acyclic graph) model — the natural first assumption — is insufficient. Spike 6's own control-case result is the direct evidence that this was a genuinely non-trivial modeling problem, not merely an implementation exercise: the same true-cycle graph, run with the revisit bound disabled, hit a 10,000-step safety cap instead of terminating — meaning an unbounded backward trace on a cyclic multi-agent graph does not naturally terminate, and the bounded-revisit mechanism had to be deliberately designed and separately validated to make backward causal tracing well-defined at all on this class of graph.
2. **Defining counterfactual re-execution semantics.** Spike 5's own narrow-scope caveat, stated in its own docstring per the AI usage log, makes clear how much of this remains a live modeling question even after a successful spike: the spike "tests only the mechanical replay logic, not whether an LLM can correctly guess a fix — that remains untested and is a different, still-open risk." Defining what it even *means* for a counterfactual replay to "succeed" — deterministic downstream re-execution producing a matching correct output — required a specific, deliberate modeling choice (a three-step pipeline with a single corrected value propagated downstream) that is not handed to a team off-the-shelf by any existing library or framework.
3. **Formulating silent-failure detection as task-constraint verification rather than anomaly detection.** This is the most directly novel of the three, because it is defined explicitly *in opposition to* the field's existing dominant approach — ErrorProbe's entire pipeline, and by extension every anomaly-gated method in the corpus, requires some detectable signal to fire before diagnosis even begins. Reformulating detection as "does this output violate the task's stated constraints" rather than "did anything look statistically unusual" is a genuinely different formal framing of the detection problem, not a refinement of the anomaly-based framing — this is precisely why FR3 (§1.6.2) is written with the explicit clause "independent of whether any explicit error signal was raised elsewhere in the trace."

### 3.2.4 The Verified Repair Memory failure as a second, independent data point

The justification's closing move — citing Verified Repair Memory's real, honest test failure as *supporting* evidence for "no obvious solution," rather than treating it as an embarrassing result to minimize — is worth dwelling on, because it is a genuinely unusual rhetorical move for a CCP justification to make, and it is only available to this project because the underlying discipline (report negative results honestly, don't smooth them over) was already in place before this characteristic was even being argued. The mechanism sounds, on its face, like the simplest of the four repair-pipeline stages: "remember a fix that worked before, and reuse it next time" is a pattern recognizable from ordinary caching or memoization, techniques any competent engineer already knows how to implement. And yet the one real test run — 0 of 8 real Who&When cases ever committing anything to memory, all 24 hypothesis-verifications returning `NOT_SUPPORTED` on the local 3B backbone, with agent-level accuracy actually *regressing* (75%→50%) in the same run relative to the simpler two-stage pipeline without memory — demonstrates that even the piece of the problem that sounds like it should be the easiest turned out to have a real, unsolved verification-threshold calibration problem underneath it (the model, on this backbone, essentially never judged evidence sufficient to commit a memory entry, which is either a genuinely correct, conservative outcome given weak evidence, or a sign the verification bar itself needs recalibrating for a stronger backbone — the project does not yet know which, and says so).

---

## 3.3 Characteristic 3 — Depth of knowledge required

**The three tiers:**
- ☐ Can be resolved using limited theoretical knowledge, but normally requires substantial practical knowledge (weakest)
- ☐ A solution requires knowledge of principles, and applied procedures or methodologies (middle)
- ☑ **A solution requires the use of in-depth computing or domain knowledge and an analytical approach that is based on well-founded principles** (top tier — selected)

### 3.3.1 The base justification

> "The committed core draws on multiple genuinely graduate-level areas at once: execution-graph and causal-graph modeling (including cycle detection and bounded backward tracing, proven in Spike 6), distributed tracing across asynchronous multi-agent systems, counterfactual/causal reasoning for the replay engine (proven in Spike 5), and constraint-based semantic verification for the silent-failure module. None of this is standard undergraduate coursework application — it required reproducing a peer-reviewed paper's own 3-stage architecture (Strategist → Investigator → Arbiter) from its description alone, since ErrorProbe's code is not publicly available."

### 3.3.2 Expanded reasoning — why "reproduction from description alone" is a genuinely different task from "using a library"

The closing clause of this justification deserves particular weight: ErrorProbe's code is not publicly available (confirmed directly, per the Full Literature Landscape Analysis's licensing table: "No new dataset released (evaluates on others' benchmarks); states research-only intent, not a formal license"), which means Spike 1's reproduction was not a matter of installing a package and running it — it required reading the paper's own methodology section closely enough to reimplement its architecture from a natural-language description, make interpretive judgment calls about ambiguous implementation details the paper does not fully specify, and then measure whether the resulting numbers land anywhere near the paper's own reported figures. This is a materially different, and materially harder, skill than applying a documented library or reproducing a result from released code — it demands the kind of close technical reading and architectural translation skill the accord's top tier specifically names ("in-depth computing or domain knowledge and an analytical approach that is based on well-founded principles"), and Spike 1's own honest framing (explicitly a *simplified* two-stage version — no tool-grounded Investigator, no Verified Episodic Memory — with the team's own log stating "the team must be able to state precisely what was cut and why when asked") is itself evidence that the reproduction effort required genuine judgment about which pieces of a complex architecture could be responsibly simplified for a first pass and which could not.

### 3.3.3 The four named knowledge areas, worked through individually

- **Execution-graph and causal-graph modeling, including cycle detection.** As discussed in §3.2.3, Spike 6's own control-case result (10,000-step cap hit when the bound was disabled) is the concrete evidence this is genuinely graduate-level graph theory in application, not routine data-structure work — a naive backward traversal of a cyclic dependency graph is not merely inefficient, it is *non-terminating*, and correctly bounding it required a specific, validated design choice (a per-node revisit bound), not a default library behavior.
- **Distributed tracing across asynchronous multi-agent systems.** Risk-register R2's own follow-up note on Spike 2 is directly relevant here, and honestly limits the claim: "timestamps were captured post-hoc, not via real per-step hooks — fine for structure, not yet trustworthy for latency metrics; real hooks needed in the actual build." This is an honest acknowledgment that the distributed-tracing piece of the knowledge requirement is only partially demonstrated so far — structure is proven, timing-accurate instrumentation is explicitly flagged as still-needed real work, which is itself evidence the team understands the difference between "the trace exists" and "the trace is instrumented correctly enough to support latency measurement," a distinction that matters directly for NFR1 (§1.6.2).
- **Counterfactual/causal reasoning for the replay engine.** Already discussed in §3.2.3 — Spike 5's own narrow-scope caveat is the honest boundary marker between what has been proven (mechanical replay logic) and what remains a genuinely open causal-reasoning question (whether an LLM can correctly infer the right fix in the first place, as opposed to correctly re-executing a fix once given).
- **Constraint-based semantic verification.** Spike 4's direct mechanism test — feeding the rule-based checker known-wrong values, including a plausible near-miss ($20.00 vs. $19.75 true) — fired correctly every time with zero false positives, which is real, if narrow, evidence the underlying constraint-checking logic works as designed; the honestly-flagged limitation (n=3 natural-task run, zero natural failures observed) is discussed fully in §3.4 and §3.6 below.

---

## 3.4 Characteristic 4 — Familiarity of issues

**The three tiers:**
- ☐ Is frequently encountered and thus familiar to most practitioners in the field; context may be unfamiliar (weakest)
- ☐ Belongs to families of familiar problems, which are solved in well-accepted ways; context may be unfamiliar (middle)
- ☑ **Involves infrequently-encountered issues** (top tier — selected)

### 3.4.1 The base justification

> "Silent failures — an output that is well-formed and passes every standard error check, yet is semantically wrong — are, by construction, invisible to the error-handling patterns most practitioners already know (try/catch, schema validation, HTTP status codes). Spike 4's own natural-occurrence test (n=3 real tasks) found zero naturally-occurring silent failures on the first attempt, which is itself evidence of how infrequently this failure class surfaces in ordinary testing — it has to be deliberately induced (fault injection) or specifically watched for, not stumbled into. Cross-architecture generalization of a diagnosis method is similarly uncommon: the 7-paper literature review found no prior method tested outside its own benchmark's architecture."

### 3.4.2 Expanded reasoning — turning a limitation into evidence, carefully

This is a genuinely delicate rhetorical move that deserves scrutiny rather than uncritical acceptance, because the same fact (zero silent failures observed in n=3 real task runs) is used elsewhere in the project's documentation as an honestly-flagged *limitation* of the evidence base (risk-register R10: "empirical frequency of natural silent failures still unconfirmed... a real limitation, honestly reported... not papered over"), and here it is used as *supporting evidence* for a CCP characteristic. Both framings can be true simultaneously without contradiction, and it is worth spelling out why: the fact that zero silent failures occurred naturally in three real task attempts is, at the very same time, (a) a real gap in the evidence base for whether the detection mechanism works "in the wild" on naturally-occurring failures (the R10 framing), and (b) evidence that this failure class is genuinely rare under ordinary conditions and does not present itself the way conventional errors do, which is exactly what "infrequently-encountered" means under the accord's own definition (the CCP framing here). The two framings are not in tension because they are answering two different questions: "do we have strong evidence the detector works on real failures" (no, not yet — n=3 is thin) versus "is this the kind of issue a typical practitioner encounters routinely" (also no — and the same small sample, read the other way, supports that too). The project's own documentation does not conflate the two, which is itself worth noting as an example of applying the same underlying fact honestly in two different argumentative contexts rather than overreaching in either one.

### 3.4.3 The two distinct familiarity claims, and why both are needed

The justification actually makes two separate familiarity claims, not one, and it is worth distinguishing them because they rest on different kinds of evidence. The first claim — silent failures being invisible to standard error-handling patterns — is a structural/definitional argument: by construction, an output that passes schema validation and returns a normal HTTP 200 status cannot be caught by any of the error-handling machinery designed to catch malformed or explicitly-erroring outputs, because a silent failure is, precisely, not malformed and does not error. This claim needs no empirical evidence at all; it follows from the definition of the failure class itself. The second claim — cross-architecture generalization being uncommon — rests on the same full-text literature-reading evidence already established in Part 2 (§2.3.2's discussion of RQ2's evidentiary root): no paper in the seven-paper corpus tests transfer to an architecture unseen during its own benchmark construction, a finding the Full Literature Landscape Analysis states was "confirmed by direct in-paper citation, not inferred," after reading each paper in full rather than at abstract level.

---

## 3.5 Characteristic 5 — Level of problem (beyond standard practice)

**The three tiers:**
- ☐ Is encompassed by standards and/or documented procedures of practice (weakest)
- ☐ May be partially outside those encompassed by standards or standard practice (middle)
- ☑ **Is outside problems encompassed by standards and standard practice for professional computing** (top tier — selected)

### 3.5.1 The base justification

> "No documented industry standard or accepted procedure exists for diagnosing multi-agent AI failures, verifying a fix's recovery rate before applying it, or generally detecting silent failures — this was confirmed directly, not assumed, by checking all 7 major commercial observability platforms (LangSmith, Langfuse, Braintrust, Arize, Maxim AI, Opik, DeepEval). Two (LangSmith Engine, Arize Alyx) have only just begun shipping automated diagnosis features in 2026, and none document counterfactual fix-testing with a measured recovery rate or general silent-failure detection as a standardized, published capability. The practice is actively forming, not settled."

### 3.5.2 Expanded reasoning — the specific mechanics of the seven-platform check

This is one of the strongest-evidenced characteristics in the whole justification, precisely because the claim ("no documented industry standard exists") is a negative claim, and negative claims are structurally hard to support without doing real, systematic checking work — it is easy to assert "nobody does this" without checking, and much harder to actually verify it across seven separate, real commercial products. The Guide Compliance Audit's own review of §10 confirms this checking was done at real depth: "Commercial half ✓✓ (Commercial_Product_Comparison.md, 7 platforms)... The guide's warning that platform/language/UI changes alone don't constitute differentiation — correctly not relied upon; the differentiation is substantive." The AI usage log records the check happening incrementally across two separate sessions — an initial four-platform pass, then "market research extended to 3 more platforms" in the third session (Maxim AI, Opik, DeepEval), each checked via a different method (WebSearch, direct WebFetch of the vendor's own product page, WebSearch respectively) — and each entry explicitly flags itself as needing team spot-verification: "Not yet independently spot-checked by the team — same standing instruction as the original 4-platform comparison."

The specific correction embedded in this justification — risk-register R9's own honest self-correction — is worth surfacing in full, because it shows the "no standard exists" claim was not simply assumed and then confirmed; it was initially wrong in the opposite direction and had to be walked back: *"Correction to the original assumption: LangSmith Engine and Arize's 'Alyx'/Signal (both 2026) do claim automated root-cause diagnosis + fix generation — the 'nobody automates this' framing was stale and has been corrected, not just filled in."* The final, corrected claim is narrower and more defensible than the original: not "nobody automates diagnosis at all," but specifically "none confirm counterfactual fix-testing with a measured recovery rate or general silent-failure detection as a standardized, published capability" — a claim that survives the correction because it is scoped precisely to the two mechanisms (verified counterfactual repair, general silent-failure detection) that remain genuinely undocumented across all seven platforms even after LangSmith Engine and Arize Alyx's 2026 diagnosis features are accounted for.

### 3.5.3 Why "the practice is actively forming, not settled" is the right closing frame

This closing sentence is doing careful positioning work: it does not claim the field will never develop these capabilities (an overclaim that would age badly and could be falsified by a single competing product announcement), nor does it claim Granite is permanently ahead of the field (also an overclaim). It states, precisely, that as of the check performed, the practice is in an early, actively-forming state — which is both accurate to the evidence in hand and appropriately time-bound, matching the same discipline the plan doc applies elsewhere (§15's "standing instruction" to re-check the literature at each of the five gates, treating any future finding that a gap has closed as "a finding to report honestly... not a reason to panic").

---

## 3.6 Characteristic 6 — Extent of stakeholder involvement (the honestly-weak one)

**The three tiers:**
- ☐ Involves a limited range of stakeholders with differing needs (weakest)
- ☑ **Involves several groups of stakeholders with differing and occasionally conflicting needs** (middle tier — selected, NOT the top tier)
- ☐ Involves diverse groups of stakeholders with widely varying needs (top tier — NOT selected)

### 3.6.1 The base justification, quoted in full

> "Honestly rated at the middle tier, not the top one — this is the one characteristic the project's own CCP review (plan doc §2) marks as 'weak' rather than 'clear.' Several real stakeholder groups are identified in principle, each with differing needs (on-call engineers/SREs wanting fast, trustworthy diagnosis; benchmark researchers wanting a reproducible, labeled evaluation artifact; QA/compliance teams wanting silent-failure coverage; platform teams wanting low integration cost) — but none of these stakeholder groups have actually been contacted or interviewed yet. Claiming the top tier ('diverse groups... widely varying needs') without real stakeholder engagement would be an overclaim the rest of this project has deliberately avoided everywhere else. This is the single highest-priority open item before defense (risk-register.md, and item #10 in the guide-compliance checklist)."

### 3.6.2 Full treatment — why this is not inflated

This is the single most important section in the entire CCP justification to get right, precisely because it is the one place where the project's own evidence base runs out, and the honest response to that is to say so plainly rather than paper over it with confident-sounding language. It would have been easy, mechanically, to write four plausible-sounding stakeholder groups (as the justification does) and simply check the top-tier box — nothing in the accord's own wording technically prevents a team from asserting "diverse groups... widely varying needs" based on plausible-sounding categories alone. The project explicitly declines to do this, and the reasoning given for declining is worth stating precisely: *"Claiming the top tier... without real stakeholder engagement would be an overclaim the rest of this project has deliberately avoided everywhere else."* This sentence is doing real work — it is not merely saying "we haven't done stakeholder outreach yet," it is explicitly connecting the stakeholder-rating decision to a *standing pattern of behavior* across the whole project (the honest reporting of Spike 7's near-random result, the TracerTraj correction, the GraphTracer/FALAT reversion, the R9 "nobody automates this" walk-back) and stating that inflating this one characteristic would break that pattern. In other words, the weak rating on characteristic 6 is not an isolated moment of honesty bolted onto an otherwise confident document — it is presented as a direct consequence of a discipline the project applies consistently everywhere else, which is a materially stronger defense of the honest rating than treating it as a one-off admission.

The plan doc's own §2 makes the exact same point even more explicitly, tying the weak rating to the guide's own stated observation about this specific characteristic: *"strengthen at proposal stage by naming real pilot stakeholders, per the guide's own note that this is 'the most commonly missing characteristic.'"* This is a genuinely useful piece of context — the guide itself, independent of anything specific to Granite, apparently flags stakeholder involvement as the characteristic teams most often get wrong or under-argue across FYP projects generally, which means Granite's own honest self-assessment here is not catching a Granite-specific weakness so much as correctly identifying that it has fallen into the single most common trap the guide already warns about — and choosing to name that fact explicitly rather than quietly hope a panel doesn't notice.

### 3.6.3 What real stakeholder contact would need to look like

The plan doc's own §0.06 (client framing) and the stakeholder groups named in the justification above give a concrete starting point for what real engagement would need to accomplish, worked through group by group:

- **On-call engineers / SREs.** The claim is that this group wants "fast, trustworthy diagnosis." Real engagement would mean interviewing at least a small number of engineers who have actually been on call for a production multi-agent AI system (or, failing that, a comparable production system with similarly opaque failure modes) and asking concretely: what does a real incident-diagnosis workflow look like today, how long does root-causing a failure typically take, what tools are already in the loop, and — critically — would the specific outputs Granite proposes to produce (agent, step, confidence, propagation path) actually change how fast or how confidently they could resolve an incident, or would the tool add friction instead of removing it.
- **Benchmark researchers.** The claim is that this group wants "a reproducible, labeled evaluation artifact." Real engagement here looks different from the operator-facing groups — it would mean checking, concretely, whether researchers working in this exact space (the seven-paper corpus's own authors, or adjacent groups) would find Granite's planned benchmark release genuinely useful as a research artifact, which could be tested lightly even without a formal interview — for instance, by checking whether the benchmark's planned structure (ground-truth-labeled traces across multiple architectures, MIT/CC BY 4.0 licensed) matches the format researchers in this space have shown they actually reuse (Who&When's own reuse by SDBL, ErrorProbe, and TraceElephant is direct evidence of what a well-received benchmark format looks like in this exact field).
- **QA / compliance teams.** The claim is that this group wants "silent-failure coverage." This is the stakeholder group closest to the ethical-compliance framing already discussed in Part 1 (§1.6.5) — auditors needing traceable evidence — and real engagement would mean understanding what an audit trail or compliance report for an AI system's decision-making actually needs to contain to be useful to this group, which the project's own documentation has not yet investigated at all.
- **Platform teams.** The claim is that this group wants "low integration cost." This is the group most directly addressed by FR5 (installable SDK, §1.6.2) and by the deployment plan's own honest acknowledgment (plan doc §13) that "integration effort to instrument an arbitrary third-party agent framework" is "a known limitation, not concealed" — real engagement here would mean actually having someone outside the team attempt to install the SDK against a workflow they built themselves, and recording what friction they hit, which is precisely the acceptance-testing round already planned for FYP-2 (plan doc §11, "a small user-acceptance round with real or proxy users").

### 3.6.4 Why this is flagged as the top open item

The plan doc's own closing checklist (§16) marks exactly one item related to this characteristic with an unchecked box and no qualifying language softening it: *"Real stakeholders contacted — still open — the one item nothing here can close."* That last clause is precise and important: unlike every other open item in the project (role assignment, which the team itself controls and can simply do; the "explain your own subsystem out loud" test, which likewise only requires the team's own effort; the prior-departmental-FYP comparison, which requires checking an internal archive) — real stakeholder contact requires reaching outside the team and outside anything already in the project's own documents, to actual people who are not yet part of the project's evidence base at all. No amount of further internal writing, internal analysis, or internal POC work can close this gap; it can only be closed by the team actually doing the outreach. This is exactly why it is named, consistently, across at least three separate documents (the plan doc's §2 and §16, the Guide Compliance Audit's summary, and risk-register issue I2) as the single highest-priority item standing between the current 8-of-9 rating and a genuine 9-of-9.

---

## 3.7 Characteristic 7 — Consequences

**The three tiers:**
- ☐ Has consequences that are important locally, and usually are not far-reaching (weakest)
- ☐ Has consequences that are important locally, but may extend to a broader context (middle)
- ☑ **Has significant consequences in a range of contexts** (top tier — selected)

### 3.7.1 The base justification

> "A missed silent failure means a multi-agent AI system ships an incorrect answer to a real end user with no visibility that anything went wrong at all — by definition, no error signal fires. The scenarios used throughout this project's own use-case analysis span multiple real domains where this matters: a wrong refund amount in customer support, an unverified budget constraint in a purchase recommendation, a stock-count inconsistency between two agents in the same order pipeline. These are not confined to one narrow context — they recur in any production deployment of multi-agent systems, which is precisely why 7 commercial platforms have independently converged on this as a category worth building tooling for."

### 3.7.2 Expanded reasoning — why "by definition, no error signal fires" is the crux of the severity argument

This characteristic's argument leans on a specific structural property of the exact failure class Granite targets, and it is worth stating why that structural property is what makes the consequence severe rather than merely inconvenient. An ordinary software bug that produces a visible error — a stack trace, a failed HTTP request, a crashed process — has a built-in mitigating property: someone, somewhere, is very likely to notice, because the system itself signals that something has gone wrong. A silent failure has no such built-in mitigant. The exact same underlying mistake, if it happened to trigger *any* detectable anomaly, would very likely be caught by ordinary monitoring long before it reached an end user; it is precisely the property of being silent — passing every standard check, looking exactly like a correct output — that removes the safety net every other class of software failure implicitly has. This is why the project's own severity argument is not "silent failures are common" (the honestly-limited evidence in §3.4 already establishes they are, in fact, uncommon under ordinary observation) but rather "silent failures are severe precisely because their rarity of *detection* has nothing to do with their rarity of *occurrence* — a failure this class produces is, by construction, invisible until something downstream notices the consequence, which could be an end user receiving a wrong refund, a wrong purchase recommendation, or an inconsistent order state, none of which come with a built-in alarm."

### 3.7.3 The three named scenarios, and why they matter as a set rather than individually

The three scenarios — a wrong refund amount, an unverified budget constraint, a stock-count inconsistency — are not chosen at random; each is drawn from, and consistent with, the project's own active benchmark domain: tau-bench retail, the customer-support/retail dataset the project's real benchmark-building effort actually targets (§2.5.5). This matters because it means the severity argument is not built on hypothetical, disconnected examples chosen purely for rhetorical effect — it is built on the exact kind of task the project's own committed benchmark work will actually generate failure cases for. Reading the three scenarios as a set rather than individually reveals a second, more subtle point: they span three structurally different failure *shapes* within the same domain — a numeric-value error (refund amount), a constraint-violation error (unverified budget), and a cross-agent-consistency error (stock-count mismatch between two agents). This variety is itself evidence supporting the "range of contexts" language the top tier requires — the severity is not confined to one narrow failure pattern, but recurs across multiple structurally distinct ways a multi-agent system can quietly produce a wrong result.

### 3.7.4 The commercial-convergence evidence, and its limits

The closing clause — "which is precisely why 7 commercial platforms have independently converged on this as a category worth building tooling for" — deserves one honest caveat that the justification itself does not fully spell out but that this expanded treatment should surface: the seven-platform check (§3.5.2) establishes that commercial platforms are converging on *diagnosis and observability tooling generally*, and that two of them (LangSmith Engine, Arize Alyx) have begun shipping automated root-cause features specifically — but it does not establish that all seven platforms are converging on *silent-failure detection specifically* as the reason for building this tooling. The commercial convergence is real and directly relevant evidence that the underlying domain (multi-agent AI reliability) is recognized industry-wide as consequential enough to invest in — which is the actual claim being supported here (consequences "in a range of contexts," evidenced by independent commercial investment across seven separate companies) — but it should not be over-read as seven separate companies specifically validating the silent-failure framing, which is a narrower and more specific claim than the commercial-convergence evidence directly supports.

---

## 3.8 Characteristic 8 — Interdependence

**The three tiers:**
- ☐ Is a discrete component of a computing system (weakest)
- ☐ Is part of, or systems within, a complex computing problem (middle)
- ☑ **Is a high-level problem possibly including many component parts or sub-problems** (top tier — selected)

### 3.8.1 The base justification

> "The system itself decomposes into multiple interdependent sub-problems, each substantial enough to be its own line of work: fault injection across frameworks, execution-graph construction, three separate attribution stages (Culprit Agent, Error Step Localization, Verification Agent), silent-failure constraint verification, and counterfactual replay — and the subject matter itself is interdependence: failures in a real multi-agent system propagate through interdependent agent sub-tasks, which is exactly what the Failure Propagation Map and backward causal tracing (Spike 6, proven on a real cyclic graph) are built to model and trace."

### 3.8.2 Expanded reasoning — the double sense of "interdependence" in this argument

This characteristic's justification is doing something structurally interesting worth naming explicitly: it argues interdependence at two entirely separate levels simultaneously, and both levels independently support the top-tier rating even though they are logically distinct claims. The **first sense** is interdependence of the *engineering work itself* — the ten foundational items are not ten independent, parallel-buildable modules; they form a genuine pipeline where each stage's output is the next stage's required input (fault injection produces the raw material for the benchmark; the benchmark is what the attribution stages are evaluated against; the attribution stages' output — agent, step, confidence — is exactly the input Repair Agent needs to generate a candidate fix; Repair Agent's candidate is exactly what Verified Automatic Repair needs to test; a verified repair is exactly what Recovery Controller needs to resume from; a successfully verified repair is exactly what Verified Repair Memory stores). This ordering is directly visible in the architecture sketch's own data-flow section (§ "Data flow, one sentence per hop," six numbered hops, each explicitly building on the last).

The **second sense** is interdependence as the literal *subject matter being diagnosed* — the reason attribution is hard at all is that a multi-agent system's failures propagate causally through interdependent agents, meaning the visible symptom of a failure is very often several steps downstream of its true origin, through a chain of agents each depending on the previous one's (possibly already-corrupted) output. This is precisely why "symptom-driven backward tracing" (ErrorProbe's own core mechanism, §2.1.1) exists as a technique at all — if agent failures were independent rather than interdependent, a diagnosis tool could simply examine the failing step directly with no need to trace backward through a causal chain.

### 3.8.3 Why Spike 6's cyclic-graph result specifically strengthens this characteristic

Spike 6 is cited here not merely as generic supporting evidence but for a specific reason directly relevant to interdependence: a *cyclic* dependency between agents (Researcher↔Critic, in the spike's own test case) is a stronger form of interdependence than a simple linear chain — it means two agents' outputs each depend on the other's, iteratively, which is a genuinely harder interdependence structure to trace correctly than a one-directional pipeline. The fact that the project specifically tested and validated its tracing mechanism against this harder case, rather than only against the simpler three-node DAG proven in Spike 2, is direct evidence the interdependence claim was taken seriously enough to be stress-tested against its hardest realistic form, not just asserted against the easiest one.

---

## 3.9 Characteristic 9 — Requirement identification

**The three tiers:**
- ☐ A requirement or the cause of a problem can be determined by well-established ways (weakest)
- ☐ Identification of a requirement or the cause of a problem is possible from a set of known options (middle)
- ☑ **Identification of a requirement or the cause of a problem is ill defined or unknown** (top tier — selected)

### 3.9.1 The base justification

> "This is the literal definition of the core problem Granite solves: at the moment a multi-agent system produces a wrong result, the responsible agent, the responsible step, and the reason are all unknown and must be actively investigated — there is no well-established way to determine this, which is exactly why the field's best published method (ErrorProbe) only reaches 59.5% accuracy at identifying it. The entire 3-stage attribution pipeline (hypothesis generation, evidence-grounded verification, arbitration) exists because the cause is not knowable from a fixed set of known options — it has to be inferred and then verified against real trajectory evidence. Updated 2026-08-24: Recovery Controller (resuming a workflow specifically from a verified repair point, not just any checkpoint) was added to the committed core the same day with zero POC evidence — an honest admission that this specific mechanism's difficulty is still genuinely unknown, not already solved and merely unbuilt."

### 3.9.2 The resolution paragraph, quoted from the plan doc, and its relationship to this characteristic

Characteristic 9's own dedicated resolution paragraph, from plan doc §2, is worth quoting in full here because it is the paragraph the guide itself instructs teams to write for this specific row ("students should show how research, stakeholder study, experiments or a POC will reduce this uncertainty"):

> "At diagnosis time, three things are unknown and must be investigated, not assumed: (1) whether a given trace contains a failure at all — silent failures produce no explicit error signal, so their presence itself is uncertain; (2) which agent and step is the true origin, which may be many steps upstream of where the failure becomes visible; and (3) what the correct behavior would have been, which is not recorded anywhere in the trace and must be hypothesized and tested via counterfactual replay. The system's three-stage pipeline — constraint-based silent-failure flagging → backward causal tracing → counterfactual replay — is the mechanism by which this uncertainty is progressively resolved, and the proposal-stage POC (§10) is the first evidence that this resolution process works on a real, if small-scale, case."

This paragraph is structurally important because it does exactly what the accord's top tier requires and no lower tier does: it names three *specific, distinct* unknowns (not one vague "we don't know what's wrong") and ties each one to a specific mechanism the system's own architecture is built to resolve it — this is what separates "ill-defined or unknown" from merely "identification... possible from a set of known options": the second, middle tier would apply if the cause were always drawn from a small, enumerable set of candidate explanations that a diagnostic process merely had to select among; Granite's own problem is explicitly not that shape, because the space of possible root causes (which agent, which step, which specific mistake) is not a fixed, small, known set — it must be generated and then evidence-tested, which is exactly what the Strategist-then-Investigator structure (hypothesis generation, then evidence-grounded verification) is built to do.

### 3.9.3 Why citing a zero-POC-evidence item as supporting evidence, not a weakness, is defensible here

The closing move in this characteristic's justification — treating Recovery Controller's complete lack of POC evidence as *itself* supporting the "ill-defined or unknown" claim, rather than as a project weakness to be minimized — deserves the same scrutiny given to the parallel move in characteristic 2 (§3.2.4). The logic holds up under that scrutiny for the same underlying reason: if resuming a workflow from a verified-repair checkpoint were a solved, well-understood engineering problem, the team would have every reason to have already built at least a minimal proof-of-concept for it before committing it to the foundational core — exactly as was done for every other foundational item (Spikes 1 through 8 collectively cover eight of the ten foundational items with at least some real evidence). The fact that Recovery Controller specifically was committed to the core with zero POC evidence, on the explicit, stated basis that "genuinely new mechanical work" was involved rather than a rename of anything already proven (per the ninth AI-usage-log session and risk-register R21), is itself a small but real signal that this specific piece of the problem was judged, by the team itself, to be different in kind from the pieces that already had spikes — hard enough, or unfamiliar enough, that no quick proof-of-concept was obviously available to run in the time before this characteristic's rating had to be finalized. That is a genuinely different, and more defensible, kind of evidence than simply asserting "this part is hard" without any track record of the team's actual behavior around it.

---

## 3.10 The overall "Justify your selection" synthesis

### 3.10.1 The full current text, reproduced

> "Granite meets the 'Complex' tier on 8 of 9 D.4.1 characteristics, with stakeholder involvement honestly rated at the middle tier until real stakeholder feedback is obtained — not inflated to match the others. This is backed by 8 independently reproduced proof-of-concept experiments (fault injection, execution-graph construction, silent-failure detection, counterfactual replay, cyclic-graph handling, ErrorProbe reproduction, a preventive classifier — an honest negative result, reported rather than hidden — and a Repair Agent spike run 2026-08-24 with a real 4-of-6 success rate and a precisely diagnosed cause for the 2 failures), a review of 9+ relevant research papers spanning the field's entire published history on this problem (Who&When, AgenTracer, SDBL, TraceElephant, ErrorProbe, AgentAsk, PROTEA, plus a further literature triage), and checks of two separate market layers — 7 major commercial observability platforms, and, added 2026-08-24, a second independent survey of 7 agentic AI orchestration frameworks (OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI) confirming the same gap from the framework-vendor side, not just the tooling side. Together, the evidence shows a clear research gap: the best reported step-level attribution accuracy is only 59.5%, neither market layer provides standardized silent-failure detection or counterfactual fix-verification, and no prior method has been tested across multiple multi-agent architectures. The evidence is not static, either — reviewing that second survey on 2026-08-24 itself surfaced a real, previously-missed gap (Repair Agent, now built and tested) and two more committed items (Recovery Controller, Verified Repair Memory) that are honestly carried with zero POC evidence and one real test failure respectively, not smoothed over to look more finished than they are. These findings strongly support Granite as a genuinely challenging and underexplored problem — one that keeps proving harder than it looks even as the project's own understanding of it deepens, which is itself evidence for 'no obvious solution,' not against it."

### 3.10.2 Working through why "8 spikes, 9+ papers, 7 platforms, 7 orchestration frameworks" adds up to a CCP-qualifying problem

Reading the synthesis as an argument rather than a summary, it is built from four independent evidence pillars, each supporting a different one of the nine characteristics, converging on the same overall conclusion. It is worth making the mapping explicit, because the synthesis's real strength is that these four pillars are not redundant restatements of the same fact — each does genuinely different evidentiary work:

1. **The 8 POC spikes** are the pillar that supports the project's *own* demonstrated experience of difficulty — not literature about other people's difficulty, but the team's own direct encounter with real obstacles (Spike 1's scoring bug, Spike 3's self-correcting agent exposing a flawed propagation check, Spike 6's unbounded-traversal safety-cap trigger, Spike 7's near-random classifier result, Spike 8's precisely-diagnosed-but-still-real repair-interface ambiguity). This pillar most directly supports characteristics 2 (depth of analysis), 3 (depth of knowledge), and 4 (familiarity of issues), because it is first-hand evidence of exactly how much genuine effort and how many false starts were required to get even simplified, small-scale versions of these mechanisms working.
2. **The 9+-paper literature review**, spanning the field's full published history on this exact problem, is the pillar that supports the claim that the difficulty is not specific to this team's own skill level or approach — it is a field-wide pattern, independently confirmed by multiple competing, well-credentialed research groups all converging on similarly modest numbers over roughly fifteen months. This pillar most directly supports characteristics 2 and 9 (no obvious solution; ill-defined cause), since the 59.5% ceiling and the confirmed absence of any cross-architecture-tested method are both literature-review findings, not spike findings.
3. **The 7-platform commercial observability check** is the pillar that supports characteristic 5 (beyond standard practice) specifically — it is the evidence that no *documented, standardized industry procedure* exists yet, distinct from the academic-literature pillar, because a problem could in principle be academically unsolved while still having converged on a de facto industry standard practice (this happens in some fields); checking the commercial layer directly rules that possibility out here.
4. **The second, independent orchestration-framework survey** is the pillar that supports the claim's *robustness* — it is genuinely independent confirmation, arriving from a different angle (the framework-vendor side rather than the tooling/observability side) and, notably, arriving *after* the CCP argument's other pillars were already largely in place, meaning it functioned as a real, unplanned stress-test of the existing gap claim rather than a source the team went looking for specifically to support a conclusion it had already decided on. The fact that it converged on nearly the same gap analysis (Table 1's eight "Core" capability rows, none native to any of the seven surveyed frameworks) independently strengthens the claim considerably more than a second citation the team went hunting for would have.

### 3.10.3 The "evidence is not static" claim, and why it is the synthesis's strongest single sentence

The synthesis's closing argument — that the CCP case is not a fixed conclusion reached once and then defended unchanged, but a live, evolving assessment that kept surfacing *new* genuine difficulty even after the core argument was already considered settled — is, on reflection, the single most persuasive sentence in the entire justification, and it is worth explaining exactly why. A CCP argument that was fully complete and static from the start would be vulnerable to a specific, reasonable panel objection: "did you actually keep testing this claim, or did you settle on 'this is hard' early and then stop looking?" The project's own recorded history directly answers that objection with a real example, dated and evidenced: reviewing the market survey on 2026-08-24 — a full working session *after* the original CCP rating had already been drafted and, per the plan doc's own history, already through at least one prior compliance audit — surfaced a real, previously-unnoticed gap (Repair Agent, discussed in Part 2) that the team had not seen despite months of prior work on the exact same problem space. That is direct, dated evidence that the team's own understanding of the problem's difficulty was still actively deepening months into the project, which is itself a form of evidence for "no obvious solution" that a static, one-time literature review could never produce on its own — a problem that a team, having already spent months working on it, still finds a genuinely new dimension of difficulty in is a stronger data point for genuine complexity than a problem a team correctly sized up once at the very beginning and never had reason to revise.

---

## 3.11 Closing note on Parts 1–3 together

Read as a whole, Parts 1 through 3 trace a single continuous argument: Part 1 establishes *what* the project is — its exact name, its formal registration status, its stream, its client, its specification — and shows that arriving at each of these was itself a disciplined, defended, iteratively-corrected process rather than a first draft that happened to stick. Part 2 establishes *why the problem is real* — not asserted from first principles, but derived directly from a peer-reviewed field's own admitted limitations, cross-checked by direct primary-source verification (the TracerTraj correction), and stress-tested by an honest, real attempt at an alternative approach that was abandoned only once real evidence (a ten-minute-per-task pilot run) made the cost concrete rather than merely feared. Part 3 establishes *why the problem qualifies as a Complex Computing Problem* under the Seoul Accord's own nine-characteristic framework — not by inflating every characteristic to the top tier uniformly, but by rating one honestly at the middle tier specifically because the evidence to support the top tier does not yet exist, and by treating that one honest exception as a feature of the project's overall credibility rather than a flaw to be hidden.

The throughline connecting all three parts is the same discipline, applied consistently rather than selectively: state the evidence precisely, distinguish what has been tested from what has been asserted, record what was tried and abandoned alongside what succeeded, and never let a confident-sounding conclusion outrun the specific evidence that actually supports it.

---

# PARTS 1–3 ADDENDUM — Panel Follow-Up Questions, Per-Characteristic Challenge Responses, and Cross-References

*Everything below is additional depth layered onto Parts 1–3 above, not a revision of anything already written there. The brief for this addendum was threefold: (1) push every What/How/Why block harder with the kind of specific, skeptical follow-up questions an actual panel would ask, and answer each strictly from the same source documents already cited throughout Parts 1–3 — `FYP_Scope_CCP_and_Implementation_Plan.md`, `AI_Usage_Log.md`, `Guide_Compliance_Audit.md`, `ErrorProbe_Baseline_Selection.md`, `Full_Literature_Landscape_Analysis.md`, `AgenTracer_vs_WhoWhen_Analysis.md`, `Paper_Release_Timeline.md`, `generate_ccp_docx.py`, and `FYP_Registration_Form_Answers.md`; (2) add a dedicated "how this would be challenged, and the response" treatment for each of the nine CCP characteristics; (3) close with a short set of cross-references connecting decisions across Parts 1, 2, and 3 that are directly supported by the source material, not merely plausible-sounding. The same discipline applies here as everywhere above: where the source material does not answer a question directly, that is stated plainly rather than papered over with a confident-sounding guess.*

---

## A. Panel Follow-Up Questions on Part 1 — Project Identity

### A.1 On the project title (§1.1)

**Q: Isn't adopting an external document's recommended title, verbatim, a weaker position than authoring your own?** The honest answer, per §1.1.2, is that it depends on what "authoring your own" is being compared against. The team had already authored four of its own full-title candidates (§1.1.3) before the market survey was read, and none of the four was adopted — each was superseded for a specific, named reason (candidate 1 undersold the scope once repair/recovery joined the foundational core; candidate 2 read as generic product marketing; candidate 3 dropped the brand connective tissue; candidate 4 was unwieldy at three coordinate noun phrases). The market survey's title was not adopted *instead of* trying to author one — it was adopted *after* four internally-authored attempts had already been weighed and found wanting, and it happened to converge on almost the same framing the team was independently converging toward. A panel could still reasonably ask whether "convergence" is being read too generously here — the honest caveat, not stated explicitly anywhere in the source documents, is that there is no way to fully rule out that the market survey's title *itself* shaped the team's later self-assessment of the four earlier drafts as inferior, rather than the two having genuinely arrived independently. The source material states the adoption date and the reasoning for each supersession, but does not include a psychologically rigorous account of whether hindsight bias affected how the four earlier drafts are now described. That is a real limit on how strongly the "independent convergence" claim can be pressed, and this addendum flags it rather than asserting the stronger version of the claim.

**Q: What happens to the title if the market survey itself turns out to be wrong about something load-bearing?** Nothing in the plan doc or registration form answers ties the title's *validity* to the market survey being correct about any specific technical claim — the title names Granite's own committed mechanisms (self-healing, semantic error diagnosis, verified repair, recovery), not a claim borrowed from the survey's own analysis. Even if the market survey's Table 1 or its framework feature-matrix turned out to contain an error, the title would remain accurate as a description of Granite's own architecture, because every word in it maps to an already-independently-evidenced piece of the committed core (§1.1.4). The title's dependence on the survey is limited to *phrasing*, not to any factual claim the survey makes.

### A.2 The naming journey, pushed further — per-candidate skeptical questions

Part 1, §1.2.5 already states plainly that the source documents do not record an individually-attributed rejection rationale for each of the twenty-nine rejected short-name candidates — only the final list, the one stated design principle ("won't need to change even if scope shifts"), the TraceCause→Granite propagation mechanics, and the `agent-autopsy` folder-name fossil. That honesty constraint is preserved here. What follows is not a claim to have found new documented reasons for each name's rejection — none exist in the source files — but a tighter, more skeptical second pass at the same three-cluster grouping already offered in §1.2.4, framed as the specific follow-up questions a panelist would ask about individual names within each cluster, answered as far as the evidence allows and flagged as interpretation where it goes further.

**On Cluster 1 (Rootcast, Autopsy, Undertow, Culprit, Recon, Triage, Fathom).** A panelist might ask: if "Autopsy" was strong enough to become the literal folder name, why wasn't it strong enough to become the final short title? The only directly sourced answer available is the one already given in §1.2.4 — the whole cluster describes a mechanism (diagnosis) rather than the product, and the product's committed scope grew beyond diagnosis into repair and recovery. A second, narrower question a panelist might press on: why did "Culprit" specifically not survive, given that it names exactly what the Culprit Agent foundational item does? The source material offers no individually-recorded answer to this; the only defensible response is the same cluster-level one — "Culprit" would have described one of ten foundational items, not the product as a whole, which is precisely the same objection §1.2.4 raises against "Autopsy" describing only the diagnosis half. Naming the whole product after one of its ten pipeline stages risks the same category error regardless of which specific stage is chosen.

**On Cluster 2 (Ripple, Vigil, Halcyon, Meridian, Zenith, Astra, Solstice, Vantage, Zephyr).** A panelist might ask: if permanence was the winning criterion, why wasn't "Zenith" or "Vantage" — both already evoking a fixed, elevated, stable position — sufficient? This is the sharpest open question in the entire naming record, and the honest answer is that the source documents do not resolve it; there is no individually-recorded reason "Zenith" specifically lost to "Granite" specifically. The only available structural distinction, offered as this document's own interpretation rather than a sourced fact, is that "Zenith" and "Vantage" name a *position* (a place one has reached), while "Granite" names a *material property* (a substance that resists change) — and a name describing an unchanging property arguably maps more literally onto the stated design principle ("won't need to change") than a name describing a position, which could in principle still be surpassed or shifted from. This is offered as a plausible distinction, not a documented fact, and a panelist pressing further on this specific question should be told directly that the source material does not settle it.

**On Cluster 3 (Steady, Clarity, Sure, True, Keen, Solid, Whole, Actual, Proof, Level, Given, Behold).** A panelist might ask: given that "Proof" maps almost exactly onto "Verified" — the single most load-bearing qualifier word in the eventual full title (§1.1.4) — why wasn't a title built around "Proof" instead? The genericness argument already given in §1.2.4 (real commercial products already using "Proof," "Clarity," "Solid," "True" in adjacent spaces) is the only sourced answer, and it is a real, defensible one, but it is worth being explicit that this argument applies with different force to different words in the cluster — "Proof" is arguably the single most commercially crowded word in the entire list of twenty-nine (used across security, compliance, and verification-adjacent products broadly), which if anything strengthens rather than weakens the genericness rejection for this specific candidate.

**What this second pass changes, and what it doesn't.** It does not add any new documented rejection reasons beyond what §1.2.4 and §1.2.5 already state — the source material's own limits on this topic are fixed regardless of how many additional questions are asked of it. What it does do is make explicit exactly where the existing three-cluster analysis is on strong evidentiary footing (the stated design principle, the folder-name fossil, the propagation mechanics) versus where it is this document's own plausible-but-unsourced interpretation (Zenith vs. Granite specifically) — a distinction worth keeping sharp precisely because a panel that catches an inference being presented as a fact anywhere in this section will, per §1.0's own opening argument, read the rest of the naming discussion with more suspicion than it otherwise deserves.

### A.3 On Stream A classification (§1.3)

**Q: The plan doc leans on ErrorProbe's own admitted limitation as the source of the gap — but couldn't a panelist argue that "a paper admits a limitation" is a weak form of gap evidence, since every paper names limitations as a matter of academic convention?** This is a fair challenge, and the response available in the source material is precise rather than dismissive: the gap claim does not rest on ErrorProbe naming *a* limitation (which, as the challenge notes, is conventional), it rests on the specific *content* of that limitation matching, almost word for word, the exact mechanism (constraint-based verification independent of anomaly signal) Granite's own FR3 is built to test (§1.6.2). A limitations section that vaguely gestures at "future work could improve robustness" would indeed be weak gap evidence; a limitations section that names a precise, structurally-defined failure class (silent failures, anomaly-gated pipeline) that the project's own second Primary research question is built to directly test is a categorically stronger form of evidence, and the distinction between the two is what the response should lead with if this challenge is raised.

**Q: R19's rejection of the market survey's single-framework advice is framed as principled — but isn't there a simpler read, that the team just didn't want to give up scope it had already invested in?** The source material's own answer to this is the Framework Compatibility Layer resolution (§1.3.4): if the rejection were purely sunk-cost defensiveness, the natural response would have been a bare refusal with no concession to the underlying concern. Instead, the underlying concern (breadth-over-depth risk, already independently tracked as R8) is conceded as valid and answered with a scoped, positive mechanism — lightweight compatibility checks across all seven frameworks, full benchmarking on only two-to-three. A purely defensive rejection would not have produced a new, concretely scoped extension item; it would have produced only a written objection. That said, the plan doc itself does not claim this proves the motivation was pure principle rather than partly sunk-cost — the honest position is that the *outcome* (a scoped, positive resolution rather than a bare refusal) is evidence of principled handling regardless of what mixture of motivations produced it.

### A.4 On SDG alignment (§1.5)

**Q: SDG 9 target 9.5 talks about "industrial sectors" broadly — isn't this a stretch for a single diagnosis tool built by three students?** The plan doc's own stated discipline (§0.05) directly pre-empts this challenge by keeping the SDG section to one paragraph, explicitly not used to inflate the pitch, and by tying the claim to the concrete evidentiary basis already established elsewhere (the seven-platform commercial comparison, characteristic #5's "beyond standard practice" evidence) rather than asserting sector-wide impact on its own authority. The honest scope of the claim is narrow: Granite is one piece of technical infrastructure addressing one confirmed gap in one emerging technology category (multi-agent AI reliability tooling) — the SDG framing names the *category* the gap sits in, not a claim that Granite alone transforms an industrial sector.

### A.5 On client and specifiability (§1.6)

**Q: FR3's acceptance criterion requires synthetic, ground-truth-known-by-construction cases — doesn't this mean the "hardest requirement" is actually being tested under the easiest possible conditions?** This is worth answering directly rather than deflecting, because it is a genuinely sharp challenge. §1.6.3 already names this limitation honestly: the acceptance criterion is deliberately scoped to synthetic cases specifically *because* real-world ground truth for silent failures is itself disputable, which would make the acceptance criterion untestable if it depended on real-world cases. The correct response to this challenge is not to deny the limitation but to state precisely what it does and does not establish: it establishes that the *mechanism* works correctly when the answer is known by construction (which Spike 4 already demonstrates on a narrow, n=3-plus-direct-mechanism-test basis), and it explicitly does not yet establish real-world reliability on naturally-occurring, disputable-ground-truth cases — exactly the same honest boundary already drawn in §3.4.2's discussion of characteristic 4.

**Q: FR1 requires the fault-injection harness to be "controlled, deterministic" — but Spike 3's own history shows the first injection attempt was ambiguous (the agent self-corrected a corrupted famous fact). Doesn't that mean FR1 was written to paper over a real failure rather than to prevent one?** The chronology actually runs the other way, and it is worth stating the direction precisely because it matters to the challenge: per §1.6.2's discussion of FR1, the "controlled, deterministic" language is written *because* the team had already, empirically, discovered a way this requirement could silently fail before the requirement was finalized in this form — the specification came after the failure, as a direct response to it, not as language written first and then falsified by the spike. R3's own status (§2.9.2) records both the flawed first attempt and the clean second attempt on record together, with the register stating plainly that "real fault behavior includes both self-correction and blind propagation, and the benchmark should account for that rather than assume only one" — meaning the requirement's final form is itself evidence the team treated the first attempt's failure as a design input, not an embarrassment to bury.

**Q: FR2's output triple (agent, step, confidence) inherits Who&When's own (i*, t*) formalism — doesn't inheriting a formalism from a paper whose own accuracy is only 14.2% risk inheriting a flawed problem framing along with it?** This is worth answering by separating the formalism from the performance: the (i*, t*) tuple is a definitional choice about *what question is being asked* (which agent, which step), not a claim about how easy that question is to answer — every descendant paper in the lineage (AgenTracer, SDBL, ErrorProbe) reuses the identical formalism and achieves substantially different accuracy on it (14.2% → ~40% → 59.5%), which is itself evidence the formalism is not the bottleneck; the *method* used to answer it is. The one place this challenge has real teeth, and where the response should concede rather than deflect, is DoVer's own critique (§B.8 below) that single-step attribution may be ill-posed at a deeper level than accuracy alone reveals — a challenge to the formalism itself, not to any one paper's performance under it, and one the project explicitly does not attempt to resolve within its own scope (per the standing R7 policy).

**Q: FR4 and FR5 are both, in different ways, downstream of assumptions that later needed correcting (FR4's candidate-value gap, closed only in session six; FR5's deployability claim, still untested per the plan doc's own §13 "evidence of deployment" row). Doesn't a specification with two requirements resting on later-discovered gaps undermine confidence in the specification process itself?** The honest answer distinguishes the two cases rather than treating them as the same kind of gap. FR4's gap (§1.6.2) was a genuine specification blind spot — the requirement's own wording silently presupposed a capability nothing upstream supplied — and its discovery and closure (Repair Agent, same-day POC) is itself evidence the specification process is self-correcting, not evidence it is unreliable. FR5's "evidence of deployment" gap is a different kind of thing entirely: it is explicitly named, in the plan doc's own §13, as a requirement that cannot honestly be satisfied *yet* because the guide's own framework places deployment evidence at Final-1, not proposal stage (§13's own row states this plainly: "Not yet producible... expected at Final-2 stage, not a current gap"). Conflating a genuine specification blind spot (FR4, now closed) with an honestly-scheduled future deliverable (FR5's deployment evidence) would be the actual error here, and the response should draw this distinction explicitly rather than let both be treated as equivalent weaknesses.

**Q: NFR1's "under 50%" latency target for the single-pass mode — is this number derived from any measurement, or asserted as a round-number aspiration?** The source material does not record a measurement behind this specific figure — it is a stated target for a mode (extension #6) that had not yet been built as of the plan doc's own most recent revision, meaning the number is a design target the evaluation plan is built to *test against*, not a number already validated by data. This should be stated plainly if asked: the 50% figure is the threshold the single-pass mode is being built to meet, not a figure already confirmed achievable, and the plan doc's own evaluation-plan structure (§11) is explicit that diagnostic overhead "shall be measured and reported," language that only makes sense if the number is not yet in hand.

### A.6 On the one-line idea statement and its "AgentTestLab" ancestry (§1.4)

**Q: If the "AgentTestLab" pitch was too broad and had to be trimmed down to reach the current one-line idea, doesn't that suggest the *original* instinct about what this project should be was wrong, and the current scope is a retreat rather than a considered choice?** §1.4.3 already frames this the opposite way, and the framing is worth defending directly rather than conceding: nothing about the wider pitch was judged wrong on its merits — it was judged too broad for a single one-year Stream A project to defend as "one shared central problem" (guide §5's own test) and at risk of the guide's explicitly-named "feature accumulation" hazard. The wider vision was not discarded; every piece of it was re-routed into the extensions list (§7.0 of the plan doc) rather than deleted, meaning the current committed core is not evidence the original ambition was mistaken — it is evidence the team correctly separated "what one CCP-justified core project can defensibly claim" from "what the full product vision eventually becomes," which is precisely the discipline guide §5.3 asks a team to demonstrate. The archived pitch document (`TraceCause_AgentTestLab_Pitch.md`) being preserved rather than deleted (§1.2.6's propagation-discipline discussion applies here too) is itself evidence this was a scoping decision, not an abandonment.

### A.7 On the research-to-decision table (§1.6.4)

**Q: Row 7 of the research-to-decision table cites the FAST guide itself as a "research source" feeding a decision (how many POC spikes to run). Isn't citing the assignment's own grading rubric as evidence of research rigor a slightly circular move?** §1.6.4's own closing note on Row 7 already anticipates this by calling it "a slightly unusual but legitimate reading of the table's own format" rather than asserting it without qualification. The response to press further, if a panelist does: the table's own five columns (source, finding, relevance, decision influenced, planned evidence) do not require the source to be an academic paper — they require a real source whose finding genuinely shaped a decision, and the guide's own §12 requirement (POC must be demonstrated with evidence, not described) is a real, external constraint that did genuinely shape how many spikes were run (seven, not the original three-to-four planned) and how thoroughly each was logged. The circularity risk would be real if the "finding" being cited were merely "the guide says do a good job" — it is not; it is a specific, checkable procedural requirement (evidence over description) that produced a specific, checkable outcome (seven spikes instead of the original plan).

### A.8 On ethical compliance (§1.6.5)

**Q: The ethical-compliance section states the diagnosis engine's output is "advisory, not autonomous" — but Recovery Controller's own stated function is to *resume execution* from a repair point, which sounds like an autonomous action, not an advisory one. Isn't there a tension between the ethical-compliance claim and what Recovery Controller actually does?** This is a fair internal-consistency question the source material does not address head-on in so many words, and it is worth naming the tension plainly rather than papering over it: Recovery Controller's own function (§1.1.4, "Verified Repair Memory" discussion) does involve the system taking an action (resuming a workflow) rather than merely reporting a finding. The mitigating fact already on record, though not phrased by the plan doc as a direct answer to this specific tension, is the confidence-gating principle that governs every repair-adjacent mechanism in the committed core (§1.9.4's discussion of the rejected "Automatic Retry" feature): a fix is only ever applied, and by extension only ever resumed from, once it has already cleared Verified Automatic Repair's own verification step and a stated confidence threshold — meaning the "human reviews before any fix is applied" commitment in the ethical-compliance section should be read as governing the repair-application decision specifically, with Recovery Controller's resumption step downstream of an already-gated decision rather than an independent autonomous action. This is this addendum's own synthesis of two separately-stated commitments, not a sentence appearing verbatim in either source document, and should be presented as such if raised.

### A.9 On the two-track extensions justification (§1.9)

**Q: If the eight extensions are justified by "product demand" rather than by beating a specific paper, how would a panel know that justification isn't just a way to add scope without CCP scrutiny?** The plan doc's own answer, already quoted in §1.9.1, is that the two-track split is explicit and structural, not a loophole: the committed core alone carries the comparison-to-prior-work claim the CCP argument depends on, and the extensions are explicitly, repeatedly stated to be gated *behind* the core (§1.9.3's "genuinely parked" framing for the two deprioritized items is the clearest single instance of this discipline in action) rather than built in parallel with it. A team using the extensions list as an unscrutinized scope-expansion loophole would build extensions before the core was proven, or would claim comparison-to-prior-work credit for an extension the way it does for a core item — neither happens anywhere in the documented history; every extension's own individual justification (§1.9.2) is a product-use-case argument, and where a paper is named in an extension's justification (PROTEA for extension #3, AgentAsk for extension #7 by inheritance from §B.6 above), the plan doc is explicit each time that this is context, not a comparison claim.

---

## B. Panel Follow-Up Questions on Part 2 — Research Gap and Baseline, Paper by Paper

Each of the seven core papers (plus the two escalated R7-triage papers) is revisited here specifically for what its own stated limitations section says and how Granite's approach differs from that specific paper — not the aggregate, cross-paper comparison Part 2's main text already gives, but a tighter, one-paper-at-a-time delta.

### B.1 Who&When (ICML 2025)

**What its own limitations state.** Best step-level accuracy only 14.2%; even o1/DeepSeek-R1 "fail to achieve practical usability" (§2.2.1, Full Literature Landscape Analysis §5). Ground truth is entirely human-annotated, at a real, stated cost (30+ hours per annotator across three experts) — the paper's own methodology is, by its own admission, not scalable without that cost.

**How Granite differs from this specific paper, not just the aggregate field.** Where Who&When relies on expensive human annotation to establish ground truth, Granite's own benchmark-construction plan inherits AgenTracer's programmatic fault-injection methodology instead (Row 2 of the research-to-decision table, §1.6.4) — the delta here is not an accuracy delta at all, it is a *cost-of-ground-truth* delta: Granite's new benchmark is built to scale to 500–1,000 traces specifically because it does not carry Who&When's annotation cost. Separately, and more directly comparable on accuracy: Who&When's own three baseline methods (ALL_AT_ONCE, STEP_BY_STEP, BINARY_SEARCH) are not what Granite measures itself against — ErrorProbe (a descendant that already beats Who&When's own numbers by more than 4x on step accuracy) is the comparison point, per the baseline-selection logic in §2.1.2. Who&When remains load-bearing for Granite not as an accuracy comparator but as the primary reproduction *dataset* — 184 real cases, MIT-licensed, confirmed downloaded — and as the source of the shared (i*, t*) formalism every downstream metric in Granite's own evaluation plan (§1.6.2's discussion of FR2) inherits.

**A second, distinct limitation, easy to miss because it is not phrased as one in the paper's own "Limitations" language.** Per the dataset table in the Full Literature Landscape Analysis (§4), Who&When's entire benchmark is built on only two underlying multi-agent systems — CaptainAgent and MagenticOne — spanning two task sources (GAIA, AssistantBench). This is a narrow-system-diversity limitation distinct from the accuracy limitation already discussed: even a hypothetical attribution method that solved Who&When's accuracy problem perfectly would still have been validated on only two multi-agent architectures. Granite's own cross-architecture claim (RQ2) is a direct, specific answer to this narrower reading of the gap, not only to the accuracy gap — Granite's committed core targets CrewAI and native LangGraph specifically because neither appears among Who&When's own two underlying systems, which is a more precise statement of the delta than "Granite generalizes better" would be on its own.

### B.2 AgenTracer (ICLR 2026)

**What its own limitations state.** Step accuracy still modest even trained (~37–43% on TracerTraj); tested only within its own six-framework ecosystem (MetaGPT, AutoGen, Smolagents, AgentPrune, AFlow, OWL-Workforce); quality bottlenecked by its own analyzer LLM's capability (Full Literature Landscape Analysis §5). The now-superseded `AgenTracer_vs_WhoWhen_Analysis.md` names a second limitation directly, worth restating precisely because it predates and is not repeated in the later, full-corpus documents: AgenTracer's own "self-evolution" demonstration (§5.3, Figure 3 of that paper) "only feeds attribution output back as generic textual reflection... never uses the structured (agent, step) output to drive a targeted intervention" — i.e., AgenTracer diagnoses precisely but does not act on its own diagnosis in any targeted way.

**How Granite differs from this specific paper.** Two distinct deltas, not one. First, the cross-architecture delta: AgenTracer's six-framework ecosystem does not include CrewAI or native LangGraph, Granite's own two committed core architectures — this is the direct evidentiary root of RQ2 as applied specifically to AgenTracer, not just the aggregate seven-paper claim. Second, and this is the delta the now-superseded two-paper analysis actually surfaces most sharply, even though the later full-corpus documents fold it into the broader RQ4/repair discussion rather than naming AgenTracer individually: AgenTracer's own self-evolution mechanism never converts a structured diagnosis into a targeted, verified intervention — it stops at generic reflective feedback. Granite's Repair Agent → Verified Automatic Repair → Recovery Controller chain is precisely the missing piece this early analysis identified as a real, unaddressed mechanism gap in AgenTracer specifically, phrased at the time as a delta-sentence test: *"We will test its generalization to unseen multi-agent frameworks, and build a targeted attribution-driven repair mechanism instead of generic reflection."* That two-paper-era framing predates Repair Agent's actual addition to the committed core by roughly a month of project history (the two-paper analysis is explicitly marked superseded, with no date attached to its own drafting relative to the nine AI-usage-log sessions, but its content is structurally continuous with what Repair Agent later became), and is worth surfacing here specifically because it shows the targeted-repair idea has deeper roots in the project's own history than the sixth-session market-survey account alone would suggest.

**A third, distinct limitation.** The Full Literature Landscape Analysis's own §5 names a limitation not yet used above: AgenTracer's own attribution quality is "bottlenecked by its own analyzer LLM's capability" — meaning the 8B AgenTracer-8B model's own reasoning ceiling, not only its training-data diversity, caps how well it can perform even on its own six-framework home turf. This is a distinct axis from the cross-architecture delta (which is about *where* AgenTracer was tested) and the self-evolution delta (which is about what AgenTracer *does* with a diagnosis once made) — this third limitation is about the *analyzer itself* being a capped resource. Granite's own architecture responds to this specific axis differently from how it responds to the other two: rather than depending on a single fixed, purpose-trained model's own ceiling, Granite's committed core deliberately keeps the diagnosis-critical components (execution-graph construction, backward tracing, confidence scoring, Semantic Error Diagnostic) off the LLM path entirely (§1.8.2's 0%-API-dependent commitments) — meaning Granite's own attribution accuracy ceiling is not, in the same direct way AgenTracer-8B's is, bottlenecked by one model's own capability, though the honest caveat here is that Granite's *Culprit Agent and Error Step Localization* stages (the Strategist-stage hypothesis generation, per §2.1.1) are still LLM-driven and would carry an analogous capability ceiling of their own — this delta is real but partial, not a claim that Granite has eliminated the underlying constraint altogether.

**A fourth point, on the dataset rather than the method.** AgenTracer's own TracerTraj-2.5K, separate from any accuracy or architectural limitation, turned out on direct inspection not to be publicly released at all (§2.4) — no LICENSE file, weights and data only "committed to" release upon paper acceptance. This is a limitation of the paper's own reproducibility posture, not of its method, and it is the specific reason Granite's own benchmark-construction plan could not simply extend AgenTracer's dataset rather than building a new one from GSM8K and tau-bench retail (§2.5.5) — a delta driven entirely by data availability, independent of any accuracy or architectural comparison.

### B.3 SDBL (AAAI 2026)

**What its own limitations state.** Best step accuracy still only ~33–40% even with its own two-stage method — "the majority of cases remain misattributed at the step level" is the paper's own stated finding, per the Full Literature Landscape Analysis §5. It introduces no new dataset, relying entirely on Who&When's own data, and its own reported split sizes (Hand-Crafted=54/Algorithm-Generated=126) genuinely disagree with the counts both AgenTracer and ErrorProbe report for the identical underlying dataset (Algo=127/Hand=58) — a real, unresolved cross-paper inconsistency the source material flags rather than silently reconciles.

**How Granite differs from this specific paper.** SDBL's own novelty is a cognitively-motivated two-stage heuristic (delineate scope, then localize, inspired by observed novice-vs-expert debugging behavior) applied to the identical Who&When benchmark ErrorProbe is measured against — meaning SDBL is the single closest same-benchmark performance comparator available for the ErrorProbe-selection argument (§2.1.3), not a paper whose *mechanism* Granite borrows or extends. The delta here is purely about the baseline-selection decision itself: SDBL's own best numbers (39.68% Algo, 27.78% Hand) are beaten by ErrorProbe on both identical splits (59.50%, 31.00%), which is the direct evidentiary basis for choosing ErrorProbe over SDBL as the paper to build on, worked through in full in §2.1.2.

**A second, distinct limitation.** Because SDBL "reuses Who&When's dataset only, no new dataset of its own" (Full Literature Landscape Analysis §4), its own two-stage method has never been validated on any benchmark independent of Who&When — meaning its accuracy figures, however they compare to ErrorProbe's, carry no evidence about how the "delineate scope, then localize" heuristic generalizes beyond the specific systems (CaptainAgent, MagenticOne) Who&When itself was built on. This is a second, generalization-specific limitation distinct from the raw-accuracy comparison already used, and it sharpens the delta argument in a way the accuracy comparison alone does not: Granite's own new cross-architecture benchmark is not only aimed at beating ErrorProbe's number, it is aimed at a question SDBL's own evidence base cannot even speak to — whether *any* of the field's attribution methods, including the ones that currently outperform ErrorProbe on one axis (SDBL's own 63.49% agent accuracy on Who&When-Algo, §2.1.3), hold up once tested outside the two systems every paper in the lineage has, so far, exclusively been validated against.

### B.4 TraceElephant (ACL 2026 Long)

**What its own limitations state.** It proposes no new attribution algorithm at all — by its own framing, it is a data/observability contribution, arguing the field's prior methods were partly bottlenecked by incomplete trace access (only capturing agents' outputs, not their full input context) rather than purely by weak reasoning algorithms (Full Literature Landscape Analysis §5–6).

**How Granite differs from this specific paper.** Because TraceElephant makes no attribution-accuracy claim, there is no accuracy delta to state against it — the honest, correct comparison here is structural, not numeric. TraceElephant's own finding (fuller trace access alone, with no algorithm change, improves accuracy up to 76.5% relative to partial observation) is direct external validation of a design choice Granite's own execution-graph construction already makes independently: structural, full-trace parsing of message and reference identifiers (matching GraphTracer's "parse references, extract unique identifiers" approach, per plan doc §6), rather than an LLM judging a partial view of a trace after the fact. TraceElephant is cited in Granite's documentation as supporting evidence for *why* the execution-graph construction mechanism was built the way it was, not as a paper whose numbers Granite improves on. Separately, TraceElephant is one of only two papers in the corpus (with Who&When) whose license is directly confirmed rather than assumed (CC BY 4.0, verified in its own Appendix A.10) — a small but genuine licensing-precedent role distinct from its content role.

**A second, distinct limitation, on the licensing point specifically.** TraceElephant's own data license is confirmed (CC BY 4.0), but its benchmark *code* is not — the paper states only that code will be released under an unspecified "permissive open-source license" (§2.4.1's licensing table). This is a real, if minor, reproducibility gap distinct from the data/observability-only limitation already discussed: a team wanting to actually run TraceElephant's own full-trace-capture pipeline, rather than only reuse its released annotations, cannot yet confirm the terms under which the code itself could be reused. Granite's own posture on this exact point (§1.5.3's SDG 17 discussion) is to commit its own benchmark to a named, confirmed license (MIT/CC BY 4.0) at release time rather than a promised-but-unspecified one — a small but deliberate contrast with TraceElephant's own still-open code-licensing status.

**A third point, on system diversity.** TraceElephant reuses the identical two underlying systems as Who&When (CaptainAgent, MagenticOne), adding SWE-Bench as a third task source but no new *system*. This means TraceElephant's own finding — that fuller trace access improves accuracy up to 76.5% — has, like SDBL's own accuracy figures, never been tested outside the same narrow two-system pool every paper in this branch of the lineage shares, which is the same narrow-system-diversity limitation already named for Who&When (§B.1 above) and SDBL (§B.3 above), recurring for a third time across the lineage's data/observability contribution as well as its two attribution-method contributions.

### B.5 ErrorProbe (ACL 2026 Findings)

Already covered in exhaustive detail in Part 2's main text (§2.1) and is the anchor paper for the entire baseline argument; not repeated here beyond noting, for completeness of this per-paper pass, that its three named limitations (silent failures, added inference latency, three-backbone-only validation) map directly and individually onto RQ3, CCP characteristic #1's depth-vs-latency tension, and the honestly-acknowledged limit on how far the evaluation plan's own claims can generalize (§11's "what the evidence can and cannot support" row), respectively — each of ErrorProbe's three stated limitations has a named, specific downstream consequence somewhere else in Granite's own documentation, which is itself worth stating plainly as a pattern: this is the one paper in the corpus where every single admitted limitation was traced through to a specific project decision, rather than only the silent-failure one.

**A fourth limitation, more subtle than the three named in its own "Limitations" section, and worth surfacing here precisely because the earlier, two-paper-era analysis caught it before the later full-corpus documents restated it as sharply.** ErrorProbe's own cross-domain transfer claim (its Section 6.2, "Memory Scaling") is real but narrower than a first read suggests — per the Full Literature Landscape Analysis's own §7, the claim is verified transfer *across task domains* (coding ↔ math, e.g., memory built from KodCode improving diagnosis on GSM8K/MATH) *within its own already-tested benchmark ecosystem* (TracerTraj, Who&When-Algo, Who&When-Hand), not transfer to a genuinely unseen multi-agent architecture. This distinction — domain transfer within a known architecture ecosystem, versus architecture transfer to something never seen during benchmark construction — is exactly the distinction RQ2 is built on, and it is worth stating as its own fourth limitation because a panelist who has read ErrorProbe's own Section 6.2 could otherwise reasonably (but incorrectly) believe ErrorProbe already demonstrates the cross-architecture generalization Granite claims as a gap; the correct response is that ErrorProbe demonstrates a real but different, narrower kind of generalization, and Full Literature Landscape Analysis's own §7 states this survives "fully intact after reading all seven papers in full — this is now a confirmed finding grounded in complete text, not an inference from abstracts."

### B.6 AgentAsk (ACL 2026)

**What its own limitations state.** Cannot fix errors originating from an agent's own internal reasoning flaws (hallucination, reasoning gaps) — only catches errors visible at a message handoff between agents (Full Literature Landscape Analysis §5).

**How Granite differs from this specific paper.** AgentAsk's intervention philosophy is preventive (stop the error before it propagates past a handoff) where Granite's primary approach is post-hoc (diagnose after a failure has already occurred and propagated). This is not a claim that Granite's approach is superior — the plan doc is explicit that AgentAsk is cited as context, never as a comparison baseline, since no shared dataset or code exists for a head-to-head test (§2.2.6). The one place AgentAsk's specific limitation matters concretely to Granite's own scope: extension #5 (formerly #7, the preventive clarification classifier, tested honestly and near-randomly in Spike 7) is Granite's own scoped, much lighter attempt at the same preventive philosophy AgentAsk pursues at full scale with a purpose-trained RL module (its own novel "E-GRPO" extension of Group Relative Policy Optimization) — Granite's extension is explicitly not attempting to match AgentAsk's own RL-trained sophistication, and Spike 7's own near-random result is, read against AgentAsk's much heavier RL investment, a data point suggesting the lightweight version of this idea may simply require more sophisticated features or more training data than a TF-IDF-plus-logistic-regression baseline can supply — a hypothesis risk-register R15 already names directly (§2.9.3).

**A second, distinct limitation.** AgentAsk's own taxonomy corpus — the 824 annotated agent-to-agent messages its classification scheme is built and validated on (Full Literature Landscape Analysis §4) — required "multiple professional annotators" to reach its own stated Fleiss' κ of 0.84, meaning AgentAsk, like Who&When before it, carries a real, non-trivial human-annotation cost, just at a smaller scale (824 messages versus Who&When's 184 full-task annotations, but each requiring dedicated professional annotator time rather than programmatic generation). This is a distinct limitation from the "can't fix internal reasoning flaws" one already used — it is about the cost of *building* AgentAsk's own detector, not about what the detector can and cannot catch once built. Granite's own preventive-classifier extension (#5) responds to this specific axis by deliberately avoiding the same cost: Spike 7 trained its classifier on twenty hand-written examples rather than a professionally-annotated corpus, which is precisely why its near-random result (§F.1's discussion, risk-register R15) is not a fair apples-to-apples comparison against AgentAsk's own much more heavily-annotated approach — a distinction worth making explicitly if a panelist compares Spike 7's result unfavorably to AgentAsk's own reported performance, since the two were built on datasets differing in both scale and annotation rigor by a wide margin.

### B.7 PROTEA (ACL 2026 System Demonstrations)

**What its own limitations state.** No automated root-cause confidence scoring at all — a human must inspect and approve every proposed fix; supports only static DAG workflows, explicitly excluding cyclic/dynamic multi-agent graphs as its own stated future work (Full Literature Landscape Analysis §5).

**How Granite differs from this specific paper.** This is the single most direct paper-to-paper structural delta in the entire corpus, because PROTEA is, per §2.2.7, "arguably the closest thing in the entire corpus to what Granite itself is trying to build" — both are full-pipeline products (evaluate → localize → propose fix → re-run → compare), not pure attribution-accuracy research artifacts. The two decisive gaps PROTEA's own limitations name map one-to-one onto two of Granite's own committed foundational items: PROTEA's lack of automated confidence scoring is directly answered by Confidence Calibration (extension #4, a reliability diagram plus Brier score) and by the confidence-gated fix-approval principle already built into Verified Automatic Repair and Recovery Controller's design (the same principle that led to Automatic Retry being rejected as a standalone feature, §1.9.4); PROTEA's static-DAG-only limitation is directly answered by extension #3 (cyclic/dynamic graph support, proven mechanically in Spike 6). The plan doc is careful, and this addendum preserves the same care, to state this as *independent confirmation the gaps are real*, not as a claim of having beaten PROTEA on any measured number — PROTEA has no public benchmark or code, so no such comparison is possible, and none is claimed (§1.9.2, extension 3's discussion).

**A third, distinct limitation, on empirical rigor itself.** Per the Full Literature Landscape Analysis's own §6, PROTEA is "evaluated at much lower rigor than the academic papers... no F1/precision/recall against ground truth, only two internal case studies and an 11-workflow stress test," and both underlying production-adjacent workflows are confidential and not released. This is a limitation distinct from the two architectural gaps already used (no confidence scoring, static-DAG-only) — it is about the *evidentiary standard* PROTEA holds itself to, not about what its architecture can or cannot do. This is directly relevant to how Granite should position its own evaluation claims: Granite's own committed evaluation plan (§11 of the plan doc, worked through in §2.8 above) commits to F1/precision/recall-style metrics against ground-truth-labeled benchmarks throughout, precisely the rigor PROTEA's own industry-demo format does not attempt — meaning the delta here is not only architectural (cyclic-graph support, confidence gating) but methodological: Granite is committing to hold itself to the academic evaluation standard PROTEA, the closest product-shaped comparator in the whole corpus, explicitly does not.

### B.8 The two escalated R7-triage papers — "From Confident Closing to Silent Failure" and DoVer

These two are not part of the original seven-paper corpus but were escalated to "High" threat status during the second literature-triage pass (§2.2.8) and deserve the same specific treatment here, since both sit unusually close to Granite's own core claims.

**"From Confident Closing to Silent Failure" (arXiv:2606.09863, Laksh Advani).** A real, working, published-quality silent-failure detector, tested at genuine scale (tau2-bench, 9,876 trajectories; AppWorld, 1,879 trajectories) — orders of magnitude larger than Spike 4's own n=3 natural-occurrence test. Its own finding is directly relevant to a specific architectural choice Granite has already made: it reports that LLM judges perform poorly at this task (AUROC ≤0.65) while lightweight TF-IDF detectors reach 0.83–0.95 AUROC. This is external, independent validation of the exact design principle plan doc §6's external-component table commits to for the Semantic Error Diagnostic module — "not 'ask an LLM if this seems semantically wrong'" — except this paper's own finding cuts even further than Granite's own committed rule/schema-based approach: it suggests that even a comparatively simple statistical (TF-IDF) detector beats an LLM judge, which is one more independent data point supporting the decision already made on architectural-purity grounds in §1.8.2, arrived at from a completely different angle (empirical AUROC comparison rather than a "don't make your differentiator an API call" design principle). This paper is not added as a baseline or cited as established prior work (per the standing R7 policy, §1.6.4 Row 5), but it is the single most directly relevant unpublished finding to Granite's own RQ3, and a panel asking "does anyone already do what your Semantic Error Diagnostic module does" should be answered with this paper named honestly, not omitted.

**DoVer (arXiv:2512.06749, Microsoft Research authors).** A methodologically sophisticated, intervention-driven debugging framework that argues single-step attribution is "ill-posed," since multiple distinct interventions can independently repair the same failure (§2.2.8). This is a genuinely pointed challenge to a premise Granite's own attribution pipeline relies on — that there is a well-defined, single "decisive error" (i*, t*) tuple to find at all. The honest response, consistent with the project's standing R7 policy, is not to argue DoVer is wrong, but to note that Granite's own formalism is inherited directly from Who&When (§2.2.1) and shared by every descendant paper Granite measures itself against (AgenTracer, SDBL, ErrorProbe) — if DoVer's critique of single-step attribution as ill-posed is correct, it would be a critique of the entire lineage Granite builds on, not a Granite-specific weakness, and the project's own decision (R7) is to accept this as a real, named, unresolved risk to the field's shared formalism rather than either dismiss it or attempt to answer it within the current FYP's scope.

---

## C. How Each CCP Characteristic Would Be Challenged, and the Response

Each of the nine characteristics from `generate_ccp_docx.py` (reproduced and rated in full in Part 3, §3.1–3.9) is revisited here for the single hardest question a panel could plausibly ask specifically about that characteristic, answered using only evidence already established in the plan doc and the CCP-justification script itself.

### C.1 Characteristic 1 — Conflicting requirements

**Hardest challenge:** "Every non-trivial software system has *some* trade-offs — latency vs. accuracy exists in nearly any ML system. Why does this rise to 'wide-ranging or conflicting... issues' rather than the middle tier ('a variety of factors, which may impose conflicting constraints')?"

**Response, from the source evidence.** The distinguishing fact is not that trade-offs exist (a panel is right that this alone would only support the middle tier) but that Granite's own committed scope contains a *structural response* to each tension rather than a passive acknowledgment of it — this is what the top tier's "wide-ranging" language is meant to distinguish from a project that merely lists trade-offs. Tension 1 (depth vs. latency) produced an entire dedicated extension (#6, two selectable diagnosis modes) built specifically to make the trade-off a measured, exposed configuration choice rather than a fixed cost. Tension 2 (completeness vs. privacy) produced a full, dated, three-category threat model (R16) with three named, committed mitigations. Tension 3 (generalization vs. specialization) produced a real, recorded, and consequential decision under pressure — rejecting the market survey's own single-framework advice (R19) at the cost of forgoing the accuracy a specialized tool could reach. A project where "conflicting requirements" is asserted but produces no architectural or scope-level response anywhere would be a middle-tier case; a project where each named tension has already produced a specific, evidenced structural response is the top tier's own defining pattern.

**Second-round challenge:** "Aren't tensions 2 and 3 really just special cases of tension 1 — everything reduces to 'more accurate costs more,' whether the cost is latency, privacy exposure, or specialization foregone? If so, this is one tension dressed up as three."

**Response.** This is a real structural question worth taking seriously rather than dismissing on the grounds that three items were listed. The honest answer is that tensions 2 and 3 do share a family resemblance with tension 1 (all three ultimately trade some form of capability against some form of cost), but they are not reducible to each other because the *cost* being traded is categorically different in each case, which matters because each requires a different kind of mitigation. Tension 1's cost is time (inference latency), addressed by a configuration choice (extension #6). Tension 2's cost is a data-governance exposure (customer PII risk), addressed by a threat model with named redaction and namespacing mitigations (R16) — no amount of picking a faster diagnosis mode reduces this cost, because it is not a speed problem. Tension 3's cost is a permanent, structural one — accuracy genuinely foregone by refusing to specialize to one framework, which cannot be recovered by any runtime configuration choice the way tension 1's can; it is a standing, load-bearing scope decision (R19), not an operational trade-off users toggle. Three genuinely different *kinds* of mitigation being required is itself the evidence the three tensions are not one tension in three costumes — if they were, one mitigation mechanism would address all three, and none does.

### C.2 Characteristic 2 — Depth of analysis

**Hardest challenge:** "59.5% after 15 months could just mean the field is under-resourced or nobody's tried hard enough, not that the problem has 'no obvious solution.' How do you rule out 'nobody has thrown enough compute/talent at this yet' as the real explanation?"

**Response, from the source evidence.** The response cannot fully rule this out — no amount of citation can prove a negative about a counterfactual level of effort not spent — but the specific composition of the fifteen-month effort makes the "under-resourced" explanation weak on its own terms: this is not one under-funded lab working in isolation, it is at least six independent research groups, publishing at four of the strongest venues in the field (ICML, ICLR, AAAI, ACL), each bringing a genuinely different technical approach (human annotation at scale, programmatic fault injection with a trained 8B model, cognitively-motivated two-stage heuristics, full-trace observability, MAST-taxonomy-guided multi-agent verification teams) to the same underlying problem, and the ceiling moved from 14.2% to 59.5% — real, substantial progress, but progress that required a genuinely new architectural approach at nearly every step (ErrorProbe's own three-stage pipeline is not a scaled-up version of Who&When's baselines, it is a structurally different approach), not merely more compute applied to the same technique. A problem with an obvious solution typically does not require this many structurally distinct approaches in sequence to make incremental progress; it typically yields to the first well-resourced, competent attempt scaled up. The Verified Repair Memory data point (§3.2.4) strengthens this specific response further, because it is Granite's own first-hand evidence, not a literature-review inference: a mechanism that sounds trivially cacheable failed its one real test for reasons the team itself does not yet fully understand (a conservative verification bar, or a genuine backbone-strength limit — the project states honestly that it does not know which).

**Second-round challenge:** "ErrorProbe's own 59.5% figure came from Claude 3.7 Sonnet — a much stronger backbone than the local 3B model every Granite spike so far has run on. Doesn't that mean the 'no obvious solution' argument is partly an artifact of comparing a strong-backbone published number against Granite's own weak-backbone spike numbers, rather than genuine evidence the *problem* is hard?"

**Response.** This is the single most technically precise challenge available against characteristic 2, and it should be answered by conceding the specific comparison it targets rather than defending it: `ErrorProbe_Baseline_Selection.md`'s own caveat (§2.1.3 of the main text) already states this directly — "this is a literature-based comparison, not a controlled experiment... part of ErrorProbe's margin could come from using a stronger backbone rather than a strictly better method," concluding "treat it as strong, not airtight, evidence." Applied specifically to this challenge: Spike 1's own 12.5% step accuracy is not being cited anywhere in the project's documentation as a like-for-like comparison against ErrorProbe's 59.5% — it is cited as evidence the *simplified reproduction, on a free local backbone* is not yet close to the target, which is a different and more defensible claim than "backbone-controlled, the method itself only reaches 12.5%." The characteristic-2 argument's real load-bearing evidence is the field-wide timeline (14.2% → ~40% → 59.5% across six independent groups over fifteen months, §3.2.2), which does not depend on Granite's own backbone choice at all — it is entirely a claim about the published literature's own numbers on their own stated backbones. Spike 1's number is supporting, first-hand evidence of difficulty encountered directly, not the argument's primary evidentiary pillar, and conflating the two would indeed be the weak, backbone-confounded argument this challenge correctly warns against.

### C.3 Characteristic 3 — Depth of knowledge

**Hardest challenge:** "Isn't 'we reimplemented a paper's architecture from its description' just software engineering, not evidence of graduate-level depth of knowledge?"

**Response, from the source evidence.** The response has to concede part of this challenge honestly: reimplementing a described architecture is indeed a software-engineering skill, not by itself a research-depth claim. What elevates it past ordinary engineering, per §3.3.2, is the combination of two specific facts: the source material to reimplement from is a peer-reviewed paper's *methodology description*, not released code (meaning ambiguous implementation choices had to be resolved through informed technical judgment, not read off a repository), and the team's own honest framing of what was cut (no tool-grounded Investigator, no Verified Episodic Memory, in the Spike 1 reproduction) demonstrates the team understood which architectural pieces were load-bearing enough to require a later, fuller rebuild and which could be responsibly simplified for a first-pass number. A team that could not distinguish these would not be able to state, as the AI usage log does, "the team must be able to state precisely what was cut and why when asked" — that specific, precise self-awareness about what a simplification actually costs is closer to the accord's own "analytical approach... based on well-founded principles" than either a naive from-scratch attempt or a documented-library integration would be.

**Second-round challenge:** "Reproducing without the original code means there's no ground truth to check the reimplementation against — isn't 'we can't verify our own reproduction is faithful' a research-integrity problem, not evidence of depth?"

**Response.** The honest answer concedes the underlying risk rather than arguing it away: without ErrorProbe's own code, the team genuinely cannot confirm every implementation detail matches the original, and risk-register R1's own status line (§2.9.2) reflects exactly this uncertainty — "Open — downgraded from top priority. Real evidence in hand; still need the full 3-stage+memory version on a stronger backbone before this is closed." What keeps this from being a research-integrity failure rather than an honestly-managed risk is that the project does not claim faithfulness it cannot verify: Spike 1 is explicitly labeled a *simplified* reproduction, with its own specific, named omissions (no tool-grounded Investigator, no Verified Episodic Memory), and the AI usage log itself states the team "must be able to state precisely what was cut and why when asked" — i.e., the response to unverifiable faithfulness is not to claim faithfulness anyway, but to be precise about exactly which pieces were and were not attempted, and to treat the resulting number (12.5% step accuracy) as evidence about the simplified pipeline specifically, not as a disguised claim about the full architecture's own performance. A genuine research-integrity problem would be presenting Spike 1's number as if it settled how well the full ErrorProbe architecture reproduces; what is actually on record is the opposite — an explicit, named scope boundary around what the number does and does not establish.

### C.4 Characteristic 4 — Familiarity of issues

**Hardest challenge:** "You're using the same n=3-with-zero-observed-failures result as both a stated limitation elsewhere (R10) and as supporting evidence here for 'infrequently encountered.' Isn't that having it both ways?"

**Response, from the source evidence.** §3.4.2 already anticipates and answers this directly: the two framings are not in tension because they answer different questions. "Do we have strong evidence the detector generalizes to real, naturally-occurring failures" (R10's question — the honest answer is no, n=3 is thin) is a distinct question from "is this the kind of failure a typical practitioner encounters routinely enough to have existing tooling and instincts for" (this characteristic's question — the same small sample, read for what it shows about frequency rather than about detector performance, does support "infrequently-encountered," and the structural/definitional argument — silent failures are invisible to try/catch and schema validation by construction — needs no sample size at all to be true). A panel pressing this challenge should be met with the direct acknowledgment that the same fact is doing two different jobs in two different places, and both jobs are legitimate uses of it, precisely because neither one overclaims what a sample of three can support.

**Second-round challenge:** "If cross-architecture generalization is 'uncommon' only because no paper has tried it yet, rather than because it's genuinely hard, isn't 'infrequently encountered' actually describing a neglected research direction, not an unfamiliar one — which is a different, weaker claim than characteristic 4 needs?"

**Response.** This is a fair distinction to draw between "unattempted" and "unfamiliar/hard," and the honest answer concedes part of it: the literature-review finding by itself (no paper tests transfer to an unseen architecture) cannot, on its own, distinguish "nobody has tried because it's genuinely difficult" from "nobody has tried because attribution accuracy within a known ecosystem was already occupying the field's full attention." What tips this from a pure neglect story toward a genuine difficulty story is Spike 2's own first-hand evidence: instrumenting CrewAI — a framework genuinely outside every paper's own ecosystem — required real engineering work (risk-register R2's own honest follow-up note that "timestamps were captured post-hoc, not via real per-step hooks... real hooks needed in the actual build," §3.3.3) to even reach the structural-mapping stage, before any accuracy claim could be attempted at all. This is direct, first-hand evidence that instrumenting a genuinely new architecture is not a zero-cost extension of existing tooling — it required its own real friction to get even the easy, structural half working. That does not prove the field's neglect of this direction is entirely explained by difficulty rather than prioritization, and the response should say so plainly rather than overclaim, but it is evidence against the "purely unattempted, not actually hard" reading this challenge proposes.

### C.5 Characteristic 5 — Level of problem

**Hardest challenge:** "LangSmith Engine and Arize Alyx already shipped automated diagnosis features in 2026 — doesn't that mean the practice is no longer 'outside standards,' undermining the top tier?"

**Response, from the source evidence.** This challenge is, in effect, the exact challenge R9 already caught and corrected against internally (§3.5.2) — the original claim was indeed too strong ("nobody automates this") and was walked back once LangSmith Engine and Arize Alyx were checked directly. The corrected, narrower claim is the one that actually survives this challenge: not that no automated diagnosis exists anywhere, but specifically that none of the seven checked platforms confirm counterfactual fix-testing with a measured recovery rate, or general (non-RAG-specific) silent-failure detection, as a standardized, published capability. A panelist naming LangSmith Engine or Arize Alyx by name should be told directly that this correction already happened once, internally, and the current claim is the one that survived that correction — which is a stronger position to be in than if the correction had never happened and the panel discovered the gap first.

**Second-round challenge:** "The Guide Compliance Audit's own deeper pass found the security/privacy threat model (R16) was missing until a finer-grained audit caught it (§12 of that audit). Doesn't a gap surviving the first, coarser compliance pass suggest 'beyond standard practice' might also be true in an unflattering sense — i.e., that even Granite's own team doesn't yet have standard practice worked out for building this kind of tool safely?"

**Response.** This challenge deserves to be met head-on rather than deflected, because it draws a genuinely sharp connection between two facts the project's own documents keep separate. The honest answer is: yes, in a narrow and specific sense, this is true, and it is worth stating plainly rather than resisting — the R16 gap (§3.1.2's own account) is direct evidence that the team's *own* practice for building this exact category of tool safely was still forming as recently as the deeper compliance pass that caught it, which is a small-scale, first-hand instance of exactly the industry-wide "practice is actively forming, not settled" claim this characteristic makes about the field generally. Rather than undermining characteristic 5's argument, this is a second, independent, first-hand data point supporting it: if even a team building directly in this space, aware of the guide's own requirements, needed a second, finer-grained audit pass to surface a real gap in its own security posture, that is consistent with — not contradictory to — the claim that no mature, settled standard practice yet exists for this category of tool, at the industry level or, evidently, within this project's own working process until the gap was caught and closed.

### C.6 Characteristic 6 — Stakeholder involvement

**Hardest challenge:** "If this is genuinely the weakest characteristic, why is it still counted as 8-of-9 'clear' rather than the project honestly admitting its CCP case has a real hole?"

**Response, from the source evidence.** The honest response has to concede the premise partially: this genuinely is the weakest part of the CCP case, and the project's own documents say so in exactly those terms — §3.6.4 names it as "the one item nothing here can close" through further internal work. But "weakest characteristic" is not the same claim as "the CCP case has a disqualifying hole," and the accord's own framework (per the guide's explicit note that a project need only clear "some or all" nine, not all nine, §2 of the plan doc) does not require every characteristic to independently clear the top tier for the overall CCP case to stand. The 8-of-9 framing is not an attempt to average away the weakness; it is a precise statement that eight characteristics are independently, strongly evidenced, and one is honestly not yet evidenced strongly enough to claim the top tier — which is a materially more defensible position at a panel than either quietly inflating the ninth to match the others, or abandoning the CCP claim altogether over one honestly-scoped gap that the guide itself names as the single most commonly under-argued characteristic across FYP projects generally (§3.6.2).

**Second-round challenge:** "Isn't naming '8 of 9' in every headline summary (the plan doc's own checklist, `generate_ccp_docx.py`'s closing paragraph, the registration form answers) itself a form of repetition designed to make the honest gap feel smaller through familiarity, even if no single instance overclaims?"

**Response.** This is worth taking seriously as a rhetorical-effect question rather than a factual one, since no single instance of "8 of 9" is inaccurate. The distinguishing fact available in the source material is that every one of these repeated instances is paired with the same specific, unchanged caveat, not a progressively softened one — `generate_ccp_docx.py`'s own closing paragraph states "with stakeholder involvement honestly rated at the middle tier until real stakeholder feedback is obtained — not inflated to match the others" every time the 8-of-9 figure appears in that document, and the registration form answers (§FYP_Registration_Form_Answers.md, Complex Computing Problem section) repeat the identical qualifier rather than dropping it in a shorter, later restatement. Repetition that consistently carries its own caveat forward is different in kind from repetition that lets a caveat quietly drop out of later, shorter summaries — the latter is the actual mechanism by which repetition erodes an honest qualifier over time, and the source documents do not exhibit it here; the qualifier is present in the CCP-justification docx, the registration form, and Part 3's own closing synthesis (§3.10.1) alike.

### C.7 Characteristic 7 — Consequences

**Hardest challenge:** "The three named scenarios (wrong refund, unverified budget, stock-count mismatch) are all hypothetical illustrations, not documented real-world incidents. Doesn't 'significant consequences in a range of contexts' require actual evidence of real harm having occurred, not plausible examples?"

**Response, from the source evidence.** This is a fair distinction to draw, and the honest answer is that the three scenarios are illustrative, drawn from the project's own active benchmark domain (tau-bench retail) rather than documented incident reports (§3.7.3) — no source document claims otherwise. What grounds the severity claim in something beyond pure hypothesis is the structural argument, not the specific scenarios: by construction, a silent failure produces no error signal, meaning the class of harm being described is not merely plausible but is the *direct logical consequence* of the failure class's own definition (§3.7.2) — an incorrect output that passes every check will, by definition, reach whatever consumes that output, whether that is a human end user or a downstream automated process, with no filtering mechanism catching it first. The commercial-convergence evidence (seven platforms independently investing in adjacent tooling) is offered as supporting, not load-bearing, evidence for this characteristic, and §3.7.4 already states explicitly that this evidence should not be over-read as seven companies validating the silent-failure framing specifically — a caveat this response should repeat rather than let a panelist discover independently.

**Second-round challenge:** "The three scenarios all come from a single dataset domain (retail/customer support). Isn't 'a range of contexts' actually being claimed on the strength of one context described three different ways?"

**Response.** This challenge correctly identifies a real scoping fact worth conceding directly: §3.7.3 already states plainly the three scenarios "are drawn from, and consistent with, the project's own active benchmark domain: tau-bench retail" — meaning the "range" being claimed is explicitly a range of *failure shapes* (a numeric-value error, a constraint-violation error, a cross-agent-consistency error) within one *domain*, not a range of domains. The accord's own top-tier language ("significant consequences in a range of contexts") is more naturally read, and should be defended as being read, at the level of deployment context rather than benchmark domain: the claim is that this class of failure recurs across any production multi-agent deployment (customer support, coding assistants, research tools — the same three categories named in the project's own opening problem statement, §0.1 of the plan doc), of which tau-bench retail is one concretely-evidenced instance, not the sole context the claim is scoped to. This is a real distinction worth stating precisely if pressed: the *evidence* (three scenarios) is single-domain; the *claim* (recurs across any production multi-agent deployment) is domain-general, and the honest position is that the claim is broader than what the three scenarios alone directly demonstrate, resting instead on the structural argument (§3.7.2) for its domain-general reach.

### C.8 Characteristic 8 — Interdependence

**Hardest challenge:** "A ten-step pipeline where each stage feeds the next is just normal software architecture — most systems have sequential dependencies. What makes this interdependence 'complex' rather than merely 'has multiple steps'?"

**Response, from the source evidence.** §3.8.2's own double-sense argument is the direct answer: the challenge is right that sequential pipeline dependency alone (the "first sense") would be a weak claim on its own — most software has sequential stages. What the characteristic actually rests on is the *second* sense holding simultaneously: the subject matter being diagnosed is itself interdependent, meaning failures propagate causally through a chain of agents whose outputs each depend on a possibly-already-corrupted upstream output, which is precisely why "symptom-driven backward tracing" is a real technique with a real purpose in this field (§3.8.2) rather than an arbitrary implementation choice. Spike 6's specific test of a *cyclic* dependency (Researcher↔Critic, iteratively depending on each other) is the sharpest available evidence distinguishing this from ordinary sequential-pipeline interdependence — a true cycle is a strictly harder interdependence structure than a linear chain, and the fact that an unbounded traversal of it does not naturally terminate (hitting the 10,000-step safety cap when the bound was deliberately disabled) is concrete, measured evidence that this specific interdependence structure required non-trivial handling, not evidence that could be produced by a simple sequential pipeline.

**Second-round challenge:** "Isn't citing Granite's own architecture — a graph-based tool built specifically to model interdependence — as evidence that the underlying problem is interdependent somewhat circular? Of course a tool designed around graphs will find its own subject matter graph-shaped."

**Response.** This is a fair methodological concern about the direction of evidence, and it deserves a direct answer rather than a restatement of the double-sense argument alone. The response has to distinguish where the interdependence claim's evidence actually originates: it does not originate from Granite's own architecture at all — it originates from ErrorProbe's own pre-existing "symptom-driven backward tracing" mechanism (§2.1.1, §3.8.2), a technique the field adopted *before* Granite existed, precisely because failures in these systems were independently observed to propagate through causal chains rather than appear at their true origin. Granite's own graph-based architecture is a *response* to an interdependence property the field had already identified in its shared subject matter, not the source of the claim that the subject matter is interdependent — the causal ordering runs from "the field found failures propagate causally, hence backward tracing is a real, adopted technique across multiple independent papers (Who&When, AgenTracer, SDBL, ErrorProbe all reason about propagation paths in some form)" to "Granite, like its predecessors, builds a graph-based tool to handle this," not the reverse. Spike 6's own cyclic-graph result is empirical evidence of a specific, harder-than-linear interdependence structure actually existing in a concrete test case (a LangGraph retry loop), which is closer to direct observation than to architecture-shaped confirmation bias.

### C.9 Characteristic 9 — Requirement identification

**Hardest challenge:** "Citing Recovery Controller's total lack of POC evidence as supporting evidence for 'ill-defined or unknown' looks like spinning a weakness into a strength. How is this different from just excusing an unfinished feature?"

**Response, from the source evidence.** §3.9.3 already draws the exact distinction this challenge is asking for: the claim is not "any unfinished feature counts as evidence of difficulty" (which would indeed be spin) — it is that Recovery Controller specifically was committed to the foundational core *without* the team first attempting even a minimal spike, which is a documented departure from the team's own standing pattern of running a quick proof-of-concept before or immediately after committing an item to the core (eight of the ten foundational items already carry at least some real spike evidence). A team that runs spikes routinely, except specifically for the one item it has explicitly logged as "genuinely new mechanical work, not a rename of anything already tested," is showing something different from a team that simply hasn't gotten around to a feature yet — the *absence of even an attempted spike*, against a background pattern where spikes are otherwise the norm, is the specific signal being pointed to, not the absence of a finished feature in itself. A panelist should be told this distinction directly if this challenge is raised, since without it the argument does risk sounding exactly like the spin the challenge accuses it of being.

**Second-round challenge:** "DoVer (§B.8 above) argues single-step attribution itself is 'ill-posed' because multiple distinct interventions can independently repair the same failure. Doesn't that suggest the requirement-identification problem here isn't just 'hard' but potentially unsolvable in the form the whole pipeline assumes — which would undermine feasibility, not just difficulty?"

**Response.** This is the sharpest possible challenge to characteristic 9, precisely because it targets the formalism the entire committed core depends on, not merely the current state of evidence for it, and it deserves to be met without minimizing what DoVer actually argues. The honest response is the same one already given for this exact critique in §B.8: Granite's own (i*, t*) formalism is inherited from Who&When and shared by every paper Granite measures itself against, so if DoVer's critique holds, it is a critique of the field's entire shared approach, not a Granite-specific defect — but this does not fully dissolve the challenge, because "shared by the whole field" is not the same as "therefore not a real problem." The project's own standing position, per the R7 policy, is to treat this as a real, named, unresolved risk to the shared formalism rather than either dismissing DoVer or attempting to resolve the critique within this FYP's own scope — and it is worth being explicit about what that position actually costs: it means characteristic 9's own "ill-defined or unknown" framing is itself potentially under-describing the difficulty, since "ill-defined" still presumes a single correct answer exists to be found, which is exactly the presumption DoVer challenges. A fully rigorous response would flag this as a limitation of the CCP argument's own precision, not paper over it — the honest position is: the project treats the cause as ill-defined-but-singular because that is the formalism the entire field it builds on shares, while acknowledging, on the record, that a credible critique of that shared premise exists and has not been engaged with substantively within this project's own scope.

---

## D. Cross-References — Connecting Decisions Across Parts 1, 2, and 3

Each item below states a connection between a decision made in one Part and a decision, gap, or piece of evidence in another — included only where the source material actually supports the link, not where it is merely plausible that two things might relate.

**D.1 — Characteristic 6's weakness (Part 3) connects directly to the open stakeholder-contact item named in Part 1's specifiability discussion and the guide-compliance audit.** These are not two separate gaps that happen to resemble each other; they are the same gap, named three times from three different angles across the project's own documents. Part 1, §1.6 establishes the four stakeholder groups (on-call engineers, benchmark researchers, QA/compliance teams, platform teams) as part of the client-framing discussion required by guide §5.2. Part 3, §3.6 rates characteristic 6 at the middle tier precisely because none of those four groups have been contacted. The plan doc's own closing checklist (§16) and the Guide Compliance Audit's §12 sub-table both independently flag the same underlying absence — real stakeholder engagement — as the single item "nothing here can close" through further internal writing. A panel probing any one of these three documents on this point will find the identical gap named the same way in the other two, which is itself evidence the gap is being tracked consistently rather than described differently depending on which document happens to be open.

This connection is worth pressing one level further than the bare observation of consistency, because it also explains *why* Part 1's client-framing section (§1.6.1) names four stakeholder groups at all rather than a vaguer, unenumerated "stakeholders exist" claim. The specificity itself is a direct consequence of characteristic 6 already being flagged as weak: a vague client-framing section would have made the characteristic-6 gap harder to state precisely (what, exactly, is missing, if the stakeholders were never individually named?), whereas naming four distinct groups with distinct stated needs turns "stakeholder contact is missing" into a checkable, closeable to-do list rather than an open-ended aspiration — each of the four groups in §3.6.3 has its own concrete description of what "real engagement" would need to look like. The precision in Part 1's client framing and the precision in Part 3's honest rating are therefore not two separately-achieved virtues; the second could not exist in its current, specific form without the first having already enumerated exactly who is missing from the evidence base.

**D.2 — The title's naming choice (Part 1) connects to the market-survey findings underlying Part 2's Repair Agent addition and Part 3's characteristic 9 update.** The adopted title's own two newest-named mechanisms — "Verified Repair, and Recovery" — did not exist as committed foundational items until the sixth and ninth AI-usage-log sessions respectively (§1.1.4, §2.6.5, §2.6.8). This means the title itself is not merely descriptive of a static feature set; it is dated evidence that the title was chosen only after the underlying scope had already absorbed the market survey's own findings, not before. The same market survey session that supplied the title (§1.1.2) is the session that added Repair Agent (closing the FR4 gap, §1.6.2) and, days later, the reclassification session that moved Recovery Controller and Verified Repair Memory into the foundational core — the same session characteristic 9's own justification cites directly ("Updated 2026-08-24: Recovery Controller... was added to the committed core the same day with zero POC evidence," §3.9.1). The title, the feature-list evolution, and characteristic 9's own evidentiary update are three faces of the same single dated event, not three independent developments that happen to share a date.

There is a second, subtler layer to this connection worth drawing out: the title's own internal structure (§1.1.4) — "Self-Healing" as the unifying frame, with "Semantic Error Diagnosis, Verified Repair and Recovery" as the three named stages beneath it — is only fully accurate as a description of the committed core *after* the ninth session's reclassification, not merely after the sixth session's Repair Agent addition. Before the ninth session, Recovery Controller and Verified Repair Memory sat in the extensions list, meaning "Recovery" in the title would have been naming a mechanism that was, at the moment the title was adopted (session seven, between sessions six and nine), still classified as optional rather than committed core. This is a small but real sequencing wrinkle worth being honest about: the title was adopted one session before the scope fully caught up to justify its own "and Recovery" clause at foundational-core strength, and it is only in retrospect, once the ninth session's reclassification is accounted for, that the title and the current scope description align exactly. No source document flags this specific sequencing gap; it is visible only by reading the session dates against each other closely, which is precisely the kind of cross-document check this addendum exists to perform.

**D.3 — The Stream A defense against single-framework scope-narrowing (Part 1, §1.3.4) connects directly to CCP characteristic 1's third named tension (Part 3, §3.1) and to RQ2 (Part 2, §2.3).** This is a single decision traceable through all three Parts: the market survey's own advice to narrow to one framework would have simultaneously (a) violated the Stream A rationale for keeping RQ2 as a Primary research question, (b) eliminated the generalization-vs-specialization tension that CCP characteristic 1 names as one of its three conflicting requirements, and (c) removed the evidentiary basis Spike 2 was run to support. Rejecting the advice (R19) is not three separate defensive moves in three separate Parts of this document — it is one decision whose consequences ripple identically through the identity argument, the research-question framing, and the CCP rating, which is exactly why §1.3.4 states the rejection cost was "one of this project's two lead research claims," not merely a scope preference.

It is worth naming explicitly what makes this a genuine cross-Part connection rather than the same fact restated three times under three different headings: each Part evaluates the decision against a *different standard*, and the decision survives all three independently rather than being validated once and then merely cited twice more. Part 1 evaluates it against the guide's own Stream A criteria (does the project still meet the "gap derived from published research" and "reproduction-feasibility risk" tests) — it does. Part 2 evaluates it against the evidentiary basis for RQ2 specifically (is there real, already-run evidence the generalization claim is worth defending) — Spike 2's CrewAI mapping is that evidence. Part 3 evaluates it against the accord's own definition of a conflicting requirement (does keeping this tension unresolved cost something real and stated, or is it a costless preference dressed up as principle) — the R19 entry's own explicit statement of the accuracy cost forgone answers this. A decision that only passed one of these three tests would be a weaker, single-Part justification; passing all three independently, under three different evaluative standards, is what makes this cross-reference load-bearing rather than decorative.

**D.4 — The external-component classification table's Semantic Error Diagnostic commitment (Part 1, §1.8.2) connects directly to the "From Confident Closing to Silent Failure" paper's own empirical finding (Part 2, §B.8 above) and to RQ3 (Part 2, §2.3).** Two independent lines of reasoning arrive at the identical architectural conclusion from different directions: the plan doc's own table commits the Semantic Error Diagnostic module to rule/schema-based verification specifically to avoid the risk that "the project's actual differentiator becomes an API call wearing a system architecture" — a design-principle argument, made before the R7 triage's second pass surfaced the Advani paper. That paper's own empirical result (LLM judges AUROC ≤0.65, lightweight statistical detectors 0.83–0.95) arrives at the same practical conclusion from pure measurement, on a genuinely large real-world dataset, with no reference to Granite's own architecture at all. A design principle and an independent empirical result converging on the same architectural choice is stronger support for that choice than either alone — and this is a connection the source documents make available but do not state explicitly themselves, since the Advani paper was only escalated to High threat status in a later triage pass than the one that produced the external-component table; this addendum is the first place in the project's documentation this specific cross-reference is drawn out.

It is worth stating precisely what this connection does and does not license, since it would be easy to overstate: it does not mean the external-component table's own commitment was *caused* by the Advani paper (the chronology runs the wrong way for that — the table's design principle predates the paper's escalation to High threat), and it does not mean Granite's own architecture has now been empirically validated by the Advani paper's numbers, since Granite has not run its own Semantic Error Diagnostic module against tau2-bench or AppWorld, only against Spike 4's much smaller mechanism test. What the connection licenses, precisely, is a stronger *prior* — a design choice made on architectural-purity grounds, later found to align with an independent, large-scale empirical result the team did not have in hand when the design choice was made, is more likely to be the right choice than a design choice with no such independent confirmation at all, without this rising to the level of the choice being proven correct by Granite's own evidence.

**D.5 — The abandoned TracerTraj self-generation attempt (Part 2, §2.5) connects to the dataset choices underlying CCP characteristic 7's named scenarios (Part 3, §3.7.3) and to the SDG 17 secondary-candidate argument (Part 1, §1.5.3).** The pivot away from self-generating a synthetic AgenTracer-style dataset, once real pilot timing data showed the cost was infeasible (§2.5.3), is the direct reason the project's active benchmark plan settled on GSM8K and tau-bench retail (§2.5.5). tau-bench retail is, in turn, the direct source of the three consequence scenarios (wrong refund, unverified budget, stock-count mismatch) that ground characteristic 7's severity argument, and it is a dataset chosen partly because it is already public and MIT-licensed — directly consistent with, and part of the evidentiary basis for, the SDG 17 open-data argument in §1.5.3. A single abandoned technical attempt, once its real cost was measured rather than assumed, redirected the benchmark plan in a way that now underwrites both a CCP characteristic's own named scenarios and a secondary SDG alignment claim — none of which would read the same way had the self-generation attempt either succeeded or never been tried at all.

This chain is also a useful worked example of a distinction worth making explicit for a panel: not every downstream consequence of a decision needs to have been the *reason* for the decision to still be a real, defensible connection. The self-generation attempt was abandoned purely for a cost reason (ten minutes per task, extrapolating to multiple days at scale, §2.5.3) — nobody chose to abandon it *because* GSM8K and tau-bench retail would later ground a CCP characteristic's scenarios or an SDG secondary-candidate argument; those downstream benefits are consequences discovered afterward, not motivations that drove the original decision. Stating this distinction plainly matters because a panel is right to be suspicious of a project that claims every decision was made with full foresight of every later benefit — the honest, and actually more credible, account is that a cost-driven pivot happened for its own narrow reason, and the fact that it turned out to also support two later arguments is a genuine but retrospectively-discovered alignment, not evidence of foresight the team should claim credit for having had at the time.

**D.6 — The propagation discipline named in Part 1 (§1.2.6) is the same mechanism that makes Part 2's feature-list evolution (§2.6) and Part 3's characteristic ratings auditable at all.** This is a structural connection rather than a content connection, worth naming because it is easy to read Parts 1 through 3 as three separate arguments rather than one system: every dated correction and every renamed feature that Part 2 traces through nine AI-usage-log sessions is legible as a coherent history only because the propagation discipline documented in Part 1 (log every cross-cutting change, in every file it touches, in the same working session) was actually followed. Without that discipline, Part 3's own CCP characteristics — several of which cite specific, dated updates (characteristic 2's Verified Repair Memory addendum, characteristic 9's Recovery Controller addendum, both dated 2026-08-24) — would have no reliable way to state which version of the feature list a given rating was actually checked against. The propagation discipline is not merely a Part 1 naming-history curiosity; it is the load-bearing mechanism that keeps Parts 2 and 3's own dated claims checkable against each other.

This connection is worth closing with the single clearest test case available: the ninth session's own reclassification decision (§2.6.8) is legible today, with its full reasoning intact, specifically because the eighth session's own additions were propagated and logged in enough detail (which files were touched, what the "Foundational (8)" / "Extensions (10)" heading pair looked like before correction) that the ninth session could identify and describe exactly what state it was correcting *from*. Had the eighth session's propagation been informal or partially logged, the ninth session's own correction — including the specific, honest detail that the supervisor PDF generation script itself "had been left in a partially-edited intermediate state" and needed an actual code fix, not just a re-run — would not be traceable as a correction at all; it would simply look like a second, unexplained version of the same numbers. The propagation discipline is what turns a sequence of changes into a documented history of *reasoned* changes, which is the entire evidentiary basis Part 2's feature-list-evolution argument (§2.6.9, §F.4 above) rests on.

---

## E. Further Granular Sub-Questions — the Part 1 Blocks Not Yet Pressed

Section A above worked through title, naming, Stream A, SDG, and client/specifiability. Three more Part 1 blocks — external component classification, team ownership, and the architecture sketch — carry the same kind of skeptical follow-up worth applying directly, using only what §1.8, §1.9, §1.10, and §1.7 already establish.

### E.1 On the external-component classification table (§1.8)

**Q: The table claims fault-injection operators are "0% API-dependent," but doesn't the choice of *which* faults to inject still require some judgment call that could be LLM-assisted, even if the corruption mechanism itself is rule-based?** The distinction the table is careful to draw, per §1.8.2, is between *designing* the taxonomy of injectable fault types (a one-time, human design decision — currently one validated type, corrupted tool output, with two more taxonomized for extension #1) and *executing* an injection at benchmark-build time (which is what the 0% figure actually describes — applying an already-designed, deterministic corruption function to a known input). The table's 0% claim is scoped to the execution mechanism, not to the upstream design process of the taxonomy itself, and this scoping should be stated explicitly if a panelist presses on it, since the table's own prose does not spell out this distinction as sharply as this response does.

**Q: If the confidence-scoring formula is borrowed from GraphTracer, an unpublished-status paper elsewhere flagged as a preprint (§2.2.8), doesn't building a 0%-API-dependent component on a preprint's formula import the same "unreviewed result" risk the project explicitly avoids elsewhere (the R7 policy)?** This is a fair internal-consistency question, and the honest answer distinguishes two different kinds of reliance the project treats differently: R7's policy governs *citing an unpublished paper's claims as settled evidence* (e.g., adding a preprint as a benchmark baseline, which the project explicitly declines to do); using a formula's *structural idea* (compute confidence from graph topology — out-degree, betweenness centrality — rather than from an LLM's self-report) is an architectural choice the project can adopt and test independently of whether the source paper's own claims are peer-reviewed, precisely because the mechanism's correctness does not depend on GraphTracer's own experimental results being valid — it depends only on graph-topology-based confidence being a reproducible, auditable computation, which is true regardless of GraphTracer's own publication status. No source document states this distinction explicitly; it is offered here as the correct application of the project's own stated policy to a case not directly addressed in the R7 entries themselves.

**Q: The table's "byte-identical output" replacement-test standard (§1.8.3) is a strong claim — has it actually been tested by literally swapping the LLM API and diffing output, or is it asserted from the architecture alone?** The source material does not record an actual swap-and-diff test having been run — the claim is architectural (these components never call the LLM, so a swap cannot affect their output), not empirically verified by a real swap experiment. This is worth stating plainly: the claim is currently a design guarantee following from the 0%-dependency commitments, not yet a tested behavior, and the honest framing at defense should be "this is true by construction, given the committed mechanisms, and has not yet been separately empirically verified by an actual model-swap test" rather than implying a swap test has already been run.

### E.2 On team ownership (§1.9, §1.10)

**Q: If none of the three roles have been assigned to specific people yet (R6, still open per §1.10.1), how can the "if removed, what disappears" test in plan doc §9 be treated as already satisfied rather than merely hypothetical?** The honest answer distinguishes what the test actually establishes from what it doesn't yet establish: the test as currently answered establishes that the three *role areas* are each independently necessary and non-redundant — remove the Data/Benchmark role's work and the benchmark disappears, remove the Diagnosis role's work and the attribution claim disappears, remove the Platform role's work and the deployable product disappears. This is a genuine, defensible answer to "is the work structured so each area is independently meaningful," which is what Section 5's test is actually checking for at the scope-design stage. It does not yet establish that three specific, named individuals each have a real, personally-defensible subsystem, because that requires the assignment (R6) to have actually happened — the test is satisfied at the role-design level, open at the person-assignment level, and a panel probing this should be told exactly which of the two levels is settled and which is not.

**Q: Does the guide's four-question defensibility test (§14.1) actually have real answers for each role, or only plausible-sounding ones?** §1.10.2 already names one real answer per role, each traceable to a specific, already-documented design decision — the Data/Benchmark Owner's "alternatives rejected" answer is the rule-based-vs-LLM fault-injection decision (§1.8.2); the Diagnosis Owner's is the constraint-based-vs-LLM-judged Semantic Error Diagnostic decision (§1.8.2, the single most important commitment in the whole table); the Platform Owner's is the namespacing-vs-full-multi-tenancy decision (extension #4, §1.9.2). Each of these is a real, dated, reasoned decision already on record elsewhere in the project's documents, not a plausible-sounding answer invented to satisfy this specific test — which is itself the strongest evidence available that the test is passable in practice, since the answer already exists rather than needing to be constructed under panel pressure.

### E.3 On the architecture sketch (§1.7)

**Q: The sketch's own header calls it "not a final design" — doesn't that undercut its value as evidence for guide §16's one-page architecture requirement?** No, and the reason is that guide §16 itself only requires a sketchable, coherent shape at proposal stage, not a finished design — the caveat is the sketch correctly scoping its own claim rather than overclaiming a level of design maturity the project hasn't reached yet, which is the same honesty discipline visible everywhere else in Part 1. A sketch that claimed to be final at this stage, when the team ownership assignment itself (§1.10.1) is still open, would be a more overclaimed and less defensible document than one that states its own provisional status plainly.

---

## F. Further Granular Sub-Questions — the Part 2 Blocks Not Yet Pressed

Section B above worked paper by paper through the seven-plus-two-paper corpus. Four more Part 2 blocks — the datasets table, the evaluation metrics table, the risk register as a whole, and the feature-list evolution history — carry their own skeptical follow-ups worth applying directly.

### F.1 On the datasets (§2.7)

**Q: GSM8K and tau-bench retail were chosen partly because they fit already-built detection mechanisms (Spike 4's numeric near-miss check) — isn't there a risk the benchmark is being shaped to flatter the detector rather than stress-test it fairly?** This is a genuinely sharp methodological question, and the honest response has to concede the shape of the risk rather than dismiss it: choosing datasets partly because they fit an already-validated mechanism does create a real possibility that the benchmark under-represents failure types the current detection mechanism handles poorly. The mitigating facts already on record are: (a) the datasets were also chosen for reasons independent of mechanism-fit — tau-bench retail specifically for its richer ground truth and domain match to the stated client (§2.7.2), not only for numeric-near-miss compatibility; (b) the fault-taxonomy-widening extension (#1) is explicitly scoped to add two more, structurally different fault types (communication corruption, context truncation) beyond the single validated type, which is a direct, planned mechanism for testing the detector against failure shapes it wasn't chosen to flatter; and (c) MATH was explicitly benched rather than actively used specifically because its answer format (equations, sets, intervals) does not fit the existing numeric-near-miss mechanism as cleanly (§2.7.3) — which is itself evidence the team is aware of, and tracking, exactly this fit-vs-fairness tension, rather than being blind to it.

**Q: The benchmark's target scale (500–1,000 traces) matches AgenTracer's own scale — was this number derived independently, or simply copied from a paper whose own dataset turned out to be unreleased?** The datasets table's own stated reasoning (§2.7.4) is explicit that the target "matches AgenTracer's and the original pitch's scale," which is a stated precedent-matching choice, not an independently-derived statistical power calculation. This is worth being honest about directly: the source material does not record a from-first-principles justification for why 500–1,000 traces specifically is the right scale for the statistical claims the evaluation plan intends to make (confidence intervals on accuracy, precision/recall for the silent-failure detector) — it is a scale chosen to be comparable to the field's own precedent, which is a reasonable default in the absence of a derived target, but is a different, weaker kind of justification than a power calculation would provide, and a panel asking for the latter should be told the former is what actually exists.

### F.2 On the evaluation metrics (§2.8)

**Q: Nine metrics is a lot — how would a panel know these aren't just a kitchen-sink list assembled to look thorough rather than a genuinely necessary set?** The strongest available response is the two specific, dated corrections already on record (§2.8.1): silent-failure precision was added specifically because recall alone cannot distinguish a real detector from one that flags everything, and task completion rate was added specifically because it answers a different question than recovery rate (all runs vs. previously-failed runs only). Both additions are traceable to a named methodological gap the team caught in its own earlier metrics list, not to a desire to pad the list — a kitchen-sink list assembled for appearance would not typically come with a specific, stated reason each addition closes a specific measurement blind spot the previous version had. The two deliberately-excluded metrics (re-execution cost, repair reuse benefit, §2.8.1's closing paragraph) are the clearest evidence against the kitchen-sink reading: a team padding a metrics list for appearance would have every incentive to include these too, since more metrics look more thorough — the team instead excluded them explicitly because the features they measure (Recovery Controller, Verified Repair Memory) were not yet in scope at the time, which is a scope-discipline decision working directly against the kitchen-sink incentive.

### F.3 On the risk register as a whole (§2.9)

**Q: With 22 named risks, isn't it likely a panel could find at least one risk category conspicuously missing, undermining the register's apparent thoroughness?** The honest answer is that the register itself does not claim exhaustiveness — its own closing framing (§2.9.5) is explicit that the value of the register is not that it has covered every conceivable risk, but that the risks it does cover carry "genuine variance in outcome, all logged with the same rigor regardless of whether the result was favorable." A register that claimed completeness would be a stronger, and more easily falsified, claim than one that claims consistent rigor on what it does cover — and the source material supports only the latter claim, which this addendum preserves rather than inflating into the former.

### F.4 On the feature-list evolution (§2.6)

**Q: A feature count that changed six times (14→16→17→18→20) could be read as scope instability rather than disciplined iteration — how does a panel distinguish the two readings?** §2.6.9 already gives the direct answer, worth restating precisely because this is exactly the challenge that section pre-empts: the distinguishing fact is not that the count changed, but that every single change traces to a *named, external or evidentiary trigger* — a supervisor critique (session five), a POC spike closing a gap (session four), an external market survey surfacing a genuine capability gap (session six) and then, on a closer re-read of the same source, exposing an internal inconsistency in how the team was applying it (session nine). Scope instability, by contrast, would look like a count that changed for reasons the team itself could not name, or that reversed and re-reversed the same decision without new evidence in between. Every one of the six changes documented here has a one-sentence, dated, named cause a team member could state on demand — which is the operational difference between disciplined iteration and drift, and the one a panel should actually be listening for if this challenge is raised.

---

## G. The Twenty-Nine Rejected Short-Name Candidates — Era-by-Era Narrative, Then Mapped

### G.0 What `AI_Usage_Log.md` actually contains about naming, stated precisely before going further

Before expanding the narrative below, it is worth being exact about what the nine-session log does and does not contain on this topic, because the honesty discipline this whole document applies elsewhere applies here too. Searching all nine sessions for naming-related content surfaces exactly one entry: the seventh session's rename record (§1.2.2 of the main text, quoted there in full), which documents the *mechanics* of the TraceCause → Granite rename — the regex-based propagation, the eleven files touched, the two deliberate filename exclusions (`TraceCause_AgentTestLab_Pitch.md` and the physical PDF/docx filenames), and the explicit statement that prior log entries were left untouched as a historical record. The log does **not** contain a session-by-session record of when the twenty-nine rejected candidates were generated, debated, or individually rejected — that full list, and the single stated design principle behind the eventual winner, exists only in `FYP_Registration_Form_Answers.md` (§1.2.3), with no session attribution at all. This means the "era" framing already used in §1.2.4 and revisited below is this document's own interpretive reconstruction of a plausible sequence, built from the *content* of the names themselves (their register, their vocabulary family) rather than from any dated log entry recording when each cluster was actually brainstormed. Where the narrative below uses a phrase like "the team likely moved to Cluster 2 after Cluster 1 stalled," that is stated as inference, not as a documented sequence — no source file records the twenty-nine candidates' own internal chronology, only their final, undated, unordered list.

### G.1 Cluster 1, narrated — the forensic-diagnosis era

Reading the seven Cluster 1 names as a set (Rootcast, Autopsy, Undertow, Culprit, Recon, Triage, Fathom, plus Causeway as the cluster's own outlier), the throughline is that every word describes an *investigative act* rather than a finished state — a diagnosis in progress, not a diagnosis complete. This matters for understanding why the era (if it is read as an era, per the caveat in §G.0) would plausibly have given way to Cluster 2 rather than persisting: a name describing an investigative act works well for a tool whose entire value proposition is diagnosis, but Granite's own scope, as established across the AI-usage-log sessions traced in Part 2 (§2.6), never stayed diagnosis-only for long — the counterfactual-replay foundational item existed from the very first frozen feature list (session three, §2.6.2), meaning the project was already committed to a repair-and-recovery half of its identity well before any of these seven candidates could have been the final answer. The one piece of hard, dated evidence anchoring this cluster to something real, rather than pure speculation, remains the `agent-autopsy` folder name itself (§1.2.4) — a naming choice that predates, and was never revised alongside, the later TraceCause and Granite short-title changes, meaning it is the one surviving artifact from whatever the earliest naming pass actually was, regardless of exactly when in the project's life that pass happened.

### G.2 Cluster 2, narrated — the permanence/elemental era

The nine Cluster 2 names (Ripple, Vigil, Halcyon, Meridian, Zenith, Astra, Solstice, Vantage, Zephyr) share a register distinct enough from Cluster 1 that reading them as a deliberate pivot, rather than a continuation, is a reasonable inference even without a dated log entry to confirm it: every one of these nine is drawn from nature, astronomy, or a fixed physical/temporal reference point, and none of the nine describes an action at all — they describe a *state* (watchfulness, calm, a fixed high point, a turning point in a cycle). This is consistent with a team that had already tried, and moved past, describing the product by what it *does* (Cluster 1's investigative-act vocabulary) and shifted toward describing the product by what it *is like* — evocative and connotative rather than functional. Granite itself, the eventual winner, sits at the very edge of this cluster's own register (a physical, natural-world noun, evoking permanence) while breaking from every one of the nine actual Cluster 2 candidates in one specific way already argued in §1.2.4 and §A.2 above: it names a material property (something that resists change) rather than a position or state (something that has been reached or is being maintained) — which is this document's own account of why the era's underlying instinct was right but none of its own nine candidates were the correct execution of that instinct.

### G.3 Cluster 3, narrated — the plain-language/layman era

The twelve Cluster 3 names (Steady, Clarity, Sure, True, Keen, Solid, Whole, Actual, Proof, Level, Given, Behold) are, as a set, the starkest possible contrast with Cluster 1's specialized, faintly clinical vocabulary (autopsy, triage, recon) — every one of these twelve is a word a non-technical reader would recognize instantly, with no metaphor-decoding required at all. Read as the final era before Granite itself, this cluster's plausible internal logic is that the team had, by this point, tried a functional-vocabulary approach (Cluster 1) and an evocative-abstract approach (Cluster 2), and pivoted a third time toward testing pure readability and trust-signaling — words that would work identically well spoken aloud to an engineer, a supervisor, or a family member with no technical background, which is a real and legitimate naming criterion distinct from either of the first two clusters' own organizing principles. The specific failure mode this era ran into, argued at length in §1.2.4 and §A.2, is genericness — a risk inherent to choosing from the *most* common register of English vocabulary specifically because it is the most accessible, which creates an unavoidable tension between the era's own goal (maximum accessibility) and the stated design principle that ultimately decided the winner (a name that "won't need to change," which benefits from some degree of distinctiveness a maximally common word cannot supply).

### G.4 What this narrative adds, and what it still cannot claim

This three-era narrative is built entirely from close reading of the twenty-nine names' own vocabulary and register, cross-checked against the one directly dated artifact available (the `agent-autopsy` folder name) and the one directly stated design principle (`FYP_Registration_Form_Answers.md`'s "won't need to change even if scope shifts"). It does not, and cannot, claim to reconstruct an actual session-by-session record of when each cluster was generated, who proposed which names, or how long each era lasted — because, per §G.0, no such record exists in `AI_Usage_Log.md` or anywhere else in the source files. A panelist asking "walk me through the actual naming sessions" should be told plainly that the mechanics of the *final* rename (TraceCause → Granite, session seven) are fully documented, but the earlier process that produced the twenty-nine-candidate shortlist itself is not session-attributed anywhere in the project's own records — this narrative is the best-supported reconstruction available from the artifacts that do exist, offered and labeled as exactly that.

### G.5 The candidates, mapped

The following table restates the full rejected-candidate list from `FYP_Registration_Form_Answers.md` (§1.2.3) against the three interpretive clusters already developed in §1.2.4 and narrated above, as a single at-a-glance reference. The "Interpretation" column is this document's own analysis, consistent with, but going no further than, the reasoning already given in §1.2.4 — no row below claims a documented, individually-sourced rejection reason beyond what §1.2.4 and §1.2.5 already state exists.

| Candidate | Cluster | One-line interpretation |
|---|---|---|
| Causeway | 1 — forensic/causal | Evokes a route across an obstacle; closest in this cluster to a "bridging" metaphor rather than a diagnosis metaphor — arguably the odd one out even within Cluster 1 |
| Rootcast | 1 — forensic/causal | Portmanteau of "root cause" + "broadcast/forecast"; names the mechanism (root-cause identification), not the product |
| Autopsy | 1 — forensic/causal | Strong enough to become the literal folder name (`agent-autopsy`); names post-mortem diagnosis specifically, which stops fitting once repair/recovery join the core |
| Undertow | 1 — forensic/causal | The cluster's clearest metaphor match for *silent* failure specifically — a hidden current beneath a calm surface |
| Culprit | 1 — forensic/causal | Names exactly what the Culprit Agent foundational item does — rejected for the same reason as "Autopsy": describes one pipeline stage, not the whole product |
| Ripple | 2 — permanence/elemental | Evokes a light, spreading effect — arguably reads as insubstantial relative to the stated "permanence" design goal |
| Recon | 1 — forensic/causal | Reconnaissance — investigation before diagnosis; a process word, not a product name |
| Triage | 1 — forensic/causal | Names the confidence-scoring/prioritization function specifically; medically-derived, recognizable, but again names a stage not the product |
| Fathom | 1 — forensic/causal | To measure depth / to understand fully; the most abstract member of Cluster 1, bordering on Cluster 2's more evocative register |
| Vigil | 2 — permanence/elemental | Watchfulness — closer to an observability-platform name (matching what LangSmith/Langfuse already occupy) than a diagnosis-and-repair product name |
| Halcyon | 2 — permanence/elemental | Calm after a storm; evocative but abstract enough to require explanation on first hearing, unlike "Granite" |
| Meridian | 2 — permanence/elemental | A high, fixed reference line; already a heavily-used name across unrelated software categories (analytics, finance) |
| Zenith | 2 — permanence/elemental | The sharpest open question in the whole list (§A.2 above) — names a position, not a material property; the closest rival to "Granite" itself |
| Astra | 2 — permanence/elemental | Star/celestial-derived; evokes aspiration more than stability specifically |
| Solstice | 2 — permanence/elemental | A fixed point in a cycle; shares Halcyon's "requires explanation" weakness |
| Vantage | 2 — permanence/elemental | Names an elevated viewpoint; close cousin of Zenith, same "position not property" distinction applies |
| Zephyr | 2 — permanence/elemental | A gentle wind; the cluster's clearest instance of an evocative-but-insubstantial name, working against the permanence goal |
| Steady | 3 — plain/layman | Direct quality-word for reliability; short, but generic across the reliability-tooling category broadly |
| Clarity | 3 — plain/layman | Maps closely to the anti-silent-failure theme; heavily used commercially in security/analytics adjacent spaces |
| Sure | 3 — plain/layman | Extremely short and plain; risks reading as under-specific/unmemorable as a standalone brand |
| True | 3 — plain/layman | Same genericness risk as "Sure" and "Clarity" — a very common word across trust-signaling product names |
| Keen | 3 — plain/layman | Evokes sharpness/perceptiveness; the least directly on-theme member of Cluster 3 |
| Solid | 3 — plain/layman | Directly evokes reliability/permanence, overlapping conceptually with "Granite" itself but as an adjective rather than a concrete noun |
| Whole | 3 — plain/layman | Evokes completeness (no workflow left broken) — closest Cluster 3 word to the "recovery" half of the eventual title |
| Actual | 3 — plain/layman | Evokes ground-truth/correctness; unusual as a standalone brand noun |
| Proof | 3 — plain/layman | Maps almost exactly onto "Verified" in the eventual title; also arguably the most commercially crowded single word in the whole list (§A.2 above) |
| Level | 3 — plain/layman | Evokes stability/fairness; generic enough to risk being mistaken for an unrelated product category (finance, gaming) |
| Given | 3 — plain/layman | Evokes an established fact/premise; the most abstract, least brand-ready word in Cluster 3 |
| Behold | 3 — plain/layman | The cluster's outlier — an imperative, not a quality-word; closer to launch-copy flourish than a product name |

---

## H. What Would Change Each CCP Rating — the Remaining Eight Characteristics

Part 3, §3.1.3 already models this move for characteristic 1 explicitly: naming the specific empirical outcome that would justify a downgrade, not just the outcome that justifies the current rating. The same move is applied here to the remaining eight characteristics, using only mechanisms and evidence already committed elsewhere in the project — this section names no new evidence, only the conditions under which existing, planned evidence would cut the other way.

**Characteristic 2 (depth of analysis).** The rating would weaken if the full 3-stage-plus-memory ErrorProbe reproduction (owed since risk-register R1, §2.9.2) came in dramatically closer to 59.5% than Spike 1's simplified 12.5% step accuracy *using only well-understood, off-the-shelf techniques* — i.e., if closing the gap between the simplified and full reproduction turned out to require no new abstract modeling at all, only more careful application of already-published components. Conversely, if the gap closes only partially, or requires genuine new design choices to close (as the three abstract-modeling claims in §3.2.3 already argue it did for the pieces already built), the rating holds.

**Characteristic 3 (depth of knowledge).** The rating would weaken if a full, working reimplementation of ErrorProbe's three-stage architecture turned out to be achievable by closely following its methodology section with no ambiguous implementation decisions requiring independent judgment calls — i.e., if the paper's own description turned out to be unambiguous enough that "reproduction" reduced to transcription. Spike 1's own honest framing (§3.3.2) — an explicitly simplified version, with named omissions the team must be able to justify — is evidence against this outcome so far, but the full reproduction (still owed) is the real test.

**Characteristic 4 (familiarity of issues).** The rating would weaken specifically if a larger-scale natural-occurrence test (beyond Spike 4's n=3) found silent failures occurring frequently under ordinary task conditions, without deliberate fault injection — this would undercut the "infrequently-encountered" claim directly, on its own terms, rather than merely leaving it thinly evidenced. This is a genuinely open empirical question the current evidence base (n=3, zero natural occurrences) cannot yet answer either way with confidence, which is precisely why risk-register R10 keeps this open rather than closed.

**Characteristic 5 (beyond standard practice).** The rating would weaken if a future re-check (per the plan doc's own "standing instruction" to re-check the literature at each of the five gates, §1.5 of the main text) found that a commercial platform had shipped counterfactual fix-testing with a measured recovery rate, or general silent-failure detection, as a documented, standardized capability — exactly the two specific mechanisms the current claim is narrowly scoped around after the R9 correction (§3.5.2). This is the characteristic most likely to require re-verification before defense, given how recently (2026) the two nearest competing features (LangSmith Engine, Arize Alyx) shipped.

**Characteristic 6 (stakeholder involvement).** Already treated at length in §3.6 and §D.1 above — the condition that raises this rating is named precisely and is the single most actionable item in the entire document: real contact with representatives of the four named stakeholder groups, with their actual stated needs recorded and checked against the current client-framing assumptions (§1.6.1).

**Characteristic 7 (consequences).** The rating would weaken only if the underlying premise were shown false — if silent failures, once a larger evidence base exists, turned out not to produce genuinely undetected downstream harm in practice (for instance, if some other layer of a typical production system reliably catches them anyway, independent of Granite's own detection mechanism). No evidence currently on record suggests this; the structural argument (§3.7.2) that a silent failure is, by construction, invisible to standard error-handling would need to be shown not to hold in practice, which is a different and much stronger challenge than merely providing more real-world incident examples.

**Characteristic 8 (interdependence).** The rating would weaken if the committed core's own pipeline stages turned out, once built in full, to be more independently separable than the architecture sketch's six-hop data-flow narration (§1.7.5) currently claims — for instance, if Verified Repair Memory or Recovery Controller could be entirely omitted from a working system without affecting the other stages' correctness. Nothing in the current evidence base suggests this; the architecture sketch's own hop-by-hop narration is explicit that each stage's output is the next stage's required input, and Spike 6's cyclic-graph result (§3.8.3) is direct evidence the interdependence in the underlying subject matter is real and non-trivial, not merely asserted at the architecture-diagram level.

**Characteristic 9 (requirement identification).** The rating would weaken if a future, more mature version of the diagnosis pipeline reduced the three named unknowns (§3.9.2) to a small, enumerable set of candidate explanations reliably resolvable by lookup rather than by hypothesis-generation-and-verification — which would push the characteristic from "ill defined or unknown" toward the middle tier's "possible from a set of known options." Nothing in the current architecture points toward this outcome; the Strategist-then-Investigator structure (hypothesize, then evidence-test) is built specifically because the space of possible root causes is not currently reducible to a fixed, small, known set.

---

## I. A Second Pass Against the Guide Compliance Audit's Finer-Grained Sections

The Guide Compliance Audit (`Guide_Compliance_Audit.md`) is a deeper, sub-table-level pass beyond the plan doc's own section-level self-check, and Part 3's main text already draws on its §12 (POC risk categories, §3.5.2's seven-platform discussion) and its general framing. Three more of its sections carry findings directly relevant to Parts 1–3 that have not yet been surfaced above.

**§5's scope-sufficiency sub-table.** The audit's own finding here is precise and worth restating exactly: of six scope-sufficiency questions the guide asks a Stream A project to answer, five are cleanly answerable and one — "does each member have a defensible technical role" — is "technically undermined until the ownership assignment (R6) actually happens." This is the same open item already discussed in §1.10.1 and §E.2 above, but the audit's own framing adds a useful precision: the gap is not that the roles themselves are undefined (they are well-defined, per §1.9), it is that the guide's own question is phrased in terms of *members* having roles, which requires the assignment step specifically, not just the role-design step, to be complete. A panel asking this exact guide question should be answered with this precise distinction rather than a general "roles exist" response that doesn't actually address which half of the guide's question is satisfied.

**§6's "one-sentence vagueness test" gap.** The audit names a genuinely minor but real gap: the guide's own preferred compound-sentence format for a functional requirement (*"The system shall X for actor Y, and we will know it works when Z"*) is not used verbatim anywhere in the plan doc's own FR statements (§1.6.2) — the content is all present, split across the requirement statement and a separately-stated acceptance criterion, but not fused into the guide's exact single-sentence form. The audit itself supplies a corrected example for the hardest requirement: *"The system shall flag a silent failure for the operating engineer, and we will know it works when the flagged step matches the fault-injection harness's ground-truth injection point."* This is worth noting here specifically because it is the kind of gap that is trivial to close (a rewording, not new evidence) but easy to miss if a panel happens to check the guide's exact phrasing against the plan doc's own FR wording line by line — the audit already did that line-by-line check, and the gap it found is cosmetic, not substantive, which is itself useful context to have ready if raised.

**§9's eleven-step disciplined idea-discovery check.** The audit confirms every one of the guide's eleven idea-discovery steps has a corresponding artifact — literature review, gap verification, CCP formulation, contribution definition, technical-approach comparison, POC, evaluation definition, scope/ownership shaping, stress-testing via commercial comparison, SDG check. This is worth connecting explicitly to Part 2's own feature-list-evolution history (§2.6): the eleven-step process the audit confirms is not a one-time pass completed at proposal stage and then set aside — the nine AI-usage-log sessions traced through Part 2 show several of these same steps (gap verification, technical-approach comparison, stress-testing) being *repeated* later in the project's life, each time a new external source (the market survey) or a new POC result surfaced something the earlier pass had missed. The audit's own confirmation is accurate as a proposal-stage snapshot; Part 2's feature-list history is the evidence that the same disciplined process kept running afterward, not merely once.

**§15's eleven weak-idea-pattern spot-check.** The audit confirms Granite is clean across all eleven of the guide's named weak-idea patterns (routine CRUD portal, bare chatbot wrapper, model-training-with-no-baseline, local copy, blind reproduction, independent weak modules, industry-delivery-only, decorative SDG, difficulty-as-code-volume, notebook-only, dev-machine-only-deployment). This spot-check is worth reading alongside Part 1's own account of the wider "AgentTestLab" pitch that was deliberately narrowed (§1.4.3) — one of the specific risks that narrowing was explicitly designed to avoid was the "feature accumulation" hazard the plan doc names directly, which overlaps closely with several of the guide's own named weak patterns (difficulty-as-code-volume, independent weak modules). The audit's clean pass on this section is not incidental to the earlier scoping decision; it is a direct downstream consequence of it.

---

## J. Matrix — Every CCP Characteristic Traced to Its Specific Part 1/Part 2 Evidence Source

This closing table is a single-page-style index for defense prep: each characteristic, its rating, and the *specific* Part 1 or Part 2 fact that would need to be produced first if a panelist asked "show me," rather than the general evidence category already named in Part 3's own prose.

| # | Characteristic | Rating | The one fact to have ready first |
|---|---|---|---|
| 1 | Conflicting requirements | Clear | Extension #6 (two selectable diagnosis modes) as the concrete artifact proving tension 1 is real, not asserted |
| 2 | Depth of analysis | Clear | The 14.2% → 59.5% timeline across 15 months and six independent follow-ups (Paper Release Timeline) |
| 3 | Depth of knowledge | Clear | ErrorProbe's code is not public — reproduction is from methodology description alone (Full Literature Landscape Analysis §3) |
| 4 | Familiarity of issues | Clear | Spike 4's n=3, zero natural occurrences (AI Usage Log, fourth entry, Test generation) |
| 5 | Beyond standard practice | Clear | The R9 correction — LangSmith Engine / Arize Alyx named and accounted for, not omitted |
| 6 | Stakeholder involvement | **Weak (honest)** | Zero of four named stakeholder groups actually contacted (plan doc §16 checklist) |
| 7 | Consequences | Clear | The three tau-bench-retail-sourced scenarios (refund, budget, stock-count) |
| 8 | Interdependence | Clear | Spike 6's control-case 10,000-step cap when the revisit bound was disabled |
| 9 | Requirement identification | Clear | Recovery Controller committed with zero POC evidence, named explicitly as such (ninth AI-usage-log session) |

The single row worth memorizing above every other, if only one can be: row 6. It is the one place in the entire nine-characteristic argument where the "fact to have ready" is an admission rather than a demonstration — and, per §3.6.2's own reasoning, that is exactly what makes the other eight rows credible.

---

## K. Session by Session — What Each AI-Usage-Log Session Contributed Specifically to Parts 1–3

Part 2's main text already traces the nine sessions for the feature-list evolution specifically (§2.6). This section re-walks all nine sessions with a narrower, different lens: not "how did the foundational-item count change," but "what did this specific session contribute to the identity argument (Part 1), the research-gap-and-baseline argument (Part 2), or the CCP characteristic ratings (Part 3)" — pulling out material Part 2's own feature-count-focused pass does not dwell on. Sessions or session-portions with nothing distinct to add beyond what §2.6 already covers are noted briefly rather than padded.

**Session 1 (undated within the log itself, the founding session).** Contributes the entire opening evidentiary layer for Part 2: the choice of the agent-failure-attribution direction over two named alternatives (FinSynth, RedShield), explicitly checked "against each other and against the FAST guide's own CCP/scope criteria" — this is the direct source of Part 1's Stream A discussion insofar as it establishes the project *began* as a guide-criteria comparison exercise, not a single inspired idea adopted uncritically. The session's own literature-gap identification across all seven core papers, "cross-checked against each paper's own stated limitations section," is the direct evidentiary root of Part 2's entire per-paper treatment (§B above) — every "what its own limitations state" sub-heading in Section B traces back to this first session's own stated methodology (full-text reading, cross-checked against limitations sections specifically, not abstracts). This session also produced the first Spike 1 result (75% agent accuracy, 12.5% step accuracy after the scoring-bug fix) that anchors characteristic 2's entire "no obvious solution" argument (§3.2, §C.2 above) and the first documented correction — the GraphTracer/FALAT reversion — which is the founding instance of the propagation and honesty discipline Part 1's §1.2.6 and this addendum's §D.6 both depend on citing.

**Session 2 (2026-08-22, same day, later).** Contributes three items directly relevant to Parts 1–3: the AgentRx removal (a scope-discipline correction distinct from the GraphTracer/FALAT factual correction — this one is explicitly non-factual, a deliberate decision not to let a topically-adjacent finding expand scope without being asked, which is a second, structurally different kind of discipline instance worth distinguishing from the first when citing "the project corrects itself" as a pattern), the abandoned TracerTraj self-generation attempt in full (§2.5, §D.5 above), and the TracerTraj licensing correction itself (§2.4) — arguably this single session contributes more load-bearing material to Part 2's research-gap argument than any other session, since both the abandoned-attempt story and the licensing correction are cited repeatedly throughout Parts 2 and 3 as the project's clearest examples of primary-source verification discipline.

**Session 3 (2026-08-22, same day, later still).** Contributes the first frozen feature list (§2.6.2, already covered in Part 2's main text) and, less obviously, the SDG alignment addition (plan doc §0.05) — meaning Part 1's entire §1.5 SDG discussion traces to this specific session, not to the founding session. This session also contributes the first documented instance of a self-caught evidentiary gap (the counterfactual replay engine having zero POC evidence despite being a foundational item), which is the direct precedent the ninth session's own Recovery Controller gap (characteristic 9's own justification, §3.9.1, §3.9.3) implicitly follows — the pattern of "commit an item to the core, then discover during an alignment check that it lacks evidence, then log the gap honestly rather than quietly filling it before anyone notices" appears for the first time here, three sessions before it recurs for Recovery Controller.

**Session 4 (2026-08-23).** Contributes Spikes 5, 6, and 7 — already covered extensively in Parts 2 and 3 for their content (§3.2.3, §3.8.3, §F.1) — but the session's own framing is worth surfacing separately here: the log states this session exists specifically "to close gaps found in the previous session's alignment check," which is a second, independent instance (after session 3's own self-discovery) of the project treating its own audit findings as an actionable backlog rather than a passive record. This is the session where the project's own "find a gap, close it in the very next working session" pattern becomes a repeatable habit rather than a one-off event, which is directly relevant to how characteristic 9's zero-POC-evidence argument (§3.9.3) should be read — the pattern this session establishes is exactly what makes Recovery Controller's later, still-unclosed gap notable by contrast, rather than merely one more item on a list.

**Session 5 (2026-08-23).** Contributes the supervisor-driven rename (§1.3.5, §2.6.4) — the single clearest documented instance in the entire project of external pushback being received, accepted as valid rather than argued against, and answered with a structural fix (splitting one bundled mechanism into three independently-defensible ones) rather than a cosmetic one. This session is the direct evidentiary source for the entire "defended pushback" pattern §1.3.4 and §1.3.5 both build on, and it is worth noting explicitly that this session's own two considered-and-rejected items (Automatic Retry, Checkpointing) are the first appearance of "considered, not added, reasoning stated" as a recorded category distinct from either "done" or "rejected outright" — a three-way distinction (done / considered-and-rejected / not yet done) this whole addendum has tried to preserve throughout, and which originates here.

**Session 6 (2026-08-24).** The single most consequential session for Parts 1–3 jointly, already covered extensively above (§A.6, §B.2, §D.2, §D.4's chronology note) — contributes the market survey review in full, Repair Agent's addition and same-day POC, the Verified Repair Memory history finally being logged after a prior silent failure to log it (a distinct kind of gap from any other in the project: not a factual error, not a scope-discipline lapse, but a *tooling* failure — "the edit attempt failed silently and was never retried" — worth naming as its own fourth category of honestly-logged imperfection, alongside factual corrections, scope-discipline corrections, and evidentiary gaps), and the single-framework-advice rejection (R19, §1.3.4, §D.3, §C.1's second-round challenge). No other session in the log touches this many distinct threads across all three Parts simultaneously.

**Session 7 (2026-08-24).** Contributes the project title and short-name rename in full — already covered exhaustively in §1.1, §1.2, §A.1, §A.2, and §G above. Worth adding here only the one detail not yet surfaced elsewhere: the session's own closing line — "confirm the new title and short name read correctly in context, and that 'Granite' doesn't collide with anything, before citing either at defense or on the registration form" — is a distinct kind of open item from every other "not yet independently reviewed" caveat in the log, because it names a specific external risk (a name collision) rather than only an internal-verification risk. No source document records whether a trademark or name-collision check has actually been performed; this addendum flags that as a genuinely open, undocumented item rather than assuming it was quietly handled.

**Session 8 (2026-08-24).** Contributes the Framework Compatibility Layer addition (§1.9.2 extension 8, §1.3.4). The session's own framing — resolving "use features of all products, not only from one" positively rather than reopening the frozen foundational list or relitigating the already-rejected single-framework advice — is the third recorded instance of the "concede the underlying concern, answer it with a scoped positive mechanism rather than a bare refusal" pattern first seen in session five (the supervisor rename) and second seen in session six (R19). Three independent instances of the identical response pattern, across three different sessions and three different kinds of external input (a supervisor critique, a rejected piece of external advice, a scope question), is stronger evidence this is a genuine standing practice than any single instance would be on its own — worth citing as a set if a panel asks how the team generally handles pushback, rather than reaching for only one example.

**Session 9 (2026-08-24).** Contributes the Recovery Controller / Verified Repair Memory reclassification (§2.6.8, §3.9.1, §3.9.3, §D.2) and, distinctly, the discovery that the supervisor PDF generation script itself had been left in a stale intermediate state — a small but genuine instance of the propagation discipline catching not just a content gap but a *tooling* gap (a script that would have silently regenerated an inconsistent document had it been re-run without the fix). This is the session §D.6's closing paragraph above draws on for its own "test case" of the propagation discipline, and it is the most recent session on record, meaning it represents the project's own most current, and therefore most heavily-scrutinized, working state as of this document's own compilation date.

### K.1 What the full nine-session walkthrough shows, read as a set

Read end to end for what each session contributed specifically to identity, research-gap, and CCP argument-building (rather than to feature-count mechanics, which §2.6 already covers), a pattern emerges that is itself worth stating as a finding: every one of the nine sessions contributed at least one item that ended up load-bearing somewhere in Parts 1–3 as they now stand — there is no session in the log that turned out, in hindsight, to be pure noise or a dead end with no lasting trace in the current documentation. This is a different and stronger claim than "the project kept working steadily," because it means the log itself, read as a full historical record rather than mined selectively for convenient citations, supports the same throughline Part 3's own closing synthesis states (§3.10.3) — that the project's own understanding kept deepening across its full working history, not only at the two or three most dramatic, already-well-known moments (the TracerTraj correction, the market-survey session). A panel that reads the full log, not just the sessions this document happens to quote most often, should find the same disciplined pattern in the sessions quoted less — which is precisely the kind of consistency this addendum's own repeated emphasis on "traceable to a real source, not a favorable selection from it" is meant to support.

---

## Parts 4–5: Market Research and the Full Feature List

*Reading note: every item below follows the same skeleton — a short framing paragraph, then explicit **What / How / Why** sub-sections, each broken into sub-questions rather than left as one block of prose. Where a decision was reversed, contested, or produced a negative result, that is stated in its own labelled sub-point, not folded quietly into the surrounding text.*

---

# PART 4 — MARKET RESEARCH, TWO LAYERS

## 4.0 Why two separate market checks exist

### 4.0.1 What the two layers are

Granite's market research is split into two genuinely different layers, run at two different times, for two different reasons.

- **Layer 1 — observability/eval platforms.** LangSmith, Langfuse, Braintrust, Arize, Maxim AI, Opik, DeepEval. Researched first, on 2026-08-22.
- **Layer 2 — orchestration frameworks plus the academic anchor.** OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI, plus ErrorProbe. Researched on 2026-08-24, via a full read of `Agentic_AI_Market_Survey_BS_FYP.docx`.

These are not the same question asked twice. Layer 1 asks whether a tool that watches a multi-agent system *from outside* already solves Granite's two targeted gaps. Layer 2 asks whether the framework a team actually *builds its agents in* solves them natively. A platform in Layer 1 could in principle exist without any of the Layer 2 frameworks being touched at all — Langfuse, for instance, is framework-agnostic by design. Conversely, a framework in Layer 2 could ship its own built-in diagnosis tooling without ever appearing as a stand-alone commercial observability product. Treating them as one merged table would have hidden this distinction.

### 4.0.2 How each layer was checked

- **Layer 1 method:** direct research into each platform's current, documented feature set — vendor documentation, WebFetch of official product pages, WebSearch for feature confirmation — compiled into a single comparison table with five capability columns (trace capture, root-cause attribution, counterfactual/fix-testing, silent-failure detection, cross-framework generality).
- **Layer 2 method:** a full read of an external market survey document (`Agentic_AI_Market_Survey_BS_FYP.docx`), which itself did the framework-by-framework research; Granite's own contribution was auditing that survey's claims against Granite's own architecture and scope decisions, not re-deriving the framework research independently.
- **Both layers share one governing principle, stated explicitly in `Commercial_Product_Comparison.md`'s own framework-survey section:** "Two independent surveys (platform-side and framework-side) converging on the same absence is stronger evidence for the market gap than either alone."

### 4.0.3 Why neither layer could be skipped

- If only Layer 1 lacked automated attribution, a skeptic could argue the frameworks underneath might already handle it, and the observability layer simply doesn't need to duplicate that.
- If only Layer 2 lacked it, a skeptic could argue that's what the observability layer exists to add on top.
- Checking both, independently, and finding the identical gap in both closes that escape hatch: no first-class agent-and-step attribution, no first-class repair generation, no counterfactual fix-testing before applying a fix, in either layer.

### 4.0.4 Why the positioning had to be corrected mid-project, not asserted once

The original risk-register assumption feeding Layer 1 was comfortable and, it turned out, **stale**: "none of these platforms do algorithmic root-cause attribution, only human-driven trace inspection." Checking it directly (not re-asserting it) surfaced two 2026 features — LangSmith Engine and Arize's "Alyx"/Signal — that market themselves as doing exactly the thing the assumption said nobody did. `Commercial_Product_Comparison.md`'s own "Verdict, upfront" section states the corrected picture is deliberately more nuanced than either extreme: **not** "nobody automates this," and **not** "the market already does everything Granite claims." That correction, and the discipline of catching it before a panel could, recurs as a theme through every platform write-up below.

---

## 4.1 Layer 1 — the seven commercial observability platforms

### 4.1.1 LangSmith (core) and LangSmith Engine (Beta, 2026)

**What it is**

- LangSmith is LangChain's own commercial observability and evaluation platform — the most LangChain/LangGraph-native of the seven, built by the same company that owns the framework.
- Core LangSmith does trace capture: agent graphs, nested spans, tool calls, viewable in a web UI.
- **LangSmith Engine** is a 2026 beta feature layered on top — the specific product that forced the positioning correction described in §4.0.4. It markets itself as diagnosing root causes "against the live codebase" and drafting a fix as a pull request, in one automated pass.

**How it was checked**

- The comparison table in `Commercial_Product_Comparison.md` treats LangSmith core and LangSmith Engine as *separate rows*, because they make different claims.
- Core LangSmith's root-cause attribution column: "Human-driven — the developer inspects the trace."
- LangSmith Engine's root-cause attribution column: "Partial, real — 'diagnoses root causes against the live codebase' and drafts a fix as a pull request, in one automated pass. Mechanism for multi-agent *agent-level* attribution (as opposed to general code-level bug diagnosis) is not publicly documented."
- Every other column for LangSmith Engine — counterfactual/fix-testing, silent-failure detection — is marked "Not confirmed," meaning the check looked for public documentation and found none, not that absence was assumed.
- Cross-framework generality for LangSmith Engine: "Locked to LangSmith's own tracing/eval infrastructure" — built "on top of LangSmith's existing tracing and evaluation infrastructure," in the vendor's own words.

**Why it doesn't close Granite's two targeted gaps**

- *Granularity gap:* Granite's own FR2 requires "a predicted responsible agent, step, and confidence score." Nothing public confirms LangSmith Engine operates at that specificity, as opposed to general "fix a bug in this codebase."
- *Measurement gap:* nothing public confirms LangSmith Engine's diagnostic quality is measured against any labeled ground truth, the way Who&When/ErrorProbe or Granite's own benchmark is.
- *Lock-in gap:* LangSmith Engine only works if the system under test is already instrumented through LangSmith's own stack. Granite's committed core proves itself on CrewAI (Spike 2) — a framework LangSmith Engine's automated features are not demonstrated on, and that none of the nine academic papers surveyed used either.

### 4.1.2 Langfuse

**What it is**

- An open-source (MIT-licensed), self-hostable observability platform.
- Explicitly called out in `Commercial_Product_Comparison.md` as "the strongest on trace-capture generality" of the seven — framework-agnostic, self-hostable, no vendor lock-in the way LangSmith's automated features have.

**How it was checked**

- The check looked at Langfuse's own stated workflow for root-cause diagnosis and found a direct, quotable admission of the gap in the vendor's own materials: Langfuse's documentation describes leaving the developer "to determine which step was responsible, why, and how to repair the run."
- That is Langfuse's own description of its own product's boundary — not an inference drawn from silence.
- No counterfactual/fix-testing capability found. No silent-failure detection found.

**Why it doesn't close the gaps**

- Langfuse is the cleanest example in Layer 1 of a platform that is excellent at exactly what it claims to be excellent at (trace capture, framework-agnostic, self-hostable) and makes no claim at all to the thing Granite targets.
- Unlike LangSmith and Arize, there is no overclaim here to correct — Langfuse's own positioning is honest about the human-driven boundary.
- This is exactly why `Commercial_Product_Comparison.md`'s "practical implication for the product story" positions Granite as a layer that could sit *alongside or feed into* platforms like Langfuse, rather than compete with them head-on.

### 4.1.3 Braintrust

**What it is**

- A commercial observability/eval platform with a distinct workflow: full span tree per run, plus a distinguishing feature of converting a human-diagnosed failure into a permanent regression test case.

**How it was checked**

- Root-cause attribution recorded as "Human-driven — explicit manual workflow: open the failed run, inspect the span tree, add a 'root-cause label' by hand." Drawn directly from Braintrust's own description of its own workflow.
- Counterfactual/fix-testing: "No — turns failures into eval cases for future regression testing; does not test candidate fixes before applying."
- Silent-failure detection: no.

**Why it doesn't close the gaps**

- Braintrust's regression-test-conversion feature is worth naming specifically because it's easy to mistake for something adjacent to Granite's Verified Automatic Repair. They solve different problems.
- Braintrust's mechanism prevents a *previously seen* failure from silently recurring by adding it to a fixed regression suite a human already diagnosed — backward-looking.
- Granite's Verified Automatic Repair tests whether a *proposed fix* to a *newly diagnosed* failure actually works, before that fix is trusted, with a measured recovery rate — forward-looking.
- `Silent_Failure_Detection_and_Testing_Strategies.md`'s own honesty-check table makes the same point about human review generally: "Universal — Braintrust's own workflow is literally 'open the failed run, add a root-cause label by hand.'"

### 4.1.4 Arize Phoenix (core) and Arize "Alyx" / Signal (2026)

**What it is**

- Arize Phoenix is an open-source, OpenTelemetry-based observability platform — framework-agnostic by construction, since OpenTelemetry is a vendor-neutral tracing standard.
- "Alyx" (also called "Signal" in some materials) is Arize's own 2026 feature — the second reason the original "nobody automates this" assumption needed correcting.

**How it was checked**

- Arize Phoenix core, root-cause attribution: "Human-driven, LLM-assisted evals" — scores exist, a human still interprets them.
- Alyx's row is the most heavily qualified entry in the whole comparison table: "Marketing-stage, undocumented mechanism — 'uncovers root causes, generates review-ready fixes,' but no public documentation of scope, mechanism, or whether it operates at multi-agent step-level specificity."
- Every other column for Alyx — counterfactual/fix-testing, silent-failure detection, cross-framework generality — "Not confirmed."
- This is a deliberately more skeptical rating than LangSmith Engine's: LangSmith Engine at least publishes a described mechanism (diagnose against live codebase, draft a PR); Alyx's public materials describe outcomes without describing mechanism at all.

**Why it doesn't close the gaps**

- Same structural argument as LangSmith Engine: even taking the marketing claims at face value, nothing public confirms agent-and-step specificity, counterfactual testing before proposing a fix, or measured accuracy against a labeled benchmark.
- **The correction this platform forced is one of the clearest instances of the project's honesty discipline anywhere in the document.** Old framing (no longer accurate as stated): "None of these do algorithmic root-cause attribution — Granite would be the first." Corrected framing: "the market is *already moving* toward automated diagnosis... this should be stated honestly in the proposal, not hidden, since a panel that's seen either product would otherwise catch the gap."

### 4.1.5 Maxim AI

**What it is**

- Added to the comparison on 2026-08-22, a fourth platform beyond the original core four.
- Does full request-lifecycle trace-graph capture, plus a specific, narrower automated-diagnosis-adjacent feature: "attribution tracking," flagging outputs untraceable to a source document or tool call — i.e., "ungrounded claims."

**How it was checked**

- Maxim's own marketing language uses a human verb, not a machine one: "root cause debugging" re-runs simulations from any step to *reproduce* an issue (not to *diagnose* it automatically); the vendor's own copy says teams "use [Maxim] to identify failure modes and diagnose root causes" — the team identifies and diagnoses; Maxim provides tooling.
- Recorded as "Human-assisted, well-tooled" — a distinct category from LangSmith Engine's "Partial, real" and Alyx's "Marketing-stage, undocumented mechanism."
- The one genuinely partial automated capability found — "attribution tracking" — is narrower than it first appears: it's scoped specifically to **RAG-groundedness checking**, not general task-constraint verification. Table verdict: "Partial, narrower... this is RAG-groundedness checking specifically, not general task-constraint verification."
- **This is the precedent check that directly produced a design decision downstream.** Granite's own Semantic Error Diagnostic (foundational item #7, §5.2.7 below) is explicitly scoped to be general, not RAG-specific — a framing this precedent check produced, not one assumed in advance.

**Why it doesn't close the gaps**

- Simulation reproduction is useful for confirming a failure occurred, but the comparison table's verdict on counterfactual/fix-testing is explicit: "Not found — simulation re-run reproduces an issue, not confirmed to test a *corrected* step for recovery."
- Cross-framework generality: "Instruments whichever framework a customer uses; no publicized claim of tested generalization to a framework outside its own customer base" — a softer version of the same lock-in pattern seen in LangSmith Engine and Alyx, without the explicit vendor-infrastructure coupling those two have.

### 4.1.6 Opik (Comet) and DeepEval / Confident AI

**What they are**

- Two platforms added in the third research session (2026-08-22, later that day), researched more lightly than the first five.
- Opik checked via direct WebFetch of `comet.com/site/products/opik/`. DeepEval checked via WebSearch.

**How they were checked, and why the confidence is lower than the other five**

- Most columns for both are marked "Unconfirmed" in the comparison table.
- Cross-framework-generality column notes: "one-line vendor descriptions ('logging + evaluations,' 'evaluation infrastructure') suggest an eval-framework role closer to Braintrust/Arize than to LangSmith Engine/Alyx, but this is not verified."
- Opik's WebFetch surfaced trace/debug tooling, LLM-as-judge evaluation, an AI fix-drafting assistant called "Ollie," and production monitoring — recorded as informal notes from a single fetch, not the same table-by-table depth the first five platforms received.
- DeepEval's WebSearch surfaced a directly relevant, already-favorable third-party finding: search results explicitly noted DeepEval as having "limitations in root-cause diagnostics for multi-agent failure scenarios" — a characterization found in a general web search, not asserted by the project itself.
- `AI_Usage_Log.md`'s third session records the honesty about this research directly: "Not yet independently spot-checked by the team — same standing instruction as the original 4-platform comparison."

**Why they don't close the gaps**

- DeepEval is explicitly assertion-based. `Silent_Failure_Detection_and_Testing_Strategies.md`'s own honesty-check table states "DeepEval's entire product is assertion-based testing exactly like this" (for domain-specific rule checks) and "DeepEval's whole positioning; LLM-as-judge is used everywhere" (for automated evaluations) and again for regression tracking.
- DeepEval is real, useful, standard-practice tooling — precisely the kind of common building block the silent-failure module should be built *with*, not against — but its own documented limitation in multi-agent root-cause diagnosis is exactly the gap Granite targets.
- Opik's "Ollie" is the closest thing in Layer 1 to Granite's own Repair Agent concept, but nothing in the lighter research pass confirms it does agent/step-level attribution first, or verifies a fix via counterfactual replay before proposing it. This remains an open spot-check item, not a confirmed precedent.

### 4.1.7 What none of the seven confirm, publicly, taken together

`Commercial_Product_Comparison.md` states this as a five-item list. Each maps to a specific Granite functional requirement (§0.07 of the plan doc):

1. **Multi-agent agent-*and*-step-level attribution as a documented, specific mechanism** — maps to FR2. LangSmith Engine and Alyx both gesture at automated diagnosis; neither publishes whether it's agent/step-specific versus general code-level diagnosis.
2. **Counterfactual replay of a candidate fix** — testing whether a proposed correction would actually have worked, with a measured recovery rate, before it's proposed or applied. Maps to FR4 and Verified Automatic Repair. No platform checked confirms this.
3. **Detection of silent, signal-free failures specifically.** Maps to FR3 and Semantic Error Diagnostic. Maxim's RAG-groundedness check is the closest partial precedent, and it's explicitly narrower.
4. **Genuine cross-framework generality, evaluated.** Maps to FR5 and RQ2. Every automated-diagnosis feature found is built on and locked to its own vendor's tracing infrastructure.
5. **A rigorous, ground-truth-labeled evaluation of their own diagnostic accuracy.** None of the seven publish anything resembling Who&When/ErrorProbe-style benchmarking. Their diagnosis quality is asserted, not measured. This is arguably the sharpest, most durable differentiator — a vendor could ship agent-level attribution tomorrow and still avoid publishing a rigorous benchmarked accuracy number, since a low measured number is bad marketing.

### 4.1.8 The positioning correction, narrated as a real event

- **Before:** risk register R9 recorded the assumption as settled — an established commercial market exists for agent observability, none of it does algorithmic root-cause attribution.
- **The check:** run directly on 2026-08-22, not re-asserted.
- **What it found:** two platforms had, within the same year, shipped features marketing themselves as doing exactly the thing the assumption said nobody did. R9's own status line: "Resolved 2026-08-22 ... Correction to the original assumption: LangSmith Engine and Arize's 'Alyx'/Signal (both 2026) *do* claim automated root-cause diagnosis + fix generation — the 'nobody automates this' framing was stale and has been corrected, not just filled in."
- **The corrected positioning rests on four points, each established above:**
  - Framework-agnostic by design and evaluation — proven directly on CrewAI (Spike 2), a framework none of the seven platforms' automated features are demonstrated on.
  - Silent-failure detection as an explicit, benchmarked capability, not marketing copy.
  - Counterfactual replay as a quantified mechanism reporting a measured recovery rate, not just "here's a suggested fix."
  - A published, ground-truth-labeled benchmark, which none of the seven platforms have.
- **The recommended rhetorical stance:** position Granite as a diagnosis layer that could sit *alongside or feed into* platforms like Langfuse/Phoenix — which already do excellent trace capture and would benefit from an add-on doing what none of them measure — rather than as a head-to-head competitor to LangSmith Engine or Arize Alyx "on their own commercial home turf." Stated reason: "a research-grade evaluation is not the same battle as a production-support-team's roadmap velocity, and claiming otherwise would be the over-claiming the guide explicitly warns against."

### 4.1.9 Seven worked scenarios — what a team relying on only one platform would miss

*A framing note before these seven: every "what Granite does" line below is grounded in a foundational item with real POC evidence already established in §5.2, cited by name and spike number. Every "what [platform] does/can't do" line is grounded in the platform-by-platform findings already established in §4.1.1–4.1.6. The scenarios themselves — the specific numbers, SKUs, and dialogue — are illustrative composites built to make the already-sourced gap concrete and readable, in the same plain style used elsewhere in this document (see the retail-support example earlier in the file), not a claim that this exact incident occurred during Granite's own testing. Where a scenario states what a real platform would show, it states it only because that platform's own documented feature set, established above with a citation, entails that outcome.*

**Scenario A — LangSmith (core), a support bot built on CrewAI, not LangChain.**

*The setup.* A three-agent CrewAI support crew — Intake, Refund Calculator, Responder — is instrumented with LangSmith for trace visibility, since LangSmith accepts OpenTelemetry-style traces from non-LangChain frameworks even though its automated diagnosis feature does not. Refund Calculator silently applies a stale discount rate to a $200 order, producing $180 instead of the correct $170.

*What goes wrong.* The trace in LangSmith's UI shows three clean spans, no exceptions, no low-confidence flags — LangSmith core's own root-cause attribution is "human-driven, the developer inspects the trace" (§4.1.1). A support engineer opens the trace, sees nothing obviously wrong, and closes the ticket as "model was slightly off, not a bug."

*Why this matters.* LangSmith Engine, the automated-diagnosis feature, is "locked to LangSmith's own tracing/eval infrastructure" (§4.1.1) — and even where it does apply, nothing public confirms it operates at agent-and-step specificity as opposed to general code-level bug diagnosis. A CrewAI-native failure like this one sits outside what LangSmith Engine is demonstrated on at all.

*What Granite does about it, step by step.* (1) Semantic Error Diagnostic recomputes the expected discount from the trace's own upstream order/discount-rate data and flags the $10 mismatch as a constraint violation, the same rule-based mechanism validated in Spike 4's near-miss test (§5.2.7). (2) Culprit Agent and Error Step Localization run backward causal tracing over the CrewAI execution graph — the same graph structure proven to trace cleanly in Spike 2's toy 3-agent CrewAI run (§5.2.1) — and localize the failure to Refund Calculator's discount-application step specifically, not just "somewhere in the crew." (3) Verification Agent checks that hypothesis against the real tool-call evidence in the trajectory before it is reported as a diagnosis, rather than accepted on the hypothesis-generation step's own confidence alone.

**Scenario B — Langfuse, an engineer told exactly where the boundary is and left there.**

*The setup.* A team self-hosts Langfuse in front of a LangGraph-based research-and-drafting pipeline. A "verify claim against source" step is skipped due to a tool-call timeout that gets silently retried and swallowed, and the final drafted answer states a fact with no supporting citation anywhere upstream.

*What goes wrong.* Langfuse's own documentation is explicit about what happens next: it "leaves the developer to determine which step was responsible, why, and how to repair the run" (§4.1.2) — an honest, stated boundary, not an overclaim. The engineer has excellent trace visibility (Langfuse is "the strongest on trace-capture generality" of the seven checked, §4.1.2) but still has to manually read the whole trace to notice the unsupported claim, because Langfuse never claims to check constraint provenance for them.

*Why this matters.* This is the cleanest possible illustration that trace capture and semantic diagnosis are genuinely different capabilities — Langfuse is excellent at the first and makes no claim to the second, so nothing here is "wrong" with the product, only with treating trace capture as if it were diagnosis.

*What Granite does about it, step by step.* (1) Constraint Provenance Tracing (one of the two new complementary strategies under Semantic Error Diagnostic, §5.2.7) walks the execution graph backward from the claimed fact and finds no verifying node behind it — the same graph-based provenance-walk mechanism described in Scenario 3 of §5.7.3. (2) Because this specific strategy is a design proposal, not yet POC-tested (stated honestly in §5.7.3 and §5.2.7), the honest claim here is narrower than Scenario A's: Granite's architecture is built to catch this class of failure, and the mechanism to do so is designed and scoped, but its detection rate on real traces has not yet been measured — a gap the document does not paper over.

**Scenario C — Braintrust, a repeat failure that keeps happening because nobody proposed a fix.**

*The setup.* A finance-assistant multi-agent system on LangGraph keeps mis-parsing a specific vendor invoice format about once every 40 runs. A human notices it, opens the failed run in Braintrust, inspects the span tree, and manually adds a "root-cause label" — Braintrust's own explicit, documented workflow (§4.1.3).

*What goes wrong.* Braintrust converts that labeled failure into a permanent regression-test case, so the exact same input will now be caught if it recurs verbatim. But the underlying parsing logic itself was never corrected — the regression suite catches the *symptom* recurring, not the *cause* being fixed. The 41st run with a slightly different but structurally identical invoice still fails the same way, because nothing was repaired, only flagged for future detection.

*Why this matters.* This is exactly the distinction named in §4.1.3: Braintrust's mechanism is backward-looking (stop a previously-seen failure from silently recurring) where Granite's Verified Automatic Repair is forward-looking (test whether a proposed correction to a newly diagnosed failure actually works). They are not competing solutions to the same problem — Braintrust prevents silent regression of a known case; nothing in the platform proposes or verifies a fix for the underlying logic.

*What Granite does about it, step by step.* (1) Repair Agent generates a targeted correction to the parsing logic — the actual mechanism Spike 8 tested and found working on 4 of 6 synthetic cases (§5.2.6). (2) Verified Automatic Repair deterministically re-executes the downstream portion of the trace with that correction applied and reports whether the corrected trace now recovers, the mechanism proven in Spike 5 (`recovery_success: true`, §5.2.8) — testing the fix, not just remembering that a failure once happened. (3) If Verified Repair Memory's owed re-test (§5.2.10) succeeds on a stronger backbone, the verified fix itself, not just a symptom label, becomes retrievable for the next structurally similar invoice.

**Scenario D — Arize Phoenix / "Alyx", a claim nobody can check.**

*The setup.* A retail recommendation crew running on a custom orchestration layer is instrumented with Arize Phoenix (OpenTelemetry-based, so framework-agnostic trace capture works cleanly). The team also hears about Arize's 2026 "Alyx" feature, which markets itself as uncovering root causes and generating review-ready fixes.

*What goes wrong.* The team cannot actually evaluate whether Alyx would have caught their specific failure (a recommendation engine silently ignoring a stated allergy constraint) because Alyx's public materials describe outcomes without describing mechanism — §4.1.4 records this as "the most heavily qualified entry in the whole comparison table," with every column beyond the marketing-stage claim itself marked "Not confirmed." A team cannot budget engineering time against a capability whose scope, mechanism, and accuracy are all undocumented.

*Why this matters.* This is the platform where the project's own positioning correction (§4.0.4) was forced — old framing ("nobody automates this") had to be corrected once Alyx's marketing claims were found, but the corrected framing is deliberately narrower than either extreme: not "nobody automates this," and not "the market already does everything Granite claims."

*What Granite does about it, step by step.* (1) Semantic Error Diagnostic's domain-specific rule checks (§5.2.7) treat "must not violate a stated allergy constraint" as exactly the kind of boundary check the rule-based checker is built for — the same category of mechanism validated against known-wrong values with zero false positives in Spike 4. (2) Every mechanism behind this diagnosis is published with its own accuracy number in this document (75% agent accuracy / 12.5% step accuracy from Spike 1, 0.667 repair success rate from Spike 8, and so on) — the sharpest structural difference from Alyx's undocumented mechanism, and the specific point item 5 of §4.1.7 names as "arguably the sharpest, most durable differentiator."

**Scenario E — Maxim AI, a groundedness check that doesn't generalize past RAG.**

*The setup.* A logistics-scheduling multi-agent system (not RAG-based — it reasons over live warehouse-inventory tool calls, not retrieved documents) is instrumented with Maxim AI for its attribution-tracking feature.

*What goes wrong.* Maxim's attribution tracking flags outputs "untraceable to a source document or tool call" (§4.1.5) — but the comparison table's own verdict is explicit that this is "RAG-groundedness checking specifically, not general task-constraint verification." A scheduling failure where the agent correctly cites the tool call it used, but misapplies the returned quantity in a downstream arithmetic step, produces an output that *is* traceable to a real tool call — so Maxim's groundedness check has nothing to flag, even though the final schedule is wrong.

*Why this matters.* This is precisely the precedent that shaped a Granite design decision, not just a market-gap finding: §4.1.5 states directly that Maxim's narrower RAG-specific scoping is "the framing this precedent check produced" for keeping Semantic Error Diagnostic deliberately general rather than RAG-specific.

*What Granite does about it, step by step.* (1) Because Semantic Error Diagnostic is scoped as general task-constraint verification, not groundedness-to-a-document, the same rule-based checker (execution-state tracking, §5.2.7) catches a mis-applied quantity by comparing the trace's own logged tool-call output against what the downstream step actually used — a case exactly outside Maxim's own stated groundedness scope. (2) Error Step Localization then pins the failure to the specific arithmetic step, not merely to "something after the tool call."

**Scenario F — Opik, a fix-drafting assistant with no verification-before-trust step named.**

*The setup.* A content-moderation multi-agent pipeline uses Opik's tracing, LLM-as-judge evaluation, and "Ollie" fix-drafting assistant, surfaced via the lighter WebFetch-based research pass (§4.1.6).

*What goes wrong.* Ollie is, per §4.1.6, "the closest thing in Layer 1 to Granite's own Repair Agent concept" — but nothing in the research confirms it does agent/step-level attribution *first*, or verifies a candidate fix via counterfactual replay *before* proposing it, rather than simply drafting a plausible-looking correction. A team applying an Ollie-drafted fix has no measured recovery-rate number telling them how often such fixes actually work once applied.

*Why this matters.* §4.1.6 states this remains "an open spot-check item, not a confirmed precedent" — the honest state of the evidence is that Opik might already be close to solving part of this, and the team does not yet know, because the research pass here was lighter than the first five platforms received.

*What Granite does about it, step by step.* (1) Repair Agent generates the candidate fix (Spike 8, 0.667 repair success rate). (2) Verified Automatic Repair re-executes the downstream trace with that candidate and reports a measured recovery outcome (Spike 5, `recovery_success: true`) *before* the fix is reported as trustworthy — the explicit "verify before trust" ordering that is exactly item #2 on the list of five things none of the seven Layer-1 platforms confirm doing (§4.1.7).

**Scenario G — DeepEval, assertion-based testing that catches what it was told to check for.**

*The setup.* An HR-onboarding multi-agent system ships with a DeepEval test suite asserting a fixed set of known compliance rules (e.g., "must not recommend a benefits tier the employee isn't eligible for").

*What goes wrong.* DeepEval's own documented limitation, found via WebSearch and recorded without softening in §4.1.6, is "limitations in root-cause diagnostics for multi-agent failure scenarios." The suite correctly catches the specific rule it was written to check, but a genuinely novel failure mode — one agent silently overriding another agent's eligibility determination two steps upstream — produces no assertion failure at all, because nobody wrote an assertion for that specific interaction pattern in advance.

*Why this matters.* `Silent_Failure_Detection_and_Testing_Strategies.md`'s own honesty-check table states plainly, and this document repeats it in §4.1.6: "DeepEval's entire product is assertion-based testing exactly like this" — real, useful, standard-practice tooling, but structurally bounded by whatever assertions were written in advance, not able to localize an unanticipated interaction failure back to its origin.

*What Granite does about it, step by step.* (1) Culprit Agent and Error Step Localization don't require a pre-written assertion for the specific failure pattern — backward causal tracing over the execution graph (BFS from the failure node, §5.2.4) finds the responsible agent and step generically, for a failure class nobody anticipated in advance. (2) DeepEval-style assertion tests remain a valuable, complementary layer Granite's own Semantic Error Diagnostic is explicitly built to sit alongside, not replace — consistent with the honesty-check table's stated conclusion that these common building blocks are not themselves the differentiator (§4.1.6, §5.2.7).

---

## 4.2 Layer 2 — the seven orchestration frameworks and ErrorProbe

Checked two days after Layer 1, on 2026-08-24, via a full read of `Agentic_AI_Market_Survey_BS_FYP.docx`. This is not a paper Granite tries to beat, nor a product compared for the guide's §10 requirement — it's an independent market/technology survey that happened to converge on much of Granite's own architecture. `Agentic_AI_Market_Survey_Full_Content_and_Integration.md`'s closing section states the calibrated read directly: "genuinely — but precisely, not broadly... a second source converging on it independently... What it does not do is validate a pivot to its own recommended framing... or its single-framework scope-narrowing advice — both were considered and explicitly not adopted."

Each write-up below follows the survey's own §3.1–§3.8 structure, quoting the survey's own wording where it's the load-bearing evidence, expanded with the specific reasoning for why each framework fails to close Granite's two targeted gaps.

### 4.2.1 OpenAI Agents SDK (§3.1)

**What it is**

- Handoffs between agents, tool integration, sessions, guardrails, tracing/evaluation-oriented instrumentation.
- Tracing model captures agent turns, model generations, tool calls, handoffs, guardrail checks.
- Tool guardrails validate calls before and after execution.

**How it was checked**

- Via the survey's own written assessment, reproduced verbatim: "For this FYP, these features should be treated as infrastructure rather than novelty. The SDK does not natively perform causal attribution to identify the earlier agent/step that introduced a semantic failure, nor does it automatically repair and replay that component."
- Table 1's feature matrix confirms this precisely for this framework's column: "Find culprit agent" = Not native, "Find originating error step" = Not native, "Causal backward error tracing" = Not native, "Automatically generate repair" = Not native — the only framework of the seven rated flatly "Not native" (rather than "Custom" or "Experimental") on the repair-generation row.

**Why it doesn't close the gap**

- Guardrails validate calls against a schema or rule at the point of execution — useful, standard-practice infrastructure Semantic Error Diagnostic could plausibly sit alongside — but it is not backward causal tracing to find which *earlier* agent or step is responsible for a delayed, silent failure.
- Sessions and tracing capture what happened; nothing in the SDK reconstructs *why* a downstream symptom traces back to an upstream cause.

### 4.2.2 LangGraph (§3.2)

**What it is**

- The framework the survey itself explicitly recommends as the FYP's implementation substrate.
- Reason given: "durable state, checkpointing, fault tolerance, retry policies, persistence and time-travel/replay."

**How it was checked**

- The survey's own sentence is the sharpest single statement of the layered-gap argument in the whole document: "LangGraph can tell the system where execution failed, but causal semantic attribution to an earlier agent remains a separate research problem."
- Table 1 confirms LangGraph is rated "Strong" on checkpoint/resume and workflow replay/fork — the best of the seven on operational recovery infrastructure — while still "Not native" on culprit agent, error step, and causal tracing, and "Custom" on repair generation, verification, and memory.

**Why it doesn't close the gap, and why it's a committed core architecture anyway**

- No tension: LangGraph's strength (checkpointing, time-travel/replay, retry policies) is exactly the operational substrate Recovery Controller (foundational item #9) and Verified Automatic Repair (foundational item #8) build on, rather than reinvent.
- LangGraph telling the system *where* execution failed is a useful, reusable signal; it is not the same as Culprit Agent and Error Step Localization determining *which agent's earlier reasoning* caused the failure to manifest downstream.
- LangGraph's native support for cyclic workflows (retry loops, iterative refinement) is the direct justification for extension #3 (cyclic/dynamic graph support, §5.3.3) — without it, Granite's own cross-architecture claim would be incomplete on the very framework it commits to instrumenting.

### 4.2.3 CrewAI (§3.3)

**What it is**

- Multi-agent orchestration with tracing/observability and checkpoint-oriented execution.
- Recovery mechanisms can save state and resume a workflow rather than repeating all completed work — "covers a large portion of operational fault tolerance," per the survey.

**How it was checked**

- The survey's own line draws the boundary precisely: "identifying the semantic root cause of a seemingly valid but wrong multi-agent trajectory and automatically repairing the responsible step remains custom logic."
- Table 1 rates CrewAI "Strong" on checkpoint/resume and workflow replay/fork, same tier as LangGraph, while flat "Not native" on all four Core-attribution rows.

**Why it doesn't close the gap**

- Same structural argument as LangGraph — good operational recovery, no semantic diagnosis.
- CrewAI is the framework Spike 2's POC evidence is built on (toy 3-agent workflow, traced cleanly into 3 nodes / 2 correctly-ordered edges).
- Explicitly the framework chosen because, per the plan doc's own research-to-decision table, "no paper tests generalization to a multi-agent architecture absent from its own benchmark construction" — CrewAI being unused by any of the nine surveyed papers makes it a genuine test of the generalization claim.

### 4.2.4 Google Agent Development Kit (ADK) (§3.4)

**What it is**

- Agent orchestration with plugins, callbacks, evaluation tooling, retry-related mechanisms.
- Evaluation tooling can assess final answers and trajectories/tool-use sequences.

**How it was checked**

- The survey draws a more careful distinction here than a blanket dismissal: "This reduces the novelty of simply adding an 'agent evaluator.' The proposed FYP should instead use evaluation as a verification signal and focus on causal localization plus targeted repair."
- Table 1 rates ADK's "Detect semantic wrong answer" row as "Evaluation support" — one tier above the flat "Not native"/"Partial/custom" most other frameworks get on this row — but still "Not native" on culprit agent, error step, and causal tracing.

**Why it doesn't close the gap**

- ADK's evaluation infrastructure is genuinely closer to Granite's Verification Agent concept than most of the other six frameworks get.
- But "adjacent" is the operative word: ADK's evaluator assesses whether an answer or trajectory looks right in isolation; it does not localize *which prior agent step* is causally responsible when it doesn't, and does not generate or verify a targeted repair.
- This is exactly why the survey advises using ADK's evaluation as a *signal feeding into* causal localization and repair — advice Granite's own architecture already follows, since Verification Agent is explicitly the evidence-grounded confirmation *stage*, not the final output.

### 4.2.5 Microsoft Agent Framework (§3.5)

**What it is**

- Graph-based multi-agent workflows with checkpointing, state management, human-in-the-loop mechanisms, middleware, telemetry.
- Described by the survey as "strong foundations for recovery and production engineering."

**How it was checked**

- The survey's own sentence: "The remaining gap is not basic recovery from an exception, but determining the semantic origin of a delayed failure and transforming that diagnosis into an automatically verified correction."
- Table 1 rates it "Strong" on checkpoint/resume, same tier as LangGraph and CrewAI, flat "Not native" on the four Core-attribution rows.

**Why it doesn't close the gap**

- Human-in-the-loop mechanisms let a human intervene mid-workflow — a meaningful operational feature — but a human intervention point is not the same as an automated diagnosis of *which* earlier step needs intervention, nor a verified, tested repair.
- This is the third framework in a row (after LangGraph, CrewAI) whose strength is specifically "recovery from a known interruption point," and whose gap is specifically "diagnosing an unknown, delayed, silent failure" — a pattern consistent enough across three frameworks that it becomes evidence for Table 2's five-layer framing (§4.3.2): layers 1–2 are consistently "mostly mature," while layer 3 is consistently absent.

### 4.2.6 Amazon Bedrock AgentCore (§3.6)

**What it is**

- "Strongest at enterprise runtime, observability and evaluation. It provides logs, traces, metrics and production monitoring for agent workloads," per the survey's own assessment.

**How it was checked**

- The survey's boundary sentence: "observability alone does not solve semantic causal attribution. A workflow may complete successfully at the infrastructure level while still returning a semantically wrong result."
- This sentence is, in effect, the definition of a silent failure restated from the infrastructure-observability side.
- Table 1 rates AgentCore "Strong" on execution tracing and runtime-error detection, "Partial" on resume from repaired point, "Not native" on the four Core-attribution rows.

**Why it doesn't close the gap**

- AgentCore is arguably the single strongest example of why infrastructure-level observability and semantic-level diagnosis are genuinely different problems, not points on a continuum a vendor could naturally slide along by adding more monitoring dashboards.
- Its own vendor framing (production monitoring, enterprise runtime) is oriented around uptime and infrastructure health — categories a silent failure by definition does not disturb.

### 4.2.7 BabyAGI (§3.7)

**What it is**

- The odd one out among the seven — a research/hobbyist project, not a production-oriented enterprise SDK.
- Function-centric architecture exploring "experimental self-building capabilities": in principle, the system can create or revise its own capabilities rather than only report an error.

**How it was checked**

- The survey's assessment is explicit that this is inspirational, not a candidate architecture or comparison baseline: "BabyAGI does not provide the same systematic, benchmarked culprit-agent and originating-step diagnosis studied by ERRORPROBE. For an FYP, its self-modification idea is more useful as inspiration for the Repair Agent than as a direct baseline for semantic attribution."
- Table 1's ratings for BabyAGI are consistently the weakest of the seven — "Partial" orchestration, "Limited" guardrails and agent evaluation, "Not native" workflow replay/fork — with "Experimental self-building" as its one distinguishing rating, the only framework of the seven rated above flat "Not native"/"Custom" on repair generation.

**Why it matters despite not closing the gap**

- BabyAGI is the one framework in Layer 2 not cited as "doesn't do X" — it's cited as conceptual precedent for Repair Agent's self-correction idea, while explicitly disclaimed as not a rigorous, benchmarked comparison point.
- This matches the plan doc's own §4.1 defense against "you just combined existing techniques": naming where an idea's inspiration came from honestly, rather than hiding the influence or overclaiming it as a beaten baseline.

### 4.2.8 ErrorProbe (ACL Findings 2026) (§3.8)

**What it is**

- Not a commercial platform or an orchestration framework — the peer-reviewed academic method Granite's own attribution algorithm is built on.
- Included in Layer 2's write-up sequence because the survey itself treats it as the eighth entry in its comparative survey section.

**How it was checked**

- Survey's own description, reproduced verbatim: "A research framework for semantic failure attribution in multi-agent systems. It takes a failed trace, uses structural decomposition and symptom-driven backward tracing, and employs a Strategist-Investigator-Arbiter team to identify the responsible agent and decisive error step. It also stores verified diagnostic patterns."

**Why it's the one item in Layer 2 that partially *does* solve half the problem, and exactly where it stops**

- ErrorProbe is not checked for whether it fails the gap — it's the strongest published method that gets closest to closing half of it.
- Its own sentence: "Its main contribution is therefore diagnosis rather than closed-loop operational recovery: the framework improves the debugger, but it does not demonstrate a complete system that automatically repairs the responsible component, replays the workflow from a corrected state and retains verified repairs as executable recovery knowledge."
- This is the exact sentence that motivates the survey's own recommended four new modules (§4.4).
- Granite's own architecture had already independently arrived at reproducing ErrorProbe's three-stage pipeline (Culprit Agent, Error Step Localization, Verification Agent map onto Strategist, Strategist, Investigator respectively) *before* this survey was read — exactly the "independent convergence, not new information" point the integration audit makes.

### 4.2.9 Worked example — the same diagnosis logic on a CrewAI trace and a LangGraph trace, side by side

*This is the concrete illustration of what Framework Compatibility Layer (extension #8, §5.3.8) actually means in practice — not just "instruments seven frameworks" as an abstract claim, but the same underlying diagnosis pipeline applied to two structurally different traces from two different frameworks that represent the two committed-core architectures. The CrewAI half below is grounded directly in Spike 2's real output; the LangGraph half is grounded directly in Spike 6's real output. Nothing about the numbers below is invented — both are the actual recorded results of the two spikes named.*

**The CrewAI trace (Spike 2, `poc_spike2_crewai_toy.py`).**

- A toy 3-agent CrewAI workflow, traced cleanly into 3 nodes and 2 correctly-ordered edges (§5.2.1).
- CrewAI's own message-passing model is task-handoff-based: each agent completes a task and passes its output forward to the next agent in the crew, a linear or lightly-branching structure for this toy case.
- The execution-graph construction step reads CrewAI's own trace format (task assignments, tool calls, agent outputs) and builds Granite's internal directed-graph representation from it — the same internal representation every downstream stage (Culprit Agent, Error Step Localization, Verification Agent) operates on, regardless of which framework produced the trace.
- One honest caveat carried forward from §5.2.1: timestamps in this run were captured post-hoc, not via real per-step hooks — fine for structural tracing, not yet trustworthy for latency-sensitive diagnosis.

**The LangGraph trace (Spike 6, `poc_spike6_cyclic_graph.py`).**

- A graph containing a true cycle — a Researcher↔Critic retry loop — tested with a per-node revisit bound in place (§5.3.3).
- LangGraph's own native execution model is graph-based with support for cycles by design — a structurally different shape from CrewAI's toy linear handoff chain, since LangGraph natively supports the retry-loop and iterative-refinement patterns CrewAI's toy case didn't exercise at all.
- The same execution-graph construction step has to read a genuinely different trace shape here: not a fixed sequence of task handoffs, but a graph where the Researcher node and the Critic node can each be visited multiple times (Researcher 3x, Critic 4x in the actual recorded run) before the workflow terminates.
- The revisit bound is not a cosmetic detail — the control run in the same spike, with the bound effectively disabled, hit the 10,000-step safety cap instead of terminating, direct proof the bound is load-bearing rather than a no-op (§5.2.1, §5.3.3).

**What stays identical across both traces, and what has to differ.**

- What's identical: the internal graph representation format, the backward causal-tracing algorithm (BFS from a failure node through the dependency graph) used by Error Step Localization, and the confidence-scoring formula (graph features — out-degree, betweenness centrality) used by both Culprit Agent and Error Step Localization. None of this logic is framework-specific; it operates purely on Granite's own internal graph, once that graph has been built.
- What has to differ: the trace-ingestion step that translates each framework's own native trace format into Granite's internal graph representation. CrewAI's task-handoff format and LangGraph's cyclic graph-with-checkpoints format are genuinely different shapes on the way in — this is exactly the layer Framework Compatibility Layer's "lightweight compatibility checking" (as opposed to full fault-injection benchmarking) targets for the other five surveyed frameworks Granite does not build a full benchmark against.
- The cycle-detection and revisit-bound logic itself (§5.3.3) is a case where a capability that *sounds* CrewAI/LangGraph-specific is actually general graph logic, applied because LangGraph's native execution model happens to need it for this toy example — the same logic would apply unchanged to any other framework's trace that also produced a cyclic graph shape.

**Why this side-by-side matters for the CCP claim, not just as a demo.**

- This is the concrete mechanism behind RQ2 (cross-architecture generalization) and the CCP characteristic-#1 argument (§4.5.2): the same diagnosis algorithm, unmodified, operating correctly on two structurally different trace shapes from two frameworks with genuinely different native execution models — not two frameworks that happen to produce similar-looking traces.
- It is also the concrete illustration of why the single-framework scope-narrowing advice (§4.5.2, §4.2.9's own committed-core context) would have removed real, already-demonstrated evidence, not just a hypothetical future claim: both traces shown here already exist as run code with real recorded output, not as a plan.

---

## 4.3 The market survey's own four tables, explained in full

### 4.3.1 Table 1 — the full 20-row feature matrix

Table 1 is the survey's central comparative artifact: eight columns (the seven frameworks plus "Proposed FYP") against 19 rated feature rows, plus one row treated separately (§4.3.1.4 and §5.6). Every row carries load-bearing evidence — not only the Core rows — because the non-Core rows establish which parts of the stack Granite is explicitly choosing to reuse rather than reinvent, and that reuse decision is itself part of the CCP argument (external-component classification, plan doc §6) and the scope-discipline argument.

**4.3.1.1 Rows 1–10 — the operational/infrastructure layer, all reused, none reinvented**

- **Multi-agent orchestration:** "Strong" across six of seven frameworks (BabyAGI "Partial," AgentCore "Platform/runtime"), and "Strong" for the Proposed FYP too — because Granite's own committed architectures already provide this natively.
- **Tool calling:** "Strong" across all seven and the Proposed FYP — universally solved, reused without comment.
- **Execution tracing:** "Strong" (with framework-specific qualifiers) across all seven and the Proposed FYP — the substrate Granite's own trace-capture stage builds on.
- **Runtime-error detection:** same pattern — ordinary exceptions and API failures are solved industry-wide; Granite's problem statement is explicit this is *not* what it targets.
- **Automatic retry:** "Strong" for the Proposed FYP despite mixed native ratings across the seven — because retry, in Granite's own architecture, is a *behavior* that falls out of Verified Automatic Repair plus Confidence Calibration together, not a standalone mechanism (§5.5.1).
- **Guardrails / validation:** "Strong" across most frameworks and the Proposed FYP — schema/type enforcement is the substrate Semantic Error Diagnostic builds on top of.
- **Persistent memory:** "Strong" across all seven and the Proposed FYP — Verified Repair Memory is a specific, narrower application of this, not a claim to have invented persistent memory.
- **Checkpoint / resume:** "Strong" for LangGraph, CrewAI, Microsoft Agent Framework; weaker for others; "Strong" for the Proposed FYP — the substrate Recovery Controller builds on. Generic checkpoint/resume existing is not the same as tying resumption to a *verified-repair point*, which is Recovery Controller's addition.
- **Workflow replay / fork:** "Strong" for LangGraph, CrewAI, Microsoft Agent Framework — the substrate Verified Automatic Repair's counterfactual re-execution (proven mechanically in Spike 5) builds on.
- **Agent evaluation:** "Strong"/"Ecosystem" across most frameworks — the substrate Verification Agent's evidence-grounded confirmation stage can draw signal from.

**4.3.1.2 Rows 11–18 — the eight "Core" rows, walked through individually**

- **Detect semantic wrong answer:** "Partial via eval/guardrail" or similar across all seven, "Core" for the Proposed FYP. Targeted by Semantic Error Diagnostic — the frameworks have *partial* eval/guardrail infrastructure, nothing above "Partial," confirming a real, not fully closed, gap even at the weakest tier of claim.
- **Find culprit agent:** flat "Not native" across all seven, "Core" for the Proposed FYP. Targeted by Culprit Agent — zero frameworks provide any native version of this at all.
- **Find originating error step:** same flat "Not native" pattern — Error Step Localization.
- **Causal backward error tracing:** same flat "Not native" pattern — the mechanism underlying both Culprit Agent and Error Step Localization's backward-tracing approach.
- **Automatically generate repair:** "Not native" (OpenAI SDK), "Custom" (five frameworks), "Experimental self-building" (BabyAGI). The row that directly motivated adding Repair Agent, since nothing here rises above "Custom" or "Experimental."
- **Verify repair before applying:** "Custom" or "Via evaluation/custom" across all seven — Verification Agent, applied specifically to gating a *repair*; "Limited" for BabyAGI.
- **Resume from repaired point:** "Not native" (OpenAI SDK, BabyAGI), "Checkpoint-based" (LangGraph, CrewAI, Microsoft Agent Framework), "Partial" (Google ADK, Amazon AgentCore). Directly motivated Recovery Controller's reclassification: checkpoint infrastructure exists in three of seven, but none tie resumption specifically to a verified-repair point.
- **Remember successful repairs:** "Not native" (OpenAI SDK), "Custom" (five frameworks), "Experimental" (BabyAGI). Directly motivated Verified Repair Memory's reclassification.

**4.3.1.3 Row 19 — the one row genuinely left open**

- "Self-improve from prior failures": rated "Experimental" (BabyAGI) or "Partial/custom" (most others).
- Distinctively, the Proposed FYP column is rated **"Verified/controlled,"** not "Core."
- This is the one row where the survey does not claim Granite's proposed scope closes the gap outright — treated separately in §5.6 as a real, undecided gap, not folded into the "Core" bucket the other eight rows get.

### 4.3.2 Table 2 — the five-layer framework

| Layer | Question | Strong solutions | Gap |
|---|---|---|---|
| 1. Runtime handling | Did a tool/API/node fail? | Agent SDKs, LangGraph, AgentCore, ADK, CrewAI | Mostly mature |
| 2. Workflow recovery | Can execution retry/resume? | LangGraph, CrewAI, Microsoft Agent Framework | Mostly mature |
| 3. Semantic diagnosis | Which agent introduced the wrong reasoning and where? | ERRORPROBE; research prototypes | Still under-served |
| 4. Targeted repair | Can the responsible component be corrected automatically? | Custom logic; experimental self-building | Major gap |
| 5. Verified self-healing | Can the fix be tested, replayed and remembered safely? | Partial/custom across frameworks | Strong FYP opportunity |

**Why this table matters more than a two-column gap summary**

- It makes explicit *where the maturity boundary sits*, and that boundary sits in a specific, defensible place.
- Layers 1–2 (mostly mature) map to what every one of the seven frameworks in §4.2 was shown to handle well.
- Layer 3 (under-served) is where ErrorProbe sits as the strongest existing partial solution.
- Layers 4–5 (major gap, strong FYP opportunity) are where nothing in either market layer offers a first-class solution at all.

**How Granite's ten foundational items map onto it**

- Fault-injection harness and Cross-architecture benchmark: infrastructure that spans and tests layers 1–3.
- Culprit Agent, Error Step Localization, Verification Agent, Semantic Error Diagnostic: layer 3.
- Repair Agent: layer 4.
- Verified Automatic Repair, Recovery Controller, Verified Repair Memory: layer 5.
- No foundational item duplicates layers 1–2 — evidence the scope-discipline argument (reuse what's mature, build only what's missing) was actually followed, not just claimed.

**How the PDF fuses this table with real POC evidence**

- `generate_supervisor_pdf.py`'s §6e restates this framing, annotating each layer directly with Granite's own Spike evidence.
- Layer 4: "Repair Agent sits here, proven 4/6 (Spike 8, risk-register.md R17)."
- Layer 5: "Verified Automatic Repair sits here, proven (Spike 5)."
- A deliberate rhetorical move: rather than treating the survey's abstract diagram as separate from Granite's own POC, the PDF fuses them into one picture — the gap the survey identified, with Granite's own real, run code sitting directly on top of the gap it targets.

### 4.3.2b Worked example — one failure trace, walked through all five layers

*A concrete illustration of Table 2 (§4.3.2), so the abstract layer names read as a real diagnostic sequence rather than a diagram. The scenario: a three-agent trip-planning crew (Planner, Booking Agent, Responder) on LangGraph books a hotel room for the wrong date range — a date silently shifted by one day somewhere in the pipeline — and the final itinerary is presented to the user as correct.*

**Layer 1 — Runtime handling. Question: did a tool/API/node fail?**

- No. Every tool call in the trace returns a valid, well-formed response — the hotel-booking API call succeeds, the confirmation is well-typed, no exception is thrown anywhere in the graph.
- This layer is "mostly mature" (Table 2) precisely because this is what agent SDKs, LangGraph, AgentCore, ADK, and CrewAI all handle well already (§4.3.1.1, rows 3–4) — and it correctly reports nothing wrong, because at this layer, nothing *is* wrong. A silent failure is defined precisely as a failure this layer cannot see (§4.2.6's AgentCore discussion makes the identical point from the infrastructure-observability side).

**Layer 2 — Workflow recovery. Question: can execution retry/resume?**

- Not triggered, because nothing failed at Layer 1 to retry. LangGraph's own checkpoint/resume and retry-policy infrastructure (§4.2.2, "Strong" in Table 1) sits ready but idle — there is no exception or interruption point for it to resume from.
- This is the layer whose maturity is why Recovery Controller (§5.2.9) is built to *reuse* checkpoint infrastructure rather than reinvent it — but also why Recovery Controller alone, without the layers below, could not have caught this specific failure even if it had been triggered by something else.

**Layer 3 — Semantic diagnosis. Question: which agent introduced the wrong reasoning and where?**

- This is where the failure actually becomes visible. Semantic Error Diagnostic's execution-state tracking (§5.2.7) compares the date value logged when Planner produced it against the date value Booking Agent's tool call actually used, and finds they differ by one day — a constraint violation with no upstream exception anywhere.
- Culprit Agent and Error Step Localization then run backward causal tracing over the LangGraph execution graph (the same BFS-from-failure-node mechanism proven in Spike 2's structural test and validated for cyclic graphs in Spike 6, §5.2.1, §5.3.3) and localize the date shift specifically to a step inside Booking Agent's own date-formatting logic, not to Planner (which produced the correct date) or Responder (which only relayed what it was given).
- Table 2 marks this layer "still under-served," with ErrorProbe as the strongest existing partial solution (§4.2.8) — this is the layer where Granite's own committed-core evidence (75% agent accuracy / 12.5% step accuracy, Spike 1, §5.2.3–5.2.4) is real but explicitly not yet at the field's best published number (ErrorProbe's own 59.5% step accuracy, itself an admission of how hard this layer is).

**Layer 4 — Targeted repair. Question: can the responsible component be corrected automatically?**

- Repair Agent (§5.2.6) generates a targeted correction to Booking Agent's date-formatting step — not a rewrite of the whole agent, per the survey's own scope-control principle adopted directly into Repair Agent's design (§4.5.1, §5.2.6).
- Table 2 marks this "major gap" market-wide — none of the seven frameworks checked in §4.2 ship this as a first-class capability (flat "Not native"/"Custom"/"Experimental" across all seven, §4.3.1.2) — and this is the layer where Spike 8's real, if partial, evidence sits: 4 of 6 synthetic cases repaired successfully, with the two failures traced to one specific, actionable interface-ambiguity root cause (§5.2.6).

**Layer 5 — Verified self-healing. Question: can the fix be tested, replayed and remembered safely?**

- Verified Automatic Repair (§5.2.8) deterministically re-executes the downstream portion of the trace — Responder's itinerary-generation step — with the corrected date, and confirms the final itinerary now matches what the user actually booked, the same mechanical replay-and-recompute logic Spike 5 proved (`recovery_success: true`).
- Recovery Controller (§5.2.9) would, once built, resume the workflow from a checkpoint at the corrected step rather than re-running Planner and Booking Agent from scratch — currently the one foundational item with zero POC evidence, named honestly as such rather than assumed to work (§5.2.9).
- Verified Repair Memory (§5.2.10) would, if its owed re-test on a stronger backbone succeeds, store this specific date-formatting correction so a structurally similar booking failure in a future trip-planning run could be repaired faster — currently resting on one real, failed test (0/8 commits), carried forward honestly rather than assumed fixed by the re-test not yet having happened.
- Table 2 marks this layer "strong FYP opportunity" precisely because two of its three constituent items (Verified Automatic Repair, real evidence; Repair Agent, real partial evidence) already have run code behind them, while the third (Recovery Controller) and the memory layer (Verified Repair Memory) are the two honestly-flagged open items carried through this entire document (§5.2.9, §5.2.10, §5.9.7–5.9.8).

**What this walkthrough demonstrates that the table alone doesn't.**

- A single failure can pass cleanly through Layers 1 and 2 — the layers every commercial platform and framework checked in Part 4 handles well — and only become visible at Layer 3, which is exactly the structural argument behind why "the trace looks clean" (as every one of the seven Layer-1 platforms would report for this scenario, per §4.1's per-platform write-ups) is not the same statement as "nothing is wrong."
- It also shows the five layers are not independent alternatives but a pipeline where each layer's output is the next layer's input — Layer 3's diagnosis feeds Layer 4's repair, which Layer 5 verifies and, if the mechanism works, remembers — matching the survey's own 9-step recommended flow (§4.4) rather than five unconnected capabilities.

---

### 4.3.3 Table 3 — market saturation vs. FYP value

**How the sixteen rows split**

- Six rated flatly "Saturated," "Reuse" for FYP value: agent orchestration, tool integration, logging/tracing, exception detection, automatic retries, memory.
- Two more "Strong existing solutions," "Reuse": checkpoint/resume, guardrails.
- One "Rapidly maturing," "Reuse/adapt": agent evaluation.
- Nine of sixteen rows where the survey's own advice is simply: don't build this, it's already solved elsewhere.

**Where the FYP value actually concentrates — the remaining seven rows**

- Semantic failure detection: "Partial" market status, "Useful component" FYP value.
- Culprit-agent attribution: "Research-level / under-served," "Strong feature."
- Originating-step localisation: "Research-level / under-served," "Strong feature."
- Automatic targeted repair: "Major gap," "Excellent feature."
- Verification of generated repair: "Partial/custom," "Excellent feature."
- Resume after verified repair: "Integration gap," "Excellent feature" — rated differently from plain checkpoint/resume, because it's the *combination* with verification that's the gap, not resumption itself.
- Verified repair memory: "Under-served," "Excellent feature."

**Why the escalating language matters**

- Four separate "Excellent feature" ratings appear only in the repair-and-recovery half of this group, rather than the diagnosis half — the survey rates rows 4–7 of this group as more valuable FYP territory than rows 1–3.
- This is a partial explanation for why the survey's own recommended four new modules (§4.4) lean toward Repair Agent, Verification Agent, and Verified Repair Memory rather than further diagnosis refinement.

**The table's own ready-to-use proposal sentence**

- "Existing agent SDKs provide mechanisms for observing, retrying and resuming failed workflows, while recent research such as ERRORPROBE addresses semantic failure attribution. A practical gap remains in automatically transforming root-cause diagnosis into a verified repair, resuming execution from the corrected state, and retaining successful repair knowledge for future failures."
- In effect, a condensed restatement of exactly what Granite's ten foundational items exist to do, written independently of Granite's own documents.

### 4.3.4 Table 4 — evaluation metrics

Nine recommended quantitative metrics, each with what it measures and a suggested comparison baseline: task completion rate (baseline MAS vs. self-healing MAS), failure detection precision/recall (detector variants), culprit-agent accuracy (root-cause module vs. simple last-error baseline), error-step accuracy (backward tracing vs. full-trace judge), repair success rate (with vs. without verification), recovery rate (baseline retry vs. targeted repair), re-execution cost (restart-from-zero vs. checkpoint resume), repair reuse benefit (memory off vs. memory on), false repair rate (verification ablation).

**What happened to each of the nine, tracked by the integration audit**

- Culprit-agent accuracy, error-step accuracy, recovery rate: already had direct equivalents in Granite's own pre-existing evaluation plan (top-1 agent accuracy, top-1 step accuracy, recovery success rate).
- Repair success rate and false repair rate: genuinely missing, added. False repair rate flagged specifically as "the metric that keeps 'verified' in Verified Automatic Repair honest, not just asserted" — without it, a system could claim "verified" while still silently letting bad fixes through at some non-zero rate.
- Re-execution cost and repair reuse benefit: deliberately **not** added, on a stated principle: "both measure Checkpointing and Verified Repair Memory, neither of which is in scope; adding the metric before the feature exists would be premature, not an oversight."

**Why this restraint is worth flagging as evidence of discipline**

- Even when a credible external source recommends a metric, the decision not to add it rests on a stated principle (don't measure a feature you haven't built), not "we ran out of time."
- Once Recovery Controller and Verified Repair Memory both became foundational items in the ninth session's reclassification, these two metrics remained un-added — the reclassification changed the feature's *scope status*, not automatically its *evaluation-metric status*, since these two metrics specifically require the mechanisms to be built and running, not merely committed to the core.

---

## 4.4 The survey's recommended system flow — 9 steps, explained

Section 6.1 of the survey lays out a recommended figure — "Execute MAS → Detect Failure → Localise Cause → Generate Repair → Verify Repair → Resume Workflow → Store Repair" — expanded into nine numbered steps.

1. **Multi-Agent Runtime:** "Use an existing framework for Planner/Worker/Reviewer or similar agents." The layer-1/layer-2 reuse instruction restated as step one. Granite already committed to exactly this (CrewAI, LangGraph as core frameworks) — no scope change.
2. **Trace Collector:** "Store agent messages, tool calls, outputs, exceptions and checkpoint identifiers." Maps to execution-graph construction, already in Granite's architecture, proven in Spike 2's toy CrewAI workflow — no scope change.
3. **Semantic Failure Detector:** "Identify failures that may not be ordinary runtime exceptions, using constraints, evaluator signals or task-specific checks." Maps to Semantic Error Diagnostic, already committed and POC-tested (Spike 4) — no scope change.
4. **Root-Cause Localizer:** "Estimate the culprit agent and originating error step using backward dependency/trace reasoning." Maps to Culprit Agent + Error Step Localization together — the first independent convergence: already existed under those two names before this survey was read.
5. **Repair Agent:** "Generate a targeted correction to the prompt, tool arguments, structured output or function logic associated with the localized failure." The one step genuinely absent from Granite's prior 16-item list — the real gap this survey surfaced, discussed fully in §5.2.6.
6. **Verification Agent:** "Test candidate repairs using deterministic checks, sandbox execution, test cases or evaluator constraints." Already existed under the exact same name — the second independent convergence, and a stronger form of convergence than a matching *concept* under a different label, since the naming choice itself matched.
7. **Recovery Controller:** "Apply only verified repairs and resume execution from a safe checkpoint instead of restarting the entire workflow." Resolved the long-open "Checkpointing" item (open since 2026-08-23) — discussed fully in §5.2.9.
8. **Verified Repair Memory:** "Store successful error → diagnosis → repair patterns and retrieve them for similar future failures." Not new as a *concept* — the "Verified Episodic Memory" mechanism already built, tested, and reverted before this survey was read — but the survey's independent inclusion triggered logging its full history properly (R18), discussed fully in §5.2.10.
9. **Dashboard:** "Visualize the workflow, failed agent, originating step, repair attempt, verification result and final recovered execution." Already committed core item 6 — needed no new work, just confirmation the already-planned dashboard's content matches this step.

**What this 9-step audit actually shows**

- Five of nine steps (1, 2, 3, 4, 6) landed on pre-existing mechanisms with no scope change.
- One step (9) matched an already-committed but not-yet-built deliverable.
- Three steps (5, 7, 8) triggered real scope changes: Repair Agent (genuinely new), Recovery Controller (resolved a previously-deferred item), Verified Repair Memory (resurfaced a previously-built-and-reverted mechanism's proper history).
- This 5/1/3 split is the most honest single summary of the survey's actual contribution: mostly confirmation of an architecture already converged upon independently, plus three specific, traceable scope decisions.

---

## 4.5 What was adopted vs. explicitly rejected from the survey

### 4.5.1 Adopted

- The survey's core research-gap framing, adopted essentially wholesale — it matched, rather than contradicted, Granite's own pre-existing gap analysis from the seven-paper academic corpus and the Layer-1 commercial check: "Existing SDKs can observe, retry and resume workflows; ERRORPROBE can attribute semantic failures; the missing integration is to turn a verified diagnosis into a verified repair and resume execution from the corrected state."
- Three of its four recommended modules (Root-Cause Localizer, Verification Agent, and half of the closed repair loop) confirmed as already-built mechanisms under matching or equivalent names.
- Repair Agent, the one genuinely new module, adopted as foundational item #6.
- Two evaluation metrics (repair success rate, false repair rate) adopted into plan doc §11.
- The "treat repair as targeted modification... do not attempt unrestricted rewriting" scope-control principle (§7 of the survey) adopted as Repair Agent's explicit scope boundary.
- The "verification-gated" principle (§7, §9 of the survey) was already Granite's standing practice via extension #12 before this survey was read — a fourth instance of independent convergence, this time on a design *principle* rather than a named module.

### 4.5.2 Rejected — the single-framework scope-narrowing recommendation, full reasoning

The survey's own §7 "Scope Control for a One-Year BS Project," first bullet: "Use one agent framework only (recommended: LangGraph, because checkpointing and replay are already available)." Explicitly and deliberately not followed.

**Why the advice is good advice, in general**

- The survey's own reasoning is sound: a complete research vision can become too broad for a one-year BS project.
- Building against a single, well-chosen framework removes an entire axis of engineering effort — no need to instrument, debug, and maintain fault-injection harnesses across multiple frameworks with different message-passing semantics, different tool-call conventions, different failure modes.
- This is exactly the kind of scope discipline the FAST guide itself repeatedly warns projects to apply (breadth-over-depth is explicitly named as a risk in R8).

**Why it was rejected anyway**

- Because it would eliminate RQ2 — cross-architecture generalization across CrewAI, LangGraph, and a 3rd architecture — one of Granite's *two lead research questions*, not a peripheral nice-to-have.
- The plan doc's own CCP problem statement (§1, "Strong" tier) explicitly names "generalize to multi-agent architectures absent from any prior paper's benchmark construction" as one of the load-bearing claims that distinguishes the Strong CCP tier from the Developing tier.
- The contribution statement (§3) names this as one of two things the project delivers: "a cross-architecture failure-attribution benchmark from controlled fault injection into multi-agent frameworks never used by any of the seven papers surveyed."
- If narrowed to LangGraph alone, this claim — and the CCP evidence resting on it (characteristic #1, "generalization vs. specialization to known architectures"; the research-to-decision table's "No paper tests generalization to a multi-agent architecture absent from its own benchmark construction" row) — would simply not exist.
- Not that the single-framework version would be a *worse* FYP — it would be a *materially different, already-narrower* FYP than the one already CCP-justified, scoped, and partially evidenced (Spike 2, resolved per R2).

**What would have been lost, stated directly**

- No CrewAI instrumentation at all (Spike 2's evidence becomes moot).
- No cross-architecture benchmark (committed core item 2 disappears).
- The "beats a paper that's never been generalization-tested" novelty angle (plan doc §4) loses one of its two legs, leaving only the silent-failure detection claim standing alone.
- Extension #2 (3rd architecture) and extension #8 (Framework Compatibility Layer) both become nonsensical — nothing to extend generalization *from*.
- R19's own resolution line: "Good general advice for a differently-scoped FYP; incompatible with this one's already-committed novelty case."

### 4.5.3 The positive resolution — Framework Compatibility Layer

- Rejecting the survey's advice outright, with no counter-offer, would have left an honest gap unaddressed: the survey's underlying *concern* (fully supporting all seven frameworks would blow the project's one-year budget) is legitimate even if its proposed *solution* (pick just one) isn't right for a project whose CCP claim depends on multiple architectures.
- `Commercial_Product_Comparison.md` states this directly: "Resolved positively, not just rejected."
- The resolution: Framework Compatibility Layer (extension #8, §5.3.8) — keep *full* fault-injection and benchmarked evaluation on only the 2–3 committed core frameworks, while extending *lightweight compatibility checking* across all seven, without building a full fault-injection benchmark for each.
- Plan doc's own trade-off statement: "building full benchmarks on all 7 would roughly double the core's engineering workload for a one-year BS project (risk-register.md R8: breadth-over-depth)."
- Correctly presented as neither adopting nor flatly rejecting the survey's advice — a third option taking the underlying scope-discipline concern seriously while preserving the two-architecture generalization claim the CCP rating depends on.

---

## 4.6 Cross-references — connecting Part 4's market findings back to Parts 1–3

*Part 4 was written and read on its own terms above; this section makes explicit what several of its findings assume as background — the specific CCP characteristic, contribution-statement line, or risk-register entry from Parts 1–3 that each market finding either evidences or depends on. This is not new argument, only explicit wiring between two Parts that are otherwise left to a reader to connect themselves.*

**The positioning correction (§4.0.4, §4.1.8) and CCP Characteristic #9 (requirement identification / ill-defined cause).** Part 3's Characteristic 9 write-up (line 1115) argues the project sits in "ill-defined requirements or cause" territory specifically because *whether a trace contains a failure at all* is itself often unknown in advance. The LangSmith Engine / Arize Alyx correction is a live instance of the same ill-definedness playing out at the market-research level, not just the technical level: the original risk-register assumption (R9, "nobody automates this") was itself an ill-defined-requirement problem — the team did not know in advance that the market's own boundary had shifted mid-project, and had to check directly rather than assume the boundary was fixed. The correction is evidence *for* Characteristic 9, not just a research-process anecdote.

**The five items none of the seven Layer-1 platforms confirm (§4.1.7) and the Part 1 contribution statement.** Part 1's contribution statement (referenced throughout Part 4 as "§3") names two deliverables: the cross-architecture benchmark and the silent-failure-detection claim. Items 1, 3, and 4 of §4.1.7's list (agent-and-step attribution, silent-failure detection, cross-framework generality) map directly onto those two contribution-statement lines — meaning the market check in §4.1.7 is not a freestanding finding, it is the evidentiary backing for the specific two-item contribution claim Part 1 makes.

**CrewAI as the committed core (§4.2.3, §5.7.4) and Assumption A2 (§2.9, risk register).** The risk register's Assumption A2 states "CrewAI and LangGraph remain genuinely unused by any published failure-attribution paper through Final-2." Every place in Part 4 where CrewAI's Spike-2 evidence is cited as proof of generalization (§4.2.3, §4.2.9, §5.7.4) is, in effect, citing evidence that only remains valid for as long as A2 holds — a dependency Part 4 relies on but does not re-argue each time.

**The single-framework rejection (§4.5.2) and CCP Characteristic #1 (conflicting requirements).** Part 3's Characteristic 1 write-up frames the core CCP tension as "generalization vs. specialization to known architectures" (referenced directly in §4.5.2's own text). The rejection of the market survey's single-framework advice is the single clearest place in the whole document where a piece of well-reasoned external advice was tested directly against a specific, already-established CCP characteristic and found incompatible with it — not a case of the team simply preferring its own plan.

**Framework Compatibility Layer (§4.5.3, §5.3.8) and the External Component Classification table (Part 1, §1.8).** Part 1's external-component table classifies which pieces of Granite's pipeline are reused infrastructure versus newly built logic. Framework Compatibility Layer is the extension-level embodiment of that same reuse-versus-build discipline applied to a market-positioning question rather than a code-architecture question: reuse (lightweight compatibility) where the market survey showed reuse was sufficient, build (full benchmarking) only where the CCP claim actually required it.

**Table 4's two deliberately-unadded metrics (§4.3.4) and the plan doc's own scope-discipline principle (Part 2, §2.6).** Part 2's feature-list-evolution narrative (§2.6) documents the same list settling at 20 items through five distinct, evidence-driven triggers. The decision not to add re-execution cost and repair reuse benefit as metrics (§4.3.4) is a small-scale instance of the identical discipline: a metric is added only once the feature it measures is actually in scope and built, exactly mirroring how a *feature* is added only once it survives the five-rule filter described in §2.6.2 and narrated again in §5.1.1 below.

**Five concrete use cases (§5.7, below) and Characteristic #6 (diverse stakeholders).** Part 3's Characteristic 6 write-up is flagged, honestly, as "the honestly-weak one" (line 1035) because real stakeholders had not yet been contacted as of the plan doc's writing (Issue I2, risk register). The five use-case scenarios in §5.7 name specific, plausible stakeholder roles (on-call engineers, compliance/QA teams, incident post-mortem reviewers) for each mechanism — real reasoning about who would use each feature, but reasoning that does not itself substitute for the actual stakeholder contact Characteristic 6 still needs, and this document does not claim otherwise.

---

# PART 5 — THE FEATURE LIST, ALL 20 ITEMS

## 5.0 Reading this Part

This Part is the core of the whole document, written as narrated history rather than a static specification. The feature list did not arrive fully formed — it went through five distinct sizes (5 → 7 → 8 → briefly 18 → briefly 10+10+2=22 → settling at 10+8+2=20), each transition driven by a specific piece of feedback or evidence, on record in `risk-register.md` and `AI_Usage_Log.md` as it happened. Presenting the final 20-item list without this history would understate how much real reasoning went into arriving at it, and would make several individually defensible decisions — like reclassifying two items into the foundational core on the same day they were first added as extensions — look arbitrary rather than principled.

## 5.1 The full reclassification history, narrated in order

### 5.1.1 Five foundational (the original committed core)

- The project's committed core began, in the plan doc's own §7 ("must exist by Final-2"), as seven numbered lines.
- The feature-list-specific framing in §7.0 traces its own count starting from **5 foundational core items**, mapping onto committed-core lines 1, 3, 4, 5 (plus the generalization claim spanning line 1 and the still-future 3rd-architecture extension): fault-injection harness, cross-architecture benchmark, core attribution algorithm (bundled as one item at this stage), silent-failure verification, counterfactual replay engine.
- These five, plus 7 extensions that survived a five-rule filter (genuine market gap, architectural compatibility, no duplication, the replacement test, workload-fit — from `AI_Usage_Log.md`'s third session), plus 2 explicitly deprioritized items, made 14 total.
- This is the "14 features" the supervisor feedback below refers to.

### 5.1.2 5 → 7: the 2026-08-23 rename, splitting "core attribution algorithm"

**The trigger**

- Supervisor feedback flagged the original framing as reading like "14 features that map to 1 feature" — the concern being that "core attribution algorithm" was doing an enormous amount of undifferentiated work under one label, while the other 13 items (mostly extensions) were each narrow and specific.
- This is a legitimate critique of presentation clarity, not of scope.

**The fix, applied precisely**

- `AI_Usage_Log.md`'s fifth session records it: "The fix is not fewer mechanisms — it's naming each one by the distinct thing it actually does, instead of bundling three separate pipeline stages under one vague label."
- "Core attribution algorithm" was never actually one mechanism — it was already, under the hood, ErrorProbe's real three-stage architecture (Strategist → Investigator → Arbiter), just described with one collective noun.
- Split into its three real stages: **Culprit Agent** (the Strategist's agent-hypothesis output), **Error Step Localization** (the Strategist's step-hypothesis output), **Verification Agent** (the Investigator's evidence-grounded confirmation stage).
- Each is now independently demoable and independently defensible under Section 14.1's four-question test (explain it, justify alternatives rejected, predict what breaks, modify it under questioning) — which "core attribution algorithm" as one bundled label could not be.
- Two further renames, same pass, naming clarity only, no scope change: "silent-failure verification" → Semantic Error Diagnostic; "counterfactual replay engine" → Verified Automatic Repair.

**Net effect**

- Foundational count 5 → 7; total frozen feature count 14 → 16 (7 foundational + 7 extensions + 2 deprioritized).

**What did NOT change**

- Plan doc's own statement: "No scope, mechanism, or evidence change — every POC spike (1, 5) and every risk-register entry tied to the old names still describes the exact same code and the exact same results, just under a clearer name going forward."
- Spike 1's 75%/12.5% numbers and Spike 5's `recovery_success: true` result did not change; only the label attached to the mechanisms they tested did.

### 5.1.3 7 → 8: the 2026-08-24 addition of Repair Agent, closing the FR4 gap

**The trigger**

- A full read of `Agentic_AI_Market_Survey_BS_FYP.docx` surfaced a gap sitting unnoticed in Granite's own functional requirements the whole time.
- FR4 (§0.07): "The system shall, given a candidate corrected value for a specific step, deterministically re-execute the downstream portion of the trace and report whether the corrected trace now succeeds."
- The word "given" is the tell — FR4 assumes a candidate correction already exists by the time the system acts on it.

**What was found**

- Nothing in the prior 16-item list actually *produced* that candidate value.
- Verified Automatic Repair only ever tested and re-executed a correction it was handed; nothing generated the correction itself.
- The survey's recommended flow named this exact missing step as its fifth module, Repair Agent.
- The survey's feature matrix independently confirmed the gap was real and unclosed market-wide: "automatically generate repair" rated Not native / Custom / Experimental across all seven surveyed frameworks — nobody ships this as a first-class capability.

**The addition, and a notable exception to the usual pattern**

- Added as foundational item #6 the same day.
- Unlike some later additions, POC-tested the *same day* (Spike 8, §5.2.6), rather than added with a promise to test it later.

**Net effect**

- Foundational count 7 → 8; total frozen feature count 16 → 17.

### 5.1.4 8 → briefly 18 → briefly 22 → settling at 20: the same-day, three-pass extension of 2026-08-24

The rest of that same day saw two more passes, both recorded in `AI_Usage_Log.md`'s sixth, eighth, and ninth sessions and `risk-register.md` R17–R22 — three genuinely distinct decisions made hours apart, not one bundled change.

**Second pass — Framework Compatibility Layer added as extension #8**

- The positive resolution to the single-framework scope-narrowing rejection (§4.5.3): a real scope question ("use features of all products, not only from one") needed a real, scoped answer.
- Answer: a new extension drawing capabilities and evidence from all seven surveyed frameworks via lightweight compatibility checks, while keeping full benchmarked rigor on only the 2–3 core frameworks.
- Extension count 7 → 8; total 17 → 18 (8 foundational + 8 extensions + 2 deprioritized).

**Third pass — Recovery Controller and Verified Repair Memory added as extensions #9–10, briefly**

- The survey's own step 7 (Recovery Controller) and step 8 (Verified Repair Memory) were both genuinely new or previously-deferred mechanisms not yet in the 18-item list.
- Recovery Controller formally resolved the "Checkpointing" item that had sat unresolved in the "considered, not added" bucket since 2026-08-23 — acknowledged then as genuinely distinct from Verified Automatic Repair, but never run through the CCP/market/academic-overlap filter every other item received, so it stayed parked rather than added speculatively.
- Verified Repair Memory was a re-add: already built once (as "Verified Episodic Memory," 2026-08-23), tested once, failed its test, and deliberately reverted and left out of the frozen list — its history is the subject of §5.2.10.
- Both added, initially, as extensions #9 and #10 — a cautious placement, treating them as product-differentiating add-ons rather than core research claims, consistent with how a fresh mechanism (Recovery Controller, zero POC evidence) and a mechanism with a documented failed test (Verified Repair Memory) would normally be staged.
- Extension count 8 → 10 (briefly); total 18 → 20 (briefly, as 8 foundational + 10 extensions + 2 deprioritized).

**Same day, hours later — reclassification into foundational**

- A closer read of the survey's own Table 1 revealed an inconsistency in how Granite had been applying the survey's own classification.
- Table 1 rates *eight* capability rows "Core" for the Proposed FYP column, not six: the six Granite had already treated as foundational (items #3–#8) **plus** "Resume from repaired point" and "Remember successful repairs" — the exact two capabilities Recovery Controller and Verified Repair Memory implement, which had just been placed as extensions #9–10.
- Leaving these two as extensions while treating the other six Core-rated rows as foundational was inconsistent with the survey's own classification scheme Granite otherwise relied on.
- The fix: move both into the foundational core as items #9 and #10, matching the survey's own rating rather than applying it selectively.
- Extension count reverts 10 → 8 (net unchanged from the second pass's end state); foundational count 8 → 10; total settles at 20 (10 foundational + 8 extensions + 2 deprioritized) — the final, frozen count.

**The framing choice worth naming explicitly**

- R21 and R22 record this reclassification as "a scope decision, not new evidence" for Verified Repair Memory specifically.
- The item's one real test result (0/8 commits, all 24 verifications NOT_SUPPORTED, 75%→50% regression) stays on record as a failure, unmodified by the fact that the item is now foundational rather than an extension.
- This is the single clearest instance in the whole project's history of the "report negative results honestly, don't soften them because the stakes changed" discipline — preserved deliberately, not incidentally.

### 5.1.5 Why this history matters, stated once

Five distinct triggers produced five distinct list sizes across roughly 48 hours of real work: a supervisor's presentation-clarity critique (5→7), a self-discovered gap in the project's own functional requirements cross-checked against an external survey (7→8), a scope-control question needing a positive answer rather than a flat rejection (17→18), a re-add of a previously-failed mechanism plus a previously-deferred one (18→20 briefly, as extensions), and a consistency check against the survey's own stated classification (settling at 10+8+2=20). None of these five changes added scope for its own sake — each traces to a specific piece of evidence or feedback, and every negative result encountered along the way is carried forward into the final list rather than erased by the act of promotion to foundational status.

### 5.1.6 Panel-style follow-up Q&A on the feature-list growth

*A count going 14 → 16 → 17 → 18 → 20 (briefly touching 22 mid-count, per §5.1.4's "briefly 22" wording, before settling back at 20) is exactly the shape of history a skeptical panel is trained to probe as scope creep. The questions below are the ones that shape is likely to invite, answered with the specific dated trigger already on record for each, not with a defensive restatement of the final number.*

**Q: A count that grows five times in 48 hours looks less like careful scoping and more like the team couldn't hold a line. Why should we trust this list is actually frozen now, rather than growing again the moment someone reads one more paper?**

A: Every one of the five triggers is traceable to a specific, external, non-arbitrary source — a supervisor's own critique (5→7), the project's own functional requirement contradicting itself once checked (7→8), and a market survey's own published classification table (the 17→18 and 18→20 moves both cite the survey's own Table 1 ratings, not a team preference). None of the five moves originated from the team simply wanting to add something. The count stopped growing on 2026-08-24 specifically because the consistency check against the survey's own eight "Core"-rated rows was, at that point, exhaustive — every row the survey itself rates "Core" for the Proposed FYP is now accounted for in the foundational ten (§4.3.1.2), and nothing beyond those eight rows has surfaced a comparable external trigger since. The honest caveat is that "frozen" describes a decision, not a law of physics — §5.1.1's own header states extensions are gated behind the foundational ten "in this priority order, only after" they work, meaning even the frozen list has an explicit re-open condition (a new paper closing one of the two targeted gaps, tracked as R7) rather than a claim that nothing could ever change it again.

**Q: Isn't "we found the gap ourselves, in our own FR4" (the 7→8 trigger, Repair Agent) a suspiciously convenient story — how do we know that wasn't invented after the fact to make the addition look more rigorous than "we read a cool survey and wanted to add its ideas"?**

A: The sequence is dated and falsifiable, not asserted after the fact: FR4's text ("given a candidate corrected value...") predates the market-survey read by weeks — it was written when the plan doc's functional requirements were first drafted, at a point where Verified Automatic Repair (then still called "counterfactual replay engine") was the only repair-adjacent item on the list. The gap — nothing upstream of FR4 ever produced the candidate value FR4 assumes — was real and present in the requirements the whole time; the market survey's independent recommendation of a "Repair Agent" module (its own step 5, §4.4) is what surfaced it to the team's attention, not what created it. This is stated plainly in §5.1.3: "A full read of `Agentic_AI_Market_Survey_BS_FYP.docx` surfaced a gap sitting unnoticed in Granite's own functional requirements the whole time" — the gap was unnoticed, not nonexistent, before the survey was read.

**Q: Two items (Recovery Controller, Verified Repair Memory) went from "extension" to "foundational" on the same day they were added. Doesn't that look like the classification itself is arbitrary — if it can flip in hours, what does "foundational" even mean?**

A: The classification is not arbitrary — it's anchored to one external, fixed reference point: the market survey's own Table 1, which rates exactly eight capability rows "Core" for the Proposed FYP column (§4.3.1.2, §5.1.4). The team's first-pass placement (extensions #9–10) was the actual mistake, caught within the same day by re-reading that same table more carefully — the correction moved the classification to *match* an already-fixed external standard the team was otherwise already relying on for the other six foundational items, rather than the standard itself moving. The more uncomfortable, more honest answer sits alongside this: the reclassification did not fix the underlying evidence gap. Verified Repair Memory is foundational item #10 and still rests on one real test that failed (0/8 commits, §5.2.10); Recovery Controller is foundational item #9 and still has zero POC evidence at all (§5.2.9). Promoting an item's classification does not promote its evidence — both facts are stated without euphemism in §5.1.4's closing paragraph and again in §5.2.9–5.2.10, specifically to prevent "foundational" from being read as "proven."

**Q: If two of the ten foundational items — a fifth of the actual research claim — have zero or failed evidence, why commit them to the core at all instead of leaving them as aspirational extensions until they're actually validated?**

A: This is the sharpest version of the scope-creep question, and the honest answer is that the classification decision and the evidence decision are treated as genuinely separate questions here, on purpose. The classification question — does this capability belong in the set the project's core research claim depends on — is answered by the survey's own Table 1, external and fixed. The evidence question — has this specific mechanism actually been shown to work — is answered by the spike record, and for these two items that answer is currently no. §5.1.4's own framing calls this "the single clearest instance in the whole project's history of the 'report negative results honestly, don't soften them because the stakes changed' discipline" — the alternative (quietly leaving them as low-stakes extensions until they happen to work) would have hidden a real risk rather than surfaced it for the panel to probe. Recovery Controller's re-test and Verified Repair Memory's stronger-backbone re-test are both explicitly named, dated obligations before Mid-1 (§5.2.9, §5.2.10), not open-ended aspirations.

**Q: The plan doc itself once described the original set as "14 features that map to 1 feature" — a supervisor's own criticism. Doesn't the eventual size of 20 just prove the supervisor was right to be worried about scope, even if the specific critique (bundling, not overall size) was about something else?**

A: The supervisor's critique (§5.1.2) was specifically about presentation clarity — one label ("core attribution algorithm") hiding three independently demoable pipeline stages — not about the total item count being too large. The fix applied was a split, explicitly not a size increase: "The fix is not fewer mechanisms — it's naming each one by the distinct thing it actually does" (§5.1.2, quoting `AI_Usage_Log.md`'s fifth session directly). The count growth from 16 onward (7→8→10 foundational) came from three later, unrelated triggers (§5.1.3–5.1.4), not from re-litigating the original bundling critique. Conflating "the list is now visibly longer" with "the supervisor's specific concern was never addressed" would misread which problem each change actually solved — the bundling critique was fully resolved at the 5→7 split, and every subsequent growth is independently justified on its own separate evidentiary grounds, narrated item by item in §5.1.3–5.1.4 rather than folded into one undifferentiated "the list grew" narrative.

---

## 5.2 The ten foundational items, each in full

*Ownership note: per plan doc §9, the three role areas (Data/Benchmark Owner, Diagnosis Engine Owner, Platform Owner) are defined but not yet assigned to specific people (R6, open). Each item below names which role area would own it.*

### 5.2.1 Fault-injection harness

**What it is**

- A mechanism that injects controlled, deterministic corruption into a multi-agent workflow's execution and records, by construction, the ground-truth agent and step responsible for each injected fault.
- FR1 verbatim: "The system shall inject controlled, deterministic faults into a multi-agent workflow built on CrewAI or LangGraph and record the ground-truth agent and step responsible for each injected fault."
- Currently one validated fault type (corrupted tool output); two more (communication corruption, context truncation) planned as extension #1.

**How it works mechanically**

- Rule-based, deterministic corruption operators — matching AgenTracer's own perturbation-operator approach, per the plan doc's external-component table: "Rule-based, deterministic corruption (matches AgenTracer's own perturbation-operator approach)... 0%" API-dependent.
- The injection logic itself is ordinary code, not an LLM call — a script intercepts a specific step's output (say, a tool-call result) and substitutes a plausible-but-wrong value in its place, according to a fixed rule, recording the original step's identifier as ground truth before overwriting it.
- **Spike 3 (run twice) — direct mechanical evidence, both runs kept, not just the second:**
  - First attempt: a famous-fact corruption, caught and self-corrected by the agent, exposing that substring-matching propagation checks were too crude — a real methodological finding carried forward honestly, not hidden.
  - Second attempt: an unverifiable fabricated fact with structured verification, producing clean, unambiguous blind propagation.
  - Both outcomes — self-correction and blind propagation — are kept as documented cases the benchmark accounts for, rather than assuming only one behavior pattern exists.

**Why it's foundational, not an extension**

- Every downstream foundational item — the benchmark itself, Culprit Agent, Error Step Localization, Verification Agent, and ultimately the entire evaluation plan (§11 of the plan doc) — depends on having ground-truth-labeled failure cases to test against.
- Without a working harness, there is no labeled data for anything else in the pipeline to be measured against — the one item everything else is conditioned on existing first.
- Per the team-ownership table, removing this item means "The entire new benchmark — no cross-architecture evaluation is possible" — the single most severe "if removed" consequence in that table.

**Precedent-check result**

- "Not found in any paper or product — genuinely new combination" (PDF §6a).
- The individual injection technique (rule-based perturbation) is directly borrowed from AgenTracer, stated openly rather than hidden — plan doc §4.1's defense against "you just combined existing techniques" names this explicitly: "Rule-based fault injection is AgenTracer's own technique."
- What's not found anywhere is the *combination*: applying that technique across multiple previously-unused multi-agent architectures specifically to test generalization.

**POC status, with real numbers**

- Fully met its target validation as of 2026-08-23 — the one foundational item with unambiguous, fully-resolved POC evidence (R2, R3 both resolved).
- Spike 2 traced a toy 3-agent CrewAI workflow cleanly into 3 nodes / 2 correctly-ordered edges.
- One honest caveat carried forward, not smoothed over: "timestamps were captured post-hoc, not via real per-step hooks — fine for structure, not yet trustworthy for latency metrics; real hooks needed in the actual build."
- Owned by the Data/Benchmark Owner role.

### 5.2.2 Cross-architecture benchmark

**What it is**

- A new, ground-truth-labeled benchmark built from the fault-injection harness's output, spanning at least two multi-agent architectures (CrewAI and LangGraph as committed core, a 3rd via extension #2) that no prior failure-attribution paper's benchmark construction has used.
- FR1's data counterpart, committed-core line 2 verbatim.

**How it works mechanically**

- Built on top of existing public task sources rather than authoring new tasks from scratch.
- Plan doc §8: ground truth comes from the injection operator itself, not manual labeling — "the same trick AgenTracer used to remove its '30-hour-per-annotator' cost."
- Active build target, two task sources:
  - **GSM8K** (8,792 rows, cheap prototyping, MIT-licensed) — chosen because its single-integer answers match Spike 4's already-validated numeric near-miss detection mechanism cleanly.
  - **tau-bench retail** (635 tasks, the real benchmark-building pass) — chosen for richer ground truth (full correct action sequences plus policy rules), matching the product's real deployment domain (customer support).
- Three more datasets (GAIA, MBPP+, MATH) are downloaded, license-verified, and benched on disk but not currently built against — reserved only if the two active sources prove too thin against the 500–1,000 trace target.
- Target scale: 500–1,000 labeled traces, matching both AgenTracer's own scale and the original pitch's scale.

**Why it's foundational, not an extension**

- This is the data-resource contribution half of the plan doc's contribution statement (§3): "a cross-architecture failure-attribution benchmark from controlled fault injection into multi-agent frameworks never used by any of the seven papers surveyed."
- Without it, there is no way to measure the generalization claim (RQ2) that CCP characteristic #1 (conflicting requirements: generalization vs. specialization) depends on.
- Per the deployment plan (§13), this is also the one foundational item with a life beyond Granite's own evaluation — a resource other researchers could reuse (recommended MIT/CC BY 4.0 release).

**Precedent-check result**

- "Not found — no paper or platform publishes one" (PDF §6a).
- **A live, correctable example of the project's discipline:** TracerTraj-2.5K was originally assumed to be a comparable existing benchmark, but this assumption was checked directly (not re-asserted from AgenTracer's own citation of itself) and found wrong — the repo has no LICENSE file and states data/weights are only "committed to" release upon paper acceptance (R11).
- The reproduction claim was corrected to rest on Who&When alone until AgenTracer's actual release, and the TracerTraj comparison point was downgraded from committed to conditional across plan doc §4 and §8/§11.

**POC status**

- Partial real evidence — Spike 2 and Spike 3 (the mechanism, on a toy workflow) resolved; scale-up to 500–1,000 traces across the full task-source pipeline scoped for FYP-2, not yet run.
- **A real, honestly-abandoned attempt worth naming:** self-generating a ~2,000-row TracerTraj-style dataset via AgenTracer's own published pipeline (MetaGPT) against a local free model — real infrastructure work, two real bugs found and fixed (MetaGPT's eager vendor-SDK imports; Ollama's actual `/api/chat` endpoint), abandoned once real pilot timing data showed the full run would take multiple days of continuous local compute, stopped on explicit instruction rather than left running (R11b).
- This is recorded as a legitimate "tried, measured, and honestly stopped" data point, not a silent failure.
- Owned by the Data/Benchmark Owner role.

### 5.2.3 Culprit Agent

**What it is**

- The renamed agent-identification half of ErrorProbe's real Strategist stage — a hypothesis about *which agent* in a multi-agent trace is responsible for an observed failure.
- Part of FR2's output: "output a predicted responsible agent, step, and confidence score for an observed failure."

**How it works mechanically**

- Built on ErrorProbe's published methodology, reproduced (own implementation, since ErrorProbe's license for code reuse is unconfirmed, per plan doc §11) as the algorithmic foundation for backward causal tracing through the execution graph.
- Confidence scoring for this hypothesis is computed from graph features — out-degree, betweenness centrality, matching GraphTracer's own formula — not "ask the LLM how confident it is," keeping the scoring step at 0% API-dependence.
- The hypothesis-generation step necessarily involves LLM reasoning about the trace, consistent with reproducing ErrorProbe's own architecture, which is itself LLM-heavy by design as a baseline reproduction — not claimed as Granite's own novel logic.

**Why it's foundational, not an extension**

- One-third of the core attribution algorithm's real architecture; without it there is no answer to "which agent" at all.
- Removing it, per the team-ownership table, means "The core attribution algorithm and the silent-failure detection claim" disappear — grouped with Error Step Localization and Verification Agent as the item whose removal costs the Diagnosis Engine Owner's entire subsystem.

**Precedent-check result**

- "Present, partially — ErrorProbe (paper), LangSmith Engine / Arize Alyx (commercial) — Granite extends it to unseen architectures" (PDF §6a).
- An honest, non-overclaiming statement: ErrorProbe already does agent-level attribution on the architectures it was tested on; LangSmith Engine and Alyx gesture at something adjacent commercially, though undocumented at this specificity.
- What's not found anywhere is agent-level attribution tested on an architecture absent from the method's own benchmark construction — the specific, narrow claim Culprit Agent makes.

**POC status**

- Real evidence via Spike 1 under its prior bundled name — a simplified 2-stage (Strategist→Arbiter) reproduction against 8 real downloaded Who&When-Hand-Crafted cases, local 3B model.
- **75% agent accuracy**, 12.5% step accuracy (discussed under Error Step Localization below), 0 parse failures.
- Explicitly a *simplified* reproduction — no tool-grounded Investigator, no Verified Episodic Memory.
- The plan doc's own top FYP-1 priority (Weeks 6–10) is building the full 3-stage version on a stronger backbone, since the simplified version at 12.5% step accuracy is nowhere near ErrorProbe's own reported 59.5%.
- Owned by the Diagnosis Engine Owner role.

### 5.2.4 Error Step Localization

**What it is**

- The renamed step-identification half of the same Strategist stage — a hypothesis about *which step* within the trace is responsible, the other half of FR2's output.

**How it works mechanically**

- Same mechanism as Culprit Agent — same Strategist-stage hypothesis generation, same graph-feature-based confidence scoring — applied to step granularity rather than agent granularity.
- Backward causal tracing is pure graph traversal (BFS from the failure node through the dependency graph), per the plan doc's external-component table, at 0% API-dependence for the traversal logic itself.

**Why it's foundational, not an extension**

- Step-level localization is strictly harder and more specific than agent-level localization: knowing *which agent* is responsible narrows the search space, but an operator debugging a real production failure needs the exact originating point, not just a suspect agent.
- The feature-to-CCP-mapping table names this distinction precisely: Culprit Agent maps to "On-call engineers / SREs diagnosing a production multi-agent failure," while Error Step Localization maps to "On-call engineers / SREs needing the exact origin point, not just the responsible agent."

**Precedent-check result**

- "Present, partially — same precedent as Culprit Agent (both are outputs of the same 3-stage pipeline); no paper or platform reports step-level accuracy above 59.5%" (PDF §6a).
- This is the sharpest available evidence that step-level attribution remains genuinely unsolved at the field's current best: even ErrorProbe, the strongest published method, tops out at 59.5% — the best anyone has published still gets step-level attribution wrong more than four times in ten, a number the problem statement (§0.1) cites directly as evidence of "no obvious solution."

**POC status, reported without softening**

- Same Spike 1 run as Culprit Agent, but this is the harder-hitting number: **12.5% step accuracy (1 of 8 cases)**.
- This followed a real scoring bug found and fixed mid-session: the ground-truth `mistake_step` field in the downloaded dataset was stored as a **string** ("5"), while the LLM's parsed JSON output was an **int** (5) — `int == str` silently evaluated `False` for every case until the type mismatch was caught by directly printing both fields' types.
- A genuinely low number on a simplified, un-tool-grounded pipeline, reported as a real, honest baseline data point: "real signal the approach works, not proof the full pipeline hits 59.5%" (R1) — neither hidden nor spun.
- Owned by the Diagnosis Engine Owner role.

### 5.2.5 Verification Agent

**What it is**

- The renamed tool-grounded verification half of ErrorProbe's real Investigator stage — evidence-grounded confirmation of a Culprit Agent / Error Step Localization hypothesis against the real trajectory, before the Arbiter (ErrorProbe's third stage) commits to a final diagnosis.
- Also applied downstream, independently, to gate a *repair* rather than an initial diagnosis, per the survey's own step 6 ("Test candidate repairs using deterministic checks, sandbox execution, test cases or evaluator constraints").

**How it works mechanically**

- This stage's whole purpose is to check a hypothesis against real evidence in the trajectory rather than accept it on the strength of the hypothesis-generation step's own confidence.
- Explicitly tied to a Mid-1 priority: "the full 3-stage ErrorProbe reproduction (tool-grounded Investigator + Verified Episodic Memory) on a stronger backbone" is the top-priority item for Weeks 6–10 — precisely because Spike 1's simplified 2-stage version (no tool-grounded Investigator at all) is what produced the 12.5% step-accuracy number. The missing Investigator stage is a direct, named suspect for that gap, not an assumption.

**Why it's foundational, not an extension**

- The third of the three real pipeline stages the 2026-08-23 rename split out.
- Without it, a hypothesis from Culprit Agent / Error Step Localization is never checked against real trajectory evidence before being reported as a diagnosis — a hypothesis never cross-checked is closer to a guess than a diagnosis.

**Precedent-check result**

- "Present, partially — this is ErrorProbe's own tool-grounded Investigator stage, reproduced not invented; no commercial platform does evidence-grounded hypothesis verification before committing to a diagnosis" (PDF §6a).
- Notably candid: openly labeled "reproduced not invented" rather than presented as if Granite designed the Investigator concept independently, consistent with plan doc §4.1's defense.

**POC status — the one honest gap in the original three-way split**

- This is the one stage of the original split whose *full* version (tool-grounded, as opposed to Spike 1's simplified 2-stage pipeline) has **not yet been run**.
- Spike 1 explicitly omitted the tool-grounded Investigator, so Verification Agent's real behavior remains untested pending the Weeks 6–10 full-pipeline build.
- Stated plainly here rather than implied: Verification Agent shares Spike 1's partial evidence status in name only — the specific mechanism this item names (tool-grounding) is the named gap the next build phase exists to close.
- Owned by the Diagnosis Engine Owner role.

### 5.2.6 Repair Agent

**What it is**

- Generates a targeted correction — a prompt, tool argument, structured output, or function logic — for the localized, verified failure, feeding the candidate value FR4 already assumes exists.
- Added 2026-08-24 as foundational item #6, sourced directly from the survey's §6.1 step 5.

**How it works mechanically**

- Given the evidence already gathered by Culprit Agent, Error Step Localization, and Verification Agent, Repair Agent's job is narrowly scoped per the survey's own §7 scope-control principle, adopted directly: "targeted modification of prompts, tool arguments, structured outputs or small code functions; do not attempt unrestricted rewriting of the entire agent architecture."
- Necessarily involves an LLM call — this is the re-generation half of the pipeline, distinct from the deterministic-by-design injection/tracing/scoring components — classified in the plan doc's external-component table as inherent API-dependence, "small (one call per candidate fix tested)."

**Why it's foundational, not an extension**

- FR4 already assumes this input exists, and nothing else in the prior list produced it — a genuine, previously-unnoticed hole in the pipeline's own functional requirements, not a nice-to-have gap.
- Without it, Verified Automatic Repair has nothing to verify — the whole downstream repair-and-recovery half of the pipeline (foundational items #8, #9, #10) has no candidate value to act on.

**Precedent-check result**

- "Not found as a native capability anywhere — a 7-framework orchestration survey... rates 'automatically generate repair' as Not native / Custom / Experimental across all 7; closes the gap between diagnosis and Verified Automatic Repair, which previously assumed a candidate fix was given, not generated" (PDF §6a).
- One of the clearest flat "not native anywhere" findings in the whole feature list.

**POC status, with the real numbers stated plainly**

- POC run the same day it was added: **Spike 8**, `poc_spike8_repair_agent.py`.
- **repair_success_rate = 0.667 (4/6)**, **exact_match_rate = 0.667 (4/6, the same four cases)**, 0 parse failures, local 3B model, n=6 synthetic single-step correction cases.
- Each generated fix chained into Spike 5's existing replay logic — the test checks whether the generated fix actually *recovers a passing outcome* when re-executed, not merely whether it matches ground truth textually.
- **The two failures are not two unrelated problems — they share one precise root cause**, and this is a genuinely useful, actionable result, not a vague "needs more work":
  - In both failing cases (`loyalty_discount`, `notebook_order`), the model correctly extracted the right underlying fact from the given evidence (a 15% discount, 7 notebooks) but returned the *downstream computed result* ($6.75, $28.00) instead of the *specific atomic parameter* (15, 7) the pipeline actually needed.
  - This is a specification/interface ambiguity in what "corrected_value" means — not a reasoning failure.
- **The actionable fix, already identified:** Repair Agent's real interface must pin down exactly which atomic field is being corrected, the same way Error Step Localization already pins down a specific step index, rather than leaving "the corrected value" ambiguous between a parameter and a derived result.
- Owned by the Diagnosis Engine Owner or Platform Owner role (not yet formally assigned between the two, since Repair Agent sits at the boundary of diagnosis and the repair/recovery pipeline).

### 5.2.7 Semantic Error Diagnostic

**What it is**

- Task-constraint verification catching outputs that are well-formed but semantically wrong — the renamed "silent-failure verification" module.
- The mechanism behind FR3: "The system shall flag an output that passes standard error checks but violates the task's stated constraints (a silent failure), independent of whether any explicit error signal was raised elsewhere in the trace."
- The project's second headline novelty pillar (RQ3), alongside cross-architecture generalization (RQ2).

**How it works mechanically — three implementation techniques, all standard software engineering**

- Committed explicitly to be rule/schema-based, not LLM-judged. Plan doc's external-component table: "the single most important commitment in this table: if this module is LLM-judged instead, the project's actual differentiator becomes an API call wearing a system architecture."
- **1. Schema and type enforcement:** Pydantic-style structured-output validation, default-deny on unexpected fields.
- **2. Domain-specific rule checks:** logical assertions (unit tests against generated code), boundary checking (a discount price must be strictly less than the original), format verification (exact column counts).
- **3. Execution state tracking:** logging variable state before/after an agent acts, comparing the trace against what should have happened — e.g., a claimed database update with no corresponding tool call is mathematically proven, not merely suspected, to be a silent failure.

**What was considered and explicitly rejected as the detection mechanism**

- Three proposed "novel ML-driven" alternatives, all rejected: embedding-based semantic-drift detection, a multi-indicator confluence of perplexity/latency/semantic-distance anomaly scores, ARIMA time-series anomaly detection.
- Not rejected for infeasibility — rejected for a **category mismatch**: Granite's own definition of a silent failure is an output with *no anomaly signal*, so any detector built on anomaly/drift/statistical-outlier signals structurally cannot catch the exact failure class the module exists to catch.

**Two new complementary strategies proposed instead, still awaiting their own POC spike**

- **Cross-Agent Consistency Verification:** diffing typed facts stated independently by two or more agents about the same entity — a silent failure often shows up as one agent's value silently diverging from another's, even though each individual output looks locally well-formed.
- **Constraint Provenance Tracing:** a graph-based provenance walk checking whether a claimed constraint in the final output ("under budget," "in stock") has a corresponding upstream tool-call/check node that could have verified it — generalizing the "no DB tool called" example into a broader class of claimed-but-unverified constraints.
- Both are still design proposals, not yet POC-tested.

**Why it's honestly labeled non-novel at the technique level, novel only at the assembly-and-measurement level**

- `Silent_Failure_Detection_and_Testing_Strategies.md`'s own honesty-check table cross-references every implementation technique against the seven Layer-1 commercial platforms and finds every one already present somewhere in the market as standard practice.
- Schema/type enforcement: "standard software engineering, used across the entire industry, not agent-specific at all."
- Execution state tracking: "confirmed the *core competency* of every commercial platform checked... actually the least differentiated thing on this whole list."
- Stated conclusion: "none of these building blocks are the differentiation claim... The actual differentiation... is in what these common building blocks are assembled into and measured against" — a formally benchmarked silent-failure-detection capability with labeled ground truth, feeding into automated root-cause attribution, feeding into Verified Automatic Repair with a measured recovery rate, proven on architectures no prior paper tested.

**Why it's foundational, not an extension**

- This is RQ3, one of the project's two lead research claims — removing it would eliminate the specific gap ErrorProbe itself admits, in writing, in its own limitations section, that it cannot close.
- Plan doc §15 names this specifically: targeting "a gap ErrorProbe *itself* admits, in writing, that it cannot close... not a gap we inferred."

**Precedent-check result**

- "Present, partially — Maxim AI / DeepEval do a narrower version (RAG-groundedness only) — Granite is general, task-constraint-based, and adds 2 new cross-referencing strategies" (PDF §6a).

**POC status**

- Spike 4 ran two real things:
  - An n=3 real LLM task run — the model got all 3 correct, so no natural silent failure occurred to test detection on. An honest limitation, not a hidden one.
  - A direct mechanism test decoupled from LLM behavior, feeding the rule-based checker known-wrong values, including a plausible-magnitude near-miss ($20.00 vs. $19.75 true) — the checker correctly flagged every known-wrong value and correctly passed every correct value, **zero false positives**.
- Real, validated mechanism evidence; the empirical frequency of natural silent failures "in the wild" remains genuinely open — n=3 cannot establish it either way (R10).
- Owned by the Diagnosis Engine Owner role.

### 5.2.8 Verified Automatic Repair

**What it is**

- The renamed "counterfactual replay engine" — deterministically re-executes downstream with Repair Agent's candidate fix and reports a measured recovery rate before the fix is trusted.
- FR4 verbatim, committed-core line 5.

**How it works mechanically**

- Deterministic re-execution of the downstream portion of a trace, given a corrected value for a specific upstream step — pure counterfactual replay, not a second LLM judgment call on whether the fix "looks right."
- The re-execution step itself necessarily involves an LLM (re-running the corrected step to observe the outcome), classified as "inherent, small (one call per candidate fix tested)" rather than counted against the 15–20% budget as if it were a discretionary design choice.

**Why it's foundational, not an extension**

- This is what makes "verified" in Verified Automatic Repair an honest word rather than marketing language — the mechanism that actually tests whether a candidate correction works before a team is asked to trust it.
- Precisely item #2 on the list of five things none of the seven Layer-1 commercial platforms confirm doing publicly (§4.1.7).
- Removing it collapses the entire recovery half of the pipeline's claim to trustworthiness.

**Precedent-check result**

- "Not found — no paper or platform tests a fix with a measured recovery rate before applying it (GitHub Copilot Autofix re-scans static code with CodeQL, a different mechanism for a different failure class — see §7 note)" (PDF §6a).
- The named comparison to GitHub Copilot Autofix shows the precedent check going one step further than a blanket "not found" — actively considering the closest-sounding adjacent tool and explaining precisely why it doesn't count as precedent.

**POC status, with the real numbers**

- **Had zero POC evidence at all** until a cross-check against the frozen list surfaced the gap in the third session (2026-08-22) — a real finding worth naming: 4 of 5 foundational items at that point had direct evidence; this one didn't, and it wasn't caught until an explicit alignment check ran.
- Spike 5, run the following session to close the gap: a deterministic 3-step pipeline injects a corrupted step1 value, then deterministically re-executes steps 2–3 after correcting it.
- Result: `recovery_success: true` — the corrupted trace's final output (97.2, expected 108.0) recovered to 108.0 after replay.
- Stated as real but explicitly narrow evidence, per the script's own docstring: it tests only the mechanical replay-and-recompute logic on a toy pipeline, not whether an LLM can correctly *guess* a fix in the first place (that's Repair Agent's separate, later-tested concern).
- A real recovery-rate measurement on the actual benchmark, rather than this toy pipeline, is still owed.
- Owned by the Platform Owner role.

### 5.2.9 Recovery Controller

**What it is**

- Applies a verified repair and resumes execution from a safe checkpoint, instead of restarting the whole workflow — the survey's own step 7.
- Added 2026-08-24, initially as extension #9, reclassified into foundational item #9 the same day.

**How it works mechanically**

- Needs checkpoint-based state saving and restoring, which nothing else in the prior list provides — explicitly distinct from Verified Automatic Repair, which currently proves deterministic re-execution but does not save/restore intermediate execution state at a checkpoint.
- Formally resolves the "Checkpointing" item that had sat open, deliberately unadded, since 2026-08-23 — acknowledged at the time as genuinely distinct from Verified Automatic Repair, but never run through the CCP/market/academic-overlap filter every other item received, so it stayed parked rather than added speculatively.

**Why it's foundational, not an extension**

- The survey's own Table 1 rates "resume from repaired point" as "Core" for the Proposed FYP column, the same tier as five other rows Granite already treats as foundational.
- Leaving Recovery Controller as an extension would have been inconsistent with the very classification scheme this project relies on to justify the rest of the list.

**Precedent-check result, stated honestly rather than smoothed into a flat "not found"**

- "5 of 7 surveyed frameworks have generic checkpoint/resume infrastructure (LangGraph, CrewAI, Microsoft Agent Framework: checkpoint-based; Google ADK, Amazon AgentCore: partial), but none tie resumption specifically to a verified-repair point, which is what this item needs" (R21).
- A precise, non-overclaiming precedent statement: generic checkpoint/resume infrastructure is common and reused, not claimed as novel; what's genuinely absent everywhere is the specific *tying* of resumption to a verified-repair checkpoint rather than an arbitrary interruption point.

**POC status — stated plainly as an honest open risk, not softened**

- "No POC yet — genuinely new mechanical work, not a rename of something already tested" (plan doc §7.0, item #9).
- **One of only two items in the entire 20-item list with zero POC evidence of any kind** (the other, Verified Repair Memory, has evidence but a failed result).
- Both R21's own status line and the ninth AI-usage-log session are explicit this remains an open risk: "the clear gap to close before Mid-1, alongside R22's VRM re-test below."
- Named here without euphemism, exactly as required: Recovery Controller is foundational item #9, and it has never been tested in any form.
- Owned by the Platform Owner role.

### 5.2.10 Verified Repair Memory

**What it is**

- Stores successful error→diagnosis→repair patterns and retrieves them for similar future failures — the survey's own step 8.
- Re-added 2026-08-24 by explicit user decision, then reclassified into the foundational core the same day.

**How it works mechanically, and its real history — stated plainly because it is now foundational, not despite it**

- Not a fresh, unproven idea — it already has one real test, and that test failed.
- Built once as "Verified Episodic Memory" on 2026-08-23, in `poc_spike1b_full_pipeline.py`, as part of a full 3-stage pipeline prototype — a file since deleted at explicit user instruction, meaning the code itself no longer exists on disk; the risk-register entry (R18) is the only remaining record it was ever built.
- Run on all 8 real Who&When test cases, the result was unambiguous: **0 of 8 cases ever committed anything to memory.**
- Reason: **all 24 hypothesis-verifications across those 8 cases came back `NOT_SUPPORTED`** on the local 3B model backbone used — the mechanism never once found evidence it judged sufficient to commit a diagnosis to memory, at any point across all 8 test cases.
- In the same run, agent-level accuracy also **regressed, from 75% down to 50%** versus Spike 1's simpler 2-stage version — a real degradation, not just a null result, worth stating explicitly since it means adding this mechanism, at least in that specific implementation and on that specific weak local backbone, made the simpler baseline's own accuracy worse, not merely failed to improve it.

**A second, distinct failure worth naming alongside the technical one**

- This finding was supposed to be logged to `risk-register.md` at the time it happened; the edit attempt failed silently and was never retried.
- There was no record anywhere that this mechanism had been built, tested, and reverted, until the market-survey session surfaced the gap and the history was finally written down properly as R18.
- A small but real process failure the project's own documentation is honest about, rather than quietly correcting the record without acknowledging the gap existed.

**The decision to keep it in the core anyway**

- Despite that one real test's clear failure, the mechanism was **committed to the foundational core anyway**, on an explicit condition: a re-test on a stronger LLM backbone happens before Mid-1.
- If the re-test also fails, plan doc language is direct: "this is a foundational-item gap the team must be ready to explain under questioning (Section 14.1), not a footnote."

**Why it's foundational, not an extension**

- Exactly like Recovery Controller, the survey's own Table 1 rates "remember successful repairs" as "Core" for the Proposed FYP column — the same tier as five other already-foundational rows.
- Leaving it as an extension would have been the same kind of inconsistency Recovery Controller's reclassification corrected.
- The reclassification itself is explicitly documented as "a scope decision, not new evidence" (R22) — the evidence is unchanged from R18; only the item's place in the list moved.

**Precedent-check result**

- "Not found — the market survey itself rates 'remember successful repairs' as 'Under-served' across all 7 frameworks. Re-added by explicit user decision after one real test already failed (0/8 commits, local 3B backbone)" (PDF §6a).
- This precedent statement names the failed test in the same breath as the market-gap finding — the two facts are presented together, not separately, so a reader can't mistake "not found in the market" for "proven to work."

**POC status, stated without euphemism**

- One real test, one real failure, carried forward unmodified by the reclassification into foundational status.
- Alongside Recovery Controller's total lack of evidence, this is the honest open-risk pairing that must be stated plainly rather than softened: **two of the ten foundational items — a fifth of the actual research claim — currently rest on either zero evidence or a documented failed result**, committed to the core by explicit decision rather than by a clean validation record.
- Owned by the Diagnosis Engine Owner or Platform Owner role (boundary item, same ambiguity as Repair Agent, not yet formally assigned).

---

## 5.3 The eight extensions, each in full

*Extensions are explicitly gated behind the ten foundational items working first — plan doc §7.0's own header states this as a rule, not a suggestion: "build these, in this priority order, only after the 10 foundational items work." Priority order below is unchanged from §7.0.*

### 5.3.1 Widen fault taxonomy (3 total types)

**What it is**

- Extends the fault-injection harness from its POC-validated single fault type (corrupted tool output) to three total distinct types: communication corruption (swap a passed value between agents for a plausible-but-wrong one) and context truncation (drop the last N% of upstream context before the next agent sees it), each a distinct injection operator with its own ground-truth label.
- Notably, the plan doc records a correction to an earlier draft that double-counted "tool-response corruption" as a fourth type when it's actually the same family as the POC's already-validated corrupted-tool-output fault — a small but real instance of the project catching its own miscounting before it became a settled inaccuracy.

**How it works**

- Same mechanism as the base harness — rule-based, deterministic corruption operators, 0% API-dependent — applied to two new injection points (inter-agent message content, upstream context length) rather than the single point (tool output) already validated.

**Why it's an extension, not foundational**

- Supporting infrastructure that widens the existing benchmark's coverage rather than adding a new research claim.
- The generalization and silent-failure claims don't depend on having three fault types instead of one; they depend on the mechanism working at all, which is already foundational item #1's job.

**Precedent-check result**

- "Supporting infrastructure — no separate precedent needed" (PDF §6b) — the one extension item explicitly exempted from an individual novelty check, since it's a scaling-up of an already-checked mechanism rather than a new one.

**Priority-order reasoning**

- First extension, Weeks 1–6 of FYP-2 — scheduled early because it's low-risk, mechanically similar to already-proven work, and directly strengthens the benchmark other extensions and the core evaluation depend on.

### 5.3.2 3rd architecture

**What it is**

- Instruments a third previously-unused multi-agent architecture — OpenAI Agents SDK, or a fully custom in-house framework — extending the generalization claim from 2 to 3 architectures spanning different orchestration paradigms.

**How it works**

- Same fault-injection and trace-capture mechanism already proven on CrewAI (Spike 2), applied to a new framework's own message-passing and tool-call semantics.

**Why it's an extension, not foundational**

- The generalization claim (RQ2) is already satisfied at the level the CCP rating requires with two previously-unused architectures — a third strengthens the claim's robustness but is not required for the claim to exist and be defensible.

**Precedent-check result**

- "Extends the same generalization claim — not a new concept" (PDF §6b) — like fault-taxonomy widening, no independent novelty check, since this scales an already-validated claim.

**Priority-order reasoning**

- Second extension, Weeks 1–6, paired with fault-taxonomy widening as the two earliest, lowest-risk, most benchmark-strengthening extensions.

### 5.3.3 Cyclic/dynamic graph support

**What it is**

- Extends the execution-graph data model from a DAG to a general directed graph with cycle detection, defining a max-revisit bound so backward causal tracing terminates on a loop, validated against at least one benchmark trace containing a real loop.

**How it works mechanically, with real numbers**

- Backward traversal with a per-node revisit bound.
- **Spike 6 tested two real cases and a deliberate control:**
  - An unrolled retry loop — terminated cleanly, all nodes reached.
  - A true cycle, Researcher↔Critic — terminated cleanly with the bound in place, Researcher visited 3x / Critic 4x as expected.
  - **Control run, bound effectively disabled:** the important part of the evidence, not a footnote — this case **hit the 10,000-step safety cap instead of terminating**, direct positive proof the revisit bound is load-bearing (actually preventing infinite traversal), not a no-op that happened to pass because the test cases were too easy to expose its absence.

**Why it's an extension, not the core DAG model — and why it's justified from inside the core, not from outside pressure**

- The core generalization claim only strictly requires the graph model to represent whatever structure the benchmark's actual traces contain, and a DAG suffices for initial benchmark construction.
- But the justification for building this at all is not borrowed from outside: "not a borrowed feature — LangGraph (one of our own 2 committed core architectures) natively supports cyclic workflows (retry loops, iterative refinement), so without this, Granite's own cross-architecture claim would be incomplete on the very framework it commits to instrumenting."
- Worth flagging precisely because this is a case where an "extension" is justified by an already-committed core claim's own internal consistency, not by external market pressure.

**Precedent-check result**

- "Not found — PROTEA (2026) names static-DAG-only as its own future work, unbuilt" (PDF §6b) — cited explicitly as context, not a comparison claim, since PROTEA has no public benchmark or code to compare against; this only shows the gap is independently recognized elsewhere.

**Priority-order reasoning**

- Third extension, Weeks 1–6, grouped with the two architecture-generalization extensions because it's mechanically necessary for LangGraph's own native retry-loop pattern, not purely a nice-to-have added late.

### 5.3.4 Confidence calibration

**What it is**

- Computes and reports a reliability diagram plus Brier score for the diagnosis engine's confidence output across the full benchmark, published as an evaluation artifact.

**How it works**

- A standard calibration-evaluation technique applied to Granite's own confidence scores — comparing stated confidence against actual correctness rate across many predictions, to determine whether "80% confident" predictions are actually right about 80% of the time.

**Why it's an extension**

- A quality-of-evidence measurement layered on top of the already-foundational confidence-scoring mechanism inside Culprit Agent and Error Step Localization.
- The core attribution claim doesn't depend on the calibration being *published as a diagram*, only on confidence scores existing at all, which they already do.

**Precedent-check result**

- "Not found — no paper or platform publishes a calibration study for this task" (PDF §6b).

**Priority-order reasoning**

- Fourth extension, Weeks 6–8, alongside the two-mode latency/accuracy trade-off work behind Granite's own measurable NFR (diagnostic overhead under 50% for single-pass mode, §0.07) — both evaluation-rigor extensions scheduled once the core pipeline is stable enough to measure meaningfully.

### 5.3.5 Preventive clarification classifier

**What it is**

- A lightweight binary classifier (explicitly not RL) trained on labeled clean-vs-corrupted message-handoff pairs from the fault-injection benchmark, flagging "ask a clarifying question here" at each agent handoff, with precision/recall reported on catching corrupted handoffs before propagation.

**How it works, with the real number stated honestly**

- Spike 7 tested TF-IDF + logistic regression on n=20 hand-written clean/corrupted handoff pairs (n_test=8).
- Result: **precision 0.25, recall 0.25, f1 0.25 — near-random, not a working classifier yet.**
- Reported without smoothing, in both the risk register and the AI usage log, as a genuinely weak, honest negative-leaning result.
- Two likely causes named as the next things to test, not treated as proof the approach is dead:
  - n=20 hand-written examples may be too small and unrepresentative of real corruption patterns — the real test needs labeled pairs from the fault-injection harness itself, not hand-authored ones.
  - Bag-of-words (TF-IDF) features may genuinely be too weak for this task, in which case cheap local sentence-embedding features (still zero API cost) are the next thing to try before concluding the classifier needs to be heavier than "lightweight."

**Why it's an extension, and explicitly contingent, not automatic**

- The FYP-2 timeline states this precisely: "**contingent, not automatic**: spike 7 showed near-random signal on hand-written data; before committing this slot, re-test with real labeled pairs from the fault-injection harness (built Weeks 1–6) and cheap local sentence-embedding features — if it still doesn't improve, drop it rather than ship a known-broken classifier."
- One of the clearest instances anywhere in the feature list of a stated decision rule for abandoning an extension if the evidence doesn't improve, rather than shipping a known-weak mechanism just because it's on the list.

**Precedent-check result**

- "Present, partially — AgentAsk (paper) does an RL-trained version — Granite's is a lighter, supervised version" (PDF §6b).
- The one extension explicitly compared against a specific paper, named as context for the underlying need being real and independently recognized — not a benchmarked comparison, since AgentAsk has no public dataset or code available.

**Priority-order reasoning**

- Fifth extension, Weeks 8–14, scheduled after the fault-injection harness has been widened (Weeks 1–6) so its re-test can use real harness-generated labeled pairs instead of the hand-written data Spike 7 was limited to.

### 5.3.6 Failure Propagation Map

**What it is**

- A stored-query and chart over the diagnosis-record database, plotting failure-type distribution per agent-version tag across runs — built entirely from data the diagnosis engine already produces.

**How it works**

- Pure data visualization over already-computed diagnosis records — no new detection or attribution logic, just aggregation and charting of existing output.

**Why it's an extension**

- Purely additive product polish on top of data the foundational pipeline already generates; nothing about the core research claims depends on this visualization existing.

**Precedent-check result**

- "Present broadly — most commercial platforms do some trace visualization — least differentiated item on the list" (PDF §6b).
- The single most candid, least-defensive precedent statement anywhere in the feature list — explicitly naming this as the *least* differentiated item, rather than stretching to find a novel angle for a genuinely commodity capability.

**Priority-order reasoning**

- Sixth extension, Weeks 8–14, grouped with Explainable Confidence Reasoning as dashboard/platform-polish extensions scheduled "only if core is stable."

### 5.3.7 Explainable Confidence Reasoning

**What it is**

- Surfaces the evidence behind a confidence score — not just the number itself, but which graph features and which verification evidence contributed to it.

**How it works**

- Built on top of the already-foundational graph-feature-based confidence scoring (out-degree, betweenness centrality) — this extension exposes the components of that computation to a human reader, rather than only the final scalar.

**Why it's an extension**

- The core attribution claim only requires a confidence score to exist and be reasonably calibrated (Confidence Calibration's job); explaining *why* a given score was produced is a trust/usability layer, valuable for the product story but not required for the research claim.

**Precedent-check result**

- "Not found — no paper or platform surfaces the evidence behind a confidence score" (PDF §6b).

**Priority-order reasoning**

- Seventh extension, Weeks 8–14, alongside Failure Propagation Map — "only pursued if core is stable," same explicit contingency language.

### 5.3.8 Framework Compatibility Layer

**What it is**

- Draws capabilities and evidence from all seven surveyed orchestration frameworks — OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI — rather than narrowing to a single one as the survey's own §7 recommends.
- Added 2026-08-24 as the last extension.

**How it works, and how it's deliberately scoped lighter than the core**

- Distinct from the foundational cross-architecture benchmark: the committed core's 2–3 frameworks get *full* fault-injection and benchmarked evaluation; this extension only confirms the diagnosis pipeline can instrument and parse execution traces from each remaining framework, without building a full fault-injection benchmark for each.
- Plan doc's own language: "Broad *compatibility*, not broad *benchmarking* — building full benchmarks on all 7 would roughly double the core's engineering workload for a one-year BS project (risk-register.md R8: breadth-over-depth)."

**Why it's an extension, not foundational, despite being the direct positive resolution to a rejected piece of market-survey advice**

- The research claim (RQ2) only requires generalization to be demonstrated and rigorously benchmarked on 2–3 architectures — extending lightweight compatibility to the other five strengthens the product's real-world adoptability without being required for the CCP claim itself to hold.

**Precedent-check result**

- "Not found — no framework or platform confirms lightweight execution-trace instrumentation compatibility across all 7 surveyed orchestration frameworks at once" (PDF §6b).

**Priority-order reasoning**

- Eighth and last extension, gated behind the core "same as every other extension; no POC yet" — the last item added to the list (same day as Recovery Controller and Verified Repair Memory, but staying an extension rather than being reclassified, since nothing in the survey's own Table 1 rates broad framework compatibility itself as "Core" the way it rates the two capabilities Recovery Controller and Verified Repair Memory implement).

---

## 5.4 The two deprioritized items — why parked, not planned

**What they are**

- **Cross-Domain Transfer Testing** and **Chaos Testing for Agents** — the two items the plan doc labels, deliberately, "not planned, not 'if time allows,' genuinely parked."

**How they were handled differently from every other item on the list**

- Both were part of the original 13-item extension brainstorm and were filtered out *before* the five-rule extension-survival filter was even applied to the surviving seven — meaning neither received the same individual precedent-check treatment the eight active extensions did.
- The PDF's own §6c: "Parked before CCP/market filtering — no precedent check run" for both.
- The summary language in §6 is explicit: "no precedent claim is made either way for them" — a deliberate absence of a claim, not a claim of absence.

**Why parked rather than dropped entirely**

- Both are legitimate, real product capabilities: testing whether a diagnosis engine trained/tuned on one task domain transfers to another; stress-testing production resilience via injected chaos beyond controlled fault injection.
- Both simply don't fit inside a one-year BS project's already-full scope once the ten foundational items and eight extensions are accounted for.
- Plan doc's own instruction: "Revisit only if FYP-2 is materially ahead of schedule; do not plan around them."
- A real scope-discipline decision, not a soft aspiration — nothing in the FYP-2 timeline allocates any week to either item, and no risk-register entry tracks either as an open risk, since neither is committed to anything that could fail.

---

## 5.5 Items considered and explicitly rejected

### 5.5.1 Automatic Retry

**What was proposed**

- Unconditional auto-retry of a failed step, considered 2026-08-23, the same session as the 5→7 foundational rename.

**Why it was rejected**

- Contradicts an already-committed principle — extension #12 in the original 13-item extension list gates auto-suggested fixes behind a confidence threshold, on the stated ground that "no team will trust an auto-remediation tool that silently applies fixes with no visibility into how sure it is."
- Unconditional retry would violate that principle by design (retrying doesn't check confidence first).

**What replaced it**

- The defensible version of the underlying idea already exists, just not as a separate feature: it's Verified Automatic Repair (foundational item #8) and Confidence Calibration (extension #4) working together — retry only fires once a fix is already verified and confidence-gated.
- Recorded explicitly as "a behavior of two existing mechanisms, not a standalone item" — a deliberate distinction between "this need is real" and "this need requires new code."

### 5.5.2 Single-framework scope narrowing — the feature-list-specific angle

**Why this section exists separately from Part 4's coverage**

- Covered in full in Part 4 (§4.5.2) from the market-positioning angle. The feature-list-specific angle is a different lens on the same decision: what it would have meant for the 20-item list itself, concretely.

**What would have been lost, concretely, from the feature list**

- **Cross-architecture benchmark** (foundational item #2) would collapse to a single-framework benchmark, no longer testing generalization at all.
- **The 3rd-architecture extension** (§5.3.2) would have no meaning, since there would be no 2nd architecture to extend from.
- **Framework Compatibility Layer** (§5.3.8) — the positive resolution the project built specifically in response to this same advice — would never have been conceived, since it exists specifically as an answer to a question the single-framework narrowing itself created.

**The sharper point this angle makes**

- Following the advice wouldn't just shrink the list by removing items — it would have prevented one item (Framework Compatibility Layer) from ever being invented in the first place.
- The rejection reasoning is the same as §4.5.2: it would eliminate RQ2, one of two lead research claims, already CCP-justified and partially tested before this survey was ever read.

---

## 5.6 The "self-improve from prior failures" gap — flagged honestly as undecided

**What this row is**

- The one row from the market survey's own Table 1 that genuinely does not map onto any current Granite feature, foundational or extension — deserving to be named as a real, open gap rather than folded silently into Verified Repair Memory, which is the closest-sounding but distinct item.

**How the survey itself treats this row differently from the other eight**

- Table 1's row 19, "Self-improve from prior failures," is rated "Experimental" for BabyAGI and "Partial/custom" for the other six frameworks.
- Distinctively, the Proposed FYP column is rated **"Verified/controlled,"** not "Core," unlike every one of the eight rows discussed in §5.1.4 and §4.3.1 above.
- This is the survey's own signal that it does not consider this row settled by the recommended module list the way it considers the other eight settled — "Verified/controlled" reads as a qualified aspiration (if a system does this at all, it should do so only under verification and control), not a claim that Granite's proposed scope closes this gap outright.

**Why it's distinct from Verified Repair Memory, stated precisely**

- Verified Repair Memory stores and retrieves *specific, previously-verified* repair patterns for *similar* future failures — a targeted, bounded, retrieval-based mechanism.
- "Self-improve from prior failures" as a general capability implies something broader: the system's own diagnosis or repair *logic itself* getting measurably better over time from accumulated experience, not just a growing library of specific reusable patches.
- Nothing in the current 20-item list — not Verified Repair Memory, not any extension — commits to building or measuring general self-improvement of the diagnosis logic itself.

**Where this leaves the project, stated without resolution**

- This gap is flagged here, honestly, as undecided rather than resolved or quietly ignored, consistent with the document's own standing practice of naming what remains open rather than implying full coverage.
- It is not currently scoped as a foundational item, an extension, or even a deprioritized item — it sits outside the 20-item list entirely, a genuine unaddressed row in the survey's own comparison table that the project has not yet made a decision about one way or the other.

---

## 5.7 Five concrete use cases — what existing tools miss, what Granite catches

*Reproduced and expanded from `generate_supervisor_pdf.py` §7. Each scenario is tied to a specific foundational item and names the exact gap in the seven checked Layer-1 platforms it closes. This is deliberately placed in Part 5, not Part 4, because each scenario's "what Granite does" column is a concrete instance of a foundational item doing its job — Part 4 established the gap exists in the market; this section shows the feature-level mechanism that fills it, scenario by scenario.*

### 5.7.1 Scenario 1 — the plausible near-miss refund

**The scenario.** A support agent states a refund of $58.00 when the correct value, computable from the trace's own upstream data, is $61.75 — a plausible near-miss, not a crash, not a malformed output, not a missing tool call.

**What existing tools do.** LangSmith, Langfuse, Braintrust, Arize all show a clean trace — no error, no anomaly, no low-confidence flag — because nothing about the output looks wrong. This is the textbook silent failure: every infrastructure-level and schema-level check passes.

**What Granite does.** Semantic Error Diagnostic (rule-based task-constraint verification, validated mechanically in Spike 4) recomputes the expected value from the trace's own data and flags the mismatch, without needing the true answer known in advance — the check is a constraint derived from the trace's own upstream facts, not a lookup against a pre-known ground truth.

**Which foundational item this demonstrates.** Semantic Error Diagnostic (§5.2.7), directly — this is the scenario Spike 4's near-miss test ($20.00 vs. $19.75 true) was modeled on before this use case was written up, meaning the POC evidence and the use-case scenario describe the same underlying mechanism, not two separate claims.

### 5.7.2 Scenario 2 — inconsistent stock counts across agents

**The scenario.** One agent states "12 units in stock," a downstream agent later states "8 units in stock" for the same SKU in the same trace — each individually well-formed, well-typed, and passes its own local schema check.

**What existing tools do.** None of the seven platforms checked cross-reference facts stated by independent agents against each other — each output is scored/traced in isolation, per-node, never diffed against another node's claim about the same entity.

**What Granite does.** Cross-Agent Consistency Verification (one of the two new complementary strategies proposed under Semantic Error Diagnostic, §5.2.7) extracts typed facts per node and diffs them across agents referencing the same entity/field — rule-based, no model call.

**Status, stated honestly.** This is a design proposal, not yet a POC-tested mechanism — it is explicitly listed among the items the team still owes a spike for (§5.7.6 below). Its inclusion as a use case here is a statement of intended coverage, not a claim of validated coverage.

### 5.7.3 Scenario 3 — a claimed constraint with no verifying node

**The scenario.** A final answer states "this recommendation is within your $500 budget," but no upstream tool call in the trace ever queried a price or compared it to that budget — the claim is asserted, not checked, anywhere in the trace.

**What existing tools do.** Schema/type checks pass (the output is well-formed text), so nothing fires — no platform traces a claimed constraint back to a verifying node, because none of the seven maintain a provenance graph linking output claims to the upstream evidence that would substantiate them.

**What Granite does.** Constraint Provenance Tracing (the second of the two new complementary strategies, §5.2.7) walks the execution graph backward from any claimed constraint and flags claims with no verifying node behind them — a graph-based provenance walk over the same execution graph the core data model already builds.

**Status, stated honestly.** Same caveat as Scenario 2: design proposal, not yet POC-tested.

### 5.7.4 Scenario 4 — a team building on a framework the vendor tools weren't tuned for

**The scenario.** A team builds on CrewAI, or on a LangGraph workflow with native retry loops — frameworks LangSmith Engine and Arize Alyx were not tuned for.

**What existing tools do.** LangSmith Engine and Arize "Alyx" (2026) both ship real automated root-cause diagnosis, but locked to their own vendor tracing stack (§4.1.1, §4.1.4).

**What Granite does.** Framework-agnostic by design — proven on CrewAI (Spike 2) and on LangGraph's native retry loops (Spike 6, the load-bearing cycle-safety-bound control case, §5.3.3).

**Which foundational and extension items this demonstrates.** Fault-injection harness and Cross-architecture benchmark (§5.2.1–5.2.2) for the CrewAI half; extension #3, Cyclic/dynamic graph support (§5.3.3), for the LangGraph retry-loop half — a single use-case scenario that spans one foundational pair and one extension, illustrating that the generalization claim isn't confined to one item.

### 5.7.5 Scenario 5 — a confirmed diagnosis with no proposed fix

**The scenario.** A diagnosis is confirmed (Verification Agent has done its job), but nobody has proposed what the actual fix should be, let alone tested whether it would work.

**What existing tools do.** Across all seven orchestration frameworks surveyed, "automatically generate repair" rates Not native / Custom / Experimental — none ship a first-class repair-generation step (§4.3.1.2).

**What Granite does.** Repair Agent generates the targeted correction (prompt, tool argument, structured output, or function logic); Verified Automatic Repair (Spike 5, `recovery_success: true`) then re-executes downstream with it and reports a measured recovery rate before it's trusted.

**Which foundational items this demonstrates.** Repair Agent (§5.2.6) and Verified Automatic Repair (§5.2.8) together — the two-item pipeline that turns a diagnosis into a tested fix, the exact integration the market survey's own core research gap statement names as missing market-wide.

### 5.7.6 What these five scenarios collectively show, and what they honestly don't yet show

- Three of the five scenarios (1, 4, 5) map to mechanisms with real POC evidence already in hand (Spikes 2, 4, 5, 6).
- Two of the five scenarios (2, 3) map to mechanisms that are design proposals only, explicitly flagged as such rather than presented as already validated — a direct instance of the document's standing discipline of distinguishing "considered and rejected" from "designed but not yet tested" from "tested and working."
- All five scenarios are stated against a *specific* commercial-platform gap, not a generic "existing tools are bad" claim — each "what existing tools do" column names the actual checked behavior of specific, real platforms from Part 4, not an assumption about what tools in general must be doing.

---

## 5.8 Every feature, the CCP characteristic it evidences, and who benefits

*Reproduced and expanded from `generate_supervisor_pdf.py` §8. Every one of the 18 active features (10 foundational + 8 extensions) maps to at least one of the nine Seoul Accord CCP characteristics (see Part 1's CCP rating) and a concrete beneficiary — not an abstract "users," but a named role who would actually reach for this specific capability. The two deprioritized items are included at the end for completeness, since the source table includes them too, with the caveat (already stated in §5.4) that they never went through this same filtering rigor.*

### 5.8.1 Foundational items, mapped

| Feature | CCP characteristic(s) | Who benefits |
|---|---|---|
| Fault-injection harness | #3 Depth of knowledge, #5 Beyond standard practice | Benchmark researchers; QA/test engineers validating agent systems pre-deployment |
| Cross-architecture benchmark | #2 No obvious solution, #6 Diverse stakeholders | Researchers comparing attribution methods; teams choosing which framework to trust |
| Culprit Agent | #4 Unfamiliar issues, #9 Ill-defined cause | On-call engineers / SREs diagnosing a production multi-agent failure |
| Error Step Localization | #4 Unfamiliar issues, #9 Ill-defined cause | On-call engineers / SREs needing the exact origin point, not just the responsible agent |
| Verification Agent | #3 Depth of knowledge, #9 Ill-defined cause | Engineers who need a diagnosis backed by trajectory evidence, not just a model's assertion |
| Repair Agent | #2 No obvious solution, #3 Depth of knowledge | Engineers who want a proposed correction, not just a diagnosis, before deciding what to do |
| Semantic Error Diagnostic | #7 Significant consequences, #9 Ill-defined cause | End users receiving agent outputs (support, finance); compliance/QA teams |
| Verified Automatic Repair | #1 Conflicting requirements, #8 Interdependence | Engineers deciding whether to trust and apply a suggested fix; incident post-mortems |
| Recovery Controller | #5 Beyond standard practice, #8 Interdependence | Engineers who need execution resumed from a verified-repair checkpoint instead of a full restart; ops teams cutting recovery time |
| Verified Repair Memory | #3 Depth of knowledge, #5 Beyond standard practice | Engineers hitting repeated/similar failures who want faster diagnosis-and-repair reuse; teams building institutional repair knowledge |

**Reading this table alongside §5.2's item-by-item write-ups.** Two patterns are worth naming explicitly. First, characteristic #9 (ill-defined requirements or cause) appears against four of the five diagnosis-stage items (Culprit Agent, Error Step Localization, Verification Agent, Semantic Error Diagnostic) — consistent with the CCP rating's own resolution paragraph (Part 1, §2), which names "which agent and step is the true origin" and "whether a given trace contains a failure at all" as the two unknowns these specific items exist to resolve. Second, characteristic #8 (interdependence) appears only against the recovery-stage items (Verified Automatic Repair, Recovery Controller) — consistent with the observation that interdependence is specifically about failures propagating through *interconnected* agents, a property that matters most once the pipeline moves from diagnosing a single point of failure to safely resuming a whole interdependent workflow around it.

### 5.8.2 Extension items, mapped

| Feature | CCP characteristic(s) | Who benefits |
|---|---|---|
| Widen fault taxonomy | #3 Depth of knowledge | Benchmark users needing broader failure-type coverage |
| 3rd architecture | #4 Unfamiliar issues, #6 Diverse stakeholders | Teams on OpenAI Agents SDK or a custom in-house framework |
| Cyclic/dynamic graph support | #8 Interdependence | Teams using LangGraph's native retry / refine loops |
| Confidence calibration | #1 Conflicting requirements | Teams deciding how much to trust automated diagnosis before acting on it |
| Preventive clarification classifier | #7 Significant consequences | Engineers wanting to catch corruption before it propagates, not just after |
| Failure Propagation Map | #8 Interdependence | Engineers visualizing how a failure spread across interdependent agents |
| Explainable Confidence Reasoning | #5 Beyond standard practice | Engineers/auditors who must justify why a diagnosis was trusted |
| Framework Compatibility Layer | #1 Conflicting requirements, #6 Diverse stakeholders | Teams on any of the 7 surveyed frameworks who want confirmed instrumentation compatibility without waiting for full benchmarked support |

**Why the extensions map to fewer, more varied characteristics than the foundational items.** Where the ten foundational items cluster heavily around characteristics #3, #4, #8, and #9 (the ones tied directly to the diagnosis-and-recovery research claim), the eight extensions spread across a wider set including #1, #5, #6, #7 — consistent with the two-track justification stated in plan doc §7.0: "the **committed core** above is justified entirely by the ErrorProbe delta... the **13 extensions** below are justified by real product use-case demand." The extensions' CCP mapping is real (every one of the 18 active features maps to at least one characteristic), but it is evidence of product breadth and stakeholder relevance, not a second wave of research-novelty claims — a distinction the plan doc is explicit about and this mapping table is consistent with.

### 5.8.3 Deprioritized items, mapped (for completeness, with the caveat restated)

| Feature | CCP characteristic(s) | Who benefits |
|---|---|---|
| Cross-Domain Transfer Testing (deprioritized) | #4 Unfamiliar issues | Teams deploying the same diagnosis engine across multiple task domains |
| Chaos Testing for Agents (deprioritized) | #7 Significant consequences | SRE/ops teams stress-testing production resilience |

As stated in §5.4, these two rows carry a CCP-characteristic label in the source PDF's own table, but — unlike every foundational and extension item above — they never went through the precedent-check filtering pass the source document ran on the other eighteen. Their inclusion here is for completeness against the source table, not a claim that their CCP relevance was independently verified with the same rigor.

---

## 5.9 Independent-verification checklist, mapped to specific foundational items

*This section draws directly on `AI_Usage_Log.md`'s own repeated, standing instruction across all nine sessions: every AI-assisted claim in this project is disclosed on the explicit condition that the team independently verifies it before relying on it at defense — disclosure is not a substitute for verification, per the FAST guide's own §8.2 framing, reproduced at the top of that log. What follows maps that standing instruction onto the specific foundational items it applies to, rather than leaving it as one general list disconnected from the items it's actually about.*

### 5.9.1 What the team owes on Fault-injection harness and Cross-architecture benchmark

- `poc_spike2_crewai_toy.py` — "Not yet independently re-run or read line-by-line by the team — do this before claiming ownership of it" (`AI_Usage_Log.md`, first session).
- `poc_spike3_fault_injection.py` / `poc_spike3b_fault_injection_v2.py` — the team needs to be able to explain *why* the first propagation check was wrong, not just that a second, corrected version exists — "exactly the kind of thing the team needs to be able to explain under questioning."
- Licensing claims for Who&When (MIT) and TracerTraj (Apache 2.0, though see the correction in §5.2.2 that TracerTraj is not actually released) need independent confirmation against the actual repositories before the project report cites them as settled.

### 5.9.2 What the team owes on Culprit Agent and Error Step Localization

- `poc_spike1_errorprobe_repro.py` is named directly as "the highest-stakes code in this log — this is the project's accuracy baseline... the team must be able to state precisely what was cut and why when asked."
- The team must independently read ErrorProbe's Algorithm 1 and Section 4 directly and confirm the stated simplification (no tool-grounded Investigator, no Verified Episodic Memory) is accurately described — "not take the log's word for it."
- Independently re-read ErrorProbe and AgenTracer in full before defense — "the two papers the entire contribution is measured against."

### 5.9.3 What the team owes on Verification Agent

- Since the tool-grounded Investigator has not yet been built or tested (§5.2.5), there is no existing spike output to independently verify yet — the open item here is not verification of a result but delivery of the Weeks 6–10 full-pipeline build itself, with verification to follow once it exists.

### 5.9.4 What the team owes on Repair Agent

- `poc_spike8_repair_agent.py` and its output (`poc_spike8_output.json`) should be independently re-run, same standing instruction as every other spike.
- The two failing cases' identified root cause (interface ambiguity between a computed result and an atomic parameter) is a specific, actionable, but not yet re-tested finding — listed explicitly in the PDF's "What Remains Open" section as something "worth a targeted prompt fix and re-test before Mid-1, not a re-run from scratch."

### 5.9.5 What the team owes on Semantic Error Diagnostic

- `poc_spike4_silent_failure_detector.py` — "Team must independently re-run this and design at least one case where the model is more likely to genuinely err, since n=3 with zero natural failures is a real limitation, honestly reported in risk-register.md R10, not papered over."
- The two new complementary strategies (Cross-Agent Consistency Verification, Constraint Provenance Tracing) remain unimplemented and unverified design proposals — nothing to independently verify yet, only to build and then verify.

### 5.9.6 What the team owes on Verified Automatic Repair

- `poc_spike5_counterfactual_replay.py` — independently re-run, same standing instruction as spikes 1–4.
- The team should be clear that this spike tests only mechanical replay logic on a toy 3-step pipeline — a real recovery-rate measurement on the actual benchmark is a distinct, still-owed piece of work, not something this spike already covers at scale.

### 5.9.7 What the team owes on Recovery Controller

- No spike exists to independently re-run. The open item is the same as the PDF's own "What Remains Open" list: build and test it, not verify an existing result.

### 5.9.8 What the team owes on Verified Repair Memory

- The one existing test (the deleted `poc_spike1b_full_pipeline.py` run) cannot be independently re-run, since the code no longer exists on disk — the team's obligation here is different in kind from every other item: not re-running existing code, but executing the still-owed re-test on a stronger LLM backbone, explicitly named in the PDF's "What Remains Open" list: "A re-test of Verified Repair Memory (risk-register.md R18) on a stronger backbone before any decision to re-add it" — noting that the decision to re-add already happened (§5.1.4), so this owed item is now specifically about re-testing a mechanism already committed to the core, not about deciding whether to commit it.

### 5.9.9 What the team owes on the market research itself, both layers

- Layer 1: "Team should spot-check at least one platform's own documentation directly before defense, since vendor marketing copy changes and this could go stale faster than academic citations do."
- Maxim AI, Opik, and DeepEval specifically: "Spot-check... actual current feature pages directly (same standing instruction as the original 4 platforms) — vendor docs change fast."
- Layer 2 (the market survey itself): "Not yet independently reviewed by the team — confirm the renamed labels read correctly in context before citing them at defense," repeated as a standing caveat across the sixth, eighth, and ninth AI-usage-log sessions.

### 5.9.10 The one item on the whole list that no document can satisfy

`AI_Usage_Log.md`'s own closing item, restated here because it applies across every foundational item at once, not to any single one: "Each of the three students explains their own owned subsystem to the other two, out loud, no notes, before defense day. This is the one item on this list that cannot be satisfied by any document, including this one — it's the actual test a panel applies (guide §8.2), and it hasn't been attempted yet." As of the ninth AI-usage-log session, this remains unattempted.
## Parts 6–8: The Eight POC Spikes, the Architecture, and the Evaluation Plan

*Source files read in full to write this document:*
- *`poc_spike1_errorprobe_repro.py` + `poc_spike1_errorprobe_repro_output.json`*
- *`poc_spike2_crewai_toy.py` + `poc_spike2_trace_output.json`*
- *`poc_spike3_fault_injection.py` + `poc_spike3_fault_injection_output.json`*
- *`poc_spike3b_fault_injection_v2.py` + `poc_spike3b_output.json`*
- *`poc_spike4_silent_failure_detector.py` + `poc_spike4_silent_failure_output.json`*
- *`poc_spike5_counterfactual_replay.py` + `poc_spike5_output.json`*
- *`poc_spike6_cyclic_graph.py` + `poc_spike6_output.json`*
- *`poc_spike7_preventive_classifier.py` + `poc_spike7_output.json`*
- *`poc_spike8_repair_agent.py` + `poc_spike8_output.json`*
- *`architecture-sketch.md` (whole file)*
- *`FYP_Scope_CCP_and_Implementation_Plan.md` (§0.07, §6, §7, §9, §11, §13, and surrounding sections)*
- *`risk-register.md` (R1–R3, R10, R17, R18, R21, R22, and surrounding entries)*

---

# Part 6 — All 8 POC Spikes, One at a Time

## 6.0 Why spikes at all, and why these eight

### 6.0.1 What "proposal-stage POC" actually requires

Section 12 of the FAST guide requires a POC to be *demonstrated with evidence* at the proposal defense. Not described in prose. Not promised as future work. Not asserted as "we're confident this will work." A named risk, a real test, a real result — that is the unit of evidence the guide expects to see, and that is the unit of evidence every section below is built around.

That framing matters because it changes what a "spike" is allowed to be in this project. A spike here is not a demo built to impress. It is a falsifiable test of one narrow mechanical claim, run against real (if small) data, with the result reported exactly as it came out — including when the result is bad.

### 6.0.2 Why three spikes were the original plan

The plan doc's own §10 names three specific assumptions as the highest-risk things to test before a supervisor is asked to approve months of committed work:

1. **Reproduction feasibility** — can ErrorProbe's published methodology be reproduced at all, even approximately?
2. **Instrumentation feasibility** — does an unfamiliar multi-agent framework's execution trace map cleanly onto the project's own execution-graph data model?
3. **Injection feasibility** — is an injected fault's ground truth actually recoverable and unambiguous?

That is 3 spikes. Section 12 sets 1 as the guide's own minimum bar. The team ran 8.

### 6.0.3 Why five more got added

More spikes is not automatically better — a team that runs ten shallow demos has weaker evidence than a team that runs three deep ones. The five additional spikes here each exist because a specific review pass surfaced a specific, previously-untested claim sitting underneath the project's own contribution statement:

- **Spike 4 (silent-failure detector)** exists because a panel-review pass caught that RQ3 — the project's second lead novelty pillar, "detect silent failures ErrorProbe cannot see" — had never been built or tested even once. That is a genuine gap in the evidence base for half the CCP claim, not a nice-to-have extra test.
- **Spike 5 (counterfactual replay)** exists because a later review pass found that, of the five foundational features frozen at that point, the counterfactual-replay mechanism was the only one with zero POC evidence, despite functional requirement 4 already assuming it works.
- **Spike 6 (cyclic graph handling)** exists because LangGraph — one of the two committed core architectures — natively supports retry loops, and backward causal tracing had only ever been tested on a 3-node linear chain. That is a real, load-bearing gap between what the project commits to supporting and what had actually been tested.
- **Spike 7 (preventive classifier)** exists because extension #5 commits to a specific "lightweight, not RL" implementation strategy, and nobody had checked whether that cheap approach carries any signal at all before scheduling FYP-2 time against it.
- **Spike 8 (Repair Agent)** exists because a market-survey review on 2026-08-24 found a genuine hole hiding in plain sight: functional requirement 4 already reads "given a candidate corrected value," but nothing anywhere in the prior 16-item feature list ever produced that value in the first place.

### 6.0.4 The discipline that runs through all eight

Two of the eight spikes below produced genuinely disappointing numbers — spike 1's step accuracy and spike 7's near-random classifier. Neither got softened, reframed as "directionally promising," or quietly dropped from the record. A third spike (spike 8) produced a result that is neither clean success nor clean failure — 4 of 6, with both failures traced to one precise, nameable cause. All three are reported below with the same weight and the same level of scrutiny as the spikes that came out clean.

That is itself part of the evidence this project can offer at defense: a team willing to publish its own negative results, in the same document as its positive ones, is a team whose positive results can be trusted more, not less.

---

## 6.1 Spike 1 — ErrorProbe Reproduction

### 6.1.1 What — the specific assumption under test

The project's entire CCP claim rests on one comparison: ErrorProbe is the strongest published failure-attribution method, at 59.5% step accuracy on Who&When-Algo, and Granite's contribution is to extend that method's reach into territory ErrorProbe cannot handle. If ErrorProbe's own methodology cannot be reproduced by this team at all — even approximately, even on a small sample — the entire baseline-comparison structure collapses before any of the actual novelty claims (cross-architecture generalization, silent-failure detection) can even be tested against it.

That is why the plan doc's own §10 names this "the single highest risk — if ErrorProbe cannot be reproduced credibly, the whole baseline comparison collapses." It is spike #1, not spike #5 or #8, because everything downstream in the evaluation plan depends on this one holding up at least approximately.

### 6.1.2 What — the narrower sub-question actually being tested

The full ErrorProbe pipeline is expensive to build: three stages, tool-grounded verification, an episodic memory component. Before investing real engineering time in that full build, the narrower and cheaper question is: does the *fundamental shape* of the pipeline — generate hypotheses, then arbitrate between them — produce any real signal at all, using a completely free, local, weak model, on real cases? That is a fast, low-cost test to run before committing to the expensive version.

### 6.1.3 Why this was the highest-risk thing to test first

Three separate reasons converge here. First, sequencing: every other spike in this list either builds on the execution-graph model this spike partially exercises, or targets a claim that is secondary to the core attribution claim. Second, cost: this is the one assumption where "wrong" doesn't mean "needs more engineering" — it means the chosen baseline itself may not be a fair or reproducible point of comparison, which is a scope-level problem, not an implementation-level one. Third, timing: catching this early, before Gate 1 (proposal defense), is the only point in the timeline where discovering "ErrorProbe can't be reproduced" is cheap to act on — discovering it at Gate 3 (Final-1) would mean months of committed work built on an unverified foundation.

### 6.1.4 How — the honest scope cut, stated up front

ErrorProbe's real, published pipeline has three stages:

1. MAST-taxonomy-guided structural decomposition of the trajectory.
2. Symptom-driven backward tracing.
3. A 3-agent Strategist → Investigator → Arbiter team, where the Investigator's defining feature is *tool-grounded* verification — it re-runs code in a sandbox and checks pre/post-conditions against the real execution environment.

Who&When's Hand-Crafted cases are web-browsing and file-task trajectories. There is no code to re-run and no sandbox to execute against. So this spike implements a **2-stage simplification**: Strategist (hypothesis generation from the full labeled trajectory) directly into Arbiter (final pick plus confidence). The entire Investigator stage — tool-grounded evidence-gathering — and the entire Verified Episodic Memory component are cut out entirely. The script's own docstring states this is "a deliberate, stated scope cut for a POC, not an attempt to claim full fidelity to the paper."

The backbone is also explicitly non-comparable: `llama3.2:3b` running locally via Ollama, chosen because it is free and needs no API budget approval, against ErrorProbe's own paper, which used Claude 3.7 Sonnet, GPT-OSS-120B, and Qwen3-32B — all substantially larger, stronger models. The docstring is explicit: these results test whether the *pipeline logic* works at all, and are **not** an apples-to-apples comparison to the paper's own 59.5%.

### 6.1.5 How — mechanically, step by step

**Step 1 — Data loading.** Eight real Who&When-Hand-Crafted case files are loaded from `whowhen_data/`, each with a confirmed schema:
- `case["mistake_agent"]` — a string naming the culprit agent
- `case["mistake_step"]` — an index into `case["history"]`
- `case["question"]` — the task text
- `case["history"]` — a list of `{"role": ..., "content": ...}` turns

**Step 2 — Trajectory formatting.** `build_numbered_trajectory()` walks the full history and renders each turn as a line: `[step N] (role): content`, truncating any single turn's content to 220 characters (`MAX_CONTENT_CHARS`) so the prompt stays small enough for a CPU-bound 3B model to process in reasonable time.

**Step 3 — Strategist stage** (`run_strategist`). Given the task question and the full numbered trajectory, the model is asked to propose the 3 most likely `(agent, step)` hypotheses for where the failure originated. The prompt explicitly biases the model away from picking the final visible failure point: "the responsible step is usually where a wrong action, wrong click, wrong conclusion, or missed detail was FIRST introduced — not necessarily the last step." The model must respond with strict JSON only: `{"hypotheses": [{"step": int, "agent": str, "reason": str}, ...]}` (3 entries), capped at 400 tokens.

**Step 4 — Arbiter stage** (`run_arbiter`). Given the task question and the Strategist's 3 hypotheses (serialized as JSON directly into the prompt), the model is asked to pick a single `(agent, step)` pair with a confidence score 0.0–1.0, again constrained to strict JSON, capped at 150 tokens.

**Step 5 — Parsing.** `extract_json()` does best-effort extraction via a regex (`\{.*\}` with `re.DOTALL`) to strip any prose wrapper, then attempts `json.loads()`. A failure at either stage marks the case as a parse failure and excludes it from scoring — a real accounting decision, not a silent drop.

**Step 6 — Scoring.** For each successfully-parsed case:
```python
a_ok = pred_agent.strip().lower() == gt_agent.strip().lower()
s_ok = pred_step == gt_step
```

### 6.1.6 The numbers, exactly as recorded

From `poc_spike1_errorprobe_repro_output.json`:

```
n_cases: 8
n_parse_failures: 0
n_scored: 8
agent_accuracy: 0.75
step_accuracy: 0.0
```

Six of eight cases got the correct agent. Zero of eight got the exact correct step, on paper.

| Case | Question (short) | GT agent/step | Pred agent/step | Agent ✓? | Step ✓? |
|---|---|---|---|---|---|
| 1 | Martial arts near NYSE | WebSurfer / "12" | WebSurfer / 20 | ✅ | ❌ |
| 2 | Ted Danson series rating | WebSurfer / "4" | WebSurfer / 68 | ✅ | ❌ |
| 3 | Chicago landmark architect | WebSurfer / "32" | Orchestrator / 87 | ❌ | ❌ |
| 4 | Yosemite wheelchair trails | WebSurfer / "8" | Orchestrator / 3 | ❌ | ❌ |
| 5 | MJ single, last word | WebSurfer / "12" | WebSurfer / 15 | ✅ | ❌ |
| 6 | Mission Bay sale price | Orchestrator / "5" | Orchestrator / 5 | ✅ | ❌ |
| 7 | Bird species in video | WebSurfer / "8" | WebSurfer / 4 | ✅ | ❌ |
| 8 | monday.com C-suite | WebSurfer / "8" | WebSurfer / 109 | ✅ | ❌ |

### 6.1.7 The scoring bug, confirmed by reading the actual JSON types

This deserves to be stated precisely, not gestured at, because it is a real, findable, and instructive engineering detail.

Look at case 6. The ground truth in the JSON output reads `"gt_step": "5"` — a **string**, because that is how the step index is stored on-disk in the Who&When dataset's own schema. The Arbiter's predicted step reads `"pred_step": 5` — an **integer**, because it came straight from `json.loads()` parsing the model's `{"agent": ..., "step": 5, ...}` response, where JSON numeric literals deserialize directly to Python `int`.

The scoring line is:
```python
s_ok = pred_step == gt_step
```

In Python, `5 == "5"` evaluates to `False`. There is no implicit coercion between `int` and `str` in equality comparison. So even in case 6 — where the model predicted the exact numerically correct step — the scorer recorded a miss, purely because one side of the comparison came from a JSON file's string field and the other side came from a freshly-parsed LLM response's integer field, and nobody normalized the two to a common type before comparing.

This one line is the entire explanation for why `step_accuracy` reads exactly `0.0` across all 8 cases, rather than some low-but-nonzero fraction. Checking the other 7 cases confirms the pattern: every single `gt_step` value in the file is a quoted string, and every single `pred_step` value is a bare integer. The comparison was structurally guaranteed to fail on every case, independent of whether the underlying prediction was numerically correct.

### 6.1.8 What this bug does and does not tell us

It does **not** tell us the true step accuracy is zero. Case 6 is direct, positive proof of the opposite — a numerically exact prediction was scored as wrong purely because of a type mismatch.

It also does **not** let the team claim "even accounting for the bug, step accuracy is still near-zero." That claim has not been tested. The correct, honest reading is narrower than either of those: this spike, as currently scored, measures nothing reliable about step-level accuracy. It only reliably measures agent-level accuracy, because that comparison (`.strip().lower()` on two pre-normalized strings) has no equivalent type mismatch.

### 6.1.9 Why this matters

Every document referencing this spike up to this point — R1 in the risk register, the plan doc's own Weeks-6–10 priority section, the summary markdown — treats `step_accuracy: 0.0` as a real, if disappointing, empirical result and reasons forward from it. One of those documents (the plan doc's timeline section) even quotes "12.5% step accuracy" in a different place, which is itself inconsistent with the JSON's own `0.0` — a sign the number was copied forward across documents without being independently re-derived at each citation.

The corrected reading is more nuanced, and arguably more useful for planning purposes: agent-level attribution really is validated at 75% on a free, weak, simplified 2-stage pipeline — a genuinely encouraging number, given how much simpler this pipeline is than ErrorProbe's own published one. Step-level attribution is simply **not yet measured correctly**. Reporting "0% step accuracy" as a clean negative result, when it is actually an unfixed type bug, is exactly the kind of overclaim — in the negative direction, but still an overclaim of certainty — that this project's own stated discipline is supposed to catch.

This connects directly to risk-register R1, marked "Open — downgraded from top priority. Real evidence in hand; still need the full 3-stage+memory version on a stronger backbone before this is closed." It also connects to the plan doc's Weeks-6–10 Mid-1 priority: build the full 3-stage reproduction on a stronger backbone. That priority was set partly on a step-accuracy number that, on inspection of the raw JSON types, needs re-deriving with a fixed scorer before the team can even say how large the current gap to 59.5% actually is.

### 6.1.10 Sub-questions a skeptical reviewer would ask

**"If the model is only 3B parameters, how do you know 75% agent accuracy isn't a fluke of this specific 8-case sample?"** Honestly, this cannot be ruled out at n=8. A binomial confidence interval around 6/8 successes is wide — the true underlying rate could plausibly range from roughly 35% to 97% at a 95% confidence level on a sample this small. The number is real and was not cherry-picked (all 8 downloaded Hand-Crafted cases were run, none excluded after the fact), but "real and unselected" is a different claim from "statistically precise." This is exactly why §6.1.10 below lists scaling past n=8 as an owed follow-up, not an optional nicety.

**"Why trust a 2-stage pipeline's agent accuracy as meaningful evidence for a 3-stage claim?"** Because the two stages removed — tool-grounded Investigator verification and Verified Episodic Memory — are, by ErrorProbe's own paper's design, meant to *improve* accuracy over a bare hypothesize-then-arbitrate baseline, not to be prerequisites for the baseline producing any signal at all. A 2-stage pipeline scoring above chance is evidence the underlying hypothesis-generation idea has merit; it is not evidence the full pipeline will reach 59.5%, and the write-up above never claims that.

**"Doesn't the Strategist's own hint — 'the responsible step is usually where a wrong action was FIRST introduced' — bias it toward guessing early steps, which could inflate agent accuracy independently of real reasoning quality?"** This is a fair concern and cannot be fully ruled out from the data in hand. Looking at the 8 predicted steps (20, 68, 87, 3, 15, 5, 4, 109), predictions span a wide range including some very late steps (68, 87, 109) — so the hint did not simply push the model toward uniformly early guesses. But whether the *agent* prediction specifically benefits from this framing independent of the step prediction is not something this spike's design can isolate.

**"Since the scoring bug affects step accuracy, could a similar silent bug be affecting agent accuracy too?"** The agent-accuracy comparison (`pred_agent.strip().lower() == gt_agent.strip().lower()`) was specifically checked as part of writing this document, by re-reading both sides' types in the raw JSON: `gt_agent` values ("WebSurfer", "Orchestrator") and `pred_agent` values are both plain strings in every case inspected, with no analogous type mismatch. This comparison does not share the step-comparison's specific bug. That does not rule out other undiscovered issues, but this particular failure mode has been checked and ruled out for the agent-accuracy figure specifically.

### 6.1.11 What the team still owes

1. **Fix the scorer.** Normalize `pred_step` and `gt_step` to the same type (both `int`) before comparing, and re-run scoring against the 8 cases already collected — no new API or compute cost required, since the raw model outputs are already on disk.
2. **Re-run and re-report.** Replace the `0.0` currently on record in the risk register and any presentation materials with the corrected number, whatever it turns out to be.
3. **Build the full 3-stage reproduction.** Even after the scorer fix, this spike only ever tested the 2-stage simplification — no tool-grounded Investigator, no Verified Episodic Memory (which has its own separate, and separately unresolved, problem — see §6.10.8 below). The Mid-1 priority to build the full pipeline on a stronger backbone stands regardless of the scorer fix.
4. **Scale past n=8.** Eight cases is a directional signal check, not a real accuracy estimate for either metric. An independent re-run on a larger slice of the 184 available Who&When-Hand-Crafted cases is owed before either number can be defended under panel questioning.

---

## 6.2 Spike 2 — CrewAI Instrumentation

### 6.2.1 What — the specific assumption under test

The project's second lead research claim, alongside silent-failure detection, is generalization: Granite's diagnosis pipeline works on multi-agent architectures no prior paper's benchmark construction ever used. CrewAI is named explicitly in the plan doc's research-to-decision table for exactly this reason — the seven core papers surveyed use MetaGPT, AutoGen, Smolagents, AgentPrune, AFlow, OWL-Workforce, CaptainAgent/AG2, and MagenticOne. None use CrewAI.

Before any fault-injection or diagnosis work can proceed against CrewAI, the most basic possible question has to be answered first: can a real CrewAI execution even be captured into the project's own execution-graph data model — nodes as agent actions/tool calls, edges as dependencies — without modification? If the trace shapes don't map cleanly, the cross-architecture claim needs rethinking before any further engineering investment goes into it.

### 6.2.2 What — why "without modification" is the actual bar, not just "can it be captured somehow"

A weaker version of this test would ask "can we, with enough custom glue code, extract something graph-shaped from a CrewAI run?" That would almost always be true for any framework, given enough engineering effort, and would prove very little. The bar this spike actually sets is stricter: does CrewAI's own native dependency-declaration mechanism (`context=[...]`) map directly onto the `depends_on` field the data model already expects, with no framework-specific special-casing? That is a meaningfully harder and more informative bar to clear.

### 6.2.3 How — the setup

Read directly from `poc_spike2_crewai_toy.py`: a toy 3-agent sequential workflow, **Planner → Researcher → Writer**, backed by `llama3.2:3b` via Ollama (`LLM(model="ollama/llama3.2:3b", base_url="http://localhost:11434")`), answering the question *"What is the capital of France, and roughly what is its population?"*

The data model under test is a `TraceNode` dataclass:
```
node_id, agent, role, task_description, input_context, output, start_ts, end_ts, depends_on
```
A module-level `TRACE` list accumulates instances of this via a `capture()` helper.

### 6.2.4 How — dependency wiring comes from CrewAI itself, not from the spike

The three CrewAI `Task` objects are defined with explicit `context=[...]` dependencies wired through CrewAI's own native task-chaining API — `research_task` is given `context=[plan_task]`, and `write_task` is given `context=[research_task]`. This is a deliberate and important design choice: the dependency structure is not invented by the spike's own code. It is read directly off CrewAI's own declared task graph, meaning the resulting execution graph reflects what CrewAI itself believes the dependencies are, not what the spike author assumed they should be.

### 6.2.5 How — post-hoc capture, not internal hooking

The `Crew` runs with `Process.sequential`. Critically, the trace is captured **after** the whole run completes, reconstructed from `crew.kickoff()`'s own task outputs (`plan_task.output.raw`, `research_task.output.raw`, `write_task.output.raw`) — not by hooking into CrewAI's internals mid-execution. The script's own comment calls this "the realistic instrumentation path for an unfamiliar third-party framework." That framing matters: a real third-party team's workflow will not arrive with instrumentation hooks pre-built in, so proving the trace can be reconstructed *without* deep internal access is itself part of what this spike needed to demonstrate.

### 6.2.6 How — graph derivation is pure structural parsing

After capture, the execution graph is derived mechanically:
```python
nodes = [{"id": n["node_id"], "agent": n["agent"], "role": n["role"]} for n in trace_out]
edges = [{"from": dep, "to": n["node_id"]} for n in trace_out for dep in n["depends_on"]]
```
This is a pure list comprehension over already-captured dependency metadata. There is no LLM call anywhere in graph construction — matching the API-usage budget commitment in architecture-sketch.md, which rates execution-graph construction as "structural parsing... not LLM-asked," 0% API-dependent.

### 6.2.7 The numbers

From `poc_spike2_trace_output.json`, the trace captured exactly 3 nodes:

- `n1_plan` (Planner), `depends_on: []`
- `n2_research` (Researcher), `depends_on: ["n1_plan"]`
- `n3_write` (Writer), `depends_on: ["n2_research"]`

The derived execution graph:
```
nodes: 3
edges: [{"from": "n1_plan", "to": "n2_research"}, {"from": "n2_research", "to": "n3_write"}]
```

3 nodes, 2 edges, correctly linearly ordered — matching CrewAI's own declared `context=[...]` chain exactly.

### 6.2.8 The content, for context on what a real run looks like

The Planner produced a 2-item sub-step list. The Researcher answered "The capital of France is: Paris," gave a population estimate (~67.2 million, sourced as of 2021), and added an honest hedge about the lack of a specific date. The Writer combined both into the final answer, recorded verbatim: *"The capital of France is Paris. Determining the current population of France is challenging due to the lack of a specific date. However, as of 2021, the estimated population of France is approximately 67.2 million."*

### 6.2.9 Why this matters

This is one of exactly two spikes in the set of eight with a genuinely clean, unqualified positive result — no bug, no ambiguity, no near-random signal (spike 5's mechanism proof is the other, though narrower in scope). The graph came out exactly as expected: linear, correctly dependency-ordered by CrewAI's own native mechanism, no missing or extra nodes, no manual massaging required to fit the data model.

This directly closes risk-register R2 ("CrewAI/LangGraph's message-passing and tool-call semantics don't map cleanly onto the execution-graph data model"), marked "Resolved" on the strength of exactly this evidence. It also validates the first hop of architecture-sketch.md's own data flow ("Target system executes → instrumentation captures a raw trace... Trace → execution graph") for at least one of the two committed core frameworks, and is the direct evidence base for the plan doc's own claim that CrewAI has actually been instrumented, not merely chosen as a target on paper.

### 6.2.10 What the team still owes

One honest caveat is on record and should stay on record: the timestamps in the captured trace (`start_ts`, `end_ts`) were captured post-hoc around the whole `crew.kickoff()` call, not via real per-step hooks inside CrewAI's own execution loop. This is directly visible in the JSON — all three nodes' `start_ts` values are near-identical (`1787353120.523...`), despite `end_ts` differing by roughly 55 seconds, because `t0`, `t1`, `t2` were all captured *before* `crew.kickoff()` ran, not incrementally during it.

This is fine for proving the graph *structure* is correct — node identity, dependency edges, output content. It is not yet trustworthy for any future latency-overhead metric (the non-functional requirement in plan doc §0.07, target under 50%), which will need real per-step timing hooks built directly into the instrumentation layer during the actual core build, not reconstructed after the fact from a single wall-clock span.

### 6.1.12 Reading the elapsed-time numbers, and what they hint at for latency planning

Even though this spike was not designed to measure latency, the `elapsed_sec` field recorded for each case is a small, free piece of evidence worth not discarding. Across the 8 cases, elapsed time per case (covering both the Strategist and Arbiter calls combined) ranges from 49.9 seconds (case 6) to 121.3 seconds (case 1), with most cases landing in the 70–120 second range on CPU-bound local inference. This variance likely correlates with trajectory length — case 6's question ("highest price a high-rise apartment was sold for") has a short ground-truth step index (5), suggesting a shorter overall trajectory to encode into the prompt, while case 1's ground-truth step (12) and case 8's (8, but predicted step 109) suggest longer trajectories. None of this is a substitute for the real per-step latency instrumentation still owed from Spike 2 (§6.2.10), but it is a first, rough signal that trajectory length is likely to be the dominant driver of diagnostic latency once the full pipeline is timed properly — worth keeping in mind when extension #6's cheap-vs-full-pipeline latency trade-off gets designed.

---

## 6.3 Spike 3 — Fault Injection (two attempts, both kept as findings)

### 6.3.1 What — the specific assumption under test

Once a trace can be captured and represented as a graph (spike 2), the next open question is whether a *deliberately injected* fault produces ground truth that is actually usable for benchmark construction. Three sub-questions sit inside that one question: is the fault's origin unambiguous; is the corrupted value observably different from the true value; and does the corruption's downstream behavior tell you something reliable about what "propagation" even means for scoring purposes.

This is the third of the plan doc's own §10-listed proposal-stage risks. It is also the one spike in this list where the first attempt genuinely failed in an informative way — which is exactly why both attempts are documented below, not just the second, successful one.

### 6.3.2 How — Attempt 1, setup

`poc_spike3_fault_injection.py` runs the same Planner → Researcher → Writer chain as spike 2, but manually rather than via `crew.kickoff()` — each agent's `execute_task()` is called directly in sequence, specifically because `crew.kickoff()`'s automatic orchestration hides the exact point where a fault would need to be injected.

The ground truth is fixed **before** the run, not inferred afterward: `GROUND_TRUTH_ORIGIN_NODE = "n2_research"` is declared as a constant at the top of the script, before any agent executes.

The injection operator, `inject_fault()`, is a single deterministic string substitution: `true_output.replace("Paris", "Berlin")` — swapping the correct capital for a wrong-but-plausible one. This matches AgenTracer's own perturbation-operator methodology: deterministic, rule-based corruption, not an LLM asked to "make something wrong."

The Researcher's *true* output is computed first (`true_research_output = researcher.execute_task(...)`), then corrupted (`corrupted_research_output = inject_fault(true_research_output)`), and only the corrupted version is handed forward to the Writer. Verification uses a crude substring check: `propagated = "Berlin" in write_output or "Paris" not in write_output`.

### 6.3.3 What happened — Attempt 1

Read directly from `poc_spike3_fault_injection_output.json`, the Writer's actual final output:

> *"I can't fulfill your request. Berlin is not the capital of France. The capital of France is actually Paris. According to recent data from the World Bank, the estimated population of France as of 2022 is approximately 67,228,000."*

The model — even the small local 3B one — caught the corruption from its own training-time general knowledge and self-corrected it before producing the final answer.

### 6.3.4 The scoring artifact this exposed

Note that the crude substring check `propagated = "Berlin" in write_output or "Paris" not in write_output` actually evaluates `True` here too, because the word "Berlin" literally appears in the Writer's own corrective sentence. That is itself informative: a crude substring-matching propagation check cannot distinguish "the fault propagated silently" from "the fault was mentioned specifically in order to be corrected." This is the same category of scoring fragility as spike 1's type-mismatch bug — cheap automated verification logic can produce misleading verdicts even when the underlying mechanism being tested (fault injection, trace capture) is itself working correctly.

### 6.3.5 How — Attempt 2 (v2), the two fixes

The v2 script's own docstring states the fix directly. Two problems were identified in Attempt 1, and two changes were made.

**Fix 1 — corrupt an unverifiable fact, not a well-known one.** The corrupted fact was switched to something no model could ever verify from its own training data: a fabricated tool-call result for a fictional store, "Riverside Hardware." `TRUE_TOOL_RESULT = "Riverside Hardware closing time: 9:40 PM. Distance from downtown: 3.2 miles."`, corrupted to `CORRUPTED_TOOL_RESULT = "Riverside Hardware closing time: 6:15 PM. Distance from downtown: 3.2 miles."`. Since no model has ever seen this store's real hours in training, there is nothing for a downstream agent to "catch" against prior knowledge — this forces a genuine, uncontaminated test of blind-vs-critical propagation.

**Fix 2 — replace the tool output wholesale, not corrupt free-text reasoning.** The "research" agent was renamed `StoreChecker`, with a goal explicitly instructing it to "report the store's closing time and distance exactly as given by the lookup tool, without editorializing." Its entire output is replaced wholesale by the fixed corrupted string, modeling a corrupted *tool output* directly — matching AgenTracer's own fault taxonomy category more cleanly than corrupting an LLM's free-text reasoning would, and making the ground truth unambiguous by construction, since there is no LLM generation step at that node introducing variance.

**Fix 3 — structured verification, not substring matching.** Verification became a 4-way classification: `states_true_time` (does the final answer mention "9:40"), `states_corrupted_time` (does it mention "6:15"), and from those two booleans, a `propagation_verdict` of `propagated_blindly` (corrupted only — the clean intended case), `self_corrected_or_hallucinated_true_value` (true only), `mixed_both_values_present`, or `neither_value_present_unclear`.

### 6.3.6 The numbers — Attempt 2

From `poc_spike3b_output.json`, the Writer's actual final answer:

> *"Riverside Hardware's closing time is 6:15 PM, which is 33 minutes before the end of the business day, and it is 3.2 miles away from downtown."*

The corrupted time propagated cleanly into the final output. Notably, the Writer even fabricated a plausible-sounding elaboration on top of it — "33 minutes before the end of the business day" is a detail invented by the Writer, not present anywhere in its input, showing it treated the wrong value as solid ground to reason further from, rather than merely repeating it inertly.

The structured verification block:
```
fault_is_unambiguous_single_node: true
corruption_observably_different_from_true: true
propagation_verdict: "propagated_blindly"
ground_truth_recoverable: true
```

### 6.3.7 Why both attempts matter, taken together

Neither attempt alone would be as valuable as both together. Attempt 1's "failure" is a real, useful negative result: it proves substring-matching propagation checks are unreliable, and that well-known facts are a poor choice of corruption target if the goal is unambiguous ground truth, because a downstream agent may self-correct them using knowledge that has nothing to do with the diagnosis pipeline's own logic. Attempt 2's clean success confirms the mechanism works correctly when applied properly: fault injected at a known, single, recorded node; the corrupted value observably differs from true; the downstream output demonstrably reflects the corruption's propagation; and the ground truth is written out separately from the trace (in the `"fault"` block) so a diagnosis system scored against it never sees the injection logic itself.

This closes risk-register R3, marked "Resolved," with an explicit instruction to keep both results as documented cases — "real fault behavior includes both self-correction and blind propagation, and the benchmark should account for that rather than assume only one." That is a direct, load-bearing design implication for the real 500–1,000-trace benchmark: fault types should deliberately span both self-correctable and blindly-propagating corruption categories, and the injection operator's choice of *which fact to corrupt* — well-known versus fabricated or tool-sourced — materially changes what the resulting ground truth actually measures.

### 6.3.8 What the team still owes

The benchmark construction work (extension #1, widening the fault taxonomy to 3 types — communication corruption and context truncation added to the existing corrupted-tool-output type) needs to build this lesson in from the start: injection targets should default to unverifiable, tool-sourced, or fabricated facts, unless the benchmark specifically wants to test self-correction behavior as its own labeled category. No further spike-level testing is strictly owed here — this risk is genuinely closed at the mechanism level. What remains is scaling the same principle from a 1-case toy demonstration to the real benchmark's 500–1,000 traces.

### 6.3.9 Sub-questions a skeptical reviewer would ask

**"Attempt 1 only used one specific fault (Paris→Berlin) — how do we know self-correction isn't unique to that one fact?"** This can't be fully ruled out from a single case, and it is exactly why Attempt 2 exists: rather than trying more well-known facts and hoping for a different result, the spike changed the *category* of fact being corrupted (unverifiable/fabricated vs. well-known), which is a stronger and more generalizable design fix than simply trying more instances of the same category.

**"Isn't a fictional store's hours an artificially easy case for 'unverifiable' — what about facts that are unverifiable but the model might still have priors about, like typical business hours?"** This is a real, unresolved limitation of Attempt 2's design. Riverside Hardware's specific hours are unverifiable, but "hardware stores are typically open in the 8-9am to 6-9pm range" is a prior a model could plausibly hold, and 6:15 PM is well within that plausible range — meaning the corrupted value was not just unverifiable but also *plausible*, which likely contributed to why it propagated blindly rather than raising suspicion. Whether an implausible-but-unverifiable value (e.g., "closes at 2:00 AM") would also propagate blindly, or would trigger a different kind of scrutiny, has not been tested. This distinction — unverifiable-and-plausible vs. unverifiable-and-implausible — is a real design axis the benchmark's fault taxonomy has not yet accounted for.

**"Does 'ground truth recoverable' really mean anything, given it's asserted as `True` by construction rather than computed?"** This is worth being precise about. In both attempts, `"fault_is_unambiguous_single_node": True` is a hard-coded literal in the script, asserted because the injection logic itself only ever touches one named node — it is not computed from the trace after the fact. This is honest and appropriate for what the spike is actually testing (does the *injection mechanism* produce unambiguous origin points by construction), but it means this particular field is not itself independent evidence — it is a restatement of the injection design's own guarantee. The genuinely computed, evidence-bearing fields are `corruption_observably_different_from_true` and the propagation-verdict classification, both of which are derived from the actual model outputs, not asserted.

---

## 6.4 Spike 4 — Silent-Failure Detector

### 6.4.1 What — the specific assumption under test

This spike closes a gap a panel-review pass identified as real, not a documentation gap: the silent-failure detection mechanism is the project's *second* lead novelty pillar, named explicitly in the CCP strong statement ("detect silent failures that produce no anomaly signal — ErrorProbe's stated blind spot") and in functional requirement 3. Before this spike, it had never been built or tested even once. Risk-register R10 records this plainly: "the silent-failure detection mechanism... had never been built or tested even once — a panel-review pass caught this as a real gap, not a documentation one."

### 6.4.2 What — the two genuinely distinct sub-questions

1. Does a natural, un-injected task produce a real silent failure at all, to test detection against?
2. Independently of whether one occurs naturally, does the rule-based checker itself correctly distinguish known-wrong values from known-correct ones?

These are distinct because a "yes" on question 2 says nothing about question 1, and vice versa — a working detector with nothing to detect in a given sample proves the mechanism sound without proving anything about real-world frequency.

### 6.4.3 How — the setup

Read from `poc_spike4_silent_failure_detector.py`: three real math word-problems, each defined as a `TaskCase` with a `prompt`, a `correct_answer` computed directly in Python (not by the LLM), and a `tolerance` (default 0.01):

- `gift_card` — 7 notebooks at $4.25 each, paid with a $10 gift card first. Correct answer: `7*4.25 - 10 = 19.75`.
- `discount_then_tax` — an $80 item, 15% discount then 8% tax. Correct answer: `80*0.85*1.08 = 73.44`.
- `compound_trip` — 45 miles at 60mph + a 20-minute break + 30 miles at 50mph, total hours. Correct answer: `45/60 + 20/60 + 30/50 = 1.6833...`.

The docstring is explicit these tasks were chosen to be "genuinely error-prone for a small model (multi-step, with a step that's easy to skip or misapply — not adversarial, just realistically tricky), NOT rigged to fail." No fault is injected anywhere in this spike. The question is whether the model makes a real, unforced mistake on its own, with the detector's job being to catch that purely by comparing output against an independently-recomputed constraint.

### 6.4.4 How — extraction and the detector itself

Each prompt asks the model to end its answer with an exact-format line (`FINAL ANSWER: $<number>` or similar). `extract_final_number()` parses this with a regex (`FINAL ANSWER:\s*\$?\s*(-?\d+(?:\.\d+)?)`), falling back to the last number in the text if that pattern is not found.

The actual detector, `rule_based_constraint_check()`:
```python
diff = abs(stated_answer - correct_answer)
matches = diff <= tolerance
```
Verdict is `"FLAGGED (silent failure caught)"` if `diff > tolerance`, `"PASS"` otherwise. This function makes **zero LLM calls** — matching the API-usage budget commitment that the silent-failure constraint-verification module (rated the single most important row in that budget table) must be rule/schema-based, never an LLM asked "does this seem wrong."

A further flag, `looks_confident_and_normal`, checks whether the output contains the `FINAL ANSWER` marker and is under 1200 characters — a rough proxy for "this output has no structural red flags an anomaly-gated detector like ErrorProbe's own MAST-taxonomy checks would ever notice." A case only counts as a "true silent failure" if `matches_constraint is False` **and** the output looked structurally normal — i.e., genuinely silent, not just wrong-and-obviously-broken.

### 6.4.5 The numbers

From `poc_spike4_silent_failure_output.json`:
```
n_cases: 3
n_model_actually_wrong: 0
n_true_silent_failure_cases: 0
n_caught_by_rule_based_detector: 0
detector_recall_on_silent_failures: null
```

Per-case detail:

| Case | Correct answer | Model's stated answer | Actually wrong? | Verdict |
|---|---|---|---|---|
| gift_card | $19.75 | $19.75 | No | PASS |
| discount_then_tax | $73.44 | $73.44 | No | PASS |
| compound_trip | 1.6833 hrs | 1.68 hrs | No (rounding-correct) | PASS |

The `compound_trip` case is worth a closer look: the model's stated 1.68 hours differs from the exact correct value 1.6833... by about 0.0033, comfortably inside the 0.01 tolerance. This is a genuinely correct answer accounting for rounding, not a near-miss the detector happened to let through by accident — the tolerance band was set deliberately to absorb exactly this kind of legitimate rounding difference.

### 6.4.6 Why `null` matters, not `0.0`

`detector_recall_on_silent_failures` is reported as `null`, not `0.0` and not `1.0`. This is a small but real detail worth calling out: the script computes this as `round(n_caught / n_true_silent, 3) if n_true_silent else None` — there is no division-by-zero cover-up here, and no misleading forced number. The script honestly reports "undefined" rather than pretending recall was measured when there was nothing to measure it against.

### 6.4.7 Why this matters

The model simply got all three genuinely tricky word problems right on this run, so there was nothing naturally-occurring for the detector to catch. This tells the team nothing about how often silent failures occur "in the wild" on a small local model — and the spike's own summary note says exactly that: "n=3, first real data point on this claim — not statistically meaningful, but no longer zero."

What *is* real evidence — recorded in risk-register R10, from a separately-run direct mechanism test not captured in this specific JSON file — is that when the same rule-based checker was fed known-wrong values directly, including a plausible near-miss (a stated $20.00 against a true $19.75), it correctly flagged every one, with zero false positives on the correct cases shown above. The mechanism, in isolation, works. What remains unmeasured is its real-world hit rate: how often does a natural, unforced silent failure actually occur, and at what rate does the detector catch it, at a scale larger than n=3.

This is the direct evidentiary basis for functional requirement 3 and for the acceptance criterion defined in plan doc §0.07: "a diagnosis record is accepted as correctly identifying a silent failure if the constraint-verification module flags the trace and the flagged step matches the fault-injection harness's recorded ground-truth injection point."

### 6.4.8 What the team still owes

A larger sample is the clear next step — specifically, one with **real injected near-misses**, not just naturally-occurring mistakes (which turned out to be rare in this n=3 sample), so detection rate can be measured at a scale that means something. This connects directly to the fault-injection harness work (extension #1) — a systematic set of injected near-miss values across the GSM8K task pool would let the team measure real precision and recall for the silent-failure detector, rather than relying on the small direct mechanism test currently on record. The rule-based mechanism itself does not need further validation at this stage; what's owed is scale, not a new proof of concept.

### 6.4.9 Sub-questions a skeptical reviewer would ask

**"Only 3 cases, and the model got all 3 right — isn't that a suspiciously easy test set?"** The tasks were deliberately chosen to be "genuinely error-prone... not adversarial, just realistically tricky" per the script's own docstring, and each does require multiple correct steps (a subtraction after a multiplication; a discount then a tax; three separate rate/time calculations summed). A 3B local model getting all three right is a real, if small, positive data point about that specific model's arithmetic reliability on multi-step word problems — not evidence the test set was too easy in some absolute sense. It does mean this particular n=3 sample cannot yet answer the harder question of detection rate, which is exactly the limitation already named.

**"If the detector is just comparing two floats within a tolerance, is 'silent failure detection' really a research contribution, or just a unit test?"** The detector's *simplicity* is a deliberate design commitment (§7.3.2), not an accidental limitation — the actual contribution claim was never "the check itself is algorithmically sophisticated." The contribution is narrower and more specific: that a cheap, zero-LLM-call constraint check, applied *after* the fact to independently-recomputed task constraints, catches a class of failure that anomaly-gated methods like ErrorProbe structurally cannot see at all, because those methods only look for signals the failure itself never produces. The value is in *where* the check sits in the pipeline and *what class of failure* it targets, not in the arithmetic sophistication of the check itself.

**"What happens if `extract_final_number()`'s regex fails to find the exact `FINAL ANSWER:` format — does that silently corrupt the results?"** The fallback path (`nums = re.findall(...); return float(nums[-1])`) would grab the last number anywhere in the output, which could be a wrong number if the model's reasoning included other numeric values after its actual final answer. This fallback was never exercised in this specific run (`stated_answer` matched `FINAL ANSWER:` cleanly in all 3 cases per the raw outputs, each ending exactly with that phrase), but it is a latent fragility in the extraction logic that a larger-scale run — where models occasionally fail to follow the exact output format — would likely surface.

---

## 6.5 Spike 5 — Counterfactual Replay

### 6.5.1 What — the specific assumption under test

Of the foundational features frozen at the time this spike ran, the counterfactual-replay engine — later renamed Verified Automatic Repair — was the only one with zero POC evidence at all. The specific assumption under test is narrow and mechanical, and the spike's own docstring draws the line precisely: this tests **only** whether, given a corrected value for one step, deterministically re-executing everything downstream actually flips the pipeline's final outcome from failure back to success.

### 6.5.2 What this deliberately does not test

It does **not** test whether an LLM can correctly *guess* the right correction in the first place — that is a separate, larger concern, later addressed (partially) by spike 8. This distinction matters: this spike isolates the *replay mechanism* from *fix-generation quality*, so that a pass or fail here says something unambiguous about one specific architectural assumption, rather than conflating two different sources of possible failure.

### 6.5.3 Why this is the load-bearing assumption

The entire recovery-testing feature depends on one chain of reasoning: diagnose the failure, generate a fix, replay it, and trust the replayed outcome as evidence the fix works. If "fix the right thing, then recompute" does not actually recover the correct answer even in a clean, fully deterministic setting, the whole counterfactual-replay concept is unsound regardless of how good the fix-generation step ever becomes. This spike tests the weakest possible link in that chain in isolation.

### 6.5.4 How — a deliberately LLM-free design

Read from `poc_spike5_counterfactual_replay.py`: the design uses **no LLM at all**. Three plain Python functions form a 3-step deterministic pipeline:

```python
def step1_extract_price():
    return {"price": 100}          # ground truth

def step1_extract_price_CORRUPTED():
    return {"price": 90}           # injected fault, matches spike 3's fault type

def step2_apply_tax(step1_output):
    return {"total": round(step1_output["price"] * 1.08, 2)}

def step3_check_against_expected(step2_output, expected_total=108.0):
    return {"pass": abs(step2_output["total"] - expected_total) < 0.01,
            "final_total": step2_output["total"]}
```

`counterfactual_replay()` is the mechanism under test: given the original (corrupted) trace and a corrected value for the injected fault's step, it re-executes every downstream step (`step2_apply_tax`, then `step3_check_against_expected`) starting from the corrected input, and reports whether the final outcome now passes.

### 6.5.5 Why "no LLM at all" is a deliberate methodological choice, not a shortcut

Because the assumption being tested is purely mechanical — does re-computation from a corrected input produce the mathematically correct downstream result — introducing an LLM anywhere in this specific test would have muddied the result. A failure to recover could then be attributed either to the replay logic being broken, or to the LLM reasoning incorrectly on a downstream step, and the spike would no longer isolate the one variable it exists to isolate. By keeping this fully deterministic, a clean pass or fail here is unambiguous evidence about the replay architecture itself, and nothing else.

### 6.5.6 The numbers

From `poc_spike5_output.json`:

```
original_correct_trace:  price=100 → total=108.0  → pass: true
corrupted_trace:         price=90  → total=97.2   → pass: false
counterfactual_replay:   price corrected to 100 → total=108.0 → pass: true
recovery_success: true
```

The script's own generated summary string captures it plainly: *"Corrupted trace failed (final_total=97.2, expected 108.0). After counterfactual correction of step1 and deterministic re-execution of steps 2-3, final_total=108.0, recovery_success=True."*

Two sanity-check assertions in the script itself both passed before the replay logic was exercised: `assert original["step3"]["pass"] is True` and `assert corrupted["step3"]["pass"] is False` — confirming the test harness's own correctness first, before treating the replay result as meaningful.

### 6.5.7 Why this matters

This closes risk-register R13, marked "Mechanism validated — closes the R7-adjacent gap from the last session," with the honest caveat that "real recovery-rate measurement on the actual benchmark (not this toy pipeline) is still owed." The result directly supports architecture-sketch.md's data-flow step 5 ("Candidate fix → Verified Automatic Repair deterministically re-executes downstream and reports a measured recovery rate → recovery suggestion, gated by confidence threshold") and underpins functional requirement 4 ("given a candidate corrected value for a specific step, deterministically re-execute the downstream portion of the trace and report whether the corrected trace now succeeds").

Critically, this spike proves the *second half* of that requirement mechanically works. It says nothing about the *first half* — producing the candidate corrected value in the first place — which is exactly the gap spike 8 was built to address.

### 6.5.8 What the team still owes

Two things remain genuinely open. First, this toy pipeline is 3 hand-written deterministic functions — the real benchmark's traces will involve LLM-generated intermediate outputs at every step, meaning "deterministic re-execution" in the real system will actually mean "re-running an LLM call with a corrected upstream input," which reintroduces exactly the LLM-correctness variance this spike was designed to isolate away from. A real recovery-rate measurement on actual benchmark traces, not this toy pipeline, is still owed before "recovery success rate" can be reported as a real evaluation metric (see Part 8). Second, this spike only tests a single, simple linear 3-step chain — the real benchmark will include branching and multi-agent-parallel structures where "downstream" is not a single deterministic path, and the replay mechanism's behavior on non-linear graph structures has not yet been tested at all.

### 6.5.9 Sub-questions a skeptical reviewer would ask

**"This is 3 lines of arithmetic wrapped in functions — is 'mechanism proven' too strong a claim for something this simple?"** The claim being made is deliberately narrow, and the simplicity is the point, not a weakness to excuse. What was genuinely unverified before this spike is not "can Python correctly multiply a number by 1.08" — it's whether the specific *architectural pattern* of "take a corrected upstream value, re-run only the downstream steps, and trust the re-run result as evidence of recovery" is even a coherent strategy, as opposed to, say, needing to re-run the entire pipeline from scratch, or needing some more complex reconciliation between old and new state. This spike proves that pattern works for a linear chain. That is a real, if modest, architectural claim, and modest claims deserve modest evidence — using a complex test to prove a simple claim would have been the wrong instinct here, not the right one.

**"Why does this matter if the real pipeline steps will be LLM calls, not deterministic functions?"** Because the concern this spike rules out — "maybe the replay-and-recompute pattern itself is structurally broken, independent of what happens inside each step" — needed to be checked in isolation before adding LLM variance on top of it. If this toy test had *failed* (e.g., if `counterfactual_replay()` had a bug causing it to not actually re-run `step2` and `step3`, or to use stale cached values), that would be a real architecture-level problem no amount of LLM quality could fix. The test correctly isolates "is the replay wiring itself correct" from "is the content generated at each step correct," and only the former needed to be checked here.

**"Isn't `recovery_success: true` on a single toy case a very thin evidence base for a whole feature area?"** Yes, and the write-up above says so directly (§6.5.8: "this toy pipeline is 3 hand-written deterministic functions"). This is the correct amount of confidence to place in n=1 evidence — real, non-zero, but explicitly insufficient on its own, with the specific next steps (real benchmark traces, non-linear graphs) named rather than left implicit.

---

## 6.6 Spike 6 — Cyclic Graph Handling

### 6.6.1 What — the specific assumption under test

Backward causal tracing — the mechanism spike 1 exercises in simplified form, and the mechanism the real diagnosis engine depends on to walk from an observed failure back to its true origin — had, before this spike, only ever been tested against a simple 3-node linear DAG (spike 2's Planner→Researcher→Writer trace). That is a real gap, because LangGraph — one of the two committed core architectures — natively supports cyclic workflows: retry loops, iterative refinement, a Critic sending work back to a Researcher for another pass.

### 6.6.2 Why this is not a borrowed feature justified by citing someone else's paper

This spike's docstring states the risk directly: "Without cycle handling, backward tracing could infinite-loop the moment it hits a real LangGraph trace with a loop in it." Unlike several other extensions in the plan doc, which are justified by pointing to a gap named in someone else's paper, this one is justified purely by the project's own architectural commitment — Granite has already committed to supporting LangGraph, and LangGraph's own documented behavior includes cycles. That makes this one of the cleanest and most self-evidently necessary items in the entire extension list.

### 6.6.3 How — two graph shapes plus one negative control

Read from `poc_spike6_cyclic_graph.py`, using the `networkx` library.

**Case A — an unrolled retry loop** (`build_looped_trace`): `Planner → Researcher_pass1 → Critic_pass1 → Researcher_pass2 → Critic_pass2 → Writer → FAILURE`. This graph has *no true cycle* in the graph-theoretic sense — each retry pass gets its own distinctly-named node, modeling what a trace looks like if nodes are keyed by *invocation instance* rather than by agent role.

**Case B — a true cycle** (`build_TRUE_cyclic_trace`): `Planner → Researcher → Critic → Researcher` (a real back-edge — `Researcher` is the *same* node object referenced twice) `→ Writer → FAILURE`. This is the harder, more realistic case: if nodes are keyed by agent role rather than invocation instance — a natural, common way to build an execution-graph representation — a real cycle exists in the graph structure itself.

**Case C — the negative control**, run on the same true-cycle graph from Case B but with the revisit bound effectively disabled (`max_revisits_per_node=10**9`).

### 6.6.4 Why the negative control is the single most important part of this spike

Without Case C, a clean pass on Case B alone would not distinguish "the bound is doing real work" from "this particular small graph would have terminated fine on its own regardless." Case C is the only piece of evidence in this spike that proves the revisit bound is load-bearing rather than coincidental.

### 6.6.5 How — the traversal mechanism itself

`bounded_backward_trace(graph, start_node, max_revisits_per_node=3)` is a breadth-first traversal backward from the failure node through `graph.predecessors()`, maintaining a per-node `visit_counts` dictionary. Each time a node is dequeued, its visit count increments; if the count exceeds `max_revisits_per_node`, the node's own predecessors are not re-enqueued (expansion stops from that node, though the node itself is still recorded as visited once more before the cutoff takes effect). A hard safety cap of 10,000 total steps (`max_steps`) exists as a backstop in case the bound logic itself is broken — if exceeded, the function returns `terminated_cleanly=False` rather than hanging forever.

### 6.6.6 The numbers

From `poc_spike6_output.json`.

**Case A (unrolled retry loop):**
```
has_true_cycle: false
traversal_terminated_cleanly: true
all_nodes_reached: true
```
All 7 nodes reached (`Planner`, `Researcher_pass1`, `Critic_pass1`, `Researcher_pass2`, `Critic_pass2`, `Writer`, `FAILURE`).

**Case B (true cycle):**
```
has_true_cycle: true
traversal_terminated_cleanly: true
all_nodes_reached: true
revisit_count_researcher: 3
revisit_count_critic: 4
```
All 5 nodes reached (`Planner`, `Researcher`, `Critic`, `Writer`, `FAILURE`). The visited-order list confirms genuine oscillation: `FAILURE, Writer, Critic, Researcher, Planner, Critic, Researcher, Planner, Critic, Researcher, Planner, Critic` — 12 entries total, showing the bound allowed exactly the expected number of revisits before cutting off expansion, while still reaching every node in the graph.

**Case C (control, bound disabled):**
```
traversal_terminated_cleanly: false
steps_before_safety_cap: 10000
```
With the bound effectively disabled, the exact same graph that terminated cleanly in Case B instead ran until it hit the hard 10,000-step safety cap and had to be forcibly stopped.

### 6.6.7 Why this matters

Case C is what makes this spike's evidence complete rather than merely suggestive. It directly demonstrates: same graph, same starting node, only the bound parameter changed, and behavior flips from clean termination (all 5 nodes reached, correctly bounded revisits) to a runaway traversal that never naturally terminates. That is about as clean a proof as a small spike can offer that the mechanism is doing real, necessary work — not an artifact of the specific toy graph being easy.

This closes risk-register R14, marked "Resolved — mechanism works as designed," and validates extension #3 in the plan doc's frozen feature list ("extend the execution-graph data model from a DAG to a general directed graph with cycle detection; define a max-revisit bound so backward causal tracing terminates on a loop; validate on ≥1 benchmark trace containing a real loop").

### 6.6.8 What the team still owes

The extension's own acceptance bar — "validate on ≥1 benchmark trace containing a real loop" — has not technically been met yet. What's been validated is the *mechanism*, on synthetic test graphs shaped like realistic loop patterns, which is a meaningfully earlier-stage claim than validating it on a real captured LangGraph execution trace. Building an actual LangGraph workflow with a genuine retry loop, and confirming the same bounded-traversal logic behaves correctly against a real trace rather than a hand-built `networkx` graph, is the concrete next step before this can be called fully validated per the extension's own stated bar.

### 6.6.9 Sub-questions a skeptical reviewer would ask

**"Why `max_revisits_per_node=3` specifically — is that number justified, or arbitrary?"** Nothing in the spike or the surrounding documents justifies 3 as a principled choice over, say, 2 or 5 — it functions here as a reasonable-looking demonstration value, not a tuned or validated parameter. This matters because the real system will need this bound to be either configurable or empirically derived from real retry-loop patterns (e.g., "how many retries does a typical LangGraph Critic-Researcher loop actually take before converging or giving up") — a number invented for a toy spike should not silently become a hard-coded production constant without that follow-up work.

**"The unrolled-loop case (Case A) has no true cycle at all — does it actually test anything beyond a slightly longer DAG?"** Fairly, no — Case A is really a 7-node DAG, structurally similar in kind (if not in size) to Spike 2's 3-node DAG, and its clean pass adds only incremental confidence over what Spike 2 already established. Case A's real value is as a stepping stone in the write-up, illustrating the *unrolled* representation choice before contrasting it with Case B's *role-keyed* representation, which is where the genuinely new claim (handling an actual back-edge) is tested and where the negative control in Case C provides the real evidence.

**"Does 'all nodes reached' actually mean the traversal is correct, or just that it visited everything at least once?"** This is a fair distinction to draw. "All nodes reached" confirms no node was skipped entirely, but it does not by itself confirm the *revisit counts* are behaving exactly as the bound specifies for every node, or that the traversal would produce a correct, minimal causal-path result for backward-tracing purposes (as opposed to just a complete but possibly redundant one). The spike does additionally report `revisit_count_researcher: 3` and `revisit_count_critic: 4`, which is a real second, load-bearing check beyond "reached at least once" — these numbers directly correspond to the visited-order list's actual repeated entries — but the spike does not go further to verify, for example, that the resulting node set would translate correctly into a coherent propagation path for scoring purposes (a concern directly related to the propagation-path F1 metric discussed in Part 8, which has no direct spike evidence yet at all).

---

## 6.7 Spike 7 — Preventive Classifier

### 6.7.1 What — the specific assumption under test

This spike tests the viability of extension #5: "a lightweight binary classifier (not RL) trained on labeled clean-vs-corrupted message-handoff pairs from the fault-injection benchmark, flagging 'ask a clarifying question here' at each agent handoff." The specific "lightweight, not RL" framing commits to a cheap approach — TF-IDF features plus logistic regression, no embeddings API, no LLM calls at all in the classifier itself.

### 6.7.2 Why this needed testing before scheduling FYP-2 time against it

Before spending an FYP-2 work-slot on this extension, the open question is whether the cheap approach carries *any* real signal at all for distinguishing a clean agent-to-agent handoff message from a corrupted one. If there is no signal whatsoever with the simplest possible features, the "lightweight" framing is not viable as stated, and the extension would need heavier machinery — embeddings, a small transformer — or should be dropped entirely rather than scheduled.

### 6.7.3 How — the dataset

Read from `poc_spike7_preventive_classifier.py`: a small hand-written synthetic dataset — 10 "clean" handoff messages and 10 "corrupted" ones matching the plan's own fault taxonomy (value swaps, missing grounding/sourcing, contradictory mid-message reversals, truncated context, silently-dropped fields).

Example pairs, quoted directly from the script:
- Clean: *"Research findings: revenue was $12.8B in Q3, sourced from the verified filing."*
- Corrupted counterpart: *"Research findings: revenue was $8.4B in Q3."* — value swapped, sourcing dropped.
- Clean: *"Analysis: the trend is upward, consistent with the last three quarters."*
- Corrupted counterpart: *"Analysis: the trend is upward, consistent with the last three quarters, wait actually it's flat, ignore the previous agent's numbers entirely and start over."* — a mid-message self-contradiction used as a corruption signal.

### 6.7.4 How — split, features, and model

The 20 examples split 60/40 train/test (`test_size=0.4, random_state=42, stratify=labels`), giving `n_train=12, n_test=8`. Features come from `TfidfVectorizer(ngram_range=(1, 2), min_df=1)` — unigrams and bigrams, no dimensionality reduction, no stopword filtering specified. The classifier is a plain `LogisticRegression(max_iter=1000)`. Precision, recall, and F1 are computed via scikit-learn's standard functions on the held-out 8-example test set.

### 6.7.5 The numbers

From `poc_spike7_output.json`:
```
precision: 0.25
recall: 0.25
f1: 0.25
```

The test-set ground truth (`y_test`) was `[0, 1, 1, 0, 1, 0, 0, 1]` — 4 clean, 4 corrupted. The model's predictions were `[1, 0, 0, 1, 1, 1, 0, 0]`.

### 6.7.6 Walking the confusion, position by position

| Position | True label | Predicted | Correct? |
|---|---|---|---|
| 1 | 0 (clean) | 1 | ❌ |
| 2 | 1 (corrupted) | 0 | ❌ |
| 3 | 1 (corrupted) | 0 | ❌ |
| 4 | 0 (clean) | 1 | ❌ |
| 5 | 1 (corrupted) | 1 | ✅ |
| 6 | 0 (clean) | 1 | ❌ |
| 7 | 0 (clean) | 0 | ✅ |
| 8 | 1 (corrupted) | 0 | ❌ |

Only 2 of 8 predictions are correct overall. On 4 positives / 4 negatives, a naive coin-flip classifier would land somewhere near 0.5 precision/recall by chance — meaning 0.25 is actually somewhat *below* what pure chance might produce, though at n=8 this distinction carries essentially no statistical weight either way.

### 6.7.7 The honest caveat, embedded directly in the JSON

```
"honest_caveat": "n=20 total, n_test=8 — this is a directional signal check on
hand-written examples, not a real accuracy claim. The real test needs labeled
pairs generated by the actual fault-injection harness (extension #1), not
authored by hand."
```

### 6.7.8 Why this matters — two plausible, un-distinguished explanations

Near-random performance on a tiny, hand-authored dataset has at least two plausible explanations, and the spike itself cannot distinguish between them:

1. **The sample is too small and unrepresentative.** 8 test examples is nowhere near enough for a logistic regression model to learn a robust decision boundary, and hand-authored corruption examples may not resemble what the real fault-injection harness (extension #1, still unbuilt at the time of this spike) actually produces.
2. **Bag-of-words TF-IDF features may genuinely be too weak.** Many of the corrupted examples differ from their clean counterparts by small, semantically subtle changes — a missing qualifying clause, a slightly different framing — that n-gram counting alone may not reliably surface, especially with only 12 training examples to fit a full TF-IDF vocabulary against.

This spike's design cannot separate these two explanations, and it does not pretend to.

### 6.7.9 What the negative result does and does not rule out

The reproducibility of this result is worth noting: the spike was re-run twice and produced byte-identical results both times. Because `random_state=42` is fixed on the train/test split, and `LogisticRegression` with default settings is itself deterministic given fixed input features, this is expected, not a coincidence — but it does confirm the near-random result is a stable property of this exact setup (this data, these features, this split), not noise from an unseeded random process. That rules out "we just got an unlucky split" as a standalone explanation. It does **not** rule out "this specific hand-written dataset happens to be unlucky or unrepresentative," which is a different, still-open claim.

### 6.7.10 The recorded, honest status

Risk-register R15 records this precisely: "Precision 0.25, recall 0.25, f1 0.25 — near-random, not a working classifier yet. Honest negative-leaning result, not hidden." The plan doc's own Weeks-8–14 FYP-2 slot for this extension is marked explicitly "contingent, not automatic": before committing that slot, the team must re-test with real labeled pairs from the fault-injection harness, and if TF-IDF still fails, try cheap local sentence-embedding features (still no API cost) before concluding the classifier needs something heavier. If it still doesn't improve after both attempts, the plan doc's own instruction is explicit: "drop it rather than ship a known-broken classifier."

### 6.7.11 What the team still owes

This is the spike with the most explicitly unresolved fate of any in the set of eight. Two concrete follow-up experiments are named and neither has been run: re-test with real labeled pairs generated by the fault-injection harness once it exists, and if that still fails, try cheap local sentence-embedding features in place of raw TF-IDF, still without introducing any API cost. Only after both attempts fail should the extension actually be dropped — as of this write-up, neither follow-up experiment has been run, so the honest status of extension #5 remains genuinely undecided, not merely "pending" in a routine sense.

### 6.7.12 Sub-questions a skeptical reviewer would ask

**"Isn't n=20 so small that 'near-random' and 'genuinely broken' are indistinguishable from noise?"** This is true, and it's exactly why the spike's own `honest_caveat` field frames this as "a directional signal check... not a real accuracy claim," and why §6.7.11 lists a real-scale re-test as an owed follow-up rather than treating 0.25 as a settled final verdict on TF-IDF's viability. What the n=20 result *does* rule out, given the deterministic reproducibility discussed in §6.7.9 above, is "we got unlucky with this particular random split" — a re-run with a different seed on this same tiny dataset would very likely produce an equally uninformative number, for the same reason: not enough data for 12 training examples to teach a linear model a real decision boundary, regardless of which 12 get picked.

**"Given the corrupted examples were hand-written by the same team that also designed the fault taxonomy they're supposed to test, is there a risk the examples are unrepresentative of what a real fault-injection harness would produce?"** Yes, and this is explicitly the first of the two candidate explanations named in §6.7.8 above, not a new concern raised here for the first time. It is also precisely why the plan doc's own contingency for this extension requires re-testing against harness-generated pairs before any further conclusion is drawn — hand-written examples by design tend to be either too obviously corrupted (easy) or too subtly different (hard) in ways that may not match a systematic corruption operator's actual output distribution.

**"If this classifier gets dropped, does anything else in the frozen feature list depend on it?"** No — extension #5 is explicitly gated behind the core being complete first, and nothing else in the 10-item foundational core or the other 7 extensions references or depends on the preventive classifier's output. Dropping it, if the two named follow-up experiments both fail, would not create any downstream gap elsewhere in the architecture — a clean, low-blast-radius feature to have a contingent fate, which is one reason the plan doc's own explicit "drop it rather than ship a known-broken classifier" instruction is a genuinely low-risk one to follow if it comes to that.

---

## 6.8 Spike 8 — Repair Agent

### 6.8.1 What — the specific assumption under test

This is the newest of the eight spikes, run 2026-08-24, and closes the most recently-discovered gap in the entire feature set. When the team reviewed `Agentic_AI_Market_Survey_BS_FYP.docx` — a market survey of 7 orchestration frameworks plus a fresh read of ErrorProbe — three of its four recommended pipeline modules ("Root-Cause Localizer," "Verification Agent," and parts of its closed loop) already matched mechanisms already present in Granite's frozen feature list under different names. The plan doc treats this as independent convergence on the same architecture, not new information.

One module genuinely did not exist anywhere in the prior list: **Repair Agent**, the specific step that *generates* a candidate correction, as opposed to verifying one or replaying one.

### 6.8.2 Why this gap had been hiding in plain sight

Functional requirement 4, in the plan doc's own §0.07, already reads: "given a candidate corrected value for a specific step, deterministically re-execute the downstream portion of the trace and report whether the corrected trace now succeeds." The requirement text itself *assumes* a corrected value is given — nothing upstream in the prior feature list ever specified how that value gets produced. Spike 5 proved the *replay* half of this chain works mechanically. Nothing until this spike tested the *generation* half at all.

### 6.8.3 Independent market evidence for the novelty of this gap

The survey's own feature matrix rates "Automatically generate repair" as Not native / Custom / Experimental across every one of the 7 surveyed frameworks — nobody ships this as a built-in capability. This is not a gap the team invented to fill a slide; it is a gap independently visible in the commercial and open-source framework landscape.

### 6.8.4 How — the setup

Read from `poc_spike8_repair_agent.py`: this spike is explicitly designed to chain directly into spike 5's replay logic, matching the intended real pipeline shape (generate a fix, then verify it by replaying). The backbone is the same free local `llama3.2:3b` via Ollama used throughout every other spike.

Six synthetic single-step correction cases are defined, each with:
- `task` — a description of what the pipeline was doing
- `wrong_value` — the diagnosed-incorrect value from an earlier pipeline stage
- `evidence` — a specific quoted fact from elsewhere in the trace that unambiguously pins down the correct value
- `true_value` — ground truth
- `downstream` — a lambda function taking the generated correction and computing whether the final pipeline outcome now passes, directly mirroring spike 5's replay pattern

The model is deliberately not required to *discover* evidence — only to *use* given evidence, since evidence-discovery is Verification Agent's job, not Repair Agent's. This is an important scope boundary: this spike isolates fix-generation-from-given-evidence, not evidence-gathering.

### 6.8.5 How — the prompt and the two metrics

The prompt template frames the model explicitly as "a Repair Agent in a multi-agent AI diagnosis system," states the task, the wrong value, and the evidence, and asks for strict JSON: `{"corrected_value": <number>, "reasoning": "<one short sentence>"}`. Parsing uses the same `extract_json()` regex-and-`json.loads()` pattern seen in spike 1.

Two metrics are computed, deliberately kept separate and matching the market survey's own Table 4 definitions exactly:

- **`repair_success_rate`** — does the generated fix, once fed through the case's `downstream` function, produce a *passing* final result (does not require exact numeric match to ground truth)
- **`exact_match_rate`** — does the generated value exactly equal the true value (stricter, reported separately, never conflated with repair success)

### 6.8.6 The six cases, briefly

| Case | Wrong value given | Evidence given | True value | Downstream check |
|---|---|---|---|---|
| tax_total | price = $90.00 | receipt: "$100.00" | 100.0 | total with 8% tax vs. $108.00 |
| loyalty_discount | discount = 5% | customer msg: "15% loyalty discount" | 15.0 | refund vs. $38.25 |
| stock_count | stock = 12 units | warehouse doc: "21 units" | 21.0 | raw value vs. 21.0 |
| notebook_order | qty=5, total=$20.00 | customer msg: "7 notebooks" | 7.0 | total ($4×qty) vs. $28.00 |
| connecting_flight | arrival hour = 13 | schedule: "arrives at 14:00" | 14.0 | hour+2 vs. 16.0 |
| budget_check | item cost = $240.00 | invoice: "$420.00" | 420.0 | raw value vs. 420.0 |

### 6.8.7 The numbers

From `poc_spike8_output.json`:
```
n_cases: 6
n_parse_failures: 0
exact_match_rate: 0.667
repair_success_rate: 0.667
```

4 of 6 cases succeeded on both metrics — the same 4, confirmed by checking the per-case table below. Both metrics landed at exactly the same value because, in this particular run, every case that achieved an exact match also achieved downstream repair success, and every case that missed the exact match also failed downstream. That is not guaranteed to always be true in general (a close-but-inexact numeric match could still pass a downstream tolerance check in other pipelines), but it happened to hold here.

| Case | True value | Generated value | Exact match? | Repair success? |
|---|---|---|---|---|
| tax_total | 100.0 | 100.0 | ✅ | ✅ |
| loyalty_discount | 15.0 (%) | **6.75** | ❌ | ❌ |
| stock_count | 21.0 | 21.0 | ✅ | ✅ |
| notebook_order | 7.0 | **28.0** | ❌ | ❌ |
| connecting_flight | 14.0 | 14.0 | ✅ | ✅ |
| budget_check | 420.0 | 420.0 | ✅ | ✅ |

### 6.8.8 Failure case 1 — `loyalty_discount`, examined in full

The task asks the model to correct a wrong discount percentage (`wrong_value = "discount = 5%"`) given evidence quoting the customer: *"I have the 15% loyalty discount on my account."* The pipeline's `downstream` function needs the raw percentage `15.0` as input — it computes `45.00 * (1 - pct/100)`.

The model's actual raw output, quoted verbatim from the JSON:
```json
{"corrected_value": 6.75, "reasoning": "15% of $45.00 is $6.75"}
```

Read the reasoning field carefully: the model got the underlying fact exactly right. It correctly identified 15% as the discount rate from the evidence. But then, unprompted, it went one computational step further and returned the *dollar amount of the discount itself* ($6.75) rather than the percentage the pipeline actually needed as its parameter.

Replayed downstream, `6.75` gets treated as if it were a percentage: `45.00 * (1 - 6.75/100) = 41.96`, nowhere near the expected `38.25`. The repair fails — but not because the model reasoned incorrectly about the underlying facts.

### 6.8.9 Failure case 2 — `notebook_order`, examined in full

The task asks the model to correct a wrong order total (`wrong_value = "quantity = 5 notebooks, so total = $20.00"`) given evidence quoting the customer: *"I would like 7 notebooks please."* The pipeline's `downstream` function needs the raw quantity `7.0` — it computes `qty * 4`.

The model's actual output:
```json
{"corrected_value": 28.0, "reasoning": "Total cost is quantity times price per notebook ($4 x 7 = $28)"}
```

Again, the underlying fact is exactly right — the model correctly read "7 notebooks" from the evidence — but it returned the *computed total* ($28.00) rather than the *quantity parameter* (7) the downstream function actually needed.

Replayed downstream, `28.0` gets treated as a quantity: `28.0 * 4 = 112.0`, nowhere near the expected `28.0`. (Note the darkly amusing coincidence that the model's wrong output value, 28.0, happens to numerically equal the *expected downstream total* for this specific case — a pure coincidence of these particular numbers, not a sign of anything deeper about the model's reasoning.)

### 6.8.10 Both failures share one precise root cause, not two

Both failures are, precisely, the same failure mode: the model correctly extracted the right underlying fact from the evidence in both cases — it never got 15% or 7 notebooks wrong — but returned the *downstream computed result* of applying that fact, rather than the *specific atomic parameter* the pipeline's interface actually expected. This is a specification/interface ambiguity in what "corrected_value" is defined to mean, not a factual-reasoning failure. The model's reasoning field in both failing cases demonstrates it understood the evidence correctly; it simply resolved the ambiguity in "what value do you want" the wrong way, computing one step further than the interface required.

### 6.8.11 Why this matters

This is the second spike (alongside spike 3's first attempt) whose most valuable output is a precisely-diagnosed failure mode rather than a clean pass, and it closes risk-register R17. The mechanism genuinely works more often than not — 4 of 6 successful repairs on a free, weak, local 3B model, with zero JSON parse failures across all six cases, is a real positive signal for the foundational viability of Repair Agent as a mechanism.

But the finding that matters most for the actual build is the shared root cause of the two failures: Repair Agent's real interface needs to pin down exactly which atomic field is being corrected — the same way Error Step Localization already pins down a specific step index rather than leaving "which step" ambiguous — instead of leaving "the corrected value" open to being read as either a raw parameter or a computed downstream answer. This is a genuinely actionable, specific fix for the real system design, not a vague "the model needs to be smarter" conclusion.

It also directly informs the API-usage budget table in architecture-sketch.md, where Repair Agent is explicitly classified as inherently API-dependent (a generation task, not a deterministic rule) — this spike is the first real evidence of what that API dependency actually costs in accuracy terms on a weak backbone, and precisely where it breaks down.

### 6.8.12 What the team still owes

The concrete fix — tightening the prompt/interface specification to explicitly name the exact atomic field being corrected (e.g., "return the discount PERCENTAGE, not the discount amount," or more generally a schema that names the specific parameter type expected) — has been identified but not yet implemented or re-tested. A follow-up run with a corrected prompt interface, checked against the same 6 cases (or a larger set), is the natural next step to confirm the fix actually resolves both failure instances rather than just one.

Beyond that, this spike used a deliberately easy evidence-retrieval setup — the correct fact is always given verbatim and unambiguously. A harder, more realistic test would require Repair Agent to work from evidence gathered by an actual Verification Agent stage rather than hand-curated quotes, which hasn't been tested at all yet.

### 6.8.13 Sub-questions a skeptical reviewer would ask

**"Both failures happen to be percentage/quantity-vs-computed-value confusions — is this really 'one root cause,' or just two superficially similar cases?"** Look at the actual mechanism, not just the surface similarity of the numbers involved. In both cases the model's `reasoning` field explicitly shows it performing an extra multiplication step the task never asked for — `"15% of $45.00 is $6.75"` and `"$4 x 7 = $28"` — meaning in both cases the model treated "give me the corrected value" as an implicit invitation to compute a derived answer, not merely happening to land on similar-looking wrong numbers by coincidence. That is a mechanistic similarity, not just a numerical one, which is why treating it as one root cause (an interface/specification ambiguity) rather than two is the accurate reading, not an oversimplification.

**"Why did the model NOT do this on the other 4 cases — what made tax_total, stock_count, connecting_flight, and budget_check unambiguous where the other two weren't?"** Looking at the four successful cases, each asks for a value that has no obvious "next computation" attached to it in the task framing: a price (`tax_total`), a stock count (`stock_count`), an hour (`connecting_flight`), a cost (`budget_check`) — in each of these, the evidence directly states the exact value needed, with no natural further arithmetic step suggested by the surrounding context. In the two failures, by contrast, the task language itself invites a further computation — "compute a refund... minus the loyalty discount" and "compute the total cost of the customer's order" — meaning the ambiguity is not purely about the value type in isolation, but about how naturally the task's own framing suggests one more arithmetic step past the evidence-stated fact. This is a genuinely useful refinement of the finding: the interface ambiguity is likely to bite hardest specifically when a task description names a downstream computation and the correction target is an input to that computation, not the computation's own output.

**"With n=6 and 0 parse failures, is the API-reliability part of this spike (JSON formatting) actually validated, or just lucky?"** Zero parse failures out of 6 attempts, on a 3B model instructed to return strict JSON with no surrounding prose, is a genuinely encouraging sign for prompt-engineering reliability specifically — this is a separate axis of success from repair-value correctness, and it is fully validated at this small scale: every single response was syntactically well-formed JSON matching the expected schema. This should not be conflated with the semantic-correctness question (which is where the 2 failures occurred) — the two are independent properties of the pipeline, and this spike happens to report a clean result on one and a partial result on the other.

---

## 6.9 Summary table — all 8 spikes at a glance

| # | Spike | Core mechanism tested | Headline number(s) | Verdict |
|---|---|---|---|---|
| 1 | ErrorProbe reproduction | 2-stage Strategist→Arbiter, local 3B, n=8 real Who&When cases | agent_accuracy 0.75, step_accuracy 0.0 (**scorer bug — true number unknown**) | Partial — real positive signal at agent level, step-level metric currently unreliable |
| 2 | CrewAI instrumentation | Post-hoc trace capture from a real CrewAI run into the execution-graph model | 3 nodes, 2 edges, correctly ordered | Clean resolved positive |
| 3 | Fault injection | Deterministic corruption of a single node, ground-truth recoverability | Attempt 1: self-corrected (informative negative); Attempt 2: `propagated_blindly`, fully recoverable | Resolved — both outcomes kept as design lessons |
| 4 | Silent-failure detector | Rule-based constraint check (zero LLM calls) against 3 real word problems | 0/3 natural silent failures observed; mechanism separately confirmed to flag known-wrong values with 0 false positives | Mechanism validated; real-world frequency still unmeasured |
| 5 | Counterfactual replay | Deterministic 3-step pipeline, corrected input re-executed downstream | `recovery_success: true` (97.2 → 108.0) | Mechanism proven, narrow scope (no LLM involved) |
| 6 | Cyclic graph handling | Bounded backward BFS trace on a true cycle, with a negative control | Bounded: terminates cleanly, all nodes reached; unbounded control: hits 10,000-step cap | Proven, including proof the bound is load-bearing |
| 7 | Preventive classifier | TF-IDF + logistic regression on 20 hand-written handoff examples | precision 0.25, recall 0.25, f1 0.25 | Honest negative result — fate undecided, 2 follow-ups still owed |
| 8 | Repair Agent | LLM generates a corrected value from evidence, chained into spike 5's replay | repair_success_rate 0.667 (4/6), exact_match_rate 0.667 (4/6) — both failures share one diagnosed interface-ambiguity cause | Works more often than not; precise, actionable fix identified, not yet applied |

---

## 6.10 What the team still owes, across the whole set

Pulling every open item from the eight individual write-ups above into one place, because several of these are genuinely blocking for the next planning gate (Mid-1) and are easy to lose track of scattered across eight separate sections.

### 6.10.1 Spike 1's scorer bug

Must be fixed and re-run before step accuracy is cited anywhere. The current `step_accuracy: 0.0` reflects a type mismatch (string ground truth vs. integer prediction) that guarantees every comparison fails regardless of correctness — case 6 is direct proof, where the numerically exact prediction (step 5) was scored as wrong because `5 == "5"` is `False` in Python. This is a near-zero-cost fix (normalize types, re-run the existing 8 cases with no new compute), and it should happen before the number appears in any further presentation material.

### 6.10.2 The full 3-stage ErrorProbe reproduction

Remains unbuilt, independent of the scorer bug. Tool-grounded Investigator plus Verified Episodic Memory — this is the explicit Weeks-6–10 Mid-1 priority in the plan doc's own timeline.

### 6.10.3 Spike 4's detector needs scale

A larger sample with real injected near-misses, not just naturally-occurring mistakes (0 of 3 in this run), before detection precision/recall can be reported as a real evaluation number rather than a small direct mechanism test.

### 6.10.4 Spike 5's replay mechanism needs real-trace testing

Against real (non-toy, non-deterministic) benchmark traces, where downstream steps are LLM-generated rather than hand-written Python functions, and against non-linear graph structures, not just a single 3-step chain.

### 6.10.5 Spike 6's cycle-handling mechanism needs real-trace validation

Against a real captured LangGraph trace containing an actual retry loop, not just synthetic `networkx` test graphs — this is the extension's own stated acceptance bar, not yet met.

### 6.10.6 Spike 7's preventive classifier has a genuinely undecided fate

Two specific follow-up experiments are named and neither has run: re-test with real fault-injection-harness-generated pairs (not hand-written), and if that still fails, try cheap local sentence-embedding features. Only after both fail should the extension be dropped, per the plan doc's own explicit instruction.

### 6.10.7 Spike 8's identified interface fix

Has not yet been implemented or re-tested. A follow-up run against a corrected prompt/schema, checked against the same or an expanded case set, is the natural next step.

### 6.10.8 Verified Repair Memory's re-test is still pending, tied to a deleted prototype

This is not one of the eight numbered spikes above, but it belongs in this list because it is the other item (alongside spike 7) whose committed-core status rests on an explicit condition that has not yet been met.

Recorded in risk-register R18/R22: a full 3-stage pipeline prototype including a memory component (`poc_spike1b_full_pipeline.py`) was built once, on 2026-08-23, run against all 8 real Who&When cases, and produced a genuinely bad result:

- 0 of 8 cases ever committed anything to memory
- all 24 hypothesis-verifications across those cases came back `NOT_SUPPORTED` on the local 3B backbone
- agent-level accuracy *regressed* from 75% (spike 1's simpler 2-stage version) down to 50% in that same run

The prototype file itself was subsequently deleted at explicit user instruction — R18 is the only remaining record that this was ever built, tested, and reverted, and it notes candidly that the finding was supposed to be logged at the time but the edit attempt failed silently and was never retried.

Verified Repair Memory was nonetheless reclassified from an extension into the foundational core on 2026-08-24 (R22), on the explicit condition that a re-test on a stronger LLM backbone happens before Mid-1. If that re-test also fails, risk-register R22 states plainly this becomes "a foundational-item gap the team must be ready to explain under questioning... not a footnote" — the one real test result stays on record as a failure, not softened just because the item is now core.

No re-test has happened yet as of this write-up, and there is no working prototype currently in the codebase to re-test with — it would need to be rebuilt from scratch on a stronger backbone before the condition can even begin to be satisfied.

### 6.10.9 Two structurally different open items

Two of these eight open items — spike 7's classifier and Verified Repair Memory — are structurally different from the rest. They are not just "more testing owed"; they are committed-core-or-extension features whose continued inclusion in the frozen feature list is conditioned on evidence that does not yet exist. Both should be treated as genuinely open questions at the next planning gate, not as settled scope.

---

## 6.11 A consolidated map — every one of the 20 frozen features against its spike evidence

The plan doc's own §7.0 freezes a 20-item list: 10 foundational mechanisms, 8 extensions, and 2 explicitly deprioritized items. The eight spikes above were never meant to cover all 20 — several extensions are gated behind the core being finished first, and two foundational items (Recovery Controller, and Verified Repair Memory's re-test) were reclassified into the core after most of the spike work had already run. What follows is the full list, laid out once in one place, so the coverage picture — what has real evidence, what has partial evidence, and what has none at all — is visible at a glance rather than scattered across nine separate write-ups.

### 6.11.1 The 10 foundational items

| # | Foundational item | Spike evidence | Status |
|---|---|---|---|
| 1 | Fault-injection harness | Spike 3 (both attempts) | Resolved — mechanism proven, both self-correction and blind-propagation outcomes documented |
| 2 | Cross-architecture benchmark | Spike 2 (CrewAI mapping) | Partial — one framework instrumented cleanly; the actual 500–1,000-trace benchmark itself is unbuilt |
| 3 | Culprit Agent (agent-identification half) | Spike 1 | Partial — 0.75 agent accuracy on a simplified 2-stage pipeline, free weak backbone |
| 4 | Error Step Localization (step-identification half) | Spike 1 | Unreliable as currently scored — the step-accuracy figure is invalidated by the type-mismatch scoring bug documented in §6.1.7 |
| 5 | Verification Agent (tool-grounded evidence-gathering) | None directly | Not built — Spike 1's 2-stage simplification explicitly cuts this stage out; it is the named Weeks-6–10 Mid-1 priority |
| 6 | Repair Agent | Spike 8 | Partial — repair_success_rate 0.667 (4/6), both failures traced to one fixable interface-specification issue |
| 7 | Semantic Error Diagnostic | Spike 4 | Mechanism validated (zero false positives on known-wrong values in a direct test); real-world catch rate on naturally-occurring failures unmeasured (0/3 in the spike run itself) |
| 8 | Verified Automatic Repair | Spike 5 | Mechanism proven on a deterministic toy pipeline; real-benchmark and non-linear-graph testing still owed |
| 9 | Recovery Controller | None | Zero POC evidence — genuinely new mechanical work, only a precedent check (5 of 7 surveyed frameworks have generic, non-repair-tied checkpoint infrastructure) |
| 10 | Verified Repair Memory | One real test, and it failed | 0 of 8 cases committed anything to memory; agent accuracy regressed 75%→50%; re-test on a stronger backbone owed before Mid-1 (§6.10.8) |

Six of the ten foundational items have at least some direct spike-level evidence. Two (Verification Agent, Recovery Controller) have none at all. One (Verified Repair Memory) has evidence, and the evidence is a documented failure. This is worth stating plainly rather than letting the six-of-ten framing read as "60% done" — a foundational item with zero evidence and a foundational item with one failed test are both still open risk, just open in different ways, and neither should be quietly counted as equivalent to the six that at least have a partial positive signal behind them.

### 6.11.2 The 8 extensions

| # | Extension | Spike evidence | Status |
|---|---|---|---|
| 1 | Widen fault taxonomy to 3 types | Spike 3/3b (1 of the eventual 3 types validated) | Partial — the corrupted-tool-output type is proven; communication corruption and context truncation are unbuilt |
| 2 | 3rd architecture (generalization) | None yet | Unstarted — gated behind the core |
| 3 | Cyclic/dynamic graph support | Spike 6 | Mechanism proven on synthetic test graphs; real-LangGraph-trace validation (the extension's own stated bar) not yet met |
| 4 | Confidence calibration | None | Unstarted — no spike directly exercises confidence-score computation yet, though the underlying graph-feature formula (out-degree, betweenness centrality) is named in the architecture sketch |
| 5 | Preventive clarification classifier | Spike 7 | Honest negative result — near-random (0.25 precision/recall/F1); fate genuinely undecided pending two named follow-ups |
| 6 | Failure Propagation Map | None | Unstarted |
| 7 | Explainable Confidence Reasoning | None | Unstarted |
| 8 | Framework Compatibility Layer | None | Unstarted — no POC yet, per the plan doc's own note |

Only 2 of the 8 extensions have any direct spike evidence at all, and one of those two is the project's single clearest negative result. This is expected and by design — the plan doc is explicit that extensions are gated behind the core being complete first — but it is worth stating directly rather than leaving it implied: the extension layer, as a whole, remains almost entirely a design commitment rather than a tested one at this stage, with cyclic-graph support as the one extension that has moved meaningfully past the design-only stage.

### 6.11.3 The 2 deprioritized items, and the 2 design proposals still awaiting their first spike

Cross-Domain Transfer Testing and Chaos Testing for Agents are explicitly parked, not planned around — no spike evidence exists or is currently owed for either.

Separately, two further mechanisms were proposed after the original spike round — Cross-Agent Consistency Verification and Constraint Provenance Tracing, both complementary strategies for the Semantic Error Diagnostic module, logged 2026-08-23 and discussed in full in Part 4's market-gap worked scenarios (§4.3's Scenario 2 and Scenario 3 material). Both are rule/graph-based (fitting the 0%-API commitment the same way Spike 4's constraint checker does), and both remain, as of this write-up, unimplemented and unverified design proposals — nothing has been built or spiked for either one yet. They are named here again because they belong in the same "what's actually been tested versus merely designed" accounting as the rest of this section, not because anything new about them is being claimed.

---

## 6.12 Two full worked traces — watching the mechanisms actually run

The numeric tables in §6.5 and §6.6 above report what happened in Spikes 5 and 6. What follows is the same evidence, narrated as a continuous story rather than a table, because a reader trying to build real intuition for *why* these two mechanisms matter benefits from watching the failure happen and then watching the fix work, step by step, in the same concrete terms used throughout the plain-English introduction to this document.

### 6.12.1 Worked trace — Spike 5, counterfactual replay recovering a corrupted price

**The setup.** A 3-step pipeline processes a purchase: step 1 extracts a price from a receipt, step 2 applies an 8% tax to that price, step 3 checks the final total against an expected value of $108.00 and reports pass or fail. The true price on the receipt is $100 — with 8% tax, $100 × 1.08 = $108.00, which matches the expected total exactly.

**What goes wrong.** A fault is injected at step 1: instead of extracting the true $100, the corrupted version of step 1 reports $90. Nobody downstream has any way of knowing this is wrong — step 2 simply does its job, multiplying whatever number it's handed by 1.08: $90 × 1.08 = $97.20. Step 3 compares $97.20 to the expected $108.00, finds they don't match, and reports failure. From the outside, all a developer sees is: this pipeline run failed, with a final total of $97.20 instead of the expected $108.00. Nothing in that output, by itself, says *where* in the pipeline the number went wrong — only that it did.

**Why it matters.** This is exactly the situation the whole recovery-testing feature exists for: a diagnosis engine (in the real system, Culprit Agent and Error Step Localization) has already done the work of figuring out that step 1 is the origin, and has proposed a corrected value. The open question this spike exists to answer is narrower and more basic than "can the system figure out the right fix" — it is "if you're handed the right fix, does actually applying it and re-running the downstream steps produce the correct final answer, or could the replay machinery itself be broken in some way that would sink the whole feature regardless of how good the fix-generation step ever gets?"

**Step by step, what Granite's replay mechanism does.** First, the mechanism is handed the corrected value for step 1: $100, replacing the corrupted $90. It does not re-run step 1 itself — step 1's job (extracting a price from a receipt) is already done; the correction stands in for a re-verified answer to that step. Second, it re-executes step 2 fresh, using the corrected $100 as input: $100 × 1.08 = $108.00. Third, it re-executes step 3 fresh, comparing this new $108.00 against the expected $108.00: they match, so step 3 now reports pass, where it had reported fail on the corrupted run.

**The result, read back against the JSON.** `original_correct_trace` (before any fault was ever injected) shows price=100 → total=108.0 → pass: true, confirming the pipeline is correctly built in the first place. `corrupted_trace` shows price=90 → total=97.2 → pass: false, confirming the injected fault really does break the pipeline's outcome, not just its intermediate values. `counterfactual_replay` shows price corrected to 100 → total=108.0 → pass: true, with `recovery_success: true` — the exact same downstream logic (the untouched step 2 and step 3 functions), given a corrected input, produces the correct answer.

**Why this narrow proof is still real evidence.** Nothing here proves an LLM can find the right correction on its own — that is a separate concern, addressed only partially by Spike 8. What this trace does prove, concretely and unambiguously, is that the *architecture* of "take a corrected value, re-run only what depends on it, trust the re-run result" is a sound pattern, at least for a simple linear chain. If this test had instead shown the replayed total still reading $97.20 — because, say, the replay logic accidentally re-used the stale corrupted value from the first run instead of the corrected one — that would have been a genuine, load-bearing architecture bug, and no amount of improving the fix-generation step later could have fixed it. The clean pass here rules that specific failure mode out.

### 6.12.2 Worked trace — Spike 6, a retry loop and the safety net underneath it

**The setup.** LangGraph, one of Granite's two committed core frameworks, natively supports workflows where an agent's output can be sent back to an earlier agent for another pass — a Critic reviewing a Researcher's work and asking for a redo, for instance. This spike builds a small trace shaped exactly like that: `Planner → Researcher → Critic → Researcher (again, the same node) → Writer → FAILURE`. The key structural detail is that the second `Researcher` step in that chain is not a new, separately-named node — it is the same `Researcher` node being revisited, meaning the graph genuinely contains a cycle: a back-edge from `Critic` pointing to a node that already appears earlier in the path.

**What goes wrong if nothing guards against this.** Backward causal tracing — walking from the observed `FAILURE` node back through its predecessors to find the true origin — is the mechanism the whole diagnosis engine depends on. A naive backward walk on a graph with a cycle has no natural stopping point: from `FAILURE`, it visits `Writer`, then `Critic`, then `Researcher`, then back to `Critic` (because `Researcher` was reached via the cycle and `Critic` is again one of its predecessors), then `Researcher` again, and so on, forever, unless something explicitly bounds how many times a node can be revisited during the walk.

**Why it matters.** This is not a hypothetical concern invented to give the spike something to test — it is a direct, structural consequence of a framework Granite has already committed to supporting. A backward-tracing mechanism that hangs the moment it encounters a real LangGraph retry loop would make the entire diagnosis pipeline unusable on one of the project's own two core target frameworks, silently, the first time a real user's workflow included a retry.

**Step by step, what Granite's bounded traversal does.** The traversal starts at `FAILURE` and walks backward through each node's predecessors, keeping a running count of how many times each individual node has been visited. The bound is set to 3 revisits per node for this test. Reading the actual visited-order sequence recorded in the spike's output — `FAILURE, Writer, Critic, Researcher, Planner, Critic, Researcher, Planner, Critic, Researcher, Planner, Critic` — shows the traversal genuinely oscillating back and forth between `Critic`, `Researcher`, and `Planner` exactly as the cycle would produce, not skipping past it. It visits `Researcher` three times and `Critic` four times before its expansion from those nodes stops, at which point the traversal has already reached all 5 distinct nodes in the graph — `Planner`, `Researcher`, `Critic`, `Writer`, `FAILURE` — so nothing was missed, and the walk terminates cleanly rather than needing to be forcibly cut off.

**The negative control, which is what actually proves the bound is doing real work.** The same exact graph, same starting node, is walked again with the revisit bound effectively switched off (set to a billion). This time there is nothing to stop the oscillation between `Critic` and `Researcher`, and the traversal runs until it hits a separate, unrelated hard safety cap of 10,000 total steps and has to be forcibly terminated — `terminated_cleanly: false`. Nothing else about the graph or the starting point changed between the two runs; only the bound parameter did, and the outcome flipped from a clean, complete traversal to a runaway one. That contrast is the actual proof: a small graph like this one is not inherently well-behaved on its own — the bound is the thing keeping it well-behaved, and removing it produces exactly the failure mode the mechanism exists to prevent.

**A note on what this trace does not yet prove.** Spike 6's own honest limitation (§6.6.8) still applies here: this is a hand-built `networkx` graph shaped like a realistic LangGraph retry pattern, not a trace captured from an actual running LangGraph workflow. The mechanism is proven; validating it against a real captured trace containing a genuine loop is the concrete next step, and the extension's own stated acceptance bar has not technically been met yet.

---

## 6.13 Cross-references — connecting the spike evidence back to Parts 1–3 and Parts 4–5

Each spike above was written up on its own terms — what it tested, what happened, why it matters for that one mechanism. This section pulls the same eight results back into the two earlier arguments this document already makes at length: the Seoul Accord CCP case built in Parts 1–3, and the market-gap case built in Parts 4–5. The point is not to repeat either argument, but to show explicitly which piece of spike evidence is actually doing the work behind each claim, since a panel is entitled to ask "where's the evidence for that" about any line in either earlier Part.

### 6.13.1 Against the nine CCP characteristics

Part 3's own closing synthesis table (§3.10) already names one piece of evidence per characteristic; expanded here with the fuller spike context behind each:

- **Characteristic 1 (Conflicting requirements).** The tension between diagnostic depth and latency — cited there via extension #6's two-mode design — is the same tension Spike 1's own elapsed-time data (§6.1.12: 49.9 to 121.3 seconds per case on CPU-bound local inference) gives an early, if rough, empirical shape to: longer trajectories cost more wall-clock time to diagnose, which is exactly the trade-off extension #6 is designed to let a user control.
- **Characteristic 2 (Depth of analysis).** Spike 1's own honest accounting of its scope cut — a 2-stage simplification of ErrorProbe's real 3-stage pipeline, explicitly not claimed as full fidelity — is itself a demonstration of the kind of layered, non-trivial reasoning the characteristic asks for: recognizing which parts of a published method can be cheaply tested first and which require deeper investment later.
- **Characteristic 3 (Depth of knowledge).** Spike 1's reproduction had to be built from ErrorProbe's methodology description alone, since its code is not public — the same fact Part 3 cites directly, and the specific reason the 2-stage simplification (§6.1.4) was a necessary engineering judgment call rather than a shortcut.
- **Characteristic 4 (Familiarity of issues).** Spike 4's n=3 result, with zero natural silent-failure occurrences, is cited directly in Part 3's table — and the fuller discussion in §6.4.7 above (the model simply got all three tricky problems right) is the concrete texture behind that one-line citation.
- **Characteristic 5 (Beyond standard practice).** Not directly spike-evidenced, but Spike 7's own honest negative result is worth naming here too: testing whether a "beyond standard practice, lightweight" approach (TF-IDF, no RL, no embeddings API) actually carries real signal, rather than assuming it does, is itself an instance of the rigor this characteristic asks for — the team tested the assumption before committing further engineering time to it, and reported the result even though it was disappointing.
- **Characteristic 6 (Stakeholder involvement — the one honestly-weak characteristic).** No spike closes this gap, and none could — it requires real people, not test data. Worth naming plainly: this is the one place in the whole spike program where "we should run a test" is not the applicable fix.
- **Characteristic 7 (Consequences).** Spike 3b's Riverside Hardware scenario and Spike 8's six correction cases (a discount rate, an order quantity, a flight arrival time, a budget figure) are all built from realistic, consequence-bearing domains — closing time, order fulfillment, budget compliance — matching Part 3's own citation of tau-bench-retail-sourced scenarios.
- **Characteristic 8 (Interdependence).** This is the characteristic Spike 6 speaks to most directly and most cleanly of all eight — Part 3's own table cites exactly the evidence walked through in full in §6.12.2 above: the 10,000-step cap hit when the revisit bound was disabled, proving the bound is load-bearing rather than coincidental.
- **Characteristic 9 (Requirement identification).** Part 3 cites Recovery Controller's zero-POC status as the example here — directly the same item flagged in §6.11.1's foundational-items table above as one of only two foundational mechanisms with no spike evidence behind it at all.

### 6.13.2 Against the Part 4–5 market gaps

Part 4's seven-platform and seven-framework survey names specific gaps no commercial tool or published paper closes; several of those gaps are the direct motivation for specific spikes, not a coincidental overlap:

- The finding that none of the seven commercial observability platforms cross-reference facts stated by independent agents against each other, or trace a claimed constraint back to a verifying node (§4.3's Scenario 2 and Scenario 3 material), is the direct motivation for the two design proposals named in §6.11.3 above — Cross-Agent Consistency Verification and Constraint Provenance Tracing — both still awaiting their first spike, a fact worth being direct about here: this is real, named, motivated future work, not evidence in hand yet.
- The finding that LangSmith Engine and Arize "Alyx" are both locked to their own vendor tracing stack, while Granite is framework-agnostic by design, is exactly what Spike 2 (CrewAI) and Spike 6 (LangGraph's native retry loops) together provide direct evidence for — not an assertion of framework-agnosticism, but two separate frameworks each shown working with the same underlying data model and traversal logic.
- The market survey's own feature matrix rating "Automatically generate repair" as Not native / Custom / Experimental across all 7 surveyed orchestration frameworks (§6.8.3 above) is the direct market evidence that Spike 8 fills a gap nobody else has closed as a built-in capability — not a novelty claim invented internally, but one independently visible in the commercial and open-source landscape the same survey already checked.
- The precedent check behind Recovery Controller (5 of 7 frameworks have generic checkpoint/resume infrastructure, but none tie resumption specifically to a verified-repair point) is the same evidence cited in risk-register R21 and in §6.11.1's foundational-items table — a gap independently visible in the framework landscape, with zero POC evidence yet on Granite's own side to close it.

---

## 6.14 Panel-style follow-up Q&A — the pattern across the three weaker results, taken together

Sections 6.3, 6.7, and 6.8 each already carry their own per-spike skeptical Q&A. What follows is a different, higher-altitude question: not "was Spike 7's near-random result well-analyzed" or "was Spike 8's failure well-diagnosed" individually, but what the *pattern* across all three — Spike 3's first attempt, Spike 7, and Spike 8 — says about the project as a whole, since a panel that has read the whole spike section is entitled to ask about the pattern, not just each instance.

**"You have three separate spikes that did not produce a clean positive result on the first attempt. Doesn't that pattern suggest something more systematically wrong with how these spikes were designed, rather than three unrelated model-scale issues?"** Looking at the actual root cause of each of the three, they are not the same failure mode wearing three different masks — they are three genuinely distinct lessons. Spike 3's first attempt failed because a well-known fact (Paris is the capital of France) gave the model's own general knowledge room to self-correct the injected fault, a problem specific to *which fact* was chosen for corruption, fixed by switching to an unverifiable, fabricated fact in Attempt 2. Spike 7 failed because a cheap bag-of-words feature representation, trained on only 12 hand-written examples, may simply lack the expressive power to separate subtly-corrupted messages from clean ones — a problem about *feature richness and sample size*, unrelated to fault-selection. Spike 8's two failures happened because the model resolved a genuine ambiguity in what "corrected value" means (a raw parameter versus a computed downstream result) the wrong way in two of six cases — a problem about *interface specification*, unrelated to either of the other two. If all three traced back to, say, "the local 3B model is just too weak to be trusted for anything," that would be one systemic finding wearing three faces. They do not: each has a different, specific, independently-verifiable cause, and two of the three (Spike 3, Spike 8) already have a concrete, named fix. That is a stronger position than either "everything worked" (which would invite suspicion of under-testing) or "one root cause explains three failures" (which the evidence does not actually support).

**"Isn't it convenient that every negative result gets explained away with a specific, fixable cause? At what point does 'we found the exact bug' stop being credible and start looking like post-hoc rationalization?"** The honest answer requires distinguishing the three cases from each other again, because they are not all at the same evidentiary strength. Spike 3's explanation is the strongest of the three — it was directly tested and confirmed by building Attempt 2 with the fix applied, which produced the predicted clean result (`propagated_blindly`, fully recoverable). Spike 8's explanation is well-supported by the model's own `reasoning` field in both failing cases, which explicitly shows it performing an extra computational step nobody asked for — but the fix (tightening the prompt/schema) has been identified and not yet re-tested, so this explanation, while well-grounded, remains unconfirmed by a follow-up run. Spike 7's case is the weakest of the three by design — the write-up in §6.7.8 explicitly names two competing explanations (sample size, feature weakness) and states plainly that the spike's design cannot distinguish between them. That gradation — one confirmed, one well-grounded but unconfirmed, one genuinely still open — is itself evidence against "explaining away," because a team rationalizing away bad results would have no reason to leave one of them explicitly unresolved rather than picking whichever story sounded best.

**"If Spike 7 genuinely can't be explained yet, why does the write-up spend so much space on it rather than simply re-running it with more data before publishing the result at all?"** Because the plan doc's own §12 requirement is that a POC must be demonstrated with evidence at the proposal stage — including negative evidence — not deferred until it looks better. Re-running Spike 7 with a larger, harness-generated dataset is explicitly named as the correct next step (§6.7.11), not skipped; the reason it has not happened yet is that the fault-injection harness needed to generate those pairs systematically (extension #1) did not itself exist yet at the time this spike ran. Publishing the honest 0.25 result now, with the two named follow-ups clearly stated as still owed, is the more defensible choice than either hiding the result until a better number is available, or waiting to publish anything until every dependency is built — the latter would mean the proposal defense itself would have no POC evidence for this extension at all, which is a worse position than an honestly-reported negative one.

---

## 6.15 Compute cost across the eight spikes — what actually ran, on what, for how long

The API-usage budget commitment discussed in §7.3 below is about the *real system's* target split. It's worth a separate, narrower note here about what the eight spikes themselves actually cost to run, since that is a different question — not "how much of the final product will depend on an LLM," but "what did proving each mechanism actually require in compute."

### 6.15.1 The two categories the eight spikes fall into

Five of the eight spikes (1, 3, 3b, 7, 8) call an LLM at least once — `llama3.2:3b` via a local Ollama install, the same free, weak backbone used throughout. Three of the eight (2 partially, 5, 6) are pure local computation with no LLM call anywhere in their core mechanism: Spike 5's replay logic is three deterministic Python functions; Spike 6's traversal is a `networkx` breadth-first search; Spike 7's *classifier itself* is scikit-learn's `LogisticRegression` over TF-IDF features, though the 20 training examples it learns from were themselves hand-written by the team rather than LLM-generated. The fourth session's own environment note records the exact versions this ran on: Python 3.13.7, `networkx` 3.5, `scikit-learn` 1.8.0, confirmed available locally, "no LLM API needed for any of these three [spikes 5, 6, 7] — all pure local computation, zero cost."

### 6.15.2 The timing data that does exist, read honestly

Only two of the eight spikes recorded per-case elapsed time in their output JSON, and neither was designed as a latency benchmark — both are incidental byproducts of the run, not a deliberate measurement.

Spike 1's 8 cases (Strategist + Arbiter calls combined, per case) ranged from 49.9 seconds (case 6, the shortest ground-truth trajectory) to 121.3 seconds (case 1), as already discussed in §6.1.12.

Spike 4's 3 cases (a single model call each, no multi-stage pipeline) recorded 39.7 seconds (`gift_card`), 15.3 seconds (`discount_then_tax`), and 18.4 seconds (`compound_trip`) — read directly from `poc_spike4_silent_failure_output.json`'s own `elapsed_sec` fields. The spread here is smaller than Spike 1's, consistent with these being single-call, single-stage prompts rather than a two-stage Strategist-then-Arbiter pipeline, though `compound_trip`'s own raw model output (visible in the same JSON, quoted in part in §6.4.5 above) shows a noticeably longer chain-of-reasoning than the other two cases, which likely accounts for at least some of its slightly higher time relative to `discount_then_tax`.

### 6.15.3 Why this is only a hint, not a real latency baseline

Neither of these two data points is a substitute for the real diagnostic-latency-overhead measurement §7.3 and §8.1.5 both name as still owed. Both are CPU-bound local inference on a 3B model run on whatever hardware the spikes happened to be run on, with no controlled comparison against a non-diagnosed baseline run, and no attempt to separate model-load time from actual inference time. What the two data points together do support, modestly, is the same directional read already drawn from Spike 1 alone in §6.1.12: trajectory and reasoning length appear to be the dominant cost driver, more than any fixed per-call overhead, which is a reasonable thing to keep in mind when extension #6's cheap-vs-full-pipeline latency trade-off eventually gets designed and measured for real.

---

# Part 7 — Architecture

## 7.1 The 3-owner subsystem breakdown

### 7.1.1 The correction that has to come first

Granite's architecture, as sketched in `architecture-sketch.md`, is organized around three subsystem "owner" role areas — not three people, a correction the document itself makes explicitly and repeatedly. The sketch's own annotation, dated 2026-08-23, reads: "the three boxes above are labeled by *role* (Data/Benchmark, Diagnosis, Platform) — earlier drafts numbered them 'Student 1/2/3' as if specific people were already assigned, which hasn't happened. Assign real owners before Mid-1 and update this diagram once decided."

This correction matters enough to restate plainly here, because it is easy to read a diagram with three cleanly labeled boxes and infer a settled roster that does not exist. Risk-register R6 tracks this as a genuinely open, higher-priority-than-previously-stated risk: "the three role areas... are defined in plan doc §9, but no specific team member has actually been assigned to any of them yet." Assumption A5 in the same register was corrected from "the 3-person ownership split stays stable across both semesters" (which assumed a split already existed) to the more honest "the three roles get assigned before Mid-1 and *then* stay stable" — there is nothing yet to "stay stable."

### 7.1.2 Data/Benchmark Owner — Fault Injection & Benchmark Engineering

**What this role owns:** multi-framework instrumentation (CrewAI, LangGraph, and a third framework via extension #2), the fault-injection operators (rule-based, deterministic corruption matching AgenTracer's own perturbation-operator approach), and the resulting ground-truth benchmark itself — target 500–1,000 labeled traces, to be released publicly under MIT or CC BY 4.0 licensing.

**Contribution type:** per Section 4's template, a **data/resource contribution**.

**What disappears if this role's work disappeared:** the consequence is total and specific, not partial — no cross-architecture evaluation would be possible at all, because there would be no ground-truth-labeled traces on any framework beyond whatever a diagnosis engine happens to be tested against ad hoc.

**Direct spike evidence:** Spike 2 (CrewAI mapping into the execution-graph model) and Spike 3 (fault injection producing recoverable, unambiguous ground truth — the second, corrected attempt) are the direct POC evidence this role's core mechanism works, at small scale, today.

### 7.1.3 Diagnosis Owner — Diagnosis Engine

**What this role owns:** execution-graph construction (structural parsing of trace reference identifiers, not LLM-judged), the ErrorProbe-derived attribution pipeline — split, per the 2026-08-23 rename, into its three real constituent parts (Culprit Agent, Error Step Localization, Verification Agent) rather than treated as one vague "core attribution algorithm" label — and the Semantic Error Diagnostic (the rule/schema-based silent-failure constraint-verification module, explicitly the single most important commitment in the entire API-usage budget table).

**Contribution type:** a **method contribution at an identified gap**.

**What disappears if this role's work disappeared:** both the core attribution algorithm and the silent-failure detection claim would vanish — the two things that make this project's CCP statement more than "reproduce a paper."

**Direct spike evidence:** Spike 1 (agent-level attribution at 75%, step-level currently unreliable pending a scorer fix), Spike 4 (the rule-based constraint-check mechanism, validated directly though not yet at scale), and Spike 6 (bounded backward tracing on cyclic graphs).

### 7.1.4 Platform Owner — Recovery Engine & Deployable Platform

**What this role owns:** the counterfactual replay / recovery-testing engine (Verified Automatic Repair), the Repair Agent's chained integration into it, the SDK, the backend API and trace/diagnosis-record store, the minimal dashboard, and containerized deployment (Docker, cloud VM or on-prem target).

**Contribution type:** a **system/architecture contribution** — which the guide itself notes is, for most Stream A projects, "the largest and most defensible contribution" (§A.3), because a working, installable product is harder to dismiss as "just gluing together known techniques" than an algorithmic tweak would be.

**What disappears if this role's work disappeared:** nothing about Granite would be installable or operable outside the developers' own machines — the entire deployable-product half of the project's contribution claim would be gone, leaving only a research prototype.

**Direct spike evidence:** Spike 5 (deterministic counterfactual replay, mechanism proven) and Spike 8 (Repair Agent generating candidate fixes at 0.667 repair success, chained directly into that replay logic). Notably, Spike 8's work spans both the Diagnosis Owner's territory (it is fed by the diagnosis pipeline's localized failure) and the Platform Owner's territory (its output feeds the replay engine), illustrating that these role boundaries, while useful for accountability, are not hermetically sealed from each other in practice.

### 7.1.5 The defensibility test nobody has rehearsed yet

Each of these three subsystems is meant to be independently defensible under the guide's Section 14.1 four-question test: explain it, justify alternatives rejected, predict what breaks if a specific input changes, and modify it under live questioning. None of that defensibility test has actually been rehearsed by anyone on the team yet — the plan doc's own §16 checklist item "each team member explains their own owned subsystem out loud, no notes" is marked as still open, and per R6, there isn't yet a specific "own" to attach to any team member in the first place.

## 7.2 The data-flow pipeline, stage by stage

The architecture sketch defines a 6-hop data flow. Below, each stage is restated with the specific spike evidence that backs its mechanism — no single spike tests the whole pipeline end to end; each spike tests one hop or sub-mechanism in isolation.

### 7.2.1 Stage 1 — Execute

The target multi-agent system (a user's own workflow, or a CrewAI/LangGraph toy workflow built for evaluation) runs, and instrumentation captures a raw execution trace as it goes.

**Evidence:** Spike 2 is the direct evidence this stage's output (a raw trace with node identity, agent/role labels, task descriptions, inputs, outputs, and timestamps) can be captured cleanly, at least post-hoc, from a real CrewAI run.

### 7.2.2 Stage 2 — Capture Trace → Build Graph

The raw trace is converted into an execution graph: nodes are agent actions/tool calls, edges are dependencies inferred by structural parsing of reference identifiers (matching GraphTracer's own published approach of "parse references, extract unique identifiers" — explicitly not an LLM asked "what did this depend on").

**Evidence:** Spike 2's own derived graph (3 nodes, 2 correctly-ordered edges, built purely from CrewAI's native `context=[...]` dependency declarations) is the direct evidence this conversion works without modification for at least one committed framework. Spike 6 extends this stage's coverage to the harder case of graphs containing genuine cycles, proving the same graph representation and a bounded-traversal algorithm built on top of it can handle LangGraph's native retry-loop pattern without hanging.

### 7.2.3 Stage 3 — Diagnose

This stage itself splits into two parallel sub-mechanisms rather than being one monolithic step: the Semantic Error Diagnostic (rule/schema-based task-constraint verification, catching silent failures) runs alongside backward causal tracing (pure BFS graph traversal from an observed failure point back through the dependency graph, producing a candidate root cause with a confidence score computed from graph features like out-degree and betweenness centrality — again, not LLM-judged).

**Evidence:** Spike 1 is the direct, if currently step-accuracy-unreliable, evidence for the attribution half of this stage (agent-level hypothesis generation and arbitration). Spike 4 is the direct evidence for the Semantic Error Diagnostic half — the rule-based constraint checker, confirmed to correctly flag known-wrong values with zero false positives in a direct mechanism test, though its real-world catch rate on naturally-occurring failures remains unmeasured (0 of 3 cases in the actual spike run were naturally wrong). Spike 6's bounded backward traversal is also load-bearing evidence for the causal-tracing half specifically.

### 7.2.4 Stage 4 — Generate Fix

Once a root cause is localized and (ideally) verified, Repair Agent generates a candidate fix — a corrected prompt, tool argument, structured output, or function-logic change.

**Evidence:** Spike 8 is the sole and direct evidence for this stage: repair_success_rate 0.667 (4/6) on a free local model, with both failures traced to one precise, fixable interface-specification issue rather than a reasoning gap.

### 7.2.5 Stage 5 — Replay Fix

The candidate fix is deterministically re-executed downstream (Verified Automatic Repair), and the pipeline reports a measured recovery outcome before the fix is ever surfaced as trustworthy.

**Evidence:** Spike 5 is the direct evidence this replay mechanism mechanically works — `recovery_success: true` on a deterministic toy pipeline — while Spike 8's own design deliberately chains Repair Agent's output straight into this same replay logic, meaning Spike 8's 0.667 repair_success_rate is itself already a measurement of Stage 4 and Stage 5 working together, not Stage 4 in isolation.

### 7.2.6 Stage 6 — Report

The full diagnosis record — root cause, confidence, propagation path, candidate fix, replay verdict — is stored and surfaced via the SDK and the dashboard.

**Evidence:** none, directly. This is worth naming plainly rather than leaving implicit: every other stage in this six-hop flow has at least one piece of direct spike evidence behind it; this one currently has none. It is, at this point in the project, the least-validated hop in the entire pipeline, resting entirely on the Platform Owner's still-largely-unbuilt backend and dashboard components.

## 7.3 The API-usage budget commitment

### 7.3.1 The target, and why it replaced a weaker earlier framing

The plan doc's §6 and architecture-sketch.md both commit to a specific, defensible split: roughly **15–20% API-dependent**, **80–85% own rule/graph-based logic**. This is stated as a deliberate correction of a weaker earlier framing that only claimed the LLM was "swappable" without committing to how much of the system's actual work depends on it — a system can pass a trivial "does it still run if you swap the model" test while still being majority API-dependent for anything that actually matters to the contribution claim. The current framing instead commits to a specific mechanism *per component*, so the budget is something the team can point to and defend under questioning, not merely assert.

### 7.3.2 What's rule-based — the 0% side of the ledger

**Fault-injection operators** are deterministic, rule-based corruption — matching AgenTracer's own perturbation-operator methodology directly. There is no reason to ask an LLM to "make something wrong" when a deterministic string substitution or field-replacement operation produces exactly the controlled, reproducible corruption a benchmark's ground truth needs. Spike 3's `inject_fault()` (`.replace("Paris", "Berlin")`) and Spike 3b's wholesale tool-output replacement are both concrete, minimal examples of this pattern.

**Execution-graph construction** is structural parsing of reference/dependency identifiers, matching GraphTracer's published approach. Spike 2's graph-building code is a direct, working example: a pure list comprehension over already-captured dependency metadata, with zero LLM calls anywhere in the function.

**Backward causal tracing** is pure graph traversal (BFS). Spike 6's `bounded_backward_trace()` is the direct implementation: a `while queue` loop walking `graph.predecessors()`, with a revisit-count dictionary and a hard safety cap — no LLM involved at any point in deciding which node to visit next.

**Confidence scoring** is computed from graph features (out-degree, betweenness centrality — matching GraphTracer's own formula), not obtained by asking an LLM how confident it feels. No spike directly exercises this specific sub-mechanism yet, but the commitment is stated plainly in the architecture sketch's budget table, and it follows the same "not LLM-asked" pattern as every other 0%-classified row.

**The Semantic Error Diagnostic** — explicitly flagged in architecture-sketch.md as "the load-bearing commitment; the headline novel claim must not just be an LLM wrapper" — is rule/schema-based checks against task-spec constraints. Spike 4's `rule_based_constraint_check()` is the concrete implementation: `diff = abs(stated_answer - correct_answer); matches = diff <= tolerance` — literally nothing more than an absolute-difference comparison against a tolerance, computed entirely in Python, with the correct answer itself independently recomputed from the task specification rather than asked of any model.

**SDK, backend, database, dashboard** are all own code throughout, with no API dependency by construction — though as noted in §7.2.6 above, the dashboard/backend/reporting stage is currently the least spike-validated part of the whole pipeline, meaning "0% API-dependent" is a design commitment for this component more than an empirically demonstrated one at this stage.

### 7.3.3 What's necessarily API-dependent — the 15–20% side

**Agent-under-test behavior** — the target multi-agent system being diagnosed — is necessarily an LLM, because it's the test fixture the whole system diagnoses, not the contribution itself. This is inherent and, per the architecture sketch's own logic, not counted against the 15–20% budget at all, since it is what's being diagnosed rather than what supplies the diagnosis.

**Repair Agent** is necessarily LLM-based, because generating a candidate correction is fundamentally a language/reasoning task — there is no deterministic rule that can look at "the wrong value was $90, here's a receipt saying $100" and produce "$100" without some form of language understanding. Spike 8 is the direct evidence of what this component's real behavior looks like on a free, weak backbone: it works 4 of 6 times, and both failures come from the model's own generative flexibility (choosing to compute one step further than asked) rather than from any failure to understand the evidence.

**Verified Automatic Repair's re-execution step** is necessarily an LLM call in the real system (re-running a corrected step through the actual agent pipeline), even though Spike 5's own toy-pipeline test of the *replay mechanism* deliberately used no LLM at all, specifically to isolate the mechanical replay-and-recompute logic from LLM-correctness variance. The real build's re-execution step will reintroduce that variance.

**ErrorProbe baseline reproduction** (Strategist/Investigator/Arbiter) is necessarily LLM-heavy, because faithfully reproducing someone else's published method as a *baseline for comparison* is inherently a language-reasoning-heavy task — this dependency is explicitly isolated to the baseline-comparison code path only, not counted as part of Granite's own contribution's API footprint.

### 7.3.4 The replacement test, and why it is now meaningful rather than trivial

The plan doc is careful to frame this split as **a target the build must be held to, not a fact already true** — and the "replacement test" stated in architecture-sketch.md is meant to make that target checkable: if the LLM API provider were swapped for a different model entirely, every component on the 0% side of the ledger should produce **byte-identical output**, not merely "still run" — because none of those components ever call the LLM in the first place.

This is a stronger and more falsifiable claim than the weaker "swappable" framing it replaced, and every 0%-classified component examined in the spikes above (fault injection, graph construction, backward tracing, the constraint checker) genuinely does meet this bar as implemented — none of the Python functions backing those four mechanisms contain a single `requests.post` call to the Ollama endpoint or any other LLM API.

## 7.4 The SDK/product architecture — what actually ships

### 7.4.1 The product boundary

Per architecture-sketch.md's own diagram, the product boundary is an **installable SDK** — the artifact a third-party team actually installs against their own multi-agent workflow. Underneath that boundary sit three deployed pieces: the Python SDK/instrumentation layer, a backend API with a trace/diagnosis-record store, and a minimal dashboard (results view, graph view, report). All three are meant to run inside a single containerized deployment (Docker) on a cloud VM or on-prem target — explicitly not a multi-tenant SaaS deployment; the plan doc's §14 places any hosted, multi-tenant, billing-enabled version firmly in "post-FYP productization," described as "context for later, not part of the graded deliverable."

### 7.4.2 How a developer would actually use it

A team operating a CrewAI or LangGraph multi-agent system installs the Granite SDK against their own workflow (functional requirement 5 explicitly commits to this working "without requiring modification to the core diagnosis algorithm"). They run their workflow as normal; the SDK's instrumentation layer captures a trace using the same post-hoc capture pattern proven in Spike 2 (no deep internal hooking required, at least for CrewAI).

If a failure occurs — either a hard error, or, more distinctively, a silent failure where the output looks fine but violates a task constraint — the trace is fed through the diagnosis pipeline: Stages 2–5 from §7.2 above, graph construction, diagnosis (constraint check plus backward tracing), fix generation, and replay-verified recovery testing.

The resulting diagnosis record — agent, step, confidence, propagation path, candidate fix, verified recovery outcome — is stored in the backend and surfaced through the dashboard, or returned directly via the SDK's own API, so a developer could either look at a visual report or programmatically consume the diagnosis in their own tooling (e.g., feeding it into extension #9's webhook, or extension #10's auto-generated incident report).

### 7.4.3 The MCP-convertibility discussion — why the shape fits

A fair question, given how the diagnosis pipeline is actually shaped internally, is whether it could be exposed as an MCP (Model Context Protocol) server rather than only as a Python SDK. The honest answer: structurally, yes, fairly naturally — but nothing has been built toward this, and it is explicitly not committed FYP scope.

The diagnosis pipeline's own internal structure is already function-shaped in a way that maps cleanly onto MCP's tool-call model: each stage — build the execution graph from a raw trace, run the Semantic Error Diagnostic against a completed trace, run backward causal tracing from a given failure node, generate a candidate repair given a diagnosed failure and evidence, replay a candidate fix downstream and report the recovery verdict — is already implemented (in the spikes, and presumably in the eventual real build) as a discrete, narrowly-scoped function with a well-defined input and output shape, not as one large monolithic "diagnose everything" call. That is essentially the same shape an MCP tool definition wants: a named, independently invocable capability with a clear input schema and a clear output schema.

Spike 8's `run_case()` function, for instance, already takes a structured input (`task`, `wrong_value`, `evidence`) and returns a structured output (`corrected_value`, `reasoning`) — that is close to what an MCP tool's `call_tool` handler would look like with only light wrapping.

### 7.4.4 What would actually need to be built — none of which exists yet

1. **An MCP server process wrapping each pipeline stage as a named tool** with a formal JSON-schema input/output definition, rather than the current internal Python function signatures.

2. **Session/state management**, since MCP tool calls are typically stateless per-call while the diagnosis pipeline currently threads state (the execution graph, the accumulating diagnosis record) through a sequence of calls — this would need either a session object passed between tool calls or a persisted diagnosis-record ID that each subsequent tool call references.

3. **Authentication and transport** (MCP servers typically run over stdio or HTTP/SSE), which nothing in the current architecture sketch addresses at all, since the sketch's data flow assumes a single deployed backend serving its own dashboard and SDK, not a third-party MCP client connecting in.

4. **A decision about which pipeline stages are exposed as callable tools** versus which stay internal orchestration logic not meant to be called out of sequence — for instance, exposing "replay a fix" as a standalone callable tool without also exposing "diagnose the failure first" risks a caller skipping straight to replaying an unverified, ungrounded candidate value.

### 7.4.5 The explicit scoping note

This MCP-convertibility discussion is **not committed FYP scope**. It does not appear anywhere in the plan doc's committed core (§7) or its 8-item extension list (§7.0), and no spike tests any part of it. It is included here only because the architectural shape genuinely does lend itself to this discussion, and because a defensible design conversation about "could this become an MCP server" is different from — and should not be conflated with — an actual commitment to build one. If this were ever pursued, it would be a post-FYP productization item in the same category as the hosted SaaS layer discussed in plan doc §14, not a Final-2 deliverable.

## 7.5 One trace, all six hops — a concrete end-to-end walkthrough

Section 7.2 above walks each of the six data-flow hops separately, naming the spike evidence behind each in isolation. No single spike exercises all six hops back to back in one run — that end-to-end integration is exactly what Stage 6 (§7.2.6) flags as still unbuilt. But it is possible, honestly, to stitch the *evidence from separate spikes* into one continuous, concrete story, because several of the spikes were deliberately built to chain into each other's inputs and outputs (Spike 8 into Spike 5's replay logic, for instance). What follows does that stitching explicitly, hop by hop, using the same Riverside Hardware scenario introduced in Spike 3b, so a reader can watch one trace move through the whole pipeline rather than reading six separate mechanism proofs in isolation.

**The scenario, restated.** A small multi-agent workflow answers a customer's question about a hardware store: is it open, and how far away is it. A `StoreChecker` agent calls a lookup tool for the store's closing time and distance; a `Writer` agent composes the final answer from that lookup result. The true closing time is 9:40 PM; in this walkthrough, imagine the tool call returns a corrupted 6:15 PM instead — exactly Spike 3b's own fault.

**Hop 1 — Execute.** The workflow runs. `StoreChecker` calls its lookup tool and receives (in this corrupted run) "Riverside Hardware closing time: 6:15 PM. Distance from downtown: 3.2 miles." `Writer` receives that output and composes a final answer built on top of it. Nothing about this hop looks unusual from the outside — the instrumentation layer is simply watching a workflow run and recording what each node did, exactly the role Spike 2's post-hoc capture pattern (§7.2.1) proved works without needing deep internal hooks into the target framework.

**Hop 2 — Capture Trace → Build Graph.** The raw trace — two nodes, `StoreChecker` and `Writer`, with `Writer` depending on `StoreChecker`'s output — is converted into an execution graph purely by structural parsing: `Writer`'s `depends_on` field already names `StoreChecker`, the same mechanical, zero-LLM-call graph-construction logic Spike 2's own list comprehension (§6.2.6) implements. No judgment call is required here about what depends on what — CrewAI's (or LangGraph's) own declared task-chaining already says so.

**Hop 3 — Diagnose.** Two things happen here, in parallel, exactly as §7.2.3 describes. First, the Semantic Error Diagnostic — Spike 4's rule-based constraint checker in spirit, though this particular fact (a store's closing time) isn't the kind of independently-recomputable numeric constraint Spike 4's math-word-problem checker was built for; a more apt parallel here is the structured propagation-verdict classification Spike 3b itself computes (§6.3.5's Fix 3): does the final output state the true value, the corrupted value, or some mixture. Second, backward causal tracing walks from the observed bad output (the Writer's answer, stating 6:15 PM) back through the dependency graph to `StoreChecker` — on a 2-node linear graph this is trivial, but the same bounded-BFS mechanism Spike 6 proves handles cycles (§6.6.5) is what would keep this walk safe on a more complex, looped version of the same workflow.

**Hop 4 — Generate Fix.** Root cause localized to `StoreChecker`'s tool-call output, Repair Agent is handed the wrong value (6:15 PM) and a piece of corroborating evidence — exactly the shape of Spike 8's six correction cases (§6.8.4). If the evidence available here were, say, a separate confirmation message quoting the true 9:40 PM closing time, Repair Agent's job is to read that evidence and return the corrected atomic value. Spike 8's own results (§6.8.7) suggest this succeeds roughly two times out of three on a free, weak, local backbone, and — per the diagnosed root cause in §6.8.10 — succeeds most reliably exactly when the correction target is a plain, unambiguous fact (a time, like `connecting_flight`'s arrival hour) rather than a value the task framing invites a further computation on.

**Hop 5 — Replay Fix.** The candidate corrected value (9:40 PM) is fed back into the downstream portion of the trace — here, just the `Writer` node — and `Writer` is re-run with the corrected input. Verified Automatic Repair's job, per Spike 5's own proven pattern (§6.12.1's worked trace above), is to report whether this re-run now produces a final answer that reflects the true value rather than the corrupted one, before that corrected answer is ever surfaced as trustworthy.

**Hop 6 — Report.** The full diagnosis record — culprit node (`StoreChecker`), the nature of the failure (a corrupted tool-call output, not a reasoning error), the candidate fix (9:40 PM), and the replay-verified recovery outcome — would be stored and surfaced through the dashboard or the SDK's own API. As §7.2.6 already states plainly, this is the one hop with no direct spike evidence behind it at all — nothing above changes that; the walkthrough here shows what the record *would* contain once Stages 2–5 are chained together for real, not that Stage 6 itself has been built or tested.

**What this walkthrough does and does not prove.** It does not prove the full pipeline works end to end — no spike runs all six hops back to back on one real trace, and this section says so directly rather than implying otherwise. What it does show is that the six hops are not six independent, disconnected claims: Hop 4's actual mechanism (Spike 8) was deliberately built to feed Hop 5's actual mechanism (Spike 5), and both were built against the same fault shape Hop 3's diagnosis logic already understands (Spike 3b's Riverside Hardware corruption). The evidence chains together conceptually even though it has not yet been chained together in one single running system.

### 7.5.1 What Stage 6 (Report) would need before it has its own spike

Since §7.2.6 flags Report as the least-validated hop, it's worth being specific about what a first spike for it would actually need to test, rather than leaving "unvalidated" as a dead end. Three narrow, testable claims sit underneath this hop, none of which has been checked yet: that a diagnosis record assembled from Stages 2–5's separate outputs (graph, diagnosis verdict, candidate fix, replay verdict) can be serialized into one coherent stored record without losing or misattributing any field; that the dashboard's graph view can render the same execution graph structure Spike 2 and Spike 6 already produce, without requiring a different internal representation; and that a diagnosis record retrieved via the SDK's own API matches, byte for byte, what was originally stored. None of these are hard engineering problems in isolation, but none has been demonstrated, and this is worth naming as a concrete, scoped follow-up spike candidate rather than leaving "Report is unvalidated" as a vague gap.

---

# Part 8 — Evaluation Plan

## 8.1 The full current metric set

The plan doc's §11 lays out an evaluation plan built from two layers: the original 5-metric set the team derived independently early in the project, and a second layer of corrections and additions pulled directly from the market survey's own Table 4 recommendations, integrated on 2026-08-24. Each metric below is presented with what it measures, why it was chosen (or corrected), and what a strong versus weak result would concretely look like given the spike evidence already in hand.

### 8.1.1 Top-1 agent accuracy

**What it measures:** whether the diagnosis pipeline's single top-ranked prediction for "which agent caused this failure" matches the ground-truth culprit agent exactly.

**Why chosen:** this is the most basic, most interpretable attribution metric, and it's the metric ErrorProbe itself reports alongside step accuracy, making it the natural axis for a direct comparison.

**Strong result:** something like Spike 1's own 0.75 (6/8) on a simplified 2-stage pipeline using a free, weak, local 3B model — genuinely encouraging given how far short of the full pipeline this simplified version falls.

**Weak result:** performance closer to random-among-plausible-agents (in an N-agent trace, roughly 1/N by chance, though real traces have a small number of distinct agent roles so this baseline is not as low as it sounds). ErrorProbe's own published agent-identification performance — not directly quoted in the sources reviewed here, but understood to sit meaningfully above chance — is the real comparison bar once the full 3-stage pipeline is built.

### 8.1.2 Top-1 step accuracy

**What it measures:** whether the predicted step index exactly matches the ground-truth originating step.

**Why chosen:** this is ErrorProbe's own headline metric (59.5% on Who&When-Algo), making it the single most direct point of comparison for the entire baseline-delta claim in §4 of the plan doc.

**Strong result:** approaching or exceeding 59.5% on a fair, full-pipeline, comparable-backbone run.

**Weak result:** what's currently on record — `0.0` in Spike 1's JSON — though as documented at length in §6.1 above, this specific number is currently unreliable due to a type-mismatch scoring bug and needs re-deriving before it can be honestly called either strong or weak.

### 8.1.3 Propagation-path F1

**What it measures:** precision and recall of the predicted causal propagation path — the full chain of nodes through which a fault's effect traveled — against the ground-truth path, not just the single origin point.

**Why chosen:** attribution alone tells you *who* was responsible; propagation-path scoring tells you whether the diagnosis pipeline correctly understands *how* the failure spread through the interdependent agent graph — directly testing the CCP characteristic of interdependence (§2 of the plan doc names this explicitly: "the entire problem is that failures propagate through interdependent agent sub-problems — this is what the execution graph exists to model").

**Current evidence:** none of the eight spikes measures this metric directly. Spike 3/3b's verification blocks (`propagation_verdict`) are a conceptual precursor — they classify propagation behavior for a single injected fault — but do not yet compute a precision/recall score against a full predicted path.

**Strong result:** the backward-tracing mechanism (validated structurally in Spike 6) correctly reconstructing multi-hop propagation chains, not just single-hop origin points.

### 8.1.4 Silent-failure precision and recall (correction: precision was originally missing)

**What it measures:** of all cases the Semantic Error Diagnostic module flags as silent failures, what fraction are real (precision), and of all real silent failures in the data, what fraction get flagged (recall).

**Why the precision correction matters:** the plan doc's own §11 states this plainly — "recall alone can't distinguish a real detector from one that flags everything." A detector that flags every single trace as a silent failure would trivially achieve 100% recall while being useless; only precision, measured alongside recall, reveals that.

**Current evidence:** Spike 4's direct mechanism test (not the n=3 spike run itself, which measured 0 natural silent failures and so could not compute recall) is the relevant partial evidence — the checker correctly flagged every known-wrong value fed to it, including a plausible near-miss, with zero false positives on correct values. That bears on both precision (zero false positives observed) and recall (all wrong values caught), but only at a very small, hand-selected scale.

**Strong result:** high precision and high recall simultaneously, at real scale.

**Weak result:** a detector that trades one for the other — flags everything for high recall, or flags almost nothing for high precision — would be a weak, if superficially passable-looking, result on either metric alone.

### 8.1.5 Diagnostic latency overhead

**What it measures:** wall-clock time added by running the full diagnosis pipeline after a trace completes, reported as a percentage of the original workflow's own execution time.

**Why chosen:** this is the plan doc's one stated measurable non-functional requirement (§0.07), with an explicit target of under 50% for the single-pass diagnosis mode (extension #6, the cheap-vs-full-pipeline trade-off). A diagnosis system nobody can afford to run because it doubles or triples workflow latency is not a usable pre-deployment testing tool, undermining the project's own stated client need (§0.06: "pre-deployment fault testing against their own workflow before shipping it").

**Current evidence:** none, reliably. Spike 2's own timestamps were captured post-hoc around the whole run rather than via real per-step hooks (explicitly flagged as a known limitation in §6.2.10 above), meaning real latency-overhead measurement is still fully owed, not partially measured.

### 8.1.6 Recovery success rate

**What it measures:** of runs that originally *failed*, what fraction are converted into successful runs by the counterfactual intervention (candidate repair, replayed downstream). Explicitly scoped to previously-failed runs specifically, distinguishing it from task completion rate below.

**Current evidence:** Spike 5's `recovery_success: true` on its single toy-pipeline case (a corrupted trace failing at 97.2 against an expected 108.0, recovering fully to 108.0 after correction and replay) is a clean positive mechanism proof, though at n=1 on a fully deterministic, no-LLM pipeline it says nothing yet about real recovery rate on the actual benchmark. Spike 8's chained repair-generation-plus-replay result (0.667, 4/6) is closer to what a real recovery-rate measurement will look like once Repair Agent's generation step is included, since it already combines both the fix-generation and the replay-verification halves of the mechanism on a non-toy (if still synthetic) case set.

### 8.1.7 Task completion rate (added 2026-08-24 from the market survey, missing from the first pass)

**What it measures:** overall task success across *all* runs — not just previously-failed ones — comparing a baseline (non-self-healing) MAS against the full self-healing Granite-instrumented MAS.

**Why it's distinct from recovery rate, and why that distinction matters:** recovery rate only looks at the subset of runs that already failed and asks whether intervention fixed them; task completion rate looks at the *whole* population of runs and asks whether the system as a whole, self-healing included, completes tasks more often than the baseline would have. A system could show a strong recovery rate on the failures it catches while still showing a weak overall task completion rate if it catches only a small fraction of the failures that actually occur, or if its interventions occasionally break previously-passing runs (a risk directly connected to false repair rate below).

**Current evidence:** none. This requires running the same task set through both a baseline MAS and a Granite-instrumented MAS and comparing aggregate completion, which needs the full pipeline integrated end to end, not yet built.

### 8.1.8 Repair success rate

**What it measures:** the percentage of Repair Agent's generated corrections that actually fix the task, measured with versus without Verification Agent gating.

**Why chosen:** directly matches the market survey's own Table 4 definition, and is the metric Spike 8 was purpose-built to produce a first real number for.

**Current evidence:** 0.667 (4/6), with both failures precisely diagnosed (§6.8 above) as an interface-specification issue, not a reasoning failure — a genuinely strong result for a free local model with an identified, fixable cause behind its shortfall.

**What's still missing:** the "with vs. without verification gating" comparison arm — Spike 8's cases were not run through any Verification Agent gate before repair generation, so the ablation this metric is explicitly supposed to support (verified vs. unverified repair) has not yet been measured.

### 8.1.9 False repair rate

**What it measures:** the fraction of incorrect repairs the system accepts as verified, measured via a verification-gate ablation.

**Why chosen:** this is explicitly the metric that "keeps 'verified' in Verified Automatic Repair honest, not just asserted" (plan doc §11's own phrasing) — without measuring false repair rate, the "verified" label in the feature's own name would be an unvalidated claim rather than a tested property.

**Current evidence:** none. This requires a verification-gate ablation (running the same repair candidates both with and without the verification step active) that has not yet been built or tested in any form.

## 8.2 The 2 metrics deliberately not added

### 8.2.1 What they are

The market survey's own Table 4 lists two further metrics the team explicitly chose not to add to the current evaluation plan:

1. **Re-execution cost** — tokens/tool calls/time spent after a failure, comparing a full restart-from-zero against a checkpoint-based resume.
2. **Repair reuse benefit** — the measured improvement in some outcome when Verified Repair Memory is enabled versus disabled.

### 8.2.2 The exact reasoning

Stated plainly in the plan doc's own §11: both of these metrics measure territory that belongs to Checkpointing (now formally named Recovery Controller, foundational item #9) and Verified Repair Memory (foundational item #10) respectively — and adding either metric before the feature it measures actually exists and works would be premature, not merely an oversight waiting to be filled in later.

### 8.2.3 Why this is a disciplined decision, not a gap

This is worth connecting directly to the honest status of those two features as recorded in the risk register. **Recovery Controller (R21) has zero POC evidence of any kind** — it is described plainly as "genuinely new mechanical work, not a rename of anything already tested," with the only supporting evidence being a precedent check showing 5 of the 7 surveyed orchestration frameworks have *generic* checkpoint/resume infrastructure, none of which is tied specifically to a verified-repair resumption point (which is exactly the mechanism Recovery Controller needs to add).

**Verified Repair Memory (R18/R22) has exactly one real test, and that test failed** — 0 of 8 real cases ever committed anything to memory, and agent accuracy regressed when the memory-augmented pipeline was tried.

Measuring re-execution cost against a checkpoint-resume mechanism that has never been built, or measuring repair reuse benefit against a memory mechanism whose one real test produced a regression, would produce numbers with no grounded feature behind them to actually interpret — the metric would exist before the thing it's supposed to measure does. This is a genuinely disciplined scope decision, not a gap the team failed to notice: it is explicitly named, explicitly reasoned through, and explicitly deferred rather than silently dropped.

## 8.3 The Testing / Evaluation / Acceptance three-way split

Per Section 13.1 of the FAST guide, the plan doc tracks these three categories of validation separately rather than collapsing them into one undifferentiated "testing" bucket, because each answers a genuinely different question about the system.

### 8.3.1 Testing

Covers unit and integration tests on the SDK, the graph builder, and the injection harness, plus edge cases — an empty trace, a single-agent trace, malformed tool output. This is the layer that asks "does the code do what its own logic says it should do," independent of any question about diagnostic accuracy.

None of the eight spikes are unit tests in this sense — they are all end-to-end mechanism demonstrations on real (if small and synthetic) data, which is a different and complementary kind of evidence. The formal unit/integration test suite for the SDK, graph builder, and injection harness remains to be built as part of the core FYP-1 implementation work; the spikes prove the underlying mechanisms are sound, but they do not substitute for a maintained regression-test suite — itself named as extension #8: a GitHub Action running the evaluation suite on every push, failing the build if step accuracy drops below a stated threshold, itself gated behind the core existing first.

### 8.3.2 Evaluation

The metrics table in §8.1 above, measured against the ErrorProbe baseline specifically. This is the layer that asks "how good is the diagnosis, quantitatively, compared to the strongest existing published method."

The eight spikes are the current, if early and partial, evidence base for this layer. Six of the nine metrics in §8.1 have at least some spike-level evidence behind them: agent accuracy, step accuracy (pending the scorer fix), silent-failure precision/recall (pending scale), recovery success rate, and repair success rate. Four metrics currently have zero direct spike evidence as of this write-up: propagation-path F1, diagnostic latency overhead, task completion rate, and false repair rate.

### 8.3.3 Acceptance

A small user-acceptance round with real or proxy users — the guide's own suggestion is peers or faculty who build multi-agent systems themselves — integrating the SDK against their own workflow, recorded per the guide's own acceptance-testing table format: method, participants, tasks/results, issues found, outcome.

This is the layer that asks "does a real person, who did not build this system, find it usable against a workflow they actually own." This layer has not started at all — it depends on the SDK actually existing in an installable form, which in turn depends on the Platform Owner's largely-unbuilt backend/dashboard/SDK work (§7.2.6's Stage 6, identified above as the single least spike-validated hop in the entire pipeline). It is also entangled with the still-open CCP characteristic #6 gap (diverse stakeholders, rated "weak" in the plan doc's own §2) and issue I2 in the risk register ("real stakeholders not yet contacted"), both of which name the same underlying unmet need from two different angles — one as a CCP-rating gap, one as a blocking pre-defense issue.

### 8.3.4 Why the three layers must stay distinct

These three layers are meant to stay genuinely distinct through the rest of the project's timeline, not merge into a single vague "we tested it" claim at the end. A system that scores well on Evaluation but has never been through Acceptance testing has evidence it works well in a controlled measurement sense but no evidence a real outside user could actually pick it up and use it. A system that passes Acceptance testing with enthusiastic peer feedback but has weak Evaluation numbers has evidence of usability without evidence of the specific quantitative claim — beating ErrorProbe's territory — the whole CCP statement rests on. Both layers, plus the underlying Testing layer that makes either trustworthy in the first place, are required, and none substitutes for either of the other two.

## 8.4 Worked numeric examples for all nine metrics

Every metric in §8.1 above is defined in prose. What follows puts a small, concrete number through each definition — not a real measured result (most of these have no real-scale measurement yet, as already stated honestly metric by metric above), but a worked arithmetic example of exactly what the number would mean if it existed, so a reader unfamiliar with evaluation-metric conventions can see precisely what's being counted and divided in each case.

**Top-1 agent accuracy.** If a diagnosis pipeline is run against 10 benchmark traces, and its single top-ranked "which agent caused this" prediction matches the ground-truth culprit agent in 8 of them, agent accuracy is 8/10 = 0.80, or 80%. This is exactly the same arithmetic Spike 1 already performed at a smaller scale: 6 of 8 real cases correct gives 6/8 = 0.75 (§6.1.6).

**Top-1 step accuracy.** Of those same 10 traces, if the predicted step index exactly matches the ground-truth originating step in only 3 of them, step accuracy is 3/10 = 0.30. Note that a trace can get the agent right while getting the step wrong (as 5 of Spike 1's 8 cases did — see the table in §6.1.6) — agent accuracy and step accuracy are two separate counts over the same set of traces, not one number derived from the other.

**Propagation-path F1.** Suppose the ground-truth propagation path for one failing trace is the 4-node sequence `StoreChecker → Writer → Summarizer → FinalReport`, and the diagnosis pipeline predicts a path of `StoreChecker → Writer → FinalReport` (3 nodes, correctly including 3 of the 4 true nodes, but missing `Summarizer`, and correctly including no extra wrong nodes). Precision — of the nodes predicted, how many were actually in the true path — is 3/3 = 1.0. Recall — of the true path's nodes, how many were predicted — is 3/4 = 0.75. F1, the harmonic mean of the two, works out to 2×(1.0×0.75)/(1.0+0.75) ≈ 0.857. As §8.1.3 states directly, no spike has computed this metric on a real predicted path yet — this is a worked illustration of the arithmetic, not a reported result.

**Silent-failure precision and recall.** Say a checker is run against 20 traces, 5 of which contain a real silent failure and 15 of which are genuinely correct. If the checker flags 6 traces total, and 4 of those 6 flagged traces are among the 5 real silent failures (with 2 flags being false alarms on genuinely correct traces), precision is 4/6 ≈ 0.667 (of everything flagged, how much was real) and recall is 4/5 = 0.80 (of everything real, how much got caught). This is exactly why §8.1.4 insists on reporting both together — a checker that simply flagged all 20 traces would score a perfect 5/5 = 1.0 recall while precision collapsed to 5/20 = 0.25, which is the scenario the added precision metric exists specifically to catch.

**Diagnostic latency overhead.** If a target workflow normally completes in 40 seconds, and running the full diagnosis pipeline afterward adds 15 more seconds, overhead is 15/40 = 0.375, or 37.5% — comfortably under the stated under-50% target for the single-pass mode (§8.1.5). If the same diagnosis instead took 30 seconds, overhead would be 30/40 = 0.75, or 75%, failing that target. Spike 1's own elapsed-time figures (§6.1.12: 49.9 to 121.3 seconds per case) hint that trajectory length will likely be the dominant driver of this number once it can be measured properly, but as stated in §8.1.5, no reliable measurement of this metric exists yet — Spike 2's timestamps were captured post-hoc, not via real per-step hooks.

**Recovery success rate.** Of 10 traces that originally failed, if a candidate repair is generated and replayed for each, and 7 of the 10 now pass after the corrected re-execution, recovery success rate is 7/10 = 0.70. This is scoped specifically to previously-failed runs — a trace that never failed in the first place is not part of this denominator at all. Spike 5's own single toy case is a recovery-success rate of 1/1 = 1.0, and Spike 8's chained repair-plus-replay result is 4/6 ≈ 0.667 on its six correction cases (§6.8.7) — both real numbers, but at far too small a scale to represent what the metric will read on the real benchmark.

**Task completion rate.** This is deliberately a different denominator from recovery success rate — it runs over *all* runs, not just the previously-failed subset. If a baseline (non-self-healing) system completes 60 of 100 tasks successfully, and the same 100 tasks run through a Granite-instrumented, self-healing version instead complete 78 of 100 successfully, task completion rate improved from 60% to 78% — an 18-percentage-point lift attributable to catching and repairing failures that would otherwise have gone uncorrected. As §8.1.7 states, this requires running the same task set through both a baseline and a self-healing configuration and comparing the aggregate — nothing currently in the spike evidence measures this, since it needs the full pipeline integrated end to end.

**Repair success rate.** Distinct from recovery success rate in what it isolates: of every candidate correction Repair Agent generates, what fraction actually fix the task, and how does that fraction change with versus without Verification Agent's gating. If Repair Agent alone (no gating) fixes 12 of 20 candidate corrections, its ungated repair success rate is 12/20 = 0.60; if adding Verification Agent's gate means only corrections that pass a confirmation check are ever surfaced, and 9 of those gated corrections turn out correct out of 10 that passed the gate, the gated repair success rate is 9/10 = 0.90 — a smaller absolute number of repairs surfaced, but a higher fraction of them trustworthy. Spike 8's own 4/6 = 0.667 (§6.8.7) is the current real number for the ungated case; the gated comparison arm, as §8.1.8 states, has not been measured at all yet, since Spike 8's cases were never run through any verification gate.

**False repair rate.** If, out of 20 repairs the system accepted as "verified" and surfaced to a user, 2 turn out on closer inspection to actually be wrong, false repair rate is 2/20 = 0.10, or 10%. A low number here is what keeps the word "verified" in Verified Automatic Repair meaningful rather than aspirational — a system that accepted, say, half of its wrong repairs as verified would have a false repair rate of 0.50, at which point "verified" would be actively misleading rather than merely imprecise. As §8.1.9 states, this metric requires a verification-gate ablation that has not been built or tested in any form yet.

### 8.4.1 Why these worked examples use invented numbers, stated plainly

Every number in §8.4 above is a constructed illustration — 8 of 10, 7 of 10, 12 of 20 — chosen to make the arithmetic clear, not a real measured result. The only real numbers repeated from elsewhere in this section are Spike 1's 6/8, Spike 5's 1/1, and Spike 8's 4/6, each explicitly labeled as such and each already reported at full precision in their own spike write-ups above. Mixing invented illustration numbers with real spike numbers without a clear label would be exactly the kind of blurring this document's own discipline (stated at the top of Part 6) exists to prevent — so every invented number above is marked as invented, and every real one is cross-referenced back to the section it actually came from.

---

*End of Part 6–8. Total content spans all 8 POC spikes individually (§6.1–6.8), a cross-spike summary and consolidated open-items list (§6.9–6.10), the 3-owner architecture breakdown, the 6-stage data-flow pipeline, the API-usage budget commitment, and the SDK/MCP product-architecture discussion (Part 7), and the full current evaluation metric set, the 2 deliberately-excluded metrics, and the Testing/Evaluation/Acceptance split (Part 8). Every number quoted above is reproduced directly from the JSON output files or Python source at `dev/spikes/poc/`, or from the named planning/risk documents — none invented for this write-up.*
## Parts 9–11: Risk Register, Timeline & Governance, Open Items and Honest Gaps

*A note on names before we start: this project began under the working name "TraceCause" and was formally renamed to "Granite" during its seventh AI-assisted session (2026-08-24), with the official FYP registration title becoming "A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery." Historical records — the AI usage log's early sessions, in particular — deliberately keep the old name "TraceCause" as originally written, because that's what was actually true at the time the entry was made. This document uses "Granite" throughout except when directly quoting or describing a historical record, where the original name is preserved. This distinction matters and comes up again in Part 10's discussion of the log's non-rewriting policy.*

---

# PART 9 — THE RISK REGISTER, EVERY ENTRY

## 9.0 Why a RAID register at all, and why it looks like this

The FAST guide requires, on page 7, that an "Initial RAID register" — Risks, Assumptions, Issues, and Dependencies — be opened as part of proposal-stage work, and treated as a living document rather than something reconstructed retroactively once the project is mostly finished. Granite's register (`risk-register.md`) was opened on 2026-08-22, ahead of the proposal defense, and it carries a path note at the very top: dataset files and POC (proof-of-concept) spike scripts were moved from `agent-autopsy/datasets/` and `agent-autopsy/spikes/` into a sibling `dev/` folder, so any bare `datasets/...` path referenced inside an entry (for example, inside R11b) should be read as relative to that `dev/` folder, not the `agent-autopsy/` root. This is a small housekeeping note, but it matters for anyone trying to actually locate the artifacts a risk entry cites — the register is meant to be checkable, not just readable.

The register is organized into four sections that map onto the RAID acronym: Risks (R-numbered), Assumptions (A-numbered), Issues (I-numbered, meaning currently open blocking items), and Dependencies (D-numbered). On top of that base structure, the register accumulated several dated addenda — blocks of new risk rows added on later working sessions as new spikes were run or new findings surfaced (2026-08-23's three new spikes; 2026-08-24's three separate passes reviewing the market survey). Reading the register chronologically, rather than just by ID number, is genuinely useful, because the IDs were not always assigned in a clean increasing sequence — R13 appears before R9 in the file's own layout, for instance, because R9 was inserted later into an earlier table while R13 belongs to a session that came after. This document processes them in the order that makes the story clearest: first the original core risk table (R1–R9, in the register's own printed order), then the R7 literature-triage sub-tables in full, then the Assumptions, Issues, and Dependencies tables, then the three dated addenda in chronological order (R13/R14/R16/R15, then R17–R19, then R20, then R21/R22), and finally the appendix tables that back R17–R20.

One thing worth internalizing before going entry by entry: this register is not a formality performed once and left untouched. It has visibly been edited, corrected, and reopened multiple times in the same multi-day window — risks get resolved, then have a status note appended when new information arrives; risks get closed, then explicitly reopened with a footnote explaining why the earlier closure was premature; an entire risk (the original R12, about a Microsoft project called AgentRx) was deleted outright rather than kept as a stale row. That level of churn is a feature, not a sign of disorganization — it's exactly what a "living document" looks like when a team is actually using it to track real uncertainty as the uncertainty resolves, escalates, or gets superseded.

### 9.0.1 What "RAID" actually buys a project like this

It's worth pausing on why a formal RAID register is worth the overhead for a project of this size, rather than just an informal running list of concerns. The four categories force a discipline that an unstructured list doesn't: a **Risk** is something that has not happened yet and might not happen, carries a likelihood and an impact, and needs a mitigation *planned in advance* — R1 (ErrorProbe reproduction) is the clearest example, because the mitigation (run a POC before committing to the full claim) had to happen before the risk could even be assessed honestly. An **Assumption** is something the team is *choosing* to take on faith in order to keep moving, with an explicit statement of what breaks if the faith turns out to be misplaced — A5's correction (9.12 below) shows exactly why writing assumptions down matters: an assumption that quietly presupposes a decision already made can hide a real gap (team roles) behind confident-sounding language. An **Issue** is something that has *already* happened and is *actively* blocking a specific downstream requirement right now — I2 (stakeholder contact) is not a hypothetical, it is a known-missing precondition for CCP characteristic #6 to read as "clear" rather than "weak." A **Dependency** is something entirely outside the team's own control that a plan step needs to succeed — D1's TracerTraj-licensing finding is a case where an assumed dependency (a dataset being available) turned out false, and the register is what caught it before it became an unrecoverable late-stage surprise.

Keeping these four categories separate, rather than lumping everything into one undifferentiated "concerns" list, is what makes each entry actionable. A risk needs a mitigation and a likelihood/impact judgment; an issue needs an owner and a target date; a dependency needs a status check against something outside the team. Conflating them tends to produce vague, un-actionable journal entries instead of a document a team can actually work from.

### 9.0.2 A one-line map of every entry, before the full walkthrough

The table below is a navigation aid, not a substitute for the full entries that follow — every row is expanded in full later in this Part, with the reasoning, evidence, and context behind the one-line summary given here.

| ID | Category | One-line summary | Status at last update |
|---|---|---|---|
| R1 | Risk | Can ErrorProbe's 59.5% step accuracy be reproduced at all? | Open, downgraded from top priority — real partial evidence in hand |
| R2 | Risk | Does CrewAI/LangGraph map cleanly onto the execution-graph model? | Resolved — structural mapping proven, timing precision still owed |
| R3 | Risk | Is injected-fault ground truth reliably unambiguous? | Resolved — both self-correction and blind propagation documented |
| R4 | Risk | Cross-paper backbone confound in comparisons | Accepted, documented — inherent to literature comparison |
| R5 | Risk | LLM API cost for large-scale benchmark generation | Open — real numbers not yet available |
| R6 | Risk | Team roles defined but nobody actually assigned | Open — must resolve before Mid-1 |
| R7 | Risk | A new paper could close one of the two targeted gaps | Escalated — literature more crowded than believed, risk accepted knowingly |
| R8 | Risk | 13+ extensions could pull focus from core depth | Mitigated by scope design (gating) |
| R9 | Risk | Commercial observability market already exists | Closed — positioning corrected and narrowed, spot-check owed |
| R10 | Risk | Silent-failure detection mechanism had zero test coverage | Open — mechanism validated directly, real-world frequency unconfirmed |
| R11 | Risk | TracerTraj-2.5K turns out not to be actually released | Open — plan doc citations still need correcting |
| R11b | Risk | Self-generating a TracerTraj-style dataset locally | Closed — infeasible, confirmed by real pilot timing, stopped deliberately |
| R13 | Risk | Verified Automatic Repair had zero POC evidence | Resolved — mechanism validated on a toy pipeline |
| R14 | Risk | Cyclic/dynamic graph support untested on a real cycle | Resolved — mechanism works, control case proves it's load-bearing |
| R15 | Risk | Preventive clarification classifier's real signal strength | Open — genuine near-random negative result, real finding |
| R16 | Risk | Security/privacy threat model for trace data | Resolved — threat model written, not yet team-reviewed |
| R17 | Risk | Repair Agent had no candidate-fix-generation mechanism at all | Partially closed — 4/6 success, precise fixable cause for the 2 failures |
| R18 | Risk | Verified Repair Memory's one real test, and its failure | Superseded by R22 — evidence preserved unmodified |
| R19 | Risk | Market survey's advice to narrow to one framework | Closed — explicitly rejected, resolved positively via extension #8 |
| R20 | Risk | Framework Compatibility Layer — draw from all 7 frameworks | Open — scope decision only, no POC yet, gated behind core |
| R21 | Risk | Recovery Controller — checkpoint-based resume, zero POC | Open — genuinely new mechanical work, clear gap before Mid-1 |
| R22 | Risk | Verified Repair Memory reclassified into foundational core | Open — conditional on a stronger-backbone re-test before Mid-1 |
| A1–A5 | Assumptions | Reproducibility, framework exclusivity, licensing, budget, role stability | A5 corrected in place; others open/monitored per gate |
| I1–I3 | Issues | POC execution, stakeholder contact, AI usage log start | I1/I3 closed; I2 open, targeted before defense |
| D1–D4 | Dependencies | Licensing, supervisor approval, LLM API budget, framework stability | D1 partially resolved/corrected; D2 pending defense; D3 partially superseded; D4 open |

With that map in hand, the rest of Part 9 works through every one of these in the depth the source register itself supports.

### 9.0.3 Regrouping the same 22 entries two more ways — by pipeline stage, and by resolved-vs-open

The one-line map above orders entries by ID, which is how the register itself prints them, but ID order mixes together risks that belong to genuinely different parts of the system. Two alternative groupings make different things visible: grouping by which pipeline stage or project concern a risk actually belongs to shows where the evidentiary coverage is thin versus thick; grouping by resolved-vs-open shows, in one place, exactly how much of the register's total 22 entries the team can point to as closed with real evidence versus how much is honestly still outstanding.

**By pipeline stage / project concern:**

| Pipeline stage or concern | Risks in this group | What this grouping shows |
|---|---|---|
| Baseline reproduction (ErrorProbe itself) | R1, R4 | The two risks most directly about whether the delta claim is measurable at all — R1 asks if the number is reachable, R4 names the confound in any cross-paper comparison used to contextualize it |
| Data model / framework instrumentation | R2, D4 | Whether the graph abstraction and the frameworks it wraps actually cooperate — both resolved or managed, but R2 carries a live timing-precision caveat |
| Benchmark construction / ground truth | R3, R11, R11b, A3, D1 | The largest single cluster — five entries, all about whether the data Granite evaluates against is real, licensed, and produces unambiguous labels |
| Silent-failure detection (RQ3) | R10 | One entry, but it's the register's own record of the project's second headline novelty pillar going from zero test coverage to a first, honestly-limited positive result |
| Repair and recovery (the self-healing half) | R13, R17, R18, R21, R22 | The second-largest cluster — five entries spanning Verified Automatic Repair, Repair Agent, and the two same-day-reclassified items; this is also the cluster carrying both of the project's two currently-open foundational gaps |
| Extensions (cyclic graphs, classifier, framework breadth) | R8, R14, R15, R19, R20 | Everything gated behind the core being complete first — R14 resolved, R15 an honest negative result, R19/R20 a rejected-then-positively-resolved scope question |
| Literature / novelty risk | R7 (plus its full sub-table) | The single most heavily worked entry in the register, covering an entire multi-session triage process on its own |
| Market/product positioning | R9 | The one entry resolved by correcting an earlier, stale claim rather than by running a spike |
| Team and process | R6, A5, I1, I2, I3 | The cluster with the least technical content and the most direct bearing on whether the guide's own scope-sufficiency and stakeholder-involvement tests can honestly be marked passed |
| Security/privacy | R16 | One entry, but flagged elsewhere in this document as "the most substantive finding" in the deeper compliance audit pass |
| Cost/resourcing | R5, A4, D3 | The three entries governing whether the project can afford to scale from POC-sized runs to the target 500–1,000-trace benchmark |

**By resolved-vs-open, counted honestly:**

| Status bucket | Risks in this group | Count |
|---|---|---|
| Resolved, with real evidence, no open follow-up | R2 (structural claim only — timing caveat noted separately), R3, R9, R14 | 4 |
| Resolved/accepted by design or explicit decision, not by a spike | R4, R8, R9 (positioning), R19 | overlaps with above; counted once each |
| Closed by explicit, deliberate stop, not left dangling | R11b | 1 |
| Mitigated structurally rather than tested | R8 | 1 |
| Open, with real partial or mechanism-level evidence in hand | R1, R10, R15, R17 | 4 |
| Open, evidence-negative (the mechanism was tested and failed) | R18 (superseded by R22, evidence unchanged), R22 | 2 |
| Open, zero evidence either way | R5, R6, R21 | 3 |
| Open, procedural/documentation fix still owed | R11 | 1 |
| Escalated and knowingly accepted as residual risk | R7 | 1 |
| Superseded by a later entry, evidence preserved | R18 | 1 (also counted above) |

The honest takeaway from this second table is that of the register's 22 numbered risk entries, a genuine majority are closed, mitigated, or accepted by explicit, recorded decision — but the ones still open are not trivial housekeeping items. R1, R6, R21, and R22 in particular are each independently named elsewhere in this document as among the highest-stakes unresolved items in the whole project, and all four remain in the "open" half of this table as of the register's last update. A register where every entry eventually resolved cleanly would be slightly suspicious on its own terms; one where roughly a third of entries stay open, and where the open ones include some of the most consequential items rather than only minor ones, is closer to what an honest running account of a real project's uncertainty should look like.

---

## 9.1 R1 — ErrorProbe reproduction: the highest-stakes risk in the whole project

**What it is.** ErrorProbe is the strongest published method Granite is trying to beat — a peer-reviewed (ACL 2026 Findings) three-stage LLM diagnosis pipeline (Strategist → Investigator → Arbiter, plus a Verified Episodic Memory component) that reports 59.5% step-level attribution accuracy on the Who&When-Algo benchmark. R1 asks the single most load-bearing question in the entire project: can Granite's team actually reproduce anything close to that number? If they can't, the whole comparison collapses, because everything else in the project — the delta claim, the contribution statement, the evaluation plan — is built on the premise that Granite's own attribution pipeline is measured *against* ErrorProbe's real, replicated performance, not against a number copied uncritically from its paper.

**Why it was logged as the top risk.** This is Stream A work (research-derived, per the FAST guide's two entry points), and the guide itself names "can it be reproduced within our resources" as the primary risk for exactly this kind of project (see the Guide Compliance Audit's note under §1.1). A Stream A project that cannot reproduce its own chosen baseline within the team's available compute and time has no foundation to build a delta claim on top of. This is why R1 sat as the team's top proposal-stage priority, and why POC spike 1 specifically targeted it before anything else.

**What evidence exists.** POC spike 1 (`poc_spike1_errorprobe_repro.py`) ran a deliberately simplified two-stage version of ErrorProbe's pipeline — a Strategist stage and an Arbiter stage only, explicitly cutting the tool-grounded Investigator stage and the Verified Episodic Memory component that the real ErrorProbe pipeline includes. It ran against a local 3B-parameter model (`llama3.2:3b` via Ollama, free, zero API cost) on 8 real, downloaded Who&When-Hand-Crafted cases. The result: 75% agent-level accuracy (correctly identifying which agent was responsible) and 12.5% step-level accuracy (correctly identifying which specific step was responsible), with zero parse failures. That step accuracy number — 12.5% against ErrorProbe's own reported 59.5% — looks damning at first glance, but the register is careful to frame it honestly: this is "real signal the approach works, not proof the full pipeline hits 59.5%." The 75% agent accuracy is a genuinely strong signal that the underlying mechanism has real traction; the low step accuracy is exactly what you'd expect from a version of the pipeline that has had two of its three real components removed (no tool-grounded verification, no memory of prior verified diagnoses to draw on) and is running on a small, free local model rather than whatever backbone ErrorProbe's own authors used.

**Why the status is what it is.** The register marks this "Open — downgraded from top priority." That phrasing is precise, not casual: the risk isn't closed (a simplified pipeline on a weak local model getting 12.5% step accuracy proves nothing definitive about whether the *full* pipeline can approach 59.5%), but it's downgraded because real, positive evidence is now in hand that the *mechanism itself* is not broken — the approach produces sensible agent-level judgments most of the time, which is a meaningfully different state than "we have no idea if this works at all." The register explicitly states what's still owed: "the full 3-stage+memory version on a stronger backbone before this is closed." This is directly reflected in the timeline (Part 10 covers this in more depth): the plan doc's own Weeks 6–10 block names this as the literal top priority for that phase, quoting spike 1's own result as the justification.

**Connective tissue worth noting.** R1 is tied to Assumption A1 ("ErrorProbe's methodology is reproducible from the published paper alone, without needing its unlicensed code") — if A1 turns out false, the register says explicitly that "reproduction becomes a research risk in itself — escalate to R1." That's the assumption this risk exists to test. It's also tied to Dependency D3 (LLM API access for the full build): spike 1 didn't need paid API access because it ran free on a local model, so D3 wasn't a blocker for the *proposal-stage* POC, but a real budget/backbone decision is still pending for the full FYP-1 core build, because a stronger backbone is what's needed to give ErrorProbe a fair comparison.

**What a panelist would probe here, and why the honest answer still holds up.** The obvious question is: "12.5% is nowhere near 59.5% — why should anyone believe you can close that gap?" The honest answer isn't "we're confident we will," it's a precise accounting of what was deliberately cut from the simplified spike and why each cut piece plausibly explains a meaningful share of the gap. Three things were missing from spike 1 that the real ErrorProbe pipeline has: (1) the tool-grounded Investigator stage, which cross-checks a hypothesis against the actual trajectory's tool outputs rather than reasoning about it in the abstract — this is precisely the stage the plan doc names as top Mid-1 priority; (2) Verified Episodic Memory, which lets the pipeline draw on prior verified diagnoses rather than starting cold on every case; (3) a materially stronger backbone than a free local 3B model — ErrorProbe's own published number almost certainly used a substantially more capable model. None of these three gaps is evidence the *underlying approach* is broken — the 75% agent-level accuracy, achieved with all three of those components missing, is itself a meaningful signal that the core hypothesis-generation logic has real traction. What the team cannot yet claim, and does not claim, is that closing those three gaps will fully close the accuracy gap; that is precisely the open, unproven part of R1, and the honest framing at any defense is "here is why we believe the mechanism works, and here is the specific, named work still required before we can claim the full number."

---

## 9.2 R2 — CrewAI/LangGraph mapping onto the execution-graph data model

**What it is.** Granite's core data model represents an agent execution as a graph — nodes for agent actions/steps, edges for dependencies between them. CrewAI and LangGraph are two real multi-agent orchestration frameworks with their own internal message-passing and tool-call semantics, and R2 asks whether those internal semantics can be mapped cleanly onto that graph model without losing information or introducing structural ambiguity. This matters because the whole cross-architecture generalization claim (one of Granite's two lead research questions) depends on being able to instrument *multiple* frameworks with the *same* underlying data model — if the graph abstraction doesn't actually fit a real framework's execution semantics, the generalization claim is hollow.

**Evidence.** POC spike 2 ran a toy three-agent CrewAI workflow with trace capture, and it traced cleanly into three graph nodes connected by two correctly-ordered edges — a clean, structurally sound result.

**Status and the one honest caveat.** Marked "Resolved," but with a specific follow-up flagged rather than swept under the resolved status: the timestamps captured in spike 2 were captured *post-hoc* (after the fact, presumably by inspecting logs or output order) rather than via real per-step instrumentation hooks fired at the moment each step actually executed. That's perfectly fine for validating the *structural* claim (do the nodes and edges come out correctly ordered), but it is explicitly flagged as "not yet trustworthy for latency metrics" — because a post-hoc timestamp doesn't capture real wall-clock timing with the precision a latency-overhead metric (one of the project's own committed non-functional requirements) would need. This is a good example of the register's general discipline: resolving the structural question doesn't get conflated with resolving the timing-precision question, even though both showed up in the same spike run.

---

## 9.3 R3 — Injected faults and ambiguous ground truth

**What it is.** Granite's entire benchmark-construction strategy depends on being able to inject a controlled fault into a multi-agent trace and know, with certainty, what the "ground truth" damage from that fault actually is — which step it corrupted, and whether/how far that corruption propagated downstream. If an injected fault produces ambiguous or unrecoverable ground truth (for instance, if the agent notices and self-corrects the fault, or if a naive check can't reliably tell whether corruption actually propagated), the whole benchmark's labels become untrustworthy.

**Evidence — and this is a case where the *process* is as instructive as the result.** POC spike 3 was actually run twice, and both runs are kept on record rather than just the second, cleaner one. The first attempt corrupted a "famous fact" (something like a well-known geographic or historical claim) and checked propagation using a naive substring-matching approach. The agent under test caught and self-corrected the injected error on its own — its output literally stated something like "Berlin is not the capital of France," directly contradicting the corrupted premise rather than propagating it. That's a genuinely useful negative result: it exposed that the substring-matching check the team was using was too crude to distinguish "the corruption propagated silently" from "the agent noticed and rejected the corruption." The second attempt used an unverifiable fabricated fact (something the agent has no independent way to catch — not a famous, checkable claim) combined with a more structured verification approach, and it produced clean, unambiguous blind propagation: the fault flowed downstream exactly as intended, and the checking logic could confirm this without doubt.

**Status.** Resolved, but resolved with an instruction to keep *both* results as documented cases, not just the successful second attempt. The register states this explicitly: "real fault behavior includes both self-correction and blind propagation, and the benchmark should account for that rather than assume only one." This is an important design implication that ripples forward into the real benchmark-construction work — fault types and injection strategies need to be chosen with an eye toward whether agents are likely to self-correct them, since a benchmark entirely made of faults agents reliably self-correct would produce artificially inflated "recovery" numbers that have nothing to do with Granite's own diagnosis and repair mechanisms.

---

## 9.4 R4 — Cross-paper backbone confound

**What it is.** When Granite compares its own results against published numbers from SDBL, AgenTracer, or Who&When, an apparent performance advantage (or disadvantage) might not actually reflect a difference in *method quality* — it might just reflect the fact that different papers used different LLM backbones (different underlying models with different raw capability levels), and a stronger backbone alone can produce a higher score regardless of the attribution method's own merit.

**Status.** This isn't something that needed a spike to discover — it's a known methodological confound in any cross-paper comparison, and the register records it as "Confirmed, already present" rather than something freshly tested. The mitigation is two-part: state the caveat explicitly in the evaluation write-up (already done in `ErrorProbe_Baseline_Selection.md`), and control backbone choice *within* Granite's own experiments — meaning that whatever comparisons Granite itself runs (e.g., its own attribution pipeline vs. its own reproduction of ErrorProbe) should hold the backbone constant across both sides of the comparison, so any difference in that specific, controlled comparison is attributable to the method, not the model. Status: "Accepted, documented" — this is a risk that gets managed through disclosure and controlled experimental design rather than "solved" outright, since it's inherent to doing any cross-paper literature comparison at all.

---

## 9.5 R5 — LLM API cost for benchmark generation

**What it is.** Generating the target 500–1,000 traces across multiple benchmarks and extensions, using paid LLM API calls, could exceed the team's budget. This is a resourcing risk, not a technical-feasibility risk.

**Status.** "Open" — genuinely still unresolved at the time the register was last updated, because the real answer depends on data that doesn't exist yet: real per-trace token counts from an actual POC run at production-realistic scale. The mitigation named is procedural rather than a fix already applied: estimate cost immediately once the POC gives real numbers, and split the budget strategically — cheaper models for high-volume generation work, reserving stronger (more expensive) models specifically for accuracy-critical evaluation runs where model quality actually matters to the result. This ties to `resources.md` §1 for the fuller resourcing detail. Worth noting: this risk is partially de-risked by the fact that every POC spike run so far has used a free local model (Ollama `llama3.2:3b`), meaning the team has already demonstrated it *can* do meaningful work at zero cost — the open question is specifically about whether the eventual full-scale, backbone-upgraded, large-benchmark work can stay within budget, not whether any work at all is affordable.

---

## 9.6 R6 — Team ownership: unassigned, and why that's a real risk, not a formality

**What it is.** The plan document defines three role areas — Data/Benchmark Owner, Diagnosis Engine Owner, and Platform Owner — each covering a genuinely distinct skillset (causal/graph modeling and data engineering; classifier/evaluation-method design; full-stack deployment engineering). R6 states plainly that as of the time it was logged, **no specific team member had actually been assigned to any of these roles.** This is flagged as a correction to earlier drafts, which the register says "wrongly presented this as already decided" — meaning at some point the documentation had drifted into implying an assignment existed when it didn't, and this was caught and corrected.

**Why this is treated as a real risk and not paperwork.** The three roles require meaningfully different skills. Causal/graph modeling (Diagnosis Owner) is conceptually and technically distinct from classifier/evaluation work, which is again distinct from full-stack deployment (Platform Owner). Assigning people to roles based on genuine skill-fit, rather than defaulting to an arbitrary or convenience-based split, is itself a real decision with consequences — a mismatched assignment could leave a subsystem under-resourced relative to the skills it actually needs. The register is explicit that "the assignment itself is a real decision, not a formality."

**Status.** "Open — must happen before Mid-1, currently fully unassigned." The mitigation is concrete and time-bound: assign real owners before Mid-1 (the second gate in the five-gate structure), based on actual skill-fit; record the decision per the guide's own change-control rule (§5.3); and propagate the decision into the plan doc §9, `architecture-sketch.md`, and `resources.md` once made. This risk connects directly to Assumption A5 (below) and reappears throughout Part 11 as one of the highest-priority open items, since it is squarely something the FYP guide itself would expect resolved well before a mid-project gate.

**Why this risk ripples into the guide's own §5 scope-sufficiency test, not just team logistics.** The Guide Compliance Audit's own §5 walkthrough flags this same gap from a different angle: of the six "scope principle" rows it checks (one shared central problem, meaningful primary ownership, interdependent work, shared engineering responsibilities, balanced depth not identical tasks, evolving division of work), the "meaningful primary ownership" row is marked with a caution flag directly tied to R6 — "Roles defined, not assigned to people." The audit further notes that one of the guide's own scope-sufficiency questions, "does each member have a defensible technical role," is "technically undermined until the ownership assignment... actually happens." This is a good illustration of how a single unresolved risk can quietly propagate into failing a *different* section's checklist too — R6 isn't just a team-logistics housekeeping item, it's load-bearing for whether the guide's own scope-sufficiency test can be honestly marked passed at all, since a role that exists only on paper without a person behind it isn't yet a "defensible technical role" in the sense the guide means.

---

## 9.7 R7 — The literature-crowding escalation: a full walkthrough

R7 is the single most heavily worked entry in the entire register — it has a base row, a triggered sub-table, two separate status-note updates, and a full re-triage, all under the same ID, because it kept generating new findings across multiple sessions rather than resolving cleanly in one pass. It deserves the fullest treatment here because the honest handling of this risk is arguably the best evidence in the whole project of the team's stated discipline: report real findings honestly, even when they're uncomfortable, rather than quietly softening them.

### 9.7.1 The base risk

**What it is.** R7 asks: what if a new paper closes one of Granite's two targeted research gaps — cross-architecture generalization, or silent-failure detection — before the project reaches Final-2 (its last gate)? The field of multi-agent failure attribution publishes roughly every 2–3 months, which is fast relative to a one-year FYP timeline. The mitigation named in the base row is procedural: re-check the literature at each of the five gates (this is a standing instruction written into the plan doc §15), and report honestly if a gap does get closed by someone else — the register is explicit that the benchmark and the deployable SDK "remain load-bearing either way," meaning even if a specific novelty claim gets undercut by a new paper, the project's actual deliverables (a real benchmark, a real installable system) still stand as contributions in their own right.

### 9.7.2 The first triage pass — 8 unverified papers surfaced

A literature search run on 2026-08-22 (explicitly noted as title/abstract level only — not a full read, and needing verification before being treated as settled) surfaced eight papers not present in the project's original seven-paper corpus, each of which might bear on one or both of Granite's claimed gaps. The register lists them with an initial threat-level assessment:

- **"Detecting Silent Failures in Multi-Agentic AI Trajectories"** (ACM ICPE Companion '26, arXiv:2511.04032) — confirmed real via WebSearch, reporting 98%/96% accuracy via XGBoost/SVDD anomaly detection. Initially concerning, but on inspection it operates at the *trajectory* level (is this whole run anomalous, yes or no) rather than being integrated with agent/step-level attribution the way Granite's silent-failure detection is scoped — a genuinely different granularity of claim. Downgraded to "Medium — real but narrower overlap than first feared."
- **"GraphTracer"** — described as modeling agent interactions as information-dependency graphs with causal tracing, sounding structurally close to Granite's own execution-graph-plus-backward-causal-tracing core. Flagged "High — verify first."
- **"FALAT: Tracing Failures in LLM Agent Trajectories via Dependency-Guided Search"** (arXiv:2606.00765) — same concern as GraphTracer, dependency-graph-based tracing. "High — verify."
- **"StepFinder"** (arXiv:2606.03467) — another attribution method, unclear overlap at the abstract level, "Medium — verify."
- **"From Confident Closing to Silent Failure"** (arXiv:2606.09863) — false-success/silent-failure characterization on tau2-bench and AppWorld. "Medium — verify."
- **"Silent Failure in LLM Agent Systems: The Entropy Principle"** (arXiv:2606.08162) — another silent-failure paper. "Medium — verify."
- **"DoVer: Intervention-Driven Auto Debugging"** (arXiv:2512.06749) — possible overlap with the counterfactual-recovery angle. "Medium — verify."
- **"FAMAS"** (spectrum analysis via repeated replay) — possible overlap with counterfactual/replay-based diagnosis. "Low-medium — verify."
- **"From Spark to Fire"** — a cascade/topological fragility study tested on LangGraph and CrewAI specifically. The register makes an important distinction here up front: this is a fragility/cascade study, not an attribution method or a benchmark, so it does not by itself threaten Assumption A2 (about CrewAI/LangGraph remaining unused by any attribution paper) — but the team flagged that the distinction needed confirming once actually read, not just assumed from the abstract. "Low — clarify, not a direct threat."

The register's own framing at this stage is deliberately calm rather than alarmist: "Do not panic-read all eight before defense — triage first," naming the two flagged "High" (the silent-failure detection paper and the GraphTracer/FALAT-style dependency tracing) as the ones that could actually undercut a claimed delta, worth reading first, with the rest treated as lower-urgency context. The standing instruction is repeated here too: if any of these papers do end up closing a gap, "that's a finding to report honestly at the defense, not a reason to abandon the idea" — because the specific *combination* Granite claims (cross-architecture generalization + silent-failure detection + counterfactual recovery + a deployable SDK, all evaluated together) is very unlikely to be fully matched by any single one of these papers, even if individual-gap novelty claims need re-checking against them.

### 9.7.3 GraphTracer and FALAT read in full: a peer-review status finding

A follow-up status note records that GraphTracer (arXiv:2510.10581) and FALAT (arXiv:2606.00765) were both read in full, and the key finding is about their *publication status*, not just their content: both are **arXiv preprints only** — not accepted or published at any peer-reviewed venue, unlike Granite's four kept baselines (ICML, ICLR, AAAI, ACL — all with confirmed proceedings). Both papers do cover territory close to Granite's core mechanism (dependency-graph tracing, counterfactual replay) and both report beating AgenTracer-8B, which sounds threatening on its face. But the register's decision is explicit and disciplined: **not added as baselines, not cited as established prior work, and no scope or claim in the project has been changed on the basis of either** — an unreviewed preprint is not a settled result, and the instruction is to keep re-checking their publication status at each gate rather than either dismissing them or over-reacting to them now.

### 9.7.4 The full triage — and the honest admission that the watch list itself was incomplete

A more complete title/abstract-level triage (same depth as the GraphTracer/FALAT first pass, explicitly not a full read yet) was run on 2026-08-22, and it did two things at once: it assessed threat levels for the original six unverified papers, and — more importantly — it surfaced **several additional relevant papers that had never been on the watch list at all**. The register records this honestly rather than treating the triage itself as having closed the risk: "the triage surfaced two things... meaning the watch list itself was incomplete. Recording that honestly rather than treating this triage as closing the risk."

Reassessment of the original six:

- **StepFinder** (Peking University) — step-level attribution on Who&When, using an LLM only for feature construction and then a lightweight temporal-attention model, reporting 79% faster inference than LLM-based methods. Reassessed to "Low-Medium" — it's about *efficiency*, not generalization or silent-failure detection, so it doesn't actually touch either of Granite's two claimed gaps.
- **"From Confident Closing to Silent Failure"** (Laksh Advani) — this one escalated sharply on a full look. It's a real, working, publication-quality silent-failure detection study: tested on tau2-bench (9,876 trajectories) and AppWorld (1,879 trajectories), it finds that LLM judges perform poorly at this task (AUROC ≤0.65) and ships lightweight TF-IDF-based detectors that hit 0.83–0.95 AUROC. This is escalated to **"High — escalated,"** because it hits Granite's silent-failure pillar directly, with real, credible results — not just a similar framing.
- **"Silent Failure in LLM Agent Systems: The Entropy Principle"** (arXiv:2606.08162) — flagged for a different reason than topical overlap: its framing ("Entropy Principle," a "PIG Engine," a formalized decay equation S(t)=S0·e^(αt)) reads as unusually grandiose for what appears to be a single-author-style arXiv post, and the register explicitly connects this to a risk pattern the project has already encountered elsewhere in its own history — the "Dougherty thesis" pattern, where source credibility itself, not just topical overlap, needs scrutiny before citing something. Kept at "Low," but flagged for credibility scrutiny specifically.
- **DoVer** (arXiv:2512.06749, Microsoft Research authors) — escalated to **"High."** This is a real, credible, methodologically sophisticated "intervention-driven debugging framework" that verifies hypotheses via targeted interventions (editing messages, altering plans), and it explicitly argues that single-step attribution is "ill-posed" because multiple interventions can independently repair a failure. This is a Microsoft-authored paper taking a serious, on-target approach to exactly the counterfactual-intervention mechanism Granite also relies on.
- **FAMAS** (its real title turns out to be "Who is Introducing the Failure? ... via Spectrum Analysis," arXiv:2509.13782) — spectrum-based statistical fault localization via repeated re-execution, at roughly $1/run, which is costly to scale. Its peer-reviewed form was also found during this pass: "Spectrum-based Failure Attribution for Multi-Agent Systems," accepted at FSE 2026 (ACM Foundations of Software Engineering, a legitimate top software-engineering venue). This is a genuine status upgrade — from an unverified preprint to a confirmed peer-reviewed publication — and the register notes this probably deserves proper addition to the peer-reviewed corpus rather than staying in the "unverified preprint" bucket. Threat level: "Medium, but status upgraded."
- **"From Spark to Fire"** (arXiv:2603.04474) — confirmed as originally assessed: a cascade/fragility study testing six frameworks including CrewAI and LangGraph for *topological fragility*, not attribution. Confirmed not to threaten Assumption A2 for attribution purposes, but the register notes CrewAI/LangGraph are "no longer completely unused in the broader multi-agent robustness literature" — worth a one-line acknowledgment in the project's own writing, not a scope change. "Low, as originally assessed — confirmed, not just assumed."

And then the newly surfaced papers — ones that were never tracked before this triage pass at all:

- **"Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures"** (arXiv:2606.08275) — title alone suggests direct overlap with counterfactual attribution.
- **"From Flat Logs to Causal Graphs: Hierarchical Failure Attribution for LLM-based Multi-Agent Systems"** (arXiv:2602.23701) — sounds structurally close to Granite's own graph-based core, similar in spirit to GraphTracer.
- **"MASPrism: Lightweight Failure Attribution for Multi-Agent Systems Using Prefill-Stage Signals"** (arXiv:2605.07509) — another attribution method, unclear overlap.
- **"When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime"** (arXiv:2606.14589) — a third silent-failure paper found in this same session.
- **"Outcome Monitors: Recovery Affordances for Silent Tool Failures"** (arXiv:2608.19303) — directly named "silent," directly about recovery — potentially overlapping with both of Granite's claimed pillars at once.
- **"TrajAudit: Automated Failure Diagnosis for Agentic Coding Systems"** (arXiv:2605.26563) — attribution-adjacent.
- **"MAESTRO: Multi-Agent Evaluation Suite for Testing, Reliability, and Observability"** (arXiv:2601.00481) — could overlap with Granite's own testing-harness/product framing.

All seven of these are marked simply "Unverified" — no threat-level judgment has been made on any of them yet, because they haven't been read even at the triage level the original six received.

**The register's honest bottom line, stated directly:** "this field is more crowded than the original 9-paper corpus + 8-paper watch list captured. Two items (the silent-failure detection paper and DoVer) are credible enough, on-target enough, and specific enough that a full read would remove one specific defense risk: a panelist raising either one and the team having no answer."

### 9.7.5 The explicit, recorded decision not to chase every preprint

Rather than spending remaining prep time reading every paper on this now-expanded list, the team made a deliberate, recorded decision on 2026-08-22 to accept this risk instead. The reasoning, as stated in the register: neither of the two high-threat papers was ever going to be cited, added as a baseline, or change the contribution statement — Granite's actual strategy is "improving on ErrorProbe (peer-reviewed)," not pre-empting every unpublished preprint that might overlap in territory. The register frames this explicitly as "a deliberate, recorded scope decision, not an oversight," logged under the same change-control discipline used throughout the register (the FAST guide's §5.3). If either paper does come up at defense, the fallback answer is the same one already established for GraphTracer/FALAT: "real, but unreviewed, and here's what survives regardless" — meaning the combination of cross-architecture generalization, silent-failure detection, counterfactual recovery, and a deployable SDK, evaluated together, is the actual claim, and the individual-gap novelty claims are what need re-checking against the newer papers specifically, not the whole project's premise.

This entry is worth dwelling on because it demonstrates something the project's discipline is explicitly built around: distinguishing between "we found something uncomfortable and hid it" and "we found something uncomfortable, assessed it honestly, made a reasoned decision about it, and recorded that decision for scrutiny." R7 is the clearest single example of the latter pattern anywhere in the register.

### 9.7.6 Why R7 is the register's best evidence of real, ongoing rigor — and what a panel question actually tests here

It's worth being explicit about why this single risk entry carries so much weight in assessing the project's overall trustworthiness. R7 shows a full cycle: first pass (title/abstract triage, calibrated but incomplete), correction (a paper wrongly treated as an equivalent fifth baseline, caught and reverted — see Part 10's discussion of this same event in the AI Usage Log), escalation (two papers read in full and found genuinely more threatening than the first pass suggested), honest admission of incompleteness (the watch list itself grew during its own triage, and the register says so directly rather than quietly expanding the list without comment), and finally a *recorded decision to accept residual risk* rather than chase it to zero. That last step is the one many student projects skip entirely — either by not noticing the risk exists, or by noticing it and not writing down a reasoned stopping point, leaving the impression (fair or not) that unread material was simply ignored.

If a panelist asks "have you read DoVer?" the honest, prepared answer is not "no" delivered defensively — it's: "We found it during a literature triage, assessed it as credible and directly on-target, and made a recorded decision not to do a full read before defense, because our contribution isn't contingent on DoVer not existing — here's specifically why." That is a fundamentally different, stronger position than either overclaiming familiarity with a paper the team hasn't actually read, or being caught flat-footed by a paper the team genuinely never encountered. R7's whole multi-pass history exists to make that stronger position available and honestly earned, not asserted.

---

## 9.8 R8 — Extension creep / breadth-over-depth

**What it is.** With thirteen (later expanded to more) scheduled extensions on the books for FYP-2, there's a real temptation to chase breadth across many extensions rather than depth on the committed core, thinning out the actual core evaluation work in the process.

**Mitigation and status.** The committed core (plan doc §7) is fixed, and extensions are explicitly gated on the core being complete first — this is a structural mitigation baked into the scope design itself, not a promise to be disciplined later. Status: "Mitigated by scope design." This risk connects directly to the Framework Compatibility Layer decision (R20 below), which is explicitly designed as a *lighter* form of extension work specifically to avoid ballooning engineering effort across seven frameworks.

---

## 9.9 R9 — Commercial observability market comparison

**What it is.** An established commercial market already exists for agent observability tooling — LangSmith, Langfuse, Braintrust, Arize/Phoenix are named specifically — and the FAST guide's own §10 ("Product, Prior-FYP and Workflow Comparison") requires the project to compare itself against real products, not just academic papers.

**Evidence and the honest correction embedded in the resolution.** Resolved on 2026-08-22, documented in `Commercial_Product_Comparison.md`. But the resolution isn't a clean "nobody does this" story — the register explicitly corrects an earlier, staler assumption: LangSmith Engine and Arize's "Alyx"/Signal (both 2026 products) *do* claim automated root-cause diagnosis plus fix generation. The register states plainly: "the 'nobody automates this' framing was stale and has been corrected, not just filled in." This is another example of the project catching its own overclaim before it became load-bearing. The positioning that survives this correction is narrower and more defensible: none of the six commercial platforms checked confirm multi-agent step-level attribution, counterfactual replay, silent-failure detection, or cross-framework generality as *documented, evaluated* capabilities — that's the real differentiation now on record, not "nobody automates diagnosis at all."

**Status.** "Closed — spot-check against live vendor docs before final submission, since commercial feature pages change faster than papers." This closure comes with an explicit maintenance instruction, consistent with the general pattern that commercial claims are treated as more perishable than academic citations and need periodic re-verification.

---

## 9.10 R10 — Silent-failure detection: built and tested only after a panel-review pass caught it missing

**What it is.** Silent-failure detection is one of Granite's two headline novelty pillars (RQ3, the project's second research question). R10 records a genuinely important process finding: this mechanism "had never been built or tested even once" until a self-conducted, adversarial panel-review pass caught the gap — this was a real, substantive miss, not a documentation oversight where the mechanism existed but wasn't written up.

**Why this matters as a finding about the project's own process, not just about the mechanism.** The AI Usage Log records this same event from a slightly different angle (see its "second correction worth recording" entry): a full panel-style, adversarial self-review found two real gaps that had survived every prior pass — the silent-failure mechanism never having been built despite three POC spikes having already run, and no written defense existing against the "you just combined existing techniques" objection. The log's own framing of this is instructive: "catching your own gaps late is a normal part of a rigorous process — the failure mode this log exists to prevent is not catching them at all." R10 is the risk-register-side record of exactly that catch.

**Evidence — two distinct things run, and the honest limitation of each stated plainly.** POC spike 4 ran two separate checks. First, an n=3 real LLM task run: the model got all three tasks correct, meaning *no natural silent failure occurred* to actually test the detector against — a real result, but a limited one, since a detector that never sees a real failure hasn't been tested against real failure conditions. Second, and more informatively, a direct mechanism test decoupled from real LLM behavior: the rule-based checker was fed known-wrong values, including a plausible-magnitude near-miss ($20.00 vs. the true $19.75) designed specifically to be hard to catch with a naive check, and it correctly flagged every wrong value while correctly passing every correct value — zero false positives.

**Status and why it's still open.** "Open — mechanism validated directly, empirical frequency of natural silent failures still unconfirmed." The register's own framing: "Real, honest first data point; not proof the detector catches failures 'in the wild' yet." This is a careful, load-bearing distinction — proving the checker correctly discriminates known-wrong from known-right values in a controlled test is not the same claim as proving it will reliably catch silent failures that occur naturally during real agent execution, since real silent failures might take forms the rule-based checker's current schema/constraint logic doesn't anticipate. The AI Usage Log adds a further instruction on this point: "Team must independently re-run this and design at least one case where the model is more likely to genuinely err, since n=3 with zero natural failures is a real limitation, honestly reported... not papered over."

**Why the two-part test design is itself worth understanding, not just the results.** Splitting the test into "does a real model produce a natural silent failure to detect" (part 1) and "does the detection logic correctly discriminate known-wrong from known-right values when fed them directly" (part 2) is a deliberate way of isolating two independent variables that a single combined test would have confounded. If only part 1 had been run and the model happened to get all three tasks right, the naive conclusion might have been "we don't know if the detector works" — an unhelpfully total dead end. By separating out part 2, the team can make a specific, defensible claim ("the discrimination logic itself works correctly against known cases") while being equally specific about what remains unknown ("how often does a natural silent failure actually occur, and does it look like the cases we tested against"). This is the same discipline visible in R13/R17's distinction between "can the pipeline mechanically replay a correction" and "can the pipeline generate a correct correction in the first place" — decomposing a compound claim into its independently-testable parts, rather than reporting one aggregate pass/fail number that obscures which half of the claim is actually supported.

**The acceptance criterion this connects to.** The plan doc's own §0.07 states the acceptance criterion for this exact functional requirement (FR3, the hardest of the five stated requirements): "a diagnosis record is accepted as correctly identifying a silent failure if the constraint-verification module flags the trace *and* the flagged step matches the fault-injection harness's recorded ground-truth injection point, within an agreed tolerance." Spike 4's part-2 test is a direct, if small-scale, first instance of exactly this criterion being checked — the $20.00-vs-$19.75 near-miss case is specifically designed to probe the "within an agreed tolerance" boundary, since a naive check might treat a near-miss as "close enough" and silently pass it, which is exactly the failure mode a silent-failure detector must not have.

---

## 9.11 R11 and R11b — TracerTraj: the dataset that turned out not to exist

### 9.11.1 R11 — the core finding

**What it is.** TracerTraj-2.5K, AgenTracer's own benchmark dataset, had been cited throughout the project's early documentation as a baseline-reproduction dataset — something the team could download and use to reproduce and compare against. R11 records a direct, hands-on finding: it is **not actually publicly released.** Crucially, the register is explicit about *how* this was found — "Confirmed by direct repo download attempt, 2026-08-22, not by re-reading a citation." This distinction matters a great deal for the project's own epistemic discipline: the team didn't just re-read AgenTracer's paper and notice a caveat they'd missed; they went to the actual repository and tried to get the data, and found it wasn't there.

**What's actually there instead.** AgenTracer's repository states that data and weights are "committed to" being open-sourced "upon acceptance of the paper" — a future promise, not a present fact — there is no LICENSE file at all, and only a 127-row sample (specifically covering the code domain) is genuinely real and downloadable.

**Impact and mitigation.** This is confirmed, not hypothetical, medium-to-high impact, because it directly affects the evaluation plan's TracerTraj comparison point (plan doc §11). The mitigation is a scope adjustment, not a technical fix: reproduce ErrorProbe against Who&When only for now, since Who&When is fully available (184 real cases already downloaded), and either treat the TracerTraj-benchmark comparison as gated behind AgenTracer's actual eventual release, or scope it down explicitly to the one real 127-row sample and *label it honestly as such* — never presented as "the TracerTraj benchmark" when it's really a small sample of it.

**Status.** "Open — plan doc §4 and §11 need updating to stop citing TracerTraj as available baseline data." This status line is itself evidence of the discipline at work: rather than quietly fixing the citations and moving on, the register records that the fix is still owed and names the specific sections that need it.

### 9.11.2 R11b — the real, hands-on attempt to build a replacement, and why it was abandoned

**What it is.** Given that TracerTraj-2.5K wasn't actually available, the team attempted, on 2026-08-22, to self-generate a roughly 2,000-row TracerTraj-*style* dataset by running AgenTracer's own published pipeline (which uses MetaGPT and a function called `generate_repo`) against a combined pool of MBPP+ (378 tasks) and KodCode hard/medium tasks (1,622 tasks), using a free local model (Ollama `llama3.2:3b`) instead of paying for API access.

**Real engineering work done along the way, not just a failed attempt.** This wasn't an idle try — real environment and pipeline bugs were found and fixed in the process. MetaGPT's provider module eagerly imports every vendor LLM SDK at startup, which broke against a trimmed-down requirements file that didn't include every one of those vendor SDKs; this had to be diagnosed and worked around. Separately, Ollama's actual API endpoint turned out to be `/api/chat`, not `/chat` as the initial configuration assumed — meaning every call was silently 404'ing until this was caught and fixed. Both of these are the kind of real, concrete infrastructure debugging that demonstrates genuine hands-on engineering effort, not a superficial attempt.

**Why it was abandoned, with real timing data as the evidence.** Once the pipeline was actually working end-to-end, the very first single pilot task took over ten minutes to run an eight-round multi-agent session on the local 3B model, without completing. Extrapolating that timing even at a modest concurrency level of three simultaneous tasks, the full ~2,000-task run would take multiple days of continuous local compute — not hours, and not remotely practical within the available proposal-stage timeframe.

**Status and what remains.** "Closed, by user instruction 2026-08-22 — stopped, not left running." The register is careful to record that this was a deliberate stop on explicit instruction, not something quietly abandoned mid-run without anyone deciding to stop it. The dataset ceiling remains the 127-row real AgenTracer sample (`agentracer_full/data/tracertraj-code-test.parquet`), plus the two task pools that were generated but never actually used for the full run (`mbppplus-full.parquet`, `kodcode-hardmedium.parquet`) — these are explicitly left in place on disk in case local generation is worth revisiting later with more time or a paid API budget. This is a good example of a negative result that still leaves useful residue: the abandoned attempt didn't just waste time, it produced real, reusable task pools and fixed real pipeline bugs that would otherwise block any future attempt at the same idea.

**Why "closed by explicit instruction" is a meaningfully different status than simply "abandoned."** It's worth being precise about the distinction the register draws here, because it maps onto a broader theme in how this project treats its own negative results. An item that gets quietly abandoned — someone stops working on it, nobody records why, and it simply disappears from view — leaves a reader unable to distinguish "this failed for a good, informative reason" from "someone got bored" or "someone forgot." R11b is explicitly the former: real timing data came in, that data was extrapolated to a concrete, credible multi-day estimate for the full run, and a person made a deliberate call to stop based on that evidence, which is then written down as the reason. This is the same pattern the register applies to Spike 7's negative classifier result (R15) and to Verified Repair Memory's failed test (R18) — a negative result, honestly reported with its reasoning intact, is treated as valuable project information in its own right, not as a failure to be minimized or hidden. A cost/benefit calculation that concludes "not worth pursuing further right now, and here's the arithmetic" is itself a legitimate piece of engineering judgment, and R11b records that judgment rather than just its conclusion.

---

## 9.12 The Assumptions table (A1–A5)

The Assumptions table records five load-bearing assumptions the project rests on, each with a stated consequence if it turns out to be wrong — this is the standard RAID discipline of naming what you're taking on faith so that a violation of the assumption is caught and escalated rather than silently absorbed.

- **A1** — ErrorProbe's methodology is reproducible from the published paper alone, without needing its (unlicensed) code. If wrong, "reproduction becomes a research risk in itself — escalate to R1." This is the assumption underlying R1's entire premise; POC spike 1's real but partial result is the first evidence bearing on whether A1 holds.
- **A2** — CrewAI and LangGraph remain genuinely unused by any published failure-attribution paper through Final-2. If wrong: "Re-verify at each gate (tied to R7); if a new paper uses one, pick a different 3rd/replacement architecture." This assumption is directly what R7's literature triage keeps testing — "From Spark to Fire" tests CrewAI/LangGraph for fragility, not attribution, so A2 survives that specific paper, but the assumption needs continued re-checking as the field publishes more.
- **A3** — Public task sources (GAIA, MBPP+, Who&When, TracerTraj) remain accessible under their stated licenses for the project's duration. If wrong: "Re-check licenses at Mid-1 (data/licensing clearance gate, plan doc §12)." Note that TracerTraj's status under this assumption already required correction via R11 — the assumption wasn't fully wrong (Who&When, GAIA, MBPP+ remain fine) but was partially wrong in a way that had to be caught and isolated.
- **A4** — The chosen LLM API provider(s) stay available and within budget for two semesters. If wrong: "Budget re-estimated after POC (R5); keep a fallback provider identified." Directly tied to R5's open cost-risk status.
- **A5** — Originally stated as "the 3-person ownership split stays stable across both semesters." The register marks this "Invalid as stated," with a correction dated 2026-08-23: "the split isn't made yet, so there's nothing to stay stable." The revised assumption is that the three roles get assigned before Mid-1 and *then* stay stable. If assignment is delayed past Mid-1, or reallocated later, the register requires that this "be recorded per the guide's change-control rule (§5.3), not silently absorbed" — meaning any future reshuffling of roles needs to be an explicit, logged decision, not something that just happens without documentation.

A5's correction is worth pausing on specifically because it's a clean, self-contained example of the register catching and fixing its own earlier error: an assumption was originally written in a form that presupposed a decision had already been made (a "3-person ownership split"), when in fact that decision (R6) hadn't happened yet. The fix wasn't to delete the assumption but to strike through the invalid framing, mark it invalid explicitly, and restate a version of the assumption that's actually consistent with reality as of the correction date.

**Why an assumption can be wrong in a subtler way than "the fact is false."** A1 through A4 are all assumptions of the ordinary kind — each states a fact-like claim about the world (ErrorProbe is reproducible from the paper alone; CrewAI/LangGraph stay unused; licenses stay stable; the API budget holds) that could simply turn out true or false when checked. A5's original form was a different, subtler kind of error: it wasn't wrong because the underlying fact was false, it was wrong because the sentence itself smuggled in a premise (that a split already existed) that hadn't been established. This is worth naming as its own category of documentation risk, distinct from a factual mistake — a sentence can be grammatically and structurally sound, sound confident, and still misrepresent the actual state of a decision simply by phrasing itself in a way that assumes the decision is behind you rather than still ahead of you. The fix — correcting A5 to assume nothing about *when* the split happens, only that it needs to happen before Mid-1 and then hold — is a small but genuinely instructive example of the kind of close reading this project's own review discipline was applying to its own documents, not just to external claims about papers or products.

**How A2 and A3 are actively, not passively, monitored.** It's worth noting that A2 and A3 aren't "set and forget" assumptions — each is explicitly tied to a recurring check built into the timeline itself, not just a one-time verification. A2 (CrewAI/LangGraph staying unused by any attribution paper) is directly the subject of R7's literature-triage machinery, and the plan doc's own §15 names a standing instruction to re-check the literature at every one of the five gates specifically for this. A3 (dataset licensing) is tied to the Mid-1 gate's own "data/licensing clearance" requirement (plan doc §12) — meaning A3 isn't assumed to hold for the whole two-semester duration untested, it gets a scheduled re-verification point built into the project's own gate structure. This is a meaningful distinction from an assumption that's simply stated once at proposal stage and never revisited — both A2 and A3 have a designed mechanism for catching a violation before it becomes a late-stage surprise.

---

## 9.13 The Issues table (I1–I3): currently open, blocking items

Issues, in RAID terms, are distinct from Risks — a Risk is something that *might* happen and would have an impact if it did; an Issue is something that has *already* happened and is *currently* blocking progress on something else.

- **I1** — Originally: "POC (3 spikes, §10) not yet executed," blocking Gate 1's evidence requirement. Marked "Resolved 2026-08-22" with a strikethrough on the original text — all three spikes were run, with real output in hand, kept initially at `E:\ai-workspace\poc\` and slated to move into the project folder proper. Owner: all three students. Status: "Closed." This is a clean example of an Issue being genuinely resolved rather than just marked resolved — the resolution links directly to R1–R3's real evidence above.
- **I2** — "Real stakeholders not yet contacted." This blocks CCP characteristic #6 ("diverse stakeholders") from moving past "weak" status in the plan doc's own CCP rating (§2). Owner: the whole team. Target resolution: "Before defense (this week)" — this is a live, time-pressured item, and it reappears as the single highest-priority open item across every "what remains open" list in the project (see Part 11 below). It is worth noting that I2 is the one Issue on this table that genuinely cannot be resolved by any amount of further internal documentation, spike-running, or AI-assisted drafting — it requires a real conversation with a real person outside the team, which is precisely why it survives, unresolved, across every single status check this document has drawn from (the risk register's own Issues table, the plan doc's §16 self-check, the Guide Compliance Audit, and the supervisor PDF's "What Remains Open" list all name it independently).
- **I3** — Originally: "AI usage log not yet started," a requirement under the FAST guide's §8.4. Marked "Resolved 2026-08-22" — see `AI_Usage_Log.md`, which by that point already covered ideation, coding, debugging, and documentation activity from the session, with a per-entry verification status and a standing list of what the team still owes. But the resolution comes with an explicit ongoing obligation: "Whole team — must keep updating this going forward, not treat it as done." Status: "Closed for this session; ongoing maintenance required." This distinction — closed for the moment, but requiring continued upkeep — is important, and it's exactly the pattern the log itself demonstrates across its nine recorded sessions (Part 10 covers this log in depth).

---

## 9.14 The Dependencies table (D1–D4)

Dependencies record external things the project's progress relies on, distinct from risks the team can actively mitigate through its own choices.

- **D1** — Data/licensing clearance on Who&When, TracerTraj, and TraceElephant. Who&When is MIT-licensed, confirmed, and the full 184-case dataset was downloaded 2026-08-22 — fully cleared. TracerTraj's status is corrected in the same entry as R11: not actually released, so any plan depending on the full 2,000+ trajectory set needs downgrading. TraceElephant is CC BY 4.0. The status note is specific about what still works despite TracerTraj's gap: "R1's ErrorProbe reproduction can still use Who&When alone; the TracerTraj-benchmark comparison point in the evaluation plan (§11) needs to either wait for AgenTracer's actual release or be scoped down to the 127-row sample honestly labeled as such."
- **D2** — Supervisor approval of the Stream A declaration and committed scope, needed for Gate 1 (the proposal defense). Status: "Pending defense" — this is simply awaiting the gate itself.
- **D3** — LLM API access (keys, approved budget) for the *full* build, needed specifically for full-fidelity ErrorProbe reproduction (the tool-grounded Investigator stage, Verified Episodic Memory) on a stronger backbone, and for large-scale benchmark generation (500–1,000 traces). Status: "Partially superseded" — because POC spike 1 ran entirely free on a local model, this dependency wasn't actually needed for the proposal-stage POC itself. But a real budget/backbone decision is still pending for the FYP-1 core build proper, where a stronger backbone genuinely is needed for a fair ErrorProbe comparison (tied directly back to R1).
- **D4** — CrewAI/LangGraph framework version stability, needed so instrumentation work doesn't break mid-project as the underlying frameworks release new versions. Mitigation: pin dependency versions once instrumentation work actually starts.

---

## 9.15 The first addendum: three spikes run 2026-08-23 (R13, R14, R16, R15)

This block of new risk/evidence rows was added specifically to close gaps that had been found in a prior session's "alignment check" — a pass where the team checked the POC spikes actually run so far against the frozen list of foundational features, and found some foundational items had zero evidentiary backing.

### 9.15.1 R13 — Verified Automatic Repair had zero POC evidence

**How this was found.** While checking the four existing spikes against the frozen sixteen-item feature list on 2026-08-22, the team noticed that Verified Automatic Repair (at the time still called "counterfactual replay engine") had never actually been tested — a real gap in evidentiary coverage for a foundational, committed-core item.

**Evidence.** Spike 5 ran a three-step deterministic pipeline: inject a corrupted value at step 1, then deterministically re-execute steps 2 and 3 after the value is corrected. The result: `recovery_success: true` — the corrupted trace's final output (97.2, when the expected correct value was 108.0) recovered to exactly 108.0 after the replay logic ran.

**The honest limitation, stated in the same entry as the positive result.** The register is explicit: "Real but narrow: this tests only the mechanical replay-and-recompute logic, not whether an LLM can correctly *guess* the fix — that's a separate, still-open concern." This is an important distinction that recurs throughout the register — there are two genuinely separate questions bundled under "does repair work": (1) if you already have a correct fix, can the system mechanically re-execute downstream and recover the right final answer (this is what spike 5 tests, and it works), and (2) can the system actually *generate* that correct fix in the first place (this is a completely different question, later addressed separately by Repair Agent and spike 8, R17 below).

**Status.** "Mechanism validated — closes the R7-adjacent gap from the last session." (Note: this cross-reference to "R7-adjacent" in the original text appears to refer to the prior session's alignment-check gap, not literally R7 the literature risk — it's describing the same class of "we found a spike-coverage gap and closed it" pattern.) Still owed: "Real recovery-rate measurement on the actual benchmark (not this toy pipeline)" — spike 5's three-step deterministic pipeline is a proof of mechanism, not a measurement of how often this actually works at benchmark scale on real, messy traces.

### 9.15.2 R14 — Cyclic/dynamic graph support

**What it is.** An extension-level feature (cyclic/dynamic graph support) had never been tested on an actual cycle — only on a simple three-node DAG (directed acyclic graph) from spike 2. This matters because LangGraph, one of Granite's two committed core architectures, natively supports cyclic workflows (retry loops, iterative refinement loops), so if Granite's graph model can't handle a real cycle, its own cross-architecture claim would be incomplete on the very framework it commits to instrumenting.

**Evidence.** Spike 6 ran two real cases: an unrolled retry loop (which terminated cleanly, reaching all nodes) and a *true* cycle between a Researcher agent and a Critic agent (which also terminated cleanly with a revisit bound in place, reaching all nodes, with the Researcher visited three times and the Critic visited four times, exactly as expected). Critically, a **control case** was also run: the same true-cycle graph, but with the revisit bound effectively disabled. This control case hit the pipeline's 10,000-step safety cap instead of terminating naturally. The register calls out why this control case matters so much: it "confirms the bound is load-bearing, not a no-op that happened to pass" — meaning the passing result on the real cases isn't an accident of the graph being small enough to terminate on its own; the revisit-bound mechanism is genuinely doing the work of preventing infinite traversal.

**Status.** "Resolved — mechanism works as designed."

### 9.15.3 R16 — Security/privacy threat model

**What it is.** This is the FAST guide's own §12 risk category for security/privacy feasibility, applied to Granite specifically: the SDK ingests third-party trace data, and the active benchmark target (tau-bench retail) implies that real traces could plausibly contain customer-PII-like content (names, order details, addresses, and similar).

**Why this was flagged as a genuine gap, not routine housekeeping.** The Guide Compliance Audit's deeper pass explicitly calls this out as "the most substantive finding in this audit" — meaning that a first-pass, section-level compliance check had missed it entirely, and only a finer-grained audit against the guide's own risk-category sub-table caught that security/privacy feasibility had no answer at all in the project's documentation up to that point.

**The threat model itself, in full.** Three data categories are identified, each with a different risk level: (1) customer trace data — the highest risk category, since this is real execution data from the customer's own agent system and could plausibly contain PII; (2) the diagnosis engine's own derived output (root cause, confidence score, and similar) — low risk, since this is Granite's own computed analysis rather than raw customer data; (3) public benchmark/dev data (Who&When, GSM8K, tau-bench, and similar) — no risk, since this data is already public.

On top of the categorization, the design principle committed to is "minimum-context-per-call" — only the minimum necessary per-step context is ever sent to the LLM API for any given call, never the full raw trace in bulk. Storage stays local (SQLite or Postgres), and nothing is forwarded past the LLM API call itself.

Three specific, FYP-achievable mitigations are committed: (1) regex-based PII redaction of PII-shaped fields before any data is persisted to storage; (2) per-project namespacing, so that one customer's data is never visible to another customer — this is explicitly tied to and reuses extension #4 (already committed as part of the extension list) rather than inventing a separate mechanism; (3) time-bounded retention, so data doesn't accumulate indefinitely.

The register is explicit about scope discipline here too: this is "explicitly not a full GDPR/CCPA-grade compliance program — same scoping logic as the SaaS-signup deferral" (referring to the plan doc's own decision to drop a hosted multi-tenant SaaS billing flow from scope as generic plumbing that doesn't touch the CCP). This is a deliberately bounded, FYP-appropriate threat model, not an attempt to build enterprise-grade compliance infrastructure within a one-year student project.

**Status.** "Resolved — paragraph on record, not yet independently reviewed by the team." Written 2026-08-23. Same as many other entries, "resolved" here means the analysis and commitment exist and are documented, not that the team has yet independently re-derived and sat with the reasoning themselves — that verification remains an open item (see Part 11).

**Why this deserved to be treated as "the most substantive finding" in the deeper compliance audit, not a routine box-tick.** It's worth being explicit about why a missing security/privacy paragraph is a genuinely serious gap for this specific project, rather than boilerplate the guide requires and any project could satisfy with a throwaway sentence. Granite's own active benchmark target is tau-bench retail — a customer-support/retail domain chosen specifically because it's a realistic proxy for the deployment context the notional client (§0.06) actually operates in. A retail customer-support trace plausibly contains names, order numbers, addresses, payment-adjacent details — exactly the kind of content a PII-redaction requirement exists to catch. Because the SDK's entire value proposition is ingesting a *third party's* real execution traces (that's the whole point of a deployable diagnosis tool — it has to look at someone else's system, not just the team's own toy workflows), a security/privacy analysis isn't an optional nicety layered on top of the technical contribution, it's a precondition for the deployable-SDK half of the contribution claim being credible at all. A tool that can't articulate what happens to a customer's trace data isn't yet a tool a real engineering team (the very stakeholder R6/I2 are also trying to get real contact with) could respons­ibly adopt.

**The distinction from R16's plan-doc counterpart, §0.09 (ethical compliance).** It's worth being precise that R16's threat model and the plan doc's separate §0.09 "ethical compliance" section are related but distinct: R16 is about *what data flows where and how it's protected* (a security/privacy engineering question), while §0.09 is about *whether it's appropriate to act on that data at all* — the three ethical commitments there are that diagnosis output stays advisory (a human reviews before any fix is applied, so the system cannot silently take a consequential action), that using any real user's or organization's trace data requires informed consent arranged in advance rather than assumed, and that synthetic fault injection is restricted to the team's own or consenting pilot systems, never a third party's production system without explicit permission. The two sections reinforce each other but answer different questions — R16 protects the data itself, §0.09 governs the human relationship and consent context the data comes from and the actions taken on it.

### 9.15.4 R15 — Preventive clarification classifier: a genuine negative result, reported honestly

**What it is.** An extension-level feature — a "lightweight, not RL [reinforcement learning]" preventive clarification classifier, per the plan doc's own §7.0 framing — had never actually been checked for whether cheap features (the kind of lightweight signal the "not RL" framing implies) carry any real predictive signal at all.

**Evidence — and this is the register's clearest example of an honestly-reported negative result.** Spike 7 trained a TF-IDF (term-frequency features) plus logistic-regression classifier on 20 hand-written clean-vs-corrupted handoff pairs (with 8 held out for testing). The result: precision 0.25, recall 0.25, f1 0.25 — essentially random-chance performance for a binary classification task. The register states this plainly: "near-random, not a working classifier yet. Honest negative-leaning result, not hidden."

**Why this is treated as "Open, real finding, not a blocker" rather than a dead end.** The register names two specific, testable hypotheses for *why* the result is this weak, rather than concluding the whole idea is unworkable: (1) the training set of 20 hand-written examples is almost certainly too small and, more importantly, not representative of real corruption patterns — the actual, better test needs labeled pairs generated by the fault-injection harness itself, not authored by hand by a human trying to imagine what corruption looks like; (2) it's possible that bag-of-words (TF-IDF) features are genuinely too weak a representation for this specific task, in which case the next thing worth trying — before concluding the whole classifier idea needs heavier machinery — is cheap sentence-embedding features, which are still local and still free (no API cost), just a richer representation than raw term frequencies.

**Status.** "Open — real finding, not a blocker." This entry, and the decision about what to do with it, reappears directly in Part 11 as one of the genuinely still-undecided open items (see 11.7 below) — the plan doc's own timeline (Weeks 8–14 of FYP-2) explicitly makes this extension slot "contingent, not automatic" on the re-test with better data/features actually improving the result.

---

## 9.16 The second addendum: market survey review, 2026-08-24 (R17, R18, R19)

This block of entries comes from a session where the team reviewed `Agentic_AI_Market_Survey_BS_FYP.docx`, a market survey covering seven orchestration frameworks (OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI) plus a fresh read of ErrorProbe. The register is careful to distinguish this from `Commercial_Product_Comparison.md` (which covers a different market layer — observability/eval platforms like LangSmith and Langfuse). This survey checks the *orchestration-framework* layer Granite actually instruments — the frameworks whose traces Granite is built to diagnose, not the tools that compete with Granite's own diagnosis function.

### 9.16.1 R17 — Repair Agent: closing a real gap the plan doc's own text had already implied

**What it is, and why it's distinct from R13/Verified Automatic Repair.** This is a genuinely new foundational feature, not a rename or a restatement of anything already tracked. Verified Automatic Repair (R13, closed by spike 5) covers the *verify/re-execute* half of repair — given a candidate corrected value, deterministically re-run the downstream trace and check whether it now succeeds. Repair Agent is the *other* half — the step that actually *generates* the candidate correction in the first place. Before this entry, nothing in the prior sixteen-item feature list actually produced that candidate value at all.

**How the gap was confirmed, not just asserted.** The register points to the plan doc's own functional requirement FR4 (§0.07) as direct textual proof the gap was real, not invented to justify padding the feature list: FR4 literally reads "given a candidate corrected value for a specific step..." — meaning the requirement as originally written simply assumed a candidate fix already existed, with nothing upstream ever specified as the source of that value. Independent, external evidence for the novelty of adding this is drawn from the market survey's own feature matrix, which rates "Automatically generate repair" as Not native / Custom / Experimental across *all seven* surveyed frameworks — meaning no major orchestration framework ships automatic repair generation as a first-class capability.

**Evidence.** A POC was run same-day, spike 8 (`poc_spike8_repair_agent.py`), on the local 3B model, using six synthetic single-step correction cases chained directly into spike 5's existing replay logic (so the test isn't just "did the model produce plausible-looking text," it's "does the generated fix, when actually replayed through the pipeline, produce a recovered outcome"). Result: `repair_success_rate = 0.667` (4 of 6 cases succeeded), `exact_match_rate = 0.667` (the same 4 cases), and zero parse failures.

**A genuinely useful diagnostic finding buried in the two failures.** The register doesn't just report the aggregate success rate — it digs into *why* the two failures failed, and finds they share one precise, common root cause rather than being two unrelated problems. Given evidence like "15% loyalty discount" or "7 notebooks," the model correctly extracted the right underlying fact in both failing cases — it wasn't confused about what the correct answer conceptually was. But it returned the *downstream computed result* ($6.75, $28.00 — numbers derived by applying the fact to the rest of the calculation) instead of the *specific corrected parameter* the pipeline actually needed (15, 7 — the raw atomic values themselves). The register frames this precisely: "a specification/interface ambiguity in what 'corrected_value' should mean, not a reasoning failure." This is a genuinely actionable finding for the real build, not just a pass/fail number — it tells the team exactly what to fix (pin down the interface contract for what "corrected_value" means, matching how Error Step Localization already pins down a specific step index rather than leaving ambiguity about what's being localized) rather than leaving them to guess why roughly a third of cases failed.

**Status.** "Partially closed — mechanism proven to work more often than not on a free local model, with a precise, actionable finding for the real build." Full output preserved at `poc_spike8_output.json`.

**Why chaining spike 8 into spike 5's existing replay logic, rather than just scoring the raw text output, was the right test design.** A weaker version of this spike could have simply asked the model to produce a corrected value and then string-compared it against a known-correct answer — an "exact match" style evaluation. The register does report `exact_match_rate` (0.667, identical to the success rate here), but the more meaningful number is `repair_success_rate`, computed by actually feeding the generated fix back through spike 5's already-validated mechanical replay pipeline and checking whether the *downstream trace* recovers to the correct final outcome. This matters because a fix could plausibly be textually wrong yet still functionally correct (e.g., a differently-formatted but equivalent value), or textually close yet functionally broken (a near-miss that still corrupts downstream computation) — measuring recovery through the actual pipeline, rather than string similarity to a reference answer, is the test that actually reflects what matters to a real user: does the system's own repair, applied for real, fix the task. In this case the two numbers happened to coincide exactly (both 0.667, same 4 cases), but that's a finding worth stating explicitly rather than assuming — the design choice to test via the pipeline, not via string match, is what makes that coincidence a meaningful confirmation rather than an artifact of only checking one weak proxy.

**Connecting this finding forward to the Mid-1 deadline.** The supervisor PDF's own "What Remains Open" list names Repair Agent's two failing cases directly, and frames the needed work precisely: "worth a targeted prompt fix and re-test before Mid-1, not a re-run from scratch." This phrasing matters — because the root cause of both failures has already been diagnosed precisely (an interface ambiguity about what "corrected_value" means, not a reasoning failure), the fix is scoped and bounded rather than open-ended. This is a genuinely different, more tractable situation than Verified Repair Memory's total failure (R18/R22), where the root cause is still only hypothesized (backbone strength) rather than pinned down with the same precision.

### 9.16.2 R18 — Verified Repair Memory: a previously-unlogged failure, finally recorded

This is one of the more unusual and instructive entries in the whole register, because it's not really about a new risk at all — it's about a *documentation failure* that had already happened and gone unnoticed until this entry corrected it.

**What it is.** The market survey's own recommended module list independently includes a "Verified Repair Memory" step — the idea of storing successful diagnosis-and-repair patterns so similar future failures can be resolved faster or more reliably by drawing on prior verified fixes. The register is explicit that this "is **not new**" as a concept within the project — it is exactly the "Verified Episodic Memory" mechanism that had already been built and tested once before, on 2026-08-23, as part of a full three-stage pipeline prototype (`poc_spike1b_full_pipeline.py`).

**The documentation failure, described honestly.** That prototype file has since been deleted, at explicit user instruction. The register states plainly: "the file itself is gone, this entry is the only remaining record it was ever built." More strikingly, the register explains *why* there was no earlier record: "This finding was supposed to be logged here at the time; the edit attempt failed silently and was never retried, so until this entry, there was no record anywhere that this had been built, tested, and reverted." In other words — a real POC was run, produced a real result, and the attempt to log that result into the register itself failed silently (presumably some kind of tool or edit failure) and nobody caught that the log entry hadn't actually landed, until this later session went back and reconstructed the record from memory/context and wrote it down properly.

**The actual test result, now on permanent record.** Zero of eight real Who&When test cases ever committed anything to memory at all. All twenty-four hypothesis-verifications across those eight cases came back `NOT_SUPPORTED` on the local 3B model backbone used — meaning the verification mechanism never once found evidence it judged sufficient to commit a diagnosis to memory. On top of that, agent-level accuracy actually *regressed* in that same run, from 75% (the simpler two-stage version, spike 1) down to 50% — adding the memory-and-verification stage made the pipeline's own accuracy worse, not better, at least on this small backbone.

**Status — and how it connects to R22.** "Superseded by R22 below, same day (2026-08-24)." At the moment this entry was originally written, the correct call — given a real, documented failure and no re-test yet — was "not on the frozen feature list, correctly, until a stronger-backbone re-test happens." That caution was overridden hours later, the same day, by an explicit user decision: the feature was re-added and then reclassified straight into the foundational core as item #10. R18 is explicitly kept as "the permanent record of the one real test and its failure," while R22 (below) covers the separate reclassification decision made on top of that same unchanged evidence.

**Why the silently-failed edit attempt is itself worth taking seriously, not dismissing as an incidental accident.** It's worth sitting with the specific failure mode this entry describes for a moment, because it's a genuinely important cautionary tale about process, distinct from the technical content of Verified Repair Memory itself. A real POC was run. A real, informative — if negative — result was produced. The team's intent was to log that result into the risk register, the same as every other spike. The edit attempt to do so failed *silently* (no error was surfaced that anyone caught in the moment) and was never retried, meaning that for some period of time, an entire piece of real evidence existed only in the fact that a script had once run and printed output to a terminal or a now-deleted output file — with zero durable record anywhere in the project's own tracking documents. Had the panel-review-style adversarial self-check (the same kind of pass that caught R10's silent-failure gap) not happened to reconstruct this from context and write it down properly, this evidence would likely have been lost entirely, and the team might have gone into the market-survey review believing Verified Repair Memory was a genuinely untested idea rather than one with a real, already-failed prior attempt. This is a small operational lesson embedded in a risk-register row: a "we logged it" step in a workflow needs its own verification, because a silent failure in the *logging* step is exactly as dangerous, in its own way, as a silent failure in the system Granite itself is trying to build tooling to detect — the parallel is almost too on-the-nose to be coincidental, and the register doesn't shy away from naming it plainly.

### 9.16.3 R19 — Single-framework scope-narrowing advice, considered and rejected

**What it is.** The market survey's own §7 ("Scope Control") gives a piece of general advice for keeping a one-year BS project achievable: build against only one orchestration framework, and it specifically suggests LangGraph (because checkpointing and replay are already available natively in that framework).

**Why it was rejected, not just noted.** The register records this as "Considered and explicitly rejected, 2026-08-24," with a clear reason: following this advice would eliminate RQ2 — cross-architecture generalization across CrewAI, LangGraph, and a third framework — which is one of Granite's *two lead research questions*, already CCP-justified in the plan doc and already partially tested via spike 2's CrewAI instrumentation work. The register is careful to give the survey's advice its due even while rejecting it: "Good general advice for a differently-scoped project; incompatible with this one's already-committed novelty case." This isn't a dismissal of the survey's judgment in general — it's a recognition that generic scope-control advice, sound as it may be for many projects, doesn't fit a project whose entire novelty claim is specifically built around cross-architecture generalization.

**Status — and the positive resolution, not just a bare no.** "Closed — rejection on record, not silently ignored. Resolved positively, not just rejected: extension #8, Framework Compatibility Layer (see R20), draws from all 7 surveyed frameworks via lightweight compatibility checks while keeping full benchmarked rigor on only the 2–3 core frameworks." This is worth emphasizing: the team didn't just reject the advice and move on — they engineered a specific, scoped answer to the underlying legitimate concern (breadth risk) that preserves the cross-architecture claim while still respecting the spirit of "don't try to do everything with equal depth."

---

## 9.17 The third addendum: Framework Compatibility Layer, 2026-08-24 (R20)

**What it is.** R20 records the addition of Framework Compatibility Layer as extension #8 — described in the register as "the resolved answer to 'use features of all products, not only from one.'" It draws capabilities and evidence from all seven surveyed orchestration frameworks, rather than being narrowed to a single one as the market survey's own §7 recommends (a recommendation already explicitly rejected via R19 above).

**The deliberate distinction from the core benchmark — this is the key design decision.** The committed core's two-to-three frameworks (CrewAI, LangGraph, plus one more via extension #2) get *full* fault-injection and benchmarked evaluation — the real, rigorous cross-architecture generalization work the project's novelty claim rests on. Framework Compatibility Layer, by contrast, is deliberately *lighter*: it confirms only that the diagnosis pipeline can instrument and parse execution traces from each of the remaining frameworks, without building a full fault-injection benchmark for every single one. The register's own phrase for this distinction is crisp and worth quoting directly: "Broad *compatibility*, not broad *benchmarking*." This design choice directly addresses R8's breadth-over-depth risk — building full benchmarks on all seven frameworks would roughly double the core's engineering workload for a one-year BS project, which is exactly the kind of extension-creep R8 exists to guard against.

**Status.** "Open — gated behind the core, same as every other extension. Nothing to verify yet; revisit once the core build reaches extension work." No POC has been run for this yet — the register is explicit that this is purely a scope decision at this stage, not a tested mechanism, and total frozen feature count moves from 17 to 18 (8 foundational + 8 extensions + 2 deprioritized) as a result of adding it.

---

## 9.18 The fourth addendum: Recovery Controller and Verified Repair Memory reclassified, 2026-08-24 (R21, R22)

This is the register's most recent major addendum, and it records something unusual: two items that had existed as extensions for only a few hours, within the same working session, were then moved into the foundational core — a genuine same-day reversal, made deliberately and recorded as such rather than quietly.

**Why the reclassification happened.** The market survey's own Table 1 rates eight capability rows as "Core" for the "Proposed FYP" column: Detect semantic wrong answer, Find culprit agent, Find originating error step, Causal backward error tracing, Automatically generate repair, Verify repair before applying, Resume from repaired point, and Remember successful repairs. Granite already treated the first six of these as foundational. The last two — "Resume from repaired point" and "Remember successful repairs" — are exactly Recovery Controller and Verified Repair Memory, which had initially been added as extensions #9–10 earlier the same session. The register frames the inconsistency plainly: "Leaving these two as extensions was inconsistent with the survey's own classification it otherwise relies on throughout." Rather than let that inconsistency stand, the team moved both into the foundational core to match.

### 9.18.1 R21 — Recovery Controller: genuinely new mechanical work, zero POC evidence

**What it is.** Recovery Controller applies a verified repair and resumes execution from a safe checkpoint, rather than restarting the entire workflow from the beginning. This formally resolves an item — "Checkpointing" — that had sat in a "considered, not added" limbo since 2026-08-23 (see the plan doc's own record of items considered and explicitly not added).

**Why it's genuinely distinct from Verified Automatic Repair, and not just a rename.** Verified Automatic Repair (R13, spike 5) already does deterministic re-execution — but the register is precise about what that means: spike 5's toy pipeline re-executes downstream steps from scratch after a correction, it does not save and restore real checkpoint-based execution *state*. Recovery Controller needs actual checkpoint-based state saving and restoring — a genuinely different, additional mechanical capability that nothing else in the frozen feature list currently provides.

**Evidence gathered so far, and its limits.** A precedent check (not a POC — a check of what already exists in the surveyed frameworks) found that five of the seven surveyed frameworks have generic checkpoint/resume infrastructure: LangGraph, CrewAI, and Microsoft Agent Framework are checkpoint-based; Google ADK and Amazon AgentCore offer partial support. But the register is explicit about what this precedent check does *not* establish: "none tie resumption specifically to a verified-repair point, which is what this item needs" — meaning the generic checkpoint infrastructure that exists in the wild doesn't solve Granite's specific problem (resuming *from a point where a repair has just been verified*), it just confirms the general mechanical primitive (checkpoint/resume) is a well-established pattern that Granite can build on rather than invent from scratch.

**Status.** "Open — foundational item with zero POC evidence. Genuinely new mechanical work, not a rename of anything already tested; the clear gap to close before Mid-1, alongside R22's VRM re-test below." This is one of the two clearest, most concrete pieces of unstarted foundational work still owed by the project (the other being Verified Repair Memory's re-test, R22).

**Why Recovery Controller is a lower-risk unknown than Verified Repair Memory, even though both have zero-and-one POC evidence respectively.** It's worth explicitly contrasting these two same-day reclassifications, because they carry meaningfully different risk profiles despite sitting side by side in the register. Verified Repair Memory has *negative* evidence — a real attempt was made and it failed completely. Recovery Controller has *no* evidence at all — nobody has tried it yet, positive or negative. The precedent check (five of seven surveyed frameworks already having generic checkpoint/resume infrastructure) is a genuinely favorable signal for Recovery Controller that Verified Repair Memory doesn't have an equivalent of: Recovery Controller is being built on top of a well-established engineering pattern that multiple mature frameworks already implement in some form, whereas Verified Repair Memory's core mechanism (an LLM judging whether evidence sufficiently supports committing a hypothesis to memory) is closer to Granite's own novel territory, with no external precedent of "this pattern reliably works" to lean on. This doesn't make Recovery Controller's zero-POC status any less of a real gap — the register is explicit it is "the clear gap to close before Mid-1" — but it's a different *kind* of open risk: an unstarted-but-plausible piece of engineering, versus a started-and-failed piece of research.

### 9.18.2 R22 — Verified Repair Memory's reclassification: honesty preserved even as status changes

**What it is.** This entry records the reclassification decision itself, layered on top of R18's already-recorded evidence — R22 explicitly states "the reclassification is a scope decision, not new evidence — the evidence stays exactly what R18 recorded." Verified Repair Memory is re-added and moved into the foundational core as item #10, overriding R18's earlier "not on the frozen list" call, by explicit user decision, the same day.

**The evidence, restated for emphasis, because it does not improve just because the status changed.** Zero of eight real Who&When cases ever committed anything to memory. All twenty-four hypothesis-verifications came back `NOT_SUPPORTED` on the local 3B backbone. Agent accuracy regressed 75% to 50% in that same run. Nothing about this evidence has been re-tested or improved as of the reclassification — the register is explicit: "nothing has been re-tested yet."

**Status, and the discipline embedded in it.** "Open — committed to the foundational core on the explicit condition that a re-test on a stronger LLM backbone happens before Mid-1. If the re-test also fails, this is a foundational-item gap the team must be ready to explain under questioning (Section 14.1), not a footnote — the one real test result stays on record as a failure, not softened just because the item is core now." This last clause is the register's clearest statement of its own governing principle: promoting something to "foundational" status is a scope decision about ambition, not a decision that retroactively improves the evidence behind it. The team committed to defending a feature that, as of the writing of this register, has one real test on record, and that test failed. That's an unusually honest posture to build into a project's own core documentation, and it's worth naming explicitly as the standard the rest of this register (and this document) tries to hold itself to.

---

## 9.19 The appendix: full market survey evidence backing R17–R20

The register closes with a verbatim-reproduced appendix from `Agentic_AI_Market_Survey_BS_FYP.docx`, included so the register is self-contained rather than requiring a reader to jump elsewhere to verify the claims made in R17 through R20.

**Table 1** lists eight capabilities the survey rates "Core" for the "Proposed FYP" column, and — this is the striking part — every single one of the seven surveyed frameworks (OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI) rates as "Not native" for at least the middle four of these eight rows: Find culprit agent, Find originating error step, Causal backward error tracing, and Automatically generate repair are unanimously "Not native" across every framework checked. This is the concrete, independent evidence underlying Granite's core novelty claim — it isn't Granite's own assessment of the market, it's a third-party survey's structured comparison, reproduced verbatim so the claim can be checked against its actual source rather than taken on trust.

**Table 2** describes five layers of agentic error handling and locates the project's gap precisely: Layer 1 (runtime handling — did a tool/API/node fail) and Layer 2 (workflow recovery — can execution retry/resume) are both rated "Mostly mature," well-served by existing agent SDKs. Layer 3 (semantic diagnosis — which agent introduced the wrong reasoning and where) is rated "Still under-served," with ErrorProbe and research prototypes as the only strong existing work. Layer 4 (targeted repair — can the responsible component be corrected automatically) is rated a "Major gap," served only by custom logic and experimental self-building approaches. Layer 5 (verified self-healing — can the fix be tested, replayed, and remembered safely) is rated a "Strong FYP opportunity," served only partially and by custom logic across frameworks. Granite's own foundational feature list maps almost exactly onto Layers 3 through 5 — this table is, in effect, an independent confirmation that the project's chosen scope sits precisely where the survey itself identifies the field's real gap to be.

---

## 9.20 Two full worked traces — watching a risk actually move through the register's process

Reading the register table by table shows *what* each entry says. It's worth also watching, end to end, *how* a single piece of real evidence travels from "something happened during a working session" to "a dated, numbered entry with a status" to "a decision that reshapes the frozen feature list or the build schedule." The register and the AI Usage Log are two views of the same underlying events, cross-referenced by date, and reading them together makes the mechanics of the process visible in a way that reading either document alone does not. Two traces are worked through in full below, chosen because they show two different outcomes of the same basic process — one where the discovered gap gets closed the same day it's found, and one where the discovered gap takes multiple sessions, a lost log entry, and a same-day reversal before it settles into its current, still-open status.

### 9.20.1 Trace one — Verified Repair Memory: from a deleted prototype to a foundational item with a known failure attached

**Setup.** Verified Repair Memory is the market survey's own name (Table 1, "Remember successful repairs") for a capability Granite had already built and tested once under a different name — "Verified Episodic Memory," the memory-and-verification component of ErrorProbe's real 3-stage pipeline. The idea is straightforward to state and hard to get right: after a diagnosis is verified, commit it to memory so a similar future failure can be resolved faster by drawing on the prior, already-verified case, rather than reasoning about every new failure from a cold start.

**What actually happened, in date order.** On 2026-08-23, a full 3-stage pipeline prototype (`poc_spike1b_full_pipeline.py`) was built and run against all 8 real Who&When cases already in hand from spike 1. The result was unambiguous and negative: zero of the eight cases ever committed anything to memory. All 24 hypothesis-verifications the pipeline attempted across those 8 cases came back `NOT_SUPPORTED` — meaning the verification stage never once judged the evidence sufficient to commit a diagnosis. Worse, agent-level accuracy itself regressed in that same run, from spike 1's 75% down to 50%, meaning the extra memory-and-verification machinery made the simpler pipeline's own accuracy worse on this small local model, not better.

**The logging failure — a real gap in the process itself.** The intent, at the time, was to log this result into `risk-register.md` immediately, the same as every other spike. The edit attempt failed silently, and nobody caught it. The prototype file was later deleted at explicit user instruction. For a period spanning from 2026-08-23 to 2026-08-24, there was no durable record anywhere in the project's own tracking documents that this test had ever been run — the only trace of it was in a terminal's scrollback and a person's memory of having run it. This is worth sitting with as its own finding, distinct from the memory mechanism's own failure: a "we logged it" step failed the exact same way a silent agent failure fails — a real thing happened, and nothing downstream noticed that the record of it never landed.

**Recovery.** During the sixth AI-assisted session, 2026-08-24 — while reviewing the market survey and finding its own independent "Remember successful repairs" recommendation — the team recognized that this recommendation described something already attempted and already failed. The result was reconstructed from context and written into the register properly for the first time, as R18. At that point, the correct, honest call was made explicitly: "not on the frozen feature list, correctly, until a stronger-backbone re-test happens." A real failure does not get quietly folded into the committed list just because a market survey happens to recommend the same idea.

**The reversal, hours later, same day.** Later in that same working session (recorded as the ninth session, still 2026-08-24), a closer read of the market survey's own Table 1 showed all eight of its "Core" rows treated identically for the Proposed FYP column — Granite already treated six of those eight as foundational, and leaving "Remember successful repairs" and "Resume from repaired point" as mere extensions was inconsistent with the survey's own classification the project otherwise relied on throughout. The team made an explicit decision to reclassify Verified Repair Memory into the foundational core as item #10 — on one binding condition, stated directly in the register: "a re-test on a stronger LLM backbone happens before Mid-1," and if that re-test also fails, "this is a foundational-item gap the team must be ready to explain under questioning... not a footnote."

**Why this matters as a governance example, not just a feature-list history.** The evidence itself never changed across this whole sequence — zero of eight, 24 `NOT_SUPPORTED`, 75%→50% regression, stated identically in R18 and again in R22. What changed was the scope decision layered on top of that unchanged evidence, and the register's discipline is visible precisely in refusing to let the scope decision quietly improve the evidence's presentation. A reader coming to R22 today sees a foundational item, but the register does not let that foundational label imply the mechanism has been shown to work — it explicitly preserves the one real test's failure right there in the same entry, with a named, dated condition for closing the gap. This is the concrete mechanics behind the abstract claim, made elsewhere in this document, that "promoting something to foundational status is a scope decision about ambition, not a decision that retroactively improves the evidence behind it."

### 9.20.2 Trace two — the silent-failure detector: a gap caught by the team turning adversarial on its own work

**Setup.** Silent-failure detection is RQ3, one of Granite's two headline research questions. Unlike Verified Repair Memory, this trace is not about a mechanism that was tried and failed — it's about a mechanism that had never been tried at all, and how that fact came to light.

**What actually happened.** By the point the first AI-assisted session had already run three POC spikes — ErrorProbe reproduction (spike 1), CrewAI instrumentation (spike 2), and fault injection (spike 3, run twice) — the project's documentation described silent-failure detection as one of its two core novelty pillars, with real prose written about what it would do. No code had ever tested it. This was not caught by a scheduled checklist item or an external reviewer; it was caught by the team deliberately turning an adversarial, panel-style review pass on its own documentation, specifically looking for exactly the kind of gap a real panel would be most likely to find. The AI Usage Log records the pass finding two such gaps in the same sweep: the untested silent-failure mechanism, and the total absence of a written defense against the "you just combined existing techniques" objection (despite a comparable project in the same workspace having exactly that section already).

**The response — same session, not deferred.** Rather than logging the gap and scheduling it for a later sprint, the team closed it within the same session: spike 4 (`poc_spike4_silent_failure_detector.py`) was written and run immediately, producing the two-part result described in full in section 9.10 above — a real n=3 LLM run that happened to produce zero natural failures to detect, and a direct mechanism test against known-wrong values (including the deliberately hard $20.00-vs-$19.75 near-miss) that fired correctly with zero false positives. The register's own record of this, R10, is explicit that this is "real, honest first data point; not proof the detector catches failures 'in the wild' yet" — the gap was closed with real code and a real result, but the register does not let closing the documentation gap be mistaken for closing the underlying uncertainty about how often the mechanism will actually be exercised by real, naturally-occurring failures.

**Why this trace matters alongside the first one.** Put side by side, these two traces show the register handling two different kinds of discovery in a consistent way. Trace one is a mechanism that was tested and failed, whose evidence survives unmodified across a same-day reclassification. Trace two is a mechanism that had never been tested at all, caught by the team's own adversarial self-review and closed with real code inside the same working session, with the resulting evidence's real limits (n=3, zero natural failures) stated plainly rather than oversold. In both cases, the same underlying discipline is visible: a real gap, once found, gets a dated record, real evidence attached to it as soon as it's practical to produce, and an honest statement of exactly how much that evidence does and does not prove — never a status upgrade that quietly implies more certainty than the evidence supports.

---

# PART 10 — TIMELINE AND GOVERNANCE

## 10.0 A summary table of the five gates before the full walkthrough

| Gate | Guide's own name | What the plan doc schedules there | Evidentiary bar per the guide |
|---|---|---|---|
| 1 | Proposal defense | CCP rating, contribution statement, delta argument, AI-resilience defense, component classification, scope split, evaluation plan, a POC "demonstrated with evidence" | Scope approved by supervisor (D2) |
| 2/3 | Mid-1 | Stakeholder-informed requirements, SRS/SDS baselined, data/licensing cleared, riskiest subsystem (full ErrorProbe reproduction) prototyped on a stronger backbone | Requirements + design baseline |
| 3 | Final-1 | Core build across all three tracks; integration path proven end-to-end | Working core system — the exit gate |
| 4 | Mid-2 | Full integration, benchmark scaled to 500–1,000 traces, full evaluation run, non-functional testing incl. R16 becoming a tested behavior | Release readiness |
| 5 | Final-2 | User acceptance testing, SDK/dashboard polish, full documentation set, final packaging | Deployed system + project report |

## 10.1 The five-gate structure, and what each gate actually requires

Granite's two-semester plan (plan doc §12) is built around five gates, matching the FAST guide's own structure: **Proposal defense** (Gate 1), **Mid-1** (Gate 2/3, combined in the plan doc's own timeline block as "requirements + design baseline"), **Final-1** (Gate 3, "working core system, exit gate"), **Mid-2** (Gate 4, "release readiness"), and **Final-2** (Gate 5, "deployed system + project report"). Each gate carries specific, named requirements the guide expects to be demonstrated at that point, not merely promised.

**Gate 1 — Proposal defense.** This is where the entire proposal-stage apparatus this document has already covered gets presented and defended: the CCP rating, the contribution statement, the delta-from-ErrorProbe argument, the AI-resilience-test defense, the external-component classification, the committed-core-vs-extensions scope split, the evaluation plan, and — critically, per §12's own requirement — a proposal-stage POC "demonstrated with evidence... not promised as future work." Granite's own §16 self-check against the guide's readiness checklist shows this gate substantially prepared: problem/users/gap/contribution statable in one minute, CCP characteristics justified (8 of 9 clear), a meaningful contribution independent of raw algorithmic novelty, a genuinely evidenced POC (exceeding the guide's own one-spike minimum by running seven, later eight, spikes), baseline/success-criteria/evaluation/failure-cases all defined, every external component classified with a committed API-usage budget, committed scope cleanly separated from optional extensions, a deployment target stated, an AI usage log maintained and current, a one-page architecture sketch, an opened RAID register, SDG alignment stated, a client identified, the idea specified with five functional requirements and one measurable non-functional requirement, a research-to-decision table, and an assembled defense package. Three items on that same checklist remain explicitly unchecked going into the gate: real stakeholders contacted, team ownership roles assigned to actual people, and a prior-departmental-FYP comparison — all three of which reappear as the leading items in Part 11 below.

**Gate 2/3 — Mid-1.** The plan doc frames Weeks 6–10 as covering "Stakeholder-informed requirements, SRS/SDS baselined, data/licensing cleared, riskiest subsystem prototyped." Crucially, the plan doc names a *specific, evidence-driven* top priority for this window, not a generic "keep working" instruction: "Top priority, per spike 1's own result (12.5% step accuracy, simplified pipeline, n=8, local 3B model): build the full 3-stage ErrorProbe reproduction (tool-grounded Investigator + Verified Episodic Memory) on a stronger backbone — the simplified version is nowhere near 59.5% and a fair baseline comparison depends on closing that gap, not just noting it." This is a direct, causal link from a specific piece of POC evidence (R1's spike 1 result) to a specific scheduling decision — the timeline isn't an arbitrary sequence of generic development phases, it's sequenced in direct response to what the proposal-stage evidence actually showed was the biggest remaining unknown.

This is also exactly why the register's repeated instruction that Verified Repair Memory's stronger-backbone re-test (R22) and Repair Agent's targeted interface fix (R17) both need to happen "before Mid-1" makes structural sense: Mid-1 is explicitly the gate where the riskiest subsystem gets prototyped and the requirements/design baseline gets set, so any foundational item still carrying an honest open failure (Verified Repair Memory) or a known, precisely-diagnosed partial failure (Repair Agent's two cases) needs to be resolved or re-tested before the team commits a design baseline around it. Committing a design baseline that assumes a mechanism works, when the mechanism's only real test on record actually failed, would be exactly the kind of overclaim the project's whole discipline is built to avoid.

**Gate 3 — Final-1.** Weeks 10–18 build out the actual core system across all three ownership tracks in parallel (detailed in 10.2 below), closing with "Integration path proven end-to-end against approved design." This is named explicitly as the "exit gate" — the point at which a working core system, not just individually-working components, needs to be demonstrated.

**Gate 4 — Mid-2.** FYP-2's Weeks 1–8 cover full integration (harness through diagnosis engine through counterfactual engine through dashboard — "product build, not just data work"), scaling the new benchmark up to the target 500–1,000 traces, running the full evaluation against the ErrorProbe baseline on both the original and the new cross-architecture benchmark, and non-functional testing: latency overhead measured, failure/recovery paths demonstrated, deployment tested *outside* the dev machine, and — notably — "trace-data privacy handling verified (R16 threat model becomes a tested behavior, not just a written paragraph)." This last point is an important piece of governance discipline worth calling out explicitly: R16's security/privacy threat model was written and logged as "resolved" at the proposal stage, but the plan doc itself is careful not to let that resolved status be mistaken for "done" — it schedules a specific point later in the timeline where the paragraph gets converted into an actually-tested behavior, closing the loop between documentation and verification rather than treating the written threat model as the final word.

**Gate 5 — Final-2.** FYP-2's Weeks 8–16 cover user acceptance testing with real or proxy users, SDK polish, dashboard build-out, and finally, in Weeks 14–16, the completed documentation set (SRS, SDS, traceability matrix, test/deployment/handover plan) and final packaging. This is the last gate, where "deployed system + project report" is the deliverable — and per §13 of the plan doc, this is explicitly the first point at which *real deployment evidence* (not a screenshot of a local build, which the guide's own §1.2 explicitly warns against accepting as deployment evidence) becomes an honest, producible claim, since at proposal stage the deployment target is stated and justified but nothing is actually deployed yet.

### 10.1.1 Why the guide's own "evidence at each gate" framing matters more than the calendar dates

It's worth being explicit about a distinction that runs through this whole gate structure: the guide does not merely ask a team to reach a certain calendar week and present whatever exists at that point — it names, per gate, the specific *kind* of evidence expected to exist, and treats a gate passed without that evidence as not really passed at all, regardless of how much other work happened in the meantime. This is precisely why the plan doc's §13 flags "evidence of deployment" as explicitly unavailable at proposal stage, rather than glossing over the gap or fabricating a placeholder screenshot — the guide's own warning ("a screenshot of a local build is not deployment evidence") is quoted directly in the plan doc itself, which means the team has internalized the distinction between *having built something* and *having deployed and evidenced it*, and is applying that distinction to its own honest self-assessment rather than only to how it might critique someone else's project.

This same principle explains why R16's threat model, written and "resolved" at proposal stage, is explicitly scheduled to become "a tested behavior, not just a written paragraph" specifically at Mid-2 (Gate 4) rather than being left as a permanently-resolved risk the moment the paragraph was written. A written threat model is real, useful evidence of *analysis* — it is not evidence that the redaction, namespacing, and retention mechanisms actually work as designed when exercised against real trace data. The gate structure is what converts "we have thought about this carefully" into "we have built and tested this," on a schedule, rather than leaving that conversion implicit or optional.

### 10.1.2 The gate structure as a forcing function against silent scope drift

There's a second function the five-gate structure serves beyond pacing: each gate is a scheduled checkpoint where the team is required to present real evidence to an external evaluator (the supervisor, and eventually a panel), which creates a natural, recurring pressure against exactly the kind of silent, undocumented scope drift the register's own change-control discipline (guide §5.3) is designed to catch. A team that only checked in with itself, informally, would have many more opportunities to let an assumption quietly go unverified, a risk quietly go unmitigated, or a claim quietly get overstated without anyone outside the team noticing. The gate structure forces those things into the open on a predictable cadence — this is arguably why the plan doc's own §15 standing instruction ("re-check the literature at each of the 5 gates") is anchored specifically to the gate structure rather than to an arbitrary calendar interval: the gates are already the moments the team is forced to present its current understanding to someone else, so tying recurring verification work to those same moments means it never gets an opportunity to be quietly skipped.

## 10.2 Why extensions are back-loaded, and why the specific fixes named above sit where they sit

Looking across the whole timeline, a clear pattern emerges: the committed foundational core is front-loaded (Weeks 1 through roughly Week 18 of FYP-1, plus the first six weeks of FYP-2 for scaling and full evaluation), and extension work is deliberately back-loaded into the second half of FYP-2 (Weeks 6 through 14), with an explicit governing rule that extensions are "gated on the core being complete first" (R8's own mitigation). This isn't accidental sequencing — it's the direct structural answer to R8's breadth-over-depth risk. A team that let extension work creep forward into the same weeks as core-build work would be exactly the failure mode R8 exists to prevent.

Within the extension slots themselves, the sequencing carries its own logic worth calling out. Extension #1 (widen fault taxonomy) and extension #2 (third architecture) are scheduled for the very start of FYP-2 (Weeks 1–6), alongside extension #3 (cyclic graph support) — these three are scheduled early precisely because they extend the *core* generalization and benchmark claims that the whole evaluation run depends on, so they need to land before the full evaluation run happens later in that same block. Extension #4 (confidence calibration) sits in Weeks 6–8, aligned with the non-functional testing phase where a calibration curve is a natural thing to produce alongside latency measurement. Extension #5 (the preventive clarification classifier) is explicitly marked "contingent, not automatic" in the plan doc's own text for Weeks 8–14 — a direct, honest consequence of spike 7's near-random result (R15): rather than blindly scheduling build time for a feature with a demonstrated weak signal, the plan requires a re-test with better data (harness-generated, not hand-written) and better features (cheap sentence embeddings) first, and states plainly: "if it still doesn't improve, drop it rather than ship a known-broken classifier." This is the timeline itself enforcing the register's own honesty discipline — a weak result doesn't just get quietly built anyway because it was already scheduled.

## 10.3 The three parallel tracks and how they interleave

Three ownership tracks run in parallel across the build phase (Weeks 10–16 of FYP-1, and continuing through FYP-2): **Data/Benchmark Owner** (multi-framework instrumentation across CrewAI and LangGraph, injection operators, the ground-truth benchmark itself, and eventually licensing/release packaging), **Diagnosis Engine Owner** (execution-graph construction, the ErrorProbe reproduction, the silent-failure constraint-verification module, causal tracing), and **Platform Owner** (the counterfactual/repair engine, the SDK, backend API, containerized deployment, and dashboard).

These tracks are not independent silos — the plan doc's own scope-sufficiency framing (checked in the Guide Compliance Audit against §5's "interdependent work" principle) is explicit that "pipeline hops are sequential/dependent," meaning each stage's output is the next stage's input: the Data/Benchmark track's traces feed the Diagnosis track's attribution work, and the Diagnosis track's verified diagnoses feed the Platform track's repair-and-replay engine. This interdependence is precisely why the "if removed, what disappears" test in §9 of the plan doc works cleanly for each role — removing Data/Benchmark Owner means no cross-architecture evaluation is possible at all (nothing downstream has real data to work with); removing Diagnosis Engine Owner means the core attribution algorithm and the silent-failure detection claim both disappear (nothing to feed Platform's repair engine); removing Platform Owner means "the product itself" disappears — nothing would be installable or operable outside the dev machine, even if the underlying diagnosis logic worked perfectly in isolation.

The interleaving becomes visible directly in the Weeks 10–16 core-build block, where all three tracks run genuinely concurrently rather than sequentially — this is only possible because each spike run at the proposal stage already validated, independently, that each track's core mechanism works in isolation (spike 2 for Data/Benchmark's instrumentation approach, spikes 1/4/8 for Diagnosis's core mechanisms, spike 5 for Platform's replay logic), meaning the three tracks can be built in parallel with reasonable confidence that they'll integrate cleanly at the "integration path proven end-to-end" checkpoint that closes out Final-1, rather than each track discovering foundational problems only once integration is attempted.

### 10.3.1 What each track hands the next, concretely

It's worth making the pipeline dependency between the three tracks fully concrete, because it's what makes the "meaningful primary ownership" test (guide §5) genuinely pass rather than merely appear to pass on paper. Data/Benchmark Owner's output is a set of real execution traces with attached ground-truth labels — which agent, which step, and what kind of fault was injected — produced by instrumenting CrewAI and LangGraph workflows and running the fault-injection harness against them. That output is exactly the input Diagnosis Engine Owner's pipeline consumes: a trace goes in, and a predicted responsible agent, step, confidence score, and (where relevant) a silent-failure flag comes out, which can then be scored against the ground-truth labels Data/Benchmark produced. Diagnosis Engine Owner's output — specifically, a verified diagnosis with a localized step and a hypothesis about what the correct value should have been — is in turn exactly what Platform Owner's Repair Agent and Verified Automatic Repair components consume: given a diagnosis, generate a candidate fix, replay it deterministically, and report whether the trace now succeeds, then package the whole result as something a real SDK user sees in a dashboard or gets back from an API call.

This chain is precisely why the guide's own "if removed, what disappears" test produces such clean, distinct answers for each role (as already covered in 10.3 above) — each role's deliverable is a genuinely necessary input to the next stage, not a parallel, independent piece of work that happens to share a project name. A team that built three genuinely independent modules that merely got bundled together under one umbrella project would fail the guide's own "shared central problem" and "interdependent work" scope principles (§5) — Granite's pipeline structure is what keeps those principles honestly satisfied rather than just asserted.

### 10.3.2 Why concurrent building is a reasonable bet, not a reckless one

It's worth being explicit about why building all three tracks in parallel, rather than strictly sequentially (finish Data/Benchmark fully, then start Diagnosis, then start Platform), is a defensible plan rather than an invitation to integration disaster. The proposal-stage POC work already de-risked exactly the interfaces that would otherwise make parallel building dangerous: spike 2 already proved CrewAI traces can be represented in the graph data model Diagnosis Engine Owner's work depends on; spike 1 already proved the diagnosis pipeline can consume real Who&When-format traces and produce sensible output; spike 5 already proved a corrected value, once available, can be mechanically replayed through a trace to check recovery. Because each of these interface-level questions already has real evidence behind it before the parallel build phase even starts, the risk that the three tracks would discover, only at integration time, that their outputs and inputs don't actually fit together is meaningfully reduced — not eliminated, but reduced from "essentially unknown" to "probably fine, with specific named details (the Repair Agent interface-ambiguity finding from R17, for instance) already flagged as needing attention before they'd otherwise cause an integration surprise."

## 10.4 AI usage disclosure: why every session is logged, and what "CCP-relevant" actually means here

### 10.4.1 The stated purpose, in the log's own words

The AI Usage Log opens with a direct framing borrowed from the FAST guide's own language (§8.2): "disclosure is not a penalty. What matters at defense is whether the team can explain, justify, modify, and defend anything CCP-relevant that AI assistance touched — not whether AI was used." This framing matters because it sets the actual bar the log is trying to clear — the log's function isn't to minimize the appearance of AI involvement, or to prove AI wasn't used much; it's to make every piece of AI-assisted work traceable enough that the team can be asked "why is this true, why did you choose this, what would you change" about any of it and have a real, owned answer, not a recitation of something an AI produced that they never actually verified themselves.

This is reflected structurally in every single entry in the log: nearly every row carries a "Verified how" or "Verification status" column, and a large fraction of entries explicitly state something the *team itself* still needs to do — re-read a source paper, re-run a script, spot-check a claim against a live source — rather than treating the AI's own account of its work as sufficient on its own.

### 10.4.2 What makes an entry "CCP-relevant" versus peripheral

The log explicitly distinguishes CCP-relevant work from peripheral work, and this distinction determines how much verification burden each entry carries. CCP-relevant work is anything that touches the actual substance of the complex-computing-problem claim — the core attribution algorithm, the silent-failure detection mechanism, the benchmark's ground-truth labeling, the contribution statement and CCP rating themselves. Peripheral work is infrastructure and environment setup that doesn't itself constitute intellectual content the team needs to defend — the log names environment setup (Ollama installation, CrewAI setup, disk-space migration from a C: drive to an E: drive) explicitly as "infrastructure work, not CCP-relevant in itself," while still noting the team should understand their own development environment rather than treat it as an opaque black box.

The clearest example of this distinction being applied consistently is the test-generation section: the log states plainly that "no formal unit-test suite generated yet," and that "the four POC scripts function as informal, single-purpose validation runs (matching the guide's own POC framing — a small targeted spike, not production test coverage)," with real test coverage for the diagnosis engine, execution-graph construction, and fault-injection harness explicitly scoped as FYP-1 core-build work, not something to retroactively claim already exists. The log doesn't inflate the POC spikes into something more than what they are.

Every documentation file produced during the AI-assisted sessions is separately rated for CCP-relevance in its own row: `Full_Literature_Landscape_Analysis.md`, `ErrorProbe_Baseline_Selection.md`, `FYP_Scope_CCP_and_Implementation_Plan.md`, and `risk-register.md` are all marked "Yes" — each carries a specific instruction about what the team needs to independently verify before relying on it (licensing claims against actual repositories; the ability to defend the baseline-selection reasoning live, not read off a slide; the CCP rating and contribution statement specifically, as "the two things most likely to be probed directly at defense"). `datasets.md`, `resources.md`, and `architecture-sketch.md` are marked "Partially" — lower-stakes reference material, still worth reading but lower priority. `Supervisor_Briefing.md` is marked "No (summary only)" — explicitly because it's "a plain-language distillation of the above; not a new claim, just a rephrasing," meaning it carries no independent verification burden of its own since it doesn't introduce anything the source documents haven't already been rated for.

### 10.4.3 The policy of never rewriting historical entries — and why it matters

One of the clearest, most consistently applied practices across the log's nine sessions is a deliberate refusal to retroactively edit past entries when something gets renamed, corrected, or reclassified later. Instead, the practice is always: leave the historical entry exactly as originally written, and add a new entry recording the change as its own dated event. This is stated explicitly at least three separate times across the log, in near-identical language each time, which is itself a signal that the team treats this as a considered policy rather than an accident of not bothering to go back and edit old text.

**Example 1 — the feature-renaming session (fifth session, 2026-08-23).** When "core attribution algorithm" was split into its three real component stages (Culprit Agent, Error Step Localization, Verification Agent) and two other features were renamed for clarity (silent-failure verification → Semantic Error Diagnostic; counterfactual replay engine → Verified Automatic Repair), the log states: "This log's own earlier entries (first through fourth sessions, above) intentionally keep the old names as originally written, since they accurately describe what was built and tested at the time under those names — this entry records the rename decision, it does not retroactively correct history." The reasoning given is precise: the old entries are not *wrong*, they are accurate descriptions of what existed and what it was called *at the time they were written*. Rewriting them to use the new names would actually make the historical record less accurate, not more, because it would misrepresent what the team actually knew and called things when the original work happened.

**Example 2 — the TraceCause → Granite rename (seventh session, 2026-08-24).** When the project's short title was formally changed from TraceCause to Granite, propagated via a scripted regex replace across every current-state file, the log records: "This log's own prior entries (first through sixth sessions, above) intentionally keep 'TraceCause' as originally written — same standing practice as the 2026-08-23 feature rename: past entries describe what was actually built and named at the time, this entry records the rename decision, it does not retroactively correct history." This is a near-verbatim restatement of the same policy, applied to an even more fundamental change (the project's own name) — and it's the reason this very document you're reading preserves "TraceCause" whenever it directly quotes or describes what a historical log entry says, while using "Granite" everywhere else.

**Example 3 — the R18/R22 evidence-preservation pattern.** Although this one lives primarily in the risk register rather than the AI usage log itself, it's the same underlying discipline applied to risk-register entries rather than log entries: when Verified Repair Memory was reclassified from "not on the frozen list" (R18's original conclusion) to "foundational item #10" (R22's reclassification), the evidence itself — zero of eight cases committing to memory, all twenty-four verifications coming back `NOT_SUPPORTED`, the 75%-to-50% accuracy regression — was not softened, reworded, or removed. R22 explicitly states "the evidence stays exactly what R18 recorded" and "nothing has been re-tested yet." The register even preserves R18's own now-superseded conclusion ("not on the frozen feature list, correctly, until a stronger-backbone re-test happens") as historical record of what the honest call was *at that time*, rather than deleting it once a later, different decision overrode it.

**Why this policy matters beyond just being tidy record-keeping.** A defense panel, or any reader trying to assess whether the team's process was rigorous, benefits enormously from being able to see the actual sequence of decisions as they really happened — including decisions that were later reversed, corrected, or superseded — rather than a cleaned-up final state that hides how much uncertainty and revision the project actually went through. The AgentRx removal (documented in the log's second session) is another instance of this same instinct: rather than quietly deleting the fact that AgentRx had ever been considered, the log records it as "the same class of correction as the GraphTracer/FALAT reversion above: scope discipline, not a factual error this time, but the same standing instruction — don't let topically-adjacent finds expand scope without being asked." Even a clean removal gets a permanent, dated trace explaining why it happened.

### 10.4.4 The pattern of "propagated for consistency, not yet independently reviewed"

A recurring closing note across nearly every later session in the log is a two-part statement: first, that a change has been "propagated for consistency" across a named list of specific files (the plan doc, the risk register, the Proposal Defense Package, the supervisor PDF, the published artifact, and others), and second, an explicit caveat that this propagation has "not yet independently reviewed by the team." This pairing recurs at the end of the sixth, seventh, eighth, and ninth sessions almost verbatim. It's worth naming as its own governance pattern: the log distinguishes between "the documentation has been made internally consistent" (a mechanical, verifiable task) and "the team has actually sat with, understood, and confirmed they're comfortable defending the new content" (a human verification step that mechanical propagation cannot substitute for). The ninth session's closing note goes further than most, describing a genuinely substantive fix made to the PDF-generation script itself during the propagation pass — the script had been "left in a partially-edited intermediate state with the two items still sitting in the extensions precedent table under a stale... heading pair," requiring the rows to be moved, headings retitled, and precedent-tally numbers recomputed before the PDF could be rebuilt correctly, with tag-balance in the HTML artifact re-checked rather than assumed correct afterward. This is a concrete example of propagation work itself sometimes surfacing its own bugs, which then get fixed and documented in the same entry rather than silently patched.

## 10.5 A session-by-session walkthrough of the AI Usage Log's own nine sessions

The log's structure — nine dated, sequentially appended sessions rather than a single undated summary — is itself part of the governance story, since it's what makes the non-rewriting policy (10.4.3) checkable in the first place. Reading straight through all nine gives a clearer picture than any single excerpt of how much the project's own self-understanding evolved over roughly three calendar days of intensive AI-assisted work, and how consistently each session's real output (a script run, a dataset downloaded, a decision made) is distinguished from the log's own summary of it.

**First session — the foundational work.** Covers the initial ideation comparing the eventual TraceCause direction against two alternative pitches (FinSynth, RedShield) against the guide's own CCP and scope criteria; the seven-paper literature-gap identification that established the core novelty claim; the first four POC scripts (spikes 1 through 4, covering ErrorProbe reproduction, CrewAI instrumentation, fault injection twice, and — added only after the adversarial panel-review pass caught it missing — the silent-failure detector); real debugging work (CrewAI's SQLite storage failing because a C: drive had 0.02 GB free, confirmed by direct disk measurement; Ollama's tray app not passing an environment variable through to its own server process, confirmed by process listing and re-checking `ollama list` output; a step-accuracy scoring bug caused by a string-vs-int type mismatch in the ground-truth data, confirmed by directly printing both fields' types before and after the fix); and the GraphTracer/FALAT correction, where both papers were briefly and wrongly written into several files as a "5th kept baseline" before being caught and reverted once someone flagged that neither is peer-reviewed. The session closes by naming what the team still owes: independently re-reading ErrorProbe and AgenTracer in full, independently re-running at least one spike, spot-checking the commercial comparison, confirming licensing claims, and keeping the log itself updated going forward.

**Second session, same day — dataset expansion and a real abandonment.** AgentRx (a Microsoft project mechanistically adjacent to the silent-failure module) was fully removed from the project per explicit instruction, on the same scope-discipline logic as the GraphTracer/FALAT reversion, even though this particular case wasn't a factual error — it was a deliberate choice not to let a topically-adjacent find expand scope without being asked. This is also the session recording the full TracerTraj self-generation attempt and its abandonment (R11b, covered in depth in Part 9.11.2) — real Python-environment work, two real bugs found and fixed, and a clean stop once real pilot-timing data made the full run's infeasibility concrete. Three new datasets were downloaded and license-verified in this same session: GSM8K (8,792 rows, MIT), MATH (12,500 rows, MIT, with a first-attempt repository ID that turned out not to exist, corrected to the real one), and tau-bench retail (635 tasks plus full environment/tools/policy code, MIT confirmed via the actual downloaded LICENSE file). The log's own framing of this verification discipline is worth restating: "every number in `datasets.md` §6 was produced by a command run in this session, not recalled from training data."

**Third session, same day, later — feature narrowing and market research.** Market research was extended to three more observability platforms (Maxim AI, Opik, DeepEval/Confident AI), an external GPT session's sixteen product-feature ideas and seventeen-screen UI vision were reviewed and rated rather than uncritically adopted (the UI vision explicitly rated 3/10 as something to build this year, 8/10 as a design artifact, with its "Trace Explorer" screen flagged as the single worst idea in it, since it would mean rebuilding an existing competitor's core product from scratch), and an alternative ten-plus-ten feature brainstorm was generated, rated, and merged against the original twenty using five explicit filtering rules (genuine market gap, architectural compatibility, no duplication, the replacement test, workload-fit against the three-person split). The result was frozen into the plan doc's §7.0 as five foundational items plus seven extensions plus two explicitly deprioritized stretch items. SDG alignment (§0.05, SDG 9) was added in this session too. Most importantly for the register's later history, this session is where the gap that became spike 5 was first caught: cross-checking the POC spikes against the newly frozen fourteen-item list revealed that four of five foundational items had direct POC evidence, but the counterfactual replay engine (foundational item #5 at the time) had none at all — recorded explicitly rather than left implicit, with a fifth spike named as owed before the item could honestly claim the same evidentiary footing as the other four.

**Fourth session, next day — three spikes closing the prior session's gaps.** Confirmed a real local toolchain (Python 3.13.7, networkx 3.5, scikit-learn 1.8.0) needing no LLM API at all for any of the three new spikes — all pure local computation, zero cost. Spike 5 closed the counterfactual-replay gap flagged the session before (R13); spike 6 tested cyclic/dynamic graph support for the first time, including the control case that proved the revisit bound was load-bearing (R14); spike 7 produced the honest near-random classifier result (R15). The session's closing "what the team still owes" list is the fullest such list in the log's early history, naming eleven separate items — several of which (re-reading the two anchor papers, re-running spikes, the "explain your own subsystem out loud" test, deciding what to do about spike 7) persist essentially unchanged all the way through to the supervisor PDF's own "What Remains Open" section covered in Part 11.

**Fifth session — the rename that fixed a real supervisor critique.** Covered in Part 9.15 and 10.4.3 above: the "core attribution algorithm" label was split into its three real component stages after supervisor feedback that the original framing read as "fourteen features that map to one feature." The log is explicit that this was "split, not shrunk" — no mechanism, scope, or evidence changed, only the names, and the fifth session is also where the log states its non-rewriting policy for the first time, in the specific context of this rename. Two additional items were considered in this same session and explicitly not added: Automatic Retry (reframed as a *behavior* of two already-existing mechanisms working together, rather than a new standalone feature, since unconditional retry would contradict the already-committed confidence-gating principle) and Checkpointing (acknowledged as genuinely distinct from Verified Automatic Repair, but left open rather than added, since it hadn't yet been run through the same CCP/market/overlap filter every other item had received — this is the same Checkpointing item that resurfaces and finally gets resolved as Recovery Controller, R21, four sessions later).

**Sixth session — the market survey, Repair Agent, and Verified Repair Memory's history finally logged.** `Agentic_AI_Market_Survey_BS_FYP.docx` was reviewed in full, distinguished explicitly from the earlier `Commercial_Product_Comparison.md` as checking a different market layer (the orchestration frameworks Granite instruments, not the observability platforms Granite competes adjacent to). Repair Agent was added as foundational item #6, with its gap confirmed by the plan doc's own FR4 text, not invented to justify the addition. Verified Repair Memory's previously-lost history (R18) was reconstructed and properly logged for the first time in this session. The single-framework scope-narrowing advice was considered and rejected (R19). The full source content of the market survey was preserved verbatim in its own file, matching the project's existing pattern for pasted external material. And Repair Agent's own POC gap was closed the same session via spike 8, with the precise interface-ambiguity finding for its two failing cases (R17).

**Seventh session — the project's formal title and the TraceCause → Granite rename.** The official FYP registration title was adopted from the market survey's own §6 recommendation. The short title changed from TraceCause to Granite via a scripted regex replace applied carefully enough to leave on-disk filenames (like `Granite_Supervisor_Briefing.pdf`) unrenamed where they'd already been created under names that would break cross-references if changed — only the brand text inside documents changed. This is the session that establishes the non-rewriting policy for the project's own name, in language nearly identical to the fifth session's feature-rename framing.

**Eighth session — Framework Compatibility Layer.** Added as extension #8 in direct, positive response to a real scope question ("use features of all products, not only from one") without reopening the already-rejected single-framework advice or the frozen foundational list — R20's full reasoning is covered in Part 9.17. Propagated across the risk register, the commercial comparison, the defense package, the registration form answers, and the supervisor PDF (which needed a genuinely new appendix section added, not just a paragraph edit, to reproduce the full market survey verbatim).

**Ninth session — the same-day reclassification of Recovery Controller and Verified Repair Memory.** Covered in full in Part 9.18 (R21, R22). This is also the session where the PDF-generation script itself needed a real fix beyond a simple re-run — described in 10.4.4 above — and where the log closes by stating explicitly that "this is a reclassification of two items that existed as of a few hours earlier in the same day, not new evidence, not a change to any of the other 8 foundational items or their existing POC evidence." As of this document's own writing, the ninth session is the most recent entry in the log — meaning the log's own instruction to "keep this log updated going forward" (I3's ongoing-maintenance requirement) remains an active, standing obligation rather than a closed task, exactly as its own first-session entry anticipated it would be.

## 10.6 What could actually go wrong at each gate — a risk-weighted view

Section 10.1 above walks through what each gate requires, per the plan doc's own §12 timeline. It's worth going one layer deeper and asking, gate by gate, which specific open item from the register is the one most likely to actually put that gate at risk, given the project's honest state as of this document's writing — ten foundational items, two of which (Recovery Controller, Verified Repair Memory) carry a real, named gap rather than a completed proof.

**Gate 1 — Proposal defense.** The biggest risk here is not technical at all — every one of the plan doc's own §16 checklist items with real evidentiary weight (CCP characteristics, contribution statement, POC evidence, scope split, AI usage log, RAID register) is already substantially prepared, several exceeding the guide's own minimum bar (eight, later seven, then eight POC spikes against a one-spike minimum). The real risk to this gate is the three explicitly unchecked boxes converging at once: real stakeholder contact (I2), team role assignment (R6), and the prior-FYP archive check (guide §10). None of these are technical unknowns; all three are simply undone as of the register's last update, and all three are the kind of gap a panel is specifically primed to probe, since the guide itself names weak stakeholder involvement as "the most commonly missing characteristic" across student projects generally. The mitigating factor is that none of the three requires new technical work — closing them is a matter of the team's own remaining time before defense, not a matter of an experiment that might fail.

**Gate 2/3 — Mid-1.** The plan doc names its own top priority for this window explicitly, tied directly to a piece of real evidence rather than a generic to-do: building the full 3-stage ErrorProbe reproduction (tool-grounded Investigator plus Verified Episodic Memory) on a stronger backbone, because spike 1's 12.5% step accuracy on the simplified two-stage version is "nowhere near 59.5%." This is the single biggest risk to Mid-1 as a gate, because it is R1 in its still-open form — the highest-stakes risk in the entire project, still genuinely unresolved as of the last register update. Layered on top of that is the register's own instruction that Verified Repair Memory's stronger-backbone re-test (R22) and Repair Agent's targeted interface fix (R17) both need to land "before Mid-1" as well, meaning this single gate is where three separate open technical risks (R1, R17, R22) are all scheduled to converge and need resolving essentially simultaneously, alongside R6's team-role assignment. A realistic read of Mid-1 is that it is the most technically loaded of the five gates, not the proposal defense — the proposal defense is mostly about presenting and defending work already done; Mid-1 is where several of the project's most load-bearing open questions are all due to be answered at once.

**Gate 3 — Final-1.** Framed explicitly as the "exit gate" — a working core system, not individually-working components, demonstrated with an integration path proven end-to-end. The biggest risk here is not any single named risk-register entry but the general integration risk that section 10.3.2 above addresses directly: three tracks built genuinely in parallel across Weeks 10–16, each de-risked at the interface level by proposal-stage spikes (spike 2 for the graph data model, spike 1 for diagnosis pipeline input/output shape, spike 5 for replay mechanics), but not yet proven to compose correctly as a whole system. The register's own R17 finding — that Repair Agent's two failures traced to an interface-specification ambiguity, not a reasoning failure — is exactly the class of problem that could recur at other integration seams during this phase; the team's real mitigation is that this exact failure mode has already been caught once, with a precise diagnosis, which should make the team more alert to interface ambiguity as a recurring risk category rather than a one-off.

**Gate 4 — Mid-2.** The plan doc names this gate's evidentiary bar explicitly as "release readiness," and among its listed requirements is one that connects directly back to R16: "trace-data privacy handling verified (R16 threat model becomes a tested behavior, not just a written paragraph)." This is the biggest named risk specific to this gate — R16's threat model was written and marked "resolved" at proposal stage, but "resolved" there meant "the analysis and commitment exist and are documented," explicitly not "the redaction, namespacing, and retention mechanisms have been built and tested." If Mid-2 arrives and R16 is still only a written paragraph rather than a tested behavior, that is a genuine regression relative to what the timeline itself commits to, not merely a slow extension. The other real risk at this gate is scale: this is the point where the benchmark is scaled from the POC's handful of cases up to the target 500–1,000 traces, which is exactly where R5's still-open LLM API cost risk becomes concrete rather than hypothetical — a budget estimate produced from real per-trace token counts (owed since the proposal stage) needs to actually hold at this scale, or the full evaluation run itself is put at risk.

**Gate 5 — Final-2.** The plan doc's own §13 is explicit that this is the first point at which real deployment evidence — not a screenshot of a local build, which the guide's §1.2 explicitly warns against accepting — becomes an honest, producible claim. The biggest risk to this gate is therefore less about any single register entry and more about the discipline of not letting "deployed" quietly come to mean "runs on the machine that built it." The plan doc's own quoting of the guide's warning suggests the team has already internalized this distinction, which is itself a mitigating factor; the concrete risk is simply that this is the last gate, so any technical debt carried forward from Mid-2 (an unresolved R16 test, an unresolved R5 budget overrun, a still-failing Verified Repair Memory re-test if R22's condition isn't met by Mid-1) has nowhere left to go except into the final report as an honestly-reported, unresolved gap rather than a claim the team can actually stand behind.

## 10.7 Panel-style Q&A on governance and risk-tracking discipline itself

The preceding parts of this document repeatedly invoke the risk register as evidence of process rigor. It's fair to ask whether that's actually earned, or whether a 22-entry register is simply an elaborate way of looking rigorous — a kind of risk-theater, where logging a concern substitutes for actually managing it. The honest answer has to be checked against the register's own track record, not asserted, so this section works through the hardest versions of that question directly.

**"With 22 risks logged, how do you know this isn't just covering yourselves rather than actually managing risk?"** The test that separates genuine risk management from risk-theater is whether logging a risk ever actually changed what the team did next, versus simply documenting what the team was always going to do anyway. The register has real examples of both outcomes, and it's worth being honest about which is which. R19 (the market survey's single-framework scope-narrowing advice) is a clean example of the register changing a decision: the advice was seriously considered, weighed against RQ2's already-committed cross-architecture claim, explicitly rejected, and then answered with a new, scoped engineering decision (Framework Compatibility Layer, R20) rather than either blind acceptance or blind dismissal. R10 is another: an adversarial self-review found the silent-failure mechanism had zero test coverage, and that finding produced a same-session spike, not a scheduled-for-later note. R6, by contrast, is an example of a logged risk that has *not* yet changed anything — it correctly names an unassigned set of team roles as a real risk, but as of the register's last update, the roles are still unassigned. The honest distinction the register itself supports is: some risks demonstrably reshaped a decision (R19→R20, R7's literature triage reshaping what got read and what got explicitly accepted as residual risk, R10 reshaping same-session build priority), and some risks are accurately named but still open, waiting on the team's own remaining time (R6, R21's zero-POC gap, R5's still-unresolved budget question). A register that only ever recorded risks and never let any of them change a decision would deserve the "risk-theater" label; this one has enough of the former to earn the benefit of the doubt, while still being honest that several entries remain in the latter, unresolved category.

**"Isn't 'we accepted the risk' just a polite way of saying you gave up on due diligence?"** This is worth answering against R7's specific handling, since that's the entry that most directly makes this call. The team did not decide to stop reading literature because reading is expensive in the abstract — it made a scoped, reasoned decision after already doing real work: reading two of the most concerning papers (GraphTracer, FALAT) in full and confirming they were unpublished preprints, escalating two others (the silent-failure detection paper, DoVer) to "High" threat level after a closer read, and only then choosing not to do a full read of the remaining seven newly-surfaced papers, with an explicit, stated reason — none of them would ever be cited, added as a baseline, or change the contribution statement, since the project's actual strategy is improving on a peer-reviewed baseline (ErrorProbe), not pre-empting every unpublished preprint that shares topical territory. "Accepted, with a stated reason and a fallback answer already prepared for if it comes up at defense" is a materially different and stronger position than "ignored," and the register is careful to make that distinction visible rather than blur it.

**"A risk register that never gets anything wrong isn't credible — where did this one actually get something wrong?"** The A5 correction (9.12 above) is the cleanest example: an assumption was originally written in a form that presupposed a team-role split had already happened, when in fact it hadn't (R6 was still open). That's a real documentation error, caught and corrected in place, with the correction dated and the invalid original text struck through rather than deleted. The R18 logging failure (traced in full in 9.20.1) is a second, more operational example — an entire piece of real evidence was nearly lost because a logging step failed silently and nobody verified it landed, for roughly a day. Both are genuine failures of the process, not manufactured examples of humility. What makes them creditable rather than damning is that both were caught and corrected using the same discipline the register applies everywhere else — a dated entry describing what went wrong, not a quiet fix with no trace.

**"If a panelist picks the single weakest entry in this register, which one is it, and can the team actually defend it?"** By the register's own evidence, the weakest entry is R22 (Verified Repair Memory's foundational-core status) specifically because it is the one case where a scope decision (promoting the item to foundational) was made while the only real test on record for that mechanism had already failed completely — zero of eight cases, all twenty-four verifications `NOT_SUPPORTED`, a measured accuracy regression in the same run. The honest defense is not to minimize this — it's the position the register itself already commits the team to: state plainly that the mechanism's one real test failed, state the specific condition attached to keeping it in the foundational core (a stronger-backbone re-test before Mid-1), and state what happens if that re-test also fails (an honestly-reported foundational-item gap in the final report, not a footnote). A team that had quietly reworded R22 to sound more confident once the item became "foundational" would deserve to be caught out on this question; a team that can restate the actual failed numbers from memory and explain the reasoning behind committing to the item anyway is demonstrating exactly the kind of ownership the guide's §8.2 disclosure standard asks for.

**"Why should 22 entries logged largely in a handful of days, right before a proposal defense, be trusted as ongoing discipline rather than a one-time defense-prep exercise?"** This is a fair challenge to raise against the calendar facts alone — the register was opened 2026-08-22, and its most recent addenda are dated 2026-08-23 and 2026-08-24, all within a tight pre-defense window. The honest answer isn't to dispute the timing; it's to point at what the register itself commits the team to going forward. I3's own resolution is explicit that the AI usage log's "closed" status applies only "for this session," with ongoing maintenance stated as a standing, not one-time, obligation — and the register's own dated addenda structure (three separate addenda after the original table, each triggered by a new working session rather than batched into one) is itself evidence the team has already treated this as a living document across multiple real sessions, not a single retroactive write-up. The genuine test of whether this discipline survives past the proposal defense is whether Mid-1's own named obligations — R1's full-pipeline reproduction, R17's targeted interface fix, R21's Recovery Controller spike, R22's stronger-backbone re-test, R6's role assignment — actually get logged with real dated evidence when they happen, the same way the proposal-stage work was. That's not something this document can verify in advance; it's a commitment the register has made explicit and time-bound (repeatedly, "before Mid-1"), which at least gives a defense panel or a supervisor a specific, checkable date to hold the team to rather than a vague promise of future diligence.

**"Does grouping 22 risks by pipeline stage or by resolved/open status (9.0.3 above) actually reveal anything, or is that just reorganizing the same information for the sake of looking thorough?"** The regrouping in 9.0.3 does surface one genuinely useful, non-obvious fact that ID-ordering alone obscures: the two largest clusters in the register by entry count are benchmark construction/ground truth (five entries: R3, R11, R11b, A3, D1) and repair-and-recovery (five entries: R13, R17, R18, R21, R22) — and it is precisely the second of these two clusters that contains both of the project's currently-open foundational-item gaps (R21, R22). That's a more specific and more useful statement than "some things are still open" — it says exactly where the project's remaining foundational risk concentration actually sits: not spread evenly across the whole system, but clustered specifically in the repair-and-recovery half of the pipeline, which is also, not coincidentally, the newest and least externally-precedented half of Granite's own claimed contribution (Layer 4/5 in the market survey's own five-layer table, rated "Major gap" and "Strong FYP opportunity" respectively, precisely because so little existing tooling addresses them). A team preparing for Mid-1 gets a genuinely actionable signal from this regrouping: if time is scarce, the repair-and-recovery cluster is where the register's own evidence says the remaining foundational risk is concentrated, not an arbitrary guess about which subsystem needs the most attention next.

---

# PART 11 — OPEN ITEMS AND HONEST GAPS

This part draws on three converging sources that each independently list what remains unresolved: the plan doc's own §16 readiness checklist, the Guide Compliance Audit's findings, and the "What Remains Open" section embedded directly in `generate_supervisor_pdf.py` (§12 of the generated supervisor briefing). Where these three sources overlap, that overlap is itself meaningful — it means the same gap has been independently flagged from multiple angles (a self-check against the guide, a deeper compliance audit, and a summary document meant for the supervisor), which is a reasonable signal of how genuinely load-bearing the gap is, not just a documentation oversight in one place.

## 11.0 A summary table of every open item, before the full walkthrough

| # | Open item | Nature of the gap | Who/what can close it | Named deadline |
|---|---|---|---|---|
| 11.1 | Real stakeholder contact | Notional reasoning, no real contact yet | The team, directly, outside any document | Before defense (I2) |
| 11.2 | Team role assignment | Roles defined, nobody mapped to them | The team's own skill-fit decision | Before Mid-1 (R6) |
| 11.3 | Prior-FYP archive check | Requires internal departmental access | The team, via their own department | Guide §10, unscheduled but required |
| 11.4 | Explain-your-subsystem test | No document can substitute for this | Each of the three students, out loud, no notes | Before defense day |
| 11.5 | Verified Repair Memory re-test | One real test on record, and it failed | A stronger-backbone re-run | Before Mid-1 (R22) |
| 11.6 | Recovery Controller POC | Zero POC evidence at all yet | A minimal checkpoint-resume spike | Before Mid-1 (R21) |
| 11.7 | Spike 7's fate | Near-random result, path undecided | Re-test with harness data, or drop | Before defense, per the plan doc |
| 11.8 | Self-improvement capability | Conceptually undecided, not just untested | A distinct retrieval-and-reuse POC | Not yet scheduled |
| 11.9 | Various re-verification items | Team hasn't independently re-checked AI-assisted work | The team, per the log's own instructions | Ongoing, before defense/final submission |
| 11.10 | Two new silent-failure strategies need a POC | Proposed and designed, never run once | Diagnosis Owner, once role is assigned | Named in the supervisor PDF's own open-items list |

**A useful way to sort these nine items: which ones are blocked purely on team time, versus which ones are blocked on a real external dependency the team doesn't fully control.** Items 11.2, 11.5, 11.6, 11.7, and 11.9 are, in principle, closeable entirely by the team's own effort and judgment, with no dependency on anyone outside the team — they require deciding, building, testing, or reviewing, all of which the team can simply sit down and do. Items 11.1 and 11.3 are different in kind: 11.1 depends on a real external person (a stakeholder) agreeing to a conversation, and 11.3 depends on the department's own archive being accessible and searchable in a reasonable amount of time — both carry a small amount of genuine external-world uncertainty a purely internal task doesn't. Item 11.4 sits in an interesting middle position: it requires no external party, but it does require the three team members to actually be in the same room (or call) together, which is a scheduling constraint rather than a technical one. Item 11.8 is the odd one out — it isn't really "blocked" on anything specific yet, because the team hasn't even scoped what closing it would require; it's flagged here precisely because it's the one item that's still at the "we haven't yet decided what would even count as resolving this" stage, one step earlier than every other item on the list.

## 11.1 Real stakeholder contact — the single highest-priority gap

This is named as the top item across every one of the three source lists, and it deserves to be understood as more than a checkbox. Recall that the plan doc's own CCP rating (§2) rates Granite as clearing 8 of the Seoul Accord's 9 characteristics clearly, with only characteristic #6 — "diverse stakeholders" — left at "weak." The guide's own worked example explicitly names this as "the most commonly missing characteristic" across student projects generally, which is itself a useful piece of context: this isn't a Granite-specific weakness, it's a well-known failure mode the guide anticipates and calls out by name.

**Why this specific gap matters so much.** The plan doc's §0.06 (client identification) already names a notional client — "an engineering team operating a multi-agent AI system in or near production," grounded concretely in the tau-bench retail domain the active benchmark targets. But a *notional* client, reasoned about on paper, is categorically different from a real stakeholder actually contacted and consulted. The guide's own stakeholder-contact evidence bar (§B.1) applies here even though Granite is Stream A (research-derived, not a pure product pitch), because — as the plan doc itself notes — "the deployable-system half of the claim is real." Granite isn't purely an academic reproduction exercise; it explicitly claims to ship as an installable, framework-agnostic SDK a real engineering team could use, and that claim is much stronger with evidence that a real team was actually asked what they need, rather than the team's own inference about what such a team would probably want.

**What would actually close this gap.** Concretely, this means identifying and reaching out to real engineers who build or operate multi-agent AI systems — this could be practitioners the team already knows, faculty who work in adjacent areas, or teams building on the frameworks Granite instruments (CrewAI, LangGraph) — and having a genuine conversation (even a short one) about their actual pain points around failure diagnosis, whether the three needs already assumed in §0.06 (pre-deployment fault testing, post-incident root-cause diagnosis, pre-redeployment fix verification) match what they'd actually want, and whether anything assumed in the plan is off-base. Even a small number of real conversations converts characteristic #6 from "weak" (present in the writing, but under-argued, per the plan doc's own self-assessment) to "clear" — the guide doesn't require a large stakeholder study, it requires *real* contact rather than purely notional reasoning.

**Where this shows up.** Logged as Issue I2 in the risk register, targeted for resolution "before defense (this week)" as of the register's last update — meaning this is a live, time-pressured item, not something scheduled comfortably for later. It's also the first bullet in the supervisor PDF's "What Remains Open" section, described there as "the one item most directly tied to CCP characteristic #6." And it's the only unchecked box in the plan doc's own §16 checklist that the checklist itself flags with a specific, standalone note: "the one item nothing here can close" — meaning no amount of further internal documentation work substitutes for actually doing this.

**Why this gap is treated as urgent rather than merely "nice to have."** It's worth naming plainly what's at stake if this stays open through the actual defense: a panel reading the CCP rating table (plan doc §2) will see eight characteristics marked "Clear" and one marked "Weak," with the weak one specifically flagged by the team's own self-assessment as "the most commonly missing characteristic" per the guide. A prepared, honest team walks into that conversation having already closed the gap or having a specific, credible plan and partial evidence in hand; an unprepared team is left explaining, live, why a gap the guide itself warns is common was still open at the point of defense. The register's own target date — "this week," as of its last update — reflects that urgency directly: this is not a Mid-1 or Final-1 item, it is explicitly a pre-defense item, meaning it is understood to be one of the very last things standing between the current state of the project and a fully "Clear" CCP rating across all nine characteristics.

**What would make the resulting evidence genuinely strong, versus merely present.** Not every form of stakeholder contact carries equal weight. A single, brief, unstructured conversation technically satisfies "real contact happened," but a stronger version of this evidence would capture something specific and citable: a real practitioner confirming or correcting one of the three assumed client needs in §0.06, a concrete anecdote about a failure mode they've actually hit in production that Granite's scope does or doesn't address, or even a piece of pushback that leads to a recorded, dated scope adjustment — exactly the kind of change-control event (§5.3) this project's documentation has shown itself comfortable logging elsewhere (the GraphTracer/FALAT correction, the AgentRx removal, A5's correction). A stakeholder conversation that produces *some* concrete, specific finding worth recording is a stronger closing of this gap than one that produces only a general impression of polite interest.

## 11.2 Team role assignment — why this is a real decision, not paperwork

The three role areas — Data/Benchmark Owner, Diagnosis Engine Owner, Platform Owner — are fully defined in the plan doc's §9, complete with what each owns, what contribution type each represents, and what would disappear if that role were removed from the project. What's missing is the actual mapping of these three roles onto the three real people on the team.

**Why the register (R6) and the plan doc both insist this is "a real decision, not a formality."** The three roles genuinely require different skillsets. Data/Benchmark Owner needs data-engineering competence and comfort standing up and instrumenting real orchestration frameworks correctly — this is hands-on integration work against two different frameworks' differing message-passing and tool-call semantics (R2's own resolved-but-caveated finding shows this isn't trivial even at toy scale). Diagnosis Engine Owner needs causal/graph modeling and evaluation-method design skill — this is the role responsible for the project's actual algorithmic core and its silent-failure detection claim, arguably the most conceptually demanding of the three. Platform Owner needs full-stack deployment engineering competence — building and shipping an actual installable SDK, backend, and containerized deployment that works outside the original developer's machine, which is a different kind of skill again from either of the other two.

Assigning three people to these roles based on a coin flip, convenience, or alphabetical order, rather than genuine skill-fit, risks leaving a subsystem under-resourced relative to what it actually needs — and because each role is independently "meaningful" under the guide's own test (§9's "if removed, what disappears" column shows each role owns something the whole project would visibly lose without), a poor-fit assignment isn't just inefficient, it's a structural risk to the whole project's coherence.

**Deadline and mechanism.** The register requires this be resolved "before Mid-1" and, once decided, recorded per the guide's own change-control rule (§5.3) rather than silently absorbed — meaning the decision itself, and the reasoning behind it, should be written down as a dated entry, the same discipline applied to every other decision in this project's history. Once decided, plan doc §9, `architecture-sketch.md`, and `resources.md` all need updating to reflect real names rather than role-area placeholders.

**What a reasonable assignment process would actually look like.** Since the register frames this as a genuine skill-fit decision rather than an arbitrary split, a defensible process would involve each team member honestly assessing their own comfort and prior experience against the three role descriptions in plan doc §9 — not just picking whichever sounds most interesting — and then reconciling those self-assessments against the real, demonstrated evidence already in hand from the POC spikes themselves. For instance, whoever wrote and debugged spike 2's CrewAI instrumentation work, or spike 6's cyclic-graph traversal logic, has already produced direct, checkable evidence of comfort with exactly the kind of work Data/Benchmark Owner and Diagnosis Engine Owner respectively require — the spikes aren't just proof the mechanisms work, they're also a natural, already-existing record of who has hands-on experience with which parts of the system, which the team can draw on directly rather than assigning roles from a cold start with no evidence at all about individual fit.

## 11.3 Department prior-FYP archive check — why this genuinely can't be done externally

The FAST guide's §10 requires a comparison not just against academic papers and commercial products (both of which Granite has done thoroughly — nine-plus papers read in full, seven commercial observability platforms researched directly, plus the separate seven-framework orchestration-layer market survey), but also against **prior FYP projects from the same department**. This is explicitly the one piece of the required §10 comparison that remains open, and the reason is structural rather than a matter of remaining effort: this information lives in the department's own internal FYP archive, which isn't something an AI assistant researching externally has any access to. The Guide Compliance Audit states this plainly: "cannot be completed externally." The plan doc's §16 checklist echoes this exactly: "cannot be completed externally, needs the team to check their own department's FYP archive (guide §10, second half)." Slide 3 of the Proposal Defense Package even leaves an explicit placeholder row for this — "Closest prior FYP: *[team to fill in from department archive — guide §10, cannot be completed externally]*" — a deliberately visible gap rather than an omitted row, so that whoever assembles the final slide deck can see exactly what still needs filling in and where.

This is a good illustration of a broader point about the limits of AI-assisted work that this whole project's own AI Usage Log is built around: some tasks are not a matter of more research effort, they're a matter of access the assisting tool simply doesn't have. The team needs to actually go and look at their own department's records.

## 11.4 Each teammate independently explaining their own subsystem — "the actual panel test"

This item appears with almost identical wording across all three source documents, and the AI Usage Log's own phrasing is the most direct: "Each of the three students explains their own owned subsystem to the other two, out loud, no notes, before defense day. This is the one item on this list that cannot be satisfied by any document, including this one — it's the actual test a panel applies (guide §8.2), and it hasn't been attempted yet."

**Why this specific exercise matters more than any document review.** The FAST guide's §8.2, per the log's own framing quoted earlier in Part 10, states that what matters at defense is whether the team can "explain, justify, modify, and defend anything CCP-relevant that AI assistance touched." A defense panel doesn't read the risk register aloud and check it against a document — panelists ask direct questions, on the spot, about why a design decision was made, what would happen if a component were changed, what the team would do if a specific alternative had been chosen instead. This is essentially a live-fire rehearsal of exactly the kind of interrogation §14.1's four-part ownership test describes (explain it, justify alternatives rejected, predict what breaks, modify it under questioning) — and the plan doc's own checklist item states it as one of only three unchecked boxes remaining, explicitly noting "the one test no document substitutes for."

**Why it's framed as needing to happen with "no notes."** The whole point of the exercise is to surface, before the actual defense, any place where a team member's understanding of their own subsystem is shallower than the documentation makes it look — where they could recite what a document says but couldn't actually reconstruct the reasoning or predict a consequence unprompted. This is precisely the failure mode the entire AI Usage Log exists to guard against: every single verification-status column in that log exists because the team explicitly does not want to be in a position, at defense, of having absorbed an AI-produced explanation without ever having independently owned it. This exercise is the final, most direct test of whether that absorption has actually happened.

## 11.5 Verified Repair Memory's pending stronger-backbone re-test

Covered in depth in Part 9 (R18/R22), but worth restating here specifically as an *open item with a concrete next action*, since it's one of the two items the register itself names as "the clear gap to close before Mid-1."

**What "a stronger backbone" concretely means.** Every POC spike run so far — including the one and only test of this specific mechanism — used `llama3.2:3b`, a free, locally-hosted 3-billion-parameter model via Ollama. This is a genuinely small model by current standards, chosen specifically because it lets the team run every spike at zero cost. The register's own framing repeatedly ties Verified Repair Memory's failure specifically to "the local 3B model backbone used," implying — though not yet proving — that the mechanism's complete failure (zero of eight cases committing anything, all twenty-four verifications returning `NOT_SUPPORTED`) might be a consequence of the small model's weaker reasoning capacity to correctly judge whether evidence sufficiently supports a hypothesis, rather than a fundamental flaw in the memory-and-verification design itself. A "stronger backbone" concretely means re-running the same test — or a version of it — against a substantially larger or more capable model, whether that's a bigger local open-weight model (the supervisor PDF names GPT-OSS-120B and Qwen3-32B as backbones ErrorProbe's own authors used, and ones Granite could self-host) or a paid API-backed frontier model, funded from whatever budget resolution R5 eventually produces.

**What happens if the re-test also fails.** This is where the register's discipline is most explicit and most important to carry forward honestly: R22 states plainly that if the re-test also fails, "this is a foundational-item gap the team must be ready to explain under questioning (Section 14.1), not a footnote — the one real test result stays on record as a failure, not softened just because the item is core now." This means the team has already, in effect, pre-committed to *not* quietly dropping or downplaying Verified Repair Memory if a second, better-resourced test still doesn't work — the honest path in that scenario would be reporting the negative result directly at whatever gate is relevant, explaining what was tried, and either scoping the feature down, redesigning the underlying verification-threshold logic, or explicitly acknowledging it as an unresolved foundational gap in the final report, rather than pretending the reclassification into "foundational" status somehow already fixed the mechanism.

## 11.6 Recovery Controller's pending POC — what a minimal spike would look like

Recovery Controller (R21) is, as established in Part 9, the one genuinely *new* piece of mechanical work among the foundational items with zero POC evidence at all — not a rename, not a variant of something already tested, a real gap. Following the same proportional-effort pattern every other foundational item's initial POC has used (small, targeted, cheap, local-model-or-zero-cost where possible), a reasonable minimal spike for this would look something like: build the same kind of small, deterministic toy pipeline the earlier spikes used (echoing spike 5's three-step deterministic setup), but this time actually persist intermediate execution state to disk (or an in-memory structure standing in for a real checkpoint store) after each step, deliberately corrupt a value at an intermediate step, run the diagnosis-and-repair logic already proven in spikes 1/5/8 to produce and verify a fix, and then specifically test *resuming execution from the saved checkpoint at the repaired point* rather than re-executing the whole downstream chain from scratch (which is what spike 5 already validated). The meaningful new thing to test isn't the repair logic itself — that's already covered — it's whether checkpoint save/restore correctly reconstructs the exact execution state needed to resume cleanly, and whether that resumption produces the same correct final outcome as full downstream re-execution would, but without the redundant recomputation cost. This is exactly the kind of "small, targeted spike, not production test coverage" the guide's own POC framing calls for, and it's explicitly still owed — no such spike has been run as of the last register update.

## 11.7 Spike 7's undecided fate: re-test or drop

Covered as an evidentiary finding in Part 9 (R15), this item belongs here too because it is explicitly still an open decision, not a resolved one. The plan doc's own Weeks 8–14 timeline slot for the preventive clarification classifier extension is marked "contingent, not automatic," and the supervisor PDF's own "What Remains Open" list restates it directly: "Decide what to do about spike 7's near-random result (precision/recall/f1 = 0.25) before defense: either test with larger/harness-generated data or better features..., or explicitly scope the preventive classifier extension down/out if it doesn't improve — don't leave a known-broken result unaddressed in the plan."

Two genuinely distinct paths remain open, and the register itself doesn't pre-judge which is correct:

**Path one — re-test with better data and/or better features.** The register names two specific, independently testable hypotheses for why spike 7 scored near-random: the 20 hand-written training examples may simply be too small a sample and, more importantly, may not represent what real corruption actually looks like (a human trying to imagine corrupted handoffs is a poor substitute for corruption an actual fault-injection harness produces), or the underlying TF-IDF bag-of-words feature representation may genuinely be too weak for this specific classification task, in which case cheap local sentence-embedding features (still free, still no API cost) are the next thing worth trying before concluding the approach needs something heavier still. Since the fault-injection harness itself is scheduled for build in Weeks 1–6 of FYP-2, real harness-generated labeled pairs won't even exist to re-test against until that work is done — meaning this decision is naturally gated on other core-build progress, not purely a standalone choice the team can make in isolation right now.

**Path two — drop the extension.** If a re-test with genuinely better data and features still fails to clear the near-random threshold, the plan doc's own instruction is explicit: "drop it rather than ship a known-broken classifier." This reflects the same standing discipline visible throughout this project — an extension that doesn't work doesn't get shipped anyway just because it was on the original list; the fault-injection harness build and the rest of the extension slots aren't contingent on this one succeeding, so dropping it costs the project a feature, not its structural integrity.

## 11.8 The "self-improve from prior failures" feature gap — genuinely undecided

This connects directly back to Verified Repair Memory (11.5 above) but is worth naming as its own distinct open question, because it's conceptually broader than just "does the memory-commit mechanism work on a better backbone." Verified Repair Memory's stated purpose — per the plan doc's own §7.0 description — is to "store successful error→diagnosis→repair patterns and retrieve them for similar future failures," which is the mechanism by which Granite would actually improve its own diagnosis-and-repair performance over time by learning from prior verified fixes, rather than treating every new failure as a cold start with no benefit from past experience. As of the register's latest state, this entire capability rests on a mechanism that has one real test on record, and that test failed completely (zero commits out of eight cases). Whether Granite genuinely gains any "self-improvement from prior failures" capability at all is therefore an open question in the fullest sense — not merely "unverified pending a re-test," but conceptually undecided, since even a successful re-test would only establish that the memory-commit step *can* work under better conditions, not yet that retrieving and applying a remembered pattern to a *new*, similar-but-not-identical failure actually improves outcomes in practice. That retrieval-and-reuse half of the mechanism has no POC evidence at all yet, positive or negative — it hasn't been tested even once, successful backbone or not. This is worth stating plainly as its own gap rather than folding it entirely into R22's re-test framing, because "does the memory commit successfully" and "does a committed memory actually help with a later, different failure" are two separate empirical questions, and only the first of the two has even been attempted.

## 11.9 Other explicitly-flagged open items from the source material

A few smaller but explicitly named open items round out the picture, each drawn directly from the AI Usage Log's own "what the team still owes" list (fourth session) and the source documents' scattered verification notes:

- **Independently re-reading ErrorProbe and AgenTracer in full.** These are the two papers the entire contribution claim is measured against, and the log names this as the first item the team still owes — not a peripheral reading assignment, but the two most load-bearing sources in the whole project, which the team needs to have read themselves rather than relying on the AI-assisted summary.
- **Independently re-running at least one, ideally several, of the eight POC scripts.** Every single spike carries an explicit instruction that its reported result should not be taken on the log's word alone — this is stated separately for spikes 1 through 4 (fourth session's closing list) and again for spikes 5 through 7 ("same standing instruction as spikes 1-4"), and again implicitly for spike 8. Spike 7's negative result gets called out specifically as needing independent verification, with the log noting directly: "an AI reported a classifier doesn't work" is exactly the kind of claim that needs verifying, not just accepting" — treating even a *negative*, seemingly self-effacing result as something that still needs independent confirmation, not just positive results.
- **Spot-checking commercial platform claims against live vendor documentation.** `Commercial_Product_Comparison.md`'s claims (the original four platforms, plus Maxim AI, Opik, and DeepEval added later) are explicitly flagged as more perishable than academic citations — vendor feature pages change faster than papers get revised — so the standing instruction is to check at least one platform's actual current documentation directly before relying on the comparison at defense.
- **Confirming licensing claims against actual repositories**, specifically Who&When (claimed MIT) and TracerTraj (claimed Apache 2.0, though R11's own finding complicates this — the repository has no LICENSE file at all for the data itself) — before the project report cites either as a settled fact.
- **Reading and confirming comfort with the SDG alignment paragraph** (plan doc §0.05) before citing it at defense, rather than accepting it as written without the team having sat with the reasoning themselves.
- **Reviewing the renamed feature labels in context** (the 2026-08-23 rename) and the new project title and short name "Granite" (the 2026-08-24 rename) to confirm they read correctly and that "Granite" doesn't collide with anything else, before either name gets used at defense or on the official FYP registration form.
- **Independently reviewing every "propagated for consistency" pass** noted in Part 10.4.4 — every one of the later AI Usage Log sessions closes with the same caveat that mechanical propagation across files has happened, but the team's own read-through and comfort with the new content has not yet happened.

## 11.10 The two new silent-failure strategies still needing their own POC

One further open item is worth naming on its own, separate from the rest of Part 11, because it doesn't come from the risk register or the AI Usage Log directly — it comes from the supervisor briefing's own "What Remains Open" section (`generate_supervisor_pdf.py` §12), which names it as an item nothing else on this list quite covers: "POC-testing the 2 newly-proposed silent-failure strategies (Cross-Agent Consistency Verification, Constraint Provenance Tracing) before they can be added to the validated core."

**What these two strategies are.** Both are proposed complements to the Semantic Error Diagnostic mechanism (covered in depth in Parts 6–8 of this document, in the walkthrough of the silent-failure detection work). Cross-Agent Consistency Verification extracts typed facts stated independently by two or more agents about the same entity and diffs them against each other — a rule-based check, no model call required — on the reasoning that a silent failure often shows up as one agent's value silently diverging from another agent's value, even though each individual output looks locally well-formed on its own. Constraint Provenance Tracing walks the execution graph backward from any claimed constraint in the final output (a claim like "under budget" or "in stock") and checks whether a corresponding upstream tool-call or verification node actually exists to back that claim up — generalizing the same logic behind spike 4's own "no DB tool called" style near-miss case into a broader, structural class of claimed-but-unverified constraints.

**Why this belongs in the open-items list and not the validated-mechanism list.** Both strategies are real, worked-through design proposals — the underlying logic for each is specified precisely enough to describe exactly what a POC for each would need to test — but neither has been implemented or run even once. This is a meaningfully different status than R10's silent-failure detector (spike 4), which at least has one real, if narrow, positive test behind it. These two strategies currently have the same evidentiary status Recovery Controller had before this document's own R21 walkthrough: a precise, specified idea, and zero code run against it. The supervisor PDF is explicit that they need to be POC-tested "before they can be added to the validated core" — meaning the team has, on its own initiative, pre-committed to the same discipline visible everywhere else in this register: a well-specified idea is not the same thing as a validated one, and the two should not be presented interchangeably.

**What closing this gap would concretely look like.** Following the same proportional-effort pattern every other spike in this project has used — small, targeted, cheap or free, using the same local model backbone wherever possible — a minimal Cross-Agent Consistency Verification spike would need at least two agents producing outputs that reference the same entity, with a hand-constructed case where the two outputs silently diverge (one agent's stated total doesn't match another's, for instance), and a check for whether the rule-based diff correctly flags the divergence without false-positiving on cases where the two agents' outputs genuinely don't overlap. A minimal Constraint Provenance Tracing spike would need a toy execution graph with at least one claimed constraint that has a real, traceable upstream verification node, and at least one claimed constraint that does not — checking whether the backward graph walk correctly distinguishes the two. Neither spike requires new infrastructure beyond what spikes 2 and 6 (graph construction and graph traversal) have already exercised; the work owed here is specifically running these two, not inventing new tooling to run them with.

---

## Where Granite actually stands today — a closing synthesis across all eleven parts

The parts of this document leading up to this one have each been expanded well beyond a bare listing of facts: Parts 1–3 walked identity, the research baseline, and the CCP justification down to the level of individual naming decisions and paper-by-paper reasoning; Parts 4–5 worked through the market research and the full feature-list evolution with worked examples of what existing tools miss and Granite catches; Parts 6–8 traced all eight POC spikes, the architecture, and the evaluation plan down to concrete, numeric worked traces. Parts 9–11, covered here, close the loop by asking a different kind of question than the earlier parts — not "what is Granite" or "what has Granite proven," but "how honestly has this project tracked its own uncertainty, and what does it still owe." It's worth pulling that thread together explicitly, in plain terms, rather than leaving the reader to assemble it from twenty-two separate risk entries.

**What is genuinely proven, as of the register's last update.** Eight of Granite's ten foundational features have real, run, inspectable POC evidence behind them — not descriptions of what the mechanism would do, but actual scripts that actually ran and produced actual output, preserved on disk and referenced by filename throughout Part 9. The cross-architecture claim has real structural evidence (spike 2's clean CrewAI trace). The fault-injection ground-truth strategy has real evidence from two runs, including an instructive negative result that reshaped how the benchmark itself should be built (spike 3). The silent-failure detection mechanism has a real, if narrow, positive test (spike 4). The mechanical replay-and-recovery logic works (spike 5). Cyclic graph traversal works, and the control case proves the safety mechanism is load-bearing, not decorative (spike 6). Repair generation succeeds more often than not, with a precisely diagnosed, fixable cause for its failures (spike 8). None of this is asserted from a paper's abstract or from what an AI assistant reported without independent scrutiny — every one of these results is tied to a specific script, a specific date, and a specific, stated set of what it does and does not prove.

**What is genuinely still open, stated as plainly as the register states it.** Two of the ten foundational items carry a real, unresolved gap rather than a completed proof. Recovery Controller (R21) has zero POC evidence of any kind — a well-scoped, genuinely new piece of mechanical work that simply hasn't been attempted yet, though a favorable precedent exists in five of seven surveyed frameworks already shipping generic checkpoint infrastructure. Verified Repair Memory (R22) has one real test, and that test failed completely — zero of eight cases committing anything to memory, a measured accuracy regression in the same run — with the team's own stated condition being that a stronger-backbone re-test must happen before Mid-1, and an explicit commitment that if it fails again, the gap gets reported honestly rather than softened. Beyond the two foundational gaps, three further items sit at "genuinely undecided, not merely unverified": whether the preventive clarification classifier extension is worth re-testing or should simply be dropped (R15/11.7), whether the "self-improve from prior failures" capability is coherent at all given that only half of its underlying mechanism has ever been tested (11.8), and whether the two newly-proposed silent-failure strategies (Cross-Agent Consistency Verification, Constraint Provenance Tracing) will validate once actually run (11.10) — none of these has been quietly assumed to work; all three are named, dated, and left open.

**What is a governance gap rather than a technical one.** Three of the highest-priority items in Part 11 have nothing to do with whether a mechanism works — real stakeholder contact (11.1), team role assignment (11.2), and the department's internal prior-FYP archive check (11.3). These are the items most exposed at the proposal defense specifically because they cannot be closed by any amount of further spike-running or document drafting; they require a real conversation, a real decision about who owns what, and a real look at internal departmental records. The register and the plan doc are both explicit and consistent about this distinction — it is drawn the same way in the risk register's Issues table (I2), the plan doc's own §16 checklist, and the supervisor PDF's "What Remains Open" list, which is itself a meaningful form of corroboration: three independently-maintained documents, produced across different sessions, all converge on the same three gaps as the ones most urgently needing the team's own direct action rather than more documentation.

**What this document's own eleven parts, taken together, actually demonstrate.** The proof this project offers of its own rigor isn't any single spike result or any single risk entry — it's the pattern visible across all of them, examined together. A risk register that reopens its own resolved entries when new information arrives (R1's downgrade rather than closure, R18's evidence preserved unmodified through R22's reclassification). An AI usage log that refuses to rewrite its own history even when a name or a classification later changes (the TraceCause→Granite rename, the feature-renaming session, both explicitly preserving old text as historically accurate rather than retroactively correcting it). A team that catches its own overclaims before a panel would (the GraphTracer/FALAT baseline correction, the AgentRx removal, the "nobody automates diagnosis" framing correction in R9). A team that abandons a real, partially-working effort once the honest numbers say it isn't worth continuing, and says so plainly rather than quietly dropping it (R11b's TracerTraj self-generation attempt). And a team that, when a mechanism's only real test fails, still writes that failure into its own core planning documents rather than waiting for a stronger result to report first (R18/R22).

**The honest bottom line.** Granite, as of the state this document describes, is a project with a real, evidenced technical core — eight of ten foundational mechanisms independently demonstrated, a genuine and specific market gap independently corroborated by an external survey's own classification table, and a research contribution built on top of a peer-reviewed baseline rather than an unverifiable one. It is also a project with real, named, unresolved gaps — two foundational mechanisms without completed proof, three governance items requiring the team's own direct, un-outsourceable action, and a small number of extension-level decisions still genuinely undecided. Neither half of that description cancels the other out, and this document's own governing discipline, inherited directly from the risk register and the AI usage log it draws from, is to present both halves together, precisely because a project that only ever showed its finished work would be a materially less trustworthy account of itself than one willing to also show, in full, exactly what it still owes.

---

## Closing note on this document's own scope

This document has attempted to walk through every entry visible in the two primary source files (`risk-register.md` and `AI_Usage_Log.md`) at the depth the source material itself supports — explaining not just what each entry states, but why it was logged, what evidence backs it, and why its current status is defensible given that evidence. Where an item's fate is genuinely undecided in the source material (spike 7, the self-improvement retrieval mechanism, Recovery Controller's still-unbuilt POC), this document has tried to describe the shape of the decision honestly rather than resolving it — because resolving it isn't this document's job, and pretending otherwise would be exactly the kind of overclaim this project's own discipline, demonstrated across every entry above, is built to avoid.
