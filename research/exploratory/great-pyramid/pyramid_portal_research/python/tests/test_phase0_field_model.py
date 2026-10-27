"""Tests for phase0_field_model.py — P0.1 closure uniformity and capstone pump.

Resolutions are reduced for speed; the full-resolution results are in
phase0/P0.1_field_model_results.md."""

import math
import numpy as np
import pytest

from python.phase0_field_model import (
    H_M, B_M, KC_FLOOR_M, ZSTAR_FRAC, INCH, G_EARTH, CONE_A_M,
    self_gravity, section_flux, study_a, solve_axisymmetric,
    dielectric_section_flux, study_b,
)


def test_cone_has_equal_base_area():
    assert abs(math.pi * CONE_A_M ** 2 - B_M ** 2) < 1e-6 * B_M ** 2


def test_self_gravity_is_tiny_and_points_up_at_base():
    g = self_gravity(np.array([[0.0, 0.0, 1.0]]), n_cells=20)
    assert g[0, 2] > 0                       # mass above pulls upward
    assert 1e-6 < g[0, 2] / G_EARTH < 2e-5


def test_uniform_field_gives_areal_flux():
    f0 = section_flux(0.0, include_self=False, include_free_air=False)
    fz = section_flux(ZSTAR_FRAC * H_M, include_self=False, include_free_air=False)
    assert abs(fz / f0 - 0.5) < 1e-10


@pytest.fixture(scope="module")
def a_result():
    return study_a(nz=11)


def test_study_a_half_point_at_z_star(a_result):
    assert abs(a_result.shift_from_zstar_in) < 0.1


def test_study_a_preregistered_test_confirms(a_result):
    assert abs(a_result.offset_from_floor_in) <= 3.0


def test_study_a_uniformity_margin(a_result):
    # 01.7 requires |eps| < 1.3e-3; the field's axial variation is far smaller.
    assert a_result.free_air_fraction < 1.3e-3 / 20
    assert a_result.self_field_fraction < a_result.free_air_fraction


@pytest.fixture(scope="module")
def b_result():
    return study_b(dr=6.0)


def test_b1_dielectric_flux_balances_above_z_star(b_result):
    """The EM pump field does not locate the Field Origin: its D-flux in a
    dielectric body balances well above z* (about 61 m at fine resolution)."""
    assert 50.0 < b_result.b1_half_point_m < 70.0
    assert b_result.b1_shift_from_zstar_m > 10.0


def test_b2_capture_area_and_power_scale(b_result):
    footprint = B_M ** 2
    assert 1.5 * footprint < b_result.b2_capture_area_m2 < 3.0 * footprint
    assert 1e-7 < b_result.b2_current_fair_A < 5e-7
    assert 5e-4 < b_result.b2_power_bound_fair_W < 2e-3
    assert 1.0 < b_result.b2_power_bound_storm_W < 20.0


def test_b2_apex_enhancement_exceeds_unity(b_result):
    assert b_result.b2_apex_enhancement > 2.0


def test_ground_and_far_field_boundary_conditions():
    g, V, eps, inside = solve_axisymmetric(dr=12.0, eps_body=8.0)
    assert np.allclose(V[:, 0], 0.0)
    assert np.allclose(V[-1, :], -130.0 * g.z)
