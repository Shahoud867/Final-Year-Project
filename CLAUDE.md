# Orientation for AI sessions

Project: Granite (F26-060), a 3-member FAST-NUCES final year project. Read [`README.md`](README.md) first, then the section of [`docs/plan/master-plan.md`](docs/plan/master-plan.md) that matches the task. The layout and naming rules are in [`docs/workspace-guide.md`](docs/workspace-guide.md); do not restate them elsewhere.

- **Source of truth for scope, schedule and rubric mapping:** `docs/plan/master-plan.md`. Official requirements: `references/university/` (handbook, Mid-1 rubric) and `references/templates/`.
- **Search `docs/` and `research/` first.** Skip `archive/` unless history is the question. **Never grep `data/raw/`** (about 1,100 third-party files). `docs/workspace-index.md` has one line per file.
- **Frozen, do not edit:** `deliverables/stage-0-proposal/` and any finished stage, `references/`, `data/raw/`, `archive/`. Fix the source and export a new version instead.
- **Old path or old filename in a document or chat?** Look it up in `archive/migration-map_2026-10-06.tsv`.
- **New files follow the naming convention** (workspace-guide section 4). Run `python scripts/check_workspace.py` and `python scripts/check_links.py` after structural changes.
- **Moves:** use `git mv`, fix links, then `python scripts/build_index.py`. Never delete tracked work; move it to `archive/`.
- **Honesty rules from the rubric apply to your output too:** do not mark anything "done" without a demonstrable artefact, and record AI assistance in `docs/registers/ai-usage-log.md`.
