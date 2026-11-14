# The Hourglass Vortex Under Parity

*Working note, Field Dynamics Research, 2026-11-13. Status: research, not a paper. Verification: `python verify_hourglass_lemma.py` (21 checks, exact sympy).*

`vortex` `hourglass` `throat` `Field-Origin` `spatial-parity` `helicity` `chirality` `TetA` `TetB` `research`

---

## Question

In GFD, TetA and TetB together form a vortex: spiral → throat → spiral, like water through a drain. The throat is the Field Origin, the neck of the hourglass (Coles Notes §2–3). TetB is the chamber beyond it, reached only through the Field Origin. The exchange of TetA and TetB is spatial parity, −I, the element that doubles the symmetry of one tetrahedron to that of the stellated octahedron ([Gram-matrix proof](../../proofs/gram-matrix-tetrad-equation/), Theorem 2).

So: what does parity do to an hourglass vortex? Which parts of the flow does it keep, which does it reverse, and where does the vortex's handedness sit?

The constitutive law is not in question here. μ(x) = x/(x+1) is proved ([exchange symmetry](../../proofs/constitutive-law-exchange-symmetry/)), and the [two-connection note](../two-connection-dual-chamber/) shows two fields on the two roots composing as TetA μg plus TetB (1 − μ)g, with odds x. That note also finds the chirality: the axial torsion is zero for any static tetrad, appears only with rotation, and is opposite on the two roots. *If chirality has a role, it is in the rotating (vortex) sector.* This note starts on that sector.

## Set-up

Put the throat at the origin and the axis along z. Split the velocity of an axisymmetric vortex into two parts:
- **the swirl,** the azimuthal component $v_\varphi$, which turns about the axis;
- **the through-flow,** the meridional components $(v_r, v_z)$, which carry the flow in through one spiral, through the throat, and out through the other.

Parity sends every point to its opposite and carries the flow along with it: $(\Pi v)(\mathbf x) = -v(-\mathbf x)$.

## Lemma (the hourglass under parity)

For any axisymmetric velocity field:

**(a)** Π is an involution, and in cylindrical components

$$\Pi:\ (v_r,\ v_\varphi,\ v_z)(r, z) \;\mapsto\; (v_r,\ v_\varphi,\ -v_z)(r, -z).$$

**(b) The rotation is preserved.** The vorticity of the image is $\boldsymbol\omega(-\mathbf x)$: the vortex turns the same way after the exchange. On the axis the vorticity points the same way above and below the throat.

**(c) The through-flow is reversed.** A drain becomes a fountain with the same swirl. The spiral that fed the throat now leaves it, and the one that left it now feeds it. Parity exchanges *which spiral feeds which*; it does not change the turning.

**(d) The handedness is the swirl times the through-flow.** The helicity density $h = \mathbf v \cdot \boldsymbol\omega$ is exactly the cross term

$$h = \mathbf v_{\rm swirl}\cdot\nabla\times\mathbf v_{\rm through} + \mathbf v_{\rm through}\cdot\nabla\times\mathbf v_{\rm swirl},$$

so pure swirl is achiral and pure through-flow is achiral. Under parity, $h[\Pi v](\mathbf x) = -h[v](-\mathbf x)$: the helicity is a pseudoscalar, and the mirror vortex has the opposite handedness. Reversing the swirl alone also reverses it.

**(e)** The throat is the only fixed point of parity.

**(f) Drive and brake are the rate difference.** Let the swirl turn at the mean rate $\bar\Omega$ plus a half-difference $\delta$ that takes opposite signs on the two sides of the throat. Far from it, TetA then turns at $\bar\Omega + \delta$ and TetB at $\bar\Omega - \delta$. Parity keeps $\bar\Omega$ and flips $\delta$, so $\delta = 0$, one rate on both sides, is the only case parity leaves unchanged. With $0 < |\delta| < \bar\Omega$ both chambers turn the same way at different rates, and the difference is a shear across the throat: the radial vorticity there is nonzero exactly when $\delta \neq 0$.

The checks verify (a), (b) and (d) for a general axisymmetric field (arbitrary component functions), and (c), (d) on an explicit smooth, incompressible hourglass: $v_r = -arz$, $v_z = az^2 - w$, $v_\varphi = \Omega r/(1 + r^2)$. For (f) the swirl is $v_\varphi = \frac{r}{1+r^2}\bigl(\bar\Omega + \delta\, z/\sqrt{1+z^2}\bigr)$.

## Reading in GFD

Read with the upper spiral as TetA, the throat as the Field Origin, and the lower spiral as TetB (the framework's reading, not derived here):

- **TetA and TetB share the turning** (b). The rotation is the part of the vortex that parity leaves alone.
- **They exchange roles in the through-flow** (c). Which chamber feeds which is the part parity reverses, so the direction of flow through the Field Origin is what tells the two chambers apart.
- **The vortex's handedness is parity-odd and needs both parts** (d). A vortex that only turns, or only flows through, has no handedness. This is the flow-level counterpart of two results already in the repo:
  - the [Gram-matrix proof](../../proofs/gram-matrix-tetrad-equation/)'s Proposition 1: the two roots differ only in orientation, which flips under parity;
  - the [two-connection note](../two-connection-dual-chamber/)'s chirality: axial torsion is zero when static, switched on by rotation, and opposite on the two roots.

  The helicity adds one thing to these. Rotation alone is not enough; the chirality needs rotation *and* through-flow.
- **Drive and brake are the rate difference across the throat** (f). TetB turns the same way as TetA. Slower, it drags the vortex (brake); faster, it drives it; at the same rate the interior is quiet. Counter-rotation is only the extreme of a brake. The quiet vortex is the pure parity image, and drive or brake is the part of the swirl parity does not produce. It shows up as a shear at the Field Origin. (The framework's position, Stephen Nelson, 2026-11-14.)

## What it does not do

- It is about a velocity field in an observer's space. It does not yet connect the flow to the tetrad's connection, so it does not show that the helicity *is* the axial torsion. That identification is the next step (below), and it has to be derived, not matched.
- The assignment of the upper spiral to TetA and the lower to TetB is the framework's reading.
- It makes no dynamical claim. Nothing here says how fast the vortex turns or what drives it.

## Next

1. **Transport theorem.** Carry a tetrad along a streamline from the TetA spiral through the throat into the TetB spiral. Show that it arrives as Proposition 2(b) of the Gram-matrix proof (connections that differ, by a torsion), not 2(a) (the covariant mirror, identical). Then compute its axial torsion and compare it with the helicity of (d).
2. **Drive and brake against the decoded mass.** By (f), drive and brake are the half-difference $\delta$ of the swirl rates. The archive already measures the drain's output as $\Delta M_{\rm eff} = M_{\rm phot} - M_{\rm dec}$: zero when the interior is quiet, positive or negative when it drives or brakes. The question is whether $\Delta M_{\rm eff}$ is a function of $\delta$, and with which sign convention.

## SPARC checks of the galaxy reading (2026-11-14)

Letter 3's figure, seen from above, looks like a galaxy: a red dome in the middle, a blue disk around it, and the white ring at $x = 1$ between them. Two readings were tested against SPARC, with the hypotheses and pass criteria fixed before the data were examined ([`check_ring_bulge_sparc.py`](check_ring_bulge_sparc.py)). The data are the SPARC mass models (Lelli, McGaugh & Schombert 2016), taken from a GitHub mirror of `Rotmod_LTG` because CDS is not reachable from the build environment. The mirror reproduces all 3,284 points of the repo's cached RAR file to 0.001 dex.

**H1: the ring is the bulge–disk boundary. Fails.** In the 18 galaxies where both crossings lie inside the data, the radius where bulge and disk contribute equally sits a median **0.48 dex (about 3×) inside the ring**. That is worse than the plain baseline of 2.2 disk scale lengths (0.36 dex). The result holds for a bulge M/L of 0.5, 0.7 and 1.0 (0.52, 0.48 and 0.43 dex). The ring lies out in the disk, where the acceleration falls to $a_0$. So the figure's inner region is the high-acceleration, baryon-dominated part of the galaxy, which contains the bulge and much of the disk. It is not the photometric bulge.

**H2: drive and brake follow the share inside the ring. Fails.** Across 148 galaxies, the rank correlation between the mass fraction inside the ring and the outer-half $\log_{10}(M_{\rm dec}/M_{\rm bar})$ is $\rho = +0.08$ ($p = 0.16$). Without bulges it is $\rho = -0.07$ ($p = 0.77$). Galaxies with no ring in the data (all below $a_0$, mostly dwarfs) sit at a median of −0.11 dex, and those with a ring at −0.03 dex. That is the predicted direction, but it is small and not significant. The pipeline has a flat M/L and about 0.18 dex of point scatter, so it can resolve the sign of a trend of this size only weakly.

> **Superseded.** H2 and H2′ below use the outermost point only, without the letter's smoothing. The full-profile audit in [`decode_audit/`](decode_audit/) replaces them: it decodes every radius, uses an area metric, and was criteria-first. Its H3 passes, and a galaxy-level part survives in star-dominated galaxies. Read that first.

**H2′: the same test, decoded as in the decoding-mass letter.** Drive and brake are only known by setting the decoded mass against each galaxy's photometric mass. So H2 was re-run that way, with the criterion fixed before running ([`check_drive_brake_photometric.py`](check_drive_brake_photometric.py)):
- **Method.** $M_{\rm dec}(r) = rv^4/[G(a_0r + v^2)]$ at the outermost point, against the enclosed photometric mass $M_{\rm phot}$. The stellar part integrates SPARC's own disk and bulge surface-brightness profiles; this reproduces SPARC's 3.6 µm luminosities to −0.02 dex. Drive means $M_{\rm dec} > M_{\rm phot}$; brake means the reverse.
- **Population.** Of 149 galaxies, 80% are quiet (within a factor of 2), 7% drive and 13% brake.
- **Result.** The share inside the ring correlates with drive across all galaxies: $\rho = +0.23$, $p = 0.003$. Galaxies entirely outside the ring brake 22% of the time and drive 3%; galaxies with a ring brake 2% and drive 10%. That is the predicted direction. But without bulges the correlation is $\rho = +0.05$ ($p = 0.30$), so **H2′ fails** its pre-set criterion.
- **Confound.** SPARC gives no gas surface-density profile, so the gas mass is estimated as $|V_{\rm gas}|V_{\rm gas}r/G$, which overstates a gas disk's enclosed mass inside its extent. Gas share alone predicts braking ($\rho = +0.35$, $p < 10^{-4}$), and 68 of the 87 all-outside galaxies are gas-dominated. In star-dominated galaxies (gas share < 0.3 or < 0.5), the ring–drive correlation is $\rho = +0.28$ ($p = 0.02$) and $+0.27$ ($p = 0.01$): positive, but marginal at these sample sizes.
- **Reading.** The direction matches the hourglass (outside the ring, drag; inside, drive), and it survives in star-dominated galaxies at about 2.5σ. Most of the brakes, though, are in gas-dominated dwarfs, where this gas estimate cannot separate a real brake from an overestimated $M_{\rm phot}$. Deciding needs HI surface-density profiles for $M_{\rm phot}$, which are not in SPARC's mass-model files.

**What follows.**
- The roll-ratio algebra is untouched: the exchange is parity, the ring is the quiet throat, and the rate difference is the share difference. What failed is the identification of the figure's regions with a galaxy's bulge and disk (H1).
- Drive and brake against the ring: see [`decode_audit/`](decode_audit/). With full profiles the predicted direction holds as pre-registered (H3), and part of it survives the shared acceleration trend in star-dominated galaxies. Whether the shared trend is physical needs HI profiles, colour-based M/L and asymmetric-drift corrections. (Earlier, single-point reading:) drive and brake against the ring are undecided, not refuted. With the letter's decode the trend has the predicted sign and survives in star-dominated galaxies at about 2.5σ, but most brakes sit where the gas estimate is weakest (H2′). The archive's other position, that drive or brake is set at the drain by the TetB in the galaxy's central throat, is not tested here.
- Letter 3 describes the figure's "disk-and-bulge morphology" as the field configuration of any bound mass. These checks say that morphology is the shares' high-acceleration core and low-acceleration exterior, not the stellar bulge and disk. Any reading of the figure as a galaxy's stellar structure should say so.

## The roll ratio

[`ROLL_RATIO.md`](ROLL_RATIO.md) takes one premise: the two chambers roll on each other without slipping at the Field Origin, with radii equal to their shares. From that, the roulette's roll ratio becomes the rate ratio, $\omega_B/\omega_A = x$. Exchange becomes parity, the ring $x = 1$ becomes the quiet throat (drive inside, drag outside), and the shear's rate of change becomes the logistic core $2\mu(1-\mu)$ (16 exact checks). Against the decode audit, the sign structure matches (median $\Delta$ +0.09 dex inside the ring, below zero outside), but the drive–drag crossing sits at $x \approx 0.34$ in all galaxies. In star-dominated galaxies the interval reaches $x = 1$ (exploratory).

## Files

| File | Contents |
|---|---|
| [`ROLL_RATIO.md`](ROLL_RATIO.md), [`verify_roll_ratio.py`](verify_roll_ratio.py), [`compare_roll_ratio_sparc.py`](compare_roll_ratio_sparc.py) | Roll-ratio theorem (16 checks) and its exploratory comparison with the decode audit |
| [`check_drive_brake_photometric.py`](check_drive_brake_photometric.py) | H2′: drive and brake decoded as in the decoding-mass letter ($M_{\rm dec}$ against enclosed photometric mass), the ring correlation, and robustness to the gas estimate |
| [`check_ring_bulge_sparc.py`](check_ring_bulge_sparc.py) | SPARC tests H1 and H2, hypotheses fixed in the docstring. Usage: `python check_ring_bulge_sparc.py ROTMOD_DIR TABLE1` (bulge M/L via `UPS_BULGE`, default 0.7) |
| [`verify_hourglass_lemma.py`](verify_hourglass_lemma.py) | Exact checks of (a)–(f): general axisymmetric field, an explicit incompressible hourglass, and two chambers co-rotating at different rates |
