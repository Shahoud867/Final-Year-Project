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
    d.edge([(57 + lx["analyst"][1] / 2 - 7, 95), n[0].top()], src="start", dst="a0")
    for a, b in zip(n, n[1:], strict=False):
        flow(a, b)
    d.edge([n[3].right(), m1.left()], src="a3", dst="m1", start="arrow")
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
        "opened?' is where a clean run ends; there is no path from a clean run to a review.",
        ["apps/web/src/pages", "apps/api/granite_api/routes.py", "apps/api/granite_api/jobs.py",
         "apps/api/granite_api/services", "packages/granite_core/granite_core"],
        "Curated. The activities are the modules of the structure chart and the messages of the two sequence diagrams.",
    )


def deployment_diagram() -> Sheet:
    d = Diagram("deployment-diagram", "Deployment diagram", 1420, 600,
                "Where Granite runs today, what the pipeline builds, and what is prepared but not yet deployed.")
    d.frame("laptop", 30, 60, 430, 400, "«device» Team laptop", "plain", note="verified")
    d.node("browser", 60, 100, 170, 54, "Browser", ["the built React UI"], "web")
    d.node("uvicorn", 60, 200, 370, 64, "«process» uvicorn: granite_api", ["port 8000 · serves /api and the web bundle", "started from apps/api (setup manual, section 3)"], "api")
    d.node("sqlite", 60, 320, 170, 74, "SQLite file", ["apps/api/.granite/", "granite.db"], "store", shape="cyl")
    d.node("ollama", 260, 320, 170, 66, "«process» Ollama", ["optional · port 11434", "llama3.2:3b, live mode"], "external")
    d.frame("github", 500, 60, 430, 400, "«cloud» GitHub", "plain", note="verified on every push")
    d.node("repo", 530, 100, 370, 54, "Repository", ["Shahoud867/Final-Year-Project · branch main"], "store")
    d.node("ci", 530, 200, 370, 92, "«pipeline» GitHub Actions: CI", ["Python: lint, types, tests, security scans",
                                                                       "Web: lint, types, tests, build · secret scan", "Container: build image, smoke test inside it"], "api")
    d.node("image", 530, 340, 370, 64, "«artifact» Container image", ["Dockerfile: API + built UI + recorded answers", "runs as a non-root user, health check"], "core")
    d.frame("render", 970, 60, 420, 400, "«cloud» Render free web service", "planned", dashed=True, note="planned, not created")
    d.node("visitor", 1000, 100, 360, 54, "Supervisor's browser", ["public URL over HTTPS"], "planned", dashed=True)
    d.node("container", 1000, 200, 360, 64, "«container» granite-demo", ["recorded mode · port 8000 · /api/health", "defined in render.yaml"], "planned", dashed=True)
    d.node("tmpdisk", 1000, 320, 170, 74, "Temporary disk", ["SQLite; resets on", "restart or deploy"], "planned", shape="cyl", dashed=True)
    d.edge([(145, 154), (145, 200)], src="browser", dst="uvicorn")
    d.label(157, 182, "HTTP :8000", anchor="start")
    d.edge([(145, 264), (145, 320)], src="uvicorn", dst="sqlite")
    d.label(157, 296, "file", anchor="start")
    d.edge([(345, 264), (345, 320)], src="uvicorn", dst="ollama")
    d.label(357, 296, "HTTP", anchor="start")
    d.edge([(460, 127), (530, 127)], "git push", "laptop", "repo", label_dy=-7)
    d.edge([(715, 154), (715, 200)], src="repo", dst="ci")
    d.label(727, 182, "push or pull request", anchor="start")
    d.edge([(715, 292), (715, 340)], src="ci", dst="image")
    d.label(727, 320, "docker build", anchor="start")
    d.edge([(900, 372), (950, 372), (950, 232), (1000, 232)], src="image", dst="container", dashed=True)
    d.label(950, 478, "deploy from render.yaml: a manual step that has not been done yet")
    d.edge([(1180, 154), (1180, 200)], src="visitor", dst="container", dashed=True)
    d.label(1192, 182, "HTTPS", anchor="start")
    d.edge([(1085, 264), (1085, 320)], src="container", dst="tmpdisk", dashed=True)
    d.legend(30, 490, [("api", "running Granite process"), ("core", "build artefact"), ("store", "data at rest"), ("external", "optional service"),
                       ("planned", "prepared, not deployed"), ("line:dashed", "planned connection")], cols=3, col_w=215)
    d.note(720, 490, 670, ["Honest status (2026-10-11)", "Left and middle are verified: the laptop run was exercised in a browser and by the smoke test, and",
                           "CI built the image and ran the smoke test inside it. The right side is only prepared: nobody has",
                           "created the Render service, so there is no public URL yet."], "warn", id="status")
    return Sheet(
        d, "Deployment", "Deployment Diagram",
        "There is one deployable unit: a container image that holds the API, the built web UI and the recorded "
        "model answers, so it runs with no model server and no key. Today that software runs in two verified "
        "places: on a team laptop as a single uvicorn process, and inside GitHub Actions, where every push "
        "builds the image and runs an end-to-end smoke test in it. A hosted copy on a free web service is "
        "prepared (render.yaml) but has not been created; the dashed elements show that plan and must not be "
        "read as existing.",
        ["Dockerfile", "docker-compose.yml", "render.yaml", ".github/workflows/ci.yml", "docs/registers/deployment-record.md",
         "evidence/repo/2026-10-09_ci-run-37924480165.md"],
        "Curated. Ports, modes and file locations are the defaults in apps/api/granite_api/config.py and the Dockerfile.",
    )


def use_case_diagram() -> Sheet:
    d = Diagram("use-case-diagram", "Use-case diagram (Mid-1 scope)", 1240, 660,
                "What an analyst can do with Granite today, and the use cases planned for later milestones.")
    d.frame("system", 250, 50, 720, 580, "Granite", "plain")
    d.actor("analyst", 70, 250, "Analyst")
    d.actor("llm", 1080, 180, "Language model")
    cases = [
        ("uc03", 290, 90, "UC-03  Run a workflow task", "with an optional injected fault", "core"),
        ("uc05", 290, 180, "UC-05  Inspect a run", "graph, steps, check results", "core"),
        ("uc07", 290, 270, "UC-07  Investigate a finding", "ranked origin hypotheses", "core"),
        ("uc08", 290, 360, "UC-08  Verify a hypothesis", "controlled replay, verdict", "core"),
        ("uc09", 290, 450, "UC-09  Review a finding", "accept, reject, ask for information", "core"),
        ("uc12", 290, 540, "UC-12  Browse and search history", "filters by severity and level", "core"),
    ]
    for cid, x, y, title, line, kind in cases:
        d.node(cid, x, y, 300, 62, title, [line], kind, shape="pill")
        d.edge([(130, 290), (290, y + 31)], src="analyst", dst=cid, end="")
    d.node("uc06", 650, 90, 290, 62, "UC-06  Analyse the run", ["checks, findings, hypotheses"], "core", shape="pill")
    d.node("uc11", 650, 450, 290, 62, "UC-11  Export a report", ["Markdown and JSON"], "core", shape="pill")
    d.node("later", 650, 250, 290, 100, "Planned for later milestones", ["UC-01/02 configure, edit checks", "UC-04 import a trace · UC-10 suggest a fix",
                                                                            "UC-13/14 benchmark, evaluation", "UC-15 SDK · UC-16/17 reuse, administer"], "planned", dashed=True)
    d.edge([(590, 121), (650, 121)], "«include»", "uc03", "uc06", dashed=True, end="open", label_dy=-7)
    d.edge([(590, 481), (650, 481)], "«extend»", "uc11", "uc09", dashed=True, start="open", end="", label_dy=-7)
    d.edge([(940, 121), (1080, 215)], src="uc06", dst="llm", end="")
    d.edge([(590, 391), (620, 391), (620, 220), (1000, 220), (1080, 225)], src="uc08", dst="llm", end="")
    d.note(990, 440, 230, ["Mid-1 scope", "Solid use cases are implemented", "and tested. The reviewer and the", "developer are the same person at",
                           "this stage (no accounts yet)."], "plain", id="scope")
    return Sheet(
        d, "Structure", "Use Cases / Use Case Diagram",
        "The identifiers are those of the requirements (master plan section 15). Eight use cases are implemented "
        "for Mid-1; the dashed box lists the ones deliberately left for later. Running a task always includes "
        "the automatic analysis (UC-06), which is why a finding appears without a separate request. Exporting a "
        "report extends reviewing: it is offered on the finding page at any time. The language model is a "
        "secondary actor in exactly two use cases, running and verifying.",
        ["docs/plan/master-plan.md", "docs/plan/requirements-trace.md", "apps/web/src/pages"],
        "Curated from the use-case table of the plan; implementation status follows docs/plan/requirements-trace.md.",
    )
