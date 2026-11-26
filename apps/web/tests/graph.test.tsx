import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Graph } from "../src/components/Graph";
import { silentGraph } from "./fixtures";

describe("pipeline graph", () => {
  it("names every step with its kind, check status and where the symptom showed", () => {
    render(<Graph graph={silentGraph} onSelect={() => undefined} />);
    expect(screen.getByRole("group")).toHaveAccessibleName(/Order Lookup: failed, Policy: ok, Refund Calculator: failed, Writer: failed/);
    expect(screen.getByRole("button", { name: "Order Lookup: Tool step, check failed" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Writer: LLM step, check failed, symptom shows here" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Policy: Code step, no failed check" })).toBeInTheDocument();
    // the run's input is context, not a step: it is not a button
    expect(screen.queryByRole("button", { name: /Task input/ })).not.toBeInTheDocument();
  });

  it("selects a step with Enter or Space and marks the selected one as pressed", async () => {
    const picked: string[] = [];
    const { rerender } = render(<Graph graph={silentGraph} onSelect={(id) => picked.push(id)} />);
    screen.getByRole("button", { name: /Order Lookup/ }).focus();
    await userEvent.keyboard("{Enter}");
    await userEvent.keyboard(" ");
    expect(picked).toEqual(["s2", "s2"]);
    rerender(<Graph graph={silentGraph} onSelect={(id) => picked.push(id)} selected="s2" />);
    expect(screen.getByRole("button", { name: /Order Lookup/ })).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByRole("button", { name: /Policy/ })).toHaveAttribute("aria-pressed", "false");
  });

  it("says which step is suspected, confirmed or refuted, in words as well as colour", () => {
    const { rerender, container } = render(
      <Graph graph={silentGraph} onSelect={() => undefined} marks={{ s2: "suspect" }} path={["s2", "s3", "s5"]} />);
    expect(screen.getByRole("button", { name: /Order Lookup: Tool step, check failed, suspect/ })).toBeInTheDocument();
    expect(container.querySelectorAll(".edge.on-path")).toHaveLength(2); // s2 -> s3 and s3 -> s5
    expect(container.querySelector(".graph")).not.toHaveClass("confirmed");
    expect(screen.getByRole("button", { name: /Intake/ })).toHaveClass("dim"); // not on the highlighted path

    rerender(<Graph graph={silentGraph} onSelect={() => undefined} marks={{ s2: "origin", s4: "refuted" }} path={["s2", "s3", "s5"]} />);
    expect(screen.getByRole("button", { name: /Order Lookup.*origin confirmed/ })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Refund Calculator.*refuted/ })).toBeInTheDocument();
    expect(container.querySelector(".graph")).toHaveClass("confirmed");
  });

  it("draws a workflow that has not run without any check status", () => {
    const plan = { nodes: silentGraph.nodes.map((n) => ({ ...n, symptom: false })), edges: silentGraph.edges };
    const { container } = render(<Graph graph={plan} plain notes={{ s2: "get_order_details" }} running label="Execution order" />);
    expect(screen.getByRole("group")).toHaveAccessibleName(/^Execution order\. Task input: Input, Intake: LLM, Order Lookup: Tool/);
    expect(container.querySelectorAll(".glyph")).toHaveLength(0);
    expect(container.querySelector(".tag")).toBeNull();
    expect(screen.getByText("get_order_details")).toBeInTheDocument();
    expect(container.querySelector(".graph")).toHaveClass("running");
  });

  it("merges the fields that flow between two steps into one edge", () => {
    const { container } = render(<Graph graph={silentGraph} />);
    const titles = [...container.querySelectorAll(".edge title")].map((t) => t.textContent);
    expect(titles).toContain("s2 → s3: status, user_id, items, payment_method");
    expect(container.querySelectorAll(".edge")).toHaveLength(8);
  });
});
