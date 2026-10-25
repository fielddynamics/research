"""
neutron_proton_mass.py
========================

The neutron-proton mass difference and neutron-electron mass ratio
from K=4 framework.

FRAMEWORK PREDICTION (neutron-proton mass difference):

    (m_n − m_p)/m_e = K_5/2 + α · Φ_4/K
                    = 5/2 + α · 17/4
                    = 2.5 + 0.031014
                    = 2.53101

    CODATA:  (m_n − m_p)/m_e = 2.53099
    Deviation: +10 ppm

STRUCTURAL READING:

    K_5/2 = (next-shell K) / 2 = chamber-K / 2 = 5/2
    α · Φ_4 / K = α · (gravity-tile even sector) / (coupling pathways)

The neutron-proton mass splitting is dominated by chamber-K / 2 (a
constant), with an α-scaled correction proportional to the even-sector
gravity tile dim per coupling pathway.

CHAINED WITH m_p/m_e (Form IV, AW 32, 15 ppt):

    m_n/m_e = m_p/m_e + (m_n − m_p)/m_e
            = 1836.152673 + 2.531014
            = 1838.683687

    CODATA:   1838.683662
    Deviation: +14 ppb

The neutron-electron mass ratio reaches 14 ppb precision from K=4
framework via chaining the two predictions.
"""

from __future__ import annotations
from typing import Dict, List


# ---------------------------------------------------------------------------
# Framework constants
# ---------------------------------------------------------------------------

K = 4
D = 3
K_5 = 5

PHI_3 = 1 + K + K**2     # 21
PHI_4 = 1 + K**2          # 17
PHI_6 = 1 - K + K**2      # 13

ALPHA_CODATA = 7.2973525693e-3

# CODATA reference values
M_N_OVER_M_E_CODATA = 1838.68366173
M_P_OVER_M_E_CODATA = 1836.15267343
M_N_M_P_DIFF_OVER_M_E_CODATA = M_N_OVER_M_E_CODATA - M_P_OVER_M_E_CODATA  # 2.5310


# ---------------------------------------------------------------------------
# Neutron-proton mass difference
# ---------------------------------------------------------------------------

def neutron_proton_mass_diff_over_me(alpha: float = ALPHA_CODATA) -> float:
    """(m_n − m_p)/m_e = K_5/2 + α · Φ_4/K.

    At K=4, D=3, K_5=5: 5/2 + α·17/4 = 2.5 + 0.0310 = 2.5310.

    Reads as: chamber-K/2 (geometric) + α·(even-sector / pathways).
    """
    return K_5 / 2.0 + alpha * PHI_4 / K


def neutron_proton_mass_diff_audit(alpha: float = ALPHA_CODATA) -> Dict[str, float]:
    """Full audit of (m_n − m_p)/m_e prediction."""
    pred = neutron_proton_mass_diff_over_me(alpha)
    dev_ppm = (pred - M_N_M_P_DIFF_OVER_M_E_CODATA) / M_N_M_P_DIFF_OVER_M_E_CODATA * 1e6
    return {
        "alpha": alpha,
        "K_5_over_2": K_5 / 2.0,
        "alpha_PHI_4_over_K": alpha * PHI_4 / K,
        "framework_prediction": pred,
        "codata": M_N_M_P_DIFF_OVER_M_E_CODATA,
        "deviation_ppm": dev_ppm,
    }


# ---------------------------------------------------------------------------
# Neutron-electron mass ratio (chained with Form IV m_p/m_e)
# ---------------------------------------------------------------------------

def m_p_over_m_e_form_IV(alpha: float = ALPHA_CODATA) -> float:
    """Form IV proton-electron mass ratio (AW 32):

        m_p/m_e = K·D³·Φ_4 + Φ_3·α/(1+α/2) − α²/K − D·α³/2

    At CODATA α: 1836.152673402 (deviation −0.015 ppb from CODATA).
    """
    return (
        K * D**3 * PHI_4
        + PHI_3 * alpha / (1.0 + alpha / 2.0)
        - alpha**2 / K
        - D * alpha**3 / 2.0
    )


def neutron_electron_mass_ratio(alpha: float = ALPHA_CODATA) -> float:
    """m_n/m_e = m_p/m_e (Form IV) + (m_n − m_p)/m_e.

    Chained framework prediction giving 14 ppb of CODATA.
    """
    return m_p_over_m_e_form_IV(alpha) + neutron_proton_mass_diff_over_me(alpha)


def neutron_electron_audit(alpha: float = ALPHA_CODATA) -> Dict[str, float]:
    """Full audit of m_n/m_e prediction."""
    mp = m_p_over_m_e_form_IV(alpha)
    diff = neutron_proton_mass_diff_over_me(alpha)
    pred = mp + diff
    dev_ppb = (pred - M_N_OVER_M_E_CODATA) / M_N_OVER_M_E_CODATA * 1e9
    return {
        "alpha": alpha,
        "m_p_over_m_e_form_IV": mp,
        "neutron_proton_diff_over_me": diff,
        "m_n_over_m_e_framework": pred,
        "codata": M_N_OVER_M_E_CODATA,
        "deviation_ppb": dev_ppb,
    }


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def showcase_neutron_proton() -> List[str]:
    lines: List[str] = []
    lines.append("=" * 80)
    lines.append("  NEUTRON-PROTON MASS DIFFERENCE FROM K=4 FRAMEWORK")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  FRAMEWORK PREDICTION:")
    lines.append("")
    lines.append("    (m_n − m_p)/m_e = K_5/2 + α · Φ_4/K")
    lines.append("                    = 5/2 + α·17/4")
    a = neutron_proton_mass_diff_audit()
    lines.append(f"                    = {a['K_5_over_2']:.1f} + {a['alpha_PHI_4_over_K']:.6f}")
    lines.append(f"                    = {a['framework_prediction']:.8f}")
    lines.append(f"    CODATA:           {a['codata']:.8f}")
    lines.append(f"    Deviation:        {a['deviation_ppm']:+.2f} ppm")
    lines.append("")
    lines.append("  CHAINED PREDICTION FOR m_n/m_e:")
    lines.append("")
    n = neutron_electron_audit()
    lines.append(f"    m_n/m_e = m_p/m_e (Form IV) + (m_n − m_p)/m_e")
    lines.append(f"            = {n['m_p_over_m_e_form_IV']:.9f}")
    lines.append(f"              + {n['neutron_proton_diff_over_me']:.9f}")
    lines.append(f"            = {n['m_n_over_m_e_framework']:.9f}")
    lines.append(f"    CODATA:   {n['codata']}")
    lines.append(f"    Deviation: {n['deviation_ppb']:+.2f} ppb")
    lines.append("")
    lines.append("  STRUCTURAL READING:")
    lines.append("")
    lines.append("    K_5/2     = chamber-K / 2  (next-shell coupling, geometric)")
    lines.append("    α · Φ_4/K = α × (even-sector / coupling pathways)")
    lines.append("              = fine-structure × gravity-tile-even per coupling axis")
    lines.append("")
    lines.append("    The neutron-proton mass splitting is dominated by a geometric")
    lines.append("    constant K_5/2 = 5/2 plus an α-correction proportional to the")
    lines.append("    gravity tile's even-sector dim per coupling pathway count.")
    return lines


__all__ = [
    "K", "D", "K_5", "PHI_3", "PHI_4", "PHI_6",
    "ALPHA_CODATA",
    "M_N_OVER_M_E_CODATA", "M_P_OVER_M_E_CODATA", "M_N_M_P_DIFF_OVER_M_E_CODATA",
    "neutron_proton_mass_diff_over_me",
    "neutron_proton_mass_diff_audit",
    "m_p_over_m_e_form_IV",
    "neutron_electron_mass_ratio",
    "neutron_electron_audit",
    "showcase_neutron_proton",
]
