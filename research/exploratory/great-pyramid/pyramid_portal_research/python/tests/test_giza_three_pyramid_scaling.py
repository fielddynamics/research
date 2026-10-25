"""Tests for giza_three_pyramid_scaling.py — 3-pyramid Sierpinski lock."""

import math
import pytest

from python.giza_three_pyramid_scaling import (
    KHUFU_BASE_M, KHAFRE_BASE_M, MENKAURE_BASE_M,
    K_FACES, PHI_4_AT_K4, SO_VERTICES, K_SQUARED_MINUS_ONE,
    K_TO_FOURTH_MINUS_ONE,
    predicted_khafre_ratio, predicted_menkaure_ratio,
    predicted_menkaure_khafre_ratio,
    observed_khafre_ratio, observed_menkaure_ratio,
    observed_menkaure_khafre_ratio,
    audit_khafre_ratio, audit_menkaure_ratio, audit_menkaure_khafre_ratio,
    all_audits, hierarchy_match_within_uncertainty,
    showcase_three_pyramid_scaling,
)


# ---------------------------------------------------------------------------
# Framework integer constants
# ---------------------------------------------------------------------------

def test_K_is_4():
    assert K_FACES == 4


def test_phi_4_is_17():
    """Φ_4(K) = K² + 1 = 17 at K=4."""
    assert PHI_4_AT_K4 == 17


def test_so_vertices_is_8():
    """Stellated octahedron has 8 vertices."""
    assert SO_VERTICES == 8


def test_K_squared_minus_one_is_15():
    assert K_SQUARED_MINUS_ONE == 15


def test_K_to_fourth_minus_one_is_255():
    """K^4 − 1 = (K² − 1)(K² + 1) = 15 × 17 = 255."""
    assert K_TO_FOURTH_MINUS_ONE == 255
    assert K_TO_FOURTH_MINUS_ONE == K_SQUARED_MINUS_ONE * PHI_4_AT_K4


# ---------------------------------------------------------------------------
# Predicted ratios are framework integer fractions
# ---------------------------------------------------------------------------

def test_khafre_predicted_is_15_over_16():
    assert predicted_khafre_ratio() == 15.0 / 16.0


def test_menkaure_predicted_is_8_over_17():
    assert predicted_menkaure_ratio() == 8.0 / 17.0


def test_menkaure_khafre_predicted_is_128_over_255():
    """(8/17) / (15/16) = (8 × 16) / (17 × 15) = 128 / 255."""
    assert abs(predicted_menkaure_khafre_ratio() - 128.0 / 255.0) < 1e-15


def test_menkaure_khafre_factor_is_2_to_7_over_K4_minus_1():
    """128/255 = 2^7 / (K^4 − 1) at K=4."""
    expected = 128.0 / (K_FACES ** 4 - 1)
    assert abs(predicted_menkaure_khafre_ratio() - expected) < 1e-15


# ---------------------------------------------------------------------------
# Observed ratios
# ---------------------------------------------------------------------------

def test_observed_khafre_ratio_is_about_0_934():
    obs = observed_khafre_ratio()
    assert 0.930 < obs < 0.940


def test_observed_menkaure_ratio_is_about_0_471():
    obs = observed_menkaure_ratio()
    assert 0.460 < obs < 0.480


def test_observed_menkaure_khafre_is_about_half():
    obs = observed_menkaure_khafre_ratio()
    assert 0.49 < obs < 0.52


# ---------------------------------------------------------------------------
# Match quality — these are the actual lock tests
# ---------------------------------------------------------------------------

def test_khafre_match_within_1_percent():
    """Khafre/Khufu matches 15/16 to better than 1%."""
    a = audit_khafre_ratio()
    assert abs(a.deviation_pct) < 1.0


def test_menkaure_match_within_0_5_percent():
    """Menkaure/Khufu matches 8/17 to better than 0.5% — the cleanest hit."""
    a = audit_menkaure_ratio()
    assert abs(a.deviation_pct) < 0.5


def test_menkaure_khufu_match_at_sub_percent():
    """The Menkaure/Khufu = 8/17 fit is the sharpest at ~0.1%."""
    a = audit_menkaure_ratio()
    assert abs(a.deviation_pct) < 0.2


def test_menkaure_khafre_match_within_1_percent():
    """Menkaure/Khafre matches 128/255 to better than 1%."""
    a = audit_menkaure_khafre_ratio()
    assert abs(a.deviation_pct) < 1.0


def test_all_within_2_sigma():
    """All three ratios fit within twice measurement uncertainty."""
    assert hierarchy_match_within_uncertainty()


# ---------------------------------------------------------------------------
# Internal structural identities
# ---------------------------------------------------------------------------

def test_khafre_predicted_complements_one_over_K_squared():
    """Khafre/Khufu predicted = 1 − 1/K² at K=4."""
    pred = predicted_khafre_ratio()
    assert abs(pred - (1.0 - 1.0 / K_FACES ** 2)) < 1e-15


def test_menkaure_is_four_times_local_impedance():
    """Menkaure/Khufu = 8/17 = 4 × (2/17) = 4 × impedance_local."""
    pred = predicted_menkaure_ratio()
    assert abs(pred - 4.0 * (2.0 / 17.0)) < 1e-15


def test_khafre_minus_menkaure_uses_different_integers():
    """The 'small step' (Khafre, 15/16) and 'big step' (Menkaure, 8/17)
    use distinct framework integers — Khafre at K², Menkaure at Φ_4(K)."""
    khafre = predicted_khafre_ratio()
    menkaure = predicted_menkaure_ratio()
    # khafre uses denominator K² = 16; menkaure uses Φ_4(K) = 17
    # The factor between them is 128/255 = 2^7 / (K^4 − 1)
    factor = menkaure / khafre
    assert abs(factor - 128.0 / 255.0) < 1e-15


# ---------------------------------------------------------------------------
# Audit dataclass shape
# ---------------------------------------------------------------------------

def test_audit_returns_three_entries():
    audits = all_audits()
    assert len(audits) == 3
    names = [a.name for a in audits]
    assert "Khafre / Khufu" in names
    assert "Menkaure / Khufu" in names
    assert "Menkaure / Khafre" in names


def test_audit_has_uncertainty_field():
    a = audit_khafre_ratio()
    assert hasattr(a, "obs_uncertainty_pct")
    assert a.obs_uncertainty_pct > 0


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def test_showcase_runs_and_contains_keywords():
    out = showcase_three_pyramid_scaling()
    text = "\n".join(out)
    assert "GIZA" in text
    assert "Sierpinski" in text
    assert "Khufu" in text
    assert "Khafre" in text
    assert "Menkaure" in text
    assert "15/16" in text
    assert "8/17" in text
    assert "128/255" in text


# ---------------------------------------------------------------------------
# K=4 ↔ K=5 hinge
# ---------------------------------------------------------------------------

def test_K_algebra_is_4_K_geometry_is_5():
    """The Great Pyramid is K=5 geometrically (square pyramid: 4 sides + base =
    5 faces, 5 vertices), but its DIMENSIONAL RATIOS encode K=4 algebra
    (the chamber's stellated-octahedron cyclotomic structure)."""
    from python.giza_three_pyramid_scaling import K_ALGEBRA, K_GEOMETRY
    assert K_ALGEBRA == 4
    assert K_GEOMETRY == 5


def test_lift_bridge_21_is_phi3_K4_and_phi6_K5():
    """The framework's K=4 ↔ K=5 lift identity: 21 = Φ_3(4) = Φ_6(5).
    This integer bridges the two K-shells."""
    from python.giza_three_pyramid_scaling import PHI_3_AT_K4, PHI_6_AT_K5
    assert PHI_3_AT_K4 == 21
    assert PHI_6_AT_K5 == 21
    assert PHI_3_AT_K4 == PHI_6_AT_K5


def test_phi_4_at_K5_is_26():
    from python.giza_three_pyramid_scaling import PHI_4_AT_K5
    assert PHI_4_AT_K5 == 26


def test_phi_3_at_K5_is_31():
    from python.giza_three_pyramid_scaling import PHI_3_AT_K5
    assert PHI_3_AT_K5 == 31


def test_K4_algebra_fits_pyramid_sizes_better_than_K5_geometry():
    """The empirical finding: K=4 cyclotomic fractions fit observed pyramid
    size ratios at sub-percent precision, while best K=5 fits are ~1-2%."""
    from python.giza_three_pyramid_scaling import K4_wins_over_K5
    assert K4_wins_over_K5()


def test_k4_vs_k5_audit_structure():
    """The k4_vs_k5_audit returns a structured side-by-side comparison."""
    from python.giza_three_pyramid_scaling import k4_vs_k5_audit
    a = k4_vs_k5_audit()
    assert "khafre_khufu" in a
    assert "menkaure_khufu" in a
    for key in ["khafre_khufu", "menkaure_khufu"]:
        assert "K4_best" in a[key]
        assert "K5_best" in a[key]
        assert "K4_better" in a[key]
        # K=4 should win in both
        assert a[key]["K4_better"]


def test_K5_best_khafre_is_at_least_one_percent_off():
    """Best K=5 fit for Khafre/Khufu is at least ~1% off — K=4 wins decisively."""
    from python.giza_three_pyramid_scaling import best_k5_fit_for_khafre_ratio
    name, val, dev = best_k5_fit_for_khafre_ratio()
    assert abs(dev) > 1.0   # at least 1% off
    assert abs(dev) < 5.0   # but not crazy off


def test_K5_best_menkaure_is_at_least_one_percent_off():
    """Best K=5 fit for Menkaure/Khufu is at least ~1% off."""
    from python.giza_three_pyramid_scaling import best_k5_fit_for_menkaure_ratio
    name, val, dev = best_k5_fit_for_menkaure_ratio()
    assert abs(dev) > 1.0
    assert abs(dev) < 5.0


# ---------------------------------------------------------------------------
# Architectural K=4 ↔ K=5 completion (Khafre+Menkaure supply the missing K=5)
# ---------------------------------------------------------------------------

def test_khufu_units_is_phi_4_at_K4():
    """Khufu's capacity-unit reference = Φ_4(K=4) = 17."""
    from python.giza_three_pyramid_scaling import khufu_capacity_units
    assert khufu_capacity_units() == 17.0


def test_menkaure_units_is_exactly_8():
    """Menkaure capacity = (8/17) × 17 = 8 exactly — equals SO vertex count."""
    from python.giza_three_pyramid_scaling import menkaure_capacity_units, SO_VERTICES
    cap = menkaure_capacity_units()
    assert abs(cap - SO_VERTICES) < 1e-12
    assert abs(cap - 8.0) < 1e-12


def test_khufu_plus_menkaure_is_K_squared_at_K5_exactly():
    """The architectural lock: Khufu + Menkaure = 17 + 8 = 25 = K²(K=5).
    INTEGER-EXACT (no measurement uncertainty — follows from 8/17 ratio)."""
    from python.giza_three_pyramid_scaling import khufu_plus_menkaure_capacity, K_GEOMETRY
    assert abs(khufu_plus_menkaure_capacity() - K_GEOMETRY ** 2) < 1e-12
    assert abs(khufu_plus_menkaure_capacity() - 25.0) < 1e-12


def test_khafre_capacity_near_K_squared_at_K4():
    """Khafre capacity ≈ K²(K=4) = 16, within 1%."""
    from python.giza_three_pyramid_scaling import khafre_capacity_units, K_ALGEBRA
    cap = khafre_capacity_units()
    expected = K_ALGEBRA ** 2  # 16
    deviation_pct = abs(cap - expected) / expected * 100.0
    assert deviation_pct < 1.0   # under 1%


def test_completion_identity_holds():
    """All three identities hold within stated tolerances."""
    from python.giza_three_pyramid_scaling import architectural_completion_holds
    assert architectural_completion_holds()


def test_completion_identity_returns_K4_plus_K5_squared():
    """The combined K-shell sum is 16 + 25 = 41."""
    from python.giza_three_pyramid_scaling import K4_K5_completion_identity
    r = K4_K5_completion_identity()
    assert r["K_squared_at_K4"] == 16
    assert r["K_squared_at_K5"] == 25
    assert r["K4_plus_K5_squared"] == 41
    # All three sum ≈ 41 within 1%
    assert abs(r["all_three_sum"] - 41.0) / 41.0 < 0.01


def test_menkaure_supplies_missing_K5_capacity():
    """The structural reading: Menkaure's 8 units = SO_v lift the K=4 squared
    base (16) to the K=5 squared base (25)."""
    from python.giza_three_pyramid_scaling import (
        menkaure_capacity_units, K_ALGEBRA, K_GEOMETRY,
    )
    lift = K_GEOMETRY ** 2 - K_ALGEBRA ** 2     # 25 - 16 = 9
    # Menkaure = 8, not 9 — but Menkaure joins Khufu's +17, not Khafre's +16
    # The actual identity:  Khufu(17) + Menkaure(8) = 25
    # which is equivalent to:  Khafre's-target(16) + 9 = 25 + 0 only if Khafre = 16
    # The +8 from Menkaure plus Khufu's K²(K=4)+1 = 17 yields K²(K=5) = 25
    assert menkaure_capacity_units() + 17 == 25


def test_showcase_has_completion_section():
    out = showcase_three_pyramid_scaling()
    text = "\n".join(out)
    assert "COMPLETION" in text
    assert "INTEGER EXACT" in text or "Integer-exact" in text or "INTEGER" in text.upper()
    assert "K²(K=5)" in text or "K²(K=5) = 25" in text
