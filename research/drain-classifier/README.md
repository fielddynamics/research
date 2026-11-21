# Dwarf Galaxies and Star Clusters, Read as Vortices

*Field Dynamics Research, 2026-11-20/21. Status: exploratory data study, with one pre-registered test. Scripts: `python decode_study.py --from-csv decode_sample.csv` and `python profile_study.py GRAVSPHERE_DIR` (numpy, pandas, scipy). Outputs: [`decode_output.txt`](decode_output.txt), [`profile_output.txt`](profile_output.txt).*

---

> **Status of the dwarf results (added 2026-11-21).** The GFD equations, and the decode in the [decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/), are defined for rotation curves: circular orbits with g = v²/r. Dwarf spheroidals do not rotate, so every dwarf reading here also depends on steps GFD has not established: turning a dispersion into a circular speed, the stars' orbit shapes, binary stars, a single mass-to-light ratio, and the host's field. The dwarf readings (Tests 2 and 3) are therefore exploratory and are not a test of GFD. Test 1 uses no GFD equation, because a system without a drain is Newtonian by the rule, so the cluster result stands. The test of the vortex facts has moved to SPARC rotation curves ([`research/sparc-drain-strength/`](../sparc-drain-strength/)).
>
> **A correction to Test 3's hypothesis.** The framework places the drain's effect by TetB's share, not by distance from the centre. The [tug-of-war proof](../../proofs/constitutive-law-tug-of-war/) says the drain's strength is written in the core and the inflow, *just as drive and brake appear where TetB's share is large and vanish where g is far above a₀*. The vortex core corresponds to where TetB's share is large, the low-acceleration region, and not to the centre of the galaxy. Test 3 assumed the second, so its hypothesis was not the framework's. Read the framework's way, drive that grows outward, where the acceleration falls, is the direction expected.

## What a drain vortex does

Every test in this folder starts from how a water vortex behaves around a drain. The standard model of a steady drain vortex is the **Burgers vortex**. Water flows inward toward the drain and down through it, and as it moves inward it spins faster. The swirl speed at distance r from the centre is

  v(r) = Γ/(2πr) · (1 − e^(−r²/r_c²)),  with core radius r_c² = 4ν/α.

The profile has two parts, and two different things set them. Inside the **core** (r below about r_c) the water turns almost like a solid body. Outside the core the swirl falls off as 1/r. Three facts follow from that formula, and each one becomes a test.

**1. Without a drain there is no steady vortex.** Take the drain away (α = 0) and the vortex spreads and slows: this is the Lamb–Oseen vortex, which decays with time. Nothing behind it keeps the swirl going.

**2. The drain's strength sets the core, and only the core.** The drain strength α sets the core radius.
- A **stronger** drain pulls the core tighter and spins it faster. The swirl rises above its usual value inside the core and is unchanged outside it.
- A **weaker** drain lets the core spread and slow. The swirl falls below its usual value, most at the centre, and again is unchanged outside the core.

**3. The swirl outside the core is set by the circulation, not by the drain.** The far swirl depends only on the circulation Γ, the amount of spin the water brings in from the edge of the basin. It can rise only if more circulation arrives from the edge, or if the flow around the vortex stirs its outer layers.

## How a galaxy maps onto the vortex

In GFD a galaxy is a vortex whose drain is the throat at its centre. The [decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/) sets out how to read it, and the vortex supplies a dictionary:

| Water vortex | Galaxy |
|---|---|
| swirl speed v(r) | circular speed of the stars, from the rotation curve or from the dispersion (v² = 3σ²) |
| inward pressure gradient v²/r | the field g that the kinematics measure |
| the usual (steady) swirl | **quiet**: the GFD law μ acting on the visible mass alone |
| swirl above usual | **drive**: TetB pulling harder than quiet |
| swirl below usual | **brake**: TetB pulling less than quiet |
| no drain | a system with no throat: a star cluster |

The decode measures the reading directly. From the kinematics alone, with no mass model, M_dec = r v⁴/[G(a₀r + v²)], and comparing it with the mass in visible stars gives the reading:
- **quiet** when M_dec ≈ M_phot;
- **drive** when M_dec > M_phot;
- **brake** when M_dec < M_phot.

A reading of drive or brake is a measurement of what the drain is doing, not a failure of μ.

The three vortex facts give three tests:

| Vortex fact | What we test |
|---|---|
| 1. no drain, no vortex | a star cluster has no TetB swirl of its own, so its stars must move exactly as Newton predicts from their visible mass |
| 2. the drain sets the core | each dwarf galaxy reads quiet, drive or brake; drive and brake should sit in the core and fade to quiet outside it |
| 3. the far swirl is set by the circulation | where swirl changes outside the core, the cause is circulation arriving from the edge or stirring by the surrounding flow, not the drain |

## The data

- **Dwarfs and clusters:** every Local Group dwarf galaxy and star cluster in the Local Volume Database (Pace et al., CC0, commit `f0b7356`) with a measured velocity dispersion, magnitude and size. That is 90 dwarfs and 47 clusters ([`decode_sample.csv`](decode_sample.csv)). The LMC, the SMC and the disrupting Sagittarius dwarf and Palomar 5 are excluded.
- **Mass in stars:** a stellar mass-to-light ratio M/L_V = 2 for these old populations, with 1 and 3 checked. For a dwarf, the decode and the visible mass are compared inside the half-light radius r₁/₂ = 4R_e/3 (Wolf et al. 2010).
- **Profiles:** Walker et al.'s star-by-star velocities for eight classical dwarfs, from the GravSphere repository (`github.com/justinread/gravsphere`, commit `09fa555`). Only the binned profiles are stored here ([`profile_bins.csv`](profile_bins.csv)).
- **Hosts:** each dwarf also sits in its host galaxy's drained field (the Milky Way, M31, M33 or the LMC). As a variant, that field is added using each host's visible mass and the GFD law.

## Test 1: star clusters have no drain, so they must be Newtonian

*Vortex fact 1.* A cluster has no throat, so it has no TetB swirl of its own. Its stars should move exactly as Newton predicts from their visible mass. Unlike the other tests, this one has no room for drive or brake, so it can fail outright.

**Result.** The two remote, low-acceleration clusters whose dispersions are measured in their own papers are Newtonian:
- **Palomar 14:** log₁₀(M_Newton/M_phot) = −0.24 ± 0.27 (Jordi et al. 2009);
- **Palomar 4:** −0.06 ± 0.18 (Frank et al. 2012).

Had μ applied to them, they would read at least +0.99 and +0.67 dex.

The ten catalogue clusters at low acceleration that are bright enough to measure cleanly (predicted σ above 1 km/s) also lean Newtonian, though with large scatter: χ²/N is 6.2 for Newton and 7.2 for μ. The faintest catalogue clusters, with predicted σ below 1 km/s (such as Kim 1 and DELVE 4), read 1.7 dex high. That is the amount by which unresolved binary stars inflate dispersions this small, so it is a limit of the measurement, not a reading of the cluster. Sagittarius II, listed as a cluster, reads +1.2 ± 0.2 dex. If it really is a star cluster it contradicts the test, so its classification needs checking.

## Test 2: what each dwarf's drain is doing

*Vortex fact 2.* Each dwarf has a drain, so its decoded reading says whether the drain is quiet, driving or braking.

**Result.** Of the 90 dwarfs, 16 read quiet, 62 drive and 12 brake ([`decode_output.txt`](decode_output.txt)).
- **Quiet:** the bright, gas-rich dwarfs NGC 6822, WLM, Leo I and Andromeda VII.
- **Mild brake, quiet with the host's field added:** Fornax and Andromeda II.
- **Strong drive:** Draco and Ursa Minor (+1.0 to +1.1 dex), and most strongly the faintest dwarfs (Segue 1, +2.5 dex).

Adding the host's field changes the reading only for dwarfs far out in it, such as Crater II and Antlia II. The counts shift with the mass-to-light ratio (quiet/drive/brake = 11/74/5 at M/L = 1 and 17/53/20 at M/L = 3), but the pattern does not.

**What the drive follows.** In a water vortex, how hard the drain works is set by how much flows through it. The framework does not yet name an observable that measures a galaxy's throughput, so this part simply asks which measured property, if any, the reading follows. It follows luminosity:

  log₁₀(M_dec/M_phot) ≈ −0.41 log₁₀ L + 2.8  (Spearman ρ = −0.73, p = 6 × 10⁻¹⁶).

Once luminosity is controlled, nothing else remains: distance from the host, surface density, size, gas content, metallicity spread and which galaxy a dwarf orbits all show no trend (every p > 0.1). Before the control, the Milky Way's satellites seem to drive harder than Andromeda's (+1.09 against +0.34 dex), but only because more of them are ultra-faint. Two cautions apply to the faintest dwarfs. Unresolved binary stars inflate their dispersions, and the outer stars of a small vortex are the most exposed to stirring by the host's flow (vortex fact 3). Dispersions measured over several epochs, which remove binaries, would separate the first effect from a real drive.

## Test 3: where in each dwarf the drive and brake sit

*Vortex fact 2 again.* If the drain alone is changing, the circulation stays fixed. Then drive or brake should sit in the core and fade to quiet outside it:
- **brake:** a deficit deepest at the centre, shrinking outward;
- **drive:** an excess in the core, shrinking outward.

*This prediction was written down and committed before the run ([`PROFILE_PREREGISTRATION.md`](PROFILE_PREREGISTRATION.md), 18e6d9b).*

**How it is measured.** For each of the eight classical dwarfs, the measured dispersion profile σ_obs(R) is compared with the quiet profile σ_quiet(R), which GFD predicts from the stars alone with no free parameter. The quiet profile uses Plummer light, M/L = 2, and the isotropic Jeans equation projected along the line of sight. The reading at each radius is Δ(R) = log₁₀(σ_obs⁴/σ_quiet⁴), positive for drive and negative for brake. Its trend with radius is the slope c₁ of Δ against log₁₀(R/R_h). A falling reading (c₁ < 0) fits a drive confined to the core. A reading that rises to 0 fits a brake confined to the core.

**Result.**

| Galaxy | Core (innermost bin) | Outskirts (outermost bin) | Slope c₁ | Matches the drain-only vortex? |
|---|---|---|---|---|
| Fornax | brake, −0.49 | quiet, −0.02 | +0.42 ± 0.09 | **yes, brake**: deficit deepest at the centre, quiet by 2 R_h |
| Leo I | brake, −0.21 | quiet, +0.20 | +0.49 ± 0.25 | **yes, brake** |
| Leo II | drive, +0.58 | drive, +0.45 | −0.21 ± 0.41 | consistent with core drive, but only 3 bins |
| Sculptor | quiet, +0.18 | drive, +0.63 | +0.48 ± 0.12 | no: the core is quiet and the excess sits outside it |
| Carina | quiet, +0.06 | drive, +0.72 | +0.54 ± 0.16 | no: the core is quiet and the excess sits outside it |
| Sextans | drive, +0.43 | drive, +0.72 | +0.22 ± 0.20 | no: the excess grows outward |
| Draco | drive, +0.90 | drive, +1.43 | +0.46 ± 0.14 | no: the excess grows outward |
| Ursa Minor | drive, +0.58 | drive, +1.29 | +0.46 ± 0.19 | no: the excess grows outward |

**Reading the result through the vortex.**
- **The braking dwarfs behave exactly as a vortex with a weakened drain does.** Fornax and Leo I have a swirl deficit deepest at the centre that fades to quiet outside the core. That is a spread core with the circulation unchanged (vortex fact 2).
- **The driving dwarfs do not behave like a vortex whose drain has simply strengthened.** In Sculptor and Carina the core is quiet and the extra swirl sits outside it. In Draco, Ursa Minor and Sextans the extra swirl is present in the core and keeps growing outward. In a water vortex, extra swirl outside the core cannot come from the drain (vortex fact 3). It comes from more circulation arriving at the edge, or from the surrounding flow stirring the vortex's outer layers. For a dwarf, the surrounding flow is its host galaxy.
- **One caution is about the measurement, not the vortex.** The quiet profile assumes the stars' orbits are equally random in every direction (isotropic). With orbits biased toward circular (β = −0.3), most of the outward rise disappears: only Sculptor keeps a slope above 2σ. With orbits biased toward radial (β = +0.3), it strengthens. The levels, which galaxies drive and which brake, do not depend on this.

**What it means.** The vortex picture passes where the drain alone has changed: the braking dwarfs show the core-only brake a weakened drain produces. The driving dwarfs carry extra swirl outside their cores. A vortex attributes that to the edge, not the drain, so the drive in these dwarfs is not only a drain effect.

## Next: fit each dwarf as a Burgers vortex

The Burgers profile has two numbers that can be fitted to each dwarf: the circulation Γ, which sets the far swirl, and the core radius r_c, which is set by the drain. Fitting both against the quiet profile asks three questions directly:
1. Do Fornax and Leo I need only a larger core, with the same circulation as quiet? That is a pure brake.
2. Do the driving dwarfs need more circulation, a smaller core, or both?
3. If they need more circulation, does it follow how strongly the host's flow acts at their edge?

As before, the predictions will be written down and committed before the fit is run.

## Earlier versions

The first version of this folder ([`drain_classifier.py`](drain_classifier.py), [`PREREGISTRATION.md`](PREREGISTRATION.md), [`results_output.txt`](results_output.txt)) had two problems:
- It scored every dwarf against the quiet state alone and counted every departure as a failure, instead of reading it as drive or brake.
- It dropped 41 dwarfs, including all of Andromeda's, M33's and the LMC's satellites, because it did not recognise the catalogue's host codes (`m_031`, `m_033`, `lmc`).

It is kept for the record.

## Files

| File | Contents |
|---|---|
| [`decode_study.py`](decode_study.py), [`decode_sample.csv`](decode_sample.csv), [`decode_output.txt`](decode_output.txt) | Tests 1 and 2: the decode of 90 dwarfs and the Newtonian test of 47 clusters |
| [`profile_study.py`](profile_study.py), [`profile_bins.csv`](profile_bins.csv), [`profile_output.txt`](profile_output.txt), [`PROFILE_PREREGISTRATION.md`](PROFILE_PREREGISTRATION.md) | Test 3: drive and brake by radius in eight classical dwarfs |
| [`drain_classifier.py`](drain_classifier.py), [`PREREGISTRATION.md`](PREREGISTRATION.md), [`lvdb_sample.csv`](lvdb_sample.csv), [`results_output.txt`](results_output.txt) | The first version, superseded |
