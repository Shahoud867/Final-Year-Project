import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api } from "../api";
import type { RunSummary } from "../types";
import { RunsTable } from "../components/RunsTable";
import { LoadingSkeleton, EmptyState, ErrorState } from "../components/States";

const SPIKE_FILTERS = ["All", "Spike 1", "Spike 2", "Spike 3", "Spike 3b", "Spike 4", "Spike 5", "Spike 6", "Spike 7", "Spike 8"];
const STATUS_FILTERS: { value: string; label: string }[] = [
  { value: "", label: "All statuses" },
  { value: "attributed_correct", label: "Correctly attributed" },
  { value: "attributed_partial", label: "Agent correct, step off" },
  { value: "attributed_incorrect", label: "Misattributed" },
  { value: "clean_no_fault", label: "Clean / no fault" },
  { value: "self_corrected", label: "Self-corrected" },
  { value: "fault_propagated", label: "Fault propagated" },
  { value: "repaired_verified", label: "Repaired & verified" },
  { value: "repair_failed", label: "Repair failed" },
  { value: "cyclic_bounded", label: "Cycle bounded" },
  { value: "classified_correct", label: "Classified correctly" },
  { value: "classified_incorrect", label: "Misclassified" },
];

export function RunsList() {
  const [searchParams] = useSearchParams();
  const initialSpike = searchParams.get("spike");
  const [runs, setRuns] = useState<RunSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [spike, setSpike] = useState(
    initialSpike && SPIKE_FILTERS.some((s) => s.toLowerCase() === initialSpike.toLowerCase())
      ? SPIKE_FILTERS.find((s) => s.toLowerCase() === initialSpike.toLowerCase())!
      : "All"
  );
  const [status, setStatus] = useState("");
  const [q, setQ] = useState("");

  const load = () => {
    setError(null);
    api
      .runs({ spike: spike === "All" ? undefined : spike, status: status || undefined, q: q || undefined })
      .then(setRuns)
      .catch((e) => setError(String(e)));
  };

  useEffect(load, [spike, status, q]);

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Runs & diagnoses</h1>
          <p className="page-subtitle">
            Every diagnosis run generated from the 8 real proposal-stage spikes — reproduction cases, fault
            injections, silent-failure checks, cyclic-graph handling, and repair generations.
          </p>
        </div>
      </div>

      <div style={{ display: "flex", gap: 10, marginBottom: 16, flexWrap: "wrap", alignItems: "center" }}>
        <input
          className="input"
          placeholder="Search question or scenario…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          style={{ minWidth: 240 }}
        />
        <select className="input" value={spike} onChange={(e) => setSpike(e.target.value)}>
          {SPIKE_FILTERS.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <select className="input" value={status} onChange={(e) => setStatus(e.target.value)}>
          {STATUS_FILTERS.map((s) => (
            <option key={s.value} value={s.value}>
              {s.label}
            </option>
          ))}
        </select>
        {runs && (
          <span className="text-muted" style={{ fontSize: 12.5 }}>
            {runs.length} run{runs.length === 1 ? "" : "s"}
          </span>
        )}
      </div>

      {error && <ErrorState message={error} onRetry={load} />}
      {!error && !runs && <LoadingSkeleton rows={8} />}
      {!error && runs && runs.length === 0 && (
        <EmptyState title="No runs match these filters" sub="Try clearing the search or status filter." />
      )}
      {!error && runs && runs.length > 0 && <RunsTable runs={runs} />}
    </div>
  );
}
