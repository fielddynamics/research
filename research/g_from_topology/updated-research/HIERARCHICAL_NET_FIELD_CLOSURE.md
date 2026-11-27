# Hierarchical NET Field closure: local settlement without double accounting

*Field Origin vertex research · November 2026 · conditional static algebra, not Proof 26*

## 1. The corrected research question

A solar system's NET Field includes both TetA and TetB already settled within its own closure. The galactic NET Field includes that registered object, without reopening its internal accounting. The local observed dynamics are not a claim that the Sun has no TetB, nor that the galaxy's gravity ceases to exist inside it. A common host acceleration affects the whole object; tidal and relative clock effects survive. The clock domain is a candidate for the scope of ownership, not a literal shielding membrane. This supersedes the interpretation that drainlessness means a microscopically inactive TetB. Earlier candidate laws remain as historical tests, not alternate established physical claims.

The upstream [mountain-scale proof](https://github.com/fielddynamics/research/tree/aad94e0e1ec766e9bf8615d8fbcf07126cbd2f95/proofs/sst-mountain-scale) already proves telescoping of source sweeping (balayage), and the [net-field rule](https://github.com/fielddynamics/research/tree/aad94e0e1ec766e9bf8615d8fbcf07126cbd2f95/proofs/net-field-rule) explicitly distinguishes the host response to the pointer from the object's bare Newtonian residual. The earlier [clock-registration study](CLOCK_REGISTRATION_AND_NESTED_RESPONSE.md) established the harmonic trace split and a boundary-only no-go for bulk nonlinear response. Here we extend those identities to variational closure and fixed nested ownership projections. We do not assume that the microscopic vortex action implements them.

![Nested closure and the external-field leakage test](figures/hierarchical_closure.png)

[Interactive explorer](interactive/hierarchy.html).

## 2. A mathematically correct closure operator [T]

In a fixed finite graph discretization of the static clock/potential field, ground the exterior reference and let K be the symmetric positive-definite stiffness (e.g. a grounded graph Laplacian). Let V be the subspace of variations supported strictly within a child; E embeds its coordinates. Define the energy projector

$$P_V=E(E^TKE)^{-1}E^TK,\qquad Q_V=I-P_V.$$

Then $P_V^2=P_V$, $P_V^TK=KP_V$, $Q_V^2=Q_V$, and $P_V^TKQ_V=0$. Thus $\phi=w+h$, with $w=P_V\phi$ a zero-boundary interior residual and $h=Q_V\phi$ a discrete harmonic lift inside the child. The continuum analogue uses the Dirichlet inner product $\int\nabla u\cdot\nabla v$ on a bounded grounded domain, and closed zero-trace subspaces. For two nested interiors $V_c\subset V_p$, orthogonal projection gives

$$P_cP_p=P_pP_c=P_c,$$
$$Q_pQ_c=Q_cQ_p=Q_p.$$

This is the precise idempotence and nested composition rule, unlike applying an acceleration-to-fraction map twice. The three bands $P_c$, $P_p-P_c$, $I-P_p$ are mutually energy-orthogonal projectors summing to identity. They generalize to an arbitrary nested chain; for multiple sibling domains use an orthogonal sum only when their owned interior spaces are energy-orthogonal. Geometric overlap is not an ownership rule. Arbitrarily adjacent nonnested interior projections need not commute (exact five-node counterexample in verifier).

### Source registration is the dual operation

Given $K\phi=f$ (sign of f depends on potential convention), the source passed to the parent is

$$f_{\rm reg}=Q_c^Tf,$$
$$K^{-1}f_{\rm reg}=Q_c\phi.$$

For each child-harmonic test $h$ (i.e. $Q_ch=h$), $h^Tf_{\rm reg}=h^Tf$. The removed source vanishes on all child-harmonic tests, and the registered source has zero entries in the child interior. For an ungrounded child subgraph with its full interface retained, or an interior sufficiently far from the outer grounded edge, the harmonic lift of constant boundary values is constant inside, hence total source is conserved. If linear coordinate functions are harmonic on the graph (as on the uniform Cartesian grid), first moments are conserved too; no arbitrary graph claim is made. Continuum balayage preserves all harmonic moments, hence mass and the exact Newtonian exterior potential with appropriate boundary conditions. This is the source-sweep identity already present upstream; the energy-dual formulation makes it directly composable with the local residual.

$$Q_p^TQ_c^Tf=Q_p^Tf.$$

The parent must replace the internal source by its registered equivalent, not append the pointer to the original source. The local residual can be reconstructed from its own source and child boundary without double counting. This telescopes for fixed nested domains. It is not a proof of a time-dependent ownership map or causal propagation.

## 3. The registered object is a response law, not just a clock number [T]

Partition an energy into interior variables u and interface b, keeping b variable:

$$E(u,b)=\tfrac12u^TK_{II}u+u^TK_{IB}b+\tfrac12b^TK_{BB}b-f_I^Tu-f_B^Tb.$$

Solving internal settlement at fixed b yields

$$u_*(b)=K_{II}^{-1}f_I-K_{II}^{-1}K_{IB}b.$$

The first term is the fixed local residual; the second is the harmonic host/boundary extension. This makes 'siloed' exact for the residual, not for the complete potential or all motions. The resulting boundary action is

$$\Gamma(b)=\tfrac12b^TSb-f_{\rm reg,B}^Tb-\tfrac12 f_I^TK_{II}^{-1}f_I,$$
$$S=K_{BB}-K_{BI}K_{II}^{-1}K_{IB},\qquad f_{\rm reg,B}=f_B-K_{BI}K_{II}^{-1}f_I.$$

The boundary current (or reaction) is $\partial_b\Gamma=Sb-f_{\rm reg,B}$. Constants in Γ do not affect fixed-domain field variation but may matter if masses or boundaries vary. This is static energy elimination, not the elimination of a dynamical oscillator. It tells us what a registered NET Field must preserve: the trace, source response and boundary stiffness (or equivalently the whole reduced action). Passing only one constant clock value loses the source. Passing the flux only at a single boundary state loses the susceptibility $S$; a changing parent needs the response function. The parent action may itself contain a nonlinear constitutive response, but it uses this record exactly once. If there are no external edges in the child action, the common-shift stiffness has a null direction; the exterior reference belongs to the total grounded problem. The source term carries the mass flux even for a uniform trace.

## 4. Nonlinear closure really is associative, but not pointwise μ [T]

For any bounded-below energy with variables (u,v,b) and finite attained minima, define the partial closure $\mathfrak C_u E(v,b)=\min_u E(u,v,b)$. Then

$$\mathfrak C_v\mathfrak C_u E(b)=\min_{u,v}E(u,v,b).$$

The same equality holds for infima under the usual extended-real conventions. This is the correct hierarchical composition law for an action. Eliminating an already absent variable is identity. For a smooth unique regular minimum, $\nabla_b\Gamma=E_b(u_*,b)$; if $E_{uu}$ is invertible then the Hessian is $E_{bb}-E_{bu}E_{uu}^{-1}E_{ub}$. Even a nonlinear child can be passed upward through its reduced action; it can respond when the parent changes the interface. Associativity does **not** imply the microscopic state stays fixed. Exact compression into finitely many scalar records requires a finite-dimensional boundary or further proven sufficient statistics. The verifier solves twenty nonlinear loaded paths both all at once and by child action/current matching using the actual fully open constitutive energy $e(v)=v^2/2-|v|+\ln(1+|v|)$ in units $a_0=1$. Its flux is $j(v)=\mu(|v|)v$. All split solutions reproduce the direct field, current and energy to the stated tolerance.

Contrast applying the flux map $j(x)=x^2/(1+x)$ for positive x to its own output:

$$j(j(x))=\frac{x^4}{(1+x)(1+x+x^2)}\ne j(x).$$

At x=1, first settlement is 1/2; repartition gives 1/6. This is a model of an erroneous double application, not a claim that a physical acceleration equals its output after closure. It explains why 'settled' must be a structural property of the closure state or eliminated variables, rather than an algebraic property of μ. The fraction map itself is also not idempotent when regarded formally as a map on positive numbers.

## 5. A minimal ownership-separable action [D]

The previous conditional trace-only action cannot generate a galaxy's bulk modified equation if applied solely to its outer surface. The nested projection resolves the *mathematical architecture* of that objection. For fixed nested ownership and the orthogonal bands $P_i$ of section 2, define one variational model

$$\mathcal E(\phi)=\sum_i\left[\tfrac12\|P_i\phi\|_K^2-f^TP_i\phi-\mathcal R_i(P_i\phi)\right].$$

Here the same established constitutive potential may supply $\mathcal R_i(z)=a_0^2\int L(|\nabla z|/a_0)$ with $L(x)=x-\ln(1+x)$, on the bands where the drained response is to be read, and zero on bands representing already-settled bare residuals. This is a conditional ownership rule, not its microscopic derivation. Fixed projectors and disjoint coordinates imply independent stationarity on each band. A perturbation in the parent band leaves the child residual unchanged exactly (even if the child's own response is nonlinear). The quadratic bare part and the prescribed per-band correction preserve the same decomposition under variation. For a linear child this is the same harmonic/residual split as above. The total reconstructed field is still the sum of its bands; the observed local Newtonian residual is the complete local settlement of TetA and TetB, not empty TetB.

If the parent is described by a continuum galactic field, its registered coarse potential can vary throughout the galaxy even if the *outer* closure clock is constant: it contains the relative boundary records of its children. Nonzero inter-child contrasts are compatible with every child having a constant clock trace. The ownership projection preserves these modes, rather than projecting all of the galaxy onto one scalar. The fully open action on that parent subspace is a projected AQUAL equation, not automatically the unrestricted AQUAL PDE everywhere. Recovery of the precise galactic continuum law requires a separate controlled coarse-graining limit. The per-band choice of response is an input, not a proof that all stars settle linearly and galaxies nonlinearly. Actual host matter, nonharmonic trace corrections, overlapping lobes, moving boundaries and relativistic junctions must be accounted for. No conclusion about instantaneous physical influence follows from static elliptic elimination.

### Why the projection matters: an exact leakage counterexample

Take two equal-weight gradient records $h=(b,b)$ and $w=(r,-r)$, so the host and residual are orthogonal. Applying the same pointwise fully open law to the total gradients gives a child contrast current $j(b+r)-j(b-r)$. For $r=1/2$, at $b=0$ this equals $1/3$, but at $b=1$ it is $11/15$. The host changes the internal response even though its uniform acceleration is common. The linear law gives $2r=1$ independent of b; a separately settled nonlinear residual gives $j(r)-j(-r)=1/3$ independently of b. Thus energy orthogonality alone does not make a nonlinear function of the *sum* separable. Ownership must restrict the argument of the nonlinear action or supply an equivalent exact cancellation. This is the algebraic reason an unqualified external-field-insulation claim cannot follow from the constitutive function alone.

## 6. Time-face read: the remaining native derivation [E]

The [three-subread closure](https://github.com/fielddynamics/research/blob/aad94e0e1ec766e9bf8615d8fbcf07126cbd2f95/research/hadamard-null-cone-vortex-flywheel/THREE_SUBREAD_CLOSURE.md) gives the exact reversible $64=1+3+12+48$ multiresolution transform. It is an address/contrast decomposition, not the stiffness-weighted projection of section 2. A common scalar records the shared clock; directional and higher contrasts may carry interface flux and tide. But counting 16 time-face addresses does not show that they encode the reduced action Γ, nor does the 64-record read prove the needed response projection. At fixed 16-dimensional interface a general symmetric Hessian alone has 136 independent coefficients, before symmetry reductions. The native dynamics may restrict this considerably; one must derive that restriction. A static snapshot can supply the boundary state, while response to perturbed boundary clocks can identify the susceptibility. This is a concrete acceptance test, not a call to insert a new physical ledger or oscillator.

Next: derive the boundary action/susceptibility from paired time-face amplitudes (rather than choosing K independently), show the child-detail modes are dark to the parent *variation* of the interaction, and match the registered source to the existing gravitational normalization. Compare the resulting stationary response on nested solar–galactic modes to the upstream ownership action. In the live engine, ensure causal clock reference and conservation through moving or changing closures. The two determinant roots, geometric clock surface and stationary finite Hamiltonian alone cannot establish this physical selection. Proofs 24/25 remain unchanged.

## Reproduce

`OPENBLAS_NUM_THREADS=1 python verify_hierarchical_closure.py > hierarchical_closure_verification_output.txt`

273 fresh assertions (29 exact + 244 numerical), covering exact path-graph projection and Schur identities, noncommuting overlaps, nonlinear leakage, 2D nested grounded graph source registration and energy identities, and direct vs hierarchical nonlinear path solves. These are tests of conditional mathematical constructions, not independent physical proofs. Earlier 3,838 recorded checks preserved, not rerun. Total recorded 4,111. No Lean build or repository write.
