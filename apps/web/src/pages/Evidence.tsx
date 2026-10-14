/** Evidence: why a silent failure is missed, what Granite does about it, and how it is delivered. */
import {
  ArrowRight, CircleCheck, CircleX, ExternalLink, EyeOff, Fingerprint, FlaskConical, GitBranch, Gavel, ListChecks, Minus, Package,
  RefreshCw, Rocket, Route, ShieldCheck, Sigma,
} from "lucide-react";
import { useState } from "react";
import { api } from "../api";
import { comparedWith } from "../components/CheckDetail";
import { Badge, Card, Compare, Notice, PageHeader, Skeleton } from "../components/ui";
import type { Icon } from "../components/ui";
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

const MECHANISMS: { icon: Icon; title: string; source: string; path: string }[] = [
  { icon: ListChecks, title: "Independent contracts", source: "checks.py", path: "packages/granite_core/granite_core/checks.py" },
  { icon: Route, title: "Deterministic attribution", source: "attribution.py", path: "packages/granite_core/granite_core/attribution.py" },
  { icon: FlaskConical, title: "Counterfactual replay", source: "experiment.py", path: "packages/granite_core/granite_core/experiment.py" },
  { icon: Sigma, title: "Statistical verdict", source: "verification.py", path: "packages/granite_core/granite_core/verification.py" },
  { icon: Gavel, title: "Human review", source: "lifecycle.py", path: "packages/granite_core/granite_core/lifecycle.py" },
  { icon: Fingerprint, title: "Hashed evidence", source: "evidence.py", path: "packages/granite_core/granite_core/evidence.py" },
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
      <PageHeader title="Evidence" sub="What Granite does that ordinary monitoring does not." />
      <Lanes />

      <Card title="What Granite does about it" icon={ShieldCheck} sub="six mechanisms, each in one file">
        <div className="ev-mech">
          {MECHANISMS.map((m) => (
            <div key={m.title} className="ev-mech-card">
              <div className="row tight"><span className="ev-icon"><m.icon size={15} aria-hidden="true" /></span><h3>{m.title}</h3></div>
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

    </div>
  );
}
