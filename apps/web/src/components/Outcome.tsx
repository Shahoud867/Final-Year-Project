import { ArrowRight, Check, FlaskConical, Gavel, Lock, Minus, UserCheck, Wrench, X } from "lucide-react";
import { useState } from "react";
import { ApiError, api } from "../api";
import { finalText, label, parseTime, pct, when } from "../format";
import { ruleLines } from "../lib/vr1";
import type { Experiment, FindingDetail } from "../types";
import { RateAxis, ReplayDots } from "./Replay";
import { Badge, Card, Chip, ErrorBox, InfoTip, JsonView, ModeBadge, Notice } from "./ui";

const time = (e: Experiment) => parseTime(e.created_at)?.getTime() ?? 0;

/** One verification experiment: the server's verdict, and the replay results and rule that explain it. */
function ExperimentBlock({ e, agent }: { e: Experiment; agent: string }) {
  const s = e.summary;
  const verdict = e.verdict ?? e.status;
  const decided = !!s && (e.verdict === "confirmed" || e.verdict === "refuted" || e.verdict === "inconclusive");
  const fixRate = s && s.n_completed > 0 ? s.k_pass / s.n_completed : null;
  const controlRate = s && s.m_completed > 0 ? s.c_pass / s.m_completed : null;
  return (
    <article className={`lab-exp v-${verdict}`} aria-label={`Experiment on ${agent}: ${label(verdict)}`}>
      <header className="lab-exp-head">
        <h3>{agent}</h3>
        <Badge value={verdict} large />
        <span className="spacer" />
        <ModeBadge mode={e.llm_mode} />
        <Chip mono title="The pre-registered verdict rule">{s?.rule_version ?? e.rule_version ?? "VR-1"}</Chip>
        {e.created_at ? <span className="small dim">{when(e.created_at)}</span> : null}
      </header>

      {e.intervention ? (
        <details className="lab-fix">
          <summary><Wrench size={13} aria-hidden="true" /> <span className="small">{e.intervention.description || `Patched step ${e.intervention.step_id}`}</span></summary>
          <JsonView value={e.intervention.patches} label={`Corrected output of ${agent}`} maxHeight={180} />
        </details>
      ) : null}

      {s ? (
        <>
          <div className="lab-compare">
            <div className="lab-rows">
              <span className="small">With the fix</span>
              <ReplayDots replays={e.replays} kind="intervention" planned={s.n_planned} label={`Fix replays of ${agent}`} />
              <span className="mono num">{s.k_pass}/{s.n_completed}<span className="dim"> correct</span></span>
              <span className="small">Control, no fix</span>
              <ReplayDots replays={e.replays} kind="control" planned={s.m_planned} label={`Control replays of ${agent}`} />
              <span className="mono num">{s.m_planned > 0 ? <>{s.c_pass}/{s.m_completed}<span className="dim"> correct</span></> : <span className="dim">n/a</span>}</span>
            </div>
            <RateAxis fix={fixRate} control={controlRate} ciLow={fixRate === null ? undefined : s.ci_low} ciHigh={fixRate === null ? undefined : s.ci_high} />
          </div>

          {decided ? (
            <div className="lab-rule">
              <span className="eyebrow">Rule {s.rule_version} <InfoTip align="start" label="About rule VR-1" text="Confirmed: at least 80% of the fix replays are correct and at most 20% of the controls are. Refuted: at most 20% of the fix replays are correct. Anything else is inconclusive. The thresholds were fixed before any result existed." /></span>
              <ul className="checklist">
                {ruleLines(s.k_pass, s.n_planned, s.c_pass, s.m_planned).map((line) => (
                  <li key={line.id} className={line.holds ? "" : "dim"}>
                    {line.holds === null ? <Minus size={14} aria-hidden="true" /> : line.holds ? <Check size={14} className="t-ok" aria-hidden="true" /> : <X size={14} aria-hidden="true" />}
                    <span>{line.text}<span className="mono"> : {line.rate === null ? "n/a" : pct(line.rate)}</span>
                      <span className="sr-only">{line.holds === null ? " (not evaluated)" : line.holds ? " (holds)" : " (does not hold)"}</span></span>
                  </li>
                ))}
              </ul>
              <p className="lab-verdict"><ArrowRight size={14} aria-hidden="true" /> Server verdict: <strong>{label(verdict)}</strong>. {s.explanation}</p>
            </div>
          ) : (
            <Notice tone="warn" title="No verdict">{s.explanation || e.error || "The replays did not finish."}</Notice>
          )}

          <details className="lab-replays">
            <summary className="small">Replay-level results ({e.replays.length})</summary>
            <div className="table-wrap">
              <table>
                <thead><tr><th>Replay</th><th>Seed</th><th>Result</th><th>Checks fixed</th><th>Still failing</th><th>Regressions</th><th>Final output</th></tr></thead>
                <tbody>
                  {e.replays.map((r) => (
                    <tr key={`${r.kind}${r.idx}`}>
                      <td className="nowrap">{r.kind === "control" ? "control" : "fix"} {r.idx + 1}</td>
                      <td className="mono">{r.seed}</td>
                      <td>{!r.completed || r.passed === null ? <Badge value="abstain" text="not finished" /> : r.passed ? <Badge value="pass" text="correct" /> : <Badge value="fail" text="still wrong" />}</td>
                      <td className="mono small">{r.judgement?.fixed.join(", ") || "none"}</td>
                      <td className="mono small">{r.judgement?.still_failing.join(", ") || "none"}</td>
                      <td className="mono small">{r.judgement?.regressions.join(", ") || "none"}</td>
                      <td className="small">{finalText(r.final_output) || <span className="dim">n/a</span>}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </details>
        </>
      ) : e.status === "error" || e.error ? (
        <Notice tone="warn" title="No verdict">{e.error || "The experiment could not run."}</Notice>
      ) : (
        <p className="muted small" role="status">Replays are running…</p>
      )}
    </article>
  );
}

export function Experiments({ f }: { f: FindingDetail }) {
  if (f.experiments.length === 0) return null;
  const newestFirst = [...f.experiments].sort((a, b) => time(b) - time(a));
  return (
    <Card title="Verification results" icon={FlaskConical} sub={`${f.experiments.length} experiment${f.experiments.length === 1 ? "" : "s"}, newest first`}>
      <div className="stack">
        {newestFirst.map((e) => (
          <ExperimentBlock key={e.id} e={e} agent={f.hypotheses.find((h) => h.id === e.hypothesis_id)?.agent ?? e.hypothesis_id} />
        ))}
      </div>
    </Card>
  );
}

export const BUTTON: Record<string, string> = {
  accept: "Accept", reject: "Reject", resolve: "Mark resolved", wont_fix: "Close without fixing",
  request_info: "Ask for more information",
};

/** What each decision does to the finding (the server's state machine decides whether it is allowed now). */
const LEADS_TO: Record<string, string> = {
  accept: "Accepted, level V3 (human-confirmed)", reject: "Rejected and closed", request_info: "Recorded; status unchanged",
  resolve: "Resolved and closed", wont_fix: "Closed without a fix",
};

/** Same rule as the server (FR-REV-01): a reason is needed to reject, close, ask, or accept an inconclusive finding. */
export function needsComment(action: string, status: string): boolean {
  return ["reject", "wont_fix", "request_info"].includes(action) || (action === "accept" && status === "inconclusive");
}

export function ReviewPanel({ f, onDone }: { f: FindingDetail; onDone: () => void }) {
  const [comment, setComment] = useState("");
  const [reviewer, setReviewer] = useState("");
  const [error, setError] = useState("");
  const [sending, setSending] = useState("");
  const actions = f.allowed_actions.filter((a) => a !== "verify");
  if (actions.length === 0) {
    const waiting = f.allowed_actions.includes("verify");
    return (
      <Card title="Human review" icon={Lock} className="lab-locked">
        <p className="muted small">
          {waiting ? "Available after a verification verdict. The server refuses a decision before that."
            : `This finding is ${label(f.status).toLowerCase()}; no further decision is open.`}
        </p>
      </Card>
    );
  }

  async function decide(a: string) {
    if (needsComment(a, f.status) && comment.trim().length < 5) { setError("Please say why (at least 5 characters)."); return; }
    setSending(a);
    try {
      await api.review(f.id, a, comment, reviewer.trim() || "analyst");
      setComment(""); setError(""); onDone();
    } catch (e) { setError(e instanceof ApiError ? e.message : "Something went wrong."); }
    setSending("");
  }

  return (
    <Card title="Your decision" icon={Gavel} tone="warn" sub="a person closes a finding, never the software">
      <div className="grid cols-2">
        <div className="field">
          <label htmlFor="rev">Your name</label>
          <input id="rev" value={reviewer} onChange={(e) => setReviewer(e.target.value)} placeholder="analyst" maxLength={80} autoComplete="name" />
        </div>
        <div className="field">
          <label htmlFor="cm">Comment</label>
          <textarea id="cm" rows={2} value={comment} onChange={(e) => setComment(e.target.value)} maxLength={2000} aria-describedby="cm-hint" />
          <div className="hint" id="cm-hint">Required to reject, close without fixing, ask for information, or accept an inconclusive finding.</div>
        </div>
      </div>
      <ErrorBox message={error} />
      <div className="row">
        {actions.map((a) => (
          <button key={a} type="button" className={`btn${a === "accept" ? " primary" : a === "reject" ? " danger" : ""}`} onClick={() => decide(a)} disabled={!!sending}>
            {a === "accept" ? <UserCheck size={14} aria-hidden="true" /> : null}{BUTTON[a] ?? label(a)}
          </button>
        ))}
      </div>
      <ul className="lab-leads small muted">
        {actions.map((a) => <li key={a}><span>{BUTTON[a] ?? label(a)}</span><ArrowRight size={12} aria-hidden="true" /><span>{LEADS_TO[a] ?? "see the lifecycle"}</span></li>)}
      </ul>
    </Card>
  );
}
