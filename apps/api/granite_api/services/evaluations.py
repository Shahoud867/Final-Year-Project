"""Evaluation results: the benchmark harness's result files, served read-only to the Evaluation page (F20 v0).

The API runs no evaluation itself. It reads ``*_benchmark-v*.json`` files written by ``research/eval/benchmark_v0.py``
from one configured directory and returns what they contain, so the page can show nothing the harness did not
measure. The ``id`` of a result is its file stem; anything else is refused, so no path can be smuggled in.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from ..errors import ProblemError

STEM = re.compile(r"^\d{4}-\d{2}-\d{2}_benchmark-v\d+[a-z0-9-]*$")


def _files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted((p for p in directory.glob("*_benchmark-v*.json") if STEM.match(p.stem)), reverse=True)


def _read(path: Path) -> dict[str, Any]:
    try:
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise ProblemError(500, "Unreadable result", f"The result file {path.name} could not be read.") from None
    return data


def list_evaluations(directory: Path) -> list[dict[str, Any]]:
    """Newest first: id, protocol and headline metrics of each result file."""
    out = []
    for path in _files(directory):
        data = _read(path)
        meta = data.get("meta", {})
        expected_runs = meta.get("n_tasks", 0) * (1 + len(meta.get("faults", [])))
        out.append({
            "id": path.stem,
            "date": meta.get("date"),
            "mode": meta.get("mode"),
            "model": meta.get("model"),
            "runs": len(data.get("rows", [])),
            "complete": bool(meta) and len(data.get("rows", [])) >= expected_runs,
            "metrics": data.get("metrics", {}),
        })
    return out


def get_evaluation(directory: Path, eval_id: str) -> dict[str, Any]:
    """One result file in full (meta, metrics and per-run rows); 404 for an unknown or malformed id."""
    if not STEM.match(eval_id):
        raise ProblemError(404, "Evaluation not found", f"There is no evaluation '{eval_id}'.")
    path = directory / f"{eval_id}.json"
    if not path.is_file():
        raise ProblemError(404, "Evaluation not found", f"There is no evaluation '{eval_id}'.")
    data = _read(path)
    return {"id": eval_id, **data}


__all__ = ["get_evaluation", "list_evaluations"]
