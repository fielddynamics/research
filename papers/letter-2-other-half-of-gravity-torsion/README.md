# The Other Half of Gravity: Torsion and the Two-Chamber Structure of the Tetrad Frame

*Letter 2 of the tetrad letters: a torsion-free connection cannot tell TetA from TetB, so the 24 torsion components carry the second chamber · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`tetrad` `torsion` `affine-connection` `parity` `exchange-symmetry` `constitutive-law` `coupling-polynomial` `dark-matter`

---

A five-page Letter, submitted to *Classical and Quantum Gravity* (CQG-115447) as the companion to Letter 1 (CQG-115428). Two versions are kept: **[`v2/`](v2/) is current** and [`v1/`](v1/) is the first submission. Each version has a supplementary note and a validation script that checks 52 claims, covering both this Letter and Letter 1.

## The argument in one paragraph

The connection on the tetrad frame has K³ = 64 components: 40 symmetric under exchange of the lower pair (the Christoffel symbols) and 24 antisymmetric (the torsion). Letter 1 showed that the tetrad equation has two bounded regions related by spatial parity, TetA and TetB.
- **Lemma.** A torsion-free connection is fixed by the metric. The metric g = η e e is bilinear in the frame, so it is unchanged by e^i → −e^i. So a torsion-free connection cannot tell TetA from TetB.
- **Corollary.** The torsion sector is the necessary carrier of the TetA/TetB distinction. Setting torsion to zero collapses the two chambers into one.
- **The fraction.** Exchange symmetry inverts the odds ratio Ω = μ/(1 − μ). With Ω a rational bijection of the projective line, this forces Ω(x) = x. So TetA carries **μ = x/(x + 1)** and TetB carries **1 − μ = 1/(x + 1)**, with no fitting.

## Results

| Section | Result |
|---|---|
| 1. The torsion question | 64 = 40 + 24. Einstein set the 24 to zero in 1915. Einstein–Cartan keeps them, coupled to spin, so they vanish in vacuum. What the 24 represent geometrically was left open |
| 2. The parity identification | The Lemma above. In v2 a Proposition adds that the tetrad equation is quadratic in the frame: TetA and TetB are its two roots, the metric is the image and is root-blind, and torsion is root-resolving. The Christoffel sector is "image-complete but root-blind" |
| 3. The TetB field fraction | μ = x/(x + 1) and 1 − μ = 1/(x + 1) from exchange symmetry, proved in the supplementary note. Torsion-free means μ = 1, so the field response it misses is Δμ = 1/(x + 1): negligible for x ≫ 1, half at x = 1, nearly all for x ≪ 1 |
| 4. The dark-to-baryon ratio | Taking the baryonic part as μ g_obs and the residual as (1 − μ) g_obs gives g_DM/g_baryon = (1 − μ)/μ = **1/x**. Shell by shell this is also M_DM/M_baryon = 1/x, with no halo profile |
| 5. The coupling polynomial | f(K, s) = 1 + sK + K² gives 21, 17, 13 at s = +1, 0, −1, with range 2K = 8. Christoffel K·K(K+1)/2 = 40 and torsion K·K(K−1)/2 = 24. **Theorem:** with D = K − 1, the torsion count equals D × 2K only at K = 4, so 24 = 3 × 8. The Letter also tabulates every standard tetrad count as a polynomial in K |
| 6. Discussion | The two arguments, parity and polynomial, are independent. Christoffel plus contorsion corresponds to μ plus 1 − μ (v2). The logistic identity x dμ/dx = μ(1 − μ) holds (v2). The strong-field tests are unaffected, and the TetB field never exceeds a₀, so there is no central cusp. 2(D + 1) = 2^D also connects to the bimetric programme |

## v1 and v2

v2 keeps v1's results and adds:
- the **Proposition** (two roots of a quadratic map, the metric root-blind, torsion root-resolving);
- the remark that root-blindness also removes the interaction core;
- the derivation of the fraction through the odds ratio Ω, replacing the functional equation μ(1/x) = 1 − μ(x);
- the Christoffel-plus-contorsion correspondence and the logistic identity in the Discussion;
- a justification document.

## Contents

| File | What it is |
|---|---|
| [`v2/letter.pdf`](v2/letter.pdf), [`v2/letter.tex`](v2/letter.tex) | The Letter, current version. [`v2/Nelson_2026_The_Other_Half_Of_Gravity.pdf`](v2/Nelson_2026_The_Other_Half_Of_Gravity.pdf) is the same text under its distribution name |
| [`v2/cover_letter.pdf`](v2/cover_letter.pdf) | Cover letter to *Classical and Quantum Gravity* |
| [`v2/justification.pdf`](v2/justification.pdf) | Submission justification |
| [`v2/Supplementary/supplementary_tetb_fraction.pdf`](v2/Supplementary/supplementary_tetb_fraction.pdf) | *The TetB Field Fraction from Exchange Symmetry* (Supplementary Note 1) |
| [`v2/Supplementary/run_all_validations.py`](v2/Supplementary/run_all_validations.py) | Validation script: 52 claims (NumPy, SciPy, SymPy). Sections 1–12 check Letter 1's geometry, Section 13 the Lemma (Pᵀη P = η for every metric sector), and Section 14 the chain from exchange symmetry to the dark-to-baryon ratio, symbolically |
| [`v1/`](v1/) | The first submission, with its own cover letter, supplementary note and validation script (also 52/52) |
| `*/build_letter.bat` | Windows build scripts |

## Running the checks

```
cd v2/Supplementary
python run_all_validations.py
```

It ends with `52/52 claims verified. 0 failures.`

## Later work in this repository

These build on the Letter. They do not change it.
- **Letter 3**, [`../letter-3-field-closure-of-tetrad-frame/`](../letter-3-field-closure-of-tetrad-frame/): the torsion-free condition keeps the s = +1 projection (40) and discards s = −1 (24); restoring them gives field closure and the SST action.
- **The constitutive law**, [`proofs/constitutive-law-exchange-symmetry/`](../../proofs/constitutive-law-exchange-symmetry/): μ = x/(x + 1) proved unique under exchange closure, with each premise shown to be necessary.
- **The torsion sector**, [`proofs/torsion-regular-representation/`](../../proofs/torsion-regular-representation/): the 24 components form the regular representation of S₄, and the sign representation occurs once in the torsion and never in the Christoffel sector.
- **The scheme**, [`proofs/tetrad-scheme-two-bounded-regions/`](../../proofs/tetrad-scheme-two-bounded-regions/): the two roots as the two connected components of the tetrad scheme.
- **An open question**, [`proofs/g-null-rotation/`](../../proofs/g-null-rotation/): there, the TetB state's count of 13 is reproduced by the total inversion (time and space reversed together), not by spatial parity. Whether the TetA ↔ TetB exchange should be read that way is left open.
- **The solar system.** The Letter says GR's strong-field predictions are unaffected because Δμ is negligible there. The later reading in the Coles Notes (§5.4) is stronger: a bound system is pure TetA, and μ applies to the host galaxy's net field.
