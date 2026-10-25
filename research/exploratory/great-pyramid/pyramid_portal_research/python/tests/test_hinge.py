"""
test_hinge.py
=============

Regression tests for the K=4 <-> K=5 portal hinge:
  - Hinge object structure
  - J_4 partial isometry shape and entries
  - Intertwiner identity H_5 J_4 = J_4 H_4 = 21 J_4
  - K=5 band assignment
"""

from __future__ import annotations

import unittest

from python.closure_read import matmul
from python.hinge import (
    interlevel_intertwiner_check,
    j4_partial_isometry,
    k5_band_assignment,
    pyramid_k4_k5_hinge,
)


class TestPyramidHinge(unittest.TestCase):

    def test_hinge_shells(self):
        hinge = pyramid_k4_k5_hinge()
        self.assertEqual(hinge.source_K, 4)
        self.assertEqual(hinge.receiver_K, 5)
        self.assertEqual(hinge.source_shell.tuple, (13, 17, 21))
        self.assertEqual(hinge.receiver_shell.tuple, (21, 26, 31))

    def test_shared_band_is_21(self):
        """Phi_3(4) = 21 = Phi_6(5) — the matched portal sector."""
        hinge = pyramid_k4_k5_hinge()
        self.assertEqual(hinge.shared_band, 21)

    def test_identity_holds(self):
        self.assertTrue(pyramid_k4_k5_hinge().identity_holds)


class TestJ4PartialIsometry(unittest.TestCase):

    def test_J4_shape(self):
        J = j4_partial_isometry()
        self.assertEqual(len(J), 3)
        self.assertEqual(len(J[0]), 3)

    def test_J4_single_nonzero_entry(self):
        """J_4 = |5,-><4,+| has a single 1 at row 0 column 2."""
        J = j4_partial_isometry()
        self.assertEqual(J[0][2], 1.0)
        zeros = [(i, j) for i in range(3) for j in range(3)
                 if not (i == 0 and j == 2)]
        for i, j in zeros:
            self.assertEqual(J[i][j], 0.0, f"J[{i}][{j}] should be 0")


class TestIntertwiner(unittest.TestCase):

    def test_intertwiner_holds(self):
        """H_5 J_4 = J_4 H_4 by the shift identity."""
        result = interlevel_intertwiner_check()
        self.assertTrue(result["holds"])

    def test_both_sides_equal_21_J4(self):
        """H_5 J_4 = J_4 H_4 = 21 * J_4 explicitly."""
        result = interlevel_intertwiner_check()
        J = j4_partial_isometry()
        expected = [[21.0 * J[i][j] for j in range(3)] for i in range(3)]
        self.assertEqual(result["H5J4"], expected)
        self.assertEqual(result["J4H4"], expected)


class TestK5BandAssignment(unittest.TestCase):

    def test_lower_band_is_21(self):
        """K=5 lower band receives the K=4 upper-emission band."""
        bands = k5_band_assignment()
        self.assertEqual(bands["lower_receive"]["band"], 21)

    def test_midpoint_band_is_26(self):
        bands = k5_band_assignment()
        self.assertEqual(bands["midpoint_balance"]["band"], 26)

    def test_upper_band_is_31(self):
        bands = k5_band_assignment()
        self.assertEqual(bands["upper_search"]["band"], 31)


class TestSubTetrahedronDecomposition(unittest.TestCase):
    """The 5-fold structure J_4 = sum_v J_4^{(v)} pi_v on the K_5 sub-tetrahedra."""

    def test_sub_tetrahedron_count_is_5(self):
        from python.hinge import sub_tetrahedron_count
        self.assertEqual(sub_tetrahedron_count(), 5)

    def test_S5_over_S4_index_is_5(self):
        from python.hinge import s5_supset_s4_branching
        d = s5_supset_s4_branching()
        self.assertEqual(d['S5_order'], 120)
        self.assertEqual(d['S4_order'], 24)
        self.assertEqual(d['index_S5_over_S4'], 5)
        self.assertEqual(d['sub_tetrahedron_count'], 5)
        self.assertTrue(d['indices_agree'])

    def test_decomposition_has_5_projectors(self):
        from python.hinge import hinge_sub_tetrahedron_decomposition
        d = hinge_sub_tetrahedron_decomposition()
        self.assertEqual(d['multiplicity'], 5)
        self.assertEqual(len(d['index_set']), 5)
        self.assertEqual(set(d['index_set']), {1, 2, 3, 4, 5})
        self.assertEqual(len(d['projector_basis']), 5)

    def test_decomposition_notes_physical_realization(self):
        from python.hinge import hinge_sub_tetrahedron_decomposition
        d = hinge_sub_tetrahedron_decomposition()
        self.assertIn('relieving chambers', d['physical_realization'])

    def test_decomposition_formula_string(self):
        from python.hinge import hinge_sub_tetrahedron_decomposition
        d = hinge_sub_tetrahedron_decomposition()
        self.assertIn('J_4', d['decomposition'])
        self.assertIn('pi_v', d['decomposition'])


if __name__ == "__main__":
    unittest.main()
