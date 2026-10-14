import { useEffect, useRef, useState } from "react";
import type { KeyboardEvent } from "react";
import { stepKind } from "../format";
import type { Graph as GraphData, GraphNode } from "../types";

/** Overlay on a node: suspected origin, origin confirmed by replay, hypothesis refuted, or the injected fault (ground truth). */
export type NodeMark = "suspect" | "origin" | "refuted" | "fault";

export interface GraphProps {
  graph: GraphData;
  onSelect?: (id: string) => void;
  selected?: string | null;
  /** Ordered step ids of a data-flow path to highlight, for example a hypothesis's recorded provenance path. */
  path?: string[];
  marks?: Record<string, NodeMark>;
  /** "auto" draws left to right when the container is wide enough and top to bottom otherwise. */
  layout?: "auto" | "horizontal" | "vertical";
  /** Small nodes for previews and side panels (always top to bottom). */
  dense?: boolean;
  /** Draw the workflow definition only: no check status, because nothing has run. */
  plain?: boolean;
  /** Second line of a node, replacing the status words (for example the step's task). */
  notes?: Record<string, string>;
  /** A job is in flight. The server reports no per-step progress, so the whole pipeline shows one moving state. */
  running?: boolean;
  legend?: boolean;
  label?: string;
}

const PAD = 12, MIN_W = 132, MAX_W = 180, MIN_GAP = 26, FALLBACK_WIDTH = 1120;
const STATUS_WORDS: Record<string, string> = { ok: "no failed check", failed: "check failed", error: "errored" };
const MARK_WORDS: Record<NodeMark, string> = { suspect: "suspect", origin: "origin confirmed", refuted: "refuted", fault: "fault injected" };

interface Box { x: number; y: number }
interface Merged { source: string; target: string; fields: string[] }

function merge(graph: GraphData): Merged[] {
  const by = new Map<string, Merged>();
  for (const e of graph.edges) {
    const key = `${e.source}>${e.target}`;
    const hit = by.get(key);
    if (hit) hit.fields.push(e.field);
    else by.set(key, { source: e.source, target: e.target, fields: [e.field] });
  }
  return [...by.values()];
}

const clip = (text: string, max: number): string => (text.length > max ? `${text.slice(0, Math.max(1, max - 1))}…` : text);

function Glyph({ status, x, y }: { status: string; x: number; y: number }) {
  const d = status === "ok" ? "M-3 0.2L-0.8 2.4L3.2 -2.2" : status === "failed" ? "M-2.6 -2.6L2.6 2.6M2.6 -2.6L-2.6 2.6" : "M0 -3.2V0.6M0 3V3.1";
  return <g className={`glyph ${status}`} transform={`translate(${x},${y})`} aria-hidden="true"><circle r={7} /><path d={d} /></g>;
}

const tagWidth = (text: string): number => text.length * 6.1 + 12;

/** Small labels above a node, laid out leftwards from `right`. */
function Tags({ tags, right, y }: { tags: [string, string][]; right: number; y: number }) {
  return (
    <>
      {tags.map(([cls, text], i) => {
        const w = tagWidth(text);
        const after = tags.slice(i + 1).reduce((sum, [, t]) => sum + tagWidth(t) + 4, 0);
        return (
          <g key={cls} className={`tag ${cls}`} transform={`translate(${right - after - w},${y})`} aria-hidden="true">
            <rect width={w} height={15} rx={7.5} /><text x={w / 2} y={10.6} textAnchor="middle">{text}</text>
          </g>
        );
      })}
    </>
  );
}

/**
 * The run as a pipeline: one node per agent step, edges for the recorded data flow. A red node failed a check, the
 * "symptom" tag marks where the wrong outcome showed, and overlays mark the suspected or confirmed origin. Every
 * node is a button for keyboard and pointer; the same facts are in the tables next to it.
 */
export function Graph({ graph, onSelect, selected, path, marks, layout = "auto", dense, plain, notes, running, legend, label }: GraphProps) {
  const wrap = useRef<HTMLDivElement>(null);
  const [measured, setMeasured] = useState(0);
  useEffect(() => {
    const el = wrap.current;
    if (!el) return;
    const read = () => setMeasured(el.clientWidth);
    read();
    if (typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(read);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const nodes = graph.nodes, n = nodes.length;
  const cw = measured > 0 ? measured : FALLBACK_WIDTH;
  const fits = cw >= n * MIN_W + (n - 1) * MIN_GAP + 2 * PAD;
  const horizontal = !dense && (layout === "horizontal" || (layout === "auto" && fits));
  const index = new Map(nodes.map((nd, i) => [nd.id, i]));
  const edges = merge(graph).filter((e) => index.has(e.source) && index.has(e.target));
  const onPath = (e: Merged) => !!path && path.some((id, i) => id === e.source && path[i + 1] === e.target);
  const span = (e: Merged) => Math.abs(index.get(e.target)! - index.get(e.source)!);
  const maxSpan = edges.reduce((m, e) => Math.max(m, span(e)), 1);

  // geometry, in real pixels (the drawing is never scaled, so text stays readable)
  const H = dense ? 36 : horizontal ? 56 : 52;
  const TOP = dense ? 20 : 26;
  let W: number, gap: number, x0: number, width: number, height: number;
  if (horizontal) {
    const avail = cw - 2 * PAD;
    W = Math.min(MAX_W, Math.max(MIN_W, (avail - (n - 1) * 44) / Math.max(n, 1)));
    gap = n > 1 ? Math.min(72, Math.max(MIN_GAP, (avail - n * W) / (n - 1))) : 0;
    x0 = Math.max(PAD, (cw - (n * W + (n - 1) * gap)) / 2);
    width = Math.max(cw, n * W + (n - 1) * gap + 2 * PAD);
    height = TOP + H + (maxSpan > 1 ? 30 + 12 * (maxSpan - 1) : 10);
  } else {
    const gutter = maxSpan > 1 ? 22 + 10 * Math.min(maxSpan - 1, 3) : 0;
    W = Math.max(120, Math.min(dense ? 300 : 340, cw - 2 * PAD - gutter));
    gap = dense ? 22 : 34;
    x0 = PAD;
    width = W + 2 * PAD + gutter;
    height = TOP + n * H + (n - 1) * gap + 8;
  }
  const at = (i: number): Box => (horizontal ? { x: x0 + i * (W + gap), y: TOP } : { x: x0, y: TOP + i * (H + gap) });
  const maxChars = Math.floor((W - 22 - (dense ? 62 : 0)) / 6.4);

  const summary = nodes.map((nd) => `${nd.label}: ${plain ? stepKind(nd.kind) : nd.status}`).join(", ");
  const key = (id: string) => (e: KeyboardEvent<SVGGElement>) => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onSelect?.(id); }
  };
  const confirmed = marks ? Object.values(marks).includes("origin") : false;

  function edgeEl(e: Merged, i: number) {
    const si = index.get(e.source)!, ti = index.get(e.target)!;
    const a = at(si), b = at(ti);
    const skip = span(e) > 1;
    const cls = `${skip ? " skip" : ""}${onPath(e) ? " on-path" : path ? " dim" : ""}`;
    const text = e.fields.length === 1 ? e.fields[0]! : `${e.fields.length} fields`;
    let d: string, arrow: string, lx = 0, ly = 0, anchor: "middle" | "end" = "middle", room = 0;
    if (horizontal && !skip) {
      const y = a.y + H / 2, x1 = a.x + W, x2 = b.x;
      d = `M${x1} ${y}L${x2 - 6} ${y}`;
      arrow = `M${x2 - 1} ${y}l-7 -3.6v7.2z`;
      lx = (x1 + x2) / 2; ly = y - 6; room = x2 - x1 - 8;
    } else if (horizontal) {
      const depth = 20 + 12 * (span(e) - 1), y = a.y + H, sx = a.x + W / 2 + 16, ex = b.x + W / 2 - 16;
      d = `M${sx} ${y}C${sx} ${y + depth} ${ex} ${y + depth} ${ex} ${y + 6}`;
      arrow = `M${ex} ${y + 1}l-3.6 7h7.2z`;
    } else if (!skip) {
      const x = a.x + W / 2, y1 = a.y + H, y2 = b.y;
      d = `M${x} ${y1}L${x} ${y2 - 6}`;
      arrow = `M${x} ${y2 - 1}l-3.6 -7h7.2z`;
      lx = x - 8; ly = (y1 + y2) / 2 + 3; anchor = "end"; room = dense ? 0 : W / 2 - 16; // left of the line: tags sit on the right
    } else {
      const bulge = 16 + 10 * Math.min(span(e) - 1, 3), x = a.x + W, sy = a.y + H / 2 + 8, ey = b.y + H / 2 - 8;
      d = `M${x} ${sy}C${x + bulge} ${sy} ${x + bulge} ${ey} ${x + 6} ${ey}`;
      arrow = `M${x + 1} ${ey}l7 -3.6v7.2z`;
    }
    return (
      <g key={i}>
        <path className={`edge${cls}`} d={d}><title>{`${e.source} → ${e.target}: ${e.fields.join(", ")}`}</title></path>
        <path className={`arrow${onPath(e) ? " on-path" : ""}${path && !onPath(e) ? " dim" : ""}`} d={arrow} />
        {room > text.length * 5.6 ? <text className="edge-label" x={lx} y={ly} textAnchor={anchor}>{text}</text> : null}
      </g>
    );
  }

  function nodeEl(nd: GraphNode, i: number) {
    const p = at(i);
    const input = nd.kind === "input";
    const mark = marks?.[nd.id];
    const state = input ? "input" : plain ? "idle" : nd.status;
    const clickable = !!onSelect && !input;
    const words = input ? "run input" : notes?.[nd.id] ?? (plain ? "" : STATUS_WORDS[nd.status] ?? nd.status);
    const tags: [string, string][] = [];
    if (nd.symptom && !plain) tags.push(["symptom", "symptom"]);
    if (mark) tags.push([mark, MARK_WORDS[mark]]);
    const name = `${nd.label}: ${stepKind(nd.kind)} step${plain || input ? "" : `, ${STATUS_WORDS[nd.status] ?? nd.status}`}`
      + `${nd.symptom && !plain ? ", symptom shows here" : ""}${mark ? `, ${MARK_WORDS[mark]}` : ""}`;
    const dim = path && !path.includes(nd.id) && !input ? " dim" : "";
    return (
      <g key={nd.id} className={`node ${state}${selected === nd.id ? " selected" : ""}${dim}`} transform={`translate(${p.x},${p.y})`}
         tabIndex={clickable ? 0 : undefined} role={clickable ? "button" : undefined} aria-label={clickable ? name : undefined}
         aria-pressed={clickable ? selected === nd.id : undefined}
         onClick={clickable ? () => onSelect?.(nd.id) : undefined} onKeyDown={clickable ? key(nd.id) : undefined}>
        {clickable ? null : <title>{name}</title>}
        <rect className="box" width={W} height={H} rx={9} />
        <rect className="bar" x={0} y={dense ? 8 : 12} width={3} height={H - (dense ? 16 : 24)} rx={1.5} />
        {mark ? <rect className={`ring ${mark}`} x={-4} y={-4} width={W + 8} height={H + 8} rx={12} /> : null}
        {dense ? (
          <>
            <text className="g-label" x={14} y={H / 2 + 4}>{clip(nd.label, maxChars)}</text>
            <text className="g-kind" x={W - (plain || input ? 12 : 30)} y={H / 2 + 3} textAnchor="end">{stepKind(nd.kind).toUpperCase()}</text>
          </>
        ) : (
          <>
            <text className="g-kind" x={14} y={horizontal ? 17 : 16}>{stepKind(nd.kind).toUpperCase()}</text>
            <text className="g-label" x={14} y={horizontal ? 33 : 31}>{clip(nd.label, maxChars)}</text>
            <text className="g-sub" x={14} y={horizontal ? 47 : 44}>{clip(words, Math.floor((W - 22) / 5.6))}</text>
          </>
        )}
        {!input && !plain ? <Glyph status={nd.status} x={W - 16} y={dense ? H / 2 : 16} /> : null}
        <Tags tags={tags} right={horizontal ? W / 2 + tags.reduce((s, [, t]) => s + tagWidth(t) + 4, -4) / 2 : W} y={-19} />
      </g>
    );
  }

  return (
    <div className="graph-wrap" ref={wrap}>
      <svg className={`graph${running ? " running" : ""}${confirmed ? " confirmed" : ""}`} width={width} height={height} viewBox={`0 0 ${width} ${height}`}
           role="group" aria-label={`${label ?? "Run graph"}. ${summary}`}>
        {edges.map(edgeEl)}
        {nodes.map(nodeEl)}
      </svg>
      {legend ? (
        <div className="graph-legend" aria-hidden="true">
          <span><i className="ok" />no failed check</span>
          <span><i className="failed" />check failed</span>
          <span><i className="error" />errored</span>
          <span><i className="suspect" />suspected origin</span>
          <span><i className="origin" />origin confirmed by replay</span>
        </div>
      ) : null}
    </div>
  );
}
