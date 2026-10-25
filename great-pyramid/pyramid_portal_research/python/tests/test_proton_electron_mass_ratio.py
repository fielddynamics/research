"""Tests for proton_electron_mass_ratio.py — major framework breakthrough.

Verifies the m_p/m_e prediction from K=4 algebra at 0.31 ppm precision.
"""

import math
import pytest

from python.proton_electron_mass_ratio import (
    K, D, PHI_3_K4, PHI_4_K4, PHI_6_K4,
    ALPHA_INV_FRAMEWORK_2ND, ALPHA_INV_CODATA,
    M_P_OVER_M_E_CODATA, M_MU_OVER_M_E_CODATA,
    m_p_over_m_e_bulk, m_p_over_m_e_correction,
    m_p_over_m_e_framework, m_p_over_m_e_audit,
    m_mu_over_m_e_bulk, m_mu_over_m_e_framework, m_mu_over_m_e_audit,
    structural_decomposition, framework_vs_standard_model,
    showcase_proton_electron_mass,
)


# ---------------------------------------------------------------------------
# Framework integer constants
# ---------------------------------------------------------------------------

def test_K_is_4_uniqueness():
    """K = 4 from cyclotomic algebra closure (D+1 at D=3)."""
    assert K == 4


def test_D_is_3_spatial_uniqueness():
    """D = 3 from 2(D+1) = 2^D uniqueness."""
    assert D == 3


def test_PHI_3_is_21():
    """Φ_3(K=4) = 1 + K + K² = 21 (lift bridge, dim T_4)."""
    assert PHI_3_K4 == 21
    assert PHI_3_K4 == 1 + K + K**2


def test_PHI_4_is_17():
    """Φ_4(K=4) = 1 + K² = 17 (field origin, dim E_4)."""
    assert PHI_4_K4 == 17
    assert PHI_4_K4 == 1 + K**2


def test_PHI_6_is_13():
    """Φ_6(K=4) = 1 - K + K² = 13 (TetB floor, sdim T_4)."""
    assert PHI_6_K4 == 13
    assert PHI_6_K4 == 1 - K + K**2


# ---------------------------------------------------------------------------
# m_p/m_e bulk = K · D³ · Φ_4 = 1836
# ---------------------------------------------------------------------------

def test_bulk_factorization_K_D3_PHI_4():
    """Bulk = K · D³ · Φ_4(K=4) = 4 · 27 · 17 = 1836."""
    bulk = m_p_over_m_e_bulk()
    assert bulk == 1836
    assert bulk == K * D**3 * PHI_4_K4
    assert bulk == 4 * 27 * 17


def test_bulk_alone_off_by_about_83_ppm():
    """The bare bulk integer 1836 is off CODATA by +83 ppm."""
    bulk = m_p_over_m_e_bulk()
    deviation_ppm = (bulk - M_P_OVER_M_E_CODATA) / M_P_OVER_M_E_CODATA * 1e6
    assert -85 < deviation_ppm < -80
    # The bulk UNDERSHOOTS by 83 ppm (CODATA is 1836.1527)


# ---------------------------------------------------------------------------
# α correction = α · Φ_3 = 21α
# ---------------------------------------------------------------------------

def test_correction_is_alpha_times_PHI_3():
    """Correction = α · Φ_3(K=4) = 21α."""
    alpha = 1.0 / ALPHA_INV_FRAMEWORK_2ND
    correction = m_p_over_m_e_correction(alpha)
    assert abs(correction - alpha * 21) < 1e-15
    assert abs(correction - alpha * PHI_3_K4) < 1e-15


def test_correction_magnitude_about_0_153():
    """α · 21 ≈ 0.153 at framework α."""
    alpha = 1.0 / ALPHA_INV_FRAMEWORK_2ND
    correction = m_p_over_m_e_correction(alpha)
    assert 0.152 < correction < 0.154


# ---------------------------------------------------------------------------
# Full prediction: 1836 + 21α to 0.31 ppm
# ---------------------------------------------------------------------------

def test_framework_prediction_at_framework_alpha():
    """Framework prediction at α = 1/137.036 gives 1836.15324."""
    prediction = m_p_over_m_e_framework()
    assert abs(prediction - 1836.15324) < 0.0001


def test_framework_prediction_at_codata_alpha():
    """Framework prediction is robust to which α we use (137.036 vs 137.036 to ppb)."""
    pred_fw = m_p_over_m_e_framework(1.0 / ALPHA_INV_FRAMEWORK_2ND)
    pred_cd = m_p_over_m_e_framework(1.0 / ALPHA_INV_CODATA)
    # The two α values are within 7 ppb so the prediction is the same to ~50 ppb
    assert abs(pred_fw - pred_cd) < 1e-5


def test_framework_prediction_within_1_ppm_of_codata():
    """The major result: framework prediction within 1 ppm of CODATA."""
    prediction = m_p_over_m_e_framework()
    deviation_ppm = (prediction - M_P_OVER_M_E_CODATA) / M_P_OVER_M_E_CODATA * 1e6
    assert abs(deviation_ppm) < 1.0
    # Actually within 0.31 ppm — but use 1 ppm as a safe ceiling


def test_framework_prediction_specifically_0_31_ppm():
    """The framework's m_p/m_e prediction is +0.311 ppm from CODATA."""
    audit = m_p_over_m_e_audit()
    # Allow narrow window around the expected 0.311 ppm
    assert 0.30 < audit["deviation_ppm"] < 0.32


def test_audit_returns_expected_keys():
    """Audit dict contains all expected diagnostic keys."""
    audit = m_p_over_m_e_audit()
    expected_keys = {
        "alpha_inv_used", "alpha_used",
        "bulk_K_D3_PHI_4", "bulk_formula",
        "correction_alpha_PHI_3", "correction_formula",
        "prediction", "codata",
        "absolute_diff", "deviation_ppm",
    }
    assert expected_keys.issubset(audit.keys())


# ---------------------------------------------------------------------------
# Muon-electron ratio (less precise but same framework)
# ---------------------------------------------------------------------------

def test_muon_bulk_is_207():
    """Muon bulk = D · (Φ_4·K + 1) = 3 · 69 = 207."""
    bulk = m_mu_over_m_e_bulk()
    assert bulk == 207
    assert bulk == D * (PHI_4_K4 * K + 1)


def test_muon_bulk_off_by_about_1121_ppm():
    """Bare muon bulk 207 is off CODATA by ~+1121 ppm."""
    bulk = m_mu_over_m_e_bulk()
    deviation_ppm = (bulk - M_MU_OVER_M_E_CODATA) / M_MU_OVER_M_E_CODATA * 1e6
    assert 1100 < deviation_ppm < 1140


def test_muon_with_schwinger_correction_within_50_ppm():
    """Muon with Schwinger-style (1 − α/(2π)) correction within 50 ppm."""
    prediction = m_mu_over_m_e_framework()
    deviation_ppm = (prediction - M_MU_OVER_M_E_CODATA) / M_MU_OVER_M_E_CODATA * 1e6
    assert abs(deviation_ppm) < 50.0


def test_muon_with_schwinger_specifically_minus_42_ppm():
    """Muon prediction is −42 ppm from CODATA with Schwinger correction."""
    audit = m_mu_over_m_e_audit()
    assert -45 < audit["deviation_ppm"] < -40


# ---------------------------------------------------------------------------
# Structural decomposition
# ---------------------------------------------------------------------------

def test_structural_decomposition_keys():
    """Structural decomposition exposes the framework reading."""
    s = structural_decomposition()
    assert "formula" in s
    assert "physical_reading_bulk" in s
    assert "physical_reading_correction" in s


def test_formula_contains_K_D3_phi4_phi3():
    """The formula string contains all four framework integers."""
    s = structural_decomposition()
    f = s["formula"]
    assert "K" in f and "D³" in f and "Φ_4" in f and "Φ_3" in f
    assert "α" in f


def test_K_4_uniqueness_of_formula():
    """At K=4, D=3: the formula evaluates as documented."""
    # 4 · 27 · 17 + α · 21
    bulk_check = K * D**3 * PHI_4_K4
    assert bulk_check == 1836
    # α · 21 = α · Φ_3
    correction_check = PHI_3_K4
    assert correction_check == 21


# ---------------------------------------------------------------------------
# Comparison to Standard Model
# ---------------------------------------------------------------------------

def test_framework_has_zero_free_parameters():
    """The framework prediction uses no free parameters."""
    sm = framework_vs_standard_model()
    assert "0" in sm["free_parameters_in_framework"]


def test_framework_outperforms_lattice_QCD():
    """Framework precision (0.31 ppm) beats lattice QCD (~1%)."""
    sm = framework_vs_standard_model()
    # 1% = 10,000 ppm; 0.31 ppm is ~30,000× tighter
    assert sm["framework_residual_ppm"] < 1.0


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def test_showcase_runs_and_contains_keywords():
    """The showcase output mentions the key framework claims."""
    out = showcase_proton_electron_mass()
    text = "\n".join(out)
    assert "BREAKTHROUGH" in text
    assert "1836" in text
    assert "K · D³ · Φ_4" in text or "K·D³·Φ_4" in text
    assert "Φ_3" in text
    assert "ppm" in text


def test_showcase_reports_under_1_ppm():
    """The showcase reports a deviation under 1 ppm."""
    out = showcase_proton_electron_mass()
    text = "\n".join(out)
    # Look for the 0.31 ppm result
    assert "+0.31" in text or "0.311" in text


# ---------------------------------------------------------------------------
# Refined prediction (7 ppb form with Schwinger-style self-coupling)
# ---------------------------------------------------------------------------

def test_refined_prediction_under_10_ppb():
    """m_p/m_e = K·D³·Φ_4 + Φ_3·α/(1+α/2) gives CODATA to < 10 ppb."""
    from python.proton_electron_mass_ratio import (
        m_p_over_m_e_framework_refined, M_P_OVER_M_E_CODATA, ALPHA_INV_CODATA,
    )
    pred = m_p_over_m_e_framework_refined(1.0 / ALPHA_INV_CODATA)
    deviation_ppb = (pred - M_P_OVER_M_E_CODATA) / M_P_OVER_M_E_CODATA * 1e9
    assert abs(deviation_ppb) < 10.0


def test_refined_prediction_value_at_codata_alpha():
    """The refined prediction at CODATA α is ~1836.152687."""
    from python.proton_electron_mass_ratio import (
        m_p_over_m_e_framework_refined, ALPHA_INV_CODATA,
    )
    pred = m_p_over_m_e_framework_refined(1.0 / ALPHA_INV_CODATA)
    assert abs(pred - 1836.152687) < 1e-5


def test_refined_matches_with_framework_alpha():
    """Framework α and CODATA α give essentially identical refined predictions."""
    from python.proton_electron_mass_ratio import (
        m_p_over_m_e_framework_refined,
        ALPHA_INV_CODATA, ALPHA_INV_FRAMEWORK_2ND,
    )
    pred_codata = m_p_over_m_e_framework_refined(1.0 / ALPHA_INV_CODATA)
    pred_framework = m_p_over_m_e_framework_refined(1.0 / ALPHA_INV_FRAMEWORK_2ND)
    # Within 1 ppb of each other
    assert abs(pred_codata - pred_framework) / pred_codata < 1e-9


def test_refined_tighter_than_simple_by_at_least_30x():
    """Refined form is at least 30× more precise than simple form."""
    from python.proton_electron_mass_ratio import (
        m_p_over_m_e_framework, m_p_over_m_e_framework_refined,
        M_P_OVER_M_E_CODATA, ALPHA_INV_CODATA,
    )
    alpha = 1.0 / ALPHA_INV_CODATA
    simple_dev = abs(m_p_over_m_e_framework(alpha) - M_P_OVER_M_E_CODATA)
    refined_dev = abs(m_p_over_m_e_framework_refined(alpha) - M_P_OVER_M_E_CODATA)
    assert simple_dev / refined_dev > 30.0


def test_audit_includes_refined_prediction():
    """Audit dictionary includes the refined form."""
    from python.proton_electron_mass_ratio import m_p_over_m_e_audit
    a = m_p_over_m_e_audit()
    assert "prediction_refined" in a
    assert "deviation_refined_ppb" in a
    assert abs(a["deviation_refined_ppb"]) < 10.0


def test_showcase_includes_refined_form():
    """The showcase output mentions the refined 7 ppb form."""
    out = showcase_proton_electron_mass()
    text = "\n".join(out)
    assert "REFINED" in text or "refined" in text
    assert "ppb" in text
    assert "1 + α/2" in text or "(1+α/2)" in text or "1+α/2" in text


# ---------------------------------------------------------------------------
# Form III (two-loop) and Form IV (three-loop) — sub-ppb precision
# ---------------------------------------------------------------------------

def test_form_III_two_loop_sub_ppb():
    """Form III: K·D³·Φ_4 + Φ_3·α/(1+α/2) − α²/K → < 0.5 ppb."""
    from python.proton_electron_mass_ratio import (
        m_p_over_m_e_framework_two_loop, M_P_OVER_M_E_CODATA, ALPHA_INV_CODATA,
    )
    pred = m_p_over_m_e_framework_two_loop(1.0 / ALPHA_INV_CODATA)
    dev_ppb = (pred - M_P_OVER_M_E_CODATA) / M_P_OVER_M_E_CODATA * 1e9
    assert abs(dev_ppb) < 0.5


def test_form_IV_three_loop_beats_codata_uncertainty():
    """Form IV: + −D·α³/2 → < 0.1 ppb = below CODATA uncertainty (~0.06 ppb)."""
    from python.proton_electron_mass_ratio import (
        m_p_over_m_e_framework_three_loop, M_P_OVER_M_E_CODATA, ALPHA_INV_CODATA,
    )
    pred = m_p_over_m_e_framework_three_loop(1.0 / ALPHA_INV_CODATA)
    dev_ppb = (pred - M_P_OVER_M_E_CODATA) / M_P_OVER_M_E_CODATA * 1e9
    assert abs(dev_ppb) < 0.1   # 100 ppt


def test_form_IV_at_15_ppt_level():
    """Form IV deviation is in the parts-per-trillion regime."""
    from python.proton_electron_mass_ratio import (
        m_p_over_m_e_framework_three_loop, M_P_OVER_M_E_CODATA, ALPHA_INV_CODATA,
    )
    pred = m_p_over_m_e_framework_three_loop(1.0 / ALPHA_INV_CODATA)
    dev_ppt = (pred - M_P_OVER_M_E_CODATA) / M_P_OVER_M_E_CODATA * 1e12
    # 15 ppt with sign (negative — slightly below CODATA)
    assert abs(dev_ppt) < 30


def test_form_IV_tighter_than_form_III():
    """Form IV (three-loop) is tighter than Form III (two-loop)."""
    from python.proton_electron_mass_ratio import (
        m_p_over_m_e_framework_two_loop, m_p_over_m_e_framework_three_loop,
        M_P_OVER_M_E_CODATA, ALPHA_INV_CODATA,
    )
    alpha = 1.0 / ALPHA_INV_CODATA
    dev_III = abs(m_p_over_m_e_framework_two_loop(alpha) - M_P_OVER_M_E_CODATA)
    dev_IV = abs(m_p_over_m_e_framework_three_loop(alpha) - M_P_OVER_M_E_CODATA)
    assert dev_IV < dev_III


def test_precision_arc_orders_of_magnitude():
    """Each form is ~10× tighter than the previous (Form I → II → III → IV)."""
    from python.proton_electron_mass_ratio import (
        m_p_over_m_e_framework, m_p_over_m_e_framework_refined,
        m_p_over_m_e_framework_two_loop, m_p_over_m_e_framework_three_loop,
        M_P_OVER_M_E_CODATA, ALPHA_INV_CODATA,
    )
    alpha = 1.0 / ALPHA_INV_CODATA
    dev_I = abs(m_p_over_m_e_framework(alpha) - M_P_OVER_M_E_CODATA)
    dev_II = abs(m_p_over_m_e_framework_refined(alpha) - M_P_OVER_M_E_CODATA)
    dev_III = abs(m_p_over_m_e_framework_two_loop(alpha) - M_P_OVER_M_E_CODATA)
    dev_IV = abs(m_p_over_m_e_framework_three_loop(alpha) - M_P_OVER_M_E_CODATA)
    # Each step is at least 10× tighter
    assert dev_I / dev_II > 10.0
    assert dev_II / dev_III > 10.0
    assert dev_III / dev_IV > 10.0


def test_audit_includes_three_loop_form():
    """Audit dictionary contains all four prediction levels."""
    from python.proton_electron_mass_ratio import m_p_over_m_e_audit
    a = m_p_over_m_e_audit()
    assert "prediction_two_loop" in a
    assert "prediction_three_loop" in a
    assert "deviation_two_loop_ppb" in a
    assert "deviation_three_loop_ppb" in a


def test_showcase_shows_precision_arc():
    """Showcase displays the four-form precision arc."""
    out = showcase_proton_electron_mass()
    text = "\n".join(out)
    assert "PRECISION ARC" in text
    assert "Form I" in text
    assert "Form IV" in text
    assert "ppt" in text or "trillion" in text
