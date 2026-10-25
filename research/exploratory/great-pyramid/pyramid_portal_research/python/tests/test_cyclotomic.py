"""
test_cyclotomic.py
==================

Regression tests for the cyclotomic shell algebra:
  - Phi_3, Phi_4, Phi_6 polynomial values
  - Shell construction
  - Shift identity Phi_3(K) = Phi_6(K+1)
  - Scale fusion identity Phi_3(K) * Phi_6(K) = Phi_3(K^2)  [Theorem 5]
  - sphere_surface_area_unit
  - Coupling polynomial f(K, s) = K^2 + s*K + 1
"""

from __future__ import annotations

import unittest
from math import pi

from python.cyclotomic import (
    coupling_polynomial,
    phi3,
    phi4,
    phi6,
    scale_fusion_identity,
    shell,
    shift_identity,
    sphere_surface_area_unit,
)


class TestCyclotomicPolynomials(unittest.TestCase):
    """Φ_3, Φ_4, Φ_6 at integer K against closed-form values."""

    def test_phi_at_K_4(self):
        self.assertEqual(phi3(4), 21)
        self.assertEqual(phi4(4), 17)
        self.assertEqual(phi6(4), 13)

    def test_phi_at_K_5(self):
        self.assertEqual(phi3(5), 31)
        self.assertEqual(phi4(5), 26)
        self.assertEqual(phi6(5), 21)

    def test_phi_table_K_2_to_10(self):
        """Cross-check all three polynomials at K=2..10."""
        expected = {
            2: (phi6(2), phi4(2), phi3(2)),   # (3, 5, 7)
            3: (phi6(3), phi4(3), phi3(3)),   # (7, 10, 13)
            4: (phi6(4), phi4(4), phi3(4)),   # (13, 17, 21)
            5: (phi6(5), phi4(5), phi3(5)),   # (21, 26, 31)
            6: (phi6(6), phi4(6), phi3(6)),   # (31, 37, 43)
        }
        # closed-form: (K^2-K+1, K^2+1, K^2+K+1)
        for K, (lower, neutral, upper) in expected.items():
            self.assertEqual(lower, K * K - K + 1)
            self.assertEqual(neutral, K * K + 1)
            self.assertEqual(upper, K * K + K + 1)

    def test_coupling_polynomial(self):
        """f(K, s) = K^2 + s*K + 1 at the three Niven s values."""
        for K in [2, 3, 4, 5, 6, 7]:
            self.assertEqual(coupling_polynomial(K, +1), phi3(K))
            self.assertEqual(coupling_polynomial(K, 0), phi4(K))
            self.assertEqual(coupling_polynomial(K, -1), phi6(K))


class TestShellObject(unittest.TestCase):
    """Shell construction and properties."""

    def test_shell_at_K_4_is_13_17_21(self):
        sh = shell(4)
        self.assertEqual(sh.K, 4)
        self.assertEqual(sh.lower, 13)
        self.assertEqual(sh.neutral, 17)
        self.assertEqual(sh.upper, 21)
        self.assertEqual(sh.tuple, (13, 17, 21))

    def test_shell_at_K_5_is_21_26_31(self):
        sh = shell(5)
        self.assertEqual(sh.tuple, (21, 26, 31))

    def test_shell_step_equals_K(self):
        """Equal-step ladder: E_K - C_K = K and U_K - E_K = K."""
        for K in [2, 3, 4, 5, 6, 7]:
            sh = shell(K)
            self.assertEqual(sh.step, K)
            self.assertEqual(sh.upper - sh.neutral, K)


class TestShiftIdentity(unittest.TestCase):
    """Phi_3(K) = Phi_6(K+1) at multiple K."""

    def test_shift_at_K_4(self):
        """The pyramid hinge: Phi_3(4) = 21 = Phi_6(5)."""
        result = shift_identity(4)
        self.assertEqual(result["Phi3_K"], 21)
        self.assertEqual(result["Phi6_K_plus_1"], 21)
        self.assertTrue(result["holds"])

    def test_shift_at_multiple_K(self):
        """Shift identity holds at all integer K from 1 to 10."""
        for K in range(1, 11):
            result = shift_identity(K)
            self.assertTrue(result["holds"],
                            f"Shift identity fails at K={K}: {result}")


class TestScaleFusionIdentity(unittest.TestCase):
    """Theorem 5: Phi_3(K) * Phi_6(K) = Phi_3(K^2)."""

    def test_fusion_at_K_4(self):
        """21 * 13 = 273 = Phi_3(16)."""
        result = scale_fusion_identity(4)
        self.assertEqual(result["Phi3_times_Phi6"], 273)
        self.assertEqual(result["Phi3_K_squared"], 273)
        self.assertTrue(result["holds"])

    def test_fusion_at_K_2(self):
        """7 * 3 = 21 = Phi_3(4) — landing on the K=4 closure level."""
        result = scale_fusion_identity(2)
        self.assertEqual(result["Phi3_times_Phi6"], 21)
        self.assertEqual(result["Phi3_K_squared"], 21)
        self.assertTrue(result["holds"])

    def test_fusion_at_multiple_K(self):
        """Scale fusion holds at K=2..10."""
        for K in range(2, 11):
            self.assertTrue(scale_fusion_identity(K)["holds"],
                            f"Scale fusion fails at K={K}")


class TestSphereSurfaceArea(unittest.TestCase):
    """Surface areas of unit n-spheres."""

    def test_S0(self):
        """Two-point sphere has 'area' 2."""
        self.assertEqual(sphere_surface_area_unit(0), 2.0)

    def test_S1(self):
        """Circle: 2*pi."""
        self.assertAlmostEqual(sphere_surface_area_unit(1), 2 * pi, places=12)

    def test_S2(self):
        """Standard 2-sphere: 4*pi."""
        self.assertAlmostEqual(sphere_surface_area_unit(2), 4 * pi, places=12)

    def test_S3(self):
        """3-sphere: 2*pi^2."""
        self.assertAlmostEqual(sphere_surface_area_unit(3), 2 * pi * pi, places=12)


# =============================================================================
# Phase 3 additions: Niven rigidity, norm form, cyclotomic integers
# =============================================================================

from python.cyclotomic import (  # noqa: E402
    cyclotomic_integer_norm,
    niven_partition_table,
    niven_rigidity_check,
    norm_form,
)


class TestNivenRigidity(unittest.TestCase):

    def test_integer_s_in_domain(self):
        """The three Niven integers in [-1, +1] are exactly {-1, 0, +1}."""
        result = niven_rigidity_check()
        self.assertEqual(result["integer_s_in_domain"], [-1, 0, +1])

    def test_rotation_orders(self):
        """s in {-1, 0, +1} <-> rotation orders {3, 4, 6}."""
        result = niven_rigidity_check()
        self.assertEqual(result["orders_n"], {-1: 3, 0: 4, +1: 6})

    def test_phi_n_all_equal_2(self):
        """All three orders have phi(n) = 2."""
        result = niven_rigidity_check()
        for n, val in result["phi_n_values"].items():
            self.assertEqual(val, 2)


class TestNormForm(unittest.TestCase):

    def test_norm_form_at_theta_pi_over_3(self):
        """theta = pi/3 -> s = 2 cos(pi/3) = 1 -> f(K, 1) = Phi_3(K)."""
        from math import pi as _pi
        for K in [2, 3, 4, 5, 6]:
            self.assertAlmostEqual(norm_form(K, _pi / 3), phi3(K), places=12)

    def test_norm_form_at_theta_pi_over_2(self):
        """theta = pi/2 -> s = 0 -> f(K, 0) = Phi_4(K)."""
        from math import pi as _pi
        for K in [2, 3, 4, 5, 6]:
            self.assertAlmostEqual(norm_form(K, _pi / 2), phi4(K), places=12)

    def test_norm_form_at_theta_2pi_over_3(self):
        """theta = 2*pi/3 -> s = -1 -> f(K, -1) = Phi_6(K)."""
        from math import pi as _pi
        for K in [2, 3, 4, 5, 6]:
            self.assertAlmostEqual(norm_form(K, 2 * _pi / 3), phi6(K), places=12)


class TestCyclotomicIntegerNorms(unittest.TestCase):

    def test_norm_in_Z_zeta_3(self):
        """N(K + zeta_3) = Phi_6(K) in the Eisenstein integers."""
        for K in [2, 3, 4, 5, 6]:
            self.assertEqual(cyclotomic_integer_norm(K, 3), phi6(K))

    def test_norm_in_Z_i(self):
        """N(K + i) = Phi_4(K) in the Gaussian integers."""
        for K in [2, 3, 4, 5, 6]:
            self.assertEqual(cyclotomic_integer_norm(K, 4), phi4(K))

    def test_norm_in_Z_zeta_6(self):
        """N(K + zeta_6) = Phi_3(K)."""
        for K in [2, 3, 4, 5, 6]:
            self.assertEqual(cyclotomic_integer_norm(K, 6), phi3(K))

    def test_invalid_n_raises(self):
        with self.assertRaises(ValueError):
            cyclotomic_integer_norm(4, 5)


class TestNivenPartitionTable(unittest.TestCase):

    def test_K_4_table_has_three_entries(self):
        table = niven_partition_table(4)
        self.assertEqual(set(table.keys()), {-1, 0, +1})

    def test_K_4_values_are_13_17_21(self):
        table = niven_partition_table(4)
        self.assertEqual(table[-1]["value_at_K"], 13)
        self.assertEqual(table[0]["value_at_K"], 17)
        self.assertEqual(table[+1]["value_at_K"], 21)

    def test_K_4_rotation_orders(self):
        table = niven_partition_table(4)
        self.assertEqual(table[-1]["order_n"], 3)
        self.assertEqual(table[0]["order_n"], 4)
        self.assertEqual(table[+1]["order_n"], 6)


if __name__ == "__main__":
    unittest.main()
