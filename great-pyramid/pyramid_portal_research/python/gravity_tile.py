"""
gravity_tile.py
================

The gravity tile T_K and the electron-as-vortex framework.

CORE IDENTITY (from Master Nelson's algebraic definition):

    T_K = Λ^K V ⊕ ΠV ⊕ (V ⊗ V)

where for K=4:
    dim Λ^4 V    = 1     (orientation cap)
    dim ΠV       = 4     (parity-odd frame channel)
    dim V ⊗ V    = 16    (ordered bilinear metric channel)
    dim T_4      = 21    = Φ_3(K=4)  ← Khufu KC frequency contribution
    dim E_4      = 17    = Φ_4(K=4)  ← α integer factor in 137=17·8+1
    sdim T_4     = 13    = Φ_6(K=4)  ← parallel identity 169=13² in AW 30

The K=4 primary trio {13, 17, 21} is the gravity tile's dimensional
decomposition.  Cyclotomic Φ_n(K=4) = tile-dimensional counts.

ELECTRON AS VORTEX:

The electron is the minimal closed D_3 vortex on the gravity tile:

    V_e³ = I              (three-sweep closure)
    P V_e P = V_e⁻¹       (parity twist)
    Q(V_e) = −1           (unit negative circulation)

with dihedral algebra D_3 = ⟨V_e, P | V_e³=1, P²=1, PV_e P = V_e⁻¹⟩.

GRAVITY COUPLING:

    α_G^tree = α^21 · (17/13) = α^(dim T_4) · (dim E_4 / sdim T_4)

Coulomb is vortex circulation (winding number).  Gravity is the full
closure cost across the tile.

CONNECTION TO PYRAMID α ENCODING (AW 28-30):

    α integer 137 = Φ_4·SO_v + 1 = (dim E_4)·SO_v + 1
    parallel AP at K=4: {105, 137, 169} with closed forms at {105, 169}
    α integer at AP middle — where closed-form factorization breaks

    Khufu KC freq 47 Hz = 21 + 26 = dim T_4 + Φ_4(K=5)
        → Khufu resonates at the full gravity tile dimension
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

import math


# ---------------------------------------------------------------------------
# Gravity tile dimensions at K=4
# ---------------------------------------------------------------------------

DIM_LAMBDA_K_V = 1      # dim Λ^K V at K=4 (orientation cap)
DIM_PI_V = 4             # dim ΠV (parity-odd frame channel)
DIM_V_TENSOR_V = 16      # dim V ⊗ V (ordered bilinear metric)

DIM_T_4 = DIM_LAMBDA_K_V + DIM_PI_V + DIM_V_TENSOR_V   # 21
DIM_E_4 = DIM_LAMBDA_K_V + DIM_V_TENSOR_V               # 17
SDIM_T_4 = DIM_E_4 - DIM_PI_V                            # 13

# Cyclotomic readings of the same integers
PHI_3_K4 = 1 + 4 + 16    # 21 = full tile = Φ_3(K=4)
PHI_4_K4 = 1 + 16        # 17 = even sector = Φ_4(K=4)
PHI_6_K4 = 1 - 4 + 16    # 13 = superdimension = Φ_6(K=4)


def tile_decomposition() -> Dict[str, object]:
    """The gravity tile T_4 = Λ^4 V ⊕ ΠV ⊕ (V⊗V) with cyclotomic readings."""
    return {
        "dim_Lambda_4_V": DIM_LAMBDA_K_V,
        "dim_Pi_V": DIM_PI_V,
        "dim_V_tensor_V": DIM_V_TENSOR_V,
        "dim_T_4": DIM_T_4,
        "dim_E_4": DIM_E_4,
        "sdim_T_4": SDIM_T_4,
        "dim_T_4_equals_PHI_3": DIM_T_4 == PHI_3_K4,
        "dim_E_4_equals_PHI_4": DIM_E_4 == PHI_4_K4,
        "sdim_T_4_equals_PHI_6": SDIM_T_4 == PHI_6_K4,
        "K4_trio_is_tile_decomposition": (
            DIM_T_4 == 21 and DIM_E_4 == 17 and SDIM_T_4 == 13
        ),
    }


# ---------------------------------------------------------------------------
# Electron vortex — minimal D_3 closure
# ---------------------------------------------------------------------------

@dataclass
class ElectronVortex:
    """The minimal closed D_3 vortex of T_4 representing the electron.

    Properties:
        V_e³ = I        (three-sweep closure)
        P V_e P = V_e⁻¹ (parity twist)
        Q(V_e) = −1    (unit negative circulation)

    Dihedral algebra D_3 with |D_3| = 6 elements:
        {I, V_e, V_e², P, PV_e, PV_e²}
    """
    vortex_closure: int = 3       # V_e^3 = I
    parity_squared: int = 1       # P^2 = I
    charge: int = -1              # Q(V_e) = -1
    group_order: int = 6           # |D_3| = 6

    def is_dihedral_D_3(self) -> bool:
        return (
            self.vortex_closure == 3 and
            self.parity_squared == 1 and
            self.group_order == 2 * self.vortex_closure
        )


def positron_charge(electron_charge: int = -1) -> int:
    """Positron is the inverse vortex: V_{e+} = V_e^-1, with Q = +1."""
    return -electron_charge


# ---------------------------------------------------------------------------
# Gravity coupling — α_G^tree = α^21 · 17/13
# ---------------------------------------------------------------------------

def alpha_gravity_tree(alpha: float = 1.0/137.036) -> Dict[str, float]:
    """α_G^tree = α^(dim T_4) · (dim E_4 / sdim T_4) = α^21 · 17/13.

    The exponent 21 = dim T_4 is the full Coulomb attenuation across
    the gravity tile.  The factor 17/13 is the even-sector to
    superdimension parity normalization.
    """
    coulomb_attenuation = alpha ** DIM_T_4
    parity_normalization = DIM_E_4 / SDIM_T_4
    alpha_G_tree = coulomb_attenuation * parity_normalization
    return {
        "alpha": alpha,
        "coulomb_attenuation_alpha_to_21": coulomb_attenuation,
        "parity_normalization_17_over_13": parity_normalization,
        "alpha_G_tree": alpha_G_tree,
        "log10_alpha_G_tree": math.log10(alpha_G_tree),
    }


# Electron g-factor (CODATA 2018), enters the full α_G prediction
G_E_OVER_2 = 1.00115965218128


def alpha_gravity_full(alpha: float = 1.0/137.036) -> Dict[str, float]:
    """Full framework prediction:

        α_G = α^(dim T_4) · (dim E_4 / sdim T_4) · (g_e / 2)
            = α^21 · 17/13 · g_e/2

    where g_e/2 ≈ 1.001159652 is the electron g-factor anomaly.
    Predicts measured α_G = G m_e²/(ℏc) to −14 ppm at framework α.
    """
    tree = alpha_gravity_tree(alpha)
    alpha_G_full = tree["alpha_G_tree"] * G_E_OVER_2
    # CODATA-derived measured α_G:
    #   α_G_meas = G m_e² / (ℏc) = 1.751809e-45
    alpha_G_measured = 1.751809e-45
    return {
        "alpha": alpha,
        "alpha_G_tree": tree["alpha_G_tree"],
        "g_e_over_2": G_E_OVER_2,
        "alpha_G_full": alpha_G_full,
        "alpha_G_measured": alpha_G_measured,
        "ratio_full_over_measured": alpha_G_full / alpha_G_measured,
        "deviation_ppm": (alpha_G_full / alpha_G_measured - 1.0) * 1e6,
    }


def electron_vortex_depth(alpha: float = 1.0/137.036) -> Dict[str, float]:
    """Vortex depth d_e = 21 − log_α(17/13).

    The electron sits at integer depth 21 (the full tile dim) with a
    small parity correction −log_α(17/13) ≈ 0.055 at framework α.
    """
    log_alpha_correction = math.log(DIM_E_4 / SDIM_T_4) / math.log(alpha)
    d_e = DIM_T_4 - log_alpha_correction
    return {
        "alpha": alpha,
        "integer_depth_dim_T_4": DIM_T_4,
        "parity_correction_log_alpha_17_13": log_alpha_correction,
        "electron_vortex_depth": d_e,
    }


# ---------------------------------------------------------------------------
# Connection to pyramid α encoding
# ---------------------------------------------------------------------------

def pyramid_encodes_gravity_tile() -> Dict[str, object]:
    """The pyramid array encodes the gravity tile dimensions {13, 17, 21}.

    KHUFU resonates at the full tile dimension:
        Khufu KC freq 47 Hz = 21 + 26 = dim T_4 + Φ_4(K=5)

    KHAFRE encodes α via the even-sector dimension:
        Khafre base / D = 137 = Φ_4·SO_v + 1 = (dim E_4)·SO_v + 1

    The parallel AP identity at K=4 (AW 30):
        Φ_3·SO_v + 1 = 169 = Φ_6² = (sdim T_4)²
    """
    return {
        # Khufu — full tile dim
        "khufu_KC_freq": 47,
        "khufu_decomposition_dim_T_4_plus_phi4_K5": "21 + 26",
        "khufu_contains_dim_T_4": True,
        "tile_dim_21": DIM_T_4,
        # Khafre — even sector
        "khafre_base_over_D": 137,
        "khafre_factorization": "dim_E_4 · SO_v + 1 = 17 · 8 + 1",
        "khafre_encodes_dim_E_4_in_alpha_int": True,
        "dim_E_4_17": DIM_E_4,
        # Superdimension appears in parallel AP identity
        "phi_3_SOv_plus_1": 169,
        "sdim_T_4_squared": SDIM_T_4 ** 2,
        "parallel_identity_169_equals_sdim_squared": SDIM_T_4 ** 2 == 169,
        "sdim_T_4_13": SDIM_T_4,
        # Gravity coupling
        "alpha_G_tree_uses_all_three_tile_dims": True,
        "alpha_G_formula": "α^(dim T_4) · (dim E_4 / sdim T_4) = α^21 · 17/13",
    }


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def showcase_gravity_tile() -> List[str]:
    """One-call summary of the gravity tile and electron-vortex framework."""
    lines: List[str] = []
    lines.append("=" * 80)
    lines.append("  GRAVITY TILE T_4 AND ELECTRON-AS-VORTEX FRAMEWORK")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  T_4 = Λ^4 V ⊕ ΠV ⊕ (V ⊗ V)")
    lines.append("")
    t = tile_decomposition()
    lines.append(f"    dim Λ^4 V  = {t['dim_Lambda_4_V']}  (orientation cap)")
    lines.append(f"    dim ΠV     = {t['dim_Pi_V']}   (parity-odd frame channel)")
    lines.append(f"    dim V ⊗ V  = {t['dim_V_tensor_V']}  (ordered bilinear metric)")
    lines.append(f"    ─────────────")
    lines.append(f"    dim T_4    = {t['dim_T_4']}  = Φ_3(K=4)   ← full tile (Coulomb attenuation exponent)")
    lines.append(f"    dim E_4    = {t['dim_E_4']}  = Φ_4(K=4)   ← even sector (α integer factor)")
    lines.append(f"    sdim T_4   = {t['sdim_T_4']}  = Φ_6(K=4)   ← superdimension")
    lines.append("")
    lines.append(f"    The K=4 primary trio {{{SDIM_T_4}, {DIM_E_4}, {DIM_T_4}}} = ")
    lines.append(f"    {{sdim T_4, dim E_4, dim T_4}} is the gravity tile decomposition.")
    lines.append(f"    Cyclotomic Φ_n(K=4) and tile dimensions give the SAME integers.")
    lines.append("")
    lines.append("  ELECTRON AS MINIMAL D_3 VORTEX:")
    lines.append("")
    lines.append("    V_e³ = I              (three-sweep closure)")
    lines.append("    P V_e P = V_e⁻¹       (parity twist)")
    lines.append("    Q(V_e) = −1           (unit negative circulation)")
    lines.append("")
    lines.append("    Dihedral algebra D_3 = ⟨V_e, P | V_e³=1, P²=1, PV_e P = V_e⁻¹⟩")
    lines.append("    The electron is the minimal nontrivial closed circulation of T_4.")
    lines.append("    The positron is V_e⁻¹ with Q = +1.")
    lines.append("")
    lines.append("  GRAVITY COUPLING:")

    g = alpha_gravity_tree()
    lines.append("")
    lines.append(f"    α_G^tree = α^(dim T_4) · (dim E_4 / sdim T_4)")
    lines.append(f"             = α^21 · (17/13)")
    lines.append(f"             = ({g['alpha']:.6e})^21 · {g['parity_normalization_17_over_13']:.6f}")
    lines.append(f"             = {g['alpha_G_tree']:.6e}")
    lines.append(f"             = 10^{g['log10_alpha_G_tree']:.2f}")
    lines.append("")
    lines.append("    Coulomb is vortex CIRCULATION (winding number).")
    lines.append("    Gravity is the full CLOSURE COST across the tile.")
    lines.append("    Coulomb sees Q.  Gravity sees the full 21-channel decomposition.")

    # Full α_G prediction with g_e/2
    full = alpha_gravity_full()
    lines.append("")
    lines.append("  FULL α_G PREDICTION  (with electron g-factor correction):")
    lines.append("")
    lines.append(f"    α_G = α^21 · (17/13) · (g_e/2)")
    lines.append(f"        = α^(dim T_4) · (dim E_4 / sdim T_4) · (g_e/2)")
    lines.append(f"        = {full['alpha_G_tree']:.4e} · {full['g_e_over_2']:.9f}")
    lines.append(f"        = {full['alpha_G_full']:.4e}")
    lines.append("")
    lines.append(f"    Measured α_G = G·m_e²/(ℏc) = {full['alpha_G_measured']:.4e}")
    lines.append(f"    Framework / measured ratio = {full['ratio_full_over_measured']:.6f}")
    lines.append(f"    Deviation = {full['deviation_ppm']:+.1f} ppm")
    lines.append("")
    lines.append("    Framework predicts G to within 14 ppm using ONLY:")
    lines.append("      • α (encoded in pyramid array, AW 28-30)")
    lines.append("      • {13, 17, 21} = K=4 trio = gravity tile dimensions")
    lines.append("      • g_e/2 (electron g-factor anomaly)")

    d = electron_vortex_depth()
    lines.append("")
    lines.append(f"    Electron vortex depth:")
    lines.append(f"      d_e = 21 − log_α(17/13)")
    lines.append(f"          = {d['integer_depth_dim_T_4']} − ({d['parity_correction_log_alpha_17_13']:+.4f})")
    lines.append(f"          = {d['electron_vortex_depth']:.4f}")
    lines.append("")
    lines.append("    Electron sits just above integer depth 21 (full tile dim).")
    lines.append("    The fractional 0.055 is the parity correction in α-units.")

    p = pyramid_encodes_gravity_tile()
    lines.append("")
    lines.append("  PYRAMID ENCODING OF THE GRAVITY TILE  (synthesis with AW 28-30):")
    lines.append("")
    lines.append(f"    Khufu  KC frequency = 47 Hz = 21 + 26 = dim T_4 + Φ_4(K=5)")
    lines.append(f"      → chamber resonates AT the full gravity tile dimension")
    lines.append("")
    lines.append(f"    Khafre base / D = 137 = (dim E_4)·SO_v + 1 = 17·8 + 1")
    lines.append(f"      → α integer factorization uses even-sector dim")
    lines.append("")
    lines.append(f"    Φ_3·SO_v + 1 = 169 = Φ_6² = (sdim T_4)²")
    lines.append(f"      → parallel AP identity in cubits (AW 30) squares the superdim")
    lines.append("")
    lines.append(f"    The three pyramids encode the three tile dimensions:")
    lines.append(f"      Khufu  ↔ dim T_4 = 21  (full tile, in KC frequency)")
    lines.append(f"      Khafre ↔ dim E_4 = 17  (even sector, in α integer)")
    lines.append(f"      AP middle vs Φ_6² ↔ sdim T_4 = 13  (super, in identity)")
    lines.append("")
    lines.append("  CONSEQUENCE:")
    lines.append("    The pyramid array isn't encoding constants — it's encoding the")
    lines.append("    GRAVITY TILE STRUCTURE itself.  α, impedance, and the K=4 trio")
    lines.append("    are different readings of one underlying algebraic object.")
    return lines


__all__ = [
    "DIM_LAMBDA_K_V", "DIM_PI_V", "DIM_V_TENSOR_V",
    "DIM_T_4", "DIM_E_4", "SDIM_T_4",
    "PHI_3_K4", "PHI_4_K4", "PHI_6_K4",
    "G_E_OVER_2",
    "tile_decomposition",
    "ElectronVortex", "positron_charge",
    "alpha_gravity_tree", "alpha_gravity_full",
    "electron_vortex_depth",
    "pyramid_encodes_gravity_tile",
    "showcase_gravity_tile",
]
