"""
test_unification_algebra.py
=============================

Tests for the unification-algebra module.  Each theorem T1-T8 from the
two canonical synthesis documents gets a verification.
"""

import unittest

from python.unification_algebra import (
    UnificationAlgebra,
    uniqueness_equation_residual,
    vertex_count_uniqueness_check,
    expected_eigenspectrum_multiplicities,
    eigenspectrum_matches_binomial_row,
    eigenspectrum_uniqueness_check,
    phi_at_negative_K, phi_at_K_minus_1, phi_n_value,
    parity_shift_collapse_at_phi3,
    parity_shift_collapse_fails_for,
    parity_shift_uniqueness_check,
    k_scaling_trace_on_channel,
    coupling_polynomial_trace_check,
    three_factorizations_of_S_3_K,
    connection_split_from_coupling,
    discriminant_constraint_scan,
    range_equals_2K_equals_2D,
    three_uniqueness_routes_to_D3,
    pipeline_stages_summary,
    showcase_unification_algebra,
)


# ===========================================================================
# T1 — vertex-count uniqueness  2(D+1) = 2^D
# ===========================================================================

class TestT1VertexCountUniqueness(unittest.TestCase):

    def test_residual_zero_at_D3(self):
        self.assertEqual(uniqueness_equation_residual(3), 0)

    def test_residual_nonzero_elsewhere(self):
        for D in (1, 2, 4, 5, 6, 7, 8):
            self.assertNotEqual(uniqueness_equation_residual(D), 0,
                                msg=f"unexpected solution at D={D}")

    def test_D3_is_unique_solution(self):
        result = vertex_count_uniqueness_check(d_max=12)
        self.assertEqual(result["solutions"], [3])
        self.assertTrue(result["unique_solution"])


# ===========================================================================
# T2 — eigenspectrum {1,D,D,1} matches binomial row D only at D=3
# ===========================================================================

class TestT2EigenspectrumMatch(unittest.TestCase):

    def test_multiplicities_at_D3_are_1_3_3_1(self):
        self.assertEqual(expected_eigenspectrum_multiplicities(3), (1, 3, 3, 1))

    def test_match_only_at_D3(self):
        for D in range(1, 9):
            ok = eigenspectrum_matches_binomial_row(D)
            if D == 3:
                self.assertTrue(ok, msg=f"D=3 should match")
            else:
                self.assertFalse(ok, msg=f"D={D} unexpectedly matches")

    def test_unique_solution_check(self):
        result = eigenspectrum_uniqueness_check(d_max=8)
        self.assertEqual(result["solutions"], [3])


# ===========================================================================
# T3 — parity-shift-conjugation collapse  Phi_3(-K) = Phi_3(K-1) = Phi_6(K)
# ===========================================================================

class TestT3ParityShiftCollapse(unittest.TestCase):

    def test_collapse_at_phi3_K4(self):
        r = parity_shift_collapse_at_phi3(4)
        self.assertEqual(r["phi3_minus_K"], 13)
        self.assertEqual(r["phi3_K_minus_1"], 13)
        self.assertEqual(r["phi6_K"], 13)
        self.assertTrue(r["all_equal"])

    def test_collapse_at_phi3_general_K(self):
        # Test the identity at several K values
        for K in (2, 3, 4, 5, 7, 10):
            r = parity_shift_collapse_at_phi3(K)
            self.assertTrue(r["all_equal"],
                            msg=f"identity should hold at K={K}: {r}")

    def test_collapse_fails_at_phi4(self):
        # Phi_4(-K) = K^2 + 1; Phi_4(K-1) = (K-1)^2 + 1.
        # At K=4: Phi_4(-4) = 17, Phi_4(3) = 10.  Should NOT be equal.
        self.assertTrue(parity_shift_collapse_fails_for(4, K=4))

    def test_collapse_fails_at_phi5(self):
        self.assertTrue(parity_shift_collapse_fails_for(5, K=4))

    def test_collapse_fails_at_phi6(self):
        # Note: Phi_6 has symmetry axis at +1/2, not -1/2, so
        # Phi_6(-K) != Phi_6(K-1) in general.
        # Phi_6(-K) = K^2 + K + 1; Phi_6(K-1) = K^2 - 3K + 3.
        # At K=4: 21 vs 7.  Identity fails.
        self.assertTrue(parity_shift_collapse_fails_for(6, K=4))

    def test_phi3_is_the_unique_solution(self):
        result = parity_shift_uniqueness_check(K=4)
        self.assertEqual(result["solutions"], [3])
        self.assertTrue(result["unique_solution_n3"])


# ===========================================================================
# T4 — Coupling polynomial as trace on K-scaling
# ===========================================================================

class TestT4CouplingPolynomialAsTrace(unittest.TestCase):

    def test_trace_on_axial_channel(self):
        # s = 0: Gaussian axial, char poly = K^2 + 1
        self.assertEqual(k_scaling_trace_on_channel(4, 0), 17)

    def test_trace_on_eisenstein_plus(self):
        # s = +1: K^2 + K + 1
        self.assertEqual(k_scaling_trace_on_channel(4, 1), 21)

    def test_trace_on_eisenstein_minus(self):
        # s = -1: K^2 - K + 1
        self.assertEqual(k_scaling_trace_on_channel(4, -1), 13)

    def test_trace_matches_coupling_polynomial(self):
        result = coupling_polynomial_trace_check(4)
        self.assertTrue(result["all_match"])
        for s in (-1, 0, 1):
            self.assertEqual(result["by_s"][s]["polynomial"],
                             result["by_s"][s]["channel_trace"])

    def test_trace_matches_at_general_K(self):
        for K in (3, 4, 5, 7, 10):
            result = coupling_polynomial_trace_check(K)
            self.assertTrue(result["all_match"],
                            msg=f"mismatch at K={K}: {result}")


# ===========================================================================
# T5 — Three factorizations of S(3, K)
# ===========================================================================

class TestT5ThreeFactorizationsOfS3K(unittest.TestCase):

    def test_three_factorizations_at_K4(self):
        r = three_factorizations_of_S_3_K(4)
        self.assertEqual(r["S_3_K"], 273)
        self.assertEqual(r["phi3_times_phi6"], 273)
        self.assertEqual(r["phi3_times_phi3_neg_K"], 273)
        self.assertEqual(r["phi3_times_phi3_K_minus_1"], 273)
        self.assertTrue(r["all_equal"])

    def test_three_factorizations_at_general_K(self):
        for K in (2, 3, 4, 5, 6, 7, 10):
            r = three_factorizations_of_S_3_K(K)
            self.assertTrue(r["all_equal"],
                            msg=f"factorizations diverge at K={K}: {r}")


# ===========================================================================
# T6 — Connection decomposition from (f-1)/2
# ===========================================================================

class TestT6ConnectionDecomposition(unittest.TestCase):

    def test_retained_per_face_is_C_K_plus_1_2(self):
        r = connection_split_from_coupling(4)
        self.assertEqual(r["retained_per_face"], 10)  # C(5,2) = 10
        self.assertEqual(r["binom_K_plus_1_choose_2"], 10)
        self.assertEqual(r["retained_per_face"], r["binom_K_plus_1_choose_2"])

    def test_discarded_per_face_is_C_K_2(self):
        r = connection_split_from_coupling(4)
        self.assertEqual(r["discarded_per_face"], 6)  # C(4,2) = 6
        self.assertEqual(r["binom_K_choose_2"], 6)

    def test_total_recovers_40_24_split(self):
        r = connection_split_from_coupling(4)
        self.assertEqual(r["retained_total"], 40)
        self.assertEqual(r["discarded_total"], 24)
        self.assertEqual(r["total"], 64)
        self.assertEqual(r["K_cubed"], 64)

    def test_split_aligns_with_closure_core_tile(self):
        # closure_core256.SierpinskiTile64 gives 40/24 from a different
        # construction.  The two should give identical numbers.
        r = connection_split_from_coupling(4)
        from python.closure_core256 import coupling_summary
        s = coupling_summary(4)
        self.assertEqual(r["retained_total"], s["four_face_sym"])
        self.assertEqual(r["discarded_total"], s["four_face_ext"])


# ===========================================================================
# T7 — Discriminant constraint s^2 < 4
# ===========================================================================

class TestT7DiscriminantConstraint(unittest.TestCase):

    def test_irreducible_iff_s_in_minus1_0_plus1(self):
        r = discriminant_constraint_scan(s_range=4)
        self.assertEqual(set(r["irreducible_s"]), {-1, 0, 1})
        self.assertTrue(r["matches_parity_tag"])

    def test_discriminant_negative_for_parity_tags(self):
        r = discriminant_constraint_scan(s_range=4)
        for s in (-1, 0, 1):
            self.assertLess(r["by_s"][s]["discriminant"], 0)

    def test_discriminant_nonnegative_outside_parity_tags(self):
        r = discriminant_constraint_scan(s_range=4)
        for s in (-4, -3, -2, 2, 3, 4):
            self.assertGreaterEqual(r["by_s"][s]["discriminant"], 0)


# ===========================================================================
# T8 — Range identity Delta f = 2K = 2^D at D=3
# ===========================================================================

class TestT8RangeIdentity(unittest.TestCase):

    def test_range_at_D3_K4_equals_8(self):
        r = range_equals_2K_equals_2D(3)
        self.assertEqual(r["delta_f"], 8)
        self.assertEqual(r["two_K"], 8)
        self.assertEqual(r["two_D"], 8)
        self.assertTrue(r["all_equal"])

    def test_uniqueness_equation_at_D3(self):
        # 2(D+1) = 2^D at D=3 means 8 = 8.  The range Delta f at D=3
        # is the same equation read off the coupling polynomial.
        r = range_equals_2K_equals_2D(3)
        self.assertEqual(r["delta_f"], 2 * (3 + 1))
        self.assertEqual(r["delta_f"], 2 ** 3)

    def test_range_fails_uniqueness_elsewhere(self):
        # 2K = 2^D only when D=3 (and degenerately D=1, K=2).
        # Verify at D=4: 2K = 10, 2^D = 16, not equal.
        r = range_equals_2K_equals_2D(4)
        self.assertNotEqual(r["two_K"], r["two_D"])


# ===========================================================================
# Three uniqueness routes combined
# ===========================================================================

class TestThreeUniquenessRoutesConverge(unittest.TestCase):

    def test_all_three_routes_force_D3(self):
        routes = three_uniqueness_routes_to_D3()
        self.assertTrue(routes["all_three_force_D3"])

    def test_routes_are_genuinely_independent(self):
        # Each route uses different mathematics:
        #   T1: vertex count Diophantine equation
        #   T2: binomial coefficient pattern
        #   T3: cyclotomic symmetry axis identity
        routes = three_uniqueness_routes_to_D3()
        self.assertEqual(routes["T1_vertex_count"]["solutions"], [3])
        self.assertEqual(routes["T2_eigenspectrum"]["solutions"], [3])
        self.assertEqual(routes["T3_parity_shift"]["solutions"], [3])


# ===========================================================================
# UnificationAlgebra dataclass
# ===========================================================================

class TestUnificationAlgebraDataclass(unittest.TestCase):

    def test_canonical_is_n3_K4(self):
        A = UnificationAlgebra.canonical()
        self.assertEqual(A.n, 3)
        self.assertEqual(A.K, 4)

    def test_canonical_total_dim_is_8(self):
        A = UnificationAlgebra.canonical()
        self.assertEqual(A.total_dim, 8)
        self.assertEqual(A.axial_dim + A.middle_dim, A.total_dim)

    def test_canonical_decomposition_string(self):
        A = UnificationAlgebra.canonical()
        self.assertIn("<1, I>", A.decomposition)
        self.assertIn("Z[omega]", A.decomposition)

    def test_canonical_is_frozen(self):
        # Verify the dataclass is immutable (architectural invariant)
        A = UnificationAlgebra.canonical()
        with self.assertRaises(Exception):
            A.n = 4


# ===========================================================================
# Pipeline stages summary
# ===========================================================================

class TestPipelineStagesSummary(unittest.TestCase):

    def test_pipeline_has_10_stages(self):
        stages = pipeline_stages_summary()
        self.assertEqual(len(stages), 10)

    def test_each_stage_has_implementation_pointer(self):
        stages = pipeline_stages_summary()
        for s in stages:
            self.assertIn("implementation", s)
            self.assertTrue(s["implementation"],
                            msg=f"stage {s['stage']} has empty implementation")

    def test_stage_names_match_canonical_pipeline(self):
        # Canonical names from appendix G stage headers.
        stages = pipeline_stages_summary()
        names = [s["name"] for s in stages]
        for required in ("State law", "Orientation cocycle", "Closure operator",
                         "Decomposition", "Coupling polynomial",
                         "Operator algebra", "Closure norm",
                         "Projective tower", "Hardware target",
                         "Dynamical realization"):
            self.assertIn(required, names, msg=f"missing stage: {required}")


# ===========================================================================
# Showcase coherence
# ===========================================================================

class TestShowcase(unittest.TestCase):

    def test_showcase_returns_lines(self):
        lines = showcase_unification_algebra()
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 20)

    def test_showcase_mentions_all_three_uniqueness_routes(self):
        joined = "\n".join(showcase_unification_algebra())
        for token in ("T1 vertex count", "T2 eigenspectrum", "T3 parity-shift"):
            self.assertIn(token, joined)

    def test_showcase_mentions_load_bearing_numbers(self):
        joined = "\n".join(showcase_unification_algebra())
        # The numbers the framework cares about
        for token in ("273", "40", "24", "21", "17", "13"):
            self.assertIn(token, joined)

    def test_showcase_mentions_the_pipeline_stages(self):
        joined = "\n".join(showcase_unification_algebra())
        for token in ("State law", "Decomposition", "Hardware target"):
            self.assertIn(token, joined)
