# scripts

Repository tooling. Python 3, standard library only.

| Script | Purpose |
|---|---|
| `check_links.py` | fails on broken relative links in Markdown and HTML; known accepted exceptions are listed in `linkcheck-allowlist.txt` |
| `check_workspace.py` | enforces the naming convention, the top-level folder set and required READMEs |
| `check_cassette_prompts.py` | fails when the recorded cassette no longer matches the prompts in the code (D-10); `--write` stamps the current prompts into the cassette after re-recording |
| `build_index.py` | regenerates `docs/workspace-index.md` (one line per file) |
| `score_usability.py` | scores a usability-check results CSV (task success, SUS) against the thresholds in `docs/manuals/usability-check-protocol.md` and prints a Markdown summary |
| `apply_workspace_migration.py` | moves files that arrive at pre-reorganization paths (see `archive/README.md`); delete when no longer needed |

Add a row here for every new script.
