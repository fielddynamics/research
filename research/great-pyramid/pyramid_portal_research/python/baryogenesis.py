"""
baryogenesis.py
=================

The matter-antimatter asymmetry of the universe from K=4 framework.

FRAMEWORK PREDICTION:

    η_B = (n_B - n_B_bar) / n_γ
        = D · (K+D)² / K_5  ·  α^K_5
        = 3 · 49 / 5  ·  α^5
        = 29.4 · α^5
        = 6.084 × 10⁻¹⁰

    Planck CMB+BBN measured: 6.10(4) × 10⁻¹⁰
    Deviation:               −0.27%
    Measurement uncertainty: ±0.7% (BBN), ±1.6% (CMB-only)

The framework prediction sits within Planck measurement uncertainty.

THE PROBLEM:

Why does the universe have matter at all?  If the Big Bang created
equal amounts of matter and antimatter, they should have annihilated,
leaving only photons.  But there is matter — about 1 baryon per
10⁹ photons (η_B ~ 6 × 10⁻¹⁰).

Sakharov's conditions are necessary for baryogenesis:
  1. Baryon number violation
  2. C and CP violation
  3. Departure from thermal equilibrium

But NO theory predicts the specific value of η_B.  It is a free
parameter, one of the great mysteries of cosmology.

Standard candidate mechanisms:
  • Electroweak baryogenesis: blocked by 125 GeV Higgs mass
  • Leptogenesis: requires heavy right-handed neutrinos (not observed)
  • GUT baryogenesis: requires GUT physics at 10¹⁶ GeV
  • Affleck-Dine: speculative

None gives the specific value η_B ≈ 6 × 10⁻¹⁰.

FRAMEWORK RESOLUTION:

The K=4 framework gives η_B directly as a K=4 combination times α^5:

    η_B = D · (K+D)² · α^K_5 / K_5

where:
  D = 3 (spatial dim)
  K + D = 7 (simplex closure)
  K_5 = 5 (chamber-K = next-shell K)
  α = fine-structure constant

The framework explains WHY the universe has matter, and predicts
the specific asymmetry value to <1% of Planck measurement.

EXPONENT K_5 = K+1:

The α-exponent K_5 = 5 (chamber-K) reads as: matter-antimatter
asymmetry scales as α to the chamber-K power, modulated by the
spatial × simplex² ratio over chamber-K.

CONNECTION TO OTHER FRAMEWORK PREDICTIONS:

  • α encoded in pyramid array (AW 28-30)
  • K_5 in Menkaure height (AW 30) and Ω_Λ denominator (AW 34)
  • D² in chamber acoustic anchor (AW 26) and Λ formula (AW 35)
  • (K+D) = 7 in α Form III denominator (AW 35)

Same K=4 framework integers throughout.
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

ALPHA_CODATA = 7.2973525693e-3

# Planck 2018 measured values
ETA_B_PLANCK_BBN = 6.10e-10        # baryon-to-photon ratio (BBN)
ETA_B_BBN_UNCERTAINTY = 0.04e-10
ETA_B_PLANCK_CMB = 6.143e-10       # from CMB-only Ω_bh²
ETA_B_CMB_UNCERTAINTY = 0.099e-10


# ---------------------------------------------------------------------------
# Framework prediction
# ---------------------------------------------------------------------------

def baryogenesis_ratio(alpha: float = ALPHA_CODATA) -> float:
    """η_B = D · (K+D)² / K_5 · α^K_5
          = D · (K+D)² · α^(K+1) / (K+1)

    At K=4, D=3, K_5=5: 3·49/5·α^5 = 29.4·α^5.
    """
    return D * (K + D)**2 / K_5 * alpha**K_5


def baryogenesis_alternative_form(alpha: float = ALPHA_CODATA) -> float:
    """Equivalent: η_B = Φ_3 · α^5 · (K+D)/K_5
                       = 21α^5·7/5

    Same value, different framework integer grouping.
    """
    return PHI_3 * alpha**5 * (K + D) / K_5


def baryogenesis_audit(alpha: float = ALPHA_CODATA) -> Dict[str, float]:
    """Full audit of η_B prediction vs Planck."""
    framework = baryogenesis_ratio(alpha)
    dev_BBN_percent = (framework - ETA_B_PLANCK_BBN) / ETA_B_PLANCK_BBN * 100
    dev_CMB_percent = (framework - ETA_B_PLANCK_CMB) / ETA_B_PLANCK_CMB * 100
    return {
        "alpha": alpha,
        "framework_prediction": framework,
        "coefficient_D_KplusD2_over_K5": D * (K + D)**2 / K_5,
        "alpha_K5": alpha**K_5,
        "planck_BBN": ETA_B_PLANCK_BBN,
        "planck_CMB": ETA_B_PLANCK_CMB,
        "deviation_from_BBN_percent": dev_BBN_percent,
        "deviation_from_CMB_percent": dev_CMB_percent,
        "BBN_uncertainty_percent": ETA_B_BBN_UNCERTAINTY / ETA_B_PLANCK_BBN * 100,
        "within_BBN_uncertainty": abs(dev_BBN_percent) < ETA_B_BBN_UNCERTAINTY / ETA_B_PLANCK_BBN * 100,
        "structural_form": "D·(K+D)²·α^K_5/K_5  =  spatial × simplex² × α^chamber-K / chamber-K",
    }


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def showcase_baryogenesis() -> List[str]:
    lines: List[str] = []
    lines.append("=" * 80)
    lines.append("  BARYOGENESIS RATIO η_B FROM K=4 FRAMEWORK")
    lines.append("  WHY THE UNIVERSE HAS MATTER")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  THE PROBLEM:")
    lines.append("")
    lines.append("    Big Bang created equal matter and antimatter — should have")
    lines.append("    annihilated completely.  But there is matter:")
    lines.append("")
    lines.append("        η_B = (n_B - n_B_bar) / n_γ ≈ 6 × 10⁻¹⁰")
    lines.append("")
    lines.append("    Sakharov's conditions are necessary but no theory predicts")
    lines.append("    the specific value.  η_B is a free parameter of cosmology.")
    lines.append("")
    lines.append("  FRAMEWORK PREDICTION:")
    lines.append("")
    lines.append("    η_B = D · (K+D)² / K_5 · α^K_5")
    lines.append("        = 3 · 49 / 5 · α^5")
    lines.append("        = 29.4 · α^5")
    lines.append("")
    a = baryogenesis_audit()
    lines.append(f"    Framework:        {a['framework_prediction']:.4e}")
    lines.append(f"    Planck BBN:        {a['planck_BBN']:.4e}")
    lines.append(f"    Planck CMB:        {a['planck_CMB']:.4e}")
    lines.append(f"    Deviation (BBN):   {a['deviation_from_BBN_percent']:+.3f}%")
    lines.append(f"    Deviation (CMB):   {a['deviation_from_CMB_percent']:+.3f}%")
    lines.append(f"    BBN uncertainty:   ±{a['BBN_uncertainty_percent']:.2f}%")
    lines.append(f"    Within uncertainty: {a['within_BBN_uncertainty']}")
    lines.append("")
    lines.append("  STRUCTURAL READING:")
    lines.append("")
    lines.append("    D · (K+D)² / K_5     = spatial × simplex² / chamber-K")
    lines.append("    α^K_5                = α to the chamber-K power")
    lines.append("")
    lines.append("    η_B emerges as α^5 attenuation × geometric K=4 ratio.")
    lines.append("    At K=4, α ≈ 1/137: α^5 ≈ 2.07 × 10⁻¹¹")
    lines.append("    Multiplied by 29.4: gives 6.1 × 10⁻¹⁰ matching Planck.")
    lines.append("")
    lines.append("  RESOLUTION OF MATTER-ANTIMATTER PUZZLE:")
    lines.append("")
    lines.append("    Why does the universe contain matter?  Because K=4 algebra")
    lines.append("    determines the specific asymmetry value.  No fine-tuning.")
    lines.append("    No anthropic argument.  Direct algebraic derivation.")
    return lines


__all__ = [
    "K", "D", "K_5", "PHI_3",
    "ALPHA_CODATA",
    "ETA_B_PLANCK_BBN", "ETA_B_PLANCK_CMB",
    "baryogenesis_ratio",
    "baryogenesis_alternative_form",
    "baryogenesis_audit",
    "showcase_baryogenesis",
]
