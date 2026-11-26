"""Write the Granite Trace v1 JSON Schema from the pydantic model (the model is the single source of truth).

    python scripts/export_trace_schema.py          # rewrite packages/granite_core/schema/granite-trace-v1.schema.json
    python scripts/export_trace_schema.py --check  # exit 1 if the committed file differs from the model
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from granite_core.trace import SCHEMA_VERSION, TraceV1

TARGET = Path(__file__).resolve().parents[1] / "packages" / "granite_core" / "schema" / "granite-trace-v1.schema.json"


def render() -> str:
    schema = TraceV1.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = f"https://granite.example/schema/{SCHEMA_VERSION.replace('/', '-')}.json"
    return json.dumps(schema, indent=2, sort_keys=True) + "\n"


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        ok = TARGET.exists() and TARGET.read_text(encoding="utf-8") == text
        print("schema up to date" if ok else f"{TARGET} is out of date; run scripts/export_trace_schema.py")
        return 0 if ok else 1
    TARGET.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
