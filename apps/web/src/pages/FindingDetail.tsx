import { useState } from "react";
import { ApiError, api } from "../api";
import { Experiments, ReviewPanel } from "../components/Outcome";
import { Badge, ErrorBox, Loading } from "../components/ui";
import { Verify } from "../components/Verify";
import { LEVELS, label, short } from "../format";
import { useLoad } from "../hooks";

const STAGES = ["Detected", "Traced", "Verified", "Reviewed"];

export function stage(status: string): number {
  if (["accepted", "rejected", "resolved", "wont_fix"].includes(status)) return 4;
  if (["confirmed", "refuted", "inconclusive", "evidence_supported"].includes(status)) return 3;
  if (["hypothesized", "verifying"].includes(status)) return 2;
  return 1;
}

export function FindingDetail({ id }: { id: string }) {
  const q = useLoad(() => api.finding(id), [id]);
  const [reportError, setReportError] = useState("");
  if (q.loading && !q.data) return <Loading />;
  if (q.error || !q.data) return <ErrorBox message={q.error || "Finding not found."} onRetry={q.reload} />;
  const f = q.data;
  const at = stage(f.status);

  async function download() {
    try {
      const text = await api.report(f.id);
      const url = URL.createObjectURL(new Blob([text], { type: "text/markdown" }));
      Object.assign(document.createElement("a"), { href: url, download: `${f.id}-report.md` }).click();
      URL.revokeObjectURL(url);
    } catch (e) { setReportError(e instanceof ApiError ? e.message : "Could not create the report."); }
  }

  return (
    <>
      <p className="small"><a href="#/">&larr; All investigations</a> · <a href={`#/runs/${f.run_id}`}>View the run</a></p>
      <div className="row between">
        <div><h1>{short(f.title, 110)}</h1><p className="muted mono">{f.id}</p></div>
        <div className="row"><Badge value={f.status} /><span className="badge" title={LEVELS[f.verification_level]}>{f.verification_level}</span></div>
      </div>
      <ol className="stepper" aria-label="Investigation progress">
        {STAGES.map((s, i) => <li key={s} className={i + 1 < at ? "done" : i + 1 === at ? "current" : ""}>{i + 1}. {s}</li>)}
      </ol>
      <div className="card">
        <p><strong>Why this was flagged:</strong> {f.detail}</p>
        <p className="small muted">{LEVELS[f.verification_level]}. Severity {f.severity}; check {f.check_id ?? "none"}; symptom appeared at step {f.symptom_step}.</p>
      </div>
      <Verify f={f} onDone={q.reload} />
      <Experiments f={f} />
      <ReviewPanel f={f} onDone={q.reload} />
      {f.reviews.length > 0 && (
        <section className="card"><h2>Review history</h2>
          {f.reviews.map((r) => <p key={r.id} className="small"><strong>{r.reviewer}</strong> chose <em>{r.decision}</em> (now {label(r.to_status)}). {r.comment}</p>)}
        </section>
      )}
      <section className="card" aria-labelledby="e-h">
        <div className="row between"><h2 id="e-h">Evidence</h2><button onClick={download}>Download report (.md)</button></div>
        <ErrorBox message={reportError} />
        <div className="table-wrap"><table>
          <thead><tr><th>Record</th><th>Type</th><th>SHA-256</th><th>Integrity</th></tr></thead>
          <tbody>{f.evidence.map((e) => (
            <tr key={e.id}>
              <td>{e.title}<details><summary className="small">Show content</summary><pre>{JSON.stringify(e.payload, null, 2)}</pre></details></td>
              <td className="small">{e.type.replace(/_/g, " ")}</td>
              <td className="mono small" title={e.sha256}>{e.sha256.slice(0, 12)}…</td>
              <td><Badge value={e.hash_valid ? "pass" : "fail"} text={e.hash_valid ? "hash matches" : "TAMPERED"} /></td>
            </tr>
          ))}</tbody>
        </table></div>
      </section>
    </>
  );
}
