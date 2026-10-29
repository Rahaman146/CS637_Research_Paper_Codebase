"""
Generate high-resolution, minimalist diagrams for the CS637 Gamma Minimal-style presentation.
All figures adhere to Gamma's Minimal aesthetic:
- Clean white (#FFFFFF) backgrounds with generous whitespace.
- Restrained color palette: Deep Slate (#0F172A), Slate Blue (#2563EB), Deep Academic Teal (#0F766E), Amber (#D97706), Alert (#DC2626), Emerald (#059669).
- High resolution: 300 DPI vector-crisp output.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = "figures_minimal"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set global matplotlib style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['text.color'] = '#0F172A'
plt.rcParams['axes.labelcolor'] = '#0F172A'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'


def generate_title_graphic_minimal():
    """Generates a clean, minimalist widescreen abstract dataflow timeline graphic with white background."""
    fig, ax = plt.subplots(figsize=(12.0, 3.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Draw timeline grid ticks spanning full horizon (0 to 36s)
    for t in range(0, 38, 4):
        ax.axvline(t, color='#E2E8F0', linestyle='--', linewidth=0.8, alpha=0.9)
        ax.text(t, -0.45, f"{t}s", color='#64748B', fontsize=9.5, ha='center', va='top')

    # 3 distinct execution tracks: PreHeat (y=2.2), Robotic Transit (y=1.2), Process Chamber (y=0.2)
    tracks = [
        ("PreHeat Chamber (w=4s)", 2.2),
        ("Robotic Transit (Dwell ≤ 3.0s)", 1.2),
        ("Process Chamber (w=6s)", 0.2)
    ]
    for name, y in tracks:
        ax.text(-0.6, y, name, color='#1E293B', fontsize=9, fontweight='bold', ha='right', va='center')
        ax.axhline(y, color='#F1F5F9', linestyle='-', linewidth=1.0)

    # Iteration 0 (k=0)
    # PreHeat: 2 to 6
    ax.add_patch(patches.Rectangle((2, 1.9), 4, 0.6, linewidth=1.2, edgecolor='#2563EB', facecolor='#EFF6FF'))
    ax.text(4, 2.2, "PreHeat [k=0]", color='#1E40AF', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Process: 6 to 12
    ax.add_patch(patches.Rectangle((6, -0.1), 6, 0.6, linewidth=1.2, edgecolor='#0F766E', facecolor='#F0FDFA'))
    ax.text(9, 0.2, "Process [k=0]", color='#0F766E', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Iteration 1 (k=1)
    # PreHeat: 6 to 10
    ax.add_patch(patches.Rectangle((6, 1.9), 4, 0.6, linewidth=1.2, edgecolor='#2563EB', facecolor='#DBEAFE'))
    ax.text(8, 2.2, "PreHeat [k=1]", color='#1E40AF', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Dwell transit wait: 10 to 12 (2s)
    ax.add_patch(patches.Rectangle((10, 0.9), 2, 0.6, linewidth=1.0, edgecolor='#D97706', facecolor='#FEF3C7', alpha=0.9))
    ax.text(11, 1.2, "Dwell: 2.0s", color='#B45309', fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Process: 12 to 18
    ax.add_patch(patches.Rectangle((12, -0.1), 6, 0.6, linewidth=1.2, edgecolor='#0F766E', facecolor='#CCFBF1'))
    ax.text(15, 0.2, "Process [k=1]", color='#0F766E', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Iteration 2 (k=2) — Synthesized deliberate upstream delay!
    # PreHeat delayed to 11 to 15
    ax.add_patch(patches.Rectangle((11, 1.9), 4, 0.6, linewidth=1.2, edgecolor='#059669', facecolor='#D1FAE5'))
    ax.text(13, 2.2, "PreHeat [k=2]\n(Delayed +1s)", color='#065F46', fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Dwell transit: 15 to 18 (3.0s clamp!)
    ax.add_patch(patches.Rectangle((15, 0.9), 3, 0.6, linewidth=1.2, edgecolor='#059669', facecolor='#A7F3D0', alpha=0.9))
    ax.text(16.5, 1.2, "Dwell: 3.0s (Clamped)", color='#065F46', fontsize=8, fontweight='bold', ha='center', va='center')

    # Process: 18 to 24
    ax.add_patch(patches.Rectangle((18, -0.1), 6, 0.6, linewidth=1.2, edgecolor='#0F766E', facecolor='#CCFBF1'))
    ax.text(21, 0.2, "Process [k=2]", color='#0F766E', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Iteration 3 (k=3) — Synthesized deliberate upstream delay!
    # PreHeat delayed to 17 to 21
    ax.add_patch(patches.Rectangle((17, 1.9), 4, 0.6, linewidth=1.2, edgecolor='#059669', facecolor='#D1FAE5'))
    ax.text(19, 2.2, "PreHeat [k=3]\n(Delayed +3s)", color='#065F46', fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Dwell transit: 21 to 24 (3.0s clamp!)
    ax.add_patch(patches.Rectangle((21, 0.9), 3, 0.6, linewidth=1.2, edgecolor='#059669', facecolor='#A7F3D0', alpha=0.9))
    ax.text(22.5, 1.2, "Dwell: 3.0s (Clamped)", color='#065F46', fontsize=8, fontweight='bold', ha='center', va='center')

    # Process: 24 to 30
    ax.add_patch(patches.Rectangle((24, -0.1), 6, 0.6, linewidth=1.2, edgecolor='#0F766E', facecolor='#CCFBF1'))
    ax.text(27, 0.2, "Process [k=3]", color='#0F766E', fontsize=9.5, fontweight='bold', ha='center', va='center')

    ax.set_xlim(-1, 37)
    ax.set_ylim(-0.8, 3.0)
    ax.axis('off')

    out_path = os.path.join(OUTPUT_DIR, "fig_title_graphic_minimal.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")


def generate_worked_example_diagram():
    """Generates an illustrative 3-actor pipeline diagram and execution comparison for Slide 10."""
    fig, axes = plt.subplots(2, 1, figsize=(11.5, 4.8), dpi=300, gridspec_kw={'height_ratios': [1.2, 1.8]})
    fig.patch.set_facecolor('#FFFFFF')

    # Subplot 0: Graph Schematic
    ax0 = axes[0]
    ax0.set_facecolor('#FFFFFF')
    ax0.set_xlim(0, 11)
    ax0.set_ylim(0, 3)
    ax0.axis('off')

    # Draw Actors A, B, C
    actors = [
        ("A: Heat", "w(A)=3", 2.0, 1.5, '#F8FAFC', '#2563EB'),
        ("B: Transport", "w(B)=2", 5.5, 1.5, '#F8FAFC', '#64748B'),
        ("C: Deposit", "w(C)=5", 9.0, 1.5, '#F0FDFA', '#0F766E')
    ]
    for name, dur, x, y, bg, border in actors:
        rect = patches.FancyBboxPatch((x-1.0, y-0.45), 2.0, 0.9, boxstyle="square,pad=0.08",
                                      facecolor=bg, edgecolor=border, lw=1.5)
        ax0.add_patch(rect)
        ax0.text(x, y+0.12, name, color='#0F172A', fontsize=10, fontweight='bold', ha='center', va='center')
        ax0.text(x, y-0.2, dur, color='#475569', fontsize=8.5, ha='center', va='center')

    # Forward Precedence Arrows
    ax0.annotate("", xy=(4.4, 1.5), xytext=(3.1, 1.5),
                 arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.8))
    ax0.text(3.75, 1.75, "FIFO (d=0)", color="#2563EB", fontsize=8.5, fontweight='bold', ha='center')

    ax0.annotate("", xy=(7.9, 1.5), xytext=(6.6, 1.5),
                 arrowprops=dict(arrowstyle="->", color="#0F766E", lw=1.8))
    ax0.text(7.25, 1.75, "FIFO (d=0)", color="#0F766E", fontsize=8.5, fontweight='bold', ha='center')

    # Upper Bound Arc: C.start - A.comp <= 4.0s -> Inverted: A.start >= C.start - 7.0s
    arrow = patches.FancyArrowPatch((8.2, 0.95), (2.8, 0.95),
                                   connectionstyle="arc3,rad=0.25",
                                   arrowstyle="->", color="#DC2626", lw=1.8, linestyle="--")
    ax0.add_patch(arrow)
    ax0.text(5.5, 0.15, "Upper Bound CU: s_C(k) - c_A(k) ≤ 4.0s  ==>  Backward Arc: s_A(k) ≥ s_C(k) - 7.0s",
             color="#DC2626", fontsize=9, fontweight='bold', ha='center')

    # Subplot 1: Schedule Comparison (Greedy vs Synthesized)
    ax1 = axes[1]
    ax1.set_facecolor('#FFFFFF')
    ax1.set_xlim(-0.5, 18.5)
    ax1.set_ylim(-0.8, 4.2)

    # Gridlines and timeline ticks
    for t in range(0, 19, 2):
        ax1.axvline(t, color='#E2E8F0', linestyle='--', linewidth=0.7, alpha=0.8)
        ax1.text(t, -0.6, f"{t}s", color='#64748B', fontsize=8.5, ha='center', va='top')

    # Track Labels
    ax1.text(-0.3, 3.1, "GREEDY (ASAP)\nViolates Dwell", color='#DC2626', fontsize=8.5, fontweight='bold', ha='right', va='center')
    ax1.text(-0.3, 1.1, "SYNTHESIZED (Bounded)\nSatisfies Dwell", color='#059669', fontsize=8.5, fontweight='bold', ha='right', va='center')
    ax1.axhline(2.1, color='#CBD5E1', linestyle='-', linewidth=1.0)

    # Track 1: Greedy Execution
    ax1.add_patch(patches.Rectangle((3, 3.2), 3, 0.6, facecolor='#EFF6FF', edgecolor='#2563EB', lw=1.2))
    ax1.text(4.5, 3.5, "A: Heat (w=3)", color='#1E40AF', fontsize=8, fontweight='bold', ha='center', va='center')
    ax1.add_patch(patches.Rectangle((6, 3.2), 2, 0.6, facecolor='#F8FAFC', edgecolor='#64748B', lw=1.2))
    ax1.text(7.0, 3.5, "B (w=2)", color='#334155', fontsize=8, ha='center', va='center')
    ax1.add_patch(patches.Rectangle((8, 3.2), 4, 0.6, facecolor='#FEE2E2', edgecolor='#DC2626', lw=1.2, hatch='//'))
    ax1.text(10.0, 3.5, "Dwell: 6.0s (VIOLATION > 4s)", color='#991B1B', fontsize=8, fontweight='bold', ha='center', va='center')
    ax1.add_patch(patches.Rectangle((12, 3.2), 5, 0.6, facecolor='#F0FDFA', edgecolor='#0F766E', lw=1.2))
    ax1.text(14.5, 3.5, "C: Deposit (w=5)", color='#0F766E', fontsize=8, fontweight='bold', ha='center', va='center')

    # Track 2: Synthesized Schedule
    ax1.add_patch(patches.Rectangle((5, 0.8), 3, 0.6, facecolor='#D1FAE5', edgecolor='#059669', lw=1.2))
    ax1.text(6.5, 1.1, "A: Heat (Delayed to t=5)", color='#065F46', fontsize=8, fontweight='bold', ha='center', va='center')
    ax1.add_patch(patches.Rectangle((8, 0.8), 2, 0.6, facecolor='#F8FAFC', edgecolor='#64748B', lw=1.2))
    ax1.text(9.0, 1.1, "B (w=2)", color='#334155', fontsize=8, ha='center', va='center')
    ax1.add_patch(patches.Rectangle((10, 0.8), 2, 0.6, facecolor='#FEF3C7', edgecolor='#D97706', lw=1.2))
    ax1.text(11.0, 1.1, "Dwell: 4.0s (EXACT)", color='#92400E', fontsize=8, fontweight='bold', ha='center', va='center')
    ax1.add_patch(patches.Rectangle((12, 0.8), 5, 0.6, facecolor='#F0FDFA', edgecolor='#0F766E', lw=1.2))
    ax1.text(14.5, 1.1, "C: Deposit (w=5)", color='#0F766E', fontsize=8, fontweight='bold', ha='center', va='center')

    ax1.axis('off')
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "fig_worked_example.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")


def generate_pipeline_minimal():
    """Generates a clean vector diagram for the 4-stage synthesis pipeline adhering to Minimal design language."""
    fig, ax = plt.subplots(figsize=(11.5, 3.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4.2)
    ax.axis('off')

    stages = [
        ("STAGE 1", "Constraint\nNormalization", "Extended HSDFG\nLower bounds C_L\nUpper bounds C_U\nDifference arcs", 1.2),
        ("STAGE 2", "State-Space\nTransformation", "Matrices A_0 .. A_D\nIntra bounds -> A_0\nInter bounds -> A_δ\nNon-reentrancy (A_1)", 4.0),
        ("STAGE 3", "Kleene Star\nClosure (M_0*)", "Intra closure M_0*\nInstantaneous loops\nCheck (M_0*)_{ii} > 0\nDetect cycle in O(n³)", 6.8),
        ("STAGE 4", "Unrolled Bellman-Ford\n& Oracle Validation", "Unroll K iterations\nLongest-path dist\nInter-iteration cycle check\nOracle validation (ε ≤ 10⁻⁹)", 9.6)
    ]

    for stage_num, title, body, x in stages:
        # Box container - crisp white with subtle gray border, teal top line
        rect = patches.Rectangle((x - 1.15, 0.5), 2.3, 3.2, facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.0)
        ax.add_patch(rect)
        top_accent = patches.Rectangle((x - 1.15, 3.66), 2.3, 0.04, facecolor='#0F766E', edgecolor='none')
        ax.add_patch(top_accent)

        # Stage Number
        ax.text(x, 3.42, stage_num, color='#0F766E', fontsize=8, fontweight='bold', ha='center', va='center')
        # Title
        ax.text(x, 2.88, title, color='#0F172A', fontsize=9.5, fontweight='bold', ha='center', va='center')
        # Hairline divider
        ax.plot([x - 0.9, x + 0.9], [2.4, 2.4], color='#E2E8F0', lw=0.8)
        # Body text
        ax.text(x, 1.45, body, color='#475569', fontsize=8, ha='center', va='center', linespacing=1.35)

    # Connecting Arrows between stages
    arrows = [(2.35, 3.65), (5.15, 6.45), (7.95, 9.25)]
    for x1, x2 in arrows:
        ax.annotate("", xy=(x2 - 0.8, 2.1), xytext=(x1 + 0.05, 2.1),
                    arrowprops=dict(arrowstyle="->", color="#0F766E", lw=1.5))

    out_path = os.path.join(OUTPUT_DIR, "fig_pipeline_minimal.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")


def generate_timing_bounds_minimal():
    """Generates a clean vector diagram explaining lower vs upper timing bounds normalization."""
    fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Draw Actor u and Actor v
    # Actor u
    rect_u = patches.Rectangle((0.8, 1.9), 2.5, 1.8, facecolor='#F8FAFC', edgecolor='#2563EB', lw=1.5)
    ax.add_patch(rect_u)
    ax.text(2.05, 3.1, "Actor u (Firing k)", color='#0F172A', fontsize=9.5, fontweight='bold', ha='center', va='center')
    ax.text(2.05, 2.4, "Duration w(u)", color='#475569', fontsize=8.5, ha='center', va='center')

    # Event labels under u
    ax.plot([0.8, 0.8], [1.4, 1.9], color='#2563EB', lw=1.2)
    ax.plot([3.3, 3.3], [1.4, 1.9], color='#2563EB', lw=1.2)
    ax.text(0.8, 0.95, "s_u(k)\n(Start)", color='#1E40AF', fontsize=8, fontweight='bold', ha='center')
    ax.text(3.3, 0.95, "c_u(k)\n(Complete)", color='#1E40AF', fontsize=8, fontweight='bold', ha='center')

    # Actor v
    rect_v = patches.Rectangle((6.7, 1.9), 2.5, 1.8, facecolor='#F0FDFA', edgecolor='#0F766E', lw=1.5)
    ax.add_patch(rect_v)
    ax.text(7.95, 3.1, "Actor v (Firing k)", color='#0F172A', fontsize=9.5, fontweight='bold', ha='center', va='center')
    ax.text(7.95, 2.4, "Duration w(v)", color='#475569', fontsize=8.5, ha='center', va='center')

    # Event labels under v
    ax.plot([6.7, 6.7], [1.4, 1.9], color='#0F766E', lw=1.2)
    ax.plot([9.2, 9.2], [1.4, 1.9], color='#0F766E', lw=1.2)
    ax.text(6.7, 0.95, "s_v(k)\n(Start)", color='#0F766E', fontsize=8, fontweight='bold', ha='center')
    ax.text(9.2, 0.95, "c_v(k)\n(Complete)", color='#0F766E', fontsize=8, fontweight='bold', ha='center')

    # Lower Bound Forward Arrow (Green/Teal): s_v - c_u >= L
    ax.annotate("", xy=(6.6, 2.8), xytext=(3.4, 2.8),
                arrowprops=dict(arrowstyle="->", color="#0F766E", lw=1.8))
    ax.text(5.0, 3.1, "Lower Bound (C_L):\ns_v(k) - c_u(k) ≥ L", color='#0F766E', fontsize=8.5, fontweight='bold', ha='center')
    ax.text(5.0, 2.15, "Normalized: s_v - s_u ≥ L + w(u)", color='#475569', fontsize=8, ha='center')

    # Upper Bound Backward Curved Arrow (Red): s_v - c_u <= U -> s_u - s_v >= -U - w(u)
    arrow_up = patches.FancyArrowPatch((7.5, 3.9), (2.5, 3.9),
                                      connectionstyle="arc3,rad=0.35",
                                      arrowstyle="->", color="#DC2626", lw=1.8, linestyle="--")
    ax.add_patch(arrow_up)
    ax.text(5.0, 5.5, "Upper Bound (C_U): s_v(k) - c_u(k) ≤ U", color='#DC2626', fontsize=8.5, fontweight='bold', ha='center')
    ax.text(5.0, 5.0, "Inverts to Backward Arc: s_u(k) - s_v(k) ≥ -U - w(u)", color='#991B1B', fontsize=8, fontweight='bold', ha='center')

    out_path = os.path.join(OUTPUT_DIR, "fig_timing_bounds_minimal.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")


def generate_multirate_minimal():
    """Generates a clean vector diagram explaining multi-rate SDF to HSDF expansion and sequentiality."""
    fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis('off')

    # Top: Multi-rate SDF
    ax.text(0.5, 5.8, "Multi-Rate SDF Graph (Balance: q(A)=3, q(B)=2)", color='#0F766E', fontsize=9, fontweight='bold')
    
    # Actor A
    circle_a = patches.Circle((2.0, 4.6), 0.65, facecolor='#F8FAFC', edgecolor='#2563EB', lw=1.5)
    ax.add_patch(circle_a)
    ax.text(2.0, 4.7, "Actor A", color='#0F172A', fontsize=8.5, fontweight='bold', ha='center')
    ax.text(2.0, 4.4, "w=2", color='#475569', fontsize=8, ha='center')

    # Actor B
    circle_b = patches.Circle((8.0, 4.6), 0.65, facecolor='#F0FDFA', edgecolor='#0F766E', lw=1.5)
    ax.add_patch(circle_b)
    ax.text(8.0, 4.7, "Actor B", color='#0F172A', fontsize=8.5, fontweight='bold', ha='center')
    ax.text(8.0, 4.4, "w=3", color='#475569', fontsize=8, ha='center')

    # Precedence arc with rates
    ax.annotate("", xy=(7.3, 4.6), xytext=(2.7, 4.6),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.5))
    ax.text(5.0, 4.9, "prd = 2, cns = 3 (d=0)", color='#2563EB', fontsize=8.5, fontweight='bold', ha='center')
    ax.text(5.0, 4.3, "Balance: 3 × 2 = 2 × 3 = 6 tokens", color='#64748B', fontsize=8, ha='center')

    # Downward expansion arrow
    ax.annotate("", xy=(5.0, 3.4), xytext=(5.0, 3.9),
                arrowprops=dict(arrowstyle="->", color="#64748B", lw=1.2))
    ax.text(5.2, 3.65, "HSDF Expansion & Serialization", color='#475569', fontsize=8, fontweight='bold')

    # Bottom: Expanded HSDF with A_0, A_1, A_2 -> B_0, B_1
    ax.text(0.5, 3.0, "Expanded Homogeneous SDF (Explicit Serialization)", color='#0F766E', fontsize=9, fontweight='bold')

    # A0, A1, A2
    a_nodes = [(1.3, "A_0"), (2.7, "A_1"), (4.1, "A_2")]
    for x, lbl in a_nodes:
        c = patches.Circle((x, 1.9), 0.45, facecolor='#F8FAFC', edgecolor='#2563EB', lw=1.2)
        ax.add_patch(c)
        ax.text(x, 1.9, lbl, color='#0F172A', fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Internal serialization A0->A1->A2
    ax.annotate("", xy=(2.2, 1.9), xytext=(1.8, 1.9), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.2))
    ax.annotate("", xy=(3.6, 1.9), xytext=(3.2, 1.9), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.2))

    # B0, B1
    b_nodes = [(7.0, "B_0"), (8.6, "B_1")]
    for x, lbl in b_nodes:
        c = patches.Circle((x, 1.9), 0.45, facecolor='#F0FDFA', edgecolor='#0F766E', lw=1.2)
        ax.add_patch(c)
        ax.text(x, 1.9, lbl, color='#0F172A', fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Internal serialization B0->B1
    ax.annotate("", xy=(8.1, 1.9), xytext=(7.5, 1.9), arrowprops=dict(arrowstyle="->", color="#0F766E", lw=1.2))

    # Cross connections: A0, A1 -> B0; A1, A2 -> B1
    ax.annotate("", xy=(6.5, 1.9), xytext=(4.6, 1.9), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.0))
    ax.annotate("", xy=(8.3, 2.3), xytext=(4.3, 2.3),
                arrowprops=dict(arrowstyle="->", color="#2563EB", lw=1.0, connectionstyle="arc3,rad=-0.25"))

    # Inter-iteration serialization loopback A2 -> A0 (d=1) - Curves UNDERNEATH
    loopback = patches.FancyArrowPatch((4.0, 1.4), (1.4, 1.4),
                                       connectionstyle="arc3,rad=-0.35",
                                       arrowstyle="->", color="#DC2626", lw=1.4, linestyle="--")
    ax.add_patch(loopback)
    ax.text(2.7, 0.55, "Inter-iteration sequentiality: A_2 → A_0 (delay d=1, single-thread)", color='#DC2626', fontsize=7.8, fontweight='bold', ha='center')

    out_path = os.path.join(OUTPUT_DIR, "fig_multirate_minimal.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")


if __name__ == "__main__":
    generate_title_graphic_minimal()
    generate_worked_example_diagram()
    generate_pipeline_minimal()
    generate_timing_bounds_minimal()
    generate_multirate_minimal()
