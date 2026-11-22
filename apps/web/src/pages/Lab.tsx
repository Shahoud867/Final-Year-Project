import { FlaskConical, Play } from "lucide-react";
import { useState } from "react";
import { ApiError, api, waitForJob } from "../api";
import type { LlmMode } from "../api";
import { FAULT_INFO } from "../components/StudioPreview";
import { Badge, Card, Empty, ErrorBox, FaultBadge, Loading, PageHeader, Progress, Segmented } from "../components/ui";
import { faultLabel, when } from "../format";
import { useLoad } from "../hooks";
import type { Batch, Job } from "../types";
import "../styles/pages/lab.css";

const MAX_RUNS = 120;
const SECONDS_PER_RUN: Record<string, number> = { recorded: 1, live: 25 };

/** Counts for one batch: per condition, runs that finished, completed, errored, and how many opened a finding. */
function BatchResult({ b }: { b: Batch }) {
  const conditions = [...b.faults];
  return (
    <div className="table-wrap">
      <table>
        <caption className="sr-only">Batch {b.id}: results per condition</caption>
        <thead>
          <tr><th scope="col">Condition</th><th scope="col" className="num">Runs</th><th scope="col" className="num">Completed</th>
            <th scope="col" className="num">Errored</th><th scope="col" className="num">With a finding</th><th scope="col">Reads as</th></tr>
        </thead>
        <tbody>
          {conditions.map((c) => {
            const g = b.groups[c] ?? { runs: 0, finished: 0, completed: 0, errored: 0, with_finding: 0 };
            const clean = c === "none";
            return (
              <tr key={c}>
                <th scope="row">{clean ? "Clean (no fault)" : faultLabel(c)}</th>
                <td className="num">{g.runs}</td><td className="num">{g.completed}</td><td className="num">{g.errored}</td>
                <td className="num">{g.with_finding}</td>
                <td className="small muted">{g.completed === 0 ? "nothing completed yet"
                  : clean ? `${g.with_finding} of ${g.completed} clean runs flagged (each is a false alarm or a genuine model error)`
                    : `${g.with_finding} of ${g.completed} faulty runs detected`}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

/** Fault Lab: generate a batch of runs over chosen faults and tasks, then read detection per condition. */
export function Lab() {
  const wf = useLoad(() => api.workflows(), []);
  const ex = useLoad(() => api.examples("refund_desk"), []);
  const recent = useLoad(() => api.batches(), []);
  const [faults, setFaults] = useState<string[]>(["stale_price", "dropped_item", "handoff_drift", "none"]);
  const [tasks, setTasks] = useState<"all" | "delivered">("delivered");
  const [mode, setMode] = useState<LlmMode>("recorded");
  const [busy, setBusy] = useState(false);
  const [job, setJob] = useState<Job | null>(null);
  const [batch, setBatch] = useState<Batch | null>(null);
  const [error, setError] = useState("");

  const offered = wf.data?.[0]?.faults ?? [];
  const chosen = (ex.data ?? []).filter((t) => tasks === "all" || (t.label ?? "").includes("(delivered)"));
  const total = chosen.length * faults.length;
  const minutes = Math.ceil((total * (SECONDS_PER_RUN[mode] ?? 25)) / 60);
  const why = faults.length === 0 ? "Choose at least one condition." : total > MAX_RUNS ? `At most ${MAX_RUNS} runs per batch.` : "";

  const toggle = (f: string) => setFaults((fs) => (fs.includes(f) ? fs.filter((x) => x !== f) : [...fs, f]));

  async function generate() {
    setBusy(true); setError(""); setBatch(null); setJob(null);
    try {
      const { job_id, batch_id } = await api.createBatch({ faults, task_ids: chosen.map((t) => t.order_id), mode });
      await waitForJob(job_id, (j) => { setJob(j); void api.batch(batch_id).then(setBatch, () => undefined); }, 1200);
      setBatch(await api.batch(batch_id));
      recent.reload();
    } catch (e) { setError(e instanceof ApiError ? e.message : "Something went wrong."); }
    setBusy(false);
  }

  if (wf.loading && !wf.data) return <Loading />;
  return (
    <div className="page lab-page">
      <PageHeader title="Fault Lab" sub="Generate many runs at once: every chosen fault, and clean runs, on every chosen task." />
      <Card title="1. Conditions" icon={FlaskConical} sub="each fault is a silent failure: the run completes and raises no error">
        <fieldset className="lab-conditions" disabled={busy}>
          <legend className="sr-only">Faults to inject</legend>
          {offered.map((f) => (
            <label key={f} className={`lab-condition${faults.includes(f) ? " on" : ""}`}>
              <input type="checkbox" checked={faults.includes(f)} onChange={() => toggle(f)} />
              <span><strong>{faultLabel(f)}</strong> <span className="mono small dim">at {FAULT_INFO[f]?.target ?? "?"}</span>
                <span className="small muted">{FAULT_INFO[f]?.text ?? ""}</span></span>
            </label>
          ))}
          <label className={`lab-condition${faults.includes("none") ? " on" : ""}`}>
            <input type="checkbox" checked={faults.includes("none")} onChange={() => toggle("none")} />
            <span><strong>Clean runs</strong><span className="small muted">No fault: any finding here is a false alarm or a genuine model error.</span></span>
          </label>
        </fieldset>
      </Card>
      <Card title="2. Tasks and mode">
        <div className="row loose">
          <Segmented label="Tasks" name="tasks" value={tasks} onChange={setTasks}
                     options={[{ value: "delivered", label: "Delivered orders" }, { value: "all", label: "All examples" }]} />
          <Segmented label="Model answers" name="mode" value={mode} onChange={setMode}
                     options={[{ value: "recorded", label: "Recorded" }, { value: "live", label: "Live model" }]} />
        </div>
        <p className="small muted lab-plan-line" aria-live="polite">
          {chosen.length} tasks × {faults.length} conditions = <strong>{total} runs</strong>, about {minutes} min in {mode} mode.
          {mode === "recorded" ? " Recorded mode can only run answers that were saved; anything else ends as an error, and the batch carries on." : ""}
        </p>
        {why ? <p className="small t-bad">{why}</p> : null}
        <button type="button" className="btn primary" onClick={generate} disabled={busy || !!why || chosen.length === 0}>
          <Play size={14} aria-hidden="true" />{busy ? "Generating…" : "Generate"}
        </button>
        <ErrorBox message={error} />
        {busy ? (
          <div className="lab-progress" aria-live="polite">
            <div className="row between small"><span>{job?.message || "Starting…"}</span><span className="mono">{job ? `${job.progress_done}/${job.progress_total}` : ""}</span></div>
            <Progress done={job?.progress_done ?? 0} total={job?.progress_total ?? total} label="Runs finished" />
          </div>
        ) : null}
      </Card>
      {batch ? (
        <Card title="Result" sub={<>batch <span className="mono">{batch.id}</span>, {batch.llm_mode} mode</>}>
          <BatchResult b={batch} />
          <p className="small muted">Ground truth (which fault was injected) is used here only to score the batch. Detection and attribution never read it.</p>
        </Card>
      ) : null}
      <Card title="Recent batches" flush>
        {recent.loading && !recent.data ? <Loading /> : recent.error ? <ErrorBox message={recent.error} onRetry={recent.reload} />
          : !recent.data?.length ? <Empty title="No batches yet">Generate one above.</Empty> : (
            <div className="table-wrap">
              <table>
                <caption className="sr-only">Recent batches</caption>
                <thead><tr><th scope="col">Batch</th><th scope="col">Conditions</th><th scope="col" className="num">Runs</th><th scope="col">Status</th><th scope="col">Started</th></tr></thead>
                <tbody>
                  {recent.data.map((b) => (
                    <tr key={b.id}>
                      <td><button type="button" className="btn ghost sm mono" onClick={() => setBatch(b)}>{b.id}</button></td>
                      <td><span className="row tight">{b.faults.map((f) => f === "none" ? <span key={f} className="chip">clean</span> : <FaultBadge key={f} fault={f} />)}</span></td>
                      <td className="num">{b.runs.length}</td>
                      <td><Badge value={b.status} /></td>
                      <td className="small dim">{when(b.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
      </Card>
    </div>
  );
}
