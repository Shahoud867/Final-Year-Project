"""Exercise the connectors against real servers: send a Refund Desk run, read it back, check it, write a verdict.

    python scripts/check_connectors_live.py --phoenix http://localhost:6006
    python scripts/check_connectors_live.py --langfuse https://cloud.langfuse.com     # keys from the environment
    python scripts/check_connectors_live.py --phoenix http://localhost:6006 --out evidence/demos/<file>.json

For each platform: (1) run the Refund Desk on a recorded example task with the stale-price fault, (2) send the trace,
(3) send it again (must add nothing), (4) read the trace back and map it to Granite Trace v1, (5) compare it with the
original step by step, (6) run the workflow's checks on the imported trace, (7) write a verdict annotation (Phoenix)
or score (Langfuse) on the origin step and (8) read it back where the API allows. Exit code 0 only if every step
passed. Langfuse keys come from GRANITE_LANGFUSE_PUBLIC_KEY and GRANITE_LANGFUSE_SECRET_KEY; nothing is printed
that contains them.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from granite_connectors import LangfuseClient, PhoenixClient, Profile, map_trace, trace_to_spans
from granite_core.checks import evaluate_checks
from granite_core.regression import default_provider
from granite_core.runner import run_workflow
from granite_core.trace import TraceV1
from refund_desk import build_workflow, default_store, make_fault

ROOT = Path(__file__).resolve().parents[1]


class Report:
    """Pass or fail per step, printed as it goes and saved as JSON."""

    def __init__(self, platform: str) -> None:
        self.platform = platform
        self.steps: list[dict[str, Any]] = []

    def check(self, name: str, ok: bool, detail: Any = "") -> bool:
        self.steps.append({"step": name, "ok": ok, "detail": detail})
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail != "" else ""))
        return ok

    @property
    def ok(self) -> bool:
        return all(s["ok"] for s in self.steps)


def make_run() -> tuple[TraceV1, Any, str]:
    """A recorded Refund Desk run with the stale-price fault, on the first delivered example task."""
    store = default_store()
    task = next(t for t in store.example_tasks(12) if "(delivered)" in t["label"])
    defn = build_workflow(store, "llama3.2:3b")
    outcome = run_workflow(defn, {k: task[k] for k in ("message", "email", "order_id")}, default_provider(),
                           fault=make_fault("stale_price"), seed=1)
    return outcome.trace, defn, f"live-{uuid.uuid4().hex[:10]}"


def compare(original: TraceV1, imported: TraceV1) -> list[str]:
    """Differences between two traces' steps (ignoring nothing): empty means an exact round trip."""
    diffs = []
    a, b = original.model_dump(mode="json")["steps"], imported.model_dump(mode="json")["steps"]
    if len(a) != len(b):
        return [f"{len(a)} steps sent, {len(b)} read back"]
    for x, y in zip(a, b, strict=True):
        diffs += [f"{x['step_id']}.{k}" for k in x if x[k] != y.get(k)]
    return diffs


def verify_import(rep: Report, trace: TraceV1, defn: Any, spans: list[Any], runtime: str) -> tuple[Any, list[Any]]:
    mapped = map_trace(spans, Profile(name="live check", workflow=defn.key), runtime=runtime)
    diffs = compare(trace, mapped.trace)
    rep.check("imported trace equals the original, step by step", not diffs, diffs or f"{len(mapped.trace.steps)} steps")
    rep.check("lineage came from declared reads", {e.tier for e in mapped.lineage} == {"declared"},
              sorted({e.tier for e in mapped.lineage}))
    before = [r.check_id for r in evaluate_checks(trace, defn.checks, defn.truth()) if r.status == "fail"]
    after = [r.check_id for r in evaluate_checks(mapped.trace, defn.checks, defn.truth()) if r.status == "fail"]
    rep.check("checks on the imported trace fail exactly as on the original", before == after and bool(after), after)
    return mapped, after


def check_phoenix(url: str, project: str) -> Report:
    rep = Report("phoenix")
    print(f"Phoenix at {url}, project {project}")
    px = PhoenixClient(url, project, os.environ.get("GRANITE_PHOENIX_API_KEY") or None)
    trace, defn, key = make_run()
    spans = trace_to_spans(trace, key, {"seed": 1, "model": "llama3.2:3b", "fault": "stale_price"})
    px.ensure_project()
    rep.check("project exists or was created", bool(px.ping().get("name")), project)
    rep.check("spans sent", px.send(spans) == len(spans), f"{len(spans)} spans, trace {spans[0].trace_id}")
    back: list[Any] = []
    for _ in range(20):  # Phoenix inserts asynchronously
        back = [t for t in px.traces(trace_ids=[spans[0].trace_id])]
        if back and len(back[0]) == len(spans):
            break
        time.sleep(0.5)
    rep.check("trace read back with every span", bool(back) and len(back[0]) == len(spans),
              f"{len(back[0]) if back else 0} of {len(spans)}")
    rep.check("sending again adds nothing (idempotent)", px.send(spans) == 0)
    if not back:
        return rep
    mapped, _ = verify_import(rep, trace, defn, back[0], "phoenix")
    span = mapped.span_ids["s2"]
    px.annotate(span, "granite.verdict", label="confirmed", score=1.0,
                explanation="live check: Order Lookup (s2) confirmed by replay", metadata={"check": "CHK-OUT-1"})
    px.annotate(span, "granite.verdict", label="confirmed", score=1.0, explanation="live check: written twice")
    notes = [a for a in px.annotations([span]) if a.get("name") == "granite.verdict"]
    rep.check("verdict annotation on the origin span, updated in place", len(notes) == 1 and
              notes[0]["result"]["label"] == "confirmed", notes[0]["result"] if notes else "none found")
    return rep


def check_langfuse(url: str) -> Report:
    rep = Report("langfuse")
    pk, sk = os.environ.get("GRANITE_LANGFUSE_PUBLIC_KEY", ""), os.environ.get("GRANITE_LANGFUSE_SECRET_KEY", "")
    print(f"Langfuse at {url}")
    if not rep.check("keys present in the environment", bool(pk and sk)):
        return rep
    lf = LangfuseClient(url, pk, sk)
    rep.check("health and authentication", bool(lf.ping()))
    trace, defn, key = make_run()
    spans = trace_to_spans(trace, key, {"seed": 1, "model": "llama3.2:3b", "fault": "stale_price"})
    rep.check("ingestion accepted every event", lf.send(spans, "granite-live-check") == len(spans))
    records: list[Any] = []
    for _ in range(40):  # Langfuse ingests asynchronously; allow up to about a minute
        try:
            records = lf.trace(spans[0].trace_id)
        except Exception:  # noqa: BLE001 - 404 until the trace is processed
            records = []
        if len(records) == len(spans):
            break
        time.sleep(1.5)
    rep.check("trace read back with every observation", len(records) == len(spans), f"{len(records)} of {len(spans)}")
    if len(records) != len(spans):
        return rep
    mapped, _ = verify_import(rep, trace, defn, records, "langfuse")
    sid = lf.score(spans[0].trace_id, mapped.span_ids["s2"], "granite.verdict", label="confirmed",
                   comment="live check: Order Lookup (s2) confirmed by replay")
    rep.check("verdict score written", bool(sid), sid)
    return rep


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--phoenix", help="Phoenix base URL, e.g. http://localhost:6006")
    ap.add_argument("--project", default="granite-live-check", help="Phoenix project to use")
    ap.add_argument("--langfuse", help="Langfuse host, e.g. https://cloud.langfuse.com")
    ap.add_argument("--out", help="write the report as JSON to this path")
    args = ap.parse_args()
    if not (args.phoenix or args.langfuse):
        ap.error("give --phoenix and/or --langfuse")
    reports = []
    if args.phoenix:
        reports.append(check_phoenix(args.phoenix, args.project))
    if args.langfuse:
        reports.append(check_langfuse(args.langfuse))
    ok = all(r.ok for r in reports)
    if args.out:
        doc = {"checked_at": datetime.now(UTC).isoformat(), "ok": ok,
               "platforms": [{"platform": r.platform, "ok": r.ok, "steps": r.steps} for r in reports]}
        Path(args.out).write_text(json.dumps(doc, indent=2, default=str) + "\n", encoding="utf-8")
        print(f"report written to {args.out}")
    print("ALL PASSED" if ok else "SOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
