# Current verification guide — Stage IX

Fresh runs from this edition of the reorganized folder (NumPy, SciPy, SymPy, Matplotlib). Every historical mathematical verifier exited successfully. The first aggregate command timed out during Stage VII; Stage VII was then run separately to completion. All final logs are retained, including exit status in `rerun_logs/status.txt`.

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
