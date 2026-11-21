# One Drain, One Strength: pre-registration

*Field Dynamics Research, written 2026-11-21 before any fit was run. Committed before the analysis script.*

## What a drain vortex does

In the Burgers vortex, the standard model of a steady drain vortex, the drain acts on the whole vortex through a single number: its strain rate α. The inflow toward the drain is u_r = −αr/2 at every radius, and the outflow through the drain is αz. There is one drain and one α, the same everywhere in the vortex. A stronger or weaker drain changes α for the whole vortex at once. It does not take one value near the axis and another far out.

## What that means for a galaxy

In GFD a galaxy is a vortex whose drain is the throat at its centre. The decode ([decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/); [tug-of-war proof](../../proofs/constitutive-law-tug-of-war/), Theorem 3) measures the drain's strength as TetB's pull w at each radius:

  w = g (g − g_bar) / g_bar,  D = w / a₀,

with g = v²/r the observed acceleration and g_bar the acceleration of the visible matter. The reading is quiet at D = 1, drive at D > 1 and brake at D < 1.

The vortex says one drain has one strength. So **D should be the same at every radius of a galaxy**, whatever its value. Equivalently, each galaxy's rotation curve should follow the GFD law with a₀ replaced by a single constant w = D a₀:

  g = ½ [g_bar + √(g_bar² + 4 g_bar w)].

This is a prediction about the shape of each curve, not about the value of D. A galaxy may be quiet, driving or braking, but it should do so with one strength.

## Data (fixed in advance)

- The SPARC rotation-curve files (`Rotmod_LTG`, Lelli et al. 2016), in a copy from `github.com/Cisneros-Galaxy/RCFM` (`data/Sparc/Rotmod_LTG/`).
- The same galaxies and the same mass-to-light ratios as the repository's SPARC RAR letter: the 163 galaxies in [`sparc_rar.csv`](../../papers/letter-radial-acceleration-relation-sparc/supplementary/sparc_rar.csv) (quality 1–2), with Υ_disk = 0.5, Υ_bul = 0.7 and the gas sign convention used there.
- Points with g_bar > 0 and v_obs > 0. Errors on g come from SPARC's errV, σ_g = 2g·errV/v_obs.

## Method (fixed in advance)

1. For each galaxy, split the points at the median radius into an inner half and an outer half.
2. In each half, fit one D by minimising χ² over a logarithmic grid, D from 0.01 to 100. The 1σ range is where χ² is within 1 of its minimum.
3. A half counts as measuring D if its 1σ range in log₁₀ D is narrower than 0.6 dex (a factor of 4). D cannot be measured where g is far above a₀, because there the curve does not depend on w.
4. For galaxies where both halves measure D, compare the two with z = (log D_out − log D_in)/√(σ_in² + σ_out²), using half-widths of the 1σ ranges.
5. As a check, repeat with an error floor, σ_v ⊕ 0.05 v_obs, to allow for inclination and distance.

## What would support the hypothesis, and what would count against it

- **Supports:** the z values scatter as measurement noise, with about 95% inside |z| < 2 and a median near 0.
- **Against:** more than 20% of galaxies with |z| > 2, or a systematic offset, with the median z different from 0 by more than 3 standard errors.
- **Reading an offset through the vortex.** If D_out > D_in systematically, there is extra swirl at the edge, which in a vortex comes from circulation arriving from the edge or from stirring by the surrounding flow, not from the drain. If D_out < D_in systematically, the outer swirl is weaker than one drain strength sustains. Either way the outcome will be reported as found.
