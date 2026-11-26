import { Download, PlugZap, Plus } from "lucide-react";
import { useState } from "react";
import { ApiError, api } from "../api";
import { Badge, Card, Chip, Empty, ErrorBox, Field, Loading, Notice, PageHeader, Segmented, describe } from "../components/ui";
import { when } from "../format";
import { useLoad } from "../hooks";
import type { Connection, ImportResult } from "../types";
import "../styles/pages/lab.css";

const PLATFORM = { phoenix: "Arize Phoenix", langfuse: "Langfuse" } as const;
const DEFAULT_URL = { phoenix: "http://localhost:6006", langfuse: "https://cloud.langfuse.com" } as const;
const TIER_TEXT: Record<string, string> = {
  declared: "reads declared by the application",
  value: "reads inferred from values passed between steps",
  order: "reads assumed from step order (weakest)",
};

const message = (e: unknown) => (e instanceof ApiError ? e.message : "Something went wrong.");

/** What one import brought in and what it skipped, with the reason for each skip. */
function ImportSummary({ r }: { r: ImportResult }) {
  return (
    <div className="stack" aria-live="polite">
      <p className="small">
        Looked at <strong>{r.fetched}</strong> trace{r.fetched === 1 ? "" : "s"}: imported <strong>{r.imported.length}</strong>,
        skipped {r.skipped.length}.
      </p>
      {r.imported.length ? (
        <div className="table-wrap">
          <table>
            <caption className="sr-only">Imported traces</caption>
            <thead><tr><th scope="col">Trace</th><th scope="col">Run</th><th scope="col" className="num">Findings</th><th scope="col">Lineage</th></tr></thead>
            <tbody>
              {r.imported.map((i) => (
                <tr key={i.trace_id}>
                  <td className="mono small">{i.trace_id.slice(0, 16)}…</td>
                  <td><a className="mono" href={`#/runs/${i.run_id}`}>{i.run_id}</a></td>
                  <td className="num">{i.findings}</td>
                  <td>{i.lineage.map((t) => <span key={t} className="chip" title={TIER_TEXT[t]}>{t}</span>)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
      {r.skipped.length ? (
        <ul className="small muted">
          {r.skipped.map((s) => <li key={s.trace_id}><span className="mono">{s.trace_id.slice(0, 16)}…</span> {s.reason}</li>)}
        </ul>
      ) : null}
    </div>
  );
}

/** One connection: its status, a reachability test and an import button. */
function ConnectionRow({ c, onChange }: { c: Connection; onChange: () => void }) {
  const [busy, setBusy] = useState("");
  const [result, setResult] = useState<ImportResult | null>(null);
  const [test, setTest] = useState<{ ok: boolean; text: string } | null>(null);
  const [error, setError] = useState("");

  async function check() {
    setBusy("test"); setError(""); setTest(null);
    try {
      const r = await api.testConnection(c.id);
      setTest({ ok: r.ok, text: r.ok ? String(r.detail.note ?? "Reachable; the keys work.") : String(r.detail.error ?? "Not reachable.") });
    } catch (e) { setError(message(e)); }
    setBusy("");
  }

  async function pull() {
    setBusy("import"); setError(""); setResult(null);
    try { setResult(await api.importTraces(c.id)); onChange(); } catch (e) { setError(message(e)); }
    setBusy("");
  }

  return (
    <Card title={c.name} icon={PlugZap}
          sub={<>{PLATFORM[c.kind]} · <span className="mono">{c.base_url}</span>{c.project ? <> · project <span className="mono">{c.project}</span></> : null}</>}
          actions={<span className="row tight">
            <button type="button" className="btn sm" onClick={check} disabled={!!busy}>{busy === "test" ? "Testing…" : "Test"}</button>
            <button type="button" className="btn primary sm" onClick={pull} disabled={!!busy || !c.keys_configured}>
              <Download size={13} aria-hidden="true" />{busy === "import" ? "Importing…" : "Import traces"}
            </button>
          </span>}>
      <div className="row loose small">
        <span>Checks of <strong>{c.workflow_key}</strong> apply</span>
        <span>{c.imported_runs} imported · {c.exported_runs} sent</span>
        <span className="dim">{c.last_sync_at ? `last import ${when(c.last_sync_at)}` : "never imported"}</span>
        {!c.keys_configured ? <Badge value="error" text="keys missing" title="Set GRANITE_LANGFUSE_PUBLIC_KEY and GRANITE_LANGFUSE_SECRET_KEY on the server" /> : null}
      </div>
      {test ? <Notice tone={test.ok ? "ok" : "bad"} title={test.ok ? "Connected" : "Not connected"}>{test.text}</Notice> : null}
      <ErrorBox message={error} />
      {result ? <ImportSummary r={result} /> : null}
    </Card>
  );
}

/** Add a Phoenix or Langfuse project. Only the URL and names are sent; keys are read from the server environment. */
function AddConnection({ onAdded }: { onAdded: () => void }) {
  const [kind, setKind] = useState<"phoenix" | "langfuse">("phoenix");
  const [name, setName] = useState("Local Phoenix");
  const [url, setUrl] = useState<string>(DEFAULT_URL.phoenix);
  const [project, setProject] = useState("granite-demo");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  function choose(k: "phoenix" | "langfuse") {
    setKind(k); setUrl(DEFAULT_URL[k]); setName(k === "phoenix" ? "Local Phoenix" : "Langfuse Cloud");
    setProject(k === "phoenix" ? "granite-demo" : "");
  }

  async function add(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true); setError("");
    try { await api.createConnection({ kind, name, base_url: url, project }); onAdded(); } catch (err) { setError(message(err)); }
    setBusy(false);
  }

  return (
    <Card title="Add a connection" icon={Plus} sub="traces come in, verdicts go back">
      <form className="stack" onSubmit={add}>
        <Segmented label="Platform" name="kind" value={kind} onChange={choose}
                   options={[{ value: "phoenix", label: PLATFORM.phoenix }, { value: "langfuse", label: PLATFORM.langfuse }]} />
        <div className="row loose">
          <Field id="con-name" label="Name" required><input id="con-name" value={name} onChange={(e) => setName(e.target.value)} maxLength={120} required /></Field>
          <Field id="con-url" label="Server URL" required><input id="con-url" value={url} onChange={(e) => setUrl(e.target.value)} maxLength={300} required /></Field>
          <Field id="con-project" label={kind === "phoenix" ? "Project" : "Trace name (optional)"} required={kind === "phoenix"}
                 hint={kind === "phoenix" ? "created on first send if it does not exist" : "import only traces with this name"}>
            <input id="con-project" value={project} onChange={(e) => setProject(e.target.value)} maxLength={120}
                   required={kind === "phoenix"} {...describe("con-project", { hint: true })} />
          </Field>
        </div>
        <p className="small muted">
          {kind === "phoenix"
            ? "If your Phoenix server has authentication on, set GRANITE_PHOENIX_API_KEY where the Granite server runs."
            : "Set GRANITE_LANGFUSE_PUBLIC_KEY and GRANITE_LANGFUSE_SECRET_KEY where the Granite server runs. Keys are never stored in Granite's database."}
        </p>
        <div><button type="submit" className="btn primary" disabled={busy}>{busy ? "Adding…" : "Add connection"}</button></div>
        <ErrorBox message={error} />
      </form>
    </Card>
  );
}

/** Connections: bring traces in from Phoenix or Langfuse, send runs there, and write verdicts back (F13). */
export function Connections() {
  const list = useLoad(() => api.connections(), []);
  return (
    <div className="page lab-page">
      <PageHeader title="Connections" sub="Investigate traces your team already sends to Arize Phoenix or Langfuse, and send Granite's verdicts back there." />
      <Notice tone="neutral" title="What an imported trace can reach">
        Checks, findings and ranked suspects work on every imported trace. Replay verification needs a workflow Granite can run,
        so traces are matched to the <Chip mono>refund_desk</Chip> workflow; a trace whose steps do not match is skipped with the reason.
      </Notice>
      {list.loading && !list.data ? <Loading /> : list.error ? <ErrorBox message={list.error} onRetry={list.reload} />
        : !list.data?.length ? <Empty title="No connections yet">Add Phoenix or Langfuse below. On a run page, “Send to” puts that run into the platform.</Empty>
          : list.data.map((c) => <ConnectionRow key={c.id} c={c} onChange={list.reload} />)}
      <AddConnection onAdded={list.reload} />
    </div>
  );
}
