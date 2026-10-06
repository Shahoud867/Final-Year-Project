# packages

Reusable libraries (master plan sections 19.2 and 28.1).

| Folder | Content | Owner |
|---|---|---|
| `granite_core/` | pure Python, no web dependencies: trace schema, graph, checks, attribution, verification, redaction. Checks and attribution: Noor. Verification: Saif | Noor / Saif |
| `granite_sdk/` | tracer and framework adapters (LangGraph at Final-1, CrewAI at Mid-2) | Shahoud |

Dependency rule: inner layers never import outer ones (enforced with import-linter in CI).
