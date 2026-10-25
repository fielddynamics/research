# GFD Three-Level Architecture: u(x), Field Equation, and the SST

**Nelson (2026) — Technical Reference Note**

---

## 1. The Constitutive Law: u(x) = x/(x+1)

### What it is

The constitutive law u(x) is a pointwise algebraic relation between the Newtonian source acceleration g_s and the total observed acceleration g_t at any point in a gravitational field. It answers a simple question: given how much baryonic mass is enclosed at radius r, what total acceleration does an orbiting body actually experience?

The field state parameter x = g_t / a₀ measures the total acceleration in units of the fundamental scale a₀ = 1.2 × 10⁻¹⁰ m/s². Then:

    u(x) = x / (x + 1)

This function maps between 0 and 1. It tells you the fraction of the total gravitational field that is attributable to the baryonic source — the "Newtonian fraction."

### The two limits

When x >> 1 (strong field, inner galaxy, Solar System), u → 1. The field is purely Newtonian. g_t ≈ g_s. Newton's law works as written. There is no field-dominated contribution.

When x << 1 (weak field, outer galaxy, deep field regime), u → 0. Almost none of the total acceleration comes from the Newtonian source directly. The field is dominated by the TetB sector — the topological enhancement. This is where rotation curves go flat: v⁴ = G·M·a₀.

At x = 1 (the field origin), u = 1/2. Exactly half the gravity is Newtonian, half is field-dominated. This is the transition radius.

### What it does in galactic rotation

Given a baryonic mass profile M_bar(r), the constitutive law converts the Newtonian source acceleration into the total acceleration that determines orbital velocity:

    g_s = G·M_bar(r) / r²                        (Poisson)
    g_t = [g_s + √(g_s² + 4·g_s·a₀)] / 2        (u(x) inverted)
    v = √(g_t · r)                                (circular orbit)

This is the "green dashed curve" in the viewer. It takes the photometric mass and pushes it through the constitutive law to predict the rotation curve. It uses zero free parameters beyond G and a₀.

The constitutive law also runs in reverse. Given an observed velocity, you can decode the effective enclosed mass:

    g_t = v² / r                                  (circular orbit)
    g_s = g_t² / (a₀ + g_t)                       (u(x) applied)
    M_dec = g_s · r² / G                           (inverse Poisson)

Combined: M_dec = r·v⁴ / [G·(a₀·r + v²)]. This is exact. The round trip M_dec → u(x) forward → v recovers the original velocity to machine precision.

### What it is NOT

The constitutive law is not a gravitational theory. It is a single algebraic function that relates accelerations at a point. It says nothing about:

- How the field propagates through space (no gradient, no divergence)
- How neighboring radii couple to each other (no differential equation)
- What the topology of the field is (no stellated octahedron structure)
- How the field couples to electromagnetism or matter (no action principle)

It is the thermometer, not the weather system. It reads the local field state but doesn't generate it.

### The corrective lens property

When applied as a correction to the photometric prediction, u(x) acts as a universal lens:

    v_corrected = v_phot × √(u_obs / u_bar)

where u_obs = u(v_obs²/(r·a₀)) and u_bar = u(v_phot²/(r·a₀)). This correction absorbs mass model errors through the constitutive law's nonlinearity. Verified across IC2574, M33, and the Milky Way, it reduces photometric RMS by 60–91%.

The correction is exact in the deep field limit (x << 1) and inert in the Newtonian limit (x >> 1). The residual after correction is √[(x_obs+1)/(x_bar+1)], which approaches 1 in the deep field.

---

## 2. The Field Equation: f(x) = (21x + 13) / (x + 1)

### What it is

The field equation is the coupling polynomial of the stellated octahedron. While u(x) describes the Newtonian fraction of the field, f(x) describes the *complete* field coupling — both TetA (our spacetime, 21 channels) and TetB (the field subspace, 13 channels).

    f(x) = (21x + 13) / (x + 1)

The numbers are not arbitrary. They come from the geometry of a tetrahedron in 3 spatial dimensions:

- 21 = f(K) = 1 + 4 + 16, the coupling polynomial evaluated at K=4 vertices. This counts TetA's field degrees of freedom.
- 13 encodes TetB, the dual tetrahedron's contribution.
- The relationship: f(x) = 21·u(x) + 13·(1 - u(x)) = 8·u(x) + 13.

### How it differs from u(x)

The constitutive law u(x) maps between g_s and g_t as if only the TetA fraction matters:

    g_s = u(x) · g_t

The field equation includes TetB's active participation in the coupling:

    g_s = f(x) · g_t / 21

The ratio between them is:

    f(x) / (21 · u(x)) = (21x + 13) / (21x) = 1 + 13/(21x)

This ratio equals 1 in the Newtonian limit (x → ∞) — the two agree when TetB is dormant. But in the deep field (x → 0), the ratio diverges: 13/(21x) >> 1. The field equation requires dramatically more source acceleration for the same total acceleration, because TetB is actively absorbing field energy.

### What it does in galactic rotation

The field equation operates as a different decode/forward pair:

    FORWARD: g_s → g_t via 21u² + (13 - 21β)u - 21β = 0, where β = g_s/a₀
    INVERSE: g_t → g_s = f(x)·g_t/21

When applied to the same photometric mass M_bar:

- The u(x) photometric baseline for IC2574 gives RMS = 7.7 km/s
- The f(x) photometric baseline gives RMS = 27.5 km/s

The field equation baseline sits well below the u(x) baseline because f(x)/21 > u(x): more of the source field is consumed by the coupling. You need more baryonic mass to produce the same orbital velocity.

The λ correction factors reflect this:

| Galaxy | λ_u range | λ_fe range |
|--------|-----------|------------|
| IC2574 | 0.03 → 1.0 | 0.5 → 6.3 |
| M33 | 0.03 → 2.1 | 0.2 → 6.8 |
| MW | 0.63 → 1.2 | 1.5 → 3.3 |

The field equation demands 3–6× more effective mass in the outer galaxy to explain the observed velocities. This is TetB's contribution — the 13 field channels that u(x) doesn't account for.

### The red curves in the viewer

The viewer shows four curves when a mass model is available:

- **Green dashed**: M_bar → u(x) → v. The constitutive law photometric baseline.
- **Gold solid**: λ_u · M_bar → u(x) → v. The Bayesian pipeline using u(x).
- **Red dashed**: M_bar → f(x) → v. The field equation photometric baseline.
- **Red solid**: λ_fe · M_bar → f(x) → v. The Bayesian pipeline using f(x).

Both pipeline curves (gold and red solid) recover the observed velocities exactly at observation points. This is guaranteed by construction — the decode and forward operations are inverses of each other within each pipeline.

### The smoothing question

Both pipeline curves track the observation points exactly, including their scatter. Switching from u(x) to f(x) does not smooth the curve because:

1. Both pipelines use the same mathematical structure: decode → λ correction → spline → forward.
2. The spline interpolates through the same observation points regardless of which decode/forward pair is used.
3. The round trip (decode then forward) is an identity operation for both u(x) and f(x), by construction.

The field equation f(x) changes the *amplitude* of the correction (λ_fe >> λ_u) and the *baseline* (red dashed << green dashed), but not the *smoothness* of the result. Smoothing would require the field equation to act as a differential operator coupling neighboring radii — which brings us to the SST.

---

## 3. The SST: Scalar-Tensor Stellated Octahedron

### What it is

The SST is the full covariant gravitational theory. It is an action principle:

    S_ST = ∫ d⁴x √(−g) [ R/(16πG) − a₀²/(8πG) F(|∇Φ|²/a₀²)
           − ¼ e^(−2Φ/c²) F_μν F^μν + L_matter ]

This is a scalar-tensor theory in which:

- **R/(16πG)**: The Einstein-Hilbert term. Standard general relativity.
- **F(|∇Φ|²/a₀²)**: The free function of the scalar field gradient. This is where the stellated octahedron topology lives. The specific form of F determines whether you recover u(x), f(x), or something else in the spherically symmetric limit.
- **e^(−2Φ/c²) F_μν F^μν**: The conformal coupling between the scalar field and electromagnetism. This is the bridge between gravity and the electromagnetic sector — the scalar field Φ modulates the effective fine structure constant.
- **L_matter**: The matter Lagrangian, minimally coupled.

### How it differs from u(x) and f(x)

The SST is a four-dimensional field theory. It lives on a curved spacetime manifold. It has:

- **Covariance**: The equations transform correctly under general coordinate changes. This is non-negotiable for a gravitational theory that claims to work beyond spherical symmetry.
- **A scalar field Φ(x)**: Not just an algebraic relation, but a dynamical field that propagates, has its own equation of motion, and mediates the transition between Newtonian and field-dominated regimes.
- **Differential equations**: The variation of the action gives field equations involving ∇²Φ, ∇Φ, and the spacetime curvature. These are partial differential equations that couple the field at neighboring points.
- **Electromagnetic coupling**: The e^(−2Φ/c²) factor means the scalar field affects how light propagates, how clocks tick, and how electromagnetic forces operate. This is testable.

In spherical symmetry, the SST field equations *reduce* to an algebraic relation between g_s and g_t. Which algebraic relation depends on the form of F:

- If F is chosen to reproduce u(x): you get the constitutive law.
- If F encodes the stellated octahedron: you get f(x) = (21x+13)/(x+1).

But in non-spherical geometries (disk galaxies, galaxy clusters, binary systems, gravitational lensing), the SST's differential structure produces effects that no algebraic relation can capture. The gradient ∇Φ couples neighboring spatial points, creating smoothing, lensing deflections, and propagation effects that are invisible in the spherically symmetric limit.

### Why the SST would smooth

The pipeline curves track observation scatter because they use pointwise algebraic operations:

1. At each observed (r, v), decode a mass.
2. Spline-interpolate between those masses.
3. At each grid point, evaluate the algebraic forward map.

No step involves spatial coupling. The spline provides mathematical smoothness (continuous derivatives) but not physical smoothness (solutions of a field equation).

The SST, by contrast, would solve:

    ∇·[F'(|∇Φ|²/a₀²) ∇Φ] = 4πG ρ_eff

This is an elliptic PDE. Its solutions are inherently smooth — an elliptic operator cannot produce the wiggles that a spline can. The SST would take the corrected mass distribution λ(r)·M_bar(r) and solve for Φ(r) as a boundary value problem. The resulting v(r) = √(r · dΦ/dr) would be as smooth as the density profile permits, with high-frequency observation noise filtered out by the differential operator.

This is the fundamental difference: u(x) and f(x) are local thermometers that read the field state at each point independently. The SST is the weather system — it enforces global consistency through the field equations, smoothing local fluctuations into a self-consistent solution.

### What it would take to compute

Running the Bayesian pipeline through the full SST would require:

1. Convert λ(r)·M_bar(r) to a density profile ρ(r) via differentiation.
2. Solve the modified Poisson equation ∇·[F'·∇Φ] = source, with appropriate boundary conditions (Φ → 0 at infinity, regularity at r = 0).
3. Extract v(r) = √(r · dΦ/dr) from the solution.

This is a nonlinear boundary value problem (because F' depends on |∇Φ|², which depends on the solution). Standard numerical methods (relaxation, shooting, or spectral methods) would handle it, but it requires choosing the explicit form of F that encodes the stellated octahedron topology.

The result would be a red curve that passes *near* but not *through* each observation point, smoothed by the differential operator. The residuals would reveal the true observation noise, separated from the physical signal by the field equation's smoothing kernel.

---

## 4. Summary: The Three Levels

| Level | Object | Type | What it does |
|-------|--------|------|-------------|
| **Constitutive law** | u(x) = x/(x+1) | Algebraic, pointwise | Maps g_s ↔ g_t. The Newtonian fraction. Local thermometer. |
| **Field equation** | f(x) = (21x+13)/(x+1) | Algebraic, pointwise | Full stellated coupling including TetB. Same structure, larger correction. |
| **SST** | S_ST action principle | Differential, covariant | The gravitational theory. Propagation, smoothing, lensing. The weather system. |

In spherical symmetry, all three collapse to algebraic relations between g_s and g_t. The difference between u(x) and f(x) is the amplitude of the TetB contribution. The difference between f(x) and the SST is the gradient coupling — the differential structure that makes it a field theory rather than a lookup table.

The pipeline as currently implemented uses Level 1 (gold curves) and Level 2 (red curves) interchangeably for the forward/inverse maps. Both nail the observations by construction. The smoothing that would distinguish the SST from a pointwise algebraic relation requires solving the actual field equation as a differential equation — Level 3.

---

*Gravity Field Dynamics — Nelson (2026)*
*Stellated Octahedron Topology · K=4, D=3 · f(x) = (21x+13)/(x+1)*
