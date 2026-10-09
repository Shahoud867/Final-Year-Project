import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { FindingDetail } from "../src/pages/FindingDetail";
import { finding, mockApi } from "./helpers";

afterEach(() => { vi.unstubAllGlobals(); });

describe("FindingDetail", () => {
  it("offers Verify only for hypotheses that can be replayed", async () => {
    mockApi({ "GET /findings/fnd_1": () => finding() });
    render(<FindingDetail id="fnd_1" />);
    expect(await screen.findByText("Stated refund is wrong")).toBeInTheDocument();
    expect(screen.getAllByRole("button", { name: "Verify" })).toHaveLength(1);
    expect(screen.getByText("no automatic replay")).toBeInTheDocument();
    expect(screen.getByText("hash matches")).toBeInTheDocument();
    expect(screen.queryByText("Your decision")).not.toBeInTheDocument();
  });

  it("runs a verification, shows progress and then reloads the finding", async () => {
    let loads = 0;
    const confirmed = finding({ status: "confirmed", verification_level: "V2", allowed_actions: ["accept", "reject"] });
    const calls = mockApi({
      "GET /findings/fnd_1": () => (++loads > 1 ? confirmed : finding()),
      "POST /hypotheses/hyp_1/experiments": () => ({ job_id: "job_1", experiment_id: "exp_1" }),
      "GET /jobs/job_1": () => ({ id: "job_1", status: "succeeded", progress_done: 7, progress_total: 7, message: "done" }),
    });
    const user = userEvent.setup();
    render(<FindingDetail id="fnd_1" />);
    await user.click(await screen.findByRole("button", { name: "Verify" }));
    expect(await screen.findByText("Your decision")).toBeInTheDocument();
    const post = calls.find((c) => c.init?.method === "POST");
    expect(JSON.parse(String(post?.init?.body))).toEqual({ n: 5, m: 2 });
  });

  it("requires a reason to reject before calling the server, then submits", async () => {
    const calls = mockApi({
      "GET /findings/fnd_1": () => finding({ status: "confirmed", allowed_actions: ["accept", "reject"] }),
      "POST /findings/fnd_1/reviews": () => ({ id: "rev_1" }),
    });
    const user = userEvent.setup();
    render(<FindingDetail id="fnd_1" />);
    await user.click(await screen.findByRole("button", { name: "Reject" }));
    expect(await screen.findByText("Please say why (at least 5 characters).")).toBeInTheDocument();
    expect(calls.some((c) => c.init?.method === "POST")).toBe(false);
    await user.type(screen.getByLabelText("Comment"), "price was correct");
    await user.click(screen.getByRole("button", { name: "Reject" }));
    await waitFor(() => expect(calls.some((c) => c.init?.method === "POST")).toBe(true));
  });

  it("flags tampered evidence loudly", async () => {
    const f = finding();
    f.evidence[0]!.hash_valid = false;
    mockApi({ "GET /findings/fnd_1": () => f });
    render(<FindingDetail id="fnd_1" />);
    expect(await screen.findByText("TAMPERED")).toBeInTheDocument();
  });
});
