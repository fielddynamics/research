> Field Dynamics (GFD) Framework | https://docs.fielddynamics.org | Section: Gravitation

# CMB Gravitational Enhancement

## Derivation

This page presents the formal derivation of the recombination-era gravitational enhancement factor within GFD. The Overview tab provides the physical narrative and interpretation. This tab contains only the derivation, the comparison with observation, and clearly labeled extensions.

---

### Target Quantity

The gravitational enhancement at recombination is defined as

$$\mathcal{E}_{\text{CMB}} \equiv \frac{g_t}{g_s} = \frac{1}{\mu(x_{\text{rec}})}$$

where $g_t$ is the total gravitational acceleration governing acoustic oscillations and $g_s$ is the source acceleration from baryonic matter alone. Within GFD, $\mu(x) = x/(x+1)$ is the constitutive law derived from the coupling polynomial $f(K,s) = 1 + sK + K^2$ at $K = 4$.

At the level of the gross gravitational driving that sets the depth of the acoustic potential wells, this enhancement corresponds to the quantity conventionally encoded by $\Omega_m / \Omega_b$ in $\Lambda$CDM. The identification is not a statement of full model equivalence at the level of the Boltzmann hierarchy; it is the zeroth-order correspondence between baryon-sourced and total gravitational driving at recombination. In $\Lambda$CDM, the excess is attributed to cold dark matter density $\Omega_c$. In GFD, it is attributed to the TetB fraction $(1 - \mu)$ of the constitutive law.

The observational target is:

$$\frac{\Omega_m}{\Omega_b} = 6.36 \pm 0.10 \quad \text{(Planck 2018)}$$

---

### Wall 1: The Derivation

#### Proposition 1 — Horizon-defined saturation scale

The saturation scale $a_0$ is identified with the Gibbons-Hawking acceleration of the cosmological horizon:

$$a_0 = \frac{cH}{2\pi}$$

*Proof.* The cosmological horizon at $r_H = c/H$ radiates at Gibbons-Hawking temperature $T_{\text{GH}} = \hbar H / (2\pi k_B c)$. The Unruh effect identifies acceleration $a$ with temperature $T = \hbar a / (2\pi c k_B)$. Equating gives $a_0 = cH/(2\pi)$. Since $H$ evolves with epoch, $a_0$ is not a constant. $\square$

#### Proposition 2 — Naive enhancement overshoots

Applying the deep-field limit of the scalar-tensor transition at recombination with naive linear scaling $a_0 \propto H$ predicts an enhancement of $\sim 28$, far above the Planck-inferred value $6.36 \pm 0.10$.

*Proof.* The scalar-tensor transition from the covariant action is

$$g_s = \frac{g_t^2}{a_0 + g_t}$$

At recombination, density perturbations have amplitude $\delta \sim 10^{-5}$ at acoustic scale $k \sim 0.1$ Mpc$^{-1}$. The perturbation-scale accelerations satisfy $g_t \ll a_0$, so the SST reduces to

$$g_s \approx \frac{g_t^2}{a_0} \quad \Rightarrow \quad g_t = \sqrt{g_s \cdot a_0}$$

For the present zeroth-order estimate, the perturbation-scale baryonic source acceleration is approximated by the Newtonian subhorizon expression

$$g_s \sim \frac{4\pi G \rho_b \delta}{k}$$

sufficient for estimating the gross enhancement factor rather than the full transfer function. The source acceleration is evaluated at the characteristic acoustic scale $k_\ast \sim 0.1$ Mpc$^{-1}$, corresponding to the sound-horizon-scale wells that dominate the primary acoustic response at recombination. Because $x \propto k^{-1/2}$, moderate variation around this characteristic scale changes the enhancement only sublinearly; the present calculation is a representative-scale estimate rather than a mode-by-mode fit. The inputs $\rho_b(z)$, $\delta$, $k$, and $H(z)/H_0$ are standard recombination-era quantities used here only for a zeroth-order enhancement estimate, not for a full transfer-function calculation. The only new GFD ingredient is the scaling of $a_0(z)$.

The dimensionless acceleration ratio is $x = g_t / a_0 = \sqrt{g_s / a_0}$. With naive $a_0^{\text{naive}} = cH(1100)/(2\pi) \approx 2.55 \times 10^{-6}$ m/s², evaluation gives $x \approx 0.037$, and

$$\mathcal{E} = \frac{x + 1}{x} = \frac{1.037}{0.037} \approx 28 \quad \square$$

#### Proposition 3 — Dense tiling fixes the boundary fraction and yields the cosmological exponent

In GFD, the constitutive response is a partition law: the total field capacity splits into complementary TetA and TetB fractions whose accumulation is multiplicative across independent local steps (Constitutive Law page; Poisson Equation and Scale Invariance page). Field closure is not a new postulate of GFD. It is already enforced by the nondegeneracy conditions of gravitational theory: $\det(g) \neq 0$ in metric language and $\det(e) \neq 0$ in tetrad language. A gravitational field cannot be partially closed; if closure fails, geometry is undefined. The TetA/TetB partition is the constitutive form of that closure. Because closure is required at every valid field boundary and at every scale, the same partition law applies to cosmological tiling boundaries as to galactic radial accumulation. At the cosmological tiling boundary, the exact coupled fraction is $\eta = 1/\pi$, so the surviving fraction per boundary traversal is $(1 - 1/\pi)$. Repeated independent traversals therefore give $a_0 \propto H^{1-1/\pi}$.

*Proof.* Two adjacent gravitational fields of radius $R$ in $D = 3$ dimensions have 2-sphere closure boundaries. At center-to-center separation $d$, the coupling arc subtends

$$\theta(d) = 2\arccos\!\left(\frac{d}{2R}\right)$$

This formula is specific to the intersection geometry of spheres in $D = 3$. In the discrete $K = 4$ tetrahedral packing at $d = R$, the coupling fraction is $\theta/(2\pi) = 1/3$.

GFD is a continuous field theory. At recombination, field separations sample the full accessible range $d \in [0, 2R]$. In the absence of an additional distributional parameter, the minimal parameter-free choice on the bounded interval is the uniform measure. The average coupling fraction is then

$$\frac{\langle\theta\rangle}{2\pi} = \frac{1}{2\pi} \cdot \frac{1}{2R}\int_0^{2R} 2\arccos\!\left(\frac{d}{2R}\right) dd$$

Substituting $u = d/(2R)$:

$$\frac{\langle\theta\rangle}{2\pi} = \frac{1}{2\pi} \cdot 2\int_0^1 \arccos(u)\,du$$

Integration by parts: $\int_0^1 \arccos(u)\,du = [u\arccos(u)]_0^1 + \int_0^1 u/\sqrt{1-u^2}\,du$. The boundary term vanishes. The remaining integral evaluates to $[-\sqrt{1-u^2}]_0^1 = 1$. Therefore $\langle\theta\rangle = 2$ and

$$\frac{\langle\theta\rangle}{2\pi} = \frac{1}{\pi}$$

<details>
<summary>Supporting note: uniform averaging</summary>

Additional motivations from cosmological homogeneity, near-scale-invariant primordial spectrum ($n_s = 0.965$), and microcanonical equilibrium of the baryon-photon plasma ($\delta \sim 10^{-5}$) independently support the uniform measure. Any non-uniform weighting would introduce a distributional shape parameter not present in the framework.

</details>

The coupled fraction at each boundary is $\eta = 1/\pi$. The uncoupled fraction is $(1 - 1/\pi)$. The constitutive partition law — already established as local, independent-channel, and multiplicative in accumulation — applies identically at the tiling boundary as it does radially in galaxies. Each tiling boundary is an independent partition step. The surviving fraction compounds. The exponent equals the surviving fraction per boundary traversal.

The scalar sector coupling in the covariant action, $\kappa_s = a_0^2/(8\pi G)$, scales as $H^2$ at tree level. Across independent tiling traversals induced by cosmological expansion, the compounded uncoupled fraction gives the scaling

$$\kappa_s \propto H^{2(1 - 1/\pi)}$$

Since $\kappa_s \propto a_0^2$, taking the square root:

$$a_0(z) = \frac{cH(z)}{2\pi} \cdot \left(\frac{H_0}{H(z)}\right)^{1/\pi}$$

equivalently $a_0 \propto H^{1-1/\pi}$. The exponent $1 - 1/\pi$ is the surviving fraction per boundary traversal, determined by the coupling integral. $\square$

#### Proposition 4 — Corrected enhancement is consistent with Planck

With the tiling-corrected scaling, the predicted recombination enhancement is $\mathcal{E}_{\text{CMB}} = 6.46$, consistent with the Planck-inferred value at the quoted uncertainty level.

*Proof.* At $z = 1100$, $H(z)/H_0 = 2.36 \times 10^4$ (standard Friedmann equation; depends on radiation and baryon content, not on dark matter). The suppression factor is

$$S = \left(\frac{H_0}{H(1100)}\right)^{1/\pi} = \left(\frac{1}{23{,}600}\right)^{0.3183} = 0.041$$

The corrected saturation scale: $a_0(z_{\text{rec}}) = S \cdot a_0^{\text{naive}}(z_{\text{rec}}) = 2.55 \times 10^{-6} \times 0.041 = 1.05 \times 10^{-7}$ m/s².

Since $a_0(z_{\text{rec}}) = S \cdot a_0^{\text{naive}}(z_{\text{rec}})$ and $x = \sqrt{g_s/a_0}$, the corrected ratio scales as $x_{\text{rec}} = x_{\text{naive}}/\sqrt{S}$:

$$x_{\text{rec}} = \frac{x_{\text{naive}}}{\sqrt{S}} = \frac{0.037}{\sqrt{0.041}} = \frac{0.037}{0.202} = 0.183$$

The enhancement:

$$\mathcal{E}_{\text{CMB}} = \frac{x + 1}{x} = \frac{1.183}{0.183} = 6.46$$

Comparison: $|6.46 - 6.36|/6.36 = 1.6\%$; the prediction lies at the upper edge of the quoted Planck interval ($6.36 \pm 0.10$). $\square$

---

### Derivation Chain

$$\boxed{\begin{aligned}
&\textbf{Target:} \quad \mathcal{E}_{\text{CMB}} = 1/\mu(x_{\text{rec}}) \\[6pt]
&\textbf{Deep-field SST:} \quad g_t = \sqrt{g_s \cdot a_0}, \quad x = \sqrt{g_s/a_0} \\[6pt]
&\textbf{Naive scaling:} \quad a_0^{\text{naive}} = cH/(2\pi) \\
&\quad \Rightarrow x \approx 0.037, \quad \mathcal{E} \approx 28 \\[6pt]
&\textbf{Tiling correction:} \quad \langle\theta/(2\pi)\rangle = 1/\pi \\
&\quad \Rightarrow a_0 \propto H^{1-1/\pi} \\
&\quad \Rightarrow a_0(z{=}1100) \approx 1.05 \times 10^{-7} \text{ m/s}^2 \\[6pt]
&\textbf{Corrected result:} \quad x \approx 0.183, \quad \mathcal{E} = 6.46 \\[6pt]
&\textbf{Planck target:} \quad \Omega_m/\Omega_b = 6.36 \pm 0.10 \text{ (Planck 2018)}
\end{aligned}}$$

---

### Numerical Trace

| Step | Quantity | Value |
|:---:|:---|:---|
| 1 | $a_0^{\text{naive}} = cH(1100)/(2\pi)$ | $2.55 \times 10^{-6}$ m/s² |
| 2 | $x_{\text{naive}} = \sqrt{g_s/a_0^{\text{naive}}}$ | $0.037$ |
| 3 | $\eta = \langle\theta\rangle/(2\pi)$ | $1/\pi = 0.3183$ |
| 4 | $S = (H_0/H_{\text{rec}})^{1/\pi}$ | $0.041$ |
| 5 | $a_0(z_{\text{rec}}) = S \cdot a_0^{\text{naive}}$ | $1.05 \times 10^{-7}$ m/s² |
| 6 | $x_{\text{rec}} = x_{\text{naive}}/\sqrt{S}$ | $0.183$ |
| 7 | $\mathcal{E}_{\text{CMB}} = (1 + x_{\text{rec}})/x_{\text{rec}}$ | $6.46$ |
| | $\Omega_m/\Omega_b$ (Planck 2018) | $6.36 \pm 0.10$ |

---

### Wall 2: Structural Justification

This section provides the conceptual defense for the steps used in Wall 1. Each item is labeled by its logical status.

**Why $a_0$ evolves (Level A: direct derivation).** The identification $a_0 = cH/(2\pi)$ follows from equating the Gibbons-Hawking and Unruh temperatures. Since $H$ evolves with epoch via the Friedmann equation, $a_0$ inherits this evolution. This is the same identification used at galactic scales; no additional assumption is made.

**Why naive linear scaling fails (Level A: direct derivation).** The naive prediction of $\mathcal{E} \approx 28$ overshoots by a factor of 4.3. The constitutive law $\mu = x/(x+1)$ is derived and non-negotiable. The deep-field approximation $\mu \approx x$ is accurate to 4% at $x = 0.037$. The gap therefore resides in the scaling law $a_0 \propto H$.

**Why dense packing modifies the scaling (Level B: model interpretation).** At galactic scales, gravitational fields are isolated and each samples the horizon temperature independently. At recombination, every region of space is gravitationally active and fields are densely packed with overlapping boundaries. The coupling between adjacent fields modifies how efficiently the horizon's thermal information propagates through the tiling.

**Why the average gives $1/\pi$ (Level A: direct derivation).** The integral $\int_0^1 \arccos(u)\,du = 1$ is exact. The arc formula $\theta(d) = 2\arccos(d/2R)$ is forced by the intersection geometry of 2-spheres in $D = 3$. The discrete baseline of $1/3$ follows from $K = 4$ tetrahedral packing. The continuous result $1/\pi$ is the continuum extension of the discrete $K = 4$ packing fraction to the fluctuating-boundary limit adopted here.

**Why the fraction enters as an exponent (Level A: partition function applied at the tiling boundary).** The constitutive partition law — local, independent-channel, multiplicative in accumulation — is established on the Constitutive Law and Poisson pages. The coupled fraction at each tiling boundary is $\eta = 1/\pi$ (exact integral). The uncoupled fraction $(1 - 1/\pi)$ compounds across independent boundaries the same way $(1-\mu)$ compounds across radii in galaxies. The exponent $1 - 1/\pi$ is the surviving fraction per independent boundary traversal.

**Why $\mathcal{E} = 1/\mu$ corresponds to $\Omega_m/\Omega_b$ (Level B: observable correspondence).** The enhancement measures the ratio of total gravitational driving ($g_t$) to baryonic source driving ($g_s$). In $\Lambda$CDM, this ratio is parameterized as $\Omega_m/\Omega_b = 1 + \Omega_c/\Omega_b$, where the excess is attributed to cold dark matter. In GFD, the same ratio is $(x+1)/x = 1/\mu(x)$, where the excess is attributed to the TetB fraction $(1-\mu)$. The numerical correspondence is asserted only at the level of gross gravitational driving: in both descriptions, the relevant quantity is the ratio of total potential-well depth to baryon-sourced driving at recombination.

---

### Wall 3: Extensions

The following results are consequences of the scaling law derived above. They are not part of the core CMB derivation but provide independent cross-checks from different epochs and observables.

#### Extension 1 — Tully-Fisher velocity evolution

From the baryonic Tully-Fisher relation $v^4 = GMa_0$ and $a_0 \propto H^{1-1/\pi}$:

$$\frac{v(z)}{v(0)} = \left[\frac{H(z)}{H_0}\right]^{(1-1/\pi)/4 \,\approx\, 0.17}$$

This predicts $\sim$21% velocity enhancement at $z = 2$ and $\sim$36% at $z = 4$. Preliminary SINS survey observations at $z \approx 2$ report $\sim$27%, consistent within geometric measurement scatter. $\Lambda$CDM, in which dark matter halos rather than $a_0$ set rotation velocities, predicts no such systematic evolution.

#### Extension 2 — Hubble constant

The H₀ Prediction page derived:

$$H_0 = \frac{2\pi a_0}{c \cdot \sqrt{K/\pi}} \approx 70.2 \text{ km/s/Mpc}$$

where $\sqrt{K/\pi} = \sqrt{4/\pi} \approx 1.128$ involves the same $K$ and $\pi$ as the cosmological scaling exponent. This value is intermediate between early-universe determinations (Planck: $67.4 \pm 0.5$) and late-universe determinations (SH0ES: $73.0 \pm 1.0$), suggesting a possible geometric account of the Hubble tension within GFD.

#### Extension 3 — Field equation at recombination

At $x = 0.183$, the coupling polynomial evaluates to $f(0.183) = (21 \times 0.183 + 13)/(0.183 + 1) \approx 14.24$, placing the entire universe just above the TetB structural floor of 13 and far below the Field Origin at 17. The gravitational field at recombination is operating globally near minimum coupling configuration — the same regime that today exists only in the exterior of galaxy vortices, where the TetB fraction flattens rotation curves.

#### Extension 4 — The galactic-cosmological equivalence (Level A: algebra)

The CMB enhancement $\mathcal{E} = 1/\mu(x)$ is algebraically identical to the ratio between the Newtonian enclosed-mass inference and the GFD decoded mass at any radius in a galaxy. This identity follows directly from the definitions of the two mass relations.

The Newtonian enclosed mass is $M_N = rv^2/G$. The GFD decoded mass is $M_{\text{dec}} = rv^4/[G(a_0 r + v^2)]$. The ratio:

$$\frac{M_N}{M_{\text{dec}}} = \frac{rv^2/G}{rv^4/[G(a_0 r + v^2)]} = \frac{a_0 r + v^2}{v^2} = 1 + \frac{1}{x} = \frac{1}{\mu(x)}$$

This holds for any $v$ at any $r$, as it follows from the definitions of the two mass formulas.

Thus the same constitutive factor $1/\mu(x)$ appears in both settings: locally as the ratio between Newtonian and GFD mass inference in galaxies, and cosmologically as the recombination-era gravitational enhancement. In this sense, the CMB enhancement and the galactic mass discrepancy are two evaluations of the same constitutive identity at different acceleration states.

---

### What This Derivation Does and Does Not Establish

**Established:** The overall gravitational enhancement factor at recombination, derived from the constitutive law and the tiling-corrected scaling of $a_0$, is consistent with the Planck-inferred value at the quoted uncertainty level. The derivation uses zero free parameters beyond those fixed at galactic scales.

**Established:** The power-law form $a_0 \propto H^{1-1/\pi}$ follows from the partition function applied at the tiling boundary. The uncoupled fraction $(1 - 1/\pi)$ compounds across the lattice through the same mechanism that produces galactic rotation curve profiles. Within GFD, the compounding is the partition operating across independent tiling steps rather than an added fitted ingredient.

**Not established:** The full CMB power spectrum. A multipole-by-multipole fit would require implementing $\nabla \cdot [\mu(x)\nabla\Phi] = 4\pi G\rho$ in a Boltzmann solver with $a_0(z) \propto H^{1-1/\pi}$ as the time-dependent saturation scale.

**Future work:** A formal recasting of the partition function in the language of the renormalization group — identifying the one-loop structure, the renormalization scale, and the anomalous dimension $\gamma_{a_0} = 1/\pi$ within a Wilsonian effective action framework. This would provide a complementary derivation of the same result in standard QFT language.

**Validation artifact:** This derivation is mirrored by a runnable test in `tests/gravitation/test_cmb_enhancement.py`.

---

### References

Bekenstein, J. D. and Milgrom, M. (1984). Does the missing mass problem signal the breakdown of Newtonian gravity? Astrophys. J. 286, 7.

Gibbons, G. W. and Hawking, S. W. (1977). Cosmological event horizons, thermodynamics, and particle creation. Phys. Rev. D 15, 2738.

Planck Collaboration (2020). Planck 2018 results. VI. Cosmological parameters. Astron. Astrophys. 641, A6.

Riess, A. G. et al. (2022). A comprehensive measurement of the local value of the Hubble constant. Astrophys. J. Lett. 934, L7.
