import { ArrowRight, PanelRight, Workflow } from "lucide-react";
import { api } from "../api";
import { ago, evidenceKind, finalText, label, pct, show } from "../format";
import { useLoad } from "../hooks";
import type { FindingSummary } from "../types";
import { Graph } from "./Graph";
import { Badge, Chip, Empty, FaultBadge, Hash, Ladder, ModeBadge, Skeleton } from "./ui";
import { leading, markOf, pathOf } from "./Verify";
import "../styles/pages/home.css";

export type Selection = { kind: "run" | "finding"; id: string };
export const kindLabel = (kind: string) => (kind === "silent_failure" ? "silent failure" : kind.replace(/_/g, " "));

/** The lead suspect's verdict in words and the replay counts behind it, from the list row alone (no extra request). */
export function verdictOf(f: FindingSummary): { word: string; counts: string } {
  const l = f.lead;
  if (!l) return { word: f.kind === "explicit_error" ? "Run stopped with an error" : "No suspect ranked", counts: "" };
  const counts = l.fix_n ? `${l.fix_pass}/${l.fix_n} with fix, ${l.control_pass ?? 0}/${l.control_n ?? 0} without` : "";
  const word = { confirmed: "Confirmed", refuted: "Refuted", inconclusive: "Inconclusive" }[l.status] ?? "Suspect, not verified yet";
  return { word, counts };
}

/** Preview of one run: pipeline, reply, failed checks. Everything shown is read from the run and its graph. */
export function RunPreview({ id }: { id: string }) {
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
        {r.findings[0] ? <a className="btn primary sm" href={`#/findings/${r.findings[0].id}`}>Open case</a> : null}
      </div>
    </div>
  );
}

/** Preview of one finding: the leading hypothesis on the pipeline, the latest verdict, and what is allowed next. */
export function FindingPreview({ id }: { id: string }) {
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
        <div className="row tight"><Badge value={f.status} /><Ladder level={f.verification_level} /><Chip>{f.severity}</Chip></div>
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
      <div className="row"><a className="btn primary sm" href={`#/findings/${f.id}`}>Open case</a><a className="btn sm" href={`#/runs/${f.run_id}`}><Workflow size={13} aria-hidden="true" />Open trace</a></div>
      <p className="small dim">Opened {ago(f.created_at)}</p>
    </div>
  );
}

export function QuickLook({ sel }: { sel: Selection | null }) {
  if (!sel) return <Empty icon={PanelRight} title="Quick look">Select a row to see its pipeline, checks and verdict here.</Empty>;
  return sel.kind === "run" ? <RunPreview id={sel.id} key={sel.id} /> : <FindingPreview id={sel.id} key={sel.id} />;
}
