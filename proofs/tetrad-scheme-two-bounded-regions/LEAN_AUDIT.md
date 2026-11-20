# Lean audit: The Tetrad Scheme and the Two Bounded Regions

| | |
|---|---|
| **Formalisation** | [`lean/TetradScheme.lean`](lean/TetradScheme.lean), 586 lines, Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../half-space-two-bounded-regions/lean/`](../half-space-two-bounded-regions/lean/) (Route 1: TetA, TetB, the projections) and [`../forced-tetrahedral-frame/lean/`](../forced-tetrahedral-frame/lean/) (the four directions), imported, not copied |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 26 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-tetrad-scheme.yml`, on every change to this proof or either proof it imports |

**Verdict.** Every statement of the note is proved, except two standard facts that the note cites and Mathlib does not contain: that `SO(4, ℂ)` is connected (Borel), and that `O(1,3)` has four connected components (Wald). The split into two roots is proved for real tetrads, not as a statement about schemes.

## 1. Definitions to check against the paper

| Lean | Paper |
|---|---|
| `etaR R = diag(−1, 1, 1, 1)` over a commutative ring `R`; `eta = etaR ℝ` | `η` |
| `IsTetrad g e : eᵀ * η * e = g` | Eq. (1); row `a` of `e` is the leg `e^a` |
| `IsLorentz Λ : Λᵀ * η * Λ = η` | `Λ ∈ O(1,3)`, i.e. `O(η)` |
| `kappa g = det g / det η` | `κ`, Eq. (2) |
| `Xplus g`, `Xminus g`: solutions with `det e = +√κ`, `−√κ` | `X₊`, `X₋` (as sets of real tetrads) |
| `P = diag(1, −1, −1, −1)`, `T = diag(−1, 1, 1, 1)` | spatial parity, time reversal |
| `obs Q`: the 4×4 matrix `diag(1, Q)` | a frame change of one observer |
| `Rq`: the quarter turn about the third axis | "a 90° rotation about one axis" |
| `TetA`, `TetB`, `proj` (imported) | Route 1's regions and the projections `v_i` |

## 2. Statements

| Paper | Lean | Notes |
|---|---|---|
| `Λ e` is a solution for `Λ ∈ O(1,3)` | `lorentz_acts` | Any commutative ring |
| `(det e)² det η = det g`; every solution invertible | `det_sq`, `isUnit_det` | Any commutative ring, `det g` a unit |
| Solution space is one orbit; distinct `Λ`, distinct solutions | `orbit` (`∃!`), `solutions_eq_orbit` | Any commutative ring: the bijection `Λ ↦ Λ e₀`, i.e. `X_g ≅ O(η)` on points |
| `κ > 0` | `det_sq_kappa`, `kappa_pos` | Derived from the existence of a solution and `det g ≠ 0` |
| `X_g = X₊ ⊔ X₋` | `two_roots` | Union and disjointness |
| Each open and closed in `X_g` | `roots_clopen` | Each closed in `ℝ¹⁶`, and `X_g` cut by the open set `det e > 0` (resp. `< 0`) |
| A frame change multiplies `det e` by `det Λ = ±1`; it exchanges the roots iff `det Λ = −1` | `frame_change` | |
| `P`, `T` have `det = −1`; `PT = −I` has `det = +1` | `P_T` | Both Lorentz |
| Four components of `O(1,3)` | `time_component`, `four_classes` | Lean proves `Λ₀₀² ≥ 1` and that `I, P, T, PT` realise the four labels `(det, sign Λ₀₀)`; that each label is one connected piece is **cited** (Wald) |
| Holding the time leg fixed gives `diag(1, Q)`, `Q ∈ O(3)`, `det Λ = det Q` | `fixed_time_leg`, `obs_lorentz`, `obs_time_leg` | Both directions; `obs (−I) = P` |
| `P` is canonical: only `±I` commute with all of `O(3)`, only `−I` has `det −1` | `center_O3` | Uses two sign matrices and two transpositions, as the note says |
| Parity is not a rotation | `parity_not_rotation`, `no_rotation_is_parity` | Via `MMᵀ = 4I` (the directions span `ℝ³`) |
| Odd dimension: `det(−I) = (−1)^D` | `parity_odd_dimension` | Every `D` |
| `P` sends `v_i → −v_i`, maps TetA onto TetB; `−n_i` keep inner product `−1/3` | `parity_TetA_TetB` | Uses Route 1's `TetB_eq_neg_TetA` |
| Caution 1: congruent, not the same frame | `same_shape` | `Rq ∈ SO(3)` maps TetA onto TetB and `{−n_a}` onto `{n_a}`, but not leg by leg |
| Caution 2: `−e = PT e` keeps `det e` | `all_legs_reversed` | Spatial legs of `−e` are those of `P e`; its time leg is reversed |
| Both schemes present | `both_present` | `e ∈ X₊ ⇒ P e ∈ X₋` |
| Metric is root-blind | `metric_blind` | Any function `F` of the metric, any type of value |
| The metric cannot choose | `metric_cannot_choose` | No `F` with `F(eᵀηe) = det e` |
| Keeping one root adds an equation; `SO⁺` stays on one root | `one_root_is_a_restriction` | `X₊ ⊊ X_g`; `det Λ = 1` preserves `X₊` |
| Signature convention selects neither root | `signature_convention` | `η → −η`, `g → −g` leaves the Lorentz group and the solutions unchanged |
| `3 + 1` pattern, relative to the legs | `three_plus_one_relative` | `diag(n_a) ∈ SO(3)` permutes the normals and sends `n₀ ↦ n_a` |

## 3. Notes for a referee

- **Schemes.** The note defines `X_g = Spec ℝ[e]/(eᵀηe − g)`. Mathlib cannot yet express this scheme or its components, so Lean proves the content on points: over any ring for the orbit and the isomorphism with `O(η)`, over `ℝ` for the split. The claim that neither piece splits further is the cited connectedness of `SO(4, ℂ)`.
- **"Every quantity built from g".** Formalised in the strongest form available: any function of the metric, to any type. Christoffel symbols, curvature and the action are such functions at a point.
- **Time leg fixed.** Formalised as: `Λ e` has the same row 0 as `e` for every `e`, i.e. row 0 of `Λ` is `(1, 0, 0, 0)`; Lean derives that column 0 is too.
- **Names and physics.** "Scheme", "root" and "TetA/TetB" are names; that the second root is physical is the framework's claim, outside the note.
