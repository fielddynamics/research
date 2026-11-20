# Lean audit: The Sixteen Half-Space Regions of the Tetrad Frame

| | |
|---|---|
| **Formalisation** | [`lean/HalfSpaceTwoBoundedRegions.lean`](lean/HalfSpaceTwoBoundedRegions.lean), 586 lines, Lean 4.36.0 + Mathlib v4.36.0 |
| **Depends on** | [`../forced-tetrahedral-frame/lean/`](../forced-tetrahedral-frame/lean/) (imported, not copied): the four directions are the columns `Mcol a` of its matrix `M` |
| **Build** | 0 errors · 0 warnings · no `sorry` / `admit` / custom `axiom` / `native_decide` |
| **Axioms** | All 14 `#print axioms` checks report only `propext`, `Classical.choice`, `Quot.sound` |
| **Reproduce** | `cd lean && lake exe cache get && lake build` |
| **CI** | `.github/workflows/lean-half-space-two-bounded-regions.yml`, on every change to this proof or the one it imports |

**Verdict.** Every mathematical statement of the note is proved. The mixed-selection argument, which the letter gives in words for one flip, is proved for all fourteen mixed selections.

## 1. Definitions to check against the paper

A Lean proof can only be wrong in its statements, so these are what a referee should read.

| Lean | Paper |
|---|---|
| `proj a p = Mcol a ⬝ᵥ p`; `proj_formulas` | `v_a`; the four formulas `x+y+z`, `x−y−z`, `−x+y−z`, `−x−y+z` |
| `sgn s a` (`+1` if `s a`, else `−1`); `region s = {p ∣ ∀ a, sgn s a · v_a(p) ≤ 1}`, `s : Fin 4 → Bool` | one half-space per projection; the `2⁴ = 16` selections (`sixteen`) |
| `TetA = region (all true)`, `TetB = region (all false)`; `mem_TetA`, `mem_TetB` | `max v_a ≤ 1`, `max (−v_a) ≤ 1` |
| `Bornology.IsBounded` (Mathlib) | bounded |
| `octVert (j, b) = ±ê_j` | the octahedron's six vertices |
| `face a = TetA ∩ {v_a = 1}`; `core a = face a ∩ TetB`; `corner a b = face a ∩ {−v_b > 1}`; `channel a b` (core if `b = a`, else corner) | the faces of TetA and their `3 + 1` pieces |

## 2. Statements

| Paper | Lean | Notes |
|---|---|---|
| `v₁ + v₂ + v₃ + v₄ = 0` | `proj_sum` | |
| "the sole algebraic relation" | `proj_relations` | A combination `Σ l_a v_a` vanishes identically iff all `l_a` are equal |
| TetA and TetB are bounded | `TetA_bounded`, `TetB_bounded` | Explicit bound `|x|, |y|, |z| ≤ 3` |
| Every mixed selection is unbounded | `mixed_direction`, `mixed_unbounded` | All 14 cases, ray `t·d`, `d = −Σ_{b∈S} n_b` |
| Exactly two of sixteen are bounded | `classification`, `exactly_two_bounded` | Bounded ⇔ all signs agree; the bounded set is `{TetA, TetB}`, of size 2 |
| TetA, TetB are tetrahedra; TetB is TetA reversed | `TetA_eq_hull`, `TetB_eq_hull`, `TetB_eq_neg_TetA` | Vertices `−n_a` and `n_a`, weights `(1 ∓ v_a)/4` |
| Each vertex passes through a face of the other | `interpenetration` | Through exactly one face, the opposite one |
| Intersection `{|v_i| ≤ 1}` is a regular octahedron | `inter_eq_octahedron`, `inter_eq_hull_octVert`, `octahedron_regular` | `= {|x|+|y|+|z| ≤ 1}` `=` hull of `±ê_j`; edges between non-opposite vertices have squared length 2, and there are 12 of them (24 ordered pairs) |
| `4 × 4 = 16` channels | `channels` | Per face: the four channels cover it, are pairwise disjoint, non-empty and convex |
| Structural inventory | `inventory` | 8 distinct vertices `= 2³`, `12 = 4·3` edges, `8 = 2·4` faces, `16 = 4²`, `28 = 4(4+3)`, `V − E + F = 4` |
| `3 + 1` face-normal pattern | `three_plus_one` | One normal `(+,+,+)`, three mixed; TetB's uniform normal is `(−,−,−)` |

## 3. Notes for a referee

- **Connected channels.** The letter calls each channel "a distinct connected region". Lean proves each is convex, which implies connected, and non-empty, and that the four on each face are disjoint and cover it.
- **Edges and faces of the inventory.** Counted as 2- and 3-element subsets of each tetrahedron's vertex set, which is exact for a tetrahedron (every pair of vertices is an edge, every triple a face); the vertex sets are the hull vertices of `TetA_eq_hull` and `TetB_eq_hull`.
- **Euler sum.** `V − E + F = 4` is arithmetic on the counts; the reading "twice the Euler characteristic of a sphere" is the letter's interpretation and is not formalised.
- **Names.** "Stellated octahedron", "stella octangula" and "Sierpiński subdivision" are names. Lean proves the content: the union of the two tetrahedra whose intersection is the regular octahedron, and the `3 + 1` pieces of each face.
- **Physics.** That the four planes come from the tetrad is the [forced tetrahedral frame](../forced-tetrahedral-frame/) result, imported here; the `(−,+,+,+)` reading of the `3 + 1` pattern is the letter's interpretation.
- **Not formalised.** The four-million-point rendering (Figure 1), which is illustration; its code is Letter 1's `fig1_tetrad_frame.html`. The script's extra check that the octahedron's vertices are edge midpoints of both tetrahedra is not a claim of the note.
