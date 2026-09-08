// Granite — Proposal Defense Deck generator
// Produces Granite_Proposal_Defense.pptx from real project data.
// Palette, layout and content match markdowns/05-deliverables/Proposal_Defense_Slide_Content_Spec.md
const pptxgen = require("pptxgenjs");

// ---------- Palette ("Granite" — dark graphite stone + gold vein, consistent with poc-demo & the Architecture Atlas) ----------
const C = {
  bgDark: "1B1E25",
  bgDark2: "20232B",
  bgLight: "FFFFFF",
  card: "F0F1F4",
  cardAlt: "E7E9EE",
  textDark: "20232B",
  textMuted: "5B6270",
  textFaint: "8A8FA0",
  textLight: "F4F5F7",
  textLightMuted: "AEB4C2",
  accent: "B87F31",
  accentLight: "D9A15C",
  accentDark: "8A5F22",
  green: "2F7A4F",
  greenSoft: "E7F1EA",
  amber: "9A6B12",
  amberSoft: "F5EDDA",
  red: "A6392F",
  redSoft: "F5E5E2",
  teal: "1F7D84",
  tealSoft: "E4F0F1",
  orange: "B5601F",
  orangeSoft: "F5E9DD",
  blue: "2F5F9E",
  blueSoft: "E4EAF3",
  border: "D8DAE1",
};
const F_TITLE = "Cambria";
const F_BODY = "Calibri";
const F_MONO = "Courier New";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "Granite — F26-060";
pres.company = "FAST School of Computing, NUCES";
pres.title = "Granite — Proposal Defense";

const PW = 13.333, PH = 7.5;
const MX = 0.55; // side margin
const CW = PW - MX * 2; // content width

// ---------- helpers ----------
function chrome(slide, num, title, kicker) {
  slide.addText(kicker.toUpperCase(), {
    x: MX, y: 0.32, w: CW, h: 0.28, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 11, bold: true, color: C.accentDark, charSpacing: 1.5,
  });
  slide.addText(title, {
    x: MX, y: 0.58, w: CW, h: 0.62, isTextBox: true, margin: 0,
    fontFace: F_TITLE, fontSize: 28, bold: true, color: C.textDark,
  });
  slide.addShape(pres.ShapeType.rect, { x: MX, y: 1.28, w: 0.5, h: 0.035, fill: { color: C.accent } });
  pageNum(slide, num);
}
function pageNum(slide, n) {
  slide.addText(`${n} / 10  ·  F26-060-Granite`, {
    x: PW - 3.0, y: PH - 0.42, w: 2.5, h: 0.28, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 9, color: C.textFaint, align: "right",
  });
}
function card(slide, x, y, w, h, fill) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.08,
    fill: { color: fill || C.card }, line: { color: C.border, width: 0.75 },
  });
}
function chip(slide, x, y, w, text, fg, bg) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h: 0.28, rectRadius: 0.14, fill: { color: bg }, line: { type: "none" },
  });
  slide.addText(text, {
    x, y, w, h: 0.28, isTextBox: true, margin: 0, align: "center", valign: "middle",
    fontFace: F_MONO, fontSize: 9, bold: true, color: fg,
  });
}
function iconCircle(slide, x, y, d, bg, label, fg) {
  slide.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: bg }, line: { type: "none" } });
  slide.addText(label, {
    x, y, w: d, h: d, isTextBox: true, margin: 0, align: "center", valign: "middle",
    fontFace: F_TITLE, fontSize: d > 0.5 ? 18 : 13, bold: true, color: fg,
  });
}
function bullets(slide, items, opts) {
  const arr = items.map((t, i) => ({
    text: t, options: { bullet: { code: "2022", indent: 14 }, breakLine: i < items.length - 1 },
  }));
  slide.addText(arr, Object.assign({
    isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 12.5, color: C.textDark,
    paraSpaceAfter: 8, valign: "top",
  }, opts));
}

// ============================================================
// SLIDE 1 — Title & one-line problem
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bgDark };
  // faceted mark (granite motif — cut-stone facets)
  const mx = PW - 2.7, my = 0.9;
  s.addShape(pres.ShapeType.rect, { x: mx, y: my, w: 1.1, h: 1.1, rotate: 45, fill: { color: C.accent }, line: { type: "none" } });
  s.addShape(pres.ShapeType.rect, { x: mx + 0.28, y: my + 0.28, w: 0.54, h: 0.54, rotate: 45, fill: { color: C.bgDark }, line: { color: C.accentLight, width: 1 } });

  s.addText("F26-060 · PROPOSAL DEFENSE · STREAM A — RESEARCH-DERIVED", {
    x: MX, y: 1.5, w: 9.5, h: 0.32, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 12, bold: true, color: C.accentLight, charSpacing: 1.5,
  });
  s.addText("Granite", {
    x: MX, y: 1.85, w: 9.5, h: 1.1, isTextBox: true, margin: 0,
    fontFace: F_TITLE, fontSize: 64, bold: true, color: C.textLight,
  });
  s.addText("A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery", {
    x: MX, y: 2.95, w: 8.6, h: 0.6, isTextBox: true, margin: 0,
    fontFace: F_BODY, fontSize: 16, italic: true, color: C.textLightMuted,
  });

  s.addShape(pres.ShapeType.line, { x: MX, y: 3.75, w: 8.6, h: 0, line: { color: "3A3F4C", width: 1 } });

  s.addText("When a multi-agent AI system fails — including when the wrong answer looks completely right — no published method can reliably say which agent caused it, and none can verify a fix before trusting it.", {
    x: MX, y: 3.95, w: 8.6, h: 1.1, isTextBox: true, margin: 0,
    fontFace: F_TITLE, fontSize: 19, color: C.textLight, italic: true,
  });

  const team = [
    ["Shahoud Shahid", "23i-2515"], ["Muhammad Noor", "23i-2520"], ["Saif Shahzad", "23i-2634"],
  ];
  let tx = MX;
  team.forEach(([n, r]) => {
    s.addText([{ text: n, options: { bold: true, breakLine: true, fontSize: 12.5 } }, { text: r, options: { fontSize: 10.5 } }], {
      x: tx, y: 5.55, w: 2.75, h: 0.6, isTextBox: true, margin: 0, fontFace: F_BODY, color: C.textLight,
    });
    tx += 2.85;
  });
  s.addShape(pres.ShapeType.line, { x: MX, y: 5.45, w: 8.6, h: 0, line: { color: "3A3F4C", width: 0.75 } });

  s.addText([
    { text: "Supervisor  ", options: { color: C.textLightMuted, fontSize: 11 } },
    { text: "Dr. Adil Majeed", options: { color: C.textLight, bold: true, fontSize: 12.5, breakLine: true } },
    { text: "FAST School of Computing, NUCES Islamabad", options: { color: C.textLightMuted, fontSize: 10.5 } },
  ], { x: MX, y: 6.5, w: 6, h: 0.6, isTextBox: true, margin: 0, fontFace: F_BODY });

  s.addNotes("Say the one-line problem exactly as written — WHO (teams running multi-agent systems), WHAT fails (attribution + silent failures), WHY it matters (nobody can verify a fix), in one breath. Do not explain the title word-by-word — slide 6 does that.");
}

// ============================================================
// SLIDE 2 — Stakeholders, problem & current workflow
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bgLight };
  chrome(s, 2, "Stakeholders, Problem & Current Workflow", "Who has this, and where it breaks");

  // left: stakeholders
  card(s, MX, 1.55, 5.5, 2.55, C.card);
  s.addText("STAKEHOLDERS", { x: MX + 0.25, y: 1.72, w: 5, h: 0.28, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 10, bold: true, color: C.accentDark, charSpacing: 1 });
  bullets(s, [
    "Primary — an engineering team operating a multi-agent AI system in or near production (grounded in a customer-support / retail workflow, our active benchmark substrate)",
    "Secondary — downstream product teams consuming the diagnosis output",
    "Secondary — auditors / compliance reviewers who need traceable evidence of what went wrong",
  ], { x: MX + 0.25, y: 2.05, w: 5.0, h: 1.95 });

  card(s, MX, 4.25, 5.5, 1.0, C.tealSoft);
  s.addText([{ text: "SDG 9  ", options: { bold: true, color: C.teal, fontSize: 12 } }, { text: "Industry, Innovation & Infrastructure (target 9.5) — reliability tooling for a new industrial category", options: { color: C.textDark, fontSize: 11.5 } }], {
    x: MX + 0.25, y: 4.4, w: 5.0, h: 0.7, isTextBox: true, margin: 0, fontFace: F_BODY,
  });

  card(s, MX, 5.4, 5.5, 1.5, C.redSoft);
  s.addText("CONSEQUENCE", { x: MX + 0.25, y: 5.55, w: 5, h: 0.25, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 10, bold: true, color: C.red, charSpacing: 1 });
  s.addText("A missed silent failure ships a confident, wrong answer to an end user — undetected.", {
    x: MX + 0.25, y: 5.82, w: 5.0, h: 1.0, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 12.5, color: C.textDark, italic: true,
  });

  // right: current workflow process strip (vertical)
  const rx = 6.4, rw = CW - (rx - MX);
  s.addText("CURRENT WORKFLOW — NO GRANITE", { x: rx, y: 1.55, w: rw, h: 0.28, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 10, bold: true, color: C.textMuted, charSpacing: 1 });
  const steps = [
    ["1", "Observability platform captures the trace", "LangSmith / Langfuse / Braintrust / Arize", C.blue, C.blueSoft],
    ["2", "A human reads the trace and guesses the root cause", "no automated attribution with published accuracy", C.orange, C.orangeSoft],
    ["3", "No systematic silent-failure check", "a confident, well-formed, wrong answer with no error signal passes unnoticed", C.red, C.redSoft],
    ["4", "No way to test a fix before redeploying", "field baseline: single-model guess scores 14.2% step accuracy (Who&When)", C.red, C.redSoft],
  ];
  let sy = 2.0;
  steps.forEach(([n, t, sub, fg, bg]) => {
    iconCircle(s, rx, sy, 0.42, bg, n, fg);
    s.addText([{ text: t, options: { bold: true, breakLine: true, fontSize: 12.5, color: C.textDark } }, { text: sub, options: { fontSize: 10.5, color: C.textMuted } }], {
      x: rx + 0.58, y: sy - 0.03, w: rw - 0.6, h: 0.85, isTextBox: true, margin: 0, fontFace: F_BODY,
    });
    if (n !== "4") s.addShape(pres.ShapeType.line, { x: rx + 0.21, y: sy + 0.42, w: 0, h: 0.42, line: { color: C.border, width: 1.5, dashType: "dash" } });
    sy += 1.18;
  });

  s.addNotes("The stakeholder line is what turns CCP characteristic #6 from weak to clear — name who was actually contacted, or say plainly this is still in progress and name the date it closes. 14.2% is the field's own measured baseline for 'a human reads the trace' — the number the whole project is trying to beat.");
}

// ============================================================
// SLIDE 3 — Existing solutions & prior FYP comparison
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bgLight };
  chrome(s, 3, "Existing Solutions & Prior FYP Comparison", "Proving the gap is structural, not a missing feature");

  const cols = ["", "Core approach", "Step-level attribution\n(published accuracy)", "Silent-failure\ndetection", "Counterfactual fix-\ntesting, measured", "Framework-\nagnostic"];
  const rows = [
    ["ErrorProbe\n(ACL 2026)", "3-stage LLM diagnosis\n+ memory", "59.5%", "✘ admits\nit cannot", "✘", "✘ 2 archs only"],
    ["LangSmith Engine /\nArize Alyx (2026)", "Automated RCA\n+ fix drafting", "not published", "not confirmed", "not confirmed", "✘ stack-locked"],
    ["Langfuse / Braintrust /\nPhoenix / Maxim / Opik", "Trace capture\n+ eval", "human-driven", "RAG-groundedness\nonly", "✘", "✘"],
    ["Closest prior FYP\n(S24-011-D-HDLM,\nSpring 2024)", "Hallucination detection\nin single-LLM text", "—\nno attribution at all", "partial — single-LLM\ntext only, not agent traces", "✘ no repair/\nreplay step", "N/A — not a\nmulti-agent system"],
    ["Current manual\nworkflow", "human reads,\nguesses", "14.2%\n(Who&When)", "✘", "✘", "N/A"],
    ["Granite\n(proposed)", "Constraint-based SED\n+ verified repair loop", "building on\nErrorProbe", "✓ scoped &\nmeasured", "✓ recovery rate\nover N replays", "✓ CrewAI +\nLangGraph, unseen"],
  ];
  const tRows = [cols.map(c => ({ text: c, options: { bold: true, fill: { color: C.bgDark2 }, color: C.textLight, fontSize: 9.5, align: "center", valign: "middle" } }))];
  rows.forEach((r, ri) => {
    const isGranite = ri === rows.length - 1;
    const isPrior = ri === 3;
    tRows.push(r.map((c, ci) => ({
      text: c,
      options: {
        fontSize: 9.5, align: ci === 0 ? "left" : "center", valign: "middle",
        bold: ci === 0 || isGranite,
        fill: { color: isGranite ? C.tealSoft : (isPrior ? C.amberSoft : (ri % 2 === 0 ? C.bgLight : C.card)) },
        color: isPrior && ci > 0 ? C.textFaint : C.textDark,
        italic: isPrior && ci > 0,
      },
    })));
  });
  s.addTable(tRows, {
    x: MX, y: 1.55, w: CW, h: 4.55,
    colW: [1.55, 2.15, 2.05, 1.85, 2.15, 1.9],
    border: { type: "solid", color: C.border, pt: 0.5 },
    autoPage: false, fontFace: F_BODY,
  });

  card(s, MX, 6.25, CW, 0.85, C.amberSoft);
  s.addText([{ text: "The real gap:  ", options: { bold: true, color: C.amber } }, { text: "no system checked — academic or commercial — confirms step-level attribution accuracy together with general silent-failure detection and counterfactual fix verification and cross-architecture generalization, evaluated as one pipeline.", options: { color: C.textDark } }], {
    x: MX + 0.25, y: 6.4, w: CW - 0.5, h: 0.6, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11.5,
  });

  s.addNotes("Volunteer the correction story: an early draft said 'nobody automates this' — direct vendor checks proved that stale, corrected on the record (R9). The gap is the combination, not any single missing feature — say this before being asked.");
}

// ============================================================
// SLIDE 4 — Research & technical basis
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bgLight };
  chrome(s, 4, "Research & Technical Basis", "9+ papers read in full — decisions, not decoration");

  // left column: decisions
  const lx = MX, lw = 6.6;
  s.addText("DECISIONS THE LITERATURE INFLUENCED", { x: lx, y: 1.55, w: lw, h: 0.28, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 10, bold: true, color: C.accentDark, charSpacing: 1 });
  const decisions = [
    ["ErrorProbe chosen as baseline", "on performance (59.5%, beats its ancestors on their own benchmarks), not recency"],
    ["CrewAI + LangGraph committed", "neither used by any of the 9 papers reviewed — the actual test of generalization"],
    ["Constraint-based SED, not LLM-judge", "“From Confident Closing to Silent Failure” (arXiv:2606.09863): LLM-judge AUROC ≤ 0.65 on tau2-bench/AppWorld"],
    ["Single-framework narrowing rejected", "the market survey's own advice, declined — would delete the cross-architecture research question (R19)"],
  ];
  let dy = 1.9;
  decisions.forEach(([t, sub]) => {
    iconCircle(s, lx, dy, 0.3, C.accentLight, "✓", C.bgDark);
    s.addText([{ text: t, options: { bold: true, breakLine: true, fontSize: 12, color: C.textDark } }, { text: sub, options: { fontSize: 10.5, color: C.textMuted } }], {
      x: lx + 0.45, y: dy - 0.06, w: lw - 0.5, h: 0.95, isTextBox: true, margin: 0, fontFace: F_BODY,
    });
    dy += 1.12;
  });

  // right column: lineage chart
  const rx = 7.5, rw = CW - (rx - MX);
  s.addText("PUBLISHED STEP-ACCURACY LINEAGE", { x: rx, y: 1.55, w: rw, h: 0.28, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 10, bold: true, color: C.accentDark, charSpacing: 1 });
  s.addChart(pres.ChartType.bar, [{
    name: "Step accuracy",
    labels: ["Who&When\n(single-LLM)", "AgenTracer", "ErrorProbe\n(chosen baseline)"],
    values: [14.2, 40.0, 59.5],
  }], {
    x: rx, y: 1.9, w: rw, h: 2.4,
    barDir: "col", chartColors: [C.accent],
    showTitle: false, showLegend: false,
    showValue: true, dataLabelPosition: "outEnd", dataLabelColor: C.textDark, dataLabelFontSize: 11, dataLabelFontBold: true,
    catAxisLabelColor: C.textMuted, catAxisLabelFontSize: 9.5, catAxisLabelFontFace: F_BODY,
    valAxisLabelColor: C.textMuted, valAxisLabelFontSize: 9, valAxisMaxVal: 70, valAxisMinVal: 0,
    valGridLine: { color: C.border, size: 0.5 }, catGridLine: { style: "none" },
    valAxisHidden: false, plotArea: { fill: { color: C.bgLight } },
  });
  card(s, rx, 4.5, rw, 1.0, C.redSoft);
  s.addText([{ text: "40.5 points still wrong  ", options: { bold: true, color: C.red } }, { text: "— the best published method misattributes the origin step 4 times in 10, and confesses it cannot see silent failures at all.", options: { color: C.textDark } }], {
    x: rx + 0.2, y: 4.63, w: rw - 0.4, h: 0.75, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11,
  });

  card(s, rx, 5.7, rw, 1.15, C.card);
  s.addText("BACKBONE-CONFOUND CAVEAT (stated up front)", { x: rx + 0.2, y: 5.83, w: rw - 0.4, h: 0.25, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9, bold: true, color: C.textMuted, charSpacing: 0.5 });
  s.addText("Cross-paper comparisons use different LLM backbones — a win partly reflects backbone strength. Controlled for within Granite's own experiments (R4).", {
    x: rx + 0.2, y: 6.08, w: rw - 0.4, h: 0.7, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.5, color: C.textDark,
  });

  s.addNotes("State the backbone-confound caveat before being asked. Name that credible unpublished preprints exist in adjacent territory and the team made a recorded decision not to chase every one — the strategy is beating a peer-reviewed baseline, not pre-empting unpublished work.");
}

// ============================================================
// SLIDE 5 — CCP justification
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bgLight };
  chrome(s, 5, "Complex Computing Problem — Seoul Accord Justification", "8 of 9 characteristics clear, evidenced not asserted");

  const items = [
    ["1", "Conflicting requirements", "Diagnostic depth vs. latency; trace completeness vs. privacy; generalization vs. specialization", true],
    ["2", "No obvious solution", "Best published step accuracy still 59.5% after 15 months, 7 papers", true],
    ["3", "Depth of knowledge", "Execution-graph modeling, causal/counterfactual reasoning, distributed tracing, eval methodology", true],
    ["4", "Unfamiliar issues", "Delayed error manifestation, LLM non-determinism, cross-architecture generalization", true],
    ["5", "Beyond standard practice", "No off-the-shelf framework solves attribution + silent-failure detection + recovery", true],
    ["6", "Diverse stakeholders", "Operators, product teams, auditors named; real contact still open", false],
    ["7", "Significant consequences", "A missed silent failure ships a wrong answer, undetected", true],
    ["8", "Interdependence", "Failures propagate through interdependent agents — the execution graph models this directly", true],
    ["9", "Ill-defined cause", "3 genuine unknowns at diagnosis time: whether, which agent/step, what the correct behavior was", true],
  ];
  const cols3 = 3, rowH = 1.55, colW = CW / cols3;
  items.forEach(([n, t, sub, clear], i) => {
    const cx = MX + (i % cols3) * colW, cy = 1.55 + Math.floor(i / cols3) * rowH;
    card(s, cx, cy, colW - 0.2, rowH - 0.18, clear ? C.greenSoft : C.amberSoft);
    iconCircle(s, cx + 0.18, cy + 0.16, 0.36, clear ? C.green : C.amber, n, C.textLight);
    s.addText(t, { x: cx + 0.65, y: cy + 0.14, w: colW - 1.0, h: 0.4, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 12.5, bold: true, color: C.textDark });
    s.addText(sub, { x: cx + 0.18, y: cy + 0.58, w: colW - 0.55, h: 0.75, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.7, color: C.textMuted });
    chip(s, cx + colW - 1.1, cy + rowH - 0.42, 0.85, clear ? "CLEAR" : "WEAK", C.textLight, clear ? C.green : C.amber);
  });

  s.addNotes("Read characteristic 9's resolution aloud if asked why this is complex — the strongest, most concrete sentence in the plan. The guide's own worked examples clear 6–9 characteristics; this clears 8, ahead of most benchmark examples.");
}

// ============================================================
// SLIDE 6 — Proposed solution & contribution
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bgLight };
  chrome(s, 6, "Proposed Solution & Contribution", "What is actually being built, and where the boundary sits");

  card(s, MX, 1.55, CW, 1.0, C.card);
  s.addText([
    { text: "Contribution.  ", options: { bold: true, color: C.accentDark, fontSize: 11.5 } },
    { text: "Existing methods reach up to 59.5% step accuracy but remain weak under two conditions: none is evaluated on an architecture absent from its own benchmark construction, and the strongest admits it cannot catch silent failures. We are building a cross-architecture fault-injection benchmark and a diagnosis pipeline with constraint-based silent-failure verification, packaged as a framework-agnostic testing SDK.", options: { color: C.textDark, fontSize: 11 } },
  ], { x: MX + 0.25, y: 1.7, w: CW - 0.5, h: 0.85, isTextBox: true, margin: 0, fontFace: F_BODY, valign: "middle" });

  // Architecture diagram — 3 lanes inside a boundary, operator + target outside, LLM API external
  const ax = MX, ay = 2.75, aw = CW, ah = 3.65;
  // target + operator
  s.addShape(pres.ShapeType.roundRect, { x: ax, y: ay + 0.2, w: 1.65, h: 0.85, rectRadius: 0.06, fill: { color: C.bgLight }, line: { color: C.textMuted, width: 1, dashType: "dash" } });
  s.addText([{ text: "Target System", options: { bold: true, breakLine: true, fontSize: 10 } }, { text: "CrewAI / LangGraph", options: { fontSize: 8.5, color: C.textMuted } }], { x: ax + 0.1, y: ay + 0.28, w: 1.45, h: 0.7, isTextBox: true, margin: 0, fontFace: F_BODY, align: "center", valign: "middle", color: C.textDark });
  s.addShape(pres.ShapeType.roundRect, { x: ax, y: ay + 2.55, w: 1.65, h: 0.85, rectRadius: 0.06, fill: { color: C.bgLight }, line: { color: C.textMuted, width: 1, dashType: "dash" } });
  s.addText([{ text: "Operator", options: { bold: true, breakLine: true, fontSize: 10 } }, { text: "engineering team", options: { fontSize: 8.5, color: C.textMuted } }], { x: ax + 0.1, y: ay + 2.63, w: 1.45, h: 0.7, isTextBox: true, margin: 0, fontFace: F_BODY, align: "center", valign: "middle", color: C.textDark });

  // boundary
  const bx = ax + 1.95, bw = 8.2;
  s.addShape(pres.ShapeType.roundRect, { x: bx, y: ay, w: bw, h: ah, rectRadius: 0.1, fill: { color: "FDFDFE" }, line: { color: C.textMuted, width: 1, dashType: "dash" } });
  s.addText("GRANITE — SYSTEM BOUNDARY", { x: bx + 0.15, y: ay + 0.05, w: 4, h: 0.22, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 8, bold: true, color: C.accentDark, charSpacing: 1 });

  const lanes = [
    ["LANE A — DATA / BENCHMARK · SHAHOUD", "Framework Adapters   ·   Fault Injection   ·   Benchmark Store", C.teal, C.tealSoft],
    ["LANE B — DIAGNOSIS · NOOR", "Trace Normalizer → Graph Builder → Semantic Error Diagnostic + Backward Causal Tracer", C.orange, C.orangeSoft],
    ["LANE C — PLATFORM · SAIF", "Repair Agent → Verified Automatic Repair → Recovery Controller / Memory (Tier 2) → API → Dashboard", C.blue, C.blueSoft],
  ];
  let ly = ay + 0.32;
  const laneH = 0.98;
  lanes.forEach(([label, content, fg, bg], i) => {
    s.addShape(pres.ShapeType.roundRect, { x: bx + 0.15, y: ly, w: bw - 1.9, h: laneH - 0.12, rectRadius: 0.06, fill: { color: bg }, line: { color: fg, width: 1 } });
    s.addText(label, { x: bx + 0.3, y: ly + 0.06, w: bw - 2.2, h: 0.22, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 8.5, bold: true, color: fg });
    s.addText(content, { x: bx + 0.3, y: ly + 0.3, w: bw - 2.2, h: 0.5, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.5, color: C.textDark });
    if (i < 2) s.addShape(pres.ShapeType.line, { x: bx + (bw - 1.9) / 2, y: ly + laneH - 0.12, w: 0, h: 0.12, line: { color: C.textMuted, width: 1.25, endArrowType: "triangle" } });
    ly += laneH;
  });

  // LLM API external
  s.addShape(pres.ShapeType.roundRect, { x: bx + bw - 1.55, y: ay + 0.35, w: 1.4, h: 1.0, rectRadius: 0.06, fill: { color: "FBF1E2" }, line: { color: C.accent, width: 1, dashType: "dash" } });
  s.addText([{ text: "LLM API", options: { bold: true, breakLine: true, fontSize: 10, color: C.accentDark } }, { text: "core-assist only\n~15–20% of components", options: { fontSize: 7.8, color: C.textMuted } }], { x: bx + bw - 1.48, y: ay + 0.43, w: 1.26, h: 0.85, isTextBox: true, margin: 0, fontFace: F_BODY, align: "center", valign: "middle" });

  s.addText("In scope: 10 committed mechanisms (Tier 1 + gated Tier 2)   ·   Out of scope: message queues, Kubernetes/multi-region, full RBAC, DR infra, multi-tenant billing", {
    x: bx, y: ay + ah + 0.1, w: bw, h: 0.24, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.5, italic: true, color: C.textMuted,
  });
  s.addText("Full traceable spec behind this diagram: Use Case Model + diagram, 3 System Sequence Diagrams, SRS, Test Plan, Software Development Plan, wireframes — architecture atlas, tab “Requirements & Design”", {
    x: bx, y: ay + ah + 0.34, w: bw, h: 0.24, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.3, italic: true, color: C.textMuted,
  });

  s.addNotes("Say unprompted: 'controlled, not deterministic' — the replay protocol is deterministic, LLM-step variance is measured over N replays, never assumed away (R25). Say unprompted: the Semantic Error Diagnostic abstains where no checkable constraint exists, and the abstention rate is reported as a metric. If asked for the full SRS/use-case/SSD/test-plan detail behind this diagram, point to the architecture atlas's new 'Requirements & Design' tab and the underlying files in markdowns/01-planning-and-scope/.");
}

// ============================================================
// SLIDE 7 — POC / feasibility evidence
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bgLight };
  chrome(s, 7, "POC / Feasibility Evidence — Mandatory", "“Show the evidence — do not merely describe that it exists”");

  const stats = [["71.4%", "agent accuracy, mean of 5 real runs"], ["13.2%", "step accuracy, mean of 5 real runs"], ["4 / 6", "Repair Agent success rate (Spike 8)"], ["8 / 8", "spikes with real, on-disk evidence"]];
  let sx = MX;
  const statW = CW / 4;
  stats.forEach(([n, l]) => {
    s.addText(n, { x: sx, y: 1.5, w: statW - 0.2, h: 0.55, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 30, bold: true, color: C.accentDark, align: "left" });
    s.addText(l, { x: sx, y: 2.05, w: statW - 0.3, h: 0.5, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.5, color: C.textMuted });
    sx += statW;
  });
  s.addShape(pres.ShapeType.line, { x: MX, y: 2.55, w: CW, h: 0, line: { color: C.border, width: 0.75 } });

  const spikeRows = [
    ["#", "Spike", "Status", "Result"],
    ["1", "ErrorProbe reproduction (simplified)", "DEMONSTRATED", "agent 62.5–85.7% (mean 71.4%) · step 0–25% (mean 13.2%) — 5 real runs, range not a point estimate"],
    ["2", "CrewAI instrumentation", "DEMONSTRATED", "Clean trace: 3 nodes, 2 correctly-ordered edges"],
    ["3/3b", "Fault injection", "DEMONSTRATED", "Ground truth unambiguous; one case self-corrected by the agent — kept as a finding"],
    ["4", "Semantic Error Diagnostic", "DEMONSTRATED", "Catches known-wrong values incl. a near-miss ($20.00 vs $19.75), zero false positives"],
    ["5", "Controlled counterfactual replay", "DEMONSTRATED", "Corrupted trace 97.2 → recovered 108.0, recovery_success = true"],
    ["6", "Cyclic graph handling", "DEMONSTRATED", "Bound proven load-bearing: control run with it disabled hit the 10,000-step safety cap"],
    ["7", "Preventive classifier", "DEMONSTRATED — honest negative", "precision / recall / F1 = 0.25, near-random — real finding, not hidden"],
    ["8", "Repair Agent", "DEMONSTRATED", "4/6 repair success; both failures share one precisely diagnosed, fixable cause"],
  ];
  const tRows = spikeRows.map((r, ri) => r.map((c, ci) => {
    if (ri === 0) return { text: c, options: { bold: true, fill: { color: C.bgDark2 }, color: C.textLight, fontSize: 9, align: ci === 0 ? "center" : "left", valign: "middle" } };
    const isNeg = r[2].includes("honest negative");
    return {
      text: c,
      options: {
        fontSize: 9, valign: "middle", align: ci === 0 ? "center" : "left",
        bold: ci === 2,
        color: ci === 2 ? (isNeg ? C.amber : C.green) : C.textDark,
        fill: { color: ri % 2 === 0 ? C.bgLight : C.card },
      },
    };
  }));
  s.addTable(tRows, {
    x: MX, y: 2.75, w: CW, h: 3.55,
    colW: [0.5, 2.6, 2.15, 6.98],
    border: { type: "solid", color: C.border, pt: 0.5 },
    autoPage: false, fontFace: F_BODY,
  });

  card(s, MX, 6.45, CW, 0.65, C.amberSoft);
  s.addText([{ text: "In progress: ", options: { bold: true, color: C.amber } }, { text: "full 3-stage reproduction (top FYP-1 priority).   ", options: { color: C.textDark } }, { text: "Planned: ", options: { bold: true, color: C.amber } }, { text: "Recovery Controller + Verified Repair Memory Tier-2 gates — pre-registered Mid-1 criteria, not yet run.", options: { color: C.textDark } }], {
    x: MX + 0.2, y: 6.58, w: CW - 0.4, h: 0.4, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10,
  });

  s.addNotes("Lead with Spike 7's negative result and Spike 8's failure analysis — quote the guide's own words on this directly. Every number on this slide is real, computed from files in this repo.");
}

// ============================================================
// SLIDE 8 — Evaluation plan
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bgLight };
  chrome(s, 8, "Evaluation Plan", "Thresholds decided before any result exists");

  card(s, MX, 1.55, CW, 0.85, C.card);
  s.addText([{ text: "Pre-registered acceptance band.  ", options: { bold: true, color: C.accentDark } }, { text: "Reproduction accepted within ±10 points of ErrorProbe's published 59.5% on a comparable-class backbone (Sonnet 5). Outside the band: both numbers reported transparently, per Annex A.2.", options: { color: C.textDark } }], {
    x: MX + 0.25, y: 1.68, w: CW - 0.5, h: 0.6, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11, valign: "middle",
  });

  const lx = MX, lw = 7.6;
  s.addText("METRICS", { x: lx, y: 2.6, w: lw, h: 0.25, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 10, bold: true, color: C.accentDark, charSpacing: 1 });
  const metrics = [
    "Agent / step accuracy · propagation-path F1",
    "Silent-failure precision / recall + coverage (abstention rate)",
    "Pipeline false-positive rate on 15–20% clean controls — absent from every paper and platform reviewed",
    "Task completion rate · recovery rate · repair success rate · false repair rate",
    "Diagnostic latency overhead — the measurable NFR, target < 50%",
  ];
  bullets(s, metrics, { x: lx, y: 2.92, w: lw, h: 1.9 });

  card(s, lx, 4.85, lw, 1.3, C.card);
  s.addText("STATISTICAL PROTOCOL", { x: lx + 0.2, y: 4.97, w: lw - 0.4, h: 0.24, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9.5, bold: true, color: C.textMuted, charSpacing: 1 });
  s.addText("Bootstrap 95% CIs · fixed seeds · N=5 replay variance · 4-item pre-declared ablation matrix · human-baseline comparison", {
    x: lx + 0.2, y: 5.22, w: lw - 0.4, h: 0.85, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.5, color: C.textDark,
  });

  card(s, lx, 6.28, lw, 0.85, C.redSoft);
  s.addText([{ text: "Cannot support: ", options: { bold: true, color: C.red } }, { text: "production-scale reliability claims beyond the tested frameworks and task domains — stated up front, not extracted under questioning.", options: { color: C.textDark } }], {
    x: lx + 0.2, y: 6.4, w: lw - 0.4, h: 0.6, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10, valign: "middle",
  });

  // right: success bands
  const rx = lx + lw + 0.3, rw = CW - lw - 0.3;
  s.addText("SUCCESS BANDS", { x: rx, y: 2.6, w: rw, h: 0.25, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 10, bold: true, color: C.accentDark, charSpacing: 1 });
  const bands = [
    ["Failure", "No measurable improvement over baseline anywhere", C.red, C.redSoft],
    ["Acceptable", "Parity on Who&When + any cross-arch result + nonzero-coverage detection", C.amber, C.amberSoft],
    ["Strong", "Beats baseline on unseen architectures, >70% silent-failure recall", C.teal, C.tealSoft],
    ["Exceptional", "Strong + >50% verified-repair recovery at low false-repair rate", C.green, C.greenSoft],
  ];
  let by = 2.92;
  bands.forEach(([n, d, fg, bg]) => {
    card(s, rx, by, rw, 0.85, bg);
    s.addText(n, { x: rx + 0.18, y: by + 0.08, w: rw - 0.36, h: 0.28, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 13, bold: true, color: fg });
    s.addText(d, { x: rx + 0.18, y: by + 0.38, w: rw - 0.36, h: 0.42, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9, color: C.textDark });
    by += 0.98;
  });

  s.addNotes("The false-positive-rate-on-clean-controls metric is absent from every paper in the reviewed corpus and every platform checked — say this is the field's gap, not just ours. The acceptance band was declared before the full reproduction runs — that ordering is the point.");
}

// ============================================================
// SLIDE 9 — Scope, risks & dependencies
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bgLight };
  chrome(s, 9, "Scope, Risks & Dependencies", "Every major risk already has a stated fallback");

  const lx = MX, lw = 6.5;
  s.addText("COMMITTED CORE — 10 ITEMS, TWO EVIDENCE TIERS", { x: lx, y: 1.55, w: lw, h: 0.25, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 10, bold: true, color: C.accentDark, charSpacing: 1 });
  card(s, lx, 1.85, lw, 1.05, C.greenSoft);
  s.addText([{ text: "TIER 1 — evidence-backed, unconditional  ", options: { bold: true, color: C.green, fontSize: 10.5 } }], { x: lx + 0.18, y: 1.94, w: lw - 0.36, h: 0.22, isTextBox: true, margin: 0, fontFace: F_MONO });
  s.addText("Fault-injection harness · cross-arch benchmark · Culprit Agent · Error Step Localization · Verification Agent · Semantic Error Diagnostic · Repair Agent · Verified Automatic Repair", {
    x: lx + 0.18, y: 2.17, w: lw - 0.36, h: 0.65, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.7, color: C.textDark,
  });
  card(s, lx, 3.0, lw, 0.85, C.amberSoft);
  s.addText([{ text: "TIER 2 — gated, pre-registered Mid-1 criteria  ", options: { bold: true, color: C.amber, fontSize: 10.5 } }], { x: lx + 0.18, y: 3.09, w: lw - 0.36, h: 0.22, isTextBox: true, margin: 0, fontFace: F_MONO });
  s.addText("Recovery Controller (no POC yet) · Verified Repair Memory (one real test, failed — 0/8, stated honestly)", {
    x: lx + 0.18, y: 3.32, w: lw - 0.36, h: 0.48, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.7, color: C.textDark,
  });

  s.addText("8 extensions, gated behind the core — built only after it works.", { x: lx, y: 4.0, w: lw, h: 0.3, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10, italic: true, color: C.textMuted });

  card(s, lx, 4.35, lw, 1.0, C.card);
  s.addText([{ text: "$0 — committed", options: { bold: true, fontSize: 16, color: C.accentDark, breakLine: true } }, { text: "Local Ollama for every model call, incl. reproduction & evaluation. Paid comparable-class backbone priced at ≈$353/≈$881 ceiling and explicitly not chosen.", options: { fontSize: 9.5, color: C.textMuted } }], { x: lx + 0.2, y: 4.5, w: lw - 0.4, h: 0.75, isTextBox: true, margin: 0, fontFace: F_BODY });

  s.addText("STACK", { x: lx, y: 5.55, w: lw, h: 0.22, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9.5, bold: true, color: C.textMuted, charSpacing: 1 });
  s.addText("Python · FastAPI · React/TypeScript · Postgres · Docker · CrewAI · LangGraph · Ollama · GitHub Actions", {
    x: lx, y: 5.8, w: lw, h: 0.4, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10, color: C.textDark,
  });

  card(s, lx, 6.3, lw, 0.8, C.redSoft);
  s.addText([{ text: "Ethical: ", options: { bold: true, color: C.red } }, { text: "advisory-only diagnosis, human-gated fix approval; consent required for real trace data; injection restricted to own/consenting systems.", options: { color: C.textDark } }], { x: lx + 0.18, y: 6.42, w: lw - 0.36, h: 0.6, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.3, valign: "middle" });

  const rx = lx + lw + 0.3, rw = CW - lw - 0.3;
  s.addText("TOP RISKS → FALLBACK", { x: rx, y: 1.55, w: rw, h: 0.25, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 10, bold: true, color: C.accentDark, charSpacing: 1 });
  const risks = [
    ["Reproduction misses ±10pt band — now expected (local, not comparable-class, backbone)", "Transparent dual-reporting, Annex A.2 — the anticipated path, not a failure"],
    ["Recovery Controller gate fails", "Resume via controlled replay — Tier 1 already delivers it"],
    ["VRM re-test fails again", "Ships as a memory-on/off ablation — a legitimate contribution"],
    ["Benchmark scale stalls", "Floor of 500; 300-with-statistics beats 1,000-without"],
    ["LLM API unavailable at runtime", "Documented degraded state, not a crash"],
  ];
  let ry = 1.9;
  risks.forEach(([r, f]) => {
    card(s, rx, ry, rw, 0.85, C.card);
    s.addText(r, { x: rx + 0.18, y: ry + 0.08, w: rw - 0.36, h: 0.32, isTextBox: true, margin: 0, fontFace: F_BODY, bold: true, fontSize: 10.5, color: C.textDark });
    s.addText(f, { x: rx + 0.18, y: ry + 0.42, w: rw - 0.36, h: 0.38, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.3, color: C.green });
    ry += 0.98;
  });

  s.addNotes("Deliver this slide as confidence, not confession: decision rules were pre-registered before results exist — exactly what the guide's change-control section asks for. If feasibility is pressed, point at slide 10's effort-budget number, don't just reassure verbally.");
}

// ============================================================
// SLIDE 10 — Team, iterations, DEI & ethics/legal
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.bgLight };
  chrome(s, 10, "Team, Iterations, DEI & Ethics/Legal", "Ownership, timeline, and the compliance lines the guide names");

  const members = [
    ["Shahoud Shahid", "Data / Benchmark", "Instrumentation (CrewAI, LangGraph), injection operators, benchmark, licensing/release", "If removed: no cross-architecture benchmark exists", C.teal, C.tealSoft],
    ["Muhammad Noor", "Diagnosis Engine", "Execution graph, ErrorProbe reproduction, Semantic Error Diagnostic, causal tracing", "If removed: no attribution algorithm, no silent-failure detection", C.orange, C.orangeSoft],
    ["Saif Shahzad", "Platform", "Replay/recovery engine, SDK, backend, dashboard, deployment", "If removed: nothing is installable outside the dev machine", C.blue, C.blueSoft],
  ];
  const mw = (CW - 0.4) / 3;
  let mx2 = MX;
  members.forEach(([n, role, own, rm, fg, bg]) => {
    card(s, mx2, 1.55, mw, 1.75, bg);
    s.addText(n, { x: mx2 + 0.18, y: 1.68, w: mw - 0.36, h: 0.28, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 13, bold: true, color: C.textDark });
    chip(s, mx2 + 0.18, 1.98, 1.9, role.toUpperCase(), C.textLight, fg);
    s.addText(own, { x: mx2 + 0.18, y: 2.35, w: mw - 0.36, h: 0.6, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.3, color: C.textDark });
    s.addText(rm, { x: mx2 + 0.18, y: 2.95, w: mw - 0.36, h: 0.3, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.5, italic: true, color: C.textMuted });
    mx2 += mw + 0.2;
  });

  // gate timeline
  s.addText("FYP-1 → FYP-2 MILESTONES", { x: MX, y: 3.55, w: CW, h: 0.24, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 10, bold: true, color: C.accentDark, charSpacing: 1 });
  const gates = ["Gate 1\nProposal Defense", "Gate 2/3\nMid-1: reproduction +\nboth Tier-2 gates", "Gate 3\nFinal-1: integrated core", "Gate 4\nMid-2: benchmark ≥500", "Gate 5\nFinal-2: full eval + release"];
  const gw = CW / gates.length;
  s.addShape(pres.ShapeType.line, { x: MX + gw / 2, y: 4.15, w: CW - gw, h: 0, line: { color: C.accent, width: 2 } });
  gates.forEach((g, i) => {
    const gx = MX + i * gw + gw / 2;
    s.addShape(pres.ShapeType.ellipse, { x: gx - 0.09, y: 4.06, w: 0.18, h: 0.18, fill: { color: C.accent }, line: { color: C.bgLight, width: 1.5 } });
    s.addText(g, { x: gx - gw / 2 + 0.1, y: 4.3, w: gw - 0.2, h: 0.55, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.3, color: C.textDark, align: "center" });
  });
  card(s, MX, 4.95, CW, 0.4, C.card);
  s.addText("Effort budget: 490h (FYP-1) + 640h (FYP-2) = 1,130h budgeted against 1,130h capacity (3 × ~15h/wk × ~28 weeks)", {
    x: MX + 0.2, y: 4.99, w: CW - 0.4, h: 0.3, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9.5, color: C.textDark, valign: "middle",
  });

  const bandY = 5.55, bandH = 1.35, bandW = (CW - 0.4) / 3;
  const bands = [
    ["DEI", [
      "Open-source release (MIT/CC BY 4.0) puts enterprise-grade diagnostic tooling within reach of resource-constrained teams",
      "Dashboard pairs color with text, not color alone — WCAG check owed by Final-1",
      "Accuracy claims stated as English-only, not generalized",
    ], C.teal, C.tealSoft],
    ["ETHICAL", [
      "Diagnosis output is advisory, not autonomous — human-gated fix approval",
      "Informed consent required for any real user's trace data",
      "Synthetic fault injection restricted to own/consenting systems only",
    ], C.red, C.redSoft],
    ["LEGAL / PROFESSIONAL", [
      "Who&When (MIT) · GSM8K (MIT) · tau-bench retail (MIT) — all license-confirmed",
      "AI usage disclosed per-session (19 sessions logged), countersigned by supervisor",
    ], C.blue, C.blueSoft],
  ];
  let bx2 = MX;
  bands.forEach(([label, pts, fg, bg]) => {
    card(s, bx2, bandY, bandW, bandH, bg);
    s.addText(label, { x: bx2 + 0.18, y: bandY + 0.12, w: bandW - 0.36, h: 0.24, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9.5, bold: true, color: fg, charSpacing: 1 });
    bullets(s, pts, { x: bx2 + 0.18, y: bandY + 0.42, w: bandW - 0.36, h: bandH - 0.55, fontSize: 9 });
    bx2 += bandW + 0.2;
  });

  s.addNotes("Each member states their own subsystem in one sentence, aloud — the panel is applying the guide's four ownership questions, and hearing three distinct voices early sets that tone. The DEI line is a real, checkable commitment, not a decorative label.");
}

pres.writeFile({ fileName: "Granite_Proposal_Defense.pptx" }).then(fn => console.log("Wrote", fn));
