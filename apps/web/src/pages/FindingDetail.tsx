import { ArrowRight, CircleCheck, FileCode2, FlaskConical, History, Siren, Workflow } from "lucide-react";
import { useState } from "react";
import { ApiError, api, downloadRegression } from "../api";
import { SendVerdict } from "../components/Platforms";
import { EvidenceLedger, ReportButtons } from "../components/EvidenceLedger";
import { BUTTON, Experiments, ReviewPanel } from "../components/Outcome";
import { Badge, Card, Chip, Compare, ErrorBox, Hash, Ladder, Loading, PageHeader, Skeleton } from "../components/ui";
import { Verify, leading } from "../components/Verify";
import { label, parseTime, pct, short, when } from "../format";
import { useLoad } from "../hooks";
import { STAGE_INFO, stage } from "../lib/lifecycle";
import type { Computation, FindingDetail as Finding } from "../types";
import "../styles/pages/finding.css";

export { stage };

const ACTION: Record<string, string> = { verify: "Verify a hypothesis", ...BUTTON };
const SECTIONS = [
  { id: "symptom", label: "Symptom" }, { id: "origin", label: "Origin" }, { id: "verification", label: "Verification" },
  { id: "decision", label: "Decision" }, { id: "evidence", label: "Evidence" },
] as const;

/** Bring a section of the case file into view and move focus to it (hash routing owns the URL fragment). */
function goTo(section: string) {
  const el = document.getElementById(`case-${section}`);
  if (!el) return;
  el.scrollIntoView?.({ behavior: "smooth", block: "start" });
  el.focus({ preventScroll: true });
}

/** Download a regression test (case file, pytest module, README) once a replay has confirmed the origin. */
export function ExportRegression({ id, enabled }: { id: string; enabled: boolean }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  return (
    <span className="row tight">
      <button type="button" className="btn sm" disabled={!enabled || busy}
              title={enabled ? "A pytest file that fails until the confirmed cause is fixed"
                : "Available once a replay has confirmed the origin"}
              onClick={async () => {
                setBusy(true); setError("");
                try { await downloadRegression(id); } catch (e) { setError(e instanceof ApiError ? e.message : "Export failed."); }
                setBusy(false);
              }}>
        <FileCode2 size={13} aria-hidden="true" />{busy ? "Exporting…" : "Export regression test"}
      </button>
      {error ? <span role="alert" className="small t-bad">{error}</span> : null}
    </span>
  );
}

/** The rail: the verdict with the replays behind it, the one next step, exports and the finding's identity. */
function CaseRail({ f }: { f: Finding }) {
  const lead = leading(f.hypotheses);
  const experiments = lead ? f.experiments.filter((e) => e.hypothesis_id === lead.id && e.summary) : [];
  const latest = experiments.sort((a, b) => (parseTime(b.created_at)?.getTime() ?? 0) - (parseTime(a.created_at)?.getTime() ?? 0))[0];
  const s = latest?.summary;
  const replayable = f.hypotheses.some((h) => h.can_verify);
  const decisions = f.allowed_actions.filter((a) => a !== "verify");
  const next = f.allowed_actions.includes("verify") ? { to: "origin", text: "Verify the suspects" }
    : decisions.length ? { to: "decision", text: "Record your decision" } : null;
  const valid = f.evidence.filter((e) => e.hash_valid).length;
  return (
    <aside className="case-rail" aria-label="Case summary">
      <section className="case-block" aria-labelledby="rail-verdict">
        <h2 id="rail-verdict" className="eyebrow">Verdict</h2>
        {lead ? (
          <>
            <div className="case-verdict"><span>{lead.agent}</span><Badge value={lead.status === "open" ? "hypothesized" : lead.status} text={lead.status === "open" ? "suspect" : undefined} /></div>
            {s ? (
              <dl className="case-counts">
                <div><dt>with the fix</dt><dd className="mono">{s.k_pass}/{s.n_completed}</dd></div>
                <div><dt>without</dt><dd className="mono">{s.c_pass}/{s.m_completed}</dd></div>
                <div><dt>95% interval</dt><dd className="mono">{pct(s.ci_low)}–{pct(s.ci_high)}</dd></div>
              </dl>
            ) : <p className="small muted">Not verified by replay yet.</p>}
          </>
        ) : <p className="small muted">No suspect was ranked for this finding.</p>}
        {!replayable && f.hypotheses.length > 0 ? <p className="small muted">Replay needs a workflow Granite can run; no suspect here can be replayed.</p> : null}
      </section>

      <section className="case-block" aria-labelledby="rail-next">
        <h2 id="rail-next" className="eyebrow">Next step</h2>
        {next ? (
          <button type="button" className="btn primary" onClick={() => goTo(next.to)}>{next.text}<ArrowRight size={14} aria-hidden="true" /></button>
        ) : <p className="small muted">This finding is {label(f.status).toLowerCase()}; nothing is open.</p>}
        <div className="row tight case-allowed">
          <span className="small dim">Allowed now:</span>
          {f.allowed_actions.length === 0 ? <Chip>none: closed</Chip>
            : f.allowed_actions.map((a) => <Chip key={a} tone="replay">{ACTION[a] ?? label(a)}</Chip>)}
        </div>
      </section>

      <section className="case-block" aria-labelledby="rail-export">
        <h2 id="rail-export" className="eyebrow">Export and share</h2>
        <ReportButtons id={f.id} />
        <ExportRegression id={f.id} enabled={!!f.can_export_regression} />
        <SendVerdict findingId={f.id} runId={f.run_id} />
        <a className="btn sm" href={`#/runs/${f.run_id}`}><Workflow size={13} aria-hidden="true" />View the run</a>
      </section>

      <section className="case-block" aria-labelledby="rail-id">
        <h2 id="rail-id" className="eyebrow">Record</h2>
        <div className="small"><Hash value={f.id} length={24} label="finding id" /></div>
        <p className={`small ${valid === f.evidence.length ? "t-ok" : "t-bad"}`}>{valid} of {f.evidence.length} evidence hashes verified</p>
        <p className="small dim">Opened {when(f.created_at)}</p>
      </section>
    </aside>
  );
}

export function FindingDetail({ id }: { id: string }) {
  const q = useLoad(() => api.finding(id), [id]);
  const runId = q.data?.run_id;
  // the causal map is an aid: if the graph cannot be loaded the page works without it
  const g = useLoad(() => (runId ? api.graph(runId) : Promise.resolve(null)), [runId]);
  if (q.loading && !q.data) return <div className="page"><Loading /><Skeleton lines={6} /></div>;
  if (q.error || !q.data) return <ErrorBox message={q.error || "Finding not found."} onRetry={q.reload} />;
  const f = q.data;
  const at = stage(f.status);
  const check = f.evidence.find((e) => e.type === "check_computation")?.payload as
    { observed?: unknown; expected?: unknown; computation?: Computation } | undefined;
  const compared = check && (check.observed !== undefined && check.observed !== null || check.expected !== undefined && check.expected !== null);
  const silent = f.kind === "silent_failure";

  return (
    <div className="page lab">
      <PageHeader
        back={{ href: "#/", label: "Inbox" }}
        eyebrow="Case file"
        title={short(f.title, 110)}
        meta={<>
          <Badge value={f.status} large />
          <Ladder level={f.verification_level} />
          <Chip title="Severity of the failed check">{f.severity} severity</Chip>
          {f.check_id ? <Chip mono title="The check that failed">{f.check_id}</Chip> : null}
          <Chip title="The step where the wrong outcome showed">symptom at {f.symptom_step}</Chip>
          <Chip tone={silent ? "bad" : "neutral"}>{silent ? "silent failure" : f.kind.replace(/_/g, " ")}</Chip>
        </>}
      />

      <nav className="case-sections" aria-label="Case sections">
        {SECTIONS.map((s, i) => <button key={s.id} type="button" className="btn ghost sm" onClick={() => goTo(s.id)}><span className="mono dim">{i + 1}</span>{s.label}</button>)}
      </nav>

      <div className="case">
        <CaseRail f={f} />
        <div className="case-main">
          <div className="lab-rail card">
            <ol className="stepper" aria-label="Investigation progress">
              {STAGE_INFO.map((s, i) => (
                <li key={s.name} className={i + 1 < at ? "done" : i + 1 === at ? "current" : ""} aria-current={i + 1 === at ? "step" : undefined}>
                  <strong>{s.name}</strong><span>{s.does}</span>
                </li>
              ))}
            </ol>
          </div>

          <div id="case-symptom" className="case-anchor" tabIndex={-1}>
            <Card title="Symptom" icon={Siren} sub="what went wrong">
              <p>{f.detail}</p>
              {compared ? <div className="lab-symptom-compare"><Compare observed={check?.observed} expected={check?.expected} observedLabel="Observed in the run" expectedLabel="Expected by the check" /></div> : null}
              {check?.computation?.expression ? (
                <details className="lab-expr"><summary className="small">The check, as evaluated</summary><p className="mono small muted wrap-any">{check.computation.expression}</p></details>
              ) : null}
              {silent ? (
                <p className="row tight small muted lab-noerror"><CircleCheck size={13} aria-hidden="true" />The run completed and raised no error: ordinary output monitoring had nothing to report.</p>
              ) : <p className="small muted">The run stopped at step {f.symptom_step}.</p>}
            </Card>
          </div>

          <div id="case-origin" className="case-anchor" tabIndex={-1}><Verify f={f} graph={g.data} onDone={q.reload} /></div>

          <div id="case-verification" className="case-anchor" tabIndex={-1}>
            {f.experiments.length > 0 ? <Experiments f={f} /> : (
              <Card title="Verification results" icon={FlaskConical}><p className="small muted">No experiment yet. Verify a suspect above: fix replays are compared with controls under rule VR-1.</p></Card>
            )}
          </div>

          <div id="case-decision" className="case-anchor stack" tabIndex={-1}>
            <ReviewPanel f={f} onDone={q.reload} />
            {f.reviews.length > 0 && (
              <Card title="Review history" icon={History}>
                <ol className="lab-history">
                  {f.reviews.map((r) => (
                    <li key={r.id}>
                      <div className="row tight">
                        <strong>{r.reviewer}</strong>
                        <Chip>{BUTTON[r.decision] ?? label(r.decision)}</Chip>
                        <span className="small muted">{r.from_status ? `${label(r.from_status)} → ` : ""}{label(r.to_status)}</span>
                        <span className="small dim">{when(r.created_at)}</span>
                      </div>
                      {r.comment ? <p className="small">{r.comment}</p> : null}
                    </li>
                  ))}
                </ol>
              </Card>
            )}
          </div>

          <div id="case-evidence" className="case-anchor" tabIndex={-1}><EvidenceLedger f={f} /></div>
        </div>
      </div>
    </div>
  );
}
