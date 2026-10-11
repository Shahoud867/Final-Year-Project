import { render } from "@testing-library/react";
import type { ReactElement } from "react";
import axe from "axe-core";
import App from "../src/App";
import { Graph } from "../src/components/Graph";
import { FindingDetail } from "../src/pages/FindingDetail";
import { Guide } from "../src/pages/Guide";
import { Home } from "../src/pages/Home";
import { NewRun } from "../src/pages/NewRun";
import { RunDetail } from "../src/pages/RunDetail";
import type { Graph as GraphData } from "../src/types";
import { finding, mockApi } from "./helpers";

// jsdom has no layout, so colour contrast is checked separately in a real browser (see the audit record).
const RULES = { rules: { "color-contrast": { enabled: false } } };

async function violations(container: HTMLElement) {
  const result = await axe.run(container, RULES);
  return result.violations.map((v) => `${v.id}: ${v.help} (${v.nodes.map((n) => n.target.join(" ")).join("; ")})`);
}

const run = {
  id: "run_1", workflow_key: "refund_desk", status: "completed", llm_mode: "recorded", model: "m", seed: 1,
  fault_type: "stale_price", task_input: { message: "Return the Pet Bed", email: "a@b.co", order_id: "#W1" }, error: "",
  created_at: "2026-10-07T10:00:00Z", finished_at: null, finding_count: 1, failed_checks: 1, trace_sha256: "a".repeat(64),
  trace: { steps: [], run: { final_output: { message: "Refund $1.00" } } }, findings: [finding()],
  check_results: [{ check_id: "CHK-OUT-1", scope: "outcome", step: "s5", type: "truth", severity: "high", status: "fail",
    observed: 1, expected: 2, message: "wrong amount" }],
  injected_fault: { fault_type: "stale_price", target_step: "s2", field_path: "items[0].price", original_value: 2,
    injected_value: 1, note: "n" },
};
const graph: GraphData = { nodes: [{ id: "task", label: "Task input", kind: "input", status: "ok" },
  { id: "s1", label: "Intake", kind: "llm", status: "failed", symptom: true }],
  edges: [{ source: "task", target: "s1", field: "message" }] };

const api = {
  "GET /health": () => ({ status: "ok", version: "0", llm_mode: "recorded", live_model_reachable: false, auth_required: false }),
  "GET /runs/run_1/graph": () => graph, "GET /runs/run_1": () => run, "GET /runs": () => [run],
  "GET /findings/fnd_1": () => finding({ status: "confirmed", allowed_actions: ["accept", "reject"] }),
  "GET /findings": () => [finding()],
  "GET /workflows/refund_desk/examples": () => [{ order_id: "#W1", email: "a@b.co", message: "m", label: "#W1 (delivered)" }],
};

describe("accessibility (axe-core, structure and semantics)", () => {
  afterEach(() => vi.unstubAllGlobals());
  const cases: [string, () => ReactElement][] = [
    ["Investigations", () => <Home />],
    ["New run", () => <NewRun />],
    ["Run detail", () => <RunDetail id="run_1" />],
    ["Finding", () => <FindingDetail id="fnd_1" />],
    ["How it works", () => <Guide />],
    ["App shell", () => <App />],
    ["Graph", () => <Graph graph={graph} />],
  ];
  it.each(cases)("%s has no violations", async (_name, view) => {
    mockApi(api);
    const { container, findAllByText } = render(view());
    await findAllByText(/./, undefined, { timeout: 2000 });
    await new Promise((r) => setTimeout(r, 150));
    expect(await violations(container)).toEqual([]);
  });
});
