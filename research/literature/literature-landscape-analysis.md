# Multi-Agent Failure Attribution — Full Literature Landscape

*All seven papers read in full from `agent-autopsy/papers/`. This supersedes the abstract-level verification in `AgenTracer_vs_WhoWhen_Analysis.md`.*

> **Status: current, still the evidence base — verified accurate as of the latest FYP scope work.** Nothing in this file has been superseded; it is the foundation [ErrorProbe_Baseline_Selection.md](errorprobe-baseline-selection.md) and [FYP_Scope_CCP_and_Implementation_Plan.md](../../deliverables/stage-0-proposal/proposal-documents/FYP_Scope_CCP_and_Implementation_Plan.md) build on (citation lineage §2, dataset table §4, licensing §3, and the confirmed-gap finding in §7 are all still directly load-bearing in the current plan). Read this first, then the two files above for how it turned into a scope decision.

---

## 1. Timestamps

| Paper | Venue | Confirmed date | Precision |
|---|---|---|---|
| Who&When | ICML 2025 | arXiv:2505.00212, submitted **30-04-25** | arXiv-verified (WebFetch) |
| AgenTracer | ICLR 2026 | arXiv:2509.03312, submitted **03-09-25** (v2: 04-09-25); poster presented **24-04-26** | arXiv-verified (WebFetch) |
| Scope Delineation Before Localization (SDBL) | AAAI-26 | 2026, page 33108 | Conference proceedings year only — no exact date in-paper |
| TraceElephant ("Seeing the Whole Elephant") | ACL 2026 (Long) | **02–07 July 2026**, San Diego | Confirmed from paper footer |
| ErrorProbe ("Towards Self-Improving Error Diagnosis") | ACL 2026 Findings | **02–07 July 2026**, San Diego | Confirmed from paper footer |
| AgentAsk | ACL 2026 (Long) | **02–07 July 2026**, San Diego | Confirmed from paper footer |
| PROTEA | ACL 2026 (System Demonstrations) | **02–07 July 2026**, San Diego | Confirmed from paper footer |

**Pace of the field:** Who&When (Apr 2025) → AgenTracer (Sep 2025, ~5 months later) → four more papers landing across AAAI-26 and ACL 2026 within roughly the following 9 months. From "barely a benchmark exists" to six independent follow-ups across ICML/ICLR/AAAI/ACL in about 15 months.

---

## 2. Improvement/citation chain (confirmed by direct in-paper citation, not inferred)

```
Who&When (Apr 2025, ICML)
   ├──→ AgenTracer (Sep 2025, ICLR 2026) — cites Who&When directly; builds TracerTraj-2.5K
   ├──→ SDBL (AAAI 2026) — explicitly adopts Who&When's ALL_AT_ONCE/STEP_BY_STEP/BINARY_SEARCH as its baselines
   └──→ TraceElephant (ACL 2026) — reuses Who&When's underlying systems (CaptainAgent, MagenticOne);
        argues the field's methods were bottlenecked by incomplete trace access, not just weak algorithms
        └──→ ErrorProbe (ACL 2026 Findings) — evaluates against BOTH Who&When AND AgenTracer's TracerTraj;
             cites both directly; the deepest synthesis of the lineage

AgentAsk (ACL 2026) — INDEPENDENT. Different benchmarks entirely (GSM8K/MATH/MMLU/HumanEval/MBPP via
   GPTSwarm/AFlow/MaAS/MasRouter frameworks). No citation of or benchmark overlap with Who&When/TracerTraj.

PROTEA (ACL 2026 Demo) — INDEPENDENT. Sony Group industry paper. Internal/confidential production
   workflows. No citation link to the Who&When lineage.
```

Two unrelated clusters exist, not one crowded field: the **Who&When → AgenTracer → {SDBL, TraceElephant} → ErrorProbe** post-hoc root-cause-attribution lineage, and two structurally different, disconnected efforts — AgentAsk's *preventive* edge-level clarification, and PROTEA's human-in-the-loop debugging tool.

---

## 3. Licensing — can we reuse their GitHub/HuggingFace content?

| Paper | License (confirmed in-paper) | Reuse verdict |
|---|---|---|
| **Who&When** | **MIT** — confirmed directly in ErrorProbe's "Licensing and Intended Use" section, citing Zhang et al. 2025b | Yes — fully permissive |
| **AgenTracer / TracerTraj** | **Corrected 2026-08-22 by direct repo inspection: "Apache 2.0" was ErrorProbe's own paper describing AgenTracer, not a verified fact.** The actual repo has no LICENSE file; its README states data/weights are "committed to" open-sourcing "upon acceptance of the paper" — not yet released | No — only a data-generation pipeline and one 127-row sample file are real. The full 2.5K dataset and AgenTracer-8B weights are not public yet. Code: `github.com/bingreeky/AgenTracer` |
| **TraceElephant** | **CC BY 4.0** for traces/annotations (its own Appendix A.10, "Artifact License and Usage Terms"); benchmark code to be released under an unspecified "permissive open-source license" | Yes for data (with attribution); confirm code license once the accompanying repo publishes it |
| **SDBL** | Not stated in-paper. Code at `github.com/Wen-qiangLi/SDBL`, no license badge visible in the text extracted | Unconfirmed — check the repo directly before reuse |
| **ErrorProbe** | No new dataset released (evaluates on others' benchmarks); states research-only intent, not a formal license | Nothing to reuse as a dataset; check repo for code license if one exists |
| **AgentAsk** | Not stated in the pages read. Has a "Code" link on the title page (USTC-affiliated) | Unconfirmed — check the repo directly |
| **PROTEA** | N/A — internal Sony production workflows, not released publicly | Nothing to reuse; closed industry demo |

**Correction, 2026-08-22:** only Who&When is actually confirmed permissively licensed and fully available (MIT, 184 real cases downloaded and confirmed). AgenTracer/TracerTraj turned out closer to RedShield's Spotlight-Guard situation than originally claimed — real code exists, but the dataset and model weights aren't released, and there's no license file to rely on. The "materially better position than RedShield" claim was true for Who&When alone, not for both artifacts as originally stated.

---

## 4. Datasets used, per paper

| Paper | Dataset(s) | Origin | Ground truth | Size (as stated in that paper) |
|---|---|---|---|---|
| Who&When | Who&When benchmark | Algorithm-generated (CaptainAgent/AG2) + hand-crafted (MagenticOne), on GAIA + AssistantBench | Human-annotated (culprit agent + decisive step) | 127 algorithm-generated + hand-crafted systems, 184 annotation tasks total |
| AgenTracer | TracerTraj-2.5K | Programmatic fault injection across 6 frameworks (MetaGPT, AutoGen, Smolagents, AgentPrune, AFlow, OWL-Workforce) on 7 datasets (MBPP+, KodCode, GSM8K, MATH, GAIA, HotpotQA, + others) | Synthetic (fault injected by a known perturbation operator — ground truth exact by construction) | 2,000+ trajectories |
| SDBL | Reuses Who&When only — no new dataset | Same as Who&When | Same as Who&When | HC=54 / AG=126 (per SDBL's own Table 1) |
| TraceElephant | TraceElephant benchmark | Same underlying systems as Who&When (CaptainAgent, MagenticOne) on GAIA, AssistantBench, SWE-Bench, but capturing **full** input+output traces, not outputs only | Human-annotated, 3 expert annotators | Not explicitly re-stated in the pages read beyond the underlying task sources |
| ErrorProbe | TracerTraj + Who&When-Algo + Who&When-Hand (3 benchmarks) | Reuses AgenTracer's and Who&When's data directly | Synthetic (TracerTraj) + human-annotated (Who&When) | Algo=127 / Hand=58 (per ErrorProbe's own Table 4 — differs slightly from SDBL's HC/AG counts) |
| AgentAsk | GSM8K, MATH, MMLU, HumanEval, MBPP + a self-collected 824-message corpus for its own taxonomy | Standard public benchmarks + 4 MAS frameworks (GPTSwarm, AFlow, MaAS, MasRouter) | Standard benchmark ground truth; taxonomy corpus annotated by multiple professional annotators, Fleiss' κ = 0.84 | 824 annotated agent-to-agent messages for taxonomy; standard benchmark sizes for evaluation |
| PROTEA | Two internal Sony production-adjacent workflows + 11 LLM-generated multi-agent workflows for a stress test | Internal, confidential | Human-provided or backward-inferred node-level references | Not disclosed (confidentiality stated explicitly) |

**Note on a cross-paper inconsistency:** Who&When's own split sizes are reported differently by the papers that reuse it — SDBL states Hand-Crafted=54 / Algorithm-Generated=126, while AgenTracer and ErrorProbe both state Algo=127 / Hand=58. Most likely explained by different filtering/exclusion choices in each downstream paper, not fabrication — but pull the authoritative count directly from Who&When's own released dataset files if exact numbers matter for a proposal, rather than trusting a secondary paper's restated figure.

---

## 5. Gaps, per paper (each paper's own admitted limitation)

- **Who&When**: step-level accuracy only 14.2% best-case; even o1/DeepSeek-R1 "fail to achieve practical usability."
- **AgenTracer**: still modest step accuracy even trained (~37–43% range); only tested within its own 6-framework ecosystem; quality bottlenecked by its analyzer LLM's own capability.
- **SDBL**: best step accuracy still only ~33–40% even with its two-stage method — the majority of cases remain misattributed at the step level.
- **TraceElephant**: proposes no new attribution algorithm at all — it is a *data/observability* contribution, arguing prior methods were partly failing from incomplete trace access rather than purely weak reasoning (full traces improve accuracy up to 76.5% relative to partial observation).
- **ErrorProbe** (from its own "Limitations" section): explicitly fails on **"silent failures"** — technically valid but semantically wrong outputs that trigger no detectable MAST-taxonomy anomaly signal; adds real inference latency from its multi-agent diagnostic team; validated on only 3 backbone model families (Claude 3.7 Sonnet, GPT-OSS-120B, Qwen3 32B).
- **AgentAsk** (from its own "Limitations" section): cannot fix errors originating from an individual agent's own internal flaws (hallucination, reasoning gaps) — only catches errors visible *at* a message handoff.
- **PROTEA**: no automated root-cause confidence scoring at all — a human must inspect and approve every fix; supports only static DAG workflows, explicitly not cyclic/dynamic multi-agent graphs (stated as future work).

---

## 6. Novelty, per paper

- **Who&When**: first to formalize automated failure attribution as a research problem with a real, human-annotated benchmark and three baseline methods.
- **AgenTracer**: first to automate annotation at scale via counterfactual replay + programmatic fault injection (removing the 30-hour-per-annotator human cost); trains a genuinely small (8B) model that beats giant proprietary LLMs on this task.
- **SDBL**: a two-stage "delineate scope, then localize" strategy inspired directly by observed novice-vs-expert human debugging behavior; introduces "Overstep" and "Loop" as predefined expertise heuristics.
- **TraceElephant**: demonstrates the field's bottleneck was partly an observability problem (missing input context), not purely an algorithmic one — a benchmark/data contribution, not a new attribution method.
- **ErrorProbe**: a three-stage pipeline (MAST-taxonomy structural decomposition → symptom-driven backward tracing → Strategist/Investigator/Arbiter verification team) plus a **Verified Episodic Memory** that only commits new failure patterns to memory once independently confirmed by executable evidence — explicitly designed to prevent "hallucinated" error-pattern pollution. The most mechanistically sophisticated of the seven.
- **AgentAsk**: an edge-level (message-handoff) failure taxonomy (Data Gap, Signal Corruption, Referential Drift, Capability Gap) plus a lightweight, RL-trained (novel "E-GRPO" — an extension of Group Relative Policy Optimization), architecture-agnostic clarification module that intervenes *before* an error propagates, rather than diagnosing it after the fact.
- **PROTEA**: a full interactive developer tool (evaluate → localize bottleneck → propose prompt fix → auto-rerun → compare before/after) validated with a small (n=6) formative user study of real LLM developers — close to a genuine product, but evaluated at much lower rigor than the academic papers (no F1/precision/recall against ground truth, only two internal case studies and an 11-workflow stress test).

---

## 7. What this means for the FYP gap analysis (updated from abstract-level to full-text-confirmed)

The earlier analysis (`AgenTracer_vs_WhoWhen_Analysis.md`) flagged "cross-domain generalization" as untested and open. Having now read ErrorProbe in full: its "cross-domain transfer" claim (Section 6.2, "Memory Scaling") is real but **narrower than it first appeared** — it is verified transfer *across task domains* (coding ↔ math, e.g., memory built from KodCode improving diagnosis on GSM8K/MATH) **within its own already-tested benchmark ecosystem** (TracerTraj, Who&When-Algo, Who&When-Hand). None of the seven papers test transfer to a **genuinely unseen multi-agent framework or architecture that was never used during any of these papers' own benchmark construction** — e.g., a custom system a student team builds independently. That specific gap survives fully intact after reading all seven papers in full — this is now a confirmed finding grounded in complete text, not an inference from abstracts.
