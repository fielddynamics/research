# Lean audit: The Two-Potential Energy of the Constitutive Law in Bimetric MOND (BIMOND)

| | |
|---|---|
| **Formalisation** | [`lean/BimondInteraction.lean`](lean/BimondInteraction.lean), 684 lines, Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../aqual-energy-functional/lean/`](../aqual-energy-functional/lean/) (`g`, its derivative and convexity), [`../constitutive-law-exchange-symmetry/lean/`](../constitutive-law-exchange-symmetry/lean/) (`μ = law`), [`../tetrad-scheme-two-bounded-regions/lean/`](../tetrad-scheme-two-bounded-regions/lean/) (`IsLorentz`, `P`, `X₋`), and through it the half-space and forced-frame formalisations; imported, not copied |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 16 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-bimond-two-potential-energy.yml`, on every change to this proof or any proof it imports |

**Verdict.** Theorems 1–3, Lemma 1, Proposition 1 and Corollaries 1–2 are proved, up to three cited standard steps (§3). Nothing in the note was found to be wrong; the low-acceleration remainder is sharpened from `O(y³)` to `O(y^{7/2})`.

## 1. Definitions to check against the paper

| Lean | Paper |
|---|---|
| `D : V →ₗ[ℝ] S`; `u = ∇φ`, `û = ∇φ̂`, `u − û = ∇φ*`, `w = 𝓜'∇φ*`; `c = 4πG` | the divergence, the fields and the coupling in Eq. (2) (only linearity of `D` is used) |
| `lemma1`'s density `det(e x) · R(g)(x)` with `g = eᵀηe` and `R` any operator on metric fields | the tetrad Einstein–Hilbert density `det(e) R[g(e)]` |
| `yOf x = x μ(x)`; `xOf y = (y + √(y² + 4y))/2`; `nu y = ½ + √(¼ + 1/y)` | `y = xμ(x)`, Eq. (6) |
| `bOf x = 1/(1+x)`; `Mx x = 2x − 1 + 2b − b² + 2 ln b` | Eq. (7) in the total field `x` |
| `My y = Mx (xOf y)`; `Mz z = My √z` | `𝓜` in `y = |∇φ*|/a₀` and in BIMOND's `z = y²` |
| `Q y = y² + My y` | the kinetic function of Eq. (4) |
| `g` (imported from `AqualEnergy`) | `g(x) = F(x²) = x² − 2x + 2 ln(1+x)` |
| Units `a₀ = 1` throughout | |

## 2. Statements

| Paper | Lean | Notes |
|---|---|---|
| Theorem 1: the combination | `combination` | `D[(αβ)(u − û) − (α+β)w] = c(αρ + βρ̂)` |
| … unique up to a factor | `unique_combination` | `û` enters `λ`(1st) + `κ`(2nd) with coefficient `λβ + κα`; zero iff `(λ, κ) ∝ (α, −β)` |
| … constant iff `α + β = 0` | `constant_iff` | for `𝓜'` nonconstant |
| … Eq. (4) | `qumond` | `D(∇φ*) = c(ρ − ρ̂)`, `D(∇φ) = cρ + D(𝓜'∇φ*)` |
| Lemma 1 | `lemma1`, `lemma1_parity` | any curvature operator `R`; uses `TetradScheme.lorentz_acts` |
| Second root ⇒ `α = −1` | `second_root_sign` | `ê ∈ X₋(ĝ)` gives `det(ê) R̂ = −√(−det ĝ) R̂`, from `TetradScheme.Xminus` |
| Proposition 1 | `prop1` | AQUAL's spherical field is exactly `xOf g_N`; realisation ⟺ `1 + 𝓜'(y²) = ν(y)`, given the BIMOND field `(1 + 𝓜')g_N` (Gauss's law, cited) |
| Theorem 2 | `theorem2`, `hasDerivAt_My`, `hasDerivAt_Mz` | `𝓜(0) = 0`; continuity; `𝓜'(z) = −½ + √(¼ + 1/√z)`; `1 + 𝓜'(y²) = ν(y)` as a derivative at `y²`; uniqueness (mean value theorem); both closed forms, the `y`-form with `arsinh`; `d𝓜/dy = 2(x − y)` |
| Corollary 1, `𝓜'` | `cor1_derivative` | `𝓜' → 0` at `∞`; with `z = t⁴`, `𝓜' − (1/t − ½ + t/8) ∈ [−t³/128, 0]` |
| Corollary 1, `𝓜` at low field | `cor1_small` | `𝓜(u²) − (4/3 u³ − ½u⁴ + ⅒u⁵) ∈ [−u⁷/224, 0]` for all `u ≥ 0` |
| Corollary 1, `𝓜` at high field | `cor1_large` | `|𝓜 − (2y − 2 ln y + 1 − 4/y + 5/y²)| ≤ 40/y³` for `y ≥ 2`, via the exact form `𝓜 − 2y + 2 ln y = 1 − b² + 4 ln(1 − b)`, `by = (1 − b)²` |
| Theorem 3 | `theorem3` | `g + Q = 2xy`; `g' = 2y`; `Q' = 2x`; `Q(y) = max_{x'≥0}(2x'y − g(x'))`, attained only at `x' = x`; the logarithms; `|∇φ̂| = μ(x) < 1` |
| Corollary 2 | `cor2`, `radial_strictConvex` | `W = Q(|q|)` strictly convex on any real inner product space (stronger than "for `q ≠ 0`"); `Q'/y = 2ν`, `Q'' = 2(x+1)²/(x(x+2))`, both positive; ratio `(x+1)/(x+2) ∈ [½, 1)`, times the AQUAL ratio `= 1` |

## 3. Cited, not proved

- **Gauss's law** in spherical symmetry (Proposition 1's first step): that Eq. (4) with `ρ̂ = 0` gives `|∇φ*| = g_N` and `|∇φ| = (1 + 𝓜')g_N`.
- **Uniqueness of harmonic functions** with zero boundary values (Corollary 2's last step).
- **The radial-Hessian formula** identifying `Q'/y` and `Q''` as the Hessian eigenvalues of `W`. It is the same formula proved for the AQUAL energy in `AqualEnergy.hessian`; here the eigenvalues are proved as the derivatives of `Q`.

## 4. Notes for a referee

- **Lemma 1.** The action is an integral of the density; Lean proves the identity of densities pointwise for an arbitrary curvature operator, which is what "`g` and `R[g]` are unchanged, `det` changes by `det Λ`" says. The 4-form version with `ε_{abcd}` is not separately formalised.
- **Units.** `a₀ = 1`; restoring `a₀` rescales `x`, `y` and `𝓜` and changes no statement.
- **BIMOND, not bigravity.** The theory is Milgrom's bimetric MOND; the Hassan–Rosen bimetric theory is treated separately in [`../bimetric-lock-constitutive-law/`](../bimetric-lock-constitutive-law/).
