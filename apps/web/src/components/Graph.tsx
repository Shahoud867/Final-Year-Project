import type { Graph as GraphData } from "../types";

const W = 132, H = 46, GAP = 30;

/** Left-to-right pipeline diagram of one run. Failed steps are filled red; the step where the symptom showed is marked. */
export function Graph({ graph, onSelect }: { graph: GraphData; onSelect?: (id: string) => void }) {
  const pos = new Map(graph.nodes.map((n, i) => [n.id, { x: 10 + i * (W + GAP), y: 30 }]));
  const width = 20 + graph.nodes.length * (W + GAP) - GAP;
  const summary = graph.nodes.map((n) => `${n.label}: ${n.status}`).join(", ");
  return (
    <div className="table-wrap">
      <svg className="graph" viewBox={`0 0 ${width} ${H + 90}`} width="100%" style={{ minWidth: 640, maxWidth: width }}
           role="group" aria-label={`Run graph. ${summary}`}>
        <defs>
          <marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">
            <path d="M0 0L8 4L0 8z" fill="var(--muted)" />
          </marker>
        </defs>
        {graph.edges.map((e, i) => {
          const a = pos.get(e.source), b = pos.get(e.target);
          if (!a || !b) return null;
          const span = Math.abs(b.x - a.x) > W + GAP;
          const x1 = a.x + W, x2 = b.x, y = a.y + H / 2;
          const d = span
            ? `M${x1 - W / 2} ${a.y + H} C${x1 - W / 2} ${a.y + H + 40} ${x2 + W / 2} ${b.y + H + 40} ${x2 + W / 2} ${b.y + H + 3}`
            : `M${x1} ${y} L${x2 - 3} ${y}`;
          return <path key={i} className="edge" d={d} markerEnd="url(#arrow)"><title>{e.field}</title></path>;
        })}
        {graph.nodes.map((n) => {
          const p = pos.get(n.id)!;
          const cls = n.kind === "input" ? "input" : n.status;
          return (
            <g key={n.id} className={`node ${cls}`} transform={`translate(${p.x},${p.y})`}
               tabIndex={n.kind === "input" ? undefined : 0} role={onSelect && n.kind !== "input" ? "button" : undefined}
               onClick={() => onSelect?.(n.id)} onKeyDown={(e) => e.key === "Enter" && onSelect?.(n.id)}>
              <rect width={W} height={H} rx={9} />
              <text x={W / 2} y={19} textAnchor="middle" fontWeight={600}>{n.label}</text>
              <text x={W / 2} y={35} textAnchor="middle" className="muted">
                {n.kind === "input" ? "input" : `${n.kind} · ${n.status}${n.symptom ? " · symptom" : ""}`}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
