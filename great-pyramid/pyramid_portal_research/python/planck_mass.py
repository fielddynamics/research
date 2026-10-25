"""
planck_mass.py
================

The Planck-to-electron mass ratio from K=4 framework α_G.

FRAMEWORK PREDICTION:

    α_G = α^{dim T_4} · (dim E_4 / sdim T_4) · (g_e / 2)
        = α^21 · (17/13) · (g_e/2)

    m_P / m_e = 1 / √α_G
              = 1 / √(α^21 · 17/13 · g_e/2)
              = α^(-21/2) · √(13/17) · √(2/g_e)

At framework α (or CODATA α):

    α_G_framework = 1.7518 × 10⁻⁴⁵
    m_P / m_e     = 2.389 × 10²²

    Measured (CODATA G):  2.389 × 10²²
    Deviation:            +7 ppm

The framework predicts the 22-orders-of-magnitude span between the
electron mass and the Planck mass to 7 ppm precision.

STRUCTURAL READING:

    α^(-21/2) = α^(-dim T_4 / 2)   ← half-tile inverse-α attenuation
    √(13/17)  = √(sdim T_4 / dim E_4)  ← parity-twist root
    √(2/g_e)  = inverse √(g_e/2)    ← g-factor square root

The Planck-to-electron mass ratio is the square root of the inverse
gravity coupling, which is determined by K=4 tile algebra plus g_e.

CONNECTION:

    m_p / m_P = √α_G · (m_p / m_e)
              = √(α^21 · 17/13 · g_e/2) · (K·D³·Φ_4 + Φ_3·α/(1+α/2) − ...)

The proton-to-Planck mass ratio combines two framework predictions:
gravity tile attenuation × proton-electron mass ratio.
"""

from __future__ import annotations
from typing import Dict, List

import math


# ---------------------------------------------------------------------------
# Framework constants
# ---------------------------------------------------------------------------

K = 4
D = 3
DIM_T_4 = 21               # = Φ_3 = full tile dim
DIM_E_4 = 17                # = Φ_4 = even sector
SDIM_T_4 = 13               # = Φ_6 = superdimension

G_E_OVER_2 = 1.00115965218128   # CODATA electron g-factor anomaly

ALPHA_CODATA = 7.2973525693e-3      # = 1/137.035999084
ALPHA_FRAMEWORK_2ND = 1.0 / 137.036  # framework second-order (AW 29)

# CODATA-derived measured value
M_PLANCK_OVER_M_E_MEASURED = 2.38922e22   # m_P/m_e using G=6.6743e-11, m_e=9.109e-31

# Standard CODATA values for verification
G_CODATA = 6.6743e-11           # m³ kg⁻¹ s⁻²
HBAR_CODATA = 1.054571817e-34   # J·s
C_EXACT = 299792458.0            # m/s (exact, SI redef)
M_E_KG = 9.1093837015e-31        # kg


# ---------------------------------------------------------------------------
# Framework predictions
# ---------------------------------------------------------------------------

def alpha_G_framework(alpha: float = ALPHA_CODATA) -> float:
    """Framework α_G = α^21 · (17/13) · (g_e/2)."""
    return alpha**DIM_T_4 * (DIM_E_4 / SDIM_T_4) * G_E_OVER_2


def m_planck_over_m_e_framework(alpha: float = ALPHA_CODATA) -> float:
    """Framework prediction: m_P/m_e = 1/√α_G_framework.

    = α^(-21/2) · √(13/17) · √(2/g_e)
    """
    return 1.0 / math.sqrt(alpha_G_framework(alpha))


def m_planck_over_m_e_decomposition(alpha: float = ALPHA_CODATA) -> Dict[str, float]:
    """Three-factor decomposition of m_P/m_e.

        m_P/m_e = α^(-dim T_4 / 2)  ·  √(sdim T_4 / dim E_4)  ·  √(2/g_e)
                = α^(-21/2)         ·  √(13/17)               ·  √(2/g_e)

    Each factor reads from K=4 framework structure.
    """
    alpha_half_attenuation = alpha**(-DIM_T_4 / 2)
    parity_root = math.sqrt(SDIM_T_4 / DIM_E_4)
    g_factor_root = math.sqrt(2.0 / (2 * G_E_OVER_2))   # = 1/√(g_e/2)
    return {
        "alpha_half_attenuation": alpha_half_attenuation,
        "alpha_to_minus_21_over_2": alpha_half_attenuation,
        "parity_root_sqrt_13_over_17": parity_root,
        "g_factor_root_1_over_sqrt_ge2": g_factor_root,
        "product": alpha_half_attenuation * parity_root * g_factor_root,
        "reads_as": "α^(-dim T_4 /2) · √(sdim/dim_E) · 1/√(g_e/2)",
    }


def planck_mass_audit(alpha: float = ALPHA_CODATA) -> Dict[str, float]:
    """Full audit of m_P/m_e prediction with measurement comparison."""
    framework = m_planck_over_m_e_framework(alpha)
    deviation_ppm = (framework - M_PLANCK_OVER_M_E_MEASURED) / M_PLANCK_OVER_M_E_MEASURED * 1e6
    return {
        "alpha": alpha,
        "alpha_G_framework": alpha_G_framework(alpha),
        "m_P_over_m_e_framework": framework,
        "m_P_over_m_e_measured": M_PLANCK_OVER_M_E_MEASURED,
        "deviation_ppm": deviation_ppm,
        "log10_m_P_over_m_e": math.log10(framework),
        "orders_of_magnitude": int(math.log10(framework)),
    }


def m_p_over_m_planck(alpha: float = ALPHA_CODATA, m_p_over_m_e: float = 1836.152673) -> Dict[str, float]:
    """Proton-to-Planck mass ratio: combines AW 31 (α_G) and AW 32 (m_p/m_e).

        m_p / m_P = (m_p / m_e) / (m_P / m_e)
                  = √α_G_framework · (m_p / m_e)
    """
    sqrt_alpha_G = math.sqrt(alpha_G_framework(alpha))
    ratio = sqrt_alpha_G * m_p_over_m_e / (m_p_over_m_e / m_p_over_m_e)
    # Equivalent: m_p/m_P = (m_p/m_e) / (m_P/m_e)
    m_P_over_m_e = m_planck_over_m_e_framework(alpha)
    return {
        "m_p_over_m_e": m_p_over_m_e,
        "m_P_over_m_e": m_P_over_m_e,
        "m_p_over_m_P": m_p_over_m_e / m_P_over_m_e,
        "sqrt_alpha_G": sqrt_alpha_G,
        "alt_formula": "m_p/m_P = √α_G · (m_p/m_e)",
        "alt_value": sqrt_alpha_G * m_p_over_m_e,
    }


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def showcase_planck_mass() -> List[str]:
    lines: List[str] = []
    lines.append("=" * 80)
    lines.append("  PLANCK-TO-ELECTRON MASS RATIO FROM K=4 FRAMEWORK")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  FRAMEWORK PREDICTION:")
    lines.append("")
    lines.append("    m_P / m_e = 1 / √α_G")
    lines.append("              = 1 / √(α^21 · 17/13 · g_e/2)")
    lines.append("              = α^(-21/2) · √(13/17) · √(2/g_e)")
    lines.append("")
    a = planck_mass_audit()
    lines.append(f"    α_G framework        = {a['alpha_G_framework']:.4e}")
    lines.append(f"    m_P/m_e framework    = {a['m_P_over_m_e_framework']:.6e}")
    lines.append(f"    m_P/m_e measured     = {a['m_P_over_m_e_measured']:.6e}")
    lines.append(f"    Deviation            = {a['deviation_ppm']:+.1f} ppm")
    lines.append(f"    Orders of magnitude  = 10^{a['log10_m_P_over_m_e']:.2f}")
    lines.append("")
    d = m_planck_over_m_e_decomposition()
    lines.append("  THREE-FACTOR DECOMPOSITION:")
    lines.append("")
    lines.append(f"    α^(-21/2)  = α^(−dim T_4 / 2)        = {d['alpha_half_attenuation']:.4e}")
    lines.append(f"    √(13/17)   = √(sdim T_4 / dim E_4)   = {d['parity_root_sqrt_13_over_17']:.6f}")
    lines.append(f"    1/√(g_e/2) = inverse g-factor root    = {d['g_factor_root_1_over_sqrt_ge2']:.6f}")
    lines.append(f"    ────────────────────────────────────────")
    lines.append(f"    Product = {d['product']:.6e}")
    lines.append("")
    lines.append("  STRUCTURAL READING:")
    lines.append("")
    lines.append("    α^(-21/2)   = half-tile-dim inverse-α attenuation")
    lines.append("    √(sdim/dimE) = parity-twist root of K=4 trio")
    lines.append("    √(2/g_e)    = inverse g-factor square root")
    lines.append("")
    lines.append("    The 22-order span from electron mass to Planck mass")
    lines.append("    is determined by HALF the gravity tile dimension")
    lines.append("    in α-units, plus the parity ratio and g_e.")
    lines.append("")
    p = m_p_over_m_planck()
    lines.append("  CONNECTION: m_p / m_Planck  (AW 31 × AW 32)")
    lines.append("")
    lines.append(f"    m_p / m_P = √α_G · (m_p / m_e)")
    lines.append(f"             = {p['m_p_over_m_P']:.4e}")
    lines.append(f"             = (m_p/m_e) / (m_P/m_e)")
    lines.append(f"             = {p['m_p_over_m_e']} / {p['m_P_over_m_e']:.4e}")
    lines.append("")
    lines.append("    The proton-to-Planck mass ratio combines:")
    lines.append("      • α_G framework (K=4 gravity coupling) — AW 31")
    lines.append("      • m_p/m_e framework (K=4 mass ratio) — AW 32")
    return lines


__all__ = [
    "K", "D", "DIM_T_4", "DIM_E_4", "SDIM_T_4",
    "G_E_OVER_2",
    "ALPHA_CODATA", "ALPHA_FRAMEWORK_2ND",
    "M_PLANCK_OVER_M_E_MEASURED",
    "alpha_G_framework",
    "m_planck_over_m_e_framework",
    "m_planck_over_m_e_decomposition",
    "planck_mass_audit",
    "m_p_over_m_planck",
    "showcase_planck_mass",
]
