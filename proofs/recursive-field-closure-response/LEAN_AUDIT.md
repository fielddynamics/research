# Lean audit: Proof 26, Gravity as the Response of Recursive Field Closure

| | |
|---|---|
| **Formalisation source** | [`lean/RecursiveFieldClosureResponse.lean`](lean/RecursiveFieldClosureResponse.lean) |
| **Toolchain** | Lean 4.36.0; Mathlib through the existing proof packages |
| **Direct dependency** | [`../recursive-triforce-closure/lean/`](../recursive-triforce-closure/lean/) (Proof 23), which imports the half-space and forced-frame proofs. Proof 23's labels, 64 addresses, `H4`, `cycle`, `cyAct` and `local_walsh_orthogonal` are imported, not restated. |
| **Build status** | **Passed** on GitHub Actions ([run 45936427946](https://github.com/fielddynamics/research/actions/runs/45936427946), November 26, 2026): `lake build` with the recursive Triforce, half-space and forced-frame proofs it imports, Mathlib from the compiled cache. |
| **Axioms** | All 36 `#print axioms` reports obtained. Every theorem depends only on Lean's standard axioms (`propext`, `Quot.sound`, and for 32 of them `Classical.choice`). No `sorry`, no custom axiom, no warnings in this file. |
| **Independent verification** | 532/532 exact Python checks (`verify_proof26.py`) and 568 appendix checks; these are not Lean proofs |
| **Reproduce** | `cd proofs/recursive-field-closure-response/lean`, then `lake exe cache get`, `lake build`, `lake env lean RecursiveFieldClosureResponse.lean`. |
| **CI** | [`lean-recursive-field-closure-response.yml`](../../.github/workflows/lean-recursive-field-closure-response.yml) rebuilds on every change to this proof or the proofs it imports, and fails on any warning, `sorry`, missing axiom report or non-standard axiom. |

**Verdict:** The finite and algebraic theorems of Proof 26 are machine-checked. The physical premises are not formalised and are not claimed: that the native action selects the collective determinant, that each invariant direction carries |t|² = α, and the long-wave source action. Proof 26 remains a candidate for how read and settlement produce G; its conditional G conclusion is not Lean-certified.

## Statement coverage

| Manuscript (Revision 4) | Lean theorems | Scope |
|---|---|---|
| Theorem 1 (blind closure, sufficient read) | `blind_closure`, `read_factorization` | Fully general: arbitrary types, feasible sets and reads. The differentiable rank corollary is in prose. |
| Theorem 2 (settlement susceptibility) | — | The implicit-function statement is in prose and Python; its finite registration witness is under Theorem 10. |
| Theorem 3 (three Walsh sweeps) | `Hm_sq`, `three_sweeps`, `sweeps_commute`, `H64_sq`, `H64_apply`, `cycle_self_adjoint` | Exact integer matrices on the 64 addresses as Kronecker products: the read is the product of three commuting radix-four sweeps, and `H64 * H64 = 64 • 1`. The XOR-translation selection proposition is in prose. |
| Theorem 4 (Sierpiński inverse) | `sierpinski_four`, `sierpinski_sixtyfour`, `shear_add`, `shear_det`, `alternating_shears` | `H = S D Sᵀ` at sizes 4 and 64 in Proof 23's bit order; one-way shears only add and have determinant one; three alternating shears give the rotation with `p = tan(θ/2)` (over ℝ). |
| Theorem 5 (projective contrast count) | `F4_field`, `cycle_is_omega`, `cycle_additive`, `cycle_free`, `grade_counts`, `cycle_preserves_grade`, `invariant_directions`, `orbit_sum_values`, `orbit_sum_plane` | The label cycle is multiplication by ω in F₄ and is additive; it moves every nonzero address; detail grades have 3, 12, 48 addresses and exactly 1, 4, 16 orbit representatives (21 in all); each orbit sum of characters takes only the values 3 and −1, with 3 on exactly 16 addresses. The F₄ table is checked for associativity, commutativity, distributivity and inverses, not built from Mathlib's `GaloisField`. Pairwise orthogonality of the 21 plane modes is checked in Python. |
| Theorem 6 (completed-block accounting) | `walsh_product`, `face_block_detail`, `channel_block_detail`, `H4e_orthogonal`, `binary_accounting`, `binary_detail_energy` | General factorisation of the Walsh transform of a product vector; completed face and channel blocks have no detail below their level; Walsh orthogonality; for binary occupancy `c₀ = A`, `∑ c² = 64A` and `∑_{a≠0} c_a² = 64A − A²`. |
| Theorem 7 (graded counts) | `coupling_capacity`, `graded_traces`, `coupling_values` | `f(K,1) f(K,−1) = 1 + K² + K⁴ = 1 + K² f(K,0)` for every integer `K`; the traces 21, 17, 13 on grades 1, 4, 16; capacity 273; the PG(2,4) and PG(2,16) counts as arithmetic. |
| Theorem 8 (collective transmission) | `collective_determinant`, `collective_response`, `trace_versus_determinant` | `det(Tᵀ T) = t₁² t₂⁸ t₃³²` for the real grade bridge; with `t² = α` the response `(17/13)·det` equals `(17/13) α²¹`; the normalised trace gives `t²` where the determinant gives `t⁴²` (symmetry does not select the determinant). Real gains; the complex case is the same with `|t|²`. The source-selection propositions are in prose. |
| Theorem 9 (fixed-geometry vortex susceptibility) | `susceptibility_values` | Arithmetic certificate only: `u′ = 2k/(1 − hk)` at the inherited values. The 3 × 3 branch matrices and Sherman–Morrison step are checked in Python. |
| Theorem 10 (recursive registration) | `two_child_registration` | The two-child finite witness: the weighted-mean settlement, flux balance, and the registered energy as a parallel combination plus a positive quadratic. The general partial-minimisation statement is in prose. |
| Theorem 11 (conditional gravitational completion) | — | Continuum Green-function result; not formalised. |
| Projective appendix | — | Its 568 exact incidence checks are in Python (`verify_projective_pencil.py`). |
