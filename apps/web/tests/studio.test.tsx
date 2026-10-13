import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { NewRun, validateTask } from "../src/pages/NewRun";
import { examples, health, workflows } from "./fixtures";
import { mockApi, problem } from "./helpers";

afterEach(() => { vi.unstubAllGlobals(); window.location.hash = ""; });

const delivered = examples.find((e) => e.label.includes("(delivered)"))!;
const cancelled = examples.find((e) => e.label.includes("(cancelled)"))!;
const routes = (over: Record<string, () => unknown> = {}) => ({
  "GET /health": () => health,
  "GET /workflows/refund_desk/examples": () => examples,
  "GET /workflows": () => workflows,
  "POST /runs": () => ({ run_id: "run_9", job_id: "job_9" }),
  "GET /jobs/job_9": () => ({ id: "job_9", status: "succeeded", progress_done: 1, progress_total: 1, message: "done" }),
  ...over,
});
const posted = (calls: { url: string; init?: RequestInit }[]) => JSON.parse(String(calls.find((c) => c.init?.method === "POST")?.init?.body));

describe("Task Studio scenarios", () => {
  it("fills the form from the delivered example, injects the stale price, and opens the trace when the run finishes", async () => {
    const calls = mockApi(routes());
    const user = userEvent.setup();
    render(<NewRun />);
    await user.click(await screen.findByRole("radio", { name: /Silent price discrepancy/ }));
    expect(screen.getByLabelText("Order id")).toHaveValue(delivered.order_id);
    expect(screen.getByLabelText("Customer e-mail")).toHaveValue(delivered.email);
    expect(screen.getByLabelText("Inject a fault")).toHaveValue("stale_price");
    await user.click(screen.getByRole("button", { name: "Run workflow" }));
    await waitFor(() => expect(window.location.hash).toBe("#/runs/run_9"));
    expect(posted(calls)).toEqual({
      workflow: "refund_desk", fault: "stale_price", mode: "auto", seed: 1,
      task_input: { message: delivered.message, email: delivered.email, order_id: delivered.order_id },
    });
  });

  it("runs the clean baseline with no fault and the edge case on the cancelled order", async () => {
    mockApi(routes());
    const user = userEvent.setup();
    render(<NewRun />);
    await user.click(await screen.findByRole("radio", { name: /Clean baseline/ }));
    expect(screen.getByLabelText("Inject a fault")).toHaveValue("none");
    expect(screen.getByLabelText("Order id")).toHaveValue(delivered.order_id);
    await user.click(screen.getByRole("radio", { name: /Cancelled-order edge case/ }));
    expect(screen.getByLabelText("Order id")).toHaveValue(cancelled.order_id);
    expect(screen.getByLabelText("Inject a fault")).toHaveValue("stale_price");
  });

  it("marks the scenario as custom once a field is edited by hand", async () => {
    mockApi(routes());
    const user = userEvent.setup();
    render(<NewRun />);
    const silent = await screen.findByRole("radio", { name: /Silent price discrepancy/ });
    await user.click(silent);
    expect(silent).toBeChecked();
    await user.type(screen.getByLabelText("Customer message"), " Thanks.");
    expect(silent).not.toBeChecked();
    expect(screen.getByText("Custom task: the fields below were edited by hand.")).toBeInTheDocument();
  });

  it("shows what will run from the workflow the server describes, with the fault marked on its target step", async () => {
    mockApi(routes());
    render(<NewRun />);
    const graph = await screen.findByRole("group", { name: /^Execution order\./ });
    expect(graph).toHaveAccessibleName(/Intake: LLM, Order Lookup: Tool, Policy: Code, Refund Calculator: LLM, Writer: LLM/);
    expect(graph.querySelector(".tag.fault")).not.toBeNull(); // stale price is selected by default
    const wf = workflows[0]!;
    expect(screen.getByText(`${wf.checks.filter((c) => c.scope === "outcome").length} outcome, ${wf.checks.filter((c) => c.scope !== "outcome").length} step`)).toBeInTheDocument();
    for (const c of wf.checks) expect(screen.getByText(c.id)).toBeInTheDocument();
  });
});

describe("Task Studio validation", () => {
  it("knows the server's rules for a task", () => {
    expect(validateTask({ message: "hi", email: "x", order_id: "12" })).toEqual({
      message: "Enter at least 3 characters", email: "Must look like name@example.com", order_id: "Must look like #W1234567",
    });
    expect(validateTask({ message: "x".repeat(2001), email: "a@b.co", order_id: "#W123" })).toEqual({ message: "Enter at most 2000 characters" });
    expect(validateTask({ message: "Return it", email: "a@b.co", order_id: "#W1234567" })).toEqual({});
  });

  it("stops an invalid task before any request, marks each field and moves focus to the first one", async () => {
    const calls = mockApi(routes());
    const user = userEvent.setup();
    render(<NewRun />);
    await screen.findByRole("radio", { name: /Silent price discrepancy/ });
    await user.type(screen.getByLabelText("Customer message"), "hi");
    await user.type(screen.getByLabelText("Order id"), "12");
    await user.click(screen.getByRole("button", { name: "Run workflow" }));
    expect(screen.getByText("Please fix the highlighted fields.")).toBeInTheDocument();
    expect(screen.getByText("Enter at least 3 characters")).toBeInTheDocument();
    expect(screen.getByText("Must look like #W1234567")).toBeInTheDocument();
    for (const name of ["Customer message", "Customer e-mail", "Order id"]) expect(screen.getByLabelText(name)).toHaveAttribute("aria-invalid", "true");
    expect(screen.getByLabelText("Customer message")).toHaveFocus();
    expect(calls.some((c) => c.init?.method === "POST")).toBe(false);
  });

  it("edits the exact request body as JSON, and refuses bodies the server would refuse", async () => {
    const calls = mockApi(routes());
    const user = userEvent.setup();
    render(<NewRun />);
    await user.click(await screen.findByRole("radio", { name: /Clean baseline/ }));
    await user.click(screen.getByRole("radio", { name: "JSON" }));
    const body = screen.getByLabelText("Request body (JSON)") as HTMLTextAreaElement;
    expect(JSON.parse(body.value)).toMatchObject({ workflow: "refund_desk", fault: null, seed: 1, mode: "auto" });

    await user.clear(body);
    await user.paste("{ not json");
    expect(screen.getByText(/^Not valid JSON:/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Run workflow" })).toBeDisabled();

    await user.clear(body);
    await user.paste(JSON.stringify({ workflow: "refund_desk", task_input: delivered, fault: null }));
    expect(screen.getByText('Unknown key "task_input.label". A task has only: message, email, order_id.')).toBeInTheDocument();

    await user.clear(body);
    await user.paste(JSON.stringify({ workflow: "refund_desk", task_input: { message: delivered.message, email: delivered.email, order_id: delivered.order_id }, fault: "stale_price", seed: 7, mode: "recorded", debug: true }));
    expect(screen.getByText(/^Unknown key "debug"\./)).toBeInTheDocument();

    await user.clear(body);
    await user.paste(JSON.stringify({ workflow: "refund_desk", task_input: { message: delivered.message, email: delivered.email, order_id: delivered.order_id }, fault: "stale_price", seed: 7, mode: "recorded" }));
    await user.click(screen.getByRole("button", { name: "Run workflow" }));
    await waitFor(() => expect(window.location.hash).toBe("#/runs/run_9"));
    expect(posted(calls)).toMatchObject({ fault: "stale_price", seed: 7, mode: "recorded" });
  });
});

describe("Task Studio execution", () => {
  it("says which mode the server uses and warns before a live run when no model is reachable", async () => {
    mockApi(routes());
    const user = userEvent.setup();
    render(<NewRun />);
    expect(await screen.findByText(/Live model not reachable now/)).toBeInTheDocument();
    expect(screen.queryByText("No live model is reachable")).not.toBeInTheDocument();
    await user.click(screen.getByRole("radio", { name: /^Live model/ }));
    expect(screen.getByText("No live model is reachable")).toBeInTheDocument();
  });

  it("sends the chosen mode and seed", async () => {
    const calls = mockApi(routes());
    const user = userEvent.setup();
    render(<NewRun />);
    await user.click(await screen.findByRole("radio", { name: /Silent price discrepancy/ }));
    await user.click(screen.getByRole("radio", { name: /^Recorded cassette/ }));
    await user.clear(screen.getByLabelText("Seed"));
    await user.type(screen.getByLabelText("Seed"), "42");
    await user.click(screen.getByRole("button", { name: "Run workflow" }));
    await waitFor(() => expect(window.location.hash).toBe("#/runs/run_9"));
    expect(posted(calls)).toMatchObject({ mode: "recorded", seed: 42 });
  });

  it("gives recovery guidance when the server refuses the run, and lets the user try again", async () => {
    mockApi(routes({ "POST /runs": () => problem(429, { title: "Too many requests", detail: "Limit is 120 changes per minute; slow down." }) }));
    const user = userEvent.setup();
    render(<NewRun />);
    await user.click(await screen.findByRole("radio", { name: /Silent price discrepancy/ }));
    await user.click(screen.getByRole("button", { name: "Run workflow" }));
    const alert = await screen.findByRole("alert");
    expect(alert).toHaveTextContent("Limit is 120 changes per minute; slow down.");
    expect(alert).toHaveTextContent("Wait a moment, then run again.");
    expect(screen.getByRole("button", { name: "Run workflow" })).toBeEnabled();
  });
});
