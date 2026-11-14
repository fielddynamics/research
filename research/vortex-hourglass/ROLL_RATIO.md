# The Roll Ratio as the Rate Ratio of the Two Chambers

*Working note, Field Dynamics Research, 2026-11-14. Status: research, not a paper. Verification: `python verify_roll_ratio.py` (16 checks, exact sympy). Data comparison: `python compare_roll_ratio_sparc.py` (exploratory, no pass condition).*

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

All of (i)–(v) are exact ([`verify_roll_ratio.py`](verify_roll_ratio.py), 16 checks).

## What it shows

Given the no-slip premise, the roulette is a theorem, not an illustration. One premise turns four objects already in the repo into one:
- Letter 2's odds become the rate ratio;
- Letter 2's exchange becomes the vortex's parity;
- Letter 3's ring becomes the quiet throat;
- the chiral-holonomy twist becomes the rate difference.

## What it does not show

- **Why the contact does not slip.** That is the framework's reading of the Field Origin.
- **The size of anything.** The theorem gives rates, not masses or forces. It predicts *where* drive turns to drag (at $x = 1$), not by how much.

## Against SPARC (exploratory)

The [decode audit](decode_audit/) measured the gap $\Delta = \log_{10}(M_{\rm dec}/M_{\rm phot})$ at every radius of every SPARC galaxy, using the decoding-mass letter's pipeline. [`compare_roll_ratio_sparc.py`](compare_roll_ratio_sparc.py) compares the theorem's sign structure with it. No pass condition was fixed in advance, so this is exploratory.

**The sign structure matches.** In the 149 quality-cut galaxies, the median $\Delta$ is +0.094 dex inside the ring ($x > 1$, 1,046 points) and −0.035 dex outside it (2,106 points). Above its baryons inside, below them outside: drive inside, drag outside.

**The crossing is lower than the ring.**

| Sample | Median $\Delta$ crosses zero at | 95% bootstrap interval | Contains $x = 1$? |
|---|---|---|---|
| All quality-cut (149) | $x = 0.34$ | 0.26–0.54 | no |
| Not gas-dominated (90) | $x = 0.39$ | 0.28–1.32 | yes |

In all galaxies the turn from drive to drag happens at about a third of $a_0$, not at the ring. In star-dominated galaxies, where the photometric mass is most reliable, the interval reaches the ring. The gas-dominated low-acceleration points pull the crossing down, and that is where the photometric mass is least certain. So the mismatch could be a systematic or a real offset, and these data do not separate the two.

**The drive does not keep growing toward the core.** The median $\Delta$ peaks around $\log_{10}x \approx 0.4$–0.6 (+0.12 dex) and falls back to about +0.04 at $\log_{10}x \approx 1.4$. Rates alone, $\omega_B/\omega_A = x$, would keep growing. TetB's share, $1 - \mu$, vanishes toward the core, so a contribution that needs both a rate excess and a TetB share would rise and then fall. But no such combination is derived here, and choosing one to fit this curve would be fitting after the fact. It is recorded as an observation, for a test whose form is fixed first.

## Next

1. **Justify no slip.** Derive the shared contact from the Field Origin as the point where both tetrads are evaluated, rather than assuming it.
2. **From rates to mass.** Derive how a rate difference $\delta$ shows up in $M_{\rm dec} - M_{\rm phot}$. Then fix the predicted $\Delta(x)$, including its crossing and its peak, *before* comparing it with the audit.
3. **The crossing.** Rerun the comparison once the photometric-mass systematics are reduced (HI profiles, colour-based M/L, asymmetric drift), and see whether the crossing moves to the ring.
