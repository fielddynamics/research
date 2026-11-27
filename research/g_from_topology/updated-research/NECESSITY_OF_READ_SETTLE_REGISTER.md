# The necessity of read, settlement and registration

*GFD · Field Origin vertex research · November 2026 · preparation for a future Proof 26*

**Status:** [T] conditional theorems of information sufficiency, local implicit response and variational composition; [D] finite static witnesses; [O] native dynamical implementation, causal ordering, physical closure principle and gravitational normalization. Proofs 24 and 25 are unchanged. This note develops the conversation's argument that closure cannot be blind to neighbors whose fields influence one another. It does not presume a literal digital computer, a second oscillator, or that every physical field is always in equilibrium.

## 1. Closure as compatibility, not an assumed algorithm

Let a Field Object A have adjustable state x, and let y denote the relevant environment (including neighboring Field Objects). For each admissible y define the feasible closure set C_y = {x : C(x,y)=0}. The constraints might include field continuity, conservation, and a common registered state. If closure selects a unique state, write it S(y). When A's own inventory is variable, write S(a,y); all statements below hold at fixed a.

**Theorem 1 (blind closure criterion).** A deterministic state selected without any dependence on y can close for every admissible y exactly when the intersection of all C_y is nonempty. If closure additionally selects unique S(y), blind settlement is possible exactly when S is constant. Proof: a blind selection x₀ must belong to every C_y; conversely any point of the intersection is a feasible blind selection. Uniqueness gives the second assertion. □

A dependence in the formula C alone is insufficient: C(x,y)=(1+y²)x has x=0 for all y. Conversely C(x,y)=x−y has no common solution when y can vary. Thus the precise premise is **environment-dependent required settlement**, not merely the presence of an interaction term. For genuinely coupled neighbors whose changes alter the admissible or selected state, blind closure cannot work.

## 2. The read as sufficient information

Let R:Y→Z be the neighbor's registered read. An exact settlement using only the read is a map F on the image of R such that S=F∘R.

**Theorem 2 (factorization).** Such F exists if and only if R(y₁)=R(y₂) implies S(y₁)=S(y₂). Necessity follows by applying F. Sufficiency: define F(z) as S(y) for any y with R(y)=z; the implication ensures independence of the chosen representative. F is unique on R(Y). No continuity or efficient implementation follows without further assumptions. □

For nonunique feasibility, the corresponding criterion is that each fibre of R has a common feasible state: intersection_{y:R(y)=z} C_y ≠ ∅ (with a selection for each fibre). A differentiable read and differentiable decoder imply ker DR ⊂ ker DS and rank DR ≥ rank DS. For a linear S this lower bound is sharp: take coordinates of S(y) in a basis of its image. For nonlinear S the local rank bound is necessary but does not guarantee a globally sufficient read.

The read can be implicit physical dependence: a local coupling responds to the relevant state without executing a separate measurement instruction. It need not record all raw interior variables. In particular, two configurations of equal mass may have different tidal responses; total mass alone need not suffice.

![Read sufficiency and blind closure](figures/necessity_01_read.svg)

## 3. Settlement sensitivity from a local energy

Assume a twice continuously differentiable energy E(x,y), and an isolated stationary branch E_x(S(y),y)=0 with nonsingular H_xx=E_xx. The implicit function theorem gives

$$ D_y S=-H_{xx}^{-1}H_{xy}. $$

If H_xx is positive definite, this is a strict local minimum. A nonzero mixed Hessian at the branch implies local dependence of the settled state. If the mixed block has rank r, any smooth sufficient read must have differential rank at least r. This is a precise information-accounting bound, not a count of literal bits. On a connected parameter region a differentiable constant branch has zero derivative; zero derivative at one point does not imply global blindness.

For the quadratic model E=½xᵀAx+xᵀBy+½yᵀDy−fᵀx with A positive definite, S=A⁻¹(f−By) and the minimal linear read has rank rank B. Eliminating x gives

$$ E_{reg}(y)=\tfrac12 y^T(D-B^TA^{-1}B)y+f^TA^{-1}By-\tfrac12 f^TA^{-1}f. $$

The registered response is the Schur complement, not simply a count. At a smooth nonlinear stationary branch, the same Schur formula gives the local Hessian of E_reg. Read = cross response, settle = solve the internal stationarity equations, register = expose reduced energy or its appropriate derivatives. These are complementary aspects of one interaction.

## 4. Mutually inclusive fields and recursive registration

GFD uses “inclusion” for overlapping influence and for nested Field Objects. Distinguish overlapping physical influence from disjoint ownership of source inventory. The same matter must not be added twice. In a fixed static partition with shared continuous scalar trace f and no surface source, a local action yields the interface conditions

$$ \Phi_A=\Phi_B,\qquad n_A\cdot j_A+n_B\cdot j_B=0. $$

Here j is the work-conjugate flux, normals are outward, and the second equation follows from variation of the shared trace. These equations are specific to this scalar variational model; other fields can have other junction conditions. Requiring consistency does not establish an instantaneous physical read of a distant neighbor.

For a domain D define W_D[f]=inf_{Φ|∂D=f} E_D[Φ]. With disjoint child interiors and a residual region, and admissible gluing at interfaces, the parent functional is

$$ W_P[f]=\inf_{\{g_i\}}\left(W_{res}[f,\{g_i\}]+\sum_i W_{child,i}[g_i]\right). $$

This equality is partial minimization of the same total action, not an additional update rule. The parent receives the relevant registered boundary functional, not a second count of all child interiors. A common shift f→f+c gives W_D[f+c]=W_D[f]+c M_D in the existing static gradient-plus-source action, with M_D the owned source integral. The first variation in the constant direction is additive; internal conormal fluxes cancel. Source inventory is not doubled by reading overlapping fields. A planet, solar system and galaxy can each perform this same registration operation, conditional on a valid partition. This does not prove that an arbitrary nonlinear overlapping physical partition is already established. See [HIERARCHICAL_NET_FIELD_CLOSURE.md](HIERARCHICAL_NET_FIELD_CLOSURE.md).

![Mutual inclusion and registered interface](figures/necessity_02_registration.svg)

### Finite interface witness

Two scalar child energies W_A(g)=k_A(g−a)²/2 and W_B(g)=k_B(g−b)²/2, with k_A,k_B>0, settle at g*=(k_A a+k_B b)/(k_A+k_B). Their derivatives at g* sum to zero. The reduced energy is k_A k_B(a−b)²/[2(k_A+k_B)]. Neither child can pick g* from its own data alone when the other boundary datum can vary. If source terms m_A g+m_B g are added, the equilibrium balance includes their sum; a constant shift of all references and the interface changes the energy by c(m_A+m_B). This is a finite witness, not a derivation of the continuum source from vortices.

## 5. What the Hadamard read does and does not prove

For 64 independent real records, full linear reconstruction requires rank 64; normalized W=H₆₄/8 is orthogonal, hence sufficient. When the required settlement is invariant under the simultaneous threefold digit rotation, it factors through orbit averaging if and only if it is insensitive to discarded noninvariant components (for a linear read this is the kernel criterion in §2). In the specified geometry there is one fixed address and 21 three-cycles, so the invariant space has dimension 22. The common scalar and recursive contrast grades have dimensions 1 and 1,4,16 respectively. The 21 is Sierpiński counting, not 21 independent oscillators. The physical source need not factor through the invariant projection merely because its output is invariant: e.g. the squared norm of noninvariant components is rotation-invariant but is lost under averaging. This distinction must be tested.

The [projective norm and Walsh bridge](PROJECTIVE_NORM_WALSH_BRIDGE.md) gives the explicit read W⁻¹ΛW and inverse recursive reconstruction, as well as the finite-field identities. This note supplies a reason to require sufficient accounting; it does not prove uniqueness of Walsh, determine Λ, or select the determinant rather than an ordinary response. The common read must not lose any physically relevant tide, orientation, inventory or history. A static solution operator does not by itself determine retarded transport or clock timing.

## 6. Force as variation of closure

Let r denote a separation or external configuration coordinate. Given a smooth stationary branch x*(r) of E(x,r), the settled energy E*(r)=E(x*(r),r) obeys the envelope identity

$$ \frac{dE_*}{dr}=E_r(x_*(r),r),\qquad F=-\frac{dE_*}{dr}. $$

The first equality follows by the chain rule and E_x=0. The second is the conservative generalized force when r is a mechanical coordinate and E is its potential energy. Differentiating again yields E*''=E_rr−E_rx H_xx⁻¹ E_xr. Thus the read, settlement and force can arise from one action. Nonzero dependence of the internal state alone does not ensure a force: E=(x−r)²/2 settles at x=r with E*=0. A nonconstant E* can give either sign of force. Therefore neither attraction, inverse-square scaling, universality of mass coupling, nor G follows just from the necessity of closure.

A useful finite witness takes E(x,r)=k(x−a)²/2+c(r)(x−b)²/2 with k,c>0. The settled energy is kc(r)(a−b)²/[2(k+c(r))] and the force is −k²c'(r)(a−b)²/[2(k+c(r))²]. This shows exactly how the closure response changes with separation and why the sign depends on the actual interaction law.

![Force from variation of settled energy](figures/necessity_03_force.svg)

For the existing Newtonian static action ∫[|∇Φ|²/(8πG)+ρΦ] dV, stationarity gives ∇²Φ=4πGρ and the conservative acceleration is g=−∇Φ. Here G is already an input. The microscopic challenge is deriving the action's coefficient, source and long-wavelength limit from the native engine, not reinserting them and calling the result a derivation.

## 7. Towards Proof 26 — gates, not claims

The theorem chain is: compatible interaction-dependent closure → sufficient read → stationary settlement → registered reduced response → conservative force under mechanical variation. The existing inverse Sierpiński construction is a candidate implementation of the read and reconstruction; the Field Origin remains the candidate nonlinear interaction, not a separate engine. The remaining tasks are (i) derive the actual native physical closure conditions and sufficient observable, (ii) demonstrate the recursive Walsh read or an equivalent native implementation, (iii) derive causal settlement and the conserved stress-energy/source, (iv) establish the α elementary gain and collective determinant/normalization rather than assume them, and (v) obtain the continuum gravitational response and compare independently with observation. No claim of G derivation or numbered proof is made here.

## Reproduce

Run `python verify_closure_necessity.py` (SymPy, standard library). The exact finite checks cover feasible blind examples, sufficient-read factorization and rank, local sensitivity, Schur reduction, shared-interface settlement, source shift, hierarchical elimination, force and counterexamples, and Walsh projection sufficiency limits. `python make_closure_necessity_visuals.py` regenerates the three SVG diagrams. [Offline explorer](interactive/closure_necessity.html) evaluates the finite witnesses. All are conditional mathematical examples; they do not certify native physics or a new Lean theorem.

## Source register

Conversation: user's mutual-inclusion / non-blind closure argument, and the preceding eight-part response. Upstream inspected at `a3a019cc553476c4288aa7a64bac8b04d754782d`: [unified closure action](https://github.com/fielddynamics/research/blob/a3a019cc553476c4288aa7a64bac8b04d754782d/research/unified-closure-action/unification/UNIFIED_CLOSURE_ACTION.md) §4; [read–settle–register bridge](https://github.com/fielddynamics/research/blob/a3a019cc553476c4288aa7a64bac8b04d754782d/research/read-settle-register-bridge/READ_SETTLE_REGISTER_BRIDGE.md) §2–3; [net-field rule](https://github.com/fielddynamics/research/blob/a3a019cc553476c4288aa7a64bac8b04d754782d/proofs/net-field-rule/README.md). This note distinguishes the new abstract necessity/factorization arguments from inherited static action results. No new upstream proof rerun.
