"""
Generate the completely redesigned CS637 academic presentation:
- Pure Canva-quality art direction:
  - Generous negative space, open layouts, NO rounded card containers.
  - Large typographic contrast and deliberate visual hierarchy.
  - Straight alignment lines and fine dividers instead of enclosing boxes.
  - Large integrated numbers placed directly in content.
  - High-resolution, custom-generated technical visuals taking center stage.
  - Coherent semantic palette: Deep Navy (#0F172A), Electric Blue (#2563EB),
    Teal (#0D9488), Crimson/Orange (#DC2626), Slate (#475569), Light Divider (#E2E8F0).
  - Clean typographic team allocation (5 members x 20% = 100%).
  - Full speaker notes on all 16 slides.
- Generates:
  - presentation/CS637_Project_Presentation_Canva_Style.pptx
  - CS637_Project_Presentation_Canva_Style.pptx (workspace root)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = "presentation"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PPTX_TARGET = os.path.join(OUTPUT_DIR, "CS637_Project_Presentation_Canva_Style.pptx")
ROOT_PPTX_TARGET = "CS637_Project_Presentation_Canva_Style.pptx"

# ---------------------------------------------------------------------------
# DESIGN TOKEN PALETTE (Editorial Academic Profile)
# ---------------------------------------------------------------------------
COLOR_BG_LIGHT = RGBColor(253, 253, 254)       # Clean subtle ivory/white
COLOR_BG_HERO = RGBColor(15, 23, 42)           # #0F172A (Deep Midnight Navy)
COLOR_TEXT_PRIMARY = RGBColor(15, 23, 42)      # #0F172A
COLOR_TEXT_WHITE = RGBColor(255, 255, 255)     # #FFFFFF
COLOR_TEXT_SLATE = RGBColor(71, 85, 105)       # #475569 (Slate 600)
COLOR_TEXT_MUTED = RGBColor(148, 163, 184)     # #94A3B8 (Slate 400)

COLOR_ACCENT_BLUE = RGBColor(37, 99, 235)      # #2563EB (Electric Blue)
COLOR_ACCENT_TEAL = RGBColor(13, 148, 136)     # #0D9488 (Teal 600)
COLOR_ACCENT_ALERT = RGBColor(220, 38, 38)     # #DC2626 (Crimson 600)
COLOR_ACCENT_AMBER = RGBColor(217, 119, 6)     # #D97706 (Amber 600)

COLOR_DIVIDER = RGBColor(226, 232, 240)        # #E2E8F0 (Fine Slate Rule)
COLOR_DIVIDER_DARK = RGBColor(30, 41, 59)      # #1E293B (Dark Divider)
COLOR_SURFACE_LIGHT = RGBColor(248, 250, 252)  # #F8FAFC (Soft Tint)

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_MONO = "Consolas"


def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # -----------------------------------------------------------------------
    # HELPER UTILITIES (CANVA EDITORIAL SYSTEM)
    # -----------------------------------------------------------------------
    def set_canvas(slide, dark=False):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG_HERO if dark else COLOR_BG_LIGHT
        bg.line.fill.background()
        return bg

    def add_editorial_header(slide, title_text, category_eyebrow, subtitle_text="", dark=False):
        """Clean typographic header with generous negative space, bold headline, and no enclosing box."""
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.40), Inches(11.733), Inches(1.22))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Category Eyebrow
        p_eye = tf.paragraphs[0]
        p_eye.text = category_eyebrow.upper()
        p_eye.font.name = FONT_HEADING
        p_eye.font.size = Pt(10.5)
        p_eye.font.bold = True
        p_eye.font.color.rgb = RGBColor(56, 189, 248) if dark else COLOR_ACCENT_BLUE

        # Action Headline (24-26 pt bold, clean and authoritative)
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT_WHITE if dark else COLOR_TEXT_PRIMARY
        p_title.space_before = Pt(3)

        # Subtitle / Takeaway
        if subtitle_text:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle_text
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(11.5)
            p_sub.font.color.rgb = COLOR_TEXT_MUTED if dark else COLOR_TEXT_SLATE
            p_sub.space_before = Pt(3)

        # Fine accent rule below header
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.8), Inches(1.68), Inches(11.733), Inches(0.015)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_DIVIDER_DARK if dark else COLOR_DIVIDER
        line.line.fill.background()

    def add_divider_line(slide, left, top, width, height=Inches(0.015), color=COLOR_DIVIDER):
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        line.fill.solid()
        line.fill.fore_color.rgb = color
        line.line.fill.background()
        return line

    def add_bullet(tf, bold_prefix, text, pt_size=11, space_before=Pt(6),
                   text_color=COLOR_TEXT_PRIMARY, prefix_color=COLOR_ACCENT_BLUE):
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

    def add_integrated_stat(slide, left, top, value_str, label_str, num_color=COLOR_ACCENT_BLUE, width=Inches(2.7), height=Inches(0.95)):
        """Open typographic metric without card borders or shadows."""
        tb = slide.shapes.add_textbox(left, top, width, height)
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = value_str
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = num_color

        p2 = tf.add_paragraph()
        p2.text = label_str
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_SLATE
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (EDITORIAL HERO)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_canvas(s1, dark=True)

    # Accent decorative top bar
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.06))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_ACCENT_BLUE
    top_bar.line.fill.background()

    # Title & Metadata Block
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.733), Inches(2.2))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0

    p_badge = tf_t.paragraphs[0]
    p_badge.text = "EMSOFT 2025 / ACM TECS RESEARCH REPRODUCTION"
    p_badge.font.name = FONT_HEADING
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = RGBColor(56, 189, 248)

    p_main = tf_t.add_paragraph()
    p_main.text = "Schedule Synthesis for Synchronous Dataflow Models\nwith Lower and Upper Timing Bounds"
    p_main.font.name = FONT_HEADING
    p_main.font.size = Pt(28)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_TEXT_WHITE
    p_main.space_before = Pt(6)

    p_sub = tf_t.add_paragraph()
    p_sub.text = "Formal (max, +) State-Space Algebra, Polynomial-Time Synthesis, and Semiconductor Wafer Cluster Tool Validation"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = COLOR_TEXT_MUTED
    p_sub.space_before = Pt(6)

    # Fine divider
    add_divider_line(s1, Inches(0.8), Inches(3.05), Inches(11.733), Inches(0.015), COLOR_DIVIDER_DARK)

    # Hero Visual: Abstract Dataflow Timeline Graphic
    img_title = "figures_canva/fig_title_graphic.png"
    if os.path.exists(img_title):
        # Spans across slide with proper aspect ratio and centered negative space
        s1.shapes.add_picture(img_title, Inches(0.8), Inches(3.25), width=Inches(11.733), height=Inches(2.85))

    # Bottom Metadata & Team Credit Line
    add_divider_line(s1, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.015), COLOR_DIVIDER_DARK)

    tb_footer = s1.shapes.add_textbox(Inches(0.8), Inches(6.38), Inches(11.733), Inches(0.85))
    tf_f = tb_footer.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0

    p_cite = tf_f.paragraphs[0]
    p_cite.text = "Paper: Joep van Wanrooij, Twan Basten, Marc Geilen (TU Eindhoven) | ACM TECS Vol. 24, Issue 5s, Art. 143 (EMSOFT 2025) | DOI: 10.1145/3762643"
    p_cite.font.size = Pt(10)
    p_cite.font.color.rgb = COLOR_TEXT_MUTED

    p_team = tf_f.add_paragraph()
    p_team.text = "CS637 Reproduction Team (IIT Kanpur): Sk J Ur Rahaman (Lead), Sanga Badri, Ampili Hemanth Kumar, Vempati Prem Santhosh, Koneti Karthik — 20% Equal Contribution Each"
    p_team.font.size = Pt(10)
    p_team.font.bold = True
    p_team.font.color.rgb = RGBColor(203, 213, 225)
    p_team.space_before = Pt(3)

    s1.notes_slide.notes_text_frame.text = (
        "Speaker 1 (Sk J Ur Rahaman): Welcome to our comprehensive evaluation and reproduction of the EMSOFT 2025 research "
        "paper titled 'Schedule synthesis for synchronous dataflow models with lower and upper timing bounds' by Joep van Wanrooij, "
        "Twan Basten, and Marc Geilen from the Eindhoven University of Technology, published in ACM Transactions on Embedded Computing "
        "Systems, DOI 10.1145/3762643. Our team from the Department of Computer Science and Engineering at IIT Kanpur has fully "
        "reproduced and verified the mathematical foundations, (max, +) state-space transformations, schedule synthesis algorithms, "
        "and industrial case studies presented in this paper. Each of our five group members contributed equally, exactly 20%, to this project."
    )

    # =========================================================================
    # SLIDE 2: THE CYBER-PHYSICAL SCHEDULING PROBLEM
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_canvas(s2)
    add_editorial_header(s2, "Upper Timing Bounds Break Conventional Dataflow: Self-Timed Firing Causes Physical Defects",
                         "01. Motivation & Problem Statement",
                         "Standard SDF assumes only lower bounds (data readiness). Cyber-physical systems impose critical upper bounds that break greedy scheduling.")

    # Top Left Column: Editorial narrative (Width: 5.4")
    tb_s2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(5.4), Inches(3.2))
    tf_s2 = tb_s2.text_frame
    tf_s2.word_wrap = True
    tf_s2.margin_left = tf_s2.margin_top = tf_s2.margin_right = tf_s2.margin_bottom = 0

    add_bullet(tf_s2, "The Dataflow Legacy:",
               "Synchronous dataflow traditionally executes in a self-timed (greedy) manner: actors fire as soon as input tokens arrive.", 11.5)
    add_bullet(tf_s2, "Real Physical Constraints:",
               "Cyber-physical systems enforce strict maximum separation limits (upper bounds):", 11.5, space_before=Pt(6))
    add_bullet(tf_s2, "• Semiconductor Fabrication:", "Hot wafers cannot dwell in transit longer than 3.0 s before etching without severe thermal degradation.", 11, space_before=Pt(3), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_s2, "• Automotive / Robotics:", "Sensor tokens become stale; late processing destabilizes real-time feedback loops.", 11, space_before=Pt(3), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_s2, "• Video DSP Pipelines:", "Premature frames overflow bounded hardware display buffers.", 11, space_before=Pt(3), prefix_color=COLOR_TEXT_PRIMARY)

    # Top Right Column: Technical Visual Diagram
    img_dwell = "figures_canva/fig_wafer_dwell_concept.png"
    if os.path.exists(img_dwell):
        s2.shapes.add_picture(img_dwell, Inches(6.5), Inches(1.85), width=Inches(6.0), height=Inches(2.5))
        tb_dcap = s2.shapes.add_textbox(Inches(6.5), Inches(4.45), Inches(6.0), Inches(0.65))
        tf_dc = tb_dcap.text_frame
        tf_dc.word_wrap = True
        tf_dc.margin_left = tf_dc.margin_top = tf_dc.margin_right = tf_dc.margin_bottom = 0
        p_dc = tf_dc.paragraphs[0]
        p_dc.text = "Downstream chamber contention traps Wafer 3 in transit, extending dwell from 0 s to 6.0 s (100% violation of thermal limit) under greedy scheduling."
        p_dc.font.name = FONT_BODY
        p_dc.font.size = Pt(9.5)
        p_dc.font.italic = True
        p_dc.font.color.rgb = COLOR_TEXT_SLATE

    # Full-width horizontal divider
    add_divider_line(s2, Inches(0.8), Inches(5.25), Inches(11.733), Inches(0.015))

    # Bottom: 3 Integrated Metrics across full slide width (no overlapping boxes)
    add_integrated_stat(s2, Inches(0.8), Inches(5.45), "3.0 s", "Physical Upper Bound Dwell Limit (Critical Thermal Decay Threshold)", COLOR_ACCENT_BLUE, width=Inches(3.6))
    add_integrated_stat(s2, Inches(4.8), Inches(5.45), "6.0 s", "Greedy Dwell Overflow (+100% Violation Ruins Wafer Yield)", COLOR_ACCENT_ALERT, width=Inches(3.6))
    add_integrated_stat(s2, Inches(8.8), Inches(5.45), "3.0 s", "Synthesized Schedule Dwell (100% Bound Adherence, 0% Makespan Loss)", COLOR_ACCENT_TEAL, width=Inches(3.7))

    s2.notes_slide.notes_text_frame.text = (
        "Speaker 1 (Sk J Ur Rahaman): Synchronous Dataflow has long served as a premier formal model for streaming embedded architectures. "
        "Traditionally, SDF assumes monotonic self-timed execution: actors fire as soon as their preceding tasks produce tokens. In standard "
        "timed systems, this only models lower bounds. However, in cyber-physical domains such as semiconductor manufacturing, upper timing bounds "
        "are essential physical constraints. As shown in our comparison diagram, when wafers are scheduled greedily, downstream chamber contention "
        "causes wafer transit dwell times to escalate to 4.0 seconds and 6.0 seconds, severely violating the 3.0-second limit and ruining wafer yields. "
        "The proposed synthesis introduces deliberate upstream delays, clamping dwell to exactly 3.0 seconds with zero makespan penalty."
    )

    # =========================================================================
    # SLIDE 3: SYNCHRONOUS DATAFLOW & MULTI-RATE EXPANSION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_canvas(s3)
    add_editorial_header(s3, "Synchronous Dataflow Foundations: Multi-Rate Balance and Homogeneous Expansion",
                         "02. Theoretical Background",
                         "Static balance equations ensure bounded buffer memory; multi-rate conversion requires explicit serialization channels.")

    # Left Column: Editorial narrative
    tb_s3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(5.0), Inches(4.8))
    tf_s3 = tb_s3.text_frame
    tf_s3.word_wrap = True
    tf_s3.margin_left = tf_s3.margin_top = tf_s3.margin_right = tf_s3.margin_bottom = 0

    add_bullet(tf_s3, "1. SDF Graph Semantics:",
               "A multigraph G = (V, E, prd, cns, d, w) where actors v in V have execution durations w(v) >= 0. Directed channels e in E transfer discrete data tokens with initial delays d(e).", 11.5)
    add_bullet(tf_s3, "2. Topology Matrix & Repetition Vector:",
               "The topology matrix Gamma satisfies Gamma · q = 0 for minimal non-trivial integer vector q. A positive repetition vector guarantees bounded memory and deadlock freedom over infinite iterations.", 11.5, space_before=Pt(8))
    add_bullet(tf_s3, "3. Homogeneous Expansion (HSDF):",
               "Every consistent multi-rate SDF graph is converted into an equivalent HSDF graph where all rates are exactly 1 (prd = cns = 1) by replicating actor v into q(v) instances.", 11.5, space_before=Pt(8))
    add_bullet(tf_s3, "4. Actor Sequentiality Preservation:",
               "Crucial reproduction insight: Single-threaded actors cannot fire concurrently. Explicit serialization channels must be added (v_i -> v_{i+1} with d=0, and v_{q-1} -> v_0 with d=1) to prevent illegal overlapping self-firings.", 11.5, space_before=Pt(8), prefix_color=COLOR_ACCENT_TEAL)

    # Right Column: Visual Diagram of Multi-Rate to HSDF
    img_mr = "figures_canva/fig_multirate_hsdf.png"
    if os.path.exists(img_mr):
        s3.shapes.add_picture(img_mr, Inches(6.1), Inches(1.85), width=Inches(6.4), height=Inches(2.8))
        add_divider_line(s3, Inches(6.1), Inches(4.85), Inches(6.4), Inches(0.015))
        tb_mr_call = s3.shapes.add_textbox(Inches(6.1), Inches(5.05), Inches(6.4), Inches(1.8))
        tf_mrc = tb_mr_call.text_frame
        tf_mrc.word_wrap = True
        tf_mrc.margin_left = tf_mrc.margin_top = tf_mrc.margin_right = tf_mrc.margin_bottom = 0
        add_bullet(tf_mrc, "Multi-Rate Expansion Rule:",
                   "q(A) · prd(e) = q(B) · cns(e) balances token rates across periods. Each channel expands into gcd(prd, cns) parallel HSDF paths.", 11)
        add_bullet(tf_mrc, "Single-Thread Invariance:",
                   "Sequentiality arcs v_i -> v_{i+1} with d=0 prevent unphysical parallel execution of the same actor across distinct sub-firings.", 11, space_before=Pt(4), prefix_color=COLOR_ACCENT_TEAL)

    s3.notes_slide.notes_text_frame.text = (
        "Speaker 2 (Sanga Badri): Slide 3 outlines the formal foundation of Synchronous Dataflow. An SDF graph consists of actors connected "
        "by FIFO channels with fixed production and consumption rates. Consistency requires the topology matrix Gamma to possess a non-trivial "
        "nullspace, yielding the repetition vector q that defines firing frequencies per periodic iteration. To synthesize schedules, general "
        "multi-rate graphs are expanded into Homogeneous SDF graphs where every rate is normalized to one. During our reproduction, we discovered "
        "that naive actor replication omits sequentiality constraints. We explicitly added intra-actor sequentiality arcs to preserve single-threaded "
        "execution semantics across all iterations."
    )

    # =========================================================================
    # SLIDE 4: RESEARCH GAP & ALGORITHMIC PARADIGMS
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_canvas(s4)
    add_editorial_header(s4, "Overcoming Combinatorial Explosion: Polynomial Synthesis via (max, +) Algebra",
                         "03. Research Gap & Contributions",
                         "Prior techniques suffered from exponential state-space blowup. The paper delivers a polynomial-time exact transformation.")

    # Clean comparison table across 4 paradigms
    table_shape = s4.shapes.add_table(5, 4, Inches(0.8), Inches(1.9), Inches(11.733), Inches(2.6))
    table = table_shape.table
    table.columns[0].width = Inches(2.4)
    table.columns[1].width = Inches(3.1)
    table.columns[2].width = Inches(2.8)
    table.columns[3].width = Inches(3.433)

    headers = ["Scheduling Approach", "Upper Bound Handling", "Computational Complexity", "Limitation / Practical Bottleneck"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_SURFACE_LIGHT
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

    rows_data = [
        ("Self-Timed / Greedy SDF", "Fails completely (cannot model upper bounds)", "O(V + E) (Linear)", "Violates critical deadlines; ruined physical yields"),
        ("MILP / SMT Solvers", "Supported via arbitrary inequality constraints", "Exponential O(2^n) worst-case", "Timeouts (> 300 s) at N >= 30 tasks with bidirectional bounds"),
        ("Timed Automata (UPPAAL)", "Supported via continuous clock variables", "PSPACE-complete (State explosion)", "Intractable for multi-iteration pipelines or high repetition rates"),
        ("Paper's (max, +) Synthesis", "Exact representation via backward difference arcs", "Polynomial O(n³ + K·m)", "Sub-second synthesis across 1,000+ task firings with zero makespan loss"),
    ]

    for row_idx, row in enumerate(rows_data, 1):
        for col_idx, text in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            is_proposed = (row_idx == 4)
            cell.fill.fore_color.rgb = RGBColor(240, 253, 250) if is_proposed else COLOR_BG_LIGHT
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = FONT_BODY
            p.font.size = Pt(10.5)
            p.font.bold = is_proposed and (col_idx == 0 or col_idx == 2)
            p.font.color.rgb = COLOR_ACCENT_TEAL if is_proposed else COLOR_TEXT_PRIMARY

    # Bottom Callout: Key Architectural Contributions
    tb_contrib = s4.shapes.add_textbox(Inches(0.8), Inches(4.8), Inches(11.733), Inches(2.1))
    tf_c = tb_contrib.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0

    p_h = tf_c.paragraphs[0]
    p_h.text = "CORE CONTRIBUTIONS OF THE REPRODUCED PAPER"
    p_h.font.name = FONT_HEADING
    p_h.font.size = Pt(11.5)
    p_h.font.bold = True
    p_h.font.color.rgb = COLOR_ACCENT_BLUE

    add_bullet(tf_c, "1. Extended HSDFG Formalism:",
               "A unified mathematical model supporting lower (C_L) and upper (C_U) timing bounds across arbitrary event pairs and iteration offsets.", 11.5, space_before=Pt(4))
    add_bullet(tf_c, "2. State-Space Linearization:",
               "Mapping bidirectional constraints to (max, +) matrices (A_0, ..., A_D) where upper bounds become backward difference arcs.", 11.5, space_before=Pt(4))
    add_bullet(tf_c, "3. Exact Polynomial Synthesis:",
               "Longest-path Bellman-Ford synthesis that produces optimal ASAP start times while isolating conflicting bounds as positive cycles.", 11.5, space_before=Pt(4))

    s4.notes_slide.notes_text_frame.text = (
        "Speaker 2 (Sanga Badri): Slide 4 highlights the research gap motivating this work. Prior approaches faced an untenable compromise: "
        "self-timed dataflow is fast but fundamentally blind to upper bounds, while generic SMT and Integer Linear Programming solvers suffer "
        "from exponential runtime explosion and timeout on moderately sized graphs. Timed automata frameworks suffer from continuous clock "
        "explosion. The seminal contribution of van Wanrooij, Basten, and Geilen is showing that bidirectional timing bounds can be embedded "
        "directly into (max, +) state-space algebra, reducing schedule synthesis to exact polynomial-time matrix operations."
    )

    # =========================================================================
    # SLIDE 5: EXTENDED HSDFG & NORMALIZED TIMING BOUNDS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_canvas(s5)
    add_editorial_header(s5, "Extended HSDFG: Unifying Lower and Upper Bounds into Canonical Difference Form",
                         "04. Mathematical Formulation",
                         "Expressing arbitrary event-pair intervals as start-time inequalities where upper bounds reverse into backward constraints.")

    # Left Column: Mathematical derivations (Width: 5.1")
    tb_s5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(5.1), Inches(4.8))
    tf_s5 = tb_s5.text_frame
    tf_s5.word_wrap = True
    tf_s5.margin_left = tf_s5.margin_top = tf_s5.margin_right = tf_s5.margin_bottom = 0

    add_bullet(tf_s5, "1. Event Representation:",
               "Events are either start timestamps s_v(k) or completion timestamps c_v(k) = s_v(k) + w(v) for actor v in iteration k.", 11.5)
    add_bullet(tf_s5, "2. Lower-Bound Normalization (C_L):",
               "A lower bound E_dst(k) - E_src(k - delta) >= L enforces minimum separation. Normalizing to start times yields:", 11.5, space_before=Pt(6))
    add_bullet(tf_s5, "   s_dst(k) - s_src(k - delta) >= L'", "", 12, prefix_color=COLOR_TEXT_PRIMARY, space_before=Pt(2))
    add_bullet(tf_s5, "3. Upper-Bound Normalization (C_U):",
               "An upper bound E_dst(k) - E_src(k - delta) <= U enforces maximum allowable latency. Crucially, rewriting this inequality:", 11.5, space_before=Pt(6))
    add_bullet(tf_s5, "   s_src(k - delta) - s_dst(k) >= -U'", "", 12, prefix_color=COLOR_ACCENT_ALERT, space_before=Pt(2))
    add_bullet(tf_s5, "Key Insight:",
               "An upper bound from source to destination reverses direction into a backward difference arc with weight -U' and delay -delta!", 11.5, space_before=Pt(4), prefix_color=COLOR_ACCENT_ALERT)
    add_bullet(tf_s5, "4. Schedulability Theorem:",
               "A valid schedule exists if and only if the unified difference constraint graph contains NO directed cycles with strictly positive weight.", 11.5, space_before=Pt(6), prefix_color=COLOR_ACCENT_TEAL)

    # Right Column: Visual Diagram & Analytical Callout
    img_tb = "figures_canva/fig_timing_bounds_math.png"
    if os.path.exists(img_tb):
        s5.shapes.add_picture(img_tb, Inches(6.3), Inches(1.85), width=Inches(6.2), height=Inches(2.5))
        add_divider_line(s5, Inches(6.3), Inches(4.55), Inches(6.2), Inches(0.015))
        tb_tb_call = s5.shapes.add_textbox(Inches(6.3), Inches(4.75), Inches(6.2), Inches(2.0))
        tf_tbc = tb_tb_call.text_frame
        tf_tbc.word_wrap = True
        tf_tbc.margin_left = tf_tbc.margin_top = tf_tbc.margin_right = tf_tbc.margin_bottom = 0
        add_bullet(tf_tbc, "Reversal Transformation:",
                   "An upper bound constraint E_dst(k) - E_src(k - delta) <= U is normalized to start timestamps and rewritten as s_src(k - delta) - s_dst(k) >= -U'.", 11)
        add_bullet(tf_tbc, "Difference Graph Duality:",
                   "Every upper bound is algebraically dual to a backward channel with negative weight -U' and negative delay -delta. This unification enables longest-path polynomial synthesis.", 11, space_before=Pt(4), prefix_color=COLOR_ACCENT_ALERT)

    s5.notes_slide.notes_text_frame.text = (
        "Speaker 3 (Ampili Hemanth Kumar): Slide 5 details the paper's mathematical formulation. In an Extended HSDFG, timing constraints "
        "can be specified between any event pair—starts or completions—across intra- or inter-iteration delays. By substituting completion "
        "times with start time plus execution duration, every constraint is transformed into a standard difference constraint. The core "
        "mathematical revelation is that an upper bound inequality reverses direction: an upper bound on downstream task start relative "
        "to upstream completion becomes a backward difference constraint with negative weight. The entire system is feasible if and only "
        "if this difference graph contains no positive-weight cycles."
    )

    # =========================================================================
    # SLIDE 6: (max, +) SEMIRING ALGEBRA (SHOWCASE MATHEMATICAL SLIDE)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_canvas(s6)
    add_editorial_header(s6, "(max, +) Semiring: Turning Non-Linear Synchronization into Linear Matrix Algebra",
                         "05. Mathematical Foundations",
                         "Replacing arithmetic addition and multiplication with maximization and addition yields closed-form analytical tractability.")

    # 3 Open Editorial Columns with fine vertical dividers
    col_w = Inches(3.6)
    col_gap = Inches(0.466)
    c1_x = Inches(0.8)
    c2_x = c1_x + col_w + col_gap
    c3_x = c2_x + col_w + col_gap

    # Col 1: Semiring Axioms
    tb_c1 = s6.shapes.add_textbox(c1_x, Inches(1.85), col_w, Inches(4.8))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_top = tf_c1.margin_right = tf_c1.margin_bottom = 0

    p1 = tf_c1.paragraphs[0]
    p1.text = "1. SEMIRING OPERATORS & AXIOMS"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_ACCENT_BLUE

    add_bullet(tf_c1, "Carrier Set:", "R_max = R \u222a {-\u221e}", 11, space_before=Pt(5))
    add_bullet(tf_c1, "Max-Plus Addition (\u2295):", "a \u2295 b = max(a, b). Neutral element \u03b5 = -\u221e.", 11, space_before=Pt(5))
    add_bullet(tf_c1, "Max-Plus Product (\u2297):", "a \u2297 b = a + b. Identity element e = 0.", 11, space_before=Pt(5))
    add_bullet(tf_c1, "Absorbing Property:", "\u03b5 \u2297 a = -\u221e + a = -\u221e = \u03b5.", 11, space_before=Pt(5))
    add_bullet(tf_c1, "Matrix Product:", "[A \u2297 B]_ij = \u2a01_k (A_ik \u2297 B_kj) = max_k (A_ik + B_kj).", 11, space_before=Pt(5))
    add_bullet(tf_c1, "Vectorized Core:", "Vectorized via NumPy 3D tensor broadcasting for 20x faster state-space evaluation.", 11, space_before=Pt(5), prefix_color=COLOR_ACCENT_TEAL)

    add_divider_line(s6, c2_x - Inches(0.233), Inches(1.85), Inches(0.015), Inches(4.8))

    # Col 2: Kleene Star Closure
    tb_c2 = s6.shapes.add_textbox(c2_x, Inches(1.85), col_w, Inches(4.8))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_top = tf_c2.margin_right = tf_c2.margin_bottom = 0

    p2 = tf_c2.paragraphs[0]
    p2.text = "2. TRANSITIVE CLOSURE & KLEENE STAR"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_ACCENT_TEAL

    add_bullet(tf_c2, "Kleene Star Series:", "A* = I \u2295 A \u2295 A\u00b2 \u2295 ... \u2295 A^{n-1} = \u2a01_{k=0}^{n-1} A^k", 11, space_before=Pt(5))
    add_bullet(tf_c2, "Graph Interpretation:", "[A*]_ij equals the maximum-weight directed path from j to i.", 11, space_before=Pt(5))
    add_bullet(tf_c2, "Convergence Criterion:", "A* exists and is finite if and only if A contains NO cycles with strictly positive weight.", 11, space_before=Pt(5))
    add_bullet(tf_c2, "Floyd-Warshall Closure:", "Computed in exact O(n\u00b3) time, analytically resolving all intra-iteration zero-delay loops.", 11, space_before=Pt(5), prefix_color=COLOR_ACCENT_TEAL)

    add_divider_line(s6, c3_x - Inches(0.233), Inches(1.85), Inches(0.015), Inches(4.8))

    # Col 3: Spectral Theory
    tb_c3 = s6.shapes.add_textbox(c3_x, Inches(1.85), col_w, Inches(4.8))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    tf_c3.margin_left = tf_c3.margin_top = tf_c3.margin_right = tf_c3.margin_bottom = 0

    p3 = tf_c3.paragraphs[0]
    p3.text = "3. SPECTRAL THEORY & THROUGHPUT"
    p3.font.name = FONT_HEADING
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_ACCENT_ALERT

    add_bullet(tf_c3, "Max-Plus Eigenvalue:", "A \u2297 v = \u03bb \u2297 v, where scalar \u03bb is the maximum cycle mean.", 11, space_before=Pt(5))
    add_bullet(tf_c3, "Karp's Spectral Theorem:", "\u03bb*(A) = max_{cycles C} [ weight(C) / length(C) ].", 11, space_before=Pt(5))
    add_bullet(tf_c3, "Sustainable Throughput:", "System throughput is \u0398 = 1 / \u03bb*. The minimum sustainable initiation interval is \u03bb*.", 11, space_before=Pt(5))
    add_bullet(tf_c3, "Polynomial Complexity:", "Karp's algorithm computes exact throughput in O(n \u00b7 m) operations without state unrolling.", 11, space_before=Pt(5), prefix_color=COLOR_ACCENT_ALERT)

    s6.notes_slide.notes_text_frame.text = (
        "Speaker 3 (Ampili Hemanth Kumar): Slide 6 introduces the algebraic machinery that makes this approach possible: the (max, +) semiring. "
        "By mapping maximization to addition and addition to multiplication, non-linear synchronization becomes linear matrix algebra. "
        "The Kleene star matrix closure computes all-pairs longest paths in O(n^3) time, resolving zero-delay constraints. Furthermore, "
        "Karp's theorem establishes that the unique max-plus eigenvalue gives the maximum cycle ratio, which defines the exact maximum sustainable "
        "throughput under all timing bounds."
    )

    # =========================================================================
    # SLIDE 7: STATE-SPACE TRANSFORMATION (EDITORIAL PIPELINE FLOW)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_canvas(s7)
    add_editorial_header(s7, "State-Space Model: Resolving Instantaneous Circularities via Kleene Star Closure",
                         "06. State-Space Formulation",
                         "Eliminating zero-delay algebraic loops and mapping multi-delay systems to canonical companion matrix form.")

    # 3 Horizontal Stages (Open editorial flow with zero card containers)
    # Stage 1: Implicit Recurrence
    tb_st1 = s7.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.733), Inches(1.4))
    tf_st1 = tb_st1.text_frame
    tf_st1.word_wrap = True
    tf_st1.margin_left = tf_st1.margin_top = tf_st1.margin_right = tf_st1.margin_bottom = 0

    p_st1_h = tf_st1.paragraphs[0]
    p_st1_h.text = "STAGE 1: IMPLICIT SYSTEM RECURRENCE"
    p_st1_h.font.name = FONT_HEADING
    p_st1_h.font.size = Pt(12)
    p_st1_h.font.bold = True
    p_st1_h.font.color.rgb = COLOR_ACCENT_BLUE

    p_eq1 = tf_st1.add_paragraph()
    p_eq1.text = "x(k) = A_0 \u2297 x(k)  \u2295  \u2a01_{d=1}^D A_d \u2297 x(k - d)"
    p_eq1.font.name = FONT_MONO
    p_eq1.font.size = Pt(14)
    p_eq1.font.bold = True
    p_eq1.font.color.rgb = COLOR_TEXT_PRIMARY
    p_eq1.space_before = Pt(4)

    p_desc1 = tf_st1.add_paragraph()
    p_desc1.text = "Matrix A_0 contains intra-iteration (delay d=0) forward precedence channels and backward upper bounds. The equation is implicit because x(k) appears on both sides!"
    p_desc1.font.name = FONT_BODY
    p_desc1.font.size = Pt(11)
    p_desc1.font.color.rgb = COLOR_TEXT_SLATE
    p_desc1.space_before = Pt(2)

    add_divider_line(s7, Inches(0.8), Inches(3.40), Inches(11.733), Inches(0.015))

    # Stage 2: Kleene Star Closure
    tb_st2 = s7.shapes.add_textbox(Inches(0.8), Inches(3.55), Inches(11.733), Inches(1.4))
    tf_st2 = tb_st2.text_frame
    tf_st2.word_wrap = True
    tf_st2.margin_left = tf_st2.margin_top = tf_st2.margin_right = tf_st2.margin_bottom = 0

    p_st2_h = tf_st2.paragraphs[0]
    p_st2_h.text = "STAGE 2: KLEENE STAR CLOSURE & FEASIBILITY RESOLUTION"
    p_st2_h.font.name = FONT_HEADING
    p_st2_h.font.size = Pt(12)
    p_st2_h.font.bold = True
    p_st2_h.font.color.rgb = COLOR_ACCENT_TEAL

    p_eq2 = tf_st2.add_paragraph()
    p_eq2.text = "x(k) = M_0* \u2297 [ \u2a01_{d=1}^D A_d \u2297 x(k - d) ]      where M_0* = A_0* = \u2a01_{k=0}^{n-1} A_0^k"
    p_eq2.font.name = FONT_MONO
    p_eq2.font.size = Pt(14)
    p_eq2.font.bold = True
    p_eq2.font.color.rgb = COLOR_TEXT_PRIMARY
    p_eq2.space_before = Pt(4)

    p_desc2 = tf_st2.add_paragraph()
    p_desc2.text = "Multiplying by Kleene closure M_0* eliminates algebraic loops in O(n\u00b3) time. Schedulability Check: If diag(M_0*) has any positive entry (> 0), an instantaneous positive cycle exists \u2192 INFEASIBLE!"
    p_desc2.font.name = FONT_BODY
    p_desc2.font.size = Pt(11)
    p_desc2.font.color.rgb = COLOR_TEXT_SLATE
    p_desc2.space_before = Pt(2)

    add_divider_line(s7, Inches(0.8), Inches(5.10), Inches(11.733), Inches(0.015))

    # Stage 3: Companion Form
    tb_st3 = s7.shapes.add_textbox(Inches(0.8), Inches(5.25), Inches(11.733), Inches(1.6))
    tf_st3 = tb_st3.text_frame
    tf_st3.word_wrap = True
    tf_st3.margin_left = tf_st3.margin_top = tf_st3.margin_right = tf_st3.margin_bottom = 0

    p_st3_h = tf_st3.paragraphs[0]
    p_st3_h.text = "STAGE 3: CANONICAL 1-STEP COMPANION MATRIX FORM"
    p_st3_h.font.name = FONT_HEADING
    p_st3_h.font.size = Pt(12)
    p_st3_h.font.bold = True
    p_st3_h.font.color.rgb = COLOR_ACCENT_ALERT

    p_eq3 = tf_st3.add_paragraph()
    p_eq3.text = "z(k) = A \u2297 z(k - 1)      where z(k) = [ x(k)\u1d40, x(k-1)\u1d40, ..., x(k-D+1)\u1d40 ]\u1d40"
    p_eq3.font.name = FONT_MONO
    p_eq3.font.size = Pt(14)
    p_eq3.font.bold = True
    p_eq3.font.color.rgb = COLOR_TEXT_PRIMARY
    p_eq3.space_before = Pt(4)

    p_desc3 = tf_st3.add_paragraph()
    p_desc3.text = "Companion matrix A has top block row [ M_0* \u2297 A_1, ..., M_0* \u2297 A_D ] and sub-diagonal identity blocks I. Simulates future iterations in O(1) step operations; Karp's cycle mean \u03bb*(A) yields exact throughput \u0398 = 1 / \u03bb*."
    p_desc3.font.name = FONT_BODY
    p_desc3.font.size = Pt(11)
    p_desc3.font.color.rgb = COLOR_TEXT_SLATE
    p_desc3.space_before = Pt(2)

    s7.notes_slide.notes_text_frame.text = (
        "Speaker 3 (Ampili Hemanth Kumar): Slide 7 presents the state-space transformation. In an Extended HSDFG, matrix A_0 contains both "
        "zero-delay forward dataflow channels and instantaneous backward upper bounds. This creates an implicit equation where x(k) depends "
        "on itself. The Kleene star closure M0* analytically resolves this circularity, making the state update purely explicit. For multi-delay "
        "systems, companion matrix augmentation creates a standard first-order recurrence z(k) = A o-times z(k-1), enabling linear simulation "
        "and throughput evaluation."
    )

    # =========================================================================
    # SLIDE 8: ALGORITHMIC SYNTHESIS & FLOWCHART
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_canvas(s8)
    add_editorial_header(s8, "Polynomial-Time Synthesis: Unrolled Bellman-Ford & Positive Cycle Conflict Isolation",
                         "07. Schedule Synthesis Algorithm",
                         "Calculating exact ASAP earliest start times and pinpointing conflicting upper/lower bounds in O(K · E) time.")

    # Top/Center: Visual Flowchart
    img_flow = "figures_canva/fig_flowchart_synthesis.png"
    if os.path.exists(img_flow):
        s8.shapes.add_picture(img_flow, Inches(2.2), Inches(1.85), width=Inches(8.933), height=Inches(3.25))

    # Fine divider
    add_divider_line(s8, Inches(0.8), Inches(5.25), Inches(11.733), Inches(0.015))

    # Bottom: Analytical Notes
    tb_fn = s8.shapes.add_textbox(Inches(0.8), Inches(5.45), Inches(11.733), Inches(1.6))
    tf_fn = tb_fn.text_frame
    tf_fn.word_wrap = True

    add_bullet(tf_fn, "Makespan Optimality:",
               "Computes As-Soon-As-Possible (ASAP) start times via longest-path propagation. Any smaller timestamp would violate at least one lower bound.", 11)
    add_bullet(tf_fn, "Positive Cycle Diagnostics:",
               "When conflicting bounds make a schedule mathematically impossible, Bellman-Ford isolates the exact loop with human-readable actor names.", 11, space_before=Pt(4), prefix_color=COLOR_ACCENT_ALERT)
    add_bullet(tf_fn, "Quantitative Slack Analysis:",
               "Slack sigma(e) = s_v(k) - (s_u(k-d) + W) distinguishes critical binding constraints (sigma = 0) from non-binding bounds (sigma > 0).", 11, space_before=Pt(4), prefix_color=COLOR_ACCENT_TEAL)

    s8.notes_slide.notes_text_frame.text = (
        "Speaker 4 (Vempati Prem Santhosh): Slide 8 outlines our ASAP schedule synthesis engine. Over a finite horizon of K iterations, the "
        "system unrolls into K times |V| nodes in a directed difference graph. We execute a Bellman-Ford longest-path relaxation in O(K · E) "
        "time. If all bounds are satisfiable, it outputs the mathematically earliest feasible start times, guaranteeing minimal makespan. "
        "If conflicting bounds exist, an additional relaxation pass triggers positive-cycle detection, isolating the contradictory loop and "
        "decoding flat indices into actor names."
    )

    # =========================================================================
    # SLIDE 9: MODULAR SOFTWARE ARCHITECTURE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_canvas(s9)
    add_editorial_header(s9, "Software Architecture: Vectorized Semiring Engine with Decoupled Independent Oracle",
                         "08. System Implementation & Architecture",
                         "Engineered for 100% reproducibility, zero proprietary solver dependencies, and cross-platform determinism.")

    # Center: Visual Architecture Diagram
    img_arch = "figures_canva/fig_architecture.png"
    if os.path.exists(img_arch):
        s9.shapes.add_picture(img_arch, Inches(2.6), Inches(1.85), width=Inches(8.133), height=Inches(3.25))

    # Fine divider
    add_divider_line(s9, Inches(0.8), Inches(5.25), Inches(11.733), Inches(0.015))

    # Bottom: Key Implementation Attributes
    tb_arch = s9.shapes.add_textbox(Inches(0.8), Inches(5.45), Inches(11.733), Inches(1.5))
    tf_ar = tb_arch.text_frame
    tf_ar.word_wrap = True

    add_bullet(tf_ar, "Vectorized Semiring:",
               "src/maxplus.py uses NumPy 3D tensor broadcasting to evaluate matrix multiplication in optimized C-level loops, accelerating closure routines by 20x.", 11)
    add_bullet(tf_ar, "Decoupled Verification Oracle:",
               "src/validator.py inspects raw start timestamps directly against physical specifications without referencing solver state, guaranteeing an unbiased check.", 11, space_before=Pt(3), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_ar, "100% Deterministic & Portable:",
               "Zero external solver dependencies (no CPLEX, Gurobi, or Z3 required). Executes identically on Windows, Linux, and macOS.", 11, space_before=Pt(3))

    s9.notes_slide.notes_text_frame.text = (
        "Speaker 4 (Vempati Prem Santhosh): Slide 9 illustrates our modular software architecture. Built from scratch in pure Python 3, "
        "the codebase is structured into five distinct modules: model.py defines dataflow elements and multi-rate expansion; maxplus.py "
        "provides semiring algebra with NumPy 3D tensor broadcasting; state_space.py transforms graphs into recurrence matrices; "
        "scheduler.py runs Bellman-Ford synthesis; and validator.py acts as a completely decoupled ground-truth oracle. The entire "
        "reproduction is self-contained with zero third-party solver dependencies."
    )

    # =========================================================================
    # SLIDE 10: TEST SUITE & VERIFICATION RESULTS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_canvas(s10)
    add_editorial_header(s10, "Comprehensive Test Suite: 28 Automated Tests with Decoupled Oracle",
                         "09. Verification & Quality Assurance",
                         "Every mathematical definition, state-space transformation, and boundary case verified warning-free in 0.17 seconds.")

    # Top Metrics Row (Integrated, open layout)
    add_integrated_stat(s10, Inches(0.8), Inches(1.85), "28 / 28", "Automated Tests Passing", COLOR_ACCENT_TEAL)
    add_integrated_stat(s10, Inches(3.8), Inches(1.85), "0.17 s", "Full Suite Execution Runtime", COLOR_ACCENT_BLUE)
    add_integrated_stat(s10, Inches(6.8), Inches(1.85), "100%", "Violation Detection Rate", COLOR_ACCENT_TEAL)
    add_integrated_stat(s10, Inches(9.8), Inches(1.85), "0", "Solver / Third-Party Deps", COLOR_TEXT_PRIMARY)

    add_divider_line(s10, Inches(0.8), Inches(2.80), Inches(11.733), Inches(0.015))

    # Clean Table for Test Modules
    table_s10 = s10.shapes.add_table(6, 4, Inches(0.8), Inches(3.0), Inches(11.733), Inches(3.6))
    t10 = table_s10.table
    t10.columns[0].width = Inches(2.4)
    t10.columns[1].width = Inches(1.4)
    t10.columns[2].width = Inches(6.433)
    t10.columns[3].width = Inches(1.5)

    th = ["Test Module", "Test Cases", "Scope & Verified Properties", "Status"]
    for c_i, txt in enumerate(th):
        c = t10.cell(0, c_i)
        c.fill.solid()
        c.fill.fore_color.rgb = COLOR_SURFACE_LIGHT
        p = c.text_frame.paragraphs[0]
        p.text = txt
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_PRIMARY

    test_rows = [
        ("tests/test_maxplus.py", "7 Tests", "Semiring axioms, vectorized matmult, Kleene star DAG closure, positive cycle detection, Karp's cycle mean", "PASS (100%)"),
        ("tests/test_model.py", "5 Tests", "Actor/channel dataclasses, multi-rate topology matrix, repetition vector q, HSDF expansion & sequentiality", "PASS (100%)"),
        ("tests/test_state_space.py", "3 Tests", "Matrices (A_0, ..., A_D), Kleene closure M0*, actor execution time bottleneck (A_1)_{vv} >= w(v)", "PASS (100%)"),
        ("tests/test_scheduler.py", "5 Tests", "ASAP makespan optimization, lower/upper bound compliance, slack analysis sigma(e), positive cycle detection", "PASS (100%)"),
        ("tests/test_validator.py", "8 Tests", "Independent oracle detecting precedence, lower bound, upper bound, non-negativity, and sequentiality errors", "PASS (100%)"),
    ]

    for r_i, r_data in enumerate(test_rows, 1):
        for c_i, val in enumerate(r_data):
            cell = t10.cell(r_i, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_BG_LIGHT
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(10)
            if c_i == 3:
                p.font.bold = True
                p.font.color.rgb = COLOR_ACCENT_TEAL
            elif c_i == 0:
                p.font.bold = True
                p.font.name = FONT_MONO
                p.font.color.rgb = COLOR_ACCENT_BLUE

    s10.notes_slide.notes_text_frame.text = (
        "Speaker 4 (Vempati Prem Santhosh): Slide 10 provides the empirical proof of our reproduction's correctness. Running python -m pytest "
        "executes 28 automated test cases across all modules in 0.17 seconds with zero warnings. Every mathematical operator, state-space "
        "transformation, and edge case is covered. Notably, our independent validator module includes negative tests that deliberately "
        "tamper with start times to confirm that precedence violations, dwell overflows, sequentiality breaches, and cyclic contradictions "
        "are caught with a 100% detection rate."
    )

    # =========================================================================
    # SLIDE 11: MANUFACTURING CASE STUDY SETUP
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_canvas(s11)
    add_editorial_header(s11, "Manufacturing Case Study: Semiconductor Wafer Cluster Tool with Dwell Bounds",
                         "10. Experimental Evaluation: Setup",
                         "Evaluating robotic transit, vacuum heating, and chemical etching under strict thermal degradation limits.")

    # Center Visual: Cluster Tool Hardware Workflow
    img_ct = "figures_canva/fig_cluster_tool_workflow.png"
    if os.path.exists(img_ct):
        s11.shapes.add_picture(img_ct, Inches(2.4), Inches(1.85), width=Inches(8.533), height=Inches(3.1))

    # Fine divider
    add_divider_line(s11, Inches(0.8), Inches(5.15), Inches(11.733), Inches(0.015))

    # Bottom: 2 Editorial Narrative Columns
    tb_ct1 = s11.shapes.add_textbox(Inches(0.8), Inches(5.35), Inches(5.6), Inches(1.8))
    tf_ct1 = tb_ct1.text_frame
    tf_ct1.word_wrap = True
    add_bullet(tf_ct1, "Physical Cluster Tool Workflow:",
               "Automated semiconductor processing where silicon wafers undergo thermal preparation and chemical etching: LoadLock -> Robot 1 (w=2s) -> PreHeat Chamber (w=4s) -> Robot 2 (w=2s) -> Process Chamber (w=6s) -> Cooling Chamber (w=4s) -> Unload (w=2s).", 11)

    tb_ct2 = s11.shapes.add_textbox(Inches(6.9), Inches(5.35), Inches(5.6), Inches(1.8))
    tf_ct2 = tb_ct2.text_frame
    tf_ct2.word_wrap = True
    add_bullet(tf_ct2, "Thermal Dwell Upper Bound Limit:",
               "Wafers must not dwell in transit between PreHeat completion and ProcessChamber start longer than 3.0 s: s_{Process}(k) - c_{PreHeat}(k) <= 3.0 s. Exceeding this limit causes thermal decay and ruins chip yield.", 11, prefix_color=COLOR_ACCENT_ALERT)
    add_bullet(tf_ct2, "Reproduction Hypothesis:", "Greedy scheduling will violate this dwell bound, whereas (max, +) synthesis will enforce it with zero makespan penalty.", 10.5, space_before=Pt(4), prefix_color=COLOR_ACCENT_TEAL)

    s11.notes_slide.notes_text_frame.text = (
        "Speaker 5 (Koneti Karthik): Slide 11 introduces our first major experimental benchmark: the semiconductor manufacturing cluster tool. "
        "In modern fabrication lines, silicon wafers are transferred between heating and chemical processing chambers by robotic arms. "
        "Chambers have single-wafer capacity, causing resource contention between consecutive wafer firings. Crucially, heated wafers must not "
        "dwell in transit longer than 3.0 seconds, otherwise rapid cooling degrades the chemical surface, ruining microchip yield. Our reproduction "
        "evaluates whether (max, +) synthesis can guarantee this upper bound without sacrificing throughput."
    )

    # =========================================================================
    # SLIDE 12: MANUFACTURING GANTT CHART ANALYSIS (CANVA DEDICATED GANTT)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_canvas(s12)
    add_editorial_header(s12, "Gantt Chart Proof: Upper Bounds Enforced with Zero Makespan Penalty",
                         "11. Manufacturing Case Study Results",
                         "Greedy scheduling causes 100% dwell overflow; state-space synthesis delays upstream firings to achieve perfection.")

    # Left Column: Dedicated Canva Gantt Chart
    img_gantt = "figures_canva/fig_gantt_canva.png"
    if os.path.exists(img_gantt):
        s12.shapes.add_picture(img_gantt, Inches(0.8), Inches(1.85), width=Inches(7.3), height=Inches(4.15))

    # Caption under Gantt Chart
    tb_gcap = s12.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(7.3), Inches(0.6))
    tf_gc = tb_gcap.text_frame
    tf_gc.word_wrap = True
    tf_gc.margin_left = tf_gc.margin_top = tf_gc.margin_right = tf_gc.margin_bottom = 0
    p_gc = tf_gc.paragraphs[0]
    p_gc.text = "Gantt execution trace across 4 wafer iterations: Greedy (top) creates 6.0s transit dwell; Synthesized (bottom) inserts deliberate preheat delays to clamp dwell to <= 3.0s."
    p_gc.font.name = FONT_BODY
    p_gc.font.size = Pt(9.5)
    p_gc.font.italic = True
    p_gc.font.color.rgb = COLOR_TEXT_SLATE

    # Fine Vertical Divider
    add_divider_line(s12, Inches(8.35), Inches(1.85), Inches(0.015), Inches(4.9))

    # Right Column: Typographic Evidence & Takeaways (Width: 4.1")
    add_integrated_stat(s12, Inches(8.65), Inches(1.85), "36.0 s", "Makespan Invariance (0.0% Throughput Penalty)", COLOR_ACCENT_BLUE, width=Inches(3.9))
    add_integrated_stat(s12, Inches(8.65), Inches(2.80), "3.0 s vs 6.0 s", "Synthesized Dwell vs Greedy Overflow (+100%)", COLOR_ACCENT_ALERT, width=Inches(3.9))

    add_divider_line(s12, Inches(8.65), Inches(3.85), Inches(3.9), Inches(0.015))

    tb_gtake = s12.shapes.add_textbox(Inches(8.65), Inches(4.0), Inches(3.9), Inches(2.8))
    tf_gt = tb_gtake.text_frame
    tf_gt.word_wrap = True
    tf_gt.margin_left = tf_gt.margin_top = tf_gt.margin_right = tf_gt.margin_bottom = 0

    add_bullet(tf_gt, "Greedy Failure:",
               "Wafer 2 dwell = 4.0s (+33% violation); Wafer 3 dwell = 6.0s (+100% violation!). Downstream contention traps wafers in transit, causing severe thermal degradation.", 10.5, prefix_color=COLOR_ACCENT_ALERT)
    add_bullet(tf_gt, "Synthesized Precision:",
               "State-space synthesis delays Wafer 2 PreHeat to t=11 and Wafer 3 to t=17, guaranteeing dwell <= 3.0s on all firings.", 10.5, space_before=Pt(6), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_gt, "Makespan Preservation:",
               "Both schedules complete all 4 wafers at t=36.0s. Complete upper bound compliance is achieved with zero throughput loss!", 10.5, space_before=Pt(6), prefix_color=COLOR_ACCENT_BLUE)

    s12.notes_slide.notes_text_frame.text = (
        "Speaker 5 (Koneti Karthik): Slide 12 presents our primary experimental reproduction result: the Gantt chart comparison. "
        "In the top plot, standard greedy scheduling causes severe dwell violations: Wafer 2 waits 4.0 seconds, and Wafer 3 waits 6.0 seconds—a "
        "100% violation of the 3.0-second limit that ruins microchip yield. In the bottom plot, our synthesized schedule automatically "
        "introduces deliberate upstream delays: Wafer 2 preheating is delayed to t=11 and Wafer 3 to t=17. As a result, both wafers arrive at "
        "the process chamber exactly on time with dwell clamped to 3.0 seconds. Both schedules finish at exactly 36.0 seconds—zero makespan penalty!"
    )

    # =========================================================================
    # SLIDE 13: DSP STREAMING BENCHMARKS & SLACK
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_canvas(s13)
    add_editorial_header(s13, "DSP Pipeline Benchmarks: Sharp Schedulability Threshold at Critical Path",
                         "12. DSP Streaming Benchmarks",
                         "Verifying the theoretical boundary between feasible execution and instant positive-cycle infeasibility.")

    # Dual Plots side by side
    img_dsp = "figures/fig2_dsp_throughput.png"
    img_slack = "figures/fig4_slack_distribution.png"

    if os.path.exists(img_dsp):
        s13.shapes.add_picture(img_dsp, Inches(0.8), Inches(1.85), width=Inches(5.7))
    if os.path.exists(img_slack):
        s13.shapes.add_picture(img_slack, Inches(6.8), Inches(1.85), width=Inches(5.7))

    # Bottom Editorial Takeaways
    add_divider_line(s13, Inches(0.8), Inches(5.65), Inches(11.733), Inches(0.015))

    tb_d1 = s13.shapes.add_textbox(Inches(0.8), Inches(5.80), Inches(5.6), Inches(1.3))
    tf_d1 = tb_d1.text_frame
    tf_d1.word_wrap = True
    add_bullet(tf_d1, "Schedulability Phase Transition (Left):",
               "In a 4-stage DSP pipeline with critical path latency L_crit = 16s, tightness alpha >= 1.0 yields feasible schedules verified by our oracle. When alpha < 1.0, Bellman-Ford instantly isolates a positive cycle in < 2 ms.", 10.5)

    tb_d2 = s13.shapes.add_textbox(Inches(6.8), Inches(5.80), Inches(5.7), Inches(1.3))
    tf_d2 = tb_d2.text_frame
    tf_d2.word_wrap = True
    add_bullet(tf_d2, "Slack Distribution Analysis (Right):",
               "Slack sigma(e) separates critical binding bounds (sigma = 0) that dictate system throughput from non-binding bounds (sigma > 0) that provide headroom for execution jitter.", 10.5, prefix_color=COLOR_ACCENT_TEAL)

    s13.notes_slide.notes_text_frame.text = (
        "Speaker 5 (Koneti Karthik): Slide 13 examines DSP streaming pipeline benchmarks. We evaluated a 4-stage pipeline across varying upper "
        "bound tightness factors alpha. The experiment confirms a sharp phase transition: for alpha >= 1.0, valid schedules are synthesized "
        "and independently verified. When alpha falls below 1.0, the upper bound is tighter than physical execution time, and our synthesis "
        "engine triggers positive-cycle detection in under 2 milliseconds. The slack distribution plot quantitatively distinguishes binding "
        "constraints from non-binding bounds."
    )

    # =========================================================================
    # SLIDE 14: COMPUTATIONAL SCALABILITY ANALYSIS
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_canvas(s14)
    add_editorial_header(s14, "Empirical Scalability: Sub-Second Synthesis Across 1,000+ Task Firings",
                         "13. Computational Performance",
                         "Empirical confirmation of polynomial scaling vs. exponential blowup and timeouts of traditional MILP/SMT solvers.")

    # Left: Scalability Plot & Analytical Callout
    img_scale = "figures/fig3_scalability.png"
    if os.path.exists(img_scale):
        s14.shapes.add_picture(img_scale, Inches(0.8), Inches(1.85), width=Inches(6.6), height=Inches(2.75))
        add_divider_line(s14, Inches(0.8), Inches(4.75), Inches(6.6), Inches(0.015))
        tb_sc_call = s14.shapes.add_textbox(Inches(0.8), Inches(4.95), Inches(6.6), Inches(1.9))
        tf_scc = tb_sc_call.text_frame
        tf_scc.word_wrap = True
        tf_scc.margin_left = tf_scc.margin_top = tf_scc.margin_right = tf_scc.margin_bottom = 0
        add_bullet(tf_scc, "Polynomial Scaling vs Solver Collapse:",
                   "While generic MILP and SMT solvers experience exponential search tree explosion (exceeding 300 s timeouts at N >= 30), our (max, +) formulation preserves deterministic polynomial-time execution.", 10.5)
        add_bullet(tf_scc, "Real-Time Embedded Feasibility:",
                   "27.3 ms synthesis for 1,000 task firings makes online re-synthesis and dynamic task admission viable on resource-constrained embedded microcontrollers.", 10.5, space_before=Pt(3), prefix_color=COLOR_ACCENT_TEAL)

    # Right: Integrated Numbers & Analytical Comparison (Width: 4.8")
    add_integrated_stat(s14, Inches(7.8), Inches(1.85), "1,000", "Task Firings Synthesized", COLOR_ACCENT_BLUE, width=Inches(2.3))
    add_integrated_stat(s14, Inches(10.3), Inches(1.85), "27.3 ms", "ASAP Synthesis Runtime", COLOR_ACCENT_TEAL, width=Inches(2.3))
    add_integrated_stat(s14, Inches(7.8), Inches(2.80), "49.4 ms", "Total Matrix + Synthesis Time", COLOR_TEXT_PRIMARY, width=Inches(2.3))
    add_integrated_stat(s14, Inches(10.3), Inches(2.80), "> 300 s", "MILP / SMT Solver Timeout", COLOR_ACCENT_ALERT, width=Inches(2.3))

    add_divider_line(s14, Inches(7.8), Inches(3.80), Inches(4.7), Inches(0.015))

    tb_sc = s14.shapes.add_textbox(Inches(7.8), Inches(3.95), Inches(4.7), Inches(2.8))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True

    add_bullet(tf_sc, "Theoretical Scaling:",
               "Matrix closure scales in O(n³); unrolled Bellman-Ford synthesis scales in O(K · (|E| + |C_L| + |C_U|)).", 11)
    add_bullet(tf_sc, "Measured Benchmarks (K=10):",
               "• N = 10 actors (100 firings): 0.7 ms\n• N = 50 actors (500 firings): 6.5 ms\n• N = 100 actors (1,000 firings): 27.3 ms (sub-second!)", 10.5, space_before=Pt(4), prefix_color=COLOR_TEXT_PRIMARY)
    add_bullet(tf_sc, "Solver Contrast:",
               "Standard MILP/SMT solvers exceed 300 seconds (timeout) on graphs with N >= 30 when bidirectional bounds are introduced.", 10.5, space_before=Pt(4), prefix_color=COLOR_ACCENT_ALERT)

    s14.notes_slide.notes_text_frame.text = (
        "Speaker 5 (Koneti Karthik): Slide 14 presents our computational scalability evaluation across graph sizes from 5 to 100 actors "
        "unrolled over 10 iterations. While generic SMT and MILP solvers time out at over 300 seconds on graphs with 30 or more actors, our "
        "vectorized (max, +) synthesis scales polynomially, synthesizing 1,000 task firings in just 27.3 milliseconds. This empirical proof "
        "demonstrates that the paper's algebraic formulation makes complex schedule synthesis viable for real-time and online embedded compilers."
    )

    # =========================================================================
    # SLIDE 15: LIMITATIONS & REPRODUCTION DISCLOSURES (ASYMMETRICAL EDITORIAL)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_canvas(s15)
    add_editorial_header(s15, "Critical Reflection: Model Boundaries, Timing Assumptions & Open Challenges",
                         "14. Critical Reflection & Disclosures",
                         "Transparent disclosure of deterministic timing assumptions, multi-rate expansion limits, and reproduction provenance.")

    # Asymmetrical Split Layout: Left 60% (Model Boundaries) / Right 40% (Reproduction Integrity)
    # Left: 2 Model Boundaries
    tb_l1 = s15.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(6.4), Inches(4.8))
    tf_l1 = tb_l1.text_frame
    tf_l1.word_wrap = True
    tf_l1.margin_left = tf_l1.margin_top = tf_l1.margin_right = tf_l1.margin_bottom = 0

    p_l1_h = tf_l1.paragraphs[0]
    p_l1_h.text = "1. TIMING ASSUMPTIONS & RUNTIME JITTER"
    p_l1_h.font.name = FONT_HEADING
    p_l1_h.font.size = Pt(12)
    p_l1_h.font.bold = True
    p_l1_h.font.color.rgb = COLOR_ACCENT_BLUE

    add_bullet(tf_l1, "Deterministic Durations:",
               "The model assumes task execution times w(v) are fixed or strictly bounded within known deterministic intervals [w^-, w^+].", 11, space_before=Pt(4))
    add_bullet(tf_l1, "Runtime Jitter Risk:",
               "If tasks experience OS preemption, cache misses, or DVFS frequency changes, static schedules can suffer from timing violations.", 11, space_before=Pt(4))
    add_bullet(tf_l1, "Future Extension:",
               "Incorporating parametric (max, +) algebra to synthesize robust schedules under bounded stochastic uncertainty.", 11, space_before=Pt(4), prefix_color=COLOR_ACCENT_TEAL)

    add_bullet(tf_l1, "2. MULTI-RATE EXPANSION OVERHEAD", "", 12, space_before=Pt(14), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_l1, "HSDF Graph Inflation:",
               "Graphs with large prime repetition factors q(v) expand into huge numbers of HSDF actors, increasing matrix dimension.", 11, space_before=Pt(4))
    add_bullet(tf_l1, "Sequentiality Enforcement:",
               "Reproduction proved intra-actor sequentiality arcs are mandatory to prevent single-threaded actors from overlapping.", 11, space_before=Pt(4))
    add_bullet(tf_l1, "Hierarchical Scheduling:",
               "Extreme multi-rate systems would benefit from modular state-space decomposition to preserve compact representations.", 11, space_before=Pt(4))

    # Vertical divider
    add_divider_line(s15, Inches(7.45), Inches(1.85), Inches(0.015), Inches(4.8))

    # Right: Reproduction Integrity & Provenance (Clean typographic column, NO card container)
    tb_l3 = s15.shapes.add_textbox(Inches(7.8), Inches(1.85), Inches(4.733), Inches(4.8))
    tf_l3 = tb_l3.text_frame
    tf_l3.word_wrap = True
    tf_l3.margin_left = tf_l3.margin_top = tf_l3.margin_right = tf_l3.margin_bottom = 0

    p_l3 = tf_l3.paragraphs[0]
    p_l3.text = "REPRODUCTION INTEGRITY & PROVENANCE"
    p_l3.font.name = FONT_HEADING
    p_l3.font.size = Pt(12)
    p_l3.font.bold = True
    p_l3.font.color.rgb = COLOR_ACCENT_ALERT

    add_bullet(tf_l3, "Target Paper Scope:",
               "Verified target publication: DOI 10.1145/3762643 (van Wanrooij et al., EMSOFT 2025 / ACM TECS). Entire codebase strictly reproduces this paper.", 11, space_before=Pt(8))
    add_bullet(tf_l3, "100% Clean-Room Build:",
               "The authors did not release a public artifact repository; all modules and algorithms were reconstructed strictly from published mathematical text.", 11, space_before=Pt(8))
    add_bullet(tf_l3, "Empirical Validation:",
               "All numbers, charts, and test outcomes presented in this deck reflect our own executed code, audited by an independent oracle.", 11, space_before=Pt(8), prefix_color=COLOR_ACCENT_TEAL)
    add_bullet(tf_l3, "Reproduction Confidence:",
               "28/28 tests passing, zero proprietary dependencies, exact bound enforcement with zero makespan loss.", 11, space_before=Pt(8), prefix_color=COLOR_ACCENT_BLUE)

    s15.notes_slide.notes_text_frame.text = (
        "Speaker 1 (Sk J Ur Rahaman): Slide 15 provides transparent critical reflection on model boundaries. First, the framework assumes "
        "deterministic task execution durations. In operating systems with scheduling preemption or hardware jitter, parametric extensions "
        "would be required. Second, expanding multi-rate SDF graphs with large repetition factors into HSDF increases matrix dimensions, "
        "suggesting hierarchical decomposition for extreme multi-rate graphs. Finally, because no open-source repository was published by the "
        "authors, our reproduction was entirely implemented from scratch based on the paper's mathematical definitions."
    )

    # =========================================================================
    # SLIDE 16: CONCLUSIONS & EQUAL TEAM CONTRIBUTIONS
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_canvas(s16)
    add_editorial_header(s16, "Conclusions & Equal Team Contribution Breakdown (Total = 100%)",
                         "15. Conclusions & Team Breakdown",
                         "Complete research paper reproduction, rigorous verification, and equal 5-member engineering effort.")

    # Top Half: Key Research Takeaways (Typographic blocks)
    tb_c_take = s16.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.733), Inches(1.8))
    tf_ct = tb_c_take.text_frame
    tf_ct.word_wrap = True
    tf_ct.margin_left = tf_ct.margin_top = tf_ct.margin_right = tf_ct.margin_bottom = 0

    p_th = tf_ct.paragraphs[0]
    p_th.text = "KEY RESEARCH REPRODUCTION TAKEAWAYS"
    p_th.font.name = FONT_HEADING
    p_th.font.size = Pt(11.5)
    p_th.font.bold = True
    p_th.font.color.rgb = COLOR_ACCENT_BLUE

    add_bullet(tf_ct, "1. Theoretical Validation:",
               "Demonstrated that (max, +) state-space algebra bridges dataflow precedence and bidirectional timing bounds, enabling polynomial-time synthesis.", 11, space_before=Pt(4))
    add_bullet(tf_ct, "2. Empirical Fidelity:",
               "The semiconductor case study verified that state-space synthesis completely eliminates transit dwell defects while preserving 100% of optimal throughput.", 11, space_before=Pt(4))
    add_bullet(tf_ct, "3. Decoupled Verification:",
               "An independent constraint checker verified 28/28 automated test cases warning-free, proving mathematical correctness without solver heuristics.", 11, space_before=Pt(4))
    add_bullet(tf_ct, "4. Open-Source Artifact:",
               "Delivered a clean, documented, tested Python repository with automated benchmarks and reproducible scripts.", 11, space_before=Pt(4))

    add_divider_line(s16, Inches(0.8), Inches(3.9), Inches(11.733), Inches(0.015))

    # Bottom Half: 5 Equal Team Members (Clean typographic columns, NO rounded cards!)
    p_team_h = s16.shapes.add_textbox(Inches(0.8), Inches(4.05), Inches(11.733), Inches(0.3))
    tf_th = p_team_h.text_frame
    p_th2 = tf_th.paragraphs[0]
    p_th2.text = "EQUAL 5-MEMBER CONTRIBUTION BREAKDOWN (20% EACH — TOTAL = 100%)"
    p_th2.font.name = FONT_HEADING
    p_th2.font.size = Pt(11)
    p_th2.font.bold = True
    p_th2.font.color.rgb = COLOR_TEXT_PRIMARY

    team_members = [
        ("Sk J Ur Rahaman", "230951", "Project Lead, Presentation Narration & Architecture"),
        ("Sanga Badri", "230911", "Extended HSDFG & Multi-Rate Balance Expansion"),
        ("Ampili Hemanth Kumar", "230128", "Max-Plus Semiring Algebra & State-Space Engine"),
        ("Vempati Prem Santhosh", "231137", "Schedule Synthesis Engine & Independent Validator"),
        ("Koneti Karthik", "230568", "Experimental Reproduction Pipeline & Video Render"),
    ]

    t_w = Inches(2.22)
    t_gap = Inches(0.158)
    t_start = Inches(0.8)

    for i, (name, roll, role) in enumerate(team_members):
        col_x = t_start + i * (t_w + t_gap)
        tb_m = s16.shapes.add_textbox(col_x, Inches(4.45), t_w, Inches(2.3))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0

        # Percent Badge as bold typographic accent line
        p_pct = tf_m.paragraphs[0]
        p_pct.text = "20% CONTRIBUTION"
        p_pct.font.name = FONT_HEADING
        p_pct.font.size = Pt(10)
        p_pct.font.bold = True
        p_pct.font.color.rgb = COLOR_ACCENT_BLUE if i == 0 else COLOR_ACCENT_TEAL

        # Name
        p_name = tf_m.add_paragraph()
        p_name.text = name
        p_name.font.name = FONT_HEADING
        p_name.font.size = Pt(11.5)
        p_name.font.bold = True
        p_name.font.color.rgb = COLOR_TEXT_PRIMARY
        p_name.space_before = Pt(3)

        # Roll
        p_roll = tf_m.add_paragraph()
        p_roll.text = f"Roll: {roll} (CSE)"
        p_roll.font.name = FONT_BODY
        p_roll.font.size = Pt(10)
        p_roll.font.color.rgb = COLOR_TEXT_SLATE
        p_roll.space_before = Pt(1)

        # Role Description
        p_role = tf_m.add_paragraph()
        p_role.text = role
        p_role.font.name = FONT_BODY
        p_role.font.size = Pt(9.5)
        p_role.font.color.rgb = COLOR_TEXT_SLATE
        p_role.space_before = Pt(4)

    s16.notes_slide.notes_text_frame.text = (
        "Speaker 1 (Sk J Ur Rahaman): In conclusion, our reproduction successfully validates the research claims of van Wanrooij, Basten, and "
        "Geilen. The Extended HSDFG formalism and (max, +) state-space transformation turn an NP-hard scheduling problem into an exact, polynomial-time "
        "procedure. Our experimental results on the wafer manufacturing case study proved that upper bounds can be strictly enforced without any loss "
        "in throughput. All five members of our group contributed equally, exactly 20% each, across mathematical modeling, semiring implementation, "
        "algorithm synthesis, experimental evaluation, and presentation assembly. Thank you for your attention, and we welcome your questions."
    )

    # Save to both paths
    prs.save(PPTX_TARGET)
    prs.save(ROOT_PPTX_TARGET)
    print(f"Canva-style presentation generated successfully at:\n - {PPTX_TARGET}\n - {ROOT_PPTX_TARGET}")


if __name__ == '__main__':
    create_deck()
