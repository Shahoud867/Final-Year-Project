# Granite (F26-060)

*A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery.* FAST-NUCES Islamabad, FYP 2026-27.
Team: Shahoud Shahid, Muhammad Noor, Saif Shahzad. Supervisor: Dr. Adil Majeed.

Granite is an evidence-first investigation workbench for multi-agent LLM workflows: **find the failure, prove the cause, verify the fix.**

## Run it

A working slice exists (state and gaps: [`docs/plan/execution-status.md`](docs/plan/execution-status.md)). Quick start in recorded mode, which needs no model, key or account:

```bash
python -m venv .venv && source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -e "packages/granite_core[dev]" -e "workflows/refund_desk[dev]" -e "apps/api[dev]"
(cd apps/web && npm ci && npm run build)
cd apps/api && GRANITE_LLM_MODE=recorded GRANITE_STATIC_DIR=../web/dist uvicorn granite_api.main:app_from_env --factory --port 8000
```

Open <http://127.0.0.1:8000>, choose **New run**, load an example and press Run. Full instructions: [`docs/manuals/setup-manual.md`](docs/manuals/setup-manual.md); how to use it: [`docs/manuals/tool-manual.md`](docs/manuals/tool-manual.md).

| Part | Where |
|---|---|
| Core library (trace, checks, attribution, verification, lifecycle, evidence) | [`packages/granite_core`](packages/granite_core/) |
| Refund Desk workflow (first system under test) | [`workflows/refund_desk`](workflows/refund_desk/) |
| API, persistence, jobs | [`apps/api`](apps/api/) |
| Web UI | [`apps/web`](apps/web/) |
| Decisions, diagrams, registers | [`docs/adr/`](docs/adr/), [`docs/diagrams/`](docs/diagrams/), [`docs/registers/`](docs/registers/) |
| Evaluation protocol and results | [`research/eval/`](research/eval/) |

## Start here

- **What to do now and what to build:** [`docs/plan/master-plan.md`](docs/plan/master-plan.md) (section 0 is the action card)
- **Where everything lives and how to name it:** [`docs/workspace-guide.md`](docs/workspace-guide.md)
- **Looking for a file that used to be somewhere else?** `grep` its old name in [`archive/migration-map_2026-10-06.tsv`](archive/migration-map_2026-10-06.tsv)

## Layout in one table

| Folder | State | Holds |
|---|---|---|
| [`docs/`](docs/) | active | master plan, report sources (LaTeX), diagrams, ADRs, manuals, meeting minutes, registers |
| [`research/`](research/) | active | literature and market notes, proposal-stage spikes, evaluation (pre-registrations, scripts, results) |
| [`data/`](data/) | active; `raw/` read-only | datasets, register and retrieval commands |
| [`apps/`](apps/), [`packages/`](packages/), [`workflows/`](workflows/), [`tests/`](tests/), [`scripts/`](scripts/) | active (code) | product code, libraries, demo workflows, tests, repository tooling |
| [`references/`](references/) | read-only | handbook, rubrics, templates, papers, market sources |
| [`deliverables/`](deliverables/) | frozen per stage | what was submitted or presented: `stage-0-proposal` ... `stage-4-fyp2-final`. For the FYP-1 mid evaluation start at [`stage-1-fyp1-mid/README.md`](deliverables/stage-1-fyp1-mid/README.md) |
| [`evidence/`](evidence/) | append-only | screenshots, recordings, UAT and interview records, exported test reports |
| [`archive/`](archive/) | history | superseded and obsolete material, migration map |

## Five rules

1. One canonical home per artefact; link, do not copy.
2. Never edit `deliverables/` once a stage is over, never edit `references/` or `data/raw/`; fix the source and export a new version.
3. Move, never delete tracked work (`archive/`).
4. Names: `lowercase-kebab-case`, ISO dates first (`2026-10-14_...`), versions only on exported files (`_v1.0`).
5. Secrets, personal data and client data never enter the repository.

## Tools

```bash
python scripts/check_links.py     # broken relative links
python scripts/check_workspace.py # naming rules and required READMEs
python scripts/build_index.py     # regenerate docs/workspace-index.md
python scripts/export_trace_schema.py --check && python scripts/build_design_pack.py --check   # schema, diagrams and data dictionary match the code
python scripts/check_traceability.py --check   # requirement -> code -> test references are real
```
