# The BBP Formula and the Coupling Polynomial on One Ladder

*How the BBP formula for π and GFD's coupling polynomial meet at the Field Origin · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`BBP-formula` `cyclotomic-polynomials` `coupling-polynomial` `Field-Origin` `stellated-octahedron` `proof`

---

This folder holds a three-page proof and a script that checks every step. The checks use exact algebra, with 40-digit numerics only where a logarithm's branch or an integral's value has to be fixed. The proof places the Bailey–Borwein–Plouffe (BBP) formula for π and GFD's coupling polynomial f(K, s) = 1 + sK + K² on one ladder of cyclotomic polynomials, and shows exactly where they meet.

## The ladder

The cyclotomic polynomial Φₙ is the minimal polynomial of a rotation by 1/n of a turn.
- **The coupling polynomial is three of them at K:** f(K, +1) = Φ₃(K), f(K, 0) = Φ₄(K) and f(K, −1) = Φ₆(K), giving TetA 21, the Field Origin 17 and TetB 13.
- **The ladder squares K at each level.** Squaring the variable sends Φ₃ to Φ₃Φ₆, Φ₄ to Φ₈ and Φ₆ to Φ₁₂.

So the coupling polynomial is one row of this table, and the Field Origin runs down its middle column:

| Ladder level | K | TetB Φ₆ | Field Origin Φ₄ | TetA Φ₃ |
|---|---|---|---|---|
| −1 | 2 | 3 | 5 | 7 |
| 0 (the photon) | 4 | 13 | 17 | 21 |
| +1 | 16 | 241 | 257 | 273 |

The cyclotomic form and the ladder are already in the [archive](../../research/exploratory/great-pyramid/pyramid_portal_research/01_framework_foundations/01.1_cyclotomic_algebra.md). Theorem 1 restates them as the frame for the rest.

## Result 1: BBP lies on the Field Origin column (Theorems 2 and 3)

BBP is the integral of p(y)/(16 − y⁸) over [0, 1]. Write y = √2·u. The denominator becomes

$$16 - y^8 = 16\,(1-u)(1+u)(1+u^2)(1+u^4).$$

- **The rungs are the Field Origin column.** The three factors 1 + u, 1 + u², 1 + u⁴ are Φ₂, Φ₄ and Φ₈: the Field Origin polynomial at three consecutive ladder levels, which take the values 5, 17 and 257 at K = 4.
- **The TetA and TetB columns are absent.** Neither Φ₃ nor Φ₆ divides the denominator.
- **Why this ladder.** The base 16 and period 8 put the poles at radius √2, so that they include 1 + i. This happens exactly when 2(D+1) = 2^D (the Lemma).
- **The rungs are the cube's binary coordinates.** (1 + u)(1 + u²)(1 + u⁴) = 1 + u + … + u⁷, with each exponent m = 4b₂ + 2b₁ + b₀ arising once. So the 8 terms are the 8 cube corners by place value, one rung per axis.
- **The rungs are turns.** On the poles, the three bits are the half-turn (−1), the quarter-turn (i) and the eighth-turn. This place-value reading is the one PROOF.md uses to label BBP's slots by cube corners.

## Result 2: every formula for π drops the coupling row's rung (Theorem 4)

The formulas for π of BBP's type are exactly BBP + r·a, a one-parameter family (proved in PROOF.md with Baker's theorem). Every one of them has a numerator divisible by (y² + 2)(y² + 2y + 2):

$$p = 16\,(y^2+2)(y^2+2y+2)\,\big[r\,(y^2-4y+2) - (y-1)\big].$$

- **y² + 2 is 2Φ₄(u),** the Field Origin rung at the coupling row's own level, 17.
- **y² + 2y + 2 is one half of Φ₈,** the half with poles at 135° and 225°.

The reason is arithmetic. Each pole contributes the logarithm of 1 − ω̄/√2. Over the Φ₄ pair these multiply to 3/2, and over the 135° pair to 5/2. Their logarithms involve the primes 3 = (√2 + i)(√2 − i) and 5 = (2 + i)(2 − i), and by Baker's theorem such logarithms can never combine into π. So every formula for π must vanish at those poles. This is forced on the whole family; it is not something BBP does in particular.

## Result 3: π is read one rung up (Theorem 5 and the Corollary)

- **What remains** after the cancellation are the poles ±√2, which give only real logarithms, and 1 ± i, on the other half of Φ₈. For BBP the 1 ± i part integrates to π + ln 4 and the ±√2 part to −ln 4.
- **So π comes from Φ₈ = Φ₄(X²),** the Field Origin one ladder level above the photon (257).
- **What selects BBP.** In the last factor, the TIME slot w₇ is the y⁶ coefficient, 16r, and the weights sum to −15r. So silence on the TIME axis and closure (weights summing to zero) are each the condition r = 0, which is BBP. BBP's factor (y − 1) is the closure condition.

## Why it matters

- **It gives the BBP connection a structural place.** The coupling polynomial reads the photon's level across its three states. BBP reads down the Field Origin column, drops the photon's own Field Origin, and takes π from the level above.
- **It explains a cancellation that was only recorded.** PROOF.md's extension test 18 lists which poles BBP's numerator cancels. This proof says why: the primes 3 and 5.
- **It locates the labelling.** The place-value reading of slots as cube corners is the binary coordinate system of the ladder's rungs.

## What it does not do

- **It does not show that BBP is the stellated octahedron.** No symmetry of the stellated octahedron has order 8: its 48 symmetries have orders 1, 2, 3, 4 and 6, and its 8 points form ℤ₂³, not BBP's ℤ₈. The ladder places BBP's period one rung up instead.
- **The formula type is an input.** Base 16 = K², period 8 = 2^D and first-power denominators are taken from PROOF.md. The Lemma shows only that this is the type whose poles reach 1 + i.
- **Some choices are left open.** The ladder fixes which bit is which rung, but not which spatial axis carries which bit. It also leaves open whether a slot is counted as j or j − 1, which does matter.
- **No GFD meaning is given to the primes 3 and 5.** Reading them as D = 3 and K + 1 = 5 would need its own argument.

## Contents

| File | Contents |
|---|---|
| [`bbp_coupling_polynomial_ladder.pdf`](bbp_coupling_polynomial_ladder.pdf) | The proof, three pages |
| [`bbp_coupling_polynomial_ladder.tex`](bbp_coupling_polynomial_ladder.tex) | LaTeX source (IOP journal class, included) |
| [`verify_bbp_coupling_polynomial_ladder.py`](verify_bbp_coupling_polynomial_ladder.py) | Checks of every theorem, the lemma, the corollary and the remarks: the cyclotomic identities, the ladder, the denominator's factorisation, the binary coordinates and turns, the logarithm at every pole, the divisibility and exact numerators of the whole family, the two remaining integrals, and the TIME and closure conditions |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy mpmath
python verify_bbp_coupling_polynomial_ladder.py      # 32/32
pdflatex -interaction=nonstopmode bbp_coupling_polynomial_ladder.tex
```

## Related

- [`research/bbp and pi field closure stepping/`](../../research/bbp%20and%20pi%20field%20closure%20stepping/): the BBP synthesis, the cyclotomic note and the count over all slot labellings.
- PROOF.md in the model repository (`dfp-gravity-field-model`, branch `test/bbp-octahedron-hypothesis`, `gravity_field_model/engine_core/field_closure/bbp_structure/`): the one-parameter family (Theorem 2) and the TIME-axis selection (Theorem 3).
- [The Stellated Octahedron, the Cube and the Hadamard Matrix](../hadamard-cube-frame/): the meaning of 2(D+1) = 2^D.
- [`coupling-algebra/`](../../research/coupling-algebra/), Result 13: f(K, s) as the characteristic polynomial of the cube's rotations.

---

*The algebra is exact and machine-checked. The reading of the ladder in terms of TetA, TetB and the Field Origin is GFD's, stated so that it can be tested.*
