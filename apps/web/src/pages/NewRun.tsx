import { useState } from "react";
import type { FormEvent } from "react";
import { ApiError, api, waitForJob } from "../api";
import { ErrorBox, Loading, Progress } from "../components/ui";
import { useLoad } from "../hooks";
import type { Job, TaskInput } from "../types";

const EMPTY: TaskInput = { message: "", email: "", order_id: "" };

export function NewRun() {
  const examples = useLoad(() => api.examples("refund_desk"), []);
  const [task, setTask] = useState<TaskInput>(EMPTY);
  const [fault, setFault] = useState("stale_price");
  const [mode, setMode] = useState("auto");
  const [busy, setBusy] = useState(false);
  const [job, setJob] = useState<Job | null>(null);
  const [error, setError] = useState("");
  const [fields, setFields] = useState<Record<string, string>>({});

  const set = (k: keyof TaskInput) => (e: { target: { value: string } }) => setTask({ ...task, [k]: e.target.value });

  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true); setError(""); setFields({}); setJob(null);
    try {
      const { run_id, job_id } = await api.createRun({ task_input: task, fault: fault === "none" ? null : fault, mode });
      await waitForJob(job_id, setJob);
      window.location.hash = `#/runs/${run_id}`;
    } catch (err) {
      if (err instanceof ApiError) {
        setError(Object.keys(err.fields).length ? "Please fix the highlighted fields." : err.message);
        setFields(err.fields);
      } else setError("Something went wrong.");
      setBusy(false);
    }
  }

  function loadExample(index: string) {
    const ex = examples.data?.[Number(index)];
    if (ex) setTask({ message: ex.message, email: ex.email, order_id: ex.order_id });
  }

  return (
    <>
      <h1>New run</h1>
      <p className="muted">Pick an example or type your own refund request. The fault simulates a stale price coming from the lookup tool.</p>
      <form className="card" onSubmit={submit} noValidate>
        <div className="field">
          <label htmlFor="example">Load an example</label>
          <select id="example" defaultValue="" disabled={busy || !examples.data} onChange={(e) => loadExample(e.target.value)}>
            <option value="" disabled>{examples.loading ? "Loading examples…" : "Choose…"}</option>
            {examples.data?.map((ex, i) => <option key={ex.order_id} value={i}>{ex.label}</option>)}
          </select>
          <ErrorBox message={examples.error} onRetry={examples.reload} />
        </div>
        <div className="field">
          <label htmlFor="message">Customer message</label>
          <textarea id="message" rows={3} value={task.message} onChange={set("message")} aria-invalid={!!fields.message} maxLength={2000} />
          {fields.message && <div className="field-error">{fields.message}</div>}
        </div>
        <div className="grid cols-2">
          <div className="field">
            <label htmlFor="email">Customer e-mail</label>
            <input id="email" type="email" value={task.email} onChange={set("email")} aria-invalid={!!fields.email} />
            {fields.email && <div className="field-error">{fields.email}</div>}
          </div>
          <div className="field">
            <label htmlFor="order">Order id</label>
            <input id="order" value={task.order_id} onChange={set("order_id")} placeholder="#W1234567" aria-invalid={!!fields.order_id} />
            {fields.order_id && <div className="field-error">{fields.order_id}</div>}
          </div>
        </div>
        <div className="grid cols-2">
          <div className="field">
            <label htmlFor="fault">Inject a fault</label>
            <select id="fault" value={fault} onChange={(e) => setFault(e.target.value)}>
              <option value="stale_price">Stale price from the lookup tool</option>
              <option value="none">No fault (clean run)</option>
            </select>
          </div>
          <div className="field">
            <label htmlFor="mode">Language model</label>
            <select id="mode" value={mode} onChange={(e) => setMode(e.target.value)}>
              <option value="auto">Automatic (live if available)</option>
              <option value="recorded">Recorded answers (examples only)</option>
              <option value="live">Live model</option>
            </select>
            <div className="hint">Recorded mode replays saved real model answers and works offline for the example tasks.</div>
          </div>
        </div>
        <ErrorBox message={error} />
        {busy && <><Loading text={job?.message || "Starting…"} /><Progress done={job?.progress_done ?? 0} total={job?.progress_total ?? 1} /></>}
        <div className="row" style={{ marginTop: 12 }}>
          <button className="primary" type="submit" disabled={busy}>{busy ? "Running…" : "Run workflow"}</button>
          <button type="button" disabled={busy} onClick={() => { setTask(EMPTY); setFields({}); setError(""); }}>Clear</button>
        </div>
      </form>
    </>
  );
}
