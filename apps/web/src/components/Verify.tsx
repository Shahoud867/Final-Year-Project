import { useState } from "react";
import { ApiError, api, waitForJob } from "../api";
import type { FindingDetail, Job } from "../types";
import { Badge, ErrorBox, Loading, Progress } from "./ui";

export function Verify({ f, onDone }: { f: FindingDetail; onDone: () => void }) {
  const [busy, setBusy] = useState("");
  const [job, setJob] = useState<Job | null>(null);
  const [error, setError] = useState("");
  const [n, setN] = useState(5);
  const [m, setM] = useState(2);
  const canVerify = f.allowed_actions.includes("verify");

  async function run(hypothesisId: string) {
    setBusy(hypothesisId); setError(""); setJob(null);
    try {
      const { job_id } = await api.verify(hypothesisId, n, m);
      await waitForJob(job_id, setJob);
    } catch (e) { setError(e instanceof ApiError ? e.message : "Something went wrong."); }
    setBusy(""); onDone();
  }

  return (
    <section className="card" aria-labelledby="h-h">
      <h2 id="h-h">Where did it begin?</h2>
      <p className="muted small">
        Candidates are ranked from the recorded data flow. Verifying replays the run from that step with the correct
        value in place ({n} times) and without it ({m} controls).
      </p>
      <div className="row" style={{ marginBottom: 8 }}>
        <label htmlFor="n" className="small">Replays with fix</label>
        <input id="n" type="number" min={1} max={10} value={n} onChange={(e) => setN(Number(e.target.value))} style={{ width: 70 }} />
        <label htmlFor="m" className="small">Controls</label>
        <input id="m" type="number" min={0} max={5} value={m} onChange={(e) => setM(Number(e.target.value))} style={{ width: 70 }} />
      </div>
      <ErrorBox message={error} />
      {busy && <><Loading text={job?.message || "Starting replays…"} /><Progress done={job?.progress_done ?? 0} total={job?.progress_total ?? 1} /></>}
      <div className="table-wrap"><table>
        <thead><tr><th>#</th><th>Step</th><th>Why</th><th>Status</th><th><span className="sr-only">Action</span></th></tr></thead>
        <tbody>
          {f.hypotheses.map((h) => (
            <tr key={h.id}>
              <td>{h.rank}</td>
              <td><strong>{h.agent}</strong><div className="small muted">{h.method} · {h.evidence_kind} · score {h.score.toFixed(2)}</div></td>
              <td className="small">{h.rationale}</td>
              <td><Badge value={h.status} /></td>
              <td>
                {h.can_verify
                  ? <button onClick={() => run(h.id)} disabled={!canVerify || !!busy}>Verify</button>
                  : <span className="small muted">no automatic replay</span>}
              </td>
            </tr>
          ))}
        </tbody>
      </table></div>
    </section>
  );
}
