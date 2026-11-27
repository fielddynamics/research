# Coupled time faces: metric constraint, susceptibility and a test of G

Continuation of `G_TIME_FACE_CONSTRAINT.md` and `G_NATIVE_CLOCK_UNIVERSALITY.md`. This audits the existing candidate effective model rather than modifying Proof 26 or H36. Exact identities below are not an independent derivation of a microscopic gravitational theory.

## 1. Time is a metric relation, not a separate attenuation channel

In coordinates x0=ct the ADM metric with spatial metric h, shift beta and lapse N has block entries g00=−N²+betaᵀ h beta, g0i=(h beta)i, gij=hij. The Schur complement gives det(g)=−N² det(h). Hence

    u = ln N = 1/2 ln|det g| − 1/2 ln det h.

The lapse is a ratio of volume measures, not the absolute determinant of an internal transmission matrix. Uniform time rescaling is a choice of normalization; relative clock rates in a static spacetime are observable. At zero shift, the acceleration of initially stationary free matter relative to static observers is −c² D u, with D the spatial gradient; stationary observers have opposite proper acceleration. See the existing [SST time-leg proof](https://github.com/fielddynamics/research/tree/main/proofs/sst-covariant-time-leg).

The logarithmic derivative of a normalized determinant read N=|det T|/|det T_ref| is Re Tr(T^−1 dT). For T=tB, T_ref=tB_ref with constant nonzero t, the factor t^21 cancels. An ordinary Gaussian elimination gives a Schur complement in the classical energy; a Gaussian fluctuation integral gives a log determinant in the effective action, not a determinant source vertex. A collective frame amplitude may be a determinant under alternating multilinearity and oriented-volume assumptions, but the physical clock is positive and orientation-independent. A determinant line must have an explicit invariant real read, or a compensating phase/orientation if complex. None of this follows merely from dimension 21.

## 2. Time scaling is necessary but insufficient for the spatial response

For static isotropic tetrad diag(exp u,exp −v,exp −v,exp −v), det e=exp(u−3v), and null rays have coordinate optical index n=exp(−u−v). If v=gamma u at weak field and u=−GM/(rc²), the first-order deflection for minimal metric light coupling is (1+gamma)2GM/(bc²) at impact parameter b. Pure lapse v=0 gives half GR; uniform spacetime conformal scaling v=−u gives no deflection; fixed four-volume v=u/3 gives two-thirds of GR. The GR lock v=u instead requires det e=exp(−2u) in these coordinates. Therefore a generic fixed-volume or uniform conformal settlement is not the sought mechanism. These are coordinate-form weak-field tests, not assertions about a literal material strain.

In static GR the lapse acts as a constraint multiplier, not an extra propagating scalar. At zero shift the static gravitational action contains N sqrt(h) R(h) (with boundary terms). Variation in N yields R(h)=16 pi G rho/c² for nonrelativistic matter; a flat spatial slice with a spatially varying lapse alone does not solve the ordinary static sourced constraint. Variation in h supplies the complementary equation. The previous weak stationary reduction gives v=u and physical stiffness c⁴/(4 pi G). A microscopic theory must derive both this spatial lock and stiffness, not assume a propagating scalar clock. The mass source rho c² u follows at weak field from universal metric matter coupling, with binding and stress to be included consistently via the full stress-energy tensor. The identification of retained TetB inventory with physical mass-energy is still open.

## 3. General invariant response target

Let q be internal dimensionless records, u=aᵀq the linearized physical lapse. Suppose the static Hessian is H(k)=CᵀLC+|k|²B, L,B positive, and kernel C=span(w). Matter couples to u through J=rho c². The response pole is

    u(k) = −J(k) (aᵀw)² / [(wᵀBw)|k|²] + regular terms.

This is independent of normalization of w and of any invertible coordinate change q=F q'. It follows by a Schur complement in a basis containing the zero direction, or generalized spectral decomposition. Hence

    G = c⁴/(4 pi) (aᵀw)²/(wᵀBw).

A static gapless susceptibility is not a causal propagation law. If the massless sector is larger, sum the residues using the gradient metric restricted to its kernel. Need prove actual microscopic gauge/constraint structure and universal overlap. Simply changing q's normalization can move a small factor between a and B, so claiming the exponent in a alone has no physical content. Only the ratio is invariant. No scale or value of G is fitted here.

## 4. The 17/13 stiffness test: covariance is not an invariant vector

The existing [collective optical closure](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/G_CLOSURE_DERIVATION.md) uses the face-pair space V=R⊕(R⁴⊗R⁴) with neutral capacity C_O=I17 and signed positive operator C_B=1⊕(I−swap). Unrestricted traces are 17 and 13. The ratio is forced if stiffness is the equally weighted full-space covariance read, not merely by tetrahedral symmetry.

For the actual time-face stabilizer C3, or S3 if reflections included, and full tetrahedral S4, project onto invariant vectors Q_G=mean rho(g), rho(g)=1⊕(P_g⊗P_g). Exact results:

| Read space | Tr Q | Tr Q C_B | neutral/signed trace ratio |
|---|---:|---:|---:|
| all vectors | 17 | 13 | 17/13 |
| C3 fixed | 7 | 5 | 7/5 |
| S3 fixed | 6 | 3 | 2 |
| S4 fixed | 3 | 1 | 3 |

The invariant vector space is not the full space of allowed invariant quadratic fluctuations or covariances. The full isotropic covariance still gives 17/13 and commutes with all these groups. But there are many invariant covariances; symmetry alone cannot fix it. This audit does not refute the algebraic ratio; it tells us that a physical scalar clock built only from invariant vectors does not automatically read the full trace. The microscopic task is to derive a full-space locked covariance or another physically justified work coefficient. In particular a scalar field coupling to the antisymmetric sector cannot be inferred from a trace without such a mechanism.

## 5. Finite-range obstruction in the prior three-grade constraint

Keep q=(q0,q1,q2,q3), u=q3, and C with rows (−t,1,0,0),(0,−t⁴,1,0),(0,0,−t¹⁶,1). Null vector w=(1,t,t⁵,t²¹). Prior root-only gradients gave three strictly local auxiliary responses. Test instead equal positive gradient stiffness kappa on all four records and equal penalties L>0 (illustrative, not derived), with ell=sqrt(kappa/L). The operator is kappa k² I+L CᵀC. If lambda_j and z_j are orthonormal eigenpairs of CᵀC, let W_j=|(z_j)_3|². W_0=t⁴²/(1+t²+t¹⁰+t⁴²), sum W_j=1. The exact potential of a point source is

    Phi(r)=−c⁴ M/(4 pi kappa r) [ W_0 + sum_(j=1..3) W_j exp(−sqrt(lambda_j) r/ell) ].

The static attractive force correction relative to the massless Newton part is

    R(r)=sum_(j=1..3)(W_j/W_0)(1+sqrt(lambda_j) r/ell) exp(−sqrt(lambda_j) r/ell).

Positive weights prohibit cancellations within this positive equal-gradient toy. At t²=alpha=1/137.035999177 (illustrative reference), 100-digit diagonalization gives W0=1.32835520568603e−45; massive eigenvalues 0.9999996142623388, 1.0, 1.0072977411376994, and weights approximately 4.34548e−22, 1, 6.41759e−35. The force correction is 2828.52 at r=100 ell and first falls below 1% at r>112.670865 ell. This is a dimensionless test, not a claimed experimental bound; physical ell is unassigned. A regularized point source or finite object modifies massive-mode form factors. The toy is linear and static, not a high-energy prediction.

The broad lesson: a residue as tiny as alpha²¹ is not enough. If the other channels propagate, their unsuppressed short-range responses can dominate long past their own characteristic decay lengths. If the time-face records are truly auxiliary constraints without spatial gradient terms, the contact limit avoids this particular exterior force. It then requires control of local self-energy and proof that eliminating the records from the real action is justified. Local gradients are not forbidden by the algebra of the prior model. This directs research toward the constraint sector of a metric theory rather than an assumed physical cascade.

## 6. Priority and criterion

Start from the actual paired time-face action, preserving the existing Triforce hierarchy. Derive the Hessian with respect to local time and spatial tetrad deformations; integrate out only demonstrably constrained or gapped variables; compute the invariant clock response above without choosing values from measured G. Show universal coupling to rest energy, no lower-order bypass, spatial lock gamma=1, and a consistent relativistic constraint structure. A static scalar calculation is not by itself an explanation of gravitational waves or instantaneous transport. Retain the distinction between drainless GR and the SST drained net-field response. The topological target remains (17/13) alpha²¹ hbar c/m_e², with proposed loop factor separate. This audit identifies specific obstructions to the earlier guessed construction; it does not establish the desired microscopic mechanism or derive G.

## Verification

Run `python verify_clock_constraint_audit.py` (SymPy, mpmath, NumPy, Matplotlib). 27 exact symbolic checks and 5 high-precision spectral checks passed, with numerical graph. No previous suite rerun, no native H36 rerun, no GitHub changes. The numerical experiment uses equal penalties and gradients without claiming that native dynamics selects them. Proof 26 unchanged.
