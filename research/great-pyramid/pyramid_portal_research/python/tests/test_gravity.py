"""
test_gravity.py
===============

Regression tests for the gravity derivation:
  - alpha_G value pinned to 16-digit reference
  - G prediction within -14 ppm of CODATA reference
  - tetrad impedance ratio is exact Fraction(17, 13)
  - Pentachoron directed-edge count = 20 = Phi_3(4) - 1
  - alpha_gravity_parts factorization is consistent
  - Four routes to K=4 all converge
  - Generalized alpha_G(K) reduces correctly at K=4
"""

from __future__ import annotations

import unittest
from fractions import Fraction

from python.constants import ALPHA, G_OBSERVED
from python.gravity import (
    G_prediction_report,
    alpha_G_for_K,
    alpha_gravity,
    alpha_gravity_parts,
    coupling_exponent_for_K,
    edge_phase_closure,
    four_routes_select_K4,
    gravity_over_coulomb_gap_exponent,
    pentachoron_directed_edge_count,
    pentachoron_edge_product,
    predict_G_from_alpha,
    tetrad_impedance_ratio,
    tetrad_renormalization_factor,
)


# Reference values pinned from the legacy monolith
ALPHA_G_REFERENCE = 1.751785102035007e-45
G_PREDICTED_REFERENCE = 6.674207444742525e-11
PPM_ERROR_REFERENCE = -13.867410436170937


class TestTetradImpedance(unittest.TestCase):

    def test_impedance_is_17_over_13(self):
        self.assertEqual(tetrad_impedance_ratio(), Fraction(17, 13))

    def test_impedance_as_float(self):
        self.assertAlmostEqual(float(tetrad_impedance_ratio()),
                               17.0 / 13.0, places=15)


class TestAlphaGravity(unittest.TestCase):

    def test_alpha_gravity_value(self):
        """alpha_G pinned to legacy 16-digit reference."""
        self.assertAlmostEqual(alpha_gravity(), ALPHA_G_REFERENCE,
                               delta=1e-58)

    def test_alpha_gravity_parts_multiply_to_alpha_G(self):
        """Decomposition is consistent: product of parts = alpha_G."""
        parts = alpha_gravity_parts()
        product = (parts["primitive_coulomb_edge_alpha"]
                   * parts["directed_pentachoron_product_alpha20"]
                   * parts["tetrad_impedance_17_over_13"]
                   * parts["spin_load_g_over_2"])
        self.assertAlmostEqual(product, parts["alpha_G"], delta=1e-58)


class TestGPrediction(unittest.TestCase):

    def test_G_predicted(self):
        """G_predicted pinned to legacy value."""
        self.assertAlmostEqual(predict_G_from_alpha(), G_PREDICTED_REFERENCE,
                               delta=1e-22)

    def test_G_prediction_within_14_ppm(self):
        """The framework predicts G within 14 ppm of CODATA reference."""
        report = G_prediction_report()
        self.assertLess(abs(report["ppm_error"]), 14.0)

    def test_ppm_error_pinned(self):
        """Pin the exact ppm error against the legacy run."""
        report = G_prediction_report()
        self.assertAlmostEqual(report["ppm_error"], PPM_ERROR_REFERENCE,
                               places=10)

    def test_G_observed_reference_in_report(self):
        report = G_prediction_report()
        self.assertEqual(report["G_observed_reference"], G_OBSERVED)


class TestPentachoronEdges(unittest.TestCase):

    def test_directed_edge_count_is_20(self):
        self.assertEqual(pentachoron_directed_edge_count(), 20)

    def test_pentachoron_edges_match_phi3_4_minus_1(self):
        """The 20 directed edges of K_5 saturate the Phi_3(4) - 1 = 20 gap."""
        from python.cyclotomic import phi3
        self.assertEqual(pentachoron_directed_edge_count(), phi3(4) - 1)

    def test_pentachoron_edge_product_zero_phase(self):
        """At zero phases, edge product is alpha^20."""
        result = pentachoron_edge_product()
        expected = ALPHA ** 20
        self.assertAlmostEqual(result.real, expected, delta=1e-58)
        self.assertAlmostEqual(result.imag, 0.0, delta=1e-58)

    def test_pentachoron_edge_product_wrong_count_raises(self):
        with self.assertRaises(ValueError):
            pentachoron_edge_product(phases=[0.0] * 19)  # one short

    def test_edge_phase_closure_zero(self):
        self.assertTrue(edge_phase_closure([0.0] * 20))

    def test_edge_phase_closure_nonzero(self):
        self.assertFalse(edge_phase_closure([0.1] + [0.0] * 19))


class TestGeneralizedKCoupling(unittest.TestCase):

    def test_coupling_exponent_at_K_4_is_21(self):
        self.assertEqual(coupling_exponent_for_K(4), 21)

    def test_coupling_exponent_at_K_5_is_31(self):
        self.assertEqual(coupling_exponent_for_K(5), 31)

    def test_gap_exponent_at_K_4_is_20(self):
        """Phi_3(K) - 1 = K(K+1); at K=4: 20."""
        self.assertEqual(gravity_over_coulomb_gap_exponent(4), 20)
        self.assertEqual(gravity_over_coulomb_gap_exponent(4), 4 * 5)

    def test_alpha_G_for_K_4_matches_alpha_gravity(self):
        """alpha_G_for_K(4) reduces to the standard alpha_gravity."""
        self.assertAlmostEqual(alpha_G_for_K(4), alpha_gravity(), delta=1e-58)

    def test_tetrad_renormalization_at_K_4(self):
        """R(alpha, 4) * alpha = alpha_G."""
        R = tetrad_renormalization_factor(4)
        self.assertAlmostEqual(R * ALPHA, alpha_gravity(), delta=1e-58)


class TestFourRoutesToK4(unittest.TestCase):

    def test_uniqueness_equation_route(self):
        """2(D+1) = 2^D has unique solution at D=3, K=4."""
        routes = four_routes_select_K4()
        uniqueness = routes[0]
        self.assertEqual(uniqueness["solutions_D_K_in_1_to_11"], [(3, 4)])
        self.assertEqual(uniqueness["selected_K"], 4)

    def test_three_sweep_divisibility(self):
        """3 divides Phi_3(K) iff K = 1 mod 3."""
        routes = four_routes_select_K4()
        three_sweep = routes[1]
        self.assertIn(4, three_sweep["small_positive_K"])
        self.assertEqual(three_sweep["selected_K"], 4)

    def test_cyclotomic_route_yields_shell(self):
        """Degree-2 cyclotomic uniqueness identifies the shell at K=4."""
        routes = four_routes_select_K4()
        cyclo = routes[2]
        self.assertEqual(cyclo["selected_shell_at_K4"], (13, 17, 21))

    def test_fermat_seed(self):
        """K = 2^(2^n) at n=1 gives K=4."""
        routes = four_routes_select_K4()
        fermat = routes[3]
        self.assertEqual(fermat["sequence"][:4], [2, 4, 16, 256])
        self.assertEqual(fermat["selected_K"], 4)


# =============================================================================
# Phase 3 additions: permutation discrimination
# =============================================================================

from python.gravity import best_permutation, permutation_discrimination  # noqa: E402


class TestPermutationDiscrimination(unittest.TestCase):

    def test_returns_six_candidates(self):
        """Six permutations of three distinct values."""
        candidates = permutation_discrimination()
        self.assertEqual(len(candidates), 6)

    def test_winner_is_framework_selection(self):
        """The best permutation is (21, 17, 13)."""
        candidates = permutation_discrimination()
        winner = candidates[0]
        self.assertEqual((winner["exp"], winner["num"], winner["den"]),
                         (21, 17, 13))

    def test_winner_has_smallest_abs_ppm(self):
        """Winner's |ppm error| is smaller than all others'."""
        candidates = permutation_discrimination()
        winner_abs = candidates[0]["abs_ppm_error"]
        for c in candidates[1:]:
            self.assertGreater(c["abs_ppm_error"], winner_abs)

    def test_winner_ppm_within_14(self):
        """Framework permutation lands within 14 ppm."""
        candidates = permutation_discrimination()
        winner = candidates[0]
        self.assertLess(abs(winner["ppm_error"]), 14.0)

    def test_runner_up_is_dramatically_worse(self):
        """Second-best permutation should be orders of magnitude worse."""
        candidates = permutation_discrimination()
        # Winner is within ~14 ppm. Runner-up (which keeps exp=21 but swaps
        # num and den to 13/17) is at ~4.15e5 ppm — about 30,000x worse.
        # Other permutations change the exponent and are absurdly far off
        # (1e14 to 1e23 ppm). Threshold of 1000 ppm is conservative.
        self.assertGreater(candidates[1]["abs_ppm_error"], 1000.0)
        # Strict separation: runner-up is at least 1000x worse than winner
        winner_abs = candidates[0]["abs_ppm_error"]
        self.assertGreater(candidates[1]["abs_ppm_error"], 1000.0 * winner_abs)

    def test_best_permutation_helper(self):
        result = best_permutation()
        self.assertEqual(result["winning_exp_num_den"], (21, 17, 13))
        self.assertTrue(result["matches_framework"])
        self.assertLess(abs(result["winner_ppm_error"]), 14.0)


if __name__ == "__main__":
    unittest.main()
