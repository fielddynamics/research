# The Roll Ratio as the Rate Ratio of the Two Chambers

*Working note, Field Dynamics Research, 2026-11-14 (corrected after an independent review, [`independent_review.md`](independent_review.md)). Status: research, not a paper. Verification: `python verify_roll_ratio.py` (18 exact sympy checks). Data: `python measured_partition.py` and `python null_simulation.py` (Letter 3's discs from SPARC, exploratory).*

---

## What this note is

The author's [roulette](../constitutive-law-u(x)/tetA_tetB_roulette_roll_ratio.html) draws TetA as a fixed circle of radius μ and TetB as a circle of radius 1 − μ rolling on it, with roll ratio μ/(1 − μ). This note writes that picture down as algebra, with its premise stated explicitly, and works out what follows. The algebra is exact. It is a restatement of the roulette, not a new physical result, and its premise is not derived.

## Premise

The two chambers meet at the Field Origin, where both are evaluated together (Coles Notes §2–3). Reading that contact as shared, the chambers roll on each other without slipping, with radii equal to their shares: $R_A = \mu$ and $R_B = 1 - \mu$. Both the no-slip reading and the identification of radii with shares come from the roulette. Neither is derived here.

## Theorem

With $\mu = x/(x+1)$ and no slip, $R_A\,\omega_A = R_B\,\omega_B$:

**(i) The rate ratio is the odds.** $\omega_B/\omega_A = R_A/R_B = \mu/(1-\mu) = x$. Given the premise this is an identity: setting the radii equal to the shares makes the rate ratio the odds by definition.

**(ii) Exchanging the chambers.** Let $\bar\omega$ be the mean rate and $\delta$ the half-difference. Then $\delta/\bar\omega = (1 - x)/(1 + x) = 1 - 2\mu$. Swapping the two chambers, each taking the other's radius and rate, still rolls without slip, sends $x \to 1/x$, keeps $\bar\omega$ and flips $\delta$. That is Letter 2's exchange, $\Omega \to 1/\Omega$, written in rates.

The [hourglass lemma](LEMMA.md)'s parity has the same algebraic form: it also keeps a mean rate and flips a half-difference. But any swap of two labelled things does that, and the two half-differences live in different settings. The lemma's is across the throat, along the vortex axis; this one is between the chambers at a given galactic radius, as a function of $x$. **That they are the same operation is a reading, not shown here.**

**(iii) The chambers turn at one rate only at $x = 1$.** $\delta = 0$ exactly at $x = 1$, where $\mu = \tfrac12$. For $x > 1$, TetB turns faster than TetA; for $x < 1$, slower. This is the partition $\mu(x)$ itself, the quiet state, with no drive or brake anywhere. The point $x = 1$ is Letter 3's white ring, where the two shares are equal and the interaction core peaks, out in the disk. **It is not the throat**, which is the Field Origin at the drain. (An earlier version called the ring "the quiet throat"; that conflated the two.)

**(iv) The rate difference changes fastest at $x = 1$.** $d(\delta/\bar\omega)/d\ln x = -2\mu(1-\mu)$. This is the logistic law's core term, $x\,d\mu/dx = \mu(1-\mu)$, largest at $x = 1$, where $\mu(1-\mu) = \tfrac14$: Letter 3's interaction core.

**(v) The chiral-holonomy twist.** The share difference $\sigma = (x-1)/(x+1)$ in the [chiral-holonomy proof](../../proofs/chiral-holonomy-closed-frame/) is $\sigma = 2\mu - 1 = -\delta/\bar\omega$.

All of (i)–(v) are exact ([`verify_roll_ratio.py`](verify_roll_ratio.py)).

## Drive and brake, and what the decode sees

**Drive and brake happen in the interior TetB** (the framework's definition, Stephen Nelson, 2026-11-14). What we observe is their result:
- the decoded mass sits above the photometric mass when the interior drives ($M_{\rm dec} > M_{\rm phot}$);
- below it when the interior brakes ($M_{\rm dec} < M_{\rm phot}$);
- equal to it when the interior is quiet.

Reading that result across a galaxy's profile tells what the interior is doing.

Under the premise, the partition $\mu(x)$ is quiet: the decode, which already contains $\mu(x)$ ($g_{\rm s} = \mu\,g_{\rm t}$), returns $M_{\rm dec} = M_{\rm phot}$ everywhere, even though the chambers turn at different rates everywhere except $x = 1$. So the rate difference in (iii) is not a drive. In the theorem's terms, a drive or brake is the interior departing from the no-slip rate: slip. In the decoding-mass letter's terms, a **quiet interior** ($\Delta M_{\rm eff} = 0$) is no slip, and an **active interior** ($\Delta M_{\rm eff} \neq 0$, the drain's power output) is slip.

## What it shows, and what it does not

**Shows.** Under one stated premise, four objects already in the repo have a single algebraic description:
- Letter 2's odds;
- Letter 2's exchange of the chambers;
- Letter 3's equal-share point $x = 1$;
- the chiral-holonomy twist.

**Does not show:**
- why the contact does not slip, or why the radii are the shares;
- that Letter 2's exchange and the hourglass lemma's parity are the same operation;
- anything about sizes: the theorem gives rate ratios, not masses or forces.

## Letter 3's discs, measured (exploratory)

[`measured_partition.py`](measured_partition.py) builds Letter 3's two surfaces from SPARC for the 149 quality-cut galaxies: blue $\mu_{\rm obs} = g_{\rm bar}/g_{\rm obs}$ and red $1 - \mu_{\rm obs}$, as medians in bins of $\log_{10}x$. It uses two versions of $g_{\rm bar}$:
- **(a) the decoding-mass letter's photometric mass,** as $GM_{\rm phot}/r^2$, the letter's declared spherical limit;
- **(b) SPARC's own Newtonian $g_{\rm bar}$** (thin disks, measured HI maps), a diagnostic.

The measured quantity is the paper's own: $\log_{10}(M_{\rm dec}/M_{\rm phot}) = \log_{10}(\mu(x)/\mu_{\rm obs})$, verified at all 3,391 radii. Outputs: [`measured_partition_output.txt`](measured_partition_output.txt), [`measured_partition.png`](measured_partition.png), [`null_simulation_output.txt`](null_simulation_output.txt), [`referee_checks_output.txt`](referee_checks_output.txt).

**T1. Where the measured discs meet** (median $\mu_{\rm obs} = \tfrac12$), with 95% bootstrap intervals over galaxies:

| $g_{\rm bar}$ | point-weighted | galaxy-weighted | bins shifted |
|---|---|---|---|
| (a) letter's $M_{\rm phot}$ | 1.62 (1.00–2.75) | 1.83 (1.11–3.18) | 1.50 |
| (b) SPARC | 1.03 (0.83–1.41) | 1.07 (0.91–1.28) | 1.02 |
| (b), unsmoothed $g_{\rm obs}$ | 1.07 (0.83–1.44) | 1.00 (0.81–1.19) | 1.00 |

With SPARC's $g_{\rm bar}$, the discs meet at $x \approx 1$, as Letter 3 draws them. **This carries little evidential weight.** $a_0$ was calibrated on the same SPARC radial acceleration relation, so any law fitting it puts $\mu = \tfrac12$ near $g_{\rm obs} = a_0$ (McGaugh's function gives $x = 0.96$). It is a consistency check, not a test. With the letter's spherical photometric mass and galaxies weighted equally, the crossing moves to $x = 1.83$, and its interval excludes 1. That is the cost of the spherical limit on disk galaxies.

**T2 and T3. The gap between the discs and the "slip" are what measurement scatter produces.** The same error in $g_{\rm obs}$ enters both $x$ and $\mu_{\rm obs}$, which biases binned medians away from saturation on both sides. [`null_simulation.py`](null_simulation.py) shows this with galaxies that obey $\mu(x)$ **exactly**: SPARC's own $g_{\rm bar}$, each point's real velocity error and a per-galaxy scatter. Compare the null model (0.10 dex per-galaxy scatter, median of 20 realisations) with the measurement, (b):

| $\log_{10}x$ | −0.88 | −0.62 | −0.38 | −0.12 | +0.12 | +0.38 | +0.62 | +0.88 | +1.12 |
|---|---|---|---|---|---|---|---|---|---|
| slip, measured | +0.30 | +0.08 | −0.02 | −0.03 | −0.03 | −0.23 | −0.16 | −0.25 | −0.62 |
| slip, null | +0.17 | +0.04 | −0.05 | −0.02 | −0.05 | −0.13 | −0.22 | −0.42 | −0.62 |
| gap, measured | 0.55 | 0.55 | 0.42 | 0.16 | 0.14 | 0.22 | 0.56 | 0.66 | 0.67 |
| gap, null | 0.64 | 0.59 | 0.46 | 0.15 | 0.10 | 0.33 | 0.52 | 0.64 | 0.73 |

The null model reproduces the sign, the rough size and the flat stretch across $x = 1$, and its crossing is at $x = 1.07$. So the measured shares are **consistent with $\mu(x)$ within the measurement scatter**. The departures away from the ring are not evidence of slip. (Earlier versions of this note read them as slip and as "saturating less than $\mu(x)$", and said measurement errors do not move the medians; both were wrong.) Reading slip pointwise as interior activity would need the errors modelled forward first.

**Drive and brake against the ring.** The decode audit's test of whether drive and brake follow a galaxy's share inside the ring was the analyst's hypothesis, not a GFD claim. In GFD they happen in the interior TetB, at the drain, and the decode already contains $\mu(x)$, so a quiet galaxy shows no gap whatever its share inside the ring. See [`decode_audit/`](decode_audit/).

## Next

1. **Justify the premise.** Derive the shared contact at the Field Origin, and the radii as shares, rather than taking them from the roulette.
2. **Forward-model the errors** before reading any pointwise departure from $\mu(x)$ as interior activity.
3. **Drive and brake from the drain.** A galaxy-level measure of what the interior TetB is doing, read from $M_{\rm dec}$ against $M_{\rm phot}$.
