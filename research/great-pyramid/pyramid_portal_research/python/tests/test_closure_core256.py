"""
test_closure_core256.py
=========================

Wraps closure_core256's verification harness into pytest so the 265
exact-algebra invariants run as part of the project regression suite.

The closure-core algebra is the *exact* substrate beneath the
resonance-wrapper layer in portal_resonance.py. Per the field-origin
integration document (AW 12), the master equation chain is:

    x_t  --(Walsh / Eisenstein)-->  R(x_t,x_{t+1},x_{t+2})
                                     |
                                     | Pi_axial
                                     v
                                    y_t  --(arg)-->  theta_{t+1}

The closure_core256 module verifies the bottom of this chain:
Walsh inversion, Eisenstein Omega^3 = 1, closure projector idempotence,
associator axial landing, and the 40/24 metric/torsion split on the
A_3 (X) A_3 = 64 tile.

This file does not duplicate those proofs.  It re-runs them under
pytest discovery so any regression in the closure-node engine shows
up alongside the rest of our suite.
"""

import unittest

from python.closure_core256 import run_tests, coupling_summary


class TestClosureCore256Invariants(unittest.TestCase):
    """The 265-test harness from closure_core256.run_tests() must pass."""

    def test_run_tests_passes_all_invariants(self):
        # run_tests() prints its own PASS lines on each invariant.  It
        # raises AssertionError on any failure.  Capture the structured
        # summary it returns so we can also pin specific numerical
        # outputs (coupling table, tile decompositions, core summary).
        summary = run_tests(verbose=False)
        self.assertIsInstance(summary, dict)
        # The summary key set is a structural invariant of the package;
        # if it changes silently the bridge below may break.
        expected_keys = {
            "hexagon_projection",
            "coupling_summary_K4",
            "tile_tensor_family_summary",
            "tile_face_rank2_summary",
            "core_summary",
            "closure_norm_distribution",
        }
        self.assertTrue(expected_keys.issubset(summary.keys()),
                        msg=f"missing keys: {expected_keys - set(summary.keys())}")

    def test_coupling_summary_K4_matches_framework(self):
        s = coupling_summary(4)
        # The five-number signature that the framework spine pins:
        self.assertEqual(s["f_plus"], 21)
        self.assertEqual(s["f_zero"], 17)
        self.assertEqual(s["f_minus"], 13)
        self.assertEqual(s["product_plus_minus"], 273)
        self.assertEqual(s["S_3_K"], 273)
        self.assertEqual(s["P2_F_K2"], 273)
        # The 40/24 metric/torsion split at tile level:
        self.assertEqual(s["four_face_sym"], 40)
        self.assertEqual(s["four_face_ext"], 24)
        self.assertEqual(s["four_face_total"], 64)
        self.assertEqual(s["sym_per_face"], 10)
        self.assertEqual(s["ext_per_face"], 6)


class TestClosureCoreFrameworkAlignment(unittest.TestCase):
    """
    Pin the alignment between closure_core256 numbers and the cyclotomic
    primitives used elsewhere in the package.  If either side drifts,
    the bridge breaks.
    """

    def test_273_equals_phi3_times_phi6_at_K4(self):
        from python.cyclotomic import phi3, phi6
        from python.closure_core256 import coupling_summary
        s = coupling_summary(4)
        self.assertEqual(s["product_plus_minus"], phi3(4) * phi6(4))

    def test_sierpinski_S_D3_K4_equals_273(self):
        from python.closure_core256 import sierpinski_S
        # S(3,4) = 1 + K^2 + K^4 = 1 + 16 + 256 = 273.
        self.assertEqual(sierpinski_S(3, 4), 273)

    def test_projective_plane_F16_equals_273(self):
        # |P^2(F_16)| = q^2 + q + 1 with q = K^2 = 16
        from python.closure_core256 import projective_plane_q2_count
        self.assertEqual(projective_plane_q2_count(4), 273)

    def test_40_24_split_matches_AW09_local_dimensions(self):
        # In AW 09 the local sector dimensions sum to 120 = |S_5|.
        # The 40 + 24 piece of that sum is the per-tile metric/torsion split.
        from python.closure_core256 import coupling_summary
        s = coupling_summary(4)
        self.assertEqual(s["four_face_sym"] + s["four_face_ext"], 64)
        self.assertEqual(s["four_face_sym"], 40)
        self.assertEqual(s["four_face_ext"], 24)
