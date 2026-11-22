# Lean audit: The Mountain Scale in the SST

| | |
|---|---|
| **Formalisation** | [`lean/MountainScale.lean`](lean/MountainScale.lean), Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../sst-khronon-preferred-frame/lean/`](../sst-khronon-preferred-frame/lean/) (`strong_field_not_pure`) and, through it, the net-field rule and the constitutive law; imported, not copied |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 3 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-sst-mountain-scale.yml` |

**Verdict.** Theorem 2 (the exact split and the dimple's blindness to the law) is proved for any real vector space, any linear `L` and `P` with `P² = P` and `LP = PL`, and any nonlinearity `N`. Theorem 3 (a) is proved. The variational derivation (Theorem 1), the projector's properties on a curved slice, the 3D solution and Proposition 4's numbers are checked by the scripts.

| Paper | Lean | Notes |
|---|---|---|
| Theorem 2 | `mountain_split` | from `L Φ + P(N(PΦ)) = s`: `L(Φ − PΦ) = s − Ps` and `P(L(PΦ) + P N(PΦ)) = Ps` |
| Theorem 2, the dimple is blind to the law | `dimple_blind_to_law` | `L` injective: two laws `N₁`, `N₂`, same source, same dimple |
| Theorem 3 (a) | `no_tail_in_dimple` | the dimple's share `(1 − 1)g = 0`; read pointwise, `0 < x(1 − μ) < 1` (`KhrononPreferredFrame.strong_field_not_pure`) |

## Cited or checked by script, not formalised

- The Euler–Lagrange derivation (P comes back as Pᵀ = P): script A2 (1D) and E1 (3D), finite-difference gradients of the discrete action.
- The spectral projector of a curved slice's Laplace–Beltrami operator: script B1.
- That the Laplacian commutes with P and is injective on zero-mean fields: true for the flat-slice Fourier projector (script A1), and the hypotheses of the Lean theorems.
- The Jacobi radii and the data (Proposition 4): script D1–D4, with the cluster dispersions from the net-field rule.
