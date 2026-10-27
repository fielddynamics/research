"""Tests for areal_closure.py — areal closure (P1) from the GFD action (01.7)."""

import math
import numpy as np
import pytest

from python.areal_closure import (
    BASE_SIDE_IN, HEIGHT_IN,
    noether_current_check, section_area,
    flux_through_section, flux_through_lateral, closure_balance,
    mu_B, odds_ratio, balance_height,
    uniform_axial, strained_axial,
)

B, H = BASE_SIDE_IN, HEIGHT_IN
ZSTAR = H * (1 - 1 / math.sqrt(2))


def test_noether_current_is_mu_grad_phi():
    pytest.importorskip("sympy")
    assert noether_current_check()


def test_section_flux_of_uniform_field_is_area():
    J = uniform_axial(2.5)
    for z in [0.0, 0.2 * H, ZSTAR, 0.8 * H]:
        assert abs(flux_through_section(J, z, B, H) - 2.5 * section_area(z, B, H)) \
            < 1e-9 * section_area(0.0, B, H)


@pytest.mark.parametrize("field", [uniform_axial(), strained_axial(eps=0.1),
                                   strained_axial(eps=-0.2)])
@pytest.mark.parametrize("frac", [0.1, 0.2929, 0.5, 0.9])
def test_divergence_theorem_closure_balance(field, frac):
    base, sec, lat, res = closure_balance(field, frac * H)
    assert abs(res) < 1e-10 * abs(base)


@pytest.mark.parametrize("frac", [0.05, 0.25, 0.5, 0.75, 0.95])
def test_P1_derived_for_uniform_axial_current(frac):
    """mu_B(z) = Phi_sec / Phi_base = A(z)/A(0): postulate P1 as a theorem."""
    z = frac * H
    assert abs(mu_B(uniform_axial(), z) - section_area(z, B, H) / section_area(0, B, H)) < 1e-12


def test_field_origin_at_z_star_for_uniform_current():
    J = uniform_axial()
    assert abs(mu_B(J, ZSTAR) - 0.5) < 1e-12
    assert abs(odds_ratio(J, ZSTAR) - 1.0) < 1e-10
    assert abs(balance_height(J) - ZSTAR) < 1e-4


def test_mu_and_omega_consistent_with_constitutive_odds():
    J = uniform_axial()
    for frac in [0.1, 0.4, 0.7]:
        m = mu_B(J, frac * H)
        assert abs(odds_ratio(J, frac * H) - m / (1 - m)) < 1e-9


def test_strained_field_is_divergence_free():
    J = strained_axial(eps=0.3)
    x, y, z = np.array([1.0, -50.0]), np.array([3.0, 20.0]), np.array([100.0, 4000.0])
    d = 1e-3
    div = ((J(x + d, y, z)[0] - J(x - d, y, z)[0])
           + (J(x, y + d, z)[1] - J(x, y - d, z)[1])
           + (J(x, y, z + d)[2] - J(x, y, z - d)[2])) / (2 * d)
    assert np.all(np.abs(div) < 1e-12)


def test_non_uniform_current_moves_balance_plane():
    """Axial non-uniformity shifts the balance plane; sign follows the gradient."""
    up = balance_height(strained_axial(eps=0.1))
    down = balance_height(strained_axial(eps=-0.1))
    assert up > ZSTAR > down


def test_uniformity_required_by_measured_floor():
    """The ~1 in agreement of 01.6 bounds the axial gradient of the driven field."""
    shift_per_eps = (balance_height(strained_axial(eps=0.01)) - ZSTAR) / 0.01
    assert 500 < shift_per_eps < 700          # ~600 in per unit fractional gradient
    eps_bound = 1.0 / shift_per_eps           # gradient giving a 1 in shift
    assert eps_bound < 0.002
