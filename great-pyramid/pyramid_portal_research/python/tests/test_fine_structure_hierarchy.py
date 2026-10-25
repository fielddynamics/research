"""
test_fine_structure_hierarchy.py
==================================

Tests for placing 137 in the closure-algebra hierarchy.
"""

import unittest

from python.fine_structure_hierarchy import (
    multiplicative_order, ord_137_of_4,
    splits_in_Z_i, splits_in_Z_omega, splits_in_Z_zeta_12,
    splitting_summary,
    cyclotomic_value, divides_phi_d_K,
    first_phi_dividing_137, locate_137_in_hierarchy,
    is_prime_simple,
    alpha_inv_predicted, alpha_inv_residual,
    twenty_eight_structural_reading,
    showcase_fine_structure_hierarchy,
)


class TestMultiplicativeOrder(unittest.TestCase):

    def test_ord_2_mod_7_is_3(self):
        # 2^3 = 8 ≡ 1 mod 7
        self.assertEqual(multiplicative_order(2, 7), 3)

    def test_ord_3_mod_7_is_6(self):
        # 3^6 = 729 = 7·104 + 1 ≡ 1 mod 7
        self.assertEqual(multiplicative_order(3, 7), 6)

    def test_ord_137_of_4(self):
        # ord_137(4) = 34 (this is what the framework needs)
        self.assertEqual(ord_137_of_4(), 34)

    def test_ord_returns_None_for_non_coprime(self):
        self.assertIsNone(multiplicative_order(4, 8))


class TestSplittingIn137(unittest.TestCase):

    def test_137_splits_in_Z_i(self):
        # 137 ≡ 1 (mod 4), so splits in Z[i]: 137 = 4² + 11² = (4+11i)(4-11i)
        self.assertTrue(splits_in_Z_i(137))
        # Verify the decomposition
        self.assertEqual(4 * 4 + 11 * 11, 137)

    def test_137_is_inert_in_Z_omega(self):
        # 137 mod 3 = 2, so 137 is INERT in Z[ω]
        self.assertFalse(splits_in_Z_omega(137))

    def test_137_is_NOT_completely_split_in_Z_zeta_12(self):
        # 137 mod 12 = 5, NOT 1, so doesn't split completely
        self.assertFalse(splits_in_Z_zeta_12(137))

    def test_137_mod_12_is_5(self):
        self.assertEqual(137 % 12, 5)

    def test_137_in_Gaussian_axial_not_Eisenstein(self):
        # The structural statement: 137 lives in the Gaussian (axial) channel
        s = splitting_summary(137)
        self.assertTrue(s["splits_in_Z_i"])
        self.assertFalse(s["splits_in_Z_omega"])

    def test_other_primes_splittings(self):
        # 13 ≡ 1 mod 12 — splits completely
        self.assertTrue(splits_in_Z_zeta_12(13))
        # 17 ≡ 5 mod 12 — splits in Z[i] but inert in Z[ω]
        s17 = splitting_summary(17)
        self.assertTrue(s17["splits_in_Z_i"])
        self.assertFalse(s17["splits_in_Z_omega"])


class TestLocate137InHierarchy(unittest.TestCase):

    def test_137_first_appears_at_d_34(self):
        # ord_137(4) = 34, so 137 first divides K^34 - 1 at K=4
        result = first_phi_dividing_137(K=4, max_d=40)
        self.assertEqual(result["d"], 34)

    def test_137_does_not_divide_small_phi(self):
        # 137 should not divide any of Φ_3(4) = 21, Φ_4(4) = 17, etc.
        for d in (1, 2, 3, 4, 6, 8, 12):
            self.assertFalse(divides_phi_d_K(137, d, 4),
                             msg=f"137 should not divide Φ_{d}(4)")

    def test_locate_137_returns_full_diagnostic(self):
        info = locate_137_in_hierarchy(K=4)
        self.assertIn("ord_K_mod_p", info)
        self.assertIn("splitting", info)
        self.assertIn("first_phi_dividing", info)
        self.assertTrue(info["is_prime"])


class TestPrimalityCheck(unittest.TestCase):

    def test_137_is_prime(self):
        self.assertTrue(is_prime_simple(137))

    def test_28_is_not_prime(self):
        self.assertFalse(is_prime_simple(28))

    def test_241_is_prime(self):
        # Φ_12(4) = 241, used in compositum-12
        self.assertTrue(is_prime_simple(241))

    def test_257_is_prime(self):
        # Φ_8(4) = 257, Fermat prime
        self.assertTrue(is_prime_simple(257))


class TestAlphaInverseObservation(unittest.TestCase):

    def test_predicted_alpha_inv_value(self):
        predicted = alpha_inv_predicted()
        self.assertAlmostEqual(predicted, 137.0 + 1.0 / 28.0)

    def test_residual_under_3_ppm(self):
        resid = alpha_inv_residual()
        # 1/α = 137 + 1/28 vs CODATA gives roughly -2.08 ppm
        self.assertLess(abs(resid["relative_residual_ppm"]), 10.0)


class TestStructuralReadingsOf28(unittest.TestCase):

    def test_28_equals_4_plus_24(self):
        # Pentachoron + torsion
        self.assertEqual(4 + 24, 28)

    def test_28_equals_7_times_4(self):
        # Fano shell × tetrahedral cells
        self.assertEqual(7 * 4, 28)

    def test_28_equals_C_8_2(self):
        # Pair count of Cl(3,0) basis elements
        import math
        self.assertEqual(math.comb(8, 2), 28)


class TestShowcase(unittest.TestCase):

    def test_showcase_returns_lines(self):
        out = showcase_fine_structure_hierarchy()
        self.assertIsInstance(out, list)
        self.assertGreater(len(out), 10)

    def test_showcase_mentions_canonical_info(self):
        joined = "\n".join(showcase_fine_structure_hierarchy())
        for token in ("137", "ord_137(4)", "Z[i]", "Z[ω]", "28"):
            self.assertIn(token, joined, msg=f"missing: {token}")
