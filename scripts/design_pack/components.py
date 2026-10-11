"""Structure design: component diagram (components, the interfaces they provide, and who uses them)."""

from __future__ import annotations

from . import Sheet
from .kit import Diagram


def component_diagram() -> Sheet:
    d = Diagram("component-diagram", "Component diagram", 1500, 730,
                "Run-time components of Granite, the interfaces they provide and the components that use them.")
    # web
    d.frame("web", 30, 60, 260, 230, "apps/web", "web")
    d.node("client", 50, 100, 220, 60, "API client", ["api.ts · waitForJob()"], "web", tip="apps/web/src/api.ts")
    d.node("pages", 50, 200, 220, 60, "Pages and components", ["React, hash routing, no UI library"], "web",
           tip="apps/web/src/pages, apps/web/src/components")
    # api
    d.frame("api", 350, 60, 650, 470, "apps/api (granite_api)", "api")
    d.node("router", 370, 100, 220, 60, "Router and middleware", ["routes.py · main.py", "errors.py (RFC 7807)"], "api")
    d.node("jobs", 370, 200, 220, 60, "Job runner", ["jobs.py: work off the request", "thread, with progress"], "api")
    d.frame("svc", 640, 84, 350, 288, "Services", "api")
    d.node("s-run", 660, 116, 310, 56, "Run and analysis", ["services/runs.py · analysis.py"], "api")
    d.node("s-exp", 660, 206, 310, 56, "Experiment", ["services/experiments.py"], "api")
    d.node("s-rev", 660, 296, 310, 56, "Review and report", ["services/reviews.py · report.py"], "api")
    d.node("repo", 370, 420, 220, 60, "Repository", ["models.py · db.py", "12 tables via SQLAlchemy"], "api")
    d.node("registry", 640, 420, 160, 60, "Workflow registry", ["registry.py"], "api")
    d.node("adapters", 830, 420, 160, 60, "Model adapters", ["providers.py", "llm_factory.py"], "api")
    # core
    d.frame("core", 1090, 60, 380, 440, "packages/granite_core", "core")
    core = [
        ("k-run", "Runner", "run_workflow() · execute_replay()"),
        ("k-chk", "Check engine", "evaluate_checks() · derive_findings()"),
        ("k-att", "Attribution", "attribute() over recorded lineage"),
        ("k-ver", "Verification", "run_experiment() · decide() (VR-1)"),
        ("k-life", "Lifecycle and evidence", "transition() · make_evidence()"),
        ("k-llm", "Model port", "LLMProvider protocol · Cassette"),
    ]
    for i, (cid, title, provides) in enumerate(core):
        d.node(cid, 1110, 96 + 62 * i, 340, 50, title, [provides], "core")
    mid = [96 + 62 * i + 25 for i in range(6)]
    # outside
    d.node("db", 385, 590, 190, 64, "Database", ["SQLite or PostgreSQL"], "store", shape="cyl")
    d.node("refund", 620, 590, 200, 60, "workflows/refund_desk", ["steps, checks, faults, data"], "workflow")
    d.node("model", 850, 590, 180, 60, "Model endpoint", ["Ollama or hosted"], "external")
    d.node("cassette", 1130, 590, 200, 60, "Cassette file", ["recorded answers (JSON)"], "store", shape="doc")
    # connectors: web
    d.edge([(160, 200), (160, 160)], src="pages", dst="client")
    d.edge([(270, 130), (370, 130)], "REST /api · JSON", "client", "router", label_dy=-7)
    # connectors: inside the API
    d.edge([(590, 130), (640, 130)], src="router", dst="svc")
    d.edge([(480, 160), (480, 200)], src="router", dst="jobs")
    d.edge([(590, 230), (640, 230)], src="jobs", dst="svc")
    d.edge([(640, 340), (615, 340), (615, 450), (590, 450)], src="svc", dst="repo")
    d.edge([(720, 372), (720, 420)], src="svc", dst="registry")
    d.edge([(910, 372), (910, 420)], src="svc", dst="adapters")
    # connectors: services use the core (interfaces are named in the core boxes)
    d.edge([(970, 128), (1070, 128), (1070, mid[0]), (1110, mid[0])], src="s-run", dst="k-run")
    d.edge([(970, 144), (1050, 144), (1050, mid[1]), (1110, mid[1])], src="s-run", dst="k-chk")
    d.edge([(970, 160), (1030, 160), (1030, mid[2]), (1110, mid[2])], src="s-run", dst="k-att")
    d.edge([(970, 255), (1050, 255), (1050, mid[3]), (1110, mid[3])], src="s-exp", dst="k-ver")
    d.edge([(970, 340), (1050, 340), (1050, mid[4]), (1110, mid[4])], src="s-rev", dst="k-life")
    d.edge([(990, 450), (1050, 450), (1050, mid[5]), (1110, mid[5])], src="adapters", dst="k-llm", dashed=True, end="tri")
    # connectors: outside
    d.edge([(480, 480), (480, 590)], src="repo", dst="db")
    d.label(492, 545, "SQL", anchor="start")
    d.edge([(720, 480), (720, 590)], src="registry", dst="refund")
    d.label(732, 565, "builds WorkflowDef", anchor="start")
    d.edge([(910, 480), (910, 590)], src="adapters", dst="model")
    d.label(922, 545, "HTTP chat API", anchor="start")
    d.edge([(1230, 456), (1230, 590)], src="k-llm", dst="cassette")
    d.label(1242, 550, "reads and writes", anchor="start")
    d.edge([(720, 650), (720, 690), (1420, 690), (1420, 500)], "imports StepDef, CheckDef, RepairRule",
           "refund", "core", label_at=(1075, 684))
    d.legend(30, 330, [("web", "user interface"), ("api", "application layer"), ("core", "granite_core"),
                       ("workflow", "system under test"), ("store", "data at rest"), ("external", "outside the product"),
                       ("line:solid", "uses / calls"), ("line:dashed", "implements the interface")], col_w=200)
    return Sheet(
        d, "Structure", "Component Diagram",
        "Each box is a deployable or replaceable part. The browser part only knows the REST interface. Inside the "
        "API, the router validates and delegates, the job runner executes long work (a run takes about a minute "
        "with a local model) and reports progress, and three services hold the use cases. Services call the core "
        "through plain functions named in the blue boxes; the core never calls back. Two parts are deliberately "
        "replaceable: the model adapter implements the core's LLMProvider interface, so a local model, a hosted "
        "model or recorded answers can be swapped by configuration, and a workflow is plugged in through the "
        "registry as a WorkflowDef.",
        ["apps/api/granite_api/routes.py", "apps/api/granite_api/services", "apps/api/granite_api/jobs.py",
         "apps/api/granite_api/registry.py", "apps/api/granite_api/providers.py", "packages/granite_core/granite_core",
         "apps/web/src/api.ts"],
        "Curated layout. Every arrow from a service to a core component corresponds to an import that the generated "
        "call graph shows function by function.",
    )
