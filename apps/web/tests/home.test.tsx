import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Home } from "../src/pages/Home";
import { Runs } from "../src/pages/Runs";
import type { FindingSummary } from "../src/types";
import { cancelledRun, cleanRun, erroredRun, findingConfirmed, silentGraph, silentRun } from "./fixtures";
import { mockApi } from "./helpers";

afterEach(() => { vi.unstubAllGlobals(); window.location.hash = ""; });

const lead = { step_id: "s2", agent: "Order Lookup", status: "confirmed", fix_pass: 5, fix_n: 5, control_pass: 0, control_n: 2 };
const confirmed: FindingSummary = { ...findingConfirmed, lead };
const traced: FindingSummary = {
  ...findingConfirmed, id: "fnd_traced", title: "Run errored at Intake", kind: "explicit_error", status: "hypothesized",
  verification_level: "V1", created_at: "2026-10-07T09:00:00Z",
  lead: { ...lead, step_id: "s1", agent: "Intake", status: "open", fix_pass: null, fix_n: null, control_pass: null, control_n: null },
};
const byStatus: Record<string, FindingSummary[]> = { confirmed: [confirmed], hypothesized: [traced] };

const routes = (counts: Record<string, number> = { confirmed: 1, hypothesized: 1 }) => ({
  "GET /findings/summary": () => counts,
  [`GET /findings/${findingConfirmed.id}`]: () => findingConfirmed,
  "GET /findings/fnd_traced": () => ({ ...findingConfirmed, ...traced, experiments: [], hypotheses: findingConfirmed.hypotheses.map((h) => ({ ...h, status: "open" })) }),
  "GET /findings": (url: string) => {
    const status = new URL(url, "http://x").searchParams.get("status");
    return status ? byStatus[status] ?? [] : [confirmed, traced];
  },
  [`GET /runs/${silentRun.id}/graph`]: () => silentGraph,
  [`GET /runs/${silentRun.id}`]: () => silentRun,
  "GET /runs": () => [silentRun, cleanRun, cancelledRun, erroredRun],
});
const list = () => within(screen.getByRole("tabpanel"));

describe("inbox", () => {
  it("opens on the findings that need a decision and counts each group from the server's summary", async () => {
    mockApi(routes());
    render(<Home />);
    const needs = await screen.findByRole("tab", { name: /Needs you/ });
    await waitFor(() => expect(needs).toHaveAttribute("aria-selected", "true"));
    expect(needs).toHaveTextContent("1");
    expect(screen.getByRole("tab", { name: /Verifying/ })).toHaveTextContent("1");
    expect(screen.getByRole("tab", { name: /Decided/ })).toHaveTextContent("0");
    expect(screen.getByRole("tab", { name: /All/ })).toHaveTextContent("2");
    expect(await list().findByText(confirmed.title)).toBeInTheDocument();
    expect(list().queryByText(traced.title)).not.toBeInTheDocument();
  });

  it("states the lead suspect and its verdict in words, with the replays behind it", async () => {
    mockApi(routes());
    render(<Home />);
    const row = (await list().findByText(confirmed.title)).closest("tr") as HTMLElement;
    expect(within(row).getByText("Order Lookup")).toBeInTheDocument();
    expect(within(row).getByText("5/5 with fix, 0/2 without")).toBeInTheDocument();
    expect(row.querySelector(".inbox-verdict")).toHaveTextContent(/^Confirmed5\/5 with fix/);
    expect(within(row).getByRole("img", { name: "Evidence level V2 of V3: replay-verified" })).toBeInTheDocument();
  });

  it("asks the server for each status of a group and says when a suspect has not been verified", async () => {
    const calls = mockApi(routes());
    const user = userEvent.setup();
    render(<Home />);
    await user.click(await screen.findByRole("tab", { name: /Verifying/ }));
    expect(await list().findByText(traced.title)).toBeInTheDocument();
    expect(list().getByText("Suspect, not verified yet")).toBeInTheDocument();
    const asked = calls.map((c) => new URL(c.url, "http://x").searchParams.get("status")).filter(Boolean);
    expect(asked).toEqual(expect.arrayContaining(["open", "hypothesized", "verifying", "refuted"]));
  });

  it("previews the selected finding with its confirmed origin and the verdict counts of the stored experiment", async () => {
    mockApi(routes());
    render(<Home />);
    const look = within(await screen.findByRole("complementary", { name: "Quick look" }));
    expect(await look.findByText("Origin confirmed")).toBeInTheDocument();
    expect(look.getByText("Order Lookup", { selector: "strong" })).toBeInTheDocument();
    expect(look.getByText("5/5 fix · 0/2 control · 57% to 100%")).toBeInTheDocument();
    expect(look.getByRole("link", { name: "Open case" })).toHaveAttribute("href", `#/findings/${findingConfirmed.id}`);
  });

  it("totals runs and findings in one line, and shows n/a, not zero, when a request failed", async () => {
    mockApi({ ...routes(), "GET /findings/summary": () => new Response("{}", { status: 500 }) });
    render(<Home />);
    const totals = await screen.findByText(/silent failures of/);
    await waitFor(() => expect(totals.closest("p")).toHaveTextContent("4 runs1 silent failures of 3 completed"));
    await waitFor(() => expect(totals.closest("p")).toHaveTextContent("n/a of n/a findings verified"));
  });

  it("lists the five newest runs below, with a way to all of them", async () => {
    mockApi(routes());
    render(<Home />);
    const recent = within((await screen.findByRole("heading", { name: "Recent runs" })).closest("section") as HTMLElement);
    expect(await recent.findAllByRole("row")).toHaveLength(5); // header + four runs
    expect(recent.getByRole("link", { name: /All runs/ })).toHaveAttribute("href", "#/runs");
  });

  it("explains an empty inbox and offers the one action that fills it", async () => {
    mockApi({ "GET /findings/summary": () => ({}), "GET /runs": () => [], "GET /findings": () => [] });
    render(<Home />);
    expect(await screen.findByText("No findings yet. Run a task with a fault.")).toBeInTheDocument();
    expect(screen.getAllByRole("link", { name: "New run" })[0]).toHaveAttribute("href", "#/new");
    expect(screen.getByText("Select a row to see its pipeline, checks and verdict here.")).toBeInTheDocument();
  });
});

describe("runs", () => {
  it("lists runs with their condition and mode, filters them on the server, and previews one by keyboard", async () => {
    const calls = mockApi(routes());
    const user = userEvent.setup();
    render(<Runs />);
    const table = within((await screen.findAllByRole("table"))[0]!);
    expect(await table.findAllByRole("row")).toHaveLength(5);
    expect(table.getAllByText("Injected fault: stale price").length).toBeGreaterThan(0);
    expect(table.getAllByText("Clean run").length).toBeGreaterThan(0);

    await user.selectOptions(screen.getByLabelText("Condition"), "none");
    await user.selectOptions(screen.getByLabelText("Run status"), "completed");
    await user.type(screen.getByLabelText("Search runs"), "W1023987");
    await user.click(screen.getByRole("button", { name: "Search runs now" }));
    await waitFor(() => {
      const last = [...calls].reverse().find((c) => c.url.startsWith("/api/runs?") && !c.url.includes("limit=100"))!;
      const p = new URL(last.url, "http://x").searchParams;
      expect([p.get("fault"), p.get("status"), p.get("q")]).toEqual(["none", "completed", "W1023987"]);
    });

    const look = screen.getByRole("button", { name: `Quick look at run ${silentRun.task_input.order_id} ${silentRun.id}` });
    look.focus();
    await user.keyboard("{Enter}");
    const panel = within(screen.getByRole("complementary", { name: "Quick look" }));
    expect(await panel.findByText(/your refund of \$662\.00/)).toBeInTheDocument();
    expect(panel.getByText("4 passed")).toBeInTheDocument();
    expect(panel.getByText("3 failed")).toBeInTheDocument();
    expect(panel.getByRole("link", { name: "Open trace" })).toHaveAttribute("href", `#/runs/${silentRun.id}`);
  });

  it("says so when nothing has run", async () => {
    mockApi({ "GET /runs": () => [] });
    render(<Runs />);
    expect(await screen.findByText("Nothing has run yet.")).toBeInTheDocument();
  });
});
