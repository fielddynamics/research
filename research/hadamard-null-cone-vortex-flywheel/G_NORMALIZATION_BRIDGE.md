# One gravitational normalization: topology to microscopic response

*GFD Standard Field Model — normalization reconciliation. [T] algebra; [D] conditional upstream expression; [E] microscopic matching.*

## 1. Inherited result

The upstream [G from Topology](https://github.com/fielddynamics/research/tree/main/research/g_from_topology) and [GFD conventions](https://github.com/fielddynamics/research/blob/main/llms.txt) specify

$$G^{(0)}_{\rm GFD}=\frac{17}{13}\alpha_{\rm EM}^{21}\frac{\hbar c}{m_e^2},\qquad G^{(1)}_{\rm GFD}=G^{(0)}_{\rm GFD}(1+\alpha_{\rm EM}/(2\pi)).$$

The graded capacities 21, 17, 13 and determinant identity are exact algebra; the physical attenuation of one factor of alpha per level and the choice of exponent and ratio are premises, with the combination rule identified as proposed upstream. The loop factor is also proposed. The SFM does not replace these premises with adjustable independent G. Numerical agreement is not independent proof of the premises.

## 2. Response matching

The [spectral model](SPECTRAL_GRAVITY_READ.md) gives an isotropic dimensionless band curvature D and a polar intensity-gradient read. Its optional work functional, with dimensionless envelope f, gives $G_{\rm eff}=\eta^2f_0^2/(2\pi K)$ in the weak-source limit. The [static field read](FIELD_ORIGIN_GRAVITY_READ.md) inherits G from the upstream expression. It does not derive that expression again.

Use the electron reduced Compton length $\ell_e=\hbar/(m_ec)$ as a reference unit, **not** an assertion about the physical cell radius. Define dimensionless $u=\eta/c^2$ and $k=K/(m_ec^2/\ell_e)$. Then exactly

$$\frac{G_{\rm eff}m_e^2}{\hbar c}=\frac{u^2 f_0^2}{2\pi k}.$$

The required tree-level matching condition is

$$\boxed{\frac{u^2 f_0^2}{2\pi k}=\frac{17}{13}\alpha_{\rm EM}^{21}.}$$

At one loop the right side carries the upstream correction. This is a dimensionless consistency condition, not a microscopic derivation. For example setting $u f_0=\sqrt{2\pi k(17/13)}\alpha_{\rm EM}^{21/2}$ enforces the tree-level target by construction and is not a prediction. A rescaling $f\mapsto t f$, $K\mapsto K/t^2$, $\eta\mapsto\eta/t^2$ for nonzero real $t$ leaves the combination invariant: the separate coefficients cannot be identified by matching G alone.

## 3. Microscopic proof gates

- Derive the physically normalized stiffness K from the actual circulating lattice, including its physical spacing, energy scale and state density, not just its dimensionless curvature D. Full and filtered kernels currently give different D.
- Derive universal source and test coupling eta and scalar reference f0 from the same microscopic energy and the [matter configuration](MATTER_VORTEX_CHARGE.md). Retained TetB content and signed charge are distinct from positive mass-energy.
- Show why the response invariant carries 21 powers of alpha and the 17/13 ratio. Neither a determinant identity nor the optical mode count alone establishes this transfer law. Since the illustrative universal coupling enters twice, the exponent cannot simply be assigned independently to both source and test coupling.
- Derive the proposed loop factor separately. Show the correct drainless Newton/GR and drained constitutive-law limits; the optional nonlinear intensity-work toy is not the GFD nonlinear law.

**Acceptance criterion:** compute the dimensionless invariant from the microscopic model without choosing parameters from G, compare with the upstream expression at the corresponding perturbative order, and establish universal source/test normalization. Until then the SFM recovers a conditional inverse-square form, not an independent prediction of G. Every Field Object still closes; the normalization update changes neither closure ownership nor the SST action.

Return to [master README](README.md).

## Collective optical closure follow-up

See [G from a collective optical closure](G_CLOSURE_DERIVATION.md) for the conditional electromagnetic-reference normalization, primitive-volume stiffness derivation and the unresolved source-selection and stiffness assignments. This does not introduce another G.


**Continuation:** [Dynamic tetrad settlement](DYNAMIC_TETRAD_SETTLEMENT.md) tests this construction against the unchanged microscopic Hamiltonian, including central-first excitation, filtered observability, static slip and the remaining relativistic constraints.

**Continuation:** [Electron closure settlement](ELECTRON_CLOSURE_SETTLEMENT.md) connects Papers IV/V and the existing topology normalization with a joint solution, conditional radial energy and optical matching.
