"""
coupling_shells.py
====================

The parity-pushout recursion and the full K=1..K=5 shell family.

Canonical source:
    99_appendices/I_coupling_polynomial_engineering_synthesis.md

This module is the engineering view of the coupling polynomial:

    f(K, s) = K^2 + s K + 1,     s in {-1, 0, +1}

reads as three set-theoretic objects:

    f_-(K) = K^2 - K + 1 = |A_K cap B_K|     shared core
    f_0(K) = K^2 + 1     = |A_K| = |B_K|     each parity sheet
    f_+(K) = K^2 + K + 1 = |A_K cup B_K|     full union

The parity-pushout recursion is the *constructive* generator:

    C_{K+1} = A_K cup_{C_K} B_K
    |C_{K+1}| = |C_K| + 2K

with seed C_1 = 1.  This recursion produces the full shell family
(1, 2, 3) -> (3, 5, 7) -> (7, 10, 13) -> (13, 17, 21) -> (21, 26, 31)
at K = 1, 2, 3, 4, 5.  Adjacent shells lock through

    f_+(K) = f_-(K + 1).

The polynomial does not merely describe a static object.  It describes
a growth rule:

    overlap -> two parity sheets -> union -> next overlap.

This module exposes:

  * The parity-pushout recursion as a generator
  * The named shell family (Seed, Fano, Star-of-David, Tetrad, Receiver)
  * The additive decomposition reading f_+(K) = f_-(K) + K + K
  * The adjacent-shell lock f_+(K) = f_-(K+1)
  * The discriminant identity (f_+(K) - f_-(K))^2 = 4K^2
  * The directed simplex edge count f_+(K) - 1 = 2 C(K+1, 2)
  * The projective plane count f_+(q) = |P^2(F_q)| at prime power q
  * The parity-pushout category as a structured object
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import math

from python.cyclotomic import phi3, phi4, phi6, coupling_polynomial


# ---------------------------------------------------------------------------
# Parity-pushout recursion
# ---------------------------------------------------------------------------

def parity_pushout_step(C_K: int, K: int) -> int:
    """
    The parity-pushout recursion:
        |C_{K+1}| = |C_K| + 2K
    Returns |C_{K+1}|.
    """
    return C_K + 2 * K


def parity_pushout_orbit(K_max: int, C_1: int = 1) -> List[int]:
    """
    Generate the parity-pushout orbit C_1, C_2, ..., C_{K_max} starting
    from a seed C_1 (default 1).

    With C_1 = 1, the orbit is 1, 3, 7, 13, 21, 31, 43, ...
    """
    if K_max < 1:
        raise ValueError("K_max must be >= 1")
    orbit = [C_1]
    for K in range(1, K_max):
        orbit.append(parity_pushout_step(orbit[-1], K))
    return orbit


def parity_pushout_closed_form(K: int, C_1: int = 1) -> int:
    """
    Closed form of the orbit:
        |C_K| = C_1 + 2 * (1 + 2 + ... + (K-1))
              = C_1 + K(K-1)
    At C_1 = 1: |C_K| = K^2 - K + 1 = Phi_6(K).
    """
    if K < 1:
        raise ValueError("K must be >= 1")
    return C_1 + K * (K - 1)


# ---------------------------------------------------------------------------
# The coupling shell as a named structure
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CouplingShell:
    """
    A coupling shell at level K.

    Fields:
        K        : shell level
        f_minus  : f(K, -1) = K^2 - K + 1 = Phi_6(K) = |A_K cap B_K| shared core
        f_zero   : f(K,  0) = K^2 + 1     = Phi_4(K) = |A_K| = |B_K|
        f_plus   : f(K, +1) = K^2 + K + 1 = Phi_3(K) = |A_K cup B_K|
        name     : framework name for this shell
    """
    K: int
    f_minus: int
    f_zero: int
    f_plus: int
    name: str

    @property
    def tuple(self) -> Tuple[int, int, int]:
        return (self.f_minus, self.f_zero, self.f_plus)

    @property
    def decomposition(self) -> str:
        """Additive parity reading: f_+(K) = f_-(K) + K + K."""
        return f"{self.f_plus} = {self.f_minus} + {self.K} + {self.K}"


# Named shells from section 3-8 of the engineering synthesis
SHELL_NAMES = {
    1: "Seed",
    2: "Fano seed",
    3: "Star-of-David",
    4: "Tetrad",
    5: "Receiver",
}


def coupling_shell(K: int) -> CouplingShell:
    """Construct the named coupling shell at level K."""
    return CouplingShell(
        K=K,
        f_minus=coupling_polynomial(K, -1),
        f_zero=coupling_polynomial(K, 0),
        f_plus=coupling_polynomial(K, 1),
        name=SHELL_NAMES.get(K, f"K={K}"),
    )


def coupling_shell_family(K_max: int = 5) -> List[CouplingShell]:
    """
    The full K=1..K_max shell family.  Default K_max = 5 covers the
    canonical Seed -> Fano -> Star-of-David -> Tetrad -> Receiver chain.
    """
    return [coupling_shell(K) for K in range(1, K_max + 1)]


def coupling_shell_table(K_max: int = 5) -> List[Dict[str, object]]:
    """Tabular dump suitable for printing / inspection."""
    rows = []
    for shell in coupling_shell_family(K_max):
        rows.append({
            "K": shell.K,
            "name": shell.name,
            "shared_core": shell.f_minus,
            "each_sheet": shell.f_zero,
            "full_union": shell.f_plus,
            "decomposition": shell.decomposition,
        })
    return rows


# ---------------------------------------------------------------------------
# Adjacent-shell lock: f_+(K) = f_-(K+1)
# ---------------------------------------------------------------------------

def adjacent_shell_lock_check(K: int) -> Dict[str, object]:
    """
    Verify the adjacent-shell lock f_+(K) = f_-(K+1).
    This is the same algebraic content as the shift identity
    Phi_3(K) = Phi_6(K+1), written in the parity-pushout language
    where it says "the K shell's full union is the K+1 shell's shared core".
    """
    f_plus_K = coupling_polynomial(K, 1)
    f_minus_K1 = coupling_polynomial(K + 1, -1)
    return {
        "K": K,
        "f_plus_K": f_plus_K,
        "f_minus_K_plus_1": f_minus_K1,
        "locked": f_plus_K == f_minus_K1,
    }


def adjacent_shell_lock_scan(K_max: int = 5) -> Dict[str, object]:
    """Verify the adjacent-shell lock across K=1..K_max."""
    results = [adjacent_shell_lock_check(K) for K in range(1, K_max + 1)]
    return {
        "by_K": results,
        "all_locked": all(r["locked"] for r in results),
    }


# ---------------------------------------------------------------------------
# Discriminant identity: (f_+(K) - f_-(K))^2 = 4 K^2
# ---------------------------------------------------------------------------

def discriminant_identity_squared(K: int) -> Dict[str, int]:
    """
    Engineering form of the range identity from the synthesis (section 14):

        (f_+(K) - f_-(K))^2 = 4 K^2

    At K=4: (21 - 13)^2 = 8^2 = 64 = K^3, matching the closure-tile size.

    Note: this is *different* in form from the linear range identity
    Delta f = 2K (T8 in unification_algebra), which gives 2K = 2^D at
    D=3 specifically.  The squared form gives 4K^2 universally.
    """
    f_plus = coupling_polynomial(K, 1)
    f_minus = coupling_polynomial(K, -1)
    delta = f_plus - f_minus
    return {
        "K": K,
        "f_plus": f_plus,
        "f_minus": f_minus,
        "delta": delta,
        "delta_squared": delta * delta,
        "four_K_squared": 4 * K * K,
        "matches": delta * delta == 4 * K * K,
    }


# ---------------------------------------------------------------------------
# Directed simplex edge count: f_+(K) - 1 = 2 C(K+1, 2)
# ---------------------------------------------------------------------------

def directed_simplex_edge_identity(K: int) -> Dict[str, int]:
    """
    Synthesis section 12 / 19:
        f_+(K) - 1 = 2 * C(K+1, 2) = K(K+1)

    At K=4: f_+(4) - 1 = 20 = 2*10 = K*(K+1).
    This is the pentachoron's directed edge count.  At K=5 it gives
    the next simplex level: f_+(5) - 1 = 30 = 2*15.
    """
    f_plus = coupling_polynomial(K, 1)
    binom = math.comb(K + 1, 2)
    return {
        "K": K,
        "f_plus_K_minus_1": f_plus - 1,
        "two_binom_K_plus_1_choose_2": 2 * binom,
        "K_times_K_plus_1": K * (K + 1),
        "matches": (f_plus - 1) == 2 * binom == K * (K + 1),
    }


# ---------------------------------------------------------------------------
# Projective plane count: f_+(q) = |P^2(F_q)| at prime power q
# ---------------------------------------------------------------------------

# Small primes for testing.  This list is sufficient to verify the
# identity at the prime powers q in {2, 3, 4, 5, 7, 8, 9, 11, ...}.
SMALL_PRIME_POWERS = (2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 32)


def projective_plane_general(q: int) -> int:
    """
    The number of points in P^2(F_q) for any prime power q.
    Formula: |P^2(F_q)| = q^2 + q + 1.

    For q a prime power, this is exactly f_+(q) = q^2 + q + 1.

    Note: this generalizes closure_core256.projective_plane_q2_count
    which gives |P^2(F_{K^2})| = K^4 + K^2 + 1, i.e. evaluated at K^2.
    Here we evaluate the identity at q directly.
    """
    if q < 2:
        raise ValueError("q must be >= 2")
    return q * q + q + 1


def projective_plane_identity_check(q: int) -> Dict[str, int]:
    """
    Verify f_+(q) = q^2 + q + 1 = |P^2(F_q)| at any q >= 2.

    For q a prime power, this gives a well-defined projective plane.
    For composite q (like q=4, 8, 9, ...) the prime-power constraint
    is satisfied by 4=2^2, 8=2^3, 9=3^2, etc.
    """
    f_plus = coupling_polynomial(q, 1)
    plane = projective_plane_general(q)
    return {
        "q": q,
        "f_plus_q": f_plus,
        "P2_F_q_count": plane,
        "matches": f_plus == plane,
    }


def is_prime_power(n: int) -> bool:
    """True iff n is a prime power (n = p^k for some prime p and k >= 1)."""
    if n < 2:
        return False
    # Find the smallest prime factor
    p = 2
    while p * p <= n:
        if n % p == 0:
            # n = p^k iff after dividing out all p, we get 1
            while n % p == 0:
                n //= p
            return n == 1
        p += 1
    # n was prime
    return True


# ---------------------------------------------------------------------------
# Parity-pushout category (objects, morphisms)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ParityPushoutMorphism:
    """One of the canonical morphisms in the parity-pushout category."""
    name: str
    description: str
    algebraic_form: str


def parity_pushout_category() -> Dict[str, object]:
    """
    The parity-pushout category from section 15 of the synthesis.

    Objects     : coupling shells C_K = (f_-(K), f_0(K), f_+(K))
    Morphisms   : parity pushout, shift, fusion, edge, projective
    """
    return {
        "objects": {
            "name": "Coupling shells",
            "definition": "C_K = (f_-(K), f_0(K), f_+(K)) at integer K >= 1",
            "shells": coupling_shell_table(5),
        },
        "morphisms": [
            ParityPushoutMorphism(
                name="parity_pushout",
                description="Glue two parity sheets along their shared core to form the next core.",
                algebraic_form="C_{K+1} = A_K cup_{C_K} B_K"
            ),
            ParityPushoutMorphism(
                name="shift",
                description="The K shell's full union equals the K+1 shell's shared core.",
                algebraic_form="f_+(K) = f_-(K+1)"
            ),
            ParityPushoutMorphism(
                name="fusion",
                description="Multiplicative scale fusion across levels.",
                algebraic_form="f_+(K) * f_-(K) = f_+(K^2)"
            ),
            ParityPushoutMorphism(
                name="edge",
                description="The full-union minus the seed reads as twice the K+1 choose 2.",
                algebraic_form="f_+(K) - 1 = 2 C(K+1, 2)"
            ),
            ParityPushoutMorphism(
                name="projective",
                description="Full union counts the points of the projective plane over F_q.",
                algebraic_form="f_+(q) = |P^2(F_q)| at prime power q"
            ),
        ],
    }


# ---------------------------------------------------------------------------
# The named transitions
# ---------------------------------------------------------------------------

def star_transition_K3_to_K4() -> Dict[str, object]:
    """
    Section 17: the K=3 -> K=4 transition.
    The K=3 shell (7, 10, 13) produces the K=4 shared core 13.
    Visually: the 13-dot Star-of-David is the bridge.
    """
    K3 = coupling_shell(3)
    K4 = coupling_shell(4)
    return {
        "from_shell": K3.tuple,
        "to_shell": K4.tuple,
        "from_name": K3.name,
        "to_name": K4.name,
        "bridge_value": K3.f_plus,  # 13 = f_+(3) = f_-(4)
        "is_locked": K3.f_plus == K4.f_minus,
        "interpretation": "K=3 full union = K=4 shared core = 13 (Star-of-David bridge)",
    }


def portal_transition_K4_to_K5() -> Dict[str, object]:
    """
    Section 18: the K=4 -> K=5 portal transition.
    The K=4 tetrad shell (13, 17, 21) produces the K=5 receiver shell's
    shared core: 21 = f_+(4) = f_-(5).
    This is the K=4 -> K=5 hinge that drives the entire portal physics.
    """
    K4 = coupling_shell(4)
    K5 = coupling_shell(5)
    return {
        "from_shell": K4.tuple,
        "to_shell": K5.tuple,
        "from_name": K4.name,
        "to_name": K5.name,
        "bridge_value": K4.f_plus,  # 21 = f_+(4) = f_-(5)
        "is_locked": K4.f_plus == K5.f_minus,
        "interpretation": "K=4 full union = K=5 shared core = 21 (Portal hinge)",
    }


# ---------------------------------------------------------------------------
# Top-level audit trail
# ---------------------------------------------------------------------------

def showcase_coupling_shells() -> List[str]:
    """One-shot audit trail of the parity-pushout recursion and shell family."""
    lines: List[str] = []
    lines.append("=" * 78)
    lines.append("  COUPLING SHELLS — parity-pushout recursion and the K=1..K=5 family")
    lines.append("=" * 78)
    lines.append("")
    lines.append(f"  Recursion : C_{{K+1}} = |A_K cup_{{C_K}} B_K| = |C_K| + 2K")
    lines.append(f"  Seed     : C_1 = 1")
    lines.append(f"  Closed form : |C_K| = K^2 - K + 1 = Phi_6(K)")
    lines.append("")

    lines.append("  Shell family (parity reading):")
    lines.append("")
    lines.append(f"  {'K':>3} | {'Name':<14} | {'core':>5} | {'sheet':>5} | {'union':>5} | decomposition")
    lines.append("  " + "-" * 72)
    for row in coupling_shell_table(5):
        lines.append(f"  {row['K']:>3} | {row['name']:<14} | {row['shared_core']:>5} | "
                     f"{row['each_sheet']:>5} | {row['full_union']:>5} | {row['decomposition']}")
    lines.append("")

    lines.append("  Adjacent-shell lock f_+(K) = f_-(K+1):")
    lock = adjacent_shell_lock_scan(5)
    for r in lock["by_K"]:
        if r["K"] < 5:
            lines.append(f"    K={r['K']}: f_+({r['K']}) = {r['f_plus_K']} = f_-({r['K']+1}) = {r['f_minus_K_plus_1']}  -> {r['locked']}")
    lines.append(f"    All locked: {lock['all_locked']}")
    lines.append("")

    lines.append("  Discriminant identity (f_+ - f_-)^2 = 4K^2 across K=2..5:")
    for K in range(2, 6):
        d = discriminant_identity_squared(K)
        lines.append(f"    K={K}: ({d['f_plus']} - {d['f_minus']})^2 = {d['delta_squared']} = 4*{K}^2 = {d['four_K_squared']}  -> {d['matches']}")
    lines.append("")

    lines.append("  Directed simplex edge identity f_+(K) - 1 = 2 C(K+1, 2):")
    for K in range(2, 6):
        e = directed_simplex_edge_identity(K)
        lines.append(f"    K={K}: f_+({K}) - 1 = {e['f_plus_K_minus_1']} = 2*C({K+1},2) = {e['two_binom_K_plus_1_choose_2']}  -> {e['matches']}")
    lines.append("")

    lines.append("  Projective plane identity f_+(q) = |P^2(F_q)| at prime powers:")
    for q in (2, 3, 4, 5, 7, 8, 9, 11):
        p = projective_plane_identity_check(q)
        lines.append(f"    q={q:>2} (prime power: {is_prime_power(q)}): f_+({q}) = {p['f_plus_q']} = |P^2(F_{q})| = {p['P2_F_q_count']}  -> {p['matches']}")
    lines.append("")

    lines.append("  Named transitions:")
    star = star_transition_K3_to_K4()
    portal = portal_transition_K4_to_K5()
    lines.append(f"    Star transition K=3 -> K=4 (bridge = {star['bridge_value']}): {star['is_locked']}")
    lines.append(f"    Portal transition K=4 -> K=5 (bridge = {portal['bridge_value']}): {portal['is_locked']}")
    lines.append("")
    return lines
