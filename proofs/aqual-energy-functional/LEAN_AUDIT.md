# Lean audit: The Energy Functional of the Constitutive Law μ(x) = x/(x+1)

| | |
|---|---|
| **Formalisation** | [`lean/AqualEnergy.lean`](lean/AqualEnergy.lean), 563 lines, Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../constitutive-law-exchange-symmetry/lean/`](../constitutive-law-exchange-symmetry/lean/) (imported): `μ` is its `law x = x/(x+1)` |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 12 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-aqual-energy-functional.yml`, on every change to this proof or the constitutive law |

**Verdict.** Theorem 1 and Theorem 2 are proved as stated (Theorem 2 on every real inner product space, which includes `ℝ³`). Corollary 1 is proved except at the single point `y = 1` of Eq. (6), where explicit error bounds hold instead. Corollary 2 is proved up to its divergence-theorem step, which is cited; its pointwise inequality is proved.

## 1. Definitions to check against the paper

| Lean | Paper |
|---|---|
| `F y = y − 2√y + 2 log(1 + √y)` | Eq. (4) |
| `g r = r² − 2r + 2 log(1 + r)`; `F_sq : F (r²) = g r` for `r ≥ 0` | `g(r) = F(r²)` in the proof of Theorem 2 |
| `law` (imported) | `μ(x) = x/(x+1)`, Eq. (3) |
| `W q = F ‖q‖²` on a real inner product space `E` | `W(q) = F(|q|²)`, `q ∈ ℝ³` |
| `G q = (2μ(‖q‖)) • q` | `∇W` |
| `A q = μ(‖q‖) • q` | `A(p)` with `a₀ = 1` (the scaling `A(p) = a₀ A(p/a₀)` changes nothing below) |
| `H q = 2μ(x) I + (2/((1+x)² x)) q qᵀ` | Eq. (6), rewritten: `2μ(I − q̂q̂ᵀ) + 2(xμ)' q̂q̂ᵀ` with `2(xμ)' − 2μ = 2x/(1+x)²` |

## 2. Statements

| Paper | Lean | Notes |
|---|---|---|
| Theorem 1 | `theorem1` | `F(0) = 0`; continuous on `[0, ∞)`; `F' = μ(√y)` for `y > 0`; right derivative `μ(0) = 0` at `0`; any `F₂` with these properties equals `F` on `[0, ∞)` (by the mean value theorem, so no derivative at `0` is assumed for `F₂`) |
| Eq. (5), `0 ≤ y < 1` | `series_small` | `HasSum` of `2(−1)^{k+1} y^{k/2}/k`, `k ≥ 3` |
| Eq. (5), `y = 1` | — | needs Abel's theorem; not formalised (`g_bounds` gives `|F − ⅔ + ½| ≤ ⅖` there) |
| Low-acceleration order | `g_bounds` | `0 ≤ F ≤ ⅔y^{3/2}` and `0 ≤ F − ⅔y^{3/2} + ½y² ≤ ⅖y^{5/2}`, all `y ≥ 0` |
| Eq. (6), `y > 1` | `series_large` | `HasSum` of the `y^{−k/2}` series; and `0 < F − (y − 2√y + ln y) ≤ 2/√y` for all `y > 0` |
| Theorem 2: `W ∈ C²` | `W_contDiff_two` | Mathlib's `ContDiff ℝ 2` |
| Smooth away from `0` | `contDiffAt_W`, `contDiffAt_G` | Every order |
| `∇W` | `hasFDerivAt_W` | At every `q`, including `0` (where `|W| ≤ ⅔|q|³`) |
| `∇²W`, Eq. (6); `∇²W(0) = 0` | `hasFDerivAt_G`, `hasFDerivAt_G_zero` | |
| Eigenvalues, positivity, Eq. (7), `(xμ)'` | `hessian` | `H q q = 2(xμ)' q`, `H q v = 2μ v` for `v ⊥ q`; both positive; ratio `(x+2)/(x+1) ∈ (1, 2]`; `HasDerivAt (x ↦ xμ(x))`; `‖H q‖ ≤ 4|q|` |
| Strict convexity | `W_strictConvex` | `StrictConvexOn ℝ univ W`: via `g` strictly convex and increasing on `[0, ∞)` and the strict convexity of the norm ball |
| Strict monotonicity of `A` | `A_strictMono` | `(A p − A p')·(p − p') > 0` for `p ≠ p'`, proved directly: `≥ (r−s)²(r+s+rs)/((1+r)(1+s))` if `|p| ≠ |p'|`, `= μ|p − p'|²` if equal |
| Corollary 2 | `A_strictMono` (pointwise part) | The divergence theorem on `Ω` and the conclusion `∇w = 0 ⇒ w = 0` are cited |

## 3. Notes for a referee

- **Dimension.** Theorem 2 is stated for any real inner product space; the paper's `ℝ³` is the case `EuclideanSpace ℝ (Fin 3)`. Nothing in the argument uses the dimension.
- **Ellipticity.** The principal symbol of `∇·A(∇Φ)` is `½ ∇²W`, so `hessian` gives its eigenvalues; "elliptic" is the paper's name for their positivity.
- **Strict convexity and monotonicity** are proved independently: neither is derived from the other, so the proof of Corollary 2's inequality does not route through the Hessian.
