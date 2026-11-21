# The Tug-of-War Theorem

*Field Dynamics Research · working note, 2026-11-21 · status: research; the finished proof, with its Lean formalisation, is [`proofs/constitutive-law-tug-of-war/`](../../proofs/constitutive-law-tug-of-war/). Checks: `python -m pytest -q test_tug_of_war.py` (85 tests).*

## The statement in one line

$$\mu(x) = \frac{x}{x+1} = \frac{g}{g + a_0}$$

μ is TetA's share of a tug of war. TetA pulls with the local pull g, TetB pulls with a₀, and each team's share is its own strength divided by the two strengths together.

## The theorem

Take a point of a galaxy's net field with total pull g, and let μ be the share of the field carried by TetA.

**Premises**

| | Premise | Status |
|---|---|---|
| P1 | **Two teams.** The field state on the stellated octahedron has the full T_d symmetry. | Geometry. Lean (`WalshEigenmodes`) proves that such a state has exactly two values, one per chamber. |
| P2 | **Exchange.** Swapping the chambers (spatial inversion −I) swaps strong and weak pulls: μ(1/x) = 1 − μ(x). | −I swapping the chambers is proved. Reading it as x → 1/x is the framework's step. |
| P3 | **Screening.** Signal and remaining capacity balance in mass-action form: xⁿ(1 − μ)ᵐ = μᵖ. | The constitutive-law folder's screening equation x(1 − μ) = μ, with general powers. It contains the folder's bimetric law (m = 2) and the Hill forms. |
| P4 | **Strengths are accelerations.** Each team pulls with an acceleration, so the two strengths add up in the units of the field. | The one physical input. Flat rotation curves select it independently. |

**Conclusions**

1. **From P1, μ is a share:** μ = w_A/(w_A + w_B). The rope position s = c_xyz/c₁ = (w_A − w_B)/(w_A + w_B) is the docs' Möbius parameter. The vortex (T₂) modes cannot move the rope. (Tests 1.1–1.5.)
2. **From P2 and P3, the screening powers match (m = p),** and the odds are a pure power: Ω = μ/(1 − μ) = xᵏ. (Tests 2.1, 2.2.)
3. **From P4, k = 1,** so μ = g/(g + a₀) = x/(x + 1) and TetB's strength is a₀. (Tests 3.3, 3.4.)
4. **Independent check on k:** the outer slope of a rotation curve is (k − 1)/(k + 1). Curves are flat, and v⁴ = GMa₀ holds, only when k = 1. (Tests 3.1, 3.2.)

**Every premise is necessary.** Each line below is an explicit, tested counterexample.

| Drop | What appears instead | Test |
|---|---|---|
| P3 (keep exchange and both MOND limits) | A smooth, increasing, exchange-symmetric law that differs from x/(x+1) by up to a few per cent | 4.1 |
| P2 (screening powers unequal) | The bimetric law x(1 − μ)² = μ, with μ(1) = 1/φ² ≈ 0.382, not ½. This is the folder's 11.8% SPARC test, and it is a test of the exchange. | 4.2 |
| P4 (k = 2) | μ = x²/(1 + x²): rotation curves keep rising (v² ∝ r^(1/3)) | 4.3 |
| Any of them | The standard, exponential and n-family functions fail the exchange | 4.4 |

**The repo's other route agrees.** A relation of degree one in x and μ, with μ(0) = 0 and the exchange, leaves two branches: x/(x+1) and x/(x−1). Requiring the share to stay between 0 and 1 removes the second, which has a pole at g = a₀. Powers other than 1 are never degree one, so both routes single out the same law. (Tests 4.5, 4.6.)

## Why the Field Origin matters

If the chambers meet only at the Field Origin, the centre is a single node between the two teams:
- **The Field Origin's state** is the strength-weighted average of the two teams.
- **Eliminating the centre** (a Schur complement, proved in Lean) leaves one rope: a rank-one coupling with TetA share t_A/(t_A + t_B). (Tests 5.1, 5.2.)
- **Direct cube-edge links between the chambers break this rule.** (Test 5.3.)

So "the chambers meet only at the Field Origin" is what makes the share a single, clean tug of war.

## The cap

Each team carries μ times its own strength: g = μg + μa₀.
- **TetA** carries μg, the Newtonian part.
- **TetB** carries μa₀ = (1 − μ)g. It rises towards a₀ and never passes it. It equals the series combination g·a₀/(g + a₀). (Tests 6.1–6.3.)
- **Missing ÷ visible = a₀/g.** (Test 6.4.)
- **a₀ is the one pull the exchange leaves fixed.** Swapping strong and weak pulls is g ↦ a₀²/g. (Test 6.5.)

## Corollary: drive, brake and quiet in the decoding-mass letter

At each radius the letter has the total pull g = v²/r and the visible pull g_bar = GM_phot/r². Two quantities follow:
- **The measured share** is μ_obs = g_bar/g.
- **TetB's measured strength** is the a₀ that would make that measured share the quiet one:

$$w = \frac{g\,(g - g_{\rm bar})}{g_{\rm bar}}$$

**The decode is TetB's measured strength compared with a₀:**

$$\frac{M_{\rm dec}}{M_{\rm phot}} = \frac{g + w}{g + a_0}, \qquad \frac{\Delta M}{M_{\rm phot}} = \frac{w - a_0}{g + a_0}$$

| State | Decode | TetB's team |
|---|---|---|
| **Quiet** | M_dec = M_phot | pulls with exactly a₀; the rope sits where μ(x) puts it |
| **Drive** | M_dec > M_phot | pulls harder than a₀ and holds more rope than μ(x) gives it |
| **Brake** | M_dec < M_phot | pulls softer than a₀ and holds less |

These three equivalences are exact and hold at every pull (tests 7.2–7.4). The same change in TetB's strength moves the decode by (w − a₀)/(g + a₀). That is large in a galaxy's outskirts and vanishes where g ≫ a₀, which is why drive and brake never show in the solar system (test 7.5).

So a₀ is TetB's quiet strength. Drive and brake are TetB pulling harder or softer than that at a given radius, and the decoded mass is how we read it.

## The vortex picture

Standard vortex physics says three things that match the framework's picture:
- **A drained vortex is sustained by its drain.** In a bathtub, the vortex is maintained by gravity's work on the water falling through the drain ([Lautrup, *Physics of Continuous Matter*, ch. 19](https://cns.gatech.edu/~predrag/courses/PHYS-4421-02/lautrup/7.5/whirls.pdf)). The spin-up comes from stretching the rotating water column as it drains ([University of Chicago sink-vortex demonstration](https://geosci.uchicago.edu/~nnn/LAB/DEMOS/sink.html)).
- **Steady means balanced.** The Burgers vortex is an exact Navier–Stokes solution. In it, inward flow concentrates the vorticity and axial stretching strengthens it, while viscous diffusion spreads it; the vortex is steady when the three balance ([Burgers vortex](https://en.wikipedia.org/wiki/Burgers_vortex)). Test 8.1 checks the solution exactly.
- **Remove the drain and the vortex spreads and decays.** This is the Lamb–Oseen solution, checked in test 8.2.

What the tests add (8.3, 8.4):
- A stronger drain tightens the core (radius ∝ √(ν/α)) and spins it up (peak swirl ∝ Γ√(α/ν)).
- Far from the core, the swirl tends to Γ/(2πr) whatever the drain's strength is.

Read across to GFD:

| Vortex | GFD |
|---|---|
| The visible swirl | TetA, the only side we see |
| The drain, below the surface | TetB, beyond the Field Origin |
| Drain balanced against diffusion (steady Burgers) | **quiet**: TetB pulls with a₀ |
| Drain strengthened: core tightens and spins up | **drive**: TetB pulls harder than a₀ |
| Drain weakened: the vortex spreads | **brake**: TetB pulls softer than a₀ |
| The far swirl forgets the drain's strength; the core does not | drive and brake show where TetB's share is large, in the deep field, and hide where g ≫ a₀ |

This table is an analogy. The vortex equations are exact, and so is the decode corollary. Identifying TetB with the drain is the framework's reading, as the vortex-hourglass README says.

## What is proved, what is assumed, what is measured

| | |
|---|---|
| **Proved (Lean)** | The two-team share on the cube; −I swaps the teams; vortex (T₂) modes cannot move the rope; the Schur reduction through the Field Origin; uniqueness from (E), (X), (A) |
| **Proved (here, exact algebra)** | Exchange ⟺ matching screening powers; matching powers ⟹ power-law odds; k = 1 ⟺ strengths are accelerations ⟺ flat curves; the decode identities for quiet, drive and brake |
| **Assumed** | Screening in mass-action form (P3); the chamber swap read as x → 1/x (P2); strengths are accelerations (P4) |
| **Measured** | The value of a₀ |

## Two corrections for `research/constitutive-law-u(x)/`

- **Langmuir sites.** The synthesis says n sites give xⁿ/(1 + xⁿ). Independent sites give x/(1 + x) for any number of them; xⁿ/(1 + xⁿ) needs the sites to fill together (Hill binding). So "one Field Origin" is not on its own what fixes k = 1; P4 is. (Test 9.1.)
- **"Not algebraic."** The standard function's inverse, μ/√(1 − μ²), is algebraic. What makes x/(x + 1) special is that its inverse is rational, a Möbius map. (Test 9.2.)
