/** "How it works": every feature with what it accepts and what it returns (panel actions A2, A3, A5). */
import {
  ArrowRight, BookOpen, ChevronRight, CornerDownRight, FileCode2, Fingerprint, FlaskConical, Gavel, ListChecks, Play, Radar, Route, Scale, Search, Siren,
} from "lucide-react";
import { Card, Chip, LevelBadge, PageHeader } from "../components/ui";
import type { Icon } from "../components/ui";
import { Vr1Explorer } from "../components/Vr1Explorer";
import { repoUrl } from "../delivery";
import { label } from "../format";
import { STAGE_INFO, TRANSITIONS, stage } from "../lib/lifecycle";
import "../styles/pages/guide.css";

type Feature = {
  step: string; name: string; purpose: string; inputs: string[]; outputs: string[]; where: string; href?: string;
  /** Id in the feature catalogue (docs/manuals/feature-catalogue.md). */
  feature: string; icon: Icon; stage: number;
};

/** The limits below are the ones the server enforces; the full rules are in the data dictionary (docs/diagrams). */
export const FEATURES: Feature[] = [
  {
    step: "1", name: "Run", purpose: "Execute a multi-agent workflow on one task and record every step.",
    inputs: [
      "Workflow: Refund Desk (five agents on real retail orders)",
      "Customer message: 3 to 2000 characters",
      "E-mail: name@example.com, at most 190 characters",
      "Order number: # W and seven digits, for example #W2378156",
      "Fault to inject (optional): none or stale price",
      "Seed: 0 to 2,000,000 · Model: recorded, live or auto",
    ],
    outputs: ["A run with each step's inputs and outputs (Granite Trace v1)", "A SHA-256 hash of the trace", "A data-flow graph"],
    where: "New run", href: "#/new", feature: "F1", icon: Play, stage: 1,
  },
  {
    step: "2", name: "Check", purpose: "Test the outcome and each step against rules and the source of truth. Runs automatically after every run.",
    inputs: ["The recorded trace", "The checks defined for the workflow", "The source of truth (orders and catalogue)"],
    outputs: ["Pass, fail, abstain or error for each check", "The observed and the expected value", "How the result was computed"],
    where: "Run page, Checks", feature: "F2", icon: ListChecks, stage: 1,
  },
  {
    step: "3", name: "Detect", purpose: "Open a finding when the outcome looks fine but a check shows it is wrong (a silent failure).",
    inputs: ["The failed outcome checks of a run"],
    outputs: ["A finding with title, severity and symptom step", "Verification level V0 (detected)"],
    where: "Investigations, Findings", feature: "F2", icon: Siren, stage: 1,
  },
  {
    step: "4", name: "Trace back", purpose: "Rank the steps where the wrong value most likely began.",
    inputs: ["The data flow between steps", "The step-level check results"],
    outputs: ["Up to 5 ranked hypotheses", "A score and a plain reason for each", "Verification level V1 (evidence)"],
    where: "Finding page, Where did it begin?", feature: "F3", icon: Route, stage: 2,
  },
  {
    step: "5", name: "Verify", purpose: "Test a hypothesis by replaying the workflow with that step corrected, and with controls.",
    inputs: ["One hypothesis", "Fix replays N: 1 to 10 (default 5)", "Control replays M: 0 to 5 (default 2)"],
    outputs: ["Verdict: confirmed, refuted or inconclusive (rule VR-1)", "Fix rate with a 95% interval, control rate", "Every replay stored", "Level V2 when confirmed"],
    where: "Finding page, Verify", feature: "F4", icon: FlaskConical, stage: 3,
  },
  {
    step: "6", name: "Review", purpose: "A person decides. No finding is closed by the software alone.",
    inputs: ["Decision: accept, reject, ask for more information, resolve or will not fix", "Comment: at most 2000 characters", "Reviewer name: 1 to 80 characters"],
    outputs: ["A new status, allowed only by the fixed lifecycle", "A review record with name and time", "Level V3 when accepted"],
    where: "Finding page, Your decision", feature: "F5", icon: Gavel, stage: 4,
  },
  {
    step: "7", name: "Record", purpose: "Keep the evidence so that someone else can check the conclusion.",
    inputs: ["Nothing to type: evidence is captured at each step above"],
    outputs: ["Evidence items, each with a SHA-256 hash that is re-checked on display", "An audit log of every action", "A report to download (Markdown or JSON)"],
    where: "Finding page, Evidence and Download report", feature: "F6", icon: Fingerprint, stage: 4,
  },
  {
    step: "8", name: "Find", purpose: "Come back to earlier work.",
    inputs: ["Search text: at most 100 characters", "Severity: critical, high, medium or low", "Verification level: V0 to V3"],
    outputs: ["The matching findings, newest first"],
    where: "Investigations", href: "#/", feature: "F7", icon: Radar, stage: 0,
  },
];

const LEVELS: [string, string, string][] = [
  ["V0", "Detected", "A check failed. Nothing is known about the cause yet."],
  ["V1", "Evidence", "The data flow points to a step. A suspicion with reasons, not proof."],
  ["V2", "Replay-verified", "Correcting that step fixed the outcome repeatedly and the controls did not."],
  ["V3", "Human-confirmed", "A reviewer accepted the verified finding."],
];

export function Guide() {
  const flow = FEATURES.filter((f) => f.stage > 0);
  return (
    <div className="page guide">
      <PageHeader eyebrow="Guide" title="How it works"
                  sub="A workflow of several AI agents gave an answer that looks fine but is wrong. Where did the error begin, and can that be shown?" />

      <Card title="The investigation, in order" icon={BookOpen} sub="seven steps, four stages, one verification level each">
        <ol className="guide-flow" aria-label="The investigation, in order">
          {STAGE_INFO.map((s, i) => (
            <li key={s.name} className="guide-stage">
              <div className="guide-stage-head"><span className="eyebrow">{s.name}</span><LevelBadge level={s.level} /></div>
              <ol className="guide-steps">
                {flow.filter((f) => f.stage === i + 1).map((f) => (
                  <li key={f.name}><a href={`#g-${f.step}`} className="guide-step"><f.icon size={15} aria-hidden="true" /><span className="mono dim">{f.step}</span>{f.name}</a></li>
                ))}
              </ol>
              {i < STAGE_INFO.length - 1 ? <ChevronRight size={16} className="guide-arrow" aria-hidden="true" /> : null}
            </li>
          ))}
        </ol>
      </Card>

      <div className="guide-grid">
        {FEATURES.map((f) => (
          <section className="card guide-feature" key={f.name} aria-labelledby={`g-${f.step}`}>
            <div className="guide-feature-head">
              <span className="guide-icon"><f.icon size={16} aria-hidden="true" /></span>
              <h2 id={`g-${f.step}`}>{f.step}. {f.name}</h2>
              <span className="spacer" />
              <Chip mono title="Feature id in the feature catalogue">{f.feature}</Chip>
            </div>
            <p className="muted">{f.purpose}</p>
            <div className="guide-io">
              <div>
                <h3>What it accepts</h3>
                <ul>{f.inputs.map((i) => <li key={i}>{i}</li>)}</ul>
              </div>
              <div>
                <h3>What you get</h3>
                <ul>{f.outputs.map((o) => <li key={o}>{o}</li>)}</ul>
              </div>
            </div>
            <p className="small dim guide-where"><CornerDownRight size={12} aria-hidden="true" />{f.href ? <a href={f.href}>{f.where}</a> : f.where}</p>
          </section>
        ))}
        <section className="card guide-feature" aria-labelledby="g-f8">
          <div className="guide-feature-head">
            <span className="guide-icon"><FileCode2 size={16} aria-hidden="true" /></span>
            <h2 id="g-f8">Explains itself</h2>
            <span className="spacer" />
            <Chip mono title="Feature id in the feature catalogue">F8</Chip>
          </div>
          <p className="muted">Every feature, input and output can be read without a document.</p>
          <ul className="checklist small">
            <li><BookOpen size={14} aria-hidden="true" /><span>This guide. A server test keeps the limits printed here equal to the ones enforced.</span></li>
            <li><FileCode2 size={14} aria-hidden="true" /><span><a href="/docs" target="_blank" rel="noreferrer">API reference</a>, generated from the code (OpenAPI).</span></li>
            <li><Fingerprint size={14} aria-hidden="true" /><span><a href={`${repoUrl()}/blob/main/packages/granite_core/schema/granite-trace-v1.schema.json`} target="_blank" rel="noreferrer">Granite Trace v1 schema</a>, the published input contract.</span></li>
          </ul>
        </section>
      </div>

      <Card title="How sure is a finding?" icon={Scale} id="g-levels">
        <ol className="guide-levels">
          {LEVELS.map(([id, name, meaning]) => (
            <li key={id}><LevelBadge level={id} /><strong>{name}</strong><span className="muted">{meaning}</span></li>
          ))}
        </ol>
        <p className="small muted">
          Invalid input is refused with a message next to the field. Nothing is stored until it has passed these rules.
        </p>
      </Card>

      <Card title="Rule VR-1" icon={FlaskConical} sub="why a single re-run proves nothing">
        <p className="muted guide-why">
          A language model can answer differently each time, so one lucky re-run can pass by chance. A hypothesis is confirmed only when
          correcting the suspect step fixes the outcome repeatedly <strong>and</strong> the same replays without the correction (controls) do not.
        </p>
        <Vr1Explorer />
      </Card>

      <Card title="Lifecycle rules" icon={Search} sub="enforced by the server; anything else is refused with HTTP 409">
        <div className="table-wrap">
          <table className="guide-life">
            <thead><tr><th>Stage</th><th>From</th><th>Event</th><th>To</th></tr></thead>
            <tbody>
              {TRANSITIONS.map(([from, event, to]) => (
                <tr key={`${from}-${event}`}>
                  <td className="small dim">{STAGE_INFO[stage(from) - 1]?.name}</td>
                  <td>{label(from)}</td>
                  <td className="mono small">{event.replace(/_/g, " ")}</td>
                  <td><span className="row tight"><ArrowRight size={12} aria-hidden="true" />{label(to)}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="small muted">The interface offers only the actions the server allows for the finding's current status. The table mirrors <a href={`${repoUrl()}/blob/main/packages/granite_core/granite_core/lifecycle.py`} target="_blank" rel="noreferrer">lifecycle.py</a>; a server test fails if they differ.</p>
      </Card>
    </div>
  );
}
