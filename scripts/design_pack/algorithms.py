"""Data structure and algorithm design: check pipeline, attribution, the VR-1 verdict rule and the replay plan.

Constants, thresholds, the verdict table and the worked examples are computed from the code and from the recorded
run in data/cassettes, so the drawings cannot drift from the implementation.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from granite_core import attribution as att
from granite_core import dsl
from granite_core import verification as ver
from granite_core.checks import evaluate_checks
from granite_core.experiment import run_experiment
from granite_core.llm import Cassette, RecordedProvider
from granite_core.runner import run_workflow
from refund_desk import CHECKS, build_workflow, default_store, make_fault

from . import Sheet
from .kit import INK, KINDS, Diagram, esc

ROOT = Path(__file__).resolve().parents[2]
CASSETTE = ROOT / "data" / "cassettes" / "refund_desk_v1.json"
V_KIND = {ver.Verdict.CONFIRMED: "ok", ver.Verdict.REFUTED: "bad", ver.Verdict.INCONCLUSIVE: "warn", ver.Verdict.ERROR: "plain"}


@lru_cache(maxsize=1)
def recorded_case() -> dict[str, Any]:
    """The first example task run with the stale-price fault, replayed from recorded model answers."""
    store = default_store()
    defn = build_workflow(store)
    task = next(t for t in store.example_tasks(12) if "(delivered)" in t["label"])
    llm = RecordedProvider(Cassette(CASSETTE))
    out = run_workflow(defn, {k: task[k] for k in ("message", "email", "order_id")}, llm, fault=make_fault("stale_price"), seed=1)
    if out.trace.run.status != "completed":
        raise SystemExit("design pack: the recorded example no longer replays; re-record the cassette")
    results = evaluate_checks(out.trace, defn.checks, defn.truth())
    failing = [r for r in results if r.scope == "outcome" and r.status.value == "fail"]
    hyps = att.attribute(out.trace, results, failing[0].step)
    exp = run_experiment(defn, out.trace, out.fault.target_step, llm, 5, 2, [r.check_id for r in failing])
    return {"defn": defn, "task": task, "out": out, "results": results, "failing": failing, "hyps": hyps, "exp": exp}


def check_pipeline() -> Sheet:
    d = Diagram("check-pipeline", "Check language: from text to result", 1440, 520,
                "How a check expression is validated once and then evaluated safely on any trace.")
    y, h = 110, 70
    n = [
        d.node("src", 30, y, 190, h, "Check expression", ["plain text, written", "by a workflow author"], "workflow"),
        d.node("parse", 270, y, 170, h, "Parse", ["ast.parse, mode 'eval'", "(never executed)"], "core"),
        d.node("validate", 490, y, 220, h, "Validate against whitelist", ["node types, names, limits;", "anything else is refused"], "core"),
        d.node("expr", 760, y, 170, h, "Expression", ["compiled once,", "lists its references"], "core"),
        d.node("eval", 980, y, 200, h, "Evaluate on a trace", ["context: task + step outputs", "truth functions, tolerance"], "core"),
        d.node("res", 1230, y, 180, h, "CheckResult", ["status, observed, expected,", "computation (for evidence)"], "core"),
    ]
    for a, b in zip(n, n[1:], strict=False):
        d.edge([a.right(), b.left()], src=a.id, dst=b.id)
    rej = d.node("rejected", 490, 250, 220, 56, "Refused when the check is saved", ["DSLSyntaxError names the construct"], "bad")
    d.edge([n[2].bottom(), rej.top()], src="validate", dst="rejected")
    outcomes = [("PASS", "expression is true", "ok"), ("FAIL", "expression is false", "bad"),
                ("ABSTAIN", "a field is missing", "warn"), ("ERROR", "it cannot be evaluated", "plain")]
    for i, (name, why, kind) in enumerate(outcomes):
        o = d.node(f"o-{name}", 830 + i * 150, 250, 138, 56, name, [why], kind)
        d.edge([(n[4].cx, y + h), (n[4].cx, 222), (o.cx, 222), o.top()], src="eval", dst=o.id)
    example = next(c for c in CHECKS if c.id == "CHK-OUT-1")
    d.label(30, 60, f"Example ({example.id}):", anchor="start", weight=700, color=INK, size=11.5, check=False)
    d.label(150, 60, example.expression, anchor="start", mono=True, color=INK, size=11, check=False)
    funcs = ", ".join(sorted(dsl.FUNCTION_NAMES)) + ", truth.<name>()"
    d.note(30, 250, 420, ["Limits (from granite_core.dsl)", f"source at most {dsl.MAX_SOURCE_LEN} characters, {dsl.MAX_NODES} syntax nodes,",
                          f"nesting depth {dsl.MAX_DEPTH}; strings up to {dsl.MAX_STRING_LEN} characters",
                          "Allowed: arithmetic, comparison, and/or/not,", "field paths such as s3.items_to_refund, and the functions",
                          funcs[:62], funcs[62:]], "plain", id="limits")
    d.note(30, 400, 800, ["Why not eval()", "A check is text typed by a user and run on data the system did not write. Python's eval would let it read files or run",
                          "commands. Here the text is only parsed; a small interpreter walks the tree and understands nothing but the whitelist.",
                          "25 hostile expressions (attribute access, imports, lambdas, comprehensions, f-strings, **) are rejected in the tests."],
           "warn", id="why")
    d.note(870, 400, 540, ["A missing field is not a pass", "If a step did not produce the field a check needs, the result is ABSTAIN,",
                           "so an incomplete run can never look correct (requirement FR-CHK-03)."], "plain", id="abstain")
    return Sheet(
        d, "Algorithms", "Data Structure and Algorithm Design",
        "The check language is the first of Granite's three core algorithms. A check is stored as text and turned "
        "into a syntax tree once; a validator walks the tree and accepts only whitelisted node types, a fixed set "
        "of function names and bounded sizes. Evaluation is a recursive interpreter over that tree with two "
        "inputs: the context (the task and every step's outputs) and the workflow's source-of-truth functions. "
        "Every operand, resolved field and truth call is kept in the result, which is why a failed check can be "
        "shown and re-computed as evidence. Complexity is linear in the number of syntax nodes (at most 150).",
        ["packages/granite_core/granite_core/dsl.py", "packages/granite_core/granite_core/checks.py",
         "packages/granite_core/tests/test_dsl.py", "docs/adr/adr-004-ast-check-dsl.md"],
        "Limits, the function list and the example expression are read from the code when the pack is built.",
    )


def attribution_algorithm() -> Sheet:
    case = recorded_case()
    d = Diagram("attribution-algorithm", "Attribution: ranking where a failure began", 1320, 800,
                "The provenance-first ranking algorithm with its weights and a worked example from a recorded run.")
    x, w = 50, 440
    a0 = d.node("in", x + 30, 50, w - 60, 44, "Input: trace, check results, symptom step", [], "actor", shape="pill")
    a1 = d.node("walk", x, 134, w, 70, "1  Walk the recorded reads backwards",
                ["breadth-first from the symptom step; hop distance per ancestor", "(a revisit bound of 3 keeps an imported cyclic trace finite)"], "core")
    a2 = d.node("classify", x, 244, w, 70, "2  Classify each ancestor by its strongest evidence",
                ["from that step's own checks: truth mismatch, contract failure,", "handoff drift, nothing known, or consistent"], "core")
    a3 = d.node("score", x, 354, w, 56, f"3  Score = evidence weight × {att.DECAY} ^ hops", ["closer steps win ties; scores are not probabilities"], "core")
    dq = d.node("q", x + 70, 450, w - 140, 78, f"Any step with weight ≥ {att.ORIGIN_THRESHOLD}?", [], "plain", shape="diamond")
    p1 = d.node("prov", x, 590, 205, 70, "Provenance ranking", ["sort by score;", "method = provenance"], "ok")
    p2 = d.node("struct", x + 235, 590, 205, 70, "Structural fallback", ["position on paths to the", "symptom, cleared steps last"], "warn")
    a5 = d.node("out", x + 30, 716, w - 60, 50, f"Keep the best {att.MAX_HYPOTHESES} as hypotheses", ["each with a rationale and its evidence"], "core")
    for a, b in ((a0, a1), (a1, a2), (a2, a3), (a3, dq)):
        d.edge([a.bottom(), b.top()], src=a.id, dst=b.id)
    d.edge([dq.bottom(), (dq.cx, 558), (p1.cx, 558), p1.top()], "yes", "q", "prov", label_at=((dq.cx + p1.cx) / 2, 552))
    d.edge([dq.bottom(), (dq.cx, 558), (p2.cx, 558), p2.top()], "no", "q", "struct", label_at=((dq.cx + p2.cx) / 2, 552))
    d.edge([p1.bottom(), (p1.cx, 690), (a5.x + 80, 690), (a5.x + 80, a5.y)], src="prov", dst="out")
    d.edge([p2.bottom(), (p2.cx, 690), (a5.x + a5.w - 80, 690), (a5.x + a5.w - 80, a5.y)], src="struct", dst="out")
    origin = "  origin evidence"
    rows = [f"{name:<16}{weight:>4.1f}{origin if weight >= att.ORIGIN_THRESHOLD else ''}"
            for name, weight in sorted(att.WEIGHTS.items(), key=lambda kv: -kv[1])]
    d.compartments("weights", 570, 50, 330, "Evidence weights", rows, "core",
                   footer=[f"origin threshold {att.ORIGIN_THRESHOLD} · decay {att.DECAY}/hop", f"at most {att.MAX_HYPOTHESES} hypotheses"],
                   tip="granite_core.attribution.WEIGHTS")
    d.note(940, 50, 340, ["What the evidence kinds mean", "truth_mismatch: the step's output contradicts the", "  source of truth",
                          "contract_fail: the step broke its own contract", "handoff_drift: it received something other than", "  what was produced upstream",
                          "unknown: no check covers the step", "consistent: its checks passed"], "plain", id="kinds")
    task = case["task"]
    ex_rows = [f"{h.rank} {h.agent:<18}{h.evidence_kind:<15}{h.score:>5.2f}" for h in case["hyps"]]
    d.compartments("example", 570, 300, 420, "Worked example (recorded run)", ex_rows, "workflow",
                   footer=[f"task {task['order_id']}, fault stale_price", f"symptom at {case['failing'][0].step}: {case['failing'][0].check_id} failed"],
                   tip="computed by attribute() on the recorded run when the pack is built")
    fault = case["out"].fault
    top = case["hyps"][0]
    verdict = "matches" if top.step_id == fault.target_step else "DOES NOT match"
    d.note(570, 530, 420, ["Checked against ground truth", f"The fault was injected at {fault.target_step} ({fault.field_path}:",
                           f"{fault.original_value} became {fault.injected_value}). Rank 1 is {top.step_id}: it {verdict}.",
                           "attribute() never receives the fault record."], "ok" if verdict == "matches" else "bad", id="truth")
    d.note(1030, 300, 250, ["Limits", "A step with no check can only be", "'unknown' (0.2). Weights are design", "choices, fixed before the feasibility",
                            "run; they were not tuned on its", "results. Cost: one backward walk,", "linear in steps plus reads."], "warn", id="limits")
    return Sheet(
        d, "Algorithms", "Data Structure and Algorithm Design",
        "Attribution answers 'where did the wrong value first appear'. It uses two data structures: the lineage "
        "graph (steps as nodes, declared reads as edges, stored inside each trace) and the list of check results. "
        "It walks the graph backwards from the step where the symptom showed, labels every ancestor with the "
        "strongest evidence its own checks provide, and scores by weight and distance. Only if no ancestor "
        "carries origin-grade evidence does it fall back to graph position. The worked example on the right is "
        "not illustrative: it is the output of attribute() on a recorded run, recomputed at build time and "
        "compared with the injected fault.",
        ["packages/granite_core/granite_core/attribution.py", "packages/granite_core/granite_core/lineage.py",
         "packages/granite_core/tests/test_attribution.py", "docs/adr/adr-005-provenance-first-attribution.md",
         "data/cassettes/refund_desk_v1.json"],
        "Weights, threshold, decay and the hypothesis limit are read from the module; the worked example and its "
        "comparison with ground truth are computed from the recorded run.",
    )


def _raw(d: Diagram, svg: str) -> None:
    d._back.append(svg)


def vr1_decision() -> Sheet:
    n_rep, m_ctl = 5, 2
    d = Diagram("vr1-decision", "Verdict rule VR-1", 1280, 600,
                "The fixed rule that turns replay results into a verdict, with every outcome for N=5, M=2.")
    ox, oy, pw, ph = 100, 110, 380, 300

    def px(p: float) -> float:
        return ox + pw * p

    def py(q: float) -> float:
        return oy + ph - ph * q

    for kind, x0, y0, x1, y1 in (("warn", px(ver.REFUTE_MAX_RATE), oy, px(1), py(0)),
                                 ("bad", px(0), oy, px(ver.REFUTE_MAX_RATE), py(0)),
                                 ("ok", px(ver.CONFIRM_MIN_RATE), py(ver.CONTROL_MAX_RATE), px(1), py(0))):
        fill, stroke = KINDS[kind]
        _raw(d, f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
    _raw(d, f'<path d="M{ox} {oy} V{oy + ph} H{ox + pw}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    for i in range(6):
        p = i / 5
        _raw(d, f'<path d="M{px(p):.1f} {oy + ph} v6" stroke="{INK}" stroke-width="1.2"/>')
        d.label(px(p), oy + ph + 20, f"{p:.1f}", size=10.5, check=False)
    for q in (0.0, 0.5, 1.0):
        _raw(d, f'<path d="M{ox} {py(q):.1f} h-6" stroke="{INK}" stroke-width="1.2"/>')
        d.label(ox - 10, py(q) + 4, f"{q:.1f}", size=10.5, anchor="end", check=False)
    d.label(ox + pw / 2, oy + ph + 42, "share of replays that pass with the fix  (k / N)", size=11.5, color=INK, check=False)
    d.label(ox - 44, oy - 14, "share of controls that pass  (c / M)", size=11.5, color=INK, anchor="start", check=False)
    d.label(px(0.1), py(0.6), "REFUTED", size=11, weight=700, color=KINDS["bad"][1], check=False)
    d.label(px(0.55), py(0.62), "INCONCLUSIVE", size=11, weight=700, color=KINDS["warn"][1], check=False)
    d.label(px(1) + 10, py(0.1) + 4, "CONFIRMED", size=11, weight=700, color=KINDS["ok"][1], anchor="start", check=False)
    for k in range(n_rep + 1):
        for c in range(m_ctl + 1):
            v = ver.decide(k, n_rep, c, m_ctl)
            _raw(d, f'<circle cx="{px(k / n_rep):.1f}" cy="{py(c / m_ctl):.1f}" r="5.5" fill="{KINDS[V_KIND[v]][1]}" stroke="#ffffff" stroke-width="1.5">'
                    f"<title>k={k} of {n_rep}, c={c} of {m_ctl}: {esc(v.value)}</title></circle>")
    d.label(ox, oy + ph + 66, f"Dots: every possible outcome for N = {n_rep} replays and M = {m_ctl} controls, coloured by decide().", size=10.8,
            anchor="start", check=False)
    # ordered rule
    rx, rw = 620, 620
    r1 = d.node("r1", rx, 60, rw, 54, "1   Did every replay and every control finish?", ["no: ERROR, no verdict is given; the finding returns to 'hypothesized'"], "plain")
    r2 = d.node("r2", rx, 140, rw, 54, f"2   k/N ≥ {ver.CONFIRM_MIN_RATE}  and  c/M ≤ {ver.CONTROL_MAX_RATE} ?", ["yes: CONFIRMED, the fix (not luck) changed the outcome"], "ok")
    r3 = d.node("r3", rx, 220, rw, 54, f"3   k/N ≤ {ver.REFUTE_MAX_RATE} ?", ["yes: REFUTED, fixing this step changes nothing, so it is not the origin"], "bad")
    r4 = d.node("r4", rx, 300, rw, 54, "4   otherwise", ["INCONCLUSIVE: run more replays, or review with a written reason"], "warn")
    for a, b in ((r1, r2), (r2, r3), (r3, r4)):
        d.edge([a.bottom(0.08), b.top(0.08)], src=a.id, dst=b.id)
    # verdict table computed from the code
    tx, ty, cw, ch = 760, 412, 74, 26
    d.label(rx, ty - 12, f"decide(k, {n_rep}, c, {m_ctl}) for every k and c:", size=11.5, weight=700, color=INK, anchor="start", check=False)
    for k in range(n_rep + 1):
        d.label(tx + k * cw + cw / 2, ty + 16, f"k = {k}", size=10.5, check=False)
    for c in range(m_ctl + 1):
        yy = ty + 24 + c * ch
        d.label(tx - 10, yy + 17, f"c = {c}", size=10.5, anchor="end", check=False)
        for k in range(n_rep + 1):
            v = ver.decide(k, n_rep, c, m_ctl)
            fill, stroke = KINDS[V_KIND[v]]
            _raw(d, f'<rect x="{tx + k * cw}" y="{yy}" width="{cw - 4}" height="{ch - 4}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
            d.label(tx + k * cw + (cw - 4) / 2, yy + 15, v.value, size=9.8, weight=600, color=INK, check=False)
    lo5, hi5 = ver.wilson(5, 5)
    lo0, hi0 = ver.wilson(0, 5)
    d.note(100, 500, 470, ["What counts as a pass, and how sure we are",
                           "A replay passes only if every originally failing target check now",
                           "passes and no check that passed before has stopped passing.",
                           f"Wilson 95% interval for k/N: 5 of 5 gives {lo5:.0%} to {hi5:.0%}; 0 of 5 gives {lo0:.0%} to {hi0:.0%}.",
                           "With five replays the interval is wide, and the report says so."], "plain", id="pass")
    d.note(rx, 530, rw, ["Limits", f"N is at most {ver.MAX_REPLAYS} and M at most {ver.MAX_CONTROLS}. A changed threshold is a new rule version (VR-2), never an edit of VR-1."],
           "warn", id="limits")
    return Sheet(
        d, "Algorithms", "Data Structure and Algorithm Design",
        "VR-1 is the answer to the panel's question about how a flaw is verified. The chart shows the whole rule: "
        "the horizontal axis is how often the outcome became correct when the suspected step was fixed, the "
        "vertical axis how often it became correct without the fix. Only the bottom-right corner is a "
        "confirmation: the fix works and the controls stay broken. The dots are the 18 possible outcomes of the "
        "default experiment and the table below repeats them as text; both are produced by calling the real "
        "decide() function, so the picture and the code cannot disagree. The rule is checked in order, and an "
        "unfinished experiment never yields a verdict.",
        ["packages/granite_core/granite_core/verification.py", "packages/granite_core/tests/test_verification.py",
         "docs/adr/adr-006-vr1-verdict-rule.md"],
        "Thresholds, limits, every dot and every table cell are computed by calling decide() and wilson() when the "
        "pack is built.",
    )


def replay_plan() -> Sheet:
    case = recorded_case()
    exp, out, defn = case["exp"], case["out"], case["defn"]
    target = out.fault.target_step
    plan = ver.plan_replay(out.trace, exp.intervention)
    steps = [s.step_id for s in defn.steps]
    agent = {s.step_id: s.agent for s in defn.steps}
    d = Diagram("replay-plan", "Replay plan: fix one step, keep everything before it", 1500, 520,
                "Which steps are copied and which are re-executed when a hypothesis is verified, on a recorded run.")
    xs = {sid: 250 + i * 200 for i, sid in enumerate(steps)}
    rows = {"orig": 96, "fix": 226, "ctl": 356}
    d.label(30, rows["orig"] + 28, "Original run", anchor="start", weight=700, color=INK, size=12.5, check=False)
    d.label(30, rows["orig"] + 46, "recorded, with the fault", anchor="start", size=10.8, check=False)
    d.label(30, rows["fix"] + 28, f"Replay with the fix (×{exp.summary.n_planned})", anchor="start", weight=700, color=INK, size=12.5, check=False)
    d.label(30, rows["fix"] + 46, "seeds 1000, 1001, ...", anchor="start", size=10.8, check=False)
    d.label(30, rows["ctl"] + 28, f"Control (×{exp.summary.m_planned})", anchor="start", weight=700, color=INK, size=12.5, check=False)
    d.label(30, rows["ctl"] + 46, "seeds 1500, 1501, ...", anchor="start", size=10.8, check=False)
    patched = ", ".join(exp.intervention.patches)
    for row, y in rows.items():
        for i, sid in enumerate(steps):
            frozen = sid in plan.frozen
            if row == "orig":
                kind, line = ("bad", "wrong value, no error") if sid == target else ("workflow", "executed")
            elif sid == target:
                kind, line = ("ok", f"copied, {patched} patched") if row == "fix" else ("bad", "copied unchanged")
            elif frozen:
                kind, line = "external", "copied, no model call"
            else:
                kind, line = "core", "executed again"
            node = d.node(f"{row}-{sid}", xs[sid], y, 170, 60, f"{sid}  {agent[sid]}", [line], kind)
            if i:
                prev = d.nodes[f"{row}-{steps[i - 1]}"]
                d.edge([prev.right(), node.left()], src=prev.id, dst=node.id)
    failing = case["failing"][0]
    s = exp.summary
    res = [("orig", "bad", f"{failing.check_id} fails", f"observed {failing.observed}, expected {failing.expected}"),
           ("fix", "ok" if s.k_pass == s.n_completed else "warn", f"{s.k_pass} of {s.n_completed} now pass", "outcome correct, no regression"),
           ("ctl", "bad" if s.c_pass == 0 else "warn", f"{s.c_pass} of {s.m_completed} pass", "still wrong without the fix")]
    for row, kind, title, line in res:
        last = d.nodes[f"{row}-{steps[-1]}"]
        r = d.node(f"{row}-result", 1270, rows[row], 200, 60, title, [line], kind, shape="pill")
        d.edge([last.right(), r.left()], src=last.id, dst=r.id)
    d.label(1370, 76, "Outcome (computed)", weight=700, color=INK, size=11.5, check=False)
    d.note(250, 448, 620, ["Verdict for this experiment", f"{s.verdict.value.upper()} under {s.rule_version}: {s.explanation}"[:112],
                           f"plan_replay() froze {', '.join(plan.frozen)} and re-executes {', '.join(plan.replay)}."], "ok" if s.verdict is ver.Verdict.CONFIRMED else "warn", id="verdict")
    d.legend(900, 430, [("external", "copied from the stored trace"), ("core", "executed again"), ("ok", "copied and patched"),
                        ("bad", "carries the wrong value")], title="Step treatment", cols=2, col_w=200)
    return Sheet(
        d, "Algorithms", "Data Structure and Algorithm Design",
        "Verification is a controlled experiment on a stored trace. The planner splits the steps at the suspected "
        "one: everything up to and including it is copied from the trace without calling a model, and only the "
        "later steps run again. In a replay with the fix the suspected step's output is patched with the value "
        "its repair rule computes; in a control it is left as it was. Different seeds are used so that a pass "
        "cannot be a lucky repetition. The outcome column is real: it is the result of running this experiment "
        "on the recorded example when the pack is built.",
        ["packages/granite_core/granite_core/verification.py", "packages/granite_core/granite_core/runner.py",
         "packages/granite_core/granite_core/experiment.py", "workflows/refund_desk/refund_desk/definition.py",
         "data/cassettes/refund_desk_v1.json"],
        "The frozen and re-executed steps come from plan_replay(), the patched field from the workflow's repair "
        "rule, and the counts and verdict from run_experiment() on the recorded run.",
    )
