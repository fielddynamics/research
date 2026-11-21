# Decoding Mass Across SPARC

*Field Dynamics Research, 2026-11-21. The decoding-mass letter's pipeline, unchanged, run on all 175 SPARC galaxies, and what the results can determine. Scripts: `python sparc_survey.py ROTMOD_DIR`, then `python sparc_survey_analysis.py ROTMOD_DIR` (numpy, scipy). Results: [`sparc_survey_results.csv`](sparc_survey_results.csv). Output: [`sparc_survey_output.txt`](sparc_survey_output.txt).*

---

## What the letter measures

The [letter](../../letter.tex) decodes a galaxy's effective mass from its rotation curve alone. The observed circular speed gives the total pull, g = v²/r. The GFD law, inverted, turns that pull into the source pull, and Poisson's equation turns the source pull into a mass:

  M_dec(r) = r v⁴ / [G(a₀r + v²)]  (letter Eq. 5).

No mass model goes in. The decoded curve is then set beside the photometric enclosed mass, M_phot(r), built from the galaxy's starlight and gas. Where the two curves agree, the interior behind the throat is **quiet**. Where the decoded curve lies above the photometric one, the interior **drives** the field beyond what the visible matter sustains. Where it lies below, the interior **brakes** it. The gap between the curves, ΔM_eff(r) = M_phot(r) − M_dec(r), is the letter's measure of what the interior is doing.

This survey measures that gap for every SPARC galaxy as the **area between the two curves** over the observed range:
- **area above:** decoded above photometric (drive);
- **area below:** decoded below photometric (brake);
- **net area:** their difference.

All three are given as fractions of the area under the photometric curve.

## What was run

Every step is the letter's own.

1. **Rotation curve.** SPARC's observed speeds (Lelli et al. 2016), smoothed with the letter's Gaussian (σ = 6.2% of the radial span), with the same setting for every galaxy.
2. **Decode.** The letter's `velocity_decode`, on 500 radii across the observed range. The script reads the letter's `diffraction_smooth` and `velocity_decode` directly from [`figures/generate_letter_figures.py`](../../figures/generate_letter_figures.py), so the code is identical, and it does so without running that script, which would rewrite the letter's figures.
3. **Photometric mass.** Built from SPARC Table 1 exactly as the letter builds it for Camelopardalis B:
   - stellar disk: M = 0.5 L[3.6], exponential, with the catalogued disk scale length R_disk;
   - gas: M = 1.33 M_HI, exponential, with scale R_HI/3.
4. **Check.** For Camelopardalis B the survey returns ΔM_eff = 4.02 × 10⁷ M☉ at the last radius, matching the letter's Fig. 2d (4.03 × 10⁷; the difference is the letter's rounding of the scale lengths).

Two groups cannot follow the recipe exactly and are flagged:
- **32 galaxies have a bulge.** Table 1 gives only their total luminosity, so it is all treated as disk. Their photometric curves are therefore approximate, and they are reported separately.
- **4 galaxies have no catalogued HI radius,** so their gas cannot be built the letter's way.

## Results

| Sample | Galaxies | Quiet | Drive | Brake | Median net area | Middle two-thirds of the sample |
|---|---|---|---|---|---|---|
| **The letter's recipe exactly** (no bulge, R_HI known) | 139 | 6 | 63 | 70 | −6% | −51% to +68% |
| … SPARC quality 1–2 only | 128 | 6 | 62 | 60 | +3% | −40% to +77% |
| Galaxies with a bulge (approximate) | 32 | 6 | 22 | 4 | +35% | −2% to +128% |
| All 175 | 175 | 12 | 87 | 76 | +5% | −43% to +86% |

"Quiet" here means a net area within ±5% of the photometric area. The letter sets no threshold, so this is only a convenience label; the areas themselves are in the CSV.

**Strongest brake** (letter recipe, quality 1–2): UGC 7577 (−95%), Camelopardalis B (−93%), UGC 6628 (−90%), UGC 7125 (−77%), UGC 9992 (−76%), UGC 7559 (−75%), UGC 7866 (−70%) and NGC 4068 (−69%).

**Strongest drive:** UGC 7399 (+303%), NGC 6789 (+284%), ESO 444-G084 (+224%), F571-8 (+183%), F563-V2 (+159%), NGC 2915 (+158%), F568-1 (+156%) and UGC 5721 (+154%).

**Quiet:** F574-1, F571-V1, NGC 5585, UGC 191, NGC 4010 and NGC 247.

## What it shows

- **Most galaxies are not quiet.** Among the 128 galaxies built exactly by the letter's recipe with good data, only 6 have decoded and photometric curves within 5% of each other. The rest split almost evenly: 62 drive and 60 brake.
- **The median galaxy is close to quiet.** The median net area is +3%, so drive and brake balance across the sample, but individual galaxies range widely, from almost entirely braked to more than three times their photometric mass.
- **The strongest brakes are small, faint galaxies.** Camelopardalis B, the letter's own brake example, is the second strongest in the sample.
- **The bulge galaxies lean towards drive.** That is at least partly because their bulge light is treated as disk, which places their photometric mass incorrectly, so their readings should wait for proper bulge models.

## What the survey can determine

*Script: `python sparc_survey_analysis.py ROTMOD_DIR` (after `sparc_survey.py`). Per galaxy: [`sparc_survey_analysis.csv`](sparc_survey_analysis.csv). Output: [`sparc_survey_analysis_output.txt`](sparc_survey_analysis_output.txt). Sample: the 128 galaxies built exactly by the letter's recipe, with SPARC quality 1–2.*

The letter's photometric recipe has one quantity that is not measured directly: the stellar mass-to-light ratio, 0.5 at 3.6 μm. Real stellar populations allow roughly 0.2 to 0.8. So the first question for each galaxy is whether its reading could simply be that number set slightly wrong. The test is to ask what mass-to-light ratio would make the galaxy quiet, that is, give zero net area between the curves.

| Mass-to-light ratio that would make it quiet | Galaxies | What the reading means |
|---|---|---|
| between 0.2 and 0.8 | 62 | **not determined**: the reading could be the stellar mass |
| below 0.2 | 29 | **brake**, with little or no room for stars; 23 of these brake even with no stars at all, because their gas alone outweighs the decoded mass |
| between 0.8 and 1.5 | 22 | leaning towards drive, but within reach of heavier stellar populations |
| above 1.5 | 15 | **drive**, beyond what stars can supply |

**1. About half the readings are not determined yet.** For 62 of the 128 galaxies a plausible stellar mass-to-light ratio makes the two curves agree. Their drive or brake can only be read once their stellar masses are known independently, for example from stellar population models or near-infrared colours.

**2. The brakes in gas-rich dwarfs are robust.** In 23 galaxies the gas alone, weighed directly from its 21 cm emission, outweighs the decoded mass, so they brake whatever the stars weigh. The result does not depend on how the gas is laid out: with SPARC's measured gas distribution instead of the letter's exponential profile, the count is 26. Almost all are small, slowly rotating, gas-rich dwarf irregulars (median rotation 60 km/s, Hubble type 10), among them UGC 7577, KK 98-251, UGCA 444, UGC 7125, DDO 161, DDO 154, IC 2574, UGC 6628 and Camelopardalis B. The letter's own brake example therefore passes this test.

One measurement effect could still lower the reading in galaxies this slow. Their gas also moves randomly, at about 8–10 km/s, and where that is not fully corrected for, the measured rotation falls below the true circular speed.

**3. The drives beyond what stars supply need one check.** Fifteen galaxies would need a mass-to-light ratio above 1.5 to be quiet: ESO 444-G084, UGC 5764, UGC 7399, UGC 6667, F568-1, F563-1, NGC 6789, F563-V2, NGC 2915, UGC 5721, UGC 4325, F568-V1, F571-8, UGC 7608 and F565-V2. Most are low-surface-brightness galaxies, and they are seen much closer to face-on than the rest: median inclination 43°, against 63°.

That matters, because the decoded mass goes as 1/sin⁴i. At 43°, an inclination error of a few degrees changes it by tens of percent. Their inclinations need checking, for example against independent kinematic or optical estimates, before their drive is read as the interior's.

**4. Most galaxies drive at some radii and brake at others.** In 70 of the 128 galaxies, the decoded and photometric curves cross within the observed range. A single net area hides that structure. The letter's profile ΔM_eff(r), radius by radius, is the full measurement.

**5. No global distortion.** Across all 128 galaxies the net area does not follow distance (ρ = +0.05) or inclination (ρ = +0.02). It follows Hubble type, surface brightness and rotation speed only weakly (|ρ| ≤ 0.24).

**In short.** The letter's method gives a firm reading for a minority of SPARC galaxies:
- brake in about two dozen gas-rich dwarf irregulars, independent of the stellar mass and of the gas profile;
- drive in fifteen mostly face-on, low-surface-brightness galaxies, pending a check of their inclinations.

For the other half, the reading cannot yet be separated from the stellar mass-to-light ratio.

## a₀ from the shape of the rotation curves

*Pre-registration: [`PREREGISTRATION_A0.md`](PREREGISTRATION_A0.md) (committed before the run, 2671319). Script: `python a0_from_slope.py ROTMOD_DIR`. Output: [`a0_from_slope_output.txt`](a0_from_slope_output.txt).*

**Why.** The framework makes a prediction for a₀ in galaxies. It is about 12% above the plain horizon value cH₀/2π = 1.08 × 10⁻¹⁰ m/s². The enhancement is either the ring's screening gap, 1/2 − 1/φ² = 0.118, giving 1.210 × 10⁻¹⁰, or the frame factor √(4/π), giving 1.221 × 10⁻¹⁰, which matches the electron tile's 16Gm_e/r_e² = 1.225 × 10⁻¹⁰.

The two enhanced values differ by only 0.9%, so no galaxy measurement can tell them apart. A galaxy measurement could in principle tell either of them from the plain 1.08. The survey alone cannot, because the a₀ that makes the median galaxy quiet moves with the stellar mass-to-light ratio: 1.61, 1.41, 1.245, 1.06 and 0.94 × 10⁻¹⁰ for Υ = 0.3 to 0.7. At the letter's 0.5 it is 1.245, but that is not a measurement.

**The method.** The net-field proof's flux involution removes the stellar mass. Where the enclosed visible mass has stopped growing, the slope of the rotation curve alone gives μ, and from μ follows a₀. On a synthetic galaxy the method returns 1.167 against a true 1.200, a 3% bias.

**The result: the method fails on SPARC.** Only 4 or 5 of the 128 galaxies have at least four measured points where the enclosed visible mass has levelled off (growing less than 10% per e-fold of radius), and only 3 of those give a usable slope, against the 15 required. SPARC's rotation curves end before their gas disks do, so in almost every galaxy the visible mass is still growing at the last measured radius.

**What would work.** Measurements that reach far beyond the gas, where the enclosed mass has certainly stopped growing. Weak gravitational lensing around isolated galaxies (KiDS-1000) extends the radial acceleration relation two decades further out than rotation curves. That is the regime the involution needs, and the SST quasi-static proof shows that lensing sees the same field as orbits (Ψ = Φ).

## Limits of the inputs

- The photometric mass uses one stellar mass-to-light ratio (0.5 at 3.6 μm) and simple exponential profiles, as in the letter. A different stellar mass-to-light ratio moves every disk-dominated galaxy's reading.
- SPARC's rotation curves carry their own distance and inclination uncertainties, which scale the decoded mass.
- The areas are measured only over each galaxy's observed range, as the letter does.

## Files

| File | Contents |
|---|---|
| [`sparc_survey.py`](sparc_survey.py) | The survey, using the letter's own smoothing and decode functions |
| [`sparc_survey_results.csv`](sparc_survey_results.csv) | Per galaxy: quality, flags, observed range, area above, area below, net area, M_dec/M_phot and ΔM_eff at the last radius, reading |
| [`sparc_survey_output.txt`](sparc_survey_output.txt) | The summary output |
| [`sparc_survey_analysis.py`](sparc_survey_analysis.py) | What the survey can determine: the mass-to-light ratio each galaxy would need to be quiet, gas against decoded mass, crossing curves |
| [`sparc_survey_analysis.csv`](sparc_survey_analysis.csv), [`sparc_survey_analysis_output.txt`](sparc_survey_analysis_output.txt) | Its per-galaxy results and summary |
| [`PREREGISTRATION_A0.md`](PREREGISTRATION_A0.md), [`a0_from_slope.py`](a0_from_slope.py), [`a0_from_slope_output.txt`](a0_from_slope_output.txt), [`a0_from_slope_results.csv`](a0_from_slope_results.csv) | a₀ from the shape of the rotation curves: the candidates, the method and its outcome |

The SPARC rotation-curve files are not stored here. They are public (`astroweb.cwru.edu/SPARC/`). Table 1 is read from [`papers/07-dual-tetrad-topology-field-origin/v7/python/sparc_tully_fisher_table.dat`](../../../07-dual-tetrad-topology-field-origin/v7/python/sparc_tully_fisher_table.dat).
