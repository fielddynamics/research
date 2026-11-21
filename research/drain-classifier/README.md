# Decoding the Local Group's Dwarfs and Clusters

*Field Dynamics Research, 2026-11-20. Status: exploratory data study. Script: `python decode_study.py --from-csv decode_sample.csv` (numpy, pandas, scipy). Output: [`decode_output.txt`](decode_output.txt). Data: the Local Volume Database (Pace et al., CC0, commit `f0b7356`).*

---

## How the test is set up

The [decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/) already says what to expect from a galaxy with a drain and how to read it. The kinematics decode an effective mass with no mass model, M_dec = r v⁴ / [G(a₀r + v²)]. Comparing it with the photometric mass then says what the interior behind the throat is doing:
- **quiet** when the two agree;
- **drive** when M_dec > M_phot;
- **brake** when M_dec < M_phot.

A departure from quiet is a measurement of TetB, not a failure of μ.

That sets the study's three parts:

1. **Drained systems: decode them.** Each dwarf galaxy is decoded at its half-light radius r₁/₂ = 4R_e/3, with circular speed v² = 3σ² from its velocity dispersion (Wolf et al. 2010). That is compared with M_phot = (M/L_V) L_V/2, with M/L_V = 2, and the result read as quiet within ±0.2 dex, drive above and brake below.
2. **Systems without a drain: they must be Newtonian.** A star cluster has no interior, so there is nothing to drive or brake. Its Newtonian dynamical mass, 3σ²r₁/₂/G, must equal its photometric mass. This is the part of the test that can fail outright.
3. **Is drive or brake physical?** If it is, the decoded reading should follow something measured independently of the dispersions: environment, structure, gas or chemical history.

The letter's decode uses the system's own field. As a variant, the study also decodes with the drained host's field added (Milky Way, M31, M33 or LMC, each with its baryonic mass and the GFD law).

## Why this replaces the first version

The first version of this folder ([`drain_classifier.py`](drain_classifier.py), [`PREREGISTRATION.md`](PREREGISTRATION.md), [`results_output.txt`](results_output.txt)) scored every dwarf against the quiet state and counted every departure as a misfit of μ. In the letter's terms that is the wrong yardstick. It also had a bug. The catalogue codes Andromeda's satellites as `m_031`, M33's as `m_033` and the LMC's as `lmc`, so the first version silently dropped 41 dwarfs, among them every satellite of Andromeda. This version uses all of them: 90 dwarfs and 47 clusters.

## Results

**1. The decoded dwarfs.** Of 90 dwarfs, 16 read quiet, 62 drive and 12 brake, with a median of +0.68 dex. The bright, gas-rich dwarfs read quiet: NGC 6822, WLM, Leo I and Andromeda VII. Fornax and Andromeda II read mild brake on their own field and quiet once the host's field is added. Draco and Ursa Minor read strong drive (+1.0 to +1.1 dex), and the faintest ultra-faint dwarfs read the strongest drive (Segue 1, +2.5 dex). Adding the host's field changes the reading only for dwarfs far out in their host's field. Crater II and Antlia II move from brake or quiet to drive, because the host's field dominates them. The counts shift with the stellar mass-to-light ratio (quiet/drive/brake = 11/74/5 at M/L = 1, 17/53/20 at M/L = 3), but the pattern does not.

**2. Drive tracks luminosity, and nothing else.** The reading falls steadily with luminosity:

  log₁₀(M_dec/M_phot) ≈ −0.41 log₁₀ L + 2.8  (Spearman ρ = −0.73, p = 6 × 10⁻¹⁶).

Without controlling for luminosity, drive also appears to follow size, surface density, distance from the host, gas content and which host a dwarf orbits. Satellites of the Milky Way read +1.09 dex, satellites of M31 +0.34 and field dwarfs +0.06, and gas-rich dwarfs read quiet while gas-free ones drive. Once luminosity is controlled, every one of these disappears (all p > 0.1). The Milky Way's satellites read higher only because more of them are ultra-faint.

So, on this sample, the decoded drive is a single trend with luminosity: in GFD's reading, TetB drives harder in fainter dwarfs. Standard cosmology reads the same trend as fainter dwarfs being more dominated by dark matter, and MOND as ultra-faint dwarfs lying above its prediction; a referee will raise both. The trend alone does not yet separate TetB's drive from those readings, or from effects of measurement:
- binary stars, which inflate the smallest dispersions;
- tidal heating by the host;
- a dispersion floor in the faintest systems.

To read it as TetB's activity, the framework needs a predictor of drive that is not luminosity.

**3. The clusters.** The ten catalogue clusters that sit at low acceleration and are bright enough for binary stars to matter little (predicted σ > 1 km/s) fit Newton slightly better than μ: χ²/N is 6.2 against 7.2. The scatter is large, and three outliers dominate it: NGC 6229, NGC 6838 and Garro 04. The two remote clusters measured in their own papers are clearer:
- **Pal 14:** log₁₀(M_N/M_phot) = −0.24 ± 0.27, where μ would give at least +0.99;
- **Pal 4:** −0.06 ± 0.18, where μ would give at least +0.67.

Both are Newtonian, as the net-field rule requires of a system without a drain. The faintest catalogue clusters (predicted σ < 1 km/s, such as Kim 1 and DELVE 4) read 1.7 dex above Newton. That is the size of the inflation binary stars produce at such small dispersions, so they do not test either rule. Sagittarius II is listed as a cluster but reads +1.2 ± 0.2 dex. If it really is a star cluster, it is a problem for the rule, and its classification is worth checking.

## What it means

- **The falsifiable part holds where the data are good.** Systems without a drain should be Newtonian. Pal 14 and Pal 4 are, and the cleaner catalogue clusters lean Newtonian. More remote clusters with dispersions measured in their own papers would make this decisive.
- **Drive and brake are measured, but what sets them is open.** Across the Local Group's dwarfs TetB's drive follows luminosity alone. That is not a contradiction of the letter, which leaves the interior dynamics open. It does mean that the next step is a physical predictor of drive that is independent of luminosity, or a way to separate it from binaries and tides, for example by using only multi-epoch dispersions, which remove binaries.
- **The study does not test μ itself in the dwarfs.** Once drive and brake are allowed, a single dwarf cannot falsify μ. That is why the clusters, and a predictor of drive, carry the weight.

## Drive and brake by radius

*Pre-registration: [`PROFILE_PREREGISTRATION.md`](PROFILE_PREREGISTRATION.md) (committed before the run, 18e6d9b). Script: `python profile_study.py GRAVSPHERE_DIR`. Output: [`profile_output.txt`](profile_output.txt), bins in [`profile_bins.csv`](profile_bins.csv).*

**The test.** In the vortex picture a stronger drain tightens and spins up the core, and the far swirl forgets the drain. Read literally, TetB's drive or brake should be strongest at the centre and fade toward quiet outward. Eight classical dwarfs have star-by-star velocities (Walker et al., from the GravSphere repository): Fornax, Sculptor, Carina, Sextans, Draco, Ursa Minor, Leo I and Leo II. For each one:
- the measured dispersion profile σ_obs(R) is compared with the quiet GFD profile σ_quiet(R), computed with no free parameter from the stars alone (Plummer light, M/L = 2, isotropic Jeans equation projected along the line of sight);
- the reading at each radius is Δ(R) = log₁₀(σ_obs⁴/σ_quiet⁴), positive for drive and negative for brake;
- the shape is the slope c₁ of Δ against log₁₀(R/R_h).

The hypothesis was c₁ < 0.

**The result: the drive does not sit in the core. It grows outward.**

| Galaxy | Core (innermost bin) | Outskirts (outermost bin) | Slope c₁ (isotropic) |
|---|---|---|---|
| Fornax | brake, −0.49 | quiet, −0.02 | +0.42 ± 0.09 |
| Sculptor | quiet, +0.18 | drive, +0.63 | +0.48 ± 0.12 |
| Carina | quiet, +0.06 | drive, +0.72 | +0.54 ± 0.16 |
| Sextans | drive, +0.43 | drive, +0.72 | +0.22 ± 0.20 |
| Draco | drive, +0.90 | drive, +1.43 | +0.46 ± 0.14 |
| Ursa Minor | drive, +0.58 | drive, +1.29 | +0.46 ± 0.19 |
| Leo I | brake, −0.21 | quiet, +0.20 | +0.49 ± 0.25 |
| Leo II | drive, +0.58 | drive, +0.45 | −0.21 ± 0.41 |

- No galaxy has c₁ < 0 at 2σ, under any of the assumptions tried: M/L of 1, 2 or 3, the host's field included, or anisotropy β = ±0.3. So the hypothesis is not supported.
- Five of the eight have c₁ > 0 at 2σ when orbits are isotropic, seven when β = +0.3 or when the host's field is included, and one when β = −0.3. The rising trend itself therefore depends on the orbits: if the stars' orbits were tangentially biased, most of it would go.
- The levels are robust and match the single-radius decode. Fornax and Leo I are quiet to braking, while Draco, Ursa Minor and Sextans drive at every radius.

**What it means.** The literal reading of the vortex picture, with drive concentrated in the core, is not what these eight dwarfs show. Where there is drive, it is present from the centre outward and is largest in the outskirts. Three readings remain open:
- in the framework, the drain's influence may reach the far field rather than the core, which the vortex picture as stated in the tug-of-war proof does not say;
- the outskirts are where the Milky Way's tide acts on a dwarf, so tidal heating would raise the outer dispersions;
- the orbits may not be isotropic.

Proper motions of individual stars, which measure anisotropy directly, would separate the third from the first two.

## Files

| File | Contents |
|---|---|
| [`decode_study.py`](decode_study.py) | The decode study |
| [`profile_study.py`](profile_study.py), [`profile_bins.csv`](profile_bins.csv), [`profile_output.txt`](profile_output.txt), [`PROFILE_PREREGISTRATION.md`](PROFILE_PREREGISTRATION.md) | Drive and brake by radius in eight classical dwarfs (velocity data: Walker et al., via github.com/justinread/gravsphere, commit 09fa555; binned profiles only are stored here) |
| [`decode_sample.csv`](decode_sample.csv) | The 137 objects used (90 dwarfs, 47 clusters), from the Local Volume Database (CC0) |
| [`decode_output.txt`](decode_output.txt) | Full output: every dwarf's reading, the clusters, the correlations |
| [`drain_classifier.py`](drain_classifier.py), [`PREREGISTRATION.md`](PREREGISTRATION.md), [`lvdb_sample.csv`](lvdb_sample.csv), [`results_output.txt`](results_output.txt) | The first version, superseded: it scored dwarfs against quiet only and dropped Andromeda's, M33's and the LMC's satellites |
