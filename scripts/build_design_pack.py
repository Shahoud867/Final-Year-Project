"""Build the design pack: SVG diagrams, Markdown pages, the data dictionary and one interactive HTML file.

    python scripts/build_design_pack.py          # write docs/diagrams/* and the interactive pack in deliverables/
    python scripts/build_design_pack.py --check  # exit 1 if any generated file differs from what the code produces

Everything is derived from the code where possible (tables, states, declared reads, call edges, thresholds, worked
examples on a recorded run). The build fails if the layout lint finds overlapping boxes, text overflow or a
connector through a box, so a diagram that passes is at least mechanically clean.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from design_pack import (  # noqa: E402
    Sheet,  # noqa: E402
    activity,
    algorithms,
    behaviour,
    components,
    data,
    dataflow,
    domain,
    sequences,
    structure,
)
from design_pack.pages import build_pages  # noqa: E402
from design_pack.viewer import build_viewer  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "diagrams"
PACK = ROOT / "deliverables" / "stage-1-fyp1-mid" / "granite_design-pack_fyp1-mid_v1.0.html"

BUILDERS = [
    activity.use_case_diagram, structure.layer_diagram, components.component_diagram, domain.domain_model,
    domain.structure_chart, behaviour.investigation_flow, activity.activity_diagram, behaviour.interaction_overview,
    dataflow.dfd_context, dataflow.dfd_level1, behaviour.state_machine, dataflow.lineage_graph, sequences.sequence_run,
    sequences.sequence_verify, sequences.call_graph, data.er_diagram, algorithms.check_pipeline,
    algorithms.attribution_algorithm, algorithms.vr1_decision, algorithms.replay_plan, activity.deployment_diagram,
]


def build() -> tuple[dict[Path, str], list[str]]:
    sheets: list[Sheet] = [b() for b in BUILDERS]
    issues = [i for s in sheets for i in s.diagram.lint()]
    keys = [s.key for s in sheets]
    if len(set(keys)) != len(keys):
        issues.append("duplicate diagram keys")
    files: dict[Path, str] = {OUT / f"{s.key}.svg": s.diagram.svg() for s in sheets}
    for name, text in build_pages(sheets).items():
        files[OUT / name] = text
    files[OUT / "data-dictionary.md"] = data.data_dictionary()
    files[PACK] = build_viewer(sheets)
    return files, issues


def main() -> int:
    files, issues = build()
    for issue in issues:
        print("LINT:", issue)
    if issues:
        print(f"design pack: {len(issues)} layout problem(s); nothing written")
        return 1
    if "--check" in sys.argv:
        stale = [p for p, text in files.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
        for p in stale:
            print("out of date:", p.relative_to(ROOT).as_posix())
        print("design pack up to date" if not stale else "run: python scripts/build_design_pack.py")
        return 1 if stale else 0
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    svgs = sum(1 for p in files if p.suffix == ".svg")
    print(f"design pack: {svgs} diagrams, {len(files) - svgs - 1} pages, 1 interactive file "
          f"({PACK.relative_to(ROOT).as_posix()}, {len(files[PACK]) // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
