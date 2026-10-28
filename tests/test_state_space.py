"""
Unit tests for (max, +) state-space transformation.
"""

import pytest
import numpy as np

from src.model import ExtendedHSDFG, EventType
from src.state_space import transform_extended_hsdfg_to_state_space
from src.maxplus import EPSILON


def test_state_space_simple_pipeline():
    g = ExtendedHSDFG("Pipeline")
    a = g.add_actor("A", 2.0)
    b = g.add_actor("B", 3.0)
    # A -> B (delay 0): s_B(k) >= s_A(k) + 2.0
    g.add_channel(a, b, initial_tokens=0)
    # B -> A (delay 1): s_A(k) >= s_B(k-1) + 3.0
    g.add_channel(b, a, initial_tokens=1)

    ss = transform_extended_hsdfg_to_state_space(g)
    assert ss.is_feasible
    assert ss.n == 2
    assert ss.max_delay == 1

    # In A_0: row b, col a has 2.0
    assert ss.a0[b, a] == 2.0
    assert ss.a0[a, b] == EPSILON

    # In A_1: row a, col b has 3.0
    assert ss.a1[a, b] == 3.0

    # Closure M_0* of A_0:
    # M_0*[b, a] = 2.0, diagonals = 0.0
    assert ss.m0_star[b, a] == 2.0
    assert ss.m0_star[a, a] == 0.0
    assert ss.m0_star[b, b] == 0.0

    # Transition matrix A = M_0* \otimes A_1
    trans = ss.compute_state_transition_matrix()
    assert trans is not None
    # trans[a, b] = M_0*[a, :] \otimes A_1[:, b] = max(0 + 3, eps + eps) = 3.0
    # trans[b, b] = M_0*[b, :] \otimes A_1[:, b] = max(2 + 3, 0 + eps) = 5.0
    assert trans[a, b] == 3.0
    assert trans[b, b] == 5.0

    # Period = 5.0 => Throughput = 1/5 = 0.2
    tp = ss.compute_spectral_throughput()
    assert pytest.approx(tp, rel=1e-5) == 0.2


def test_state_space_infeasible_upper_bound():
    # Intra-iteration lower bound: s_B(k) >= s_A(k) + 5
    # Intra-iteration upper bound: s_B(k) <= s_A(k) + 3 => s_A(k) >= s_B(k) - 3
    # Cycle in A_0: A -> B (5), B -> A (-3). Total weight = 5 - 3 = 2 > 0!
    # Contradiction: s_B cannot be >= s_A + 5 AND <= s_A + 3!
    g = ExtendedHSDFG("Contradiction")
    a = g.add_actor("A", 1.0)
    b = g.add_actor("B", 1.0)
    g.add_lower_bound(a, EventType.START, b, EventType.START, 5.0, delay=0)
    g.add_upper_bound(a, EventType.START, b, EventType.START, 3.0, delay=0)

    ss = transform_extended_hsdfg_to_state_space(g)
    assert not ss.is_feasible


def test_state_space_actor_execution_time_bottleneck():
    # Actor A with execution time 100.0 without manual feedback channel
    # Must have (A_1)_{AA} = 100.0 and spectral throughput = 1/100 = 0.01
    g = ExtendedHSDFG("BottleneckGraph")
    a = g.add_actor("A", 100.0)
    b = g.add_actor("B", 1.0)
    g.add_channel(a, b, initial_tokens=0)

    ss = transform_extended_hsdfg_to_state_space(g)
    assert ss.is_feasible
    assert ss.a1[a, a] == 100.0
    assert ss.a1[b, b] == 1.0
    tp = ss.compute_spectral_throughput()
    assert tp is not None
    assert pytest.approx(tp, rel=1e-5) == 0.01
