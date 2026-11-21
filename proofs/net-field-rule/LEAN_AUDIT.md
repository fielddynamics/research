# Lean audit: The Net-Field Rule

| | |
|---|---|
| **Formalisation** | [`lean/NetFieldRule.lean`](lean/NetFieldRule.lean), 348 lines, Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../constitutive-law-tug-of-war/lean/`](../constitutive-law-tug-of-war/lean/) (`Exchange`) and [`../constitutive-law-exchange-symmetry/lean/`](../constitutive-law-exchange-symmetry/lean/) (`law`); imported, not copied |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 20 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-net-field-rule.yml`, on every change to this proof or any proof it imports |

**Verdict.** Theorem 1 (except the vacuum divergence for general configurations), Corollary 1, Proposition 1 (b)–(c), Proposition 2 (a)–(b), Theorem 2 (b)–(e) and Proposition 4 (a) are proved. Theorem 2 (a), Propositions 2 (c), 3, 4 (b)–(c) and 5, the vacuum divergence and the vortex remark are checked by the script.

## 1. Definitions to check against the paper

| Lean | Paper |
|---|---|
| `drained a g` | the drained law (1), `g_t = (g + √(g² + 4ga₀))/2` |
| `gN a t` | its inverse, `g_N = g_t²/(g_t + a₀)` |
| `mu` | `ConstitutiveLaw.law`, `x/(x + 1)` |
| `TugOfWar.Exchange μ` | the exchange `μ(x⁻¹) = 1 − μ(x)` for all `x > 0` |
| `tophat G M l r` | the pointer's field: a uniform ball of mass `M` and radius `l` |

## 2. Statements

| Paper | Lean | Notes |
|---|---|---|
| (1) | `drained_inverts` | `g_N(F(g)) = g` and `μ(F(g)/a₀) F(g) = g` |
| Theorem 1, the dictionary | `dictionary` | `x = m/(1 − m)`; `ν(xm) = 1/2 + √(1/4 + 1/(xm)) = 1/m`; `dg_t/dg_N = 1/(m(2 − m))`; the log-degree `1/(2 − m)` |
| Theorem 1, the four faces | `four_faces` | for `m ∈ (0, 1]` each defect is zero iff `m = 1` |
| Theorem 1 (i) | `subadditive` | `F(b + c) < F(b) + F(c)` for `b, c > 0` |
| Theorem 1 (ii) | `response_not_identity` | `1/μ > 1` and `1/(μ(2 − μ)) > 1` for every `x > 0` |
| Theorem 1 (iii) | `gN_deriv`, `flux_exponent` | `g_N'` as `HasDerivAt`, its log-degree `2 − μ`, and `s = 2 − 2/(2 − μ) = 2(1 − μ)/(2 − μ)`, slope `−μ/(2 − μ)` |
| Corollary 1 | `involution`, `involution_singles_out` | `f(f(u)) = u` for `u ≠ 2`; for `n = 2`, `f₂(f₂(3/10)) ≠ 3/10` |
| Proposition 1 (b)–(c) | `sun_screening` | `x(1 − μ) = μ`, `1 − μ = 1/(1 + x)`, the core radius, and the screened mass below `a₀R²/G` |
| Proposition 2 (a) | `tail_bounds` | `a₀g/(g + a₀) ≤ F(g) − g < a₀` |
| Proposition 2 (b) | `tail_forced` | for any `μ` with `Exchange` and `μ(u)/u → 1` as `u → 0⁺`, `x(1 − μ(x)) → 1` as `x → ∞` |
| Theorem 2 (b) | `sheet_vanishes_outside`, `sheet_continuous` | the sheet's own term is zero for `r ≥ l`, continuous at `l`, and `GM/r² − GMr/l³` inside |
| Theorem 2 (c) | `free_fall`, `com_free_fall` | in any additive group; in any real module with antisymmetric forces over `Fin n` |
| Theorem 2 (d) | `no_self_force` | in any real module, for any linear `R`, `∑ mᵢ R(k(pᵢ − c)) = 0` when `c` is the centre of mass |
| Theorem 2 (e) | `flat_tide`, `jacobi` | `Φ'` and `Φ''` as `HasDerivAt`; `κ² = 2Ω²`; `GM/r_J³ = 2Ω²` |
| Proposition 4 (a) | `kepler_absorbs` | Kepler's period with `G/μ` and `M` equals that with `G` and `M/μ` |

## 3. Not formalised

- **Theorem 1 (iii), vacuum divergence for general configurations.** Proved for the sum of two point fields with sympy, and checked numerically for the drained field at random points.
- **Theorem 2 (a).** The pointer projection's idempotence, nesting and mass conservation are checked on explicit point sets, and the multipole expansion with sympy.
- **Proposition 2 (c).** The Cassini quadrupole is a numerical integral of the phantom density.
- **Propositions 3, 4 (b)–(c) and 5** use data (Cassini, the cluster and dwarf dispersions, SPARC) and numerical estimators.
- **The vortex remark.** Galilean invariance, Burgers and Lamb–Oseen are checked with sympy; Burgers and Lamb–Oseen are also proved in the tug-of-war formalisation.

## 4. Notes for a referee

- **Premises.** The drain criterion and the net-field rule enter as the choice of which term goes through `drained` and which stays linear. In Lean this is the content of `free_fall`, `no_self_force` and `sheet_vanishes_outside`, which hold for any host response; nothing is assumed as an axiom.
- **`tail_forced`** is stated for every exchange-symmetric law, not just `x/(x + 1)`, which is why the per-mass reading fails for all of them.
- **`no_self_force`** is proved in an arbitrary real module with an arbitrary linear map, so it covers the anisotropic response of Theorem 1 (ii) and any other.
