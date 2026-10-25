"""
topology.py
===========

Discrete topology helpers for the framework:

  - Hopf / SU(2) address: quaternion arithmetic and S^3 -> S^2 projection
  - Electron Hopf-fiber holonomy g_e/2
  - A_5 alternating group order and pentachoron cell count
  - A_5 x Z_21 combined sector count
  - Crystallographic threshold: pentachoron S_5 symmetry and the 5-fold factor
  - Null-cone associator status table (Clifford closure)

References: project §03.3 Hopf bundle, §03.4 icosahedral A_5 structure;
legacy §10, §11, §16.
"""

from __future__ import annotations

from math import sqrt
from typing import Dict, Tuple

from .constants import G_E_OVER_2
from .gravity import pentachoron_directed_edge_count


# =============================================================================
# Quaternion arithmetic
# =============================================================================

Quaternion = Tuple[float, float, float, float]
Vector3 = Tuple[float, float, float]


def q_normalize(q: Quaternion) -> Quaternion:
    n = sqrt(sum(x * x for x in q))
    if n == 0:
        raise ValueError("Cannot normalize zero quaternion.")
    return tuple(x / n for x in q)  # type: ignore[return-value]


def q_conjugate(q: Quaternion) -> Quaternion:
    w, x, y, z = q
    return (w, -x, -y, -z)


def q_multiply(a: Quaternion, b: Quaternion) -> Quaternion:
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    )


def hopf_projection(q: Quaternion) -> Vector3:
    """
    Hopf projection q in S^3 -> S^2, implemented by rotating the z-axis:
        q * k * q^{-1}
    """
    import cmath  # noqa: F401  (cmath unused, retained for consistency)
    qn = q_normalize(q)
    k = (0.0, 0.0, 0.0, 1.0)
    rotated = q_multiply(q_multiply(qn, k), q_conjugate(qn))
    _, x, y, z = rotated
    return (x, y, z)


def hopf_fiber_phase(theta: float) -> complex:
    """U(1) fiber phase exp(i*theta)."""
    import cmath
    return cmath.exp(1j * theta)


def electron_hopf_fiber_holonomy(g_over_2: float = G_E_OVER_2) -> float:
    """Framework interpretation: g_e/2 as spin / Hopf-fiber holonomy scalar."""
    return g_over_2


# =============================================================================
# A_5 and pentachoron symmetry
# =============================================================================

def alternating_group_A5_order() -> int:
    """Order of A_5, the orientation-preserving symmetry group of the pentachoron."""
    return 60


def pentachoron_cell_count() -> int:
    """Boundary of a pentachoron has five tetrahedral 3-cells."""
    return 5


def a5_address_sector_count(z21_count: int = 21) -> int:
    """Combined discrete A_5 x Z_21 sector count."""
    return alternating_group_A5_order() * z21_count


def crystallographic_threshold_pentachoron() -> Dict[str, object]:
    """
    Crystallographic threshold at the pentachoron:

      - Tetrahedron has crystallographic rotation orders 2, 3.
      - Pentachoron symmetry group is S_5 of order 120 = 2^3 * 3 * 5.
      - The factor 5 marks a non-crystallographic rotation order in 3D.
      - alpha^20 is the cost of crossing from the 3D crystallographic tetrad
        into the 4D next-simplex pentachoron edge network.
    """
    s5_order = 120
    factorization = {2: 3, 3: 1, 5: 1}
    return {
        "polytope": "pentachoron / 4-simplex",
        "vertices": 5,
        "directed_edges": pentachoron_directed_edge_count(),
        "symmetry_group": "S5",
        "symmetry_group_order": s5_order,
        "factorization": factorization,
        "has_5fold_factor": True,
        "interpretation": (
            "5-fold symmetry appears at the next simplex; "
            "5-fold rotations are non-crystallographic in 3D lattices."
        ),
    }


# =============================================================================
# Null-cone associator status (Clifford closure)
# =============================================================================

def null_cone_associator_status() -> Dict[str, object]:
    """
    Status table recovered from the null-cone closure algebra notes:

      - 48/512 basis triples have nonzero associator
      - Nonzero associator lands axially in <1, I>
      - Support patterns: AMM and MMA

    This records the algebraic test status; full Clifford closure tests are
    elsewhere.
    """
    return {
        "basis_triples": 512,
        "nonzero_associator_triples": 48,
        "image_subspace": "<1, I> axial sector",
        "nonzero_support_patterns": ["AMM", "MMA"],
        "vanishing_patterns": ["AAA", "AAM", "AMA", "MAA", "MAM", "MMM"],
        "physics_reading": "middle-sector circulation can generate axial curvature / source defect",
        "status": "documented / tested in null-cone closure algebra notes",
    }


# =============================================================================
# SU(2) Chern-Simons and WRT invariant of Sigma(2, 3, 5)
# =============================================================================
#
# In SU(2)_k Chern-Simons theory the relevant integer is the "shifted level"
# k + 2, which counts integrable representations and indexes the quantum
# parameter q = exp(2 pi i / (k + 2)).
#
# The framework realizes its Phi_3(4) = 21 = Phi_6(5) hinge as the shifted
# level k + 2 = 21, i.e. k = 19. The central charge is c = 3k / (k + 2) =
# 3 * 19 / 21 = 57/21 = 19/7.
#
# The WRT invariant tau_k(Sigma(2, 3, 5)) of the Poincaré homology sphere
# at level k carries the global obstruction information of the framework
# (project §03.6); at the framework's level k = 19 the numerical reference
# value |tau_21| = 8.0962 (computed via the Lawrence-Rozansky-Hikami
# formula in the project's `cs_calc/` companion notebook).

def wrt_su2_level_to_k_plus_2(k: int) -> int:
    """
    SU(2)_k Chern-Simons shifted level. The framework reads this directly:
        k = 19  ->  k + 2 = 21 = Phi_3(4) = Phi_6(5).
    """
    return k + 2


def wrt_central_charge(k: int) -> float:
    """
    Affine SU(2)_k central charge:
        c = 3 k / (k + 2)

    At k = 19: c = 57 / 21 = 19 / 7. This is the framework's
    operator-content rank fraction.
    """
    return 3.0 * k / (k + 2)


def wrt_su2_19_chern_simons() -> Dict[str, object]:
    """
    Canonical SU(2)_19 Chern-Simons data of the framework.

      - level k = 19
      - shifted level k + 2 = 21
      - integrable representations indexed by 0, 1/2, ..., k/2 = 19/2 (20 in total)
      - central charge c = 3 k / (k + 2) = 19 / 7
    """
    k = 19
    return {
        "level_k":           k,
        "shifted_level":     wrt_su2_level_to_k_plus_2(k),
        "integrable_reps":   k + 1,                  # 20
        "central_charge":    wrt_central_charge(k),  # 19/7
        "central_charge_fraction": "19/7",
        "framework_role":    "shifted level 21 = Phi_3(4) = Phi_6(5)",
    }


# Numerical reference value for the WRT invariant at the framework's level,
# computed elsewhere (project's cs_calc companion) and pinned here as a
# regression target.
_WRT_TAU_21_SIGMA_235_ABS_REFERENCE = 8.0962


def wrt_invariant_sigma235_target(level: int = 21) -> Dict[str, object]:
    """
    Numerical regression target for the WRT invariant of the Poincaré
    homology sphere Sigma(2, 3, 5) at SU(2)_(k+2) shifted level.

    At the framework's level k + 2 = 21 (i.e. k = 19), the absolute value
    |tau_21(Sigma(2, 3, 5))| = 8.0962 is pinned as a regression reference;
    the full computation lives in the project's cs_calc/ companion via the
    Lawrence-Rozansky-Hikami formula.
    """
    if level != 21:
        return {
            "level":         level,
            "available":     False,
            "comment":       "only level 21 has a pinned reference value here",
        }
    return {
        "level":              level,
        "manifold":           "Poincare homology sphere Sigma(2, 3, 5)",
        "formula":            "Lawrence-Rozansky-Hikami",
        "abs_tau_reference":  _WRT_TAU_21_SIGMA_235_ABS_REFERENCE,
        "computation_source": "project cs_calc/ companion",
        "status":             "regression target (numerical pin)",
    }
