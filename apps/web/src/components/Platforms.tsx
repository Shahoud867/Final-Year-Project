import { Send, Share2 } from "lucide-react";
import { useState } from "react";
import { ApiError, api } from "../api";
import { useLoad } from "../hooks";
import type { WriteBackResult } from "../types";
import { Card, Chip } from "./ui";
import "../styles/pages/lab.css";

const PLATFORM: Record<string, string> = { phoenix: "Phoenix", langfuse: "Langfuse" };
const message = (e: unknown) => (e instanceof ApiError ? e.message : "Something went wrong.");

/** Where this run lives on connected platforms, and a control to send it to one (F13). Hidden with no connections. */
export function RunPlatforms({ runId }: { runId: string }) {
  const cons = useLoad(() => api.connections(), []);
  const links = useLoad(() => api.runLinks(runId), [runId]);
  const [target, setTarget] = useState("");
  const [busy, setBusy] = useState(false);
  const [note, setNote] = useState("");
  const [error, setError] = useState("");
  const all = cons.data ?? [];
  if (!all.length && !links.data?.length) return null;
  const chosen = target || all[0]?.id || "";
  const name = (id: string) => all.find((c) => c.id === id);

  async function send() {
    setBusy(true); setError(""); setNote("");
    try {
      const r = await api.exportRun(runId, chosen);
      setNote(r.spans_sent ? `Sent ${r.spans_sent} spans (trace ${r.trace_id.slice(0, 12)}…).` : "Already there; nothing new to send.");
      links.reload();
    } catch (e) { setError(message(e)); }
    setBusy(false);
  }

  return (
    <Card title="Observability platforms" icon={Share2} sub="this run as a trace in Phoenix or Langfuse">
      {links.data?.length ? (
        <ul className="small stack">
          {links.data.map((l) => {
            const c = name(l.connection_id);
            const tiers = [...new Set(l.lineage.map((e) => e.tier))];
            return (
              <li key={`${l.connection_id}-${l.direction}`} className="row tight">
                <Chip>{l.direction === "imported" ? "imported from" : "sent to"} {c ? `${PLATFORM[c.kind]} · ${c.name}` : l.connection_id}</Chip>
                <span className="mono dim">trace {l.external_trace_id.slice(0, 16)}…</span>
                {tiers.length ? <span className="dim">lineage: {tiers.join(", ")}</span> : null}
              </li>
            );
          })}
        </ul>
      ) : <p className="small dim">Not on any platform yet.</p>}
      {all.length ? (
        <div className="row tight platform-send">
          <label className="sr-only" htmlFor={`send-${runId}`}>Connection</label>
          <select id={`send-${runId}`} value={chosen} onChange={(e) => setTarget(e.target.value)} disabled={busy}>
            {all.map((c) => <option key={c.id} value={c.id}>{PLATFORM[c.kind]} · {c.name}</option>)}
          </select>
          <button type="button" className="btn sm" onClick={send} disabled={busy || !chosen}>
            <Send size={13} aria-hidden="true" />{busy ? "Sending…" : "Send to"}
          </button>
          {note ? <span className="small t-ok" role="status">{note}</span> : null}
          {error ? <span className="small t-bad" role="alert">{error}</span> : null}
        </div>
      ) : null}
    </Card>
  );
}

/** Write the finding's current verdict to the platforms its run is linked to; hidden when there are none. */
export function SendVerdict({ findingId, runId }: { findingId: string; runId: string }) {
  const links = useLoad(() => api.runLinks(runId), [runId]);
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState<WriteBackResult | null>(null);
  const [error, setError] = useState("");
  if (!links.data?.length) return null;
  return (
    <span className="row tight">
      <button type="button" className="btn sm" disabled={busy}
              title="Annotate the origin step's span in Phoenix, or score it in Langfuse, with this finding's verdict"
              onClick={async () => {
                setBusy(true); setError(""); setDone(null);
                try { setDone(await api.writeBack(findingId)); } catch (e) { setError(message(e)); }
                setBusy(false);
              }}>
        <Send size={13} aria-hidden="true" />{busy ? "Sending…" : "Send verdict"}
      </button>
      {done ? <span className="small t-ok" role="status">“{done.label}” written to {done.written.length} platform{done.written.length === 1 ? "" : "s"}</span> : null}
      {error ? <span className="small t-bad" role="alert">{error}</span> : null}
    </span>
  );
}
