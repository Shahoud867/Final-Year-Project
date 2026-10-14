import { render } from "@testing-library/react";
import type { ReactElement } from "react";
import axe from "axe-core";
import App from "../src/App";
import { Graph } from "../src/components/Graph";
import { Evidence } from "../src/pages/Evidence";
import { FindingDetail } from "../src/pages/FindingDetail";
import { Guide } from "../src/pages/Guide";
import { Home } from "../src/pages/Home";
import { NewRun } from "../src/pages/NewRun";
import { RunDetail } from "../src/pages/RunDetail";
import type { Graph as GraphData } from "../src/types";
import { erroredRun, examples, findingConfirmed, findingTraced, health, silentGraph, silentRun, workflows } from "./fixtures";
import { finding, mockApi } from "./helpers";

// jsdom has no layout, so colour contrast is checked separately in a real browser (see the audit record).
const RULES = { rules: { "color-contrast": { enabled: false } } };

async function violations(container: HTMLElement) {
  const result = await axe.run(container, RULES);
  return result.violations.map((v) => `${v.id}: ${v.help} (${v.nodes.map((n) => n.target.join(" ")).join("; ")})`);
}

afterEach(() => { vi.unstubAllGlobals(); sessionStorage.clear(); window.location.hash = ""; });

// A deliberately sparse API: optional fields missing, as an older record or another workflow could return them.
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

const sparse = {
  "GET /health": () => ({ status: "ok", version: "0", llm_mode: "recorded", live_model_reachable: false, auth_required: false }),
  "GET /runs/run_1/graph": () => graph, "GET /runs/run_1": () => run, "GET /runs": () => [run],
  "GET /findings/fnd_1": () => finding({ status: "confirmed", allowed_actions: ["accept", "reject"] }),
  "GET /findings": () => [finding()],
  "GET /workflows/refund_desk/examples": () => [{ order_id: "#W1", email: "a@b.co", message: "m", label: "#W1 (delivered)" }],
};

// The real payloads of a full investigation, so every panel of every screen is rendered.
const real = {
  "GET /health": () => health,
  "GET /findings/summary": () => ({ confirmed: 1, hypothesized: 1 }),
  [`GET /findings/${findingConfirmed.id}`]: () => findingConfirmed,
  "GET /findings/fnd_traced": () => ({ ...findingTraced, id: "fnd_traced" }),
  "GET /findings": () => [findingConfirmed],
  [`GET /runs/${silentRun.id}/graph`]: () => silentGraph,
  [`GET /runs/${silentRun.id}`]: () => silentRun,
  [`GET /runs/${erroredRun.id}/graph`]: () => ({ nodes: silentGraph.nodes.slice(0, 2), edges: [] }),
  [`GET /runs/${erroredRun.id}`]: () => erroredRun,
  "GET /runs": () => [silentRun, erroredRun],
  "GET /workflows/refund_desk/examples": () => examples,
  "GET /workflows": () => workflows,
  "GET https://api.github.com": () => ({ workflow_runs: [{ id: 1, name: "CI", run_number: 16, status: "completed", conclusion: "success",
    head_branch: "main", head_sha: "ee4b227000", event: "push", created_at: "2026-10-13T21:25:00Z", html_url: "https://github.com/x/y/actions/runs/1" }] }),
};

describe("accessibility (axe-core, structure and semantics)", () => {
  const cases: [string, Record<string, () => unknown>, () => ReactElement][] = [
    ["Investigations", sparse, () => <Home />],
    ["New run", sparse, () => <NewRun />],
    ["Run detail", sparse, () => <RunDetail id="run_1" />],
    ["Finding", sparse, () => <FindingDetail id="fnd_1" />],
    ["How it works", sparse, () => <Guide />],
    ["App shell", sparse, () => <App />],
    ["Graph", sparse, () => <Graph graph={graph} />],
    ["Investigations with a full investigation", real, () => <Home />],
    ["Task Studio with the workflow preview", real, () => <NewRun />],
    ["Pipeline trace of a silent failure", real, () => <RunDetail id={silentRun.id} />],
    ["Pipeline trace of an errored run", real, () => <RunDetail id={erroredRun.id} />],
    ["Verification lab with two experiments", real, () => <FindingDetail id={findingConfirmed.id} />],
    ["Verification lab before any verification", real, () => <FindingDetail id="fnd_traced" />],
    ["Evidence", real, () => <Evidence />],
    ["Pipeline graph with a marked path", real, () => <Graph graph={silentGraph} onSelect={() => undefined} marks={{ s2: "origin" }} path={["s2", "s3", "s5"]} legend />],
  ];
  it.each(cases)("%s has no violations", async (_name, api, view) => {
    mockApi(api);
    const { container, findAllByText } = render(view());
    await findAllByText(/./, undefined, { timeout: 2000 });
    await new Promise((r) => setTimeout(r, 250));
    expect(await violations(container)).toEqual([]);
    // axe walks the whole rendered tree; the larger pages need more than the 5 s default.
  }, 30_000);
});
