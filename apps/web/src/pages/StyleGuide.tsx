import { FlaskConical, Inbox, Play, Trash2 } from "lucide-react";
import { useState } from "react";
import { RateAxis, ReplayDots } from "../components/Replay";
import {
  Badge, BrandMark, Card, Chip, Compare, Empty, ErrorBox, FaultBadge, Field, Hash, InfoTip, JsonView, Ladder, LevelBadge,
  Loading, Meter, ModeBadge, Notice, PageHeader, Progress, Segmented, Skeleton, Stat, TabPanel, Tabs, describe,
} from "../components/ui";
import type { Replay } from "../types";
import "../styles/pages/styleguide.css";

const SWATCHES = ["bg", "surface", "line", "text", "text-2", "text-3", "ok", "bad", "warn", "replay", "primary"];
const STATUSES = ["completed", "errored", "pass", "fail", "hypothesized", "verifying", "confirmed", "refuted", "inconclusive", "accepted", "rejected", "abstain"];
const replays: Replay[] = [
  ...[0, 1, 2, 3, 4].map((idx) => ({ kind: "intervention", idx, seed: 1000 + idx, completed: idx < 4, passed: idx < 4 ? idx !== 2 : null })),
  ...[0, 1].map((idx) => ({ kind: "control", idx, seed: 2000 + idx, completed: true, passed: false })),
];

/**
 * Every shared component in every state, on the current theme. It is the design system's reference and its test
 * surface: the accessibility suite runs on this page. Shipped only in development builds or with VITE_STYLEGUIDE=1.
 */
export function StyleGuide() {
  const [tab, setTab] = useState("one");
  const [seg, setSeg] = useState<"a" | "b">("a");
  return (
    <div className="page styleguide">
      <PageHeader eyebrow="Design system" title="Style guide" sub="Tokens and components as the product renders them. Switch the theme in the top bar to check both." />

      <Card title="Identity and colour">
        <div className="row loose">
          <span className="sg-mark"><BrandMark size={56} /></span>
          <ul className="sg-swatches">
            {SWATCHES.map((s) => <li key={s}><i style={{ background: `var(--${s})` }} /><span className="mono small">--{s}</span></li>)}
          </ul>
        </div>
      </Card>

      <Card title="Type scale">
        <div className="stack tight">
          <span style={{ fontSize: "var(--fs-xl)", fontWeight: 700 }}>30 · Order Lookup confirmed</span>
          <span style={{ fontSize: "var(--fs-lg)", fontWeight: 650 }}>22 · Page title</span>
          <span style={{ fontSize: "var(--fs-md)", fontWeight: 600 }}>17 · Card and section title</span>
          <span>15 · Body text, the default size for reading.</span>
          <span className="small">13 · Labels and metadata</span>
          <span className="mono">JetBrains Mono · CHK-OUT-1 · 662.23 · a3f9c1…</span>
        </div>
      </Card>

      <Card title="Buttons">
        <div className="row">
          <button type="button" className="btn primary"><Play size={14} aria-hidden="true" />Primary</button>
          <button type="button" className="btn">Secondary</button>
          <button type="button" className="btn ghost">Ghost</button>
          <button type="button" className="btn danger"><Trash2 size={14} aria-hidden="true" />Danger</button>
          <button type="button" className="btn" disabled>Disabled</button>
          <button type="button" className="btn sm">Small</button>
          <button type="button" className="btn icon" aria-label="Icon only"><FlaskConical size={15} aria-hidden="true" /></button>
        </div>
      </Card>

      <Card title="Status, metadata and evidence">
        <div className="stack">
          <div className="row tight">{STATUSES.map((s) => <Badge key={s} value={s} />)}</div>
          <div className="row tight">
            <Chip>metadata</Chip><Chip mono>CHK-OUT-1</Chip><Chip tone="replay">Verify a hypothesis</Chip>
            <FaultBadge fault="stale_price" /><FaultBadge fault={null} /><ModeBadge mode="recorded" /><ModeBadge mode="live" model="llama3.2:3b" />
          </div>
          <div className="row loose">{["V0", "V1", "V2", "V3"].map((l) => <Ladder key={l} level={l} />)}</div>
          <div className="row loose">{["V0", "V1", "V2", "V3"].map((l) => <LevelBadge key={l} level={l} showName />)}</div>
          <div className="row loose sg-meters">
            <Meter value={0.81} threshold={0.5} label="Suspect score" format={(v) => v.toFixed(2)} />
            <Meter value={0.4} label="Check coverage" tone="warn" format={(v) => `${Math.round(v * 100)}%`} />
          </div>
          <div className="row tight"><Hash value={"a".repeat(64)} label="example hash" /><InfoTip text="A tooltip explains one term in one or two sentences." label="About tooltips" /></div>
        </div>
      </Card>

      <Card title="Verification">
        <div className="grid cols-2">
          <div className="stack tight">
            <ReplayDots replays={replays} kind="intervention" planned={5} label="Fix replays (example)" />
            <ReplayDots replays={replays} kind="control" planned={2} label="Control replays (example)" />
          </div>
          <RateAxis fix={0.75} control={0} ciLow={0.3} ciHigh={0.95} />
        </div>
        <div className="sg-gap"><Compare observed={662} expected={662.23} observedLabel="Observed in the run" expectedLabel="Expected by the check" /></div>
      </Card>

      <Card title="Feedback">
        <div className="stack">
          <Notice tone="bad" title="Silent failure">The run completed without an error, but an outcome check shows the answer is wrong.</Notice>
          <Notice tone="warn" title="No verdict">Two replays needed model answers that are not in the recording.</Notice>
          <Notice tone="ok" title="No finding">Every check that could be evaluated passed.</Notice>
          <Notice tone="replay" title="Replays are running">Results appear as they arrive; the rest of the page stays usable.</Notice>
          <ErrorBox message="Cannot reach the Granite server. Is it running?" onRetry={() => undefined} />
          <Progress done={3} total={7} label="Example progress" />
          <Progress done={0} total={0} label="Example progress, total unknown" />
          <Loading />
          <Skeleton lines={2} />
          <Empty icon={Inbox} action={<button type="button" className="btn sm">New run</button>}>No findings yet. Run a task with a fault.</Empty>
        </div>
      </Card>

      <Card title="Navigation and input">
        <Tabs idBase="sg" label="Example tabs" value={tab} onChange={setTab} tabs={[{ id: "one", label: "Needs you", count: 3 }, { id: "two", label: "Decided", count: 12 }]} />
        <TabPanel idBase="sg" id="one" active={tab === "one"}><p className="small sg-gap">First panel.</p></TabPanel>
        <TabPanel idBase="sg" id="two" active={tab === "two"}><p className="small sg-gap">Second panel.</p></TabPanel>
        <div className="grid cols-2 sg-gap">
          <Field id="sg-ok" label="Replays with fix" hint="1 to 10">
            <input id="sg-ok" type="number" defaultValue={5} {...describe("sg-ok", { hint: true })} />
          </Field>
          <Field id="sg-bad" label="Controls" hint="0 to 5" error="Use 0 to 5">
            <input id="sg-bad" type="number" defaultValue={6} {...describe("sg-bad", { hint: true, error: "Use 0 to 5" })} />
          </Field>
        </div>
        <Segmented label="Mode" name="sg-mode" value={seg} onChange={setSeg} options={[{ value: "a", label: "Recorded" }, { value: "b", label: "Live" }]} />
      </Card>

      <div className="grid cols-3">
        <Stat label="Detection" value="30/30" sub="95% interval 89% to 100%" />
        <Stat label="False alarms" value="1/10" sub="a genuine model error" />
        <Stat label="Top-1 attribution" value="82%" />
      </div>

      <Card title="Data">
        <JsonView value={{ step_id: "s2", outputs: { items: [{ price: 452.03 }] }, ok: true }} label="Example JSON" maxHeight={160} />
      </Card>
    </div>
  );
}
