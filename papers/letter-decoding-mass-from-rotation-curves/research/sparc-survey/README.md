# Decoding Mass Across SPARC

*Field Dynamics Research, 2026-11-21. The decoding-mass letter's pipeline, unchanged, run on all 175 SPARC galaxies. Script: `python sparc_survey.py ROTMOD_DIR` (numpy, scipy). Results: [`sparc_survey_results.csv`](sparc_survey_results.csv). Output: [`sparc_survey_output.txt`](sparc_survey_output.txt).*

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

The SPARC rotation-curve files are not stored here. They are public (`astroweb.cwru.edu/SPARC/`). Table 1 is read from [`papers/07-dual-tetrad-topology-field-origin/v7/python/sparc_tully_fisher_table.dat`](../../../07-dual-tetrad-topology-field-origin/v7/python/sparc_tully_fisher_table.dat).
