"""
test_topology.py
================

Regression tests for topology helpers:
  - Quaternion algebra (normalize, conjugate, multiply)
  - Hopf S^3 -> S^2 projection
  - A_5 order, pentachoron cells, A_5 x Z_21 sectors
  - Crystallographic threshold (S_5 order, 5-fold factor)
  - Null-cone associator status table
"""

from __future__ import annotations

import unittest

from python.constants import G_E_OVER_2
from python.topology import (
    a5_address_sector_count,
    alternating_group_A5_order,
    crystallographic_threshold_pentachoron,
    electron_hopf_fiber_holonomy,
    hopf_fiber_phase,
    hopf_projection,
    null_cone_associator_status,
    pentachoron_cell_count,
    q_conjugate,
    q_multiply,
    q_normalize,
)


class TestQuaternionAlgebra(unittest.TestCase):

    def test_q_normalize_unit(self):
        """A unit quaternion is unchanged by normalization."""
        q = (1.0, 0.0, 0.0, 0.0)
        result = q_normalize(q)
        self.assertEqual(result, q)

    def test_q_normalize_scales_to_unit(self):
        q = (2.0, 0.0, 0.0, 0.0)
        result = q_normalize(q)
        self.assertEqual(result, (1.0, 0.0, 0.0, 0.0))

    def test_q_normalize_zero_raises(self):
        with self.assertRaises(ValueError):
            q_normalize((0.0, 0.0, 0.0, 0.0))

    def test_q_conjugate(self):
        q = (1.0, 2.0, 3.0, 4.0)
        self.assertEqual(q_conjugate(q), (1.0, -2.0, -3.0, -4.0))

    def test_q_multiply_identity(self):
        """(1, 0, 0, 0) * q = q."""
        q = (0.5, 0.1, 0.2, 0.3)
        I = (1.0, 0.0, 0.0, 0.0)
        result = q_multiply(I, q)
        for a, b in zip(result, q):
            self.assertAlmostEqual(a, b)

    def test_q_multiply_basis_ij_equals_k(self):
        """Quaternion basis identity: i * j = k."""
        i = (0.0, 1.0, 0.0, 0.0)
        j = (0.0, 0.0, 1.0, 0.0)
        k = (0.0, 0.0, 0.0, 1.0)
        result = q_multiply(i, j)
        for a, b in zip(result, k):
            self.assertAlmostEqual(a, b)


class TestHopfProjection(unittest.TestCase):

    def test_identity_quaternion_projects_to_north_pole(self):
        """q = (1, 0, 0, 0) leaves k = (0, 0, 1) fixed: Hopf projection = (0, 0, 1)."""
        result = hopf_projection((1.0, 0.0, 0.0, 0.0))
        self.assertAlmostEqual(result[0], 0.0)
        self.assertAlmostEqual(result[1], 0.0)
        self.assertAlmostEqual(result[2], 1.0)

    def test_hopf_projection_is_unit_vector(self):
        """The image of the Hopf map is on S^2."""
        from math import sqrt
        q = (1.0, 2.0, 3.0, 4.0)
        result = hopf_projection(q)
        magnitude = sqrt(sum(x * x for x in result))
        self.assertAlmostEqual(magnitude, 1.0)

    def test_hopf_fiber_phase_zero(self):
        """exp(0) = 1."""
        result = hopf_fiber_phase(0.0)
        self.assertAlmostEqual(result.real, 1.0)
        self.assertAlmostEqual(result.imag, 0.0)


class TestElectronHopfHolonomy(unittest.TestCase):

    def test_g_e_over_2(self):
        self.assertEqual(electron_hopf_fiber_holonomy(), G_E_OVER_2)


class TestA5AndPentachoron(unittest.TestCase):

    def test_A5_order_is_60(self):
        self.assertEqual(alternating_group_A5_order(), 60)

    def test_pentachoron_cells(self):
        self.assertEqual(pentachoron_cell_count(), 5)

    def test_a5_x_z21_is_1260(self):
        self.assertEqual(a5_address_sector_count(), 1260)
        self.assertEqual(a5_address_sector_count(), 60 * 21)


class TestCrystallographicThreshold(unittest.TestCase):

    def test_S5_order_is_120(self):
        result = crystallographic_threshold_pentachoron()
        self.assertEqual(result["symmetry_group_order"], 120)

    def test_factorization_has_5_fold(self):
        result = crystallographic_threshold_pentachoron()
        self.assertIn(5, result["factorization"])
        self.assertEqual(result["factorization"][5], 1)

    def test_directed_edges_20(self):
        result = crystallographic_threshold_pentachoron()
        self.assertEqual(result["directed_edges"], 20)


class TestNullConeAssociator(unittest.TestCase):

    def test_48_of_512_nonzero(self):
        result = null_cone_associator_status()
        self.assertEqual(result["basis_triples"], 512)
        self.assertEqual(result["nonzero_associator_triples"], 48)

    def test_support_patterns(self):
        result = null_cone_associator_status()
        self.assertEqual(result["nonzero_support_patterns"], ["AMM", "MMA"])
        self.assertEqual(len(result["vanishing_patterns"]), 6)


# =============================================================================
# Phase 3 additions: WRT invariant and SU(2)_19 Chern-Simons
# =============================================================================

from python.topology import (  # noqa: E402
    wrt_central_charge,
    wrt_invariant_sigma235_target,
    wrt_su2_19_chern_simons,
    wrt_su2_level_to_k_plus_2,
)


class TestSU2ChernSimons(unittest.TestCase):

    def test_shifted_level_at_k_19_is_21(self):
        """k = 19  ->  k + 2 = 21 = Phi_3(4)."""
        self.assertEqual(wrt_su2_level_to_k_plus_2(19), 21)

    def test_central_charge_at_k_19(self):
        """c = 3*19/21 = 19/7."""
        self.assertAlmostEqual(wrt_central_charge(19), 19.0 / 7.0, places=12)

    def test_su2_19_data(self):
        """The canonical SU(2)_19 CS data of the framework."""
        data = wrt_su2_19_chern_simons()
        self.assertEqual(data["level_k"], 19)
        self.assertEqual(data["shifted_level"], 21)
        self.assertEqual(data["integrable_reps"], 20)
        self.assertAlmostEqual(data["central_charge"], 19.0 / 7.0, places=12)


class TestWRTInvariantTarget(unittest.TestCase):

    def test_level_21_has_reference(self):
        result = wrt_invariant_sigma235_target(21)
        self.assertAlmostEqual(result["abs_tau_reference"], 8.0962)

    def test_other_levels_not_available(self):
        result = wrt_invariant_sigma235_target(10)
        self.assertFalse(result["available"])


if __name__ == "__main__":
    unittest.main()
