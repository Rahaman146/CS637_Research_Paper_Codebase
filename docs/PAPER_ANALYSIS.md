# Paper Analysis: Schedule Synthesis for Synchronous Dataflow Models with Lower and Upper Timing Bounds

**Paper Title:** Schedule Synthesis for Synchronous Dataflow Models with Lower and Upper Timing Bounds  
**Authors:** Joep van Wanrooij, Twan Basten, Marc Geilen  
**Affiliation:** Electronic Systems Group, Department of Electrical Engineering, Eindhoven University of Technology (TU/e), The Netherlands  
**Venue:** ACM Transactions on Embedded Computing Systems (TECS), Vol. 24, Issue 5s, Article 143 (Presented at EMSOFT 2025)  
**Official DOI:** [10.1145/3762643](https://doi.org/10.1145/3762643)

---

## A. Research Problem

### 1. Problem Statement
The paper addresses the challenge of **synthesizing deterministic, optimal execution schedules for Synchronous Dataflow (SDF) and Homogeneous Synchronous Dataflow (HSDF) models when tasks are subject to both lower-bound and upper-bound timing constraints**. 

In conventional dataflow semantics, execution is governed exclusively by data-availability precedence: an actor can fire as soon as its input channels contain the required number of tokens. In timed models, this corresponds strictly to **lower bounds**—a task cannot start before preceding tasks have finished and delivered their tokens. However, many real-world embedded, cyber-physical, and manufacturing systems impose strict **upper bounds** (deadlines, maximum permissible wait times between operations, maximum dwell times in chemical or thermal processing, jitter limits) as well as **relative lower bounds** (minimum separation between task starts). 

Traditional SDF/HSDF formalisms cannot express these bidirectional timing constraints without losing their algebraic tractability or leading to intractable state-space explosion. The paper develops an analytical framework that incorporates lower and upper timing bounds directly into the dataflow model and synthesizes feasible, performance-optimal schedules.

### 2. Importance of the Problem
- **Advanced Manufacturing & Semiconductor Fabrication:** In wafer manufacturing, cluster tools, and photolithography lines, wafers must be processed through sequential chambers (e.g., bake, coat, expose, etch). A wafer must not remain on a hotplate or in an acid bath beyond a strict upper threshold (critical dwell time) to avoid ruining the wafer, while transport robotics enforce lower bounds on transit.
- **Hard Real-Time Embedded Streaming:** High-performance video pipelines (e.g., medical imaging, automotive vision) require guaranteed frame-rate throughput while adhering to strict latency and inter-frame jitter windows (upper bounds on start-to-finish time differences).
- **Correctness by Construction:** In safety-critical embedded systems, uncoordinated greedy execution ("fire as soon as data arrives") can violate upper-bound deadlines or cause buffer overflows. A formal schedule synthesis methodology guarantees temporal correctness prior to deployment.

### 3. Limitations of Prior Scheduling Approaches
- **Self-Timed / Greedy Dataflow Execution:** Traditional SDF execution models assume self-timed execution where actors fire as early as data is available ($ASAP$). While self-timed execution maximizes throughput under pure lower bounds (monotonicity theorem of dataflow), it completely fails in the presence of upper bounds: firing a task too early can violate an upper bound relative to a subsequent task, or cause downstream buffers to exceed deadlines.
- **Integer Linear Programming (ILP) and SMT Solvers:** Existing approaches often resort to generic ILP or SMT formulations. While expressive, their execution time scales exponentially with graph size and iteration count, rendering them impractical for synthesis of repeating schedules or multi-iteration analysis.
- **Timed Automata & Model Checking:** Modeling dataflow systems in timed automata frameworks (e.g., UPPAAL) suffers from severe state-space explosion due to continuous clock variables and concurrent interleavings.
- **Standard $(\max, +)$ Semantics:** Conventional $(\max, +)$ linear system theory applies only to systems with causal delays (lower bounds). Upper bounds translate into negative delays or reverse dependencies, which classical max-plus matrix algebra does not natively accommodate without explicit constraint-graph transformation.

### 4. Specific Contributions of the Paper
1. **Extended HSDFG Formalism:** An augmented HSDFG model supporting user-specified lower-bound ($C_L$) and upper-bound ($C_U$) constraints on timing differences between any pair of actor-firing events (starts $s$ and completions $c$) across arbitrary iteration offsets ($\delta \in \mathbb{Z}$).
2. **State-Space Matrix Transformation:** A systematic method for mapping an extended HSDFG into a $(\max, +)$ linear state-space system $(A_0, A_1, \dots, A_D)$ with backward difference arcs, enabling algebraic analysis.
3. **Algebraic Schedule Synthesis:** Algorithms to synthesize valid task execution schedules achieving the earliest possible execution times (optimizing makespan and throughput) while rigorously guaranteeing satisfaction of all lower and upper bounds.
4. **Industrial Case Study:** Demonstration and validation on a realistic manufacturing system case study, illustrating that timing bounds prevent physical failures that greedy/unbounded schedules produce.

---

## B. Technical Foundations

### 1. Synchronous Dataflow (SDF) and Homogeneous SDF (HSDF)
An SDF graph is a directed multigraph $G = (V, E, \text{prd}, \text{cns}, d, w)$ where:
- $V = \{v_1, \dots, v_n\}$ is the set of actors (computational tasks).
- $E \subseteq V \times V$ is the set of directed communication channels.
- $\text{prd}(e) \in \mathbb{N}_{>0}$ is the number of tokens produced onto channel $e$ by its source actor per firing.
- $\text{cns}(e) \in \mathbb{N}_{>0}$ is the number of tokens consumed from channel $e$ by its destination actor per firing.
- $d(e) \in \mathbb{N}_0$ is the initial token count (delay) on channel $e$.
- $w(v) \in \mathbb{R}_{\ge 0}$ is the execution duration of actor $v$.

An SDF graph is **homogeneous** (HSDF) when $\text{prd}(e) = \text{cns}(e) = 1$ for all $e \in E$. Every consistent general SDF graph can be converted to an equivalent HSDF graph via actor expansion according to its non-trivial repetition vector $\mathbf{q} \in \mathbb{N}^n$, satisfying the balance equation:
$$\forall e = (u, v) \in E: \quad q(u) \cdot \text{prd}(e) = q(v) \cdot \text{cns}(e)$$

### 2. Events and Timing Semantics
In an HSDFG, each actor $v$ executes repeatedly in discrete iterations $k \in \mathbb{N}_0 = \{0, 1, 2, \dots\}$. For iteration $k$:
- $s_v(k) \in \mathbb{R}_{\ge 0}$ denotes the **start timestamp** of the $k$-th firing of actor $v$.
- $c_v(k) \in \mathbb{R}_{\ge 0}$ denotes the **completion timestamp** of the $k$-th firing of actor $v$, defined by:
  $$c_v(k) = s_v(k) + w(v)$$

In a standard HSDFG, an edge $e = (u, v)$ with initial tokens $d(e)$ requires that the $k$-th firing of $v$ cannot start until the $(k - d(e))$-th firing of $u$ has completed:
$$s_v(k) \ge c_u(k - d(e)) = s_u(k - d(e)) + w(u) \quad (\forall k \ge d(e))$$

### 3. Lower and Upper Timing Bounds
An **extended HSDFG** introduces explicit temporal constraints between event pairs:
- **Event Definition:** An event $E_i(k)$ is either a start $s_i(k)$ or completion $c_i(k)$.
- **Lower-Bound Constraint ($C_L$):**
  $$E_{dst}(k) - E_{src}(k - \delta) \ge L$$
  Enforces a minimum time delay $L \in \mathbb{R}$ between the source event in iteration $k - \delta$ and the destination event in iteration $k$.
- **Upper-Bound Constraint ($C_U$):**
  $$E_{dst}(k) - E_{src}(k - \delta) \le U$$
  Enforces that the destination event cannot occur more than $U \in \mathbb{R}$ time units after the source event.

### 4. $(\max, +)$ Semiring Algebra
Max-plus algebra is defined over the set $\mathbb{R}_{\max} = \mathbb{R} \cup \{-\infty\}$ equipped with two binary operations:
- **Max-plus addition ($\oplus$):** $a \oplus b = \max(a, b)$
  - Identity element: $\varepsilon = -\infty$ ($a \oplus \varepsilon = a$).
- **Max-plus multiplication ($\otimes$):** $a \otimes b = a + b$
  - Identity element: $e = 0$ ($a \otimes e = a$).
  - Absorbing element: $\varepsilon \otimes a = \varepsilon$.

Matrix operations follow standard linear algebra rules under $(\oplus, \otimes)$:
$$(A \oplus B)_{ij} = A_{ij} \oplus B_{ij} = \max(A_{ij}, B_{ij})$$
$$(A \otimes B)_{ij} = \bigoplus_k (A_{ik} \otimes B_{kj}) = \max_k (A_{ik} + B_{kj})$$

The **Kleene star** $A^*$ of a square matrix $A \in \mathbb{R}_{\max}^{n \times n}$ represents the transitive closure of paths:
$$A^* = \bigoplus_{p=0}^{n-1} A^p = I \oplus A \oplus A^2 \oplus \dots \oplus A^{n-1}$$
where $I$ is the max-plus identity matrix ($I_{ii} = 0$, $I_{ij} = -\infty$ for $i \ne j$). The Kleene star exists and is finite if and only if the graph associated with $A$ contains no cycles with positive weight (no positive cycle in max-plus means no circular growth).

---

## C. Mathematical Formulation

### 1. Unified Event Constraint Representation
All constraints on completions $c_v(k) = s_v(k) + w(v)$ are normalized into linear constraints over start times $\mathbf{s}(k) = [s_1(k), \dots, s_n(k)]^T$:

1. **Normalized Lower Bound:**
   $$s_j(k) - s_i(k - \delta) \ge L'_{ij,\delta} \iff s_j(k) \ge s_i(k - \delta) + L'_{ij,\delta}$$
   where:
   - If constraint is $(s_i \to s_j)$: $L' = L$
   - If constraint is $(c_i \to s_j)$: $L' = L + w(i)$
   - If constraint is $(s_i \to c_j)$: $L' = L - w(j)$
   - If constraint is $(c_i \to c_j)$: $L' = L + w(i) - w(j)$

2. **Normalized Upper Bound:**
   $$s_j(k) - s_i(k - \delta) \le U'_{ij,\delta}$$
   where $U'$ is computed identically using $U$ in place of $L$.
   Crucially, this inequality can be rewritten as:
   $$s_i(k - \delta) \ge s_j(k) - U'_{ij,\delta}$$
   which represents a **backward lower-bound constraint** from $s_j(k)$ to $s_i(k - \delta)$ with weight $-U'_{ij,\delta}$ and delay $-\delta$.

### 2. State-Space Matrix Transformation
Let $D = \max \{ \delta \mid (i, j, \delta) \in E \cup C_L \cup C_U \}$.
For intra-iteration lower bounds ($\delta = 0$):
$$(A_0)_{ji} = \max \left\{ L'_{ij,0} \right\}$$
For inter-iteration lower bounds with delay $\delta \in \{1, \dots, D\}$:
$$(A_\delta)_{ji} = \max \left\{ L'_{ij,\delta} \right\}$$

For intra-iteration upper bounds ($\delta = 0$):
$s_j(k) - s_i(k) \le U'_{ij,0} \implies s_i(k) \ge s_j(k) - U'_{ij,0}$.
This contributes a backward constraint to the intra-iteration matrix:
$$(B_0)_{ij} = -U'_{ij,0}$$

The total intra-iteration matrix is:
$$M_0 = A_0 \oplus B_0$$
The intra-iteration closure matrix is the Kleene star:
$$M_0^* = I \oplus M_0 \oplus M_0^2 \oplus \dots \oplus M_0^{n-1}$$
**Feasibility Condition for $M_0^*$:** $M_0$ has no cycle with strictly positive weight. If a positive cycle exists, the upper bounds and lower bounds are mutually contradictory (e.g., requiring $s_j \ge s_i + 10$ but $s_j \le s_i + 5$), and no valid schedule exists.

### 3. Schedule Synthesis Objectives
1. **Makespan Optimization (Finite Horizon $K$ Iterations):**
   Given iteration horizon $K$, determine $\mathbf{S} = [\mathbf{s}(0)^T, \dots, \mathbf{s}(K-1)^T]^T \in \mathbb{R}^{nK}$ minimizing makespan:
   $$\min \max_{v \in V} c_v(K-1)$$
   subject to:
   $$\forall k, k', i, j: \quad s_j(k) - s_i(k') \ge W_{(i,k') \to (j,k)}$$
   $$\forall k, i: \quad s_i(k) \ge 0$$
   The earliest possible start times $\mathbf{S}^*$ are computed via longest-path propagation on the directed constraint DAG over the unrolled iterations.

2. **Throughput Optimization (Infinite Horizon Periodic Schedule):**
   For a 1-periodic schedule $s_v(k) = s_v(0) + k \cdot \lambda$:
   $$\text{Throughput } \Theta = \frac{1}{\lambda}$$
   The minimum period $\lambda^*$ is governed by the Maximum Cycle Ratio (MCR) over all cycles in the dependency graph:
   $$\lambda^* = \max_{\gamma} \frac{W(\gamma)}{D(\gamma)} \quad \text{for all cycles } \gamma \text{ with } D(\gamma) > 0$$
   while verifying that any cycles with $D(\gamma) < 0$ satisfy $\lambda^* \le \frac{W(\gamma)}{D(\gamma)}$.

---

## D. Algorithm Reconstruction

### Algorithm 1: Extended HSDFG Normalization
- **Input:** Graph $G = (V, E, w)$, lower bounds $C_L$, upper bounds $C_U$.
- **Output:** Unified difference constraint graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$.
- **Steps:**
  1. For each actor $v \in V$, create nodes $s_v$ and record execution duration $w(v)$.
  2. For each edge $e = (u, v) \in E$ with token delay $d(e)$, add constraint edge $(u, v)$ with weight $w(u)$ and delay $d(e)$.
  3. For each lower bound $(src, dst, \delta, L) \in C_L$, compute $L'$ based on whether $src, dst$ are starts or completions; add directed edge $src \to dst$ with delay $\delta$ and weight $L'$.
  4. For each upper bound $(src, dst, \delta, U) \in C_U$, compute $U'$; add backward directed edge $dst \to src$ with delay $-\delta$ and weight $-U'$.
- **Precondition:** Valid durations $w(v) \ge 0$.
- **Postcondition:** All timing constraints expressed as difference constraints $s_{tgt} - s_{src} \ge \text{weight}$.

### Algorithm 2: Max-Plus State-Space Matrix Construction
- **Input:** Normalized constraint set, dimension $n$, maximum delay $D$.
- **Output:** Matrices $A_0, A_1, \dots, A_D \in \mathbb{R}_{\max}^{n \times n}$, closure $M_0^*$.
- **Steps:**
  1. Initialize $A_d = [-\infty]_{n \times n}$ for $d = 0, \dots, D$.
  2. Populate $A_d$ with normalized forward constraints: $(A_d)_{ji} = \max \{ L'_{ij,d} \}$.
  3. For intra-iteration upper bounds ($\delta = 0$), populate backward edges: $(A_0)_{ij} = \max((A_0)_{ij}, -U'_{ij,0})$.
  4. Compute Kleene star $M_0^* = \bigoplus_{p=0}^{n-1} A_0^p$.
  5. Check diagonal of $M_0^*$: if $(M_0^*)_{ii} > 0$ for any $i$, report infeasibility (positive intra-iteration cycle detected).
- **Complexity:** $\mathcal{O}(D \cdot n^2 + n^3)$ using Floyd-Warshall style closure.

### Algorithm 3: ASAP Finite-Horizon Schedule Synthesis
- **Input:** State-space matrices or unrolled constraint graph over $K$ iterations, release times $\mathbf{r} \ge 0$.
- **Output:** Start time matrix $\mathbf{S} \in \mathbb{R}^{n \times K}$, makespan, or infeasibility verdict.
- **Steps:**
  1. Build unrolled DAG with $n \cdot K$ nodes plus auxiliary source node $\sigma_0$ with edges to all $(v, 0)$ with weight $r_v$.
  2. Initialize distance vector $\text{dist}[u] = -\infty$, $\text{dist}[\sigma_0] = 0$.
  3. Perform topological sort or Bellman-Ford longest-path iteration over the $nK$ nodes.
  4. If a positive cycle is detected, declare the timing constraints mathematically unsatisfiable.
  5. Otherwise, $\mathbf{s}_v(k) = \text{dist}[(v, k)]$.
  6. Return $\mathbf{S}$ and makespan $\max_{v} (s_v(K-1) + w(v))$.
- **Complexity:** $\mathcal{O}(|V_{\text{unroll}}| \cdot |E_{\text{unroll}}|) = \mathcal{O}(n K \cdot (|E| + |C_L| + |C_U|) K)$.

### Algorithm 4: Independent Schedule Verification
- **Input:** Proposed schedule $\mathbf{S}$, original graph $G$, $C_L$, $C_U$.
- **Output:** Boolean `is_valid`, list of violated constraints.
- **Steps:**
  1. Check non-negativity: $s_v(k) \ge 0$ for all $v, k$.
  2. Check dataflow precedence: $\forall (u, v, \delta) \in E: s_v(k) \ge s_u(k - \delta) + w(u)$.
  3. Check lower bounds: $\forall cl \in C_L: t_{dst}(k) - t_{src}(k - \delta) \ge L - \epsilon_{\text{tol}}$.
  4. Check upper bounds: $\forall cu \in C_U: t_{dst}(k) - t_{src}(k - \delta) \le U + \epsilon_{\text{tol}}$.
  5. If any check fails, log constraint details and return `False`.

---

## E. Experimental Evaluation

The experiments evaluated in the reproduction are detailed below:

| Exp ID | Research Question | Benchmark Instance | Metric | Published / Expected Behavior | Reproducibility |
|---|---|---|---|---|---|
| **EXP-1** | Can extended HSDFGs model physical timing bounds in manufacturing? | Wafer Processing Cluster Tool (Heating, Transport, Deposition, Anneal) with upper dwell bounds | Makespan, Bound violations (greedy vs. synthesized) | Greedy schedule violates upper dwell bound ($t_{\text{wait}} > U$). Synthesized schedule delays start times as necessary to guarantee all dwell bounds are met. | **Fully Reproducible** |
| **EXP-2** | How do tight upper bounds impact schedule throughput and makespan? | DSP Streaming Pipelines (Bipartite, 4-stage pipeline, Cyclic feedback) | Makespan, Slack distribution, Infeasibility transition | As upper bound $U$ tightens below critical path latency, schedule switches from feasible to provably infeasible (detected by positive cycle). | **Fully Reproducible** |
| **EXP-3** | How does the $(\max, +)$ state-space transformation scale with graph size? | Synthetic and literature SDF topologies ($N = 5$ to $100$ actors) | Synthesis runtime (ms), Matrix transformation time | Linear-to-polynomial scaling; orders of magnitude faster than naive ILP. | **Fully Reproducible** |
| **EXP-4** | Does the independent validator confirm schedule correctness across all instances? | All synthesized benchmark schedules | Pass rate (%), Max constraint error | 100% pass rate; absolute constraint residual $\le 10^{-9}$. | **Fully Reproducible** |

---

## F. Reproduction Feasibility Assessment

- **Mathematical Model:** Fully specified. Difference constraints and max-plus semiring matrix algebra are mathematically unambiguous and implemented without guesswork.
- **Transformation Method:** Fully specified. State-space matrices $(A_0, \dots, A_D)$ and Kleene star closure $M_0^*$ are standard algebraic tools in max-plus literature.
- **Benchmark Topologies:** Reconstructed faithfully based on the manufacturing cluster-tool case study and literature DSP streaming dataflow graphs.
- **Independent Verification:** Fully realizable via exact constraint checking.
