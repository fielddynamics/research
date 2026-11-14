# Referee Review and Response

*An internal review of everything in `research/vortex-hourglass/`, rechecked on 2026-11-14 against a fresh reading of the decoding-mass letter and its supplement, written as a journal referee would write it. It covers the hourglass lemma, the roll-ratio theorem, the SPARC tests, the decode audit and the CamB correction to the decoding-mass letter. Each point records the change made. 2026-11-14.*

---

## Summary of the work

**Proved, given stated premises.**
- **The hourglass lemma** (21 exact checks). Parity keeps a vortex's swirl and reverses its through-flow. Its helicity, the swirl × through-flow cross term, flips sign. Drive and brake, in the rate sense, are the swirl's half-difference across the throat.
- **The roll-ratio theorem** (18 exact checks). If the two chambers roll without slipping, with radii equal to their shares, then:
  - the rate ratio is the odds, $x$;
  - exchanging the chambers keeps the mean and flips the half-difference (its identification with the lemma's parity is a reading);
  - the chambers turn at one rate only at $x = 1$, Letter 3's equal-share ring *(an earlier wording, "the quiet throat", was withdrawn: see the independent-review section)*;
  - the shear changes at $2\mu(1-\mu)$, fastest at the ring.

**Tested against SPARC.**
- **H1:** the ring is the bulge–disk boundary.
- **H2 and H2′:** drive and brake from a single outer point.
- **H3:** drive and brake from full profiles, with criteria committed before measurement.
- **The measured shares** (Letter 3's discs).

**Corrected along the way.**
- **The audit's photometric mass.** It was built by the audit itself; it now follows the letter's pipeline.
- **CamB's mass model in the letter.** Its values had been read from the wrong table columns.
- **A comparison** that read the decoded gap as the theorem's rate difference.

The verifications are exact and reproducible: every script reruns to identical output. The concerns are about **what the data comparisons can support**.

## Major points

**M1. The lemma is fluid kinematics; its link to the tetrad's parity is a reading.** The lemma's Π acts on a velocity field in an observer's space, $(\Pi v)(\mathbf x) = -v(-\mathbf x)$. GFD's parity acts on the frame: $e \to Pe$, or $-I$ on the spatial realisation in the [Gram-matrix proof](../../proofs/gram-matrix-tetrad-equation/). Nothing proves that the vortex's flow is a realisation of the tetrad, so the identifications are readings:
- upper spiral = TetA;
- throat = Field Origin;
- the lemma's Π = the frame's parity.

*Response.* [`LEMMA.md`](LEMMA.md) already labels the assignment "the framework's reading, not derived here". This review records explicitly that the lemma is exact as kinematics, and that its use for TetA and TetB depends on that reading. The transport theorem, the first item under Next in [`README.md`](README.md) and [`LEMMA.md`](LEMMA.md), is the step that would derive it.

**M2. The roll-ratio theorem's content is its premise.** Once the radii are set equal to the shares, $\omega_B/\omega_A = \mu/(1-\mu)$ is an identity. The physics sits in two assumptions:
- no slip at the Field Origin;
- radii = shares.

Neither is derived.

*Response.* The note now says that (i) is an identity, and that the content is the identification and what follows in (ii)–(v). Both premises are listed as unproved, and deriving no-slip is the first item in Next.

**M3. Exchange was checked incorrectly.** The note claimed that exchange "keeps $\bar\omega$ and flips $\delta$". The script checked only that the normalised ratio $\delta/\bar\omega$ flips. And it modelled exchange by swapping the radii with TetA's rate held fixed, which does *not* keep the mean rate.

*Response.* Exchange is now modelled as swapping the two chambers, each taking the other's radius and rate. The script checks four things (18 checks, all passing):
- the exchanged pair still rolls without slip;
- the rate ratio becomes $1/x$;
- the mean rate is kept;
- the half-difference flips.

**M4. "Drive" has two meanings, and under the theorem they come apart.** The hourglass lemma and the theorem's (iii) use the *rate* sense: TetB turning faster or slower than TetA. The decoding-mass letter uses the *mass* sense: $M_{\rm dec}$ above or below $M_{\rm phot}$. With no slip at $\mu(x)$, the chambers turn at different rates everywhere except the ring, yet $M_{\rm dec} = M_{\rm phot}$ everywhere. An earlier version of the roll-ratio note compared the theorem's rate pattern with the decoded gap and reported a match. That comparison was invalid.

*Response.* The note carries a correction section and a "Drive and brake, and what the decode sees" paragraph. A decoded drive or brake measures **slip**, not the rate difference. The data are compared with the theorem only through the shares, which are directly testable: where they meet, how far apart they are, and how much they slip. **Resolved (2026-11-14).** The framework's definition is that drive and brake happen in the interior TetB. Their observable result is the decoded mass sitting above ($M_{\rm dec} > M_{\rm phot}$, drive) or below ($M_{\rm dec} < M_{\rm phot}$, brake) the photometric mass, and reading that result tells what the interior is doing. In the theorem's terms, the interior drives or brakes by departing from the rate the no-slip partition gives it (slip). The rate difference of (iii) is the quiet baseline, not a drive. `LEMMA.md`, `ROLL_RATIO.md` and the README now use only this sense.

**M5. Drive and brake depend on the photometric method.** The decode audit's H3 passes under the letter's pipeline: $\rho = +0.47$ overall and $+0.32$ in galaxies that are not gas-dominated. That pipeline makes two approximations:
- it turns enclosed mass into acceleration as a sphere, $GM/r^2$, which understates a thin disk's pull inside a few scale lengths;
- it models the gas as an exponential disk with scale length $R_{\rm HI}/3$.

With SPARC's own Newtonian $g_{\rm bar}$ (thin disks, measured HI maps), H3 drops to $\rho = +0.16$ ($p = 0.02$) overall and $+0.14$ ($p = 0.10$) in star-dominated galaxies. Galaxies entirely outside the ring move from a median of −0.24 dex (brake) to −0.03 dex (quiet).

*Response.* Diagnostic D1 is now in the decode-audit README and the hourglass README. Both say that the drive/brake pattern against the ring is **not established**: under the letter's method H3 passes, but most of its signal comes from that method's approximations.

**M6. Overstated agreement in the measured partition.** The first write-up made two claims:
- "within about 0.5 dex of the ring" the measured discs follow the theory and mirror each other;
- the slip is under 0.03 dex "within ±0.4 dex".

The outputs show the agreement is narrower:
- at $\log_{10}x = +0.38$, the gap is 0.22 against the theory's 0.41, while $-0.38$ matches (0.42 against 0.41);
- the slip at $+0.38$ is −0.23;
- one quoted slip value came from the star-dominated sample, not the full one.

*Response.* The text now gives the per-bin values:
- the gap equals the theory at $\pm0.12$;
- exchange symmetry holds at the ring and at $\pm0.62$ (0.55 and 0.56), but not at $\pm0.38$;
- the slip is under 0.03 dex for $-0.5 < \log_{10}x < +0.25$ and grows outside that range, more steeply on the inner side.

**M7. The ring crossing under the letter's method depends on weighting.** Binned medians over points give large galaxies, with many points, more weight. The note had said the ring lies inside every 95% interval.

*Response.* [`referee_checks.py`](referee_checks.py) adds three variants: every galaxy weighted equally (R1), bins shifted by half a bin (R2), and unsmoothed velocities (R3). With SPARC's $g_{\rm bar}$ the crossing stays at $x = 1.00$–1.07 under all of them. With the letter's photometric mass and galaxies weighted equally, it is at $x = 1.83$ (1.54–3.10), which **excludes** the ring. The note now says so.

**M8. Forking paths.** Several tests have been run on the same 175 galaxies:
- H1, H2, H2′;
- H3 under two photometric masses;
- the post-hoc checks P1–P3;
- Diagnostic D1;
- the measured partition T1–T3;
- R1–R4.

Only H1, H2 and H3 had criteria fixed before measurement. Everything else is exploratory.

*Response.* Each result is labelled pre-registered or exploratory where it appears, and failed tests are kept in the record (H1, H2, H2′). No exploratory result is presented as a confirmation. In particular, the ring crossing at $x \approx 1$ with SPARC's $g_{\rm bar}$ is described as a consistency check: any law that fits the radial acceleration relation would put $\mu = \tfrac12$ near $g_{\rm obs} = a_0$.

**M9. Tied ranks in the rank correlation.** Every Spearman correlation in this folder ranked with `argsort(argsort(·))`, which breaks ties arbitrarily instead of averaging them. The ring share $f_{\rm in}$ is heavily tied: 74 galaxies have exactly 0. So the correlations depended on row order. (This was found during the recheck: two runs on the same data gave +0.46 and +0.47.)

*Response.* All scripts now use average ranks (`scipy.stats.rankdata`), every test is rerun, and every quoted number is updated. The conclusions hold, with one exception:

| Test | Before | After |
|---|---|---|
| H2, outer half (pre-registered) | +0.08; no bulge −0.07: fail | +0.20 ($p = 0.008$); no bulge +0.11 ($p = 0.11$): **fail** |
| **H2′, outer point, letter's decode (pre-registered)** | +0.23; no bulge +0.05: fail | +0.33; no bulge +0.21 ($p = 0.0094$): **pass**, narrowly |
| H3 v1 | +0.32 / +0.34 | +0.29 / +0.36: pass |
| H3 v2 (letter's pipeline) | +0.46 / +0.33 | +0.47 / +0.32: pass |
| v2, shared trend removed | +0.24 / +0.23 | +0.27 ($p = 0.0005$) / +0.22 ($p = 0.019$) |
| D1, SPARC's $g_{\rm bar}$ | +0.18 / +0.12 | +0.16 ($p = 0.02$) / +0.14 ($p = 0.10$) |

**H2′'s verdict changes from fail to pass.** The record now says so. H2′ is superseded by the full-profile H3 and by D1, whose conclusion is unchanged: the drive/brake pattern against the ring rests mostly on the letter's photometric approximations. D1 itself had been computed inline; it is now a script, [`decode_audit/diagnostic_d1.py`](decode_audit/diagnostic_d1.py), with its output saved.

## Minor points

- **m1. Points with $\mu_{\rm obs}$ outside (0, 1).** These are 157–192 points (5–6%) where $g_{\rm bar} > g_{\rm obs}$. They are kept in the median shares and excluded from the slip, since $\Omega$ is undefined there. The scripts print the counts, and this review now states it.
- **m2. Points within a galaxy are correlated.** Every bootstrap resamples galaxies, not points (2,000 draws for T1, and 1,000 and 400 for R1).
- **m3. Bootstrap noise.** The intervals from `measured_partition.py` (2,000 draws) and `referee_checks.py` (1,000 draws) differ slightly for the same quantity: 0.99–2.72 and 1.05–2.50 for the letter's method. The note says which is which.
- **m4. Errors not propagated.** Distance and inclination errors are not carried through. *(Corrected after the independent review: they do change the binned medians. See M2 in the section below and [`null_simulation.py`](null_simulation.py).)* They would matter for per-galaxy classes, which the decode audit already reports as fragile to M/L.
- **m5. Smoothing mismatch in the diagnostic.** Diagnostic (b) used smoothed $g_{\rm obs}$ against SPARC's unsmoothed $g_{\rm bar}$. R3 reruns it unsmoothed: the crossing is $x = 1.07$ (point-weighted) and $x = 1.00$ (galaxy-weighted). No change.
- **m6. The hourglass example is local.** Its axial velocity grows as $z^2$ away from the throat. That is fine for a local, exact check of the lemma; it is not a global model.

## Findings about the decoding-mass letter's pipeline

These come from reproducing the letter. None changes its text. They are recorded for whoever revises it.

- **F1. CamB's mass model (corrected).** The letter's old CamB values match other columns of SPARC table 1 exactly: R_disk and SB_disk, two places over from M_HI and R_HI. The /2.5 divisor is not Gravis's R_HI/3, so the builder that produced them is unknown. They are corrected to the catalogue values, Figure 2 is regenerated and `run_all_validations.py` passes (commit `cec64d5`):

  | | Was | Equals | Now |
  |---|---|---|---|
  | Gas mass | $6.251\times10^8$ | $1.33 \times R_{\rm disk}$ | $1.596\times10^7$ (1.33 × $M_{\rm HI}$) |
  | Gas $R_d$ | 26.48 kpc | ${\rm SB}_{\rm disk}/2.5$ | 0.40 kpc |
  | Disk $R_d$ | 1.0 kpc | Gravis's parser default (plausible, unproven) | 0.47 kpc |

  One consequence for the text: with the corrected baryons, the ΛCDM curve in panel (a) now passes through CamB's outermost point.
- **F2. Bulge light is counted twice in the SPARC catalogue.** The letter's pipeline (Gravis, `data/build_sparc_sources.py`) sets the disk mass to $0.5\,L_{[3.6]}$ of the *total* light, then adds a bulge on top. In the 29 SPARC galaxies with a bulge, the median bulge share of the light is 0.19. Gravis's stellar mass is a median 1.19 times SPARC's ($0.5L_{\rm disk} + 0.7L_{\rm bulge}$), and up to 2.09 times (R4). That biases bulge galaxies toward brake in the letter's pipeline.
- **F3. Sphere approximation.** The letter states that it works in the spherically symmetric limit (Letter §2; Supplement §2), and its pipeline turns enclosed mass into acceleration as $GM/r^2$. This is a declared simplification, not an error; D1 measures what it costs on SPARC's disks. Inside a few disk scale lengths this understates a thin disk's pull, which:
  - flattens the inner measured shares;
  - moves their crossing outward (to $x = 1.62$ point-weighted, 1.83 galaxy-weighted);
  - produces most of H3's signal (M5).
- **F4. Gas scale length.** The pipeline gives every SPARC gas disk a scale length of $R_{\rm HI}/3$. $R_{\rm HI}$ is the radius where the HI surface density falls to $1\,M_\odot\,{\rm pc}^{-2}$; HI disks are not exponential, and the factor of 3 is a convention. SPARC's own $V_{\rm gas}$ uses the measured HI maps.
- **F5. Drive and brake sign convention.** The letter calls $\Delta M_{\rm eff} = M_{\rm phot} - M_{\rm dec} > 0$ (CamB) "additional field strength sustained by the interior", which reads as a drive. In the archive's convention (EINSTEIN_TETA_PARTITION.md), it is a brake. The Coles Notes already record this. The audit uses the archive's convention.

## Assessment after revision

**The proved parts stand as proved, given their stated premises.** The lemma is exact kinematics. The theorem is exact once no slip and radii = shares are granted, and its exchange step is now checked correctly.

**What the data show** *(revised after the independent review)*: with SPARC's own Newtonian $g_{\rm bar}$, the measured TetA and TetB shares are consistent with $\mu(x)$ within the measurement scatter, including where they meet ($x \approx 1$). A null model that obeys $\mu(x)$ exactly reproduces the departures away from the ring. Two cautions:
- the crossing at $x \approx 1$ carries little weight, because $a_0$ was calibrated on these same galaxies;
- an earlier version of this assessment claimed under 0.03 dex of slip near the ring and "saturation" away from it; both readings are withdrawn.

**Not established:**
- that drive and brake follow the ring (and no GFD paper claims they do);
- that the vortex's helicity is the axial torsion;
- that the chambers do not slip.

**For the decoding-mass letter:**
- CamB is corrected;
- the bulge double count, the sphere approximation and the gas scale length are recorded as F2–F4 for its next revision.

## Independent review (2026-11-14) and the corrections it led to

A separate reviewer, with no access to this analysis's reasoning, reread the papers, reran every script and reported in [`independent_review.md`](independent_review.md). It confirmed:
- the Gram-matrix proof;
- the lemma and roll-ratio algebra;
- the decode and its byte-for-byte reproducibility;
- the substance of the CamB correction.

It found the following, and each is now corrected:

| Finding | Correction |
|---|---|
| **C1.** The ring tests (H2, H2′, H3) test the analyst's premise, not GFD. No paper links drive or brake to the ring; in GFD they happen in the interior TetB at the drain. | The README, the decode-audit README, `ROLL_RATIO.md` and `CRITERIA.md` (with a dated note) now say this plainly. The results stay in the record as the analyst's hypothesis. |
| **M1.** A bootstrap bug in `referee_checks.py`: resampled galaxies collapsed onto one key. | Fixed and rerun. SPARC $g_{\rm bar}$: $x = 1.03$ (0.83–1.41). The letter's method, galaxy-weighted: 1.83 (1.11–3.18), still excluding 1. |
| **M2.** The "slip" and "saturation" away from $x = 1$ are what binning on a noisy $g_{\rm obs}$ produces. This review's m4 ("errors do not change medians") was wrong. | Added [`null_simulation.py`](null_simulation.py): galaxies obeying $\mu(x)$ exactly reproduce the pattern and the crossing ($x = 1.07$). The notes now say the measured shares are consistent with $\mu(x)$ within the scatter, and no slip is claimed. |
| **M3.** "Pre-registered" overstated it: H3's criteria came after H2 and H2′ had been run on the same galaxies. Also, H2′'s criterion was in fact fixed before running, contrary to M8 above. | Wording corrected in the decode audit and in `CRITERIA.md`'s note. |
| **M4.** The crossing at $x \approx 1$ is close to circular, since $a_0$ was calibrated on SPARC. | Called a consistency check with little evidential weight. |
| **M5.** The "quiet throat" conflated the ring (the interaction core, out in the disk) with the throat (the Field Origin, at the drain), and merged two different "half-differences". | Removed; `ROLL_RATIO.md` (ii) and (iii) rewritten. |
| **M6.** The roll-ratio "unification" was overclaimed. | Restated as the roulette written as algebra under a stated premise. |
| **m1.** The A8 output was stale after the CamB fix. | Rerun: CamB is −0.771 dex at its outer point, $A = -2.04$. Text updated. |
| **m2.** The CamB provenance: the columns are two over, and the /2.5 divisor is unexplained. | F1 reworded. |
| **m9.** "The only parity-invariant case" holds for the swirl only, and the script's check was trivial. | `LEMMA.md` and the README reworded; the check replaced with a real one (21/21). |

**Findings for the decoding-mass letter** (M7 and F5 fixed in the letter on 2026-11-14, with the author's approval):
- **M7. CamB's Figure 2, after the correction.** The Newtonian baryonic curve lies above the observed velocities inside about 1 kpc (12.4 against 8.9 km/s), which usually signals non-circular motion in a Q = 2 dwarf. Also, the curve labelled "NFW halo fit" is abundance-matched, not fitted, and it misses the inner points. *Fixed:* the legend and caption now say "NFW halo sized by abundance matching, not fitted". The caption states that the Newtonian curve lies above the data inside 1 kpc and that CamB's SPARC quality flag is 2, so non-circular motion may contribute there.
- **F5, again.** The letter presented CamB, a brake by the framework's definition, as the example of "power output". *Fixed:* §4 now says the sign of $\Delta M_{\rm eff}$ tells what the interior is doing (negative: drive; positive: brake), and calls CamB a brake: its decoded mass lies below the photometric mass at every observed radius, by 0.77 dex at 1.79 kpc. Figure 2's panel (d) and its legends say "brake", and the vortex paragraph says the drain drives or brakes. The letter is still 5 pages.
- **m3.** `run_all_validations.py` checks no CamB number. *Still open.*

**Finding for Letter 2: M8, withdrawn (2026-11-14).** This review and the independent one said Letter 2's Proposition, "a torsionful connection … is therefore root-resolving", was contradicted by the Gram-matrix proof's Proposition 2(a). It is not. 2(a) shows only that the coordinate torsion tensor alone is the same on both roots, as $y = x^2$ is the same for $\pm x$. Letter 2 works with the frame, and the frame-form torsion $T^a = De^a$ reverses with the root exactly as the frame does. Read with the frame's orientation, the torsion's dual reverses sign too, and the torsion-free part has nothing at first order to carry the root. These are now Proposition 3 of the Gram-matrix proof (76/76). Letter 2 is unchanged.

**Gram-matrix proof** (m5–m8): its script labels are realigned with the paper, and its wording is tightened (see the proof's folder).

## Reproduce

```bash
python verify_hourglass_lemma.py                                   # 21/21
python verify_roll_ratio.py                                        # 18/18
python decode_audit/decode_audit_paper_mphot.py GRAVIS_DIR         # decode audit v2 -> decode_audit/results_paper_mphot/
python decode_audit/posthoc_checks.py decode_audit/results_paper_mphot
python measured_partition.py decode_audit/results_paper_mphot measured_partition.png ROTMOD_DIR
python decode_audit/diagnostic_d1.py ROTMOD_DIR                    # D1
python referee_checks.py ROTMOD_DIR GRAVIS_DIR                     # R1-R4
```

`GRAVIS_DIR` is a checkout of [fielddynamics/gravis](https://github.com/fielddynamics/gravis) (commit `c19da3a`). `ROTMOD_DIR` holds SPARC's `*_rotmod.dat` files; the audit README gives their source and validation.
