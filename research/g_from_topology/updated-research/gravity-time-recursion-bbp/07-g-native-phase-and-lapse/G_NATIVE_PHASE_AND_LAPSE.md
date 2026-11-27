# Native phase dynamics and the static lapse obstruction

Continuation of Proof 26 §7, CONSTITUTIVE_VERTEX.md, and G_NATIVE_INVENTORY_RESPONSE.md. No new Hamiltonian or fitted attenuation. All exact matrix results refer to the fixed-orientation six-complex-coordinate invariant sector of the existing 33-coordinate nonlinear vertex, at its symmetric saturation operating point where specified. They are not claims about the entire microscopic network or the physical mass map.

## 1. Relative phase is not a static clock deformation

Let x=(1/3,1,-4/15), Gm=[[3,-1,0],[-1,3,0],[0,0,1]], lambda=11/10, and use the matrices M+, C from Proof 26. Define the normalized bracket <v,w>=v^T Gm w/(x^T Gm x). In parity coordinates the balanced stationary vector is (x,0). The odd rotating-frame generator D=M+−2C−lambda I has entries [[−31/10,3/2,−2],[1/2,−1/10,1],[−7,5,−12]]. Its characteristic polynomial is (25 z^3+380 z^2+474 z−167)/25. Eigenvalues −13.7899587688, −1.69570952175, +0.285668290568. Since u is exchange-even, its linear odd perturbation vanishes; the linearized odd evolution is independent of F'' at this branch.

Add the same diagnostic differential energy delta(t) N_B as in the preceding note. After removing the common shift, i dot z=D z−delta x/2. With z=p+iq, dot p=D q, dot q=−D p+delta x/2. The occupations and phase of the projection onto x give delta N_B=−<x,p>, relative phase theta_B−theta_A=−2<x,q> to first order. This defines a collective phase read, not all individual tile phases. For harmonic forcing with convention exp(−i omega t),

p=(D²−omega² I)^−1 D x delta/2,
q=−i omega (D²−omega² I)^−1 x delta/2.

Set zeta=omega² and P=625 zeta³−120700 zeta²+351596 zeta−27889. Then

F(zeta)=<x,(D²−zeta I)^−1 x>=−(48125 zeta²−8627025 zeta+23957017)/(77 P),
A(zeta)=−<x,D(D²−zeta I)^−1 x>/2=−(36875 zeta²+1994575 zeta−6805751)/(154 P).

Thus theta_rel/delta=i omega F(omega²), delta N_B/delta=A(omega²). At zero, F=3422431/306779, A=−40753/25718. The phase has no static response and all three nonzero resonances contribute. For a suddenly applied constant small delta and zero initial perturbation, p=(I−cos Dt)D^−1 x delta/2 and q=sin(Dt)D^−1 x delta/2. A closed conservative system oscillates rather than relaxes; the static branch is the stationary response, not an asymptotic step response. The bounded linear phase excursions have no secular drift.

## 2. Exact static Hessian and phase Ward identity

For fixed chemical potential lambda, define the rotating-frame functional H−lambda n. In real/imaginary and even/odd coordinates its quadratic coefficient matrix (half the real Hessian, with a common normalization removed) has blocks Gm K, Gm D, Gm L, Gm D, with L=M+−lambda I and

K=L+(h/2) C x x^T Gm C/(x^T Gm x), h=F''(chi).

At h=308/59, det K=413/50, det D=167/25, rank L=2; hence rank of the real 12×12 Hessian is 11 and its sole null direction in this fixed orientation sector is the common phase i(x,0). It is indefinite, not an unconstrained positive energy minimum. At fixed norm the radial variation is removed; global orientation variations outside this sector are not audited here. The inverse common real response is <x,K^−1 x>=102694/170569, reproducing the inverse norm-frequency susceptibility from the preceding note. This is finite, not a massless scalar pole.

The differential load and the common norm load have zero projection onto the common phase null direction. More generally, if a differentiable source functional B(psi) is invariant under global U(1), differentiation gives DB(psi)[i psi]=0. This identity holds irrespective of the nonlinear gain and includes the Hamiltonian energy and occupation source. The constant phase degeneracy cannot couple to such a source at zero wavevector. In an extended analytic finite-range lattice, if that is the only soft branch at k=0, its eigenvalue is quadratic in |k| with nonzero stiffness, and the gapped complement remains invertible, its projected source is O(|k|); two insertions of the same source yield O(1), not a nonzero 1/|k|² monopole residue. This conditional no-go does not rule out an independent physical metric constraint, other soft modes, nonanalytic long-range kernels, or the separate scalar band-edge construction around a different state. It also does not say the common phase mode cannot propagate dynamically.

## 3. What happens when the existing Hamiltonian is expressed in proper time?

The exact canonical action of this candidate finite vertex in proper time is S=∫[i hbar/2(psi† dpsi/dtau−dpsi†/dtau psi)−E(psi)] d tau (in physical units once normalized). Substitution d tau=N dt gives S=∫[i hbar/2(psi† dot psi−dot psi† psi)−N E(psi)] dt. Thus a common lapse multiplies the entire Hamiltonian and cancels out of the symplectic term. At fixed N>0 and fixed occupation the normalized stationary shape is unchanged, while the coordinate-time generator frequency scales by N. Variation with respect to N gives −E, or with respect to u=ln N gives −NE, not the overlap or an inverse determinant. This is the ordinary universal energy coupling, but the finite action has no spatial metric kinetic/constraint term. Varying N in this action alone would impose E=0, not a gravitational Poisson equation. The physical rest energy normalization is not fixed by the dimensionless vortex Hamiltonian: adding a constant times occupation shifts energy and common frequency without changing internal relative dynamics, but changes a gravitational energy source if one promotes the energy to physical mass. A physical reference, not a convention for the isolated oscillator, must determine it.

In the inherited covariant time-leg theory, the missing geometric part already exists macroscopically and contains G. Its weak drainless reduced stiffness is c^4/(4 pi G) for u; this is not a derivation from the native Hamiltonian. The microscopic task is to derive its coefficient (including spatial intercell constraints and physical units) without importing G. The identity g=−c² grad ln N is exact for static observers, and the independent spatial metric must satisfy its own constraints. A local uniform time multiplier alone cannot produce spatial curvature.

## 4. Consequence for the G target

The old target G=(17/13) alpha^21 hbar c/m_e² requires the physical log-lapse susceptibility to have long-wave coefficient (4 pi hbar/(m_e² c³))(17/13)alpha^21. The exact native relative phase response is gapped, the common phase zero mode is source-dark at k=0, and the direct common energy read is finite in this sector. None yields that coefficient. This is a discriminating result, not a reason to install an arbitrary attenuation or new geometry. The next physically relevant object is the spatial metric constraint Hessian of a dimensionfully normalized, metric-dependent coupled-time-face action, with an actual energy source. Such an action is not supplied by the existing finite Hamiltonian; the existing covariant SST contains the target coupling already. A unique G cannot be computed from these equations alone. No inference of instantaneous propagation, no new proof number, no change to Proof 26.

Sources: https://github.com/fielddynamics/research/blob/main/proofs/recursive-field-closure-response/PROOF_26.md ; https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/vertex-research/CONSTITUTIVE_VERTEX.md ; https://github.com/fielddynamics/research/tree/main/proofs/sst-covariant-time-leg ; preceding local inventory response note.

Verification: OPENBLAS_NUM_THREADS=1 python verify_phase.py. 29 checks (24 symbolic, 5 independent matrix exponential step response comparisons); prior suites and full 33-coordinate/network dynamics not rerun. No Lean certification, empirical validation or GitHub writes.
