# Drain-Classifier Study

*Field Dynamics Research, 2026-11-20. Status: pre-registered test, run once, reported as it came out. Pre-registration: [`PREREGISTRATION.md`](PREREGISTRATION.md) (committed before the analysis, 4e71ce6 and 8b75824). Script: `python drain_classifier.py --from-csv lvdb_sample.csv` (numpy, pandas). Output: [`results_output.txt`](results_output.txt).*

---

## The question

The [net-field rule](../../proofs/net-field-rule/) says μ acts only on a field that has a drain. Its data test labelled three objects as drained or not by type. A label chosen after looking at the dynamics could fit anything, so this study fixes the label in advance from non-dynamical data and tests it on a larger sample.

## What was done

Two classifiers were fixed before any dispersion was compared:
- **C1, structural:** drained if the half-light radius is at least 20 pc;
- **C2, chemical:** drained if the stars show a resolved spread in metallicity (at least 0.10 dex), read as a record of gas cycling through the system's own field.

The sample is every Local Group dwarf and star cluster in the Local Volume Database (Pace et al., CC0, commit `f0b7356`) with a measured velocity dispersion, magnitude and size. That is 97 objects, 48 from the cluster tables and 49 from the dwarf tables, after excluding the LMC, the SMC and the disrupting Sagittarius dwarf. Drained objects are predicted with μ, including the host galaxy's field; the others are predicted with Newton. The extracted sample is [`lvdb_sample.csv`](lvdb_sample.csv).

One correction to the script after its first run, recorded here: the excluded objects are named `LMC`, `SMC` and `Sagittarius` in the catalogue, not by their full names, so the first run kept the LMC. Fixing the name changed no conclusion.

## Results

χ² per object on the **informative** objects, those where μ and Newton differ by more than 50% (63 objects for C1, 57 for C2):

| Rule | C1 sample | C2 sample |
|---|---|---|
| The classifier (drained → μ, not drained → Newton) | 10.9 | 11.4 |
| Newton for everything | 46.6 | 50.6 |
| μ for everything (acceleration only) | 10.7 | 11.0 |

The same ordering holds for stellar mass-to-light ratios of 1 and 3.

**1. Systems the classifiers call drained strongly prefer μ to Newton.** On 49 informative dwarfs, χ²/N is 12.5 with μ and 58 with Newton. This is what any MOND-type law predicts, so it supports μ but not the drain criterion in particular.

**2. The test does not separate the drain criterion from an acceleration-only rule.** The objects that would separate them are the informative systems the classifiers call *not* drained: 14 under C1 and 9 under C2. On those, Newton does not fit better than μ (χ²/N 5.5 against 4.6 for C1, and 6.3 against 3.8 for C2). Most of them are ultra-faint star clusters with only a few hundred to a few thousand suns of light, such as Koposov 2, Kim 1 and DELVE 4, whose measured dispersions lie above *both* predictions. Unresolved binary stars inflate the dispersions of systems this faint, so they are weak tests of either rule. Among the brighter ones (more than 10⁴ suns, a cut chosen after the fact), there are only 4 or 5 objects, and the result is mixed.

**3. The pre-registered criterion for failure is met.** The pre-registration said the drain criterion would count against itself if neither classifier beat the better of "Newton for everything" and "μ for everything". Neither does. On this sample the drain criterion adds nothing measurable to the acceleration-only rule.

**4. The clusters that supported the criterion are not in this sample.** The net-field proof's evidence for the bare G came from Pal 14 and Pal 4. The catalogue has only an upper limit for Pal 14 (1.56 km/s) and no dispersion for Pal 4. The evidence for the criterion therefore still rests on those two remote clusters, taken from the original papers.

**5. μ itself underpredicts many dwarfs.** Among the drained, informative objects the median shortfall is 1.9σ, and 37% lie more than 3σ above the prediction. The classical dwarfs fit better (χ²/N 10, median 1.0σ) than the ultra-faint ones (χ²/N 15, median 2.9σ). The largest misfits are Draco, Ursa Minor, Canes Venatici I, Sextans, Antlia II and Andromeda XVIII. MOND has the same tension with these dwarfs. It is usually attributed to tidal stirring, binary stars and departures from equilibrium, but it is a real tension, and the simple dispersion estimator used here does not resolve it.

**6. The size boundary is not clean.** Segue 1 and Willman 1, which are ultra-faint galaxies with spreads in metallicity, sit at 19.5 and 20.0 pc, just below C1's threshold, so C1 calls them star clusters. The chemical classifier calls them galaxies. Neither prediction fits them.

## What this means for the net-field rule

- The rule's statements about the solar system do not depend on this test. Cassini excludes a drain around every star whatever the classification of dwarfs and clusters.
- The claim that *only* the drain criterion fits clusters and dwarfs together rested on three objects, and a larger, pre-registered test does not confirm it. The proof should say so.
- The drain criterion remains a premise whose observable signature has not yet been isolated in the data. Remote clusters with low internal accelerations and well-measured dispersions are the decisive objects (Pal 14, Pal 4, NGC 2419, Pal 3, Pal 15, AM 1). Only one of them, NGC 2419, has a catalogue dispersion, and it is not informative, because μ and Newton differ there by less than 50%.

## Files

| File | Contents |
|---|---|
| [`PREREGISTRATION.md`](PREREGISTRATION.md) | Classifiers, cuts, estimators and failure criterion, fixed before the analysis |
| [`drain_classifier.py`](drain_classifier.py) | The analysis |
| [`lvdb_sample.csv`](lvdb_sample.csv) | The 97 objects used, extracted from the Local Volume Database (CC0) |
| [`results_output.txt`](results_output.txt) | Full output, including M/L sensitivity and the per-object table |
