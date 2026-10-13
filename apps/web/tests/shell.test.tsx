import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "../src/App";
import { health } from "./fixtures";
import { mockApi, problem } from "./helpers";

afterEach(() => { vi.unstubAllGlobals(); window.location.hash = ""; localStorage.clear(); sessionStorage.clear(); delete document.documentElement.dataset.theme; });

const base = { "GET /health": () => health, "GET /runs": () => [], "GET /findings": () => [] };

describe("application shell", () => {
  it("offers the four sections and marks the current one", async () => {
    mockApi(base);
    window.location.hash = "#/evidence";
    render(<App />);
    const nav = screen.getByRole("navigation", { name: "Main" });
    expect(within(nav).getAllByRole("link").map((a) => a.textContent)).toEqual(["Investigations", "Task Studio", "How it works", "Evidence"]);
    expect(within(nav).getByRole("link", { name: "Evidence" })).toHaveAttribute("aria-current", "page");
    expect(within(nav).getByRole("link", { name: "Investigations" })).not.toHaveAttribute("aria-current");
    expect(await screen.findByRole("heading", { level: 1, name: "Evidence" })).toBeInTheDocument();
  });

  it("shows how the server produces model answers, as the server reports it", async () => {
    mockApi(base);
    render(<App />);
    expect(await screen.findByRole("status", { name: "Server online, recorded mode" })).toBeInTheDocument();
    expect(screen.getAllByText("Recorded cassette").length).toBeGreaterThan(0);
    expect(screen.queryByText("model online")).not.toBeInTheDocument();
  });

  it("says so when the server cannot be reached, and claims nothing else", async () => {
    mockApi({ ...base, "GET /health": () => problem(503, { title: "Unavailable", detail: "down" }) });
    render(<App />);
    expect(await screen.findByText("server unreachable")).toBeInTheDocument();
    expect(screen.getByText("Server unreachable")).toBeInTheDocument();
    expect(screen.queryByText("Server online")).not.toBeInTheDocument();
    expect(screen.queryByText("Recorded cassette")).not.toBeInTheDocument();
  });

  it("does not pretend to know the build it was made from when there is no stamp", async () => {
    mockApi(base);
    render(<App />);
    expect(await screen.findByText("v0.1.0")).toBeInTheDocument();
    expect(screen.getByText("no build stamp")).toBeInTheDocument();
  });

  it("switches between the dark and light themes and remembers the choice", async () => {
    mockApi(base);
    const user = userEvent.setup();
    render(<App />);
    expect(document.documentElement.dataset.theme).toBe("dark");
    await user.click(screen.getByRole("button", { name: "Switch to light theme" }));
    expect(document.documentElement.dataset.theme).toBe("light");
    expect(localStorage.getItem("granite.theme")).toBe("light");
    expect(screen.getByRole("button", { name: "Switch to dark theme" })).toBeInTheDocument();
  });

  it("answers the Test model button with the server's own message", async () => {
    mockApi({ ...base, "POST /settings/test-llm": () => ({ ok: true, mode: "recorded", message: "Recorded mode: saved answers are used, no model needed." }) });
    const user = userEvent.setup();
    render(<App />);
    await user.click(screen.getByRole("button", { name: "Test model" }));
    expect(await screen.findByText("Recorded mode: saved answers are used, no model needed.")).toBeInTheDocument();
  });

  it("explains an unknown route and offers the way back", () => {
    mockApi(base);
    window.location.hash = "#/nowhere";
    render(<App />);
    expect(screen.getByRole("heading", { level: 1, name: "Page not found" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Back to investigations" })).toHaveAttribute("href", "#/");
  });
});
