"""
Generate a professional, publication-quality PDF of the CS637 Presentation Speaker Scripts,
clearly divided by person (Prem, Badri, Rahaman, Hemanth, Karthik).
Every speaker has a dedicated 2-page section (total 11 pages), with running headers,
footers, page numbers, and clickable PDF Table of Contents bookmarks.
"""

import os
import subprocess
import shutil
import re
import fitz

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CS637 Presentation Speaker Scripts - Schedule Synthesis Reproduction</title>
<style>
  @page {
    size: A4;
    margin: 12mm 14mm 14mm 14mm;
  }

  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    line-height: 1.45;
    font-size: 9.2pt;
    margin: 0;
    padding: 0;
  }

  h1, h2, h3, h4 {
    color: #0f172a;
    margin-top: 0;
    font-weight: 700;
  }

  /* Cover & Overview Page */
  .cover-container {
    padding-top: 4px;
    padding-bottom: 10px;
  }

  .header-badge {
    display: inline-block;
    background-color: #e0e7ff;
    color: #3730a3;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 4px;
    margin-bottom: 6px;
  }

  .main-title {
    font-size: 17pt;
    line-height: 1.25;
    color: #0f172a;
    margin-bottom: 4px;
  }

  .subtitle {
    font-size: 10pt;
    color: #475569;
    margin-bottom: 12px;
    line-height: 1.35;
  }

  .paper-card {
    background-color: #f8fafc;
    border-left: 4px solid #2563eb;
    border-top: 1px solid #e2e8f0;
    border-right: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    padding: 8px 12px;
    border-radius: 0 6px 6px 0;
    margin-bottom: 14px;
    font-size: 8.8pt;
    line-height: 1.45;
  }

  .paper-card strong {
    color: #1e3a8a;
  }

  /* Table Styling */
  table.roster-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 14px;
    font-size: 8.8pt;
  }

  table.roster-table th {
    background-color: #0f172a;
    color: #ffffff;
    text-align: left;
    padding: 6px 9px;
    font-weight: 600;
    font-size: 8.5pt;
    letter-spacing: 0.03em;
  }

  table.roster-table td {
    padding: 6px 9px;
    border-bottom: 1px solid #e2e8f0;
  }

  table.roster-table tr:nth-child(even) td {
    background-color: #f8fafc;
  }

  .speaker-num-badge {
    display: inline-block;
    width: 18px;
    height: 18px;
    line-height: 18px;
    text-align: center;
    background-color: #2563eb;
    color: #ffffff;
    border-radius: 50%;
    font-weight: 700;
    font-size: 7.5pt;
  }

  .pronunciation-box {
    background-color: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 14px;
    font-size: 8.5pt;
  }

  .pronunciation-box h4 {
    margin-bottom: 5px;
    color: #334155;
    font-size: 9pt;
  }

  .pronunciation-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px 14px;
  }

  /* Page Break Rule */
  .page-break {
    page-break-before: always;
  }

  /* Speaker Division Banner */
  .speaker-section-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    color: #ffffff;
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 10px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }

  .speaker-meta-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2px;
  }

  .speaker-tag {
    background-color: #3b82f6;
    color: #ffffff;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 2px 7px;
    border-radius: 3px;
  }

  .speaker-time-badge {
    background-color: rgba(255, 255, 255, 0.2);
    color: #f8fafc;
    font-size: 7.5pt;
    font-weight: 600;
    padding: 2px 7px;
    border-radius: 3px;
  }

  .speaker-name {
    font-size: 14pt;
    font-weight: 700;
    color: #ffffff;
    margin: 1px 0 2px 0;
  }

  .speaker-role {
    font-size: 8.5pt;
    color: #cbd5e1;
    margin: 0;
  }

  /* Slide Block */
  .slide-block {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px 11px;
    margin-bottom: 8px;
    page-break-inside: avoid;
  }

  .slide-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-bottom: 6px;
  }

  .slide-title-wrap {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .slide-badge {
    background-color: #0f172a;
    color: #ffffff;
    font-weight: 700;
    font-size: 7.5pt;
    padding: 2px 6px;
    border-radius: 3px;
  }

  .slide-title {
    font-size: 9.8pt;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
  }

  .slide-timing {
    font-size: 7.5pt;
    font-weight: 600;
    color: #64748b;
    background-color: #f1f5f9;
    padding: 1px 6px;
    border-radius: 3px;
  }

  /* Visual Cue Box */
  .visual-cue-box {
    background-color: #f8fafc;
    border-left: 3px solid #3b82f6;
    padding: 4px 8px;
    font-size: 8pt;
    color: #334155;
    margin-bottom: 6px;
    border-radius: 0 3px 3px 0;
  }

  .visual-cue-box strong {
    color: #1e40af;
  }

  /* Spoken Text */
  .script-content {
    font-size: 8.8pt;
    line-height: 1.42;
    color: #1e293b;
    margin: 0 0 5px 0;
    text-align: justify;
  }

  .script-content em {
    font-style: italic;
    color: #0f172a;
  }

  /* Handoff Box */
  .handoff-box {
    background-color: #f0fdf4;
    border: 1px solid #86efac;
    border-left: 3.5px solid #16a34a;
    border-radius: 4px;
    padding: 5px 8px;
    font-size: 8.5pt;
    color: #166534;
    margin-top: 6px;
  }

  .handoff-box strong {
    color: #14532d;
    text-transform: uppercase;
    font-size: 7.5pt;
    letter-spacing: 0.05em;
  }

  .math {
    font-family: 'Cambria Math', 'Times New Roman', serif;
    font-style: italic;
  }

  .footer-note {
    font-size: 8pt;
    color: #94a3b8;
    text-align: center;
    margin-top: 10px;
  }
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- COVER & EXECUTIVE SUMMARY PAGE (PAGE 1) -->
<!-- ========================================================================= -->
<div class="cover-container">
  <div class="header-badge">CS637: Embedded Systems · Research Paper Evaluation & Reproduction</div>
  <h1 class="main-title">Schedule Synthesis for Synchronous Dataflow Models with Lower and Upper Timing Bounds</h1>
  <div class="subtitle">Complete Presentation Speech Scripts · Equal 20% Team Distribution (4 Slides / 2 Pages per Speaker)</div>

  <div class="paper-card">
    <strong>Assigned Paper:</strong> <em>Schedule synthesis for synchronous dataflow models with lower and upper timing bounds</em><br>
    <strong>Authors:</strong> Joep van Wanrooij, Twan Basten, Marc Geilen (TU Eindhoven) — <em>ACM TECS / EMSOFT 2025</em> (DOI: 10.1145/3762643)<br>
    <strong>Target Presentation:</strong> <code>CS637_Presentation_Final.pptx</code> (20 Slides, 16:9 Widescreen) · <strong>Total Time:</strong> ~12–14 Minutes
  </div>

  <h3 style="font-size: 10.5pt; margin-bottom: 6px; border-bottom: 2px solid #0f172a; padding-bottom: 3px;">Speaker Order & Slide Allocation (4 Slides per Speaker)</h3>
  <table class="roster-table">
    <thead>
      <tr>
        <th style="width: 5%;">#</th>
        <th style="width: 23%;">Speaker Name</th>
        <th style="width: 14%;">Roll Number</th>
        <th style="width: 12%;">Slides</th>
        <th style="width: 34%;">Assigned Presentation Focus</th>
        <th style="width: 12%;">Target Time</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><span class="speaker-num-badge">1</span></td>
        <td><strong>Vempati Prem Santhosh</strong></td>
        <td>231137 (CSE)</td>
        <td><strong>Slides 1–4</strong></td>
        <td>Welcome, Title, Roadmap, Industrial Motivation, Research Gap</td>
        <td>~2.5–3.0 min</td>
      </tr>
      <tr>
        <td><span class="speaker-num-badge">2</span></td>
        <td><strong>Sanga Badri</strong></td>
        <td>230911 (CSE)</td>
        <td><strong>Slides 5–8</strong></td>
        <td>SDF/HSDF Semantics, Bound Inversion, Objectives, Max-Plus Algebra</td>
        <td>~2.5–3.0 min</td>
      </tr>
      <tr>
        <td><span class="speaker-num-badge">3</span></td>
        <td><strong>Sk J Ur Rahaman</strong> <em>(Lead)</em></td>
        <td>230951 (CSE)</td>
        <td><strong>Slides 9–12</strong></td>
        <td>4-Stage Pipeline, Alg 2 (Kleene), Alg 3 (Bellman-Ford), Worked Example</td>
        <td>~2.5–3.0 min</td>
      </tr>
      <tr>
        <td><span class="speaker-num-badge">4</span></td>
        <td><strong>Ampili Hemanth Kumar</strong></td>
        <td>230128 (CSE)</td>
        <td><strong>Slides 13–16</strong></td>
        <td>Formal Proofs, Test Oracle, Wafer Tool Results, Scalability Sweeps</td>
        <td>~2.5–3.0 min</td>
      </tr>
      <tr>
        <td><span class="speaker-num-badge">5</span></td>
        <td><strong>Koneti Karthik</strong></td>
        <td>230568 (CSE)</td>
        <td><strong>Slides 17–20</strong></td>
        <td>Critical Reflection, Takeaways, Bibliography, Team Roster & Q&A</td>
        <td>~2.5–3.0 min</td>
      </tr>
    </tbody>
  </table>

  <div class="pronunciation-box">
    <h4>Pronunciation & Key Mathematical Terminology</h4>
    <div class="pronunciation-grid">
      <div><strong>Joep van Wanrooij:</strong> <em>“Yoop van WAN-roy”</em></div>
      <div><strong>Twan Basten & Marc Geilen:</strong> <em>“Twan BAHS-ten & Marc GUY-len”</em></div>
      <div><strong>Kleene Star (M₀*):</strong> <em>“CLAY-nee star”</em></div>
      <div><strong>Max-Plus Semiring:</strong> (ℝ_max, ⊕, ⊗) with ⊕ as max and ⊗ as +</div>
      <div><strong>Maximum Cycle Ratio (λ*):</strong> <em>“Lambda star”</em> (minimal sustainable period)</div>
      <div><strong>HSDFG:</strong> <em>“Homogeneous Synchronous Dataflow Graph”</em></div>
      <div><strong>Wafer Dwell Limit:</strong> Transit thermal boundary window (≤ 3.0 s)</div>
      <div><strong>Bellman-Ford Algorithm:</strong> <em>“BELL-man FORD”</em> longest-path relaxation</div>
    </div>
  </div>

  <div class="footer-note">
    Department of Computer Science & Engineering · Indian Institute of Technology Kanpur (IITK)
  </div>
</div>

<!-- ========================================================================= -->
<!-- SPEAKER 1: VEMPATI PREM SANTHOSH (PAGES 2 & 3) -->
<!-- ========================================================================= -->
<div class="page-break"></div>

<!-- Page 2: Prem Part 1 (Banner + Slides 1 & 2) -->
<div class="speaker-section-banner">
  <div class="speaker-meta-top">
    <span class="speaker-tag">Speaker 1 · Part 1</span>
    <span class="speaker-time-badge">Slides 1 to 4 · Target: ~2.5–3.0 Minutes</span>
  </div>
  <div class="speaker-name">Vempati Prem Santhosh</div>
  <div class="speaker-role">Roll Number: 231137 · Dept. of Computer Science & Engineering, IIT Kanpur · Focus: Welcome, Problem Context & Research Gap</div>
</div>

<!-- Slide 1 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 1</span>
      <span class="slide-title">CS637: Embedded Systems · Research Paper Evaluation & Reproduction</span>
    </div>
    <span class="slide-timing">~40 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Title banner, authors (Joep van Wanrooij, Twan Basten, Marc Geilen), TU Eindhoven, EMSOFT 2025 badge, team roster, and ≤ 3.0 s wafer dwell window callout.
  </div>
  <p class="script-content">
    “Good morning, respected instructor and colleagues. Welcome to our CS637 Embedded Systems research project presentation.
  </p>
  <p class="script-content">
    Today, our team presents our complete evaluation and codebase reproduction of the EMSOFT 2025 research paper titled: <em>'Schedule synthesis for synchronous dataflow models with lower and upper timing bounds'</em>, authored by Joep van Wanrooij, Twan Basten, and Marc Geilen from Eindhoven University of Technology, published in ACM Transactions on Embedded Computing Systems.
  </p>
  <p class="script-content">
    Our team from the Department of Computer Science and Engineering at IIT Kanpur comprises five members: myself, Vempati Prem Santhosh, alongside Sanga Badri, our project lead Sk J Ur Rahaman, Ampili Hemanth Kumar, and Koneti Karthik. Each of us has contributed an equal twenty percent to this reproduction effort.
  </p>
  <p class="script-content">
    In this talk, we will demonstrate how analytical max-plus state-space algebra enables polynomial-time schedule synthesis for embedded dataflow systems with rigid upper timing bounds, validated on industrial semiconductor wafer cluster tools.”
  </p>
</div>

<!-- Slide 2 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 2</span>
      <span class="slide-title">OVERVIEW · Roadmap: Six Steps from Problem to Verdict</span>
    </div>
    <span class="slide-timing">~35 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> 6 numbered chapter cards: (1) The Problem, (2) The Model, (3) The Idea, (4) The Algorithms, (5) The Evidence, (6) The Verdict.
  </div>
  <p class="script-content">
    “Here is our roadmap for today's talk, structured into six sequential chapters.
  </p>
  <p class="script-content">
    First, in <em>The Problem</em>, we uncover why classical dataflow scheduling fails when upper timing bounds are introduced. 
    Second, in <em>The Model</em>, we formalize Synchronous Dataflow semantics and show how upper bounds are inverted into difference constraints. 
    Third, in <em>The Idea</em>, we reveal the core theoretical breakthrough: linearizing timing constraints into a max-plus semiring. 
    Fourth, in <em>The Algorithms</em>, we walk through the polynomial-time Kleene closure and Bellman-Ford synthesis algorithms with an illustrative worked example. 
    Fifth, in <em>The Evidence</em>, we present our formal correctness proofs, benchmark methodology, wafer cluster tool results, and scalability stress-tests. 
    Finally, in <em>The Verdict</em>, we provide our critical reflection, engineering conclusions, and open the floor for your questions.”
  </p>
</div>

<!-- Page 3: Prem Part 2 (Slides 3 & 4 + Handoff) -->
<div class="page-break"></div>

<!-- Slide 3 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 3</span>
      <span class="slide-title">01 · PRACTICAL MOTIVATION · When Firing Early Becomes a Defect</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Semiconductor wafer fab diagram, critical ≤ 3.0 s dwell limit, and red comparison highlighting greedy execution causing a catastrophic 6.0-second transit delay.
  </div>
  <p class="script-content">
    “Let us examine the practical motivation. In embedded real-time systems, Synchronous Dataflow—or SDF—is the gold standard for modeling concurrent streaming pipelines. Standard SDF assumes <em>self-timed execution</em>: actors fire greedily as soon as input tokens arrive. This naturally guarantees maximal throughput when only <em>lower</em> bounds exist—meaning an operation cannot start before its inputs are ready.
  </p>
  <p class="script-content">
    However, modern cyber-physical and manufacturing systems impose strict <em>upper</em> timing bounds. Consider semiconductor fabrication: a silicon wafer undergoes chemical vapor deposition in a high-temperature chamber. Once pre-heated, the wafer cannot dwell in transit for more than 3.0 seconds, or thermal decay ruins the wafer surface. Similarly, in hard real-time multimedia, video frames must traverse processing stages within bounded jitter windows to avoid buffer overflows.
  </p>
  <p class="script-content">
    This exposes the <em>Self-Timed Scheduling Paradox</em>: greedy execution fires tasks as early as possible. But if a downstream chamber is occupied, the upstream product is forced to wait in an unheated buffer. In a wafer tool, greedy execution forces a 6.0-second wait—a 100% defective wafer! Firing <em>early</em> is literally what causes the defect. We need schedule synthesis that guarantees correctness by construction.”
  </p>
</div>

<!-- Slide 4 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 4</span>
      <span class="slide-title">02 · RESEARCH GAP & ALGORITHMIC PARADIGMS · Why Prior Approaches Fall Short</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Comparison matrix contrasting Heuristic Throttling, MILP/SMT Solvers, Timed Automata, and the Proposed (max, +) State-Space approach.
  </div>
  <p class="script-content">
    “Why do existing scheduling paradigms fall short?
  </p>
  <p class="script-content">
    Designers historically faced an unacceptable compromise. On one hand, runtime heuristics and artificial delay insertion lack formal guarantees and fail under tight multi-stage dependencies. On the other hand, exact formal methods like Mixed-Integer Linear Programming or SMT solvers exhibit exponential worst-case complexity—timing out beyond thirty actors. Meanwhile, model-checking with Timed Automata suffers from severe state-space explosion due to dense continuous clock regions.
  </p>
  <p class="script-content">
    The central research gap is: <em>How can we enforce rigid bidirectional timing bounds on dataflow graphs while preserving polynomial-time scalability and analytical closed-form rigor?</em>
  </p>
  <p class="script-content">
    The paper's breakthrough is to recognize that upper bounds can be re-cast as backward difference constraints, embedded into max-plus linear state-space matrices, and solved via Kleene closure and longest-path propagation.”
  </p>
  <div class="handoff-box">
    <strong>Verbal Handoff to Speaker 2:</strong> “I will now pass the floor to Sanga Badri to walk us through the formal dataflow semantics and the timing bounds transformation.”
  </div>
</div>

<!-- ========================================================================= -->
<!-- SPEAKER 2: SANGA BADRI (PAGES 4 & 5) -->
<!-- ========================================================================= -->
<div class="page-break"></div>

<!-- Page 4: Badri Part 1 (Banner + Slides 5 & 6) -->
<div class="speaker-section-banner">
  <div class="speaker-meta-top">
    <span class="speaker-tag">Speaker 2 · Part 1</span>
    <span class="speaker-time-badge">Slides 5 to 8 · Target: ~2.5–3.0 Minutes</span>
  </div>
  <div class="speaker-name">Sanga Badri</div>
  <div class="speaker-role">Roll Number: 230911 · Dept. of Computer Science & Engineering, IIT Kanpur · Focus: Dataflow Semantics, Bound Inversion & Semiring Algebra</div>
</div>

<!-- Slide 5 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 5</span>
      <span class="slide-title">03 · FORMAL DATAFLOW SEMANTICS · SDF Foundations: Rates, Balance, HSDF</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Multi-rate token production/consumption diagram (u produces 2, v consumes 3), repetition vector q = [3, 2]ᵀ, balance nullspace equation Γ · q = 0, and non-reentrancy serialization loops.
  </div>
  <p class="script-content">
    “Thank you, Prem. I am Sanga Badri, and I will explain the formal dataflow foundations.
  </p>
  <p class="script-content">
    A Synchronous Dataflow graph <span class="math">G = (V, E, prd, cns, d, w)</span> consists of computational actors <span class="math">V</span>, connected by FIFO channels <span class="math">E</span>. Every time an actor <span class="math">u</span> fires, it produces a fixed number of tokens <span class="math">prd(e)</span>, and the consuming actor <span class="math">v</span> consumes <span class="math">cns(e)</span> tokens.
  </p>
  <p class="script-content">
    For an SDF graph to execute indefinitely with bounded buffer memory, it must be consistent. This is captured by the fundamental balance equation: <span class="math">Γ · q = 0</span>, where <span class="math">Γ</span> is the topology matrix and <span class="math">q</span> is the non-trivial repetition vector. For instance, if actor <span class="math">u</span> produces 2 tokens and actor <span class="math">v</span> consumes 3 tokens, consistency requires that <span class="math">u</span> fires 3 times for every 2 firings of <span class="math">v</span>, ensuring zero net token drift.
  </p>
  <p class="script-content">
    To enable analytical timing analysis, we expand the multi-rate SDF graph into an equivalent Homogeneous SDF—or HSDF—graph in <span class="math">O(|V| + |E|)</span> time, where each actor <span class="math">u</span> is instantiated into <span class="math">q(u)</span> single-rate sub-actors. To prevent a physical actor from firing concurrently with itself on multi-core hardware, we inject non-reentrancy serialization edges with zero delay between successive sub-instances, and a unit-delay loopback edge from the last sub-instance to the first.”
  </p>
</div>

<!-- Slide 6 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 6</span>
      <span class="slide-title">04 · TIMING BOUNDS SEMANTICS · Upper Bounds are Just Backward Arcs</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Algebraic derivation box showing s_dst(k) − s_src(k−δ) ≤ U' converting to s_src(k−δ) − s_dst(k) ≥ −U', and normalization rules for completion events.
  </div>
  <p class="script-content">
    “Now, let us examine the paper's key algebraic insight on timing bounds.
  </p>
  <p class="script-content">
    In an HSDF graph, timing constraints are defined between event timestamps: actor start times <span class="math">s_v(k)</span> and completion times <span class="math">c_v(k) = s_v(k) + w(v)</span>. A conventional precedence edge enforces a lower bound: <span class="math">s_dst(k) − s_src(k−δ) ≥ L'</span>.
  </p>
  <p class="script-content">
    But an upper timing bound states that the destination cannot start later than <span class="math">U'</span> time units after the source: <span class="math">s_dst(k) − s_src(k−δ) ≤ U'</span>.
  </p>
  <p class="script-content">
    The crucial mathematical move is multiplying this inequality by negative one:
    <br><center><span class="math">s_src(k−δ) − s_dst(k) ≥ −U'</span></center>
  </p>
  <p class="script-content">
    This simple inversion reveals that an upper bound from source to destination is mathematically identical to a <em>backward lower-bound constraint</em> from destination to source, carrying an iteration delay of <span class="math">−δ</span> and a negative weight of <span class="math">−U'</span>. All timing requirements collapse into one canonical form: <span class="math">s_target − s_source ≥ W</span>.”
  </p>
</div>

<!-- Page 5: Badri Part 2 (Slides 7 & 8 + Handoff) -->
<div class="page-break"></div>

<!-- Slide 7 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 7</span>
      <span class="slide-title">05 · MATHEMATICAL OPTIMIZATION OBJECTIVES · Two Objectives, One Constraint System</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Side-by-side comparison between Objective 1 (Finite-horizon makespan min) and Objective 2 (1-periodic throughput max Θ = 1/λ* via Karp's cycle mean).
  </div>
  <p class="script-content">
    “With all constraints unified into difference inequalities, we can formally state our two mathematical optimization objectives.
  </p>
  <p class="script-content">
    Objective 1 is <em>Finite-Horizon Makespan Minimization</em>. Given a finite batch of <span class="math">K</span> iterations—such as processing a lot of silicon wafers—we seek schedule vectors <span class="math">S*</span> that minimize the completion time of the latest actor: <span class="math">min_S max_v (s_v(K−1) + w(v))</span>, subject to our difference constraints, non-negativity, and non-reentrancy. Because all constraints are difference constraints, the earliest valid start times form the unique componentwise minimum, computed via longest-path propagation on the unrolled DAG.
  </p>
  <p class="script-content">
    Objective 2 is <em>1-Periodic Throughput Maximization</em> for infinite streaming runs. Here, execution repeats with a constant period <span class="math">λ</span>, such that <span class="math">s_v(k) = s_v(0) + k · λ</span>. The maximum throughput <span class="math">Θ = 1/λ*</span> is dictated by the maximum cycle ratio over all directed cycles with positive delays: <span class="math">λ* = max_γ W(γ) / D(γ)</span>.
  </p>
  <p class="script-content">
    Crucially, our backward upper-bound edges introduce cycles with <em>negative</em> token delays <span class="math">D(γ) &lt; 0</span>. These invert the inequality and impose an <em>upper bound</em> on the period: <span class="math">λ* ≤ W(γ) / D(γ)</span>. If the lower throughput bound exceeds the upper bound, the periodic schedule is provably unsatisfiable.”
  </p>
</div>

<!-- Slide 8 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 8</span>
      <span class="slide-title">06 · CORE THEORETICAL INSIGHT · Max-Plus Turns Bounds into Linear Algebra</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Semiring definition (ℝ_max, ⊕, ⊗), state equation x(k) = A₀⊗x(k) ⊕ A₁⊗x(k−1), and Kleene star series M₀* = I ⊕ M₀ ⊕ ... ⊕ M₀ⁿ⁻¹.
  </div>
  <p class="script-content">
    “This brings us to the theoretical heart of the paper: max-plus semiring linearization.
  </p>
  <p class="script-content">
    In classical algebra, synchronization and scheduling constraints appear non-linear because of the <span class="math">max</span> operator. However, in the max-plus semiring <span class="math">(ℝ ∪ {−∞}, ⊕, ⊗)</span>, we define addition as <span class="math">max(a, b)</span> and multiplication as conventional addition <span class="math">a + b</span>. Under this algebra, complex dataflow synchronization transforms into linear matrix-vector recurrence:
    <br><center><span class="math">x(k) = A₀ ⊗ x(k) ⊕ A₁ ⊗ x(k−1) ⊕ ... ⊕ A_D ⊗ x(k−D)</span></center>
  </p>
  <p class="script-content">
    Here, <span class="math">A₀</span> captures instantaneous, intra-iteration dependencies—including our backward upper-bound arcs. Because <span class="math">x(k)</span> appears on both sides of the equation, we resolve the implicit algebraic loop using the <em>Kleene star closure</em>:
    <br><center><span class="math">M₀* = I ⊕ M₀ ⊕ M₀² ⊕ ... ⊕ M₀ⁿ⁻¹</span></center>
  </p>
  <p class="script-content">
    In max-plus algebra, the Kleene star computes all-pairs longest paths in <span class="math">O(n³)</span> time without unrolling. If any diagonal entry <span class="math">(M₀*)_{ii} &gt; 0</span>, it proves that an intra-iteration contradictory cycle exists, immediately catching infeasibility.”
  </p>
  <div class="handoff-box">
    <strong>Verbal Handoff to Speaker 3:</strong> “I will now pass the floor to our project lead, Sk J Ur Rahaman, to walk us through the methodological pipeline, algorithmic formulations, and our worked example.”
  </div>
</div>

<!-- ========================================================================= -->
<!-- SPEAKER 3: SK J UR RAHAMAN (PAGES 6 & 7) -->
<!-- ========================================================================= -->
<div class="page-break"></div>

<!-- Page 6: Rahaman Part 1 (Banner + Slides 9 & 10) -->
<div class="speaker-section-banner">
  <div class="speaker-meta-top">
    <span class="speaker-tag">Speaker 3 · Part 1</span>
    <span class="speaker-time-badge">Slides 9 to 12 · Target: ~2.5–3.0 Minutes</span>
  </div>
  <div class="speaker-name">Sk J Ur Rahaman (Project Lead)</div>
  <div class="speaker-role">Roll Number: 230951 · Dept. of Computer Science & Engineering, IIT Kanpur · Focus: Pipeline Architecture, Synthesis Algorithms & Worked Trace</div>
</div>

<!-- Slide 9 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 9</span>
      <span class="slide-title">07 · METHODOLOGICAL PIPELINE · From Specification to Verified Schedule</span>
    </div>
    <span class="slide-timing">~40 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> 4-stage pipeline horizontal flow: Stage 1 (Normalization), Stage 2 (State-Space Construction), Stage 3 (Kleene Closure), and Stage 4 (Synthesis & Oracle Validation).
  </div>
  <p class="script-content">
    “Thank you, Badri. I am Sk J Ur Rahaman. I will explain the end-to-end synthesis pipeline and our algorithmic implementation.
  </p>
  <p class="script-content">
    The methodological architecture consists of four distinct stages.
  </p>
  <p class="script-content">
    In Stage 1, <em>Normalization</em>, we parse the Extended HSDF graph and convert all arbitrary start and completion bounds into canonical difference constraints <span class="math">s_j(k) − s_i(k−δ) ≥ W</span>.
  </p>
  <p class="script-content">
    In Stage 2, <em>State-Space Construction</em>, we build the max-plus transition matrices <span class="math">A₀</span> through <span class="math">A_D</span>. We embed backward upper bounds into <span class="math">A₀</span> and enforce sequential actor execution by setting <span class="math">(A₁)ᵥᵥ ≥ w(v)</span>.
  </p>
  <p class="script-content">
    In Stage 3, <em>Kleene Closure</em>, we compute <span class="math">M₀*</span> in <span class="math">O(D · n² + n³)</span> operations. This pre-computes all instantaneous paths and verifies that no positive-weight zero-delay cycles exist.
  </p>
  <p class="script-content">
    Finally, in Stage 4, <em>Synthesis and Independent Validation</em>, we unroll the system across <span class="math">K</span> iterations into an unrolled difference DAG, execute Bellman-Ford longest-path propagation in <span class="math">O(K · E)</span> time, and pass the resulting schedule to a completely decoupled verification oracle.”
  </p>
</div>

<!-- Slide 10 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 10</span>
      <span class="slide-title">08 · ALGORITHMIC FORMULATION · Algorithm 2: Kleene-Star State-Space Closure</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Algorithm 2 pseudocode, backward arc insertion at line 5 (A₀[u, v] ← max(A₀[u, v], −U')), and diagonal positive cycle check at line 8 (M₀*[i, i] > 0).
  </div>
  <p class="script-content">
    “Let us look at the formal pseudocode of Algorithm 2, which constructs the state-space matrices and computes the Kleene closure.
  </p>
  <p class="script-content">
    We initialize matrices <span class="math">A₀</span> to <span class="math">A_D</span> with <span class="math">−∞</span>, representing absence of constraints. In lines 2 to 3, forward lower-bound constraints populate the matrices with weight <span class="math">L'</span> at delay index <span class="math">δ</span>.
  </p>
  <p class="script-content">
    In lines 4 to 5, we encounter the key paper contribution: for each intra-iteration upper bound with delay <span class="math">δ = 0</span>, we insert a reverse edge from destination <span class="math">v</span> back to source <span class="math">u</span> in matrix <span class="math">A₀</span>, with weight <span class="math">−U'</span>.
  </p>
  <p class="script-content">
    In lines 6 to 7, we compute the Kleene star closure <span class="math">M₀*</span> through <span class="math">n−1</span> iterations of max-plus matrix multiplication, which is structurally equivalent to the Floyd-Warshall algorithm.
  </p>
  <p class="script-content">
    In line 8, we verify the fundamental feasibility invariant: if any diagonal entry <span class="math">M₀*[i, i] &gt; 0</span>, an intra-iteration contradictory cycle exists. The algorithm immediately halts and returns <code>INFEASIBLE_CYCLE</code>. This catches contradictions purely in matrix space, without unrolling a single iteration.”
  </p>
</div>

<!-- Page 7: Rahaman Part 2 (Slides 11 & 12 + Handoff) -->
<div class="page-break"></div>

<!-- Slide 11 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 11</span>
      <span class="slide-title">08 · ALGORITHMIC FORMULATION · Algorithm 3: ASAP Longest-Path Synthesis</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Algorithm 3 pseudocode, Bellman-Ford relaxation over |V_u|−1 iterations, and inter-iteration positive cycle detection check.
  </div>
  <p class="script-content">
    “Once the state-space matrices pass the Kleene check, Algorithm 3 synthesizes the exact earliest start times <span class="math">S*</span> over a finite horizon of <span class="math">K</span> iterations.
  </p>
  <p class="script-content">
    We construct the unrolled difference graph <span class="math">G_u</span>, containing <span class="math">K · |V|</span> task nodes. We initialize the distance array to <span class="math">−∞</span>, with iteration-zero release times set in line 2.
  </p>
  <p class="script-content">
    Lines 3 to 5 execute classic Bellman-Ford longest-path relaxation. For <span class="math">|V_u| − 1</span> rounds, every edge is relaxed using max-plus algebra:
    <br><center><span class="math">dist[v, k_v] = max(dist[v, k_v], dist[u, k_u] + W)</span></center>
  </p>
  <p class="script-content">
    In lines 6 to 7, we perform a final consistency pass. If any edge can still be relaxed, it mathematically proves that a positive-weight cycle spans across iterations—meaning the combination of execution times and upper bounds is physically impossible to satisfy.
  </p>
  <p class="script-content">
    Otherwise, the algorithm outputs the exact schedule <span class="math">S*[v, k] = dist[v, k]</span>. The computational complexity is <span class="math">O(K · |V| · (|E| + |CL| + |CU|))</span>, which is strictly polynomial in all input dimensions.”
  </p>
</div>

<!-- Slide 12 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 12</span>
      <span class="slide-title">09 · ILLUSTRATIVE WORKED EXAMPLE · Delaying on Purpose to Meet a Dwell Limit</span>
    </div>
    <span class="slide-timing">~50 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> 3-stage wafer timeline comparing Greedy ASAP (defect at 6.0 s) against Synthesized execution (intentional delay to t = 5.0 s, dwell = 4.0 s).
  </div>
  <p class="script-content">
    “To make this crystal clear, Slide 12 presents a step-by-step worked example adapted from semiconductor manufacturing.
  </p>
  <p class="script-content">
    We have three tasks: <span class="math">A</span> (Pre-Heat, duration 3s), <span class="math">B</span> (Transport, duration 2s), and <span class="math">C</span> (Chemical Deposition, duration 5s). The engineering constraint is that after Pre-Heat finishes, Deposition must begin within 4.0 seconds: <span class="math">s_C − c_A ≤ 4.0 s</span>. Crucially, downstream chamber <span class="math">C</span> is occupied by wafer <span class="math">k−1</span> until timestamp <span class="math">t = 12.0 s</span>.
  </p>
  <p class="script-content">
    Look at the top timeline: Greedy ASAP fires Pre-Heat as early as possible at <span class="math">t = 3.0 s</span>, completing at <span class="math">t = 6.0 s</span>. But Chamber <span class="math">C</span> is busy until <span class="math">t = 12.0 s</span>! The heated wafer sits idling for <span class="math">12 − 6 = 6.0 seconds</span>—violating the 4.0-second dwell limit and destroying the wafer!
  </p>
  <p class="script-content">
    Now observe the synthesized schedule below: our algorithm inverts the upper bound into a backward constraint:
    <br><center><span class="math">s_A ≥ s_C − 4 − w(A) = 12 − 4 − 3 = 5.0 s</span></center>
  </p>
  <p class="script-content">
    The synthesizer <em>deliberately delays</em> Pre-Heat to start at <span class="math">t = 5.0 s</span>. Pre-Heat completes at <span class="math">t = 8.0 s</span>, and when Chamber <span class="math">C</span> opens at <span class="math">t = 12.0 s</span>, the wafer has waited exactly <span class="math">12 − 8 = 4.0 seconds</span>—satisfying the upper bound with mathematical perfection!”
  </p>
  <div class="handoff-box">
    <strong>Verbal Handoff to Speaker 4:</strong> “I now hand over to Ampili Hemanth Kumar to walk us through the theoretical correctness proofs and our experimental evaluation.”
  </div>
</div>

<!-- ========================================================================= -->
<!-- SPEAKER 4: AMPILI HEMANTH KUMAR (PAGES 8 & 9) -->
<!-- ========================================================================= -->
<div class="page-break"></div>

<!-- Page 8: Hemanth Part 1 (Banner + Slides 13 & 14) -->
<div class="speaker-section-banner">
  <div class="speaker-meta-top">
    <span class="speaker-tag">Speaker 4 · Part 1</span>
    <span class="speaker-time-badge">Slides 13 to 16 · Target: ~2.5–3.0 Minutes</span>
  </div>
  <div class="speaker-name">Ampili Hemanth Kumar</div>
  <div class="speaker-role">Roll Number: 230128 · Dept. of Computer Science & Engineering, IIT Kanpur · Focus: Correctness Proofs, Test Oracle & Empirical Results</div>
</div>

<!-- Slide 13 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 13</span>
      <span class="slide-title">10 · THEORETICAL CORRECTNESS & PROOFS · Provably Correct, Complete and Optimal</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Four theoretical proof pillars: Soundness (zero false schedules), Completeness (exact feasibility verdict), Optimality (earliest starts), and Zero Throughput Degradation (0.0 s penalty).
  </div>
  <p class="script-content">
    “Thank you, Rahaman. I am Ampili Hemanth Kumar. I will present the formal correctness guarantees and our empirical evaluation.
  </p>
  <p class="script-content">
    The paper establishes four foundational theorems that we formally re-verified during our reproduction.
  </p>
  <p class="script-content">
    First is <em>Soundness</em>: every synthesized schedule <span class="math">S*</span> is guaranteed to satisfy all lower and upper bounds without exception. Bellman-Ford termination guarantees that <span class="math">dist[v] ≥ dist[u] + W</span> holds across every arc.
  </p>
  <p class="script-content">
    Second is <em>Completeness</em>: the algorithm is an exact decision procedure. If a feasible schedule exists, it will find it; if no schedule exists, it will extract an explicit positive cycle proving unsatisfiability. There are zero false negatives.
  </p>
  <p class="script-content">
    Third is <em>Componentwise Optimality</em>: for any other feasible schedule <span class="math">S'</span>, <span class="math">S* ≤ S'</span> holds for every task and iteration. This ensures the earliest completion and minimal makespan.
  </p>
  <p class="script-content">
    Fourth is the <em>Zero Throughput Degradation Theorem</em>: as long as upper bounds exceed the pipeline's critical cycle latency, inserting intentional delays absorbs non-critical slack without affecting the bottleneck resource. The total makespan penalty is exactly zero seconds.”
  </p>
</div>

<!-- Slide 14 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 14</span>
      <span class="slide-title">11 · EXPERIMENTAL METHODOLOGY · How We Tested It</span>
    </div>
    <span class="slide-timing">~40 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> 3 benchmark suites (Wafer Tool, DSP Streaming, Synthetic Scalability), 28-test verification badge, and 5 decoupled oracle checks with ε ≤ 10⁻⁹.
  </div>
  <p class="script-content">
    “To validate these theoretical claims, we constructed an exhaustive empirical testbed across three benchmark families.
  </p>
  <p class="script-content">
    Benchmark 1 is the industrial Semiconductor Wafer Tool, featuring a 5-chamber cluster line with dual thermal dwell limits of <span class="math">≤ 3.0 s</span> and <span class="math">≤ 2.0 s</span>. 
    Benchmark 2 is a 4-stage DSP video streaming pipeline subjected to tightness sweeps across varying jitter thresholds. 
    Benchmark 3 comprises synthetic pipeline topologies scaled up to 100 actors and 20 iterations—encompassing 1,000 task firings.
  </p>
  <p class="script-content">
    To ensure total scientific integrity, we built an <em>independent test oracle</em> that completely isolates itself from the max-plus solver. For every synthesized schedule, the oracle evaluates five ground-truth physical constraints: non-negativity, FIFO token precedence, lower bounds, upper bounds, and non-reentrancy, with floating-point residual tolerance <span class="math">ε ≤ 10⁻⁹</span>. All 28 automated tests pass with 100% compliance in 0.17 seconds.”
  </p>
</div>

<!-- Page 9: Hemanth Part 2 (Slides 15 & 16 + Handoff) -->
<div class="page-break"></div>

<!-- Slide 15 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 15</span>
      <span class="slide-title">12 · EXPERIMENT 1 · WAFER CLUSTER TOOL · Zero Dwell Violations, Zero Makespan Penalty</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Before-and-after comparison showing greedy dwell violations (4.0 s and 6.0 s) clamped to exactly 3.0 s, with identical 36.0 s makespan.
  </div>
  <p class="script-content">
    “Slide 15 shows our results on the industrial semiconductor wafer tool across <span class="math">K = 4</span> wafer lots.
  </p>
  <p class="script-content">
    Under greedy self-timed execution, wafer 2 suffered a transit dwell time of 4.0 seconds, and wafer 3 suffered 6.0 seconds—both severely violating the 3.0-second thermal threshold. In an actual semiconductor fab, both silicon wafers would be scrap.
  </p>
  <p class="script-content">
    When our synthesized schedule is deployed, the synthesizer detects the bottleneck at the Process Chamber (<span class="math">w = 6.0 s</span>) and intentionally delays the LoadLock and PreHeat operations of subsequent wafers.
  </p>
  <p class="script-content">
    As you can see, wafer 2 and wafer 3 dwell times are clamped precisely to 3.000 seconds—completely eliminating all fabrication defects!
  </p>
  <p class="script-content">
    And here is the remarkable result: the total makespan for both greedy and synthesized schedules is identical at exactly 36.0 seconds! By shifting tasks into available idle slack, we achieved 100% constraint satisfaction with zero makespan degradation.”
  </p>
</div>

<!-- Slide 16 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 16</span>
      <span class="slide-title">13 · EXPERIMENTS 2 & 3 · SCALABILITY · Polynomial Scaling: 1,000 Firings in 154 ms</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Runtime scaling curve (154 ms for 1,000 tasks vs >300s MILP timeout) and sharp phase transition cliff at tightness factor tf = 1.0.
  </div>
  <p class="script-content">
    “In Experiments 2 and 3, we evaluated scalability and constraint tightness limits.
  </p>
  <p class="script-content">
    On the left, we compare our max-plus synthesis algorithm against standard MILP and SMT formulations as task counts grow. While MILP solvers experience exponential explosion and time out past thirty actors, our algorithm scales strictly polynomially. For a massive topology of 100 actors across 10 iterations—totaling 1,000 task firings—our implementation synthesizes the complete schedule in just 154 milliseconds! This sub-second execution makes dynamic, online schedule reconfiguration entirely feasible on embedded controllers.
  </p>
  <p class="script-content">
    On the right, we examine the DSP pipeline across a tightness sweep from <span class="math">tf = 0.8</span> to <span class="math">2.0</span>. At <span class="math">tf = 1.0</span>, where the upper bound equals the critical cycle latency (<span class="math">T_crit = 12.0 s</span>), slack hits exactly zero. The moment <span class="math">tf &lt; 1.0</span>, an inter-iteration positive cycle forms, and our algorithm rejects the specification in just 0.02 milliseconds!”
  </p>
  <div class="handoff-box">
    <strong>Verbal Handoff to Speaker 5:</strong> “I now hand over to Koneti Karthik for our critical reflection, conclusions, and team overview.”
  </div>
</div>

<!-- ========================================================================= -->
<!-- SPEAKER 5: KONETI KARTHIK (PAGES 10 & 11) -->
<!-- ========================================================================= -->
<div class="page-break"></div>

<!-- Page 10: Karthik Part 1 (Banner + Slides 17 & 18) -->
<div class="speaker-section-banner">
  <div class="speaker-meta-top">
    <span class="speaker-tag">Speaker 5 · Part 1</span>
    <span class="speaker-time-badge">Slides 17 to 20 · Target: ~2.5–3.0 Minutes</span>
  </div>
  <div class="speaker-name">Koneti Karthik</div>
  <div class="speaker-role">Roll Number: 230568 · Dept. of Computer Science & Engineering, IIT Kanpur · Focus: Critical Reflection, Key Findings & Open-Source Artifacts</div>
</div>

<!-- Slide 17 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 17</span>
      <span class="slide-title">14 · CRITICAL REFLECTION & THREATS TO VALIDITY · Honest Limits: Theirs and Ours</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Side-by-side comparison between Author-Acknowledged Limitations (deterministic execution, static dataflow, unrolling) and Our Reproduction Findings (memory scaling, no public code, sub-millisecond RTOS jitter).
  </div>
  <p class="script-content">
    “Thank you, Hemanth. I am Koneti Karthik. I will conclude our talk with an honest critical appraisal, key conclusions, and our team contributions.
  </p>
  <p class="script-content">
    In Slide 17, we distinguish between limitations acknowledged by the authors and additional practical challenges we discovered during our reproduction.
  </p>
  <p class="script-content">
    The authors openly acknowledge that their framework assumes deterministic task durations <span class="math">w(v)</span>. In real cyber-physical systems, cache misses, bus contention, or memory stalls can introduce execution jitter that may violate tight bounds at runtime. Furthermore, the model is restricted to static dataflow; variable-rate systems like Cyclo-Static or Scenario-Aware SDF require worst-case expansions.
  </p>
  <p class="script-content">
    From our engineering perspective, we identified three vital threats:
    First, while synthesis time is <span class="math">O(K · E)</span>, graph memory scales with <span class="math">K · |V|</span>; horizons beyond 1,000 iterations require sparse matrix data structures. 
    Second, the authors provided no public reference implementation; our team reconstructed the entire mathematics from the formal text. 
    Third, enforcing zero-slack schedules requires microsecond-accurate OS dispatching, mandating a hard Real-Time Operating System.”
  </p>
</div>

<!-- Slide 18 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 18</span>
      <span class="slide-title">15 · CONCLUSIONS & KEY TAKEAWAYS · Four Findings from the Reproduction</span>
    </div>
    <span class="slide-timing">~45 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Four conclusion pillars: Algebraic Unification, Defects Gone with No Penalty, Sub-Second Tractability, and Full Reproduction Fidelity.
  </div>
  <p class="script-content">
    “To summarize our findings, this reproduction delivers four foundational takeaways.
  </p>
  <p class="script-content">
    First, <em>Algebraic Unification</em>: upper timing bounds are not non-linear roadblocks requiring exponential search. In difference-constraint space, they are simply backward directed arcs with negative weights, fully solvable with linear algebra.
  </p>
  <p class="script-content">
    Second, <em>Zero Makespan Penalty</em>: on the semiconductor wafer tool, critical dwell violations were reduced from 6.0 seconds down to the 3.0-second limit, eliminating thermal defects while preserving the optimal 36.0-second makespan.
  </p>
  <p class="script-content">
    Third, <em>Sub-Second Tractability</em>: by replacing exponential solvers with Bellman-Ford propagation, 1,000 task firings synthesize in 154 milliseconds, proving the feasibility of embedded online re-scheduling.
  </p>
  <p class="script-content">
    Fourth, <em>Complete Reproduction Fidelity</em>: our Python implementation, accompanied by 28 automated test cases, reproduces the paper's claims with numerical precision <span class="math">ε ≤ 10⁻⁹</span>.”
  </p>
</div>

<!-- Page 11: Karthik Part 2 (Slides 19 & 20 + Concluding Q&A) -->
<div class="page-break"></div>

<!-- Slide 19 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 19</span>
      <span class="slide-title">16 · BIBLIOGRAPHY · References</span>
    </div>
    <span class="slide-timing">~30 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Primary EMSOFT 2025 Paper, Foundational Dataflow Literature (Lee & Messerschmitt 1987, Bhattacharyya et al. 1996), and Max-Plus Semiring Literature (Baccelli et al. 1992, Karp 1978, Cuninghame-Green 1979).
  </div>
  <p class="script-content">
    “Slide 19 lists our primary bibliography.
  </p>
  <p class="script-content">
    In addition to the primary paper by van Wanrooij, Basten, and Geilen in ACM TECS 2025, our mathematical implementation rests on foundational dataflow theory by Edward Lee and David Messerschmitt, as well as the definitive max-plus linear system treatises by Baccelli, Cohen, Olsder, and Quadrat, along with Richard Karp's minimum cycle-mean characterization.
  </p>
  <p class="script-content">
    Every equation, matrix transformation, and cycle ratio calculation in our codebase was cross-referenced and verified against these foundational texts.”
  </p>
</div>

<!-- Slide 20 -->
<div class="slide-block">
  <div class="slide-header">
    <div class="slide-title-wrap">
      <span class="slide-badge">SLIDE 20</span>
      <span class="slide-title">17 · TEAM ALLOCATION & Q&A · Team Contributions, Deliverables and Questions</span>
    </div>
    <span class="slide-timing">~40 seconds</span>
  </div>
  <div class="visual-cue-box">
    <strong>Visual Focus:</strong> Five team member cards showing equal 20% distribution in order (Prem, Badri, Rahaman, Hemanth, Karthik), verified test suite (28/28 tests), and open Q&A invitation.
  </div>
  <p class="script-content">
    “Finally, Slide 20 highlights our team allocation and open-source project deliverables.
  </p>
  <p class="script-content">
    Following the speaking order of today's presentation, our team divided the engineering workload into five equal twenty percent components:
    Vempati Prem Santhosh built the independent test oracle and the 28-case automated verification suite. 
    Sanga Badri developed the Extended HSDF model, balance equations, and actor serialization. 
    Our project lead, Sk J Ur Rahaman, engineered the max-plus matrix engine, state-space construction, and Kleene star closure. 
    Ampili Hemanth Kumar implemented the Bellman-Ford synthesis algorithm and cycle conflict extractor. 
    And I, Koneti Karthik, engineered the benchmark suites, parameter sweeps, and presentation assets.
  </p>
  <p class="script-content">
    Our full codebase, along with documentation and reproduction scripts, is verified and committed to our repository.
  </p>
  <p class="script-content">
    On behalf of our entire team from IIT Kanpur, thank you for your attention. We are delighted to answer any questions on max-plus linearization, synthesis algorithms, or our experimental results.”
  </p>
</div>

</body>
</html>
"""

def generate_pdf():
    html_path = os.path.abspath("presentation/speaker_scripts.html")
    raw_pdf_path = os.path.abspath("presentation/temp_raw.pdf")
    final_pdf_path = os.path.abspath("CS637_Presentation_Speaker_Scripts.pdf")

    # 1. Write HTML
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    print(f"Wrote HTML to {html_path}")

    # 2. Find browser
    browser_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    browser = None
    for b in browser_candidates:
        if os.path.exists(b):
            browser = b
            break

    if not browser:
        raise RuntimeError("No headless browser found.")

    print(f"Rendering HTML to PDF with: {browser}")
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={raw_pdf_path}",
        html_path
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Browser PDF failed: {res.stderr}")

    # 3. Post-process with PyMuPDF: add headers, footers, rules, and PDF bookmarks
    doc = fitz.open(raw_pdf_path)
    total_pages = len(doc)
    print(f"Raw rendered PDF pages: {total_pages}")

    # Stamping running header & footer
    for idx, page in enumerate(doc):
        if idx == 0:
            continue  # Leave Cover page clean
        rect = page.rect
        # Running top header
        page.insert_text(fitz.Point(39, 22), "CS637: EMBEDDED SYSTEMS — PRESENTATION SPEECH SCRIPTS", fontsize=7.5, color=(0.4, 0.45, 0.52))
        page.insert_text(fitz.Point(rect.width - 135, 22), "IIT KANPUR · CSE DEPT", fontsize=7.5, color=(0.4, 0.45, 0.52))
        page.draw_line(fitz.Point(39, 26), fitz.Point(rect.width - 39, 26), color=(0.82, 0.86, 0.9), width=0.6)

        # Running bottom footer
        page.insert_text(fitz.Point(39, rect.height - 18), "Schedule Synthesis for Synchronous Dataflow (EMSOFT 2025 / ACM TECS)", fontsize=7.2, color=(0.45, 0.5, 0.58))
        page.insert_text(fitz.Point(rect.width - 92, rect.height - 18), f"Page {idx + 1} of {total_pages}", fontsize=7.5, color=(0.3, 0.35, 0.45))
        page.draw_line(fitz.Point(39, rect.height - 24), fitz.Point(rect.width - 39, rect.height - 24), color=(0.82, 0.86, 0.9), width=0.6)

    # Build Table of Contents / Bookmarks Tree
    # Determine slide positions
    slide_pages = {}
    for i, page in enumerate(doc, 1):
        txt = page.get_text()
        for s in range(1, 21):
            if f"SLIDE {s}" in txt and s not in slide_pages:
                slide_pages[s] = i

    toc = [
        [1, "Cover & Executive Roster Table", 1],
        [1, "Speaker 1: Vempati Prem Santhosh (Slides 1–4)", 2],
        [2, "Slide 1: Title & Presentation Introduction", slide_pages.get(1, 2)],
        [2, "Slide 2: Overview & Presentation Roadmap", slide_pages.get(2, 2)],
        [2, "Slide 3: Practical Motivation (Wafer Dwell Limit)", slide_pages.get(3, 3)],
        [2, "Slide 4: Research Gap & Algorithmic Paradigms", slide_pages.get(4, 3)],
        [1, "Speaker 2: Sanga Badri (Slides 5–8)", 4],
        [2, "Slide 5: Formal Dataflow Semantics (SDF & HSDF)", slide_pages.get(5, 4)],
        [2, "Slide 6: Timing Bounds Semantics (Backward Arcs)", slide_pages.get(6, 4)],
        [2, "Slide 7: Mathematical Optimization Objectives", slide_pages.get(7, 5)],
        [2, "Slide 8: Core Theoretical Insight (Max-Plus Algebra)", slide_pages.get(8, 5)],
        [1, "Speaker 3: Sk J Ur Rahaman (Slides 9–12)", 6],
        [2, "Slide 9: Methodological Pipeline (4 Stages)", slide_pages.get(9, 6)],
        [2, "Slide 10: Algorithm 2 (Kleene-Star State-Space Closure)", slide_pages.get(10, 6)],
        [2, "Slide 11: Algorithm 3 (Bellman-Ford ASAP Synthesis)", slide_pages.get(11, 7)],
        [2, "Slide 12: Illustrative Worked Example (Wafer Walkthrough)", slide_pages.get(12, 7)],
        [1, "Speaker 4: Ampili Hemanth Kumar (Slides 13–16)", 8],
        [2, "Slide 13: Theoretical Correctness & Proof Guarantees", slide_pages.get(13, 8)],
        [2, "Slide 14: Experimental Methodology & Independent Oracle", slide_pages.get(14, 8)],
        [2, "Slide 15: Experiment 1 — Wafer Cluster Tool Results", slide_pages.get(15, 9)],
        [2, "Slide 16: Experiments 2 & 3 — Scalability & Phase Transitions", slide_pages.get(16, 9)],
        [1, "Speaker 5: Koneti Karthik (Slides 17–20)", 10],
        [2, "Slide 17: Critical Reflection & Threats to Validity", slide_pages.get(17, 10)],
        [2, "Slide 18: Conclusions & Four Key Takeaways", slide_pages.get(18, 10)],
        [2, "Slide 19: Bibliography & Formal References", slide_pages.get(19, 11)],
        [2, "Slide 20: Team Allocation, Deliverables & Open Q&A", slide_pages.get(20, 11)],
    ]

    doc.set_toc(toc)
    doc.save(final_pdf_path)
    doc.close()

    # Remove temporary raw PDF
    if os.path.exists(raw_pdf_path):
        os.remove(raw_pdf_path)

    print(f"Saved final bookmarked and styled PDF at {final_pdf_path} (Size: {os.path.getsize(final_pdf_path)} bytes)")

    # Copy to presentation/ and docs/
    shutil.copy(final_pdf_path, "presentation/CS637_Presentation_Speaker_Scripts.pdf")
    shutil.copy(final_pdf_path, "docs/CS637_Presentation_Speaker_Scripts.pdf")
    print("Copied final PDF to presentation/ and docs/ folders.")

if __name__ == "__main__":
    generate_pdf()
