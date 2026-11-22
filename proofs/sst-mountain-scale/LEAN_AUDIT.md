# Lean audit: The Mountain Scale in the SST

| | |
|---|---|
| **Formalisation** | [`lean/MountainScale.lean`](lean/MountainScale.lean), Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../sst-khronon-preferred-frame/lean/`](../sst-khronon-preferred-frame/lean/) (`strong_field_not_pure`) and, through it, the net-field rule and the constitutive law; imported, not copied |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 8 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-sst-mountain-scale.yml` |

**Verdict.** Theorem 1 (the ownership split, with overlapping spheres, for any law) and Theorem 2 (the four ports) are proved. Theorem 3 (b) is proved (`no_tail_in_dimple`). The variational derivation, the sweep's exactness outside each sphere, the matter equation, the 3D solutions, Proposition 4's numbers and Theorems 5–6 are checked by the script.

## Statements used by the paper

| Paper | Lean | Notes |
|---|---|---|
| Theorem 1 | `ownership_split` | `K` linear (`−∇²`), `d` the systems' own interior fields with `K d = s − s̄`: from `KΦ + N(Φ − d) = s`, the mountain solves `K(Φ − d) + N(Φ − d) = s̄`. Nothing assumes the spheres are disjoint |
| Theorem 1, the same for every law | `ownership_blind_to_law` | two laws, same matter: both mountains solve their laws on `s̄`, and `d` is shared |
| Theorem 2 | `four_ports` | point masses with centre of mass at the origin in `c₀ + b ⬝ x + q(x)`: interaction `(Σm) c₀ + Σ m q(pᵢ)`; the dipole term vanishes |
| Theorem 3 (b) | `no_tail_in_dimple` | the own field's share `(1 − 1)g = 0`; read pointwise, `0 < x(1 − μ) < 1` (`KhrononPreferredFrame.strong_field_not_pure`) |

## Earlier forms, still proved

`mountain_split`, `dimple_blind_to_law`, `energy_split` and `energy_blind_to_law` are the splits for a projector on the field: a fixed-scale low-pass, and a region sweep that is self-adjoint in the field-energy product. They are true, but the paper no longer uses them, because a projector on regions of space cannot let closure spheres overlap.

## Checked by script, not formalised

- The sweep (balayage) leaves the field outside each sphere unchanged: script A1 (1D, to 4 × 10⁻¹⁴) and G1 (3D).
- The Euler–Lagrange equation of the discrete action: script A2.
- The matter equation and its size: script B1.
- The tidal suppression (s/r_J)³ and the Jacobi radii: script C2, D1–D3.
- A field-dependent radius and the edge theorem: script E1–E2, F1–F2.
