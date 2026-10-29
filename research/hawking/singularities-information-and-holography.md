# Singularities, Information and Holography in Gravity Field Dynamics

### Four consequences of restoring the full affine connection

*Stephen Nelson · Field Dynamics Research · working note*

---

## Abstract

General relativity imposes the torsion-free condition $\Gamma^\lambda_{\mu\nu} = \Gamma^\lambda_{\nu\mu}$. This keeps 40 of the 64 components of the affine connection and discards 24. Gravity Field Dynamics (GFD) identifies the discarded components with the second root of the tetrad equation, the TetB sector. Restoring them, with the constitutive law $\mu(x) = x/(x+1)$ dividing the field between the two sectors, gives the full connection (Letter 3; [`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md)).

This note examines what the restored connection implies for four long-standing problems:

1. the singularity theorems;
2. the black-hole information paradox;
3. the non-renormalisability of perturbative quantum gravity;
4. the holographic principle.

In each case it states the standard problem, derives the relevant GFD identity, and sets out what the identity establishes and what remains to be shown. All four identities are exact consequences of the constitutive law and have been verified symbolically. Their physical interpretation, as a mechanism for each problem, is the programme's working hypothesis.

## Notation

| Symbol | Meaning |
|---|---|
| $x = g/a_0$ | acceleration in units of the scale $a_0 = 1.2 \times 10^{-10}$ m s⁻² |
| $\mu(x) = x/(x+1)$ | the TetA (retained) fraction of the field |
| $1 - \mu(x) = 1/(x+1)$ | the TetB (torsion-sector) fraction |
| $s(x) = (x-1)/(x+1)$ | the state coordinate of the coupling polynomial $f(K,s) = 1 + sK + K^2$ |
| $F(y) = y - 2\sqrt y + 2\ln(1+\sqrt y)$ | the kinetic functional of the covariant action, with $y = x^2$ and $dF/dy = \mu(\sqrt y)$ |

## 1. The singularity theorems

**The problem.** The singularity theorems of Penrose (1965) and of Hawking and Penrose (1970) show that, under general energy conditions, gravitational collapse leads to geodesic incompleteness. Their engine is the Raychaudhuri equation for a congruence of timelike geodesics:

$$\frac{d\theta}{d\tau} = -\tfrac13\theta^2 - \sigma_{ab}\sigma^{ab} + \omega_{ab}\omega^{ab} - R_{ab}u^a u^b .$$

For a congruence without vorticity ($\omega_{ab} = 0$) satisfying the strong energy condition, every term on the right is non-positive. The expansion $\theta$ then diverges to $-\infty$ in finite proper time. Only the vorticity term opposes focusing, and in the torsion-free theory, for hypersurface-orthogonal congruences, it vanishes.

**The GFD identity.** In GFD the torsion sector carries the share $1 - \mu$ of the field. The acceleration it carries is

$$g_{\text{TetB}} \;=\; g\,(1 - \mu) \;=\; \frac{a_0\, g}{g + a_0},$$

and in the limit of arbitrarily strong fields

$$\lim_{g \to \infty} g_{\text{TetB}} \;=\; a_0 .$$

The torsion-sector acceleration is bounded by $a_0$ at every field strength. In a collapsing configuration the TetA share grows without limit, but the TetB share saturates.

**What this establishes, and what remains.** The bound is exact. The proposed mechanism is that the restored torsion sector supplies the vorticity-like contribution that the torsion-free theory lacks, and that this halts focusing before a singularity forms. There is precedent for torsion acting this way: in Einstein–Cartan theory, spin–torsion coupling produces an effective repulsion at extreme densities that can replace a cosmological singularity with a bounce (Kopczyński 1972; Hehl et al. 1976; Popławski 2010). To complete the argument, GFD must:
- write the Raychaudhuri equation for the full 64-component connection;
- show that the TetB contribution enters with the opposing sign;
- show that a contribution bounded by $a_0$ is sufficient against a TetA term that grows without bound.

## 2. The information paradox

**The problem.** Hawking (1975) showed that black holes radiate thermally. If the radiation is exactly thermal and the black hole evaporates completely, a pure initial state evolves into a mixed final state, which violates the unitarity of quantum mechanics (Hawking 1976).

**The GFD identity.** The kinetic functional of the GFD action has three terms. Writing $u = \sqrt y$, its derivation is

$$F(y) = \int \mu(u)\, dy = \int 2u\,\mu(u)\, du = u^2 - 2u + 2\ln(1+u),$$

and the logarithmic term comes entirely from the TetB fraction:

$$2\ln(1+u) \;=\; \int 2\,[1 - \mu(u)]\, du .$$

This term has the form of the Shannon–Hartley channel capacity, $C \propto \log(1 + S/N)$, with the field ratio $u = g/a_0$ in the role of the signal-to-noise ratio. The transition between the sectors is a smooth rotation in the logarithmic acceleration $t = \ln x$:

$$s \;=\; \frac{x-1}{x+1} \;=\; \tanh\frac{t}{2}.$$

**The proposed mechanism.** General relativity keeps only the torsion-free sector and so has no degrees of freedom in which the structure of collapsing matter could be recorded geometrically. In GFD the 24 torsion components form such a sector. As collapse drives the state across the Field Origin ($s = 0$) along the $\tanh(t/2)$ rotation, the information carried by the infalling matter is transferred into the torsion sector rather than destroyed. The black hole then retains it as a structured state of the $K = 4$ geometry, and unitarity is preserved.

**What this establishes, and what remains.**
- **Exact:** the logarithmic term arises from the TetB fraction, and the sector transition is $\tanh(t/2)$.
- **A structural correspondence, not yet a derivation:** that this term measures an information capacity.

Making the mechanism precise requires:
- a microscopic count of the torsion-sector states, compared with the Bekenstein–Hawking entropy $S = A/4\ell_P^2$;
- an account of how the stored information is returned in the radiation.

The GFD working notes already read the factor 4 in $A/4$ as $K$ ([`the-pixel-and-the-lattice.md`](../photonic/the-pixel-and-the-lattice.md)).

## 3. Renormalisation and the running of the field

**The problem.** Perturbative quantum gravity is non-renormalisable. Pure gravity is finite at one loop ('t Hooft and Veltman 1974), but diverges at two loops (Goroff and Sagnotti 1986), and coupling it to matter introduces divergences already at one loop. Two responses are prominent: theories with additional structure, such as string theory, and the asymptotic-safety programme, which seeks a non-trivial ultraviolet fixed point of the gravitational renormalisation-group flow (Weinberg 1979; Reuter 1998).

**The GFD identity.** In the logarithmic variable $t = \ln(g/a_0)$, the constitutive law obeys the logistic equation

$$\frac{d\mu}{dt} \;=\; \mu\,(1 - \mu).$$

This has the form of a renormalisation-group beta function $\beta(\mu) = d\mu/d\ln(\text{scale})$, with two fixed points:
- **$\mu = 1$ ($s = +1$)**, approached at high acceleration: the regime of general relativity;
- **$\mu = 0$ ($s = -1$)**, approached at low acceleration: the regime of galactic dynamics.

The flow between them is smooth, and the Field Origin ($\mu = \tfrac12$) is the point of maximum running, where $\beta = \tfrac14$.

**The interpretation.** General relativity corresponds to fixing the field at one fixed point, $\mu = 1$. GFD keeps the whole flow, and the gravitational interaction "runs" between its two fixed points with the acceleration scale. On this reading, the difficulties of quantising gravity about a single fixed background may reflect that truncation.

**What this establishes, and what remains.** The logistic flow and its fixed points are exact, and the parallel with an RG flow is formal. It is not yet a statement about quantum divergences. To bear on renormalisability, the flow must be derived as the running of a coupling in a quantum treatment of the GFD action, and its relation to the fixed points sought in asymptotic safety must be established.

## 4. The holographic principle

**The problem.** The entropy of a black hole is proportional to its horizon area, not its volume (Bekenstein 1973; Hawking 1975). The holographic principle elevates this to a bound on the information content of any region ('t Hooft 1993; Susskind 1995). Standard physics accepts the area law but lacks a classical structural account of why three-dimensional regions are governed by two-dimensional boundaries.

**The GFD identity.** Interpreted in Newtonian terms, the extra mass needed to account for an observed acceleration $g$ at radius $r$ is

$$M_{\text{extra}}(r) \;=\; \frac{r^2}{G}\,[\,g - \mu(x)\,g\,] \;=\; \frac{a_0\, r^2}{G}\,\mu(x).$$

This is the mass conventionally attributed to dark matter, written exactly. It is the acceleration scale times the area of the sphere, weighted by the TetA fraction.

**The interpretation.** In GFD the connection is read through faces: the field closes through the $K = 4$ faces of each tetrahedral chamber, and the normalisation $4\pi = K\pi$ counts solid angle per face. On this reading, the area scaling of the "missing" mass and the area law of black-hole entropy share an origin: the field's content is evaluated on two-dimensional boundaries.

**What this establishes, and what remains.** The identity is exact. Its $r^2$ scaling, however, follows from Gauss's law for an inverse-square field, so the scaling alone does not establish holography. The link to the entropy area law has a notable precedent: Verlinde (2017) derives MOND-like galactic phenomenology, with $a_0$ related to the Hubble scale, from the entropy of de Sitter space. A full GFD account would derive the area law of black-hole entropy from the face structure of the connection, with the $K$ in $A/(K\ell_P^2)$ arising from the same count.

## 5. Summary

| Problem | GFD identity (exact) | Proposed mechanism | Required to complete |
|---|---|---|---|
| Singularities | $g(1-\mu) = a_0 g/(g+a_0) \to a_0$ | the bounded torsion sector halts geodesic focusing | the Raychaudhuri equation for the full connection |
| Information | $2\ln(1+u) = \int 2(1-\mu)\,du$; $s = \tanh(t/2)$ | information is stored in the 24 torsion components | a state count matching $A/4\ell_P^2$, and the return channel |
| Renormalisation | $d\mu/d\ln x = \mu(1-\mu)$ | gravity runs between two fixed points | the flow derived as the running of a quantum coupling |
| Holography | $M_{\text{extra}} = a_0 r^2 \mu/G$ | field content is evaluated on boundaries | the entropy area law derived from the face structure |

The four problems share a common thread in this reading. Each arises in a theory that retains only the torsion-free 40 components of the connection, and each is addressed, in GFD, by the 24 components that the torsion-free condition removes. The identities above are the exact algebraic content of that claim. The programme of work set out in the right-hand column is what would turn each into a result.

---

## References

- Bekenstein, J. D. (1973). Black holes and entropy. *Phys. Rev. D* 7, 2333.
- Goroff, M. H. and Sagnotti, A. (1986). The ultraviolet behavior of Einstein gravity. *Nucl. Phys. B* 266, 709.
- Hawking, S. W. (1975). Particle creation by black holes. *Commun. Math. Phys.* 43, 199.
- Hawking, S. W. (1976). Breakdown of predictability in gravitational collapse. *Phys. Rev. D* 14, 2460.
- Hawking, S. W. and Penrose, R. (1970). The singularities of gravitational collapse and cosmology. *Proc. R. Soc. Lond. A* 314, 529.
- Hehl, F. W., von der Heyde, P., Kerlick, G. D. and Nester, J. M. (1976). General relativity with spin and torsion: foundations and prospects. *Rev. Mod. Phys.* 48, 393.
- Kopczyński, W. (1972). A non-singular universe with torsion. *Phys. Lett. A* 39, 219.
- Penrose, R. (1965). Gravitational collapse and space-time singularities. *Phys. Rev. Lett.* 14, 57.
- Popławski, N. J. (2010). Cosmology with torsion: an alternative to cosmic inflation. *Phys. Lett. B* 694, 181.
- Raychaudhuri, A. K. (1955). Relativistic cosmology. I. *Phys. Rev.* 98, 1123.
- Reuter, M. (1998). Nonperturbative evolution equation for quantum gravity. *Phys. Rev. D* 57, 971.
- Shannon, C. E. (1949). Communication in the presence of noise. *Proc. IRE* 37, 10.
- Susskind, L. (1995). The world as a hologram. *J. Math. Phys.* 36, 6377.
- 't Hooft, G. (1993). Dimensional reduction in quantum gravity. [arXiv:gr-qc/9310026](https://arxiv.org/abs/gr-qc/9310026).
- 't Hooft, G. and Veltman, M. (1974). One-loop divergencies in the theory of gravitation. *Ann. Inst. Henri Poincaré A* 20, 69.
- Verlinde, E. (2017). Emergent gravity and the dark universe. *SciPost Phys.* 2, 016.
- Weinberg, S. (1979). Ultraviolet divergences in quantum theories of gravitation. In S. W. Hawking and W. Israel (eds.), *General Relativity: An Einstein Centenary Survey*. Cambridge University Press.

**GFD sources:** Letter 3 and [`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md) (the 40/24 split and its restoration); the covariant action and kinetic functional, [`docs/02-gravitation/06-covariant-completion.md`](../../docs/02-gravitation/06-covariant-completion.md); the constitutive law, [`docs/02-gravitation/03-constitutive-law-mu-x.md`](../../docs/02-gravitation/03-constitutive-law-mu-x.md).
