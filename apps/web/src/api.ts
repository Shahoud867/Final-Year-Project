import type {
  Example, Experiment, FindingDetail, FindingSummary, Graph, Health, Job, RunDetail, RunSummary, TaskInput, Workflow,
} from "./types";

/** An error from the API, already phrased for a person (RFC 7807 problem body). */
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public fields: Record<string, string> = {},
    public allowedActions: string[] = [],
  ) {
    super(message);
  }
}

const TOKEN_KEY = "granite.token";
export const getToken = (): string => {
  try { return localStorage.getItem(TOKEN_KEY) ?? ""; } catch { return ""; }
};
export const setToken = (value: string): void => {
  try {
    if (value) localStorage.setItem(TOKEN_KEY, value);
    else localStorage.removeItem(TOKEN_KEY);
  } catch { /* private mode */ }
};

interface Problem { title?: string; detail?: string; errors?: { field: string; message: string }[]; allowed_actions?: string[] }

export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = getToken();
  let res: Response;
  try {
    res = await fetch(`/api${path}`, {
      ...init,
      headers: {
        ...(init.body ? { "Content-Type": "application/json" } : {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...init.headers,
      },
    });
  } catch {
    throw new ApiError("Cannot reach the Granite server. Is it running?", 0);
  }
  if (res.ok) return (res.headers.get("content-type")?.includes("json") ? res.json() : res.text()) as Promise<T>;
  let problem: Problem = {};
  try { problem = (await res.json()) as Problem; } catch { /* not JSON */ }
  const fields = Object.fromEntries((problem.errors ?? []).map((e) => [e.field, e.message]));
  const detail = problem.detail || problem.title || `Request failed (${res.status})`;
  throw new ApiError(detail, res.status, fields, problem.allowed_actions ?? []);
}

const post = <T>(path: string, body: unknown) => request<T>(path, { method: "POST", body: JSON.stringify(body) });

export const PAGE = 25;

export interface FindingFilter { q?: string; severity?: string; level?: string; status?: string; limit?: number }

/** Query string from the filters that have a value. */
export function qs(params: Record<string, string | number | undefined>): string {
  const u = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) if (v !== undefined && v !== "") u.set(k, String(v));
  return u.toString();
}

export interface RunRequest { task_input: TaskInput; fault: string | null; mode?: string; seed?: number }

export const api = {
  health: () => request<Health>("/health"),
  workflows: () => request<Workflow[]>("/workflows"),
  examples: (key: string) => request<Example[]>(`/workflows/${key}/examples`),
  createRun: (body: RunRequest) => post<{ run_id: string; job_id: string }>("/runs", { workflow: "refund_desk", ...body }),
  runs: (q = "") => request<RunSummary[]>(`/runs?${qs({ q, limit: PAGE })}`),
  run: (id: string) => request<RunDetail>(`/runs/${id}`),
  graph: (id: string) => request<Graph>(`/runs/${id}/graph`),
  findings: (f: FindingFilter = {}) => request<FindingSummary[]>(`/findings?${qs({ ...f, limit: f.limit ?? PAGE })}`),
  finding: (id: string) => request<FindingDetail>(`/findings/${id}`),
  report: (id: string) => request<string>(`/findings/${id}/report`),
  verify: (hypothesisId: string, n: number, m: number) =>
    post<{ job_id: string; experiment_id: string }>(`/hypotheses/${hypothesisId}/experiments`, { n, m }),
  experiment: (id: string) => request<Experiment>(`/experiments/${id}`),
  review: (id: string, decision: string, comment: string, reviewer: string) =>
    post(`/findings/${id}/reviews`, { decision, comment, reviewer }),
  job: (id: string) => request<Job>(`/jobs/${id}`),
  testLlm: () => post<{ ok: boolean; mode: string; message: string }>("/settings/test-llm", {}),
};

/** Poll a job until it finishes; reports progress. Resolves with the final job row. */
export async function waitForJob(id: string, onProgress?: (job: Job) => void, intervalMs = 800): Promise<Job> {
  for (;;) {
    const job = await api.job(id);
    onProgress?.(job);
    if (job.status === "succeeded" || job.status === "failed") return job;
    await new Promise((r) => setTimeout(r, intervalMs));
  }
}
