import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../api";
import type { RunDetail as RunDetailT } from "../types";
import { StatusBadge } from "../components/StatusBadge";
import { GraphView } from "../components/GraphView";
import { EvidencePanel } from "../components/EvidencePanel";
import { RepairReplayReport } from "../components/RepairReplayReport";
import { LoadingSkeleton, ErrorState } from "../components/States";

export function RunDetailPage() {
  const { id, tab } = useParams<{ id: string; tab?: string }>();
  const [run, setRun] = useState<RunDetailT | null>(null);
  const [error, setError] = useState<string | null>(null);
  const activeTab = tab === "repair" ? "repair" : "trace";

  const load = () => {
    if (!id) return;
    setError(null);
    setRun(null);
    api
      .run(id)
      .then(setRun)
      .catch((e) => setError(String(e)));
  };

  useEffect(load, [id]);

  if (error)
    return (
      <div className="page">
        <ErrorState message={error} onRetry={load} />
      </div>
    );
  if (!run)
    return (
      <div className="page">
        <LoadingSkeleton rows={6} />
      </div>
    );

  return (
    <div className="page">
      <Link to="/runs" className="text-muted" style={{ fontSize: 12.5, display: "inline-block", marginBottom: 10 }}>
        ← back to runs
      </Link>
      <div className="page-header">
        <div style={{ minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6, flexWrap: "wrap" }}>
            <span className="text-secondary mono" style={{ fontSize: 12 }}>
              {run.spike}
            </span>
            <StatusBadge status={run.status} />
          </div>
          <h1 className="page-title" style={{ maxWidth: 760 }}>
            {run.question}
          </h1>
          <p className="page-subtitle">
            {run.scenario} · {run.framework}
          </p>
          {run.final_answer && (
            <p className="text-secondary" style={{ fontSize: 12.5, marginTop: 8 }}>
              <b>Final answer:</b> {run.final_answer}
            </p>
          )}
        </div>
      </div>

      <div className="tabs">
        <Link to={`/runs/${id}`} className={`tab ${activeTab === "trace" ? "active" : ""}`}>
          Trace & graph view
        </Link>
        <Link to={`/runs/${id}/repair`} className={`tab ${activeTab === "repair" ? "active" : ""}`}>
          Repair & replay report
        </Link>
      </div>

      {activeTab === "trace" ? (
        <div style={{ display: "grid", gridTemplateColumns: "1.4fr 1fr", gap: 20, alignItems: "start" }}>
          <div className="card card-pad">
            <div style={{ fontWeight: 700, fontSize: 13.5, marginBottom: 14 }}>Execution graph</div>
            <GraphView graph={run.graph} />
          </div>
          <EvidencePanel run={run} />
        </div>
      ) : (
        <RepairReplayReport run={run} />
      )}
    </div>
  );
}
