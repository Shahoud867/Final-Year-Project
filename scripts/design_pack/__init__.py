"""Design pack: SVG design artefacts generated from the code (see scripts/build_design_pack.py)."""

from __future__ import annotations

from dataclasses import dataclass, field

from .kit import Diagram


@dataclass
class Sheet:
    """One design artefact: the drawing plus what a reader needs to trust and use it."""

    diagram: Diagram
    category: str  # Structure | Behaviour | Data | Algorithms | Deployment
    table1a: str  # the handbook Table 1a item this artefact answers
    explanation: str  # project-specific explanation shown with the diagram
    sources: list[str] = field(default_factory=list)  # repository paths the drawing is based on
    derived: str = ""  # which parts are computed from the code, and how the rest is checked

    @property
    def key(self) -> str:
        return self.diagram.key
