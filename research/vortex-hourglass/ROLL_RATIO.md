# The Roll Ratio as the Rate Ratio of the Two Chambers

*Working note, Field Dynamics Research, 2026-11-14. Status: research, not a paper. Verification: `python verify_roll_ratio.py` (18 checks, exact sympy). Data: `python measured_partition.py` (Letter 3's discs from SPARC, exploratory). `compare_roll_ratio_sparc.py` is the superseded first comparison, kept for the record.*

---

## Question

Four results in the repo each describe TetA and TetB, and nothing yet ties them together:

- **[Letter 2](../../papers/letter-2-other-half-of-gravity-torsion/):** exchanging the chambers inverts their odds, Ω → 1/Ω, and that forces Ω = μ/(1 − μ) = x.
- **The [roulette](../constitutive-law-u(x)/tetA_tetB_roulette_roll_ratio.html):** TetA is a fixed circle of radius μ and TetB a circle of radius 1 − μ rolling on it, with roll ratio μ/(1 − μ).
- **The [hourglass lemma](README.md):** parity keeps the mean swirl rate of the two chambers and flips their half-difference. Drive and brake are that rate difference.
- **[Letter 3](../../papers/letter-3-field-closure-of-tetrad-frame/)'s figure:** the two shares as surfaces that meet on the ring $x = 1$.

The question is whether the roll ratio is the rate ratio of the vortex's two chambers, and what follows if it is.

## Premise

The two chambers meet at one point, the Field Origin, where both are evaluated together (Coles Notes §2–3: "the neck of the hourglass"). At a shared contact point the velocity is shared from both sides, so the chambers roll on each other without slipping. Their radii are their shares, as in the roulette: $R_A = \mu$ and $R_B = 1 - \mu$, which together fill the unit.

The no-slip reading of the Field Origin is the premise. It is the framework's reading, not derived here.

## Theorem

With $\mu = x/(x+1)$ and no slip, $R_A\,\omega_A = R_B\,\omega_B$:

**(i) The roll ratio is the rate ratio, and it is the odds.** $\omega_B/\omega_A = R_A/R_B = \mu/(1-\mu) = x$.

**(ii) Exchange is parity.** Let $\bar\omega$ be the mean rate and $\delta$ the half-difference of the two chambers. Then

$$\frac{\delta}{\bar\omega} = \frac{1 - x}{1 + x} = 1 - 2\mu .$$

Exchanging the chambers swaps the radii, so $x \to 1/x$. That keeps $\bar\omega$ and flips $\delta$, which is exactly what parity does to the hourglass (lemma (f)). Letter 2's exchange of the chambers and the vortex's parity are the same operation.

**(iii) The ring is the quiet throat.** $\delta = 0$ exactly at $x = 1$, where $\mu = \tfrac12$. Inside the ring ($x > 1$) TetB turns faster: drive. Outside it ($x < 1$) TetB turns slower: drag.

**(iv) The shear changes fastest at the ring.** $\dfrac{d(\delta/\bar\omega)}{d\ln x} = -2\mu(1-\mu)$. This is the logistic law's core term, $x\,d\mu/dx = \mu(1-\mu)$, and it is largest at $x = 1$, where $\mu(1-\mu) = \tfrac14$: the interaction core of Letters 2 and 3.

**(v) The chiral-holonomy twist.** The share difference $\sigma = (x-1)/(x+1)$ that weights the steps of the [chiral-holonomy proof](../../proofs/chiral-holonomy-closed-frame/) is $\sigma = 2\mu - 1 = -\delta/\bar\omega$.

All of (i)–(v) are exact ([`verify_roll_ratio.py`](verify_roll_ratio.py), 18 checks). Given the premise, (i) is an identity: setting the radii equal to the shares makes the rate ratio the odds by definition. The content of the theorem is the identification, and what the premise then implies in (ii)–(v).

**Two senses of drive.** In (iii), "drive" and "drag" refer to *rates*: TetB turning faster or slower than TetA, the hourglass lemma's sense. In the decoding-mass letter, drive and brake are *masses*: $M_{\rm dec}$ above or below $M_{\rm phot}$. Under the premise these come apart. The chambers turn at different rates everywhere except the ring, yet with no slip at $\mu(x)$ the decoded mass equals the photometric mass everywhere. A decoded drive or brake therefore measures slip, not the rate difference of (iii). This matches the decoding-mass letter's own terms. The decode already contains $\mu(x)$ ($g_{\rm s} = \mu\,g_{\rm t}$), so a **quiet interior** ($\Delta M_{\rm eff} = 0$, effective mass equal to the baryons) is no slip, and an **active interior** ($\Delta M_{\rm eff} \neq 0$, the drain's power output) is slip. Which sense the framework means by drive and brake is a question for the framework, recorded here, not settled.

## What it shows

Given the no-slip premise, the roulette is a theorem, not an illustration. One premise turns four objects already in the repo into one:
- Letter 2's odds become the rate ratio;
- Letter 2's exchange becomes the vortex's parity;
- Letter 3's ring becomes the quiet throat;
- the chiral-holonomy twist becomes the rate difference.

## What it does not show

- **Why the contact does not slip.** That is the framework's reading of the Field Origin.
- **The size of anything.** The theorem gives rates, not masses or forces. It predicts *where* drive turns to drag (at $x = 1$), not by how much.

## What the data can test (correction, 2026-11-14)

An earlier version of this note compared the theorem's drive-inside, drag-outside pattern with the decode audit's gap $\Delta = \log_{10}(M_{\rm dec}/M_{\rm phot})$, and reported that "the sign structure matches". **That comparison was wrong.** If the chambers roll without slipping at $\mu(x)$, the decode returns $M_{\rm dec} = M_{\rm phot}$ at every radius: every galaxy is quiet, even though the chambers turn at different rates everywhere except the ring. The rate difference in (iii) does not produce a mass gap. What $\Delta$ measures is the departure of the measured shares from $\mu(x)$:

$$\Delta = \log_{10}\frac{\mu(x)}{\mu_{\rm obs}}, \qquad \mu_{\rm obs} = \frac{g_{\rm bar}}{g_{\rm obs}}, \qquad \Omega_{\rm obs} = \frac{\mu_{\rm obs}}{1 - \mu_{\rm obs}} .$$

With no slip at the *measured* radii, $\Omega_{\rm obs}$ is the measured roll ratio, and $\log_{10}(\Omega_{\rm obs}/x)$ is the **slip**. So the data test the theorem through the shares themselves: where they meet, how far apart they are, and how far the measured roll ratio slips from $x$. That is Letter 3's figure, built from data.

## The red and blue discs, measured (exploratory)

[`measured_partition.py`](measured_partition.py) builds Letter 3's two surfaces from SPARC: blue $\mu_{\rm obs}$ and red $1 - \mu_{\rm obs}$, as medians over $\log_{10}x$ for the 149 quality-cut galaxies. It uses $g_{\rm obs}$ from the letter's smoothed velocities and two versions of $g_{\rm bar}$:
- **(a) the decoding-mass letter's photometric mass,** as the spherical $GM_{\rm phot}/r^2$ (decode audit v2);
- **(b) SPARC's own Newtonian $g_{\rm bar}$,** computed by Lelli et al. for thin disks with the measured HI maps (a diagnostic, not the letter's method).

Nothing is fitted. Output: [`measured_partition_output.txt`](measured_partition_output.txt); figure: [`measured_partition.png`](measured_partition.png).

**T1. Where the discs meet** (median $\mu_{\rm obs} = \tfrac12$; theory: the ring, $x = 1$):

| $g_{\rm bar}$ | All (149) | Not gas-dominated (90) |
|---|---|---|
| (a) letter's $M_{\rm phot}$, spherical | $x = 1.62$ (0.99–2.72) | $x = 1.33$ (0.92–2.66) |
| (b) SPARC, thin disk | $x = 1.03$ (0.83–1.43) | $x = 0.97$ (0.77–1.33) |

With SPARC's $g_{\rm bar}$ the measured discs meet within 3% of $x = 1$. The robustness checks ([`referee_checks.py`](referee_checks.py), [`referee_checks_output.txt`](referee_checks_output.txt)) are:
- **R1:** every galaxy weighted equally, instead of every point;
- **R2:** bins shifted by half a bin;
- **R3:** unsmoothed velocities.

| $g_{\rm bar}$ | point-weighted | galaxy-weighted (R1) | bins shifted (R2) |
|---|---|---|---|
| (a) letter's $M_{\rm phot}$ | 1.62 (1.05–2.50) | **1.83 (1.54–3.10)** | 1.50 |
| (b) SPARC | 1.03 (0.88–1.24) | 1.07 (0.92–1.21) | 1.02 |
| (b), unsmoothed $g_{\rm obs}$ (R3) | 1.07 (0.88–1.29) | 1.00 (0.88–1.13) | 1.00 |

With SPARC's $g_{\rm bar}$ the crossing stays at $x = 1.00$–1.07 under every variant. With the letter's photometric mass and every galaxy weighted equally, it is at $x = 1.83$, and the 95% interval **excludes** the ring. (The bootstrap intervals in this table use 1,000 draws, and those in the table above 2,000; they differ by Monte Carlo noise.)

**T2. The gap between the discs**, $|2\mu_{\rm obs} - 1|$, against the theory's $|2\mu - 1| = |\delta/\bar\omega|$, with (b):

| $\log_{10}x$ | −0.88 | −0.62 | −0.38 | −0.12 | +0.12 | +0.38 | +0.62 | +0.88 |
|---|---|---|---|---|---|---|---|---|
| measured | 0.55 | 0.55 | 0.42 | 0.16 | 0.14 | 0.22 | 0.56 | 0.66 |
| theory | 0.76 | 0.62 | 0.41 | 0.14 | 0.14 | 0.41 | 0.62 | 0.76 |

- **In the two bins either side of the ring** ($\log_{10}x = \pm0.12$) the measured gap equals the theory (0.16 and 0.14, against 0.14). At $-0.38$ it matches (0.42 against 0.41). At $+0.38$, just inside the ring, it is low (0.22 against 0.41). At $\pm0.62$ the two sides equal each other (0.55 and 0.56), below the theory's 0.62. Exchange symmetry, $\mu(1/x) = 1 - \mu(x)$, therefore holds at the ring and at $\pm0.62$, but not at $\pm0.38$.
- **Further out on both sides** the measured discs stay closer together than the theory: the measured shares saturate less.

With (a), the inner side flattens: the measured TetA share stays near 0.5–0.6 inside the ring. That is the spherical $GM/r^2$, which understates a thin disk's pull inside a few scale lengths, not a property of the shares.

**T3. The slip**, $\log_{10}(\Omega_{\rm obs}/x)$, with (b), all 149 galaxies: −0.016, −0.028 and −0.026 at $\log_{10}x = -0.38$, $-0.12$ and $+0.12$. That is, under 0.03 dex across $-0.5 < \log_{10}x < +0.25$. It then grows: −0.23 at $+0.38$, +0.08 and −0.16 at ∓0.62, +0.30 and −0.25 at ∓0.88. The chambers roll at the theorem's ratio across the ring, and slip away from it, more steeply on the inner side.

**What this shows.** With SPARC's $g_{\rm bar}$, Letter 3's ring is where the measured shares meet, robust to weighting, binning and smoothing. Across the ring the shares follow $\mu(x)$, and the roll ratio holds without measurable slip. Away from it they depart, and exchange symmetry holds only in part.

**What it does not show.**
- **Whether the outer departures are physical.** At the rim they sit in gas-rich dwarfs. At the centre they sit in bulges and inner disks, where the fixed stellar M/L matters most.
- **Anything unique to GFD.** Any law that fits the radial acceleration relation puts $\mu = \tfrac12$ near $g_{\rm obs} = a_0$. T1 is a consistency check of the ring, not a test that singles GFD out.

**Drive and brake depend on the photometric method.** Under the letter's method, the decode audit's H3 passes ($\rho = +0.47$). With SPARC's $g_{\rm bar}$ the same test gives $\rho = +0.16$ ($p = 0.02$) over all galaxies and $+0.14$ ($p = 0.10$) in galaxies that are not gas-dominated ([`decode_audit/diagnostic_d1.py`](decode_audit/diagnostic_d1.py)). The median net area of galaxies entirely outside the ring moves from −0.24 dex (brake) to −0.03 dex (quiet). Most of the drive–brake pattern in the audit comes from the spherical photometric approximation and the model gas disks, not from the galaxies.

## Next

1. **Justify no slip.** Derive the shared contact from the Field Origin as the point where both tetrads are evaluated, rather than assuming it.
2. **The outer departures.** Test whether the measured shares' weaker saturation, at the rim and at the centre, survives colour-based stellar M/L and asymmetric-drift corrections. If it does, it is a slip the theorem must account for.
3. **Drive and brake from the throat.** The pointwise slip does not give a robust galaxy-level drive or brake. A measure of the drain itself is needed, not of the disk's share.
