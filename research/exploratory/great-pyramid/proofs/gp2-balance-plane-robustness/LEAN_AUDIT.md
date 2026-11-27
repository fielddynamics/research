# Lean audit: gp2-balance-plane-robustness

| | |
|---|---|
| **File** | [`lean/BalanceRobustness.lean`](lean/BalanceRobustness.lean) |
| **Imports** | `Mathlib` (v4.36.0, the same version as the root `proofs/` chain) |
| **Theorems** | 11 |
| **Axioms** | every `#print axioms` reports only `propext`, `Classical.choice`, `Quot.sound` (some fewer); no `sorry` |
| **CI** | [`.github/workflows/lean-great-pyramid-gp2.yml`](../../../../../.github/workflows/lean-great-pyramid-gp2.yml): builds, then fails on any warning, error, `sorry` or non-standard axiom |

## Statements formalised

| README | Lean | Statement |
|---|---|---|
| Theorem 3 | `affine_share_diff` | `g(u) - g(v) = (v-u) Q(u,v,b)` (exact factorisation) |
| Theorem 3 | `affine_share_strictAntiOn` | for `-1 < b ≤ 2`, `g(u) = (1-u)²(1+bu)` is strictly decreasing on `[0,1]` |
| Theorem 3 | `affine_balance_unique` | unique balance level for `-1 < b ≤ 2` |
| Theorems 3–4 | `partials` | `∂g/∂u = -(1-u)(2-b+3bu)` and `∂g/∂b = (1-u)²u` (as `HasDerivAt`) |
| Theorem 4 | `shift_coefficient` | `(1-u₀)²u₀ / (2(1-u₀)) = (√2-1)/4` at `u₀ = 1 - 1/√2` |
| Theorem 5 | `interval_sq` | `r ∈ [1-ε,1+ε]`, `(1-u)²r = 1/2` ⇒ `1/(2(1+ε)) ≤ (1-u)² ≤ 1/(2(1-ε))` |
| Theorem 5 | `interval_sqrt` | ⇒ `1 - 1/√(2(1-ε)) ≤ u ≤ 1 - 1/√(2(1+ε))` |
| Theorem 5 | `interval_sharp` | the constant ratios `1 ± ε` attain the ends |
| Theorem 8 | `constitutive_half_iff` | `x/(x+1) = 1/2 ↔ x = 1` (`g = a₀`) |
| Theorem 8 | `structural_ne_constitutive` | `|1/2 - 1| = 1/2` |
| Theorem 8 | `tetB_share_small` | `1 - x/(x+1) < 1/x` for `x > 0` |

## Checked by script, not formalised

- Theorems 1–2 (centroid identity, frustum flux balance): script, exact rationals.
- Theorem 3 for `b > 2` (non-monotone but still a unique root): script, exact root isolation.
- Theorem 4's second-order coefficient `1 - 11√2/16`: script (sympy).
- Theorems 6–7 (Earth monopole solid-angle fluxes, self-gravity bound): script, 40-digit numerics.
- Theorem 8's premise, the net-field rule, is itself Lean-checked in `proofs/net-field-rule/` (not imported here).

A Lean proof can be wrong only in its statements; a referee should check the statements above against the README, not the proofs.
