"""Tests for vortex_calibration.py."""

import math
import numpy as np
import pytest

from python.vortex_calibration import (
    continuous_eisenstein_rotation,
    continuous_omega_rotation,
    sector_norms,
    run_closure_cycle,
    compute_votes,
    compute_impedance,
    make_test_state,
    make_axial_only_state,
    make_mixed_test_state,
    sweep_v_read,
    showcase_vortex_calibration,
)
from python.closure_core256 import omega_power3


# ---------------------------------------------------------------------------
# Continuous rotation primitives
# ---------------------------------------------------------------------------

def test_continuous_eisenstein_zero_is_identity():
    """θ = 0 leaves the pair unchanged."""
    pair = (0.7, -0.3)
    out = continuous_eisenstein_rotation(pair, 0.0)
    assert abs(out[0] - pair[0]) < 1e-12
    assert abs(out[1] - pair[1]) < 1e-12


def test_continuous_eisenstein_2pi_returns_to_start():
    """θ = 2π returns the pair to itself."""
    pair = (1.3, 0.5)
    out = continuous_eisenstein_rotation(pair, 2 * math.pi)
    assert abs(out[0] - pair[0]) < 1e-10
    assert abs(out[1] - pair[1]) < 1e-10


def test_continuous_eisenstein_at_2pi_over_3_matches_discrete_omega():
    """θ = 2π/3 should reproduce the discrete Ω-action on the pair."""
    # Discrete Ω on Eisenstein pair: (x, y) → (-y, x - y).
    pair = (0.6, 0.4)
    out_continuous = continuous_eisenstein_rotation(pair, 2 * math.pi / 3)
    out_discrete = (-pair[1], pair[0] - pair[1])
    assert abs(out_continuous[0] - out_discrete[0]) < 1e-10
    assert abs(out_continuous[1] - out_discrete[1]) < 1e-10


def test_continuous_omega_at_2pi_over_3_matches_omega_power3():
    """The full-coefficient continuous Ω at θ=2π/3 = discrete omega_power3."""
    state = make_mixed_test_state()
    out_continuous = continuous_omega_rotation(state, 2 * math.pi / 3)
    out_discrete = omega_power3(state, 1)
    np.testing.assert_allclose(out_continuous, out_discrete, atol=1e-10)


def test_continuous_omega_2pi_returns_to_start():
    state = make_mixed_test_state()
    out = continuous_omega_rotation(state, 2 * math.pi)
    np.testing.assert_allclose(out, state, atol=1e-10)


def test_axial_sector_fixed_under_rotation():
    """Pure axial states are invariant under Ω-rotation at any angle."""
    state = make_axial_only_state()
    for theta in [0.1, 0.7, 1.5, 2.0, math.pi, 5.1]:
        out = continuous_omega_rotation(state, theta)
        np.testing.assert_allclose(out, state, atol=1e-12)


# ---------------------------------------------------------------------------
# Sector norms
# ---------------------------------------------------------------------------

def test_sector_norms_for_test_state():
    """Initial state e_0 + T_2: axial norm 1, bivector norm √3, vector 0."""
    state = make_test_state()
    ax, vec, biv = sector_norms(state)
    assert abs(ax - 1.0) < 1e-12
    assert abs(vec - 0.0) < 1e-12
    assert abs(biv - math.sqrt(3.0)) < 1e-12


def test_sector_norms_axial_only():
    state = make_axial_only_state()
    ax, vec, biv = sector_norms(state)
    assert abs(ax - math.sqrt(2.0)) < 1e-12
    assert vec == 0.0
    assert biv == 0.0


# ---------------------------------------------------------------------------
# Closure cycle
# ---------------------------------------------------------------------------

def test_full_cycle_returns_to_initial_state():
    """One full closure cycle (2π in each channel) returns to initial state."""
    state = make_mixed_test_state()
    trace = run_closure_cycle(state, v_read=1.0, n_substeps=360)
    np.testing.assert_allclose(trace.states[-1], trace.states[0], atol=1e-10)


def test_axial_norm_invariant_along_cycle():
    """Axial-sector norm is invariant along the cycle (Ω fixes axial)."""
    state = make_test_state()
    trace = run_closure_cycle(state, v_read=1.0, n_substeps=120)
    ax0 = trace.sector_axial[0]
    for ax_t in trace.sector_axial:
        assert abs(ax_t - ax0) < 1e-10


def test_axial_only_state_stays_axial():
    """Axial state has zero vector and bivector content throughout the cycle."""
    state = make_axial_only_state()
    trace = run_closure_cycle(state, v_read=1.0, n_substeps=60)
    assert np.all(np.abs(trace.sector_vector) < 1e-12)
    assert np.all(np.abs(trace.sector_bivector) < 1e-12)


# ---------------------------------------------------------------------------
# Votes — (P1) v_read invariance
# ---------------------------------------------------------------------------

def test_vote_ratios_v_read_invariant():
    """(P1) Vote ratios are EXACTLY invariant under v_read."""
    state = make_test_state()
    v_values = [0.25, 1.0, 4.0, 16.0]
    ratios_biv = []
    ratios_vec = []
    for v in v_values:
        trace = run_closure_cycle(state, v_read=v, n_substeps=360)
        votes = compute_votes(trace)
        ratios_biv.append(votes.ratio_biv_over_axial)
        ratios_vec.append(votes.ratio_vector_over_axial)
    # The ratio range across v_read should be zero up to round-off.
    assert (max(ratios_biv) - min(ratios_biv)) < 1e-12
    assert (max(ratios_vec) - min(ratios_vec)) < 1e-12


def test_axial_vote_equals_axial_norm():
    """For the canonical test state, axial vote = axial norm = 1 (it's fixed)."""
    state = make_test_state()
    trace = run_closure_cycle(state, v_read=1.0, n_substeps=360)
    votes = compute_votes(trace)
    assert abs(votes.V_axial - 1.0) < 1e-10


def test_vector_and_bivector_votes_close_by_symmetry():
    """Under continuous rotation, V_vec and V_biv are approximately equal.

    The continuous Ω-rotation mixes grade-1 and grade-2 content through
    the Hodge-like dual coupling, giving time-averages that match to
    leading order.  Not exactly equal because the rotation is asymmetric
    between the two grades — but close enough that the symmetry is
    structurally evident (within 1% for the canonical seed).
    """
    state = make_test_state()
    trace = run_closure_cycle(state, v_read=1.0, n_substeps=720)
    votes = compute_votes(trace)
    # Within 1% of each other.
    rel_diff = abs(votes.V_vector - votes.V_bivector) / max(
        votes.V_vector, votes.V_bivector
    )
    assert rel_diff < 0.01


# ---------------------------------------------------------------------------
# Impedance — (P2) v_read scaling
# ---------------------------------------------------------------------------

def test_leakage_per_cycle_v_read_invariant():
    """(P2 negative half) Leakage per cycle does NOT depend on v_read."""
    state = make_test_state()
    leakages = []
    for v in [0.25, 1.0, 4.0, 16.0]:
        trace = run_closure_cycle(state, v_read=v, n_substeps=360)
        leakages.append(compute_impedance(trace)["leakage_half_cycle"])
    spread = max(leakages) - min(leakages)
    assert spread < 1e-10


def test_impedance_per_unit_time_scales_linearly_with_v_read():
    """(P2 positive half) Impedance / time scales linearly with v_read."""
    state = make_test_state()
    pairs = []
    for v in [0.5, 1.0, 2.0, 4.0]:
        trace = run_closure_cycle(state, v_read=v, n_substeps=360)
        imp = compute_impedance(trace)["impedance_per_unit_time"]
        pairs.append((v, imp))
    # Linear: imp = k * v_read for some constant k.
    k_values = [imp / v for v, imp in pairs]
    assert (max(k_values) - min(k_values)) < 1e-9


def test_pure_scalar_state_has_zero_leakage():
    """A pure scalar state is mirror-fixed and has zero leakage.

    Note: a state with non-zero I (pseudoscalar) component picks up a
    parity-flip leakage of 2|c_I| because grade involution negates I.
    """
    state = np.zeros(8, dtype=float)
    state[0] = 1.0
    trace = run_closure_cycle(state, v_read=1.0, n_substeps=180)
    imp = compute_impedance(trace)
    assert imp["leakage_half_cycle"] < 1e-10


def test_axial_state_with_I_picks_up_parity_leakage():
    """An e_0 + I state leaks exactly 2 from grade-involution mismatch.

    The state is fixed by Ω rotation (axial sector), but parity flip
    negates I, so half-cycle state and mirror-expected state differ by 2I,
    norm 2.  An axial-only mode is the vortex axis itself, with zero
    circulation; the parity leakage of 2 isolates this kinematic effect
    from the dynamical vortex picture.
    """
    state = make_axial_only_state()
    trace = run_closure_cycle(state, v_read=1.0, n_substeps=180)
    imp = compute_impedance(trace)
    assert abs(imp["leakage_half_cycle"] - 2.0) < 1e-10


# ---------------------------------------------------------------------------
# Specific structural values
# ---------------------------------------------------------------------------

def test_leakage_for_T2_state_is_2_sqrt_3():
    """For the e_0 + T_2 state, half-cycle leakage = 2√3 exactly."""
    state = make_test_state()
    trace = run_closure_cycle(state, v_read=1.0, n_substeps=720)
    imp = compute_impedance(trace)
    assert abs(imp["leakage_half_cycle"] - 2 * math.sqrt(3)) < 1e-3


# ---------------------------------------------------------------------------
# Sweep + showcase
# ---------------------------------------------------------------------------

def test_sweep_v_read_returns_one_row_per_value():
    rows = sweep_v_read([0.5, 1.0, 2.0], n_substeps=60)
    assert len(rows) == 3
    for r in rows:
        assert "v_read" in r
        assert "V_axial" in r
        assert "impedance_per_unit_time" in r


def test_showcase_produces_output():
    out = showcase_vortex_calibration()
    text = "\n".join(out)
    assert "VORTEX CALIBRATION" in text
    assert "v_read" in text
    assert "P1" in text and "P2" in text
