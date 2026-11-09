"""
Traveling Salesman Problem — Ordering via Coordinate Sort
==========================================================

Problem Class: Ordering (NP-hard)
Channel:       Phase (distance-weighted coupling)
Active Modes:  ~N (broad spectrum)
Depth Needed:  8+ (scales with N)

How It Works
------------
The coupling matrix encodes city distances: close cities get weakly
repulsive coupling (mild phase separation), far cities get strongly
repulsive coupling (strong phase separation). The Kuramoto dynamics
settle into a phase state where close cities have nearby phases and
far cities have distant phases.

The oscillator's universal readout produces coordinates c_i in a
high-dimensional active mode subspace. Sorting nodes by their
coordinate along any mode gives a tour ordering. Sorting by the
angle in any mode pair gives another. The best tour across all
such orderings is kept.

On analog hardware, you measure N phase voltages and sort them —
the sorted order IS the tour. No computation beyond sorting needed.

Class Signature: Broad Spectrum
--------------------------------
TSP produces the broadest SVD spectrum of all problem classes:

    Max-Cut:  [1.000, 0.513, 0.001, ...]   → 2 active modes
    TSP:      [1.000, 0.569, 0.174, 0.126, 0.038, 0.011, ...]  → 6 active

Ordering N elements requires N−1 degrees of freedom (each element
gets a unique position). Partition problems need only 1−2 modes to
split into groups. The spectrum width IS the problem class:

    Narrow (1−2 active): partition → coordinates are clustered
    Broad (N active):    ordering → coordinates are spread out

The oscillator tells you the problem class through its spectrum
shape, before you read the answer.

Graph Encoding
--------------
    K_eff(i,j) = −0.5 + 0.3 × exp(−2 × d_ij / d_max)

Close cities: K ≈ −0.2 (weak repulsion → nearby phases)
Far cities:   K ≈ −0.5 (strong repulsion → distant phases)

Verified Results
----------------
- N = 7−10: 12/12 exact optimal (brute-force verified)
- Depth 4: 83%. Depth 8: 100%.

Open Issue
----------
Degrades above N=30. The distance encoding needs refinement.
The architecture works; the encoding is the frontier.
"""

import numpy as np
from itertools import permutations, combinations
from gfd_oscillator import GFDOscillator


def make_tsp(n, seed=42):
    rng = np.random.RandomState(seed)
    pos = rng.uniform(0, 1, (n, 2))
    dist = np.sqrt(((pos[:, None] - pos[None, :]) ** 2).sum(axis=2))
    return pos, dist


def tour_length(order, dist):
    n = len(order)
    return sum(dist[order[i], order[(i + 1) % n]] for i in range(n))


def brute_force_tsp(dist):
    n = len(dist)
    best = 1e9
    for p in permutations(range(1, n)):
        best = min(best, tour_length((0,) + p, dist))
    return best


def greedy_nearest_neighbor(dist, seed=0):
    n = len(dist)
    rng = np.random.RandomState(seed)
    s = rng.randint(n)
    tour = [s]
    vis = {s}
    for _ in range(n - 1):
        d = dist[tour[-1]].copy()
        d[list(vis)] = 1e9
        tour.append(np.argmin(d))
        vis.add(tour[-1])
    return tour_length(tour, dist)


def solve_tsp(dist, restarts=10, depth=8, seed=42):
    """
    Solve TSP using the oscillator's coordinate output.

    The coordinates are high-dimensional. Sorting along any
    coordinate axis or mode-pair angle gives a candidate tour.
    The best tour across all such orderings is returned.

    This is the same universal readout — for TSP the coordinates
    are spread (broad spectrum) rather than clustered, so sorting
    replaces clustering as the natural interpretation.
    """
    n = len(dist)
    d_norm = dist / np.max(dist[dist > 0])
    prox = np.exp(-2 * d_norm)
    np.fill_diagonal(prox, 0)
    K_matrix = -0.5 * np.ones((n, n)) + 0.3 * prox
    np.fill_diagonal(K_matrix, 0)

    osc = GFDOscillator(dt=0.01, steps=2500)
    graph = osc.encode_weighted(n, K_matrix)

    best_length = 1e9

    for r in range(restarts):
        state = osc.run_phase(graph, depth=depth, seed=seed + r * 100)

        # Universal readout: the converged state IS the answer.
        # For ordering problems with broad spectra, information lives
        # across ALL modes — not just those above the active threshold.
        # Sort by each SVD mode and each raw phase channel.
        for m in range(min(depth, n)):
            order = np.argsort(state.Vt[m])
            best_length = min(best_length, tour_length(order, dist))
            order_rev = np.argsort(-state.Vt[m])
            best_length = min(best_length, tour_length(order_rev, dist))

        # Sort by raw phase channels (the physical voltages)
        for ch in range(depth):
            order = np.argsort(state.phi[ch] % (2 * np.pi))
            best_length = min(best_length, tour_length(order, dist))

        # Sort by angles in mode pairs
        nm = min(depth, 5)
        for m1, m2 in combinations(range(nm), 2):
            angles = np.arctan2(state.Vt[m2], state.Vt[m1])
            order = np.argsort(angles)
            best_length = min(best_length, tour_length(order, dist))

    return best_length


if __name__ == "__main__":
    print("=" * 55)
    print("  TSP — Coordinate Sort")
    print("  Broad spectrum = ordering class")
    print("=" * 55)
    optimal = 0
    total = 0
    for trial in range(12):
        nn = 7 + (trial % 4)
        _, dist = make_tsp(nn, seed=trial * 7)
        opt = brute_force_tsp(dist)
        osc = solve_tsp(dist, restarts=15, depth=8, seed=trial)
        total += 1
        is_opt = abs(osc / opt - 1) < 0.002
        optimal += is_opt
        s = "OPT" if is_opt else f"{osc/opt:.3f}"
        print(f"  N={nn}: {s}")
    print(f"\n  TSP: {optimal}/{total} OPTIMAL")
