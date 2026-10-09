import type { FindingDetail as Finding } from "../src/types";

type Handler = (url: string, init?: RequestInit) => unknown | Promise<unknown>;

/** Replace fetch with an in-memory API. Keys look like "GET /runs"; the first key that prefixes the request wins. */
export function mockApi(routes: Record<string, Handler>) {
  const calls: { url: string; init?: RequestInit }[] = [];
  vi.stubGlobal("fetch", async (url: string, init?: RequestInit) => {
    calls.push({ url, init });
    const request = `${init?.method ?? "GET"} ${url.replace("/api", "")}`;
    const key = Object.keys(routes).find((k) => request.startsWith(k));
    if (!key) return problem(404, { title: "Not found", detail: `no mock for ${request}` });
    const out = await routes[key]!(url, init);
    if (out instanceof Response) return out;
    return new Response(JSON.stringify(out), { status: 200, headers: { "content-type": "application/json" } });
  });
  return calls;
}

export const problem = (status: number, body: object) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/problem+json" } });

export const finding = (over: Partial<Finding> = {}): Finding => ({
  id: "fnd_1", run_id: "run_1", kind: "silent_failure", severity: "high", title: "Stated refund is wrong",
  check_id: "CHK-OUT-1", symptom_step: "s5", status: "hypothesized", verification_level: "V1",
  created_at: "2026-10-06T10:00:00Z", detail: "observed 662.0 expected 662.23",
  hypotheses: [
    { id: "hyp_1", rank: 1, step_id: "s2", agent: "Order Lookup", method: "provenance", evidence_kind: "truth_mismatch",
      score: 0.9, rationale: "price differs from the catalogue", status: "open", can_verify: true },
    { id: "hyp_2", rank: 2, step_id: "s3", agent: "Policy", method: "provenance", evidence_kind: "consistent",
      score: 0.3, rationale: "consistent with its inputs", status: "open", can_verify: false },
  ],
  experiments: [], reviews: [],
  evidence: [{ id: "ev_1", type: "check_computation", title: "Check CHK-OUT-1 computation", sha256: "a".repeat(64),
    hash_valid: true, payload: {} }],
  allowed_actions: ["verify"], ...over,
});
