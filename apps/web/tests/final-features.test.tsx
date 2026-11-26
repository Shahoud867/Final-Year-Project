import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import axe from "axe-core";
import { Attempts } from "../src/components/Verify";
import { Evaluation } from "../src/pages/Evaluation";
import { FindingDetail } from "../src/pages/FindingDetail";
import { Lab } from "../src/pages/Lab";
import type { Batch, Evaluation as EvalData, Investigation, Rate } from "../src/types";
import { examples, health, workflows } from "./fixtures";
import { finding, mockApi } from "./helpers";

const rate = (k: number, n: number): Rate => ({ k, n, rate: n ? k / n : null, ci95: [0.3, 1] });
const evaluation: EvalData = {
  id: "2026-11-15_benchmark-v0",
  meta: { date: "2026-11-15", model: "llama3.2:3b", mode: "live", prereg_sha256: "ab".repeat(32), git_head: "21eba51448",
    git_dirty: true, n_tasks: 1, faults: ["stale_price"], n: 5, m: 2, budget: 21 },
  metrics: {
    detection: rate(1, 1), detection_by_fault: { stale_price: rate(1, 1) }, clean_runs_with_finding: rate(0, 1),
    llm_judge_top1: rate(0, 1),
    top1: Object.fromEntries(["100", "60", "40"].map((lv) => [lv, {
      last_agent: rate(0, 1), earliest_check: rate(1, 1), granite_rank: rate(1, 1), granite_verified: rate(1, 1),
    }])),
    nondeterminism: { placebo_vr1_confirms: rate(0, 1), placebo_single_replay_confirms: rate(1, 1),
      origin_vr1_confirms: rate(1, 1), origin_single_replay_confirms: rate(1, 1) },
  },
  rows: [{ order_id: "#W1", fault: "none", status: "completed", detected: false, findings: [] },
    { order_id: "#W1", fault: "stale_price", status: "completed", detected: true, findings: ["CHK-OUT-1"], origin: "s2" }],
};
const batch: Batch = {
  id: "bat_1", workflow_key: "refund_desk", status: "done", llm_mode: "recorded", faults: ["stale_price", "none"],
  task_count: 2, seed: 1, created_at: "2026-11-15T10:00:00Z", finished_at: "2026-11-15T10:01:00Z",
  groups: { stale_price: { runs: 2, finished: 2, completed: 2, errored: 0, with_finding: 2 },
    none: { runs: 2, finished: 2, completed: 2, errored: 0, with_finding: 0 } },
  runs: [],
};
const investigation: Investigation = {
  id: "inv_1", finding_id: "fnd_1", status: "done", llm_mode: "recorded", n: 5, m: 2, budget: 21, replays_used: 14,
  outcome: "confirmed", confirmed_step: "s2", error: "", created_at: "2026-11-15T10:00:00Z", finished_at: null,
  attempts: [
    { step_id: "s4", agent: "Refund Calculator", status: "verified", verdict: "refuted", replays_used: 7, reason: "" },
    { step_id: "s2", agent: "Order Lookup", status: "verified", verdict: "confirmed", replays_used: 7, reason: "" },
    { step_id: "s1", agent: "Intake", status: "not_reached", replays_used: 0, reason: "the replay budget was spent" },
  ],
};

async function violations(container: HTMLElement) {
  const res = await axe.run(container, { rules: { "color-contrast": { enabled: false }, region: { enabled: false } } });
  return res.violations.map((v) => v.id);
}

describe("Investigate", () => {
  it("lists every suspect tried, in order, with its verdict or why it was not tried", () => {
    render(<Attempts inv={investigation} />);
    expect(screen.getByText("Origin confirmed: Order Lookup")).toBeInTheDocument();
    const rows = screen.getAllByRole("listitem");
    expect(rows.map((r) => r.textContent)).toEqual([
      expect.stringContaining("Refund Calculator"), expect.stringContaining("Order Lookup"), expect.stringContaining("Not reached"),
    ]);
    expect(screen.getByText("14/21 replays")).toBeInTheDocument();
  });

  it("starts an investigation with the chosen budget and shows the result", async () => {
    const calls = mockApi({
      "GET /findings/fnd_1": () => finding(),
      "GET /runs/run_1/graph": () => ({ nodes: [], edges: [] }),
      "POST /findings/fnd_1/investigations": () => ({ job_id: "job_1", investigation_id: "inv_1" }),
      "GET /jobs/job_1": () => ({ id: "job_1", status: "succeeded", progress_done: 14, progress_total: 21, message: "finished" }),
      "GET /investigations/inv_1": () => investigation,
    });
    const user = userEvent.setup();
    render(<FindingDetail id="fnd_1" />);
    const budget = await screen.findByLabelText("Replay budget");
    await user.clear(budget);
    await user.type(budget, "14");
    await user.click(screen.getByRole("button", { name: "Investigate" }));
    expect(await screen.findByText("Origin confirmed: Order Lookup")).toBeInTheDocument();
    const sent = calls.find((c) => c.url.endsWith("/investigations"));
    expect(JSON.parse(String(sent?.init?.body))).toEqual({ n: 5, m: 2, budget: 14 });
  });

  it("refuses a budget smaller than one experiment", async () => {
    mockApi({ "GET /findings/fnd_1": () => finding(), "GET /runs/run_1/graph": () => ({ nodes: [], edges: [] }) });
    const user = userEvent.setup();
    render(<FindingDetail id="fnd_1" />);
    const budget = await screen.findByLabelText("Replay budget");
    await user.clear(budget);
    await user.type(budget, "3");
    expect(screen.getByText("Use 7 to 60")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Investigate" })).toBeDisabled();
  });

  it("offers the regression export only once an origin is confirmed", async () => {
    mockApi({ "GET /findings/fnd_1": () => finding(), "GET /runs/run_1/graph": () => ({ nodes: [], edges: [] }) });
    render(<FindingDetail id="fnd_1" />);
    expect(await screen.findByRole("button", { name: /Export regression test/ })).toBeDisabled();
  });
});

describe("Fault Lab", () => {
  const routes = {
    "GET /workflows/refund_desk/examples": () => examples,
    "GET /workflows": () => [{ ...workflows[0], faults: ["dropped_item", "handoff_drift", "stale_price"] }],
    "GET /batches/bat_1": () => batch,
    "GET /batches": () => [batch],
    "POST /batches": () => ({ job_id: "job_b", batch_id: "bat_1" }),
    "GET /jobs/job_b": () => ({ id: "job_b", status: "succeeded", progress_done: 4, progress_total: 4, message: "done" }),
    "GET /health": () => health,
  };

  it("computes the plan, generates the batch and reads detection per condition", async () => {
    const calls = mockApi(routes);
    const user = userEvent.setup();
    render(<Lab />);
    const delivered = examples.filter((e) => e.label.includes("(delivered)")).length;
    expect(await screen.findByText(`${delivered * 4} runs`)).toBeInTheDocument();
    await user.click(screen.getByRole("checkbox", { name: /Handoff drift/ }));
    expect(screen.getByText(`${delivered * 3} runs`)).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Generate" }));
    const result = await screen.findByRole("table", { name: /Batch bat_1/ });
    expect(within(result).getByText("2 of 2 faulty runs detected")).toBeInTheDocument();
    expect(within(result).getByText(/0 of 2 clean runs flagged/)).toBeInTheDocument();
    const sent = JSON.parse(String(calls.find((c) => c.init?.method === "POST")?.init?.body));
    expect(sent.faults).toEqual(["stale_price", "dropped_item", "none"]);
  });

  it("has no accessibility violations", async () => {
    mockApi(routes);
    const { container } = render(<Lab />);
    await screen.findByRole("checkbox", { name: /Stale price/ });
    expect(await violations(container)).toEqual([]);
  }, 30_000);
});

describe("Evaluation", () => {
  const routes = {
    "GET /evaluations/2026-11-15_benchmark-v0": () => evaluation,
    "GET /evaluations": () => [{ id: evaluation.id, date: "2026-11-15", mode: "live", model: "m", runs: 2, complete: true, metrics: evaluation.metrics }],
  };

  it("shows the measured table with intervals, ties included, and the protocol hash", async () => {
    mockApi(routes);
    render(<Evaluation />);
    const table = await screen.findByRole("table", { name: /Top-1 attribution/ });
    expect(within(table).getAllByText("1/1").length).toBeGreaterThanOrEqual(9);
    expect(screen.getByRole("table", { name: /Confirmations/ })).toHaveTextContent("Placebo on an innocent step");
    expect(screen.getByText("abababababababab")).toBeInTheDocument();
  });

  it("says when there is nothing to show yet", async () => {
    mockApi({ "GET /evaluations": () => [] });
    render(<Evaluation />);
    expect(await screen.findByText("No results yet")).toBeInTheDocument();
  });

  it("has no accessibility violations", async () => {
    mockApi(routes);
    const { container } = render(<Evaluation />);
    await screen.findByRole("table", { name: /Top-1 attribution/ });
    expect(await violations(container)).toEqual([]);
  }, 30_000);
});
