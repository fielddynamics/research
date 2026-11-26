# Lean audit: Recursive Triforce Closure of the Dual Tetrad

| | |
|---|---|
| **Formalisation source** | [`lean/RecursiveTriforceClosure.lean`](lean/RecursiveTriforceClosure.lean) |
| **Toolchain** | Lean 4.36.0; Mathlib through the existing half-space package |
| **Direct dependency** | [`../half-space-two-bounded-regions/lean/`](../half-space-two-bounded-regions/lean/), which imports the forced-frame proof |
| **Build status** | **NOT RUN.** Lean, Lake and Elan are not installed in the current runtime. Network DNS access to GitHub is unavailable. |
| **Axioms** | `#print axioms` commands included; their outputs have not been obtained. No custom axiom, `sorry`, `admit` or `native_decide` is intentionally used in the source. |
| **Independent verification** | 214/214 exact Python checks passed; not Lean proofs |
| **Reproduce** | Place the directory in the repository, `cd proofs/recursive-triforce-closure/lean`, then `lake update`, `lake exe cache get`, `lake build`. |
| **CI** | Not enabled. Add CI only after compiler and axiom gates pass. |

**Verdict:** This is a proposed formalization, not a verified Lean result. The source contains actual theorem statements and proof terms/tactics, rather than placeholder axioms, but compilation may reveal elaboration, termination, finite-decision or import issues. In particular, some large finite `decide` goals may require splitting or a more structural proof. Do not add a green badge, change the formal proof count, or call this package machine-checked before an actual kernel build.

## Statement coverage

| Paper | Lean statements supplied | Limitations |
|---|---|---|
| Theorem 1 | `inherited_hull`, `medial_cover`, `medial_unique_interiors`, `medial_center_iff`, `medial_corner_iff`, `medial_area_factor` | Barycentric affine inverses, covering inequalities and area multiplier. The geometric partition for arbitrary depth, face-area theorem, and identification of the first medial regions with inherited core/corners are proved in prose; not fully formalized as sets of real points. |
| Theorem 2 | `midpoint_lattice`, `projection_surjective`, `face_lattice_grid`, `quarter_grid_card`, `dyadic_depth`, `reference_grid_saturated` | Integer lattice basis characterization, arithmetic normal projection, reference-face grid and all-depth divisibility, finite refined-grid saturation. The 3D-to-2D real projection identification, nearest-neighbour mesh/clique theorem and transfer to every normal plane are prose proofs. |
| Theorem 3 | `vertex_bridge`, `refined_coefficients`, `refined_half_integral`, `refined_lattice_sum`, `distinct_refined_tiles`, `address_count`, `geometric_covariance`, `table_complete` | Explicit barycentric integer model, tied to upstream real matrix; actual coefficient covariance. Passage to real triangles and paired-chamber quotient is justified in prose, not a Lean quotient of real sets. |
| Theorem 4 | `pointing_counts`, `pointing_recurrence`, `face_trace`, `trace_polynomial` | Exact finite counts and general recurrence; interpretation as triangle pointing follows from affine maps in prose. |
| Theorem 5 | `dictionary_left_inverse`, `dictionary_right_inverse`, `dictionary_bijective`, `dictionary_grading`, `dictionary_unit_sign`, `proper_equivariance`, `repaired_equivariance`, `reflection_trace_witness`, `table_complete` | Signed basis isomorphism for all enumerated permutations (with completeness). Extension to vector spaces, group representation law, trace invariance under similarity and nonuniqueness are proved in prose; no Lean formalization of exterior/symmetric tensor products or actual torsion tensor bundles. The reflection witness is a signed character calculation, not a machine-checked theorem about all linear intertwiners. |
| Theorem 6 | `local_walsh_orthogonal`, `tree_counts`, `cycle_order`, `cycle_fixed`, `invariant_counts`, `cycle_pointing_fixed`, `invariant_pointing_counts` | Local orthogonality and exact finite counts. Full 64×64 orthogonality independently verified in Python; general tree factorization, Burnside argument, mean-zero compression and no-equivariant-bijection are established in prose. |
| Proposition | — | Measure additivity, radial projection and weighted conditional expectation remain analytic prose. Numerical angles from existing research are not an exact proof. |

## Build gates

1. Use the pinned toolchain, and build the real upstream package rather than copying its geometry into independent axioms.
2. Run `lake build` and fix any compiler errors or warnings. Confirm no unfinished proof, custom axiom, or native decision oracle is used. `decide` uses the kernel's reduction, but large finite calculations may need structural lemmas.
3. Inspect all `#print axioms` output. The repository's usual release policy permits only `propext`, `Classical.choice`, and `Quot.sound` where they occur.
4. Extend formal coverage or accurately describe narrower statements in the released audit. Re-run the Python checks; do not add their counts to the Lean theorem count.
5. Only then amend the proof index and dependency diagrams or enable CI.

No changes to the upstream half-space, frame, torsion or SST proof packages are required by this draft.
