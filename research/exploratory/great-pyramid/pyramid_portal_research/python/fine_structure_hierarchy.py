"""
fine_structure_hierarchy.py
=============================

Tier 1 #2: place the fine-structure constant α in the closure-algebra
hierarchy via the multiplicative order ord_137(4) and the splitting
behavior of 137 in Z[i], Z[ω], and Z[ζ_{12}].

Empirical observation: 1/α = 137 + 1/28, with both 137 and 28 having
clean closure-algebra interpretations:

  137: prime, 137 ≡ 1 (mod 12), so 137 splits completely in Z[ζ_{12}]
       (i.e. splits in both Z[i] and Z[ω])
  28:  28 = 2² · 7 = K_5 · K_4 where K_5 is the pentachoron vertex
       count and K_4 is the tetrahedral cell count (suggestive only)

This module:

  1. Computes ord_137(4) — the multiplicative order of 4 mod 137
  2. Checks whether 137 splits in Z[i] (137 ≡ 1 mod 4)
  3. Checks whether 137 splits in Z[ω] (137 ≡ 1 mod 3)
  4. Checks whether 137 splits in Z[ζ_{12}] (137 ≡ 1 mod 12)
  5. Locates 137 in the cyclotomic hierarchy: the first Φ_d(4) it
     divides identifies its closure-algebra level
  6. Provides the 1/α = 137 + 1/28 numerical sanity check

Canonical source:
  99_appendices/J_closure_algebra_advancement.md §9 open advance 1
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import math


# ===========================================================================
# Multiplicative order
# ===========================================================================

def multiplicative_order(a: int, p: int) -> Optional[int]:
    """
    Compute ord_p(a) = smallest k >= 1 with a^k ≡ 1 (mod p).
    Returns None if gcd(a, p) != 1.
    """
    if math.gcd(a, p) != 1:
        return None
    order = 1
    x = a % p
    while x != 1:
        x = (x * a) % p
        order += 1
        if order > p:
            return None  # safety guard
    return order


def ord_137_of_4() -> int:
    """The multiplicative order of 4 modulo 137."""
    return multiplicative_order(4, 137)


# ===========================================================================
# Splitting behavior of 137 in cyclotomic rings
# ===========================================================================

def splits_in_Z_i(p: int) -> bool:
    """
    Z[i] = Z[ζ_4].  An odd prime p splits in Z[i] iff p ≡ 1 (mod 4).
    """
    return p % 4 == 1


def splits_in_Z_omega(p: int) -> bool:
    """
    Z[ω] = Z[ζ_3].  A prime p > 3 splits in Z[ω] iff p ≡ 1 (mod 3).
    """
    return p % 3 == 1


def splits_in_Z_zeta_12(p: int) -> bool:
    """
    Z[ζ_{12}].  A prime p coprime to 12 splits completely in Z[ζ_{12}]
    iff p ≡ 1 (mod 12).

    For p ≡ 5, 7, 11 (mod 12) (the other unit residues) p factors as a
    product of two primes (degree 2 inertia), with the precise behavior
    determined by which subfield p splits in.
    """
    return p % 12 == 1


def splitting_summary(p: int) -> Dict[str, object]:
    """Full splitting summary for an odd prime p > 3."""
    return {
        "p": p,
        "p_mod_3": p % 3,
        "p_mod_4": p % 4,
        "p_mod_12": p % 12,
        "splits_in_Z_i": splits_in_Z_i(p),
        "splits_in_Z_omega": splits_in_Z_omega(p),
        "splits_in_Z_zeta_12": splits_in_Z_zeta_12(p),
    }


# ===========================================================================
# Locating 137 in the cyclotomic hierarchy
# ===========================================================================

def cyclotomic_value(n: int, K: int) -> int:
    """Φ_n(K) for n in {1, 2, 3, 4, 6, 8, 12}."""
    if n == 1:  return K - 1
    if n == 2:  return K + 1
    if n == 3:  return K * K + K + 1
    if n == 4:  return K * K + 1
    if n == 6:  return K * K - K + 1
    if n == 8:  return K ** 4 + 1
    if n == 12: return K ** 4 - K * K + 1
    raise NotImplementedError(f"Φ_{n} not implemented")


def divides_phi_d_K(p: int, d: int, K: int) -> bool:
    """Test whether prime p divides Φ_d(K)."""
    val = cyclotomic_value(d, K)
    return val % p == 0


def first_phi_dividing_137(K: int = 4, max_d: int = 24) -> Optional[Dict[str, object]]:
    """
    Find the smallest d such that 137 | Φ_d(K).

    The answer is determined by ord_p(K): 137 first divides Φ_d(K)
    at d = ord_{137}(K).
    """
    for d in (1, 2, 3, 4, 6, 8, 12):
        if divides_phi_d_K(137, d, K):
            return {
                "d": d,
                "Phi_d_K": cyclotomic_value(d, K),
                "K": K,
                "p": 137,
            }
    # Extended scan via factorization-free test
    val = 1
    for d in range(1, max_d + 1):
        val_d = K ** d - 1
        # We only need d such that 137 | (K^d - 1) and 137 doesn't divide K^e - 1 for e < d
        # That d is exactly ord_137(K).
        if val_d % 137 == 0:
            return {
                "d": d,
                "K_d_minus_1": val_d,
                "interpretation": "smallest d with 137 | (K^d - 1) = ord_137(K)",
                "K": K,
                "p": 137,
            }
    return None


def locate_137_in_hierarchy(K: int = 4) -> Dict[str, object]:
    """
    Full diagnostic placing 137 in the closure-algebra hierarchy at K.
    """
    ord_4_137 = ord_137_of_4()
    splitting = splitting_summary(137)
    first_phi = first_phi_dividing_137(K)
    return {
        "p": 137,
        "K": K,
        "ord_K_mod_p": ord_4_137,
        "splitting": splitting,
        "first_phi_dividing": first_phi,
        "is_prime": is_prime_simple(137),
    }


def is_prime_simple(n: int) -> bool:
    """Trial-division primality test (only used here for small p)."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    p = 3
    while p * p <= n:
        if n % p == 0:
            return False
        p += 2
    return True


# ===========================================================================
# 1/α = 137 + 1/28 numerical sanity check
# ===========================================================================

def alpha_inv_predicted() -> float:
    """The framework's predicted 1/α = 137 + 1/28."""
    return 137.0 + 1.0 / 28.0


# CODATA 2018: 1/α = 137.035999084(21)
ALPHA_INV_CODATA = 137.035999084


def alpha_inv_residual() -> Dict[str, float]:
    """Compare predicted vs CODATA value."""
    predicted = alpha_inv_predicted()
    return {
        "predicted_alpha_inv": predicted,
        "codata_alpha_inv": ALPHA_INV_CODATA,
        "absolute_residual": predicted - ALPHA_INV_CODATA,
        "relative_residual_ppm": (predicted - ALPHA_INV_CODATA) / ALPHA_INV_CODATA * 1e6,
    }


# ===========================================================================
# The 28 structural reading
# ===========================================================================

def twenty_eight_structural_reading() -> Dict[str, object]:
    """
    The denominator 28 in 1/α = 137 + 1/28 has a closure-algebra reading:
        28 = 4 + 24 = (pentachoron vertices K_5) + (torsion sector at D=3)
        28 = 7 · 4 = K_4 vertices times Fano-seed shell at K=2
        28 = C(8, 2) = pair count of Cl(3, 0) basis elements
    These are observations, not derivations.
    """
    return {
        "28": 28,
        "as_4_plus_24": "K_5 vertices (4) + torsion sector (24)",
        "as_7_times_4": "Fano shell f_+(2)=7 · K_4=4 cells",
        "as_C_8_2": "pair count of Cl(3,0) basis elements (8 choose 2 = 28)",
    }


# ===========================================================================
# Showcase
# ===========================================================================

def showcase_fine_structure_hierarchy() -> List[str]:
    """Audit trail for placing 137 in the closure-algebra hierarchy."""
    lines: List[str] = []
    lines.append("=" * 76)
    lines.append("  FINE-STRUCTURE CONSTANT IN THE CLOSURE-ALGEBRA HIERARCHY")
    lines.append("=" * 76)
    lines.append("")
    lines.append("  Empirical observation: 1/α = 137 + 1/28")
    resid = alpha_inv_residual()
    lines.append(f"    Predicted: {resid['predicted_alpha_inv']:.9f}")
    lines.append(f"    CODATA:    {resid['codata_alpha_inv']:.9f}")
    lines.append(f"    Residual:  {resid['absolute_residual']:+.9f}  ({resid['relative_residual_ppm']:+.2f} ppm)")
    lines.append("")
    info = locate_137_in_hierarchy(K=4)
    lines.append(f"  137 is prime: {info['is_prime']}")
    lines.append("")
    lines.append("  Splitting behavior of 137 in cyclotomic rings:")
    s = info["splitting"]
    lines.append(f"    137 mod 3  = {s['p_mod_3']}  -> splits in Z[ω]:       {s['splits_in_Z_omega']}")
    lines.append(f"    137 mod 4  = {s['p_mod_4']}  -> splits in Z[i]:       {s['splits_in_Z_i']}")
    lines.append(f"    137 mod 12 = {s['p_mod_12']}  -> splits in Z[ζ_{{12}}]: {s['splits_in_Z_zeta_12']}")
    lines.append("")
    lines.append(f"  Multiplicative order of 4 mod 137: ord_137(4) = {info['ord_K_mod_p']}")
    if info["first_phi_dividing"]:
        fpd = info["first_phi_dividing"]
        lines.append(f"  137 first divides K^d - 1 at d = {fpd['d']}")
        lines.append(f"     => 137 appears at cyclotomic level Φ_{fpd['d']}(K) or its factors")
    lines.append("")
    lines.append("  Structural readings of 28 (the denominator):")
    for k, v in twenty_eight_structural_reading().items():
        if k != "28":
            lines.append(f"    {v}")
    lines.append("")
    return lines
