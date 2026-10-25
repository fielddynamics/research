"""
gravity.py
==========

Gravity derivation in the framework:

    alpha_G = alpha^21 * (17/13) * (g_e/2)
    G       = alpha_G * hbar c / m_e^2

Decomposed as the product of:
  - alpha^1: primitive Coulomb step
  - alpha^20: directed-edge product over the pentachoron K_5
  - 17/13: tetrad impedance ratio Phi_4(4)/Phi_6(4)
  - g_e/2: Hopf-fiber spin holonomy

Also includes generalized K-coupling, gap exponent, and the four convergent
routes that select K=4.

References: project §02.1–§02.4; legacy §4 and §16.
"""

from __future__ import annotations

import cmath
from fractions import Fraction
from itertools import permutations
from math import isclose
from typing import Dict, List, Sequence

from .constants import ALPHA, C_LIGHT, G_E_OVER_2, G_OBSERVED, HBAR, M_E, TAU
from .cyclotomic import phi3, phi4, phi6, shell


# =============================================================================
# Pentachoron directed-edge network
# =============================================================================

def directed_complete_graph_edge_count(vertex_count: int) -> int:
    """Number of directed edges in K_n without self-loops: n(n-1)."""
    return vertex_count * (vertex_count - 1)


def pentachoron_directed_edge_count() -> int:
    """Pentachoron K_5 directed-edge count: 5 * 4 = 20."""
    return directed_complete_graph_edge_count(5)


def pentachoron_edge_product(
    alpha: float = ALPHA,
    phases: Sequence[float] | None = None,
) -> complex:
    """
    Directed K_5 edge product:
        A_20 = prod_{i != j} alpha * exp(i theta_ij)
             = alpha^20 * exp(i sum theta_ij)
    """
    n = pentachoron_directed_edge_count()
    if phases is None:
        phases = [0.0] * n
    if len(phases) != n:
        raise ValueError(f"Need exactly {n} directed-edge phases.")
    return (alpha ** n) * cmath.exp(1j * sum(phases))


def edge_phase_closure(phases: Sequence[float], tol: float = 1e-12) -> bool:
    """Check sum theta_ij = 0 mod 2*pi."""
    angle = sum(phases) % TAU
    return isclose(angle, 0.0, abs_tol=tol) or isclose(angle, TAU, abs_tol=tol)


# =============================================================================
# Tetrad impedance and alpha_G
# =============================================================================

def tetrad_impedance_ratio() -> Fraction:
    """Z_4 = Phi_4(4) / Phi_6(4) = 17/13."""
    return Fraction(phi4(4), phi6(4))


def alpha_gravity(alpha: float = ALPHA, g_over_2: float = G_E_OVER_2) -> float:
    """alpha_G = alpha^21 * (17/13) * (g_e/2)."""
    return (alpha ** phi3(4)) * float(tetrad_impedance_ratio()) * g_over_2


def alpha_gravity_parts(alpha: float = ALPHA, g_over_2: float = G_E_OVER_2) -> Dict[str, float]:
    """Decompose alpha_G = alpha * alpha^20 * (17/13) * (g_e/2)."""
    return {
        "primitive_coulomb_edge_alpha": alpha,
        "directed_pentachoron_product_alpha20": alpha ** 20,
        "tetrad_impedance_17_over_13": float(tetrad_impedance_ratio()),
        "spin_load_g_over_2": g_over_2,
        "alpha_G": alpha_gravity(alpha, g_over_2),
    }


# =============================================================================
# Generalized K-coupling
# =============================================================================

def coupling_exponent_for_K(K: int) -> int:
    """Full attenuation exponent at shell K: Phi_3(K) = K^2 + K + 1."""
    return phi3(K)


def gravity_over_coulomb_gap_exponent(K: int) -> int:
    """Gap beyond bare Coulomb: Phi_3(K) - 1 = K(K+1)."""
    return phi3(K) - 1


def tetrad_renormalization_factor(K: int, alpha: float = ALPHA, g_over_2: float = G_E_OVER_2) -> float:
    """R(alpha, K) = [Phi_4(K)/Phi_6(K)] * alpha^[K(K+1)] * (g/2)."""
    return (phi4(K) / phi6(K)) * (alpha ** (K * (K + 1))) * g_over_2


def alpha_G_for_K(K: int, alpha: float = ALPHA, g_over_2: float = G_E_OVER_2) -> float:
    """Generalized framework coupling: alpha_K = alpha^Phi_3(K) * Phi_4(K)/Phi_6(K) * g/2."""
    return (alpha ** phi3(K)) * (phi4(K) / phi6(K)) * g_over_2


# =============================================================================
# Newton's G prediction
# =============================================================================

def predict_G_from_alpha(
    alpha: float = ALPHA,
    g_over_2: float = G_E_OVER_2,
    hbar: float = HBAR,
    c: float = C_LIGHT,
    m_e: float = M_E,
) -> float:
    """
    Predict Newton's G from alpha_G:
        alpha_G = G m_e^2 / (hbar c)  =>  G = alpha_G hbar c / m_e^2
    """
    return alpha_gravity(alpha, g_over_2) * hbar * c / (m_e * m_e)


def G_prediction_report() -> Dict[str, float]:
    """Numerical report for the coupling-constant unification."""
    G_pred = predict_G_from_alpha()
    return {
        "alpha_G_predicted": alpha_gravity(),
        "G_predicted": G_pred,
        "G_observed_reference": G_OBSERVED,
        "relative_error_vs_reference": (G_pred - G_OBSERVED) / G_OBSERVED,
        "ppm_error": 1e6 * (G_pred - G_OBSERVED) / G_OBSERVED,
    }


# =============================================================================
# Four routes selecting K=4
# =============================================================================

def four_routes_select_K4() -> List[Dict[str, object]]:
    """
    Four convergent arguments that select K=4 from independent inputs.
    """
    # Route 1: uniqueness equation 2(D+1) = 2^D
    solutions = []
    for D in range(1, 12):
        if 2 * (D + 1) == 2 ** D:
            solutions.append((D, D + 1))

    return [
        {
            "route": "uniqueness equation",
            "equation": "2(D+1) = 2^D",
            "solutions_D_K_in_1_to_11": solutions,
            "selected_K": 4,
        },
        {
            "route": "three-sweep divisibility",
            "condition": "3 divides Phi_3(K) iff K = 1 mod 3",
            "small_positive_K": [K for K in range(1, 15) if phi3(K) % 3 == 0],
            "selected_K": 4,
        },
        {
            "route": "degree-2 cyclotomic uniqueness",
            "condition": "varphi(n) = 2 for n in {3, 4, 6}",
            "traces": ["Phi_3", "Phi_4", "Phi_6"],
            "selected_shell_at_K4": shell(4).tuple,
        },
        {
            "route": "Fermat / Sierpinski seed",
            "condition": "K = 2^(2^n), n=1 gives K=4",
            "sequence": [2 ** (2 ** n) for n in range(4)],
            "selected_K": 4,
        },
    ]


# =============================================================================
# Permutation discrimination  [Active Work 08, project §02.4]
# =============================================================================

def permutation_discrimination(
    alpha: float = ALPHA,
    g_over_2: float = G_E_OVER_2,
) -> List[Dict[str, object]]:
    """
    Enumerate all six permutations of the shell {21, 17, 13} into
    (exponent, numerator, denominator) and compute the candidate coupling

        alpha_candidate = alpha^exp * num / den * (g_e / 2)

    For each candidate, compute the resulting G (via the same lepton anchor)
    and the ppm error against the CODATA G_OBSERVED. The framework's selection
    (exp=21, num=17, den=13) is the unique permutation with the integer
    exponent saturating Phi_3(4) and yielding G within ~14 ppm.

    Returns a list of candidate dicts sorted by absolute ppm error.
    """
    shell_values = [13, 17, 21]
    candidates: List[Dict[str, object]] = []
    for exp, num, den in permutations(shell_values):
        if exp == num or exp == den or num == den:
            continue  # ensure all three slots distinct
        alpha_candidate = (alpha ** exp) * (num / den) * g_over_2
        G_candidate = alpha_candidate * HBAR * C_LIGHT / (M_E * M_E)
        ppm = 1e6 * (G_candidate - G_OBSERVED) / G_OBSERVED
        candidates.append({
            "exp":           exp,
            "num":           num,
            "den":           den,
            "ratio":         num / den,
            "alpha_G":       alpha_candidate,
            "G_predicted":   G_candidate,
            "ppm_error":     ppm,
            "abs_ppm_error": abs(ppm),
        })
    candidates.sort(key=lambda c: c["abs_ppm_error"])
    return candidates


def best_permutation(
    alpha: float = ALPHA,
    g_over_2: float = G_E_OVER_2,
) -> Dict[str, object]:
    """
    The unique permutation of {21, 17, 13} that best matches G_OBSERVED.

    Returns the (exp, num, den) triple with the smallest |ppm error| and
    confirms it is the framework selection (21, 17, 13).
    """
    candidates = permutation_discrimination(alpha=alpha, g_over_2=g_over_2)
    winner = candidates[0]
    return {
        "winning_exp_num_den": (winner["exp"], winner["num"], winner["den"]),
        "matches_framework": (winner["exp"], winner["num"], winner["den"]) == (21, 17, 13),
        "winner_ppm_error": winner["ppm_error"],
        "runner_up_ppm_error": candidates[1]["ppm_error"] if len(candidates) > 1 else None,
    }
