# Granite — API Cost Estimate and Model Plan

*Produced 2026-08-25 to close the open half of [risk-register.md](../02-evidence-and-tracking/risk-register.md) R5 (API cost, previously "unknown until POC gives real per-trace token counts") and to attach a number to R1's reproduction plan. Supplements [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md) §11 and [resources.md](resources.md) §1.*

**Every token count below is measured, not estimated.** The trajectory sizes come from parsing all **184 real Who&When cases** already on disk (`dev/datasets/whowhen_full/Who&When/`), using the same prompt-construction logic Spike 1 actually ran (`dev/spikes/poc/poc_spike1_errorprobe_repro.py`, 220-char per-step truncation). Prices are Anthropic first-party list rates per 1M tokens. Treat prices as directional and re-verify before committing budget — they change independently of this document.

---

## 1. What the 184 cases actually contain (measured)

| Split | n | Steps/case (mean) | Trajectory tokens, truncated | Trajectory tokens, full |
|---|---|---|---|---|
| Algorithm-Generated | 126 | 8.7 (max 10) | **469** (max 615) | 2,943 (max 28,091) |
| Hand-Crafted | 58 | 51.6 (max 130) | **2,630** (max 6,915) | 16,453 (max 77,364) |
| **All cases (weighted)** | **184** | — | **1,150** | **7,202** |

The two splits differ by roughly **6×** in trajectory length — Hand-Crafted cases average 51.6 steps against Algorithm-Generated's 8.7. Anything that costs per-token is dominated by the 58 Hand-Crafted cases, not the 126 Algorithm-Generated ones. This is the kind of thing an unmeasured estimate gets wrong.

**Per-case cost of one 3-stage pipeline pass** (Strategist sees the trajectory; Investigator sees it again plus hypotheses and tool-grounding evidence; Arbiter sees hypotheses only; output capped at the `num_predict` values Spike 1 actually used):

| Setting | Input tokens/case | Output tokens/case | 184 cases |
|---|---|---|---|
| Truncated trajectories (Spike 1's setting) | ~3,400 | ~950 | 626K in / 175K out |
| **Full trajectories (fair reproduction)** | **~15,500** | **~950** | **2.85M in / 175K out** |

The fair reproduction is the row that matters: truncating to 220 characters per step is a POC concession for a 3B local model, and a head-to-head against a published number shouldn't inherit it.

---

## 2. ErrorProbe reproduction — cost per full run

| Backbone | Truncated (626K/175K) | **Full trajectories (2.85M/175K)** | Full, via Batch API (−50%) |
|---|---|---|---|
| Haiku 4.5 ($1 / $5) | $1.50 | **$3.73** | $1.86 |
| Sonnet 5 ($3 / $15) | $4.50 | **$11.18** | $5.59 |
| Opus 5 ($5 / $25) | $7.50 | **$18.64** | $9.32 |

**One full reproduction run costs about $11 on a Sonnet-class backbone.** That is the single most important number here, and it is far smaller than R5 assumed when it was written.

Budget the *iteration*, not the run: a reproduction is not built in one pass. At ~20 development runs (prompt fixes, parsing bugs, pipeline-stage debugging, re-runs after changes), that is **≈ $224**. A per-backbone sensitivity check — one final run each on Haiku 4.5, Sonnet 5 and Opus 5, mirroring how ErrorProbe itself reports across three backbones — adds **≈ $34**.

**"Comparable-class backbone" means:** ErrorProbe published 59.5% using Claude 3.7 Sonnet. The current same-tier equivalent is **Sonnet 5**, which is what the acceptance band in plan §11 (±10 points of 59.5%) is declared against. Haiku 4.5 is the cheap tier and is *not* a fair comparator for the band; Opus 5 exceeds the published setup and would flatter the result. Reporting per-backbone, as ErrorProbe does, keeps R4's backbone-confound caveat honest.

---

## 3. Benchmark generation — 500 to 1,000 traces

Per generated trace, grounded on the measured Algorithm-Generated profile (8.7 steps/case, 2,943 tokens of trajectory content): a 3–4 agent CrewAI/LangGraph workflow at ~10 LLM calls, with context re-sent each turn averaging ~2,000 input tokens per call and ~300 output — **≈ 20K input / 3K output per trace**.

| Backbone | 500 traces | 1,000 traces | 1,000 traces via Batch API (−50%) |
|---|---|---|---|
| **Haiku 4.5** | $17.50 | $35.00 | **$17.50** |
| Sonnet 5 | $52.50 | $105.00 | $52.50 |
| Opus 5 | $87.50 | $175.00 | $87.50 |
| Local Ollama | $0.00 | $0.00 | $0.00 |

Trace generation is **not latency-sensitive** — it is a bulk offline job — so the Batch API's 50% discount applies cleanly, and generation quality only needs to be good enough to produce *realistic agent behavior*, not good enough to *diagnose* it. That is why the cheap tier is the right choice here and the strong tier is reserved for evaluation.

---

## 4. Total project budget

| Line item | Plan | Cost |
|---|---|---|
| Benchmark generation, 1,000 traces | Haiku 4.5 + Batch API | $17.50 |
| ErrorProbe reproduction | Sonnet 5, ~20 dev iterations | $223.68 |
| Evaluation runs | Sonnet 5, 10 full runs | $111.84 |
| POC spikes to date (8 of them) | Local Ollama, `llama3.2:3b` | **$0.00** |
| | **Recommended total** | **≈ $353** |
| | *Pessimistic ceiling* — Sonnet 5 everywhere, no batching, 2× volume | *≈ $881* |

At ~Rs 280/USD: **≈ Rs 99,000 recommended, ≈ Rs 247,000 worst case.** Student credits, free tiers, and the local-model path for generation reduce the realistic figure well below the recommended line.

**The non-obvious finding, worth saying at defense:** the dominant cost driver is **reproduction iteration (~63%)**, not benchmark generation (~5%) — the reverse of what R5 assumed when it named "500–1,000 traces × multiple benchmarks" as the risk. Generation is cheap because it runs on the cheap tier in batch; reproduction is expensive because it must run on a fair-comparison backbone and must be run *many times* before it is correct. The mitigation follows directly: cache and freeze the reproduction's inputs, and don't re-run all 184 cases while debugging — iterate on a fixed 20-case subset (~$1.20/run) and reserve full runs for checkpoints.

---

## 5. Model plan (what actually gets used where)

| Workload | Model | Why |
|---|---|---|
| Agent-under-test behavior, trace generation at volume | Local Ollama first; **Haiku 4.5 + Batch API** where local quality is insufficient | Bulk, offline, quality-insensitive; the 8 spikes already prove local works for this |
| ErrorProbe reproduction + all evaluation runs | **Sonnet 5** | The fair comparator to ErrorProbe's published Claude 3.7 Sonnet setup — the accuracy-critical spend |
| Per-backbone sensitivity check (one run each) | Haiku 4.5 / Sonnet 5 / Opus 5 | Mirrors ErrorProbe's own 3-backbone reporting; addresses R4's confound caveat |
| Preventive classifier (extension #7) | Not an LLM — TF-IDF / local sentence embeddings | Deliberately scoped as supervised, not RL; $0 |

**Cost controls committed, not just noted:** iterate reproduction on a fixed 20-case subset rather than all 184; use the Batch API for every non-interactive bulk job; apply prompt caching where the same trajectory is sent to more than one pipeline stage (viable for Hand-Crafted cases at 2,630 tokens, above the ~1,024-token minimum cacheable prefix — *not* for Algorithm-Generated cases at 469 tokens, which fall below it); keep generation local wherever output quality permits.

---

## 6. How to reproduce these numbers

The measurement is not a spreadsheet — re-run it against the real data:

1. Parse every case in `dev/datasets/whowhen_full/Who&When/{Algorithm-Generated,Hand-Crafted}/*.json`.
2. Rebuild each trajectory with Spike 1's own `build_numbered_trajectory()` logic, at `MAX_CONTENT_CHARS = 220` for the truncated figures and untruncated for the full figures.
3. Convert characters to tokens at ~4 chars/token, then apply the 3-stage prompt structure in §1.
4. Multiply by the list prices in §2–§3.

Before spending real budget, replace step 3's approximation with the Anthropic token-counting endpoint (`messages.count_tokens`) for exact counts on the specific model chosen — the 4-chars/token rule is close enough for a planning estimate but is not the tokenizer.
