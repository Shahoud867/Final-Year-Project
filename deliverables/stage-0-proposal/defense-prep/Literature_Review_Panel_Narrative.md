# Literature Review — Workflow & Panel Narrative

This is grounded directly in `markdowns/03-market-and-literature-research/Literature_Review_Sheet.xlsx` (6 sheets: Start Here, Papers, The Numbers, Datasets, The Gap, Lineage) — nothing here is invented; every figure traces back to a paper's own results table or a verified download. Use this to explain *how* the review was done and to argue convincingly that Granite is grounded in, not disconnected from, related work.

---

## 1. The workflow — how the review was actually done

**Step 1 — Find the field.** Searched for automated failure attribution in multi-agent AI systems. Found the field is genuinely new: it barely existed before April 2025, when Who&When (ICML 2025) formalized it as a research problem and built the first human-annotated benchmark.

**Step 2 — Read full text, not abstracts.** All 7 papers were read end-to-end. The "own admitted gap" recorded for each paper is a direct quote from that paper's own Limitations section — this is what makes it defensible to cite a weakness *against* a paper: it's not our interpretation, it's their own admission.

**Step 3 — Track lineage, not just topic.** Rather than treating all 7 papers as one undifferentiated pile, citation links were traced directly (Sheet 6). This revealed **two separate clusters**, not one crowded field: a main lineage descending from Who&When (AgenTracer, SDBL, TraceElephant, ErrorProbe), and two independent papers (AgentAsk, PROTEA) with no citation or benchmark overlap with that lineage at all.

**Step 4 — Pick the baseline on performance, not recency.** ErrorProbe was chosen because it beats both its lineage ancestors (Who&When, AgenTracer) on their own benchmarks — not because it's the newest of the four ACL 2026 papers in the set.

**Step 5 — Verify every number and every license at the source, not at the citation.** Two honesty rules were applied throughout:
- *Verify at the source:* TracerTraj was described as Apache 2.0 in ErrorProbe's own paper — direct repository inspection found **no LICENSE file at all** and no released dataset. That single check is now the standing lesson behind every other license claim in the sheet: a citation is not a license check.
- *Report ranges as ranges:* AgenTracer publishes ~37–43%, not a single number — it's reported as a range everywhere in the sheet, the same discipline applied to our own Spike 1 results.

**Step 6 — Check the department, not just the wider field.** All 660 registered titles across 12 published cohorts (Spring 2019 – Fall 2025) were checked structurally, not just by title, for a prior FYP covering the same ground. Closest match: S24-011-D-HDLM (hallucination detection in one LLM's text) — confirmed as covering roughly one of Granite's four pipeline stages, not the whole problem.

**Step 7 — Turn the reading into a gap statement, not just a summary.** Sheet 5 ("The Gap") is the actual argument the whole Stream A claim rests on: five specific, evidenced gaps, each paired with what Granite does about it.

---

## 2. The numbers — and the caveat that makes them defensible

| Benchmark / metric | Who&When | AgenTracer | SDBL | ErrorProbe (our baseline) |
|---|---|---|---|---|
| Who&When-Algo — step accuracy | 14.2% | — | 39.68% | **59.50%** |
| Who&When-Hand — step accuracy | 14.2% | — | 27.78% | 31.00% |
| TracerTraj — step accuracy | — | ~37–43% | — | 44.40% |
| Who&When-Algo — agent accuracy | 53.5% | — | 63.49% | 60.30% |

**The caveat, say it before a panelist says it to you:** this is a literature-based comparison, not a controlled experiment. Every paper chose its own backbone LLM (SDBL: GPT-4o/DeepSeek; AgenTracer: its own trained 8B; ErrorProbe: Claude 3.7 Sonnet, GPT-OSS-120B, Qwen3-32B). No paper runs all methods on an identical backbone, so part of ErrorProbe's margin could reflect a stronger backbone rather than a better method. Granite controls for this *inside its own experiments* and dual-reports the result rather than presenting a single number as clean.

**Our own POC numbers, for honest comparison (Spike 1, 5 runs, local 3B model):**
- Agent accuracy: 71.4% mean (62.5–85.7% range) vs. ErrorProbe's published 60.30% — but on a **simplified, single-stage** pipeline, not a like-for-like claim.
- Step accuracy: 13.2% mean (0–25% range) vs. ErrorProbe's published 59.50% — far below, and expected, since this is a 1-stage reproduction of ErrorProbe's full 3-stage method.
- Acceptance band: ±10 points of 59.5%, pre-registered in the plan before any run — landing outside it is dual-reported, not quietly revised after the fact.

---

## 3. Datasets — role, verification, and what got cut

| Dataset | Role | License (verified) | Status |
|---|---|---|---|
| Who&When | Baseline reproduction | MIT | ACTIVE — load-bearing |
| tau-bench (retail) | Injection substrate | MIT | ACTIVE |
| GSM8K | Injection substrate | MIT | ACTIVE |
| TracerTraj-2.5K | Would have been baseline data | **No LICENSE file exists** | BLOCKED |
| MATH | Injection substrate | MIT | BENCHED (numeric format fits GSM8K better) |
| MBPP+ | Injection substrate | Permissive | BENCHED |
| GAIA | Injection substrate | Gated, no redistribution | BENCHED, must be purged from history before going public |
| Our own benchmark | The contribution | MIT/CC BY 4.0 (target) | TO BUILD — 500–1,000 labeled traces, ground truth by construction |

**The one line that shows real diligence:** TracerTraj was blocked *after* being planned as baseline data, because direct inspection (not the paper's own description) found no license file and no released dataset. That's the kind of check a panel wants to see happened.

---

## 4. The gap — the actual argument, in five rows

1. **Silent failures are undetectable by every method reviewed** — ErrorProbe's own Limitations section admits its pipeline is anomaly-gated, so an error producing no anomaly is structurally invisible to it. Every other method in the lineage inherits the same gating assumption. → Granite's Semantic Error Diagnostic runs unconditionally, in parallel, never gated on an anomaly, and reports its own abstention rate as a metric.
2. **No paper tests transfer to an unseen architecture** — confirmed after full-text reading of all seven; ErrorProbe's "cross-domain transfer" is transfer across *task* domains within its own tested ecosystem, not architecture transfer. → Granite commits to CrewAI and native LangGraph, neither used by any of the nine papers reviewed.
3. **No method verifies a fix before trusting it** — PROTEA proposes fixes but requires human approval with no automated confidence scoring; nothing else reviewed measures whether a repair actually works before applying it. → Verified Automatic Repair measures a recovery rate over N controlled replays (Spike 5: 97.2 → 108.0).
4. **Nobody measures the false-positive rate** — absent from every paper and all seven commercial platforms checked. → Granite's benchmark includes 15–20% deliberately clean controls, provisional target under 5% FPR.
5. **No prior departmental FYP covers this** — checked against all 660 titles; S24-011-D-HDLM is the closest, covering roughly one of Granite's four stages.

**The one-sentence version to close with:** *"No system checked — academic or commercial — confirms step-level attribution accuracy together with general silent-failure detection, counterfactual fix verification, and cross-architecture generalization, evaluated as one pipeline. The gap is the combination, not any single missing feature."*

---

## 5. Convincing the panel this is genuinely related-work-grounded

If challenged with *"this looks like you're just picking holes in other people's papers"* — the answer is that every gap claimed is the paper's **own stated limitation**, not our interpretation, and every number is pulled from a results table or a verified download, never estimated. If challenged with *"the field looks crowded, why does this need to exist"* — point to Sheet 6: two separate, non-overlapping clusters, six independent follow-ups to a single 2025 paper in about 15 months, and step-level accuracy still stuck at 59.5% despite all of it. That pace and that ceiling, together, are the argument that the problem is real, active, and still open — not solved and not overcrowded.
