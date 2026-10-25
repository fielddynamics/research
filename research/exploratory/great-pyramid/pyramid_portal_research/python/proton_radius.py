"""
proton_radius.py
==================

Proton charge radius from K=4 framework.

FRAMEWORK PREDICTION:

    r_p = K · λ_C_bar(p) = K · ℏ / (m_p · c)

where λ_C_bar(p) is the reduced Compton wavelength of the proton.

At K=4:

    r_p = 4 · ℏ/(m_p·c)
        = 4 · 2.1031 × 10⁻¹⁶ m
        = 0.8412 fm

    CODATA r_p (2018):  0.8414 ± 0.0019 fm  (puzzle: range 0.8331–0.8775)
    Deviation:           −195 ppm (within CODATA uncertainty)

STRUCTURAL READING:

    K            = coupling pathway count at uniqueness
                 = D+1 = 4 (number of spacetime axes)
    λ_C_bar(p)   = reduced Compton wavelength of proton

    r_p = (coupling pathways) × (reduced Compton wavelength)

The proton charge radius equals K times its reduced Compton wavelength.
This connects the K=4 framework's coupling pathway count directly to
the proton's spatial extent.

CONNECTION TO PROTON MASS:

    From AW 32: m_p/m_e = K·D³·Φ_4 + α-corrections (to 15 ppt)
    Here:        r_p / λ_C_bar(p) = K  (to 200 ppm)

    Combining: r_p / λ_C_bar(e) = K · m_e/m_p = K/(K·D³·Φ_4 + α-corr)
                                = 1/(D³·Φ_4 + α-corr/K)
                                ≈ 1/(27·17) = 1/459 (to leading order)

The proton charge radius in electron-Compton units is set by the
inverse of the integer factor D³·Φ_4 that determines m_p/m_e bulk.

PROTON RADIUS PUZZLE:

    Muonic hydrogen Lamb shift: 0.84087(39) fm
    Electron-proton scattering: 0.8775(50) fm (older value)
    H spectroscopy (Mainz):     0.8335(95) fm
    PRad-II (2019):             0.831(14) fm
    Modern average:             0.8414(19) fm

The puzzle: muonic measurements gave significantly smaller value than
electron scattering. Current values are converging on ~0.841 fm.

Framework prediction 0.8412 fm sits within the modern consensus range.
"""

from __future__ import annotations
from typing import Dict, List


# ---------------------------------------------------------------------------
# Framework constants
# ---------------------------------------------------------------------------

K = 4
D = 3
PHI_4 = 1 + K**2          # 17

# CODATA 2018 reference values
HBAR_CODATA = 1.054571817e-34   # J·s (exact since SI redef)
C_EXACT = 299792458.0            # m/s (exact)
M_P_KG = 1.67262192369e-27       # kg (CODATA 2018)
M_E_KG = 9.1093837015e-31         # kg

R_P_CODATA = 0.8414e-15            # m (CODATA 2018)
R_P_UNCERTAINTY = 0.0019e-15       # m (~2300 ppm)


# ---------------------------------------------------------------------------
# Predictions
# ---------------------------------------------------------------------------

def reduced_compton_wavelength(mass_kg: float) -> float:
    """λ_C_bar = ℏ / (m · c)."""
    return HBAR_CODATA / (mass_kg * C_EXACT)


def proton_compton_wavelength() -> float:
    """λ_C_bar(p) at CODATA m_p."""
    return reduced_compton_wavelength(M_P_KG)


def proton_charge_radius_framework() -> float:
    """r_p = K · λ_C_bar(p) at K=4."""
    return K * proton_compton_wavelength()


def proton_radius_audit() -> Dict[str, float]:
    """Full audit of proton charge radius prediction."""
    lambda_C = proton_compton_wavelength()
    framework = proton_charge_radius_framework()
    dev_ppm = (framework - R_P_CODATA) / R_P_CODATA * 1e6
    return {
        "lambda_C_bar_proton_m": lambda_C,
        "lambda_C_bar_proton_fm": lambda_C * 1e15,
        "framework_prediction_m": framework,
        "framework_prediction_fm": framework * 1e15,
        "codata_m": R_P_CODATA,
        "codata_fm": R_P_CODATA * 1e15,
        "codata_uncertainty_fm": R_P_UNCERTAINTY * 1e15,
        "deviation_ppm": dev_ppm,
        "within_codata_uncertainty": abs(framework - R_P_CODATA) < R_P_UNCERTAINTY,
    }


def proton_radius_in_electron_compton() -> Dict[str, float]:
    """r_p / λ_C_bar(e) = K · (m_e/m_p) = K/(K·D³·Φ_4 + α-corr).

    At K=4, D=3: r_p/λ_C_bar(e) = 4/1836.15 ≈ 1/459 (leading order).
    """
    lambda_C_e = reduced_compton_wavelength(M_E_KG)
    r_p = proton_charge_radius_framework()
    ratio = r_p / lambda_C_e
    # Leading-order framework prediction
    mp_over_me_bulk = K * D**3 * PHI_4   # 1836
    framework_ratio_leading = K / mp_over_me_bulk
    return {
        "r_p_over_lambda_C_e": ratio,
        "framework_leading_K_over_KD3PHI4": framework_ratio_leading,
        "approximation": "r_p / λ_C_bar(e) ≈ 1/(D³·Φ_4) = 1/459 at K=4",
        "value_1_over_DcubedPHI4": 1.0 / (D**3 * PHI_4),
    }


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def showcase_proton_radius() -> List[str]:
    lines: List[str] = []
    lines.append("=" * 80)
    lines.append("  PROTON CHARGE RADIUS FROM K=4 FRAMEWORK")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  FRAMEWORK PREDICTION:")
    lines.append("")
    lines.append("    r_p = K · λ_C_bar(p) = K · ℏ/(m_p·c)")
    lines.append("        = 4 · ℏ/(m_p·c)")
    a = proton_radius_audit()
    lines.append(f"        = 4 · {a['lambda_C_bar_proton_fm']:.4f} fm")
    lines.append(f"        = {a['framework_prediction_fm']:.4f} fm")
    lines.append("")
    lines.append(f"    CODATA: r_p = {a['codata_fm']:.4f} ± {a['codata_uncertainty_fm']:.4f} fm")
    lines.append(f"    Deviation:   {a['deviation_ppm']:+.0f} ppm")
    lines.append(f"    Within CODATA uncertainty (~2300 ppm): {a['within_codata_uncertainty']}")
    lines.append("")
    lines.append("  STRUCTURAL READING:")
    lines.append("")
    lines.append("    K          = coupling pathway count at uniqueness = D+1 = 4")
    lines.append("    λ_C_bar(p) = reduced Compton wavelength of proton")
    lines.append("")
    lines.append("    The proton charge radius = (coupling pathways) × (Compton wavelength)")
    lines.append("                            = number of spacetime axes × ℏ/(m_p c)")
    lines.append("")
    lines.append("  PROTON RADIUS PUZZLE NOTE:")
    lines.append("")
    lines.append("    Muonic hydrogen:    0.84087(39) fm")
    lines.append("    Electron scattering: 0.8775(50) fm  (older)")
    lines.append("    Modern average:      0.8414(19) fm  ← framework matches")
    lines.append("")
    lines.append("    Framework prediction 0.8412 fm sits in modern consensus range.")
    return lines


__all__ = [
    "K", "D", "PHI_4",
    "HBAR_CODATA", "C_EXACT", "M_P_KG", "M_E_KG",
    "R_P_CODATA", "R_P_UNCERTAINTY",
    "reduced_compton_wavelength",
    "proton_compton_wavelength",
    "proton_charge_radius_framework",
    "proton_radius_audit",
    "proton_radius_in_electron_compton",
    "showcase_proton_radius",
]
