#!/usr/bin/env python3
"""Regenerate docs/workspace-index.md: one line per file (path and title), grouped by top-level folder.

The index is generated, never edited by hand. Titles come from the first Markdown heading, the HTML <title>,
or the first line of a Python module docstring. data/raw/ is summarised per dataset (about 1,100 files).

Usage:  python scripts/build_index.py
"""
from __future__ import annotations

import ast
import datetime
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
OUT = os.path.join(REPO, "docs", "workspace-index.md")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist"}
STATE = {
    "docs": "active", "research": "active", "data": "active (raw/ read-only)", "apps": "active (code)",
    "packages": "active (code)", "workflows": "active (code)", "tests": "active (code)", "scripts": "active (code)",
    "references": "read-only reference", "deliverables": "frozen records per stage", "evidence": "append-only",
    "archive": "history", ".claude": "tool configuration", "(root)": "entry points",
}


def title_of(path: str) -> str:
    low = path.lower()
    try:
        if low.endswith(".md"):
            with open(path, encoding="utf-8", errors="replace") as fh:
                first = ""
                for line in fh:
                    s = line.strip()
                    if s.startswith("# "):
                        return s[2:].strip()
                    if s and not first and not s.startswith(("---", "|", "<")):
                        first = s
                return first[:110]
        if low.endswith(".html"):
            with open(path, encoding="utf-8", errors="replace") as fh:
                m = re.search(r"<title>(.*?)</title>", fh.read(20000), re.S | re.I)
            return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        if low.endswith(".py"):
            with open(path, encoding="utf-8", errors="replace") as fh:
                doc = ast.get_docstring(ast.parse(fh.read()))
            return (doc or "").strip().splitlines()[0][:110] if doc else ""
    except (OSError, SyntaxError, ValueError):
        return ""
    return ""


def collect():
    groups: dict[str, list[tuple[str, str]]] = {}
    raw_summary: dict[str, list[int]] = {}
    for dp, dn, fn in os.walk(REPO):
        dn[:] = sorted(d for d in dn if d not in SKIP_DIRS)
        rel_dir = os.path.relpath(dp, REPO).replace(os.sep, "/")
        rel_dir = "" if rel_dir == "." else rel_dir
        for f in sorted(fn):
            rel = f"{rel_dir}/{f}" if rel_dir else f
            if rel == "docs/workspace-index.md":
                continue
            if rel.startswith("data/raw/"):
                ds = rel.split("/")[2] if rel.count("/") >= 3 else "(files)"
                size = os.path.getsize(os.path.join(dp, f))
                s = raw_summary.setdefault(ds, [0, 0])
                s[0] += 1
                s[1] += size
                continue
            top = rel.split("/")[0] if "/" in rel else "(root)"
            groups.setdefault(top, []).append((rel, title_of(os.path.join(dp, f))))
    for ds, (n, size) in sorted(raw_summary.items()):
        groups.setdefault("data", []).append((f"data/raw/{ds}/", f"third-party dataset: {n} files, {size / 1e6:.1f} MB (not listed per file)"))
    return groups


def main():
    groups = collect()
    total = sum(len(v) for v in groups.values())
    lines = [
        "# Workspace index (generated)",
        "",
        f"Generated {datetime.date.today().isoformat()} by `python scripts/build_index.py`. **Do not edit by hand.** "
        "One line per file (path and title); `data/raw/` is summarised per dataset. Layout and naming rules: "
        "[`workspace-guide.md`](workspace-guide.md). Old paths: [`archive/migration-map_2026-10-06.tsv`](../archive/migration-map_2026-10-06.tsv).",
        "",
        f"Entries: {total}",
        "",
    ]
    order = ["(root)", "docs", "research", "data", "apps", "packages", "workflows", "tests", "scripts", "references",
             "deliverables", "evidence", "archive", ".claude"]
    for top in order + sorted(set(groups) - set(order)):
        if top not in groups:
            continue
        lines += [f"## {top}  ({STATE.get(top, '')})" if top != "(root)" else "## (repository root)", "",
                  "| Path | Title / description |", "|---|---|"]
        for rel, title in sorted(groups[top], key=lambda x: x[0].lower()):
            lines.append(f"| `{rel}` | {title.replace('|', '/')} |")
        lines.append("")
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))
    print(f"wrote {os.path.relpath(OUT, REPO)}: {total} entries")


if __name__ == "__main__":
    sys.exit(main())
