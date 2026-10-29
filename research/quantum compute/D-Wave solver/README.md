# GFD Universal Graph Solver

**One oscillator. One readout. Five NP-hard problems.**

`kuramoto-model` `phase-oscillators` `combinatorial-optimization` `np-hard` `max-cut` `graph-coloring` `ising-model` `qubo`

The oscillator produces coordinates. The coordinates ARE the answer.

## The Core Idea

The GFD oscillator probes the eigenstructure of a coupling matrix K via
Kuramoto dynamics. The converged state — expressed as weighted SVD
coordinates — encodes the solution. On analog hardware, you measure the
voltages. On a digital computer, SVD extracts the same information.

There is one readout: **the weighted SVD coordinates of the converged state.**

What differs between problems is the **coordinate geometry** — and the
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

Both run simultaneously. The amplitude channel solves flow problems.
The phase channel solves partition, ordering, and clustering problems.

## Self-Regulation

The SVD spectrum encodes two things:

**Problem class** (spectrum width):
- 1 active mode = flow
- 2 active modes = partition
- N active modes = ordering

**Resolution quality** (depth gauge = S_last/S₀):
- Gauge ≈ 0: fully resolved
- Gauge >> 0: need more depth (nesting)

The oscillator tells you what class of problem it solved AND whether
the answer is trustworthy — through the same SVD decomposition that
produces the coordinates.

## Results

| Problem | Coupling | Verified |
|---------|----------|----------|
| Maze (250K nodes) | Ferromagnetic (amplitude) | 20/20 optimal |
| Max-Cut (N≤5000) | −2·Adjacency | 20/20 optimal, 18% vs greedy |
| 3-Coloring | −2·Adjacency | 20/20 valid |
| TSP (N≤10) | Distance-weighted | 12/12 optimal |
| Community | Modularity B_ij | 15/15 perfect |

## Quick Start

```bash
python3 run_all.py
```

## Files

```
gfd_solver/
├── gfd_oscillator.py      Core engine + universal readout
├── solve_maze.py           Flow — coordinate gradient
├── solve_maxcut.py         Partition — coordinate sign
├── solve_coloring.py       Partition — coordinate angle
├── solve_tsp.py            Ordering — coordinate sort
├── solve_community.py      Clustering — coordinate proximity
├── run_all.py              Full benchmark
└── README.md               This file
```

## Reference

Stephen Nelson, Field Dynamics Research
https://docs.fielddynamics.org

MIT (code) / CC BY 4.0 (documentation)
