#!/usr/bin/env python3
"""
GFD Universal Solver — Run All Benchmarks
==========================================

One oscillator. One coupling. One readout. Five problems.

The readout is always the same: weighted SVD coordinates of the
converged state. The coordinates ARE the answer. What differs is
the coordinate GEOMETRY — and the geometry is determined by the
coupling matrix, not by the readout technique.

    Flow:       coordinates form a gradient → follow it
    Partition:  coordinates form clusters   → sign/angle
    Ordering:   coordinates form a sequence → sort
    Clustering: coordinates form groups     → proximity

These are not different readouts. They are different coordinate
geometries produced by different coupling matrices, all read
by the same SVD decomposition.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_section(title, fn):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    t0 = time.time()
    fn()
    print(f"  Time: {time.time() - t0:.1f}s")


def test_maze():
    from solve_maze import solve_maze
    wins = sum(solve_maze(16, 16, seed=s * 7 + 13)[2] for s in range(10))
    print(f"  Maze 16×16: {wins}/10 OPTIMAL")


def test_maxcut():
    from solve_maxcut import solve_maxcut, brute_force_maxcut, random_graph
    opt = 0
    total = 0
    for trial in range(15):
        nn = 12 + (trial % 4)
        edges = random_graph(nn, 0.25, trial * 7 + 3)
        if len(edges) < 3:
            continue
        osc = solve_maxcut(nn, edges, restarts=10, seed=trial)
        exact = brute_force_maxcut(nn, edges)
        total += 1
        opt += (osc == exact)
    print(f"  Max-Cut: {opt}/{total} OPTIMAL")


def test_coloring():
    from solve_coloring import solve_coloring, make_k_colorable
    valid = 0
    total = 0
    for trial in range(15):
        edges, _ = make_k_colorable(20, k=3, density=0.25, seed=trial * 13)
        if len(edges) < 5:
            continue
        conflicts, _ = solve_coloring(20, edges, k=3, restarts=5, seed=trial)
        total += 1
        valid += (conflicts == 0)
    print(f"  3-Coloring: {valid}/{total} VALID")


def test_tsp():
    from solve_tsp import solve_tsp, make_tsp, brute_force_tsp
    opt = 0
    total = 0
    for trial in range(8):
        nn = 7 + (trial % 3)
        _, dist = make_tsp(nn, seed=trial * 7)
        osc = solve_tsp(dist, restarts=8, depth=8, seed=trial)
        exact = brute_force_tsp(dist)
        total += 1
        opt += (abs(osc / exact - 1) < 0.002)
    print(f"  TSP: {opt}/{total} OPTIMAL")


def test_community():
    from solve_community import (solve_communities, make_communities,
                                  normalized_mutual_info)
    perfect = 0
    total = 0
    for trial in range(12):
        k = 2 + (trial % 3)
        n, edges, true_labels = make_communities(10, k, 0.5, 0.02, trial * 7)
        pred = solve_communities(n, edges, k, restarts=5, seed=trial)
        score = normalized_mutual_info(true_labels, pred)
        total += 1
        perfect += (score > 0.95)
    print(f"  Community Detection: {perfect}/{total} PERFECT")


if __name__ == "__main__":
    print("=" * 60)
    print("  GFD UNIVERSAL SOLVER")
    print("  One oscillator. One readout. Five problems.")
    print("=" * 60)
    print()
    print("  The oscillator produces coordinates.")
    print("  The coordinates ARE the answer.")
    print("  Sign, angle, sort, gradient — these are the")
    print("  coordinate geometry, not the readout technique.")

    run_section("MAZE — Coordinate Gradient (Flow)", test_maze)
    run_section("MAX-CUT — Coordinate Sign (Partition)", test_maxcut)
    run_section("3-COLORING — Coordinate Angle (Partition)", test_coloring)
    run_section("TSP — Coordinate Sort (Ordering)", test_tsp)
    run_section("COMMUNITY — Coordinate Proximity (Clustering)", test_community)

    print("\n" + "=" * 60)
    print("  UNIVERSAL READOUT: SVD coordinates of converged state")
    print("=" * 60)
    print()
    print("  Problem       Coupling K        Coord Geometry   Class")
    print("  ───────────── ──────────────── ────────────────  ──────────")
    print("  Maze          attractive (amp) gradient (1D)     Flow")
    print("  Max-Cut       −2·A             sign (1D)         Partition")
    print("  3-Coloring    −2·A             angle (2D)        Partition")
    print("  TSP           dist-weighted    spread (ND)       Ordering")
    print("  Community     B = A−kk'/2m     clusters (kD)     Clustering")
    print()
    print("  Spectrum width = class signature:")
    print("    1 active mode:  flow")
    print("    2 active modes: partition")
    print("    N active modes: ordering")
    print("    k active modes: k-clustering")
    print()
    print("  Depth gauge = resolution:")
    print("    S_last ≈ 0: resolved at current depth")
    print("    S_last > 0: need more nesting")
    print("=" * 60)
