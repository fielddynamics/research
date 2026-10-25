"""
test_mirror_match_distribution.py
====================================

Tests for the mirror-match distribution analysis (Tier 1 #5).
"""

import unittest
import numpy as np

from python.mirror_match_distribution import (
    random_unit_vector, random_shaft_keys, random_address, mirror_pair,
    DistributionStats,
    sample_mirror_match_distribution, sample_designed_mirror_pairs,
    chirality_gate, phase_gate, gram_gate,
    gate_decomposition_stats,
    tolerance_sweep,
    showcase_mirror_match_distribution,
)


class TestRandomGeneration(unittest.TestCase):

    def test_random_unit_vector_is_unit_norm(self):
        rng = np.random.default_rng(0)
        for _ in range(20):
            v = random_unit_vector(rng)
            n = np.sqrt(sum(x * x for x in v))
            self.assertAlmostEqual(n, 1.0, places=10)

    def test_random_address_has_triad(self):
        rng = np.random.default_rng(1)
        addr = random_address(rng)
        self.assertEqual(len(addr.triad), 3)


class TestMirrorPairConstruction(unittest.TestCase):

    def test_mirror_pair_preserves_gram(self):
        rng = np.random.default_rng(2)
        u = random_address(rng)
        v = mirror_pair(u)
        for i in range(3):
            for j in range(3):
                self.assertAlmostEqual(u.gram[i][j], v.gram[i][j], places=10)

    def test_mirror_pair_flips_chirality(self):
        rng = np.random.default_rng(3)
        u = random_address(rng)
        v = mirror_pair(u)
        # Random triads almost always have non-zero chirality
        if u.chirality != 0:
            self.assertEqual(v.chirality, -u.chirality)

    def test_mirror_pair_preserves_phase(self):
        rng = np.random.default_rng(4)
        u = random_address(rng)
        v = mirror_pair(u)
        self.assertEqual(v.phase, u.phase)


class TestRandomMatchDistribution(unittest.TestCase):
    """Random pairs should give M ≈ 0 (bimodal spike at zero)."""

    def test_random_pairs_almost_all_zero(self):
        stats = sample_mirror_match_distribution(n_pairs=100, seed=42)
        # >= 95% of random pairs give M = 0
        self.assertGreaterEqual(stats.n_zero / stats.n_pairs, 0.95)

    def test_random_pairs_max_is_small(self):
        stats = sample_mirror_match_distribution(n_pairs=200, seed=42)
        self.assertLess(stats.max_value, 0.01)


class TestDesignedMatchDistribution(unittest.TestCase):
    """Designed mirror pairs should give M ≈ 1."""

    def test_designed_pairs_match_perfectly(self):
        stats = sample_designed_mirror_pairs(n_pairs=50, seed=7)
        # All designed pairs should give M close to 1
        self.assertGreaterEqual(stats.n_above_0_9, 45)  # at least 45/50

    def test_designed_pairs_have_max_M_at_one(self):
        stats = sample_designed_mirror_pairs(n_pairs=30, seed=7)
        self.assertAlmostEqual(stats.max_value, 1.0, places=4)


class TestGateDecomposition(unittest.TestCase):

    def test_chirality_gate_fires_about_half(self):
        # For random chirality assignments (each ±1 with prob ~1/2),
        # the gate fires with prob ~1/2
        stats = gate_decomposition_stats(n_pairs=400, seed=11)
        rate = stats["chirality_fire_rate"]
        self.assertGreater(rate, 0.4)
        self.assertLess(rate, 0.6)

    def test_phase_gate_rarely_fires_for_random_pairs(self):
        # Phase closure is a measure-zero condition for random phases
        stats = gate_decomposition_stats(n_pairs=200, seed=13)
        self.assertEqual(stats["phase_fire_rate"], 0.0)

    def test_gram_gate_rarely_fires_for_random_pairs(self):
        # Random Gram matrices match with probability ~ε^3 ≈ 0 at small ε
        stats = gate_decomposition_stats(n_pairs=200, seed=15)
        self.assertEqual(stats["gram_fire_rate"], 0.0)

    def test_all_three_fire_is_zero_for_random(self):
        stats = gate_decomposition_stats(n_pairs=300, seed=17)
        self.assertEqual(stats["all_three_fire_rate"], 0.0)


class TestIndividualGates(unittest.TestCase):

    def test_chirality_gate_at_opposite_chiralities(self):
        rng = np.random.default_rng(0)
        u = random_address(rng)
        v = mirror_pair(u)
        if u.chirality != 0 and v.chirality != 0:
            self.assertAlmostEqual(chirality_gate(u, v), 1.0)

    def test_phase_gate_at_matching_phases(self):
        rng = np.random.default_rng(0)
        u = random_address(rng)
        v = mirror_pair(u)
        self.assertAlmostEqual(phase_gate(u, v), 1.0)

    def test_gram_gate_at_matching_gram_at_least_1(self):
        rng = np.random.default_rng(0)
        u = random_address(rng)
        v = mirror_pair(u)
        # Identity permutation contributes exp(0) = 1
        self.assertGreaterEqual(gram_gate(u, v, epsilon=1e-3), 1.0)


class TestToleranceSweep(unittest.TestCase):

    def test_sweep_designed_pairs_all_match(self):
        sweep = tolerance_sweep(use_designed_pairs=True, n_pairs=30)
        for row in sweep:
            self.assertGreater(row["max_M"], 0.9)

    def test_sweep_random_pairs_no_match(self):
        sweep = tolerance_sweep(use_designed_pairs=False, n_pairs=30)
        # At small epsilon, max should be ≈ 0; at large epsilon, may have noise
        for row in sweep:
            if row["epsilon"] < 1e-2:
                self.assertLess(row["max_M"], 0.5)


class TestShowcase(unittest.TestCase):

    def test_showcase_returns_lines(self):
        out = showcase_mirror_match_distribution()
        self.assertIsInstance(out, list)
        self.assertGreater(len(out), 10)

    def test_showcase_mentions_canonical_terms(self):
        joined = "\n".join(showcase_mirror_match_distribution())
        for token in ("Random", "Designed", "chirality", "phase", "Gram"):
            self.assertIn(token, joined, msg=f"missing: {token}")
