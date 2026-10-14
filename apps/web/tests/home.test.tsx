import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Home } from "../src/pages/Home";
import { cancelledRun, cleanRun, erroredRun, findingConfirmed, silentGraph, silentRun } from "./fixtures";
import { mockApi } from "./helpers";

afterEach(() => { vi.unstubAllGlobals(); window.location.hash = ""; });

const explicit = { ...findingConfirmed, id: "fnd_err", run_id: erroredRun.id, kind: "explicit_error", title: "Run errored at Intake", status: "hypothesized", verification_level: "V1" };
const routes = () => ({
  "GET /findings/summary": () => ({ confirmed: 1, hypothesized: 1 }),
  [`GET /findings/${findingConfirmed.id}`]: () => findingConfirmed,
  "GET /findings": () => [findingConfirmed, explicit],
  [`GET /runs/${silentRun.id}/graph`]: () => silentGraph,
  [`GET /runs/${silentRun.id}`]: () => silentRun,
  "GET /runs": () => [silentRun, cleanRun, cancelledRun, erroredRun],
});
const tile = (name: string) => within(screen.getByText(name).closest(".stat") as HTMLElement);

describe("command center telemetry", () => {
  it("counts executions, silent failures, verified findings and pending reviews from what the API returned", async () => {
    mockApi(routes());
    render(<Home />);
    expect(await tile("Executions").findByText("4")).toBeInTheDocument();
    expect(tile("Executions").getByText("3 completed")).toBeInTheDocument();
    expect(tile("Executions").getByText("1 errored")).toBeInTheDocument();
    // a silent failure is a run that completed and still failed an outcome check: only the stale-price run
    expect(tile("Silent failures").getByText("1")).toBeInTheDocument();
    expect(tile("Silent failures").getByText("of 3 completed")).toBeInTheDocument();
    expect(tile("Verified (V2+)").getByText("of 2 findings")).toBeInTheDocument();
    const funnel = within(tile("Verified (V2+)").getByRole("list", { name: "Findings by stage reached" }));
    expect(funnel.getAllByRole("listitem").map((li) => li.textContent)).toEqual(["Detected2", "Traced2", "Verified1", "Reviewed0"]);
    expect(tile("Awaiting review").getByText("1")).toBeInTheDocument();
  });

  it("shows n/a, not zero, for numbers whose request failed", async () => {
    mockApi({ ...routes(), "GET /findings/summary": () => new Response("{}", { status: 500 }) });
    render(<Home />);
    await tile("Executions").findByText("4");
    await waitFor(() => expect(tile("Verified (V2+)").getByText("n/a")).toBeInTheDocument());
    expect(tile("Awaiting review").getByText("n/a")).toBeInTheDocument();
  });
});

describe("command center workbench", () => {
  it("previews the first finding with its confirmed origin and the verdict counts of the stored experiment", async () => {
    mockApi(routes());
    render(<Home />);
    const inspector = within(await screen.findByRole("complementary", { name: "Trace inspector" }));
    expect(await inspector.findByText("Origin confirmed")).toBeInTheDocument();
    expect(inspector.getByText("Order Lookup", { selector: "strong" })).toBeInTheDocument();
    expect(inspector.getByText("5/5 fix · 0/2 control · 57% to 100%")).toBeInTheDocument();
    expect(await inspector.findByRole("group", { name: /^Causal map\./ })).toBeInTheDocument();
    expect(inspector.getByRole("link", { name: "Open investigation" })).toHaveAttribute("href", `#/findings/${findingConfirmed.id}`);
  });

  it("lists runs with their condition and mode, filters them on the server, and inspects one by keyboard", async () => {
    const calls = mockApi(routes());
    const user = userEvent.setup();
    render(<Home />);
    await user.click(await screen.findByRole("tab", { name: /Runs/ }));
    const panel = within(screen.getByRole("tabpanel", { name: /Runs/ }));
    expect(panel.getAllByRole("row")).toHaveLength(5); // header + four runs
    expect(panel.getAllByText("Injected fault: stale price").length).toBeGreaterThan(0);
    expect(panel.getAllByText("Clean run").length).toBeGreaterThan(0);

    await user.selectOptions(panel.getByLabelText("Condition"), "none");
    await user.selectOptions(panel.getByLabelText("Run status"), "completed");
    await user.type(panel.getByLabelText("Search runs"), "W1023987");
    await user.click(panel.getByRole("button", { name: "Search runs now" }));
    await waitFor(() => {
      const last = [...calls].reverse().find((c) => c.url.startsWith("/api/runs?"))!;
      const p = new URL(last.url, "http://x").searchParams;
      expect([p.get("fault"), p.get("status"), p.get("q")]).toEqual(["none", "completed", "W1023987"]);
    });

    const inspect = panel.getByRole("button", { name: `Inspect run ${silentRun.task_input.order_id} ${silentRun.id}` });
    inspect.focus();
    await user.keyboard("{Enter}");
    const inspector = within(screen.getByRole("complementary", { name: "Trace inspector" }));
    expect(await inspector.findByText(/your refund of \$662\.00/)).toBeInTheDocument();
    expect(inspector.getByText("4 passed")).toBeInTheDocument();
    expect(inspector.getByText("3 failed")).toBeInTheDocument();
    expect(inspector.getByText("CHK-OUT-1")).toBeInTheDocument();
    expect(inspector.getByRole("link", { name: "Open trace" })).toHaveAttribute("href", `#/runs/${silentRun.id}`);
  });

  it("explains an empty inspector instead of showing a blank panel", async () => {
    mockApi({ "GET /runs": () => [], "GET /findings": () => [] });
    render(<Home />);
    expect(await screen.findByText("Select a run or a finding to see its pipeline, checks and verdict here.")).toBeInTheDocument();
  });
});
