import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { pct } from "../src/format";
import { FindingDetail } from "../src/pages/FindingDetail";
import type { FindingDetail as Finding } from "../src/types";
import { findingConfirmed, findingTraced, silentGraph } from "./fixtures";
import { mockApi, problem } from "./helpers";

afterEach(() => { vi.unstubAllGlobals(); window.location.hash = ""; });

const serve = (f: Finding, over: Record<string, () => unknown> = {}) => mockApi({
  [`GET /findings/${f.id}/report`]: () => problem(500, { title: "Internal error", detail: "The report could not be built." }),
  [`GET /findings/${f.id}`]: () => f,
  [`GET /runs/${f.run_id}/graph`]: () => silentGraph,
  ...over,
});
const experiment = (name: RegExp) => within(screen.getByRole("article", { name }));

describe("verification results", () => {
  it("draws each experiment from the server's own replays, counts, interval and verdict", async () => {
    serve(findingConfirmed);
    render(<FindingDetail id={findingConfirmed.id} />);
    await screen.findByRole("heading", { name: "Verification results" });
    const confirmed = findingConfirmed.experiments.find((e) => e.verdict === "confirmed")!.summary!;
    const lookup = experiment(/Experiment on Order Lookup: Confirmed/);
    expect(lookup.getAllByRole("img", { name: /^fix \d: correct, seed \d+$/ })).toHaveLength(5);
    expect(lookup.getAllByRole("img", { name: /^control \d: still wrong, seed \d+$/ })).toHaveLength(2);
    expect(lookup.getByText(`95% interval ${pct(confirmed.ci_low)} to ${pct(confirmed.ci_high)}`)).toBeInTheDocument();
    expect(lookup.getByText(/Server verdict:/)).toHaveTextContent(`Server verdict: Confirmed. ${confirmed.explanation}`);
    expect(lookup.getAllByText("Recorded cassette").length).toBe(1);

    const calc = experiment(/Experiment on Refund Calculator: Refuted/);
    expect(calc.getAllByRole("img", { name: /^fix \d: still wrong/ })).toHaveLength(5);
    expect(calc.getByText("95% interval 0% to 43%")).toBeInTheDocument();
    // newest first: Order Lookup was verified after the Refund Calculator
    expect(screen.getAllByRole("article").map((a) => a.getAttribute("aria-label"))).toEqual([
      "Experiment on Order Lookup: Confirmed", "Experiment on Refund Calculator: Refuted",
    ]);
  });

  it("explains the verdict with the rule evaluated on the real rates", async () => {
    serve(findingConfirmed);
    render(<FindingDetail id={findingConfirmed.id} />);
    await screen.findByRole("heading", { name: "Verification results" });
    const lines = (name: RegExp) => experiment(name).getAllByRole("listitem").filter((li) => /≥|≤/.test(li.textContent ?? "")).map((li) => li.textContent);
    expect(lines(/Order Lookup/)).toEqual([
      "Fix replays correct ≥ 80% : 100% (holds)", "Control replays correct ≤ 20% : 0% (holds)", "Refuted when fix replays correct ≤ 20% : 100% (does not hold)",
    ]);
    expect(lines(/Refund Calculator/)).toEqual([
      "Fix replays correct ≥ 80% : 0% (does not hold)", "Control replays correct ≤ 20% : 0% (holds)", "Refuted when fix replays correct ≤ 20% : 0% (holds)",
    ]);
  });

  it("lists every replay with its seed, the checks it fixed and its final output", async () => {
    serve(findingConfirmed);
    const user = userEvent.setup();
    render(<FindingDetail id={findingConfirmed.id} />);
    await screen.findByRole("heading", { name: "Verification results" });
    const lookup = experiment(/Order Lookup/);
    await user.click(lookup.getByText("Replay-level results (7)"));
    const rows = lookup.getAllByRole("row").slice(1);
    expect(rows).toHaveLength(7);
    expect(within(rows[0]!).getByText("1000")).toBeInTheDocument();
    expect(within(rows[0]!).getAllByText("CHK-OUT-1").length).toBe(1);
    expect(within(rows[0]!).getByText(/refund of \$662\.23/)).toBeInTheDocument();
    expect(within(rows[6]!).getByText("still wrong")).toBeInTheDocument();
  });

  it("never shows a verdict the server did not return", async () => {
    const errored: Finding = { ...findingConfirmed, experiments: [{ ...findingConfirmed.experiments[0]!, verdict: null, status: "error", summary: null,
      error: "2 replay(s) needed model answers that are not in the recording.", replays: [] }] };
    serve(errored);
    render(<FindingDetail id={errored.id} />);
    const block = within(await screen.findByRole("article"));
    expect(block.getByText("No verdict")).toBeInTheDocument();
    expect(block.getByText("2 replay(s) needed model answers that are not in the recording.")).toBeInTheDocument();
    expect(block.queryByText(/Server verdict:/)).not.toBeInTheDocument();
    expect(block.queryByText(/95% interval/)).not.toBeInTheDocument();
  });
});

describe("root-cause hypotheses", () => {
  it("highlights the recorded path of the hypothesis the analyst selects", async () => {
    serve(findingConfirmed);
    const user = userEvent.setup();
    render(<FindingDetail id={findingConfirmed.id} />);
    const map = within(await screen.findByRole("group", { name: /^Causal map\./ }));
    expect(map.getByText("origin confirmed")).toBeInTheDocument(); // the confirmed hypothesis leads
    await user.click(screen.getByRole("button", { name: "Show path from Refund Calculator" }));
    expect(map.getByText("refuted")).toBeInTheDocument();
    expect(map.queryByText("origin confirmed")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Show path from Refund Calculator" })).toHaveAttribute("aria-pressed", "true");
    const plan = within(screen.getByRole("group", { name: "Replay plan for Refund Calculator" }));
    expect(plan.getByText("Refund Calculator").parentElement).toHaveTextContent("Refund Calculatorpatched");
    expect(plan.getByText("Policy").parentElement).toHaveTextContent("Policyreused");
    expect(plan.getByText("Writer").parentElement).toHaveTextContent("Writerre-run");
  });

  it("refuses replay counts outside the server's range before any request", async () => {
    const calls = serve(findingTraced);
    const user = userEvent.setup();
    render(<FindingDetail id={findingTraced.id} />);
    const n = await screen.findByLabelText("Replays with fix");
    expect(screen.getAllByRole("button", { name: "Verify" })[0]).toBeEnabled();
    await user.clear(n);
    await user.type(n, "11");
    expect(screen.getByText("Use 1 to 10")).toBeInTheDocument();
    expect(n).toHaveAttribute("aria-invalid", "true");
    for (const b of screen.getAllByRole("button", { name: "Verify" })) expect(b).toBeDisabled();
    await user.clear(screen.getByLabelText("Controls"));
    await user.type(screen.getByLabelText("Controls"), "6");
    expect(screen.getByText("Use 0 to 5")).toBeInTheDocument();
    expect(calls.some((c) => c.init?.method === "POST")).toBe(false);
  });

  it("locks the human decision until a verdict exists, as the lifecycle requires", async () => {
    serve(findingTraced);
    render(<FindingDetail id={findingTraced.id} />);
    expect(await screen.findByRole("heading", { name: "Human review" })).toBeInTheDocument();
    expect(screen.getByText("Available after a verification verdict. The server refuses a decision before that.")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Accept" })).not.toBeInTheDocument();
    const rail = within(screen.getByRole("list", { name: "Investigation progress" }));
    expect(rail.getByText("Traced").closest("li")).toHaveAttribute("aria-current", "step");
    expect(screen.getByText("Verify a hypothesis")).toBeInTheDocument();
  });

  it("offers exactly the decisions the server allows", async () => {
    serve(findingConfirmed);
    render(<FindingDetail id={findingConfirmed.id} />);
    const decision = within((await screen.findByRole("heading", { name: "Your decision" })).closest("section") as HTMLElement);
    expect(decision.getAllByRole("button").map((b) => b.textContent)).toEqual(["Accept", "Reject", "Ask for more information"]);
  });
});

describe("evidence ledger", () => {
  it("counts verified hashes and opens a record with its full hash and how to reproduce it", async () => {
    serve(findingConfirmed);
    const user = userEvent.setup();
    render(<FindingDetail id={findingConfirmed.id} />);
    const total = findingConfirmed.evidence.length;
    expect(await screen.findByText(`${total} records, ${total} hashes verified`)).toBeInTheDocument();
    const record = findingConfirmed.evidence[0]!;
    await user.click(screen.getByRole("button", { name: `View ${record.title}` }));
    const panel = within(screen.getByRole("dialog", { name: record.title }));
    expect(panel.getByText(record.sha256)).toBeInTheDocument();
    expect(panel.getByText(record.reproduce!)).toBeInTheDocument();
    expect(panel.getByText("hash matches the content")).toBeInTheDocument();
    await user.keyboard("{Escape}");
    await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument());
    expect(screen.getByRole("button", { name: `View ${record.title}` })).toHaveFocus();
  });

  it("raises an alert when a record no longer matches its hash", async () => {
    const tampered: Finding = { ...findingConfirmed, evidence: findingConfirmed.evidence.map((e, i) => (i === 2 ? { ...e, hash_valid: false } : e)) };
    serve(tampered);
    render(<FindingDetail id={tampered.id} />);
    expect(await screen.findByRole("alert")).toHaveTextContent("Integrity check failed");
    expect(screen.getByText(`${tampered.evidence.length} records, ${tampered.evidence.length - 1} hashes verified`)).toBeInTheDocument();
    expect(screen.getAllByText("TAMPERED")).toHaveLength(1);
  });

  it("says so when the report cannot be created", async () => {
    serve(findingConfirmed);
    const user = userEvent.setup();
    render(<FindingDetail id={findingConfirmed.id} />);
    await user.click(await screen.findByRole("button", { name: "Download report (.md)" }));
    expect(await screen.findByText("The report could not be built.")).toBeInTheDocument();
  });
});
