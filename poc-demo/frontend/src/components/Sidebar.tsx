import { NavLink } from "react-router-dom";

const NAV = [
  { to: "/", label: "Overview", icon: "◧", end: true },
  { to: "/runs", label: "Runs & diagnoses", icon: "☰" },
  { to: "/evidence", label: "POC evidence", icon: "◈" },
];

export function Sidebar() {
  return (
    <aside
      style={{
        borderRight: "1px solid var(--border)",
        background: "var(--bg-elevated)",
        padding: "20px 14px",
        display: "flex",
        flexDirection: "column",
        gap: 4,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "4px 10px 22px" }}>
        <div
          style={{
            width: 30,
            height: 30,
            borderRadius: 8,
            background: "linear-gradient(135deg, var(--accent), #a56a2b)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontWeight: 800,
            fontSize: 15,
            color: "#1a1204",
          }}
        >
          G
        </div>
        <div>
          <div style={{ fontWeight: 800, fontSize: 15, letterSpacing: "-0.01em" }}>Granite</div>
          <div className="text-muted" style={{ fontSize: 10.5, marginTop: -2 }}>
            Diagnosis Console — PoC
          </div>
        </div>
      </div>

      {NAV.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          end={item.end}
          style={({ isActive }) => ({
            display: "flex",
            alignItems: "center",
            gap: 10,
            padding: "9px 12px",
            borderRadius: 8,
            fontSize: 13.5,
            fontWeight: 600,
            color: isActive ? "var(--text)" : "var(--text-secondary)",
            background: isActive ? "var(--surface)" : "transparent",
          })}
        >
          <span style={{ width: 16, textAlign: "center", opacity: 0.85 }}>{item.icon}</span>
          {item.label}
        </NavLink>
      ))}

      <div style={{ flex: 1 }} />

      <div className="card card-pad" style={{ margin: "0 2px" }}>
        <div style={{ fontSize: 11.5, fontWeight: 700, color: "var(--accent)", marginBottom: 4 }}>
          Proposal-defense PoC
        </div>
        <div className="text-muted" style={{ fontSize: 11, lineHeight: 1.5 }}>
          Every number on this console is read live from the 8 committed spike output files in{" "}
          <code className="mono" style={{ fontSize: 10 }}>dev/spikes/poc/</code>. Nothing is simulated.
        </div>
      </div>
    </aside>
  );
}
