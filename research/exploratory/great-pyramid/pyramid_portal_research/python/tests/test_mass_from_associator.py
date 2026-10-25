"""
test_mass_from_associator.py
==============================

Tests for the mass-from-associator formalism (Tier 1 #1).
Partial closure: formalism explicit; calibration to m_e is open.
"""

import unittest
import numpy as np

from python.mass_from_associator import (
    clifford_associator, sweep_associator, sweep_product, omega_on_clifford,
    AXIAL_MASKS_FIXED, axial_projector_8, axial_component,
    axial_residue_norm, non_axial_residue_norm_fixed,
    tet_a_axial_seed, tet_b_axial_seed, bridge_seed,
    hexagonal_eisenstein_seed,
    axial_residue_for_structured_triple,
    axial_residue_for_hexagonal_triple,
    MassResidueResult, mass_from_associator_residue,
    showcase_mass_from_associator,
)
from python.cyclotomic_12 import (
    cl_basis_1, cl_basis_T1, cl_basis_T2, cl_basis_I,
)


class TestCliffordAssociator(unittest.TestCase):
    """Cl(3, 0) is associative, so its associator is identically zero."""

    def test_associator_of_basis_elements_is_zero(self):
        for a_factory, b_factory, c_factory in [
            (cl_basis_1, cl_basis_T1, cl_basis_I),
            (cl_basis_T1, cl_basis_T2, cl_basis_I),
            (cl_basis_T2, cl_basis_T1, cl_basis_I),
        ]:
            a = a_factory(); b = b_factory(); c = c_factory()
            result = clifford_associator(a, b, c)
            np.testing.assert_array_almost_equal(result, np.zeros(8))

    def test_associator_for_random_triples_is_zero(self):
        rng = np.random.default_rng(0)
        for _ in range(10):
            a = rng.standard_normal(8)
            b = rng.standard_normal(8)
            c = rng.standard_normal(8)
            result = clifford_associator(a, b, c)
            np.testing.assert_array_almost_equal(result, np.zeros(8))


class TestSweepAssociator(unittest.TestCase):
    """Sweep product is non-associative (Ω-projection is not a ring hom)."""

    def test_sweep_associator_can_be_nonzero(self):
        # Structured triple gives non-zero sweep associator
        a = tet_a_axial_seed(1.0, 0.5)
        b = tet_b_axial_seed(1.0, 0.5)
        c = bridge_seed(1.0)
        result = sweep_associator(a, b, c)
        # Axial norm should be non-zero
        norm = axial_residue_norm(result)
        self.assertGreater(norm, 0.0)


class TestAxialProjection(unittest.TestCase):

    def test_axial_masks_are_0_and_7(self):
        self.assertEqual(AXIAL_MASKS_FIXED, (0, 7))

    def test_axial_projector_picks_scalar_and_pseudoscalar(self):
        P = axial_projector_8()
        v = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
        projected = P @ v
        np.testing.assert_array_almost_equal(
            projected, [1.0, 0, 0, 0, 0, 0, 0, 8.0]
        )

    def test_axial_component_extraction(self):
        v = np.array([3.0, 0, 0, 0, 0, 0, 0, 4.0])
        s, p = axial_component(v)
        self.assertEqual(s, 3.0)
        self.assertEqual(p, 4.0)

    def test_axial_norm_is_pythagorean(self):
        v = np.array([3.0, 0, 0, 0, 0, 0, 0, 4.0])
        self.assertAlmostEqual(axial_residue_norm(v), 5.0)

    def test_non_axial_norm(self):
        v = np.array([3.0, 1.0, 1.0, 0, 0, 0, 0, 4.0])
        # Non-axial: masks 1..6.  Norms: 1+1 = 2, sqrt(2)
        self.assertAlmostEqual(non_axial_residue_norm_fixed(v), np.sqrt(2.0))


class TestStructuredSeeds(unittest.TestCase):

    def test_tet_a_axial_has_scalar_and_T1_components(self):
        seed = tet_a_axial_seed(alpha=2.0, beta=3.0)
        # mask 0: 2.0, masks 1, 2, 4: 3.0 each
        self.assertEqual(seed[0], 2.0)
        self.assertEqual(seed[1], 3.0)
        self.assertEqual(seed[2], 3.0)
        self.assertEqual(seed[4], 3.0)

    def test_tet_b_axial_has_scalar_and_T2_components(self):
        seed = tet_b_axial_seed(gamma=2.0, delta=3.0)
        self.assertEqual(seed[0], 2.0)
        # T_2 = mask 3 + mask 6 - mask 5
        self.assertEqual(seed[3], 3.0)
        self.assertEqual(seed[6], 3.0)
        self.assertEqual(seed[5], -3.0)

    def test_bridge_seed_is_pseudoscalar(self):
        seed = bridge_seed(epsilon=4.0)
        self.assertEqual(seed[7], 4.0)
        self.assertEqual(np.sum(np.abs(seed)) - 4.0, 0.0)


class TestStructuredTripleResidue(unittest.TestCase):

    def test_clifford_axial_norm_is_zero(self):
        result = axial_residue_for_structured_triple()
        self.assertAlmostEqual(result["clifford_associator_axial_norm"], 0.0)

    def test_sweep_axial_norm_can_be_nonzero(self):
        result = axial_residue_for_structured_triple(
            alpha=1.0, beta=0.5, gamma=1.0, delta=0.5, epsilon=1.0
        )
        self.assertGreater(result["sweep_associator_axial_norm"], 0.0)

    def test_sweep_residue_scales_with_seeds(self):
        # Scaling all seeds by k should scale the associator by k^3
        result_1 = axial_residue_for_structured_triple(
            alpha=1.0, beta=0.5, gamma=1.0, delta=0.5, epsilon=1.0
        )
        result_2 = axial_residue_for_structured_triple(
            alpha=2.0, beta=1.0, gamma=2.0, delta=1.0, epsilon=2.0
        )
        ratio = (result_2["sweep_associator_axial_norm"] /
                 result_1["sweep_associator_axial_norm"])
        # Trilinear scaling: should be 8x for 2x seeds
        self.assertAlmostEqual(ratio, 8.0, places=4)


class TestHexagonalTripleResidue(unittest.TestCase):

    def test_hexagonal_seed_is_basis_vector(self):
        e1 = hexagonal_eisenstein_seed(1)
        self.assertEqual(e1[1], 1.0)
        self.assertEqual(np.sum(np.abs(e1)) - 1.0, 0.0)

    def test_clifford_associator_zero_for_hexagonal_triple(self):
        result = axial_residue_for_hexagonal_triple(1, 2, 3)
        self.assertTrue(result["clifford_associator_is_zero"])


class TestMassResidueMapping(unittest.TestCase):

    def test_dimensionless_residue_without_calibration(self):
        struct = axial_residue_for_structured_triple()
        mr = mass_from_associator_residue(struct)
        self.assertEqual(mr.calibration_status, "open")
        self.assertIsNone(mr.physical_mass_eV)

    def test_dimensionless_residue_with_calibration(self):
        struct = axial_residue_for_structured_triple()
        mr = mass_from_associator_residue(struct, calibration_eV=1.0e6)
        self.assertEqual(mr.calibration_status, "applied")
        self.assertIsNotNone(mr.physical_mass_eV)

    def test_partial_closure_status_is_acknowledged(self):
        struct = axial_residue_for_structured_triple()
        mr = mass_from_associator_residue(struct)
        # Default has no calibration — open
        self.assertEqual(mr.calibration_status, "open")


class TestShowcase(unittest.TestCase):

    def test_showcase_runs(self):
        out = showcase_mass_from_associator()
        self.assertIsInstance(out, list)
        self.assertGreater(len(out), 5)

    def test_showcase_mentions_partial_closure(self):
        joined = "\n".join(showcase_mass_from_associator())
        for token in ("PARTIAL CLOSURE", "associator", "axial", "open"):
            self.assertIn(token, joined, msg=f"missing: {token}")
