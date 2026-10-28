"""
Unit tests for max-plus semiring algebra.
"""

import pytest
import numpy as np

from src.maxplus import (
    EPSILON,
    mp_add,
    mp_mult,
    mp_identity,
    mp_zero,
    kleene_star,
    maximum_cycle_mean,
    MPMatrix,
)


def test_maxplus_addition():
    a = np.array([[1.0, 5.0], [EPSILON, 3.0]])
    b = np.array([[2.0, 4.0], [0.0, EPSILON]])
    c = mp_add(a, b)
    expected = np.array([[2.0, 5.0], [0.0, 3.0]])
    assert np.allclose(c, expected)


def test_maxplus_multiplication():
    # In max-plus: (A \otimes B)_ij = max_k (A_ik + B_kj)
    a = np.array([[2.0, 3.0], [EPSILON, 1.0]])
    b = np.array([[1.0, EPSILON], [4.0, 2.0]])
    # (0,0): max(2+1, 3+4) = max(3, 7) = 7
    # (0,1): max(2+eps, 3+2) = 5
    # (1,0): max(eps+1, 1+4) = 5
    # (1,1): max(eps+eps, 1+2) = 3
    c = mp_mult(a, b)
    expected = np.array([[7.0, 5.0], [5.0, 3.0]])
    assert np.allclose(c, expected)


def test_maxplus_identity_and_zero():
    n = 3
    eye = mp_identity(n)
    zero = mp_zero(n)
    a = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])

    # A \otimes I = A
    assert np.allclose(mp_mult(a, eye), a)
    # I \otimes A = A
    assert np.allclose(mp_mult(eye, a), a)
    # A \oplus 0 = A
    assert np.allclose(mp_add(a, zero), a)


def test_kleene_star_dag():
    # DAG: 0 -> 1 (wt 3), 1 -> 2 (wt 4)
    # Paths: 0->0: 0, 1->1: 0, 2->2: 0, 0->1: 3, 1->2: 4, 0->2: 7
    a = np.full((3, 3), EPSILON)
    a[1, 0] = 3.0
    a[2, 1] = 4.0

    a_star, is_feasible = kleene_star(a)
    assert is_feasible
    assert a_star[0, 0] == 0.0
    assert a_star[1, 1] == 0.0
    assert a_star[2, 2] == 0.0
    assert a_star[1, 0] == 3.0
    assert a_star[2, 1] == 4.0
    assert a_star[2, 0] == 7.0
    assert a_star[0, 1] == EPSILON


def test_kleene_star_positive_cycle():
    # Cycle: 0 -> 1 (wt 2), 1 -> 0 (wt 3) => cycle weight 5 > 0
    a = np.full((2, 2), EPSILON)
    a[1, 0] = 2.0
    a[0, 1] = 3.0

    _, is_feasible = kleene_star(a)
    assert not is_feasible


def test_maximum_cycle_mean():
    # Simple 2-node cycle with weight 6 across 2 hops => MCM = 3.0
    # x(k+1) = A \otimes x(k)
    a = np.full((2, 2), EPSILON)
    a[0, 1] = 4.0
    a[1, 0] = 2.0
    mcm = maximum_cycle_mean(a)
    assert pytest.approx(mcm, rel=1e-5) == 3.0


def test_mpmatrix_wrapper():
    a = MPMatrix(np.array([[1.0, 2.0], [3.0, 4.0]]))
    b = MPMatrix(np.array([[0.0, 5.0], [2.0, 1.0]]))
    c = a + b
    assert np.allclose(c.data, np.array([[1.0, 5.0], [3.0, 4.0]]))
