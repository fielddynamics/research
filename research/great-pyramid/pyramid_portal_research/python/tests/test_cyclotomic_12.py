"""
test_cyclotomic_12.py
=======================

Tests for the cyclotomic-12 unification A_3^Ω ≅ Z[ζ_{12}].

Canonical source: 99_appendices/J_closure_algebra_advancement.md
"""

import unittest
import numpy as np
from fractions import Fraction

from python.cyclotomic_12 import (
    # Z[ζ_{12}] abstract ring
    z12, z12_add, z12_sub, z12_mul, z12_pow, z12_one, z12_zeta,
    phi_12_at, verify_minimal_polynomial, verify_powers_of_zeta,
    # Cl(3, 0) embedding
    cl_3_0_mul, cl_basis_1, cl_basis_T1, cl_basis_T2, cl_basis_I,
    closure_fixed_subalgebra_multiplication_table,
    verify_closure_fixed_multiplication_table,
    # ζ_{12} in Clifford
    zeta_12_in_clifford, cl_pow, verify_zeta_12_powers_in_clifford,
    # Galois action
    galois_units_mod_12, galois_action_on_zeta,
    quadratic_subfield_fixed_points, parity_tag_to_subfield,
    verify_galois_group_structure,
    # Subrings
    gaussian_imaginary_unit_as_zeta, eisenstein_omega_as_zeta,
    verify_gaussian_in_zeta12, verify_eisenstein_in_zeta12,
    # Compositum-12
    divisors_above_two_of_12, divisors_above_two_of_2D,
    phi_n_value_extended, compositum_12_closure_tower,
    # Sweep on Ω-fixed
    omega_action_on_clifford, is_omega_fixed,
    sweep_multiplication_on_omega_fixed,
    # Showcase
    showcase_cyclotomic_12,
)


# ===========================================================================
# Z[ζ_{12}] as abstract ring
# ===========================================================================

class TestZ12RingArithmetic(unittest.TestCase):

    def test_addition(self):
        a = z12(1, 2, 3, 4)
        b = z12(5, 6, 7, 8)
        self.assertEqual(z12_add(a, b), z12(6, 8, 10, 12))

    def test_multiplication_identity(self):
        a = z12(2, 3, 4, 5)
        self.assertEqual(z12_mul(a, z12_one()), a)

    def test_zeta_squared(self):
        # ζ² = (0, 0, 1, 0)
        zeta = z12_zeta()
        z2 = z12_mul(zeta, zeta)
        self.assertEqual(z2, z12(0, 0, 1, 0))

    def test_zeta_cubed(self):
        # ζ³ = (0, 0, 0, 1)
        zeta = z12_zeta()
        z3 = z12_pow(zeta, 3)
        self.assertEqual(z3, z12(0, 0, 0, 1))

    def test_zeta_fourth(self):
        # ζ⁴ = ζ² - 1 = (-1, 0, 1, 0)
        zeta = z12_zeta()
        z4 = z12_pow(zeta, 4)
        self.assertEqual(z4, z12(-1, 0, 1, 0))

    def test_zeta_sixth_is_minus_one(self):
        zeta = z12_zeta()
        z6 = z12_pow(zeta, 6)
        self.assertEqual(z6, z12(-1, 0, 0, 0))

    def test_zeta_twelfth_is_one(self):
        zeta = z12_zeta()
        z12_val = z12_pow(zeta, 12)
        self.assertEqual(z12_val, z12_one())


# ===========================================================================
# Minimal polynomial Φ_{12}(ζ) = 0
# ===========================================================================

class TestMinimalPolynomial(unittest.TestCase):

    def test_phi_12_at_zeta_is_zero(self):
        result = verify_minimal_polynomial()
        self.assertTrue(result["is_zero"])

    def test_phi_12_formula(self):
        # Direct: ζ⁴ - ζ² + 1 = (-1, 0, 1, 0) - (0, 0, 1, 0) + (1, 0, 0, 0) = (0, 0, 0, 0)
        z4 = z12(-1, 0, 1, 0)
        z2 = z12(0, 0, 1, 0)
        one = z12(1, 0, 0, 0)
        diff = z12_sub(z4, z2)
        result = z12_add(diff, one)
        self.assertEqual(result, z12(0, 0, 0, 0))


# ===========================================================================
# Cl(3, 0) embedding: multiplication table on {1, T_1, T_2, I}
# ===========================================================================

class TestClosureFixedMultiplicationTable(unittest.TestCase):
    """The canonical multiplication table T_1² = 3, T_2² = -3, T_1 T_2 = 3I, etc."""

    def test_T1_squared_is_3(self):
        T1 = cl_basis_T1()
        one = cl_basis_1()
        product = cl_3_0_mul(T1, T1)
        np.testing.assert_array_almost_equal(product, 3 * one)

    def test_T2_squared_is_minus_3(self):
        T2 = cl_basis_T2()
        one = cl_basis_1()
        product = cl_3_0_mul(T2, T2)
        np.testing.assert_array_almost_equal(product, -3 * one)

    def test_T1_T2_equals_3I(self):
        T1 = cl_basis_T1()
        T2 = cl_basis_T2()
        I = cl_basis_I()
        product = cl_3_0_mul(T1, T2)
        np.testing.assert_array_almost_equal(product, 3 * I)

    def test_I_squared_is_minus_1(self):
        I = cl_basis_I()
        one = cl_basis_1()
        product = cl_3_0_mul(I, I)
        np.testing.assert_array_almost_equal(product, -1 * one)

    def test_I_T1_equals_T2(self):
        I = cl_basis_I()
        T1 = cl_basis_T1()
        T2 = cl_basis_T2()
        product = cl_3_0_mul(I, T1)
        np.testing.assert_array_almost_equal(product, T2)

    def test_I_T2_equals_minus_T1(self):
        I = cl_basis_I()
        T1 = cl_basis_T1()
        T2 = cl_basis_T2()
        product = cl_3_0_mul(I, T2)
        np.testing.assert_array_almost_equal(product, -T1)

    def test_full_table_check(self):
        result = verify_closure_fixed_multiplication_table()
        for key, val in result.items():
            self.assertTrue(val, msg=f"{key} failed")


# ===========================================================================
# ζ_{12} = (T_1 + I) / 2 — embedding into Cl(3, 0)
# ===========================================================================

class TestZeta12InClifford(unittest.TestCase):

    def test_zeta_definition(self):
        zeta = zeta_12_in_clifford()
        T1 = cl_basis_T1()
        I = cl_basis_I()
        expected = 0.5 * (T1 + I)
        np.testing.assert_array_almost_equal(zeta, expected)

    def test_zeta_cubed_equals_I_in_clifford(self):
        zeta = zeta_12_in_clifford()
        z3 = cl_pow(zeta, 3)
        I = cl_basis_I()
        np.testing.assert_array_almost_equal(z3, I)

    def test_zeta_sixth_equals_minus_one_in_clifford(self):
        zeta = zeta_12_in_clifford()
        z6 = cl_pow(zeta, 6)
        one = cl_basis_1()
        np.testing.assert_array_almost_equal(z6, -one)

    def test_zeta_twelfth_equals_one_in_clifford(self):
        zeta = zeta_12_in_clifford()
        z12_val = cl_pow(zeta, 12)
        one = cl_basis_1()
        np.testing.assert_array_almost_equal(z12_val, one)

    def test_phi_12_at_zeta_in_clifford_is_zero(self):
        result = verify_zeta_12_powers_in_clifford()
        self.assertTrue(result["phi_12_at_zeta_is_zero"])

    def test_all_canonical_powers(self):
        result = verify_zeta_12_powers_in_clifford()
        for key in ("zeta_squared_equals_half_1_plus_T2",
                    "zeta_cubed_equals_I",
                    "zeta_fourth_equals_half_minus_1_plus_T2",
                    "zeta_sixth_equals_minus_one",
                    "zeta_twelfth_equals_one"):
            self.assertTrue(result[key], msg=f"{key} failed")


# ===========================================================================
# Galois group (Z/12)* = V_4
# ===========================================================================

class TestGaloisGroup(unittest.TestCase):

    def test_units_are_1_5_7_11(self):
        units = galois_units_mod_12()
        self.assertEqual(sorted(units), [1, 5, 7, 11])

    def test_all_non_identity_have_order_2(self):
        result = verify_galois_group_structure()
        for a, o in result["orders"].items():
            if a == 1:
                self.assertEqual(o, 1)
            else:
                self.assertEqual(o, 2, msg=f"element {a} has order {o}")

    def test_klein_4_structure(self):
        result = verify_galois_group_structure()
        self.assertTrue(result["all_non_identity_order_2"])
        self.assertTrue(result["size_4"])

    def test_galois_action_sigma_a_is_zeta_a(self):
        # σ_a(ζ) = ζ^a for each unit a
        for a in galois_units_mod_12():
            action = galois_action_on_zeta(a)
            zeta_a = z12_pow(z12_zeta(), a)
            self.assertEqual(action, zeta_a)

    def test_three_quadratic_subfields_documented(self):
        subfields = quadratic_subfield_fixed_points()
        self.assertEqual(set(subfields.keys()), {5, 7, 11})

    def test_parity_tag_map(self):
        parities = parity_tag_to_subfield()
        self.assertEqual(set(parities.keys()), {-1, 0, +1})


# ===========================================================================
# Z[i] and Z[ω] as subrings
# ===========================================================================

class TestSubringsOfZ12(unittest.TestCase):

    def test_i_is_zeta_cubed(self):
        i_elem = gaussian_imaginary_unit_as_zeta()
        self.assertEqual(i_elem, z12(0, 0, 0, 1))

    def test_i_squared_is_minus_1(self):
        result = verify_gaussian_in_zeta12()
        self.assertTrue(result["i_squared_is_minus_1"])

    def test_omega_is_zeta_fourth(self):
        omega = eisenstein_omega_as_zeta()
        self.assertEqual(omega, z12(-1, 0, 1, 0))

    def test_omega_satisfies_minimal_poly(self):
        result = verify_eisenstein_in_zeta12()
        self.assertTrue(result["minimal_poly_holds"])

    def test_subrings_are_distinct(self):
        # Z[i] and Z[ω] sit inside Z[ζ_{12}] but are different subrings
        i_elem = gaussian_imaginary_unit_as_zeta()
        omega = eisenstein_omega_as_zeta()
        self.assertNotEqual(i_elem, omega)


# ===========================================================================
# Compositum-12 closure tower
# ===========================================================================

class TestCompositum12ClosureTower(unittest.TestCase):

    def test_phi_8_at_K4_is_257(self):
        # Fermat prime 257 = 2^8 + 1
        self.assertEqual(phi_n_value_extended(8, 4), 257)

    def test_phi_12_at_K4_is_241(self):
        # 241 is prime, 241 ≡ 1 mod 12
        self.assertEqual(phi_n_value_extended(12, 4), 241)
        # Verify primality:
        self.assertTrue(all(241 % p != 0 for p in (2, 3, 5, 7, 11, 13)))

    def test_primary_trio_is_13_17_21(self):
        result = compositum_12_closure_tower(4)
        self.assertEqual(result["primary_trio"], (13, 17, 21))

    def test_full_compositum_contains_13_17_21_257_241(self):
        result = compositum_12_closure_tower(4)
        values = [v for _, v in result["full_compositum_12_factors"]]
        for n in (13, 17, 21, 257, 241):
            self.assertIn(n, values)

    def test_full_compositum_product(self):
        # 21 * 17 * 13 * 257 * 241 = 287449617
        result = compositum_12_closure_tower(4)
        self.assertEqual(result["full_compositum_12_product"], 21 * 17 * 13 * 257 * 241)


# ===========================================================================
# Sweep multiplication on the Ω-fixed subalgebra
# ===========================================================================

class TestSweepOnOmegaFixed(unittest.TestCase):

    def test_sweep_on_scalar_is_ordinary_product(self):
        # 1 ⋆ 1 = 1
        one = cl_basis_1()
        product = sweep_multiplication_on_omega_fixed(one, one)
        np.testing.assert_array_almost_equal(product, one)

    def test_sweep_on_pseudoscalar(self):
        # I ⋆ I = I² = -1 (Ω-fixed; sweep = Clifford product)
        I = cl_basis_I()
        one = cl_basis_1()
        product = sweep_multiplication_on_omega_fixed(I, I)
        np.testing.assert_array_almost_equal(product, -one)


# ===========================================================================
# Showcase
# ===========================================================================

class TestShowcase(unittest.TestCase):

    def test_showcase_returns_lines(self):
        out = showcase_cyclotomic_12()
        self.assertIsInstance(out, list)
        self.assertGreater(len(out), 30)

    def test_showcase_mentions_canonical_results(self):
        joined = "\n".join(showcase_cyclotomic_12())
        for token in ("ζ_{12}", "T_1", "T_2", "Φ_{12}",
                      "Klein 4-group", "Z[i]", "Z[ω]", "(13, 17, 21)"):
            self.assertIn(token, joined, msg=f"missing: {token}")
