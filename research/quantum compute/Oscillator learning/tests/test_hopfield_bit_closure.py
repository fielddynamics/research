"""
test_hopfield_bit_closure.py
==============================

Bit-level field closure: round 1 produces a candidate retrieval r₁ with
per-bit confidence (lock quality at each phase).  Round 2 LOCKS the
confident bits and re-solves only the uncertain bits.

Mechanism:
  1. Run oscillator on K with query as init.
  2. Each retrieved bit r_i has a per-node lock quality |cos(φ_i)|.
     High |cos(φ_i)| → confident lock.  Low → uncertain.
  3. Pick threshold τ.  Bits with |cos(φ_i)| ≥ τ are LOCKED at sign(cos).
  4. For bits below τ, run a SECOND oscillator on the projected
     sub-problem: K restricted to uncertain bits, with locked bits acting
     as fixed external biases on the dynamics of uncertain bits.
  5. Combine: locked bits unchanged + uncertain bits from round 2.

This mirrors the 3+1 nested oscillator's idea: outer level locks, inner
level handles the residual.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from test_hopfield import hebbian_K, corrupt_pattern, hamming_distance


def retrieve_with_per_bit_lock(query, K, depth=4, dt=0.05, steps=2000,
                                seed=42, init_noise=0.05):
    """Returns (retrieved, per_bit_lock, cos_avg).
    per_bit_lock[i] is |mean cos(φ_i across channels)| — confidence per bit.
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
    per_bit_lock = np.abs(cos_avg)
    return retrieved, per_bit_lock, cos_avg


def retrieve_with_locked_bits(query, K, locked_bits, locked_values,
                               depth=4, dt=0.05, steps=2000, seed=42,
                               init_noise=0.05):
    """
    Run oscillator with some bits LOCKED at fixed values.

    locked_bits: array of bit indices that are fixed.
    locked_values: ±1 values for those bits.

    Locked bits don't evolve; their phases stay at target (0 or π).
    Their K_ij couplings still influence neighbors as static biases.
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

    # Initial phases: locked bits at their locked values, free bits at query
    locked_set = set(locked_bits.tolist() if hasattr(locked_bits, 'tolist') else list(locked_bits))
    locked_map = dict(zip(
        locked_bits.tolist() if hasattr(locked_bits, 'tolist') else list(locked_bits),
        locked_values.tolist() if hasattr(locked_values, 'tolist') else list(locked_values)))

    target = np.zeros(N)
    for i in range(N):
        if i in locked_set:
            target[i] = 0.0 if locked_map[i] == 1 else np.pi
        else:
            target[i] = 0.0 if query[i] == 1 else np.pi

    phi = np.zeros((depth, N))
    for ch in range(depth):
        for i in range(N):
            phi[ch, i] = target[i] + rng.uniform(-init_noise, init_noise)

    # Mask: which bits are free to evolve
    free_mask = np.ones(N, dtype=bool)
    for i in locked_set:
        free_mask[i] = False

    for step in range(steps):
        for ch in range(depth):
            diffs = phi[ch, dst] - phi[ch, src]
            forces = kvals * np.sin(diffs)
            kur = np.zeros(N)
            np.add.at(kur, src, forces)
            # Only advance free bits
            phi[ch][free_mask] += dt * kur[free_mask]
            # Force locked bits back to their target (in case integration drift)
            for i in locked_set:
                phi[ch, i] = target[i]

    cos_avg = np.mean(np.cos(phi), axis=0)
    retrieved = np.sign(cos_avg).astype(int)
    retrieved[retrieved == 0] = 1
    # Force locked bits to their values in output
    for i, v in locked_map.items():
        retrieved[i] = v
    return retrieved, np.abs(cos_avg)


def two_round_closure(query, K, lock_threshold=0.5, seed=42):
    """
    Round 1: retrieve, see per-bit confidence.
    Round 2: lock high-confidence bits, re-solve uncertain bits with K|locked.
    """
    # Round 1
    r1, lock1, _ = retrieve_with_per_bit_lock(query, K, seed=seed)

    # Identify locked bits
    locked_bits = np.where(lock1 >= lock_threshold)[0]
    locked_values = r1[locked_bits]

    if len(locked_bits) == len(query):
        # Everything was confident, no round 2 needed
        return r1, r1, locked_bits, lock1

    # Round 2 with locked bits
    r2, _ = retrieve_with_locked_bits(query, K, locked_bits, locked_values,
                                        seed=seed + 1)
    return r2, r1, locked_bits, lock1


def evaluate(n_flips, k=3, N=32, n_trials=15, lock_threshold=0.5):
    rng_p = np.random.RandomState(99)
    patterns = np.array([rng_p.choice([-1, 1], N) for _ in range(k)])
    K = hebbian_K(patterns)

    results = {
        'r1_correct': 0,
        'r2_correct': 0,
        'r1_to_r2_improved': 0,  # r2 right, r1 wrong
        'r1_to_r2_worse': 0,     # r1 right, r2 wrong
        'avg_locked_pct': [],
        'avg_lock_quality_correct_bits': [],
        'avg_lock_quality_wrong_bits': [],
        'total': 0,
    }

    for p_idx, p in enumerate(patterns):
        for trial in range(n_trials // k):
            query_seed = trial * 31 + p_idx * 17 + n_flips
            rng_q = np.random.RandomState(query_seed)
            query = corrupt_pattern(p, n_flips, rng_q)

            r2, r1, locked_bits, lock1 = two_round_closure(
                query, K, lock_threshold=lock_threshold, seed=query_seed)

            r1_ok = (hamming_distance(r1, p) == 0)
            r2_ok = (hamming_distance(r2, p) == 0)
            results['r1_correct'] += r1_ok
            results['r2_correct'] += r2_ok
            if r2_ok and not r1_ok:
                results['r1_to_r2_improved'] += 1
            if r1_ok and not r2_ok:
                results['r1_to_r2_worse'] += 1
            results['avg_locked_pct'].append(len(locked_bits) / N)
            results['total'] += 1

            # Track: are locked bits actually correct?
            for i in locked_bits:
                if r1[i] == p[i]:
                    results['avg_lock_quality_correct_bits'].append(lock1[i])
                else:
                    results['avg_lock_quality_wrong_bits'].append(lock1[i])

    return results


def main():
    print("=" * 76)
    print("  Bit-level field closure — round 2 on uncertain bits only")
    print("=" * 76)
    print()
    print("  Round 1 retrieves and reports per-bit lock quality |cos(φ)|.")
    print("  Round 2 locks bits with lock_quality >= threshold, re-solves rest.")
    print()
    print(f"  Lock threshold: 0.5")
    print()

    print(f"  {'flips':>5}  {'%':>4}  "
          f"{'r1':>9}  {'r2':>9}  "
          f"{'r2>r1':>6}  {'r1>r2':>6}  "
          f"{'%locked':>8}  {'lock(correct bits)':>19}  {'lock(wrong bits)':>17}")

    for n_flips in [0, 4, 8, 10, 12, 14]:
        r = evaluate(n_flips)
        t = r['total']
        r1_pct = r['r1_correct'] / t
        r2_pct = r['r2_correct'] / t
        avg_locked = np.mean(r['avg_locked_pct'])
        lock_correct = np.mean(r['avg_lock_quality_correct_bits']) if r['avg_lock_quality_correct_bits'] else float('nan')
        lock_wrong = np.mean(r['avg_lock_quality_wrong_bits']) if r['avg_lock_quality_wrong_bits'] else float('nan')
        print(f"  {n_flips:>5}  {n_flips/32:>4.0%}  "
              f"{r['r1_correct']:>2d}/{t} ({r1_pct:>3.0%})  "
              f"{r['r2_correct']:>2d}/{t} ({r2_pct:>3.0%})  "
              f"{r['r1_to_r2_improved']:>6d}  {r['r1_to_r2_worse']:>6d}  "
              f"{avg_locked:>7.0%}  {lock_correct:>19.3f}  {lock_wrong:>17.3f}")

    print()
    print("  Reading:")
    print("    r2>r1 = cases where round 2 corrected round 1's mistake")
    print("    r1>r2 = cases where round 2 made round 1 worse (locked wrong bits)")
    print("    lock(correct bits)  = avg confidence of bits that R1 got RIGHT")
    print("    lock(wrong bits)    = avg confidence of bits that R1 got WRONG")
    print("    If lock(correct) >> lock(wrong), per-bit confidence is informative.")


if __name__ == "__main__":
    main()
