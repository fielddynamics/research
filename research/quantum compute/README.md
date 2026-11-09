# Quantum Compute

*Oscillator computing from the GFD framework · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`ising-model` `qubo` `oscillator-ising-machine` `kuramoto-model` `combinatorial-optimization` `d-wave` `t-bit`

---

This folder holds the computing side of GFD: networks of coupled oscillators, built on GFD's coupling and constitutive law, used to solve hard optimisation problems. Its main result is the oscillator Ising machine.

## The oscillator Ising machine

**[`oscillator ising machine/`](<oscillator ising machine/>)** turns the GFD oscillator into a solver for the problems D-Wave's quantum annealers solve: find spins $s_i = \pm 1$ that minimise

$$E(s) = \sum_i h_i s_i + \sum_{i<j} J_{ij} s_i s_j .$$

Max-Cut, graph colouring, scheduling, the travelling salesperson problem and many others can be written in this form.

- **It speaks D-Wave's format.** It accepts any Ising or QUBO problem as a D-Wave (dimod) model, fields included, and returns a D-Wave sample set. It drops into D-Wave's own problem library unchanged.
- **It is verified.** Twelve tests check the dynamics themselves: they are a gradient flow on the Ising energy, and each oscillator settles to a spin.
- **It is benchmarked the way D-Wave benchmarks**, against D-Wave's own classical solvers:

| | Original oscillator | Oscillator Ising machine | D-Wave simulated annealing |
|---|---|---|---|
| Small spin glasses with fields: runs reaching the ground state | 47% | 83% | 84% |
| 500-spin glasses: best run above the best known solution | +58 to +89 | +3 to +6 | 0 to +1.3 |
| Planted problems on D-Wave's chip graphs: runs reaching the ground state | 1–13% | 1–9% (21% tuned) | 62–71% |

On spin glasses it is competitive with D-Wave's classical solvers. On planted problems on D-Wave's own chip graphs it is not yet, and closing that gap is the next step. Everything runs in software; on analog or FPGA hardware, one run would take 160 times the network's coupling time constant, a projection not yet measured. The [folder's README](<oscillator ising machine/README.md>) has the details, and [`RESULTS.md`](<oscillator ising machine/RESULTS.md>) the full tables.

```bash
cd "oscillator ising machine"
pip install numpy scipy networkx dimod dwave-samplers dwave-networkx
python test_oscillator_ising.py     # 12/12
python benchmark.py                 # writes RESULTS.md, about 8 minutes
```

## Also in this folder

| Folder | Contents |
|---|---|
| [`graph solver/`](<graph solver/>) | The original GFD graph solver the Ising machine grew from: one oscillator, one SVD readout, applied to Max-Cut, colouring, TSP, community detection and mazes, with an ablation and classical baselines. Also holds the Walsh-Hadamard gate-bridge solver and the April 2026 syntheses |
| [`t-bit algebra/`](<t-bit algebra/>) | The tetrahedral bit (t-bit): a computation algebra built on GFD's constitutive law, in three parts (`tbit_algebra.md`, `tbit_network_algebra.md`, and `tb compute/tbit_compute_theory.md`), with verification scripts, the "tb compute" experiments, the cube-lattice compute node and the π-walk oscillator |
| [`oscillator history/`](<oscillator history/>) | Earlier versions of the oscillator: v1 (synthesis of confirmed findings), v2 (the first universal graph solver), and Oscillator learning (Hopfield memory, Walsh recovery and learning experiments) |

## Layout

```
quantum compute/
├── README.md                    this page
├── oscillator ising machine/    the D-Wave-class solver
├── graph solver/                the original graph solver, gate bridge and syntheses
├── t-bit algebra/               t-bit theory, verification and experiments
└── oscillator history/          GFD oscillator v1, v2 and Oscillator learning
```

## Known issue

The three t-bit verification scripts (`tbit_verify.py`, `tbit_network_verify.py`, `tbit_extended_verify.py`) import a module named `gfd_algebra__2_`, the name of an uploaded copy of [`research/gfd_algebra.py`](../gfd_algebra.py). That module is not in the repository, so the scripts do not run as committed. This predates the reorganisation.

---

*Stephen Nelson, Field Dynamics Research*
