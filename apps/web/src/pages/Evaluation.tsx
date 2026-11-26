import { Sigma } from "lucide-react";
import { useState } from "react";
import { api } from "../api";
import { Card, Empty, ErrorBox, Loading, Notice, PageHeader } from "../components/ui";
import { faultLabel } from "../format";
import { useLoad } from "../hooks";
import type { EvalMetrics, Evaluation as EvaluationData, Rate } from "../types";
import "../styles/pages/lab.css";

const METHODS: [string, string][] = [
  ["last_agent", "Last agent (where it showed)"],
  ["earliest_check", "Earliest failing check"],
  ["granite_rank", "Granite ranking"],
  ["granite_verified", "Granite with verification"],
];
const LEVELS: [string, string][] = [["100", "100%"], ["60", "60%"], ["40", "40%"]];

const pct = (x: number | null | undefined) => (x === null || x === undefined ? "n/a" : `${Math.round(x * 100)}%`);

/** A rate as "k/n (p%)" with its Wilson 95% interval drawn as a bar. */
export function RateCell({ r, best }: { r?: Rate | null; best?: boolean }) {
  if (!r || !r.n) return <span className="dim">n/a</span>;
  const [lo, hi] = r.ci95;
  return (
    <span className="eval-cell">
      <span className={best ? "eval-best" : undefined}>{r.k}/{r.n} <span className="mono">({pct(r.rate)})</span></span>
      <span className="eval-interval" role="img" aria-label={`95% interval ${pct(lo)} to ${pct(hi)}`}>
        <i style={{ left: `${lo * 100}%`, width: `${(hi - lo) * 100}%` }} /><b style={{ left: `${(r.rate ?? 0) * 100}%` }} />
      </span>
      <span className="small dim mono">{pct(lo)}–{pct(hi)}</span>
    </span>
  );
}

function top1(m: EvalMetrics, level: string, method: string): Rate | undefined {
  return m.top1?.[level]?.[method] as Rate | undefined;
}

function Results({ e }: { e: EvaluationData }) {
  const m = e.metrics;
  const nd = m.nondeterminism ?? {};
  const meta = e.meta;
  const expected = (meta.n_tasks ?? 0) * (1 + (meta.faults?.length ?? 0));
  return (
    <>
      {e.rows.length < expected ? (
        <Notice tone="warn" title="Incomplete run">{e.rows.length} of {expected} runs are in this file; the numbers below cover only those.</Notice>
      ) : null}
      {meta.mode !== "live" ? <Notice title="Replayed, not live">These numbers come from saved model answers.</Notice> : null}
      <Card title="Detection" icon={Sigma} sub="does a completed run with a wrong answer get flagged, and do clean runs stay quiet?">
        <div className="eval-headline">
          <div className="eval-stat"><span className="eyebrow">Faulty runs detected</span><RateCell r={m.detection} /></div>
          {Object.entries(m.detection_by_fault ?? {}).map(([f, r]) => (
            <div key={f} className="eval-stat"><span className="eyebrow">{faultLabel(f)}</span><RateCell r={r} /></div>
          ))}
          <div className="eval-stat"><span className="eyebrow">Clean runs flagged</span><RateCell r={m.clean_runs_with_finding} />
            <span className="small muted">each one is a false alarm or a genuine model error; read the run to tell</span></div>
        </div>
      </Card>
      <Card title="Where did it begin? Top-1 accuracy" sub="share of detected faulty runs where the method names the injected step, by share of step checks kept">
        <div className="table-wrap">
          <table>
            <caption className="sr-only">Top-1 attribution by method and step-check coverage</caption>
            <thead><tr><th scope="col">Method</th>{LEVELS.map(([, l]) => <th key={l} scope="col">{l} of step checks</th>)}</tr></thead>
            <tbody>
              {METHODS.map(([key, name]) => (
                <tr key={key}>
                  <th scope="row">{name}</th>
                  {LEVELS.map(([lv]) => {
                    const r = top1(m, lv, key);
                    const bestRate = Math.max(...METHODS.map(([k]) => top1(m, lv, k)?.rate ?? -1));
                    return <td key={lv}><RateCell r={r} best={r?.rate === bestRate && bestRate >= 0} /></td>;
                  })}
                </tr>
              ))}
              <tr>
                <th scope="row">LLM judge (sees the whole trace, no checks)</th>
                <td><RateCell r={m.llm_judge_top1} /></td><td className="dim">not run</td><td className="dim">not run</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="small muted">Bold marks the highest rate in a column, ties included. With checks removed, Granite can only replay a step whose remaining checks say what its output should be.</p>
      </Card>
      <Card title="Why controls: confirmations by chance" sub="a placebo patch changes nothing; any confirmation there is luck">
        <div className="table-wrap">
          <table>
            <caption className="sr-only">Confirmations by rule VR-1 and by a single replay</caption>
            <thead><tr><th scope="col">Case</th><th scope="col">VR-1 (5 with the fix, 2 without)</th><th scope="col">One replay, no control</th></tr></thead>
            <tbody>
              <tr><th scope="row">Placebo on an innocent step (should be 0)</th>
                <td><RateCell r={nd.placebo_vr1_confirms} /></td><td><RateCell r={nd.placebo_single_replay_confirms} /></td></tr>
              <tr><th scope="row">True origin (should be high)</th>
                <td><RateCell r={nd.origin_vr1_confirms} /></td><td><RateCell r={nd.origin_single_replay_confirms} /></td></tr>
            </tbody>
          </table>
        </div>
      </Card>
      <Card title="Protocol">
        <div className="eval-provenance small">
          <span>Pre-registration <span className="mono">research/eval/prereg-v2.md</span>, SHA-256 <span className="mono">{meta.prereg_sha256?.slice(0, 16)}</span></span>
          <span>Model <span className="mono">{meta.model}</span>, {meta.mode} answers</span>
          <span>{meta.n_tasks} tasks × {(meta.faults ?? []).map(faultLabel).join(", ")} + clean</span>
          <span>N={meta.n}, M={meta.m}, budget {meta.budget} replays</span>
          <span>Commit <span className="mono">{meta.git_head?.slice(0, 10)}</span>{meta.git_dirty ? " (uncommitted changes)" : ""}</span>
        </div>
        <p className="small muted">Ten tasks, three faults written by the team, one small model: an early test, not a benchmark. The faults and the checks that catch them were designed together; the coverage columns measure how much that matters.</p>
      </Card>
    </>
  );
}

/** Evaluation: benchmark results written by the harness, shown as measured (ties and losses included). */
export function Evaluation() {
  const list = useLoad(() => api.evaluations(), []);
  const [picked, setPicked] = useState("");
  const id = picked || list.data?.[0]?.id || "";
  const one = useLoad(() => (id ? api.evaluation(id) : Promise.resolve(null)), [id]);
  return (
    <div className="page eval-page">
      <PageHeader title="Evaluation" sub="How well detection, attribution and verification work across many runs, against simple baselines." />
      {list.loading && !list.data ? <Loading /> : list.error ? <ErrorBox message={list.error} onRetry={list.reload} />
        : !list.data?.length ? (
          <Empty title="No results yet">Run <span className="mono">python research/eval/benchmark_v0.py</span>; its result file appears here.</Empty>
        ) : (
          <>
            {list.data.length > 1 ? (
              <div className="field">
                <label htmlFor="eval-pick">Result</label>
                <select id="eval-pick" value={id} onChange={(e) => setPicked(e.target.value)}>
                  {list.data.map((e) => <option key={e.id} value={e.id}>{e.id} ({e.mode}, {e.runs} runs{e.complete ? "" : ", incomplete"})</option>)}
                </select>
              </div>
            ) : null}
            {one.loading && !one.data ? <Loading /> : one.error ? <ErrorBox message={one.error} onRetry={one.reload} />
              : one.data ? <Results e={one.data} /> : null}
          </>
        )}
    </div>
  );
}
