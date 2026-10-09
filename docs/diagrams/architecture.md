# Architecture

One repository, four packages, one dependency direction (arrows point from the dependent to the dependency). See [ADR-001](../adr/adr-001-modular-monolith.md).

```mermaid
flowchart TB
    web["apps/web: React UI (built into the API image)"]
    api["apps/api: granite_api (HTTP, SQLite or PostgreSQL, background jobs, providers)"]
    wf["workflows/refund_desk: steps, checks, faults, repair rules, retail data"]
    core["packages/granite_core: trace, checks language, attribution, verification, lifecycle, evidence, runner (no web, database or network code)"]
    llm[("Ollama, hosted endpoint, or cassette of recorded answers")]
    db[("SQLite file or PostgreSQL")]
    web -->|HTTP /api| api
    api --> wf
    api --> core
    wf --> core
    api -.->|providers.py| llm
    api -.->|SQLAlchemy| db
```

| Layer | May import | Must not import |
|---|---|---|
| `granite_core` | standard library, pydantic | fastapi, sqlalchemy, httpx, urllib, any workflow |
| `refund_desk` | `granite_core` | the API, any web or database library |
| `granite_api` | core, refund_desk, fastapi, sqlalchemy | UI code |

The rule is checked by what the core's dependency list contains (`pydantic` only) and by its tests running without a network or a database.

## Deployment

Only the first two rows exist today. Nothing is hosted ([deployment record](../registers/deployment-record.md), [ADR-007](../adr/adr-007-free-hosting-render.md)).

```mermaid
flowchart LR
    subgraph laptop["Developer or supervisor machine (works today)"]
        browser["Browser"] --> uvicorn["uvicorn: API plus built UI, SQLite file"]
        uvicorn -.->|optional live mode| ollama["Ollama on the same machine"]
    end
    subgraph compose["docker compose (defined, image not yet built)"]
        c["one container, volume /data for the database, recorded mode by default"]
    end
    subgraph hosted["Free web-service host (planned, not created)"]
        h["same image, recorded mode, optional hosted model key"]
    end
    gh["GitHub Actions: lint, types, tests, security, build, smoke test (written, not yet run)"]
    gh --> compose
    gh --> hosted
```
