import type { RunDetail, RunSummary, Scope, Stats } from "./types";

const BASE = "/api";
// Static-export mode: bakes a frozen snapshot of the live backend's responses
// into the bundle (see src/staticData.json + README-static-export.md), so the
// built app is one shareable, self-contained page with zero server dependency.
// Toggled at build time only -- `npm run dev` is completely unaffected.
export const STATIC = import.meta.env.VITE_STATIC_EXPORT === "true";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API ${path} failed: ${res.status}`);
  }
  return res.json();
}

// Mirrors backend/main.py's list_runs() filtering exactly (status exact
// match, spike normalized-equal, q substring over question/scenario).
function filterRuns(all: RunSummary[], params?: { status?: string; spike?: string; q?: string }): RunSummary[] {
  let out = all;
  if (params?.status) out = out.filter((r) => r.status === params.status);
  if (params?.spike) {
    const norm = (s: string) => s.toLowerCase().replace(/\s+/g, "");
    out = out.filter((r) => norm(r.spike) === norm(params.spike!));
  }
  if (params?.q) {
    const ql = params.q.toLowerCase();
    out = out.filter((r) => r.question.toLowerCase().includes(ql) || r.scenario.toLowerCase().includes(ql));
  }
  return out;
}

async function staticData() {
  const mod = await import("./staticData.json");
  // Same trust-the-backend contract as the fetch path above (res.json()
  // returns `any` there too) -- the raw /api/runs/{id} payload omits a few
  // RunSummary-only fields (has_fault etc.) that RunDetail.tsx never reads.
  return mod.default as unknown as { stats: Stats; runsList: RunSummary[]; runsById: Record<string, RunDetail>; scope: Scope };
}

export const api = STATIC
  ? {
      stats: async () => (await staticData()).stats,
      runs: async (params?: { status?: string; spike?: string; q?: string }) =>
        filterRuns((await staticData()).runsList, params),
      run: async (id: string) => {
        const d = await staticData();
        const run = d.runsById[id];
        if (!run) throw new Error(`No run with id '${id}'`);
        return run;
      },
      scope: async () => (await staticData()).scope,
    }
  : {
      stats: () => get<Stats>("/stats"),
      runs: (params?: { status?: string; spike?: string; q?: string }) => {
        const qs = new URLSearchParams();
        if (params?.status) qs.set("status", params.status);
        if (params?.spike) qs.set("spike", params.spike);
        if (params?.q) qs.set("q", params.q);
        const suffix = qs.toString() ? `?${qs.toString()}` : "";
        return get<RunSummary[]>(`/runs${suffix}`);
      },
      run: (id: string) => get<RunDetail>(`/runs/${id}`),
      scope: () => get<Scope>("/scope"),
    };
