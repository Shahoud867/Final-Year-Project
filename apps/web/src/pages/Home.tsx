import { Activity, ArrowRight, EyeOff, FlaskConical, Hourglass, PanelRight, Radar, ShieldCheck, Target, Workflow } from "lucide-react";
import { useState } from "react";
import { PAGE, api } from "../api";
import type { FindingFilter, RunFilter } from "../api";
import { Filters, RunFilters } from "../components/Filters";
import { Graph } from "../components/Graph";
import {
  Badge, Card, Chip, Drawer, Empty, ErrorBox, FaultBadge, Hash, LevelBadge, Loading, ModeBadge, PageHeader, Skeleton, Stat, TabPanel, Tabs,
} from "../components/ui";
import { leading, markOf, pathOf } from "../components/Verify";
import { ago, evidenceKind, finalText, label, pct, show } from "../format";
import { useLoad, useMediaQuery } from "../hooks";
import { AWAITING_REVIEW, STAGES, VERIFIED, countIn, reached } from "../lib/lifecycle";
import type { FindingSummary, RunSummary } from "../types";
import "../styles/pages/home.css";

type Selection = { kind: "run" | "finding"; id: string };
const kindLabel = (kind: string) => (kind === "silent_failure" ? "silent failure" : kind.replace(/_/g, " "));

/** Preview of one run: pipeline, reply, failed checks. Everything shown is read from the run and its graph. */
function RunPreview({ id }: { id: string }) {
  const run = useLoad(() => api.run(id), [id]);
  const graph = useLoad(() => api.graph(id), [id]);
  if (run.loading && !run.data) return <Skeleton lines={5} />;
  if (!run.data) return <p className="small muted">This run could not be loaded.</p>;
  const r = run.data;
  const n = (status: string) => r.check_results.filter((c) => c.status === status).length;
  const failed = r.check_results.filter((c) => c.status === "fail");
  const reply = finalText(r.trace?.run.final_output);
  return (
    <div className="home-preview">
      <header className="home-preview-head">
        <span className="eyebrow">Run</span>
        <h2>{r.task_input.order_id} <span className="mono small dim">{r.id}</span></h2>
        <div className="row tight"><Badge value={r.status} /><FaultBadge fault={r.fault_type} /><ModeBadge mode={r.llm_mode} model={r.model} /></div>
      </header>
      {graph.data && graph.data.nodes.length > 0 ? <Graph graph={graph.data} dense label="Run pipeline" /> : graph.loading ? <Skeleton lines={4} /> : null}
      {r.error ? <p className="small t-bad wrap-any">{r.error}</p> : (
        <div><div className="eyebrow">Workflow replied</div><p className="small home-clip">{reply || "n/a"}</p></div>
      )}
      {r.check_results.length > 0 ? (
        <div className="stack tight">
          <div className="eyebrow">Checks</div>
          <div className="bar" aria-hidden="true">
            {n("pass") ? <i className="tone-ok" style={{ flex: n("pass") }} /> : null}{n("fail") ? <i className="tone-bad" style={{ flex: n("fail") }} /> : null}
            {n("abstain") + n("error") ? <i className="tone-warn" style={{ flex: n("abstain") + n("error") }} /> : null}
          </div>
          <div className="legend"><span>{n("pass")} passed</span><span>{n("fail")} failed</span>{n("abstain") + n("error") ? <span>{n("abstain") + n("error")} not evaluated</span> : null}</div>
          {failed.map((c) => (
            <div key={c.check_id} className="small home-failed"><span className="mono t-bad">{c.check_id}</span><span className="mono">{show(c.observed)} <ArrowRight size={11} aria-hidden="true" /> expected {show(c.expected)}</span></div>
          ))}
        </div>
      ) : null}
      {r.trace_sha256 ? <div className="row tight small muted">trace <Hash value={r.trace_sha256} label="trace SHA-256" /></div> : null}
      <div className="row">
        <a className="btn sm" href={`#/runs/${r.id}`}><Workflow size={13} aria-hidden="true" />Open trace</a>
        {r.findings[0] ? <a className="btn primary sm" href={`#/findings/${r.findings[0].id}`}>Open investigation</a> : null}
      </div>
    </div>
  );
}

/** Preview of one finding: the leading hypothesis on the pipeline, the latest verdict, and what is allowed next. */
function FindingPreview({ id }: { id: string }) {
  const q = useLoad(() => api.finding(id), [id]);
  const runId = q.data?.run_id;
  const graph = useLoad(() => (runId ? api.graph(runId) : Promise.resolve(null)), [runId]);
  if (q.loading && !q.data) return <Skeleton lines={5} />;
  if (!q.data) return <p className="small muted">This finding could not be loaded.</p>;
  const f = q.data;
  const lead = leading(f.hypotheses);
  const path = pathOf(lead);
  const last = [...f.experiments].sort((a, b) => (b.created_at ?? "").localeCompare(a.created_at ?? ""))[0];
  const s = last?.summary;
  return (
    <div className="home-preview">
      <header className="home-preview-head">
        <span className="eyebrow">Finding · {kindLabel(f.kind)}</span>
        <h2>{f.title}</h2>
        <div className="row tight"><Badge value={f.status} /><LevelBadge level={f.verification_level} showName /><Chip>{f.severity}</Chip></div>
      </header>
      {graph.data && graph.data.nodes.length > 0 ? (
        <Graph graph={graph.data} dense label="Causal map" path={path.length > 1 ? path : undefined} marks={lead ? { [lead.step_id]: markOf(lead) } : undefined} />
      ) : graph.loading ? <Skeleton lines={4} /> : null}
      {lead ? (
        <div className="stack tight">
          <div className="eyebrow">{lead.status === "confirmed" ? "Origin confirmed" : "Leading hypothesis"}</div>
          <div className="row tight"><strong>{lead.agent}</strong><Chip>{evidenceKind(lead.evidence_kind)}</Chip><span className="mono small muted">score {lead.score.toFixed(2)}</span></div>
        </div>
      ) : null}
      {last ? (
        <div className="stack tight">
          <div className="eyebrow">Latest verification</div>
          <div className="row tight"><Badge value={last.verdict ?? last.status} />
            {s ? <span className="mono small">{s.k_pass}/{s.n_completed} fix · {s.c_pass}/{s.m_completed} control · {pct(s.ci_low)} to {pct(s.ci_high)}</span> : null}
          </div>
        </div>
      ) : null}
      <div className="stack tight">
        <div className="eyebrow">Allowed now</div>
        <div className="row tight">{f.allowed_actions.length === 0 ? <Chip>none: closed</Chip> : f.allowed_actions.map((a) => <Chip key={a} tone="replay">{label(a)}</Chip>)}</div>
      </div>
      <div className="row"><a className="btn primary sm" href={`#/findings/${f.id}`}>Open investigation</a><a className="btn sm" href={`#/runs/${f.run_id}`}><Workflow size={13} aria-hidden="true" />Open trace</a></div>
    </div>
  );
}

function Inspector({ sel }: { sel: Selection | null }) {
  if (!sel) return <Empty icon={PanelRight} title="Trace inspector">Select a run or a finding to see its pipeline, checks and verdict here.</Empty>;
  return sel.kind === "run" ? <RunPreview id={sel.id} key={sel.id} /> : <FindingPreview id={sel.id} key={sel.id} />;
}

export function Home() {
  const [tab, setTab] = useState("findings");
  const [filter, setFilter] = useState<FindingFilter>({});
  const [runFilter, setRunFilter] = useState<RunFilter>({});
  const [limit, setLimit] = useState(PAGE);
  const [sel, setSel] = useState<Selection | null>(null);
  const narrow = useMediaQuery("(max-width: 1100px)");
  // telemetry: loaded once; the lists below reload on their own filters
  const all = useLoad(() => api.runs({ limit: 100 }), []);
  const counts = useLoad(() => api.findingCounts(), []);
  const findings = useLoad(() => api.findings({ ...filter, limit }), [filter, limit]);
  const runFiltered = Object.values(runFilter).some(Boolean);
  const runList = useLoad(() => (tab === "runs" && runFiltered ? api.runs(runFilter) : Promise.resolve(null)), [tab, runFilter]);
  const filtered = Object.values(filter).some(Boolean);

  const runs = all.data ?? [];
  const done = runs.filter((r) => r.status === "completed");
  const errored = runs.filter((r) => r.status === "errored").length;
  const other = runs.length - done.length - errored;
  const silent = done.filter((r) => r.finding_count > 0).length;
  const total = reached(counts.data, 1);
  const stages = STAGES.map((name, i) => ({ name, n: reached(counts.data, i + 1) }));
  const faults = [...new Set(runs.map((r) => r.fault_type).filter((f): f is string => !!f))];
  const shownRuns: RunSummary[] = runFiltered ? runList.data ?? [] : runs.slice(0, PAGE);
  const rowsF: FindingSummary[] = findings.data ?? [];
  const first: Selection | null = tab === "findings"
    ? (rowsF[0] ? { kind: "finding", id: rowsF[0].id } : null)
    : (shownRuns[0] ? { kind: "run", id: shownRuns[0].id } : null);
  const shown = narrow ? sel : sel ?? first;
  const isSel = (kind: string, id: string) => shown?.kind === kind && shown.id === id;
  const na = (loading: boolean, value: number | string) => (loading ? <Skeleton lines={1} /> : value);

  return (
    <div className="page home">
      <PageHeader title="Investigations" />
      <ErrorBox message={all.error} onRetry={all.reload} />

      <div className="grid cols-4 home-kpis">
        <Stat label="Executions" icon={Activity} value={all.error ? "n/a" : na(all.loading && !all.data, runs.length)}
              unit={runs.length === 100 ? "latest" : undefined}
              sub={all.error || runs.length ? undefined : all.loading ? undefined : "No runs yet."}>
          {runs.length > 0 ? (
            <>
              <div className="bar" aria-hidden="true">{done.length ? <i className="tone-ok" style={{ flex: done.length }} /> : null}{errored ? <i className="tone-bad" style={{ flex: errored }} /> : null}{other ? <i className="tone-replay" style={{ flex: other }} /> : null}</div>
              <div className="legend"><span><i className="dot tone-ok" />{done.length} completed</span><span><i className="dot tone-bad" />{errored} errored</span>{other ? <span><i className="dot tone-replay" />{other} in progress</span> : null}</div>
            </>
          ) : null}
        </Stat>
        <Stat label="Silent failures" icon={EyeOff} hint="Runs that completed without raising an error but failed an outcome check. Output monitoring reports these as successful."
              value={all.error ? "n/a" : na(all.loading && !all.data, silent)} unit={all.error ? undefined : `of ${done.length} completed`} />
        <Stat label="Verified (V2+)" icon={Target} hint="Findings at level V2 (origin confirmed by controlled replays under rule VR-1) or V3 (accepted by a reviewer)."
              value={counts.error ? "n/a" : na(counts.loading && !counts.data, countIn(counts.data, VERIFIED))} unit={counts.error ? undefined : `of ${total} findings`}>
          {total > 0 ? (
            <ol className="home-funnel" aria-label="Findings by stage reached">
              {stages.map((s) => (
                <li key={s.name}><span>{s.name}</span><span className="bar" aria-hidden="true"><i className="tone-replay" style={{ flex: s.n }} /><i style={{ flex: total - s.n, background: "transparent" }} /></span><span className="mono num">{s.n}</span></li>
              ))}
            </ol>
          ) : null}
        </Stat>
        <Stat label="Awaiting review" icon={Hourglass} hint="Findings with a verdict (or strong evidence) that a person has not yet accepted or rejected."
              value={counts.error ? "n/a" : na(counts.loading && !counts.data, countIn(counts.data, AWAITING_REVIEW))} />
      </div>

      <div className="home-work">
        <Card flush className="home-list">
          <Tabs idBase="home" label="Records" value={tab} onChange={(t) => { setTab(t); setSel(null); }}
                tabs={[{ id: "findings", label: "Findings", icon: Radar, count: counts.data && !Array.isArray(counts.data) ? total : rowsF.length },
                       { id: "runs", label: "Runs", icon: Workflow, count: runs.length === 100 ? "100+" : runs.length }]} />
          <TabPanel idBase="home" id="findings" active={tab === "findings"} className="home-panel">
            <Filters value={filter} onApply={(next) => { setFilter(next); setLimit(PAGE); setSel(null); }} />
            <ErrorBox message={findings.error} onRetry={findings.reload} />
            {findings.loading && !findings.data ? <Loading /> : null}
            {findings.data && rowsF.length === 0 && !findings.error ? (
              <Empty icon={ShieldCheck} action={filtered ? undefined : <a className="btn sm" href="#/new"><FlaskConical size={13} aria-hidden="true" />Open Task Studio</a>}>
                {filtered ? "No finding matches these filters." : "No findings yet. Start a run with a fault injected to see one."}
              </Empty>
            ) : null}
            {rowsF.length > 0 ? (
              <div className="table-wrap"><table className="home-table">
                <thead><tr><th>Finding</th><th>Status</th><th>Level</th><th>Severity</th><th>Symptom</th><th>Opened</th><th><span className="sr-only">Inspect</span></th></tr></thead>
                <tbody>
                  {rowsF.map((f) => (
                    <tr key={f.id} className="click" aria-selected={isSel("finding", f.id) || undefined} onClick={() => setSel({ kind: "finding", id: f.id })}>
                      <td><a className="home-title" href={`#/findings/${f.id}`} title={f.title}>{f.title}</a><div className="row tight small"><span className="mono dim">{f.id}</span><Chip tone={f.kind === "silent_failure" ? "bad" : "neutral"}>{kindLabel(f.kind)}</Chip></div></td>
                      <td><Badge value={f.status} /></td>
                      <td><LevelBadge level={f.verification_level} /></td>
                      <td>{f.severity}</td>
                      <td className="mono">{f.symptom_step}</td>
                      <td className="small nowrap">{ago(f.created_at)}</td>
                      <td><button type="button" className="btn ghost icon sm" aria-label={`Inspect ${f.title}`} onClick={(e) => { e.stopPropagation(); setSel({ kind: "finding", id: f.id }); }}><PanelRight size={14} aria-hidden="true" /></button></td>
                    </tr>
                  ))}
                </tbody>
              </table></div>
            ) : null}
            {findings.data && findings.data.length >= limit ? <div className="home-more"><button type="button" className="btn sm" onClick={() => setLimit(limit + PAGE)}>Show more</button></div> : null}
          </TabPanel>
          <TabPanel idBase="home" id="runs" active={tab === "runs"} className="home-panel">
            <RunFilters value={runFilter} faults={faults} onApply={(next) => { setRunFilter(next); setSel(null); }} />
            <ErrorBox message={runList.error} onRetry={runList.reload} />
            {runFiltered && runList.loading && !runList.data ? <Loading /> : null}
            {shownRuns.length === 0 && !(runFiltered && runList.loading) ? (
              <Empty icon={Workflow} action={runFiltered ? undefined : <a className="btn sm" href="#/new"><FlaskConical size={13} aria-hidden="true" />Open Task Studio</a>}>
                {runFiltered ? "No run matches these filters." : "Nothing has run yet."}
              </Empty>
            ) : null}
            {shownRuns.length > 0 ? (
              <div className="table-wrap"><table className="home-table">
                <thead><tr><th>Run</th><th>Status</th><th>Condition</th><th>Mode</th><th className="num">Failed checks</th><th className="num">Findings</th><th>Started</th><th><span className="sr-only">Inspect</span></th></tr></thead>
                <tbody>
                  {shownRuns.map((r) => (
                    <tr key={r.id} className="click" aria-selected={isSel("run", r.id) || undefined} onClick={() => setSel({ kind: "run", id: r.id })}>
                      <td><a href={`#/runs/${r.id}`}>{r.task_input.order_id}</a><div className="small mono dim">{r.id}</div></td>
                      <td><Badge value={r.status} /></td>
                      <td><FaultBadge fault={r.fault_type} /></td>
                      <td><ModeBadge mode={r.llm_mode} /></td>
                      <td className="num">{r.failed_checks}</td>
                      <td className="num">{r.finding_count}</td>
                      <td className="small nowrap">{ago(r.created_at)}</td>
                      <td><button type="button" className="btn ghost icon sm" aria-label={`Inspect run ${r.task_input.order_id} ${r.id}`} onClick={(e) => { e.stopPropagation(); setSel({ kind: "run", id: r.id }); }}><PanelRight size={14} aria-hidden="true" /></button></td>
                    </tr>
                  ))}
                </tbody>
              </table></div>
            ) : null}
            {!runFiltered && runs.length > PAGE ? <p className="small dim home-more">Showing the {PAGE} newest of {runs.length === 100 ? "100 or more" : runs.length} runs. Filter to find older ones.</p> : null}
          </TabPanel>
        </Card>

        {narrow ? (
          <Drawer open={!!sel} onClose={() => setSel(null)} title="Trace inspector" width={460}><Inspector sel={sel} /></Drawer>
        ) : (
          <aside className="card home-inspector" aria-label="Trace inspector"><Inspector sel={shown} /></aside>
        )}
      </div>
    </div>
  );
}
