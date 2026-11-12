# BBP Field Closure: Synthesis Document

> **Revised November 2026.** This note was written before the proofs in the model repository's [`bbp_structure/`](https://github.com/fielddynamics/dfp-gravity-field-model/tree/test/bbp-octahedron-hypothesis/gravity_field_model/engine_core/field_closure/bbp_structure) package (`PROOF.md`, 17 core tests, 29 extensions). The revision:
> - moves the uniqueness of BBP's active slots from "not proved" to "proved";
> - corrects Constraint B, which was false;
> - marks the constitutive-law reading as an interpretation;
> - points to the script that actually accompanies this folder.
>
> The general-reader account is [`BOOK_OF_CHANGES_AND_PI.md`](../exploratory/i-ching/BOOK_OF_CHANGES_AND_PI.md).

## The claim

The Bailey–Borwein–Plouffe formula for π has the structure of a closed reading of the stellated octahedron:
- its constants are the integers of GFD's selection equation;
- its active slots are four spatial corners, two in each tetrahedron, with the TIME axis silent;
- its weights sum to zero.

Since this note was first written, the central step has been proved. Among all formulas for π of BBP's type, the octahedron's TIME axis selects BBP uniquely.

---

## Background

The GFD covariant action is

$$S = \int d^4x \sqrt{-g} \left[ \frac{R}{16\pi G} - \frac{a_0^2}{8\pi G} F(y) - \frac{1}{4} e^{-2\Phi/c^2} F_{\mu\nu}F^{\mu\nu} + \mathcal{L}_m \right]$$

Its three prefactors, 16, 8 and 4, are $K^2$, $2^D$ and $K$ at $K = 4$, $D = 3$, the unique positive integer solution of the selection equation $2(D+1) = 2^D$. The stellated octahedron (two interlocking tetrahedra inscribed in a cube) has $8 = 2^D$ vertices, $K = 4$ faces per tetrahedron and $K^2 = 16$ face-coupling channels.

The Bailey–Borwein–Plouffe formula (1997) is

$$\pi = \sum_{n=0}^{\infty} \frac{1}{16^n} \left[ \frac{4}{8n+1} - \frac{2}{8n+4} - \frac{1}{8n+5} - \frac{1}{8n+6} \right].$$

It was found in pure number theory, with no geometric motivation. Its base is 16, its period is 8, its leading weight is 4, and it has 4 active slots per period: the same integers {16, 8, 4}.

---

## What is proved

### 1. The selection equation in three forms

**A. Dimensional selection.** $2(D+1) = 2^D$ has $D = 3$ as its only positive integer solution. This fixes $K = D + 1 = 4$, and then $K = 2^{D-1}$, so $\{K, 2^D, K^2\} = \{4, 8, 16\}$ are three consecutive powers of 2.

**B. Geometric ratio (corrected).** The original note stated that $K^3 = 2^{2D}$ has an integer solution only at $D = 3$. **That is false.** It has the solution $K = 2^{2D/3}$ whenever 3 divides $D$: $D = 3, 6, 9, \ldots$, ten solutions with $D \le 30$ (extension test 20). Only together with $K = D + 1$ does it give $D = 3$. So it is not an independent constraint.

**C. The BBP integral.** BBP's slot series are integrals over $1/(16 - y^8)$, whose poles lie at radius $16^{1/8} = \sqrt2$. Generalise to base $2^{D+1}$ and period $2^D$:
- the poles of $1/(2^{D+1} - y^{2^D})$ lie at radius $2^{(D+1)/2^D}$;
- that radius is $\sqrt2$, so the poles include $1 + i$, which produces π, exactly when $2(D+1) = 2^D$, i.e. only at $D = 3$;
- PSLQ finds no formula for π of this kind at $D = 1, 2, 4$ (extension test 23).

So A and C are not independent constraints that happen to agree. They are **one equation, read twice**:
- in GFD it says two simplices fill the cube's vertices;
- in BBP it says the integrand has the Gaussian pole $1 + i$.

That is a sharper statement than the original "triple lock".

### 2. The face-channel reading

Identify slot $j$ with the cube vertex labelled $j \bmod 8$ (3-bit encoding, bottom line most significant, the encoding fixed by the *I Ching*'s *Shuo Gua*). Exhaustive enumeration of the 70 four-element subsets of $\{0, \ldots, 7\}$ under five conditions:
- **chamber balance:** 2 vertices in TetA = {1, 2, 4, 7}, 2 in TetB = {0, 3, 5, 6};
- **TIME silence:** neither 0 nor 7 active;
- **spatial selectivity:** no TIME face penetrated;
- **weight balance:** weights {+4, −2, −1, −1} with chamber nets ±2;
- **pair pattern:** one fully active, two half-active and one silent complementary pair.

Exactly 6 subsets satisfy all five, forming one orbit under the spatial rotations. BBP's {1, 4, 5, 6} is one of them.

| Axis | Pair | Reading | Weight(s) |
|---|---|---|---|
| TIME | (0, 7) | silent | — |
| X | (1, 6) | double | V1: +4, V6: −1 |
| Y | (2, 5) | single | V5: −1 |
| Z | (3, 4) | single | V4: −2 |

**Which element of the orbit (now proved).** The original note said the choice of {1, 4, 5, 6} needs number theory and cannot come from the geometry. That is now settled:
- **Theorem 2** (`PROOF.md`): every formula for π of BBP's type (base 16, period 8, rational weights) is $w(r) = \text{BBP} + r\,(8, -8, -4, -8, -2, -2, 1, 0)$. The proof uses Baker's theorem. There are no others.
- **Theorem 3:** Kun's slot is silent in every one, and Qian's only at $r = 0$. **The TIME axis alone selects BBP from all formulas for π.** Its four slots, its 2 + 2 split and its zero sum then follow without being assumed.
- **Extension test 03:** of the 216 formulas with BBP's octahedral shape and magnitudes, only ±BBP evaluate to a single named constant, and that constant is π.

What remains an input is the identification of slot $j$ with vertex $j \bmod 8$. Counting the other way selects a different formula (extension test 07).

### 3. Weight balance as closure

The BBP weights {+4, −2, −1, −1}:
- sum to 0, the closure condition;
- have absolute sum $8 = 2^D$;
- split into chamber nets +2 (TetA) and −2 (TetB).

Their magnitudes {4, 2, 1} are the binary place values of three bits.

Theorem 6 (`PROOF.md`) recovers the rules that write these weights from the trigram lines, without assuming π. Among all affine readings meeting the structural conditions, only one gives a single named constant, and it gives π:
- the weight is $2\ell_b + \ell_m + \ell_t$;
- the step is $2\ell_t + 1$.

### 4. Hex–octal alignment

BBP works in base 16 (4-bit digits); the closure walk in base 8 (3-bit digits). Both read the same binary expansion of π, and the two frames realign every $\mathrm{lcm}(4, 3) = 12$ bits:
- $12 = K \times D$, the edge count of the stellated octahedron;
- each 12-bit window holds $K = 4$ octal digits and $D = 3$ hex digits.

The BBP ladder reaches every base-8 digit directly (core test `test_bbp_ladder_base8.py`; extension tests 13 and 14).

---

## An interpretation: the constitutive law

BBP's poles lie at radius $\sqrt2$, equivalently its integration limit is $1/\sqrt2 = 16^{-1/8}$. The original note read:
- $(1/\sqrt2)^2 = 1/2 = \mu(1)$, the GFD constitutive law $\mu(x) = x/(1+x)$ at the transition acceleration $x = 1$;
- $\mu(1)^{2^{D-1}} = 1/16 = 1/K^2$.

The arithmetic is correct, but the identification is an interpretation, not a derivation. The value 1/2 arises in many ways, and nothing in BBP refers to accelerations. It should be presented as a numerical correspondence.

---

## What is not proved

- **The class of readings.** Theorems 3 and 6 work within formulas of BBP's type and affine readings. Formulas or readings outside those classes are not covered.
- **That the walk singles out π.** The closure walk is π re-encoded: every step can be checked against the BBP formula on its own (`PROOF.md` §10). But its statistics are those of random digits, in pre-registered tests with a trials factor (extension tests 24 and 28). Ln 2, √2 and e also close the 64 hexagrams.
- **Isomorphism.** BBP's operations (digit extraction, series, polylogarithms) do not map onto GFD's (field equations, variational limits, constitutive law). The connection is shared structure, not an operation-preserving map.
- **Physics.** Nothing here shows that the gravitational field is the stellated octahedron. The mathematics holds whether or not GFD is right.

---

## Precise formulation

> **Theorem.** Let $D$ be the unique positive integer with $2(D+1) = 2^D$, and $K = D + 1$. Then:
>
> 1. $D = 3$, $K = 4 = 2^{D-1}$, and $\{K, 2^D, K^2\} = \{4, 8, 16\}$ are consecutive powers of 2.
> 2. The BBP formula has base $K^2$, period $2^D$ and leading weight $K$.
> 3. In base $2^{D+1}$, period $2^D$, the integrand's poles include $1 + i$ (the source of π) only when $2(D+1) = 2^D$.
> 4. Every formula for π of BBP's type is $\text{BBP} + r\,a$, with $a = (8, -8, -4, -8, -2, -2, 1, 0)$ (Theorem 2).
> 5. Reading slot $j$ as vertex $j \bmod 8$, exactly one of these leaves the TIME axis silent. It is BBP, with active slots {1, 4, 5, 6}, split 2 + 2 across the tetrahedra, and weights summing to zero (Theorem 3).

> **Corollary.** BBP's weights close (sum 0), have absolute sum $2^D$, and split ±2 across the chambers: the closure conditions of the octahedral reading.

---

## Deflated claims

- **Constraint B** ($K^3 = 2^{2D}$ "only at D = 3") is false; see §1.
- **"Three independent locks."** A and C are the same equation; B is not independent.
- **The coupling triple {13, 17, 21} among BBP denominators** is statistically unsurprising. About 25% of triples spaced by 4 land among BBP denominators, and other spacings appear too.
- **The ring surjection** $\mathbb Z[x]/(x^8 - 1) \to \mathbb Z[s]/(s^2 - 1)$ exists for every even period, not just 8.

---

## Validation

- **This folder:** [`bbp_field_closure_complete.py`](bbp_field_closure_complete.py), 30 checks, all passing. Several of its checks are weaker than their names, and their docstrings say so:
  - 02 and 06 assume $D = 3$ rather than test uniqueness;
  - 22–24 show only that the usual series for e, ln 2, √2 and φ are not of BBP's form. Whether e, √2 or φ have formulas of BBP's type is not known.
- **The proofs:** the model repository's `bbp_structure/` package. `PROOF.md` gives Theorems 1–6 and §§10–11. The tests use exact arithmetic wherever the claim is exact.
- The two suites the original note named (`bbp_gfd_structural_tests.py`, `bbp_field_closure_tests.py`, 36 checks) are not in this repository.

---

## Summary

BBP's constants are the integers of GFD's selection equation. The same equation is the condition for BBP's integrand to reach the pole $1 + i$ that produces π.

Among all formulas for π of BBP's type, which are exactly one family, silence on the stellated octahedron's TIME axis selects BBP uniquely. BBP then has the octahedron's other features without their being assumed:
- four spatial corners;
- two in each tetrahedron;
- weights summing to zero.

The precise term remains **common algebraic origin with structural realization**, now with the realization proved unique. The bridge from this mathematics to gravitational physics is not established.

---

## Addendum (2026-11-12): one cyclotomic family, and the weight of the labelling

[`bbp_cyclotomic_structure.md`](bbp_cyclotomic_structure.md), with [`verify_bbp_cyclotomic_and_labelling.py`](verify_bbp_cyclotomic_and_labelling.py) (21 checks), adds three results.

- **BBP and the coupling polynomial are one cyclotomic family.**
  - The coupling polynomial's states are Φ₃, Φ₄, Φ₆ at K (21, 17, 13).
  - In u = y/√2, BBP's integrand has denominator −16 Φ₁Φ₂Φ₄Φ₈(u).
  - Its numerator cancels exactly Φ₄ (the Field Origin polynomial) and the 135° half of Φ₈. π comes from the 45° half of Φ₈ (poles 1 ± i).
  - The two families share only Φ₄. Φ₈(K) = Φ₄(K²) = 257 is the Field Origin one step up the Sierpiński ladder.
- **The slot → vertex labelling carries little weight.**
  - Over all 8! labellings, 42.9% give BBP an octahedral reading through some body diagonal. The I Ching labelling does, through the TIME axis, but so does, for example, Gray code, through another diagonal.
  - The labelling-free core is closure: within the family BBP + r·a the weights sum to −15r, so zero total weight alone selects BBP.
- **Why those factors cancel.**
  - Every formula for π of BBP's type cancels Φ₄ and the 135° half of Φ₈, not BBP alone. Their poles carry the primes 3 and 5, whose logarithms are independent of π by Baker's theorem.
  - Every such numerator is 16(y² + 2)(y² + 2y + 2)[r(y² − 4y + 2) − (y − 1)]. TIME silence and closure both set r = 0, so BBP's factor (y − 1) is the closure condition.
