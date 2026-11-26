import { ArrowRight, FlaskConical, PanelRight, ShieldCheck, Workflow } from "lucide-react";
import { useState } from "react";
import { PAGE, api } from "../api";
import type { FindingFilter } from "../api";
import { Filters } from "../components/Filters";
import { QuickLook, kindLabel, verdictOf } from "../components/QuickLook";
import type { Selection } from "../components/QuickLook";
import { Badge, Card, Chip, Drawer, Empty, ErrorBox, FaultBadge, Ladder, Loading, PageHeader, TabPanel, Tabs, toneOf } from "../components/ui";
import { ago } from "../format";
import { useLoad, useMediaQuery } from "../hooks";
import { AWAITING_REVIEW, INBOX_GROUPS, VERIFIED, countIn } from "../lib/lifecycle";
import type { FindingSummary, RunSummary } from "../types";
import "../styles/pages/home.css";

const RECENT = 5;

/** Findings in the given statuses, newest first: one request per status (the API filters by one status at a time). */
async function findingsIn(statuses: string[] | null, filter: FindingFilter, limit: number): Promise<FindingSummary[]> {
  if (!statuses) return api.findings({ ...filter, limit });
  const lists = await Promise.all(statuses.map((status) => api.findings({ ...filter, status, limit })));
  return lists.flat().sort((a, b) => b.created_at.localeCompare(a.created_at)).slice(0, limit);
}

/** One line of totals; each number is read from the API, and a failed request reads "n/a", never zero. */
function Totals({ runs, runsFailed, counts, countsFailed }: {
  runs: RunSummary[] | null; runsFailed: boolean; counts: Record<string, number> | null; countsFailed: boolean;
}) {
  const all = runs ?? [];
  const done = all.filter((r) => r.status === "completed");
  const silent = done.filter((r) => r.finding_count > 0).length;
  const na = "n/a";
  return (
    <p className="inbox-totals">
      <span><strong className="num">{runsFailed ? na : all.length === 100 ? "100+" : all.length}</strong> runs</span>
      <span><strong className="num">{runsFailed ? na : silent}</strong> silent failures of {runsFailed ? na : done.length} completed</span>
      <span><strong className="num">{countsFailed ? na : countIn(counts, VERIFIED)}</strong> of {countsFailed ? na : sum(counts)} findings verified (V2+)</span>
      <span><strong className="num">{countsFailed ? na : countIn(counts, AWAITING_REVIEW)}</strong> awaiting a decision</span>
    </p>
  );
}

const sum = (counts: Record<string, number> | null | undefined) =>
  counts && !Array.isArray(counts) ? Object.values(counts).reduce((s, n) => s + (typeof n === "number" ? n : 0), 0) : 0;

export function Home() {
  const counts = useLoad(() => api.findingCounts(), []);
  const runs = useLoad(() => api.runs({ limit: 100 }), []);
  const [chosen, setChosen] = useState<string | null>(null);
  const [filter, setFilter] = useState<FindingFilter>({});
  const [limit, setLimit] = useState(PAGE);
  const [sel, setSel] = useState<Selection | null>(null);
  const narrow = useMediaQuery("(max-width: 1100px)");

  const groupCount = (statuses: string[]) => (counts.data ? countIn(counts.data, statuses) : undefined);
  const needs = groupCount(INBOX_GROUPS[0]!.statuses);
  // until the counts arrive the inbox shows everything; then it opens on the work that needs a person, if any
  const tab = chosen ?? (needs ? "needs" : "all");
  const group = INBOX_GROUPS.find((g) => g.id === tab);
  const findings = useLoad(() => findingsIn(group?.statuses ?? null, filter, limit), [tab, filter, limit]);
  const rows = findings.data ?? [];
  const filtered = Object.values(filter).some(Boolean);
  const total = sum(counts.data);
  const tabIds = [...INBOX_GROUPS.map((g) => g.id), "all"];
  const recent = (runs.data ?? []).slice(0, RECENT);
  const shown = narrow ? sel : sel ?? (rows[0] ? { kind: "finding" as const, id: rows[0].id } : null);
  const isSel = (id: string) => shown?.kind === "finding" && shown.id === id;
  const pick = (t: string) => { setChosen(t); setSel(null); setLimit(PAGE); };

  return (
    <div className="page inbox">
      <PageHeader title="Inbox" sub="Findings that need a decision first, then everything still being verified." />
      <ErrorBox message={counts.error || runs.error} onRetry={() => { counts.reload(); runs.reload(); }} />
      <Totals runs={runs.data} runsFailed={!!runs.error} counts={counts.data} countsFailed={!!counts.error} />

      <div className="home-work">
        <Card flush className="home-list">
          <Tabs idBase="inbox" label="Findings by who acts next" value={tab} onChange={pick}
                tabs={[...INBOX_GROUPS.map((g) => ({ id: g.id, label: g.label, count: groupCount(g.statuses) })),
                       { id: "all", label: "All", count: counts.data ? total : undefined }]} />
          {tabIds.filter((t) => t !== tab).map((t) => <TabPanel key={t} idBase="inbox" id={t} active={false}>{null}</TabPanel>)}
          <TabPanel idBase="inbox" id={tab} active className="home-panel">
            <Filters value={filter} onApply={(next) => { setFilter(next); setLimit(PAGE); setSel(null); }} />
            <ErrorBox message={findings.error} onRetry={findings.reload} />
            {findings.loading && !findings.data ? <Loading /> : null}
            {findings.data && rows.length === 0 && !findings.error ? (
              <Empty icon={ShieldCheck}
                     action={filtered || tab !== "all" ? undefined : <a className="btn primary sm" href="#/new"><FlaskConical size={13} aria-hidden="true" />New run</a>}>
                {filtered ? "No finding matches these filters."
                  : tab === "needs" ? "Nothing waits for a decision."
                    : tab === "verifying" ? "No finding is being verified."
                      : tab === "decided" ? "No finding has been decided yet."
                        : "No findings yet. Run a task with a fault."}
              </Empty>
            ) : null}
            {rows.length > 0 ? (
              <div className="table-wrap"><table className="home-table inbox-table">
                <thead><tr><th>Finding</th><th>Lead suspect</th><th>Evidence</th><th>Verdict</th><th>Opened</th><th><span className="sr-only">Quick look</span></th></tr></thead>
                <tbody>
                  {rows.map((f) => (
                    <tr key={f.id} className="click" aria-selected={isSel(f.id) || undefined} onClick={() => setSel({ kind: "finding", id: f.id })}>
                      <td><a className="home-title" href={`#/findings/${f.id}`} title={f.title}>{f.title}</a>
                        <div className="row tight small"><Badge value={f.status} /><Chip tone={f.kind === "silent_failure" ? "bad" : "neutral"}>{kindLabel(f.kind)}</Chip><Chip>{f.severity}</Chip></div></td>
                      <td>{f.lead ? <><strong>{f.lead.agent}</strong><div className="small dim mono">{f.lead.step_id}</div></> : <span className="dim">none</span>}</td>
                      <td><Ladder level={f.verification_level} compact /></td>
                      <td className="inbox-verdict"><span className={`t-${f.lead ? toneOf(f.lead.status === "open" ? "hypothesized" : f.lead.status) : "neutral"}`}>{verdictOf(f).word}</span>
                        {verdictOf(f).counts ? <div className="small dim mono">{verdictOf(f).counts}</div> : null}</td>
                      <td className="small nowrap">{ago(f.created_at)}</td>
                      <td><button type="button" className="btn ghost icon sm" aria-label={`Quick look at ${f.title}`} onClick={(e) => { e.stopPropagation(); setSel({ kind: "finding", id: f.id }); }}><PanelRight size={14} aria-hidden="true" /></button></td>
                    </tr>
                  ))}
                </tbody>
              </table></div>
            ) : null}
            {findings.data && findings.data.length >= limit ? <div className="home-more"><button type="button" className="btn sm" onClick={() => setLimit(limit + PAGE)}>Show more</button></div> : null}
          </TabPanel>
        </Card>

        {narrow ? (
          <Drawer open={!!sel} onClose={() => setSel(null)} title="Quick look" width={460}><QuickLook sel={sel} /></Drawer>
        ) : (
          <aside className="card home-inspector" aria-label="Quick look"><QuickLook sel={shown} /></aside>
        )}
      </div>

      <Card flush title="Recent runs" icon={Workflow} actions={<a className="btn ghost sm" href="#/runs">All runs<ArrowRight size={13} aria-hidden="true" /></a>}>
        {recent.length === 0 ? (
          <Empty icon={Workflow} action={runs.data ? <a className="btn sm" href="#/new">New run</a> : undefined}>{runs.loading ? "Loading runs…" : "Nothing has run yet."}</Empty>
        ) : (
          <div className="table-wrap"><table className="home-table">
            <thead><tr><th>Task</th><th>Status</th><th>Condition</th><th className="num">Findings</th><th>Started</th></tr></thead>
            <tbody>
              {recent.map((r) => (
                <tr key={r.id}>
                  <td><a href={`#/runs/${r.id}`}>{r.task_input.order_id}</a><div className="small mono dim">{r.id}</div></td>
                  <td><Badge value={r.status} /></td>
                  <td><FaultBadge fault={r.fault_type} /></td>
                  <td className="num">{r.finding_count}</td>
                  <td className="small nowrap">{ago(r.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table></div>
        )}
      </Card>
    </div>
  );
}
