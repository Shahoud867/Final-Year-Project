import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { RunDetail } from "../src/pages/RunDetail";
import { cancelledRun, cleanRun, erroredRun, findingConfirmed, findingTraced, silentGraph, silentRun } from "./fixtures";
import { mockApi } from "./helpers";
import type { RunDetail as Run } from "../src/types";

afterEach(() => { vi.unstubAllGlobals(); window.location.hash = ""; });

const serve = (run: Run, finding: unknown = findingConfirmed) => mockApi({
  [`GET /runs/${run.id}/graph`]: () => silentGraph,
  [`GET /runs/${run.id}`]: () => run,
  "GET /findings/": () => finding,
});

describe("pipeline trace of a silent failure", () => {
  it("sets what monitoring sees beside what the checks see, with the run's own values", async () => {
    serve(silentRun);
    render(<RunDetail id={silentRun.id} />);
    expect(await screen.findByText("Silent failure")).toBeInTheDocument();
    expect(screen.getByText("Run status: completed")).toBeInTheDocument();
    expect(screen.getByText("Error raised: none")).toBeInTheDocument();
    expect(screen.getByText("Outcome checks: 1 passed, 1 failed")).toBeInTheDocument();
    expect(screen.getByText(/your refund of \$662\.00/, { selector: "p" })).toBeInTheDocument();
    expect(screen.getByText("Injected fault: stale price")).toBeInTheDocument();
    expect(screen.getAllByText("Recorded cassette").length).toBeGreaterThan(0);
    expect(screen.getByRole("link", { name: "Investigate" })).toHaveAttribute("href", `#/findings/${silentRun.findings[0]!.id}`);
  });

  it("lists the checks once, grouped by scope with failures first, each against what it was compared with", async () => {
    serve(silentRun);
    const user = userEvent.setup();
    render(<RunDetail id={silentRun.id} />);
    await user.click(await screen.findByRole("tab", { name: /Checks/ }));
    const ids = (name: string) => within(screen.getByRole("region", { name })).getAllByText(/^(CT|CHK)-/).map((e) => e.textContent);
    expect(ids("Outcome checks")).toEqual(["CHK-OUT-1", "CHK-OUT-2"]);
    expect(ids("Step checks").slice(0, 2)).toEqual(["CT-LOOKUP", "CT-CALC"]);
    const lookup = screen.getByText("CT-LOOKUP").closest("tr") as HTMLElement;
    expect(within(lookup).getByText("source of truth (catalog_total)")).toBeInTheDocument();
    const compare = within(lookup.querySelector(".compare") as HTMLElement);
    expect(compare.getByText("661.98")).toBeInTheDocument();
    expect(compare.getByText("662.23")).toBeInTheDocument();
    const calc = screen.getByText("CT-CALC").closest("tr") as HTMLElement;
    expect(within(calc).getByText("the step's own contract over its inputs")).toBeInTheDocument();
  });

  it("shows each step's checks under its name in the trace, and the raw trace on the Data tab", async () => {
    serve(silentRun);
    const user = userEvent.setup();
    render(<RunDetail id={silentRun.id} />);
    const row = (await screen.findByRole("button", { name: "Inspect Order Lookup" })).closest("tr") as HTMLElement;
    expect(within(row).getByText("CT-LOOKUP fail")).toBeInTheDocument();
    expect(screen.queryByRole("heading", { name: "Observed vs source of truth" })).not.toBeInTheDocument();
    await user.click(screen.getByRole("tab", { name: /Data/ }));
    expect(screen.getByRole("group", { name: "Trace (Granite Trace v1)" })).toHaveTextContent('"step_id": "s2"');
    expect(screen.getByRole("link", { name: `Open case ${silentRun.findings[0]!.id}` })).toHaveAttribute("href", `#/findings/${silentRun.findings[0]!.id}`);
  });

  it("marks the origin a replay confirmed, and reveals the injected fault only on request", async () => {
    serve(silentRun);
    const user = userEvent.setup();
    render(<RunDetail id={silentRun.id} />);
    // the mark arrives with the finding, which is loaded after the run
    expect(await screen.findByRole("button", { name: /Order Lookup: Tool step, check failed, origin confirmed/ }, { timeout: 5000 })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /fault injected/ })).not.toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Reveal injected fault" }));
    expect(screen.getByRole("button", { name: /Order Lookup.*fault injected/ })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Hide injected fault" })).toHaveAttribute("aria-pressed", "true");
  });

  it("marks only a suspect while nothing has been verified", async () => {
    serve(silentRun, findingTraced);
    render(<RunDetail id={silentRun.id} />);
    expect(await screen.findByRole("button", { name: /Order Lookup: Tool step, check failed, suspect/ }, { timeout: 5000 })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /origin confirmed/ })).not.toBeInTheDocument();
  });

  it("opens a step from the keyboard and shows exactly what it received, produced and how its check was computed", async () => {
    serve(silentRun);
    const user = userEvent.setup();
    render(<RunDetail id={silentRun.id} />);
    const node = await screen.findByRole("button", { name: /^Order Lookup: Tool step/ });
    node.focus();
    await user.keyboard("{Enter}");
    const panel = within(screen.getByRole("dialog", { name: "Order Lookup" }));
    expect(panel.getByText("s1.order_id")).toBeInTheDocument();
    expect(panel.getByRole("group", { name: "Order Lookup received" })).toHaveTextContent('"s1.order_id": "#W1023987"');
    expect(panel.getByRole("group", { name: "Order Lookup produced" })).toHaveTextContent('"price": 452.03');
    expect(panel.getByText("Lookup prices match the catalogue: observed 661.98, expected 662.23")).toBeInTheDocument();
    expect(panel.getByText(/truth\.catalog_total\(/, { selector: "span" })).toHaveTextContent("returned 662.23");
    expect(panel.getByText("deterministic")).toBeInTheDocument();
    await user.click(panel.getByRole("button", { name: /Policy/ }));
    expect(screen.getByRole("dialog", { name: "Policy" })).toBeInTheDocument();
    await user.keyboard("{Escape}");
    await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
  });

  it("lists every step with how its answer was produced", async () => {
    serve(silentRun);
    render(<RunDetail id={silentRun.id} />);
    await screen.findByRole("button", { name: "Inspect Intake" });
    expect(screen.getAllByText("recorded answer")).toHaveLength(3); // the three language-model steps replayed saved answers
    expect(screen.getAllByText("deterministic")).toHaveLength(2); // the tool and the code step
  });
});

describe("pipeline trace of the other scenarios", () => {
  it("reports a clean run as clean", async () => {
    serve(cleanRun, null);
    render(<RunDetail id={cleanRun.id} />);
    expect(await screen.findByText("Every check that could be evaluated passed.")).toBeInTheDocument();
    expect(screen.getByText("No finding: no outcome check failed.")).toBeInTheDocument();
    expect(screen.getByText("Clean run")).toBeInTheDocument();
    expect(screen.queryByText("Silent failure")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Reveal injected fault" })).not.toBeInTheDocument();
  });

  it("explains a failed step check that did not change the outcome", async () => {
    serve(cancelledRun, null);
    render(<RunDetail id={cancelledRun.id} />);
    expect(await screen.findByText("1 step check failed, but the outcome is correct, so no finding was opened.")).toBeInTheDocument();
    expect(screen.getByText("No finding: no outcome check failed.")).toBeInTheDocument();
  });

  it("gives the reason once when a run stopped early", async () => {
    serve(erroredRun, findingTraced);
    render(<RunDetail id={erroredRun.id} />);
    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent("this exact request was never recorded");
    expect(screen.getAllByRole("alert")).toHaveLength(1);
    expect(screen.getByText("Run status: errored")).toBeInTheDocument();
    expect(screen.getByText("Outcome checks could not be evaluated.")).toBeInTheDocument();
  });
});
