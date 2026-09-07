// Granite — Proposal Defense Deck, v2
// Produces Granite_Proposal_Defense_v2.pptx
//
// Differences from v1 (generate_proposal_deck.js), which is kept untouched for comparison:
//   1. Slides 8-10 follow a deliberate hybrid of the two structures in circulation,
//      because they do not agree and the handbook's own rule (C.16) is that "the slide
//      order may be adjusted, but all of the following information should be visible":
//        · Slide 8  — from the circulated image: "Evaluation plan AND risks".
//        · Slide 9  — from BOTH: the handbook's "Scope, risks and dependencies"
//                     (committed scope, extensions, resources, tools, dependencies,
//                     deployment) merged with the image's "Work division and
//                     iteration plan" (member-wise ownership + milestones).
//        · Slide 10 — from the handbook: "Team responsibilities and iterations, DEI
//                     and ethical/legal issues". Individual ownership sits on slide 9,
//                     so slide 10 carries the SHARED half that C.5 says stays a team
//                     responsibility (architecture, integration, QA, security/ethics,
//                     repo discipline, the defense), the gate-by-gate iteration plan,
//                     and the DEI / ethical / legal statements.
//      This keeps every C.16-required item visible while matching the circulated
//      slide titles. v1 by contrast crammed team + milestones + DEI + ethics + legal
//      onto a single slide 10.
//   2. Slide 3's "Closest prior FYP" row is filled with real data — v1 shipped
//      "[TO BE PROVIDED]". Now: all 660 titles, 12 published cohorts, Spring-2019→Fall-2025.
//   3. Slide 5 adds the handbook's own AI-resilience test (C.7) — "why this is not
//      a course project" — which the official structure names for this slide.
//   4. Slide 10 names the AI-assisted development level (Level 2, handbook C.8),
//      a requirement v1 predates.
//   5. Refined theme: deeper base, restrained gold, left accent rail, footer band,
//      and inline evidence tags citing the repo file behind each load-bearing claim.
const pptxgen = require("pptxgenjs");

// ---------- Palette v2 — deeper graphite, restrained gold, higher-contrast semantics ----------
const C = {
  ink:        "0F1219",  // deepest base
  ink2:       "171C26",  // secondary dark
  panel:      "1E242F",  // dark panel / table header
  paper:      "FBFBFC",  // content background (softer than pure white)
  card:       "F1F2F5",
  cardAlt:    "E8EAEF",
  textDark:   "1B202A",
  textMuted:  "596273",
  textFaint:  "8B92A2",
  textLight:  "F5F6F8",
  textLightMuted: "A9B0BE",
  gold:       "C89B3C",
  goldLight:  "E3BC6E",
  goldDark:   "8E6A1F",
  green:      "1E7A52",  greenSoft: "E6F1EB",
  amber:      "A8760F",  amberSoft: "F7EFDC",
  red:        "A83A30",  redSoft:   "F6E6E3",
  teal:       "15707A",  tealSoft:  "E3EFF1",
  indigo:     "31558F",  indigoSoft:"E4E9F2",
  orange:     "B05C1C",  orangeSoft:"F6EADD",
  border:     "D9DCE3",
  hair:       "2C3340",
};
const F_TITLE = "Georgia";
const F_BODY  = "Calibri";
const F_MONO  = "Consolas";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Granite — F26-060";
pres.company = "FAST School of Computing, NUCES Islamabad";
pres.title = "Granite — Proposal Defense (v2)";
pres.subject = "Stage 1 Proposal Defense — F26-060-Granite";

const PW = 13.333, PH = 7.5;
const MX = 0.62;
const CW = PW - MX * 2;
const RAIL = 0.055;               // left accent rail width

// ================= helpers =================
function chrome(slide, num, title, kicker) {
  // left accent rail
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: RAIL, h: PH, fill: { color: C.gold }, line: { type: "none" },
  });
  facetWatermark(slide);
  slide.addText(kicker.toUpperCase(), {
    x: MX, y: 0.34, w: CW, h: 0.26, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 10.5, bold: true, color: C.goldDark, charSpacing: 1.8,
  });
  slide.addText(title, {
    x: MX, y: 0.60, w: CW, h: 0.64, isTextBox: true, margin: 0,
    fontFace: F_TITLE, fontSize: 27, bold: true, color: C.textDark,
  });
  slide.addShape(pres.ShapeType.rect, { x: MX, y: 1.30, w: 0.62, h: 0.04, fill: { color: C.gold }, line: { type: "none" } });
  footer(slide, num);
}
function footer(slide, n) {
  slide.addShape(pres.ShapeType.line, { x: MX, y: PH - 0.46, w: CW, h: 0, line: { color: C.border, width: 0.75 } });
  slide.addText("F26-060-GRANITE  ·  PROPOSAL DEFENSE  ·  STREAM A", {
    x: MX, y: PH - 0.40, w: 6.5, h: 0.26, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 8.5, color: C.textFaint, charSpacing: 0.8,
  });
  slide.addText(`${n} / 10`, {
    x: PW - MX - 1.2, y: PH - 0.40, w: 1.2, h: 0.26, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 8.5, bold: true, color: C.goldDark, align: "right",
  });
}
// Cards carry a soft elevation. NOTE: this is drawn as an offset plate rather than
// via pptxgenjs's `shadow:` option — that option emits <a:effectLst> containing
// whitespace text nodes, which PowerPoint rejects outright (the file will not open,
// even though the XML is well-formed and the element order is schema-correct).
// Verified by bisect: identical deck with `shadow:` fails to open, without it opens.
const SHADOW_PLATE = "E4E6EB";
function card(slide, x, y, w, h, fill, accentEdge) {
  slide.addShape(pres.ShapeType.roundRect, {
    x: x + 0.022, y: y + 0.028, w, h, rectRadius: 0.06,
    fill: { color: SHADOW_PLATE }, line: { type: "none" },
  });
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.06,
    fill: { color: fill || C.card }, line: { color: C.border, width: 0.75 },
  });
  if (accentEdge) {
    slide.addShape(pres.ShapeType.rect, {
      x, y: y + 0.06, w: 0.045, h: h - 0.12, fill: { color: accentEdge }, line: { type: "none" },
    });
  }
}
// Thematic granite facet — a faint cut-stone watermark echoing the title mark.
function facetWatermark(slide) {
  // Kept extremely low-contrast so it reads as paper texture, never as an object
  // competing with content — content is laid out over this region on several slides.
  const wx = PW - 1.72, wy = PH - 1.72;
  slide.addShape(pres.ShapeType.rect, { x: wx, y: wy, w: 1.10, h: 1.10, rotate: 45, fill: { type: "none" }, line: { color: "F4F5F7", width: 1 } });
  slide.addShape(pres.ShapeType.rect, { x: wx + 0.26, y: wy + 0.26, w: 0.58, h: 0.58, rotate: 45, fill: { type: "none" }, line: { color: "F7F4ED", width: 1 } });
}
function label(slide, x, y, w, text, color) {
  slide.addText(text.toUpperCase(), {
    x, y, w, h: 0.24, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 9.5, bold: true, color: color || C.goldDark, charSpacing: 1.2,
  });
}
function chip(slide, x, y, w, text, fg, bg) {
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.26, rectRadius: 0.13, fill: { color: bg }, line: { type: "none" } });
  slide.addText(text, {
    x, y, w, h: 0.26, isTextBox: true, margin: 0, align: "center", valign: "middle",
    fontFace: F_MONO, fontSize: 8.5, bold: true, color: fg,
  });
}
function dot(slide, x, y, d, bg, text, fg) {
  slide.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: bg }, line: { type: "none" } });
  slide.addText(text, {
    x, y, w: d, h: d, isTextBox: true, margin: 0, align: "center", valign: "middle",
    fontFace: F_TITLE, fontSize: d > 0.5 ? 17 : 12, bold: true, color: fg,
  });
}
// evidence tag — the v2 defensibility device: every load-bearing claim cites its file
function evidence(slide, x, y, w, text) {
  slide.addText(`▸ ${text}`, {
    x, y, w, h: 0.22, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 8, color: C.textFaint,
  });
}
function bullets(slide, items, opts) {
  const arr = items.map((t, i) => ({
    text: t, options: { bullet: { code: "25AA", indent: 13 }, breakLine: i < items.length - 1 },
  }));
  slide.addText(arr, Object.assign({
    isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 12, color: C.textDark,
    paraSpaceAfter: 7, valign: "top",
  }, opts));
}

// ============================================================
// SLIDE 1 — Title & one-line problem
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.ink };

  // layered facet mark (granite motif, refined: three nested rotated squares)
  const mx = PW - 3.0, my = 1.15;
  s.addShape(pres.ShapeType.rect, { x: mx, y: my, w: 1.5, h: 1.5, rotate: 45, fill: { color: C.ink2 }, line: { color: C.goldDark, width: 1 } });
  s.addShape(pres.ShapeType.rect, { x: mx + 0.26, y: my + 0.26, w: 0.98, h: 0.98, rotate: 45, fill: { color: C.gold }, line: { type: "none" } });
  s.addShape(pres.ShapeType.rect, { x: mx + 0.50, y: my + 0.50, w: 0.50, h: 0.50, rotate: 45, fill: { color: C.ink }, line: { color: C.goldLight, width: 1 } });

  s.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: RAIL * 1.6, h: PH, fill: { color: C.gold }, line: { type: "none" } });

  s.addText("F26-060  ·  PROPOSAL DEFENSE  ·  STREAM A — RESEARCH-DERIVED", {
    x: MX, y: 1.45, w: 9.2, h: 0.30, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 11.5, bold: true, color: C.goldLight, charSpacing: 1.8,
  });
  s.addText("Granite", {
    x: MX, y: 1.80, w: 9.2, h: 1.15, isTextBox: true, margin: 0,
    fontFace: F_TITLE, fontSize: 68, bold: true, color: C.textLight,
  });
  s.addText("A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery", {
    x: MX, y: 2.98, w: 8.4, h: 0.62, isTextBox: true, margin: 0,
    fontFace: F_BODY, fontSize: 15.5, italic: true, color: C.textLightMuted,
  });

  s.addShape(pres.ShapeType.rect, { x: MX, y: 3.78, w: 1.1, h: 0.035, fill: { color: C.gold }, line: { type: "none" } });

  s.addText("When a multi-agent AI system fails — including when the wrong answer looks completely right — no published method can reliably say which agent caused it, and none can verify a fix before trusting it.", {
    x: MX, y: 4.00, w: 8.4, h: 1.05, isTextBox: true, margin: 0,
    fontFace: F_TITLE, fontSize: 18.5, color: C.textLight, italic: true,
  });

  s.addShape(pres.ShapeType.line, { x: MX, y: 5.50, w: 8.4, h: 0, line: { color: C.hair, width: 1 } });
  const team = [["Shahoud Shahid", "23i-2515", "Data / Benchmark"], ["Muhammad Noor", "23i-2520", "Diagnosis Engine"], ["Saif Shahzad", "23i-2634", "Platform"]];
  let tx = MX;
  team.forEach(([n, r, role]) => {
    s.addText([
      { text: n, options: { bold: true, breakLine: true, fontSize: 12.5, color: C.textLight } },
      { text: `${r}  ·  `, options: { fontSize: 10, color: C.textLightMuted } },
      { text: role, options: { fontSize: 10, color: C.goldLight } },
    ], { x: tx, y: 5.62, w: 2.8, h: 0.62, isTextBox: true, margin: 0, fontFace: F_BODY });
    tx += 2.85;
  });

  s.addText([
    { text: "Supervisor   ", options: { color: C.textLightMuted, fontSize: 10.5 } },
    { text: "Dr. Adil Majeed", options: { color: C.textLight, bold: true, fontSize: 12.5, breakLine: true } },
    { text: "FAST School of Computing, NUCES Islamabad", options: { color: C.textLightMuted, fontSize: 10 } },
  ], { x: MX, y: 6.52, w: 6, h: 0.6, isTextBox: true, margin: 0, fontFace: F_BODY });

  s.addNotes("Say the one-line problem exactly as written — WHO (teams running multi-agent systems), WHAT fails (attribution + silent failures), WHY it matters (nobody can verify a fix), in one breath. Do not explain the title word-by-word — slide 6 does that. Three names, three distinct subsystems, said aloud here sets the ownership tone before the panel has to ask.");
}

// ============================================================
// SLIDE 2 — Problem & users
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 2, "Problem & Users", "Who has this, how it is handled today, why it matters");

  card(s, MX, 1.52, 5.45, 2.45, C.card, C.teal);
  label(s, MX + 0.28, 1.68, 5, "Stakeholders");
  bullets(s, [
    "Primary — an engineering team operating a multi-agent AI system in or near production (grounded in a customer-support / retail workflow, our active benchmark substrate)",
    "Secondary — downstream product teams consuming the diagnosis output",
    "Secondary — auditors / compliance reviewers needing traceable evidence of what went wrong",
  ], { x: MX + 0.28, y: 1.98, w: 4.95, h: 1.9, fontSize: 11 });

  card(s, MX, 4.10, 5.45, 0.92, C.tealSoft);
  s.addText([{ text: "SDG 9  ", options: { bold: true, color: C.teal, fontSize: 11.5 } }, { text: "Industry, Innovation & Infrastructure (target 9.5) — reliability tooling for a genuinely new industrial category", options: { color: C.textDark, fontSize: 11 } }], {
    x: MX + 0.28, y: 4.24, w: 4.95, h: 0.66, isTextBox: true, margin: 0, fontFace: F_BODY,
  });

  card(s, MX, 5.15, 5.45, 1.30, C.redSoft, C.red);
  label(s, MX + 0.28, 5.30, 5, "Consequence of failure", C.red);
  s.addText("A missed silent failure ships a confident, wrong answer to an end user — with no crash, no error, and no signal that anything went wrong.", {
    x: MX + 0.28, y: 5.58, w: 4.95, h: 0.8, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11.5, color: C.textDark, italic: true,
  });
  evidence(s, MX, 6.55, 5.45, "plan §0.1 · §0.05 (SDG) · Full_Literature_Landscape_Analysis.md");

  const rx = 6.42, rw = CW - (rx - MX);
  label(s, rx, 1.52, rw, "Current workflow — without Granite", C.textMuted);
  const steps = [
    ["1", "Observability platform captures the trace", "LangSmith / Langfuse / Braintrust / Arize", C.indigo, C.indigoSoft],
    ["2", "A human reads the trace and guesses the root cause", "no automated attribution with published accuracy", C.orange, C.orangeSoft],
    ["3", "No systematic silent-failure check", "a confident, well-formed, wrong answer passes unnoticed", C.red, C.redSoft],
    ["4", "No way to test a fix before redeploying", "field baseline: single-model guess = 14.2% step accuracy (Who&When)", C.red, C.redSoft],
  ];
  let sy = 1.92;
  steps.forEach(([n, t, sub, fg, bg], i) => {
    dot(s, rx, sy, 0.40, bg, n, fg);
    s.addText([{ text: t, options: { bold: true, breakLine: true, fontSize: 12, color: C.textDark } }, { text: sub, options: { fontSize: 10, color: C.textMuted } }], {
      x: rx + 0.56, y: sy - 0.04, w: rw - 0.58, h: 0.82, isTextBox: true, margin: 0, fontFace: F_BODY,
    });
    if (i < 3) s.addShape(pres.ShapeType.line, { x: rx + 0.20, y: sy + 0.40, w: 0, h: 0.42, line: { color: C.border, width: 1.5, dashType: "dash" } });
    sy += 1.16;
  });
  card(s, rx, 6.10, rw, 0.72, C.amberSoft);
  s.addText([{ text: "Stakeholder evidence today:  ", options: { bold: true, color: C.amber } }, { text: "published literature + the commercial landscape (7 vendors shipping for this pain). Direct practitioner contact is scheduled inside the Mid-2 acceptance study, declared open rather than claimed.", options: { color: C.textDark } }], {
    x: rx + 0.20, y: 6.22, w: rw - 0.4, h: 0.52, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.8,
  });

  s.addNotes("14.2% is the field's own measured baseline for 'a human reads the trace' — the number the whole project is trying to beat. On stakeholders: state plainly that this is Stream A, that the problem's reality rests on published evidence and a commercial market, and that live practitioner contact is scheduled in the Mid-2 acceptance study (C.13.1). Do not overclaim contact that has not happened — risk-register R33.");
}

// ============================================================
// SLIDE 3 — Existing solutions & prior FYP comparison
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 3, "Existing Solutions & Prior FYP Comparison", "Proving the gap is structural, not a missing feature");

  const cols = ["", "Core approach", "Step-level attribution\n(published accuracy)", "Silent-failure\ndetection", "Counterfactual fix-\ntesting, measured", "Framework-\nagnostic"];
  const rows = [
    ["ErrorProbe\n(ACL 2026)", "3-stage LLM diagnosis\n+ memory", "59.5%", "✘ admits\nit cannot", "✘", "✘ 2 archs only"],
    ["LangSmith Engine /\nArize Alyx (2026)", "Automated RCA\n+ fix drafting", "not published", "not confirmed", "not confirmed", "✘ stack-locked"],
    ["Langfuse / Braintrust /\nPhoenix / Maxim / Opik", "Trace capture\n+ eval", "human-driven", "RAG-groundedness\nonly", "✘", "✘"],
    // Named prior FYP from Shahoud's 2026-09-06 archive check (R39), merged with the
    // 660-title structural sweep — a named closest match answers a panel better than
    // "we found nothing", and the two findings agree rather than compete.
    ["Closest prior FYP\n(S24-011-D-HDLM,\nSpring 2024)", "hallucination detection\nin single-LLM text", "—\nno attribution at all", "partial — single-LLM\ntext only, not agent traces", "✘ no repair /\nreplay step", "N/A — not a\nmulti-agent system"],
    ["Current manual\nworkflow", "human reads,\nguesses", "14.2%\n(Who&When)", "✘", "✘", "N/A"],
    ["Granite\n(proposed)", "Constraint-based SED\n+ verified repair loop", "building on\nErrorProbe", "✓ scoped &\nmeasured", "✓ recovery rate\nover N replays", "✓ CrewAI +\nLangGraph, unseen"],
  ];
  const tRows = [cols.map(c => ({ text: c, options: { bold: true, fill: { color: C.panel }, color: C.textLight, fontSize: 9.5, align: "center", valign: "middle" } }))];
  rows.forEach((r, ri) => {
    const isGranite = ri === rows.length - 1;
    const isPrior = ri === 3;
    tRows.push(r.map((c, ci) => ({
      text: c,
      options: {
        fontSize: 9.5, align: ci === 0 ? "left" : "center", valign: "middle",
        bold: ci === 0 || isGranite,
        fill: { color: isGranite ? C.tealSoft : (isPrior ? C.greenSoft : (ri % 2 === 0 ? C.paper : C.card)) },
        color: C.textDark,
      },
    })));
  });
  s.addTable(tRows, {
    x: MX, y: 1.50, w: CW, h: 3.98,
    colW: [1.72, 2.10, 2.00, 1.80, 2.10, 1.87],
    border: { type: "solid", color: C.border, pt: 0.5 },
    autoPage: false, fontFace: F_BODY,
  });

  card(s, MX, 5.56, 6.05, 1.18, C.greenSoft, C.green);
  label(s, MX + 0.22, 5.67, 5.6, "Prior-FYP check — closed", C.green);
  s.addText([
    { text: "All 12 published cohorts, Spring-2019 → Fall-2025, 660 registered titles, compared structurally. Closest match: ", options: { color: C.textDark } },
    { text: "S24-011-D-HDLM", options: { bold: true, color: C.green } },
    { text: " — hallucination detection in a single LLM's text (Spring 2024): same underlying problem (untrustworthy output, no error signal), roughly one of our four pipeline stages. Other analogs use “multi-agent” only as an application pattern (PropPal, LawSphere, CampusHive); nearest detect-then-repair is AutoVulRepair (fuzzing/C++).", options: { color: C.textDark } },
  ], {
    x: MX + 0.22, y: 5.93, w: 5.65, h: 0.76, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.8,
  });

  card(s, MX + 6.25, 5.56, CW - 6.25, 1.18, C.amberSoft, C.amber);
  label(s, MX + 6.47, 5.67, 5.4, "The real gap", C.amber);
  s.addText("No system checked — academic or commercial — confirms step-level attribution accuracy together with general silent-failure detection, counterfactual fix verification and cross-architecture generalization, evaluated as one pipeline.", {
    x: MX + 6.47, y: 5.93, w: CW - 6.7, h: 0.76, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.3, color: C.textDark,
  });
  evidence(s, MX, 6.80, CW, "plan §0.095 (full 660-title comparison)  ·  Commercial_Product_Comparison.md  ·  risk-register R9/R33");

  s.addNotes("Volunteer the correction story: an early draft said 'nobody automates this' — direct vendor checks proved that stale, corrected on the record (R9). On prior FYPs, give the number unprompted: 660 titles across every published cohort back to 2019, checked structurally, not by title — and name AutoVulRepair yourself as the nearest analog before a panelist finds it. The gap is the combination, not any single missing feature.");
}

// ============================================================
// SLIDE 4 — R&D / recent technical work
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 4, "Research & Technical Basis", "9+ papers read in full — decisions, not decoration");

  const lx = MX, lw = 6.5;
  label(s, lx, 1.52, lw, "Decisions the literature actually changed");
  const decisions = [
    ["ErrorProbe chosen as baseline", "on performance (59.5%, beats its ancestors on their own benchmarks), not on recency"],
    ["CrewAI + LangGraph committed", "neither used by any of the 9 papers reviewed — the actual test of generalization"],
    ["Constraint-based SED, not LLM-judge", "“From Confident Closing to Silent Failure” (arXiv:2606.09863): LLM-judge AUROC ≤ 0.65"],
    ["Single-framework narrowing rejected", "the market survey's own advice, declined — it would delete the research question (R19)"],
  ];
  let dy = 1.86;
  decisions.forEach(([t, sub]) => {
    dot(s, lx, dy, 0.30, C.goldLight, "✓", C.ink);
    s.addText([{ text: t, options: { bold: true, breakLine: true, fontSize: 11.5, color: C.textDark } }, { text: sub, options: { fontSize: 10, color: C.textMuted } }], {
      x: lx + 0.44, y: dy - 0.06, w: lw - 0.48, h: 0.92, isTextBox: true, margin: 0, fontFace: F_BODY,
    });
    dy += 1.06;
  });
  evidence(s, lx, 6.15, lw, "Full_Literature_Landscape_Analysis.md · ErrorProbe_Baseline_Selection.md · plan §0.08");

  const rx = 7.42, rw = CW - (rx - MX);
  label(s, rx, 1.52, rw, "Published step-accuracy lineage");
  // Figures are reported exactly as published — dataLabelFormatCode is required,
  // otherwise pptxgenjs rounds 59.5 to "60" and contradicts the 40.5-points-wrong
  // callout below. AgenTracer is published as a RANGE (37–43% on Who&When), so the
  // bar shows its midpoint and the range is named underneath rather than hidden.
  s.addChart(pres.ChartType.bar, [{
    name: "Step accuracy",
    labels: ["Who&When\n(single-LLM)", "AgenTracer\n(midpoint of range)", "ErrorProbe\n(baseline)"],
    values: [14.2, 40.0, 59.5],
  }], {
    x: rx, y: 1.84, w: rw, h: 2.14,
    barDir: "col", chartColors: [C.gold],
    showTitle: false, showLegend: false,
    showValue: true, dataLabelPosition: "outEnd", dataLabelColor: C.textDark,
    dataLabelFontSize: 11, dataLabelFontBold: true, dataLabelFormatCode: "0.0",
    catAxisLabelColor: C.textMuted, catAxisLabelFontSize: 9, catAxisLabelFontFace: F_BODY,
    valAxisLabelColor: C.textMuted, valAxisLabelFontSize: 9, valAxisMaxVal: 70, valAxisMinVal: 0,
    valAxisLabelFormatCode: "0",
    valGridLine: { color: C.border, size: 0.5 }, catGridLine: { style: "none" },
    plotArea: { fill: { color: C.paper } },
  });
  s.addText("Step-level accuracy on Who&When, % · AgenTracer-8B is published as a 37–43% range, not a point estimate — midpoint plotted, range stated.", {
    x: rx, y: 4.00, w: rw, h: 0.24, isTextBox: true, margin: 0,
    fontFace: F_BODY, fontSize: 8, italic: true, color: C.textMuted,
  });

  card(s, rx, 4.28, rw, 0.95, C.redSoft, C.red);
  s.addText([{ text: "40.5 points still wrong  ", options: { bold: true, color: C.red } }, { text: "— the best published method misattributes the origin step 4 times in 10, and confesses it cannot see silent failures at all.", options: { color: C.textDark } }], {
    x: rx + 0.22, y: 4.40, w: rw - 0.44, h: 0.72, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.5,
  });

  card(s, rx, 5.36, rw, 1.10, C.card);
  label(s, rx + 0.22, 5.48, rw - 0.44, "Backbone-confound caveat — stated up front", C.textMuted);
  s.addText("Cross-paper comparisons use different LLM backbones — a win partly reflects backbone strength. Controlled within Granite's own experiments (R4); dual-reported per Annex A.2.", {
    x: rx + 0.22, y: 5.74, w: rw - 0.44, h: 0.62, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10, color: C.textDark,
  });

  s.addNotes("State the backbone-confound caveat before being asked. Name that credible unpublished preprints exist in adjacent territory and the team made a recorded decision not to chase every one — the strategy is beating a peer-reviewed baseline, not pre-empting unpublished work.");
}

// ============================================================
// SLIDE 5 — Complex computing challenge (+ why this is not a course project)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 5, "Complex Computing Challenge", "What is technically hard — and why this is not a course project");

  // CCP grid — compact 3x3
  const items = [
    ["1", "Conflicting requirements", "Depth vs. latency; completeness vs. privacy; generalization vs. specialization", true],
    ["2", "No obvious solution", "Best published step accuracy still 59.5% after 15 months, 7 papers", true],
    ["3", "Depth of knowledge", "Execution-graph modeling, causal reasoning, distributed tracing, eval methodology", true],
    ["4", "Unfamiliar issues", "Delayed error manifestation, LLM non-determinism, cross-arch generalization", true],
    ["5", "Beyond standard practice", "No off-the-shelf framework solves attribution + silent-failure detection + recovery", true],
    ["6", "Diverse stakeholders", "Operators, product teams, auditors named; live contact scheduled at Mid-2", false],
    ["7", "Significant consequences", "A missed silent failure ships a wrong answer, undetected", true],
    ["8", "Interdependence", "Failures propagate through interdependent agents — the graph models this directly", true],
    ["9", "Ill-defined cause", "3 unknowns at diagnosis time: whether, which agent/step, what correct behavior was", true],
  ];
  const cols3 = 3, rowH = 1.14, colW = CW / cols3;
  items.forEach(([n, t, sub, clear], i) => {
    const cx = MX + (i % cols3) * colW, cy = 1.50 + Math.floor(i / cols3) * rowH;
    card(s, cx, cy, colW - 0.18, rowH - 0.14, clear ? C.greenSoft : C.amberSoft, clear ? C.green : C.amber);
    dot(s, cx + 0.16, cy + 0.13, 0.30, clear ? C.green : C.amber, n, C.textLight);
    s.addText(t, { x: cx + 0.56, y: cy + 0.12, w: colW - 0.86, h: 0.30, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 11.5, bold: true, color: C.textDark });
    s.addText(sub, { x: cx + 0.16, y: cy + 0.46, w: colW - 0.48, h: 0.52, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9, color: C.textMuted });
  });
  s.addText("8 of 9 characteristics clear — the guide's own worked “Strong” examples clear 6 to 9.", {
    x: MX, y: 4.94, w: 6.4, h: 0.26, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.5, italic: true, color: C.textMuted,
  });

  // NEW in v2 — the handbook's AI-resilience test (C.7)
  card(s, MX, 5.24, CW, 1.48, C.ink2);
  s.addText("THE HANDBOOK'S OWN TEST (C.7):  “Could a strong student with AI assistance build a working version of this in a week?”", {
    x: MX + 0.28, y: 5.36, w: CW - 0.56, h: 0.28, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 10, bold: true, color: C.goldLight, charSpacing: 0.5,
  });
  const hard = [
    ["The wrapper", "yes — in a weekend", "An SDK that captures traces and calls an LLM to guess a culprit is a week of work.", C.textLightMuted],
    ["What it would get wrong", "everything that carries the marks", "It would have no benchmark on unseen architectures, no way to tell a silent failure from a correct answer, no measured false-positive rate on clean controls, and no evidence its fix works.", C.textLight],
    ["Where our difficulty sits", "data, evaluation, constraints", "Building the cross-architecture fault-injection benchmark, defining verifiable constraints, and proving a repair works via controlled replay — none of which generation removes.", C.textLight],
  ];
  let hx = MX + 0.28;
  const hw = (CW - 0.9) / 3;
  hard.forEach(([k, v, d, col]) => {
    s.addText([
      { text: k.toUpperCase(), options: { fontFace: F_MONO, fontSize: 8.5, bold: true, color: C.gold, breakLine: true, charSpacing: 0.8 } },
      { text: v, options: { fontFace: F_BODY, fontSize: 10.5, bold: true, color: C.textLight, breakLine: true } },
      { text: d, options: { fontFace: F_BODY, fontSize: 8.7, color: col } },
    ], { x: hx, y: 5.68, w: hw, h: 0.96, isTextBox: true, margin: 0 });
    hx += hw + 0.17;
  });
  evidence(s, MX, 6.80, CW, "02_Panel_Defense_Question_Bank.md Q8a  ·  plan §1 (three-tier CCP)  ·  §2 (9-characteristic rating)");

  s.addNotes("This is the slide the panel uses to decide whether the project deserves capstone status. Do not read the nine boxes — point at them and speak the bottom band instead: concede immediately that the wrapper is a weekend's work, then name precisely what such a version would get wrong. Characteristic 6 is amber on purpose; say so before they spot it. Read characteristic 9's resolution aloud if pressed on complexity.");
}

// ============================================================
// SLIDE 6 — Proposed solution & contribution
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 6, "Proposed Solution & Contribution", "What is being built, and where the boundary sits");

  card(s, MX, 1.50, CW, 0.95, C.card, C.gold);
  s.addText([
    { text: "Contribution.  ", options: { bold: true, color: C.goldDark, fontSize: 11 } },
    { text: "Existing methods reach up to 59.5% step accuracy but remain weak under two conditions: none is evaluated on an architecture absent from its own benchmark construction, and the strongest admits it cannot catch silent failures. We are building a cross-architecture fault-injection benchmark and a diagnosis pipeline with constraint-based silent-failure verification, packaged as a framework-agnostic testing SDK.", options: { color: C.textDark, fontSize: 10.8 } },
  ], { x: MX + 0.28, y: 1.62, w: CW - 0.56, h: 0.78, isTextBox: true, margin: 0, fontFace: F_BODY, valign: "middle" });

  const ax = MX, ay = 2.62, aw = CW, ah = 3.55;
  s.addShape(pres.ShapeType.roundRect, { x: ax, y: ay + 0.22, w: 1.62, h: 0.82, rectRadius: 0.05, fill: { color: C.paper }, line: { color: C.textMuted, width: 1, dashType: "dash" } });
  s.addText([{ text: "Target System", options: { bold: true, breakLine: true, fontSize: 9.8 } }, { text: "CrewAI / LangGraph", options: { fontSize: 8.3, color: C.textMuted } }], { x: ax + 0.08, y: ay + 0.30, w: 1.46, h: 0.66, isTextBox: true, margin: 0, fontFace: F_BODY, align: "center", valign: "middle", color: C.textDark });
  s.addShape(pres.ShapeType.roundRect, { x: ax, y: ay + 2.48, w: 1.62, h: 0.82, rectRadius: 0.05, fill: { color: C.paper }, line: { color: C.textMuted, width: 1, dashType: "dash" } });
  s.addText([{ text: "Operator", options: { bold: true, breakLine: true, fontSize: 9.8 } }, { text: "engineering team", options: { fontSize: 8.3, color: C.textMuted } }], { x: ax + 0.08, y: ay + 2.56, w: 1.46, h: 0.66, isTextBox: true, margin: 0, fontFace: F_BODY, align: "center", valign: "middle", color: C.textDark });

  const bx = ax + 1.92, bw = 8.15;
  s.addShape(pres.ShapeType.roundRect, { x: bx, y: ay, w: bw, h: ah, rectRadius: 0.08, fill: { color: "FFFFFF" }, line: { color: C.gold, width: 1.25, dashType: "dash" } });
  s.addText("GRANITE — SYSTEM BOUNDARY", { x: bx + 0.16, y: ay + 0.06, w: 4, h: 0.22, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 8, bold: true, color: C.goldDark, charSpacing: 1 });

  const lanes = [
    ["LANE A — DATA / BENCHMARK · SHAHOUD", "Framework Adapters   ·   Fault Injection   ·   Benchmark Store", C.teal, C.tealSoft],
    ["LANE B — DIAGNOSIS · NOOR", "Trace Normalizer → Graph Builder → Semantic Error Diagnostic + Backward Causal Tracer", C.orange, C.orangeSoft],
    ["LANE C — PLATFORM · SAIF", "Repair Agent → Verified Automatic Repair → Recovery Controller / Memory (Tier 2) → API → Dashboard", C.indigo, C.indigoSoft],
  ];
  let ly = ay + 0.34;
  const laneH = 0.95;
  lanes.forEach(([lab, content, fg, bg], i) => {
    s.addShape(pres.ShapeType.roundRect, { x: bx + 0.16, y: ly, w: bw - 1.88, h: laneH - 0.12, rectRadius: 0.05, fill: { color: bg }, line: { color: fg, width: 1 } });
    s.addText(lab, { x: bx + 0.30, y: ly + 0.06, w: bw - 2.16, h: 0.22, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 8.3, bold: true, color: fg });
    s.addText(content, { x: bx + 0.30, y: ly + 0.29, w: bw - 2.16, h: 0.48, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.3, color: C.textDark });
    if (i < 2) s.addShape(pres.ShapeType.line, { x: bx + (bw - 1.88) / 2, y: ly + laneH - 0.12, w: 0, h: 0.12, line: { color: C.textMuted, width: 1.25, endArrowType: "triangle" } });
    ly += laneH;
  });

  s.addShape(pres.ShapeType.roundRect, { x: bx + bw - 1.55, y: ay + 0.38, w: 1.38, h: 0.98, rectRadius: 0.05, fill: { color: "FBF3E3" }, line: { color: C.gold, width: 1, dashType: "dash" } });
  s.addText([{ text: "LLM API", options: { bold: true, breakLine: true, fontSize: 9.8, color: C.goldDark } }, { text: "core-assist only\n~15–20% of components", options: { fontSize: 7.6, color: C.textMuted } }], { x: bx + bw - 1.49, y: ay + 0.46, w: 1.26, h: 0.84, isTextBox: true, margin: 0, fontFace: F_BODY, align: "center", valign: "middle" });

  // C.16 slide 6 asks for "boundaries AND the intended deployment target" — both stated here.
  s.addText([
    { text: "In scope: ", options: { bold: true, color: C.textDark } },
    { text: "10 committed mechanisms (Tier 1 + gated Tier 2).     ", options: { color: C.textMuted } },
    { text: "Out of scope: ", options: { bold: true, color: C.textDark } },
    { text: "message queues, Kubernetes / multi-region, full RBAC, DR infrastructure, multi-tenant billing.     ", options: { color: C.textMuted } },
    { text: "Deployment target: ", options: { bold: true, color: C.goldDark } },
    { text: "containerized (Docker) with a pip-installable SDK — installed and operated from documented steps by someone who did not build it.", options: { color: C.textMuted } },
  ], {
    x: bx, y: ay + ah + 0.08, w: bw, h: 0.36, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9, italic: true,
  });
  // Pointer to the full requirements/design set added 2026-09-06 (R39) — carried over
  // from v1 so both decks cite the same traceable spec behind this diagram.
  evidence(s, MX, ay + ah + 0.44, CW, "Software_Design_Specification.md §2–§6  ·  plan §7.0 (frozen scope)  ·  architecture-sketch.md");
  evidence(s, MX, ay + ah + 0.64, CW, "Full traceable spec: Use Case Model + diagram · 3 System Sequence Diagrams · SRS · Test Plan · Software Development Plan · Traceability Matrix · 16-screen wireframes");

  s.addNotes("Say unprompted: 'controlled, not deterministic' — the replay protocol is deterministic, LLM-step variance is measured over N replays, never assumed away (R25). Say unprompted: the Semantic Error Diagnostic abstains where no checkable constraint exists, and the abstention rate is reported as a metric, not hidden.");
}

// ============================================================
// SLIDE 7 — POC-lite / feasibility evidence
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 7, "POC / Feasibility Evidence", "“Show the evidence — do not merely describe that it exists”");

  const stats = [["71.4%", "agent accuracy — mean of 5 real runs"], ["13.2%", "step accuracy — mean of 5 real runs"], ["4 / 6", "Repair Agent success (Spike 8)"], ["8 / 8", "spikes with real, on-disk evidence"]];
  let sx = MX;
  const statW = CW / 4;
  stats.forEach(([n, l]) => {
    s.addText(n, { x: sx, y: 1.46, w: statW - 0.2, h: 0.52, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 29, bold: true, color: C.goldDark });
    s.addText(l, { x: sx, y: 1.98, w: statW - 0.3, h: 0.44, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.3, color: C.textMuted });
    sx += statW;
  });
  s.addShape(pres.ShapeType.line, { x: MX, y: 2.46, w: CW, h: 0, line: { color: C.border, width: 0.75 } });

  const spikeRows = [
    ["#", "Spike", "Status", "Result"],
    ["1", "ErrorProbe reproduction (simplified)", "DEMONSTRATED", "agent 62.5–85.7% (mean 71.4%) · step 0–25% (mean 13.2%) — 5 real runs, a range not a point estimate"],
    ["2", "CrewAI instrumentation", "DEMONSTRATED", "Clean trace: 3 nodes, 2 correctly-ordered edges"],
    ["3/3b", "Fault injection", "DEMONSTRATED", "Ground truth unambiguous; one case self-corrected by the agent — kept as a finding"],
    ["4", "Semantic Error Diagnostic", "DEMONSTRATED", "Catches known-wrong values incl. a near-miss ($20.00 vs $19.75), zero false positives"],
    ["5", "Controlled counterfactual replay", "DEMONSTRATED", "Corrupted trace 97.2 → recovered 108.0, recovery_success = true"],
    ["6", "Cyclic graph handling", "DEMONSTRATED", "Bound proven load-bearing: control run with it disabled hit the 10,000-step safety cap"],
    ["7", "Preventive classifier", "HONEST NEGATIVE", "precision / recall / F1 = 0.25, near-random — reported, not hidden"],
    ["8", "Repair Agent", "DEMONSTRATED", "4/6 repair success; both failures share one precisely diagnosed, fixable cause"],
  ];
  const tRows = spikeRows.map((r, ri) => r.map((c, ci) => {
    if (ri === 0) return { text: c, options: { bold: true, fill: { color: C.panel }, color: C.textLight, fontSize: 9, align: ci === 0 ? "center" : "left", valign: "middle" } };
    const isNeg = r[2] === "HONEST NEGATIVE";
    return {
      text: c,
      options: {
        fontSize: 8.8, valign: "middle", align: ci === 0 ? "center" : "left",
        bold: ci === 2,
        color: ci === 2 ? (isNeg ? C.amber : C.green) : C.textDark,
        fill: { color: isNeg ? C.amberSoft : (ri % 2 === 0 ? C.paper : C.card) },
      },
    };
  }));
  s.addTable(tRows, {
    x: MX, y: 2.62, w: CW, h: 3.35,
    colW: [0.5, 2.55, 2.05, 7.02],
    border: { type: "solid", color: C.border, pt: 0.5 },
    autoPage: false, fontFace: F_BODY,
  });

  card(s, MX, 6.06, CW, 0.66, C.amberSoft, C.amber);
  s.addText([{ text: "In progress: ", options: { bold: true, color: C.amber } }, { text: "full 3-stage reproduction (top FYP-1 priority).     ", options: { color: C.textDark } }, { text: "Planned: ", options: { bold: true, color: C.amber } }, { text: "Recovery Controller + Verified Repair Memory Tier-2 gates — pre-registered Mid-1 criteria, not yet run.", options: { color: C.textDark } }], {
    x: MX + 0.22, y: 6.17, w: CW - 0.44, h: 0.44, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.8,
  });
  evidence(s, MX, 6.80, CW, "dev/spikes/poc/ (8 scripts + output JSONs on disk)  ·  markdowns/04-poc-evidence/POC_Spike_Outputs_Full.md");

  s.addNotes("Lead with Spike 7's negative result and Spike 8's failure analysis — quote the guide's own words on this directly: a POC that disproved an assumption is more valuable than one that confirmed it. Every number on this slide is real and recomputable from files in the repository; offer to open one.");
}

// ============================================================
// SLIDE 8 — Evaluation plan AND risks  (official structure)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 8, "Evaluation Plan & Risks", "Thresholds and fallbacks decided before any result exists");

  card(s, MX, 1.48, CW, 0.72, C.card, C.gold);
  s.addText([{ text: "Pre-registered acceptance band.  ", options: { bold: true, color: C.goldDark } }, { text: "Reproduction accepted within ±10 points of ErrorProbe's published 59.5% on a comparable-class backbone. Outside the band, both numbers are reported transparently per Annex A.2 — declared before the run, not after.", options: { color: C.textDark } }], {
    x: MX + 0.26, y: 1.58, w: CW - 0.52, h: 0.54, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.5, valign: "middle",
  });

  const lx = MX, lw = 5.35;
  label(s, lx, 2.34, lw, "Metrics");
  bullets(s, [
    "Agent / step accuracy · propagation-path F1",
    "Silent-failure precision / recall + coverage (abstention rate)",
    "Pipeline false-positive rate on 15–20% clean controls — absent from every paper and platform reviewed",
    "Task completion · recovery rate · repair success · false-repair rate",
    "Diagnostic latency overhead — the measurable NFR, target < 50%",
  ], { x: lx, y: 2.62, w: lw, h: 1.85, fontSize: 10.3 });

  // C.16 slide 8 asks for "baseline, DATA OR SCENARIOS, metrics, success criteria..." —
  // the data/scenarios half is named here rather than left implicit.
  card(s, lx, 4.54, lw, 0.95, C.card);
  label(s, lx + 0.20, 4.62, lw - 0.4, "Data / scenarios  ·  statistical protocol", C.textMuted);
  s.addText([
    { text: "Data: ", options: { bold: true, color: C.textDark } },
    { text: "Who&When (184 real cases) for the reproduction; our own cross-architecture fault-injection benchmark on GSM8K + tau-bench retail substrates, with 15–20% deliberately clean controls.  ", options: { color: C.textDark } },
    { text: "Protocol: ", options: { bold: true, color: C.textDark } },
    { text: "bootstrap 95% CIs · fixed seeds · N=5 replay variance · 4-item pre-declared ablation matrix · human baseline.", options: { color: C.textDark } },
  ], {
    x: lx + 0.20, y: 4.84, w: lw - 0.4, h: 0.62, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.6,
  });
  card(s, lx, 5.60, lw, 0.80, C.redSoft, C.red);
  s.addText([{ text: "Cannot support: ", options: { bold: true, color: C.red } }, { text: "production-scale reliability claims beyond the tested frameworks and task domains — stated up front, not extracted under questioning.", options: { color: C.textDark } }], {
    x: lx + 0.20, y: 5.70, w: lw - 0.4, h: 0.62, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.5, valign: "middle",
  });

  // middle: success bands
  const mx3 = lx + lw + 0.26, mw3 = 2.85;
  label(s, mx3, 2.34, mw3, "Success bands");
  const bands = [
    ["Failure", "No measurable improvement anywhere", C.red, C.redSoft],
    ["Acceptable", "Parity on Who&When + any cross-arch result", C.amber, C.amberSoft],
    ["Strong", "Beats baseline on unseen archs, >70% SF recall", C.teal, C.tealSoft],
    ["Exceptional", "Strong + >50% verified-repair recovery", C.green, C.greenSoft],
  ];
  let by = 2.62;
  bands.forEach(([n, d, fg, bg]) => {
    card(s, mx3, by, mw3, 0.78, bg, fg);
    s.addText(n, { x: mx3 + 0.18, y: by + 0.07, w: mw3 - 0.36, h: 0.25, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 11.5, bold: true, color: fg });
    s.addText(d, { x: mx3 + 0.18, y: by + 0.33, w: mw3 - 0.36, h: 0.42, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.6, color: C.textDark });
    by += 0.86;
  });

  // right: risks → fallback
  const rx = mx3 + mw3 + 0.26, rw = CW - (rx - MX);
  label(s, rx, 2.34, rw, "Top risks → stated fallback");
  const risks = [
    ["Reproduction misses the ±10pt band — now expected (local backbone)", "Transparent dual-reporting (Annex A.2) — the anticipated path, not a failure"],
    ["Recovery Controller gate fails at Mid-1", "Resume via controlled replay — Tier 1 already delivers it"],
    ["Verified Repair Memory re-test fails again", "Ships as a memory-on/off ablation — still a legitimate contribution"],
    ["Benchmark scale stalls below 500", "Floor of 500; 300-with-statistics beats 1,000-without"],
  ];
  let ry = 2.62;
  risks.forEach(([r, f]) => {
    card(s, rx, ry, rw, 0.78, C.card);
    s.addText(r, { x: rx + 0.18, y: ry + 0.07, w: rw - 0.36, h: 0.32, isTextBox: true, margin: 0, fontFace: F_BODY, bold: true, fontSize: 9.5, color: C.textDark });
    s.addText(f, { x: rx + 0.18, y: ry + 0.40, w: rw - 0.36, h: 0.34, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.8, color: C.green });
    ry += 0.86;
  });
  card(s, mx3, 6.12, CW - (mx3 - MX), 0.62, C.indigoSoft, C.indigo);
  s.addText([{ text: "Tool / API / GenAI boundary:  ", options: { bold: true, color: C.indigo } }, { text: "every external component classified Support / Core-assist / Core-replacement on Form 13. Nothing we claim as contribution sits in core-replacement — the LLM is core-assist, and the contribution survives swapping it.", options: { color: C.textDark } }], {
    x: mx3 + 0.20, y: 6.21, w: CW - (mx3 - MX) - 0.4, h: 0.46, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.1,
  });
  evidence(s, MX, 6.80, CW, "plan §11 (acceptance band, pre-registered)  ·  Form13_GenAI_Disclosure_Sheet.md  ·  risk-register.md (R4/R25/R37)");

  s.addNotes("The false-positive-rate-on-clean-controls metric is absent from every paper in the reviewed corpus and every platform checked — say this is the field's gap, not just ours. Deliver the risk column as confidence, not confession: each decision rule was pre-registered before results exist, which is exactly what the guide's change-control section asks for.");
}

// ============================================================
// SLIDE 9 — Work division & iteration plan  (official structure)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 9, "Scope, Work Division & Iteration Plan", "Committed scope, member-wise ownership, dependencies and milestones");

  const members = [
    ["Shahoud Shahid", "23i-2515", "DATA / BENCHMARK", [
      "Framework instrumentation (CrewAI, LangGraph)",
      "Fault-injection operators + ground-truth labelling",
      "Cross-architecture benchmark build & licensed release",
    ], "If removed: no cross-architecture benchmark exists — the core research claim is untestable", C.teal, C.tealSoft],
    ["Muhammad Noor", "23i-2520", "DIAGNOSIS ENGINE", [
      "Execution-graph construction + trace normalization",
      "ErrorProbe reproduction and the measured baseline",
      "Semantic Error Diagnostic + backward causal tracing",
    ], "If removed: no attribution algorithm and no silent-failure detection — the contribution disappears", C.orange, C.orangeSoft],
    ["Saif Shahzad", "23i-2634", "PLATFORM", [
      "Counterfactual replay + Recovery Controller",
      "Framework-agnostic SDK, FastAPI backend, Postgres",
      "React dashboard, containerized deployment",
    ], "If removed: nothing is installable or operable outside the development machine", C.indigo, C.indigoSoft],
  ];
  const mw = (CW - 0.44) / 3;
  let mx2 = MX;
  members.forEach(([n, roll, role, own, rm, fg, bg]) => {
    card(s, mx2, 1.44, mw, 2.26, bg, fg);
    s.addText([
      { text: n, options: { bold: true, fontSize: 13, fontFace: F_TITLE, color: C.textDark } },
      { text: `   ${roll}`, options: { fontSize: 8.5, fontFace: F_MONO, color: C.textMuted } },
    ], { x: mx2 + 0.20, y: 1.54, w: mw - 0.4, h: 0.28, isTextBox: true, margin: 0 });
    chip(s, mx2 + 0.20, 1.86, 2.05, role, C.textLight, fg);
    bullets(s, own, { x: mx2 + 0.20, y: 2.22, w: mw - 0.4, h: 0.98, fontSize: 9 });
    s.addShape(pres.ShapeType.line, { x: mx2 + 0.20, y: 3.24, w: mw - 0.4, h: 0, line: { color: fg, width: 0.75 } });
    s.addText(rm, { x: mx2 + 0.20, y: 3.30, w: mw - 0.4, h: 0.36, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.4, italic: true, color: C.textMuted });
    mx2 += mw + 0.22;
  });

  // Handbook C.16 slide 9 requires these explicitly: committed scope, optional
  // extensions, resources, modern tools / external dependencies, deployment target.
  const scopeCols = [
    ["COMMITTED CORE", "Tier 1 — 8 items, evidence-backed, unconditional.  Tier 2 — 2 items (Recovery Controller, Verified Repair Memory), gated on pre-registered Mid-1 criteria.  8 further extensions sit behind the core and are built only after it works.", C.green],
    ["RESOURCES", "$0 committed — local Ollama for every model call, including reproduction and evaluation. A paid comparable-class backbone was priced (≈$353, ≈$881 ceiling) and explicitly declined, with the confound dual-reported.", C.amber],
    ["TOOLS · DEPENDENCIES · DEPLOYMENT", "Python · FastAPI · React/TypeScript · Postgres · Docker · CrewAI · LangGraph · Ollama · GitHub Actions.  Ships as a container plus a pip-installable SDK — operable by someone who did not build it.", C.indigo],
  ];
  const scw = (CW - 0.44) / 3;
  let scx = MX;
  scopeCols.forEach(([h, body, fg]) => {
    card(s, scx, 3.78, scw, 0.94, C.card, fg);
    s.addText(h, { x: scx + 0.20, y: 3.86, w: scw - 0.38, h: 0.20, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 8.2, bold: true, color: fg, charSpacing: 0.8 });
    s.addText(body, { x: scx + 0.20, y: 4.06, w: scw - 0.38, h: 0.62, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.3, color: C.textDark });
    scx += scw + 0.22;
  });

  label(s, MX, 4.82, CW, "FYP-1 → FYP-2 milestones (five approval gates)");
  const gates = [
    ["GATE 1", "Proposal Defense", "scope approved"],
    ["GATE 2/3", "Mid-1", "reproduction + both Tier-2 gates + design baseline"],
    ["GATE 3", "Final-1", "integrated working core, end to end"],
    ["GATE 4", "Mid-2", "benchmark ≥ 500 · release readiness"],
    ["GATE 5", "Final-2", "full evaluation, UAT, deployed + released"],
  ];
  const gw = CW / gates.length;
  s.addShape(pres.ShapeType.line, { x: MX + gw / 2, y: 5.32, w: CW - gw, h: 0, line: { color: C.gold, width: 2 } });
  gates.forEach(([g, n, d], i) => {
    const gx = MX + i * gw + gw / 2;
    s.addShape(pres.ShapeType.ellipse, { x: gx - 0.10, y: 5.22, w: 0.20, h: 0.20, fill: { color: i === 0 ? C.gold : C.paper }, line: { color: C.gold, width: 2 } });
    s.addText([
      { text: g, options: { fontFace: F_MONO, fontSize: 8, bold: true, color: C.goldDark, breakLine: true } },
      { text: n, options: { fontFace: F_BODY, fontSize: 10, bold: true, color: C.textDark, breakLine: true } },
      { text: d, options: { fontFace: F_BODY, fontSize: 8, color: C.textMuted } },
    ], { x: gx - gw / 2 + 0.12, y: 5.46, w: gw - 0.24, h: 0.66, isTextBox: true, margin: 0, align: "center" });
  });

  card(s, MX, 6.16, CW, 0.54, C.card, C.gold);
  s.addText([
    { text: "Effort budget:  ", options: { bold: true, color: C.goldDark, fontSize: 9.8 } },
    { text: "490h (FYP-1) + 640h (FYP-2) = 1,130h, budgeted line-by-line against 1,130h of capacity (3 × ~15h/week × ~28 weeks). Balanced depth, not identical tasks — each lane carries decisions, implementation and validation.", options: { color: C.textDark, fontSize: 9.4 } },
  ], { x: MX + 0.22, y: 6.24, w: CW - 0.44, h: 0.40, isTextBox: true, margin: 0, fontFace: F_BODY });
  evidence(s, MX, 6.76, CW, "plan §3 (ownership) · §7.0 (frozen scope) · §12 (effort) · cost-estimate.md · 06_Expanded_Scope_and_Feasibility_Plan.md");

  s.addNotes("Each member states their own subsystem in one sentence, aloud — the panel is applying the guide's four ownership questions (explain / justify against an alternative / predict what breaks / modify under questioning), and hearing three distinct voices here sets that tone early. The 'if removed' line under each card is the guide's own scope test, answered honestly rather than asserted.");
}

// ============================================================
// SLIDE 10 — Team responsibilities & iterations, DEI, Ethics/Legal
// (handbook C.16 slide 10 in full: "Primary technical ownership, shared
//  integration/quality work and FYP-1/FYP-2 milestones, DEI statement,
//  ethical and legal statement". Individual ownership is detailed on slide 9,
//  so this slide carries the SHARED half — the part C.5 says stays a team
//  responsibility even when one member leads — plus the compliance statements.)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 10, "Team Responsibilities, Iterations, DEI & Ethics/Legal", "What stays shared, how it iterates, and the compliance lines the guide names");

  // --- Row 1: primary ownership recap + shared engineering responsibilities ---
  card(s, MX, 1.44, CW, 1.00, C.card, C.gold);
  label(s, MX + 0.24, 1.53, 3.6, "Primary ownership (detail on slide 9)");
  const owners = [
    ["Shahoud", "Benchmark", C.teal],
    ["Noor", "Diagnosis", C.orange],
    ["Saif", "Platform", C.indigo],
  ];
  let ox = MX + 0.24;
  owners.forEach(([n, lane, col]) => {
    s.addText([
      { text: `${n} — `, options: { bold: true, fontSize: 9.4, color: C.textDark } },
      { text: lane, options: { fontSize: 9.4, color: col, bold: true } },
    ], { x: ox, y: 1.80, w: 1.72, h: 0.22, isTextBox: true, margin: 0, fontFace: F_BODY });
    ox += 1.74;
  });
  s.addText("Each lane carries its own decisions, implementation and validation — not slides or manual testing.", {
    x: MX + 0.24, y: 2.06, w: 5.0, h: 0.28, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.8, italic: true, color: C.textMuted,
  });
  s.addShape(pres.ShapeType.line, { x: MX + 5.55, y: 1.56, w: 0, h: 0.76, line: { color: C.border, width: 1 } });
  label(s, MX + 5.80, 1.53, 6.0, "Shared by all three — never delegated to one member", C.goldDark);
  s.addText("System architecture   ·   integration across the three lanes   ·   quality assurance and the defect list   ·   security, ethics and data handling   ·   repository and change-control discipline   ·   the final defense itself. Per guide §C.5 these remain team responsibilities even where one member leads the component.", {
    x: MX + 5.80, y: 1.79, w: CW - 6.04, h: 0.56, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.8, color: C.textDark,
  });

  // --- Row 2: iteration cadence across the five gates ---
  label(s, MX, 2.54, CW, "Iteration plan — what the team jointly owns at each gate");
  const iters = [
    ["FYP-1", "Gate 1 · Proposal", "scope + POC evidence approved", C.gold],
    ["FYP-1", "Gate 2/3 · Mid-1", "requirements + design baselined; reproduction run; both Tier-2 gates judged", C.gold],
    ["FYP-1", "Gate 3 · Final-1", "integrated core working end to end, integration proven not assumed", C.gold],
    ["FYP-2", "Gate 4 · Mid-2", "benchmark ≥500; non-functional targets measured; UAT plan exists", C.indigo],
    ["FYP-2", "Gate 5 · Final-2", "full evaluation, acceptance testing, deployed + released", C.indigo],
  ];
  const iw = (CW - 0.32) / 5;
  let ix = MX;
  iters.forEach(([phase, gate, what, col]) => {
    card(s, ix, 2.82, iw, 0.92, C.paper, col);
    s.addText(phase, { x: ix + 0.16, y: 2.88, w: iw - 0.3, h: 0.18, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 7.2, bold: true, color: col, charSpacing: 0.6 });
    s.addText(gate, { x: ix + 0.16, y: 3.05, w: iw - 0.3, h: 0.20, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.4, bold: true, color: C.textDark });
    s.addText(what, { x: ix + 0.16, y: 3.26, w: iw - 0.3, h: 0.44, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 7.8, color: C.textMuted });
    ix += iw + 0.08;
  });

  // --- Row 3: DEI / Ethical / Legal statements ---
  const bandW = (CW - 0.44) / 3;
  const bands = [
    ["DEI", C.teal, C.tealSoft, [
      "Open-source release (MIT / CC BY 4.0) puts enterprise-grade diagnostic tooling within reach of resource-constrained teams — the SDG 9 access-equity line made concrete",
      "Dashboard pairs colour with text and shape, never colour alone — WCAG contrast check owed by Final-1, named as owed",
      "Accuracy claims stated as English-only, not generalized",
    ]],
    ["ETHICAL", C.red, C.redSoft, [
      "Diagnosis is advisory, never autonomous — every repair is human-gated before it is applied",
      "Informed consent required for any real user's trace data; synthetic substrate by default",
      "Fault injection restricted to our own or explicitly consenting systems",
      "Negative results published as found — Spike 7 is on the evidence slide, not buried",
    ]],
    ["LEGAL / PROFESSIONAL", C.indigo, C.indigoSoft, [
      "Who&When · GSM8K · tau-bench retail — all MIT, each licence confirmed against its own LICENSE file, not a secondary claim",
      "Released artefacts carry MIT / CC BY 4.0, attribution preserved upstream",
      "AI usage disclosed per session (19 logged) on Form 13, countersigned by the supervisor",
    ]],
  ];
  let bx2 = MX;
  bands.forEach(([lab, fg, bg, pts]) => {
    card(s, bx2, 3.84, bandW, 1.76, bg, fg);
    s.addText(lab, { x: bx2 + 0.20, y: 3.92, w: bandW - 0.4, h: 0.22, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9, bold: true, color: fg, charSpacing: 1.2 });
    bullets(s, pts, { x: bx2 + 0.20, y: 4.16, w: bandW - 0.4, h: 1.36, fontSize: 8.2 });
    bx2 += bandW + 0.22;
  });

  // --- Row 4: AI-assisted development level (handbook C.8) + the ownership standard ---
  card(s, MX, 5.70, CW, 1.02, C.ink2);
  s.addText("AI-ASSISTED DEVELOPMENT LEVEL — REQUIRED TO BE NAMED AND JUSTIFIED AT THIS STAGE (HANDBOOK C.8)", {
    x: MX + 0.28, y: 5.78, w: CW - 0.56, h: 0.22, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 8.8, bold: true, color: C.goldLight, charSpacing: 0.8,
  });
  s.addText([
    { text: "Level 2 — AI-Assisted.  ", options: { bold: true, color: C.goldLight, fontSize: 12, fontFace: F_TITLE } },
    { text: "Humans lead both judgment and execution; AI assists with isolated tasks — checked against our own log before claiming it. Level 3 would relocate exactly the design and evaluation work Seoul Accord GA-4 requires the graduate to demonstrate.  ", options: { color: C.textLightMuted, fontSize: 9 } },
    { text: "Ownership standard accepted: ", options: { bold: true, color: C.goldLight, fontSize: 9 } },
    { text: "for every CCP-relevant component the responsible member can explain it, justify it against a rejected alternative, predict what breaks, and modify it under questioning. Authorship of keystrokes is not the test.", options: { color: C.textLightMuted, fontSize: 9 } },
  ], { x: MX + 0.28, y: 6.02, w: CW - 0.56, h: 0.64, isTextBox: true, margin: 0, fontFace: F_BODY });

  evidence(s, MX, 6.80, CW, "plan §3 (ownership) · guide §C.5 (shared responsibilities) · AI_Usage_Log.md · Form13_GenAI_Disclosure_Sheet.md · risk-register R30/R38");

  s.addNotes("The DEI line is a real, checkable commitment, not a decorative label — say the access-equity sentence in your own words. Name Level 2 out loud and say why it is not Level 3: accreditation requires the graduate to have done the design and evaluation, and delegating that would forfeit the attribute. If asked about AI use at all, the answer is that it is logged per session, disclosed on Form 13, and that every CCP-relevant component has a member who can defend it live — offer to demonstrate that on any component they pick.");
}

pres.writeFile({ fileName: "Granite_Proposal_Defense_v2.pptx" }).then(fn => console.log("Wrote", fn));
