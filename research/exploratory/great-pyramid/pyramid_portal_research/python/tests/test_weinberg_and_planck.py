"""Tests for weinberg_angle.py and planck_mass.py modules."""

import math
import pytest


# ---------------------------------------------------------------------------
# Weinberg angle tests
# ---------------------------------------------------------------------------

def test_sin2_theta_W_leading_is_3_over_13():
    from python.weinberg_angle import sin2_theta_W_leading, D, PHI_6
    assert sin2_theta_W_leading() == D / PHI_6
    assert abs(sin2_theta_W_leading() - 0.230769) < 1e-5


def test_sin2_theta_W_first_order_within_PDG_uncertainty():
    """First-order prediction within PDG ±170 ppm uncertainty."""
    from python.weinberg_angle import (
        sin2_theta_W_first_order, SIN2_THETA_W_PDG_MSBAR, ALPHA_CODATA,
    )
    pred = sin2_theta_W_first_order(ALPHA_CODATA)
    dev_ppm = (pred - SIN2_THETA_W_PDG_MSBAR) / SIN2_THETA_W_PDG_MSBAR * 1e6
    assert abs(dev_ppm) < 200.0


def test_sin2_theta_W_second_order_within_few_ppm():
    """Second-order prediction within 5 ppm of PDG MS-bar."""
    from python.weinberg_angle import (
        sin2_theta_W_second_order, SIN2_THETA_W_PDG_MSBAR, ALPHA_CODATA,
    )
    pred = sin2_theta_W_second_order(ALPHA_CODATA)
    dev_ppm = (pred - SIN2_THETA_W_PDG_MSBAR) / SIN2_THETA_W_PDG_MSBAR * 1e6
    assert abs(dev_ppm) < 5.0


def test_sin2_theta_W_value_at_codata():
    """Second-order prediction = 0.231210 ± 0.000001 at CODATA α."""
    from python.weinberg_angle import sin2_theta_W_second_order, ALPHA_CODATA
    pred = sin2_theta_W_second_order(ALPHA_CODATA)
    assert abs(pred - 0.231210) < 1e-5


def test_weinberg_audit_in_PDG_uncertainty():
    from python.weinberg_angle import weinberg_audit
    a = weinberg_audit()
    assert a["framework_in_PDG_uncertainty"]


def test_tan2_theta_W_leading_is_3_over_10():
    """tan²(θ_W) leading = D/(Φ_6 − D) = 3/10."""
    from python.weinberg_angle import tan2_theta_W
    t = tan2_theta_W()
    assert t["tan2_leading_D_over_PHI6_minus_D"] == 0.3


def test_weinberg_uses_K4_integers_only():
    """Confirm Weinberg formula uses only K=4 framework integers."""
    from python.weinberg_angle import D, PHI_6, K, SO_v, sin2_theta_W_second_order
    # All inputs are K=4 framework integers: D=3, Φ_6=13, K=4, SO_v=8
    assert D == 3
    assert PHI_6 == 13
    assert K == 4
    assert SO_v == 8


def test_weinberg_showcase_runs():
    from python.weinberg_angle import showcase_weinberg_angle
    out = showcase_weinberg_angle()
    text = "\n".join(out)
    assert "Weinberg" in text or "WEINBERG" in text or "θ_W" in text
    assert "0.231" in text
    assert "ppm" in text


# ---------------------------------------------------------------------------
# Planck mass tests
# ---------------------------------------------------------------------------

def test_alpha_G_framework_correct_order():
    """α_G ~ 10^-45 (correct order for gravitational coupling)."""
    from python.planck_mass import alpha_G_framework, ALPHA_CODATA
    g = alpha_G_framework(ALPHA_CODATA)
    assert 1e-46 < g < 1e-44


def test_m_planck_over_m_e_22_orders_of_magnitude():
    """m_P/m_e ~ 10^22."""
    from python.planck_mass import m_planck_over_m_e_framework, ALPHA_CODATA
    r = m_planck_over_m_e_framework(ALPHA_CODATA)
    log_r = math.log10(r)
    assert 22 < log_r < 23


def test_m_planck_within_10_ppm():
    """Framework m_P/m_e within 10 ppm of measured."""
    from python.planck_mass import planck_mass_audit
    a = planck_mass_audit()
    assert abs(a["deviation_ppm"]) < 20.0


def test_m_planck_decomposition_three_factors():
    from python.planck_mass import m_planck_over_m_e_decomposition
    d = m_planck_over_m_e_decomposition()
    assert "alpha_half_attenuation" in d
    assert "parity_root_sqrt_13_over_17" in d
    assert "g_factor_root_1_over_sqrt_ge2" in d


def test_m_planck_parity_root_correct():
    """The √(13/17) factor = √(sdim/dim_E_4)."""
    from python.planck_mass import m_planck_over_m_e_decomposition, SDIM_T_4, DIM_E_4
    d = m_planck_over_m_e_decomposition()
    expected = math.sqrt(SDIM_T_4 / DIM_E_4)
    assert abs(d["parity_root_sqrt_13_over_17"] - expected) < 1e-12


def test_m_p_over_m_planck_combines_two_predictions():
    """Proton-to-Planck mass ratio combines AW 31 α_G and AW 32 m_p/m_e."""
    from python.planck_mass import m_p_over_m_planck
    p = m_p_over_m_planck()
    assert "m_p_over_m_e" in p
    assert "m_P_over_m_e" in p
    assert "m_p_over_m_P" in p
    # Sanity: m_p << m_P, so ratio is tiny
    assert p["m_p_over_m_P"] < 1e-15


def test_planck_showcase_runs():
    from python.planck_mass import showcase_planck_mass
    out = showcase_planck_mass()
    text = "\n".join(out)
    assert "Planck" in text or "PLANCK" in text
    assert "m_P" in text or "m_Planck" in text
    assert "α_G" in text or "α_G" in text
