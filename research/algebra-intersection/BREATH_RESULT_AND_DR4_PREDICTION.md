# Result of pre-registration 3, and a registered prediction for Gaia DR4

*Pre-registration: [`BREATH_SPARC_PREREG.md`](BREATH_SPARC_PREREG.md), committed 347f611 before computing. Code: [`breath_sparc.py`](breath_sparc.py), [`breath_wide_binaries.py`](breath_wide_binaries.py).*

## SPARC: undecided, as registered

| | Mean residual (dex) | σ (dex) |
|---|---|---|
| Baseline (letter), reproduced | −0.0269 | 0.1814 |
| H_breath | +0.0138 | 0.1814 |

σ_H − σ_base < 0.0001 dex, inside the ±0.002 dex window: **undecided**. The mean moves towards zero (−0.027 to +0.014), but as registered the mean does not decide, since it depends on mass-to-light ratios. Note: the CSV has 163 distinct galaxies, against the letter's stated 164.

**Why SPARC cannot tell.** H_breath is exactly the letter's relation with $a_0 \to \tfrac{13}{17}a_0 = 0.918\times10^{-10}$ m/s². Both in the algebraic relation and in the field equation, $\mu(x)(x+1)/(x + 13/17) = x/(x + 13/17)$. On the radial acceleration relation, a 24% change in $a_0$ shifts the curve along a direction that the mass-to-light ratio can absorb. Wide binaries cannot absorb it, because their external field is fixed in m/s².

## Registered prediction for Gaia DR4 (before its 2 December 2026 release)

Computed with the archive's own solver ([`wide-binaries/gfd_field_solver.py`](../wide-binaries/gfd_field_solver.py)), unchanged, with $a_0 = 0.918\times10^{-10}$. The Galactic field is then 2.28 $a_0$, against 1.744 $a_0$ in the registered GFD prediction.

| | $R$ = median $\tilde v$ (10–30 kau) / median $\tilde v$ (1–2 kau) | plateau $\gamma$ | Chae's $\Gamma$ |
|---|---|---|---|
| GFD, registered (fixed breath, `wide-binaries/PREREGISTRATION.md`) | **1.163** (1.138–1.184) | 1.416 | 0.075 |
| **H_breath (field-dependent breath)** | **1.126** (1.118–1.131, M = 1–2 M☉) | 1.315 | 0.059 |
| Newton | 1.000 | 1.000 | 0 |

The ranges do not overlap. A qualifying DR4 analysis that measures $R$ to about ±0.01 decides between them:
- $R \approx 1.16$: the breath is universal and 17/13 is a constant.
- $R \approx 1.13$: the breath is set by the local field, and G's prefactor runs from 17/13 (strong field) to 1 (deep field).
- $R \approx 1.00$: both are wrong.

Pass and fail rules are as in `wide-binaries/PREREGISTRATION.md`. This registration takes effect with the commit that adds this file.
