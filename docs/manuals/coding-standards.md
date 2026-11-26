# Coding standards

| | |
|---|---|
| Version | 1.0 |
| Date | 2026-10-11 |
| Status | In force. Every rule below is enforced by a tool in CI unless it says "by review". Numbers were measured on this date |
| Covers | Handbook Table 1a, Development Phase: comments, naming conventions, static analysis, unit test suites |

A standard that is only written down is not evidence. Each rule here names the tool that enforces it and the command that proves it.

## 1. Naming

| Thing | Python | TypeScript / React | Enforced by |
|---|---|---|---|
| Functions, variables | `snake_case` | `camelCase` | ruff `N` (PEP 8 naming); typescript-eslint |
| Classes, types, components | `PascalCase` | `PascalCase` | ruff `N`; by review for components |
| Constants | `UPPER_CASE` (`MAX_REPLAYS`, `CONFIRM_MIN_RATE`) | `UPPER_CASE` | ruff `N`; by review |
| Modules, files | `snake_case.py` | `PascalCase.tsx` for components, `camelCase.ts` otherwise | ruff `N999`; by review |
| Private helpers | leading underscore (`_finish`) | not exported | by review |
| Tests | `test_<behaviour>` that reads as a sentence | `it("…")` that reads as a sentence | pytest and vitest collection |
| Documents, evidence | `kebab-case`, date prefix for dated files | | [`check_workspace.py`](../../scripts/check_workspace.py) |

**Domain vocabulary is fixed.** Code, UI, API and documents use the same words: *run, step, check, finding, hypothesis, experiment, replay, verdict, evidence, review*. A finding is never an "issue", "bug" or "case" in code. The words are defined in the [data dictionary](../diagrams/data-dictionary.md).

**One documented exception:** domain exceptions are named for the condition (`ProviderUnavailable`, `IllegalTransition`, `ReplayUnavailable`) and do not end in `Error`, so ruff rule `N818` is switched off in each `pyproject.toml` with that reason next to it.

## 2. Comments and docstrings

| Rule | Enforced by |
|---|---|
| Every public module, class, method and function has a docstring that says what it does or returns | ruff `D100`, `D101`, `D102`, `D103`, `D104`: **0 violations** in the three Python packages (38 modules, about 3,760 lines of code) |
| Comments explain **why**, never restate the code | by review |
| A constant that encodes a design decision cites it (`# VR-1, ADR-006`) | by review |
| Route docstrings are user-facing: they become the description in the generated API documentation at `/docs` | FastAPI |
| System tests carry their specification in the docstring (`ID Title`, `Requirement:`, `Steps:`, `Expected:`) | [`build_test_docs.py`](../../scripts/build_test_docs.py) fails if a field is missing |
| Exported React components and non-obvious functions have a `/** … */` comment | by review |

## 3. Static analysis

| Tool | Scope | Configuration | Gate |
|---|---|---|---|
| **ruff** | all Python: packages, API, scripts, tests | `select = E, F, I, B, C90, UP, N, D100-D104`; line length 120; cyclomatic complexity at most 12 | 0 findings |
| **mypy --strict** | `granite_core`, `refund_desk`, `granite_api` (38 source files) | `strict = true`, pydantic plugin | 0 errors |
| **Architecture check** | `granite_core`, `refund_desk` | [`check_architecture.py`](../../scripts/check_architecture.py): the core imports only the standard library and pydantic, and no network, database or process module; the workflow imports only the core | 0 violations |
| **bandit** | the three packages | medium severity and above | 0 findings |
| **pip-audit**, **npm audit** | dependencies | known vulnerabilities; npm at high and above | 0 findings |
| **gitleaks** | full git history | default rules | 0 secrets |
| **ESLint** | `apps/web/src`, `apps/web/tests` | `typescript-eslint` recommended, `react-hooks`, `no-explicit-any` as an error | 0 findings |
| **TypeScript** | `apps/web` | `strict`, `noUnusedLocals`, `noUnusedParameters`, `noUncheckedIndexedAccess` | 0 errors |
| **Generated-file checks** | trace schema, design pack, test catalogue, requirement trace | each generator has `--check` | no difference |

The plan asked for a complexity limit of 10; the enforced limit is 12, because two functions (the check-expression evaluator and the attribution ranking) are clearer as one function than as fragments. This is recorded in the [change log](../registers/change-log.md).

## 4. Tests

| Level | Where | Tool | What it proves |
|---|---|---|---|
| Unit and property | `packages/granite_core/tests` | pytest, hypothesis | Each algorithm alone: check language, attribution, verdict rule, lifecycle, evidence hashing, redaction, trace |
| Unit and integration | `workflows/refund_desk/tests` | pytest | The five agents, the fault, the source-of-truth store, on recorded model answers |
| Integration | `apps/api/tests` | pytest, FastAPI test client | Every endpoint: one success and at least one failure; validation, limits, security, restart recovery |
| Component and accessibility | `apps/web/tests` | vitest, Testing Library, axe-core | Screens, forms, error states, keyboard use, structure |
| System (black box) | `tests/system` | pytest over real HTTP | The whole product as a separate process; see the [test catalogue](system-test-cases.md) |

Rules: a new behaviour comes with a test; a fixed defect comes with a test that failed before the fix; coverage of `granite_core` and `granite_api` must stay at or above 90% (CI fails below). Tests name the requirement they cover, and [`check_traceability.py`](../../scripts/check_traceability.py) fails if a requirement marked "met" has no test.

**Limit, stated plainly:** the tests and the code were produced in the same AI-assisted sessions. High coverage shows that the code does what was intended; it does not show that the intent is right. Review by a second member is the control for that, and it has not happened yet (see the [repository evidence](../../evidence/repo/)).

## 5. Run every gate locally

```bash
ruff check packages/granite_core workflows/refund_desk apps/api scripts tests
```

```bash
python scripts/check_architecture.py
```

```bash
pytest tests/system
```

The complete list, in the order CI runs it, is in the [setup manual](setup-manual.md). The latest recorded results are in [`evidence/reports/`](../../evidence/reports/).
