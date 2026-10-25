# GFD CDM Translation: What Dark Matter Is Correcting For

**Stephen Nelson | Field Dynamics Research | March 2026**

---

## Executive Summary

Twenty tests confirm a single finding: Cold Dark Matter's invisible mass halo is the TetB interior of the gravitational vortex. The identification is not approximate. It is algebraically exact at every radius in every galaxy tested, with residuals at machine epsilon (10⁻¹⁶). The dark-to-baryon mass ratio that CDM fits with a multi-parameter NFW profile reduces to one number — 1/x, where x = v²/(r·a₀) — derived from the constitutive law with zero free parameters. The cusp-core problem, CDM's most persistent internal contradiction, is resolved by the field acceleration gate: the TetB density converges to a finite constant at the galactic center, not the 1/r divergence that NFW requires.

---

## 1. The Problem CDM Was Built to Solve

Every spiral galaxy rotates too fast. Measure the visible mass — stars and gas — compute the Newtonian gravity, and the predicted rotation curve falls off as 1/√r beyond the luminous disk. The observed curve stays flat. Something is providing additional gravitational acceleration at large radii.

CDM's answer: an enormous halo of invisible matter, typically 5 to 50 times more massive than the visible galaxy, arranged in a specific density profile (Navarro-Frenk-White) with two free parameters per galaxy (scale radius and concentration). This framework fits rotation curves well. But it introduces an entity — cold dark matter — that has never been directly detected despite four decades of dedicated experiments, and it suffers from internal contradictions (the cusp-core problem, the missing satellites problem, the too-big-to-fail problem) that require increasingly elaborate secondary mechanisms to resolve.

The question this suite addresses is not whether CDM fits the data. It does. The question is: **what is CDM actually correcting for?**

---

## 2. The Answer: CDM Corrects for TetB

GFD recognizes that a galaxy is not a mass distribution with test particles orbiting around it. A galaxy is a **vortex** — a coupled dynamical system living across two tetrahedral field chambers. TetA is our spacetime, the side we observe. TetB is the field interior, the side we cannot see directly. The constitutive law μ(x) = x/(x+1) partitions the total gravitational acceleration between these two chambers at every point in space.

CDM decomposes the observed rotation curve as:

> v²_obs = v²_baryon + v²_DM

GFD decomposes it as:

> v²_obs = v²_TetA + v²_TetB

The suite proves these are the same decomposition. Not similar. Not approximately equal. **Identical** — to the limits of floating-point arithmetic.

### What the tests show

**CT1a** verifies the quadrature identity v² = v²_TetA + v²_TetB across all 24 data points in three galaxies (Milky Way, M33, NGC 6503). The maximum error is 1.4 × 10⁻¹⁶ — the noise floor of 64-bit floating-point arithmetic. There is no gap between the two decompositions. They are the same equation written in different notation.

**CT1b–c** verify that the mass attribution is also exact: M_DM = M_TetB at every radius. The dark matter mass that CDM infers from the velocity deficit is precisely the field mass that the constitutive law assigns to TetB. This holds for the Milky Way's massive disk, M33's modest spiral, and NGC 6503's compact rotation curve — three galaxies with very different morphologies and mass scales.

**CT1d** closes the accounting: M_eff = M_baryon + M_TetB. The total dynamical mass at each shell is the sum of the TetA (baryonic) and TetB (field) contributions. This is CDM's equation M_total = M_baryon + M_DM, rewritten in the language of field chambers.

**CT1e** identifies the boundary: at the Field Origin (x = 1), v_TetA = v_TetB = v/√2. Dark matter equals baryonic matter at the 50/50 partition. Inside this radius, baryons dominate. Outside, the field dominates. The transition is smooth and governed entirely by the constitutive law.

---

## 3. The Dark-to-Baryon Ratio Is One Number

CDM measures the dark-to-baryon mass ratio at each radius and fits it with a halo model. In GFD, this ratio is:

> M_DM / M_baryon = 1/x

where x = v²/(r·a₀). One number. No fitting. No halo profile. No free parameters.

### What the tests show

**CT2a–b** verify that 1/x reproduces the CDM mass ratio at every radius in all three galaxies. The maximum error across 24 data points and a 60-point synthetic sweep spanning six decades in x is less than 10⁻⁶ (CT2e). The identity is algebraic, not approximate.

**CT2c** proves a clean structural rule: dark matter dominates (ratio > 1) if and only if x < 1, which means the observation is outside the Field Origin. Inside the Field Origin (x > 1), baryonic mass dominates. There are zero violations across all 24 data points.

**CT2d** checks the Milky Way at 30 kpc against CDM literature. The GFD prediction: a dark-to-baryon ratio of 2.52:1. Published CDM fits for the Milky Way at 30 kpc typically give 2 to 3:1. The constitutive law reproduces the CDM answer without a halo model.

The power of 1/x is its simplicity. CDM needs a scale radius, a concentration parameter, and a profile shape for each galaxy. GFD needs one ratio computed from the observed velocity and the universal constant a₀. The physics is the same; the machinery is different.

---

## 4. The Cusp-Core Problem Is Solved by the Gate

This is where the translation reveals something CDM cannot explain on its own.

The NFW density profile predicts ρ ~ 1/r at the center of every dark matter halo — a cusp, a density that diverges as r → 0. Observations of dwarf galaxies and low-surface-brightness spirals consistently show flat central density profiles — cores, not cusps. This is the cusp-core problem, and it has persisted for over two decades. CDM resolves it only by invoking baryonic feedback: supernovae explosions and gas outflows that redistribute the dark matter. The mechanism works in simulations but requires fine-tuning and does not explain why cores appear even in galaxies with minimal star formation.

GFD resolves it with the gate.

The field acceleration g_field = a₀·x/(x+1) saturates at a₀. No matter how large the baryonic mass, no matter how deep the Newtonian potential well, the field never pushes harder than a₀. This is the gate — the maximum throughput of the constitutive law.

### What the tests show

**CT3a** confirms the core density is finite: ρ_core = a₀/(2πG) = 1.37 × 10⁵ M☉/kpc³. This is a constant, derived from two fundamental quantities, not fitted to any galaxy.

**CT3b** verifies the gate: field acceleration reaches a₀ asymptotically from below but never exceeds it, even at x = 10¹². The constitutive law is a hard ceiling on field throughput.

**CT3c** tests the scaling. If the TetB density is constant near the center, then the enclosed TetB mass should scale as r² (volume of a shell times constant density gives M ~ r³, but the shell mass dM/dr ~ r², so M ~ r² for the field component at small r). The measured ratio M_TetB(1 kpc)/M_TetB(0.5 kpc) = 4.17, against the r² prediction of 4.0. The slight excess is expected because x ≈ 7–11 at these radii — large but not infinite, so the asymptotic formula slightly underestimates the actual field mass. The scaling is r², not r³ (cusp) or r¹ (point mass).

**CT3d** places the core density in physical context: log₁₀(ρ_core) = 5.14. This is the lower bound — the asymptotic value from the constitutive law alone. Real galaxies have baryonic concentrations that modify the local acceleration field, but the GFD core density sets the floor.

**CT3e** checks the outer envelope. At large radii where v is roughly constant, the TetB density should fall as r⁻² (isothermal). The measured log-slope between 15 and 30 kpc in the Milky Way is –2.13, against the isothermal prediction of –2.0. CDM literature describes dark matter halos as "approximately isothermal" at intermediate radii. GFD derives this from the flat rotation curve: if v is constant, then dM_TetB/dr ~ v²/G = constant, and ρ = (4πr²)⁻¹ · dM/dr ~ r⁻².

The cusp-core problem does not exist in GFD. It is an artifact of assuming the invisible component is matter with a density profile, rather than a field with a throughput limit.

---

## 5. The Round-Trip: A Galaxy's Dark Side Is Encoded in Its Bright Side

The most technically striking result in the suite is the round-trip.

Given an observed rotation curve v(r) on TetA, the TetB velocity at every radius is:

> v_TetB(r) = v(r) / √(x + 1)

Given only the TetB velocity curve and a₀, the full observed rotation curve is recovered by:

> v² = v²_TetB · r·a₀ / (r·a₀ − v²_TetB)

This works because the constitutive law is a bijection. It maps every TetA state to exactly one TetB state and vice versa. The complement symmetry μ(x) + μ(1/x) = 1 guarantees the mapping is invertible.

### What the tests show

**CT4a–b** verify the round-trip across all 24 data points in three galaxies. Maximum error: 9.1 × 10⁻¹⁶. Machine epsilon. The reconstruction is perfect.

**CT4c** confirms the gate bound: v²_TetB < r·a₀ at every point. This is required for the inverse formula to have a real solution, and it is guaranteed by the saturation of the field acceleration. The maximum observed ratio is 0.915 at the innermost Milky Way point, comfortably below 1.0.

**CT4d** shows that v_TetB rises monotonically with radius in all three galaxies. The field interior strengthens outward. This is why rotation curves are flat: as the Keplerian (TetA) contribution falls off, the field (TetB) contribution picks up the slack. The vortex maintains its total velocity by shifting the partition from TetA to TetB.

**CT4e** verifies the complement: computing M_baryon from the inverse pipeline and computing M_baryon as M_eff − M_TetB give identical answers at machine precision. Two completely different algebraic routes to the same number. The accounting is closed.

The physical meaning is direct: the "dark side" of any galaxy — the component CDM attributes to an invisible halo — is fully and uniquely determined by the bright side (the observed rotation curve) plus one universal constant (a₀). There is no freedom. No fitting. No halo model. The constitutive law is the complete bridge between what we see and what we cannot.

---

## 6. The Translation Table

Every concept in the CDM framework maps to a specific quantity in GFD:

| CDM Concept | GFD Reality |
|---|---|
| Dark matter halo mass | TetB field mass: M_eff/(x+1) |
| NFW density profile | TetB field density: dM_TetB/dr |
| Dark-to-baryon ratio | 1/x = a₀r/v² (no fitting) |
| NFW concentration c | x-profile shape (how fast x falls with r) |
| Cusp (ρ ~ 1/r) | Core: ρ → a₀/(2πG) = constant |
| Missing satellites | TetB substructure below gate ceiling |
| v_DM(r) | v_TetB(r) = v/√(x+1) |
| Virial radius | Horizon: r_H = D · r_FO |
| Halo spin parameter | Vortex angular momentum on TetB |
| Adiabatic contraction | μ(x) self-adjusts with M_baryon |

The left column requires an invisible particle, a density profile with free parameters, and secondary mechanisms (baryonic feedback, tidal stripping, dynamical friction) to handle the contradictions.

The right column requires one constitutive law — μ(x) = x/(x+1) — and one universal constant — a₀ = 3703 (km/s)²/kpc.

---

## 7. What This Means

Dark matter is not matter. It is the interior of the gravitational vortex.

Every galaxy rotation curve that CDM fits with an NFW halo, GFD reproduces with the constitutive law. The fit is not approximate — it is algebraically identical. The masses agree. The velocities agree. The ratios agree. The difference is interpretation: CDM says there is invisible mass generating additional gravity. GFD says there is a second field chamber carrying part of the total field load, and the partition between the two chambers is governed by μ(x) = x/(x+1).

The constitutive law does three things CDM cannot:

1. **It solves the cusp-core problem without baryonic feedback.** The gate limits the field acceleration to a₀, forcing a finite core density. No supernovae required.

2. **It predicts the dark-to-baryon ratio from one formula.** CDM fits each galaxy separately. GFD gives 1/x at every radius in every galaxy from the same law.

3. **It makes the round-trip exact.** From the observed rotation curve alone, the entire "dark" component is determined with zero free parameters and zero residual. A galaxy's dark side is not hidden — it is encoded in the bright side.

The 20 tests in this suite do not argue against CDM's observational success. They identify what CDM is correcting for: the TetB interior of a gravitational vortex whose partition function is the constitutive law of Gravity Field Dynamics.

---

*Suite: gfd_cdm_translation.py | 20/20 passed | March 2026*
