# Drain-classifier study: pre-registration

*Field Dynamics Research, written 2026-11-20 before any velocity dispersion was compared with a prediction. Committed to the repository before the analysis script was run, so the git history records the order.*

## Purpose

The [net-field rule](../../proofs/net-field-rule/) says μ acts only on a field that has a drain. Its data test assigned "drained" or "not drained" by object type, using three objects. A label chosen by type, after looking at the dynamics, could fit anything. This study fixes the label **in advance from non-dynamical data**, then tests the predictions on a larger, independent sample.

## Data

The Local Volume Database (Pace et al., [github.com/apace7/local_volume_database](https://github.com/apace7/local_volume_database)), commit `f0b7356` (2026-11-20). Tables: `dwarf_mw`, `dwarf_m31`, `dwarf_local_field`, `gc_harris`, `gc_mw_new`, `gc_ambiguous`.

The catalogue's own "galaxy" label is **not** used as a classifier, because for the smallest systems it is assigned partly from their dynamics.

## Sample cuts (fixed in advance)

- A measured line-of-sight velocity dispersion `vlos_sigma` with errors (upper limits excluded), `M_V`, `rhalf_sph_physical` and a distance to the host.
- Excluded as not in dispersion-supported equilibrium: the LMC, the SMC, the Sagittarius dwarf (disrupting), and any object whose catalogue entry has no host distance.
- Hosts: Milky Way (baryonic mass 6 × 10¹⁰ M☉) and M31 (1.0 × 10¹¹ M☉); field dwarfs are treated as isolated.

## Classifiers (fixed in advance)

| | Drained if | Basis |
|---|---|---|
| **C1, structural** | spherical half-light radius r_h ≥ 20 pc | the size distribution alone: star clusters lie mostly below 15 pc, galaxies mostly above 30 pc, and the overlap is 15–30 pc; 20 pc is set inside the overlap without reference to any dispersion |
| **C2, chemical** | a resolved spectroscopic metallicity spread, σ[Fe/H] ≥ 0.10 dex (a measured value, not an upper limit) | self-enrichment, i.e. a history of gas cycling through the system's own potential; objects without a measurement are left unclassified by C2 |

Reading C2 in the framework's terms: a drained field is one through which matter has flowed into TetB, and a spread of metallicities records that the system once held and processed gas in its own field. This is a hypothesis about what a drain is, stated before the test.

## Predictions (fixed in advance)

- Stellar mass: L_V from M_V (M_V,☉ = 4.83) with M/L_V = 2 for every object (old populations). Sensitivity reported for M/L_V = 1 and 3.
- Dispersion estimator (Wolf et al. 2010): σ_N² = G M / (8 R_e), with R_e = `rhalf_sph_physical`.
- Host's net field at the object: g_e = F(G M_host/D²), with F the drained law. Its Newtonian equivalent is g_e μ(g_e/a₀).
- **Not drained (Newton):** σ = σ_N.
- **Drained (GFD):** σ² = σ_N² ν(y), with y = (g_e μ(g_e/a₀) + g_in)/a₀, g_in = G(M/2)/r_{1/2}², r_{1/2} = 4R_e/3, and ν(y) = ½ + √(¼ + 1/y). This is the quasi-Newtonian estimate with the host field included.
- a₀ = 1.2 × 10⁻¹⁰ m/s².
- Uncertainty: the measured error in quadrature with a 20% model error on σ (from M/L and the estimator).

## What is compared

For each classifier, the χ² per object and the fraction of objects within 3σ, for:
1. the classifier's predictions (drained → GFD, not drained → Newton);
2. Newton for everything;
3. GFD for everything (an acceleration-only rule).

The main comparison uses the **informative subset**: objects where the two predictions differ by more than the combined uncertainty (ν > 1.5). Results are reported whatever they are, including failures.

## What would count against the drain criterion

- A classifier whose predictions do no better than the better of "Newton for everything" and "GFD for everything" on the informative subset.
- Systematic misfits on one side of the threshold, for example large star clusters that are not Newtonian, or compact galaxies that are.
