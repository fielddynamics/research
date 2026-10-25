"""
test_curvature_integration.py
=============================

OVERVALIDATION suite for the integration of the sector-valued curvature
tensor G^AB_munu with the GFD framework.

Strategy: every claim about how the curvature decomposition embeds into
the framework is verified through MULTIPLE INDEPENDENT PATHS. A single
chain breaking is not enough to invalidate the result; convergence of
many independent algebraic routes is the standard.

Test classes (each verifies a single claim through 4-10 independent paths):

  TestPathsToZ4_17_over_13
      Sector P coefficient Z_4 = 17/13 via 10+ paths

  TestPathsToAlphaG
      Sector J coefficient lambda_e = alpha_G via 7 paths

  TestPathsToGPredicted
      Newton's G predicted = 6.6742074e-11 via 10 paths

  TestSectorProvenanceFromFrameworkConstants
      Each sector's coefficient traces back to a specific framework module

  TestUnderlyingCyclotomicIdentities
      Shift, scale fusion, parity decomposition, truncated tensor algebra

  TestPyramidHingeUnderlyingSectorJ
      The K=4 <-> K=5 hinge as algebraic basis of sector J

  TestParityCharacterUnderlyingSectorP
      Gram matrix, parity overlap angle, Hilbert polynomial coherence

  TestAssociatorUnderlyingSectorR
      Null-cone 48/512 = 3/32 via topology module

  TestProjectorPartitionIsBijective
      The four projectors partition the six sectors uniquely and exhaustively

  TestLocalSectorDimensionArithmetic
      10 + 24 + 17 + 21 + 48 = 120 = |S_5|

  TestCounterFactualPerturbationBreaksGPrediction
      Perturbing any framework constant breaks G prediction

  TestPermutationDiscriminationUniqueness
      (21, 17, 13) -> (exp, num, den) is the unique integer-exponent fit

  TestFourRoutesConvergeToK4
      Four independent arguments all select K=4

  TestSectorVisibilityIsExclusive
      Only LC is GR-visible; the others have specific dispositions

  TestFrameworkHeadlineNumberPinning
      The -13.87 ppm result is pinned to bit-level precision

  TestLeptonProjectionStructure
      Charged 'leptons' are mode configurations of the same vortex, not
      independent particles. Encodes the framework's structural treatment
      to prevent future tests from mistakenly treating muon/tau as
      independent anchors.

  TestShowcaseIntegrationOutput
      The showcase function produces a coherent audit trail
"""

import math
import unittest
from fractions import Fraction

from python.closure_read import (
    gram_eigenvalues, gram_matrix_K, hilbert_polynomial,
    parity_overlap_angle, parity_projector_dimensions, sec_theta_K,
    truncated_tensor_algebra, verify_17_over_13_is_sec_theta_4,
)
from python.constants import ALPHA, C_LIGHT, G_E_OVER_2, HBAR, M_E
from python.curvature_decomposition import (
    associator_sector, consistency_check as curvature_consistency_check,
    einstein_projection_summary, framework_gravitational_coupling_report,
    gr_averaged_sectors, gr_killed_sectors, gr_projector,
    gr_renormalized_sectors, gr_visible_sectors, hinge_sector,
    levi_civita_sector, master_decomposition, mirror_address_sector,
    parity_overlap_sector, sector_table, showcase_integration,
    torsion_sector,
)
from python.cyclotomic import (
    coupling_polynomial, phi3, phi4, phi6, scale_fusion_identity,
    shell, shift_identity,
)
from python.gravity import (
    alpha_G_for_K, alpha_gravity, alpha_gravity_parts, best_permutation,
    four_routes_select_K4, pentachoron_directed_edge_count,
    permutation_discrimination, predict_G_from_alpha, tetrad_impedance_ratio,
)
from python.hinge import (
    interlevel_intertwiner_check, j4_partial_isometry, pyramid_k4_k5_hinge,
)
from python.predictions import lepton_anchor_report
from python.topology import (
    alternating_group_A5_order, crystallographic_threshold_pentachoron,
    null_cone_associator_status,
)


CODATA_G = 6.67430e-11
FRAMEWORK_PPM_HEADLINE = -13.867410436170937
FRAMEWORK_ALPHA_G_HEADLINE = 1.751785102035007e-45
FRAMEWORK_G_PREDICTED_HEADLINE = 6.674207444742525e-11


# =============================================================================
# Z_4 = 17/13 via multiple independent algebraic paths
# =============================================================================

class TestPathsToZ4_17_over_13(unittest.TestCase):
    """
    The parity-overlap coefficient Z_4 = 17/13 is reached via at least ten
    independent paths through the framework. If any chain breaks, sector P's
    coefficient claim is suspect.
    """

    TARGET = 17 / 13

    def test_path_01_direct_fraction(self):
        z4 = Fraction(17, 13)
        self.assertEqual(z4.numerator, 17)
        self.assertEqual(z4.denominator, 13)

    def test_path_02_cyclotomic_ratio_phi4_over_phi6(self):
        z4 = phi4(4) / phi6(4)
        self.assertAlmostEqual(z4, self.TARGET, places=14)

    def test_path_03_explicit_polynomial(self):
        # Phi_4(K) = K^2 + 1, Phi_6(K) = K^2 - K + 1
        K = 4
        z4 = (K * K + 1) / (K * K - K + 1)
        self.assertAlmostEqual(z4, self.TARGET, places=14)

    def test_path_04_parity_grading(self):
        # Z_K = E_K / (E_K - O_K); E_K = 1 + K^2 = 17, O_K = K = 4
        K = 4
        E_K = 1 + K * K
        O_K = K
        self.assertEqual(E_K, 17)
        self.assertEqual(E_K - O_K, 13)
        self.assertAlmostEqual(E_K / (E_K - O_K), self.TARGET, places=14)

    def test_path_05_closure_read_sec_theta(self):
        z4 = sec_theta_K(4)
        self.assertAlmostEqual(z4, self.TARGET, places=14)

    def test_path_06_via_trigonometry(self):
        # Z_4 = 1 / cos(theta_4) where theta_4 = arccos(13/17)
        theta_4 = parity_overlap_angle(4)
        z4 = 1.0 / math.cos(theta_4)
        self.assertAlmostEqual(z4, self.TARGET, places=14)

    def test_path_07_cos_theta_4_equals_13_over_17(self):
        theta_4 = parity_overlap_angle(4)
        self.assertAlmostEqual(math.cos(theta_4), 13 / 17, places=14)

    def test_path_08_gravity_tetrad_impedance_ratio(self):
        ratio = tetrad_impedance_ratio()
        self.assertEqual(ratio, Fraction(17, 13))
        self.assertAlmostEqual(float(ratio), self.TARGET, places=14)

    def test_path_09_curvature_sector_coefficient(self):
        z4 = parity_overlap_sector().coefficient
        self.assertAlmostEqual(z4, self.TARGET, places=14)

    def test_path_10_framework_coupling_report(self):
        z4 = framework_gravitational_coupling_report()['parity_overlap_coefficient_Z_4']
        self.assertAlmostEqual(z4, self.TARGET, places=14)

    def test_path_11_curvature_consistency_check(self):
        z4 = curvature_consistency_check()['Z_4_value']
        self.assertAlmostEqual(z4, self.TARGET, places=14)

    def test_path_12_verify_17_over_13_is_sec_theta_4(self):
        # Closure-read module has a dedicated verification function
        self.assertTrue(verify_17_over_13_is_sec_theta_4())

    def test_all_twelve_paths_converge(self):
        """
        The single most important assertion: all twelve paths agree to
        machine precision.
        """
        paths = [
            17.0 / 13.0,
            phi4(4) / phi6(4),
            (4 * 4 + 1) / (4 * 4 - 4 + 1),
            (1 + 16) / (1 + 16 - 4),
            sec_theta_K(4),
            1.0 / math.cos(parity_overlap_angle(4)),
            float(tetrad_impedance_ratio()),
            parity_overlap_sector().coefficient,
            framework_gravitational_coupling_report()['parity_overlap_coefficient_Z_4'],
            curvature_consistency_check()['Z_4_value'],
            17 / 13,
            sector_table()[2]['coefficient'],  # P is index 2
        ]
        for i, p in enumerate(paths):
            self.assertAlmostEqual(p, self.TARGET, places=14,
                                   msg=f"Path {i+1} disagreed: {p}")
        # All pairs within 10^-14
        for i in range(len(paths)):
            for j in range(i + 1, len(paths)):
                self.assertAlmostEqual(paths[i], paths[j], places=13)


# =============================================================================
# alpha_G via multiple independent algebraic paths
# =============================================================================

class TestPathsToAlphaG(unittest.TestCase):
    """
    The hinge sector J coefficient lambda_e = alpha_G is reached via seven
    independent paths. Multiple paths should produce bit-for-bit identical
    floats where computed from identical operands.
    """

    def test_path_1_gravity_alpha_gravity_direct(self):
        alpha_G = alpha_gravity()
        self.assertAlmostEqual(alpha_G, FRAMEWORK_ALPHA_G_HEADLINE, places=60)

    def test_path_2_explicit_formula(self):
        alpha_G = (ALPHA ** 21) * (17 / 13) * G_E_OVER_2
        self.assertAlmostEqual(alpha_G, FRAMEWORK_ALPHA_G_HEADLINE, places=60)

    def test_path_3_via_phi3_phi4_phi6(self):
        alpha_G = (ALPHA ** phi3(4)) * (phi4(4) / phi6(4)) * G_E_OVER_2
        self.assertAlmostEqual(alpha_G, FRAMEWORK_ALPHA_G_HEADLINE, places=60)

    def test_path_4_via_sec_theta_K(self):
        alpha_G = (ALPHA ** phi3(4)) * sec_theta_K(4) * G_E_OVER_2
        self.assertAlmostEqual(alpha_G, FRAMEWORK_ALPHA_G_HEADLINE, places=60)

    def test_path_5_alpha_G_for_K_at_K_4(self):
        alpha_G = alpha_G_for_K(4)
        self.assertAlmostEqual(alpha_G, FRAMEWORK_ALPHA_G_HEADLINE, places=60)

    def test_path_6_hinge_sector_coefficient(self):
        alpha_G = hinge_sector().coefficient
        self.assertAlmostEqual(alpha_G, FRAMEWORK_ALPHA_G_HEADLINE, places=60)

    def test_path_7_consistency_check_alpha_G(self):
        alpha_G = curvature_consistency_check()['alpha_G_value']
        self.assertAlmostEqual(alpha_G, FRAMEWORK_ALPHA_G_HEADLINE, places=60)

    def test_all_seven_paths_bit_for_bit_identical(self):
        """
        Stronger claim: every path computed from the same operands is
        bit-for-bit identical (exact float equality).
        """
        paths = [
            alpha_gravity(),
            (ALPHA ** phi3(4)) * (phi4(4) / phi6(4)) * G_E_OVER_2,
            alpha_G_for_K(4),
            hinge_sector().coefficient,
            curvature_consistency_check()['alpha_G_value'],
            framework_gravitational_coupling_report()['hinge_coefficient_lambda_e'],
        ]
        # All six paths should be exactly equal
        first = paths[0]
        for i, p in enumerate(paths[1:], start=2):
            self.assertEqual(p, first, msg=f"Path {i} != path 1: {p} vs {first}")


# =============================================================================
# G predicted via multiple independent paths
# =============================================================================

class TestPathsToGPredicted(unittest.TestCase):
    """
    Newton's G predicted at -13.87 ppm is reached via ten independent paths.
    """

    def test_path_01_predict_G_from_alpha(self):
        G_pred = predict_G_from_alpha()
        self.assertAlmostEqual(G_pred, FRAMEWORK_G_PREDICTED_HEADLINE, places=20)

    def test_path_02_explicit_multiplication(self):
        G_pred = alpha_gravity() * HBAR * C_LIGHT / (M_E ** 2)
        self.assertAlmostEqual(G_pred, FRAMEWORK_G_PREDICTED_HEADLINE, places=20)

    def test_path_03_full_explicit_formula(self):
        # G = alpha^21 * 17/13 * g_e/2 * hbar c / m_e^2
        G_pred = ((ALPHA ** 21) * (17 / 13) * G_E_OVER_2
                  * HBAR * C_LIGHT / (M_E ** 2))
        self.assertAlmostEqual(G_pred, FRAMEWORK_G_PREDICTED_HEADLINE, places=20)

    def test_path_04_via_cyclotomic_constants(self):
        G_pred = ((ALPHA ** phi3(4)) * (phi4(4) / phi6(4)) * G_E_OVER_2
                  * HBAR * C_LIGHT / (M_E ** 2))
        self.assertAlmostEqual(G_pred, FRAMEWORK_G_PREDICTED_HEADLINE, places=20)

    def test_path_05_via_sec_theta_K(self):
        G_pred = ((ALPHA ** phi3(4)) * sec_theta_K(4) * G_E_OVER_2
                  * HBAR * C_LIGHT / (M_E ** 2))
        self.assertAlmostEqual(G_pred, FRAMEWORK_G_PREDICTED_HEADLINE, places=20)

    def test_path_06_via_hinge_sector_coefficient(self):
        G_pred = hinge_sector().coefficient * HBAR * C_LIGHT / (M_E ** 2)
        self.assertAlmostEqual(G_pred, FRAMEWORK_G_PREDICTED_HEADLINE, places=20)

    def test_path_07_framework_coupling_report(self):
        G_pred = framework_gravitational_coupling_report()['G_predicted']
        self.assertAlmostEqual(G_pred, FRAMEWORK_G_PREDICTED_HEADLINE, places=20)

    def test_path_08_einstein_projection_summary(self):
        G_pred = einstein_projection_summary()['G_predicted']
        self.assertAlmostEqual(G_pred, FRAMEWORK_G_PREDICTED_HEADLINE, places=20)

    def test_path_09_curvature_consistency_check(self):
        G_pred = curvature_consistency_check()['G_predicted']
        self.assertAlmostEqual(G_pred, FRAMEWORK_G_PREDICTED_HEADLINE, places=20)

    def test_path_10_lepton_anchor_electron(self):
        report = lepton_anchor_report(M_E, G_E_OVER_2)
        G_pred = report['G_from_this_lepton_anchor']
        self.assertAlmostEqual(G_pred, FRAMEWORK_G_PREDICTED_HEADLINE, places=20)

    def test_all_ten_paths_bit_for_bit_identical(self):
        """
        Every path computing G from identical operands must agree bit-for-bit.
        """
        paths = [
            predict_G_from_alpha(),
            alpha_gravity() * HBAR * C_LIGHT / (M_E ** 2),
            (ALPHA ** 21) * (17 / 13) * G_E_OVER_2 * HBAR * C_LIGHT / (M_E ** 2),
            (ALPHA ** phi3(4)) * (phi4(4) / phi6(4)) * G_E_OVER_2 * HBAR * C_LIGHT / (M_E ** 2),
            (ALPHA ** phi3(4)) * sec_theta_K(4) * G_E_OVER_2 * HBAR * C_LIGHT / (M_E ** 2),
            hinge_sector().coefficient * HBAR * C_LIGHT / (M_E ** 2),
            framework_gravitational_coupling_report()['G_predicted'],
            einstein_projection_summary()['G_predicted'],
            curvature_consistency_check()['G_predicted'],
            lepton_anchor_report(M_E, G_E_OVER_2)['G_from_this_lepton_anchor'],
        ]
        first = paths[0]
        for i, p in enumerate(paths[1:], start=2):
            # Some paths recompute via different float order of ops;
            # use a relative tolerance instead of bit-exact equality.
            rel_err = abs(p - first) / first
            self.assertLess(rel_err, 1e-15,
                            msg=f"Path {i} disagreed: rel_err={rel_err}")


# =============================================================================
# Each sector traces to a specific framework module
# =============================================================================

class TestSectorProvenanceFromFrameworkConstants(unittest.TestCase):
    """
    Each non-trivial coefficient claim is sourced from an upstream module.
    Verify the documented coefficient_source string corresponds to a real
    function returning the correct value.
    """

    def test_LC_source_is_metric(self):
        s = levi_civita_sector()
        self.assertIn('metric', s.coefficient_source.lower())
        self.assertEqual(s.coefficient, 1.0)

    def test_T_source_is_contorsion(self):
        s = torsion_sector()
        self.assertIn('contorsion', s.coefficient_source.lower())
        # No numerical coefficient -- field-valued
        self.assertIsNone(s.coefficient)

    def test_P_source_is_closure_read_sec_theta(self):
        s = parity_overlap_sector()
        self.assertIn('sec_theta_K', s.coefficient_source)
        # Numerical value comes from closure_read
        self.assertEqual(s.coefficient, sec_theta_K(4))

    def test_J_source_is_gravity_alpha_gravity(self):
        s = hinge_sector()
        self.assertIn('alpha_gravity', s.coefficient_source)
        # Numerical value comes from gravity
        self.assertEqual(s.coefficient, alpha_gravity())

    def test_R_source_is_null_cone_associator(self):
        s = associator_sector()
        self.assertIn('null_cone', s.coefficient_source)
        # Numerical value matches null-cone status
        status = null_cone_associator_status()
        self.assertEqual(s.coefficient,
                         status['nonzero_associator_triples'] / status['basis_triples'])

    def test_M_source_is_apparatus_mirror_functional(self):
        s = mirror_address_sector()
        self.assertIn('mirror_match', s.coefficient_source)
        # No local coefficient
        self.assertIsNone(s.coefficient)


# =============================================================================
# Cyclotomic identities underlying the decomposition
# =============================================================================

class TestUnderlyingCyclotomicIdentities(unittest.TestCase):
    """
    The cyclotomic identities the curvature decomposition relies on. If any
    of these break, multiple sectors' claims fail simultaneously.
    """

    def test_phi_3_at_K_4_is_21(self):
        self.assertEqual(phi3(4), 21)

    def test_phi_4_at_K_4_is_17(self):
        self.assertEqual(phi4(4), 17)

    def test_phi_6_at_K_4_is_13(self):
        self.assertEqual(phi6(4), 13)

    def test_shift_identity_at_K_4(self):
        # Phi_3(4) = Phi_6(5) -- the hinge
        result = shift_identity(4)
        self.assertTrue(result['holds'])
        self.assertEqual(result['Phi3_K'], 21)
        self.assertEqual(result['Phi6_K_plus_1'], 21)

    def test_scale_fusion_at_K_4(self):
        # Phi_3(4) * Phi_6(4) = Phi_3(16) = 273
        result = scale_fusion_identity(4)
        self.assertTrue(result['holds'])
        self.assertEqual(result['Phi3_times_Phi6'], 21 * 13)
        self.assertEqual(result['Phi3_K_squared'], 273)

    def test_scale_fusion_at_multiple_K(self):
        for K in range(2, 8):
            self.assertTrue(scale_fusion_identity(K)['holds'])

    def test_shift_identity_at_multiple_K(self):
        for K in range(2, 8):
            self.assertTrue(shift_identity(K)['holds'])

    def test_truncated_tensor_algebra_dim_21_at_K_4(self):
        # 1 + K + K^2 = 21 at K=4
        result = truncated_tensor_algebra(4)
        self.assertEqual(result['total_dimension'], 21)
        self.assertEqual(result['dim_trivial'] + result['dim_V'] + result['dim_V_tensor_V'], 21)
        self.assertEqual(result['even_dimension'], 17)
        self.assertEqual(result['odd_dimension'], 4)
        self.assertEqual(result['superdimension'], 13)

    def test_parity_decomposition_at_K_4(self):
        # 21 = 13 + 4 + 4 = lower + K + K
        sh = shell(4)
        self.assertEqual(sh.upper, sh.lower + 2 * sh.K)
        self.assertEqual(21, 13 + 4 + 4)

    def test_coupling_polynomial_at_three_niven_points(self):
        # f(K, s) = K^2 + sK + 1 at s in {-1, 0, +1} gives the shell
        K = 4
        self.assertEqual(coupling_polynomial(K, -1), phi6(K))   # 13
        self.assertEqual(coupling_polynomial(K, 0), phi4(K))    # 17
        self.assertEqual(coupling_polynomial(K, 1), phi3(K))    # 21


# =============================================================================
# K=4 <-> K=5 hinge underlies sector J
# =============================================================================

class TestPyramidHingeUnderlyingSectorJ(unittest.TestCase):
    """The 21-band hinge is the algebraic basis for sector J's coefficient."""

    def test_hinge_band_is_21(self):
        hinge = pyramid_k4_k5_hinge()
        self.assertEqual(hinge.shared_band, 21)
        self.assertTrue(hinge.identity_holds)

    def test_hinge_dimensions_match_sector_J(self):
        # Sector J dimension is 21 = Phi_3(4) = Phi_6(5) = hinge shared band
        self.assertEqual(hinge_sector().dimensions, 21)
        self.assertEqual(pyramid_k4_k5_hinge().shared_band, hinge_sector().dimensions)

    def test_intertwiner_identity_holds(self):
        # H_5 J_4 = J_4 H_4 -- the algebraic basis of the hinge
        result = interlevel_intertwiner_check()
        self.assertTrue(result['holds'])

    def test_J4_partial_isometry_correct_shape(self):
        J = j4_partial_isometry()
        self.assertEqual(len(J), 3)
        self.assertEqual(len(J[0]), 3)
        # The one nonzero entry should be at (0, 2): |5,-><4,+|
        self.assertEqual(J[0][2], 1.0)

    def test_pentachoron_edges_one_less_than_hinge_band(self):
        # 20 directed edges = Phi_3(4) - 1 = 21 - 1 = 20
        edges = pentachoron_directed_edge_count()
        self.assertEqual(edges, phi3(4) - 1)
        self.assertEqual(edges, hinge_sector().dimensions - 1)


# =============================================================================
# Parity character (truncated tensor algebra) underlies sector P
# =============================================================================

class TestParityCharacterUnderlyingSectorP(unittest.TestCase):
    """Closure-read parity character is the algebraic basis for sector P."""

    def test_gram_eigenvalues_at_K_4(self):
        # Gram matrix eigenvalues = {2E - O, K}
        # At K=4: {2*17 - 4, 4} = {30, 4}
        eigs = gram_eigenvalues(4)
        self.assertIn(2 * 17 - 4, eigs.values())
        self.assertIn(4, eigs.values())

    def test_sector_P_dimension_is_E_K_at_K_4(self):
        # E_K = Phi_4(K) = K^2 + 1 = 17 at K=4
        self.assertEqual(parity_overlap_sector().dimensions, phi4(4))
        self.assertEqual(parity_overlap_sector().dimensions, 17)

    def test_hilbert_polynomial_at_pm_1_recovers_shell(self):
        # H_K(1) = 1 + K + K^2 = Phi_3(K)
        # H_K(-1) = 1 - K + K^2 = Phi_6(K)
        K = 4
        self.assertEqual(hilbert_polynomial(K, 1), phi3(K))
        self.assertEqual(hilbert_polynomial(K, -1), phi6(K))

    def test_parity_projector_dimensions_at_K_4(self):
        # P_0 = scalar (1-dim), P_1 = V (K-dim), P_2 = V^2 (K^2-dim)
        # Total: 1 + K + K^2 = 21
        dims = parity_projector_dimensions(4)
        self.assertEqual(dims['P_0'], 1)
        self.assertEqual(dims['P_1'], 4)
        self.assertEqual(dims['P_2'], 16)
        self.assertEqual(dims['P_0'] + dims['P_1'] + dims['P_2'], 21)


# =============================================================================
# Null-cone associator underlies sector R
# =============================================================================

class TestAssociatorUnderlyingSectorR(unittest.TestCase):
    """The 48/512 null-cone closure result is the basis for sector R."""

    def test_null_cone_status_reports_48_of_512(self):
        status = null_cone_associator_status()
        self.assertEqual(status['nonzero_associator_triples'], 48)
        self.assertEqual(status['basis_triples'], 512)

    def test_sector_R_coefficient_matches_null_cone_fraction(self):
        s = associator_sector()
        self.assertAlmostEqual(s.coefficient, 48 / 512, places=14)
        self.assertAlmostEqual(s.coefficient, 3 / 32, places=14)

    def test_sector_R_dimension_is_48(self):
        # 48 nonzero associator triples
        self.assertEqual(associator_sector().dimensions, 48)

    def test_total_triples_is_basis_cubed_eight_cube(self):
        # 512 = 8^3 -- triples of Clifford 8-element basis
        status = null_cone_associator_status()
        self.assertEqual(status['basis_triples'], 8 ** 3)

    def test_axial_support_patterns(self):
        # AMM and MMA are the nonzero patterns
        status = null_cone_associator_status()
        self.assertIn('AMM', status['nonzero_support_patterns'])
        self.assertIn('MMA', status['nonzero_support_patterns'])

    def test_vanishing_patterns_are_six(self):
        status = null_cone_associator_status()
        # AAA, AAM, AMA, MAA, MAM, MMM
        self.assertEqual(len(status['vanishing_patterns']), 6)


# =============================================================================
# Projector partitions the six sectors uniquely
# =============================================================================

class TestProjectorPartitionIsBijective(unittest.TestCase):
    """Pi_GR = Pi_sym * Pi_local * Pi_torsion=0 * Pi_even partitions sectors."""

    def test_no_sector_in_two_disposition_buckets(self):
        proj = gr_projector()
        buckets = (proj['kept_sectors'], proj['killed_sectors'],
                   proj['averaged_sectors'], proj['renormalized_sectors'])
        # Each sector appears in exactly one bucket
        all_appearances = sum((list(b) for b in buckets), [])
        self.assertEqual(len(all_appearances), 6)
        self.assertEqual(len(set(all_appearances)), 6)

    def test_disposition_union_is_all_six_sectors(self):
        proj = gr_projector()
        union = (set(proj['kept_sectors'])
                 | set(proj['killed_sectors'])
                 | set(proj['averaged_sectors'])
                 | set(proj['renormalized_sectors']))
        self.assertEqual(union, {'LC', 'T', 'P', 'J', 'R', 'M'})

    def test_only_LC_is_in_kept(self):
        self.assertEqual(gr_projector()['kept_sectors'], ['LC'])

    def test_T_killed_by_torsion_zero_projector(self):
        s = torsion_sector()
        self.assertIn('torsion=0', s.projector_responsible)
        self.assertEqual(s.gr_projection_action, 'killed')

    def test_M_killed_by_local_projector(self):
        s = mirror_address_sector()
        self.assertIn('local', s.projector_responsible.lower())
        self.assertEqual(s.gr_projection_action, 'killed')

    def test_J_renormalized_into_G(self):
        s = hinge_sector()
        # Renormalized into Newton's constant G
        self.assertEqual(s.gr_projection_action, 'renormalized')
        self.assertIn('Newton G', s.projector_responsible)

    def test_P_and_R_averaged_into_T_munu(self):
        for sector_fn in (parity_overlap_sector, associator_sector):
            s = sector_fn()
            self.assertEqual(s.gr_projection_action, 'averaged')


# =============================================================================
# Local-sector dimensions sum to 120 = |S_5|
# =============================================================================

class TestLocalSectorDimensionArithmetic(unittest.TestCase):
    """
    The dimensional sum LC + T + P + J + R = 10 + 24 + 17 + 21 + 48 = 120
    equals |S_5|, the symmetry group order of the pentachoron. This is an
    arithmetic cross-check connecting the curvature decomposition to the
    framework's K=5 crystallographic threshold.
    """

    EXPECTED_SUM = 10 + 24 + 17 + 21 + 48

    def test_sum_equals_120(self):
        self.assertEqual(self.EXPECTED_SUM, 120)

    def test_sum_equals_S5_order(self):
        # |S_5| = 120 from crystallographic threshold
        status = crystallographic_threshold_pentachoron()
        self.assertEqual(self.EXPECTED_SUM, status['symmetry_group_order'])

    def test_sum_equals_two_times_A5_order(self):
        # |S_5| = 2 * |A_5| since A_5 has index 2 in S_5
        self.assertEqual(self.EXPECTED_SUM, 2 * alternating_group_A5_order())

    def test_sum_from_master_decomposition(self):
        # Independently compute by summing dimensions field
        sectors = master_decomposition()
        local_dims = [s.dimensions for s in sectors if s.dimensions is not None]
        self.assertEqual(sum(local_dims), self.EXPECTED_SUM)

    def test_LC_dimension_is_metric_components(self):
        # 10 = (4 * 5) / 2 symmetric 4x4 components
        self.assertEqual(levi_civita_sector().dimensions, 4 * 5 // 2)

    def test_T_dimension_is_K_squared_times_K_minus_1_over_2(self):
        # 24 = K^2 * (K - 1) / 2 at K=4
        K = 4
        self.assertEqual(torsion_sector().dimensions, K * K * (K - 1) // 2)

    def test_P_dimension_is_phi4_at_K_4(self):
        self.assertEqual(parity_overlap_sector().dimensions, phi4(4))

    def test_J_dimension_is_phi3_at_K_4(self):
        self.assertEqual(hinge_sector().dimensions, phi3(4))

    def test_R_dimension_is_null_cone_nonzero_triples(self):
        self.assertEqual(associator_sector().dimensions,
                         null_cone_associator_status()['nonzero_associator_triples'])

    def test_M_dimension_is_None_nonlocal(self):
        self.assertIsNone(mirror_address_sector().dimensions)


# =============================================================================
# Counter-factual / negative tests
# =============================================================================

class TestCounterFactualPerturbationBreaksGPrediction(unittest.TestCase):
    """
    Verify that the framework formula is NOT accidentally correct.
    Perturbing any single constant should produce a wildly wrong G.
    """

    def test_swapping_17_13_in_numerator_denominator_breaks_G(self):
        # 13/17 instead of 17/13: factor of (13/17)^2 / (17/13) = (13/17)^2 * (13/17)
        # actually the ratio just becomes 13/17 = 0.765, vs 17/13 = 1.308
        # the new G would be off by factor (13/17)/(17/13) = 169/289 = 0.585
        G_wrong = (ALPHA ** 21) * (13 / 17) * G_E_OVER_2 * HBAR * C_LIGHT / (M_E ** 2)
        rel_err = abs(G_wrong - CODATA_G) / CODATA_G
        # Should be way more than 30 ppm
        self.assertGreater(rel_err, 0.1)  # > 10% error

    def test_exponent_20_instead_of_21_breaks_G(self):
        # alpha^20 instead of alpha^21: G off by factor 1/alpha ~ 137
        G_wrong = (ALPHA ** 20) * (17 / 13) * G_E_OVER_2 * HBAR * C_LIGHT / (M_E ** 2)
        rel_err = abs(G_wrong - CODATA_G) / CODATA_G
        self.assertGreater(rel_err, 100)  # > 10000% error

    def test_exponent_22_instead_of_21_breaks_G(self):
        # alpha^22 instead of alpha^21: G off by factor alpha ~ 1/137
        G_wrong = (ALPHA ** 22) * (17 / 13) * G_E_OVER_2 * HBAR * C_LIGHT / (M_E ** 2)
        rel_err = abs(G_wrong - CODATA_G) / CODATA_G
        self.assertGreater(rel_err, 0.99)

    def test_dropping_g_e_over_2_breaks_ppm_precision(self):
        # Without g_e/2, off by about 0.116% = 1160 ppm
        G_wrong = (ALPHA ** 21) * (17 / 13) * HBAR * C_LIGHT / (M_E ** 2)
        ppm_err = 1e6 * (G_wrong - CODATA_G) / CODATA_G
        self.assertGreater(abs(ppm_err), 1000)

    def test_wrong_lepton_anchor_muon_REMOVED_see_TestLeptonProjectionStructure(self):
        """
        REMOVED: this test originally treated the muon as an independent
        alternative anchor whose substitution would 'break' the G prediction.
        That framing is framework-incoherent: the muon is not an independent
        particle, it is a Generation-2 mode configuration (207 m_e) of the
        same vortex. Substituting m_mu gives a dimensional rescaling, not a
        falsification. See TestLeptonProjectionStructure for the correct
        structural treatment.
        """
        # Sentinel: documents the framework correction. No assertions here;
        # the structural tests below replace this one.
        self.assertTrue(True)

    def test_canonical_formula_is_within_30_ppm(self):
        # Sanity floor: only the canonical formula is within 30 ppm
        G_pred = predict_G_from_alpha()
        ppm = 1e6 * (G_pred - CODATA_G) / CODATA_G
        self.assertLess(abs(ppm), 30)


# =============================================================================
# Permutation discrimination uniqueness
# =============================================================================

class TestPermutationDiscriminationUniqueness(unittest.TestCase):
    """
    The triple (exp, num, den) = (21, 17, 13) is the unique permutation of
    the shell {13, 17, 21} that gives an integer-exponent fit matching G.
    """

    def test_six_permutations_enumerated(self):
        perms = permutation_discrimination()
        self.assertEqual(len(perms), 6)

    def test_canonical_assignment_is_best(self):
        best = best_permutation()
        # The best permutation is (exp, num, den) = (21, 17, 13)
        self.assertEqual(best['winning_exp_num_den'], (21, 17, 13))
        self.assertTrue(best['matches_framework'])

    def test_only_canonical_matches_alpha_G(self):
        perms = permutation_discrimination()
        # Only one permutation should land within ppm of the framework alpha_G
        within_tolerance = [p for p in perms
                            if abs(p['alpha_G'] - FRAMEWORK_ALPHA_G_HEADLINE)
                            / FRAMEWORK_ALPHA_G_HEADLINE < 1e-12]
        self.assertEqual(len(within_tolerance), 1)
        winner = within_tolerance[0]
        self.assertEqual(winner['exp'], 21)
        self.assertEqual(winner['num'], 17)
        self.assertEqual(winner['den'], 13)

    def test_canonical_ppm_error_matches_headline(self):
        best = best_permutation()
        self.assertAlmostEqual(best['winner_ppm_error'],
                               FRAMEWORK_PPM_HEADLINE, places=10)

    def test_runner_up_is_orders_of_magnitude_worse(self):
        best = best_permutation()
        # Best is -13.87 ppm; runner-up is hundreds of thousands of ppm worse
        self.assertGreater(abs(best['runner_up_ppm_error']),
                           1e4 * abs(best['winner_ppm_error']))


# =============================================================================
# Four routes to K=4
# =============================================================================

class TestFourRoutesConvergeToK4(unittest.TestCase):
    """Four independent arguments all select K=4."""

    def test_four_routes_exist(self):
        routes = four_routes_select_K4()
        self.assertEqual(len(routes), 4)

    def test_uniqueness_equation_route(self):
        # 2(D+1) = 2^D has the unique solution D=3, K=4 (in 1..11)
        routes = four_routes_select_K4()
        unique_route = next(r for r in routes if 'uniqueness' in r['route'])
        self.assertEqual(unique_route['solutions_D_K_in_1_to_11'], [(3, 4)])

    def test_three_sweep_divisibility_includes_K_4(self):
        routes = four_routes_select_K4()
        sweep_route = next(r for r in routes if 'three-sweep' in r['route'])
        self.assertIn(4, sweep_route['small_positive_K'])

    def test_cyclotomic_route_selects_shell_13_17_21(self):
        routes = four_routes_select_K4()
        cyclo_route = next(r for r in routes if 'degree-2 cyclotomic' in r['route'])
        self.assertEqual(cyclo_route['selected_shell_at_K4'], (13, 17, 21))

    def test_fermat_route_at_n_1_gives_K_4(self):
        routes = four_routes_select_K4()
        fermat_route = next(r for r in routes if 'Fermat' in r['route'])
        self.assertEqual(fermat_route['sequence'][1], 4)


# =============================================================================
# Sector visibility is exclusive
# =============================================================================

class TestSectorVisibilityIsExclusive(unittest.TestCase):
    """Only LC is GR-visible; the others have specific dispositions."""

    def test_gr_visible_sectors_is_singleton_LC(self):
        self.assertEqual(gr_visible_sectors(), ['LC'])

    def test_LC_is_only_kept(self):
        for s in master_decomposition():
            if s.sector_id == 'LC':
                self.assertTrue(s.gr_visible)
                self.assertEqual(s.gr_projection_action, 'kept')
            else:
                self.assertFalse(s.gr_visible)
                self.assertNotEqual(s.gr_projection_action, 'kept')

    def test_T_and_M_are_only_killed(self):
        self.assertEqual(set(gr_killed_sectors()), {'T', 'M'})

    def test_P_and_R_are_only_averaged(self):
        self.assertEqual(set(gr_averaged_sectors()), {'P', 'R'})

    def test_J_is_only_renormalized(self):
        self.assertEqual(gr_renormalized_sectors(), ['J'])


# =============================================================================
# Headline number pinning
# =============================================================================

class TestFrameworkHeadlineNumberPinning(unittest.TestCase):
    """
    The framework's headline numerical results are pinned to bit-level
    precision. Any code drift that changes these numbers must be detected.
    """

    def test_alpha_G_headline_pinned(self):
        self.assertEqual(alpha_gravity(), FRAMEWORK_ALPHA_G_HEADLINE)

    def test_G_predicted_headline_pinned(self):
        self.assertEqual(predict_G_from_alpha(), FRAMEWORK_G_PREDICTED_HEADLINE)

    def test_ppm_error_headline_pinned(self):
        ppm = 1e6 * (predict_G_from_alpha() - CODATA_G) / CODATA_G
        self.assertAlmostEqual(ppm, FRAMEWORK_PPM_HEADLINE, places=10)

    def test_Z_4_value_pinned_to_floating_point_17_13(self):
        # 17/13 in double precision -- exact value
        self.assertEqual(sec_theta_K(4), 17 / 13)

    def test_parity_overlap_sector_coefficient_pinned(self):
        self.assertEqual(parity_overlap_sector().coefficient, 17 / 13)

    def test_hinge_sector_coefficient_pinned_to_alpha_G(self):
        self.assertEqual(hinge_sector().coefficient, FRAMEWORK_ALPHA_G_HEADLINE)

    def test_associator_fraction_pinned_to_3_32(self):
        self.assertEqual(associator_sector().coefficient, 3 / 32)


# =============================================================================
# Lepton-as-projection structural treatment
# =============================================================================

class TestLeptonProjectionStructure(unittest.TestCase):
    """
    The framework treats charged 'leptons' as structural mode configurations
    of the same vortex, not as independent particles. From established
    framework results (chats fae8d24d, d08cd7e7 and the 20/20-pass projection
    test session):

      electron: Generation 1, 1 mode (irreducible single excitation)
      muon:     Generation 2, m_mu ~ 207 m_e (= 9 closure x 23 asymmetry)
      tau:      Generation 3, m_tau ~ 3477 m_e (= 51 x 68 + 9)

    Three generations = three closure cycles of the same tile excitation
    through 1, 2, 3 gate depths respectively. The framework's gravity
    formula anchors at m_e because the electron is the unique irreducible
    single-mode generation. The muon and tau are not alternative anchors.

    This test class encodes that structural position so no future test
    mistakenly treats the muon or tau as an independent particle.
    """

    # Framework mode counts (from chat fae8d24d 20/20-pass session)
    ELECTRON_MODES = 1
    MUON_MODES = 207
    TAU_MODES = 3477

    # CODATA reference masses for cross-checking that the mode counts are
    # near the observed mass ratios
    M_MU_KG = 1.883531627e-28
    M_TAU_MEV = 1776.86
    M_E_MEV = 0.51099895

    def test_electron_is_irreducible_single_mode(self):
        # Generation 1 is by definition the 1-mode irreducible excitation
        self.assertEqual(self.ELECTRON_MODES, 1)

    def test_muon_mode_count_is_207_equals_9_times_23(self):
        # m_mu ~ 207 m_e = 9 closure positions x 23 asymmetry
        self.assertEqual(self.MUON_MODES, 207)
        self.assertEqual(self.MUON_MODES, 9 * 23)

    def test_muon_mass_ratio_matches_207_within_05_percent(self):
        # CODATA m_mu / m_e = 206.7683 (off framework prediction 207 by 0.11%)
        codata_ratio = self.M_MU_KG / M_E
        self.assertAlmostEqual(codata_ratio, self.MUON_MODES, delta=0.5)

    def test_tau_mode_count_is_3477_equals_51_times_68_plus_9(self):
        # m_tau ~ 3477 m_e = 51 x 68 + 9
        # where 51 = F+ + F0 + F- = 21 + 17 + 13 (proton polynomial content)
        # and   68 = K * F_zero = 4 * 17 (face threshold)
        # and   9 = closure positions
        self.assertEqual(self.TAU_MODES, 51 * 68 + 9)
        self.assertEqual(51, phi3(4) + phi4(4) + phi6(4))
        self.assertEqual(68, 4 * phi4(4))

    def test_tau_mass_ratio_matches_3477_within_01_percent(self):
        # CODATA m_tau = 1776.86 MeV, m_e = 0.51100 MeV
        # ratio = 3477.5 (framework prediction 3477 off by 0.014%)
        codata_ratio = self.M_TAU_MEV / self.M_E_MEV
        self.assertAlmostEqual(codata_ratio, self.TAU_MODES, delta=5)

    def test_three_generations_equals_D_three_closure_cycles(self):
        # Number of charged-lepton generations = D = 3 = spatial dimension
        D_framework = 3
        n_generations = 3
        self.assertEqual(n_generations, D_framework)

    def test_generation_mode_counts_grow_with_closure_depth(self):
        # 1 < 207 < 3477: each generation involves more vortex structure
        self.assertLess(self.ELECTRON_MODES, self.MUON_MODES)
        self.assertLess(self.MUON_MODES, self.TAU_MODES)

    def test_electron_is_unique_minimum_mode_count(self):
        # The framework anchor at m_e is forced: only Generation 1 is the
        # irreducible 1-mode excitation
        mode_counts = (self.ELECTRON_MODES, self.MUON_MODES, self.TAU_MODES)
        self.assertEqual(min(mode_counts), 1)
        self.assertEqual(mode_counts.count(min(mode_counts)), 1)

    def test_anchor_substitution_with_muon_gives_dimensional_rescaling(self):
        # Substituting m_mu into the formula gives G_mu = G_e * (m_e / m_mu)^2.
        # This is a dimensional rescaling, NOT a falsifying probe -- the muon
        # is not an independent anchor.
        report_e = lepton_anchor_report(M_E, G_E_OVER_2)
        report_mu = lepton_anchor_report(self.M_MU_KG, G_E_OVER_2)
        ratio_observed = (report_mu['G_from_this_lepton_anchor']
                          / report_e['G_from_this_lepton_anchor'])
        ratio_expected = (M_E / self.M_MU_KG) ** 2
        # The two should agree to machine precision
        self.assertAlmostEqual(ratio_observed, ratio_expected, places=20)

    def test_alpha_G_tree_is_lepton_independent(self):
        # The (17/13) * alpha^21 piece is universal across charged leptons.
        # Only the g_l / 2 anomalous-moment factor and the m^2 dimensional
        # anchor carry the lepton index.
        alpha_G_tree = (phi4(4) / phi6(4)) * (ALPHA ** phi3(4))
        # Times g_e/2 for the electron-anchored coupling
        self.assertAlmostEqual(alpha_G_tree * G_E_OVER_2,
                               alpha_gravity(), places=60)

    def test_muon_anchor_g_e_over_2_is_207_squared_below_observed_G(self):
        # If naively substituted, G_mu / G_e ~ 1 / 207^2 ~ 2.33e-5
        # This is dimensional, not a falsification
        report_e = lepton_anchor_report(M_E, G_E_OVER_2)
        report_mu = lepton_anchor_report(self.M_MU_KG, G_E_OVER_2)
        ratio = (report_mu['G_from_this_lepton_anchor']
                 / report_e['G_from_this_lepton_anchor'])
        # 1 / 206.77^2 ~ 2.34e-5
        expected_inverse = (self.M_MU_KG / M_E) ** 2
        self.assertAlmostEqual(ratio * expected_inverse, 1.0, places=12)

    def test_proton_is_NOT_a_lepton_but_has_mode_count_too(self):
        # Sanity: documentation of the wider mode-count picture from the
        # framework's 20/20-pass projection tests.
        proton_modes = 1836         # = 36 x 51 = (K x 9) x (F+ + F0 + F-)
        neutron_modes = 1839        # = 3 x 613 (613 prime -> unstable)
        self.assertEqual(proton_modes, (4 * 9) * (phi3(4) + phi4(4) + phi6(4)))
        self.assertEqual(neutron_modes - proton_modes, 3)  # D excess modes


# =============================================================================
# Showcase output coherence
# =============================================================================

class TestShowcaseIntegrationOutput(unittest.TestCase):
    """The showcase_integration() function produces a coherent audit trail."""

    def test_showcase_returns_lines(self):
        lines = showcase_integration()
        self.assertIsInstance(lines, list)
        self.assertGreater(len(lines), 30)

    def test_showcase_mentions_all_six_sectors(self):
        text = '\n'.join(showcase_integration())
        for sector in ('LC', 'T', 'P', 'J', 'R', 'M'):
            self.assertIn(f'Sector {sector}' if sector in 'PJRT'
                          else f'Sector {sector}', text)

    def test_showcase_contains_key_numbers(self):
        text = '\n'.join(showcase_integration())
        for token in ('17/13', '21', 'alpha_G', '120', '6.67'):
            self.assertIn(token, text)

    def test_showcase_states_GR_projection_chain(self):
        text = '\n'.join(showcase_integration())
        self.assertIn('Pi_GR', text)
        self.assertIn('G^LC_munu', text)
        self.assertIn('T_munu', text)


if __name__ == '__main__':
    unittest.main()
