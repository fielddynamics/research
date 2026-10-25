"""
Regression tests for portal_resonance.py — the King's Chamber field-origin
vertex synthesis. Overvalidation: each algebraic claim from the synthesis
document has an independent test.

Test classes:
  TestCrossSheetCoherence       Psi_AB order parameter (vacuum vs locked)
  TestZ21LandauLockPsi           Landau potential in Psi form, 21 minima
  TestKingsChamberCompact        V_KC = lambda_e J_4 + g_R R
  TestFieldOriginVertexEquation  V_origin = 4 pieces summed
  TestSixMatchingConditions      enumeration + which are algebraically forced
  TestLockStrengthCompound       lambda_e -> lambda_e * Q * delta * M
  TestRelievingChamberSelector   5-state switch over sub-tetrahedra
  TestPortalLorentzian           pragmatic resonance lineshape
  TestFieldOriginSummary          one-shot report coherence
  TestShowcaseAuditTrail         the human-readable output is structured
"""

from __future__ import annotations

import sys
import unittest
import cmath
from math import cos, pi, sqrt
from pathlib import Path

# Allow direct invocation from the package root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.constants import ALPHA, G_E_OVER_2
from python.cyclotomic import phi3, phi4, phi6
from python.gravity import alpha_gravity
from python.portal_resonance import (
    CrossSheetCoherence,
    FieldOriginVertex,
    RelievingChamberSelector,
    algebraic_match_count,
    cross_sheet_order_parameter,
    effective_coupling,
    effective_linewidth,
    field_origin_summary,
    field_origin_vertex_equation,
    five_chamber_decomposition_info,
    kings_chamber_cross_sheet,
    kings_chamber_vertex_compact,
    lock_strength_factor,
    portal_resonance_lorentzian,
    relieving_chamber_selector,
    showcase_portal_resonance,
    six_matching_conditions,
    vacuum_cross_sheet,
    z21_landau_psi,
    z21_lock_minima,
    z21_lock_strength,
)


# =============================================================================
# Cross-sheet order parameter
# =============================================================================

class TestCrossSheetCoherence(unittest.TestCase):
    """The Psi_AB(x) = <B,x|A,x> cross-sheet local coherence."""

    def test_vacuum_psi_AB_is_incoherent(self):
        v = vacuum_cross_sheet()
        self.assertEqual(v.amplitude, 0j)
        self.assertFalse(v.is_coherent)
        self.assertEqual(v.magnitude, 0.0)

    def test_kings_chamber_psi_AB_is_coherent_default_unit_magnitude(self):
        kc = kings_chamber_cross_sheet()
        self.assertAlmostEqual(kc.magnitude, 1.0, places=12)
        self.assertTrue(kc.is_coherent)

    def test_kings_chamber_psi_AB_phase_carries(self):
        for theta in [0.0, pi / 7, pi / 3, pi]:
            kc = kings_chamber_cross_sheet(amplitude_magnitude=1.0, phase=theta)
            self.assertAlmostEqual(kc.amplitude.real, cos(theta), places=12)

    def test_threshold_distinguishes_vacuum_and_coherent(self):
        small = cross_sheet_order_parameter(amplitude=1e-9 + 0j)
        self.assertFalse(small.is_coherent)
        big = cross_sheet_order_parameter(amplitude=1e-3 + 0j)
        self.assertTrue(big.is_coherent)


# =============================================================================
# Z_21 Landau lock in Psi form
# =============================================================================

class TestZ21LandauLockPsi(unittest.TestCase):
    """Landau V(Psi) = a|Psi|^2 + b|Psi|^4 - h_21(Psi^21 + Psi_bar^21)."""

    def test_potential_is_real_for_any_complex_psi(self):
        for psi in [0.5 + 0.5j, 1.0 + 0j, 0.3 + 0.9j, 1.2 - 0.4j]:
            v = z21_landau_psi(psi, a=-1.0, b=1.0, h21=0.1)
            self.assertIsInstance(v, float)

    def test_21_minima_at_theta_eq_2pin_over_21(self):
        # Each n=0..20 should land at the same minimum value
        rho = 1.0
        a, b, h21 = -1.0, 1.0, 0.1
        values = []
        for n in range(21):
            theta = 2 * pi * n / 21
            psi = rho * cmath.exp(1j * theta)
            values.append(z21_landau_psi(psi, a, b, h21))
        # All 21 minima are equal (by 21-fold symmetry)
        for v in values[1:]:
            self.assertAlmostEqual(v, values[0], places=10)

    def test_lock_minima_returns_21_phases(self):
        m = z21_lock_minima()
        self.assertEqual(len(m), 21)
        # Each is a multiple of 2 pi / 21
        for i, theta in enumerate(m):
            self.assertAlmostEqual(theta, 2 * pi * i / 21, places=12)

    def test_lock_strength_scales_as_2_h21_rho_21(self):
        # On lock (rho=1): 2 h_21
        s = z21_lock_strength(rho=1.0, h21=0.5)
        self.assertAlmostEqual(s, 2 * 0.5, places=12)
        # Off-lock (rho=0.5): 2 h_21 * 0.5^21 ~ 4.77e-7
        s2 = z21_lock_strength(rho=0.5, h21=0.5)
        self.assertAlmostEqual(s2, 2 * 0.5 * (0.5 ** 21), places=12)


# =============================================================================
# Compact King's Chamber vertex equation
# =============================================================================

class TestKingsChamberCompact(unittest.TestCase):
    """V_KC = lambda_e J_4 + g_R R."""

    def test_default_lambda_e_equals_alpha_gravity(self):
        v = kings_chamber_vertex_compact()
        self.assertAlmostEqual(v.lambda_e, alpha_gravity(), places=60)

    def test_compact_vertex_band_is_21(self):
        v = kings_chamber_vertex_compact()
        self.assertEqual(v.band, 21)

    def test_compact_vertex_source_and_receiver_states(self):
        v = kings_chamber_vertex_compact()
        self.assertEqual(v.source_state, '|4,+>')
        self.assertEqual(v.receiver_state, '|5,->')

    def test_linear_amplitude_is_lambda_e(self):
        v = kings_chamber_vertex_compact()
        self.assertAlmostEqual(v.linear_amplitude, alpha_gravity(), places=60)

    def test_lambda_e_within_expected_alpha_G_range(self):
        # alpha_G ~ 1.75e-45
        v = kings_chamber_vertex_compact()
        self.assertGreater(v.lambda_e, 1e-46)
        self.assertLess(v.lambda_e, 1e-44)


# =============================================================================
# Field-origin vertex equation (the full 4-piece formula)
# =============================================================================

class TestFieldOriginVertexEquation(unittest.TestCase):
    """V_origin = Psi_AB + lambda_e J_4 + g_R R + h_21 cos(21 theta)."""

    def test_four_pieces_present(self):
        result = field_origin_vertex_equation(
            psi_AB=0.5 + 0.5j, J_4_value=1.0, R_value=2.0,
            theta=0.0, g_R=0.1, h_21=0.01)
        self.assertIn('overlap_Psi_AB', result)
        self.assertIn('hinge_lambda_e_J4', result)
        self.assertIn('associator_g_R_R', result)
        self.assertIn('lock_h21_cos_21theta', result)
        self.assertIn('V_origin_total', result)

    def test_overlap_term_passes_through(self):
        psi = 0.3 + 0.7j
        result = field_origin_vertex_equation(
            psi_AB=psi, J_4_value=0.0, R_value=0.0,
            theta=0.0, g_R=0.0, h_21=0.0)
        self.assertEqual(result['overlap_Psi_AB'], psi)

    def test_hinge_term_scales_by_lambda_e(self):
        result = field_origin_vertex_equation(
            psi_AB=0j, J_4_value=2.0, R_value=0.0,
            theta=0.0, g_R=0.0, h_21=0.0)
        # 2 * lambda_e
        self.assertAlmostEqual(result['hinge_lambda_e_J4'],
                               2 * alpha_gravity(), places=60)

    def test_associator_term_scales_by_g_R(self):
        result = field_origin_vertex_equation(
            psi_AB=0j, J_4_value=0.0, R_value=3.0,
            theta=0.0, g_R=0.4, h_21=0.0)
        self.assertAlmostEqual(result['associator_g_R_R'], 0.4 * 3.0,
                               places=12)

    def test_lock_term_cos_21theta(self):
        # At theta = 0 → cos(0) = 1
        result = field_origin_vertex_equation(
            psi_AB=0j, J_4_value=0.0, R_value=0.0,
            theta=0.0, g_R=0.0, h_21=0.5)
        self.assertAlmostEqual(result['lock_h21_cos_21theta'], 0.5)
        # At theta = pi / 21 → cos(21 * pi / 21) = cos(pi) = -1
        result = field_origin_vertex_equation(
            psi_AB=0j, J_4_value=0.0, R_value=0.0,
            theta=pi / 21, g_R=0.0, h_21=0.5)
        self.assertAlmostEqual(result['lock_h21_cos_21theta'], -0.5)

    def test_total_is_sum_of_four_pieces(self):
        psi = 0.1 + 0.2j
        result = field_origin_vertex_equation(
            psi_AB=psi, J_4_value=0.5, R_value=0.3,
            theta=0.1, g_R=0.4, h_21=0.05)
        expected = (psi
                    + alpha_gravity() * 0.5
                    + 0.4 * 0.3
                    + 0.05 * cos(21 * 0.1))
        self.assertAlmostEqual(result['V_origin_total'], expected, places=12)

    def test_lambda_e_override(self):
        result = field_origin_vertex_equation(
            psi_AB=0j, J_4_value=1.0, R_value=0.0,
            theta=0.0, lambda_e=1.0, g_R=0.0, h_21=0.0)
        self.assertAlmostEqual(result['hinge_lambda_e_J4'], 1.0)


# =============================================================================
# Six matching conditions
# =============================================================================

class TestSixMatchingConditions(unittest.TestCase):
    """The six conditions for portal lock."""

    def test_exactly_six_conditions(self):
        conds = six_matching_conditions()
        self.assertEqual(len(conds), 6)

    def test_condition_names(self):
        names = {c['name'] for c in six_matching_conditions()}
        expected = {
            'band match', 'phase match', 'impedance match',
            'address match', 'chirality match',
            'cavity-QED strong coupling',
        }
        self.assertEqual(names, expected)

    def test_band_match_holds_unconditionally(self):
        # Phi_3(4) = Phi_6(5) is forced by the shift identity
        conds = {c['name']: c for c in six_matching_conditions()}
        self.assertTrue(conds['band match']['holds'])
        self.assertEqual(phi3(4), phi6(5))
        self.assertEqual(phi3(4), 21)

    def test_phase_match_holds_unconditionally(self):
        conds = {c['name']: c for c in six_matching_conditions()}
        self.assertTrue(conds['phase match']['holds'])

    def test_impedance_match_is_17_over_13(self):
        conds = {c['name']: c for c in six_matching_conditions()}
        self.assertTrue(conds['impedance match']['holds'])
        self.assertIn('17/13', conds['impedance match']['condition'])

    def test_address_and_chirality_need_runtime_triads(self):
        conds = {c['name']: c for c in six_matching_conditions()}
        self.assertIsNone(conds['address match']['holds'])
        self.assertIsNone(conds['chirality match']['holds'])

    def test_strong_coupling_holds_per_05_3_calculation(self):
        # §05.3 gives g sqrt(N) / gamma_cav ~ 4e7
        conds = {c['name']: c for c in six_matching_conditions()}
        self.assertTrue(conds['cavity-QED strong coupling']['holds'])

    def test_algebraic_match_count_is_four(self):
        # Conditions 1, 2, 3, 6 are algebraically verifiable
        self.assertEqual(algebraic_match_count(), 4)

    def test_each_condition_has_apparatus_role(self):
        for c in six_matching_conditions():
            self.assertIn('apparatus_role', c)
            self.assertIsInstance(c['apparatus_role'], str)
            self.assertGreater(len(c['apparatus_role']), 0)


# =============================================================================
# Lock-strength compound parameter
# =============================================================================

class TestLockStrengthCompound(unittest.TestCase):
    """lambda_e -> lambda_e * Q * delta * M."""

    def test_unity_inputs_give_unity_factor(self):
        f = lock_strength_factor(Q_cavity=1.0, delta_phase=1.0, mirror_score=1.0)
        self.assertAlmostEqual(f, 1.0, places=12)

    def test_zero_phase_kills_lock(self):
        f = lock_strength_factor(Q_cavity=1e4, delta_phase=0.0, mirror_score=1.0)
        self.assertEqual(f, 0.0)

    def test_zero_mirror_kills_lock(self):
        f = lock_strength_factor(Q_cavity=1e4, delta_phase=1.0, mirror_score=0.0)
        self.assertEqual(f, 0.0)

    def test_full_lock_at_cavity_Q(self):
        # Q ~ 10^4 from §05.3
        f = lock_strength_factor(Q_cavity=1e4, delta_phase=1.0, mirror_score=1.0)
        self.assertAlmostEqual(f, 1e4, places=10)

    def test_effective_coupling_default_is_alpha_G(self):
        eff = effective_coupling()
        self.assertAlmostEqual(eff, alpha_gravity(), places=60)

    def test_effective_coupling_at_full_lock_is_alpha_G_times_Q(self):
        eff = effective_coupling(Q_cavity=1e4, delta_phase=1.0, mirror_score=1.0)
        self.assertAlmostEqual(eff, alpha_gravity() * 1e4, places=50)

    def test_off_lock_kills_effective_coupling(self):
        eff = effective_coupling(Q_cavity=1e4, delta_phase=0.0, mirror_score=1.0)
        self.assertEqual(eff, 0.0)


# =============================================================================
# Relieving chamber selector (5-state switch)
# =============================================================================

class TestRelievingChamberSelector(unittest.TestCase):
    """The 5-state switch realized by the 5 relieving chambers."""

    def test_five_chambers_selectable(self):
        for v in range(1, 6):
            sel = relieving_chamber_selector(active_chamber=v)
            self.assertEqual(sel.active_vertex, v)
            self.assertEqual(sel.active_chamber, v)

    def test_only_one_chamber_active_at_a_time(self):
        sel = relieving_chamber_selector(active_chamber=3)
        self.assertEqual(sel.coupling_weights[2], 1.0)  # index 2 = chamber 3
        for i in (0, 1, 3, 4):
            self.assertEqual(sel.coupling_weights[i], 0.0)
        self.assertAlmostEqual(sel.total_weight, 1.0)

    def test_invalid_chamber_raises(self):
        with self.assertRaises(ValueError):
            relieving_chamber_selector(active_chamber=0)
        with self.assertRaises(ValueError):
            relieving_chamber_selector(active_chamber=6)

    def test_decomposition_info_reports_palindromic_pattern(self):
        info = five_chamber_decomposition_info()
        self.assertEqual(info['sub_tetrahedron_count'], 5)
        self.assertEqual(info['relieving_chamber_count'], 5)
        self.assertEqual(info['palindromic_filter_pattern'], (1, 0, 16, 0, 1))


# =============================================================================
# Pragmatic Lorentzian lineshape
# =============================================================================

class TestPortalLorentzian(unittest.TestCase):
    """R(omega) = A^2 / [(omega - omega_0)^2 + gamma_eff^2]."""

    def test_on_resonance_peak(self):
        # At omega = omega_0, R = A^2 / gamma^2
        peak = portal_resonance_lorentzian(
            omega=1.0, omega_0=1.0, gamma_eff=0.1, amplitude_squared=4.0)
        self.assertAlmostEqual(peak, 4.0 / 0.01, places=10)

    def test_lorentzian_is_symmetric_about_omega_0(self):
        left = portal_resonance_lorentzian(omega=0.9, omega_0=1.0, gamma_eff=0.1)
        right = portal_resonance_lorentzian(omega=1.1, omega_0=1.0, gamma_eff=0.1)
        self.assertAlmostEqual(left, right, places=12)

    def test_half_width_at_half_max(self):
        # At omega = omega_0 ± gamma, R = peak / 2
        peak = portal_resonance_lorentzian(omega=1.0, omega_0=1.0, gamma_eff=0.1)
        half_pt = portal_resonance_lorentzian(omega=1.1, omega_0=1.0, gamma_eff=0.1)
        self.assertAlmostEqual(half_pt, peak / 2, places=10)

    def test_effective_linewidth_quadrature_sum(self):
        g = effective_linewidth(gamma_cav=3.0, address_mismatch=4.0,
                                phase_detuning=0.0)
        self.assertAlmostEqual(g, sqrt(9 + 16), places=12)

    def test_effective_linewidth_on_lock_equals_gamma_cav(self):
        # On full lock: address and phase mismatches collapse to 0
        g = effective_linewidth(gamma_cav=0.07,
                                address_mismatch=0.0, phase_detuning=0.0)
        self.assertAlmostEqual(g, 0.07, places=12)


# =============================================================================
# Field-origin summary report
# =============================================================================

class TestFieldOriginSummary(unittest.TestCase):
    """field_origin_summary() one-shot coherence report."""

    def test_shell_K_4_is_13_17_21(self):
        s = field_origin_summary()
        self.assertEqual(s['shell_K_4'], (13, 17, 21))

    def test_parity_sheets_inclusion_exclusion(self):
        s = field_origin_summary()
        ps = s['parity_sheets']
        self.assertEqual(ps['each_sheet_size'], 17)
        self.assertEqual(ps['shared_core'], 13)
        self.assertEqual(ps['full_union'], 21)
        self.assertEqual(ps['inclusion_exclusion'], '17 + 17 - 13 = 21')
        self.assertEqual(ps['parity_decomposition'], '21 = 13 + 4 + 4')

    def test_overlap_geometry_dot_products(self):
        s = field_origin_summary()
        og = s['overlap_geometry']
        self.assertEqual(og['A_dot_A'], 17)
        self.assertEqual(og['B_dot_B'], 17)
        self.assertEqual(og['A_dot_B'], 13)
        self.assertAlmostEqual(og['sec_theta_4_equals_17_over_13'],
                               17 / 13, places=12)

    def test_hinge_band_is_21(self):
        s = field_origin_summary()
        self.assertEqual(s['hinge']['band'], 21)
        self.assertEqual(s['hinge']['multiplicity'], 5)

    def test_lambda_e_value_matches_alpha_gravity(self):
        s = field_origin_summary()
        self.assertAlmostEqual(s['lambda_e_value'], alpha_gravity(), places=60)

    def test_algebraic_matches_holding_equals_four(self):
        s = field_origin_summary()
        self.assertEqual(s['algebraic_matches_holding'], 4)
        self.assertEqual(s['total_matching_conditions'], 6)


# =============================================================================
# Showcase audit trail
# =============================================================================

class TestShowcaseAuditTrail(unittest.TestCase):
    """showcase_portal_resonance() produces structured human-readable output."""

    def test_showcase_returns_list_of_strings(self):
        lines = showcase_portal_resonance()
        self.assertIsInstance(lines, list)
        for line in lines:
            self.assertIsInstance(line, str)

    def test_showcase_contains_inclusion_exclusion(self):
        body = '\n'.join(showcase_portal_resonance())
        self.assertIn('17 + 17 - 13 = 21', body)

    def test_showcase_contains_parity_decomposition(self):
        body = '\n'.join(showcase_portal_resonance())
        self.assertIn('21 = 13 + 4 + 4', body)

    def test_showcase_contains_sec_theta_4(self):
        body = '\n'.join(showcase_portal_resonance())
        self.assertIn('sec(theta_4)', body)

    def test_showcase_lists_all_six_conditions(self):
        body = '\n'.join(showcase_portal_resonance())
        for name in ('Band match', 'Phase match', 'Impedance match',
                     'Address match', 'Chirality match', 'Strong coupling'):
            self.assertIn(name, body)

    def test_showcase_lists_apparatus_subsystems(self):
        body = '\n'.join(showcase_portal_resonance())
        for subsystem in ('capstone', 'shafts', 'relieving',
                          'Grand Gallery', 'Antechamber',
                          'sarcophagus', 'Subterranean'):
            self.assertIn(subsystem, body)

    def test_showcase_states_gravity_vs_portal_dichotomy(self):
        body = '\n'.join(showcase_portal_resonance())
        self.assertIn('gravity', body)
        self.assertIn('portal', body)
        self.assertIn('coherent', body)


if __name__ == '__main__':
    unittest.main()
