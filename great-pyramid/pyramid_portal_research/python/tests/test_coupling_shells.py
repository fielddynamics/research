"""
test_coupling_shells.py
=========================

Tests for the parity-pushout recursion and the full K=1..K=5 coupling
shell family.  Verifies the 5 missing identities from the engineering
synthesis (appendix I).
"""

import unittest

from python.coupling_shells import (
    parity_pushout_step,
    parity_pushout_orbit,
    parity_pushout_closed_form,
    CouplingShell, SHELL_NAMES,
    coupling_shell, coupling_shell_family, coupling_shell_table,
    adjacent_shell_lock_check, adjacent_shell_lock_scan,
    discriminant_identity_squared,
    directed_simplex_edge_identity,
    projective_plane_general, projective_plane_identity_check,
    is_prime_power,
    parity_pushout_category, ParityPushoutMorphism,
    star_transition_K3_to_K4, portal_transition_K4_to_K5,
    showcase_coupling_shells,
)


# ===========================================================================
# Parity-pushout recursion
# ===========================================================================

class TestParityPushoutRecursion(unittest.TestCase):

    def test_step_adds_2K(self):
        # C_{K+1} = C_K + 2K
        self.assertEqual(parity_pushout_step(1, 1), 3)
        self.assertEqual(parity_pushout_step(3, 2), 7)
        self.assertEqual(parity_pushout_step(7, 3), 13)
        self.assertEqual(parity_pushout_step(13, 4), 21)
        self.assertEqual(parity_pushout_step(21, 5), 31)

    def test_orbit_from_seed_1_gives_canonical_shell_cores(self):
        # Starting from C_1 = 1, the orbit is 1, 3, 7, 13, 21
        orbit = parity_pushout_orbit(5)
        self.assertEqual(orbit, [1, 3, 7, 13, 21])

    def test_orbit_extends_to_K6_giving_31(self):
        # Extending: at K=5, C_6 = C_5 + 2*5 = 21 + 10 = 31
        orbit = parity_pushout_orbit(6)
        self.assertEqual(orbit, [1, 3, 7, 13, 21, 31])

    def test_closed_form_matches_phi6(self):
        # |C_K| = K^2 - K + 1 = Phi_6(K) starting from C_1 = 1
        from python.cyclotomic import phi6
        for K in range(1, 10):
            self.assertEqual(parity_pushout_closed_form(K), phi6(K),
                             msg=f"closed form failed at K={K}")


# ===========================================================================
# The named shell family
# ===========================================================================

class TestCouplingShellFamily(unittest.TestCase):

    def test_K1_seed_shell_is_1_2_3(self):
        s = coupling_shell(1)
        self.assertEqual(s.tuple, (1, 2, 3))
        self.assertEqual(s.name, "Seed")

    def test_K2_Fano_seed_shell_is_3_5_7(self):
        s = coupling_shell(2)
        self.assertEqual(s.tuple, (3, 5, 7))
        self.assertEqual(s.name, "Fano seed")

    def test_K3_star_of_David_shell_is_7_10_13(self):
        s = coupling_shell(3)
        self.assertEqual(s.tuple, (7, 10, 13))
        self.assertEqual(s.name, "Star-of-David")

    def test_K4_tetrad_shell_is_13_17_21(self):
        s = coupling_shell(4)
        self.assertEqual(s.tuple, (13, 17, 21))
        self.assertEqual(s.name, "Tetrad")

    def test_K5_receiver_shell_is_21_26_31(self):
        s = coupling_shell(5)
        self.assertEqual(s.tuple, (21, 26, 31))
        self.assertEqual(s.name, "Receiver")

    def test_family_length(self):
        family = coupling_shell_family(5)
        self.assertEqual(len(family), 5)

    def test_decomposition_strings(self):
        # 21 = 13 + 4 + 4 at K=4
        s = coupling_shell(4)
        self.assertEqual(s.decomposition, "21 = 13 + 4 + 4")
        # 7 = 3 + 2 + 2 at K=2 (Fano)
        s = coupling_shell(2)
        self.assertEqual(s.decomposition, "7 = 3 + 2 + 2")

    def test_table_has_expected_keys(self):
        table = coupling_shell_table(5)
        for row in table:
            for key in ("K", "name", "shared_core", "each_sheet",
                        "full_union", "decomposition"):
                self.assertIn(key, row)


# ===========================================================================
# Adjacent-shell lock: f_+(K) = f_-(K+1)
# ===========================================================================

class TestAdjacentShellLock(unittest.TestCase):

    def test_lock_K1_to_K2(self):
        # f_+(1) = 3 = f_-(2)
        r = adjacent_shell_lock_check(1)
        self.assertEqual(r["f_plus_K"], 3)
        self.assertEqual(r["f_minus_K_plus_1"], 3)
        self.assertTrue(r["locked"])

    def test_lock_K2_to_K3(self):
        # f_+(2) = 7 = f_-(3)
        r = adjacent_shell_lock_check(2)
        self.assertEqual(r["f_plus_K"], 7)
        self.assertEqual(r["f_minus_K_plus_1"], 7)
        self.assertTrue(r["locked"])

    def test_lock_K3_to_K4(self):
        # f_+(3) = 13 = f_-(4)  (Star -> Tetrad)
        r = adjacent_shell_lock_check(3)
        self.assertEqual(r["f_plus_K"], 13)
        self.assertEqual(r["f_minus_K_plus_1"], 13)
        self.assertTrue(r["locked"])

    def test_lock_K4_to_K5(self):
        # f_+(4) = 21 = f_-(5)  (Tetrad -> Receiver, the portal hinge)
        r = adjacent_shell_lock_check(4)
        self.assertEqual(r["f_plus_K"], 21)
        self.assertEqual(r["f_minus_K_plus_1"], 21)
        self.assertTrue(r["locked"])

    def test_full_scan_K1_to_K5(self):
        scan = adjacent_shell_lock_scan(5)
        self.assertTrue(scan["all_locked"])


# ===========================================================================
# Discriminant identity: (f_+ - f_-)^2 = 4K^2
# ===========================================================================

class TestDiscriminantIdentity(unittest.TestCase):

    def test_K4_gives_64(self):
        # (21 - 13)^2 = 64 = 4 * 16 = K^3 at K=4
        r = discriminant_identity_squared(4)
        self.assertEqual(r["delta"], 8)
        self.assertEqual(r["delta_squared"], 64)
        self.assertEqual(r["four_K_squared"], 64)
        self.assertTrue(r["matches"])

    def test_identity_universal(self):
        # The identity holds at every K
        for K in range(1, 15):
            r = discriminant_identity_squared(K)
            self.assertTrue(r["matches"], msg=f"failed at K={K}: {r}")

    def test_delta_always_2K(self):
        # delta = f_+ - f_- = 2K
        for K in range(1, 10):
            r = discriminant_identity_squared(K)
            self.assertEqual(r["delta"], 2 * K)


# ===========================================================================
# Directed simplex edge identity: f_+(K) - 1 = 2 C(K+1, 2)
# ===========================================================================

class TestDirectedSimplexEdge(unittest.TestCase):

    def test_K4_pentachoron_has_20_edges(self):
        # f_+(4) - 1 = 21 - 1 = 20 = K(K+1) = 4*5
        r = directed_simplex_edge_identity(4)
        self.assertEqual(r["f_plus_K_minus_1"], 20)
        self.assertEqual(r["two_binom_K_plus_1_choose_2"], 20)
        self.assertEqual(r["K_times_K_plus_1"], 20)
        self.assertTrue(r["matches"])

    def test_K3_tetrahedron_has_12_edges(self):
        # f_+(3) - 1 = 13 - 1 = 12 = K(K+1) = 3*4
        r = directed_simplex_edge_identity(3)
        self.assertEqual(r["f_plus_K_minus_1"], 12)
        self.assertTrue(r["matches"])

    def test_identity_universal(self):
        for K in range(1, 10):
            r = directed_simplex_edge_identity(K)
            self.assertTrue(r["matches"], msg=f"failed at K={K}: {r}")


# ===========================================================================
# Projective plane identity: f_+(q) = |P^2(F_q)| at prime powers
# ===========================================================================

class TestProjectivePlaneIdentity(unittest.TestCase):

    def test_Fano_plane_at_q2(self):
        # |P^2(F_2)| = 7 (Fano plane has 7 points)
        self.assertEqual(projective_plane_general(2), 7)
        r = projective_plane_identity_check(2)
        self.assertTrue(r["matches"])

    def test_plane_at_q3_is_13(self):
        self.assertEqual(projective_plane_general(3), 13)
        r = projective_plane_identity_check(3)
        self.assertTrue(r["matches"])

    def test_plane_at_q4_is_21_pentachoron_overlap(self):
        # q=4 is the framework's preferred prime power, giving 21 = f_+(4)
        self.assertEqual(projective_plane_general(4), 21)
        r = projective_plane_identity_check(4)
        self.assertTrue(r["matches"])

    def test_identity_across_prime_powers(self):
        # Check the identity at small prime powers
        prime_powers = (2, 3, 4, 5, 7, 8, 9, 11, 13, 16)
        for q in prime_powers:
            r = projective_plane_identity_check(q)
            self.assertTrue(r["matches"], msg=f"failed at q={q}: {r}")

    def test_is_prime_power_basics(self):
        self.assertTrue(is_prime_power(2))
        self.assertTrue(is_prime_power(3))
        self.assertTrue(is_prime_power(4))   # 2^2
        self.assertTrue(is_prime_power(5))
        self.assertTrue(is_prime_power(7))
        self.assertTrue(is_prime_power(8))   # 2^3
        self.assertTrue(is_prime_power(9))   # 3^2
        self.assertTrue(is_prime_power(16))  # 2^4
        self.assertFalse(is_prime_power(6))  # 2*3
        self.assertFalse(is_prime_power(10)) # 2*5
        self.assertFalse(is_prime_power(12)) # 2^2 * 3
        self.assertFalse(is_prime_power(1))


# ===========================================================================
# Parity-pushout category
# ===========================================================================

class TestParityPushoutCategory(unittest.TestCase):

    def test_category_has_objects_and_morphisms(self):
        cat = parity_pushout_category()
        self.assertIn("objects", cat)
        self.assertIn("morphisms", cat)

    def test_category_has_five_morphisms(self):
        cat = parity_pushout_category()
        names = [m.name for m in cat["morphisms"]]
        for required in ("parity_pushout", "shift", "fusion", "edge", "projective"):
            self.assertIn(required, names)

    def test_each_morphism_has_algebraic_form(self):
        cat = parity_pushout_category()
        for m in cat["morphisms"]:
            self.assertIsInstance(m, ParityPushoutMorphism)
            self.assertTrue(m.algebraic_form, msg=f"{m.name} has empty form")


# ===========================================================================
# Named transitions: star (K=3->K=4) and portal (K=4->K=5)
# ===========================================================================

class TestNamedTransitions(unittest.TestCase):

    def test_star_transition_bridge_is_13(self):
        t = star_transition_K3_to_K4()
        self.assertEqual(t["from_shell"], (7, 10, 13))
        self.assertEqual(t["to_shell"], (13, 17, 21))
        self.assertEqual(t["bridge_value"], 13)
        self.assertTrue(t["is_locked"])

    def test_portal_transition_bridge_is_21(self):
        t = portal_transition_K4_to_K5()
        self.assertEqual(t["from_shell"], (13, 17, 21))
        self.assertEqual(t["to_shell"], (21, 26, 31))
        self.assertEqual(t["bridge_value"], 21)
        self.assertTrue(t["is_locked"])

    def test_portal_bridge_equals_framework_21_band(self):
        # The portal bridge value 21 IS the framework's 21-band that
        # drives gravity coupling alpha^21.  Verify equality.
        from python.cyclotomic import phi3
        t = portal_transition_K4_to_K5()
        self.assertEqual(t["bridge_value"], phi3(4))


# ===========================================================================
# Cross-module alignment
# ===========================================================================

class TestAlignmentWithFramework(unittest.TestCase):

    def test_shell_K4_matches_cyclotomic_shell(self):
        from python.cyclotomic import shell as cyclotomic_shell
        coupling = coupling_shell(4)
        cyc = cyclotomic_shell(4)
        self.assertEqual(coupling.tuple, cyc.tuple)

    def test_shell_K5_matches_cyclotomic_shell(self):
        from python.cyclotomic import shell as cyclotomic_shell
        coupling = coupling_shell(5)
        cyc = cyclotomic_shell(5)
        self.assertEqual(coupling.tuple, cyc.tuple)

    def test_adjacent_lock_matches_shift_identity(self):
        # f_+(K) = f_-(K+1) is the same as Phi_3(K) = Phi_6(K+1)
        from python.cyclotomic import shift_identity
        for K in range(1, 8):
            lock = adjacent_shell_lock_check(K)
            shift = shift_identity(K)
            self.assertEqual(lock["locked"], shift["holds"])

    def test_directed_simplex_K4_matches_pentachoron_edges(self):
        # f_+(4) - 1 = 20 = pentachoron directed edges
        from python.gravity import pentachoron_directed_edge_count
        edge_id = directed_simplex_edge_identity(4)
        self.assertEqual(edge_id["f_plus_K_minus_1"],
                         pentachoron_directed_edge_count())

    def test_discriminant_K4_matches_AW09_64_tile(self):
        # (21-13)^2 = 64 = the closure tile total
        from python.closure_core256 import coupling_summary
        d = discriminant_identity_squared(4)
        s = coupling_summary(4)
        self.assertEqual(d["delta_squared"], s["four_face_total"])
        self.assertEqual(d["four_K_squared"], 64)


# ===========================================================================
# Showcase audit
# ===========================================================================

class TestShowcase(unittest.TestCase):

    def test_showcase_returns_lines(self):
        out = showcase_coupling_shells()
        self.assertIsInstance(out, list)
        self.assertGreater(len(out), 20)

    def test_showcase_mentions_all_five_named_shells(self):
        joined = "\n".join(showcase_coupling_shells())
        for name in ("Seed", "Fano", "Star-of-David", "Tetrad", "Receiver"):
            self.assertIn(name, joined)

    def test_showcase_mentions_critical_numbers(self):
        joined = "\n".join(showcase_coupling_shells())
        for n in ("1", "3", "7", "13", "21", "31"):
            self.assertIn(n, joined)

    def test_showcase_mentions_named_transitions(self):
        joined = "\n".join(showcase_coupling_shells())
        self.assertIn("Star transition", joined)
        self.assertIn("Portal transition", joined)
