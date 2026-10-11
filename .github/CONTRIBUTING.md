# How we change this repository

The short version: **nobody pushes to `main`. Every change is a small branch, a pull request, a green CI run and one review by another member.** The decision and its reasons are in [ADR-010](../docs/adr/adr-010-git-branching.md).

> Status on 2026-10-11: this is the agreed working method from Iteration 2 onward. Up to that date the history shows direct pushes to `main` and one long-lived branch (`noor`); `main` is not protected yet and there are no pull requests. See the [repository evidence](../evidence/repo/) for what is actually in place.

## Branches

| Branch | Purpose | Lives for |
|---|---|---|
| `main` | Always releasable. CI runs on every push; CD publishes the image and deploys the demo from here | Permanent |
| `feat/<area>-<topic>` | A feature, for example `feat/verify-control-replays` | Days, then deleted |
| `fix/<issue>-<topic>` | A defect from the [defect list](../docs/registers/defect-list.md), for example `fix/d07-redaction` | Days |
| `docs/<topic>`, `chore/<topic>` | Documents, tooling, CI | Days |

Milestones are **tags** on `main`, not branches: `v0.1.0-mid1`, `v0.2.0-final1`. Pushing a tag creates a GitHub Release and a tagged container image (see [`cd.yml`](workflows/cd.yml)).

## The loop

```bash
git switch main && git pull
git switch -c feat/verify-control-replays
# ... work in small commits ...
git push -u origin feat/verify-control-replays
gh pr create --fill
```

1. Open the pull request early (draft is fine). The [template](pull_request_template.md) asks what changed, how it was checked and whether AI tools were used.
2. CI must be green: lint, types, unit, integration and system tests, security scans, the container smoke test.
3. One other member reviews. The reviewer runs the change or reads the tests; "looks good" without reading is not a review.
4. Squash-merge, delete the branch.

## Commit messages

[Conventional Commits](https://www.conventionalcommits.org/): `type(scope): what changed`, in the imperative, under 72 characters.

`feat(verify): add control replays` · `fix(api): cache the model probe` · `test(system): cover restart` · `docs(adr): record ADR-010 revision` · `ci: run system tests against the container`

One logical change per commit. Commit as you go: several small commits a week from each member are the evidence the rubric asks for; one large commit before a deadline is the red flag it names.

## Before you push

```bash
ruff check packages/granite_core workflows/refund_desk apps/api scripts tests
python scripts/check_architecture.py
pytest tests/system
```

The full list of gates and how to run each is in the [coding standards](../docs/manuals/coding-standards.md) and the [setup manual](../docs/manuals/setup-manual.md).

## Ownership

Each module has an owner who reviews changes to it and can explain it line by line: see the table in the [code walkthrough](../docs/manuals/code-walkthrough.md#who-owns-what). Using an AI tool does not move ownership: whoever merges the code answers for it, and the use is logged in the [AI usage log](../docs/registers/ai-usage-log.md).
