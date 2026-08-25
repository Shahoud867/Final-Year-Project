# Granite — Resources

*Supplements [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md). Covers everything needed to build the system that isn't a dataset (see [datasets.md](datasets.md) for those). Treat prices/limits below as directional — verify current terms before committing budget, since API/hosting pricing changes independently of this document.*

---

## 1. LLM APIs — agent behavior + diagnosis reasoning

Per the plan doc §6, the LLM is classified as **Core-assist**, not Core-replacement: it powers agent behavior and the diagnosis team's reasoning, but the system must still function (structurally) if swapped.

| Use | Candidate models | Why |
|---|---|---|
| Agent-under-test behavior (the multi-agent systems being diagnosed) | Any instruction-following model reachable via API — pick 1 primary for development, 1 secondary for the generalization/backbone-sensitivity check | Mirrors how every paper in the corpus varies its own backbone (ErrorProbe used Claude 3.7 Sonnet, GPT-OSS-120B, Qwen3-32B) |
| Diagnosis team reasoning (Strategist / Investigator / Arbiter, reproducing ErrorProbe's pipeline) | Same backbone(s) as above, kept consistent with what's used for the ErrorProbe reproduction so the baseline comparison is fair | Comparing your reproduction against ErrorProbe's published numbers is only meaningful if backbone choice is controlled for and disclosed, per the caveat already in [ErrorProbe_Baseline_Selection.md](../03-market-and-literature-research/ErrorProbe_Baseline_Selection.md) |
| Preventive clarification classifier (extension #7) | A small open-weight model or a traditional classifier (not necessarily an LLM at all) — this is deliberately scoped as supervised, not RL, per the plan doc | Keeps this extension light rather than a training-stability project of its own |

**Budget planning — now quantified, see [cost-estimate.md](cost-estimate.md) (2026-08-25, closes risk-register.md R5).** Headline: **≈ $353 recommended for the whole project, ≈ $881 pessimistic ceiling**, computed from measured token counts across all 184 real Who&When cases rather than estimated.

**Correction worth noting:** this section previously assumed benchmark generation was "the single largest API cost driver." Measurement showed the opposite — generation is ~5% of the budget (it runs on the cheap tier, in batch, and is quality-insensitive), while **ErrorProbe reproduction iteration is ~63%** (it must run on a fair-comparison backbone and must be re-run many times before it's correct). The practice that follows: iterate reproduction on a fixed 20-case subset (~$1.20/run) and reserve full 184-case runs for checkpoints. Model plan in cost-estimate.md §5 — cheap/local for volume, **Sonnet 5** reserved for reproduction and evaluation as the fair comparator to ErrorProbe's published Claude 3.7 Sonnet setup.

---

## 2. Multi-agent frameworks to instrument

| Framework | Status vs. the 7-paper corpus | Role |
|---|---|---|
| **CrewAI** | Not used by any of the 7 papers | Primary "unseen architecture" #1 — committed core |
| **Native LangGraph** | Not used by any of the 7 papers (AutoGen, Smolagents, AFlow, MetaGPT, GPTSwarm, MaAS, MasRouter, AG2/CaptainAgent, MagenticOne, OWL-Workforce are the ones already covered) | Primary "unseen architecture" #2 — committed core |
| **OpenAI Agents SDK** *or* a fully custom in-house framework | Not used by any of the 7 papers | "Unseen architecture" #3 — extension #2 |

Cross-check any additional framework choice against the full "already used" list above before treating it as a genuinely novel architecture for the generalization claim — reusing an already-covered framework would undercut the CCP's characteristic-4 claim (unfamiliar issues) in the plan doc §2.

---

## 3. Core libraries and tooling, by subsystem

| Subsystem | Owner | Likely libraries/tools |
|---|---|---|
| Fault injection + benchmark packaging | **Shahoud Shahid** — Data/Benchmark Owner | The multi-agent frameworks above; a Python-based orchestration/scripting layer; Hugging Face `datasets` for packaging and release |
| Execution-graph construction + diagnosis engine | **Muhammad Noor** — Diagnosis Owner | A graph library (e.g. `networkx` for the DAG/graph representation and cycle detection needed for extension #3); standard ML/eval tooling for the confidence-calibration study (extension #5) |
| Controlled counterfactual replay engine + SDK + backend + deployment | **Saif Shahzad** — Platform Owner | A backend API framework (e.g. FastAPI); a lightweight database for trace/diagnosis records (start with SQLite or Postgres — Postgres if the per-project namespacing in extension #4 needs real multi-row isolation testing); Docker for containerized deployment; a minimal dashboard (a simple React/Next.js frontend, or a lighter framework like Streamlit if UI polish is deprioritized in favor of backend rigor) |

Keep the dashboard framework choice deliberately light in FYP-1 — per the plan doc, the dashboard is explicitly *not* where the CCP lives, so time invested there should not come at the expense of the diagnosis engine or benchmark.

---

## 4. Compute and hosting

| Need | Plan |
|---|---|
| Development/training compute | The system is LLM-API-driven, not a from-scratch model-training project (the one exception is the lightweight classifier in extension #7, which is small enough to train on a laptop CPU/GPU or a free-tier cloud notebook) |
| Deployment target (plan doc §13) | A single containerized deployment on a cloud VM or on-prem container — state and justify the specific choice at proposal stage; free/student tiers of major cloud providers are normally sufficient for a single-tenant demo deployment |
| CI compute | GitHub Actions' free tier is sufficient for the regression-check extension (#8) |

---

## 5. Version control, CI, and process

| Tool | Purpose |
|---|---|
| GitHub | Source control, issue tracking, the regression-check GitHub Action (extension #8), and the eventual public benchmark + code release (plan doc §14) |
| GitHub Actions | Extension #8 — one job running the evaluation suite on every push |
| A shared risk register / decision log | Required by the guide itself (§5.3 — any change to scope, architecture, baseline, or ownership needs a recorded decision) — a simple shared doc or GitHub issues label is sufficient, no dedicated tool needed |
| AI usage log | Required alongside this document per the guide's §8.4 — track where AI assistance was used and how CCP-relevant output was verified |

---

## 6. Licensing checklist before build starts

| Component | License to confirm |
|---|---|
| Who&When | MIT — confirmed |
| TracerTraj / AgenTracer | Apache 2.0 — confirmed |
| TraceElephant | CC BY 4.0 (data); code license pending repo release — check before use |
| SDBL | Not stated in-paper — check `github.com/Wen-qiangLi/SDBL` directly before any reuse |
| ErrorProbe | No formal license stated — reproduce methodology from the paper, do not depend on reusing its repository |
| Chosen LLM API provider(s) | Standard commercial API terms — confirm redistribution/training-use restrictions before using any API output as training data for extension #7's classifier |
| CrewAI / LangGraph / OpenAI Agents SDK | Standard open-source framework licenses — check before bundling any framework code into the released SDK rather than just depending on it |
