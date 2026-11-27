# Coupled time-face constraint: recursive clock susceptibility and G

Continuation of `G_TIME_FACE_LAPSE.md` and `G_NATIVE_CLOCK_UNIVERSALITY.md`. Exact mathematical results for a proposed static quadratic reduction, not a new physical derivation of G. The native H36 and Proof 26 are unchanged. No new geometric object is introduced.

## 1. Physical target and the spatial metric

The repository's [SST time-leg proof](https://github.com/fielddynamics/research/tree/main/proofs/sst-covariant-time-leg) identifies the physical lapse N in a static metric. Put u=ln N=Phi/c². The acceleration of an initially comoving free test body relative to the static observers is −c² D u, where D denotes the spatial gradient. A uniform offset in u is a time normalization, not gravity. Ordinary weak-static minimally coupled rest energy contributes +rho c²u to the energy functional (−rho c²u to the Lagrangian). Relativistic stress and dynamical matter require the full metric action.

For the weak static drainless limit, write ds²=−e^(2u)c²dt²+e^(−2v)delta_ij dx^i dx^j. The zero-shift static Einstein-Hilbert integrand is N sqrt(h) R^(3), up to boundary terms. The spatial scalar curvature is R^(3)=e^(2v)(4 Delta v−2|grad v|²). Integrating by parts gives the static energy to quadratic order, with fixed boundary values,

E_GR = c⁴/(8 pi G) integral (2 grad u·grad v − |grad v|²) d³x + integral rho c²u d³x.

Varying v gives Delta(v−u)=0, hence v=u under homogeneous difference boundary conditions and negligible spatial stress. The stationary reduction gives the positive scalar gradient energy c⁴/(8 pi G) integral |grad u|². This is a stationary constraint elimination, not minimization over v: the pre-elimination scalar functional is indefinite. It is the weak-static result of the metric theory, not proof that the native time face creates this action. In particular an independent wave equation for u would add degrees of freedom absent from the GR lapse constraint. The result specifies the spatial response that any microscopic clock model must match.

## 2. Three collective constraints, no additional geometry [conditional construction]

Proof 26 defines three invariant contrast grades of dimensions 1,4,16. For the stated diagonal gain bridge with elementary real amplitude t>0, the determinant lines of the three grades carry factors t, t⁴, t¹⁶. The exterior power of a direct sum factors as a tensor product of the three top exterior powers; the product of the three determinants is t²¹. This is algebra; it does not imply a physical cascade or time order.

Test a static model in which q0 is a gapless collective reference and q1,q2,q3 are three scalar records, with u=q3 the *physical* log lapse. These are proposed effective coordinates, not extra geometric objects or already identified native H36 variables. The assumed settlement energy is

E = integral [ kappa0 |grad q0|²/2 + L1(q1−t q0)²/2 + L2(q2−t⁴q1)²/2 + L3(q3−t¹⁶q2)²/2 + rho c² q3 ] d³x,

where kappa0>0 has units J/m and L_i>0 have units J/m³ for dimensionless q. The three constraints have rank three, and their exact null vector is v=(1,t,t⁵,t²¹). Thus this model has only one gapless static channel. It is invariant in its free part under a uniform shift along v, with the physical boundary clock normalization fixed. The mass source changes by a field-independent constant under that shift. It is not a generally covariant action.

This construction is motivated by the determinant grades; it does not derive the three constraints or t from the time-face geometry. It demonstrates what happens *if* the physical lapse is selected only at the completion of the collective settlement.

## 3. Exact elimination, including the local deformation

Define z1=q1−t q0, z2=q2−t⁴q1, z3=q3−t¹⁶q2. The transformation (q0,q1,q2,q3)→(q0,z1,z2,z3) is unimodular. Its inverse gives

u=q3=t²¹ q0+t²⁰ z1+t¹⁶ z2+z3.

In Fourier space at nonzero spatial wavevector k, the energy Hessian in these coordinates is diag(kappa0 |k|²,L1,L2,L3). For source J=rho c², solve the stationary equations. The exact lapse response is

u(k) = −J(k) [ t⁴²/(kappa0 |k|²) + t⁴⁰/L1 + t³²/L2 + 1/L3 ].

The last three terms are contact contributions: for constant local coefficients and no gradients on the residual coordinates, they have support only on the source in position space. They may matter for interior stability and self energy. They do not create an extra exterior 1/r field. On disjoint supports the cross interaction after elimination is exactly −c⁴ t⁴² M1 M2/(4 pi kappa0 r) for point masses, or the corresponding Newton kernel for distributed masses. Boundary conditions: asymptotically fixed clock, or suitable Dirichlet Green function; zero mode handled separately. For the open-space weak exterior, G=c⁴ t⁴²/(4 pi kappa0). The inverse-Laplacian sign gives slower clocks near positive mass. The linear model is not a strong-field solution.

The key result is that the suppression applies to the **pole residue**, not the absolute rate of a clock, and not necessarily to the local response in matter. A constant absolute attenuation would cancel on normalizing clocks. Here the collective constraints instead set how strongly the physical clock overlaps the gapless response. The source and test each couple via the same terminal coordinate.

## 4. Robustness to gradient terms and the bypass obstruction

With an arbitrary positive gradient matrix B on the four coordinates, the Hessian in Fourier space is A(k)=Cᵀ L C + |k|² B, where C is the 3×4 constraint matrix and L positive definite. Its rank-three constant part has kernel span(v). Since the other eigenvalues are positive, the inverse satisfies

lim_(k→0) |k|² A(k)^−1 = vvᵀ/(vᵀ B v).

This follows by orthogonal splitting into the one-dimensional kernel and its complement and taking the Schur complement; all off-diagonal gradient blocks are O(k²). With terminal read e3, the long-range coefficient is t⁴²/(vᵀ B v). For B=kappa I, vᵀ B v=kappa(1+t²+t¹⁰+t⁴²). This is a different prefactor from the root-only model; the massive branches can give finite-range corrections. Their masses are not computed for a physical time-face model. In the semidefinite root-only case the same pole is exact by the change of variables in section 3.

If matter sees u=b0 q0+b1 q1+b2 q2+b3 q3 instead, then the massless pole numerator is (b0+b1 t+b2 t⁵+b3 t²¹)². Any fixed nonzero lower-grade read generically gives a lower power of t and overwhelms the proposed alpha²¹. This is a strong microscopic selection test. It is not enough that a complete determinant channel exists: the physical matter coupling must avoid all lower-grade long-range bypasses (or enforce exact cancellations). Direct ordinary linear source coupling in the native H36 has not been shown to satisfy this test.

## 5. G normalization without hiding a fit

With t²=alpha, Gm_e²/(hbar c)=alpha²¹ m_e² c³/(4 pi hbar kappa_eff), where kappa_eff=vᵀ B v (kappa0 in the root-only model). Define kappa_e=m_e² c³/(4 pi hbar). Then the inherited tree-level GFD target is equivalent to kappa_eff=(13/17) kappa_e. The constraint model does not derive that stiffness ratio, the electron scale, or the elementary t²=alpha. Choosing them to reproduce the target would be circular. With the equal-gradient example even the dimensionless denominator differs from 13/17. The loop correction is independent and remains open.

For the physical log lapse the reduced stiffness is kappa_eff/t⁴². This must equal c⁴/(4 pi G) to match the weak-static Einstein scalar constraint. Do not insert this as a new measured G and claim an independent microscopic prediction. The spatial metric constraint must also follow from the same physical action; the scalar toy alone cannot predict lensing or covariant dynamics.

## 6. Native proof gates

1. Derive the three effective constraints from the already existing paired time-face addresses and the actual native vortex action. Exhibit a gapless collective reference and identify the physical lapse, rather than installing a sequence of independent attenuators. The three Walsh grades are not necessarily serial physical stages.
2. Derive the no-bypass condition for universal matter coupling; distinguish mass-energy registration from occupation, charge and circulating amplitude. It must survive composition of Field Objects, including binding energy. The exponent belongs to the universal response, not every enclosing closure.
3. Derive the physical gradient stiffness, its 13/17 normalization and elementary electromagnetic intensity from the same action. No geometric count alone forces a physical energy coefficient.
4. Recover the weak drainless metric constraint, then the existing SST drained/net-field rule and covariant completion, without adding an unobserved scalar gravitational degree of freedom. A static pole is not a signal propagation law.

## Reproduce

`OPENBLAS_NUM_THREADS=1 python verify_time_face_constraint.py` (SymPy, NumPy, Matplotlib). 23 exact algebra checks pass, including the rational adjugate pole verification for a nontrivial gradient matrix, exact contact response, bypass test and normalization identity. The diagram shows the conditional constraint, not measured dynamics. Prior H36 simulation and previous suites not rerun; no empirical validation, no remote edits, no Proof 26 change.
