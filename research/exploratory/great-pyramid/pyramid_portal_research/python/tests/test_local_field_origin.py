"""Tests for local_field_origin.py — local Field Origin of a bounded closure (01.6)."""

import math
import pytest

from python.local_field_origin import (
    FIELD_ORIGIN_FRACTION, VOLUMETRIC_FRACTION,
    PETRIE_HEIGHT_IN, PETRIE_HALF_AREA_LEVEL_IN, PETRIE_HALF_AREA_ERR_IN,
    PETRIE_KC_FLOOR_RANGE_IN, ROYAL_CUBIT_IN,
    mu_of_x, s_of_x, s_of_mu, coupling_capacity,
    area_fraction, local_state, local_field_origin_height,
    volumetric_balance_height, great_pyramid_comparison,
)


# ---------------------------------------------------------------------------
# GFD identities
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("x", [1e-6, 0.1, 0.5, 1.0, 2.0, 10.0, 1e6])
def test_identity_s_equals_two_mu_minus_one(x):
    assert abs(s_of_x(x) - s_of_mu(mu_of_x(x))) < 1e-12


def test_field_origin_states():
    assert mu_of_x(1.0) == 0.5
    assert s_of_x(1.0) == 0.0
    assert coupling_capacity(0.0) == 17.0
    assert coupling_capacity(+1.0) == 21.0
    assert coupling_capacity(-1.0) == 13.0


# ---------------------------------------------------------------------------
# Proposition 1: full-range realisation
# ---------------------------------------------------------------------------

def test_base_is_tetA_and_apex_is_tetB():
    h = 100.0
    assert local_state(0.0, h) == (1.0, 1.0, 21.0)
    mu, s, f = local_state(h, h)
    assert (mu, s, f) == (0.0, -1.0, 13.0)


def test_capacity_linear_in_area():
    h = 1.0
    for z in [0.0, 0.1, 0.3, 0.7, 1.0]:
        mu, s, f = local_state(z, h)
        assert abs(f - (13.0 + 8.0 * area_fraction(z, h))) < 1e-12


def test_area_fraction_rejects_out_of_range():
    with pytest.raises(ValueError):
        area_fraction(-0.1, 1.0)
    with pytest.raises(ValueError):
        area_fraction(1.1, 1.0)


# ---------------------------------------------------------------------------
# Theorem 1 and corollaries
# ---------------------------------------------------------------------------

def test_theorem_1_fraction():
    assert abs(FIELD_ORIGIN_FRACTION - 0.2928932188134524) < 1e-15


@pytest.mark.parametrize("h", [1.0, 146.7, 5776.0, 1e6])
def test_field_origin_is_half_area_and_s_zero_at_any_scale(h):
    z = local_field_origin_height(h)
    mu, s, f = local_state(z, h)
    assert abs(mu - 0.5) < 1e-12
    assert abs(s) < 1e-12
    assert abs(f - 17.0) < 1e-12
    assert abs(z / h - FIELD_ORIGIN_FRACTION) < 1e-15   # Corollary 2


def test_vertical_section_reading_agrees():
    """Corollary 1: the triangle above z* has half the vertical-section area."""
    h, base = 5776.0, 9068.8
    z = local_field_origin_height(h)
    full = 0.5 * base * h
    above = 0.5 * (base * (1 - z / h)) * (h - z)
    assert abs(above / full - 0.5) < 1e-12


def test_volumetric_alternative_is_distinct():
    assert abs(VOLUMETRIC_FRACTION - (1 - 2 ** (-1 / 3))) < 1e-15
    assert VOLUMETRIC_FRACTION < FIELD_ORIGIN_FRACTION - 0.08
    h = PETRIE_HEIGHT_IN
    z_vol = volumetric_balance_height(h)
    vol_above = (1 - z_vol / h) ** 3
    assert abs(vol_above - 0.5) < 1e-12


# ---------------------------------------------------------------------------
# Comparison with the Great Pyramid
# ---------------------------------------------------------------------------

def test_prediction_matches_petrie_half_area_level():
    z = local_field_origin_height(PETRIE_HEIGHT_IN)
    assert abs(z - PETRIE_HALF_AREA_LEVEL_IN) < PETRIE_HALF_AREA_ERR_IN


def test_kings_chamber_floor_on_local_field_origin():
    c = great_pyramid_comparison()
    lo, hi = PETRIE_KC_FLOOR_RANGE_IN
    assert lo <= c.measured_in <= hi
    assert abs(c.sigma) < 1.0
    assert abs(c.difference_in) < 3.0


def test_cubit_values():
    c = great_pyramid_comparison()
    assert abs(PETRIE_HEIGHT_IN / ROYAL_CUBIT_IN - 280.0) < 0.1
    assert abs(c.predicted_cubits - 82.0) < 0.1
    assert abs(c.measured_cubits - 82.0) < 0.1


def test_measured_fraction():
    c = great_pyramid_comparison()
    assert abs(c.measured_fraction - FIELD_ORIGIN_FRACTION) < 5e-4
