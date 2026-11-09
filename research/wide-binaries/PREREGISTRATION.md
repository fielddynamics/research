# Pre-registered Prediction: Wide Binary Stars in Gaia DR4

*Registered 9 November 2026, by the commit that adds this file, before the release of Gaia DR4 (scheduled 2 December 2026) · Field Dynamics Research*

---

## The prediction

Two stars thousands of AU apart orbit each other in a field weaker than $a_0$, but inside the Milky Way's own gravitational field. GFD's covariant action fixes how such a pair moves. Its field equation,

$$\nabla \cdot \left[\mu\!\left(\frac{|\nabla\Phi|}{a_0}\right) \nabla\Phi\right] = 4\pi G\rho, \qquad \mu(x) = \frac{x}{1+x},$$

was solved numerically for a binary in the Galactic field ([`wide_binary_prediction.py`](wide_binary_prediction.py)). The result is the gravity between the two stars relative to Newton, $\gamma = g/g_{\text{Newton}}$, averaged over orbit orientations:

| Separation (kau) | 1 | 2 | 3 | 5 | 7 | 10 | 15 | 20 | 30 |
|---|---|---|---|---|---|---|---|---|---|
| $\gamma$, $M = 1.5\,M_\odot$ | 1.014 | 1.052 | 1.109 | 1.250 | 1.366 | 1.402 | 1.412 | 1.414 | 1.416 |
| velocity boost $\sqrt\gamma$ | 1.007 | 1.026 | 1.053 | 1.118 | 1.169 | 1.184 | 1.188 | 1.189 | 1.190 |

Close pairs are Newtonian. Beyond about 10 kau, gravity is **42% stronger** than Newton's and orbital velocities are **19% faster**.

In the notation of the two published Gaia DR3 analyses:
- **Chae:** $\Gamma = \tfrac12\log_{10}\gamma_g = 0.075$ on the plateau.
- **Banik et al.:** $\alpha_{\text{grav}} \approx 1$ (the MOND value with the simple interpolating function; 0 is Newton).

### The single number

For each binary, let $\tilde v = v_p / \sqrt{G M / s_p}$, with $v_p$ the sky-projected relative velocity, $s_p$ the projected separation and $M$ the total mass. Then:

$$R = \frac{\text{median } \tilde v \;(s_p = 10\text{–}30 \text{ kau})}{\text{median } \tilde v \;(s_p = 1\text{–}2 \text{ kau})} = \mathbf{1.163}$$

| | $R$ |
|---|---|
| GFD, measured Galactic field, $M = 1.5\,M_\odot$ | **1.163** |
| GFD, range over Galactic field 1.6–1.9 $a_0$ and $M$ = 1–2 $M_\odot$ | 1.138 – 1.184 |
| Newtonian gravity | 1.000 |

$R$ needs no absolute calibration: under Newton, the distribution of $\tilde v$ is the same at every separation, so any departure from 1 is a change in gravity.

## Inputs, none fitted

| Input | Value | Source |
|---|---|---|
| $\mu(x)$ | $x/(1+x)$ | GFD's constitutive law, derived from exchange symmetry |
| $a_0$ | $1.2 \times 10^{-10}$ m/s² | the archive's value (RAR letter) |
| Galactic field at the Sun | $v_c^2/R_0 = 2.09 \times 10^{-10}$ m/s² $= 1.744\,a_0$ | $v_c = 229.0$ km/s, $R_0 = 8.122$ kpc (Eilers et al. 2019) |
| Binary mass | 1.0, 1.5, 2.0 $M_\odot$ | typical total masses |

## Approximations, stated in advance

- The relative motion is that of a test body around the pair's total mass, the standard treatment in published wide-binary predictions.
- At fixed separation, velocities scale as $\sqrt{\gamma}$: exact if $\gamma$ is constant along an orbit, and close to it beyond 10 kau, where $\gamma$ is flat.
- Projected separations are converted to true separations by the isotropic mean factor $4/\pi$.
- The Galactic field is uniform across the binary; tides and the disk's vertical field are neglected.
- The field equation is the action's static scalar-sector equation, in its AQUAL form, as stated in Letter 3's covariant-completion supplement.

## The solver

[`gfd_field_solver.py`](gfd_field_solver.py) solves the full nonlinear equation on an axisymmetric finite-volume grid. [`validate_solver.py`](validate_solver.py) checks it against two exact results (5/5):
- **Isolated mass:** within 0.3% of the exact spherical solution, and within 0.05% beyond 3 MOND radii.
- **Mass in an external field:** within 0.3% of the analytic far field.
- Two grid resolutions agree within 0.3%.

## Pass and fail

Only analyses of Gaia DR4 data count. An analysis qualifies if it models hierarchical triples, chance alignments and projection, as both published DR3 analyses do.

- **Pass:** a qualifying analysis finds $R$, $\Gamma$ or $\alpha_{\text{grav}}$ within 2σ of the GFD value and excludes Newtonian gravity at 5σ or more.
- **Fail:** a qualifying analysis finds a result consistent with Newtonian gravity that excludes the GFD value at 5σ or more.
- **Otherwise inconclusive.** If qualifying analyses disagree, as the DR3 analyses do, record each result; the question stays open until an independent analysis resolves it.

## Status before DR4

The two published DR3 analyses disagree:
- Banik et al. (2024) exclude MOND at 16σ, finding $\alpha_{\text{grav}} = -0.021^{+0.065}_{-0.045}$ for separations of 2–30 kau.
- Chae (2025) finds $\Gamma = 0.085 \pm 0.040$ ($\gamma_g \approx 1.48$) in the low-acceleration regime, consistent with MOND.

GFD sides with the second. DR4 has roughly twice the observing time of DR3 and should settle it.

## What a pass would and would not show

A pass would show that GFD's action holds where Newtonian gravity fails, at stellar scale, without dark matter, which cannot be present in binaries. It would not distinguish GFD from MOND with the same interpolating function, which predicts the same curve: this test is between GFD and Newton, not between GFD and MOND. A fail would rule out the action's static field equation in the regime where it is meant to apply.

---

**Run:** `python validate_solver.py` (about 1 minute), then `python wide_binary_prediction.py` (about 2 minutes). Requires numpy and scipy.

**References**
- I. Banik et al., *Strong constraints on the gravitational law from Gaia DR3 wide binaries*, MNRAS 527 (2024) 4573, arXiv:2311.03436.
- K.-H. Chae, *Low-acceleration gravitational anomaly from Bayesian 3D modeling of wide binary orbits*, arXiv:2502.09373 (2025).
- A.-C. Eilers et al., *The circular velocity curve of the Milky Way from 5 to 25 kpc*, ApJ 871 (2019) 120.
- ESA, Gaia DR4 release, 2 December 2026, cosmos.esa.int/web/gaia/news-2026.
