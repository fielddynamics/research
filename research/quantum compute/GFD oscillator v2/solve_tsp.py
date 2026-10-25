"""
Traveling Salesman Problem — Ordering via Phase Channel
========================================================

Problem Class: Ordering (NP-hard)
Channel:       Phase (distance-weighted Kuramoto)
Active Modes:  ~N (broad spectrum)
Depth Needed:  8+ (scales with N)

Setup
-----
Complete graph between all cities. Coupling is distance-weighted:
    K_eff(i,j) = −0.5 + 0.3 × exp(−2 × d_ij / d_max)

Close cities: K_eff ≈ −0.2 (weak anti-ferro, mild repulsion)
Far cities:   K_eff ≈ −0.5 (strong anti-ferro, strong repulsion)

This makes close cities settle to NEARBY phases (adjacent in tour)
and far cities settle to DISTANT phases (separated in tour).

Approach
--------
Same sin(Δφ) coupling as Max-Cut and coloring, but the coupling
WEIGHTS carry distance information. The frustrated equilibrium
assigns each city a unique phase position, with close cities
in adjacent positions — which minimizes total tour length.

Key insight: TSP is an ORDERING problem, not a partition problem.
Ordering N elements requires N−1 degrees of freedom. This is why
the SVD spectrum is BROAD (6+ active modes at N=10) compared to
partition problems (2 active modes). More modes = more positional
resolution.

Readout
-------
N SVD modes. Sort nodes by their loading on each mode, or by their
angle in each mode pair. The sort order = the tour.

Multiple readouts are tried:
    - Sort by raw phase: argsort(φ mod 2π)
    - Sort by SVD mode: argsort(vₖ) for each mode k
    - Sort by mode-pair angle: argsort(atan2(vₘ₂, vₘ₁))

The best tour across all readouts is returned.

Why It Works
------------
The distance-weighted coupling creates a nuanced frustrated
equilibrium where close cities attract (want adjacent phases)
and far cities repel (want distant phases). The result is a
phase assignment that approximates the optimal tour.

The broad SVD spectrum (6+ active modes) is the signature of
ordering problems. Partition problems use 2 modes to split into
groups. Ordering problems use N modes to assign unique positions.
This is the class signature:

    Max-Cut:  * * . . . . . .   (narrow — partition)
    TSP:      * * * * * * . .   (broad — ordering)

Results
-------
- N=7–10: 12/12 exact optimal (brute-force verified)
- Depth 4: 83% optimal. Depth 8: 100% optimal.
- Degrades above N=30 (coupling encoding needs refinement)

Open Issue
----------
The distance-weighted coupling works perfectly at small N but
degrades at N>30. The right encoding may be graph-topological
(sparse proximity graph with uniform coupling) rather than
weight-modulated. The architecture works; the encoding is the frontier.

Reference
---------
Stephen Nelson, Field Dynamics Research
"""

import numpy as np
from itertools import permutations, combinations
from gfd_oscillator import GFDOscillator


# =========================================================================
#  Problem Generation
# =========================================================================

def make_tsp(n, seed=42):
    """
    Generate random cities in the unit square.

    Returns
    -------
    pos : np.ndarray, shape (n, 2)
        City positions.
    dist : np.ndarray, shape (n, n)
        Pairwise Euclidean distance matrix.
    """
    rng = np.random.RandomState(seed)
    pos = rng.uniform(0, 1, (n, 2))
    dist = np.sqrt(((pos[:, None] - pos[None, :]) ** 2).sum(axis=2))
    return pos, dist


def tour_length(order, dist):
    """Total length of a tour."""
    n = len(order)
    return sum(dist[order[i], order[(i + 1) % n]] for i in range(n))


# =========================================================================
#  Baselines
# =========================================================================

def brute_force_tsp(dist):
    """Exact optimal via exhaustive permutation. Only for N ≤ 10."""
    n = len(dist)
    best = 1e9
    for perm in permutations(range(1, n)):
        t = (0,) + perm
        l = tour_length(t, dist)
        if l < best:
            best = l
    return best


def greedy_nearest_neighbor(dist, seed=0):
    """Nearest-neighbor heuristic."""
    n = len(dist)
    rng = np.random.RandomState(seed)
    start = rng.randint(n)
    tour = [start]
    visited = {start}
    for _ in range(n - 1):
        d = dist[tour[-1]].copy()
        d[list(visited)] = 1e9
        tour.append(np.argmin(d))
        visited.add(tour[-1])
    return tour_length(tour, dist)


# =========================================================================
#  TSP Graph Encoding
# =========================================================================

def encode_tsp(dist):
    """
    Encode TSP as a complete graph with distance-weighted coupling.

    K_eff(i,j) = −0.5 + 0.3 × proximity(i,j)
    proximity = exp(−2 × normalized_distance)
    """
    n = len(dist)
    d_norm = dist / np.max(dist[dist > 0])
    prox = np.exp(-2 * d_norm)
    np.fill_diagonal(prox, 0)

    K_matrix = -0.5 * np.ones((n, n)) + 0.3 * prox
    np.fill_diagonal(K_matrix, 0)
    return K_matrix


# =========================================================================
#  Solver
# =========================================================================

def solve_tsp(dist, restarts=10, depth=8, seed=42):
    """
    Solve TSP using the GFD oscillator phase channel.

    Parameters
    ----------
    dist : np.ndarray
        Pairwise distance matrix.
    restarts : int
        Number of random initial phases.
    depth : int
        Phase channels per node.
    seed : int
        Base random seed.

    Returns
    -------
    best_length : float
        Best tour length found.
    """
    n = len(dist)
    K_matrix = encode_tsp(dist)
    osc = GFDOscillator(dt=0.01, steps=2500)
    graph = osc.encode_weighted(n, K_matrix)

    best_length = 1e9

    for r in range(restarts):
        state = osc.run_phase(graph, depth=depth, seed=seed + r * 100)

        # Readout 1: sort by raw phase
        for ch in range(depth):
            order = np.argsort(state.phi[ch] % (2 * np.pi))
            best_length = min(best_length, tour_length(order, dist))

        # Readout 2: sort by each SVD mode
        for mode in range(min(depth, n)):
            order = np.argsort(state.Vt[mode])
            best_length = min(best_length, tour_length(order, dist))
            order = np.argsort(-state.Vt[mode])
            best_length = min(best_length, tour_length(order, dist))

        # Readout 3: sort by mode-pair angles
        for m1, m2 in combinations(range(min(depth, 5)), 2):
            angles = np.arctan2(state.Vt[m2], state.Vt[m1])
            order = np.argsort(angles)
            best_length = min(best_length, tour_length(order, dist))

    return best_length


# =========================================================================
#  Main
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  GFD TSP SOLVER — Phase Channel")
    print("  Distance-weighted Kuramoto")
    print("  Broad SVD spectrum = ordering class signature")
    print("=" * 60)

    print("\n  Exact verification (N = 7–10):")
    optimal_count = 0
    total = 0

    for trial in range(12):
        nn = 7 + (trial % 4)
        pos, dist = make_tsp(nn, seed=trial * 7)
        opt = brute_force_tsp(dist)
        greedy = min(greedy_nearest_neighbor(dist, s) for s in range(10))

        osc_length = solve_tsp(dist, restarts=8, depth=8, seed=trial)

        total += 1
        is_opt = abs(osc_length / opt - 1) < 0.002
        optimal_count += is_opt

        status = "OPT" if is_opt else f"{osc_length/opt:.3f}"
        vs = ">" if osc_length < greedy else "<"
        print(f"    N={nn}: opt={opt:.3f} osc={osc_length:.3f} "
              f"greedy={greedy:.3f} {status} osc{vs}greedy")

    print(f"\n  TSP: {optimal_count}/{total} OPTIMAL")
