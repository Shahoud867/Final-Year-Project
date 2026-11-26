# archive

History. Nothing here is current. Move things in, never delete them. Names here are historical and exempt from the naming rules.

| Folder | Holds |
|---|---|
| `proposal-phase/` | Aug-Sep 2026 working material that was not a stage deliverable: `audits/` (root audit and Q&A documents 01-07), `tracking/` (old trackers, checklists, the pre-reorganization index), `explanations/` (long-form narratives) |
| `pre-granite/` | "TraceCause"-era drafts, before the rename to Granite |
| `superseded/` | earlier versions of active documents (master plan v1.0) and an analysis its own header calls superseded |
| `migration-map_2026-10-06.tsv` | action, old path, new path and reason for every file moved or deleted in the reorganization |

Future phases get their own folder (`fyp1-phase/`, ...).

## Finishing the 2026-10-06 reorganization in git

The reorganization was done on the filesystem only. Nothing was staged, committed or merged, so git still shows the old paths as deleted and the new ones as untracked. A full backup (31.9 MB, tracked and untracked files except the datasets, which are clean in git) is at `../_backup_pre-reorg_2026-10-06.zip`, outside the repository. Suggested order:

1. **Stale rebase state.** `git status` reports a rebase in progress, but `.git/rebase-merge/` is empty, so there is nothing left to replay. If no one is mid-conflict, `git rebase --quit` clears the state and leaves the working tree untouched.
2. **Commit the moves on a branch:** `git switch -c chore/workspace-reorg`, `git add -A`, review with `git status` (or `git diff --cached -M --stat` after `git add -A`). A dry run in a throwaway index found 1,249 exact renames and 31 renames with edits. Three files show as delete + add instead of a rename: `dev/README.md` and `markdowns/INDEX.md` (rewritten) and `Granite_Proposal_Defense_v2.pptx` (see step 3). Then commit.
3. **Bring in `origin/noor`** (5 commits ahead; they edit files at their *old* paths): `git fetch`, `git merge origin/noor`. Edits should follow the renames. **Expect one conflict:** `Granite_Proposal_Defense_v2.pptx` has an uncommitted local modification *and* a commit on the remote, and git cannot rename-track a modified binary, so it reports modify/delete. The remote copy is the committed one; unless your local rebuild is newer, keep the remote version at `deliverables/stage-0-proposal/proposal-deck/`. Other binaries (`.docx`, `.pdf` under `defense-prep/` and `proposal-deck/`) should follow their renames; if git reports a conflict on one, keep the remote version at the new path.
4. **Files created on the remote** (`Granite_FYP_Preparation_Guide.*`, `Granite_PoC_Explanation_Guide.*`) arrive at the old paths. Run `python scripts/apply_workspace_migration.py` to move them. Then fix the one link the script deliberately left alone: line 39 of `deliverables/stage-0-proposal/proposal-deck/Proposal_Defense_Package.md` (`../01-planning-and-scope/` becomes `../proposal-documents/`). Then run `python scripts/check_links.py`.
5. **Teammates** after pulling: delete the leftover empty old folders. Local untracked deck-build folders (`_render_check/`, `canvas/`, `Granite.pptx`) under the old `markdowns/05-deliverables/proposal-deck/` belong in `deliverables/stage-0-proposal/proposal-deck/` (git-ignored there).
6. **Tidy afterwards:** the root `.gitignore` was left untouched to avoid a merge conflict; its two comments about `dev/datasets/` and `dev/spikes/poc/` and its three deck-build rules now point at old paths. Delete `scripts/apply_workspace_migration.py` once step 4 is done, and the backup zip once the commit is verified.
