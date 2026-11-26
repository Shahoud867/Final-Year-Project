/// <reference types="vitest/config" />
import { execSync } from "node:child_process";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const api = process.env.GRANITE_API_URL ?? "http://127.0.0.1:8000";

/** Commit the bundle is built from: set by the container build or CI, else read from git, else unknown (""). */
function buildSha(): string {
  const fromEnv = process.env.GRANITE_BUILD_SHA || process.env.RENDER_GIT_COMMIT || process.env.GITHUB_SHA;
  if (fromEnv) return fromEnv.slice(0, 7);
  try { return execSync("git rev-parse --short=7 HEAD", { stdio: ["ignore", "pipe", "ignore"] }).toString().trim(); } catch { return ""; }
}

// Tests get a fixed stamp so nothing depends on the clock or the checkout.
const build = process.env.VITEST
  ? { sha: "", time: "", repo: "Shahoud867/Final-Year-Project" }
  : { sha: buildSha(), time: new Date().toISOString(), repo: process.env.GRANITE_REPO ?? "Shahoud867/Final-Year-Project" };

export default defineConfig({
  plugins: [react()],
  define: { __GRANITE_BUILD__: JSON.stringify(build) },
  server: { port: 5173, proxy: { "/api": api } },
  // no inlined assets: the server's content-security policy allows fonts from this origin only, not data: URLs
  build: { outDir: "dist", sourcemap: false, assetsInlineLimit: 0 },
  test: { environment: "jsdom", globals: true, setupFiles: ["tests/setup.ts"], css: false },
});
