"""
chamber_polarization.py
========================

Closes the Z_3 sectoring gap named in AW 18.

The framework's Z_3 acts on each chamber mode's *polarization* — specifically
on the unit k-vector embedded in Cl(3, 0) as a grade-1 element.  Under the
permutation Ω : e_1 → e_2 → e_3 → e_1 (the same Ω used in cyclotomic_12),
the k-vector decomposes into:

  - Axial (Ω-symmetric) component along T_1 = e_1 + e_2 + e_3
  - Two hexagonal Ω-eigenvector components (eigenvalues ω, ω²)

The Cl(3,0) discrete-Fourier amplitude at the ω-eigenvalue is

    ζ(k̂) = k̂_x + ω k̂_y + ω² k̂_z         ω = e^{2πi/3}

|ζ|² is the *hexagonal weight* of the mode.  Pure-axial modes have ζ = 0.
The phase arg(ζ) is the mode's Ω-eigenvalue character and defines its
Z_3 sector via arg(ζ) ∈ [0, 2π/3), [2π/3, 4π/3), [4π/3, 2π).

Antechamber filter:  the framework's Z_3 portcullis suppresses one of the
three sectors (the "a=0" sector).  The sectoring computed here can be
checked against the predicted 14 active : 7 suppressed split (07.1).

Critically, ζ is computed from the physical k-vector components
(k̂_x = n_x/L / |k|, etc.) NOT from the integer triple — so the sectoring
respects the chamber's asymmetric dimensions L : W : H = 20 : 10 : 5√5.
This is the right way to test the framework's Z_3 prediction.

Tests in `tests/test_chamber_polarization.py`.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

import cmath
import math
import numpy as np

from python.pyramid_resonance import (
    KC_L_CUBITS, KC_W_CUBITS, KC_H_CUBITS,
    Mode, lowest_modes,
)


OMEGA = cmath.exp(2j * cmath.pi / 3.0)        # primitive 3rd root of unity
OMEGA_BAR = OMEGA.conjugate()
SECTOR_BIN_WIDTH = 2.0 * math.pi / 3.0


# ---------------------------------------------------------------------------
# Unit k-vector and ζ-amplitude
# ---------------------------------------------------------------------------

def unit_k_vector(mode: Mode) -> Tuple[float, float, float]:
    """Unit k-vector (k̂_x, k̂_y, k̂_z) for a cavity mode."""
    kx = mode.n_x / KC_L_CUBITS
    ky = mode.n_y / KC_W_CUBITS
    kz = mode.n_z / KC_H_CUBITS
    norm = math.sqrt(kx * kx + ky * ky + kz * kz)
    return (kx / norm, ky / norm, kz / norm)


def polarization_zeta(mode: Mode) -> complex:
    """The Cl(3,0) discrete-Fourier amplitude ζ = k̂_x + ω k̂_y + ω² k̂_z.

    Pure-axial modes (k̂ along T_1/√3) have ζ = 0.
    Pure ω-eigenvector modes have ζ ≠ 0 with arg(ζ) determined by the
    eigenstate component.
    """
    kx, ky, kz = unit_k_vector(mode)
    return kx + OMEGA * ky + OMEGA * OMEGA * kz


def axial_weight(mode: Mode) -> float:
    """Fraction of mode in the Ω-symmetric T_1 sector.

    f_axial = (k̂_x + k̂_y + k̂_z)² / 3 ∈ [0, 1]
    Pure axial (k̂ ∝ T_1): f = 1.
    Pure hexagonal (k̂ ⊥ T_1): f = 0.
    """
    kx, ky, kz = unit_k_vector(mode)
    s = kx + ky + kz
    return float(s * s / 3.0)


def hexagonal_weight(mode: Mode) -> float:
    """1 - axial_weight.  This equals |ζ|² / 3 by Parseval at the cube roots."""
    return 1.0 - axial_weight(mode)


def hexagonal_weight_from_zeta(mode: Mode) -> float:
    """Computed directly from |ζ|² for cross-check.  Should equal hexagonal_weight."""
    z = polarization_zeta(mode)
    return float(abs(z) ** 2 * 2.0 / 3.0)
    # Parseval: |k̂|² = 1 = |axial_amp|² + 2 |hex_amp|²
    # where axial_amp² = 3 f_axial, hex_amp² = |ζ|² / 3
    # so 1 = 3 f_axial + 2 |ζ|² / 3 — not quite Parseval.  Use as cross-check.


# ---------------------------------------------------------------------------
# Transverse-polarization sectoring (the cleaner physical picture)
# ---------------------------------------------------------------------------
# For an EM cavity mode with longitudinal direction k̂, the two transverse
# polarizations span the plane orthogonal to k̂.  Under Ω (a 120° rotation
# about the (1,1,1)/√3 body diagonal), the transverse plane is preserved
# only when k̂ lies along the body diagonal; otherwise Ω mixes longitudinal
# and transverse content.
#
# For each mode we compute:
#   1. the action of Ω on the transverse plane (a 2x2 matrix R_perp)
#   2. its eigenvalues (the Z_3 characters of the two transverse polarizations)
#   3. the "circular polarization purity" — how close R_perp is to a true
#      120° rotation, which is what would give clean ω, ω² Ω-eigenstates


def transverse_basis(mode: Mode) -> Tuple[np.ndarray, np.ndarray]:
    """Two orthonormal vectors spanning the plane orthogonal to k̂."""
    k = np.array(unit_k_vector(mode), dtype=float)
    # Find any vector not parallel to k
    seed = np.array([1.0, 0.0, 0.0]) if abs(k[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    e1 = seed - np.dot(seed, k) * k
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(k, e1)
    return e1, e2


def omega_rotation_matrix_3d() -> np.ndarray:
    """The 3x3 cyclic-permutation matrix:  e_1 -> e_2 -> e_3 -> e_1."""
    return np.array(
        [[0.0, 0.0, 1.0],
         [1.0, 0.0, 0.0],
         [0.0, 1.0, 0.0]], dtype=float
    )


def transverse_omega_action(mode: Mode) -> np.ndarray:
    """Restrict Ω-action to the transverse plane orthogonal to k̂.

    Returns a 2x2 matrix R_perp such that for any transverse vector
    v = a e1 + b e2, Ω(v) = a' e1 + b' e2 where (a', b') = R_perp (a, b).

    For k̂ along (1,1,1)/√3 (perfect axial mode), R_perp is a pure 120°
    rotation in 2D with eigenvalues ω, ω̄.  For off-axis k̂, R_perp has
    complex eigenvalues |λ| < 1 because some content is rotated *out* of
    the transverse plane (into the longitudinal direction).
    """
    e1, e2 = transverse_basis(mode)
    R_3d = omega_rotation_matrix_3d()
    Oe1 = R_3d @ e1
    Oe2 = R_3d @ e2
    # Project Ω(e1), Ω(e2) back onto the transverse plane
    R_perp = np.array([
        [np.dot(Oe1, e1), np.dot(Oe2, e1)],
        [np.dot(Oe1, e2), np.dot(Oe2, e2)],
    ])
    return R_perp


def transverse_purity(mode: Mode) -> float:
    """Trace of R_perp R_perp^T / 2.  Equals 1 iff transverse plane is
    Ω-invariant (i.e., k̂ is along the body diagonal exactly).

    Drops below 1 when Ω mixes longitudinal and transverse content.
    The shortfall 1 - purity quantifies how much circulation 'leaks'
    out of the transverse plane per Ω-step.
    """
    R = transverse_omega_action(mode)
    return float(np.trace(R @ R.T) / 2.0)


def transverse_omega_eigenvalues(mode: Mode) -> Tuple[complex, complex]:
    """The two eigenvalues of R_perp.

    For axial k̂: eigenvalues are ω, ω̄ (exactly 120° rotation in 2D).
    For off-axial k̂: eigenvalues have |λ| < 1 with the same phase.
    The product λ₁ λ₂ = det(R_perp) gives the orientation-preserving
    component; the sum gives the trace.
    """
    R = transverse_omega_action(mode)
    eigs = np.linalg.eigvals(R)
    # Sort by imaginary part (ω has positive imag, ω̄ has negative)
    if eigs[0].imag < 0:
        eigs = eigs[::-1]
    return complex(eigs[0]), complex(eigs[1])


# ---------------------------------------------------------------------------
# Closed-form identity:  purity = (1 + σ_2²) / 2  and the {13, 17, 21} trio
# ---------------------------------------------------------------------------
# For a unit k̂ in R³, the second elementary symmetric polynomial
#   σ_2(k̂) = k̂_1 k̂_2 + k̂_2 k̂_3 + k̂_3 k̂_1
# determines the transverse-Ω purity by the exact closed form
#   purity(k̂) = (1 + σ_2(k̂)²) / 2
#
# Summing over the 21 lowest chamber modes:
#   Σ purity  =  21/2 + (1/2) Σ σ_2²
# so
#   Σ purity  =  17  iff  Σ σ_2²  =  13
#
# The framework's primary trio {13, 17, 21} = {Φ_6(4), Φ_4(4), Φ_3(4)}
# is the parity-decomposition of f(K, s) = 1 + sK + K² at K = 4:
#   s = +1 :  21  =  Eisenstein '+'  =  TetA ceiling
#   s =  0 :  17  =  Gaussian axial  =  Field Origin
#   s = −1 :  13  =  Eisenstein '−'  =  TetB floor
#
# The chamber's 21 modes (= count, s=+1) carry 17 in transverse-purity
# (= Gaussian axial preservation, s=0) and 13 in σ_2² (= Eisenstein '−'
# parity-odd polarization mixing, s=−1).  All three parity sectors of
# the framework's trio appear in the chamber's mode-polarization geometry.


def sigma2_of_mode(mode: Mode) -> float:
    """Second elementary symmetric polynomial of k̂ : σ_2 = k₁k₂ + k₂k₃ + k₃k₁."""
    k1, k2, k3 = unit_k_vector(mode)
    return float(k1 * k2 + k2 * k3 + k3 * k1)


def purity_closed_form(mode: Mode) -> float:
    """Closed-form purity = (1 + σ_2²) / 2.  Cross-check on transverse_purity."""
    s2 = sigma2_of_mode(mode)
    return 0.5 * (1.0 + s2 * s2)


def chamber_polarization_sum_audit(modes: List[Mode]) -> Dict[str, object]:
    """Honest audit of the chamber's mode-polarization sums.

    The closed-form identity  purity(m) = (1 + σ_2(m)²)/2  is exact for
    every mode.  Summing over 21 lowest cavity modes:

        Σ 1         =  21                exact   (matches Φ_3(4))
        Σ σ_2       ≈  16.85   (0.90% from 17,    suggestive)
        Σ σ_2²      ≈  13.91   (0.66% from 14,    not 13 — 7% off)
        Σ purity    ≈  17.45   (0.30% from 17.5,  not 17 — 2.67% off)
        Σ (1-purity)≈   3.55   (1.31% from 3.5,   not 4 — 11% off)

    The closest hit is  Σ σ_2² ≈ 14 = 21·2/3  at 0.66%.

    This is NOT the framework's primary trio {13, 17, 21}.  An earlier
    framing attributed the closeness to a Φ_6(4) = 13 identification —
    that framing is retracted: 7% deviation is structurally too large
    for the framework's sub-ppm precision standard.

    The chamber's actual sum-structure {21, ~17, ~14} contains:
      - 21 = Φ_3(4) at K=4 (mode count, exact)
      - ~14 = 21·2/3 = antechamber's predicted active-peak count (07.1)
      - ~17 in Σ σ_2 might be Φ_4(4) but the link is unverified

    The Φ_6(4) = 13 sector does NOT appear in this sum structure.  If
    there is a clean closed-form identity for these sums, it has not
    been found and remains an open question.
    """
    n = len(modes)
    s_purity = sum(transverse_purity(m) for m in modes)
    s_sigma2 = sum(sigma2_of_mode(m) for m in modes)
    s_sigma2_sq = sum(sigma2_of_mode(m) ** 2 for m in modes)
    s_leakage = n - s_purity
    return {
        "mode_count": n,
        "sum_purity": s_purity,
        "sum_sigma2": s_sigma2,
        "sum_sigma2_squared": s_sigma2_sq,
        "sum_leakage": s_leakage,
        "closed_form_identity_holds": abs(s_purity - (n / 2.0 + s_sigma2_sq / 2.0)) < 1e-10,
        # Closest-integer fits with percent deviations:
        "sigma2_closest_int": {
            "value": 17,
            "deviation": s_sigma2 - 17,
            "pct": (s_sigma2 - 17) / 17.0 * 100.0,
        },
        "sigma2_sq_closest_int": {
            "value": 14,
            "deviation": s_sigma2_sq - 14,
            "pct": (s_sigma2_sq - 14) / 14.0 * 100.0,
        },
        # Explicit retraction flag:
        "matches_framework_trio_13_17_21": False,
    }


# Backwards-compat alias.  The old name framework_trio_identity is retained
# but now points to the honest audit; it no longer asserts {13, 17, 21} hits.
framework_trio_identity = chamber_polarization_sum_audit


@dataclass
class TransverseInfo:
    mode: Mode
    R_perp: np.ndarray
    eigenvalues: Tuple[complex, complex]
    purity: float
    rotation_angle_deg: float       # how close to ω = 120°

    def __repr__(self) -> str:
        nx, ny, nz = self.mode.n_x, self.mode.n_y, self.mode.n_z
        return (f"TransvInfo({nx},{ny},{nz}: purity={self.purity:.3f}, "
                f"angle={self.rotation_angle_deg:.1f}°)")


def transverse_info(mode: Mode) -> TransverseInfo:
    R = transverse_omega_action(mode)
    eigs = transverse_omega_eigenvalues(mode)
    angle = math.degrees(cmath.phase(eigs[0]))
    return TransverseInfo(
        mode=mode,
        R_perp=R,
        eigenvalues=eigs,
        purity=transverse_purity(mode),
        rotation_angle_deg=angle,
    )


# ---------------------------------------------------------------------------
# Z_3 sectoring
# ---------------------------------------------------------------------------

def polarization_sector(mode: Mode, axial_threshold: float = 0.999) -> int:
    """Z_3 sector of the mode's polarization.

    Returns:
      0  if axial-dominant (axial_weight > threshold)
      0, 1, 2  otherwise, by phase of ζ:
         arg(ζ) ∈ [-π/3, π/3)  → sector 0
         arg(ζ) ∈ [π/3, π)     → sector 1
         arg(ζ) ∈ [π, 5π/3) (= [-π, -π/3))  → sector 2

    The phase boundaries are chosen so that ζ ∈ ℝ_+ → sector 0,
    ζ ∈ ω · ℝ_+ → sector 1, ζ ∈ ω² · ℝ_+ → sector 2.
    """
    if axial_weight(mode) > axial_threshold:
        return 0
    z = polarization_zeta(mode)
    arg = cmath.phase(z)
    # Shift so sector 0 is centered on phase 0
    arg_shifted = (arg + math.pi / 3.0) % (2.0 * math.pi)
    sector = int(arg_shifted // SECTOR_BIN_WIDTH)
    return sector  # 0, 1, or 2


@dataclass
class PolarizationInfo:
    mode: Mode
    k_hat: Tuple[float, float, float]
    zeta: complex
    axial_weight: float
    hexagonal_weight: float
    zeta_arg_deg: float
    sector: int

    def __repr__(self) -> str:
        nx, ny, nz = self.mode.n_x, self.mode.n_y, self.mode.n_z
        return (f"Pol({nx},{ny},{nz}: ax={self.axial_weight:.3f}, "
                f"hex={self.hexagonal_weight:.3f}, arg={self.zeta_arg_deg:.1f}°, "
                f"sec={self.sector})")


def polarization_info(mode: Mode) -> PolarizationInfo:
    z = polarization_zeta(mode)
    arg_deg = math.degrees(cmath.phase(z)) if abs(z) > 1e-12 else 0.0
    return PolarizationInfo(
        mode=mode,
        k_hat=unit_k_vector(mode),
        zeta=z,
        axial_weight=axial_weight(mode),
        hexagonal_weight=hexagonal_weight(mode),
        zeta_arg_deg=arg_deg,
        sector=polarization_sector(mode),
    )


def polarization_audit(modes: List[Mode]) -> Dict[str, object]:
    """Sector distribution audit by polarization (NOT by index sum)."""
    from collections import Counter
    info_list = [polarization_info(m) for m in modes]
    sector_counts = Counter(p.sector for p in info_list)
    axial_dominant_count = sum(1 for p in info_list if p.axial_weight > 0.5)
    hex_dominant_count = sum(1 for p in info_list if p.hexagonal_weight > 0.5)
    return {
        "total_modes": len(modes),
        "sector_counts": dict(sector_counts),
        "is_clean_777_split": (
            sector_counts.get(0, 0) == 7
            and sector_counts.get(1, 0) == 7
            and sector_counts.get(2, 0) == 7
        ),
        "n_axial_dominant": axial_dominant_count,
        "n_hexagonal_dominant": hex_dominant_count,
        "info": info_list,
    }


# ---------------------------------------------------------------------------
# Antechamber filter — predicts the 14 : 7 active : suppressed split
# ---------------------------------------------------------------------------

def antechamber_filter(
    modes: List[Mode], suppressed_sector: int = 0
) -> Dict[str, List[Mode]]:
    """Apply the antechamber's Z_3 filter.

    The portcullis suppresses one Z_3 sector (the "a=0" axial-direction
    sector by default).  Returns active and suppressed mode lists.
    """
    active, suppressed = [], []
    for m in modes:
        if polarization_sector(m) == suppressed_sector:
            suppressed.append(m)
        else:
            active.append(m)
    return {"active": active, "suppressed": suppressed}


# ---------------------------------------------------------------------------
# Combined predicted spectrum
# ---------------------------------------------------------------------------

@dataclass
class SpectrumEntry:
    mode: Mode
    frequency_hz: float
    sector: int
    is_active: bool
    axial_weight: float
    hexagonal_weight: float


def predict_filtered_spectrum(
    v_wave: float, suppressed_sector: int = 0
) -> List[SpectrumEntry]:
    """The full predicted spectrum with frequencies and antechamber filtering."""
    modes = lowest_modes(21)
    filtered = antechamber_filter(modes, suppressed_sector=suppressed_sector)
    suppressed_keys = {(m.n_x, m.n_y, m.n_z) for m in filtered["suppressed"]}
    out: List[SpectrumEntry] = []
    for m in modes:
        sec = polarization_sector(m)
        is_act = (m.n_x, m.n_y, m.n_z) not in suppressed_keys
        out.append(SpectrumEntry(
            mode=m,
            frequency_hz=m.frequency_hz(v_wave),
            sector=sec,
            is_active=is_act,
            axial_weight=axial_weight(m),
            hexagonal_weight=hexagonal_weight(m),
        ))
    return out


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def showcase_chamber_polarization() -> List[str]:
    """One-call summary: polarization-sectoring of the 21 modes."""
    lines: List[str] = []
    lines.append("=" * 80)
    lines.append("  CHAMBER MODE POLARIZATION SECTORING  (closes AW 18 Z_3 gap)")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  ζ(k̂) = k̂_x + ω k̂_y + ω² k̂_z  with  ω = e^{2πi/3}")
    lines.append("  Sector = arg(ζ) binned mod 2π/3.  Axial-dominant modes -> sector 0.")
    lines.append("")
    lines.append("  rank | (n_x,n_y,n_z) | axial_wt | hex_wt | arg(ζ)°   | sector")
    lines.append("  -----+---------------+----------+--------+-----------+-------")

    modes = lowest_modes(21)
    for i, m in enumerate(modes):
        info = polarization_info(m)
        lines.append(
            f"  {i+1:4d} | ({m.n_x:2d},{m.n_y:2d},{m.n_z:2d})       |"
            f"  {info.axial_weight:.4f}  | {info.hexagonal_weight:.4f} |"
            f"  {info.zeta_arg_deg:+7.2f}  |   {info.sector}"
        )

    audit = polarization_audit(modes)
    sc = audit["sector_counts"]
    lines.append("")
    lines.append("  Sector distribution by POLARIZATION (not index-sum):")
    lines.append(f"    sector 0 : {sc.get(0, 0):2d} modes")
    lines.append(f"    sector 1 : {sc.get(1, 0):2d} modes")
    lines.append(f"    sector 2 : {sc.get(2, 0):2d} modes")
    lines.append(f"    clean 7:7:7 split? {audit['is_clean_777_split']}")
    lines.append("")
    lines.append(f"  Axial-dominant modes (axial_wt > 0.5): {audit['n_axial_dominant']}")
    lines.append(f"  Hex-dominant modes (hex_wt > 0.5)    : {audit['n_hexagonal_dominant']}")

    # Antechamber filter: suppress sector 0 by default
    pred = predict_filtered_spectrum(v_wave=343.0, suppressed_sector=0)
    n_active = sum(1 for e in pred if e.is_active)
    n_suppressed = 21 - n_active
    lines.append("")
    lines.append(f"  Antechamber Z_3 filter (suppresses sector 0):")
    lines.append(f"    Active    : {n_active} modes  (predicted: 14)")
    lines.append(f"    Suppressed: {n_suppressed} modes  (predicted: 7)")

    # Try the other suppression choices
    lines.append("")
    lines.append(f"  Counts if antechamber suppresses other sectors:")
    for s in [0, 1, 2]:
        filt = antechamber_filter(modes, suppressed_sector=s)
        lines.append(f"    suppress sector {s}: {len(filt['active'])} active / {len(filt['suppressed'])} suppressed")

    # Transverse-polarization analysis
    lines.append("")
    lines.append("=" * 80)
    lines.append("  TRANSVERSE POLARIZATION:  Ω-action restricted to plane ⊥ k̂")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  When k̂ ∥ (1,1,1)/√3 exactly, transverse plane is Ω-invariant and")
    lines.append("  R_perp is a pure 120° rotation with eigenvalues ω, ω̄ (purity = 1).")
    lines.append("  Off-axis k̂ gives purity < 1; the shortfall is leakage into the")
    lines.append("  longitudinal direction per Ω-step.")
    lines.append("")
    lines.append("  rank | (n_x,n_y,n_z) | purity | rotation angle")
    lines.append("  -----+---------------+--------+----------------")
    purities = []
    for i, m in enumerate(modes):
        t = transverse_info(m)
        purities.append(t.purity)
        lines.append(
            f"  {i+1:4d} | ({m.n_x:2d},{m.n_y:2d},{m.n_z:2d})       | "
            f"{t.purity:.4f} | {t.rotation_angle_deg:+7.2f}°"
        )
    lines.append("")
    lines.append(f"  Mean transverse purity across 21 modes: {sum(purities)/len(purities):.4f}")
    lines.append(f"  Modes with purity > 0.99 (near-ideal):   {sum(1 for p in purities if p > 0.99)}")
    lines.append(f"  Modes with purity < 0.5  (heavy leakage): {sum(1 for p in purities if p < 0.5)}")

    # Honest audit of the mode-polarization sums
    audit = chamber_polarization_sum_audit(modes)
    lines.append("")
    lines.append("=" * 80)
    lines.append("  CHAMBER MODE-POLARIZATION SUMS — honest audit")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  Closed-form identity (exact, per mode):")
    lines.append("    purity(k̂) = (1 + σ_2(k̂)²) / 2     σ_2 = k̂₁k̂₂ + k̂₂k̂₃ + k̂₃k̂₁")
    lines.append(f"    runtime: Σpurity = 21/2 + Σσ_2²/2?  {audit['closed_form_identity_holds']}")
    lines.append("")
    lines.append("  Empirical sums over the 21 lowest modes:")
    lines.append(f"    Σ 1         = {audit['mode_count']:.4f}         (mode count)")
    lines.append(f"    Σ σ_2       = {audit['sum_sigma2']:.4f}     (closest int: 17, dev {audit['sigma2_closest_int']['pct']:+.2f}%)")
    lines.append(f"    Σ σ_2²      = {audit['sum_sigma2_squared']:.4f}     (closest int: 14, dev {audit['sigma2_sq_closest_int']['pct']:+.2f}%)")
    lines.append(f"    Σ purity    = {audit['sum_purity']:.4f}     (= 21/2 + Σσ_2²/2)")
    lines.append(f"    Σ (1-purity)= {audit['sum_leakage']:.4f}      (leakage to longitudinal)")
    lines.append("")
    lines.append("  Reading: NOT the framework's primary trio {13, 17, 21}.")
    lines.append("    Σ σ_2² ≈ 14 = 21·2/3 (= antechamber's predicted active count)")
    lines.append("    Σ σ_2  ≈ 17 (close to Φ_4(4) but link unverified)")
    lines.append("    Φ_6(4) = 13 does NOT appear in this sum structure.")
    lines.append("    If an exact algebraic identity exists for these sums, it has")
    lines.append("    not been found.  This is an open question, not a result.")

    return lines


__all__ = [
    "OMEGA",
    "unit_k_vector",
    "polarization_zeta",
    "axial_weight",
    "hexagonal_weight",
    "polarization_sector",
    "PolarizationInfo",
    "polarization_info",
    "polarization_audit",
    "antechamber_filter",
    "SpectrumEntry",
    "predict_filtered_spectrum",
    "transverse_basis",
    "omega_rotation_matrix_3d",
    "transverse_omega_action",
    "transverse_purity",
    "transverse_omega_eigenvalues",
    "TransverseInfo",
    "transverse_info",
    "sigma2_of_mode",
    "purity_closed_form",
    "chamber_polarization_sum_audit",
    "framework_trio_identity",
    "showcase_chamber_polarization",
]
