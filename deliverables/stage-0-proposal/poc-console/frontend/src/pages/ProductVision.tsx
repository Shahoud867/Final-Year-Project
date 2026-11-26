import { useEffect, useState } from "react";
import { api } from "../api";
import type { Scope } from "../types";
import { LoadingSkeleton, ErrorState } from "../components/States";

const BAND_TONE: Record<string, { color: string; bg: string }> = {
  core: { color: "var(--green)", bg: "var(--green-soft)" },
  advanced: { color: "var(--blue)", bg: "var(--blue-soft)" },
  stretch: { color: "var(--amber)", bg: "var(--amber-soft)" },
  future: { color: "var(--text-muted)", bg: "var(--surface-hover)" },
};

function CodeBlock({ code, lang }: { code: string; lang: string | null }) {
  return (
    <div
      style={{
        background: "var(--bg)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-sm)",
        padding: "10px 12px",
        marginTop: 10,
        overflowX: "auto",
      }}
    >
      {lang && (
        <div className="text-muted mono" style={{ fontSize: 10, marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.06em" }}>
          {lang}
        </div>
      )}
      <pre className="mono" style={{ margin: 0, fontSize: 12, lineHeight: 1.6, color: "var(--text)", whiteSpace: "pre" }}>
        {code}
      </pre>
    </div>
  );
}

export function ProductVision() {
  const [scope, setScope] = useState<Scope | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    setError(null);
    api.scope().then(setScope).catch((e) => setError(String(e)));
  };
  useEffect(load, []);

  if (error) return <div className="page"><ErrorState message={error} onRetry={load} /></div>;
  if (!scope)
    return (
      <div className="page">
        <LoadingSkeleton rows={6} />
      </div>
    );

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Product vision & committed scope</h1>
          <p className="page-subtitle">
            Two things a panel can't see from the diagnosis screens alone: how a team would actually adopt
            Granite, and exactly what is committed versus gated versus out of scope — with each item's real
            status, including the one that failed its only test.
          </p>
        </div>
      </div>

      {/* ---------- SECTION A: SDK journey (ILLUSTRATIVE) ---------- */}
      <div
        className="card fade-in"
        style={{ marginBottom: 30, borderColor: "var(--amber)", borderWidth: 2, overflow: "hidden" }}
      >
        <div
          style={{
            background: "var(--amber-soft)",
            padding: "12px 20px",
            borderBottom: "1px solid var(--amber)",
            display: "flex",
            gap: 12,
            alignItems: "flex-start",
          }}
        >
          <div style={{ fontSize: 18, lineHeight: 1.2 }}>⚠</div>
          <div>
            <div style={{ fontWeight: 800, fontSize: 13.5, color: "var(--amber)", letterSpacing: "0.01em" }}>
              ILLUSTRATIVE CONCEPT — NOT BUILT
            </div>
            <div className="text-secondary" style={{ fontSize: 12.5, lineHeight: 1.6, marginTop: 4 }}>
              {scope.sdk_disclaimer}
            </div>
          </div>
        </div>

        <div className="card-pad">
          <div style={{ fontWeight: 700, fontSize: 14, marginBottom: 4 }}>
            How a team would adopt Granite
          </div>
          <div className="text-secondary" style={{ fontSize: 12.5, marginBottom: 20 }}>
            The adoption path implied by FR5 — installable against a user-supplied CrewAI or LangGraph
            workflow without modifying the core diagnosis algorithm.
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {scope.sdk_journey.map((s, i) => (
              <div key={s.step} style={{ display: "flex", gap: 14 }}>
                <div style={{ flexShrink: 0, display: "flex", flexDirection: "column", alignItems: "center" }}>
                  <div
                    style={{
                      width: 26,
                      height: 26,
                      borderRadius: "50%",
                      background: "var(--amber-soft)",
                      border: "1px solid var(--amber)",
                      color: "var(--amber)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontWeight: 800,
                      fontSize: 12,
                    }}
                  >
                    {s.step}
                  </div>
                  {i < scope.sdk_journey.length - 1 && (
                    <div style={{ flex: 1, width: 1, background: "var(--border-strong)", marginTop: 4, minHeight: 20 }} />
                  )}
                </div>
                <div style={{ flex: 1, minWidth: 0, paddingBottom: 4 }}>
                  <div style={{ fontWeight: 700, fontSize: 13.5, marginBottom: 3 }}>{s.title}</div>
                  <div className="text-secondary" style={{ fontSize: 12.5, lineHeight: 1.6 }}>
                    {s.detail}
                  </div>
                  {s.code && <CodeBlock code={s.code} lang={s.lang} />}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ---------- SECTION B: Tier 1 ---------- */}
      <div style={{ marginBottom: 12, display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap" }}>
        <h2 style={{ fontSize: 16, fontWeight: 800, margin: 0 }}>Committed core — Tier 1</h2>
        <span className="pill" style={{ color: "var(--green)", background: "var(--green-soft)" }}>
          evidence-backed · unconditional
        </span>
      </div>
      <p className="text-secondary" style={{ fontSize: 12.5, marginTop: 0, marginBottom: 14 }}>
        Eight mechanisms, each with a proof-of-concept spike behind it. Committed without conditions.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: 12, marginBottom: 30 }}>
        {scope.tier_1.map((t) => (
          <div key={t.n} className="card card-pad fade-in" style={{ borderLeft: "3px solid var(--green)" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6, flexWrap: "wrap" }}>
              <span className="mono text-muted" style={{ fontSize: 11 }}>#{t.n}</span>
              <span style={{ fontWeight: 700, fontSize: 13.5 }}>{t.name}</span>
              {t.spike && (
                <span className="pill" style={{ color: "var(--green)", background: "var(--green-soft)", fontSize: 10.5 }}>
                  {t.spike}
                </span>
              )}
              {!t.spike && (
                <span className="pill" style={{ color: "var(--amber)", background: "var(--amber-soft)", fontSize: 10.5 }}>
                  partial
                </span>
              )}
            </div>
            <div className="text-secondary" style={{ fontSize: 12.5, lineHeight: 1.55, marginBottom: 8 }}>
              {t.what}
            </div>
            <div style={{ fontSize: 12, lineHeight: 1.55, padding: "8px 10px", background: "var(--bg)", borderRadius: 6 }}>
              <span className="text-muted" style={{ fontSize: 10.5, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em" }}>
                Evidence
              </span>
              <div style={{ marginTop: 3 }}>{t.evidence}</div>
            </div>
          </div>
        ))}
      </div>

      {/* ---------- SECTION C: Tier 2 (gated) ---------- */}
      <div style={{ marginBottom: 12, display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap" }}>
        <h2 style={{ fontSize: 16, fontWeight: 800, margin: 0 }}>Committed core — Tier 2</h2>
        <span className="pill" style={{ color: "var(--amber)", background: "var(--amber-soft)" }}>
          committed · pre-registered Mid-1 gates
        </span>
      </div>
      <p className="text-secondary" style={{ fontSize: 12.5, marginTop: 0, marginBottom: 14 }}>
        Still committed core — not demoted. These two carry the weakest evidence in the list, so each has a
        pass/fail rule written <b>before</b> the result exists, with a recorded fallback. Nothing here is
        shown as working, because neither is.
      </p>

      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 30 }}>
        {scope.tier_2.map((t) => (
          <div key={t.n} className="card card-pad fade-in" style={{ borderLeft: "3px solid var(--amber)" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6, flexWrap: "wrap" }}>
              <span className="mono text-muted" style={{ fontSize: 11 }}>#{t.n}</span>
              <span style={{ fontWeight: 700, fontSize: 13.5 }}>{t.name}</span>
              <span className="pill" style={{ color: "var(--amber)", background: "var(--amber-soft)", fontSize: 10.5 }}>
                gated · {t.risk}
              </span>
            </div>
            <div className="text-secondary" style={{ fontSize: 12.5, lineHeight: 1.55, marginBottom: 10 }}>
              {t.what}
            </div>
            <div
              style={{
                fontSize: 12.5,
                lineHeight: 1.6,
                padding: "10px 12px",
                background: "var(--red-soft)",
                borderRadius: 6,
                marginBottom: 8,
              }}
            >
              <span style={{ fontSize: 10.5, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em", color: "var(--red)" }}>
                Honest status
              </span>
              <div style={{ marginTop: 3 }}>{t.status}</div>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: 10 }}>
              <div style={{ fontSize: 12, lineHeight: 1.55, padding: "8px 10px", background: "var(--bg)", borderRadius: 6 }}>
                <span className="text-muted" style={{ fontSize: 10.5, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em" }}>
                  Gate (by Mid-1)
                </span>
                <div style={{ marginTop: 3 }}>{t.gate}</div>
              </div>
              <div style={{ fontSize: 12, lineHeight: 1.55, padding: "8px 10px", background: "var(--bg)", borderRadius: 6 }}>
                <span className="text-muted" style={{ fontSize: 10.5, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em" }}>
                  Recorded fallback
                </span>
                <div style={{ marginTop: 3 }}>{t.fallback}</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* ---------- SECTION D: Scope bands ---------- */}
      <h2 style={{ fontSize: 16, fontWeight: 800, margin: "0 0 4px" }}>Scope bands</h2>
      <p className="text-secondary" style={{ fontSize: 12.5, marginTop: 0, marginBottom: 14 }}>
        The grading and sequencing layer over the frozen mechanism list. What gets built, in what order, and
        what gets dropped first under schedule pressure.
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 12, marginBottom: 20 }}>
        {scope.bands.map((b) => {
          const tone = BAND_TONE[b.tone] ?? BAND_TONE.future;
          return (
            <div key={b.band} className="card card-pad fade-in" style={{ borderTop: `3px solid ${tone.color}` }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                <span style={{ fontWeight: 800, fontSize: 14, color: tone.color }}>{b.band}</span>
              </div>
              <div className="text-secondary" style={{ fontSize: 11.5, lineHeight: 1.5, marginBottom: 10, fontStyle: "italic" }}>
                {b.rule}
              </div>
              <ul style={{ margin: 0, paddingLeft: 16, display: "flex", flexDirection: "column", gap: 5 }}>
                {b.items.map((it, i) => (
                  <li key={i} style={{ fontSize: 12, lineHeight: 1.5 }}>
                    {it}
                  </li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>

      <div className="card card-pad fade-in">
        <div style={{ fontWeight: 700, fontSize: 13.5, marginBottom: 4 }}>
          Pre-registered descope ladder
        </div>
        <div className="text-secondary" style={{ fontSize: 12.5, marginBottom: 12 }}>
          If the schedule slips, work drops in exactly this order — decided in advance, recorded when it
          happens, so schedule pressure produces a recorded scope decision instead of quiet quality decay.
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {scope.descope_ladder.map((d, i) => (
            <div key={i} style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
              <span
                className="mono"
                style={{
                  flexShrink: 0,
                  fontSize: 10.5,
                  fontWeight: 700,
                  color: i === scope.descope_ladder.length - 1 ? "var(--green)" : "var(--text-muted)",
                  paddingTop: 1,
                }}
              >
                {i === scope.descope_ladder.length - 1 ? "STOP" : `${i + 1}.`}
              </span>
              <span
                style={{
                  fontSize: 12.5,
                  lineHeight: 1.5,
                  fontWeight: i === scope.descope_ladder.length - 1 ? 700 : 400,
                  color: i === scope.descope_ladder.length - 1 ? "var(--green)" : "var(--text)",
                }}
              >
                {d}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
