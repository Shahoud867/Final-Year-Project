# Granite — Resources

*Supplements [FYP_Scope_CCP_and_Implementation_Plan.md](FYP_Scope_CCP_and_Implementation_Plan.md). Covers everything needed to build the system that isn't a dataset (see [datasets.md](datasets.md) for those). Treat prices/limits below as directional — verify current terms before committing budget, since API/hosting pricing changes independently of this document.*

---

## 1. LLM APIs — agent behavior + diagnosis reasoning

Per the plan doc §6, the LLM is classified as **Core-assist**, not Core-replacement: it powers agent behavior and the diagnosis team's reasoning, but the system must still function (structurally) if swapped.

**Committed model plan, 2026-09-04 (cost-estimate.md §0): local Ollama for every row below, no paid API tier anywhere. Total committed cost: $0.**

| Use | Committed model | Why |
|---|---|---|
| Agent-under-test behavior (the multi-agent systems being diagnosed) | Local Ollama (the same class already used for all 8 real POC spikes) | $0, already proven to work for this at POC stage |
| Diagnosis team reasoning (Strategist / Investigator / Arbiter, reproducing ErrorProbe's pipeline) | Local Ollama — same backbone as the reproduction target below | Kept internally consistent; the fair-comparison backbone match to ErrorProbe's own Claude 3.7 Sonnet setup is knowingly given up for cost, not overlooked — see the tradeoff recorded in cost-estimate.md §0 |
| Preventive clarification classifier (extension #7) | A small open-weight model or a traditional classifier (not necessarily an LLM at all) — deliberately scoped as supervised, not RL | $0 either way |

**Budget: $0 committed** (cost-estimate.md §0, 2026-09-04 decision). The **≈$353 recommended / ≈$881 ceiling** figures below describe the paid-tier alternative that was priced and explicitly not chosen — kept for reference, not the plan.

**Correction worth noting, still true regardless of which model plan is chosen:** this section previously assumed benchmark generation was "the single largest API cost driver." Measurement showed the opposite — generation is ~5% of what a paid-tier budget would spend, while **ErrorProbe reproduction iteration is ~63%** of it (it must be re-run many times before it's correct). Under the committed $0 plan this is moot for cost, but the practice still applies for *time*: iterate reproduction on a fixed 20-case subset before running all 184 cases, to keep local-model turnaround manageable.

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
