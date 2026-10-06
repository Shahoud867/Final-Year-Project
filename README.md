# Granite (F26-060)

*A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery.* FAST-NUCES Islamabad, FYP 2026-27.
Team: Shahoud Shahid, Muhammad Noor, Saif Shahzad. Supervisor: Dr. Adil Majeed.

Granite is an evidence-first investigation workbench for multi-agent LLM workflows: **find the failure, prove the cause, verify the fix.**

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
| [`deliverables/`](deliverables/) | frozen per stage | what was submitted or presented: `stage-0-proposal` ... `stage-4-fyp2-final` |
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
```
