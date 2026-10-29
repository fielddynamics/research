# Singularities, Information and Holography in Gravity Field Dynamics

### Four consequences of restoring the full affine connection

*Stephen Nelson · Field Dynamics Research · working note*

---

## Abstract

General relativity imposes the torsion-free condition $\Gamma^\lambda_{\mu\nu} = \Gamma^\lambda_{\nu\mu}$. This keeps 40 of the 64 components of the affine connection and discards 24. Gravity Field Dynamics (GFD) identifies the discarded components with the second root of the tetrad equation, the TetB sector. It restores them in full, with the constitutive law $\mu(x) = x/(x+1)$ dividing the field between the two sectors (Letter 3; [`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md)).

This note examines what the restored connection implies for four long-standing problems:

1. the singularity theorems;
2. the black-hole information paradox;
3. the non-renormalisability of perturbative quantum gravity;
4. the holographic principle.

It first locates black holes on the TetA/TetB partition. Their horizons sit at $x = g/a_0 \sim 10^{13}$–$10^{22}$, where the TetB share of the field is $10^{-14}$–$10^{-23}$. This explains why GFD agrees with general relativity at horizons to that precision. It also sets the terms on which the restored sector can matter there.

It then derives the Raychaudhuri equation for the full 64-component connection. The torsion term decomposes cleanly:
- the vector part couples only to expansion;
- the axial part only to vorticity;
- the tensor part to shear and vorticity.

Applied to GFD, the derivation shows that a torsion sector whose amplitude follows the TetB share of the acceleration is too weak to halt collapse, by 14 to 23 orders of magnitude. It identifies what would succeed: torsion sourced by the spin density of matter, as in Einstein–Cartan theory.

For each problem the note states the standard result, the exact GFD identity, and what remains to be shown. Every identity and numerical claim is checked by [`verify_identities.py`](verify_identities.py) (16 of 16 checks pass).

## Notation

| Symbol | Meaning |
|---|---|
| $x = g/a_0$ | acceleration in units of the scale $a_0 = 1.2 \times 10^{-10}$ m s⁻² |
| $\mu(x) = x/(x+1)$ | the TetA (retained) fraction of the field |
| $1 - \mu(x) = 1/(x+1)$ | the TetB (torsion-sector) fraction |
| $s(x) = (x-1)/(x+1)$ | the state coordinate of the coupling polynomial $f(K,s) = 1 + sK + K^2$ |
| $F(y) = y - 2\sqrt y + 2\ln(1+\sqrt y)$ | the kinetic functional of the covariant action, with $y = x^2$ and $dF/dy = \mu(\sqrt y)$ |
| $T^\lambda{}_{\mu\nu} = \Gamma^\lambda{}_{\mu\nu} - \Gamma^\lambda{}_{\nu\mu}$ | torsion, 24 components |
| $\theta, \sigma_{ab}, \omega_{ab}$ | expansion, shear and vorticity of a timelike congruence $u^a$ |

## 1. Where black holes sit on the partition

![The TetA/TetB partition near the transition, and the TetB share at the scales of galaxies, the Earth and black-hole horizons](regime_map.png)

The partition depends only on the local field strength $x = g/a_0$. The table places three black holes on it, using the surface gravity of the horizon, $\kappa = c^4/4GM$:

| Black hole | Horizon surface gravity | $x = \kappa/a_0$ | TetB share $1 - \mu$ |
|---|---|---|---|
| 10 $M_\odot$ | $1.5 \times 10^{12}$ m s⁻² | $1.3 \times 10^{22}$ | $8 \times 10^{-23}$ |
| Sgr A\* ($4.3 \times 10^6\,M_\odot$) | $3.5 \times 10^{6}$ m s⁻² | $2.9 \times 10^{16}$ | $3 \times 10^{-17}$ |
| M87\* ($6.5 \times 10^9\,M_\odot$) | $2.3 \times 10^{3}$ m s⁻² | $2.0 \times 10^{13}$ | $5 \times 10^{-14}$ |

Two consequences follow, and the rest of the note is built on them.

**Agreement with general relativity at horizons.** At every horizon the field is overwhelmingly TetA, and GFD reduces to general relativity to between 13 and 22 decimal places. This is why the framework is consistent with the horizon-scale images of the Event Horizon Telescope and with the ringdown of black-hole mergers observed by gravitational-wave detectors. The departures from general relativity that GFD predicts lie at the other end of the scale, in the outskirts of galaxies, where $x \lesssim 1$.

**The terms on which the restored sector can act.** Near and inside a black hole, the TetB *share* of the field is negligible. Any role for the restored torsion sector in the singularity or information problems must therefore come from something other than the share: from the sector's *structure* (its 24 components and their degrees of freedom), or from a source of torsion that grows with density. The next two sections make this precise.

## 2. Focusing with the full connection

### 2.1 The problem

The singularity theorems of Penrose (1965) and of Hawking and Penrose (1970) show that, under general energy conditions, gravitational collapse leads to geodesic incompleteness. Their engine is the focusing of geodesics, governed by the Raychaudhuri equation (Raychaudhuri 1955).

### 2.2 The Raychaudhuri equation for the full connection

**Conventions.** Let $\nabla$ be a metric-compatible connection with torsion: the full 64-component connection. Take $\nabla_a V^c = \partial_a V^c + \Gamma^c{}_{ad}V^d$ and $T^c{}_{ab} = \Gamma^c{}_{ab} - \Gamma^c{}_{ba}$. Then the commutator of covariant derivatives acquires a torsion term:

$$(\nabla_a\nabla_b - \nabla_b\nabla_a)\,u^c \;=\; R^c{}_{dab}\,u^d \;-\; T^d{}_{ab}\,\nabla_d u^c .$$

**The derivation.** Consider a congruence of timelike curves with unit tangent $u^a$, autoparallel with respect to $\nabla$ ($u^b \nabla_b u^a = 0$). Metric compatibility gives $u_a \nabla_b u^a = 0$, so the tensor $B^a{}_b = \nabla_b u^a$ is purely spatial. It decomposes as

$$B^a{}_b = \tfrac13\theta\, h^a{}_b + \sigma^a{}_b + \omega^a{}_b .$$

Contracting the commutator over $a = c$ and multiplying by $u^b$ gives

$$\boxed{\;\frac{d\theta}{d\tau} \;=\; -\tfrac13\theta^2 - \sigma_{ab}\sigma^{ab} + \omega_{ab}\omega^{ab} - R_{ab}\,u^a u^b \;+\; T^d{}_{ab}\,u^b\,\nabla_d u^a\;}$$

Here $R_{ab}$ is the Ricci tensor of the full connection, and the final term is the explicit torsion coupling. The structure agrees with the general form given by Luz and Vitagliano (2017), whose torsion is defined with a factor $\tfrac12$.

**The torsion term, decomposed.** The 24 torsion components separate into three irreducible parts:
- a vector part, the trace $T_b = T^a{}_{ab}$, with 4 components;
- an axial part, totally antisymmetric and dual to an axial vector $S^a$, with 4 components;
- a traceless tensor part, with 16 components.

Each couples to a different kinematic quantity:

| Torsion part | Components | Contribution to $d\theta/d\tau$ | Couples to |
|---|---|---|---|
| Vector | 4 | $\tfrac13 (T_b u^b)\,\theta$ | expansion only |
| Axial (totally antisymmetric) | 4 | $T_{[dab]}\, u^b\, \omega^{ad}$, proportional to $S_a \omega^a$ | vorticity only |
| Tensor | 16 | $q^d{}_{ab}\, u^b (\sigma^a{}_d + \omega^a{}_d)$ | shear and vorticity, not expansion |

The decomposition and each row are verified numerically over random torsion fields and kinematics ([`verify_identities.py`](verify_identities.py), checks B0–B4).

**Geodesics and autoparallels.** In theories with torsion, matter without intrinsic spin follows the geodesics of the metric, not the autoparallels of the full connection (Luz and Vitagliano 2017). For such matter the focusing equation keeps its standard form. Torsion then influences focusing only through the field equations, by changing the effective energy density in $R_{ab}u^a u^b$. Matter with spin couples to torsion directly.

### 2.3 Application to GFD

**The vorticity channel.** Only the vorticity term $+\omega_{ab}\omega^{ab}$ opposes focusing in the torsion-free theory, and the axial part of the torsion couples directly to it. The structure of the GFD torsion sector points to this channel. The staging draft of the full-connection letter (*Field Closure of General Relativity*, [`letter 4 staging/`](../../papers/letter-3-field-closure-of-tetrad-frame/letter%204%20staging/letter.tex)) shows two things:
- the 24 torsion components factor as $8 \times 3$, the eight null directions of the closed frame times three rotation planes;
- parallel transport around the frame has non-trivial holonomy once the TetA/TetB chirality is respected, which defines a preferred rotation axis.

An intrinsic axial preference is exactly the property that would couple the torsion sector to vorticity.

**The magnitude.** Suppose the torsion amplitude follows the TetB share of the acceleration. Then it is bounded by $g(1-\mu) \le a_0$, that is, $|T| \lesssim a_0/c^2 \approx 1.3 \times 10^{-27}$ m⁻¹. At a horizon of Schwarzschild radius $r_s$, the focusing term is of order $1/r_s^2$, while a torsion coupling of this size contributes of order $(a_0/c^2)/r_s$. The ratio is $10^{-14}$ to $10^{-23}$ for the black holes of §1, and it falls further inside, where $\theta$ and $R_{ab}u^au^b$ grow without bound. **A torsion sector whose amplitude is set by the acceleration share cannot halt collapse.**

**What would.** In Einstein–Cartan theory the decisive effect is not the linear kinematic coupling but a field-equation effect. Spin–torsion coupling contributes to the effective energy density a negative term quadratic in the spin density. For a fermion number density $n$ it is $-\alpha n^2$ with $\alpha = 9\kappa/16$ (Popławski 2012). Because it grows faster than the ordinary density, it overtakes gravitational attraction near the Cartan density and replaces the singularity with a bounce (Kopczyński 1972; Hehl et al. 1976; Popławski 2010, 2012).

For GFD the conclusion is therefore precise. Singularity resolution requires the torsion sector to be sourced by the spin density of matter at high density, not only by the acceleration share. GFD already ties its structure to spin: the face structure gives the intrinsic spin $\hbar/2$, and the torsion sector carries the parity distinction between the chambers. The task is to derive from the GFD action a spin–torsion source of this kind, and to show that its quadratic contribution dominates before a singularity forms.

## 3. The information paradox

**The problem.** Hawking (1975) showed that black holes radiate thermally. If the radiation is exactly thermal and the black hole evaporates completely, a pure initial state evolves into a mixed final state, which violates the unitarity of quantum mechanics (Hawking 1976). Any unitary account must reproduce the Page curve, in which the entropy of the radiation rises and then falls back to zero (Page 1993). Recent semiclassical calculations recover this curve through the "island" contribution to the entropy of the radiation (Penington 2020; Almheiri et al. 2020).

**The GFD identities.** The kinetic functional of the GFD action has three terms. Writing $u = \sqrt y$:

$$F(y) = \int 2u\,\mu(u)\, du = u^2 - 2u + 2\ln(1+u), \qquad 2\ln(1+u) = \int 2\,[1 - \mu(u)]\, du .$$

The logarithmic term comes entirely from the TetB fraction. It has the form of the Shannon–Hartley channel capacity, $C \propto \log(1 + S/N)$, with the field ratio $g/a_0$ in the role of the signal-to-noise ratio. The transition between sectors is a smooth rotation in $t = \ln x$:

$$s = \frac{x-1}{x+1} = \tanh\frac t2 .$$

**The proposed mechanism.** General relativity retains only the torsion-free sector, so it has no geometric degrees of freedom in which the structure of infalling matter could be recorded. GFD restores 24 such components. Their structure is rich: at $K = 4$ they carry the regular representation of $S_4$, which contains every irreducible representation of the tetrahedral symmetry group at full multiplicity (Paper B). The proposal is that the information carried by collapsing matter is transferred into this sector rather than destroyed.

**What §1 requires of the mechanism.** At a horizon the TetB share is $10^{-14}$–$10^{-23}$. The information therefore cannot reside in the share. It must reside in the configuration of the torsion degrees of freedom, or in a torsion amplitude sourced by spin, as in §2.3. To become a result, the mechanism needs three things:
1. a count of the torsion-sector states per unit area, compared with the Bekenstein–Hawking entropy $S = A/4\ell_P^2$. The GFD working notes read the 4 as $K$ ([`the-pixel-and-the-lattice.md`](../photonic/the-pixel-and-the-lattice.md));
2. an account of how the stored information is returned in the radiation;
3. a demonstration that the resulting entropy follows the Page curve.

## 4. Renormalisation and the running of the field

**The problem.** Perturbative quantum gravity is non-renormalisable. Pure gravity is finite at one loop ('t Hooft and Veltman 1974), but diverges at two loops (Goroff and Sagnotti 1986). Two responses are prominent: theories with additional structure, such as string theory, and the asymptotic-safety programme, which seeks a non-trivial ultraviolet fixed point of the gravitational renormalisation-group flow (Weinberg 1979; Reuter 1998).

**The GFD identity.** In $t = \ln(g/a_0)$, the constitutive law obeys the logistic equation

$$\frac{d\mu}{dt} = \mu(1-\mu) \equiv \beta(\mu).$$

This has the form of a renormalisation-group beta function with two fixed points:
- **$\mu = 1$ ($s = +1$):** critical exponent $\beta'(1) = -1$, approached at high acceleration, the regime of general relativity;
- **$\mu = 0$ ($s = -1$):** exponent $\beta'(0) = +1$, approached at low acceleration, the regime of galactic dynamics.

The running is fastest at the Field Origin, where $\beta(\tfrac12) = \tfrac14$.

**The interpretation.** General relativity corresponds to fixing the field at one fixed point, $\mu = 1$. GFD keeps the whole flow, and the gravitational interaction runs between its two fixed points with the acceleration scale. On this reading, the difficulties of quantising gravity about a single fixed background may reflect that truncation.

**What remains.** The flow and its exponents are exact, and the parallel with a renormalisation-group flow is formal. It does not yet bear on quantum divergences. That requires deriving the flow as the running of a coupling in a quantum treatment of the GFD action, and comparing its fixed points and exponents with those computed in asymptotic safety.

## 5. The holographic principle

**The problem.** The entropy of a black hole is proportional to its horizon area, not its volume (Bekenstein 1973; Hawking 1975). The holographic principle elevates this to a bound on the information content of any region ('t Hooft 1993; Susskind 1995).

**The GFD identity.** Interpreted in Newtonian terms, the extra mass needed to account for an observed acceleration $g$ at radius $r$ is

$$M_{\text{extra}}(r) = \frac{r^2}{G}\,[\,g - \mu g\,] = \frac{a_0\, r^2}{G}\,\mu(x).$$

This is the mass conventionally attributed to dark matter, written exactly: the acceleration scale times the area of the sphere, weighted by the TetA fraction.

**The interpretation.** In GFD the connection is read through faces: the field closes through the $K = 4$ faces of each tetrahedral chamber, and $4\pi = K\pi$ counts solid angle per face. On this reading, the area scaling of the "missing" mass and the area law of black-hole entropy share an origin: the field's content is evaluated on two-dimensional boundaries.

**What remains, and a test.** The $r^2$ scaling also follows from Gauss's law for an inverse-square field, so the scaling alone does not establish holography. The closest precedent is Verlinde (2017), who derives MOND-like galactic phenomenology from the entropy of de Sitter space. His apparent dark-matter mass follows a different relation from GFD's. Both have been, or can be, confronted with weak gravitational lensing around isolated galaxies (Brouwer et al. 2017, 2021), which gives the holography section a test that distinguishes GFD, MOND and emergent gravity.

## 6. Summary

| Problem | Exact GFD content | What the analysis shows | Required to complete |
|---|---|---|---|
| Regime | $1-\mu = 10^{-14}$–$10^{-23}$ at horizons | GFD matches GR at horizons; the share cannot act there | — |
| Singularities | Raychaudhuri equation for the full connection; torsion couples vector–expansion, axial–vorticity, tensor–shear/vorticity | torsion bounded by $a_0/c^2$ is too weak by $10^{14}$–$10^{23}$; spin-sourced torsion, as in Einstein–Cartan, is the viable route | derive a spin–torsion source from the GFD action and its quadratic term |
| Information | $2\ln(1+u) = \int 2(1-\mu)\,du$; $s = \tanh(t/2)$; 24 torsion components carrying the regular representation of $S_4$ | storage must be in the torsion configuration, not the share | state count against $A/4\ell_P^2$; return channel; Page curve |
| Renormalisation | $d\mu/d\ln x = \mu(1-\mu)$; exponents $\pm 1$ | a formal two-fixed-point flow | derive as the running of a quantum coupling |
| Holography | $M_{\text{extra}} = a_0 r^2 \mu/G$ | area scaling, with Gauss's law as the confound | the entropy area law from the face structure; the lensing test |

The four problems share a thread in this reading. Each arises in a theory that retains only the 40 torsion-free components of the connection, and each is addressed in GFD by the 24 components the torsion-free condition removes. The analysis above sharpens that claim. The restored sector is structurally the right one: it couples to vorticity and carries rich symmetry. It acts through its structure and its sources, not through its share of the field, which is negligible wherever gravity is strong.

## Verification

```bash
cd research/hawking
python verify_identities.py     # 16 checks: the four identities, the full-connection Raychaudhuri decomposition, the black-hole regime
```

---

## References

- Almheiri, A., Hartman, T., Maldacena, J., Shaghoulian, E. and Tajdini, A. (2020). Replica wormholes and the entropy of Hawking radiation. *JHEP* 05, 013.
- Bekenstein, J. D. (1973). Black holes and entropy. *Phys. Rev. D* 7, 2333.
- Brouwer, M. M. et al. (2017). First test of Verlinde's theory of emergent gravity using weak gravitational lensing measurements. *Mon. Not. R. Astron. Soc.* 466, 2547.
- Brouwer, M. M. et al. (2021). The weak lensing radial acceleration relation. *Astron. Astrophys.* 650, A113.
- Goroff, M. H. and Sagnotti, A. (1986). The ultraviolet behavior of Einstein gravity. *Nucl. Phys. B* 266, 709.
- Hawking, S. W. (1975). Particle creation by black holes. *Commun. Math. Phys.* 43, 199.
- Hawking, S. W. (1976). Breakdown of predictability in gravitational collapse. *Phys. Rev. D* 14, 2460.
- Hawking, S. W. and Penrose, R. (1970). The singularities of gravitational collapse and cosmology. *Proc. R. Soc. Lond. A* 314, 529.
- Hehl, F. W., von der Heyde, P., Kerlick, G. D. and Nester, J. M. (1976). General relativity with spin and torsion: foundations and prospects. *Rev. Mod. Phys.* 48, 393.
- Kopczyński, W. (1972). A non-singular universe with torsion. *Phys. Lett. A* 39, 219.
- Luz, P. and Vitagliano, V. (2017). Raychaudhuri equation in spacetimes with torsion. *Phys. Rev. D* 96, 024021. [arXiv:1709.07261](https://arxiv.org/abs/1709.07261).
- Page, D. N. (1993). Information in black hole radiation. *Phys. Rev. Lett.* 71, 3743.
- Pasmatsiou, K., Tsagas, C. G. and Barrow, J. D. (2017). Kinematics of Einstein–Cartan universes. *Phys. Rev. D* 95, 104007. [arXiv:1611.07878](https://arxiv.org/abs/1611.07878).
- Penington, G. (2020). Entanglement wedge reconstruction and the information paradox. *JHEP* 09, 002.
- Penrose, R. (1965). Gravitational collapse and space-time singularities. *Phys. Rev. Lett.* 14, 57.
- Popławski, N. J. (2010). Cosmology with torsion: an alternative to cosmic inflation. *Phys. Lett. B* 694, 181.
- Popławski, N. J. (2012). Nonsingular, big-bounce cosmology from spinor-torsion coupling. *Phys. Rev. D* 85, 107502. [arXiv:1111.4595](https://arxiv.org/abs/1111.4595).
- Raychaudhuri, A. K. (1955). Relativistic cosmology. I. *Phys. Rev.* 98, 1123.
- Reuter, M. (1998). Nonperturbative evolution equation for quantum gravity. *Phys. Rev. D* 57, 971.
- Shannon, C. E. (1949). Communication in the presence of noise. *Proc. IRE* 37, 10.
- Susskind, L. (1995). The world as a hologram. *J. Math. Phys.* 36, 6377.
- 't Hooft, G. (1993). Dimensional reduction in quantum gravity. [arXiv:gr-qc/9310026](https://arxiv.org/abs/gr-qc/9310026).
- 't Hooft, G. and Veltman, M. (1974). One-loop divergencies in the theory of gravitation. *Ann. Inst. Henri Poincaré A* 20, 69.
- Verlinde, E. (2017). Emergent gravity and the dark universe. *SciPost Phys.* 2, 016.
- Weinberg, S. (1979). Ultraviolet divergences in quantum theories of gravitation. In S. W. Hawking and W. Israel (eds.), *General Relativity: An Einstein Centenary Survey*. Cambridge University Press.

**GFD sources:**
- Letter 3 and [`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md): the 40/24 split and its restoration.
- [*Field Closure of General Relativity*, staging draft](../../papers/letter-3-field-closure-of-tetrad-frame/letter%204%20staging/letter.tex): the full 64-component connection; the $8 \times 3$ structure of the torsion sector and its chiral holonomy.
- Paper B, [`gfd_paper_b_torsion_S4.tex`](../../papers/algebraic-papers-a-b-c/gfd_paper_b_torsion_S4.tex): the torsion sector as the regular representation of $S_4$.
- The covariant action and kinetic functional: [`06-covariant-completion.md`](../../docs/02-gravitation/06-covariant-completion.md).
