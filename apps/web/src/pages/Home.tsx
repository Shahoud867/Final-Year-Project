import { useState } from "react";
import { PAGE, api } from "../api";
import type { FindingFilter } from "../api";
import { Filters } from "../components/Filters";
import { Badge, Empty, ErrorBox, Loading } from "../components/ui";
import { label, when } from "../format";
import { useLoad } from "../hooks";

export function Home() {
  const [filter, setFilter] = useState<FindingFilter>({});
  const [limit, setLimit] = useState(PAGE);
  const runs = useLoad(() => api.runs(), []);
  const findings = useLoad(() => api.findings({ ...filter, limit }), [filter, limit]);
  const filtered = Object.values(filter).some(Boolean);
  return (
    <>
      <div className="row between">
        <div>
          <h1>Investigations</h1>
          <p className="muted">Run a multi-agent workflow, find outcomes that look fine but are wrong, and trace them to their origin.</p>
        </div>
        <a className="btn primary" href="#/new">New run</a>
      </div>

      <section className="card" aria-labelledby="f-h">
        <h2 id="f-h">Findings</h2>
        <Filters value={filter} onApply={(next) => { setFilter(next); setLimit(PAGE); }} />
        <ErrorBox message={findings.error} onRetry={findings.reload} />
        {findings.loading && !findings.data ? <Loading /> : null}
        {findings.data && findings.data.length === 0 && !findings.error ? (
          <Empty>{filtered ? "No finding matches these filters." : "No findings yet. Start a run with a fault injected to see one."}</Empty>
        ) : null}
        {findings.data && findings.data.length > 0 ? (
          <div className="table-wrap"><table>
            <thead><tr><th>Finding</th><th>Status</th><th>Level</th><th>Severity</th><th>Opened</th></tr></thead>
            <tbody>
              {findings.data.map((f) => (
                <tr key={f.id} className="click" onClick={() => { window.location.hash = `#/findings/${f.id}`; }}>
                  <td><a href={`#/findings/${f.id}`}>{f.title}</a><div className="small muted mono">{f.id}</div></td>
                  <td><Badge value={f.status} /></td>
                  <td title={f.verification_level}>{f.verification_level}</td>
                  <td>{f.severity}</td>
                  <td className="small">{when(f.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table></div>
        ) : null}
        {findings.data && findings.data.length >= limit && (
          <div className="row" style={{ marginTop: 10 }}><button onClick={() => setLimit(limit + PAGE)}>Show more</button></div>
        )}
      </section>

      <section className="card" aria-labelledby="r-h">
        <h2 id="r-h">Recent runs</h2>
        <ErrorBox message={runs.error} onRetry={runs.reload} />
        {runs.loading && !runs.data ? <Loading /> : null}
        {runs.data && runs.data.length === 0 && !runs.error ? <Empty>No runs yet.</Empty> : null}
        {runs.data && runs.data.length > 0 ? (
          <div className="table-wrap"><table>
            <thead><tr><th>Run</th><th>Status</th><th>Fault</th><th>Checks failed</th><th>Mode</th><th>Started</th></tr></thead>
            <tbody>
              {runs.data.map((r) => (
                <tr key={r.id} className="click" onClick={() => { window.location.hash = `#/runs/${r.id}`; }}>
                  <td><a href={`#/runs/${r.id}`}>{r.task_input.order_id}</a><div className="small muted mono">{r.id}</div></td>
                  <td><Badge value={r.status} /></td>
                  <td>{r.fault_type ? label(r.fault_type) : "none"}</td>
                  <td>{r.failed_checks}</td>
                  <td>{r.llm_mode}</td>
                  <td className="small">{when(r.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table></div>
        ) : null}
      </section>
    </>
  );
}
