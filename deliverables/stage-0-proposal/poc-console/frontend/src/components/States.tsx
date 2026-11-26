export function LoadingSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="skeleton" style={{ height: 46, borderRadius: 10 }} />
      ))}
    </div>
  );
}

export function EmptyState({ title, sub }: { title: string; sub?: string }) {
  return (
    <div
      className="card card-pad fade-in"
      style={{ textAlign: "center", padding: "48px 20px", color: "var(--text-secondary)" }}
    >
      <div style={{ fontSize: 28, marginBottom: 10, opacity: 0.5 }}>◌</div>
      <div style={{ fontWeight: 700, color: "var(--text)", marginBottom: 4 }}>{title}</div>
      {sub && <div style={{ fontSize: 13 }}>{sub}</div>}
    </div>
  );
}

export function ErrorState({ message, onRetry }: { message: string; onRetry?: () => void }) {
  return (
    <div
      className="card card-pad fade-in"
      style={{ textAlign: "center", padding: "40px 20px", borderColor: "var(--red)" }}
    >
      <div style={{ fontSize: 24, marginBottom: 10, color: "var(--red)" }}>⚠</div>
      <div style={{ fontWeight: 700, marginBottom: 4 }}>Couldn't reach the diagnosis API</div>
      <div className="text-secondary" style={{ fontSize: 13, marginBottom: 14 }}>
        {message}
      </div>
      {onRetry && (
        <button className="btn btn-primary" onClick={onRetry}>
          Retry
        </button>
      )}
    </div>
  );
}
