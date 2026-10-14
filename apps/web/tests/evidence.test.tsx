import { render, screen, within } from "@testing-library/react";
import { Evidence } from "../src/pages/Evidence";
import { cleanRun, health, silentRun } from "./fixtures";
import { mockApi } from "./helpers";

afterEach(() => { vi.unstubAllGlobals(); sessionStorage.clear(); });

const ghRun = (over: object) => ({
  id: 1, name: "CI", run_number: 16, status: "completed", conclusion: "success", head_branch: "main", head_sha: "ee4b2270000000",
  event: "push", created_at: "2026-10-13T21:25:00Z", html_url: "https://github.com/x/y/actions/runs/1", ...over,
});
const github = { "GET https://api.github.com": () => ({ workflow_runs: [
  ghRun({}), ghRun({ id: 2, name: "CD", run_number: 7, event: "workflow_run" }),
  ghRun({ id: 3, name: "CD", run_number: 6, event: "push", head_branch: "v0.1.0-mid1", head_sha: "336ca550000000" }),
] }) };
const server = { "GET /health": () => health, [`GET /runs/${silentRun.id}`]: () => silentRun, "GET /runs": () => [cleanRun, silentRun] };
const card = (title: string) => within(screen.getByRole("heading", { name: title }).closest("section") as HTMLElement);

describe("Evidence: why a silent failure is missed", () => {
  it("uses a real silent-failure run of this server, with its own observed and expected values", async () => {
    mockApi({ ...server, ...github });
    render(<Evidence />);
    const lanes = card("Why output monitoring misses a silent failure");
    expect(await lanes.findByText("Looks healthy")).toBeInTheDocument();
    expect(lanes.getByText(/your refund of \$662\.00/)).toBeInTheDocument();
    expect(lanes.getByText("Told to the customer").parentElement).toHaveTextContent("662");
    expect(lanes.getByText("Source of truth").parentElement).toHaveTextContent("662.23");
    expect(lanes.getByText("Silent failure found")).toBeInTheDocument();
    expect(lanes.getByRole("link", { name: "Open the finding" })).toHaveAttribute("href", `#/findings/${silentRun.findings[0]!.id}`);
    expect(lanes.getByRole("link", { name: silentRun.id })).toHaveAttribute("href", `#/runs/${silentRun.id}`);
  });

  it("falls back to a schematic without numbers when no such run exists", async () => {
    mockApi({ "GET /health": () => health, "GET /runs": () => [cleanRun], ...github });
    render(<Evidence />);
    const lanes = card("Why output monitoring misses a silent failure");
    expect(await lanes.findByRole("link", { name: "Run the silent price discrepancy scenario" })).toHaveAttribute("href", "#/new");
    expect(lanes.getByText("schematic: no such run on this server yet")).toBeInTheDocument();
    expect(lanes.queryByText(/\d{3}\.\d{2}/)).not.toBeInTheDocument();
  });
});

describe("Evidence: delivery pipeline", () => {
  it("shows the latest CI and CD runs and the release tag exactly as GitHub reports them", async () => {
    mockApi({ ...server, ...github });
    render(<Evidence />);
    const delivery = card("Delivery pipeline (CI/CD)");
    expect(await delivery.findByRole("link", { name: /CI #16/ })).toHaveAttribute("href", "https://github.com/x/y/actions/runs/1");
    expect(delivery.getByRole("link", { name: /CD #7/ })).toBeInTheDocument();
    expect(delivery.getByRole("link", { name: /CD #6/ })).toBeInTheDocument();
    expect(delivery.getAllByText("success")).toHaveLength(3);
    expect(delivery.getByText("v0.1.0-mid1")).toBeInTheDocument();
    expect(delivery.getByText("v0.1.0, recorded cassette")).toBeInTheDocument();
    // the test build has no stamp, so the page must not claim that its commit passed CI
    expect(delivery.getByText("no build stamp")).toBeInTheDocument();
    expect(delivery.getByText("No successful CI run for this build's commit among the latest runs")).toBeInTheDocument();
    expect(delivery.queryByText(/This build's commit passed CI/)).not.toBeInTheDocument();
  });

  it("reports a failed pipeline as failed", async () => {
    mockApi({ ...server, "GET https://api.github.com": () => ({ workflow_runs: [ghRun({ conclusion: "failure" })] }) });
    render(<Evidence />);
    const delivery = card("Delivery pipeline (CI/CD)");
    expect(await delivery.findByText("failure")).toBeInTheDocument();
    expect(delivery.queryByText("success")).not.toBeInTheDocument();
    expect(delivery.getAllByText("no completed run among the latest listed")).toHaveLength(2); // CD and the release tag
  });

  it("says the status is unknown when GitHub cannot be reached, and shows no success of any kind", async () => {
    mockApi({ ...server, "GET https://api.github.com": () => new Response("{}", { status: 403 }) });
    render(<Evidence />);
    const delivery = card("Delivery pipeline (CI/CD)");
    expect(await delivery.findByText("Pipeline status unknown")).toBeInTheDocument();
    expect(delivery.getByText(/request limit/)).toBeInTheDocument();
    expect(delivery.getByRole("link", { name: "Open the Actions page" })).toBeInTheDocument();
    expect(delivery.queryByText("success")).not.toBeInTheDocument();
    expect(delivery.queryByText(/passed CI/)).not.toBeInTheDocument();
  });
});
