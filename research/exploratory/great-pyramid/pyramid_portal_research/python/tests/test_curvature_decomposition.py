"""
test_curvature_decomposition.py
===============================

Regression tests for the sector-valued curvature tensor and its GR projection.
"""

import unittest

from python.closure_read import sec_theta_K
from python.curvature_decomposition import (
    CurvatureSector,
    associator_sector,
    consistency_check,
    einstein_projection_summary,
    framework_gravitational_coupling_report,
    gr_averaged_sectors,
    gr_killed_sectors,
    gr_projector,
    gr_renormalized_sectors,
    gr_visible_sectors,
    hinge_sector,
    levi_civita_sector,
    master_decomposition,
    mirror_address_sector,
    parity_overlap_sector,
    sector_table,
    torsion_sector,
)
from python.gravity import alpha_gravity, predict_G_from_alpha


# =============================================================================
# Master decomposition shape
# =============================================================================

class TestMasterDecomposition(unittest.TestCase):

    def test_six_sectors(self):
        self.assertEqual(len(master_decomposition()), 6)

    def test_sector_ids_in_canonical_order(self):
        ids = [s.sector_id for s in master_decomposition()]
        self.assertEqual(ids, ['LC', 'T', 'P', 'J', 'R', 'M'])

    def test_each_sector_is_CurvatureSector(self):
        for s in master_decomposition():
            self.assertIsInstance(s, CurvatureSector)

    def test_sector_table_keys(self):
        for row in sector_table():
            self.assertIn('id', row)
            self.assertIn('gr_visible', row)
            self.assertIn('coefficient', row)
            self.assertIn('gr_action', row)


# =============================================================================
# Sector coefficients
# =============================================================================

class TestSectorCoefficients(unittest.TestCase):

    def test_levi_civita_coefficient_is_one(self):
        self.assertEqual(levi_civita_sector().coefficient, 1.0)

    def test_parity_overlap_coefficient_is_17_over_13(self):
        s = parity_overlap_sector()
        self.assertAlmostEqual(s.coefficient, 17 / 13, places=12)

    def test_parity_overlap_coefficient_matches_sec_theta_4(self):
        s = parity_overlap_sector()
        self.assertEqual(s.coefficient, sec_theta_K(4))

    def test_hinge_coefficient_is_alpha_G(self):
        s = hinge_sector()
        self.assertEqual(s.coefficient, alpha_gravity())

    def test_associator_fraction_is_48_over_512(self):
        s = associator_sector()
        self.assertAlmostEqual(s.coefficient, 48 / 512, places=12)
        self.assertAlmostEqual(s.coefficient, 3 / 32, places=12)

    def test_torsion_has_no_fixed_coefficient(self):
        # depends on the contorsion field
        self.assertIsNone(torsion_sector().coefficient)

    def test_mirror_has_no_local_coefficient(self):
        # nonlocal -- no single coefficient
        self.assertIsNone(mirror_address_sector().coefficient)


# =============================================================================
# Sector dimensions
# =============================================================================

class TestSectorDimensions(unittest.TestCase):

    def test_LC_dimensions_are_10(self):
        # symmetric 4x4 components
        self.assertEqual(levi_civita_sector().dimensions, 10)

    def test_T_dimensions_are_24(self):
        # Letter 3: 24 antisymmetric connection components at K=4
        self.assertEqual(torsion_sector().dimensions, 24)

    def test_P_dimensions_are_17(self):
        # E_4 = Phi_4(4) = K^2 + 1 = 17 even-sector dimension
        self.assertEqual(parity_overlap_sector().dimensions, 17)

    def test_J_dimensions_are_21(self):
        # Phi_3(4) = Phi_6(5) = 21 hinge band
        self.assertEqual(hinge_sector().dimensions, 21)

    def test_R_dimensions_are_48(self):
        # 48 nonzero associator triples out of 512
        self.assertEqual(associator_sector().dimensions, 48)

    def test_M_dimensions_are_None(self):
        # nonlocal -- no fixed local dimension
        self.assertIsNone(mirror_address_sector().dimensions)


# =============================================================================
# GR projector and sector disposition
# =============================================================================

class TestGRProjector(unittest.TestCase):

    def test_four_projector_components(self):
        proj = gr_projector()
        self.assertEqual(len(proj['components']), 4)

    def test_LC_is_kept(self):
        self.assertEqual(gr_projector()['kept_sectors'], ['LC'])

    def test_T_and_M_are_killed(self):
        self.assertEqual(set(gr_killed_sectors()), {'T', 'M'})

    def test_P_and_R_are_averaged(self):
        self.assertEqual(set(gr_averaged_sectors()), {'P', 'R'})

    def test_J_is_renormalized(self):
        self.assertEqual(gr_renormalized_sectors(), ['J'])

    def test_only_LC_is_gr_visible(self):
        self.assertEqual(gr_visible_sectors(), ['LC'])

    def test_each_sector_has_a_valid_disposition(self):
        valid = {'kept', 'killed', 'averaged', 'renormalized'}
        for s in master_decomposition():
            self.assertIn(s.gr_projection_action, valid)

    def test_all_sectors_covered_in_disposition(self):
        proj = gr_projector()
        all_listed = (set(proj['kept_sectors'])
                      | set(proj['killed_sectors'])
                      | set(proj['averaged_sectors'])
                      | set(proj['renormalized_sectors']))
        self.assertEqual(all_listed, {'LC', 'T', 'P', 'J', 'R', 'M'})


# =============================================================================
# Framework coupling tie-back
# =============================================================================

class TestFrameworkCouplingTieBack(unittest.TestCase):

    def test_G_predicted_matches_gravity_module(self):
        report = framework_gravitational_coupling_report()
        self.assertEqual(report['G_predicted'], predict_G_from_alpha())

    def test_parity_overlap_coefficient_is_Z_4(self):
        report = framework_gravitational_coupling_report()
        self.assertEqual(report['parity_overlap_coefficient_Z_4'], sec_theta_K(4))
        self.assertAlmostEqual(report['parity_overlap_coefficient_Z_4'], 17 / 13,
                               places=12)

    def test_hinge_coefficient_is_alpha_G(self):
        report = framework_gravitational_coupling_report()
        self.assertEqual(report['hinge_coefficient_lambda_e'], alpha_gravity())


# =============================================================================
# Einstein projection summary
# =============================================================================

class TestEinsteinProjectionSummary(unittest.TestCase):

    def test_summary_lists_all_six_sectors(self):
        s = einstein_projection_summary()
        for symbol in ('G^LC', 'G^T', 'G^P', 'G^J', 'G^R', 'G^M'):
            self.assertIn(symbol, s['full_object'])

    def test_result_is_LC(self):
        s = einstein_projection_summary()
        self.assertEqual(s['result'], 'G_munu = G^LC_munu')

    def test_G_predicted_close_to_CODATA(self):
        s = einstein_projection_summary()
        G_pred = s['G_predicted']
        # CODATA reference 6.67430e-11
        rel_err = abs(G_pred - 6.6743e-11) / 6.6743e-11
        self.assertLess(rel_err, 30e-6)  # within 30 ppm

    def test_sector_disposition_partitions_all_six(self):
        s = einstein_projection_summary()
        disp = s['sector_disposition']
        all_listed = (set(disp['kept'])
                      | set(disp['killed'])
                      | set(disp['averaged_into_T_munu'])
                      | set(disp['renormalized_into_G']))
        self.assertEqual(all_listed, {'LC', 'T', 'P', 'J', 'R', 'M'})

    def test_no_sector_in_two_disposition_buckets(self):
        s = einstein_projection_summary()
        disp = s['sector_disposition']
        total = (len(disp['kept']) + len(disp['killed'])
                 + len(disp['averaged_into_T_munu'])
                 + len(disp['renormalized_into_G']))
        self.assertEqual(total, 6)


# =============================================================================
# Cross-module consistency
# =============================================================================

class TestConsistencyCheck(unittest.TestCase):

    def test_Z_4_consistent_across_modules(self):
        c = consistency_check()
        self.assertTrue(c['Z_4_consistent'])

    def test_alpha_G_consistent_with_hinge_sector(self):
        c = consistency_check()
        self.assertTrue(c['alpha_G_consistent'])

    def test_G_predicted_within_30_ppm_of_CODATA(self):
        c = consistency_check()
        self.assertTrue(c['within_30_ppm'])

    def test_ppm_error_matches_framework_headline(self):
        c = consistency_check()
        # The framework headline is alpha_G -> G predicted at about -13.87 ppm
        self.assertAlmostEqual(c['ppm_error'], -13.867410436170937, places=8)


if __name__ == '__main__':
    unittest.main()
