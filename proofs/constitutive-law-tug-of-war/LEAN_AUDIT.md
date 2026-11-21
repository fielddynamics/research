# Lean audit: The Constitutive Law as a Tug of War

| | |
|---|---|
| **Formalisation** | [`lean/TugOfWar.lean`](lean/TugOfWar.lean), 477 lines, Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../walsh-eigenmodes-of-the-cube/lean/`](../walsh-eigenmodes-of-the-cube/lean/) (`mu`, `SA`, `SB`, `coef`, `scalar_invariant`, `node_mu`, `inversion_exchanges`) and [`../constitutive-law-exchange-symmetry/lean/`](../constitutive-law-exchange-symmetry/lean/) (`law`); imported, not copied |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 12 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-constitutive-law-tug-of-war.yml`, on every change to this proof or any proof it imports |

**Verdict.** Lemma 1, Theorem 1, Theorem 2 (i)–(iii), Proposition 1 (b)–(d), Proposition 2, Theorem 3 and Proposition 3 (i)–(ii) are proved. Theorem 2 (iv) is the imported `unique_law`. Proposition 1 (a) and (e) and the Burgers core scaling are checked by the script.

## 1. Definitions to check against the paper

| Lean | Paper |
|---|---|
| `teams wA wB` | the two-team state: `wA` on TetA's corners, `wB` on TetB's |
| `mu`, `SA`, `SB`, `coef` (from Walsh) | the TetA share `S_A/(S_A + S_B)`, the chamber sums and the Walsh coefficients `c_S` |
| `Screens n m p μ` | the screening relation (S): `xⁿ (1 − μ)ᵐ = μᵖ` for all `x > 0`, with real exponents |
| `Exchange μ` | the exchange (X): `μ(x⁻¹) = 1 − μ(x)` for all `x > 0` |
| `muk k x` | the power-law family `μ_k = x^k/(1 + x^k)` |
| `gdeep k GM a0 r` | the deep-field pull, `(GM a₀^k r^(−2))^(1/(k+1))`, solving `x^k g = GM/r²` |
| `strength g gbar` | TetB's measured strength `w = g (g − g_bar)/g_bar` |
| `ratio g gbar a0` | the decode `M_dec/M_phot = μ(g/a₀) g/g_bar` |
| `om β`, `om1 β`, `om2 β` | the Burgers vorticity `exp(−βr²)` and its first two derivatives |
| `lo Γ ν r t` | the Lamb–Oseen vorticity `(Γ/4πνt) exp(−r²/4νt)` |

## 2. Statements

| Paper | Lean | Notes |
|---|---|---|
| Lemma 1 | `lemma1`, `cube_tug_of_war` | symmetric states are `teams` states; share `w_A/(w_A + w_B)`; rope position `c_xyz/c₁ = (w_A − w_B)/(w_A + w_B) = 2μ − 1`; `−I` swaps the teams; `T₂` modes leave `μ` unchanged; with `g` and `a₀` the share is `ConstitutiveLaw.law (g/a₀)` |
| Theorem 1 | `theorem1`, `exchange_half`, `muk_exchange` | (X) ⟺ `m = p`, for real exponents with `p > 0`; then odds `x^(n/p)` and `μ = μ_{n/p}`; every `μ_k` is exchange-symmetric |
| Theorem 2 (i) ⟺ (ii) | `strengths_are_accelerations` | `μ_k(g/a₀)(g + a₀) = g` for all `g > 0` ⟺ `k = 1` |
| Theorem 2 (i) ⟺ (iii) | `deep_field` | `x^k g = GM/r²`; `v² = (GM a₀^k)^(1/(k+1)) r^((k−1)/(k+1))`; flat ⟺ `k = 1`; then `v⁴ = GM a₀` |
| Theorem 2, the law | `muk_one` | `μ₁` is `ConstitutiveLaw.law`, the law of the AQUAL and BIMOND chains |
| Proposition 1 (b)–(d) | `necessity` | the bound-state law breaks (X), with root `(3 − √5)/2 ≠ ½` at `x = 1`; the standard and exponential functions break (X) |
| Proposition 2 | `prop2` | the node's weighted average and the series link; `g = μg + μa₀`, `(1 − μ)g = μa₀ < a₀`, increasing; missing/visible `= a₀/g`; a dilation-covariant swap is `E(1)/g` with one fixed pull `√E(1)` |
| Theorem 3 | `decode`, `letter_decode` | `M_dec/M_phot = (g + w)/(g + a₀)`, `ΔM/M_phot = (w − a₀)/(g + a₀)`; quiet ⟺ `w = a₀` ⟺ `g_bar = μg`; drive ⟺ `w > a₀` ⟺ TetB pulls more than `μa₀`; brake ⟺ `w < a₀`; the decode is `r v⁴/(G(a₀r + v²))` |
| Proposition 3 (i) | `burgers` | the derivatives as `HasDerivAt`, and `u_r ω' = α ω + ν(ω'' + ω'/r)` with `β = α/4ν` |
| Proposition 3 (ii) | `lamb_oseen` | the time derivative as `HasDerivAt`, the radial profile as a Burgers profile with `β = 1/4νt`, and `∂_t ω = ν(ω'' + ω'/r)` |

## 3. Not formalised

- **Theorem 2 (iv)** is not restated. Its content, that degree one with the endpoint and exchange closure gives the law, is `ConstitutiveLaw.unique_law`, imported by the chain. The script checks that `x^k` has no Möbius form for `k = 2, 3`.
- **Proposition 1 (a).** The counterexample's MOND limits need asymptotic analysis. The script checks the exchange exactly, and the limits and monotonicity on twelve decades.
- **Proposition 1 (e)**, the two branches of the degree-one relation, is a sympy coefficient comparison.
- **Proposition 3 (iii).** The core radius, the central vorticity at fixed circulation (an integral) and the far-field limit are checked by sympy and numerically.
- **The cube with its centre.** The explicit nine-site model of the Field Origin as one node is checked numerically. Its general reduction is `WalshEigenmodes.whole_cube`.

## 4. Notes for a referee

- **Real exponents.** Theorem 1 is proved with `Real.rpow`. The proof that (X) forces `m = p` uses only `x = 1`, where (X) gives `μ(1) = ½` and (S) gives `(½)^m = (½)^p`.
- **The deep field** is stated for the exact deep law `μ = x^k`, the leading behaviour of `μ_k` as `x → 0`. The full rotation curves for `k = ½, 1, 2, 3` are solved numerically in the script.
- **Physical premises.** These are the screening form, the chamber swap read as `x → 1/x`, and the strengths being accelerations. They enter as hypotheses (`Screens`, `Exchange`, and the identity in `strengths_are_accelerations`), never as axioms.
