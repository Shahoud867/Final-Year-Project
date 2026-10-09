export const LEVELS: Record<string, string> = {
  V0: "Detected by a check; not yet reproduced",
  V1: "Supported by evidence; not replay-verified",
  V2: "Verified by controlled replays",
  V3: "Confirmed by a human reviewer",
};

export const STATUS_LABEL: Record<string, string> = {
  open: "Open", hypothesized: "Hypotheses ready", verifying: "Verifying", confirmed: "Confirmed", refuted: "Refuted",
  inconclusive: "Inconclusive", evidence_supported: "Evidence-supported", accepted: "Accepted", rejected: "Rejected",
  resolved: "Resolved", wont_fix: "Won't fix",
};

export const label = (status: string): string => STATUS_LABEL[status] ?? status.replace(/_/g, " ");

export function short(value: unknown, max = 70): string {
  const text = typeof value === "string" ? value : JSON.stringify(value);
  return text.length > max ? `${text.slice(0, max - 1)}…` : text;
}

export function when(iso: string | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  return Number.isNaN(d.getTime()) ? "" : d.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
}

export function pct(x: number): string {
  return `${Math.round(x * 100)}%`;
}
