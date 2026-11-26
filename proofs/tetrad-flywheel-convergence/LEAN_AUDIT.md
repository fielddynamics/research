# Lean audit — Proof 25

**Status: machine-checked.** Lean 4.36.0; direct import `FlywheelTetradGeometry`, through it `RecursiveTriforceClosure` and the preceding geometry packages. **Passed** on GitHub Actions ([run 45895547770](https://github.com/fielddynamics/research/actions/runs/45895547770), November 26, 2026). All 35 `#print axioms` reports obtained: 33 theorems depend only on Lean's standard axioms (`propext`, `Classical.choice`, `Quot.sound`) and 2 on no axioms at all. No `sorry`, no custom axiom, no warnings in this file. [![Lean proof](https://github.com/fielddynamics/research/actions/workflows/lean-tetrad-flywheel-convergence.yml/badge.svg)](https://github.com/fielddynamics/research/actions/workflows/lean-tetrad-flywheel-convergence.yml) The 297 exact Python assertions are independent checks, not Lean certification.

| Manuscript | Lean theorems | Limits of formal coverage |
|---|---|---|
| 1 | `shared_outside_vertex`, `attached_triangles` | Critical vertex equality for arbitrary vertex type. Reduction from general simple graph and orientation uniqueness in prose. |
| 2 | `dual_symmetric`, `dual_involutive`, `dual_cut_cycle`, `dual_projectors`, `closureP_symm`, `closureP_idem`, `intrinsic_frame_gram`, the four inherited real Gram statements | Signed complementary-edge identities; concrete common metric. Full group covariance in Proof 24 and Python; abstract uniqueness from forced frame in prose. |
| 3 | `zero_gram`, `support_of_gram`, `transport_apply`, `transport_composition`, source and target projectors, idempotence, uniqueness on image | Generic real matrix theorem in normalized coordinates X/2. Interpretation as orthogonal isometry and arbitrary finite sequence follows in prose. |
| 4 | `barycentric_inverse`, `barycentric_sum`, `upper_bound_forces_lower`, `unique_outer_spike`, `fourth_saturation`, `inherited_core` | Scalar algebra and inherited set identity. General convex extreme-point and recession cone arguments in prose. |
| 5 | `pair_row_gram`, `core_vertex_gram`, `core_tight_frame`, `core_spatial_bridge`, `core_face_adjacency` | Pair-incidence metric and finite face adjacency. General 3+2 current theorem imported from Proof 24; current conversion and physical interpretation in prose. |
| 6 | `diagonal_metric_rigidity`, `constant_weights_gram`, `anisotropy_square` | Necessity, sufficiency, explicit polynomial. Sharp norm bounds and equality cases proved in prose; Python checks exact witnesses. |

## Build

From the repository: `cd proofs/tetrad-flywheel-convergence/lean`; `lake exe cache get`; `lake build`; `lake env lean TetradFlywheelConvergence.lean`. The workflow [`lean-tetrad-flywheel-convergence.yml`](../../.github/workflows/lean-tetrad-flywheel-convergence.yml) fails on any warning, error, missing report or non-standard axiom.

The supplied source had never been compiled and did not elaborate. It was repaired without weakening any theorem (the finite matrix statements were first re-checked with exact arithmetic): matrix number types stated explicitly, `closureP` marked `noncomputable`, rational matrix identities proved entry by entry instead of with `decide`, the inherited Gram theorems composed from Proof 24's lemmas by congruence, and the rigidity cases naming each edge for `linarith`. The unused-simp-argument style linter is switched off for this file; it does not affect what is proved. All physical assumptions remain explicit, irrespective of formal certification.
