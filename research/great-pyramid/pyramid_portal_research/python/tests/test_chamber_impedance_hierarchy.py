"""Tests for chamber_impedance_hierarchy.py — locks {1/68, 2/17, 3/68²}."""

import math
import pytest

from python.chamber_impedance_hierarchy import (
    PHI_4_AT_K4, K_FACES, SO_VERTICES, DIM_SPACE,
    IMP_GLOBAL, IMP_LOCAL, IMP_ROTATIONAL,
    IMP_GLOBAL_DEN, IMP_ROTATIONAL_DEN,
    TROPICAL_YEAR_DAYS, GIZA_LATITUDE_OBSERVED_DEG,
    predicted_year_days, year_match,
    vertex_impedance,
    predicted_coriolis_stretch,
    predicted_coriolis_latitude_deg,
    predicted_coriolis_period_s, predicted_coriolis_period_hours,
    coriolis_at_giza_period_s, coriolis_match,
    latitude_for_D, giza_offset_for_D,
    D_uniqueness_audit, D_minimizing_giza_offset,
    hierarchy_audit, showcase_chamber_impedance_hierarchy,
)


# ---------------------------------------------------------------------------
# Framework constants
# ---------------------------------------------------------------------------

def test_global_impedance_is_one_over_68():
    """68 = Φ_4(4) × K_faces = 17 × 4."""
    assert IMP_GLOBAL_DEN == 68
    assert IMP_GLOBAL == 1.0 / 68.0
    assert abs(IMP_GLOBAL - 0.0147058823529) < 1e-12


def test_local_impedance_is_2_over_17():
    """Local = 8 × Global = 8/68 = 2/17."""
    assert IMP_LOCAL == 8.0 / 68.0
    assert abs(IMP_LOCAL - 2.0 / 17.0) < 1e-15
    assert abs(IMP_LOCAL - SO_VERTICES * IMP_GLOBAL) < 1e-15


def test_local_to_global_relationship():
    """The Stellated Octahedron's 8 vertices × global impedance = local impedance."""
    v = vertex_impedance()
    assert v["identity_holds"]


def test_rotational_impedance_is_D_over_68_squared():
    """Order-2: D / 68² with D=3 → 3/4624."""
    assert IMP_ROTATIONAL_DEN == 68 * 68
    assert IMP_ROTATIONAL_DEN == 4624
    assert IMP_ROTATIONAL == 3.0 / 4624.0
    assert abs(IMP_ROTATIONAL - 0.000648789) < 1e-7


def test_phi_4_at_K4_is_17():
    """Φ_4(4) = K² + 1 = 17."""
    assert PHI_4_AT_K4 == 17
    assert PHI_4_AT_K4 == K_FACES ** 2 + 1


def test_D_is_3_from_uniqueness():
    """The framework's spatial-dimension uniqueness: 2(D+1) = 2^D → D=3."""
    assert DIM_SPACE == 3
    assert 2 * (DIM_SPACE + 1) == 2 ** DIM_SPACE


# ---------------------------------------------------------------------------
# Order-1 global — year length
# ---------------------------------------------------------------------------

def test_predicted_year_is_365_29():
    """360 × (1 + 1/68) = 365.2941 days."""
    y = predicted_year_days()
    assert abs(y - 365.2941) < 0.01


def test_year_matches_tropical_within_0_02_pct():
    """Predicted year matches observed tropical year to better than 0.02%."""
    m = year_match()
    assert abs(m["relative_error_pct"]) < 0.02


def test_year_error_is_about_5_pct_of_one_day():
    """The leap-year correction is ~ 1/4 day per year. Our error ~0.05 day = ~1 hour."""
    m = year_match()
    assert abs(m["absolute_error_days"]) < 0.1


# ---------------------------------------------------------------------------
# Order-1 local — vertex throat
# ---------------------------------------------------------------------------

def test_vertex_impedance_is_11_76_percent():
    v = vertex_impedance()
    assert abs(v["percent"] - 11.7647) < 0.001


# ---------------------------------------------------------------------------
# Order-2 rotational — Coriolis at Giza
# ---------------------------------------------------------------------------

def test_predicted_coriolis_stretch_matches_3_over_4624():
    assert abs(predicted_coriolis_stretch() - 3.0 / 4624.0) < 1e-15


def test_predicted_coriolis_period_is_23_95_hours():
    """T_Cor = T_sidereal × (1 + 3/4624) ≈ 23.95 h exactly."""
    h = predicted_coriolis_period_hours()
    assert abs(h - 23.9500) < 0.001


def test_predicted_coriolis_latitude_is_close_to_giza():
    """Predicted latitude 29.9786°; Giza 29.9792°.  Offset < 100 m."""
    phi_pred = predicted_coriolis_latitude_deg()
    offset_deg = GIZA_LATITUDE_OBSERVED_DEG - phi_pred
    offset_m = abs(offset_deg) * 111320.0  # m per degree of latitude
    assert offset_m < 100.0   # within 100 m
    # More precisely: within 80 m
    assert offset_m < 80.0


def test_coriolis_period_relative_error_under_30_ppm():
    """Predicted T_Cor matches observed at Giza within 30 ppm."""
    m = coriolis_match()
    assert abs(m["period_relative_error_ppm"]) < 30.0


def test_coriolis_at_giza_period_about_86218_s():
    """The actual Coriolis period at Giza's measured latitude."""
    T = coriolis_at_giza_period_s()
    assert 86215.0 < T < 86225.0


# ---------------------------------------------------------------------------
# D-uniqueness audit
# ---------------------------------------------------------------------------

def test_D_3_minimizes_giza_offset_in_range_1_to_8():
    """The integer D that minimizes the Giza-latitude offset is 3."""
    D_best = D_minimizing_giza_offset((1, 8))
    assert D_best == 3


def test_D_3_offset_under_100m():
    """D=3 places the predicted latitude within 100 m of Giza."""
    row = giza_offset_for_D(3)
    assert row["offset_abs_km"] < 0.1   # under 100 m


def test_neighbouring_D_values_are_much_worse():
    """D=2 and D=4 are at least 10× worse than D=3."""
    row_D3 = giza_offset_for_D(3)
    row_D2 = giza_offset_for_D(2)
    row_D4 = giza_offset_for_D(4)
    assert row_D2["offset_abs_km"] > 10.0 * row_D3["offset_abs_km"]
    assert row_D4["offset_abs_km"] > 10.0 * row_D3["offset_abs_km"]


def test_audit_has_correct_shape():
    rows = D_uniqueness_audit((1, 6))
    assert len(rows) == 6
    Ds = [r["D"] for r in rows]
    assert Ds == [1, 2, 3, 4, 5, 6]
    for r in rows:
        assert "predicted_latitude_deg" in r
        assert "offset_abs_km" in r


# ---------------------------------------------------------------------------
# Combined audit dataclass
# ---------------------------------------------------------------------------

def test_hierarchy_audit_assembles_all_pieces():
    h = hierarchy_audit()
    assert h.impedance_global == 1.0 / 68.0
    assert h.impedance_local == 2.0 / 17.0
    assert h.impedance_rotational == 3.0 / 4624.0
    assert h.D_minimizing == 3
    assert abs(h.year_match["relative_error_pct"]) < 0.02
    assert abs(h.coriolis_match["period_relative_error_ppm"]) < 30.0


# ---------------------------------------------------------------------------
# Cross-consistency with kc_kinematics
# ---------------------------------------------------------------------------

def test_consistency_with_kc_kinematics_giza_period():
    """The Coriolis period at Giza computed via kc_kinematics matches the
    period computed via the impedance-hierarchy module."""
    from python.kc_kinematics import (
        OMEGA_EARTH_VERTICAL, coriolis_split_rad_per_s, SIDEREAL_DAY_S,
    )
    from python.pyramid_resonance import Mode

    m = Mode(1, 1, 1, 0.0205)
    delta_omega = coriolis_split_rad_per_s(m)
    period_via_kinematics = 2.0 * math.pi / delta_omega

    period_via_hierarchy = coriolis_at_giza_period_s()

    assert abs(period_via_kinematics - period_via_hierarchy) < 1.0


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def test_showcase_runs_and_contains_keywords():
    out = showcase_chamber_impedance_hierarchy()
    text = "\n".join(out)
    assert "IMPEDANCE HIERARCHY" in text
    assert "1/68" in text
    assert "2/17" in text
    assert "3/68" in text or "3/4624" in text
    assert "Giza" in text or "giza" in text.lower()
    assert "365" in text
    assert "D = 3" in text or "D=3" in text


def test_showcase_marks_D3_with_star():
    out = showcase_chamber_impedance_hierarchy()
    text = "\n".join(out)
    # The D=3 row should be marked
    lines_with_3 = [l for l in out if l.strip().startswith("3 |")]
    assert len(lines_with_3) >= 1
    assert "★" in lines_with_3[0]


# ---------------------------------------------------------------------------
# Geodynamic correction — African plate drift since construction
# ---------------------------------------------------------------------------

def test_years_since_construction():
    """Years from ~2500 BCE to current year."""
    from python.chamber_impedance_hierarchy import (
        years_since_construction,
        PYRAMID_CONSTRUCTION_YEAR_BCE, CURRENT_YEAR_CE,
    )
    assert years_since_construction() == CURRENT_YEAR_CE + PYRAMID_CONSTRUCTION_YEAR_BCE
    assert years_since_construction() > 4000


def test_drift_correction_at_typical_rate():
    """At 12 mm/yr northward, ~4500 yr × 12 mm = ~54 m."""
    from python.chamber_impedance_hierarchy import drift_correction_m
    shift = drift_correction_m(12.0)
    assert 50.0 < shift < 60.0


def test_drift_brackets_residual():
    """The MORVEL drift bracket (10–15 mm/yr × 4500 yr = 45–68 m)
    should bracket the 62 m modern residual."""
    from python.chamber_impedance_hierarchy import (
        geodynamic_bracket, GIZA_LATITUDE_OBSERVED_DEG, DEG_TO_M_AT_EARTH,
        predicted_coriolis_latitude_deg,
    )
    g = geodynamic_bracket()
    drift_lo = g["lo_drift"]["northward_drift_m"]
    drift_hi = g["hi_drift"]["northward_drift_m"]

    residual_m = (GIZA_LATITUDE_OBSERVED_DEG - predicted_coriolis_latitude_deg()) * DEG_TO_M_AT_EARTH

    # Modern residual is bracketed by drift
    assert drift_lo <= residual_m * 1.1   # 10% margin
    assert drift_hi >= residual_m * 0.9


def test_construction_epoch_residual_within_uncertainty():
    """At a drift rate that lies in the MORVEL range, the construction-epoch
    residual should be smaller in magnitude than 30 m (well within latitude
    measurement uncertainty for a 4500-year-old monument)."""
    from python.chamber_impedance_hierarchy import geodynamic_match
    # at 13.7 mm/yr the construction-epoch residual essentially closes
    m = geodynamic_match(13.7)
    assert abs(m["residual_at_construction_m"]) < 30.0


def test_high_drift_essentially_closes_residual():
    """At the MORVEL high-end drift rate (15 mm/yr × 4500 yr = 68 m), the
    construction-epoch residual essentially zeros: ~0.6 m, well below any
    plausible historical-latitude measurement uncertainty."""
    from python.chamber_impedance_hierarchy import geodynamic_match
    m = geodynamic_match(15.0)
    assert abs(m["residual_at_construction_m"]) < 5.0


def test_low_drift_leaves_small_residual():
    """At MORVEL low-end (10 mm/yr × 4500 yr = 45 m), residual at construction
    is ~23 m — left over for other geodetic corrections (KC south offset ~7 m,
    geodetic-vs-astronomical latitude deflection of ~5–15 m)."""
    from python.chamber_impedance_hierarchy import geodynamic_match
    m = geodynamic_match(10.0)
    # 17 m to 30 m
    assert 15.0 < m["residual_at_construction_m"] < 35.0


def test_showcase_includes_geodynamic_section():
    out = showcase_chamber_impedance_hierarchy()
    text = "\n".join(out)
    assert "Geodynamic" in text or "geodynamic" in text.lower() or "drift" in text.lower()
    assert "construction" in text.lower()
    assert "chronology" in text.lower() or "Chronology" in text


# ---------------------------------------------------------------------------
# Symmetric mean-drift formulation (chronology-agnostic)
# ---------------------------------------------------------------------------

def test_required_drift_inverse_of_implied_age():
    """The two inverse functions round-trip."""
    from python.chamber_impedance_hierarchy import (
        required_mean_drift_rate_mm_per_yr,
        implied_construction_age_years,
    )
    age = 8_000.0
    r = required_mean_drift_rate_mm_per_yr(age)
    age_back = implied_construction_age_years(r)
    assert abs(age - age_back) < 0.01


def test_required_drift_at_khufu_matches_morvel_high():
    """At 4500 yr, required mean rate is ~15.2 mm/yr (MORVEL high)."""
    from python.chamber_impedance_hierarchy import required_mean_drift_rate_mm_per_yr
    r = required_mean_drift_rate_mm_per_yr(4500)
    assert 14.5 < r < 16.0


def test_required_drift_at_younger_dryas_is_half_modern():
    """At 11,700 yr (end of YD), required mean rate is ~5.9 mm/yr,
    ≈ half of modern MORVEL — plausible for Holocene-averaged drift."""
    from python.chamber_impedance_hierarchy import required_mean_drift_rate_mm_per_yr
    r = required_mean_drift_rate_mm_per_yr(11_700)
    assert 5.4 < r < 6.4


def test_chronology_audit_returns_eight_rows():
    """Default chronology audit covers eight ages spanning conventional + alternative."""
    from python.chamber_impedance_hierarchy import chronology_audit
    rows = chronology_audit()
    assert len(rows) == 8
    # Each row has required mean drift and MORVEL ratios
    for row in rows:
        assert "age_years" in row
        assert "required_mean_drift_mm_per_yr" in row
        assert "morvel_modern_lo_ratio" in row


def test_drift_age_product_equals_residual():
    """For any chronology, (required mean rate) × (age) = modern residual.
    This is the chronology-agnostic geometric lock."""
    from python.chamber_impedance_hierarchy import (
        required_mean_drift_rate_mm_per_yr, modern_residual_m,
    )
    R = modern_residual_m()
    for age in [4_500, 7_000, 10_500, 12_000]:
        r = required_mean_drift_rate_mm_per_yr(age)
        product_m = r * 1e-3 * age   # mm/yr → m/yr × yr = m
        assert abs(product_m - R) < 1e-6


def test_modern_residual_is_about_62m():
    from python.chamber_impedance_hierarchy import modern_residual_m
    r = modern_residual_m()
    assert 60.0 < r < 75.0
