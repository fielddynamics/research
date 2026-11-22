# Lean audit: The Mountain Scale in the SST

| | |
|---|---|
| **Formalisation** | [`lean/MountainScale.lean`](lean/MountainScale.lean), Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../sst-khronon-preferred-frame/lean/`](../sst-khronon-preferred-frame/lean/) (`strong_field_not_pure`) and, through it, the net-field rule and the constitutive law; imported, not copied |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 5 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-sst-mountain-scale.yml` |

**Verdict.** The exact split of Theorem 1 and the dimple's blindness to the law are proved for any real vector space and any nonlinearity `N`: for the sweeping projector (idempotent, self-adjoint in the energy product, not commuting with the Laplacian), and for the commuting spectral special case. Theorem 2 (a) is proved. The variational derivation, the projector's properties, the 3D solution, Proposition 3's numbers and Theorem 4 (the edge test) are checked by the script.

| Paper | Lean | Notes |
|---|---|---|
| Theorem 1 (sweeping projector) | `energy_split` | `K` an invertible linear map (`−∇²`), `P² = P`, `K(Pv) = Pᵀ(Kv)`: from `KΦ + Pᵀ N(PΦ) = s`, `Φ − PΦ = K⁻¹s − P(K⁻¹s)` |
| Theorem 1, blind to the law | `energy_blind_to_law` | two laws, same source, same dimple |
| Theorem 1 (commuting special case) | `mountain_split` | from `L Φ + P(N(PΦ)) = s`: `L(Φ − PΦ) = s − Ps` and `P(L(PΦ) + P N(PΦ)) = Ps` |
| Commuting case, blind to the law | `dimple_blind_to_law` | `L` injective: two laws `N₁`, `N₂`, same source, same dimple |
| Theorem 2 (a) | `no_tail_in_dimple` | the dimple's share `(1 − 1)g = 0`; read pointwise, `0 < x(1 − μ) < 1` (`KhrononPreferredFrame.strong_field_not_pure`) |

## Cited or checked by script, not formalised

- The Euler–Lagrange derivation (P comes back as Pᵀ = P): script A2 (1D) and E1 (3D), finite-difference gradients of the discrete action.
- The spectral projector of a curved slice's Laplace–Beltrami operator: script B1.
- That the Laplacian commutes with P and is injective on zero-mean fields: true for the flat-slice Fourier projector (script A1), and the hypotheses of the Lean theorems.
- The Jacobi radii and the data (Proposition 4): script D1–D4, with the cluster dispersions from the net-field rule.
