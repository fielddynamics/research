# Collective tetrad settlement and the emergence of AQUAL

**Proposed standalone GFD proof — November 2026.** Conditional theorem. The new results are the independent-face obstruction, uniqueness of the invariant quadratic face capacity, collective read/registration factorization, and the resulting coupled four-face response. The scalar screening, vacancy energy and AQUAL elimination have antecedents in the repository; they are not claimed as new microscopic derivations.

## 1. Definitions and premises

Let e=(1,1,1,1)^T, V=e^perp, P=I-ee^T/4, and let

$$T=\tfrac12\begin{pmatrix}1&1&1\\1&-1&-1\\-1&1&-1\\-1&-1&1\end{pmatrix}.$$

Then T^T T=I_3 and TT^T=P. Use dimensionless drive x=∇Φ/a₀ and face drive z=Tx, so z lies in V. Let q in V be the dimensionless corrective response, not the TetA share itself. The following premises have separate meanings:

1. **Complete read.** Face/channel/subchannel values represent a consistent snapshot; a new registered state is committed only once its required read and settlement are complete. This is a proposed protocol, not a timing theorem.
2. **Collective capacity.** There is one normalized remaining vacancy v=1-b, where b=||q||₂ is the magnitude of the joint directional response (0≤b<1). The squared norm is quadratic and invariant under relabelling of the tetrahedral faces; its normalization is inherited from T.
3. **Degree-one settlement.** With a fixed drive, all directional components use the same available capacity: q=vz at equilibrium. This is the vector form of the existing scalar balance b=x(1-b). A possible rate model is qdot=κ[(1-||q||)z-q], κ>0; the rate is not needed for the static theorem.
4. **Work conjugacy.** The effective flux is x-p, p=T^Tq, or equivalently a Newtonian quadratic energy and a local work term −x·p with a cost for the internal response. The driving x is identified with the time-leg acceleration in the static regime. Neither this identification nor the physical realization of the vacancy is forced by combinatorics alone.

No new static fitted constant is used. The scale a₀ and Newton's constant G are inherited inputs here.

## 2. Independent-face obstruction

**Lemma 1.** If a continuous face-local map h is identical on all four faces and h applied componentwise sends V into V, then h(t)=kt. Indeed h(0)=0 from the zero tuple; (t,−t,0,0) establishes oddness, and (s,t,−s−t,0) gives additivity. Continuity gives linearity. The conclusion assumes arbitrary signed face drives in V; the same local result holds on a neighborhood with the corresponding restricted additive equation.

Thus a nonlinear face-local response needs reconciliation or shared information. Atomic commit alone does not supply that reconciliation: the projected map P h(z) is a counterexample. For h(t)=t/(1+|t|), take equal-norm z=(1,1,−1,−1) and z'=(√3,−1/√3,−1/√3,−1/√3), both of norm 2. Then P h(z)=z/2 but P h(z')=(√3/4)z'. Hence even zero-sum preservation after projection plus atomic commit and permutation symmetry do not guarantee isotropy.

## 3. Why the collective quadratic magnitude is canonical

**Lemma 2.** A quadratic form invariant under every face permutation is aI+b ee^T. To see this, all diagonal entries coincide, as do all off-diagonal entries. Restricted to V it is a||z||², and requiring ||Tx||=||x|| fixes a=1. Equivalently average a symmetric matrix over all 24 permutations. This proves uniqueness among normalized quadratic forms, not uniqueness among arbitrary tetrahedrally invariant nonlinear functions. For example ∑z_i⁴ is also invariant and distinguishes the two directions above.

The complete normalized Walsh/tree read preserves the norm of its input. For a 64-leaf snapshot r=(r_abc), define U: R⁴→R⁶⁴ by (Uz)_abc=z_a/4, so U^TU=I. The coarse directional read is z=P U^T r. Its squared magnitude is r^T U P U^T r. This quantity is invariant under a mere change of orthonormal read basis B: use the transformed projector B U P U^T B^T acting on Br. A full 64-record norm is NOT generally the same as this coarse norm: constant and fine-detail components can contribute without changing z. A physical theory must justify which modes are registered in the local acceleration, rather than equating all 64 coordinates to a single three-dimensional gradient.

## 4. The collective settlement theorem

**Theorem.** Under premises 2–3, for any z∈V there is a unique settled q∈V with ||q||<1. Writing R=||z||, its value and common vacancy are

$$q_* = \frac{z}{1+R},\qquad b_* = \frac{R}{1+R},\qquad v_* = \frac1{1+R}.$$

Proof. Since q=vz with v>0, taking norms gives b=(1-b)R. Solve the scalar equation, then substitute; the solution lies in the open unit ball and V. At R=0 the unique response is zero. No angular ambiguity remains because the shared degree-one drive fixes q parallel to z. ∎

The shared vacancy is one scalar, but q still has three directional components. Its complement flux is z−q*=Rz/(1+R). The magnitude b equals μ(R); the fraction of the drive carried by q is instead v=1−μ(R). The coupling polynomial's capacity may consequently be written C=17+4σ=13+8b with σ=2b−1, the continuous share difference (not the state label s, whose value −1 is TetB). This is an inherited count/partition identity, not a proof of a microscopic gravitational normalization.

For the optional rate model and fixed z, V is invariant. With b=||q||>0, bdot≤κ[(1−b)R−b]; thus an initial point in the open unit ball remains there and b(t)≤max(b(0),R/(1+R)). Transverse components decay as exp(−κt). The Lyapunov function in §5 ensures convergence to the unique equilibrium; it does not establish physical dissipation or select κ. Along an aligned nonnegative response, b(t)=b*+(b(0)−b*)exp[−κ(1+R)t]. A new registration may be defined only after settlement to the required tolerance (or as the exact static solution); finite-time exact convergence is not implied.

## 5. Derivation of the work potential and AQUAL

With p=T^Tq, let b=||p||. If work conjugacy is −x·p and the vacancy-dependent mobility is κ(1−b), matching the rate law to gradient descent uniquely requires

$$\nabla_p W = p/(1-b).$$

Integrating radially, W(0)=0 gives W(b)=−b−ln(1−b). Its Hessian has eigenvalues 1/(1−b) transverse and 1/(1−b)^2 radial, and equals I at b=0. It is strictly convex. Therefore

$$E(x,p)=\tfrac12||x||^2-x\cdot p+W(||p||)$$

has a unique minimum in p, given by the theorem. Substitution yields

$$E_{eff}(x)=\tfrac12R^2-R+\ln(1+R),\quad R=||x||.$$

Envelope differentiation yields J=x−p*=μ(R)x, μ=R/(1+R). Restoring dimensions, the static action is

$$\mathcal S[\Phi]=\int [\frac{a_0^2}{4\pi G}E_{eff}(\nabla\Phi/a_0)+\rho\Phi]d^3r.$$

For compactly supported variations (or fixed boundary data), integration by parts gives

$$\nabla\cdot[\mu(|\nabla\Phi|/a_0)\nabla\Phi]=4\pi G\rho.$$

This is AQUAL with F(y)=2E_eff(√y)=y−2√y+2ln(1+√y). The weak-field density is R³/3+O(R⁴), while the leading large-R density is R²/2. No assumption that Newtonian and total fields align is needed for this variation.

For the rate model the cost W−x·p decreases at rate −κ(1−b)||∇W−x||². On the compact ball guaranteed in §4, the mobility is bounded below, and strong convexity implies exponential decay of the energy gap. This is a mathematical dissipative model, not an autonomous conservative vortex derivation.

## 6. Cross-face susceptibility: a falsifiable signature

For z∈V and R>0, the intrinsic derivative, represented as a four-by-four matrix annihilating the common direction, is

$$Dq_* = \frac{P}{1+R}-\frac{zz^T}{R(1+R)^2}.$$

At R=0 it is P. The off-diagonal entries include both the zero-sum constraint and the rank-one feedback from the shared vacancy. On V its eigenvalues are (1+R)^−1 twice and (1+R)^−2 once. The effective current derivative is P−Dq*, with eigenvalues R/(1+R) twice and R(R+2)/(1+R)^2 once. Both derivatives are symmetric and annihilate e. In 3D coordinates the latter is the AQUAL tangent tensor. It is positive definite for R>0 and degenerates at zero.

This provides a native-engine test stronger than checking scalar saturation. The complete correction has rank 3 for every finite R. A model with only a single regular internal scalar coupled linearly to the drive, or a two-dimensional internal tangent, cannot generate that correction solely by a Schur complement B H^−1 B^T. A field-dependent direct Hessian is another possible mechanism and is not ruled out. Three directional response coordinates with one shared scalar vacancy are sufficient in the constructed model. In a microscopic derivation the coupled directional susceptibility must emerge from the inherited Hamiltonian and work term, not from inserting the target matrix.

## 7. Snapshot and registration

Let r be a coherent leaf snapshot, z=P U^Tr, and define the registration record q*=z/(1+||z||). Given complete r, any lossless traversal producing the same r yields the same q*, and the normalized Walsh basis does not change the quadratic statistic. This is a statement about completed reads, not uniqueness of π as an addressing schedule. The complete response is nonlinear: for two admissible snapshots whose first two face readings coincide but whose remaining entries differ, the first response can differ because R differs. E.g. (1,−1,0,0) and (1,−1,2,−2) give first responses 1/(1+√2) and 1/(1+√10). Therefore early independent commits can be wrong even for faces already read. Reading all necessary information, not necessarily every redundant address separately, resolves that ambiguity. Atomic commit is compatible with the theorem but does not force premise 2 or 3.

## 8. Boundary of the result and next native test

- The scalar balance and vector vacancy construction already occur in the November read–settle–register bridge; the new part is their embedding in the four-face closure constraint, the locality obstruction, the invariant quadratic argument, the read factorization and explicit cross-face signature.
- Full T_d symmetry alone allows higher-order anisotropic invariants. A single shared quadratic capacity and degree-one response are physical premises. Even isotropy, exchange, and Newtonian/deep limits do not suffice to fix μ (e.g. odds Ω=x exp[ε x(x−1)/(1+x)^3], with small nonzero ε, have these limits and Ω(1/x)=1/Ω(x)).
- The native scalar vortex branch in Proof 26 is a local maximum in its specified sector, not the positive minimizing cost in §5. The proof does not identify q with that scalar overlap or claim the native Hamiltonian has the required sign or rank.
- The model applies to the fully open constitutive branch. It does not derive the drained/drainless NET Field selection, a₀, G, causal propagation, general relativistic dynamics, or the π schedule.
- Next test: derive three polar time-leg response operators from the full native vortex state, calculate their complete response Hessian with the inherited geometry and check rank, sign, off-diagonal term and dependence on the common magnitude. The axial vortex and polar time-leg response must not be conflated.

## Sources

- [Forced tetrad frame and Hadamard geometry](https://github.com/fielddynamics/research/tree/main/proofs/hadamard-cube-frame)
- [Constitutive exchange proof](https://github.com/fielddynamics/research/tree/main/proofs/constitutive-law-exchange-symmetry)
- [Read–settle–register bridge (Paper VII balance and auxiliary action)](https://github.com/fielddynamics/research/blob/main/research/read-settle-register-bridge/READ_SETTLE_REGISTER_BRIDGE.md)
- [Three-subread closure](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/THREE_SUBREAD_CLOSURE.md)
- [AQUAL energy proof](https://github.com/fielddynamics/research/tree/main/proofs/aqual-energy-functional)
- [Proof 26 revision 4 and native vortex response](https://github.com/fielddynamics/research/tree/main/proofs/recursive-field-closure-response)
