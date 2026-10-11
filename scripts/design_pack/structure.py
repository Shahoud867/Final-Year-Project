"""Structure design: layer diagram, component diagram, domain model, structure chart."""

from __future__ import annotations

from . import Sheet
from .kit import Diagram


# ---------------------------------------------------------------------------------------------------------
def layer_diagram() -> Sheet:
    d = Diagram("layer-diagram", "Layer diagram", 1400, 736,
                "Four layers of Granite and the only dependencies allowed between them.")
    ya, yb, y3 = 232, 334, 458  # application row A, row B, domain band
    # presentation
    d.frame("L1", 30, 50, 1060, 104, "Presentation layer: apps/web (React, TypeScript)", "web")
    d.node("pages", 55, 82, 320, 56, "Pages", ["Home · NewRun · RunDetail · FindingDetail"], "web",
           tip="apps/web/src/pages/")
    d.node("comps", 400, 82, 320, 56, "Components", ["Graph · Verify · Outcome · Filters · ui"], "web",
           tip="apps/web/src/components/")
    d.node("client", 745, 82, 320, 56, "API client", ["api.ts: typed requests, readable errors"], "web",
           tip="apps/web/src/api.ts")
    # application
    d.frame("L2", 30, 200, 1060, yb + 58 + 20 - 200, "Application layer: apps/api (granite_api, FastAPI)", "api")
    d.node("http", 55, ya, 320, 58, "HTTP boundary", ["main.py middleware · routes.py", "schemas.py · errors.py"], "api")
    d.node("services", 400, ya, 320, 58, "Services", ["runs · analysis · experiments", "reviews · report · views"], "api")
    d.node("jobs", 745, ya, 320, 58, "Background jobs", ["jobs.py: thread pool, progress,", "recovery after a restart"], "api")
    d.node("config", 55, yb, 320, 58, "Configuration", ["config.py: environment variables", "registry.py: workflows offered"], "api")
    d.node("adapters", 400, yb, 320, 58, "Model adapters", ["providers.py: Ollama, OpenAI-compatible", "llm_factory.py: live or recorded"], "api")
    d.node("persist", 745, yb, 320, 58, "Persistence", ["models.py: 12 tables (SQLAlchemy)", "db.py: engine and sessions"], "api")
    l2_bottom = yb + 58 + 20
    # domain
    d.frame("L3a", 30, y3, 310, 176, "Domain: system under test", "workflow")
    d.node("refund", 50, y3 + 36, 270, 122, "workflows/refund_desk",
           ["definition.py: 5 steps, 7 checks,", "repair rules", "steps.py · faults.py · store.py", "prompts/ (versioned)"], "workflow")
    d.frame("L3b", 390, y3, 700, 176, "Domain: packages/granite_core (pure Python)", "core")
    xs, w = (410, 635, 860), 210
    d.node("c-run", xs[0], y3 + 34, w, 52, "Run and trace", ["runner.py · trace.py"], "core")
    d.node("c-chk", xs[1], y3 + 34, w, 52, "Checks", ["dsl.py · checks.py"], "core")
    d.node("c-llm", xs[2], y3 + 34, w, 52, "Model port", ["llm.py: LLMProvider, Cassette"], "core")
    d.node("c-ver", xs[0], y3 + 104, w, 52, "Verify", ["verification.py · experiment.py"], "core")
    d.node("c-life", xs[1], y3 + 104, w, 52, "Lifecycle and evidence", ["lifecycle.py · evidence.py"], "core")
    d.node("c-att", xs[2], y3 + 104, w, 52, "Trace back", ["lineage.py · attribution.py"], "core")
    # outside the product
    d.node("browser", 1150, 74, 220, 56, "Analyst's browser", ["loads the built UI"], "external")
    d.node("model", 1150, ya, 220, 58, "Language model", ["Ollama (local) or a hosted", "OpenAI-compatible endpoint"], "external")
    d.node("db", 1150, yb - 4, 220, 66, "Database", ["SQLite file (default)", "or PostgreSQL URL"], "store", shape="cyl")
    d.node("cassette", 1150, y3 + 34, 220, 52, "Cassette file", ["recorded model answers (JSON)"], "store", shape="doc")
    d.node("snapshot", 50, y3 + 208, 270, 46, "Retail data snapshot", ["data/seed/taubench_retail_v1"], "store", shape="doc")
    d.note(1150, y3 + 104, 220, ["Dependency rule", "granite_core imports only the", "standard library and pydantic.", "Checked on every push by", "scripts/check_architecture.py"], "warn", id="rule")
    # dependencies
    d.edge([(1150, 102), (1090, 102)], "runs", "browser", "L1", label_dy=-7)
    d.edge([(560, 154), (560, 200)], src="L1", dst="L2")
    d.label(572, 181, "HTTP + JSON on /api/*", anchor="start")
    d.edge([(185, l2_bottom), (185, y3)], src="L2", dst="L3a")
    d.label(197, y3 - 19, "builds WorkflowDef", anchor="start")
    d.edge([(470, l2_bottom), (470, y3)], src="L2", dst="L3b")
    d.label(458, y3 - 19, "calls pure functions", anchor="end")
    d.edge([(340, y3 + 88), (390, y3 + 88)], src="L3a", dst="L3b")
    d.label(365, y3 + 80, "imports")
    d.edge([(590, yb + 58), (590, y3 - 22), (965, y3 - 22), (965, y3 + 34)], "implements LLMProvider", "adapters", "c-llm",
           dashed=True, end="tri", label_at=(790, y3 - 28))
    d.edge([(1065, yb + 29), (1150, yb + 29)], "SQL", "persist", "db", label_dy=-7)
    d.edge([(560, yb), (560, yb - 22), (1120, yb - 22), (1120, ya + 29), (1150, ya + 29)], "HTTP chat API", "adapters", "model",
           label_at=(900, yb - 28))
    d.edge([(1070, y3 + 60), (1150, y3 + 60)], "JSON", "c-llm", "cassette", label_dy=-7)
    d.edge([(185, y3 + 158), (185, y3 + 208)], src="refund", dst="snapshot")
    d.label(197, y3 + 190, "reads", anchor="start")
    return Sheet(
        d, "Structure", "Layer Diagram",
        "Granite has four layers and dependencies point downward only. The web UI talks to the API over HTTP and "
        "knows nothing about the engine. The API layer owns everything with side effects (HTTP, database, threads, "
        "network calls to a model). The domain layer is split in two: the Refund Desk workflow (the system being "
        "investigated) and granite_core, which decides what is wrong, where it began and whether a diagnosis is "
        "proven. The core has no web, database or network code, which is why its 207 tests run in seconds; the API "
        "plugs a model into it by implementing the core's LLMProvider interface (dependency inversion).",
        ["apps/web/src", "apps/api/granite_api", "workflows/refund_desk/refund_desk", "packages/granite_core/granite_core",
         "docs/adr/adr-001-modular-monolith.md"],
        "Layout is curated. The dependency rule it shows is enforced mechanically by scripts/check_architecture.py.",
    )
