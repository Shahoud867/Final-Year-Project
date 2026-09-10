"""
Generates Granite_Speaking_Notes_and_QA.pdf — a rehearsal-ready speaking-notes
and Q&A coaching document for the proposal defense, built strictly from the
actual content and speaker notes of Granite_Proposal_Defense_v2.pptx (10
slides) plus the handbook requirements already cross-referenced in this repo
(plan doc, risk-register, Software_Design_Specification.md, Form13, etc.).
Every number, name, and citation below traces to that source material —
nothing here is invented beyond natural spoken phrasing of what's already on
the slides and in their notes.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    ListFlowable, ListItem, HRFlowable, KeepTogether
)

# ---------------------------------------------------------------- styles ---
styles = getSampleStyleSheet()
INK = HexColor("#1a1a2e")
ACCENT = HexColor("#1e7a8c")
ACCENT_SOFT = HexColor("#e4f1f3")
GOLD = HexColor("#a86a1f")
GOLD_SOFT = HexColor("#f5ead9")
WARN = HexColor("#a8681a")
WARN_SOFT = HexColor("#fbf0df")
GREEN = HexColor("#2f7a4f")
GREEN_SOFT = HexColor("#e2eee6")
LINE = HexColor("#cccccc")
MUTED = HexColor("#666666")

styles.add(ParagraphStyle(name="TCTitle", fontSize=23, leading=27, alignment=TA_CENTER, spaceAfter=6, textColor=INK, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="TCSubtitle", fontSize=12.5, leading=17, alignment=TA_CENTER, textColor=MUTED, spaceAfter=4))
styles.add(ParagraphStyle(name="TCMeta", fontSize=10, leading=14, alignment=TA_CENTER, textColor=ACCENT, spaceAfter=2))
styles.add(ParagraphStyle(name="H1", fontSize=16, leading=20, spaceBefore=20, spaceAfter=10, textColor=INK, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="H2", fontSize=12.5, leading=16, spaceBefore=12, spaceAfter=6, textColor=ACCENT, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="H3", fontSize=10.8, leading=14, spaceBefore=8, spaceAfter=4, textColor=GOLD, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Body", fontSize=10, leading=14.5, spaceAfter=6))
styles.add(ParagraphStyle(name="Say", fontSize=10.3, leading=15.5, spaceAfter=6, textColor=INK, fontName="Helvetica"))
styles.add(ParagraphStyle(name="Small", fontSize=8.5, leading=12, textColor=MUTED))
styles.add(ParagraphStyle(name="Transition", fontSize=9.7, leading=13.5, textColor=colors.white, fontName="Helvetica-Oblique"))
styles.add(ParagraphStyle(name="CellHead", fontSize=8.6, leading=11, textColor=colors.white, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Cell", fontSize=8.4, leading=11.5))
styles.add(ParagraphStyle(name="CellBold", fontSize=8.4, leading=11.5, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="QText", fontSize=9.8, leading=13.5, fontName="Helvetica-Bold", textColor=INK, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle(name="AText", fontSize=9.6, leading=13.5, textColor=HexColor("#222222"), spaceAfter=2))
styles.add(ParagraphStyle(name="KeyPoint", fontSize=9, leading=12.5, textColor=ACCENT, fontName="Helvetica-Oblique", spaceAfter=8))

PAGE_WIDTH = A4[0] - 4 * cm

def P(text, style="Body"):
    return Paragraph(text, styles[style])

def cellify(rows, bold_first_col=False):
    out = []
    for r_idx, row in enumerate(rows):
        new_row = []
        for c_idx, cell in enumerate(row):
            if r_idx == 0:
                new_row.append(Paragraph(str(cell), styles["CellHead"]))
            elif bold_first_col and c_idx == 0:
                new_row.append(Paragraph(str(cell), styles["CellBold"]))
            else:
                new_row.append(Paragraph(str(cell), styles["Cell"]))
        out.append(new_row)
    return out

def table(data, col_fractions, bold_first_col=False, head_color=None):
    col_widths = [PAGE_WIDTH * f for f in col_fractions]
    wrapped = cellify(data, bold_first_col=bold_first_col)
    t = Table(wrapped, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), head_color or INK),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, HexColor("#f5f5fa")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def slide_box(num, title, presenter, seconds, say_paragraphs, covers=None):
    """One slide's full speaking-note block, boxed and kept together where possible."""
    flow = []
    header = Table(
        [[Paragraph(f"<b>SLIDE {num}</b> — {title}", styles["H3"]),
          Paragraph(f"<b>{presenter}</b>  ·  ~{seconds}s", styles["Small"])]],
        colWidths=[PAGE_WIDTH * 0.72, PAGE_WIDTH * 0.28],
    )
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GOLD_SOFT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("RIGHTPADDING", (1, 0), (1, 0), 8),
    ]))
    flow.append(header)
    flow.append(Spacer(1, 4))
    flow.append(P("<b>SAY THIS:</b>", "Small"))
    for para in say_paragraphs:
        flow.append(P(para, "Say"))
    if covers:
        flow.append(P(f"<i>Covers:</i> {covers}", "Small"))
    flow.append(Spacer(1, 10))
    return flow

def transition_box(text):
    t = Table([[Paragraph(text, styles["Transition"])]], colWidths=[PAGE_WIDTH])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t

def qa(question, answer, key=None):
    flow = [P(f"Q: {question}", "QText"), P(answer, "AText")]
    if key:
        flow.append(P(f"Key point to remember: {key}", "KeyPoint"))
    return KeepTogether(flow)

story = []

# ============================================================ TITLE PAGE ===
story.append(Spacer(1, 40))
story.append(P("Granite — Proposal Defense", "TCTitle"))
story.append(P("Speaking Notes, Timing Plan &amp; Q&amp;A Coaching Guide", "TCSubtitle"))
story.append(Spacer(1, 6))
story.append(P("Built from Granite_Proposal_Defense_v2.pptx (10 slides) — every line traceable to a slide or its notes", "TCMeta"))
story.append(P("Team: Shahoud Shahid (23i-2515) · Muhammad Noor (23i-2520) · Saif Shahzad (23i-2634)", "TCMeta"))
story.append(P("Supervisor: Dr. Adil Majeed  ·  F26-060-Granite  ·  Stream A", "TCMeta"))
story.append(Spacer(1, 14))
story.append(HRFlowable(width=PAGE_WIDTH, thickness=1, color=LINE))
story.append(Spacer(1, 14))
story.append(P(
    "This document is a rehearsal tool, not a script to read verbatim. Read it several times, "
    "then speak from memory in your own words — the panel is testing whether you understand the "
    "project, not whether you can recite a paragraph. Total target time: <b>9 minutes 50 seconds</b>, "
    "leaving a natural buffer inside the 10-minute limit.", "Body"
))
story.append(PageBreak())

# ============================================================ 1. OVERVIEW ==
story.append(P("1. Presentation Overview &amp; 10-Minute Timing Plan", "H1"))
story.append(P(
    "Ten slides, three presenters, one continuous story: what's broken today → why it's genuinely "
    "hard → what we built and proved → how we'll prove the rest → who owns what. The timing below "
    "is deliberately under 10 minutes so normal delivery speed — including a breath between slides — "
    "still lands inside the limit.", "Body"
))

timing_rows = [
    ["#", "Slide title", "Presenter", "Target time", "Running total"],
    ["1", "Title &amp; One-Line Problem", "Shahoud", "~25s", "0:25"],
    ["2", "Problem &amp; Users", "Shahoud", "~55s", "1:20"],
    ["3", "Existing Solutions &amp; Prior FYP Comparison", "Shahoud", "~65s", "2:25"],
    ["4", "Research &amp; Technical Basis", "Shahoud", "~55s", "3:20"],
    ["—", "Transition: Shahoud → Noor", "—", "~15s", "3:35"],
    ["5", "Complex Computing Challenge (CCP)", "Noor", "~65s", "4:40"],
    ["6", "Proposed Solution &amp; Contribution", "Noor", "~65s", "5:45"],
    ["7", "POC / Feasibility Evidence", "Noor", "~65s", "6:50"],
    ["—", "Transition: Noor → Saif", "—", "~15s", "7:05"],
    ["8", "Evaluation Plan &amp; Risks", "Saif", "~60s", "8:05"],
    ["9", "Scope, Work Division &amp; Iteration Plan", "Saif", "~60s", "9:05"],
    ["10", "Team Responsibilities, DEI &amp; Ethics/Legal", "Saif", "~45s", "9:50"],
]
story.append(table(timing_rows, [0.05, 0.42, 0.15, 0.14, 0.17], head_color=INK))
story.append(Spacer(1, 10))
story.append(P(
    "<b>Total: 9 minutes 50 seconds</b> against a 10-minute limit — a real, usable ~10-second buffer, "
    "not a razor's edge. If a presenter runs slightly long on one slide, the next presenter can trim "
    "their own opening line rather than rushing the whole remaining deck.", "Body"
))

story.append(P("2. Presenter / Slide Allocation", "H1"))
alloc_rows = [
    ["Presenter", "Slides owned", "Total time", "Why this grouping"],
    ["Shahoud\n(Data / Benchmark)", "1, 2, 3, 4", "~3 min 20s",
     "Opens the story: title → problem → what already exists and the one prior FYP checked → the literature "
     "that shaped our decisions. Natural fit — the prior-FYP archive check and dataset/benchmark choices are "
     "Shahoud's own subsystem."],
    ["Noor\n(Diagnosis Engine)", "5, 6, 7", "~3 min 15s",
     "Carries the technical core: why this is genuinely hard (CCP), what's actually being built (the diagnosis "
     "architecture), and the real proof-of-concept evidence — almost all of which comes from the diagnosis "
     "pipeline Noor owns."],
    ["Saif\n(Platform)", "8, 9, 10", "~2 min 45s",
     "Closes with how it will be judged (evaluation + risks), how the work is split and scheduled, and the "
     "team/ethics wrap-up — a natural closing role for the person who owns deployment and the product itself."],
]
story.append(table(alloc_rows, [0.16, 0.13, 0.13, 0.58], bold_first_col=True))
story.append(PageBreak())

# ============================================================ 3. SPEAKING NOTES ==
story.append(P("3. Complete Slide-by-Slide Speaking Notes", "H1"))
story.append(P(
    "Every number, name and claim below appears on the slide or in its embedded speaker notes. "
    "Nothing here introduces a new fact — it explains, in plain spoken words, what the slide already says.",
    "Body"
))
story.append(Spacer(1, 6))

# ---- Slide 1 ----
story += slide_box(1, "Title &amp; One-Line Problem", "SHAHOUD", 25, [
    "Good morning. We're Team Granite. I'm Shahoud, and with me are Noor and Saif. "
    "Granite is a self-healing multi-agent system for semantic error diagnosis, verified repair, and recovery.",
    "In one sentence: when a team of AI agents fails — even when the wrong answer looks completely "
    "right — no existing method can reliably say which agent caused it, or check whether a proposed "
    "fix actually works before you trust it. That's the gap we're closing, under the supervision of "
    "Dr. Adil Majeed.",
], covers="C.16 slide 1 — title, team, supervisor, stream, one-line problem")

# ---- Slide 2 ----
story += slide_box(2, "Problem &amp; Users", "SHAHOUD", 55, [
    "So who actually has this problem? Picture an engineering team that's running several AI "
    "\"agents\" together — think of them as specialist workers on a task: one plans, one looks things "
    "up, one writes the final answer. When that team is running in or near production, product teams "
    "downstream depend on its output, and auditors need to be able to see what went wrong when it fails.",
    "Here's today's actual workflow, without Granite: a trace of what the agents did gets captured — "
    "by tools like LangSmith, Langfuse, Braintrust or Arize — and then a human just reads through it "
    "and guesses the root cause. There's no published accuracy for that guess. There's no check at "
    "all for what we call a \"silent failure\" — a confident, wrong answer that doesn't trigger any "
    "error or crash, so it slips through unnoticed. And there's no way to test a fix before you ship it.",
    "The field's own measured number for \"a human reads the trace and guesses\" is 14.2% step "
    "accuracy — that's the baseline the entire project is trying to beat. This connects to UN "
    "Sustainable Development Goal 9, industry and infrastructure, because this is genuinely new "
    "reliability tooling for a genuinely new category of software.",
], covers="C.16 slide 2 — stakeholders, current workflow, consequence of failure, SDG")

# ---- Slide 3 ----
story += slide_box(3, "Existing Solutions &amp; Prior FYP Comparison", "SHAHOUD", 65, [
    "Is this gap real, or did we just miss a feature that already exists somewhere? We checked, "
    "carefully. ErrorProbe, the strongest published academic method, reaches 59.5% step accuracy — "
    "but by its own admission it cannot catch silent failures, and it's never been tested on an agent "
    "framework outside the two it was built and tuned on.",
    "On the commercial side, LangSmith Engine and Arize Alyx both launched automated diagnosis "
    "features this year — we say that upfront, because an early draft of our own research claimed "
    "\"nobody automates this,\" and a direct check proved that stale. We corrected it ourselves, on "
    "the record. But neither of them publishes an accuracy number, neither is confirmed to test a fix "
    "before applying it, and both are locked to their own platform.",
    "And we didn't stop at commercial products — we checked our own department's history too. We "
    "went through 660 project titles across every cohort back to 2019 and compared them structurally, "
    "not just by title. The closest one we found is a Spring 2024 project on hallucination detection "
    "in a single AI model's text — same underlying problem, but it only covers roughly one of our four "
    "pipeline stages, with no multi-agent tracing and no repair step at all.",
    "So the real gap isn't any single missing feature. It's that nothing — not one paper, not one "
    "product, not one prior project here — combines attribution, silent-failure detection, verified "
    "repair, and generalizing across different agent frameworks, in one working pipeline.",
], covers="C.10 — product/prior-FYP/workflow comparison, structural not title-level; C.16 slide 3")

# ---- Slide 4 ----
story += slide_box(4, "Research &amp; Technical Basis", "SHAHOUD", 55, [
    "We read seven papers in full, not just abstracts, and every major decision we made traces "
    "back to one of them. The field's own progress looks like a climb: a single AI model just "
    "guessing scores 14.2%, an early automated method called AgenTracer lands around 37 to 43%, and "
    "ErrorProbe — our chosen baseline — reaches 59.5%. We picked ErrorProbe because it's the strongest "
    "published number, not because it's the newest.",
    "Three decisions followed directly from that reading. We committed to CrewAI and LangGraph as our "
    "two agent frameworks specifically because none of the seven papers we reviewed used either one — "
    "that's what actually tests generalization. We chose a rule-based, constraint-checking approach "
    "for catching silent failures instead of asking another AI model to judge the output, because the "
    "literature shows that approach barely beats a coin flip. And a market survey recommended we "
    "narrow down to just one agent framework to keep the project small — we read that advice and "
    "declined it, because narrowing to one framework would delete the entire cross-framework question "
    "we're trying to answer.",
    "One honest caveat, said before anyone has to ask for it: different papers use different underlying "
    "AI models, so some of the reported gap partly reflects raw model strength, not just method quality "
    "— we control for that inside our own experiments.",
], covers="Section 11/C.11 — research-to-decision table; literature review; research gap")

story.append(transition_box(
    "TRANSITION — Shahoud to Noor: \"That's the landscape and the gap. Noor will now walk you through "
    "why this is genuinely hard, what we're actually building, and the real evidence we already have "
    "on disk.\""
))
story.append(Spacer(1, 10))

# ---- Slide 5 ----
story += slide_box(5, "Complex Computing Challenge (CCP)", "NOOR", 65, [
    "Before I explain what we're building, I want to answer the question every panel asks first: is "
    "this actually hard enough to count as a final-year capstone, or is it routine coding? The "
    "handbook gives nine specific characteristics of genuinely complex computing work, and we checked "
    "ourselves against every one of them. We clear eight of the nine clearly — things like "
    "conflicting requirements, no obvious existing solution, needing real depth of knowledge, and "
    "consequences that actually matter if we get it wrong. The ninth, having genuinely diverse "
    "stakeholders, we're honestly marking as still developing, because live practitioner contact is "
    "scheduled for later in the project, not done yet — we'd rather say that plainly than overclaim it.",
    "But here's the real test the handbook itself proposes: could a capable student, with AI "
    "assistance, build this in a week? Our honest answer is yes — for a stripped-down wrapper that "
    "just captures a trace and asks a model to guess. But that quick version would get wrong exactly "
    "the parts that actually carry the marks: it wouldn't be tested on an unfamiliar agent framework, "
    "it couldn't tell a silent failure from a correct answer, it wouldn't measure a false-positive "
    "rate on clean, working examples, and it would have zero proof that any suggested fix actually "
    "works. Our real difficulty lives in the data, the evaluation design, and the constraints — not "
    "in the wrapper around a model call.",
], covers="C.7 — CCP/complex-computing justification, 9 Seoul Accord characteristics, resilience test")

# ---- Slide 6 ----
story += slide_box(6, "Proposed Solution &amp; Contribution", "NOOR", 65, [
    "So what are we actually building? The best published method tops out at 59.5% accuracy, has "
    "never been tested outside two agent frameworks, and admits it misses silent failures. We're "
    "building two things on top of that: a new benchmark that tests generalization across different "
    "agent frameworks, and a diagnosis pipeline that adds a rule-based check specifically for silent "
    "failures — packaged as an installable toolkit, not just a research script.",
    "Here's how it actually works, end to end. The target system — built on CrewAI or LangGraph — "
    "runs, and our system watches it. Lane A, which I'll call the data lane, instruments the "
    "framework and injects controlled test faults to build our benchmark. Lane B, the diagnosis lane "
    "that I personally own, normalizes the execution trace, builds a dependency graph out of it, and "
    "runs two things at once: a backward trace to find the responsible agent and step, and our "
    "Semantic Error Diagnostic — a rule-based checker that catches confident-but-wrong outputs "
    "directly, without ever calling an AI model to judge itself. And where there's genuinely no rule "
    "to check against, it says so honestly instead of guessing — that abstention rate is reported as "
    "its own number, not hidden. Lane C, the platform lane, then generates a candidate repair, "
    "verifies it through a controlled replay before trusting it, and surfaces everything through a "
    "dashboard and an installable SDK.",
    "The AI model itself only sits at about fifteen to twenty percent of the components — the "
    "differentiating logic, the part that actually makes the diagnosis, never calls it at all.",
], covers="C.6 — proposed solution, architecture, contribution statement; C.14 — external component classification")

# ---- Slide 7 ----
story += slide_box(7, "POC / Feasibility Evidence", "NOOR", 65, [
    "The handbook requires us to show evidence, not just describe it — so here it is, and I want to "
    "lead with the honest negative first. One of our eight proof-of-concept spikes — a preventive "
    "classifier — came back at 0.25 precision, recall and F1, essentially random. We're not hiding "
    "that; the guide itself says a spike that disproves an assumption is worth more than one that "
    "just confirms what you already believed, and every number on this slide is real and "
    "recomputable straight from files in our repository — happy to open one live if asked.",
    "Now the real results. Across five independent runs, our reproduction of ErrorProbe's method "
    "hit an average of 71.4% agent-level accuracy and 13.2% step-level accuracy — reported as a range "
    "because we're honest about run-to-run variance, not just one lucky number. Our Semantic Error "
    "Diagnostic caught a genuinely tricky near-miss — twenty dollars reported against nineteen "
    "seventy-five actually correct — with zero false alarms. Our repair-and-replay mechanism took a "
    "corrupted result of ninety-seven point two and correctly recovered it to one-oh-eight. And our "
    "Repair Agent succeeded on four out of six real test cases, with both failures traced to one "
    "single, fixable cause. Eight spikes, eight with real evidence on disk. We also have a working, "
    "clickable prototype console you can see right here, running against real spike data.",
], covers="C.12 — mandatory proposal-stage POC, demonstrated with evidence")

story.append(transition_box(
    "TRANSITION — Noor to Saif: \"That's the evidence that this already works at small scale. Saif "
    "will now cover how we'll prove it at full scale, how the work is split across the team, and "
    "wrap up with our timeline and ethics commitments.\""
))
story.append(Spacer(1, 10))

# ---- Slide 8 ----
story += slide_box(8, "Evaluation Plan &amp; Risks", "SAIF", 60, [
    "Good evidence isn't enough on its own — you also need to know, in advance, what counts as "
    "success. So before running the full reproduction, we pre-registered our acceptance rule: we "
    "accept it if it lands within ten points of ErrorProbe's published 59.5%, on a fairly comparable "
    "model. We measure agent and step accuracy, how far an error propagates, silent-failure precision "
    "and recall, and — something no paper we reviewed reports — a false-positive rate measured on "
    "clean, correctly-working runs, not just failing ones.",
    "We also defined four honest outcome bands in advance, each tied to a specific risk. If the "
    "reproduction misses our ten-point band, that's reported transparently side-by-side with the "
    "published number, exactly as the handbook itself allows — that's the floor, not a failure of the "
    "project. If our Recovery Controller mechanism doesn't pass its checkpoint at Mid-1, we fall back "
    "to a method we've already proven works, and that lands us at an acceptable result. If our repair "
    "memory feature fails its re-test, it still ships as a legitimate before-and-after comparison "
    "study, and a strong result means beating the baseline on frameworks it's never seen, with over "
    "seventy percent silent-failure accuracy. An exceptional result adds over fifty percent recovery "
    "on verified repairs. Every one of these rules was written before we have the results — nothing "
    "gets adjusted afterward to make a number look better.",
], covers="C.13 — evaluation plan, baseline, metrics, success criteria, failure cases; §5.3 pre-registration")

# ---- Slide 9 ----
story += slide_box(9, "Scope, Work Division &amp; Iteration Plan", "SAIF", 60, [
    "Here's exactly who owns what, and why each piece genuinely needs to exist. Shahoud owns data "
    "and the benchmark — instrumenting the agent frameworks, injecting test faults, and building and "
    "releasing the benchmark itself. Without that piece, there's no cross-framework benchmark and no "
    "way to test our core claim at all. Noor owns the diagnosis engine — the graph construction, the "
    "ErrorProbe reproduction, the Semantic Error Diagnostic, and the causal tracing. Without that, "
    "there's no attribution and no silent-failure detection — the actual contribution disappears. I "
    "own the platform — the repair-and-replay engine, the SDK, the backend, and the deployment. "
    "Without that piece, nothing here is actually installable outside our own development machines.",
    "Our committed core is eight mechanisms already backed by real evidence, plus two more that are "
    "gated on specific criteria we'll test at Mid-1 — eight further extensions only get built once "
    "that core genuinely works. The whole project runs at zero committed cost — every model call runs "
    "on a free, local model — and we deliberately chose not to spend roughly three-hundred-fifty to "
    "eight-hundred-eighty dollars on a paid alternative, reporting that trade-off honestly rather than "
    "hiding it. We're scheduled against five formal approval gates from this proposal defense through "
    "to final delivery, against a budget of eleven-hundred-thirty planned hours across both semesters "
    "— which is exactly what our combined capacity actually is.",
], covers="C.5 — scope, ownership, ability to lose a member and still lose a real piece of contribution; timeline")

# ---- Slide 10 ----
story += slide_box(10, "Team Responsibilities, DEI &amp; Ethics/Legal", "SAIF", 45, [
    "To close: while each of us owns a subsystem, the architecture, integration, quality, security, "
    "data handling, and this defense itself stay shared across all three of us, at every one of our "
    "five gates. On responsible development — releasing our benchmark and tools openly widens who "
    "can access this kind of tooling, in line with that same Sustainable Development Goal we opened "
    "with. Every proposed repair stays advisory, gated behind a human, never applied automatically. "
    "We only inject test faults into systems that have actually consented to it. And when a result "
    "came back negative, like that classifier spike, we published it as found rather than burying it.",
    "One more thing we want to say plainly, because the handbook asks us to name it directly: our AI "
    "usage is Level 2, AI-assisted. We lead every judgment call and every piece of execution "
    "ourselves; AI assists on isolated tasks, and it's logged, session by session, for all nineteen "
    "sessions so far. Any one of us can explain, justify, and modify our own piece of this system "
    "under direct questioning — happy to demonstrate that live, on any part you'd like to pick. Thank "
    "you — we're ready for your questions.",
], covers="C.8 — AI-assisted development level named and justified; C.16 slide 10 — DEI, ethics, legal, ownership test")

story.append(PageBreak())

# ============================================================ 4. TRANSITIONS ==
story.append(P("4. Presenter Transition Lines (quick reference)", "H1"))
story.append(P(
    "The same two lines already embedded above, collected here for a fast run-through during "
    "rehearsal without paging back through the full notes.", "Body"
))
story.append(transition_box(
    "1 → Shahoud to Noor (after slide 4): \"That's the landscape and the gap. Noor will now walk you "
    "through why this is genuinely hard, what we're actually building, and the real evidence we "
    "already have on disk.\""
))
story.append(Spacer(1, 8))
story.append(transition_box(
    "2 → Noor to Saif (after slide 7): \"That's the evidence that this already works at small scale. "
    "Saif will now cover how we'll prove it at full scale, how the work is split across the team, and "
    "wrap up with our timeline and ethics commitments.\""
))
story.append(Spacer(1, 14))
story.append(P(
    "Delivery tip: say the transition while making eye contact with the next presenter, and physically "
    "step back or hand across a clicker if you have one — a visible handoff reads as a rehearsed, "
    "confident team, not three separate solo presentations stitched together.", "Small"
))

story.append(PageBreak())

# ============================================================ 5. CHECKLIST ==
story.append(P("5. Proposal-Defense Coverage Checklist", "H1"))
story.append(P(
    "Every area the handbook expects a proposal defense to cover, mapped to exactly where it's said "
    "out loud. Nothing on this list is forced in artificially — categories genuinely not applicable "
    "at proposal stage (e.g. final deployment evidence, owed at Final-2) are marked as such rather "
    "than stretched to fit.", "Body"
))
checklist_rows = [
    ["Area", "Covered on", "How"],
    ["Problem statement", "Slides 1, 2", "One-line problem (S1); stakeholders, current workflow, consequence (S2)"],
    ["Motivation", "Slides 2, 5", "SDG 9 framing; why the failure mode matters (missed silent failures ship undetected)"],
    ["Proposed solution", "Slide 6", "Contribution statement, three-lane architecture, pipeline walkthrough"],
    ["Objectives / scope", "Slides 6, 9", "In-scope 10 mechanisms; explicit out-of-scope list; committed core vs. gated vs. extensions"],
    ["Target users", "Slide 2", "Primary: engineering teams running multi-agent systems; secondary: product teams, auditors"],
    ["Key features", "Slides 6, 7", "Attribution, silent-failure detection, verified repair, cross-framework SDK — each with POC evidence"],
    ["How the system works", "Slide 6", "Trace → graph → parallel attribution/SED → repair → verified replay → dashboard/SDK"],
    ["Methodology / technical approach", "Slides 4, 6, 8", "Literature-driven decisions; architecture; statistical evaluation protocol"],
    ["Literature review", "Slide 4", "7 papers read in full; accuracy lineage 14.2% → ~40% → 59.5%"],
    ["Research gap", "Slide 3", "Structural comparison table; \"the real gap\" stated as a combination, not one feature"],
    ["Dataset / data sources", "Slide 8", "Who&amp;When (184 cases), own benchmark, GSM8K + tau-bench, clean controls"],
    ["Model / algorithm / technology choices", "Slides 4, 9", "ErrorProbe as baseline; constraint-based SED over LLM-judge; stack listed on S9"],
    ["Expected results", "Slide 8", "Pre-registered acceptance band; 4 success bands (Failure/Acceptable/Strong/Exceptional)"],
    ["Final product", "Slide 6", "Docker + pip-installable SDK — \"operable by someone who didn't build it\""],
    ["Innovation / novelty", "Slide 3, 6", "Combination no other system/paper/prior FYP has: attribution + SED + verified repair + cross-arch"],
    ["Comparison with existing solutions", "Slide 3", "ErrorProbe, LangSmith Engine/Arize Alyx, Langfuse family, closest prior FYP — one table"],
    ["Feasibility", "Slide 5, 7", "9-characteristic CCP self-rating; the \"could AI build this in a week\" resilience test; real POC evidence"],
    ["Cost / budget", "Slide 9", "$0 committed (local model); paid alternative (~$353–$881) priced and declined, on record"],
    ["Work division among team members", "Slides 9, 10", "Per-member ownership + \"if removed\" test; shared responsibilities named separately"],
    ["Timeline", "Slide 9", "5 gates (Proposal → Mid-1 → Final-1 → Mid-2 → Final-2); 1,130-hour effort budget"],
    ["Risks and limitations", "Slides 5, 8", "Characteristic 6 held honestly weak; 4 named risks each with a stated fallback"],
    ["DEI statement", "Slide 10", "Open-source access equity; colour-plus-text accessibility; English-only scope named honestly"],
    ["Ethical / legal compliance", "Slide 10", "Advisory-only repairs; consent for real trace data; MIT/CC BY 4.0 licensing confirmed"],
    ["AI-assisted development disclosure", "Slide 10", "Level 2 named and justified per handbook C.8; logged per session, Form 13"],
    ["Prior-FYP / departmental comparison", "Slide 3", "660 titles across every cohort since 2019, checked structurally — closed, not left blank"],
]
story.append(table(checklist_rows, [0.24, 0.14, 0.62], bold_first_col=True))

story.append(PageBreak())

# ============================================================ 6. Q&A =======
story.append(P("6. Comprehensive Q&amp;A Preparation", "H1"))
story.append(P(
    "Organized from the questions every panel opens with, through to the ones designed to end a weak "
    "defense. Rehearse the challenging section hardest — those are the ones a panel actually uses to "
    "decide.", "Body"
))

story.append(P("6.1 Basic / Expected Questions", "H2"))

story.append(qa(
    "What is the problem you're solving?",
    "When AI agents work together and one of them fails, current tools can't reliably say which agent "
    "caused it — and none of them can catch a wrong answer that looks completely correct, or check "
    "whether a proposed fix would actually work before you trust it.",
    "Lead with the sentence on slide 1 — it's built to answer this in one breath."
))
story.append(qa(
    "Why is this problem important?",
    "Multi-agent AI systems are already moving into real production use — customer support, coding "
    "assistants, research tools. A silent failure in one of these ships a wrong answer with zero "
    "warning sign. That's not a hypothetical; it's the specific failure mode current tools cannot catch.",
    "Anchor to SDG 9 and \"ships a confident, wrong answer — no crash, no signal\" from slide 2."
))
story.append(qa(
    "Why did you choose this topic?",
    "We read the recent literature on multi-agent failure diagnosis and found a specific, confirmed "
    "gap: the strongest published method admits it can't catch silent failures and has never been "
    "tested outside two agent frameworks. That's a real, evidenced opening, not a topic we picked "
    "because it sounded interesting.",
    "Point to the accuracy lineage (14.2% → ~40% → 59.5%) as proof this is an active, fast-moving area."
))
story.append(qa(
    "What exactly are you building?",
    "A diagnosis-and-repair layer that sits on top of a multi-agent system: it finds which agent and "
    "step caused a failure, catches failures that show no error signal at all, generates and tests a "
    "fix before trusting it, and ships as an installable SDK, not a one-off script.",
    "Say \"layer on top of,\" not \"replacement for\" — it complements existing trace-capture tools."
))
story.append(qa(
    "Who benefits from this, specifically?",
    "The primary user is an engineering team running a multi-agent system in or near production. "
    "Downstream, product teams benefit from fewer undetected wrong answers reaching users, and "
    "auditors benefit from traceable evidence of what happened and why.",
    "Three named beneficiaries on slide 2 — primary and two secondary."
))
story.append(qa(
    "What makes your solution different from just asking an AI model what went wrong?",
    "Pasting a trace into a chatbot gives you one unbenchmarked opinion with no ground truth. Ours is "
    "a fault-injection harness that creates cases where the true cause is known by construction, so "
    "accuracy is a measured number; a rule-based checker that catches silent failures with zero model "
    "calls; and a replay mechanism that actually tests a fix before anyone trusts it.",
    "The field's own baseline for \"just ask a model\" is 14.2% — that's the number a chatbot answer "
    "loses to by 45 points."
))

story.append(P("6.2 Technical / Methodology Questions", "H2"))

story.append(qa(
    "What is your research gap, precisely?",
    "Not one missing feature — a missing combination. No paper, product, or prior project we checked "
    "combines published step-level attribution accuracy, general silent-failure detection, verified "
    "counterfactual fix-testing, and cross-framework generalization, all in one evaluated pipeline.",
    "Say \"the gap is the combination\" — this is the single line to repeat if pressed."
))
story.append(qa(
    "Why did you choose ErrorProbe as your baseline instead of a newer method?",
    "We chose it on measured performance, not recency — it's the strongest published step-accuracy "
    "number in the literature we reviewed, at 59.5%.",
    "\"On performance, not recency\" is the exact phrase from slide 4 — use it."
))
story.append(qa(
    "Why CrewAI and LangGraph specifically?",
    "Because neither was used by any of the seven papers we reviewed. Testing on frameworks the method "
    "was never tuned on is the actual test of whether it generalizes — that's the whole point of the "
    "claim.",
    "This is also why a market survey's advice to narrow to one framework was explicitly declined."
))
story.append(qa(
    "Why a rule-based checker instead of using an AI model to judge outputs?",
    "The literature shows an AI model judging another AI model's output for this kind of silent "
    "failure performs barely above chance — the reported figure is an AUROC of about 0.65. A "
    "deterministic, rule-based check is falsifiable and auditable in a way an AI-judging-AI approach "
    "isn't.",
    "\"Barely above chance\" is the phrase to use — it pre-empts \"why not just use a bigger model.\""
))
story.append(qa(
    "What datasets are you using, and why these?",
    "Who&amp;When for baseline reproduction (184 real cases, already in hand), plus our own new "
    "benchmark built on GSM8K and tau-bench, including deliberately clean, non-broken control cases "
    "so we can measure a false-positive rate — something no paper we reviewed reports.",
    "Naming the false-positive-rate gap unprompted is a strong, specific point most panels won't expect."
))
story.append(qa(
    "How will you evaluate the system, concretely?",
    "Agent and step accuracy, how far an error spreads through the agents, silent-failure precision "
    "and recall, false-positive rate on clean runs, task completion and repair success rates, and "
    "latency overhead — measured with bootstrap confidence intervals, fixed seeds, and repeated "
    "replays, not a single run.",
    "All five metric groups are listed on slide 8 — recite the list, don't paraphrase loosely."
))
story.append(qa(
    "What are your success metrics, exactly?",
    "Four pre-registered bands. Failure means missing our accuracy band with no improvement anywhere. "
    "Acceptable means at least parity with the published baseline plus a cross-architecture result. "
    "Strong means beating the baseline with over 70% silent-failure accuracy. Exceptional adds over "
    "50% verified-repair recovery on top of Strong.",
    "These were written before any result exists — say that explicitly; it's the whole point."
))
story.append(qa(
    "How will multi-agent systems actually be diagnosed and repaired, step by step?",
    "The target system runs, we capture its trace, build a dependency graph from it, then run two "
    "checks in parallel: a backward trace to find the responsible agent and step, and our constraint "
    "checker for silent failures. Once a cause is found, a repair candidate is generated and "
    "re-executed under a controlled replay before it's ever reported as verified.",
    "\"In parallel\" is important — the silent-failure check never waits on the attribution result."
))
story.append(qa(
    "What happens if the repair doesn't actually fix the problem?",
    "It's never applied automatically in the first place — every repair is advisory and gated behind "
    "a human. The controlled replay measures a recovery rate across repeated runs before anything is "
    "even proposed as trustworthy, and if it fails, that's reported honestly, not hidden.",
    "\"Advisory, human-gated\" ties directly to the ethics statement on slide 10."
))

story.append(P("6.3 Challenging / Skeptical Questions", "H2"))

story.append(qa(
    "Your title says self-healing and recovery — show me the evidence. Isn't one of these components "
    "unbuilt and the other already failed?",
    "Fair question, and we'd rather say it ourselves than have it found. Recovery Controller has no "
    "proof-of-concept yet and Verified Repair Memory's one real test did fail — both carry pre-"
    "registered gates at Mid-1, decided before any result exists, each with a stated fallback that "
    "still keeps the loop closed either way. Six of our other core mechanisms already have real "
    "evidence behind them.",
    "Lead with this unprompted, don't wait to be asked — concealment reads far worse than an honest "
    "gate."
))
story.append(qa(
    "This looks like three separate projects — reproduction, a new benchmark, and a product — for "
    "three people in one year. Isn't that too much?",
    "They're one pipeline, not three projects — the benchmark feeds the diagnosis engine, and the SDK "
    "is the packaging of that same engine. The budget is real and specific: 1,130 planned hours "
    "against 1,130 hours of actual combined capacity, scheduled across five gates.",
    "Cite the exact hour figure — a specific number beats a reassurance every time."
))
story.append(qa(
    "Your reproduction only reached 13.2% step accuracy versus ErrorProbe's published 59.5%. Isn't "
    "your whole comparison built on a baseline you can't even reproduce?",
    "That number is from a deliberately minimal early spike — a simplified version, run five "
    "independent times specifically to prove the approach produces real signal before spending more "
    "effort, and it did: 71.4% agent accuracy on average. The full reproduction is scheduled with a "
    "pre-registered ten-point acceptance band, and if it lands outside that band, both numbers get "
    "reported side by side, exactly as the handbook allows for a faithful reproduction. Either outcome "
    "is a real result — only staying silent about a gap would be a failure.",
    "Never say \"we'll get a better number\" — say \"either outcome is reported honestly.\""
))
story.append(qa(
    "LangSmith and Arize already shipped automated diagnosis this year, built by teams far bigger than "
    "yours. Aren't you just rebuilding a funded product?",
    "We checked both directly and corrected our own earlier positioning when we found them — that's on "
    "our own record. What neither confirms, as documented capability: a published accuracy number on "
    "any benchmark, general silent-failure detection, counterfactual fix-testing with a measured "
    "recovery rate, or anything that isn't locked to their own platform. That combination, measured "
    "and published, is what we're actually contributing.",
    "\"We checked and corrected our own claim\" lands better than defending the original assumption."
))
story.append(qa(
    "Rule-based detection of \"semantic\" errors sounds like a contradiction — either your rules only "
    "check surface formatting, which is trivial, or you're claiming rules understand meaning, which is "
    "impossible. Which is it?",
    "Neither extreme. We scope the claim precisely: where a task's own specification yields a "
    "checkable constraint — a numeric total that must match, a policy rule that must hold — a "
    "deterministic check catches violations of it, including a genuinely subtle near-miss we caught "
    "in testing. Where no such constraint exists, the system abstains rather than guessing, and we "
    "report that abstention rate as its own metric instead of hiding it.",
    "\"Abstains and reports it\" is the exact answer that defuses this — memorize the phrase."
))
story.append(qa(
    "Couldn't a capable student with AI assistance build this whole thing in a couple of weeks?",
    "A stripped wrapper — capture a trace, ask a model what went wrong — yes, in about a week. What "
    "that version would get wrong is exactly what carries the marks: no benchmark tested on an "
    "unfamiliar framework, no way to distinguish a silent failure from a correct answer, no measured "
    "false-positive rate, and zero proof any suggested fix works. That's where our actual difficulty "
    "sits.",
    "This is verbatim the handbook's own resilience test (C.7) — answer it in the handbook's own terms."
))
story.append(qa(
    "You're evaluating your own system against a benchmark you built yourselves. Isn't that grading "
    "your own homework?",
    "Ground truth constructed by controlled fault injection — where you already know the true origin "
    "point because you injected it — is the field's own established method; ErrorProbe and AgenTracer "
    "both do the same thing. What makes it realistic is that the underlying tasks come from unmodified "
    "public sources — Who&amp;When, GSM8K, tau-bench — not tasks we wrote ourselves to be easy to "
    "solve.",
    "Name the two datasets and stress \"unmodified\" — that's what makes it not self-serving."
))
story.append(qa(
    "What if, six months from now, someone publishes a paper that does exactly what you're proposing?",
    "A real, named risk we track openly, checked at every project gate. If it happens, we'd report it "
    "honestly as a finding rather than hide it — and the benchmark and the deployable tool we build "
    "stay valuable either way, since a single competing paper wouldn't replace either.",
    "Don't claim it can't happen — claim you're watching for it and have a real answer if it does."
))
story.append(qa(
    "What's the weakest part of your entire proposal, in your own words?",
    "Two committed mechanisms — Recovery Controller and Verified Repair Memory — carry the thinnest "
    "evidence: one has no proof-of-concept at all yet, and the other's one real test failed. We "
    "named both ourselves, gave each a pre-registered pass/fail test at Mid-1, and a recorded fallback "
    "either way, rather than waiting for a panel to find them.",
    "Answering this unprompted, specifically, is worth more credibility than any slide."
))

story.append(P("6.4 \"Do You Actually Understand Your Own System\" Questions", "H2"))

story.append(qa(
    "Explain, without notes, exactly what your own subsystem does and what breaks if it's removed.",
    "Each team member should be able to answer this live, unaided, using the exact \"if removed\" line "
    "already written for their own lane on slide 9 — Shahoud: no cross-architecture benchmark, "
    "Noor: no attribution algorithm or silent-failure detection, Saif: nothing installable outside "
    "the development machine.",
    "This is a live spoken test, not a document question — the only way to prepare is to rehearse it "
    "out loud, alone, from memory."
))
story.append(qa(
    "If I asked you to swap out the underlying AI model for a different one, what would actually "
    "break?",
    "Almost nothing that matters to our core claim. Roughly 80–85% of the components — the graph "
    "construction, the causal tracing, the constraint checking, the confidence scoring — never call "
    "an AI model at all, so they're byte-identical either way. Only the agent's own behavior, the "
    "repair generation, and the replay's re-execution step touch a model.",
    "This is the \"replacement test\" from the handbook's external-component rule — know the ~15–20% "
    "figure cold."
))
story.append(qa(
    "Why is the ability to say a repair 'recovered' the system meaningfully different from just "
    "re-running it and hoping?",
    "Because the correction is re-executed under a controlled protocol — everything before the fix "
    "stays frozen, decoding settings are pinned — repeated multiple times specifically because model "
    "output isn't perfectly repeatable, and the result is a measured recovery rate across those runs, "
    "not a single lucky pass.",
    "Say \"controlled, not deterministic\" unprompted — it's the exact phrase the team already flagged "
    "as needing to be said before being asked."
))

story.append(PageBreak())

# ============================================================ 7. TIPS ======
story.append(P("7. Final Last-Minute Defense Tips", "H1"))
tips = [
    "Lead with weaknesses you already know about — the two gated Tier-2 mechanisms, characteristic 6 "
    "held honestly weak, Spike 7's negative result. Saying it first reads as rigor; having it found "
    "reads as concealment.",
    "When a number appears on a slide, know which spike or document it came from and offer to open it "
    "live. Every number in this deck is real and traceable — use that as a strength, not just a fact.",
    "Rehearse the two transition lines out loud with the next presenter until the handoff feels "
    "natural, not read. A visible, confident handoff signals a genuinely integrated team.",
    "Don't read slide 5's nine CCP characteristics one by one — point at the grid and speak the "
    "bottom summary band instead, exactly as the slide's own notes say.",
    "If asked something outside your own slides, it's fine to say \"that's [teammate]'s subsystem — "
    "[name], can you take that?\" A clean handoff is stronger than a guessed answer.",
    "Time yourself at home at least twice, out loud, with a visible clock. The written timing plan is "
    "a guide, not a guarantee — your own natural pace is what actually counts on the day.",
    "If a question challenges something genuinely unresolved (stakeholder contact, the two Tier-2 "
    "gates), answer with the real, current status — never imply something is done when it isn't.",
    "Breathe before answering a hard question. A three-second pause reads as thinking; a rushed, "
    "defensive answer reads as unprepared.",
]
story.append(ListFlowable(
    [ListItem(P(t, "Body")) for t in tips],
    bulletType="bullet",
))

story.append(Spacer(1, 16))
story.append(HRFlowable(width=PAGE_WIDTH, thickness=1, color=LINE))
story.append(Spacer(1, 8))
story.append(P(
    "Good luck, Team Granite. Every claim in this document traces back to a real file in your own "
    "repository — that's the actual advantage walking into the room.", "Small"
))

# ============================================================ build =======
doc = SimpleDocTemplate(
    "Granite_Speaking_Notes_and_QA.pdf",
    pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm,
    title="Granite — Speaking Notes and Q&A", author="Team Granite",
)
doc.build(story)
print("PDF written: Granite_Speaking_Notes_and_QA.pdf")
