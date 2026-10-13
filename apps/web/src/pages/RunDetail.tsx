import {
  ArrowDown, CircleCheck, CircleX, Eye, EyeOff, ListChecks, MessageSquare, RotateCcw, Scale, Search, ShieldAlert, Syringe, Waypoints,
} from "lucide-react";
import { useState } from "react";
import type { ReactNode } from "react";
import { ApiError, api, waitForJob } from "../api";
import { Computation, comparedWith } from "../components/CheckDetail";
import { Graph } from "../components/Graph";
import type { NodeMark } from "../components/Graph";
import { StepInspector, produced } from "../components/StepInspector";
import { Badge, Card, Chip, Compare, ErrorBox, FaultBadge, Hash, LevelBadge, Loading, ModeBadge, Notice, PageHeader, Skeleton } from "../components/ui";
import { leading, markOf, pathOf } from "../components/Verify";
import { duration, finalText, show, stepKind, when } from "../format";
import { useLoad } from "../hooks";
import type { CheckResult } from "../types";
import "../styles/pages/run.css";

/** One line of the "what monitoring sees" list: a fact of the run and whether it looks healthy. */
function Seen({ ok, children }: { ok: boolean; children: ReactNode }) {
  return (
    <li>{ok ? <CircleCheck size={14} className="t-ok" aria-hidden="true" /> : <CircleX size={14} className="t-bad" aria-hidden="true" />}
      <span>{children}</span></li>
  );
}

export function RunDetail({ id }: { id: string }) {
  const run = useLoad(() => api.run(id), [id]);
  const graph = useLoad(() => api.graph(id), [id]);
  const findingId = run.data?.findings[0]?.id;
  // the leading hypothesis decides which step is marked as suspect or confirmed origin; the page works without it
  const finding = useLoad(() => (findingId ? api.finding(findingId) : Promise.resolve(null)), [findingId]);
  const [selected, setSelected] = useState<string | null>(null);
  const [reveal, setReveal] = useState(false);
  const [retrying, setRetrying] = useState(false);
  const [retryError, setRetryError] = useState("");

  if (run.loading && !run.data) return <Loading />;
  if (run.error || !run.data) return <ErrorBox message={run.error || "Run not found."} onRetry={run.reload} />;
  const r = run.data;
  const steps = r.trace?.steps ?? [];
  const agent = (stepId: string) => steps.find((s) => s.step_id === stepId)?.agent ?? stepId;
  const order = (c: CheckResult) => { const i = steps.findIndex((s) => s.step_id === c.step); return i < 0 ? 99 : i; };
  const reply = finalText(r.trace?.run.final_output);
  const completed = r.status === "completed";
  const outcome = r.check_results.filter((c) => c.scope === "outcome");
  const failedOutcome = outcome.filter((c) => c.status === "fail");
  const passedOutcome = outcome.filter((c) => c.status === "pass");
  const failed = r.check_results.filter((c) => c.status === "fail").sort((a, b) => order(a) - order(b) || (a.scope === "outcome" ? 1 : -1));
  const failedSteps = failed.filter((c) => c.scope === "step");
  const count = (status: string) => r.check_results.filter((c) => c.status === status).length;
  const lead = finding.data ? leading(finding.data.hypotheses) : undefined;
  const path = pathOf(lead);
  const marks: Record<string, NodeMark> = {};
  if (lead) marks[lead.step_id] = markOf(lead);
  if (reveal && r.injected_fault) marks[r.injected_fault.target_step] = "fault";

  async function retry() {
    setRetrying(true); setRetryError("");
    try {
      const { run_id, job_id } = await api.createRun({ task_input: r.task_input, fault: r.fault_type, mode: "auto", seed: r.seed });
      await waitForJob(job_id);
      window.location.hash = `#/runs/${run_id}`;
    } catch (e) {
      setRetryError(e instanceof ApiError ? e.message : "Something went wrong.");
      setRetrying(false);
    }
  }

  return (
    <div className="page run">
      <PageHeader
        back={{ href: "#/", label: "All investigations" }}
        eyebrow="Pipeline trace"
        title={`Run ${r.task_input.order_id}`}
        meta={<>
          <Badge value={r.status} large />
          <FaultBadge fault={r.fault_type} />
          <ModeBadge mode={r.llm_mode} model={r.model} />
          <Chip mono title="Seed of this run: the same task and seed give the same trace hash">seed {r.seed}</Chip>
          {r.trace_sha256 ? <span className="row tight small muted">trace <Hash value={r.trace_sha256} label="trace SHA-256" /></span> : null}
          <span className="small dim">{when(r.created_at)}{duration(r.created_at, r.finished_at) ? ` · ${duration(r.created_at, r.finished_at)}` : ""}</span>
        </>}
        actions={<span className="mono small dim">{r.id}</span>}
      />

      <Card title="Outcome" icon={MessageSquare}>
        <div className="run-outcome">
          <div className="run-exchange">
            <div><div className="eyebrow">Customer asked</div><p>{r.task_input.message}</p></div>
            <div><div className="eyebrow">Workflow replied</div>{reply ? <p className="run-reply">{reply}</p> : <p className="dim">No reply: the run did not finish.</p>}</div>
          </div>
          <div className="run-contrast">
            <div className="run-lane">
              <div className="eyebrow">Output monitoring sees</div>
              <ul className="checklist small">
                <Seen ok={completed}>Run status: {r.status}</Seen>
                <Seen ok={!r.error}>Error raised: {r.error ? "yes" : "none"}</Seen>
                <Seen ok={!!reply}>Reply produced: {reply ? "yes" : "no"}</Seen>
              </ul>
            </div>
            <div className="run-lane">
              <div className="eyebrow">Granite's checks see</div>
              {outcome.length === 0 || passedOutcome.length + failedOutcome.length === 0 ? <p className="small dim">Outcome checks could not be evaluated.</p> : (
                <ul className="checklist small">
                  <Seen ok={failedOutcome.length === 0}>Outcome checks: {passedOutcome.length} passed, {failedOutcome.length} failed</Seen>
                  {failedOutcome.map((c) => <li key={c.check_id} className="run-lane-fail"><span className="mono">{c.check_id}</span><span>observed <strong className="mono">{show(c.observed)}</strong>, expected <strong className="mono">{show(c.expected)}</strong></span></li>)}
                </ul>
              )}
            </div>
          </div>
        </div>
        {r.error ? (
          <div className="alert tone-bad run-verdict" role="alert">
            <ShieldAlert size={15} aria-hidden="true" />
            <div className="alert-body">
              <div className="alert-title">The run stopped early: {r.error}</div>
              <div className="row" style={{ marginTop: 8 }}>
                <button type="button" className="btn sm" onClick={retry} disabled={retrying}><RotateCcw size={13} aria-hidden="true" />{retrying ? "Running again…" : "Run again"}</button>
                <a className="btn sm ghost" href="#/new">Change the task</a>
              </div>
              {retryError ? <div className="field-error">{retryError}</div> : null}
            </div>
          </div>
        ) : completed && failedOutcome.length > 0 ? (
          <div className="run-verdict"><Notice tone="bad" icon={ShieldAlert} title="Silent failure"
            action={r.findings[0] ? <a className="btn primary sm" href={`#/findings/${r.findings[0].id}`}>Investigate</a> : undefined}>
            The run completed without an error, but {failedOutcome.length === 1 ? "an outcome check shows" : `${failedOutcome.length} outcome checks show`} the answer is wrong.
          </Notice></div>
        ) : completed && failedSteps.length > 0 ? (
          <div className="run-verdict"><Notice tone="warn" title="No finding">
            {failedSteps.length} step check{failedSteps.length === 1 ? "" : "s"} failed, but the outcome is correct, so no finding was opened.
          </Notice></div>
        ) : completed ? (
          <div className="run-verdict"><Notice tone="ok" title="No finding">Every check that could be evaluated passed.</Notice></div>
        ) : null}
      </Card>

      <Card title="Pipeline" icon={Waypoints} sub="select a step to inspect it"
            actions={r.injected_fault ? (
              <button type="button" className="btn sm" aria-pressed={reveal} onClick={() => setReveal(!reveal)} title="Ground truth of the injected fault. The analysis never reads it.">
                {reveal ? <EyeOff size={13} aria-hidden="true" /> : <Eye size={13} aria-hidden="true" />}{reveal ? "Hide injected fault" : "Reveal injected fault"}
              </button>
            ) : null}>
        {graph.loading && !graph.data ? <Skeleton lines={3} /> : graph.data && graph.data.nodes.length > 0 ? (
          <Graph graph={graph.data} onSelect={setSelected} selected={selected} marks={marks} path={path.length > 1 ? path : undefined} legend />
        ) : <p className="small dim">{graph.error ? "The graph could not be loaded; the steps are listed below." : "No step was recorded for this run."}</p>}
        {lead && path.length > 1 ? (
          <p className="small muted run-pathnote">
            <Search size={13} aria-hidden="true" /> Highlighted: the recorded data-flow path from <strong>{lead.agent}</strong> ({lead.status === "confirmed" ? "origin confirmed by replay" : lead.status === "refuted" ? "refuted by replay" : "first-ranked suspect"}) to the symptom.
          </p>
        ) : null}
        {steps.length > 0 ? (
          <div className="table-wrap run-steps">
            <table>
              <thead><tr><th>#</th><th>Step</th><th>Kind</th><th>Answer</th><th>Duration</th><th>Checks</th><th><span className="sr-only">Inspect</span></th></tr></thead>
              <tbody>
                {steps.map((s, i) => (
                  <tr key={s.step_id} aria-selected={selected === s.step_id || undefined}>
                    <td className="mono dim">{i + 1}</td>
                    <td><strong>{s.agent}</strong><div className="small dim mono">{s.step_id}{s.name ? ` · ${s.name}` : ""}</div></td>
                    <td>{stepKind(s.kind)}</td>
                    <td className="small">{produced(s)}</td>
                    <td className="mono small">{duration(s.started_at, s.ended_at) || "n/a"}</td>
                    <td><div className="row tight">
                      {s.error ? <Badge value="error" text="errored" /> : null}
                      {r.check_results.filter((c) => c.step === s.step_id).map((c) => <Badge key={c.check_id} value={c.status} text={`${c.check_id} ${c.status}`} />)}
                    </div></td>
                    <td><button type="button" className="btn ghost sm" onClick={() => setSelected(s.step_id)} aria-label={`Inspect ${s.agent}`}><Eye size={13} aria-hidden="true" />Inspect</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : null}
      </Card>

      {failed.length > 0 ? (
        <Card title="Observed vs source of truth" icon={Scale} sub="each failed check, in pipeline order">
          <ol className="run-chain">
            {failed.map((c, i) => (
              <li key={c.check_id}>
                <div className="run-chain-head">
                  <strong>{agent(c.step)}</strong><Chip mono>{c.check_id}</Chip><Chip tone={c.scope === "outcome" ? "bad" : "neutral"}>{c.scope} check</Chip>
                  <span className="small muted">compared with {comparedWith(c)}</span>
                </div>
                <Compare observed={c.observed} expected={c.expected} />
                {i < failed.length - 1 ? <div className="run-chain-arrow" aria-hidden="true"><ArrowDown size={14} /></div> : null}
              </li>
            ))}
          </ol>
        </Card>
      ) : null}

      <Card title="Checks" icon={ListChecks}
            sub={<span className="row tight">
              <Badge value="pass" text={`${count("pass")} passed`} /><Badge value="fail" text={`${count("fail")} failed`} tone={count("fail") ? "bad" : "neutral"} />
              {count("abstain") ? <Badge value="abstain" text={`${count("abstain")} abstained`} /> : null}{count("error") ? <Badge value="error" text={`${count("error")} errored`} /> : null}
            </span>}>
        <div className="table-wrap">
          <table className="run-checks">
            <thead><tr><th>Check</th><th>Scope</th><th>Step</th><th>Severity</th><th>Result</th></tr></thead>
            <tbody>
              {r.check_results.map((c) => (
                <tr key={c.check_id}>
                  <td>
                    <span className="mono">{c.check_id}</span>
                    <div className="small muted">{c.message}</div>
                    <details><summary className="small">How it was computed</summary><Computation c={c} /></details>
                  </td>
                  <td>{c.scope}</td>
                  <td>{agent(c.step)}</td>
                  <td>{c.severity}</td>
                  <td><Badge value={c.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <Card title="Findings" icon={Search}>
        {r.findings.length === 0
          ? <p className="muted">{completed ? "No outcome check failed." : "No findings."}</p>
          : <ul className="list-plain stack tight">{r.findings.map((f) => (
            <li key={f.id} className="run-finding">
              <div className="grow"><a href={`#/findings/${f.id}`}><strong>{f.title}</strong></a><div className="small dim mono">{f.id}</div></div>
              <Badge value={f.status} /><LevelBadge level={f.verification_level} />
              <a className="btn primary sm" href={`#/findings/${f.id}`} aria-label={`Open investigation ${f.id}`}>Open investigation</a>
            </li>
          ))}</ul>}
      </Card>

      {r.injected_fault && (
        <details className="card run-fault">
          <summary><Syringe size={14} aria-hidden="true" /> Injected fault (ground truth, hidden from the analysis, shown only to check it)</summary>
          <p>Step <strong>{agent(r.injected_fault.target_step)}</strong>, field <code>{r.injected_fault.field_path}</code>:
            {" "}<span className="mono">{String(r.injected_fault.original_value)}</span> became <span className="mono">{String(r.injected_fault.injected_value)}</span>. {r.injected_fault.note}</p>
        </details>
      )}

      <StepInspector steps={steps} checks={r.check_results} selected={selected} onSelect={setSelected} onClose={() => setSelected(null)} />
    </div>
  );
}
