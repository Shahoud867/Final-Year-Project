import {
  ArrowRight, Braces, CircleCheck, CircleX, Eye, EyeOff, ListChecks, MessageSquare, RotateCcw, Search, ShieldAlert, Syringe, Waypoints,
} from "lucide-react";
import { useState } from "react";
import type { ReactNode } from "react";
import { ApiError, api, waitForJob } from "../api";
import { Computation, comparedWith } from "../components/CheckDetail";
import { Graph } from "../components/Graph";
import { RunPlatforms } from "../components/Platforms";
import type { NodeMark } from "../components/Graph";
import { StepInspector, produced } from "../components/StepInspector";
import { Badge, Card, Chip, Compare, ErrorBox, FaultBadge, Hash, JsonView, Ladder, Loading, ModeBadge, Notice, PageHeader, Skeleton, TabPanel, Tabs } from "../components/ui";
import { leading, markOf, pathOf } from "../components/Verify";
import { duration, finalText, show, stepKind, when } from "../format";
import { useLoad } from "../hooks";
import type { CheckResult } from "../types";
import "../styles/pages/run.css";

/** Failures first, then outcome before step checks, then pipeline order. */
const byConcern = (order: (c: CheckResult) => number) => (a: CheckResult, b: CheckResult) =>
  Number(b.status === "fail") - Number(a.status === "fail") || order(a) - order(b);

/** One group of checks (outcome or step): what each compared, the result, and how it was computed on demand. */
function CheckGroup({ title, checks, agent }: { title: string; checks: CheckResult[]; agent: (step: string) => string }) {
  if (checks.length === 0) return null;
  return (
    <section className="stack tight" aria-label={title}>
      <h3 className="eyebrow">{title}</h3>
      <div className="table-wrap">
        <table className="run-checks">
          <thead><tr><th>Check</th><th>Step</th><th>Compared with</th><th>Observed and expected</th><th>Result</th></tr></thead>
          <tbody>
            {checks.map((c) => (
              <tr key={c.check_id}>
                <td>
                  <span className="mono">{c.check_id}</span>
                  <div className="small muted">{c.message}</div>
                  <details><summary className="small">How it was computed</summary><Computation c={c} /></details>
                </td>
                <td>{agent(c.step)}</td>
                <td className="small">{comparedWith(c)}</td>
                <td>{c.observed !== undefined && c.observed !== null || c.expected !== undefined && c.expected !== null
                  ? <Compare observed={c.observed} expected={c.expected} match={c.status === "pass"} /> : <span className="dim">n/a</span>}</td>
                <td><Badge value={c.status} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

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
  const caseFile = useLoad(() => (findingId ? api.finding(findingId) : Promise.resolve(null)), [findingId]);
  const [selected, setSelected] = useState<string | null>(null);
  const [tab, setTab] = useState("trace");
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
  const failedSteps = r.check_results.filter((c) => c.status === "fail" && c.scope === "step");
  const count = (status: string) => r.check_results.filter((c) => c.status === status).length;
  const finding = r.findings[0];
  const lead = caseFile.data ? leading(caseFile.data.hypotheses) : undefined;
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
        back={{ href: "#/runs", label: "Runs" }}
        eyebrow="Run"
        title={`Run ${r.task_input.order_id}`}
        meta={<>
          <Badge value={r.status} large />
          <FaultBadge fault={r.fault_type} />
          <ModeBadge mode={r.llm_mode} model={r.model} />
          <Chip mono title="Seed of this run: the same task and seed give the same trace hash">seed {r.seed}</Chip>
          {r.trace_sha256 ? <span className="row tight small muted">trace <Hash value={r.trace_sha256} label="trace SHA-256" /></span> : null}
          <span className="small dim">{when(r.created_at)}{duration(r.created_at, r.finished_at) ? ` · ${duration(r.created_at, r.finished_at)}` : ""}</span>
        </>}
        actions={finding ? (
          <span className="row run-case">
            <Ladder level={finding.verification_level} compact />
            <a className="btn sm" href={`#/findings/${finding.id}`} aria-label={`Open case ${finding.id}`}>Open case<ArrowRight size={13} aria-hidden="true" /></a>
          </span>
        ) : <span className="small dim">{completed ? "No finding: no outcome check failed." : "No finding."}</span>}
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

      <Card flush className="run-tabs">
        <div className="run-tabbar">
          <Tabs idBase="run" label="Run views" value={tab} onChange={setTab}
                tabs={[{ id: "trace", label: "Trace", icon: Waypoints, count: steps.length },
                       { id: "checks", label: "Checks", icon: ListChecks, count: `${count("fail")} failed` },
                       { id: "data", label: "Data", icon: Braces }]} />
          {r.injected_fault ? (
            <button type="button" className="btn sm" aria-pressed={reveal} onClick={() => setReveal(!reveal)} title="Ground truth of the injected fault. The analysis never reads it.">
              {reveal ? <EyeOff size={13} aria-hidden="true" /> : <Eye size={13} aria-hidden="true" />}{reveal ? "Hide injected fault" : "Reveal injected fault"}
            </button>
          ) : null}
        </div>

        <TabPanel idBase="run" id="trace" active={tab === "trace"} className="run-panel">
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
                <thead><tr><th>#</th><th>Step and its checks</th><th>Kind</th><th>Answer</th><th>Duration</th><th><span className="sr-only">Inspect</span></th></tr></thead>
                <tbody>
                  {steps.map((s, i) => {
                    const mine = r.check_results.filter((c) => c.step === s.step_id).sort(byConcern(order));
                    return (
                      <tr key={s.step_id} aria-selected={selected === s.step_id || undefined}>
                        <td className="mono dim">{i + 1}</td>
                        <td>
                          <strong>{s.agent}</strong><span className="small dim mono"> {s.step_id}{s.name ? ` · ${s.name}` : ""}</span>
                          <div className="row tight run-marks">
                            {s.error ? <Badge value="error" text="errored" /> : null}
                            {mine.map((c) => <Badge key={c.check_id} value={c.status} text={`${c.check_id} ${c.status}`} />)}
                            {!s.error && mine.length === 0 ? <span className="small dim">no check on this step</span> : null}
                          </div>
                        </td>
                        <td>{stepKind(s.kind)}</td>
                        <td className="small">{produced(s)}</td>
                        <td className="mono small">{duration(s.started_at, s.ended_at) || "n/a"}</td>
                        <td><button type="button" className="btn ghost sm" onClick={() => setSelected(s.step_id)} aria-label={`Inspect ${s.agent}`}><Eye size={13} aria-hidden="true" />Inspect</button></td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : null}
          <p className="small dim">Inspect a step to see what it received and produced, and each of its checks against what it was compared with.</p>
        </TabPanel>

        <TabPanel idBase="run" id="checks" active={tab === "checks"} className="run-panel">
          <div className="row tight">
            <Badge value="pass" text={`${count("pass")} passed`} /><Badge value="fail" text={`${count("fail")} failed`} tone={count("fail") ? "bad" : "neutral"} />
            {count("abstain") ? <Badge value="abstain" text={`${count("abstain")} abstained`} /> : null}{count("error") ? <Badge value="error" text={`${count("error")} errored`} /> : null}
          </div>
          {r.check_results.length === 0 ? <p className="small dim">No check was evaluated on this run.</p> : null}
          <CheckGroup title="Outcome checks" checks={r.check_results.filter((c) => c.scope === "outcome").sort(byConcern(order))} agent={agent} />
          <CheckGroup title="Step checks" checks={r.check_results.filter((c) => c.scope !== "outcome").sort(byConcern(order))} agent={agent} />
        </TabPanel>

        <TabPanel idBase="run" id="data" active={tab === "data"} className="run-panel">
          {r.trace ? <JsonView value={r.trace} label="Trace (Granite Trace v1)" maxHeight={560} /> : <p className="small dim">No trace was stored for this run.</p>}
        </TabPanel>
      </Card>

      <RunPlatforms runId={r.id} />

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
