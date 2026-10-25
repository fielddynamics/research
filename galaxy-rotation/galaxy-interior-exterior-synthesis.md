# Galaxy Rotation Curves: Interior and Exterior Field Synthesis

## One Field Equation, One Topology, Zero Free Parameters

*Field Dynamics Research — March 2026*
*Stephen Nelson*

---

## The Central Result

The galaxy rotation curve problem reduces to one equation:

$$f(x) = \frac{21x + 13}{x + 1}$$

This is the coupling polynomial of the stellated octahedron, promoted from three discrete structural evaluations to a continuous function of the acceleration ratio x = g/a₀. At each radius of every galaxy, f(x) tells you the coupling capacity of the gravitational field — how much of the topology's range is active. The observed velocity, the predicted velocity, and the interior contribution all follow from f and its normalization μ = x/(x+1).

The same equation governs the interior of the atomic vortex. The galaxy and the atom are the same physics at different scales. What determines the interior contribution in a galaxy is the same structural mechanism that determines electron shielding in an atom.

---

## The Framework

### The Field Equation

The stellated octahedron — two interpenetrating tetrahedra sharing a common center (the Field Origin) — is characterized by the coupling polynomial:

$$f(k, s) = 1 + sk + k^2$$

evaluated at k = K = 4 (the face count per tetrahedron, fixed by the uniqueness equation 2(D+1) = 2^D at D = 3). The structural state s takes three discrete values:

| State | s | f(4,s) | Physical Regime |
|-------|---|--------|-----------------|
| TetA (Newtonian) | +1 | 21 | Baryonic gravity dominates |
| Field Origin (transition) | 0 | 17 | Bimetric equilibrium |
| TetB (deep field) | −1 | 13 | Interior field dominates |

The Möbius map s(x) = (x−1)/(x+1) makes the state continuous in the acceleration ratio x = g/a₀. Substituting into f(4, s(x)):

$$f(x) = 17 + \frac{4(x-1)}{x+1} = \frac{21x + 13}{x + 1}$$

Normalizing between the floor f = 13 and ceiling f = 21 gives the constitutive law:

$$\mu(x) = \frac{f(x) - 13}{8} = \frac{x}{x+1}$$

This is the fraction of the gravitational field attributable to baryonic matter (TetA). The complement 1/(x+1) is the fraction from the interior topology (TetB). Their sum is always 1.

### The Two Pipelines

**Forward pipeline.** From photometric baryonic mass M_bar(r), compute the Newtonian acceleration g_s = GM_bar/r², then solve the SST quadratic:

$$g_t = \frac{g_s + \sqrt{g_s^2 + 4g_s a_0}}{2}$$

The predicted velocity is v_gfd = √(g_t · r). This is the quiet topology prediction — what the constitutive law produces with zero free parameters.

**Inverse pipeline.** From observed velocity v_obs, compute the decoded effective mass:

$$M_{dec} = \frac{r \cdot v_{obs}^4}{G(a_0 r + v_{obs}^2)}$$

This is the mass the topology requires to produce the observed velocity. Comparing M_dec to M_bar reveals whether the interior is absorbing, amplifying, or quiet.

### The Interior Contribution

At each observed radius, the interior contribution is simply:

$$\Delta v(r) = v_{obs}(r) - v_{gfd}(r)$$

Negative: the interior absorbs — the galaxy shows less velocity than the quiet topology predicts. Positive: the interior amplifies — the galaxy shows more. Near zero: quiet — the constitutive law alone accounts for the observations.

This is the only number that matters for diagnosing the interior. It requires no model assumptions, no field decomposition ratios, and no fitting. Two velocities from the API, one subtraction.

---

## The Field Decomposition

### TetA and TetB on One Chart

At each radius, the observed acceleration gives x_obs = g_obs/a₀. The constitutive law predicts:

- TetA fraction: μ = x/(x+1)
- TetB fraction: 1 − μ = 1/(x+1)

The observed fractions are:

- TetA observed: μ_obs = g_bar/g_obs
- TetB observed: 1 − μ_obs

Plotting both theoretical curves and both sets of data points on one chart — x on a log axis, field fraction on y — produces the field decomposition diagram. The two curves cross at x = 1 (the Field Origin) where both equal 0.5. To the left, TetB dominates. To the right, TetA dominates. The data points track the curves when the topology is quiet and deviate when the interior is active.

### What the Full Catalog Shows

Across 175 SPARC galaxies (3,758 data points), the field decomposition reveals:

The data forms two mirrored clouds tracking the GFD curves, not the MOND curves. In the transition region (x ≈ 0.1–3), where GFD and MOND differ by up to 17%, the data envelope follows the slower GFD saturation μ = x/(x+1), not MOND's steeper x/√(1+x²).

The scatter is real and diagnostic. Galaxies whose data sits on the theoretical curves are quiet (NGC 4183, NGC 3198, D631-7). Galaxies whose TetB points are elevated above the curve are amplifying (NGC 7814, UGC 11914, NGC 5985). Galaxies whose TetA points are elevated above the curve are absorbing (CamB, IC 2574). The field decomposition classifies galaxies by their interior topology state at a glance.

### The Möbius Map

Pushing the data through the Möbius map s(x) = (x−1)/(x+1) linearizes the constitutive law. On the s-axis (linear, from −1 to +1), the TetA and TetB curves become straight lines crossing at s = 0. Five decades of acceleration compress into a unit interval.

On this axis, the coupling polynomial f(K,s) = 17 + 4s is visibly linear. The data bands track the theoretical lines, with the offset between data and theory constant across the s range — revealing that the interior's contribution is a uniform displacement in structural-state space, not a varying function of acceleration.

The catalog mean structural state is s = −0.234. The average galactic disk radius sits between the Field Origin and the TetB endpoint. Most of the matter in the observable universe lives in a regime where the interior topology contributes more than the baryons.

---

## The Interior Residual

### The Histogram

The simplest and most informative diagnostic is the per-radius residual histogram: v_obs − v_gfd plotted as a bar at each observed radius. Teal bars point down (absorption). Red bars point up (amplification). The yellow dashed line shows the mean.

This histogram requires one API call — the photometric rotation curve endpoint returns the residuals directly. No client-side physics, no decomposition, no normalization. One subtraction per radius.

### Galaxy Classification from the Histogram

**Absorbing galaxies** (CamB, IC 2574): all bars teal, mean negative. CamB shows −15.6 km/s mean across 9 radii, 9/9 absorbing. The quiet topology predicts 26 km/s but the galaxy shows 11 km/s. The interior suppresses the field at every radius.

**Amplifying galaxies** (UGC 11914, NGC 7814, NGC 5985): all bars red, mean positive. UGC 11914 shows +62.3 km/s mean across 65 radii, 65/65 amplifying. The quiet topology predicts 220 km/s but the galaxy shows 290 km/s. The interior adds field at every radius.

**Quiet galaxies** (NGC 4183, NGC 3198): bars scatter around zero, mean near zero. NGC 4183 shows −1.2 km/s mean, RMS 4.34 km/s. The quiet topology matches the observations directly. No interior correction needed.

**Sign-changing galaxies** (D631-7, NGC 2403): bars teal at inner radii, red at outer radii, crossing zero in the mid-disk. D631-7 shows −1.9 km/s mean but 8 absorbing / 8 amplifying. The interior absorbs in the inner disk and amplifies in the outer disk. The mean is near zero from cancellation, not from absence.

### The Radial Profile

The shape of the histogram across radius is the radial profile of the interior contribution. For absorbing galaxies, the profile often peaks (most negative) near the center and tapers outward — a pattern consistent with a vortex configuration concentrated at the interior. For amplifying galaxies, the profile is often flat or rises outward. For sign-changing galaxies, the profile crosses zero at a characteristic radius that may correlate with the transition between disk components (bulge, disk, gas).

---

## Connection to the Atomic Scale

### Same Equation, Different Coupling

The galaxy equation v⁴ = GM(v²/r + a₀) and the atomic vortex equation v⁴ = (kZe²/mₑ)(v²/r + a₀ᵥ) are structurally identical. Both are governed by the constitutive law μ = x/(x+1). Both produce a flat rotation curve at large r. Both have a Field Origin at x = 1 where the golden ratio emerges from g² − g − 1 = 0.

The field equation f(x) = (21x + 13)/(x + 1) governs both scales. The coupling polynomial's three structural states are the same: TetA (exterior/baryonic/Newtonian), Field Origin (transition), TetB (interior/bound/deep field).

### What Drives the Interior

In an atom, the interior is the nucleus — bound gravity fields packed on TetB. The vortex (electric field) spirals outward from TetB into TetA, illuminating tiles (electrons). Each inner tile absorbs flux from the vortex, shielding outer tiles. The shielding pattern — 0.35 per same-shell tile, 0.86 per inner-shell tile, 1.00 per deep tile — determines how much vortex flux reaches each shell.

In a galaxy, the interior is the gravitational Field Origin — the shared center of TetA and TetB where the coupling polynomial has its bottleneck at f = 17. The constitutive law μ = x/(x+1) is the Field Origin's saturation response: one processing site (k⁰ = 1) handling K² = 16 coupling channels. The interior contribution at each radius is the field equation's answer to how much of the baryonic signal passes through the topology and how much is absorbed or amplified.

The shielding in atoms and the interior contribution in galaxies are the same mechanism at different scales: the coupling polynomial evaluated at different structural states, with the Möbius map translating between the acceleration ratio and the topological state.

### The Packing Connection

Unbound gravity fields on TetA screen in one direction: x(1 − μ) = μ, giving μ = x/(x+1). This governs galactic dynamics. The exponent 1 in (1 − μ)¹ reflects one-directional screening in the unbound ocean.

Bound gravity fields on TetB compress bidirectionally: x(1 − μ)² = μ. This governs nuclear binding. The exponent 2 reflects the bidirectional compression of fields trapped on TetB.

The difference between the galaxy and the nucleus is not a parameter to be fitted. It is the physics of the state the field is in: unbound (one-directional, exponent 1) or bound (bidirectional, exponent 2). The field equation is the same. The topology is the same. The state determines the exponent.

---

## The Energy Functional

### From Polynomial to Energy

The AQUAL energy functional F(y) is the integral of the constitutive law:

$$F(y) = y - 2\sqrt{y} + 2\ln(1 + \sqrt{y})$$

where y = x² = (g/a₀)². Each term maps to a structural level of the coupling polynomial:

| Term | Polynomial Level | Physical Role |
|------|-----------------|---------------|
| y | K² = 16 (face coupling) | Newtonian energy, dominates at high acceleration |
| −2√y | sK = 4s (face propagation) | Transition energy, state-dependent flow between regimes |
| 2ln(1+√y) | k⁰ = 1 (Field Origin) | Saturation energy, irreducible base from field closure |

At each radius, the observed acceleration determines y, and the three terms decompose the gravitational energy budget into contributions from each structural level. In the deep field regime (low y), the Field Origin term dominates — the saturation floor sustains the rotation curve. In the Newtonian regime (high y), the face-coupling term dominates — standard gravity. In the transition (y ≈ 1), the flow term competes with both.

### The Covariant Action

The energy functional enters the covariant action as the scalar sector:

$$S = S_R + S_\phi + S_{em} + S_m$$

Four terms, each with a prefactor determined by the stellated octahedron. Three structural levels in the kinetic functional. Two field equations (Poisson and SST). One topology. Zero free parameters. The entire pipeline from the coupling polynomial to the galaxy rotation curve is algebraic.

---

## The Diagnostic Tools

### What Exists

Five interactive HTML tools consume the Field Dynamics API and present the physics:

**Galaxy Explorer** (galaxy-explorer.html): Four-panel dashboard — rotation curve with GFD/MOND/Newtonian predictions, decoded effective mass, per-point residuals, and the field decomposition (TetA μ(x) vs TetB 1/(x+1)) for any SPARC galaxy.

**Full Catalog Field Decomposition** (field-decomposition-all.html): Loads all 175 SPARC galaxies sequentially, plotting TetA and TetB data points against the theoretical curves. Produces the full-catalog RAR in field decomposition form — 3,758 points across 179 galaxies.

**Interior Residual Histogram** (interior-residual.html): Per-radius bar chart of v_obs − v_gfd from the photometric rotation curve endpoint. The simplest possible diagnostic: one subtraction, one bar, one color (teal = absorbed, red = amplified). Mean, RMS, peak absorption, peak boost.

**Field Residual Diagnostic** (field-residual-diagnostic.html): Δ(TetA) and Δ(TetB) scatter plots showing the deviation of observed field fractions from the GFD theoretical curves at each radius.

**Full Catalog Möbius Map** (mobius-map-all.html): All 175 galaxies plotted on the linearized s = (x−1)/(x+1) axis. The coupling polynomial becomes a straight line. Data bands, systematic offsets, and the catalog mean structural state are visible.

### What the Tools Show

The tools converge on a single conclusion: the constitutive law μ = x/(x+1) correctly predicts the field partition for quiet galaxies, and the deviation from the prediction — measured in km/s at each radius — is the interior topology's active contribution. This contribution is:

- Measurable at every observed radius without any model
- Classifiable by sign (absorbing/amplifying/quiet)
- Profiled radially without assuming a functional form
- Consistent with the letter's Burgers vortex analysis where that analysis was performed
- Connected to the same field equation that governs atomic structure

The interior of the galaxy is not dark matter. It is not modified inertia. It is the coupling polynomial of the stellated octahedron, evaluated at the acceleration ratio the galaxy presents, with the deviation from the quiet prediction revealing the active work of the Field Origin.

---

## Summary

One field equation: f(x) = (21x + 13)/(x + 1).

One constitutive law: μ = x/(x + 1).

One topology: the stellated octahedron at K = 4, D = 3.

The exterior is TetA — the baryonic fraction μ. The interior is TetB — the complement 1/(x+1). The partition is measured at every radius. The deviation from the quiet prediction is the interior's active contribution, stated in km/s. The field equation connects galactic dynamics to nuclear binding to atomic structure through the same polynomial evaluated in different states.

The rotation curve problem is solved in the same sense that the atomic radius problem is solved: the constitutive law gives the baseline, the field equation gives the coupling capacity, and the residual from the photometric prediction gives the interior's contribution — all from a single geometric object with zero free parameters.

---

*Validated across 175 SPARC galaxies (3,758 data points), 100 atomic/compound tests (100/100 passing), 20 nuclear packing tests (20/20 passing), 50 constitutive law tests (50/50 passing).*
