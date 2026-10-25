"""
test_apparatus.py
=================

Regression tests for the pyramid apparatus operators:
  - Shaft triad utilities: dot, norm, normalize, gram_matrix
  - Chirality detection
  - Mirror match functional with chirality and phase factors
  - Internal subsystem operators
  - Grand Gallery Z_7 phase closure
  - Z_3 projector eigenvalues
  - Z_21 sectors count and order parameter
"""

from __future__ import annotations

import unittest
from math import cos, isclose, pi, sin, sqrt

from python.apparatus import (
    Address,
    KQInterferometer,
    KingsChamberVertex,
    PortalMachine,
    ShaftKey,
    apex_top_collector,
    chirality,
    coffer_reflection_coefficient,
    determinant_3,
    dot,
    grand_gallery_z7_kernel,
    gram_matrix,
    granite_isolation,
    josephson_portal_current,
    kings_chamber_vertex,
    kq_phase_lock,
    landau_z21_potential,
    local_force_kernel,
    make_address,
    mirror_match_functional,
    norm,
    normalize,
    phase_closed,
    portal_address_kernel,
    portal_scalar_amplitude,
    triadic_phase,
    z3_projector_eigenvalue,
    z21_comb_frequencies,
    z21_order_parameter,
    z21_phase_sectors,
)
from python.constants import TAU
from python.gravity import alpha_gravity


class TestVectorUtilities(unittest.TestCase):

    def test_dot(self):
        self.assertEqual(dot((1, 2, 3), (4, 5, 6)), 32)

    def test_norm(self):
        self.assertAlmostEqual(norm((3, 4, 0)), 5.0)

    def test_normalize(self):
        v = normalize((3, 0, 0))
        self.assertAlmostEqual(v[0], 1.0)
        self.assertAlmostEqual(v[1], 0.0)
        self.assertAlmostEqual(v[2], 0.0)

    def test_normalize_raises_on_zero(self):
        with self.assertRaises(ValueError):
            normalize((0, 0, 0))


class TestGramAndChirality(unittest.TestCase):

    def test_gram_of_orthonormal_is_identity(self):
        G = gram_matrix([(1, 0, 0), (0, 1, 0), (0, 0, 1)])
        for i in range(3):
            for j in range(3):
                expected = 1.0 if i == j else 0.0
                self.assertAlmostEqual(G[i][j], expected, places=12)

    def test_chirality_right_handed(self):
        self.assertEqual(chirality([(1, 0, 0), (0, 1, 0), (0, 0, 1)]), 1)

    def test_chirality_left_handed(self):
        self.assertEqual(chirality([(1, 0, 0), (0, 1, 0), (0, 0, -1)]), -1)

    def test_determinant_identity_basis(self):
        self.assertAlmostEqual(
            determinant_3([(1, 0, 0), (0, 1, 0), (0, 0, 1)]), 1.0)


class TestPhaseClosure(unittest.TestCase):

    def test_zero_is_closed(self):
        self.assertTrue(phase_closed(0.0))

    def test_2pi_is_closed(self):
        self.assertTrue(phase_closed(TAU))

    def test_pi_is_not_closed(self):
        self.assertFalse(phase_closed(pi))


class TestKingsChamberVertex(unittest.TestCase):

    def test_band_is_21(self):
        v = kings_chamber_vertex()
        self.assertEqual(v.band, 21)

    def test_alpha_G_matches(self):
        v = kings_chamber_vertex()
        self.assertAlmostEqual(v.alpha_G, alpha_gravity(), delta=1e-58)

    def test_portal_scalar_amplitude_at_M_1(self):
        alphaG = alpha_gravity()
        self.assertAlmostEqual(portal_scalar_amplitude(1.0), alphaG)

    def test_portal_scalar_amplitude_at_M_0(self):
        self.assertEqual(portal_scalar_amplitude(0.0), 0.0)


class TestShaftKeyAndAddress(unittest.TestCase):

    def test_shaft_key_accumulated_phase(self):
        sk = ShaftKey(direction=(1, 0, 0), length=10.0, impedance=1.0,
                      omega=0.1, phase=0.5, band=21)
        self.assertAlmostEqual(sk.accumulated_phase, 0.5 + 0.1 * 10.0)

    def test_triadic_phase_sum(self):
        keys = [ShaftKey(direction=(1, 0, 0), length=0, impedance=1, omega=0,
                         phase=0.1, band=21),
                ShaftKey(direction=(0, 1, 0), length=0, impedance=1, omega=0,
                         phase=0.2, band=21),
                ShaftKey(direction=(0, 0, 1), length=0, impedance=1, omega=0,
                         phase=0.3, band=21)]
        self.assertAlmostEqual(triadic_phase(keys), 0.6)


class TestMirrorMatchFunctional(unittest.TestCase):

    def _orthonormal_address(self, signs=(1, 1, 1), phase=0.0, band=21):
        keys = [
            ShaftKey(direction=(signs[0], 0, 0), length=0, impedance=1, omega=1,
                     phase=phase, band=band),
            ShaftKey(direction=(0, signs[1], 0), length=0, impedance=1, omega=1,
                     phase=phase, band=band),
            ShaftKey(direction=(0, 0, signs[2]), length=0, impedance=1, omega=1,
                     phase=phase, band=band),
        ]
        return make_address(keys)

    def test_match_with_opposite_chirality(self):
        """Source right-handed, target left-handed flipped on z — non-zero match."""
        src = self._orthonormal_address(signs=(1, 1, 1))
        tgt = self._orthonormal_address(signs=(1, 1, -1))
        M = mirror_match_functional(src, tgt)
        self.assertGreater(M, 0.0)

    def test_no_match_same_chirality(self):
        """Same chirality means chirality_factor = 0."""
        src = self._orthonormal_address(signs=(1, 1, 1))
        tgt = self._orthonormal_address(signs=(1, 1, 1))
        M = mirror_match_functional(src, tgt)
        self.assertEqual(M, 0.0)


class TestInternalSubsystems(unittest.TestCase):

    def test_apex_collector_linear(self):
        """T_top = eta * C * dPhi/dt."""
        self.assertEqual(apex_top_collector(env_flux_derivative=10,
                                            capacitance=2, eta=0.5), 10.0)

    def test_granite_isolation_no_leak(self):
        """At leak_gamma=0: I_granite = 1."""
        self.assertEqual(granite_isolation(leak_gamma=0, wall_length=10), 1.0)


class TestGrandGallery(unittest.TestCase):

    def test_z7_k_0_to_6_sums_to_21(self):
        result = grand_gallery_z7_kernel(index_from_zero=True)
        self.assertEqual(result["index_sum"], 21)

    def test_z7_k_0_to_6_phase_is_6pi(self):
        """k=0..6: theta = (2*pi/7)*21 = 6*pi."""
        result = grand_gallery_z7_kernel(index_from_zero=True)
        self.assertAlmostEqual(result["theta_over_pi"], 6.0)

    def test_z7_k_0_to_6_closes(self):
        """6*pi = 0 mod 2*pi."""
        result = grand_gallery_z7_kernel(index_from_zero=True)
        self.assertTrue(result["closed"])

    def test_z7_k_1_to_7_phase_is_8pi(self):
        result = grand_gallery_z7_kernel(index_from_zero=False)
        self.assertAlmostEqual(result["theta_over_pi"], 8.0)

    def test_z7_k_1_to_7_closes(self):
        result = grand_gallery_z7_kernel(index_from_zero=False)
        self.assertTrue(result["closed"])


class TestZ3Projector(unittest.TestCase):

    def test_z3_at_m_0_is_1(self):
        result = z3_projector_eigenvalue(0)
        self.assertAlmostEqual(result.real, 1.0)
        self.assertAlmostEqual(result.imag, 0.0)

    def test_z3_at_m_1_is_0(self):
        result = z3_projector_eigenvalue(1)
        self.assertAlmostEqual(abs(result), 0.0, places=14)

    def test_z3_at_m_2_is_0(self):
        result = z3_projector_eigenvalue(2)
        self.assertAlmostEqual(abs(result), 0.0, places=14)


class TestZ21(unittest.TestCase):

    def test_21_sectors(self):
        sectors = z21_phase_sectors()
        self.assertEqual(len(sectors), 21)

    def test_sectors_on_unit_circle(self):
        sectors = z21_phase_sectors()
        for s in sectors:
            self.assertAlmostEqual(abs(s), 1.0)

    def test_z21_order_locked(self):
        """Perfect alignment at theta=0 gives |Omega| = 1."""
        result = z21_order_parameter([0.0, 0.0, 0.0, 0.0])
        self.assertAlmostEqual(abs(result), 1.0)

    def test_z21_comb_count(self):
        freqs = z21_comb_frequencies(110.0)
        self.assertEqual(len(freqs), 21)

    def test_z21_comb_first_is_f0(self):
        freqs = z21_comb_frequencies(110.0)
        self.assertAlmostEqual(freqs[0], 110.0)


class TestLandauJosephson(unittest.TestCase):

    def test_landau_quadratic_at_zero_rho(self):
        self.assertEqual(landau_z21_potential(rho=0, theta=0, a=1, b=1, h21=1), 0.0)

    def test_josephson_at_zero_difference(self):
        """sin(0) = 0."""
        self.assertEqual(
            josephson_portal_current(Ic=1, theta_x=0, theta_y=0,
                                     address_holonomy=0), 0.0)

    def test_josephson_at_pi_over_42(self):
        """Test Josephson at delta = pi/(2*21): I = Ic * sin(pi/2) = Ic."""
        Ic = 3.0
        delta = pi / (2 * 21)
        self.assertAlmostEqual(
            josephson_portal_current(Ic=Ic, theta_x=delta, theta_y=0,
                                     address_holonomy=0),
            Ic)


class TestKQInterferometer(unittest.TestCase):

    def test_kq_phase(self):
        king_keys = [ShaftKey((1, 0, 0), 0, 1, 0, 0.1, 21),
                     ShaftKey((0, 1, 0), 0, 1, 0, 0.2, 21),
                     ShaftKey((0, 0, 1), 0, 1, 0, 0.3, 21)]
        queen_keys = [ShaftKey((1, 0, 0), 0, 1, 0, 0.05, 26),
                      ShaftKey((0, 1, 0), 0, 1, 0, 0.10, 26),
                      ShaftKey((0, 0, 1), 0, 1, 0, 0.15, 26)]
        kq = KQInterferometer(make_address(king_keys), make_address(queen_keys))
        # K phase = 0.6, Q phase = 0.3, address_phase = 0.3 mod 2π
        self.assertAlmostEqual(kq.address_phase, 0.3, places=12)


class TestPortalMachine(unittest.TestCase):

    def test_portal_amplitude_M_1(self):
        machine = PortalMachine(alpha_G=alpha_gravity(), mirror_selector=1.0)
        self.assertAlmostEqual(abs(machine.amplitude), alpha_gravity(), delta=1e-58)

    def test_portal_amplitude_M_0(self):
        machine = PortalMachine(alpha_G=alpha_gravity(), mirror_selector=0.0)
        self.assertEqual(machine.amplitude, 0.0)

    def test_local_force_kernel(self):
        self.assertAlmostEqual(local_force_kernel(2.0, r=4.0), 0.5)

    def test_local_force_kernel_zero_r_raises(self):
        with self.assertRaises(ValueError):
            local_force_kernel(1.0, r=0.0)


class TestCofferReflection(unittest.TestCase):

    def test_matched_impedance_no_reflection(self):
        """When Z_C = conj(Z_KC) and Z_KC is real, Gamma = 0."""
        Z = complex(1.0, 0.0)
        Gamma = coffer_reflection_coefficient(Z_coffer=Z, Z_kc=Z)
        self.assertAlmostEqual(abs(Gamma), 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
