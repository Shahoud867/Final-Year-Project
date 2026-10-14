/**
 * The finding lifecycle as the interface draws it. The server owns the state machine
 * (packages/granite_core/granite_core/lifecycle.py) and tells each page which actions are allowed now;
 * this copy only labels and groups the states. A server test keeps TRANSITIONS equal to the server's table.
 */

export const STAGES = ["Detected", "Traced", "Verified", "Reviewed"] as const;

/** What each stage means, which feature produces it and the verification level it gives. */
export const STAGE_INFO: { name: (typeof STAGES)[number]; does: string; level: string }[] = [
  { name: "Detected", does: "An outcome check failed on a completed run", level: "V0" },
  { name: "Traced", does: "Suspect steps ranked from the recorded data flow", level: "V1" },
  { name: "Verified", does: "Fix replays compared with controls under VR-1", level: "V2" },
  { name: "Reviewed", does: "A named person accepted or rejected it", level: "V3" },
];

/** Stage 1 to 4 of a finding status (Detected, Traced, Verified, Reviewed). */
export function stage(status: string): number {
  if (["accepted", "rejected", "resolved", "wont_fix"].includes(status)) return 4;
  if (["confirmed", "refuted", "inconclusive", "evidence_supported"].includes(status)) return 3;
  if (["hypothesized", "verifying"].includes(status)) return 2;
  return 1;
}

/** Statuses in which a finding waits for a person's decision (services/reviews.py AWAITING_REVIEW). */
export const AWAITING_REVIEW = ["confirmed", "inconclusive", "evidence_supported"];
/** Statuses that end an investigation. */
export const TERMINAL = ["rejected", "resolved", "wont_fix"];
/** Statuses whose verification level is V2 or V3. */
export const VERIFIED = ["confirmed", "accepted", "resolved", "wont_fix"];

/** [from, event, to] for every legal transition, in the order lifecycle.py lists them. */
export const TRANSITIONS: [string, string, string][] = [
  ["open", "hypotheses_ready", "hypothesized"],
  ["hypothesized", "verify_started", "verifying"],
  ["hypothesized", "evidence_supported", "evidence_supported"],
  ["verifying", "verdict_confirmed", "confirmed"],
  ["verifying", "verdict_refuted", "refuted"],
  ["verifying", "verdict_inconclusive", "inconclusive"],
  ["verifying", "verify_error", "hypothesized"],
  ["refuted", "verify_started", "verifying"],
  ["inconclusive", "verify_started", "verifying"],
  ["confirmed", "review_accept", "accepted"],
  ["confirmed", "review_reject", "rejected"],
  ["inconclusive", "review_accept", "accepted"],
  ["inconclusive", "review_reject", "rejected"],
  ["evidence_supported", "review_accept", "accepted"],
  ["evidence_supported", "review_reject", "rejected"],
  ["accepted", "resolve", "resolved"],
  ["accepted", "wont_fix", "wont_fix"],
];

/** Sum the counts of the given statuses in a GET /findings/summary result. */
export function countIn(counts: Record<string, number> | null | undefined, statuses: string[]): number {
  if (!counts || Array.isArray(counts)) return 0;
  return statuses.reduce((sum, s) => sum + (typeof counts[s] === "number" ? counts[s] : 0), 0);
}

/** Findings that have reached at least the given stage (1 to 4), from a GET /findings/summary result. */
export function reached(counts: Record<string, number> | null | undefined, atLeast: number): number {
  if (!counts || Array.isArray(counts)) return 0;
  return Object.entries(counts).reduce((sum, [status, n]) => sum + (stage(status) >= atLeast && typeof n === "number" ? n : 0), 0);
}
