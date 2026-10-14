import { ArrowRight, CircleCheck, History, Siren, Workflow } from "lucide-react";
import { api } from "../api";
import { EvidenceLedger } from "../components/EvidenceLedger";
import { BUTTON, Experiments, ReviewPanel } from "../components/Outcome";
import { Badge, Card, Chip, Compare, ErrorBox, LevelBadge, Loading, PageHeader } from "../components/ui";
import { Verify } from "../components/Verify";
import { label, short, when } from "../format";
import { useLoad } from "../hooks";
import { STAGE_INFO, stage } from "../lib/lifecycle";
import type { Computation } from "../types";
import "../styles/pages/finding.css";

export { stage };

const ACTION: Record<string, string> = { verify: "Verify a hypothesis", ...BUTTON };

export function FindingDetail({ id }: { id: string }) {
  const q = useLoad(() => api.finding(id), [id]);
  const runId = q.data?.run_id;
  // the causal map is an aid: if the graph cannot be loaded the page works without it
  const g = useLoad(() => (runId ? api.graph(runId) : Promise.resolve(null)), [runId]);
  if (q.loading && !q.data) return <Loading />;
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
        back={{ href: "#/", label: "All investigations" }}
        eyebrow="Verification lab"
        title={short(f.title, 110)}
        meta={<>
          <Badge value={f.status} large />
          <LevelBadge level={f.verification_level} showName />
          <Chip title="Severity of the failed check">{f.severity} severity</Chip>
          {f.check_id ? <Chip mono title="The check that failed">{f.check_id}</Chip> : null}
          <Chip title="The step where the wrong outcome showed">symptom at {f.symptom_step}</Chip>
          <Chip tone={silent ? "bad" : "neutral"}>{silent ? "silent failure" : f.kind.replace(/_/g, " ")}</Chip>
          <span className="mono small dim">{f.id}</span>
        </>}
        actions={<a className="btn sm" href={`#/runs/${f.run_id}`}><Workflow size={13} aria-hidden="true" />View the run</a>}
      />

      <div className="lab-rail card">
        <ol className="stepper" aria-label="Investigation progress">
          {STAGE_INFO.map((s, i) => (
            <li key={s.name} className={i + 1 < at ? "done" : i + 1 === at ? "current" : ""} aria-current={i + 1 === at ? "step" : undefined}>
              <strong>{s.name}</strong><span>{s.does}</span>
            </li>
          ))}
        </ol>
        <div className="lab-allowed">
          <span className="eyebrow">Allowed now</span>
          {f.allowed_actions.length === 0 ? <Chip>none: closed</Chip>
            : f.allowed_actions.map((a) => <Chip key={a} tone="replay" icon={ArrowRight}>{ACTION[a] ?? label(a)}</Chip>)}
        </div>
      </div>

      <Card title="Symptom" icon={Siren} sub="why this was flagged">
        <p>{f.detail}</p>
        {compared ? <div className="lab-symptom-compare"><Compare observed={check?.observed} expected={check?.expected} observedLabel="Observed in the run" expectedLabel="Expected by the check" /></div> : null}
        {check?.computation?.expression ? <p className="mono small muted wrap-any lab-expr">{check.computation.expression}</p> : null}
        {silent ? (
          <p className="row tight small muted lab-noerror"><CircleCheck size={13} aria-hidden="true" />The run completed and raised no error: ordinary output monitoring had nothing to report.</p>
        ) : <p className="small muted">The run stopped at step {f.symptom_step}.</p>}
      </Card>

      <Verify f={f} graph={g.data} onDone={q.reload} />
      <Experiments f={f} />
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

      <EvidenceLedger f={f} />
    </div>
  );
}
