import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import type { Stats } from "../types";
import { LoadingSkeleton, ErrorState } from "../components/States";

export function Evidence() {
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
        <LoadingSkeleton rows={6} />
      </div>
    );

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Proposal-stage POC evidence</h1>
          <p className="page-subtitle">
            Guide §12: "the panel should ask to see the evidence, not a description of it." This screen is the
            index — click through to <code className="mono" style={{ fontSize: 11 }}>dev/spikes/poc/*.json</code>{" "}
            on disk, or filter the runs list by spike, to see the raw output this console is built from.
          </p>
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {stats.spikes.map((s) => (
          <div key={s.id} className="card card-pad fade-in" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 14, flexWrap: "wrap" }}>
            <div>
              <div style={{ fontWeight: 700, fontSize: 13.5 }}>{s.name}</div>
              <div className="text-secondary" style={{ fontSize: 12.5, marginTop: 2 }}>
                {s.result}
              </div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <span className="text-muted" style={{ fontSize: 12 }}>
                {s.n_cases} case{s.n_cases === 1 ? "" : "s"}
              </span>
              <Link to={`/runs?spike=${encodeURIComponent(s.id.replace("spike", "spike "))}`} className="btn btn-ghost" style={{ fontSize: 12 }}>
                View runs →
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
