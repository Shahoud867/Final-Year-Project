# Silent-Failure Detection Implementation & General Multi-Agent Testing Strategies

*Pasted reference material, 2026-08-23. See the honesty check at the bottom — these are documented as common industry practice, not a novelty claim, consistent with the rest of this project's rigor about what's actually differentiated vs. standard toolkit.*

---

## Implementing Task-Constraint Verification for Silent Failures

In multi-agent systems, a silent failure is one of the most dangerous errors: the agent produces an output that looks completely valid and grammatically correct, but is semantically wrong, with no detectable anomaly signal.

Granite's supervisor briefing states this mechanism must rely on rule-based or graph-based logic, not an unpredictable LLM call (matches architecture-sketch.md's committed 0%-API silent-failure module). Practical implementation, via standard software engineering techniques:

### 1. Schema and Type Enforcement

The most robust way to catch a hallucinating agent is to force it to communicate in structured data formats.

- **Define Strict Models:** instead of letting the agent return a raw text string, require it to return a JSON object.
- **Automatic Validation:** pass that JSON directly through a data validation library like Pydantic. If the agent hallucinates a string where an integer was required, the validation model throws an error, instantly transforming a "silent" failure into a loud, catchable exception.
- **Default Deny:** reject any output that contains unexpected extra fields, which often indicate the agent went off-script.

### 2. Domain-Specific Rule Checks

Task-constraint verification means writing pure Python code to check the boundaries of the agent's answer.

- **Logical Assertions:** if an agent is tasked with writing code, run an automated unit test against it. If it fails, the agent failed silently.
- **Boundary Checking:** if an agent calculates a financial discount, use a simple script to verify the final price is strictly less than the original price.
- **Format Verification:** if an agent is designed to extract information into CSV rows, check that the output has the exact required number of columns before passing it down the pipeline.

### 3. Execution State Tracking

Because multi-agent frameworks pass state from one agent to another, errors often compound.

- **State Signatures:** log the exact state of the variables before and after an agent takes action.
- **Trace Comparison:** if an agent's required task was to update a database, but the execution trace shows no tool was ever called to connect to the backend, you have mathematically proven a silent failure occurred.

By treating the agents as unreliable data sources that must be aggressively validated, you can build a highly effective detection module without needing advanced AI techniques.

**Open planning question this material raised:** what specific task will the dummy multi-agent system perform during the Mid-1 presentation (writing code, answering customer queries, fetching web data)? See the recommendation below.

---

## Current Strategies to Test a Multiagent System

Testing multiagent systems involves a combination of traditional software testing methods and specialized techniques that account for the unique aspects of AI systems:

- **Benchmark Datasets:** use benchmark datasets to evaluate the agent's performance across various scenarios and inputs.
- **Workflow Tracing:** implement workflow tracing to monitor the agent's decision-making process and identify potential issues.
- **Simulations:** conduct simulations to test the agent's behavior under different conditions and edge cases.
- **Tool-Call Validation:** verify that the agent correctly calls external tools and APIs, ensuring actions are authorized and executed as intended.
- **Human Review:** utilize human review to assess the quality of the agent's responses and ensure compliance with quality standards.
- **Automated Evaluations:** use automated evaluations to quickly assess the agent's performance and identify areas for improvement.
- **Regression Tracking:** track regression changes to ensure the agent's behavior remains consistent and reliable over time.
- **Security Testing:** conduct security testing to identify vulnerabilities and ensure the agent's behavior is safe and secure.

---

## Honesty check: common toolkit vs. Granite-specific — checked against everything already researched

**Short answer: all of it is common, standard practice — none of these individual techniques or strategies are unique to Granite.** That's not a problem; it's consistent with the project's own established framing (see [ErrorProbe_Baseline_Selection.md](../03-market-and-literature-research/ErrorProbe_Baseline_Selection.md) and the "anticipated objection, answered in advance" already on the record: *"No individual mechanism is new... The claim was never the parts."*

| Technique/strategy | Already confirmed present elsewhere | Verdict |
|---|---|---|
| Schema/type enforcement (Pydantic, JSON validation) | Standard software engineering, used across the entire industry, not agent-specific at all | Common |
| Domain-specific rule checks (unit tests, boundary checks, format checks) | DeepEval's entire product is assertion-based testing exactly like this | Common |
| Execution state tracking / trace comparison | Confirmed the *core competency* of every commercial platform checked — LangSmith, Langfuse, Braintrust, Arize, Maxim, Opik all do this as their baseline feature | Common — actually the least differentiated thing on this whole list |
| Benchmark Datasets | Standard ML/AI evaluation practice; also literally what Granite's own evaluation plan already does (Who&When, the new cross-architecture benchmark) | Common |
| Workflow Tracing | Same as execution state tracking above — universal | Common |
| Simulations | Maxim AI explicitly does this — "simulation-based testing... synthetic users and custom personas" | Common |
| Tool-Call Validation | Standard part of any observability platform's baseline feature set | Common |
| Human Review | Universal — Braintrust's own workflow is literally "open the failed run, add a root-cause label by hand" | Common |
| Automated Evaluations | DeepEval's whole positioning; LLM-as-judge is used everywhere | Common |
| Regression Tracking | DeepEval's core positioning again; this is also why the original CI-regression-check extension was cut from the frozen 16 during CCP filtering — flagged as significant commercial overlap at the time | Common — already known and accounted for |
| Security Testing | Standard practice; matches R16's threat model, itself framed as baseline table stakes, not a differentiator | Common |

**What this means, honestly, for the project:** none of these building blocks are the differentiation claim, and none of them should be presented as if they were. They are the correct, sensible way to *implement* the silent-failure module and general test coverage — exactly the "own logic, not an LLM wrapper" approach already committed to in architecture-sketch.md. The actual differentiation (verified across the whole literature and market check) is in what these common building blocks are assembled into and measured against, specifically:

1. Applying them as a formally **benchmarked silent-failure-detection capability** with a labeled ground-truth dataset — nobody else publishes this measurement, even though the underlying validation code is standard.
2. Feeding into **automated root-cause attribution** (which agent, which step) — not just "this output looks wrong."
3. Feeding into **Verified Automatic Repair, with a measured recovery rate** — testing whether a fix works before applying it, which no paper or platform checked does.
4. Proven on **architectures no prior paper tested** — the cross-architecture generalization claim.

Use every technique listed above — they're the right engineering choices, and several (schema validation, rule checks) are already exactly what the committed silent-failure module design calls for. Just don't describe them as novel in the report or defense; describe the *assembly and measurement* as novel, and the techniques as the correct, standard way to build it.

---

## Considered and rejected: 3 proposed "novel ML-driven" strategies (2026-08-23)

Pasted for evaluation: (1) a Latent-Space Perception classifier using embedding-based semantic-drift detection, (2) Multi-Indicator Confluence combining perplexity + latency + semantic-distance anomaly scores, (3) ARIMA-based time-series anomaly detection over graph-execution metrics. All three were rejected — logged here rather than silently discarded, matching the same practice already used for the GraphTracer/FALAT baseline reversal and the AgentRx removal.

| Strategy | Verdict | Why |
|---|---|---|
| Latent-Space Perception (embedding semantic drift) | Rejected | Targets a different failure mode (topical/semantic drift) than the validated pattern (a plausible near-miss value that reads as on-topic and correct). Also not novel — this is RAGAS/DeepEval-style embedding-similarity scoring, already standard industry practice. |
| Multi-Indicator Confluence (perplexity + latency + semantic-distance) | Rejected | Detects *statistical anomalies*. Granite's own definition of a silent failure is an output with **no anomaly signal** — adopting an anomaly-detection method here reintroduces exactly the blind spot the project critiques ErrorProbe for. Also not novel — confidence/latency anomaly detection is decades-old ops practice. |
| ARIMA time-series anomaly detection | Rejected | Same core problem as above (anomaly-based, not silent-failure-shaped) plus it's standard ops/infra monitoring, not agent-specific or new. |

**Why this matters for the module design:** the project's own definition of "silent failure" *is* the absence of an anomaly signal — schema validity, no latency spike, no confidence drop, no topical drift. Any detector built on anomaly/drift/statistical-outlier signals structurally cannot catch the exact failure class the module exists to catch. This isn't a novelty judgment call, it's a category mismatch.

---

## Two new alternatives proposed instead (same module, core item #6 — Semantic Error Diagnostic)

Both are complementary to the existing rule-based checker (schema/type enforcement, domain rule checks, execution-state tracking, §1 above) — they add cross-referencing power the single-agent-output checks above can't provide, and neither appears in the commercial-platform comparison already done in this project ([Commercial_Product_Comparison.md](../03-market-and-literature-research/Commercial_Product_Comparison.md)).

### Cross-Agent Consistency Verification

When two or more agents in the same trace independently produce or reference the same fact (a price, a date, a name, a count), check that their values agree with each other — not against an external ground truth (which may not exist at inference time), but against each other. A silent failure often shows up as one agent's stated value silently diverging from another agent's earlier-stated value for the same fact, even though each individual output looks locally well-formed and confident.

- **Mechanism:** rule/graph-based, not LLM-judged — extract typed facts (numbers, dates, named entities) per node via existing schema-validation output, then diff extracted facts across nodes that reference the same entity/field.
- **Why it's not already covered:** execution-state tracking (§1.3 above) checks a *single* agent's state before/after; this checks *agreement between independent agents*, which is a different, currently-uncovered failure shape.
- **Fits the 0%-API commitment:** yes — pure comparison logic over already-extracted structured fields, no additional model call.

### Constraint Provenance Tracing

For any final output value, trace which upstream node(s) actually produced or last touched that value's inputs. If the final output states a constraint was satisfied (e.g., "under budget," "in stock," "wheelchair-accessible") but no upstream node in the trace ever actually checked that constraint against real data, flag it — the agent asserted compliance without any traceable verification step behind it.

- **Mechanism:** graph-based provenance walk over the execution graph (already part of the core data model) — for each claimed constraint in the final output, check whether a corresponding tool-call/check node exists upstream that could have verified it.
- **Why it's not already covered:** §1.3's "trace comparison" example (no DB tool called, so no DB update happened) checks for a *missing action*; this generalizes it to check for a missing *verification* behind any claimed constraint, which is a broader and currently-uncovered class.
- **Fits the 0%-API commitment:** yes — pure graph traversal, no model call.

Both remain to be POC-tested before being added to the frozen 16-feature list (§7.0 of the plan doc) — right now they're design proposals, not validated mechanisms, same status the existing rule-based checker had before Spike 4.

---

## Recommended Mid-1 dummy task, given what's already active

Per [datasets.md §6](../01-planning-and-scope/datasets.md), the active build plan is **GSM8K** (cheap prototyping) + **tau-bench retail** (the real benchmark-building pass). For the Mid-1 demo specifically:

**Recommend GSM8K-style numeric/math tasks** — not tau-bench retail — for the live Mid-1 presentation, because it's the *already-proven* path: Spike 4's silent-failure mechanism was already validated on exactly this pattern (a plausible near-miss numeric value, $20.00 vs. $19.75 true). A live demo built on an already-working mechanism is lower risk than debugging a new task type in front of a panel. Save tau-bench retail's richer, multi-turn customer-support scenario for the fuller FYP-2 benchmark and later demos, once there's more runway to handle its added complexity.
