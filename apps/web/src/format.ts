export const LEVELS: Record<string, string> = {
  V0: "Detected by a check; not yet reproduced",
  V1: "Supported by evidence; not replay-verified",
  V2: "Verified by controlled replays",
  V3: "Confirmed by a human reviewer",
};

/** Short names of the four verification levels, for badges and ladders. */
export const LEVEL_NAME: Record<string, string> = { V0: "Detected", V1: "Evidence", V2: "Replay-verified", V3: "Human-confirmed" };

export const STATUS_LABEL: Record<string, string> = {
  open: "Open", hypothesized: "Hypotheses ready", verifying: "Verifying", confirmed: "Confirmed", refuted: "Refuted",
  inconclusive: "Inconclusive", evidence_supported: "Evidence-supported", accepted: "Accepted", rejected: "Rejected",
  resolved: "Resolved", wont_fix: "Won't fix",
};

export const label = (status: string): string => STATUS_LABEL[status] ?? status.replace(/_/g, " ");

/** How a hypothesis was classified by attribution (granite_core/attribution.py), in plain words. */
export const EVIDENCE_KIND: Record<string, string> = {
  truth_mismatch: "Contradicts the source of truth",
  contract_fail: "Broke its own contract",
  handoff_drift: "Received a different value than upstream produced",
  consistent: "Consistent with its inputs",
  unknown: "No check on this step",
};
export const evidenceKind = (kind: string): string => EVIDENCE_KIND[kind] ?? kind.replace(/_/g, " ");

export const EVIDENCE_TYPE: Record<string, string> = {
  step_snapshot: "Step snapshot", check_computation: "Check computation", source_of_truth_query: "Source-of-truth query",
  provenance_path: "Provenance path", replay_output: "Replay output", diff: "Diff", verdict_computation: "Verdict computation",
  llm_opinion: "LLM opinion", reviewer_note: "Reviewer note",
};
export const evidenceType = (type: string): string => EVIDENCE_TYPE[type] ?? type.replace(/_/g, " ");

export const STEP_KIND: Record<string, string> = { llm: "LLM", tool: "Tool", code: "Code", handoff: "Hand-off", input: "Input" };
export const stepKind = (kind: string): string => STEP_KIND[kind] ?? kind;

/** How the model answers were produced. "recorded" replays saved real answers; "live" calls the model. */
export const MODE_LABEL: Record<string, string> = { recorded: "Recorded cassette", live: "Live model", auto: "Automatic" };
export const modeLabel = (mode: string): string => MODE_LABEL[mode] ?? mode;

export const FAULT_LABEL: Record<string, string> = { stale_price: "Stale price" };
export const faultLabel = (fault: string | null | undefined): string => (fault ? FAULT_LABEL[fault] ?? label(fault) : "None");

export function short(value: unknown, max = 70): string {
  const text = typeof value === "string" ? value : JSON.stringify(value);
  return text.length > max ? `${text.slice(0, max - 1)}…` : text;
}

/** The API stores UTC without a zone suffix; read such timestamps as UTC, not local time. */
export function parseTime(iso: string | null | undefined): Date | null {
  if (!iso) return null;
  const zoned = /(?:Z|[+-]\d{2}:?\d{2})$/.test(iso) || !iso.includes("T") ? iso : `${iso}Z`;
  const d = new Date(zoned);
  return Number.isNaN(d.getTime()) ? null : d;
}

export function when(iso: string | null | undefined): string {
  const d = parseTime(iso);
  return d ? d.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" }) : "";
}

/** "3 min ago", "2 h ago", then a date. */
export function ago(iso: string | null | undefined, now: Date = new Date()): string {
  const d = parseTime(iso);
  if (!d) return "";
  const s = Math.max(0, Math.round((now.getTime() - d.getTime()) / 1000));
  if (s < 60) return "just now";
  if (s < 3600) return `${Math.floor(s / 60)} min ago`;
  if (s < 86400) return `${Math.floor(s / 3600)} h ago`;
  return d.toLocaleDateString(undefined, { dateStyle: "medium" });
}

/** Elapsed time between two timestamps: "224 ms", "3.2 s", "1 min 5 s". Empty when either is missing. */
export function duration(from: string | null | undefined, to: string | null | undefined): string {
  const a = parseTime(from), b = parseTime(to);
  if (!a || !b) return "";
  const ms = Math.max(0, b.getTime() - a.getTime());
  if (ms < 1000) return `${ms} ms`;
  if (ms < 60_000) return `${(ms / 1000).toFixed(1)} s`;
  return `${Math.floor(ms / 60_000)} min ${Math.round((ms % 60_000) / 1000)} s`;
}

export function pct(x: number): string {
  return `${Math.round(x * 100)}%`;
}

/** A value for display: numbers keep their precision, strings stay, everything else is compact JSON. */
export function show(value: unknown): string {
  if (value === null || value === undefined) return "n/a";
  if (typeof value === "number") return Number.isInteger(value) ? String(value) : String(Number(value.toFixed(4)));
  if (typeof value === "string") return value;
  if (typeof value === "boolean") return value ? "true" : "false";
  return JSON.stringify(value);
}

/** Signed difference of two numbers ("-0.25"), or "" when either is not a number. */
export function delta(observed: unknown, expected: unknown): string {
  if (typeof observed !== "number" || typeof expected !== "number") return "";
  const d = Number((observed - expected).toFixed(4));
  return d === 0 ? "0" : `${d > 0 ? "+" : "−"}${Math.abs(d)}`;
}

/** First text value of a workflow's final output (the Refund Desk returns {message}). */
export function finalText(output: Record<string, unknown> | null | undefined): string {
  if (!output) return "";
  const first = Object.values(output)[0];
  return first === undefined || first === null ? "" : typeof first === "string" ? first : JSON.stringify(first);
}

export const hashShort = (sha: string | null | undefined, n = 12): string => (sha ? `${sha.slice(0, n)}…` : "");
