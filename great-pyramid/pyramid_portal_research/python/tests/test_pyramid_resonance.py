"""Tests for pyramid_resonance.py — King's Chamber 21-mode comb."""

import math
import pytest

from python.pyramid_resonance import (
    ROYAL_CUBIT_M, KC_L_CUBITS, KC_W_CUBITS, KC_H_CUBITS,
    V_AIR, V_GRANITE_P,
    Mode, enumerate_modes, lowest_modes,
    kc_dimensions_m, kc_space_diagonal_squared_cubits,
    kc_space_diagonal_cubits, verify_kc_K_squared_identity,
    cyclotomic_sector, omega_orbit, sector_distribution_audit,
    predict_21_mode_comb,
    vortex_omega_for_chamber, vortex_frequency_for_apparatus,
    bare_K4_K5_transition_bracket,
    showcase_pyramid_resonance,
)


# ---------------------------------------------------------------------------
# Chamber identity
# ---------------------------------------------------------------------------

def test_kc_dimensions_in_cubits():
    """20 × 10 × 5√5 royal cubits."""
    assert KC_L_CUBITS == 20.0
    assert KC_W_CUBITS == 10.0
    assert abs(KC_H_CUBITS - 5.0 * math.sqrt(5.0)) < 1e-12


def test_kc_dimensions_in_metres():
    """Converted to metres: ~10.47 × ~5.24 × ~5.85."""
    L, W, H = kc_dimensions_m()
    assert abs(L - 10.472) < 0.001
    assert abs(W - 5.236) < 0.001
    assert abs(H - 5.854) < 0.001     # 5√5 × 0.5236 = 5.854


def test_space_diagonal_squared_is_625():
    """The signature framework identity: L² + W² + H² = 625 = 25²."""
    assert abs(kc_space_diagonal_squared_cubits() - 625.0) < 1e-9


def test_space_diagonal_is_25_cubits():
    """The diagonal length is exactly 25 cubits — K at K = 5."""
    assert abs(kc_space_diagonal_cubits() - 25.0) < 1e-9


def test_K_squared_identity_recovers_K5():
    """Full structural verification of the K = 5 identity."""
    out = verify_kc_K_squared_identity()
    assert out["L_squared"] == 400.0
    assert out["W_squared"] == 100.0
    assert abs(out["H_squared"] - 125.0) < 1e-9
    assert abs(out["sum"] - 625.0) < 1e-9
    assert out["K"] == 5
    assert out["K_squared"] == 25
    assert out["matches"]


# ---------------------------------------------------------------------------
# Mode enumeration
# ---------------------------------------------------------------------------

def test_enumerate_modes_returns_n_max_cubed():
    """All positive-integer triples are enumerated."""
    modes = enumerate_modes(n_max=4)
    assert len(modes) == 4 * 4 * 4


def test_enumerate_modes_sorted_by_Q():
    """Modes are returned in ascending Q order."""
    modes = enumerate_modes(n_max=6)
    Q_values = [m.Q for m in modes]
    assert Q_values == sorted(Q_values)


def test_lowest_mode_is_111():
    """The fundamental cavity mode is (n_x, n_y, n_z) = (1, 1, 1)."""
    m = lowest_modes(1)[0]
    assert (m.n_x, m.n_y, m.n_z) == (1, 1, 1)


def test_lowest_mode_Q_is_correct():
    """Q for (1,1,1) = 1/400 + 1/100 + 1/125 = 0.0205."""
    m = lowest_modes(1)[0]
    expected = 1.0 / 400.0 + 1.0 / 100.0 + 1.0 / 125.0
    assert abs(m.Q - expected) < 1e-12
    assert abs(m.Q - 0.0205) < 1e-12


def test_lowest_21_modes_exist():
    """The framework's 21-mode comb is recovered as the 21 lowest-frequency modes."""
    modes = lowest_modes(21)
    assert len(modes) == 21


def test_mode_frequency_in_air():
    """Fundamental mode frequency in air is approximately 47 Hz."""
    m = Mode(1, 1, 1, 1.0 / 400.0 + 1.0 / 100.0 + 1.0 / 125.0)
    f = m.frequency_hz(V_AIR)
    assert 46.0 < f < 48.0


def test_mode_frequency_in_granite():
    """Fundamental mode frequency for granite P-wave is approximately 820 Hz."""
    m = Mode(1, 1, 1, 1.0 / 400.0 + 1.0 / 100.0 + 1.0 / 125.0)
    f = m.frequency_hz(V_GRANITE_P)
    assert 815.0 < f < 825.0


def test_21_modes_in_expected_frequency_range():
    """All 21 modes fall in 10 Hz - 1 kHz (air) or 100 Hz - 10 kHz (granite)."""
    modes = lowest_modes(21)
    f_air = [m.frequency_hz(V_AIR) for m in modes]
    f_gran = [m.frequency_hz(V_GRANITE_P) for m in modes]
    assert min(f_air) >= 10.0
    assert max(f_air) <= 1000.0
    assert min(f_gran) >= 100.0
    assert max(f_gran) <= 10000.0


# ---------------------------------------------------------------------------
# Cyclotomic sectoring — research finding
# ---------------------------------------------------------------------------

def test_cyclotomic_sector_of_111_is_0():
    m = Mode(1, 1, 1, 0.0205)
    assert cyclotomic_sector(m) == 0


def test_cyclotomic_sector_of_211_is_1():
    m = Mode(2, 1, 1, 0.028)
    assert cyclotomic_sector(m) == 1


def test_cyclotomic_sector_of_311_is_2():
    m = Mode(3, 1, 1, 0.0405)
    assert cyclotomic_sector(m) == 2


def test_omega_orbit_of_symmetric_mode_has_size_1():
    """(1,1,1) is Ω-symmetric — orbit size 1."""
    m = Mode(1, 1, 1, 0.0205)
    assert len(omega_orbit(m)) == 1


def test_omega_orbit_of_asymmetric_mode_has_size_3():
    """(3,1,2) is fully asymmetric — orbit size 3."""
    m = Mode(3, 1, 2, 0.0645)
    assert len(omega_orbit(m)) == 3


def test_sector_distribution_is_not_777():
    """The 21 lowest modes do NOT split 7:7:7 across Z_3 by index-sum.

    This is a research finding: the simple (n_x+n_y+n_z) mod 3 sectoring
    cannot recover the framework's predicted Z_3 × Z_7 = 21 structure
    because the chamber's L : W : H asymmetry breaks the cyclic symmetry
    on spatial indices.  The Z_3 must act on each mode's polarization
    (Cl(3,0) Eisenstein decomposition) instead.
    """
    modes = lowest_modes(21)
    audit = sector_distribution_audit(modes)
    assert audit["total_modes"] == 21
    sc = audit["sector_counts"]
    assert sum(sc.values()) == 21
    assert not audit["is_clean_777_split"]
    # The observed empirical distribution is 6 : 8 : 7
    assert sc[0] == 6
    assert sc[1] == 8
    assert sc[2] == 7


def test_partial_omega_orbits_exist():
    """Several orbits are partial because chamber is dimensionally asymmetric."""
    modes = lowest_modes(21)
    audit = sector_distribution_audit(modes)
    assert audit["n_partial_orbits"] > 0


# ---------------------------------------------------------------------------
# Frequency predictions
# ---------------------------------------------------------------------------

def test_predict_air_comb_returns_21_frequencies():
    pred = predict_21_mode_comb(V_AIR, "air")
    assert len(pred.frequencies_hz) == 21
    assert len(pred.modes) == 21
    assert pred.medium == "air"


def test_predict_granite_comb_returns_21_frequencies():
    pred = predict_21_mode_comb(V_GRANITE_P, "granite-P")
    assert len(pred.frequencies_hz) == 21
    assert all(100.0 < f < 10000.0 for f in pred.frequencies_hz)


def test_air_comb_span_under_1khz():
    """The air-coupled 21-mode comb fits below 1 kHz."""
    pred = predict_21_mode_comb(V_AIR, "air")
    assert pred.f_max() < 1000.0


def test_granite_p_comb_includes_kHz_range():
    """The granite-coupled comb extends into kHz."""
    pred = predict_21_mode_comb(V_GRANITE_P, "granite-P")
    assert pred.f_min() > 100.0
    assert pred.f_max() > 1000.0


def test_predictions_proportional_to_wave_speed():
    """Frequencies scale linearly with wave speed (verifying f = v·k/2π)."""
    p1 = predict_21_mode_comb(1000.0, "ref")
    p2 = predict_21_mode_comb(2000.0, "double")
    for f1, f2 in zip(p1.frequencies_hz, p2.frequencies_hz):
        assert abs(f2 / f1 - 2.0) < 1e-10


# ---------------------------------------------------------------------------
# Vortex calibration connection
# ---------------------------------------------------------------------------

def test_vortex_omega_identity():
    """ω = 2π v / ℓ — basic vortex identity."""
    omega = vortex_omega_for_chamber(v_read=343.0, ell_closure_m=10.472)
    expected = 2.0 * math.pi * 343.0 / 10.472
    assert abs(omega - expected) < 1e-9


def test_vortex_frequency_for_air():
    """Apparatus vortex frequency with air ≈ 32.7 Hz."""
    out = vortex_frequency_for_apparatus(V_AIR)
    assert 32.0 < out["f_hz"] < 34.0
    assert abs(out["ell_closure_cubits"] - 20.0) < 1e-12


def test_vortex_frequency_for_granite():
    """Apparatus vortex frequency with granite P ≈ 573 Hz."""
    out = vortex_frequency_for_apparatus(V_GRANITE_P)
    assert 570.0 < out["f_hz"] < 576.0


def test_K4_K5_bare_bracket():
    """Bracket on ω_{K4→K5} from framework + CODATA constants."""
    out = bare_K4_K5_transition_bracket()
    # ω_C ≈ 7.76e20 rad/s (electron Compton)
    assert 7.7e20 < out["omega_Compton"] < 7.8e20
    # ω_K4K5_bare via α²¹ ≈ 10⁻²⁵ rad/s (gravity-scale)
    assert 1e-25 < out["omega_K4K5_bare_via_alpha21"] < 1e-23
    # Vortex identity: ω_C = 2π c / λ_C exactly
    assert out["vortex_identity_holds"]


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def test_showcase_produces_output():
    out = showcase_pyramid_resonance()
    text = "\n".join(out)
    assert "KING'S CHAMBER" in text
    assert "21 lowest-frequency modes" in text
    assert "vortex" in text.lower()
    assert "ω_Compton" in text or "Compton" in text


def test_showcase_lists_all_21_modes():
    out = showcase_pyramid_resonance()
    text = "\n".join(out)
    # Spot-check the first mode (1,1,1)
    assert "( 1, 1, 1)" in text
    # And one of the higher modes
    assert "( 5, 1, 2)" in text
