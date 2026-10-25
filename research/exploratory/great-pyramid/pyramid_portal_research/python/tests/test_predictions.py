"""
test_predictions.py
===================

Regression tests for framework predictions:
  - Coffer alpha-step against Petrie's 16.19 c^3 (0.77% deviation)
  - Relieving-chamber volume prediction
  - Sierpinski hierarchy: K=4 marked as gravity match, others as extrapolation
  - K=2 Schwinger hypothesis: alpha / (2*pi) first-order term
  - Lepton-anchor calculation
  - Golden impedance split: 13/34 close to 1/phi^2
"""

from __future__ import annotations

import unittest
from math import pi, sqrt

from python.constants import ALPHA, G_E_OVER_2, M_E
from python.predictions import (
    coffer_chamber_alpha_step,
    golden_impedance_split,
    k2_schwinger_loop_structure,
    lepton_anchor_report,
    relieving_chamber_volume_prediction,
    sierpinski_force_hierarchy,
)


class TestCofferStep(unittest.TestCase):

    def test_chamber_volume_is_1000_sqrt_5(self):
        result = coffer_chamber_alpha_step()
        self.assertAlmostEqual(result["V_chamber_cubits3"], 1000 * sqrt(5))

    def test_coffer_volume_petrie(self):
        """Default coffer volume from Petrie: 16.19 c^3."""
        result = coffer_chamber_alpha_step()
        self.assertAlmostEqual(result["V_coffer_ext_cubits3"], 16.19)

    def test_ratio_close_to_inverse_alpha(self):
        """V_chamber / V_coffer should be close to 1/alpha = 137.036."""
        result = coffer_chamber_alpha_step()
        ratio = result["V_chamber_over_V_coffer"]
        self.assertAlmostEqual(ratio, 138.114, places=2)
        self.assertLess(abs(ratio - 1 / ALPHA), 2.0)

    def test_relative_error_below_1_percent(self):
        """Petrie measurement lands within 1% of the predicted alpha-step."""
        result = coffer_chamber_alpha_step()
        self.assertLess(result["relative_error_vs_alpha"], 0.01)


class TestRelievingChamberVolume(unittest.TestCase):

    def test_prediction_at_K5(self):
        """V_relieving ≈ 5 * alpha * V_chamber."""
        V_chamber = 1000 * sqrt(5)
        expected = 5 * ALPHA * V_chamber
        self.assertAlmostEqual(relieving_chamber_volume_prediction(), expected)


class TestSierpinskiHierarchy(unittest.TestCase):

    def test_K_4_marked_gravity_match(self):
        rows = sierpinski_force_hierarchy()
        K4_row = next(r for r in rows if r.get("K") == 4)
        self.assertEqual(K4_row["status"], "gravity match")

    def test_K_2_K_16_K_256_extrapolation(self):
        rows = sierpinski_force_hierarchy()
        for K in [2, 16, 256]:
            row = next(r for r in rows if r.get("K") == K)
            self.assertEqual(row["status"], "algebraic extrapolation")

    def test_bare_coulomb_row(self):
        rows = sierpinski_force_hierarchy()
        bare = rows[0]
        self.assertEqual(bare["label"], "bare Coulomb")
        self.assertEqual(bare["full_exponent_Phi3"], 1)
        self.assertAlmostEqual(bare["attenuation"], ALPHA)

    def test_K_4_full_exponent_is_21(self):
        rows = sierpinski_force_hierarchy()
        K4_row = next(r for r in rows if r.get("K") == 4)
        self.assertEqual(K4_row["full_exponent_Phi3"], 21)
        self.assertEqual(K4_row["gap_exponent_KKplus1"], 20)
        self.assertAlmostEqual(K4_row["cyclotomic_ratio"], 17 / 13)


class TestK2Schwinger(unittest.TestCase):

    def test_alpha_over_2pi(self):
        """The Schwinger first-order anomaly is alpha / (2*pi)."""
        result = k2_schwinger_loop_structure()
        expected = ALPHA / (2 * pi)
        self.assertAlmostEqual(
            result["schwinger_first_order_alpha_over_2pi"], expected)

    def test_S1_volume_is_2pi(self):
        result = k2_schwinger_loop_structure()
        self.assertAlmostEqual(result["S1_volume"], 2 * pi)

    def test_g_over_2_first_order(self):
        """Predicted g/2 to first order: 1 + alpha/(2*pi)."""
        result = k2_schwinger_loop_structure()
        self.assertAlmostEqual(
            result["g_over_2_first_order"], 1 + ALPHA / (2 * pi))

    def test_first_order_close_to_observed(self):
        """First-order alpha/(2*pi) approximation is close to measured g_e/2."""
        result = k2_schwinger_loop_structure()
        observed_difference = G_E_OVER_2 - 1
        predicted_first_order = result["schwinger_first_order_alpha_over_2pi"]
        # First-order Schwinger is close but not exact — higher orders push it.
        # The difference should be small compared to the first-order term itself.
        self.assertLess(
            abs(observed_difference - predicted_first_order)
            / predicted_first_order, 0.01)


class TestLeptonAnchor(unittest.TestCase):

    def test_electron_anchor_recovers_G(self):
        """With electron mass and g_e/2 the lepton anchor recovers the gravity prediction."""
        from python.gravity import predict_G_from_alpha
        result = lepton_anchor_report(mass_kg=M_E, g_over_2=G_E_OVER_2)
        self.assertAlmostEqual(
            result["G_from_this_lepton_anchor"],
            predict_G_from_alpha(),
            delta=1e-22)


class TestGoldenImpedance(unittest.TestCase):

    def test_raw_is_3_over_8(self):
        result = golden_impedance_split()
        self.assertEqual(result["exterior_raw_float"], 3 / 8)

    def test_refined_close_to_inverse_phi_squared(self):
        """13/34 should be close to 1/phi^2."""
        result = golden_impedance_split()
        phi = (1 + sqrt(5)) / 2
        self.assertAlmostEqual(
            result["refined_float"], 1 / (phi * phi), places=3)

    def test_refined_minus_inverse_phi_squared_is_small(self):
        """The difference 13/34 - 1/phi^2 is order 4e-4."""
        result = golden_impedance_split()
        self.assertLess(abs(result["difference"]), 1e-3)


if __name__ == "__main__":
    unittest.main()
