/**
 * Delivery evidence: what this bundle was built from, and the live state of the CI and CD workflows on GitHub.
 * Nothing here is assumed: the build stamp is written at build time and the workflow runs are read from GitHub's
 * public API when the page asks. If GitHub cannot be reached the status is "unknown", never "passed".
 */

import { ApiError } from "./api";

declare const __GRANITE_BUILD__: { sha: string; time: string; repo: string };

export interface BuildInfo { sha: string; time: string; repo: string }

/** Commit and time this bundle was built from ("" when the build did not know them), and the repository slug. */
export const BUILD: BuildInfo =
  typeof __GRANITE_BUILD__ === "undefined" ? { sha: "", time: "", repo: "Shahoud867/Final-Year-Project" } : __GRANITE_BUILD__;

export const repoUrl = (repo = BUILD.repo): string => `https://github.com/${repo}`;
export const commitUrl = (sha: string, repo = BUILD.repo): string => `${repoUrl(repo)}/commit/${sha}`;
export const actionsUrl = (repo = BUILD.repo): string => `${repoUrl(repo)}/actions`;
export const workflowFileUrl = (file: string, repo = BUILD.repo): string => `${repoUrl(repo)}/blob/main/.github/workflows/${file}`;

export interface WorkflowRun {
  id: number; name: string; run_number: number; status: string; conclusion: string | null;
  head_branch: string | null; head_sha: string; event: string; created_at: string; html_url: string;
}

export interface Pipeline { runs: WorkflowRun[]; fetchedAt: string }

const CACHE_KEY = "granite.pipeline";
const CACHE_MS = 120_000; // the unauthenticated GitHub API allows 60 requests an hour per address

function cached(): Pipeline | null {
  try {
    const raw = sessionStorage.getItem(CACHE_KEY);
    if (!raw) return null;
    const hit = JSON.parse(raw) as Pipeline;
    return Date.now() - new Date(hit.fetchedAt).getTime() < CACHE_MS ? hit : null;
  } catch { return null; }
}

/**
 * Latest workflow runs of the repository, newest first, straight from api.github.com. No credentials are sent
 * (the Granite access token never leaves this origin). Throws with a readable message when GitHub is unreachable.
 */
export async function fetchPipeline(repo = BUILD.repo, fresh = false): Promise<Pipeline> {
  const hit = fresh ? null : cached();
  if (hit) return hit;
  let res: Response;
  try {
    res = await fetch(`https://api.github.com/repos/${repo}/actions/runs?per_page=30`, { headers: { Accept: "application/vnd.github+json" } });
  } catch {
    throw new ApiError("GitHub could not be reached from this browser, so the pipeline status is unknown.", 0);
  }
  if (!res.ok) {
    throw new ApiError(res.status === 403 || res.status === 429
      ? "GitHub's request limit for this network was reached; the pipeline status is unknown until it resets."
      : `GitHub answered ${res.status}; the pipeline status is unknown.`, res.status);
  }
  const body = (await res.json()) as { workflow_runs?: WorkflowRun[] };
  const runs = (body.workflow_runs ?? []).map((r) => ({
    id: r.id, name: r.name, run_number: r.run_number, status: r.status, conclusion: r.conclusion,
    head_branch: r.head_branch, head_sha: r.head_sha, event: r.event, created_at: r.created_at, html_url: r.html_url,
  }));
  const out = { runs, fetchedAt: new Date().toISOString() };
  try { sessionStorage.setItem(CACHE_KEY, JSON.stringify(out)); } catch { /* private mode */ }
  return out;
}

/** Latest completed run of a workflow on a branch (or tag), ignoring runs GitHub skipped. */
export function latestRun(runs: WorkflowRun[], name: string, branch = "main"): WorkflowRun | null {
  return runs.find((r) => r.name === name && r.head_branch === branch && r.status === "completed" && r.conclusion !== "skipped") ?? null;
}

/** A run of the named workflow that finished successfully for exactly this commit, if GitHub lists one. */
export function passedFor(runs: WorkflowRun[], name: string, sha: string): WorkflowRun | null {
  if (!sha) return null;
  return runs.find((r) => r.name === name && r.conclusion === "success" && r.head_sha.startsWith(sha)) ?? null;
}

/** The jobs of ci.yml and cd.yml, in order, as plain names (the files are linked next to them in the interface). */
export const CI_JOBS: { name: string; does: string }[] = [
  { name: "Python", does: "ruff, mypy strict, unit, API and system tests with coverage gates, bandit, pip-audit, architecture rule" },
  { name: "Web", does: "ESLint, tsc, component and accessibility tests, production build, npm audit" },
  { name: "Secret scan", does: "gitleaks over the full history" },
  { name: "Container", does: "docker build, smoke test and system tests against the running image" },
];
export const CD_JOBS: { name: string; does: string }[] = [
  { name: "Publish image", does: "build, smoke-test that exact image, push to the GitHub Container Registry" },
  { name: "Deploy and verify", does: "ask Render to deploy, then smoke-test the public URL" },
  { name: "Release", does: "on a v* tag: tagged image and a GitHub Release" },
];
