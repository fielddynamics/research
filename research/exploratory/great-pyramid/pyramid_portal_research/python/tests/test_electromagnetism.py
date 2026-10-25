"""
test_electromagnetism.py
========================

Regression tests for the Maxwell module:
  - V tensor V = Sym^2 oplus Lambda^2 dimensions
  - Six edges of K_4 (3 time-space E, 3 space-space B)
  - Three perfect matchings = three opposite-edge pairs
  - Self-dual / anti-self-dual decomposition F_pm = (E pm icB)/2
  - Hodge star squared = -1 in Lorentzian
  - Dirac quantization e*g = n hbar c / 2
  - Coulomb step alpha^1
  - Gravity as 21 Coulomb steps (3 sweeps of 7)
"""

from __future__ import annotations

import unittest

from python.constants import ALPHA, C_LIGHT, HBAR
from python.electromagnetism import (
    F_mu_nu_basis,
    anti_self_dual_part,
    coulomb_step,
    dirac_quantization_check,
    gravity_as_21_coulomb_steps,
    hodge_star_squared_lorentzian,
    opposite_edge_pairs_K4,
    perfect_matchings_K4,
    self_dual_anti_self_dual_decomposition,
    self_dual_part,
    space_space_edges,
    tetrahedral_edges,
    time_space_edges,
    vv_decomposition,
)


class TestVVDecomposition(unittest.TestCase):

    def test_K_4_dimensions(self):
        """At K = 4: 10 oplus 6 = 16 = 4^2."""
        result = vv_decomposition(4)
        self.assertEqual(result["dim_sym2_V"], 10)
        self.assertEqual(result["dim_lambda2_V"], 6)
        self.assertEqual(result["total"], 16)
        self.assertEqual(result["check_K_squared"], 16)

    def test_K_5(self):
        """At K = 5: 15 oplus 10 = 25 = 5^2."""
        result = vv_decomposition(5)
        self.assertEqual(result["dim_sym2_V"], 15)
        self.assertEqual(result["dim_lambda2_V"], 10)
        self.assertEqual(result["total"], 25)

    def test_dimensions_match_K_squared(self):
        for K in [2, 3, 4, 5, 6, 7]:
            result = vv_decomposition(K)
            self.assertEqual(result["total"], K * K)


class TestTetrahedralEdges(unittest.TestCase):

    def test_K_4_has_six_edges(self):
        edges = tetrahedral_edges(4)
        self.assertEqual(len(edges), 6)

    def test_K_4_edges_explicit(self):
        edges = tetrahedral_edges(4)
        expected = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        self.assertEqual(edges, expected)

    def test_K_5_has_ten_edges(self):
        edges = tetrahedral_edges(5)
        self.assertEqual(len(edges), 10)


class TestTimeSpaceEdges(unittest.TestCase):

    def test_three_time_space_edges(self):
        """3 electric components."""
        edges = time_space_edges(4)
        self.assertEqual(len(edges), 3)
        self.assertEqual(edges, [(0, 1), (0, 2), (0, 3)])

    def test_three_space_space_edges(self):
        """3 magnetic components."""
        edges = space_space_edges(4)
        self.assertEqual(len(edges), 3)
        self.assertEqual(edges, [(1, 2), (1, 3), (2, 3)])


class TestFMuNuBasis(unittest.TestCase):

    def test_six_basis_elements(self):
        basis = F_mu_nu_basis()
        self.assertEqual(len(basis), 6)

    def test_three_electric_three_magnetic(self):
        basis = F_mu_nu_basis()
        electric = [b for b in basis if b["type"] == "electric"]
        magnetic = [b for b in basis if b["type"] == "magnetic"]
        self.assertEqual(len(electric), 3)
        self.assertEqual(len(magnetic), 3)


class TestPerfectMatchings(unittest.TestCase):

    def test_three_matchings(self):
        """K_4 has exactly three perfect matchings."""
        matchings = perfect_matchings_K4()
        self.assertEqual(len(matchings), 3)

    def test_three_opposite_edge_pairs(self):
        pairs = opposite_edge_pairs_K4()
        self.assertEqual(len(pairs), 3)

    def test_opposite_pairs_are_disjoint(self):
        """Each pair is disjoint: the two edges share no vertex."""
        for e1, e2 in opposite_edge_pairs_K4():
            self.assertEqual(set(e1) & set(e2), set())

    def test_opposite_pairs_partition_vertices(self):
        """Each opposite pair uses all 4 vertices."""
        for e1, e2 in opposite_edge_pairs_K4():
            self.assertEqual(set(e1) | set(e2), {0, 1, 2, 3})


class TestSelfDualDecomposition(unittest.TestCase):

    def test_self_dual_at_real_E_zero_B(self):
        """E^k = 1, B^k = 0: F_+ = 1/2."""
        self.assertEqual(self_dual_part(1.0, 0.0, c=1.0), 0.5 + 0.0j)

    def test_anti_self_dual_at_real_E_zero_B(self):
        """E^k = 1, B^k = 0: F_- = 1/2."""
        self.assertEqual(anti_self_dual_part(1.0, 0.0, c=1.0), 0.5 + 0.0j)

    def test_sum_recovers_E(self):
        """F_+ + F_- = E."""
        E_k = 3.5 + 0.0j
        B_k = 1.2 + 0.0j
        F_plus = self_dual_part(E_k, B_k)
        F_minus = anti_self_dual_part(E_k, B_k)
        self.assertEqual(F_plus + F_minus, E_k)

    def test_difference_gives_icB(self):
        """F_+ - F_- = i c B."""
        E_k = 3.5 + 0.0j
        B_k = 1.2 + 0.0j
        c = 2.0
        F_plus = self_dual_part(E_k, B_k, c)
        F_minus = anti_self_dual_part(E_k, B_k, c)
        self.assertEqual(F_plus - F_minus, 1j * c * B_k)

    def test_decomposition_three_components(self):
        E = (1.0 + 0j, 2.0 + 0j, 3.0 + 0j)
        B = (0.1 + 0j, 0.2 + 0j, 0.3 + 0j)
        result = self_dual_anti_self_dual_decomposition(E, B)
        self.assertEqual(len(result["F_plus"]), 3)
        self.assertEqual(len(result["F_minus"]), 3)
        for k in range(3):
            self.assertEqual(result["F_plus"][k] + result["F_minus"][k], E[k])


class TestHodgeStar(unittest.TestCase):

    def test_star_squared_is_minus_1(self):
        """In Lorentzian 4D the Hodge star on 2-forms gives ** = -1."""
        self.assertEqual(hodge_star_squared_lorentzian(), -1)


class TestDiracQuantization(unittest.TestCase):

    def test_n_1(self):
        """e * g = hbar * c / 2 satisfied exactly for n = 1."""
        rhs = HBAR * C_LIGHT / 2.0
        # Pick any e and let g be such that e*g = rhs
        e = 1.0
        g_mag = rhs / e
        result = dirac_quantization_check(e_charge=e, g_magnetic_charge=g_mag, n=1)
        self.assertTrue(result["satisfied"])

    def test_inconsistent_n(self):
        """If the LHS does not match n*hbar*c/2 for the given n, satisfied = False."""
        e = 1.0
        g_mag = 1.0  # arbitrary
        # n chosen so the equation fails
        result = dirac_quantization_check(e_charge=e, g_magnetic_charge=g_mag, n=1000)
        self.assertFalse(result["satisfied"])


class TestCoulombStep(unittest.TestCase):

    def test_returns_alpha(self):
        self.assertEqual(coulomb_step(), ALPHA)

    def test_gravity_as_21_steps_match(self):
        """3 sweeps of 7 modes = alpha^21."""
        result = gravity_as_21_coulomb_steps()
        self.assertTrue(result["match"])

    def test_alpha_to_21_explicit(self):
        result = gravity_as_21_coulomb_steps()
        self.assertAlmostEqual(result["alpha_composite_3_sweeps"], ALPHA ** 21,
                               delta=1e-58)


if __name__ == "__main__":
    unittest.main()
