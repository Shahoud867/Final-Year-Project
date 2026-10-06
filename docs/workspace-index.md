# Workspace index (generated)

Generated 2026-10-06 by `python scripts/build_index.py`. **Do not edit by hand.** One line per file (path and title); `data/raw/` is summarised per dataset. Layout and naming rules: [`workspace-guide.md`](workspace-guide.md). Old paths: [`archive/migration-map_2026-10-06.tsv`](../archive/migration-map_2026-10-06.tsv).

Entries: 217

## (repository root)

| Path | Title / description |
|---|---|
| `.gitignore` |  |
| `CLAUDE.md` | Orientation for AI sessions |
| `README.md` | Granite (F26-060) |

## docs  (active)

| Path | Title / description |
|---|---|
| `docs/adr/adr-000-template.md` | ADR-000: <short decision title> |
| `docs/adr/README.md` | docs/adr: architecture decision records |
| `docs/diagrams/README.md` | docs/diagrams |
| `docs/manuals/README.md` | docs/manuals |
| `docs/meetings/README.md` | docs/meetings |
| `docs/plan/master-plan.md` | Granite — FYP Master Execution Plan |
| `docs/registers/ai-usage-log.md` | AI Usage Log — Granite |
| `docs/registers/form-13-genai-disclosure.md` | Form 13 — External Tool / API / GenAI Disclosure Sheet |
| `docs/registers/README.md` | docs/registers |
| `docs/registers/risk-register.md` | Granite — RAID Register (Risks, Assumptions, Issues, Dependencies) |
| `docs/report/.gitignore` |  |
| `docs/report/README.md` | docs/report: report sources (LaTeX) |
| `docs/workspace-guide.md` | Granite Workspace Guide |

## research  (active)

| Path | Title / description |
|---|---|
| `research/eval/README.md` | research/eval |
| `research/literature/errorprobe-baseline-selection.md` | Why ErrorProbe Is the Selected SOTA Baseline |
| `research/literature/literature-landscape-analysis.md` | Multi-Agent Failure Attribution — Full Literature Landscape |
| `research/literature/literature-review-sheet.xlsx` |  |
| `research/literature/paper-release-timeline.md` | Multi-Agent Failure Attribution — Release Timeline (Most Recent → Oldest) |
| `research/market/agentic-ai-market-survey-integration.md` | Agentic AI Market Survey — Full Content, and Integration Audit |
| `research/market/commercial-product-comparison.md` | Commercial Product & Prior-FYP Comparison — Granite vs. the Existing Market and Department Archive |
| `research/README.md` | research |
| `research/spikes/poc-spike-outputs-full.md` | Granite — Full POC Spike Outputs, With Reasoning |
| `research/spikes/poc_spike1_errorprobe_repro.py` | POC Spike 1 -- reproduce ErrorProbe's methodology (simplified) against a small |
| `research/spikes/poc_spike1_errorprobe_repro_output.json` |  |
| `research/spikes/poc_spike1_multirun_runner.py` | Runs poc_spike1_errorprobe_repro.py N more times (as a subprocess, unmodified), |
| `research/spikes/poc_spike1_multirun_summary.json` |  |
| `research/spikes/poc_spike1_rescore.py` | Rescores the 5 already-collected real Spike 1 runs (poc_spike1_run{1..5} |
| `research/spikes/poc_spike1_run1_output.json` |  |
| `research/spikes/poc_spike1_run2_output.json` |  |
| `research/spikes/poc_spike1_run3_output.json` |  |
| `research/spikes/poc_spike1_run4_output.json` |  |
| `research/spikes/poc_spike1_run5_output.json` |  |
| `research/spikes/poc_spike2_crewai_toy.py` | POC Spike 2 — instrument one toy multi-agent workflow in CrewAI. |
| `research/spikes/poc_spike2_trace_output.json` |  |
| `research/spikes/poc_spike3_fault_injection.py` | POC Spike 3 — inject one controlled fault into the toy CrewAI workflow and |
| `research/spikes/poc_spike3_fault_injection_output.json` |  |
| `research/spikes/poc_spike3b_fault_injection_v2.py` | POC Spike 3, take 2 -- fixes the two problems the first run surfaced: |
| `research/spikes/poc_spike3b_output.json` |  |
| `research/spikes/poc_spike4_silent_failure_detector.py` | POC Spike 4 -- the one that was actually missing: does a rule-based |
| `research/spikes/poc_spike4_silent_failure_output.json` |  |
| `research/spikes/poc_spike4b_mechanism_output.json` |  |
| `research/spikes/poc_spike4b_mechanism_test.py` | POC Spike 4b -- the direct mechanism test, committed. |
| `research/spikes/poc_spike5_counterfactual_replay.py` | POC Spike 5 — Counterfactual replay engine (minimal mechanism test) |
| `research/spikes/poc_spike5_output.json` |  |
| `research/spikes/poc_spike6_cyclic_graph.py` | POC Spike 6 — Cyclic/dynamic graph support (extension #3 in the frozen 14) |
| `research/spikes/poc_spike6_output.json` |  |
| `research/spikes/poc_spike7_output.json` |  |
| `research/spikes/poc_spike7_preventive_classifier.py` | POC Spike 7 — Preventive clarification classifier (extension #5 in the frozen 14) |
| `research/spikes/poc_spike8_output.json` |  |
| `research/spikes/poc_spike8_repair_agent.py` | POC Spike 8 -- Repair Agent (minimal generation test) |
| `research/spikes/README.md` | Research: proposal-stage spikes |
| `research/spikes/silent-failure-detection-strategies.md` | Silent-Failure Detection Implementation & General Multi-Agent Testing Strategies |
| `research/spikes/whowhen_data/1.json` |  |
| `research/spikes/whowhen_data/2.json` |  |
| `research/spikes/whowhen_data/3.json` |  |
| `research/spikes/whowhen_data/4.json` |  |
| `research/spikes/whowhen_data/5.json` |  |
| `research/spikes/whowhen_data/6.json` |  |
| `research/spikes/whowhen_data/7.json` |  |
| `research/spikes/whowhen_data/8.json` |  |

## data  (active (raw/ read-only))

| Path | Title / description |
|---|---|
| `data/datasets.md` | Granite — Datasets |
| `data/DOWNLOAD.md` | Datasets — provenance, licensing, and retrieval |
| `data/raw/agentracer_full/` | third-party dataset: 871 files, 18.4 MB (not listed per file) |
| `data/raw/gaia_official/` | third-party dataset: 7 files, 0.3 MB (not listed per file) |
| `data/raw/gsm8k/` | third-party dataset: 2 files, 2.7 MB (not listed per file) |
| `data/raw/math/` | third-party dataset: 2 files, 4.8 MB (not listed per file) |
| `data/raw/mbppplus/` | third-party dataset: 4 files, 4.8 MB (not listed per file) |
| `data/raw/taubench_retail/` | third-party dataset: 33 files, 3.3 MB (not listed per file) |
| `data/raw/whowhen_full/` | third-party dataset: 200 files, 10.9 MB (not listed per file) |
| `data/README.md` | data |

## apps  (active (code))

| Path | Title / description |
|---|---|
| `apps/README.md` | apps |

## packages  (active (code))

| Path | Title / description |
|---|---|
| `packages/README.md` | packages |

## workflows  (active (code))

| Path | Title / description |
|---|---|
| `workflows/README.md` | workflows |

## tests  (active (code))

| Path | Title / description |
|---|---|
| `tests/README.md` | tests |

## scripts  (active (code))

| Path | Title / description |
|---|---|
| `scripts/apply_workspace_migration.py` | Apply the 2026-10-06 workspace migration. Idempotent and non-destructive. |
| `scripts/build_index.py` | Regenerate docs/workspace-index.md: one line per file (path and title), grouped by top-level folder. |
| `scripts/check_links.py` | Check that relative links in Markdown (and plain href/src in HTML) point at files that exist. |
| `scripts/check_workspace.py` | Check the workspace against docs/workspace-guide.md. |
| `scripts/linkcheck-allowlist.txt` |  |
| `scripts/README.md` | scripts |

## references  (read-only reference)

| Path | Title / description |
|---|---|
| `references/market/agentic-ai-market-survey-bs-fyp.docx` |  |
| `references/papers/2025_icml_whowhen.pdf` |  |
| `references/papers/2026_aaai_sdbl.pdf` |  |
| `references/papers/2026_acl-demo_protea.pdf` |  |
| `references/papers/2026_acl-findings_errorprobe.pdf` |  |
| `references/papers/2026_acl-long_agentask.pdf` |  |
| `references/papers/2026_acl-long_traceelephant.pdf` |  |
| `references/papers/2026_iclr_agentracer.pdf` |  |
| `references/papers/README.md` | references/papers |
| `references/README.md` | references |
| `references/templates/fyp1-mid-report-template_latex.zip` |  |
| `references/templates/fyp1-mid-report-template_rendered.pdf` |  |
| `references/university/bs-fyp-handbook-2026-draft.pdf` |  |
| `references/university/fast-fyp-idea-selection-guide.pdf` |  |
| `references/university/fyp1-mid-assessment-guidelines-and-rubrics.pdf` |  |

## deliverables  (frozen records per stage)

| Path | Title / description |
|---|---|
| `deliverables/README.md` | deliverables |
| `deliverables/stage-0-proposal/ccp-justification/CCP_Characteristics_Not_On_Slide.md` | CCP Characteristics Not Shown on Slide 5 |
| `deliverables/stage-0-proposal/ccp-justification/generate_ccp_cheatsheet_pdf.py` | Generates Granite_CCP_Cheatsheet.pdf — a one-page, 9-card rehearsal |
| `deliverables/stage-0-proposal/ccp-justification/generate_ccp_docx.py` | Generates the Seoul Accord D.4.1 Complex Computing Problem justification |
| `deliverables/stage-0-proposal/ccp-justification/Granite_CCP_Cheatsheet.pdf` |  |
| `deliverables/stage-0-proposal/ccp-justification/Granite_CCP_Justification.docx` |  |
| `deliverables/stage-0-proposal/ccp-justification/Granite_CCP_Justification_Seoul_Accord.docx` |  |
| `deliverables/stage-0-proposal/defense-prep/CCP_and_Spikes_Full_Reasoning.md` | CCP, Spikes & Contribution — Full Panel-Defense Reasoning |
| `deliverables/stage-0-proposal/defense-prep/Full_Defense_Prep.docx` |  |
| `deliverables/stage-0-proposal/defense-prep/Full_Defense_Prep.pdf` |  |
| `deliverables/stage-0-proposal/defense-prep/Full_Defense_Speaking_Script_7to10min.md` | Full Defense Speaking Script — 7 to 10 Minutes |
| `deliverables/stage-0-proposal/defense-prep/Literature_Review_Panel_Narrative.md` | Literature Review — Workflow & Panel Narrative |
| `deliverables/stage-0-proposal/defense-prep/Slides_5_6_7_Speaking_Notes_Expanded.md` | Slides 5, 6, 7 — Expanded Speaking Notes |
| `deliverables/stage-0-proposal/design-visuals/Granite_Architecture_Atlas.html` | Granite Architecture Atlas |
| `deliverables/stage-0-proposal/design-visuals/Granite_Pipeline_Diagram.png` |  |
| `deliverables/stage-0-proposal/design-visuals/Granite_Wireframes.html` | Granite Wireframe Set |
| `deliverables/stage-0-proposal/design-visuals/Granite_Wireframes_2.html` | Granite High-Fidelity Mockups |
| `deliverables/stage-0-proposal/poc-canvas/Granite_Interactive_PoC.html` | Granite — Interactive PoC |
| `deliverables/stage-0-proposal/poc-canvas/Granite_PoC_canvas_export.html` | Granite PoC |
| `deliverables/stage-0-proposal/poc-console/.gitignore` |  |
| `deliverables/stage-0-proposal/poc-console/backend/data_loader.py` | Granite proposal-defense PoC — data loader. |
| `deliverables/stage-0-proposal/poc-console/backend/main.py` | Granite proposal-defense PoC backend. |
| `deliverables/stage-0-proposal/poc-console/backend/requirements.txt` |  |
| `deliverables/stage-0-proposal/poc-console/backend/scope_data.py` | Scope, status, and product-journey data for the Granite PoC console. |
| `deliverables/stage-0-proposal/poc-console/frontend/.gitignore` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/index.html` | Granite — Diagnosis Console |
| `deliverables/stage-0-proposal/poc-console/frontend/package-lock.json` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/package.json` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/public/onclick-demo/index.html` | Granite — Live System Demonstration |
| `deliverables/stage-0-proposal/poc-console/frontend/src/api.ts` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/App.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/components/EvidencePanel.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/components/GraphView.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/components/RepairReplayReport.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/components/RunsAggregate.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/components/RunsTable.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/components/Sidebar.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/components/States.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/components/StatTile.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/components/StatusBadge.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/main.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/pages/Evidence.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/pages/LiveDemo.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/pages/Overview.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/pages/ProductVision.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/pages/RunDetail.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/pages/RunsList.tsx` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/staticData.json` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/styles/global.css` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/types.ts` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/src/vite-env.d.ts` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/tsconfig.json` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/vite.config.static.ts` |  |
| `deliverables/stage-0-proposal/poc-console/frontend/vite.config.ts` |  |
| `deliverables/stage-0-proposal/poc-console/index.html` | Granite — Diagnosis Console |
| `deliverables/stage-0-proposal/poc-console/README.md` | Granite — Proposal-Defense PoC (Diagnosis Console) |
| `deliverables/stage-0-proposal/proposal-deck/.gitignore` |  |
| `deliverables/stage-0-proposal/proposal-deck/add_transitions_v2.js` |  |
| `deliverables/stage-0-proposal/proposal-deck/assets_console_thumb.png` |  |
| `deliverables/stage-0-proposal/proposal-deck/diagram1_cropped.png` |  |
| `deliverables/stage-0-proposal/proposal-deck/diagram4_cropped.png` |  |
| `deliverables/stage-0-proposal/proposal-deck/diagram7_cropped.png` |  |
| `deliverables/stage-0-proposal/proposal-deck/generate_proposal_deck.js` |  |
| `deliverables/stage-0-proposal/proposal-deck/generate_proposal_deck_v2.js` |  |
| `deliverables/stage-0-proposal/proposal-deck/generate_speaking_notes_pdf.py` | Generates Granite_Speaking_Notes_and_QA.pdf — a rehearsal-ready speaking-notes |
| `deliverables/stage-0-proposal/proposal-deck/Granite_Proposal_Defense.pptx` |  |
| `deliverables/stage-0-proposal/proposal-deck/Granite_Proposal_Defense_v2.pptx` |  |
| `deliverables/stage-0-proposal/proposal-deck/Granite_Speaking_Notes_and_QA.pdf` |  |
| `deliverables/stage-0-proposal/proposal-deck/Proposal_Defense_Package.md` | Granite — Proposal Defense Package (Guide §16) |
| `deliverables/stage-0-proposal/proposal-deck/Proposal_Defense_Slide_Content_Spec.md` | Granite — Proposal Defense Slide Content Specification |
| `deliverables/stage-0-proposal/proposal-documents/architecture-sketch.md` | Granite — One-Page Architecture Sketch |
| `deliverables/stage-0-proposal/proposal-documents/cost-estimate.md` | Granite — API Cost Estimate and Model Plan |
| `deliverables/stage-0-proposal/proposal-documents/diagrams/SSD1_Submit_Trace_and_Diagnose.svg` |  |
| `deliverables/stage-0-proposal/proposal-documents/diagrams/SSD2_Generate_and_Verify_Repair.svg` |  |
| `deliverables/stage-0-proposal/proposal-documents/diagrams/SSD3_Review_Diagnosis_Dashboard.svg` |  |
| `deliverables/stage-0-proposal/proposal-documents/diagrams/Use_Case_Diagram.svg` |  |
| `deliverables/stage-0-proposal/proposal-documents/FYP_Scope_CCP_and_Implementation_Plan.md` | Granite — FYP Scope, CCP Rating, and Implementation Plan |
| `deliverables/stage-0-proposal/proposal-documents/Granite_FYP_Idea_OnePage.md` | The One-Page FYP Idea Description (Official Format) |
| `deliverables/stage-0-proposal/proposal-documents/Project_Vision.md` | Granite — Project Vision |
| `deliverables/stage-0-proposal/proposal-documents/resources.md` | Granite — Resources |
| `deliverables/stage-0-proposal/proposal-documents/Software_Design_Specification.md` | Granite — Software Design Specification |
| `deliverables/stage-0-proposal/proposal-documents/Software_Development_Plan.md` | Granite — Software Development Plan |
| `deliverables/stage-0-proposal/proposal-documents/Software_Requirements_Specification.md` | Granite — Software Requirements Specification (SRS) |
| `deliverables/stage-0-proposal/proposal-documents/System_Sequence_Diagrams.md` | Granite — System Sequence Diagrams (SSDs) |
| `deliverables/stage-0-proposal/proposal-documents/Test_Plan.md` | Granite — Test Plan |
| `deliverables/stage-0-proposal/proposal-documents/Use_Case_Model.md` | Granite — Use Case Model |
| `deliverables/stage-0-proposal/README.md` | stage-0-proposal |
| `deliverables/stage-0-proposal/registration/FYP_Registration_Form_Answers.md` | Granite — FYP Registration Form Answers |
| `deliverables/stage-0-proposal/registration/Stream_Decision_Memo.docx` |  |
| `deliverables/stage-0-proposal/supervisor-briefing/generate_supervisor_pdf.py` | Generates a supervisor-shareable PDF briefing for Granite. |
| `deliverables/stage-0-proposal/supervisor-briefing/Granite_Supervisor_Briefing.pdf` |  |
| `deliverables/stage-0-proposal/supervisor-briefing/Supervisor_Briefing.md` | Supervisor Briefing — Granite |
| `deliverables/stage-1-fyp1-mid/README.md` | stage-1-fyp1-mid |
| `deliverables/stage-2-fyp1-final/README.md` | stage-2-fyp1-final |
| `deliverables/stage-3-fyp2-mid/README.md` | stage-3-fyp2-mid |
| `deliverables/stage-4-fyp2-final/README.md` | stage-4-fyp2-final |

## evidence  (append-only)

| Path | Title / description |
|---|---|
| `evidence/.gitignore` |  |
| `evidence/README.md` | evidence |

## archive  (history)

| Path | Title / description |
|---|---|
| `archive/migration-map_2026-10-06.tsv` |  |
| `archive/pre-granite/TraceCause_AgentTestLab_Pitch.md` | Granite / Agent Autopsy 2.0 / AgentTestLab — Pasted Pitch |
| `archive/pre-granite/TraceCause_Product_Vision_UI.md` | Granite — Full Product Vision ("Mission Control Center" UI) |
| `archive/proposal-phase/audits/01_Executive_Audit_and_Verdict.md` | Granite — Independent Critical Audit and Verdict |
| `archive/proposal-phase/audits/02_Panel_Defense_Question_Bank.md` | Granite — Adversarial Rejection Attempt + Panel Defense Bank |
| `archive/proposal-phase/audits/03_Proposal_Slides_with_Speaker_Notes.md` | Granite — Proposal Defense Deck (10 slides, guide §16 order) |
| `archive/proposal-phase/audits/04_Granite_Knowledge_Base.md` | Granite — Layman-to-Expert Knowledge Base |
| `archive/proposal-phase/audits/05_Repository_Change_and_Commit_Plan.md` | Granite — Repository Change and Commit Plan |
| `archive/proposal-phase/audits/06_Expanded_Scope_and_Feasibility_Plan.md` | Granite — Expanded Scope and Feasibility Plan |
| `archive/proposal-phase/audits/07_Handbook_2026_Compliance_Audit_and_Response.md` | Granite — Handbook (2026, 3rd Edition DRAFT) Compliance Audit & Strategic Response |
| `archive/proposal-phase/explanations/explanation.md` | Complete FYP Guide & Architectural Reconstitution: Project Granite |
| `archive/proposal-phase/explanations/Granite_Full_Project_Explanation.md` | Granite — Full Project Explanation |
| `archive/proposal-phase/tracking/Guide_Compliance_Audit.md` | Granite — Full Sub-Part Compliance Audit vs. FAST FYP Guide (all 30 pages, all 17 sections + Annex A/C) |
| `archive/proposal-phase/tracking/markdowns-index_pre-reorg.md` | Granite — Documentation Index |
| `archive/proposal-phase/tracking/Pre_Defense_Checklist.md` | Pre-Defense Checklist — Compiled from AI_Usage_Log.md |
| `archive/proposal-phase/tracking/Team_Action_Items.md` | Team Action Items — Human-Only, Before Defense |
| `archive/proposal-phase/tracking/Traceability_Matrix.md` | Granite — Traceability Matrix & Final Consistency Audit |
| `archive/README.md` | archive |
| `archive/superseded/AgenTracer_vs_WhoWhen_Analysis.md` | Who&When vs. AgenTracer — Overlap, Novelty, and FYP Feasibility Analysis |
| `archive/superseded/master-plan_v1.0_2026-10-04.md` | Granite — FYP Master Execution Plan |

## .claude  (tool configuration)

| Path | Title / description |
|---|---|
| `.claude/launch.json` |  |
