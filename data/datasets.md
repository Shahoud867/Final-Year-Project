# Granite — Datasets

*Supplements [FYP_Scope_CCP_and_Implementation_Plan.md](../deliverables/stage-0-proposal/proposal-documents/FYP_Scope_CCP_and_Implementation_Plan.md) §8. All datasets below are public. Verify each license and current access point directly before use — this list reflects what was confirmed during literature review in [Full_Literature_Landscape_Analysis.md](../research/literature/literature-landscape-analysis.md).*

**Path note (2026-08-22):** actual dataset files and the POC spike scripts moved from `agent-autopsy/datasets/` and `agent-autopsy/spikes/` to a new sibling `dev/` folder (`dev/datasets/`, `dev/spikes/`), separating development artifacts from this research/planning documentation. Every bare `datasets/...` path referenced below is relative to `dev/`, not to this `markdowns/` folder. **Update (2026-10-06):** `dev/` no longer exists; the datasets are now in `data/raw/` and the spikes in `research/spikes/` (see `docs/workspace-guide.md`).

---

## 1. Baseline-reproduction datasets (reused, not built)

These exist to reproduce ErrorProbe's and its ancestors' published numbers, so the head-to-head comparison in the evaluation plan is apples-to-apples.

| Dataset | Introduced by | License | Size | Access | Role |
|---|---|---|---|---|---|
| **Who&When** (Algorithm-Generated + Hand-Crafted splits) | Who&When, ICML 2025 (arXiv:2505.00212) | MIT — confirmed in ErrorProbe's own "Licensing and Intended Use" section | 127 systems / 184 annotated tasks (algo/hand split counts differ slightly across citing papers — pull the authoritative count from the released files, not a secondary paper's restated figure) | Public repository linked from the paper (`proceedings.mlr.press/v267/zhang25cq.html`) | Baseline reproduction: agent/step attribution accuracy |
| **TracerTraj-2.5K** | AgenTracer, ICLR 2026 (arXiv:2509.03312) | **Corrected 2026-08-22, verified by direct repo inspection, not by trusting ErrorProbe's citation of it:** the full 2.5K dataset and AgenTracer-8B model weights are **not released yet** — the repo's own README states "We commit to open-sourcing the model weights and training data/scripts upon acceptance of the paper." **No LICENSE file exists in the repo**, contradicting the "Apache 2.0" claim, which traced back to ErrorProbe's paper describing AgenTracer's license, not to a direct check of the source | What's actually public: a data-generation *pipeline* ("a minimal working example... applied to MetaGPT") plus **one real sample file confirmed by direct download: 127 rows**, code-domain only (`data/tracertraj-code-test.parquet`) — not the full 2,000+ trajectory set | `github.com/bingreeky/AgenTracer` | Downgraded from "baseline reproduction data" to "pipeline reference + 127-row sample only" until the full release happens |
| **TraceElephant benchmark** | TraceElephant, ACL 2026 Long (arXiv:2604.22708) | CC BY 4.0 for traces/annotations (paper's own Appendix A.10); benchmark code license unspecified pending repo release | Full input+output traces on GAIA, AssistantBench, SWE-Bench | `github.com/TraceElephant/TraceElephant` | Optional secondary reproduction target if full-trace observability becomes relevant to a later extension |

**Reuse note:** ErrorProbe itself has no confirmed license for its own code/repo (states research-only intent, not a formal license) — reproduce its *methodology* from the paper rather than depend on reusing its repository directly, consistent with the delta statement in the plan doc.

---

## 2. Public task sources used as injection substrate

Not new datasets in themselves — these supply the task prompts that the new benchmark's agent runs are built on top of, so ground truth comes from the injection operator rather than manual annotation (the same cost-saving trick AgenTracer used).

| Source | License / access | Approx. size | Already used by |
|---|---|---|---|
| **GAIA** | **Correction (2026-08-22): gated, confirmed by direct attempt, not just documentation.** `gaia-benchmark/GAIA` (official), `NEAR-AI/gaia`, and `anivenu/gaia-verified` (both supposed mirrors) **all three** returned `DatasetNotFoundError: gated dataset, must be authenticated` when actually attempted. Requires a real Hugging Face account + accepting GAIA's terms via `huggingface-cli login` — no way around it found | ~450+ tasks across 3 difficulty levels | Who&When, TraceElephant |
| **HotpotQA** | Public, Hugging Face Datasets (`hotpotqa/hotpot_qa`) | ~113k QA pairs | AgenTracer |
| **MBPP+** (EvalPlus-extended MBPP) | Public, Hugging Face Datasets (`evalplus/mbppplus`) | **Correction (2026-08-22): 378 tasks**, not ~1,000 — the original MBPP has ~1,000 but EvalPlus's extended-test version removed broken tasks, landing at 378 | AgenTracer |
| **GSM8K** | Public, Hugging Face Datasets (OpenAI release) | ~8.5k grade-school math problems | AgenTracer, AgentAsk |
| **MATH** | Public, Hugging Face Datasets | ~12.5k competition math problems | AgenTracer, AgentAsk |
| **SWE-bench** | Public, Hugging Face Datasets | ~2,300 real GitHub issue/PR pairs | TraceElephant |

Pick 1–2 of these (not all six) to seed the new benchmark's task pool — breadth across many task domains is not the point of this benchmark; breadth across *unseen architectures* is (see plan doc §1, §4).

---

## 3. The new contribution — cross-architecture fault-injection benchmark

| Field | Plan |
|---|---|
| Built from | Task prompts drawn from §2 above (recommend GAIA + one coding-style source, e.g. MBPP+) |
| Run through | ≥2 previously-unused multi-agent frameworks (CrewAI, native LangGraph — see [resources.md](../deliverables/stage-0-proposal/proposal-documents/resources.md) §2) |
| Fault types | Corrupted tool output (POC scope) + communication corruption, context truncation, tool-response corruption (extension #1 in the plan doc's §7) |
| Ground truth | Exact by construction — the injection operator *is* the label, no manual annotation needed |
| Target size | 500–1,000 labeled traces (matches AgenTracer's TracerTraj scale) |
| Intended license on release | MIT or CC BY 4.0 — matches the field's own norm (Who&When: MIT; AgenTracer: Apache 2.0; TraceElephant: CC BY 4.0) |
| Where it's released | Public GitHub repo + Hugging Face Datasets, paired with the leaderboard page (plan doc §7, extension #13) |

---

## 4. Known caveat carried over from the literature review

There is a **confirmed cross-paper inconsistency** in Who&When's own reported split sizes: SDBL states Hand-Crafted=54/Algorithm-Generated=126, while AgenTracer and ErrorProbe both state Algo=127/Hand=58. Likely different filtering/exclusion choices per paper, not fabrication — but when exact counts matter for the project report, pull them from Who&When's own released dataset files directly rather than trusting either secondary paper's restated figure.

---

## 5. Attempted self-generation of a TracerTraj-scale dataset — tried, abandoned (2026-08-22)

Since TracerTraj-2.5K itself isn't released (§1), one path considered was generating an equivalent-scale dataset ourselves: run AgenTracer's own published pipeline (`MetaGPT` + `generate_repo`, vendored in `datasets/agentracer_full/MetaGPT/coding/`) against real task prompts, using a free local model instead of a paid API.

**What was actually built:** a Python 3.11 venv (system Python was 3.13, incompatible with MetaGPT's `<3.12` requirement), MetaGPT installed from the vendored repo, and two real task-pool files generated: `mbppplus-full.parquet` (378 tasks, adapted from our own downloaded MBPP+) and `kodcode-hardmedium.parquet` (1,622 tasks, pulled live from the public, ungated `KodCode/KodCode-Light-RL-10K` dataset's hard+medium split) — 2,000 tasks combined. Two real pipeline bugs were found and fixed in the process: MetaGPT's provider module eagerly imports every vendor LLM SDK at startup (breaks if any are missing, even unused ones); Ollama's actual chat endpoint is `/api/chat`, not `/chat`, so the first config silently 404'd every call.

**Why it was abandoned:** once the pipeline was genuinely working, a single pilot task (one 8-round multi-agent coding session via local `llama3.2:3b`) ran over 10 minutes without completing. Extrapolated across ~2,000 tasks at even modest concurrency, the full run would take multiple days of continuous local compute — not a viable timeframe. Stopped by explicit instruction, not left running unattended.

**What's left in place:** the venv, MetaGPT install, and both generated task-pool parquet files remain on disk (`E:\ai-workspace\metagpt-venv`, `datasets/agentracer_full/MetaGPT/coding/datasets/code/`) in case this is revisited later with more time or a paid API budget. The dataset ceiling for this project remains the 127-row real AgenTracer sample from §1, plus Who&When (184), MBPP+ (378), and GAIA (466).

---

## 6. Injection-substrate datasets added 2026-08-22 — GSM8K, MATH, tau-bench (retail)

Added specifically as task-prompt substrate for the project's own cross-architecture fault-injection benchmark (§3 above), chosen over SWE-bench/tau-bench-airline for cost reasons — see the discussion in-session: GSM8K/MATH are cheap (single-turn, single-checkable-number ground truth, matches the mechanism already validated in POC Spike 4), tau-bench retail is the primary substrate for the real benchmark-building pass (richer, structured ground truth — full correct action sequences plus explicit policy rules — better suited to constraint-based silent-failure checking than a lone number, and inherently multi-turn/agentic already). All three verified directly (downloaded and counted, not estimated from a citation).

| Dataset | Location | Size (verified) | License (verified) | Source |
|---|---|---|---|---|
| **GSM8K** | `datasets/gsm8k/{train,test}.parquet` | 7,473 train + 1,319 test = **8,792 total** | MIT — confirmed via HF API `cardData` | `openai/gsm8k` (Hugging Face) |
| **MATH** | `datasets/math/{train,test}.parquet` | 7,500 train + 5,000 test = **12,500 total** (7 subject configs: algebra, counting_and_probability, geometry, intermediate_algebra, number_theory, prealgebra, precalculus — concatenated) | MIT — confirmed via HF API `cardData` | `EleutherAI/hendrycks_math` (Hugging Face). **Correction:** `hendrycks/competition_math`, the repo id first tried, does not exist (401/repo-not-found) — the license figure attached to that nonexistent repo in an earlier pass of this session was accordingly wrong at the time; this entry supersedes it with a verified repo and license |
| **tau-bench (retail)** | `datasets/taubench_retail/` | 500 train + 20 dev + 115 test = **635 tasks**, plus full env code (`env.py`, `rules.py`, 16 tool implementations, `data/{orders,products,users}.json`, policy `wiki.md`) | MIT — confirmed via the repo's own downloaded `LICENSE` file, not just a citation | `sierra-research/tau-bench` (GitHub). Repo carries its own warning that these tasks are "not updated" and points to a newer τ²-bench successor with an added banking domain — worth checking before committing further build time to this version |

**Not downloaded, by deliberate choice:** tau-bench (airline) — only 50 tasks, test-only, no train/dev split, lower priority than retail's 635; SWE-bench — same heavy per-task multi-agent-workflow cost profile that made the AgenTracer self-generation attempt (§5) infeasible, skipped for the same reason.

**Active vs. benched, decided 2026-08-22:** downloading all of GAIA/MBPP+/GSM8K/MATH/tau-bench does not mean all five should be built against — this file's own §2 already says "pick 1–2, not all six." The active build plan is narrowed to **GSM8K** (cheap prototyping, single-integer answers match POC Spike 4's numeric near-miss mechanism cleanly) + **tau-bench retail** (the real benchmark-building pass — richer ground truth, matches the product's actual customer-support deployment story). **GAIA, MBPP+, and MATH are benched** — downloaded, verified, kept on disk, but not currently part of the build: MATH specifically because its answers (equations/sets/intervals) fit the near-miss check worse than GSM8K's plain integers; GAIA/MBPP+ because the 2-source plan already covers the 500–1,000 trace target several times over. Reintroduce only if GSM8K + tau-bench retail proves too thin in practice.
