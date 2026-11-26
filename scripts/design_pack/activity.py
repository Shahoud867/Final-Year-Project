"""Behaviour design: activity diagram with swimlanes, deployment diagram, use-case diagram."""

from __future__ import annotations

from . import Sheet
from .kit import Diagram, vhv


def activity_diagram() -> Sheet:
    d = Diagram("activity-investigation", "Activity diagram: one investigation", 1400, 1570,
                "Who does what, in order, from choosing a task to downloading the report.")
    lanes = [("analyst", "Analyst", "actor", 30, 260), ("ui", "Web UI", "web", 290, 260), ("api", "API and jobs", "api", 550, 300),
             ("core", "granite_core", "core", 850, 280), ("model", "Language model", "external", 1130, 240)]
    lx = {}
    for lid, label, kind, x, w in lanes:
        d.lane(f"lane-{lid}", x, 40, w, 1510, label, kind)
        lx[lid] = (x + 20, w - 40, kind)

    def act(id: str, lane: str, row: int, title: str, line: str):
        x, w, kind = lx[lane]
        return d.node(id, x, 110 + row * 82, w, 54, title, [line], kind)

    def flow(a, b, label: str = ""):
        if abs(a.cx - b.cx) < 1:
            d.edge([a.bottom(), b.top()], src=a.id, dst=b.id)
        else:
            d.edge(vhv(a.bottom(), b.top()), src=a.id, dst=b.id)
        if label:
            d.label(a.cx + 10, a.y + a.h + 16, label, anchor="start")

    d.terminal("start", lx["analyst"][0] + lx["analyst"][1] / 2, 88)
    n = [
        act("a0", "analyst", 0, "Choose a task, set the fault", "an example, or own text"),
        act("a1", "ui", 1, "Check the form, send the run", "POST /api/runs"),
        act("a2", "api", 2, "Validate, store run, queue job", "answers 202 at once"),
        act("a3", "core", 3, "Execute the five steps", "run_workflow, record reads"),
        act("a4", "core", 4, "Check, detect, rank", "evaluate_checks, attribute"),
        act("a5", "api", 5, "Store trace, results, finding,", "hypotheses and evidence"),
        act("a6", "ui", 6, "Show graph, checks, finding", "poll the job, load the run"),
    ]
    m1 = act("m1", "model", 3, "Answer three prompts", "live, or recorded answers")
    ix, iw_, _ = lx["api"]
    imp = d.node("imported", ix, 110 + 3 * 82, iw_, 54, "Accept a trace file or SDK run", ["planned · FYP-1 Final"], "planned",
                 dashed=True)
    mx, mw, _ = lx["model"]
    so = d.node("second", mx, 110 + 4 * 82, mw, 54, "Second opinion", ["planned · FYP-2 Mid"], "planned", dashed=True)
    d.edge([(57 + lx["analyst"][1] / 2 - 7, 95), n[0].top()], src="start", dst="a0")
    for a, b in zip(n, n[1:], strict=False):
        flow(a, b)
    d.edge([n[3].right(), m1.left()], src="a3", dst="m1", start="arrow")
    d.edge([imp.bottom(), (imp.cx, imp.y + 68), (n[4].cx, imp.y + 68), n[4].top()], src="imported", dst="a4", dashed=True)
    d.edge([n[4].right(), so.left()], src="a4", dst="second", dashed=True, start="arrow")
    ax, aw, _ = lx["analyst"]
    q = d.node("q-finding", ax + 10, 110 + 7 * 82 - 6, aw - 20, 70, "Finding opened?", [], "plain", shape="diamond")
    flow(n[6], q)
    ux, uw, _ = lx["ui"]
    clean = d.node("clean", ux, 110 + 7 * 82 + 2, uw, 54, "Clean run: nothing to investigate", ["all outcome checks passed"], "ok")
    d.edge([q.right(), clean.left()], "no", "q-finding", "clean", label_dy=-7)
    d.terminal("end-clean", clean.cx + uw / 2 + 60, clean.cy, final=True)
    d.edge([clean.right(), (clean.cx + uw / 2 + 51, clean.cy)], src="clean", dst="end-clean")
    v = [
        act("v0", "analyst", 8, "Press Verify on a hypothesis", "choose N replays, M controls"),
        act("v1", "api", 9, "Check state and repair rule,", "queue the experiment"),
        act("v2", "core", 10, "Replay N with fix, M without", "run_experiment"),
        act("v3", "core", 11, "Decide by rule VR-1", "counts, Wilson interval"),
        act("v4", "api", 12, "Store replays, verdict,", "evidence, new status"),
        act("v5", "ui", 13, "Show the verdict and replays", "progress shown while running"),
        act("v6", "analyst", 14, "Accept, reject or ask", "the comment rule applies"),
        act("v7", "api", 15, "Record review and audit entry", "apply_review, lifecycle"),
        act("v8", "ui", 16, "Show status, offer the report", "Markdown or JSON"),
    ]
    m2 = act("m2", "model", 10, "Answer replay prompts", "only the re-executed steps")
    flow(q, v[0], "yes")
    for a, b in zip(v, v[1:], strict=False):
        flow(a, b)
    d.edge([v[2].right(), m2.left()], src="v2", dst="m2", start="arrow")
    d.terminal("end", v[8].cx, v[8].y + v[8].h + 40, final=True)
    d.edge([v[8].bottom(), (v[8].cx, v[8].y + v[8].h + 31)], src="v8", dst="end")
    d.note(lx["core"][0], 110 + 6 * 82, 430, ["Two things run without the analyst", "Steps in the green and blue lanes happen in a background job;",
                                              "the UI only polls. The model is reached from granite_core alone,", "never from the UI or the routes."],
           "plain", id="note")
    return Sheet(
        d, "Behaviour", "Activity Diagram",
        "Each lane is a responsibility, and the diagram shows that the analyst acts only three times: to start a "
        "run, to ask for verification and to decide. Everything between those actions is automatic and happens "
        "in a background job, which is why the UI lane only sends a request and then displays results. The "
        "language model is used in exactly two activities, both started from the core. The decision 'Finding "
        "opened?' is where a clean run ends; there is no path from a clean run to a review. The dashed activities "
        "are planned: from FYP-1 Final the API also accepts a trace file or an SDK run, which goes straight to "
        "checking, and from FYP-2 Mid ranking can ask the model for a second-opinion hypothesis.",
        ["apps/web/src/pages", "apps/api/granite_api/routes.py", "apps/api/granite_api/jobs.py",
         "apps/api/granite_api/services", "packages/granite_core/granite_core"],
        "Curated. The activities are the modules of the structure chart and the messages of the two sequence diagrams.",
    )


def deployment_diagram() -> Sheet:
    d = Diagram("deployment-diagram", "Deployment diagram", 1420, 700,
                "Where Granite runs today, how a change reaches the public demo, and what is planned for FYP-1 Final and FYP-2.")
    d.frame("laptop", 30, 60, 430, 400, "«device» Team laptop", "plain", note="verified")
    d.node("browser", 60, 100, 170, 54, "Browser", ["the built React UI"], "web")
    d.node("sdkapp", 260, 92, 170, 70, "App with the SDK", ["LangGraph: FYP-1 Final", "CrewAI: FYP-2 Mid"], "planned", dashed=True)
    d.node("uvicorn", 60, 200, 370, 64, "«process» uvicorn: granite_api", ["port 8000 · serves /api and the web bundle", "started from apps/api (setup manual, section 3)"], "api")
    d.node("sqlite", 60, 320, 170, 74, "SQLite file", ["apps/api/.granite/", "granite.db"], "store", shape="cyl")
    d.node("ollama", 260, 320, 170, 66, "«process» Ollama", ["optional · port 11434", "llama3.2:3b, live mode"], "external")
    d.frame("github", 500, 60, 430, 490, "«cloud» GitHub", "plain", note="verified on every push")
    d.node("repo", 530, 100, 370, 54, "Repository", ["Shahoud867/Final-Year-Project · branch main"], "store")
    d.node("ci", 530, 200, 370, 92, "«pipeline» GitHub Actions: CI", ["Python: lint, types, tests, security scans",
                                                                       "Web: lint, types, tests, build · secret scan", "Container: build image, smoke test inside it"], "api")
    d.node("cd", 530, 340, 370, 80, "«pipeline» GitHub Actions: CD", ["after CI passes on main: build the image,",
                                                                       "smoke-test it, publish it to ghcr.io,", "then call the Render deploy hook"], "api")
    d.node("oauth", 530, 470, 370, 60, "GitHub sign-in (OAuth)", ["reviewer identity · FYP-2 Mid"], "planned", dashed=True)
    d.frame("render", 970, 60, 420, 400, "«cloud» Render free web service", "plain", note="live since 11 Oct")
    d.node("visitor", 1000, 100, 360, 54, "Visitor's browser", ["https://granite-demo.onrender.com"], "web")
    d.node("container", 1000, 200, 360, 64, "«container» granite-demo", ["recorded mode · port 8000 · /api/health", "created from render.yaml"], "api")
    d.node("tmpdisk", 1000, 320, 170, 74, "Temporary disk", ["SQLite; resets on", "restart or deploy"], "store", shape="cyl")
    d.node("pg", 1190, 320, 170, 74, "PostgreSQL", ["tested at FYP-1 Final,", "deployed at FYP-2 Mid"], "planned", shape="cyl", dashed=True)
    d.edge([(145, 154), (145, 200)], src="browser", dst="uvicorn")
    d.label(157, 182, "HTTP :8000", anchor="start")
    d.edge([(345, 162), (345, 200)], src="sdkapp", dst="uvicorn", dashed=True)
    d.label(357, 186, "traces", anchor="start")
    d.edge([(145, 264), (145, 320)], src="uvicorn", dst="sqlite")
    d.label(157, 296, "file", anchor="start")
    d.edge([(345, 264), (345, 320)], src="uvicorn", dst="ollama")
    d.label(357, 296, "HTTP", anchor="start")
    d.edge([(460, 127), (530, 127)], "git push", "laptop", "repo", label_dy=-7)
    d.edge([(715, 154), (715, 200)], src="repo", dst="ci")
    d.label(727, 182, "push or pull request", anchor="start")
    d.edge([(715, 292), (715, 340)], src="ci", dst="cd")
    d.label(727, 320, "green on main", anchor="start")
    d.edge([(900, 372), (950, 372), (950, 232), (1000, 232)], src="cd", dst="container")
    d.label(956, 300, "deploy hook", anchor="start")
    d.edge([(1180, 154), (1180, 200)], src="visitor", dst="container")
    d.label(1192, 182, "HTTPS", anchor="start")
    d.edge([(1085, 264), (1085, 320)], src="container", dst="tmpdisk")
    d.edge([(1275, 264), (1275, 320)], src="container", dst="pg", dashed=True)
    d.label(1287, 296, "SQL", anchor="start")
    d.edge([(1000, 250), (985, 250), (985, 500), (900, 500)], src="container", dst="oauth", dashed=True)
    d.label(942, 494, "sign-in")
    d.legend(30, 600, [("api", "Granite process, pipeline"), ("web", "browser"), ("store", "data at rest"), ("external", "optional service"),
                       ("planned", "planned (milestone in the box)"), ("line:dashed", "planned connection")], cols=3, col_w=215)
    d.note(720, 600, 670, ["Status (2026-10-22)", "Everything solid is verified. The demo has been live on Render since 11 October. Since 13 October",
                           "CD calls the deploy hook once CI passes on main; Render builds the Dockerfile and CD then smoke-tests",
                           "the public URL, so no step is manual. Dashed parts are planned for FYP-1 Final and FYP-2."], "warn", id="status")
    return Sheet(
        d, "Deployment", "Deployment Diagram",
        "There is one deployable unit: a container image that holds the API, the built web UI and the recorded "
        "model answers, so it runs with no model server and no key. It runs in three verified places: on a team "
        "laptop as a single uvicorn process, inside GitHub Actions, where every push builds the image and runs an "
        "end-to-end smoke test in it, and on Render's free plan, where the public demo has run since 11 October. "
        "Since 13 October the CD workflow calls Render's deploy hook after CI passes on main, Render builds the "
        "Dockerfile, and CD smoke-tests the public URL. The dashed elements are planned: an application "
        "instrumented with the Granite SDK (LangGraph at FYP-1 Final, CrewAI at FYP-2 Mid), PostgreSQL in place "
        "of the temporary SQLite disk, and GitHub sign-in for reviewer identity at FYP-2 Mid.",
        ["Dockerfile", "docker-compose.yml", "render.yaml", ".github/workflows/ci.yml", ".github/workflows/cd.yml",
         "docs/registers/deployment-record.md", "evidence/repo/2026-10-09_ci-run-37924480165.md"],
        "Curated. Ports, modes and file locations are the defaults in apps/api/granite_api/config.py and the Dockerfile.",
    )


def use_case_diagram() -> Sheet:
    d = Diagram("use-case-diagram", "Use-case diagram (FYP-1 and FYP-2 scope)", 1540, 990,
                "All seventeen use cases: those built for FYP-1 Mid, and those planned for FYP-1 Final and FYP-2 Mid.")
    d.frame("system", 150, 40, 1180, 910, "Granite", "plain")
    lanes = [("lane-mid1", 195, "FYP-1 Mid: built and tested (Iteration 1)", "plain", False, ""),
             ("lane-final1", 585, "FYP-1 Final (Iteration 2)", "planned", True, "planned"),
             ("lane-mid2", 965, "FYP-2 Mid (Iteration 3)", "planned", True, "planned")]
    for lid, x, label, kind, dashed, note in lanes:
        d.frame(lid, x, 70, 340, 860, label, kind, dashed=dashed, note=note)
    columns = [
        (205, False, [("uc03", "UC-03  Run a workflow task", "with an optional injected fault"),
                      ("uc06", "UC-06  Analyse the run", "included by UC-03 and UC-04"),
                      ("uc05", "UC-05  Inspect a run", "graph, steps, check results"),
                      ("uc07", "UC-07  Investigate a finding", "ranked origin hypotheses"),
                      ("uc08", "UC-08  Verify a hypothesis", "controlled replay, verdict"),
                      ("uc09", "UC-09  Review a finding", "accept, reject, ask for information"),
                      ("uc11", "UC-11  Export a report", "Markdown, JSON; regression test later"),
                      ("uc12", "UC-12  Browse and search history", "filters by severity and level")]),
        (595, True, [("uc15a", "UC-15  Instrument via the SDK", "LangGraph adapter"),
                     ("uc01", "UC-01  Configure a project", "seeded at Mid-1, editable here"),
                     ("uc02", "UC-02  Define and test checks", "check editor with a dry run"),
                     ("uc04", "UC-04  Import a trace", "Granite Trace v1, Who&When files"),
                     ("uc10", "UC-10  Suggest and verify a fix", "LLM fix, then a recovered run"),
                     ("uc13", "UC-13  Generate a benchmark", "Fault Lab: labelled runs"),
                     ("uc14a", "UC-14  Run the evaluation (v0)", "120+ runs against baselines")]),
        (975, True, [("uc15b", "UC-15  Instrument via the SDK", "CrewAI adapter added"),
                     ("uc14b", "UC-14  Run the evaluation (full)", "300+ runs, confidence intervals"),
                     ("uc16", "UC-16  Reuse a known verified fix", "matched by failure signature"),
                     ("uc17", "UC-17  Manage keys and data", "API keys, retention, deletion"),
                     ("uc07x", "Second opinion (extends UC-07)", "LLM hypothesis, unverified until replayed")]),
    ]
    cy = {}
    for x, planned, cases in columns:
        for row, (cid, title, line) in enumerate(cases):
            y = 140 + 96 * row
            d.node(cid, x, y, 320, 56, title, [line], "planned" if planned else "core", shape="pill", dashed=planned)
            cy[cid] = y + 28
    d.actor("analyst", 40, 430, "Analyst")
    d.actor("iw", 1410, 128, "Instrumented workflow")
    d.actor("admin", 1410, 416, "Administrator")
    d.actor("llm", 1410, 860, "Language model")
    # the analyst reaches the first column from a trunk on the left, the planned columns over the top
    for cid in ("uc03", "uc05", "uc07", "uc08", "uc09", "uc11", "uc12"):
        d.edge([(100, 470), (170, 470), (170, cy[cid]), (205, cy[cid])], src="analyst", dst=cid, end="")
    for cid, trunk, x in [(c, 575, 595) for c in ("uc15a", "uc01", "uc02", "uc04", "uc10", "uc13", "uc14a")] + \
                         [(c, 955, 975) for c in ("uc15b", "uc14b", "uc16", "uc07x")]:
        d.edge([(100, 470), (170, 470), (170, 110), (trunk, 110), (trunk, cy[cid]), (x, cy[cid])], src="analyst", dst=cid, end="")
    # the language model reaches its use cases along the bottom
    for cid, x_out, x_bus in (("uc03", 525, 550), ("uc08", 525, 550), ("uc10", 915, 930), ("uc07x", 1295, 1315)):
        d.edge([(x_out, cy[cid]), (x_bus, cy[cid]), (x_bus, 900), (1410, 900)], src=cid, dst="llm", end="")
    d.edge([(1295, cy["uc15b"]), (1410, 168)], src="uc15b", dst="iw", end="")
    d.edge([(915, cy["uc15a"]), (940, cy["uc15a"]), (940, 216), (1360, 216), (1360, 168), (1410, 168)], src="uc15a", dst="iw", end="")
    d.edge([(1295, cy["uc17"]), (1410, 456)], src="uc17", dst="admin", end="")
    d.edge([(365, 196), (365, 236)], src="uc03", dst="uc06", dashed=True, end="open")
    d.label(377, 220, "«include»", anchor="start")
    d.edge([(365, 706), (365, 666)], src="uc11", dst="uc09", dashed=True, end="open")
    d.label(377, 690, "«extend»", anchor="start")
    d.note(980, 620, 300, ["FYP-2 Final (Iteration 4)", "No new use cases: all seventeen are", "acceptance-tested with 5 to 8 outside",
                           "users (SUS ≥ 68, ≥ 80% task success)."], "plain", id="iter4")
    d.legend(980, 712, [("core", "built and tested"), ("planned", "planned for the column's milestone"),
                        ("line:dashed", "«include» or «extend»"), ("line:solid", "takes part in the use case")], col_w=280)
    d.note(205, 878, 320, ["Analyst: developer and reviewer", "One person until GitHub sign-in (FYP-2 Mid)."], "plain", id="analyst-note")
    return Sheet(
        d, "Structure", "Use Cases / Use Case Diagram",
        "The identifiers are those of the requirements (master plan section 15). The left column holds the eight "
        "use cases built and tested for FYP-1 Mid; the dashed columns hold the use cases planned for FYP-1 Final "
        "(Iteration 2) and FYP-2 Mid (Iteration 3). UC-14 and UC-15 appear twice because they are delivered in two "
        "parts: the LangGraph adapter and evaluation version 0 at FYP-1 Final, then the CrewAI adapter and the "
        "full evaluation at FYP-2 Mid. FYP-2 Final (Iteration 4) adds no use case; it acceptance-tests all "
        "seventeen with outside users. Running a task always includes the automatic analysis (UC-06), and "
        "exporting a report extends reviewing. The language model takes part in running, verifying, fix "
        "suggestion and the planned second opinion; the analysis itself is deterministic.",
        ["docs/plan/master-plan.md", "docs/plan/requirements-trace.md", "apps/web/src/pages"],
        "Curated from the use-case table of the plan; implementation status follows docs/plan/requirements-trace.md "
        "and milestones follow the iteration plan.",
    )
