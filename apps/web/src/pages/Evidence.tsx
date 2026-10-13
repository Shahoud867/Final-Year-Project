/** Evidence: why a silent failure is missed, what Granite does about it, what is built and planned, and how it is delivered. */
import {
  ArrowRight, CircleCheck, CircleDashed, CircleHelp, CircleX, ExternalLink, EyeOff, Fingerprint, FlaskConical, GitBranch, Gavel, ListChecks,
  MessagesSquare, Minus, Package, RefreshCw, Rocket, Route, Scale, Server, ShieldCheck, Sigma, TriangleAlert,
} from "lucide-react";
import { useState } from "react";
import { api } from "../api";
import { comparedWith } from "../components/CheckDetail";
import { Badge, Card, Chip, Compare, Notice, PageHeader, Skeleton } from "../components/ui";
import type { Icon, Tone } from "../components/ui";
import { BUILD, CD_JOBS, CI_JOBS, actionsUrl, commitUrl, fetchPipeline, latestRun, passedFor, repoUrl, workflowFileUrl } from "../delivery";
import type { WorkflowRun } from "../delivery";
import { finalText, modeLabel, when } from "../format";
import { useLoad } from "../hooks";
import "../styles/pages/evidence.css";

const doc = (path: string) => `${repoUrl()}/blob/main/${path}`;

/** Evidence classes of attribution and their weights (packages/granite_core/granite_core/attribution.py, WEIGHTS). */
const WEIGHTS: [string, number][] = [
  ["contradicts the source of truth", 1.0], ["broke its own contract", 0.8], ["hand-off differs from upstream", 0.7],
  ["no check on the step", 0.2], ["consistent with its inputs", 0.1],
];

const MECHANISMS: { icon: Icon; title: string; text: string; source: string; path: string }[] = [
  { icon: ListChecks, title: "Independent contracts", text: "Every run is tested by executable rules against data the workflow does not control. No answer key is needed.", source: "checks.py", path: "packages/granite_core/granite_core/checks.py" },
  { icon: Route, title: "Deterministic attribution", text: "Steps on the path back from the symptom are ranked by the evidence they carry. No model is asked.", source: "attribution.py", path: "packages/granite_core/granite_core/attribution.py" },
  { icon: FlaskConical, title: "Counterfactual replay", text: "Earlier steps are frozen, the suspect's output is corrected, and the rest of the workflow runs again.", source: "experiment.py", path: "packages/granite_core/granite_core/experiment.py" },
  { icon: Sigma, title: "Statistical verdict", text: "Fix replays are compared with control replays under a rule fixed in advance, with a 95% interval.", source: "verification.py", path: "packages/granite_core/granite_core/verification.py" },
  { icon: Gavel, title: "Human review", text: "A named person accepts or rejects. The server refuses any decision the lifecycle does not allow.", source: "lifecycle.py", path: "packages/granite_core/granite_core/lifecycle.py" },
  { icon: Fingerprint, title: "Hashed evidence", text: "Each record stores the SHA-256 of its canonical JSON, recomputed every time it is shown. Nothing can be edited.", source: "evidence.py", path: "packages/granite_core/granite_core/evidence.py" },
];

type Cell = [Tone | "none", string];
/** From research/market/commercial-product-comparison.md (public documentation reviewed 2026-08-22). */
const MATRIX: { row: string; cells: [Cell, Cell, Cell, Cell] }[] = [
  { row: "Trace capture and agent graph", cells: [["warn", "One workflow, own runner"], ["ok", "Yes"], ["ok", "Yes: graphs, nested spans"], ["ok", "Yes: OpenTelemetry"]] },
  { row: "Root-cause attribution", cells: [["ok", "Step-level, deterministic"], ["neutral", "Human-driven. Engine (beta): mechanism not published"], ["neutral", "Human-driven"], ["neutral", "Human-driven, LLM-assisted. Alyx: mechanism not documented"]] },
  { row: "Fix tested by replay before it is trusted", cells: [["ok", "N fix replays against M controls"], ["none", "Not documented"], ["none", "Not documented"], ["none", "Not documented"]] },
  { row: "Silent-failure detection", cells: [["ok", "Executable checks against a source of truth"], ["none", "Not documented"], ["none", "Not documented"], ["none", "Not documented"]] },
  { row: "Framework generality", cells: [["warn", "Refund Desk only; adapters planned"], ["neutral", "LangChain and LangGraph oriented"], ["ok", "Framework-agnostic, open source, self-hostable"], ["ok", "Framework-agnostic, open source"]] },
  { row: "Maturity and scale", cells: [["warn", "Student prototype, 10-task feasibility run"], ["ok", "Production platform"], ["ok", "Production platform"], ["ok", "Production platform"]] },
];
const CELL_ICON: Record<string, Icon> = { ok: CircleCheck, warn: TriangleAlert, neutral: CircleDashed, none: CircleHelp };

const BUILT: [string, string, string][] = [
  ["F1", "Run a workflow and record every step", "#/new"], ["F2", "Check the outcome, detect silent failures", "#/"],
  ["F3", "Trace back to where it began", "#/"], ["F4", "Verify by controlled replay", "#/"], ["F5", "Review: a person decides", "#/"],
  ["F6", "Record evidence, export a report", "#/"], ["F7", "Find earlier runs and findings", "#/"], ["F8", "Explain itself: guide and API reference", "#/guide"],
];
const PLANNED_FINAL1 = ["Trace import from other tools", "A second workflow", "Three fault types", "Python SDK with a LangGraph adapter", "Fix suggestions", "Redaction of stored personal data", "PDF reports", "First evaluation against baselines"];
const PLANNED_FYP2 = ["Benchmark of at least 300 runs", "CrewAI adapter", "User acceptance testing", "Graph view for branching workflows"];
const LIMITS = [
  "One workflow and one fault type",
  "Personal data is not redacted before storage (defect D-07); synthetic data only",
  "No usability test with outside users yet",
  "Evaluation so far: ten tasks, one small model",
];

/** Pre-registered feasibility run, research/eval/results/2026-10-07_refund-desk-feasibility.md (copied exactly). */
const METRICS: [string, string, string, string][] = [
  ["M1", "Faulty runs detected", "10/10", "at least 90%"],
  ["M2", "Clean runs with a finding", "1/10", "0 false alarms"],
  ["M3", "Origin ranked first", "10/10", "at least 80%"],
  ["M4", "Origin confirmed by replay", "9/10", "at least 80%"],
  ["M5", "Innocent step refuted", "10/10", "at least 80%"],
  ["M6", "Runs completed", "20/20", "at least 95%"],
];

const PANEL: [string, string, [string, string][]][] = [
  ["A1", "UI/UX needs improvement.", [["This interface", "#/"]]],
  ["A2", "Features are not sufficiently clear.", [["How it works", "#/guide"]]],
  ["A3", "It is unclear what inputs each feature will accept.", [["How it works", "#/guide"], ["Task Studio", "#/new"]]],
  ["A4", "It is unclear how flaws will be verified and how results will be captured.", [["A finding: Verification results, Evidence", "#/"]]],
  ["A5", "The overall project workflow must be redefined.", [["Lifecycle on every finding", "#/"], ["Guide", "#/guide"]]],
  ["A6", "Core module with CI/CD on a live interface.", [["Delivery pipeline, on this page", "#/evidence"]]],
];

function Lanes() {
  const pick = useLoad(async () => {
    const runs = await api.runs({ limit: 50 });
    const hit = runs.find((r) => r.status === "completed" && r.finding_count > 0);
    return hit ? api.run(hit.id) : null;
  }, []);
  const r = pick.data;
  const failed = r?.check_results.find((c) => c.scope === "outcome" && c.status === "fail");
  const finding = r?.findings[0];
  return (
    <Card title="Why output monitoring misses a silent failure" icon={EyeOff}
          sub={r ? <>a real run on this server: <a href={`#/runs/${r.id}`} className="mono">{r.id}</a></> : "schematic: no such run on this server yet"}>
      {pick.loading && !pick.data ? <Skeleton lines={4} /> : (
        <div className="ev-lanes">
          <div className="ev-lane">
            <div className="eyebrow">Output monitoring</div>
            <ul className="checklist small">
              <li><CircleCheck size={14} className="t-ok" aria-hidden="true" /><span>Run status: {r ? r.status : "completed"}</span></li>
              <li><CircleCheck size={14} className="t-ok" aria-hidden="true" /><span>Error raised: {r?.error ? "yes" : "none"}</span></li>
              <li><CircleCheck size={14} className="t-ok" aria-hidden="true" /><span>A fluent reply was produced</span></li>
            </ul>
            {r ? <p className="small ev-reply">{finalText(r.trace?.run.final_output)}</p> : null}
            <div className="ev-conclusion"><Badge value="ok" text="Looks healthy" /></div>
          </div>
          <div className="ev-lane-arrow" aria-hidden="true"><ArrowRight size={18} /></div>
          <div className="ev-lane ev-lane-granite">
            <div className="eyebrow">Granite</div>
            {failed ? (
              <>
                <p className="small">Outcome check <span className="mono">{failed.check_id}</span> compares the reply with {comparedWith(failed)}.</p>
                <Compare observed={failed.observed} expected={failed.expected}
                         observedLabel={failed.type === "truth" ? "Told to the customer" : "Observed"} expectedLabel={failed.type === "truth" ? "Source of truth" : "Expected"} />
              </>
            ) : (
              <ul className="checklist small">
                <li><ListChecks size={14} aria-hidden="true" /><span>An outcome check compares the reply with a source of truth the workflow does not control</span></li>
                <li><CircleX size={14} className="t-bad" aria-hidden="true" /><span>A mismatch opens a finding, even though nothing crashed</span></li>
              </ul>
            )}
            <div className="ev-conclusion">
              <Badge value="fail" text="Silent failure found" />
              {finding ? <a className="btn sm" href={`#/findings/${finding.id}`}>Open the finding</a> : <a className="btn sm" href="#/new">Run the silent price discrepancy scenario</a>}
            </div>
          </div>
        </div>
      )}
    </Card>
  );
}

function RunLine({ title, run }: { title: string; run: WorkflowRun | null }) {
  return (
    <li className="ev-runline">
      <span className="ev-runline-title">{title}</span>
      {run ? (
        <>
          <Badge value={run.conclusion ?? run.status} />
          <a href={run.html_url} target="_blank" rel="noreferrer" className="mono">{run.name} #{run.run_number}<ExternalLink size={11} aria-hidden="true" /></a>
          <span className="mono small dim">{run.head_sha.slice(0, 7)}</span>
          <span className="small dim">{when(run.created_at)}</span>
        </>
      ) : <span className="small dim">no completed run among the latest listed</span>}
    </li>
  );
}

function Delivery() {
  const health = useLoad(() => api.health(), []);
  const [fresh, setFresh] = useState(0);
  const pipe = useLoad(() => fetchPipeline(BUILD.repo, fresh > 0), [fresh]);
  const runs = pipe.data?.runs ?? [];
  const tag = runs.find((r) => r.name === "CD" && r.event === "push" && (r.head_branch ?? "").startsWith("v") && r.status === "completed") ?? null;
  const proof = passedFor(runs, "CI", BUILD.sha);
  const failedToLoad = !pipe.loading && !pipe.data;
  return (
    <Card title="Delivery pipeline (CI/CD)" icon={Rocket} sub="read live, never assumed"
          actions={<button type="button" className="btn sm" onClick={() => setFresh(fresh + 1)} disabled={pipe.loading}><RefreshCw size={13} aria-hidden="true" className={pipe.loading ? "spin" : undefined} />Refresh</button>}>
      <div className="ev-delivery">
        <div className="ev-instance">
          <div className="eyebrow">This instance</div>
          <dl className="kv">
            <dt>Address</dt><dd className="mono wrap-any">{window.location.origin}</dd>
            <dt>Server</dt><dd>{health.data ? <>v{health.data.version}, {modeLabel(health.data.llm_mode).toLowerCase()}</> : health.loading ? "checking…" : "server unreachable"}</dd>
            <dt>Built from</dt>
            <dd>{BUILD.sha ? <><a className="mono" href={commitUrl(BUILD.sha)} target="_blank" rel="noreferrer">{BUILD.sha}</a>{BUILD.time ? <span className="small dim"> · {when(BUILD.time)}</span> : null}</> : <span className="dim">no build stamp</span>}</dd>
          </dl>
          {pipe.data ? (
            proof
              ? <p className="small row tight"><CircleCheck size={14} className="t-ok" aria-hidden="true" />This build's commit passed CI (<a href={proof.html_url} target="_blank" rel="noreferrer">run #{proof.run_number}</a>)</p>
              : <p className="small muted row tight"><Minus size={14} aria-hidden="true" />No successful CI run for this build's commit among the latest runs</p>
          ) : null}
        </div>
        <div className="ev-status" aria-live="polite">
          <div className="eyebrow">Workflows on GitHub</div>
          {pipe.loading && !pipe.data ? <Skeleton lines={3} /> : failedToLoad ? (
            <Notice tone="warn" title="Pipeline status unknown">
              {pipe.error}{" "}
              <a href={actionsUrl()} target="_blank" rel="noreferrer">Open the Actions page</a>
            </Notice>
          ) : (
            <>
              <ul className="ev-runs">
                <RunLine title="CI on main" run={latestRun(runs, "CI")} />
                <RunLine title="CD on main" run={latestRun(runs, "CD")} />
                <RunLine title="Release tag" run={tag} />
              </ul>
              <p className="small dim">Read from api.github.com at {when(pipe.data?.fetchedAt)}{tag ? <> · tag <span className="mono">{tag.head_branch}</span></> : null}</p>
            </>
          )}
        </div>
      </div>
      <ol className="ev-pipeline" aria-label="Pipeline stages">
        <li className="ev-pstage"><span className="ev-pstage-title"><GitBranch size={14} aria-hidden="true" />Branch and pull request</span><span className="small muted">short-lived branch, review, squash-merge to main</span></li>
        {CI_JOBS.map((j) => <li key={j.name} className="ev-pstage ci"><span className="ev-pstage-title"><ShieldCheck size={14} aria-hidden="true" />CI: {j.name}</span><span className="small muted">{j.does}</span></li>)}
        {CD_JOBS.map((j) => <li key={j.name} className="ev-pstage cd"><span className="ev-pstage-title"><Package size={14} aria-hidden="true" />CD: {j.name}</span><span className="small muted">{j.does}</span></li>)}
      </ol>
      <p className="small muted row loose">
        <a href={workflowFileUrl("ci.yml")} target="_blank" rel="noreferrer">ci.yml</a>
        <a href={workflowFileUrl("cd.yml")} target="_blank" rel="noreferrer">cd.yml</a>
        <a href={doc(".github/CONTRIBUTING.md")} target="_blank" rel="noreferrer">branching method</a>
        <a href={doc("docs/registers/deployment-record.md")} target="_blank" rel="noreferrer">deployment record</a>
      </p>
    </Card>
  );
}

export function Evidence() {
  return (
    <div className="page ev">
      <PageHeader eyebrow="Evidence and differentiation" title="Evidence"
                  sub="What Granite does that ordinary monitoring does not, what is built, what is planned, and how it is delivered." />
      <Lanes />

      <Card title="What Granite does about it" icon={ShieldCheck} sub="six mechanisms, each in one file">
        <div className="ev-mech">
          {MECHANISMS.map((m) => (
            <div key={m.title} className="ev-mech-card">
              <div className="row tight"><span className="ev-icon"><m.icon size={15} aria-hidden="true" /></span><h3>{m.title}</h3></div>
              <p className="small muted">{m.text}</p>
              {m.source === "attribution.py" ? (
                <ul className="ev-weights" aria-label="Evidence classes and weights">
                  {WEIGHTS.map(([name, w]) => <li key={name}><span>{name}</span><span className="bar" aria-hidden="true"><i className="tone-warn" style={{ flex: w }} /><i style={{ flex: 1 - w, background: "transparent" }} /></span><span className="mono">{w.toFixed(1)}</span></li>)}
                </ul>
              ) : null}
              <a className="chip mono ev-src" href={doc(m.path)} target="_blank" rel="noreferrer">{m.source}<ExternalLink size={10} aria-hidden="true" /></a>
            </div>
          ))}
        </div>
      </Card>

      <Card title="Compared with agent observability platforms" icon={Scale} sub="from public documentation; not a benchmark">
        <div className="table-wrap">
          <table className="ev-matrix">
            <thead><tr><th>Capability</th><th>Granite</th><th>LangSmith</th><th>Langfuse</th><th>Arize Phoenix</th></tr></thead>
            <tbody>
              {MATRIX.map((m) => (
                <tr key={m.row}>
                  <th scope="row">{m.row}</th>
                  {m.cells.map(([tone, text], i) => {
                    const I = CELL_ICON[tone] ?? CircleDashed;
                    return <td key={i}><span className={`ev-cell${tone === "ok" ? " t-ok" : tone === "warn" ? " t-warn" : ""}`}><I size={13} aria-hidden="true" /><span>{text}</span></span></td>;
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="small muted">
          Based on what each vendor's public documentation stated when the team reviewed it on 22 August 2026
          (<a href={doc("research/market/commercial-product-comparison.md")} target="_blank" rel="noreferrer">source and caveats</a>). "Not documented" means no public description was found, not that the capability is absent.
          No superiority is claimed: these platforms capture traces at production scale, which Granite does not attempt. Granite is a diagnosis layer that could sit beside them.
        </p>
      </Card>

      <Card title="Built and planned" icon={Package}>
        <div className="ev-scope">
          <div className="ev-col">
            <div className="row tight"><h3>Built</h3><Chip tone="ok" icon={CircleCheck}>FYP-1 mid, Iteration 1</Chip></div>
            <ul className="list-plain stack tight">
              {BUILT.map(([id, text, href]) => <li key={id} className="ev-item"><Chip mono>{id}</Chip><a href={href}>{text}</a></li>)}
            </ul>
          </div>
          <div className="ev-col">
            <div className="row tight"><h3>FYP-1 final</h3><Chip icon={CircleDashed}>Planned, Iteration 2</Chip></div>
            <ul className="list-plain stack tight">{PLANNED_FINAL1.map((t) => <li key={t} className="ev-item planned"><span>{t}</span><span className="small dim">Planned</span></li>)}</ul>
          </div>
          <div className="ev-col">
            <div className="row tight"><h3>FYP-2</h3><Chip icon={CircleDashed}>Planned</Chip></div>
            <ul className="list-plain stack tight">{PLANNED_FYP2.map((t) => <li key={t} className="ev-item planned"><span>{t}</span><span className="small dim">Planned</span></li>)}</ul>
            <h3 className="ev-limits-h">Known limits today</h3>
            <ul className="ev-limits small muted">{LIMITS.map((t) => <li key={t}>{t}</li>)}</ul>
          </div>
        </div>
      </Card>

      <Card title="Measured so far" icon={Sigma} sub="pre-registered feasibility run, 7 October 2026: 10 tasks, 1 fault type, llama3.2:3b">
        <div className="ev-metrics">
          {METRICS.map(([id, name, result, threshold]) => (
            <div key={id} className="ev-metric">
              <span className="eyebrow">{id} · {name}</span>
              <span className="ev-metric-value mono">{result}</span>
              <span className="small dim">threshold: {threshold}</span>
            </div>
          ))}
        </div>
        <p className="small muted">
          Read with care: ten tasks, one fault, one small model; four tasks were not blind. The M2 finding was a genuine model error that nobody injected, and the M4 miss was a second, masked fault.
          Thresholds were fixed before the run. <a href={doc("research/eval/results/2026-10-07_refund-desk-feasibility-notes.md")} target="_blank" rel="noreferrer">Results and how to read them</a>
        </p>
      </Card>

      <Delivery />

      <Card title="Panel feedback, and where to see the answer" icon={MessagesSquare}>
        <ul className="ev-panel">
          {PANEL.map(([id, quote, links]) => (
            <li key={id}>
              <Chip mono>{id}</Chip>
              <span className="ev-quote">{quote}</span>
              <span className="row tight">{links.map(([text, href]) => <a key={text} className="btn sm ghost" href={href}><ArrowRight size={12} aria-hidden="true" />{text}</a>)}</span>
            </li>
          ))}
        </ul>
        <p className="small muted row tight"><Server size={13} aria-hidden="true" />Status and evidence for each action are kept in the <a href={doc("docs/registers/form-10-panel-actions.md")} target="_blank" rel="noreferrer">Form 10 register</a>, not here.</p>
      </Card>
    </div>
  );
}
