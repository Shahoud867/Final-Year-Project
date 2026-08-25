# Datasets — provenance, licensing, and retrieval

*Written 2026-08-25. This directory currently holds **~46MB of third-party data and code vendored directly into git**. That works today and is not urgent to change for the proposal defense — but it must be resolved **before this repository is ever made public**, for one licensing reason and two professionalism reasons. This file records where every dataset came from, under what license, and how to retrieve it, so the tracked copies can be replaced with retrieval steps whenever the team decides to.*

---

## ⚠️ Read this first: GAIA cannot be redistributed

**`gaia_official/` is a gated dataset.** Access on Hugging Face requires accepting an access agreement, which means the data was obtained under terms that permit *use*, not *redistribution*. Publishing this repository with `gaia_official/` in it would very likely breach those terms.

Two things make this lower-stakes than it sounds, and one makes it urgent:

- **Lower-stakes:** GAIA is *benched, not active* ([datasets.md](../../markdowns/01-planning-and-scope/datasets.md) §6) — the committed benchmark plan uses GSM8K + tau-bench retail only. Nothing in the build depends on GAIA. It can simply be removed.
- **Also lower-stakes:** the repository is currently private. No redistribution has occurred yet.
- **Urgent:** deleting it from the working tree is *not enough* if the repository goes public with history intact — git history would still contain it. History must be rewritten before publishing, not after.

**What to do, in order, and only when the team decides to go public:**

```bash
git rm -r --cached dev/datasets/gaia_official
```

Then, and only then — after taking a full backup, because history rewriting is destructive and irreversible:

```bash
git filter-repo --path dev/datasets/gaia_official --invert-paths
```

Do this deliberately, once, with every collaborator informed (it rewrites commit hashes for everyone). If GAIA is ever needed again, re-download it per the table below rather than restoring it from history.

---

## Every dataset in this directory

| Directory | What it is | License | Status in the project | How to retrieve |
|---|---|---|---|---|
| `whowhen_full/` | **Who&When** — 184 annotated failure-attribution cases (127 systems), the baseline reproduction dataset | **MIT** — `LICENSE` present in-tree, verified | **Active and load-bearing.** All of Spike 1 and the entire ErrorProbe reproduction run against this | Clone the Who&When repository from its published source and take `Who&When/{Algorithm-Generated,Hand-Crafted}/` |
| `taubench_retail/` | **tau-bench (retail)** — 635 customer-support tasks with policy rules and full correct action sequences | Permissive — `LICENSE` present in-tree, verified | **Active.** One of the two committed benchmark substrates; the richer ground truth (policy rules + action sequences) and the domain match to the notional client | Clone tau-bench upstream; the retail domain lives under its `data/` tree |
| `gsm8k/` | **GSM8K** — 8,792 grade-school math problems with single-integer answers | Permissive (MIT) — verify against the upstream repo before release | **Active.** The other committed substrate; single-integer answers match Spike 4's validated numeric near-miss check cleanly | `datasets.load_dataset("gsm8k", "main")` |
| `agentracer_full/` | **AgenTracer** upstream repository, vendored whole — *including a complete copy of MetaGPT* | MetaGPT is **MIT**; AgenTracer itself has **no LICENSE file** (R11) | **Benched.** Only the 127-row `tracertraj-code-test.parquet` sample is real data; TracerTraj-2.5K was never released (R11, confirmed by direct download attempt) | Pin a specific upstream commit hash here rather than vendoring the tree — see "Why vendoring is wrong" below |
| `mbppplus/` | **MBPP+** — 378 programming tasks | Permissive — verify before release | **Benched.** Left over from the abandoned TracerTraj self-generation attempt (R11b) | `datasets.load_dataset("evalplus/mbppplus")` |
| `math/` | **MATH** — 12,500 competition math problems | Permissive — verify before release | **Benched.** Answers (equations/sets/intervals) fit Spike 4's numeric check worse than GSM8K's plain integers | `datasets.load_dataset("hendrycks/competition_math")` |
| `gaia_official/` | **GAIA** — 466 general-assistant benchmark tasks | ⚠️ **Gated access agreement — redistribution not permitted** | **Benched.** Nothing depends on it | Requires accepting GAIA's access agreement on Hugging Face, per-user. **Do not redistribute** |

*Licenses marked "verify before release" have not been confirmed against their primary source in-tree yet. Confirm each at the Mid-1 data/licensing clearance gate ([plan §12](../../markdowns/01-planning-and-scope/FYP_Scope_CCP_and_Implementation_Plan.md)), the same way Who&When and tau-bench already were — a citation is not a license check (the TracerTraj lesson, R11).*

---

## Why vendoring these into git is wrong, even where it's legal

MetaGPT (`agentracer_full/MetaGPT/`) is MIT-licensed, so vendoring it breaks no license. It is still the wrong engineering choice, for reasons a supervisor or reviewer will recognize immediately:

1. **It hides provenance.** A vendored copy has no version. Six months from now, nobody can tell which upstream commit it came from or whether it carries local modifications. A pinned commit hash answers both questions in one line.
2. **It inflates the repository permanently.** Git history is append-only; 46MB committed today is 46MB every clone pays for forever, including the 20MB of vendored framework code nothing in the active build plan uses (the committed plan targets CrewAI and LangGraph, not MetaGPT).
3. **It blurs the ownership boundary the FYP is graded on.** Guide §14 asks which components are the team's own work. A repository whose file count is dominated by someone else's framework makes that question harder to answer than it needs to be — the team's actual work is `dev/spikes/poc/` and `markdowns/`, and it should be visually obvious.

**None of this affects `dev/spikes/poc/`.** Those scripts and their output JSON are the team's own work and are proposal-defense evidence under guide §12 — they stay in git.

## When to act

Not before the defense. The change plan ([`05_Repository_Change_and_Commit_Plan.md`](../../05_Repository_Change_and_Commit_Plan.md)) deliberately schedules this **after the defense and before the repository goes public** — a 46MB cleanup three days out from a defense is risk with no upside, and the datasets are actively being read by the spikes right now. The trigger is publication, not a date.
