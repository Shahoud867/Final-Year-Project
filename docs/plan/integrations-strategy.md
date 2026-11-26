# Integrations strategy: Granite on Langfuse and Arize Phoenix

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-11-15 |
| Status | Proposal from an AI-assisted session (AI usage log, twenty-seventh session). **Section 5.1 is implemented** (twenty-eighth session, 2026-11-15) with Phoenix brought forward from 5.2; what was built and where it departs from this proposal is in [ADR-012](../adr/adr-012-observability-connectors.md) and change C-07 in the [change log](../registers/change-log.md). Sections 5.2 onward remain proposals |
| Job of this document | How Granite works on teams' real AI applications through the observability tools they already use; what that changes in the product, the architecture, the roadmap and the business case |
| Companions | [`product-strategy.md`](product-strategy.md) (vision and roadmap), [`fyp1-completion-plan.md`](fyp1-completion-plan.md) (what is committed now) |
| Basis | Langfuse and Arize Phoenix documentation and changelogs read on 15 November 2026 (sources at the end); Granite at branch `feat/fyp1-final-scope` |

## 1. The idea in one paragraph

Teams that run AI agents in production already send their traces to Langfuse or Phoenix. Those tools show what happened. Granite should read those traces, run the team's checks on them, find the step where a wrong answer began, and write the result back into the tool the team already looks at, as a score or an annotation on the right span. Langfuse and Phoenix stay where traces are captured and viewed; Granite becomes the step after: *this run was wrong, it began here, and here is the proof*. That makes the two tools partners, not competitors, and makes Granite useful on day one without asking a team to re-instrument anything.

## 2. What the platforms actually offer (checked 15 November 2026)

| | Langfuse | Arize Phoenix |
|---|---|---|
| Licence and hosting | Open source (MIT), self-hosted or Cloud | Open source, self-hosted or Arize-hosted |
| Free tier | Cloud Hobby: free, about 50k units a month, 30-day data access (third-party summaries of the pricing page; verify) | Self-hosted at no cost |
| Read traces | `GET /api/public/v2/observations`: cursor pagination, `fields` groups (`core` always: id, traceId, parentObservationId, type, times; `io` for input and output), filters by trace and time. Observation types include GENERATION, SPAN, EVENT, AGENT, TOOL, CHAIN, RETRIEVER, EVALUATOR, EMBEDDING, GUARDRAIL. Older `GET /api/public/traces` and v1 observations still work but are deprecated; **self-hosted Langfuse v3 should keep using v1** | `GET /v1/projects/{project}/spans/otlpv1`: spans in a time range, cursor pagination; filters by span name, kind and status from server 13.15. Attributes follow OpenInference: `openinference.span.kind` (LLM, TOOL, AGENT, CHAIN, RETRIEVER, …), `input.value` |
| Write results back | `POST /api/public/scores`: on a trace, an observation or a session; NUMERIC, CATEGORICAL or BOOLEAN (sent as 1/0); upserts on id | `POST /v1/span_annotations`: on a span by OpenTelemetry span id; an annotation of the same name is overwritten unless its `identifier` differs |
| Auth | HTTP Basic: project public key as user, secret key as password | `api_key` header or `Authorization: Bearer` |
| Push events | No confirmed native webhook for new traces; third-party tools poll | Not found |
| Known quirks | v2 endpoints can lag up to 15 minutes for data from older SDKs or direct OpenTelemetry exporters | Span API features depend on the server version |

Two consequences follow. **Ingestion is pull-based** (poll with a cursor and a time window), because neither platform pushes. And **the connector must hide API versions**, because Langfuse already has two generations of read endpoints in use at once.

## 3. What Granite can and cannot do on imported traces

This is the honest boundary. It decides the design.

| Granite step | On its own workflows (today) | On a trace imported from Langfuse or Phoenix |
|---|---|---|
| Record | Its runner records every step and declares which step read which value | The trace already exists; Granite maps it |
| Check | Checks address step ids and call a source of truth | Same check language, addressed through a per-connection **profile** that names the steps (section 4.2); a source of truth needs a connector of its own (section 4.5) |
| Detect | Failed outcome check on a completed run | Same |
| Trace back | Walks declared data flow | **Data flow is not in these traces.** They hold nesting and timing, not "who read what". Granite infers it (section 4.3), and an inferred edge counts for less than a declared one |
| Verify by replay | Re-executes its own steps | **Not possible in general:** Granite cannot re-run someone else's production agent. Imported findings stop at V1 (evidence-supported) unless the application exposes a replay hook (section 4.6) |
| Review, evidence, regression export | Yes | Yes; the regression test re-checks the stored trace, and re-runs it only where a replay hook exists |

Say this in the product and in the report. The strongest, most defensible claim on imported traces is **detection and ranked attribution with evidence, written back where the team works**; replay-verified attribution on imported traces is a later, opt-in capability.

## 4. Architecture

### 4.1 Shape

```
 Team's application ──traces──▶ Langfuse  ─┐                          ┌─▶ score on the trace / observation
                    ──traces──▶ Phoenix   ─┤  pull, cursor + window    │   (Langfuse)
                    ──OTLP────▶ (later) ───┤                           ├─▶ span annotation (Phoenix)
                                           ▼                           │
  packages/granite_connectors   Source plugins ─▶ SpanRecord ─▶ Mapper + Profile ─▶ Granite Trace v1
  (new package, outside core)   Sink plugins  ◀──────── verdicts ◀─────────────────────────────┐
                                TruthProvider plugins (HTTP, static file)                      │
                                Replayer plugins (own runner, replay hook, LangGraph fork)      │
                                                                                               │
  packages/granite_core (unchanged contract): checks ─ attribution ─ verification ─ evidence ──┘
  apps/api: connections · sync jobs · imported runs · findings     apps/web: Connections screen
```

Rules that keep this extensible for years:

1. **Granite Trace v1 stays the only contract the core sees.** Every source is mapped into it; the core never imports a connector. This already holds today ([ADR-009](../adr/adr-009-trace-schema-v1.md)) and is enforced by `scripts/check_architecture.py`.
2. **Connectors live in their own package** (`packages/granite_connectors`), installable separately, discovered through Python entry points. A new platform is a new plugin, not a core change.
3. **Four plugin interfaces**, each small: `Source` (list traces since a cursor; yields `SpanRecord`s), `Sink` (publish a verdict), `TruthProvider` (answer `truth.<name>(...)` for checks), `Replayer` (re-execute from a step with a patch). Each declares its capabilities, so the interface can say "replay not available" instead of failing.
4. **One neutral intermediate, `SpanRecord`** (id, parent id, name, kind, start, end, input, output, status, attributes), shaped after OpenTelemetry spans. Langfuse observations, Phoenix spans and a future OTLP receiver all produce it, so the mapper is written once.
5. **Versioned mapping.** Each imported trace records the source, the API version and the mapper version, so a later mapper never silently changes old evidence.

### 4.2 Profiles: naming the steps

Imported observation ids change on every run, but checks need stable names. A **profile** per connection maps observation names to step aliases and lists the checks:

```yaml
connection: support-agent-prod          # a Langfuse project
steps:
  "order-lookup tool": lookup           # observation name -> step alias used in checks
  "refund calculator": calc
  "reply writer": writer
checks:
  - id: OUT-REFUND
    scope: outcome
    step: writer
    expression: approx(number_in(writer.output), truth.order_total(lookup.order_id))
truth: { provider: http, url: https://internal.example/granite-truth }   # optional, section 4.5
```

The check language is unchanged (the same safe expression evaluator, ADR-004). Observations without an alias are kept in the trace but get no checks.

### 4.3 Inferring who read what

Attribution needs data-flow edges. Three sources, used in this order, each recorded on the edge:

| Tier | How | Confidence |
|---|---|---|
| Declared | The application adds `granite.reads=["lookup.items"]` to an observation's metadata (one line with either SDK) | Full |
| Value match | A later step's input contains a value (a number, or a string of at least 12 characters) that appears in an earlier step's output | Medium; an edge weight below 1 lowers the score of hypotheses that rely on it |
| Order | Otherwise, each step is taken to read its predecessor | Low; ranks by position only, as attribution already does when no step has direct evidence |

How accurate value matching is, is an open research question worth a section of the FYP-2 evaluation: measure inferred edges against the declared edges of Granite's own workflows and against the tau-bench Retail Agent.

### 4.4 Ingestion, reliability and scale

- **Pull jobs per connection.** Poll every N minutes (default 5) for traces in `[cursor, now − lag)`, with `lag` defaulting to 15 minutes to respect Langfuse's v2 data delay. Store the cursor after each page.
- **Idempotent.** A run is keyed by (connection, external trace id); re-reading a trace updates nothing that is already analysed.
- **Bounded.** A page limit, a per-sync trace cap, exponential backoff on HTTP 429 and 5xx, and a circuit breaker that pauses a connection after repeated failures and says so in the interface.
- **Filtered at the source.** Only traces matching the profile (trace name, tags, or a sampling rate) are imported, so cost tracks the traces a team cares about, not its total volume.
- **Jobs.** The current thread pool is enough for a demo. A shared deployment needs a durable queue; a Postgres-backed queue keeps the stack to one database (FYP-2).

### 4.5 Sources of truth for production checks

Checks that call `truth.*` need the team's own data. Two providers: **static** (a JSON or CSV reference file uploaded with the profile) and **HTTP** (Granite calls an endpoint the team runs, with the function name and arguments; https only, no redirects, a timeout, a response size cap, and every call stored as evidence). Without a provider, checks are limited to a step's own contract (for example "the reply states the amount the calculator produced"), which still catches many silent failures.

### 4.6 Replay on imported traces (opt-in)

Three routes to V2 for teams that want it, from simplest to most general:

1. **Granite's own runner**, when the imported trace comes from a workflow Granite can execute (the FYP-1 demo case below).
2. **A replay hook**: the team exposes one HTTP endpoint (or decorates a Python function with a Granite SDK helper) that re-runs its agent from a named step with a patched value and a seed, and returns the new output. Granite then applies rule VR-1 unchanged.
3. **LangGraph checkpoint fork**: LangGraph can fork a run from a past checkpoint with changed state, which is exactly the operation VR-1 needs.

### 4.7 Security and privacy

- **Credentials** are stored encrypted (Fernet, key from an environment variable), never logged, never returned by the API after creation; the interface shows only the last four characters. Langfuse keys are project-scoped; recommend a dedicated project key for Granite.
- **Personal data:** production traces carry customer data. **Redaction before storage (FR-SEC-01, not met today) becomes a hard prerequisite** before any real production connection is offered. Granite should also support "analyse without storing payloads", keeping only check results, hashes and the evidence a finding needs.
- **Least writing:** write-back is off until enabled per connection, and only writes scores or annotations named `granite.*`.
- **Self-hosting first:** a team can run Granite next to its self-hosted Langfuse or Phoenix so traces never leave its network.

## 5. Capabilities, phases and priorities

Effort is in developer-days from the current code. Value: what a user gains. Priority: P0 (do first in its phase) to P3.

### 5.1 FYP-1 Final: one real round trip (optional, needs C-07)

| # | Capability | Approach | Depends on | Effort | Value | Priority |
|---|---|---|---|---|---|---|
| 1 | Refund Desk sends its own runs to a real Langfuse Cloud project | The Langfuse Python SDK (or OTLP) behind a setting; off by default | A free Langfuse Cloud Hobby account and project keys created by a team member, kept in `.env` | 0.5 | Real data in a real platform, not a mock | P1 |
| 2 | Langfuse source connector | `httpx` client, Basic auth, v2 observations with cursor and time window; v1 fallback for self-hosted | 1 | 2 | Reads production-format traces | P1 |
| 3 | Mapper and the Refund Desk profile | `SpanRecord` → Trace v1; declared reads via observation metadata (Granite writes them, so lineage is exact here) | 2 | 1.5 | Checks, attribution and verification run unchanged | P1 |
| 4 | Write-back to Langfuse | `POST /api/public/scores`: BOOLEAN `granite.silent_failure` on the trace, CATEGORICAL `granite.origin` (confirmed, refuted, suspect) on the origin observation, with a link to the finding | 3 | 0.5 | The verdict appears inside Langfuse, where the team already works | P1 |
| 5 | Import screen: connect, sync now, imported runs | One form (host, keys, project), a sync button, the existing run and finding pages | 2 to 4 | 1 | Demonstrable | P2 |

About 5.5 days. Because the imported traces come from Refund Desk, Granite can also replay them (route 1 in 4.6), so the demo shows the full chain: **a run captured by Langfuse, read by Granite, traced back, replay-verified, and the verdict visible back in Langfuse**. Say plainly that the data is Granite's own workflow sent through a real platform, and that replay on other teams' traces needs a hook (section 4.6).

**Recommendation:** do this only after the five committed items are merged, the code walkthrough has happened and report v2.0 is drafted. If the date is tight, it becomes the first FYP-2 milestone; nothing in the committed plan depends on it. A recorded copy of the API responses (like the model cassette) keeps the demo working without network.

### 5.2 FYP-2: integrations a team could adopt

| # | Capability | Approach | Depends on | Effort | Value | Priority |
|---|---|---|---|---|---|---|
| 6 | Redaction before storage (FR-SEC-01) | The token vault designed in defect D-07; "analyse without storing payloads" mode | none | 3 | Required before any real customer data | **P0** |
| 7 | Connections and profiles in the product | Encrypted credentials, profile editor with a dry run on the last 20 traces, sync status and errors | FYP-1 items 2 to 5 | 4 | Self-service setup | P0 |
| 8 | Scheduled sync with backoff, caps and a durable job queue | Postgres-backed queue; per-connection cursor; circuit breaker | 7 | 4 | Runs unattended | P0 |
| 9 | Phoenix source and annotation sink | Spans API with cursor; OpenInference attribute mapping; `POST /v1/span_annotations` with identifier `granite` | Mapper | 3 | Second platform: proves Granite is platform-neutral | P1 |
| 10 | Inferred lineage (value match) and its evaluation | Section 4.3; measured against declared edges | Mapper; Retail Agent | 3 + research | Attribution on traces with no declared reads | P1 |
| 11 | Static and HTTP truth providers | Section 4.5 | 7 | 3 | Source-of-truth checks on production data | P1 |
| 12 | Replay hook protocol and a Python SDK helper | Section 4.6, route 2 | 6 | 5 | V2 verification on a team's own agent | P2 |
| 13 | LangGraph checkpoint-fork replayer | Section 4.6, route 3 | 12 | 4 | V2 for LangGraph users without writing a hook | P2 |
| 14 | `granite-verify` GitHub Action | Runs exported regression cases in CI | Regression export (built) | 2 | Granite in the team's daily workflow | P2 |
| 15 | OTLP receiver | Accept OpenTelemetry traces directly (dual export from the app) | Mapper | 4 | Any OTel-instrumented app, no platform needed | P3 |

### 5.3 After the FYP: product and business

| # | Capability | Value | Priority |
|---|---|---|---|
| 16 | Organisations, projects, roles, SSO; reviewer identity on every decision | Teams and audits | P0 |
| 17 | Hosted Granite Cloud with usage metering | Revenue | P0 |
| 18 | Alerts (Slack, e-mail, webhook) on new confirmed findings | Daily habit | P1 |
| 19 | Check packs for common failure classes (price, policy, hand-off, retrieval) shared across teams | Faster setup; a library others add to | P1 |
| 20 | More sources through OTLP and dedicated connectors (LangSmith export, Datadog LLM Observability) as demand shows | Reach | P2 |
| 21 | Signed evidence bundles for auditors | Regulated customers | P2 |

## 6. Why a team would use it, and keep using it

| Competitor or tool | What it already does | What Granite adds on top |
|---|---|---|
| Langfuse, Phoenix (partners) | Capture, view, evaluate traces; human annotation; LLM-as-judge; Phoenix's PXI investigates in beta | A verdict on where a wrong answer began, from executable checks and (with a replay route) controlled replay; written back into their interface |
| LangSmith Engine | Diagnoses failures and opens fix pull requests, inside LangSmith only | Works on Langfuse and Phoenix data; verdicts with controls and an interval; self-hosted; open |
| Arize AX Signal | Ranked recurring failures with likely causes, Enterprise tier | Free and self-hosted; evidence a reviewer can re-check |
| Raindrop | Model-judged failure detection, simulations on production traffic | Detection by executable checks against the team's own truth; step-level origin |

Retention comes from value that accumulates, not lock-in: **every confirmed finding leaves a regression test in the team's CI and a check in its profile.** After a few months the team's definition of "correct" lives in Granite. Data stays exportable (Trace v1 JSON, evidence bundles), which is itself a reason to trust it.

Risk to name: Langfuse or Phoenix could build this themselves (Phoenix's PXI points that way). The defence is to be the neutral, open, measured option that works across both, and to publish the evaluation.

## 7. Business model (hypotheses to test, not plans to bill)

**Who pays.** (1) Small AI teams and software houses already on Langfuse or Phoenix who lose hours to wrong-but-silent runs; (2) teams in regulated work (finance, health, public sector) who need an auditable record of what failed and who decided; (3) later, platform teams running many agents.

**Open core.** The core engine, connectors and self-hosted app stay open source. Paid offers sit where cost or responsibility is ours:

| Offer | Price idea (to test) | Includes |
|---|---|---|
| Self-hosted | Free | Everything for one team, community support |
| Cloud Free | Free | 1 project, 1 connection, a monthly cap on investigations (for example 50) |
| Cloud Team | Per project per month, low tens of dollars (Langfuse Core at $29 is the reference point users know) | More investigations, alerts, CI action, 90-day retention |
| Business | Higher, per organisation | SSO, roles, audit exports, longer retention, support |
| Enterprise | Contract | Self-hosted support, security review, custom connectors |

**Meter investigations, not traces.** Observability tools charge per trace or unit; Granite's value is per wrong run explained. Replays call the customer's own model keys (bring your own key), so Granite's running cost is mostly ingestion, storage and check evaluation, which keeps margins workable even at low prices.

**Costs.** Development and the first users run on free tiers (Render, Neon, Langfuse Hobby, local Ollama). A paid hosted offer would start with a small always-on instance (Render's paid starter instance removes the free tier's sleep) and a paid Postgres plan; size it when the first paying team exists, not before.

**Getting users.** Open-source repository with the benchmark published; listing in Langfuse's and Phoenix's integration directories; the GitHub Action in the marketplace; posts showing a real silent failure found and proven; pilots with local software houses that ship agents to foreign clients.

**Validate before building billing.** Interview 5 to 8 people who use Langfuse or Phoenix (the stakeholder interviews the handbook already asks for), recruit 3 design partners, and track one number: confirmed findings per active team per week. No payment system until a team asks to pay.

## 8. Proposed requirements (for C-07)

| ID | Requirement | Phase |
|---|---|---|
| FR-INT-01 | Import traces from a Langfuse project by API, incrementally, without duplicates | FYP-1 (optional) / FYP-2 |
| FR-INT-02 | Map imported observations to Granite Trace v1 through a profile; record source, API and mapper versions | FYP-1 (optional) / FYP-2 |
| FR-INT-03 | Write a finding's verdict back to the source platform as a score or annotation, only when enabled | FYP-1 (optional) / FYP-2 |
| FR-INT-04 | Import from Arize Phoenix and write span annotations | FYP-2 |
| FR-INT-05 | Store third-party credentials encrypted; never return or log them | FYP-2 |
| FR-INT-06 | Mark imported runs that cannot be replayed and refuse replay with a reason (extends FR-IMP-02 and FR-VER-04) | FYP-2 |
| NFR-INT-01 | A sync tolerates rate limits and outages without losing its position or importing a trace twice | FYP-2 |

## Sources

Checked on 15 November 2026.

- Langfuse: [public API and authentication](https://langfuse.com/docs/api-and-data-platform/features/public-api), [observations API v2](https://langfuse.com/docs/api-and-data-platform/features/observations-api.md), [deprecated API migration](https://langfuse.com/docs/deprecated-api-migration), [observations query continuation, 3 November 2026](https://langfuse.com/changelog/2026-11-03-observations-api-continuation), [scores API](https://langfuse.com/docs/api-and-data-platform/features/scores-api), [non-numeric scores](https://langfuse.com/changelog/2024-07-11-non-numeric-scores-api), [pricing](https://langfuse.com/pricing) and a third-party summary of it ([usagepricing.com](https://usagepricing.com/blueprint/langfuse))
- Langfuse push events: only third-party polling triggers found ([Pipedream](https://pipedream.com/apps/langfuse/triggers/new-score-received), [n8n community](https://community.n8n.io/t/free-langfuse-slack-alerting-connector-for-llmops-workflows/287334?tl=en))
- Phoenix: [create span annotations](https://www.arize.com/docs/phoenix/sdk-api-reference/rest-api/api-reference/spans/create-span-annotations.md), [list spans](https://phoenix.arize.com/docs/api-reference/spans/list-spans.md), [REST API improvements, March 2026](https://arize.com/docs/phoenix/release-notes/03-2026/03-13-2026-rest-api-improvements.md), [capture feedback](https://www.arize.com/docs/phoenix/tracing/how-to-tracing/feedback-and-annotations/capture-feedback)
- OpenInference: [span kinds](https://www.arize.com/docs/phoenix/tracing/concepts-tracing/otel-openinference/span-kinds), [semantic conventions mirror](https://www.mintlify.com/Arize-ai/openinference/spec/semantic-conventions)
- Competitors and LangGraph replay: see the sources of [`product-strategy.md`](product-strategy.md)
