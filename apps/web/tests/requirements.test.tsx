import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { needsComment } from "../src/components/Outcome";
import { FindingDetail } from "../src/pages/FindingDetail";
import { Home } from "../src/pages/Home";
import { RunDetail } from "../src/pages/RunDetail";
import { finding, mockApi } from "./helpers";

afterEach(() => { vi.unstubAllGlobals(); window.location.hash = ""; });

const erroredRun = {
  id: "run_1", workflow_key: "refund_desk", status: "errored", llm_mode: "live", model: "m", seed: 7, fault_type: "stale_price",
  task_input: { message: "Return the Pet Bed", email: "a@b.co", order_id: "#W1" }, error: "Intake: model endpoint unreachable",
  created_at: "2026-10-07T10:00:00Z", finished_at: null, finding_count: 0, failed_checks: 0, trace_sha256: null, trace: null,
  findings: [], check_results: [], injected_fault: null,
};

describe("FR-RUN-04 an errored run shows the reason and offers a retry", () => {
  it("re-runs the same task and fault, then opens the new run", async () => {
    const calls = mockApi({
      "GET /runs/run_1/graph": () => ({ nodes: [], edges: [] }),
      "GET /runs/run_1": () => erroredRun,
      "POST /runs": () => ({ run_id: "run_2", job_id: "job_2" }),
      "GET /jobs/job_2": () => ({ id: "job_2", status: "succeeded", progress_done: 1, progress_total: 1, message: "" }),
    });
    const user = userEvent.setup();
    render(<RunDetail id="run_1" />);
    expect(await screen.findByRole("alert")).toHaveTextContent("model endpoint unreachable");
    await user.click(screen.getByRole("button", { name: "Run again" }));
    await waitFor(() => expect(window.location.hash).toBe("#/runs/run_2"));
    const post = calls.find((c) => c.init?.method === "POST");
    expect(JSON.parse(String(post?.init?.body))).toMatchObject({ fault: "stale_price", seed: 7, mode: "auto", task_input: erroredRun.task_input });
  });
});

describe("FR-REV-01 reviewer decisions", () => {
  it("knows which decisions need a comment", () => {
    expect(needsComment("reject", "confirmed")).toBe(true);
    expect(needsComment("request_info", "confirmed")).toBe(true);
    expect(needsComment("wont_fix", "accepted")).toBe(true);
    expect(needsComment("accept", "inconclusive")).toBe(true);
    expect(needsComment("accept", "confirmed")).toBe(false);
  });

  it("asks for a reason before accepting an inconclusive finding", async () => {
    const calls = mockApi({
      "GET /findings/fnd_1": () => finding({ status: "inconclusive", allowed_actions: ["accept", "reject", "request_info"] }),
      "POST /findings/fnd_1/reviews": () => ({ id: "rev_1" }),
    });
    const user = userEvent.setup();
    render(<FindingDetail id="fnd_1" />);
    await user.click(await screen.findByRole("button", { name: "Accept" }));
    expect(await screen.findByText("Please say why (at least 5 characters).")).toBeInTheDocument();
    expect(calls.some((c) => c.init?.method === "POST")).toBe(false);
  });

  it("lets a reviewer ask for more information with a comment", async () => {
    const calls = mockApi({
      "GET /findings/fnd_1": () => finding({ status: "confirmed", allowed_actions: ["accept", "reject", "request_info"] }),
      "POST /findings/fnd_1/reviews": () => ({ id: "rev_1" }),
    });
    const user = userEvent.setup();
    render(<FindingDetail id="fnd_1" />);
    await user.type(await screen.findByLabelText("Comment"), "Which catalogue version?");
    await user.click(screen.getByRole("button", { name: "Ask for more information" }));
    await waitFor(() => expect(calls.some((c) => c.init?.method === "POST")).toBe(true));
    const post = calls.find((c) => c.init?.method === "POST");
    expect(JSON.parse(String(post?.init?.body))).toMatchObject({ decision: "request_info", comment: "Which catalogue version?" });
  });
});

describe("FR-HIS-01 findings can be searched and filtered", () => {
  it("sends the filters to the server and explains an empty result", async () => {
    const calls = mockApi({ "GET /runs": () => [], "GET /findings": () => [] });
    const user = userEvent.setup();
    render(<Home />);
    await screen.findByText(/No findings yet/);
    await user.type(screen.getByLabelText("Search findings"), "refund");
    await user.selectOptions(screen.getByLabelText("Severity"), "high");
    await user.selectOptions(screen.getByLabelText("Verification level"), "V2");
    await user.click(screen.getByRole("button", { name: "Search" }));
    expect(await screen.findByText("No finding matches these filters.")).toBeInTheDocument();
    const last = [...calls].reverse().find((c) => c.url.includes("/findings"))!;
    const params = new URL(last.url, "http://x").searchParams;
    expect([params.get("q"), params.get("severity"), params.get("level"), params.get("limit")]).toEqual(["refund", "high", "V2", "25"]);
  });
});

describe("Panel actions A2 and A3: every feature states what it accepts and what it returns", () => {
  it("lists each feature with its inputs and outputs, in workflow order", async () => {
    const { Guide, FEATURES } = await import("../src/pages/Guide");
    render(<Guide />);
    expect(screen.getByRole("heading", { level: 1, name: "How it works" })).toBeInTheDocument();
    expect(FEATURES.map((f) => f.name)).toEqual(["Run", "Check", "Detect", "Trace back", "Verify", "Review", "Record", "Find"]);
    for (const f of FEATURES) {
      expect(f.inputs.length).toBeGreaterThan(0);
      expect(f.outputs.length).toBeGreaterThan(0);
      expect(screen.getByRole("heading", { level: 2, name: `${f.step}. ${f.name}` })).toBeInTheDocument();
    }
    expect(screen.getAllByRole("heading", { level: 3, name: "What it accepts" })).toHaveLength(FEATURES.length);
    expect(screen.getByText(/Customer message: 3 to 2000 characters/)).toBeInTheDocument();
  });

  it("is reachable from the main navigation", async () => {
    mockApi({ "GET /health": () => ({ status: "ok", version: "0", llm_mode: "recorded", live_model_reachable: false, auth_required: false }) });
    window.location.hash = "#/guide";
    const { default: App } = await import("../src/App");
    render(<App />);
    expect(await screen.findByRole("heading", { level: 1, name: "How it works" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "How it works" })).toHaveAttribute("aria-current", "page");
  });
});
