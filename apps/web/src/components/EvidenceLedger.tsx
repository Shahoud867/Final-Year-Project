import { Download, Eye, FileJson, Fingerprint } from "lucide-react";
import { useState } from "react";
import { ApiError, downloadReport } from "../api";
import { evidenceType, when } from "../format";
import type { Evidence, FindingDetail } from "../types";
import { Badge, Card, ErrorBox, Hash, InfoTip, JsonView, KV, Drawer, Notice } from "./ui";

/**
 * The evidence behind a finding: every record with its SHA-256 and the server's integrity check, the full payload on
 * demand, and the report export. `hash_valid` is the server's answer each time the finding is read, not a stored flag.
 */
export function EvidenceLedger({ f }: { f: FindingDetail }) {
  const [open, setOpen] = useState<Evidence | null>(null);
  const [error, setError] = useState("");
  const valid = f.evidence.filter((e) => e.hash_valid).length;
  const broken = f.evidence.length - valid;

  async function download(format: "md" | "json") {
    setError("");
    try { await downloadReport(f.id, format); }
    catch (e) { setError(e instanceof ApiError ? e.message : "Could not create the report."); }
  }

  return (
    <Card title="Evidence" icon={Fingerprint} className="lab-evidence"
          sub={<>{`${f.evidence.length} record${f.evidence.length === 1 ? "" : "s"}, ${valid} hash${valid === 1 ? "" : "es"} verified`} <InfoTip label="How evidence is checked" text="Each record is stored once with the SHA-256 of its canonical JSON. Every time the finding is opened the server recomputes the hash and compares. The API has no way to edit or delete a record." /></>}
          actions={<>
            <button type="button" className="btn sm" onClick={() => download("md")}><Download size={13} aria-hidden="true" />Download report (.md)</button>
            <button type="button" className="btn sm" onClick={() => download("json")}><FileJson size={13} aria-hidden="true" />Report (.json)</button>
          </>}>
      <ErrorBox message={error} />
      {broken > 0 ? (
        <Notice tone="bad" role="alert" title="Integrity check failed">
          {broken} record{broken === 1 ? "" : "s"} no longer match{broken === 1 ? "es" : ""} the stored hash. Treat the conclusions that rest on {broken === 1 ? "it" : "them"} as unproven.
        </Notice>
      ) : null}
      <div className="table-wrap">
        <table className="lab-ledger">
          <thead><tr><th>Record</th><th>Recorded</th><th>SHA-256</th><th>Integrity</th><th><span className="sr-only">Content</span></th></tr></thead>
          <tbody>{f.evidence.map((e) => (
            <tr key={e.id}>
              <td><div>{e.title}</div><div className="small dim">{evidenceType(e.type)}</div></td>
              <td className="small nowrap">{when(e.created_at) || <span className="dim">n/a</span>}</td>
              <td><Hash value={e.sha256} label={`SHA-256 of ${e.title}`} /></td>
              <td><Badge value={e.hash_valid ? "pass" : "fail"} text={e.hash_valid ? "hash matches" : "TAMPERED"} /></td>
              <td><button type="button" className="btn ghost sm" onClick={() => setOpen(e)} aria-label={`View ${e.title}`}><Eye size={13} aria-hidden="true" />View</button></td>
            </tr>
          ))}</tbody>
        </table>
      </div>
      <Drawer open={!!open} onClose={() => setOpen(null)} title={open?.title ?? ""} sub={open ? evidenceType(open.type) : undefined} width={600}>
        {open ? (
          <>
            <KV items={[
              ["Integrity", <Badge key="i" value={open.hash_valid ? "pass" : "fail"} text={open.hash_valid ? "hash matches the content" : "content does not match the hash"} />],
              ["SHA-256", <span key="h" className="mono small wrap-any">{open.sha256}</span>],
              ["Recorded", when(open.created_at) || "n/a"],
              ...(open.reproduce ? [["Reproduce", open.reproduce] as [string, string]] : []),
            ]} />
            <JsonView value={open.payload} label={`Content of ${open.title}`} maxHeight={520} />
          </>
        ) : null}
      </Drawer>
    </Card>
  );
}
