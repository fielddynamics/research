# Why Extrapolation Is Hard

## The Stream Problem

You stand at a point on a river and measure the water velocity. You walk upstream and measure again. And again. You now have velocity at r = 1, 2, 3, 4, 5 km from the mouth.

The question: what is the velocity at r = 0?

You know the physics. You know how water flows. You know the channel geometry from satellite photos (the photometric mass model). You know the constitutive law that relates gradient to flow. But you don't know what's around the bend — a boulder, a narrows, a dam, a tributary joining. Any of those would change the velocity at r = 0 dramatically, and none of them are visible from your measurement points downstream.

This is the galaxy extrapolation problem.

## What We Know

At every observed radius, the field equation gives us f(x) exactly. The coupling capacity of the stellated octahedron at that point is measured, not modelled. The interior contribution — the signed velocity delta v\_obs − v\_gfd — is a fact at each data point. The histogram bars are measurements.

The photometric mass model gives us the channel geometry: how much baryonic mass is enclosed at each radius, derived from luminosity profiles and gas maps. This is the prior — the satellite photo of the river channel.

The field equation f(x) = (21x + 13)/(x + 1) gives us the physics: how the coupling capacity varies with acceleration. The Möbius map s(x) = (x − 1)/(x + 1) linearises it. The AQUAL functional F(y) = y − 2√y + 2ln(1 + √y) gives us the energy. These are exact.

## What We Don't Know

Between observed radii, we interpolate. The field equation constrains the interpolation — f(x) is smooth, the topology enforces continuity — but we don't know the mass distribution between data points. A density clump at r = 3.7 kpc, sitting between observations at r = 3.1 and r = 4.3, would change f locally without being visible in either measurement.

Inside the first observation, we extrapolate. The photometric model provides the prior shape (Hernquist bulge, exponential disk). But the interior vortex configuration — the boulder around the bend — is unknown. The Burgers vortex gives a Gaussian guess with two parameters (α, r\_v), and the data overdetermines those parameters when you have enough points. But it's still a guess about the shape. The data doesn't constrain the interior uniquely.

Beyond the last observation, we extrapolate outward. The prior says the rotation curve flattens (the constitutive law guarantees v⁴ = GMa₀ in the deep field). But whether it truly flattens, rises slightly, or dips depends on the mass distribution beyond the last HI measurement. Tidal interactions, gas stripping, or a warp in the disk would change the outer curve.

## The Topology Helps But Doesn't Solve It

The stellated octahedron sits at r = 0 — the Field Origin. We know f(0) must approach the topology's boundary condition. In the deep interior where acceleration is high (x → ∞), f → 21 and the field is purely Newtonian. The coupling capacity at the center is determined by the enclosed mass, which the photometric model estimates.

But the transition from the observed inner radii to r = 0 passes through the region where the interior vortex is strongest. The vortex's radial profile — whether it's Gaussian, polynomial, or something else entirely — shapes the velocity curve in the unmeasured region. Two galaxies with identical observations at r > 0.5 kpc could have completely different velocity profiles at r < 0.5 kpc depending on their central mass concentration and vortex configuration.

## What the Tools Actually Do

The interior residual histogram shows what is measured — no extrapolation, no guessing. Each bar is v\_obs minus v\_gfd at an observed radius, straight from the API.

The Bayesian field propagation shows both. Inside the observation zone, the posterior passes through the data points exactly. Outside, it reverts toward the photometric prior with a widening uncertainty band. The band is the honest answer: we think the velocity is approximately here, but we could be wrong by this much.

The Burgers vortex extrapolation adds a physical model for the interior — a Gaussian absorption or amplification profile with two fitted parameters. It's the best two-parameter guess, overdetermined by the data. But it assumes the vortex is Gaussian. A more complex interior structure would require more observations, closer to the center.

## The Bottom Line

At observed radii: exact. Between observations: constrained interpolation, small uncertainty. Beyond observations: informed extrapolation, growing uncertainty. At r = 0: a guess, anchored by photometry and topology, but still a guess.

More observations at smaller radii reduce the guess. Denser sampling reduces the interpolation uncertainty. But the interior will always have a region that is extrapolated, because no telescope can measure the rotation velocity at r = 0.

The field equation tells you what f must be at every point. The observations tell you what f actually is where you can measure. The gap between them is the interior vortex. Measuring that gap precisely, at as many radii as possible, is the path from guess to knowledge.
