import { Database } from "lucide-react";
import { show } from "../format";
import type { CheckResult } from "../types";
import { JsonView } from "./ui";

/** What a check compared the step's value with: the independent source of truth, policy, or the step's own contract. */
export function comparedWith(c: CheckResult): string {
  const calls = c.computation?.truth_calls ?? [];
  if (c.type === "truth") return calls.length > 0 ? `source of truth (${calls.map((t) => t.function).join(", ")})` : "source of truth";
  if (c.type === "policy") return "policy, read from the source of truth";
  return "the step's own contract over its inputs";
}

const args = (a: unknown): string => (Array.isArray(a) ? a.map((x) => show(x)).join(", ") : show(a));

/** How a check result was computed: the expression, the values it read from the trace, and each source-of-truth call. */
export function Computation({ c }: { c: CheckResult }) {
  const k = c.computation;
  if (!k) return <p className="small dim">The computation was not recorded for this result.</p>;
  return (
    <div className="stack tight">
      {k.expression ? <code className="check-expr wrap-any">{k.expression}</code> : null}
      {k.truth_calls && k.truth_calls.length > 0 ? (
        <ul className="list-plain stack tight">
          {k.truth_calls.map((t, i) => (
            <li key={i} className="small row tight top">
              <Database size={13} aria-hidden="true" className="t-replay" />
              <span className="mono wrap-any grow">truth.{t.function}({args(t.arguments)}) <span className="dim">returned</span> <strong>{show(t.returned)}</strong></span>
            </li>
          ))}
        </ul>
      ) : null}
      {k.resolved && Object.keys(k.resolved).length > 0 ? <JsonView value={k.resolved} label={`Values read by ${c.check_id}`} maxHeight={200} /> : null}
      {typeof k.tolerance === "number" ? <span className="small dim">tolerance {k.tolerance}</span> : null}
    </div>
  );
}
