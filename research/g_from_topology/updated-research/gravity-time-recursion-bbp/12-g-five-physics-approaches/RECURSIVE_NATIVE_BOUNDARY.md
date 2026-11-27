# Recursive native Field Origin: boundary antiresonance and the clock read

November 2026 · Continuation of RECURSIVE_ORIGIN_CLOCK.md · exact finite algebra, conditional interface. Proof 26 unchanged.

## 1. Native geometry and boundary identification

The previous centroid construction gives the next stellated octahedron at scale 1/3: the eight face centroids of the central octahedron are the child cube corners. Reuse Stage IX H36, reconstructed from the actual 33 tile positions and the directional Field Origin. Let E be the 36×8 injection of the eight central faces, and F_s the existing four-tile injections indexed by stellation sign s. Let P_s=F_s(1,1,1,6)^T/sqrt(39) and P be the eight-column array. E†E=P†P=I8 and E†P=6I8/sqrt(39). These are different read spaces. The inherited optical filter is conditional; the fact that the centroid is a child vertex does not prove a Hamiltonian interaction. As the minimal explicit test use a reciprocal link −γ E_parent P_child† and its adjoint, with γ a real energy scale, not fitted to G. The signs can be reversed by a local basis phase. This involves all eight records at the internal interface, not eight new exterior links. There remain four external active ports. Other link laws could behave differently.

## 2. Exact native boundary resolvents

The eight sign characters split into degrees j=0,1,2,3 with multiplicities 1,3,3,1. In each character use p=P a/sqrt(8), e=E a/sqrt(8), where a is the ±1 character vector. Define g_p=p†(zI−H)^−1p, g_e=e†(zI−H)^−1e, g_m=p†(zI−H)^−1e. These are rational functions, with removable singularities interpreted by the restriction to the joint cyclic subspace (which excludes the port-dark zero-energy states). The verifier constructs the joint Krylov space and exactly solves its resolvent without fitting. The four dimensions are 3,4,3,2. All permutations within each grade give identical rational functions.

Write D0=z³+6z²−11z−24 and D1=z⁴+2z³−19z²−4z+32. The first two grades give:

| Grade | g_p | g_m | g_e |
|---|---|---|---|
|0|(13z²+15z−8)/(13D0)|6z(z+2)/(sqrt(39)D0)|z(z+3)/D0|
|1|(39z³−13z²−84z+32)/(39D1)|2z(3z²+z−8)/(sqrt(39)D1)|z(z²+z−4)/D1|

For both grades at zero: g_p=1/39, g_m=g_e=0; g_m′=−1/(2sqrt(39)), g_e′=−1/8. The other grade port responses are −5/13 and −3/13, with nonzero mixed responses −4/sqrt(39), −2/sqrt(39), respectively. Full rational expressions are printed in the verification log, with its port convention unnormalized (divide the pp entry by 39 and mixed entries by sqrt(39)). All of these are spectral susceptibilities of an indefinite Hamiltonian, not positive clock-energy stiffnesses. z=0 uses the specified energy origin and is not automatically a physical stationary frequency. In particular, the original full H has dark eigenstates at zero.

## 3. Exact recursive elimination

If level n has energy multiplier ε_n, use g^(n)(z)=g(z/ε_n)/ε_n. Let B_(n+1)(z) be the child outward port response after eliminating all still deeper children. The Schur complement adds γ_n² B_(n+1) to the face block of the effective parent Hamiltonian. The rank-one resolvent identity gives exactly, grade by grade:

B_n = g_p^(n) + γ_n² B_(n+1) (g_m^(n))² / (1 − γ_n² B_(n+1) g_e^(n)).

The terminal B_L=g_p^(L). Where the denominator is nonzero this is a scalar recurrence, not a new state variable. At z=0 the scalar and polar mixed responses and face self response vanish. Induction for every finite depth gives B_n(0)=1/(39 ε_n), independent of all deeper couplings and of depth. The leading child correction in these sectors is O(z²), with coefficient γ_n²/[156 ε_n⁴] B_(n+1)(0). This remains true for any finite nonzero positive ε_n. A uniform energy rescaling changes z and ε together, not the statement about the specified spectral reference. Direct exact nested matrices through three levels confirm the result, choosing ε_n=3^n and γ=1/sqrt(39) in the test's dimensionless units solely for illustration. At z=11/10 the child does change both port responses; this is a nonzero test frequency, not a claim that the linear Stage IX model has the nonlinear branch's stationary frequency. An infinite-depth limit with singular accumulation would need separate control.

## 4. The origin is not the port

In grades 0 and 1 the normalized central origin coordinate o couples to e with H_oe=−sqrt(8) and no other direct couplings. The resolvent equation gives R_oe=−sqrt(8)g_e/z, R_op=−sqrt(8)g_m/z, R_oo=(1+8g_e/z)/z. At z=0 these limits are 1/sqrt(8), sqrt(8)/(2sqrt(39)), 1/8, respectively, equal in both grades. For ε_n>0 divide all these zero responses by ε_n. Applying the same rank-one identity gives the modified parent central read

R̃_oo(0)=1/(8ε_n)+γ_n²/(312 ε_n² ε_(n+1)).

This is a nonzero local origin renormalization, identical for scalar and polar coordinates, while the external port response remains exactly unchanged. The deeper child levels do not multiply the effect: their outward port response is protected at this spectral reference. This is a precise antiresonance in the mixed read, not gravitational shielding or instantaneous signal transmission. At a generic nonzero z the equality and decoupling need not hold. The scalar/polar equality is not the metric equality of temporal and spatial potentials; these are amplitudes in a finite linear model.

## 5. Consequence for the G programme

The physical proper-time variable is u=ln N, and the prior lapse-action result gives δS/δN=−E for a physical energy expressed in proper time. Neither the present resolvent nor the older internal Hessian is the metric-gradient stiffness κ_N=c⁴/(4πG). The explicit recursion above cannot generate a product of twenty-one elementary gains in its static external scalar/polar read. It also contains no independently defined electromagnetic coupling, physical cell energy, metric-dependent link or map from the resolved child state to lapse. The geometric shrink factor 1/3 is not α. The protected mixed-response zero suggests a concrete constraint: deriving a metric-dependent inter-level junction and evaluating its response in the actual stationary state (including its physical energy reference) must precede an identification with G. A local common phase is source-dark in the previous fixed-orientation analysis; one must derive the clock metric variation, not simply identify a frequency or invert this boundary response. Keep the original G formula as the target, not a choice of γ or a fit to the spectral parameter. No independent derivation of G, a0, spin-2 propagation or general covariance is claimed.

Sources: [native Walsh read](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/NATIVE_WALSH_READ.md); [optical four-port resonator](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/OPTICAL_FOUR_PORT_RESONATOR.md); [Stage IX geometry and H](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/verify_coupled_origins.py); [Proof 26](https://github.com/fielddynamics/research/blob/main/proofs/recursive-field-closure-response/PROOF_26.md); prior local RECURSIVE_ORIGIN_CLOCK.md. No remote repository modification. Run `OPENBLAS_NUM_THREADS=1 python verify_recursive_boundary.py`. The 56 checks (including the numerical verification of centroid locations) are not 52 independent theorems. Full nonlinear vortex evolution and earlier suites not rerun.
