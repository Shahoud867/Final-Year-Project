# Granite — Documentation Index

This folder holds all FYP documentation for **Granite** (recently renamed from "TraceCause" — a few filenames still carry the old name intentionally, as historical/reference material). Files are organized into six numbered subfolders by purpose. This index is the entry point — start here.

---

## [01-planning-and-scope/](01-planning-and-scope/)
Core scope, architecture, and resourcing — the living plan the rest of the project traces back to.

- [FYP_Scope_CCP_and_Implementation_Plan.md](01-planning-and-scope/FYP_Scope_CCP_and_Implementation_Plan.md) — the index document for the whole project: scope, CCP rating, implementation plan
- [architecture-sketch.md](01-planning-and-scope/architecture-sketch.md) — one-page system architecture sketch
- [datasets.md](01-planning-and-scope/datasets.md) — datasets used/considered, licensing, access notes
- [resources.md](01-planning-and-scope/resources.md) — compute, models, tooling, and cost resourcing

## [02-evidence-and-tracking/](02-evidence-and-tracking/)
Ongoing project bookkeeping — risk, AI-usage, and compliance records.

- [risk-register.md](02-evidence-and-tracking/risk-register.md) — RAID register (risks, assumptions, issues, dependencies)
- [AI_Usage_Log.md](02-evidence-and-tracking/AI_Usage_Log.md) — AI usage log across the project
- [Guide_Compliance_Audit.md](02-evidence-and-tracking/Guide_Compliance_Audit.md) — audit against the FAST FYP guide's requirements

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
Supervisor- and panel-facing deliverables, including the two Python generator scripts and their outputs.

- [FYP_Registration_Form_Answers.md](05-deliverables/FYP_Registration_Form_Answers.md) — official FYP registration form answers
- [Proposal_Defense_Package.md](05-deliverables/Proposal_Defense_Package.md) — proposal defense slide-by-slide package
- [Supervisor_Briefing.md](05-deliverables/Supervisor_Briefing.md) — plain-language condensed briefing for the supervisor meeting
- [generate_supervisor_pdf.py](05-deliverables/generate_supervisor_pdf.py) — generator script for `Granite_Supervisor_Briefing.pdf` (run from within this folder)
- [generate_ccp_docx.py](05-deliverables/generate_ccp_docx.py) — generator script for `Granite_CCP_Justification.docx` (run from within this folder)
- `Granite_Supervisor_Briefing.pdf` — generated 12-section supervisor briefing (output of `generate_supervisor_pdf.py`)
- `Granite_CCP_Justification.docx` — generated CCP justification document (output of `generate_ccp_docx.py`)

## [06-archive-superseded/](06-archive-superseded/)
Earlier, since-narrowed drafts kept for history — not live spec, not to be updated.

- [TraceCause_AgentTestLab_Pitch.md](06-archive-superseded/TraceCause_AgentTestLab_Pitch.md) — the original, un-scoped ~10-layer "AgentTestLab" pitch, frozen intentionally
- [TraceCause_Product_Vision_UI.md](06-archive-superseded/TraceCause_Product_Vision_UI.md) — aspirational "Mission Control Center" UI vision, not part of the FYP scope

---

*Maintained as the entry point to `markdowns/`. When adding a new file, file it under the closest-matching subfolder above and add a line here.*
