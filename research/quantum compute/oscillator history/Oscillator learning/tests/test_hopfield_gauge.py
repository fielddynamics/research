"""
test_hopfield_gauge.py
=======================

Measure gauge values during Hopfield retrieval and test:
  1. Does gauge correlate with retrieval success?
  2. Is gauge > 1% at high corruption?
  3. Does increasing depth (8, 16, 32) fix the high-corruption failures?
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from test_hopfield import hebbian_K, corrupt_pattern, hamming_distance, retrieve


def retrieve_with_full_diagnostics(query, K, depth=4, dt=0.05, steps=2000,
                                   seed=42, init_noise=0.05):
    """Returns (retrieved, gauge, lock_quality, all_Sv)."""
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

    cos_mat = np.array([np.cos(phi[ch] % (2 * np.pi)) for ch in range(depth)])
    _, Sv, _ = np.linalg.svd(cos_mat, full_matrices=False)
    gauge = float(Sv[-1] / Sv[0]) if Sv[0] > 1e-10 else 0.0
    lock_quality = float(np.mean(np.abs(cos_avg)))

    return retrieved, gauge, lock_quality, Sv


# ---------------------------------------------------------------
def t1_gauge_vs_success():
    """At each corruption level, measure gauge for successes vs failures."""
    print("=" * 76)
    print("  T1: Gauge values per corruption level (depth=4)")
    print("=" * 76)
    print()

    rng_p = np.random.RandomState(99)
    N = 32
    k = 3
    patterns = np.array([rng_p.choice([-1, 1], N) for _ in range(k)])
    K = hebbian_K(patterns)

    print(f"  K eigenvalues (top 5): {sorted(np.linalg.eigvalsh(K))[-5:]}")
    print()
    print(f"  {'flips':>5}  {'%':>4}  "
          f"{'avg_gauge':>10} {'gauge_success':>14} {'gauge_fail':>11}  "
          f"{'success%':>9}  {'gauge<1%':>9}")

    for n_flips in [0, 4, 8, 10, 12, 14, 16]:
        gauges = []
        gauges_succ = []
        gauges_fail = []
        n_succ = 0
        n_low_gauge = 0
        n_total = 0

        for p_idx, p in enumerate(patterns):
            for trial in range(5):
                query_seed = trial * 31 + p_idx * 17 + n_flips
                rng_q = np.random.RandomState(query_seed)
                query = corrupt_pattern(p, n_flips, rng_q)
                retrieved, gauge, lock, Sv = retrieve_with_full_diagnostics(
                    query, K, depth=4, seed=query_seed)
                ok = (hamming_distance(retrieved, p) == 0)
                gauges.append(gauge)
                if ok:
                    gauges_succ.append(gauge)
                    n_succ += 1
                else:
                    gauges_fail.append(gauge)
                if gauge < 0.01:
                    n_low_gauge += 1
                n_total += 1

        avg_g = np.mean(gauges)
        avg_g_s = np.mean(gauges_succ) if gauges_succ else float('nan')
        avg_g_f = np.mean(gauges_fail) if gauges_fail else float('nan')
        print(f"  {n_flips:>5}  {n_flips/N:>4.0%}  "
              f"{avg_g:>10.4f} {avg_g_s:>14.4f} {avg_g_f:>11.4f}  "
              f"{n_succ/n_total:>9.0%}  {n_low_gauge/n_total:>9.0%}")

    print()
    print("  Reading: if gauge_success < gauge_fail, gauge correctly flags bad runs.")
    print("           If gauge_fail > 0.01, depth-doubling SHOULD help those runs.")


def t2_depth_scaling():
    """Take a high-corruption case, run at depth=4, 8, 16, 32. Does success rate climb?"""
    print()
    print("=" * 76)
    print("  T2: Does depth scaling rescue high-corruption retrievals?")
    print("=" * 76)
    print()

    rng_p = np.random.RandomState(99)
    N = 32
    k = 3
    patterns = np.array([rng_p.choice([-1, 1], N) for _ in range(k)])
    K = hebbian_K(patterns)

    print(f"  Test: 14 flips (44% corruption), 15 trials at each depth")
    print()
    print(f"  {'depth':>5}  {'success%':>9}  {'avg_gauge':>10}  "
          f"{'gauge<1%':>9}  {'avg_lock':>9}")

    for depth in [4, 8, 16, 32]:
        gauges = []
        n_succ = 0
        n_total = 0
        n_low_gauge = 0
        locks = []

        for p_idx, p in enumerate(patterns):
            for trial in range(5):
                query_seed = trial * 31 + p_idx * 17 + 14
                rng_q = np.random.RandomState(query_seed)
                query = corrupt_pattern(p, 14, rng_q)
                retrieved, gauge, lock, _ = retrieve_with_full_diagnostics(
                    query, K, depth=depth, seed=query_seed)
                ok = (hamming_distance(retrieved, p) == 0)
                gauges.append(gauge)
                locks.append(lock)
                if ok:
                    n_succ += 1
                if gauge < 0.01:
                    n_low_gauge += 1
                n_total += 1

        print(f"  {depth:>5}  {n_succ/n_total:>9.0%}  {np.mean(gauges):>10.4f}  "
              f"{n_low_gauge/n_total:>9.0%}  {np.mean(locks):>9.4f}")


def t3_gauge_filter():
    """At each corruption level, what does the success rate look like if we ONLY
    accept runs with gauge < 1%, treating high-gauge as 'don't know'?"""
    print()
    print("=" * 76)
    print("  T3: Gauge-filtered retrieval — only trust gauge < 1%")
    print("=" * 76)
    print()

    rng_p = np.random.RandomState(99)
    N = 32
    k = 3
    patterns = np.array([rng_p.choice([-1, 1], N) for _ in range(k)])
    K = hebbian_K(patterns)

    print(f"  {'flips':>5}  {'%':>4}  "
          f"{'all_runs%':>10}  {'low_gauge%':>11}  "
          f"{'success_when_low_gauge':>23}  {'success_when_high_gauge':>24}")

    for n_flips in [0, 4, 8, 10, 12, 14]:
        n_total = 0
        n_succ = 0
        n_low_gauge = 0
        n_succ_low = 0
        n_succ_high = 0
        n_high_gauge = 0

        for p_idx, p in enumerate(patterns):
            for trial in range(10):
                query_seed = trial * 31 + p_idx * 17 + n_flips
                rng_q = np.random.RandomState(query_seed)
                query = corrupt_pattern(p, n_flips, rng_q)
                retrieved, gauge, _, _ = retrieve_with_full_diagnostics(
                    query, K, depth=4, seed=query_seed)
                ok = (hamming_distance(retrieved, p) == 0)
                n_total += 1
                if ok: n_succ += 1
                if gauge < 0.01:
                    n_low_gauge += 1
                    if ok: n_succ_low += 1
                else:
                    n_high_gauge += 1
                    if ok: n_succ_high += 1

        all_pct = n_succ / n_total
        low_g_pct = n_low_gauge / n_total
        succ_low = (n_succ_low / n_low_gauge) if n_low_gauge > 0 else float('nan')
        succ_high = (n_succ_high / n_high_gauge) if n_high_gauge > 0 else float('nan')
        print(f"  {n_flips:>5}  {n_flips/N:>4.0%}  "
              f"{all_pct:>10.0%}  {low_g_pct:>11.0%}  "
              f"{succ_low:>23.0%}  {succ_high:>24.0%}")
    print()
    print("  Reading: if 'success_when_low_gauge' >> 'success_when_high_gauge',")
    print("           the gauge IS a reliable confidence meter for retrieval.")


def main():
    t1_gauge_vs_success()
    t2_depth_scaling()
    t3_gauge_filter()


if __name__ == "__main__":
    main()
