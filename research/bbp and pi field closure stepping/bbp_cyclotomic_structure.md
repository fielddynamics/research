# BBP and the Coupling Polynomial: One Cyclotomic Family

*Addendum to [the synthesis](bbp_field_closure_synthesis.md) · Gravity Field Dynamics (GFD) · Field Dynamics Research*

*Note, 2026-11-12. Status: the factorisations and counts are exact. The coupling polynomial's cyclotomic form is already in the archive; reading BBP's integrand in the same family, and the shared Φ₄, are new here. Run `python3 verify_bbp_cyclotomic_and_labelling.py` (21 checks, exact algebra, 35-digit integrals, an exhaustive count over 8! labellings).*

---

This note adds three results to the BBP folder.
- **Result 1** shows that the BBP formula and GFD's coupling polynomial are built from the same family of polynomials, the cyclotomic polynomials Φₙ. They share exactly one member, the Field Origin's.
- **Result 2** measures how much the slot-to-vertex labelling contributes to the octahedral reading of BBP in [`PROOF.md`](https://github.com/fielddynamics/dfp-gravity-field-model/tree/test/bbp-octahedron-hypothesis/gravity_field_model/engine_core/field_closure/bbp_structure) (Theorem 3). That labelling is the one input its scope table names.
- **Result 3** explains why the Field Origin factor Φ₄ and the 135° half of Φ₈ cancel. Every formula for π of BBP's type cancels them, because their poles carry the primes 3 and 5. What singles out BBP is the factor (y − 1), which is the closure condition.

## 1. One cyclotomic family

The cyclotomic polynomial Φₙ is the minimal polynomial of a rotation by 1/n of a turn.

**The coupling polynomial is three of them, evaluated at K** (check 1a):

| State | f(K, s) | Cyclotomic | Rotation | K = 4 |
|---|---|---|---|---|
| TetA | K² + K + 1 | Φ₃ | 120° | 21 |
| Field Origin | K² + 1 | Φ₄ | 90° | 17 |
| TetB | K² − K + 1 | Φ₆ | 60° | 13 |

These are the planar rotations the cube allows, of orders 3, 4 and 6. The identity is already in the archive ([`01.1_cyclotomic_algebra.md`](../exploratory/great-pyramid/pyramid_portal_research/01_framework_foundations/01.1_cyclotomic_algebra.md), "the two registers are identical"). It also agrees with [coupling-algebra Result 13](../coupling-algebra/README.md), where f(K, s) = det(K − R) for the cube's rotations.

**BBP's integrand is built from four of them** (checks 1b–1f). By PROOF.md Theorem 2, Step 1:

$$\pi = \int_0^1 \frac{p(y)}{16 - y^8}\,dy, \qquad p(y) = -16\,(y-1)(y^2+2)(y^2+2y+2).$$

**Denominator.** Write y = √2 u. Then

$$16 - y^8 = -16\,\Phi_1(u)\,\Phi_2(u)\,\Phi_4(u)\,\Phi_8(u),$$

the rotations of order 1, 2, 4 and 8, which are the divisors of 8 = 2^D. Over ℚ(√2), Φ₈ splits into two halves:
- u² − √2u + 1, with poles at 45° and 315°;
- u² + √2u + 1, with poles at 135° and 225°.

**The numerator cancels two factors exactly.** Section 3 shows that every formula for π of this type cancels these same two, so this is not a choice BBP makes:
- y² + 2 = 2Φ₄(u), the Field Origin polynomial, with poles at ±90°;
- y² + 2y + 2 = 2(u² + √2u + 1), the 135° half of Φ₈.

**What remains** is 16(y − 1)/((y² − 2)(y² − 2y + 2)), and π comes from it as follows (check 1g):
- the 45° half of Φ₈, with poles 1 ± i, gives π + ln 4;
- Φ₁Φ₂, with poles ±√2, gives −ln 4, which cancels the logarithm.

This is PROOF.md Theorem 4, read cyclotomically.

**Together** (checks 1h, 1i):
- **The same family, different members.** The coupling polynomial reads the rotations of the 3D cube (Φ₃, Φ₄, Φ₆) at K. BBP is built from the 2-power rotations (Φ₁, Φ₂, Φ₄, Φ₈).
- **They share exactly one member, Φ₄,** the Field Origin's K² + 1 = 17. That factor is absent from BBP's integrand, and from every formula for π of its type (section 3).
- **BBP's π comes from one half of Φ₈.** Since Φ₈(K) = K⁴ + 1 = Φ₄(K²), this is the Field Origin one step up the archive's Sierpiński ladder K → K² (257 at K = 4, in the same `01.1_cyclotomic_algebra.md`). Classically, x⁴ + 1 is also the characteristic polynomial of the tesseract's Coxeter rotation, which needs four dimensions.

This explains a fact independently: no symmetry of the 3D stellated octahedron has order 8. Its 48 symmetries have orders 1, 2, 3, 4 and 6, and its 8 points form the group ℤ₂³, not BBP's ℤ₈. So BBP's 8-cycle can't be one of its symmetries. In cyclotomic terms it belongs one level up.

## 2. How much the labelling matters

PROOF.md Theorem 3 reads slot j as cube vertex j mod 8 (place value fixed by the *Shuo Gua*). With that reading, silencing the TIME axis selects BBP, with 4 active slots, a 2 + 2 split and zero total weight. Its scope table lists the labelling as the one real input. I checked every possible labelling (check 2c):

| Over all 8! = 40,320 slot → vertex labellings | Count |
|---|---|
| Some body diagonal, silenced, selects BBP with the octahedral shape | 17,280 (42.9%) |
| Exactly one diagonal does | 13,824 (34.3%) |
| Exactly the Kun–Qian (TIME) diagonal does | 3,456 (8.6%) |

The individual labellings behave as follows (checks 2d, 2e):
- **I Ching place value:** selects through the Kun–Qian diagonal only, as PROOF.md states.
- **Gray code** (consecutive slots one cube edge apart): also selects BBP, through a different diagonal.
- **Reverse place value:** selects none, matching PROOF.md's extension test 07.

**What this means:**
- **The labelling carries little weight.** About two labellings in five give BBP an octahedral reading. That's because BBP leaves 4 of its 8 slots silent and balances its weights, so many arrangements place a silent pair on some diagonal. The I Ching labelling is consistent with the octahedral reading, but it isn't what makes the reading possible.
- **The labelling-free core is closure.** In the family BBP + r·a the weights sum to −15r (check 2b), a fact PROOF.md records in its Theorem 3 remark. So weights summing to zero alone selects BBP, with no labelling. Together with Theorem 2 (one family), this is the strongest form of the selection: **among all BBP-type formulas for π, closure picks BBP.**
- **Where labelling-specific content remains.** Any content that depends on the I Ching labelling would sit in PROOF.md's Theorems 5–6, the reading rules built from the trigram lines. Those were not re-examined here.

## 3. Why Φ₄ and the 135° half cancel: the primes 3 and 5

By PROOF.md Theorem 2 (Step 1), the pole at y = √2ω contributes the logarithm of 1 − ω̄/√2. Multiplying the two poles of each conjugate pair gives each pair's arithmetic (checks 3a, 3b):

| Pole pair | Factor | Product | Logarithms it brings |
|---|---|---|---|
| 0°, 180° | Φ₁Φ₂ | 1/2 | log 2, log(1 + √2), both real |
| 45°, 315° | 45° half of Φ₈ | 1/2 | log 2 and ±iπ/4, from (1 ± i)/2 |
| 90°, 270° | Φ₄, the Field Origin | 3/2 | log(√2 ± i), from the prime 3 = (√2 + i)(√2 − i) |
| 135°, 225° | 135° half of Φ₈ | 5/2 | log(2 ∓ i), from the prime 5 = (2 + i)(2 − i) |

The argument then runs:
- **Each of these logarithms sits at exactly one pole.** log(√2 ± i) appears only at the 90° and 270° poles; log(2 ∓ i) only at the 135° and 225° poles.
- **By Baker's theorem they are independent of π, log 2 and log(1 + √2).** PROOF.md Theorem 2 (Step 3) proves this.
- **So a formula whose value is π must have zero residue at those four poles.** Its numerator must vanish there, which means it is divisible by (y² + 2)(y² + 2y + 2) (check 3c).

So the Field Origin factor and the 135° half cancel because their poles carry the odd primes 3 and 5, which can never combine into π. Only the 45° pair has a value of norm 1/2 with a nonzero argument, (1 ± i)/2 at ±π/4, so π can only come from there (check 3g).

**The whole family in one formula.** Every formula for π of BBP's type, BBP + r·a, has numerator

$$16\,(y^2+2)(y^2+2y+2)\,\big[\,r\,(y^2 - 4y + 2) - (y - 1)\,\big].$$

- **y² + 2:** the Field Origin factor, forced out by the prime 3, for every r.
- **y² + 2y + 2:** the 135° half of Φ₈, forced out by the prime 5, for every r.
- **The bracket:**
  - its y² coefficient is 16r, which is exactly the TIME slot w₇, so TIME silence means r = 0 (check 3d);
  - closure (weights summing to zero) means the numerator vanishes at y = 1, the end of the integration range, which also forces r = 0 (check 3f).

What is left at r = 0 is −(y − 1). So **BBP's factor (y − 1) is the closure condition**, and TIME silence and closure act on the same last factor (checks 3e, 3f).

**What this does not show.** It does not show that the primes 3 and 5 mean anything in GFD terms. Reading them as D = 3 and K + 1 = 5 is tempting, but nothing here forces it, so it is recorded as an observation only.

## Status

| Statement | Status |
|---|---|
| f(K, s) as Φ₃, Φ₄, Φ₆ | Already in the archive (`01.1_cyclotomic_algebra.md`) |
| BBP's integrand = p/(−16 Φ₁Φ₂Φ₄Φ₈) in u = y/√2; the numerator cancels Φ₄ and the 135° half of Φ₈; π from the 45° half | Exact algebra; integral checked to 35 digits |
| Every formula for π of BBP's type cancels Φ₄ and the 135° half, because their poles carry the primes 3 and 5 (Baker's theorem) | Proved, from PROOF.md Theorem 2 |
| The family's numerators are 16(y² + 2)(y² + 2y + 2)[r(y² − 4y + 2) − (y − 1)]; (y − 1) is the closure condition | Exact algebra |
| BBP and the coupling polynomial as one cyclotomic family sharing only Φ₄; BBP's π from Φ₈ = Φ₄ one Sierpiński level up | New reading |
| 42.9% / 34.3% / 8.6% of labellings give the octahedral reading | Exhaustive count |
| Closure alone selects BBP within the family | Exact (PROOF.md, Theorem 3 remark) |

## Open

- **Whether the primes 3 and 5 at the cancelled poles have a GFD meaning.** Section 3 explains the cancellation by number theory. A reading grounded in the Field Origin would be the next step, and nothing yet supports one.
- **Whether Theorems 5–6 (the reading rules) are labelling-specific** in a way that survives the same exhaustive treatment.

## Related

- [The synthesis](bbp_field_closure_synthesis.md) and [`bbp_field_closure_complete.py`](bbp_field_closure_complete.py) (30 checks).
- PROOF.md in the model repository (`dfp-gravity-field-model`, branch `test/bbp-octahedron-hypothesis`, `gravity_field_model/engine_core/field_closure/bbp_structure/`).
- [`01.1_cyclotomic_algebra.md`](../exploratory/great-pyramid/pyramid_portal_research/01_framework_foundations/01.1_cyclotomic_algebra.md): f(K, s) = Φ₆, Φ₄, Φ₃ and the Sierpiński ladder (241, 257, 273 at K = 16).
- [`coupling-algebra/`](../coupling-algebra/), Result 13: f(K, s) as the characteristic polynomial of the cube's rotations.
