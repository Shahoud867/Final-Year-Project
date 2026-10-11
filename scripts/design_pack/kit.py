"""A small SVG drawing kit for the design pack: boxes, connectors, labels, and a layout lint.

No third-party dependency. Every diagram is built from the same primitives so typography, spacing and colour are
identical across the pack, and `Diagram.lint()` rejects overlapping boxes, text that does not fit its box, labels
that sit on a box, and connectors that pass through a box they do not belong to.
"""

from __future__ import annotations

import html
from dataclasses import dataclass, field

FONT = "'Segoe UI', system-ui, -apple-system, Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'Cascadia Mono', Consolas, 'Courier New', monospace"
INK, MUTED, LINE, CANVAS = "#1b2430", "#586474", "#7b8696", "#ffffff"

# kind -> (fill, stroke). One meaning per colour across the whole pack.
KINDS: dict[str, tuple[str, str]] = {
    "core": ("#e8f0fe", "#3b6fd4"),  # granite_core
    "api": ("#e2f5f1", "#1b8576"),  # application layer
    "web": ("#f0eafc", "#6f4fc7"),  # user interface
    "workflow": ("#fdf2d9", "#b0731a"),  # system under test
    "external": ("#eef1f5", "#66717f"),  # things outside the product
    "store": ("#f4f6f9", "#55606e"),  # data at rest
    "actor": ("#ffffff", "#3d4a5c"),
    "ok": ("#e3f4e9", "#1d7a46"),
    "bad": ("#fde7e4", "#c0392b"),
    "warn": ("#fdf0d0", "#a86a00"),
    "plain": ("#ffffff", "#7b8696"),
    "planned": ("#ffffff", "#9aa4b1"),
    "terminal": ("#eceff3", "#3d4a5c"),
}

_NARROW, _WIDE = set("iljtfr.,:;|!'()[]{} "), set("mwMW@%")


def text_width(text: str, size: float = 12.0, bold: bool = False) -> float:
    """Estimate rendered width in px (calibrated for Segoe UI / Arial); used only for layout checks."""
    total = 0.0
    for ch in text:
        if ch in _NARROW:
            total += 0.30
        elif ch in _WIDE:
            total += 0.86
        elif ch.isupper() or ch.isdigit():
            total += 0.63
        else:
            total += 0.53
    return total * size * (1.06 if bold else 1.0)


@dataclass
class Node:
    id: str
    x: float
    y: float
    w: float
    h: float
    kind: str = "plain"
    container: bool = False

    @property
    def cx(self) -> float:
        return self.x + self.w / 2

    @property
    def cy(self) -> float:
        return self.y + self.h / 2

    def top(self, f: float = 0.5) -> tuple[float, float]:
        return (self.x + self.w * f, self.y)

    def bottom(self, f: float = 0.5) -> tuple[float, float]:
        return (self.x + self.w * f, self.y + self.h)

    def left(self, f: float = 0.5) -> tuple[float, float]:
        return (self.x, self.y + self.h * f)

    def right(self, f: float = 0.5) -> tuple[float, float]:
        return (self.x + self.w, self.y + self.h * f)

    def box(self, pad: float = 0.0) -> tuple[float, float, float, float]:
        return (self.x - pad, self.y - pad, self.x + self.w + pad, self.y + self.h + pad)


@dataclass
class _Edge:
    points: list[tuple[float, float]]
    src: str
    dst: str


@dataclass
class _Label:
    box: tuple[float, float, float, float]
    text: str
    owner: str = ""


def _overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def _segment_hits(p: tuple[float, float], q: tuple[float, float], box: tuple[float, float, float, float]) -> bool:
    """True if the segment p-q crosses the interior of box (Liang-Barsky clipping)."""
    x0, y0, x1, y1 = box
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for d, lo, hi, start in ((dx, x0, x1, p[0]), (dy, y0, y1, p[1])):
        if abs(d) < 1e-9:
            if start <= lo or start >= hi:
                return False
            continue
        a, b = (lo - start) / d, (hi - start) / d
        if a > b:
            a, b = b, a
        t0, t1 = max(t0, a), min(t1, b)
        if t0 >= t1:
            return False
    return t1 - t0 > 1e-6


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


@dataclass
class Diagram:
    key: str
    title: str
    width: int
    height: int
    desc: str = ""
    nodes: dict[str, Node] = field(default_factory=dict)
    _back: list[str] = field(default_factory=list)  # frames and lanes, drawn first
    _edges_svg: list[str] = field(default_factory=list)
    _nodes_svg: list[str] = field(default_factory=list)
    _front: list[str] = field(default_factory=list)  # labels and notes, drawn last
    _edges: list[_Edge] = field(default_factory=list)
    _labels: list[_Label] = field(default_factory=list)
    _text_issues: list[str] = field(default_factory=list)

    # ---- text helpers -------------------------------------------------------------------------------
    def _text(self, x: float, y: float, text: str, size: float = 12, weight: int = 400, fill: str = INK,
              anchor: str = "middle", mono: bool = False, italic: bool = False, halo: bool = False) -> str:
        style = f"font-size:{size}px;font-weight:{weight};fill:{fill};"
        if mono:
            style += f"font-family:{MONO};"
        if italic:
            style += "font-style:italic;"
        cls = ' class="halo"' if halo else ""
        return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="{style}"{cls}>{esc(text)}</text>'

    def _fit(self, owner: str, text: str, size: float, bold: bool, room: float, mono: bool = False) -> None:
        width = len(text) * 0.602 * size if mono else text_width(text, size, bold)
        if width > room + 0.5:
            self._text_issues.append(f"text does not fit in '{owner}' ({width:.0f} > {room:.0f}px): {text}")

    # ---- containers ---------------------------------------------------------------------------------
    def frame(self, id: str, x: float, y: float, w: float, h: float, label: str, kind: str = "plain",
              dashed: bool = False, note: str = "") -> Node:
        fill, stroke = KINDS[kind]
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self._back.append(
            f'<g class="frame" data-id="{esc(id)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
            f'fill="{fill}" fill-opacity="0.45" stroke="{stroke}" stroke-width="1.2"{dash}/>'
            + self._text(x + 12, y + 19, label, 12, 700, stroke, "start")
            + (self._text(x + w - 12, y + 19, note, 11, 400, MUTED, "end", italic=True) if note else "")
            + "</g>"
        )
        self._labels.append(_Label((x + 10, y + 6, x + 14 + text_width(label, 12, True), y + 24), label, id))
        node = Node(id, x, y, w, h, kind, container=True)
        self.nodes[id] = node
        return node

    def lane(self, id: str, x: float, y: float, w: float, h: float, label: str, kind: str = "plain") -> Node:
        """A swimlane column with a header band."""
        fill, stroke = KINDS[kind]
        self._back.append(
            f'<g class="lane"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" fill-opacity="0.28" '
            f'stroke="{LINE}" stroke-width="1"/><rect x="{x}" y="{y}" width="{w}" height="30" fill="{fill}" '
            f'stroke="{LINE}" stroke-width="1"/>' + self._text(x + w / 2, y + 20, label, 12.5, 700, INK) + "</g>"
        )
        node = Node(id, x, y, w, h, kind, container=True)
        self.nodes[id] = node
        return node

    # ---- nodes --------------------------------------------------------------------------------------
    def node(self, id: str, x: float, y: float, w: float, h: float, title: str, lines: tuple[str, ...] | list[str] = (),
             kind: str = "plain", shape: str = "rect", tip: str = "", dashed: bool = False, mono_lines: bool = False,
             title_size: float = 12.5) -> Node:
        fill, stroke = KINDS[kind]
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        base = f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"{dash}'
        if shape == "pill":
            body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" {base}/>'
        elif shape == "diamond":
            cx, cy = x + w / 2, y + h / 2
            body = f'<path d="M{cx} {y} L{x + w} {cy} L{cx} {y + h} L{x} {cy} Z" {base}/>'
        elif shape == "cyl":
            ry = 7
            body = (f'<path d="M{x} {y + ry} A{w / 2} {ry} 0 0 1 {x + w} {y + ry} V{y + h - ry} A{w / 2} {ry} 0 0 1 {x} '
                    f'{y + h - ry} Z" {base}/><path d="M{x} {y + ry} A{w / 2} {ry} 0 0 0 {x + w} {y + ry}" fill="none" '
                    f'stroke="{stroke}" stroke-width="1.4"{dash}/>')
        elif shape == "store":  # DFD data store: open-ended box
            body = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="none"/>'
                    f'<path d="M{x} {y} H{x + w} M{x} {y + h} H{x + w} M{x} {y} V{y + h} M{x + 26} {y} V{y + h}" '
                    f'fill="none" stroke="{stroke}" stroke-width="1.4"/>')
        elif shape == "circle":
            body = f'<ellipse cx="{x + w / 2}" cy="{y + h / 2}" rx="{w / 2}" ry="{h / 2}" {base}/>'
        elif shape == "doc":
            body = (f'<path d="M{x} {y} H{x + w} V{y + h - 8} Q{x + w * 0.75} {y + h - 16} {x + w / 2} {y + h - 8} '
                    f'T{x} {y + h - 8} Z" {base}/>')
        else:
            body = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" {base}/>'
        pad = 30 if shape == "diamond" else (30 if shape == "store" else 10)
        room = w - 2 * pad if shape != "store" else w - 26 - 12
        tx = x + w / 2 if shape != "store" else x + 26 + (w - 26) / 2
        line_h = 15
        block = 16 + line_h * len(lines)
        usable = h - 10 if shape == "doc" else h  # keep text clear of the wavy bottom edge
        top = y + (usable - block) / 2 + 13
        if shape == "cyl":  # start below the rim of the cylinder
            top = y + 14 + (h - 14 - block) / 2 + 13
        parts = [body, self._text(tx, top, title, title_size, 650, INK)]
        self._fit(id, title, title_size, True, room)
        for i, ln in enumerate(lines):
            parts.append(self._text(tx, top + 16 + i * line_h, ln, 11, 400, MUTED, mono=mono_lines))
            self._fit(id, ln, 11, False, room, mono=mono_lines)
        tip_el = f"<title>{esc(tip)}</title>" if tip else ""
        self._nodes_svg.append(f'<g class="node" data-id="{esc(id)}" tabindex="0">{tip_el}{"".join(parts)}</g>')
        node = Node(id, x, y, w, h, kind)
        self.nodes[id] = node
        return node

    def actor(self, id: str, x: float, y: float, label: str) -> Node:
        """A stick figure with a label; the node box covers figure and label."""
        cx = x + 30
        fig = (f'<circle cx="{cx}" cy="{y + 9}" r="8" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
               f'<path d="M{cx} {y + 17} V{y + 40} M{cx - 15} {y + 26} H{cx + 15} M{cx} {y + 40} L{cx - 12} {y + 58} '
               f'M{cx} {y + 40} L{cx + 12} {y + 58}" fill="none" stroke="{INK}" stroke-width="1.5"/>')
        self._nodes_svg.append(f'<g class="node" data-id="{esc(id)}" tabindex="0">{fig}'
                               + self._text(cx, y + 75, label, 12.5, 650) + "</g>")
        node = Node(id, x, y, 60, 80, "actor")
        self.nodes[id] = node
        return node

    def compartments(self, id: str, x: float, y: float, w: float, title: str, rows: list[str], kind: str = "core",
                     stereotype: str = "", footer: list[str] | None = None, tip: str = "") -> Node:
        """A class or table box: header, attribute rows (monospace), optional second compartment."""
        fill, stroke = KINDS[kind]
        head = 40 if stereotype else 28
        row_h = 15.5
        body_h = 8 + row_h * len(rows) + 4
        foot = footer or []
        foot_h = (8 + row_h * len(foot) + 2) if foot else 0
        h = head + body_h + foot_h
        parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#ffffff" stroke="{stroke}" stroke-width="1.4"/>',
                 f'<path d="M{x} {y + head} H{x + w} V{y + 6} Q{x + w} {y} {x + w - 6} {y} H{x + 6} Q{x} {y} {x} {y + 6} Z" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>']
        if stereotype:
            parts.append(self._text(x + w / 2, y + 15, f"«{stereotype}»", 10.5, 400, MUTED, italic=True))
            parts.append(self._text(x + w / 2, y + 31, title, 12.5, 700))
        else:
            parts.append(self._text(x + w / 2, y + 19, title, 12.5, 700))
        self._fit(id, title, 12.5, True, w - 16)
        for i, row in enumerate(rows):
            parts.append(self._text(x + 9, y + head + 17 + i * row_h, row, 10.8, 400, INK, "start", mono=True))
            self._fit(id, row, 10.8, False, w - 16, mono=True)
        if foot:
            fy = y + head + body_h
            parts.append(f'<path d="M{x} {fy} H{x + w}" stroke="{stroke}" stroke-width="1"/>')
            for i, row in enumerate(foot):
                parts.append(self._text(x + 9, fy + 16 + i * row_h, row, 10.8, 400, MUTED, "start", mono=True))
                self._fit(id, row, 10.8, False, w - 16, mono=True)
        tip_el = f"<title>{esc(tip)}</title>" if tip else ""
        self._nodes_svg.append(f'<g class="node" data-id="{esc(id)}" tabindex="0">{tip_el}{"".join(parts)}</g>')
        node = Node(id, x, y, w, h, kind)
        self.nodes[id] = node
        return node

    def terminal(self, id: str, x: float, y: float, final: bool = False) -> Node:
        """UML initial node (filled dot) or final node (bullseye), centred on (x, y)."""
        if final:
            svg = (f'<circle cx="{x}" cy="{y}" r="9" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
                   f'<circle cx="{x}" cy="{y}" r="5" fill="{INK}"/>')
        else:
            svg = f'<circle cx="{x}" cy="{y}" r="7" fill="{INK}"/>'
        self._nodes_svg.append(f'<g class="node" data-id="{esc(id)}">{svg}</g>')
        r = 9 if final else 7
        node = Node(id, x - r, y - r, 2 * r, 2 * r, "terminal")
        self.nodes[id] = node
        return node

    def ref(self, id: str, x: float, y: float, w: float, h: float, title: str, lines: list[str], kind: str = "core",
            tag: str = "ref") -> Node:
        """An interaction-use frame (UML 'ref'): a box with a tag in its top-left corner."""
        fill, stroke = KINDS[kind]
        tab_w = 16 + text_width(tag, 11, True)
        parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>',
                 f'<path d="M{x} {y} H{x + tab_w} V{y + 14} L{x + tab_w - 8} {y + 22} H{x} Z" fill="#ffffff" stroke="{stroke}" stroke-width="1.2"/>',
                 self._text(x + 7, y + 16, tag, 11, 700, stroke, "start")]
        block = 16 + 15 * len(lines)
        top = y + 22 + (h - 22 - block) / 2 + 13
        parts.append(self._text(x + w / 2, top, title, 12.5, 650))
        self._fit(id, title, 12.5, True, w - 20)
        for i, ln in enumerate(lines):
            parts.append(self._text(x + w / 2, top + 16 + i * 15, ln, 11, 400, MUTED))
            self._fit(id, ln, 11, False, w - 20)
        self._nodes_svg.append(f'<g class="node" data-id="{esc(id)}" tabindex="0">{"".join(parts)}</g>')
        node = Node(id, x, y, w, h, kind)
        self.nodes[id] = node
        return node

    # ---- connectors ---------------------------------------------------------------------------------
    @staticmethod
    def _path(points: list[tuple[float, float]], radius: float = 9.0) -> str:
        if len(points) < 3:
            return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)
        d = [f"M{points[0][0]:.1f} {points[0][1]:.1f}"]
        for i in range(1, len(points) - 1):
            (px, py), (cx, cy), (nx, ny) = points[i - 1], points[i], points[i + 1]
            l1 = ((cx - px) ** 2 + (cy - py) ** 2) ** 0.5
            l2 = ((nx - cx) ** 2 + (ny - cy) ** 2) ** 0.5
            r = min(radius, l1 / 2, l2 / 2)
            if r < 0.5:
                d.append(f"L{cx:.1f} {cy:.1f}")
                continue
            ax, ay = cx - (cx - px) / l1 * r, cy - (cy - py) / l1 * r
            bx, by = cx + (nx - cx) / l2 * r, cy + (ny - cy) / l2 * r
            d.append(f"L{ax:.1f} {ay:.1f} Q{cx:.1f} {cy:.1f} {bx:.1f} {by:.1f}")
        d.append(f"L{points[-1][0]:.1f} {points[-1][1]:.1f}")
        return " ".join(d)

    def edge(self, points: list[tuple[float, float]], label: str = "", src: str = "", dst: str = "",
             dashed: bool = False, end: str = "arrow", start: str = "", color: str = LINE, width: float = 1.5,
             label_at: tuple[float, float] | None = None, label_seg: int | None = None, label_dy: float = -6,
             label_dx: float = 0, label_anchor: str = "middle", tip: str = "", label_size: float = 10.8) -> None:
        dash = ' stroke-dasharray="6 4"' if dashed else ""
        m_end = f' marker-end="url(#{self.key}-{end})"' if end else ""
        m_start = f' marker-start="url(#{self.key}-{start})"' if start else ""
        tip_el = f"<title>{esc(tip or label)}</title>" if (tip or label) else ""
        svg = (f'<g class="edge" data-from="{esc(src)}" data-to="{esc(dst)}">{tip_el}<path d="{self._path(points)}" '
               f'fill="none" stroke="{color}" stroke-width="{width}"{dash}{m_end}{m_start}/></g>')
        self._edges_svg.append(svg)
        self._edges.append(_Edge(points, src, dst))
        if label:
            if label_at is None:
                segs = list(zip(points, points[1:], strict=False))
                if label_seg is None:
                    label_seg = max(range(len(segs)), key=lambda i: (segs[i][1][0] - segs[i][0][0]) ** 2 + (segs[i][1][1] - segs[i][0][1]) ** 2)
                (ax, ay), (bx, by) = segs[label_seg]
                label_at = ((ax + bx) / 2 + label_dx, (ay + by) / 2 + label_dy)
            self.label(label_at[0], label_at[1], label, size=label_size, anchor=label_anchor, owner=f"{src}->{dst}")

    def label(self, x: float, y: float, text: str, size: float = 10.8, anchor: str = "middle", color: str = MUTED,
              weight: int = 500, owner: str = "", mono: bool = False, check: bool = True) -> None:
        self._front.append(self._text(x, y, text, size, weight, color, anchor, mono=mono, halo=True))
        w = text_width(text, size if not mono else size * 1.1, weight >= 600)
        left = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
        if check:
            self._labels.append(_Label((left - 1, y - size, left + w + 1, y + 3), text, owner))

    def note(self, x: float, y: float, w: float, lines: list[str], kind: str = "warn", id: str = "") -> Node:
        fill, stroke = KINDS[kind]
        h = 14 + 15 * len(lines)
        parts = [f'<path d="M{x} {y} H{x + w - 12} L{x + w} {y + 12} V{y + h} H{x} Z" fill="{fill}" stroke="{stroke}" '
                 f'stroke-width="1.1"/><path d="M{x + w - 12} {y} V{y + 12} H{x + w}" fill="none" stroke="{stroke}" stroke-width="1.1"/>']
        nid = id or f"note-{len(self.nodes)}"
        for i, ln in enumerate(lines):
            parts.append(self._text(x + 10, y + 18 + i * 15, ln, 11, 700 if i == 0 else 400, INK, "start"))
            self._fit(nid, ln, 11, i == 0, w - 22)
        self._nodes_svg.append(f'<g class="note">{"".join(parts)}</g>')
        node = Node(nid, x, y, w, h, kind)
        self.nodes[nid] = node
        return node

    def legend(self, x: float, y: float, items: list[tuple[str, str]], title: str = "Legend", cols: int = 1,
               col_w: float = 190) -> None:
        """items: (kind or 'line:dashed' / 'line:solid', text)."""
        rows = (len(items) + cols - 1) // cols
        w, h = col_w * cols + 16, 30 + rows * 19
        parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#ffffff" stroke="#c9d0d9" stroke-width="1"/>',
                 self._text(x + 12, y + 18, title, 11.5, 700, INK, "start")]
        for i, (kind, text) in enumerate(items):
            cx, cy = x + 12 + (i // rows) * col_w, y + 36 + (i % rows) * 19
            if kind.startswith("line"):
                dash = ' stroke-dasharray="5 4"' if kind.endswith("dashed") else ""
                parts.append(f'<path d="M{cx} {cy - 4} H{cx + 24}" stroke="{LINE}" stroke-width="1.6"{dash} '
                             f'marker-end="url(#{self.key}-arrow)"/>')
            else:
                fill, stroke = KINDS[kind]
                dash = ' stroke-dasharray="4 3"' if kind == "planned" else ""
                parts.append(f'<rect x="{cx}" y="{cy - 11}" width="22" height="13" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.2"{dash}/>')
            parts.append(self._text(cx + 32, cy, text, 11, 400, INK, "start"))
        self._front.append(f'<g class="legend">{"".join(parts)}</g>')
        self.nodes[f"legend-{len(self.nodes)}"] = Node("legend", x, y, w, h, "plain")

    # ---- quality gate -------------------------------------------------------------------------------
    def lint(self) -> list[str]:
        issues = list(self._text_issues)
        solid = [n for n in self.nodes.values() if not n.container]
        for i, a in enumerate(solid):
            if a.x < 0 or a.y < 0 or a.x + a.w > self.width or a.y + a.h > self.height:
                issues.append(f"'{a.id}' is outside the canvas")
            for b in solid[i + 1:]:
                if _overlap(a.box(), b.box()):
                    issues.append(f"boxes overlap: '{a.id}' and '{b.id}'")
        for lab in self._labels:
            if lab.box[0] < 0 or lab.box[2] > self.width or lab.box[1] < 0 or lab.box[3] > self.height:
                issues.append(f"label outside the canvas: {lab.text}")
            for n in solid:
                if n.id != lab.owner and _overlap(lab.box, n.box(-1)):
                    issues.append(f"label '{lab.text}' sits on box '{n.id}'")
        for i, a in enumerate(self._labels):
            for b in self._labels[i + 1:]:
                if _overlap(a.box, b.box):
                    issues.append(f"labels overlap: '{a.text}' and '{b.text}'")
        for e in self._edges:
            for n in solid:
                if n.id in (e.src, e.dst):
                    continue
                for p, q in zip(e.points, e.points[1:], strict=False):
                    if _segment_hits(p, q, n.box(-2)):
                        issues.append(f"connector {e.src or '?'} -> {e.dst or '?'} passes through box '{n.id}'")
                        break
        return [f"[{self.key}] {m}" for m in dict.fromkeys(issues)]

    # ---- output -------------------------------------------------------------------------------------
    def _defs(self) -> str:
        k = self.key
        return (
            "<defs>"
            f'<marker id="{k}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10 Z" fill="{LINE}"/></marker>'
            f'<marker id="{k}-open" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">'
            f'<path d="M0 0 L10 5 L0 10" fill="none" stroke="{LINE}" stroke-width="1.6"/></marker>'
            f'<marker id="{k}-tri" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">'
            f'<path d="M0 0 L12 6 L0 12 Z" fill="#fff" stroke="{LINE}" stroke-width="1.3"/></marker>'
            f'<marker id="{k}-diamond" viewBox="0 0 16 10" refX="15" refY="5" markerWidth="13" markerHeight="9" orient="auto-start-reverse">'
            f'<path d="M0 5 L8 0 L16 5 L8 10 Z" fill="{LINE}"/></marker>'
            f'<marker id="{k}-odiamond" viewBox="0 0 16 10" refX="15" refY="5" markerWidth="13" markerHeight="9" orient="auto-start-reverse">'
            f'<path d="M0 5 L8 0 L16 5 L8 10 Z" fill="#fff" stroke="{LINE}" stroke-width="1.3"/></marker>'
            f'<marker id="{k}-many" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">'
            f'<path d="M0 6 H12 M2 6 L12 1 M2 6 L12 11" fill="none" stroke="{LINE}" stroke-width="1.4"/></marker>'
            f'<marker id="{k}-one" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">'
            f'<path d="M0 6 H12 M7 1 V11" fill="none" stroke="{LINE}" stroke-width="1.4"/></marker>'
            f'<marker id="{k}-dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7">'
            f'<circle cx="5" cy="5" r="4" fill="{LINE}"/></marker>'
            "</defs>"
        )

    def svg(self, standalone: bool = True) -> str:
        style = (
            f"text{{font-family:{FONT};}} .halo{{paint-order:stroke;stroke:#ffffff;stroke-width:4px;stroke-linejoin:round;}}"
            " .node:focus{outline:none;} .node:focus > :first-child, .node:focus > rect{stroke-width:2.6;}"
        )
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" width="{self.width}" '
                f'height="{self.height}" role="img" aria-labelledby="{self.key}-t {self.key}-d" data-diagram="{self.key}">')
        body = (f'<title id="{self.key}-t">{esc(self.title)}</title><desc id="{self.key}-d">{esc(self.desc)}</desc>'
                f"<style>{style}</style>{self._defs()}"
                f'<rect width="{self.width}" height="{self.height}" fill="{CANVAS}"/>'
                + "".join(self._back) + "".join(self._edges_svg) + "".join(self._nodes_svg) + "".join(self._front))
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n' if standalone else ""
        return f"{xml}{head}{body}</svg>\n"


# ---- routing helpers ----------------------------------------------------------------------------------

def hv(a: tuple[float, float], b: tuple[float, float]) -> list[tuple[float, float]]:
    """Horizontal first, then vertical."""
    return [a, (b[0], a[1]), b]


def vh(a: tuple[float, float], b: tuple[float, float]) -> list[tuple[float, float]]:
    """Vertical first, then horizontal."""
    return [a, (a[0], b[1]), b]


def hvh(a: tuple[float, float], b: tuple[float, float], x: float | None = None) -> list[tuple[float, float]]:
    mid = (a[0] + b[0]) / 2 if x is None else x
    return [a, (mid, a[1]), (mid, b[1]), b]


def vhv(a: tuple[float, float], b: tuple[float, float], y: float | None = None) -> list[tuple[float, float]]:
    mid = (a[1] + b[1]) / 2 if y is None else y
    return [a, (a[0], mid), (b[0], mid), b]
