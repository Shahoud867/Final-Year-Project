import { Braces, CassetteTape, CircleSlash, Cpu, EyeOff, FormInput, Play, ShieldCheck, Shuffle, Syringe } from "lucide-react";
import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { ApiError, api, waitForJob } from "../api";
import type { LlmMode } from "../api";
import { FAULT_INFO, StudioPreview } from "../components/StudioPreview";
import { Card, ErrorBox, Field, Notice, PageHeader, Progress, Segmented, describe } from "../components/ui";
import type { Icon } from "../components/ui";
import { faultLabel, modeLabel } from "../format";
import { useLoad } from "../hooks";
import type { Example, Job, TaskInput } from "../types";
import "../styles/pages/studio.css";

const EMPTY: TaskInput = { message: "", email: "", order_id: "" };
const EMAIL = /^[^@\s]{1,64}@[^@\s]{1,120}\.[^@\s]{2,24}$/;
const ORDER = /^#W\d{3,12}$/;
const SEED_MAX = 2_000_000;
const KEYS = ["workflow", "task_input", "fault", "seed", "mode"];
const MODES: LlmMode[] = ["recorded", "live", "auto"];

/** The server's rules for a task, with the server's own wording, so a mistake is caught before the request is sent. */
export function validateTask(t: TaskInput): Partial<Record<keyof TaskInput, string>> {
  const out: Partial<Record<keyof TaskInput, string>> = {};
  if (t.message.length < 3) out.message = "Enter at least 3 characters";
  else if (t.message.length > 2000) out.message = "Enter at most 2000 characters";
  if (t.email.length > 190 || !EMAIL.test(t.email)) out.email = "Must look like name@example.com";
  if (!ORDER.test(t.order_id)) out.order_id = "Must look like #W1234567";
  return out;
}

type ScenarioId = "silent" | "clean" | "cancelled";
interface Scenario { id: ScenarioId; title: string; icon: Icon; does: string; expect: string; status: "delivered" | "cancelled"; fault: string }
const SCENARIOS: Scenario[] = [
  { id: "silent", title: "Silent price discrepancy", icon: EyeOff, status: "delivered", fault: "stale_price",
    does: "The lookup tool reports one price too low. Nothing crashes.", expect: "an outcome check fails, one finding opens" },
  { id: "clean", title: "Clean baseline", icon: ShieldCheck, status: "delivered", fault: "none",
    does: "The same request with no fault: the control for false alarms.", expect: "every check passes, no finding" },
  { id: "cancelled", title: "Cancelled-order edge case", icon: CircleSlash, status: "cancelled", fault: "stale_price",
    does: "The refund is refused either way, so the wrong price never reaches the customer.", expect: "one step check fails, outcome correct, no finding" },
];
const exampleFor = (examples: Example[] | null, status: string) => examples?.find((e) => e.label.includes(`(${status})`));
const without = (errors: Record<string, string>, key: string): Record<string, string> =>
  Object.fromEntries(Object.entries(errors).filter(([k]) => k !== key));

const MODE_INFO: Record<LlmMode, { icon: Icon; does: string }> = {
  recorded: { icon: CassetteTape, does: "Replays saved real model answers. Deterministic; works for the example tasks only." },
  live: { icon: Cpu, does: "Calls the configured local model. Any task; answers can vary between runs." },
  auto: { icon: Shuffle, does: "Live when a model is reachable, otherwise the recorded cassette." },
};

/** Recovery guidance for an error that is not about a field. */
function guidance(e: ApiError): string {
  if (e.status === 0) return "Start the Granite server, then run again.";
  if (e.status === 429) return "Too many requests in a minute. Wait a moment, then run again.";
  if (/never recorded/i.test(e.message)) return "Recorded mode only replays the example tasks. Load an example, or choose Live model.";
  if (e.status === 401) return "Enter the access token in the top bar.";
  return "";
}

export function NewRun() {
  const examples = useLoad(() => api.examples("refund_desk"), []);
  const workflows = useLoad(() => api.workflows(), []);
  const health = useLoad(() => api.health(), []);
  const [task, setTask] = useState<TaskInput>(EMPTY);
  const [fault, setFault] = useState("stale_price");
  const [mode, setMode] = useState<LlmMode>("auto");
  const [seed, setSeed] = useState(1);
  const [scenario, setScenario] = useState<ScenarioId | "custom">("custom");
  const [view, setView] = useState<"form" | "json">("form");
  const [jsonText, setJsonText] = useState("");
  const [jsonError, setJsonError] = useState("");
  const [busy, setBusy] = useState(false);
  const [job, setJob] = useState<Job | null>(null);
  const [elapsed, setElapsed] = useState(0);
  const [error, setError] = useState("");
  const [hint, setHint] = useState("");
  const [fields, setFields] = useState<Record<string, string>>({});

  useEffect(() => {
    if (!busy) return;
    const t0 = Date.now();
    const timer = setInterval(() => setElapsed(Math.round((Date.now() - t0) / 1000)), 500);
    return () => clearInterval(timer);
  }, [busy]);

  const workflow = workflows.data?.find((w) => w.key === "refund_desk") ?? workflows.data?.[0] ?? null;
  const faults = workflow?.faults ?? (fault !== "none" ? [fault] : []);
  const seedOk = Number.isInteger(seed) && seed >= 0 && seed <= SEED_MAX;
  const body = { workflow: "refund_desk", task_input: task, fault: fault === "none" ? null : fault, seed, mode };
  const liveDown = mode === "live" && health.data ? !health.data.live_model_reachable : false;

  const edit = (k: keyof TaskInput) => (e: { target: { value: string } }) => {
    setTask({ ...task, [k]: e.target.value }); setScenario("custom");
    if (fields[k]) setFields((f) => without(f, k));
  };
  const blur = (k: keyof TaskInput) => () => {
    const problem = validateTask(task)[k];
    setFields((f) => (problem && task[k] ? { ...f, [k]: problem } : without(f, k)));
  };

  function choose(s: Scenario) {
    const ex = exampleFor(examples.data, s.status);
    if (!ex) return;
    setTask({ message: ex.message, email: ex.email, order_id: ex.order_id });
    setFault(s.fault); setScenario(s.id); setFields({}); setError(""); setHint("");
  }

  function loadExample(index: string) {
    const ex = examples.data?.[Number(index)];
    if (!ex) return;
    setTask({ message: ex.message, email: ex.email, order_id: ex.order_id }); setScenario("custom"); setFields({});
  }

  function switchView(next: "form" | "json") {
    if (next === "json") { setJsonText(JSON.stringify(body, null, 2)); setJsonError(""); }
    setView(next);
  }

  /** Parse an edited request body; accept it only if it has the shape the server accepts. */
  function editJson(text: string) {
    setJsonText(text); setScenario("custom");
    let parsed: unknown;
    try { parsed = JSON.parse(text); } catch (e) { setJsonError(`Not valid JSON: ${e instanceof Error ? e.message : "cannot be parsed"}`); return; }
    if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) { setJsonError("The body must be a JSON object."); return; }
    const o = parsed as Record<string, unknown>;
    const unknown = Object.keys(o).find((k) => !KEYS.includes(k));
    if (unknown) { setJsonError(`Unknown key "${unknown}". The server accepts only: ${KEYS.join(", ")}.`); return; }
    const t = o.task_input as Record<string, unknown> | undefined;
    if (typeof t !== "object" || t === null || Array.isArray(t)) { setJsonError('"task_input" must be an object with message, email and order_id.'); return; }
    const extra = Object.keys(t).find((k) => !(k in EMPTY));
    if (extra) { setJsonError(`Unknown key "task_input.${extra}". A task has only: message, email, order_id.`); return; }
    if (o.mode !== undefined && o.mode !== null && !MODES.includes(o.mode as LlmMode)) { setJsonError('"mode" must be "recorded", "live" or "auto".'); return; }
    if (o.fault !== undefined && o.fault !== null && typeof o.fault !== "string") { setJsonError('"fault" must be a fault name or null.'); return; }
    if (o.seed !== undefined && typeof o.seed !== "number") { setJsonError('"seed" must be a number.'); return; }
    setJsonError("");
    setTask({ message: String(t.message ?? ""), email: String(t.email ?? ""), order_id: String(t.order_id ?? "") });
    setFault(typeof o.fault === "string" ? o.fault : "none");
    if (typeof o.seed === "number") setSeed(o.seed);
    if (typeof o.mode === "string") setMode(o.mode as LlmMode);
  }

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (view === "json" && jsonError) return;
    const problems: Record<string, string> = { ...validateTask(task) };
    if (!seedOk) problems.seed = `Use a whole number from 0 to ${SEED_MAX.toLocaleString("en-US")}`;
    setHint("");
    if (Object.keys(problems).length) {
      setFields(problems); setError("Please fix the highlighted fields.");
      if (view === "form") document.getElementById(["message", "email", "order", "seed"].find((id) => problems[id === "order" ? "order_id" : id]) ?? "")?.focus();
      return;
    }
    setBusy(true); setError(""); setFields({}); setJob(null); setElapsed(0);
    try {
      const { run_id, job_id } = await api.createRun({ task_input: task, fault: fault === "none" ? null : fault, mode, seed });
      await waitForJob(job_id, setJob);
      window.location.hash = `#/runs/${run_id}`;
    } catch (err) {
      if (err instanceof ApiError) {
        const byField = Object.keys(err.fields).length > 0;
        setError(byField ? "Please fix the highlighted fields." : err.message);
        setHint(byField ? "" : guidance(err));
        setFields(err.fields);
      } else setError("Something went wrong.");
      setBusy(false);
    }
  }

  function clear() {
    setTask(EMPTY); setFields({}); setError(""); setHint(""); setScenario("custom"); setSeed(1);
    if (view === "json") { setJsonText(JSON.stringify({ ...body, task_input: EMPTY, seed: 1 }, null, 2)); setJsonError(""); }
  }

  const fieldsInJson = view === "json" ? Object.entries(fields) : [];
  return (
    <div className="page studio">
      <PageHeader eyebrow="Task studio" title="New run"
                  sub="Launch the Refund Desk on one customer request, with or without an injected fault, and see what Granite finds." />
      <div className="studio-cols">
        <form className="studio-form" onSubmit={submit} noValidate>
          <Card title="1. Scenario" sub="expected results were verified in recorded mode">
            <div className="studio-scns" role="radiogroup" aria-label="Scenario">
              {SCENARIOS.map((s) => {
                const ex = exampleFor(examples.data, s.status);
                return (
                  <label key={s.id} className={`studio-opt${scenario === s.id ? " on" : ""}${ex ? "" : " off"}`}>
                    <input type="radio" name="scenario" value={s.id} checked={scenario === s.id} disabled={!ex || busy} onChange={() => choose(s)} />
                    <span className="studio-opt-title"><s.icon size={15} aria-hidden="true" />{s.title}</span>
                    <span className="small muted">{s.does}</span>
                    <span className="small studio-expect">{ex ? <>Expect: {s.expect}</> : examples.loading ? "Loading examples…" : `No ${s.status} example is available`}</span>
                  </label>
                );
              })}
            </div>
            <ErrorBox message={examples.error} onRetry={examples.reload} />
            {scenario === "custom" && (task.message || task.email || task.order_id) ? <p className="small muted">Custom task: the fields below were edited by hand.</p> : null}
          </Card>

          <Card title="2. Task input" actions={
            <Segmented name="view" label="Edit as" value={view} onChange={switchView}
                       options={[{ value: "form", label: "Form", icon: FormInput }, { value: "json", label: "JSON", icon: Braces }]} />}>
            {view === "form" ? (
              <>
                <Field id="example" label="Load an example" hint="Recorded mode can run exactly these tasks.">
                  <select id="example" defaultValue="" disabled={busy || !examples.data} onChange={(e) => loadExample(e.target.value)} aria-describedby="example-hint">
                    <option value="" disabled>{examples.loading ? "Loading examples…" : "Choose…"}</option>
                    {examples.data?.map((ex, i) => <option key={ex.order_id} value={i}>{ex.label}</option>)}
                  </select>
                </Field>
                <Field id="message" label="Customer message" required error={fields.message} hint={`${task.message.length}/2000 characters, at least 3`}>
                  <textarea id="message" rows={3} value={task.message} onChange={edit("message")} onBlur={blur("message")} maxLength={2000} required
                            {...describe("message", { hint: true, error: fields.message })} />
                </Field>
                <div className="studio-two">
                  <Field id="email" label="Customer e-mail" required error={fields.email} hint="name@example.com">
                    <input id="email" type="email" value={task.email} onChange={edit("email")} onBlur={blur("email")} maxLength={190} autoComplete="off" required
                           {...describe("email", { hint: true, error: fields.email })} />
                  </Field>
                  <Field id="order" label="Order id" required error={fields.order_id} hint="#W and digits">
                    <input id="order" className="mono" value={task.order_id} onChange={edit("order_id")} onBlur={blur("order_id")} placeholder="#W1234567" autoComplete="off" required
                           {...describe("order", { hint: true, error: fields.order_id })} />
                  </Field>
                </div>
              </>
            ) : (
              <Field id="body" label="Request body (JSON)" error={jsonError} hint="Exactly what is sent to POST /api/runs. Unknown keys are refused.">
                <textarea id="body" className="mono studio-json" rows={12} spellCheck={false} value={jsonText} onChange={(e) => editJson(e.target.value)}
                          {...describe("body", { hint: true, error: jsonError })} />
                {fieldsInJson.map(([k, v]) => <div key={k} className="field-error"><span className="mono">{k}</span>: {v}</div>)}
              </Field>
            )}
          </Card>

          <Card title="3. Fault and execution">
            <div className="studio-two">
              <Field id="fault" label="Inject a fault" hint={fault === "none" ? "A clean run: the baseline that must raise no finding." : FAULT_INFO[fault]?.text ?? "No description is available for this fault."}>
                <select id="fault" value={fault} disabled={busy} onChange={(e) => { setFault(e.target.value); setScenario("custom"); }} aria-describedby="fault-hint">
                  {faults.map((f) => <option key={f} value={f}>{faultLabel(f)}</option>)}
                  <option value="none">No fault (clean run)</option>
                </select>
              </Field>
              <Field id="seed" label="Seed" error={fields.seed} hint="Same task and seed give the same trace hash.">
                <input id="seed" type="number" className="mono" min={0} max={SEED_MAX} step={1} value={Number.isNaN(seed) ? "" : seed} disabled={busy}
                       onChange={(e) => setSeed(e.target.valueAsNumber)} {...describe("seed", { hint: true, error: fields.seed })} />
              </Field>
            </div>
            {fault !== "none" ? <p className="small muted studio-truth"><Syringe size={13} aria-hidden="true" />An injected fault is a test condition. Its ground truth is stored apart and never read by the analysis.</p> : null}

            <div className="studio-modes" role="radiogroup" aria-label="Execution mode">
              {MODES.map((m) => {
                const I = MODE_INFO[m].icon;
                return (
                  <label key={m} className={`studio-opt${mode === m ? " on" : ""}`}>
                    <input type="radio" name="mode" value={m} checked={mode === m} disabled={busy} onChange={() => setMode(m)} />
                    <span className="studio-opt-title"><I size={15} aria-hidden="true" />{modeLabel(m)}</span>
                    <span className="small muted">{MODE_INFO[m].does}</span>
                  </label>
                );
              })}
            </div>
            <p className="small muted" role="status">
              {health.data ? <>Server default: <strong>{modeLabel(health.data.llm_mode)}</strong>. Live model {health.data.live_model_reachable ? "reachable now" : "not reachable now"}.</>
                : health.error ? "The server did not report its model mode." : "Asking the server for its model mode…"}
            </p>
            {liveDown ? <Notice tone="warn" title="No live model is reachable">The run will end as errored. Start the local model, or choose Recorded cassette.</Notice> : null}
          </Card>

          {error ? (
            <div className="alert tone-bad" role="alert"><div className="alert-body"><div className="alert-title">{error}</div>{hint ? <div className="small">{hint}</div> : null}</div></div>
          ) : null}
          {busy ? (
            <div className="studio-live card" aria-live="polite">
              <div className="row between small"><span>{job?.message || "Starting…"}</span><span className="mono">{elapsed} s</span></div>
              <Progress done={job?.progress_done ?? 0} total={job && job.progress_total > 1 ? job.progress_total : 0} label="Run in progress" />
            </div>
          ) : null}
          <div className="row studio-actions">
            <button className="btn primary" type="submit" disabled={busy || (view === "json" && !!jsonError)}><Play size={14} aria-hidden="true" />{busy ? "Running…" : "Run workflow"}</button>
            <button className="btn" type="button" disabled={busy} onClick={clear}>Clear</button>
            <span className="small dim">Opens the pipeline trace when the run finishes.</span>
          </div>
        </form>

        <StudioPreview workflow={workflow} loading={workflows.loading} fault={fault} running={busy} />
      </div>
    </div>
  );
}
