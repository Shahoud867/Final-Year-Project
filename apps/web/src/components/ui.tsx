import {
  ArrowLeft, CassetteTape, Check, CircleAlert, CircleCheck, CircleDashed, CircleHelp, CircleSlash, CircleX, Copy, Cpu,
  FlaskConical, Hourglass, Inbox, Info, LoaderCircle, RefreshCw, ShieldCheck, Syringe, TriangleAlert, X,
} from "lucide-react";
import { useEffect, useId, useRef } from "react";
import type { CSSProperties, ComponentType, KeyboardEvent as ReactKeyboardEvent, ReactNode } from "react";
import { LEVELS, LEVEL_NAME, delta, faultLabel, hashShort, label, modeLabel, show } from "../format";
import { useCopy } from "../hooks";

/** The five tones of the design system. Each is always shown with an icon and a word, never as colour alone. */
export type Tone = "ok" | "bad" | "warn" | "replay" | "neutral";
export type Icon = ComponentType<{ size?: number | string; className?: string; "aria-hidden"?: boolean | "true" | "false" }>;

const TONE: Record<string, Tone> = {
  completed: "ok", pass: "ok", confirmed: "ok", accepted: "ok", resolved: "ok", succeeded: "ok", ok: "ok", success: "ok",
  fail: "bad", errored: "bad", error: "bad", rejected: "bad", failed: "bad", failure: "bad",
  refuted: "neutral", skipped: "neutral", cancelled: "neutral",
  hypothesized: "replay", verifying: "replay", running: "replay", queued: "replay", evidence_supported: "replay", in_progress: "replay",
  inconclusive: "warn", abstain: "warn", wont_fix: "warn", open: "warn",
};
const TONE_ICON: Record<Tone, Icon> = { ok: CircleCheck, bad: CircleX, warn: TriangleAlert, replay: FlaskConical, neutral: CircleDashed };
const VALUE_ICON: Record<string, Icon> = {
  running: LoaderCircle, queued: Hourglass, verifying: LoaderCircle, in_progress: LoaderCircle, refuted: CircleSlash,
  abstain: CircleHelp, inconclusive: CircleHelp, accepted: ShieldCheck, resolved: ShieldCheck,
};

/** Tone of a status word from the API ("completed", "fail", "confirmed" ...). Unknown words are neutral. */
export const toneOf = (value: string): Tone => TONE[value] ?? "neutral";

/** Status pill: an icon and a word. `value` is an API status; `text` overrides the label, `tone` the colour. */
export function Badge({ value, text, tone, title, large }: { value: string; text?: string; tone?: Tone; title?: string; large?: boolean }) {
  const t = tone ?? toneOf(value);
  const I = VALUE_ICON[value] ?? TONE_ICON[t];
  const busy = value === "running" || value === "verifying" || value === "in_progress";
  return (
    <span className={`badge tone-${t}${large ? " lg" : ""}`} title={title}>
      <I size={12} aria-hidden="true" className={busy ? "spin" : undefined} />{text ?? label(value)}
    </span>
  );
}

/** Neutral metadata pill (ids, kinds, counts). Pass `tone` only when the value itself carries a status. */
export function Chip({ children, tone = "neutral", icon: I, title, mono }: { children: ReactNode; tone?: Tone; icon?: Icon; title?: string; mono?: boolean }) {
  return <span className={`chip tone-${tone}${mono ? " mono" : ""}`} title={title}>{I && <I size={12} aria-hidden="true" />}{children}</span>;
}

/** How the model answers of a run or experiment were produced: a recorded cassette or a live model. */
export function ModeBadge({ mode, model }: { mode: string; model?: string }) {
  const recorded = mode === "recorded";
  const title = recorded
    ? "Saved real model answers were replayed. Deterministic; no model was called."
    : mode === "live" ? "A model was called for this execution." : "Live model when one is reachable, otherwise the recorded cassette.";
  return (
    <span className={`chip tone-${recorded ? "neutral" : "replay"}`} title={title}>
      {recorded ? <CassetteTape size={12} aria-hidden="true" /> : <Cpu size={12} aria-hidden="true" />}
      {modeLabel(mode)}{model ? <span className="mono dim">{model}</span> : null}
    </span>
  );
}

/** Whether a fault was injected into a run (a test condition, labelled as such) or the run was clean. */
export function FaultBadge({ fault }: { fault: string | null | undefined }) {
  return fault
    ? <span className="chip tone-warn" title="A fault was injected on purpose to test detection. Analysis never reads it."><Syringe size={12} aria-hidden="true" />Injected fault: {faultLabel(fault).toLowerCase()}</span>
    : <span className="chip" title="No fault was injected."><Check size={12} aria-hidden="true" />Clean run</span>;
}

/** Verification level V0 to V3 as a four-bar ladder with its name. */
export function LevelBadge({ level, showName }: { level: string; showName?: boolean }) {
  const n = Math.max(0, ["V0", "V1", "V2", "V3"].indexOf(level));
  return (
    <span className={`level${n === 3 ? " full" : ""}`} title={LEVELS[level] ?? level}>
      <span className="level-bars" aria-hidden="true">{[0, 1, 2, 3].map((i) => <i key={i} className={i <= n ? "on" : undefined} />)}</span>
      {level}{showName && LEVEL_NAME[level] ? <span className="muted" style={{ fontFamily: "var(--font-sans)", fontWeight: 500 }}>{LEVEL_NAME[level]}</span> : null}
    </span>
  );
}

/** Button that copies a value; announces "Copied" to assistive technology. */
export function CopyButton({ value, label: what = "value" }: { value: string; label?: string }) {
  const [copied, copy] = useCopy();
  return (
    <button type="button" className={`copy${copied ? " done" : ""}`} onClick={(e) => { e.stopPropagation(); copy(value); }}
            aria-label={copied ? `Copied ${what}` : `Copy ${what}`} title={copied ? "Copied" : `Copy ${what}`}>
      {copied ? <Check size={13} aria-hidden="true" /> : <Copy size={13} aria-hidden="true" />}
    </button>
  );
}

/** A SHA-256 or id in monospace, shortened for display, with the full value on hover and a copy button. */
export function Hash({ value, length = 12, label: what = "hash" }: { value: string | null | undefined; length?: number; label?: string }) {
  if (!value) return <span className="dim">n/a</span>;
  return <span className="hash" title={value}>{value.length > length ? hashShort(value, length) : value}<CopyButton value={value} label={what} /></span>;
}

/** Titled surface. With a `title` it renders a <section> labelled by its heading. */
export function Card({ title, icon: I, sub, actions, children, className = "", tone, flush, id, level = 2 }: {
  title?: ReactNode; icon?: Icon; sub?: ReactNode; actions?: ReactNode; children?: ReactNode; className?: string;
  tone?: Tone; flush?: boolean; id?: string; level?: 2 | 3;
}) {
  const auto = useId();
  const hid = `${id ?? auto}-h`;
  const H = level === 2 ? "h2" : "h3";
  const cls = `card${flush ? " flush" : ""}${tone && tone !== "neutral" ? ` tone-${tone}` : ""} ${className}`.trim();
  if (!title) return <div className={cls} id={id}>{children}</div>;
  return (
    <section className={cls} id={id} aria-labelledby={hid}>
      <div className="card-head">
        <div className="card-title">{I && <I size={15} aria-hidden="true" />}<H id={hid}>{title}</H></div>
        {sub ? <span className="card-sub">{sub}</span> : null}
        {actions ? <div className="card-actions">{actions}</div> : null}
      </div>
      {children}
    </section>
  );
}

/** Telemetry tile: a label, one number and a line of context. The number must come from the API. */
export function Stat({ label: name, value, unit, sub, icon: I, hint, children }: {
  label: string; value: ReactNode; unit?: string; sub?: ReactNode; icon?: Icon; hint?: string; children?: ReactNode;
}) {
  return (
    <div className="card stat">
      <div className="stat-label">{I && <I size={13} aria-hidden="true" />}{name}{hint ? <InfoTip text={hint} label={`About ${name}`} /> : null}</div>
      <div className="stat-value">{value}{unit ? <small>{unit}</small> : null}</div>
      {sub ? <div className="stat-sub">{sub}</div> : null}
      {children}
    </div>
  );
}

export interface TabDef { id: string; label: string; count?: number | string; icon?: Icon }

/** Tab list (arrow keys move between tabs). Render the panel yourself with <TabPanel>. */
export function Tabs({ tabs, value, onChange, label: name, idBase }: { tabs: TabDef[]; value: string; onChange: (id: string) => void; label: string; idBase: string }) {
  const onKey = (e: ReactKeyboardEvent<HTMLDivElement>) => {
    const i = tabs.findIndex((t) => t.id === value);
    const next = e.key === "ArrowRight" ? tabs[(i + 1) % tabs.length] : e.key === "ArrowLeft" ? tabs[(i - 1 + tabs.length) % tabs.length]
      : e.key === "Home" ? tabs[0] : e.key === "End" ? tabs[tabs.length - 1] : undefined;
    if (!next) return;
    e.preventDefault();
    onChange(next.id);
    document.getElementById(`${idBase}-tab-${next.id}`)?.focus();
  };
  return (
    <div className="tabs" role="tablist" aria-label={name} onKeyDown={onKey}>
      {tabs.map((t) => (
        <button key={t.id} type="button" role="tab" id={`${idBase}-tab-${t.id}`} className="tab" aria-selected={t.id === value}
                aria-controls={`${idBase}-panel-${t.id}`} tabIndex={t.id === value ? 0 : -1} onClick={() => onChange(t.id)}>
          {t.icon && <t.icon size={14} aria-hidden="true" />}{t.label}
          {t.count !== undefined ? <span className="tab-count">{t.count}</span> : null}
        </button>
      ))}
    </div>
  );
}

export function TabPanel({ idBase, id, active, children, className }: { idBase: string; id: string; active: boolean; children: ReactNode; className?: string }) {
  return (
    <div role="tabpanel" id={`${idBase}-panel-${id}`} aria-labelledby={`${idBase}-tab-${id}`} hidden={!active} className={className}>
      {active ? children : null}
    </div>
  );
}

export interface SegOption<T extends string> { value: T; label: string; icon?: Icon; disabled?: boolean; title?: string }

/** Single choice shown as a row of buttons (a radio group underneath). */
export function Segmented<T extends string>({ options, value, onChange, label: name, name: group }: {
  options: SegOption<T>[]; value: T; onChange: (v: T) => void; label: string; name: string;
}) {
  return (
    <div className="segmented" role="radiogroup" aria-label={name}>
      {options.map((o) => (
        <label key={o.value} title={o.title}>
          <input type="radio" name={group} value={o.value} checked={o.value === value} disabled={o.disabled} onChange={() => onChange(o.value)} />
          <span>{o.icon && <o.icon size={13} aria-hidden="true" />}{o.label}</span>
        </label>
      ))}
    </div>
  );
}

/** A small "?" that explains a term on hover or keyboard focus. Keep the text to one or two sentences. */
export function InfoTip({ text, label: name = "More information", align }: { text: string; label?: string; align?: "start" | "end" | "below" }) {
  const id = useId();
  return (
    <span className={`tip${align ? ` ${align}` : ""}`}>
      <button type="button" className="tip-btn" aria-label={name} aria-describedby={id}><Info size={13} aria-hidden="true" /></button>
      <span role="tooltip" id={id} className="tip-bubble">{text}</span>
    </span>
  );
}

const FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

/**
 * Side panel over the page (a bottom sheet on phones). Modal: focus moves in, Tab stays inside, Escape or the
 * backdrop closes it, and focus returns to whatever opened it.
 */
export function Drawer({ open, onClose, title, sub, children, footer, width }: {
  open: boolean; onClose: () => void; title: ReactNode; sub?: ReactNode; children: ReactNode; footer?: ReactNode; width?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const hid = useId();
  useEffect(() => {
    if (!open) return;
    const opener = document.activeElement as HTMLElement | null;
    ref.current?.querySelector<HTMLElement>("[data-autofocus]")?.focus();
    return () => { opener?.focus?.(); };
  }, [open]);
  if (!open) return null;
  const onKey = (e: ReactKeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Escape") { e.stopPropagation(); onClose(); return; }
    if (e.key !== "Tab" || !ref.current) return;
    const items = [...ref.current.querySelectorAll<HTMLElement>(FOCUSABLE)];
    const first = items[0], last = items[items.length - 1];
    if (!first || !last) return;
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  };
  return (
    <>
      <div className="drawer-scrim" onClick={onClose} />
      <div ref={ref} className="drawer" role="dialog" aria-modal="true" aria-labelledby={hid} onKeyDown={onKey}
           style={width ? ({ "--drawer-w": `${width}px` } as CSSProperties) : undefined}>
        <div className="drawer-head">
          <div className="grow stack tight"><h2 id={hid}>{title}</h2>{sub ? <div className="muted small">{sub}</div> : null}</div>
          <button type="button" className="btn ghost icon sm" onClick={onClose} aria-label="Close panel" data-autofocus><X size={15} aria-hidden="true" /></button>
        </div>
        <div className="drawer-body">{children}</div>
        {footer ? <div className="drawer-foot">{footer}</div> : null}
      </div>
    </>
  );
}

function tokens(text: string): ReactNode[] {
  const out: ReactNode[] = [];
  const re = /("(?:\\.|[^"\\])*")(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?/g;
  let last = 0, m: RegExpExecArray | null, i = 0;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(text.slice(last, m.index));
    const cls = m[1] ? (m[2] ? "j-key" : "j-str") : m[3] ? "j-lit" : "j-num";
    out.push(<span key={i++} className={cls}>{m[1] ?? m[0]}</span>);
    if (m[2]) out.push(m[2]);
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}

/** Pretty-printed, lightly coloured JSON in a scrollable, keyboard-focusable box with a copy button. */
export function JsonView({ value, label: name = "JSON", maxHeight }: { value: unknown; label?: string; maxHeight?: number }) {
  const text = JSON.stringify(value, null, 2) ?? "null";
  return (
    <div className="json" style={maxHeight ? ({ "--json-max": `${maxHeight}px` } as CSSProperties) : undefined}>
      <pre tabIndex={0} role="group" aria-label={name}>{tokens(text)}</pre>
      <CopyButton value={text} label={name} />
    </div>
  );
}

/** Definition list of label and value pairs. */
export function KV({ items }: { items: [string, ReactNode][] }) {
  return <dl className="kv">{items.map(([k, v]) => <FragmentRow key={k} k={k} v={v} />)}</dl>;
}
function FragmentRow({ k, v }: { k: string; v: ReactNode }) {
  return <><dt>{k}</dt><dd>{v}</dd></>;
}

/**
 * What a check observed next to what it expected (the source of truth or the step's own contract), with the
 * difference for numbers. Pass the values straight from the API.
 */
export function Compare({ observed, expected, observedLabel = "Observed", expectedLabel = "Expected", match }: {
  observed: unknown; expected: unknown; observedLabel?: string; expectedLabel?: string; match?: boolean;
}) {
  const d = delta(observed, expected);
  return (
    <div className={`compare${match ? " match" : ""}`}>
      <div className="compare-cell observed"><div className="eyebrow">{observedLabel}</div><div className="compare-value">{show(observed)}</div></div>
      <div className="compare-cell expected"><div className="eyebrow">{expectedLabel}</div><div className="compare-value">{show(expected)}</div></div>
      {d ? <div className="compare-delta"><span className="eyebrow">Difference</span><span className={d === "0" ? "t-ok" : "t-bad"}>{d}</span></div> : null}
    </div>
  );
}

/** Inline callout. Use role="alert" only for errors the user must act on. */
export function Notice({ tone = "neutral", icon: I, title, children, role, action }: {
  tone?: Tone; icon?: Icon; title?: ReactNode; children?: ReactNode; role?: "alert" | "status" | "note"; action?: ReactNode;
}) {
  const Ico = I ?? (tone === "bad" ? CircleAlert : tone === "warn" ? TriangleAlert : tone === "ok" ? CircleCheck : Info);
  return (
    <div className={`alert tone-${tone}`} role={role}>
      <Ico size={15} aria-hidden="true" />
      <div className="alert-body">{title ? <div className="alert-title">{title}</div> : null}{children}</div>
      {action}
    </div>
  );
}

export function ErrorBox({ message, onRetry }: { message: string; onRetry?: () => void }) {
  if (!message) return null;
  return (
    <div className="alert tone-bad" role="alert">
      <CircleAlert size={15} aria-hidden="true" />
      <div className="alert-body">{message}</div>
      {onRetry && <button type="button" className="btn sm" onClick={onRetry}><RefreshCw size={12} aria-hidden="true" />Try again</button>}
    </div>
  );
}

export function Loading({ text = "Loading…" }: { text?: string }) {
  return <p className="loading" role="status"><LoaderCircle size={14} className="spin" aria-hidden="true" />{text}</p>;
}

/** Placeholder lines while a panel loads. */
export function Skeleton({ lines = 3 }: { lines?: number }) {
  return <div aria-hidden="true">{Array.from({ length: lines }, (_, i) => <span key={i} className="skeleton" style={{ width: `${92 - i * 14}%` }} />)}</div>;
}

/** Empty state: say what the area is for and give the one action that fills it. */
export function Empty({ children, title, icon: I = Inbox, action }: { children?: ReactNode; title?: string; icon?: Icon; action?: ReactNode }) {
  return (
    <div className="empty">
      <I size={22} aria-hidden="true" />
      {title ? <div className="empty-title">{title}</div> : null}
      {children ? <div>{children}</div> : null}
      {action}
    </div>
  );
}

/** Progress of a background job. Without a known total it shows an indeterminate bar, not an invented percentage. */
export function Progress({ done, total, label: name = "Progress" }: { done: number; total: number; label?: string }) {
  const known = total > 0;
  const width = known ? Math.round((done / total) * 100) : 0;
  return (
    <div className={`progress${known ? "" : " indeterminate"}`} role="progressbar" aria-label={name}
         aria-valuenow={known ? done : undefined} aria-valuemin={0} aria-valuemax={known ? total : undefined}>
      <div style={{ width: `${width}%` }} />
    </div>
  );
}

/** Page title block: optional back link and eyebrow, the h1, a line of context, metadata chips and actions. */
export function PageHeader({ title, eyebrow, sub, meta, actions, back }: {
  title: ReactNode; eyebrow?: ReactNode; sub?: ReactNode; meta?: ReactNode; actions?: ReactNode; back?: { href: string; label: string };
}) {
  return (
    <div className="page-head">
      <div className="page-head-main">
        {back ? <a className="back" href={back.href}><ArrowLeft size={13} aria-hidden="true" />{back.label}</a> : null}
        {eyebrow ? <div className="eyebrow">{eyebrow}</div> : null}
        <h1>{title}</h1>
        {sub ? <p className="page-sub">{sub}</p> : null}
        {meta ? <div className="page-meta">{meta}</div> : null}
      </div>
      {actions ? <div className="row">{actions}</div> : null}
    </div>
  );
}

/** Label, control, hint and error wired for assistive technology. Give the control `id` and spread `describe(id, ...)`. */
export function Field({ id, label: name, hint, error, required, children, className = "" }: {
  id: string; label: ReactNode; hint?: ReactNode; error?: string; required?: boolean; children: ReactNode; className?: string;
}) {
  return (
    <div className={`field${required ? " required" : ""} ${className}`.trim()}>
      <label htmlFor={id}>{name}</label>
      {children}
      {error ? <div className="field-error" id={`${id}-err`}><CircleAlert size={13} aria-hidden="true" />{error}</div> : null}
      {hint ? <div className="hint" id={`${id}-hint`}>{hint}</div> : null}
    </div>
  );
}

/** aria attributes for a control inside <Field>: points at its hint and error and marks it invalid. */
export function describe(id: string, opts: { hint?: boolean; error?: string }): { "aria-describedby"?: string; "aria-invalid"?: boolean } {
  const ids = [opts.error ? `${id}-err` : "", opts.hint ? `${id}-hint` : ""].filter(Boolean).join(" ");
  return { "aria-describedby": ids || undefined, "aria-invalid": opts.error ? true : undefined };
}
