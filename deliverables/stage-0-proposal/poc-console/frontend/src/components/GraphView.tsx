import type { Graph } from "../types";

const AGENT_COLORS = ["#6ea8e0", "#e0b555", "#52c98c", "#c58ee0", "#52b8c9", "#e08a55", "#e06868", "#9aa6c9"];

function colorFor(agent: string) {
  let hash = 0;
  for (let i = 0; i < agent.length; i++) hash = (hash * 31 + agent.charCodeAt(i)) >>> 0;
  return AGENT_COLORS[hash % AGENT_COLORS.length];
}

/**
 * Renders the execution graph as a vertical timeline: one card per node, in
 * order, connected by a spine. This matches what every trace in the real
 * spike data actually is -- a (mostly) linear dependency chain, occasionally
 * revisiting a node under a cycle -- and stays legible at any node count,
 * unlike a force-directed layout with 20+ nodes.
 */
export function GraphView({ graph }: { graph: Graph }) {
  const seen = new Map<string, number>();

  return (
    <div style={{ position: "relative", paddingLeft: 28 }}>
      <div
        style={{
          position: "absolute",
          left: 9,
          top: 10,
          bottom: 10,
          width: 2,
          background: "var(--border-strong)",
        }}
      />
      {graph.nodes.map((n, i) => {
        const revisitCount = (seen.get(n.agent) ?? 0) + 1;
        seen.set(n.agent, revisitCount);
        const color = colorFor(n.agent);
        const isSpecial = n.is_culprit || n.is_fault_injected;

        return (
          <div key={`${n.id}-${i}`} style={{ position: "relative", marginBottom: 10 }} className="fade-in">
            <div
              style={{
                position: "absolute",
                left: -28 + 3,
                top: 14,
                width: 12,
                height: 12,
                borderRadius: "50%",
                background: color,
                border: "2px solid var(--bg-elevated)",
                boxShadow: isSpecial ? `0 0 0 3px ${n.is_culprit ? "var(--red-soft)" : "var(--amber-soft)"}` : "none",
              }}
            />
            <div
              className="card"
              style={{
                padding: "10px 14px",
                borderColor: n.is_culprit ? "var(--red)" : n.is_fault_injected ? "var(--amber)" : "var(--border)",
                borderLeftWidth: isSpecial ? 3 : 1,
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4, flexWrap: "wrap" }}>
                <span style={{ fontWeight: 700, fontSize: 12.5, color }}>{n.agent}</span>
                <span className="text-muted mono" style={{ fontSize: 10.5 }}>
                  {n.role}
                </span>
                {revisitCount > 1 && (
                  <span className="pill" style={{ background: "var(--surface-hover)", color: "var(--text-secondary)", fontSize: 10 }}>
                    revisit ×{revisitCount}
                  </span>
                )}
                {n.is_culprit && (
                  <span className="pill" style={{ color: "var(--red)", background: "var(--red-soft)", fontSize: 10 }}>
                    culprit step
                  </span>
                )}
                {n.is_fault_injected && (
                  <span className="pill" style={{ color: "var(--amber)", background: "var(--amber-soft)", fontSize: 10 }}>
                    fault injected here
                  </span>
                )}
              </div>
              {n.label && (
                <div className="text-secondary" style={{ fontSize: 12.5, lineHeight: 1.5 }}>
                  {n.label}
                </div>
              )}
            </div>
          </div>
        );
      })}
      {graph.nodes.length === 0 && (
        <div className="text-muted" style={{ fontSize: 13 }}>
          No trace nodes recorded for this run.
        </div>
      )}
    </div>
  );
}
