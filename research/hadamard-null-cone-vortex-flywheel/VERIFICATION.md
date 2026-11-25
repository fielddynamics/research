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
