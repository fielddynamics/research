# Atomic inverse reconstruction and the gravitational coupling

*Continuation of the same Field Origin research — not Proof 26.*

**Status:** exact conditional selection theorem, constructive effective model, and explicit obstructions. Neither a native source vertex nor a first-principles prediction of G has been established. Upstream repository inspected at `a3a019cc553476c4288aa7a64bac8b04d754782d`. Proofs 24/25 and the live repository are unchanged.

## 1. One ledger, three inverse subreads

[Three subreads](https://github.com/fielddynamics/research/blob/a3a019cc553476c4288aa7a64bac8b04d754782d/research/hadamard-null-cone-vortex-flywheel/THREE_SUBREAD_CLOSURE.md) supplies W=DB, with normalized full Walsh read W, recursive orthogonal tree B, and within-scale mixer D. Therefore W^{-1}=B^T D^T. The reverse tree restores four, sixteen and sixty-four records with 1,4,16 four-way readers. It requires all retained detail coordinates; a single common record cannot recover a generic truth table. The Sierpiński matrices in the [null-rotation proof](https://github.com/fielddynamics/research/tree/a3a019cc553476c4288aa7a64bac8b04d754782d/proofs/g-null-rotation) are different triangular factors of Walsh matrices; the 1/4/16 block operator has 91 filled entries and determinant one. Its 273 within-grade capacity is not its nonzero count. Neither reversible transform produces physical attenuation.

For the recursive rotation cycling three noncentral labels and fixing the central label, depth k has exactly one fixed word and (4^k-1)/3 three-cycles. Prefix-constant invariant ranks are 1,2,6,22. Differences are 1,4,16, giving 21 invariant contrasts. The other two complex C3 character spaces each have dimension 21; full detail dimension is 63. Both the actual tree and detail mixer commute with this simultaneous label rotation. Symmetry alone does not force a physical source to read only invariant contrasts, nor does this operation equal the core's spatial rotation on arbitrary microscopic amplitudes.

## 2. Complete-frame selection theorem [T/D]

Let E be the real 21-dimensional invariant contrast space and T:E→E the candidate transmission, holding the common clock fixed. The squared volume of a transmitted orthonormal frame is

$$P(T)=\|Tv_1\wedge\cdots\wedge Tv_{21}\|^2=\det(T^T T)=|\det T|^2.$$

This is invariant under orthonormal basis changes and vanishes if rank(T)<21. More generally suppose a nonnegative response functional on square contractions obeys (i) invariance under independent orthogonal input/output changes of basis, (ii) serial composition P(AB)=P(A)P(B), (iii) calibrated single-direction response P(diag(t,1,...,1))=|t|². By singular-value decomposition and the product of the single-direction diagonal matrices, P(T)=product_i s_i²=det(T^T T). Rank-deficient matrices are included by the single-direction calibration at zero. This is a uniqueness theorem *conditional on the functional premises*, not proof that a gravitational source satisfies them. An equivalent complex statement uses unitary basis changes.

If T is an ordered nonlinear inverse reconstruction Jacobian at a fixed common record, with diagonal blocks tI_1,tI_4,tI_16, arbitrary lower cross-grade derivatives do not change its determinant. For |t|²=alpha the complete-frame response is alpha^21. This local derivative volume is not generally an ordinary wave intensity, nor the probability of a completion event without an appropriate measurement law. A state-dependent transmission may give nonconstant volume.

## 3. What atomicity does and does not force [T]

[What Is Gravity?](https://github.com/fielddynamics/research/blob/a3a019cc553476c4288aa7a64bac8b04d754782d/research/g_from_topology/what_is_gravity.md) quotes Paper I's simultaneous agreement principle. That principle is weaker than independent orthogonal-frame volume registration or independent gate success. For 21 Bernoulli events of identical marginal probability alpha, independent gates give alpha^21; a common random gate yields alpha and still registers only when all events succeed. The general intersection bounds are max(0,21 alpha-20) <= P_all <= alpha. Neither atomicity nor equal marginal probability chooses the product. A scalar common-gate map tI can attenuate every direction and still couple a scalar source to its ordinary norm, giving alpha rather than alpha^21.

A useful stronger hypothesis is independent gate deletion: a real-analytic (or complex-analytic in independent gate amplitudes) completion amplitude A(t_1,...,t_21) vanishes identically whenever any individual t_i=0. Its convergent power series must have every exponent >=1, so A=(product_i t_i)F(t). If F(0) is finite and nonzero, the common-gain intensity begins at order alpha^21 for t_i=sqrt(alpha), with coefficient |F(0)|². Exact alpha^21 follows only if the factor has unit modulus, e.g. the calibrated complete-frame determinant. This deletion rule is stronger than the existence of a single completed stationary solution. Internal cross interactions can change F, and atomicity does not imply independent deletion. In the existing 33-site Stage VII model the 104-edge incidence has rank 32; every diagonal phase symmetry of the nonzero hopping graph is a common phase. Thus 21 independent site phases cannot be presumed as microscopic protection of this monomial. This does not rule out a derived nonlocal symmetry or constrained source law.

## 4. A geometric candidate for elementary alpha [D]

The existing electron relation gives r_e/bar_lambda_C=alpha_EM, using the classical electron radius and reduced Compton wavelength. Normalized constant profiles on nested one-dimensional intervals of lengths L and r have overlap sqrt(r/L). If the paired time faces read such normalized temporal modes at identical propagation speed c, with durations bar_lambda_C/c and r_e/c, their elementary squared overlap is alpha_EM. This needs no fitted numerical coefficient, *given the profiles, 1D measure and scales*. Uniform profiles in d-dimensional geometrically similar supports instead give alpha_EM^d. This is not a native derivation of time-face profiles, a Compton clock, or the value of alpha. General mode shapes or phase mismatch change the overlap. A two-output lossless dilation T^T T+C^T C=I retains the complementary response; no destruction of the microscopic ledger follows.

## 5. Winding settlement and source calibration [D]

For K=4 and the 120-degree contrast-plane shift S, S+S^T=-I. The prescribed squared residuals (KI∓S)^T(KI∓S) have stiffness f_A=K²+K+1 and f_B=K²-K+1. In normalized even/odd coordinates the common-scale stiffness is H=[[f_O,K],[K,f_O]], f_O=K²+1. Its determinant is f_A f_B=273, with f_A f_B-1=K² f_O=272. Eliminating the internal odd coordinate gives effective stiffness f_A f_B/f_O. Comparing its compliance to the TetA reference gives f_O/f_B=17/13. No native Hamiltonian Hessian is asserted to equal this prescribed winding energy. The reference drive and response normalization must come from the same native interaction.

For a dimensionally explicit candidate effective model, let phi have dimension inverse length, rho be rest mass density, and use

$$E[\phi]=\hbar c\left[\frac{\kappa}{8\pi}\int|\nabla\phi|^2 d^3x + g\int(\rho/m_e)\phi\,d^3x\right].$$

Variation with isolated boundary conditions gives Laplacian phi=4πg rho/(κ m_e). Two separated masses interact with cross energy -ħc g² m_1 m_2/(κ m_e² r). Thus G=ħc g²/(κ m_e²). Taking g as the complete-frame amplitude |det T|=alpha^(21/2) and κ=f_B/f_O=13/17 reproduces the target. Equivalently Phi=ħc g phi/m_e gives the conventional mass-coupled potential. This derives the consequence of one explicitly specified source vertex and stiffness, not their physical selection. The mass charge must be additive for local pointers; alpha^21 must be an intensive cell coupling, not multiplied once per child, star or galaxy. The complete boundary response action remains necessary for tides and nonlinear parent fields.

## 6. Decisive obstruction to replacing the source calculation by a determinant [T]

For a positive stiffness A and drive j, minimization of 1/2 x^T A x-j^T x yields -1/2 j^T A^{-1} j. Gaussian integration gives a determinant prefactor (det A)^(-1/2) which cancels in the normalized generating function Z(j)/Z(0); the connected source Hessian is A^{-1}. Thus simply counting all settled internal degrees, or integrating them out, does not multiply a universal force by their determinant. It is necessary that the physical source itself couple to the complete-frame registration (or that an equivalent selection rule remove all lower-order terms). Under ordinary rotational and common-phase symmetry, squared contrast norm is an allowed scalar alongside the determinant. The physical argument needs a stronger constraint, not another polynomial coincidence. The [unified closure action](https://github.com/fielddynamics/research/blob/a3a019cc553476c4288aa7a64bac8b04d754782d/research/unified-closure-action/unification/UNIFIED_CLOSURE_ACTION.md) explicitly leaves the product source vertex, elementary alpha, native stiffness ratio and mass normalization open. Its existing static charge identity starts from a prescribed source. The present theorem identifies sufficient conditions and concrete failure tests.

## 7. Next acceptance test

Derive the actual coupling of rest-energy variation to time-face reconstruction. Compute the response with one symmetry-adapted contrast transmission disabled while all other directions are allowed to settle. A determinant-selected gravitational vertex vanishes when any independent direction is genuinely blocked; ordinary scalar read need not. Test all 21 directions, basis covariance, phase and clock dependence, source reciprocity and conservation. Show the measured lower-order terms vanish by a constraint of the native action, not by a fitted subtraction. Then evaluate the native one-channel overlap and winding susceptibility with independent physical scales. The conditional model gives the desired algebra, but the native action and source selection are not solved. No one-loop QED derivation is claimed.

## Reproduce

`OPENBLAS_NUM_THREADS=1 python verify_atomic_reconstruction.py > atomic_reconstruction_verification_output.txt`

89 assertions (32 exact and 57 numerical), including rotation orbits, inverse tree, Sierpiński support, winding Schur algebra, deletion examples, nested uniform overlap integrals, Stage VII graph phase-constraint rank, orthogonal-basis invariance and rank-loss examples, norm complements, triangular determinant and conditional source energy. Counts are test assertions, not independent theorems. Historical 4,111 assertions retained, not rerun. Cumulative recorded 4,200. No Lean build or repository write.
