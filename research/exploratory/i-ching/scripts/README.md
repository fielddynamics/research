# Original scripts

The verification scripts and analysis engines from the original notes in [`../notes/`](../notes/). The first three need only `mpmath`; run them from this folder.

| Script | What it does |
|---|---|
| `closure_walk_proof_iching.py` | π in base 8 from mpmath and from the three-axis (BBP) mechanism, matched digit for digit; the walk closes at step 332 |
| `why_pi_verification.py` | the six constraints, and the term-by-term identity with the BBP series |
| `run_all_validations_with_i-ching-intact.py` | Paper IX's validation suite with its I Ching section intact (46 checks) |
| `verify_hexagram_closure_read.py` | the hexagrams and the closure read: R = ω on corresponding lines, 21 = 1 + 4 + 16 and 7 + 14, the TIME rotation's 23, the shared Walsh read, the flywheel core, and the π walk tested against R (26 checks; needs `numpy` and `mpmath`) |
| `verify_prime_two.py` | the coupling polynomial at the prime two: det(K·I − Cₙ), the Eisenstein and Gaussian norms, the reductions mod 2 and mod 4, the swap conjugate to the Sierpiński generator, GL(2,2) and its orbits on the hexagrams (28 checks; needs `sympy`) |
| `finite_field_reciprocity/` | the field tower GF(4) ⊂ GF(16), GF(64) ⊂ GF(4096) built in `finite_geometry.py`; six test files for the six finite-field notes, 258 tests in all: `test_iching_bridge.py`, `test_reciprocal_tower.py`, `test_shared_zone.py`, `test_shared_zone_rotation.py`, `test_walsh_reciprocal_action.py` and `test_common_mode_proof.py`. Four `make_*_figures.py` scripts regenerate nine of the ten diagrams; `canonical_common_mode.svg` is static. Run with `python -m pytest` (needs `requirements.txt`) |
| `traversal_analyzer.py`, `tetragram_analyzer.py` | the walk's step ledger and its 32 sub-channels; copies of the modules in the model repository's `engine_core/common/`, where they run |

The tests behind the write-up are in the model repository's [`bbp_structure/`](https://github.com/fielddynamics/dfp-gravity-field-model/tree/test/bbp-octahedron-hypothesis/gravity_field_model/engine_core/field_closure/bbp_structure).
