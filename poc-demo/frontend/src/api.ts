import type { RunDetail, RunSummary, Scope, Stats } from "./types";

const BASE = "/api";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API ${path} failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
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
