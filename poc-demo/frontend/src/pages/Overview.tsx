import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import type { Stats } from "../types";
import { StatTile } from "../components/StatTile";
import { LoadingSkeleton, ErrorState } from "../components/States";

export function Overview() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    setError(null);
    api
      .stats()
      .then(setStats)
      .catch((e) => setError(String(e)));
  };

  useEffect(load, []);

  if (error) return <div className="page"><ErrorState message={error} onRetry={load} /></div>;
  if (!stats)
    return (
      <div className="page">
        <LoadingSkeleton rows={3} />
      </div>
    );

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Granite Diagnosis Console</h1>
          <p className="page-subtitle">
            Proposal-defense proof of concept — every metric below is computed live from the 8 committed spike
            output files, not simulated. {stats.total_runs} diagnosis runs across {stats.n_spikes} spikes.
          </p>
        </div>
        <Link to="/runs" className="btn btn-primary">
          Browse all runs →
        </Link>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: 14, marginBottom: 26 }}>
        <StatTile label="Agent accuracy" value={`${(stats.agent_accuracy * 100).toFixed(0)}%`} sub={`n=${stats.n_reproduction_cases}, Spike 1`} tone="good" />
        <StatTile
          label="Step accuracy"
          value={`${(stats.step_accuracy_type_safe * 100).toFixed(1)}%`}
          sub="n=8, corrected comparison — see flag below"
          tone="warn"
          flag="Raw file reports 0.0% due to a str/int type-mismatch bug in the scoring script — see the discrepancy note below."
        />
        <StatTile
          label="Repair success rate"
          value={`${(stats.repair_success_rate * 100).toFixed(1)}%`}
          sub={`n=${stats.repair_n_cases}, Spike 8`}
          tone="good"
        />
        <StatTile
          label="Recovery via replay"
          value={stats.recovery_success ? "1/1" : "0/1"}
          sub="Spike 5 — mechanism validated"
          tone="good"
        />
        <StatTile
          label="Cyclic graphs bounded"
          value={`${stats.cyclic_cases_bounded}/${stats.cyclic_cases_total}`}
          sub="Spike 6, incl. control run"
          tone="good"
        />
        <StatTile
          label="Preventive classifier"
          value={`${(stats.preventive_classifier.precision * 100).toFixed(0)}%`}
          sub="Spike 7 — honest negative"
          tone="bad"
        />
      </div>

      {stats.step_accuracy_discrepancy_flag && (
        <div
          className="card card-pad fade-in"
          style={{ marginBottom: 26, borderColor: "var(--amber)", display: "flex", gap: 12 }}
        >
          <div style={{ fontSize: 20 }}>⚑</div>
          <div>
            <div style={{ fontWeight: 700, marginBottom: 4 }}>Data discrepancy found while building this console</div>
            <div className="text-secondary" style={{ fontSize: 13, lineHeight: 1.6 }}>
              <code className="mono">poc_spike1_errorprobe_repro_output.json</code>'s own <code className="mono">summary.step_accuracy</code> field
              reads <b>0.0</b> — every case's <code className="mono">step_correct</code> flag is <code className="mono">false</code> — while the
              documentation throughout this project (audit, slides, question bank) states <b>12.5%</b>. The likely cause, visible in the raw
              data: ground-truth step indices are stored as strings (e.g. <code className="mono">"5"</code>) while predicted steps are ints
              (<code className="mono">5</code>), so <code className="mono">pred_step == gt_step</code> silently returns <code className="mono">False</code> even
              when the values are numerically equal — case 6 is exactly this: <code className="mono">gt_step="5"</code>, <code className="mono">pred_step=5</code>.
              This console reports both the raw file's number and a type-safe recomputation side by side, rather than picking one silently.
            </div>
          </div>
        </div>
      )}

      <div className="card card-pad">
        <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 4 }}>Honest findings, led with — not buried</div>
        <div className="text-secondary" style={{ fontSize: 12.5, marginBottom: 14 }}>
          Per the guide's own words: "a POC that disproved the assumption is usually more valuable."
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          <div style={{ padding: "12px 14px", background: "var(--red-soft)", borderRadius: 10 }}>
            <div style={{ fontWeight: 700, fontSize: 13, color: "var(--red)", marginBottom: 4 }}>
              Spike 7 — Preventive classifier
            </div>
            <div className="text-secondary" style={{ fontSize: 12.5, lineHeight: 1.5 }}>{stats.preventive_classifier.honest_caveat}</div>
          </div>
          <div style={{ padding: "12px 14px", background: "var(--amber-soft)", borderRadius: 10 }}>
            <div style={{ fontWeight: 700, fontSize: 13, color: "var(--amber)", marginBottom: 4 }}>
              Spike 8 — Repair Agent, 2 of 6 failures
            </div>
            <div className="text-secondary" style={{ fontSize: 12.5, lineHeight: 1.5 }}>
              Both failures share one root cause: the model returned the downstream computed result instead of
              the specific corrected parameter (R17) — an interface-specification issue, not a reasoning gap.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
