# Lean audit — Proof 25

**Status: source draft, build pending.** Lean 4.36.0; direct import `FlywheelTetradGeometry`, through it `RecursiveTriforceClosure` and the preceding geometry packages. The repository's Proof 24 CI was present at the inspected commit, but no successful build was established here. This package contains no new axiom declarations, unfinished proofs or native decision oracle. The 297 exact Python assertions are independent checks, not Lean certification.

| Manuscript | Formal statements supplied | Limits of formal coverage |
|---|---|---|
| 1 | `shared_outside_vertex`, `attached_triangles` | Critical vertex equality for arbitrary vertex type. Reduction from general simple graph and orientation uniqueness in prose. |
| 2 | `dual_symmetric`, `dual_involutive`, `dual_cut_cycle`, `dual_projectors`, `closureP_symm`, `closureP_idem`, `intrinsic_frame_gram`, the four inherited real Gram statements | Signed complementary-edge identities; concrete common metric. Full group covariance in Proof 24 and Python; abstract uniqueness from forced frame in prose. |
| 3 | `zero_gram`, `support_of_gram`, `transport_apply`, `transport_composition`, source and target projectors, idempotence, uniqueness on image | Generic real matrix theorem in normalized coordinates X/2. Interpretation as orthogonal isometry and arbitrary finite sequence follows in prose. |
| 4 | `barycentric_inverse`, `barycentric_sum`, `upper_bound_forces_lower`, `unique_outer_spike`, `fourth_saturation`, `inherited_core` | Scalar algebra and inherited set identity. General convex extreme-point and recession cone arguments in prose. |
| 5 | `pair_row_gram`, `core_vertex_gram`, `core_tight_frame`, `core_spatial_bridge`, `core_face_adjacency` | Pair-incidence metric and finite face adjacency. General 3+2 current theorem imported from Proof 24; current conversion and physical interpretation in prose. |
| 6 | `diagonal_metric_rigidity`, `constant_weights_gram`, `anisotropy_square` | Necessity, sufficiency, explicit polynomial. Sharp norm bounds and equality cases proved in prose; Python checks exact witnesses. |

## Build

From the repository: `cd proofs/tetrad-flywheel-convergence/lean`; `lake update` if a manifest is absent; `lake exe cache get`; `lake build`; `lake env lean TetradFlywheelConvergence.lean`. Audit every `#print axioms` report, allowing only standard Lean axioms. The workflow draft checks for warnings, errors and nonstandard axioms. Do not mark this proof + Lean verified until the build and reports actually pass. Fix any elaboration errors without weakening the theorems. All physical assumptions remain explicit, irrespective of formal certification.
