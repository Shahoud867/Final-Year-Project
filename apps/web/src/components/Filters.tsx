import { useState } from "react";
import type { FormEvent } from "react";
import type { FindingFilter } from "../api";

/** Search and filter row for the findings list (FR-HIS-01). Applied when the form is submitted, not on every keystroke. */
export function Filters({ value, onApply }: { value: FindingFilter; onApply: (next: FindingFilter) => void }) {
  const [draft, setDraft] = useState<FindingFilter>(value);
  const set = (k: keyof FindingFilter) => (e: { target: { value: string } }) => setDraft({ ...draft, [k]: e.target.value });
  const submit = (e: FormEvent) => { e.preventDefault(); onApply(draft); };
  const clear = () => { setDraft({}); onApply({}); };
  return (
    <form className="row" onSubmit={submit} role="search" aria-label="Filter findings" style={{ marginBottom: 12 }}>
      <div style={{ flex: "1 1 200px" }}>
        <label htmlFor="f-q" className="sr-only">Search findings</label>
        <input id="f-q" type="search" placeholder="Search findings" value={draft.q ?? ""} onChange={set("q")} maxLength={100} />
      </div>
      <div>
        <label htmlFor="f-sev" className="sr-only">Severity</label>
        <select id="f-sev" value={draft.severity ?? ""} onChange={set("severity")}>
          <option value="">Any severity</option>
          {["critical", "high", "medium", "low"].map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
      </div>
      <div>
        <label htmlFor="f-lvl" className="sr-only">Verification level</label>
        <select id="f-lvl" value={draft.level ?? ""} onChange={set("level")}>
          <option value="">Any level</option>
          <option value="V0">V0 detected</option>
          <option value="V1">V1 evidence</option>
          <option value="V2">V2 replay-verified</option>
          <option value="V3">V3 human-confirmed</option>
        </select>
      </div>
      <button type="submit">Search</button>
      <button type="button" onClick={clear}>Clear</button>
    </form>
  );
}
