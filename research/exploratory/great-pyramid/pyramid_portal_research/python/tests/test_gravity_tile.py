"""Tests for gravity_tile.py — the electron-as-vortex framework."""

import math
import pytest

from python.gravity_tile import (
    DIM_LAMBDA_K_V, DIM_PI_V, DIM_V_TENSOR_V,
    DIM_T_4, DIM_E_4, SDIM_T_4,
    PHI_3_K4, PHI_4_K4, PHI_6_K4,
    tile_decomposition,
    ElectronVortex, positron_charge,
    alpha_gravity_tree, electron_vortex_depth,
    pyramid_encodes_gravity_tile,
    showcase_gravity_tile,
)


# ---------------------------------------------------------------------------
# Tile dimensions
# ---------------------------------------------------------------------------

def test_dim_Lambda_K_V_is_1_at_K_4():
    """dim Λ^K V = 1 at K=4 (orientation cap is one-dimensional)."""
    assert DIM_LAMBDA_K_V == 1


def test_dim_Pi_V_is_4():
    """dim ΠV = 4 (parity-odd frame channel for K=4)."""
    assert DIM_PI_V == 4


def test_dim_V_tensor_V_is_16_at_K_4():
    """dim V⊗V = 16 at K=4 (ordered bilinear metric = K²)."""
    assert DIM_V_TENSOR_V == 16


def test_dim_T_4_is_21():
    """dim T_4 = 1 + 4 + 16 = 21."""
    assert DIM_T_4 == 21
    assert DIM_T_4 == DIM_LAMBDA_K_V + DIM_PI_V + DIM_V_TENSOR_V


def test_dim_E_4_is_17():
    """dim E_4 = dim Λ^4 V + dim V⊗V = 17 (even sector)."""
    assert DIM_E_4 == 17
    assert DIM_E_4 == DIM_LAMBDA_K_V + DIM_V_TENSOR_V


def test_sdim_T_4_is_13():
    """sdim T_4 = dim E_4 − dim ΠV = 13 (superdimension)."""
    assert SDIM_T_4 == 13
    assert SDIM_T_4 == DIM_E_4 - DIM_PI_V


# ---------------------------------------------------------------------------
# Cyclotomic / tile equivalence — the K=4 trio
# ---------------------------------------------------------------------------

def test_dim_T_4_equals_phi_3_K_4():
    """dim T_4 = 21 = Φ_3(K=4) = 1 + K + K²."""
    assert DIM_T_4 == PHI_3_K4
    assert DIM_T_4 == 1 + 4 + 4**2


def test_dim_E_4_equals_phi_4_K_4():
    """dim E_4 = 17 = Φ_4(K=4) = 1 + K²."""
    assert DIM_E_4 == PHI_4_K4
    assert DIM_E_4 == 1 + 4**2


def test_sdim_T_4_equals_phi_6_K_4():
    """sdim T_4 = 13 = Φ_6(K=4) = 1 − K + K²."""
    assert SDIM_T_4 == PHI_6_K4
    assert SDIM_T_4 == 1 - 4 + 4**2


def test_K4_trio_is_tile_decomposition():
    """The K=4 primary trio {13, 17, 21} equals the gravity tile decomposition."""
    t = tile_decomposition()
    assert t["K4_trio_is_tile_decomposition"]
    assert t["dim_T_4_equals_PHI_3"]
    assert t["dim_E_4_equals_PHI_4"]
    assert t["sdim_T_4_equals_PHI_6"]


# ---------------------------------------------------------------------------
# Electron vortex algebra
# ---------------------------------------------------------------------------

def test_electron_vortex_default_charge_minus_1():
    e = ElectronVortex()
    assert e.charge == -1


def test_electron_vortex_satisfies_D_3():
    e = ElectronVortex()
    assert e.is_dihedral_D_3()
    assert e.vortex_closure == 3
    assert e.parity_squared == 1
    assert e.group_order == 6


def test_positron_inverse_charge():
    """Positron charge = +1 (inverse vortex circulation)."""
    assert positron_charge(electron_charge=-1) == +1


# ---------------------------------------------------------------------------
# Gravity coupling α_G^tree = α^21 · 17/13
# ---------------------------------------------------------------------------

def test_alpha_G_tree_exponent_is_dim_T_4():
    """The α exponent in gravity coupling = dim T_4 = 21."""
    g = alpha_gravity_tree(1.0/137.036)
    # α^21 verified by reconstructing
    alpha = 1.0/137.036
    assert abs(g["coulomb_attenuation_alpha_to_21"] - alpha**21) < 1e-60


def test_alpha_G_tree_parity_factor_is_17_over_13():
    """The parity factor in α_G^tree = 17/13 = dim E_4 / sdim T_4."""
    g = alpha_gravity_tree()
    assert abs(g["parity_normalization_17_over_13"] - 17.0/13.0) < 1e-12


def test_alpha_G_tree_full_formula():
    """α_G^tree = α^21 · 17/13."""
    alpha = 1.0/137.036
    g = alpha_gravity_tree(alpha)
    expected = alpha**21 * 17.0/13.0
    assert abs(g["alpha_G_tree"] - expected) < 1e-60


def test_alpha_G_tree_order_of_magnitude():
    """α_G^tree ~ 10^-45 at framework α (correct order for gravitational coupling)."""
    g = alpha_gravity_tree()
    assert -46.0 < g["log10_alpha_G_tree"] < -44.0


def test_alpha_G_full_with_g_e_correction():
    """Full α_G = α^21 · 17/13 · g_e/2 predicts measured G to within 20 ppm."""
    from python.gravity_tile import alpha_gravity_full
    f = alpha_gravity_full()
    assert abs(f["deviation_ppm"]) < 20.0


def test_alpha_G_full_g_e_over_2_value():
    """g_e/2 = 1.001159652 (CODATA, electron g-factor anomaly)."""
    from python.gravity_tile import G_E_OVER_2, alpha_gravity_full
    f = alpha_gravity_full()
    assert abs(G_E_OVER_2 - 1.001159652) < 1e-9
    assert abs(f["g_e_over_2"] - G_E_OVER_2) < 1e-15


def test_alpha_G_full_versus_tree():
    """Full prediction is g_e/2 times tree prediction."""
    from python.gravity_tile import alpha_gravity_full
    f = alpha_gravity_full()
    assert abs(f["alpha_G_full"] / f["alpha_G_tree"] - f["g_e_over_2"]) < 1e-12


# ---------------------------------------------------------------------------
# Electron vortex depth d_e
# ---------------------------------------------------------------------------

def test_vortex_depth_integer_part_is_21():
    """Integer part of vortex depth = dim T_4 = 21."""
    d = electron_vortex_depth()
    assert d["integer_depth_dim_T_4"] == 21


def test_vortex_depth_just_above_21():
    """d_e = 21 + small parity correction; sits between 21.0 and 21.1 at framework α."""
    d = electron_vortex_depth()
    assert 21.0 < d["electron_vortex_depth"] < 21.1


def test_vortex_depth_parity_correction_negative_log():
    """The parity correction is small negative (since 17/13 > 1 and α < 1)."""
    d = electron_vortex_depth()
    # log_α(17/13) < 0 (because α < 1 and 17/13 > 1)
    assert d["parity_correction_log_alpha_17_13"] < 0


# ---------------------------------------------------------------------------
# Pyramid → gravity tile encoding (synthesis)
# ---------------------------------------------------------------------------

def test_khufu_KC_freq_contains_dim_T_4():
    """Khufu KC freq 47 Hz = 21 + 26 = dim T_4 + Φ_4(K=5)."""
    p = pyramid_encodes_gravity_tile()
    assert p["khufu_KC_freq"] == 47
    assert p["tile_dim_21"] == 21
    assert p["khufu_contains_dim_T_4"]


def test_khafre_alpha_int_uses_dim_E_4():
    """Khafre base / D = 137 = (dim E_4)·SO_v + 1."""
    p = pyramid_encodes_gravity_tile()
    assert p["khafre_base_over_D"] == 137
    assert p["dim_E_4_17"] == 17
    # 17 · 8 + 1 = 137
    assert 17 * 8 + 1 == p["khafre_base_over_D"]


def test_parallel_identity_uses_sdim_squared():
    """Φ_3·SO_v + 1 = 169 = (sdim T_4)² = Φ_6²."""
    p = pyramid_encodes_gravity_tile()
    assert p["phi_3_SOv_plus_1"] == 169
    assert p["sdim_T_4_13"] == 13
    assert p["parallel_identity_169_equals_sdim_squared"]
    assert 13 ** 2 == 169


# ---------------------------------------------------------------------------
# Showcase
# ---------------------------------------------------------------------------

def test_showcase_runs_and_contains_keywords():
    out = showcase_gravity_tile()
    text = "\n".join(out)
    assert "GRAVITY TILE" in text
    assert "VORTEX" in text or "vortex" in text
    assert "D_3" in text
    assert "α_G" in text or "α^21" in text
    assert "Khufu" in text and "Khafre" in text
    assert "21" in text and "17" in text and "13" in text
