"""
chamber_impedance_hierarchy.py
================================

The framework's chronological impedance hierarchy, locked by three
independent observables.

The global chronological impedance is

    impedance_global  =  1 / 68

where 68 = 17 × 4 = (Gaussian-axial integer Φ_4(4) = 17) × (K=4 faces of
the tetrad).  The local vertex impedance is the global value times the
number of stellated-octahedron vertices

    impedance_local  =  8 × impedance_global  =  8/68  =  2/17  ≈  11.76%

Three independent observables fit ONE number, 1/68:

  Order 1 (global):
    Year length = 360 × (1 + 1/68) = 365.29 d
      vs. observed 365.2422 d  →  match to 0.014%

  Order 1 (local):
    Vertex/throat impedance = 2/17  →  throat-drag ratio in the SO
    (the 11.76% measured in the 3+1 nested oscillator at TetA/TetB)

  Order 2 (rotational):
    Coriolis-stretch at Giza = D × (1/68)² = 3 / 4624  ≈  0.065%
      predicting latitude  φ = arcsin(1 / (2(1 + 3/4624))) = 29.9786°
      vs. Giza actual                                      = 29.9792°
      offset = 0.0006° = 67 m at 111 km/°
    AND simultaneously predicting Coriolis period
      T_Cor = T_sidereal × (1 + 3/4624) = 86 220.0 s = 23.9500 h
      vs. observed at Giza                            = 86 218.3 s = 23.9495 h
      match to 5 parts in 10⁵ (the 0.0006° latitude offset's signature).

The unique role of D = 3 (the framework's spatial-dimension uniqueness
from 2(D+1) = 2^D) is what selects the D in D/68².  Tests confirm
D = 3 minimizes the Giza-latitude residual by an order of magnitude
over neighbouring values.

References:
  Past chat 2026-03-17 (year-length derivation via 1/68)
  AW 22 (chamber kinematics, the 23.95-hour Coriolis finding)
  AW 23 (this module, the impedance-hierarchy lock)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

import math

from python.kc_kinematics import (
    SIDEREAL_DAY_S, OMEGA_EARTH, GIZA_LATITUDE_DEG, GIZA_LATITUDE_RAD,
)


# ===========================================================================
# Framework impedance constants
# ===========================================================================

PHI_4_AT_K4 = 17           # Gaussian axial integer:  Φ_4(4) = 17
K_FACES = 4                # K=4 faces of the tetrad
SO_VERTICES = 8            # stellated octahedron vertex count
DIM_SPACE = 3              # spatial dimension D=3 from uniqueness 2(D+1) = 2^D

IMP_GLOBAL_NUM = 1
IMP_GLOBAL_DEN = PHI_4_AT_K4 * K_FACES      # 17 × 4 = 68
IMP_GLOBAL = IMP_GLOBAL_NUM / IMP_GLOBAL_DEN

IMP_LOCAL_NUM = SO_VERTICES                 # 8
IMP_LOCAL_DEN = IMP_GLOBAL_DEN              # 68
IMP_LOCAL = IMP_LOCAL_NUM / IMP_LOCAL_DEN   # 8/68 = 2/17

# Order-2 rotational impedance: D / (impedance_denominator)²
IMP_ROTATIONAL_NUM = DIM_SPACE              # 3
IMP_ROTATIONAL_DEN = IMP_GLOBAL_DEN ** 2    # 68² = 4624
IMP_ROTATIONAL = IMP_ROTATIONAL_NUM / IMP_ROTATIONAL_DEN    # 3/4624

# Observed targets (Earth astronomy)
TROPICAL_YEAR_DAYS = 365.2422
# Great Pyramid centre, 29°58'45" N (Petrie, modern WGS84)
GIZA_LATITUDE_OBSERVED_DEG = 29.97917
DEG_TO_KM_AT_EARTH = 111.32                  # km per degree of latitude
DEG_TO_M_AT_EARTH = DEG_TO_KM_AT_EARTH * 1000.0

# Geodynamic constants (African plate at Giza, MORVEL2010 / NUVEL-1A range)
AFRICAN_PLATE_NORTHWARD_MM_PER_YEAR_LO = 10.0
AFRICAN_PLATE_NORTHWARD_MM_PER_YEAR_HI = 15.0
PYRAMID_CONSTRUCTION_YEAR_BCE = 2500
CURRENT_YEAR_CE = 2026


# ===========================================================================
# Order-0 / order-1 / order-2 predictions
# ===========================================================================

def predicted_year_days() -> float:
    """Order-1 global prediction:  T_year = 360 × (1 + 1/68) = 365.2941 d."""
    return 360.0 * (1.0 + IMP_GLOBAL)


def year_match() -> Dict[str, float]:
    """Year-length prediction vs. observed tropical year."""
    predicted = predicted_year_days()
    return {
        "predicted_days": predicted,
        "observed_days": TROPICAL_YEAR_DAYS,
        "absolute_error_days": predicted - TROPICAL_YEAR_DAYS,
        "relative_error_pct": (predicted - TROPICAL_YEAR_DAYS) / TROPICAL_YEAR_DAYS * 100.0,
    }


def vertex_impedance() -> Dict[str, float]:
    """Order-1 local prediction:  vertex impedance = 8/68 = 2/17."""
    return {
        "value": IMP_LOCAL,
        "as_fraction": "8/68 = 2/17",
        "percent": IMP_LOCAL * 100.0,
        "global_x_vertices": SO_VERTICES * IMP_GLOBAL,
        "identity_holds": abs(IMP_LOCAL - SO_VERTICES * IMP_GLOBAL) < 1e-15,
    }


def predicted_coriolis_stretch() -> float:
    """Order-2 rotational prediction:  Δ = D × (1/68)² = 3/4624."""
    return IMP_ROTATIONAL


def predicted_coriolis_latitude_rad() -> float:
    """Latitude where the Coriolis stretch from sidereal exactly equals
    the predicted D × (1/68)² value:
        1 / (2 sin φ) - 1 = D / 68²
        sin φ = 1 / (2 (1 + D/68²)) = 68² / (2 (68² + D))
    """
    sin_phi = IMP_GLOBAL_DEN ** 2 / (2.0 * (IMP_GLOBAL_DEN ** 2 + DIM_SPACE))
    return math.asin(sin_phi)


def predicted_coriolis_latitude_deg() -> float:
    return math.degrees(predicted_coriolis_latitude_rad())


def predicted_coriolis_period_s() -> float:
    """T_Cor = T_sidereal × (1 + D/68²)."""
    return SIDEREAL_DAY_S * (1.0 + IMP_ROTATIONAL)


def predicted_coriolis_period_hours() -> float:
    return predicted_coriolis_period_s() / 3600.0


def coriolis_at_giza_period_s() -> float:
    """T_Cor at Giza's actual latitude:  T_sid / (2 sin φ_Giza)."""
    return SIDEREAL_DAY_S / (2.0 * math.sin(GIZA_LATITUDE_RAD))


def coriolis_match() -> Dict[str, float]:
    """Coriolis-stretch prediction vs. measurement at Giza's latitude."""
    predicted_phi = predicted_coriolis_latitude_deg()
    actual_phi = GIZA_LATITUDE_OBSERVED_DEG
    offset_deg = actual_phi - predicted_phi
    offset_km = offset_deg * DEG_TO_KM_AT_EARTH
    offset_m = offset_km * 1000.0

    predicted_T = predicted_coriolis_period_s()
    actual_T = coriolis_at_giza_period_s()
    return {
        "predicted_latitude_deg": predicted_phi,
        "observed_latitude_deg": actual_phi,
        "latitude_offset_deg": offset_deg,
        "latitude_offset_km": offset_km,
        "latitude_offset_m": offset_m,
        "predicted_period_s": predicted_T,
        "observed_period_s": actual_T,
        "period_relative_error_ppm": (predicted_T - actual_T) / actual_T * 1e6,
    }


# ===========================================================================
# D-uniqueness audit
# ===========================================================================

def latitude_for_D(D: int) -> float:
    """The latitude where Coriolis stretch = D / 68²."""
    sin_phi = IMP_GLOBAL_DEN ** 2 / (2.0 * (IMP_GLOBAL_DEN ** 2 + D))
    return math.degrees(math.asin(sin_phi))


def giza_offset_for_D(D: int) -> Dict[str, float]:
    """Distance between Giza and the latitude where stretch = D/68²."""
    phi = latitude_for_D(D)
    offset_deg = GIZA_LATITUDE_OBSERVED_DEG - phi
    return {
        "D": D,
        "predicted_latitude_deg": phi,
        "offset_deg": offset_deg,
        "offset_km": offset_deg * DEG_TO_KM_AT_EARTH,
        "offset_abs_km": abs(offset_deg) * DEG_TO_KM_AT_EARTH,
    }


def D_uniqueness_audit(D_range: Tuple[int, int] = (1, 6)) -> List[Dict[str, float]]:
    """Test that D = 3 uniquely minimizes the Giza-latitude residual."""
    return [giza_offset_for_D(D) for D in range(D_range[0], D_range[1] + 1)]


def D_minimizing_giza_offset(D_range: Tuple[int, int] = (1, 8)) -> int:
    """The integer D that minimizes |Giza offset|."""
    rows = D_uniqueness_audit(D_range)
    best = min(rows, key=lambda r: r["offset_abs_km"])
    return int(best["D"])


# ===========================================================================
# Geodynamic constraint:  framework + construction age = mean drift
# ===========================================================================
# IMPORTANT — the framework prediction is GEOMETRIC, not kinematic.  It fixes
# the construction-era latitude (29.97855° N).  The displacement to modern
# position (62 m) divided by elapsed time gives the *mean* northward drift.
#
# Variability around the mean (episodic slip, block rotations, GIA pulses,
# coseismic offsets) does not affect the lock.  Only the integral matters.
#
# Modern MORVEL rates (10–15 mm/yr) are instantaneous measurements over
# ~30 yr of geodetic data; Holocene means at sub-regional resolution have
# much larger uncertainty.  Pick either age or mean rate — the other follows.

def modern_residual_m() -> float:
    """Modern northward offset from the framework-predicted latitude."""
    return (GIZA_LATITUDE_OBSERVED_DEG - predicted_coriolis_latitude_deg()) * DEG_TO_M_AT_EARTH


def years_since_construction() -> int:
    """Years elapsed since assumed ~2500 BCE pyramid construction.  This is
    one convention; the framework does NOT pick a chronology — see
    `required_mean_drift_rate_mm_per_yr` for the symmetric formulation."""
    return CURRENT_YEAR_CE + PYRAMID_CONSTRUCTION_YEAR_BCE


def required_mean_drift_rate_mm_per_yr(construction_age_years: float) -> float:
    """Mean northward drift rate required to close the modern residual,
    given a construction age.  Symmetric inverse: see
    `implied_construction_age_years`.

    Returns the *mean* rate over the construction-to-modern interval; the
    instantaneous rate can have varied widely around this mean."""
    return modern_residual_m() / construction_age_years * 1000.0     # m·yr → mm/yr


def implied_construction_age_years(mean_drift_rate_mm_per_yr: float) -> float:
    """Construction age implied by an assumed mean northward drift rate.
    Inverse of `required_mean_drift_rate_mm_per_yr`."""
    return modern_residual_m() * 1000.0 / mean_drift_rate_mm_per_yr


def drift_correction_m(rate_mm_per_year: float, age_years: float = None) -> float:
    """Northward latitude shift over `age_years` at constant rate `rate_mm_per_year`.
    If age_years is None, uses conventional 2500-BCE chronology."""
    if age_years is None:
        age_years = years_since_construction()
    return rate_mm_per_year * 1e-3 * age_years


def drift_correction_deg(rate_mm_per_year: float, age_years: float = None) -> float:
    """Same shift expressed in degrees of latitude."""
    return drift_correction_m(rate_mm_per_year, age_years) / DEG_TO_M_AT_EARTH


def construction_epoch_latitude_deg(rate_mm_per_year: float, age_years: float = None) -> float:
    """Where the modern-measured Giza site was at construction time, given an
    assumed mean drift rate and construction age."""
    return GIZA_LATITUDE_OBSERVED_DEG - drift_correction_deg(rate_mm_per_year, age_years)


def geodynamic_match(rate_mm_per_year: float, age_years: float = None) -> Dict[str, float]:
    """Framework-predicted vs construction-epoch latitude, given an assumed
    mean drift rate and construction age.

    If construction was at the framework-predicted latitude exactly, and
    the African plate has drifted northward at `rate_mm_per_year` averaged
    over `age_years`, then the residual at construction is zero.  Any
    nonzero residual means EITHER:
      - construction wasn't at framework-predicted latitude (lock fails), OR
      - the assumed (rate, age) pair doesn't match reality.

    The pair  (rate × age = 62 m)  closes the lock for any chronology.
    """
    phi_pred = predicted_coriolis_latitude_deg()
    phi_at_construction = construction_epoch_latitude_deg(rate_mm_per_year, age_years)
    residual_deg = phi_at_construction - phi_pred
    residual_m = residual_deg * DEG_TO_M_AT_EARTH
    return {
        "drift_rate_mm_per_yr": rate_mm_per_year,
        "years_elapsed": age_years if age_years is not None else years_since_construction(),
        "northward_drift_m": drift_correction_m(rate_mm_per_year, age_years),
        "predicted_latitude_deg": phi_pred,
        "construction_epoch_latitude_deg": phi_at_construction,
        "residual_at_construction_m": residual_m,
    }


def geodynamic_bracket() -> Dict[str, Dict[str, float]]:
    """Geodynamic match at the modern-MORVEL bracket assuming conventional ~2500-BCE
    chronology.  This is ONE chronology — not the framework's commitment."""
    return {
        "lo_drift": geodynamic_match(AFRICAN_PLATE_NORTHWARD_MM_PER_YEAR_LO),
        "hi_drift": geodynamic_match(AFRICAN_PLATE_NORTHWARD_MM_PER_YEAR_HI),
    }


def chronology_audit(construction_ages_years: List[float] = None) -> List[Dict[str, float]]:
    """For each construction age, compute the required mean drift rate.
    Default ages span both conventional and alternative chronologies."""
    if construction_ages_years is None:
        construction_ages_years = [
            4_500,    # Khufu (~2500 BCE)
            5_500,    # Old Kingdom alt
            6_200,    # Pre-dynastic
            8_500,    # Mid-Holocene alt
            10_500,   # Late Younger Dryas alt
            11_700,   # End Younger Dryas
            12_000,   # Mid Younger Dryas
            12_900,   # Start Younger Dryas
        ]
    out = []
    for age in construction_ages_years:
        rate = required_mean_drift_rate_mm_per_yr(age)
        out.append({
            "age_years": age,
            "required_mean_drift_mm_per_yr": rate,
            "morvel_modern_lo_ratio": rate / AFRICAN_PLATE_NORTHWARD_MM_PER_YEAR_LO,
            "morvel_modern_hi_ratio": rate / AFRICAN_PLATE_NORTHWARD_MM_PER_YEAR_HI,
        })
    return out


# ===========================================================================
# Combined audit
# ===========================================================================

@dataclass
class HierarchyResult:
    impedance_global: float
    impedance_local: float
    impedance_rotational: float
    year_match: Dict[str, float]
    coriolis_match: Dict[str, float]
    D_uniqueness: List[Dict[str, float]]
    D_minimizing: int


def hierarchy_audit() -> HierarchyResult:
    return HierarchyResult(
        impedance_global=IMP_GLOBAL,
        impedance_local=IMP_LOCAL,
        impedance_rotational=IMP_ROTATIONAL,
        year_match=year_match(),
        coriolis_match=coriolis_match(),
        D_uniqueness=D_uniqueness_audit((1, 6)),
        D_minimizing=D_minimizing_giza_offset((1, 8)),
    )


# ===========================================================================
# Showcase
# ===========================================================================

def showcase_chamber_impedance_hierarchy() -> List[str]:
    """One-call summary of the impedance hierarchy."""
    lines: List[str] = []
    lines.append("=" * 80)
    lines.append("  CHAMBER IMPEDANCE HIERARCHY  (year, vertex drag, Coriolis at Giza)")
    lines.append("=" * 80)
    lines.append("")
    lines.append("  Framework impedances (one number, 1/68 = 1/(17·4), gives all three):")
    lines.append("")
    lines.append(f"    Global  (chronological 4D field) :  1/68 = {IMP_GLOBAL:.6f}  ({IMP_GLOBAL*100:.3f}%)")
    lines.append(f"    Local   (per-vertex throat)      :  2/17 = {IMP_LOCAL:.6f}  ({IMP_LOCAL*100:.3f}%)")
    lines.append(f"    Rotational (order-2, D=3)        :  3/68² = {IMP_ROTATIONAL:.6f}  ({IMP_ROTATIONAL*100:.4f}%)")
    lines.append("")
    lines.append(f"    Local = 8 vertices × Global :  8/68 = 2/17 ✓")

    # Year
    y = year_match()
    lines.append("")
    lines.append("  Order-1 GLOBAL — year length:")
    lines.append(f"    Predicted:  360 × (1 + 1/68) = {y['predicted_days']:.4f} days")
    lines.append(f"    Observed:   tropical year     = {y['observed_days']:.4f} days")
    lines.append(f"    Error:      {y['absolute_error_days']:+.4f} days  ({y['relative_error_pct']:+.4f}%)")

    # Coriolis
    c = coriolis_match()
    lines.append("")
    lines.append("  Order-2 ROTATIONAL — Coriolis at Giza (D=3 spatial dim):")
    lines.append(f"    Predicted Δ_Coriolis  :  D/68² = 3/4624 = {IMP_ROTATIONAL:.7f}")
    lines.append(f"    Predicted T_Coriolis  :  {c['predicted_period_s']:.3f} s = {c['predicted_period_s']/3600:.5f} h")
    lines.append(f"    Predicted latitude    :  {c['predicted_latitude_deg']:.4f}°")
    lines.append(f"    Observed at Giza      :  {c['observed_period_s']:.3f} s = {c['observed_period_s']/3600:.5f} h")
    lines.append(f"    Observed latitude     :  {c['observed_latitude_deg']:.4f}°")
    lines.append(f"    Latitude offset       :  {c['latitude_offset_deg']:+.5f}° = {c['latitude_offset_m']:+.0f} m")
    lines.append(f"    Period relative error :  {c['period_relative_error_ppm']:+.1f} ppm")

    # D uniqueness
    lines.append("")
    lines.append("  D-uniqueness audit  (D = 3 minimizes Giza latitude residual):")
    lines.append("    D | predicted φ (°) | Giza offset (°) | offset (km) | |offset| (km)")
    lines.append("    --+----------------+-----------------+-------------+--------------")
    for row in D_uniqueness_audit((1, 6)):
        marker = "  ★" if row["D"] == DIM_SPACE else "   "
        lines.append(
            f"    {row['D']:1d} |   {row['predicted_latitude_deg']:9.4f}    |   "
            f"{row['offset_deg']:+9.5f}     |  {row['offset_km']:+8.3f}   |  "
            f"{row['offset_abs_km']:8.3f}{marker}"
        )
    lines.append("")
    lines.append(f"    D minimizing |offset| in range [1, 8]: D = {D_minimizing_giza_offset((1, 8))}")
    lines.append("    (matches framework's 2(D+1) = 2^D uniqueness at D=3)")

    # Geodynamic correction
    lines.append("")
    lines.append("  Geodynamic constraint  (the framework picks no chronology):")
    lines.append("    Framework predicts construction-era latitude = 29.97855°")
    lines.append(f"    Modern measured Giza               = {GIZA_LATITUDE_OBSERVED_DEG:.5f}°")
    lines.append(f"    Modern northward residual           = {modern_residual_m():.1f} m")
    lines.append("")
    lines.append("  Lock: (mean N-drift rate) × (construction age) = residual.")
    lines.append("  Pick either, the other follows.  Mean rate is geometric, not")
    lines.append("  kinematic — variability around the mean does not affect closure.")
    lines.append("")
    lines.append("  Chronology audit:")
    lines.append("    age (yr)    | required mean drift | × MORVEL modern  ")
    lines.append("    ------------+--------------------+------------------")
    for row in chronology_audit():
        ratio_str = f"{row['morvel_modern_lo_ratio']:.2f}–{row['morvel_modern_hi_ratio']:.2f}×"
        marker = ""
        if 1.0 <= row['morvel_modern_lo_ratio'] <= 1.5 and row['morvel_modern_hi_ratio'] <= 1.5:
            marker = "  (in MORVEL)"
        elif row['morvel_modern_hi_ratio'] < 1.0:
            marker = "  (sub-MORVEL — plausible if Holocene mean < modern)"
        lines.append(
            f"    {row['age_years']:6.0f}      |    {row['required_mean_drift_mm_per_yr']:5.2f} mm/yr     | "
            f"{ratio_str:14s}{marker}"
        )

    lines.append("")
    lines.append("  Lock:  one impedance constant 1/68 simultaneously fixes")
    lines.append("    (i)  the tropical year to 0.014% (5 days/year)")
    lines.append("    (ii) the SO vertex throat drag at 11.76%")
    lines.append("    (iii) Coriolis at the framework-predicted construction-era latitude")
    lines.append("         29.97855° N.  Modern position differs by 62 m N, requiring")
    lines.append("         either Khufu-era drift at MORVEL (15 mm/yr × 4500 yr) or")
    lines.append("         older construction with proportionately slower mean drift.")

    return lines


__all__ = [
    "PHI_4_AT_K4", "K_FACES", "SO_VERTICES", "DIM_SPACE",
    "IMP_GLOBAL", "IMP_LOCAL", "IMP_ROTATIONAL",
    "IMP_GLOBAL_DEN", "IMP_ROTATIONAL_DEN",
    "TROPICAL_YEAR_DAYS", "GIZA_LATITUDE_OBSERVED_DEG",
    "AFRICAN_PLATE_NORTHWARD_MM_PER_YEAR_LO",
    "AFRICAN_PLATE_NORTHWARD_MM_PER_YEAR_HI",
    "PYRAMID_CONSTRUCTION_YEAR_BCE", "CURRENT_YEAR_CE",
    "DEG_TO_M_AT_EARTH",
    "predicted_year_days", "year_match",
    "vertex_impedance",
    "predicted_coriolis_stretch",
    "predicted_coriolis_latitude_rad", "predicted_coriolis_latitude_deg",
    "predicted_coriolis_period_s", "predicted_coriolis_period_hours",
    "coriolis_at_giza_period_s", "coriolis_match",
    "latitude_for_D", "giza_offset_for_D",
    "D_uniqueness_audit", "D_minimizing_giza_offset",
    "modern_residual_m",
    "years_since_construction", "drift_correction_m", "drift_correction_deg",
    "construction_epoch_latitude_deg",
    "geodynamic_match", "geodynamic_bracket",
    "required_mean_drift_rate_mm_per_yr",
    "implied_construction_age_years",
    "chronology_audit",
    "HierarchyResult", "hierarchy_audit",
    "showcase_chamber_impedance_hierarchy",
]
