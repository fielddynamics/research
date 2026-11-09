# GFD Universal Graph Solver

**One oscillator. One readout. Five graph problems.**

`kuramoto-model` `phase-oscillators` `combinatorial-optimization` `max-cut` `graph-coloring` `community-detection`

> **For D-Wave-class problems, use the [oscillator Ising machine](<../oscillator ising machine/>).** It builds on this solver's coupling, accepts any Ising or QUBO problem in D-Wave's own format, and is benchmarked against D-Wave's classical solvers. This folder is the original graph solver it grew from.

The oscillator produces coordinates. The coordinates are the answer.

## The Core Idea

The GFD oscillator probes the eigenstructure of a coupling matrix K via
Kuramoto dynamics. The converged state, expressed as weighted SVD
coordinates, encodes the solution. On analog hardware, you would measure the
voltages. On a digital computer, SVD extracts the same information.

There is one readout: **the weighted SVD coordinates of the converged state.**

What differs between problems is the **coordinate geometry**, and the
geometry is determined by the coupling matrix, not by the readout:

| Geometry | Meaning | Problems |
|----------|---------|----------|
| Gradient (1D) | Follow the potential | Maze |
| Bimodal (1D) | Threshold at zero | Max-Cut |
| Angular (2D) | Sectors on a circle | k-Coloring |
| Spread (ND) | Sort by position | TSP |
| Clustered (kD) | Group by proximity | Community detection |

## Architecture

Two channels, one ODE:

```
Amplitude:  dμ/dt = x·(1−μ)² − μ         (constitutive law)
Phase:      dφ/dt = ω + Σ K_ij·sin(φⱼ−φᵢ)  (Kuramoto)
```

The amplitude channel is used for the maze. The phase channel is used for
partition, ordering and clustering problems.

## Self-Regulation

As described in [`SYNTHESIS.md`](SYNTHESIS.md), the SVD spectrum encodes two things:

**Problem class** (spectrum width): 1 active mode = flow, 2 = partition, N = ordering.

**Resolution quality** (depth gauge = S_last/S₀): near 0 means resolved; well above 0 means more depth is needed.

These are reported findings; the benchmarks below do not test them.

## Results

`run_all.py` reproduces the following. Two companion scripts make each figure checkable:

- `ablation.py` runs the same benchmark with the oscillator's dynamics switched off, so the readout sees only random starting phases;
- `baselines.py` runs a standard classical method on the same instances.

| Problem | Instances | Oscillator | Dynamics off | Standard method on the same instances |
|---|---|---|---|---|
| Max-Cut | 15 graphs, 12–15 nodes | 15/15 optimal | 0/15 | 15/15, single-flip local search (0.5 s) |
| 3-Colouring | 15 graphs, 20 nodes | 15/15 valid | 0/15 | 15/15, DSATUR + min-conflicts (0.01 s) |
| TSP | 8 tours, 7–9 cities | 8/8 optimal | 0/8 | 8/8, nearest neighbour + 2-opt (0.2 s) |
| Community | 12 graphs, 20–40 nodes | 11/12 perfect | 0/12 | 10/12, spectral modularity (0.2 s) |
| Maze | 10 mazes, 16 × 16 | 10/10 optimal | 7/10 | 10/10, Dijkstra on a flat field (0.02 s) |

What this shows:

- **The oscillator does the work on four of the five problems.** With the dynamics off, Max-Cut, colouring, TSP and community detection all drop to zero.
- **On these sizes, standard methods match it, in less time.** The oscillator takes 0.4–20 s per problem set. On community detection it is slightly ahead of spectral modularity.
- **The maze test does not isolate the oscillator.** The path is found by Dijkstra's algorithm on the oscillator's field, and a flat field gives the same 10/10.
- **On larger Max-Cut graphs (100–260 nodes)** the oscillator beat single-flip local search with the same number of restarts by about 1%, but not when local search was given the same time.

Earlier versions of this README reported mazes of 250,000 nodes and Max-Cut up to 5,000 nodes with an 18% margin over greedy. `run_all.py` does not run those sizes. The greedy baseline used for the Max-Cut margin is a single pass that counts not-yet-placed nodes as being in group 0, so the margin overstates the oscillator's advantage. The [oscillator Ising machine](<../oscillator ising machine/>) has the current large-scale benchmark.

## Quick Start

```bash
python3 run_all.py      # the benchmark
python3 ablation.py     # the same benchmark with the dynamics switched off
python3 baselines.py    # standard methods on the same instances
```

## Files

```
graph solver/
├── gfd_oscillator.py           Core engine + universal readout
├── solve_maze.py               Flow: coordinate gradient
├── solve_maxcut.py             Partition: coordinate sign
├── solve_coloring.py           Partition: coordinate angle
├── solve_tsp.py                Ordering: coordinate sort
├── solve_community.py          Clustering: coordinate proximity
├── run_all.py                  Full benchmark
├── ablation.py                 Benchmark with the dynamics switched off
├── baselines.py                Standard methods on the same instances
├── SYNTHESIS.md                Theory and reported findings (April 2026)
├── documentation/              Eigenspectrum, Clifford and oscillator syntheses
└── circuit gate bridge solver/ Boolean gate recognition via Walsh-Hadamard bridges
```

## Reference

Stephen Nelson, Field Dynamics Research
https://docs.fielddynamics.org

MIT (code) / CC BY 4.0 (documentation)
