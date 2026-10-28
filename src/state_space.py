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
    ):
        self.n = n
        self.max_delay = max_delay
        self.a_matrices = a_matrices  # d -> A_d (n x n)
        self.m0_star = m0_star        # (n x n) Kleene star of A_0
        self.is_feasible = is_feasible
        self.backward_inter_constraints = backward_inter_constraints

    @property
    def a0(self) -> np.ndarray:
        return self.a_matrices[0]

    @property
    def a1(self) -> Optional[np.ndarray]:
        return self.a_matrices.get(1, None)

    def compute_state_transition_matrix(self) -> Optional[np.ndarray]:
        r"""
        For systems with maximum delay D=1:
        Computes A = M_0^* \otimes A_1.
        """
        if not self.is_feasible or 1 not in self.a_matrices:
            return None
        return mp_mult(self.m0_star, self.a_matrices[1])

    def compute_spectral_throughput(self) -> Optional[float]:
        r"""
        Computes throughput via Maximum Cycle Mean (MCM) on A = M_0^* \otimes A_1.
        Throughput = 1 / lambda*
        """
        trans = self.compute_state_transition_matrix()
        if trans is None:
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
    - Actor execution times w(u)
    - Token delays on channels
    - Normalized lower-bound constraints
    - Intra-iteration upper-bound backward arcs inserted into A_0
    - Multi-iteration backward constraints tracked for global unrolled synthesis
    """
    n = graph.num_actors
    if n == 0:
        return StateSpaceMatrices(0, 0, {0: mp_identity(0)}, mp_identity(0), True, [])

    diff_constraints = graph.normalize_to_difference_constraints()

    # Determine maximum forward delay (at least 1 for non-empty graphs to capture actor sequentiality)
    max_delay = max([dc.delay for dc in diff_constraints] + [1 if n > 0 else 0])

    # Initialize matrices A_0, ..., A_max_delay with -infinity
    a_matrices: Dict[int, np.ndarray] = {
        d: mp_zero(n, n) for d in range(max_delay + 1)
    }

    # Intra-actor non-reentrant sequential execution: s_v(k) >= s_v(k-1) + w(v)
    for aid, actor in graph.actors.items():
        if aid < n:
            a_matrices[1][aid, aid] = max(a_matrices[1][aid, aid], actor.execution_time)

    backward_inter_constraints: List[NormalizedDifferenceConstraint] = []

    for dc in diff_constraints:
        src = dc.src_id
        dst = dc.dst_id
        weight = dc.weight
        delay = dc.delay

        if delay >= 0:
            # Forward constraint: s_dst(k) >= s_src(k - delay) + weight
            # Matrix entry: (A_delay)[dst, src] = max((A_delay)[dst, src], weight)
            a_matrices[delay][dst, src] = max(a_matrices[delay][dst, src], weight)
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
    )
