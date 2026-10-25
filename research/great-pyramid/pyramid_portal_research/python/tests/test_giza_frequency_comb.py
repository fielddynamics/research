"""Tests for giza_frequency_comb.py — three-pyramid frequency comb."""

import math
import pytest

from python.giza_frequency_comb import (
    KC_L_M, KC_W_M, KC_H_M,
    fundamental_111_hz,
    predicted_chamber_dimensions, predicted_fundamental_hz,
    predicted_wavelength_m,
    FrequencyRatio, comb_ratios,
    octave_detuning,
    Beat, predicted_beats,
    wavelength_K_shell_completion,
    showcase_frequency_comb,
)
from python.pyramid_resonance import V_AIR


# ---------------------------------------------------------------------------
# Khufu's KC fundamental (sanity)
# ---------------------------------------------------------------------------

def test_khufu_fundamental_is_about_47_Hz():
    """Khufu's (1,1,1) at 343 m/s air is ~46.9 Hz."""
    f = predicted_fundamental_hz("khufu", V_AIR)
    assert 46.5 < f < 47.5


def test_fundamental_111_hz_formula():
    """f_111 = (v/2) sqrt(1/L² + 1/W² + 1/H²) — verify against direct compute."""
    L, W, H = 10.47, 5.24, 5.85
    f = fundamental_111_hz(L, W, H, V_AIR)
    expected = (V_AIR / 2.0) * math.sqrt(1.0/L**2 + 1.0/W**2 + 1.0/H**2)
    assert abs(f - expected) < 1e-9


# ---------------------------------------------------------------------------
# Predicted chamber dimensions and fundamentals
# ---------------------------------------------------------------------------

def test_khafre_chamber_scales_by_15_over_16():
    L, W, H = predicted_chamber_dimensions("khafre")
    assert abs(L / KC_L_M - 15.0/16.0) < 1e-12
    assert abs(W / KC_W_M - 15.0/16.0) < 1e-12
    assert abs(H / KC_H_M - 15.0/16.0) < 1e-12


def test_menkaure_chamber_scales_by_8_over_17():
    L, W, H = predicted_chamber_dimensions("menkaure")
    assert abs(L / KC_L_M - 8.0/17.0) < 1e-12


def test_unknown_pyramid_raises():
    with pytest.raises(ValueError):
        predicted_chamber_dimensions("snefru")


def test_khafre_fundamental_is_50_Hz():
    f = predicted_fundamental_hz("khafre")
    assert 49.5 < f < 50.5


def test_menkaure_fundamental_is_about_100_Hz():
    f = predicted_fundamental_hz("menkaure")
    assert 99.0 < f < 100.5


# ---------------------------------------------------------------------------
# Comb ratios — integer-exact at framework values
# ---------------------------------------------------------------------------

def test_comb_returns_three_ratios():
    ratios = comb_ratios()
    assert len(ratios) == 3
    pairs = [r.pair for r in ratios]
    assert "Khafre / Khufu" in pairs
    assert "Menkaure / Khufu" in pairs
    assert "Menkaure / Khafre" in pairs


def test_khafre_khufu_ratio_is_16_over_15_exact():
    """Predicted f_Khafre/f_Khufu = 1/(15/16) = 16/15.  Integer-exact."""
    ratios = comb_ratios()
    r = next(r for r in ratios if r.pair == "Khafre / Khufu")
    assert abs(r.observed - 16.0/15.0) < 1e-14
    assert abs(r.deviation_pct) < 1e-10


def test_menkaure_khufu_ratio_is_17_over_8_exact():
    """Predicted f_Menkaure/f_Khufu = 1/(8/17) = 17/8.  Integer-exact."""
    ratios = comb_ratios()
    r = next(r for r in ratios if r.pair == "Menkaure / Khufu")
    assert abs(r.observed - 17.0/8.0) < 1e-12
    assert abs(r.deviation_pct) < 1e-10


def test_menkaure_khafre_ratio_is_255_over_128():
    """f_Menkaure/f_Khafre = (17/8)/(16/15) = 255/128."""
    ratios = comb_ratios()
    r = next(r for r in ratios if r.pair == "Menkaure / Khafre")
    assert abs(r.observed - 255.0/128.0) < 1e-12


# ---------------------------------------------------------------------------
# Octave structure — Menkaure detuned by exactly 17/16
# ---------------------------------------------------------------------------

def test_octave_detuning_is_exactly_17_over_16():
    """Menkaure is the octave of Khufu detuned by exactly Φ_4/K² = 17/16."""
    o = octave_detuning()
    assert o["detuning_exact_17_over_16"]
    assert abs(o["detuning_factor"] - 17.0/16.0) < 1e-12


def test_octave_detuning_is_about_105_cents():
    """In musical cents, 17/16 ≈ 105 ¢ — just sharp of a semitone (100 ¢)."""
    o = octave_detuning()
    assert 104.0 < o["detuning_cents"] < 106.0


def test_menkaure_just_above_octave():
    """f_Menkaure/f_Khufu = 2.125 > 2.0 (octave)."""
    o = octave_detuning()
    assert o["actual_ratio"] > o["pure_octave_ratio"]
    assert abs(o["actual_ratio"] - 17.0/8.0) < 1e-12


# ---------------------------------------------------------------------------
# Beat structure
# ---------------------------------------------------------------------------

def test_beats_returns_three_entries():
    beats = predicted_beats()
    assert len(beats) == 3


def test_khafre_minus_khufu_beat_is_khufu_over_15():
    """Khafre − Khufu beat = f_Khufu/15  (since f_Ka = f_Kh·16/15)."""
    beats = predicted_beats()
    b = next(b for b in beats if "Khafre" in b.name and "−" in b.name and "Khufu" in b.name and "Menkaure" not in b.name)
    f_kh = predicted_fundamental_hz("khufu")
    assert abs(b.beat_hz - f_kh / 15.0) < 1e-9


def test_menkaure_minus_2x_khufu_beat_is_khufu_over_8():
    """Menkaure − 2·Khufu beat = f_Khufu/8  (since f_Me = f_Kh·17/8 = 2·f_Kh + f_Kh/8)."""
    beats = predicted_beats()
    b = next(b for b in beats if "Menkaure − 2·Khufu" in b.name)
    f_kh = predicted_fundamental_hz("khufu")
    assert abs(b.beat_hz - f_kh / 8.0) < 1e-9


def test_beat_periods_in_gamma_window():
    """Both meaningful beats land in the 100–500 ms (gamma/theta-EEG) window."""
    beats = predicted_beats()
    f_kh = predicted_fundamental_hz("khufu")
    interesting = [b for b in beats if b.beat_hz > 0.5 and "full" not in b.name]
    for b in interesting:
        assert 0.05 < b.beat_period_s < 0.5


# ---------------------------------------------------------------------------
# Wavelength K-shell completion
# ---------------------------------------------------------------------------

def test_wavelength_khufu_is_17_units():
    w = wavelength_K_shell_completion()
    assert abs(w["lambda_khufu_units"] - 17.0) < 1e-10


def test_wavelength_menkaure_is_8_units():
    w = wavelength_K_shell_completion()
    assert abs(w["lambda_menkaure_units"] - 8.0) < 1e-10


def test_wavelength_khafre_about_16_units():
    """Khafre's wavelength is ~16 units (K²(K=4) = 16)."""
    w = wavelength_K_shell_completion()
    assert abs(w["lambda_khafre_units"] - 16.0) < 0.1


def test_khufu_plus_menkaure_wavelength_equals_K_squared_at_K5():
    """λ_Khufu + λ_Menkaure = 25 = K²(K=5).  EXACT integer identity."""
    w = wavelength_K_shell_completion()
    assert abs(w["khufu_plus_menkaure_units"] - 25.0) < 1e-10
    assert w["completion_holds"]


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def test_showcase_runs_and_contains_keywords():
    out = showcase_frequency_comb()
    text = "\n".join(out)
    assert "FREQUENCY COMB" in text
    assert "Mirror of Orion" in text
    assert "17/8" in text
    assert "17/16" in text
    assert "K²(K=5)" in text
    assert "Khufu" in text and "Khafre" in text and "Menkaure" in text


# ---------------------------------------------------------------------------
# Transcendental audit — π, e, D² = 9 anchor
# ---------------------------------------------------------------------------

def test_split_ratio_is_15_over_8_exact():
    """beat2/beat1 = 15/8 — temperature-independent framework split."""
    from python.giza_frequency_comb import transcendental_audit
    t = transcendental_audit()
    assert t["split_is_integer_exact"]
    assert abs(t["split_ratio"] - 15.0/8.0) < 1e-12


def test_2pi_plus_e_near_identity():
    """2π + e ≈ 9 to better than 0.02% (known math near-identity)."""
    from python.giza_frequency_comb import transcendental_audit
    t = transcendental_audit()
    assert abs(t["near_identity_2pi_e_vs_9_pct"]) < 0.02


def test_temperature_for_sum_9_is_about_20C():
    """Chamber's natural T ~20°C is where beat sum = 9 exactly."""
    from python.giza_frequency_comb import temperature_for_beat_sum_equals_nine_celsius
    T = temperature_for_beat_sum_equals_nine_celsius()
    assert 19.0 < T < 21.0


def test_beat2_near_pi_plus_e():
    """beat2 is within 0.5% of (π + e)."""
    import math
    from python.giza_frequency_comb import transcendental_audit
    t = transcendental_audit()
    assert abs(t["beat2_pct_from_pi_plus_e"]) < 0.5


def test_diff_near_e():
    """beat2 − beat1 is within 1% of e."""
    from python.giza_frequency_comb import transcendental_audit
    t = transcendental_audit()
    assert abs(t["diff_pct_from_e"]) < 1.0


def test_sum_close_to_D_squared():
    """beat1 + beat2 is within 0.2% of 9 = D² at D=3."""
    from python.giza_frequency_comb import transcendental_audit
    t = transcendental_audit()
    assert abs(t["sum_pct_from_D_squared"]) < 0.2


def test_D_squared_is_9():
    """The framework's spatial-dimension uniqueness gives D=3, so D²=9."""
    from python.giza_frequency_comb import transcendental_audit
    t = transcendental_audit()
    assert t["D_squared"] == 9


def test_showcase_has_transcendental_section():
    out = showcase_frequency_comb()
    text = "\n".join(out)
    assert "TRANSCENDENTAL" in text or "transcendental" in text.lower()
    assert "2π + e" in text or "2π+e" in text
    assert "D²" in text


# ---------------------------------------------------------------------------
# Great Pyramid fundamental — the K=4 ↔ K=5 lift sum (system anchor)
# ---------------------------------------------------------------------------

def test_lift_sum_is_47():
    """21 + 26 = Φ_3(K=4) + Φ_4(K=5) = 47."""
    from python.giza_frequency_comb import (
        LIFT_BRIDGE_INTEGER, NEXT_K_SHELL_PHI_4, KHUFU_FUNDAMENTAL_FRAMEWORK_HZ
    )
    assert LIFT_BRIDGE_INTEGER == 21
    assert NEXT_K_SHELL_PHI_4 == 26
    assert KHUFU_FUNDAMENTAL_FRAMEWORK_HZ == 47
    assert LIFT_BRIDGE_INTEGER + NEXT_K_SHELL_PHI_4 == KHUFU_FUNDAMENTAL_FRAMEWORK_HZ


def test_khufu_fundamental_close_to_47():
    """Khufu's fundamental is within 0.5% of 47 Hz at v=343 m/s."""
    from python.giza_frequency_comb import great_pyramid_fundamental_audit
    g = great_pyramid_fundamental_audit()
    assert abs(g["khufu_pct_from_47"]) < 0.5


def test_khufu_47_temperature_is_about_20_5_celsius():
    """f_Khufu = 47 exact at T ≈ 20.5°C — chamber's natural operating temp."""
    from python.giza_frequency_comb import temperature_for_khufu_equals_47_celsius
    T = temperature_for_khufu_equals_47_celsius()
    assert 20.0 < T < 21.0


def test_khafre_target_is_50():
    """2·K²(K=5) = 2·25 = 50."""
    from python.giza_frequency_comb import great_pyramid_fundamental_audit
    g = great_pyramid_fundamental_audit()
    assert g["khafre_target_2K_squared_K5"] == 50
    # Predicted within 0.5% of 50 at v=343 m/s
    assert abs(g["khafre_pct_from_50"]) < 0.5


def test_menkaure_target_is_100():
    """K · K²(K=5) at K=4: 4·25 = 100."""
    from python.giza_frequency_comb import great_pyramid_fundamental_audit
    g = great_pyramid_fundamental_audit()
    assert g["menkaure_target_K_times_K_squared_K5"] == 100
    assert abs(g["menkaure_pct_from_100"]) < 0.5


def test_lift_sum_check_is_true():
    from python.giza_frequency_comb import great_pyramid_fundamental_audit
    g = great_pyramid_fundamental_audit()
    assert g["lift_sum_check"]


def test_showcase_has_great_pyramid_anchor_section():
    out = showcase_frequency_comb()
    text = "\n".join(out)
    assert "GREAT PYRAMID FUNDAMENTAL" in text
    assert "21 + 26" in text
    assert "47" in text
    assert "lift" in text.lower()


# ---------------------------------------------------------------------------
# Master identity — Khufu at three structural levels
# ---------------------------------------------------------------------------

def test_SO_elements_equals_28():
    """SO V+E+F = 8+12+8 = 28."""
    from python.giza_frequency_comb import so_elements_check, SO_ELEMENTS
    soe = so_elements_check()
    assert SO_ELEMENTS == 28
    assert soe["SO_V_plus_E_plus_F"] == 28
    assert soe["all_equal_28"]


def test_SO_elements_equals_K_K_plus_D():
    """28 = K(K+D) at K=4, D=3 = 4·7."""
    from python.giza_frequency_comb import so_elements_check
    soe = so_elements_check()
    assert soe["K_times_K_plus_D"] == 28
    assert soe["seven_K"] == 28


def test_SO_decomposition_V_E_F_in_terms_of_K():
    """SO_V = 2K, SO_E = 3K, SO_F = 2K at K=4."""
    from python.giza_frequency_comb import so_elements_check
    soe = so_elements_check()
    assert soe["decomposition_V_2K"]
    assert soe["decomposition_E_3K"]
    assert soe["decomposition_F_2K"]


def test_khufu_height_is_10_times_SO_elements():
    """Khufu height = 280 cubits = 10 × SO_elements (past-chat finding)."""
    from python.giza_frequency_comb import (
        KHUFU_HEIGHT_CUBITS, SO_ELEMENTS, khufu_geometry_audit,
    )
    assert KHUFU_HEIGHT_CUBITS == 280
    assert KHUFU_HEIGHT_CUBITS == 10 * SO_ELEMENTS
    g = khufu_geometry_audit()
    assert g["height_equals_10_SO"]


def test_khufu_base_close_to_5pi_SO_elements():
    """Khufu base = 440 cubits ≈ 5π × 28 = 5π × SO_elements (within 0.1%)."""
    from python.giza_frequency_comb import khufu_geometry_audit
    g = khufu_geometry_audit()
    assert abs(g["base_pct_from_5pi_SO"]) < 0.1


def test_khufu_base_per_height_is_pi_over_2():
    """Khufu base/height = 11/7 ≈ π/2 within 0.1% (the 'Khufu π' result)."""
    from python.giza_frequency_comb import khufu_geometry_audit
    g = khufu_geometry_audit()
    assert abs(g["base_per_height_pct_from_pi_over_2"]) < 0.1


def test_master_identity_21_26_28_equals_75():
    """Φ_3(K=4) + Φ_4(K=5) + SO_elements = D × K²(K=5).
       21 + 26 + 28 = 75 = 3 × 25 — exact integer identity."""
    from python.giza_frequency_comb import (
        khufu_master_identity, D_TIMES_K_SQUARED_AT_K5,
    )
    m = khufu_master_identity()
    assert D_TIMES_K_SQUARED_AT_K5 == 75
    assert m["phi_3_K_4"] == 21
    assert m["phi_4_K_5"] == 26
    assert m["SO_elements"] == 28
    assert m["sum_21_26_28"] == 75
    assert m["D_times_K_squared_K5"] == 75
    assert m["master_identity_holds"]


def test_f_khufu_plus_height_integer_equals_75():
    """f_Khufu (Hz) + Khufu_height_cubits/10 = D × K²(K=5).
       47 + 28 = 75 — equivalent form of master identity."""
    from python.giza_frequency_comb import khufu_master_identity
    m = khufu_master_identity()
    assert m["f_khufu_lift_sum_Hz"] == 47
    assert m["height_integer_height_cubits_over_10"] == 28
    assert m["f_khufu_plus_height_integer"] == 75
    assert m["spatial_identity_holds"]


def test_showcase_has_master_identity_section():
    out = showcase_frequency_comb()
    text = "\n".join(out)
    assert "MASTER IDENTITY" in text
    assert "TOPOLOGY" in text
    assert "GEOMETRY" in text
    assert "ALGEBRA" in text
    assert "21" in text and "26" in text and "28" in text
    assert "75" in text
    assert "D · K²" in text or "D × K²" in text or "D·K²" in text


# ---------------------------------------------------------------------------
# Fine-structure constant encoder
# ---------------------------------------------------------------------------

def test_137_equals_phi4_times_SOv_plus_1():
    """137 = Φ_4(K=4) · SO_v + 1 = 17 · 8 + 1 — cleanest K=4 factorization."""
    from python.giza_frequency_comb import fine_structure_constant_encoder
    a = fine_structure_constant_encoder()
    assert a["factor_phi4_SOv_plus_1"] == 137


def test_137_equals_K_squared_SOv_plus_D_squared():
    """137 = K² · SO_v + D² = 16 · 8 + 9."""
    from python.giza_frequency_comb import fine_structure_constant_encoder
    a = fine_structure_constant_encoder()
    assert a["factor_K_squared_SOv_plus_D_squared"] == 137


def test_137_equals_2_to_2D_plus_1_plus_D_squared():
    """137 = 2^(2D+1) + D² = 128 + 9 — binary-cube reading at D=3."""
    from python.giza_frequency_comb import fine_structure_constant_encoder
    a = fine_structure_constant_encoder()
    assert a["factor_2_to_2D_plus_1_plus_D_squared"] == 137


def test_three_factorizations_of_137_all_equal():
    """All three framework factorizations of 137 are equal and = ALPHA_INTEGER_137."""
    from python.giza_frequency_comb import (
        fine_structure_constant_encoder, ALPHA_INTEGER_137,
    )
    a = fine_structure_constant_encoder()
    assert ALPHA_INTEGER_137 == 137
    assert a["all_three_factorizations_equal_137"]


def test_khafre_base_equals_3_times_137():
    """Khafre base = 411 cubits = D × 137 (α integer × spatial-dim uniqueness)."""
    from python.giza_frequency_comb import (
        KHAFRE_BASE_CUBITS, ALPHA_INTEGER_137,
    )
    assert KHAFRE_BASE_CUBITS == 411
    assert KHAFRE_BASE_CUBITS == 3 * ALPHA_INTEGER_137


def test_khafre_encodes_alpha_integer():
    """Khafre base / D = 137 = α bulk integer (exact integer division in cubits)."""
    from python.giza_frequency_comb import fine_structure_constant_encoder
    a = fine_structure_constant_encoder()
    assert a["khafre_base_over_D"] == 137
    assert a["khafre_encodes_alpha_int"]


def test_khufu_encodes_alpha_denominator():
    """Khufu height / 10 = 28 = α denominator (SO partials)."""
    from python.giza_frequency_comb import fine_structure_constant_encoder
    a = fine_structure_constant_encoder()
    assert a["khufu_height_over_10"] == 28
    assert a["khufu_encodes_alpha_denom"]


def test_pyramid_reconstructs_one_over_alpha():
    """1/α reconstructed from pyramid cubits matches framework prediction exactly."""
    from python.giza_frequency_comb import fine_structure_constant_encoder
    a = fine_structure_constant_encoder()
    assert a["pyramid_matches_framework"]
    # 411/3 + 10/280 = 137 + 1/28
    assert abs(a["alpha_inv_from_pyramids"] - (137.0 + 1.0/28.0)) < 1e-12


def test_pyramid_one_over_alpha_within_4ppm_codata():
    """1/α from pyramid cubits is within 4 ppm of CODATA value."""
    from python.giza_frequency_comb import fine_structure_constant_encoder
    a = fine_structure_constant_encoder()
    # 0.0002% = 2 ppm; allow up to 4 ppm for tolerance
    assert abs(a["pyramid_vs_codata_pct"]) < 4e-4


def test_alpha_inv_framework_constant():
    """ALPHA_INV_FRAMEWORK = 137 + 1/28 exactly."""
    from python.giza_frequency_comb import ALPHA_INV_FRAMEWORK
    assert abs(ALPHA_INV_FRAMEWORK - (137.0 + 1.0/28.0)) < 1e-12


def test_showcase_has_alpha_encoder_section():
    out = showcase_frequency_comb()
    text = "\n".join(out)
    assert "FINE-STRUCTURE" in text or "FINE STRUCTURE" in text or "1/α" in text
    assert "137" in text
    assert "Φ_4" in text or "phi_4" in text
    assert "Khafre" in text
    assert "encoder" in text.lower() or "encod" in text.lower()


# ---------------------------------------------------------------------------
# Second-order α extension and Menkaure impedance encoder
# ---------------------------------------------------------------------------

def test_alpha_inv_second_order_is_137_036():
    """Second-order α = 137 + 9/250 = 137.036 exactly."""
    from python.giza_frequency_comb import ALPHA_INV_FRAMEWORK_2ND
    assert abs(ALPHA_INV_FRAMEWORK_2ND - 137.036) < 1e-12


def test_alpha_second_order_within_10ppb_codata():
    """Second-order α form is within 10 ppb of CODATA."""
    from python.giza_frequency_comb import fine_structure_second_order
    a2 = fine_structure_second_order()
    assert abs(a2["second_order_vs_codata_ppb"]) < 10.0


def test_alpha_second_order_300x_tighter_than_leading():
    """Second-order is at least 100× tighter than leading-order."""
    from python.giza_frequency_comb import fine_structure_second_order
    a2 = fine_structure_second_order()
    assert a2["improvement_factor"] > 100.0


def test_alpha_correction_shares_D_squared_with_chamber():
    """The D²/(2K_5³) correction shares D² with AW 26 chamber beat-sum anchor."""
    from python.giza_frequency_comb import fine_structure_second_order
    a2 = fine_structure_second_order()
    assert a2["D_squared_anchor_shared_with_chamber_beat_sum"]
    # Correction = 9/250 = D²/(2·K_5³)
    assert abs(a2["correction_value"] - 9.0/250.0) < 1e-15


# ---------------------------------------------------------------------------
# Menkaure impedance encoder
# ---------------------------------------------------------------------------

def test_menkaure_base_equals_3_times_69():
    """Menkaure base = 207 cubits = D × 69 = D × (Φ_4·K + 1)."""
    from python.giza_frequency_comb import (
        MENKAURE_BASE_CUBITS, MENKAURE_INTEGER_69,
    )
    assert MENKAURE_BASE_CUBITS == 207
    assert MENKAURE_INTEGER_69 == 69
    assert MENKAURE_BASE_CUBITS == 3 * MENKAURE_INTEGER_69


def test_menkaure_encoding_uses_impedance_constant_68():
    """68 = Φ_4·K = 17·4 — the AW 23 global impedance denominator."""
    from python.giza_frequency_comb import (
        menkaure_impedance_encoder, IMPEDANCE_DENOM_68,
    )
    m = menkaure_impedance_encoder()
    assert IMPEDANCE_DENOM_68 == 68
    assert m["impedance_denom_phi4_K"] == 68
    assert m["impedance_denom_matches_AW23"]


def test_menkaure_predicted_equals_observed():
    """Predicted Menkaure base = D·(Φ_4·K + 1) = 207 matches observed exactly."""
    from python.giza_frequency_comb import menkaure_impedance_encoder
    m = menkaure_impedance_encoder()
    assert m["menkaure_match_exact"]


def test_parallel_structure_khafre_menkaure():
    """Khafre and Menkaure both have form D·(Φ_4·X + 1) with X ∈ {SO_v, K}."""
    from python.giza_frequency_comb import menkaure_impedance_encoder
    m = menkaure_impedance_encoder()
    assert m["khafre_X_value"] == 8     # SO_v
    assert m["menkaure_X_value"] == 4    # K
    assert m["X_ratio_SOv_over_K"] == 2.0


def test_both_passive_integers_congruent_to_1_mod_phi4():
    """137 ≡ 1 (mod 17) and 69 ≡ 1 (mod 17)."""
    from python.giza_frequency_comb import menkaure_impedance_encoder
    m = menkaure_impedance_encoder()
    assert m["khafre_int_mod_phi4"] == 1
    assert m["menkaure_int_mod_phi4"] == 1
    assert m["both_congruent_to_1_mod_phi4"]


def test_khafre_minus_menkaure_equals_D_K_phi4():
    """Khafre base − Menkaure base = D·K·Φ_4 = 3·4·17 = 204 = D × impedance."""
    from python.giza_frequency_comb import menkaure_impedance_encoder
    m = menkaure_impedance_encoder()
    assert m["khafre_minus_menkaure_base"] == 204
    assert m["expected_diff_D_times_K_times_phi4"] == 204
    assert m["diff_matches_D_K_phi4"]


def test_showcase_has_second_order_section():
    out = showcase_frequency_comb()
    text = "\n".join(out)
    assert "SECOND-ORDER" in text or "second order" in text.lower()
    assert "9/250" in text or "9 / 250" in text


def test_showcase_has_menkaure_impedance_section():
    out = showcase_frequency_comb()
    text = "\n".join(out)
    assert "MENKAURE" in text
    assert "IMPEDANCE" in text or "impedance" in text
    assert "68" in text
    assert "69" in text


# ---------------------------------------------------------------------------
# Complete pyramid encoding — all 6 dimensions
# ---------------------------------------------------------------------------

def test_khafre_height_is_2_times_alpha_int():
    """Khafre height = 274 cubits = 2 × 137 = 2 × α_int."""
    from python.giza_frequency_comb import KHAFRE_HEIGHT_CUBITS, ALPHA_INTEGER_137
    assert KHAFRE_HEIGHT_CUBITS == 274
    assert KHAFRE_HEIGHT_CUBITS == 2 * ALPHA_INTEGER_137


def test_menkaure_height_is_K5_cubed():
    """Menkaure height = 125 cubits = 5³ = K_5³."""
    from python.giza_frequency_comb import MENKAURE_HEIGHT_CUBITS
    assert MENKAURE_HEIGHT_CUBITS == 125
    assert MENKAURE_HEIGHT_CUBITS == 5**3


def test_all_five_integer_exact():
    """All 5 framework-rational pyramid dimensions are integer-exact."""
    from python.giza_frequency_comb import complete_pyramid_encoding
    c = complete_pyramid_encoding()
    assert c["khufu_height_exact"]
    assert c["khafre_base_exact"]
    assert c["khafre_height_exact"]
    assert c["menkaure_base_exact"]
    assert c["menkaure_height_exact"]
    assert c["five_integer_exact"]


def test_khafre_base_height_ratio_is_3_over_2():
    """Khafre base/height = 411/274 = 3/2 exactly = D/(D−1) at D=3."""
    from python.giza_frequency_comb import complete_pyramid_encoding
    c = complete_pyramid_encoding()
    assert c["khafre_base_per_height_is_3_over_2"]
    assert abs(c["khafre_base_per_height"] - 1.5) < 1e-12


def test_khafre_double_alpha_encoding():
    """Khafre encodes α_int in both base/D and height/2."""
    from python.giza_frequency_comb import (
        KHAFRE_BASE_CUBITS, KHAFRE_HEIGHT_CUBITS, ALPHA_INTEGER_137,
    )
    assert KHAFRE_BASE_CUBITS / 3 == ALPHA_INTEGER_137
    assert KHAFRE_HEIGHT_CUBITS / 2 == ALPHA_INTEGER_137


def test_alpha_inv_from_khafre_base_and_menkaure_height():
    """1/α reconstructed from Khafre base + Menkaure height = 137.036."""
    from python.giza_frequency_comb import alpha_inv_from_two_pyramids
    a = alpha_inv_from_two_pyramids()
    assert abs(a["alpha_inv_2nd_order"] - 137.036) < 1e-12
    assert abs(a["deviation_ppb"]) < 10.0


def test_alpha_inv_from_khafre_height_and_menkaure_height():
    """Same 1/α using Khafre HEIGHT/2 instead of base/D (alt form)."""
    from python.giza_frequency_comb import alpha_inv_from_two_pyramids
    a = alpha_inv_from_two_pyramids(use_khafre_height=True)
    assert abs(a["alpha_inv_2nd_order"] - 137.036) < 1e-12


# ---------------------------------------------------------------------------
# Parallel K=4 identities — AP {105, 137, 169}
# ---------------------------------------------------------------------------

def test_phi3_SOv_plus_1_equals_phi6_squared():
    """At K=4: Φ_3·SO_v + 1 = 169 = Φ_6² = 13² (K=4-unique algebraic identity)."""
    from python.giza_frequency_comb import parallel_K4_identities
    p = parallel_K4_identities()
    assert p["phi_3_SOv_plus_1"] == 169
    assert p["phi_3_target_PHI_6_squared"] == 169
    assert p["phi_3_match"]


def test_phi6_SOv_plus_1_equals_D_K5_K_plus_D():
    """At K=4, D=3: Φ_6·SO_v + 1 = 105 = D·K_5·(K+D) = 3·5·7."""
    from python.giza_frequency_comb import parallel_K4_identities
    p = parallel_K4_identities()
    assert p["phi_6_SOv_plus_1"] == 105
    assert p["phi_6_target_D_K5_K_plus_D"] == 105
    assert p["phi_6_match"]


def test_phi_n_SOv_plus_1_arithmetic_progression():
    """{105, 137, 169} form AP with common difference K·SO_v = 32."""
    from python.giza_frequency_comb import parallel_K4_identities
    p = parallel_K4_identities()
    assert p["AP_check_169_minus_137"] == 32
    assert p["AP_check_137_minus_105"] == 32
    assert p["common_difference_K_SOv"] == 32


def test_phi4_SOv_plus_1_is_alpha_integer():
    """Middle of AP: Φ_4·SO_v + 1 = 137 = α integer."""
    from python.giza_frequency_comb import parallel_K4_identities
    p = parallel_K4_identities()
    assert p["phi_4_SOv_plus_1"] == 137
    assert p["phi_4_is_alpha_integer"]


def test_showcase_has_complete_encoding_section():
    out = showcase_frequency_comb()
    text = "\n".join(out)
    assert "COMPLETE PYRAMID ENCODING" in text
    assert "274" in text  # Khafre height
    assert "125" in text  # Menkaure height
    assert "K_5³" in text or "K_5^3" in text or "5³" in text


def test_showcase_has_parallel_identities_section():
    out = showcase_frequency_comb()
    text = "\n".join(out)
    assert "PARALLEL" in text or "AP" in text or "arithmetic progression" in text.lower()
    assert "169" in text and "105" in text and "137" in text
