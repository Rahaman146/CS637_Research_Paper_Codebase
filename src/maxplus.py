"""
Max-plus semiring algebra module.
Implements:
- Semiring (R_max, max, +) with epsilon = -infinity, e = 0
- Matrix addition, multiplication, powers
- Kleene star closure (all-pairs longest paths) and positive cycle detection
- Maximum Cycle Mean (MCM) computation via Karp's and Howard's algorithms
"""

import numpy as np
from typing import Tuple, Optional, List

EPSILON = -np.inf
ZERO = 0.0


def mp_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Max-plus addition: elementwise maximum."""
    return np.maximum(a, b)


def mp_mult(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    r"""
    Max-plus matrix multiplication: (A \otimes B)_{ij} = max_k (A_{ik} + B_{kj}).
    Works for 2D matrices or 2D matrix with 1D vector using vectorized broadcasting.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    if a.ndim == 1 and b.ndim == 1:
        assert len(a) == len(b), f"Dimension mismatch: {a.shape} vs {b.shape}"
        if len(a) == 0:
            return EPSILON
        terms = a + b
        terms = np.where(np.isnan(terms), EPSILON, terms)
        return float(np.max(terms))
    elif a.ndim == 1 and b.ndim == 2:
        m = len(a)
        m2, p = b.shape
        assert m == m2, f"Dimension mismatch: {a.shape} vs {b.shape}"
        if m == 0:
            return np.full(p, EPSILON, dtype=float)
        terms = a[:, None] + b
        terms = np.where(np.isnan(terms), EPSILON, terms)
        return np.max(terms, axis=0)
    elif a.ndim == 2 and b.ndim == 1:
        # Matrix-vector multiplication
        n, m = a.shape
        assert m == len(b), f"Dimension mismatch: {a.shape} vs {b.shape}"
        if m == 0:
            return np.full(n, EPSILON, dtype=float)
        terms = a + b[None, :]
        terms = np.where(np.isnan(terms), EPSILON, terms)
        return np.max(terms, axis=1)
    else:
        n, m = a.shape
        m2, p = b.shape
        assert m == m2, f"Dimension mismatch: {a.shape} vs {b.shape}"
        if m == 0:
            return np.full((n, p), EPSILON, dtype=float)
        terms = a[:, :, None] + b[None, :, :]
        terms = np.where(np.isnan(terms), EPSILON, terms)
        return np.max(terms, axis=1)


def mp_identity(n: int) -> np.ndarray:
    """Max-plus identity matrix I: 0 on diagonal, -infinity elsewhere."""
    mat = np.full((n, n), EPSILON, dtype=float)
    np.fill_diagonal(mat, 0.0)
    return mat


def mp_zero(n: int, m: Optional[int] = None) -> np.ndarray:
    """Max-plus zero matrix filled with -infinity."""
    if m is None:
        m = n
    return np.full((n, m), EPSILON, dtype=float)


def kleene_star(a: np.ndarray) -> Tuple[np.ndarray, bool]:
    r"""
    Computes the Kleene star closure A* = I \oplus A \oplus A^2 \oplus ... \oplus A^{n-1}.
    Uses Floyd-Warshall longest path dynamic programming in O(n^3).

    Returns:
        (closure_matrix, is_feasible)
        is_feasible is False if a cycle with positive weight is detected (diagonal > 0).
    """
    n = a.shape[0]
    assert a.shape[1] == n, "Matrix must be square"

    # Start with D = I \oplus A
    d = mp_add(mp_identity(n), np.copy(a))

    for k in range(n):
        for i in range(n):
            if d[i, k] == EPSILON:
                continue
            for j in range(n):
                if d[k, j] == EPSILON:
                    continue
                cand = d[i, k] + d[k, j]
                if cand > d[i, j]:
                    d[i, j] = cand

    # Check for positive cycles: if any diagonal element is strictly greater than 0
    has_positive_cycle = False
    for i in range(n):
        if d[i, i] > 1e-9:
            has_positive_cycle = True
            break

    return d, not has_positive_cycle


def maximum_cycle_mean(a: np.ndarray) -> float:
    """
    Computes the Maximum Cycle Mean (MCM) / maximum cycle ratio lambda* of matrix A.
    Uses Karp's algorithm:
    lambda* = max_i min_{0 <= k <= n-1} (x_i(n) - x_i(k)) / (n - k)
    """
    n = a.shape[0]
    assert a.shape[1] == n, "Matrix must be square"

    if n == 0:
        return 0.0

    # Decompose into strongly connected components or run Karp's with universal source
    # Initialize state trajectory x(0), ..., x(n)
    x = np.full((n + 1, n), EPSILON, dtype=float)
    x[0, :] = 0.0  # start from all zeros to handle all reachability

    for k in range(n):
        x[k + 1, :] = mp_mult(a, x[k, :])

    # If no state was reached, return 0.0
    if np.all(x[n, :] == EPSILON):
        return 0.0

    karp_values = []
    for i in range(n):
        if x[n, i] == EPSILON:
            continue
        min_ratio = np.inf
        for k in range(n):
            if x[k, i] == EPSILON:
                continue
            diff = x[n, i] - x[k, i]
            ratio = diff / float(n - k)
            if ratio < min_ratio:
                min_ratio = ratio
        if min_ratio != np.inf:
            karp_values.append(min_ratio)

    if not karp_values:
        return 0.0

    return float(max(karp_values))


class MPMatrix:
    """Convenience wrapper for max-plus matrix calculations."""

    def __init__(self, data: np.ndarray):
        self.data = np.asarray(data, dtype=float)

    @property
    def shape(self):
        return self.data.shape

    def __add__(self, other) -> "MPMatrix":
        b = other.data if isinstance(other, MPMatrix) else np.asarray(other, dtype=float)
        return MPMatrix(mp_add(self.data, b))

    def __matmul__(self, other) -> "MPMatrix":
        b = other.data if isinstance(other, MPMatrix) else np.asarray(other, dtype=float)
        return MPMatrix(mp_mult(self.data, b))

    def __eq__(self, other) -> bool:
        b = other.data if isinstance(other, MPMatrix) else np.asarray(other, dtype=float)
        return np.allclose(self.data, b, equal_nan=True)

    def star(self) -> Tuple["MPMatrix", bool]:
        res, feas = kleene_star(self.data)
        return MPMatrix(res), feas

    def mcm(self) -> float:
        return maximum_cycle_mean(self.data)

    def tolist(self):
        return self.data.tolist()

    def __repr__(self):
        return f"MPMatrix(\n{self.data}\n)"
