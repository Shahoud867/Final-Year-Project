"""Behaviour design: two sequence diagrams and a call graph computed from the source code."""

from __future__ import annotations

import ast
from pathlib import Path

from . import Sheet
from .kit import INK, LINE, MUTED, Diagram, esc, text_width

ROOT = Path(__file__).resolve().parents[2]


# ---- sequence diagrams ------------------------------------------------------------------------------------
def _sequence(key: str, title: str, desc: str, parts: list[tuple[str, str, str]], steps: list[tuple], spacing: int = 178) -> Diagram:
    """parts: (id, label, kind). steps: ('msg'|'ret', from, to, text) | ('self', who, text) | ('frame', tag, guard, left, right, rows)."""
    xs = {pid: 95 + i * spacing for i, (pid, _, _) in enumerate(parts)}
    rows = [s for s in steps if s[0] != "frame"]
    ys: list[float] = []
    y = 132.0
    for s in rows:
        ys.append(y)
        y += 48 if s[0] == "self" else 42
    height = int(y + 30)
    width = int(max(xs.values()) + 190)
    d = Diagram(key, title, width, height, desc)
    for pid, label, kind in parts:
        d.node(pid, xs[pid] - 78, 40, 156, 46, label, [], kind)
        d._back.append(f'<path d="M{xs[pid]} 86 V{height - 20}" stroke="{LINE}" stroke-width="1.1" stroke-dasharray="5 5" fill="none"/>')
    # frames
    row_i = 0
    for s in steps:
        if s[0] != "frame":
            row_i += 1
            continue
        _, tag, guard, left, right, n = s
        top, bottom = ys[row_i] - 28, ys[row_i + n - 1] + 18
        x0, x1 = xs[left] - 84, xs[right] + 84
        tab = 16 + text_width(tag, 11, True)
        d._back.append(
            f'<g class="frame"><rect x="{x0}" y="{top}" width="{x1 - x0}" height="{bottom - top}" rx="4" fill="#f6f8fb" '
            f'fill-opacity="0.75" stroke="#9aa4b1" stroke-width="1.1"/>'
            f'<path d="M{x0} {top} H{x0 + tab} V{top + 13} L{x0 + tab - 7} {top + 20} H{x0} Z" fill="#ffffff" stroke="#9aa4b1" stroke-width="1.1"/>'
            f'<text x="{x0 + 7}" y="{top + 14}" style="font-size:11px;font-weight:700;fill:{INK}">{esc(tag)}</text>'
            f'<text x="{x0 + tab + 8}" y="{top + 14}" style="font-size:11px;font-style:italic;fill:{MUTED}">[{esc(guard)}]</text></g>'
        )
    # messages
    for n, (s, yy) in enumerate(zip(rows, ys, strict=True), 1):
        if s[0] == "self":
            _, who, text = s
            x = xs[who]
            d.edge([(x, yy), (x + 44, yy), (x + 44, yy + 20), (x + 3, yy + 20)], src=who, dst=who, tip=text)
            d.label(x + 52, yy + 14, f"{n}  {text}", anchor="start", size=11, check=False)
        else:
            kind, f, t, text = s
            x1, x2 = xs[f], xs[t]
            pad = 3 if x2 > x1 else -3
            d.edge([(x1, yy), (x2 - pad, yy)], src=f, dst=t, dashed=(kind == "ret"), end="open" if kind == "ret" else "arrow",
                   tip=text)
            d.label((x1 + x2) / 2, yy - 6, f"{n}  {text}", size=11, check=False)
    return d


def sequence_run() -> Sheet:
    parts = [("analyst", "Analyst", "actor"), ("ui", "Web UI", "web"), ("api", "API routes", "api"), ("db", "Database", "store"),
             ("jobs", "Job runner", "api"), ("svc", "Run service", "api"), ("core", "granite_core", "core"),
             ("model", "Model provider", "external")]
    steps = [
        ("msg", "analyst", "ui", "Run workflow (task, fault)"),
        ("msg", "ui", "api", "POST /api/runs"),
        ("self", "api", "validate task; choose live or recorded"),
        ("msg", "api", "db", "insert run (queued)"),
        ("msg", "api", "jobs", "submit(run job)"),
        ("ret", "api", "ui", "202 run_id, job_id"),
        ("msg", "jobs", "svc", "run_job(run_id)"),
        ("msg", "svc", "core", "run_workflow(...)"),
        ("frame", "loop", "each of the 5 steps; model steps only", "core", "model", 2),
        ("msg", "core", "model", "complete(request)"),
        ("ret", "model", "core", "Completion"),
        ("ret", "core", "svc", "RunOutcome (trace)"),
        ("msg", "svc", "core", "evaluate_checks()"),
        ("msg", "svc", "core", "derive_findings(), attribute()"),
        ("ret", "core", "svc", "findings, hypotheses"),
        ("msg", "svc", "db", "trace, results, finding, hypotheses, evidence"),
        ("frame", "loop", "until the job has finished", "ui", "api", 2),
        ("msg", "ui", "api", "GET /api/jobs/{id}"),
        ("ret", "api", "ui", "status, progress"),
        ("msg", "ui", "api", "GET /api/runs/{id}"),
        ("ret", "api", "ui", "run, graph, findings"),
        ("ret", "ui", "analyst", "graph, checks, finding"),
    ]
    d = _sequence("run-sequence", "Sequence diagram: run and analyse", "From pressing Run to seeing a finding.", parts, steps)
    return Sheet(
        d, "Behaviour", "Call Graph or Sequence Diagram",
        "The request returns at message 6, before any model is called: a run with a local model takes about a "
        "minute, so the work is handed to the job runner and the browser polls for progress (messages 17 and 18). "
        "The model is called only inside the loop, by the core, through the provider interface. Analysis "
        "(messages 13 to 15) happens in the same job, immediately after the run, and everything is written in "
        "one transaction (message 16): a run is never visible without its check results.",
        ["apps/api/granite_api/routes.py", "apps/api/granite_api/services/runs.py", "apps/api/granite_api/services/analysis.py",
         "apps/api/granite_api/jobs.py", "packages/granite_core/granite_core/runner.py", "apps/web/src/pages/NewRun.tsx"],
        "Curated from the code paths; the function names appear in the generated call graph, and the journey is "
        "exercised by apps/api/tests/test_journeys.py and tests/system.",
    )


def sequence_verify() -> Sheet:
    parts = [("analyst", "Analyst", "actor"), ("ui", "Web UI", "web"), ("api", "API routes", "api"), ("db", "Database", "store"),
             ("jobs", "Job runner", "api"), ("svc", "Experiment service", "api"), ("core", "granite_core", "core"),
             ("model", "Model provider", "external")]
    steps = [
        ("msg", "analyst", "ui", "Verify (N, M)"),
        ("msg", "ui", "api", "POST .../experiments"),
        ("msg", "api", "svc", "create_experiment()"),
        ("msg", "svc", "core", "build_intervention()"),
        ("frame", "alt", "no repair rule, or the state forbids it", "api", "svc", 1),
        ("ret", "svc", "api", "422 cannot verify / 409 allowed actions"),
        ("msg", "svc", "db", "finding = verifying; experiment queued"),
        ("msg", "api", "jobs", "submit(experiment job)"),
        ("ret", "api", "ui", "202 experiment_id, job_id"),
        ("msg", "jobs", "svc", "experiment_job()"),
        ("msg", "svc", "core", "run_experiment(N, M)"),
        ("frame", "loop", "N replays with the fix, then M controls", "db", "model", 6),
        ("self", "core", "execute_replay: copy frozen steps"),
        ("msg", "core", "model", "complete()"),
        ("ret", "model", "core", "Completion"),
        ("self", "core", "evaluate_checks, judge_replay"),
        ("ret", "core", "svc", "on_replay(record)"),
        ("msg", "svc", "db", "store replay, progress"),
        ("self", "core", "decide (VR-1), Wilson interval"),
        ("ret", "core", "svc", "summary, replays"),
        ("msg", "svc", "db", "verdict, evidence, finding status"),
        ("msg", "ui", "api", "GET /api/findings/{id}"),
        ("ret", "api", "ui", "status, verdict, evidence"),
        ("ret", "ui", "analyst", "verdict card"),
    ]
    d = _sequence("verification-sequence", "Sequence diagram: verify a hypothesis", "From pressing Verify to a verdict.", parts, steps)
    return Sheet(
        d, "Behaviour", "Call Graph or Sequence Diagram",
        "Two refusals happen before any model call (message 5): a step with no repair rule cannot be replayed, and "
        "a finding in the wrong state cannot be verified. Inside the loop, message 12 is the reason replays are "
        "cheap and exact: steps up to the suspected one are copied from the stored trace, and only later steps "
        "run again, each replay with its own seed. Every replay is stored as it finishes (message 17), so "
        "progress is visible and a failure half-way keeps the completed replays. The verdict (message 18) is "
        "computed once, by a fixed rule, after all replays.",
        ["apps/api/granite_api/services/experiments.py", "packages/granite_core/granite_core/experiment.py",
         "packages/granite_core/granite_core/runner.py", "packages/granite_core/granite_core/verification.py",
         "apps/web/src/components/Verify.tsx"],
        "Curated from the code paths; the same calls appear in the generated call graph and the flow is covered by "
        "packages/granite_core/tests/test_experiment.py.",
    )


# ---- call graph (computed) --------------------------------------------------------------------------------
MODULES: dict[str, tuple[str, str]] = {
    "granite_api.routes": ("apps/api/granite_api/routes.py", "api"),
    "granite_api.jobs": ("apps/api/granite_api/jobs.py", "api"),
    "granite_api.llm_factory": ("apps/api/granite_api/llm_factory.py", "api"),
    "granite_api.registry": ("apps/api/granite_api/registry.py", "api"),
    "granite_api.services.runs": ("apps/api/granite_api/services/runs.py", "api"),
    "granite_api.services.analysis": ("apps/api/granite_api/services/analysis.py", "api"),
    "granite_api.services.experiments": ("apps/api/granite_api/services/experiments.py", "api"),
    "granite_api.services.reviews": ("apps/api/granite_api/services/reviews.py", "api"),
    "granite_api.services.report": ("apps/api/granite_api/services/report.py", "api"),
    "granite_api.services.common": ("apps/api/granite_api/services/common.py", "api"),
    "granite_core.runner": ("packages/granite_core/granite_core/runner.py", "core"),
    "granite_core.checks": ("packages/granite_core/granite_core/checks.py", "core"),
    "granite_core.dsl": ("packages/granite_core/granite_core/dsl.py", "core"),
    "granite_core.attribution": ("packages/granite_core/granite_core/attribution.py", "core"),
    "granite_core.lineage": ("packages/granite_core/granite_core/lineage.py", "core"),
    "granite_core.verification": ("packages/granite_core/granite_core/verification.py", "core"),
    "granite_core.experiment": ("packages/granite_core/granite_core/experiment.py", "core"),
    "granite_core.lifecycle": ("packages/granite_core/granite_core/lifecycle.py", "core"),
    "granite_core.evidence": ("packages/granite_core/granite_core/evidence.py", "core"),
}
# Small helpers that nearly everything calls; drawing them would hide the structure. Listed in the diagram's note.
OMITTED = {"granite_api.services.common.audit", "granite_core.evidence.canonical_json", "granite_core.lineage.edges",
           "granite_core.lineage.incoming", "granite_api.llm_factory.live_available"}
ENTRY = ["granite_api.routes.create_run", "granite_api.routes.start_experiment", "granite_api.routes.post_review",
         "granite_api.routes.get_report"]


def _scan() -> tuple[dict[str, set[str]], dict[str, str]]:
    """Return (calls between top-level functions, function -> module) using only static analysis."""
    defs: dict[str, dict[str, ast.FunctionDef]] = {}
    symbols: dict[str, dict[str, tuple[str, str | None]]] = {}
    for mod, (path, _) in MODULES.items():
        tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
        defs[mod] = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
        table: dict[str, tuple[str, str | None]] = {name: (mod, name) for name in defs[mod]}
        pkg = mod.split(".")[:-1]
        for node in tree.body:
            if not isinstance(node, ast.ImportFrom):
                continue
            base = pkg[: len(pkg) - (node.level - 1)] if node.level else []
            source = ".".join([*base, *(node.module.split(".") if node.module else [])])
            for alias in node.names:
                local = alias.asname or alias.name
                if f"{source}.{alias.name}" in MODULES:
                    table[local] = (f"{source}.{alias.name}", None)  # a module alias
                elif source in MODULES:
                    table[local] = (source, alias.name)  # an imported function (or class)
        symbols[mod] = table

    def callees(mod: str, fn: ast.FunctionDef) -> set[str]:
        found: set[str] = set()
        for node in ast.walk(fn):
            if not isinstance(node, ast.Call):
                continue
            target: tuple[str, str | None] | None = None
            if isinstance(node.func, ast.Name):
                target = symbols[mod].get(node.func.id)
            elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                owner = symbols[mod].get(node.func.value.id)
                if owner and owner[1] is None:
                    target = (owner[0], node.func.attr)
            if target and target[1] and target[1] in defs.get(target[0], {}):
                found.add(f"{target[0]}.{target[1]}")
        return found

    raw = {f"{mod}.{name}": callees(mod, fn) for mod, fns in defs.items() for name, fn in fns.items()}

    def public_callees(name: str, seen: frozenset[str] = frozenset()) -> set[str]:
        """Calls made by a function, with the calls of the private helpers it uses folded in."""
        out: set[str] = set()
        for callee in raw.get(name, ()):
            if callee in seen or callee == name or callee in OMITTED:
                continue
            if callee.rsplit(".", 1)[1].startswith("_"):
                out |= public_callees(callee, seen | {name})
            else:
                out.add(callee)
        return out

    graph: dict[str, set[str]] = {}
    todo = list(ENTRY)
    while todo:
        cur = todo.pop()
        if cur in graph:
            continue
        graph[cur] = public_callees(cur)
        todo.extend(graph[cur])
    return graph, {name: name.rsplit(".", 1)[0] for name in graph}


def call_graph() -> Sheet:
    graph, owner = _scan()
    missing = [e for e in ENTRY if e not in graph]
    if missing:
        raise SystemExit(f"call graph: entry points not found: {missing}")
    depth: dict[str, int] = {}

    def level(name: str, trail: tuple[str, ...] = ()) -> int:
        if name in depth:
            return depth[name]
        callers = [c for c, targets in graph.items() if name in targets and c not in trail]
        depth[name] = 0 if not callers else 1 + max(level(c, (*trail, name)) for c in callers)
        return depth[name]

    for name in graph:
        level(name)
    order: list[str] = []

    def visit(name: str) -> None:
        if name in order:
            return
        order.append(name)
        for callee in sorted(graph[name], key=lambda c: (depth[c], c)):
            visit(callee)

    for e in ENTRY:
        visit(e)
    cols = max(depth.values()) + 1
    col_w, gap, row_h, box_h = 232, 84, 31, 24
    width = 40 + cols * col_w + (cols - 1) * gap + 40
    height = 110 + len(order) * row_h + 90
    d = Diagram("call-graph", "Call graph (computed from the source)", width, height,
                "Which function calls which, from the four HTTP entry points down to the core primitives.")
    short = lambda n: n.split(".", 1)[1].replace("services.", "")  # noqa: E731
    for i, name in enumerate(order):
        x = 40 + depth[name] * (col_w + gap)
        d.node(name, x, 80 + i * row_h, col_w, box_h, short(name), [], MODULES[owner[name]][1], tip=name, title_size=11.2)
    for c in range(cols):
        d.label(40 + c * (col_w + gap) + col_w / 2, 62, "HTTP entry points" if c == 0 else f"call depth {c}", size=11.5, weight=700,
                color=INK, check=False)
    sources_per_col: dict[int, list[str]] = {}
    for name in order:
        if graph[name]:
            sources_per_col.setdefault(depth[name], []).append(name)
    edges = 0
    for col, names in sources_per_col.items():
        step = (gap - 24) / max(len(names), 1)
        for k, name in enumerate(names):
            a = d.nodes[name]
            channel = a.x + col_w + 12 + k * step
            for callee in sorted(graph[name], key=order.index):
                b = d.nodes[callee]
                d.edge([a.right(), (channel, a.cy), (channel, b.cy), b.left()], src=name, dst=callee, width=1.15,
                       tip=f"{short(name)} calls {short(callee)}")
                edges += 1
    d.legend(40, height - 78, [("api", "apps/api function"), ("core", "granite_core function")], title="Colour", cols=2, col_w=200)
    d.note(480, height - 78, 760, ["How this was produced",
                                   f"Parsed with Python's ast module: {len(order)} functions, {edges} calls. Private helpers (names starting",
                                   "with _) are folded into their public caller. Five small helpers are left out: " + ", ".join(sorted(n.rsplit(".", 1)[1] for n in OMITTED)) + ".",
                                   "Method calls on objects are not followed."],
           "plain", id="how")
    return Sheet(
        d, "Behaviour", "Call Graph or Sequence Diagram",
        "The graph answers 'what code runs when I press this button'. Its four roots are the HTTP handlers for "
        "running a task, verifying a hypothesis, recording a review and exporting a report. Colours show the "
        "architecture holding: green application functions sit on the left and call blue core functions to their "
        "right, and no blue function ever calls a green one. Select a function in the interactive pack to "
        "highlight exactly what it calls and what calls it.",
        [path for path, _ in MODULES.values()],
        f"Fully computed: {len(order)} functions and {edges} call edges extracted from {len(MODULES)} source files by "
        "static analysis every time the pack is built.",
    )
