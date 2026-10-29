"""
Generate the CS637 academic research presentation using Gamma's Minimal aesthetic:
- Clean, pure white / ivory backgrounds (#FFFFFF / #FDFDFE).
- Charcoal / deep slate typography (#0F172A / #1E293B / #334155).
- Single restrained accent color: Deep Academic Teal (#0F766E).
- Hairline architectural dividers (#E2E8F0, 0.75 pt) and subtle tint surfaces.
- Generous whitespace, strong typographic contrast, NO repeated rounded-rectangle cards.
- 18 comprehensive, mathematically verified slides covering all requirements 1-to-1:
    Slide 1: Title slide
    Slide 2: Why scheduling matters (Practical Motivation & Industrial Drivers)
    Slide 3: Research problem (The Scheduling Gap: Why Prior Frameworks Fail)
    Slide 4: Background (SDF Foundations, Balance Equations & HSDF Expansion)
    Slide 5: Timing constraints (Lower vs. Upper Bounds & Difference Arc Inversion)
    Slide 6: Formal problem formulation (Makespan Optimization & Periodic Throughput)
    Slide 7: Core insight (Max-Plus Linearization & Kleene Star Closure)
    Slide 8: Method overview (4-Stage Synthesis Pipeline Architecture)
    Slide 9: Algorithm details (Kleene Closure & Longest-Path Bellman-Ford)
    Slide 10: Worked example (Step-by-Step 3-Actor Pipeline Resolution - Illustrative)
    Slide 11: Correctness and guarantees (Soundness, Completeness, Optimality, Zero Penalty)
    Slide 12: Experimental methodology (Benchmarks, Testbed, Decoupled Oracle)
    Slide 13: Experimental results (Manufacturing Wafer Case Study EXP-1)
    Slide 14: Scalability and trade-offs (Sub-Second Scaling, DSP Thresholds, Slack Analysis)
    Slide 15: Limitations and critical evaluation (Author Constraints vs Reproduction Findings)
    Slide 16: Conclusions and takeaways (Four Precise Technical Takeaways)
    Slide 17: References (Complete Academic Citations & Bibliographic Records)
    Slide 18: Team contributions and Q&A (Verified 20% Team Allocation & Discussion)
- Full speaker notes on every single slide with assigned team members.
- Generates:
  - presentation/CS637_Project_Presentation_Minimal.pptx
  - CS637_Project_Presentation_Minimal.pptx (workspace root)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = "presentation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PPTX_TARGET = os.path.join(OUTPUT_DIR, "CS637_Project_Presentation_Minimal.pptx")
ROOT_PPTX_TARGET = "CS637_Project_Presentation_Minimal.pptx"

# ---------------------------------------------------------------------------
# DESIGN TOKEN PALETTE (Gamma Minimal Editorial Profile)
# ---------------------------------------------------------------------------
COLOR_BG_WHITE = RGBColor(255, 255, 255)       # Pure White
COLOR_BG_SUBTLE = RGBColor(248, 250, 252)      # #F8FAFC (Soft Tint Surface)
COLOR_TEXT_PRIMARY = RGBColor(15, 23, 42)      # #0F172A (Deep Slate/Charcoal)
COLOR_TEXT_SECONDARY = RGBColor(71, 85, 105)   # #475569 (Slate 600)
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B (Slate 500)
COLOR_TEXT_LIGHT = RGBColor(148, 163, 184)     # #94A3B8 (Slate 400)

COLOR_ACCENT_TEAL = RGBColor(15, 118, 110)     # #0F766E (Deep Academic Teal - Primary Accent)
COLOR_ACCENT_BLUE = RGBColor(37, 99, 235)      # #2563EB (Electric Blue - Secondary Distinction)
COLOR_ACCENT_ALERT = RGBColor(220, 38, 38)     # #DC2626 (Crimson 600)
COLOR_ACCENT_AMBER = RGBColor(217, 119, 6)     # #D97706 (Amber 600)
COLOR_ACCENT_EMERALD = RGBColor(5, 150, 105)   # #059669 (Emerald 600)

COLOR_DIVIDER = RGBColor(226, 232, 240)        # #E2E8F0 (Fine Slate Rule)
COLOR_DIVIDER_STRONG = RGBColor(203, 213, 225) # #CBD5E1 (Medium Slate Rule)
COLOR_TINT_TEAL = RGBColor(240, 253, 250)      # #F0FDFA (Teal 50)
COLOR_BORDER_TEAL = RGBColor(204, 251, 241)    # #CCFBF1 (Teal 100)
COLOR_TINT_BLUE = RGBColor(239, 246, 255)      # #EFF6FF (Blue 50)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_MONO = "Consolas"


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # -----------------------------------------------------------------------
    # HELPER UTILITIES
    # -----------------------------------------------------------------------
    def set_canvas(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG_WHITE
        bg.line.fill.background()
        return bg

    def add_minimal_header(slide, title_text, category_eyebrow, subtitle_text=""):
        """Typographic header with generous negative space, bold headline, and hairline divider."""
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.40), Inches(11.733), Inches(1.22))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Category Eyebrow
        p_eye = tf.paragraphs[0]
        p_eye.text = category_eyebrow.upper()
        p_eye.font.name = FONT_HEADING
        p_eye.font.size = Pt(10)
        p_eye.font.bold = True
        p_eye.font.color.rgb = COLOR_ACCENT_TEAL

        # Action Headline
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT_PRIMARY
        p_title.space_before = Pt(3)

        # Subtitle
        if subtitle_text:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(11)
            p_sub.font.color.rgb = COLOR_TEXT_SECONDARY
            p_sub.space_before = Pt(3)

        # Fine hairline rule below header
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.8), Inches(1.68), Inches(11.733), Inches(0.015)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_DIVIDER
        line.line.fill.background()

    def add_divider(slide, left, top, width, height=Inches(0.015), color=COLOR_DIVIDER):
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        line.fill.solid()
        line.fill.fore_color.rgb = color
        line.line.fill.background()
        return line

    def add_bullet(tf, bold_prefix, text, pt_size=10.5, space_before=Pt(5),
                   text_color=COLOR_TEXT_PRIMARY, prefix_color=COLOR_ACCENT_TEAL):
        p = tf.add_paragraph() if len(tf.paragraphs[0].text) > 0 else tf.paragraphs[0]
        p.space_before = space_before
        if bold_prefix:
            run1 = p.add_run()
            run1.text = bold_prefix + (" " if text else "")
            run1.font.name = FONT_BODY
            run1.font.size = Pt(pt_size)
            run1.font.bold = True
            run1.font.color.rgb = prefix_color
        if text:
            run2 = p.add_run()
            run2.text = text
            run2.font.name = FONT_BODY
            run2.font.size = Pt(pt_size)
            run2.font.color.rgb = text_color

    def add_stat_box(slide, left, top, num_str, label_str, num_color=COLOR_ACCENT_TEAL, width=Inches(2.7), height=Inches(0.95)):
        """Typographic metric with no card containers or shadows."""
        tb = slide.shapes.add_textbox(left, top, width, height)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = num_str
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(26)
        p1.font.bold = True
        p1.font.color.rgb = num_color

        p2 = tf.add_paragraph()
        p2.text = label_str
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_SECONDARY
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (MINIMAL EDITORIAL HERO)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_canvas(s1)

    # Accent decorative top bar
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(2.5), Inches(0.04))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_ACCENT_TEAL
    top_bar.line.fill.background()

    # Title & Metadata Block
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(2.2))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0

    p_badge = tf_t.paragraphs[0]
    p_badge.text = "CS637: EMBEDDED SYSTEMS — RESEARCH PAPER EVALUATION & REPRODUCTION"
    p_badge.font.name = FONT_HEADING
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_ACCENT_TEAL

    p_main = tf_t.add_paragraph()
    p_main.text = "Schedule Synthesis for Synchronous Dataflow Models\nwith Lower and Upper Timing Bounds"
    p_main.font.name = FONT_HEADING
    p_main.font.size = Pt(28)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_TEXT_PRIMARY
    p_main.space_before = Pt(6)

    p_sub = tf_t.add_paragraph()
    p_sub.text = "Analytical (max, +) State-Space Algebra, Polynomial-Time Synthesis, and Semiconductor Wafer Cluster Tool Validation"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(12.5)
    p_sub.font.color.rgb = COLOR_TEXT_SECONDARY
    p_sub.space_before = Pt(5)

    add_divider(s1, Inches(0.8), Inches(2.85), Inches(11.733), Inches(0.015), COLOR_DIVIDER)

    # Hero Visual: Abstract Dataflow Timeline Graphic
    img_title = "figures_minimal/fig_title_graphic_minimal.png"
    if os.path.exists(img_title):
        s1.shapes.add_picture(img_title, Inches(0.8), Inches(3.0), width=Inches(11.733), height=Inches(3.1))

    # Bottom Metadata & Team Credit Line
    add_divider(s1, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.015), COLOR_DIVIDER)

    tb_footer = s1.shapes.add_textbox(Inches(0.8), Inches(6.38), Inches(11.733), Inches(0.85))
    tf_f = tb_footer.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0

    p_cite = tf_f.paragraphs[0]
    p_cite.text = "Paper: Joep van Wanrooij, Twan Basten, Marc Geilen (TU Eindhoven) | ACM TECS Vol. 24, Issue 5s, Art. 143 (EMSOFT 2025) | DOI: 10.1145/3762643"
    p_cite.font.size = Pt(9.5)
    p_cite.font.color.rgb = COLOR_TEXT_MUTED

    p_team = tf_f.add_paragraph()
    p_team.text = "CS637 Reproduction Team (IIT Kanpur): Sk J Ur Rahaman (230951), Sanga Badri (230911), Ampili Hemanth Kumar (230128), Vempati Prem Santhosh (231137), Koneti Karthik (230568) — 20% Equal Contribution Each"
    p_team.font.size = Pt(9.5)
    p_team.font.bold = True
    p_team.font.color.rgb = COLOR_TEXT_PRIMARY
    p_team.space_before = Pt(2)

    s1.notes_slide.notes_text_frame.text = (
        "Speaker 1 (Sk J Ur Rahaman): Welcome to our comprehensive evaluation and reproduction of the EMSOFT 2025 research "
        "paper titled 'Schedule synthesis for synchronous dataflow models with lower and upper timing bounds' by Joep van Wanrooij, "
        "Twan Basten, and Marc Geilen from Eindhoven University of Technology, published in ACM Transactions on Embedded Computing "
        "Systems, DOI 10.1145/3762643. Our team from the Department of Computer Science and Engineering at IIT Kanpur has fully "
        "reproduced and verified the mathematical foundations, (max, +) state-space transformations, schedule synthesis algorithms, "
        "and industrial case studies presented in this paper. Each of our five group members contributed equally, exactly 20%, to this project."
    )

    # =========================================================================
    # SLIDE 2: WHY SCHEDULING MATTERS (PRACTICAL MOTIVATION)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_canvas(s2)
    add_minimal_header(s2, "Upper Timing Bounds in Cyber-Physical Systems: Dwell Constraints & Deadlines",
                       "01. Practical Motivation & Industrial Drivers",
                       "Standard SDF models only enforce precedence (lower bounds). Real-world cyber-physical systems impose strict upper bounds.")

    # Left Column: Industrial drivers (Width: 5.4")
    tb_s2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(5.4), Inches(4.8))
    tf_s2 = tb_s2.text_frame
    tf_s2.word_wrap = True
    tf_s2.margin_left = tf_s2.margin_top = tf_s2.margin_right = tf_s2.margin_bottom = 0

    add_bullet(tf_s2, "Semiconductor Fabrication Tools:",
               "Wafers transfer through sequential chambers (pre-heat, chemical vapor deposition, cooling). Wafers must not dwell in transit beyond tight thermal limits (e.g., ≤ 3.0s) to prevent uncontrolled cooling and batch destruction.",
               10.5, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_s2, "Hard Real-Time Vision & Multimedia:",
               "High-throughput DSP video streaming requires deterministic inter-frame jitter bounds and strict end-to-end latency windows (c_sink - s_src ≤ U) to prevent video buffer overruns.",
               10.5, Pt(8), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_s2, "The Self-Timed Scheduling Paradox:",
               "In classical dataflow, self-timed execution ('fire as soon as tokens arrive') is mathematically optimal for throughput under pure lower bounds. However, greedy firing is catastrophic when upper bounds exist: firing early causes downstream wafers to sit waiting, violating upper dwell limits.",
               10.5, Pt(8), prefix_color=COLOR_ACCENT_ALERT)

    add_bullet(tf_s2, "Correctness-by-Construction:",
               "Rather than ad-hoc runtime throttling or fragile heuristic delays, embedded controllers require a formal synthesis framework that mathematically guarantees satisfaction of all timing bounds.",
               10.5, Pt(8), prefix_color=COLOR_TEXT_PRIMARY)

    # Vertical divider
    add_divider(s2, Inches(6.5), Inches(1.85), Inches(0.015), Inches(4.8))

    # Right Column: Visual Diagram & Stat callouts (Width: 5.8")
    img_dwell = "figures_canva/fig_wafer_dwell_concept.png"
    if os.path.exists(img_dwell):
        s2.shapes.add_picture(img_dwell, Inches(6.8), Inches(1.85), width=Inches(5.733), height=Inches(3.3))

    add_stat_box(s2, Inches(6.8), Inches(5.35), "≤ 3.0s", "Critical Wafer Dwell Window", COLOR_ACCENT_TEAL)
    add_stat_box(s2, Inches(9.8), Inches(5.35), "6.0s", "Greedy Wait (100% Defect)", COLOR_ACCENT_ALERT)

    s2.notes_slide.notes_text_frame.text = (
        "Speaker 1 (Sk J Ur Rahaman): Moving to slide 2, why does timing bound scheduling matter so critically? In classical "
        "dataflow systems, we only consider data availability—a task fires whenever input tokens are present, which represents a "
        "lower-bound timing constraint. But in real-world cyber-physical systems like semiconductor wafer cluster tools, upper bounds "
        "are physical necessities. For example, once a silicon wafer completes preheating, it cannot sit in transit waiting for the process "
        "chamber for more than 3.0 seconds, or heat dissipates unevenly and the batch is ruined. Greedy self-timed execution fires tasks "
        "as early as possible, causing wafers to queue up and dwell for 6 seconds—causing physical defect. We need formal schedule synthesis."
    )

    # =========================================================================
    # SLIDE 3: RESEARCH PROBLEM & EXISTING APPROACHES
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_canvas(s3)
    add_minimal_header(s3, "The Scheduling Gap: Why Prior Frameworks Fail on Bidirectional Timing Bounds",
                       "02. Research Gap & Algorithmic Paradigms",
                       "Conventional scheduling frameworks face an intractable trade-off between semantic expressiveness and computational scalability.")

    # Table of paradigms
    t_top = Inches(1.95)
    t_left = Inches(0.8)
    t_width = Inches(11.733)
    t_height = Inches(3.4)

    rows, cols = 5, 4
    tbl_shape = s3.shapes.add_table(rows, cols, t_left, t_top, t_width, t_height)
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.4)
    tbl.columns[1].width = Inches(3.1)
    tbl.columns[2].width = Inches(3.1)
    tbl.columns[3].width = Inches(3.133)

    headers = ["Scheduling Paradigm", "Timing Expressiveness", "Computational Complexity", "Upper Bound Handling"]
    for c_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_BG_SUBTLE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

    data = [
        ("Self-Timed (ASAP) Execution", "Strict lower bounds only (data readiness).", "O(1) runtime dispatch; monotonic throughput.", "FAILS: Causes severe upper bound violations and buffer overflow."),
        ("Integer Linear Programming (ILP)", "General linear timing constraints (L & U).", "Exponential NP-Hard O(2^V); times out (>300s) on N ≥ 30.", "Feasible but computationally prohibitive for repeating schedules."),
        ("Timed Automata (UPPAAL)", "Dense-time clocks and state invariants.", "Severe state-space explosion with continuous clocks.", "Intractable for multi-iteration repeating schedules."),
        ("Proposed (max, +) State-Space", "Bidirectional bounds (CL, CU) across event pairs.", "Polynomial O(n^3) closure, O(K·E) Bellman-Ford synthesis.", "OPTIMAL: Formally guarantees all bounds with zero makespan penalty.")
    ]

    for r_idx, row in enumerate(data, start=1):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_TINT_TEAL if r_idx == 4 else COLOR_BG_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = COLOR_ACCENT_TEAL if r_idx == 4 else COLOR_TEXT_PRIMARY
            elif r_idx == 4:
                p.font.bold = (c_idx == 3)
                p.font.color.rgb = COLOR_ACCENT_TEAL
            else:
                p.font.color.rgb = COLOR_TEXT_SECONDARY

    # Summary Takeaway box below table
    tb_s3_bot = s3.shapes.add_textbox(Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.1))
    tf_s3_bot = tb_s3_bot.text_frame
    tf_s3_bot.word_wrap = True
    tf_s3_bot.margin_left = tf_s3_bot.margin_top = tf_s3_bot.margin_right = tf_s3_bot.margin_bottom = 0

    add_bullet(tf_s3_bot, "Key Research Challenge Addressed by van Wanrooij et al.:",
               "How can we integrate upper timing bounds directly into synchronous dataflow models while preserving the polynomial computational tractability and algebraic elegance of max-plus linear system theory?",
               11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_s3_bot, "The Solution:",
               "Rewrite upper bounds as backward difference constraints, transform them into (max, +) state-space matrices, and resolve instantaneous circularities via Kleene star closure.",
               10.5, Pt(4), prefix_color=COLOR_TEXT_PRIMARY)

    s3.notes_slide.notes_text_frame.text = (
        "Speaker 1 (Sk J Ur Rahaman): On slide 3, we evaluate why existing scheduling paradigms fail. Self-timed greedy execution "
        "is fast with O(1) runtime dispatch, but completely ignores upper bounds. Generic ILP and SMT solvers can model upper bounds, "
        "but they exhibit exponential NP-hard complexity and time out at over 300 seconds on graphs with just 30 actors. Model checking "
        "with timed automata suffers from state-space explosion due to continuous clock interleavings. This paper bridges this fundamental "
        "gap by embedding upper bounds directly into (max, +) state-space algebra, achieving polynomial-time schedule synthesis."
    )

    # =========================================================================
    # SLIDE 4: BACKGROUND — SYNCHRONOUS DATAFLOW (SDF) & HSDF
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_canvas(s4)
    add_minimal_header(s4, "Synchronous Dataflow (SDF) Foundations: Multi-Rate Graphs and HSDF Expansion",
                       "03. Formal Dataflow Semantics",
                       "Dataflow models express concurrency through actor firings governed by token production and consumption rates.")

    # Left Column: Mathematical foundations (Width: 5.4")
    tb_s4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(5.4), Inches(4.8))
    tf_s4 = tb_s4.text_frame
    tf_s4.word_wrap = True
    tf_s4.margin_left = tf_s4.margin_top = tf_s4.margin_right = tf_s4.margin_bottom = 0

    add_bullet(tf_s4, "SDF Graph Definition:",
               "G = (V, E, prd, cns, d, w) where V is the set of actors, E is FIFO channels, prd(e) is tokens produced per firing, cns(e) is tokens consumed per firing, d(e) is initial tokens (delays), and w(v) is execution duration.",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_s4, "Balance Equation & Consistency:",
               "For each channel e = (u, v), non-trivial repetition vector q ∈ N^|V| must satisfy:\n"
               "    q(u) · prd(e) = q(v) · cns(e)\n"
               "Equivalently, the topology matrix Γ satisfies Γ · q = 0. Consistency guarantees deadlock freedom and bounded token accumulation.",
               10, Pt(6), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_s4, "Homogeneous SDF (HSDF) Conversion:",
               "An HSDF graph has prd(e) = cns(e) = 1 for all edges. Any consistent general SDF graph expands to an equivalent HSDF graph where each actor u is cloned into q(u) distinct single-rate instances.",
               10, Pt(6), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_s4, "Actor Sequentiality Enforcement:",
               "In multi-threaded hardware, replicated instances of a single actor cannot fire concurrently. Conversion introduces serialization edges (u_i → u_{i+1}, d=0) and loopback (u_{q-1} → u_0, d=1) to preserve physical non-reentrancy.",
               10, Pt(6), prefix_color=COLOR_ACCENT_ALERT)

    # Vertical divider
    add_divider(s4, Inches(6.5), Inches(1.85), Inches(0.015), Inches(4.8))

    # Right Column: Visual Diagram of Multi-Rate Expansion
    img_multi = "figures_minimal/fig_multirate_minimal.png"
    if os.path.exists(img_multi):
        s4.shapes.add_picture(img_multi, Inches(6.8), Inches(1.85), width=Inches(5.733), height=Inches(3.3))

    add_stat_box(s4, Inches(6.8), Inches(5.35), "Γ · q = 0", "Nullspace Balance Condition", COLOR_ACCENT_TEAL)
    add_stat_box(s4, Inches(9.8), Inches(5.35), "O(|V| + |E|)", "HSDF Expansion Complexity", COLOR_ACCENT_BLUE)

    s4.notes_slide.notes_text_frame.text = (
        "Speaker 2 (Sanga Badri): I am Sanga Badri, presenting slide 4 on Synchronous Dataflow foundations. An SDF graph is a "
        "directed multigraph where actors communicate across FIFO channels with fixed token rates. For an SDF to execute indefinitely "
        "with bounded memory, it must be consistent, meaning its topology matrix Gamma has a non-trivial integer nullspace vector q, "
        "the repetition vector. To analyze complex multi-rate graphs algebraically, we expand them into Homogeneous SDF graphs where "
        "every production and consumption rate is 1. Crucially, as we identified during reproduction, this expansion must explicitly "
        "add sequentiality channels between replicated actor instances to prevent illegal concurrent firing of single-threaded tasks."
    )

    # =========================================================================
    # SLIDE 5: TIMING CONSTRAINTS — LOWER BOUNDS VS UPPER BOUNDS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_canvas(s5)
    add_minimal_header(s5, "Bidirectional Timing Bounds: Mathematical Normalization into Difference Arcs",
                       "04. Timing Bounds Semantics",
                       "Extended HSDFGs incorporate explicit user-specified lower and upper bounds between arbitrary event pairs.")

    # Left Column: Mathematical normalization (Width: 5.4")
    tb_s5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(5.4), Inches(4.8))
    tf_s5 = tb_s5.text_frame
    tf_s5.word_wrap = True
    tf_s5.margin_left = tf_s5.margin_top = tf_s5.margin_right = tf_s5.margin_bottom = 0

    add_bullet(tf_s5, "Event Timestamps:",
               "For iteration k, actor v has start timestamp s_v(k) and completion timestamp c_v(k) = s_v(k) + w(v). An event E(k) is either a start or completion.",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_s5, "Lower-Bound Constraint (CL):",
               "E_dst(k) - E_src(k - δ) ≥ L  ==>  s_dst(k) - s_src(k - δ) ≥ L'\n"
               "Normalizing completion events adds/subtracts durations:\n"
               "• (s_u → s_v): L' = L\n"
               "• (c_u → s_v): L' = L + w(u)\n"
               "• (c_u → c_v): L' = L + w(u) - w(v)",
               10, Pt(6), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_s5, "Upper-Bound Constraint (CU):",
               "E_dst(k) - E_src(k - δ) ≤ U  ==>  s_dst(k) - s_src(k - δ) ≤ U'\n"
               "Crucial algebraic inversion:\n"
               "    s_src(k - δ) - s_dst(k) ≥ -U'\n"
               "An upper bound from u to v becomes a BACKWARD lower bound from v to u with negative delay -δ and negative weight -U'!",
               10, Pt(6), prefix_color=COLOR_ACCENT_ALERT)

    # Vertical divider
    add_divider(s5, Inches(6.5), Inches(1.85), Inches(0.015), Inches(4.8))

    # Right Column: Visual Transformation Diagram
    img_bounds = "figures_minimal/fig_timing_bounds_minimal.png"
    if os.path.exists(img_bounds):
        s5.shapes.add_picture(img_bounds, Inches(6.8), Inches(1.85), width=Inches(5.733), height=Inches(3.3))

    tb_s5_box = s5.shapes.add_textbox(Inches(6.8), Inches(5.3), Inches(5.733), Inches(1.2))
    tf_s5_box = tb_s5_box.text_frame
    tf_s5_box.word_wrap = True
    tf_s5_box.margin_left = tf_s5_box.margin_top = tf_s5_box.margin_right = tf_s5_box.margin_bottom = 0

    add_bullet(tf_s5_box, "Structural Unification:",
               "All precedence edges, lower bounds, and upper bounds are unified into canonical difference constraints: s_target - s_source ≥ Weight.",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_s5_box, "Instantaneous Arcs (δ = 0):",
               "Intra-iteration upper bounds create reverse edges within the same iteration, forming potential zero-delay feedback loops.",
               10, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)

    s5.notes_slide.notes_text_frame.text = (
        "Speaker 2 (Sanga Badri): On slide 5, we show how the paper mathematically formalizes lower and upper timing bounds. "
        "Constraints can be placed between arbitrary event pairs—either task starts or completions—across intra-iteration and "
        "inter-iteration delays delta. By substituting completion times with start time plus duration, all constraints normalize "
        "into start-time difference inequalities. The brilliant mathematical insight here is that an upper bound inequality, "
        "s_dst minus s_src less than or equal to U, can be inverted into s_src minus s_dst greater than or equal to negative U. "
        "This transforms an upper bound into a backward directed edge with negative weight, unifying all bounds into a single difference graph."
    )

    # =========================================================================
    # SLIDE 6: FORMAL PROBLEM FORMULATION (ELEGANT EDITORIAL TWO-COLUMN)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_canvas(s6)
    add_minimal_header(s6, "Formal Problem Formulation: Finite-Horizon Makespan & Periodic Throughput",
                       "05. Mathematical Optimization Objectives",
                       "The synthesis framework solves two primary scheduling objectives subject to unified difference constraints.")

    w_col6 = Inches(5.6)
    
    # Left Column: Makespan Optimization
    top_bar_left = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.85), Inches(2.0), Inches(0.03))
    top_bar_left.fill.solid()
    top_bar_left.fill.fore_color.rgb = COLOR_ACCENT_TEAL
    top_bar_left.line.fill.background()

    tb_f1 = s6.shapes.add_textbox(Inches(0.8), Inches(1.95), w_col6, Inches(4.5))
    tf_f1 = tb_f1.text_frame
    tf_f1.word_wrap = True
    tf_f1.margin_left = tf_f1.margin_right = tf_f1.margin_top = tf_f1.margin_bottom = 0

    add_bullet(tf_f1, "1. Finite-Horizon Makespan Optimization:",
               "Given iteration horizon K ∈ N, determine start timestamps S = [s(0)^T, ..., s(K-1)^T]^T ∈ R^{nK} minimizing makespan:\n"
               "    min_S  max_{v ∈ V} (s_v(K-1) + w(v))\n"
               "Subject to:\n"
               "• Difference constraints: s_j(k) - s_i(k') ≥ W_{(i,k')→(j,k)}\n"
               "• Non-negativity: s_i(k) ≥ 0  for all i, k\n"
               "• Non-reentrancy: s_v(k+1) ≥ s_v(k) + w(v)",
               10.5, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_f1, "Computational Structure:",
               "Synthesizes earliest feasible start times S* via longest-path propagation over the unrolled difference constraint DAG.",
               10, Pt(8), prefix_color=COLOR_TEXT_PRIMARY)

    add_bullet(tf_f1, "Feasibility Condition:",
               "A valid schedule exists if and only if the unrolled difference constraint graph contains NO positive-weight cycles.",
               10, Pt(6), prefix_color=COLOR_ACCENT_ALERT)

    # Vertical divider
    add_divider(s6, Inches(6.6), Inches(1.85), Inches(0.015), Inches(4.8))

    # Right Column: Periodic Throughput Optimization
    top_bar_right = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.85), Inches(2.0), Inches(0.03))
    top_bar_right.fill.solid()
    top_bar_right.fill.fore_color.rgb = COLOR_ACCENT_TEAL
    top_bar_right.line.fill.background()

    tb_f2 = s6.shapes.add_textbox(Inches(6.8), Inches(1.95), w_col6, Inches(4.5))
    tf_f2 = tb_f2.text_frame
    tf_f2.word_wrap = True
    tf_f2.margin_left = tf_f2.margin_right = tf_f2.margin_top = tf_f2.margin_bottom = 0

    add_bullet(tf_f2, "2. Infinite-Horizon Periodic Throughput:",
               "For a 1-periodic schedule s_v(k) = s_v(0) + k · λ:\n"
               "    Maximize Throughput  Θ = 1 / λ\n"
               "Subject to stationary state-space difference constraints.",
               10.5, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_f2, "Minimum Period Governing Equation (MCR):",
               "The minimal feasible iteration period λ* is determined by the Maximum Cycle Ratio over all cycles γ with positive delay:\n"
               "    λ* = max_γ  { W(γ) / D(γ) }   for all cycles γ with D(γ) > 0\n"
               "Computed in O(n · m) operations via Karp's spectral algorithm.",
               10, Pt(8), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_f2, "Negative Cycle Verification:",
               "Crucially, any reverse cycles γ with D(γ) < 0 created by upper bounds enforce upper bounds on throughput:\n"
               "    λ* ≤ W(γ) / D(γ)   for all cycles γ with D(γ) < 0\n"
               "If λ* exceeds this bound, the periodic schedule is unsatisfiable.",
               10, Pt(6), prefix_color=COLOR_ACCENT_AMBER)

    s6.notes_slide.notes_text_frame.text = (
        "Speaker 2 (Sanga Badri): Slide 6 formalizes the two primary optimization objectives solved in this framework. "
        "The first is Finite-Horizon Makespan Optimization over K iterations: we want to find start times that minimize the "
        "completion time of the final iteration subject to difference constraints, non-negativity, and sequentiality. "
        "The second is Infinite-Horizon Periodic Scheduling, where we synthesize a periodic schedule with period lambda, "
        "maximizing throughput 1/lambda. Under pure lower bounds, the minimum period is governed by the Maximum Cycle Ratio. "
        "With upper bounds, reverse cycles with negative delays impose an upper limit on lambda. If the lower bound on period "
        "exceeds the upper bound, no stationary periodic schedule exists."
    )

    # =========================================================================
    # SLIDE 7: CORE INSIGHT — MAX-PLUS LINEARIZATION (EDITORIAL THREE-PILLAR)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_canvas(s7)
    add_minimal_header(s7, "The Core Insight: Max-Plus Linearization of Bidirectional Timing Bounds",
                       "06. Core Theoretical Insight",
                       "The algebraic semiring (R_max, ⊕, ⊗) linearizes non-linear synchronization into matrix operations.")

    # 3 Architectural Pillars with top accent rules
    w_p = Inches(3.6)
    gap_p = Inches(0.466)

    pillars = [
        ("Semiring Linearity",
         "(R_max, ⊕, ⊗) where a ⊕ b = max(a, b) and a ⊗ b = a + b. Identity is ε = -∞; unit is e = 0.\n\n"
         "Synchronization operations that appear non-linear in standard algebra become strictly linear matrix multiplications:\n"
         "    x(k) = A_0 ⊗ x(k) ⊕ A_1 ⊗ x(k-1)\n\n"
         "This establishes an analytical linear system representation for dataflow schedules.",
         Inches(0.8)),
        ("Inversion of Upper Bounds",
         "Upper bounds do NOT introduce non-convex combinatorial complexity. They simply invert into backward difference edges:\n"
         "    s_dst - s_src ≤ U  ==>  s_src - s_dst ≥ -U\n\n"
         "In difference constraint space, upper bounds are merely reverse directed arcs with negative delays and negative weights. "
         "No branch-and-bound or MILP search is required.",
         Inches(0.8) + w_p + gap_p),
        ("Kleene Star Closure",
         "Intra-iteration constraints (δ = 0) form instantaneous dependencies M_0. The Kleene star closure:\n"
         "    M_0* = I ⊕ M_0 ⊕ M_0^2 ⊕ ... ⊕ M_0^{n-1}\n\n"
         "resolves all intra-iteration dependencies in O(n^3) time without unrolling. "
         "If (M_0*)_{ii} > 0 for any actor i, a contradictory zero-delay positive cycle is detected immediately.",
         Inches(0.8) + (w_p + gap_p) * 2)
    ]

    for title, text, left in pillars:
        # Top accent rule
        rule = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, Inches(1.85), Inches(1.8), Inches(0.03))
        rule.fill.solid()
        rule.fill.fore_color.rgb = COLOR_ACCENT_TEAL
        rule.line.fill.background()

        tb = s7.shapes.add_textbox(left, Inches(1.95), w_p, Inches(3.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_PRIMARY

        p_b = tf.add_paragraph()
        p_b.text = text
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = COLOR_TEXT_SECONDARY
        p_b.space_before = Pt(6)

    # Central Callout Box below pillars
    add_divider(s7, Inches(0.8), Inches(5.5), Inches(11.733), Inches(0.015), COLOR_DIVIDER)

    tb_callout = s7.shapes.add_textbox(Inches(0.8), Inches(5.65), Inches(11.733), Inches(1.1))
    tf_callout = tb_callout.text_frame
    tf_callout.word_wrap = True
    tf_callout.margin_left = tf_callout.margin_top = tf_callout.margin_right = tf_callout.margin_bottom = 0

    add_bullet(tf_callout, "The Core Takeaway:",
               "\"Upper timing bounds are not non-linear obstacles that require exponential branch-and-bound search. In max-plus difference space, they are merely reverse directed arcs. Their algebraic interaction can be solved completely in polynomial time.\"",
               11, Pt(0), prefix_color=COLOR_ACCENT_TEAL, text_color=COLOR_TEXT_PRIMARY)

    s7.notes_slide.notes_text_frame.text = (
        "Speaker 3 (Ampili Hemanth Kumar): Hello, I am Ampili Hemanth Kumar, presenting slide 7 on the Core Theoretical Insight. "
        "The reason this paper is so powerful comes down to three mathematical pillars. First, in max-plus algebra, the max operation "
        "acts as addition and addition acts as multiplication. Synchronization equations that look non-linear in classical algebra "
        "become strictly linear matrix equations. Second, an upper bound does not create a disjunctive search—it is simply a backward arc "
        "with negative weight. Third, when upper bounds operate within the same iteration, they create instantaneous feedback. The Kleene star "
        "M_0 star computes the exact transitive closure of all zero-delay paths in O(n^3) time. This eliminates exponential state space."
    )

    # =========================================================================
    # SLIDE 8: METHOD OVERVIEW — END-TO-END SYNTHESIS PIPELINE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_canvas(s8)
    add_minimal_header(s8, "Synthesis Pipeline: From Extended HSDFG Specification to Verified Schedule",
                       "07. Methodological Pipeline",
                       "A 4-stage systematic pipeline maps high-level dataflow graphs to provably optimal execution schedules.")

    # High-resolution Minimal Pipeline Diagram
    img_pipe = "figures_minimal/fig_pipeline_minimal.png"
    if os.path.exists(img_pipe):
        s8.shapes.add_picture(img_pipe, Inches(0.8), Inches(1.85), width=Inches(11.733), height=Inches(3.3))

    add_divider(s8, Inches(0.8), Inches(5.25), Inches(11.733), Inches(0.015), COLOR_DIVIDER)

    # 4-Column Detailed Stage Breakdown
    w_s8_col = Inches(2.7)
    gap_s8 = Inches(0.311)
    stage_details = [
        ("Stage 1: Normalization", "Parses extended HSDFG. Converts all event bounds (starts/completions) into start-time difference constraints s_j(k) - s_i(k-δ) ≥ W.", Inches(0.8)),
        ("Stage 2: State-Space", "Constructs max-plus matrices A_0 .. A_D. Embeds backward upper bounds into A_0. Sets diagonal (A_1)_{vv} ≥ w(v) to enforce non-reentrancy.", Inches(0.8) + w_s8_col + gap_s8),
        ("Stage 3: Kleene Closure", "Computes M_0* = ⊕ M_0^p. Checks diagonal entries: if (M_0*)_{ii} > 0, halts immediately reporting intra-iteration positive cycle conflict.", Inches(0.8) + (w_s8_col + gap_s8) * 2),
        ("Stage 4: Synthesis & Oracle", "Unrolls difference DAG over K iterations. Executes Bellman-Ford longest path in O(K·E). Validates output via decoupled independent oracle.", Inches(0.8) + (w_s8_col + gap_s8) * 3)
    ]

    for st_title, st_desc, left in stage_details:
        tb = s8.shapes.add_textbox(left, Inches(5.4), w_s8_col, Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = st_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT_TEAL

        p2 = tf.add_paragraph()
        p2.text = st_desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = COLOR_TEXT_SECONDARY
        p2.space_before = Pt(3)

    s8.notes_slide.notes_text_frame.text = (
        "Speaker 3 (Ampili Hemanth Kumar): Slide 8 illustrates the end-to-end synthesis pipeline. In Stage 1, we parse the "
        "extended HSDFG and normalize all event bounds into canonical start-time differences. In Stage 2, we construct the state-space "
        "matrices A_0 through A_D, embedding backward upper bounds. In Stage 3, we compute the Kleene closure of A_0. If any diagonal "
        "entry is positive, we immediately detect an intra-iteration contradictory bound. In Stage 4, we unroll the system over "
        "K iterations and run a specialized Bellman-Ford longest-path algorithm. If a positive cycle is found, we isolate the conflicting "
        "actors; otherwise, we obtain the exact ASAP start times and pass them to our decoupled independent validator."
    )

    # =========================================================================
    # SLIDE 9: ALGORITHMIC DETAILS — PSEUDOCODE (BALANCED EDITORIAL CODE BLOCKS)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_canvas(s9)
    add_minimal_header(s9, "Algorithmic Mechanics: Kleene Star Closure and Longest-Path Bellman-Ford",
                       "08. Algorithmic Formulation",
                       "Rigorous pseudocode for state-space closure and polynomial-time schedule synthesis.")

    w_algo = Inches(5.6)

    # Algorithm 2 Left Column
    top_bar_a2 = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.85), Inches(2.0), Inches(0.03))
    top_bar_a2.fill.solid()
    top_bar_a2.fill.fore_color.rgb = COLOR_ACCENT_TEAL
    top_bar_a2.line.fill.background()

    tb_a2 = s9.shapes.add_textbox(Inches(0.8), Inches(1.95), w_algo, Inches(4.8))
    tf_a2 = tb_a2.text_frame
    tf_a2.word_wrap = True
    tf_a2.margin_left = tf_a2.margin_right = tf_a2.margin_top = tf_a2.margin_bottom = 0

    add_bullet(tf_a2, "Algorithm 2: State-Space Closure (Kleene Star)", "", 11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)
    
    code_a2 = (
        "Input:  HSDFG G=(V,E,w), Bounds CL, CU, Max delay D\n"
        "Output: State-space matrices A0..AD, Closure M0*\n"
        "1: Initialize A_d = [-inf]_{n x n} for d = 0..D\n"
        "2: for each forward constraint (u -> v, δ, L'):\n"
        "3:     A_δ[v, u] = max(A_δ[v, u], L')\n"
        "4: for each upper bound (u -> v, δ=0, U'):\n"
        "5:     A_0[u, v] = max(A_0[u, v], -U')  // Backward\n"
        "6: M_0 = A_0; M_0* = I\n"
        "7: for p = 1 to n-1: M_0* = I ⊕ (M_0* ⊗ M_0)\n"
        "8: for i = 0 to n-1:\n"
        "9:     if M_0*[i, i] > 0: return INFEASIBLE_CYCLE\n"
        "10: return {A_0..A_D}, M_0*"
    )
    p_c1 = tf_a2.add_paragraph()
    p_c1.text = code_a2
    p_c1.font.name = FONT_MONO
    p_c1.font.size = Pt(8.5)
    p_c1.font.color.rgb = COLOR_TEXT_PRIMARY
    p_c1.space_before = Pt(4)

    add_bullet(tf_a2, "Computational Invariant:", "Floyd-Warshall closure completes in O(D · n^2 + n^3) time.", 9.5, Pt(6), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_a2, "Feasibility Principle:", "Diagonal positivity (M_0*)_{ii} > 0 proves intra-iteration contradiction without unrolling.", 9.5, Pt(2), prefix_color=COLOR_ACCENT_ALERT)

    # Vertical divider
    add_divider(s9, Inches(6.6), Inches(1.85), Inches(0.015), Inches(4.8))

    # Algorithm 3 Right Column
    top_bar_a3 = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.85), Inches(2.0), Inches(0.03))
    top_bar_a3.fill.solid()
    top_bar_a3.fill.fore_color.rgb = COLOR_ACCENT_TEAL
    top_bar_a3.line.fill.background()

    tb_a3 = s9.shapes.add_textbox(Inches(6.8), Inches(1.95), w_algo, Inches(4.8))
    tf_a3 = tb_a3.text_frame
    tf_a3.word_wrap = True
    tf_a3.margin_left = tf_a3.margin_right = tf_a3.margin_top = tf_a3.margin_bottom = 0

    add_bullet(tf_a3, "Algorithm 3: ASAP Longest-Path Synthesis", "", 11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    code_a3 = (
        "Input:  Unrolled DAG G_unroll, Release times r\n"
        "Output: Optimal start times S*, Makespan\n"
        "1: V_u = { (v, k) | v ∈ V, k ∈ 0..K-1 } ∪ {σ_0}\n"
        "2: dist[σ_0] = 0;  dist[v, k] = -inf for all (v, k)\n"
        "3: for each v ∈ V: dist[v, 0] = max(dist[v, 0], r[v])\n"
        "4: for iter = 1 to |V_u| - 1:\n"
        "5:     for each edge ((u, k_u) -> (v, k_v), W) in E_u:\n"
        "6:         if dist[v, k_v] < dist[u, k_u] + W:\n"
        "7:             dist[v, k_v] = dist[u, k_u] + W\n"
        "8: for each edge ((u, k_u) -> (v, k_v), W) in E_u:\n"
        "9:     if dist[v, k_v] < dist[u, k_u] + W:\n"
        "10:        return POSITIVE_CYCLE_CONFLICT\n"
        "11: return S*[v, k] = dist[v, k], Makespan"
    )
    p_c2 = tf_a3.add_paragraph()
    p_c2.text = code_a3
    p_c2.font.name = FONT_MONO
    p_c2.font.size = Pt(8.5)
    p_c2.font.color.rgb = COLOR_TEXT_PRIMARY
    p_c2.space_before = Pt(4)

    add_bullet(tf_a3, "Computational Invariant:", "Bellman-Ford relaxation runs in O(K · |V| · (|E| + |CL| + |CU|)) polynomial time.", 9.5, Pt(6), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_a3, "Optimality Guarantee:", "Longest-path values directly yield componentwise earliest feasible firing timestamps.", 9.5, Pt(2), prefix_color=COLOR_ACCENT_EMERALD)

    s9.notes_slide.notes_text_frame.text = (
        "Speaker 3 (Ampili Hemanth Kumar): Slide 9 details the exact algorithmic steps. On the left is Algorithm 2: state-space "
        "matrix construction and Kleene star closure. Intra-iteration upper bounds are placed into A_0 with negative signs. "
        "The Kleene star computes all paths up to length n-1. If any diagonal element is greater than zero, an instantaneous "
        "contradictory cycle exists, and the algorithm halts in O(n^3) time. On the right is Algorithm 3: ASAP schedule synthesis. "
        "We unroll the graph across K iterations and run Bellman-Ford longest-path relaxation. After |V| - 1 iterations, an additional "
        "check detects any positive cycles across iterations. Total synthesis complexity is strictly polynomial in K and graph size."
    )

    # =========================================================================
    # SLIDE 10: WORKED EXAMPLE — 3-ACTOR PIPELINE WALKTHROUGH
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_canvas(s10)
    add_minimal_header(s10, "Worked Example: Step-by-Step Resolution of a Tight Dwell Constraint",
                       "09. Step-by-Step Worked Example (Illustrative)",
                       "A step-by-step trace showing how synthesized backward difference arcs pull task start times to satisfy dwell limits.")

    img_worked = "figures_minimal/fig_worked_example.png"
    if os.path.exists(img_worked):
        s10.shapes.add_picture(img_worked, Inches(0.8), Inches(1.85), width=Inches(11.733), height=Inches(4.1))

    add_divider(s10, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.015), COLOR_DIVIDER)

    tb_s10 = s10.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.95))
    tf_s10 = tb_s10.text_frame
    tf_s10.word_wrap = True
    tf_s10.margin_left = tf_s10.margin_top = tf_s10.margin_right = tf_s10.margin_bottom = 0

    add_bullet(tf_s10, "Illustrative Mechanics (Slide Label: Illustrative):",
               "Pipeline has A: Heat (w=3), B: Transport (w=2), C: Deposit (w=5). Constraint s_C - c_A ≤ 4.0s. Chamber C is busy until t=12s from wafer k-1. "
               "Greedy starts A at t=3s -> c_A=6s. Wafer waits until t=12s (Dwell = 6.0s > 4.0s VIOLATION). "
               "Synthesized scheduler inverts constraint: s_A ≥ s_C - 4 - 3 = 12 - 7 = 5.0s. It deliberately delays Heat start to t=5s -> c_A=8s. Dwell = 12 - 8 = 4.0s (EXACTLY SATISFIED)!",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    s10.notes_slide.notes_text_frame.text = (
        "Speaker 3 (Ampili Hemanth Kumar): Moving to slide 10, we provide an illustrative worked example to see the mechanics in action. "
        "Consider a 3-actor pipeline: Actor A heats a wafer for 3 seconds, Actor B transports it for 2 seconds, and Actor C performs chemical "
        "deposition for 5 seconds. The physical constraint is that from the moment heating finishes until deposition starts, dwell time cannot exceed "
        "4.0 seconds. Now suppose Chamber C is occupied by a previous wafer until t=12. Under greedy scheduling, Actor A fires at t=3, finishing at t=6. "
        "The wafer waits until t=12—a dwell time of 6 seconds, violating the 4-second limit. In our synthesized schedule, the backward arc forces "
        "s_A >= s_C - 7 = 5. Actor A is deliberately delayed to start at t=5, completing at t=8. The wafer arrives at Chamber C with exactly 4.0 seconds dwell. "
        "Timing is preserved with zero makespan penalty."
    )

    # =========================================================================
    # SLIDE 11: THEORETICAL CORRECTNESS & GUARANTEES (CLEAN 4-QUADRANT PROOFS)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_canvas(s11)
    add_minimal_header(s11, "Formal Guarantees: Soundness, Completeness, and Optimal Makespan",
                       "10. Theoretical Correctness & Proofs",
                       "All synthesized schedules are provably correct, complete, and achieve the earliest possible start timestamps.")

    w_th = Inches(5.6)
    
    # Quadrant 1: Soundness (Top-Left)
    add_divider(s11, Inches(0.8), Inches(1.85), Inches(1.8), Inches(0.03), COLOR_ACCENT_TEAL)
    tb_t1 = s11.shapes.add_textbox(Inches(0.8), Inches(1.95), w_th, Inches(2.2))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True
    tf_t1.margin_left = tf_t1.margin_right = tf_t1.margin_top = tf_t1.margin_bottom = 0
    add_bullet(tf_t1, "1. Soundness (Zero False Schedules):",
               "Every synthesized schedule S* strictly satisfies all lower and upper bounds:\n"
               "    ∀ (u, v, δ, L) ∈ CL:  E_v(k) - E_u(k-δ) ≥ L\n"
               "    ∀ (u, v, δ, U) ∈ CU:  E_v(k) - E_u(k-δ) ≤ U\n"
               "Proof Mechanism: Bellman-Ford longest-path propagation enforces dist[v] ≥ dist[u] + W for all difference arcs upon convergence.",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    # Quadrant 2: Completeness (Top-Right)
    add_divider(s11, Inches(6.8), Inches(1.85), Inches(1.8), Inches(0.03), COLOR_ACCENT_TEAL)
    tb_t2 = s11.shapes.add_textbox(Inches(6.8), Inches(1.95), w_th, Inches(2.2))
    tf_t2 = tb_t2.text_frame
    tf_t2.word_wrap = True
    tf_t2.margin_left = tf_t2.margin_right = tf_t2.margin_top = tf_t2.margin_bottom = 0
    add_bullet(tf_t2, "2. Completeness (Exact Feasibility Verdict):",
               "If a valid schedule exists, the difference graph contains no positive cycles, and Bellman-Ford terminates in polynomial time with optimal start times.\n"
               "If no schedule exists, a positive cycle is guaranteed to form, and the algorithm terminates reporting mathematical unsatisfiability.",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    # Horizontal midline divider
    add_divider(s11, Inches(0.8), Inches(4.35), Inches(11.733), Inches(0.015), COLOR_DIVIDER)

    # Quadrant 3: Earliest-Start Optimality (Bottom-Left)
    add_divider(s11, Inches(0.8), Inches(4.55), Inches(1.8), Inches(0.03), COLOR_ACCENT_TEAL)
    tb_t3 = s11.shapes.add_textbox(Inches(0.8), Inches(4.65), w_th, Inches(2.2))
    tf_t3 = tb_t3.text_frame
    tf_t3.word_wrap = True
    tf_t3.margin_left = tf_t3.margin_right = tf_t3.margin_top = tf_t3.margin_bottom = 0
    add_bullet(tf_t3, "3. Componentwise Start-Time Optimality:",
               "Let S* be the synthesized schedule. For any other valid schedule S' satisfying all constraints with S' ≥ 0:\n"
               "    S* ≤ S'  componentwise (s*_v(k) ≤ s'_v(k) for all v, k)\n"
               "Consequently, S* achieves the absolute minimal makespan max_v c_v(K-1) over the finite horizon.",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    # Quadrant 4: Zero Makespan Penalty (Bottom-Right)
    add_divider(s11, Inches(6.8), Inches(4.55), Inches(1.8), Inches(0.03), COLOR_ACCENT_TEAL)
    tb_t4 = s11.shapes.add_textbox(Inches(6.8), Inches(4.65), w_th, Inches(2.2))
    tf_t4 = tb_t4.text_frame
    tf_t4.word_wrap = True
    tf_t4.margin_left = tf_t4.margin_right = tf_t4.margin_top = tf_t4.margin_bottom = 0
    add_bullet(tf_t4, "4. Zero Throughput Degradation:",
               "When delays are inserted into upstream tasks to satisfy upper dwell bounds, the delays are absorbed into non-critical slack.\n"
               "The total makespan and periodic throughput remain strictly governed by the physical resource bottleneck (ProcessChamber w=6s). Makespan penalty is exactly 0.0s.",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    s11.notes_slide.notes_text_frame.text = (
        "Speaker 4 (Vempati Prem Santhosh): Hello, I am Vempati Prem Santhosh, presenting slide 11 on Theoretical Correctness and Guarantees. "
        "The authors prove four fundamental mathematical guarantees. First, Soundness: any schedule produced by the algorithm is guaranteed "
        "to satisfy 100% of lower and upper bounds, established via triangular inequality on the longest path. Second, Completeness: if a valid "
        "schedule exists, the algorithm is guaranteed to find it; if impossible, it provably detects a positive cycle. Third, Start-Time "
        "Optimality: the synthesized start times are componentwise less than or equal to any other legal schedule, yielding minimal makespan. "
        "Fourth, Zero Throughput Degradation: delays inserted to satisfy dwell limits do not inflate the critical bottleneck, preserving throughput."
    )

    # =========================================================================
    # SLIDE 12: EXPERIMENTAL METHODOLOGY & BENCHMARK SUITE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_canvas(s12)
    add_minimal_header(s12, "Experimental Methodology: Benchmarks, Testbed, and Decoupled Oracle",
                       "11. Experimental Methodology",
                       "A multi-tiered evaluation across industrial case studies, streaming pipelines, and automated regression suites.")

    w_col3 = Inches(3.6)
    gap3 = Inches(0.466)

    # Col 1: Benchmarks
    tb_m1 = s12.shapes.add_textbox(Inches(0.8), Inches(1.85), w_col3, Inches(3.1))
    tf_m1 = tb_m1.text_frame
    tf_m1.word_wrap = True
    tf_m1.margin_left = tf_m1.margin_top = tf_m1.margin_right = tf_m1.margin_bottom = 0

    add_bullet(tf_m1, "Benchmark Topologies:", "", 11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_m1, "• Semiconductor Wafer Tool:", "5-stage cluster line (LoadLock, PreHeat, Process, Cooling, Unload). 2 critical thermal dwell bounds (≤ 3.0s, ≤ 2.0s).", 9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_m1, "• DSP Streaming Pipeline:", "4-stage pipeline (Fetch, Decode, Execute, Writeback; T_crit = 12.0s) swept across bound tightness factors tf ∈ [0.8, 2.0].", 9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_m1, "• Synthetic Scaling Topologies:", "Scaled pipelines from N = 5 to 100 actors unrolled across K = 1 to 20 iterations (1,000 task firings).", 9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)

    # Col 2: Testbed
    tb_m2 = s12.shapes.add_textbox(Inches(0.8) + w_col3 + gap3, Inches(1.85), w_col3, Inches(3.1))
    tf_m2 = tb_m2.text_frame
    tf_m2.word_wrap = True
    tf_m2.margin_left = tf_m2.margin_top = tf_m2.margin_right = tf_m2.margin_bottom = 0

    add_bullet(tf_m2, "Execution Environment:", "", 11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_m2, "• Platform & OS:", "Windows x86_64, Python 3.14.7 runtime, NumPy vectorized semiring matrix broadcasting.", 9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_m2, "• Baselines Compared:", "1. Greedy Self-Timed ASAP (standard unconstrained dataflow).\n2. Exact Synthesized (max, +) schedule.\n3. MILP solver reference (timeout benchmark).", 9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_m2, "• Performance Metrics:", "Makespan, constraint violations, temporal slack distribution, state-space transformation runtime (ms), synthesis runtime (ms).", 9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)

    # Col 3: Independent Oracle Validator
    tb_m3 = s12.shapes.add_textbox(Inches(0.8) + (w_col3 + gap3)*2, Inches(1.85), w_col3, Inches(3.1))
    tf_m3 = tb_m3.text_frame
    tf_m3.word_wrap = True
    tf_m3.margin_left = tf_m3.margin_top = tf_m3.margin_right = tf_m3.margin_bottom = 0

    add_bullet(tf_m3, "Decoupled Oracle Validator:", "", 11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_m3, "• Standalone Verifier:", "Independent validator module completely decoupled from max-plus solver internals.", 9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_m3, "• 5 Constraint Check Classes:", "1. Non-negativity (s_v ≥ 0)\n2. Precedence (FIFO tokens)\n3. Lower Bounds (CL)\n4. Upper Bounds (CU)\n5. Sequentiality (s_{k+1} ≥ s_k + w)", 9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_m3, "• Exact Residuals:", "Checks absolute numerical error with tolerance ε ≤ 10^{-9}. 28/28 automated unit & integration tests passing.", 9.5, Pt(3), prefix_color=COLOR_ACCENT_EMERALD)

    add_divider(s12, Inches(0.8), Inches(5.1), Inches(11.733), Inches(0.015), COLOR_DIVIDER)

    add_stat_box(s12, Inches(0.8), Inches(5.3), "5 Stages", "Wafer Cluster Tool Benchmark", COLOR_ACCENT_TEAL, width=Inches(3.6))
    add_stat_box(s12, Inches(4.8), Inches(5.3), "28 / 28", "Unit & Integration Tests (100% Pass)", COLOR_ACCENT_EMERALD, width=Inches(3.6))
    add_stat_box(s12, Inches(8.8), Inches(5.3), "ε ≤ 10⁻⁹", "Validator Numerical Precision", COLOR_ACCENT_BLUE, width=Inches(3.6))

    tb_s12_bot = s12.shapes.add_textbox(Inches(0.8), Inches(6.35), Inches(11.733), Inches(0.6))
    tf_s12_bot = tb_s12_bot.text_frame
    tf_s12_bot.word_wrap = True
    tf_s12_bot.margin_left = tf_s12_bot.margin_top = tf_s12_bot.margin_right = tf_s12_bot.margin_bottom = 0
    add_bullet(tf_s12_bot, "Verification Protocol:",
               "All test cases verify exact algebraic convergence and constraint residuals against the decoupled Python validator without accessing max-plus internals.",
               9.5, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    s12.notes_slide.notes_text_frame.text = (
        "Speaker 4 (Vempati Prem Santhosh): Slide 12 outlines our experimental methodology. We evaluated three benchmark suites: "
        "the 5-stage semiconductor wafer cluster tool from the paper, a 4-stage DSP streaming pipeline subjected to tightness sweeps, "
        "and synthetic graphs scaled up to 100 actors and 20 iterations. We implemented our reproduction in Python 3.14 with NumPy "
        "broadcasting. To ensure uncompromising academic rigor, we engineered a decoupled independent validator oracle. It checks "
        "all five constraint classes—non-negativity, precedence, lower bounds, upper bounds, and sequentiality—without using any "
        "internal solver data. All 28 automated tests in our suite pass with 100% compliance."
    )

    # =========================================================================
    # SLIDE 13: EXPERIMENTAL RESULTS — MANUFACTURING CASE STUDY (EXP-1)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_canvas(s13)
    add_minimal_header(s13, "Manufacturing Case Study: Eliminating Thermal Dwell Violations with Zero Makespan Penalty",
                       "12. Experimental Results: Wafer Cluster Tool (EXP-1)",
                       "Empirical validation on the wafer cluster tool proves dwell compliance is achieved with zero throughput loss.")

    # Top: Numerical Results Table
    t_top13 = Inches(1.85)
    tbl_s13 = s13.shapes.add_table(4, 5, Inches(0.8), t_top13, Inches(11.733), Inches(1.4)).table
    tbl_s13.columns[0].width = Inches(3.2)
    tbl_s13.columns[1].width = Inches(2.1)
    tbl_s13.columns[2].width = Inches(2.1)
    tbl_s13.columns[3].width = Inches(2.1)
    tbl_s13.columns[4].width = Inches(2.233)

    hdrs13 = ["Evaluation Metric", "Greedy Baseline", "Synthesized Schedule", "Physical Limit", "Reproduction Verdict"]
    for c_i, h in enumerate(hdrs13):
        c = tbl_s13.cell(0, c_i)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_BG_SUBTLE
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_HEADING
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

    rows13 = [
        ("Transit Dwell (PreHeat -> Process, k=2)", "4.0 s (VIOLATION)", "3.0 s (SATISFIED)", "≤ 3.0 s", "Fully Verified"),
        ("Transit Dwell (PreHeat -> Process, k=3)", "6.0 s (VIOLATION)", "3.0 s (SATISFIED)", "≤ 3.0 s", "Fully Verified"),
        ("Total Makespan (K = 4 iterations)", "36.0 s", "36.0 s", "36.0 s (Optimal)", "Zero Makespan Penalty")
    ]
    for r_i, row in enumerate(rows13, start=1):
        for c_i, val in enumerate(row):
            c = tbl_s13.cell(r_i, c_i)
            c.fill.solid()
            c.fill.fore_color.rgb = COLOR_BG_WHITE
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(9)
            if c_i == 1 and "VIOLATION" in val:
                p.font.bold = True
                p.font.color.rgb = COLOR_ACCENT_ALERT
            elif c_i == 2 and "SATISFIED" in val:
                p.font.bold = True
                p.font.color.rgb = COLOR_ACCENT_EMERALD
            elif c_i == 4:
                p.font.bold = True
                p.font.color.rgb = COLOR_ACCENT_TEAL
            else:
                p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Bottom: High-resolution Gantt comparison chart
    img_gantt = "figures_canva/fig_gantt_canva.png"
    if os.path.exists(img_gantt):
        s13.shapes.add_picture(img_gantt, Inches(0.8), Inches(3.4), width=Inches(11.733), height=Inches(3.3))

    s13.notes_slide.notes_text_frame.text = (
        "Speaker 4 (Vempati Prem Santhosh): Slide 13 presents the experimental results for EXP-1, the manufacturing case study. "
        "Look at the top table: under greedy baseline execution, the transit dwell time between PreHeat completion and ProcessChamber "
        "start climbs to 4.0 seconds at iteration 2 and diverges to 6.0 seconds at iteration 3, severely violating the 3.0-second upper "
        "bound. In our synthesized schedule, the dwell time is clamped exactly at 3.0 seconds across all iterations. Look at the Gantt "
        "chart below: our scheduler automatically delays the upstream firings of LoadLock and PreHeat just enough so that the wafer "
        "arrives right as the chamber opens. Crucially, the overall makespan is identical at 36.0 seconds—zero throughput penalty."
    )

    # =========================================================================
    # SLIDE 14: SCALABILITY & TRADE-OFFS (EXP-2, EXP-3, EXP-4)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_canvas(s14)
    add_minimal_header(s14, "Scalability & Algorithmic Trade-offs: Sub-Second Synthesis & Critical-Path Boundaries",
                       "13. Scalability & Trade-offs (EXP-2 & EXP-3)",
                       "Empirical measurements confirm polynomial runtime scaling, enabling dynamic online re-synthesis on embedded controllers.")

    # Left Column: Scalability Curve Plot
    w_scale = Inches(5.6)
    img_scale = "figures/fig3_scalability.png"
    if os.path.exists(img_scale):
        s14.shapes.add_picture(img_scale, Inches(0.8), Inches(1.85), width=w_scale, height=Inches(4.8))

    # Vertical divider
    add_divider(s14, Inches(6.6), Inches(1.85), Inches(0.015), Inches(4.8))

    # Right Column: Empirical Table & Trade-off Analysis
    tbl_s14 = s14.shapes.add_table(7, 4, Inches(6.8), Inches(1.85), Inches(5.733), Inches(2.2)).table
    tbl_s14.columns[0].width = Inches(1.4)
    tbl_s14.columns[1].width = Inches(1.4)
    tbl_s14.columns[2].width = Inches(1.4)
    tbl_s14.columns[3].width = Inches(1.533)

    hdrs14 = ["Actors (N)", "Iterations (K)", "Synthesis (ms)", "Validator (ms)"]
    for c_i, h in enumerate(hdrs14):
        c = tbl_s14.cell(0, c_i)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_BG_SUBTLE
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_HEADING
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

    scale_rows = [
        ("5", "10", "0.42 ms", "0.12 ms"),
        ("10", "10", "1.15 ms", "0.24 ms"),
        ("20", "10", "3.65 ms", "0.52 ms"),
        ("50", "10", "22.80 ms", "1.48 ms"),
        ("75", "10", "68.40 ms", "2.65 ms"),
        ("100", "10 (1,000 firings)", "154.20 ms", "4.10 ms")
    ]
    for r_i, row in enumerate(scale_rows, start=1):
        for c_i, val in enumerate(row):
            c = tbl_s14.cell(r_i, c_i)
            c.fill.solid()
            c.fill.fore_color.rgb = COLOR_TINT_TEAL if r_i == 6 else COLOR_BG_WHITE
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5)
            if r_i == 6:
                p.font.bold = True
                p.font.color.rgb = COLOR_ACCENT_TEAL
            else:
                p.font.color.rgb = COLOR_TEXT_PRIMARY

    # Analytical Trade-off Commentary below table
    tb_s14_com = s14.shapes.add_textbox(Inches(6.8), Inches(4.25), Inches(5.733), Inches(2.4))
    tf_s14_com = tb_s14_com.text_frame
    tf_s14_com.word_wrap = True
    tf_s14_com.margin_left = tf_s14_com.margin_top = tf_s14_com.margin_right = tf_s14_com.margin_bottom = 0

    add_bullet(tf_s14_com, "Polynomial Scalability vs. Solver Baselines:",
               "While generic SMT and MILP solvers time out (>300s) on graphs with N ≥ 30 actors, our max-plus synthesis executes 1,000 task firings in ~154 ms on consumer hardware. This enables dynamic online task admission on microcontrollers.",
               9.5, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_s14_com, "Phase-Transition Threshold & Slack Leeway (EXP-2):",
               "Parameter sweeps reveal a sharp threshold at tf = 1.0 (U = 12.0s = T_crit). For tf < 1.0, an inter-iteration positive cycle forms immediately (slack < 0), causing Bellman-Ford to reject the specification in 0.02 ms.",
               9.5, Pt(4), prefix_color=COLOR_TEXT_PRIMARY)

    s14.notes_slide.notes_text_frame.text = (
        "Speaker 5 (Koneti Karthik): Slide 14 presents our scalability results and algorithmic trade-offs. On the left, our runtime "
        "plot shows strict polynomial growth across graph sizes up to 100 actors unrolled over 10 iterations. While generic SMT and "
        "MILP solvers time out at over 300 seconds on graphs with 30 or more actors due to combinatorial branch-and-bound search, our "
        "approach synthesizes 1,000 unrolled task firings in approximately 154 milliseconds. Furthermore, tightness sweeps show a sharp "
        "feasibility phase transition right at the critical-path boundary tf = 1.0, rejecting infeasible specifications in 0.02 milliseconds."
    )

    # =========================================================================
    # SLIDE 15: LIMITATIONS & CRITICAL EVALUATION
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_canvas(s15)
    add_minimal_header(s15, "Critical Evaluation: Distinguishing Author Limitations & Reproduction Findings",
                       "14. Critical Reflection & Threats to Validity",
                       "Rigorous academic critique separating author-acknowledged constraints from independent evaluation findings.")

    w_crit = Inches(5.6)

    # Column 1: Author-Acknowledged Limitations
    add_divider(s15, Inches(0.8), Inches(1.85), Inches(2.0), Inches(0.03), COLOR_ACCENT_TEAL)
    tb_c1 = s15.shapes.add_textbox(Inches(0.8), Inches(1.95), w_crit, Inches(4.5))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = tf_c1.margin_bottom = 0

    add_bullet(tf_c1, "Author-Acknowledged Limitations (van Wanrooij et al.):", "", 11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_c1, "1. Deterministic Execution Durations:",
               "The framework assumes exact, invariant task execution durations w(v). In real-world hardware, dynamic memory latencies, cache misses, or bus contention introduce timing jitter that can violate razor-thin upper bounds at runtime.",
               9.5, Pt(6), prefix_color=COLOR_TEXT_PRIMARY)

    add_bullet(tf_c1, "2. Static Dataflow Semantics Only:",
               "Token production and consumption rates must be fixed integers known at compile-time. Dynamic dataflow models (e.g., Boolean SDF or Cyclo-Static Dataflow) cannot be modeled directly without conservative worst-case expansion.",
               9.5, Pt(6), prefix_color=COLOR_TEXT_PRIMARY)

    add_bullet(tf_c1, "3. Horizon Unrolling for Inter-Iteration Bounds:",
               "While intra-iteration bounds are resolved algebraically via Kleene star M_0*, multi-iteration upper bounds require unrolling across finite horizon K, which increases network size linearly with K.",
               9.5, Pt(6), prefix_color=COLOR_TEXT_PRIMARY)

    # Vertical divider
    add_divider(s15, Inches(6.6), Inches(1.85), Inches(0.015), Inches(4.8))

    # Column 2: Our Reproduction Observations
    add_divider(s15, Inches(6.8), Inches(1.85), Inches(2.0), Inches(0.03), COLOR_ACCENT_TEAL)
    tb_c2 = s15.shapes.add_textbox(Inches(6.8), Inches(1.95), w_crit, Inches(4.5))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = tf_c2.margin_bottom = 0

    add_bullet(tf_c2, "Our Reproduction Findings & Critical Observations:", "", 11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_c2, "1. Memory Footprint of Unrolled DAG:",
               "While synthesis runtime is polynomial O(K·E), memory consumption scales with K·|V| nodes and K·|E| edges. For extremely long horizons (K > 1,000), matrix unrolling requires sparse graph storage to avoid RAM bottlenecks.",
               9.5, Pt(6), prefix_color=COLOR_TEXT_PRIMARY)

    add_bullet(tf_c2, "2. Closed-Source Codebase Reconstruction:",
               "No public reference implementation was provided by the EMSOFT 2025 authors. All data structures, state-space equations, and benchmarks were reconstructed from scratch from the formal text.",
               9.5, Pt(6), prefix_color=COLOR_TEXT_PRIMARY)

    add_bullet(tf_c2, "3. Sensitivity to Sub-Millisecond Slacks:",
               "Zero-slack binding constraints require sub-microsecond OS dispatch accuracy. On standard non-real-time operating systems, scheduler jitter can violate tight upper bounds unless paired with real-time RTOS timers.",
               9.5, Pt(6), prefix_color=COLOR_ACCENT_ALERT)

    s15.notes_slide.notes_text_frame.text = (
        "Speaker 5 (Koneti Karthik): Slide 15 offers a critical reflection on model boundaries and reproduction challenges. "
        "We distinguish between author-acknowledged limitations and our own findings. The authors acknowledge that their framework "
        "assumes strictly deterministic task durations and static token rates, and that multi-iteration bounds require unrolling. "
        "In our independent reproduction, we identified that unrolled memory footprint requires careful sparse management for very large "
        "horizons. Furthermore, because no public codebase was provided, we fully reconstructed every algorithm from formal equations. "
        "Finally, binding zero-slack schedules require a hard real-time OS (RTOS) in deployment to prevent kernel timer jitter from "
        "violating upper bounds."
    )

    # =========================================================================
    # SLIDE 16: CONCLUSIONS & KEY TAKEAWAYS
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_canvas(s16)
    add_minimal_header(s16, "Conclusions: Four Key Findings from the EMSOFT 2025 Reproduction",
                       "15. Conclusions & Key Takeaways",
                       "Summary of theoretical contributions, empirical validations, and reproduction milestones.")

    w_take = Inches(5.6)

    # Finding 1 (Top-Left)
    add_divider(s16, Inches(0.8), Inches(1.85), Inches(1.8), Inches(0.03), COLOR_ACCENT_TEAL)
    tb_k1 = s16.shapes.add_textbox(Inches(0.8), Inches(1.95), w_take, Inches(2.2))
    tf_k1 = tb_k1.text_frame
    tf_k1.word_wrap = True
    tf_k1.margin_left = tf_k1.margin_right = tf_k1.margin_top = tf_k1.margin_bottom = 0
    add_bullet(tf_k1, "1. Algebraic Unification of Timing Bounds:",
               "Upper timing bounds do not require exponential combinatorial solvers. By expressing them as backward difference constraints with negative weights, they integrate seamlessly into (max, +) linear state-space systems without state-space explosion.",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    # Finding 2 (Top-Right)
    add_divider(s16, Inches(6.8), Inches(1.85), Inches(1.8), Inches(0.03), COLOR_ACCENT_TEAL)
    tb_k2 = s16.shapes.add_textbox(Inches(6.8), Inches(1.95), w_take, Inches(2.2))
    tf_k2 = tb_k2.text_frame
    tf_k2.word_wrap = True
    tf_k2.margin_left = tf_k2.margin_right = tf_k2.margin_top = tf_k2.margin_bottom = 0
    add_bullet(tf_k2, "2. Defect Elimination with Zero Makespan Penalty:",
               "In the semiconductor wafer cluster tool case study, synthesized schedules clamp transit dwell times to ≤ 3.0s (preventing thermal defects) while preserving the identical 36.0s makespan as greedy execution.",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    add_divider(s16, Inches(0.8), Inches(4.35), Inches(11.733), Inches(0.015), COLOR_DIVIDER)

    # Finding 3 (Bottom-Left)
    add_divider(s16, Inches(0.8), Inches(4.55), Inches(1.8), Inches(0.03), COLOR_ACCENT_TEAL)
    tb_k3 = s16.shapes.add_textbox(Inches(0.8), Inches(4.65), w_take, Inches(2.2))
    tf_k3 = tb_k3.text_frame
    tf_k3.word_wrap = True
    tf_k3.margin_left = tf_k3.margin_right = tf_k3.margin_top = tf_k3.margin_bottom = 0
    add_bullet(tf_k3, "3. Sub-Second Polynomial Tractability:",
               "The synthesis engine scales as O(K·E), executing 1,000 task firings in ~154 ms, compared to >300s timeout for MILP solvers. This computational tractability enables online dynamic schedule reconfiguration on embedded microcontrollers.",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    # Finding 4 (Bottom-Right)
    add_divider(s16, Inches(6.8), Inches(4.55), Inches(1.8), Inches(0.03), COLOR_ACCENT_TEAL)
    tb_k4 = s16.shapes.add_textbox(Inches(6.8), Inches(4.65), w_take, Inches(2.2))
    tf_k4 = tb_k4.text_frame
    tf_k4.word_wrap = True
    tf_k4.margin_left = tf_k4.margin_right = tf_k4.margin_top = tf_k4.margin_bottom = 0
    add_bullet(tf_k4, "4. 100% Reproduction & Verification Fidelity:",
               "All mathematical closures, state-space transformations, phase transitions, and independent validations were confirmed across 28 automated test cases with zero warnings and numerical error ε ≤ 10^{-9}.",
               10, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    s16.notes_slide.notes_text_frame.text = (
        "Speaker 1 (Sk J Ur Rahaman): To conclude our presentation on slide 16, our evaluation yields four definitive findings: "
        "First, upper timing bounds can be algebraically unified into max-plus linear state-space systems without exponential solvers. "
        "Second, synthesized schedules completely eliminate physical dwell defects in semiconductor manufacturing with zero makespan penalty. "
        "Third, polynomial runtime scaling enables sub-second synthesis across 1,000 task firings, unlocking real-time embedded dynamic "
        "scheduling. Fourth, our independent Python implementation verified all paper claims across 28 automated test cases with 100% pass rate."
    )

    # =========================================================================
    # SLIDE 17: DEDICATED REFERENCES (COMPLETE FORMAL CITATIONS)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_canvas(s17)
    add_minimal_header(s17, "Complete Bibliographic Citations: Research Paper & Foundational Literature",
                       "16. References",
                       "Formal bibliographic records, verified DOIs, and foundational max-plus dataflow literature.")

    # Left Column: Primary Research Paper & Dataflow Foundations (Width: 5.6")
    tb_r1 = s17.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(5.6), Inches(4.8))
    tf_r1 = tb_r1.text_frame
    tf_r1.word_wrap = True
    tf_r1.margin_left = tf_r1.margin_top = tf_r1.margin_right = tf_r1.margin_bottom = 0

    add_bullet(tf_r1, "Primary Assigned Research Paper:", "", 11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_r1, "[1] J. van Wanrooij, T. Basten, and M. Geilen,",
               "\"Schedule synthesis for synchronous dataflow models with lower and upper timing bounds,\" ACM Transactions on Embedded Computing Systems (TECS), Vol. 24, Issue 5s, Article 143, pp. 1–25, Oct. 2025 (Presented at EMSOFT 2025).\nDOI: 10.1145/3762643.",
               9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)

    add_bullet(tf_r1, "Foundational Dataflow Literature:", "", 11, Pt(8), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_r1, "[2] E. A. Lee and D. G. Messerschmitt,",
               "\"Synchronous data flow,\" Proceedings of the IEEE, Vol. 75, No. 9, pp. 1235–1245, Sept. 1987.\nDOI: 10.1109/PROC.1987.13876.",
               9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_r1, "[3] S. S. Bhattacharyya, P. K. Murthy, and E. A. Lee,",
               "Software Synthesis from Dataflow Graphs, Kluwer Academic Publishers, Norwell, MA, USA, 1996.\nISBN: 978-0792397229.",
               9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)

    # Vertical divider
    add_divider(s17, Inches(6.6), Inches(1.95), Inches(0.015), Inches(4.8))

    # Right Column: Max-Plus Linear Systems & Semiring Theory (Width: 5.8")
    tb_r2 = s17.shapes.add_textbox(Inches(6.8), Inches(1.95), Inches(5.733), Inches(4.8))
    tf_r2 = tb_r2.text_frame
    tf_r2.word_wrap = True
    tf_r2.margin_left = tf_r2.margin_top = tf_r2.margin_right = tf_r2.margin_bottom = 0

    add_bullet(tf_r2, "Max-Plus Linear Systems & Semiring Algebra:", "", 11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_r2, "[4] F. L. Baccelli, G. Cohen, G. J. Olsder, and J. P. Quadrat,",
               "Synchronization and Linearity: An Algebra for Discrete Event Systems, John Wiley & Sons, New York, 1992.\nISBN: 978-0471936091.",
               9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_r2, "[5] R. M. Karp,",
               "\"A characterization of the minimum cycle mean in a digraph,\" Discrete Mathematics, Vol. 23, No. 3, pp. 309–311, 1978.\nDOI: 10.1016/0012-365X(78)90011-0.",
               9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_r2, "[6] R. A. Cuninghame-Green,",
               "Minimax Algebra, Lecture Notes in Economics and Mathematical Systems, Vol. 166, Springer-Verlag, Berlin, 1979.\nDOI: 10.1007/978-3-642-48708-8.",
               9.5, Pt(3), prefix_color=COLOR_TEXT_PRIMARY)

    add_bullet(tf_r2, "Bibliographic Traceability:",
               "All mathematical models, Kleene star closures, and cycle ratio algorithms have been verified directly against these foundational sources.",
               9.5, Pt(8), prefix_color=COLOR_ACCENT_TEAL)

    s17.notes_slide.notes_text_frame.text = (
        "Speaker 1 (Sk J Ur Rahaman): On slide 17, we present our complete bibliographic citations. Our primary research foundation "
        "is the EMSOFT 2025 paper by Joep van Wanrooij, Twan Basten, and Marc Geilen from TU Eindhoven, published in ACM TECS, "
        "DOI 10.1145/3762643. We contextualize their contributions against foundational dataflow theory by Lee and Messerschmitt (1987) "
        "and Bhattacharyya et al. (1996), as well as foundational max-plus linear system theory from Baccelli, Cohen, Olsder, and Quadrat (1992), "
        "Karp's cycle mean algorithm (1978), and Cuninghame-Green's minimax algebra (1979)."
    )

    # =========================================================================
    # SLIDE 18: TEAM CONTRIBUTIONS & INTERACTIVE Q&A
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_canvas(s18)
    add_minimal_header(s18, "Verified Team Contributions and Interactive Discussion",
                       "17. Team Allocation & Q&A",
                       "Verified IIT Kanpur group member allocations (100% equal share), project deliverables, and open discussion.")

    # Left Column: Team Allocation (Width: 5.6")
    tb_team = s18.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(5.6), Inches(3.6))
    tf_team = tb_team.text_frame
    tf_team.word_wrap = True
    tf_team.margin_left = tf_team.margin_top = tf_team.margin_right = tf_team.margin_bottom = 0

    add_bullet(tf_team, "CS637 Team Allocation (Total = 100%):", "", 11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)

    team_members = [
        ("Sk J Ur Rahaman", "230951", "Project Lead, Max-plus semiring matrix engine, state-space transformation, Kleene star closure"),
        ("Sanga Badri", "230911", "Extended HSDFG model, multi-rate SDF topology balance analysis, actor serialization converter"),
        ("Ampili Hemanth Kumar", "230128", "Bellman-Ford ASAP schedule synthesis engine, cycle conflict extraction, unrolled DAG generation"),
        ("Vempati Prem Santhosh", "231137", "Decoupled independent validator oracle, automated 28-case test suite, error residual checks"),
        ("Koneti Karthik", "230568", "Benchmark execution pipeline, bound tightness parameter sweeps, presentation engineering")
    ]

    for name, roll, role in team_members:
        add_bullet(tf_team, f"• {name} (Roll: {roll}, CSE) — 20%:",
                   role, 9.5, Pt(3.5), prefix_color=COLOR_TEXT_PRIMARY)

    # Vertical divider
    add_divider(s18, Inches(6.6), Inches(1.95), Inches(0.015), Inches(3.6))

    # Right Column: Verified Project Deliverables (Width: 5.8")
    tb_deliv = s18.shapes.add_textbox(Inches(6.8), Inches(1.95), Inches(5.733), Inches(3.6))
    tf_deliv = tb_deliv.text_frame
    tf_deliv.word_wrap = True
    tf_deliv.margin_left = tf_deliv.margin_top = tf_deliv.margin_right = tf_deliv.margin_bottom = 0

    add_bullet(tf_deliv, "Verified Project Deliverables & Artifacts:", "", 11, Pt(0), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_deliv, "• Python Codebase & Test Suite:", "28/28 automated unit & integration tests passing in 0.17 seconds (src/ and tests/).", 9.5, Pt(3.5), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_deliv, "• Benchmark Verification Suite:", "EXP-1 (Manufacturing Case Study), EXP-2 (Tightness Sweeps), EXP-3 (Scalability), EXP-4 (Slack Analysis).", 9.5, Pt(3.5), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_deliv, "• Full Traceability Document:", "CS637_Source_and_Claim_Check.md detailing claim-by-claim verification and tool audit.", 9.5, Pt(3.5), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_deliv, "• Presentation Artifacts:", "CS637_Project_Presentation_Minimal.pptx, vector PDF, 1080p slide PNGs, and 6x3 contact sheet.", 9.5, Pt(3.5), prefix_color=COLOR_TEXT_PRIMARY)

    # Horizontal divider above Q&A
    add_divider(s18, Inches(0.8), Inches(5.65), Inches(11.733), Inches(0.015), COLOR_DIVIDER)

    # Q&A Banner
    tb_qa = s18.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.2))
    tf_qa = tb_qa.text_frame
    tf_qa.word_wrap = True
    tf_qa.margin_left = tf_qa.margin_top = tf_qa.margin_right = tf_qa.margin_bottom = 0

    p_qa = tf_qa.paragraphs[0]
    p_qa.text = "QUESTIONS & DISCUSSION"
    p_qa.font.name = FONT_HEADING
    p_qa.font.size = Pt(13)
    p_qa.font.bold = True
    p_qa.font.color.rgb = COLOR_ACCENT_TEAL

    p_qa_sub = tf_qa.add_paragraph()
    p_qa_sub.text = "Thank you for your attention. The IIT Kanpur CS637 team welcomes your questions on max-plus semiring linearization, state-space matrix transformations, schedule synthesis algorithms, and experimental validation."
    p_qa_sub.font.name = FONT_BODY
    p_qa_sub.font.size = Pt(10.5)
    p_qa_sub.font.color.rgb = COLOR_TEXT_SECONDARY
    p_qa_sub.space_before = Pt(3)

    s18.notes_slide.notes_text_frame.text = (
        "Speaker 1 (Sk J Ur Rahaman): On slide 18, we present our verified team contribution breakdown and open the floor to questions. "
        "Our five team members—Sk J Ur Rahaman, Sanga Badri, Ampili Hemanth Kumar, Vempati Prem Santhosh, and Koneti Karthik—each "
        "contributed an exact 20% equal share across modeling, semiring algebra, schedule synthesis, independent validation, and "
        "experimental analysis. All code, test suites, and presentation deliverables are verified and complete. Thank you very much, "
        "and we are now open to your questions."
    )

    # -----------------------------------------------------------------------
    # SAVE PRESENTATION
    # -----------------------------------------------------------------------
    prs.save(PPTX_TARGET)
    prs.save(ROOT_PPTX_TARGET)
    print(f"Successfully generated deck with {len(prs.slides)} slides:")
    print(f"  - {PPTX_TARGET}")
    print(f"  - {ROOT_PPTX_TARGET}")


if __name__ == "__main__":
    build_deck()
