import { createRequire } from "node:module";
import { expect, test } from "@playwright/test";
import type { Page } from "@playwright/test";

const axePath = createRequire(import.meta.url).resolve("axe-core/axe.min.js");

/** Colour contrast can only be measured with real layout, so it is checked here and not in the jsdom suite. */
async function contrastViolations(page: Page): Promise<string[]> {
  await page.addScriptTag({ path: axePath });
  return page.evaluate(async () => {
    const axe = (window as unknown as { axe: { run: (ctx: unknown, opts: unknown) => Promise<{ violations: { id: string; nodes: { target: string[] }[] }[] }> } }).axe;
    const r = await axe.run(document, { runOnly: { type: "rule", values: ["color-contrast"] } });
    return r.violations.flatMap((v) => v.nodes.map((n) => `${v.id}: ${n.target.join(" ")}`));
  });
}

test("a silent failure is run, traced, verified by replay and decided by a person", async ({ page, isMobile }) => {
  await page.goto("/#/");
  await expect(page.getByRole("heading", { level: 1, name: "Inbox" })).toBeVisible();
  expect(await contrastViolations(page)).toEqual([]);

  // run the Refund Desk with the stale-price fault
  await page.getByRole("link", { name: "New run" }).first().click();
  await expect(page.getByRole("heading", { level: 1, name: "New run" })).toBeVisible();
  await page.getByRole("radio", { name: /Silent price discrepancy/ }).check();
  await expect(page.getByLabel("Order id")).toHaveValue(/^#W/);
  // recorded answers keep the journey deterministic even where a live model is reachable
  await page.getByRole("radiogroup", { name: "Execution mode" }).getByRole("radio", { name: /Recorded cassette/ }).check();
  await page.getByRole("button", { name: "Run workflow" }).click();

  // the run page: monitoring sees success, the checks see the wrong refund
  await expect(page.getByRole("heading", { level: 1, name: /^Run #W/ })).toBeVisible();
  await expect(page.getByText("Silent failure", { exact: true })).toBeVisible();
  await expect(page.getByText("Run status: completed")).toBeVisible();
  await page.getByRole("tab", { name: /Checks/ }).click();
  await expect(page.getByRole("region", { name: "Outcome checks" }).getByText("CHK-OUT-1")).toBeVisible();
  await page.getByRole("tab", { name: /Trace/ }).click();
  expect(await contrastViolations(page)).toEqual([]);

  // the case file: verify the first-ranked suspect by controlled replay
  await page.getByRole("link", { name: "Investigate" }).click();
  await expect(page.getByText("Case file")).toBeVisible();
  const rail = page.getByRole("complementary", { name: "Case summary" });
  await expect(rail.getByText("Not verified by replay yet.")).toBeVisible();
  await page.getByRole("button", { name: "Verify", exact: true }).first().click();
  await expect(page.getByRole("article", { name: "Experiment on Order Lookup: Confirmed" })).toBeVisible({ timeout: 90_000 });
  await expect(rail.getByText("5/5")).toBeVisible();
  await expect(rail.getByText("0/2")).toBeVisible();

  // a person decides; the software never closes the finding
  await rail.getByRole("button", { name: "Record your decision" }).click();
  await page.getByLabel("Your name").fill("e2e reviewer");
  await page.getByRole("button", { name: "Accept" }).click();
  await expect(page.getByRole("img", { name: "Evidence level V3 of V3: human-confirmed" }).first()).toBeVisible();
  expect(await contrastViolations(page)).toEqual([]);

  // the dark theme keeps the same contrast
  if (!isMobile) {
    await page.getByRole("button", { name: "Switch to dark theme" }).click();
    expect(await contrastViolations(page)).toEqual([]);
    await page.getByRole("button", { name: "Switch to light theme" }).click();
  }

  // back in the inbox the case is listed as decided
  await page.goto("/#/");
  await page.getByRole("tab", { name: /Decided/ }).click();
  await expect(page.getByRole("tabpanel").getByRole("link", { name: /Stated refund/ }).first()).toBeVisible();
});
