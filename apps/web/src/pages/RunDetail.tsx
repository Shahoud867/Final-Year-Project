import { useState } from "react";
import { ApiError, api, waitForJob } from "../api";
import { Graph } from "../components/Graph";
import { Badge, ErrorBox, Loading } from "../components/ui";
import { label, short, when } from "../format";
import { useLoad } from "../hooks";

export function RunDetail({ id }: { id: string }) {
  const run = useLoad(() => api.run(id), [id]);
  const graph = useLoad(() => api.graph(id), [id]);
  const [selected, setSelected] = useState<string | null>(null);
  const [retrying, setRetrying] = useState(false);
  const [retryError, setRetryError] = useState("");

  if (run.loading && !run.data) return <Loading />;
  if (run.error || !run.data) return <ErrorBox message={run.error || "Run not found."} onRetry={run.reload} />;
  const r = run.data;
  const step = r.trace?.steps.find((s) => s.step_id === selected);

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
    <>
      <p className="small"><a href="#/">&larr; All investigations</a></p>
      <div className="row between">
        <div>
          <h1>Run {r.task_input.order_id}</h1>
          <p className="muted mono">{r.id}</p>
        </div>
        <div className="row">
          <Badge value={r.status} />
          <Badge value="info" text={r.fault_type ? `fault: ${label(r.fault_type)}` : "clean run"} />
          <Badge value="" text={`${r.llm_mode} · ${r.model}`} />
        </div>
      </div>
      <div className="card">
        <p><strong>Customer asked:</strong> {r.task_input.message}</p>
        {r.status === "completed" && r.trace && (
          <p><strong>Workflow replied:</strong> {String(Object.values(r.trace.run.final_output)[0] ?? "")}</p>
        )}
        {r.error && (
          <div className="alert bad" role="alert">
            The run stopped early: {r.error}
            <div className="row" style={{ marginTop: 8 }}>
              <button onClick={retry} disabled={retrying}>{retrying ? "Running again…" : "Run again"}</button>
              <a className="btn" href="#/new">Change the task</a>
            </div>
            {retryError && <div className="field-error">{retryError}</div>}
          </div>
        )}
        <p className="small muted">Started {when(r.created_at)} · seed {r.seed} · trace SHA-256 <span className="mono">{r.trace_sha256?.slice(0, 16)}…</span></p>
      </div>

      <section className="card" aria-labelledby="g-h">
        <h2 id="g-h">What happened, step by step</h2>
        {graph.data ? <Graph graph={graph.data} onSelect={setSelected} /> : <Loading />}
        <p className="small muted">Red steps failed a check. Select a step to see exactly what it received and produced.</p>
        {step && (
          <div className="grid cols-2">
            <div><h3>{step.agent} received</h3><pre>{JSON.stringify(step.inputs, null, 2)}</pre></div>
            <div><h3>{step.agent} produced</h3><pre>{JSON.stringify(step.outputs, null, 2)}</pre>
              {step.error && <div className="alert bad">{step.error}</div>}</div>
          </div>
        )}
      </section>

      <section className="card" aria-labelledby="f-h">
        <h2 id="f-h">Findings from this run</h2>
        {r.findings.length === 0
          ? <p className="muted">{r.status === "completed" ? "No outcome check failed." : "No findings."}</p>
          : r.findings.map((f) => (
            <div key={f.id} className="alert warn">
              <div className="row between">
                <a href={`#/findings/${f.id}`}><strong>{f.title}</strong></a>
                <Badge value={f.status} />
              </div>
              <div className="small">The outcome looked complete, but a check shows it is wrong. Open the finding to trace where it began.</div>
            </div>
          ))}
      </section>

      <section className="card" aria-labelledby="c-h">
        <h2 id="c-h">Checks</h2>
        <div className="table-wrap"><table>
          <thead><tr><th>Check</th><th>Step</th><th>Result</th><th>What was compared</th></tr></thead>
          <tbody>
            {r.check_results.map((c) => (
              <tr key={c.check_id}>
                <td><span className="mono">{c.check_id}</span><div className="small muted">{c.scope === "outcome" ? "outcome" : "step"} · {c.severity}</div></td>
                <td>{c.step}</td>
                <td><Badge value={c.status} /></td>
                <td className="small">{short(c.message || `${JSON.stringify(c.observed)} vs ${JSON.stringify(c.expected)}`, 140)}</td>
              </tr>
            ))}
          </tbody>
        </table></div>
      </section>

      {r.injected_fault && (
        <details className="card">
          <summary>Injected fault (ground truth, hidden from the analysis, shown only to check it)</summary>
          <p>Step <strong>{r.injected_fault.target_step}</strong>, field <code>{r.injected_fault.field_path}</code>:
            {" "}{String(r.injected_fault.original_value)} became {String(r.injected_fault.injected_value)}. {r.injected_fault.note}</p>
        </details>
      )}
    </>
  );
}
