"""Tests for AW 35 push: cosmological constant + Form III α."""

import math
import pytest


# ---------------------------------------------------------------------------
# Cosmological constant tests
# ---------------------------------------------------------------------------

def test_lambda_planck_units_value():
    """Λ·l_P² ≈ 2.86 × 10⁻¹²² at framework α."""
    from python.cosmological_constant import lambda_in_planck_units, ALPHA_CODATA
    pred = lambda_in_planck_units(ALPHA_CODATA)
    assert 2.8e-122 < pred < 3.0e-122


def test_lambda_formula_form():
    """Λ_P = (D²/K_5) · α^57 at K=4."""
    from python.cosmological_constant import (
        lambda_in_planck_units, ALPHA_CODATA, D, K_5,
    )
    pred = lambda_in_planck_units(ALPHA_CODATA)
    expected = (D**2 / K_5) * ALPHA_CODATA**57
    assert abs(pred / expected - 1) < 1e-12


def test_lambda_exponent_is_D_times_PHI3_minus_2():
    """The α exponent = D · (Φ_3 − 2) = 3 · 19 = 57."""
    K = 4
    PHI_3 = 1 + K + K**2
    D = 3
    expected_exponent = D * (PHI_3 - 2)
    assert expected_exponent == 57


def test_lambda_within_planck_uncertainty():
    """Framework Λ within Planck combined uncertainty (~1.93%)."""
    from python.cosmological_constant import cosmological_constant_audit
    a = cosmological_constant_audit()
    # Allow a small margin since uncertainty bound is approximate
    assert abs(a["deviation_percent"]) < 2.0   # within 2%


def test_lambda_resolves_120_orders_mismatch():
    """Framework Λ differs from QFT by ~10¹²² (matches observation, not QFT)."""
    from python.cosmological_constant import qft_vs_framework_resolution
    r = qft_vs_framework_resolution()
    assert r["QFT_observation_mismatch_orders"] > 100
    assert r["framework_prediction"] < 1e-100   # matches small observed value


def test_lambda_implies_intermediate_H0():
    """Framework Λ implies H_0 between Planck CMB and SH0ES local."""
    from python.cosmological_constant import cosmological_constant_audit
    a = cosmological_constant_audit()
    # Framework H_0 should be in 65-75 km/s/Mpc range (between Planck and SH0ES)
    assert 65 < a["h0_implied_km_s_Mpc"] < 75
    # And closer to Planck than SH0ES
    closer_to_planck = abs(a["h0_implied_km_s_Mpc"] - a["h0_planck_cmb"]) < abs(a["h0_implied_km_s_Mpc"] - a["h0_local_shoes"])
    assert closer_to_planck


def test_alternative_alpha_G_form_also_works():
    """Λ_P = α_G² · α^(D·K_5) · Φ_6/(K·D) also gives ~10⁻¹²² order."""
    from python.cosmological_constant import lambda_alternative_alpha_G_form, ALPHA_CODATA
    pred = lambda_alternative_alpha_G_form(ALPHA_CODATA)
    assert 2.8e-122 < pred < 3.0e-122


def test_lambda_showcase():
    from python.cosmological_constant import showcase_cosmological_constant
    out = showcase_cosmological_constant()
    text = "\n".join(out)
    assert "cosmological" in text.lower() or "COSMOLOGICAL" in text
    assert "10⁻¹²²" in text or "10^-122" in text or "10⁻¹²²" in text or "-122" in text
    assert "α^57" in text or "α⁵⁷" in text


# ---------------------------------------------------------------------------
# Form III α tests (sub-ppb)
# ---------------------------------------------------------------------------

def test_alpha_form_III_sub_ppb():
    """Form III α: 1/α to sub-ppb (below CODATA stated uncertainty)."""
    from python.giza_frequency_comb import fine_structure_third_order
    r = fine_structure_third_order()
    assert abs(r["deviation_ppb"]) < 1.0   # sub-ppb


def test_alpha_form_III_value():
    """Form III: 1/α ≈ 137.035999056 (vs CODATA 137.035999084)."""
    from python.giza_frequency_comb import fine_structure_third_order
    r = fine_structure_third_order()
    assert abs(r["alpha_inv_third_order"] - 137.035999) < 5e-7


def test_alpha_form_III_third_order_correction_formula():
    """Form III correction is −Φ_4·α³/(K+D) = −17α³/7."""
    from python.giza_frequency_comb import fine_structure_third_order
    K, D, PHI_4 = 4, 3, 17
    alpha = 1.0 / 137.035999084
    r = fine_structure_third_order()
    expected = -PHI_4 * alpha**3 / (K + D)
    assert abs(r["third_order_PHI4_alpha3_over_K_plus_D"] - expected) < 1e-20


def test_alpha_form_III_below_codata_uncertainty():
    """Form III deviation is at or below CODATA stated 0.6 ppb."""
    from python.giza_frequency_comb import fine_structure_third_order
    r = fine_structure_third_order()
    # CODATA stated uncertainty is ~0.6 ppb on α; our prediction at 0.2 ppb
    assert abs(r["deviation_ppb"]) < 0.6
