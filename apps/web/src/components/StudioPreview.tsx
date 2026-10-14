import { FileCheck2, ListChecks, Workflow as WorkflowIcon } from "lucide-react";
import type { Graph as GraphData, Workflow } from "../types";
import { Graph } from "./Graph";
import { Card, Chip, Skeleton } from "./ui";

/** What is known about each fault the workflow offers: where it strikes and what it does (workflows/refund_desk/faults.py). */
export const FAULT_INFO: Record<string, { target: string; text: string }> = {
  stale_price: { target: "s2", text: "The order-lookup tool returns an outdated price for one requested item. No error is raised." },
};

/** Field rules, exactly as the server enforces them (registry.py RefundTask, schemas.py RunCreate). */
export const RULES: [string, string][] = [
  ["Customer message", "3 to 2000 characters"],
  ["Customer e-mail", "name@example.com, at most 190 characters"],
  ["Order id", "#W followed by 3 to 12 digits, for example #W1234567"],
  ["Fault", "none, or a fault this workflow offers"],
  ["Seed", "whole number, 0 to 2,000,000 (default 1)"],
  ["Execution mode", "recorded, live or auto"],
  ["Anything else", "refused: unknown keys are not accepted"],
];

/** The right-hand column of Task Studio: the pipeline that will run, its checks, the outputs and the input rules. */
export function StudioPreview({ workflow, loading, fault, running }: { workflow: Workflow | null; loading: boolean; fault: string; running: boolean }) {
  const steps = workflow?.steps ?? [];
  const graph: GraphData = {
    nodes: [{ id: "task", label: "Task input", kind: "input", status: "ok" }, ...steps.map((s) => ({ id: s.id, label: s.agent, kind: s.kind, status: "ok" as const }))],
    edges: steps.map((s, i) => ({ source: i === 0 ? "task" : steps[i - 1]!.id, target: s.id, field: "" })),
  };
  const target = FAULT_INFO[fault]?.target;
  const marks = target && steps.some((s) => s.id === target) ? { [target]: "fault" as const } : undefined;
  const agent = (id: string) => steps.find((s) => s.id === id)?.agent ?? id;
  const outcome = workflow?.checks.filter((c) => c.scope === "outcome") ?? [];
  const stepChecks = workflow?.checks.filter((c) => c.scope !== "outcome") ?? [];
  return (
    <div className="studio-preview">
      <Card title="What will run" icon={WorkflowIcon} sub={workflow ? `${workflow.title}: ${steps.length} agents in execution order` : undefined}>
        {loading && !workflow ? <Skeleton lines={4} /> : !workflow ? <p className="small dim">The workflow definition could not be loaded from the server.</p> : (
          <>
            <Graph graph={graph} plain running={running} marks={marks} notes={Object.fromEntries(steps.map((s) => [s.id, s.name]))} label="Execution order" />
            {running ? <p className="small muted" aria-hidden="true">Running. The server reports no per-step progress, so no step is singled out.</p> : null}
          </>
        )}
      </Card>
      {workflow ? (
        <Card title="Checks that will run" icon={ListChecks} sub={`${outcome.length} outcome, ${stepChecks.length} step`}>
          <ul className="studio-checks">
            {[...outcome, ...stepChecks].map((c) => (
              <li key={c.id}><Chip mono tone={c.scope === "outcome" ? "replay" : "neutral"}>{c.id}</Chip><span className="grow small">{c.name}</span><span className="small dim nowrap">{agent(c.step)}</span></li>
            ))}
          </ul>
        </Card>
      ) : null}
      <Card title="Accepted input" icon={FileCheck2} className="studio-rules">
        <dl className="kv">{RULES.map(([k, v]) => <div key={k} style={{ display: "contents" }}><dt>{k}</dt><dd>{v}</dd></div>)}</dl>
      </Card>
    </div>
  );
}
