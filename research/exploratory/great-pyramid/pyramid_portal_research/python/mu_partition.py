"""
mu_partition.py
===============

GFD gravitational partition:

    mu(x) = x / (x + 1)         TetA share
    1 - mu(x) = 1 / (x + 1)     TetB share
    mu / (1 - mu) = x = g / a_0  odds ratio

Plus the Born-rule map mu = (1 + cos(theta)) / 2 connecting the parity-character
angle (from the closure-read) to the gravitational partition. Under this map,
the three Niven readings of the parity character correspond to three specific
gravitational regimes:

    s = -1  <->  theta = 2 pi / 3  <->  mu = 1/4  <->  x = 1/3   (sub-transition)
    s =  0  <->  theta =  pi / 2   <->  mu = 1/2  <->  x = 1     (MOND transition,
                                                                  g = a_0)
    s = +1  <->  theta =  pi / 3   <->  mu = 3/4  <->  x = 3     (super-transition)

The middle reading at the MOND transition is forced by parity-even =
exchange-invariance.

References: Active Work 05, project §02.1 / framework foundations.
"""

from __future__ import annotations

from math import cos, isclose, pi, sqrt
from typing import Dict, List

from .cyclotomic import niven_partition_table


# =============================================================================
# Constitutive law: mu(x)
# =============================================================================

def mu(x: float) -> float:
    """TetA share: mu(x) = x / (x + 1)."""
    return x / (x + 1.0)


def tetA_share(x: float) -> float:
    """TetA share is mu(x)."""
    return mu(x)


def tetB_share(x: float) -> float:
    """TetB share: 1 - mu(x) = 1 / (x + 1)."""
    return 1.0 / (x + 1.0)


def odds_ratio(x: float) -> float:
    """
    Odds ratio of the partition: mu / (1 - mu) = x.

    The dimensionless acceleration x = g / a_0 is exactly the TetA:TetB
    odds ratio.
    """
    m = mu(x)
    return m / (1.0 - m)


# =============================================================================
# Logistic identity
# =============================================================================

def mu_derivative(x: float) -> float:
    """dmu/dx = 1 / (x + 1)^2."""
    return 1.0 / ((x + 1.0) ** 2)


def logistic_identity_check(x: float, tol: float = 1e-12) -> bool:
    """
    Logistic identity:
        x * dmu/dx = mu(x) * (1 - mu(x))

    Equivalent to the substrate equation governing the partition flow under
    log-acceleration.
    """
    lhs = x * mu_derivative(x)
    rhs = mu(x) * (1.0 - mu(x))
    return abs(lhs - rhs) < tol


# =============================================================================
# Born-rule map  [Active Work 05]
# =============================================================================

def born_rule_map(theta: float) -> float:
    """
    mu = cos^2(theta / 2) = (1 + cos(theta)) / 2

    Connects the parity-character rotation angle theta to the gravitational
    partition value mu.
    """
    return (1.0 + cos(theta)) / 2.0


def inverse_born_rule(mu_value: float) -> float:
    """
    cos(theta) = 2 mu - 1

    Inverse of the Born-rule map; returns cos(theta), not theta itself.
    """
    return 2.0 * mu_value - 1.0


def x_from_theta(theta: float) -> float:
    """
    x = cot^2(theta / 2) = (1 + cos(theta)) / (1 - cos(theta))

    Map from the rotation angle theta to the dimensionless acceleration x.
    """
    c = cos(theta)
    if isclose(c, 1.0):
        return float("inf")
    return (1.0 + c) / (1.0 - c)


def partition_to_x(mu_value: float) -> float:
    """x = mu / (1 - mu)."""
    if isclose(mu_value, 1.0):
        return float("inf")
    return mu_value / (1.0 - mu_value)


def x_to_partition(x: float) -> float:
    """mu = x / (x + 1). Same as mu(x), included for naming symmetry."""
    return mu(x)


# =============================================================================
# Three interior Niven readings as gravitational regimes
# =============================================================================

def niven_partition_points() -> List[Dict[str, object]]:
    """
    The three interior Niven readings mapped to gravitational regimes.

    Each row carries s, theta, n (rotation order), mu, x, and a regime label.
    The middle reading (s=0) sits at the MOND transition by parity-even =
    exchange-invariance.
    """
    table = niven_partition_table(K=4)
    rows: List[Dict[str, object]] = []
    regimes = {
        -1: "sub-transition",
        0:  "MOND transition (g = a_0)",
        +1: "super-transition",
    }
    for s in (-1, 0, +1):
        entry = table[s]
        theta = entry["theta"]
        mu_value = born_rule_map(theta)
        x = partition_to_x(mu_value)
        rows.append({
            "s":                s,
            "theta":            theta,
            "order_n":          entry["order_n"],
            "phi_n_at_K4":      entry["value_at_K"],
            "mu":               mu_value,
            "x":                x,
            "regime":           regimes[s],
        })
    return rows


def mond_transition_check(tol: float = 1e-12) -> Dict[str, object]:
    """
    Verify the parity-even <-> MOND transition identification:
        s = 0  <->  theta = pi/2  <->  mu = 1/2  <->  x = 1
    """
    theta = pi / 2
    m = born_rule_map(theta)
    x = partition_to_x(m)
    return {
        "theta":  theta,
        "mu":     m,
        "x":      x,
        "is_one_half": abs(m - 0.5) < tol,
        "x_is_one":    abs(x - 1.0) < tol,
        "interpretation": "g = a_0 at the parity-symmetric center of TetA/TetB",
    }


# =============================================================================
# SST quadratic / spherical static limit
# =============================================================================

def sst_quadratic(g: float, a_0: float) -> float:
    """
    Spherically-symmetric static SST source-balance scalar:
        g^2 / (g + a_0)

    The full SST static-spherical limit is g^2 / (g + a_0) = GM / r^2, so this
    function returns the LHS for given (g, a_0).
    """
    return (g * g) / (g + a_0)


def sst_static_solve_g(a_0: float, GM_over_r2: float) -> float:
    """
    Solve g^2 / (g + a_0) = GM / r^2 for g (positive root).

    Quadratic in g:
        g^2 - (GM/r^2) g - a_0 (GM/r^2) = 0
        g = ( (GM/r^2) + sqrt( (GM/r^2)^2 + 4 a_0 (GM/r^2) ) ) / 2
    """
    s = GM_over_r2
    disc = s * s + 4.0 * a_0 * s
    if disc < 0:
        raise ValueError("Negative discriminant in SST solve.")
    return (s + sqrt(disc)) / 2.0
