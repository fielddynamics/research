"""
predictions.py
==============

Numerical predictions and algebraic extrapolations of the framework:

  - Coffer / chamber alpha-volume step (apparatus identification)
  - Relieving-chamber volume prediction
  - Sierpinski force hierarchy across K levels
  - K=2 -> Schwinger 2*pi loop structure
  - Lepton-anchor calculation across charged-lepton flavors
  - Golden impedance split

References: project §07 predictions and tests; legacy §13, §16.
"""

from __future__ import annotations

from fractions import Fraction
from math import sqrt
from typing import Dict, List, Sequence

from .constants import ALPHA, C_LIGHT, G_E_OVER_2, HBAR
from .cyclotomic import phi3, phi4, phi6, sphere_surface_area_unit
from .gravity import tetrad_impedance_ratio


# =============================================================================
# Coffer / chamber alpha-volume step
# =============================================================================

def coffer_chamber_alpha_step(
    chamber_volume_cubits3: float = 1000 * sqrt(5),
    coffer_external_volume_cubits3: float = 16.19,
    alpha: float = ALPHA,
) -> Dict[str, float]:
    """
    Coffer / chamber alpha-step identification:
        alpha_geom = V_coffer / V_chamber  approx  alpha
    """
    alpha_geom = coffer_external_volume_cubits3 / chamber_volume_cubits3
    return {
        "V_chamber_cubits3": chamber_volume_cubits3,
        "V_coffer_ext_cubits3": coffer_external_volume_cubits3,
        "V_chamber_over_V_coffer": chamber_volume_cubits3 / coffer_external_volume_cubits3,
        "alpha_geom_V_coffer_over_V_chamber": alpha_geom,
        "alpha": alpha,
        "relative_error_vs_alpha": abs(alpha_geom - alpha) / alpha,
    }


def relieving_chamber_volume_prediction(
    chamber_volume_cubits3: float = 1000 * sqrt(5),
    alpha: float = ALPHA,
    K: int = 5,
) -> float:
    """
    Total relieving-chamber volume prediction:
        V_relieving  approx  K * alpha * V_chamber  for K = 5
    """
    return K * alpha * chamber_volume_cubits3


# =============================================================================
# Sierpinski force hierarchy
# =============================================================================

def sierpinski_force_hierarchy(
    levels: Sequence[int] = (2, 4, 16, 256),
    alpha: float = ALPHA,
) -> List[Dict[str, object]]:
    """
    Sierpinski hierarchy across K levels.

    Only K=4 is observationally matched to gravity; other levels are algebraic
    extrapolations along the K -> K^2 scale-fusion ladder.
    """
    rows: List[Dict[str, object]] = [
        {
            "label": "bare Coulomb",
            "K": None,
            "gap_exponent_KKplus1": None,
            "full_exponent_Phi3": 1,
            "attenuation": alpha,
            "cyclotomic_ratio": None,
            "status": "observed bare coupling",
        }
    ]
    for K in levels:
        ratio = phi4(K) / phi6(K)
        rows.append({
            "label": f"K={K} shell read",
            "K": K,
            "gap_exponent_KKplus1": K * (K + 1),
            "full_exponent_Phi3": phi3(K),
            "attenuation": alpha ** phi3(K),
            "cyclotomic_ratio": ratio,
            "status": "gravity match" if K == 4 else "algebraic extrapolation",
        })
    return rows


# =============================================================================
# K=2 -> Schwinger 2*pi structure
# =============================================================================

def k2_schwinger_loop_structure(alpha: float = ALPHA) -> Dict[str, float | str]:
    """
    K=2 structural hypothesis:

    At K=2, frame directions lie on S^(K-1) = S^1, whose measure is 2*pi.
    The first Schwinger term is alpha / (2*pi).
    """
    s1_volume = sphere_surface_area_unit(1)
    first_order = alpha / s1_volume
    return {
        "K": 2,
        "sphere": "S^1",
        "S1_volume": s1_volume,
        "schwinger_first_order_alpha_over_2pi": first_order,
        "g_over_2_first_order": 1 + first_order,
        "status": "structural hypothesis, not rigorous derivation",
    }


# =============================================================================
# Lepton anchor
# =============================================================================

def lepton_anchor_report(
    mass_kg: float,
    g_over_2: float,
    alpha: float = ALPHA,
    hbar: float = HBAR,
    c: float = C_LIGHT,
) -> Dict[str, float]:
    """
    General mass-anchor calculation:
        G_anchored = alpha_G(g_l) * hbar * c / m^2

    Framework position on charged 'leptons':

      The framework does NOT treat the muon and tau as independent
      particles. They are structural mode configurations of the same
      vortex, viewed through Generations 1, 2, 3:

        electron: Generation 1, 1 mode  (irreducible single excitation)
        muon:     Generation 2, ~207 m_e  (9 closure x 23 asymmetry)
        tau:      Generation 3, ~3477 m_e  (51 x 68 + 9)

      The framework's gravity formula anchors at m_e because the electron
      is the unique irreducible single-mode generation. Substituting a
      heavier mass produces a dimensional rescaling of G by (m_e / m)^2 --
      this is NOT a falsifying probe of the framework, because the muon
      and tau are not independent anchors. They are projections of the
      same closure structure.

      The tree-level coupling alpha_G^tree = (17/13) * alpha^21 is
      lepton-independent. The g_l/2 anomalous-moment factor is structurally
      tied to Generation 1 (the electron).

    This function is therefore primarily diagnostic: it answers the
    arithmetic question 'what value of G would the formula return if
    anchored at this mass?', without making any framework claim about
    the independence of the anchor.
    """
    alphaG_l = (alpha ** 21) * float(tetrad_impedance_ratio()) * g_over_2
    return {
        "mass_kg": mass_kg,
        "g_over_2": g_over_2,
        "alphaG_l": alphaG_l,
        "G_from_this_lepton_anchor": alphaG_l * hbar * c / (mass_kg * mass_kg),
    }


# =============================================================================
# Golden impedance split
# =============================================================================

def golden_impedance_split() -> Dict[str, object]:
    """
    Null-cone / golden-impedance split:
        Raw exterior:  24/64 = 3/8
        Refined:       13/34  approx  1/phi^2
    """
    phi = (1 + sqrt(5)) / 2
    return {
        "exterior_raw_fraction": Fraction(24, 64),
        "exterior_raw_float": 24 / 64,
        "refined_fraction": Fraction(13, 34),
        "refined_float": 13 / 34,
        "golden_complement_inverse_phi_squared": 1 / (phi * phi),
        "difference": (13 / 34) - (1 / (phi * phi)),
    }
