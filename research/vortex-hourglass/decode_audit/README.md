# Drive and Brake from Full Decoded Profiles: Audit and Results

*Field Dynamics Research, 2026-11-14. Criteria fixed and committed first ([`CRITERIA.md`](CRITERIA.md), commit `10ada6b`), then every SPARC galaxy measured. Pipeline: [`decode_audit.py`](decode_audit.py); post-hoc checks: [`posthoc_checks.py`](posthoc_checks.py).*

---

## Summary

- **The decode is correct.** It runs the [decoding-mass letter](../../../papers/letter-decoding-mass-from-rotation-curves/)'s own functions and constants, loaded from its script rather than re-typed. It matches the closed form to machine precision at all 3,391 SPARC points, and it reproduces the letter's published M33 value, $1.381\times10^{10}\,M_\odot$ against the quoted $1.38\times10^{10}$.
- **Full profiles replace the single outer point.** For each of 174 galaxies, $M_{\rm dec}(r)$ and $M_{\rm phot}(r)$ are compared at every observed radius, 3,366 in all. The new metric is the area of the profile above and below its baryons.
- **Across SPARC (quality cut, 148 galaxies):** 59% quiet, 19% drive, 22% brake, none mixed. A third of the classes change when the stellar M/L moves by ±20%, so individual classifications are fragile. Brakes are the most robust (30 of 33).
- **H3 passes as pre-registered.** The more of a galaxy lies inside the ring $x = 1$, the higher its net area: $\rho = +0.32$ ($p < 10^{-4}$) over all galaxies and $\rho = +0.34$ ($p = 0.001$) over galaxies that are not gas-dominated.
- **Post-hoc, the effect has two parts.** Most of it, across the whole sample, is a gap that depends on acceleration in the same way in every galaxy. In star-dominated galaxies, a galaxy-level part survives with that shared trend removed ($\rho = +0.33$, $p = 0.003$). The form of μ is not the cause: decoding with McGaugh et al.'s empirical relation instead gives the same result.

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
| (a) all quality-cut | 148 | +0.32 | < 0.0001 |
| (b) not gas-dominated | 71 | +0.34 | 0.0014 |
| no bulge | 120 | +0.35 | < 0.0001 |
| gas-dominated | 77 | +0.43 | < 0.0001 |

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
- **all galaxies:** the ring correlation falls from +0.32 to **+0.10 ($p = 0.11$)**, so across the whole sample the effect is mostly the shared trend;
- **galaxies that are not gas-dominated:** it stays at **+0.33 ($p = 0.003$)**, a galaxy-level effect beyond the shared trend.

**P3. Not the form of μ.** Decoding with McGaugh, Lelli & Schombert (2016)'s empirical relation instead of $\mu = x/(x+1)$ leaves everything in place: $\rho = +0.33$ overall and $+0.35$ not gas-dominated, with the same point-level trend (+0.35).

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
```

`ROTMOD_DIR` holds SPARC's `*_rotmod.dat` mass models (Lelli, McGaugh & Schombert 2016). They are taken from a GitHub mirror of `Rotmod_LTG`, because CDS is not reachable from the build environment; the mirror reproduces all 3,284 points of the repo's cached RAR file to 0.001 dex. `TABLE1` is SPARC table 1, cached in the repo at `papers/07-dual-tetrad-topology-field-origin/v7/python/sparc_tully_fisher_table.dat`. Outputs as run are in [`results/`](results/), including the console logs.
