# BBP and the Coupling Polynomial: One Cyclotomic Family

*Addendum to [the synthesis](bbp_field_closure_synthesis.md) · Gravity Field Dynamics (GFD) · Field Dynamics Research*

*Note, 2026-11-12. Status: the factorisations and counts are exact. The coupling polynomial's cyclotomic form is already in the archive; reading BBP's integrand in the same family, and the shared Φ₄, are new here. Run `python3 verify_bbp_cyclotomic_and_labelling.py` (14 checks, exact algebra, 35-digit integrals, an exhaustive count over 8! labellings).*

---

This note adds two results to the BBP folder.
- **Result 1** shows that the BBP formula and GFD's coupling polynomial are built from the same family of polynomials, the cyclotomic polynomials Φₙ. They share exactly one member, the Field Origin's.
- **Result 2** measures how much the slot-to-vertex labelling contributes to the octahedral reading of BBP in [`PROOF.md`](https://github.com/fielddynamics/dfp-gravity-field-model/tree/test/bbp-octahedron-hypothesis/gravity_field_model/engine_core/field_closure/bbp_structure) (Theorem 3). That labelling is the one input its scope table names.

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

**The numerator cancels two factors exactly:**
- y² + 2 = 2Φ₄(u), the Field Origin polynomial, with poles at ±90°;
- y² + 2y + 2 = 2(u² + √2u + 1), the 135° half of Φ₈.

**What remains** is 16(y − 1)/((y² − 2)(y² − 2y + 2)), and π comes from it as follows (check 1g):
- the 45° half of Φ₈, with poles 1 ± i, gives π + ln 4;
- Φ₁Φ₂, with poles ±√2, gives −ln 4, which cancels the logarithm.

This is PROOF.md Theorem 4, read cyclotomically.

**Together** (checks 1h, 1i):
- **The same family, different members.** The coupling polynomial reads the rotations of the 3D cube (Φ₃, Φ₄, Φ₆) at K. BBP is built from the 2-power rotations (Φ₁, Φ₂, Φ₄, Φ₈).
- **They share exactly one member, Φ₄,** the Field Origin's K² + 1 = 17. BBP's numerator removes precisely that factor.
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

## Status

| Statement | Status |
|---|---|
| f(K, s) as Φ₃, Φ₄, Φ₆ | Already in the archive (`01.1_cyclotomic_algebra.md`) |
| BBP's integrand = p/(−16 Φ₁Φ₂Φ₄Φ₈) in u = y/√2; the numerator cancels Φ₄ and the 135° half of Φ₈; π from the 45° half | Exact algebra; integral checked to 35 digits |
| BBP and the coupling polynomial as one cyclotomic family sharing only Φ₄; BBP's π from Φ₈ = Φ₄ one Sierpiński level up | New reading |
| 42.9% / 34.3% / 8.6% of labellings give the octahedral reading | Exhaustive count |
| Closure alone selects BBP within the family | Exact (PROOF.md, Theorem 3 remark) |

## Open

- **Why BBP's numerator removes exactly Φ₄ and the 135° half of Φ₈.** PROOF.md's extension test 18 records which poles cancel, but not why. A reason grounded in the Field Origin, rather than in number theory, would be the real next step.
- **Whether Theorems 5–6 (the reading rules) are labelling-specific** in a way that survives the same exhaustive treatment.

## Related

- [The synthesis](bbp_field_closure_synthesis.md) and [`bbp_field_closure_complete.py`](bbp_field_closure_complete.py) (30 checks).
- PROOF.md in the model repository (`dfp-gravity-field-model`, branch `test/bbp-octahedron-hypothesis`, `gravity_field_model/engine_core/field_closure/bbp_structure/`).
- [`01.1_cyclotomic_algebra.md`](../exploratory/great-pyramid/pyramid_portal_research/01_framework_foundations/01.1_cyclotomic_algebra.md): f(K, s) = Φ₆, Φ₄, Φ₃ and the Sierpiński ladder (241, 257, 273 at K = 16).
- [`coupling-algebra/`](../coupling-algebra/), Result 13: f(K, s) as the characteristic polynomial of the cube's rotations.
