import { Search, X } from "lucide-react";
import { useState } from "react";
import type { FormEvent } from "react";
import type { FindingFilter, RunFilter } from "../api";
import { faultLabel } from "../format";

/** Search and filter row for the findings list (FR-HIS-01). Applied when the form is submitted, not on every keystroke. */
export function Filters({ value, onApply }: { value: FindingFilter; onApply: (next: FindingFilter) => void }) {
  const [draft, setDraft] = useState<FindingFilter>(value);
  const set = (k: keyof FindingFilter) => (e: { target: { value: string } }) => setDraft({ ...draft, [k]: e.target.value });
  const submit = (e: FormEvent) => { e.preventDefault(); onApply(draft); };
  const clear = () => { setDraft({}); onApply({}); };
  return (
    <form className="filters" onSubmit={submit} role="search" aria-label="Filter findings">
      <div className="filters-q">
        <label htmlFor="f-q" className="sr-only">Search findings</label>
        <input id="f-q" type="search" placeholder="Search findings by title" value={draft.q ?? ""} onChange={set("q")} maxLength={100} />
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
      <button type="submit" className="btn sm"><Search size={13} aria-hidden="true" />Search</button>
      <button type="button" className="btn ghost sm" onClick={clear}><X size={13} aria-hidden="true" />Clear</button>
    </form>
  );
}

/** The same row for the runs list: text in the task, run status, and whether a fault was injected (`faults` = names seen in the runs). */
export function RunFilters({ value, onApply, faults }: { value: RunFilter; onApply: (next: RunFilter) => void; faults: string[] }) {
  const [draft, setDraft] = useState<RunFilter>(value);
  const set = (k: keyof RunFilter) => (e: { target: { value: string } }) => setDraft({ ...draft, [k]: e.target.value });
  const submit = (e: FormEvent) => { e.preventDefault(); onApply(draft); };
  const clear = () => { setDraft({}); onApply({}); };
  return (
    <form className="filters" onSubmit={submit} role="search" aria-label="Filter runs">
      <div className="filters-q">
        <label htmlFor="r-q" className="sr-only">Search runs</label>
        <input id="r-q" type="search" placeholder="Search runs by order, e-mail or message" value={draft.q ?? ""} onChange={set("q")} maxLength={100} />
      </div>
      <div>
        <label htmlFor="r-status" className="sr-only">Run status</label>
        <select id="r-status" value={draft.status ?? ""} onChange={set("status")}>
          <option value="">Any status</option>
          {["completed", "errored", "running", "queued"].map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
      </div>
      <div>
        <label htmlFor="r-fault" className="sr-only">Condition</label>
        <select id="r-fault" value={draft.fault ?? ""} onChange={set("fault")}>
          <option value="">Any condition</option>
          {faults.map((f) => <option key={f} value={f}>Injected fault: {faultLabel(f).toLowerCase()}</option>)}
          <option value="none">Clean run</option>
        </select>
      </div>
      <button type="submit" className="btn sm" aria-label="Search runs now"><Search size={13} aria-hidden="true" />Search</button>
      <button type="button" className="btn ghost sm" onClick={clear} aria-label="Clear run filters"><X size={13} aria-hidden="true" />Clear</button>
    </form>
  );
}
