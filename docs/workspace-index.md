# Workspace index (generated)

Generated 2026-10-07 by `python scripts/build_index.py`. **Do not edit by hand.** One line per file (path and title); `data/raw/` is summarised per dataset. Layout and naming rules: [`workspace-guide.md`](workspace-guide.md). Old paths: [`archive/migration-map_2026-10-06.tsv`](../archive/migration-map_2026-10-06.tsv).

Entries: 611

## (repository root)

| Path | Title / description |
|---|---|
| `.dockerignore` |  |
| `.env.example` |  |
| `.gitignore` |  |
| `CLAUDE.md` | Orientation for AI sessions |
| `docker-compose.yml` |  |
| `Dockerfile` |  |
| `README.md` | Granite (F26-060) |

## docs  (active)

| Path | Title / description |
|---|---|
| `docs/adr/adr-000-template.md` | ADR-000: <short decision title> |
| `docs/adr/adr-001-modular-monolith.md` | ADR-001: One repository, a framework-free core library and thin application layers |
| `docs/adr/adr-002-own-runner-first.md` | ADR-002: Build a small workflow runner before adopting an agent framework |
| `docs/adr/adr-003-persistence-sqlalchemy.md` | ADR-003: SQLAlchemy with SQLite by default and PostgreSQL by connection string |
| `docs/adr/adr-004-ast-check-dsl.md` | ADR-004: Checks are written in a small expression language evaluated over a restricted syntax tree |
| `docs/adr/adr-005-provenance-first-attribution.md` | ADR-005: Rank where a failure began from recorded data flow first, structure second |
| `docs/adr/adr-006-vr1-verdict-rule.md` | ADR-006: Decide verification verdicts with a fixed, published rule (VR-1) |
| `docs/adr/adr-007-free-hosting-render.md` | ADR-007: Host the public demo on a free web-service tier |
| `docs/adr/adr-008-llm-provider-and-recorded-mode.md` | ADR-008: Language models sit behind one interface, and every answer can be recorded and replayed |
| `docs/adr/adr-009-trace-schema-v1.md` | ADR-009: One versioned trace format for every run, replay and import |
| `docs/adr/adr-010-git-branching.md` | ADR-010: Work on short-lived branches, review every change, release from main |
| `docs/adr/README.md` | docs/adr: architecture decision records |
| `docs/diagrams/architecture.md` | Architecture |
| `docs/diagrams/database-schema.md` | Database schema |
| `docs/diagrams/finding-state-machine.md` | Finding state machine |
| `docs/diagrams/README.md` | docs/diagrams |
| `docs/diagrams/refund-desk-dataflow.md` | Refund Desk data flow |
| `docs/diagrams/verification-sequence.md` | Verification sequence |
| `docs/manuals/README.md` | docs/manuals |
| `docs/manuals/setup-manual.md` | Setup manual |
| `docs/manuals/tool-manual.md` | Tool manual: using Granite |
| `docs/meetings/README.md` | docs/meetings |
| `docs/plan/execution-status.md` | Execution status |
| `docs/plan/master-plan.md` | Granite — FYP Master Execution Plan |
| `docs/plan/requirements-trace.json` |  |
| `docs/plan/requirements-trace.md` | Requirements traceability (functional requirements, Mid-1) |
| `docs/registers/ai-usage-log.md` | AI Usage Log — Granite |
| `docs/registers/change-log.md` | Change log |
| `docs/registers/defect-list.md` | Defect list |
| `docs/registers/dependency-licence-register.md` | Dependency and licence register |
| `docs/registers/deployment-record.md` | Deployment record |
| `docs/registers/form-10-panel-actions.md` | Panel action register (A1 to A6) |
| `docs/registers/form-13-genai-disclosure.md` | Form 13 — External Tool / API / GenAI Disclosure Sheet |
| `docs/registers/milestone-log.md` | Milestone log |
| `docs/registers/README.md` | docs/registers |
| `docs/registers/risk-register.md` | Granite — RAID Register (Risks, Assumptions, Issues, Dependencies) |
| `docs/report/.gitignore` |  |
| `docs/report/README.md` | docs/report: report sources (LaTeX) |
| `docs/workspace-guide.md` | Granite Workspace Guide |

## research  (active)

| Path | Title / description |
|---|---|
| `research/eval/prereg-v1.md` | Pre-registration v1: Refund Desk feasibility validation |
| `research/eval/README.md` | research/eval |
| `research/eval/results/2026-10-07_refund-desk-feasibility-notes.md` | Refund Desk feasibility validation: results and how to read them |
| `research/eval/results/2026-10-07_refund-desk-feasibility.json` |  |
| `research/eval/results/2026-10-07_refund-desk-feasibility.md` | Refund Desk feasibility validation, 2026-10-07 |
| `research/eval/results/run.log` |  |
| `research/eval/validate_refund_desk.py` | Mid-1 feasibility validation of Granite on Refund Desk. Protocol: research/eval/prereg-v1.md (read it first). |
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
| `data/cassettes/record.log` |  |
| `data/cassettes/refund_desk_v1.json` |  |
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
| `data/seed/taubench_retail_v1/LICENSE.txt` |  |
| `data/seed/taubench_retail_v1/orders.json` |  |
| `data/seed/taubench_retail_v1/products.json` |  |
| `data/seed/taubench_retail_v1/README.md` | taubench_retail_v1 (truth snapshot) |
| `data/seed/taubench_retail_v1/users.json` |  |

## apps  (active (code))

| Path | Title / description |
|---|---|
| `apps/api/.coverage` |  |
| `apps/api/.gitignore` |  |
| `apps/api/.mypy_cache/.gitignore` |  |
| `apps/api/.mypy_cache/3.11/cache.0.db` |  |
| `apps/api/.mypy_cache/3.11/cache.1.db` |  |
| `apps/api/.mypy_cache/3.11/cache.10.db` |  |
| `apps/api/.mypy_cache/3.11/cache.11.db` |  |
| `apps/api/.mypy_cache/3.11/cache.12.db` |  |
| `apps/api/.mypy_cache/3.11/cache.13.db` |  |
| `apps/api/.mypy_cache/3.11/cache.14.db` |  |
| `apps/api/.mypy_cache/3.11/cache.15.db` |  |
| `apps/api/.mypy_cache/3.11/cache.2.db` |  |
| `apps/api/.mypy_cache/3.11/cache.3.db` |  |
| `apps/api/.mypy_cache/3.11/cache.4.db` |  |
| `apps/api/.mypy_cache/3.11/cache.5.db` |  |
| `apps/api/.mypy_cache/3.11/cache.6.db` |  |
| `apps/api/.mypy_cache/3.11/cache.7.db` |  |
| `apps/api/.mypy_cache/3.11/cache.8.db` |  |
| `apps/api/.mypy_cache/3.11/cache.9.db` |  |
| `apps/api/.mypy_cache/CACHEDIR.TAG` |  |
| `apps/api/.pytest_cache/.gitignore` |  |
| `apps/api/.pytest_cache/CACHEDIR.TAG` |  |
| `apps/api/.pytest_cache/README.md` | pytest cache directory # |
| `apps/api/.pytest_cache/v/cache/lastfailed` |  |
| `apps/api/.pytest_cache/v/cache/nodeids` |  |
| `apps/api/.ruff_cache/.gitignore` |  |
| `apps/api/.ruff_cache/0.16.10/1268613837147474529` |  |
| `apps/api/.ruff_cache/0.16.10/9005716141011272895` |  |
| `apps/api/.ruff_cache/0.16.10/9398265696974144633` |  |
| `apps/api/.ruff_cache/CACHEDIR.TAG` |  |
| `apps/api/build/lib/granite_api/__init__.py` | Granite application layer: HTTP API, persistence and background jobs around granite_core. |
| `apps/api/build/lib/granite_api/config.py` | Runtime configuration, read once from environment variables (twelve-factor). No secrets have defaults. |
| `apps/api/build/lib/granite_api/db.py` | Engine and session factory. SQLite by default; any SQLAlchemy URL (e.g. PostgreSQL) works. |
| `apps/api/build/lib/granite_api/errors.py` | RFC 7807 problem responses: every error the API returns has the same shape and never leaks internals. |
| `apps/api/build/lib/granite_api/jobs.py` | Background jobs: a small thread pool with a persisted job row for progress and crash recovery. |
| `apps/api/build/lib/granite_api/llm_factory.py` | Choose how model answers are produced: live (Ollama or a hosted endpoint) or recorded (saved answers). |
| `apps/api/build/lib/granite_api/main.py` | Application factory: wires settings, database, job runner, middleware and routes. |
| `apps/api/build/lib/granite_api/models.py` | Database tables (master plan 14.6). Evidence and audit rows are append-only: the API has no update path. |
| `apps/api/build/lib/granite_api/providers.py` | Network LLM providers (infrastructure layer): Ollama and any OpenAI-compatible endpoint. |
| `apps/api/build/lib/granite_api/registry.py` | Workflows the API can run. Adding a workflow means adding one entry here (the core stays unchanged). |
| `apps/api/build/lib/granite_api/routes.py` | HTTP endpoints. Handlers stay thin: validation here, behaviour in services. |
| `apps/api/build/lib/granite_api/schemas.py` | Request and response models (they also drive the OpenAPI documentation at /docs). |
| `apps/api/build/lib/granite_api/services/__init__.py` |  |
| `apps/api/build/lib/granite_api/services/analysis.py` | After a run: persist the trace, run the checks, open findings, rank origin hypotheses, record evidence. |
| `apps/api/build/lib/granite_api/services/common.py` | Shared persistence helpers: evidence, audit log, finding transitions. |
| `apps/api/build/lib/granite_api/services/experiments.py` | Verification experiments: replay from a hypothesised step with and without the fix, decide with VR-1. |
| `apps/api/build/lib/granite_api/services/report.py` | A plain-text investigation report for one finding (Markdown), built only from stored records. |
| `apps/api/build/lib/granite_api/services/reviews.py` | Human review: the analyst accepts or rejects a finding and closes it. Every decision is recorded. |
| `apps/api/build/lib/granite_api/services/runs.py` | Create runs and execute them in the background. |
| `apps/api/build/lib/granite_api/views.py` | Turn database rows into API response objects (derived fields live here, not in the tables). |
| `apps/api/granite_api.egg-info/dependency_links.txt` |  |
| `apps/api/granite_api.egg-info/PKG-INFO` |  |
| `apps/api/granite_api.egg-info/requires.txt` |  |
| `apps/api/granite_api.egg-info/SOURCES.txt` |  |
| `apps/api/granite_api.egg-info/top_level.txt` |  |
| `apps/api/granite_api/__init__.py` | Granite application layer: HTTP API, persistence and background jobs around granite_core. |
| `apps/api/granite_api/config.py` | Runtime configuration, read once from environment variables (twelve-factor). No secrets have defaults. |
| `apps/api/granite_api/db.py` | Engine and session factory. SQLite by default; any SQLAlchemy URL (e.g. PostgreSQL) works. |
| `apps/api/granite_api/errors.py` | RFC 7807 problem responses: every error the API returns has the same shape and never leaks internals. |
| `apps/api/granite_api/jobs.py` | Background jobs: a small thread pool with a persisted job row for progress and crash recovery. |
| `apps/api/granite_api/llm_factory.py` | Choose how model answers are produced: live (Ollama or a hosted endpoint) or recorded (saved answers). |
| `apps/api/granite_api/main.py` | Application factory: wires settings, database, job runner, middleware and routes. |
| `apps/api/granite_api/models.py` | Database tables (master plan 14.6). Evidence and audit rows are append-only: the API has no update path. |
| `apps/api/granite_api/providers.py` | Network LLM providers (infrastructure layer): Ollama and any OpenAI-compatible endpoint. |
| `apps/api/granite_api/registry.py` | Workflows the API can run. Adding a workflow means adding one entry here (the core stays unchanged). |
| `apps/api/granite_api/routes.py` | HTTP endpoints. Handlers stay thin: validation here, behaviour in services. |
| `apps/api/granite_api/schemas.py` | Request and response models (they also drive the OpenAPI documentation at /docs). |
| `apps/api/granite_api/services/__init__.py` |  |
| `apps/api/granite_api/services/analysis.py` | After a run: persist the trace, run the checks, open findings, rank origin hypotheses, record evidence. |
| `apps/api/granite_api/services/common.py` | Shared persistence helpers: evidence, audit log, finding transitions. |
| `apps/api/granite_api/services/experiments.py` | Verification experiments: replay from a hypothesised step with and without the fix, decide with VR-1. |
| `apps/api/granite_api/services/report.py` | A plain-text investigation report for one finding (Markdown), built only from stored records. |
| `apps/api/granite_api/services/reviews.py` | Human review: the analyst accepts or rejects a finding and closes it. Every decision is recorded. |
| `apps/api/granite_api/services/runs.py` | Create runs and execute them in the background. |
| `apps/api/granite_api/views.py` | Turn database rows into API response objects (derived fields live here, not in the tables). |
| `apps/api/pyproject.toml` |  |
| `apps/api/README.md` | granite_api |
| `apps/api/tests/__init__.py` |  |
| `apps/api/tests/conftest.py` | API test fixtures. Tests run in recorded mode on the committed cassette: deterministic, no model needed. |
| `apps/api/tests/test_journeys.py` | End-to-end journeys through the HTTP API (SYS-CORE J1/J2): run, detect, trace, verify, review, report. |
| `apps/api/tests/test_platform.py` | Validation, errors, security, resilience (SYS-ERR, NFR-SEC, NFR-REL). |
| `apps/api/tests/test_providers.py` | Live model providers against a local stub server (no real model needed). |
| `apps/api/tests/test_requirements.py` | Acceptance criteria of the Mid-1 functional requirements (master plan section 15), one test per requirement. |
| `apps/README.md` | apps |
| `apps/web/.gitignore` |  |
| `apps/web/eslint.config.js` |  |
| `apps/web/index.html` | Granite |
| `apps/web/package-lock.json` |  |
| `apps/web/package.json` |  |
| `apps/web/README.md` | web |
| `apps/web/src/api.ts` |  |
| `apps/web/src/App.tsx` |  |
| `apps/web/src/components/Filters.tsx` |  |
| `apps/web/src/components/Graph.tsx` |  |
| `apps/web/src/components/Outcome.tsx` |  |
| `apps/web/src/components/ui.tsx` |  |
| `apps/web/src/components/Verify.tsx` |  |
| `apps/web/src/format.ts` |  |
| `apps/web/src/hooks.ts` |  |
| `apps/web/src/main.tsx` |  |
| `apps/web/src/pages/FindingDetail.tsx` |  |
| `apps/web/src/pages/Home.tsx` |  |
| `apps/web/src/pages/NewRun.tsx` |  |
| `apps/web/src/pages/RunDetail.tsx` |  |
| `apps/web/src/styles.css` |  |
| `apps/web/src/types.ts` |  |
| `apps/web/tests/a11y.test.tsx` |  |
| `apps/web/tests/finding.test.tsx` |  |
| `apps/web/tests/helpers.ts` |  |
| `apps/web/tests/pages.test.tsx` |  |
| `apps/web/tests/requirements.test.tsx` |  |
| `apps/web/tests/setup.ts` |  |
| `apps/web/tests/unit.test.ts` |  |
| `apps/web/tsconfig.json` |  |
| `apps/web/vite.config.ts` |  |

## packages  (active (code))

| Path | Title / description |
|---|---|
| `packages/granite_core/.coverage` |  |
| `packages/granite_core/.hypothesis/.gitignore` |  |
| `packages/granite_core/.hypothesis/constants/020e895fd6a059b4` |  |
| `packages/granite_core/.hypothesis/constants/0bbbdc3240b67114` |  |
| `packages/granite_core/.hypothesis/constants/0ef890823c425a7c` |  |
| `packages/granite_core/.hypothesis/constants/2a910b6c34d606bf` |  |
| `packages/granite_core/.hypothesis/constants/3a76c03500cf6ef4` |  |
| `packages/granite_core/.hypothesis/constants/3d49abf751a4aeef` |  |
| `packages/granite_core/.hypothesis/constants/3f95b6cd9cc047e7` |  |
| `packages/granite_core/.hypothesis/constants/4492b90790a254bf` |  |
| `packages/granite_core/.hypothesis/constants/52b10e8994eec85e` |  |
| `packages/granite_core/.hypothesis/constants/5d3c6a64ac91e867` |  |
| `packages/granite_core/.hypothesis/constants/5fa806864b561dcf` |  |
| `packages/granite_core/.hypothesis/constants/62d0f744afb38256` |  |
| `packages/granite_core/.hypothesis/constants/63a4acdfbd5e8e3e` |  |
| `packages/granite_core/.hypothesis/constants/6485567c1222d2c4` |  |
| `packages/granite_core/.hypothesis/constants/7a35ee7ede7d1ced` |  |
| `packages/granite_core/.hypothesis/constants/7ba9f0d97ebf4e10` |  |
| `packages/granite_core/.hypothesis/constants/7c7c0c8174dd4fcc` |  |
| `packages/granite_core/.hypothesis/constants/7e3c026441916e54` |  |
| `packages/granite_core/.hypothesis/constants/8acb7798546ec761` |  |
| `packages/granite_core/.hypothesis/constants/8bf5f64806a4bdf5` |  |
| `packages/granite_core/.hypothesis/constants/97c3fe1be73ed427` |  |
| `packages/granite_core/.hypothesis/constants/a400ccb562c8f527` |  |
| `packages/granite_core/.hypothesis/constants/af5f99b2160918e9` |  |
| `packages/granite_core/.hypothesis/constants/b1a103582fbe5438` |  |
| `packages/granite_core/.hypothesis/constants/b7f605f97bb2c987` |  |
| `packages/granite_core/.hypothesis/constants/bb97c445387f61f2` |  |
| `packages/granite_core/.hypothesis/constants/bc3da858fe3b650a` |  |
| `packages/granite_core/.hypothesis/constants/bcd704d19fa66c84` |  |
| `packages/granite_core/.hypothesis/constants/bfb3523c69904364` |  |
| `packages/granite_core/.hypothesis/constants/c568580b452a98ed` |  |
| `packages/granite_core/.hypothesis/constants/ca0c5a85814efbd1` |  |
| `packages/granite_core/.hypothesis/constants/ceb13b2f3daa8d03` |  |
| `packages/granite_core/.hypothesis/constants/d37e5a8e268e283e` |  |
| `packages/granite_core/.hypothesis/constants/de0c498d4ef1db93` |  |
| `packages/granite_core/.hypothesis/constants/e9f9eb24bf363cba` |  |
| `packages/granite_core/.hypothesis/constants/ec851c84d5c7621b` |  |
| `packages/granite_core/.hypothesis/constants/f2223ac708804293` |  |
| `packages/granite_core/.hypothesis/constants/f3ff697dee19318c` |  |
| `packages/granite_core/.hypothesis/examples/04e6b3400353b141/7d0909f09d2bf1f5` |  |
| `packages/granite_core/.hypothesis/examples/04e6b3400353b141/df1b93c879a85422` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/1e8564ab213306ac` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/31584c90d73628a6` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/37470933fe877979` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/4451befc68619979` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/5180fde11d286015` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/653dd7da6c7619e3` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/6a9ff06428ccaafe` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/71676817b0fb0fd3` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/758dccf0a726be53` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/78998a20755b54b2` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/95f64473a0d9cce7` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/9745ea156c486e08` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/a0d5fc81a17d2719` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/cfe82c844ca15cac` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/d576c25b55e4d880` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/f212013e75285397` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/fce8fadca7e8e755` |  |
| `packages/granite_core/.hypothesis/examples/7d0909f09d2bf1f5/ff0ce391d22bdbdf` |  |
| `packages/granite_core/.hypothesis/examples/df1b93c879a85422/fe9bf3fc01789212` |  |
| `packages/granite_core/.hypothesis/tmp/tmp0jeles37` |  |
| `packages/granite_core/.hypothesis/tmp/tmpa29v7cpx` |  |
| `packages/granite_core/.hypothesis/tmp/tmpbgixarfu` |  |
| `packages/granite_core/.hypothesis/tmp/tmpfpjmdxav` |  |
| `packages/granite_core/.hypothesis/tmp/tmpfywdfl1u` |  |
| `packages/granite_core/.hypothesis/tmp/tmpihphwa9u` |  |
| `packages/granite_core/.hypothesis/tmp/tmpjgmz8m71` |  |
| `packages/granite_core/.hypothesis/tmp/tmplmcx_slk` |  |
| `packages/granite_core/.hypothesis/tmp/tmpnukno1to` |  |
| `packages/granite_core/.hypothesis/tmp/tmppfymygsh` |  |
| `packages/granite_core/.hypothesis/tmp/tmpqi1o6gdm` |  |
| `packages/granite_core/.hypothesis/tmp/tmprdzjc177` |  |
| `packages/granite_core/.hypothesis/tmp/tmprwwod5xx` |  |
| `packages/granite_core/.hypothesis/tmp/tmpsi9t9dw9` |  |
| `packages/granite_core/.hypothesis/tmp/tmpt1flvw8a` |  |
| `packages/granite_core/.hypothesis/tmp/tmpt5l4x68p` |  |
| `packages/granite_core/.hypothesis/tmp/tmpusaa32c7` |  |
| `packages/granite_core/.hypothesis/tmp/tmpuxtemasb` |  |
| `packages/granite_core/.hypothesis/tmp/tmpyhohe3ni` |  |
| `packages/granite_core/.hypothesis/unicode_data/14.0.0/charmap.json.gz` |  |
| `packages/granite_core/.hypothesis/unicode_data/14.0.0/codec-v2-utf-8.json.gz` |  |
| `packages/granite_core/.mypy_cache/.gitignore` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.0.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.1.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.10.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.11.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.12.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.13.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.14.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.15.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.2.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.3.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.4.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.5.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.6.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.7.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.8.db` |  |
| `packages/granite_core/.mypy_cache/3.11/cache.9.db` |  |
| `packages/granite_core/.mypy_cache/CACHEDIR.TAG` |  |
| `packages/granite_core/.pytest_cache/.gitignore` |  |
| `packages/granite_core/.pytest_cache/CACHEDIR.TAG` |  |
| `packages/granite_core/.pytest_cache/README.md` | pytest cache directory # |
| `packages/granite_core/.pytest_cache/v/cache/lastfailed` |  |
| `packages/granite_core/.pytest_cache/v/cache/nodeids` |  |
| `packages/granite_core/.ruff_cache/.gitignore` |  |
| `packages/granite_core/.ruff_cache/0.16.10/10731053879492683424` |  |
| `packages/granite_core/.ruff_cache/0.16.10/11616233939615180134` |  |
| `packages/granite_core/.ruff_cache/0.16.10/11701819773364907638` |  |
| `packages/granite_core/.ruff_cache/0.16.10/12394674784211129769` |  |
| `packages/granite_core/.ruff_cache/0.16.10/14839009929315258217` |  |
| `packages/granite_core/.ruff_cache/0.16.10/4178381786369584450` |  |
| `packages/granite_core/.ruff_cache/0.16.10/5248883725732258102` |  |
| `packages/granite_core/.ruff_cache/0.16.10/7358003054907178856` |  |
| `packages/granite_core/.ruff_cache/0.16.10/8145696949316050166` |  |
| `packages/granite_core/.ruff_cache/CACHEDIR.TAG` |  |
| `packages/granite_core/build/lib/granite_core/__init__.py` | Granite core: pure-Python library (no web, no database, no network). |
| `packages/granite_core/build/lib/granite_core/attribution.py` | Deterministic value-provenance attribution (master plan 21.4; FR-ATT-01/02). |
| `packages/granite_core/build/lib/granite_core/checks.py` | Checks engine: executable rules over a trace (FR-CHK-01..06). |
| `packages/granite_core/build/lib/granite_core/dsl.py` | Safe expression language for checks (ADR-004: AST whitelist, never ``eval``). |
| `packages/granite_core/build/lib/granite_core/evidence.py` | Evidence records: typed, hashed, append-only (master plan 14.5). |
| `packages/granite_core/build/lib/granite_core/experiment.py` | Verification experiment: N replays with the intervention, M controls without it (FR-VER-01..05, VR-1). |
| `packages/granite_core/build/lib/granite_core/lifecycle.py` | Finding lifecycle as a state machine (master plan 13.3; FR-REV-02). Illegal transitions raise. |
| `packages/granite_core/build/lib/granite_core/lineage.py` | Lineage graph over a trace: who read what from whom (derived from each step's ``reads``). |
| `packages/granite_core/build/lib/granite_core/llm.py` | LLM provider interface and the offline record/replay providers (master plan 21.2; FR-RUN-03/04). |
| `packages/granite_core/build/lib/granite_core/py.typed` |  |
| `packages/granite_core/build/lib/granite_core/redaction.py` | PII redaction before anything is stored (FR-SEC-01, NFR-08). Idempotent. |
| `packages/granite_core/build/lib/granite_core/runner.py` | Workflow runner: executes a workflow definition and records a Granite trace; re-executes for replay. |
| `packages/granite_core/build/lib/granite_core/trace.py` | Granite Trace v1: the input contract for runs, imports and the SDK (master plan 22.4). |
| `packages/granite_core/build/lib/granite_core/verification.py` | Controlled-replay verification, protocol VR-1 (master plan 14.4 and 21.5; FR-VER-01..04). |
| `packages/granite_core/granite_core.egg-info/dependency_links.txt` |  |
| `packages/granite_core/granite_core.egg-info/PKG-INFO` |  |
| `packages/granite_core/granite_core.egg-info/requires.txt` |  |
| `packages/granite_core/granite_core.egg-info/SOURCES.txt` |  |
| `packages/granite_core/granite_core.egg-info/top_level.txt` |  |
| `packages/granite_core/granite_core/__init__.py` | Granite core: pure-Python library (no web, no database, no network). |
| `packages/granite_core/granite_core/attribution.py` | Deterministic value-provenance attribution (master plan 21.4; FR-ATT-01/02). |
| `packages/granite_core/granite_core/checks.py` | Checks engine: executable rules over a trace (FR-CHK-01..06). |
| `packages/granite_core/granite_core/dsl.py` | Safe expression language for checks (ADR-004: AST whitelist, never ``eval``). |
| `packages/granite_core/granite_core/evidence.py` | Evidence records: typed, hashed, append-only (master plan 14.5). |
| `packages/granite_core/granite_core/experiment.py` | Verification experiment: N replays with the intervention, M controls without it (FR-VER-01..05, VR-1). |
| `packages/granite_core/granite_core/lifecycle.py` | Finding lifecycle as a state machine (master plan 13.3; FR-REV-02). Illegal transitions raise. |
| `packages/granite_core/granite_core/lineage.py` | Lineage graph over a trace: who read what from whom (derived from each step's ``reads``). |
| `packages/granite_core/granite_core/llm.py` | LLM provider interface and the offline record/replay providers (master plan 21.2; FR-RUN-03/04). |
| `packages/granite_core/granite_core/py.typed` |  |
| `packages/granite_core/granite_core/redaction.py` | PII redaction before anything is stored (FR-SEC-01, NFR-08). Idempotent. |
| `packages/granite_core/granite_core/runner.py` | Workflow runner: executes a workflow definition and records a Granite trace; re-executes for replay. |
| `packages/granite_core/granite_core/trace.py` | Granite Trace v1: the input contract for runs, imports and the SDK (master plan 22.4). |
| `packages/granite_core/granite_core/verification.py` | Controlled-replay verification, protocol VR-1 (master plan 14.4 and 21.5; FR-VER-01..04). |
| `packages/granite_core/pyproject.toml` |  |
| `packages/granite_core/README.md` | granite_core |
| `packages/granite_core/schema/granite-trace-v1.schema.json` |  |
| `packages/granite_core/tests/__init__.py` |  |
| `packages/granite_core/tests/conftest.py` | Shared fixtures: a small refund-style trace built by hand (no LLM), with a tiny source of truth. |
| `packages/granite_core/tests/test_attribution.py` | Provenance attribution: golden traces, clean runs, metamorphic invariances, determinism (TC-ATT-01..05). |
| `packages/granite_core/tests/test_dsl.py` | Check-expression language: behaviour, and the malicious-expression suite (TC-CHK-04, TC-CHK-SEC). |
| `packages/granite_core/tests/test_experiment.py` | Verification experiment orchestration on a toy workflow (TC-VER-01..05). |
| `packages/granite_core/tests/test_lifecycle_evidence_redaction_llm.py` | Lifecycle state machine (TC-REV-01), evidence hashing, redaction (TC-SEC-03), LLM cassettes. |
| `packages/granite_core/tests/test_runner.py` | Workflow runner: recorded inputs/lineage, faults, error handling, replay freezing (TC-RUN-01..04, TC-VER-03). |
| `packages/granite_core/tests/test_schema.py` | The published Granite Trace v1 schema must match the model; example traces must validate against it. |
| `packages/granite_core/tests/test_trace_and_checks.py` | Trace contract (TC-IMP) and checks engine (TC-CHK-01..06). |
| `packages/granite_core/tests/test_verification.py` | Verification protocol VR-1 (TC-VER-01..06): verdict decision table, CI, regression guard, replay planning. |
| `packages/README.md` | packages |

## workflows  (active (code))

| Path | Title / description |
|---|---|
| `workflows/README.md` | workflows |
| `workflows/refund_desk/.coverage` |  |
| `workflows/refund_desk/.mypy_cache/.gitignore` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.0.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.1.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.10.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.11.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.12.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.13.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.14.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.15.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.2.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.3.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.4.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.5.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.6.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.7.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.8.db` |  |
| `workflows/refund_desk/.mypy_cache/3.11/cache.9.db` |  |
| `workflows/refund_desk/.mypy_cache/CACHEDIR.TAG` |  |
| `workflows/refund_desk/.pytest_cache/.gitignore` |  |
| `workflows/refund_desk/.pytest_cache/CACHEDIR.TAG` |  |
| `workflows/refund_desk/.pytest_cache/README.md` | pytest cache directory # |
| `workflows/refund_desk/.pytest_cache/v/cache/lastfailed` |  |
| `workflows/refund_desk/.pytest_cache/v/cache/nodeids` |  |
| `workflows/refund_desk/.ruff_cache/.gitignore` |  |
| `workflows/refund_desk/.ruff_cache/0.16.10/3737181727954000509` |  |
| `workflows/refund_desk/.ruff_cache/0.16.10/5069954027938668190` |  |
| `workflows/refund_desk/.ruff_cache/0.16.10/7685517349561320950` |  |
| `workflows/refund_desk/.ruff_cache/CACHEDIR.TAG` |  |
| `workflows/refund_desk/build/lib/refund_desk/__init__.py` | Refund Desk: Granite's first system under test (master plan 21.3). |
| `workflows/refund_desk/build/lib/refund_desk/definition.py` | Refund Desk workflow definition: steps and their declared reads, checks, and repair rules. |
| `workflows/refund_desk/build/lib/refund_desk/faults.py` | Fault operators for Refund Desk. Faults are rule-based and deterministic: no LLM is involved. |
| `workflows/refund_desk/build/lib/refund_desk/prompts/calculator_v1.md` | You are a refund calculator. You are given the items to refund with their prices. |
| `workflows/refund_desk/build/lib/refund_desk/prompts/intake_v1.md` | You extract a refund request from a customer's message. |
| `workflows/refund_desk/build/lib/refund_desk/prompts/writer_v1.md` | You write a short, polite customer-service message of at most two sentences. |
| `workflows/refund_desk/build/lib/refund_desk/steps.py` | The five Refund Desk steps. Each takes a :class:`StepContext` and returns the step's outputs. |
| `workflows/refund_desk/build/lib/refund_desk/store.py` | Retail data: the Refund Desk's customers/orders and, independently, Granite's source of truth. |
| `workflows/refund_desk/granite_refund_desk.egg-info/dependency_links.txt` |  |
| `workflows/refund_desk/granite_refund_desk.egg-info/PKG-INFO` |  |
| `workflows/refund_desk/granite_refund_desk.egg-info/requires.txt` |  |
| `workflows/refund_desk/granite_refund_desk.egg-info/SOURCES.txt` |  |
| `workflows/refund_desk/granite_refund_desk.egg-info/top_level.txt` |  |
| `workflows/refund_desk/pyproject.toml` |  |
| `workflows/refund_desk/README.md` | refund_desk |
| `workflows/refund_desk/refund_desk/__init__.py` | Refund Desk: Granite's first system under test (master plan 21.3). |
| `workflows/refund_desk/refund_desk/definition.py` | Refund Desk workflow definition: steps and their declared reads, checks, and repair rules. |
| `workflows/refund_desk/refund_desk/faults.py` | Fault operators for Refund Desk. Faults are rule-based and deterministic: no LLM is involved. |
| `workflows/refund_desk/refund_desk/prompts/calculator_v1.md` | You are a refund calculator. You are given the items to refund with their prices. |
| `workflows/refund_desk/refund_desk/prompts/intake_v1.md` | You extract a refund request from a customer's message. |
| `workflows/refund_desk/refund_desk/prompts/writer_v1.md` | You write a short, polite customer-service message of at most two sentences. |
| `workflows/refund_desk/refund_desk/steps.py` | The five Refund Desk steps. Each takes a :class:`StepContext` and returns the step's outputs. |
| `workflows/refund_desk/refund_desk/store.py` | Retail data: the Refund Desk's customers/orders and, independently, Granite's source of truth. |
| `workflows/refund_desk/tests/__init__.py` |  |
| `workflows/refund_desk/tests/conftest.py` | A deterministic stand-in for the language model that reads the three Refund Desk prompts. |
| `workflows/refund_desk/tests/test_faults_and_verification.py` | Fault injection, detection, attribution and verification on the real workflow definition (TC-FLT, TC-VER). |
| `workflows/refund_desk/tests/test_store_and_steps.py` | Source of truth, policy rules and step parsing (TC-WF-*). |

## tests  (active (code))

| Path | Title / description |
|---|---|
| `tests/README.md` | tests |

## scripts  (active (code))

| Path | Title / description |
|---|---|
| `scripts/.ruff_cache/.gitignore` |  |
| `scripts/.ruff_cache/0.16.10/16623373247564932835` |  |
| `scripts/.ruff_cache/0.16.10/7006256987119764914` |  |
| `scripts/.ruff_cache/CACHEDIR.TAG` |  |
| `scripts/apply_workspace_migration.py` | Apply the 2026-10-06 workspace migration. Idempotent and non-destructive. |
| `scripts/build_index.py` | Regenerate docs/workspace-index.md: one line per file (path and title), grouped by top-level folder. |
| `scripts/build_truth_snapshot.py` | Build data/seed/taubench_retail_v1/ from the raw tau-bench retail data (deterministic). |
| `scripts/check_links.py` | Check that relative links in Markdown (and plain href/src in HTML) point at files that exist. |
| `scripts/check_traceability.py` | Requirements traceability: requirement (master plan) -> implementation -> tests, checked against the repositor |
| `scripts/check_workspace.py` | Check the workspace against docs/workspace-guide.md. |
| `scripts/export_diagrams.py` | Generate the diagrams that must always match the code, as Mermaid inside Markdown files. |
| `scripts/export_trace_schema.py` | Write the Granite Trace v1 JSON Schema from the pydantic model (the model is the single source of truth). |
| `scripts/linkcheck-allowlist.txt` |  |
| `scripts/README.md` | scripts |
| `scripts/record_cassettes.py` | Record real model responses so the demo and the tests can run offline (Granite 'recorded mode'). |
| `scripts/ruff.toml` |  |
| `scripts/smoke-test.sh` |  |

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
| `evidence/demos/2026-10-07_finding-accepted-review-history.jpg` |  |
| `evidence/demos/2026-10-07_finding-ranked-hypotheses.jpg` |  |
| `evidence/demos/2026-10-07_finding-refuted-experiment-and-review.jpg` |  |
| `evidence/demos/2026-10-07_new-run-form-running.jpg` |  |
| `evidence/demos/2026-10-07_run-detail-mobile-375px.jpg` |  |
| `evidence/demos/2026-10-07_run-detail-stale-price-graph.jpg` |  |
| `evidence/README.md` | evidence |
| `evidence/reports/2026-10-07_accessibility-audit.md` | Accessibility audit, 2026-10-07 |

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

## .github  ()

| Path | Title / description |
|---|---|
| `.github/workflows/ci.yml` |  |
