import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Graph } from "../src/components/Graph";
import { Home } from "../src/pages/Home";
import { NewRun } from "../src/pages/NewRun";
import type { Graph as GraphData } from "../src/types";
import { mockApi, problem } from "./helpers";

afterEach(() => { vi.unstubAllGlobals(); window.location.hash = ""; });

describe("Home", () => {
  it("shows friendly empty states", async () => {
    mockApi({ "GET /runs": () => [], "GET /findings": () => [] });
    render(<Home />);
    expect(await screen.findByText(/No findings yet/)).toBeInTheDocument();
    expect(screen.getByText("No runs yet.")).toBeInTheDocument();
  });

  it("shows an error with a retry button when the server fails", async () => {
    mockApi({
      "GET /runs": () => problem(500, { title: "Internal error", detail: "Something went wrong on the server." }),
      "GET /findings": () => [],
    });
    render(<Home />);
    expect(await screen.findByRole("alert")).toHaveTextContent("Something went wrong on the server.");
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
  });
});

describe("NewRun", () => {
  it("loads an example into the form and shows server-side field errors", async () => {
    const example = { order_id: "#W1023987", email: "a@b.co", message: "Return the Pet Bed", label: "#W1023987 (delivered): Pet Bed" };
    mockApi({
      "GET /workflows/refund_desk/examples": () => [example],
      "POST /runs": () => problem(422, {
        title: "Invalid request", detail: "x", errors: [{ field: "email", message: "must look like name@example.com" }],
      }),
    });
    const user = userEvent.setup();
    render(<NewRun />);
    await user.selectOptions(await screen.findByLabelText("Load an example"), "0");
    expect(screen.getByLabelText("Order id")).toHaveValue("#W1023987");
    await user.click(screen.getByRole("button", { name: "Run workflow" }));
    expect(await screen.findByText("must look like name@example.com")).toBeInTheDocument();
    expect(screen.getByText("Please fix the highlighted fields.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Run workflow" })).toBeEnabled();
  });
});

describe("Graph", () => {
  const graph: GraphData = {
    nodes: [
      { id: "task", label: "Task input", kind: "input", status: "ok" },
      { id: "s1", label: "Intake", kind: "llm", status: "ok" },
      { id: "s2", label: "Order Lookup", kind: "tool", status: "failed" },
    ],
    edges: [{ source: "task", target: "s1", field: "message" }, { source: "s1", target: "s2", field: "order_id" }],
  };

  it("describes the whole run for screen readers and selects a step by keyboard", async () => {
    const picked: string[] = [];
    render(<Graph graph={graph} onSelect={(id) => picked.push(id)} />);
    expect(screen.getByRole("group")).toHaveAccessibleName(/Order Lookup: failed/);
    screen.getByRole("button", { name: /Order Lookup/ }).focus();
    await userEvent.keyboard("{Enter}");
    expect(picked).toEqual(["s2"]);
  });
});
