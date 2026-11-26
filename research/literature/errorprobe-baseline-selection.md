# Why ErrorProbe Is the Selected SOTA Baseline

*Compiled from full-text verification of all 7 papers in `agent-autopsy/papers/`. Complements [Full_Literature_Landscape_Analysis.md](literature-landscape-analysis.md) and [Paper_Release_Timeline.md](paper-release-timeline.md).*

---

## Verdict

**ErrorProbe (ACL 2026 Findings)** is selected as the baseline to position the FYP product/contribution against. This is a **performance-based decision, not a recency-based one** — ErrorProbe is not the newest paper in the set (see [Recency — why it's irrelevant here](#recency--why-its-irrelevant-here)), but it is the empirically strongest performer on every benchmark where a direct, same-benchmark comparison against other papers is possible.

---

## 1. The lineage: ErrorProbe inherited and beat both of its ancestors

```
Who&When (ICML 2025)
  Formalized automated failure attribution as a research problem.
  Best baseline: 53.5% agent accuracy / 14.2% step accuracy.
        │
        │ improved by
        ▼
AgenTracer (ICLR 2026)
  Built TracerTraj-2.5K via programmatic fault injection; trained its own 8B model.
  Reported step accuracy: ~37–43% on TracerTraj.
        │
        │ improved by
        ▼
ErrorProbe (ACL 2026 Findings)
  Evaluated on BOTH Who&When's benchmark AND AgenTracer's TracerTraj benchmark directly.
  Three-stage pipeline (Strategist / Investigator / Arbiter) + Verified Episodic Memory.
  Beats both ancestors' own self-reported numbers on their own benchmarks (Section 2).
```

Two other papers in the corpus also descend from Who&When but sit on a **separate branch**, not part of ErrorProbe's data ancestry:

- **TraceElephant** (ACL 2026 Long) — reuses Who&When's underlying systems (CaptainAgent, MagenticOne) but introduces no new attribution algorithm; a data/observability contribution only (fuller traces improve accuracy up to 76.5% relative to partial observation).
- **SDBL** (AAAI 2026) — reuses Who&When's dataset only, no new dataset of its own; two-stage "delineate scope, then localize" method.

**AgentAsk** and **PROTEA** are fully independent of the Who&When lineage — different benchmarks, no citation overlap, not part of this comparison.

---

## 2. Performance verification — same benchmark, cross-paper numbers

Pulled directly from each paper's own results tables (not inferred or estimated):

| Benchmark | Who&When (its own baseline) | AgenTracer | SDBL | **ErrorProbe** |
|---|---|---|---|---|
| Who&When-Algo — step acc. | 14.2% | — | 39.68% (SDBL-EASD, DeepSeek-V3) | **59.50%** (Claude 3.7 Sonnet + memory) |
| Who&When-Hand — step acc. | 14.2% | — | 27.78% (SDBL-EASD, GPT-4o/DeepSeek-V3) | **31.00%** (Qwen3-32B + memory) |
| TracerTraj — step acc. | — | ~37–43% (own trained 8B model) | — | **44.40%** (Qwen3-32B + memory) |
| Who&When-Algo — agent acc. | 53.5% | — | 63.49% (SDBL-EASD, DeepSeek-V3) | **60.30%** (Claude 3.7 Sonnet + memory) |

**ErrorProbe's best reported step accuracy beats the best reported step accuracy of every other paper on every benchmark they share:**

- vs. Who&When's own baseline (Who&When-Algo): **59.50% vs. 14.2%** — more than 4x
- vs. SDBL on the identical Who&When-Algo split: **59.50% vs. 39.68%**
- vs. SDBL on the identical Who&When-Hand split: **31.00% vs. 27.78%**
- vs. AgenTracer on TracerTraj: **44.40% vs. ~37–43%**

Step-level localization is the harder and more decision-relevant metric across this entire literature (agent-level accuracy alone is considered close to solved; step-level is where every paper admits it still struggles — see Section 4). ErrorProbe's lead is largest exactly on this axis.

### Caveat — read before citing this table uncritically

This is a **literature-based comparison, not a controlled experiment**. Each paper chose its own backbone LLM:

- SDBL: GPT-4o, DeepSeek-R1, DeepSeek-V3
- AgenTracer: its own trained 8B model
- ErrorProbe: Claude 3.7 Sonnet, GPT-OSS-120B, Qwen3-32B

No single paper runs all methods on identical backbones to isolate method-quality from backbone-strength. Part of ErrorProbe's margin could come from using a stronger backbone rather than a strictly better method. This is the best evidence obtainable from published numbers without re-implementing all four methods yourself under one controlled protocol — treat it as strong, not airtight, evidence.

There is also a known **cross-paper inconsistency in the Who&When split sizes**: SDBL reports Hand-Crafted=54/Algorithm-Generated=126, while AgenTracer and ErrorProbe both report Algo=127/Hand=58. Most likely different filtering choices per paper, not fabrication — but pull the authoritative counts from Who&When's own released dataset files if exact sizes matter for a proposal.

---

## 3. Gaps in ErrorProbe itself — where a new contribution can still beat it

Selecting ErrorProbe as baseline only makes sense alongside knowing exactly what it still gets wrong, per its own "Limitations" section:

- **Fails on "silent failures"** — technically valid but semantically wrong outputs that trigger no detectable MAST-taxonomy anomaly signal. Its whole pipeline is anomaly-detection-gated, so an error that produces no anomaly signal is invisible to it.
- **Adds real inference latency** from its multi-agent diagnostic team (Strategist → Investigator → Arbiter is not a single pass).
- **Validated on only 3 backbone model families** (Claude 3.7 Sonnet, GPT-OSS-120B, Qwen3-32B) — generalization to other backbones is untested.
- **No paper in the whole 7-paper corpus, ErrorProbe included, tests transfer to a genuinely unseen multi-agent architecture** outside its own benchmark construction (Who&When's CaptainAgent/MagenticOne, AgenTracer's 6-framework ecosystem). This is the one gap confirmed to survive across all 7 papers after full-text reading — see [Full_Literature_Landscape_Analysis.md § 7](literature-landscape-analysis.md#7-what-this-means-for-the-fyp-gap-analysis-updated-from-abstract-level-to-full-text-confirmed).

## 4. Gaps in the other three ACL 2026 papers, for context

- **TraceElephant** — proposes no new attribution algorithm at all; purely a data/observability contribution.
- **AgentAsk** — cannot fix errors originating from an agent's own internal reasoning flaws; only catches errors visible at a message handoff.
- **PROTEA** — no automated root-cause confidence scoring (human must approve every fix); supports only static DAG workflows, not cyclic/dynamic multi-agent graphs.

---

## 5. Recency — why it's irrelevant here

Raised and resolved earlier in this analysis; recorded here so the reasoning isn't re-litigated later.

| Measure | ErrorProbe's standing |
|---|---|
| Official ACL publication date | Tied with TraceElephant, AgentAsk, PROTEA — all four are "ACL 2026," 2–7 July 2026 |
| arXiv preprint date | **19 Apr 2026** — second-oldest of the four (TraceElephant: 24 Apr 2026; PROTEA: 18 May 2026; only AgentAsk, Oct 2025, is older) |

ErrorProbe is **not** the most recent paper by either measure. That's fine — recency was never the criterion for a baseline choice. Performance on shared benchmarks is, and that's what Section 2 establishes.

**DOI (official record):** 10.18653/v1/2026.findings-acl.98 — *Towards Self-Improving Error Diagnosis in Multi-Agent Systems*, Jiazheng Li, Emine Yilmaz, Bei Chen, Dieu-Thu Le. Findings of ACL 2026, pages 2063–2077.

---

## Conclusion

ErrorProbe is the correct baseline because:

1. It is a **direct descendant** of both Who&When and AgenTracer — evaluated on both of their benchmarks directly, not a benchmark it invented itself.
2. It **beats both ancestors' own self-reported numbers**, and also beats SDBL (a third, independent descendant of Who&When) on the identical Who&When splits.
3. Its own stated limitations (silent failures, latency, narrow backbone validation, no test on unseen architectures) mark out exactly where a new contribution has room to differentiate.

Beating ErrorProbe on step-level accuracy — especially on a genuinely unseen multi-agent architecture, which no paper in this corpus has tested — is the most defensible framing for the FYP's experimental claim.
