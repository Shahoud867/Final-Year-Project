// Granite — 3-Slide Condensed Proposal Defense Deck
// Mirrors the 3-act "Exhibit I/II/III" structure of the animated HTML deck,
// compressed from the full 10-slide Proposal_Defense_Slide_Content_Spec.md.
// Same palette convention as generate_proposal_deck.js (graphite + gold).
const pptxgen = require("pptxgenjs");

const C = {
  bgDark: "0E1119",
  panel: "171B28",
  panelAlt: "1E2333",
  line: "2B3145",
  textLight: "EEF1F8",
  textMuted: "9AA3BA",
  textFaint: "6B7390",
  accent: "D9A15C",
  accentBright: "F0C084",
  accentDark: "8A5F22",
  green: "57C98F",
  greenSoft: "1C3327",
  amber: "E0B555",
  amberSoft: "352A14",
  red: "E37070",
  redSoft: "3A1E1E",
  teal: "4FB3C4",
  tealSoft: "17282B",
  orange: "E08A55",
  blue: "6EA8E0",
};
const F_TITLE = "Cambria";
const F_BODY = "Calibri";
const F_MONO = "Consolas";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "Granite — F26-060";
pres.company = "FAST School of Computing, NUCES";
pres.title = "Granite — Proposal Defense (3-Slide)";

const PW = 13.333, PH = 7.5;
const MX = 0.55;
const CW = PW - MX * 2;

function bgSlide(slide) {
  slide.background = { color: C.bgDark };
}
function chrome(slide, num, title, kicker, sub) {
  slide.addText(kicker.toUpperCase(), {
    x: MX, y: 0.3, w: CW * 0.7, h: 0.26, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 11, bold: true, color: C.accentBright, charSpacing: 2,
  });
  slide.addText(`EXHIBIT ${num} / III`, {
    x: MX, y: 0.3, w: CW * 0.3, h: 0.26, isTextBox: true, margin: 0, align: "right",
    fontFace: F_MONO, fontSize: 10, color: C.textFaint, charSpacing: 1,
  });
  slide.addText(title, {
    x: MX, y: 0.56, w: CW, h: 0.6, isTextBox: true, margin: 0,
    fontFace: F_TITLE, fontSize: 30, bold: true, color: C.textLight,
  });
  if (sub) {
    slide.addText(sub, {
      x: MX, y: 1.16, w: CW, h: 0.42, isTextBox: true, margin: 0,
      fontFace: F_BODY, fontSize: 11.5, color: C.textMuted, italic: false,
    });
  }
  slide.addShape(pres.ShapeType.rect, { x: MX, y: sub ? 1.58 : 1.28, w: 0.55, h: 0.03, fill: { color: C.accent } });
  slide.addText(`Granite  ·  F26-060  ·  ${num}/3`, {
    x: PW - 2.2, y: PH - 0.42, w: 1.9, h: 0.3, isTextBox: true, margin: 0, align: "right",
    fontFace: F_MONO, fontSize: 8.5, color: C.textFaint,
  });
  return sub ? 1.86 : 1.56; // returns top Y for body content
}
function card(slide, x, y, w, h, accentColor) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.06,
    fill: { color: C.panel }, line: { color: C.line, width: 0.75 },
  });
  slide.addShape(pres.ShapeType.rect, { x, y: y + 0.1, w: 0.035, h: h - 0.2, fill: { color: accentColor } });
}
function cardHeader(slide, x, y, w, label) {
  slide.addText(label.toUpperCase(), {
    x: x + 0.18, y: y + 0.1, w: w - 0.3, h: 0.24, isTextBox: true, margin: 0,
    fontFace: F_MONO, fontSize: 9, bold: true, color: C.textFaint, charSpacing: 1,
  });
}
function pill(slide, x, y, text, color, soft) {
  const w = 0.16 + text.length * 0.072;
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h: 0.22, rectRadius: 0.11,
    fill: { color: soft }, line: { color, width: 0.75 },
  });
  slide.addText(text, {
    x, y: y - 0.01, w, h: 0.22, isTextBox: true, margin: 0, align: "center", valign: "middle",
    fontFace: F_MONO, fontSize: 8, bold: true, color,
  });
  return w;
}

// ============================================================
// SLIDE 1 — EXHIBIT I: THE FAILURE
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, "I", "The Failure Nobody Can Name",
    "Problem · Stakeholders · Gap · Lineage",
    "A confident, well-formed, wrong answer — and no published method can reliably say which agent caused it, or verify a fix before it ships.");

  // Problem statement + team card row
  const heroH = 1.05;
  card(s, MX, topY, CW * 0.6 - 0.1, heroH, C.accent);
  s.addText([
    { text: "“", options: { color: C.accent, fontSize: 20, bold: true } },
    { text: "When a multi-agent AI system fails — including when the wrong answer looks completely right — no published method can reliably say which agent caused it, and none can verify a fix before trusting it.”", options: { italic: true, color: C.textLight } },
  ], { x: MX + 0.22, y: topY + 0.12, w: CW * 0.6 - 0.5, h: heroH - 0.24, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 12, valign: "middle" });

  card(s, MX + CW * 0.6, topY, CW * 0.4, heroH, C.teal);
  const team = [["Shahoud Shahid", "23i-2515 · Data/Benchmark"], ["Muhammad Noor", "23i-2520 · Diagnosis Engine"], ["Saif Shahzad", "23i-2634 · Platform"]];
  team.forEach((t, i) => {
    s.addText(t[0], { x: MX + CW * 0.6 + 0.2, y: topY + 0.08 + i * 0.32, w: 2.2, h: 0.26, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10.5, bold: true, color: C.textLight });
    s.addText(t[1], { x: MX + CW * 0.6 + 2.3, y: topY + 0.08 + i * 0.32, w: 2.6, h: 0.26, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 8.5, color: C.textFaint, align: "right" });
  });

  const rowY = topY + heroH + 0.16;
  const colW = (CW - 0.32) / 3;
  const rowH = PH - rowY - 0.55;

  // Card 1: Stakeholders
  card(s, MX, rowY, colW, rowH, C.teal);
  cardHeader(s, MX, rowY, colW, "01 · Stakeholders & Workflow");
  s.addText([
    { text: "Primary: ", options: { bold: true, color: C.textLight } },
    { text: "engineering teams running multi-agent systems near production (tau-bench retail).\n\n", options: { color: C.textMuted } },
    { text: "Today: ", options: { bold: true, color: C.textLight } },
    { text: "trace captured → human reads it → guesses the cause. No systematic silent-failure check. No fix verification.\n\n", options: { color: C.textMuted } },
    { text: "Field baseline: 14.2% step accuracy (Who&When) — the number this project must beat.", options: { color: C.accentBright } },
  ], { x: MX + 0.2, y: rowY + 0.38, w: colW - 0.38, h: rowH - 0.5, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 10, lineSpacing: 15, valign: "top" });

  // Card 2: Gap table
  const x2 = MX + colW + 0.16;
  card(s, x2, rowY, colW, rowH, C.orange);
  cardHeader(s, x2, rowY, colW, "02 · The Gap Is Structural");
  const gapRows = [
    [{ text: "", options: { fill: C.panelAlt } }, { text: "Attribution", options: { bold: true } }, { text: "Silent-fail", options: { bold: true } }, { text: "Fix-verify", options: { bold: true } }],
    ["ErrorProbe", "59.5%", "admits no", "—"],
    ["Manual", "14.2%", "—", "—"],
    ["Granite", "on 59.5%", "scoped+meas.", "recovery rate"],
  ];
  s.addTable(gapRows.map((r, ri) => r.map((c, ci) => (
    typeof c === "string" ? { text: c, options: { fontSize: 8.3, color: ri === 0 ? C.textFaint : (ri === 3 ? C.green : C.textMuted), fontFace: F_MONO, bold: ri === 3 } } : c
  ))), {
    x: x2 + 0.2, y: rowY + 0.4, w: colW - 0.4, h: 1.15,
    border: { type: "solid", color: C.line, pt: 0.5 }, autoPage: false, fill: { color: C.panel },
    colW: [(colW - 0.4) * 0.28, (colW - 0.4) * 0.24, (colW - 0.4) * 0.24, (colW - 0.4) * 0.24],
  });
  s.addText("No system checked confirms attribution + silent-failure detection + counterfactual verification + cross-arch generalization, as one pipeline.", {
    x: x2 + 0.2, y: rowY + 1.65, w: colW - 0.4, h: rowH - 1.8, isTextBox: true, margin: 0,
    fontFace: F_BODY, fontSize: 9.3, color: C.textMuted, lineSpacing: 13,
  });

  // Card 3: Research lineage
  const x3 = x2 + colW + 0.16;
  card(s, x3, rowY, colW, rowH, C.accent);
  cardHeader(s, x3, rowY, colW, "03 · Research Lineage");
  const bars = [["Who&When\nICML 25", 14.2, 0.24], ["AgenTracer\nICLR 26", null, 0.34], ["ErrorProbe\nACL 26", 59.5, 1.0]];
  const barAreaY = rowY + 0.45, barAreaH = 1.15, barW = 0.55, gap = 0.22;
  let bx = x3 + 0.35;
  bars.forEach((b) => {
    const h = barAreaH * b[2];
    s.addShape(pres.ShapeType.roundRect, { x: bx, y: barAreaY + (barAreaH - h), w: barW, h, rectRadius: 0.04, fill: { color: C.accent } });
    s.addText(b[1] ? `${b[1]}%` : "—", { x: bx - 0.15, y: barAreaY + (barAreaH - h) - 0.24, w: barW + 0.3, h: 0.22, isTextBox: true, margin: 0, align: "center", fontFace: F_MONO, fontSize: 9, bold: true, color: C.accentBright });
    s.addText(b[0], { x: bx - 0.2, y: barAreaY + barAreaH + 0.06, w: barW + 0.4, h: 0.4, isTextBox: true, margin: 0, align: "center", fontFace: F_MONO, fontSize: 7.3, color: C.textFaint });
    bx += barW + gap;
  });
  s.addText("ErrorProbe chosen on performance, not recency. CrewAI+LangGraph used by none of 9 papers reviewed. Constraint-based SED, not LLM-judge (≤0.65 AUROC).", {
    x: x3 + 0.2, y: rowY + 2.05, w: colW - 0.4, h: rowH - 2.2, isTextBox: true, margin: 0,
    fontFace: F_BODY, fontSize: 8.8, color: C.textMuted, lineSpacing: 12,
  });
}

// ============================================================
// SLIDE 2 — EXHIBIT II: THE DIAGNOSIS
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, "II", "The Diagnosis, Proven Piece by Piece",
    "Complexity · Architecture · Proof of Concept",
    "Trace → execution graph → Semantic Error Diagnostic (parallel) → causal trace → Repair Agent → verified replay. Eight real spikes back every arrow.");

  // pipeline strip
  const steps = ["trace", "execution graph", "Semantic Error Diagnostic", "causal trace", "Repair Agent", "verified replay"];
  let px = MX;
  const stepH = 0.32;
  steps.forEach((st, i) => {
    const w = 0.35 + st.length * 0.075;
    s.addShape(pres.ShapeType.roundRect, { x: px, y: topY, w, h: stepH, rectRadius: 0.05, fill: { color: C.panelAlt }, line: { color: C.line, width: 0.5 } });
    s.addText(st, { x: px, y: topY, w, h: stepH, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F_MONO, fontSize: 8, color: C.textMuted });
    px += w + 0.14;
    if (i < steps.length - 1) {
      s.addText("→", { x: px - 0.12, y: topY, w: 0.2, h: stepH, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F_BODY, fontSize: 10, color: C.textFaint });
      px += 0.06;
    }
  });

  const rowY = topY + stepH + 0.2;
  const leftW = CW * 0.42, rightW = CW - leftW - 0.16;

  // CCP card (left)
  card(s, MX, rowY, leftW, 2.85, C.teal);
  cardHeader(s, MX, rowY, leftW, "04 · Complex Computing — 8 of 9 Clear");
  const ccp = [
    ["1", "Conflicting reqs — depth vs. latency vs. privacy"],
    ["2", "No obvious solution — best published 59.5% after 7 papers"],
    ["3", "Depth of knowledge — graph modeling, causal reasoning"],
    ["4", "Unfamiliar issues — non-determinism, cross-arch."],
    ["5", "Beyond standard practice — no off-the-shelf equivalent"],
    ["6*", "Diverse stakeholders — contact pending"],
    ["7", "Real consequences — a missed failure ships silently"],
    ["8", "Interdependence — the execution graph models it"],
    ["9", "Ill-defined cause — 3 unknowns at diagnosis time"],
  ];
  ccp.forEach((row, i) => {
    const y = rowY + 0.4 + i * 0.265;
    const isWeak = row[0] === "6*";
    s.addText(row[0].replace("*", ""), { x: MX + 0.2, y, w: 0.3, h: 0.25, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 8.5, color: isWeak ? C.amber : C.textFaint, bold: true });
    s.addText(row[1], { x: MX + 0.5, y, w: leftW - 0.7, h: 0.25, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.6, color: isWeak ? C.amber : C.textMuted });
  });

  // Live diagnosis exhibit (right, static "frozen frame" of the animated version)
  card(s, MX + leftW + 0.16, rowY, rightW, 2.85, C.accent);
  cardHeader(s, MX + leftW + 0.16, rowY, rightW, "· Exhibit — One Real Diagnosis Run");
  const nodes = [["PriceExtractor", "price = 100.00", C.green], ["TaxCalculator", "total = 108.00", C.green], ["Verifier", "pass = true", C.green]];
  const nx0 = MX + leftW + 0.16 + 0.35, ny = rowY + 0.6, nw = 1.55, nh = 0.85;
  const gapN = (rightW - 0.7 - nw * 3) / 2;
  nodes.forEach((n, i) => {
    const x = nx0 + i * (nw + gapN);
    s.addShape(pres.ShapeType.roundRect, { x, y: ny, w: nw, h: nh, rectRadius: 0.06, fill: { color: C.panelAlt }, line: { color: n[2], width: 1.25 } });
    s.addText(n[0], { x, y: ny + 0.12, w: nw, h: 0.26, isTextBox: true, margin: 0, align: "center", fontFace: F_BODY, fontSize: 9.5, bold: true, color: C.textLight });
    s.addText(n[1], { x, y: ny + 0.42, w: nw, h: 0.26, isTextBox: true, margin: 0, align: "center", fontFace: F_MONO, fontSize: 9, color: C.accentBright });
    if (i < 2) s.addText("→", { x: x + nw + gapN / 2 - 0.1, y: ny + 0.25, w: 0.2, h: 0.3, isTextBox: true, margin: 0, align: "center", fontFace: F_BODY, fontSize: 12, color: C.textFaint });
  });
  s.addText([
    { text: "Fault: ", options: { bold: true, color: C.red } }, { text: "price silently corrupted $100.00 → $90.00 → wrong total $97.20 (expected $108.00).\n", options: { color: C.textMuted } },
    { text: "Repair: ", options: { bold: true, color: C.green } }, { text: "SED flags mismatch → causal trace localizes PriceExtractor → Repair Agent proposes $100.00 → replayed: 97.20 → 108.00, recovery_success = true.", options: { color: C.textMuted } },
  ], { x: MX + leftW + 0.36, y: ny + nh + 0.16, w: rightW - 0.4, h: 0.9, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9, lineSpacing: 13 });
  s.addText("Chained from Spike 5 + Spike 8 case “tax_total” — the same run in the poc-demo console.", {
    x: MX + leftW + 0.36, y: rowY + 2.85 - 0.3, w: rightW - 0.5, h: 0.24, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 7.5, color: C.textFaint,
  });

  // Spike evidence table (full width, bottom)
  const tY = rowY + 2.85 + 0.16;
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
    text: c, options: {
      fontSize: ri === 0 ? 8 : 8.3, fontFace: ci === 1 && ri > 0 ? F_MONO : F_BODY,
      bold: ri === 0, color: ri === 0 ? C.textFaint : (ci === 1 ? statusColor(c) : C.textMuted),
      fill: { color: ri === 0 ? C.panelAlt : C.panel },
    },
  }))), {
    x: MX, y: tY, w: CW, h: PH - tY - 0.5,
    border: { type: "solid", color: C.line, pt: 0.5 },
    colW: [CW * 0.24, CW * 0.18, CW * 0.58],
    autoPage: false,
  });
}

// ============================================================
// SLIDE 3 — EXHIBIT III: THE VERDICT
// ============================================================
{
  const s = pres.addSlide(); bgSlide(s);
  const topY = chrome(s, "III", "The Verdict, Decided Before The Data",
    "Evaluation · Scope & Risk · People",
    "Every threshold below was written before any result exists — so the evidence judges the project, not the other way around.");

  const colW = (CW - 0.32) / 3;
  const rowH = PH - topY - 0.55;

  // Card 1: Evaluation plan
  card(s, MX, topY, colW, rowH, C.blue);
  cardHeader(s, MX, topY, colW, "06 · Evaluation Plan");
  s.addText([
    { text: "Baseline: ", options: { bold: true, color: C.textLight } }, { text: "ErrorProbe reproduced — pre-registered ±10pt band around 59.5%.\n\n", options: { color: C.textMuted } },
    { text: "Data: ", options: { bold: true, color: C.textLight } }, { text: "Who&When (184) + new benchmark, floor 500 / stretch 1,000, 15–20% clean controls.\n\n", options: { color: C.textMuted } },
    { text: "Metrics: ", options: { bold: true, color: C.textLight } }, { text: "accuracy · propagation F1 · silent-fail P/R+coverage · FP rate on clean controls · recovery rate · false repair rate · latency overhead (<50%)", options: { color: C.textMuted } },
  ], { x: MX + 0.2, y: topY + 0.38, w: colW - 0.4, h: 1.85, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.3, lineSpacing: 13 });
  const bandY = topY + 2.35;
  const bands = [["failure", C.red], ["acceptable", C.textFaint], ["strong", C.teal], ["exceptional", C.green]];
  let bx = MX + 0.2;
  const bw = (colW - 0.5) / 4 - 0.06;
  bands.forEach((b) => {
    s.addShape(pres.ShapeType.roundRect, { x: bx, y: bandY, w: bw, h: 0.32, rectRadius: 0.05, line: { color: b[1], width: 1 } });
    s.addText(b[0], { x: bx, y: bandY, w: bw, h: 0.32, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F_MONO, fontSize: 6.8, color: b[1] });
    bx += bw + 0.08;
  });
  s.addText("FP-rate-on-clean-controls appears in zero reviewed papers or platforms.", {
    x: MX + 0.2, y: bandY + 0.44, w: colW - 0.4, h: 0.5, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.3, italic: true, color: C.textFaint,
  });

  // Card 2: Scope & risk
  const x2 = MX + colW + 0.16;
  card(s, x2, topY, colW, rowH, C.amber);
  cardHeader(s, x2, topY, colW, "07 · Scope, Risk & $0 Resourcing");
  s.addText([
    { text: "Core, 10 items: ", options: { bold: true, color: C.textLight } },
    { text: "Tier 1 · 8 ", options: { color: C.green, bold: true } }, { text: "each with a real spike; ", options: { color: C.textMuted } },
    { text: "Tier 2 · 2 ", options: { color: C.amber, bold: true } }, { text: "gated — Recovery Controller (no PoC yet), Verified Repair Memory (failed its one test, stated honestly).\n\n", options: { color: C.textMuted } },
    { text: "Resources: ", options: { bold: true, color: C.textLight } }, { text: "$0 — local Ollama, full project. Paid alt priced (≈$353–$881) and explicitly rejected.", options: { color: C.textMuted } },
  ], { x: x2 + 0.2, y: topY + 0.38, w: colW - 0.4, h: 1.55, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.3, lineSpacing: 13 });
  const riskRows = [
    [{ text: "Risk", options: { bold: true } }, { text: "Fallback", options: { bold: true } }],
    ["Miss the ±10pt band", "Transparent dual-reporting"],
    ["Recovery Controller gate fails", "Resume via replay — Tier 1 delivers it"],
    ["Repair Memory fails again", "Ships as memory on/off ablation"],
    ["LLM API down at runtime", "Documented degraded state, not a crash"],
  ];
  s.addTable(riskRows.map((r, ri) => r.map((c) => (
    typeof c === "string" ? { text: c, options: { fontSize: 8, fontFace: F_BODY, color: ri === 0 ? C.textFaint : C.textMuted } } : c
  ))), {
    x: x2 + 0.2, y: topY + 2.0, w: colW - 0.4, h: rowH - 2.15,
    border: { type: "solid", color: C.line, pt: 0.5 }, colW: [(colW - 0.4) * 0.45, (colW - 0.4) * 0.55], autoPage: false,
  });

  // Card 3: Team & DEI
  const x3 = x2 + colW + 0.16;
  card(s, x3, topY, colW, rowH, C.green);
  cardHeader(s, x3, topY, colW, "08 · Team, Timeline & DEI");
  const teamRows = [
    ["Shahoud — Data/Benchmark", "If removed: no cross-architecture benchmark exists.", C.teal],
    ["Noor — Diagnosis Engine", "If removed: no attribution algorithm, no SED.", C.orange],
    ["Saif — Platform", "If removed: nothing installs outside the dev machine.", C.blue],
  ];
  teamRows.forEach((t, i) => {
    const y = topY + 0.42 + i * 0.62;
    s.addShape(pres.ShapeType.roundRect, { x: x3 + 0.2, y, w: 0.32, h: 0.32, rectRadius: 0.06, fill: { color: t[2] } });
    s.addText(t[0][0], { x: x3 + 0.2, y, w: 0.32, h: 0.32, isTextBox: true, margin: 0, align: "center", valign: "middle", fontFace: F_TITLE, fontSize: 12, bold: true, color: C.bgDark });
    s.addText(t[0], { x: x3 + 0.6, y: y - 0.02, w: colW - 0.8, h: 0.24, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 9.5, bold: true, color: C.textLight });
    s.addText(t[1], { x: x3 + 0.6, y: y + 0.22, w: colW - 0.8, h: 0.3, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8, italic: true, color: C.textMuted });
  });
  const barY = topY + 0.42 + 3 * 0.62 + 0.14;
  s.addShape(pres.ShapeType.rect, { x: x3 + 0.2, y: barY, w: (colW - 0.4) * (490 / 1130), h: 0.22, fill: { color: C.teal } });
  s.addShape(pres.ShapeType.rect, { x: x3 + 0.2 + (colW - 0.4) * (490 / 1130), y: barY, w: (colW - 0.4) * (640 / 1130), h: 0.22, fill: { color: C.orange } });
  s.addText("FYP-1 · 490h", { x: x3 + 0.2, y: barY + 0.26, w: (colW - 0.4) / 2, h: 0.2, isTextBox: true, margin: 0, fontFace: F_MONO, fontSize: 7.5, color: C.textFaint });
  s.addText("FYP-2 · 640h", { x: x3 + 0.2 + (colW - 0.4) / 2, y: barY + 0.26, w: (colW - 0.4) / 2, h: 0.2, isTextBox: true, margin: 0, align: "right", fontFace: F_MONO, fontSize: 7.5, color: C.textFaint });
  s.addText("DEI: MIT/CC BY 4.0 release; color paired with text (WCAG owed Final-1). Ethics: advisory-only, human-gated fixes, informed consent for real trace data.", {
    x: x3 + 0.2, y: barY + 0.5, w: colW - 0.4, h: rowH - (barY - topY) - 0.6, isTextBox: true, margin: 0, fontFace: F_BODY, fontSize: 8.3, color: C.textMuted, lineSpacing: 12,
  });
}

const OUT = process.argv[2] || "Granite_Proposal_Defense_3Slide.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("Wrote " + OUT));
