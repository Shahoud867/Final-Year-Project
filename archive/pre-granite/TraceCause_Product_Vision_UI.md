# Granite — Full Product Vision ("Mission Control Center" UI)

> **Status: aspirational reference only — NOT part of the FYP scope, NOT an approved extension.** This is a maximalist product-design vision (from a GPT session), preserved here for later reference (post-graduation, if the startup track is pursued). It is explicitly **not** compatible with the committed core in [FYP_Scope_CCP_and_Implementation_Plan.md](../../deliverables/stage-0-proposal/proposal-documents/FYP_Scope_CCP_and_Implementation_Plan.md) §7 or the "minimal dashboard" scoping already decided there. See the brutally honest rating at the bottom before treating any of this as a to-do list.

---

## Core design philosophy proposed

> Every major backend capability must have a visible, interactive product experience.

| Backend capability | Proposed user-facing experience |
|---|---|
| Execution graph | Interactive workflow map |
| Root-cause algorithm | "Why did this fail?" panel |
| Propagation analysis | Blast-radius visualization |
| Confidence model | Evidence and confidence panel |
| Counterfactual replay | Replay Lab |
| Regression evaluation | Regression Center |
| Fault taxonomy | Failure analytics |
| Benchmark | Public leaderboard |
| Clarification classifier | Prevention warnings |

## Proposed information architecture

```
TRACECAUSE
├── Overview — system health, recent activity, active incidents, reliability trends
├── Workflows — workflow graph, agents, versions, test suites
├── Live Runs — real-time execution view, timeline, live anomaly detection
├── Incidents — root cause, propagation, evidence, blast radius
├── Trace Lab — trace explorer, step inspector, dependency graph (IDE/debugger-style)
├── Replay Lab — counterfactual experiments, fix comparison, recovery results
├── Compare — TraceDiff, version comparison, regression analysis
├── Analytics — failure patterns, failure clusters, agent health, trends
├── Benchmark — dataset, baselines, leaderboard
├── Integrations — SDK, frameworks, webhooks, GitHub Actions
└── Settings
```

## The 17 proposed screens/features

1. **Mission-control home nav** — persistent sidebar, always-visible health/incidents/recovery stat cards
2. **Overview dashboard, three onboarding modes** — Demo Mode (pre-loaded sample incident), Connect Existing Workflow (SDK/CrewAI/LangGraph/custom), Build a Test Workflow (visual workflow builder)
3. **Home dashboard, four live sections** — System Health (score + breakdown), Live Activity Feed (timestamped event stream), Active Incidents panel
4. **Workflows page** — card-based workflow list, each opens to a graph view with hoverable per-agent stats
5. **Live Runs** — real-time, animated per-agent progress bars during execution, "Investigate Now" trigger on anomaly, live diagnosis-in-progress messages
6. **Incident page** — root cause, confidence, failure type, blast radius, propagation chain with clickable nodes and a per-step side panel
7. **"Why do you think this?" evidence panel** — checklist-style evidence list backing the confidence score
8. **Trace Explorer** — three-pane IDE/debugger-style view (timeline, step details, dependencies), explicitly compared to "GitHub + Chrome DevTools + Datadog trace explorer, but for AI agents"
9. **Replay Lab** — create multiple named "experiments" (replace a step's output, re-run with a different prompt version, etc.), see them side-by-side with a recovery score and a "best fix" badge
10. **TraceDiff** — baseline vs. comparison run, structured diff of prompt/model/tool-response/context-size/output, with a "likely divergence begins here" marker on the graph
11. **Analytics page** — organized as answered questions ("what fails most," "where do failures start," "are things improving," "what changed") with bar/line charts
12. **Failure Clusters page** — recurring-pattern cards (occurrence count, root agent, trend direction), each opens to its member incidents and common pattern
13. **Agent Health Profiles** — per-agent score breakdown, weekly trend chart, "what caused this decline" drill-through to related incidents
14. **Regression Center** — version-over-version reliability comparison, likely-cause ranking, per-agent before/after pass/fail grid
15. **Alert Center** — rule builder ("IF confidence > 85% AND blast radius > 3 THEN webhook + incident")
16. **Interactive onboarding** — guided 4-step "diagnose your first sample failure" flow ending in a completion badge
17. **Micro-activity everywhere** — animated graph edges during live runs, progress bars during diagnosis ("Scanning execution graph... ████░░"), hover-reveal propagation probabilities

---

## Brutally honest rating

**Overall: 3/10 as something to actually build this year. 8/10 as a product-design portfolio piece.** Those are both true at once, and the gap between them is the whole problem.

**What's genuinely good about it:** the underlying principle — don't let a real algorithm's output rot as raw JSON, give it *some* visible form — is correct and worth keeping. The information architecture is well-organized, and several individual concepts (Replay Lab, the confidence-evidence panel, Failure Clusters, Blast Radius) map to ideas already independently rated 8-9/10 as genuine market gaps in [GPT-Feature-Response.md](GPT-Feature-Response.md). The instinct isn't wrong. The *scale* is.

**Why this can't be this year's plan:**

1. **It's a full SaaS product built by one committed-core role.** Student 3 already owns the counterfactual engine, the backend API, containerized deployment, *and* 6 of the 13 already-planned extensions (webhook, incident report, trend view, project namespacing, human-gated approval, CI check). This document proposes roughly 10x that scope in UI work alone — real-time animated execution views, a three-pane IDE-style trace debugger, a rule-builder alert engine, multi-mode onboarding, a visual workflow builder — each one individually a multi-week project for a dedicated frontend engineer, not a side task.
2. **Item 8 (Trace Explorer) is the single worst idea in the document, rated honestly.** Building "GitHub + Chrome DevTools + Datadog, but for AI agents" means competing directly with LangSmith, Langfuse, Braintrust, Arize, and Maxim on the *one thing they already do best* — confirmed in [Commercial_Product_Comparison.md](../../research/market/commercial-product-comparison.md) as their core, most mature competency. A 3-person team cannot out-build five funded companies at their own specialty, and trying to is pure sunk time with negative differentiation.
3. **Most of it has zero CCP value and the guide names this exact failure mode.** Animated activity feeds, progress-bar micro-interactions, a badge-and-completion onboarding flow, a card-based workflow gallery — none of this touches the complex computing problem. It's precisely what §15 of the FAST guide calls "routine portal... feature-rich application — size and screen count do not establish a CCP or contribution." A panel would ask "where's the hard problem in this screen?" for at least 12 of these 17 items and there's no good answer.
4. **It's the "maximal dashboard" question from a few turns ago, at 10x the scale, dressed as a design vision.** The earlier answer still stands: build the Tier 1 items that flow free from the diagnosis engine's own output, treat everything else as post-graduation. This document is almost entirely Tier 2 and Tier 3 — the exact territory already flagged as "don't touch until after Final-2."

**What I'd actually salvage, if anything:** the Incident page (item 6) plus the "why this root cause" evidence panel (item 7) — because that's not new work, it's just a reasonable display of what core items #1-#4 already have to output for the evaluation anyway. Everything else in this document — all three onboarding modes, Live Runs animation, Trace Explorer, Replay Lab's full experiment-comparison UI, TraceDiff, the Analytics page, Failure Clusters, Agent Health Profiles, Regression Center, Alert Center, guided onboarding — belongs in a "if this becomes a real company" folder, not FYP-2's task list.

**The honest bottom line:** this is what Granite could look like with a Series A and a product team. It is not what three students building a research-grounded diagnosis engine should be spending their limited months on. Keep the file for later. Don't let it anywhere near this year's plan.
