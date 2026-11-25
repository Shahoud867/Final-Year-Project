"""Structure design: component diagram (components, the interfaces they provide, and who uses them)."""

from __future__ import annotations

from . import Sheet
from .kit import Diagram


def component_diagram() -> Sheet:
    d = Diagram("component-diagram", "Component diagram", 1500, 840,
                "Run-time components of Granite, the interfaces they provide, the components that use them, and the "
                "components planned for FYP-1 Final and FYP-2.")
    # web
    d.frame("web", 30, 60, 260, 330, "apps/web", "web")
    d.node("client", 50, 100, 220, 60, "API client", ["api.ts · waitForJob()"], "web", tip="apps/web/src/api.ts")
    d.node("pages", 50, 200, 220, 60, "Pages and components", ["React, hash routing, no UI library"], "web",
           tip="apps/web/src/pages, apps/web/src/components")
    d.node("screens", 50, 300, 220, 60, "Planned screens", ["check editor, evaluation,", "known fixes, API keys"], "planned", dashed=True)
    # api
    d.frame("api", 350, 60, 650, 600, "apps/api (granite_api)", "api")
    d.node("router", 370, 100, 220, 60, "Router and middleware", ["routes.py · main.py", "errors.py (RFC 7807)"], "api")
    d.node("jobs", 370, 200, 220, 60, "Job runner", ["jobs.py: work off the request", "thread, with progress"], "api")
    d.frame("svc", 640, 84, 350, 468, "Services", "api")
    d.node("s-run", 660, 116, 310, 56, "Run and analysis", ["services/runs.py · analysis.py"], "api")
    d.node("s-exp", 660, 206, 310, 56, "Experiment", ["services/experiments.py"], "api")
    d.node("s-rev", 660, 296, 310, 56, "Review and report", ["services/reviews.py · report.py"], "api")
    d.node("s-ingest", 660, 386, 310, 56, "Ingest and accounts", ["trace files, SDK events (FYP-1 Final);", "sign-in, API keys (FYP-2 Mid)"],
           "planned", dashed=True)
    d.node("s-eval", 660, 476, 310, 56, "Evaluation and fixes", ["Fault Lab, fix suggestion (FYP-1 Final);", "known fixes (FYP-2 Mid)"],
           "planned", dashed=True)
    d.node("repo", 370, 580, 220, 60, "Repository", ["models.py · db.py", "12 tables via SQLAlchemy"], "api")
    d.node("registry", 640, 580, 160, 60, "Workflow registry", ["registry.py"], "api")
    d.node("adapters", 830, 580, 160, 60, "Model adapters", ["providers.py", "llm_factory.py"], "api")
    # core
    d.frame("core", 1090, 60, 380, 540, "packages/granite_core", "core")
    core = [
        ("k-run", "Runner", "run_workflow() · execute_replay()", False),
        ("k-chk", "Check engine", "evaluate_checks() · derive_findings()", False),
        ("k-att", "Attribution", "attribute() over recorded lineage", False),
        ("k-ver", "Verification", "run_experiment() · decide() (VR-1)", False),
        ("k-life", "Lifecycle and evidence", "transition() · make_evidence()", False),
        ("k-eval", "Fault Lab and evaluation", "benchmark, baselines · FYP-1 Final", True),
        ("k-second", "Second opinion", "LLM hypothesis, unverified · FYP-2 Mid", True),
        ("k-llm", "Model port", "LLMProvider protocol · Cassette", False),
    ]
    for i, (cid, title, provides, planned) in enumerate(core):
        d.node(cid, 1110, 96 + 62 * i, 340, 50, title, [provides], "planned" if planned else "core", dashed=planned)
    mid = [96 + 62 * i + 25 for i in range(len(core))]
    # outside
    d.node("sdkapp", 30, 700, 260, 60, "App with the Granite SDK", ["LangGraph: FYP-1 Final · CrewAI: FYP-2 Mid"], "planned", dashed=True)
    d.node("db", 385, 700, 190, 64, "Database", ["SQLite or PostgreSQL"], "store", shape="cyl")
    d.node("refund", 620, 700, 200, 60, "workflows/refund_desk", ["steps, checks, faults, data"], "workflow")
    d.node("model", 850, 700, 180, 60, "Model endpoint", ["Ollama or hosted"], "external")
    d.node("cassette", 1130, 700, 200, 60, "Cassette file", ["recorded answers (JSON)"], "store", shape="doc")
    d.node("second-wf", 1350, 700, 140, 60, "Second workflow", ["GSM8K · FYP-1 Final"], "planned", dashed=True)
    # connectors: web
    d.edge([(160, 200), (160, 160)], src="pages", dst="client")
    d.edge([(270, 130), (370, 130)], "REST /api · JSON", "client", "router", label_dy=-7)
    d.edge([(290, 730), (320, 730), (320, 145), (370, 145)], src="sdkapp", dst="router", dashed=True)
    d.label(296, 722, "traces", anchor="start")
    # connectors: inside the API
    d.edge([(590, 130), (640, 130)], src="router", dst="svc")
    d.edge([(480, 160), (480, 200)], src="router", dst="jobs")
    d.edge([(590, 230), (640, 230)], src="jobs", dst="svc")
    d.edge([(640, 340), (615, 340), (615, 610), (590, 610)], src="svc", dst="repo")
    d.edge([(720, 552), (720, 580)], src="svc", dst="registry")
    d.edge([(910, 552), (910, 580)], src="svc", dst="adapters")
    # connectors: services use the core (interfaces are named in the core boxes)
    d.edge([(970, 128), (1070, 128), (1070, mid[0]), (1110, mid[0])], src="s-run", dst="k-run")
    d.edge([(970, 144), (1050, 144), (1050, mid[1]), (1110, mid[1])], src="s-run", dst="k-chk")
    d.edge([(970, 160), (1030, 160), (1030, mid[2]), (1110, mid[2])], src="s-run", dst="k-att")
    d.edge([(970, 255), (1050, 255), (1050, mid[3]), (1110, mid[3])], src="s-exp", dst="k-ver")
    d.edge([(970, 340), (1050, 340), (1050, mid[4]), (1110, mid[4])], src="s-rev", dst="k-life")
    d.edge([(970, 490), (1050, 490), (1050, mid[5]), (1110, mid[5])], src="s-eval", dst="k-eval", dashed=True)
    d.edge([(970, 520), (1030, 520), (1030, mid[6]), (1110, mid[6])], src="s-eval", dst="k-second", dashed=True)
    d.edge([(990, 610), (1050, 610), (1050, mid[7]), (1110, mid[7])], src="adapters", dst="k-llm", dashed=True, end="tri")
    # connectors: outside
    d.edge([(480, 640), (480, 700)], src="repo", dst="db")
    d.label(492, 675, "SQL", anchor="start")
    d.edge([(720, 640), (720, 700)], src="registry", dst="refund")
    d.label(732, 675, "builds WorkflowDef", anchor="start")
    d.edge([(910, 640), (910, 700)], src="adapters", dst="model")
    d.label(922, 675, "HTTP chat API", anchor="start")
    d.edge([(1230, 580), (1230, 700)], src="k-llm", dst="cassette")
    d.label(1242, 650, "reads and writes", anchor="start")
    d.edge([(720, 760), (720, 800), (1340, 800), (1340, 600)], "imports StepDef, CheckDef, RepairRule",
           "refund", "core", label_at=(1030, 794))
    d.legend(30, 420, [("web", "user interface"), ("api", "application layer"), ("core", "granite_core"),
                       ("workflow", "system under test"), ("store", "data at rest"), ("external", "outside the product"),
                       ("planned", "planned (milestone in the box)"), ("line:solid", "uses / calls"),
                       ("line:dashed", "implements / planned use")], col_w=230)
    return Sheet(
        d, "Structure", "Component Diagram",
        "Each box is a deployable or replaceable part. The browser part only knows the REST interface. Inside the "
        "API, the router validates and delegates, the job runner executes long work (a run takes about a minute "
        "with a local model) and reports progress, and three services hold the use cases. Services call the core "
        "through plain functions named in the blue boxes; the core never calls back. Two parts are deliberately "
        "replaceable: the model adapter implements the core's LLMProvider interface, so a local model, a hosted "
        "model or recorded answers can be swapped by configuration, and a workflow is plugged in through the "
        "registry as a WorkflowDef. Dashed parts are planned: an application instrumented with the SDK sends traces "
        "to the router, two new services handle ingest, accounts, evaluation and fixes, and the core gains Fault "
        "Lab and evaluation (FYP-1 Final) and the LLM second opinion (FYP-2 Mid). The second workflow plugs in "
        "through the same registry.",
        ["apps/api/granite_api/routes.py", "apps/api/granite_api/services", "apps/api/granite_api/jobs.py",
         "apps/api/granite_api/registry.py", "apps/api/granite_api/providers.py", "packages/granite_core/granite_core",
         "apps/web/src/api.ts"],
        "Curated layout. Every solid arrow from a service to a core component corresponds to an import that the "
        "generated call graph shows function by function.",
    )
