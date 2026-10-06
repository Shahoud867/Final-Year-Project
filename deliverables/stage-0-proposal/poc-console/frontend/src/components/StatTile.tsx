import type { ReactNode } from "react";

export function StatTile({
  label,
  value,
  sub,
  tone = "default",
  flag,
}: {
  label: string;
  value: ReactNode;
  sub?: ReactNode;
  tone?: "default" | "good" | "warn" | "bad";
  flag?: string;
}) {
  const toneColor =
    tone === "good" ? "var(--green)" : tone === "warn" ? "var(--amber)" : tone === "bad" ? "var(--red)" : "var(--text)";
  return (
    <div className="card card-pad fade-in" style={{ position: "relative", minWidth: 0 }}>
      {flag && (
        <div
          title={flag}
          style={{
            position: "absolute",
            top: 10,
            right: 10,
            width: 8,
            height: 8,
            borderRadius: "50%",
            background: "var(--amber)",
            boxShadow: "0 0 0 3px var(--amber-soft)",
          }}
        />
      )}
      <div className="text-secondary" style={{ fontSize: 12, fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.04em", marginBottom: 8 }}>
        {label}
      </div>
      <div style={{ fontSize: 26, fontWeight: 800, color: toneColor, letterSpacing: "-0.02em", lineHeight: 1.1 }}>{value}</div>
      {sub && (
        <div className="text-muted" style={{ fontSize: 12, marginTop: 6 }}>
          {sub}
        </div>
      )}
    </div>
  );
}
