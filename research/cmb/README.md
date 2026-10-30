# The Oldest Light

*The cosmic microwave background and the depth of the early universe · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`cosmic-microwave-background` `cosmology` `recombination` `dark-matter` `hubble-parameter` `tully-fisher-relation` `modified-gravity`

---

Three hundred and eighty thousand years after the Big Bang, the universe became transparent. Before that moment it was a glowing plasma of light and charged matter, too dense for light to travel far. After it, hydrogen formed, the fog cleared, and the light of that instant set off across space. It is still arriving. Stretched by thirteen billion years of expansion into microwaves, it fills the sky as the cosmic microwave background (CMB), the oldest light there is.

That light carries a picture of sound. In the young plasma, gravity pulled matter into slight hollows, and the pressure of light pushed it back out. The result was a sea of acoustic oscillations: ripples in density, rising and falling, frozen into the sky at the instant the universe cleared. The Planck satellite measured their pattern with exquisite precision, and the pattern sets a number.

**The wells that drove those oscillations were about 6.4 times deeper than ordinary matter alone could have dug.**

Standard cosmology closes the gap with cold dark matter: a substance with about five times the mass of ordinary matter that does not interact with light and has never been detected directly. This folder asks whether the gap can instead be closed by the same law that GFD uses for galaxies, evaluated at the moment the universe became transparent.

## One law, an earlier epoch

In GFD, a gravitational field shares its response between two chambers, TetA and TetB, according to the constitutive law

$$\mu(x) = \frac{x}{x+1}, \qquad x = \frac{g}{a_0} .$$

Where the field is strong, TetA carries nearly all of it and gravity is Newtonian. Where it is weak, TetB carries most of it, and the field is stronger than ordinary matter alone would produce. The enhancement is

$$\mathcal{E} = \frac{1}{\mu(x)} = \frac{x+1}{x} .$$

At the edges of galaxies, this is the factor conventionally attributed to dark-matter halos. The question here is what it was at recombination.

Two inputs decide it. The first is the acceleration scale $a_0$. GFD identifies it with the temperature of the cosmological horizon: equating the Gibbons–Hawking temperature of the horizon with the Unruh temperature of an accelerated observer gives $a_0 = cH/2\pi$. The universe expanded much faster at recombination, so $a_0$ was much larger then. The second input is the field strength of the acoustic wells themselves, which was tiny: density ripples of about one part in a hundred thousand. The early universe therefore sat deep in the weak-field regime, where TetB carries most of the field.

## A first attempt that fails

Take $a_0$ to scale in proportion to the expansion rate, and the calculation is short. At recombination it gives $x \approx 0.037$ and an enhancement of about **28**. The observed value is about 6.4, so the prediction overshoots by more than a factor of four.

The constitutive law is not the problem. It is derived, and at $x = 0.037$ the weak-field approximation is accurate to 4%. The problem has to lie in how $a_0$ scales with the expansion rate. Something about the early universe must change the way the horizon's scale reaches each field.

## Packed bubbles

The difference is crowding.

A galaxy today is an isolated gravitational field. It closes on its own, like a single bubble floating free, and it reads the horizon scale directly. At recombination there were no isolated fields. Every region of space was gravitationally active, and every field's closure boundary pressed against its neighbours, like bubbles packed into foam.

Where two closed fields of radius $R$ overlap at separation $d$, the shared part of the boundary subtends an arc

$$\theta(d) = 2\arccos\!\left(\frac{d}{2R}\right).$$

In the early plasma, separations ranged over every value from touching to fully overlapping. With no reason to prefer any separation, take the uniform average, the one choice that adds no new parameter. The integral is exact:

$$\frac{\langle\theta\rangle}{2\pi} = \frac{1}{\pi}\int_0^1 \arccos(u)\,du = \frac{1}{\pi}.$$

On average, a fraction $1/\pi$ of each field's boundary is coupled to its neighbours, and $1 - 1/\pi$ is not.

Every boundary is a closure boundary, so the same partition applies at each one. The fraction that survives compounds from one boundary to the next, much as the TetB share compounds outward through a galaxy. Compounded across the expansion, it turns linear scaling into a power law:

$$a_0 \propto H^{\,1 - 1/\pi}.$$

## The result

| Step | Quantity | Value |
|---|---|---|
| 1 | Naive acceleration scale at recombination, $cH/2\pi$ | $2.55 \times 10^{-6}$ m/s² |
| 2 | Naive field ratio, $x$ | 0.037 (enhancement ≈ 28) |
| 3 | Coupled boundary fraction | $1/\pi = 0.318$ |
| 4 | Suppression, $(H_0/H_{\mathrm{rec}})^{1/\pi}$ | 0.041 |
| 5 | Corrected acceleration scale | $1.05 \times 10^{-7}$ m/s² |
| 6 | Corrected field ratio, $x_{\mathrm{rec}}$ | 0.183 |
| 7 | **Enhancement**, $(1 + x)/x$ | **6.46** |
| | Planck 2018, $\Omega_m/\Omega_b$ | $6.36 \pm 0.10$ |

The prediction lands 1.6% from the Planck value, at the upper edge of its quoted range. No parameter was adjusted to reach it. The constitutive law comes from the galaxy work, $a_0$ from the horizon, and $1/\pi$ from an integral. The expansion rate at recombination comes from standard cosmology and does not depend on dark matter.

## One equation, two epochs

The most striking consequence is an identity. In a galaxy, the Newtonian mass inferred from a rotation curve, $M_N = rv^2/G$, exceeds the mass GFD decodes, $M = rv^4/[G(a_0 r + v^2)]$, by the factor

$$\frac{M_N}{M} = 1 + \frac{1}{x} = \frac{1}{\mu(x)} .$$

That is exactly the expression for the CMB enhancement. The "dark matter" in the early universe and the "dark matter" in galaxies today are the same function, evaluated at different field strengths: once globally at recombination, and again locally at every radius of every galaxy.

Two further results follow from the same law:
- **The matter ratio.** The law also implies $\mu/(1-\mu) = x$. Reading $\mu$ and $1 - \mu$ as the baryon and dark-matter shares, this says $\Omega_b/\Omega_c$ should equal $x_{\mathrm{rec}}$. GFD gives 0.183; Planck's measured densities give 0.187.
- **The acoustic Tully–Fisher relation.** In the weak-field limit, the sound speed of the plasma and the mass of an acoustic well obey $c_s^4 = G M a_0$. That is the baryonic Tully–Fisher relation for galaxies, $v^4 = G M a_0$, with the sound speed in place of the orbital speed.

## Echoes in younger galaxies

If $a_0$ scales as $H^{1-1/\pi}$, galaxies in the past should have rotated faster for the same mass. Through $v^4 = G M a_0$, the prediction is

$$\frac{v(z)}{v(0)} = \left[\frac{H(z)}{H_0}\right]^{(1 - 1/\pi)/4} \approx \left[\frac{H(z)}{H_0}\right]^{0.17}.$$

This is about 21% faster at redshift 2, and 36% at redshift 4. The [Tully–Fisher evolution paper](../../papers/tully-fisher-velocity-evolution/) tests this exponent against nine integral-field measurements out to redshift 3, and all nine fall within the predicted band. The same exponent, derived from the CMB, governs galaxy kinematics ten billion years later.

## The microscopic clock

Two notes in this folder look beneath the scaling law and ask what does the compounding.

[*From Compton Oscillation to CMB Enhancement*](compton_to_cmb_synthesis.md) proposes that field closure is not static but cycles. Each field "breathes" through its coupling range, $13 \to 21$, at the electron's Compton frequency, and exposes the fraction $1/\pi$ of its boundary on every cycle. There are about $10^{38}$ such cycles in a Hubble time. Each is negligible on its own, but independent attenuations multiply, and their product converges exactly to the power law: $(1 - 2\eta/N)^N \to e^{-2\eta}$, with $\eta = 1/\pi$, per e-fold of expansion.

The logic parallels GFD's derivation of the gravitational constant, where 21 independent coupling levels each attenuate by the fine-structure constant to give $\alpha^{21}$.

[*The Velocity Exponent*](velocity_exponent_synthesis.md) follows the 0.17 further. It notes how closely $(\pi - 1)/4\pi = 0.1704$ sits to the Field Origin value 17, and proposes that CMB photons crossing the lattice meet the same $1/\pi$ filtering, a cosmological form of Buffon's needle.

## What is established, and what is not

- **Derived:** the enhancement of 6.46 from the constitutive law, the horizon scale and the boundary integral, with no parameter adjusted. The galactic and cosmological enhancements are the same algebraic identity.
- **Assumed:** the uniform average over boundary separations. It is the one choice that adds no parameter, and it is supported by the homogeneity of the early universe, but it is a choice.
- **A correspondence, not an equivalence:** the enhancement is matched to Planck's $\Omega_m/\Omega_b$ at the level of how deep the acoustic wells were. GFD has not yet been run through a full Boltzmann calculation of the CMB power spectrum, peak by peak. That is the decisive next test.
- **In progress:** deriving the compounding from the covariant action itself. The exponent script and the lattice propagator explore this as a renormalisation-group effect, in which $1/\pi$ appears as an anomalous dimension.

## Contents

| File | Contents |
|---|---|
| [`cmb_gravitational_enhancement_derivation_complete.md`](cmb_gravitational_enhancement_derivation_complete.md) | **Start here.** The formal derivation: horizon scale, the naive overshoot, the boundary integral, the corrected enhancement, and extensions to Tully–Fisher, $H_0$ and the galactic identity |
| [`test_cmb_enhancement.py`](test_cmb_enhancement.py) | Validation suite mirroring the derivation step by step (36 tests, pytest) |
| [`gfd_cmb_cosmological_synthesis.md`](gfd_cmb_cosmological_synthesis.md) | An earlier synthesis of the cosmological extension: horizon thermodynamics, tetrahedral packing and the scaling law |
| [`gfd_cmb_cosmological_suite.py`](gfd_cmb_cosmological_suite.py) | The companion 20-test suite |
| [`cmb_structural_extensions.md`](cmb_structural_extensions.md) | Further results: the closed-form enhancement, the acoustic Tully–Fisher relation, $\Omega_b/\Omega_c \leftrightarrow x$, and the mirror symmetry through the Field Origin |
| [`compton_to_cmb_synthesis.md`](compton_to_cmb_synthesis.md) | The microscopic picture: closure cycles at the Compton frequency compounding into $H^{1-1/\pi}$ |
| [`gfd_compton_to_hubble.py`](gfd_compton_to_hubble.py) | Simulates the cycle-by-cycle compounding and recovers the power law |
| [`compton_to_hubble.html`](compton_to_hubble.html) | Interactive chart: the microscopic oscillation and the macroscopic scaling side by side |
| [`velocity_exponent_synthesis.md`](velocity_exponent_synthesis.md) | The 0.17 exponent: two routes to it, the Field Origin, and the time-face lattice |
| [`gfd_exponent_derivation.py`](gfd_exponent_derivation.py) | The exponent as a one-loop renormalisation-group effect of boundary coupling |
| [`gfd_lattice_propagator.py`](gfd_lattice_propagator.py) | Four lattice models testing whether $1/\pi$ emerges as an anomalous dimension |

```bash
pip install numpy pytest
python -m pytest test_cmb_enhancement.py     # 36 passed
python gfd_cmb_cosmological_suite.py         # 20/20
python gfd_compton_to_hubble.py              # enhancement from the microscopic picture
```

## Related work

- **Paper II**, [*A Covariant Theory Without Dark Matter*](../../papers/02-covariant-theory-without-dark-matter/2026-01_28_Nelson_DFPII_A_Covariant_Theory_Without_Dark_Matter.pdf) ([doi:10.5281/zenodo.18360354](https://doi.org/10.5281/zenodo.18360354)): the published cosmological extension and the enhancement of 6.46.
- [*Tully–Fisher Velocity Evolution*](../../papers/tully-fisher-velocity-evolution/): the 0.17 exponent tested against integral-field surveys to redshift 3.
- [`field-closure/`](../field-closure/): why a gravitational field must close, the idea the packed-bubble argument builds on.

---

*The oldest light in the universe records how deep its first gravitational wells were. GFD's claim is that the depth was set by the same law that shapes galaxies today, read at a time when every field in the universe was pressed against its neighbours.*

---

**References**

- Gibbons, G. W. and Hawking, S. W. (1977). Cosmological event horizons, thermodynamics, and particle creation. *Phys. Rev. D* 15, 2738.
- Planck Collaboration (2020). Planck 2018 results. VI. Cosmological parameters. *Astron. Astrophys.* 641, A6.
- Unruh, W. G. (1976). Notes on black-hole evaporation. *Phys. Rev. D* 14, 870.
