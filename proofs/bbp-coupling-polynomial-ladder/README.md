# The BBP Formula and the Coupling Polynomial on One Ladder

*How the BBP formula for π and GFD's coupling polynomial meet at the Field Origin · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`BBP-formula` `cyclotomic-polynomials` `coupling-polynomial` `Field-Origin` `stellated-octahedron` `proof`

---

This folder holds a four-page proof in two parts, a script that checks every step (46 checks), and an independent blind test of Part II (9 checks, in [`extensions/`](extensions/)). The checks use exact algebra, with 40-digit numerics only where a logarithm's branch or an integral's value has to be fixed. The proof places the Bailey–Borwein–Plouffe (BBP) formula for π and GFD's coupling polynomial f(K, s) = 1 + sK + K² on one ladder of cyclotomic polynomials, and shows exactly where they meet.

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

## Part II: the dictionary and the ladder

### Result 4: the rung dictionary (Theorem 6)

BBP's eight slot series evaluate to combinations of seven constants. For each constant the formulas again form a one-parameter family, and each family must use exactly the pole pairs whose arithmetic it contains. All seven formulas are checked exactly, not numerically: for example ln 3 = 2S₂ + ½S₆ and arctan(1/2) = S₂ − ¼S₆.

| Pole pair | Its number 1 − ω̄/√2 | Constants whose formulas must use it |
|---|---|---|
| 0°, 180° | real, involving the unit 1 + √2 | √2 ln(1 + √2) |
| 45°, 315° | (1 ± i)/2, argument π/4 | π, arctan(1/2) |
| 90°, 270° (Field Origin, Φ₄) | (√2 ± i)/√2, norm 3/2 | ln 3, √2 arctan(1/√2) |
| 135°, 225° | (1 ± i)(2 ∓ i)/2, norm 5/2 | ln 5, arctan(1/2) |

So π and ln 3 are complementary. Every formula for π drops the Field Origin pair, and every formula for ln 3 uses it.

### Result 5: π lives on one rung (Theorem 7)

The member r = −1/4 of the π family is the classical base −4 formula, π = Σ(−1/4)ᵏ[2/(4k+1) + 2/(4k+2) + 1/(4k+3)].
- **It is the only member with no ±√2 poles.**
- **Its whole integrand is 4/(y² − 2y + 2),** so π = 4 arctan 1 is read from the 45° half of Φ₈ alone.
- **Its natural denominator is one rung:** 4 + y⁴ = 4Φ₈(u).

BBP is the same π spread over the period-8 ladder. Its extra ±√2 poles contribute −ln 4, and closure fixes the member.

### Result 6: the rungs carry the Field Origin column (Lemma 2, Theorem 8)

At BBP's own point 1/√2 the rungs take the values

$$2^{2^{k-2}}\,\Phi_{2^k}(1/\sqrt2) = F_{k-2} = \Phi_4\big(K^{2^{k-4}}\big),$$

the Fermat numbers 3, 5, 17, 257, 65537. These are exactly the Field Origin column of the ladder, read at X = K^(1/4), K^(1/2), K, K², K⁴.
- **The rung Φ₁₆ carries the Field Origin's own value,** f(K, 0) = 17.
- **The primes 3 and 5 of Result 2 are the Field Origin values one and two levels below the photon.** Of the two:
  - 5 = K + 1 holds for every K;
  - 3 = √K + 1 equals D = K − 1 only at K = 4.
- **For k ≥ 4 each rung's poles form one Galois orbit,** so every pole on the rung has this norm. At k = 3 the orbit is only half the rung, which is why Φ₈ splits into its 45° and 135° halves.

### Result 7: climbing the ladder adds nothing (Theorem 9)

Generalise BBP's type to base 2^(2^(m−1)) and period 2^m. The poles stay at radius √2.
- **Every prime factor of F_(k−2) is ≡ 1 mod 2^k** (Euler–Lucas), so it splits completely.
- **So each new rung's poles carry private primes,** and by Baker's theorem every formula for π must drop them.
- **What remains is the period-8 integrand,** so the formulas for π are the same one-parameter family at every level.

This is proved for periods 16, 32 and 64, where F₂, F₃ and F₄ are prime. Beyond that it rests on each Fermat number having a prime factor to the first power, which is not known in general.

The blind test in [`extensions/`](extensions/) searches by lattice reduction without using the theorem. At each of the three periods it finds exactly two integer relations among π and the slot series, both in the lifted family, with nothing else below coefficients of about 10²².

## Why it matters

- **It gives the BBP connection a structural place.** The coupling polynomial reads the photon's level across its three states. BBP reads down the Field Origin column, drops the photon's own Field Origin, and takes π from the level above.
- **It explains a cancellation that was only recorded.** PROOF.md's extension test 18 lists which poles BBP's numerator cancels. This proof says why: the primes 3 and 5.
- **It locates the labelling.** The place-value reading of slots as cube corners is the binary coordinate system of the ladder's rungs.
- **It ties BBP's primes to the Field Origin.** The primes that block π on each rung are the Field Origin column read down the ladder. The first one above the photon's own level is 17, and no formula for π can use the rung that carries it.

## What it does not do

- **It does not show that BBP is the stellated octahedron.** No symmetry of the stellated octahedron has order 8: its 48 symmetries have orders 1, 2, 3, 4 and 6, and its 8 points form ℤ₂³, not BBP's ℤ₈. The ladder places BBP's period one rung up instead.
- **The formula type is an input.** Base 16 = K², period 8 = 2^D and first-power denominators are taken from PROOF.md. The Lemma shows only that this is the type whose poles reach 1 + i.
- **Some choices are left open.** The ladder fixes which bit is which rung, but not which spatial axis carries which bit. It also leaves open whether a slot is counted as j or j − 1, which does matter.
- **The primes get only the meaning Theorem 8 gives them.** They are the Field Origin values below the photon's level. Reading 3 as D works only because K = 4.
- **Theorem 9 beyond period 64 is conditional.** It needs each Fermat number to have a prime factor to the first power.

## Correction

The first version of this proof (commit b128fb4) printed the cancelled integrand of Theorem 5 with the wrong sign. The correct integrand is 16[(y − 1) − r(y² − 4y + 2)]/((y² − 2)(y² − 2y + 2)). The numerators in Theorem 4 were right. The script had accepted either sign; it now checks the sign strictly. The error came to light when the period-16 search was compared with the lifted family.

## Contents

| File | Contents |
|---|---|
| [`bbp_coupling_polynomial_ladder.pdf`](bbp_coupling_polynomial_ladder.pdf) | The proof, four pages: Part I (Theorems 1–5) and Part II (Theorems 6–9) |
| [`bbp_coupling_polynomial_ladder.tex`](bbp_coupling_polynomial_ladder.tex) | LaTeX source (IOP journal class, included) |
| [`verify_bbp_coupling_polynomial_ladder.py`](verify_bbp_coupling_polynomial_ladder.py) | Checks of every theorem, the lemma, the corollary and the remarks: the cyclotomic identities, the ladder, the denominator's factorisation, the binary coordinates and turns, the logarithm at every pole, the divisibility and exact numerators of the whole family, the two remaining integrals, the TIME and closure conditions; Part II: the seven formulas of the dictionary checked exactly through the logarithm expansion, the dictionary table, the base −4 formula, the Galois orbits and norms of the rungs at k = 3 to 6, the Fermat values, Euler–Lucas, and the lifted family at periods 16, 32 and 64 |
| [`extensions/`](extensions/) | Blind lattice-reduction test of Theorem 9 at periods 16, 32 and 64 (needs fpylll) |
| [`iopjournal.cls`](iopjournal.cls) | Document class, so the source builds here |

```bash
pip install sympy mpmath
python verify_bbp_coupling_polynomial_ladder.py      # 46/46
python extensions/test_ladder_invariance_lll.py      # 9/9 (pip install fpylll cysignals)
pdflatex -interaction=nonstopmode bbp_coupling_polynomial_ladder.tex
```

## Related

- [`research/bbp and pi field closure stepping/`](../../research/bbp%20and%20pi%20field%20closure%20stepping/): the BBP synthesis, the cyclotomic note and the count over all slot labellings.
- PROOF.md in the model repository (`dfp-gravity-field-model`, branch `test/bbp-octahedron-hypothesis`, `gravity_field_model/engine_core/field_closure/bbp_structure/`): the one-parameter family (Theorem 2) and the TIME-axis selection (Theorem 3).
- [The Stellated Octahedron, the Cube and the Hadamard Matrix](../hadamard-cube-frame/): the meaning of 2(D+1) = 2^D.
- [`coupling-algebra/`](../../research/coupling-algebra/), Result 13: f(K, s) as the characteristic polynomial of the cube's rotations.

---

*The algebra is exact and machine-checked. The reading of the ladder in terms of TetA, TetB and the Field Origin is GFD's, stated so that it can be tested.*
