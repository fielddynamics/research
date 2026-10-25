"""
test_mu_partition.py
====================

Regression tests for the gravitational partition module:
  - mu(x) constitutive law and TetA / TetB shares
  - Odds ratio mu/(1-mu) = x
  - Logistic identity x dmu/dx = mu(1-mu)
  - Born-rule map mu = (1+cos theta)/2 and inverse
  - Three interior Niven readings:
      s = -1 <-> mu = 1/4 <-> x = 1/3   (sub-transition)
      s =  0 <-> mu = 1/2 <-> x = 1     (MOND transition, g = a_0)
      s = +1 <-> mu = 3/4 <-> x = 3     (super-transition)
  - SST static-spherical limit g^2/(g+a_0) = GM/r^2
"""

from __future__ import annotations

import unittest
from math import isclose, pi

from python.mu_partition import (
    born_rule_map,
    inverse_born_rule,
    logistic_identity_check,
    mond_transition_check,
    mu,
    mu_derivative,
    niven_partition_points,
    odds_ratio,
    partition_to_x,
    sst_quadratic,
    sst_static_solve_g,
    tetA_share,
    tetB_share,
    x_from_theta,
    x_to_partition,
)


class TestMuConstitutiveLaw(unittest.TestCase):

    def test_mu_at_x_0(self):
        self.assertEqual(mu(0.0), 0.0)

    def test_mu_at_x_1(self):
        self.assertEqual(mu(1.0), 0.5)

    def test_mu_at_x_3(self):
        self.assertAlmostEqual(mu(3.0), 0.75)

    def test_mu_at_x_third(self):
        self.assertAlmostEqual(mu(1.0 / 3.0), 0.25)

    def test_mu_large_x(self):
        """mu approaches 1 as x -> infinity (Newtonian limit)."""
        self.assertAlmostEqual(mu(1e10), 1.0, places=9)

    def test_tetA_plus_tetB_is_one(self):
        for x in [0.1, 0.5, 1.0, 2.0, 5.0, 100.0]:
            self.assertAlmostEqual(tetA_share(x) + tetB_share(x), 1.0)


class TestOddsRatio(unittest.TestCase):

    def test_odds_at_x_1(self):
        """At x = 1: odds = 1 (parity-symmetric MOND transition)."""
        self.assertAlmostEqual(odds_ratio(1.0), 1.0)

    def test_odds_equals_x(self):
        """The odds ratio mu/(1-mu) is exactly x."""
        for x in [0.3, 1.0, 3.0, 10.0]:
            self.assertAlmostEqual(odds_ratio(x), x, places=12)


class TestLogisticIdentity(unittest.TestCase):

    def test_at_multiple_x(self):
        """x * dmu/dx = mu * (1 - mu) at multiple x."""
        for x in [0.1, 0.5, 1.0, 2.0, 5.0, 100.0]:
            self.assertTrue(logistic_identity_check(x),
                            f"Logistic identity failed at x={x}")

    def test_mu_derivative_at_x_1(self):
        """dmu/dx at x=1: 1/4."""
        self.assertAlmostEqual(mu_derivative(1.0), 0.25)


class TestBornRuleMap(unittest.TestCase):

    def test_theta_pi_over_3_gives_mu_three_quarters(self):
        """theta = pi/3 (s = +1) -> cos = 1/2 -> mu = 3/4."""
        self.assertAlmostEqual(born_rule_map(pi / 3), 0.75)

    def test_theta_pi_over_2_gives_mu_one_half(self):
        """theta = pi/2 (s = 0) -> cos = 0 -> mu = 1/2."""
        self.assertAlmostEqual(born_rule_map(pi / 2), 0.5)

    def test_theta_two_pi_over_3_gives_mu_one_quarter(self):
        """theta = 2pi/3 (s = -1) -> cos = -1/2 -> mu = 1/4."""
        self.assertAlmostEqual(born_rule_map(2 * pi / 3), 0.25)

    def test_inverse_round_trip(self):
        """inverse_born_rule(born_rule_map(theta)) = cos(theta)."""
        from math import cos
        for theta in [0.1, 0.5, 1.0, 2.0]:
            cos_value = inverse_born_rule(born_rule_map(theta))
            self.assertAlmostEqual(cos_value, cos(theta), places=12)


class TestThetaToX(unittest.TestCase):

    def test_x_from_theta_pi_over_2(self):
        """theta = pi/2 -> x = 1."""
        self.assertAlmostEqual(x_from_theta(pi / 2), 1.0)

    def test_x_from_theta_pi_over_3(self):
        """theta = pi/3 -> x = 3."""
        self.assertAlmostEqual(x_from_theta(pi / 3), 3.0)

    def test_x_from_theta_two_pi_over_3(self):
        """theta = 2pi/3 -> x = 1/3."""
        self.assertAlmostEqual(x_from_theta(2 * pi / 3), 1.0 / 3.0)


class TestPartitionXMapping(unittest.TestCase):

    def test_round_trip(self):
        """x_to_partition(x) and partition_to_x are inverses."""
        for x in [0.1, 0.5, 1.0, 3.0, 10.0]:
            self.assertAlmostEqual(partition_to_x(x_to_partition(x)), x)


class TestNivenPartitionPoints(unittest.TestCase):

    def test_three_rows(self):
        rows = niven_partition_points()
        self.assertEqual(len(rows), 3)

    def test_s_minus_1_is_sub_transition(self):
        rows = niven_partition_points()
        sub = next(r for r in rows if r["s"] == -1)
        self.assertAlmostEqual(sub["mu"], 0.25)
        self.assertAlmostEqual(sub["x"], 1.0 / 3.0)
        self.assertEqual(sub["order_n"], 3)
        self.assertEqual(sub["phi_n_at_K4"], 13)
        self.assertIn("sub-transition", sub["regime"])

    def test_s_0_is_mond_transition(self):
        rows = niven_partition_points()
        mond = next(r for r in rows if r["s"] == 0)
        self.assertAlmostEqual(mond["mu"], 0.5)
        self.assertAlmostEqual(mond["x"], 1.0)
        self.assertEqual(mond["order_n"], 4)
        self.assertEqual(mond["phi_n_at_K4"], 17)
        self.assertIn("MOND", mond["regime"])

    def test_s_plus_1_is_super_transition(self):
        rows = niven_partition_points()
        sup = next(r for r in rows if r["s"] == +1)
        self.assertAlmostEqual(sup["mu"], 0.75)
        self.assertAlmostEqual(sup["x"], 3.0)
        self.assertEqual(sup["order_n"], 6)
        self.assertEqual(sup["phi_n_at_K4"], 21)
        self.assertIn("super-transition", sup["regime"])


class TestMondTransitionCheck(unittest.TestCase):

    def test_mu_is_half(self):
        result = mond_transition_check()
        self.assertTrue(result["is_one_half"])

    def test_x_is_one(self):
        result = mond_transition_check()
        self.assertTrue(result["x_is_one"])


class TestSSTQuadratic(unittest.TestCase):

    def test_at_deep_newtonian(self):
        """At g >> a_0: g^2/(g+a_0) ~ g (Newtonian limit)."""
        g = 1.0
        a_0 = 1e-10
        result = sst_quadratic(g, a_0)
        self.assertAlmostEqual(result, g, places=8)

    def test_at_deep_mond(self):
        """At g << a_0: g^2/(g+a_0) ~ g^2/a_0 (deep MOND limit)."""
        g = 1e-10
        a_0 = 1.0
        result = sst_quadratic(g, a_0)
        self.assertAlmostEqual(result, g * g / a_0, places=8)

    def test_at_transition(self):
        """At g = a_0: g^2/(2a_0) = a_0/2."""
        g = 1.0
        a_0 = 1.0
        result = sst_quadratic(g, a_0)
        self.assertAlmostEqual(result, 0.5)

    def test_solve_round_trip(self):
        """sst_static_solve_g(a_0, GM/r^2) returns g such that g^2/(g+a_0) = GM/r^2."""
        a_0 = 1.2e-10
        for GM_over_r2 in [1e-12, 1e-10, 1e-9, 1e-6]:
            g = sst_static_solve_g(a_0, GM_over_r2)
            self.assertAlmostEqual(sst_quadratic(g, a_0), GM_over_r2, places=10)


if __name__ == "__main__":
    unittest.main()
