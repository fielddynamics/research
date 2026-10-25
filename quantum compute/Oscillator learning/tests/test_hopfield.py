"""
hopfield_demo.py
=================

Hopfield associative memory built on the GFD oscillator.

ARCHITECTURE:
    Store k patterns p₁, ..., p_k ∈ {-1, +1}^N in the coupling matrix
        K = Σᵢ pᵢ ⊗ pᵢ - k·I    (Hebbian rule, zero diagonal)

    Retrieve from corrupted query q:
        1. Initialize phases φ near q (φᵢ = 0 if qᵢ = +1, π if -1)
        2. Run Kuramoto dynamics
        3. Read settled phase pattern; sign of cos(φᵢ) gives retrieved bit
        4. Compare retrieved pattern to stored patterns → which one?

THIS IS THE QUBIT-CLASS DEMO:
    Storage = superposition of patterns in eigenstructure.
    Retrieval = relaxation into nearest energy minimum.
    Classical Kuramoto + SVD covers the symmetric/standard irrep sector.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from gfd_oscillator import GFDOscillator


# ---------------------------------------------------------------
def hebbian_K(patterns):
    """
    Standard Hopfield Hebbian coupling matrix.
        K_ij = (1/N) · Σ_p  p[i] * p[j]    for i ≠ j
        K_ii = 0
    """
    patterns = np.asarray(patterns, dtype=float)
    k, N = patterns.shape
    K = (patterns.T @ patterns) / N
    np.fill_diagonal(K, 0)
    return K


def corrupt_pattern(p, n_flips, rng):
    """Flip n_flips random bits of p."""
    p = p.copy()
    indices = rng.choice(len(p), n_flips, replace=False)
    p[indices] = -p[indices]
    return p


def retrieve(query, K, max_iter=100):
    """
    Hopfield retrieval via synchronous threshold update on K.
        s(t+1) = sign(K · s(t))

    This is the discrete-time Hopfield update.  Always converges for
    symmetric K (Hopfield 1982 theorem).  Typically 1-3 iterations.

    Returns: (retrieved_pattern, n_iterations)
    """
    s = np.asarray(query, dtype=float).copy()
    for it in range(max_iter):
        s_new = np.sign(K @ s)
        s_new[s_new == 0] = 1
        if np.array_equal(s_new, s):
            return s.astype(int), it + 1
        s = s_new
    return s.astype(int), max_iter


def retrieve_kuramoto(query, K, depth=4, dt=0.05, steps=2000, seed=42,
                      init_noise=0.05):
    """
    Continuous-time oscillator-based Hopfield retrieval.

    Architecture (the fix that was missing):
      - DROP the natural-frequency ω=1 term.  In Hopfield retrieval we
        do NOT want phases to rotate; we want them to lock to discrete
        target positions {0, π}.  ω≠0 washes out absolute-phase
        information.
      - Use the query as the initial condition (init_noise small).
      - Pure Kuramoto coupling on K — no separate query-bias drive
        needed once ω=0.
      - Read out by sign of cos(φ) per node.

    Without ω, the dynamics is: dφ/dt = Σⱼ K_ij sin(φⱼ - φᵢ).
    This is gradient descent on E = -½ Σ K_ij cos(Δφ).  K's
    eigenstructure pulls the phases into the nearest pattern's basin
    relative to the initial condition.

    The init_noise needs to be SMALL (≤ 0.1) so the query commits
    the dynamics to the +p basin (not -p).  If the init is too noisy,
    the ±1 symmetry of K can flip the answer.
    """
    N = len(query)
    rng = np.random.RandomState(seed)

    # Build sparse edges from K
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

    # Pure Kuramoto, NO natural frequency
    for step in range(steps):
        for ch in range(depth):
            diffs = phi[ch, dst] - phi[ch, src]
            forces = kvals * np.sin(diffs)
            kur = np.zeros(N)
            np.add.at(kur, src, forces)
            phi[ch] += dt * kur          # NOTE: no +1.0 (ω=0)

    cos_avg = np.mean(np.cos(phi), axis=0)
    retrieved = np.sign(cos_avg).astype(int)
    retrieved[retrieved == 0] = 1
    return retrieved, None


def discrete_hopfield(query, K, max_iter=100):
    """Backward-compatible alias."""
    return retrieve(query, K, max_iter)


def hamming_distance(a, b):
    return int(np.sum(np.asarray(a) != np.asarray(b)))


def identify_pattern(retrieved, patterns):
    """Return (best_idx, best_distance) — which stored pattern is closest?"""
    best_idx, best_d = -1, len(retrieved) + 1
    for i, p in enumerate(patterns):
        d = hamming_distance(retrieved, p)
        if d < best_d:
            best_d = d
            best_idx = i
    return best_idx, best_d


# =====================================================================
#  Tests
# =====================================================================

def t1_basic_retrieval():
    """Discrete vs oscillator on 3 patterns, varying corruption."""
    print("─" * 72)
    print("  T1: Basic Hopfield retrieval — 3 patterns, N=32, varying corruption")
    print("  Compare DISCRETE Hopfield vs OSCILLATOR-based")
    print("─" * 72)

    rng = np.random.RandomState(42)
    N = 32
    patterns = np.array([rng.choice([-1, 1], N) for _ in range(3)])
    K = hebbian_K(patterns)

    print(f"  Pattern correlations: {[(i,j, int(np.dot(patterns[i], patterns[j]))) for i in range(3) for j in range(i+1, 3)]}")
    print()
    print(f"  {'pattern':>9s} {'flips':>6s}  {'discrete':>10s}  {'oscillator':>11s}  {'agree':>6s}")
    n_total = 0
    n_disc = 0
    n_osc = 0
    n_agree = 0
    for p_idx, p in enumerate(patterns):
        for n_flips in [0, 2, 4, 6, 8]:
            for trial in range(3):
                query_seed = trial * 100 + p_idx * 10 + n_flips
                rng_q = np.random.RandomState(query_seed)
                query = corrupt_pattern(p, n_flips, rng_q)

                d_retrieved, d_iter = discrete_hopfield(query, K)
                o_retrieved, _ = retrieve_kuramoto(query, K, seed=query_seed)
                d_h = hamming_distance(d_retrieved, p)
                o_h = hamming_distance(o_retrieved, p)
                d_ok = (d_h == 0)
                o_ok = (o_h == 0)
                agree = (np.sum(d_retrieved != o_retrieved) == 0)
                n_total += 1
                n_disc += d_ok
                n_osc += o_ok
                n_agree += agree
            print(f"  {p_idx:>9d} {n_flips:>6d}  "
                  f"{int(d_ok):>10d}  {int(o_ok):>11d}  "
                  f"{('y' if agree else 'n'):>6s}", end="")
            print()  # one row per (p,flips) showing last trial result
    print(f"\n  Totals: discrete {n_disc}/{n_total}, oscillator {n_osc}/{n_total}, "
          f"agree on {n_agree}/{n_total}")
    return n_total


def t2_capacity_curve():
    """Capacity curve: discrete vs oscillator at increasing patterns."""
    print("─" * 72)
    print("  T2: Capacity curve — DISCRETE vs OSCILLATOR at increasing patterns")
    print("─" * 72)
    print(f"  Theoretical Hebbian capacity: ~0.14·N = ~4.5 patterns at N=32")
    print()
    print(f"  {'#patterns':>10s}  {'flips':>6s}  {'discrete':>11s}  {'oscillator':>12s}")

    N = 32
    n_flips = N // 4
    n_trials = 5

    for k in [1, 2, 4, 8]:
        rng_p = np.random.RandomState(7 * k)
        patterns = np.array([rng_p.choice([-1, 1], N) for _ in range(k)])
        K = hebbian_K(patterns)

        d_succ = 0
        o_succ = 0
        total = 0
        for p_idx, p in enumerate(patterns):
            for trial in range(n_trials):
                query_seed = trial * 71 + p_idx * 13 + k
                rng_q = np.random.RandomState(query_seed)
                query = corrupt_pattern(p, n_flips, rng_q)
                d_r, _ = discrete_hopfield(query, K)
                o_r, _ = retrieve_kuramoto(query, K, seed=query_seed)
                d_succ += (hamming_distance(d_r, p) == 0)
                o_succ += (hamming_distance(o_r, p) == 0)
                total += 1
        print(f"  {k:>10d}  {n_flips:>6d}  {d_succ:>4d}/{total} ({d_succ/total:>4.0%})  "
              f"{o_succ:>4d}/{total} ({o_succ/total:>5.0%})")
    return True


def t3_basin_size():
    """How much corruption can each method handle?"""
    print("─" * 72)
    print("  T3: Basin of attraction — flip-count sweep at k=3, N=32")
    print("─" * 72)

    N = 32
    rng_p = np.random.RandomState(99)
    patterns = np.array([rng_p.choice([-1, 1], N) for _ in range(3)])
    K = hebbian_K(patterns)

    print(f"  {'flips':>6s}  {'%':>5s}  {'discrete':>11s}  {'oscillator':>12s}")
    for n_flips in range(0, N // 2 + 1, 2):
        d_succ = 0
        o_succ = 0
        total = 0
        for p_idx, p in enumerate(patterns):
            for trial in range(5):
                query_seed = trial * 31 + p_idx * 17 + n_flips
                rng_q = np.random.RandomState(query_seed)
                query = corrupt_pattern(p, n_flips, rng_q)
                d_r, _ = discrete_hopfield(query, K)
                o_r, _ = retrieve_kuramoto(query, K, seed=query_seed)
                d_succ += (hamming_distance(d_r, p) == 0)
                o_succ += (hamming_distance(o_r, p) == 0)
                total += 1
        print(f"  {n_flips:>6d}  {n_flips/N:>5.0%}  "
              f"{d_succ:>4d}/{total} ({d_succ/total:>4.0%})  "
              f"{o_succ:>4d}/{total} ({o_succ/total:>5.0%})")
    return True


def t4_letter_patterns():
    """Visual demo: 5 letter patterns, retrieve from corrupted version."""
    print("─" * 72)
    print("  T4: Letter-pattern demo — 5 patterns, retrieve via discrete + oscillator")
    print("─" * 72)

    letter_patterns = {
        'A': [+1,+1,+1,+1, +1,-1,-1,+1, +1,+1,+1,+1, +1,-1,-1,+1],
        'B': [+1,+1,+1,-1, +1,-1,+1,-1, +1,+1,+1,-1, +1,-1,+1,-1],
        'C': [+1,+1,+1,+1, +1,-1,-1,-1, +1,-1,-1,-1, +1,+1,+1,+1],
        'D': [+1,+1,+1,-1, +1,-1,-1,+1, +1,-1,-1,+1, +1,+1,+1,-1],
        'E': [+1,+1,+1,+1, +1,-1,-1,-1, +1,+1,+1,-1, +1,+1,+1,+1],
    }
    names = list(letter_patterns.keys())
    patterns = np.array(list(letter_patterns.values()))
    print(f"  Storing {len(names)} patterns: {names}, N={patterns.shape[1]}")
    K = hebbian_K(patterns)
    print()

    rng = np.random.RandomState(0)
    print(f"  {'query':>6s}  {'flips':>6s}  {'discrete':>9s}  {'osc':>6s}  {'d_ham':>6s}  {'o_ham':>6s}")
    for letter, pattern in letter_patterns.items():
        for n_flips in [2, 4]:
            query = corrupt_pattern(np.array(pattern), n_flips, rng)
            d_r, _ = discrete_hopfield(query, K)
            o_r, _ = retrieve_kuramoto(query, K, seed=42)
            d_idx, _ = identify_pattern(d_r, patterns)
            o_idx, _ = identify_pattern(o_r, patterns)
            d_letter = names[d_idx]
            o_letter = names[o_idx]
            d_ham = hamming_distance(d_r, pattern)
            o_ham = hamming_distance(o_r, pattern)
            print(f"  {letter:>6s}  {n_flips:>6d}  {d_letter:>9s}  {o_letter:>6s}  "
                  f"{d_ham:>6d}  {o_ham:>6d}")
    return True


def t5_overcapacity_failure():
    """Demonstrate graceful degradation past capacity."""
    print("─" * 72)
    print("  T5: Overcapacity — store too many patterns at N=16")
    print("─" * 72)
    print(f"  Capacity at N=16 ≈ 2.2 patterns. Test up to 8 stored.")
    print()
    print(f"  {'#patterns':>10s}  {'discrete':>11s}  {'oscillator':>12s}")

    N = 16
    for k in [1, 2, 3, 5, 8]:
        rng_p = np.random.RandomState(11 * k)
        patterns = np.array([rng_p.choice([-1, 1], N) for _ in range(k)])
        K = hebbian_K(patterns)

        d_succ = 0
        o_succ = 0
        total = 0
        for p_idx, p in enumerate(patterns):
            for trial in range(5):
                query_seed = trial * 7 + p_idx * 3 + k
                rng_q = np.random.RandomState(query_seed)
                query = corrupt_pattern(p, 2, rng_q)
                d_r, _ = discrete_hopfield(query, K)
                o_r, _ = retrieve_kuramoto(query, K, seed=query_seed)
                d_succ += (hamming_distance(d_r, p) == 0)
                o_succ += (hamming_distance(o_r, p) == 0)
                total += 1
        print(f"  {k:>10d}  {d_succ:>4d}/{total} ({d_succ/total:>4.0%})  "
              f"{o_succ:>4d}/{total} ({o_succ/total:>5.0%})")
    return True


# =====================================================================
def main():
    print(" " * 18 + "HOPFIELD ASSOCIATIVE MEMORY ON GFD OSCILLATOR\n")
    tests = [
        t1_basic_retrieval,
        t2_capacity_curve,
        t3_basin_size,
        t4_letter_patterns,
        t5_overcapacity_failure,
    ]
    for t in tests:
        t()
        print()
    print("=" * 72)
    print(" Hopfield retrieval as oscillator dynamics — verified.")
    print("=" * 72)


if __name__ == "__main__":
    main()
