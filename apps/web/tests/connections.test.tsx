import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import axe from "axe-core";
import { RunPlatforms, SendVerdict } from "../src/components/Platforms";
import { Connections } from "../src/pages/Connections";
import type { Connection, ImportResult, TraceLink } from "../src/types";
import { mockApi, problem } from "./helpers";

const phoenix: Connection = {
  id: "con_1", kind: "phoenix", name: "Local Phoenix", base_url: "http://localhost:6006", project: "granite-demo",
  workflow_key: "refund_desk", profile: { steps: {} }, created_at: "2026-11-15T10:00:00Z", last_sync_at: null,
  last_error: "", keys_configured: true, imported_runs: 0, exported_runs: 1,
};
const langfuse: Connection = { ...phoenix, id: "con_2", kind: "langfuse", name: "Langfuse Cloud", base_url: "https://cloud.langfuse.com",
  project: "", keys_configured: false };
const imported: ImportResult = {
  connection_id: "con_1", fetched: 2,
  imported: [{ trace_id: "a".repeat(32), run_id: "run_9", findings: 1, lineage: ["declared"], status: "completed" }],
  skipped: [{ trace_id: "b".repeat(32), reason: "steps s1, s2 of refund_desk are missing (found chat)" }],
};
const link: TraceLink = {
  connection_id: "con_1", run_id: "run_1", direction: "imported", external_trace_id: "c".repeat(32), root_span_id: "r",
  span_ids: { s2: "d".repeat(16) }, lineage: [{ read: "s1.order_id", step_id: "s2", tier: "value" }], created_at: "2026-11-15T10:00:00Z",
};

async function violations(container: HTMLElement) {
  const res = await axe.run(container, { rules: { "color-contrast": { enabled: false }, region: { enabled: false } } });
  return res.violations.map((v) => v.id);
}

describe("Connections page", () => {
  it("imports traces and explains every skip", async () => {
    const calls = mockApi({ "GET /connections": () => [phoenix], "POST /connections/con_1/import": () => imported });
    const { container } = render(<Connections />);
    await userEvent.click(await screen.findByRole("button", { name: "Import traces" }));
    expect(await screen.findByRole("link", { name: "run_9" })).toHaveAttribute("href", "#/runs/run_9");
    expect(screen.getByText(/steps s1, s2 of refund_desk are missing/)).toBeInTheDocument();
    expect(screen.getByText("declared")).toHaveAttribute("title", "reads declared by the application");
    expect(calls.some((c) => c.url === "/api/connections/con_1/import" && c.init?.body === JSON.stringify({ limit: 20 }))).toBe(true);
    expect(await violations(container)).toEqual([]);
  });

  it("blocks Langfuse imports until keys are configured and reports a failed test", async () => {
    mockApi({ "GET /connections": () => [langfuse],
      "POST /connections/con_2/test": () => ({ ok: false, detail: { error: "HTTP 401: Invalid keys" } }) });
    render(<Connections />);
    expect(await screen.findByRole("button", { name: "Import traces" })).toBeDisabled();
    expect(screen.getByText("keys missing")).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: "Test" }));
    expect(await screen.findByText("HTTP 401: Invalid keys")).toBeInTheDocument();
  });

  it("adds a connection with only the URL and names, switching defaults per platform", async () => {
    const calls = mockApi({ "GET /connections": () => [], "POST /connections": () => phoenix });
    render(<Connections />);
    expect(await screen.findByText("No connections yet")).toBeInTheDocument();
    await userEvent.click(screen.getByRole("radio", { name: "Langfuse" }));
    expect(screen.getByLabelText("Server URL")).toHaveValue("https://cloud.langfuse.com");
    await userEvent.click(screen.getByRole("radio", { name: "Arize Phoenix" }));
    await userEvent.click(screen.getByRole("button", { name: "Add connection" }));
    const sent = calls.find((c) => c.init?.method === "POST");
    expect(JSON.parse(String(sent?.init?.body))).toEqual({
      workflow: "refund_desk", kind: "phoenix", name: "Local Phoenix", base_url: "http://localhost:6006", project: "granite-demo",
    });
  });
});

describe("Run and finding controls", () => {
  it("shows where a run lives and sends it to a platform", async () => {
    const calls = mockApi({
      "GET /connections": () => [phoenix], "GET /runs/run_1/links": () => [link],
      "POST /runs/run_1/export": () => ({ connection_id: "con_1", run_id: "run_1", trace_id: "e".repeat(32), spans_sent: 6, spans_total: 6 }),
    });
    render(<RunPlatforms runId="run_1" />);
    expect(await screen.findByText(/imported from Phoenix · Local Phoenix/)).toBeInTheDocument();
    expect(screen.getByText("lineage: value")).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: "Send to" }));
    expect(await screen.findByText(/Sent 6 spans/)).toBeInTheDocument();
    expect(calls.some((c) => c.url === "/api/runs/run_1/export")).toBe(true);
  });

  it("renders nothing without connections, and the verdict button only for linked runs", async () => {
    mockApi({ "GET /connections": () => [], "GET /runs/run_1/links": () => [] });
    const { container } = render(<><RunPlatforms runId="run_1" /><SendVerdict findingId="fnd_1" runId="run_1" /></>);
    await new Promise((r) => setTimeout(r, 20));
    expect(container).toBeEmptyDOMElement();
  });

  it("writes the verdict back and shows errors from the platform", async () => {
    let fail = false;
    mockApi({
      "GET /runs/run_1/links": () => [link],
      "POST /findings/fnd_1/writeback": () => (fail ? problem(502, { detail: "Phoenix request failed" })
        : { finding_id: "fnd_1", label: "confirmed", step_id: "s2", explanation: "", written: [{ connection_id: "con_1", kind: "phoenix", span_id: "d", ref: "a1" }] }),
    });
    render(<SendVerdict findingId="fnd_1" runId="run_1" />);
    await userEvent.click(await screen.findByRole("button", { name: "Send verdict" }));
    expect(await screen.findByText("“confirmed” written to 1 platform")).toBeInTheDocument();
    fail = true;
    await userEvent.click(screen.getByRole("button", { name: "Send verdict" }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Phoenix request failed");
  });
});
