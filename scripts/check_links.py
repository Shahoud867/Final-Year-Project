#!/usr/bin/env python3
"""Check that relative links in Markdown (and plain href/src in HTML) point at files that exist.

Usage:
    python scripts/check_links.py            # check the whole repo, exit 1 if any link is broken
    python scripts/check_links.py --list     # also print every broken link
    python scripts/check_links.py PATH...    # restrict to files/folders

Skips: external URLs, mailto:, pure #anchors, code fences, inline code, and the vendored/raw data
folders (their READMEs belong to third parties).

Known, accepted exceptions live in scripts/linkcheck-allowlist.txt (one `path::target` per line). They are
counted separately and do not fail the run, so every tolerated broken link is written down and reviewable.
"""
from __future__ import annotations

import os
import re
import sys
from urllib.parse import unquote

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "dist-static"}
SKIP_PREFIXES = ("data/raw/", "dev/datasets/")  # third-party content

MD_LINK = re.compile(r"\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
MD_REF = re.compile(r"^\s{0,3}\[[^\]\n]+\]:\s*<?(\S+?)>?(?:\s+\"[^\"]*\")?\s*$")
HTML_ATTR = re.compile(r"""\b(?:href|src)\s*=\s*"([^"]+)\"""")
INLINE_CODE = re.compile(r"`[^`\n]*`")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def iter_files(roots):
    for root in roots:
        if os.path.isfile(root):
            yield root
            continue
        for dp, dn, fn in os.walk(root):
            rel = os.path.relpath(dp, REPO).replace(os.sep, "/") + "/"
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            if rel.startswith(SKIP_PREFIXES):
                dn[:] = []
                continue
            for f in fn:
                if f.lower().endswith((".md", ".html")):
                    yield os.path.join(dp, f)


def extract(path):
    """Yield (line_no, target) for every checkable link in a file."""
    is_html = path.lower().endswith(".html")
    in_fence = False
    with open(path, encoding="utf-8", errors="replace") as fh:
        for n, line in enumerate(fh, 1):
            if not is_html:
                if line.lstrip().startswith(("```", "~~~")):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                scan = INLINE_CODE.sub("", line)
                for m in MD_LINK.finditer(scan):
                    yield n, m.group(1)
                m = MD_REF.match(scan)
                if m:
                    yield n, m.group(1)
            else:
                for m in HTML_ATTR.finditer(line):
                    t = m.group(1)
                    if any(c in t for c in "${}'+"):  # JS template fragments, not real links
                        continue
                    yield n, t


def resolve(src, target):
    t = target.split("#", 1)[0].split("?", 1)[0]
    if not t or SCHEME.match(target) or target.startswith("#"):
        return None
    t = unquote(t)
    if t.startswith("/"):
        return os.path.normpath(os.path.join(REPO, t.lstrip("/")))
    return os.path.normpath(os.path.join(os.path.dirname(src), t))


def load_allowlist():
    path = os.path.join(os.path.dirname(__file__), "linkcheck-allowlist.txt")
    allowed = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.rstrip(chr(10))
                if line.strip() and not line.lstrip().startswith("#") and "::" in line:
                    f, t = line.split("::", 1)
                    allowed.add((f.strip(), t))
    return allowed


def main(argv):
    show = "--list" in argv
    roots = [a for a in argv if not a.startswith("--")] or [REPO]
    roots = [os.path.abspath(r) for r in roots]
    checked = broken = 0
    problems = []
    for f in sorted(iter_files(roots)):
        for n, target in extract(f):
            dest = resolve(f, target)
            if dest is None:
                continue
            checked += 1
            if not os.path.exists(dest):
                broken += 1
                problems.append((os.path.relpath(f, REPO).replace(os.sep, "/"), n, target))
    allowed = load_allowlist()
    accepted = [p for p in problems if (p[0], p[2]) in allowed]
    real = [p for p in problems if (p[0], p[2]) not in allowed]
    if show or real:
        for f, n, t in (problems if show else real[:50]):
            tag = "accepted" if (f, t) in allowed else "broken"
            print(f"{f}:{n}: {tag} -> {t}")
    print(f"links checked: {checked}; broken: {len(real)}; accepted (allowlisted): {len(accepted)}")
    return 1 if real else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
