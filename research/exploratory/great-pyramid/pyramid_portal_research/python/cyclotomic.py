"""
cyclotomic.py
=============

Cyclotomic shell algebra:

  - Phi_3(K), Phi_4(K), Phi_6(K) — the three degree-2 cyclotomic polynomials
  - The shell C_K = (Phi_6, Phi_4, Phi_3) at level K
  - Shift identity: Phi_3(K) = Phi_6(K+1)
  - Scale fusion: Phi_3(K) * Phi_6(K) = Phi_3(K^2)
  - Coupling polynomial f(K, s) = K^2 + sK + 1
  - The parity-character lift s = 2 cos(theta) with three Niven readings

References: Active Work 03–04 (parity-character upgrade, core theory integration).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gamma, pi
from typing import Dict, Tuple


# =============================================================================
# Degree-2 cyclotomic polynomials
# =============================================================================

def phi3(K: int) -> int:
    """Phi_3(K) = K^2 + K + 1. Upper / union / total-dimension channel."""
    return K * K + K + 1


def phi4(K: int) -> int:
    """Phi_4(K) = K^2 + 1. Neutral / even-dimension / parity-even channel."""
    return K * K + 1


def phi6(K: int) -> int:
    """Phi_6(K) = K^2 - K + 1. Lower / overlap / superdimension channel."""
    return K * K - K + 1


def coupling_polynomial(K: int, s: int | float) -> int | float:
    """f(K, s) = K^2 + s*K + 1."""
    return K * K + s * K + 1


# =============================================================================
# The shell object
# =============================================================================

@dataclass(frozen=True)
class Shell:
    """Three-band shell C_K = (Phi_6(K), Phi_4(K), Phi_3(K))."""
    K: int
    lower: int
    neutral: int
    upper: int

    @property
    def tuple(self) -> Tuple[int, int, int]:
        return (self.lower, self.neutral, self.upper)

    @property
    def step(self) -> int:
        """The equal step E_K - C_K = K, also U_K - E_K = K."""
        return self.neutral - self.lower

    @property
    def parity_decomposition(self) -> str:
        return f"{self.upper} = {self.lower} + {self.K} + {self.K}"


def shell(K: int) -> Shell:
    """Construct the shell at level K."""
    return Shell(K=K, lower=phi6(K), neutral=phi4(K), upper=phi3(K))


# =============================================================================
# Cyclotomic identities
# =============================================================================

def shift_identity(K: int) -> Dict[str, object]:
    """
    Cyclotomic shift identity:
        Phi_3(K) = Phi_6(K+1)

    The pyramid hinge sits at K=4:
        Phi_3(4) = 21 = Phi_6(5)
    """
    left = phi3(K)
    right = phi6(K + 1)
    return {"K": K, "Phi3_K": left, "Phi6_K_plus_1": right, "holds": left == right}


def scale_fusion_identity(K: int) -> Dict[str, object]:
    """
    Sierpinski / scale-fusion identity:
        Phi_3(K) * Phi_6(K) = Phi_3(K^2)

    This lifts the closure-read at level K to level K^2.
    At K=4: 21 * 13 = 273 = Phi_3(16).
    """
    left = phi3(K) * phi6(K)
    right = phi3(K * K)
    return {"K": K, "Phi3_times_Phi6": left, "Phi3_K_squared": right, "holds": left == right}


# =============================================================================
# Math utilities used across modules
# =============================================================================

def sphere_surface_area_unit(n: int) -> float:
    """
    Surface area of the unit n-sphere S^n embedded in R^{n+1}:
        Area(S^n) = 2 * pi^((n+1)/2) / Gamma((n+1)/2)

    Direct values are returned for small n to avoid scipy dependence.
    """
    if n == 0:
        return 2.0
    if n == 1:
        return 2 * pi
    if n == 2:
        return 4 * pi
    if n == 3:
        return 2 * pi * pi
    return 2 * (pi ** ((n + 1) / 2)) / gamma((n + 1) / 2)


# =============================================================================
# Niven rigidity and norm-form lift  [Active Work 04]
# =============================================================================

def niven_rigidity_check() -> Dict[str, object]:
    """
    Niven's theorem applied to the parity-character lift s = 2 cos(theta):
    the only rational s in [-1, +1] for which theta is a rational multiple
    of pi are s in {-1, 0, +1}.

    These correspond to rotation orders n in {3, 4, 6}, i.e., the only
    positive integers with phi(n) = 2 and therefore the only degree-2
    cyclotomic polynomials. The framework's three discrete readings exhaust
    this Niven non-trivial set.
    """
    return {
        "theorem": "Niven (1956)",
        "statement": (
            "rational values of cos(theta) at rational theta/pi are "
            "{0, +/-1/2, +/-1}; therefore 2*cos(theta) in {0, +/-1, +/-2}"
        ),
        "framework_domain": "|s| <= 1 (parity-character non-degenerate)",
        "integer_s_in_domain": [-1, 0, +1],
        "orders_n": {-1: 3, 0: 4, +1: 6},
        "phi_n_values": {3: 2, 4: 2, 6: 2},
        "cyclotomic_polynomials": {
            3: "Phi_6(K) = K^2 - K + 1",
            4: "Phi_4(K) = K^2 + 1",
            6: "Phi_3(K) = K^2 + K + 1",
        },
        "boundary_points_excluded": {
            -2: "trivial half-turn theta=pi, (K-1)^2, no rotational content",
            +2: "trivial rotation theta=0, (K+1)^2, no rotational content",
        },
        "conclusion": (
            "framework's three readings s in {-1, 0, +1} are the unique "
            "non-degenerate Niven integers in [-1, +1]"
        ),
    }


def norm_form(K: int, theta: float) -> float:
    """
    Coupling polynomial via algebraic norm:
        f(K, s) = |K + e^{i*theta}|^2 = K^2 + 2*K*cos(theta) + 1

    with s = 2*cos(theta). Evaluating at the three Niven angles
    theta in {pi/3, pi/2, 2*pi/3} recovers (Phi_3, Phi_4, Phi_6) at K.
    """
    from math import cos as _cos
    return K * K + 2 * K * _cos(theta) + 1


def cyclotomic_integer_norm(K: int, n: int) -> int:
    """
    Norm of the cyclotomic integer (K + zeta_n) in Z[zeta_n] for n in {3, 4, 6}:

        n = 3: N(K + zeta_3) = K^2 - K + 1 = Phi_6(K)   (Eisenstein)
        n = 4: N(K + zeta_4) = K^2 + 1     = Phi_4(K)   (Gaussian)
        n = 6: N(K + zeta_6) = K^2 + K + 1 = Phi_3(K)   (Eisenstein)

    These are the three K=4 closure-read traces (13, 17, 21) realized as norms
    of specific algebraic integers in cyclotomic rings of degree 2.
    """
    if n == 3:
        return phi6(K)
    if n == 4:
        return phi4(K)
    if n == 6:
        return phi3(K)
    raise ValueError(
        f"n must be in {{3, 4, 6}} (the orders with phi(n) = 2); got n={n}"
    )


def niven_partition_table(K: int) -> Dict[int, Dict[str, object]]:
    """
    The three interior Niven readings at level K.

    Each reading s in {-1, 0, +1} carries:
      - corresponding rotation angle theta
      - the rotation order n with phi(n) = 2
      - the cyclotomic polynomial value Phi_n(K)
      - the cyclotomic ring Z[zeta_n] identification
    """
    from math import pi as _pi
    return {
        -1: {
            "theta": 2 * _pi / 3,
            "order_n": 3,
            "polynomial": "Phi_6(K)",
            "value_at_K": phi6(K),
            "ring": "Z[zeta_3] (Eisenstein integers)",
        },
        0: {
            "theta": _pi / 2,
            "order_n": 4,
            "polynomial": "Phi_4(K)",
            "value_at_K": phi4(K),
            "ring": "Z[i] (Gaussian integers)",
        },
        +1: {
            "theta": _pi / 3,
            "order_n": 6,
            "polynomial": "Phi_3(K)",
            "value_at_K": phi3(K),
            "ring": "Z[zeta_6] = Z[zeta_3] (Eisenstein integers)",
        },
    }
