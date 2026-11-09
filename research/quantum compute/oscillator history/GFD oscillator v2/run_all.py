#!/usr/bin/env python3
"""
GFD Universal Solver — Run All Benchmarks
==========================================

Runs all five problem solvers and reports results.
One oscillator. One coupling. Five NP-hard problems.

Usage: python3 run_all.py
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
    print(f"\n  Time: {time.time() - t0:.1f}s")


def test_maze():
    from solve_maze import solve_maze
    optimal = 0
    total = 10
    for trial in range(total):
        _, _, is_opt = solve_maze(16, 16, seed=trial * 7 + 13)
        optimal += is_opt
    print(f"  Maze 16×16: {optimal}/{total} OPTIMAL")


def test_maxcut():
    from solve_maxcut import solve_maxcut, brute_force_maxcut, random_graph
    optimal = 0
    total = 0
    for trial in range(15):
        nn = 12 + (trial % 4)
        edges = random_graph(nn, 0.25, trial * 7 + 3)
        if len(edges) < 3:
            continue
        osc = solve_maxcut(nn, edges, restarts=10, seed=trial)
        exact = brute_force_maxcut(nn, edges)
        total += 1
        optimal += (osc == exact)
    print(f"  Max-Cut: {optimal}/{total} OPTIMAL")


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
    optimal = 0
    total = 0
    for trial in range(8):
        nn = 7 + (trial % 3)
        _, dist = make_tsp(nn, seed=trial * 7)
        opt = brute_force_tsp(dist)
        osc = solve_tsp(dist, restarts=8, depth=8, seed=trial)
        total += 1
        optimal += (abs(osc / opt - 1) < 0.002)
    print(f"  TSP: {optimal}/{total} OPTIMAL")


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
    print("  GFD UNIVERSAL SOLVER — FULL BENCHMARK")
    print("  One oscillator. One coupling. Five problems.")
    print("  dphi/dt = omega + K * sum sin(phi_j - phi_i)")
    print("=" * 60)

    run_section("MAZE (Amplitude Channel — Flow)", test_maze)
    run_section("MAX-CUT (Phase Channel — 2-Partition)", test_maxcut)
    run_section("3-COLORING (Phase Channel — 3-Partition)", test_coloring)
    run_section("TSP (Phase Channel — Ordering)", test_tsp)
    run_section("COMMUNITY DETECTION (Modularity — Clustering)", test_community)

    print("\n" + "=" * 60)
    print("  COMPLETE")
    print("=" * 60)
    print()
    print("  Problem         Channel    Class       Readout")
    print("  ─────────────── ────────── ─────────── ──────────────")
    print("  Maze            Amplitude  Flow        Dijkstra on μ")
    print("  Max-Cut         Phase      Partition   sign(v₀)")
    print("  3-Coloring      Phase      Partition   angle(vₐ,vᵦ)")
    print("  TSP             Phase      Ordering    sort(vₖ)")
    print("  Community Det.  Phase      Clustering  modularity(B)")
    print()
    print("  SVD spectrum width IS the problem class signature.")
    print("  Depth gauge (S_last) IS the resolution indicator.")
    print("  One equation: K · sin(φⱼ − φᵢ)")
    print("=" * 60)
