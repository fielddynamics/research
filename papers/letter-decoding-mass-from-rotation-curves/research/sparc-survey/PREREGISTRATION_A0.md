# a₀ from the Shape of SPARC Rotation Curves: pre-registration

*Field Dynamics Research, written 2026-11-21 before the measurement was run. Committed before the script.*

## Why

The survey ([`README.md`](README.md)) found that the value of a₀ which makes the median SPARC galaxy quiet depends on the stellar mass-to-light ratio: 1.61, 1.41, 1.245, 1.06 and 0.94 × 10⁻¹⁰ m/s² for Υ = 0.3 to 0.7. So it cannot test a prediction for a₀. The net-field proof gives a way round the stellar mass: [Corollary 1](../../../../proofs/net-field-rule/), the flux involution. Where a galaxy's enclosed visible mass has stopped growing, the *slope* of its rotation curve alone gives μ, and with it a₀. The stellar mass-to-light ratio drops out.

## The candidate values

| Candidate | Value at H₀ = 70 km/s/Mpc | Source |
|---|---|---|
| cH₀/2π (measured frame) | 1.082 × 10⁻¹⁰ | horizon thermodynamics (Paper IV) |
| cH₀/2π × (1 + 0.118), the ring's screening gap 1/2 − 1/φ² | 1.210 × 10⁻¹⁰ | the gap between the one-directional and bound laws at x = 1 |
| cH₀/2π × √(4/π) = 16 G m_e/r_e² | 1.221 × 10⁻¹⁰ (electron tile: 1.225) | the frame factor (Paper IV) |

H₀ itself is uncertain from about 67 to 73 km/s/Mpc, which moves each value by about ±4%. The second and third candidates differ by 0.9%, so no galaxy measurement can separate them. **What this measurement can decide is whether a₀ in galaxies is the plain cH₀/2π or about 12% above it.** Separating those needs a precision of about 5%.

## Method (fixed in advance)

1. **Data.** The 128 SPARC galaxies built exactly by the letter's recipe, with quality 1–2, using SPARC's rotation curves smoothed with the letter's 6.2% Gaussian.
2. **Where the enclosed mass has levelled off.** The letter's photometric recipe gives the shape of M_phot(r), and its growth γ = d ln M_phot/d ln r. Only points with γ < 0.10 are used, and a galaxy is used only if it has at least 4 such points. γ depends only weakly on the stellar mass-to-light ratio. The main run uses Υ = 0.5, with 0.3 and 0.7 as checks.
3. **The slope.** Fit ln v² against ln r over those points to get the slope b, and the flux exponent s = 1 + b.
4. **μ from the slope.** For an enclosed mass growing as r^γ, the flux involution generalises to μ = 2 − (2 − γ)/(2 − s), which for γ = 0 is the proof's μ = 2(1 − s)/(2 − s). The median γ of the points is used.
5. **a₀.** x = μ/(1 − μ), and a₀ = g/x with g = v²/r at the median radius of the points. A galaxy gives a value only if 0.05 < μ < 0.95. Flat or rising outer curves give μ near or below 0, where a₀ cannot be measured.
6. **The sample's a₀.** The median over galaxies, with a 68% interval from 2000 bootstrap resamplings of the galaxies.

## The premise this rests on

In GFD a galaxy's interior can drive or brake. The slope then returns TetB's actual strength in that galaxy's outer region, not the quiet value. One galaxy therefore measures its own TetB pull, and **the sample median estimates the quiet a₀ only if drive and brake balance across the sample.** This is stated before the run.

## What would count as a result

- **Separates the candidates:** the 68% interval excludes either cH₀/2π (1.08) or the enhanced value (about 1.21–1.22), and it holds at Υ = 0.3, 0.5 and 0.7.
- **Does not separate them:** the interval includes both, or the verdict changes with Υ. This will be reported as the precision reached, not as support for either.
- **Fails as a method:** fewer than 15 galaxies give a value.
