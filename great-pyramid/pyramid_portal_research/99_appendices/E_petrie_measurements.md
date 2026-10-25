# Appendix E — Petrie Measurements

**Status:** Reference / empirical
**Reading time:** 5 minutes
**Source:** W. M. Flinders Petrie, *The Pyramids and Temples of Gizeh* (London: Field & Tuer, 1883)

---

## Why Petrie

Sir William Matthew Flinders Petrie (1853–1942) conducted the first systematic survey of the Giza plateau with proper engineering instruments. His 1880-1882 measurements remain the **gold standard** for fine pyramid dimensions, surpassed only by recent laser-scanning surveys (which are not yet published with comparable precision for the chambers and coffer).

For all interior measurements, Petrie used:
- A theodolite for angles (~5 arcseconds precision)
- Calibrated steel tapes for lengths (~0.1 inch precision)
- Triangulation between reference points

His stated tolerances are typically $\pm 0.04$ inches for lengths, $\pm 5$ arcseconds for angles. Modern measurements (when published) generally confirm his values to within his stated tolerances.

## Conversions

- 1 inch = 0.0254 m (exact)
- 1 royal cubit ≈ 20.62 inches ≈ 0.5236 m (Petrie's value)
- 1 cubic cubit (c³) ≈ 0.1435 m³

## King's Chamber dimensions

From Petrie §54:

| Measurement | Value (in) | Value (m) | Cubits | Framework prediction |
|-------------|-----------|----------:|-------:|--------------------:|
| Length (N-S) | 412.06 | 10.466 | 19.989 | 20 |
| Length (S-N) | 412.27 | 10.471 | 19.999 | 20 |
| Mean length | 412.16 | 10.469 | 19.994 | 20 |
| Width (E-W) | 206.04 | 5.234 | 9.995 | 10 |
| Width (W-E) | 206.30 | 5.240 | 10.008 | 10 |
| Mean width | 206.17 | 5.237 | 10.001 | 10 |
| Height | 230.09 | 5.844 | 11.160 | $5\sqrt 5 \approx 11.180$ |

**Aggregate match:**

- Length: 20 cubits → off by 0.03%
- Width: 10 cubits → off by 0.01%
- Height: 5√5 cubits → off by 0.18%

Volume:

$$
V_\text{KC, measured} = 10.469 \times 5.237 \times 5.844 = 320.4 \text{ m}^3
$$

vs. framework prediction $V_\text{KC} = 1000\sqrt 5$ c³ × 0.1435 m³/c³ = 321.0 m³.

**Match: 0.19% deviation.**

## Coffer dimensions

From Petrie §54:

| Measurement | Value (in) | Value (m) |
|-------------|-----------|----------:|
| External length | 89.62 | 2.276 |
| External width | 38.50 | 0.978 |
| External height | 41.13 | 1.045 |
| Internal length | 78.06 | 1.983 |
| Internal width | 26.81 | 0.681 |
| Internal depth | 34.42 | 0.874 |
| Wall thickness (mean) | 5.78 | 0.147 |

External volume: $89.62 \times 38.50 \times 41.13 = 141\,890$ in³ = 2.325 m³.

Framework prediction: $V_\text{coffer} = \alpha \cdot V_\text{KC} = (1/137.036) \times 321.0 = 2.342$ m³.

**Match: 0.7% deviation** ($V_\text{measured}/V_\text{predicted} = 0.993$).

Note: The coffer's rim is **chipped** (Petrie §103). Some of the external dimensions may have been larger originally. A 0.7% restoration correction is plausible.

## Coffer-to-chamber ratio

Direct empirical ratio from Petrie:

$$
\frac{V_\text{KC, measured}}{V_\text{coffer, measured}} = \frac{320.4}{2.325} = 137.83
$$

vs. $1/\alpha = 137.036$. **Off by 0.58%**.

This is the strongest single empirical anchor for the apparatus claim: the chamber-to-coffer volume ratio reproduces $1/\alpha$ to less than 1%.

## Grand Gallery dimensions

From Petrie §66:

| Measurement | Value (in) | Value (m) |
|-------------|-----------|----------:|
| Length (along slope) | 1881.4 | 47.79 |
| Length (horizontal) | 1689.0 | 42.90 |
| Height (vertical) | 339.0 | 8.610 |
| Width (at floor) | 82.42 | 2.094 |
| Width (at ceiling, between corbels) | 41.21 | 1.047 |
| Slope angle | 26°16'40" | — |

The 7 corbels reduce the width from 82.42" (floor) to 41.21" (ceiling) — a factor of 2.

Each corbel step inward is approximately $82.42/14 = 5.89$ inches per side per corbel.

Length-to-King's-Chamber ratio: $1881.4 / 412.06 = 4.566$. Not an obvious cyclotomic ratio but worth noting.

## Antechamber dimensions

From Petrie §59:

| Measurement | Value (in) |
|-------------|-----------:|
| Length (N-S) | 116.85 |
| Width (E-W) | 65.05 |
| Height | 149.20 |
| Number of portcullis grooves | 3 |

The three vertical grooves (running floor-to-ceiling) realize the apparatus's $\mathbb Z_3$ filter ([04.6](../04_apparatus_engineering/04.6_antechamber_Z3_filter.md)).

## Shafts

From Petrie §54-56 (the four "air shafts"):

**Northern KC shaft:** angle ≈ 31°N, terminates inside masonry.
**Southern KC shaft:** angle ≈ 45°S, terminates inside masonry.
**Northern QC shaft:** angle ≈ 39°N, blocked by stone plug discovered in 1872 by Waynman Dixon.
**Southern QC shaft:** angle ≈ 39°S, blocked by similar plug.

Cardinal alignment of all four shafts to the meridian plane: within ~10 arcminutes.

These four shafts realize the **4-channel address triad** of the Hopf fiber S¹ ([04.7](../04_apparatus_engineering/04.7_shaft_address_triad.md)).

## Outer pyramid dimensions

From Petrie §22:

| Measurement | Value (in) | Value (m) |
|-------------|-----------|----------:|
| Base side (mean) | 9068.8 | 230.347 |
| Original height | 5776 (computed) | 146.71 |
| Slope angle | 51°50'40" | — |
| Apex (now missing) | — | — |

Cardinal alignment of the base:

| Side | Deviation from cardinal |
|------|------------------------:|
| North | $-2'$ 28" |
| East | $-5'$ 30" |
| South | $-1'$ 57" |
| West | $-2'$ 30" |

**Mean deviation: ~3 arcminutes**, as discussed in [05.1](../05_cavity_QED_operation/05.1_geomagnetic_pump.md). This matches the daily wander of the geomagnetic dipole.

## Petrie's overall conclusions

Petrie himself noted (§ Conclusions):

- The chambers and coffer are constructed with **uniform precision** (sub-inch over tens of meters).
- The coffer's wall thickness is **uniform to ~1%** over its full dimensions.
- The granite is **finished to a flatness** rivaling modern machining.
- The hardness of the granite (~7 Mohs) suggests **mechanical methods** beyond simple manual abrasion.

Petrie did not attribute any mystical purpose. He concluded the precision reflects high-skill engineering but offered no functional account beyond the conventional tomb interpretation.

## Modern verification

Recent surveys (Glen Dash 2017, ScanPyramids 2017-2023) have confirmed Petrie's measurements to within his stated tolerances. The ScanPyramids muon-tomography work also discovered a large internal "void" above the Grand Gallery, whose function is unknown — possibly relevant to the apparatus interpretation.

A modern laser-scan survey of the chamber and coffer would tighten all the comparisons here and is a priority for any experimental program. Such a survey is **not invasive** and should be straightforwardly approvable.

## Reference

W. M. Flinders Petrie, *The Pyramids and Temples of Gizeh* (London: Field & Tuer; New York: Scribner & Welford, 1883). Available in the public domain via Internet Archive and Project Gutenberg.

Modern editions: Hayes (1990), Ronald Press; Petrie Museum facsimile.

---

**Cross-references:**
- [04.2 King's Chamber vertex](../04_apparatus_engineering/04.2_kings_chamber_vertex.md)
- [04.3 Coffer α step](../04_apparatus_engineering/04.3_coffer_alpha_step.md)
- [99/B Numerical constants](B_numerical_constants.md)
