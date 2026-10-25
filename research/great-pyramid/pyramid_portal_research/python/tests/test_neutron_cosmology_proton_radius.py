"""Tests for AW 34 push: neutron, dark energy, proton radius."""

import math
import pytest


# ---------------------------------------------------------------------------
# Neutron-proton mass tests
# ---------------------------------------------------------------------------

def test_neutron_proton_diff_formula():
    """(m_n − m_p)/m_e = K_5/2 + α·Φ_4/K."""
    from python.neutron_proton_mass import (
        neutron_proton_mass_diff_over_me, ALPHA_CODATA, K, K_5, PHI_4,
    )
    pred = neutron_proton_mass_diff_over_me(ALPHA_CODATA)
    expected = K_5/2 + ALPHA_CODATA * PHI_4/K
    assert abs(pred - expected) < 1e-15


def test_neutron_proton_diff_within_15_ppm():
    """(m_n − m_p)/m_e prediction within 15 ppm of CODATA."""
    from python.neutron_proton_mass import (
        neutron_proton_mass_diff_audit, ALPHA_CODATA,
    )
    a = neutron_proton_mass_diff_audit(ALPHA_CODATA)
    assert abs(a["deviation_ppm"]) < 15.0


def test_m_n_over_m_e_chained_to_20_ppb():
    """Chained m_n/m_e prediction (Form IV + neutron diff) within 20 ppb."""
    from python.neutron_proton_mass import neutron_electron_audit
    n = neutron_electron_audit()
    assert abs(n["deviation_ppb"]) < 20.0


def test_neutron_proton_showcase():
    from python.neutron_proton_mass import showcase_neutron_proton
    out = showcase_neutron_proton()
    text = "\n".join(out)
    assert "NEUTRON" in text or "neutron" in text
    assert "K_5/2" in text or "5/2" in text
    assert "ppm" in text


# ---------------------------------------------------------------------------
# Cosmological density tests
# ---------------------------------------------------------------------------

def test_omega_lambda_leading_is_17_over_25():
    """Leading Ω_Λ = Φ_4/K_5² = 17/25 = 0.68."""
    from python.cosmological_density import omega_lambda_leading
    assert omega_lambda_leading() == 17/25
    assert abs(omega_lambda_leading() - 0.68) < 1e-12


def test_omega_lambda_framework_within_planck_uncertainty():
    """Ω_Λ framework prediction within Planck 1σ uncertainty."""
    from python.cosmological_density import cosmological_audit
    a = cosmological_audit()
    assert a["omega_lambda_within_planck_uncertainty"]


def test_omega_lambda_value_at_codata_alpha():
    """Ω_Λ ≈ 0.685 at CODATA α."""
    from python.cosmological_density import omega_lambda_framework, ALPHA_CODATA
    pred = omega_lambda_framework(ALPHA_CODATA)
    assert abs(pred - 0.685) < 1e-3


def test_omega_m_complements_omega_lambda():
    """Ω_m + Ω_Λ = 1 (flat universe)."""
    from python.cosmological_density import (
        omega_lambda_framework, omega_matter_framework,
    )
    om_L = omega_lambda_framework()
    om_m = omega_matter_framework()
    assert abs(om_L + om_m - 1.0) < 1e-12


def test_baryon_fraction_framework_approximation():
    """Ω_b/Ω_m ≈ Φ_3·α = 21α ≈ 0.153 (within 5% of Planck)."""
    from python.cosmological_density import baryon_fraction_of_matter
    b = baryon_fraction_of_matter()
    assert abs(b["deviation_percent"]) < 5.0


def test_cosmological_showcase():
    from python.cosmological_density import showcase_cosmological_density
    out = showcase_cosmological_density()
    text = "\n".join(out)
    assert "Ω_Λ" in text or "Omega" in text or "dark energy" in text.lower()
    assert "Planck" in text
    assert "K_5" in text or "chamber" in text.lower()


# ---------------------------------------------------------------------------
# Proton radius tests
# ---------------------------------------------------------------------------

def test_proton_compton_wavelength_value():
    """λ_C_bar(p) ≈ 2.103 × 10⁻¹⁶ m."""
    from python.proton_radius import proton_compton_wavelength
    lam = proton_compton_wavelength()
    assert 2.10e-16 < lam < 2.11e-16


def test_proton_radius_framework_equals_K_times_compton():
    """r_p = K · λ_C_bar(p) at K=4."""
    from python.proton_radius import (
        proton_charge_radius_framework, proton_compton_wavelength, K,
    )
    r_p = proton_charge_radius_framework()
    expected = K * proton_compton_wavelength()
    assert abs(r_p - expected) < 1e-25


def test_proton_radius_in_fm_within_codata_uncertainty():
    """Framework r_p within CODATA uncertainty (~2300 ppm)."""
    from python.proton_radius import proton_radius_audit
    a = proton_radius_audit()
    assert a["within_codata_uncertainty"]
    assert abs(a["deviation_ppm"]) < 2300


def test_proton_radius_around_0p84_fm():
    """Framework r_p ≈ 0.841 fm."""
    from python.proton_radius import proton_radius_audit
    a = proton_radius_audit()
    assert 0.835 < a["framework_prediction_fm"] < 0.845


def test_proton_radius_in_electron_compton_approx():
    """r_p / λ_C_bar(e) ≈ K/(K·D³·Φ_4) = 1/(D³·Φ_4) = 1/459."""
    from python.proton_radius import proton_radius_in_electron_compton, K, PHI_4
    D = 3
    r = proton_radius_in_electron_compton()
    expected_leading = 1.0 / (D**3 * PHI_4)
    assert abs(r["value_1_over_DcubedPHI4"] - expected_leading) < 1e-12


def test_proton_radius_showcase():
    from python.proton_radius import showcase_proton_radius
    out = showcase_proton_radius()
    text = "\n".join(out)
    assert "r_p" in text or "PROTON" in text
    assert "λ_C" in text or "Compton" in text
    assert "K" in text
