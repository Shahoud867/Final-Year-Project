import { fetchPipeline, latestRun, passedFor } from "../src/delivery";
import type { WorkflowRun } from "../src/delivery";
import { ago, delta, duration, evidenceKind, faultLabel, finalText, modeLabel, parseTime, show } from "../src/format";
import { AWAITING_REVIEW, STAGES, TRANSITIONS, VERIFIED, countIn, reached, stage } from "../src/lib/lifecycle";
import { CONFIRM_MIN_RATE, CONTROL_MAX_RATE, decide, ruleLines, wilson } from "../src/lib/vr1";

afterEach(() => { vi.unstubAllGlobals(); sessionStorage.clear(); });

describe("rule VR-1 as the interface explains it", () => {
  it("gives the Wilson interval the server reports (values from the stored experiments)", () => {
    const round = ([lo, hi]: [number, number]) => [Number(lo.toFixed(4)), Number(hi.toFixed(4))];
    expect(round(wilson(5, 5))).toEqual([0.5655, 1]);
    expect(round(wilson(0, 5))).toEqual([0, 0.4345]);
    expect(wilson(0, 0)).toEqual([0, 1]);
  });

  it("follows the server's decision table", () => {
    expect(decide(5, 5, 0, 2)).toBe("confirmed");
    expect(decide(4, 5, 0, 2)).toBe("confirmed"); // exactly 80% with the fix
    expect(decide(5, 5, 1, 2)).toBe("inconclusive"); // the controls passed too often: luck is not ruled out
    expect(decide(3, 5, 0, 2)).toBe("inconclusive");
    expect(decide(1, 5, 0, 2)).toBe("refuted"); // exactly 20%
    expect(decide(0, 5, 2, 2)).toBe("refuted");
    expect(decide(5, 5, 0, 0)).toBe("confirmed"); // no controls requested
    expect(decide(4, 5, 0, 2, 4, 2)).toBe("error"); // a fix replay did not finish
    expect(decide(5, 5, 0, 2, 5, 1)).toBe("error"); // a control did not finish
  });

  it("evaluates each condition on the real counts", () => {
    const [fix, control, refute] = ruleLines(5, 5, 0, 2);
    expect([fix!.holds, control!.holds, refute!.holds]).toEqual([true, true, false]);
    expect(fix!.text).toContain(`${CONFIRM_MIN_RATE * 100}%`);
    expect(control!.text).toContain(`${CONTROL_MAX_RATE * 100}%`);
    expect(ruleLines(0, 5, 0, 0)[1]!.holds).toBeNull(); // no controls: nothing to evaluate
    expect(ruleLines(0, 0, 0, 0)[0]!.rate).toBeNull();
  });
});

describe("finding lifecycle helpers", () => {
  it("maps every status of the transition table to a stage", () => {
    const statuses = new Set(TRANSITIONS.flatMap(([from, , to]) => [from, to]));
    expect(statuses.size).toBe(11);
    for (const s of statuses) expect(stage(s)).toBeGreaterThanOrEqual(1);
    expect(STAGES).toHaveLength(4);
  });

  it("counts findings by group and by stage reached", () => {
    const counts = { hypothesized: 2, confirmed: 1, inconclusive: 1, accepted: 3, open: 1 };
    expect(countIn(counts, AWAITING_REVIEW)).toBe(2);
    expect(countIn(counts, VERIFIED)).toBe(4);
    expect([1, 2, 3, 4].map((n) => reached(counts, n))).toEqual([8, 7, 5, 3]);
  });

  it("returns zero for a missing or malformed summary instead of failing", () => {
    expect(countIn(null, VERIFIED)).toBe(0);
    expect(countIn([] as unknown as Record<string, number>, VERIFIED)).toBe(0);
    expect(reached(undefined, 1)).toBe(0);
  });
});

describe("format helpers for the workbench", () => {
  it("reads the server's zoneless timestamps as UTC", () => {
    expect(parseTime("2026-10-13T19:11:28.763574")?.toISOString()).toBe("2026-10-13T19:11:28.763Z");
    expect(parseTime("2026-10-13T19:11:28Z")?.toISOString()).toBe("2026-10-13T19:11:28.000Z");
    expect(parseTime("nonsense")).toBeNull();
  });

  it("formats elapsed and relative time", () => {
    expect(duration("2026-10-13T19:11:28.763574", "2026-10-13T19:11:28.986987")).toBe("223 ms");
    expect(duration("2026-10-13T19:11:00Z", "2026-10-13T19:11:03.200Z")).toBe("3.2 s");
    expect(duration("2026-10-13T19:11:00Z", "2026-10-13T19:12:05Z")).toBe("1 min 5 s");
    expect(duration(null, "2026-10-13T19:12:05Z")).toBe("");
    const now = new Date("2026-10-13T20:00:00Z");
    expect(ago("2026-10-13T19:59:40", now)).toBe("just now");
    expect(ago("2026-10-13T19:45:00", now)).toBe("15 min ago");
    expect(ago("2026-10-13T17:00:00", now)).toBe("3 h ago");
  });

  it("shows values and differences without inventing precision", () => {
    expect(show(662)).toBe("662");
    expect(show(661.98)).toBe("661.98");
    expect(show(null)).toBe("n/a");
    expect(show(true)).toBe("true");
    expect(delta(661.98, 662.23)).toBe("−0.25");
    expect(delta(662, 661.98)).toBe("+0.02");
    expect(delta(1, 1)).toBe("0");
    expect(delta("a", 1)).toBe("");
  });

  it("labels modes, faults and evidence classes", () => {
    expect(modeLabel("recorded")).toBe("Recorded cassette");
    expect(modeLabel("live")).toBe("Live model");
    expect(faultLabel("stale_price")).toBe("Stale price");
    expect(faultLabel(null)).toBe("None");
    expect(evidenceKind("truth_mismatch")).toBe("Contradicts the source of truth");
    expect(evidenceKind("something_new")).toBe("something new");
    expect(finalText({ message: "Refund $1.00" })).toBe("Refund $1.00");
    expect(finalText(null)).toBe("");
  });
});

describe("delivery evidence", () => {
  const run = (over: Partial<WorkflowRun>): WorkflowRun => ({
    id: 1, name: "CI", run_number: 13, status: "completed", conclusion: "success", head_branch: "main", head_sha: "336ca55aaaaaaaaa",
    event: "push", created_at: "2026-10-13T17:11:19Z", html_url: "https://github.com/x/y/actions/runs/1", ...over,
  });

  it("picks the latest completed run of a workflow and ignores skipped ones", () => {
    const runs = [run({ name: "CD", run_number: 4, conclusion: "skipped" }), run({ name: "CD", run_number: 3, conclusion: "success" }), run({})];
    expect(latestRun(runs, "CD")?.run_number).toBe(3);
    expect(latestRun(runs, "CI")?.run_number).toBe(13);
    expect(latestRun(runs, "CI", "v0.1.0")).toBeNull();
  });

  it("confirms a commit only when a successful run for exactly that commit is listed", () => {
    const runs = [run({}), run({ run_number: 12, head_sha: "37e7b6d000", conclusion: "failure" })];
    expect(passedFor(runs, "CI", "336ca55")?.run_number).toBe(13);
    expect(passedFor(runs, "CI", "37e7b6d")).toBeNull();
    expect(passedFor(runs, "CI", "")).toBeNull();
  });

  it("reads runs from GitHub without credentials, then serves the next call from the session cache", async () => {
    const spy = vi.fn<(url: string, init?: RequestInit) => Promise<Response>>(async () =>
      new Response(JSON.stringify({ workflow_runs: [run({})] }), { status: 200, headers: { "content-type": "application/json" } }));
    vi.stubGlobal("fetch", spy);
    const first = await fetchPipeline("x/y");
    expect(first.runs[0]?.run_number).toBe(13);
    const [url, init] = spy.mock.calls[0]!;
    expect(url).toBe("https://api.github.com/repos/x/y/actions/runs?per_page=30");
    expect(JSON.stringify(init?.headers ?? {})).not.toContain("Authorization");
    await fetchPipeline("x/y");
    expect(spy).toHaveBeenCalledTimes(1);
    await fetchPipeline("x/y", true);
    expect(spy).toHaveBeenCalledTimes(2);
  });

  it("says the status is unknown when GitHub cannot be reached or limits the caller", async () => {
    vi.stubGlobal("fetch", () => Promise.reject(new TypeError("Failed to fetch")));
    await expect(fetchPipeline("x/y", true)).rejects.toThrow(/status is unknown/);
    vi.stubGlobal("fetch", async () => new Response("{}", { status: 403 }));
    await expect(fetchPipeline("x/y", true)).rejects.toThrow(/request limit/);
  });
});
