/** "How it works": every feature with what it accepts and what it returns (panel actions A2, A3, A5). */

type Feature = { step: string; name: string; purpose: string; inputs: string[]; outputs: string[]; where: string; href?: string };

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
    where: "New run", href: "#/new",
  },
  {
    step: "2", name: "Check", purpose: "Test the outcome and each step against rules and the source of truth. Runs automatically after every run.",
    inputs: ["The recorded trace", "The checks defined for the workflow", "The source of truth (orders and catalogue)"],
    outputs: ["Pass, fail, abstain or error for each check", "The observed and the expected value", "How the result was computed"],
    where: "Run page, Checks",
  },
  {
    step: "3", name: "Detect", purpose: "Open a finding when the outcome looks fine but a check shows it is wrong (a silent failure).",
    inputs: ["The failed outcome checks of a run"],
    outputs: ["A finding with title, severity and symptom step", "Verification level V0 (detected)"],
    where: "Investigations, Findings",
  },
  {
    step: "4", name: "Trace back", purpose: "Rank the steps where the wrong value most likely began.",
    inputs: ["The data flow between steps", "The step-level check results"],
    outputs: ["Up to 5 ranked hypotheses", "A score and a plain reason for each", "Verification level V1 (evidence)"],
    where: "Finding page, Where did it begin?",
  },
  {
    step: "5", name: "Verify", purpose: "Test a hypothesis by replaying the workflow with that step corrected, and with controls.",
    inputs: ["One hypothesis", "Fix replays N: 1 to 10 (default 5)", "Control replays M: 0 to 5 (default 2)"],
    outputs: ["Verdict: confirmed, refuted or inconclusive (rule VR-1)", "Fix rate with a 95% interval, control rate", "Every replay stored", "Level V2 when confirmed"],
    where: "Finding page, Verify",
  },
  {
    step: "6", name: "Review", purpose: "A person decides. No finding is closed by the software alone.",
    inputs: ["Decision: accept, reject, ask for more information, resolve or will not fix", "Comment: at most 2000 characters", "Reviewer name: 1 to 80 characters"],
    outputs: ["A new status, allowed only by the fixed lifecycle", "A review record with name and time", "Level V3 when accepted"],
    where: "Finding page, Your decision",
  },
  {
    step: "7", name: "Record", purpose: "Keep the evidence so that someone else can check the conclusion.",
    inputs: ["Nothing to type: evidence is captured at each step above"],
    outputs: ["Evidence items, each with a SHA-256 hash that is re-checked on display", "An audit log of every action", "A report to download (Markdown or JSON)"],
    where: "Finding page, Evidence and Download report",
  },
  {
    step: "8", name: "Find", purpose: "Come back to earlier work.",
    inputs: ["Search text: at most 100 characters", "Severity: critical, high, medium or low", "Verification level: V0 to V3"],
    outputs: ["The matching findings, newest first"],
    where: "Investigations", href: "#/",
  },
];

const LEVELS: [string, string, string][] = [
  ["V0", "Detected", "A check failed. Nothing is known about the cause yet."],
  ["V1", "Evidence", "The data flow points to a step. A suspicion with reasons, not proof."],
  ["V2", "Replay-verified", "Correcting that step fixed the outcome repeatedly and the controls did not."],
  ["V3", "Human-confirmed", "A reviewer accepted the verified finding."],
];

export function Guide() {
  return (
    <>
      <h1>How it works</h1>
      <p className="muted">
        Granite investigates one question: a workflow of several AI agents gave an answer that looks fine but is wrong, so
        where did the error begin, and can that be shown? Each step below says what it accepts and what it gives back.
      </p>
      <ol className="stepper" aria-label="The investigation, in order">
        {FEATURES.slice(0, 7).map((f) => <li key={f.name}>{f.step}. {f.name}</li>)}
      </ol>

      <div className="grid cols-2">
        {FEATURES.map((f) => (
          <section className="card" key={f.name} aria-labelledby={`g-${f.step}`}>
            <h2 id={`g-${f.step}`}>{f.step}. {f.name}</h2>
            <p>{f.purpose}</p>
            <h3>What it accepts</h3>
            <ul>{f.inputs.map((i) => <li key={i}>{i}</li>)}</ul>
            <h3>What you get</h3>
            <ul>{f.outputs.map((o) => <li key={o}>{o}</li>)}</ul>
            <p className="small muted">Where: {f.href ? <a href={f.href}>{f.where}</a> : f.where}</p>
          </section>
        ))}
      </div>

      <section className="card" aria-labelledby="g-levels">
        <h2 id="g-levels">How sure is a finding?</h2>
        <div className="table-wrap"><table>
          <thead><tr><th>Level</th><th>Name</th><th>What it means</th></tr></thead>
          <tbody>{LEVELS.map(([id, name, meaning]) => <tr key={id}><td>{id}</td><td>{name}</td><td>{meaning}</td></tr>)}</tbody>
        </table></div>
        <p className="small muted">
          Invalid input is refused with a message next to the field. Nothing is stored until it has passed these rules.
        </p>
      </section>
    </>
  );
}
