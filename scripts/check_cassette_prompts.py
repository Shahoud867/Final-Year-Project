"""Fail when the recorded cassette no longer matches the prompts in the code (defect D-10).

    python scripts/check_cassette_prompts.py           # verify
    python scripts/check_cassette_prompts.py --write   # stamp the current prompts into the cassette

A recorded answer is keyed by a hash of the model, the messages and the parameters, so editing one
word of a prompt invalidates every entry at once. Recorded mode then fails for every task, and it
fails at run time with RecordedMiss rather than at the point the prompt was changed. That is slow to
diagnose and it breaks the offline demo.

This stamps a fingerprint of the prompt files into the cassette and checks it, so a prompt edit is
caught in CI by the person who made it, with the fix named in the error.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASSETTE = ROOT / "data" / "cassettes" / "refund_desk_v1.json"
PROMPTS = ROOT / "workflows" / "refund_desk" / "refund_desk" / "prompts"


def fingerprint() -> dict[str, str]:
    """SHA-256 of each prompt file, by name.

    Line endings are normalised before hashing: git checks these files out as CRLF on Windows and
    LF on the CI runner, and the model is sent the decoded text either way. Hashing raw bytes would
    report every prompt as changed on whichever platform did not record the cassette.
    """
    return {
        path.name: hashlib.sha256(path.read_text(encoding="utf-8").replace("\r\n", "\n").encode()).hexdigest()
        for path in sorted(PROMPTS.glob("*.md"))
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="stamp the current prompts into the cassette")
    args = ap.parse_args()

    if not CASSETTE.exists():
        print(f"no cassette at {CASSETTE.relative_to(ROOT)}", file=sys.stderr)
        return 1

    data = json.loads(CASSETTE.read_text(encoding="utf-8"))
    current = fingerprint()
    if not current:
        print(f"no prompt files under {PROMPTS.relative_to(ROOT)}", file=sys.stderr)
        return 1

    if args.write:
        data["prompts"] = current
        CASSETTE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"stamped {len(current)} prompt hashes into {CASSETTE.relative_to(ROOT)}")
        return 0

    recorded = data.get("prompts")
    if recorded is None:
        print("the cassette carries no prompt fingerprint; run: python scripts/check_cassette_prompts.py --write")
        return 1

    drifted = sorted(name for name in current if recorded.get(name) != current[name])
    missing = sorted(set(recorded) - set(current))
    added = sorted(set(current) - set(recorded))
    if drifted or missing or added:
        for name in drifted:
            print(f"prompt changed since the cassette was recorded: {name}")
        for name in missing:
            print(f"prompt recorded but no longer present: {name}")
        for name in added:
            print(f"prompt added since the cassette was recorded: {name}")
        print()
        print("Recorded mode answers by hashing the messages, so this invalidates every entry and")
        print("every task fails with RecordedMiss. Re-record, then stamp:")
        print("  python scripts/record_cassettes.py")
        print("  python scripts/check_cassette_prompts.py --write")
        return 1

    print(f"cassette matches all {len(current)} prompts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
