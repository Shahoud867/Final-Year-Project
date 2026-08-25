"""
Generates the Seoul Accord D.4.1 Complex Computing Problem justification
as a .docx, for the FYP registration form's CCP section.
Answers grounded in the project's own evidence (POC spikes, literature/market
checks) already assembled in FYP_Scope_CCP_and_Implementation_Plan.md §2 and
the supervisor briefing PDF/artifact — not written fresh from scratch.
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

INK = RGBColor(0x1a, 0x1a, 0x2e)
ACCENT = RGBColor(0x1e, 0x7a, 0x8c)
MUTED = RGBColor(0x66, 0x66, 0x66)
GOOD = RGBColor(0x2f, 0x7a, 0x2f)
WARN = RGBColor(0xa8, 0x68, 0x1a)

doc = Document()

# --- base style ---
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(10.5)
for section in doc.sections:
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)

def shade_cell(cell, hex_color):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    cell._tc.get_or_add_tcPr().append(shd)

def title(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = INK
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

def subtitle(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(12)
    r.font.color.rgb = MUTED
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

def h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = INK

def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = ACCENT

def body(text, bold=False, italic=False, size=10.5, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    if color:
        r.font.color.rgb = color
    return p

def option_line(text, selected=False):
    p = doc.add_paragraph(style=None)
    p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.space_after = Pt(2)
    mark = "☑  " if selected else "☐  "
    r = p.add_run(mark + text)
    r.font.size = Pt(10)
    if selected:
        r.font.bold = True
        r.font.color.rgb = GOOD
    else:
        r.font.color.rgb = MUTED

def divider():
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:color"), "CCCCCC")
    pBdr.append(bottom)
    pPr.append(pBdr)

# ============================================================
# TITLE PAGE
# ============================================================
doc.add_paragraph().paragraph_format.space_before = Pt(40)
title("Granite")
subtitle("Complex Computing Problem Justification")
subtitle("Per Seoul Accord Sections D.4.1 and D.4.2")
body("")
body("Prepared 2026-08-23, updated 2026-08-24. Every selection below is drawn from "
     "evidence already on record in this project — 8 run POC spikes, a 9+ paper "
     "literature review, a 7-platform commercial market check, and a second market "
     "survey covering 7 orchestration frameworks — not asserted without support.",
     italic=True, color=MUTED)

doc.add_page_break()

# ============================================================
# INTRO
# ============================================================
h1("How to read this document")
body(
    "For each of the 9 characteristics in Seoul Accord D.4.1 (Range of Problem "
    "Solving), the three tiered descriptions from the accord are reproduced "
    "exactly as published, the tier that best describes Granite is checked, "
    "and a justification grounded in this project's own evidence follows. One "
    "characteristic (#6, stakeholder involvement) is honestly rated at the "
    "middle tier, not the top one — see its justification for why, and what "
    "would need to happen to raise it."
)

doc.add_page_break()

# ============================================================
# THE 9 CHARACTERISTICS
# ============================================================

characteristics = [
    {
        "n": 1,
        "name": "Range of conflicting requirements",
        "options": [
            "Involves wide-ranging or conflicting technical, computing, and other issues",
            "Involves a variety of factors, which may impose conflicting constraints",
            "Involves several issues, but with few of these exerting conflicting constraints",
        ],
        "selected": 0,
        "justification": (
            "Granite has three real, unresolved tensions baked into its own design, not "
            "hypothetical ones: (1) diagnostic depth vs. latency — the full 3-stage "
            "attribution pipeline (Culprit Agent, Error Step Localization, Verification "
            "Agent) is more accurate than a single-pass method but costs more inference "
            "time per diagnosis, and the product must expose this trade-off as a "
            "configuration choice, not hide it; (2) trace completeness vs. privacy — "
            "accurate attribution needs full execution traces, which conflicts directly "
            "with data-minimization and privacy requirements for any team handling real "
            "user data (the project's own R16 threat model exists precisely because of "
            "this conflict); (3) generalization vs. specialization — the cross-"
            "architecture claim (working on CrewAI, LangGraph, and a 3rd framework with "
            "no per-framework tuning) trades away the accuracy a framework-specific tool "
            "could achieve by hard-coding assumptions about one orchestration paradigm."
        ),
    },
    {
        "n": 2,
        "name": "Depth of analysis required",
        "options": [
            "Has no obvious solution, and requires conceptual thinking and innovative analysis to formulate suitable abstract models",
            "Can be solved by application of well-proven analysis techniques",
            "Can be solved in standardized ways",
        ],
        "selected": 0,
        "justification": (
            "The strongest published method in this exact space, ErrorProbe (ACL 2026), "
            "still only reaches 59.5% step-level attribution accuracy — after Who&When "
            "(ICML 2025) opened the problem and at least 7 papers spent roughly 15 months "
            "actively working on it. If a well-proven, standardized analysis technique "
            "existed, that number would not still be under 60% after this much sustained "
            "research effort. Solving it required building a new abstract model from "
            "scratch — representing multi-agent execution as a causal graph, defining "
            "counterfactual re-execution semantics, and formulating silent-failure "
            "detection as task-constraint verification rather than anomaly detection "
            "— none of which existed as an off-the-shelf technique to apply. Updated "
            "2026-08-24 with a second data point: Verified Repair Memory, a mechanism "
            "recommended independently by an external market survey, was built and "
            "tested once and failed outright (0 of 8 cases committed, local 3B backbone) "
            "— even the piece of this problem that sounds simplest (remember a fix that "
            "worked before) turned out to have no obvious solution either."
        ),
    },
    {
        "n": 3,
        "name": "Depth of knowledge required",
        "options": [
            "A solution requires the use of in-depth computing or domain knowledge and an analytical approach that is based on well-founded principles",
            "A solution requires knowledge of principles, and applied procedures or methodologies",
            "Can be resolved using limited theoretical knowledge, but normally requires substantial practical knowledge",
        ],
        "selected": 0,
        "justification": (
            "The committed core draws on multiple genuinely graduate-level areas at once: "
            "execution-graph and causal-graph modeling (including cycle detection and "
            "bounded backward tracing, proven in Spike 6), distributed tracing across "
            "asynchronous multi-agent systems, counterfactual/causal reasoning for the "
            "replay engine (proven in Spike 5), and constraint-based semantic verification "
            "for the silent-failure module. None of this is standard undergraduate "
            "coursework application — it required reproducing a peer-reviewed paper's "
            "own 3-stage architecture (Strategist → Investigator → Arbiter) from "
            "its description alone, since ErrorProbe's code is not publicly available."
        ),
    },
    {
        "n": 4,
        "name": "Familiarity of issues",
        "options": [
            "Involves infrequently-encountered issues",
            "Belongs to families of familiar problems, which are solved in well-accepted ways; context may be unfamiliar",
            "Is frequently encountered and thus familiar to most practitioners in the field; context may be unfamiliar",
        ],
        "selected": 0,
        "justification": (
            "Silent failures — an output that is well-formed and passes every standard "
            "error check, yet is semantically wrong — are, by construction, invisible "
            "to the error-handling patterns most practitioners already know (try/catch, "
            "schema validation, HTTP status codes). Spike 4's own natural-occurrence test "
            "(n=3 real tasks) found zero naturally-occurring silent failures on the first "
            "attempt, which is itself evidence of how infrequently this failure class "
            "surfaces in ordinary testing — it has to be deliberately induced (fault "
            "injection) or specifically watched for, not stumbled into. Cross-architecture "
            "generalization of a diagnosis method is similarly uncommon: the 7-paper "
            "literature review found no prior method tested outside its own benchmark's "
            "architecture."
        ),
    },
    {
        "n": 5,
        "name": "Level of problem",
        "options": [
            "Is outside problems encompassed by standards and standard practice for professional computing",
            "May be partially outside those encompassed by standards or standard practice",
            "Is encompassed by standards and/or documented procedures of practice",
        ],
        "selected": 0,
        "justification": (
            "No documented industry standard or accepted procedure exists for diagnosing "
            "multi-agent AI failures, verifying a fix's recovery rate before applying it, "
            "or generally detecting silent failures — this was confirmed directly, not "
            "assumed, by checking all 7 major commercial observability platforms "
            "(LangSmith, Langfuse, Braintrust, Arize, Maxim AI, Opik, DeepEval). Two "
            "(LangSmith Engine, Arize Alyx) have only just begun shipping automated "
            "diagnosis features in 2026, and none document counterfactual fix-testing "
            "with a measured recovery rate or general silent-failure detection as a "
            "standardized, published capability. The practice is actively forming, not "
            "settled."
        ),
    },
    {
        "n": 6,
        "name": "Extent of stakeholder involvement and level of conflicting requirements",
        "options": [
            "Involves diverse groups of stakeholders with widely varying needs",
            "Involves several groups of stakeholders with differing and occasionally conflicting needs",
            "Involves a limited range of stakeholders with differing needs",
        ],
        "selected": 1,
        "justification": (
            "Honestly rated at the middle tier, not the top one — this is the one "
            "characteristic the project's own CCP review (plan doc §2) marks as "
            "“weak” rather than “clear.” Several real stakeholder groups are "
            "identified in principle, each with differing needs (on-call engineers/SREs "
            "wanting fast, trustworthy diagnosis; benchmark researchers wanting a "
            "reproducible, labeled evaluation artifact; QA/compliance teams wanting "
            "silent-failure coverage; platform teams wanting low integration cost) — "
            "but none of these stakeholder groups have actually been contacted or "
            "interviewed yet. Claiming the top tier (“diverse groups... widely varying "
            "needs”) without real stakeholder engagement would be an overclaim the rest "
            "of this project has deliberately avoided everywhere else. This is the single "
            "highest-priority open item before defense (risk-register.md, and item #10 "
            "in the guide-compliance checklist)."
        ),
    },
    {
        "n": 7,
        "name": "Consequences",
        "options": [
            "Has significant consequences in a range of contexts",
            "Has consequences that are important locally, but may extend to a broader context",
            "Has consequences that are important locally, and usually are not far-reaching",
        ],
        "selected": 0,
        "justification": (
            "A missed silent failure means a multi-agent AI system ships an incorrect "
            "answer to a real end user with no visibility that anything went wrong at "
            "all — by definition, no error signal fires. The scenarios used throughout "
            "this project's own use-case analysis span multiple real domains where this "
            "matters: a wrong refund amount in customer support, an unverified budget "
            "constraint in a purchase recommendation, a stock-count inconsistency between "
            "two agents in the same order pipeline. These are not confined to one "
            "narrow context — they recur in any production deployment of multi-agent "
            "systems, which is precisely why 7 commercial platforms have independently "
            "converged on this as a category worth building tooling for."
        ),
    },
    {
        "n": 8,
        "name": "Interdependence",
        "options": [
            "Is a high-level problem possibly including many component parts or sub-problems",
            "Is part of, or systems within, a complex computing problem",
            "Is a discrete component of a computing system",
        ],
        "selected": 0,
        "justification": (
            "The system itself decomposes into multiple interdependent sub-problems, each "
            "substantial enough to be its own line of work: fault injection across "
            "frameworks, execution-graph construction, three separate attribution stages "
            "(Culprit Agent, Error Step Localization, Verification Agent), silent-failure "
            "constraint verification, and counterfactual replay — and the subject "
            "matter itself is interdependence: failures in a real multi-agent system "
            "propagate through interdependent agent sub-tasks, which is exactly what the "
            "Failure Propagation Map and backward causal tracing (Spike 6, proven on a "
            "real cyclic graph) are built to model and trace."
        ),
    },
    {
        "n": 9,
        "name": "Requirement identification",
        "options": [
            "Identification of a requirement or the cause of a problem is ill defined or unknown",
            "Identification of a requirement or the cause of a problem is possible from a set of known options",
            "A requirement or the cause of a problem can be determined by well-established ways",
        ],
        "selected": 0,
        "justification": (
            "This is the literal definition of the core problem Granite solves: at the "
            "moment a multi-agent system produces a wrong result, the responsible agent, "
            "the responsible step, and the reason are all unknown and must be actively "
            "investigated — there is no well-established way to determine this, which "
            "is exactly why the field's best published method (ErrorProbe) only reaches "
            "59.5% accuracy at identifying it. The entire 3-stage attribution pipeline "
            "(hypothesis generation, evidence-grounded verification, arbitration) exists "
            "because the cause is not knowable from a fixed set of known options — it "
            "has to be inferred and then verified against real trajectory evidence. "
            "Updated 2026-08-24: Recovery Controller (resuming a workflow specifically "
            "from a verified repair point, not just any checkpoint) was added to the "
            "committed core the same day with zero POC evidence — an honest admission "
            "that this specific mechanism's difficulty is still genuinely unknown, not "
            "already solved and merely unbuilt."
        ),
    },
]

for c in characteristics:
    h1(f"{c['n']}. {c['name']}")
    for i, opt in enumerate(c["options"]):
        option_line(opt, selected=(i == c["selected"]))
    h2("Justification")
    body(c["justification"])
    divider()

doc.add_page_break()

# ============================================================
# OVERALL JUSTIFICATION
# ============================================================
h1("Justify your selection — overall")
body(
    "Granite meets the “Complex” tier on 8 of 9 D.4.1 characteristics, with "
    "stakeholder involvement honestly rated at the middle tier until real stakeholder "
    "feedback is obtained — not inflated to match the others. This is backed by 8 "
    "independently reproduced proof-of-concept experiments (fault injection, "
    "execution-graph construction, silent-failure detection, counterfactual replay, "
    "cyclic-graph handling, ErrorProbe reproduction, a preventive classifier — an "
    "honest negative result, reported rather than hidden — and a Repair Agent spike "
    "run 2026-08-24 with a real 4-of-6 success rate and a precisely diagnosed cause "
    "for the 2 failures), a review of 9+ relevant research papers spanning the field's "
    "entire published history on this problem (Who&When, AgenTracer, SDBL, "
    "TraceElephant, ErrorProbe, AgentAsk, PROTEA, plus a further literature triage), "
    "and checks of two separate market layers — 7 major commercial observability "
    "platforms, and, added 2026-08-24, a second independent survey of 7 agentic AI "
    "orchestration frameworks (OpenAI Agents SDK, LangGraph, CrewAI, Google ADK, "
    "Microsoft Agent Framework, Amazon Bedrock AgentCore, BabyAGI) confirming the "
    "same gap from the framework-vendor side, not just the tooling side. Together, "
    "the evidence shows a clear research gap: the best reported step-level "
    "attribution accuracy is only 59.5%, neither market layer provides standardized "
    "silent-failure detection or counterfactual fix-verification, and no prior method "
    "has been tested across multiple multi-agent architectures. The evidence is not "
    "static, either — reviewing that second survey on 2026-08-24 itself surfaced a "
    "real, previously-missed gap (Repair Agent, now built and tested) and two more "
    "committed items (Recovery Controller, Verified Repair Memory) that are honestly "
    "carried with zero POC evidence and one real test failure respectively, not "
    "smoothed over to look more finished than they are. These findings strongly "
    "support Granite as a genuinely challenging and underexplored problem — one "
    "that keeps proving harder than it looks even as the project's own understanding "
    "of it deepens, which is itself evidence for “no obvious solution,” not against it."
)

doc.save("Granite_CCP_Justification.docx")
print("DOCX written: Granite_CCP_Justification.docx")
