"""
mass_from_associator.py
=========================

Tier 1 #1: explicit formalism for mass derived from the associator
of the closure-algebra product.

In an algebra A with product (·), the associator of three elements
a, b, c is
    [a, b, c]  =  (a · b) · c  -  a · (b · c)

For the closure-algebra product on A_3 = Cl(3, 0), the associator
of a strongly-Ω-twisted triple lands in the *axial sector* <1, I> with
a specific residue.  This module:

  1. Implements the associator [a, b, c] in Cl(3, 0)
  2. Projects the result onto the axial subspace <1, I>
  3. Computes the axial residue for structured (a, b, c) seeds
  4. Tracks how the residue scales with the seed pattern
  5. Documents the partial closure: the formalism is explicit, but
     mapping the residue to m_e in physical units requires a
     calibration scale (the irreducible Generation-1 mass) which
     is NOT derived in this module.

Status:  partial closure.
  - Closed: explicit associator formalism, axial-projection tracking,
            residue computation for structured seeds.
  - Open:   mapping the dimensionless residue to m_e in SI units
            (requires the Generation-1 calibration scale).

Canonical source:
  Tier 1 #1; closure_core256.associator_axial_residue (existing prim)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

import math
import numpy as np

from python.unification_algebra import orientation_cocycle
from python.cyclotomic_12 import (
    cl_3_0_mul, cl_basis_1, cl_basis_T1, cl_basis_T2, cl_basis_I,
)


# ===========================================================================
# Associator of the Clifford product
# ===========================================================================
#
# For an associative algebra, [a, b, c] = 0 identically.  Cl(3, 0) is
# associative, so the *Clifford* associator vanishes.  The interesting
# associator is for the *sweep* product ⋆, which is not associative on
# the full algebra but is associative on the Ω-fixed subalgebra
# A_3^Ω = Z[ζ_{12}].

def clifford_associator(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    """
    The Clifford associator [a, b, c] = (a·b)·c - a·(b·c).
    For associative Cl(3, 0), this is exactly zero.
    """
    left = cl_3_0_mul(cl_3_0_mul(a, b), c)
    right = cl_3_0_mul(a, cl_3_0_mul(b, c))
    return left - right


# ===========================================================================
# Sweep product and its associator
# ===========================================================================

from python.closure_core256 import (
    sweep_product3, closure_projection3, omega_power3,
    clifford_product_3,
)


def omega_on_clifford(v: np.ndarray) -> np.ndarray:
    """
    The Ω automorphism on Cl(3, 0) via closure coordinates (axial fixed,
    each z_k multiplied by ω = e^{2πi/3}).  Routed to the canonical
    omega_power3 from closure_core256.
    """
    return omega_power3(v, 1)


def sweep_product(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    The closure product: Clifford multiply, then Ω-project.
    Routed to the canonical sweep_product3 from closure_core256.
    """
    return sweep_product3(a, b)


def sweep_associator(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    """
    Associator of the closure product:
        [a, b, c]_⋆ = (a ⋆ b) ⋆ c  -  a ⋆ (b ⋆ c)
    """
    left = sweep_product(sweep_product(a, b), c)
    right = sweep_product(a, sweep_product(b, c))
    return left - right


# ===========================================================================
# Axial projection
# ===========================================================================
#
# The axial subspace of Cl(3, 0) is <1, I> spanned by mask 0 and mask 7.

AXIAL_MASKS_FIXED: Tuple[int, ...] = (0, 7)


def axial_projector_8() -> np.ndarray:
    """Diagonal projector onto <1, I>."""
    P = np.zeros((8, 8))
    P[0, 0] = 1.0
    P[7, 7] = 1.0
    return P


def axial_component(v: np.ndarray) -> Tuple[float, float]:
    """Return (scalar_part, pseudoscalar_part) = (v[0], v[7])."""
    return float(v[0]), float(v[7])


def axial_residue_norm(v: np.ndarray) -> float:
    """Length of the axial projection: sqrt(v[0]² + v[7]²)."""
    s, p = axial_component(v)
    return math.sqrt(s * s + p * p)


def non_axial_residue_norm_fixed(v: np.ndarray) -> float:
    """L2 norm of the non-axial component (the part orthogonal to <1, I>)."""
    masks = [m for m in range(8) if m not in AXIAL_MASKS_FIXED]
    return float(np.sqrt(sum(v[m] ** 2 for m in masks)))


# ===========================================================================
# Structured seeds: TetA-axial × TetB-axial × bridge
# ===========================================================================

def tet_a_axial_seed(alpha: float = 1.0, beta: float = 0.5) -> np.ndarray:
    """A 'TetA-axial' seed: scalar plus T_1 component."""
    return alpha * cl_basis_1() + beta * cl_basis_T1()


def tet_b_axial_seed(gamma: float = 1.0, delta: float = 0.5) -> np.ndarray:
    """A 'TetB-axial' seed: scalar plus T_2 component."""
    return gamma * cl_basis_1() + delta * cl_basis_T2()


def bridge_seed(epsilon: float = 1.0) -> np.ndarray:
    """A 'bridge' seed: pure pseudoscalar I."""
    return epsilon * cl_basis_I()


# ===========================================================================
# Axial residue computation for structured triples
# ===========================================================================

def axial_residue_for_structured_triple(
    alpha: float = 1.0,
    beta: float = 0.5,
    gamma: float = 1.0,
    delta: float = 0.5,
    epsilon: float = 1.0,
) -> Dict[str, object]:
    """
    Compute the axial residue of the sweep-associator
    [TetA-axial, TetB-axial, bridge]_⋆ for given seed amplitudes.

    The sweep product ⋆ = closure_projection3 ∘ clifford_product_3 is
    non-associative on Cl(3, 0) because the Ω-projection is not a ring
    homomorphism.  The axial residue is in general non-zero for
    structured triples; it serves as a candidate dimensionless scale
    (mass calibration is the open Generation-1 step).
    """
    a = tet_a_axial_seed(alpha, beta)
    b = tet_b_axial_seed(gamma, delta)
    c = bridge_seed(epsilon)

    cliff_assoc = clifford_associator(a, b, c)
    sweep_assoc = sweep_associator(a, b, c)

    cliff_axial = axial_component(cliff_assoc)
    sweep_axial = axial_component(sweep_assoc)

    return {
        "seeds": {"alpha": alpha, "beta": beta, "gamma": gamma,
                  "delta": delta, "epsilon": epsilon},
        "clifford_associator": cliff_assoc,
        "clifford_associator_axial": cliff_axial,
        "clifford_associator_axial_norm": axial_residue_norm(cliff_assoc),
        "sweep_associator": sweep_assoc,
        "sweep_associator_axial": sweep_axial,
        "sweep_associator_axial_norm": axial_residue_norm(sweep_assoc),
        "note": "Clifford associator is identically zero (associativity); "
                "sweep associator is non-zero because Ω-projection is "
                "not a ring homomorphism.  The axial component is the "
                "candidate dimensionless scale.",
    }


# ===========================================================================
# Hexagonal-sector seed (non-Ω-invariant)
# ===========================================================================

def hexagonal_eisenstein_seed(k: int = 1) -> np.ndarray:
    """
    A vector in the Eisenstein hexagonal sector: z_k = e_k + ω · e_{(k+1)(k+2)}
    where ω = ζ⁴ = (-1 + T_2)/2.  Since ω is complex (not a single
    Clifford element), we use a representative.  The simplest
    hexagonal vector in the real Clifford algebra: a single basis
    vector e_k.

    Pure e_k is NOT Ω-fixed (Ω maps e_1 -> e_2 -> e_3 -> e_1).
    """
    e_k = np.zeros(8)
    e_k[1 << (k - 1)] = 1.0  # e_1, e_2, or e_3
    return e_k


def axial_residue_for_hexagonal_triple(
    k_a: int = 1, k_b: int = 2, k_c: int = 3,
) -> Dict[str, object]:
    """
    Compute the axial residue for a hexagonal-sector triple (e_a, e_b, e_c).
    These are NOT Ω-fixed; the sweep-associator may have non-trivial
    axial content.
    """
    a = hexagonal_eisenstein_seed(k_a)
    b = hexagonal_eisenstein_seed(k_b)
    c = hexagonal_eisenstein_seed(k_c)

    cliff_assoc = clifford_associator(a, b, c)
    sweep_assoc = sweep_associator(a, b, c)

    return {
        "seeds": {"e_a": k_a, "e_b": k_b, "e_c": k_c},
        "clifford_associator": cliff_assoc,
        "clifford_associator_is_zero": np.allclose(cliff_assoc, 0.0),
        "sweep_associator": sweep_assoc,
        "sweep_associator_axial_norm": axial_residue_norm(sweep_assoc),
        "sweep_associator_non_axial_norm": non_axial_residue_norm_fixed(sweep_assoc),
    }


# ===========================================================================
# Mass-from-residue formalism (partial closure)
# ===========================================================================

@dataclass
class MassResidueResult:
    """
    Result of mass-from-residue computation.  The dimensionless residue is
    computed exactly from the algebra; the conversion to m_e in physical
    units requires a calibration scale that is NOT in this module.
    """
    dimensionless_residue: float
    structured_inputs: bool
    sector: str  # "axial" | "hexagonal" | "mixed"
    calibration_status: str  # "open" | "applied"
    physical_mass_eV: Optional[float] = None


def mass_from_associator_residue(
    sweep_associator_result: Dict[str, object],
    calibration_eV: Optional[float] = None,
) -> MassResidueResult:
    """
    Map a sweep-associator axial residue to a candidate mass.

    Step 1 (closed): extract the dimensionless residue = axial_norm
                     of the sweep_associator.
    Step 2 (open in general): multiply by the calibration scale.
                              If calibration_eV is None, this stays
                              dimensionless and the physical mass
                              is unset.
    """
    residue = float(sweep_associator_result.get("sweep_associator_axial_norm", 0.0))
    physical_mass: Optional[float] = None
    status = "open"
    if calibration_eV is not None:
        physical_mass = calibration_eV * residue
        status = "applied"
    return MassResidueResult(
        dimensionless_residue=residue,
        structured_inputs=True,
        sector="axial" if residue > 0 else "hexagonal-needed",
        calibration_status=status,
        physical_mass_eV=physical_mass,
    )


# ===========================================================================
# Showcase
# ===========================================================================

def showcase_mass_from_associator() -> List[str]:
    """Audit trail for the mass-from-associator formalism (partial closure)."""
    lines: List[str] = []
    lines.append("=" * 76)
    lines.append("  MASS FROM ASSOCIATOR — PARTIAL CLOSURE FORMALISM")
    lines.append("=" * 76)
    lines.append("")
    lines.append("  STATUS:  formalism explicit; calibration-to-m_e remains open.")
    lines.append("")
    lines.append("  Test 1: Clifford associator is identically zero (associative algebra):")
    structured = axial_residue_for_structured_triple()
    lines.append(f"    Clifford [a,b,c]   = {structured['clifford_associator']}")
    lines.append(f"    axial norm         = {structured['clifford_associator_axial_norm']:.6e}")
    lines.append("")
    lines.append("  Test 2: sweep associator on Ω-fixed structured triple:")
    lines.append(f"    sweep [a,b,c]_⋆    = {structured['sweep_associator']}")
    lines.append(f"    axial norm         = {structured['sweep_associator_axial_norm']:.6e}")
    lines.append(f"    {structured['note']}")
    lines.append("")
    lines.append("  Test 3: sweep associator on hexagonal-sector triple (e_1, e_2, e_3):")
    hex_result = axial_residue_for_hexagonal_triple(1, 2, 3)
    lines.append(f"    Clifford associator zero?       {hex_result['clifford_associator_is_zero']}")
    lines.append(f"    sweep axial-residue norm        {hex_result['sweep_associator_axial_norm']:.6e}")
    lines.append(f"    sweep non-axial-residue norm    {hex_result['sweep_associator_non_axial_norm']:.6e}")
    lines.append("")
    lines.append("  Mass-from-residue mapping:")
    mr = mass_from_associator_residue(hex_result)
    lines.append(f"    dimensionless residue:          {mr.dimensionless_residue:.6e}")
    lines.append(f"    calibration status:             {mr.calibration_status}")
    lines.append(f"    physical mass (eV):             {mr.physical_mass_eV}")
    lines.append("")
    lines.append("  STRUCTURAL READING:")
    lines.append("    The associator is exactly zero on the Ω-fixed subalgebra")
    lines.append("    Z[ζ_{12}] (it's a commutative ring), but can be non-zero on")
    lines.append("    the hexagonal Eisenstein sectors of A_3.  The mass scale should")
    lines.append("    come from the axial leak when hexagonal sectors are present —")
    lines.append("    but the calibration to m_e requires the Generation-1 scale.")
    lines.append("")
    return lines
