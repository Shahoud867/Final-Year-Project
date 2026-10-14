/**
 * Rule VR-1 as the interface explains it. The verdict of a real experiment always comes from the server
 * (packages/granite_core/granite_core/verification.py); these functions only draw the rule and let a reader
 * explore it. A server test keeps the constants below equal to the ones the server uses.
 */

export const RULE_VERSION = "VR-1";
export const CONFIRM_MIN_RATE = 0.8;
export const CONTROL_MAX_RATE = 0.2;
export const REFUTE_MAX_RATE = 0.2;
export const MAX_REPLAYS = 10;
export const MAX_CONTROLS = 5;
export const DEFAULT_REPLAYS = 5;
export const DEFAULT_CONTROLS = 2;

export type Verdict = "confirmed" | "refuted" | "inconclusive" | "error";

/** Wilson score interval for k successes in n trials (95% by default), as the server reports it. */
export function wilson(k: number, n: number, z = 1.96): [number, number] {
  if (n <= 0) return [0, 1];
  const p = k / n;
  const denom = 1 + (z * z) / n;
  const centre = (p + (z * z) / (2 * n)) / denom;
  const half = (z * Math.sqrt((p * (1 - p)) / n + (z * z) / (4 * n * n))) / denom;
  return [Math.max(0, centre - half), Math.min(1, centre + half)];
}

/** VR-1: k of n fix replays passed, c of m control replays passed. Unfinished replays give no verdict. */
export function decide(k: number, n: number, c: number, m: number, completed = n, completedControls = m): Verdict {
  if (completed < n || completedControls < m) return "error";
  const p = k / n;
  const q = m > 0 ? c / m : 0;
  if (p >= CONFIRM_MIN_RATE && q <= CONTROL_MAX_RATE) return "confirmed";
  if (p <= REFUTE_MAX_RATE) return "refuted";
  return "inconclusive";
}

export interface RuleLine { id: "fix" | "control" | "refute"; text: string; rate: number | null; holds: boolean | null }

/**
 * The conditions of VR-1 evaluated on the counts of one experiment, for display next to its verdict.
 * `holds` is null when a rate cannot be computed (nothing finished, or no controls were requested).
 */
export function ruleLines(k: number, n: number, c: number, m: number): RuleLine[] {
  const p = n > 0 ? k / n : null;
  const q = m > 0 ? c / m : null;
  return [
    { id: "fix", text: `Fix replays correct ≥ ${CONFIRM_MIN_RATE * 100}%`, rate: p, holds: p === null ? null : p >= CONFIRM_MIN_RATE },
    { id: "control", text: `Control replays correct ≤ ${CONTROL_MAX_RATE * 100}%`, rate: q, holds: q === null ? null : q <= CONTROL_MAX_RATE },
    { id: "refute", text: `Refuted when fix replays correct ≤ ${REFUTE_MAX_RATE * 100}%`, rate: p, holds: p === null ? null : p <= REFUTE_MAX_RATE },
  ];
}
