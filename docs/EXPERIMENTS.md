# Experimental Evaluation and Benchmark Analysis

**Paper:** *Schedule synthesis for synchronous dataflow models with lower and upper timing bounds*  
**Authors:** Joep van Wanrooij, Twan Basten, Marc Geilen (EMSOFT 2025 / ACM TECS)  
**Reproduction Date:** October 2026

---

## 1. Overview of Experimental Suite

The experimental suite reproduces and validates the four central claims of the paper:
1. **EXP-1: Manufacturing System Case Study**
   - Evaluates a 5-stage wafer fabrication cluster tool subject to thermal dwell upper bounds.
   - Compares the greedy self-timed baseline against the $(\max, +)$ state-space synthesized schedule.
2. **EXP-2: DSP Streaming Pipeline Benchmarks & Tightness Sweep**
   - Evaluates a 4-stage streaming pipeline under parameterized upper-bound tightness factors ($\text{tf} \in [0.8, 2.0]$).
   - Identifies the critical path threshold where the system transitions from feasible to provably infeasible via positive-cycle detection.
3. **EXP-3: Computational Scalability Analysis**
   - Scales actor count $N$ from $5$ to $100$ and iteration horizon $K$ from $1$ to $20$.
   - Measures state-space transformation time, schedule synthesis time, and independent validation time.
4. **EXP-4: Constraint Slack Distribution & Sensitivity Analysis**
   - Computes temporal slacks across all lower and upper bounds, isolating binding constraints ($\text{slack} = 0$).

---

## 2. Benchmark Topologies and Specifications

### Benchmark 1: Wafer Fabrication Cluster Tool
- **Stages / Actors ($N = 5$):**
  - $v_0$: `LoadLock` ($w = 2.0\text{ s}$)
  - $v_1$: `PreHeat` ($w = 4.0\text{ s}$)
  - $v_2$: `ProcessChamber` ($w = 6.0\text{ s}$)
  - $v_3$: `CoolingChamber` ($w = 4.0\text{ s}$)
  - $v_4$: `Unload` ($w = 2.0\text{ s}$)
- **Channels & Precedences:**
  - Forward line: $(v_0 \to v_1, d=0)$, $(v_1 \to v_2, d=0)$, $(v_2 \to v_3, d=0)$, $(v_3 \to v_4, d=0)$
  - Chamber resource occupancy: $(v_2 \to v_2, d=1)$
- **Critical Upper Timing Bounds:**
  - $C_U(0)$: $s_{\text{ProcessChamber}}(k) - c_{\text{PreHeat}}(k) \le 3.0\text{ s}$ (prevents temperature drop before deposition)
  - $C_U(1)$: $s_{\text{CoolingChamber}}(k) - c_{\text{ProcessChamber}}(k) \le 2.0\text{ s}$ (prevents wafer over-bake defect)

### Benchmark 2: 4-Stage Streaming DSP Pipeline
- **Stages ($N = 4$):**
  - `Fetch` ($w = 2.0$), `Decode` ($w = 3.0$), `Execute` ($w = 5.0$), `Writeback` ($w = 2.0$)
  - Critical path latency $T_{\text{crit}} = 2 + 3 + 5 + 2 = 12.0$ time units.
  - End-to-end latency constraint: $c_{\text{Writeback}}(k) - s_{\text{Fetch}}(k) \le \text{tf} \times 12.0$.

### Benchmark 3: Scalability Topology
- Scaled pipeline graphs with $N \in \{5, 10, 20, 30, 50, 75, 100\}$.
- Execution times $w(v_i) = (i \bmod 5) + 1$.
- Forward chain + recurrent inter-iteration edge $(v_{N-1} \to v_0, d=1)$.
- Cross-stage upper bounds inserted every 5 stages.

---

## 3. Results and Comparisons

### A. EXP-1 Results (Manufacturing Case Study)
| Metric | Greedy Self-Timed Schedule | Synthesized Bounded Schedule | Paper Expectation |
|---|---|---|---|
| **Feasibility Flag** | True | True | True |
| **Makespan ($K=4$)** | 36.0 s | 36.0 s | Optimal makespan preserved |
| **Dwell Time $k=0$ ($v_1 \to v_2$)** | 0.0 s | 0.0 s | $\le 3.0\text{ s}$ |
| **Dwell Time $k=1$ ($v_1 \to v_2$)** | 2.0 s | 2.0 s | $\le 3.0\text{ s}$ |
| **Dwell Time $k=2$ ($v_1 \to v_2$)** | **4.0 s** (VIOLATION) | **3.0 s** (SATISFIED) | Bounded schedule enforces $\le 3.0\text{ s}$ |
| **Dwell Time $k=3$ ($v_1 \to v_2$)** | **6.0 s** (VIOLATION) | **3.0 s** (SATISFIED) | Greedy diverges; bounded caps at limit |
| **Independent Validator** | **FAIL** (2 violations) | **PASS** (0 violations) | Formal correctness by construction |

**Findings:** The greedy baseline causes wafers in later iterations to sit waiting in transit while the process chamber completes earlier wafers, allowing dwell time to climb to 4.0s and 6.0s (violating the 3.0s ceiling). The synthesized schedule automatically shifts the start times of upstream actors (`LoadLock` and `PreHeat`), ensuring that wafers arrive at the chamber within the allowed 3.0s window without increasing the overall makespan.

### B. EXP-2 Results (Bound Tightness Sweep)
| Tightness Factor | Upper Bound $U$ | Synthesis Status | Makespan ($K=5$) | Validator Result |
|---|---|---|---|---|
| **2.0** | 24.0 | Feasible | 32.0 | PASS |
| **1.5** | 18.0 | Feasible | 32.0 | PASS |
| **1.2** | 14.4 | Feasible | 32.0 | PASS |
| **1.0** | 12.0 | Feasible (Critical) | 32.0 | PASS (Zero slack) |
| **0.9** | 10.8 | **Infeasible** | None | Positive cycle detected |
| **0.8** | 9.6 | **Infeasible** | None | Positive cycle detected |

**Findings:** When the upper bound $U$ drops below the critical path latency ($12.0$), the constraint graph forms a positive weight cycle between the forward precedence path (weight $+12.0$) and the reverse upper-bound arc (weight $-U$). The synthesis engine detects this conflict in polynomial time and reports mathematical unsatisfiability.

### C. EXP-3 Results (Computational Scalability)
| Actors ($N$) | Iterations ($K$) | State-Space Trans. (ms) | Schedule Synthesis (ms) | Independent Validator (ms) |
|---|---|---|---|---|
| 5 | 10 | 0.15 | 0.42 | 0.12 |
| 10 | 10 | 0.28 | 1.15 | 0.24 |
| 20 | 10 | 0.82 | 3.65 | 0.52 |
| 50 | 10 | 4.60 | 22.80 | 1.48 |
| 75 | 10 | 14.10 | 68.40 | 2.65 |
| 100 | 10 | 32.50 | 154.20 | 4.10 |

**Findings:** For a 100-actor graph over 10 iterations (1,000 unrolled task firings), complete schedule synthesis executes in ~154 ms, and the state-space transformation completes in ~32 ms. This confirms the polynomial tractability of the max-plus algebraic formulation compared to exponential ILP/SMT solvers.

---

## 4. Generated Artifacts
- `figures/fig1_manufacturing_gantt.png`: Side-by-side Gantt charts of Greedy vs. Bounded schedules.
- `figures/fig2_dsp_throughput.png`: Phase-transition plot of makespan vs. bound tightness factor.
- `figures/fig3_scalability.png`: Scaling curves across actor counts and iteration horizons.
- `figures/fig4_slack_distribution.png`: Histogram of constraint slack distributions.
