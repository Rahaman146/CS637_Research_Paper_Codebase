r"""
Transformation of Extended HSDFG models into (max, +) linear state-space systems.
Implements:
- Construction of state-space matrices A_0, A_1, ..., A_D
- Backward difference arc integration for upper bounds
- Intra-iteration closure via Kleene star M_0*
- Infeasibility detection (positive weight cycles)
- Computation of closed-loop transition matrix A = M_0* \otimes A_1
"""

from typing import Dict, List, Optional, Tuple
import numpy as np

from .maxplus import (
    EPSILON,
    mp_zero,
    mp_identity,
    mp_add,
    mp_mult,
    kleene_star,
    maximum_cycle_mean,
)
from .model import ExtendedHSDFG, NormalizedDifferenceConstraint


class StateSpaceMatrices:
    r"""
    State-space matrix container for extended HSDFG:
    x(k) = A_0 \otimes x(k) \oplus A_1 \otimes x(k-1) \oplus ... \oplus A_D \otimes x(k-D)
    Resolved form:
    x(k) = M_0^* \otimes \bigoplus_{d=1}^D (A_d \otimes x(k-d))
    """

    def __init__(
        self,
        n: int,
        max_delay: int,
        a_matrices: Dict[int, np.ndarray],
        m0_star: np.ndarray,
        is_feasible: bool,
        backward_inter_constraints: List[NormalizedDifferenceConstraint],
        actor_to_idx: Optional[Dict[int, int]] = None,
        idx_to_actor: Optional[Dict[int, int]] = None,
    ):
        self.n = n
        self.max_delay = max_delay
        self.a_matrices = a_matrices  # d -> A_d (n x n)
        self.m0_star = m0_star        # (n x n) Kleene star of A_0
        self.is_feasible = is_feasible
        self.backward_inter_constraints = backward_inter_constraints
        self.actor_to_idx = actor_to_idx or {i: i for i in range(n)}
        self.idx_to_actor = idx_to_actor or {i: i for i in range(n)}

    @property
    def a0(self) -> np.ndarray:
        return self.a_matrices[0]

    @property
    def a1(self) -> Optional[np.ndarray]:
        return self.a_matrices.get(1, None)

    def compute_state_transition_matrix(self) -> Optional[np.ndarray]:
        r"""
        Computes the state transition matrix:
        - For D = 1: A = M_0^* \otimes A_1 (dimension n x n).
        - For D > 1: General companion transition matrix \hat{A} of dimension (nD x nD):
          [ M_0^* \otimes A_1, M_0^* \otimes A_2, ..., M_0^* \otimes A_D ]
          [ I_n,               \epsilon,           ..., \epsilon          ]
          [ \epsilon,          I_n,                ..., \epsilon          ]
        """
        if not self.is_feasible or self.n == 0:
            return None if not self.is_feasible else mp_identity(0)
        if 1 not in self.a_matrices:
            return None

        D = max(1, self.max_delay)
        n = self.n

        if D == 1:
            return mp_mult(self.m0_star, self.a_matrices[1])

        # Multi-delay companion matrix formulation for D > 1
        comp = mp_zero(n * D, n * D)
        for d in range(1, D + 1):
            ad = self.a_matrices.get(d, mp_zero(n, n))
            block = mp_mult(self.m0_star, ad)
            comp[0:n, (d - 1) * n : d * n] = block

        eye = mp_identity(n)
        for d in range(1, D):
            comp[d * n : (d + 1) * n, (d - 1) * n : d * n] = eye

        return comp

    def compute_spectral_throughput(self) -> Optional[float]:
        r"""
        Computes throughput via Maximum Cycle Mean (MCM) on the companion transition matrix.
        Throughput \Theta = 1 / \lambda*.
        """
        trans = self.compute_state_transition_matrix()
        if trans is None or trans.shape[0] == 0:
            return None
        mcm = maximum_cycle_mean(trans)
        if mcm <= 0:
            return float("inf")
        return 1.0 / mcm


def transform_extended_hsdfg_to_state_space(graph: ExtendedHSDFG) -> StateSpaceMatrices:
    """
    Transforms an ExtendedHSDFG into (max, +) state-space matrices:
    A_0, A_1, ..., A_D and closure M_0*.

    Handles:
    - Arbitrary, non-contiguous actor IDs via canonical indexing
    - Actor execution times w(u)
    - Token delays on channels (arbitrary D >= 1)
    - Normalized lower-bound constraints
    - Intra-iteration upper-bound backward arcs inserted into A_0
    - Multi-iteration backward constraints tracked for global unrolled synthesis
    """
    n = graph.num_actors
    if n == 0:
        return StateSpaceMatrices(0, 0, {0: mp_identity(0)}, mp_identity(0), True, [])

    actor_ids = sorted(graph.actors.keys())
    actor_to_idx = {aid: idx for idx, aid in enumerate(actor_ids)}
    idx_to_actor = {idx: aid for idx, aid in enumerate(actor_ids)}

    diff_constraints = graph.normalize_to_difference_constraints()

    # Determine maximum forward delay (at least 1 for non-empty graphs to capture actor sequentiality)
    forward_delays = [dc.delay for dc in diff_constraints if dc.delay >= 0]
    max_delay = max(forward_delays + [1 if n > 0 else 0])

    # Initialize matrices A_0, ..., A_max_delay with -infinity
    a_matrices: Dict[int, np.ndarray] = {
        d: mp_zero(n, n) for d in range(max_delay + 1)
    }

    # Intra-actor non-reentrant sequential execution: s_v(k) >= s_v(k-1) + w(v)
    for aid, actor in graph.actors.items():
        idx = actor_to_idx[aid]
        a_matrices[1][idx, idx] = max(a_matrices[1][idx, idx], actor.execution_time)

    backward_inter_constraints: List[NormalizedDifferenceConstraint] = []

    for dc in diff_constraints:
        src_idx = actor_to_idx[dc.src_id]
        dst_idx = actor_to_idx[dc.dst_id]
        weight = dc.weight
        delay = dc.delay

        if delay >= 0:
            # Forward constraint: s_dst(k) >= s_src(k - delay) + weight
            # Matrix entry: (A_delay)[dst_idx, src_idx] = max((A_delay)[dst_idx, src_idx], weight)
            a_matrices[delay][dst_idx, src_idx] = max(a_matrices[delay][dst_idx, src_idx], weight)
        else:
            # Negative delay (inter-iteration upper bound reverse constraint):
            # s_dst(k - |delay|) >= s_src(k) + weight
            backward_inter_constraints.append(dc)

    # Compute Kleene star closure of intra-iteration dependencies: M_0* = (A_0)*
    m0_star, is_feasible = kleene_star(a_matrices[0])

    return StateSpaceMatrices(
        n=n,
        max_delay=max_delay,
        a_matrices=a_matrices,
        m0_star=m0_star,
        is_feasible=is_feasible,
        backward_inter_constraints=backward_inter_constraints,
        actor_to_idx=actor_to_idx,
        idx_to_actor=idx_to_actor,
    )
