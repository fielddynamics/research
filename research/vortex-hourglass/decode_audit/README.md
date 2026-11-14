# Drive and Brake from Full Decoded Profiles: Audit and Results

*Field Dynamics Research, 2026-11-14. Criteria fixed and committed first ([`CRITERIA.md`](CRITERIA.md), commit `10ada6b`), then every SPARC galaxy measured. Pipeline: [`decode_audit.py`](decode_audit.py); post-hoc checks: [`posthoc_checks.py`](posthoc_checks.py).*

---

## Version 2 (canonical): the photometric mass exactly as the letter's pipeline builds it

*Added 2026-11-14 at Stephen Nelson's instruction. Version 1 below built $M_{\rm phot}$ itself, from SPARC surface brightness for the stars and a velocity-based estimate for the gas. That was not what the letter does, and Version 2 replaces it.*

**What the letter does.** Its general script, [`generate_from_api_galaxy.py`](../../../papers/letter-decoding-mass-from-rotation-curves/research/generate_from_api_galaxy.py), takes each galaxy's observations and `mass_model` from the [Gravis](https://github.com/fielddynamics/gravis) catalogue and computes $M_{\rm phot}(r)$ with Gravis's `physics/mass_model.enclosed_mass`: a Hernquist bulge plus an exponential disk and an exponential gas disk. For SPARC galaxies, Gravis builds the mass model from SPARC table 1 (`data/build_sparc_sources.py`):
- **disk:** $M = 0.5\,L_{[3.6]}$, with scale length $R_{\rm disk}$;
- **gas:** $M = 1.33\,M_{\rm HI}$, with scale length $R_{\rm HI}/3$;
- **bulge:** $M = 0.15\,M_{\rm disk}(V_{\rm bul,max}/V_{\rm disk,max})^2$, with $a = 0.3$ kpc.

[`decode_audit_paper_mphot.py`](decode_audit_paper_mphot.py) uses those observations, mass models and `enclosed_mass` unchanged (Gravis commit `c19da3a`), and the letter's own decode, smoothing and bounds. The area metric, classes and H3 are the ones in [`CRITERIA.md`](CRITERIA.md). Gravis's observations equal SPARC's exactly. Results are in [`results_paper_mphot/`](results_paper_mphot/).

**Results (175 galaxies; quality cut 149):**

| | All | Quality cut | Robust to M/L ×0.8–1.2 |
|---|---|---|---|
| Drive | 34 (19%) | 28 (19%) | 20 |
| Quiet | 82 (47%) | 76 (51%) | 49 |
| Brake | 59 (34%) | 45 (30%) | 36 |

**H3 passes:**

| Sample | N | $\rho(f_{\rm in}, A)$ | one-sided $p$ |
|---|---|---|---|
| (a) all quality-cut | 149 | +0.47 | < 0.0001 |
| (b) not gas-dominated | 90 | +0.32 | 0.0008 |
| no bulge | 118 | +0.50 | < 0.0001 |
| gas-dominated | 59 | +0.51 | < 0.0001 |

By ring position:

| | N | median $A$ | Classes |
|---|---|---|---|
| Whole galaxy outside the ring | 74 | −0.24 | 6 drive, 34 quiet, 34 brake |
| Ring inside the data | 72 | +0.04 | 20 drive, 41 quiet, 11 brake |
| Whole galaxy inside the ring | 3 | +0.32 | |

**Post-hoc** ([`results_paper_mphot/posthoc_output.txt`](results_paper_mphot/posthoc_output.txt)):
- **The shared trend is still there.** $\Delta$ follows acceleration in every galaxy: −0.95 dex in the deepest field, rising to +0.10 to +0.12 around and inside the ring.
- **A galaxy-level part survives its removal:** $\rho = +0.27$ ($p = 0.0005$) over all galaxies and $+0.22$ ($p = 0.019$) not gas-dominated.
- **Not the form of μ.** McGaugh's empirical relation gives the same result: $\rho = +0.48$ and $+0.33$. *(Numbers updated 2026-11-14 after a tie-handling bug in the rank correlation was fixed; see [`referee_review.md`](referee_review.md), M9.)*

**CamB.** With the letter's pipeline the gap at 1.79 kpc is 0.77 dex (5.9×), not the 0.42 dex of the letter's Figure 2. The reason is that the letter's CamB figure uses a hand-set mass model in `generate_letter_figures.py`: a disk of $3.75\times10^7$ with $R_d = 1.0$ kpc, and gas of $6.25\times10^8$ with $R_d = 26.48$ kpc. Its own catalogue has CamB's disk at $R_d = 0.47$ kpc (SPARC's measured value) and its gas at $1.6\times10^7$, $R_d = 0.40$ kpc (1.33 × SPARC's $M_{\rm HI}$). The figure's gas mass is 39 times SPARC's. Both versions show CamB as a brake; the figure's depth comes from parameters that differ from the catalogue. **Corrected 2026-11-14:** the figure's CamB values had been read from the neighbouring columns of SPARC table 1 (gas $6.251\times10^8 = 1.33\times R_{\rm disk}$, gas $R_d = 26.48 = {\rm SB}_{\rm disk}/2.5$, disk $R_d = 1.0$ = parser default). The letter's scripts now use the catalogue values, and Figure 2 is regenerated: 0.77 dex at 1.79 kpc, matching this audit.

Reproduce: `python decode_audit_paper_mphot.py GRAVIS_DIR` then `python posthoc_checks.py results_paper_mphot`.

**Diagnostic D1: dependence on the photometric method** (added 2026-11-14; [`../measured_partition.py`](../measured_partition.py), [`../ROLL_RATIO.md`](../ROLL_RATIO.md)). The letter works, by its own statement, in the spherical limit: it turns $M_{\rm phot}$ into an acceleration as $GM_{\rm phot}/r^2$, which understates a thin disk's pull inside a few scale lengths. Its gas is a model exponential disk. D1 measures the cost of that declared simplification ([`diagnostic_d1.py`](diagnostic_d1.py), [`results_paper_mphot/diagnostic_d1_output.txt`](results_paper_mphot/diagnostic_d1_output.txt)). Replacing that $g_{\rm bar}$ by SPARC's own Newtonian $g_{\rm bar}$ (thin disks, measured HI maps) weakens H3 from $\rho = +0.47$ to $+0.16$ ($p = 0.02$), and in galaxies that are not gas-dominated from $+0.32$ to $+0.14$ ($p = 0.10$, not significant). Galaxies entirely outside the ring move from a median net area of −0.24 dex (brake) to −0.03 dex (quiet). **H3 passes under the letter's method, but most of its signal comes from that method's approximations.**

---

# Version 1 (superseded: photometric mass built by the audit)

## Summary

- **The decode is correct.** It runs the [decoding-mass letter](../../../papers/letter-decoding-mass-from-rotation-curves/)'s own functions and constants, loaded from its script rather than re-typed. It matches the closed form to machine precision at all 3,391 SPARC points, and it reproduces the letter's published M33 value, $1.381\times10^{10}\,M_\odot$ against the quoted $1.38\times10^{10}$.
- **Full profiles replace the single outer point.** For each of 174 galaxies, $M_{\rm dec}(r)$ and $M_{\rm phot}(r)$ are compared at every observed radius, 3,366 in all. The new metric is the area of the profile above and below its baryons.
- **Across SPARC (quality cut, 148 galaxies):** 59% quiet, 19% drive, 22% brake, none mixed. A third of the classes change when the stellar M/L moves by ±20%, so individual classifications are fragile. Brakes are the most robust (30 of 33).
- **H3 passes as pre-registered.** The more of a galaxy lies inside the ring $x = 1$, the higher its net area: $\rho = +0.29$ ($p = 0.0001$) over all galaxies and $\rho = +0.36$ ($p = 0.001$) over galaxies that are not gas-dominated. *(Numbers updated 2026-11-14 after a tie-handling bug in the rank correlation was fixed; see [`referee_review.md`](referee_review.md), M9.)*
- **Post-hoc, the effect has two parts.** Most of it, across the whole sample, is a gap that depends on acceleration in the same way in every galaxy. In star-dominated galaxies, a galaxy-level part survives with that shared trend removed ($\rho = +0.35$, $p = 0.002$). The form of μ is not the cause: decoding with McGaugh et al.'s empirical relation instead gives the same result.

## 1. Audit

| | Check | Result |
|---|---|---|
| A1 | Closed form $rv^4/[G(a_0r + v^2)]$ against the letter's `velocity_decode`, all 3,391 points | max relative difference $8.9\times10^{-16}$ ✓ |
| A2 | Round trip: $M_{\rm dec}$ through the letter's forward relation returns $v$ | $4.4\times10^{-16}$ ✓ |
| A3 | M33 at 17 kpc, from the letter's data and code path | $1.381\times10^{10}\,M_\odot$ (published $1.38\times10^{10}$) ✓ |
| A4 | Constants $G$, $a_0$, kpc, $M_\odot$ as in the letter | identical ✓ |
| A5 | Integrated SPARC surface photometry against SPARC's $L_{[3.6]}$, 175 galaxies | median −0.024 dex ✓ |
| A6 | Velocity smoothing: the letter's `diffraction_smooth`, width 6.2% of the span | loaded from its source ✓ |
| A7 (added) | CamB, which the letter shows with decoded mass below photometric | decode identical; brake in both, by −0.83 dex here and −0.42 dex with the letter's own mass model |
| A8 (added) | The letter's own `run_all_validations.py` reference values, recomputed in dex from its data, mass models and decode ([`verify_against_letter.py`](verify_against_letter.py)) | MW 25 kpc −0.046, M33 17 kpc +0.304, NGC 3198 30 kpc −0.104: all identical to the validations ✓ |

**A8 in detail** ([`results/verify_against_letter_output.txt`](results/verify_against_letter_output.txt)):
- **The letter's reference values reproduce exactly in dex.** MW at 25 kpc, $6.58\times10^{10}$ against $7.31\times10^{10}$, is −0.046. M33 at 17 kpc, $1.38\times10^{10}$ against $6.85\times10^{9}$, is +0.304. NGC 3198 at 30 kpc, $2.60\times10^{10}$ against $3.30\times10^{10}$, is −0.104.
- **On the letter's own four galaxies the area metric gives** MW quiet ($A = +0.01$), M33 quiet ($A = -0.19$), NGC 3198 quiet ($A = -0.07$) and CamB brake ($A = -1.42$).
- **M33 shows why the profile matters.** Its outermost point sits +0.30 dex above its baryons, which read alone would be a drive. Its profile, though, lies mostly *below* them inside, so it averages to quiet.
- **Galaxies in both.** For CamB the decoded mass is identical at all nine radii. The dex differ only through $M_{\rm phot}$, which is 3–3.5 times higher from SPARC photometry than in the letter's model. For NGC 3198, the decoded masses agree within about 0.03 dex beyond 8 kpc, and at 30 kpc the dex are −0.10 (letter) and −0.13 (SPARC). Inside 8 kpc the velocity data differ: the letter uses Begeman's 8-point curve, SPARC 43 points. Both call NGC 3198 quiet.

A7 locates the uncertainty. The decode is exact; $M_{\rm phot}$ is not. For CamB, the SPARC-built photometric mass is about 2.5 times the letter's model, mainly from the gas term (SPARC gives no gas surface-density profile, so gas is estimated as $|V_{\rm gas}|V_{\rm gas}r/G$) and the disk model. The sign agrees; the depth depends on $M_{\rm phot}$.

## 2. Population

The profile gap is $\Delta(r) = \log_{10}[M_{\rm dec}(r)/M_{\rm phot}(r)]$. $A_+$ and $A_-$ are its average height above and depth below zero over $\ln r$, and $A = A_+ - A_-$. Classes use $\tau = 0.15$ dex and the velocity-error counts $f_\pm$ ([`CRITERIA.md`](CRITERIA.md) §4).

| | All (174) | Quality cut (148) | Robust to M/L ×0.8–1.2 (quality cut) |
|---|---|---|---|
| Drive | 36 (21%) | 28 (19%) | 20 |
| Quiet | 93 (53%) | 87 (59%) | 48 |
| Brake | 45 (26%) | 33 (22%) | 30 |
| Mixed | 0 | 0 | 0 |
| Class changes with M/L | 55 | 50 | |

Median $A$ is −0.006 dex in the quality cut: on average the decoded field sits on its baryons. No galaxy crosses from well above to well below its baryons along its profile; where a profile departs, it departs one way.

Every profile is drawn in [`results/profile_atlas.pdf`](results/profile_atlas.pdf): decoded mass (with its velocity-error band) against photometric mass, with the ring marked. Per-galaxy numbers are in [`results/galaxy_summary.csv`](results/galaxy_summary.csv), and per-radius numbers in [`results/profiles.csv`](results/profiles.csv).

## 3. H3: drive and brake against the ring

| Sample | N | $\rho(f_{\rm in}, A)$ | one-sided $p$ |
|---|---|---|---|
| (a) all quality-cut | 148 | +0.29 | 0.0001 |
| (b) not gas-dominated | 71 | +0.36 | 0.0009 |
| no bulge | 120 | +0.31 | 0.0005 |
| gas-dominated | 77 | +0.34 | 0.0013 |

**H3: PASS.** By ring position:

| | N | median $A$ | drive | quiet | brake |
|---|---|---|---|---|---|
| Whole galaxy outside the ring ($x < 1$ everywhere) | 73 | −0.109 | 11 | 35 | 27 |
| Ring inside the data | 72 | +0.029 | 17 | 49 | 6 |
| Whole galaxy inside the ring | 3 | +0.075 | 0 | 3 | 0 |

Locally, in the 72 galaxies that contain the ring, $\Delta$ is higher inside the ring than outside in 67% of them (median +0.064 dex). This is the hourglass direction: drive inside, drag outside.

## 4. Post-hoc checks (after the result; no pass conditions)

**P1. The gap depends on acceleration, in every galaxy alike.** Median $\Delta$ over all points, binned by $x = g_{\rm obs}/a_0$:

| $\log_{10}x$ | −1.5…−1 | −1…−0.5 | −0.5…0 | 0…0.5 | 0.5…1 | 1…2 |
|---|---|---|---|---|---|---|
| points | 76 | 909 | 1088 | 638 | 298 | 106 |
| median $\Delta$ (dex) | −0.75 | −0.10 | +0.08 | +0.08 | +0.02 | −0.04 |

The field sits above its baryons around the ring, at about its baryons in the high-acceleration core, and below them in the low-acceleration exterior, steeply so in the deepest field. Point-level $\rho(\log x, \Delta) = +0.34$.

**P2. Shared trend removed.** Subtracting the median $\Delta(x)$ from every point and recomputing the area:
- **all galaxies:** the ring correlation falls from +0.29 to **+0.09 ($p = 0.15$)**, so across the whole sample the effect is mostly the shared trend;
- **galaxies that are not gas-dominated:** it stays at **+0.35 ($p = 0.002$)**, a galaxy-level effect beyond the shared trend.

**P3. Not the form of μ.** Decoding with McGaugh, Lelli & Schombert (2016)'s empirical relation instead of $\mu = x/(x+1)$ leaves everything in place: $\rho = +0.30$ overall and $+0.37$ not gas-dominated, with the same point-level trend (+0.35).

## 5. What this does and does not show

**Shows:**
- **The decode is right,** and full profiles are now measured for all of SPARC, with an area metric and classes.
- **The predicted direction holds.** Galaxies with more of their mass inside the ring sit higher above their baryons, and within a galaxy the field is higher inside the ring than outside. This holds as pre-registered, and it is not an artefact of the interpolation function.
- **A galaxy-level part survives in star-dominated galaxies,** where $M_{\rm phot}$ is most reliable.

**Does not show:**
- **Whether the shared trend is physical or systematic.** In GFD terms, a gap that rises toward the ring and falls outside it in every galaxy is what the hourglass reading predicts. But the same shape would come from three known systematics: a stellar M/L that varies with surface brightness (the fixed 0.5 overweights low-surface-brightness disks), the spherical gas estimate (which overstates enclosed gas mass inside the gas disk), and rotation that understates circular speed in the slowly rising inner parts of dwarfs (pressure support, beam smearing). The deep-field bin (−0.75 dex, 76 points) is where all three are largest.
- **Reliable individual classes.** A third change with ±20% in M/L.

**To decide:**
- HI surface-density profiles, to replace the gas estimate;
- M/L from colours or population synthesis instead of a single value;
- asymmetric-drift corrections for the dwarfs.

Each of these removes one systematic that could fake the shared trend. If the trend survives all three, it is physical.

## Reproduce

```bash
python decode_audit.py ROTMOD_DIR TABLE1      # audit A1-A6, all galaxies, H3, atlas -> results/
python posthoc_checks.py results              # P1-P3
python verify_against_letter.py results       # A8: dex against the letter's validations
```

`ROTMOD_DIR` holds SPARC's `*_rotmod.dat` mass models (Lelli, McGaugh & Schombert 2016). They are taken from a GitHub mirror of `Rotmod_LTG`, because CDS is not reachable from the build environment; the mirror reproduces all 3,284 points of the repo's cached RAR file to 0.001 dex. `TABLE1` is SPARC table 1, cached in the repo at `papers/07-dual-tetrad-topology-field-origin/v7/python/sparc_tully_fisher_table.dat`. Outputs as run are in [`results/`](results/), including the console logs.
