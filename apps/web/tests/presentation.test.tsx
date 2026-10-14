/**
 * Presentation contract: the decisions that make the interface readable and quiet.
 *
 * These guard choices that are easy to undo by accident in a stylesheet or a quick edit:
 * the light default, the three-size type scale, the collapsed reference detail on the guide,
 * and the rule that a number shown once is not then repeated in words.
 */
import { render, screen, within } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import App from "../src/App";
import { Guide } from "../src/pages/Guide";
import { Home } from "../src/pages/Home";
import { cancelledRun, cleanRun, erroredRun, findingConfirmed, health, silentRun, workflows } from "./fixtures";
import { mockApi } from "./helpers";

afterEach(() => { vi.unstubAllGlobals(); window.location.hash = ""; localStorage.clear(); });

const tokens = readFileSync(resolve(process.cwd(), "src/styles/tokens.css"), "utf8");
const light = tokens.slice(0, tokens.indexOf(':root[data-theme="dark"]'));

/** Relative luminance and contrast ratio, per WCAG 2.2. */
function luminance(hex: string) {
  const to = (c: number) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const [r, g, b] = [1, 3, 5].map((i) => to(parseInt(hex.slice(i, i + 2), 16) / 255));
  return 0.2126 * r! + 0.7152 * g! + 0.0722 * b!;
}
function contrast(fg: string, bg: string) {
  const [a, b] = [luminance(fg), luminance(bg)].sort((x, y) => y - x);
  return (a! + 0.05) / (b! + 0.05);
}
const token = (name: string) => light.match(new RegExp(`--${name}:\\s*(#[0-9a-f]{6})`, "i"))?.[1] ?? "";

describe("presentation: theme and type scale", () => {
  it("opens in the light theme, so the first view needs no setting changed", async () => {
    mockApi({ "GET /health": () => health, "GET /workflows": () => workflows, "GET /findings/summary": () => ({}), "GET /findings": () => [], "GET /runs": () => [] });
    render(<App />);
    expect(document.documentElement.dataset.theme).toBe("light");
    expect(await screen.findByRole("button", { name: "Switch to dark theme" })).toBeInTheDocument();
  });

  it("defines three font sizes, with the older names kept as aliases", () => {
    const real = [...light.matchAll(/--fs-[\w-]+:\s*([\d.]+rem)/g)].map((m) => m[1]);
    expect(new Set(real).size).toBe(3);
    for (const alias of ["xs", "md", "xl", "2xl"]) {
      expect(light).toMatch(new RegExp(`--fs-${alias}:\\s*var\\(--fs-`));
    }
  });

  it("keeps every status colour readable on the page and on a card", () => {
    const page = token("bg");
    const card = token("surface");
    for (const name of ["text", "text-2", "text-3", "ok-text", "bad-text", "warn-text", "replay-text"]) {
      const fg = token(name);
      expect(fg, `--${name} is missing from the light theme`).toMatch(/^#[0-9a-f]{6}$/i);
      expect(contrast(fg, page), `--${name} on the page`).toBeGreaterThanOrEqual(4.5);
      expect(contrast(fg, card), `--${name} on a card`).toBeGreaterThanOrEqual(4.5);
    }
  });

  it("answers a request for more contrast from the operating system", () => {
    const base = readFileSync(resolve(process.cwd(), "src/styles/base.css"), "utf8");
    expect(base).toMatch(/@media \(prefers-contrast: more\)/);
  });
});

describe("presentation: what the pages show", () => {
  it("folds each feature's inputs and outputs away until they are asked for", async () => {
    mockApi({ "GET /health": () => health });
    const { container } = render(<Guide />);
    const folds = container.querySelectorAll("details.guide-io-more");
    expect(folds.length).toBeGreaterThanOrEqual(8);
    for (const fold of folds) expect(fold).not.toHaveAttribute("open");
    expect((folds[0] as HTMLElement).querySelector("summary")).toHaveTextContent(/inputs and outputs/i);
  });

  it("states a count once: the run tile shows the legend, not the same split in words", async () => {
    mockApi({
      "GET /findings/summary": () => ({ confirmed: 1 }),
      "GET /findings": () => [findingConfirmed],
      "GET /runs": () => [silentRun, cleanRun, cancelledRun, erroredRun],
    });
    render(<Home />);
    const tile = within((await screen.findByText("Executions")).closest(".stat") as HTMLElement);
    expect(tile.getByText(/\d+ completed/)).toBeInTheDocument();
    expect(tile.queryByText(/with injected fault/)).not.toBeInTheDocument();
  });
});
