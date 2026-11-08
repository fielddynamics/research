# Original scripts

The verification scripts and analysis engines from the original notes in [`../notes/`](../notes/). The first three need only `mpmath`; run them from this folder.

| Script | What it does |
|---|---|
| `closure_walk_proof_iching.py` | π in base 8 from mpmath and from the three-axis (BBP) mechanism, matched digit for digit; the walk closes at step 332 |
| `why_pi_verification.py` | the six constraints, and the term-by-term identity with the BBP series |
| `run_all_validations_with_i-ching-intact.py` | Paper IX's validation suite with its I Ching section intact (46 checks) |
| `traversal_analyzer.py`, `tetragram_analyzer.py` | the walk's step ledger and its 32 sub-channels; copies of the modules in the model repository's `engine_core/common/`, where they run |

The tests behind the write-up are in the model repository's [`bbp_structure/`](https://github.com/fielddynamics/dfp-gravity-field-model/tree/test/bbp-octahedron-hypothesis/gravity_field_model/engine_core/field_closure/bbp_structure).
