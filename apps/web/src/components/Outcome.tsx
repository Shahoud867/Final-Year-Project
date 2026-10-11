import { useState } from "react";
import { ApiError, api } from "../api";
import { label, pct } from "../format";
import type { FindingDetail } from "../types";
import { Badge, ErrorBox } from "./ui";

export function Experiments({ f }: { f: FindingDetail }) {
  if (f.experiments.length === 0) return null;
  return (
    <section className="card" aria-labelledby="x-h">
      <h2 id="x-h">Verification results</h2>
      {f.experiments.map((e) => {
        const hyp = f.hypotheses.find((h) => h.id === e.hypothesis_id);
        const s = e.summary;
        const tone = e.verdict === "confirmed" ? "ok" : e.verdict === "refuted" ? "bad" : "warn";
        return (
          <div key={e.id} className={`alert ${tone}`}>
            <div className="row between"><strong>{hyp?.agent ?? e.hypothesis_id}</strong><Badge value={e.verdict ?? e.status} /></div>
            {s ? (
              <>
                <p>{s.explanation}</p>
                <p className="small">
                  With the fix: {s.k_pass}/{s.n_completed} correct (95% interval {pct(s.ci_low)} to {pct(s.ci_high)}).
                  Without it: {s.m_completed ? `${s.c_pass}/${s.m_completed} correct` : "no control finished"}. Rule {s.rule_version}.
                </p>
                <div className="row">
                  {e.replays.map((r) => (
                    <span key={`${r.kind}${r.idx}`} className="badge" title={`seed ${r.seed}`}>
                      {r.kind === "control" ? "control" : "fix"} {r.idx + 1}: {r.passed === null ? "unfinished" : r.passed ? "correct" : "still wrong"}
                    </span>
                  ))}
                </div>
              </>
            ) : <p>{e.error || "Running…"}</p>}
          </div>
        );
      })}
    </section>
  );
}

export const BUTTON: Record<string, string> = {
  accept: "Accept", reject: "Reject", resolve: "Mark resolved", wont_fix: "Close without fixing",
  request_info: "Ask for more information",
};

/** Same rule as the server (FR-REV-01): a reason is needed to reject, close, ask, or accept an inconclusive finding. */
export function needsComment(action: string, status: string): boolean {
  return ["reject", "wont_fix", "request_info"].includes(action) || (action === "accept" && status === "inconclusive");
}

export function ReviewPanel({ f, onDone }: { f: FindingDetail; onDone: () => void }) {
  const [comment, setComment] = useState("");
  const [reviewer, setReviewer] = useState("");
  const [error, setError] = useState("");
  const actions = f.allowed_actions.filter((a) => a !== "verify");
  if (actions.length === 0) return null;

  async function decide(a: string) {
    if (needsComment(a, f.status) && comment.trim().length < 5) { setError("Please say why (at least 5 characters)."); return; }
    try {
      await api.review(f.id, a, comment, reviewer.trim() || "analyst");
      setComment(""); setError(""); onDone();
    } catch (e) { setError(e instanceof ApiError ? e.message : "Something went wrong."); }
  }

  return (
    <section className="card" aria-labelledby="rv-h">
      <h2 id="rv-h">Your decision</h2>
      <div className="grid cols-2">
        <div className="field">
          <label htmlFor="rev">Your name</label>
          <input id="rev" value={reviewer} onChange={(e) => setReviewer(e.target.value)} placeholder="analyst" maxLength={80} />
        </div>
        <div className="field">
          <label htmlFor="cm">Comment</label>
          <textarea id="cm" rows={2} value={comment} onChange={(e) => setComment(e.target.value)} maxLength={2000} />
          <div className="hint">Required to reject, close without fixing, ask for information, or accept an inconclusive finding.</div>
        </div>
      </div>
      <ErrorBox message={error} />
      <div className="row">
        {actions.map((a) => (
          <button key={a} className={a === "accept" ? "primary" : ""} onClick={() => decide(a)}>{BUTTON[a] ?? label(a)}</button>
        ))}
      </div>
    </section>
  );
}
