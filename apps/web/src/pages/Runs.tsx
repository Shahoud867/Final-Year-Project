import { FlaskConical, PanelRight, Workflow } from "lucide-react";
import { useState } from "react";
import { PAGE, api } from "../api";
import type { RunFilter } from "../api";
import { RunFilters } from "../components/Filters";
import { QuickLook } from "../components/QuickLook";
import type { Selection } from "../components/QuickLook";
import { Badge, Card, Drawer, Empty, ErrorBox, FaultBadge, Loading, ModeBadge, PageHeader } from "../components/ui";
import { ago } from "../format";
import { useLoad, useMediaQuery } from "../hooks";
import "../styles/pages/home.css";

/** Every run, newest first, filtered on the server; one run opens its trace, a row previews it. */
export function Runs() {
  const [filter, setFilter] = useState<RunFilter>({});
  const [limit, setLimit] = useState(PAGE);
  const [sel, setSel] = useState<Selection | null>(null);
  const narrow = useMediaQuery("(max-width: 1100px)");
  const runs = useLoad(() => api.runs({ ...filter, limit }), [filter, limit]);
  // the condition filter offers the faults that occur in recent runs
  const recent = useLoad(() => api.runs({ limit: 100 }), []);
  const faults = [...new Set((recent.data ?? []).map((r) => r.fault_type).filter((f): f is string => !!f))];
  const rows = runs.data ?? [];
  const filtered = Object.values(filter).some(Boolean);
  const shown = narrow ? sel : sel ?? (rows[0] ? { kind: "run" as const, id: rows[0].id } : null);

  return (
    <div className="page runs">
      <PageHeader title="Runs" sub="Every execution of the workflow, with the condition it ran under and what the checks found." />
      <div className="home-work">
        <Card flush className="home-list">
          <div className="home-panel">
            <RunFilters value={filter} faults={faults} onApply={(next) => { setFilter(next); setLimit(PAGE); setSel(null); }} />
            <ErrorBox message={runs.error} onRetry={runs.reload} />
            {runs.loading && !runs.data ? <Loading /> : null}
            {runs.data && rows.length === 0 && !runs.error ? (
              <Empty icon={Workflow} action={filtered ? undefined : <a className="btn primary sm" href="#/new"><FlaskConical size={13} aria-hidden="true" />New run</a>}>
                {filtered ? "No run matches these filters." : "Nothing has run yet."}
              </Empty>
            ) : null}
            {rows.length > 0 ? (
              <div className="table-wrap"><table className="home-table">
                <thead><tr><th>Run</th><th>Status</th><th>Condition</th><th>Mode</th><th className="num">Failed checks</th><th className="num">Findings</th><th>Started</th><th><span className="sr-only">Quick look</span></th></tr></thead>
                <tbody>
                  {rows.map((r) => (
                    <tr key={r.id} className="click" aria-selected={shown?.id === r.id || undefined} onClick={() => setSel({ kind: "run", id: r.id })}>
                      <td><a href={`#/runs/${r.id}`}>{r.task_input.order_id}</a><div className="small mono dim">{r.id}</div></td>
                      <td><Badge value={r.status} /></td>
                      <td><FaultBadge fault={r.fault_type} /></td>
                      <td><ModeBadge mode={r.llm_mode} /></td>
                      <td className="num">{r.failed_checks}</td>
                      <td className="num">{r.finding_count}</td>
                      <td className="small nowrap">{ago(r.created_at)}</td>
                      <td><button type="button" className="btn ghost icon sm" aria-label={`Quick look at run ${r.task_input.order_id} ${r.id}`} onClick={(e) => { e.stopPropagation(); setSel({ kind: "run", id: r.id }); }}><PanelRight size={14} aria-hidden="true" /></button></td>
                    </tr>
                  ))}
                </tbody>
              </table></div>
            ) : null}
            {runs.data && runs.data.length >= limit ? <div className="home-more"><button type="button" className="btn sm" onClick={() => setLimit(limit + PAGE)}>Show more</button></div> : null}
          </div>
        </Card>
        {narrow ? (
          <Drawer open={!!sel} onClose={() => setSel(null)} title="Quick look" width={460}><QuickLook sel={sel} /></Drawer>
        ) : (
          <aside className="card home-inspector" aria-label="Quick look"><QuickLook sel={shown} /></aside>
        )}
      </div>
    </div>
  );
}
