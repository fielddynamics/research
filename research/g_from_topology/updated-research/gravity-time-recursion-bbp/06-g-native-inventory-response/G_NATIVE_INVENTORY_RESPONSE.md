# Native inventory response of the coupled time faces

Continuation of Proof 26 §7 and `vertex-research/CONSTITUTIVE_VERTEX.md` and `ORDERED_RESPONSE_AND_DRAIN.md`. Exact results within their existing dimensionless stationary sector. No new Hamiltonian or fitted attenuation. The occupation probe is not yet physical mass; the eigenfrequency is not yet universal proper time.

## Matrices and solution

Use Gm=[[3,-1,0],[-1,3,0],[0,0,1]], x=(1/3,1,-4/15), lambda=11/10, M+ and C=MC as in Proof 26. Set M-=M+−2C. The inherited balanced branch has chi=59/308 and k=42815/290521. Set n=||psi||², g(u)=F'(u)/2, h=F''(chi); at n=1, g=1. The existing constitutive family gives h=2t/[chi(1+t)] (t is its saturation parameter, NOT electromagnetic transmission). All calculations follow the branch locally for 1−hk≠0 and nondegenerate eigenvalue in the fixed-orientation parity sector.

### Differential chamber probe

Add delta times the TetB occupation to the stationary energy, as a diagnostic external load. In the normalized parity basis its matrix is delta/2 [[I,-I],[-I,I]]. Subtracting its common identity shift, chamber exchange implements delta→−delta; u is exchange-even. Hence du/delta=0 at delta=0. Let R=(lambda I−M-)^-1, with det inverse denominator matrix = −167/25. Then R x = (−479/501,−1673/501,−2144/2505). Let <v,w>=v^T Gm w/(x^T Gm x). The odd amplitude derivative is −R x/2 in coordinates where the even vector is x. Define c=<x,Rx>=−40753/12859. The eigenvalue of the *fixed-g* problem has expansion lambda(g)+delta/2+c(g) delta²/4+O(delta⁴). The stationary physical energy W (not the generator eigenfrequency) has W(delta)=W(0)+delta/2+c delta²/4+O(delta⁴), because the self-consistent state is stationary. Thus N_B=1/2+c delta/2+O(delta³). Legendre transforming along this branch gives constrained energy curvature −2/c=25718/40753 with respect to N_B. This is a local dimensionless curvature, not continuum clock stiffness or proof of full-state stability.

The derivative of c(g) at g=1 is 2<x_g,Rx>−<Rx,(lambda' I+C)Rx>, with x_g=A^-1 b_* and lambda'=2chi. Exact result c'=22223198598/8102340169. The fixed-g overlap follows by Feynman–Hellmann u=(1/2)partial_g lambda(g,delta). Self-consistency dg=(h/2)du and partial_g u=2k give

u(delta)=chi + [c'/(8(1−hk))] delta²+O(delta⁴).

For t=1 this coefficient is 655584358641/441061076764 = 1.48637998948. An exchange-odd occupation imbalance is not the same as an even positive mass source.

### Common occupation probe (no extra term in H)

For psi=sqrt(n) v with ||v||=1, let chi(g)=v(g)^*Vv(g)/2. The exact local stationary system is u=n chi(g(u)), lambda=lambda(g(u)), chi'(1)=2k, lambda'(1)=2chi. Differentiate at n=1:

du/dn=chi/(1−hk), dlambda/dn=h chi²/(1−hk).

At t=1 both derivatives equal 170569/205388. On the subcritical branch h>0 and hk<1, frequency increases with n. Energy envelope derivative dW/dn=lambda by constrained stationarity; hence its local curvature is dlambda/dn. This tests a physical-clock identification: identifying N=lambda(n)/lambda(1) would give an increasing lapse with occupation, opposite to the exterior redshift of a positive mass if n is assumed larger near matter. It is also not universal across all transitions. Neither inversion of the clock read nor choosing a fitted sign constitutes a derivation. Total occupation is conserved in isolated dynamics; varying n compares distinct stationary states, not spontaneous evolution.

## Gravitational normalization verdict

The actual local Hessian has an order-one response, and the constitutive parameter h remains variable with unchanged geometry and witness. Neither alpha nor physical lattice spacing nor a physical metric read occurs in these equations. Their solution cannot uniquely yield (17/13)alpha^21. Even calibrating alpha separately does not determine the map from these occupation/overlap changes to proper time or the coefficient of its spatial gradient energy. Uniform lapse multiplication of H changes coordinate-time frequencies but leaves the normalized local stationary branch unchanged. The prior covariant time-leg identity g=−c² grad ln N remains exact in the static limit, but does not determine N from this Hamiltonian. The missing physical equation is the metric variation of the native action: delta H/delta e^0_0 (including spatial intercell terms and their dimensionful normalization). No new determinant, no new oscillator, no Proof 26 change. The exact local curvatures above are inputs for that reduction, not replacements for it.

## Verification

Run `OPENBLAS_NUM_THREADS=1 python verify_native_load.py`. Exact SymPy identities and independent six-dimensional generalized eigensolves with self-consistent nonlinear gain (three subcritical operating points), plus common norm branch tests. 43 assertions pass; finite differences use dimensionless loads and the norm derivative is evaluated with step 1e−6 (larger steps near the curvature threshold are less accurate). No full 33-coordinate simulation, prior-suite rerun, Lean check, empirical validation or remote write. Sources: https://github.com/fielddynamics/research/blob/main/proofs/recursive-field-closure-response/PROOF_26.md and https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/vertex-research/CONSTITUTIVE_VERTEX.md .
