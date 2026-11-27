# Five algebraic investigations of the recursive BBP Field Origin

November 2026 · Additive GFD research · One assistant, five separate analytical approaches, not independently executed agents. Proof 26 unchanged.

## Sources and scope

This continuation reuses the exact source snapshots [`RECURSIVE_NATIVE_BOUNDARY.md`](../09-g-recursive-native-boundary/RECURSIVE_NATIVE_BOUNDARY.md) and [`BBP_NATIVE_ROTATION.md`](../11-g-bbp-native-rotation/BBP_NATIVE_ROTATION.md) from the preceding packages, and the inherited Stage IX 36-coordinate geometry in `native_geometry.py`. Upstream: [BBP ladder](https://github.com/fielddynamics/research/tree/main/proofs/bbp-coupling-polynomial-ladder), [Proof 26](https://github.com/fielddynamics/research/blob/main/proofs/recursive-field-closure-response/PROOF_26.md), [ordered time-face exchange](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/vertex-research/ORDERED_RESPONSE_AND_DRAIN.md), [native geometry](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/verify_coupled_origins.py). The linear Stage IX Hamiltonian differs in weights from the nonlinear Stage VII vertex. Do not silently identify their generators. The inter-level link is the already proposed reciprocal E-parent/P-child interface. It is not uniquely forced by centroid geometry.

## A. Mathematical physics: exact depth dependence and analytic fixed point

For each scalar or polar grade, the existing recurrence is

    F_n(B)=p_n+gamma_n^2 m_n^2 B/(1-gamma_n^2 e_n B).

Its exact difference is

    F_n(A)-F_n(B)=gamma_n^2 m_n^2(A-B)/[(1-gamma_n^2 e_n A)(1-gamma_n^2 e_n B)].

Use the inherited rational functions p,m,e from the previous boundary note. Both grades have p(0)=1/39, m(0)=e(0)=0 and m'(0)=-1/(2 sqrt(39)). In physical energy units q_n(z)=q(z/epsilon_n)/epsilon_n for each q=p,m,e. Define B^[d] as the root response of levels 0 through d inclusive, with no deeper child. For nonzero finite couplings and positive finite energies, repeated application of the exact difference identity gives

    B^[d](z)-B^[d-1](z)
      = z^(2d)/(39 epsilon_d) product_{i=0}^{d-1}[gamma_i^2/(156 epsilon_i^4)] + O(z^(2d+1)).

Reason: at level d-1 compare a child with no child; its leading difference is p_d(0)=1/(39 epsilon_d), multiplied by m_{d-1}^2. Each preceding junction multiplies by another second-order zero. All denominators equal one at z=0. This establishes the first nonzero correction and its coefficient, not only a bound. Both grades share the coefficient. Verified exact through d=4, for unit coupling and for gamma_i=3^i, in units epsilon_0=1.

If epsilon_i=epsilon_0 3^i, gamma_i=g epsilon_i (a self-similar scaling assumption, not a derived coupling), then

    B^[d]-B^[d-1] = [1/(39 epsilon_0)] (g^2/156)^d 3^(-d^2) (z/epsilon_0)^(2d) + O(z^(2d+1)).

The d^2 exponent follows from 2 sum_{i<d} i+d=d^2. This leading Taylor coefficient decays faster than exponentially in depth. It is not a uniform-in-z estimate by itself.

For that scaling, write b(w)=epsilon_n B_n(epsilon_n w). The infinite self-similar boundary equation is

    b(w)=p(w)+(g^2/3)m(w)^2 b(w/3)/[1-(g^2/3)e(w)b(w/3)].

For any fixed finite g, choose a small closed disk |w|<=r with p,m,e holomorphic and a sup-norm ball of holomorphic functions bounded by M>1/39. Since m,e vanish at zero, r can be made small enough that |(g^2/3)e(w) b(w/3)|<=1/2 throughout the ball, the image is bounded by M, and the difference identity gives Lipschitz constant <=4(g^2/3)sup|m|^2<1. Banach's theorem then gives a unique analytic fixed point in this ball and convergence of finite truncations starting from p. In particular b(0)=1/39. This resolves the possible singular-depth concern locally for the stated scaling. No assertion of global convergence or of a physical static operating frequency. No alpha is present.

## B. Vortex dynamics: exact dark sector persists under recursion

On the 12 ordered off-diagonal face-pair addresses let R and Q be row and column sums and T transpose. The space V=ker R intersect ker Q intersect ker(T-I) has dimension two. The Stage VII constitutive vertex's native exchange sector uses this space. Independently reconstruct Stage IX H36: embed V in each chamber's lateral sites via the actual face labels, producing a 36x4 injection J. Exact computation gives

    H36 J = J [[I2,-I2],[-I2,I2]], E^T J=P^T J=0.

The two eigenvalues 0 and 2 each have multiplicity two. On any finite nested network with links of the form -gamma E_n P_(n+1)^T/sqrt(39) plus adjoints, a copy of J supported on one cell remains an invariant block and has zero central or filtered read. This follows directly from both annihilation identities; no depth-dependent perturbation can illuminate it through those links. The verifier checks each block for networks of two, three and four cells. An added excitation in the positive eigenvalue sector changes the dimensionless linear Hamiltonian energy at fixed exterior port history. This is a counterexample to universal energy registration by the existing filtered linear read; it is not an assertion that a physical mass has been created. The Stage VII nonlinear globally dependent gain may couple other perturbations and is not ruled out by this linear result. A full interface or a derived nonlinear work read could expose the mode.

## C. Statistical physics: exact BBP odds and constitutive distinction

For the previous BBP quadratures R_±=cos(theta)±sin(theta) in the positive branch, p_±=R_±^2/2 and b=sin(2theta). Define v=(1/2)ln(p_+/p_-)=atanh b. Then p_±=exp(±v)/(2 cosh v), so p_+=mu(exp(2v)) with the existing mu(x)=x/(1+x). The BBP paired KL deficit is exactly

    D=-(1/2)ln(1-b^2)=ln cosh v,
    dD/dv=tanh v, d²D/dv²=sech² v.

Thus the same odds normalization is present, but the paired cost and the one-sided W(b)=-b-ln(1-b) are not the same work law: D'(b)=b/(1-b²), W'(b)=b/(1-b), difference b²/(1-b²). They coincide at quadratic order near b=0 only. In a symmetric state, using the geometric-mean clock read gives ln N=-D/2, with zero linear derivative. An even read needs a nonzero background or another independently derived mechanism to supply a linear clock response. These are mathematical read probabilities, not measured chamber occupancies. An entropy functional is not physical energy without a conversion law.

## D. Recursive information theory: 21 constraints do not imply 21 powers of attenuation

If the 21 independent contrast directions each carry complementary BBP reads, their product probability register has KL divergence from the balanced product equal to the sum of the individual divergences:

    D_total = -(1/2) sum_{j=1}^{21} ln(1-b_j²).

At the balanced state its Hessian is I21; along a uniform displacement b_j=b, the second derivative is 21. This conditional product-register calculation establishes additive logarithmic curvature, not alpha^21 in the physical linear susceptibility. A determinant of the full register measures a different observable. The assumed 21 independent BBP pairs are not derived from native amplitudes. The earlier 1/4/16 contrast structure and inherited 17/13 ratio remain unchanged; nothing here turns their counts into work coefficients.

## E. Relativity and normalization: the invariant missing metric variation

Let q be a collective deformation, u=ln N=a q the physical clock read at linear order, and kappa the coefficient of |grad q|²/2. The proper-time matter source is rho c² a q. Elimination in Fourier space gives

    u(k) = -rho(k)c² a²/(kappa |k|²),
    G = c⁴ a²/(4 pi kappa).

Under q'=lambda q the coefficients transform a'=a/lambda and kappa'=kappa/lambda², so a²/kappa is invariant. Changing the physical stiffness by a factor without changing the clock and matter units changes G by the reciprocal factor. The finite dimensionless vortex, BBP odds, and boundary equations contain neither a native electromagnetic alpha nor an independent metric-gradient normalization. A common energy shift of the isolated Hamiltonian also changes the zero used by the resolvent; its specified z=0 is not established as the gravitational static reference. Hence the existing equations alone do not fix the target invariant susceptibility (4 pi hbar/(m_e² c³))(17/13) alpha^21. One must establish a physical metric-dependent energy of the inter-level junction, and show that its variation registers the dark-sector energy as well. The fixed-point depth law is a genuine recursive algebraic result; it cannot be used as a numerical fit for G.

## Verification

Run `OPENBLAS_NUM_THREADS=1 python verify_five_approaches.py`. 52 passing checks: exact matrix invariance, rational formal Taylor coefficients, odds identities, register Hessian and coordinate normalization. The local analytic fixed-point proof is given in the text. No full nonlinear network simulation, previous-suite rerun, independent agent execution, Lean certification, empirical validation or repository write.
