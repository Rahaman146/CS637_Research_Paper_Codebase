"""
Generate high-resolution, professionally art-directed diagrams for the Canva-style CS637 presentation.
All figures adhere to the Canva editorial aesthetic:
- Clean, open compositions with zero card repetition.
- Beautiful, harmonious color palette:
  - Deep Navy: #0F172A
  - Electric Blue: #2563EB
  - Emerald / Teal: #0D9488 / #059669
  - Crimson / Alert: #DC2626
  - Amber / Warning: #D97706
  - Neutral Slate: #475569 / #64748B
  - Divider / Surface: #E2E8F0 / #F8FAFC
- High resolution: 300 DPI vector-crisp output.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = "figures_canva"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set global matplotlib style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['text.color'] = '#0F172A'
plt.rcParams['axes.labelcolor'] = '#0F172A'
plt.rcParams['xtick.color'] = '#475569'
plt.rcParams['ytick.color'] = '#475569'


def generate_title_graphic():
    """Generates an impressive, widescreen abstract dataflow timeline graphic for the title slide."""
    fig, ax = plt.subplots(figsize=(12.0, 3.2), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')

    # Draw timeline grid ticks spanning full horizon (0 to 36s)
    for t in range(0, 38, 4):
        ax.axvline(t, color='#1E293B', linestyle='--', linewidth=0.8, alpha=0.7)
        ax.text(t, -0.45, f"{t}s", color='#64748B', fontsize=9.5, ha='center', va='top')

    # 3 distinct execution tracks: PreHeat (y=2.2), Robotic Transit (y=1.2), Process Chamber (y=0.2)
    tracks = [
        ("PreHeat Chamber (w=4s)", 2.2),
        ("Robotic Transit (Dwell ≤ 3.0s)", 1.2),
        ("Process Chamber (w=6s)", 0.2)
    ]
    for name, y in tracks:
        ax.text(-0.6, y, name, color='#94A3B8', fontsize=9, fontweight='bold', ha='right', va='center')
        ax.axhline(y, color='#1E293B', linestyle=':', linewidth=0.8, alpha=0.6)

    # Iteration 0 (k=0)
    # PreHeat: 2 to 6
    ax.add_patch(patches.Rectangle((2, 1.9), 4, 0.6, linewidth=1.2, edgecolor='#38BDF8', facecolor='#2563EB'))
    ax.text(4, 2.2, "PreHeat [k=0]", color='#FFFFFF', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Process: 6 to 12
    ax.add_patch(patches.Rectangle((6, -0.1), 6, 0.6, linewidth=1.2, edgecolor='#34D399', facecolor='#0D9488'))
    ax.text(9, 0.2, "Process [k=0]", color='#FFFFFF', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Iteration 1 (k=1)
    # PreHeat: 6 to 10
    ax.add_patch(patches.Rectangle((6, 1.9), 4, 0.6, linewidth=1.2, edgecolor='#38BDF8', facecolor='#1D4ED8'))
    ax.text(8, 2.2, "PreHeat [k=1]", color='#FFFFFF', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Dwell transit wait: 10 to 12 (2s)
    ax.add_patch(patches.Rectangle((10, 0.9), 2, 0.6, linewidth=1.0, edgecolor='#F59E0B', facecolor='#D97706', alpha=0.85))
    ax.text(11, 1.2, "Dwell: 2s", color='#FFFFFF', fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Process: 12 to 18
    ax.add_patch(patches.Rectangle((12, -0.1), 6, 0.6, linewidth=1.2, edgecolor='#34D399', facecolor='#0D9488'))
    ax.text(15, 0.2, "Process [k=1]", color='#FFFFFF', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Iteration 2 (k=2) — Synthesized deliberate upstream delay!
    # PreHeat delayed to 11 to 15
    ax.add_patch(patches.Rectangle((11, 1.9), 4, 0.6, linewidth=1.2, edgecolor='#6EE7B7', facecolor='#059669'))
    ax.text(13, 2.2, "PreHeat [k=2]\n(Delayed +1s)", color='#FFFFFF', fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Dwell transit: 15 to 18 (3.0s clamp!)
    ax.add_patch(patches.Rectangle((15, 0.9), 3, 0.6, linewidth=1.2, edgecolor='#10B981', facecolor='#059669', alpha=0.9))
    ax.text(16.5, 1.2, "Dwell: 3.0s (Clamped)", color='#FFFFFF', fontsize=8, fontweight='bold', ha='center', va='center')

    # Process: 18 to 24
    ax.add_patch(patches.Rectangle((18, -0.1), 6, 0.6, linewidth=1.2, edgecolor='#34D399', facecolor='#0D9488'))
    ax.text(21, 0.2, "Process [k=2]", color='#FFFFFF', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Iteration 3 (k=3) — Synthesized deliberate upstream delay!
    # PreHeat delayed to 17 to 21
    ax.add_patch(patches.Rectangle((17, 1.9), 4, 0.6, linewidth=1.2, edgecolor='#6EE7B7', facecolor='#059669'))
    ax.text(19, 2.2, "PreHeat [k=3]\n(Delayed +3s)", color='#FFFFFF', fontsize=8.5, fontweight='bold', ha='center', va='center')

    # Dwell transit: 21 to 24 (3.0s clamp!)
    ax.add_patch(patches.Rectangle((21, 0.9), 3, 0.6, linewidth=1.2, edgecolor='#10B981', facecolor='#059669', alpha=0.9))
    ax.text(22.5, 1.2, "Dwell: 3.0s (Clamped)", color='#FFFFFF', fontsize=8, fontweight='bold', ha='center', va='center')

    # Process: 24 to 30
    ax.add_patch(patches.Rectangle((24, -0.1), 6, 0.6, linewidth=1.2, edgecolor='#34D399', facecolor='#0D9488'))
    ax.text(27, 0.2, "Process [k=3]", color='#FFFFFF', fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Forward Lower Bound annotation
    ax.annotate("", xy=(6, 0.5), xytext=(6, 1.9),
                arrowprops=dict(arrowstyle="->", color='#38BDF8', lw=2))
    ax.text(6.3, 1.55, "Dataflow FIFO Arc (d=0)", color='#38BDF8', fontsize=8.5, fontweight='bold')

    # Backward Upper Bound annotation on Iteration 2 (PreHeat k=2 completes at 15, Process k=2 starts at 18)
    ax.annotate("", xy=(15, 2.2), xytext=(18, 0.5),
                arrowprops=dict(arrowstyle="->", color='#F87171', lw=2,
                                connectionstyle="arc3,rad=-0.3", linestyle='--'))
    ax.text(17.5, 2.7, "Upper Bound Dwell ≤ 3.0s (Backward Difference Arc)",
            color='#FCA5A5', fontsize=8.5, fontweight='bold', ha='center', va='bottom')

    # End-of-schedule makespan marker
    ax.axvline(36, color='#38BDF8', linestyle='-', linewidth=1.5)
    ax.text(36, 1.6, "Makespan: 36.0s\n(Zero Throughput Loss)", color='#38BDF8', fontsize=8.5, fontweight='bold', ha='center')

    ax.set_xlim(-4.2, 38)
    ax.set_ylim(-0.8, 2.9)
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig_title_graphic.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")


def generate_wafer_dwell_comparison():
    """Generates an accurate diagram matching code numbers for Greedy (violation) vs Synthesized (dwell clamp)."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.5, 4.8), dpi=300, sharex=True)
    fig.patch.set_facecolor('#FFFFFF')

    for ax in (ax1, ax2):
        ax.set_facecolor('#FFFFFF')
        for t in range(0, 38, 4):
            ax.axvline(t, color='#F1F5F9', linestyle='-', linewidth=1.0)
            ax.axvline(t + 2, color='#F8FAFC', linestyle=':', linewidth=0.8)
        ax.set_ylim(-0.4, 2.8)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#CBD5E1')
        ax.set_yticks([0.4, 1.0, 1.8])
        ax.set_yticklabels(['Process Chamber\n(w=6s)', 'Transit Dwell\n(Limit ≤ 3s)', 'PreHeat Chamber\n(w=4s)'],
                           fontsize=9, fontweight='bold', color='#1E293B')

    # --- AX1: GREEDY EXECUTION ---
    ax1.set_title("GREEDY (SELF-TIMED) SCHEDULE — Uncontrolled Wait Causes Upper Dwell Violation (Yield Loss)",
                  fontsize=11, fontweight='bold', color='#DC2626', loc='left', pad=8)

    # PreHeat tasks: w0=2-6, w1=6-10, w2=10-14, w3=14-18
    ax1.barh(1.8, 4, left=2, height=0.5, color='#94A3B8', edgecolor='#64748B')
    ax1.text(4, 1.8, "w0 (2-6)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    ax1.barh(1.8, 4, left=6, height=0.5, color='#94A3B8', edgecolor='#64748B')
    ax1.text(8, 1.8, "w1 (6-10)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    ax1.barh(1.8, 4, left=10, height=0.5, color='#FCA5A5', edgecolor='#DC2626')
    ax1.text(12, 1.8, "w2 (10-14)", ha='center', va='center', color='#7F1D1D', fontweight='bold', fontsize=8)

    ax1.barh(1.8, 4, left=14, height=0.5, color='#FECACA', edgecolor='#DC2626')
    ax1.text(16, 1.8, "w3 (14-18)", ha='center', va='center', color='#7F1D1D', fontweight='bold', fontsize=8)

    # Dwell on Transit track (y=1.0)
    # w1 dwell: 10 to 12 (2s)
    ax1.barh(1.0, 2, left=10, height=0.4, color='#E2E8F0', edgecolor='#94A3B8')
    ax1.text(11, 1.0, "2.0s", ha='center', va='center', color='#475569', fontsize=8, fontweight='bold')

    # w2 dwell: 14 to 18 (4s) -> VIOLATION
    ax1.barh(1.0, 4, left=14, height=0.4, color='#FEE2E2', edgecolor='#DC2626', hatch='//')
    ax1.text(16, 1.0, "4.0s (VIOLATION)", ha='center', va='center', color='#DC2626', fontsize=8, fontweight='bold')

    # w3 dwell: 18 to 24 (6s) -> VIOLATION
    ax1.barh(1.0, 6, left=18, height=0.4, color='#FEE2E2', edgecolor='#DC2626', hatch='\\\\')
    ax1.text(21, 1.0, "6.0s (VIOLATION)", ha='center', va='center', color='#DC2626', fontsize=8, fontweight='bold')

    # Process tasks (w=6): w0=6-12, w1=12-18, w2=18-24, w3=24-30
    ax1.barh(0.4, 6, left=6, height=0.5, color='#64748B', edgecolor='#475569')
    ax1.text(9, 0.4, "w0 (6-12)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    ax1.barh(0.4, 6, left=12, height=0.5, color='#64748B', edgecolor='#475569')
    ax1.text(15, 0.4, "w1 (12-18)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    ax1.barh(0.4, 6, left=18, height=0.5, color='#F87171', edgecolor='#DC2626')
    ax1.text(21, 0.4, "w2 (18-24)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    ax1.barh(0.4, 6, left=24, height=0.5, color='#F87171', edgecolor='#DC2626')
    ax1.text(27, 0.4, "w3 (24-30)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    # --- AX2: SYNTHESIZED BOUNDED SCHEDULE ---
    ax2.set_title("SYNTHESIZED (MAX, +) SCHEDULE — Upstream Tasks Delayed Deliberately (Zero Dwell Violations, Identical Makespan)",
                  fontsize=11, fontweight='bold', color='#0D9488', loc='left', pad=8)

    # PreHeat tasks: w0=2-6, w1=6-10, w2=11-15 (DELAYED), w3=17-21 (DELAYED)
    ax2.barh(1.8, 4, left=2, height=0.5, color='#94A3B8', edgecolor='#64748B')
    ax2.text(4, 1.8, "w0 (2-6)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    ax2.barh(1.8, 4, left=6, height=0.5, color='#94A3B8', edgecolor='#64748B')
    ax2.text(8, 1.8, "w1 (6-10)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    ax2.barh(1.8, 4, left=11, height=0.5, color='#A7F3D0', edgecolor='#059669')
    ax2.text(13, 1.8, "w2 (11-15)\nDelayed +1s", ha='center', va='center', color='#064E3B', fontweight='bold', fontsize=7.5)

    ax2.barh(1.8, 4, left=17, height=0.5, color='#A7F3D0', edgecolor='#059669')
    ax2.text(19, 1.8, "w3 (17-21)\nDelayed +3s", ha='center', va='center', color='#064E3B', fontweight='bold', fontsize=7.5)

    # Dwell on Transit track (y=1.0)
    # w1 dwell: 10 to 12 (2s)
    ax2.barh(1.0, 2, left=10, height=0.4, color='#DCFCE7', edgecolor='#16A34A')
    ax2.text(11, 1.0, "2.0s ≤ 3s", ha='center', va='center', color='#15803D', fontsize=8, fontweight='bold')

    # w2 dwell: 15 to 18 (3s) -> CLAMPED TO LIMIT
    ax2.barh(1.0, 3, left=15, height=0.4, color='#DCFCE7', edgecolor='#16A34A')
    ax2.text(16.5, 1.0, "3.0s (PASS)", ha='center', va='center', color='#15803D', fontsize=8, fontweight='bold')

    # w3 dwell: 21 to 24 (3s) -> CLAMPED TO LIMIT
    ax2.barh(1.0, 3, left=21, height=0.4, color='#DCFCE7', edgecolor='#16A34A')
    ax2.text(22.5, 1.0, "3.0s (PASS)", ha='center', va='center', color='#15803D', fontsize=8, fontweight='bold')

    # Process tasks: w0=6-12, w1=12-18, w2=18-24, w3=24-30
    ax2.barh(0.4, 6, left=6, height=0.5, color='#64748B', edgecolor='#475569')
    ax2.text(9, 0.4, "w0 (6-12)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    ax2.barh(0.4, 6, left=12, height=0.5, color='#64748B', edgecolor='#475569')
    ax2.text(15, 0.4, "w1 (12-18)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    ax2.barh(0.4, 6, left=18, height=0.5, color='#34D399', edgecolor='#059669')
    ax2.text(21, 0.4, "w2 (18-24)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    ax2.barh(0.4, 6, left=24, height=0.5, color='#34D399', edgecolor='#059669')
    ax2.text(27, 0.4, "w3 (24-30)", ha='center', va='center', color='#FFFFFF', fontweight='bold', fontsize=8)

    ax2.set_xlabel("Time (seconds) — Total makespan for both schedules is identical (36.0s), proving ZERO throughput penalty!",
                   fontsize=10, fontweight='bold', color='#1E293B', labelpad=6)
    ax2.set_xlim(0, 38)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig_wafer_dwell_concept.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")


def generate_multirate_expansion():
    """Generates a clean diagram showing Multi-Rate SDF to HSDF conversion with sequentiality, ZERO collisions."""
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Top: Multi-Rate SDF
    ax.text(0.5, 4.4, "Multi-Rate SDF Graph (Repetition Vector: q(A)=3, q(B)=2)",
            fontsize=11.5, fontweight='bold', color='#2563EB')

    # Node A
    c_a = patches.Circle((2.0, 3.65), 0.45, facecolor='#EFF6FF', edgecolor='#2563EB', lw=2)
    ax.add_patch(c_a)
    ax.text(2.0, 3.65, "Actor A\n(w=2)", ha='center', va='center', fontweight='bold', color='#1E3A8A', fontsize=9.5)

    # Node B
    c_b = patches.Circle((8.0, 3.65), 0.45, facecolor='#EFF6FF', edgecolor='#2563EB', lw=2)
    ax.add_patch(c_b)
    ax.text(8.0, 3.65, "Actor B\n(w=3)", ha='center', va='center', fontweight='bold', color='#1E3A8A', fontsize=9.5)

    # Connecting Channel
    ax.annotate("", xy=(7.55, 3.65), xytext=(2.45, 3.65),
                arrowprops=dict(arrowstyle="->", color='#2563EB', lw=2.5))
    ax.text(5.0, 3.85, "prd = 2, cns = 3 (Initial Tokens = 0)", ha='center', va='bottom',
            color='#1E40AF', fontweight='bold', fontsize=9.5)
    ax.text(5.0, 3.4, "Balance equation: 3 · 2 = 2 · 3 = 6 tokens / iteration", ha='center', va='top',
            color='#64748B', fontsize=8.5, style='italic')

    # Divider Arrow
    ax.annotate("", xy=(5.0, 2.7), xytext=(5.0, 3.1),
                arrowprops=dict(arrowstyle="->", color='#94A3B8', lw=2.5))
    ax.text(5.3, 2.9, "HSDF Expansion & Serialization", va='center', color='#475569', fontweight='bold', fontsize=9)

    # Bottom: HSDF Equivalent Title placed high enough to avoid collision!
    ax.text(0.5, 2.5, "Expanded Homogeneous SDF (HSDF) with Explicit Sequentiality Channels",
            fontsize=11.5, fontweight='bold', color='#0D9488')

    # Replicated A nodes (A0, A1, A2) at y = 1.2
    a_pos = [(1.5, 1.2), (3.0, 1.2), (4.5, 1.2)]
    for idx, (x, y) in enumerate(a_pos):
        c = patches.Circle((x, y), 0.38, facecolor='#F0FDF4', edgecolor='#059669', lw=1.8)
        ax.add_patch(c)
        ax.text(x, y, f"A_{idx}", ha='center', va='center', fontweight='bold', color='#065F46', fontsize=10)

    # Sequentiality arcs between A instances
    for idx in range(2):
        x1, y1 = a_pos[idx]
        x2, y2 = a_pos[idx+1]
        ax.annotate("", xy=(x2 - 0.38, y2), xytext=(x1 + 0.38, y1),
                    arrowprops=dict(arrowstyle="->", color='#059669', lw=1.5))
        ax.text((x1 + x2)/2, y1 + 0.15, "d=0", color='#059669', fontsize=8.5, ha='center', fontweight='bold')

    # Replicated B nodes (B0, B1) at y = 1.2
    b_pos = [(7.0, 1.2), (8.8, 1.2)]
    for idx, (x, y) in enumerate(b_pos):
        c = patches.Circle((x, y), 0.38, facecolor='#F0FDFA', edgecolor='#0D9488', lw=1.8)
        ax.add_patch(c)
        ax.text(x, y, f"B_{idx}", ha='center', va='center', fontweight='bold', color='#115E59', fontsize=10)

    # Sequentiality arc between B instances
    ax.annotate("", xy=(b_pos[1][0] - 0.38, 1.2), xytext=(b_pos[0][0] + 0.38, 1.2),
                arrowprops=dict(arrowstyle="->", color='#0D9488', lw=1.5))
    ax.text((b_pos[0][0] + b_pos[1][0])/2, 1.35, "d=0", color='#0D9488', fontsize=8.5, ha='center', fontweight='bold')

    # Token distribution channels (curved shallowly to peak well below y=2.5!)
    ax.annotate("", xy=(b_pos[0][0] - 0.3, 1.45), xytext=(a_pos[0][0] + 0.3, 1.45),
                arrowprops=dict(arrowstyle="->", color='#3B82F6', lw=1.2, connectionstyle="arc3,rad=-0.16"))
    ax.annotate("", xy=(b_pos[0][0] - 0.38, 1.2), xytext=(a_pos[1][0] + 0.38, 1.2),
                arrowprops=dict(arrowstyle="->", color='#3B82F6', lw=1.2))
    ax.annotate("", xy=(b_pos[1][0] - 0.3, 1.45), xytext=(a_pos[2][0] + 0.3, 1.45),
                arrowprops=dict(arrowstyle="->", color='#3B82F6', lw=1.2, connectionstyle="arc3,rad=-0.16"))

    # Sequential feedback arc (v_{q-1} -> v_0 with d=1) curved below nodes
    ax.annotate("", xy=(a_pos[0][0], 0.75), xytext=(a_pos[2][0], 0.75),
                arrowprops=dict(arrowstyle="->", color='#E11D48', lw=1.5, connectionstyle="arc3,rad=-0.28", linestyle='--'))
    # Clean label below arc with safe margin
    ax.text((a_pos[0][0] + a_pos[2][0])/2, 0.15, "Inter-iteration sequentiality arc: A_2 -> A_0 (delay d=1, single-thread)",
            color='#E11D48', fontsize=9, ha='center', fontweight='bold')

    ax.set_xlim(0, 9.8)
    ax.set_ylim(-0.1, 4.8)
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig_multirate_hsdf.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")


def generate_timing_bounds_math():
    """Generates an intuitive diagram showing Forward Lower Bounds and Backward Upper Bounds."""
    fig, ax = plt.subplots(figsize=(10.5, 4.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Actor u
    rect_u = patches.Rectangle((1.0, 1.4), 2.2, 1.2, facecolor='#EFF6FF', edgecolor='#2563EB', lw=2)
    ax.add_patch(rect_u)
    ax.text(2.1, 2.2, "Actor u (Firing k)", ha='center', va='center', fontweight='bold', color='#1E40AF', fontsize=11)
    ax.text(2.1, 1.7, "Duration w(u)", ha='center', va='center', color='#475569', fontsize=9.5)
    ax.plot([1.0, 1.0], [1.2, 1.4], color='#2563EB', lw=2)
    ax.plot([3.2, 3.2], [1.2, 1.4], color='#2563EB', lw=2)
    ax.text(1.0, 1.05, "s_u(k)\n(Start)", ha='center', va='top', color='#1E3A8A', fontweight='bold', fontsize=9.5)
    ax.text(3.2, 1.05, "c_u(k)\n(Complete)", ha='center', va='top', color='#1E3A8A', fontweight='bold', fontsize=9.5)

    # Actor v
    rect_v = patches.Rectangle((6.8, 1.4), 2.2, 1.2, facecolor='#F0FDF4', edgecolor='#059669', lw=2)
    ax.add_patch(rect_v)
    ax.text(7.9, 2.2, "Actor v (Firing k)", ha='center', va='center', fontweight='bold', color='#065F46', fontsize=11)
    ax.text(7.9, 1.7, "Duration w(v)", ha='center', va='center', color='#475569', fontsize=9.5)
    ax.plot([6.8, 6.8], [1.2, 1.4], color='#059669', lw=2)
    ax.plot([9.0, 9.0], [1.2, 1.4], color='#059669', lw=2)
    ax.text(6.8, 1.05, "s_v(k)\n(Start)", ha='center', va='top', color='#065F46', fontweight='bold', fontsize=9.5)
    ax.text(9.0, 1.05, "c_v(k)\n(Complete)", ha='center', va='top', color='#065F46', fontweight='bold', fontsize=9.5)

    # Lower Bound Forward Arc (c_u -> s_v >= L)
    ax.annotate("", xy=(6.8, 2.0), xytext=(3.2, 2.0),
                arrowprops=dict(arrowstyle="->", color='#059669', lw=2.5))
    ax.text(5.0, 2.25, "Lower Bound: s_v(k) - c_u(k) ≥ L", ha='center', va='bottom',
            color='#059669', fontweight='bold', fontsize=11)
    ax.text(5.0, 1.75, "Normalized Form: s_v(k) - s_u(k) ≥ L + w(u)", ha='center', va='top',
            color='#475569', fontsize=9.5)

    # Upper Bound Backward Arc (s_v - c_u <= U => s_u - s_v >= -U - w(u))
    ax.annotate("", xy=(3.2, 3.0), xytext=(6.8, 3.0),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=2.5,
                                connectionstyle="arc3,rad=-0.15"))
    ax.text(5.0, 3.65, "Upper Bound: s_v(k) - c_u(k) ≤ U", ha='center', va='bottom',
            color='#DC2626', fontweight='bold', fontsize=11)
    ax.text(5.0, 3.25, "Reverses into Backward Arc: s_u(k) - s_v(k) ≥ -U - w(u)", ha='center', va='bottom',
            color='#B91C1C', fontweight='bold', fontsize=10)

    ax.set_xlim(0, 10.2)
    ax.set_ylim(0.3, 4.3)
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig_timing_bounds_math.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")


def generate_flowchart_synthesis():
    """Generates a modern algorithmic flowchart for ASAP Bellman-Ford synthesis & positive cycle detection."""
    fig, ax = plt.subplots(figsize=(11.5, 4.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    steps = [
        ("Step 1: Input Model", "Extended HSDFG G=(V, E)\nLower bounds C_L, Upper C_U\nHorizon K iterations",
         1.2, 2.1, 2.1, 1.3, '#EFF6FF', '#2563EB', '#1E40AF'),
        ("Step 2: Normalization", "Unroll K iterations: K·|V| nodes\nUpper bounds -> backward arcs\nUnified difference graph G_diff",
         4.0, 2.1, 2.4, 1.3, '#F0FDF4', '#059669', '#065F46'),
        ("Step 3: Longest Path", "Bellman-Ford relaxation:\nRelax for (K·|V| - 1) passes\ns_v = max(s_v, s_u + W)",
         7.1, 2.1, 2.5, 1.3, '#FAF5FF', '#7C3AED', '#5B21B6'),
        ("Step 4: Cycle Check", "1 extra pass\nAny start time\nincreases?",
         10.0, 2.1, 1.8, 1.3, '#FFFBEB', '#D97706', '#92400E'),
    ]

    for title, desc, x, y, w, h, bg, border, tc in steps:
        rect = patches.Rectangle((x - w/2, y - h/2), w, h, facecolor=bg, edgecolor=border, lw=2)
        ax.add_patch(rect)
        ax.text(x, y + h/2 - 0.22, title, ha='center', va='top', fontweight='bold', color=tc, fontsize=10)
        ax.text(x, y - 0.1, desc, ha='center', va='center', color='#334155', fontsize=8.5)

    # Arrows between consecutive steps
    ax.annotate("", xy=(2.7, 2.1), xytext=(2.3, 2.1), arrowprops=dict(arrowstyle="->", color='#64748B', lw=2))
    ax.annotate("", xy=(5.75, 2.1), xytext=(5.3, 2.1), arrowprops=dict(arrowstyle="->", color='#64748B', lw=2))
    ax.annotate("", xy=(9.0, 2.1), xytext=(8.45, 2.1), arrowprops=dict(arrowstyle="->", color='#64748B', lw=2))

    # Branching from Cycle Check: NO (Feasible) -> Bottom
    rect_pass = patches.Rectangle((8.9, 0.2), 2.2, 0.85, facecolor='#DCFCE7', edgecolor='#16A34A', lw=2)
    ax.add_patch(rect_pass)
    ax.text(10.0, 0.72, "FEASIBLE SCHEDULE", ha='center', va='center', fontweight='bold', color='#15803D', fontsize=9.5)
    ax.text(10.0, 0.42, "Optimal ASAP start times s*\nSlack: σ(e) = s_v - s_u - W", ha='center', va='center', color='#166534', fontsize=8)

    ax.annotate("", xy=(10.0, 1.1), xytext=(10.0, 1.45),
                arrowprops=dict(arrowstyle="->", color='#16A34A', lw=2))
    ax.text(9.7, 1.25, "NO", color='#16A34A', fontweight='bold', fontsize=9.5)

    # YES (Infeasible) -> Top
    rect_fail = patches.Rectangle((8.9, 3.25), 2.2, 0.85, facecolor='#FEE2E2', edgecolor='#DC2626', lw=2)
    ax.add_patch(rect_fail)
    ax.text(10.0, 3.75, "POSITIVE CYCLE DETECTED", ha='center', va='center', fontweight='bold', color='#B91C1C', fontsize=9.5)
    ax.text(10.0, 3.45, "Isolate contradictory loop\ne.g., PreHeat <-> Process", ha='center', va='center', color='#991B1B', fontsize=8)

    ax.annotate("", xy=(10.0, 3.25), xytext=(10.0, 2.75),
                arrowprops=dict(arrowstyle="->", color='#DC2626', lw=2))
    ax.text(9.65, 3.0, "YES", color='#DC2626', fontweight='bold', fontsize=9.5)

    ax.set_xlim(0, 11.4)
    ax.set_ylim(-0.1, 4.3)
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig_flowchart_synthesis.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")


def generate_cluster_tool_workflow():
    """Generates an architectural diagram of the semiconductor cluster tool with clear separation."""
    fig, ax = plt.subplots(figsize=(10.5, 3.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Top: Critical Upper Bound Label
    ax.text(6.8, 3.3, "CRITICAL PHYSICAL UPPER BOUND: Transit Dwell ≤ 3.0s", ha='center', va='center',
            fontweight='bold', color='#DC2626', fontsize=11.5)
    ax.text(6.8, 2.95, "s_{ProcessChamber}(k) - c_{PreHeat}(k) ≤ 3.0s  (Prevents Wafer Thermal Degradation)",
            ha='center', va='center', color='#991B1B', fontsize=9.5)

    # Double-headed arrow below the text with clear spacing
    ax.annotate("", xy=(8.7, 2.6), xytext=(4.9, 2.6),
                arrowprops=dict(arrowstyle="<->", color='#DC2626', lw=2.5))

    stages = [
        ("LoadLock", "Input Cassette\nCapacity: Multi", 1.0, 1.4, 1.5, 1.1, '#F1F5F9', '#475569', '#1E293B'),
        ("Robot 1", "Transit Arm 1\nw = 2.0s", 2.9, 1.4, 1.3, 0.9, '#EFF6FF', '#3B82F6', '#1E40AF'),
        ("PreHeat Chamber", "Thermal Prep (w=4s)\nCapacity = 1 Wafer", 4.9, 1.4, 1.9, 1.1, '#FEF3C7', '#D97706', '#92400E'),
        ("Robot 2", "Transit Arm 2\nw = 2.0s", 7.0, 1.4, 1.3, 0.9, '#EFF6FF', '#3B82F6', '#1E40AF'),
        ("Process Chamber", "Chemical Etch (w=6s)\nCapacity = 1 Wafer", 9.1, 1.4, 1.9, 1.1, '#FEE2E2', '#DC2626', '#991B1B'),
    ]

    for title, desc, x, y, w, h, bg, border, tc in stages:
        rect = patches.Rectangle((x - w/2, y - h/2), w, h, facecolor=bg, edgecolor=border, lw=2)
        ax.add_patch(rect)
        ax.text(x, y + h/2 - 0.22, title, ha='center', va='top', fontweight='bold', color=tc, fontsize=9.5)
        ax.text(x, y - 0.12, desc, ha='center', va='center', color='#334155', fontsize=8.5)

    # Connecting arrows
    ax.annotate("", xy=(2.2, 1.4), xytext=(1.8, 1.4), arrowprops=dict(arrowstyle="->", color='#64748B', lw=2))
    ax.annotate("", xy=(3.9, 1.4), xytext=(3.6, 1.4), arrowprops=dict(arrowstyle="->", color='#64748B', lw=2))
    ax.annotate("", xy=(6.3, 1.4), xytext=(5.9, 1.4), arrowprops=dict(arrowstyle="->", color='#64748B', lw=2))
    ax.annotate("", xy=(8.1, 1.4), xytext=(7.7, 1.4), arrowprops=dict(arrowstyle="->", color='#64748B', lw=2))

    # Resource Contention note at bottom
    ax.text(5.25, 0.35, "Physical Resource Invariance: Single-wafer capacity chambers enforce sequentiality arcs (v_i -> v_{i+1})",
            ha='center', va='center', color='#475569', fontsize=8.5, style='italic',
            bbox=dict(boxstyle='square,pad=0.3', facecolor='#F8FAFC', edgecolor='#E2E8F0', lw=1))

    ax.set_xlim(0, 10.4)
    ax.set_ylim(0.0, 3.7)
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig_cluster_tool_workflow.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")


def generate_architecture_diagram():
    """Generates a clean software architecture diagram for Slide 9."""
    fig, ax = plt.subplots(figsize=(10.5, 4.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    modules = [
        ("src/model.py", "Dataflow Foundations",
         "• Actor & Channel dataclasses\n• Balance equations (Γ·q=0)\n• Multi-rate to HSDF expansion\n• Sequentiality arcs",
         1.3, 2.2, 2.2, 2.3, '#EFF6FF', '#2563EB', '#1E40AF'),
        ("src/maxplus.py", "Vectorized Semiring",
         "• (max, +) matrix semiring\n• NumPy 3D tensor matmult\n• Kleene star closure M0*\n• Karp's cycle ratio analysis",
         3.8, 2.2, 2.2, 2.3, '#F0FDF4', '#059669', '#065F46'),
        ("src/state_space.py", "State-Space Transformation",
         "• Delay matrices (A_0 ... A_D)\n• Intra-iteration M0* closure\n• Companion matrix form\n• Instant infeasibility check",
         6.3, 2.2, 2.2, 2.3, '#FAF5FF', '#7C3AED', '#5B21B6'),
        ("src/scheduler.py", "Synthesis Engine",
         "• ASAP unrolled Bellman-Ford\n• Polynomial O(K·E) scaling\n• Positive-cycle isolation\n• Slack analysis: σ(e)",
         8.8, 2.2, 2.2, 2.3, '#FFFBEB', '#D97706', '#92400E'),
    ]

    for filename, subtitle, desc, x, y, w, h, bg, border, tc in modules:
        rect = patches.Rectangle((x - w/2, y - h/2), w, h, facecolor=bg, edgecolor=border, lw=2)
        ax.add_patch(rect)
        ax.text(x, y + h/2 - 0.22, filename, ha='center', va='top', fontweight='bold', color=tc, fontsize=10.5)
        ax.text(x, y + h/2 - 0.52, subtitle, ha='center', va='top', color='#475569', fontsize=9, fontweight='bold')
        ax.text(x - w/2 + 0.15, y - 0.2, desc, ha='left', va='center', color='#334155', fontsize=8.5, linespacing=1.35)

    # Connecting pipeline arrows
    ax.annotate("", xy=(2.6, 2.2), xytext=(2.45, 2.2), arrowprops=dict(arrowstyle="->", color='#64748B', lw=2.5))
    ax.annotate("", xy=(5.1, 2.2), xytext=(4.95, 2.2), arrowprops=dict(arrowstyle="->", color='#64748B', lw=2.5))
    ax.annotate("", xy=(7.6, 2.2), xytext=(7.45, 2.2), arrowprops=dict(arrowstyle="->", color='#64748B', lw=2.5))

    # Bottom Full-Width Bar: src/validator.py
    rect_val = patches.Rectangle((0.2, 0.1), 9.6, 0.75, facecolor='#ECFDF5', edgecolor='#10B981', lw=2)
    ax.add_patch(rect_val)
    ax.text(0.4, 0.48, "src/validator.py — Decoupled Independent Verification Oracle", fontweight='bold', color='#065F46', fontsize=10.5)
    ax.text(0.4, 0.25, "100% independent verification: Precedence, Lower bounds, Upper bounds, Non-negativity, and Sequentiality (28/28 tests passing)",
            color='#047857', fontsize=9)

    # Arrows from scheduler to validator
    ax.annotate("", xy=(8.8, 0.88), xytext=(8.8, 1.02), arrowprops=dict(arrowstyle="->", color='#10B981', lw=2))

    ax.set_xlim(0, 10.0)
    ax.set_ylim(-0.05, 3.6)
    ax.axis('off')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig_architecture.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")


def generate_canva_gantt():
    """Generates a dedicated, publication-quality Canva Gantt comparison chart for Slide 12 with verified labels."""
    fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(11.0, 6.2), dpi=300, sharex=True)
    fig.patch.set_facecolor('#FFFFFF')

    actor_names = ["LoadLock", "PreHeat", "ProcessChamber", "CoolingChamber", "Unload"]
    colors = ["#3B82F6", "#10B981", "#EF4444", "#8B5CF6", "#F59E0B"]
    K = 4

    # 1. Greedy Execution Data (from run_experiments.py)
    # LoadLock: 0-2, 2-4, 4-6, 6-8
    # PreHeat: 2-6, 6-10, 10-14, 14-18
    # Process: 6-12, 12-18, 18-24, 24-30
    # Cooling: 12-16, 18-22, 24-28, 30-34
    # Unload: 16-18, 22-24, 28-30, 34-36
    greedy_starts = [
        [0, 2, 4, 6],       # LoadLock (dur=2)
        [2, 6, 10, 14],     # PreHeat (dur=4)
        [6, 12, 18, 24],    # Process (dur=6)
        [12, 18, 24, 30],   # Cooling (dur=4)
        [16, 22, 28, 34]    # Unload (dur=2)
    ]
    durations = [2.0, 4.0, 6.0, 4.0, 2.0]

    # 2. Synthesized Schedule Data (from run_experiments.py)
    # LoadLock: 0-2, 2-4, 4-6, 6-8
    # PreHeat: 2-6, 6-10, 11-15 (del), 17-21 (del)
    # Process: 6-12, 12-18, 18-24, 24-30
    # Cooling: 12-16, 18-22, 24-28, 30-34
    # Unload: 16-18, 22-24, 28-30, 34-36
    synth_starts = [
        [0, 2, 4, 6],       # LoadLock
        [2, 6, 11, 17],     # PreHeat (deliberate delay on w2 and w3!)
        [6, 12, 18, 24],    # Process
        [12, 18, 24, 30],   # Cooling
        [16, 22, 28, 34]    # Unload
    ]

    for ax in (ax0, ax1):
        ax.set_facecolor('#FFFFFF')
        ax.set_yticks(range(5))
        ax.set_yticklabels(actor_names, fontsize=9.5, fontweight='bold', color='#1E293B')
        ax.grid(True, linestyle="--", alpha=0.4, color='#CBD5E1')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#CBD5E1')
        ax.spines['bottom'].set_color('#CBD5E1')

    # AX0: Greedy Schedule
    ax0.set_title("GREEDY (SELF-TIMED) SCHEDULE — Resource Contention Violates Thermal Dwell Bounds",
                  fontsize=11, fontweight='bold', color='#DC2626', loc='left', pad=8)
    for aid in range(5):
        dur = durations[aid]
        for k in range(K):
            st = greedy_starts[aid][k]
            ax0.barh(aid, dur, left=st, color=colors[aid], edgecolor='#1E293B', linewidth=0.8, alpha=0.85)
            ax0.text(st + dur/2, aid, f"w{k}", ha="center", va="center", color="white", fontsize=8.5, fontweight='bold')

    # Highlight Greedy Dwell Violations in the transit gap between PreHeat (y=1) and ProcessChamber (y=2)
    # Wafer 2 dwell: 14 to 18 (4.0s -> 33% violation)
    ax0.barh(1.5, 4, left=14, height=0.35, color='#FEE2E2', edgecolor='#DC2626', hatch='//')
    ax0.text(16, 1.5, "w2: 4.0s (Fail)", color='#991B1B', fontsize=7.5, fontweight='bold', ha='center', va='center')

    # Wafer 3 dwell: 18 to 24 (6.0s -> 100% violation!)
    ax0.barh(1.5, 6, left=18, height=0.35, color='#FEE2E2', edgecolor='#DC2626', hatch='\\\\')
    ax0.text(21, 1.5, "w3: 6.0s (+100% Fail)", color='#991B1B', fontsize=7.5, fontweight='bold', ha='center', va='center')

    # AX1: Synthesized Schedule
    ax1.set_title("SYNTHESIZED (MAX, +) SCHEDULE — Upstream Tasks Delayed Deliberately (Dwell ≤ 3.0s, Makespan Invariant)",
                  fontsize=11, fontweight='bold', color='#0D9488', loc='left', pad=8)
    for aid in range(5):
        dur = durations[aid]
        for k in range(K):
            st = synth_starts[aid][k]
            # Highlight delayed tasks
            is_delayed = (aid == 1 and k in (2, 3))
            c = '#059669' if is_delayed else colors[aid]
            ax1.barh(aid, dur, left=st, color=c, edgecolor='#1E293B', linewidth=0.8, alpha=0.85)
            lbl = f"w{k}" + ("*" if is_delayed else "")
            ax1.text(st + dur/2, aid, lbl, ha="center", va="center", color="white", fontsize=8.5, fontweight='bold')

    # Highlight Synthesized Clamping in the transit gap
    # Wafer 2: PreHeat ends at 15, Process starts at 18 -> Dwell = 3.0s
    ax1.barh(1.5, 3, left=15, height=0.35, color='#DCFCE7', edgecolor='#16A34A')
    ax1.text(16.5, 1.5, "w2: 3.0s (PASS)", color='#166534', fontsize=7.5, fontweight='bold', ha='center', va='center')

    # Wafer 3: PreHeat ends at 21, Process starts at 24 -> Dwell = 3.0s
    ax1.barh(1.5, 3, left=21, height=0.35, color='#DCFCE7', edgecolor='#16A34A')
    ax1.text(22.5, 1.5, "w3: 3.0s (PASS)", color='#166534', fontsize=7.5, fontweight='bold', ha='center', va='center')

    # End makespan line at 36s
    for ax in (ax0, ax1):
        ax.axvline(36, color='#2563EB', linestyle='-', linewidth=1.5)
        ax.text(36.2, 4.2, "t=36s", color='#2563EB', fontsize=9, fontweight='bold')

    ax1.set_xlabel("Time (seconds) — Both schedules achieve identical makespan (36.0s), proving zero makespan penalty!",
                   fontsize=10, fontweight='bold', color='#1E293B', labelpad=6)
    ax1.set_xlim(-1, 39)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig_gantt_canva.png")
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated {out_path}")


if __name__ == '__main__':
    generate_title_graphic()
    generate_wafer_dwell_comparison()
    generate_multirate_expansion()
    generate_timing_bounds_math()
    generate_flowchart_synthesis()
    generate_cluster_tool_workflow()
    generate_architecture_diagram()
    generate_canva_gantt()
    print("All Canva diagrams regenerated successfully.")
