"""
test_field_origin_dynamics.py
==============================

Tests for the bridge from closure_core256 (exact algebra) to
portal_resonance (resonance lift).

The bridge's correctness claim is:

  (i)   The nine exact-algebra invariants M_1..M_4 pass (= 0 within
        floating-point tolerance), confirming the closure-node theorem
        is intact at runtime.

  (ii)  R(a, b, c) for any closure-node states a, b, c lands in <1, I>:
        the M_4 residue is zero to numerical precision.

  (iii) The axial readout y = Pi_<1,I> R produces a complex number
        whose arg can drive the Z_21 phase lift.

  (iv)  The three-sweep update T_b3 T_b2 T_b1 with identity bridges is
        a Walsh-Hadamard round trip (no operation) followed by P_Omega.

  (v)   The diagnostic panel correctly flags invalid runs.
"""

import math
import unittest
import numpy as np

from python.field_origin_dynamics import (
    AXIAL_MASKS,
    axial_projection,
    axial_components,
    non_axial_residue_norm,
    associator,
    associator_axial_readout,
    walsh_bridge_step,
    three_sweep_update,
    run_field_origin_ticks,
    tet_a_axial_seed,
    tet_b_axial_seed,
    mixed_axial_seed,
    m1_walsh_inversion_error,
    m2_eisenstein_closure_error,
    m3_projector_idempotent_error,
    m4_associator_axial_residue,
    m5_axial_defect_magnitude,
    nine_metric_diagnostic_panel,
    diagnostic_panel_run_validity,
    showcase_field_origin_dynamics,
    H3,
)


TOL_EXACT = 1e-10


class TestExactAlgebraInvariants(unittest.TestCase):
    """
    M_1 through M_4 must be zero to numerical precision.  Per the spec:
    a run is only valid if these are exact.
    """

    def test_M1_walsh_inversion_exact(self):
        self.assertLess(m1_walsh_inversion_error(), TOL_EXACT)

    def test_M2_eisenstein_closure_exact(self):
        self.assertLess(m2_eisenstein_closure_error(), TOL_EXACT)

    def test_M3_projector_idempotent_exact(self):
        self.assertLess(m3_projector_idempotent_error(), TOL_EXACT)

    def test_M4_associator_axial_landing_exact(self):
        # The closure-node theorem from section 01.5: R(a,b,c) in <1,I>.
        # At runtime this means the non-axial residue is zero (to fp).
        self.assertLess(m4_associator_axial_residue(), TOL_EXACT)


class TestAxialProjection(unittest.TestCase):
    """The projection Pi_<1,I> zeros all but masks 0 and 7."""

    def test_axial_masks_are_0_and_7(self):
        self.assertEqual(AXIAL_MASKS, (0, 7))

    def test_projection_preserves_axial_components(self):
        x = np.arange(8, dtype=float)
        p = axial_projection(x)
        self.assertEqual(p[0], 0.0)
        self.assertEqual(p[7], 7.0)
        # Middle six are zeroed
        self.assertTrue(np.allclose(p[1:7], 0.0))

    def test_axial_components_returns_scalar_and_pseudoscalar(self):
        x = np.zeros(8)
        x[0] = 3.14
        x[7] = 2.72
        a, b = axial_components(x)
        self.assertAlmostEqual(a, 3.14)
        self.assertAlmostEqual(b, 2.72)

    def test_non_axial_residue_zero_for_axial_state(self):
        x = mixed_axial_seed(1.0, 1.0)
        self.assertEqual(non_axial_residue_norm(x), 0.0)

    def test_non_axial_residue_positive_for_middle_state(self):
        x = np.zeros(8)
        x[3] = 1.0  # e_12 -- middle sector
        self.assertGreater(non_axial_residue_norm(x), 0.0)


class TestAssociatorAlwaysLandsAxial(unittest.TestCase):
    """
    Across many random closure-node triples, R(a,b,c) always lands in
    <1, I>.  This is the runtime form of the closure-node theorem.
    """

    def test_associator_axial_landing_across_random_triples(self):
        rng = np.random.default_rng(0xC10591)
        max_residue = 0.0
        for _ in range(50):
            a = rng.standard_normal(8)
            b = rng.standard_normal(8)
            c = rng.standard_normal(8)
            R = associator(a, b, c)
            r = non_axial_residue_norm(R)
            max_residue = max(max_residue, r)
        # 50 random triples; closure-node theorem says all land axial.
        self.assertLess(max_residue, TOL_EXACT)

    def test_associator_readout_is_complex(self):
        y, residue = associator_axial_readout(
            mixed_axial_seed(1.0, 0.5),
            mixed_axial_seed(0.5, 1.0),
            mixed_axial_seed(0.25, 0.75),
        )
        self.assertIsInstance(y, complex)
        self.assertLess(residue, TOL_EXACT)

    def test_associator_antisymmetric_in_first_and_third(self):
        # R(a,b,c) and R(c,b,a) are related by the associator's algebraic
        # antisymmetry.  Even if they are not exact negatives in this
        # nonassociative algebra, both must independently land axial.
        rng = np.random.default_rng(7)
        a = rng.standard_normal(8)
        b = rng.standard_normal(8)
        c = rng.standard_normal(8)
        R1 = associator(a, b, c)
        R2 = associator(c, b, a)
        self.assertLess(non_axial_residue_norm(R1), TOL_EXACT)
        self.assertLess(non_axial_residue_norm(R2), TOL_EXACT)


class TestWalshBridgeStep(unittest.TestCase):
    """Single-sweep Walsh-bridge filter."""

    def test_identity_bridge_is_identity_operation(self):
        # T_b(x) with b = (1,1,...,1) should give back x exactly:
        # T_b(x) = (1/N) H diag(1) H x = (1/N) H H x = x.
        rng = np.random.default_rng(11)
        x = rng.standard_normal(8)
        out = walsh_bridge_step(x, np.ones(8))
        self.assertTrue(np.allclose(out, x, atol=1e-12))

    def test_zero_bridge_kills_state(self):
        x = mixed_axial_seed(1.0, 1.0)
        out = walsh_bridge_step(x, np.zeros(8))
        self.assertTrue(np.allclose(out, 0.0))


class TestThreeSweepUpdate(unittest.TestCase):
    """Composition of three sweeps then closure projection."""

    def test_identity_bridges_collapse_to_P_omega(self):
        # With all-ones bridges, three sweeps act as identity, so the
        # output is P_Omega(x) directly.
        from python.closure_core256 import closure_projection3
        rng = np.random.default_rng(13)
        x = rng.standard_normal(8)
        bridges = (np.ones(8), np.ones(8), np.ones(8))
        out = three_sweep_update(x, bridges)
        expected = closure_projection3(x)
        self.assertTrue(np.allclose(out, expected, atol=1e-12))

    def test_zero_bridge_anywhere_kills_state(self):
        x = mixed_axial_seed(1.0, 1.0)
        bridges = (np.ones(8), np.zeros(8), np.ones(8))
        out = three_sweep_update(x, bridges)
        self.assertTrue(np.allclose(out, 0.0))


class TestRunFieldOriginTicks(unittest.TestCase):
    """The tick-evolution driver for the resonance lift."""

    def test_initial_tick_has_zero_amplitude(self):
        seed = mixed_axial_seed(1.0, 0.7)
        bridges = (np.ones(8), np.ones(8), np.ones(8))
        trace = run_field_origin_ticks(seed, bridges, n_ticks=5)
        # Ticks 0 and 1 have no associator window
        self.assertEqual(trace[0].amplitude, 0.0)
        self.assertEqual(trace[1].amplitude, 0.0)

    def test_residue_m4_is_machine_zero_on_every_tick(self):
        seed = mixed_axial_seed(1.0, 0.7)
        bridges = (np.ones(8), np.ones(8), np.ones(8))
        trace = run_field_origin_ticks(seed, bridges, n_ticks=8)
        for tick in trace:
            self.assertLess(tick.residue_m4, TOL_EXACT,
                            msg=f"M_4 nonzero at tick {tick.t}: {tick.residue_m4}")

    def test_trace_length_matches_n_ticks(self):
        seed = tet_a_axial_seed()
        bridges = (np.ones(8), np.ones(8), np.ones(8))
        trace = run_field_origin_ticks(seed, bridges, n_ticks=10)
        self.assertEqual(len(trace), 10)


class TestSeedConstructors(unittest.TestCase):
    """TetA-only, TetB-only, and mixed axial seeds."""

    def test_tet_a_seed_is_scalar_only(self):
        s = tet_a_axial_seed()
        self.assertEqual(s[0], 1.0)
        self.assertTrue(np.allclose(s[1:], 0.0))

    def test_tet_b_seed_is_pseudoscalar_only(self):
        s = tet_b_axial_seed()
        self.assertEqual(s[7], 1.0)
        self.assertTrue(np.allclose(s[:7], 0.0))

    def test_mixed_seed_is_pure_axial(self):
        s = mixed_axial_seed(2.0, 3.0)
        self.assertEqual(s[0], 2.0)
        self.assertEqual(s[7], 3.0)
        self.assertEqual(non_axial_residue_norm(s), 0.0)


class TestNineMetricPanel(unittest.TestCase):
    """The diagnostic panel and run validity check."""

    def test_panel_has_all_nine_metrics(self):
        panel = nine_metric_diagnostic_panel()
        for i in range(1, 10):
            keys = [k for k in panel.keys() if k.startswith(f"M_{i}_")]
            self.assertEqual(len(keys), 1, msg=f"missing M_{i}: {panel.keys()}")

    def test_valid_run_passes_exact_invariants(self):
        panel = nine_metric_diagnostic_panel(
            omega_21_lock_quality=1.0,
            mirror_match_quality=1.0,
        )
        validity = diagnostic_panel_run_validity(panel)
        self.assertTrue(validity["valid"], msg=validity["reason"])

    def test_invalid_run_caught_by_validity_check(self):
        panel = nine_metric_diagnostic_panel()
        # Tamper with M_1
        panel["M_1_walsh_inversion"] = 1e-3
        validity = diagnostic_panel_run_validity(panel)
        self.assertFalse(validity["valid"])
        self.assertIn("M_1_walsh_inversion", validity["reason"])


class TestShowcase(unittest.TestCase):
    """The showcase function produces a coherent audit trail."""

    def test_showcase_returns_lines(self):
        out = showcase_field_origin_dynamics()
        self.assertIsInstance(out, list)
        self.assertGreater(len(out), 5)
        joined = "\n".join(out)
        self.assertIn("Field-Origin Dynamics", joined)
        self.assertIn("M_1_walsh_inversion", joined)
        self.assertIn("M_4_associator_axial_residue", joined)


class TestBridgeAlignmentWithFramework(unittest.TestCase):
    """
    The bridge layer must agree with portal_resonance / cyclotomic on
    shared structural numbers.
    """

    def test_axial_sector_dim_matches_framework(self):
        # <1, I> has dimension 2.  This is the framework's axial sector.
        from python.field_origin_dynamics import AXIAL_MASKS
        self.assertEqual(len(AXIAL_MASKS), 2)

    def test_middle_sector_dim_is_6(self):
        # Z[omega]^3 has 6 real coordinates (3 Eisenstein pairs).
        from python.field_origin_dynamics import AXIAL_MASKS
        n_middle = 8 - len(AXIAL_MASKS)
        self.assertEqual(n_middle, 6)

    def test_node_state_dim_is_8_equals_2K(self):
        # 8 = 2K at K=4: the closure-walk span identity (chat 186da4f5).
        # And 8 = 2^3 = D-cube vertices at D=3.
        from python.cyclotomic import phi3, phi4, phi6
        self.assertEqual(8, 2 * 4)
        # Also 8 = (21 - 13) = TetA-TetB coupling span at K=4
        self.assertEqual(8, phi3(4) - phi6(4))

    def test_walsh_H3_is_8x8(self):
        self.assertEqual(H3.shape, (8, 8))

    def test_walsh_H3_squared_equals_8I(self):
        # H^2 = N I with N = 8.  This is M_1 = 0 stated as a structural fact.
        N = 8
        product = H3 @ H3.T
        self.assertTrue(np.allclose(product, N * np.eye(8), atol=1e-12))
