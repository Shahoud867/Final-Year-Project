import { Lock, Play, Repeat, Route, Search, Wrench } from "lucide-react";
import { useState } from "react";
import { ApiError, api, waitForJob } from "../api";
import { evidenceKind, label } from "../format";
import { DEFAULT_CONTROLS, DEFAULT_REPLAYS, MAX_CONTROLS, MAX_REPLAYS } from "../lib/vr1";
import type { Experiment, FindingDetail, Graph as GraphData, Hypothesis, Job } from "../types";
import { Graph } from "./Graph";
import type { NodeMark } from "./Graph";
import { ReplayDots } from "./Replay";
import { Badge, Card, Chip, ErrorBox, InfoTip, Progress, describe } from "./ui";

/** Step ids of the data-flow path the server recorded from a suspected step to the symptom. */
export function pathOf(h: Hypothesis | undefined): string[] {
  return h?.evidence?.find((e) => e.type === "provenance_path")?.path?.map((p) => p.step_id) ?? [];
}

/** How a hypothesis is drawn on the graph: confirmed by replay, refuted by replay, or still a suspect. */
export function markOf(h: Hypothesis): NodeMark {
  return h.status === "confirmed" ? "origin" : h.status === "refuted" ? "refuted" : "suspect";
}

/** The hypothesis an investigation leads with: the one a replay confirmed, otherwise the first-ranked. */
export function leading(hypotheses?: Hypothesis[] | null): Hypothesis | undefined {
  return hypotheses?.find((h) => h.status === "confirmed") ?? hypotheses?.[0];
}

const inRange = (v: number, lo: number, hi: number) => Number.isInteger(v) && v >= lo && v <= hi;

/** Ranked origin hypotheses with the causal map, and the controlled-replay experiment that tests one of them. */
export function Verify({ f, graph, onDone }: { f: FindingDetail; graph?: GraphData | null; onDone: () => void }) {
  const [busy, setBusy] = useState("");
  const [job, setJob] = useState<Job | null>(null);
  const [live, setLive] = useState<Experiment | null>(null);
  const [error, setError] = useState("");
  const [n, setN] = useState(DEFAULT_REPLAYS);
  const [m, setM] = useState(DEFAULT_CONTROLS);
  const [picked, setPicked] = useState("");
  const canVerify = f.allowed_actions.includes("verify");
  const nOk = inRange(n, 1, MAX_REPLAYS), mOk = inRange(m, 0, MAX_CONTROLS);
  const chosen = f.hypotheses.find((h) => h.id === picked) ?? leading(f.hypotheses);
  const path = pathOf(chosen);
  const steps = graph?.nodes.filter((nd) => nd.kind !== "input") ?? [];
  const cut = chosen ? steps.findIndex((s) => s.id === chosen.step_id) : -1;
  const symptom = steps.find((s) => s.id === f.symptom_step)?.label ?? f.symptom_step;

  async function run(h: Hypothesis) {
    setBusy(h.id); setError(""); setJob(null); setLive(null); setPicked(h.id);
    try {
      const { job_id, experiment_id } = await api.verify(h.id, n, m);
      await waitForJob(job_id, (j) => {
        setJob(j);
        // each finished replay is stored at once, so the marks below fill with real results (failure is not fatal)
        void api.experiment(experiment_id).then(setLive, () => undefined);
      });
    } catch (e) { setError(e instanceof ApiError ? e.message : "Something went wrong."); }
    setBusy(""); onDone();
  }

  const why = busy ? "" : !canVerify ? `Replays are not available while the finding is ${label(f.status).toLowerCase()}.`
    : !nOk || !mOk ? "Fix the replay counts to verify." : "";

  return (
    <Card title="Where did it begin?" icon={Search} className="lab-origin"
          sub={<>ranked from the recorded data flow <InfoTip text="Each step on the path back from the symptom is classified from evidence already in the run: its own check against the source of truth, its contract, and what it received. No model is asked, and the injected fault is never read." label="How suspects are ranked" /></>}>
      {graph && graph.nodes.length > 0 && chosen ? (
        <figure className="lab-map">
          <Graph graph={graph} path={path.length > 1 ? path : undefined} marks={{ [chosen.step_id]: markOf(chosen) }} label="Causal map" />
          <figcaption className="small muted">
            <Route size={13} aria-hidden="true" /> {path.length > 1
              ? <>Recorded data-flow path from <strong>{chosen.agent}</strong> to the symptom at <strong>{symptom}</strong></>
              : <><strong>{chosen.agent}</strong> is where the symptom showed</>}
          </figcaption>
        </figure>
      ) : null}

      <ol className="lab-hyps">
        {f.hypotheses.map((h) => {
          const on = chosen?.id === h.id;
          return (
            <li key={h.id} className={`lab-hyp${on ? " on" : ""}`}>
              <span className="lab-rank mono" aria-label={`Rank ${h.rank}`}>{h.rank}</span>
              <div className="lab-hyp-main">
                <div className="row tight">
                  <strong>{h.agent}</strong>
                  <Chip tone={h.evidence_kind === "truth_mismatch" || h.evidence_kind === "contract_fail" ? "warn" : "neutral"}>{evidenceKind(h.evidence_kind)}</Chip>
                  <Badge value={h.status} text={h.status === "open" ? "Not tested" : undefined} tone={h.status === "open" ? "neutral" : undefined} />
                </div>
                <p className="small muted">{h.rationale}</p>
              </div>
              <div className="lab-score" title={`${h.method} score ${h.score.toFixed(2)}`}>
                <span className="eyebrow">score</span>
                <span className="mono">{h.score.toFixed(2)}</span>
                <span className="bar" aria-hidden="true"><i className="tone-warn" style={{ flex: Math.max(0, Math.min(1, h.score)) }} /><i style={{ flex: 1 - Math.max(0, Math.min(1, h.score)), background: "transparent" }} /></span>
              </div>
              <div className="lab-hyp-actions">
                <button type="button" className="btn ghost sm" aria-pressed={on} aria-label={`Show path from ${h.agent}`} onClick={() => setPicked(h.id)}>
                  <Route size={13} aria-hidden="true" />Path
                </button>
                {h.can_verify
                  ? <button type="button" className="btn primary sm" onClick={() => run(h)} disabled={!canVerify || !!busy || !nOk || !mOk}><Play size={12} aria-hidden="true" />Verify</button>
                  : <span className="small dim" title="The workflow defines no repair rule for this step, so a replay would have nothing to test">no automatic replay</span>}
              </div>
            </li>
          );
        })}
      </ol>

      <div className="lab-replay">
        <div className="lab-replay-set">
          <div className="field">
            <label htmlFor="n">Replays with fix</label>
            <input id="n" type="number" min={1} max={MAX_REPLAYS} step={1} value={Number.isNaN(n) ? "" : n} onChange={(e) => setN(e.target.valueAsNumber)}
                   {...describe("n", { error: nOk ? "" : "x" })} />
            {nOk ? null : <div className="field-error" id="n-err">Use 1 to {MAX_REPLAYS}</div>}
          </div>
          <div className="field">
            <label htmlFor="m">Controls</label>
            <input id="m" type="number" min={0} max={MAX_CONTROLS} step={1} value={Number.isNaN(m) ? "" : m} onChange={(e) => setM(e.target.valueAsNumber)}
                   {...describe("m", { error: mOk ? "" : "x" })} />
            {mOk ? null : <div className="field-error" id="m-err">Use 0 to {MAX_CONTROLS}</div>}
          </div>
        </div>
        {cut >= 0 && chosen ? (
          <div className="lab-plan" aria-label={`Replay plan for ${chosen.agent}`} role="group">
            <span className="eyebrow">Replay plan <InfoTip text="Steps up to the suspect are reused exactly as recorded. The suspect's output is replaced with the value its contract or the source of truth requires, then the later steps run again: N times with the correction and M times without it (controls)." label="About the replay plan" align="start" /></span>
            <div className="lab-plan-steps">
              {steps.map((s, i) => (
                <span key={s.id} className={`lab-plan-step ${i < cut ? "frozen" : i === cut ? "patched" : "rerun"}`}>
                  {i < cut ? <Lock size={11} aria-hidden="true" /> : i === cut ? <Wrench size={11} aria-hidden="true" /> : <Repeat size={11} aria-hidden="true" />}
                  {s.label}<span className="dim">{i < cut ? "reused" : i === cut ? "patched" : "re-run"}</span>
                </span>
              ))}
            </div>
          </div>
        ) : null}
      </div>
      {why ? <p className="small muted">{why}</p> : null}
      <ErrorBox message={error} />
      {busy ? (
        <div className="lab-live" aria-live="polite">
          <div className="row between small"><span>{job?.message || "Starting replays…"}</span><span className="mono">{job ? `${job.progress_done}/${job.progress_total}` : ""}</span></div>
          <Progress done={job?.progress_done ?? 0} total={job?.progress_total ?? 0} label="Replays finished" />
          <div className="lab-rows">
            <span className="small muted">With the fix</span><ReplayDots replays={live?.replays ?? []} kind="intervention" planned={n} label="Fix replays so far" />
            <span className="small muted">Control, no fix</span><ReplayDots replays={live?.replays ?? []} kind="control" planned={m} label="Control replays so far" />
          </div>
        </div>
      ) : null}
    </Card>
  );
}
