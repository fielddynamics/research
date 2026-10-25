"""Tests for kc_kinematics.py — King's Chamber kinematic predictions."""

import math
import pytest

from python.kc_kinematics import (
    OMEGA_EARTH, GIZA_LATITUDE_DEG, GIZA_LATITUDE_RAD,
    OMEGA_EARTH_VERTICAL, SIDEREAL_DAY_S,
    k_vector_magnitude_m_inv,
    mode_wavelength_m, mode_period_s, mode_angular_frequency_rad_per_s,
    mode_phase_velocity_m_per_s,
    axis_roundtrip_time_s, all_axis_roundtrips,
    adjacent_mode_beats, mode_circulation_m2_per_s,
    coriolis_split_rad_per_s, coriolis_split_hz,
    sagnac_phase_per_roundtrip_rad,
    mode_kinematics, all_modes_kinematics,
    showcase_kc_kinematics,
)
from python.pyramid_resonance import (
    KC_L_CUBITS, KC_W_CUBITS, KC_H_CUBITS, ROYAL_CUBIT_M,
    V_AIR, V_GRANITE_P,
    Mode, lowest_modes,
)


# ---------------------------------------------------------------------------
# Earth and site constants
# ---------------------------------------------------------------------------

def test_sidereal_day_is_close_to_86164s():
    """One sidereal day ≈ 86164.0905 s."""
    assert abs(SIDEREAL_DAY_S - 86164.0905) < 1.0


def test_omega_earth_is_correct():
    """Ω_E = 2π / T_sidereal ≈ 7.292e-5 rad/s."""
    assert abs(OMEGA_EARTH - 7.2921e-5) < 5e-9


def test_giza_latitude_value():
    """Great Pyramid latitude is 29.9792° N."""
    assert abs(GIZA_LATITUDE_DEG - 29.9792) < 0.001
    assert abs(math.sin(GIZA_LATITUDE_RAD) - 0.4997) < 0.001


def test_omega_earth_vertical_at_giza():
    """Vertical component Ω_E sin(φ) ≈ 3.644e-5 rad/s."""
    expected = OMEGA_EARTH * math.sin(GIZA_LATITUDE_RAD)
    assert abs(OMEGA_EARTH_VERTICAL - expected) < 1e-12
    assert 3.6e-5 < OMEGA_EARTH_VERTICAL < 3.7e-5


# ---------------------------------------------------------------------------
# Per-mode kinematics
# ---------------------------------------------------------------------------

def test_k_vector_magnitude_for_fundamental():
    """|k| for (1,1,1) mode is finite and positive."""
    m = Mode(1, 1, 1, 0.0205)
    k = k_vector_magnitude_m_inv(m)
    assert k > 0
    # Order of magnitude check: |k| ~ π/L ~ π/10.47 ~ 0.3 m^-1; total ~0.86
    assert 0.5 < k < 1.5


def test_mode_wavelength_matches_v_over_f():
    """λ = v / f for any mode."""
    for m in lowest_modes(21):
        f = m.frequency_hz(V_AIR)
        wavelength = mode_wavelength_m(m, V_AIR)
        assert abs(wavelength - V_AIR / f) < 1e-9


def test_mode_period_matches_one_over_f():
    """T = 1 / f."""
    for m in lowest_modes(5):
        T = mode_period_s(m, V_AIR)
        f = m.frequency_hz(V_AIR)
        assert abs(T - 1.0 / f) < 1e-12


def test_phase_velocity_equals_wave_speed():
    """For non-dispersive medium, v_phase = v_wave for every mode."""
    for m in lowest_modes(21):
        vp = mode_phase_velocity_m_per_s(m, V_AIR)
        assert vp == V_AIR


# ---------------------------------------------------------------------------
# Roundtrip times
# ---------------------------------------------------------------------------

def test_axis_roundtrip_basic_formula():
    """T_rt = 2 L_axis / v_wave."""
    L_m = KC_L_CUBITS * ROYAL_CUBIT_M
    T_rt = axis_roundtrip_time_s(KC_L_CUBITS, V_AIR)
    assert abs(T_rt - 2.0 * L_m / V_AIR) < 1e-12


def test_L_axis_roundtrip_in_air_is_about_60ms():
    """L = 20 cubits = 10.47 m;  2L/343 ≈ 61 ms."""
    rt = all_axis_roundtrips(V_AIR)
    assert 59e-3 < rt["L_axis_s"] < 63e-3


def test_L_axis_roundtrip_in_granite_is_about_3point5ms():
    """L = 10.47 m;  2L/6000 ≈ 3.5 ms."""
    rt = all_axis_roundtrips(V_GRANITE_P)
    assert 3.0e-3 < rt["L_axis_s"] < 4.0e-3


def test_diagonal_roundtrip_uses_25_cubits():
    """Space-diagonal = 25 cubits = 13.09 m."""
    rt_air = all_axis_roundtrips(V_AIR)
    expected = 2.0 * 25.0 * ROYAL_CUBIT_M / V_AIR
    assert abs(rt_air["diagonal_s"] - expected) < 1e-12


# ---------------------------------------------------------------------------
# Mode degeneracies — three exact pairs in the 21 lowest
# ---------------------------------------------------------------------------

def test_three_exact_frequency_degeneracies():
    """Chamber dimensions force three exact degeneracies among 21 lowest modes:
      (2,2,1) and (4,1,1) at 78.88 Hz
      (2,2,2) and (4,1,2) at 93.79 Hz
      (3,1,3) and (5,1,2) at 105.88 Hz
    Driven by  n_x² + 4 n_y² = invariant  (from L:W = 2:1).
    """
    modes = lowest_modes(21)
    frequencies = [m.frequency_hz(V_AIR) for m in modes]
    triples = [(m.n_x, m.n_y, m.n_z) for m in modes]

    # Pair 1: (2,2,1) <-> (4,1,1)
    i1 = triples.index((2, 2, 1))
    i2 = triples.index((4, 1, 1))
    assert abs(frequencies[i1] - frequencies[i2]) < 1e-9

    # Pair 2: (2,2,2) <-> (4,1,2)
    i1 = triples.index((2, 2, 2))
    i2 = triples.index((4, 1, 2))
    assert abs(frequencies[i1] - frequencies[i2]) < 1e-9

    # Pair 3: (3,1,3) <-> (5,1,2)
    i1 = triples.index((3, 1, 3))
    i2 = triples.index((5, 1, 2))
    assert abs(frequencies[i1] - frequencies[i2]) < 1e-9


def test_degeneracy_quadratic_form_invariant():
    """The L:W = 2:1 ratio makes  n_x² + 4 n_y²  an invariant of mode equivalence
    in the (n_x, n_y) projection.

    Pairs: (2,2) and (4,1):  4 + 16 = 16 + 4 = 20.
    """
    def q(n_x: int, n_y: int) -> int:
        return n_x ** 2 + 4 * n_y ** 2

    assert q(2, 2) == q(4, 1) == 20
    # (3, 1) and (1, ...) : 9 + 4 = 13.  Find (a, b) with q(a, b) = 13.
    # a²+4b²=13:  a=3,b=1: 13.  a=1,b=√3: not integer.  Unique.


# ---------------------------------------------------------------------------
# Adjacent-mode beats
# ---------------------------------------------------------------------------

def test_adjacent_beats_returns_20_pairs():
    """21 modes → 20 adjacent pairs."""
    beats = adjacent_mode_beats(V_AIR, 21)
    assert len(beats) == 20


def test_three_zero_beats_from_degeneracies():
    """Three of the 20 adjacent-pair gaps are exactly zero (the degeneracies)."""
    beats = adjacent_mode_beats(V_AIR, 21)
    zero_beats = [b for b in beats if b.delta_f < 1e-9]
    assert len(zero_beats) == 3


def test_beat_period_under_2s_for_close_pairs():
    """Adjacent non-degenerate pairs in the comb beat in ~0.5–2 s."""
    beats = adjacent_mode_beats(V_AIR, 21)
    finite_periods = [b.beat_period_s for b in beats if b.delta_f > 1e-6]
    # Most adjacent pairs beat at under 5 seconds; some are much faster
    short = [t for t in finite_periods if t < 2.0]
    assert len(short) >= 5


# ---------------------------------------------------------------------------
# Coriolis splitting
# ---------------------------------------------------------------------------

def test_coriolis_split_is_2_omega_sin_phi():
    """Δω = 2 Ω_E sin(φ_Giza), mode-independent."""
    m = Mode(1, 1, 1, 0.0205)
    delta = coriolis_split_rad_per_s(m)
    expected = 2.0 * OMEGA_EARTH_VERTICAL
    assert abs(delta - expected) < 1e-12


def test_coriolis_split_is_mode_independent():
    """Coriolis Δω is the same for every mode (pure kinematic effect)."""
    deltas = [coriolis_split_rad_per_s(m) for m in lowest_modes(21)]
    spread = max(deltas) - min(deltas)
    assert spread < 1e-15


def test_coriolis_period_is_about_24_hours():
    """T = 1 / Δf ≈ sidereal day ≈ 86164 s ≈ 23.93 hr."""
    m = Mode(1, 1, 1, 0.0205)
    df = coriolis_split_hz(m)
    T = 1.0 / df
    assert 23.5 * 3600.0 < T < 24.5 * 3600.0
    # More precise: T = (2π/Δω) = π/(Ω_E sin φ) = T_sidereal / (2 sin φ)
    expected = SIDEREAL_DAY_S / (2.0 * math.sin(GIZA_LATITUDE_RAD))
    assert abs(T - expected) < 1.0


# ---------------------------------------------------------------------------
# Sagnac phase
# ---------------------------------------------------------------------------

def test_sagnac_phase_positive_for_chamber():
    """Sagnac phase per roundtrip is positive for all modes at Giza."""
    for m in lowest_modes(21):
        s = sagnac_phase_per_roundtrip_rad(m, V_AIR)
        assert s > 0


def test_sagnac_grows_with_mode_index():
    """Higher-|k| modes have larger Sagnac phase (Δφ ∝ |k|)."""
    modes = lowest_modes(21)
    sagnacs = [sagnac_phase_per_roundtrip_rad(m, V_AIR) for m in modes]
    # Sagnac for mode 21 > for mode 1
    assert sagnacs[-1] > sagnacs[0]
    # Ratio sagnac_21 / sagnac_1 should equal |k|_21 / |k|_1
    k1 = k_vector_magnitude_m_inv(modes[0])
    k21 = k_vector_magnitude_m_inv(modes[20])
    expected_ratio = k21 / k1
    actual_ratio = sagnacs[-1] / sagnacs[0]
    assert abs(actual_ratio - expected_ratio) < 1e-9


# ---------------------------------------------------------------------------
# Vortex circulation per mode
# ---------------------------------------------------------------------------

def test_circulation_equals_v_times_wavelength():
    """Γ = v · λ for every mode."""
    for m in lowest_modes(5):
        gamma = mode_circulation_m2_per_s(m, V_AIR)
        lam = mode_wavelength_m(m, V_AIR)
        assert abs(gamma - V_AIR * lam) < 1e-9


def test_fundamental_circulation_largest():
    """Lowest-frequency mode has the longest λ, hence largest circulation."""
    modes = lowest_modes(21)
    gammas = [mode_circulation_m2_per_s(m, V_AIR) for m in modes]
    # Fundamental (1,1,1) has the longest λ
    assert gammas[0] == max(gammas)


# ---------------------------------------------------------------------------
# Comprehensive kinematic entry & showcase
# ---------------------------------------------------------------------------

def test_mode_kinematics_assembles_all_fields():
    m = Mode(1, 1, 1, 0.0205)
    k = mode_kinematics(m, V_AIR)
    assert k.f_hz > 0
    assert k.period_s > 0
    assert k.wavelength_m > 0
    assert k.k_magnitude_inv_m > 0
    assert k.circulation_m2_per_s > 0
    assert k.coriolis_split_hz > 0


def test_all_modes_kinematics_returns_21():
    out = all_modes_kinematics(21, V_AIR)
    assert len(out) == 21


def test_showcase_runs_and_includes_keywords():
    out = showcase_kc_kinematics()
    text = "\n".join(out)
    assert "KING'S CHAMBER KINEMATICS" in text
    assert "Coriolis" in text or "coriolis" in text.lower()
    assert "Sagnac" in text or "sagnac" in text.lower()
    assert "circulation" in text.lower()
    assert "roundtrip" in text.lower()
