# One Drain, One Strength: SPARC Rotation Curves

*Field Dynamics Research, 2026-11-21. Status: two pre-registered tests (all galaxies; gas-dominated galaxies), each run once and reported as it came out. Pre-registration: [`PREREGISTRATION.md`](PREREGISTRATION.md) (committed before the run, 72ccae9). Script: `python drain_strength.py ROTMOD_DIR` (numpy). Output: [`drain_strength_output.txt`](drain_strength_output.txt); per galaxy: [`drain_strength_results.csv`](drain_strength_results.csv).*

---

## What a drain vortex does

In the Burgers vortex, the standard model of a steady drain vortex, the drain acts on the whole vortex through a single number, its strain rate α. Water flows inward at u_r = −αr/2 at every radius and leaves through the drain. A vortex has one drain and one α. Making the drain stronger or weaker changes α everywhere at once.

## What we test

In GFD a galaxy is a vortex whose drain is the throat at its centre, and the decode measures the drain's strength as TetB's pull at each radius (tug-of-war proof, Theorem 3):

  w = g (g − g_bar)/g_bar,  D = w/a₀,

where g = v²/r is the measured acceleration and g_bar is the visible matter's. D = 1 is quiet, D > 1 drive and D < 1 brake.

One drain has one strength. So D should be the same at every radius of a galaxy, whatever value it takes. To test this, D is fitted separately in the inner half and the outer half of each SPARC rotation curve, and the two are compared. This uses rotation curves, which is where the decode is defined, so no step from dispersions or orbit shapes is needed.

**Data.** SPARC's per-radius rotation curves (Lelli et al. 2016) for the 155 galaxies, out of the 163 in the repository's RAR letter, with at least six usable points. They use the same mass-to-light ratios as that letter (Υ_disk = 0.5, Υ_bul = 0.7), and errors from SPARC's velocity uncertainties.

## Results

| | Velocity errors only | With a 5% error floor |
|---|---|---|
| Galaxies where both halves measure D | 143 | 139 |
| Inner and outer D agree within 2σ | 29% | 45% |
| Median of log D_out − log D_in | −0.03 dex | −0.01 dex |
| D_out larger than D_in | 45% | 49% |
| Spread of log D_out − log D_in (16–84%) | −0.27 to +0.28 dex | −0.27 to +0.31 dex |
| One D for the whole curve, median | −0.11 dex (close to quiet) | −0.10 dex |

**1. The pre-registered test does not pass.** It required about 95% of galaxies, and at least 80%, to agree within 2σ. Only 29%, or 45% with the error floor, do. Measured against the quoted errors, the inner and outer strengths differ by more than one drain strength allows.

**2. There is no trend outward.** The differences go both ways equally: the median is zero, and the outer half is stronger in half the galaxies. In vortex terms there is no sign of extra swirl at the edge, so in rotating galaxies nothing points to circulation arriving from outside. The spread is about ±0.28 dex in each direction.

**3. The test cannot separate drain strength from the mass of the disk.** The inner half of a rotation curve is dominated by the stellar disk and the outer half by gas. A disk mass-to-light ratio set slightly wrong therefore changes the inner D and the outer D differently. Checked after the fact: in 79% of the galaxies, some disk mass-to-light ratio between 0.2 and 1.0 (median 0.6) makes the two halves agree within 2σ. So the scatter can come entirely from not knowing each disk's mass. This is a limit of the measurement, not a reading of the drain.

**4. Most galaxies are close to quiet.** Fitted with one D over the whole curve, the median galaxy reads −0.11 dex (D ≈ 0.8). The middle two-thirds read between −0.42 and +0.24 dex.

## What it means

- The vortex's prediction that one drain has one strength is not confirmed. At the precision of the quoted errors, the inner and outer halves of many curves disagree.
- The disagreement has no direction. A drain-plus-edge effect (vortex fact 3) would push the outer halves up systematically, and that does not happen.
- The disagreement is about the size that uncertainty in disk mass alone produces. So this test, as designed, cannot tell a varying drain from an imperfectly known disk.

To make it decisive, the disk's mass has to be fixed independently of the rotation curve, for example from stellar population models or near-infrared colours. Alternatively, the test can use galaxies dominated by gas, whose visible mass is measured directly. In such a galaxy one drain, one strength is a clean prediction: D should come out the same in the inner and outer halves.

## Follow-up: gas-dominated galaxies

*Pre-registration: [`PREREGISTRATION_GAS.md`](PREREGISTRATION_GAS.md) (committed before the run, df494d2). Script: `python drain_strength_gas.py ROTMOD_DIR`. Output: [`drain_strength_gas_output.txt`](drain_strength_gas_output.txt).*

**Why.** The first run could not separate a varying drain from an imperfectly known stellar disk. In a galaxy whose visible mass is mostly gas, the gas is weighed directly from its 21 cm emission, so the stellar mass-to-light ratio barely matters and one drain, one strength becomes a clean prediction. Fourteen SPARC galaxies have gas supplying at least half the visible pull in both halves of their curve. They were selected from the mass models alone: D631-7, DDO 154, DDO 161, DDO 168, DDO 170, ESO 444-G084, KK 98-251, NGC 55, NGC 3109, NGC 3741, UGC 731, UGC 5764, UGCA 442 and UGCA 444. The test was repeated at Υ_disk = 0.3, 0.5 and 0.8, and the verdict had to hold at all three.

**Result.**

| Υ_disk (5% error floor) | Agree within 2σ | Median log D_out − log D_in | Outer stronger | Median z |
|---|---|---|---|---|
| 0.3 | 29% | +0.14 dex | 11 of 14 | +2.1 ± 1.6 |
| 0.5 | 21% | +0.23 dex | 11 of 14 | +2.6 ± 1.6 |
| 0.8 | 21% | +0.32 dex | 11 of 14 | +3.0 ± 1.5 |

- **One drain, one strength is not supported here either.** Only about a quarter of these galaxies have the same strength in both halves, against the required 80%, at every Υ_disk. As intended, the stellar mass no longer explains the difference: the result barely changes as Υ_disk goes from 0.3 to 0.8.
- **Unlike the full sample, the disagreement now has a direction.** In 11 of the 14 the outer half is stronger, and the inner half reads below quiet: brake in the inner half, near quiet outside. The median offset is about 1.7 standard errors from zero, so by the pre-registered measure it is not yet significant, and 11 of 14 would arise by chance about 6% of the time. Fourteen galaxies is a small sample.
- **Read through the vortex**, as pre-registered: if the pattern holds up, the outer swirl is stronger than one drain strength sustains. That is either extra circulation arriving at the edge or a weaker inner swirl than a uniform drain gives. The second resembles a vortex whose core has spread (vortex fact 2), the brake pattern Fornax showed.
- **One measurement effect pushes the same way and must be ruled out first.** In small, gas-rich galaxies the gas also has random motions of about 8–10 km/s, comparable to the rotation in their inner parts. Where that support is not fully corrected (asymmetric drift), and where the radio beam smears the inner curve, the measured rotation in the inner half falls below the true circular speed. That reads as brake in the inner half. The next step is to repeat the test using only rotation curves corrected for pressure support, or only radii where rotation is well above the gas dispersion.

## Files

| File | Contents |
|---|---|
| [`PREREGISTRATION.md`](PREREGISTRATION.md) | The vortex reasoning, the method and the criteria, fixed before the run |
| [`drain_strength.py`](drain_strength.py) | The analysis |
| [`drain_strength_results.csv`](drain_strength_results.csv) | Per galaxy: inner, outer and whole-curve D with 1σ ranges |
| [`drain_strength_output.txt`](drain_strength_output.txt) | The summary output |
| [`PREREGISTRATION_GAS.md`](PREREGISTRATION_GAS.md), [`drain_strength_gas.py`](drain_strength_gas.py), [`drain_strength_gas_output.txt`](drain_strength_gas_output.txt) | The gas-dominated follow-up |

The SPARC rotation-curve files are not stored here. They are public (`astroweb.cwru.edu/SPARC/`), and the copy used is in `github.com/Cisneros-Galaxy/RCFM` under `data/Sparc/Rotmod_LTG/`.
