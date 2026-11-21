# The Constitutive Law as a Tug of War

*Why μ(x) = x/(x + 1), read as TetA pulling with g against TetB pulling with a₀, and what the decoded mass of a galaxy tells us about that contest · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`constitutive-law` `MOND` `exchange-symmetry` `screening` `decoding-mass` `Burgers-vortex` `proof` `Lean`

[![Lean proof](https://github.com/fielddynamics/research/actions/workflows/lean-constitutive-law-tug-of-war.yml/badge.svg)](https://github.com/fielddynamics/research/actions/workflows/lean-constitutive-law-tug-of-war.yml)

---

This folder holds a four-page proof, a script that checks every statement in it (42 checks), and a Lean formalisation that proves its algebraic and geometric core. The working notes it grew from, with 85 finer tests, are in [`research/constitutive-law-u(x)/`](../../research/constitutive-law-u(x)/). This page explains the proof the way a textbook on vortices would explain a drain: first the picture, then the equations, and then what the equations allow us to measure.

## A tug of war

Picture a rope with a flag tied at its middle. Two teams pull on it from opposite ends, and however hard they pull, the rope never gets longer; all that changes is how much of it each team holds. If one team pulls with strength $g$ and the other with strength $a_0$, the first team holds the fraction

$$\mu = \frac{g}{g + a_0} = \frac{x}{x + 1}, \qquad x = \frac{g}{a_0},$$

and that is the constitutive law of GFD. TetA, the chamber of the stellated octahedron that we observe as ordinary space and time, pulls with the local gravitational field $g$, while TetB, the chamber that lies beyond the Field Origin and is never seen directly, pulls with the fixed acceleration $a_0 \approx 1.2 \times 10^{-10}$ m/s². When $g$ is far larger than $a_0$, as it is everywhere in the solar system, TetA holds almost all of the rope and gravity is Newtonian. When $g$ falls to $a_0$, the flag sits exactly at the middle and the two chambers share the field equally. When $g$ falls well below $a_0$, at the edges of galaxies, TetB holds most of the rope, and its share is what astronomers have been calling dark matter.

The picture is simple, and the proof's job is to show that it is not merely a convenient story. Milgrom's modified gravity allows infinitely many interpolating functions with the right limits, so a referee is entitled to ask what, exactly, selects this one. The proof answers by taking the tug of war apart into premises and showing that each of them is needed.

## The two teams come from the cube

The stellated octahedron sits inside a cube, with TetA on four of the cube's corners and TetB on the other four. A field state on those eight corners that respects the tetrahedral symmetry of the figure cannot vary within a chamber, because the symmetry carries every corner of a chamber onto every other. Such a state therefore consists of exactly two numbers, one strength for each team, and its TetA share is the first strength divided by their sum (Lemma 1).

Two further facts come with the lemma, and both matter later. The position of the rope, the ratio of the cube's $xyz$ Walsh coefficient to its constant coefficient, turns out to be the Möbius map $s = (x - 1)/(x + 1)$ of the archive's coupling polynomial, so the docs' capacity $f = 17 + 4s$ is the same tug of war written on a dial. And the six Walsh modes out of which the cube's vortices are built sum to zero on each chamber, so no amount of rotation can move the rope. The vortex lives in a different part of the field from the share.

## Why the exchange shapes the law

The constitutive-law synthesis writes the law as a screening balance, in which the signal times the remaining capacity equals the used capacity: $x(1 - \mu) = \mu$. That balance is one member of a broader family, $x^n(1 - \mu)^m = \mu^p$, which also contains the bound-state law $x(1 - \mu)^2 = \mu$ and the cooperative binding laws of chemistry. Swapping the two chambers turns odds of $\Omega = \mu/(1 - \mu)$ into odds of $1/\Omega$, and if that swap is a symmetry, the law must obey $\mu(1/x) = 1 - \mu(x)$; at $x = 1$ this already forces an even split.

Theorem 1 shows how much the swap decides. A screening law respects it exactly when its two capacity powers are equal, $m = p$, and when they are equal the odds become a pure power of the field, $\Omega = x^k$. A single reflection has thus reduced an infinite family of possible laws to a ladder with one rung for each exponent $k$.

## What fixes the rung

Theorem 2 gives four conditions that each pick out the rung $k = 1$, and shows that they are equivalent. The first is the tug of war itself: with odds $x^k$ the two strengths are $g^k$ and $a_0^k$, and only when $k = 1$ are they accelerations that, weighted by their shares, add back up to the field. The second is astronomical: in the outskirts of a galaxy the rotation speed grows as $r^{(k-1)/(k+1)}$, which is flat only for $k = 1$, and then it obeys the Tully–Fisher relation $v^4 = GMa_0$. The third is algebraic: only $k = 1$ makes the odds a Möbius function, which is the premise the [exchange-symmetry proof](../constitutive-law-exchange-symmetry/) starts from. The fact that $a_0$ is an acceleration, on the same footing as $g$, and the fact that rotation curves are flat are therefore the same constraint seen from two sides.

## Every premise is necessary

Proposition 1 removes the premises one at a time and exhibits what appears in their place. Without the screening form, a law can respect the exchange and both of Milgrom's limits and still differ from $x/(x + 1)$ by a few per cent. Without equal capacity powers, the exchange fails, and the bound-state law gives a share of $1/\varphi^2 \approx 0.382$ at $x = 1$ instead of one half. That law is not wrong; it describes a field that sources itself and couples in both directions, and the proposition shows that such a field cannot be exchange-symmetric. The 11.8% gap between the two at $x = 1$, which the synthesis proposes as a test against galaxy rotation curves, is therefore a test of the exchange. Without $k = 1$, rotation curves keep rising. And the standard and exponential interpolating functions of the MOND literature both break the exchange.

## The Field Origin as the knot

If the two chambers meet only at the Field Origin, the centre of the cube is a single knot between the teams, and a single knot behaves in a characteristic way: it settles at the strength-weighted average of the two ends, and removing it leaves one rope whose strength is the series combination of the two pulls (Proposition 2). This is why the chambers' meeting at one point produces a clean share at all; direct links along the cube's edges would spoil it.

The same algebra explains the cap that Letters 2 and 3 describe. Each team carries its share of its own strength, so the field splits as $g = \mu g + \mu a_0$. TetB's part, $\mu a_0$, rises towards $a_0$ as the field grows but never reaches it, and the missing pull, divided by the visible pull, is simply $a_0/g$. The cap is not imposed; it is what a share of a fixed strength must do.

## Reading drive and brake

The [decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/) turns an observed rotation curve into a mass, $M_{\rm dec} = rv^4/[G(a_0r + v^2)]$, and compares it with the mass counted from starlight and gas. At each radius we can ask how hard TetB would have to pull for the measured share to be the quiet one, and the answer is a single number, TetB's measured strength $w$. Theorem 3 shows that the decoding comparison is exactly this strength set against $a_0$:

$$\frac{M_{\rm dec}}{M_{\rm phot}} = \frac{g + w}{g + a_0}.$$

When the two masses agree, TetB is pulling with exactly $a_0$ and the interior is quiet. When the decoded mass is larger, TetB is pulling harder than $a_0$ and holds more rope than the quiet law gives it, which is drive; when it is smaller, TetB is pulling more softly, which is brake. The denominator also tells us where we can see the difference: a given change in TetB's strength shifts the decode by tens of per cent in a galaxy's outskirts and by parts in ten million where the field is strong, which is why the solar system never shows drive or brake. In this reading $a_0$ acquires a second meaning, as TetB's quiet strength.

## What a vortex teaches

Fluid mechanics offers a precise picture of a quiet, a driven and a braking flow, and the proof uses it (Proposition 3).

Water draining from a bathtub rarely goes straight down. Any slight rotation it had is concentrated as it moves inward, because angular momentum is conserved, and the rotating column is stretched as it falls through the drain, which spins it faster still. The vortex is sustained by gravity's work on the water passing through the drain, and when the drain is closed the swirl slowly spreads and dies. Viscosity, meanwhile, works against the concentration, spreading the vorticity outwards.

Jan Burgers found the exact steady state of this contest in 1948. In the Burgers vortex an inward flow carries vorticity towards the axis, the axial outflow stretches it and strengthens it, and viscous diffusion spreads it back out, and the three effects balance exactly. The balance fixes the size of the core: its radius scales as $\sqrt{\nu/\alpha}$, where $\nu$ is the viscosity and $\alpha$ the strength of the drain, and at a fixed circulation its central vorticity grows in proportion to the drain. Far from the core, however, the swirl settles to $\Gamma/2\pi r$, which depends only on the total circulation and not on the drain at all. Without a drain, the same circulation obeys the Lamb–Oseen solution and simply diffuses away.

These three solutions map directly onto the three states of the decode. A drain in balance with diffusion is a steady vortex, the quiet interior with TetB pulling at $a_0$. A stronger drain tightens the core and spins it up, which is drive, and a weaker drain lets the vortex spread, which is brake carried, in the limit of no drain, to its end. The Burgers vortex even shares the decode's sense of where to look: the drain's strength is written in the core and in the inflow, not in the far swirl, just as drive and brake appear where TetB's share is large and vanish where $g$ is far above $a_0$. The vortex equations and the decode identity are exact; the identification of TetB with the drain is the framework's reading, as in the [vortex-hourglass note](../../research/vortex-hourglass/).

## What is proved, assumed and measured

The two-team share on the cube and the exchange as an operation on the cube are geometry, proved in Lean. Three premises are physical: that the law has the screening form, that the chamber swap acts on the field as $x \to 1/x$, and that the two strengths are accelerations; the last is confirmed independently by flat rotation curves. The value of $a_0$ is the one measurement the law needs.

Two statements of the March 2026 synthesis need rewording, although neither changes the law. Independent binding sites fill to $x/(1 + x)$ whatever their number, so the form $x^N/(1 + x^N)$ that the synthesis attributes to $N$ sites requires them to fill together, as in Hill's cooperative binding. And the inverse of the standard function $x/\sqrt{1 + x^2}$ is algebraic; what sets $x/(x + 1)$ apart is that its inverse is rational.

## Machine-checked in Lean

The [`lean/`](lean/) folder proves the note in [Lean 4](https://lean-lang.org) with the [Mathlib](https://github.com/leanprover-community/mathlib4) library, and the Lean kernel checks every step. It imports two earlier formalisations rather than restating them: the [Walsh eigenmodes of the cube](../walsh-eigenmodes-of-the-cube/), which supplies the two-team share, and the [constitutive law from exchange symmetry](../constitutive-law-exchange-symmetry/), whose law is the one the AQUAL and BIMOND chains are built on.

- **Lemma 1** is proved from the cube: symmetric states are two-team states, with the share, the rope position, the swap and the vortex modes as stated. On the cube, the tug of war of $g$ against $a_0$ is proved to give the archive's law.
- **Theorem 1** is proved for real exponents: the exchange holds exactly when the capacity powers match, and then the odds are $x^{n/p}$.
- **Theorem 2** is proved in its first three forms. The strengths are accelerations exactly when $k = 1$, and the deep-field speed is $r^{(k-1)/(k+1)}$ times a constant, so it is flat exactly when $k = 1$, with Tully–Fisher. The fourth form is the exchange-symmetry formalisation's `unique_law`.
- **Proposition 1** is proved for the bound-state law and for the standard and exponential functions, all of which break the exchange.
- **Proposition 2** is proved in full: the knot as a weighted average, the series link, the cap and the fixed point of the swap.
- **Theorem 3** is proved in full: the decode identity, and quiet, drive and brake as $w = a_0$, $w > a_0$ and $w < a_0$, together with the decoding letter's formula.
- **Proposition 3** is proved for the Burgers and Lamb–Oseen vortices, with every derivative computed in Lean.

The counterexample of Proposition 1 (a), whose limits need asymptotic analysis, the branch count of (e) and the Burgers core scaling are checked by the script rather than proved. GitHub re-checks the proof automatically whenever it, or any proof it builds on, changes, and the badge at the top of this page shows the latest result; it is green only if the proof builds with no warnings, no gaps (`sorry`) and only Lean's standard axioms. [`LEAN_AUDIT.md`](LEAN_AUDIT.md) is a referee's guide to the formalisation.

## Contents

| File | Contents |
|---|---|
| [`constitutive_law_tug_of_war.pdf`](constitutive_law_tug_of_war.pdf) | The proof (four pages, including references) |
| [`constitutive_law_tug_of_war.tex`](constitutive_law_tug_of_war.tex) | LaTeX source |
| [`verify_constitutive_law_tug_of_war.py`](verify_constitutive_law_tug_of_war.py) | 42 checks of every statement (numpy, scipy, sympy) |
| [`verify_output.txt`](verify_output.txt) | The script's output |
| [`lean/TugOfWar.lean`](lean/TugOfWar.lean) | The Lean 4 formalisation |
| [`lean/lakefile.toml`](lean/lakefile.toml), [`lean/lean-toolchain`](lean/lean-toolchain), [`lean/lake-manifest.json`](lean/lake-manifest.json) | Project files: Lean 4.36.0, Mathlib v4.36.0, and the six formalisations it imports |
| [`LEAN_AUDIT.md`](LEAN_AUDIT.md) | Referee's guide to the formalisation |
| `iopjournal.cls` | Journal class file |

## Reproduce

```bash
python verify_constitutive_law_tug_of_war.py

pdflatex -jobname=constitutive_law_tug_of_war '\providecommand\ead[1]{\email{#1}}\input{constitutive_law_tug_of_war.tex}'

# Lean (needs elan: https://github.com/leanprover/elan)
cd lean
lake exe cache get    # downloads Mathlib, already compiled
lake build            # checks every theorem, and the proofs it imports
```

## Related

- [The constitutive law from exchange symmetry](../constitutive-law-exchange-symmetry/): the same law from degree one, the endpoint and closure under exchange.
- [The Walsh eigenmodes of the cube](../walsh-eigenmodes-of-the-cube/): the two-team share, the vortex modes and the Field Origin's Schur reduction.
- [TetA and TetB as one vortex](../../research/vortex-hourglass/): the hourglass lemma, the roll ratio and the measured partition from SPARC.
- [The constitutive-law research folder](../../research/constitutive-law-u(x)/): the March 2026 syntheses, the roulettes and the tug-of-war tests.
