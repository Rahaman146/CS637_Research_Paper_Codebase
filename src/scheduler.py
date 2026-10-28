r"""
Schedule synthesis engine for Extended HSDFGs with Lower and Upper Timing Bounds.
Implements:
- As-Soon-As-Possible (ASAP) schedule synthesis over finite horizon K iterations
  (minimizing makespan while satisfying all lower and upper bounds)
- Detection of infeasibility and contradictory bounds via positive cycle analysis
- Periodic schedule synthesis (optimizing throughput \lambda*)
- Slack analysis and sensitivity evaluation
"""

from typing import Dict, List, Optional, Tuple, NamedTuple
import numpy as np

from .model import ExtendedHSDFG, EventType, BoundType, NormalizedDifferenceConstraint
from .state_space import transform_extended_hsdfg_to_state_space


class ScheduleResult:
    """Container for synthesized schedule outputs."""

    def __init__(
        self,
        is_feasible: bool,
        start_times: Optional[np.ndarray] = None,  # (n_actors, K)
        completion_times: Optional[np.ndarray] = None,  # (n_actors, K)
        makespan: float = 0.0,
        throughput: Optional[float] = None,
        iterations: int = 0,
        conflict_info: Optional[str] = None,
    ):
        self.is_feasible = is_feasible
        self.start_times = start_times
        self.completion_times = completion_times
        self.makespan = makespan
        self.throughput = throughput
        self.iterations = iterations
        self.conflict_info = conflict_info

    def get_start(self, actor_id: int, iteration: int) -> float:
        if not self.is_feasible or self.start_times is None:
            raise ValueError("Schedule is not feasible")
        return float(self.start_times[actor_id, iteration])

    def get_completion(self, actor_id: int, iteration: int) -> float:
        if not self.is_feasible or self.completion_times is None:
            raise ValueError("Schedule is not feasible")
        return float(self.completion_times[actor_id, iteration])

    def __repr__(self):
        if not self.is_feasible:
            return f"ScheduleResult(INFEASIBLE: {self.conflict_info})"
        return (
            f"ScheduleResult(FEASIBLE, iterations={self.iterations}, "
            f"makespan={self.makespan:.3f}, throughput={self.throughput})"
        )


def synthesize_asap_schedule(
    graph: ExtendedHSDFG,
    iterations: int = 1,
    release_times: Optional[Dict[int, float]] = None,
) -> ScheduleResult:
    """
    Synthesizes the earliest-possible (ASAP) schedule for K iterations satisfying
    all dataflow precedences, lower-bound timing constraints, and upper-bound timing constraints.

    Solves the longest-path problem on the unrolled difference constraint graph.
    Detects contradictory constraints (positive cycles) and returns an infeasibility verdict.
    """
    n = graph.num_actors
    K = iterations
    if n == 0 or K <= 0:
        return ScheduleResult(is_feasible=True, makespan=0.0, iterations=0)

    # 1. First check intra-iteration state space feasibility
    ss = transform_extended_hsdfg_to_state_space(graph)
    if not ss.is_feasible:
        return ScheduleResult(
            is_feasible=False,
            iterations=K,
            conflict_info="Contradictory intra-iteration constraints (positive cycle in Kleene star M_0*)",
        )

    # 2. Extract all normalized difference constraints: s_dst(k) - s_src(k - delay) >= weight
    diff_constraints = graph.normalize_to_difference_constraints()

    # Total nodes = n * K + 1 (auxiliary source node sigma_0 at index n*K)
    num_nodes = n * K
    src_node = num_nodes

    # Node indexing: (actor_id, k) -> actor_id * K + k
    def get_idx(aid: int, k: int) -> int:
        return aid * K + k

    # Build edge list: (u, v, weight) where s_v >= s_u + weight
    edges: List[Tuple[int, int, float]] = []

    # Edges from auxiliary source node to iteration 0 (release times)
    for aid in range(n):
        r = 0.0
        if release_times and aid in release_times:
            r = float(release_times[aid])
        edges.append((src_node, get_idx(aid, 0), r))

    # All unrolled difference constraints
    for dc in diff_constraints:
        for k in range(K):
            k_src = k - dc.delay
            if 0 <= k_src < K:
                u = get_idx(dc.src_id, k_src)
                v = get_idx(dc.dst_id, k)
                edges.append((u, v, dc.weight))

    # Also enforce self-timed sequential execution within each actor stream:
    # s_v(k+1) >= c_v(k) = s_v(k) + w(v) (actors cannot fire concurrently with themselves)
    for aid, actor in graph.actors.items():
        w = actor.execution_time
        for k in range(K - 1):
            edges.append((get_idx(aid, k), get_idx(aid, k + 1), w))

    # 3. Longest Path via Bellman-Ford algorithm over num_nodes + 1
    total_nodes = num_nodes + 1
    dist = np.full(total_nodes, -np.inf, dtype=float)
    dist[src_node] = 0.0

    # Relaxation passes (total_nodes - 1 times)
    for _ in range(total_nodes - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != -np.inf:
                cand = dist[u] + w
                if cand > dist[v] + 1e-12:
                    dist[v] = cand
                    updated = True
        if not updated:
            break

    # Positive cycle check on pass total_nodes
    for u, v, w in edges:
        if dist[u] != -np.inf:
            if dist[u] + w > dist[v] + 1e-9:
                def node_desc(idx: int) -> str:
                    if idx == src_node:
                        return "auxiliary source sigma_0"
                    aid = idx // K
                    k = idx % K
                    aname = graph.actors[aid].name if aid in graph.actors else f"Actor_{aid}"
                    return f"Actor {aname} (k={k})"

                u_str = node_desc(u)
                v_str = node_desc(v)
                return ScheduleResult(
                    is_feasible=False,
                    iterations=K,
                    conflict_info=f"Contradictory constraints detected: positive cycle between {u_str} and {v_str}",
                )

    # 4. Construct start_times and completion_times matrices
    start_times = np.zeros((n, K), dtype=float)
    completion_times = np.zeros((n, K), dtype=float)

    for aid in range(n):
        w = graph.actors[aid].execution_time
        for k in range(K):
            val = dist[get_idx(aid, k)]
            # If node wasn't reached from source, default to 0.0
            st = max(0.0, val if val != -np.inf else 0.0)
            start_times[aid, k] = st
            completion_times[aid, k] = st + w

    makespan = float(np.max(completion_times))
    throughput = None
    if K > 1:
        # Measure empirical throughput over last iterations
        delta_iter = K - 1
        avg_period = (np.mean(start_times[:, -1]) - np.mean(start_times[:, 0])) / delta_iter
        if avg_period > 1e-9:
            throughput = 1.0 / avg_period

    return ScheduleResult(
        is_feasible=True,
        start_times=start_times,
        completion_times=completion_times,
        makespan=makespan,
        throughput=throughput,
        iterations=K,
    )


def synthesize_periodic_schedule(
    graph: ExtendedHSDFG,
    max_test_iterations: int = 10,
) -> ScheduleResult:
    r"""
    Synthesizes a periodic schedule and determines the steady-state period \lambda*
    and throughput \Theta = 1/\lambda*.
    """
    ss = transform_extended_hsdfg_to_state_space(graph)
    if not ss.is_feasible:
        return ScheduleResult(
            is_feasible=False,
            conflict_info="Intra-iteration constraint contradiction prevents periodic schedule",
        )

    # Run multi-iteration synthesis to measure steady-state period
    res = synthesize_asap_schedule(graph, iterations=max_test_iterations)
    if not res.is_feasible:
        return res

    # Compute period from steady state
    if max_test_iterations >= 3 and res.start_times is not None:
        p1 = res.start_times[:, -1] - res.start_times[:, -2]
        p0 = res.start_times[:, -2] - res.start_times[:, -3]
        if np.allclose(p1, p0, atol=1e-5):
            steady_period = float(np.mean(p1))
            res.throughput = 1.0 / steady_period if steady_period > 1e-9 else float("inf")

    return res


def analyze_bound_slack(
    graph: ExtendedHSDFG, schedule: ScheduleResult
) -> Dict[str, List[Dict]]:
    """
    Computes temporal slack for all lower and upper bounds against the schedule.
    Slack = 0 indicates a critical, binding constraint.
    """
    if not schedule.is_feasible or schedule.start_times is None:
        raise ValueError("Cannot analyze slack on an infeasible schedule")

    K = schedule.iterations
    lower_slacks = []
    upper_slacks = []

    for ct in graph.constraints:
        w_src = graph.actors[ct.src_id].execution_time
        w_dst = graph.actors[ct.dst_id].execution_time

        for k in range(K):
            k_src = k - ct.delay
            if 0 <= k_src < K:
                s_src = schedule.get_start(ct.src_id, k_src)
                s_dst = schedule.get_start(ct.dst_id, k)

                t_src = s_src + (w_src if ct.src_event == EventType.COMPLETION else 0.0)
                t_dst = s_dst + (w_dst if ct.dst_event == EventType.COMPLETION else 0.0)
                actual_diff = t_dst - t_src

                if ct.bound_type == BoundType.LOWER:
                    slack = actual_diff - ct.bound_value
                    lower_slacks.append({
                        "constraint_id": ct.id,
                        "iteration": k,
                        "actual_diff": actual_diff,
                        "bound_value": ct.bound_value,
                        "slack": slack,
                        "is_binding": abs(slack) < 1e-5,
                    })
                else:
                    slack = ct.bound_value - actual_diff
                    upper_slacks.append({
                        "constraint_id": ct.id,
                        "iteration": k,
                        "actual_diff": actual_diff,
                        "bound_value": ct.bound_value,
                        "slack": slack,
                        "is_binding": abs(slack) < 1e-5,
                    })

    channel_slacks = []
    for ch in graph.channels.values():
        w_src = graph.actors[ch.src_id].execution_time
        d = ch.initial_tokens
        for k in range(K):
            k_src = k - d
            if 0 <= k_src < K:
                s_src = schedule.get_start(ch.src_id, k_src)
                s_dst = schedule.get_start(ch.dst_id, k)
                diff = s_dst - (s_src + w_src)
                channel_slacks.append({
                    "channel_id": ch.id,
                    "src_actor": graph.actors[ch.src_id].name,
                    "dst_actor": graph.actors[ch.dst_id].name,
                    "iteration": k,
                    "slack": diff,
                    "is_binding": abs(diff) < 1e-5,
                })

    return {
        "lower_bounds": lower_slacks,
        "upper_bounds": upper_slacks,
        "channels": channel_slacks,
    }
