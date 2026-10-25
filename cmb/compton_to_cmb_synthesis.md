# From Compton Oscillation to CMB Enhancement

## A Technical Synthesis of the Gravitational Tiling Exponent

**Stephen Nelson — Gravity Field Dynamics**
**March 2026**

---

## 1. What This Document Derives

The cosmic microwave background encodes the gravitational physics of the universe at redshift $z = 1100$. Planck 2018 measured that the gravitational potential wells shaping the acoustic oscillations were $6.36 \pm 0.10$ times deeper than baryonic matter alone could produce. Standard cosmology explains this factor with cold dark matter. This document derives it from the coupling topology of the stellated octahedron, with zero free parameters.

The derivation has three layers. The first layer is the constitutive law $\mu(x) = x/(x+1)$, which determines how the gravitational field responds at any acceleration. The second layer is the boundary coupling integral, which computes the fraction $1/\pi$ of each field boundary that participates in neighbor coupling. The third layer is the connection between the microscopic closure oscillation and the macroscopic cosmological scaling — the bridge that turns $1/\pi$ per breath into $a_0 \propto H^{1-1/\pi}$ across cosmic time.

The third layer is the one that has been hardest to pin down. This document shows that it follows from the same structural logic that produces $G = (17/13)\alpha^{21}\hbar c/m_e^2$: topology dictates the coupling structure, and independent traversals through that structure multiply.

---

## 2. The Target

At the level of gross gravitational driving of the acoustic peaks, the enhancement at recombination corresponds to the quantity $\Omega_m/\Omega_b$ in $\Lambda$CDM. In GFD, this enhancement is the inverse of the constitutive law evaluated at the recombination-epoch acceleration ratio:

$$\mathcal{E}_{\text{CMB}} = \frac{1}{\mu(x_{\text{rec}})} = \frac{x_{\text{rec}} + 1}{x_{\text{rec}}}$$

The observational target is $6.36 \pm 0.10$ (Planck 2018). The GFD prediction is 6.46, lying at the upper edge of the quoted interval.

To compute this, we need $x_{\text{rec}}$, the dimensionless acceleration ratio at recombination. That ratio depends on the saturation scale $a_0(z)$, which depends on how $a_0$ evolves with the Hubble rate. The central question of the derivation is: what is the scaling law $a_0(H)$?

---

## 3. The Constitutive Law

The coupling polynomial of the stellated octahedron is

$$f(K,s) = 1 + sK + K^2$$

where $K = 4$ is the tetrahedral face count and $s \in [-1, +1]$ is the state parameter. It evaluates to 13 in TetB ($s = -1$), 17 at the Field Origin ($s = 0$), and 21 in TetA ($s = +1$). The range is $21 - 13 = 8 = 2K$.

The constitutive law $\mu(x) = x/(x+1)$ is the continuous Möbius normalization of this polynomial. It maps the dimensionless acceleration ratio $x = g_t/a_0$ to the fraction of the gravitational field operating in the TetA (Newtonian) mode. In the strong-field limit ($x \gg 1$), $\mu \to 1$ and gravity is Newtonian. In the deep-field limit ($x \ll 1$), $\mu \to x$ and gravity is enhanced by factor $1/\mu = 1/x$.

At galactic scales, this law reproduces rotation curves and the baryonic Tully-Fisher relation with zero free parameters. At cosmological scales, it produces the CMB enhancement — provided $a_0$ evolves correctly with epoch.

---

## 4. The Saturation Scale Evolves

The saturation scale $a_0$ is identified with the Gibbons-Hawking acceleration of the cosmological horizon. The horizon at radius $r_H = c/H$ radiates at the Gibbons-Hawking temperature. The Unruh effect relates temperature to acceleration. Equating the two gives:

$$a_0 = \frac{cH}{2\pi}$$

Since $H$ evolves with epoch via the Friedmann equation, $a_0$ is not a constant. At tree level (no tiling correction), $a_0$ scales linearly with $H$.

---

## 5. The Naive Calculation and Why It Fails

At recombination ($z = 1100$), the perturbation-scale accelerations satisfy $g_t \ll a_0$, placing the entire universe in the deep-field limit. The scalar-tensor transition reduces to $g_t = \sqrt{g_s \cdot a_0}$, giving $x = \sqrt{g_s/a_0}$.

With naive linear scaling $a_0 \propto H$, the dimensionless ratio evaluates to $x \approx 0.037$. The enhancement is

$$\mathcal{E} = \frac{1.037}{0.037} \approx 28$$

The target is 6.4. The naive calculation overshoots by a factor of 4.3. The constitutive law is non-negotiable (it is derived from the polynomial). The deep-field approximation is accurate to 4% at this $x$. The gap therefore resides in the scaling law $a_0 \propto H$. Something modifies the linear relationship between $a_0$ and $H$ at cosmological densities.

---

## 6. The Boundary Coupling Integral

At galactic scales, gravitational fields are isolated. Each field samples the horizon temperature independently, and $a_0 = cH/(2\pi)$ holds without correction. At recombination, every region of space is gravitationally active. Fields are densely packed with overlapping boundaries. The question is: what fraction of each field's boundary actually participates in coupling to its neighbors?

Two adjacent gravitational fields of radius $R$ in $D = 3$ dimensions have 2-sphere closure boundaries. At center-to-center separation $d$, the coupling arc subtends $\theta(d) = 2\arccos(d/2R)$. This formula is specific to the intersection geometry of spheres in $D = 3$ and would not hold in $D = 2$ or $D = 4$.

In the discrete $K = 4$ tetrahedral packing at $d = R$, the coupling fraction is $\theta/(2\pi) = 1/3$. But GFD is a continuous field theory. At recombination, field separations sample the full range $d \in [0, 2R]$. In the absence of any additional shape parameter, the uniform distribution is the unique parameter-free choice. The average coupling fraction is

$$\frac{\langle\theta\rangle}{2\pi} = \frac{1}{2\pi} \cdot \frac{1}{2R}\int_0^{2R} 2\arccos\left(\frac{d}{2R}\right) dd$$

Substituting $u = d/(2R)$ and integrating by parts: $\int_0^1 \arccos(u)\,du = 1$. Therefore $\langle\theta\rangle = 2$, and

$$\frac{\langle\theta\rangle}{2\pi} = \frac{1}{\pi}$$

This is exact. It is the mean fraction of each field boundary that is effectively neighbor-coupled in the continuous dense-packing limit — the geometric efficiency of the $K = 4$ tiling when field boundaries fluctuate across all accessible separations.

---

## 7. From Fraction to Exponent — The Central Question

The boundary integral gives $\eta = 1/\pi$. The question that has been hardest to settle is: how does this fraction enter the scaling law? Does it modify $a_0$ as a prefactor ($a_0 \propto H/\pi$), or as an exponent ($a_0 \propto H^{1-1/\pi}$)?

A prefactor would mean: the boundary coupling attenuates $a_0$ once, by a fixed fraction, at one boundary. An exponent would mean: the boundary coupling attenuates $a_0$ cumulatively across the lattice, compounding at each step. The data strongly prefer the exponent ($\mathcal{E} = 6.46$) over the prefactor ($\mathcal{E}$ would be far from 6.4). But the question is whether the exponent is derived or merely fitted.

The answer is that it is derived, from the same structural logic that produces the gravitational constant. To see this requires understanding the microscopic mechanism — field closure — and its parallel in the $G$ derivation.

---

## 8. The Precedent: How $G$ Gets Its Exponent

The Gravitational Constant page derives

$$G = \frac{17}{13} \cdot \alpha^{21} \cdot \frac{\hbar c}{m_e^2}$$

The exponent 21 is the full coupling depth of the stellated octahedron: $f(K, +1) = 1 + 4 + 16 = 21$. At each of the 21 coupling levels, the interaction attenuates by the fine structure constant $\alpha \approx 1/137$. The product of 21 independent attenuations is $\alpha^{21} \approx 10^{-45}$, which is why gravity is weak.

The logic is:
- The topology dictates 21 coupling levels (from the polynomial)
- Each level independently attenuates by $\alpha$ (from the topology's own scale ratio)
- Independent attenuations multiply: $\alpha \times \alpha \times \cdots = \alpha^{21}$
- The product enters as an exponent, not a prefactor

Nobody asks "prove from the action that the attenuation is multiplicative across coupling levels." The topology dictates the structure. Each level is one step deeper into the stellated octahedron. Independent steps through a geometric structure multiply. This is what topology does.

The agreement is 0.12% at tree level, improving to 0.001% with the Schwinger one-loop QED correction $\alpha/(2\pi)$.

---

## 9. The Microscopic Mechanism: Field Closure at the Compton Frequency

The closure vortex analysis shows that the coupling polynomial oscillates as a sawtooth wave — $f: 13 \to 21 \to$ reset — at the Compton frequency $\omega_C = m_e c^2/\hbar$. Each cycle is one complete breath of the field: the stellated octahedron reads all 64 hexagram state transitions, the constitutive law sweeps from $\mu = 0$ to $\mu = 1$, and the vortex expands from core ($f = 13$) to horizon ($f = 21$) before collapsing back.

This oscillation is the microscopic clock of the gravitational field. It is not a metaphor. The coupling channel analysis confirms it computationally: the hexagram walk completes in 333 base-8 digits of $\pi$, resets, completes again in 303 digits, resets again in 250 digits, and continues indefinitely.

At each breath, the tile's boundary interfaces with its neighbors. The fraction of the boundary that participates in this coupling is $\eta = 1/\pi$, computed exactly from the overlap integral. The remaining fraction $1 - 1/\pi$ faces outward, carrying no coupling information.

---

## 10. The Bridge: Compton Oscillation Integrates to Hubble Scaling

The microscopic picture is the sawtooth chart: $f$ oscillating $13 \to 21$ at frequency $\omega_C$, with $\eta = 1/\pi$ of the boundary transmitting at each cycle. The macroscopic picture is the CMB scaling law: $a_0 \propto H^{1-1/\pi}$. This section shows they are the same object at different scales.

### 10.1 The counting

In one Hubble time $1/H$, there are $N = \omega_C/H$ individual closure cycles. At $z = 0$, this is approximately $3.6 \times 10^{38}$ breaths. At $z = 1100$, it is approximately $1.5 \times 10^{34}$ breaths. Each one is individually negligible — the attenuation per cycle is of order $10^{-39}$.

### 10.2 The compounding

Each breath independently exposes $\eta = 1/\pi$ of the boundary to neighbor coupling. Independent attenuations multiply. Over $N$ breaths in one e-fold of expansion ($d\ln H = 1$), the cumulative attenuation to the scalar sector coupling $g_s = a_0^2/(8\pi G)$ is

$$\left(1 - \frac{2\eta}{N}\right)^N \longrightarrow e^{-2\eta} = e^{-2/\pi} \quad \text{as } N \to \infty$$

The convergence is excellent: at $N = 10^4$, the match to $e^{-2/\pi}$ is already $2 \times 10^{-5}$. At $N = 10^{38}$ (the physical value), the match is at machine epsilon.

### 10.3 The beta function

The cumulative correction per logarithmic step defines the beta function:

$$\beta = \frac{d\ln g_s}{d\ln H} = 2 - 2\eta = 2\left(1 - \frac{1}{\pi}\right)$$

The tree-level contribution is $+2$ (from $a_0 \propto H$ at tree level, so $g_s = a_0^2 \propto H^2$). The boundary correction is $-2\eta$ (the cumulative attenuation from $N$ closure cycles per e-fold). Since $g_s \propto a_0^2$, taking the square root gives:

$$a_0 \propto H^{(2-2/\pi)/2} = H^{1-1/\pi}$$

### 10.4 The identity

The suppression factor at any redshift is

$$S = e^{-\eta \cdot \ln(H/H_0)} = \left(\frac{H_0}{H}\right)^{1/\pi}$$

These are the same expression. The left side is the integral of $\omega_C/H$ infinitesimal attenuations over $\ln(H/H_0)$ e-folds. The right side is the power law on the CMB derivation page. They match at $10^{-16}$ precision because they are algebraically identical: $e^{-\eta \ln x} = x^{-\eta}$ for any $x$ and any $\eta$.

The closure walk chart shows the integrand. The CMB scaling law is the integral.

---

## 11. Why This Has the Same Status as $G$

The $G$ derivation and the CMB derivation share identical logical structure:

| Element | $G$ derivation | CMB derivation |
|:---|:---|:---|
| **Topology** | Stellated octahedron | Stellated octahedron |
| **Coupling structure** | 21 coupling levels | $\omega_C/H$ closure breaths per e-fold |
| **Per-step attenuation** | $\alpha$ (topology's scale ratio) | $\eta = 1/\pi$ (boundary overlap fraction) |
| **Compounding** | $\alpha^{21}$ (independent levels multiply) | $(1-2\eta/N)^N \to e^{-2\eta}$ (independent breaths multiply) |
| **Result** | $G = (17/13)\alpha^{21}\hbar c/m_e^2$ | $a_0 \propto H^{1-1/\pi}$ |
| **Agreement** | 0.12% tree, 0.001% one-loop | Within Planck $\pm 0.10$ |

In both cases:
- The topology dictates the coupling structure (the polynomial tells you the depth; the boundary integral tells you the efficiency).
- Each step through the structure is independent.
- Independent attenuations multiply.
- The product enters as a power.

If $\alpha^{21}$ is "derived from the topology" — and it is, giving $G$ to extraordinary precision — then $e^{-\eta \ln(H/H_0)} = (H_0/H)^{1/\pi}$ is derived from the topology on the same grounds. The standard of proof is the same. The structural logic is the same. The difference is only what is being counted: coupling levels in one case, closure breaths in the other.

---

## 12. The Corrected Result

With $a_0 \propto H^{1-1/\pi}$, the suppression factor at $z = 1100$ is

$$S = \left(\frac{1}{23{,}600}\right)^{1/\pi} = 0.041$$

The corrected saturation scale is $a_0(z_{\text{rec}}) = S \cdot a_0^{\text{naive}} = 1.05 \times 10^{-7}$ m/s². Since $x = \sqrt{g_s/a_0}$, the corrected acceleration ratio is

$$x_{\text{rec}} = \frac{x_{\text{naive}}}{\sqrt{S}} = \frac{0.037}{0.202} = 0.183$$

The enhancement:

$$\mathcal{E}_{\text{CMB}} = \frac{1.183}{0.183} = 6.46$$

The progression from naive to corrected:

$$\text{Naive: } 28 \qquad \text{Discrete: } 6.05 \qquad \text{Continuous: } 6.46 \qquad \text{Planck: } 6.36 \pm 0.10$$

The prediction lies at the upper edge of the quoted Planck interval, within 1.6% of the central value.

---

## 13. What $\Lambda$CDM Calls Dark Matter Is $1/\mu(x)$

There is a result that connects the CMB enhancement to every galaxy ever measured, and it requires only a pencil.

$\Lambda$CDM computes enclosed mass as $M_{\text{CDM}} = rv^2/G$ (Newtonian, $\mu = 1$). GFD decodes mass as $M_{\text{dec}} = rv^4/[G(a_0 r + v^2)]$ (constitutive law applied). The ratio:

$$\frac{M_{\text{CDM}}}{M_{\text{dec}}} = \frac{a_0 r + v^2}{v^2} = 1 + \frac{1}{x} = \frac{1}{\mu(x)}$$

This is algebra, not data. It holds for any $v$ at any $r$, before any galaxy is observed, because it follows from the definitions of the two mass formulas. CDM uses $\mu = 1$. GFD uses $\mu = x/(x+1)$. The ratio between their mass estimates is always, everywhere, algebraically, $1/\mu(x)$.

At the CMB, the same ratio evaluated globally gives $1/\mu(0.183) = 6.46$. The "dark matter" in the early universe and the "dark matter" in late-universe galaxies are not two phenomena linked by structure formation. They are the same algebraic identity — $1/\mu(x)$ — evaluated at different acceleration states.

$\Lambda$CDM requires billions of years of N-body simulations to connect the cosmic dark matter density at $z = 1100$ to the dark matter halos of galaxies at $z = 0$. GFD connects them with one line of algebra.

---

## 14. What the Two Charts Show

The coupling channel analysis chart shows the sawtooth oscillation $f: 13 \to 21 \to$ reset. Each cycle is one Compton breath. Cycle 0 takes 333 digits. Cycle 1 takes 303. Cycle 2 takes 250. The cycles shorten because the later orbits are smaller — fewer new hexagrams remain to find. The vortex breathes indefinitely; $\pi$ has infinite digits.

The Compton-to-Hubble chart shows the same oscillation with its macroscopic envelope superimposed. The sawtooth still reaches from 13 up to its local ceiling in each cycle. But that ceiling — the effective maximum of $f$ — drops as $(H_0/H)^{1/\pi}$ over cosmological time. At $z = 0$, the ceiling is 21 (full capacity). At $z = 1100$, the ceiling has dropped to approximately 13.3. The universe at recombination is operating just above the TetB floor.

The charts are the same object at different zoom levels. The first is the integrand. The second is the integral.

---

## 15. The Screening Equation Across Scales

The screening identity $x(1 - \mu) = \mu$ can be rearranged to

$$\frac{\mu}{1-\mu} = x$$

The TetA fraction $\mu$ maps to ordinary baryonic matter. The TetB fraction $(1-\mu)$ maps to what $\Lambda$CDM calls dark matter. The ratio $\Omega_b/\Omega_c$ in the standard parameterization therefore corresponds to $x$.

At recombination, $x = 0.183$. From Planck 2018, $\Omega_b h^2/\Omega_c h^2 = 0.0224/0.1200 = 0.187$. Agreement within 2%.

If this correspondence holds, $\Lambda$CDM's six free parameters reduce by one: $\Omega_c h^2$ is not independent of $\Omega_b h^2$ but is locked to it by the screening equation. The ratio of ordinary matter to "dark matter" is the acceleration ratio $x$, computed from the constitutive law with zero free parameters.

---

## 16. The Möbius State Map at Recombination

The Möbius map $s(x) = (x-1)/(x+1)$ places the recombination epoch in the stellated octahedron's state space:

| Quantity | $x$ | $s(x)$ | $f(x)$ | Regime |
|:---|:---:|:---:|:---:|:---|
| TetB floor | $0$ | $-1$ | $13$ | Deep-field ceiling |
| Naive CMB | $0.037$ | $-0.929$ | $13.28$ | Pinned to floor |
| **Corrected CMB** | **$0.183$** | **$-0.690$** | **$14.24$** | Interior TetB |
| Field Origin | $1$ | $0$ | $17$ | 50/50 partition |
| CMB complement | $5.46$ | $+0.690$ | $19.76$ | Interior TetA |
| TetA ceiling | $\infty$ | $+1$ | $21$ | Full Newtonian |

The complement symmetry $\mu(x) + \mu(1/x) = 1$ means the CMB state at $s = -0.690$ has an exact mirror at $s = +0.690$. The TetB fraction driving the CMB enhancement (84.5%) is identically the TetA fraction of a system at the reciprocal acceleration $x = 5.46$ — the strong-field interior of a galactic vortex. The early universe and a galaxy's Newtonian core are topological duals.

And the enhancement itself: $\mathcal{E} = 1 + 1/x = 1 + 5.46 = 6.46$. The enhancement IS one plus the complement point.

---

## 17. The Complete Derivation Chain

$$\boxed{\begin{aligned}
&\textbf{Topology:} \quad K = 4, \; D = 3, \; f(K,s) = 1 + sK + K^2 \\[4pt]
&\textbf{Constitutive law:} \quad \mu(x) = x/(x+1) \\[4pt]
&\textbf{Horizon identification:} \quad a_0 = cH/(2\pi) \quad \text{(tree level)} \\[4pt]
&\textbf{Boundary integral:} \quad \eta = \langle\theta\rangle/(2\pi) = 1/\pi \quad \text{(exact)} \\[4pt]
&\textbf{Compton clock:} \quad \omega_C/H \text{ breaths per e-fold, each at } \eta \\[4pt]
&\textbf{Compounding:} \quad (1-2\eta/N)^N \to e^{-2\eta} \quad \text{(independent breaths multiply)} \\[4pt]
&\textbf{Beta function:} \quad \beta = 2 - 2/\pi \\[4pt]
&\textbf{Scaling law:} \quad a_0 \propto H^{1-1/\pi} \\[4pt]
&\textbf{At } z = 1100: \quad x = 0.183, \quad \mathcal{E} = 6.46 \\[4pt]
&\textbf{Planck target:} \quad \Omega_m/\Omega_b = 6.36 \pm 0.10
\end{aligned}}$$

---

## 18. What This Establishes

The CMB gravitational enhancement is the constitutive law $\mu(x) = x/(x+1)$ evaluated at the recombination-epoch acceleration state, with the saturation scale corrected for cosmological tiling.

The correction $a_0 \propto H^{1-1/\pi}$ follows from three ingredients, all derived:

1. The boundary coupling fraction $\eta = 1/\pi$ (exact integral from the overlap geometry of 2-spheres in $D = 3$).

2. The Compton-frequency closure oscillation (the stellated octahedron reading its own faces, producing the sawtooth $f: 13 \to 21 \to$ reset at $\omega_C = m_e c^2/\hbar$).

3. Multiplicative compounding of independent attenuations (the same structural logic that gives $G = (17/13)\alpha^{21}\hbar c/m_e^2$: each independent step through the topology costs a factor, and factors multiply).

No free parameters are adjusted. The constitutive law, the boundary integral, the Compton frequency, and the compounding rule all follow from $K = 4$ and $D = 3$, which are themselves fixed by the uniqueness equation $2(D+1) = 2^D$.

The CMB result is not a separate fit layered onto the galactic framework. It is the same constitutive law, the same TetB fraction, and the same topology, evaluated at a denser epoch where the horizon-controlled saturation scale is modified by continuous gravitational tiling.

---

## References

Bekenstein, J. D. and Milgrom, M. (1984). Does the missing mass problem signal the breakdown of Newtonian gravity? *Astrophys. J.* 286, 7.

Gibbons, G. W. and Hawking, S. W. (1977). Cosmological event horizons, thermodynamics, and particle creation. *Phys. Rev. D* 15, 2738.

Planck Collaboration (2020). Planck 2018 results. VI. Cosmological parameters. *Astron. Astrophys.* 641, A6.

Riess, A. G. et al. (2022). A comprehensive measurement of the local value of the Hubble constant. *Astrophys. J. Lett.* 934, L7.

---

*Copyright © 2025–2026 Stephen Nelson. Documentation: CC BY 4.0. Code: MIT.*
