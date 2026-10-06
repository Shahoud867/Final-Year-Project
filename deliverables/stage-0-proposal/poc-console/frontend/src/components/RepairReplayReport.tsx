import type { RunDetail } from "../types";
import { EmptyState } from "./States";

function ConfidenceGate({ confidence }: { confidence: number | null }) {
  const threshold = 0.7; // illustrative -- extension #12's gate, not yet spike-tested
  if (confidence == null) {
    return (
      <div className="card card-pad" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12 }}>
        <div>
          <div style={{ fontWeight: 700, fontSize: 13 }}>Confidence gate</div>
          <div className="text-muted" style={{ fontSize: 11.5, marginTop: 2 }}>
            Extension #12's design (threshold {threshold}) — not applicable here because this spike's script
            doesn't emit a confidence score. Not fabricated; genuinely not measured yet.
          </div>
        </div>
        <span className="pill" style={{ color: "var(--text-secondary)", background: "var(--surface-hover)", fontSize: 12 }}>
          not measured
        </span>
      </div>
    );
  }
  const gated = confidence >= threshold;
  return (
    <div
      className="card card-pad"
      style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12 }}
    >
      <div>
        <div style={{ fontWeight: 700, fontSize: 13 }}>Confidence gate</div>
        <div className="text-muted" style={{ fontSize: 11.5, marginTop: 2 }}>
          Illustrative — extension #12's design, threshold {threshold}. Not yet spike-tested.
        </div>
      </div>
      <span
        className="pill"
        style={{
          color: gated ? "var(--green)" : "var(--amber)",
          background: gated ? "var(--green-soft)" : "var(--amber-soft)",
          fontSize: 12,
        }}
      >
        {gated ? "Auto-suggested" : "Needs human review"}
      </span>
    </div>
  );
}

export function RepairReplayReport({ run }: { run: RunDetail }) {
  const { repair, replay, fault } = run;

  if (!repair && !replay) {
    return (
      <EmptyState
        title="No repair was attempted for this run"
        sub="This spike tests attribution, silent-failure detection, or graph handling — not the Repair Agent / Verified Automatic Repair stage. See Spike 5 or Spike 8 runs for a repair & replay report."
      />
    );
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
      {fault && (
        <div className="card card-pad">
          <div style={{ fontWeight: 700, fontSize: 13.5, marginBottom: 10 }}>Diagnosed fault</div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <div>
              <div className="text-muted" style={{ fontSize: 11, marginBottom: 4 }}>
                TRUE VALUE
              </div>
              <div className="mono" style={{ fontSize: 12.5, color: "var(--green)" }}>
                {fault.true_value}
              </div>
            </div>
            <div>
              <div className="text-muted" style={{ fontSize: 11, marginBottom: 4 }}>
                CORRUPTED VALUE
              </div>
              <div className="mono" style={{ fontSize: 12.5, color: "var(--red)" }}>
                {fault.corrupted_value}
              </div>
            </div>
          </div>
        </div>
      )}

      {repair && (
        <div className="card card-pad">
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10 }}>
            <div style={{ fontWeight: 700, fontSize: 13.5 }}>Repair Agent — candidate fix</div>
            <span
              className="pill"
              style={{
                color: repair.exact_match ? "var(--green)" : "var(--amber)",
                background: repair.exact_match ? "var(--green-soft)" : "var(--amber-soft)",
              }}
            >
              {repair.exact_match ? "exact match" : "no exact match"}
            </span>
          </div>
          <div className="mono" style={{ fontSize: 15, fontWeight: 700, marginBottom: 8 }}>
            corrected_value = {String(repair.candidate_value)}
          </div>
          <div className="text-secondary" style={{ fontSize: 12.5, lineHeight: 1.55 }}>
            {repair.reasoning}
          </div>
        </div>
      )}

      {replay && (
        <div className="card card-pad">
          <div style={{ fontWeight: 700, fontSize: 13.5, marginBottom: 10 }}>
            Verified Automatic Repair — controlled replay
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 18, marginBottom: 12 }}>
            {replay.before != null && (
              <div>
                <div className="text-muted" style={{ fontSize: 11 }}>
                  BEFORE
                </div>
                <div className="mono" style={{ fontSize: 20, fontWeight: 800, color: "var(--red)" }}>
                  {replay.before}
                </div>
              </div>
            )}
            {replay.before != null && <div style={{ color: "var(--text-muted)", fontSize: 18 }}>→</div>}
            <div>
              <div className="text-muted" style={{ fontSize: 11 }}>
                AFTER REPLAY
              </div>
              <div
                className="mono"
                style={{ fontSize: 20, fontWeight: 800, color: replay.recovery_success ? "var(--green)" : "var(--red)" }}
              >
                {replay.after}
              </div>
            </div>
            <div>
              <div className="text-muted" style={{ fontSize: 11 }}>
                EXPECTED
              </div>
              <div className="mono" style={{ fontSize: 20, fontWeight: 800, color: "var(--text-secondary)" }}>
                {replay.expected}
              </div>
            </div>
          </div>
          <div
            className="pill"
            style={{
              color: replay.recovery_success ? "var(--green)" : "var(--red)",
              background: replay.recovery_success ? "var(--green-soft)" : "var(--red-soft)",
              fontSize: 12.5,
            }}
          >
            {replay.recovery_success ? "recovery_success: true" : "recovery_success: false"} · N={replay.n_replays} replay
            {replay.n_replays === 1 ? "" : "s"}
          </div>
        </div>
      )}

      <ConfidenceGate confidence={run.attribution?.confidence ?? null} />
    </div>
  );
}
