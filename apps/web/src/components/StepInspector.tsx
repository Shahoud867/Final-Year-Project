import { ChevronLeft, ChevronRight } from "lucide-react";
import type { ReactNode } from "react";
import { duration, stepKind, when } from "../format";
import type { CheckResult, TraceStep } from "../types";
import { Computation } from "./CheckDetail";
import { Badge, Chip, Compare, Drawer, Hash, JsonView, KV, Notice } from "./ui";

/** How a step's answer was produced: a saved answer replayed, a model called, or plain code. */
export function produced(step: TraceStep): string {
  if (step.kind !== "llm") return "deterministic";
  return step.params?.recorded ? "recorded answer" : "live model";
}

const has = (v: unknown) => v !== null && v !== undefined;

/** Side panel for one step of a run: its contract checks, what it read, received and produced, and how it ran. */
export function StepInspector({ steps, checks, selected, onSelect, onClose }: {
  steps: TraceStep[]; checks: CheckResult[]; selected: string | null; onSelect: (id: string) => void; onClose: () => void;
}) {
  const i = steps.findIndex((s) => s.step_id === selected);
  const step = steps[i];
  const mine = step ? checks.filter((c) => c.step === step.step_id) : [];
  const prev = steps[i - 1], next = steps[i + 1];
  const p = step?.params;
  const exec: [string, ReactNode][] = step ? ([
    ["Answer", produced(step)],
    ["Model", step.model],
    ["Temperature", p?.temperature],
    ["Tokens", has(p?.tokens_in) || has(p?.tokens_out) ? `${p?.tokens_in ?? "n/a"} in, ${p?.tokens_out ?? "n/a"} out` : null],
    ["Prompt hash", step.prompt_hash ? <Hash key="h" value={step.prompt_hash} length={16} label="prompt hash" /> : null],
    ["Started", when(step.started_at) || null],
    ["Duration", duration(step.started_at, step.ended_at) || null],
  ] as [string, ReactNode][]).filter(([, v]) => has(v) && v !== "") : [];
  return (
    <Drawer open={!!step} onClose={onClose} width={560}
            title={step?.agent ?? ""}
            sub={step ? <span className="mono">{step.step_id} · {stepKind(step.kind)}{step.name ? ` · ${step.name}` : ""}</span> : undefined}
            footer={<>
              <button type="button" className="btn sm" disabled={!prev} onClick={() => prev && onSelect(prev.step_id)}><ChevronLeft size={13} aria-hidden="true" />{prev ? prev.agent : "First step"}</button>
              <button type="button" className="btn sm" disabled={!next} onClick={() => next && onSelect(next.step_id)}>{next ? next.agent : "Last step"}<ChevronRight size={13} aria-hidden="true" /></button>
            </>}>
      {step ? (
        <>
          {step.error ? <Notice tone="bad" title="This step raised an error">{step.error}</Notice> : null}
          <section className="stack tight" aria-label="Contract checks">
            <h3 className="eyebrow">Contract checks on this step</h3>
            {mine.length === 0 ? <p className="small dim">No check is defined on this step.</p> : mine.map((c) => (
              <div key={c.check_id} className="run-check">
                <div className="row tight"><Chip mono>{c.check_id}</Chip><Badge value={c.status} /><span className="small muted">{c.scope} check</span></div>
                <p className="small">{c.message}</p>
                {has(c.observed) || has(c.expected) ? <Compare observed={c.observed} expected={c.expected} match={c.status === "pass"} /> : null}
                <details><summary className="small">How it was computed</summary><Computation c={c} /></details>
              </div>
            ))}
          </section>
          {step.reads && step.reads.length > 0 ? (
            <section className="stack tight" aria-label="Reads">
              <h3 className="eyebrow">Reads</h3>
              <div className="row tight">{step.reads.map((r) => <Chip key={r} mono>{r}</Chip>)}</div>
            </section>
          ) : null}
          <section className="stack tight" aria-label="Received">
            <h3 className="eyebrow">Received</h3>
            <JsonView value={step.inputs} label={`${step.agent} received`} maxHeight={240} />
          </section>
          <section className="stack tight" aria-label="Produced">
            <h3 className="eyebrow">Produced</h3>
            <JsonView value={step.outputs} label={`${step.agent} produced`} maxHeight={280} />
          </section>
          {exec.length > 0 ? (
            <section className="stack tight" aria-label="Execution">
              <h3 className="eyebrow">Execution</h3>
              <KV items={exec} />
            </section>
          ) : null}
        </>
      ) : null}
    </Drawer>
  );
}
