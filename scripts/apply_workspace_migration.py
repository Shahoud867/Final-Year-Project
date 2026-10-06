#!/usr/bin/env python3
"""Apply the 2026-10-06 workspace migration. Idempotent and non-destructive.

Reads archive/migration-map_2026-10-06.tsv, moves every file that is still at an OLD path to its NEW path,
then rewrites relative Markdown / HTML links inside the files it moved so they keep resolving.

  * Never overwrites: if the destination exists with different content the file is reported and left alone.
  * Never deletes files (empty old folders are removed).
  * Does not touch git. Run it, then review `git status` yourself.
  * Safe to re-run after `git merge origin/noor`: files that arrive at old paths are moved too.
    Once that has been done, this script has served its purpose and can be deleted.

usage:
    python scripts/apply_workspace_migration.py [--dry-run] [--no-links] [--map FILE] [--log FILE]
"""
from __future__ import annotations

import argparse
import hashlib
import os
import posixpath
import re
import sys
from urllib.parse import quote, unquote

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
DEFAULT_MAP = os.path.join(REPO, "archive", "migration-map_2026-10-06.tsv")
SKIP_DIRS = {".git", "node_modules", "__pycache__"}
MOVE_ACTIONS = {"MOVE", "RENAME", "ARCHIVE"}

MD_LINK = re.compile(r"(\[[^\]\n]*\]\(\s*<?)([^)\s>]+)(>?(?:\s+\"[^\"]*\")?\s*\))")
MD_REF = re.compile(r"^(\s{0,3}\[[^\]\n]+\]:\s*<?)(\S+?)(>?(?:\s+\"[^\"]*\")?\s*)$")
HTML_ATTR = re.compile(r"""(\b(?:href|src)\s*=\s*")([^"]+)(")""")
CODE_SPAN = re.compile(r"(`[^`\n]*`)")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
NEWLINES = chr(13) + chr(10)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class Rules:
    def __init__(self, map_path):
        self.exact, self.dirs = {}, {}
        with open(map_path, encoding="utf-8") as fh:
            next(fh)  # header
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 3 or parts[0] not in MOVE_ACTIONS:
                    continue
                _, old, new = parts[:3]
                (self.dirs if old.endswith("/") else self.exact)[old] = new

    def map(self, old):
        """New repo-relative path for an OLD repo-relative path, or None if the path does not move."""
        if old in self.exact:
            return self.exact[old]
        best = None
        for d in self.dirs:
            if old.startswith(d) and (best is None or len(d) > len(best)):
                best = d
        if best:
            return self.dirs[best] + old[len(best):]
        stripped = old.rstrip("/") + "/"  # a link to the directory itself
        if stripped in self.dirs:
            return self.dirs[stripped].rstrip("/") + ("/" if old.endswith("/") else "")
        return None


def candidates(rules):
    """(old, new) for every file that is still at an OLD location."""
    out = {}
    for old, new in rules.exact.items():
        if os.path.isfile(os.path.join(REPO, old)):
            out[old] = new
    for d, nd in rules.dirs.items():
        base = os.path.join(REPO, d)
        if not os.path.isdir(base):
            continue
        for dp, dn, fn in os.walk(base):
            dn[:] = [x for x in dn if x not in SKIP_DIRS]
            for f in fn:
                old = os.path.relpath(os.path.join(dp, f), REPO).replace(os.sep, "/")
                new = rules.map(old)
                if new:
                    out[old] = new
    return out


def rewrite_target(raw, old_dir, new_dir, remap):
    """Return the replacement link text, or None to keep it unchanged."""
    if SCHEME.match(raw) or raw.startswith("#"):
        return None
    m = re.match(r"([^#?]*)([#?].*)?$", raw)
    path, tail = m.group(1), m.group(2) or ""
    if not path or path.startswith("/"):
        return None
    decoded = unquote(path)
    target_old = posixpath.normpath(posixpath.join(old_dir, decoded)) if old_dir else posixpath.normpath(decoded)
    if raw.split("#")[0].endswith("/"):
        target_old += "/"
    if target_old.startswith(".."):
        return None
    target_new = remap(target_old)
    if target_new is None:
        return None
    rel = posixpath.relpath(target_new.rstrip("/"), new_dir or ".")
    if target_new.endswith("/"):
        rel += "/"
    if posixpath.normpath(decoded) == rel.rstrip("/"):
        return None  # same relation as before ('./x' vs 'x' is formatting, not a change): leave the text alone
    new_raw = quote(rel, safe="/:@!$&'*+,;=-._~") + tail
    return None if new_raw == raw else new_raw


def rewrite_text(text, old_dir, new_dir, remap, is_html):
    changed = 0
    out = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if is_html:
            def sub_html(m):
                nonlocal changed
                raw = m.group(2)
                if any(c in raw for c in "${}'+"):
                    return m.group(0)
                n = rewrite_target(raw, old_dir, new_dir, remap)
                if n is None:
                    return m.group(0)
                changed += 1
                return m.group(1) + n + m.group(3)
            out.append(HTML_ATTR.sub(sub_html, line))
            continue
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        # Mask inline code with same-length filler so links whose TEXT contains code (`[`x`](t)`) still match,
        # while anything that is wholly inside a code span is never touched.
        masked = CODE_SPAN.sub(lambda m: "x" * len(m.group(0)), line)
        edits = []  # (start, end, replacement) positions in `line`
        for m in MD_LINK.finditer(masked):
            n = rewrite_target(line[m.start(2):m.end(2)], old_dir, new_dir, remap)
            if n is not None:
                edits.append((m.start(2), m.end(2), n))
        body = masked.rstrip(NEWLINES)
        mref = MD_REF.match(body)
        if mref:
            n = rewrite_target(line[mref.start(2):mref.end(2)], old_dir, new_dir, remap)
            if n is not None:
                edits.append((mref.start(2), mref.end(2), n))
        for a_, b_, n in sorted(edits, reverse=True):
            line = line[:a_] + n + line[b_:]
            changed += 1
        out.append(line)
    return "".join(out), changed


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", default=DEFAULT_MAP)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-links", action="store_true")
    ap.add_argument("--log")
    ap.add_argument("--avoid-ref", help="git ref (e.g. origin/noor): do not rewrite links on lines within 2 lines of "
                                        "edits that ref made, so a later merge cannot conflict; they are reported instead")
    a = ap.parse_args(argv)

    rules = Rules(a.map)
    moves = candidates(rules)
    remap = make_remap_for(rules, moves)

    # collision checks
    dests = {}
    for old, new in moves.items():
        if new in dests:
            sys.exit(f"ABORT: two files map to {new}: {dests[new]} and {old}")
        dests[new] = old

    log, conflicts, identical_dupes, deferred = [], [], [], []
    link_total = files_rewritten = 0
    for old, new in sorted(moves.items()):
        src, dst = os.path.join(REPO, old), os.path.join(REPO, new)
        if os.path.exists(dst):
            if sha256(src) == sha256(dst):
                identical_dupes.append((old, new))
            else:
                conflicts.append((old, new))
            continue
        old_sha = sha256(src)
        rewritten = 0
        text_kind = old.lower().endswith((".md", ".html")) and not a.no_links
        if not a.dry_run:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.rename(src, dst)
        if text_kind:
            path_for_read = dst if not a.dry_run else src
            with open(path_for_read, encoding="utf-8", newline="") as fh:
                data = fh.read()
            new_data, rewritten = rewrite_text(
                data, posixpath.dirname(old), posixpath.dirname(new), remap, old.lower().endswith(".html")
            )
            if rewritten and a.avoid_ref:
                new_data, rewritten, skipped = keep_lines_near_remote_edits(data, new_data, old, a.avoid_ref)
                deferred.extend((old, n, t) for n, t in skipped)
            if rewritten and not a.dry_run:
                with open(dst, "w", encoding="utf-8", newline="") as fh:
                    fh.write(new_data)
            if rewritten:
                files_rewritten += 1
                link_total += rewritten
        new_sha = sha256(dst if not a.dry_run else src) if (rewritten or not a.dry_run) else old_sha
        log.append((old, new, old_sha, new_sha, rewritten))

    # remove old directories that are now empty (bottom-up; os.rmdir refuses non-empty folders)
    if not a.dry_run:
        prune_empty_old_dirs(rules)

    if a.log and not a.dry_run:
        with open(a.log, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("old\tnew\told_sha256\tnew_sha256\tlinks_rewritten\n")
            for row in log:
                fh.write("\t".join(map(str, row)) + "\n")

    verb = "would move" if a.dry_run else "moved"
    print(f"{verb}: {len(log)} files; links rewritten: {link_total} in {files_rewritten} files")
    for old, n, text in deferred:
        print(f"DEFERRED link (line {n} of {old} is near an edit on the remote; fix by hand after merging): {text}")
    for old, new in conflicts:
        print(f"CONFLICT (destination exists, different content; left in place): {old} -> {new}")
    for old, new in identical_dupes:
        print(f"DUPLICATE (identical file already at destination; old copy left in place): {old}")
    return 1 if conflicts else 0


def prune_empty_old_dirs(rules):
    roots = {d.rstrip("/") for d in rules.dirs}
    roots |= {os.path.dirname(o) for o in rules.exact if os.path.dirname(o)}
    top = {r.split("/")[0] for r in roots}
    for t in sorted(top):
        base = os.path.join(REPO, t)
        if not os.path.isdir(base):
            continue
        for dp, _dn, _fn in os.walk(base, topdown=False):
            try:
                os.rmdir(dp)
            except OSError:
                pass


def keep_lines_near_remote_edits(old_text, new_text, old_path, ref):
    """Undo link rewrites on lines that `ref` also edited (within 2 lines). Returns (text, n_rewrites_left, skipped)."""
    import subprocess
    diff = subprocess.run(["git", "diff", "-U0", "HEAD", ref, "--", old_path], cwd=REPO,
                          capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    ranges = []
    for h in re.finditer(r"^@@ -(\d+)(?:,(\d+))? \+", diff, re.M):
        a = int(h.group(1))
        ranges.append((a - 2, a + max(int(h.group(2) or 1), 1) + 1))
    if not ranges:
        return new_text, sum(1 for x, y in zip(old_text.splitlines(), new_text.splitlines()) if x != y), []
    old_lines, new_lines = old_text.splitlines(keepends=True), new_text.splitlines(keepends=True)
    skipped, kept = [], 0
    for i, (x, y) in enumerate(zip(old_lines, new_lines), 1):
        if x == y:
            continue
        if any(lo <= i <= hi for lo, hi in ranges):
            skipped.append((i, x.strip()[:110]))
            new_lines[i - 1] = x
        else:
            kept += 1
    return "".join(new_lines), kept, skipped


def make_remap_for(rules, moves):
    """Remap that also works in --dry-run (where nothing has moved yet)."""
    def remap(target_old):
        new = rules.map(target_old)
        if new is not None:
            return new
        if os.path.exists(os.path.join(REPO, target_old)) or target_old in moves:
            return target_old
        return None
    return remap


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
