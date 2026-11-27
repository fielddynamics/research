# Information across closure boundaries and the Green response

*GFD · Field Origin vertex research · November 2026 · preparation for a future Proof 26*

**Status:** [T] exact conditional finite variational and graph theorems; [D] continuum scalar response under explicit assumptions; [O] native vortex action, physical source calibration, causality and G. Continuation of [NECESSITY_OF_READ_SETTLE_REGISTER.md](NECESSITY_OF_READ_SETTLE_REGISTER.md) and [HIERARCHICAL_NET_FIELD_CLOSURE.md](HIERARCHICAL_NET_FIELD_CLOSURE.md). Proofs 24 and 25 unchanged. The read here is dependence through interaction, not an asserted algorithm or instantaneous communication.

## 1. The minimum read is determined by the interface, not the total inventory

Let x be interior records of a child, g its interface records, and y its exterior environment. For a fixed owned source f, suppose the child energy is

$$E_C(x,g)=\tfrac12 x^TAx+x^TCg+\tfrac12 g^TDg-f^Tx,$$

where A is symmetric positive definite. The child solution and its exact registered functional are

$$x_*(g)=A^{-1}(f-Cg),$$
$$W_C(g)=\tfrac12 g^T(D-C^TA^{-1}C)g+g^TC^TA^{-1}f-\tfrac12 f^TA^{-1}f.$$

The parent receives the interface response $\nabla_gW_C=(D-C^TA^{-1}C)g+C^TA^{-1}f$. For all allowed g, the minimum sufficient **linear** read of g for interior settlement has dimension rank C. Proof: the sensitivity is −A⁻¹C, with the same kernel and rank as C; coordinates of Cg on im C suffice. The dual read of the child's source into the parent has the same rank, rank(CᵀA⁻¹)=rank C. The source self-energy constant must also be retained if comparing energies or varying a mechanical coordinate; it may be dropped only for fixed-geometry interface stationarity. Equal boundary responses can hide different internal energy.

![Interface read and register](figures/information_01_separator.svg)

Suppose the whole static stiffness is L with a separator B between an interior I and exterior O, L_IO=0. For fixed source in I, variation of the exterior source induces

$$\delta u_I=-L_{II}^{-1}L_{IB}\,\delta u_B,\qquad (L^{-1})_{IO}=-L_{II}^{-1}L_{IB}(L^{-1})_{BO}.$$

Hence rank((L⁻¹)_IO) ≤ rank L_IB ≤ |B|. The equality of ranks is not general; it holds when the exterior drives all required interface directions. This is an exact distributed accounting bound. Even when the complete inverse is dense, the information from a neighbor can be exposed through a small interface. The source inventory is owned once, and influence may overlap. Nested elimination composes by minimizing over all shared traces, as in the preceding research. This does not establish a physical partition for arbitrary overlapping nonlinear fields.

## 2. A positive local closure law cannot be blind to any connected source

Take a finite connected graph with positive edge weights, grounded at at least one boundary vertex, and let L be its Dirichlet weighted graph Laplacian on the remaining vertices. Assume the ungrounded graph is connected and connected to the ground. Its energy is strictly positive away from zero. The inverse G_L=L⁻¹ has strictly positive entries: solve Lu=e_j; at a negative minimum the Laplacian cannot be positive, and equality forces all neighbors to share the minimum (including along a path to ground). Thus u≥0. At a zero minimum away from j, all neighbors must also be zero, contradicting the equation at j by connectedness. Grounded edges act as edges to fixed zero. This is the finite maximum principle. If removing ground disconnects the free graph, strict positivity holds only within its connected blocks.

For energy E(u;s)=κ uᵀLu/2+q sᵀu with κ>0, q≠0, the settled potential is

$$u_*(s)=-\frac{q}{\kappa}L^{-1}s.$$

Consequently $\partial u_i^*/\partial s_j=-(q/\kappa)(L^{-1})_{ij}$ is nonzero for every free connected pair. For this specified class of closure law, nonblind accounting follows, even for objects not adjacent in the graph. No requirement exists for each object to access every raw record directly. The interface theorem above explains how local reads yield a global dependence. In an actual dynamical system static dependence is not instantaneous signal transport.

### Exact six-node witness

Use a path with six free nodes, unit edges, grounded ends at 0 and 7. For i,j=1,…,6,

$$(L^{-1})_{ij}=\frac{\min(i,j)[7-\max(i,j)]}{7}.$$

Divide the path into I={1,2,3}, B={4}, O={5,6}. All six entries of the cross inverse are positive, yet the 3×2 cross block has rank one: all external source changes affect the interior through the one interface value. The verifier reconstructs the complete solution by separate child and exterior solves with a shared interface, for arbitrary symbolic sources. It also checks that sources differing by (2,−1,0) in I have the same boundary source term, yet different interior potentials and generally different source self-energy.

![Dense global Green response and rank-one separator](figures/information_02_green.svg)

## 3. The gravitational candidate is the variation of the same settled energy

Eliminate u from the preceding energy:

$$E_*(s)=-\frac{q^2}{2\kappa}s^TL^{-1}s.$$

The mixed derivative is

$$\frac{\partial^2E_*}{\partial s_i\partial s_j}=-\frac{q^2}{\kappa}(L^{-1})_{ij}.$$

For two positive sources m_A and m_B at distinct vertices the cross energy is −(q²/κ)m_A m_B(G_L)_AB; the two terms in the symmetric quadratic cancel the factor 1/2. Positivity of G_L establishes a negative cross energy, not monotonicity with distance on an arbitrary graph. It is also a derivative of the same operator that controls the read. In this sense the interaction is not an additional step after settlement. The force is mechanical variation of the reduced energy including any geometry dependence of L, source placement and self-energies.

### Continuum conditional result

Assume an isotropic local scalar stiffness in three infinite spatial dimensions, with fields decaying at infinity, and an additive source coupling qρφ. Set

$$E[\phi]=\int\left(\tfrac{\kappa}{2}|\nabla\phi|^2+q\rho\phi\right)d^3x.$$

Varying yields −κΔφ+qρ=0. The inverse of −Δ is 1/(4πr) with these boundary conditions. For two compact separated distributions the cross energy is −q²/(4πκ) times the double integral of ρ_A(x)ρ_B(y)/|x−y|. For point sources (discard divergent position-independent self energies) or disjoint spherical sources, it reduces to

$$E_{AB}(r)=-\frac{q^2}{4\pi\kappa}\frac{m_A m_B}{r},\qquad F_r=-\frac{q^2}{4\pi\kappa}\frac{m_A m_B}{r^2}.$$

For generic finite sources this is the leading far-field monopole with higher multipoles. The acceleration of B is force divided by its inertial mass; universal source/inertial mass equality is an additional premise. Thus in this class

$$G_{\rm eff}=\frac{q^2}{4\pi\kappa}.$$

The dimensionful q and κ are defined by the action; this is not a numerical derivation of G. Anisotropic, massive, nonlocal or different-dimensional operators yield other Green functions. The graph positivity proof and the continuum attraction require an actual source term and sign. The earlier four-port diamond symbol has leading acoustic term 2h²|k|² from the tetrahedral frame sum; this supplies a conditional spatial route to the scalar continuum stiffness, not its physical calibration or a covariant completion. The new verifier checks that quadratic coefficient independently. See upstream FIELD_ORIGIN_GRAVITY_READ.md for the inherited diamond calculation.

![Inverse-square response and scale ambiguity](figures/information_03_force.svg)

## 4. Two precise obstructions to deriving the value of G from closure alone

**Scale ambiguity.** Replacing E by λE for λ>0 preserves every stationary minimizer, every sufficient read, and the closure compatibility conditions. It scales the reduced energy and mechanical force by λ if the inertial normalization is held fixed. The geometry and the settlement map alone cannot select the energy normalization. An independent physical action/energy scale is necessary.

**Source selection.** A quadratic scalar source response with a bridge T and positive stiffness K gives a susceptibility of the form vᵀT†K⁻¹Tv. If T=tI, this scales as |t|², not |t|⁴². A rank-deficient T can still couple a nonzero source. Hence a 21-dimensional complete-frame determinant cannot be inferred from the ordinary static read, stationarity or atomic closure. The [projective norm and Walsh bridge](PROJECTIVE_NORM_WALSH_BRIDGE.md) remains an exact construction for the distinct collective observable. Deriving that observable requires a physical source vertex that is sensitive to all independent reconstructed directions, with lower-order contributions absent or canceled. A determinant of a linear operator is not the same as the derivative of its minimized quadratic energy.

In particular, the required microscopic source normalization is q²/(4πκ)=(17/13)α²¹ ħc/m_e² for the tree-level target. Do not introduce it as a fit. The proposed loop factor is separate. The parent-level source is additive, not multiplied by α²¹ again on every hierarchical closure.

## 5. Static read versus temporal propagation

A local wave witness on the same graph has u¨+ω²Lu=−b e_j with zero initial conditions and a step source. Taylor expansion gives

$$u(t)=-b\sum_{n\ge0}\frac{(-\omega^2)^n t^{2n+2}}{(2n+2)!}L^n e_j.$$

If d is the graph distance between i and j, then (L^n)_ij=0 for n<d, and (L^d)_ij is (−1)^d times the positive sum of shortest-path weight products. For the unit path the first remote term is −bω^{2d}t^{2d+2}/(2d+2)!. This demonstrates successive local dependence, not strict light-cone causality: an analytic continuous-time finite lattice generally has small immediate tails. A physically causal continuum limit or retarded interface action must be derived separately. Static elimination itself is not a signaling protocol.

## 6. Next gate for the native engine

The source and boundary read are mathematically linked by one action in the positive scalar model. The decisive next step is to obtain such a response from the sustained collective flywheel and nonlinear time-face coupling without assuming scalar potential energy or inserting G. Extract a gauge-invariant mechanical source vertex, its mixed derivative with respect to registered inventory and boundary state, and its long-wave stiffness. Compare it to ordinary single-mode response and the projective collective determinant. Test source additivity, lower-order source terms, the sign, retarded propagation, and the equality of gravitational and inertial mass. Read–settle–register necessity supplies the reason to seek these quantities; it does not by itself prove the native implementation. No new numbered proof or Lean certification.

## Reproduce and sources

`python verify_closure_information.py` (SymPy) verifies the six-node graph Green matrix, rank-one factorization, symbolic child/exterior solve, source-nullspace witness, mixed source energy, scale and rank-defect obstructions, shortest-walk onset and tetrahedral acoustic quadratic coefficient. `python make_closure_information_visuals.py` produces the three SVGs. [Offline explorer](interactive/closure_information.html) evaluates the graph and continuum witnesses. Inherited sources: the cumulative closure necessity and hierarchy notes; upstream [Field Origin gravity read](https://github.com/fielddynamics/research/blob/a3a019cc553476c4288aa7a64bac8b04d754782d/research/hadamard-null-cone-vortex-flywheel/FIELD_ORIGIN_GRAVITY_READ.md), and [unified closure action](https://github.com/fielddynamics/research/blob/a3a019cc553476c4288aa7a64bac8b04d754782d/research/unified-closure-action/unification/UNIFIED_CLOSURE_ACTION.md), as documented in previous archive source excerpts. New conditional theorems here: explicit separator minimal read, positive graph nonblind source response, mixed-source Green energy and scaling obstruction, local time-onset calculation. No previous suites rerun.
