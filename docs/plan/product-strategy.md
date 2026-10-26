# Granite product strategy and roadmap

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-11-14 |
| Status | Proposal from an AI-assisted assessment (see the [AI usage log](../registers/ai-usage-log.md), twenty-fifth session). **Not yet agreed by the team or the supervisor.** |
| Job of this document | What Granite is, for whom, why it can matter, how it should be built and where it goes after FYP-1. It changes slowly |
| Companions | [`fyp1-completion-plan.md`](fyp1-completion-plan.md): the next three weeks. [`execution-status.md`](execution-status.md): what is true today. [`master-plan.md`](master-plan.md): the detailed specification (requirements, screens, schema, rubric mapping) |
| Basis | The repository at `main` `21eba51`, the final [handbook](../../references/university/bs-fyp-handbook-2026.pdf), the registers, and a web check of vendors and papers on 14 November 2026 (sources at the end) |

## 1. Where the project stands

Checked on 14 November 2026. Each row can be reproduced.

| Fact | Evidence |
|---|---|
| A working slice exists: run, check, detect, trace back, verify, review, record, on one workflow with one fault type | [`execution-status.md`](execution-status.md); Python suites pass locally today (core 209 tests, Refund Desk 49, API suite) |
| No product code has changed since 14 October. The three commits since are documents | `git log --since=2026-10-15` |
| **CI on `main` has been red since 11 November.** The web job's dependency audit fails on two high-severity advisories (`undici`, `zod`); `npm audit fix` is offered for both | `gh run list --branch main`; `cd apps/web && npm audit --audit-level=high` |
| Four planning documents overlap: the master plan (2,893 lines), its section 31, the completion plan and the execution status. None is approved | Change log: "C-01 drafted; not yet approved"; [`docs/meetings/`](../meetings/) holds no minutes |
| No GitHub issue exists; work is not assigned anywhere a panel can see | `gh issue list` |
| One fault type, one workflow, ten tasks, one 3B model. The feasibility notes call attribution "easy by construction" | [`research/eval/results/`](../../research/eval/results/) |
| Draft pull request #12 adds six poster versions, each with its own copy of the fonts, to `deliverables/stage-2-fyp1-final/` (about 38,000 added lines) | `gh pr view 12` |
| The registered title promises "Verified Repair and Recovery". The product verifies a cause and never applies a repair | Master plan section 4, principle 4 |
| Commits: Noor 67, Shahoud 53, Saif 8. The registers say most work came from AI-assisted sessions on one machine and that no member has done the code walkthrough | `git shortlog -sne --all`; [Form 10](../registers/form-10-panel-actions.md), ownership note |

**Reading.** The workspace is not what makes the project hard to manage. Its structure passes its own checks and should stay. The difficulty comes from three things: too many plans and no agreed one, a month without implementation, and no decision recorded with the supervisor. The fix is one agreed scope, small enough to finish, with each item owned by a named member.

## 2. Market, November 2026

"Verified" means read from the vendor's own documentation or release notes on 14 November. "Reported" means a press or third-party source only.

### 2.1 Products

| Product | What it does now | Status | What it does not show |
|---|---|---|---|
| **LangSmith Engine** | Groups failing production traces into issues; diagnoses each against the traces and the connected repository; opens a pull request with a fix and a matching evaluator. Never merges on its own | Verified. Public beta; Plus and Enterprise plans; usage-priced, no public rate | No statement that the diagnosis is tested by re-execution with controls. Runs on LangSmith traces |
| **Arize AX: Alyx 2.0, Signal** | Signal reviews traces on a schedule and ranks recurring failures, each with a likely cause and a proposed fix. Alyx plans and investigates across the platform | Verified. Signal generally available on the Enterprise tier (July 2026 notes) | Mechanism and accuracy unpublished |
| **Arize Phoenix: PXI** | An in-product agent that investigates failures and root causes from traces, in the open-source Phoenix | Verified. Beta, Phoenix 17+ | LLM-driven investigation; no verdict rule |
| **Langfuse** | Open source (MIT), self-hosted. 2026 added code evaluators (deterministic Python or TypeScript checks), experiments as a top-level feature that run in GitHub Actions, and an MCP server | Verified | Diagnosis stays with the developer. No replay |
| **Raindrop** | Detects failures that raise no error with its own models. **Simulations** replays real production traffic against a proposed change and reports behaviour changes with a fidelity score | Reported. Series A in September 2026, $50M total; Simulations in public beta by November | Detection is model-judged. Simulations tests a change to the whole agent, not a suspected cause at one step |
| **Patronus Percival** | Analyses agent traces for more than 20 failure modes; suggests prompt fixes; learns from confirmations. Reads OpenTelemetry and OpenInference traces | Verified (docs) | LLM-judged; no replay |
| **Galileo** | Insights Engine groups failure modes across runs; graph view; free tier | Verified (vendor blog) | LLM-judged; no replay |
| **Braintrust** | Evaluation-first platform; Loop agent generates test cases and iterates on prompts; failures become regression cases | Reported only; sources disagree on prices and limits | Not checked against vendor documentation |

### 2.2 Research

| Work | Contribution | Bearing on Granite |
|---|---|---|
| Who&When (ICML 2025) | First attribution benchmark. Best method: 53.5% agent accuracy, 14.2% step accuracy | The baseline numbers everyone quotes |
| Who&When Pro (arXiv 2607.09996) | A larger benchmark across frameworks, single- and multi-agent. Finds that current LLMs do not saturate the task | The benchmark to report on in FYP-2. Not yet read in full |
| AgenTracer (ICLR 2026) | Counterfactual replay to label failures; a small trained tracer model | Replay is used for labelling, not for a per-incident verdict |
| DoVer (arXiv 2512.06749) | Treats attribution as a hypothesis and tests it by intervening and re-executing | Closest prior work. Single replay; no control group |
| EMFA (arXiv 2610.11600) | Models error propagation in a graph, then applies counterfactual verification to find the decisive step | **New since our last review.** Read it before any novelty claim |
| FlowFixer (arXiv 2607.02882) | Symbolic traces, inferred specifications, automatic repair of workflows on Dify, Coze and n8n | Repair is an active research line; the registered title is not ahead of it |
| TraceElephant (arXiv 2604.22708) | Shows that attribution improves sharply with full execution traces over output-only logs | Supports Granite's bet on recorded data flow |

### 2.3 What this means

1. **The gap in the proposal has mostly closed.** In August the comparison said automated diagnosis was emerging. It has now shipped in three commercial products, and verification by counterfactual replay appears in at least three papers. "Nobody does root-cause attribution" and "nobody replays" are both false today.
2. **What is still not shown publicly:** a verdict on a suspected cause that rests on repeated replays *with controls* and a rule fixed in advance; detection by executable checks against a source of truth the workflow does not control, rather than by a model's judgement; one tamper-evident record from detection to a human decision; all of it self-hosted at no cost.
3. **The market's pain is real and stated.** In LangChain's State of Agent Engineering survey (1,300+ respondents), quality is the top blocker to production and 89% already have observability, against 52% with evaluations. Teams can see their traces. They struggle to act on them.
4. **OpenTelemetry's GenAI conventions are the common trace format but are still marked Development** (moved to their own repository in June 2026). Build an adapter; do not hard-wire the attribute names.

## 3. Product vision

**Problem.** A multi-step AI workflow finishes without an error and returns a wrong answer. The team can see the trace in any observability tool. They cannot tell which step introduced the error, and a single re-run that passes proves little because the model answers differently each time.

**User.** A developer or QA reviewer in a small team that builds agent workflows on data it may not send to a foreign SaaS: software houses delivering agents for clients, regulated back-office automation, and student or research teams with no budget. The reviewer who must sign off a fix is the second user.

**What Granite is.** A self-hosted investigation tool that takes one wrong run and returns three things: the step where the error began, a verdict from controlled replays, and a regression test that fails until the cause is fixed.

**In one sentence.** Connect your workflow, declare what "correct" means, and Granite turns a wrong run into a proven cause and a test that keeps it fixed.

**What Granite is not.**

- It is not an observability platform. Langfuse and Phoenix are free, mature and better at capture; Granite should read their traces, not compete with them, and write its verdicts back into them ([integrations strategy](integrations-strategy.md)).
- It does not repair anything on its own. It proposes a corrected value, tests it by replay and leaves the decision to a person.
- It is not a general evaluation suite.

**Why someone would use it every week.** Each confirmed finding leaves a regression case that runs in the team's CI. The value accumulates: after ten incidents the team has ten tests that encode what "correct" means for their workflow. That is the habit to design for, more than the investigation screen.

**Commercial reading, stated plainly.** A hosted platform competing with LangSmith, Arize or Raindrop is not a realistic business for three students: they are funded, integrated and already ship automated diagnosis. Two paths are realistic.

| Path | What it needs | When to judge it |
|---|---|---|
| Open-source tool with a CI integration (`granite-verify` as a GitHub Action), used alongside Langfuse or Phoenix | Trace ingestion from those tools; one mainstream framework adapter; documentation | After FYP-2 Mid, by stars, installs and issues from strangers |
| Reliability reviews for local software houses that ship agents to clients, using Granite as the instrument | Three real conversations, one pilot | During FYP-2, through the stakeholder interviews the handbook already asks for |

Neither earns money before FYP-2 ends. Both are honest things to say to a panel.

## 4. Differentiation

Each line is a claim only when the evidence in the third column exists.

| Differentiator | Against | Evidence required | Today |
|---|---|---|---|
| Verdicts that hold under nondeterminism: N replays with the fix, M without, rule VR-1 fixed in advance | DoVer (single replay); commercial tools (unpublished) | False confirmations on innocent steps, single replay against VR-1, live model at temperature above 0 | Not measured |
| Detection without a model's judgement: executable checks against a source of truth | Raindrop, Percival, Galileo | Detection and false-alarm rates on runs we did not author | Measured only on our own fault |
| Corrections derived from the failed check, not written by hand per step | Our own current design | Refund Desk verified with no repair rule | Not built |
| One hashed, append-only record from detection to decision | All of them | Tamper test; exported report re-verifies | **Built and tested** |
| Runs offline at no cost | All hosted products | Install by a non-owner from the manual | Built; not yet done by a non-owner |
| A regression test from every confirmed finding | Braintrust (manual), Engine (evaluator) | Test fails on the faulty trace, passes on the fixed one | Not built |

Say "we measured X against baseline Y". Do not say "first", "best" or "outperforms" about any product or paper.

## 5. Technical blueprint

Keep the modular monolith ([ADR-001](../adr/adr-001-modular-monolith.md)). Nothing below needs a rewrite.

```
  Sources of runs
  ┌──────────────────────┐ ┌────────────────────────┐ ┌─────────────────────────────┐
  │ Own runner           │ │ Trace import           │ │ Adapters (FYP-2)            │
  │ Refund Desk          │ │ Granite Trace v1 JSON  │ │ LangGraph: fork checkpoint  │
  │ Retail Agent (FYP-2) │ │ Who&When converter     │ │ OTLP GenAI: read-only       │
  └──────────┬───────────┘ └───────────┬────────────┘ └──────────────┬──────────────┘
             └─────────────────────────┼─────────────────────────────┘
                                       ▼
  packages/granite_core  (no framework, no I/O)
    trace ─ redaction ─ dsl ─ checks ─ lineage ─ attribution
    interventions (from the failed check, else a rule) ─ verification VR-1 ─ experiment
    orchestrator (verify ranked suspects within a replay budget)        NEW
    lifecycle ─ evidence ─ regression export                            NEW
                                       ▼
  apps/api  (FastAPI)
    runs · findings · experiments · reviews · evidence · reports
    imports · fault-lab batches · evaluations · investigate              NEW
    jobs: thread pool now; a Postgres job table when a second worker is needed
    SQLite locally · Postgres (Neon free) for the hosted instance
                                       ▼
  apps/web  (React, TypeScript)
    existing six screens + Investigate action · Fault Lab · Evaluation · Import
                                       ▼
  LLM: Ollama locally · any OpenAI-compatible endpoint · recorded cassettes for CI and demos
  research/eval: harness that calls the same core code as the API; results JSON feeds the Evaluation screen
```

| Area | Decision | Reason |
|---|---|---|
| Core library | **Retain.** Typed, framework-free, about 2,000 lines, 97% covered | The strongest asset; every new feature is a module here |
| Hand-written repair rules (`REPAIRS`) | **Replace** with interventions derived from the failed source-of-truth check; keep a rule only where no check holds the correct value | Removes the "you wrote the fix yourselves" objection and a per-step cost no user would pay |
| Verification | **Retain;** add an orchestrator that verifies suspects in rank order within a budget | Turns a manual step into one action and is what the research measures |
| Persistence | **Refactor:** run the suite against Postgres (defect D-08), add Alembic migrations, host on Neon | The demo database is lost on every deploy; the report needs a migration history |
| Jobs | **Retain** the thread pool through FYP-1 | One instance, small batches. A queue adds operations work with no user-visible gain yet |
| Trace intake | **New:** `POST /api/traces` validating Granite Trace v1; replay marked unavailable on imported traces | Makes the product usable on a system the team did not write |
| Framework adapter | **FYP-2:** LangGraph only, using its checkpoint fork to replay from a step | LangGraph's time travel re-executes nodes and allows state edits at a checkpoint, which is the operation VR-1 needs. One adapter done well beats seven shallow ones |
| Third-party sources | **Connectors in a separate package** (`granite_connectors`): Langfuse first, then Phoenix, then an OTLP receiver; all map to Granite Trace v1 through one neutral span record | Teams keep the tools they have; the core stays framework-free. Design: [integrations strategy](integrations-strategy.md) |
| OpenTelemetry | **Post-FYP OTLP receiver**, behind the same interface | The GenAI conventions are still Development; isolate the mapping |
| Authentication | **FYP-2:** GitHub OAuth for reviewers, API keys for ingestion | A reviewer's identity makes the evidence record meaningful. Not needed for a single-team demo |
| Redaction before storage (FR-SEC-01, D-07) | **FYP-2 first milestone** | A stated requirement that is not met; say so in the report |
| Web | **Retain.** Add screens only where a new backend feature needs one | The interface was rebuilt in October; more redesign earns nothing |
| Testing | **Retain** the suites; add one browser end-to-end test in CI | The scripted walkthrough already exists by hand |
| Deployment | **Retain** Render and the container; fix CI first | CD is skipped while CI is red |

**Security and data.** Check expressions stay behind the AST whitelist ([ADR-004](../adr/adr-004-ast-check-dsl.md)). Only synthetic data goes to any hosted model endpoint, and that use is disclosed in Form 13. Secrets stay out of the repository.

**Scale, honestly.** The design is sound for one team and thousands of runs. Multi-tenant hosting needs authentication, per-project isolation, a job queue and object storage for traces. None of that belongs in the FYP.

## 6. Research and innovation

**The weakness to remove.** We wrote the workflow, the fault, the check that catches it and the rule that undoes it. A panel member who sees this will discount every number. The feasibility run also cannot separate Granite from "blame the earliest step whose check fails".

**Questions the project can answer in the time it has.**

| # | Question | Experiment | Baselines | Metric |
|---|---|---|---|---|
| RQ1 | Does a verdict from N fix replays and M controls confirm fewer innocent steps than a single replay? | Live model, temperature above 0; verify true origins and innocent steps both ways | Single replay (DoVer style) | False confirmations and false refutations, Wilson intervals |
| RQ2 | How does attribution degrade when checks are missing, and does verification recover it? | Remove step checks to 100%, 60% and 30% coverage, including the origin's own | Earliest failing check; last agent; an all-at-once LLM judge; Granite ranking alone; Granite with verification | Top-1 accuracy; replays spent per confirmed origin |
| RQ3 | Does it work on failures we did not inject? | A tool-calling Retail Agent on tau-bench retail tasks, judged by tau-bench's own gold end state | Same as RQ2 | Natural failure rate; share investigated to a confirmed origin; two-member blind labels with agreement |
| RQ4 | Where does the method stop working? | Who&When, then Who&When Pro: chat logs with no recorded data flow and no checks | Published numbers | Agent and step accuracy, reported even when poor |

RQ1 and RQ2 fit FYP-1 Final on the three fault types. RQ3 and RQ4 are the FYP-2 evaluation, and stating them now is the "FYP-2 evaluation plan" Form 5 marks.

**Rules.** Pre-register thresholds and commit the file before any run ([`research/eval/prereg-v1.md`](../../research/eval/prereg-v1.md) is the pattern). Report negative results. A tie with the trivial baseline at full check coverage is expected and should be written down as such.

**What is achievable and what is not.**

| Idea | Verdict |
|---|---|
| Interventions derived from checks; verified attribution loop; coverage and nondeterminism ablations | Achievable before FYP-1 Final |
| Retail Agent with an external oracle; Who&When import; LangGraph adapter | Achievable in FYP-2 |
| Suggesting checks automatically and validating them on clean runs | Worth a spike in FYP-2; real research risk |
| A trained attribution model, automatic repair of prompts or code, seven-framework compatibility | Out of reach with three students and no compute; other groups already publish on them |

**Publication.** A workshop or student-track paper is plausible after FYP-2 Mid if RQ1 or RQ2 gives a clear result on more than one workflow. Read EMFA and DoVer in full first; if either already uses a control group, the contribution narrows to the executable-check side and the measured comparison.

## 7. Roadmap

| Phase | Objective | Must exist at the end | Evidence |
|---|---|---|---|
| **A. To FYP-1 Final** (about three weeks) | Remove the circularity; show the method measured against baselines; every member owns a module | The five committed items in the [completion plan](fyp1-completion-plan.md); green CI; report v2.0; tag `v0.2.0`. Optional, if time allows: one real Langfuse round trip ([integrations strategy](integrations-strategy.md), section 5.1) | Pre-registration hash, results JSON, pull requests per member, walkthrough |
| **B. FYP-2 to Mid** (weeks 1 to 8) | Work on systems and failures we did not author, and on traces from the tools teams already use | Langfuse connector with profiles, write-back and scheduled sync; redaction before storage first; Retail Agent on 30 or more tau-bench tasks; LangGraph adapter; Postgres with migrations; redaction; reviewer login; evaluation v1 on RQ1 to RQ3 | Benchmark v1 with a datasheet; evaluation report; four to six stakeholder interviews |
| **C. FYP-2 Mid to Final** (weeks 9 to 15) | Prove it with users; hand it over | Phoenix connector; inferred lineage evaluated; replay hook for a team's own agent; UAT with five to eight people (recruited among Langfuse and Phoenix users); Who&When Pro boundary study; `granite-verify` GitHub Action; handover package; `v1.0.0` | UAT report; final report; install by a stranger from the manual |
| **D. Before anyone pays** (after the FYP) | A tool a team can adopt without us | OTLP receiver; organisations, roles and SSO; hosted Cloud with usage metering; alerts; check packs; a job queue; documentation site; a security review | Three external teams running it for a month |

Phase A is the only one with dates. Phases B and C replace master plan section 32 once the panel sets the FYP-2 milestone register at the Final.

## 8. Free tools and limits

Limits change often. Check each provider's own page before depending on a number; rows marked "check" were not confirmed from a primary source today.

| Need | Use | Limit to know | If it fails |
|---|---|---|---|
| Database | Neon Postgres free plan | 1 GB per project, 100 compute-hours a month, sleeps after 5 idle minutes | SQLite file on a Render disk; Supabase free |
| Hosting | Render free web service | Sleeps after 15 idle minutes, about a minute to wake, 750 hours a month, files lost on restart | Run the container on a laptop for the demo; Azure for Students credit (check) |
| CI and images | GitHub Actions and the Container Registry | Free for public repositories | Already in use |
| Local model | Ollama with `llama3.2:3b`, a 7B model if the laptop allows | 5 to 35 seconds a call on CPU | Record cassettes overnight |
| Hosted model for batches | Groq, Cerebras, Google AI Studio free tiers; OpenRouter `:free` models | Tens of requests a minute, daily caps, terms may allow training on prompts | Synthetic data only; disclose in Form 13; fall back to Ollama |
| GPU | Kaggle and Colab free notebooks (check quotas) | Session and weekly caps | Not needed while the project trains nothing |
| Trace tools to read from | Langfuse and Phoenix, both open source and self-hosted | None at this scale | Either one is enough |
| Student programmes | GitHub Student Developer Pack | Third-party guides report that Copilot student sign-ups were paused in mid-2026 and that some credits changed; verify at education.github.com/pack | None is required by this plan |

The plan needs no paid service. Do not design for one.

## 9. What not to build

- More interface redesign, logo work or poster versions. The interface was rebuilt in October and the poster carries 10 marks.
- A second or third framework adapter before one works end to end.
- Automatic repair of prompts or code.
- Accounts, teams, billing, webhooks or a PDF exporter before FYP-2 Mid.
- A new workflow of our own design. The next system under test must be one whose correctness we do not define (tau-bench).

## Sources

Checked on 14 November 2026.

- LangSmith Engine: [documentation](https://docs.langchain.com/langsmith/engine-overview), [announcement](https://www.langchain.com/blog/introducing-langsmith-engine), [pricing](https://www.langchain.com/pricing-langsmith), [VentureBeat](https://venturebeat.com/orchestration/langsmith-engine-closes-the-agent-debugging-loop-automatically-but-multi-model-enterprises-still-need-a-neutral-layer)
- Arize: [Alyx 2.0](https://arize.com/blog/alyx-2-0-the-ai-agent-that-actually-plans/), [AX release notes, July 2026](https://www.arize.com/docs/ax/release-notes/history/2026/07-2026), [Phoenix PXI release note](https://arize.com/docs/phoenix/release-notes/06-2026/06-02-2026-pxi-agent.md)
- Langfuse: [changelog](https://langfuse.com/changelog), [April 2026 update](https://langfuse.com/blog/2026-04-30-langfuse-april-update)
- Raindrop: [The Next Web on the Series A and Simulations](https://thenextweb.com/news/raindrop-series-a-50m-crv-agent-failures-simulations), [documentation](https://www.raindrop.ai/docs/introduction)
- Patronus [Percival](https://docs.patronus.ai/docs/percival/percival); Galileo on [debugging agents](https://galileo.ai/blog/debug-ai-agents)
- LangChain, [State of Agent Engineering](https://langchain.com/state-of-agent-engineering)
- OpenTelemetry [GenAI span conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/); Dash0, [conventions explained](https://www.dash0.com/knowledge/opentelemetry-genai-semantic-conventions-explained)
- LangGraph [time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel)
- Papers: [Who&When](https://arxiv.org/abs/2505.00212), [Who&When Pro](https://arxiv.org/html/2607.09996), [AgenTracer](https://arxiv.org/abs/2509.03312), [DoVer](https://arxiv.org/pdf/2512.06749), [EMFA](https://arxiv.org/html/2610.11600v1), [FlowFixer](https://arxiv.org/abs/2607.02882), [TraceElephant](https://arxiv.org/html/2604.22708v1)
- Free tiers: [Neon limits](https://neon.com/faqs/free-plan-limits-and-quotas), [Render free](https://render.com/docs/free), [OpenRouter's comparison of free LLM APIs](https://openrouter.ai/blog/tutorials/free-llm-apis-compared/)
