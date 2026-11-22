# Lean audit: The SST Khronon

| | |
|---|---|
| **Formalisation** | [`lean/KhrononPreferredFrame.lean`](lean/KhrononPreferredFrame.lean), Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../net-field-rule/lean/`](../net-field-rule/lean/) (`flux_exponent`, `free_fall`, `jacobi`) and [`../constitutive-law-exchange-symmetry/lean/`](../constitutive-law-exchange-symmetry/lean/) (`law`); imported, not copied |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 15 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-sst-khronon-preferred-frame.yml`, on every change to this proof or any proof it imports |

**Verdict.** The algebra of the picture (slope, dimple, edge), of Theorems 1, 3, 4 (1), 5 and of Theorem 6 is proved. Flanagan's equations (the slow-motion action, the khronon fluid, the kinetic matrix and the stability conditions) and Bonetti and Barausse's PPN formulas are cited, not formalised. Theorem 2, the family scan of Theorem 4 (2), the solar-system numbers and Proposition 7 are checked by the script.

## 1. Definitions to check against the paper

| Lean | Paper |
|---|---|
| `law` | `ConstitutiveLaw.law`, `μ(x) = x/(x + 1)` |
| `alpha1 α β`, `alpha2 α β l`, `cs2 α β l` | Bonetti–Barausse Eqs. 15, 16, 14 (`l` is their λ) |
| `fun a => 2 * a * (m (a / a0) - 1)` | `f'(a)` for a general law `m` (paper Eq. 1) |
| `fun t => t * (1 - m t)` | the TetB share in units of `a₀`, `x(1 − μ)` |

## 2. Statements

| Paper | Lean | Notes |
|---|---|---|
| Theorem 1 | `bb_point` | at β = 0: `α₁ = −4α`; `λ α₂ = α(λ − α − 2αλ)/(α − 2)`, non-zero at λ = 0; `c_s² = 0` at β = λ = 0 |
| Theorem 3, Eq. (2) | `stability_dictionary` | for any differentiable `m`: the derivative of `f'` at `a₀x`; `−f''/2` is the derivative of the TetB share; `a f'' − f' = 2a·x m'` |
| Theorem 3, `x(1 − μ) = μ` | `share_eq_law` | for `x ≥ 0` |
| Theorem 3, `μ'` and the share's derivative | `law_deriv`, `share_deriv` | both `1/(x + 1)²` |
| Theorem 3, Eq. (3) | `gfd_stable` | `f' = −2a₀μ`, `f''` value `−2/(x+1)²`, `a f'' − f' = 2a₀x²/(x+1)²`, with signs, for every `x > 0` |
| Theorem 4 (1) | `stability_forces_tail`, `no_constant_limit` | `f'` antitone on `[a₁, ∞)`, `f'(a₁) < 0` ⇒ `f → −∞`, no finite limit |
| Theorem 4 (1), GFD's tail | `share_limit` | `x(1 − μ) → 1`, i.e. the tail → `a₀` |
| Theorem 4 (2), `n = 2` | `standard_law_turns_over` | the share at `x = 10` is below its value at `x = 1` |
| Theorem 5 | `density_exponent` | `2 + (1 − m)(−2/(2 − m)) = 2/(2 − m) = 2 − s`, positive (uses `NetFieldRule.flux_exponent`) |
| Theorem 5, Eq. (4) | `oscillation_frequency` | `ρ_T0/h_⊥ = [2/(2 − μ)]Ω² = −dg/dr`, strictly between `Ω²` and `2Ω²` |
| The picture | `strong_field_not_pure` | for every `x > 0`, `0 < x(1 − μ) < 1`: a stronger field never gives pure TetA |
| The picture, Theorem 6 | `slope_and_dimple` | the dimple's linear share `(1 − 1)g = 0`; a uniform slope drops out (`NetFieldRule.free_fall`); at `r_J³ = GM/2Ω²` the Sun's pull equals the tide, `GM/r_J² = 2Ω² r_J` (`NetFieldRule.jacobi`) |
| Theorem 6 | `inertia_vanishes` | `(1 − μ) → 0` and `(1 − μ)² → 0` |

## 3. Cited, not formalised

- Bonetti and Barausse's PPN formulas (their Eqs. 14–16), and Flanagan's statement that their expansion does not apply at β = λ = 0.
- Flanagan's slow-motion action, khronon fluid (Eqs. 21–24), kinetic matrix (Eq. 32) and stability conditions (Eqs. 43, 48, 53, 54).
- The radial profile around a point mass, `d ln x/d ln r = −2/(2 − μ)`, enters `density_exponent` and `oscillation_frequency` as an algebraic input; it is checked by the script (C2) and follows from `NetFieldRule.gN_deriv`.
