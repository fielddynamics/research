# Pushing the Pixel Λ System Further: Results

*Run 2026-11-15 against [`PLAN.md`](PLAN.md), committed before any script ran. Outputs are in [`output/`](output/).*

## Answer in brief

1. **The root is in the phase, not in any energy.** Swapping TetA and TetB leaves every energy of the pixel and of the tiling unchanged, and conjugates the tiling's wave phase (R1). This is the same split as in the Gram-matrix proof: the metric is blind to the root and the frame carries it.
2. **That phase has the parity character, and it changes sign at the ring.** In the tiling's waves, the TetA/TetB asymmetry enters only through $k_xk_yk_z$, the $xyz$ Walsh function in momentum space, with strength $2\mu - 1 = (x-1)/(x+1)$ (R2). It is zero on Letter 3's white ring and has opposite signs inside and outside it.
3. **The horizon gives the right form for the fixed TetB coupling, but not the right factor.** Take the tiling's coupling amplitudes as the Unruh temperature of the local acceleration (TetA) and the Gibbons–Hawking temperature of the cosmic horizon (TetB). That gives exactly $\mu = x/(1+x)$ with $x = g/(cH)$, so $a_0 = cH$. That is 5.7 times the observed $a_0$. The repo's $a_0 = cH/2\pi$ fits the data (0.90 of $1.2\times10^{-10}$ at $H_0 = 70$) but needs a further $1/2\pi$ that the standard temperatures do not supply (R3).

| Test | Verdict | Result |
|---|---|---|
| R1 energies against phases | **PASS** (expected) | Isolated pixel: the characteristic polynomial depends on the couplings only through $t_A^2 + t_B^2$. Tiling: exchange sends $F(k) \to F(k)^*$, so $\lvert F\rvert^2$ and both bands are unchanged, while the Bloch phase reverses (e.g. $+0.0167 \to -0.0167$ at a generic $k$). |
| R2 the asymmetry in the waves | **PASS** (expected) | $F(k) = (t_A + t_B)\,[4 - k^2/2 + (k_x^4 + \dots + 6k_x^2k_y^2 + \dots)/96] - \tfrac{i}{2}(t_A - t_B)\,k_xk_yk_z + O(k^5)$. The only odd term is the parity character. $\arg F = -(\sigma/8)\,k_xk_yk_z + O(k^5)$, with $\sigma = 2\mu - 1$; under the tiling law $\sigma = (x-1)/(x+1)$. It is zero at the ring, reverses across it, and is odd under exchange and under parity. |
| R3 the horizon reading | **PASS** (reported) | Amplitudes proportional to temperatures in the tiling give $x = g/(cH)$, the right form, with $a_0 = cH = 6.8\times10^{-10}$ m/s². The repo's $a_0 = cH/2\pi = 1.08\times10^{-10}$ m/s² matches the observed value but does not follow from the standard temperatures. The isolated picture with squares gives $(g/cH)^2$, with no Tully–Fisher. |

## What this adds

- **Where the root lives in the pixel lattice.** Not in the spectrum, which is exchange-blind, but in the wave phase. The Gram-matrix proof says the same of the metric and the frame, and Letter 2 says the same of the Christoffel part and the torsion.
- **An order parameter for Letter 3's ring.** The coefficient of the $k_xk_yk_z$ phase, $2\mu - 1$, is positive inside the ring (TetA dominant), zero on it, and negative outside (TetB dominant). Letter 3 describes the ring as the equal-share locus. Here it is also where the lattice's parity-odd phase changes sign.
- **A candidate for the fixed TetB coupling, with its one problem stated.** The cosmic horizon's temperature is fixed while the Unruh temperature grows with $g$, which is exactly the pattern the tiling needs. The form comes out right. The scale is off by $2\pi$.

## A note on the repo's derivation

[`GFD_COLES_NOTES.md`](../../../GFD_COLES_NOTES.md) (the CMB paper's summary, "Saturation scale") writes the Gibbons–Hawking temperature as $T_{GH} = \hbar H/(2\pi k_B c)$ and says that with the Unruh relation it gives $a_0 = cH/2\pi$.
- **The written form isn't a temperature.** $\hbar H/(2\pi k_B c)$ is a temperature divided by a speed, and equating it with $T_U$ gives $a = H$, which isn't an acceleration either.
- **The standard form gives $cH$.** With the standard $T_{GH} = \hbar H/(2\pi k_B)$, the equality gives $a = cH$.
- **What $cH/2\pi$ amounts to.** $cH/2\pi$ corresponds to using the horizon's cycle frequency $H/2\pi$ in place of its rate $H$; the repo's "speed of light over the horizon circumference" describes the same thing. That is a choice the derivation would need to justify.

This note does not change the repo. It is recorded for the author.

## Still open

- **Which picture is GFD's.** Shared corners need the linear law; owned corners need the squared law. The horizon reading of R3 has the right form only in the shared-corner (tiling) picture, which leans toward the tiling.
- **The factor of $2\pi$** in $a_0 = cH/2\pi$.
