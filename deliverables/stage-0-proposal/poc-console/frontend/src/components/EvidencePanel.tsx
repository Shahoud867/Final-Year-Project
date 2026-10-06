import type { RunDetail } from "../types";

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "128px 1fr", gap: 12, padding: "8px 0", borderBottom: "1px solid var(--border)" }}>
      <div className="text-muted" style={{ fontSize: 12, fontWeight: 600, paddingTop: 1 }}>
        {label}
      </div>
      <div style={{ fontSize: 13 }}>{children}</div>
    </div>
  );
}

export function EvidencePanel({ run }: { run: RunDetail }) {
  const a = run.attribution;
  const sed = run.sed;
  const fault = run.fault;
  const clf = run.classifier;

  return (
    <div className="card card-pad fade-in">
      <div style={{ fontWeight: 700, fontSize: 13.5, marginBottom: 6 }}>Diagnosis evidence</div>

      {a && (
        <>
          <Row label="Culprit agent">
            <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              <span>
                ground truth: <b>{a.gt_agent ?? "—"}</b>
              </span>
              {a.pred_agent && (
                <span className={a.agent_correct ? "" : "text-secondary"}>
                  predicted: <b style={{ color: a.agent_correct ? "var(--green)" : "var(--red)" }}>{a.pred_agent}</b>{" "}
                  {a.agent_correct ? "✓" : "✗"}
                </span>
              )}
            </div>
          </Row>
          <Row label="Culprit step">
            <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              <span className="mono">
                gt: <b>{String(a.gt_step ?? "—")}</b>
              </span>
              {a.pred_step != null && (
                <span className="mono">
                  pred: <b style={{ color: a.step_correct_type_safe ? "var(--green)" : "var(--red)" }}>{String(a.pred_step)}</b>{" "}
                  {a.step_correct_type_safe ? "✓" : "✗"}
                </span>
              )}
            </div>
          </Row>
          {a.confidence != null && (
            <Row label="Confidence">
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <div style={{ width: 90, height: 6, background: "var(--surface-hover)", borderRadius: 3, overflow: "hidden" }}>
                  <div style={{ width: `${a.confidence * 100}%`, height: "100%", background: "var(--accent)" }} />
                </div>
                <span className="mono">{a.confidence.toFixed(2)}</span>
              </div>
            </Row>
          )}
          {a.hypotheses.length > 0 && (
            <Row label="Hypotheses">
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                {a.hypotheses.map((h, i) => (
                  <div key={i} className="text-secondary" style={{ fontSize: 12 }}>
                    <span className="mono" style={{ color: "var(--text)" }}>
                      step {h.step} · {h.agent}
                    </span>{" "}
                    — {h.reason}
                  </div>
                ))}
              </div>
            </Row>
          )}
        </>
      )}

      {sed && (
        <>
          <Row label="SED verdict">
            <span style={{ color: sed.verdict.startsWith("PASS") ? "var(--green)" : "var(--red)" }}>{sed.verdict}</span>
          </Row>
          <Row label="Constraint check">
            <span className="mono">
              expected {sed.correct_answer} · stated {sed.stated_answer} · model wrong: {String(sed.model_was_actually_wrong)}
            </span>
          </Row>
        </>
      )}

      {clf && (
        <>
          <Row label="True label">
            <span className="mono" style={{ color: clf.true_label === "corrupted" ? "var(--amber)" : "var(--green)" }}>
              {clf.true_label}
            </span>
          </Row>
          <Row label="Predicted">
            <span className="mono" style={{ color: clf.correct ? "var(--green)" : "var(--red)" }}>
              {clf.predicted_label} {clf.correct ? "✓" : "✗"}
            </span>
          </Row>
          <Row label="Method">
            <span className="text-secondary" style={{ fontSize: 12 }}>{clf.method}</span>
          </Row>
        </>
      )}

      {fault && (
        <>
          <Row label="Fault type">
            <span className="mono">{fault.type}</span>
          </Row>
          <Row label="Origin node">
            <span className="mono">{fault.origin_node}</span>
          </Row>
          <Row label="Propagation">
            <span>{fault.propagation_verdict.replaceAll("_", " ")}</span>
          </Row>
        </>
      )}

      {run.ground_truth_note && (
        <div
          style={{
            marginTop: 14,
            padding: "10px 12px",
            background: "var(--accent-soft)",
            borderRadius: "var(--radius-sm)",
            fontSize: 12.5,
            lineHeight: 1.55,
            color: "var(--text)",
          }}
        >
          <b style={{ color: "var(--accent-strong)" }}>Note: </b>
          {run.ground_truth_note}
        </div>
      )}
    </div>
  );
}
