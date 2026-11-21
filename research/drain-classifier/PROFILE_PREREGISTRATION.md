# Drive and brake by radius: pre-registration

*Field Dynamics Research, written 2026-11-20 before any profile was computed. Committed before the analysis script was run.*

## Question

The decode study read each dwarf's drive or brake at one radius. The vortex picture says where the drain's influence should sit. In the tug-of-war proof (Proposition 3), a stronger drain tightens and spins up the core, and far from the core the swirl forgets the drain. The decoding-mass letter puts the drain at the centre, behind the throat. So TetB's drive or brake should be **strongest in the core and fade outward towards quiet**.

## Data

Walker et al.'s star-by-star line-of-sight velocities and photometric membership for eight classical dwarfs: Fornax, Sculptor, Carina, Sextans, Draco, Ursa Minor, Leo I and Leo II. They are taken from the GravSphere repository (`github.com/justinread/gravsphere`, commit `09fa555`, `Data/Walker_dwarfs/`), with the distances used there. Stars are weighted by their membership probability. Luminosities and half-light radii come from the Local Volume Database (commit `f0b7356`).

## Method (fixed in advance)

1. **Observed profile.** Bin the members in projected radius R into bins of equal effective number (at least 60 members each, at most 10 bins). In each bin, find the dispersion by maximum likelihood, with each star's measurement error included and membership weights applied. Errors come from 200 bootstrap resamplings.
2. **Quiet profile.** The stars follow a Plummer profile with the catalogue's half-light radius. Stellar mass is M/L_V = 2 times L_V (sensitivity checked at 1 and 3). The quiet field is the GFD law applied to that mass, g = F(g_N). The host's field is added as a variant, using g = ν(y)g_N with y = (g_N + g_e,N)/a₀. Isotropic Jeans equation, projected along the line of sight, gives σ_quiet(R), with no free parameter.
3. **The reading by radius.** Δ(R) = log₁₀[σ_obs(R)⁴ / σ_quiet(R)⁴]. Positive is drive and negative is brake; in the deep field this equals log₁₀(M_dec/M_phot).
4. **Shape.** For each galaxy, fit Δ(R) = c₀ + c₁ log₁₀(R/R_h), weighted by the errors.

## Hypothesis and what would count against it

- **H (the drain sits in the core):** c₁ < 0, so drive or brake is largest at small R and Δ moves towards 0 outward.
- **Against H:** c₁ ≥ 0 within 2σ in most of the eight galaxies, that is, drive or brake that is constant with radius or grows outward.
- Because isotropy is assumed, the shape is also reported for constant anisotropy β = −0.3 and +0.3. A conclusion that flips with β will be reported as not robust.
