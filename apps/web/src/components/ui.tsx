import type { ReactNode } from "react";
import { label } from "../format";

const TONE: Record<string, string> = {
  completed: "ok", pass: "ok", confirmed: "ok", accepted: "ok", resolved: "ok", succeeded: "ok",
  fail: "bad", errored: "bad", error: "bad", rejected: "bad", refuted: "bad", failed: "bad",
  hypothesized: "info", verifying: "info", running: "info", queued: "info", evidence_supported: "info",
  inconclusive: "warn", abstain: "warn", wont_fix: "warn", open: "warn",
};

export function Badge({ value, text }: { value: string; text?: string }) {
  return <span className={`badge ${TONE[value] ?? ""}`}>{text ?? label(value)}</span>;
}

export function ErrorBox({ message, onRetry }: { message: string; onRetry?: () => void }) {
  if (!message) return null;
  return (
    <div className="alert bad" role="alert">
      {message} {onRetry && <button onClick={onRetry} style={{ marginLeft: 8 }}>Try again</button>}
    </div>
  );
}

export function Loading({ text = "Loading…" }: { text?: string }) {
  return <p className="muted" role="status">{text}</p>;
}

export function Empty({ children }: { children: ReactNode }) {
  return <div className="empty">{children}</div>;
}

export function Progress({ done, total }: { done: number; total: number }) {
  const width = total ? Math.round((done / total) * 100) : 0;
  return (
    <div className="progress" role="progressbar" aria-valuenow={done} aria-valuemin={0} aria-valuemax={total}>
      <div style={{ width: `${width}%` }} />
    </div>
  );
}
