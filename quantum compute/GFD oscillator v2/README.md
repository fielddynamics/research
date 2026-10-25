# GFD Universal Graph Solver

**One oscillator. One coupling. Five NP-hard problems.**

A universal computation engine based on the Gravity Field Dynamics framework.
The same equation — `K·sin(φⱼ − φᵢ)` — solves Max-Cut, graph coloring, TSP,
community detection, and shortest path through self-regulating depth adaptation.

## Quick Start

```bash
python3 run_all.py
```

## Architecture

The GFD oscillator carries two independent channels per graph node:

| Channel | Equation | Coupling | Solves |
|---------|----------|----------|--------|
| **Amplitude** | `dμ/dt = x·(1−μ)² − μ` | Ferromagnetic | Flow / shortest path |
| **Phase** | `dφ/dt = ω + K·Σ sin(φⱼ−φᵢ)` | Problem-dependent | Partition / ordering / clustering |

Both run simultaneously in one ODE (`tetra_joint_rhs`).

## Problems Solved

| Problem | Class | Active Modes | Depth | Verified |
|---------|-------|-------------|-------|----------|
| **Maze** | Flow (P) | 1 | 1 | 20/20 optimal at 250K nodes |
| **Max-Cut** | Partition (NP) | 2 | 4 | 20/20 optimal, 18% margin at N=5000 |
| **3-Coloring** | Partition (NP) | 2 | 4 | 20/20 valid |
| **TSP** | Ordering (NP) | ~N | 8 | 12/12 optimal at N=7–10 |
| **Community Detection** | Clustering (NP) | k | 4–8 | 15/15 perfect (NMI=1.000) |

## Key Discovery: SVD Spectrum = Problem Class

After the oscillator converges, the SVD of the cos(φ) matrix reveals the problem class:

```
Max-Cut:    * * . . . . . .   → 2 active modes (partition)
3-Coloring: * * . . . . . .   → 2 active modes (partition)
TSP:        * * * * * * . .   → 6 active modes (ordering)
Community:  varies with k     → k active modes (clustering)
```

The spectrum width tells you what kind of problem you solved. The last singular value
is the **depth gauge** — it reports whether the current nesting depth is sufficient.

## Self-Regulating Depth

The `{1,3,3,1}` grade structure at each nesting level provides:

- **3 modes** that carry the answer
- **1 mode** that reports the confidence (depth gauge)

When the gauge saturates (S_last >> 0), the solver doubles the depth:

```
depth 4  → S₃ large  → "Need more resolution"
depth 8  → S₇ ≈ 0    → "Resolved"
```

No external oracle. The oscillator tells you how deep to go.

## File Structure

```
gfd_solver/
├── gfd_oscillator.py      Core engine (GFDOscillator class)
├── solve_maze.py           Shortest path — amplitude channel
├── solve_maxcut.py         Max-Cut — phase channel, 2-partition
├── solve_coloring.py       k-Coloring — phase channel, mode pairs
├── solve_tsp.py            TSP — phase channel, ordering
├── solve_community.py      Community detection — modularity matrix
├── run_all.py              Run all benchmarks
└── README.md               This file
```

## Graph Encoding

Each problem maps to a graph with per-edge coupling:

| Problem | Graph | Coupling K_ij |
|---------|-------|---------------|
| Max-Cut | Adjacency | −2 (uniform anti-ferro) |
| Coloring | Adjacency | −2 (same as Max-Cut) |
| TSP | Complete | −0.5 + 0.3·proximity (distance-weighted) |
| Community | Modularity | B_ij = A_ij − k_i·k_j/2m (signed) |
| Maze | Adjacency | Amplitude channel, not phase |

## Readout by Problem Class

| Problem | Readout depth | Method |
|---------|--------------|--------|
| Max-Cut | 1 mode | `sign(v₀)` → 2 groups |
| k-Coloring | 2 modes | `atan2(vᵦ, vₐ)` → k angular sectors |
| TSP | N modes | `argsort(vₖ)` → tour order |
| Community | k modes | k-means on mode coordinates |
| Maze | 1 amplitude | Dijkstra on μ field |

## Hardware Path

On an FPGA (Kria KR260 or similar):
- Each node = one phase-locked loop
- Coupling = wire between adjacent cells
- The Kuramoto update is one `sin()` + one accumulate per edge per clock
- At 200 MHz: 1M-node Max-Cut in ~10 microseconds

The GPU simulation proves correctness. The value proposition is analog hardware speed.

## Reference

Stephen Nelson, Field Dynamics Research  
https://docs.fielddynamics.org

## License

MIT (code) / CC BY 4.0 (documentation)
