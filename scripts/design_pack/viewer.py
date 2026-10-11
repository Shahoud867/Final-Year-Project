"""The interactive design pack: one self-contained HTML file (no external requests) holding every diagram."""

from __future__ import annotations

import html
import json

from . import Sheet

ORDER = ["Structure", "Behaviour", "Data", "Algorithms", "Deployment"]

_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Granite design pack (FYP-1 Mid)</title>
<style>
:root { --bg:#f4f6f9; --surface:#ffffff; --ink:#1b2430; --muted:#586474; --line:#d5dbe3; --accent:#3b6fd4; --accent-bg:#e8f0fe; }
* { box-sizing: border-box; }
html, body { height: 100%; }
body { margin: 0; font: 14px/1.5 'Segoe UI', system-ui, -apple-system, Roboto, Arial, sans-serif; color: var(--ink); background: var(--bg); }
.app { display: grid; grid-template-columns: 290px 1fr; grid-template-rows: auto 1fr; height: 100vh; }
header { grid-column: 1 / -1; background: var(--surface); border-bottom: 1px solid var(--line); padding: 10px 18px; display: flex; gap: 16px; align-items: baseline; flex-wrap: wrap; }
header h1 { font-size: 17px; margin: 0; }
header p { margin: 0; color: var(--muted); font-size: 13px; }
nav { background: var(--surface); border-right: 1px solid var(--line); overflow: auto; padding: 12px; }
nav input { width: 100%; padding: 7px 10px; border: 1px solid var(--line); border-radius: 8px; font: inherit; }
nav h2 { font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); margin: 16px 6px 4px; }
nav ul { list-style: none; margin: 0; padding: 0; }
nav button { width: 100%; text-align: left; border: 0; background: none; font: inherit; color: var(--ink); padding: 6px 8px; border-radius: 7px; cursor: pointer; }
nav button small { display: block; color: var(--muted); font-size: 11.5px; }
nav button:hover { background: #eef1f5; }
nav button[aria-current="true"] { background: var(--accent-bg); box-shadow: inset 3px 0 0 var(--accent); }
main { overflow: hidden; display: grid; grid-template-rows: auto 1fr auto; min-width: 0; }
.bar { display: flex; gap: 8px; align-items: center; padding: 8px 14px; background: var(--surface); border-bottom: 1px solid var(--line); flex-wrap: wrap; }
.bar h2 { font-size: 15px; margin: 0 8px 0 0; }
.bar .tag { background: var(--accent-bg); color: #254f9e; border-radius: 99px; padding: 1px 10px; font-size: 12px; white-space: nowrap; }
.bar .spacer { flex: 1; }
.bar button { font: inherit; border: 1px solid var(--line); background: var(--surface); border-radius: 7px; padding: 4px 10px; cursor: pointer; min-width: 34px; }
.bar button:hover { background: #eef1f5; }
.stage { overflow: auto; background: #e9edf2; cursor: grab; padding: 14px; }
.stage.dragging { cursor: grabbing; user-select: none; }
.sheet svg { display: block; background: #fff; box-shadow: 0 1px 4px rgba(20, 30, 50, .18); border-radius: 4px; max-width: none; height: auto; }
.sheet[hidden] { display: none; }
.info { background: var(--surface); border-top: 1px solid var(--line); padding: 10px 18px 12px; max-height: 34vh; overflow: auto; display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: 6px 26px; }
.info h3 { font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); margin: 0 0 2px; }
.info p { margin: 0 0 8px; }
.info ul { margin: 0; padding-left: 18px; }
.info code { font: 12px ui-monospace, Consolas, monospace; background: #f1f3f6; padding: 0 4px; border-radius: 4px; overflow-wrap: anywhere; }
.hint { color: var(--muted); font-size: 12px; }
svg .node { cursor: pointer; }
svg .dim { opacity: .14; transition: opacity .15s; }
svg .hit > path { stroke: #d9480f; stroke-width: 2.4; }
:focus-visible { outline: 3px solid #2563eb; outline-offset: 1px; }
@media (max-width: 860px) { .app { grid-template-columns: 1fr; grid-template-rows: auto auto 1fr; height: auto; } nav { max-height: 38vh; border-right: 0; border-bottom: 1px solid var(--line); } .info { grid-template-columns: 1fr; max-height: none; } main { min-height: 80vh; } }
@media (prefers-reduced-motion: reduce) { svg .dim { transition: none; } }
@media print { nav, .bar button, .hint { display: none; } .app { display: block; height: auto; } .stage { overflow: visible; background: #fff; padding: 0; } .sheet svg { width: 100% !important; box-shadow: none; } .info { max-height: none; } }
</style>
</head>
<body>
<div class="app">
<header>
  <h1>Granite design pack</h1>
  <p>FYP-1 Mid · __COUNT__ design artefacts generated from the code · handbook Table 1a, Iteration 1 design phase</p>
</header>
<nav aria-label="Design artefacts">
  <label class="hint" for="q">Search</label>
  <input id="q" type="search" placeholder="name, handbook item, file…" autocomplete="off">
  __NAV__
  <p class="hint" style="margin:14px 6px 0">Keys: ← → previous and next · + − zoom · 0 fit · click a box to see what it connects to.</p>
</nav>
<main>
  <div class="bar">
    <h2 id="title"></h2><span class="tag" id="item"></span><span class="tag" id="cat"></span>
    <span class="spacer"></span>
    <button id="prev" title="Previous diagram" aria-label="Previous diagram">←</button>
    <button id="next" title="Next diagram" aria-label="Next diagram">→</button>
    <button id="zout" title="Zoom out" aria-label="Zoom out">−</button>
    <button id="zin" title="Zoom in" aria-label="Zoom in">+</button>
    <button id="fit" title="Fit to width">Fit</button>
    <button id="full" title="Actual size">100%</button>
    <button id="clear" title="Clear highlight">Clear highlight</button>
  </div>
  <div class="stage" id="stage" tabindex="0" aria-label="Diagram; drag or scroll to pan">__SHEETS__</div>
  <section class="info" aria-live="polite">
    <div><h3>What it shows</h3><p id="explain"></p><h3>How it is kept true to the code</h3><p id="derived"></p></div>
    <div><h3>Drawn from</h3><ul id="sources"></ul><p class="hint" id="picked"></p></div>
  </section>
</main>
</div>
<script>
const SHEETS = __DATA__;
const byKey = Object.fromEntries(SHEETS.map((s, i) => [s.key, i]));
const stage = document.getElementById('stage');
let current = 0, zoom = 1;
const svgOf = (i) => document.querySelector('#sheet-' + SHEETS[i].key + ' svg');
function applyZoom() { const s = svgOf(current); s.style.width = (SHEETS[current].width * zoom) + 'px'; }
function fit() { zoom = Math.max(0.2, Math.min(1.6, (stage.clientWidth - 30) / SHEETS[current].width)); applyZoom(); }
function clearPick() {
  document.querySelectorAll('svg .dim, svg .hit').forEach(e => e.classList.remove('dim', 'hit'));
  document.getElementById('picked').textContent = '';
}
function show(i, push) {
  current = (i + SHEETS.length) % SHEETS.length;
  const s = SHEETS[current];
  document.querySelectorAll('.sheet').forEach(e => { e.hidden = e.id !== 'sheet-' + s.key; });
  document.querySelectorAll('nav button').forEach(b => b.setAttribute('aria-current', b.dataset.key === s.key ? 'true' : 'false'));
  document.getElementById('title').textContent = s.title;
  document.getElementById('item').textContent = 'Table 1a: ' + s.table1a;
  document.getElementById('cat').textContent = s.category;
  document.getElementById('explain').textContent = s.explanation;
  document.getElementById('derived').textContent = s.derived;
  const ul = document.getElementById('sources'); ul.textContent = '';
  s.sources.forEach(p => { const li = document.createElement('li'); const c = document.createElement('code'); c.textContent = p; li.appendChild(c); ul.appendChild(li); });
  clearPick(); fit(); stage.scrollTo(0, 0);
  if (push !== false) history.replaceState(null, '', '#' + s.key);
  document.title = s.title + ' · Granite design pack';
}
function pick(node) {
  const svg = node.closest('svg'), id = node.dataset.id;
  clearPick();
  const near = new Set([id]); let n = 0;
  svg.querySelectorAll('.edge').forEach(e => {
    const hit = e.dataset.from === id || e.dataset.to === id;
    if (hit) { e.classList.add('hit'); near.add(e.dataset.from); near.add(e.dataset.to); n++; } else e.classList.add('dim');
  });
  svg.querySelectorAll('.node').forEach(x => { if (!near.has(x.dataset.id)) x.classList.add('dim'); });
  document.getElementById('picked').textContent = n ? 'Selected "' + id + '": ' + n + ' connection(s) highlighted.' : 'Selected "' + id + '": no connectors start or end here.';
}
document.querySelectorAll('nav button').forEach(b => b.addEventListener('click', () => show(byKey[b.dataset.key])));
document.querySelectorAll('svg .node').forEach(n => {
  n.addEventListener('click', (e) => { e.stopPropagation(); pick(n); });
  n.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(n); } });
});
stage.addEventListener('click', clearPick);
document.getElementById('prev').onclick = () => show(current - 1);
document.getElementById('next').onclick = () => show(current + 1);
document.getElementById('zin').onclick = () => { zoom = Math.min(3, zoom * 1.2); applyZoom(); };
document.getElementById('zout').onclick = () => { zoom = Math.max(0.2, zoom / 1.2); applyZoom(); };
document.getElementById('fit').onclick = fit;
document.getElementById('full').onclick = () => { zoom = 1; applyZoom(); };
document.getElementById('clear').onclick = clearPick;
document.getElementById('q').addEventListener('input', (e) => {
  const q = e.target.value.trim().toLowerCase();
  document.querySelectorAll('nav li').forEach(li => { li.hidden = q && !li.dataset.search.includes(q); });
});
document.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT') return;
  if (e.key === 'ArrowRight') show(current + 1); else if (e.key === 'ArrowLeft') show(current - 1);
  else if (e.key === '+' || e.key === '=') document.getElementById('zin').click();
  else if (e.key === '-') document.getElementById('zout').click();
  else if (e.key === '0') fit();
  else if (e.key === '/') { e.preventDefault(); document.getElementById('q').focus(); }
  else if (e.key === 'Escape') clearPick();
});
let drag = null;
stage.addEventListener('mousedown', (e) => { if (e.target.closest('.node')) return; drag = { x: e.clientX, y: e.clientY, l: stage.scrollLeft, t: stage.scrollTop }; stage.classList.add('dragging'); });
window.addEventListener('mousemove', (e) => { if (!drag) return; stage.scrollLeft = drag.l - (e.clientX - drag.x); stage.scrollTop = drag.t - (e.clientY - drag.y); });
window.addEventListener('mouseup', () => { drag = null; stage.classList.remove('dragging'); });
window.addEventListener('resize', fit);
window.addEventListener('hashchange', () => { const k = location.hash.slice(1); if (k in byKey) show(byKey[k], false); });
show(byKey[location.hash.slice(1)] ?? 0, false);
</script>
</body>
</html>
"""


def build_viewer(sheets: list[Sheet]) -> str:
    nav = []
    for cat in ORDER:
        group = [s for s in sheets if s.category == cat]
        if not group:
            continue
        nav.append(f"<h2>{html.escape(cat)}</h2><ul>")
        for s in group:
            search = html.escape(" ".join([s.diagram.title, s.table1a, cat, *s.sources]).lower(), quote=True)
            nav.append(f'<li data-search="{search}"><button type="button" data-key="{s.key}">{html.escape(s.diagram.title)}'
                       f"<small>{html.escape(s.table1a)}</small></button></li>")
        nav.append("</ul>")
    ordered = [s for cat in ORDER for s in sheets if s.category == cat]
    data = [{"key": s.key, "title": s.diagram.title, "category": s.category, "table1a": s.table1a, "explanation": s.explanation,
             "derived": s.derived, "sources": s.sources, "width": s.diagram.width, "height": s.diagram.height} for s in ordered]
    body = "".join(f'<div class="sheet" id="sheet-{s.key}" hidden>{s.diagram.svg(standalone=False)}</div>' for s in ordered)
    return (_PAGE.replace("__COUNT__", str(len(sheets))).replace("__NAV__", "".join(nav)).replace("__SHEETS__", body)
            .replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
