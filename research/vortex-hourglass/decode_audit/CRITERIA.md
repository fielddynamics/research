# Drive and Brake from Full Decoded Profiles: Criteria

*Fixed and committed on 2026-11-14 before any galaxy is measured. Pipeline: [`decode_audit.py`](decode_audit.py). Results: [`README.md`](README.md).*

---

## Why this replaces the earlier test

The first drive/brake test (H2′ in the [hourglass note](../README.md)) compared decoded and photometric mass at the **outermost point only**, with **no smoothing**. The [decoding-mass letter](../../../papers/letter-decoding-mass-from-rotation-curves/) does neither. It decodes the whole observed profile, after light smoothing, and reads $\Delta M_{\rm eff}(r)$ at every radius. A single point can be an outlier, a warp or a non-circular motion. A profile shows where along the galaxy the field sits above or below its baryons.

## 1. Audit of the decode (must pass before any galaxy is classified)

| | Check | Pass |
|---|---|---|
| A1 | The decode, $M_{\rm dec}(r) = r v^4 / [G(a_0 r + v^2)]$, equals the letter's own `velocity_decode` function at every SPARC point | Relative difference < $10^{-10}$ |
| A2 | Round trip: the letter's forward relation applied to $M_{\rm dec}$ returns the input velocity | Relative difference < $10^{-10}$ |
| A3 | The letter's published M33 value is reproduced from its own data and code path: $M_{\rm dec}(17\,{\rm kpc}) = 1.38\times10^{10}\,M_\odot$ | Agreement to the quoted 3 figures |
| A4 | Constants as in the letter: $G = 6.674\times10^{-11}$, $a_0 = 1.2\times10^{-10}$ m s⁻², kpc $= 3.086\times10^{19}$ m, $M_\odot = 1.989\times10^{30}$ kg | Identical |
| A5 | The photometric stellar mass integrates SPARC's own surface-brightness profiles correctly: total 3.6 µm light matches SPARC's catalogue $L_{[3.6]}$ | Median within 0.05 dex |
| A6 | Velocity smoothing as in the letter: Gaussian of width 6.2% of the radial span | Same function |

## 2. The profile

At **every observed radius** of each galaxy:

- **Decoded mass.** $M_{\rm dec}(r)$ from the smoothed velocity, with bounds $M_{\rm dec}^{\pm}(r)$ from $v \pm \sigma_v$. These are the letter's `M_dec_bounds`, applied to the observed velocity and its error.
- **Photometric mass.** $M_{\rm phot}(r)$ is the enclosed baryonic mass:
  - stars: $\Upsilon \int 2\pi R\,\Sigma(R)\,dR$ over SPARC's disk ($\Upsilon_d = 0.5$) and bulge ($\Upsilon_b = 0.7$) surface-brightness profiles, with constant surface brightness inside the first point;
  - gas: $|V_{\rm gas}|V_{\rm gas}\,r/G$. SPARC's $V_{\rm gas}$ already includes helium (1.33 × HI). SPARC gives no gas surface-density profile, so this is a spherical estimate and is flagged.
- **The gap.** $\Delta(r) = \log_{10}[M_{\rm dec}(r)/M_{\rm phot}(r)]$. A positive $\Delta$ means the field exceeds its baryons, which is drive. A negative $\Delta$ is brake. (In the letter's sign, $\Delta M_{\rm eff} = M_{\rm phot} - M_{\rm dec}$ is negative for a drive.)

## 3. The metric: area above and below

Integrate over the observed span in $\ln r$, so that every factor of radius counts equally and galaxies of different size compare directly. Let $L = \ln(r_{\max}/r_{\min})$ and use the trapezoid rule:

$$A_+ = \frac1L\int \max(\Delta, 0)\,d\ln r, \qquad A_- = \frac1L\int \max(-\Delta, 0)\,d\ln r, \qquad A = A_+ - A_-.$$

These are in dex. $A_+$ is the average height of the profile above its baryons, $A_-$ its average depth below them, and $A$ the net. Two companion counts use the velocity errors:
- $f_+$ is the fraction of points with $M_{\rm dec}^- > M_{\rm phot}$ (above, beyond the error);
- $f_-$ is the fraction with $M_{\rm dec}^+ < M_{\rm phot}$ (below, beyond the error).

## 4. Classification

The threshold is $\tau = 0.15$ dex, a factor of 1.4, roughly the systematic uncertainty of a stellar M/L at 3.6 µm. The rules are applied in this order:

1. **Mixed:** $A_+ > \tau$ and $A_- > \tau$. Above its baryons in one region and below in another.
2. **Drive:** $A > +\tau$ and $f_+ \ge 0.5$.
3. **Brake:** $A < -\tau$ and $f_- \ge 0.5$.
4. **Quiet:** otherwise.

**Robustness.** The classification is repeated with every stellar M/L scaled by 0.8 and 1.2. A galaxy's class is **robust** if it is the same at all three; otherwise it is reported as **uncertain**. Galaxies whose gas makes up half or more of $M_{\rm phot}$ at the outermost point are flagged **gas-dominated**, because their $M_{\rm phot}$ rests on the spherical gas estimate.

All 175 SPARC galaxies are measured and tabulated. The quality cut (Q ≤ 2, inclination ≥ 30°, ≥ 5 points) is applied only to the hypothesis test.

## 5. Hypothesis H3: drive and brake against the ring

The hourglass reading predicts drag outside the ring $x = g_{\rm obs}/a_0 = 1$ and drive inside it. So the more of a galaxy's baryonic mass lies inside the ring, the higher its net area $A$ should be. The ring share $f_{\rm in}$ is $M_{\rm phot}$ at the ring over $M_{\rm phot}$ at the outermost point; it is 0 if the whole galaxy is below $a_0$ and 1 if the whole galaxy is above it.

**H3 passes** if the one-sided Spearman correlation $\rho(f_{\rm in}, A) > 0$ with $p < 0.01$ in both:
- (a) all quality-cut galaxies;
- (b) quality-cut galaxies that are not gas-dominated.

Galaxies without a bulge are reported separately but are not part of the pass condition. Otherwise H3 fails.

A local version is also reported, without a pass condition. Inside each galaxy that contains the ring, compare $\Delta$ inside the ring with $\Delta$ outside it.
