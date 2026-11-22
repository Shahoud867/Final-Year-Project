import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "../src/App";
import { health } from "./fixtures";
import { mockApi, problem } from "./helpers";

afterEach(() => { vi.unstubAllGlobals(); window.location.hash = ""; localStorage.clear(); sessionStorage.clear(); delete document.documentElement.dataset.theme; });

const base = { "GET /health": () => health, "GET /runs": () => [], "GET /findings": () => [] };

describe("application shell", () => {
  it("puts the working pages first and the explanations in a help group, and marks the current one", async () => {
    mockApi(base);
    window.location.hash = "#/evidence";
    render(<App />);
    const nav = screen.getByRole("navigation", { name: "Main" });
    expect(within(nav).getAllByRole("link").map((a) => a.textContent)).toEqual(["Inbox", "Runs", "Fault Lab", "Evaluation", "Connections", "How it works", "Why Granite"]);
    expect(within(within(nav).getByRole("group", { name: "Help" })).getAllByRole("link").map((a) => a.textContent)).toEqual(["How it works", "Why Granite"]);
    expect(within(nav).getByRole("link", { name: "Why Granite" })).toHaveAttribute("aria-current", "page");
    expect(within(nav).getByRole("link", { name: "Inbox" })).not.toHaveAttribute("aria-current");
    expect(await screen.findByRole("heading", { level: 1, name: "Why Granite" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "New run" })).toHaveAttribute("href", "#/new");
  });

  it("keeps the section of a run page and a case file highlighted", async () => {
    mockApi(base);
    window.location.hash = "#/runs/run_x";
    const { unmount } = render(<App />);
    expect(within(screen.getByRole("navigation", { name: "Main" })).getByRole("link", { name: "Runs" })).toHaveAttribute("data-active");
    unmount();
    window.location.hash = "#/findings/fnd_x";
    render(<App />);
    expect(within(screen.getByRole("navigation", { name: "Main" })).getByRole("link", { name: "Inbox" })).toHaveAttribute("data-active");
  });

  it("serves the style guide in development builds", async () => {
    mockApi(base);
    window.location.hash = "#/styleguide";
    render(<App />);
    expect(await screen.findByRole("heading", { level: 1, name: "Style guide" })).toBeInTheDocument();
    expect(screen.getAllByRole("img", { name: /^Evidence level V\d of V3/ })).toHaveLength(4);
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

  it("switches between the light and dark themes and remembers the choice", async () => {
    mockApi(base);
    const user = userEvent.setup();
    render(<App />);
    expect(document.documentElement.dataset.theme).toBe("light");
    await user.click(screen.getByRole("button", { name: "Switch to dark theme" }));
    expect(document.documentElement.dataset.theme).toBe("dark");
    expect(localStorage.getItem("granite.theme")).toBe("dark");
    expect(screen.getByRole("button", { name: "Switch to light theme" })).toBeInTheDocument();
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
    expect(screen.getByRole("link", { name: "Back to the inbox" })).toHaveAttribute("href", "#/");
  });
});
