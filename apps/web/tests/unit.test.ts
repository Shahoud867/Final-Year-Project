import { ApiError, getToken, request, setToken, waitForJob } from "../src/api";
import { label, pct, short, when } from "../src/format";
import { stage } from "../src/pages/FindingDetail";

function respond(status: number, body: unknown, type = "application/json") {
  return Promise.resolve(new Response(typeof body === "string" ? body : JSON.stringify(body), { status, headers: { "content-type": type } }));
}

afterEach(() => { vi.unstubAllGlobals(); localStorage.clear(); });

async function failure(p: Promise<unknown>): Promise<ApiError> {
  try { await p; } catch (e) { return e as ApiError; }
  throw new Error("expected the request to fail");
}

describe("api client", () => {
  it("turns a 422 problem body into per-field messages", async () => {
    vi.stubGlobal("fetch", () => respond(422, { title: "Invalid request", detail: "bad", errors: [{ field: "email", message: "must look like name@example.com" }] }));
    const err = await failure(request("/runs"));
    expect(err).toBeInstanceOf(ApiError);
    expect(err.status).toBe(422);
    expect(err.fields).toEqual({ email: "must look like name@example.com" });
  });

  it("keeps allowed actions from a 409", async () => {
    vi.stubGlobal("fetch", () => respond(409, { title: "Action not allowed", detail: "no", allowed_actions: ["verify_started"] }));
    const err = await failure(request("/x"));
    expect(err.allowedActions).toEqual(["verify_started"]);
  });

  it("explains an unreachable server in plain words", async () => {
    vi.stubGlobal("fetch", () => Promise.reject(new TypeError("Failed to fetch")));
    await expect(request("/health")).rejects.toThrow("Cannot reach the Granite server");
  });

  it("falls back to a generic message when the error body is not JSON", async () => {
    vi.stubGlobal("fetch", () => respond(502, "<html>bad gateway</html>", "text/html"));
    await expect(request("/health")).rejects.toThrow("Request failed (502)");
  });

  it("sends the bearer token when one is stored", async () => {
    setToken("abc");
    const spy = vi.fn(() => respond(200, { ok: true }));
    vi.stubGlobal("fetch", spy);
    await request("/health");
    const init = (spy.mock.calls[0] as unknown as [string, RequestInit])[1];
    expect((init.headers as Record<string, string>).Authorization).toBe("Bearer abc");
    setToken("");
    expect(getToken()).toBe("");
  });

  it("polls a job until it has finished and reports progress", async () => {
    const states = [
      { id: "j", status: "running", progress_done: 1, progress_total: 3, message: "a" },
      { id: "j", status: "succeeded", progress_done: 3, progress_total: 3, message: "b" },
    ];
    vi.stubGlobal("fetch", () => respond(200, states.shift()));
    const seen: number[] = [];
    const job = await waitForJob("j", (j) => seen.push(j.progress_done), 1);
    expect(job.status).toBe("succeeded");
    expect(seen).toEqual([1, 3]);
  });
});

describe("format helpers", () => {
  it("labels statuses for people", () => {
    expect(label("evidence_supported")).toBe("Evidence-supported");
    expect(label("some_new_status")).toBe("some new status");
  });
  it("shortens long text and values", () => {
    expect(short("x".repeat(100), 10)).toHaveLength(10);
    expect(short({ a: 1 })).toBe('{"a":1}');
  });
  it("formats dates and percentages safely", () => {
    expect(when(null)).toBe("");
    expect(when("not a date")).toBe("");
    expect(pct(0.566)).toBe("57%");
  });
  it("maps finding status to the stepper stage", () => {
    expect(["open", "hypothesized", "confirmed", "accepted"].map(stage)).toEqual([1, 2, 3, 4]);
  });
});
