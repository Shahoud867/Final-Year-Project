// Granite — 10-Slide Proposal Defense Deck (pptx)
// Content mirrors poc-demo/frontend/public/slides/index.html 1:1 (same 10 exhibits,
// same numbers, same tables). Same Granite palette as generate_proposal_deck.js /
// generate_3slide_deck.js. Native PowerPoint slide transitions + entrance animations
// are injected as a post-process (see inject_animations.js) since pptxgenjs has no
// animation/transition API.
const pptxgen = require("pptxgenjs");

const C = {
  bgDark: "0E1119", panel: "171B28", panelAlt: "1E2333", line: "2B3145",
  textLight: "EEF1F8", textMuted: "9AA3BA", textFaint: "6B7390",
  accent: "D9A15C", accentBright: "F0C084", accentDark: "8A5F22",
  green: "57C98F", greenSoft: "1C3327", amber: "E0B555", amberSoft: "352A14",
  red: "E37070", redSoft: "3A1E1E", teal: "4FB3C4", tealSoft: "17282B",
  orange: "E08A55", blue: "6EA8E0",
};
const F_TITLE = "Cambria", F_BODY = "Calibri", F_MONO = "Consolas";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Granite — F26-060";
pres.company = "FAST School of Computing, NUCES";
pres.title = "Granite — Proposal Defense";

const PW = 13.333, PH = 7.5, MX = 0.55, CW = PW - MX * 2;

function bgSlide(s) { s.background = { color: C.bgDark }; }
function chrome(s, num, kicker, tag, title, sub) {
  s.addText(kicker.toUpperCase(), { x: MX, y: 0.3, w: CW * 0.5, h: 0.24, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 11, bold: true, color: C.accentBright, charSpacing: 2 });
  s.addText(tag, { x: MX + CW * 0.5, y: 0.3, w: CW * 0.5, h: 0.24, isTextBox: true, margin: 0, align: "right", fontFace: F_MONO, fontSize: 9.5, color: C.textFaint, charSpacing: 1 });
  s.addText(title, { x: MX, y: 0.56, w: CW, h: sub ? 0.7 : 0.7, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 27, bold: true, color: C.textLight });
  let topY = 1.34;
  if (sub) {
    s.addText(sub, { x: MX, y: 1.28, w: CW, h: 0.5, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11, color: C.textMuted, lineSpacing: 14 });
    topY = 1.78;
  }
  s.addShape(pres.ShapeType.rect, { x: MX, y: topY - 0.1, w: 0.55, h: 0.03, fill: { color: C.accent } });
  s.addText(`Granite  ·  F26-060  ·  ${num}/10`, { x: PW - 2.2, y: PH - 0.4, w: 1.9, h: 0.28, isTextBox: true, margin: 0, align: "right", fontFace: F_MONO, fontSize: 8.5, color: C.textFaint });
  return topY;
}
function card(s, x, y, w, h, accentColor) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.06, fill: { color: C.panel }, line: { color: C.line, width: 0.75 } });
  s.addShape(pres.ShapeType.rect, { x, y: y + 0.1, w: 0.035, h: h - 0.2, fill: { color: accentColor } });
}
function cardHeader(s, x, y, w, label) {
  s.addText(label.toUpperCase(), { x: x + 0.18, y: y + 0.1, w: w - 0.3, h: 0.22, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9, bold: true, color: C.textFaint, charSpacing: 1 });
}
function pill(s, x, y, text, color, soft) {
  const w = 0.2 + text.length * 0.075;
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.24, rectRadius: 0.12, fill: { color: soft }, line: { color, width: 0.75 } });
  s.addText(text, { x, y: y - 0.005, w, h: 0.24, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F_MONO, fontSize: 8, bold: true, color });
  return w;
}
function table(s, rows, x, y, w, h, colW, opts = {}) {
  s.addTable(rows.map((r, ri) => r.map((c) => (
    typeof c === "string" ? { text: c, options: { fontSize: opts.fontSize || 9, fontFace: F_BODY, color: ri === 0 ? C.textFaint : C.textMuted, bold: ri === 0, fill: { color: ri === 0 ? C.panelAlt : C.panel } } } : c
  ))), { x, y, w, h, border: { type: "solid", color: C.line, pt: 0.5 }, colW, autoPage: false });
}

// ============================================================
// SLIDE 1 — Title & Problem
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, 1, "EXHIBIT 01", "TITLE & PROBLEM",
    "Granite — A Self-Healing Multi-Agent System\nfor Semantic Error Diagnosis, Verified Repair & Recovery", null);
  const heroH = 1.5;
  card(s, MX, topY, CW, heroH, C.accent);
  cardHeader(s, MX, topY, CW, "One-line problem");
  s.addText("“When a multi-agent AI system fails — including when the wrong answer looks completely right — no published method can reliably say which agent caused it, and none can verify a fix before trusting it.”", {
    x: MX + 0.25, y: topY + 0.4, w: CW - 0.5, h: heroH - 0.5, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 15, italic: true, color: C.textLight, valign: "middle", lineSpacing: 20,
  });
  const rowY = topY + heroH + 0.2, colW = (CW - 0.48) / 4, rowH = PH - rowY - 0.5;
  const cards4 = [
    ["Project", "F26-060-Granite", "Stream A — Research-derived", C.teal],
    ["Supervisor", "Dr. Adil Majeed", "", C.orange],
    ["Team", "Shahoud Shahid", "Muhammad Noor\nSaif Shahzad", C.blue],
    ["SDG", "9.5", "Industry, Innovation &\nInfrastructure", C.green],
  ];
  cards4.forEach((c, i) => {
    const x = MX + i * (colW + 0.16);
    card(s, x, rowY, colW, rowH, c[3]);
    cardHeader(s, x, rowY, colW, c[0]);
    s.addText(c[1], { x: x + 0.2, y: rowY + 0.4, w: colW - 0.4, h: 0.4, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 15, bold: true, color: C.textLight });
    if (c[2]) s.addText(c[2], { x: x + 0.2, y: rowY + 0.85, w: colW - 0.4, h: rowH - 1, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10, color: C.textMuted, lineSpacing: 14 });
  });
}

// ============================================================
// SLIDE 2 — Stakeholders & Workflow
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, 2, "EXHIBIT 02", "STAKEHOLDERS & WORKFLOW",
    "Who Has This Problem — And Where It Breaks",
    "Primary: engineering teams running multi-agent systems near production (tau-bench retail). Auditors and downstream product teams depend on the diagnosis output.");
  let px = MX;
  const stepH = 0.34;
  ["Capture trace", "Human reads", "Guesses root cause"].forEach((st, i) => {
    const w = 0.4 + st.length * 0.085;
    s.addShape(pres.ShapeType.roundRect, { x: px, y: topY, w, h: stepH, rectRadius: 0.05, fill: { color: C.panelAlt }, line: { color: C.line, width: 0.5 } });
    s.addText(st, { x: px, y: topY, w, h: stepH, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F_MONO, fontSize: 9, color: C.textMuted });
    px += w + 0.16;
    if (i < 2) { s.addText("→", { x: px - 0.14, y: topY, w: 0.22, h: stepH, isTextBox: true, margin: 0, align: "center", valign: "middle", fontSize: 11, color: C.textFaint }); px += 0.08; }
  });
  pill(s, px + 0.1, topY + 0.02, "unmeasured", C.red, C.redSoft);

  const rowY = topY + stepH + 0.22, leftW = CW * 0.58, rightW = CW - leftW - 0.16, rowH = PH - rowY - 0.5;
  card(s, MX, rowY, leftW, rowH, C.red);
  cardHeader(s, MX, rowY, leftW, "Where it fails today");
  s.addText([
    { text: "No automated attribution with published accuracy. No systematic check for ", options: { color: C.textMuted } },
    { text: "silent failures", options: { bold: true, color: C.textLight } },
    { text: " — a confident, well-formed, wrong answer with no error signal. No way to test a fix before redeploying.\n\n", options: { color: C.textMuted } },
    { text: "Consequence: ", options: { bold: true, color: C.accentBright } },
    { text: "a missed silent failure ships an incorrect answer to an end user, undetected.", options: { color: C.accentBright } },
  ], { x: MX + 0.2, y: rowY + 0.4, w: leftW - 0.4, h: rowH - 0.55, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11.5, lineSpacing: 17, valign: "top" });

  card(s, MX + leftW + 0.16, rowY, rightW, rowH, C.accent);
  cardHeader(s, MX + leftW + 0.16, rowY, rightW, "Field baseline");
  s.addText("14.2%", { x: MX + leftW + 0.36, y: rowY + 0.4, w: rightW - 0.4, h: 0.55, isTextBox: true, margin: 0, fontFace: F_TITLE, fontSize: 34, bold: true, color: C.textLight });
  s.addText("step accuracy (Who&When) — “just reading the trace.” The number this project has to beat.", { x: MX + leftW + 0.36, y: rowY + 1.0, w: rightW - 0.5, h: rowH - 1.15, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10, color: C.textMuted, lineSpacing: 14 });
}

// ============================================================
// SLIDE 3 — Existing Solutions & Gap
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, 3, "EXHIBIT 03", "EXISTING SOLUTIONS & GAP", "The Gap Is Structural, Not a Missing Feature", null);
  const rows = [
    ["Approach", "Attribution", "Silent-failure", "Fix-verify", "Framework-agnostic"],
    ["ErrorProbe (ACL 26)", "59.5%", "admits it cannot", "—", "2 arch. only"],
    ["LangSmith / Arize (26)", "unpublished", "unconfirmed", "—", "stack-locked"],
    ["Langfuse / Braintrust / etc.", "human-driven", "RAG-groundedness only", "—", "—"],
    ["Manual workflow (today)", "14.2%", "—", "—", "N/A"],
    ["Granite (proposed)", "building on 59.5%", "scoped + measured", "recovery rate, N replays", "CrewAI+LangGraph, unseen"],
  ];
  const tH = 2.6;
  s.addTable(rows.map((r, ri) => r.map((c) => ({
    text: c, options: {
      fontSize: 10, fontFace: F_BODY, bold: ri === 0 || ri === 5,
      color: ri === 0 ? C.textFaint : (ri === 5 ? C.green : C.textMuted),
      fill: { color: ri === 0 ? C.panelAlt : (ri === 5 ? C.greenSoft : C.panel) },
    },
  }))), { x: MX, y: topY, w: CW, h: tH, border: { type: "solid", color: C.line, pt: 0.5 }, colW: [CW * 0.24, CW * 0.19, CW * 0.2, CW * 0.19, CW * 0.18], autoPage: false });

  const cardY = topY + tH + 0.2, cardH = PH - cardY - 0.5;
  card(s, MX, cardY, CW, cardH, C.accent);
  cardHeader(s, MX, cardY, CW, "Real gap");
  s.addText([
    { text: "No system checked confirms attribution ", options: { color: C.textMuted } },
    { text: "+ ", options: { bold: true, color: C.accentBright } },
    { text: "silent-failure detection ", options: { bold: true, color: C.textLight } },
    { text: "+ ", options: { bold: true, color: C.accentBright } },
    { text: "counterfactual verification ", options: { bold: true, color: C.textLight } },
    { text: "+ ", options: { bold: true, color: C.accentBright } },
    { text: "cross-architecture generalization", options: { bold: true, color: C.textLight } },
    { text: ", evaluated as one pipeline.", options: { color: C.textMuted } },
  ], { x: MX + 0.22, y: cardY + 0.36, w: CW - 0.44, h: cardH - 0.5, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 12.5, lineSpacing: 18, valign: "middle" });
}

// ============================================================
// SLIDE 4 — Research & Technical Basis
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, 4, "EXHIBIT 04", "RESEARCH & TECHNICAL BASIS", "Read For Decisions, Not Decoration", null);
  const leftW = CW * 0.46, rightW = CW - leftW - 0.16, rowH = PH - topY - 0.5;
  card(s, MX, topY, leftW, rowH, C.accent);
  cardHeader(s, MX, topY, leftW, "Research lineage");
  const bars = [["Who&When\nICML 25", "14.2%", 0.22], ["AgenTracer\nICLR 26", "—", 0.34], ["ErrorProbe\nACL 26", "59.5%", 1.0]];
  const barAreaY = topY + 0.5, barAreaH = rowH - 1.5, barW = 0.7, gap = leftW / bars.length - barW - 0.1;
  let bx = MX + (leftW - (bars.length * barW + (bars.length - 1) * gap)) / 2;
  bars.forEach((b) => {
    const h = barAreaH * b[2];
    s.addShape(pres.ShapeType.roundRect, { x: bx, y: barAreaY + (barAreaH - h), w: barW, h, rectRadius: 0.04, fill: { color: C.accent } });
    s.addText(b[1], { x: bx - 0.2, y: barAreaY + (barAreaH - h) - 0.3, w: barW + 0.4, h: 0.26, isTextBox: true, margin: 0, align: "center", fontFace: F_MONO, fontSize: 11, bold: true, color: C.accentBright });
    s.addText(b[0], { x: bx - 0.25, y: barAreaY + barAreaH + 0.08, w: barW + 0.5, h: 0.5, isTextBox: true, margin: 0, align: "center", fontFace: F_MONO, fontSize: 9, color: C.textFaint });
    bx += barW + gap;
  });
  card(s, MX + leftW + 0.16, topY, rightW, rowH, C.teal);
  cardHeader(s, MX + leftW + 0.16, topY, rightW, "Decisions, not defaults");
  s.addText([
    { text: "ErrorProbe chosen as baseline on ", options: { color: C.textMuted } }, { text: "performance, not recency", options: { bold: true, color: C.textLight } }, { text: ".\n\n", options: {} },
    { text: "CrewAI + LangGraph committed — used by ", options: { color: C.textMuted } }, { text: "none", options: { bold: true, color: C.textLight } }, { text: " of the 9 papers reviewed: the actual generalization test.\n\n", options: { color: C.textMuted } },
    { text: "Constraint-based SED chosen — LLM judges score ≤0.65 AUROC on this task.\n\n", options: { color: C.textMuted } },
    { text: "Single-framework scope-narrowing explicitly ", options: { color: C.textMuted } }, { text: "rejected", options: { bold: true, color: C.red } }, { text: " (R19).", options: { color: C.textMuted } },
  ], { x: MX + leftW + 0.36, y: topY + 0.4, w: rightW - 0.4, h: rowH - 0.55, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11, lineSpacing: 17 });
}

// ============================================================
// SLIDE 5 — Complex Computing / CCP
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, 5, "EXHIBIT 05", "COMPLEX COMPUTING / CCP", "8 of 9 Seoul Accord Characteristics — Clear", null);
  const rows = [
    ["Conflicting requirements", "ok", "Diagnostic depth vs. latency; trace completeness vs. privacy"],
    ["No obvious solution", "ok", "Best published step accuracy still 59.5% after 7 papers"],
    ["Depth of knowledge", "ok", "Execution-graph modeling, causal/counterfactual reasoning"],
    ["Unfamiliar issues", "ok", "Delayed error manifestation, LLM non-determinism"],
    ["Beyond standard practice", "ok", "No off-the-shelf equivalent solves this combination"],
    ["Diverse stakeholders", "weak", "Operators, product teams, auditors named — contact pending"],
    ["Significant consequences", "ok", "A missed silent failure ships a wrong answer, undetected"],
    ["Interdependence", "ok", "The execution graph models exactly this"],
    ["Ill-defined cause", "ok", "3 unknowns: did it fail, which agent/step, correct behavior"],
  ];
  const rowH = (PH - topY - 0.5) / rows.length;
  rows.forEach((r, i) => {
    const y = topY + i * rowH;
    const isOk = r[1] === "ok";
    s.addShape(pres.ShapeType.ellipse, { x: MX, y: y + rowH / 2 - 0.13, w: 0.26, h: 0.26, fill: { color: isOk ? C.greenSoft : C.amberSoft }, line: { color: isOk ? C.green : C.amber, width: 1 } });
    s.addText(isOk ? "✓" : "!", { x: MX, y: y + rowH / 2 - 0.14, w: 0.26, h: 0.26, isTextBox: true, margin: 0, align: "center", valign: "middle", fontSize: 10, bold: true, color: isOk ? C.green : C.amber });
    s.addText([{ text: `${i + 1}. ${r[0]}`, options: { bold: true, color: C.textLight } }, { text: `  —  ${r[2]}`, options: { color: C.textMuted } }], {
      x: MX + 0.38, y: y + rowH / 2 - 0.18, w: CW - 0.5, h: 0.36, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11, valign: "middle",
    });
  });
}

// ============================================================
// SLIDE 6 — Proposed Solution
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, 6, "EXHIBIT 06", "PROPOSED SOLUTION", "What Is Actually Being Built", null);
  const c1H = 1.55;
  card(s, MX, topY, CW, c1H, C.accent);
  cardHeader(s, MX, topY, CW, "Contribution");
  s.addText("Existing methods reach up to 59.5% step accuracy but remain weak under two conditions: none is evaluated on an architecture absent from its own benchmark construction, and the strongest method admits it cannot catch silent failures. We are building a cross-architecture fault-injection benchmark and a diagnosis pipeline with constraint-based silent-failure verification, packaged as a framework-agnostic testing SDK.", {
    x: MX + 0.2, y: topY + 0.36, w: CW - 0.4, h: c1H - 0.5, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.5, color: C.textMuted, lineSpacing: 15,
  });
  const c2Y = topY + c1H + 0.16, c2H = 0.85;
  card(s, MX, c2Y, CW, c2H, C.blue);
  cardHeader(s, MX, c2Y, CW, "Pipeline");
  let px = MX + 0.2;
  const steps = ["trace", "execution graph", "Semantic Error Diagnostic", "causal trace", "Repair Agent", "verified replay", "confidence-gated rec."];
  const availW = CW - 0.4;
  const totalTextW = steps.reduce((a, s2) => a + 0.3 + s2.length * 0.072, 0);
  const arrowW = 0.22, totalArrows = (steps.length - 1) * arrowW;
  const scale = Math.min(1, (availW - totalArrows) / totalTextW);
  steps.forEach((st, i) => {
    const w = (0.3 + st.length * 0.072) * scale;
    s.addShape(pres.ShapeType.roundRect, { x: px, y: c2Y + 0.42, w, h: 0.3, rectRadius: 0.05, fill: { color: C.panelAlt }, line: { color: C.line, width: 0.5 } });
    s.addText(st, { x: px, y: c2Y + 0.42, w, h: 0.3, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F_MONO, fontSize: 7.5, color: C.textMuted });
    px += w;
    if (i < steps.length - 1) { s.addText("→", { x: px, y: c2Y + 0.42, w: arrowW, h: 0.3, isTextBox: true, margin: 0, align: "center", valign: "middle", fontSize: 9, color: C.textFaint }); px += arrowW; }
  });
  const c3Y = c2Y + c2H + 0.16, c3H = PH - c3Y - 0.5, c3W = (CW - 0.16) / 2;
  card(s, MX, c3Y, c3W, c3H, C.green);
  cardHeader(s, MX, c3Y, c3W, "In scope");
  s.addText("The 10 committed mechanisms (Tier 1 unconditional + Tier 2 gated). Deployment: single Docker container.", { x: MX + 0.2, y: c3Y + 0.36, w: c3W - 0.4, h: c3H - 0.5, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.5, color: C.textMuted, lineSpacing: 15 });
  card(s, MX + c3W + 0.16, c3Y, c3W, c3H, C.red);
  cardHeader(s, MX + c3W + 0.16, c3Y, c3W, "Out of scope");
  s.addText("Message queues, Kubernetes/multi-region, full RBAC, disaster-recovery infra, multi-tenant billing.", { x: MX + c3W + 0.36, y: c3Y + 0.36, w: c3W - 0.4, h: c3H - 0.5, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.5, color: C.textMuted, lineSpacing: 15 });
}

// ============================================================
// SLIDE 7 — POC / Feasibility Evidence
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, 7, "EXHIBIT 07", "POC / FEASIBILITY EVIDENCE", "8 Real Spikes — Including Two Honest Negatives", null);
  const c1H = 1.85;
  card(s, MX, topY, CW, c1H, C.accent);
  cardHeader(s, MX, topY, CW, "Live exhibit — one real diagnosis run (recovered state)");
  const nodes = [["PriceExtractor", "price = 100.00"], ["TaxCalculator", "total = 108.00"], ["Verifier", "pass = true"]];
  const nw = 1.9, nh = 0.85, gapN = 0.5;
  const nx0 = MX + (CW - (nw * 3 + gapN * 2)) / 2, ny = topY + 0.45;
  nodes.forEach((n, i) => {
    const x = nx0 + i * (nw + gapN);
    s.addShape(pres.ShapeType.roundRect, { x, y: ny, w: nw, h: nh, rectRadius: 0.07, fill: { color: C.panelAlt }, line: { color: C.green, width: 1.5 } });
    s.addText(n[0], { x, y: ny + 0.15, w: nw, h: 0.3, isTextBox: true, margin: 0, align: "center", fontFace: F_BODY, fontSize: 11.5, bold: true, color: C.textLight });
    s.addText(n[1], { x, y: ny + 0.48, w: nw, h: 0.3, isTextBox: true, margin: 0, align: "center", fontFace: F_MONO, fontSize: 10.5, color: C.accentBright });
    if (i < 2) s.addText("→", { x: x + nw + gapN / 2 - 0.12, y: ny + 0.25, w: 0.24, h: 0.35, isTextBox: true, margin: 0, align: "center", fontSize: 14, color: C.green });
  });
  s.addText("Fault injected: PriceExtractor silently corrupted $100.00 → $90.00 → wrong total $97.20. SED flags the mismatch → causal trace localizes PriceExtractor → Repair Agent proposes $100.00 → replayed: 97.20 → 108.00, recovery_success = true.", {
    x: MX + 0.25, y: ny + nh + 0.12, w: CW - 0.5, h: c1H - (ny + nh - topY) - 0.15, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.5, color: C.textMuted, align: "center", lineSpacing: 13,
  });
  const tY = topY + c1H + 0.16, tH = PH - tY - 0.5;
  const spikes = [
    ["Spike", "Status", "Result"],
    ["1 · ErrorProbe repro", "demonstrated", "agent 71.4% mean · step 13.2% mean (5 runs)"],
    ["2 · CrewAI instrumentation", "demonstrated", "clean 3-node, 2-edge trace"],
    ["3/3b · Fault injection", "demonstrated", "ground truth unambiguous; one self-correction kept"],
    ["4 · Semantic Error Diagnostic", "demonstrated", "$20.00 vs $19.75 near-miss caught, zero false positives"],
    ["5 · Counterfactual replay", "demonstrated", "97.2 → 108.0 recovered, recovery_success = true"],
    ["6 · Cyclic graph handling", "demonstrated", "bound proven load-bearing vs. 10,000-step cap"],
    ["7 · Preventive classifier", "honest negative", "P/R/F1 = 0.25, near-random — reported, not hidden"],
    ["8 · Repair Agent", "demonstrated", "repair_success_rate 4/6 (0.667)"],
  ];
  const statusColor = (t) => (t === "demonstrated" ? C.green : t === "honest negative" ? C.amber : C.textMuted);
  s.addTable(spikes.map((r, ri) => r.map((c, ci) => ({
    text: c, options: { fontSize: ri === 0 ? 8.5 : 9, fontFace: ci === 1 && ri > 0 ? F_MONO : F_BODY, bold: ri === 0, color: ri === 0 ? C.textFaint : (ci === 1 ? statusColor(c) : C.textMuted), fill: { color: ri === 0 ? C.panelAlt : C.panel } },
  }))), { x: MX, y: tY, w: CW, h: tH, border: { type: "solid", color: C.line, pt: 0.5 }, colW: [CW * 0.24, CW * 0.18, CW * 0.58], autoPage: false });
}

// ============================================================
// SLIDE 8 — Evaluation Plan
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, 8, "EXHIBIT 08", "EVALUATION PLAN", "Success, Defined Before The Data Exists", null);
  const leftW = CW * 0.58, rightW = CW - leftW - 0.16, rowH = PH - topY - 0.5;
  card(s, MX, topY, leftW, rowH, C.blue);
  cardHeader(s, MX, topY, leftW, "Baseline, data & metrics");
  s.addText([
    { text: "Baseline: ", options: { bold: true, color: C.textLight } }, { text: "ErrorProbe reproduced — pre-registered ±10pt band around 59.5%.\n\n", options: { color: C.textMuted } },
    { text: "Data: ", options: { bold: true, color: C.textLight } }, { text: "Who&When (184) + new benchmark, floor 500 / stretch 1,000, 15–20% clean controls.\n\n", options: { color: C.textMuted } },
    { text: "Metrics: ", options: { bold: true, color: C.textLight } }, { text: "accuracy · propagation F1 · silent-fail P/R+coverage · FP rate on clean controls · recovery rate · false repair rate · latency overhead (<50%)", options: { color: C.textMuted } },
  ], { x: MX + 0.2, y: topY + 0.4, w: leftW - 0.4, h: rowH - 0.55, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 11.5, lineSpacing: 17 });

  card(s, MX + leftW + 0.16, topY, rightW, rowH, C.amber);
  cardHeader(s, MX + leftW + 0.16, topY, rightW, "Success bands");
  const bands = [["failure", C.red], ["acceptable", C.textFaint], ["strong", C.teal], ["exceptional", C.green]];
  let by = topY + 0.42;
  bands.forEach((b) => {
    s.addShape(pres.ShapeType.roundRect, { x: MX + leftW + 0.36, y: by, w: rightW - 0.7, h: 0.4, rectRadius: 0.06, line: { color: b[1], width: 1.25 } });
    s.addText(b[0], { x: MX + leftW + 0.36, y: by, w: rightW - 0.7, h: 0.4, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F_MONO, fontSize: 10, bold: true, color: b[1] });
    by += 0.52;
  });
  s.addText("FP-rate-on-clean-controls appears in zero reviewed papers or platforms.", { x: MX + leftW + 0.36, y: by + 0.05, w: rightW - 0.7, h: rowH - (by - topY) - 0.15, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.5, italic: true, color: C.textFaint, lineSpacing: 13 });
}

// ============================================================
// SLIDE 9 — Scope, Risk & $0 Resourcing
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, 9, "EXHIBIT 09", "SCOPE, RISK & $0 RESOURCING", "Every Risk Has A Recorded Fallback", null);
  const leftW = CW * 0.42, rightW = CW - leftW - 0.16, rowH = PH - topY - 0.5;
  card(s, MX, topY, leftW, rowH, C.amber);
  cardHeader(s, MX, topY, leftW, "Core & resourcing");
  const p1x = MX + 0.2, p1y = topY + 0.42;
  let pw = pill(s, p1x, p1y, "Tier 1 · 8", C.green, C.greenSoft);
  pill(s, p1x + pw + 0.12, p1y, "Tier 2 · 2", C.amber, C.amberSoft);
  s.addText("each Tier-1 item has a real spike. Tier 2 gated — Recovery Controller (no PoC yet), Verified Repair Memory (failed its one test, stated honestly).", {
    x: MX + 0.2, y: p1y + 0.32, w: leftW - 0.4, h: 1.1, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.5, color: C.textMuted, lineSpacing: 15,
  });
  s.addText([{ text: "Resources: ", options: { bold: true, color: C.textLight } }, { text: "$0", options: { bold: true, color: C.accentBright, fontSize: 15 } }, { text: " — local Ollama, full project. Paid alt priced (≈$353–$881) and rejected.", options: { color: C.textMuted } }], {
    x: MX + 0.2, y: p1y + 1.5, w: leftW - 0.4, h: rowH - (p1y - topY) - 1.6, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.5, lineSpacing: 15,
  });

  card(s, MX + leftW + 0.16, topY, rightW, rowH, C.red);
  cardHeader(s, MX + leftW + 0.16, topY, rightW, "Top risks + fallback");
  const riskRows = [
    ["Risk", "Fallback"],
    ["Miss the ±10pt band", "Transparent dual-reporting"],
    ["Recovery Controller gate fails", "Resume via replay — Tier 1 delivers it"],
    ["Repair Memory fails again", "Ships as memory on/off ablation"],
    ["LLM API down at runtime", "Documented degraded state, not a crash"],
  ];
  s.addTable(riskRows.map((r, ri) => r.map((c) => ({ text: c, options: { fontSize: 10, fontFace: F_BODY, color: ri === 0 ? C.textFaint : C.textMuted, bold: ri === 0, fill: { color: ri === 0 ? C.panelAlt : C.panel } } }))), {
    x: MX + leftW + 0.36, y: topY + 0.4, w: rightW - 0.4, h: rowH - 0.55, border: { type: "solid", color: C.line, pt: 0.5 }, colW: [(rightW - 0.4) * 0.42, (rightW - 0.4) * 0.58], autoPage: false,
  });
}

// ============================================================
// SLIDE 10 — Team, Timeline & DEI
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, 10, "EXHIBIT 10", "TEAM, TIMELINE & DEI", "People, Ownership & The Compliance Lines", null);
  const c1H = 2.5;
  card(s, MX, topY, CW, c1H, C.green);
  cardHeader(s, MX, topY, CW, "Team");
  const team = [
    ["Shahoud — Data/Benchmark", "If removed: no cross-architecture benchmark exists.", C.teal, "S"],
    ["Noor — Diagnosis Engine", "If removed: no attribution algorithm, no SED.", C.orange, "N"],
    ["Saif — Platform", "If removed: nothing installs outside the dev machine.", C.blue, "F"],
  ];
  team.forEach((t, i) => {
    const y = topY + 0.42 + i * 0.68;
    s.addShape(pres.ShapeType.roundRect, { x: MX + 0.22, y, w: 0.4, h: 0.4, rectRadius: 0.08, fill: { color: t[2] } });
    s.addText(t[3], { x: MX + 0.22, y, w: 0.4, h: 0.4, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F_TITLE, fontSize: 15, bold: true, color: C.bgDark });
    s.addText(t[0], { x: MX + 0.75, y: y - 0.02, w: CW - 1, h: 0.28, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 12, bold: true, color: C.textLight });
    s.addText(t[1], { x: MX + 0.75, y: y + 0.25, w: CW - 1, h: 0.32, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.5, italic: true, color: C.textMuted });
  });

  const c2Y = topY + c1H + 0.16, c2H = PH - c2Y - 0.5;
  card(s, MX, c2Y, CW, c2H, C.accent);
  cardHeader(s, MX, c2Y, CW, "Effort budget — 1,130h capacity");
  const barY = c2Y + 0.45, barW = CW - 0.4, barH = 0.34;
  const w1 = barW * (490 / 1130), w2 = barW * (640 / 1130);
  s.addShape(pres.ShapeType.rect, { x: MX + 0.2, y: barY, w: w1, h: barH, fill: { color: C.teal } });
  s.addShape(pres.ShapeType.rect, { x: MX + 0.2 + w1, y: barY, w: w2, h: barH, fill: { color: C.orange } });
  s.addText("FYP-1 · 490h", { x: MX + 0.2, y: barY + barH + 0.06, w: w1, h: 0.22, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 9, color: C.textFaint });
  s.addText("FYP-2 · 640h", { x: MX + 0.2 + w1, y: barY + barH + 0.06, w: w2, h: 0.22, isTextBox: true, margin: 0, align: "right", fontFace: F_MONO, fontSize: 9, color: C.textFaint });
  s.addText("DEI: MIT/CC BY 4.0 release; color paired with text (WCAG owed Final-1). Ethics: advisory-only, human-gated fixes, informed consent for real trace data.", {
    x: MX + 0.2, y: barY + barH + 0.4, w: barW, h: c2H - (barY + barH - c2Y) - 0.5, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10, color: C.textMuted, lineSpacing: 14,
  });
}

const OUT = process.argv[2] || "Granite_Proposal_Defense_10Slide.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("Wrote " + OUT));
