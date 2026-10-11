"""Behaviour design: data flow diagrams (context and level 1) and the lineage graph of the Refund Desk."""

from __future__ import annotations

from collections import defaultdict

from refund_desk import StalePriceFault, build_workflow

from . import Sheet
from .kit import Diagram


def dfd_context() -> Sheet:
    d = Diagram("dfd-context", "Data flow diagram: context (level 0)", 1240, 400,
                "Granite as one process, with everything that crosses its boundary.")
    d.node("analyst", 40, 170, 190, 80, "Analyst", ["developer, QA or reviewer"], "actor")
    d.node("granite", 500, 130, 240, 160, "0   Granite", ["investigation workbench"], "core", shape="circle", title_size=14)
    d.node("llm", 1010, 120, 200, 70, "Language model", ["Ollama or hosted endpoint"], "external")
    d.node("retail", 1010, 232, 200, 70, "Retail data", ["orders, customers, catalogue"], "external")
    d.edge([(230, 190), (504, 190)], src="analyst", dst="granite")
    d.label(367, 168, "task, fault choice,")
    d.label(367, 183, "verify request, review decision")
    d.edge([(506, 236), (230, 236)], src="granite", dst="analyst")
    d.label(367, 252, "run trace, check results, findings,")
    d.label(367, 267, "ranked hypotheses, verdicts, evidence, report")
    d.edge([(680, 140), (1010, 140)], "prompts (messages, seed)", "granite", "llm", label_dy=-7)
    d.edge([(1010, 172), (726, 172)], "completions", "llm", "granite", label_dy=15)
    d.edge([(1010, 267), (709, 267)], "orders, catalogue prices (source of truth)", "retail", "granite", label_dy=-7)
    d.note(40, 300, 420, ["Boundary", "In recorded mode the language model is replaced by a file of saved",
                          "answers; nothing else about the flows changes."], "plain", id="boundary")
    return Sheet(
        d, "Behaviour", "Data Flow Diagram (DFD)",
        "At context level Granite has three neighbours. The analyst supplies a task and decisions and receives "
        "everything needed to judge a run. The language model is the only non-deterministic neighbour; it receives "
        "prompts and returns text, and can be replaced by recorded answers. The retail data plays two roles on "
        "purpose: the workflow's tool step reads orders from it, and the checks read catalogue prices from it "
        "independently, which is what lets a stale tool answer be detected.",
        ["apps/api/granite_api/routes.py", "apps/api/granite_api/providers.py", "workflows/refund_desk/refund_desk/store.py"],
        "Curated; the level-1 diagram refines the single process.",
    )


def dfd_level1() -> Sheet:
    d = Diagram("dfd-level-1", "Data flow diagram: level 1", 1380, 800,
                "The six processes inside Granite, the stores they share and the data that moves between them.")
    # processes
    d.node("p1", 290, 150, 180, 80, "1.0  Run workflow", ["runner.run_workflow"], "core", shape="pill")
    d.node("p2", 600, 150, 180, 80, "2.0  Check and detect", ["checks, findings"], "core", shape="pill")
    d.node("p3", 910, 150, 180, 80, "3.0  Trace back", ["attribution"], "core", shape="pill")
    d.node("p4", 290, 560, 180, 80, "4.0  Verify by replay", ["experiment, VR-1"], "core", shape="pill")
    d.node("p5", 910, 560, 180, 80, "5.0  Review and record", ["lifecycle, audit"], "core", shape="pill")
    d.node("p6", 1180, 560, 170, 80, "6.0  Report", ["Markdown, JSON"], "core", shape="pill")
    # stores
    d.node("d1", 290, 380, 180, 46, "Runs and traces", [], "store", shape="store")
    d.node("d2", 600, 380, 180, 46, "Check results", [], "store", shape="store")
    d.node("d3", 860, 380, 280, 46, "Investigation records", [], "store", shape="store")
    d.node("d4", 590, 577, 200, 46, "Audit log", [], "store", shape="store")
    d.node("d5", 430, 40, 230, 46, "Retail data snapshot", [], "store", shape="store")
    for sid, tag in (("d1", "D1"), ("d2", "D2"), ("d3", "D3"), ("d4", "D4"), ("d5", "D5")):
        n = d.nodes[sid]
        d.label(n.x + 13, n.cy + 4, tag, size=10.5, weight=700, check=False)
    # external entities
    d.node("a1", 30, 160, 130, 60, "Analyst", [], "actor")
    d.node("m1", 30, 40, 130, 60, "Language model", [], "external")
    d.node("a2", 30, 570, 130, 60, "Analyst", ["(repeated)"], "actor")
    d.node("m2", 30, 700, 130, 60, "Language model", ["(repeated)"], "external")
    d.node("a3", 935, 720, 130, 60, "Analyst", ["(repeated)"], "actor")
    # flows
    d.edge([(160, 190), (290, 190)], "task, fault, mode", "a1", "p1", label_dy=-7)
    d.edge([(335, 150), (335, 70), (160, 70)], "prompts / completions", "p1", "m1", start="arrow", label_at=(247, 64))
    d.edge([(445, 86), (445, 150)], src="d5", dst="p1")
    d.label(437, 124, "orders", anchor="end")
    d.edge([(630, 86), (630, 150)], src="d5", dst="p2")
    d.label(642, 124, "catalogue prices (truth)", anchor="start")
    d.edge([(470, 190), (600, 190)], "trace", "p1", "p2", label_dy=-7)
    d.edge([(780, 190), (910, 190)], "trace + results", "p2", "p3", label_dy=-7)
    d.edge([(380, 230), (380, 380)], src="p1", dst="d1")
    d.label(392, 312, "trace, fault record", anchor="start")
    d.edge([(690, 230), (690, 380)], src="p2", dst="d2")
    d.label(678, 345, "check results", anchor="end")
    d.edge([(753, 228), (753, 300), (900, 300), (900, 380)], "finding, evidence", "p2", "d3", label_at=(826, 294))
    d.edge([(1000, 230), (1000, 380)], src="p3", dst="d3")
    d.label(1012, 312, "ranked hypotheses, evidence", anchor="start")
    d.edge([(380, 426), (380, 560)], src="d1", dst="p4")
    d.label(368, 520, "original trace", anchor="end")
    d.edge([(434, 560), (434, 490), (880, 490), (880, 426)], "hypothesis in · replays, verdict, evidence out", "p4", "d3",
           start="arrow", label_at=(657, 484))
    d.edge([(1000, 560), (1000, 426)], src="p5", dst="d3", start="arrow")
    d.label(1012, 546, "status, review, note", anchor="start")
    d.edge([(1110, 426), (1110, 520), (1265, 520), (1265, 560)], src="d3", dst="p6")
    d.label(1122, 512, "finding, experiments, evidence", anchor="start")
    d.edge([(160, 600), (290, 600)], "hypothesis, N, M", "a2", "p4", label_dy=-7)
    d.edge([(335, 640), (335, 730), (160, 730)], "prompts / completions", "p4", "m2", start="arrow", label_at=(247, 724))
    d.edge([(910, 600), (790, 600)], "state change, actor", "p5", "d4", label_dy=-7)
    d.edge([(1000, 720), (1000, 640)], src="a3", dst="p5")
    d.label(988, 688, "decision, comment", anchor="end")
    d.edge([(1265, 640), (1265, 750), (1065, 750)], "report", "p6", "a3", label_at=(1165, 744))
    d.legend(1150, 40, [("core", "process"), ("store", "data store (tables, files)"), ("actor", "external entity")], col_w=200)
    d.note(1150, 130, 200, ["Stores and tables", "D1 runs, fault_injections", "D2 check_results", "D3 findings, hypotheses,",
                            "   experiments, replays,", "   evidence, reviews", "D4 audit_log, jobs", "D5 data/seed (read-only)"],
           "plain", id="stores")
    return Sheet(
        d, "Behaviour", "Data Flow Diagram (DFD)",
        "The top row is what happens automatically after a task is submitted: run, check, trace back. The bottom "
        "row is what a person starts later: verify, review, report. The two rows share only stored data, which "
        "is the reason a verification can be run on a trace recorded earlier. Process 4 never reads the fault "
        "record in D1, and process 3 never reads it either: the injected fault is kept only to score the "
        "analysis. The note on the right maps each store to real tables.",
        ["apps/api/granite_api/services", "apps/api/granite_api/models.py", "packages/granite_core/granite_core"],
        "Curated; process names are the modules of the structure chart and the stores are the tables of the ER diagram.",
    )


def lineage_graph() -> Sheet:
    defn = build_workflow()
    fault_step = StalePriceFault().target_step
    order = ["task", *[s.step_id for s in defn.steps]]
    pos = {sid: 40 + i * 262 for i, sid in enumerate(order)}
    fields: dict[tuple[str, str], list[str]] = defaultdict(list)
    for s in defn.steps:
        for ref in s.reads:
            src, fld = ref.split(".", 1)
            fields[(src, s.step_id)].append(fld)
    checks_at: dict[str, list[str]] = defaultdict(list)
    for c in defn.checks:
        checks_at[c.step].append(c.id)

    def wrap(names: list[str], limit: int = 15) -> list[str]:
        lines, cur = [], ""
        for i, name in enumerate(names):
            piece = name + ("," if i < len(names) - 1 else "")
            if cur and len(cur) + 1 + len(piece) > limit:
                lines.append(cur)
                cur = piece
            else:
                cur = f"{cur} {piece}".strip()
        return [*lines, cur]

    d = Diagram("refund-desk-dataflow", "Lineage graph of the Refund Desk", 1530, 580,
                "Which step reads which field of which earlier step: the graph attribution walks backwards.")
    y, w, h = 230, 170, 96
    d.node("task", pos["task"], y, w, h, "Task input", ["message, e-mail,", "order id"], "actor")
    for s in defn.steps:
        lines = [f"{s.kind} step", *checks_at.get(s.step_id, [])]
        if defn.repairs.get(s.step_id):
            lines.append("replay defined")
        d.node(s.step_id, pos[s.step_id], y, w, h, f"{s.step_id}  {s.agent}", lines,
               "bad" if s.step_id == fault_step else "workflow", tip="reads: " + ", ".join(s.reads))
    above, below = 0, 0
    for (src, dst), flds in sorted(fields.items(), key=lambda kv: (order.index(kv[0][1]) - order.index(kv[0][0]), kv[0])):
        span = order.index(dst) - order.index(src)
        text = ", ".join(flds)
        a, b = d.nodes[src], d.nodes[dst]
        if span == 1:
            d.edge([a.right(), b.left()], src=src, dst=dst, tip=text)
            parts = wrap(flds)
            for i, part in enumerate(parts):
                d.label((a.x + a.w + b.x) / 2, a.cy - 8 - (len(parts) - 1 - i) * 14.5, part, size=10.2, owner=f"{src}->{dst}")
        elif above <= below:
            lane = y - 60 - above * 46
            d.edge([a.top(0.72), (a.x + a.w * 0.72, lane), (b.x + b.w * 0.28, lane), b.top(0.28)], text, src, dst,
                   label_at=((a.x + a.w * 0.72 + b.x + b.w * 0.28) / 2, lane - 6))
            above += 1
        else:
            lane = y + h + 60 + below * 46
            d.edge([a.bottom(0.72), (a.x + a.w * 0.72, lane), (b.x + b.w * 0.28, lane), b.bottom(0.28)], text, src, dst,
                   label_at=((a.x + a.w * 0.72 + b.x + b.w * 0.28) / 2, lane - 6))
            below += 1
    fx = d.nodes[fault_step]
    d.note(fx.x - 40, 460, 250, ["Where the fault enters", f"stale_price changes {fault_step}.items[i].price", "by 0.25 with no error; every later",
                                 "step then works correctly on a wrong value."], "bad", id="fault")
    d.edge([(fx.cx, 460), fx.bottom(0.5)], src="fault", dst=fault_step, dashed=True)
    d.note(1100, 460, 390, ["Why this graph matters", "A wrong amount in s5's message is followed backwards along",
                           "these edges. A step whose own check failed against the source",
                           "of truth is the best origin candidate (weight 1.0)."], "plain", id="why")
    return Sheet(
        d, "Behaviour", "Network Automata / Graphs or State Machine",
        "This is the data-lineage graph of the system under test, drawn from the reads each step declares in "
        "refund_desk/definition.py. The runner records these edges with every run, and attribution walks them "
        "backwards from the step where the symptom appeared. Under each step are the checks attached to it, and "
        "'replay defined' marks the steps for which the workflow gives a repair rule, so a hypothesis blaming "
        "them can be verified by replay. The red step is where the built-in fault is injected.",
        ["workflows/refund_desk/refund_desk/definition.py", "workflows/refund_desk/refund_desk/faults.py",
         "packages/granite_core/granite_core/lineage.py"],
        "Fully generated: steps, edges, field names, checks per step, repair rules and the fault target are read from "
        "the workflow definition when the pack is built.",
    )
