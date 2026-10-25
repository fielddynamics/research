"""
test_closure_read.py
====================

Regression tests for the matrix utilities and shell Hamiltonian.
"""

from __future__ import annotations

import unittest

from python.closure_read import diag, matmul, matrix_equal, shell_hamiltonian


class TestMatrixUtilities(unittest.TestCase):

    def test_diag_3x3(self):
        D = diag([1.0, 2.0, 3.0])
        self.assertEqual(D, [[1.0, 0.0, 0.0],
                             [0.0, 2.0, 0.0],
                             [0.0, 0.0, 3.0]])

    def test_diag_2x2(self):
        D = diag([5.0, 7.0])
        self.assertEqual(D, [[5.0, 0.0], [0.0, 7.0]])

    def test_matmul_identity(self):
        I = diag([1.0, 1.0, 1.0])
        A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]]
        self.assertEqual(matmul(I, A), A)
        self.assertEqual(matmul(A, I), A)

    def test_matmul_2x2(self):
        A = [[1.0, 2.0], [3.0, 4.0]]
        B = [[5.0, 6.0], [7.0, 8.0]]
        # A*B = [[19, 22], [43, 50]]
        result = matmul(A, B)
        self.assertEqual(result, [[19.0, 22.0], [43.0, 50.0]])

    def test_matrix_equal_within_tol(self):
        A = [[1.0, 2.0], [3.0, 4.0]]
        B = [[1.0 + 1e-15, 2.0], [3.0, 4.0]]
        self.assertTrue(matrix_equal(A, B, tol=1e-12))

    def test_matrix_equal_outside_tol(self):
        A = [[1.0, 2.0], [3.0, 4.0]]
        B = [[1.0 + 1e-6, 2.0], [3.0, 4.0]]
        self.assertFalse(matrix_equal(A, B, tol=1e-12))


class TestShellHamiltonian(unittest.TestCase):

    def test_H4(self):
        """H_4 = diag(13, 17, 21)."""
        H = shell_hamiltonian(4)
        self.assertEqual(H, [[13, 0, 0], [0, 17, 0], [0, 0, 21]])

    def test_H5(self):
        """H_5 = diag(21, 26, 31)."""
        H = shell_hamiltonian(5)
        self.assertEqual(H, [[21, 0, 0], [0, 26, 0], [0, 0, 31]])

    def test_H4_trace_is_phi3(self):
        """Sum of diagonal = Phi_3(K) at K=4 is 13+17+21 = 51 = sum of shell traces."""
        H = shell_hamiltonian(4)
        trace = sum(H[i][i] for i in range(len(H)))
        self.assertEqual(trace, 13 + 17 + 21)


# =============================================================================
# Phase 3 additions: T_<=2(V), Gram matrix, sec(theta_K), Hilbert polynomial
# =============================================================================

from math import acos, cos  # noqa: E402

from python.closure_read import (  # noqa: E402
    gram_eigenvalues,
    gram_matrix_K,
    graded_identity_trace,
    hilbert_polynomial,
    parity_overlap_angle,
    parity_projector_dimensions,
    sec_theta_K,
    truncated_tensor_algebra,
    verify_17_over_13_is_sec_theta_4,
)


class TestTruncatedTensorAlgebra(unittest.TestCase):

    def test_K_4_dimensions(self):
        result = truncated_tensor_algebra(4)
        self.assertEqual(result["dim_trivial"], 1)
        self.assertEqual(result["dim_V"], 4)
        self.assertEqual(result["dim_V_tensor_V"], 16)
        self.assertEqual(result["total_dimension"], 21)
        self.assertEqual(result["even_dimension"], 17)    # 1 + 16
        self.assertEqual(result["odd_dimension"], 4)
        self.assertEqual(result["superdimension"], 13)    # 17 - 4
        self.assertEqual(result["shell"], (13, 17, 21))

    def test_E_minus_O_equals_phi6(self):
        """E - O = (K^2 + 1) - K = K^2 - K + 1 = Phi_6(K)."""
        for K in [2, 3, 4, 5, 6]:
            from python.cyclotomic import phi6
            result = truncated_tensor_algebra(K)
            self.assertEqual(result["even_dimension"] - result["odd_dimension"],
                             phi6(K))


class TestParityProjectorDimensions(unittest.TestCase):

    def test_at_K_4(self):
        dims = parity_projector_dimensions(4)
        self.assertEqual(dims, {"P_0": 1, "P_1": 4, "P_2": 16})

    def test_sum_to_K_squared_plus_K_plus_1(self):
        """Sum of projector dimensions = Phi_3(K) = K^2 + K + 1."""
        for K in [2, 3, 4, 5]:
            dims = parity_projector_dimensions(K)
            total = dims["P_0"] + dims["P_1"] + dims["P_2"]
            self.assertEqual(total, K * K + K + 1)


class TestGradedIdentityTrace(unittest.TestCase):

    def test_Tr_at_s_plus_1(self):
        """Tr(I_+1) = 1 + K + K^2 = Phi_3(K)."""
        from python.cyclotomic import phi3
        for K in [2, 3, 4, 5, 6]:
            self.assertEqual(graded_identity_trace(K, +1), phi3(K))

    def test_Tr_at_s_0(self):
        """Tr(I_0) = 1 + K^2 = Phi_4(K)."""
        from python.cyclotomic import phi4
        for K in [2, 3, 4, 5, 6]:
            self.assertEqual(graded_identity_trace(K, 0), phi4(K))

    def test_Tr_at_s_minus_1(self):
        """Tr(I_-1) = 1 - K + K^2 = Phi_6(K)."""
        from python.cyclotomic import phi6
        for K in [2, 3, 4, 5, 6]:
            self.assertEqual(graded_identity_trace(K, -1), phi6(K))


class TestGramMatrix(unittest.TestCase):

    def test_K_4_gram_is_17_13_13_17(self):
        G = gram_matrix_K(4)
        self.assertEqual(G, ((17, 13), (13, 17)))

    def test_diagonal_is_phi4(self):
        """G_{ii} = E = Phi_4(K)."""
        from python.cyclotomic import phi4
        for K in [2, 3, 4, 5]:
            G = gram_matrix_K(K)
            self.assertEqual(G[0][0], phi4(K))
            self.assertEqual(G[1][1], phi4(K))

    def test_off_diagonal_is_phi6(self):
        """G_{ij} (i!=j) = E - O = Phi_6(K)."""
        from python.cyclotomic import phi6
        for K in [2, 3, 4, 5]:
            G = gram_matrix_K(K)
            self.assertEqual(G[0][1], phi6(K))
            self.assertEqual(G[1][0], phi6(K))


class TestGramEigenvalues(unittest.TestCase):

    def test_K_4_eigenvalues(self):
        """Eigenvalues at K=4: {2E - O, O} = {30, 4}."""
        eigs = gram_eigenvalues(4)
        self.assertEqual(eigs["lambda_symmetric_2E_minus_O"], 30)
        self.assertEqual(eigs["lambda_antisymmetric_O"], 4)

    def test_antisymmetric_eigenvalue_equals_K(self):
        """Antisymmetric eigenvalue equals K exactly at any K."""
        for K in [2, 3, 4, 5, 6, 7, 8]:
            eigs = gram_eigenvalues(K)
            self.assertEqual(eigs["lambda_antisymmetric_O"], K)

    def test_eigenvalue_sum_is_trace(self):
        """lambda_+ + lambda_- = 2E = trace of G_K."""
        for K in [2, 3, 4, 5]:
            eigs = gram_eigenvalues(K)
            self.assertEqual(
                eigs["lambda_symmetric_2E_minus_O"] + eigs["lambda_antisymmetric_O"],
                eigs["trace_2E"])


class TestParityOverlapAngle(unittest.TestCase):

    def test_theta_4_cosine(self):
        """cos(theta_4) = 13/17."""
        self.assertAlmostEqual(cos(parity_overlap_angle(4)), 13.0 / 17.0,
                               places=12)

    def test_theta_4_arccos(self):
        """theta_4 = arccos(13/17) = 40.119 degrees ~ 0.6997 rad."""
        from math import degrees
        theta = parity_overlap_angle(4)
        # arccos(13/17) is approximately 40.119 degrees, not exactly 40
        self.assertAlmostEqual(degrees(theta), 40.1192, places=3)


class TestSecThetaK(unittest.TestCase):

    def test_sec_theta_4_is_17_over_13(self):
        self.assertAlmostEqual(sec_theta_K(4), 17.0 / 13.0, places=12)

    def test_verify_helper(self):
        """The dedicated verifier returns True."""
        self.assertTrue(verify_17_over_13_is_sec_theta_4())

    def test_sec_at_K_5_is_26_over_21(self):
        self.assertAlmostEqual(sec_theta_K(5), 26.0 / 21.0, places=12)


class TestHilbertPolynomial(unittest.TestCase):

    def test_H_at_t_plus_1_is_phi3(self):
        """H_K(+1) = 1 + K + K^2 = Phi_3(K)."""
        from python.cyclotomic import phi3
        for K in [2, 3, 4, 5, 6]:
            self.assertEqual(hilbert_polynomial(K, 1), phi3(K))

    def test_H_at_t_minus_1_is_phi6(self):
        """H_K(-1) = 1 - K + K^2 = Phi_6(K)."""
        from python.cyclotomic import phi6
        for K in [2, 3, 4, 5, 6]:
            self.assertEqual(hilbert_polynomial(K, -1), phi6(K))

    def test_average_at_pm_1_is_phi4(self):
        """(H_K(+1) + H_K(-1)) / 2 = Phi_4(K)."""
        from python.cyclotomic import phi4
        for K in [2, 3, 4, 5, 6]:
            avg = (hilbert_polynomial(K, 1) + hilbert_polynomial(K, -1)) / 2.0
            self.assertAlmostEqual(avg, phi4(K))


class TestParitySheetInclusionExclusion(unittest.TestCase):
    """Inclusion-exclusion reading: |A| + |B| - |A intersect B| = |A union B|."""

    def test_K4_sheet_sizes_and_intersection_union(self):
        from python.closure_read import parity_sheet_inclusion_exclusion
        d = parity_sheet_inclusion_exclusion(4)
        self.assertEqual(d['sheet_A_size'], 17)
        self.assertEqual(d['sheet_B_size'], 17)
        self.assertEqual(d['intersection_size'], 13)
        self.assertEqual(d['union_size'], 21)
        self.assertTrue(d['inclusion_exclusion_holds'])

    def test_K4_parity_decomposition_holds(self):
        # 21 = 13 + 4 + 4 (core + sheet-exclusive x 2)
        from python.closure_read import parity_sheet_inclusion_exclusion
        d = parity_sheet_inclusion_exclusion(4)
        self.assertTrue(d['parity_decomposition_holds'])
        self.assertEqual(d['sheet_minus_core'], 4)

    def test_impedance_at_K_4_is_17_over_13(self):
        from python.closure_read import parity_sheet_inclusion_exclusion
        d = parity_sheet_inclusion_exclusion(4)
        self.assertAlmostEqual(d['impedance_Z_K'], 17 / 13, places=12)

    def test_inclusion_exclusion_holds_for_K_2_through_6(self):
        from python.closure_read import parity_sheet_inclusion_exclusion
        for K in (2, 3, 4, 5, 6):
            d = parity_sheet_inclusion_exclusion(K)
            self.assertTrue(d['inclusion_exclusion_holds'])
            self.assertTrue(d['parity_decomposition_holds'])


class TestParitySheetDotProducts(unittest.TestCase):
    """Gram-matrix dot products: <A,A> = <B,B> = 17, <A,B> = 13 at K=4."""

    def test_K4_self_overlaps_equal_17(self):
        from python.closure_read import parity_sheet_dot_products
        d = parity_sheet_dot_products(4)
        self.assertEqual(d['A_dot_A'], 17)
        self.assertEqual(d['B_dot_B'], 17)

    def test_K4_cross_overlap_equals_13(self):
        from python.closure_read import parity_sheet_dot_products
        d = parity_sheet_dot_products(4)
        self.assertEqual(d['A_dot_B'], 13)

    def test_cos_theta_K_equals_13_over_17_at_K_4(self):
        from python.closure_read import parity_sheet_dot_products
        d = parity_sheet_dot_products(4)
        self.assertAlmostEqual(d['cos_theta_K'], 13 / 17, places=12)

    def test_sec_theta_K_equals_17_over_13_at_K_4(self):
        from python.closure_read import parity_sheet_dot_products
        d = parity_sheet_dot_products(4)
        self.assertAlmostEqual(d['sec_theta_K'], 17 / 13, places=12)

    def test_dot_products_are_phi4_and_phi6_for_K_2_through_6(self):
        from python.closure_read import parity_sheet_dot_products
        from python.cyclotomic import phi4, phi6
        for K in (2, 3, 4, 5, 6):
            d = parity_sheet_dot_products(K)
            self.assertEqual(d['A_dot_A'], phi4(K))
            self.assertEqual(d['B_dot_B'], phi4(K))
            self.assertEqual(d['A_dot_B'], phi6(K))


class TestParityOverlapAngleGeometric(unittest.TestCase):
    """Geometric construction of theta_K from the dot products."""

    def test_geometric_matches_algebraic_at_K_4(self):
        from python.closure_read import (parity_overlap_angle,
                                         parity_overlap_angle_geometric)
        self.assertAlmostEqual(parity_overlap_angle(4),
                               parity_overlap_angle_geometric(4),
                               places=12)

    def test_geometric_matches_algebraic_for_K_2_through_6(self):
        from python.closure_read import (parity_overlap_angle,
                                         parity_overlap_angle_geometric)
        for K in (2, 3, 4, 5, 6):
            self.assertAlmostEqual(parity_overlap_angle(K),
                                   parity_overlap_angle_geometric(K),
                                   places=12)


if __name__ == "__main__":
    unittest.main()
