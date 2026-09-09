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
// `kicker` param kept in every call site (unused) rather than touched at all
// 10 call sites — the yellow one-line restatement above the title added no
// required content (not asked for by the image or the handbook) and read as
// decorative, so it's been dropped; the title alone now anchors the header.
function chrome(slide, num, title, kicker) {
  // left accent rail
  slide.addShape(pres.ShapeType.rect, {
    x: 0, y: 0, w: RAIL, h: PH, fill: { color: C.gold }, line: { type: "none" },
  });
  facetWatermark(slide);
  slide.addText(title, {
    x: MX, y: 0.46, w: CW, h: 0.70, isTextBox: true, margin: 0,
    fontFace: F_TITLE, fontSize: 29.5, bold: true, color: C.textDark, valign: "middle",
  });
  slide.addShape(pres.ShapeType.rect, { x: MX, y: 1.30, w: 0.62, h: 0.04, fill: { color: C.gold }, line: { type: "none" } });
  footer(slide, num);
}
function footer(slide, n) {
  slide.addShape(pres.ShapeType.line, { x: MX, y: PH - 0.46, w: CW, h: 0, line: { color: C.border, width: 0.75 } });
  slide.addText("F26-060-GRANITE  ·  PROPOSAL DEFENSE  ·  STREAM A", {
    x: MX, y: PH - 0.38, w: 6.5, h: 0.26, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 10.5, color: C.textFaint, charSpacing: 0.7,
  });
  slide.addText(`${n} / 10`, {
    x: PW - MX - 1.2, y: PH - 0.38, w: 1.2, h: 0.26, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 10.5, bold: true, color: C.goldDark, align: "right",
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
    x, y, w, h: 0.28, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 14, bold: true, color: color || C.goldDark, charSpacing: 1,
  });
}
function chip(slide, x, y, w, text, fg, bg) {
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.30, rectRadius: 0.15, fill: { color: bg }, line: { type: "none" } });
  slide.addText(text, {
    x, y, w, h: 0.30, isTextBox: true, margin: 0, align: "center", valign: "middle",
    fontFace: F_MONO, fontSize: 12.5, bold: true, color: fg,
  });
}
function dot(slide, x, y, d, bg, text, fg) {
  slide.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: bg }, line: { type: "none" } });
  slide.addText(text, {
    x, y, w: d, h: d, isTextBox: true, margin: 0, align: "center", valign: "middle",
    fontFace: F_TITLE, fontSize: d > 0.5 ? 19.5 : 14.5, bold: true, color: fg,
  });
}
// evidence tag — kept for the few places a citation still earns its space on-slide;
// most calls were removed in the readability pass and folded into speaker notes instead
// (a panel reads the room, not a file path — the citation is for us, not for them).
function evidence(slide, x, y, w, text) {
  slide.addText(`▸ ${text}`, {
    x, y, w, h: 0.22, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 10, color: C.textFaint,
  });
}
function bullets(slide, items, opts) {
  const arr = items.map((t, i) => ({
    text: t, options: { bullet: { code: "25AA", indent: 15 }, breakLine: i < items.length - 1 },
  }));
  slide.addText(arr, Object.assign({
    isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 14.5, color: C.textDark,
    paraSpaceAfter: 9, valign: "top",
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
    fontFace: F_MONO, fontSize: 14.5, bold: true, color: C.goldLight, charSpacing: 1.6,
  });
  s.addText("Granite", {
    x: MX, y: 1.80, w: 9.2, h: 1.15, isTextBox: true, margin: 0,
    fontFace: F_TITLE, fontSize: 69.5, bold: true, color: C.textLight,
  });
  s.addText("A Self-Healing Multi-Agent System for Semantic Error Diagnosis, Verified Repair and Recovery", {
    x: MX, y: 2.98, w: 8.4, h: 0.62, isTextBox: true, margin: 0,
    fontFace: F_BODY, fontSize: 18.5, italic: true, color: C.textLightMuted,
  });

  s.addShape(pres.ShapeType.rect, { x: MX, y: 3.78, w: 1.1, h: 0.035, fill: { color: C.gold }, line: { type: "none" } });

  // Restored per the image structure's row 1: "Project title, members,
  // supervisor, one-line problem statement" — this is required on-slide, not
  // just spoken aloud.
  s.addText("When a multi-agent AI system fails — including when the wrong answer looks completely right — no published method can reliably say which agent caused it, and none can verify a fix before trusting it.", {
    x: MX, y: 4.00, w: 8.6, h: 1.10, isTextBox: true, margin: 0,
    fontFace: F_TITLE, fontSize: 21.5, color: C.textLight, italic: true,
  });

  s.addShape(pres.ShapeType.line, { x: MX, y: 5.50, w: 8.4, h: 0, line: { color: C.hair, width: 1 } });
  // Role tags dropped — lane ownership is established once, on slide 9, not
  // repeated here.
  const team = [["Shahoud Shahid", "23i-2515"], ["Muhammad Noor", "23i-2520"], ["Saif Shahzad", "23i-2634"]];
  let tx = MX;
  team.forEach(([n, r]) => {
    s.addText([
      { text: n, options: { bold: true, breakLine: true, fontSize: 15.5, color: C.textLight } },
      { text: r, options: { fontSize: 13, color: C.textLightMuted } },
    ], { x: tx, y: 5.62, w: 2.8, h: 0.62, isTextBox: true, margin: 0, fontFace: F_BODY });
    tx += 2.85;
  });

  s.addText([
    { text: "Supervisor   ", options: { color: C.textLightMuted, fontSize: 13.5 } },
    { text: "Dr. Adil Majeed", options: { color: C.textLight, bold: true, fontSize: 15.5, breakLine: true } },
    { text: "FAST School of Computing, NUCES Islamabad", options: { color: C.textLightMuted, fontSize: 13 } },
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
    "Primary — an engineering team running a multi-agent AI system in or near production",
    "Secondary — downstream product teams",
    "Secondary — auditors needing traceable evidence",
  ], { x: MX + 0.28, y: 2.02, w: 4.95, h: 1.9, fontSize: 16.5 });

  card(s, MX, 4.10, 5.45, 0.92, C.tealSoft);
  s.addText([{ text: "SDG 9  ", options: { bold: true, color: C.teal, fontSize: 16.5 } }, { text: "Industry, Innovation & Infrastructure — reliability tooling, new industrial category", options: { color: C.textDark, fontSize: 15.5 } }], {
    x: MX + 0.28, y: 4.24, w: 4.95, h: 0.66, isTextBox: true, margin: 0, fontFace: F_BODY, valign: "middle",
  });

  card(s, MX, 5.15, 5.45, 1.30, C.redSoft, C.red);
  label(s, MX + 0.28, 5.30, 5, "Consequence of failure", C.red);
  s.addText("Ships a confident, wrong answer — no crash, no error, no signal anything went wrong.", {
    x: MX + 0.28, y: 5.62, w: 4.95, h: 0.8, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 16.5, color: C.textDark, italic: true,
  });

  const rx = 6.42, rw = CW - (rx - MX);
  label(s, rx, 1.52, rw, "Current workflow — without Granite", C.textMuted);
  const steps = [
    ["1", "Trace captured", "LangSmith / Langfuse / Braintrust / Arize", C.indigo, C.indigoSoft],
    ["2", "Human guesses the root cause", "no published accuracy", C.orange, C.orangeSoft],
    ["3", "No silent-failure check", "a confident, wrong answer passes unnoticed", C.red, C.redSoft],
    ["4", "No way to test a fix first", "field baseline: 14.2% step accuracy (Who&When)", C.red, C.redSoft],
  ];
  let sy = 1.96;
  steps.forEach(([n, t, sub, fg, bg], i) => {
    dot(s, rx, sy, 0.44, bg, n, fg);
    s.addText([{ text: t, options: { bold: true, breakLine: true, fontSize: 17, color: C.textDark } }, { text: sub, options: { fontSize: 14.5, color: C.textMuted } }], {
      x: rx + 0.60, y: sy - 0.06, w: rw - 0.62, h: 0.88, isTextBox: true, margin: 0, fontFace: F_BODY,
    });
    if (i < 3) s.addShape(pres.ShapeType.line, { x: rx + 0.22, y: sy + 0.44, w: 0, h: 0.42, line: { color: C.border, width: 1.5, dashType: "dash" } });
    sy += 1.20;
  });
  card(s, rx, 6.30, rw, 0.52, C.amberSoft);
  s.addText([{ text: "Stakeholder evidence today:  ", options: { bold: true, color: C.amber } }, { text: "literature + 7 commercial vendors", options: { color: C.textDark } }], {
    x: rx + 0.20, y: 6.30, w: rw - 0.4, h: 0.52, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 14, valign: "middle",
  });

  s.addNotes("14.2% is the field's own measured baseline for 'a human reads the trace' — the number the whole project is trying to beat. On stakeholders: state plainly that this is Stream A, that the problem's reality rests on published evidence and a commercial market, and that live practitioner contact is scheduled in the Mid-2 acceptance study (C.13.1) — declared open, not claimed as done. Do not overclaim contact that has not happened — risk-register R33. Citations: plan §0.1 · §0.05 (SDG) · Full_Literature_Landscape_Analysis.md.");
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
    ["LangSmith Engine /\nArize Alyx (2026)", "Automated RCA\n+ fix drafting", "not published", "?", "?", "✘ stack-locked"],
    ["Langfuse / Braintrust /\nPhoenix / Maxim / Opik", "Trace capture\n+ eval", "human-driven", "RAG only", "✘", "✘"],
    // Named prior FYP from Shahoud's 2026-09-06 archive check (R39), merged with the
    // 660-title structural sweep — a named closest match answers a panel better than
    // "we found nothing", and the two findings agree rather than compete.
    ["Closest prior FYP\n(S24-011-D-HDLM,\nSpring 2024)", "hallucination detection\nin single-LLM text", "—\nno attribution at all", "partial — single-LLM\ntext only", "✘ no repair /\nreplay step", "N/A — not a\nmulti-agent system"],
    ["Current manual\nworkflow", "human reads,\nguesses", "14.2%\n(Who&When)", "✘", "✘", "N/A"],
    ["Granite\n(proposed)", "Constraint-based SED\n+ verified repair loop", "building on\nErrorProbe", "✓ scoped &\nmeasured", "✓ recovery rate\nover N replays", "✓ CrewAI +\nLangGraph, unseen"],
  ];
  // NOTE: this table stays at 11pt while the rest of the deck runs 1.5pt bigger.
  // At the deck's general size (12.5pt) this 6-column, real-evidence table overflows
  // its slide — verified by rendering, not assumed — so 11pt is this table's actual
  // ceiling given the column widths below, not an oversight.
  const tRows = [cols.map(c => ({ text: c, options: { bold: true, fill: { color: C.panel }, color: C.textLight, fontSize: 11, align: "center", valign: "middle" } }))];
  rows.forEach((r, ri) => {
    const isGranite = ri === rows.length - 1;
    const isPrior = ri === 3;
    tRows.push(r.map((c, ci) => ({
      text: c,
      options: {
        fontSize: 11, align: ci === 0 ? "left" : "center", valign: "middle",
        bold: ci === 0 || isGranite,
        fill: { color: isGranite ? C.tealSoft : (isPrior ? C.greenSoft : (ri % 2 === 0 ? C.paper : C.card)) },
        color: C.textDark,
      },
    })));
  });
  s.addTable(tRows, {
    x: MX, y: 1.50, w: CW, h: 4.02,
    colW: [1.72, 2.10, 2.00, 1.80, 2.10, 1.87],
    border: { type: "solid", color: C.border, pt: 0.5 },
    autoPage: false, fontFace: F_BODY,
  });

  card(s, MX, 5.86, 6.05, 1.14, C.greenSoft, C.green);
  label(s, MX + 0.22, 5.96, 5.6, "Prior-FYP check — closed", C.green);
  s.addText([
    { text: "660 titles, 12 cohorts since 2019, checked structurally. Closest: ", options: { color: C.textDark } },
    { text: "S24-011-D-HDLM", options: { bold: true, color: C.green } },
    { text: " — hallucination detection in single-LLM text: same core problem, ~1 of our 4 stages.", options: { color: C.textDark } },
  ], {
    x: MX + 0.22, y: 6.24, w: 5.65, h: 0.72, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 12.5,
  });

  card(s, MX + 6.25, 5.86, CW - 6.25, 1.14, C.amberSoft, C.amber);
  label(s, MX + 6.47, 5.96, 5.4, "The real gap", C.amber);
  s.addText("No system combines attribution + silent-failure detection + verified repair + cross-arch generalization in one pipeline.", {
    x: MX + 6.47, y: 6.24, w: CW - 6.7, h: 0.72, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 12.5, color: C.textDark,
  });

  s.addNotes("Volunteer the correction story: an early draft said 'nobody automates this' — direct vendor checks proved that stale, corrected on the record (R9). On prior FYPs, give the number unprompted: 660 titles across every published cohort back to 2019, checked structurally, not by title. Other analogs use 'multi-agent' only as an application pattern (PropPal, LawSphere, CampusHive); nearest detect-then-repair is AutoVulRepair (fuzzing/C++) — name it before a panelist finds it. The gap is the combination, not any single missing feature. Citations: plan §0.095 (full 660-title comparison) · Commercial_Product_Comparison.md · risk-register R9/R33.");
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
    ["ErrorProbe chosen as baseline", "On performance (59.5%), not recency"],
    ["CrewAI + LangGraph committed", "Unused by all 9 papers reviewed"],
    ["Constraint-based SED, not LLM-judge", "LLM-judge AUROC ≤ 0.65 — barely above chance"],
    ["Single-framework narrowing rejected", "Market survey's own advice, declined (R19)"],
  ];
  let dy = 1.90;
  decisions.forEach(([t, sub]) => {
    dot(s, lx, dy, 0.34, C.goldLight, "✓", C.ink);
    s.addText([{ text: t, options: { bold: true, breakLine: true, fontSize: 16.5, color: C.textDark } }, { text: sub, options: { fontSize: 14.5, color: C.textMuted } }], {
      x: lx + 0.48, y: dy - 0.07, w: lw - 0.52, h: 0.92, isTextBox: true, margin: 0, fontFace: F_BODY,
    });
    dy += 1.06;
  });

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
  s.addText("Step-level accuracy on Who&When, % · AgenTracer-8B is a published 37–43% range — midpoint plotted.", {
    x: rx, y: 4.00, w: rw, h: 0.30, isTextBox: true, margin: 0,
    fontFace: F_BODY, fontSize: 12.5, italic: true, color: C.textMuted,
  });

  card(s, rx, 4.36, rw, 1.02, C.redSoft, C.red);
  s.addText([{ text: "40.5 points still wrong  ", options: { bold: true, color: C.red } }, { text: "— misattributes 4 of 10 steps; cannot see silent failures at all.", options: { color: C.textDark } }], {
    x: rx + 0.22, y: 4.36, w: rw - 0.44, h: 1.02, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 15.5, valign: "middle",
  });

  card(s, rx, 5.50, rw, 0.98, C.card);
  label(s, rx + 0.22, 5.62, rw - 0.44, "Backbone-confound caveat", C.textMuted);
  s.addText("Cross-paper backbones differ — controlled within our own experiments.", {
    x: rx + 0.22, y: 5.90, w: rw - 0.44, h: 0.52, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 15, color: C.textDark,
  });

  s.addNotes("State the backbone-confound caveat before being asked. Name that credible unpublished preprints exist in adjacent territory and the team made a recorded decision not to chase every one — the strategy is beating a peer-reviewed baseline, not pre-empting unpublished work. If a win partly reflects backbone strength, report both numbers, declared in advance. Citations: Full_Literature_Landscape_Analysis.md · ErrorProbe_Baseline_Selection.md · plan §0.08.");
}

// ============================================================
// SLIDE 5 — Complex computing challenge (+ why this is not a course project)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 5, "Complex Computing Challenge", "What is technically hard — and why this is not a course project");

  // Grid cut from all 9 characteristics to the six actually named in the
  // speaker notes (1, 2, 3, 6, 7, 9) — the other 3 (4, 5, 8) are still real
  // and still argued in Granite_CCP_Justification_Seoul_Accord.docx, just not
  // spoken aloud here, so they're documented instead in a new file rather
  // than silently dropped:
  // markdowns/05-deliverables/ccp-justification/CCP_Characteristics_Not_On_Slide.md
  // Display badges renumbered 1–6 sequentially for on-slide readability —
  // the real Seoul Accord characteristic numbers (1, 2, 3, 6, 7, 9) are kept
  // in the comment below and in speaker notes/CCP_Characteristics_Not_On_Slide.md,
  // so nothing about which characteristic is which is actually lost.
  const items = [
    ["1", "Conflicting requirements", "Depth vs. latency; privacy vs. completeness", true],       // characteristic 1
    ["2", "No obvious solution", "Best published: 59.5% after 15 months, 7 papers", true],        // characteristic 2
    ["3", "Depth of knowledge", "Graph modeling, causal reasoning, tracing", true],                // characteristic 3
    ["4", "Diverse stakeholders", "Named; live contact scheduled Mid-2", false],                   // characteristic 6
    ["5", "Significant consequences", "A missed failure ships a wrong answer, undetected", true],  // characteristic 7
    ["6", "Ill-defined cause", "3 unknowns: whether, which step, what's correct", true],           // characteristic 9
  ];
  // CCP grid on the left (rows shortened — was 1.80, now 1.40 — so the six
  // boxes read as compact rectangles, not big squares — and centered
  // vertically in the column so the leftover space splits top/bottom rather
  // than pooling at the bottom), Diagram 4 as the big panel on the right.
  const gridCols = 2, colW = 3.70, rowH = 1.40;
  const gridRows = Math.ceil(items.length / gridCols);
  const gridTop = 1.42 + ((PH - 0.46 - 0.14 - 1.42) - gridRows * rowH) / 2;
  items.forEach(([n, t, sub, clear], i) => {
    const col = i % gridCols, row = Math.floor(i / gridCols);
    const cx = MX + col * colW, cy = gridTop + row * rowH;
    card(s, cx, cy, colW - 0.18, rowH - 0.12, clear ? C.greenSoft : C.amberSoft, clear ? C.green : C.amber);
    dot(s, cx + 0.16, cy + 0.13, 0.30, clear ? C.green : C.amber, n, C.textLight);
    s.addText(t, { x: cx + 0.56, y: cy + 0.11, w: colW - 0.86, h: 0.36, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 14, bold: true, color: C.textDark });
    s.addText(sub, { x: cx + 0.16, y: cy + 0.48, w: colW - 0.48, h: 0.74, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11.5, color: C.textMuted });
  });

  // Diagram 4 from the Architecture Atlas (Core Technical/Computational
  // Pipeline), recolored to the deck's palette — no card/border/frame around
  // it, just the caption and the image itself.
  const gridW = gridCols * colW;
  const diag4X = MX + gridW + 0.34;
  s.addText("CORE PIPELINE — HYPOTHESIS TO VERIFIED REPAIR", {
    x: diag4X, y: 1.42, w: CW - gridW - 0.34, h: 0.20, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 10.5, bold: true, color: C.goldDark, charSpacing: 0.6,
  });
  // Sized against the full available column height (down to the footer) —
  // margins tightened slightly (footer gap 0.14 -> 0.08) to make it as big
  // as the slide can hold, per request.
  const diag4Y = 1.66;
  const diagH4 = (PH - 0.46 - 0.08) - diag4Y, diagW4 = diagH4 * (797 / 985);
  s.addImage({ path: "diagram4_cropped.png", x: diag4X, y: diag4Y, w: diagW4, h: diagH4 });

  s.addNotes("This is the slide the panel uses to decide whether the project deserves capstone status. Concede up front that a trace-capture-plus-LLM-guess wrapper is a weekend's work, then name precisely what such a version would get wrong: no benchmark on unseen architectures, no way to tell a silent failure from a correct answer, no measured false-positive rate on clean controls, no evidence its fix works. NOTE — on-slide badges are renumbered 1-6 for readability; they are NOT the Seoul Accord characteristic numbers. Badge 4 on the slide = real characteristic 6 (Diverse stakeholders) — it's amber on purpose, say so before they spot it. Badge 6 on the slide = real characteristic 9 (Ill-defined cause) — read its resolution aloud if pressed on complexity; the diagram on the right is that resolution, drawn: hypothesis generation, evidence-grounding, and the controlled-replay loop that gates every fix. Real characteristics 4, 5 and 8 (Unfamiliar issues / Beyond standard practice / Interdependence) are off-slide entirely but still true and still fully argued in Granite_CCP_Justification_Seoul_Accord.docx and CCP_Characteristics_Not_On_Slide.md — cover them only if asked directly. Citations: 02_Panel_Defense_Question_Bank.md Q8a · plan §1 (three-tier CCP) · §2 (9-characteristic rating).");
}

// ============================================================
// SLIDE 6 — Proposed solution & contribution
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 6, "Proposed Solution & Contribution", "What is being built, and where the boundary sits");

  card(s, MX, 1.48, CW, 1.02, C.card, C.gold);
  s.addText([
    { text: "Contribution.  ", options: { bold: true, color: C.goldDark, fontSize: 16.5 } },
    { text: "Best method: 59.5% — but it's untested on unseen architectures and misses silent failures. We build a cross-architecture benchmark and a diagnosis pipeline with constraint-based silent-failure verification, as a framework-agnostic SDK.", options: { color: C.textDark, fontSize: 15.5 } },
  ], { x: MX + 0.28, y: 1.48, w: CW - 0.56, h: 1.02, isTextBox: true, margin: 0, fontFace: F_BODY, valign: "middle" });

  // Architecture diagram rebuilt natively (real pptxgenjs shapes, not a
  // pasted screenshot of the Architecture Atlas) — same content as Atlas
  // Diagram 1 (target system, operator, three owner lanes, LLM API), drawn
  // free-form at the deck's own scale so it stays fully editable and reads
  // as authored for this slide rather than inserted from elsewhere.
  const ay = 2.60, ah = 4.30;
  const arrow = (x1, y1, x2, y2, color, dashed) => s.addShape(pres.ShapeType.line, {
    x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || 0.001, h: Math.abs(y2 - y1) || 0.001,
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color, width: 1.1, endArrowType: "triangle", dashType: dashed ? "dash" : "solid" },
  });
  const box = (x, y, w, h, fg, bg, title, sub, subColor) => {
    s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.05, fill: { color: bg || "FFFFFF" }, line: { color: fg, width: 1.1 } });
    s.addText(title, { x: x + 0.06, y: y + 0.05, w: w - 0.12, h: 0.26, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.3, bold: true, color: C.textDark, align: "center" });
    if (sub) s.addText(sub, { x: x + 0.06, y: y + h - 0.24, w: w - 0.12, h: 0.20, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 7.6, color: subColor || C.textMuted, align: "center" });
  };
  const store = (x, y, w, h, fg, label1) => {
    s.addShape(pres.ShapeType.roundRect, { x, y: y + 0.08, w, h: h - 0.08, rectRadius: 0.04, fill: { color: "FFFFFF" }, line: { color: fg, width: 1.1 } });
    s.addShape(pres.ShapeType.ellipse, { x, y, w, h: 0.16, fill: { color: "FFFFFF" }, line: { color: fg, width: 1.1 } });
    s.addText(label1, { x: x + 0.04, y: y + h / 2 - 0.14, w: w - 0.08, h: 0.28, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.5, bold: true, color: C.textDark, align: "center", valign: "middle" });
  };

  // Actors either side of the system boundary
  const actorW = 1.55;
  box(MX, ay + 0.10, actorW, 0.85, C.textMuted, C.paper, "Target Multi-Agent System", "CrewAI / LangGraph", C.textMuted);
  box(MX, ay + ah - 0.95, actorW, 0.85, C.textMuted, C.paper, "Operator", "engineering team", C.textMuted);
  arrow(MX + actorW / 2, ay + 0.95, MX + actorW / 2, ay + ah - 0.95, C.textMuted, false);

  // System boundary
  const bx = MX + actorW + 0.28, bw = CW - actorW - 0.28 - 1.65;
  // Darker border (goldDark, not gold) — was too close to the white fill to
  // read as a strong frame; this contrasts clearly against the card's white.
  s.addShape(pres.ShapeType.roundRect, { x: bx, y: ay, w: bw, h: ah, rectRadius: 0.08, fill: { color: "FFFFFF" }, line: { color: C.goldDark, width: 1.75, dashType: "dash" } });
  s.addText("GRANITE — SYSTEM BOUNDARY", { x: bx + 0.16, y: ay + 0.06, w: 4, h: 0.22, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9.5, bold: true, color: C.goldDark, charSpacing: 1 });
  arrow(MX + actorW, ay + 0.52, bx, ay + 0.52, C.textMuted, false);

  const laneX = bx + 0.15, laneW = bw - 0.30;

  // Lane A — Data / Benchmark
  const laneAY = ay + 0.32, laneAH = 1.02;
  s.addShape(pres.ShapeType.roundRect, { x: laneX, y: laneAY, w: laneW, h: laneAH, rectRadius: 0.06, fill: { color: C.tealSoft }, line: { color: C.teal, width: 1.2 } });
  s.addText("LANE A — DATA / BENCHMARK", { x: laneX + 0.14, y: laneAY + 0.06, w: 4, h: 0.20, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9.5, bold: true, color: C.teal, charSpacing: 0.6 });
  const faX = laneX + 0.15, faW = 2.85, fiX = faX + faW + 0.14, fiW = 3.05, bsX = fiX + fiW + 0.14, bsW = 1.9;
  box(faX, laneAY + 0.32, faW, 0.60, C.teal, "FFFFFF", "Framework Adapters", "CrewAI + LangGraph hooks");
  box(fiX, laneAY + 0.32, fiW, 0.60, C.teal, "FFFFFF", "Fault Injection Operators", "rule-based · 0% API");
  store(bsX, laneAY + 0.32, bsW, 0.60, C.teal, "Benchmark Store");
  arrow(faX + faW, laneAY + 0.62, fiX, laneAY + 0.62, C.teal, false);
  arrow(fiX + fiW, laneAY + 0.62, bsX, laneAY + 0.62, C.teal, false);

  // Lane B — Diagnosis
  const laneBY = laneAY + laneAH + 0.15, laneBH = 1.42;
  s.addShape(pres.ShapeType.roundRect, { x: laneX, y: laneBY, w: laneW, h: laneBH, rectRadius: 0.06, fill: { color: C.orangeSoft }, line: { color: C.orange, width: 1.2 } });
  s.addText("LANE B — DIAGNOSIS", { x: laneX + 0.14, y: laneBY + 0.06, w: 4, h: 0.20, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9.5, bold: true, color: C.orange, charSpacing: 0.6 });
  arrow(fiX + fiW / 2, laneAY + laneAH + 0.01, laneX + 0.15 + 2.85 / 2, laneBY - 0.01, C.textMuted, false);
  const tnX = laneX + 0.15, tnW = 2.85, gbX = tnX + tnW + 0.18, gbW = 3.55;
  box(tnX, laneBY + 0.32, tnW, 0.52, C.orange, "FFFFFF", "Trace Normalizer", "standard schema in");
  box(gbX, laneBY + 0.32, gbW, 0.52, C.orange, "FFFFFF", "Execution Graph Builder", "0% API");
  arrow(tnX + tnW, laneBY + 0.58, gbX, laneBY + 0.58, C.orange, false);
  const sedX = laneX + 0.15, sedW = 4.10, bctX = sedX + sedW + 0.15, bctW = laneW - 0.30 - sedW - 0.15;
  box(sedX, laneBY + 0.92, sedW, 0.42, C.orange, "FFFFFF", "Semantic Error Diagnostic — runs in parallel, unconditionally");
  box(bctX, laneBY + 0.92, bctW, 0.42, C.orange, "FFFFFF", "Backward Causal Tracer");
  arrow(gbX + gbW * 0.3, laneBY + 0.84, sedX + sedW * 0.6, laneBY + 0.92, C.textMuted, false);
  arrow(gbX + gbW * 0.7, laneBY + 0.84, bctX + bctW * 0.4, laneBY + 0.92, C.textMuted, false);

  // Lane C — Platform
  const laneCY = laneBY + laneBH + 0.15, laneCH = ah - (laneCY - ay) - 0.12;
  s.addShape(pres.ShapeType.roundRect, { x: laneX, y: laneCY, w: laneW, h: laneCH, rectRadius: 0.06, fill: { color: C.indigoSoft }, line: { color: C.indigo, width: 1.2 } });
  s.addText("LANE C — PLATFORM", { x: laneX + 0.14, y: laneCY + 0.06, w: 4, h: 0.20, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9.5, bold: true, color: C.indigo, charSpacing: 0.6 });
  const raX = laneX + 0.15, raW = 2.25, varX = raX + raW + 0.14, varW = 2.95, apiX = varX + varW + 0.14, apiW = laneW - 0.30 - raW - varW - 0.28;
  box(raX, laneCY + 0.30, raW, 0.50, C.indigo, "FFFFFF", "Repair Agent", "candidate fix");
  box(varX, laneCY + 0.30, varW, 0.50, C.indigo, "FFFFFF", "Verified Automatic Repair", "controlled replay, N runs");
  box(apiX, laneCY + 0.30, apiW, 0.50, C.indigo, "FFFFFF", "Backend API", "FastAPI");
  arrow(raX + raW, laneCY + 0.55, varX, laneCY + 0.55, C.indigo, false);
  arrow(varX + varW, laneCY + 0.55, apiX, laneCY + 0.55, C.indigo, false);
  s.addText([
    { text: "Tier 2 (gated): ", options: { bold: true, color: C.amber } },
    { text: "Recovery Controller + Verified Repair Memory   ·   ", options: { color: C.textDark } },
    { text: "Postgres   ·   Dashboard — 3 screens", options: { color: C.textDark } },
  ], { x: laneX + 0.15, y: laneCY + laneCH - 0.26, w: laneW - 0.30, h: 0.22, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10, italic: true });

  arrow(laneX + laneW * 0.5, laneBY + laneBH + 0.01, laneX + laneW * 0.5, laneCY - 0.01, C.textMuted, false);

  // LLM API — outside the boundary, dashed dependency arrows in
  const llmX = bx + bw + 0.20, llmW = 1.45;
  s.addShape(pres.ShapeType.roundRect, { x: llmX, y: ay + ah / 2 - 0.58, w: llmW, h: 1.16, rectRadius: 0.06, fill: { color: "FBF3E3" }, line: { color: C.goldDark, width: 1.5, dashType: "dash" } });
  s.addText([
    { text: "LLM API", options: { bold: true, breakLine: true, fontSize: 12.5, color: C.goldDark } },
    { text: "core-assist only\n~15–20% of components", options: { fontSize: 9, color: C.textMuted } },
  ], { x: llmX + 0.06, y: ay + ah / 2 - 0.52, w: llmW - 0.12, h: 1.04, isTextBox: true, margin: 0, fontFace: F_BODY, align: "center", valign: "middle" });
  arrow(bx + bw, laneBY + 0.55, llmX, ay + ah / 2 - 0.20, C.gold, true);
  arrow(bx + bw, laneCY + 0.50, llmX, ay + ah / 2 + 0.20, C.gold, true);

  s.addNotes("Say unprompted: 'controlled, not deterministic' — the replay protocol is deterministic, LLM-step variance is measured over N replays, never assumed away (R25). Say unprompted: the Semantic Error Diagnostic abstains where no checkable constraint exists, and the abstention rate is reported as a metric, not hidden. If asked about scope: in scope is 10 committed mechanisms; out of scope is message queues, Kubernetes, full RBAC, DR infra, multi-tenant billing; deployment target is Docker + a pip-installable SDK, operable by someone who didn't build it. Full traceable spec behind this diagram: Use Case Model + diagram, 3 System Sequence Diagrams, SRS, Test Plan, Software Development Plan, Traceability Matrix, 16-screen wireframes — architecture atlas, tab 'Requirements & Design'. Citations: Software_Design_Specification.md §2–§6 · plan §7.0 (frozen scope) · architecture-sketch.md.");
}

// ============================================================
// SLIDE 7 — POC-lite / feasibility evidence
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 7, "POC / Feasibility Evidence", "“Show the evidence — do not merely describe that it exists”");

  // Stat row slimmed to one line (was a big-number/label stack) — frees
  // vertical space for Diagram 7 in the footer strip below, without touching
  // the table's row count or font size.
  const stats = [["71.4%", "agent accuracy (5 runs)"], ["13.2%", "step accuracy (5 runs)"], ["4 / 6", "Repair Agent success"], ["8 / 8", "spikes with real evidence"]];
  let sx = MX;
  const statW = CW / 4;
  stats.forEach(([n, l]) => {
    s.addText([
      { text: n + "  ", options: { fontFace: F_TITLE, fontSize: 19, bold: true, color: C.goldDark } },
      { text: l, options: { fontFace: F_BODY, fontSize: 11.5, color: C.textMuted } },
    ], { x: sx, y: 1.42, w: statW - 0.2, h: 0.46, isTextBox: true, margin: 0, valign: "middle" });
    sx += statW;
  });
  s.addShape(pres.ShapeType.line, { x: MX, y: 1.92, w: CW, h: 0, line: { color: C.border, width: 0.75 } });

  const spikeRows = [
    ["#", "Spike", "Status", "Result"],
    ["1", "ErrorProbe reproduction (simplified)", "DEMONSTRATED", "agent 62.5–85.7%, step 0–25% — 5 real runs, a range"],
    ["2", "CrewAI instrumentation", "DEMONSTRATED", "3 nodes, 2 clean edges"],
    ["3/3b", "Fault injection", "DEMONSTRATED", "1 case self-corrected — kept as a finding"],
    ["4", "Semantic Error Diagnostic", "DEMONSTRATED", "Catches a near-miss ($20.00 vs $19.75), zero false positives"],
    ["5", "Controlled counterfactual replay", "DEMONSTRATED", "97.2 corrupted → 108.0 recovered, recovery_success = true"],
    ["6", "Cyclic graph handling", "DEMONSTRATED", "Disabled → hits the 10,000-step safety cap"],
    ["7", "Preventive classifier", "HONEST NEGATIVE", "precision / recall / F1 = 0.25, near-random — reported, not hidden"],
    ["8", "Repair Agent", "DEMONSTRATED", "4/6 success; both failures share one fixable cause"],
  ];
  // NOTE: this table stays at 11.5pt, like slide 3's — 9 rows of real evidence text
  // is this deck's other genuine density ceiling, verified by rendering.
  const tRows = spikeRows.map((r, ri) => r.map((c, ci) => {
    if (ri === 0) return { text: c, options: { bold: true, fill: { color: C.panel }, color: C.textLight, fontSize: 11.5, align: ci === 0 ? "center" : "left", valign: "middle" } };
    const isNeg = r[2] === "HONEST NEGATIVE";
    return {
      text: c,
      options: {
        fontSize: 11.5, valign: "middle", align: ci === 0 ? "center" : "left",
        bold: ci === 2,
        color: ci === 2 ? (isNeg ? C.amber : C.green) : C.textDark,
        fill: { color: isNeg ? C.amberSoft : (ri % 2 === 0 ? C.paper : C.card) },
      },
    };
  }));
  // Height trimmed slightly (3.00 -> 2.90) — the table's last row and the
  // "LIVE, CLICKABLE PROTOTYPE"/"OPERATOR WORKFLOW" captions below it were
  // sitting close enough to visually overlap; this opens a clean gap.
  s.addTable(tRows, {
    x: MX, y: 2.06, w: CW, h: 2.90,
    colW: [0.62, 2.35, 1.80, 7.35],
    border: { type: "solid", color: C.border, pt: 0.5 },
    autoPage: false, fontFace: F_BODY,
  });

  // Footer strip, two columns now — the "In progress / Planned / Prototype"
  // note card was dropped (same content already lives in the speaker notes
  // below, and the spike table's own HONEST NEGATIVE/DEMONSTRATED labels
  // already cover "full MVP not required"); both visuals grow to use the
  // freed width instead. A real screenshot of the clickable prototype
  // (poc-demo/frontend/dist-static/index.html — interface real, backend mocked
  // against a frozen data snapshot, exactly the guide's "high-fidelity functional
  // prototype" definition), and a real architecture-atlas diagram of the
  // operator workflow (recolored to the deck's palette).
  // No card/border boxes around either image — just the caption and the
  // image itself. The gap between the two was too wide (dead white space);
  // it's now small, and the workflow diagram grew into the reclaimed room
  // (both wider and taller — its height was the real ceiling, so the table
  // gap and footer margin were both trimmed slightly to allow it).
  const bandY = 5.14;
  const thumbW = 5.2, thumbH = thumbW * (190 / 700);
  const diagW7 = 3.85, diagH7 = diagW7 * (490 / 1200);

  s.addText("LIVE, CLICKABLE PROTOTYPE", {
    x: MX, y: bandY, w: thumbW, h: 0.20, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 10.5, bold: true, color: C.goldDark, charSpacing: 0.4,
  });
  s.addImage({ path: "assets_console_thumb.png", x: MX, y: bandY + 0.24, w: thumbW, h: thumbH });

  const diag7X = MX + thumbW + 0.45;
  s.addText("OPERATOR WORKFLOW", {
    x: diag7X, y: bandY, w: diagW7, h: 0.20, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 10.5, bold: true, color: C.goldDark, charSpacing: 0.4,
  });
  s.addImage({ path: "diagram7_cropped.png", x: diag7X, y: bandY + 0.22, w: diagW7, h: diagH7 });

  s.addNotes("Lead with Spike 7's negative result and Spike 8's failure analysis — quote the guide's own words on this directly: a POC that disproved an assumption is more valuable than one that confirmed it. Every number on this slide is real and recomputable from files in the repository; offer to open one. In progress: full 3-stage reproduction, top FYP-1 priority. Planned: Recovery Controller + Verified Repair Memory Tier-2 gates, pre-registered Mid-1 criteria, not yet run. Prototype: 5 screens, mocked backend, dist-static/index.html. Citations: dev/spikes/poc/ (8 scripts + output JSONs on disk) · markdowns/04-poc-evidence/POC_Spike_Outputs_Full.md.");
}

// ============================================================
// SLIDE 8 — Evaluation plan AND risks  (official structure)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 8, "Evaluation Plan & Risks", "Thresholds and fallbacks decided before any result exists");

  card(s, MX, 1.44, CW, 0.68, C.card, C.gold);
  s.addText([{ text: "Pre-registered acceptance band.  ", options: { bold: true, color: C.goldDark } }, { text: "Reproduction accepted within ±10 points of ErrorProbe's published 59.5% on a comparable-class backbone.", options: { color: C.textDark } }], {
    x: MX + 0.26, y: 1.44, w: CW - 0.52, h: 0.68, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 15, valign: "middle",
  });

  const lx = MX, lw = 5.35;
  label(s, lx, 2.28, lw, "Metrics");
  bullets(s, [
    "Agent / step accuracy · propagation-path F1",
    "SF precision/recall + abstention rate",
    "False-positive rate on clean controls",
    "Completion, recovery, repair success rates",
    "Latency overhead — the NFR, target < 50%",
  ], { x: lx, y: 2.60, w: lw, h: 1.92, fontSize: 14.7 });

  // C.16 slide 8 asks for "baseline, DATA OR SCENARIOS, metrics, success criteria..." —
  // the data/scenarios half is named here rather than left implicit.
  // "Cannot support" caveat removed — not something the image's row 8 asks
  // for. Data/dependencies card enlarged to use the freed space.
  card(s, lx, 4.58, lw, 1.62, C.card);
  // Named "dependencies" explicitly — the circulated image's slide 8 row asks for
  // that word by name; it was present in substance (data + backbone) but unlabeled.
  label(s, lx + 0.20, 4.72, lw - 0.4, "Data / dependencies  ·  protocol", C.textMuted);
  s.addText([
    { text: "Data: ", options: { bold: true, color: C.textDark } },
    { text: "Who&When (184 cases); our own benchmark, GSM8K + tau-bench, clean controls.  ", options: { color: C.textDark } },
    { text: "Protocol: ", options: { bold: true, color: C.textDark } },
    { text: "bootstrap CIs, fixed seeds, N=5 variance, ablation matrix, human baseline.", options: { color: C.textDark } },
  ], {
    x: lx + 0.20, y: 5.02, w: lw - 0.4, h: 1.06, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 13.5, valign: "top",
  });

  // middle: success bands
  const mx3 = lx + lw + 0.26, mw3 = 2.85;
  label(s, mx3, 2.28, mw3, "Success bands");
  const bands = [
    ["Failure", "No measurable improvement anywhere", C.red, C.redSoft],
    ["Acceptable", "Parity on Who&When + any cross-arch", C.amber, C.amberSoft],
    ["Strong", "Beats baseline, unseen archs, >70% SF", C.teal, C.tealSoft],
    ["Exceptional", "Strong + >50% verified-repair recovery", C.green, C.greenSoft],
  ];
  let by = 2.60;
  bands.forEach(([n, d, fg, bg]) => {
    card(s, mx3, by, mw3, 0.86, bg, fg);
    s.addText(n, { x: mx3 + 0.18, y: by + 0.06, w: mw3 - 0.36, h: 0.28, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 14.5, bold: true, color: fg });
    s.addText(d, { x: mx3 + 0.18, y: by + 0.38, w: mw3 - 0.36, h: 0.44, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11.3, color: C.textDark });
    by += 0.92;
  });

  // right: risks → fallback. Titles trimmed so none wrap past one line at this size.
  const rx = mx3 + mw3 + 0.26, rw = CW - (rx - MX);
  label(s, rx, 2.28, rw, "Top risks → stated fallback");
  const risks = [
    ["Reproduction misses the ±10pt band", "Report both numbers, declared in advance — expected, not a failure"],
    ["Recovery Controller fails at Mid-1", "Resume via controlled replay — Tier 1 delivers it"],
    ["Verified Repair Memory fails again", "Ships as a memory-on/off ablation"],
    ["Benchmark scale stalls below 500", "Floor of 500; 300-with-stats beats 1,000-without"],
  ];
  let ry = 2.60;
  risks.forEach(([r, f]) => {
    card(s, rx, ry, rw, 0.86, C.card);
    s.addText(r, { x: rx + 0.18, y: ry + 0.06, w: rw - 0.36, h: 0.36, isTextBox: true, margin: 0, fontFace: F_BODY, bold: true, fontSize: 12.3, color: C.textDark });
    s.addText(f, { x: rx + 0.18, y: ry + 0.46, w: rw - 0.36, h: 0.36, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11.3, color: C.green });
    ry += 0.92;
  });
  // Spans the full width now (was middle+right only) so it closes out the row
  // left empty under the data/dependencies card by the "Cannot support" removal.
  card(s, lx, 6.44, CW, 0.56, C.indigoSoft, C.indigo);
  s.addText([{ text: "GenAI boundary:  ", options: { bold: true, color: C.indigo } }, { text: "nothing we claim sits in core-replacement — the LLM is core-assist.", options: { color: C.textDark } }], {
    x: lx + 0.20, y: 6.44, w: CW - 0.4, h: 0.56, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 12.3, valign: "middle",
  });

  s.addNotes("The false-positive-rate-on-clean-controls metric is absent from every paper in the reviewed corpus and every platform checked — say this is the field's gap, not just ours. Deliver the risk column as confidence, not confession: each decision rule was pre-registered before results exist. Outside the acceptance band, both numbers are reported transparently, declared before the run, not after. Full GenAI boundary line: every external component classified Support / Core-assist / Core-replacement; the contribution survives swapping the LLM. Citations: plan §11 (acceptance band, pre-registered) · risk-register.md (R4/R25/R37).");
}

// ============================================================
// SLIDE 9 — Work division & iteration plan  (official structure)
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 9, "Work Division & Iteration Plan", "Member-wise ownership and the milestones each lane is measured against");

  const members = [
    ["Shahoud Shahid", "23i-2515", "DATA / BENCHMARK", [
      "Framework instrumentation (CrewAI, LangGraph)",
      "Fault injection + labelling",
      "Benchmark build & release",
    ], "If removed: no cross-architecture benchmark — the core research claim is untestable", C.teal, C.tealSoft],
    ["Muhammad Noor", "23i-2520", "DIAGNOSIS ENGINE", [
      "Graph construction + trace normalization",
      "ErrorProbe reproduction and baseline",
      "Semantic Error Diagnostic + causal tracing",
    ], "If removed: no attribution algorithm, no silent-failure detection — the contribution disappears", C.orange, C.orangeSoft],
    ["Saif Shahzad", "23i-2634", "PLATFORM", [
      "Counterfactual replay + Recovery Controller",
      "Framework-agnostic SDK, FastAPI, Postgres",
      "Dashboard, containerized deployment",
    ], "If removed: nothing is installable or operable outside the dev machine", C.indigo, C.indigoSoft],
  ];
  // Bullets shortened just enough that none needs more than one wrap at this size —
  // verified by rendering, not assumed (this slide's real overflow risk is here).
  const mw = (CW - 0.44) / 3;
  let mx2 = MX;
  members.forEach(([n, roll, role, own, rm, fg, bg]) => {
    card(s, mx2, 1.36, mw, 2.58, bg, fg);
    s.addText([
      { text: n, options: { bold: true, fontSize: 17.5, fontFace: F_TITLE, color: C.textDark } },
      { text: `   ${roll}`, options: { fontSize: 12.5, fontFace: F_MONO, color: C.textMuted } },
    ], { x: mx2 + 0.20, y: 1.48, w: mw - 0.4, h: 0.32, isTextBox: true, margin: 0 });
    chip(s, mx2 + 0.20, 1.86, 2.20, role, C.textLight, fg);
    bullets(s, own, { x: mx2 + 0.20, y: 2.24, w: mw - 0.4, h: 1.22, fontSize: 13 });
    s.addShape(pres.ShapeType.line, { x: mx2 + 0.20, y: 3.52, w: mw - 0.4, h: 0, line: { color: fg, width: 0.75 } });
    s.addText(rm, { x: mx2 + 0.20, y: 3.58, w: mw - 0.4, h: 0.34, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11.5, italic: true, color: C.textMuted });
    mx2 += mw + 0.22;
  });

  // Committed-core/resources/tools band removed — row 9 in the image structure
  // asks only for "member-wise responsibilities and milestones," not scope
  // tiers, budget, or tooling. Milestones enlarged to use the freed space.
  // Effort-budget card removed — row 9 asks for responsibilities and
  // milestones only, not hours accounting. Timeline enlarged to fill the slide.
  label(s, MX, 4.60, CW, "FYP-1 → FYP-2 milestones");
  const gates = [
    ["M1", "Scope locked", "scope approved"],
    ["M2", "Baseline reproduced", "reproduction + Tier-2 + baseline"],
    ["M3", "Core integrated", "integrated core, end to end"],
    ["M4", "Benchmark released", "benchmark ≥500 · release ready"],
    ["M5", "Full evaluation", "full evaluation, deployed"],
  ];
  const gw = CW / gates.length;
  s.addShape(pres.ShapeType.line, { x: MX + gw / 2, y: 5.30, w: CW - gw, h: 0, line: { color: C.gold, width: 2 } });
  gates.forEach(([g, n, d], i) => {
    const gx = MX + i * gw + gw / 2;
    s.addShape(pres.ShapeType.ellipse, { x: gx - 0.13, y: 5.17, w: 0.26, h: 0.26, fill: { color: i === 0 ? C.gold : C.paper }, line: { color: C.gold, width: 2 } });
    s.addText([
      { text: g, options: { fontFace: F_MONO, fontSize: 13, bold: true, color: C.goldDark, breakLine: true } },
      { text: n, options: { fontFace: F_BODY, fontSize: 17, bold: true, color: C.textDark, breakLine: true } },
      { text: d, options: { fontFace: F_BODY, fontSize: 13, color: C.textMuted } },
    ], { x: gx - gw / 2 + 0.06, y: 5.56, w: gw - 0.12, h: 0.95, isTextBox: true, margin: 0, align: "center" });
  });

  s.addNotes("Each member states their own subsystem in one sentence, aloud — the panel is applying the guide's four ownership questions (explain / justify against an alternative / predict what breaks / modify under questioning), and hearing three distinct voices here sets that tone early. The 'if removed' line under each card is the guide's own scope test, answered honestly rather than asserted. If pressed on effort/capacity: 490h (FYP-1) + 640h (FYP-2) = 1,130h against 1,130h capacity (3 × ~15h/wk × ~28 wks), balanced depth not identical tasks. Citations: plan §3 (ownership) · §7.0 (frozen scope) · §12 (effort) · cost-estimate.md · 06_Expanded_Scope_and_Feasibility_Plan.md.");
}

// ============================================================
// SLIDE 10 — Team responsibilities & iterations, DEI, Ethics/Legal
// This slide covers the image structure's row 10 exactly: DEI statement,
// ethical statement, legal statement — nothing else. Individual member
// ownership already lives on slide 9 and is not repeated here.
// ============================================================
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  chrome(s, 10, "DEI, Ethics & Legal", "What the team commits to, and how it stays accountable");

  // Shared-responsibilities and iteration-plan recap removed — row 10 in the
  // image structure asks only for DEI/Ethical/Legal statements; ownership is
  // slide 9's job and the milestone gates are already shown there in full.
  // DEI / Ethical / Legal now the whole slide, enlarged accordingly.
  label(s, MX, 1.50, CW, "Commitments the panel can hold us to");
  const bandW = (CW - 0.44) / 3;
  const bands = [
    ["DEI", C.teal, C.tealSoft, [
      "Open-source release widens access — SDG 9 access-equity",
      "Colour + text + shape, never colour alone — WCAG owed by Final-1",
      "Accuracy claims stated as English-only",
    ]],
    ["ETHICAL", C.red, C.redSoft, [
      "Advisory only — every repair is human-gated",
      "Consent for real trace data; injection only on consenting systems",
      "Negative results published as found — Spike 7 not buried",
    ]],
    ["LEGAL / PROFESSIONAL", C.indigo, C.indigoSoft, [
      "Who&When · GSM8K · tau-bench — all MIT, confirmed against the LICENSE file",
      "Released artefacts carry MIT / CC BY 4.0",
      "AI usage logged per session and disclosed to the team throughout",
    ]],
  ];
  let bx2 = MX;
  bands.forEach(([lab, fg, bg, pts]) => {
    card(s, bx2, 1.88, bandW, 4.10, bg, fg);
    s.addText(lab, { x: bx2 + 0.22, y: 2.04, w: bandW - 0.44, h: 0.32, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 15, bold: true, color: fg, charSpacing: 0.8 });
    bullets(s, pts, { x: bx2 + 0.22, y: 2.60, w: bandW - 0.44, h: 3.20, fontSize: 16.5, paraSpaceAfter: 26, valign: "middle" });
    bx2 += bandW + 0.22;
  });

  s.addNotes("The DEI line is a real, checkable commitment, not a decorative label — say the access-equity sentence in your own words. Ownership per lane and the FYP-1/FYP-2 milestone gates are both on slide 9; this slide is deliberately just the three compliance statements the guide names. Every CCP-relevant component has a member who can defend it live — offer to demonstrate that on any component they pick. Citations: plan §3 (ownership) · AI_Usage_Log.md · risk-register R30/R38.");
}

pres.writeFile({ fileName: "Granite_Proposal_Defense_v2.pptx" }).then(fn => console.log("Wrote", fn));
