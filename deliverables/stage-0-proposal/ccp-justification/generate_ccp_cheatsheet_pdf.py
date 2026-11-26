"""
Generates Granite_CCP_Cheatsheet.pdf — a one-page, 9-card rehearsal
cheat sheet for the Seoul Accord CCP characteristics, condensed from
FYP_Scope_CCP_and_Implementation_Plan.md §2 (the source of truth: 8 clear,
1 weak). Landscape A4, everything on a single page by design.
"""
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer

INK = HexColor("#1d1a15")
INK2 = HexColor("#5c5449")
GOLD = HexColor("#a96a1f")
GOLD2 = HexColor("#8a5417")
GOLD_SOFT = HexColor("#f5ead9")
AMBER = HexColor("#93701a")
AMBER_SOFT = HexColor("#f4eeda")
BORDER = HexColor("#e8e1d4")
BORDER2 = HexColor("#d9cfbc")
CARDBG = HexColor("#fdfbf7")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CSTitle", fontSize=18, leading=21, textColor=INK, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Sub", fontSize=9.5, leading=12.5, textColor=INK2))
styles.add(ParagraphStyle(name="CardNum", fontSize=10, leading=12, textColor=colors.white, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CardName", fontSize=12, leading=14.5, textColor=INK, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Lbl", fontSize=7.4, leading=9, textColor=GOLD2, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Body", fontSize=8.6, leading=11, textColor=INK))
styles.add(ParagraphStyle(name="Say", fontSize=8.6, leading=11, textColor=GOLD2, fontName="Helvetica-Oblique"))
styles.add(ParagraphStyle(name="WeakTag", fontSize=7.4, leading=9, textColor=AMBER, fontName="Helvetica-Bold"))

def P(t, s="Body"):
    return Paragraph(t, styles[s])

# (num, name, weak?, plain, example, say)
DATA = [
 (1, "Conflicting requirements", False,
  "Two good things fight each other.",
  "Depth vs. speed; a full trace helps diagnosis, but a full trace risks privacy.",
  "&ldquo;We can&rsquo;t max out both at once.&rdquo;"),
 (2, "No obvious solution", False,
  "Top researchers haven&rsquo;t solved it well.",
  "Best published method still wrong 4/10, after 15 months and 7 papers.",
  "&ldquo;If it were easy, someone&rsquo;d be at 95%. Nobody is.&rdquo;"),
 (3, "Depth of knowledge", False,
  "Needs several specialist skills at once.",
  "Graph modeling + causal reasoning + AI-evaluation method &mdash; combined.",
  "&ldquo;Not one skill &mdash; three, together.&rdquo;"),
 (4, "Unfamiliar issues", False,
  "Problems you can&rsquo;t just look up.",
  "Same question to the same agent can give two different answers.",
  "&ldquo;That breaks how software is normally tested.&rdquo;"),
 (5, "Beyond standard practice", False,
  "No existing tool does this.",
  "No framework does attribution + silent-failure detection + repair together.",
  "&ldquo;We had to build all three ourselves.&rdquo;"),
 (6, "Diverse stakeholders", True,
  "Different people, different needs.",
  "Engineer wants the culprit; product team wants ship/no-ship; auditor wants proof.",
  "&ldquo;We just haven&rsquo;t talked to real ones yet.&rdquo;"),
 (7, "Significant consequences", False,
  "If it&rsquo;s wrong, it actually matters.",
  "Agents already run support &amp; write code &mdash; a silent failure ships undetected.",
  "&ldquo;Not hypothetical &mdash; already in production.&rdquo;"),
 (8, "Interdependence", False,
  "One part&rsquo;s mistake spreads to the rest.",
  "Agent 1&rsquo;s small error feeds into Agent 2, then Agent 3&rsquo;s work.",
  "&ldquo;One mistake becomes every downstream agent&rsquo;s problem.&rdquo;"),
 (9, "Ill-defined cause", False,
  "You don&rsquo;t know what you&rsquo;re looking for yet.",
  "Don&rsquo;t know IF it failed, WHICH agent, or WHAT was correct.",
  "&ldquo;Three unknowns, stacked at once.&rdquo;"),
]

def card(num, name, weak, plain, example, say):
    numbadge = Table([[P(str(num), "CardNum")]], colWidths=[1.7*cm], rowHeights=[0.6*cm])
    numbadge.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AMBER if weak else GOLD),
        ("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    header_cells = [numbadge, P(name, "CardName")]
    if weak:
        header_cells.append(P("STILL\nDEVELOPING", "WeakTag"))
    head = Table([header_cells], colWidths=[1.7*cm, None, 2.3*cm] if weak else [1.7*cm, None])
    head.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 3), ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    body = [
        head, Spacer(1, 5),
        P("PLAIN", "Lbl"), P(plain, "Body"), Spacer(1, 4),
        P("EXAMPLE", "Lbl"), P(example, "Body"), Spacer(1, 4),
        P("SAY", "Lbl"), P(say, "Say"),
    ]
    t = Table([[body]], colWidths=[8.7*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AMBER_SOFT if weak else CARDBG),
        ("BOX", (0,0), (-1,-1), 1, AMBER if weak else BORDER2),
        ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 9), ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    return t

# ---- assemble 3x3 grid ----
cards = [card(*d) for d in DATA]
grid_rows = [cards[0:3], cards[3:6], cards[6:9]]
grid = Table(grid_rows, colWidths=[9.0*cm]*3)
grid.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 0), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
]))

story = []
title_row = Table([[
    P("Granite &mdash; CCP Cheat Sheet", "CSTitle"),
    P("Seoul Accord, 9 characteristics &middot; 8 clear, 1 held-honestly-weak &middot; F26-060", "Sub"),
]], colWidths=[9*cm, None])
title_row.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"BOTTOM"), ("ALIGN",(1,0),(1,0),"RIGHT")]))
story.append(title_row)
story.append(Spacer(1, 9))
story.append(grid)
story.append(Spacer(1, 4))
story.append(P(
    "Full reasoning: <b>FYP_Scope_CCP_and_Implementation_Plan.md</b> §2 (source of truth) &middot; "
    "held-back-4 detail: <b>defense-prep/CCP_and_Spikes_Full_Reasoning.md</b> &middot; "
    "formal write-up: <b>Granite_CCP_Justification_Seoul_Accord.docx</b>", "Sub"
))

doc = SimpleDocTemplate(
    "Granite_CCP_Cheatsheet.pdf",
    pagesize=landscape(A4),
    leftMargin=1.1*cm, rightMargin=1.1*cm, topMargin=1.0*cm, bottomMargin=1.0*cm,
    title="Granite — CCP Cheat Sheet", author="Team Granite",
)
doc.build(story)
print("PDF written: Granite_CCP_Cheatsheet.pdf")
