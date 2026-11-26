import { tmpdir } from "node:os";
import { join } from "node:path";
import { defineConfig, devices } from "@playwright/test";

/**
 * Browser test of the main journey against the real API in recorded mode (no model needed), serving the built
 * interface from apps/web/dist. Build first: `npm run build`. The API's Python comes from GRANITE_PYTHON.
 */
const port = Number(process.env.GRANITE_E2E_PORT ?? 8031);
const python = process.env.GRANITE_PYTHON ?? "python";

export default defineConfig({
  testDir: "e2e",
  testMatch: /.*\.e2e\.ts/,
  timeout: 120_000,
  expect: { timeout: 20_000 },
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["list"], ["html", { open: "never", outputFolder: "playwright-report" }]] : "list",
  use: {
    baseURL: `http://127.0.0.1:${port}`,
    trace: "retain-on-failure",
    // the server's content-security policy refuses inline scripts; the test injects axe-core to measure contrast
    bypassCSP: true,
    // locally the installed Chrome is used; CI installs Playwright's own Chromium
    ...(process.env.CI ? {} : { channel: "chrome" }),
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"], viewport: { width: 1366, height: 900 } } },
    { name: "phone", use: { ...devices["Pixel 7"] } },
  ],
  webServer: {
    command: `"${python}" -m uvicorn granite_api.main:app_from_env --factory --port ${port}`,
    cwd: "../api",
    url: `http://127.0.0.1:${port}/api/health`,
    timeout: 120_000,
    reuseExistingServer: false,
    env: {
      GRANITE_LLM_MODE: "recorded",
      GRANITE_DB_URL: `sqlite:///${join(tmpdir(), `granite-e2e-${process.pid}.db`).replace(/\\/g, "/")}`,
      GRANITE_STATIC_DIR: "../web/dist",
      GRANITE_RATE_LIMIT: "0",
    },
  },
});
