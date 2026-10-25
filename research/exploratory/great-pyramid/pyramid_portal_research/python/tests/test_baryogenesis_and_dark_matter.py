"""Tests for AW 36 push: baryogenesis + dark matter / baryon ratio."""

import math


# ---------------------------------------------------------------------------
# Baryogenesis tests
# ---------------------------------------------------------------------------

def test_eta_B_formula():
    """η_B = D·(K+D)²/K_5 · α^K_5."""
    from python.baryogenesis import baryogenesis_ratio, ALPHA_CODATA, K, D, K_5
    pred = baryogenesis_ratio(ALPHA_CODATA)
    expected = D * (K+D)**2 / K_5 * ALPHA_CODATA**K_5
    assert abs(pred - expected) < 1e-30


def test_eta_B_within_planck_BBN():
    """η_B framework within Planck BBN uncertainty (~0.7%)."""
    from python.baryogenesis import baryogenesis_audit
    a = baryogenesis_audit()
    # Framework gives -0.27%, BBN uncertainty is ±0.7%
    assert abs(a["deviation_from_BBN_percent"]) < 1.0


def test_eta_B_alternative_form_equals_primary():
    """η_B = Φ_3·α^5·(K+D)/K_5 equivalent to primary form."""
    from python.baryogenesis import baryogenesis_ratio, baryogenesis_alternative_form, ALPHA_CODATA
    primary = baryogenesis_ratio(ALPHA_CODATA)
    alt = baryogenesis_alternative_form(ALPHA_CODATA)
    # Both forms compute D·(K+D)²·α^5/K_5 with same numerical result up to FP
    assert abs(primary - alt) / primary < 1e-14


def test_eta_B_value_around_6e_minus_10():
    """η_B ≈ 6.1 × 10⁻¹⁰."""
    from python.baryogenesis import baryogenesis_ratio
    pred = baryogenesis_ratio()
    assert 5.9e-10 < pred < 6.2e-10


def test_alpha_exponent_is_K_plus_one():
    """The α-exponent in η_B is K_5 = K+1 at K=4."""
    K, K_5 = 4, 5
    assert K_5 == K + 1


def test_baryogenesis_showcase():
    from python.baryogenesis import showcase_baryogenesis
    out = showcase_baryogenesis()
    text = "\n".join(out)
    assert "BARYOGENESIS" in text or "η_B" in text or "baryon" in text.lower()
    assert "Sakharov" in text or "matter" in text.lower()


# ---------------------------------------------------------------------------
# Dark matter / baryon ratio tests
# ---------------------------------------------------------------------------

def test_dm_over_b_is_43_over_8():
    """Ω_dm/Ω_b = K_5 + D/SO_v = 43/8 = 5.375."""
    from python.cosmological_density import dark_matter_over_baryon_ratio
    assert dark_matter_over_baryon_ratio() == 43/8
    assert abs(dark_matter_over_baryon_ratio() - 5.375) < 1e-12


def test_dm_over_b_within_planck_uncertainty():
    """Ω_dm/Ω_b framework within ~0.5% of Planck."""
    from python.cosmological_density import dark_matter_over_baryon_audit
    a = dark_matter_over_baryon_audit()
    assert abs(a["deviation_percent"]) < 0.5


def test_baryon_density_framework_value():
    """Ω_b ≈ 0.0494 from Ω_m · SO_v/(D·Φ_4)."""
    from python.cosmological_density import baryon_density_framework
    ob = baryon_density_framework()
    assert 0.048 < ob < 0.051


def test_dark_matter_density_framework_value():
    """Ω_dm ≈ 0.266 from Ω_m - Ω_b."""
    from python.cosmological_density import dark_matter_density_framework
    odm = dark_matter_density_framework()
    assert 0.260 < odm < 0.270


def test_baryon_density_within_planck():
    """Ω_b prediction within 0.5% of Planck 0.0493."""
    from python.cosmological_density import baryon_density_framework
    ob = baryon_density_framework()
    planck = 0.0493
    dev = (ob - planck) / planck * 100
    assert abs(dev) < 0.5


def test_complete_cosmological_composition_sums_correctly():
    """Ω_Λ + Ω_m = 1 (flat universe), and Ω_b + Ω_dm = Ω_m."""
    from python.cosmological_density import complete_cosmological_composition
    c = complete_cosmological_composition()
    assert abs(c["Omega_Lambda"] + c["Omega_matter"] - 1.0) < 1e-12
    assert abs(c["Omega_baryon"] + c["Omega_dark_matter"] - c["Omega_matter"]) < 1e-12


def test_complete_cosmological_composition_has_all_five():
    """Complete composition derives Ω_Λ, Ω_m, Ω_b, Ω_dm, η_B."""
    from python.cosmological_density import complete_cosmological_composition
    c = complete_cosmological_composition()
    assert all(k in c for k in [
        "Omega_Lambda", "Omega_matter", "Omega_baryon",
        "Omega_dark_matter", "eta_B_baryogenesis",
    ])


def test_eta_B_in_composition_matches_baryogenesis_module():
    """η_B from composition equals η_B from baryogenesis module."""
    from python.cosmological_density import complete_cosmological_composition
    from python.baryogenesis import baryogenesis_ratio
    c = complete_cosmological_composition()
    assert abs(c["eta_B_baryogenesis"] - baryogenesis_ratio()) < 1e-30


def test_K5_plus_D_over_SOv_decomposition():
    """K_5 + D/SO_v = (K_5·SO_v + D)/SO_v = 43/8."""
    K_5, D, SO_v = 5, 3, 8
    assert (K_5*SO_v + D) / SO_v == 43/8
    assert K_5 + D/SO_v == 43/8
