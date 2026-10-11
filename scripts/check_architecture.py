"""Check the layer rule of the architecture by reading the imports of every source file (no code is executed).

    python scripts/check_architecture.py

Rules (docs/diagrams/architecture.md, ADR-001):
  granite_core   may import the standard library, pydantic and itself. Nothing else: no web framework, database
                 driver, HTTP client, workflow or application code.
  refund_desk    may import the standard library, granite_core and itself.
  granite_api    may import anything except test code; it is the only layer allowed to touch the network or a database.

Exit code 1 lists every violation with file and line.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYERS: dict[str, tuple[Path, set[str]]] = {
    "granite_core": (ROOT / "packages" / "granite_core" / "granite_core", {"granite_core", "pydantic"}),
    "refund_desk": (ROOT / "workflows" / "refund_desk" / "refund_desk", {"refund_desk", "granite_core"}),
}
# Even from the standard library, the core must not reach the network, a database or a subprocess.
CORE_FORBIDDEN_STDLIB = {"urllib", "http", "socket", "sqlite3", "subprocess", "ftplib", "smtplib", "asyncio"}


def imports_of(path: Path, package: str) -> list[tuple[int, str]]:
    """(line, top-level module) for every absolute import in a file; relative imports stay inside the package."""
    found: list[tuple[int, str]] = []
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            found += [(node.lineno, alias.name.split(".")[0]) for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            found.append((node.lineno, package if node.level else (node.module or "").split(".")[0]))
    return found


def violations(layers: dict[str, tuple[Path, set[str]]] = LAYERS) -> list[str]:
    out: list[str] = []
    for package, (folder, allowed) in layers.items():
        for path in sorted(folder.rglob("*.py")):
            for line, module in imports_of(path, package):
                where = f"{path.relative_to(ROOT).as_posix()}:{line}"
                if module in sys.stdlib_module_names:
                    if package == "granite_core" and module in CORE_FORBIDDEN_STDLIB:
                        out.append(f"{where}: granite_core must not use '{module}' (network, database or process access)")
                elif module not in allowed:
                    out.append(f"{where}: {package} must not import '{module}' (allowed: standard library, {', '.join(sorted(allowed))})")
    return out


def main() -> int:
    bad = violations()
    for b in bad:
        print(b)
    files = sum(1 for folder, _ in LAYERS.values() for _ in folder.rglob("*.py"))
    print(f"architecture check: {len(bad)} violation(s) in {files} files of {', '.join(LAYERS)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
