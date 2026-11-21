# The Constitutive Law μ(x)

*Working material on where μ(x) = x/(x + 1) comes from · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`constitutive-law` `screening` `exchange-symmetry` `tug-of-war` `decoding-mass` `vortex`

*Research folder. Status: working notes with checks, not a paper. The finished proof is [`proofs/constitutive-law-tug-of-war/`](../../proofs/constitutive-law-tug-of-war/).*

---

## What is here

The folder holds three generations of work on the constitutive law.

The first generation, from March 2026, is the derivation from the coupling polynomial. `gfd_constitutive_law_synthesis.docx` reads μ(x) as the Field Origin's saturation response, built from the three terms of f(k, s) = 1 + sk + k², and `gfd_constitutive_law_suite.py` checks it in 30 tests. The extended synthesis and its 50-test suite, `gfd_constitutive_law_extended.py`, add the Poisson duality and the comparison with the other interpolating functions of MOND.

The second generation is visual. The two roulettes, `tetA_tetB_roulette_roll_ratio.html` and `tetA_tetB_roulette_fullscale.html`, draw TetA as a fixed circle of radius μ and TetB as a circle of radius 1 − μ rolling on it, so that the roll ratio is the odds μ/(1 − μ) = x. The [roll-ratio note](../vortex-hourglass/ROLL_RATIO.md) writes that picture as algebra.

The third generation, [`TUG_OF_WAR_THEOREM.md`](TUG_OF_WAR_THEOREM.md) with its 85 tests in [`test_tug_of_war.py`](test_tug_of_war.py), asks which premises are actually needed and shows that each one is necessary. It reads μ as a tug of war in which TetA pulls with the local field g and TetB pulls with a₀. The exchange of the two chambers, applied to the folder's own screening equation, forces the odds to be a power of x, and flat rotation curves fix that power at 1. The same algebra turns the decoding-mass letter's drive and brake into TetB pulling harder or softer than a₀.

## Contents

| File | Contents |
|---|---|
| `gfd_constitutive_law_synthesis.docx`, `gfd_constitutive_law_suite.py` | The coupling-polynomial derivation and its 30 checks |
| `gfd_constitutive_law_extended_synthesis.docx`, `gfd_constitutive_law_extended.py` | The extended synthesis and its 50 checks |
| `tetA_tetB_roulette_roll_ratio.html`, `tetA_tetB_roulette_fullscale.html` | The roll-ratio roulettes |
| [`TUG_OF_WAR_THEOREM.md`](TUG_OF_WAR_THEOREM.md) | The tug-of-war theorem, its corollary for decoding mass, and the vortex reading |
| [`test_tug_of_war.py`](test_tug_of_war.py) | 85 tests: `python -m pytest -q test_tug_of_war.py` (numpy, scipy, sympy, pytest) |

## Two corrections to the first generation

The tug-of-war work found two statements in the March syntheses that need rewording; neither changes the law.
- **Langmuir sites.** The syntheses say that n sites give xⁿ/(1 + xⁿ). Independent sites give x/(1 + x) for any number of them, and xⁿ/(1 + xⁿ) appears only when the sites fill together (Hill binding). The single Field Origin is therefore not, by itself, what fixes the power at 1 (test 9.1).
- **"Not algebraic".** The extended synthesis says that the inverse of the standard function x/√(1 + x²) is not algebraic. That inverse, μ/√(1 − μ²), is algebraic; what sets x/(x + 1) apart is that its inverse is rational, a Möbius map (test 9.2).
