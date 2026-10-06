import { useNavigate } from "react-router-dom";
import type { RunSummary } from "../types";
import { StatusBadge } from "./StatusBadge";

export function RunsTable({ runs }: { runs: RunSummary[] }) {
  const nav = useNavigate();

  return (
    <div className="card fade-in" style={{ overflow: "hidden" }}>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", minWidth: 760 }}>
          <thead>
            <tr style={{ borderBottom: "1px solid var(--border)" }}>
              {["Spike", "Scenario", "Question / case", "Framework", "Status"].map((h) => (
                <th
                  key={h}
                  style={{
                    textAlign: "left",
                    padding: "11px 16px",
                    fontSize: 11.5,
                    fontWeight: 700,
                    color: "var(--text-muted)",
                    textTransform: "uppercase",
                    letterSpacing: "0.04em",
                  }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {runs.map((r) => (
              <tr
                key={r.id}
                onClick={() => nav(`/runs/${r.id}`)}
                style={{ borderBottom: "1px solid var(--border)", cursor: "pointer" }}
                className="run-row"
              >
                <td style={{ padding: "12px 16px", fontSize: 12.5, color: "var(--accent)", fontWeight: 700, whiteSpace: "nowrap" }}>
                  {r.spike}
                </td>
                <td style={{ padding: "12px 16px", fontSize: 12.5, color: "var(--text-secondary)", maxWidth: 220 }}>{r.scenario}</td>
                <td style={{ padding: "12px 16px", fontSize: 13, maxWidth: 340 }}>
                  <div
                    style={{
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {r.question}
                  </div>
                </td>
                <td style={{ padding: "12px 16px", fontSize: 12, color: "var(--text-secondary)", whiteSpace: "nowrap" }}>
                  {r.framework}
                </td>
                <td style={{ padding: "12px 16px" }}>
                  <StatusBadge status={r.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <style>{`.run-row:hover { background: var(--surface-hover); }`}</style>
    </div>
  );
}
