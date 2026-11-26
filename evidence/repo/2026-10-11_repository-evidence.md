# Repository evidence, 2026-10-11

Read from the repository with `git` and the GitHub CLI on 2026-10-11 (commit `5099243` on `main`, the latest pushed commit). Nothing here is an estimate. It is written for rubric criterion 6 (repository, milestone and member evidence) and it reports the weak points as they are.

## Facts

| Item | State | How it was read |
|---|---|---|
| Repository | `Shahoud867/Final-Year-Project`, private, default branch `main` | `gh repo view` |
| Commits on `main` | 74, from 25 August to 9 October 2026 | `git rev-list --count HEAD` |
| Branches | `main`, `noor` (long-lived, from the proposal stage) | `git branch -a` |
| Pull requests | **None** | `gh pr list --state all` |
| Tags, releases | **None** | `git tag` |
| Protection of `main` | **Not protected** | `gh api repos/.../branches/main/protection` returned 404 |
| CI | Green on the two latest pushed commits, all four jobs | [CI record](2026-10-09_ci-run-37924480165.md) |
| CD | Workflow written, not yet pushed or run | `.github/workflows/cd.yml` |
| Uncommitted work on this date | About 150 changed or new files (design pack, system tests, docstrings, guide page, registers, this folder) | `git status --short` |

## Commit timeline by member

Noor's two commit identities (`Muhammad Noor`, `MuhammadNoor7`) are counted together.

| ISO week | Dates | Shahoud | Noor | Saif | What the commits were |
|---|---|---|---|---|---|
| 2026-W35 | 24 to 30 Aug | 18 | 5 | 0 | Idea, literature, early spikes |
| 2026-W36 | 31 Aug to 6 Sep | 4 | 5 | 1 | Proposal material |
| 2026-W37 | 7 to 13 Sep | 2 | 30 | 0 | Proposal deck and defense preparation (defense on 11 Sep) |
| W38 to W40 | 14 Sep to 4 Oct | 0 | 0 | 0 | **No commits for three weeks** |
| 2026-W41 | 5 to 11 Oct | 9 | 0 | 0 | The whole product: workspace reorganisation, core library, workflow, API, web UI, CI, documents |
| **Total** | | **33** | **40** | **1** | |

## What this shows, read against the rubric

| Rubric text | Our state |
|---|---|
| Exemplary: "regular, incremental commits from all members with meaningful messages" | Not met |
| Developing: "uneven commit history but all members contributed" | True for the whole history (proposal stage) |
| Marginal: "sparse commits or repo history dominated by a single member" | **True for the implementation.** All nine commits since 6 October are from one account, and they add about 297,000 lines in 2,800 file changes (most of that is the workspace reorganisation and data files, but the product code is all in them too) |
| Red flag: "sudden code volumes" | **Applies.** Three silent weeks, then the complete product in four days |
| Red flag: "uneven contribution" | **Applies.** Saif has one commit in the whole history; Noor has none on the product |

The reason is not hidden: the implementation was produced in AI-assisted sessions on one member's machine and committed in large batches (see the [AI usage log](../../docs/registers/ai-usage-log.md)). The commit messages are meaningful and follow one convention, but the history is not incremental and not shared.

## What changes, starting now

The working method is in [`.github/CONTRIBUTING.md`](../../.github/CONTRIBUTING.md). The first steps that produce real evidence, in order:

| # | Step | Who | Evidence to save here |
|---|---|---|---|
| 1 | Commit the pending work as **several small commits by area**, not one batch. Each member commits the area they own from their own account, after reading it (see the [code walkthrough](../../docs/manuals/code-walkthrough.md)) | All three | The commit list |
| 2 | Protect `main`: require a pull request, one approval and green CI. On a private repository this needs GitHub Pro (free with the Student Developer Pack) or a public repository | Saif | Screenshot of the rule |
| 3 | Each member opens one pull request with a real change to their area, reviewed by another member. Good first changes: D-25 (Noor), D-12 (Saif), a second fault type (Shahoud) | All three | Links to the three pull requests |
| 4 | Tag `v0.1.0-mid1` on the commit that is demonstrated | Saif | The release page |
| 5 | Add `.mailmap` so Noor's two identities count as one | Noor | `git shortlog -sne` |

Until steps 1 to 3 have happened, criterion 6 should be expected in the 3 to 6 range, whatever the quality of the code.
