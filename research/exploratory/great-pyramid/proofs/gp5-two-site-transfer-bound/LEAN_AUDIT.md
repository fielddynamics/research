# Lean audit: gp5-two-site-transfer-bound

| | |
|---|---|
| **File** | [`lean/TransferBound.lean`](lean/TransferBound.lean) |
| **Imports** | `Mathlib` (v4.36.0, the same version as the root `proofs/` chain) |
| **Theorems** | 12 |
| **Axioms** | every `#print axioms` reports only `propext`, `Classical.choice`, `Quot.sound` (some fewer); no `sorry` |
| **CI** | [`.github/workflows/lean-great-pyramid-gp5.yml`](../../../../../.github/workflows/lean-great-pyramid-gp5.yml): builds, then fails on any warning, error, `sorry` or non-standard axiom |

## Statements formalised

| README | Lean | Statement |
|---|---|---|
| Theorem 1 | `closed_form_norm` | `cos² + (Δ/Ω)² sin² + (4κ²/Ω²) sin² = 1` when `Ω² = Δ² + 4κ²` |
| Theorem 1 | `peak_le_one` | peak `4κ²/(Δ²+4κ²) ≤ 1` |
| Theorem 1 | `peak_eq_one_iff` | peak `= 1 ↔ Δ = 0` (κ ≠ 0) |
| Theorem 1 | `peak_le_detuned` | peak `≤ 4κ²/Δ²` |
| Proposition 4 | `detuning_tolerance` | peak `≥ η ↔ Δ² ≤ 4κ²(1-η)/η` |
| Theorem 6 | `budget_mono` | a selector `M ∈ [0,1]` only lowers `sin²(min(κ₀Mt, π/2))` |
| Theorem 6 | `selector_mem` | `M_xy ∈ [0,1]` |
| Theorem 6 | `selector_eq_one_iff` | `M_xy = 1 ↔ d = 0 ∧ χx = -χy ∧ cos²(Δθ/2) = 1` |
| Theorem 6 | `cos_sq_half_eq_one_iff` | `cos²(θ/2) = 1 ↔ θ ∈ 2πℤ` |
| Theorem 6 | `orbitDist_symm` | finite isometric group action: `d(x,y) = d(y,x)` |
| Theorem 6 | `orbitDist_triangle` | `d(x,z) ≤ d(x,y) + d(y,z)` |
| Theorem 6 | `orbitDist_self_smul` | `d(x, g•x) = 0` (zero on relabellings) |

## Checked by script, not formalised

- Theorem 1's ODE solution: script (sympy).
- Theorem 2, the coupling-budget inequality for time-dependent drives (geodesic length on S³): script, 300 random drives; not formalised.
- Corollary 3 and Proposition 5: script.

A Lean proof can be wrong only in its statements; a referee should check the statements above against the README, not the proofs.
