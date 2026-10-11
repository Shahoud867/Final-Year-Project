"""Behaviour design: finding state machine (from the code), investigation flow, interaction overview."""

from __future__ import annotations

from granite_core.lifecycle import TERMINAL, TRANSITIONS, Event, FindingStatus, verification_level

from . import Sheet
from .kit import Diagram

S, E = FindingStatus, Event
REVIEWABLE = (S.CONFIRMED, S.INCONCLUSIVE, S.EVIDENCE_SUPPORTED)

# Where each transition is drawn. The set of keys must equal the transitions in the code, apart from the two
# review events, which are drawn once on the composite state "awaiting review".
_ROUTES: dict[tuple[FindingStatus, Event], dict] = {
    (S.OPEN, E.HYPOTHESES_READY): {"pts": [(210, 275), (340, 275)], "at": (275, 268)},
    (S.HYPOTHESIZED, E.VERIFY_STARTED): {"pts": [(490, 265), (640, 265)], "at": (565, 258)},
    (S.VERIFYING, E.VERIFY_ERROR): {"pts": [(640, 287), (490, 287)], "at": (565, 303)},
    (S.VERIFYING, E.VERDICT_INCONCLUSIVE): {"pts": [(770, 265), (920, 265)], "at": (845, 258)},
    (S.INCONCLUSIVE, E.VERIFY_STARTED): {"pts": [(920, 287), (770, 287)], "at": (845, 303)},
    (S.VERIFYING, E.VERDICT_CONFIRMED): {"pts": [(705, 250), (705, 115), (920, 115)], "at": (812, 108)},
    (S.VERIFYING, E.VERDICT_REFUTED): {"pts": [(685, 300), (685, 410)], "at": (677, 360), "anchor": "end"},
    (S.REFUTED, E.VERIFY_STARTED): {"pts": [(725, 410), (725, 300)], "at": (733, 360), "anchor": "start"},
    (S.HYPOTHESIZED, E.EVIDENCE_SUPPORTED): {"pts": [(415, 300), (415, 560), (995, 560), (995, 460)], "at": (700, 553)},
    (S.ACCEPTED, E.RESOLVE): {"pts": [(1245, 150), (1245, 115), (1400, 115)], "at": (1322, 108)},
    (S.ACCEPTED, E.WONT_FIX): {"pts": [(1310, 175), (1355, 175), (1355, 235), (1400, 235)], "at": (1363, 200), "anchor": "start"},
}
_POS: dict[FindingStatus, tuple[int, int, int]] = {
    S.OPEN: (90, 250, 120), S.HYPOTHESIZED: (340, 250, 150), S.VERIFYING: (640, 250, 130), S.REFUTED: (640, 410, 130),
    S.CONFIRMED: (920, 90, 150), S.INCONCLUSIVE: (920, 250, 150), S.EVIDENCE_SUPPORTED: (920, 410, 150),
    S.ACCEPTED: (1180, 150, 130), S.REJECTED: (1180, 370, 130), S.RESOLVED: (1400, 90, 120), S.WONT_FIX: (1400, 210, 120),
}
_KIND = {S.CONFIRMED: "ok", S.ACCEPTED: "ok", S.RESOLVED: "ok", S.REFUTED: "bad", S.REJECTED: "bad",
         S.INCONCLUSIVE: "warn", S.WONT_FIX: "warn"}


def state_machine() -> Sheet:
    review = {(s, e) for s in REVIEWABLE for e in (E.REVIEW_ACCEPT, E.REVIEW_REJECT)}
    in_code = set(TRANSITIONS)
    if not review <= in_code:
        raise SystemExit("state machine drawing is out of date: a reviewable state lost a review transition")
    if in_code - review != set(_ROUTES):
        raise SystemExit(f"state machine drawing is out of date: {sorted(str(k) for k in (in_code - review) ^ set(_ROUTES))}")
    for (src, ev), spec in _ROUTES.items():
        spec["dst"] = TRANSITIONS[(src, ev)]
    if TERMINAL != {S.REJECTED, S.RESOLVED, S.WONT_FIX} or set(_POS) != set(FindingStatus):
        raise SystemExit("state machine drawing is out of date: states changed")

    d = Diagram("finding-state-machine", "Finding state machine", 1600, 620,
                "Every status a finding can have and the only events that may change it.")
    d.frame("review", 900, 52, 190, 444, "awaiting review", "plain", dashed=True)
    for st, (x, y, w) in _POS.items():
        d.node(st.value, x, y, w, 50, st.value.replace("_", " "), [f"level {verification_level(st)}"],
               _KIND.get(st, "core"), tip=f"FindingStatus.{st.name}")
    d.terminal("start", 45, 275)
    d.edge([(52, 275), (90, 275)], src="start", dst=S.OPEN.value)
    for (src, ev), spec in _ROUTES.items():
        d.edge(spec["pts"], ev.value, src.value, spec["dst"].value, label_at=spec["at"],
               label_anchor=spec.get("anchor", "middle"), tip=f"{src.value} --{ev.value}--> {spec['dst'].value}")
    d.edge([(1090, 175), (1180, 175)], E.REVIEW_ACCEPT.value, "review", S.ACCEPTED.value, label_at=(1135, 168))
    d.edge([(1090, 395), (1180, 395)], E.REVIEW_REJECT.value, "review", S.REJECTED.value, label_at=(1135, 388))
    for st, (x, y) in ((S.REJECTED, (1372, 395)), (S.RESOLVED, (1565, 115)), (S.WONT_FIX, (1565, 235))):
        px, py, pw = _POS[st]
        d.terminal(f"end-{st.value}", x, y, final=True)
        d.edge([(px + pw, y), (x - 9, y)], src=st.value, dst=f"end-{st.value}")
    d.note(60, 420, 300, ["How to read it", "Labels are the events in granite_core.lifecycle.",
                          "An event not drawn from a state is refused:", "transition() raises, the API answers 409",
                          "and lists the allowed actions."], "plain", id="read")
    d.note(1150, 470, 400, ["Composite state", "review_accept and review_reject leave from each of",
                            "the three states inside 'awaiting review'.",
                            "request_info is recorded without changing the state."], "plain", id="composite")
    return Sheet(
        d, "Behaviour", "Network Automata / Graphs or State Machine",
        "A finding moves through eleven states and nothing can skip a step: it cannot be accepted before it was "
        "verified or supported by evidence, and it cannot be resolved before a person accepted it. Verification "
        "can end three ways; a refuted or inconclusive result leads back to verifying (the next hypothesis, or "
        "more replays), and a technical failure returns to 'hypothesized' instead of inventing a verdict. The "
        "level under each state (V0 to V3) is computed from the state. Reaching 'evidence supported' happens "
        "automatically when the first-ranked step has strong provenance evidence but no replay is defined for it.",
        ["packages/granite_core/granite_core/lifecycle.py", "apps/api/granite_api/services/common.py",
         "apps/api/granite_api/services/reviews.py", "packages/granite_core/tests/test_lifecycle_evidence_redaction_llm.py"],
        "States, events, targets and levels are read from granite_core.lifecycle when the pack is built. If a "
        "transition is added or removed in the code, the build fails until the drawing is updated.",
    )


def investigation_flow() -> Sheet:
    d = Diagram("investigation-flow", "Investigation flow", 1180, 1650,
                "Flowchart of one investigation from the submitted task to the report, with every decision point.")
    px, pw, dx, dw = 430, 320, 460, 260  # process and decision geometry on the spine
    cx = px + pw / 2

    def proc(id: str, y: float, title: str, lines: list[str], kind: str = "api", h: float = 56):
        return d.node(id, px, y, pw, h, title, lines, kind)

    def dec(id: str, y: float, title: str):
        return d.node(id, dx, y, dw, 74, title, [], "plain", shape="diamond")

    def down(a, b, label: str = ""):
        d.edge([a.bottom(), b.top()], src=a.id, dst=b.id)
        if label:
            d.label(cx + 10, (a.y + a.h + b.y) / 2 + 4, label, anchor="start")

    n0 = d.node("start", px - 20, 40, pw + 40, 44, "Analyst submits a task (optionally with a fault)", [], "actor", shape="pill")
    n1 = proc("validate", 124, "Validate the task input", ["message, e-mail, order id; no unknown keys"])
    d1 = dec("d-valid", 220, "Input valid?")
    e1 = d.node("rejected-input", 60, 232, 280, 50, "Refused with field errors", ["HTTP 422; nothing is stored"], "bad")
    n2 = proc("run", 334, "Run the five workflow steps", ["record inputs, outputs and declared reads"], "core")
    d2 = dec("d-run", 430, "Run completed?")
    x1 = d.node("explicit", 860, 442, 290, 50, "Open finding: explicit error", ["the run stopped at a step"], "bad")
    n3 = proc("checks", 544, "Evaluate the checks", ["2 outcome checks, 5 step contracts"], "core")
    d3 = dec("d-fail", 640, "Outcome check failed?")
    c1 = d.node("clean", 60, 652, 280, 50, "Clean run: no finding", ["nothing to investigate"], "ok")
    n4 = proc("finding", 754, "Open finding: silent failure", ["detected, not yet explained · level V0"], "warn")
    n5 = proc("rank", 850, "Rank where it began", ["provenance first, structure as fallback · V1"], "core")
    d4 = dec("d-repair", 946, "Replay defined for the step?")
    ev = d.node("supported", 60, 958, 280, 50, "Evidence-supported", ["no automatic replay; judge the evidence"], "warn")
    n6 = proc("replay", 1060, "Replay N times with the fix, M without", ["controls show it was the fix, not luck"], "core")
    d5 = dec("d-verdict", 1156, "Origin confirmed?")
    lp = d.node("next", 900, 1168, 250, 50, "Try the next hypothesis", ["or run more replays"], "plain")
    n7 = proc("review", 1270, "Human review", ["accept · reject · ask for more information"], "actor")
    d6 = dec("d-accept", 1366, "Accepted?")
    rj = d.node("rejected", 60, 1378, 280, 50, "Rejected: closed with a reason", ["comment is mandatory"], "bad")
    n8 = proc("resolve", 1480, "Resolve, or close without fixing", ["confirmed by a person · level V3"], "ok")
    n9 = d.node("report", px - 20, 1576, pw + 40, 44, "Report with hashed evidence (Markdown, JSON)", [], "actor", shape="pill")

    down(n0, n1)
    down(n1, d1)
    down(d1, n2, "yes")
    d.edge([d1.left(), e1.right()], "no", d1.id, e1.id, label_dy=-7)
    down(n2, d2)
    down(d2, n3, "yes")
    d.edge([d2.right(), x1.left()], "no", d2.id, x1.id, label_dy=-7)
    down(n3, d3)
    down(d3, n4, "yes")
    d.edge([d3.left(), c1.right()], "no", d3.id, c1.id, label_dy=-7)
    down(n4, n5)
    d.edge([x1.bottom(0.31), (x1.x + x1.w * 0.31, n5.y + 18), (px + pw, n5.y + 18)], src=x1.id, dst=n5.id)
    down(n5, d4)
    down(d4, n6, "yes")
    d.edge([d4.left(), ev.right()], "no", d4.id, ev.id, label_dy=-7)
    down(n6, d5)
    down(d5, n7, "confirmed · V2")
    d.edge([d5.right(), lp.left()], "refuted · inconclusive · error", d5.id, lp.id, label_dy=-7)
    d.edge([lp.top(0.76), (lp.x + lp.w * 0.76, n5.y + 42), (px + pw, n5.y + 42)], src=lp.id, dst=n5.id)
    d.edge([ev.bottom(), (ev.cx, n7.cy), n7.left()], src=ev.id, dst=n7.id)
    down(n7, d6)
    down(d6, n8, "yes")
    d.edge([d6.left(), rj.right()], "no", d6.id, rj.id, label_dy=-7)
    down(n8, n9)
    d.legend(860, 40, [("api", "application step"), ("core", "granite_core step"), ("actor", "person"),
                       ("warn", "open question"), ("bad", "failure outcome"), ("ok", "good outcome")], col_w=250)
    return Sheet(
        d, "Behaviour", "Flow Diagram",
        "The flowchart is the product's one workflow, the answer to the panel's request to redefine it. It has "
        "six decision points and each one has a visible outcome in the UI. Two findings are possible: an explicit "
        "error (the run stopped) and a silent failure (the run finished but an outcome check failed). Ranking "
        "comes before proof, and proof is optional only when no replay is defined for the suspected step, in "
        "which case the finding is marked evidence-supported and a person judges it. A refuted or inconclusive "
        "result loops back to the ranked list rather than ending the investigation.",
        ["apps/api/granite_api/services/runs.py", "apps/api/granite_api/services/analysis.py",
         "apps/api/granite_api/services/experiments.py", "apps/api/granite_api/services/reviews.py",
         "packages/granite_core/granite_core/checks.py"],
        "Curated. The statuses it names are the states of the generated state machine.",
    )


def interaction_overview() -> Sheet:
    d = Diagram("interaction-overview", "Interaction overview diagram", 1560, 470,
                "How the three interactions (run, verify, review) follow one another, with the decisions between them.")
    d.terminal("start", 50, 170)
    r1 = d.ref("io-run", 100, 120, 240, 100, "sd Run and analyse", ["sequence diagram: run-sequence", "POST /api/runs to a finding"], "api")
    q1 = d.node("io-q1", 410, 133, 190, 74, "Finding opened?", [], "plain", shape="diamond")
    r2 = d.ref("io-verify", 670, 120, 240, 100, "sd Verify a hypothesis", ["sequence diagram: verification-sequence", "N replays, M controls, verdict"], "core")
    q2 = d.node("io-q2", 980, 133, 190, 74, "Origin confirmed?", [], "plain", shape="diamond")
    r3 = d.ref("io-review", 1240, 120, 240, 100, "sd Review and record", ["accept, reject or ask;", "audit entry and report"], "actor")
    d.terminal("end", 1530, 170, final=True)
    d.terminal("end-clean", 505, 300, final=True)
    d.edge([(57, 170), r1.left()], src="start", dst=r1.id)
    d.edge([r1.right(), q1.left()], src=r1.id, dst=q1.id)
    d.edge([q1.right(), r2.left()], "yes", q1.id, r2.id, label_dy=-7)
    d.edge([q1.bottom(), (505, 291)], src=q1.id, dst="end-clean")
    d.label(517, 255, "no: clean run", anchor="start")
    d.edge([r2.right(), q2.left()], src=r2.id, dst=q2.id)
    d.edge([q2.right(), r3.left()], "yes", q2.id, r3.id, label_dy=-7)
    d.edge([q2.bottom(), (1075, 290), (790, 290), r2.bottom()], "no: next hypothesis, or more replays", q2.id, r2.id,
           label_at=(932, 284))
    d.edge([r3.right(), (1521, 170)], src=r3.id, dst="end")
    d.edge([r2.top(0.3), (r2.x + r2.w * 0.3, 60), (r3.cx, 60), r3.top()], "no replay is defined for the step: review on the evidence",
           r2.id, r3.id, label_at=(1050, 54), dashed=True)
    d.note(100, 340, 380, ["Reading the diagram", "Each 'ref' box stands for a whole interaction that has its own",
                           "sequence diagram in this pack. Diamonds are decisions",
                           "taken from stored state, not from the user's memory."], "plain", id="read")
    return Sheet(
        d, "Behaviour", "Interaction Overview Diagram",
        "An investigation is three conversations between the analyst and the system, and this diagram shows their "
        "order. The first always happens. The second happens only if a finding was opened, and may repeat: each "
        "pass verifies one hypothesis. The third needs either a confirmed origin or, when the workflow defines no "
        "replay for the suspected step, the evidence alone. Because the decisions are stored states, the analyst "
        "can stop after any box and continue another day.",
        ["apps/api/granite_api/routes.py", "packages/granite_core/granite_core/lifecycle.py"],
        "Curated; each 'ref' names a sequence diagram of this pack.",
    )
