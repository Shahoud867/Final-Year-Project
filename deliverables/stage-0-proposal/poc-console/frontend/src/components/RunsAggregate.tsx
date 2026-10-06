import type { RunStatus, RunSummary } from "../types";

const STATUS_META: Record<RunStatus, { label: string; color: string }> = {
  attributed_correct: { label: "Correctly attributed", color: "var(--green)" },
  attributed_partial: { label: "Agent correct, step off", color: "var(--amber)" },
  attributed_incorrect: { label: "Misattributed", color: "var(--red)" },
  clean_no_fault: { label: "Clean / no fault", color: "var(--blue)" },
  self_corrected: { label: "Self-corrected", color: "var(--teal)" },
  fault_propagated: { label: "Fault propagated", color: "var(--orange)" },
  repaired_verified: { label: "Repaired & verified", color: "var(--green)" },
  repair_failed: { label: "Repair failed", color: "var(--red)" },
  cyclic_bounded: { label: "Cycle bounded", color: "var(--blue)" },
  classified_correct: { label: "Classified correctly", color: "var(--green)" },
  classified_incorrect: { label: "Misclassified", color: "var(--red)" },
};

/**
 * Collection-level view over whatever set of runs is currently in scope.
 * Recomputes with the active filters so the numbers always describe exactly
 * what the table below is showing -- never a stale total.
 */
export function RunsAggregate({ runs }: { runs: RunSummary[] }) {
  if (runs.length === 0) return null;

  const bySpike = new Map<string, number>();
  const byStatus = new Map<RunStatus, number>();
  for (const r of runs) {
    bySpike.set(r.spike, (bySpike.get(r.spike) ?? 0) + 1);
    byStatus.set(r.status, (byStatus.get(r.status) ?? 0) + 1);
  }

  const spikes = [...bySpike.entries()].sort((a, b) =>
    a[0].localeCompare(b[0], undefined, { numeric: true })
  );
  const statuses = [...byStatus.entries()].sort((a, b) => b[1] - a[1]);

  return (
    <div className="card card-pad fade-in" style={{ marginBottom: 16 }}>
      <div style={{ display: "flex", gap: 24, flexWrap: "wrap", alignItems: "flex-start" }}>
        <div style={{ flex: "1 1 300px", minWidth: 0 }}>
          <div
            className="text-muted"
            style={{ fontSize: 10.5, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}
          >
            Outcome distribution · {runs.length} run{runs.length === 1 ? "" : "s"} in view
          </div>

          <div style={{ display: "flex", height: 8, borderRadius: 4, overflow: "hidden", marginBottom: 10 }}>
            {statuses.map(([status, count]) => (
              <div
                key={status}
                title={`${STATUS_META[status]?.label ?? status}: ${count}`}
                style={{
                  width: `${(count / runs.length) * 100}%`,
                  background: STATUS_META[status]?.color ?? "var(--text-muted)",
                }}
              />
            ))}
          </div>

          <div style={{ display: "flex", flexWrap: "wrap", gap: "6px 14px" }}>
            {statuses.map(([status, count]) => (
              <div key={status} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 12 }}>
                <span
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: 2,
                    background: STATUS_META[status]?.color ?? "var(--text-muted)",
                    flexShrink: 0,
                  }}
                />
                <span className="text-secondary">{STATUS_META[status]?.label ?? status}</span>
                <span className="mono" style={{ fontWeight: 700 }}>{count}</span>
              </div>
            ))}
          </div>
        </div>

        <div style={{ flex: "0 1 auto", minWidth: 0 }}>
          <div
            className="text-muted"
            style={{ fontSize: 10.5, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em", marginBottom: 8 }}
          >
            By spike
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {spikes.map(([spike, count]) => (
              <span
                key={spike}
                className="pill"
                style={{ background: "var(--surface-hover)", color: "var(--text-secondary)", fontSize: 11.5 }}
              >
                {spike}
                <span className="mono" style={{ fontWeight: 700, color: "var(--accent)" }}>{count}</span>
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
