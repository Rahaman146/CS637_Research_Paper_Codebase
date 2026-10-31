# CS637: Embedded Systems — Presentation Speech Scripts
## Schedule Synthesis for Synchronous Dataflow Models with Lower and Upper Timing Bounds
### Research Paper Evaluation & Reproduction
**Assigned Paper:** *Schedule synthesis for synchronous dataflow models with lower and upper timing bounds*  
**Authors:** Joep van Wanrooij, Twan Basten, Marc Geilen (TU Eindhoven) — EMSOFT 2025 / ACM TECS (DOI: [10.1145/3762643](https://doi.org/10.1145/3762643))  
**Presentation Deck:** `CS637_Presentation_Final.pptx` (20 slides, 16:9 widescreen)  
**Total Target Duration:** 12 to 14 minutes (~35–45 seconds per slide)  
**Speaking Order:** **Prem → Badri → Rahaman → Hemanth → Karthik** (Equal 20% / 4 slides each)

---

## Team Allocation & Slide Mapping

| Speaker # | Member Name | Roll Number | Department | Slides | Section Focus & Key Contributions | Target Time |
|:---:|:---|:---:|:---:|:---:|:---|:---:|
| **1** | **Vempati Prem Santhosh** | 231137 | CSE | **Slides 1–4** | Welcome & Introduction, Roadmap, Industrial Motivation, Research Gap & Algorithmic Paradigms | ~2.5–3.0 min |
| **2** | **Sanga Badri** | 230911 | CSE | **Slides 5–8** | SDF/HSDF Semantics, Timing Bounds Inversion, Optimization Objectives, Max-Plus Algebra | ~2.5–3.0 min |
| **3** | **Sk J Ur Rahaman** *(Project Lead)* | 230951 | CSE | **Slides 9–12** | Methodological Pipeline, Algorithm 2 Kleene Star, Algorithm 3 Bellman-Ford, Worked Example | ~2.5–3.0 min |
| **4** | **Ampili Hemanth Kumar** | 230128 | CSE | **Slides 13–16** | Correctness Guarantees, Experimental Methodology, Exp 1 Wafer Tool, Exp 2 & 3 Scalability | ~2.5–3.0 min |
| **5** | **Koneti Karthik** | 230568 | CSE | **Slides 17–20** | Critical Reflection & Threats, Key Conclusions, Bibliography, Team Allocation & Q&A | ~2.5–3.0 min |

---

## Pronunciation & Terminology Guide
- **Joep van Wanrooij:** *“Yoop van WAN-roy”*
- **Twan Basten & Marc Geilen:** *“Twan BAHS-ten and Marc GUY-len”*
- **Kleene Star:** *“CLAY-nee star”* ($M_0^*$)
- **Max-Plus Semiring:** $(\mathbb{R}_{\max}, \oplus, \otimes)$ where $\oplus$ is $\max(a, b)$ and $\otimes$ is conventional addition $a + b$
- **$\lambda^*$:** *“Lambda star”* (maximum cycle ratio / minimum sustainable period)
- **HSDFG:** *“Homogeneous Synchronous Dataflow Graph”*
- **Dwell Time:** The maximum allowable idle latency between consecutive physical operations (e.g., thermal residency $\le 3.0\text{ s}$)
- **Bellman-Ford:** *“BELL-man FORD”*

---

# Detailed Slide-by-Slide Speech Scripts

```
========================================================================================
SPEAKER 1: Vempati Prem Santhosh (Roll: 231137)
SLIDES: 1 to 4  |  TARGET TIME: ~2.5 to 3.0 Minutes
========================================================================================
```

### Slide 1: Title & Presentation Introduction
- **Visual Callout:** Title, authors, TU Eindhoven affiliation, EMSOFT 2025 citation, team roster at bottom, and the $\le 3.0\text{ s}$ dwell window badge.
- **Target Time:** 40 seconds

> **[Spoken Script]**
> "Good morning, respected instructor and colleagues. Welcome to our CS637 Embedded Systems research project presentation. 
> 
> Today, our team presents our complete evaluation and codebase reproduction of the EMSOFT 2025 research paper titled: *'Schedule synthesis for synchronous dataflow models with lower and upper timing bounds'*, authored by Joep van Wanrooij, Twan Basten, and Marc Geilen from Eindhoven University of Technology, published in ACM Transactions on Embedded Computing Systems.
> 
> Our team from the Department of Computer Science and Engineering at IIT Kanpur comprises five members: myself, Vempati Prem Santhosh, alongside Sanga Badri, our project lead Sk J Ur Rahaman, Ampili Hemanth Kumar, and Koneti Karthik. Each of us has contributed an equal twenty percent to this reproduction effort. 
> 
> In this talk, we will demonstrate how analytical max-plus state-space algebra enables polynomial-time schedule synthesis for embedded dataflow systems with rigid upper timing bounds, validated on industrial semiconductor wafer cluster tools."

---

### Slide 2: Overview & Presentation Roadmap
- **Visual Callout:** The 6-chapter sequence cards (The Problem, The Model, The Idea, The Algorithms, The Evidence, The Verdict).
- **Target Time:** 35 seconds

> **[Spoken Script]**
> "Here is our roadmap for today's talk, structured into six sequential chapters. 
> 
> First, in *The Problem*, we uncover why classical dataflow scheduling fails when upper timing bounds are introduced. 
> Second, in *The Model*, we formalize Synchronous Dataflow semantics and show how upper bounds are inverted into difference constraints. 
> Third, in *The Idea*, we reveal the core theoretical breakthrough: linearizing timing constraints into a max-plus semiring. 
> Fourth, in *The Algorithms*, we walk through the polynomial-time Kleene closure and Bellman-Ford synthesis algorithms with an illustrative worked example. 
> Fifth, in *The Evidence*, we present our formal correctness proofs, benchmark methodology, wafer cluster tool results, and scalability stress-tests. 
> Finally, in *The Verdict*, we provide our critical reflection, engineering conclusions, and open the floor for your questions."

---

### Slide 3: Practical Motivation — When Firing Early Becomes a Defect
- **Visual Callout:** The wafer fabrication thermal diagram, the $\le 3.0\text{ s}$ critical dwell limit, and the red comparison showing greedy execution causing a catastrophic 6.0-second delay.
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "Let us examine the practical motivation. In embedded real-time systems, Synchronous Dataflow—or SDF—is the gold standard for modeling concurrent streaming pipelines. Standard SDF assumes *self-timed execution*: actors fire greedily as soon as input tokens arrive. This naturally guarantees maximal throughput when only *lower* bounds exist—meaning an operation cannot start before its inputs are ready.
> 
> However, modern cyber-physical and manufacturing systems impose strict *upper* timing bounds. Consider semiconductor fabrication: a silicon wafer undergoes chemical vapor deposition in a high-temperature chamber. Once pre-heated, the wafer cannot dwell in transit for more than 3.0 seconds, or thermal decay ruins the wafer surface. Similarly, in hard real-time multimedia, video frames must traverse processing stages within bounded jitter windows to avoid buffer overflows.
> 
> This exposes the *Self-Timed Scheduling Paradox*: greedy execution fires tasks as early as possible. But if a downstream chamber is occupied, the upstream product is forced to wait in an unheated buffer. In a wafer tool, greedy execution forces a 6.0-second wait—a 100% defective wafer! Firing *early* is literally what causes the defect. We need schedule synthesis that guarantees correctness by construction."

---

### Slide 4: Research Gap & Algorithmic Paradigms
- **Visual Callout:** Comparison table between Heuristic Throttling, MILP/SMT Solvers, Timed Automata, and the Proposed (max, +) State-Space approach.
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "Why do existing scheduling paradigms fall short? 
> 
> Designers historically faced an unacceptable compromise. On one hand, runtime heuristics and artificial delay insertion lack formal guarantees and fail under tight multi-stage dependencies. On the other hand, exact formal methods like Mixed-Integer Linear Programming or SMT solvers exhibit exponential worst-case complexity—timing out beyond thirty actors. Meanwhile, model-checking with Timed Automata suffers from severe state-space explosion due to dense continuous clock regions.
> 
> The central research gap is: *How can we enforce rigid bidirectional timing bounds on dataflow graphs while preserving polynomial-time scalability and analytical closed-form rigor?*
> 
> The paper's breakthrough is to recognize that upper bounds can be re-cast as backward difference constraints, embedded into max-plus linear state-space matrices, and solved via Kleene closure and longest-path propagation.
> 
> I will now pass the floor to Sanga Badri to walk us through the formal dataflow semantics and the timing bounds transformation."

---

```
========================================================================================
SPEAKER 2: Sanga Badri (Roll: 230911)
SLIDES: 5 to 8  |  TARGET TIME: ~2.5 to 3.0 Minutes
========================================================================================
```

### Slide 5: Formal Dataflow Semantics (SDF & HSDF)
- **Visual Callout:** Production/consumption rate diagram ($u \xrightarrow{2, 3} v$), repetition vector $q = [3, 2]^T$, nullspace equation $\Gamma \cdot q = 0$, and non-reentrancy self-loops.
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "Thank you, Prem. I am Sanga Badri, and I will explain the formal dataflow foundations.
> 
> A Synchronous Dataflow graph $G = (V, E, \text{prd}, \text{cns}, d, w)$ consists of computational actors $V$, connected by FIFO channels $E$. Every time an actor $u$ fires, it produces a fixed number of tokens $\text{prd}(e)$, and the consuming actor $v$ consumes $\text{cns}(e)$ tokens.
> 
> For an SDF graph to execute indefinitely with bounded buffer memory, it must be consistent. This is captured by the fundamental balance equation: $\Gamma \cdot q = 0$, where $\Gamma$ is the topology matrix and $q$ is the non-trivial repetition vector. For instance, if actor $u$ produces 2 tokens and actor $v$ consumes 3 tokens, consistency requires that $u$ fires 3 times for every 2 firings of $v$, ensuring zero net token drift.
> 
> To enable analytical timing analysis, we expand the multi-rate SDF graph into an equivalent Homogeneous SDF—or HSDF—graph in $O(|V| + |E|)$ time, where each actor $u$ is instantiated into $q(u)$ single-rate sub-actors. To prevent a physical actor from firing concurrently with itself on multi-core hardware, we inject non-reentrancy serialization edges with zero delay between successive sub-instances, and a unit-delay loopback edge from the last sub-instance to the first."

---

### Slide 6: Timing Bounds Semantics — Upper Bounds as Backward Arcs
- **Visual Callout:** The algebraic derivation showing how $s_{\text{dst}}(k) - s_{\text{src}}(k-\delta) \le U'$ inverts to $s_{\text{src}}(k-\delta) - s_{\text{dst}}(k) \ge -U'$, and the three event-type normalization rules.
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "Now, let us examine the paper's key algebraic insight on timing bounds.
> 
> In an HSDF graph, timing constraints are defined between event timestamps: actor start times $s_v(k)$ and completion times $c_v(k) = s_v(k) + w(v)$. A conventional precedence edge enforces a lower bound: $s_{\text{dst}}(k) - s_{\text{src}}(k-\delta) \ge L'$.
> 
> But an upper timing bound states that the destination cannot start later than $U'$ time units after the source: $s_{\text{dst}}(k) - s_{\text{src}}(k-\delta) \le U'$.
> 
> The crucial mathematical move is multiplying this inequality by negative one:
> $$s_{\text{src}}(k-\delta) - s_{\text{dst}}(k) \ge -U'$$
> 
> This simple inversion reveals that an upper bound from source to destination is mathematically identical to a *backward lower-bound constraint* from destination to source, carrying an iteration delay of $-\delta$ and a negative weight of $-U'$.
> 
> Furthermore, all combinations of start and completion events normalize cleanly to start-to-start constraints by shifting execution weights: for completion-to-start, $L' = L + w(u)$; for completion-to-completion, $L' = L + w(u) - w(v)$. All timing requirements collapse into one single canonical form: $s_{\text{target}} - s_{\text{source}} \ge W$."

---

### Slide 7: Mathematical Optimization Objectives
- **Visual Callout:** The two objective panels: Objective 1 (Finite-horizon makespan minimization) and Objective 2 (1-periodic throughput maximization via Karp's cycle mean $\lambda^*$).
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "With all constraints unified into difference inequalities, we can formally state our two mathematical optimization objectives.
> 
> Objective 1 is *Finite-Horizon Makespan Minimization*. Given a finite batch of $K$ iterations—such as processing a lot of silicon wafers—we seek schedule vectors $S^*$ that minimize the completion time of the latest actor: $\min_S \max_v (s_v(K-1) + w(v))$, subject to our difference constraints, non-negativity, and non-reentrancy. Because all constraints are difference constraints, the earliest valid start times form the unique componentwise minimum, computed via longest-path propagation on the unrolled DAG.
> 
> Objective 2 is *1-Periodic Throughput Maximization* for infinite streaming runs. Here, execution repeats with a constant period $\lambda$, such that $s_v(k) = s_v(0) + k \cdot \lambda$. The maximum throughput $\Theta = 1/\lambda^*$ is dictated by the maximum cycle ratio over all directed cycles with positive delays: $\lambda^* = \max_\gamma W(\gamma) / D(\gamma)$. 
> 
> Crucially, our backward upper-bound edges introduce cycles with *negative* token delays $D(\gamma) < 0$. These invert the inequality and impose an *upper bound* on the period: $\lambda^* \le W(\gamma)/D(\gamma)$. If the lower throughput bound exceeds the upper bound, the periodic schedule is provably unsatisfiable."

---

### Slide 8: Core Theoretical Insight — Max-Plus Semiring Linearization
- **Visual Callout:** The max-plus semiring $(\mathbb{R}_{\max}, \oplus, \otimes)$, state equation $x(k) = A_0 \otimes x(k) \oplus A_1 \otimes x(k-1)$, and the Kleene star polynomial series $M_0^* = \bigoplus_{p=0}^{n-1} M_0^p$.
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "This brings us to the theoretical heart of the paper: max-plus semiring linearization.
> 
> In classical algebra, synchronization and scheduling constraints appear non-linear because of the $\max$ operator. However, in the max-plus semiring $(\mathbb{R} \cup \{-\infty\}, \oplus, \otimes)$, we define addition as $\max(a, b)$ and multiplication as conventional addition $a + b$. Under this algebra, complex dataflow synchronization transforms into linear matrix-vector recurrence:
> $$x(k) = A_0 \otimes x(k) \oplus A_1 \otimes x(k-1) \oplus \dots \oplus A_D \otimes x(k-D)$$
> 
> Here, $A_0$ captures instantaneous, intra-iteration dependencies—including our backward upper-bound arcs. Because $x(k)$ appears on both sides of the equation, we resolve the implicit algebraic loop using the *Kleene star closure*:
> $$M_0^* = I \oplus M_0 \oplus M_0^2 \oplus \dots \oplus M_0^{n-1}$$
> 
> In max-plus algebra, the Kleene star computes all-pairs longest paths in $O(n^3)$ time without unrolling. If any diagonal entry $(M_0^*)_{ii} > 0$, it proves that an intra-iteration contradictory cycle exists, immediately catching infeasibility.
> 
> I will now pass the floor to our project lead, Sk J Ur Rahaman, to walk us through the methodological pipeline, algorithmic formulations, and our worked example."

---

```
========================================================================================
SPEAKER 3: Sk J Ur Rahaman (Roll: 230951 — Project Lead)
SLIDES: 9 to 12  |  TARGET TIME: ~2.5 to 3.0 Minutes
========================================================================================
```

### Slide 9: Methodological Pipeline — Specification to Verified Schedule
- **Visual Callout:** The 4-stage pipeline horizontal flow: Stage 1 (Normalization), Stage 2 (State-Space Construction), Stage 3 (Kleene Closure), and Stage 4 (Synthesis & Oracle Validation).
- **Target Time:** 40 seconds

> **[Spoken Script]**
> "Thank you, Badri. I am Sk J Ur Rahaman. I will explain the end-to-end synthesis pipeline and our algorithmic implementation.
> 
> The methodological architecture consists of four distinct stages.
> 
> In Stage 1, *Normalization*, we parse the Extended HSDF graph and convert all arbitrary start and completion bounds into canonical difference constraints $s_j(k) - s_i(k-\delta) \ge W$.
> 
> In Stage 2, *State-Space Construction*, we build the max-plus transition matrices $A_0$ through $A_D$. We embed backward upper bounds into $A_0$ and enforce sequential actor execution by setting $(A_1)_{vv} \ge w(v)$.
> 
> In Stage 3, *Kleene Closure*, we compute $M_0^*$ in $O(D \cdot n^2 + n^3)$ operations. This pre-computes all instantaneous paths and verifies that no positive-weight zero-delay cycles exist.
> 
> Finally, in Stage 4, *Synthesis and Independent Validation*, we unroll the system across $K$ iterations into an unrolled difference DAG, execute Bellman-Ford longest-path propagation in $O(K \cdot E)$ time, and pass the resulting schedule to a completely decoupled verification oracle."

---

### Slide 10: Algorithmic Formulation — Algorithm 2: Kleene-Star State-Space Closure
- **Visual Callout:** Pseudocode for Algorithm 2, highlighting the backward arc insertion at line 5 ($A_0[u, v] \leftarrow \max(A_0[u, v], -U')$) and diagonal positive cycle check at line 8 ($M_0^*[i, i] > 0$).
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "Let us look at the formal pseudocode of Algorithm 2, which constructs the state-space matrices and computes the Kleene closure.
> 
> We initialize matrices $A_0$ to $A_D$ with $-\infty$, representing absence of constraints. In lines 2 to 3, forward lower-bound constraints populate the matrices with weight $L'$ at delay index $\delta$.
> 
> In lines 4 to 5, we encounter the key paper contribution: for each intra-iteration upper bound with delay $\delta = 0$, we insert a reverse edge from destination $v$ back to source $u$ in matrix $A_0$, with weight $-U'$.
> 
> In lines 6 to 7, we compute the Kleene star closure $M_0^*$ through $n-1$ iterations of max-plus matrix multiplication, which is structurally equivalent to the Floyd-Warshall algorithm.
> 
> In line 8, we verify the fundamental feasibility invariant: if any diagonal entry $M_0^*[i, i] > 0$, an intra-iteration contradictory cycle exists. The algorithm immediately halts and returns `INFEASIBLE_CYCLE`. This catches contradictions purely in matrix space, without unrolling a single iteration."

---

### Slide 11: Algorithmic Formulation — Algorithm 3: ASAP Longest-Path Synthesis
- **Visual Callout:** Pseudocode for Algorithm 3, showing Bellman-Ford relaxation over $|V_u|-1$ iterations and the positive cycle detection check.
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "Once the state-space matrices pass the Kleene check, Algorithm 3 synthesizes the exact earliest start times $S^*$ over a finite horizon of $K$ iterations.
> 
> We construct the unrolled difference graph $G_u$, containing $K \cdot |V|$ task nodes. We initialize the distance array to $-\infty$, with iteration-zero release times set in line 2.
> 
> Lines 3 to 5 execute classic Bellman-Ford longest-path relaxation. For $|V_u| - 1$ rounds, every edge is relaxed using max-plus algebra: 
> $$\text{dist}[v, k_v] = \max(\text{dist}[v, k_v], \text{dist}[u, k_u] + W)$$
> 
> In lines 6 to 7, we perform a final consistency pass. If any edge can still be relaxed, it mathematically proves that a positive-weight cycle spans across iterations—meaning the combination of execution times and upper bounds is physically impossible to satisfy.
> 
> Otherwise, the algorithm outputs the exact schedule $S^*[v, k] = \text{dist}[v, k]$. The computational complexity is $O(K \cdot |V| \cdot (|E| + |CL| + |CU|))$, which is strictly polynomial in all input dimensions."

---

### Slide 12: Illustrative Worked Example — Delaying on Purpose
- **Visual Callout:** The 3-stage wafer walkthrough timeline comparing Greedy ASAP (defect at 6.0 s) against Synthesized execution (deliberate delay to $t=5.0\text{ s}$, dwell = 4.0 s).
- **Target Time:** 50 seconds

> **[Spoken Script]**
> "To make this crystal clear, Slide 12 presents a step-by-step worked example adapted from semiconductor manufacturing.
> 
> We have three tasks: $A$ (Pre-Heat, duration 3s), $B$ (Transport, duration 2s), and $C$ (Chemical Deposition, duration 5s). The engineering constraint is that after Pre-Heat finishes, Deposition must begin within 4.0 seconds: $s_C - c_A \le 4.0\text{ s}$. Crucially, downstream chamber $C$ is occupied by wafer $k-1$ until timestamp $t = 12.0\text{ s}$.
> 
> Look at the top timeline: Greedy ASAP fires Pre-Heat as early as possible at $t = 3.0\text{ s}$, completing at $t = 6.0\text{ s}$. But Chamber $C$ is busy until $t = 12.0\text{ s}$! The heated wafer sits idling for $12 - 6 = 6.0\text{ seconds}$—violating the 4.0-second dwell limit and destroying the wafer!
> 
> Now observe the synthesized schedule below: our algorithm inverts the upper bound into a backward constraint: 
> $$s_A \ge s_C - 4 - w(A) = 12 - 4 - 3 = 5.0\text{ s}$$
> 
> The synthesizer *deliberately delays* Pre-Heat to start at $t = 5.0\text{ s}$. Pre-Heat completes at $t = 8.0\text{ s}$, and when Chamber $C$ opens at $t = 12.0\text{ s}$, the wafer has waited exactly $12 - 8 = 4.0\text{ seconds}$—satisfying the upper bound with mathematical perfection!
> 
> I now hand over to Ampili Hemanth Kumar to walk us through the theoretical correctness proofs and our experimental evaluation."

---

```
========================================================================================
SPEAKER 4: Ampili Hemanth Kumar (Roll: 230128)
SLIDES: 13 to 16  |  TARGET TIME: ~2.5 to 3.0 Minutes
========================================================================================
```

### Slide 13: Theoretical Correctness & Formal Guarantees
- **Visual Callout:** The four proof pillars: Soundness (zero false schedules), Completeness (exact feasibility verdict), Optimality (earliest starts), and Zero Throughput Degradation ($0.0\text{ s}$ penalty).
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "Thank you, Rahaman. I am Ampili Hemanth Kumar. I will present the formal correctness guarantees and our empirical evaluation.
> 
> The paper establishes four foundational theorems that we formally re-verified during our reproduction.
> 
> First is *Soundness*: every synthesized schedule $S^*$ is guaranteed to satisfy all lower and upper bounds without exception. Bellman-Ford termination guarantees that $\text{dist}[v] \ge \text{dist}[u] + W$ holds across every arc.
> 
> Second is *Completeness*: the algorithm is an exact decision procedure. If a feasible schedule exists, it will find it; if no schedule exists, it will extract an explicit positive cycle proving unsatisfiability. There are zero false negatives.
> 
> Third is *Componentwise Optimality*: for any other feasible schedule $S'$, $S^* \le S'$ holds for every task and iteration. This ensures the earliest completion and minimal makespan.
> 
> Fourth is the *Zero Throughput Degradation Theorem*: as long as upper bounds exceed the pipeline's critical cycle latency, inserting intentional delays absorbs non-critical slack without affecting the bottleneck resource. The total makespan penalty is exactly zero seconds."

---

### Slide 14: Experimental Methodology & Independent Verification
- **Visual Callout:** The three benchmark suites (Wafer Tool, DSP Streaming, Synthetic Scalability), the 28-test verification badge, and the 5 decoupled oracle checks with $\varepsilon \le 10^{-9}$.
- **Target Time:** 40 seconds

> **[Spoken Script]**
> "To validate these theoretical claims, we constructed an exhaustive empirical testbed across three benchmark families.
> 
> Benchmark 1 is the industrial Semiconductor Wafer Tool, featuring a 5-chamber cluster line with dual thermal dwell limits of $\le 3.0\text{ s}$ and $\le 2.0\text{ s}$. 
> Benchmark 2 is a 4-stage DSP video streaming pipeline subjected to tightness sweeps across varying jitter thresholds. 
> Benchmark 3 comprises synthetic pipeline topologies scaled up to 100 actors and 20 iterations—encompassing 1,000 task firings.
> 
> To ensure total scientific integrity, we built an *independent test oracle* that completely isolates itself from the max-plus solver. For every synthesized schedule, the oracle evaluates five ground-truth physical constraints: non-negativity, FIFO token precedence, lower bounds, upper bounds, and non-reentrancy, with floating-point residual tolerance $\varepsilon \le 10^{-9}$. All 28 automated tests pass with 100% compliance in 0.17 seconds."

---

### Slide 15: Experiment 1 — Semiconductor Wafer Cluster Tool Results
- **Visual Callout:** The before-and-after comparison showing greedy dwell violations (4.0s and 6.0s) clamped to exactly 3.0s, with identical 36.0s makespan.
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "Slide 15 shows our results on the industrial semiconductor wafer tool across $K = 4$ wafer lots.
> 
> Under greedy self-timed execution, wafer 2 suffered a transit dwell time of 4.0 seconds, and wafer 3 suffered 6.0 seconds—both severely violating the 3.0-second thermal threshold. In an actual semiconductor fab, both silicon wafers would be scrap.
> 
> When our synthesized schedule is deployed, the synthesizer detects the bottleneck at the Process Chamber ($w = 6.0\text{ s}$) and intentionally delays the LoadLock and PreHeat operations of subsequent wafers. 
> 
> As you can see, wafer 2 and wafer 3 dwell times are clamped precisely to 3.000 seconds—completely eliminating all fabrication defects!
> 
> And here is the remarkable result: the total makespan for both greedy and synthesized schedules is identical at exactly 36.0 seconds! By shifting tasks into available idle slack, we achieved 100% constraint satisfaction with zero makespan degradation."

---

### Slide 16: Experiments 2 & 3 — Scalability & Phase Transitions
- **Visual Callout:** The execution time scaling graph showing 154 ms for 1,000 tasks versus >300s MILP timeout, and the sharp phase transition cliff at tightness factor $t_f = 1.0$.
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "In Experiments 2 and 3, we evaluated scalability and constraint tightness limits.
> 
> On the left, we compare our max-plus synthesis algorithm against standard MILP and SMT formulations as task counts grow. While MILP solvers experience exponential explosion and time out past thirty actors, our algorithm scales strictly polynomially. For a massive topology of 100 actors across 10 iterations—totaling 1,000 task firings—our implementation synthesizes the complete schedule in just 154 milliseconds! This sub-second execution makes dynamic, online schedule reconfiguration entirely feasible on embedded controllers.
> 
> On the right, we examine the DSP pipeline across a tightness sweep from $t_f = 0.8$ to $2.0$. At $t_f = 1.0$, where the upper bound equals the critical cycle latency ($T_{\text{crit}} = 12.0\text{ s}$), slack hits exactly zero. The moment $t_f < 1.0$, an inter-iteration positive cycle forms, and our algorithm rejects the specification in just 0.02 milliseconds!
> 
> I now hand over to Koneti Karthik for our critical reflection, conclusions, and team overview."

---

```
========================================================================================
SPEAKER 5: Koneti Karthik (Roll: 230568)
SLIDES: 17 to 20  |  TARGET TIME: ~2.5 to 3.0 Minutes
========================================================================================
```

### Slide 17: Critical Reflection & Threats to Validity
- **Visual Callout:** The side-by-side comparison between Author-Acknowledged Limitations (deterministic execution, static dataflow, unrolling) and Our Reproduction Findings (memory scaling, no public code, sub-millisecond RTOS jitter).
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "Thank you, Hemanth. I am Koneti Karthik. I will conclude our talk with an honest critical appraisal, key conclusions, and our team contributions.
> 
> In Slide 17, we distinguish between limitations acknowledged by the authors and additional practical challenges we discovered during our reproduction.
> 
> The authors openly acknowledge that their framework assumes deterministic task durations $w(v)$. In real cyber-physical systems, cache misses, bus contention, or memory stalls can introduce execution jitter that may violate tight bounds at runtime. Furthermore, the model is restricted to static dataflow; variable-rate systems like Cyclo-Static or Scenario-Aware SDF require worst-case expansions.
> 
> From our engineering perspective, we identified three vital threats:
> First, while synthesis time is $O(K \cdot E)$, graph memory scales with $K \cdot |V|$; horizons beyond 1,000 iterations require sparse matrix data structures. 
> Second, the authors provided no public reference implementation; our team reconstructed the entire mathematics from the formal text. 
> Third, enforcing zero-slack schedules requires microsecond-accurate OS dispatching, mandating a hard Real-Time Operating System."

---

### Slide 18: Conclusions & Key Takeaways
- **Visual Callout:** The four takeaway blocks: Algebraic Unification, Defects Gone with No Penalty, Sub-Second Tractability, and Full Reproduction Fidelity.
- **Target Time:** 45 seconds

> **[Spoken Script]**
> "To summarize our findings, this reproduction delivers four foundational takeaways.
> 
> First, *Algebraic Unification*: upper timing bounds are not non-linear roadblocks requiring exponential search. In difference-constraint space, they are simply backward directed arcs with negative weights, fully solvable with linear algebra.
> 
> Second, *Zero Makespan Penalty*: on the semiconductor wafer tool, critical dwell violations were reduced from 6.0 seconds down to the 3.0-second limit, eliminating thermal defects while preserving the optimal 36.0-second makespan.
> 
> Third, *Sub-Second Tractability*: by replacing exponential solvers with Bellman-Ford propagation, 1,000 task firings synthesize in 154 milliseconds, proving the feasibility of embedded online re-scheduling.
> 
> Fourth, *Complete Reproduction Fidelity*: our Python implementation, accompanied by 28 automated test cases, reproduces the paper's claims with numerical precision $\varepsilon \le 10^{-9}$."

---

### Slide 19: Bibliography & Formal References
- **Visual Callout:** The three bibliography sections: Primary EMSOFT 2025 Paper, Foundational Dataflow Literature (Lee & Messerschmitt 1987, Bhattacharyya et al. 1996), and Max-Plus Linear Systems (Baccelli et al. 1992, Karp 1978, Cuninghame-Green 1979).
- **Target Time:** 30 seconds

> **[Spoken Script]**
> "Slide 19 lists our primary bibliography. 
> 
> In addition to the primary paper by van Wanrooij, Basten, and Geilen in ACM TECS 2025, our mathematical implementation rests on foundational dataflow theory by Edward Lee and David Messerschmitt, as well as the definitive max-plus linear system treatises by Baccelli, Cohen, Olsder, and Quadrat, along with Richard Karp's minimum cycle-mean characterization.
> 
> Every equation, matrix transformation, and cycle ratio calculation in our codebase was cross-referenced and verified against these foundational texts."

---

### Slide 20: Team Allocation, Deliverables & Q&A
- **Visual Callout:** Team member cards showing equal 20% distribution, repository deliverables list (clean codebase, 28/28 tests passing in 0.17s, benchmarks, claim traceability doc), and Q&A invitation.
- **Target Time:** 40 seconds

> **[Spoken Script]**
> "Finally, Slide 20 highlights our team allocation and open-source project deliverables.
> 
> Following the speaking order of today's presentation, our team divided the engineering workload into five equal twenty percent components:
> Vempati Prem Santhosh built the independent test oracle and the 28-case automated verification suite. 
> Sanga Badri developed the Extended HSDF model, balance equations, and actor serialization. 
> Our project lead, Sk J Ur Rahaman, engineered the max-plus matrix engine, state-space construction, and Kleene star closure. 
> Ampili Hemanth Kumar implemented the Bellman-Ford synthesis algorithm and cycle conflict extractor. 
> And I, Koneti Karthik, engineered the benchmark suites, parameter sweeps, and presentation assets.
> 
> Our full codebase, along with documentation and reproduction scripts, is verified and committed to our repository.
> 
> On behalf of our entire team from IIT Kanpur, thank you for your attention. We are delighted to answer any questions on max-plus linearization, synthesis algorithms, or our experimental results."

---
*End of Speaker Scripts*
