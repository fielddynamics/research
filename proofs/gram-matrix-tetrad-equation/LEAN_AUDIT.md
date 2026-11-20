# Lean audit: The Gram Matrix of the Tetrad Equation

| | |
|---|---|
| **Formalisation** | [`lean/GramMatrixTetradEquation.lean`](lean/GramMatrixTetradEquation.lean), 904 lines, Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../tetrad-scheme-two-bounded-regions/lean/`](../tetrad-scheme-two-bounded-regions/lean/) (`P`, `η`, the quarter turn), [`../half-space-two-bounded-regions/lean/`](../half-space-two-bounded-regions/lean/) and [`../forced-tetrahedral-frame/lean/`](../forced-tetrahedral-frame/lean/) (`M₁`, `MᵀM`, `MMᵀ`), imported, not copied |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 21 `#print axioms` checks report only Lean's standard axioms (`levi_spec` uses only `propext`; the rest `propext`, `Classical.choice`, `Quot.sound`) |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-gram-matrix-tetrad-equation.yml`, on every change to this proof or any proof it imports |

**Verdict.** Every lemma, proposition and theorem is proved. Three statements are proved in a narrower form than the note states, listed in §3; no statement of the note was found to be wrong.

## 1. Definitions to check against the paper

| Lean | Paper |
|---|---|
| `M1 = Mmat` (imported), `M2 = −M1` | Eq. (2) and the second root |
| `gram U W = Uᵀ W`; `G = gram M1 M1`; `J 4` | `G_{UW}`, `G`, `J` |
| `Hhat`: `M1` with a row of ones on top | `Ĥ` |
| `omega a b c M = det(v_a, v_b, v_c)` | `ω_abc` |
| `corner v`: every entry `±1` | a corner of the cube `{±1}³` |
| `IsSymA L`: `LᵀL = 1` and `L` sends each `v_a` to some `v_b` | `Sym(TetA)` |
| `IsSymS L`: `LᵀL = 1` and `L` sends each `v_a` to some `±v_b` | `Sym(S)` (a linear map sending the four `v_a` into `S` sends `−v_a` into `S` too) |
| `Idx = Fin 4 × Fin 4 × Fin 4`, `(λ, μ, ν)` | index of `Γ^λ_{μν}` |
| `tau`, `Pplus = ½(1 + τ)`, `torsion = 1 − τ`, `oddPart = ker(1 + τ)` | `τ`, `Π₊`, `T`, the `τ`-odd part |
| `lower g D (λ,μ,ν) = Σ_s g_{λs} D^s_{μν}` | lowering the first index |
| `compat g`: `D` with `(lower g D)_{λμν} + (lower g D)_{νμλ} = 0` | the difference of two `g`-compatible connections |
| `gammaOf e de ω`: `(e⁻¹(∂_μ e + ω_μ e))^λ_ν`, with `de μ = ∂_μ e` at the point | `Γ` of Proposition 2 |
| `IsLorentzConn ω`: `η ω_μ` antisymmetric | Lorentz connection |
| `frameTorsion e de ω` | `T^a_{μν}` of Proposition 3(i) |
| `levi a b c d = sign ∏_{i<j}(x_j − x_i)`; `levi_spec` | the Levi-Civita symbol: `ε_{0123} = 1`, antisymmetric in every adjacent pair (hence totally) |
| `dualT vol gi T`, `axial vol gi g T`, with `vol = det e`, `gi = g⁻¹` | `⋆T` and `A` |

## 2. Statements

| Paper | Lean | Notes |
|---|---|---|
| Lemma 1 | `lemma1` | |
| Lemma 2 | `lemma2` | Including: each product depends only on same/opposite root |
| Lemma 3 | `lemma3` | `ĤĤᵀ = 4I` by computation; `ĤᵀĤ = 4I` derived via the inverse, as in the paper |
| Lemma 4 | `lemma4` | Projections; `Gx = 0` iff `x` constant; `Gx = 4x` iff `Σx = 0`; `GM₁ᵀ = 4M₁ᵀ`; rows independent; cross-coupling `−G` |
| Lemma 5 | `lemma5` | Invariance; rigidity with `∃!`, `Q = ¼WM₁ᵀ`; `Q = −I` for `M₂`. Proved directly (`W1 = 0` from `‖W1‖² = 1ᵀG1 = 0`) |
| Proposition 1 | `prop1` | All 24 ordered distinct triples nonzero; `ω(QM) = det Q · ω(M)`; reversal |
| Theorem 1 | `theorem1` | Columns of `M₁` = corners with `xyz = +1` exactly; `M₂` with `xyz = −1`; edges `8`; centred; disjoint |
| Theorem 2 | `realise_perm`, `induced_perm`, `symA_card`, `theorem2`, `quarter_turn_exchanges` | Every permutation realised by exactly one `L`; `|Sym(TetA)| = 24`; `IsSymS L ↔ IsSymA L ∨ IsSymA (−L)`, never both; `|Sym(S)| = 48`; non-TetA elements carry TetA onto TetB; `−I` central; the quarter turn is an exchanging rotation |
| Eq. (6) | `grid` | `24 + 16 + 24 = 64` |
| Lemma 6 | `lemma6` | `τ² = 1`; diagonal fixed; triangles exchanged; `Π₊² = Π₊`; range = `τ`-even; kernel = `τ`-odd = torsions; `finrank ker = 24`, `finrank range = 40` |
| The two cautions | `cautions` | `τ` commutes with relabelling; reversal swaps triangles; symmetric (inhomogeneous) terms have zero torsion |
| Theorem 3(i) | `theorem3_i` | `T = 0` iff in range of `Π₊`; `Π₊` not injective |
| Theorem 3(ii) | `theorem3_ii` | Every invertible `g`: torsion map injective and onto the torsions, contorsion `½(T_{λμν} + T_{νλμ} + T_{μλν})` as inverse; `finrank = 24` |
| Theorem 3(iii) | `theorem3_iii` | Two `g`-compatible connections with equal torsion are equal |
| Proposition 2 | `prop2` | (a) `PωP` Lorentz and `Γ` unchanged; (b) a boost generator: both connections `η`-compatible, torsions differ |
| Proposition 3 | `prop3` | (i) frame torsion becomes `P` times itself, coordinate form unchanged and equal to the torsion of `Γ`; (ii) `det(Pe) = −det e`, `⋆T` and `A` reverse for every `g`, `⋆T = 0 ⇒ T = 0` at `g = η`, `vol ≠ 0`; (iii) `Alt(lower g T) = 2 Alt(lower g Γ)`, `Alt(lower g (Π₊Γ)) = 0` |

## 3. Narrower than the note

- **`⋆T ≠ 0` (Proposition 3(ii)).** The note argues `⋆⋆ = −1` for any Lorentzian `g`. Lean proves injectivity at `g = η` (the frame metric at a point), by computing all six components; the sign reversal is proved for every `g`.
- **Normal coordinates (Proposition 3(iii)).** "A torsion-free connection has no tensor at first order" is a statement about calculus on manifolds and is not formalised. The algebraic half, the totally antisymmetric part, is.
- **Compatibility in Proposition 2.** The note states that `Γ` built from a Lorentz `ω` is compatible with `g = eᵀηe`; this involves derivatives of `g` and is not formalised in general. For the example in (b) (constant frames), both connections are proved `η`-compatible.

## 4. Notes for a referee

- **Pointwise.** As the note says, all statements in Parts III–IV are pointwise; derivatives `∂_μ e` enter only as given matrices `de μ`.
- **`Sym(S)` as a product.** Lean proves the set equation `Sym(S) = Sym(TetA) ∪ −Sym(TetA)` with the union disjoint and `−I` central, which is the content of `Sym(TetA) × {±I}`.
- **Labels.** "TetA", "TetB", "upper triangle = TetA" are the framework's readings; the theorems hold whatever the labels, as the note says.
