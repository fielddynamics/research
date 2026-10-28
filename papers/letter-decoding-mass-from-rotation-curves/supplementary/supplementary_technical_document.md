# Supplemental Material (Technical Document): Derivation and Uniqueness Argument

**Scope.** This document supports the letter "Gravity Field Dynamics: Decoding mass from observed rotation curves." It is self-contained: no references to Paper I, Paper II, Zenodo, or other unpublished work. The letter states: "See Supplemental Material for the derivation and uniqueness argument." No other papers need to be cited in the letter or this supplement. The Tully-Fisher velocity evolution paper remains internal; it can be provided as additional supplementary material if referees request it.

---

## Document spine (internal use)

| Section | Core purpose | Three key concepts | Exit with |
|---------|--------------|--------------------|-----------|
| 1 | Establish that the constitutive law is uniquely fixed, not chosen | MSC class and postulates A1–A3; detailed balance and exchange symmetry fix n = 1; same functional form as MOND "simple" but different logical status | Reader knows why the "simple" interpolant is the minimal-closure fixed point |
| 2 | Show that the letter equations are the spherical limit of the covariant theory | Tetrad and field closure; two tetrads and coupling hierarchy; scalar-tensor action reduces to Poisson + transition | Reader sees Poisson + transition as the limit, not disconnected machinery |
| 3 | Address smoothing choice and sensitivity of decoded mass | Why 6.2% smoothing; sensitivity over 4%–10%; decoded mass remains well below LambdaCDM at outer radii | Reader accepts robustness and knows the numbers |

---

## Section 1. Why the constitutive law is unique, not chosen

**Spine (internal):**  
**Purpose:** Show that \(\mu(x) = x/(1+x)\) is uniquely fixed within a declared closure class, so it is not an ansatz.  
**Key concepts:** (1) Minimal Single-Channel Saturating Closure (MSC) and postulates A1–A3. (2) Detailed balance at the closure boundary gives \(\varepsilon = x/(1+x)\); exchange symmetry \(x \to 1/x\) forces \(n = 1\) in \(\mu(x) = x/(n+x)\). (3) Same functional form as the "simple" MOND interpolant, but here it is a uniqueness result, not a model choice.  
**Exit with:** Reader understands that we explain why the "simple" interpolant is the unique equilibrium law under minimal closure assumptions.

---

The letter uses the relation \(\mu(x) = x/(1+x)\) with \(x = g_{\mathrm{t}}/a_0\), which in form coincides with the "simple" MOND interpolating function used in many rotation-curve fits. The important distinction is one of status, not shape. In phenomenological MOND, \(\mu\) is typically chosen from a family of interpolating functions. Here it is not an ansatz: it is uniquely fixed as the equilibrium solution within a well-defined closure class derived from field-closure constraints at the boundary \(\Sigma\).

That closure class is the Minimal Single-Channel Saturating Closure (MSC). Within it, three postulates determine the constitutive response: (A1) local closure at the field boundary \(\Sigma\); (A2) lossless transmission (no extra dissipation channel); and (A3) a single calibration state at \(\Sigma\) (one scale fixes the response). Under these postulates, \(\mu(x) = x/(1+x)\) is the unique solution. Other forms (e.g. \(\mu = x/\sqrt{1+x^2}\), the "standard" MOND interpolant) correspond to different closure assumptions (non-minimal or multi-channel) and remain testable against data. So \(\mu\) is not a fitted choice; it is the unique form in the minimal closure class.

A second route to the same result uses detailed balance and symmetry at the closure boundary. The field partitions into a resolved fraction \(\varepsilon\) (transmitted) and an unresolved fraction \(1 - \varepsilon\) (saturated). At equilibrium, the resolution rate scales as \(x(1-\varepsilon)\) and the relaxation rate as \(\varepsilon\); balancing them gives \(\varepsilon = x/(1+x)\), so \(\mu(x) \equiv \varepsilon(x) = x/(1+x)\). Why the constant in the denominator is 1 and not some other number follows from the topology of the stellated octahedron. Define \(x = g/a_0\). Under exchange of the two tetrahedral sectors (TetA \(\leftrightarrow\) TetB), the dimensionless acceleration transforms as \(x \to 1/x\). Total capacity is unity: \(\mu(x) + \mu(1/x) = 1\). For the one-parameter family \(\mu(x) = x/(n+x)\), this holds if and only if \(n = 1\). In the scalar-tensor reduction, the closure condition at the Field Origin contributes an additive constant in the constitutive denominator; that constant appears as 1 in \(\mu(x) = x/(1+x)\).

**Summary for the supplement.** Our constitutive law coincides with the commonly used "simple" MOND interpolant, but here it is uniquely fixed as the equilibrium solution within the Minimal Single-Channel Saturating Closure (MSC) class derived from field-closure constraints at \(\Sigma\). The core claim is conditional and referee-safe: unique within MSC under postulates A1–A3. This result retrospectively explains why the "simple" interpolant performs well in fits: it is the minimal closure fixed point.

---

## Section 2. From tetrad and bimetric theory to the letter equations

**Spine (internal):**  
**Purpose:** Show that the working machinery of the letter (Poisson equation plus transition relation in spherical symmetry) is the limit of the full covariant theory, not name-dropped machinery.  
**Key concepts:** (1) Tetrad formulation and field closure (non-degeneracy of the metric). (2) Two tetrads, opposite orientations, and the coupling polynomial \(f(k) = 1 + k + k^2\) at \(k = 4\); zero free parameters. (3) The covariant scalar-tensor action reduces in spherical symmetry to Poisson plus a single algebraic relation between source and total acceleration.  
**Exit with:** Reader sees that Eqs. (1) and (3)–(4) of the letter are the spherical limit of tetrad-based, ghost-free bimetric field closure.

---

The letter is built on two equations: the Poisson equation for the potential and the transition relation between source acceleration \(g_{\mathrm{s}}\) and total acceleration \(g_{\mathrm{t}}\). These are not introduced ad hoc. They are the spherically symmetric limit of a covariant theory based on the tetrad formulation of general relativity and ghost-free bimetric gravity.

In the tetrad formulation, the metric is \(g_{\mu\nu} = \eta_{ab}\, e^a_\mu\, e^b_\nu\). The four tetrad legs at each point span the tangent space; in \((3+1)\) dimensions the spatial triad defines a tetrahedron at each field node. Field closure is the requirement that the metric be non-degenerate everywhere, \(\det(g) \neq 0\), i.e. that the four legs span completely. Self-consistency and ghost-freedom require two tetrahedral sectors with opposite orientations, coupled at a single vertex (the Field Origin). The minimal topology that realizes this is the stellated octahedron: two tetrahedra sharing a center.

The coupling structure is encoded in the polynomial \(f(k) = 1 + k + k^2\) evaluated at \(k = 4\) (simplex count in three spatial dimensions). The terms correspond to the Field Origin (1), vierbein face propagation (4), and full bimetric coupling (16). The resulting integers fix the gravitational constant and the constitutive response; the bimetric potential is fully determined with zero free parameters. The covariant scalar-tensor action (letter Eq. 2) is
\[
S_{\mathrm{ST}} = \int d^4 x\,\sqrt{-g}\left[ \frac{R}{16\pi G} - \frac{a_0^2}{8\pi G}\,F\big(|\nabla\Phi|^2/a_0^2\big) + \ldots \right].
\]
The kinetic function \(F\) is fixed by the constitutive law: \(\mu(\sqrt{y}) = dF/dy\) with \(y = |\nabla\Phi|^2/a_0^2\) yields \(F(y) = y - 2\sqrt{y} + 2\ln(1+\sqrt{y})\). Where the structural integers (e.g. 21, 17, 13) enter explicitly, they appear in the normalization of \(G\) and in the Poisson prefactor (e.g. \(4\pi \times (17/13)\) in the scale-invariant form); one may cite a single such equation if referring to the fingerprint.

In spherically symmetric situations (rotation curves), the scalar-tensor field equation reduces to two pieces. First, the Poisson equation \(\nabla^2\Phi = 4\pi G\rho\) (letter Eq. 1), which defines the source acceleration \(g_{\mathrm{s}}\) from the mass distribution. Second, a single algebraic relation between \(g_{\mathrm{s}}\) and the total acceleration \(g_{\mathrm{t}}\) that governs circular orbits. That relation is the constitutive law \(\mu(g_{\mathrm{t}}/a_0)\) and produces the letter transition (Eqs. 3–4). So the spherically symmetric limit of the covariant theory (tetrad plus ghost-free bimetric field closure and the coupling hierarchy \(f(k)\)) is exactly: Poisson plus transition. No extra gravitational parameters beyond \(G\) and \(a_0\). The "fingerprint" is that the form of the transition is fixed by field closure (detailed balance and exchange symmetry), the coupling hierarchy determines the kinetic term \(F\) and the scale \(a_0\), and the letter equations are the spherical limit of that theory.

---

## Section 3. Uncertainty and robustness

**Spine (internal):**  
**Purpose:** Address why a fixed smoothing fraction is used and how sensitive the decoded mass is to that choice; show that conclusions are robust.  
**Key concepts:** (1) Why 6.2% smoothing: \(v^4\) in the inverse amplifies noise; a single fixed Gaussian width (6.2% of radial span) is used for all galaxies and is not tuned per object. (2) Sensitivity: varying the smoothing fraction from 4% to 10% shifts decoded masses by \(\le\)10% (MW) and \(\le\)3% (M33) at the reference radii. (3) At the outermost radii, decoded mass remains many sigma below the LambdaCDM enclosed mass.  
**Exit with:** Reader accepts that the smoothing choice is justified and that \(M_{\mathrm{dec}}\) conclusions are stable; optional note that the same 6.2% appears as a topological scatter factor elsewhere can be added if desired.

---

The inverse pipeline uses \(M_{\mathrm{dec}}(r) = r v^4 / (G(a_0 r + v^2))\). The \(v^4\) factor amplifies measurement noise in the observed velocity. To reduce point-to-point scatter without changing the large-scale profile, a single fixed Gaussian smoothing (width equal to 6.2% of the radial span) is applied to the observed velocities before decoding. This value is identical for every galaxy and is not tuned per object.

How sensitive are the decoded mass profiles to this choice? Pipeline runs with smoothing fraction 4%, 6.2%, and 10% give: for the Milky Way at 25 kpc, \(M_{\mathrm{dec}}\) in the range \(\sim 6.34\times10^{10}\) to \(\sim 6.95\times10^{10}\,M_\odot\) (range about +9.6%); at 50 kpc, \(\sim 5.80\times10^{10}\) to \(\sim 6.10\times10^{10}\,M_\odot\) (range about +5.2%). For M33 at 17 kpc, \(M_{\mathrm{dec}}\) runs from \(\sim 1.35\times10^{10}\) to \(\sim 1.39\times10^{10}\,M_\odot\) (range about \(-\)3.1%). So varying the smoothing fraction from 4% to 10% shifts the decoded masses by \(\le\)10% (MW) and \(\le\)3% (M33) at the reference radii. The decoded mass profiles and their comparison to baryonic mass are stable over this range; we use 6.2% as a single fixed value for all galaxies.

At the outermost measured radii, where velocity uncertainties are largest, the decoded effective mass remains 6.4\(\sigma\) (MW, 50 kpc) and 17.2\(\sigma\) (M33, 17 kpc) below the LambdaCDM enclosed mass. So the main conclusion (effective mass consistent with baryonic mass and far below the LambdaCDM mass budget) is robust to the smoothing choice and is not an artifact of the 6.2% value.

**Optional (if the choice is principled):** The same field topology that yields the letter equations gives a natural scatter scale \((k/\pi)^{1/4} = 1.062\) (\(\pm 6.2\%\)), from the geometric ratio between the flat tetrahedral frame (\(k=4\)) and the curved boundary (\(\pi\)). That factor bounds the Hubble tension and the Tully-Fisher velocity evolution uncertainty band in a separate, internal treatment. If the smoothing fraction is set to this topological scale, one may state: "The smoothing fraction is the topology-derived scatter factor \((k/\pi)^{1/4} = 6.2\%\), so it is fixed by the field geometry rather than chosen." If the match was coincidental, sensitivity over 4%–10% remains the main robustness answer; the Tully-Fisher velocity evolution paper can be offered as additional supplementary material if referees request it.

---

## Implementation checklist (internal)

- [ ] Letter: "See Supplemental Material for the derivation and uniqueness argument." Optional footnote: "This form is unique within MSC under postulates A1–A3 (Supplemental Material)."
- [ ] Letter (optional): "...their derivation from the full covariant theory is beyond the scope of this letter (see Supplemental Material)."
- [ ] Letter or supplement: "Varying the smoothing fraction from 4% to 10% shifts the decoded masses by \(\le\)10% (MW) and \(\le\)3% (M33) at the reference radii; we use 6.2%."
- [ ] Supplement: self-contained; no references to Paper I, Paper II, Zenodo, or Dual Tetrad by name. TF paper available as additional supplementary document if requested.
