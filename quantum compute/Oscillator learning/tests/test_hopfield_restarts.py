"""
test_hopfield_restarts.py
==========================

Test whether multi-restart with gauge tracking improves Hopfield retrieval
in the high-corruption regime.

Hypothesis:
  At 38-44% corruption, single-shot retrieval gets ~33%.
  If failures land in different wrong basins each restart, majority vote
  across multiple seeds should boost success significantly.
  If failures concentrate in the same wrong basin, restarts won't help.

  Gauge tracking adds: trust runs with low gauge (tight lock = correct
  basin) and discard high-gauge runs (loose lock = spurious state).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from collections import Counter

from test_hopfield import (hebbian_K, corrupt_pattern, hamming_distance,
                            identify_pattern, retrieve_kuramoto, retrieve)


def retrieve_with_gauge(query, K, depth=4, dt=0.05, steps=2000, seed=42,
                         init_noise=0.05):
    """
    Same as retrieve_kuramoto but also returns the SVD gauge.
    """
    N = len(query)
    rng = np.random.RandomState(seed)

    src, dst, kvals = [], [], []
    for i in range(N):
        for j in range(N):
            if i != j and abs(K[i, j]) > 1e-12:
                src.append(i); dst.append(j); kvals.append(K[i, j])
    src = np.array(src, dtype=np.int32)
    dst = np.array(dst, dtype=np.int32)
    kvals = np.array(kvals, dtype=np.float64)

    target = np.array([0.0 if query[i] == 1 else np.pi for i in range(N)])

    phi = np.zeros((depth, N))
    for ch in range(depth):
        for i in range(N):
            phi[ch, i] = target[i] + rng.uniform(-init_noise, init_noise)

    for step in range(steps):
        for ch in range(depth):
            diffs = phi[ch, dst] - phi[ch, src]
            forces = kvals * np.sin(diffs)
            kur = np.zeros(N)
            np.add.at(kur, src, forces)
            phi[ch] += dt * kur

    cos_avg = np.mean(np.cos(phi), axis=0)
    retrieved = np.sign(cos_avg).astype(int)
    retrieved[retrieved == 0] = 1

    # SVD for gauge
    cos_mat = np.array([np.cos(phi[ch] % (2 * np.pi)) for ch in range(depth)])
    _, Sv, _ = np.linalg.svd(cos_mat, full_matrices=False)
    gauge = float(Sv[-1] / Sv[0]) if Sv[0] > 1e-10 else 0.0

    # Lock quality: how close cos_avg is to ±1 (1 = perfect lock, 0 = noise)
    lock_quality = float(np.mean(np.abs(cos_avg)))

    return retrieved, gauge, lock_quality


def majority_vote(retrievals):
    """Take per-bit majority across multiple retrieved patterns."""
    if not retrievals:
        return None
    arr = np.array(retrievals)
    # Per-bit majority
    summed = np.sum(arr, axis=0)
    voted = np.sign(summed).astype(int)
    voted[voted == 0] = 1  # tie-break to +1
    return voted


def retrieve_multi_seed(query, K, n_restarts=5):
    """Run retrieval n_restarts times, return all (retrieved, gauge, lock) results."""
    results = []
    for r in range(n_restarts):
        retrieved, gauge, lock = retrieve_with_gauge(query, K, seed=42 + r * 137)
        results.append((retrieved, gauge, lock))
    return results


def vote_strategies(results):
    """Try different voting strategies on the multi-seed results."""
    all_retrievals = [r[0] for r in results]
    gauges = [r[1] for r in results]
    locks = [r[2] for r in results]

    # Strategy 1: simple majority across all restarts
    s1 = majority_vote(all_retrievals)

    # Strategy 2: lock-quality threshold (only count tight locks)
    median_lock = np.median(locks)
    high_lock = [r[0] for r in results if r[2] >= median_lock]
    s2 = majority_vote(high_lock) if high_lock else s1

    # Strategy 3: take best single (lowest gauge or highest lock)
    best_idx = max(range(len(results)), key=lambda i: results[i][2])  # highest lock
    s3 = results[best_idx][0]

    return {
        'majority': s1,
        'lock_filtered': s2,
        'best_single': s3,
        'all_results': all_retrievals,
        'gauges': gauges,
        'locks': locks,
    }


def evaluate_corruption_regime(n_flips, k_patterns, N, n_trials=15, n_restarts=5):
    """At given corruption level, compare single-shot vs multi-restart."""
    rng_p = np.random.RandomState(99)
    patterns = np.array([rng_p.choice([-1, 1], N) for _ in range(k_patterns)])
    K = hebbian_K(patterns)

    results = {
        'single_shot': 0,
        'majority': 0,
        'lock_filtered': 0,
        'best_single': 0,
        'discrete': 0,
        'total': 0,
    }
    distinct_wrong_basins = []

    for p_idx, p in enumerate(patterns):
        for trial in range(n_trials // k_patterns):
            query_seed = trial * 31 + p_idx * 17 + n_flips
            rng_q = np.random.RandomState(query_seed)
            query = corrupt_pattern(p, n_flips, rng_q)

            # Single-shot oscillator
            single, gauge, lock = retrieve_with_gauge(query, K, seed=query_seed)
            single_ok = (hamming_distance(single, p) == 0)

            # Discrete
            d_r, _ = retrieve(query, K)
            d_ok = (hamming_distance(d_r, p) == 0)

            # Multi-restart oscillator
            multi = retrieve_multi_seed(query, K, n_restarts=n_restarts)
            strategies = vote_strategies(multi)

            # Track basin diversity
            unique_results = set()
            for r in strategies['all_results']:
                unique_results.add(tuple(r.tolist()))
            distinct_wrong_basins.append(len(unique_results))

            results['single_shot'] += single_ok
            results['discrete'] += d_ok
            results['majority'] += (hamming_distance(strategies['majority'], p) == 0)
            results['lock_filtered'] += (hamming_distance(strategies['lock_filtered'], p) == 0)
            results['best_single'] += (hamming_distance(strategies['best_single'], p) == 0)
            results['total'] += 1

    return results, np.mean(distinct_wrong_basins)


def main():
    print("=" * 76)
    print("  Hopfield retrieval: does restart + gauge tracking help?")
    print("=" * 76)
    print()
    print("  Setup: 3 patterns, N=32, vary corruption.")
    print("  For each query, run 5 oscillator restarts, try 3 voting strategies.")
    print("  Compare to single-shot oscillator and discrete Hopfield.")
    print()
    print(f"  {'flips':>5}  {'%':>4}  "
          f"{'discrete':>9} {'single':>7} {'majority':>9} {'lock_filt':>10} "
          f"{'best_single':>12}  {'distinct_basins':>16}")

    N = 32
    k = 3
    for n_flips in [0, 4, 8, 10, 12, 14, 16]:
        results, distinct = evaluate_corruption_regime(
            n_flips, k_patterns=k, N=N, n_trials=15, n_restarts=5)
        t = results['total']
        d_pct = results['discrete'] / t
        s_pct = results['single_shot'] / t
        m_pct = results['majority'] / t
        l_pct = results['lock_filtered'] / t
        b_pct = results['best_single'] / t
        print(f"  {n_flips:>5}  {n_flips/N:>4.0%}  "
              f"{d_pct:>9.0%} {s_pct:>7.0%} {m_pct:>9.0%} {l_pct:>10.0%} "
              f"{b_pct:>12.0%}  {distinct:>16.2f}")

    print()
    print("  Reading the table:")
    print("    distinct_basins = avg # of unique results across 5 restarts.")
    print("      1.0 = all restarts give same answer (restarts don't help)")
    print("      >1  = restarts diverge, voting can disambiguate")
    print("    majority      = simple majority vote across 5 restarts")
    print("    lock_filtered = majority of restarts with above-median lock quality")
    print("    best_single   = highest-lock-quality single restart")


if __name__ == "__main__":
    main()
