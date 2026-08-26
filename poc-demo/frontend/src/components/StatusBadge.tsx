import type { RunStatus } from "../types";

const CONFIG: Record<RunStatus, { label: string; color: string; bg: string }> = {
  attributed_correct: { label: "Correctly attributed", color: "var(--green)", bg: "var(--green-soft)" },
  attributed_partial: { label: "Agent correct, step off", color: "var(--amber)", bg: "var(--amber-soft)" },
  attributed_incorrect: { label: "Misattributed", color: "var(--red)", bg: "var(--red-soft)" },
  clean_no_fault: { label: "Clean / no fault", color: "var(--blue)", bg: "var(--blue-soft)" },
  self_corrected: { label: "Self-corrected", color: "var(--teal)", bg: "var(--teal-soft)" },
  fault_propagated: { label: "Fault propagated", color: "var(--orange)", bg: "var(--orange-soft)" },
  repaired_verified: { label: "Repaired & verified", color: "var(--green)", bg: "var(--green-soft)" },
  repair_failed: { label: "Repair failed", color: "var(--red)", bg: "var(--red-soft)" },
  cyclic_bounded: { label: "Cycle bounded correctly", color: "var(--blue)", bg: "var(--blue-soft)" },
};

export function StatusBadge({ status }: { status: RunStatus }) {
  const c = CONFIG[status] ?? { label: status, color: "var(--text-secondary)", bg: "var(--surface-hover)" };
  return (
    <span className="pill" style={{ color: c.color, background: c.bg }}>
      <span className="pill-dot" />
      {c.label}
    </span>
  );
}
