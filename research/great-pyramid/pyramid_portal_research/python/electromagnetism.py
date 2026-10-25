"""
electromagnetism.py
===================

Maxwell theory inside the GFD framework.

At level K, the dimension-K^2 tensor product V tensor V decomposes as

    V tensor V = Sym^2(V)  oplus  Lambda^2(V)
    dim:          K(K+1)/2  oplus   K(K-1)/2  =  K^2

At K = 4: 10 oplus 6 = 16. The symmetric piece carries the gravitational
quadratic form g_{mu nu}; the antisymmetric piece carries the Maxwell field
tensor F^{mu nu} as the 6 edges of the tetrahedron K_4.

  - 3 time-space edges (0i for i = 1, 2, 3) carry the electric components E^i
  - 3 space-space edges (ij for 1 <= i < j <= 3) carry the magnetic components B^k

The three perfect matchings of K_4 (the three pairings of opposite edges) give
the basis for the self-dual / anti-self-dual decomposition

    F_pm^{(k)} = (E^k pm i c B^k) / 2

The Hodge star on 2-forms in Lorentzian signature (-+++) squares to -1, giving
the complex structure on Lambda^2(V).

TetA carries the electric field tensor F_e; TetB carries the magnetic dual
F_m = *F. Dirac quantization e * g_mag = n hbar c / 2 follows from the
holonomy of the TetA / TetB pair around a worldsheet boundary.

The framework's Coulomb step alpha^1 is the primitive coupling; gravity is
the composition of 21 such steps via three parity sweeps of seven non-trivial
modes each (Phi_3(4) = 21 = 3 * 7).

References: Active Work 07, project §02.1.
"""

from __future__ import annotations

from itertools import combinations
from typing import Dict, List, Tuple

from .constants import ALPHA, C_LIGHT, HBAR


# =============================================================================
# V tensor V decomposition at level K
# =============================================================================

def vv_decomposition(K: int) -> Dict[str, int]:
    """
    Sym^2 and Lambda^2 dimensions in V tensor V at dim V = K.

        dim Sym^2(V) = K (K+1) / 2
        dim Lambda^2(V) = K (K-1) / 2
        total           = K^2

    At K = 4: (10, 6, 16).
    """
    sym = K * (K + 1) // 2
    anti = K * (K - 1) // 2
    return {
        "K": K,
        "dim_sym2_V":   sym,
        "dim_lambda2_V": anti,
        "total":         sym + anti,
        "check_K_squared": K * K,
    }


# =============================================================================
# Tetrahedral edges of K_K
# =============================================================================

def tetrahedral_edges(K: int) -> List[Tuple[int, int]]:
    """
    All unordered edges (i, j) with 0 <= i < j < K, dimensionally
    K (K-1) / 2.
    """
    return list(combinations(range(K), 2))


def time_space_edges(K: int = 4) -> List[Tuple[int, int]]:
    """
    Time-space edges (0, i) for i = 1 .. K-1. At K = 4: three edges.
    These carry the electric field components E^1, E^2, E^3.
    """
    return [(0, i) for i in range(1, K)]


def space_space_edges(K: int = 4) -> List[Tuple[int, int]]:
    """
    Space-space edges (i, j) for 1 <= i < j < K. At K = 4: three edges.
    These carry the magnetic field components B^1, B^2, B^3 via the
    Hodge dual: B^k = (1/2) epsilon^{kij} F^{ij}.
    """
    return [(i, j) for i in range(1, K) for j in range(i + 1, K)]


def F_mu_nu_basis() -> List[Dict[str, object]]:
    """
    Full basis of Lambda^2(V) at K = 4: six wedge elements indexed by
    (edge, component, type).

    Time-space edges:  E^1 along (0,1), E^2 along (0,2), E^3 along (0,3)
    Space-space edges: B^3 along (1,2), B^2 along (1,3), B^1 along (2,3)
    (using B^k = (1/2) epsilon^{kij} F^{ij}, so B^1 ~ F^{23}, B^2 ~ F^{31}, B^3 ~ F^{12}).
    """
    return [
        {"edge": (0, 1), "component": "E^1", "type": "electric"},
        {"edge": (0, 2), "component": "E^2", "type": "electric"},
        {"edge": (0, 3), "component": "E^3", "type": "electric"},
        {"edge": (2, 3), "component": "B^1", "type": "magnetic"},  # eps^{1 2 3} F^{23}
        {"edge": (1, 3), "component": "B^2", "type": "magnetic"},  # eps^{2 3 1} F^{31}
        {"edge": (1, 2), "component": "B^3", "type": "magnetic"},  # eps^{3 1 2} F^{12}
    ]


# =============================================================================
# Perfect matchings of K_4
# =============================================================================

def perfect_matchings_K4() -> List[List[Tuple[Tuple[int, int], Tuple[int, int]]]]:
    """
    The three perfect matchings of K_4: each pairs the six edges into three
    opposite pairs of disjoint edges.

    The three matchings are:
      M_1: {(0,1), (2,3)}, paired with the other two pairings closing in K_4
      M_2: {(0,2), (1,3)}
      M_3: {(0,3), (1,2)}

    Each matching is a partition of the 4 vertices into 2 disjoint edges.
    """
    return [
        [((0, 1), (2, 3))],
        [((0, 2), (1, 3))],
        [((0, 3), (1, 2))],
    ]


def opposite_edge_pairs_K4() -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    The three opposite-edge pairs of K_4. Each pair consists of an E-edge and
    its dual B-edge, giving the natural (E^k, B^k) pairing:

        (0,1) <-> (2,3)   E^1 paired with B^1
        (0,2) <-> (1,3)   E^2 paired with B^2
        (0,3) <-> (1,2)   E^3 paired with B^3
    """
    return [
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    ]


# =============================================================================
# Self-dual / anti-self-dual decomposition
# =============================================================================

def self_dual_part(E_k: complex, B_k: complex, c: float = 1.0) -> complex:
    """
    Self-dual projection of the k-th component:
        F_+^(k) = (E^k + i c B^k) / 2

    The three F_+^(k) for k = 1, 2, 3 span the 3-dim self-dual subspace of
    Lambda^2(V).
    """
    return (E_k + 1j * c * B_k) / 2.0


def anti_self_dual_part(E_k: complex, B_k: complex, c: float = 1.0) -> complex:
    """
    Anti-self-dual projection of the k-th component:
        F_-^(k) = (E^k - i c B^k) / 2
    """
    return (E_k - 1j * c * B_k) / 2.0


def self_dual_anti_self_dual_decomposition(
    E: Tuple[complex, complex, complex],
    B: Tuple[complex, complex, complex],
    c: float = 1.0,
) -> Dict[str, Tuple[complex, complex, complex]]:
    """
    Full decomposition F = F_+ + F_- on each of the three matchings.

    F_+^(k) = (E^k + i c B^k) / 2
    F_-^(k) = (E^k - i c B^k) / 2

    Verification: F_+^(k) + F_-^(k) = E^k and (F_+^(k) - F_-^(k)) / i = c B^k.
    """
    F_plus = tuple(self_dual_part(E[k], B[k], c) for k in range(3))
    F_minus = tuple(anti_self_dual_part(E[k], B[k], c) for k in range(3))
    return {"F_plus": F_plus, "F_minus": F_minus}


def hodge_star_squared_lorentzian() -> int:
    """
    In 4D Lorentzian signature (-+++) the Hodge star on 2-forms satisfies
    ** = -1, giving Lambda^2(V) the structure of a complex 3-dimensional
    vector space with complex structure J = *.
    """
    return -1


# =============================================================================
# Dirac quantization
# =============================================================================

def dirac_quantization_check(
    e_charge: float,
    g_magnetic_charge: float,
    n: int,
    hbar: float = HBAR,
    c: float = C_LIGHT,
    tol: float = 1e-9,
) -> Dict[str, object]:
    """
    Dirac quantization condition:
        e * g_magnetic = n * hbar * c / 2  for integer n.

    In the framework, TetA carries electric charges and TetB carries magnetic
    charges; the quantization condition follows from the holonomy of the
    TetA/TetB exchange around a closed worldsheet boundary.
    """
    lhs = e_charge * g_magnetic_charge
    rhs = n * hbar * c / 2.0
    relative_error = abs(lhs - rhs) / abs(rhs) if rhs != 0 else float("inf")
    return {
        "e_times_g_magnetic":    lhs,
        "n_hbar_c_over_2":       rhs,
        "n":                     n,
        "satisfied":             relative_error < tol,
        "relative_error":        relative_error,
    }


# =============================================================================
# Coulomb step as framework primitive
# =============================================================================

def coulomb_step(alpha: float = ALPHA) -> float:
    """
    The framework's primitive coupling step: alpha^1.

    This is the bare Coulomb amplitude, the K=0 / K=1 row of the Sierpinski
    hierarchy. Gravity at K=4 is the composition of 21 such steps with the
    tetrad-impedance and Hopf-fiber factors.
    """
    return alpha


def gravity_as_21_coulomb_steps(alpha: float = ALPHA) -> Dict[str, object]:
    """
    Decomposition of alpha^21 as three parity sweeps of seven non-trivial
    modes each:

        Phi_3(4) = 21 = 3 * 7

    Three sweeps correspond to the three parity sectors (TetA, mixed, TetB);
    each sweep contributes seven mode amplitudes (the seven non-trivial
    elements of Z/7 in the Grand Gallery decoration), yielding alpha^7 per
    sweep. The full coupling is alpha^(3*7) = alpha^21.
    """
    seven_per_sweep = alpha ** 7
    three_sweeps = seven_per_sweep ** 3
    return {
        "alpha_per_step":          alpha,
        "modes_per_sweep":         7,
        "sweeps":                  3,
        "alpha_per_sweep":         seven_per_sweep,
        "alpha_composite_3_sweeps": three_sweeps,
        "alpha_to_21":             alpha ** 21,
        "match":                   abs(three_sweeps - alpha ** 21) < 1e-58,
    }
