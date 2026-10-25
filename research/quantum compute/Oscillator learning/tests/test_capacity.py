"""
test_capacity.py
=================

How does N=100 oscillators handle increasing knowledge?

Stream facts in, after each batch measure:
  1. Gauge (S_last/S_0) — does the depth=8 cascade resolve cleanly?
  2. Spectrum width — how many modes carry meaningful eigenvalue mass?
  3. Embedding quality — do held-out semantic queries still work?
  4. Capacity ratio — facts/N²

Question: at what facts/N ratio does quality degrade, and does any
internal signal (gauge, spectrum) detect it before quality fails?
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import time
from gfd_oscillator import GFDOscillator
from ontology_learner_large import build_facts, build_K, build_vocab, embed, cos_sim, nearest


def measure_quality(emb, vocab, test_pairs):
    """For each (a, b, expect_close) pair, compute cosine similarity.
    Return mean cosine for expect_close pairs minus mean for expect_far.
    Higher = better discrimination."""
    close_sims = []
    far_sims = []
    for a, b, kind in test_pairs:
        if a not in vocab or b not in vocab:
            continue
        s = cos_sim(emb[vocab.index(a)], emb[vocab.index(b)])
        if kind == "close":
            close_sims.append(s)
        else:
            far_sims.append(s)
    if not close_sims or not far_sims:
        return float('nan'), float('nan'), float('nan')
    return (np.mean(close_sims), np.mean(far_sims),
            np.mean(close_sims) - np.mean(far_sims))


# Held-out test pairs from the ontology — should be stable as we add knowledge
TEST_PAIRS = [
    # Same-class pairs (should be close)
    ("cat", "dog", "close"),
    ("lion", "tiger", "close"),
    ("salmon", "tuna", "close"),
    ("eagle", "hawk", "close"),
    ("snake", "lizard", "close"),
    ("bee", "butterfly", "close"),
    # Different-class pairs (should be far)
    ("cat", "salmon", "far"),
    ("eagle", "snake", "far"),
    ("bee", "lion", "far"),
    ("frog", "eagle", "far"),
    # Cross-attribute (should be far)
    ("ocean", "desert", "far"),
    ("predator", "grass", "far"),
]


def main():
    print("=" * 76)
    print(" CAPACITY PROBE: how does fixed N handle growing knowledge?")
    print("=" * 76)

    # Get all facts, then stream in batches
    all_facts = build_facts()
    print(f"\n  Total facts available: {len(all_facts)}")
    print(f"  Test pairs: {len(TEST_PAIRS)} ({sum(1 for _,_,k in TEST_PAIRS if k=='close')} close, {sum(1 for _,_,k in TEST_PAIRS if k=='far')} far)")

    # Stream facts in increasing batches
    batch_sizes = [50, 100, 150, 200, 272]

    print(f"\n  {'#facts':>7s} {'N':>5s} {'edges':>7s} "
          f"{'cap=facts/N²':>13s} "
          f"{'gauge':>10s} {'eigval_top':>11s} {'eigval_last':>12s} "
          f"{'cos_close':>10s} {'cos_far':>9s} {'discrim':>8s}")

    for n_facts in batch_sizes:
        facts_subset = all_facts[:n_facts]
        vocab, vocab_idx = build_vocab(facts_subset)
        N = len(vocab)
        K, C = build_K(facts_subset, vocab_idx)
        n_edges = (C > 0).sum()

        # Gauge from a single oscillator pass at depth=8
        osc = GFDOscillator(dt=0.05, steps=2000)
        graph = GFDOscillator.encode_weighted(N, K)
        state = osc.run_phase(graph, depth=8, seed=42)
        gauge = state.gauge

        # Run full deflation cascade for embedding
        emb, eigvals = embed(K, n_dims=12, depth=8, verbose=False)
        eig_top = eigvals[0] if eigvals else float('nan')
        eig_last = eigvals[-1] if len(eigvals) >= 12 else float('nan')

        # Quality
        m_close, m_far, discrim = measure_quality(emb, vocab, TEST_PAIRS)

        capacity = n_facts / (N * N) if N > 0 else float('nan')
        print(f"  {n_facts:>7d} {N:>5d} {n_edges:>7d} "
              f"{capacity:>13.4f} "
              f"{gauge:>10.4f} {eig_top:>11.3f} {eig_last:>12.3f} "
              f"{m_close:>+10.3f} {m_far:>+9.3f} {discrim:>+8.3f}")

    print()
    print("  Reading the table:")
    print("    gauge      = S_last/S_0 from depth=8 single pass")
    print("    eig_top    = magnitude of dominant deflation eigenvalue")
    print("    eig_last   = magnitude of 12th deflation eigenvalue")
    print("    cos_close  = avg cosine for semantically-close pairs (higher = better)")
    print("    cos_far    = avg cosine for semantically-far pairs (lower = better)")
    print("    discrim    = cos_close - cos_far (higher = sharper semantic structure)")


if __name__ == "__main__":
    main()
