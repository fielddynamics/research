"""
test_unification_algebra_core.py
==================================

Tests for the *core constructive* theorems R1-R7 from appendix G Part III.

These complement test_unification_algebra.py which tests the eight
uniqueness theorems T1-T8.  The R-block tests the algebra's actual
operations:

  R2 — orientation cocycle sigma -> Clifford relations
  R3 — closure operator Omega: e_1 -> e_2 -> e_3, with Omega^3 = id
  R4 — A_3 = <1, I> + Z[omega]^3 decomposition under Omega
  R5 — coupling polynomial as norm trace on Z[i] and Z[omega]
  R6 — S(D, K) divisor formula = product Phi_d(K) for d | 2D, d > 2
  R7 — Cl(3, 0) grade decomposition matches {1, 3, 3, 1}

Plus the worked example: a 3-bit Boolean function as closure-algebra element.
"""

import unittest

from python.unification_algebra import (
    # R2 — orientation cocycle
    orientation_cocycle, twisted_product, clifford_relations_check_3,
    # R3 — closure operator
    omega_permute_mask, omega_order_check, omega_fixed_masks, omega_cycled_masks,
    # R4 — decomposition
    omega_decomposition_check,
    # R5 — imaginary-quadratic norms
    gaussian_norm_Z_i, eisenstein_norm_Z_omega,
    coupling_polynomial_as_norm_trace_check,
    # R6 — divisor formula for S(D, K)
    divisors_above_two, cyclotomic_value_for_divisor, S_D_K_divisor_formula,
    # R7 — Cl(3, 0) grade decomposition
    cl_3_0_grade_dimensions, cl_3_0_grade_check,
    # Worked example
    ClosureAlgebraReading, boolean_function_through_pipeline,
    # Audit
    showcase_core_constructive_theorems,
)


# ===========================================================================
# R2 — Orientation cocycle and Clifford relations
# ===========================================================================

class TestR2OrientationCocycle(unittest.TestCase):
    """Verify the cocycle sigma(a, b) = (-1)^{sum a_i b_j with i > j}."""

    def test_cocycle_at_zero_is_one(self):
        # sigma(0, anything) = +1 because the exponent sum is empty
        for b in range(8):
            self.assertEqual(orientation_cocycle(0, b), 1)

    def test_cocycle_at_e1_e1_is_plus_one(self):
        # e_1 * e_1: the exponent sum involves a_2 b_1 + a_3 b_1 + a_3 b_2.
        # With a = b = 1 (bit 0 set only), all higher bits are 0, so sum = 0.
        self.assertEqual(orientation_cocycle(1, 1), 1)

    def test_cocycle_e2_e1_is_minus_one(self):
        # a = 2 (bit 1), b = 1 (bit 0): exponent has a_1 b_0 = 1 * 1 = 1
        self.assertEqual(orientation_cocycle(2, 1), -1)

    def test_cocycle_e1_e2_is_plus_one(self):
        # a = 1 (bit 0), b = 2 (bit 1): exponent has a_0 b_1 ... wait, that's
        # i > j, so we need bit i of a times bit j of b with i > j.
        # a = 1 has only bit 0 set, so a_i = 0 for i >= 1.  Sum = 0.
        self.assertEqual(orientation_cocycle(1, 2), 1)


class TestTwistedProduct(unittest.TestCase):

    def test_e_i_squared_gives_identity_mask(self):
        for g in (1, 2, 4):
            sign, mask = twisted_product(g, g)
            self.assertEqual(mask, 0, msg=f"e_{g}^2 should have mask 0")
            self.assertEqual(sign, 1, msg=f"e_{g}^2 should give +1")

    def test_e_1_times_e_2_gives_mask_3(self):
        sign, mask = twisted_product(1, 2)
        self.assertEqual(mask, 3)        # 1 XOR 2 = 3 = e_{12}
        self.assertEqual(sign, 1)

    def test_e_2_times_e_1_gives_minus_mask_3(self):
        sign, mask = twisted_product(2, 1)
        self.assertEqual(mask, 3)
        self.assertEqual(sign, -1)


class TestCliffordRelationsCheck(unittest.TestCase):
    """The combined Clifford-relations verification."""

    def test_clifford_relations_all_pass(self):
        result = clifford_relations_check_3()
        self.assertTrue(result["all_pass"])

    def test_all_three_generators_square_to_plus_one(self):
        result = clifford_relations_check_3()
        for v in result["squares_to_plus_one"].values():
            self.assertTrue(v)

    def test_all_three_pairs_anticommute(self):
        result = clifford_relations_check_3()
        # Three unordered pairs of generators: (1,2), (1,4), (2,4)
        self.assertEqual(len(result["anticommutation"]), 3)
        for v in result["anticommutation"].values():
            self.assertTrue(v)


# ===========================================================================
# R3 — Closure operator Omega
# ===========================================================================

class TestR3OmegaPermutation(unittest.TestCase):
    """Omega cyclically permutes generators e_1 -> e_2 -> e_3."""

    def test_omega_fixes_scalar(self):
        self.assertEqual(omega_permute_mask(0), 0)

    def test_omega_fixes_pseudoscalar_I(self):
        self.assertEqual(omega_permute_mask(7), 7)

    def test_omega_cycles_e1_e2_e3(self):
        # e_1 (mask 1) -> e_2 (mask 2) -> e_3 (mask 4) -> e_1
        self.assertEqual(omega_permute_mask(1), 2)
        self.assertEqual(omega_permute_mask(2), 4)
        self.assertEqual(omega_permute_mask(4), 1)

    def test_omega_cycles_bivectors(self):
        # e_12 (mask 3) cycles
        # Under e_1 -> e_2, e_2 -> e_3, e_3 -> e_1:
        # e_12 -> e_23 (mask 6)
        # e_23 -> e_13 wait carefully... let's just check via the permute
        self.assertEqual(omega_permute_mask(3), 6)
        self.assertEqual(omega_permute_mask(6), 5)
        self.assertEqual(omega_permute_mask(5), 3)

    def test_omega_cubed_is_identity(self):
        result = omega_order_check()
        self.assertTrue(result["all_return_after_3_iterations"])
        self.assertEqual(result["failures"], [])

    def test_fixed_masks_are_scalar_and_pseudoscalar(self):
        fixed = omega_fixed_masks()
        self.assertEqual(sorted(fixed), [0, 7])

    def test_two_cycled_orbits_of_length_3(self):
        orbits = omega_cycled_masks()
        self.assertEqual(len(orbits), 2)
        for orb in orbits:
            self.assertEqual(len(orb), 3)


# ===========================================================================
# R4 — Decomposition A_3 = <1, I> + Z[omega]^3
# ===========================================================================

class TestR4Decomposition(unittest.TestCase):

    def test_axial_dimension_is_2(self):
        result = omega_decomposition_check()
        self.assertEqual(result["fixed_dimension"], 2)
        self.assertTrue(result["axial_dim_equals_2"])

    def test_middle_dimension_is_6(self):
        result = omega_decomposition_check()
        self.assertEqual(result["cycled_dimension"], 6)
        self.assertTrue(result["middle_dim_equals_6"])

    def test_total_matches_Cl_3_0(self):
        result = omega_decomposition_check()
        self.assertEqual(result["total_dimension"], 8)
        self.assertTrue(result["matches_Cl_3_0"])

    def test_two_Eisenstein_orbits_correspond_to_vectors_and_bivectors(self):
        # The two length-3 orbits: vectors {e_1, e_2, e_3} and
        # bivectors {e_12, e_23, e_13}.
        result = omega_decomposition_check()
        orbits = result["cycled_orbits"]
        all_masks_in_orbits = sorted([m for orb in orbits for m in orb])
        self.assertEqual(all_masks_in_orbits, [1, 2, 3, 4, 5, 6])


# ===========================================================================
# R5 — Coupling polynomial as norm trace
# ===========================================================================

class TestR5NormTrace(unittest.TestCase):

    def test_gaussian_norm_K_minus_i_at_K4(self):
        # N_{Z[i]/Z}(4 - i) = 16 + 1 = 17 = Phi_4(4) = f(4, 0)
        self.assertEqual(gaussian_norm_Z_i(4, -1), 17)

    def test_eisenstein_norm_K_minus_omega_at_K4(self):
        # N_{Z[omega]/Z}(4 - omega) = 16 + 4 + 1 = 21 = Phi_3(4) = f(4, +1)
        self.assertEqual(eisenstein_norm_Z_omega(4, -1), 21)

    def test_eisenstein_norm_K_plus_omega_at_K4(self):
        # N_{Z[omega]/Z}(4 + omega) = 16 - 4 + 1 = 13 = Phi_6(4) = f(4, -1)
        self.assertEqual(eisenstein_norm_Z_omega(4, +1), 13)

    def test_norm_trace_full_check_at_K4(self):
        result = coupling_polynomial_as_norm_trace_check(4)
        self.assertTrue(result["all_match"])

    def test_norm_trace_across_general_K(self):
        for K in (2, 3, 4, 5, 7, 10, 16):
            result = coupling_polynomial_as_norm_trace_check(K)
            self.assertTrue(result["all_match"],
                            msg=f"norm trace failed at K={K}: {result}")

    def test_eisenstein_norm_formula(self):
        # N(a + b*omega) = a^2 - a*b + b^2
        # Spot-check at a few values
        self.assertEqual(eisenstein_norm_Z_omega(0, 0), 0)
        self.assertEqual(eisenstein_norm_Z_omega(1, 0), 1)
        self.assertEqual(eisenstein_norm_Z_omega(0, 1), 1)
        self.assertEqual(eisenstein_norm_Z_omega(1, 1), 1)    # 1 - 1 + 1
        self.assertEqual(eisenstein_norm_Z_omega(2, 1), 3)    # 4 - 2 + 1
        self.assertEqual(eisenstein_norm_Z_omega(3, 1), 7)    # 9 - 3 + 1


# ===========================================================================
# R6 — Divisor formula for S(D, K)
# ===========================================================================

class TestR6DivisorFormula(unittest.TestCase):

    def test_divisors_above_two_of_4(self):
        # Divisors of 4 above 2: {4}
        self.assertEqual(divisors_above_two(4), [4])

    def test_divisors_above_two_of_6(self):
        # Divisors of 6 above 2: {3, 6}
        self.assertEqual(divisors_above_two(6), [3, 6])

    def test_divisors_above_two_of_8(self):
        # Divisors of 8 above 2: {4, 8}
        self.assertEqual(divisors_above_two(8), [4, 8])

    def test_S_2_K4_equals_17(self):
        r = S_D_K_divisor_formula(2, 4)
        self.assertEqual(r["product"], 17)
        self.assertTrue(r["matches_sierpinski_S"])

    def test_S_3_K4_equals_273(self):
        r = S_D_K_divisor_formula(3, 4)
        self.assertEqual(r["product"], 273)
        self.assertTrue(r["matches_sierpinski_S"])

    def test_S_4_K4_equals_4369(self):
        # S(4, 4) = Phi_4(4) * Phi_8(4) = 17 * 257 = 4369
        r = S_D_K_divisor_formula(4, 4)
        self.assertEqual(r["product"], 17 * 257)
        self.assertEqual(r["product"], 4369)

    def test_factor_breakdown_for_D3(self):
        r = S_D_K_divisor_formula(3, 4)
        names = [name for name, _ in r["factor_breakdown"]]
        self.assertIn("Phi_3(4)", names)
        self.assertIn("Phi_6(4)", names)

    def test_S_D_K_consistency_across_K(self):
        for D in (2, 3):
            for K in (3, 4, 5, 7):
                r = S_D_K_divisor_formula(D, K)
                self.assertTrue(r["matches_sierpinski_S"],
                                msg=f"S({D},{K}) mismatch: {r}")


# ===========================================================================
# R7 — Cl(3, 0) grade decomposition
# ===========================================================================

class TestR7Cl30GradeDecomposition(unittest.TestCase):

    def test_grade_dimensions_are_1_3_3_1(self):
        dims = cl_3_0_grade_dimensions()
        self.assertEqual(dims, {0: 1, 1: 3, 2: 3, 3: 1})

    def test_grade_check_returns_correct_tuple(self):
        result = cl_3_0_grade_check()
        self.assertEqual(result["tuple"], (1, 3, 3, 1))
        self.assertTrue(result["matches_1_3_3_1"])

    def test_total_dimension_is_8(self):
        dims = cl_3_0_grade_dimensions()
        self.assertEqual(sum(dims.values()), 8)

    def test_grade_decomposition_matches_T2_eigenspectrum(self):
        # The {1, 3, 3, 1} from R7 matches the {1, D, D, 1} from T2 at D=3
        from python.unification_algebra import expected_eigenspectrum_multiplicities
        spec = expected_eigenspectrum_multiplicities(3)
        result = cl_3_0_grade_check()
        self.assertEqual(spec, result["tuple"])


# ===========================================================================
# Worked example: a 3-bit Boolean function through the pipeline
# ===========================================================================

class TestWorkedExample(unittest.TestCase):

    def test_pipeline_returns_reading_dataclass(self):
        # AND gate truth table on three bits: f = +1 iff all three bits are
        # +1 (i.e. mask = 0b111 = 7); otherwise -1.
        # Truth table in mask order 0..7: (-, -, -, -, -, -, -, +)
        tt = [-1, -1, -1, -1, -1, -1, -1, +1]
        reading = boolean_function_through_pipeline(tt)
        self.assertIsInstance(reading, ClosureAlgebraReading)
        self.assertEqual(reading.truth_table, tuple(tt))

    def test_pipeline_returns_8_walsh_coefficients(self):
        tt = [+1, +1, -1, +1, -1, +1, +1, -1]
        reading = boolean_function_through_pipeline(tt)
        self.assertEqual(len(reading.walsh_coefficients), 8)

    def test_pipeline_axial_components_are_floats(self):
        tt = [1, 1, 1, 1, 1, 1, 1, 1]
        reading = boolean_function_through_pipeline(tt)
        # All-ones truth table has only the scalar Walsh coefficient nonzero
        self.assertAlmostEqual(reading.axial_scalar, 1.0)
        self.assertAlmostEqual(reading.axial_pseudoscalar, 0.0)

    def test_pipeline_hex_channels_are_pairs(self):
        tt = [+1, -1, +1, -1, +1, -1, +1, -1]
        reading = boolean_function_through_pipeline(tt)
        self.assertEqual(len(reading.hex_z1), 2)
        self.assertEqual(len(reading.hex_z2), 2)
        self.assertEqual(len(reading.hex_z3), 2)

    def test_pipeline_closure_norm_is_real(self):
        tt = [+1, +1, -1, +1, -1, +1, +1, -1]
        reading = boolean_function_through_pipeline(tt)
        self.assertIsInstance(reading.closure_norm, float)

    def test_pipeline_rejects_wrong_length(self):
        with self.assertRaises(ValueError):
            boolean_function_through_pipeline([1, 1, 1])


# ===========================================================================
# Showcase audit
# ===========================================================================

class TestCoreShowcase(unittest.TestCase):

    def test_core_showcase_returns_lines(self):
        out = showcase_core_constructive_theorems()
        self.assertIsInstance(out, list)
        self.assertGreater(len(out), 20)

    def test_core_showcase_mentions_R2_through_R7(self):
        joined = "\n".join(showcase_core_constructive_theorems())
        for token in ("R2 — Orientation cocycle", "R3 — Closure operator",
                      "R4 — Decomposition", "R5 — Coupling polynomial",
                      "R6 — S(D, K)", "R7 — Cl(3,0)"):
            self.assertIn(token, joined, msg=f"missing: {token}")

    def test_core_showcase_mentions_worked_example(self):
        joined = "\n".join(showcase_core_constructive_theorems())
        self.assertIn("Worked example", joined)
        self.assertIn("Walsh coefficients", joined)
        self.assertIn("Closure norm", joined)
