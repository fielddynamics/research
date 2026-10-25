"""
mirror_match_distribution.py
==============================

Tier 1 #5: characterize the mirror-match functional M(U, V) as a
distribution over random triad pairs.

The mirror-match functional from apparatus.py:

    M(U, V) = (sum over permutations P) exp(-||G_U - P^T G_V P||² / ε²)
              · (1 - chi_U · chi_V) / 2
              · δ_phase

decomposes into three gate factors:
  - chirality_factor (∈ {0, 1}) — non-zero only when chiralities oppose
  - phase_factor (∈ {0, 1})     — non-zero only when phases close mod 2π
  - gram_factor (∈ [0, 6])      — Gaussian kernel sum over S_3 permutations

Across a random ensemble of triad pairs:
  1. Most pairs fail the chirality gate (one of {-1, 0, +1} × {-1, 0, +1})
  2. Most pairs fail the phase-closure gate
  3. Only triads whose Gram matrices match up to a permutation give
     non-trivial gram_factor

The expected distribution is therefore strongly bimodal: a large
spike at 0 (most pairs) plus a small set of matched pairs near 1.

This module:
  1. Generates ensembles of random Address objects
  2. Computes M for all pairs in the ensemble
  3. Builds a histogram of M values
  4. Characterizes match rates as a function of tolerance ε
  5. Demonstrates the gate-decomposition independently
  6. Connects to the S_3 permutation structure of triads

Canonical source:
  Tier 1 #5; apparatus.mirror_match_functional
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import math
import numpy as np

from python.apparatus import (
    Address, ShaftKey, make_address, mirror_match_functional,
    chirality, gram_matrix, triadic_phase, phase_closed,
    normalize, TAU,
)


# ===========================================================================
# Random Address generation
# ===========================================================================

def random_unit_vector(rng: np.random.Generator) -> Tuple[float, float, float]:
    """Sample a uniform point on S^2."""
    v = rng.standard_normal(3)
    n = float(np.linalg.norm(v))
    return (float(v[0] / n), float(v[1] / n), float(v[2] / n))


def random_shaft_keys(rng: np.random.Generator, band: int = 0) -> List[ShaftKey]:
    """Generate three random ShaftKey-like objects covering the Address inputs."""
    keys = []
    for _ in range(3):
        d = random_unit_vector(rng)
        phase = float(rng.uniform(0.0, TAU))
        omega = float(rng.uniform(0.5, 1.5))
        keys.append(ShaftKey(
            direction=d,
            length=1.0,
            impedance=1.0,
            omega=omega,
            phase=phase,
            band=band,
        ))
    return keys


def random_address(rng: np.random.Generator, band: int = 0) -> Address:
    """Generate a random Address."""
    keys = random_shaft_keys(rng, band=band)
    return make_address(keys)


def mirror_pair(addr: Address) -> Address:
    """
    Construct a deliberate mirror partner V of U: same Gram matrix,
    opposite chirality, matching phase (so all three gates fire).

    Simplest construction: reflect the triad through the origin
    (negate each vector).  This flips chirality (det(-A) = -det(A))
    but preserves the Gram matrix (G is invariant under orthogonal
    transformations including reflection).

    We set the phase equal so the phase gate fires.  In practice the
    phase of the mirror partner would be encoded by mirror physics
    (TetA <-> TetB swap) which can preserve the closure value.
    """
    reflected_triad = tuple((-v[0], -v[1], -v[2]) for v in addr.triad)
    new_gram = gram_matrix(reflected_triad)
    new_chir = chirality(reflected_triad)
    return Address(
        triad=reflected_triad,  # type: ignore[arg-type]
        gram=new_gram,
        chirality=new_chir,
        phase=addr.phase,  # designed to match
        band=addr.band,
    )


# ===========================================================================
# Distribution sampling
# ===========================================================================

@dataclass
class DistributionStats:
    n_pairs: int
    epsilon: float
    values: List[float]
    n_zero: int
    n_above_0_5: int
    n_above_0_9: int
    max_value: float
    mean_value: float

    def summary(self) -> Dict[str, float]:
        return {
            "n_pairs": self.n_pairs,
            "epsilon": self.epsilon,
            "n_zero": self.n_zero,
            "n_above_0_5": self.n_above_0_5,
            "n_above_0_9": self.n_above_0_9,
            "max_value": self.max_value,
            "mean_value": self.mean_value,
            "fraction_zero": self.n_zero / self.n_pairs if self.n_pairs else 0.0,
            "fraction_above_0_9": self.n_above_0_9 / self.n_pairs if self.n_pairs else 0.0,
        }


def sample_mirror_match_distribution(
    n_pairs: int = 200,
    epsilon: float = 1e-3,
    seed: int = 42,
    band: int = 0,
) -> DistributionStats:
    """
    Sample M(U, V) for random independent Address pairs and characterize
    the distribution.
    """
    rng = np.random.default_rng(seed)
    values: List[float] = []
    for _ in range(n_pairs):
        u = random_address(rng, band=band)
        v = random_address(rng, band=band)
        m = mirror_match_functional(u, v, epsilon=epsilon)
        values.append(m)
    arr = np.array(values, dtype=float)
    return DistributionStats(
        n_pairs=n_pairs,
        epsilon=epsilon,
        values=values,
        n_zero=int((arr == 0.0).sum()),
        n_above_0_5=int((arr >= 0.5).sum()),
        n_above_0_9=int((arr >= 0.9).sum()),
        max_value=float(arr.max()) if n_pairs > 0 else 0.0,
        mean_value=float(arr.mean()) if n_pairs > 0 else 0.0,
    )


def sample_designed_mirror_pairs(
    n_pairs: int = 50,
    epsilon: float = 1e-3,
    seed: int = 7,
    band: int = 0,
) -> DistributionStats:
    """
    Sample M(U, mirror(U)) for random U with the mirror-partner construction
    (reflect through origin).  Most should match strongly.
    """
    rng = np.random.default_rng(seed)
    values: List[float] = []
    for _ in range(n_pairs):
        u = random_address(rng, band=band)
        v = mirror_pair(u)
        m = mirror_match_functional(u, v, epsilon=epsilon)
        values.append(m)
    arr = np.array(values, dtype=float)
    return DistributionStats(
        n_pairs=n_pairs,
        epsilon=epsilon,
        values=values,
        n_zero=int((arr == 0.0).sum()),
        n_above_0_5=int((arr >= 0.5).sum()),
        n_above_0_9=int((arr >= 0.9).sum()),
        max_value=float(arr.max()) if n_pairs > 0 else 0.0,
        mean_value=float(arr.mean()) if n_pairs > 0 else 0.0,
    )


# ===========================================================================
# Gate decomposition: chirality, phase, Gram
# ===========================================================================

def chirality_gate(u: Address, v: Address) -> float:
    """The chirality gate factor (1 - chi_u · chi_v) / 2."""
    return (1.0 - u.chirality * v.chirality) / 2.0


def phase_gate(u: Address, v: Address, tol: float = 1e-6) -> float:
    """The phase-closure gate factor."""
    dphase = (u.phase - v.phase) % TAU
    return 1.0 if phase_closed(dphase, tol=tol) else 0.0


def gram_gate(u: Address, v: Address, epsilon: float = 1e-3) -> float:
    """
    The Gram-matching factor: sum over S_3 permutations of
    exp(-||G_u - P^T G_v P||² / ε²).
    """
    G_u = np.array(u.gram)
    G_v = np.array(v.gram)
    total = 0.0
    perms = [
        (0, 1, 2), (0, 2, 1), (1, 0, 2),
        (1, 2, 0), (2, 0, 1), (2, 1, 0),
    ]
    for p in perms:
        P = np.zeros((3, 3))
        for i, pi in enumerate(p):
            P[pi, i] = 1.0
        diff = G_u - P.T @ G_v @ P
        norm_sq = float(np.sum(diff * diff))
        total += math.exp(-norm_sq / (epsilon * epsilon))
    return total


def gate_decomposition_stats(
    n_pairs: int = 200,
    seed: int = 11,
    band: int = 0,
) -> Dict[str, object]:
    """
    For an ensemble of random pairs, count how often each gate fires.
    The Gram gate is treated as "fires" if its value exceeds 1 (a
    weak threshold; matching adds 1.0 to the sum per identity-permutation).
    """
    rng = np.random.default_rng(seed)
    chir_fires = 0
    phase_fires = 0
    gram_fires = 0
    all_three_fire = 0

    for _ in range(n_pairs):
        u = random_address(rng, band=band)
        v = random_address(rng, band=band)
        c = chirality_gate(u, v) > 0.0
        p = phase_gate(u, v) > 0.0
        g = gram_gate(u, v) > 1.0
        if c: chir_fires += 1
        if p: phase_fires += 1
        if g: gram_fires += 1
        if c and p and g: all_three_fire += 1

    return {
        "n_pairs": n_pairs,
        "chirality_fire_rate": chir_fires / n_pairs if n_pairs else 0.0,
        "phase_fire_rate": phase_fires / n_pairs if n_pairs else 0.0,
        "gram_fire_rate": gram_fires / n_pairs if n_pairs else 0.0,
        "all_three_fire_rate": all_three_fire / n_pairs if n_pairs else 0.0,
        "expected_random_match_rate": "≈ 0  (chirality + phase + Gram simultaneously fire only rarely)",
    }


# ===========================================================================
# Tolerance sweep: M as function of epsilon
# ===========================================================================

def tolerance_sweep(
    epsilons: Optional[List[float]] = None,
    n_pairs: int = 100,
    seed: int = 23,
    use_designed_pairs: bool = True,
) -> List[Dict[str, float]]:
    """
    Sweep epsilon and record summary stats for the distribution at
    each tolerance.

    For designed mirror pairs (perfect Gram match), increasing epsilon
    makes the Gaussian wider but the match was already exact, so
    the value saturates.  For random pairs, increasing epsilon
    eventually finds any pair "close enough."
    """
    if epsilons is None:
        epsilons = [1e-6, 1e-4, 1e-3, 1e-2, 1e-1]
    out: List[Dict[str, float]] = []
    for eps in epsilons:
        if use_designed_pairs:
            stats = sample_designed_mirror_pairs(n_pairs=n_pairs, epsilon=eps, seed=seed)
        else:
            stats = sample_mirror_match_distribution(n_pairs=n_pairs, epsilon=eps, seed=seed)
        out.append({
            "epsilon": eps,
            "max_M": stats.max_value,
            "mean_M": stats.mean_value,
            "fraction_above_0_9": stats.n_above_0_9 / stats.n_pairs if stats.n_pairs else 0.0,
        })
    return out


# ===========================================================================
# Showcase
# ===========================================================================

def showcase_mirror_match_distribution() -> List[str]:
    """Audit trail for the mirror-match distribution analysis."""
    lines: List[str] = []
    lines.append("=" * 76)
    lines.append("  MIRROR-MATCH DISTRIBUTION OVER RANDOM TRIAD PAIRS")
    lines.append("=" * 76)
    lines.append("")
    lines.append("  Random independent pairs (no matching constraint):")
    rd = sample_mirror_match_distribution(n_pairs=200, epsilon=1e-3, seed=42)
    rds = rd.summary()
    lines.append(f"    n_pairs:           {rds['n_pairs']}")
    lines.append(f"    fraction at M=0:   {rds['fraction_zero']:.3f}")
    lines.append(f"    fraction M >= 0.9: {rds['fraction_above_0_9']:.3f}")
    lines.append(f"    max M observed:    {rds['max_value']:.6e}")
    lines.append(f"    mean M:            {rds['mean_value']:.6e}")
    lines.append("")
    lines.append("  Designed mirror-partner pairs V = -U:")
    dd = sample_designed_mirror_pairs(n_pairs=50, epsilon=1e-3, seed=7)
    dds = dd.summary()
    lines.append(f"    n_pairs:           {dds['n_pairs']}")
    lines.append(f"    fraction at M=0:   {dds['fraction_zero']:.3f}")
    lines.append(f"    fraction M >= 0.9: {dds['fraction_above_0_9']:.3f}")
    lines.append(f"    max M observed:    {dds['max_value']:.6f}")
    lines.append(f"    mean M:            {dds['mean_value']:.6f}")
    lines.append("")
    lines.append("  Gate decomposition (random pairs):")
    gate = gate_decomposition_stats(n_pairs=200, seed=11)
    lines.append(f"    chirality fires:   {gate['chirality_fire_rate']:.3f}")
    lines.append(f"    phase fires:       {gate['phase_fire_rate']:.3f}")
    lines.append(f"    Gram fires:        {gate['gram_fire_rate']:.3f}")
    lines.append(f"    all three fire:    {gate['all_three_fire_rate']:.3f}")
    lines.append("")
    lines.append("  Tolerance sweep (designed pairs):")
    sweep = tolerance_sweep(use_designed_pairs=True)
    for row in sweep:
        lines.append(f"    ε={row['epsilon']:.0e}: max_M={row['max_M']:.4f}, "
                     f"mean={row['mean_M']:.4f}, frac>=0.9={row['fraction_above_0_9']:.2f}")
    lines.append("")
    lines.append("  Structural interpretation:")
    lines.append("    Random pairs: M ≈ 0 (bimodal distribution spike at zero).")
    lines.append("    Mirror-designed pairs: M ≈ 1 when chirality + phase + Gram align.")
    lines.append("    The three gates filter ~1/4 (chirality) × ~0 (phase, continuous)")
    lines.append("    × ~ε³ (Gram) = effectively zero for generic random pairs.")
    lines.append("")
    return lines
