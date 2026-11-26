"""Score a usability check (docs/manuals/usability-check-protocol.md) and print a Markdown summary.

    python scripts/score_usability.py evidence/uat/2026-10-14_usability-check-results.csv

Input: one row per participant, columns as in docs/manuals/usability-results-template.csv. Task outcomes are
S (success without help), A (success after a hint) or F (failed or gave up); SUS answers are 1 to 5.
The thresholds are the ones fixed in section 1 of the protocol before any session.
"""

from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

TASKS = ["t1", "t2", "t3", "t4", "t5"]
TASK_NAMES = {
    "t1": "Start a faulty run",
    "t2": "Tell that the answer is wrong",
    "t3": "Find which agent caused it",
    "t4": "Prove it and explain the verdict",
    "t5": "Record a decision and download the report",
}
MIN_UNAIDED = 0.80  # share of all task attempts completed without help
MIN_SUS = 68.0  # published average SUS score
MIN_T3_UNAIDED = 2  # participants who find the origin without help


def sus_score(answers: list[int]) -> float:
    """Standard SUS: odd items (a - 1), even items (5 - a), sum times 2.5."""
    if len(answers) != 10 or any(a < 1 or a > 5 for a in answers):
        raise ValueError(f"SUS needs ten answers from 1 to 5, got {answers}")
    total = sum((a - 1) if i % 2 == 0 else (5 - a) for i, a in enumerate(answers))
    return total * 2.5


def load(path: Path) -> list[dict[str, str]]:
    """Read the results CSV and check every outcome code."""
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = [r for r in csv.DictReader(fh) if r.get("participant", "").strip()]
    if not rows:
        raise SystemExit(f"{path}: no participant rows")
    for r in rows:
        for t in TASKS:
            if r[t].strip().upper() not in {"S", "A", "F"}:
                raise SystemExit(f"{r['participant']}: {t} must be S, A or F, got {r[t]!r}")
    return rows


def summarise(rows: list[dict[str, str]], source: str) -> str:
    """Build the Markdown summary with each threshold marked met or not met."""
    out = [f"# Usability check summary\n\nSource: `{source}` · participants: {len(rows)}\n"]

    out.append("## Tasks\n\n| Task | " + " | ".join(r["participant"] for r in rows) + " | Unaided | Median time (s) |")
    out.append("|---|" + "---|" * len(rows) + "---|---|")
    unaided_total = 0
    for t in TASKS:
        codes = [r[t].strip().upper() for r in rows]
        unaided = codes.count("S")
        unaided_total += unaided
        times = [float(r[f"{t}_s"]) for r in rows if r[f"{t}_s"].strip()]
        median = f"{statistics.median(times):.0f}" if times else "n/a"
        out.append(f"| {t.upper()} {TASK_NAMES[t]} | " + " | ".join(codes) + f" | {unaided}/{len(rows)} | {median} |")
    attempts = len(rows) * len(TASKS)

    scores = [sus_score([int(r[f"sus{i}"]) for i in range(1, 11)]) for r in rows]
    out.append("\n## SUS\n\n| Participant | Role | SUS |\n|---|---|---|")
    for r, s in zip(rows, scores, strict=True):
        out.append(f"| {r['participant']} | {r.get('role', '').strip()} | {s:.1f} |")
    mean_sus = statistics.mean(scores)
    out.append(f"| **Mean** | | **{mean_sus:.1f}** |")

    t3_unaided = [r["t3"].strip().upper() for r in rows].count("S")
    checks = [
        ("Tasks completed without help", f"{unaided_total}/{attempts} ({unaided_total / attempts:.0%})",
         f">= {MIN_UNAIDED:.0%}", unaided_total / attempts >= MIN_UNAIDED),
        ("Mean SUS", f"{mean_sus:.1f}", f">= {MIN_SUS:.0f}", mean_sus >= MIN_SUS),
        ("T3 (find the cause) without help", f"{t3_unaided}/{len(rows)}", f">= {MIN_T3_UNAIDED}",
         t3_unaided >= MIN_T3_UNAIDED),
    ]
    out.append("\n## Thresholds (fixed before the sessions)\n\n| Measure | Result | Threshold | Outcome |\n|---|---|---|---|")
    for name, result, threshold, ok in checks:
        out.append(f"| {name} | {result} | {threshold} | {'met' if ok else '**not met**'} |")

    out.append("\n## What participants said\n")
    for r in rows:
        out.append(f"- **{r['participant']}**, most confusing: {r.get('most_confusing', '').strip() or '(none)'}; "
                   f"would change: {r.get('would_change', '').strip() or '(none)'}")
    return "\n".join(out) + "\n"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    path = Path(sys.argv[1])
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]  # Windows consoles default to cp1252
    print(summarise(load(path), path.as_posix()))


if __name__ == "__main__":
    main()
