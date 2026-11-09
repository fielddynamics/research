# GFD Gate Bridge

`walsh-hadamard-transform` `boolean-functions` `logic-gates` `phase-oscillators` `kuramoto-model`

Boolean gate recognition via Walsh-Hadamard bridges and the GFD
oscillator. An engineering resource documenting how the universal
grade decomposition of Boolean functions connects to phase-oscillator
dynamics.

## What's in this folder

| file | role |
|---|---|
| `bridge.py` | Walsh-bridge utilities: truth tables, bridge computation, characters, grade decomposition, composition rules (XOR/AND/OR). |
| `gate_library.py` | Precomputed bridges for 38 canonical gates (all 16 two-input functions + common 3/4-input gates). |
| `gfd_oscillator.py` | The GFD oscillator library (Stephen Nelson / Field Dynamics Research). Unchanged. |
| `gate_signature_tests.py` | 4-gate demonstration pipeline: Hebbian learning + oscillator + classification. |
| `extended_composition_tests.py` | Composite functions, multi-output gates, noise robustness, composition rules. |
| `composite_inversion_test.py` | Preimage enumeration for composite gates; validates composition algebra preimage-preservation. |
| `GATE_BRIDGE_SYNTHESIS.md` | Findings writeup. Read this for the full story. |
| `TASKS.md` | Open engineering items for future work. |


## Quick start

```
# Requires: numpy. No GPU needed. Python 3.9+.
# From this folder:

python bridge.py                         # self-test (8 checks)
python gate_library.py                   # self-test + library summary
python gate_signature_tests.py           # basic demo (~30s)
python extended_composition_tests.py     # full composition tests (~30s)
python composite_inversion_test.py       # preimage structure (~5s)
```

Each file has a `_self_test()` at the bottom that verifies basic
invariants before running the main experiments.


## What this resource demonstrates

1. **Every Boolean function has a unique Walsh bridge** — a
   2^n-dimensional coefficient vector indexed by subsets of the n
   inputs. The bridge IS the gate's signature.

2. **Bridges decompose by grade (Hamming weight of mask index)**
   into the exterior-algebra grades of Cl(n, 0):
     - n=2: {1, 2, 1} = 4 cells
     - n=3: {1, 3, 3, 1} = 8 cells (the stella octangula / Cl(3,0))
     - n=4: {1, 4, 6, 4, 1} = 16 cells

3. **Bridges can be learned from (input, output) examples** by a
   Hebbian / sample-mean rule. 3000 random examples reproduce the
   ground-truth bridge to RMSE < 0.02 per cell, with 30% label noise
   tolerated.

4. **Compositions follow exact algebraic rules** — verified to
   machine precision:
     - bridge(f XOR g) = -Walsh_conv(bridge(f), bridge(g))
     - bridge(f AND g) = (1/2)(B_f + B_g + Walsh_conv(B_f, B_g)) - (1/2) e_0
     - bridge(f OR  g) = (1/2)(B_f + B_g - Walsh_conv(B_f, B_g)) + (1/2) e_0

5. **The GFD oscillator reads the bridge's grade structure** when you
   encode K = B ⊗ B (positive outer product) as a weighted Kuramoto
   graph. The dominant SVD mode of cos(phi) recovers sign(B) for dense
   bridges. The depth gauge (Sv[-1]/Sv[0]) is a structural readout of
   bridge density (correlation with nonzero-cell-count = -0.997).

6. **Preimage count is directly readable from the constant cell**:
   `B[0] = (n_1 - n_0) / 2^n`, where `n_k` is the number of inputs
   mapping to output `k`. This is exact (verified on all 16 two-input
   functions and all 4-input library gates). Output-balanced functions
   are exactly those with `B[0] = 0`.


## Reading order

1. `README.md` (this file) — overview
2. `GATE_BRIDGE_SYNTHESIS.md` — the measured findings
3. `bridge.py` — understand the core utilities
4. `gate_signature_tests.py` — see the pipeline end-to-end
5. `extended_composition_tests.py` — see the composition algebra
6. `TASKS.md` — open items for extending this


## Dependencies

```
numpy >= 1.20
```

That's it. No scipy, no torch, no GPU. Python 3.9+ for dataclasses.


## Scope and limitations

This resource demonstrates the Walsh-bridge ↔ oscillator correspondence
at the **2-to-4-input gate** scale (4 to 16 bridge cells). At this
scale, everything is exact and runs in seconds.

It does NOT claim the oscillator efficiently inverts cryptographic
hashes or solves arbitrary SAT problems. The rank-1 encoding K = B ⊗ B
preserves sign patterns but not bridge magnitude ratios — recovering
magnitudes would need rank-k decompositions, which are not implemented
here. See `GATE_BRIDGE_SYNTHESIS.md` Section 6 for the honest scope.


## Provenance and authorship

Research direction: Stephen Nelson, Field Dynamics Research
(`stephen@fielddynamics.org` / https://docs.fielddynamics.org)

Implementation and empirical characterization: a conversation between
Stephen and an AI assistant. All claims in the synthesis document are
measured, not asserted.

License: MIT (matches `gfd_oscillator.py`'s license header).
