# The AQUAL Algebra, Taken Further

*The one-directional law, its inverse, the bound law and the energy functional as one algebra · Field Dynamics Research · working note, November 2026*

---

## Where the archive stands

The archive takes the constitutive law $\mu(x) = x/(x+1)$ through four steps:

- three derivations: exchange symmetry, the metric read, and equilibrium closure;
- the closed-form kinetic function $F(y) = y - 2\sqrt y + 2\ln(1+\sqrt y)$;
- its convexity and ellipticity (Theorem 2 of the energy-functional proof);
- the logistic equation $x\,\mu' = \mu(1-\mu)$.

Separately, Papers XI and XIII use the bound law $x(1-\mu)^2 = \mu$ for nuclei.

The pieces have not yet been connected to each other. This note connects them. Every claim is checked twice: once directly and once by an independent route. The [Verification](#verification) section describes both.

**Notation.**

| Symbol | Meaning |
|---|---|
| $x = g_t/a_0$ | total acceleration |
| $z = g_s/a_0 = x\mu$ | source (baryonic) acceleration |
| $\mu$, $1-\mu$ | TetA share, TetB share: the fractions of the coupling capacity resolved through each chamber |
| $\Omega = \mu/(1-\mu)$ | odds between the chambers |
| $\varphi = (1+\sqrt5)/2$ | the golden ratio |

**Terms.** The following terms recur in this note. The archive does not always keep them apart, so they are fixed here.

*TetA and TetB.* A galaxy is a vortex, with an exterior and an interior ([decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/)).

- **TetA** is the exterior: the observable disk, our spacetime, in which stars and gas orbit. The baryons are tracers of the flow. They follow it but do not set it.
- **TetB** is the interior: the subspace reached only through the Field Origin. In a galaxy it lies beyond the throat at the centre, the drain of the vortex. Matter spirals inward through the throat and passes into TetB, so **a galaxy's TetB is occupied, not empty**. Paper VII accordingly counts galaxies among the bound gravity-field configurations.
- **Empty TetB.** Only an individual *unbound envelope*, a single tile of the long-range mesh, has an empty TetB chamber (Paper VII).

*The deep field.* The deep field, or deep-MOND regime, is the low-acceleration regime $x \ll 1$, in which $\mu \to x$ (Paper VII; Letter 2). It is a range of $x$. A galaxy reaches it toward its rim (Letter 3), so it lies in the exterior, among the tracers, as far from TetB as the galaxy extends. The deep field is not TetB.

*The TetB share.* The quantity $1-\mu$ is the fraction of the coupling capacity resolved through TetB (Paper VII). It characterises the partition of the field at a point, not the occupancy of TetB. It belongs to the *quiet* prediction: the field the constitutive law yields when the interior neither drives nor brakes the rotation.

*The interior's active contribution.* Departures from the quiet prediction are measured separately, by $\Delta M_{\text{eff}} = M_{\text{phot}} - M_{\text{dec}}$ ([decoding-mass letter](../../papers/letter-decoding-mass-from-rotation-curves/); [`what_is_gravity.md`](../g_from_topology/what_is_gravity.md) §7). The interior is quiet when $\Delta M_{\text{eff}} = 0$, and otherwise it drives or brakes the rotation. $\Delta M_{\text{eff}}$ is not the TetB share.

*The state label $s$ and the share difference $\sigma(x)$.* These are kept strictly apart.

- **$s$** is the state label of the coupling polynomial $f(K, s) = 1 + sK + K^2$. It takes the values $s = +1$ (TetA), $s = 0$ (the Field Origin) and $s = -1$ (TetB), and names states of the structure.
- **$\sigma(x) = (x-1)/(x+1) = \mu - (1-\mu)$** is the TetA share minus the TetB share at acceleration $x$. It is a continuous function of position in the field.
- **$f(K, \sigma(x)) = 13 + 8\mu$** is the coupling capacity at that acceleration.

$\sigma(x)$ takes the *values* of the state labels without being those states:

- $\sigma(x) = 0$ on the ring $x = 1$, a radius in the exterior where the shares are equal. The ring is not the Field Origin, which in a galaxy is the gate at the centre.
- $\sigma(x) \to -1$ only as $x \to 0$, in the deep field, where the TetB share approaches 1. That is not TetB.

*Naming.* The law $x(1-\mu) = \mu$ is called the *one-directional law*: matter sources the field and the field does not source itself. It governs the exterior field of a galaxy. A galaxy is never unbound; it is a vortex whose TetB is occupied, fed through the drain at its centre. The self-consistent law $x(1-\mu)^2 = \mu$ of the nuclear papers keeps its archive name, the *bound law*. Throughout, "TetB share" means $1-\mu$ and "deep field" means $x \ll 1$.

---

## 1. One algebra, two readings, three forms

The archive keeps two statements apart:

- **The constitutive law**, $\mu(x) = x/(x+1)$, is kinematic: the TetA share at acceleration $x$.
- **The field equation's spherical-static limit**, $g_s = g_t^2/(a_0 + g_t)$, is dynamic: it comes from varying the action.

They are connected by the AQUAL identity $\mu = dF/dy$ and are algebraically identical, but they are not the same statement. The three forms below share one algebra. (1a) is the constitutive law. (1b) and (1c) bring in the source acceleration $g_s$, so they are readings of the field equation.

$$\text{(1a)}\quad x(1-\mu) = \mu, \qquad \text{(1b)}\quad z(1-\mu) = \mu^2, \qquad \text{(1c)}\quad g_t = g_s + a_0\,\mu .$$

- **(1b)** follows from (1a) with $z = x\mu$ and $x = \mu/(1-\mu)$.
- **(1c)** says the TetB share of the acceleration is $(1-\mu)g_t = (1-\mu)x\,a_0 = \mu\,a_0$. **The share of the field resolved through TetB is $a_0$ times the TetA share.** It never exceeds $a_0$, as Letter 3 states, and it equals $a_0/2$ on the ring $x = 1$.

**Closed forms from (1b).** Solving (1b) as a quadratic gives the forward pipeline:

$$g_t = \tfrac12\Big(g_s + \sqrt{g_s^2 + 4a_0 g_s}\Big), \qquad \nu \equiv \frac{g_t}{g_s} = \frac{1 + \sqrt{1 + 4a_0/g_s}}{2}.$$

For a point mass this gives the full rotation curve in closed form:

$$v^2 = \frac{v_N^2}{2} + \sqrt{\frac{v_N^4}{4} + GMa_0}.$$

The Newtonian part $v_N^2 = GM/r$ fades with radius, and $v^4$ tends to $GMa_0$.

**The golden ratio in the one-directional law.** At $g_s = a_0$, (1b) becomes $\mu^2 + \mu - 1 = 0$. So $\mu = 1/\varphi$ and $g_t = \varphi\,a_0$. The archive has the golden ratio only in the bound law, at $x = 1$. It is also in the one-directional law, at unit *source* acceleration.

**Scope: where these forms are pointwise.**

- **GFD's field equation.** The scalar sector of GFD's covariant action has the AQUAL form, so its field equation is the AQUAL one. In it, $\mu(|g_t|/a_0)\,\vec g_t = \vec g_s$ holds pointwise only where the curl term of Bekenstein and Milgrom vanishes: spherical, cylindrical and planar symmetry. Elsewhere (1a)–(1c) and $\nu$ are approximations whose error is that curl field.
- **QUMOND, for comparison.** QUMOND (§7) is a different action, not a rewriting of GFD's. Its field equation makes (1a)–(1c) exact by construction in any geometry. There the vector form of (1c) is
$$\vec g_t - \vec g_s = a_0\,\mu\!\left(\frac{|\vec g_t|}{a_0}\right)\hat g_s ,$$
so the TetB share of the field is $a_0\mu$ along the source field. The density a halo fit would infer from that share is $\rho_B = (a_0/4\pi G)\,\nabla\cdot(\mu\,\hat g_s)$. In GFD this vector form holds where the curl term vanishes.

The point-mass forms and density slopes (§§7–10) are spherical, so for them the distinction does not arise. The kinetic functions $F$, $F_b$ and $Q$ are local and hold in any geometry.

## 2. The bound law is the exchange image of the source form

The exchange $(x, \mu) \to (1/x,\, 1-\mu)$ is derived in the exchange-symmetry proof. In the total variable it carries (1a) to itself, which is $\mu(x) + \mu(1/x) = 1$.

Apply the same exchange to the source form (1b):

$$z(1-\mu) = \mu^2 \quad\xrightarrow{\;(z,\mu)\,\to\,(1/z,\,1-\mu)\;}\quad z\,(1-\mu)^2 = \mu .$$

**That is Paper XIII's bound law, exactly.** Equivalently, $1 - \mu_b(x) = 1/\nu(1/x)$: the bound law's TetB share at $x$ is the one-directional law's $g_s/g_t$ at source acceleration $a_0/x$.

Three things follow.

- **The two golden ratios are one equation.** The one-directional TetA share at $g_s = a_0$ and the bound TetB share at $x = 1$ are both $1/\varphi$. Each is the root of $\mu^2 + \mu - 1 = 0$, read from either side of the exchange.
- **The $1/A$ saturation is the bound law's asymptote.** For large $x$, $1 - \mu_b \simeq 1/\sqrt x - 1/(2x)$. At $x = A^2$ this is $1/A$, against $1/(1+A^2)$ for the one-directional law. This is the "$1/A$, not $1/A^2$" signature claimed in [`bound-gravity-and-packing/`](../bound-gravity-and-packing/).
- **Degree depends on the variable.** The one-directional law has degree $(1,1)$ in $(x,\mu)$ but degree $(1,2)$ in $(z,\mu)$, the same degree the bound law has in $x$. The exchange proof's premise (A), that the degree in $\mu$ counts the directions in which the coupling runs, therefore holds in the total variable specifically. The proof works in $x$, so it is unaffected, but the reading of "degree" should say which variable it uses.

- **The cycle closes.** Rewrite the bound law in *its* source variable $z_b = x\mu_b$. Then $x = \mu/(1-\mu)^2$ gives $\sqrt{z_b} = \mu/(1-\mu)$, so
$$\mu_b = \frac{\sqrt{z_b}}{1 + \sqrt{z_b}} .$$
In its own source variable, the bound law is the one-directional law at $\sqrt{z_b}$. That form is exchange-symmetric again. §11 shows this is one orbit of two operations.

**Status.** The identity is exact. It is a candidate derivation of the bound law from the one-directional law plus the exchange. Whether exchanging in the source variable is the physical content of "binding" is the framework's call, not the algebra's.

## 3. The logistic family

Every member of the necessity table's family $x^n(1-\mu)^m = \mu$ has a logistic form:

$$x\,\frac{d\mu}{dx} = \frac{n\,\mu(1-\mu)}{1 + (m-1)\mu}.$$

| Law | $x\,\mu'$ | Value at $x = 1$ | Slope at $x = 1$ |
|---|---|---|---|
| One-directional, $(n,m) = (1,1)$ | $\mu(1-\mu)$ | $\mu = 1/2$ | $1/4$ |
| Bound, $(n,m) = (1,2)$ | $\mu(1-\mu)/(1+\mu)$ | $\mu = 1/\varphi^2$ | $1/(\sqrt5\,\varphi^2) = (3\sqrt5 - 5)/10 \approx 0.171$ |

The denominator $1+\mu$ is the bound law's extra direction. The bound transition is slower and peaks later. Its rate is greatest at $\mu = \sqrt2 - 1$, that is at $x = (1+\sqrt2)/2 \approx 1.21$, where it reaches $(\sqrt2-1)^2 \approx 0.172$. The one-directional rate peaks at $1/4$ at $x = 1$ itself.

## 4. The anisotropy of the field equation is the TetB share

Theorem 2 gives the two Hessian eigenvalues of the energy as $2\mu$ (twice, transverse) and $2(x\mu)'$ (once, along the field). Their ratio is $1 + x\mu'/\mu$, and for the one-directional law

$$\frac{(x\mu)'}{\mu} = \frac{x+2}{x+1} = 1 + (1-\mu).$$

**Stiffness along the field exceeds stiffness across it by exactly the TetB share.** The equation is isotropic where that share vanishes ($x \gg 1$, Newtonian) and approaches a factor of 2 as the share approaches 1 ($x \ll 1$, the deep field). This is a statement about the partition at each point, not about TetB's occupancy. For the bound law the ratio is $2/(1+\mu)$.

For the whole family the ratio is $1 + n(1-\mu)/(1 + (m-1)\mu) > 1$. Both eigenvalues stay positive, so every member gives a strictly convex, elliptic AQUAL equation.

## 5. The logarithm is the screening identity integrated

The screening identity (1a) can be read as $\mu/x = 1-\mu$. Integrating it gives

$$\ln(1+x) = \int_0^x (1-\mu)\,dx' = \int_0^x \mu\;d\ln x' .$$

The logarithm in $F$ is the TetB share integrated on the linear measure, which the Letter 3 summary notes. It is equally the TetA share integrated on the logarithmic measure, which is the measure the exchange $x \to 1/x$ leaves invariant.

**$F$ in partition variables.** With $\sqrt y = x = \Omega$,

$$F = \Omega^2 - 2\Omega - 2\ln(1-\mu).$$

**The TetB share of the energy.** Its complement is

$$y - F = \int_0^y (1-\mu)\,dy' = 2\big[\sqrt y - \ln(1+\sqrt y)\big].$$

This grows only as $2\sqrt y$. The energy of the TetB share is sub-quadratic, the energy-level counterpart of the TetB share of the acceleration being bounded by $a_0$ in (1c).

## 6. The mean coupling is 17 by exchange symmetry

Evaluating the coupling polynomial at the share difference $\sigma(x) = (x-1)/(x+1)$ gives the capacity at acceleration $x$,

$$f(K, \sigma(x)) = 13 + 8\mu = \frac{21x + 13}{x+1}.$$

Because $\mu(x) + \mu(1/x) = 1$, the average of $\mu$ over any window symmetric in $\ln x$ is exactly $1/2$, so $\langle f\rangle = 17$.

This is the continuous counterpart of the closure-climb result that 17, the value of the Field Origin state, is the mean of a closure. Both rest on one fact: $f$ is affine in its second argument, and both measures are symmetric about the value 0. In the closure climb that argument runs linearly with the hexagram count; here it is $\sigma(x)$.

The bound law is not exchange-symmetric. Over the same windows it gives the following, all below 17:

| Window | $\lvert\ln x\rvert \le 0.5$ | $\le 2$ | $\le 10$ |
|---|---|---|---|
| Bound law $\langle f\rangle$ | 16.06 | 16.10 | 16.61 |

## 7. Closed forms

**The Legendre dual of $F$ is the QUMOND kinetic function.** With $z = |g_s|/a_0$ and $Q'(z^2) = \nu(z)$:

$$Q(z^2) = \frac{z^2}{2} + \frac{(z+2)\sqrt{z(z+4)}}{2} - 4\,\mathrm{asinh}\frac{\sqrt z}{2}.$$

It is the exact Legendre transform of the GFD energy density, $W^*(2z) = Q(z^2)$. This duality is between energy densities, not actions. QUMOND built on $Q$ is a separate action, which matches GFD's field equation where the curl term vanishes and differs from it elsewhere. It is not a rewriting of GFD's covariant action. At unit source acceleration, $z = 1$, $\mathrm{asinh}(1/2) = \ln\varphi$. The AQUAL–QUMOND duality is standard (Milgrom 2010); this closed form for GFD's $\mu$ is new to the archive.

**The bound law has an algebraic kinetic function, with no logarithm.**

$$F_b(y) = y + \sqrt y - \Big(\tfrac23\sqrt y + \tfrac16\Big)\sqrt{1 + 4\sqrt y} + \tfrac16 .$$

- **Deep field:** it has the same deep-field limit as $F$, $\tfrac23 y^{3/2} - y^2 + \cdots$.
- **Strong field:** it goes as $y - \tfrac43 y^{3/4} + \cdots$, with no $\ln y$.

So the logarithm, which the archive reads as the Field Origin term, belongs to the one-directional law only.

**The potential of a point mass.** With $r_M = \sqrt{GM/a_0}$:

$$\Phi(r) = \sqrt{GMa_0}\left[\mathrm{asinh}\frac{2r}{r_M} - \frac{r_M}{2r}\Big(1 + \sqrt{1 + 4r^2/r_M^2}\Big)\right].$$

| Region | $\Phi(r)$ | Reading |
|---|---|---|
| Inside $r_M$ | $-GM/r + a_0 r + \cdots$ | the TetB share of the acceleration, which tends to $a_0$ near the mass (1c) |
| Outside $r_M$ | $\sqrt{GMa_0}\,[\ln(4r/r_M) - 1]$ | the logarithmic potential of flat rotation |

## 8. A check on Letter 3's "bounded central density"

Letter 3, as summarised in [`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md), lists as a consequence that the TetB fraction never exceeds unity, "so the torsion-sector acceleration never exceeds $a_0$. This removes the central divergence of cuspy halo profiles algebraically."

The acceleration statement is exact; it is (1c). The density statement does not follow from it. The density a halo fit would infer from the TetB share of the field, in spherical symmetry, is

$$\rho_B = \frac{a_0}{4\pi G\,r^2}\,\frac{d(r^2\mu)}{dr}.$$

Its slope at the centre is:

| Baryons | $d\ln\rho_B/d\ln r$ at the centre |
|---|---|
| Point mass | $-1$, with $\rho_B \to a_0/(2\pi G r)$ |
| $1/r$ cusp (Hernquist) | $-1$, with $\rho_B \to a_0\mu_c/(2\pi G r)$, $\mu_c$ the central share |
| Uniform core (Plummer) | $-\tfrac12$, with $\rho_B \to \tfrac52\,(a_0/4\pi G)\,(r/b)^{-1/2}$ for $GM = a_0 b^2$ |

So the inferred density $\rho_B$ stays finite in mass but is not bounded. Around cuspy baryons it has the same $1/r$ slope as NFW. Around cored baryons it is a shallower $r^{-1/2}$ cusp. The reason is that the acceleration falls below $a_0$ at the very centre, which puts the centre in the deep-field regime.

A wording that stays within the algebra: *the TetB share of the acceleration never exceeds $a_0$, so the mass it implies grows no faster than $a_0 r^2/G$.* Any stronger statement about central density needs the baryon profile.

## 9. The point mass in one hyperbolic variable

Set $\sinh\psi = 2r/r_M$, with $r_M = \sqrt{GM/a_0}$. Every square root in §7 is then a perfect square, since $1 + 4r^2/r_M^2 = \cosh^2\psi$, and the whole point-mass field takes one line each:

$$\frac{g_t}{a_0} = \operatorname{csch}^2\frac{\psi}{2}, \qquad \mu = \operatorname{sech}^2\frac{\psi}{2}, \qquad v^2 = \sqrt{GMa_0}\,\coth\frac{\psi}{2}, \qquad \Phi = \sqrt{GMa_0}\;\psi - v^2 .$$

- **An invariant.** $\Phi + v^2 = \sqrt{GMa_0}\,\psi$ at every radius. The potential and the circular speed are tied together by the one variable $\psi$.
- **Limits.** As $\psi \to \infty$, $\coth \to 1$ and $v^4 \to GMa_0$. As $\psi \to 0$, $\coth(\psi/2) \approx 2/\psi \approx r_M/r$ and $v^2 \to GM/r$.
- **Unit source field and unit total field.** Unit source field, $g_s = a_0$, is reached at $r = r_M$, where $\cosh^2(\psi/2) = \varphi$ and $\mu = 1/\varphi$. Unit total field, $g_t = a_0$ (the ring $x = 1$), is reached at $r = \sqrt2\,r_M$, where $\sinh(\psi/2) = 1$, so $\psi/2 = \ln(1+\sqrt2)$, the logarithm of the silver ratio. The golden ratio marks unit source field and the silver ratio marks unit total field.

## 10. The bound law in the same variable

With $\sinh\psi = 2\sqrt x$, the bound law $x(1-\mu)^2 = \mu$ becomes

$$\mu_b = \tanh^2\frac{\psi}{2}, \qquad 1 - \mu_b = \operatorname{sech}^2\frac{\psi}{2}.$$

Compare §9. **At the same $\psi$, the bound law's TetA share is the point mass's TetB share**, with $x = r^2/r_M^2 = a_0/g_s$. This is identity 2c of §2 in geometric form: the bound law reads the point-mass field from the other side of the exchange. The QUMOND energy $Q$ of §7 also lives on this variable: on the point-mass field, $z = g_s/a_0 = 4/\sinh^2\psi$, and its logarithmic term is $\mathrm{asinh}(\sqrt z/2) = \ln\coth(\psi/2) = \ln\big(v^2/\sqrt{GMa_0}\big)$.

For comparison, the one-directional law in its natural variable $\sqrt x = e^{\theta}$ is $\mu = (1 + \tanh\theta)/2$. The one-directional law is a tanh of a logarithm; the bound law is a tanh squared of an asinh.

## 11. Two operations generate the laws

Take the family $x^n(1-\mu)^m = \mu^k$, which includes the necessity table's alternatives, and the two operations used above:

- **S**, rewrite in the source variable $z = x\mu$: $(n, m, k) \to (n, m, k+n)$;
- **E**, the exchange $(x,\mu) \to (1/x, 1-\mu)$: $(n, m, k) \to (n, k, m)$.

A law depends only on the ratio $n : m : k$, since taking roots does not change its solution. Starting from the one-directional law $U = (1,1,1)$:

$$U \xrightarrow{\;S\;} (1,1,2) \xrightarrow{\;E\;} (1,2,1) = \text{bound} \xrightarrow{\;S\;} (1,2,2) = U \text{ at } \sqrt z \xrightarrow{\;E\;} \text{itself}.$$

Two facts about the family make the uniqueness of the one-directional law structural:

- **Tails.** $\mu \sim x^{n/k}$ in the deep field and $1 - \mu \sim x^{-n/m}$ in the strong field.
- **Fixed points.** The members fixed by E are exactly $m = k$, which are the laws $\mu = x^a/(1+x^a)$ with $a = n/m$. All of them are exchange-symmetric.

So within the family, **deep-field scaling ($n = k$) plus exchange symmetry ($m = k$) leaves only $n = m = k$: the one-directional law.** This is the exchange proof's conclusion reached without the degree lemma: premise (A) is replaced by the deep-field exponent, which the equilibrium route already fixes.

## 12. Composition: the partition adds like rapidities

The share difference $\sigma(x) = (x-1)/(x+1) = \tanh(\tfrac12\ln x)$ composes under multiplied acceleration ratios by Einstein's velocity-addition law:

$$\sigma(x_1x_2) = \frac{\sigma_1 + \sigma_2}{1 + \sigma_1\sigma_2}.$$

Because the capacity is $f(K, \sigma) = 17 + 4\sigma$, the capacity at a product of scales is fixed by the capacities of its factors through this law. The odds simply multiply, $\Omega(x_1x_2) = \Omega_1\Omega_2$, since $\Omega = x$. The exchange $x \to 1/x$ is $\sigma \to -\sigma$, and $\sigma = 0$, the ring $x = 1$, is the identity of the composition. This is algebra only; how nested closures (the Solar System inside the galaxy) should compose is a physical question it does not answer.

## 13. Why general relativity never meets 13, 17 and 21

General relativity already contains every count the coupling polynomial uses. What it lacks is the parameter that joins them.

**The counts are standard.** Let $V = \mathbb R^4$ and let $\tau$ be the swap on $V \otimes V$, $\tau(a \otimes b) = b \otimes a$. Since $\tau^2 = 1$, it splits $V \otimes V$ into a symmetric part of dimension 10 and an antisymmetric part of dimension 6, with projectors $P_\pm = (1 \pm \tau)/2$. General relativity meets this split twice:

- **The tetrad** $e^a{}_\mu$ has 16 components: the 10 of the metric, and the 6 of local Lorentz transformations, which GR treats as gauge.
- **Each slice of the connection** $\Gamma^\lambda{}_{\mu\nu}$ has 16 components: 10 symmetric (Christoffel) and 6 antisymmetric (torsion), which the torsion-free condition removes.

In both places GR keeps the symmetric sector and discards the antisymmetric one.

**The polynomial is a trace.** Since $\mathrm{Tr}\,1 = K^2 = 16$ and $\mathrm{Tr}\,\tau = K = 4$,

$$f(K, s) = 1 + \mathrm{Tr}_{V\otimes V}(1 + s\tau).$$

So $21 = 1 + 2 \cdot 10$, $17 = 1 + 16$ and $13 = 1 + 2 \cdot 6$. These are the symmetric sector doubled, the whole tensor product, and the antisymmetric sector doubled, each with the scalar 1 of the non-degeneracy condition.

**The constitutive law weights the two sectors.** Evaluate the operator at the share difference $\sigma(x) = (x-1)/(x+1)$, so that $\mu = (1+\sigma)/2$:

$$1 + \sigma(x)\,\tau = 2\big[\mu\,P_{\text{sym}} + (1-\mu)\,P_{\text{anti}}\big], \qquad f(K, \sigma(x)) = 1 + 2\big[10\,\mu + 6\,(1-\mu)\big] = 13 + 8\mu.$$

The constitutive law is the weight the operator places on the symmetric sector, and the TetB share is its weight on the antisymmetric sector. The operator's eigenvalues are $2\mu$ on the symmetric sector and $2(1-\mu)$ on the antisymmetric sector, so the acceleration ratio is their quotient: $x = \lambda_{\text{sym}}/\lambda_{\text{anti}}$. This is the odds $\Omega = x$ of the exchange proof, now read as an eigenvalue ratio.

**The weighting is a one-parameter group.** Because $\tau^2 = 1$, $e^{\theta\tau} = \cosh\theta + \tau\sinh\theta$, and with $\theta = \tfrac12\ln x$,

$$1 + \sigma(x)\,\tau = \operatorname{sech}\theta\; e^{\theta\tau}.$$

Up to normalisation, the operator is a boost generated by the swap, with rapidity $\theta = \tfrac12\ln x$. It acts as $\sqrt x$ on the symmetric sector and $1/\sqrt x$ on the antisymmetric sector. Two consequences follow:

- The exchange $x \to 1/x$ is $\theta \to -\theta$, which interchanges the two sectors.
- The rapidity addition of §12 is the group law $e^{a\tau}e^{b\tau} = e^{(a+b)\tau}$.

**Where general relativity sits.** GR sets $\mu = 1$: Einstein's equation is the TetA partition with the constitutive law fixed at unity ([`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md)). Then $\sigma = +1$, $1 + \sigma\tau = 2P_{\text{sym}}$, the antisymmetric sector has weight zero, $\theta = \infty$, and $f = 21$ identically. The share difference has reached the value of the TetA state label, $s = +1$. In that limit:

- 21 is a fixed count, $1 + 2\dim\mathrm{Sym}^2 V$, with no partner value to compare it with.
- 17 and 13 require $\mu < 1$, a non-zero weight on the antisymmetric sector. GR's two conventions, one root of the tetrad equation and a torsion-free connection, set that weight to zero.
- Nothing in GR combines the non-degeneracy scalar and the doubled sectors into one polynomial in a sign parameter.

The three integers are therefore not absent from general relativity: their ingredients, 10, 6 and 16, are textbook. They are never assembled, because GR evaluates the operator only at $\sigma = +1$, and an endpoint value is a count, not a coupling.

**Status.** The operator identities are exact (checked below). Reading $\mu$ as the weight on the metric sector rests on the archive's identification of the antisymmetric sector with TetB (Letters 2 and 3). What the algebra adds is that the constitutive law and the coupling polynomial are one and the same weighting of $\mathrm{Sym}^2 V \oplus \Lambda^2 V$.

---

## Status

| Result | Status |
|---|---|
| (1c) $g_t = g_s + a_0\mu$; source form (1b) | Exact; new readings of a known law |
| $\nu(z)$, the point-mass $v^2$ and $\Phi$ | Exact; standard for this $\mu$ in MOND, now stated in GFD terms |
| One-directional golden ratio at $g_s = a_0$ | Exact; not previously in the archive |
| Bound law = exchange of (1b) | Exact identity; its physical reading is open |
| $1 - \mu_b \simeq 1/\sqrt x$, giving $1/A$ | Exact asymptote; consistent with the bound-gravity README |
| Logistic family; bound slope $1/(\sqrt5\varphi^2)$ at $x = 1$ | Exact |
| Anisotropy $= 1 + (1-\mu)$; family convexity | Exact, from Theorem 2 |
| Logarithm as the screening identity integrated; $F$ in $\Omega$; TetB energy | Exact |
| $\langle f\rangle = 17$ from exchange symmetry | Exact; explains the closure-climb mean as a symmetry |
| QUMOND dual $Q$; bound $F_b$ | Exact closed forms, new to the archive |
| Cusp in the density inferred from the TetB share, slopes $-1$ and $-\tfrac12$, with coefficients | Exact asymptotics; bears on Letter 3, consequence 2 |
| Vector form $\vec g_t - \vec g_s = a_0\mu\,\hat g_s$ | Exact in GFD's (AQUAL-form) field equation where the curl term vanishes; exact everywhere in QUMOND, a separate action |
| Hyperbolic point mass; $\Phi + v^2 = \sqrt{GMa_0}\,\psi$; golden ratio at unit source field, silver ratio at unit total field | Exact |
| Bound law $= \tanh^2(\psi/2)$; it mirrors the point mass's TetB share | Exact |
| S and E generate the laws; the bound law's source form is $U(\sqrt z)$ | Exact |
| Deep scaling plus exchange symmetry select $U$ within the family | Exact, within the stated family |
| Rapidity composition of $\sigma(x)$ | Exact; its physical use is open |
| $f(K,s) = 1 + \mathrm{Tr}(1 + s\tau)$; $1 + \sigma(x)\tau = 2[\mu P_{\text{sym}} + (1-\mu)P_{\text{anti}}]$; $x = \lambda_{\text{sym}}/\lambda_{\text{anti}}$; GR at $\mu = 1$ | Exact; the physical reading of the sectors is the archive's |

## Verification

Two scripts, standard `sympy` and `mpmath`:

| Script | Checks | Method |
|---|---|---|
| [`verify_aqual_algebra.py`](verify_aqual_algebra.py) | 50 | Each claim checked by the algebra that produced it: symbolic simplification, exact series and limits |
| [`verify_independent.py`](verify_independent.py) | 48 | Independent routes, listed below |

The independent script does not reuse the closed forms it tests:

1. every identity evaluated at random points to 60 digits: 200 points with tolerance $10^{-45}$, or $10^{-30}$ where a numerical derivative or integral is involved (40 points for the integrals);
2. the hyperbolic forms proved symbolically through $a = \sinh(\psi/2)$, with the perfect square shown explicitly;
3. the field solved from Gauss's law by root-finding, with no closed-form inverse, and the potential obtained by quadrature, for a point mass and a Plummer sphere;
4. the QUMOND vector form tested on 300 random non-spherical field vectors;
5. the Legendre dual computed as a numerical supremum, not from its maximiser;
6. the Hessian of the energy by finite differences in three dimensions at random gradients;
7. the family: irreducibility over $\mathbb Q$, a Sturm count of one root in $[0,1]$, the action of S and E on 25 random members, and the tails solved in log space;
8. the mean coupling 17 by quadrature in two different measures;
9. the central slopes and coefficients of the density inferred from the TetB share, from numerical derivatives of the root-found field.

```bash
pip install sympy mpmath
python verify_aqual_algebra.py     # 50/50
python verify_independent.py       # 48/48
```

Checking found one error in the first draft of this note: the bound law's rate peaks *later* than $x = 1$, not earlier (§3).

## References

- Bekenstein, J. and Milgrom, M. (1984). Does the missing mass problem signal the breakdown of Newtonian gravity? *Astrophys. J.* 286, 7.
- Milgrom, M. (2010). Quasi-linear formulation of MOND. *Mon. Not. R. Astron. Soc.* 403, 886.
- Archive sources: [`proofs/aqual-energy-functional/`](../../proofs/aqual-energy-functional/), [`proofs/constitutive-law-exchange-symmetry/`](../../proofs/constitutive-law-exchange-symmetry/), [the equilibrium route](../../papers/letter-constitutive-law-tetrad-geometry/Supplementary/supplementary_equilibrium_route.tex), [Paper XIII](../../papers/13-nuclear-binding-bidirectional-sst/), [`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md), [`g_from_the_closure_climb.md`](../g_from_topology/g_from_the_closure_climb.md). The [README](README.md) maps the rest.
