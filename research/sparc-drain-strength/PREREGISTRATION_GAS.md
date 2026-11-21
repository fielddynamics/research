# One Drain, One Strength in Gas-Dominated Galaxies: pre-registration

*Field Dynamics Research, written 2026-11-21 after the first run (4af6de5) and before this one. Committed before the analysis script was written.*

## Why this follow-up

A Burgers drain acts on the whole vortex through one strain rate, so one drain has one strength. In the first run, the inner and outer TetB strengths D of SPARC galaxies disagreed more than their errors allow, but with no direction. A slightly wrong stellar mass-to-light ratio reproduces that: the inner half of a curve is dominated by the stellar disk and the outer half by gas, so the error shifts the two halves differently. The test can be made clean by using galaxies whose visible mass is mostly gas, measured directly from its 21 cm emission, so that the stellar mass-to-light ratio barely matters.

## What a drain vortex does, and what we test

Unchanged from [`PREREGISTRATION.md`](PREREGISTRATION.md): **one drain, one strength.** TetB's strength D = w/a₀, with w = g(g − g_bar)/g_bar, should be the same in the inner and outer halves of each rotation curve.

## Sample (fixed in advance)

The same 163 galaxies and SPARC files as the first run. A galaxy is **gas-dominated** if, at the nominal Υ_disk = 0.5 and Υ_bul = 0.7, gas supplies at least half of g_bar (Vgas² ≥ Υ_disk Vdisk² + Υ_bul Vbul²) at the median point of the inner half and at the median point of the outer half. This selection uses only the mass models, not the observed velocities.

## Method (fixed in advance)

As in the first run: the curve is split at the median radius, one D is fitted in each half, a half counts only if its 1σ range is narrower than 0.6 dex, and the two are compared by z. Errors are SPARC's errV, with a second run using a 5% floor.

**The new requirement is robustness to the stellar mass.** The comparison is repeated at Υ_disk = 0.3, 0.5 and 0.8. If gas really dominates, the verdict must not change across these.

## What would support the hypothesis, and what would count against it

The same criteria as the first run.
- **Supports:** at least 80% of galaxies agree within |z| < 2, and the median z is within 3 standard errors of 0. This must hold at all three values of Υ_disk, with the 5% floor.
- **Against:** fewer than 80% agree, or a systematic offset, at any of the three values.

If the sample has fewer than 10 galaxies that measure D in both halves, the result will be reported as too small to decide.
