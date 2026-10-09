#!/usr/bin/env python3
"""Check the workspace against docs/workspace-guide.md.

Checks
  1. Only the agreed top-level folders and files exist.
  2. Required README.md files exist.
  3. Naming rules (guide section 4) outside the exempt areas.

Exempt from naming rules (guide section 4.4): archive/, data/raw/, deliverables/stage-0-proposal/,
docs/report/ (the prescribed LaTeX template keeps its own file names), and the legacy poc_spike*
files in research/spikes/. Code folders are only checked for spaces and parentheses.

Usage:  python scripts/check_workspace.py        exit code 1 if anything is wrong
"""
from __future__ import annotations

import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

TOP_DIRS = {".claude", ".git", ".github", "apps", "archive", "data", "deliverables", "docs", "evidence",
            "packages", "references", "research", "scripts", "tests", "workflows"}
TOP_FILES = {"README.md", "CLAUDE.md", "LICENSE", "CHANGELOG.md", "CODEOWNERS", "Dockerfile", "docker-compose.yml",
             "pyproject.toml", ".gitignore", ".gitattributes", ".mailmap", ".editorconfig", ".env.example",
             ".dockerignore"}
REQUIRED_READMES = ["apps", "archive", "data", "deliverables", "evidence", "packages", "references", "research",
                    "scripts", "tests", "workflows", "docs/report", "docs/diagrams", "docs/adr", "docs/manuals",
                    "docs/meetings", "docs/registers", "research/eval", "references/papers"]
REQUIRED_FILES = ["docs/workspace-guide.md", "docs/plan/master-plan.md"]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", ".ruff_cache", ".mypy_cache", ".pytest_cache"}
EXEMPT = ("archive/", "data/raw/", "deliverables/stage-0-proposal/", "docs/report/")
CODE = ("apps/", "packages/", "workflows/", "tests/", "scripts/", ".github/")
META_OK = {"README.md", "CLAUDE.md", "CHANGELOG.md", "LICENSE", "LICENSE.txt", "DOWNLOAD.md", ".gitignore", ".gitkeep",
           "CODEOWNERS", "Dockerfile"}

KEBAB = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
ADR = re.compile(r"^adr-\d{3}-[a-z0-9-]+\.md$")
MEETING = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-z0-9-]+\.md$")
EVIDENCE = re.compile(r"^\d{4}-\d{2}-\d{2}_[a-z0-9._-]+$")
PAPER = re.compile(r"^\d{4}_[a-z-]+_[a-z0-9-]+\.pdf$")
DELIVERABLE = re.compile(r"^granite_[a-z0-9-]+_[a-z0-9-]+_(v\d+\.\d+|draft)\.[a-z0-9]+$")
BAD_CHARS = re.compile(r"[ ()]")


def violations():
    out = []
    for name in sorted(os.listdir(REPO)):
        full = os.path.join(REPO, name)
        if os.path.isdir(full) and name not in TOP_DIRS and name not in SKIP_DIRS:
            out.append((name + "/", "top-level folder not in the guide (section 2); change the guide first (section 9)"))
        if os.path.isfile(full) and name not in TOP_FILES:
            out.append((name, "unexpected file at the repository root"))
    for d in REQUIRED_READMES:
        if not os.path.isfile(os.path.join(REPO, d, "README.md")):
            out.append((d + "/README.md", "required README is missing"))
    stages = os.path.join(REPO, "deliverables")
    if os.path.isdir(stages):
        for s in sorted(os.listdir(stages)):
            if os.path.isdir(os.path.join(stages, s)) and not os.path.isfile(os.path.join(stages, s, "README.md")):
                out.append((f"deliverables/{s}/README.md", "required README is missing"))
    for f in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(REPO, f)):
            out.append((f, "required file is missing"))

    for dp, dn, fn in os.walk(REPO):
        rel_dir = os.path.relpath(dp, REPO).replace(os.sep, "/")
        rel_dir = "" if rel_dir == "." else rel_dir + "/"
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        if rel_dir.startswith(("data/raw/", "archive/")):
            dn[:] = []
            continue
        for name, is_dir in [(d, True) for d in dn] + [(f, False) for f in fn]:
            rel = rel_dir + name
            if rel.startswith(EXEMPT) or rel + "/" in ("data/raw/", "archive/", "deliverables/stage-0-proposal/", "docs/report/"):
                continue
            if BAD_CHARS.search(name):
                out.append((rel, "name contains a space or parenthesis"))
                continue
            if name.startswith("."):
                continue  # tool files and folders (.claude, .github, .gitignore, ...)
            if rel.startswith(CODE) or rel in ("scripts", "apps", "packages", "workflows", "tests"):
                continue
            if rel.startswith("research/spikes/") and (name.startswith("poc_spike") or name == "whowhen_data" or rel_dir.startswith("research/spikes/whowhen_data/")):
                continue
            if name in META_OK:
                continue
            if rel_dir == "docs/adr/" and not is_dir and not ADR.match(name):
                out.append((rel, "ADR files are named adr-NNN-slug.md"))
            elif rel_dir == "docs/meetings/" and not is_dir and not MEETING.match(name):
                out.append((rel, "meeting files are named YYYY-MM-DD_slug.md"))
            elif rel_dir.startswith("evidence/") and rel_dir.count("/") == 2 and not is_dir and not EVIDENCE.match(name):
                out.append((rel, "evidence files are named YYYY-MM-DD_slug.ext"))
            elif rel_dir == "references/papers/" and not is_dir and not PAPER.match(name):
                out.append((rel, "papers are named YYYY_venue_shortname.pdf"))
            elif re.match(r"deliverables/stage-[1-4]-[a-z0-9-]+/$", rel_dir) and not is_dir and not DELIVERABLE.match(name):
                out.append((rel, "deliverables are named granite_<artifact>_<stage>_v<X.Y>.<ext> or ..._draft.<ext>"))
            elif not KEBAB.match(name) and rel_dir not in ("deliverables/",):
                out.append((rel, "use lowercase-kebab-case (guide section 4.1)"))
    return out


def main():
    bad = violations()
    for path, why in bad:
        print(f"{path}: {why}")
    print(f"workspace check: {len(bad)} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
