# Granite — Documentation Index

This folder holds all FYP documentation for **Granite** (recently renamed from "TraceCause" — a few filenames still carry the old name intentionally, as historical/reference material). Files are organized into six numbered subfolders by purpose. This index is the entry point — start here.

---

## [01-planning-and-scope/](01-planning-and-scope/)
Core scope, architecture, and resourcing — the living plan the rest of the project traces back to.

- [FYP_Scope_CCP_and_Implementation_Plan.md](01-planning-and-scope/FYP_Scope_CCP_and_Implementation_Plan.md) — the index document for the whole project: scope, CCP rating, implementation plan
- [Granite_FYP_Idea_OnePage.md](01-planning-and-scope/Granite_FYP_Idea_OnePage.md) — the handbook's required one-page FYP idea format (title, difficulty, narrative, references, deliverables, prerequisites, supervisor), filled from the plan doc
- [architecture-sketch.md](01-planning-and-scope/architecture-sketch.md) — one-page system architecture sketch
- [datasets.md](01-planning-and-scope/datasets.md) — datasets used/considered, licensing, access notes
- [resources.md](01-planning-and-scope/resources.md) — compute, models, tooling, and cost resourcing
- [cost-estimate.md](01-planning-and-scope/cost-estimate.md) — API cost estimate and model plan; §0 records the 2026-09-04 decision to run the full project at $0 committed spend, on local Ollama throughout (closes risk-register R5, R37)
- [Software_Design_Specification.md](01-planning-and-scope/Software_Design_Specification.md) — component/data/API/schema-level design (Mid-1-track, not proposal-defense material): system context, component architecture, data flow, ER diagram, API contract, sequence/state diagrams, deployment — strictly within the frozen scope, nothing added
- [Project_Vision.md](01-planning-and-scope/Project_Vision.md) — standalone project vision: problem, motivation, target users, product/research vision, objectives, boundaries, expected outcomes, novelty
- [Use_Case_Model.md](01-planning-and-scope/Use_Case_Model.md) — full actor/use-case model (11 use cases, `«include»`/`«extend»` relationships with rationale), paired with [diagrams/Use_Case_Diagram.svg](01-planning-and-scope/diagrams/Use_Case_Diagram.svg)
- [System_Sequence_Diagrams.md](01-planning-and-scope/System_Sequence_Diagrams.md) — 3 black-box SSDs (actor + `:Granite` system boundary, distinct from the SDS's internal design-level sequence diagram): [SSD1_Submit_Trace_and_Diagnose.svg](01-planning-and-scope/diagrams/SSD1_Submit_Trace_and_Diagnose.svg), [SSD2_Generate_and_Verify_Repair.svg](01-planning-and-scope/diagrams/SSD2_Generate_and_Verify_Repair.svg), [SSD3_Review_Diagnosis_Dashboard.svg](01-planning-and-scope/diagrams/SSD3_Review_Diagnosis_Dashboard.svg)
- [Software_Requirements_Specification.md](01-planning-and-scope/Software_Requirements_Specification.md) — formal SRS (what the system must do): functional/non-functional requirements with IDs and priorities, stakeholders, actors, scope, assumptions, constraints, dependencies, external interfaces — distinct from the SDS (how it's built)
- [Test_Plan.md](01-planning-and-scope/Test_Plan.md) — formal test plan: objectives, strategy, levels, functional/non-functional/security/performance testing, techniques, environments, entry/exit criteria, defect handling, requirement→test traceability
- [Software_Development_Plan.md](01-planning-and-scope/Software_Development_Plan.md) — formal SDP: methodology, phases, work breakdown, milestones, roles, tech stack, environment, VCS/branching, standards, integration/deployment strategy — restructured from the plan doc, not a renamed copy

## [02-evidence-and-tracking/](02-evidence-and-tracking/)
Ongoing project bookkeeping — risk, AI-usage, and compliance records.

- [risk-register.md](02-evidence-and-tracking/risk-register.md) — RAID register (risks, assumptions, issues, dependencies)
- [AI_Usage_Log.md](02-evidence-and-tracking/AI_Usage_Log.md) — AI usage log across the project
- [Guide_Compliance_Audit.md](02-evidence-and-tracking/Guide_Compliance_Audit.md) — audit against the FAST FYP guide's requirements
- [Form13_GenAI_Disclosure_Sheet.md](02-evidence-and-tracking/Form13_GenAI_Disclosure_Sheet.md) — the handbook's Form 13 (External Tool/API/GenAI Disclosure Sheet), filled from `AI_Usage_Log.md`
- [Pre_Defense_Checklist.md](02-evidence-and-tracking/Pre_Defense_Checklist.md) — every "team must verify/decide" item compiled across all `AI_Usage_Log.md` sessions, deduplicated
- [Team_Action_Items.md](02-evidence-and-tracking/Team_Action_Items.md) — the human-only subset of the checklist above (things no document can close on the team's behalf)
- [Traceability_Matrix.md](02-evidence-and-tracking/Traceability_Matrix.md) — requirement → use case → design → test matrix, plus the final cross-document consistency audit (use cases vs. requirements, SSDs vs. use cases, wireframes vs. real functionality, terminology, scope boundary)

## [03-market-and-literature-research/](03-market-and-literature-research/)
Literature review, baseline selection, and commercial/market landscape.

- [Commercial_Product_Comparison.md](03-market-and-literature-research/Commercial_Product_Comparison.md) — comparison against commercial observability platforms
- [Agentic_AI_Market_Survey_Full_Content_and_Integration.md](03-market-and-literature-research/Agentic_AI_Market_Survey_Full_Content_and_Integration.md) — full market survey content and integration notes
- [ErrorProbe_Baseline_Selection.md](03-market-and-literature-research/ErrorProbe_Baseline_Selection.md) — why ErrorProbe was selected as the SOTA baseline
- [Full_Literature_Landscape_Analysis.md](03-market-and-literature-research/Full_Literature_Landscape_Analysis.md) — full-text review of all 7 core papers, the current evidence base
- [AgenTracer_vs_WhoWhen_Analysis.md](03-market-and-literature-research/AgenTracer_vs_WhoWhen_Analysis.md) — superseded, kept for history (see file header)
- [Paper_Release_Timeline.md](03-market-and-literature-research/Paper_Release_Timeline.md) — publication timeline of the core papers

## [04-poc-evidence/](04-poc-evidence/)
Proof-of-concept spike results and the silent-failure-detection research behind them.

- [POC_Spike_Outputs_Full.md](04-poc-evidence/POC_Spike_Outputs_Full.md) — full outputs from all proposal-stage POC spikes
- [Silent_Failure_Detection_and_Testing_Strategies.md](04-poc-evidence/Silent_Failure_Detection_and_Testing_Strategies.md) — silent-failure detection strategies, evaluated and honesty-checked

## [05-deliverables/](05-deliverables/)
Supervisor- and panel-facing deliverables. Reorganized 2026-09-07: each generator script now sits next to its own output in its own subfolder (so "run from within this folder" instructions still work unchanged); markdown deliverables that other documents link to directly stay at this folder's root.

- [FYP_Registration_Form_Answers.md](05-deliverables/FYP_Registration_Form_Answers.md) — official FYP registration form answers
- [Proposal_Defense_Package.md](05-deliverables/Proposal_Defense_Package.md) — proposal defense slide-by-slide package (markdown content)
- [Supervisor_Briefing.md](05-deliverables/Supervisor_Briefing.md) — plain-language condensed briefing for the supervisor meeting
- [Granite_Architecture_Atlas.html](05-deliverables/Granite_Architecture_Atlas.html) — 9 architecture diagrams plus a "Requirements & Design" tab (Use Case Diagram, 3 SSDs, wireframe-set link) and a coverage matrix / gaps-and-decisions reference — open directly in a browser, no build step
- [Granite_Wireframes.html](05-deliverables/Granite_Wireframes.html) — 16 screens/states across 8 sections, low-fidelity/grayscale by convention, each annotated with the requirement or endpoint it satisfies; flags the genuine gaps (SDK onboarding, live trace submission, repair approval) distinctly from the real, shipped `poc-demo` screens
- [Granite_Wireframes_2.html](05-deliverables/Granite_Wireframes_2.html) — same 16 screens at near-final visual fidelity: real palette, realistic sample data drawn from the actual spike evidence, and explicit **Novelty** flags on the 3 capabilities with strong, specific evidence of being a genuine differentiator (checked against LangSmith/Langfuse/Braintrust/Arize/Maxim/Opik/DeepEval)

**[proposal-deck/](05-deliverables/proposal-deck/)**
- [Proposal_Defense_Slide_Content_Spec.md](05-deliverables/proposal-deck/Proposal_Defense_Slide_Content_Spec.md) — full slide-by-slide spec (purpose, on-slide content, visual, evidence, presenter emphasis) behind the pptx deck, plus final slide order, narrative, [TO BE PROVIDED] list, and panel attack points
- [generate_proposal_deck.js](05-deliverables/proposal-deck/generate_proposal_deck.js) — pptxgenjs generator for `Granite_Proposal_Defense.pptx` (run with `node generate_proposal_deck.js` from within this subfolder)
- `Granite_Proposal_Defense.pptx` — the actual 10-slide defense deck (output of `generate_proposal_deck.js`), supervisor Dr. Adil Majeed, project code F26-060-Granite

**[supervisor-briefing/](05-deliverables/supervisor-briefing/)**
- [generate_supervisor_pdf.py](05-deliverables/supervisor-briefing/generate_supervisor_pdf.py) — generator script for `Granite_Supervisor_Briefing.pdf` (run from within this subfolder)
- `Granite_Supervisor_Briefing.pdf` — generated 12-section supervisor briefing (output of `generate_supervisor_pdf.py`)

**[ccp-justification/](05-deliverables/ccp-justification/)**
- [generate_ccp_docx.py](05-deliverables/ccp-justification/generate_ccp_docx.py) — generator script for `Granite_CCP_Justification.docx` (run from within this subfolder)
- `Granite_CCP_Justification.docx` — generated CCP justification document (output of `generate_ccp_docx.py`)
- `Granite_CCP_Justification_Seoul_Accord.docx` — Seoul-Accord-framed variant of the same justification

## [06-archive-superseded/](06-archive-superseded/)
Earlier, since-narrowed drafts kept for history — not live spec, not to be updated.

- [TraceCause_AgentTestLab_Pitch.md](06-archive-superseded/TraceCause_AgentTestLab_Pitch.md) — the original, un-scoped ~10-layer "AgentTestLab" pitch, frozen intentionally
- [TraceCause_Product_Vision_UI.md](06-archive-superseded/TraceCause_Product_Vision_UI.md) — aspirational "Mission Control Center" UI vision, not part of the FYP scope

## [07-full-project-explanation/](07-full-project-explanation/)
- [Granite_Full_Project_Explanation.md](07-full-project-explanation/Granite_Full_Project_Explanation.md) — **internal narrative record, not a deliverable.** Long-form explanation kept for the team's own reference; do not present from it and do not treat it as spec — the plan doc (§01) is the source of truth.

---

## Pre-defense audit deliverables (repository root)

Produced 2026-08-25 by an independent critical audit of this repository against the full FAST FYP guide. The audit's verdict was *"approvable, with six specific vulnerabilities"* — all six have since been applied to the documents above, with each decision recorded in risk-register.md R23–R26.

- [`01_Executive_Audit_and_Verdict.md`](../01_Executive_Audit_and_Verdict.md) — the audit itself: verdict, six vulnerabilities ranked, compliance matrix, scorecard, prioritized change log
- [`02_Panel_Defense_Question_Bank.md`](../02_Panel_Defense_Question_Bank.md) — adversarial rejection attempt (A1–A10) + full question bank (Q1–Q24), each with the ≤30-second answer to say aloud. **Rehearse Part A first**
- [`03_Proposal_Slides_with_Speaker_Notes.md`](../03_Proposal_Slides_with_Speaker_Notes.md) — the 10-slide deck with speaker notes and the question each slide triggers
- [`04_Granite_Knowledge_Base.md`](../04_Granite_Knowledge_Base.md) — every load-bearing concept at four levels (layman → undergraduate → how Granite uses it → the likely panel question)
- [`05_Repository_Change_and_Commit_Plan.md`](../05_Repository_Change_and_Commit_Plan.md) — the file-by-file change plan executed on 2026-08-25
- [`06_Expanded_Scope_and_Feasibility_Plan.md`](../06_Expanded_Scope_and_Feasibility_Plan.md) — the scope expansion + feasibility engineering pass: limitation inventory, eleven methodology additions, Core/Advanced/Stretch/Future bands, effort budget, descope ladder, MDP-per-gate, panel objections both ways (risk-register R27)
- [`07_Handbook_2026_Compliance_Audit_and_Response.md`](../07_Handbook_2026_Compliance_Audit_and_Response.md) — 2026-09-04 re-audit against the fuller `docs/BS-FYP-Handbook-2026_DRAFT.pdf` (3rd Edition, 85 pages, read in full): section-by-section compliance (A), PoC audit (B), 1-year feasibility (C), market validation (D), all 27 requested questions answered, 10 additional adversarial questions, and 16 final deliverables (verdicts, scores, roadmap, pitch). Found and fixed two real gaps (DEI statement, `AI_Usage_Log.md`'s stale header) — risk-register R30–R33
- [`poc-demo/`](../poc-demo/) — a working, locally-runnable proposal-defense prototype (FastAPI + React/TypeScript). Wired to the **real** 8 spike outputs, not simulated data — see `poc-demo/README.md` for what's real vs. illustrative, run instructions, and a data discrepancy the build surfaced in Spike 1's step-accuracy figure (since fixed and re-run 5×, see risk-register R28)

---

*Maintained as the entry point to `markdowns/`. When adding a new file, file it under the closest-matching subfolder above and add a line here.*
