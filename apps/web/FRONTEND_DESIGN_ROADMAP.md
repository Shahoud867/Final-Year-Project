# Granite frontend design roadmap

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-11-15 |
| Status | P0 and P1 implemented on branch `feat/fyp1-final-scope` on 2026-11-15 (section 10.1), by the AI assistant (see the [AI usage log](../../docs/registers/ai-usage-log.md)); uncommitted and not yet reviewed by the team. P2 is open |
| Scope | `apps/web` only. Product scope and dates stay in [`fyp1-completion-plan.md`](../../docs/plan/fyp1-completion-plan.md); this document says how each screen should look and behave, and in what order to build it |
| Name | The file name is the one requested. It is allowed here because code folders are checked only for spaces and parentheses ([workspace guide](../../docs/workspace-guide.md), section 4.4) |

## 0. Read this first

**What this document is based on.**

- The existing frontend: all 4,331 lines of source, the design tokens and the October screenshots in `evidence/demos/`.
- Competitors' public documentation, changelogs and release notes, read on 14 and 15 November 2026.

**What it is not based on.**

- I could not log in to any competitor's dashboard, and I could not view their screenshots. Every competitor statement below comes from text: documentation, changelogs, release notes, or press. Where a layout claim cannot be confirmed from text, it says so. Open each product's public demo or free tier yourself before copying any pattern.
- No user has tested the current interface. The usability check for panel action A1 ([protocol](../../docs/manuals/usability-check-protocol.md)) has not been run. Every "problem" below is a design judgement. Test it with three people before spending days on it.

**A tension with an earlier recommendation.** The [product strategy](../../docs/plan/product-strategy.md) says more interface redesign earns nothing before the Final. That still holds for polish for its own sake. This roadmap therefore puts the screens that new features need first (section 10, P0), then a small set of changes to the existing screens (P1), and leaves the rest for FYP-2. Do not start P1 before the five committed backend items are merged.

## 1. What exists today

Hash-routed React 19 and TypeScript with Vite; no router, no component library, no data library. Lucide icons and two self-hosted fonts. 32 web tests including automated accessibility checks (axe).

| Screen | Route | Source | What it does well | Problem |
|---|---|---|---|---|
| Investigations | `#/` | `pages/Home.tsx` | Telemetry, filters, a trace-inspector drawer | One screen holds findings, runs and telemetry; a reviewer's first question, "what needs me?", has no direct answer |
| Task Studio | `#/new` | `pages/NewRun.tsx` | Three scenarios; validation in the server's own words | Name says nothing; it is a form for starting a run |
| Pipeline trace | `#/runs/{id}` | `pages/RunDetail.tsx` | The silent-failure contrast; a clear graph; a step inspector | About 2,400 px of six stacked cards. The same check results appear three times: pipeline table, "Observed vs source of truth", "Checks" |
| Verification lab | `#/findings/{id}` | `pages/FindingDetail.tsx` | The lifecycle stepper; ranked suspects; replay marks; evidence | The case is told top to bottom, but nothing stays on screen: the verdict and the next action scroll away |
| How it works | `#/guide` | `pages/Guide.tsx` | Features, levels, a VR-1 explorer | An explainer, not part of the working loop |
| Evidence | `#/evidence` | `pages/Evidence.tsx` | Contrast, comparison, live CI status | Mostly a panel-facing page; sits at the same level as the working screens |

Inconsistencies found in the code and docs:

- `apps/web/README.md` says dark is the default theme; `tokens.css` and the October change log say light is the default. The README is stale.
- Every card, the sidebar and the top bar use a blurred translucent "glass" fill over a fixed coloured "aurora" background (`base.css`, `components.css`). It serves no information, costs rendering time, and is the single most template-like part of the interface.
- Three type sizes only (13, 15 and 22 px), chosen for contrast checks. Hierarchy is flat: a page title and a card title are the same size.
- Spacing tokens are 4, 8, 14, 18, 22, 26 and 34 px: not a consistent scale.
- The brand mark is a stock mountain icon. A drafted mark exists in `docs/brand/` and is not adopted; the poster uses it.
- The interface has no toast or notification component, no keyboard shortcuts and no way to compare two runs.

## 2. Competitor research

Facts below are from the sources listed at the end. "Beta" and "GA" are the vendor's own words.

### 2.1 Patterns worth taking

| Source | Pattern | Evidence | Granite equivalent |
|---|---|---|---|
| Langfuse | Trace detail has **Tree, Timeline and Graph** tabs, plus a Log view that concatenates everything. In July 2026 the graph gained **Aggregated and Expanded** modes (beta) because loops made it unreadable | Agent Graphs docs; July 2026 changelog | Tabs on the run page: Trace, Timeline, Data. Keep the graph linear and expanded. Aggregated is for FYP-2 when a workflow loops |
| Arize Phoenix | **Evaluation badges under each span row** in the trace tree, so a failed check is visible while scanning; trace-level and span-level annotations side by side (release notes of 30 September 2026) | Release notes | Under each step row, show its checks as small pass and fail marks. This replaces the duplicated tables |
| LangSmith | A run tree with inputs and outputs per node; a chronological **Trajectory** view; Engine groups failures into **issues**, each with a diagnosis, supporting traces and a proposed fix | Docs; Engine announcement | The Inbox is a list of findings, each showing cause and evidence at a glance |
| Braintrust | **Diff mode** against a baseline: rows aligned by input, **score deltas** coloured green for gains and red for regressions; a grid layout; diff works only in the trace view | Compare-experiments docs | Compare two runs of the same task (clean against faulty, before and after a fix) with changed steps and values highlighted. P2 |
| Sentry | Issue details restructured around **information hierarchy and progressive disclosure**; breadcrumbs as a timeline where each type has its own icon and colour | Issue Details docs; changelog | The case file: the verdict first, evidence below, raw data one click away; the evidence ladder V0 to V3 as a timeline |
| Raindrop | A "Sentry for agents" framing; signals that are positive, negative or neutral; a triage agent. The docs name a signals dashboard; I could not read its layout | Docs; press | Frame the Inbox the same way: an issue list, not a data table. No layout is copied |
| Linear | Principle quoted in its own refresh post: "Don't compete for attention you haven't earned"; fewer borders, less visual noise; theme generation used for the main themes | Linear's blog (secondary summaries disagree on details) | Flat surfaces, one border colour, colour used only for meaning |

### 2.2 Problems in competitors that Granite can avoid

These are limits of the documented behaviour, not complaints from users. None is a claim about quality.

1. **Diagnosis presented as a conclusion.** Engine and Signal show a cause and a fix. The documentation reviewed does not show how confident the product is or what was tried. Granite's screen can show the replays, the control group and the interval next to the verdict.
2. **Many views of the same trace.** Langfuse now has Tree, Timeline, Graph and Log. Four views is a lot for someone who has never opened one. Granite should open on one view that answers "where did it go wrong" and offer the others behind tabs.
3. **Evaluation results scattered.** Braintrust's diff is available only in one row mode, and Timeline and Thread are disabled while it is on. Granite should keep every view available in a comparison.
4. **Product-first, not finding-first.** Observability tools open on traces or projects. Granite's unit is a finding with a state, so its home should be a work queue.

### 2.3 What Granite already does that none of these documented

- It shows what ordinary monitoring sees beside what the checks see on the same run (the "Outcome" card).
- It shows the lifecycle as a rule the server enforces, with allowed next actions.
- It shows a hash for every piece of evidence and re-checks it on display.

Keep these. They are the identity, not decoration.

## 3. Design philosophy

**A case file, not a dashboard.** A finding is a case: a symptom, a suspect, a test, a verdict and a decision. The interface should read like opening a case. Everything on the case page answers one of five questions in order: what went wrong, where did it start, how do we know, what was decided, what is the proof.

Principles, each tied to a decision below:

1. **The next action is always visible.** A sticky summary on the case page and on the run page.
2. **One fact, one place.** A check result appears once and is linked from elsewhere.
3. **Colour means state only.** Red failure, amber suspect, green passed, blue verification. Every state has an icon and a word as well. This matches the poster, so the two read as one product.
4. **Show the evidence before the conclusion's confidence.** A verdict is shown with its replays and interval next to it, never alone.
5. **Say what is not available.** Imported traces cannot be replayed; the button explains why instead of disappearing.
6. **Flat, quiet surfaces.** Remove the glass and aurora. Information earns emphasis.

**Identity.** Two things make Granite recognisable without decoration:

- **The fault line.** The mark is a block split by a stepped offset; use that stepped line as the one graphic motif, drawing the origin-to-symptom path in the graph and the replay path in the case file.
- **The evidence ladder.** V0 to V3 as a four-step bar that fills as a finding progresses. It appears on every finding row, the case header and the report.

## 4. Navigation and page structure

Operational pages first, explanation last. Names say what the page is.

| Order | Nav item | Route | Page | Phase |
|---|---|---|---|---|
| 1 | Inbox | `#/` | Findings needing action, then recent runs | P0 (restructure) |
| 2 | Runs | `#/runs` and `#/runs/{id}` | All runs; one run's trace | exists; P1 |
| 3 | Fault Lab | `#/lab` | Choose faults and tasks, generate a batch, watch progress | P0 |
| 4 | Evaluation | `#/evaluation` | Measured results against baselines | P0 |
| 5 | Import | `#/import` | Upload a trace, see the validation report | P2 (stretch for the Final) |
| | *Help group* | | | |
| 6 | How it works | `#/guide` | Unchanged | exists |
| 7 | Why Granite | `#/evidence` | The current Evidence page, renamed | exists |

The finding route `#/findings/{id}` is the case file and is reached from the Inbox, never from the sidebar. "New run" stays a primary button in the top bar and opens the existing Task Studio form, renamed "New run".

The sidebar footer keeps the server status, model mode and build stamp.

## 5. Page specifications

Wireframes use text boxes; widths are for 1280 px and up.

### 5.1 Inbox (`#/`)

Purpose: tell a reviewer what needs them.

```
┌ Inbox ───────────────────────────────────────────── [New run] ┐
│ Needs you (3)   Verifying (1)   Decided (12)   All            │  tabs by lifecycle group
├───────────────────────────────────────────────────────────────┤
│ ● Stated refund ≠ catalogue total      Order Lookup  V2 ▮▮▮▯  │  one finding per row
│   run #W1023987 · high · confirmed 5/5 vs 0/2 · 2 min ago     │
│ ● ...                                                         │
├ Recent runs ──────────────────────────────────────────────────┤
│ compact table: task, status, faults, findings, time           │
└───────────────────────────────────────────────────────────────┘
```

- Tabs map lifecycle states: Needs you = confirmed or evidence-supported and not yet reviewed; Verifying = open, hypothesised, verifying; Decided = accepted, rejected, resolved, won't fix.
- Each row: title, suspected step, evidence ladder, verdict in words, severity, age. The whole row opens the case file.
- The telemetry tiles from the current Home collapse to one line of totals above the tabs.
- Empty: "No findings yet. Run a task with a fault." with the New run button.
- Keep the filters component; keep the drawer as a quick look (`Home.tsx` already has it).

### 5.2 Case file (`#/findings/{id}`): the centrepiece

Layout: header, then a main column and a sticky right rail (320 px; it moves below the header on screens under 1100 px).

```
Header:  title · state pill · evidence ladder V0▮ V1▮ V2▮ V3▯ · severity · hash
Main:    1 Symptom   2 Origin   3 Verification   4 Decision   5 Evidence      section links, sticky
         each section a heading + one idea
Rail:    Verdict "Order Lookup · confirmed", 5/5 with fix, 0/2 without, 57–100%
         Next action: the one allowed button (Review, Mark resolved, ...)
         Export report · Export regression test        P0 for the second
         Hash of the finding, copy button
```

- **Symptom.** Observed and expected side by side, the check expression in a collapsed block, and one sentence: "The run completed with no error." This is today's card, unchanged.
- **Origin.** The graph with the recorded data-flow path, above a ranked list of suspects (existing). Each suspect row: rank, step, reason in words, score bar, and its verdict once tested. Add the **Investigate** control here: one button that verifies suspects in order and shows each attempt as a row being filled (item 12 of the plan). Keep the per-suspect Verify button as secondary.
- **Verification.** One result per experiment: the five fix replays and two controls as marks (existing `Replay.tsx`), the VR-1 axis with the interval (reuse `Vr1Explorer.tsx`), and the verdict. Show the replay plan as a row of step chips (existing).
- **Decision.** The reviewer's note field and the allowed actions (existing, from `lib/lifecycle.ts`). History below it.
- **Evidence.** The ledger with hashes (existing).
- States: loading skeleton in the shape of the sections; a finding not found shows the existing error box; an experiment in progress shows the progress count and keeps the rest of the page usable.
- Not available: on an imported trace the Verify and Investigate controls are disabled and the rail says "Replay needs a workflow Granite can run".

### 5.3 Run page (`#/runs/{id}`)

Purpose: show the trace and what the checks found, without repeating it.

- **Summary strip** (replaces the Outcome card header): task, status, mode, fault badge, duration, and the finding link if one exists.
- **Two-up contrast** (existing): "What output monitoring sees" and "What Granite's checks see", with the Investigate or Open finding button.
- **Tabs:** `Trace` (default), `Timeline`, `Checks`, `Data`.
  - *Trace*: the graph on top, the step table below. Each step row shows its checks as small pass and fail marks under the name (the Phoenix pattern), and the step inspector opens in the existing drawer. The "Observed vs source of truth" content moves into the inspector, shown only for the selected step.
  - *Timeline*: horizontal bars by step duration. P2; build only if timings are meaningful in live mode.
  - *Checks*: the existing table, grouped by scope, collapsed by default to failures first.
  - *Data*: the raw trace JSON (existing `JsonView`).
- This removes two of the three repeats and about 40% of the scroll height; measure it, do not assume it.

### 5.4 New run (`#/new`)

Keep. Rename to "New run". Change only: scenario cards stay; the three numbered cards become one two-column form with the pipeline preview on the right so it stays visible while the form scrolls.

### 5.5 Fault Lab (`#/lab`), new

```
Fault types:  ☑ stale price  ☑ handoff drift  ☑ dropped field   (each with one-line effect and a mini diagram)
Tasks:        ◉ all 12 recorded   ○ choose…          Clean controls: 20%      Mode: recorded | live
Plan:         "3 faults × 12 tasks + 7 clean = 43 runs, about 6 min in recorded mode"        [Generate]
Progress:     43 bar, per-run dots (done, failed, running), cancel
Result:       table: fault, runs, detected, findings opened → open in Inbox
```

- The plan sentence is computed, so the user knows the cost before pressing Generate.
- Progress uses the existing `Progress` component and a polling hook like the experiment page.
- Errors: a run that fails is marked and the batch continues; the summary says how many failed.
- Ground truth for each run stays hidden from the analysis and is revealed only in the result table, matching the current "Reveal injected fault" behaviour.

### 5.6 Evaluation (`#/evaluation`), new

Purpose: show whether Granite works in general, honestly.

- **Headline row:** four numbers with intervals: detection, false alarms, top-1 attribution, verified top-1.
- **Comparison table:** rows are methods (earliest failing check, last agent, LLM judge, Granite ranking, Granite with verification); columns are check coverage 100%, 60%, 30%. Each cell: percentage and interval. Cells where Granite ties or loses are not hidden or recoloured to look good.
- **Coverage chart:** one line per method across coverage, drawn as plain SVG with interval bars (no chart library; the VR-1 explorer already draws SVG).
- **Nondeterminism panel:** false confirmations, single replay against VR-1.
- **Provenance strip:** the pre-registration file name and hash, run date, commit, model, number of tasks. If the numbers come from fewer than 30 tasks, a visible note says "early result, not a benchmark".
- Data comes from the harness's results JSON served by the API; the page shows nothing that is not in that file.

### 5.7 Import (`#/import`), P2

Drop zone for a Granite Trace v1 file; a validation report listing each problem with its path in the file; a preview of the steps; a button to create the run. Invalid files show errors, never a partial import.

### 5.8 Help pages

`How it works` and `Why Granite`: keep content; move to a Help group; apply the new tokens only. No structural change.

## 6. Design system

Build on the existing tokens and components in `styles/tokens.css` and `components/ui.tsx`. Change values; keep names so no rule has to move.

### 6.1 Colour

Meaning is fixed and matches the poster.

| Role | Light | Dark | Use |
|---|---|---|---|
| Page | `#F7F6F3` | `#0A1220` | background |
| Surface | `#FFFFFF` | `#111E38` | cards, tables |
| Line | `#E2DFD8` | `#22314F` | the one border colour |
| Text, secondary, tertiary | `#1C1A17`, `#403C36`, `#5A564E` | `#F4F7FB`, `#B9C6DC`, `#9AA8BF` | |
| OK | `#0F7032` | `#35D07F` | passed, confirmed, done |
| Bad | `#B3251A` | `#FF5A4E` | failed check, symptom |
| Warn | `#8A5200` | `#FFB020` | suspect, awaiting review |
| Replay | `#0A52AD` | `#7CC0FF` | verification, links |
| Primary action | `#0071E3` | `#0062CC` | one per screen |

- Every status shows an icon and a word as well as colour.
- Dark values match the poster. The poster measured them at 5.6:1 to 16:1 against its card colour; re-measure on the interface's surfaces with a contrast checker before shipping, because the surfaces differ.
- Remove the aurora variables and the glass variables. Keep `--shadow-2` for drawers and menus only.
- Decision for the team: light as default (projectors) or dark. The code says light; fix the README.

### 6.2 Type

Inter for text, JetBrains Mono for IDs, hashes, values and check names. Add two sizes so hierarchy exists. Larger sizes keep the 3:1 rule for large text; body stays at or above 4.5:1.

| Token | Size / line | Weight | Use |
|---|---|---|---|
| `--fs-sm` | 13 / 18 | 500 | labels, metadata |
| `--fs-base` | 15 / 22 | 400 | body |
| `--fs-md` | 17 / 24 | 600 | card and section titles |
| `--fs-lg` | 22 / 28 | 650 | page titles |
| `--fs-xl` | 30 / 36 | 700 | case verdict, evaluation headline numbers |

Numbers use tabular figures. Never go below 13 px on screen.

### 6.3 Space, radius, elevation

- Space: 4, 8, 12, 16, 24, 32, 48. Replace `--s-3` to `--s-8` values.
- Radius: 6 (controls, chips), 10 (cards), 14 (drawers). The current 8, 10, 16 are close enough that only the largest changes.
- Elevation: none on cards (a line instead); one shadow for drawers, menus and tooltips.

### 6.4 Components

Each exists in `components/ui.tsx` unless marked New.

| Component | Specification |
|---|---|
| Button | Primary, secondary, ghost, danger; sizes 32 and 40 px (44 on touch); an icon only from Lucide, with an `aria-label` when there is no text; one primary per view |
| Status pill | Icon, word, tone. Replaces `Badge` and `Chip` where state is shown; chips stay for metadata |
| Evidence ladder | New. Four segments V0 to V3 with the level name on hover and focus; filled to the current level |
| Card | Flat: 1 px line, no fill change, a title row with optional actions; `flush` for tables |
| Table | 36 px rows; sticky header; tabular numbers; the whole row is a link or a button, never only a cell; keyboard: arrow keys move rows, Enter opens |
| Tabs | Existing `Tabs`; underline style; counts in the label |
| Form field | Existing `Field`: label above, hint below, error replaces hint, `aria-describedby` wired |
| Drawer | Existing; focus trap and restore; Escape closes |
| Replay marks | Existing `Replay.tsx`: circle with a tick for correct, ring with a cross for incorrect |
| Meter | New. A bar with a threshold marker; used for scores, coverage and VR-1 |
| Toast | New. Bottom right, 4 s for success, until dismissed for an error; `role="status"` or `role="alert"`; never the only way to learn a result |
| Skeleton | Existing; add one per page shaped like the page |
| Empty state | Existing; always a sentence and one action |

### 6.5 Patterns

- **Loading.** Skeleton in the page's shape; if old data is on screen, keep it and show a thin progress line (the `useLoad` hook already keeps stale data during reload).
- **Long operations** (replays, batches): a count, a bar, a cancel control, and the rest of the page remains usable. Results appear as they arrive.
- **Errors.** Plain words, what happened, what to do, a Retry button. Never a stack trace; the server's own message is shown.
- **Destructive or irreversible actions** (accept, reject): a confirm step that restates the consequence. The lifecycle table already makes the allowed set explicit.
- **Motion.** 120 ms for hover and focus, 220 ms for panels, easing `cubic-bezier(0.32, 0.72, 0, 1)` (existing). Replay marks fill as each result arrives. Nothing loops. `prefers-reduced-motion` is already handled in `base.css`; keep it and test it.

## 7. Responsive behaviour

Keep the existing three tiers; they are sound.

| Width | Layout |
|---|---|
| 1100 px and up | Sidebar 232 px; case file with the right rail |
| 721 to 1099 px | Icon rail 60 px; the rail moves under the case header |
| 720 px and below | Bottom tab bar with the first five nav items; tables become stacked rows; the graph draws vertically (existing); touch targets 44 px |

Wide tables get an `overflow-x: auto` box, never a page scroll. Evaluation's comparison table becomes one card per method on phones.

## 8. Accessibility

Existing: skip link, keyboard-operable graph, axe checks in the test suite, light and dark themes, plain-language field errors.

Requirements for everything new:

1. WCAG 2.2 AA: 4.5:1 for text, 3:1 for large text and graphical objects.
2. State never by colour alone (icon and word).
3. Every interactive element reachable and operable by keyboard; visible 2 px focus ring; focus restored when a drawer closes.
4. Live regions: progress and completion announced with `role="status"`; failures with `role="alert"`.
5. Charts have a table equivalent and a text summary.
6. Run axe on every new page in the existing `a11y.test.tsx`.
7. Manual pass with a screen reader and at 200% zoom before the Final. Automated checks catch part of the problems; this has not been done yet and the record says so.

## 9. Implementation notes

- **No new runtime dependency is required.** Routing stays on hash routes; add three route cases to `App.tsx`. Charts are plain SVG.
- **Free tooling if wanted:** Playwright for a browser end-to-end test and screenshots in CI (the committed plan already asks for one browser test); `axe-core` is installed.
- **A style guide page** at `#/styleguide` that renders every component in every state, behind a build flag. It replaces a separate design tool and keeps the design system testable.
- **Where each change lands:**

| Change | Files |
|---|---|
| New tokens, remove glass and aurora | `styles/tokens.css`, `styles/base.css`, `styles/components.css`, `styles/shell.css` |
| Navigation and routes | `App.tsx` |
| Inbox | `pages/Home.tsx`, `components/Filters.tsx` |
| Case file rail and Investigate | `pages/FindingDetail.tsx`, `components/Verify.tsx`, `components/Outcome.tsx` |
| Run page tabs and step badges | `pages/RunDetail.tsx`, `components/Graph.tsx`, `components/StepInspector.tsx` |
| Fault Lab, Evaluation, Import | new `pages/Lab.tsx`, `Evaluation.tsx`, `Import.tsx`; `api.ts`, `types.ts` |
| New components | `components/ui.tsx` (ladder, meter, toast) |

- **Do not break:** the interface shows only values returned by the API; the two server tests that compare the interface's copy of VR-1 and the lifecycle table to the server's must keep passing.

## 10. Prioritised roadmap

Effort is in person-days for one developer, from the code as it stands. Order assumes the backend items in the completion plan land first.

| Phase | Work | Days | Done when |
|---|---|---|---|
| **P0: with the committed features** | Investigate control and live attempts list in the case file | 1.5 | One click verifies suspects in order; progress is announced; works with a failing replay |
| | Fault Lab page (5.5) | 2 | A 43-run batch is generated and summarised from the page |
| | Export regression test action in the case rail | 0.5 | Downloads the file; error state shown |
| | Evaluation page (5.6), table first, chart second | 2.5 | Shows the harness JSON only; ties are visible; axe passes |
| | Navigation restructure, Inbox tabs (4, 5.1) | 1.5 | Every old link still works; tests updated |
| **P1: only if P0 is merged and time remains** | New tokens: remove glass and aurora, space and type scales, README fix | 1.5 | Visual regression screenshots reviewed; contrast re-measured |
| | Case file layout: sticky rail and section links | 1.5 | Verdict and next action stay visible while scrolling |
| | Run page: tabs, step badges, remove the duplicated tables | 2 | One place for each check result; scroll height measured before and after |
| | Adopt the Granite mark; favicon | 0.5 | `docs/brand/` status updated |
| | Style guide page; Playwright test of the main journey | 1.5 | Runs in CI |
| **P2: FYP-2** | Import page and validation report | 2 | Invalid and hostile files refused with a path |
| | Compare two runs (diff) | 3 | Changed steps and values highlighted |
| | Timeline tab (only with live timings) | 1.5 | |
| | Command palette (`Ctrl+K`) and list shortcuts | 1.5 | Keyboard only journey works |
| | Settings page: model, thresholds shown read-only | 1 | |
| | Aggregated graph mode for looping workflows | 3 | Needed once a workflow loops |

P0 is about 8 days of interface work across the team, on top of the backend items. If the schedule cannot hold it, cut in this order: the Evaluation chart (keep the table), then the Inbox tabs, then the Fault Lab progress detail.

### 10.1 Implementation status (2026-11-15)

| Item | State | Where, and how it was checked |
|---|---|---|
| P0: Investigate, Fault Lab, regression export, Evaluation | Done (earlier the same day) | `Verify.tsx`, `Lab.tsx`, `FindingDetail.tsx`, `Evaluation.tsx` |
| P0: Inbox with lifecycle tabs; Runs as its own page; Help group; "New run" only in the top bar | Done | `Home.tsx`, `Runs.tsx`, `QuickLook.tsx`, `App.tsx`. Tabs ask the server for each status of their group. The API's finding list now names the lead suspect and its latest replay counts (`lead`, tested in `test_journeys.py`), so a row shows the verdict without a request per row. [Screenshot](../../evidence/demos/2026-11-15_ui-inbox.png), [phone](../../evidence/demos/2026-11-15_ui-inbox-phone-390px.png) |
| P1: tokens; glass and aurora removed; five-step type scale; spacing 4 to 48 | Done | `tokens.css`, `base.css`, `components.css`, `shell.css`; guarded by `presentation.test.tsx` (scale, no `backdrop-filter`, contrast of every text token) |
| P1: case file with sticky rail and section links | Done | `FindingDetail.tsx`: verdict with fix and control counts and the interval, the one next step, exports, record; section links; the rail moves under the header below 1100 px. [Screenshot](../../evidence/demos/2026-11-15_ui-case-file-rail.png), [dark](../../evidence/demos/2026-11-15_ui-case-file-dark.png) |
| P1: run page tabs, step badges, duplicates removed | Done | `RunDetail.tsx`: Trace, Checks (outcome and step groups, failures first, each with what it was compared with), Data. "Observed vs source of truth" and the Findings card are gone; the step inspector shows observed against expected for the selected step. Timeline stays P2. [Trace](../../evidence/demos/2026-11-15_ui-run-trace-tab.png), [Checks](../../evidence/demos/2026-11-15_ui-run-checks-tab.png) |
| P1: Granite mark and favicon | Done | `BrandMark` in `ui.tsx` (the concept geometry from `docs/brand/`); favicon in `index.html` |
| P1: style guide page | Done | `#/styleguide`, in development builds or with `VITE_STYLEGUIDE=1`; in the axe suite. [Screenshot](../../evidence/demos/2026-11-15_ui-style-guide.png) |
| P1: Playwright test of the main journey | Done locally; **not yet run on GitHub** | `e2e/journey.e2e.ts`: Inbox, New run, run page tabs, case file, Verify (5/5 against 0/2), Accept, Decided tab, at 1366 px and on a Pixel 7 viewport, against the real API in recorded mode. It also runs axe's colour-contrast rule in the real browser on four screens, light and dark. Passed twice on 2026-11-15 in local Chrome. CI job `e2e` added to `ci.yml` |
| New components: evidence ladder, meter | Done | `Ladder`, `Meter` in `ui.tsx`. Toast not built (no screen needs it yet) |
| Manual screen-reader pass and 200% zoom (section 8, item 7) | **Not done** | Needs a person |
| Usability check with three people | **Not done** | [Protocol](../../docs/manuals/usability-check-protocol.md) |

## 11. How to know it worked

Measure these; do not claim them without the numbers.

| Question | Measure | Target to aim for |
|---|---|---|
| Can a new person find the origin of a failure? | Three people outside the team, five tasks from the usability protocol; time and errors | All three complete the core task unaided |
| Is the case page quicker to read? | Scroll height and steps to the verdict, before and after | Verdict and next action visible without scrolling |
| Is it accessible? | axe on every page; manual keyboard and screen-reader pass | Zero axe violations; the manual pass recorded in `evidence/uat/` |
| Is it responsive? | Screenshots at 390, 768 and 1280 px in CI | No horizontal page scroll |
| Does it still tell the truth? | The existing tests that tie the interface to the server | All pass |

## Sources

Read on 14 and 15 November 2026. Documentation and changelog text only; no screenshots or logged-in dashboards were viewed.

- Langfuse: [Agent Graphs](https://langfuse.com/docs/observability/features/agent-graphs), [graph view modes, July 2026](https://langfuse.com/changelog/2026-07-13-graph-view-modes), [timeline view](https://langfuse.com/changelog/2024-06-12-timeline-view)
- Arize Phoenix: [trace tree evals and decision spans, 30 September 2026](https://arize.com/docs/phoenix/release-notes/10-2026/10-01-2026-trace-tree-evals-and-decision-spans), [annotations release note](https://www.arize.com/docs/phoenix/release-notes/06-2026/06-24-2026-annotations-labels-and-pxi-server-tools)
- LangSmith: [trajectories](https://www.langchain.com/blog/langsmith-trajectories-tracing), [Engine overview](https://docs.langchain.com/langsmith/engine-overview), [quickstart](https://docs.langchain.com/langsmith/observability-quickstart/index.html)
- Braintrust: [compare experiments](https://www.braintrust.dev/docs/evaluate/compare-experiments), [interpret results](https://www.braintrust.dev/docs/evaluate/interpret-results.md)
- Raindrop: [documentation](https://www.raindrop.ai/docs/introduction), [signals](https://raindrop.ai/docs/platform/signals)
- Sentry: [Issue Details](https://docs.sentry.io/product/issues/issue-details), [new issue details UI](https://sentry.io/changelog/new-issue-details-ui-now-available/), [improved breadcrumbs](https://sentry.io/changelog/improved-breadcrumbs-on-issues)
- Linear: [behind the latest design refresh](https://linear.app/blog/behind-the-latest-design-refresh), [a design reset](https://linear.app/now/a-design-reset)
