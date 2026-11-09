"""
test_hopfield_iterate.py
==========================

Hypothesis: when single-shot retrieval lands in a wrong basin, feeding
the result back as a new query lets a second round of dynamics finish
the correction.

Three variants tested:
  1. Iterate-on-state: r_{k+1} = osc(r_k, K)
  2. Iterate-with-K-update: r_{k+1} = osc(query, K + α·r_k·r_kᵀ)
  3. Voting closure across multiple seeds, threshold uncertain bits

All compared to single-shot baseline at the high-corruption regime
where single-shot gets ~33%.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
from test_hopfield import (hebbian_K, corrupt_pattern, hamming_distance,
                            retrieve, retrieve_kuramoto)


# ---------------------------------------------------------------
def iterate_on_state(query, K, n_rounds=5, **osc_kwargs):
    """Variant 1: re-run oscillator with previous output as new query."""
    current = query.copy()
    history = [current]
    for round_idx in range(n_rounds):
        retrieved, _ = retrieve_kuramoto(current, K, **osc_kwargs)
        history.append(retrieved)
        if np.array_equal(retrieved, current):
            break  # fixed point
        current = retrieved
    return current, history


def iterate_with_K_update(query, K, n_rounds=5, alpha=0.1, **osc_kwargs):
    """Variant 2: each round adds the retrieved pattern's outer product to K."""
    K_current = K.copy()
    N = len(query)
    history = []
    for round_idx in range(n_rounds):
        retrieved, _ = retrieve_kuramoto(query, K_current, **osc_kwargs)
        history.append(retrieved)
        # Add the retrieved pattern as evidence (with decay)
        outer = np.outer(retrieved, retrieved) / N
        np.fill_diagonal(outer, 0)
        K_current = K_current + alpha * outer
        if len(history) >= 2 and np.array_equal(history[-1], history[-2]):
            break
    return history[-1], history


def voting_closure(query, K, n_seeds=5, **osc_kwargs):
    """Variant 3: run multiple seeds, vote per bit, lock high-confidence bits.

    For bits where votes are unanimous, lock them.  For uncertain bits,
    average across seeds and threshold.
    """
    N = len(query)
    retrievals = []
    for s in range(n_seeds):
        kwargs = dict(osc_kwargs)
        kwargs['seed'] = osc_kwargs.get('seed', 42) + s * 137
        r, _ = retrieve_kuramoto(query, K, **kwargs)
        retrievals.append(r)
    arr = np.array(retrievals)
    # Per-bit majority
    summed = np.sum(arr, axis=0)
    voted = np.sign(summed).astype(int)
    voted[voted == 0] = 1
    return voted, retrievals


def hybrid_iterate_then_vote(query, K, n_rounds=3, n_seeds=3, **osc_kwargs):
    """First iterate-on-state, then vote across seeds in the final round."""
    # First: iterate on state until stable
    current = query.copy()
    for _ in range(n_rounds):
        retrieved, _ = retrieve_kuramoto(current, K, **osc_kwargs)
        if np.array_equal(retrieved, current):
            break
        current = retrieved
    # Then: vote across seeds with the (hopefully closer) current
    voted, _ = voting_closure(current, K, n_seeds=n_seeds, **osc_kwargs)
    return voted


# ---------------------------------------------------------------
def evaluate_method(method_name, method_fn, n_flips, k=3, N=32, n_trials=15):
    rng_p = np.random.RandomState(99)
    patterns = np.array([rng_p.choice([-1, 1], N) for _ in range(k)])
    K = hebbian_K(patterns)

    n_succ = 0
    n_total = 0
    n_improved = 0  # cases where iteration improved over single-shot

    for p_idx, p in enumerate(patterns):
        for trial in range(n_trials // k):
            query_seed = trial * 31 + p_idx * 17 + n_flips
            rng_q = np.random.RandomState(query_seed)
            query = corrupt_pattern(p, n_flips, rng_q)

            # Single-shot baseline
            r0, _ = retrieve_kuramoto(query, K, seed=query_seed)
            single_ok = (hamming_distance(r0, p) == 0)

            # Method
            r_method = method_fn(query, K, seed=query_seed)
            if isinstance(r_method, tuple):
                r_method = r_method[0]
            method_ok = (hamming_distance(r_method, p) == 0)

            n_succ += method_ok
            n_total += 1
            if method_ok and not single_ok:
                n_improved += 1

    return n_succ, n_total, n_improved


def main():
    print("=" * 76)
    print("  Hopfield iterate-then-vote — does another round of field closure help?")
    print("=" * 76)
    print()
    print("  Setup: 3 patterns, N=32, vary corruption.")
    print("  Compare single-shot vs 4 closure strategies.")
    print()

    methods = [
        ("single-shot", lambda q, K, seed: retrieve_kuramoto(q, K, seed=seed)[0]),
        ("iterate(state)", lambda q, K, seed: iterate_on_state(q, K, n_rounds=5, seed=seed)[0]),
        ("iterate(K)", lambda q, K, seed: iterate_with_K_update(q, K, n_rounds=5, alpha=0.3, seed=seed)[0]),
        ("vote(5 seeds)", lambda q, K, seed: voting_closure(q, K, n_seeds=5, seed=seed)[0]),
        ("iter+vote", lambda q, K, seed: hybrid_iterate_then_vote(q, K, n_rounds=3, n_seeds=5, seed=seed)),
    ]

    print(f"  {'flips':>5} {'%':>4}  ", end="")
    for name, _ in methods:
        print(f"{name:>14}  ", end="")
    print("improved")

    for n_flips in [0, 4, 8, 10, 12, 14]:
        print(f"  {n_flips:>5} {n_flips/32:>4.0%}  ", end="")
        single_succ = None
        for name, fn in methods:
            n_succ, n_total, n_improved = evaluate_method(name, fn, n_flips)
            pct = n_succ / n_total
            print(f"{n_succ}/{n_total} ({pct:>3.0%})    ", end="")
            if name == "single-shot":
                single_succ = n_succ
        print()


if __name__ == "__main__":
    main()
