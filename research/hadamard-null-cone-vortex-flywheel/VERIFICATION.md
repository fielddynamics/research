# Verification guide — complete research record

Historical Stage IX reruns from the reorganized folder (NumPy, SciPy, SymPy, Matplotlib). Every historical mathematical verifier exited successfully. The first aggregate command timed out during Stage VII; Stage VII was then run separately to completion. All final logs are retained, including exit status in `rerun_logs/status.txt`.

| Stage | Script | New checks in that stage (freshly rerun) |
|---|---|---:|
| I | `archive/stages-I-VI/verify_hadamard_null_cone.py` | 501 |
| II | `archive/stages-I-VI/verify_current_closure.py` | 483 |
| III | `archive/stages-I-VI/verify_extended_validation.py` | 211 |
| IV | `archive/stages-I-VI/verify_core_hardening.py` | 170 |
| V | `archive/stages-I-VI/verify_face_core_stability.py` | 132 |
| VI | `archive/stages-I-VI/verify_triforce_flywheel.py` | 271 |
| VII | `verify_sustained_flywheel.py` | 809 |
| VIII | `verify_open_throat.py` | 160 |
| IX | `verify_coupled_origins.py` | 115 |
| Total | | 2,852 |

These are assertion counts, not independent theorems; imported checks may run more than once but are counted only in their originating stage. The archive's historical Stage VII snapshot is not a separate stage. No Lean compilation or full browser regression testing was performed. The new explorer visualizes the computed CSV, not a new simulation.

The following historical runner executes Stages I–IX only. For the five subsequent verification commands see the extension sections below or the [current README](README.md#reproduce-the-results).

```sh
python -m pip install numpy scipy sympy matplotlib
python run_all_verifiers.py
```

Stage IX log: [coupled_origins_verification_output.txt](coupled_origins_verification_output.txt). Historical logs: `rerun_logs/`. Existing verification reports remain available for comparison.


## Whole-field four-port extension

`python verify_four_port_packing.py` — 348/348 new checks, [output](four_port_verification_output.txt). Prior 2,852 checks preserved, not rerun in this edition. The total recorded checks are 3,200; not independent theorems.

## Corner-first contact bound

`python verify_corner_first.py`: 43/43 fresh exact algebraic checks. The 3,200 prior recorded assertions are preserved, not rerun. Total recorded assertions: 3,243. The general cap bound is proved analytically, not by enumeration alone.

## Hadamard–Flower lattice

`python verify_hadamard_flower.py`: 314/314 fresh checks, [log](hadamard_flower_verification_output.txt). Prior 3,243 recorded assertions retained but not rerun. Total recorded assertions 3,557. Exact rational projection, lattice enumeration, Voronoi vertices and Triforce overlap areas; conditional 8-amplitude numerical interface checks. JavaScript syntax and mocked canvas execution checked; no full browser rendering regression or Lean compilation.


## Unified Hadamard–Flower field dynamics

`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_unified_flower.py`: 316/316 fresh assertions; [log](unified_flower_verification_output.txt). Reuses the geometry/H definition prefix of Stage IX without running the historical test body. Tests exact port partition, symmetry, overlap spectrum and leading origin transfer, original diamond-net relation, connected 54-node periodic lattice and numerical current continuity, norm and energy at 401 times. Prior 3,557 recorded checks preserved, not rerun; cumulative 3,873 recorded checks. No new Lean or browser regression.


## Optical four-port resonator

`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_optical_ports.py`: 108/108 fresh assertions; [log](optical_ports_verification_output.txt). Exact projector ranks, permutation covariance, 36 integer Hamiltonian moments on the common dark kernel, central Schur split, 641-frequency unitary reciprocal optical comparison, and two 16-field conservative network runs at 321 time samples. Previous 3,873 recorded assertions retained, not rerun; cumulative 3,981. Assertion counts are not independent theorems. No Lean compilation.


## Field Origin gravity read

`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_field_read.py` — 130/130 fresh checks, [log](field_read_verification_output.txt). Prior 3,981 preserved, not rerun; total 4,111 recorded assertions. Static potential is a separate conditional model, not a microscopic derivation.

## Spectral gravity read

`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_spectral_read.py`: 194/194 new assertions; [log](spectral_read_verification_output.txt). Prior 4,111 recorded assertions preserved, not rerun. Total 4,305. Checks include exact identities tested numerically, Bloch eigensystems, curvature and inverse response, and a conditional spherical work model. No global band-minimum proof.

## Matter vortex and signed charge

`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_matter_charge.py` — 157/157 new assertions; [log](matter_charge_verification_output.txt). Complete Walsh algebra, original 36-coordinate Hamiltonian charge obstruction, local energy minima and conservative numerical perturbations, neutral TetA circulation at reduced equilibria, all 24 tetrahedral symmetry checks, dressed exchange conservation, static 432-node diamond Gauss problem and kernel comparison. No full microscopic particle/capture simulation, empirical validation or Lean compilation. Prior 4,305 preserved, not rerun; total 4,462 recorded assertions.
