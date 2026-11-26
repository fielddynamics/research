# Lean audit: The Intrinsic Tetrahedral Geometry of the Collective Flywheel

| | |
|---|---|
| **Formalisation source** | [`lean/FlywheelTetradGeometry.lean`](lean/FlywheelTetradGeometry.lean) |
| **Toolchain** | Lean 4.36.0, Mathlib inherited through the existing proof packages |
| **Direct dependency** | [`../recursive-triforce-closure/lean/`](../recursive-triforce-closure/lean/), which imports the half-space and forced-frame proofs |
| **Build status** | **Passed** on GitHub Actions ([run 45893486437](https://github.com/fielddynamics/research/actions/runs/45893486437), November 26, 2026): `lake build` with the recursive Triforce, half-space and forced-frame proofs it imports, Mathlib from the compiled cache. |
| **Axioms** | All 57 `#print axioms` reports obtained (the 50 manuscript statements plus 7 helper lemmas). Every theorem depends only on Lean's standard axioms (`propext`, `Classical.choice`, `Quot.sound`). No `sorry`, no custom axiom, no warnings in this file. |
| **Independent verification** | 65 exact Python checks; 167 companion checks (including numerical time evolution), not Lean proofs |
| **Reproduce** | `cd proofs/flywheel-tetrad-geometry/lean`; `lake exe cache get`; `lake build` |
| **CI** | [`lean-flywheel-tetrad-geometry.yml`](../../.github/workflows/lean-flywheel-tetrad-geometry.yml) rebuilds on every change to this proof or the proofs it imports, and fails on any warning, `sorry`, missing axiom report or non-standard axiom. [![Lean proof](https://github.com/fielddynamics/research/actions/workflows/lean-flywheel-tetrad-geometry.yml/badge.svg)](https://github.com/fielddynamics/research/actions/workflows/lean-flywheel-tetrad-geometry.yml) |

**Verdict:** Machine-checked. The table below records which manuscript statements are formalised; the prose parts named in it are not. The physical selection of the incidence, norm and spatial embedding remains open.

## Statement coverage

| Manuscript theorem | Lean theorems | Scope |
|---|---|---|
| 1. Cycle Gram | `incidence_gram`, `cycle_gram`, `boundary_boundary`, `cycle_projector`, `gram_projector`, `cycle_zero_sum`, `real_cycle_projector`, `weighted_gram_entries` | Exact signed finite incidence matrices, rational projector identities and real weighted entries. The dimension and image/kernel argument is given in prose using these identities. |
| 2. Column Gram and minimum norm | `row_gram`, `row_projector_idempotent`, `row_projector_symmetric`, `row_projector_closed`, `column_gram`, `read_right_inverse`, `read_row_closed`, `read_norm`, `read_orthogonality`, `real_column_definition`, `real_column_gram`, `common_real_gram`, `normalizing_factor` | The exact certificates for the minimum-norm solution, including the real normalized Gram. The abstract complex Hilbert-space minimization and uniqueness argument is in the manuscript. |
| 3. Oriented isometry | `isometry_maps_frame`, `isometry_source_projector`, `isometry_target_projector`, `column_covariant`, `cycle_covariant`, `all_relabelings` | Rational rescaling L0 = (3/8)DC of the real partial isometry L; its identities and all 24 label permutations, with completeness imported. The normalization gives L = sqrt(2/3)L0; extension as a real linear isometry and the covariance of L follow in prose. |
| 4. Actual core | `inversion_squared`, `even_embedding`, `even_embedding_norm`, `even_cycles_are_core_cycles`, `even_parametrization`, `odd_parametrization`, `even_family`, `odd_family`, `even_parameters_unique`, `odd_parameters_unique`, `core_decomposition` | Explicit real 3- and 2-coordinate families and their inverse coordinates; parity split of conservative currents. Dimension language follows from these linear parametrizations, rather than relying on a separate rank oracle. |
| 5. Collective phase and edge current | `wedge_row_closed`, `wedge_core`, `cycle_reconstruction`, `common_shift_cancels`, `common_core_gain`, `physical_current_identity` | Real phase wedge conservation, explicit cycle reconstruction and undivided current identity. Complex multiplication is expressed as real pairs. Exterior-power surjectivity and correspondence to the inherited Stage VII Hamiltonian are prose/Python results, not a formalisation of the Schrödinger evolution. |
| 6. Spatial reconstruction | `real_cycle_tetrad_gram`, `flywheel_tetrad_gram`, `positive_hull`, `negative_hull`, `shared_octahedron`, `inherited_midpoints` | Exact common Gram tied to the upstream real frame, imported positive and negative convex hulls and octahedral intersection, and midpoint certificate. General congruence of spanning realizations and the eight attached tetrahedra argument are in the manuscript. |

## Repair before the first build

The supplied source had never been compiled and did not elaborate. It was repaired without changing what any theorem states (every matrix statement was first re-checked with exact arithmetic):

- matrix number types are stated explicitly where Lean could not infer them;
- the real-valued tables are marked `noncomputable`;
- finite matrix identities are proved entry by entry (`fin_cases` with `norm_num`) through explicit rational forms of `rowProjector`, `C`, `Z` and `L0`, each proved equal to its definition (`rowProjector_eq`, `C_eq`, `Z_eq`, `L0_eq`);
- relabelling covariance goes through closed integer tables (`tileCoeff_eq`, `edgeCoeff_eq`, `epsT_covariant`);
- the core parametrisations use four-term row sums so `linarith` sees matching terms.

The unused-simp-argument style linter is switched off for this file, because the shared simp sets list structural lemmas some identities do not use; it does not affect what is proved. The Python check counts are not counted as Lean theorems.
