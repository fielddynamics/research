# TASKS — remaining engineering items

This task list reflects the state after two enhancement passes.

Items marked [DONE] were completed; [PASS 2] were completed in the
most recent pass; [OPEN] remain for future work.


## Cross-file

### Completed

1. [DONE] Consolidated `walsh_bridge`, `truth_table`, `character`,
   `evaluate_bridge`, `reshape_4x4`, `grade_energy`, `grade_decomposition`
   into `bridge.py`. All test files import from it.
2. [DONE] Added AND and OR composition rules (`bridge_and`, `bridge_or`)
   to `bridge.py`, verified to machine precision.
3. [DONE] Added `README.md` as folder entry point.
4. [DONE] Self-tests on every Python module.
5. [DONE] Fixed `run_oscillator` to compute mean-of-cosines.
6. [PASS 2] Added `gate_library.py` — precomputed bridges for all 16
   two-input functions, 11 three-input gates, 11 four-input gates.
7. [PASS 2] Added `composite_inversion_test.py` — preimage enumeration
   for composite functions; verifies composition algebra is
   preimage-preserving.
8. [PASS 2] Added complexity/runtime table to synthesis (Section 13).
9. [PASS 2] Added canonical gate library section to synthesis (Section 14).
10. [PASS 2] Discovered and documented the identity
    `B[0] = (n_1 - n_0) / 2^n` (preimage count from constant cell).
11. [PASS 2] Updated `gfd_oscillator.py` docstring to note the general
    {1, C(n,1), ..., C(n,n)} grade structure alongside the Cl(3,0)
    minimal SO.

### Open

12. [OPEN] Add `__init__.py` to make this a proper Python package.
13. [OPEN] Add `requirements.txt` or `pyproject.toml`.
14. [OPEN] Generate visualizations: 4x4 bridge heatmaps for a reference
    set of gates.
15. [OPEN] Add a version tag (`__version__` in `bridge.py`).


## bridge.py

### Open

1. [OPEN] `walsh_bridge` is O(N²). Add FWHT-based O(N log N) version
   for n >= 8. Measured impact: at n=8, 60 ms drops to <1 ms.
2. [OPEN] `walsh_conv` is also O(N²). Same FWHT speedup applies.
3. [OPEN] Add `bridge_not(B) = -B` for API completeness.
4. [OPEN] Add `bridge_compose_via_circuit(circuit, bridges_of_gates)` —
   given a small DAG of gates, compose bridges to get the whole
   circuit's bridge. Reference implementation for circuit analysis.


## gate_library.py  [NEW in Pass 2]

### Open

1. [OPEN] Add n=5 and n=6 common gates (threshold, carry, add-with-carry).
2. [OPEN] Pickle the library to disk to avoid rebuilding on import.
3. [OPEN] Programmatic search: "find all gates with bridge matching
   pattern P" (for reverse lookup from learned bridges).


## GATE_BRIDGE_SYNTHESIS.md

### Completed

1. [DONE] Section 4 rewritten with universal grade structure.
2. [DONE] Section 7 has exact AND and OR composition rules.
3. [DONE] Section 10 corrections updated.
4. [PASS 2] Section 13 — complexity/runtime table with measured numbers.
5. [PASS 2] Section 14 — canonical gate library reference.

### Open

6. [OPEN] Section 1 worked-example derivation of the AND bridge
   `[-0.5, 0.5, 0.5, 0.5]` by hand (makes the formula concrete).
7. [OPEN] Section 3 "anti-ferromagnetic Kuramoto" language — tighten
   to "signed Kuramoto with K = +B (x) B, mixed ferro/antiferro per
   edge by sign of product."
8. [OPEN] Section 5 gauge density — tabulate the 14-gate data for
   reproducibility.
9. [OPEN] Section 8 bent function claim should cite Rothaus 1976.
10. [OPEN] Add a B[0] = preimage-count identity as its own micro-section.
11. [OPEN] Consolidate "when it fails" checklist across sections 6,7,8,9,10.


## gfd_oscillator.py

### Completed

1. [PASS 2] Docstring updated with general grade structure note.

### Open (for Stephen)

2. [OPEN] Add optional `phi_init` to `run_phase` for warm starts.
3. [OPEN] Expose omega as a parameter (currently hardcoded 1.0).
4. [OPEN] `run_adaptive`: let user specify starting depth and doubling.
5. [OPEN] Warn when Sv[0] is near zero (degenerate dynamics).


## gate_signature_tests.py

### Completed

1. [DONE] Shared imports from `bridge.py`.
2. [DONE] `_self_test()` with invariant checks.
3. [DONE] Modernized numpy RNG.
4. [DONE] Mean-of-cosines with error bars.
5. [DONE] Docstring clarifications.

### Open

6. [OPEN] Expand GATES dict using `gate_library.lookup` — centralizes
   gate definitions rather than redefining `gate_xor4`, etc.
7. [OPEN] Add type hints to function signatures.
8. [OPEN] Plot-generating routine for bridge heatmaps.


## extended_composition_tests.py

### Completed

1. [DONE] Header comment updated to reflect verified composition rules.
2. [DONE] `run_oscillator` computes mean-of-cosines.
3. [DONE] TEST A checks all three rules (XOR, AND, OR) plus cross-checks.
4. [DONE] Shared imports from `bridge.py`.
5. [DONE] Error bars in TEST B and TEST C.

### Open

6. [OPEN] Deterministic tie-breaking for TEST D's top-grade argmax.
7. [OPEN] TEST E noise study currently tests ONE function. Parametrize
   across grade-2/3/4 representatives.
8. [OPEN] CI-friendly main that returns status code.


## composite_inversion_test.py  [NEW in Pass 2]

### Open

1. [OPEN] Implement METHOD 2 (oscillator-based input recovery) — the
   file sketches the approach but doesn't build it. This requires a
   different graph encoding where input bits are nodes and characters
   are coupling structures. Open design question.
2. [OPEN] Extend to n=5, n=6 to study how preimage structure scales.
3. [OPEN] Connect to SAT: a CNF formula is a conjunction of disjunctions;
   each clause is a Boolean function; the whole formula has a bridge
   (via AND composition), and preimage-of-1 IS the set of satisfying
   assignments. Test this connection on small 3-SAT instances.


## Priority items for next pass

If time permits only ONE more pass, do these three:

1. **Implement FWHT for bridge.py** (bridge.py open #1 and #2).
   This is the single biggest speedup — moves the framework from
   "works at n=4-8" to "works at n=16-20", which is where real
   problems start.

2. **Implement oscillator-based input recovery** (composite_inversion
   open #1). This is the natural next oscillator experiment: given
   bridge + target output, can Kuramoto dynamics find a valid preimage?
   Open design question with clear success criteria (preimage recovered
   correctly = 1, otherwise 0).

3. **Connect to 3-SAT** (composite_inversion open #3). A 3-SAT formula
   with m clauses at n variables has a bridge computed by AND-composing
   the clause bridges. Preimage of 1 = satisfying assignments. This
   puts the framework in direct contact with a canonical NP-complete
   benchmark.
