# BBP, native exchange and the information curvature of recursive settlement

November 2026 | Additive GFD research; Proof 26 unchanged. Exact identities and finite native-sector tests; physical read and normalization open.

## 1. Existing sources

- [BBP ladder, Part III](https://github.com/fielddynamics/research/tree/main/proofs/bbp-coupling-polynomial-ladder): octahedral pole geometry and BBP closure.
- [Ordered response](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/vertex-research/ORDERED_RESPONSE_AND_DRAIN.md): exact invariant native two-amplitude sector.
- [Vertex factorization](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/vertex-research/VERTEX_FACTORIZATION.md): explicit row, column and transpose kernels.
- [Constitutive vertex](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/vertex-research/CONSTITUTIVE_VERTEX.md): F_t and finite vacancy cost.
- Prior local `BBP_CORE_SETTLEMENT.md` and `RECURSIVE_NATIVE_BOUNDARY.md` reopened. The latter gives the two exact port resolvents reproduced below. No remote changes.

## 2. Exact BBP rotation

For e=x−1 and theta=2 atan(e), R=(1−2e−e²)/(1+e²)=cos(theta)−sin(theta). On the real branch R>0 containing theta=0,

S(theta)=pi+2 theta+2 ln R.

S(−pi/2)=0, S(0)=pi, S'(0)=0, S''(0)=−4, so the x-coordinate curvature is −16. The original BBP integration path is −pi/2≤theta≤0; positive theta near zero is an analytic continuation, not the digit extraction interval. The candidate R can exceed one on the original interval; it is not itself a passive probability.

## 3. Exact realization in the existing nonlinear Hamiltonian

In Stage VII, take an outer symmetric row- and column-zero array v, with central entries zero and unit norm. The exact common eigenspace has dimension two. With H_l v=v and C v=−v/2, set A=a v, B=b v. The registered overlap u=−Re(a* b)/2 is conserved. Thus Omega=−g(u)/2 is constant on the orbit, and i a_dot=a+Omega b, i b_dot=b+Omega a. Define X=2Re(a* b), Y=2Im(a* b), Z=|a|²−|b|². Then X is constant, Z_dot=2Omega Y and Y_dot=−2Omega Z. For real unequal initial amplitudes with nonzero product, Y(0)=0, Z0≠0 and generally Omega≠0. For theta=2Omega t,

Z/Z0=cos theta, Y/Z0=−sin theta; (Z+Y)/Z0=R.

The read is a chosen coherent projection, not a measurement derived from the vertex. It is undefined at Z0=0, the balanced state. Under time reversal Y reverses, so (Z−Y)/Z0 is the companion read. This sector is dark at the origin and to the row-sum filtered ports; the full interface and a nonlinear metric read are not tested here. The invariants n and u make H=n+F_t(u) constant. Therefore the nonconstant BBP deficit cannot be the native mechanical energy along this orbit, and its curvature cannot be substituted as a native energy Hessian. This is an exact obstruction, not an objection to BBP mathematics.

## 4. Even settlement and relative entropy

For |theta|<pi/4 both R_±=cos theta±sin theta are positive. Their squares sum to 2. The normalized squared quadrature records p_±=R_±²/2=(1±sin 2theta)/2 have sum one; they are mathematical probabilities of these normalized real read coordinates, not actual chamber occupation probabilities. Averaging the two BBP reads gives

D=pi−[S(theta)+S(−theta)]/2=−ln cos(2theta)
 = D_KL((1/2,1/2)||(p_−,p_+)).

Writing b=sin 2theta, D=−(1/2)ln(1−b²). This is precisely the average of the analytic continuations W(b)=−b−ln(1−b) and W(−b), not a claim that a negative vacancy is physical. The existing one-sided cost is defined for b≥0. D=2theta²+O(theta⁴), D''(0)=4. If N were the geometric mean of the two candidate clock reads, ln N=−D/2, with no first-order clock response around the symmetric state. Neither that read nor the dimensionful energy multiplying D has been established. For an exactly symmetric differentiable read, a perturbation theta proportional to a small load cannot provide a linear Newtonian source through this even response. A nonzero background, nonanalytic mapping or different invariant read would require independent derivation. This does not rule out the full theory.

## 5. Native boundary response and imaginary frequency

From the prior exact H36 resolvent, p0=(13z²+15z−8)/(13(z³+6z²−11z−24)), p1=(39z³−13z²−84z+32)/(39(z⁴+2z³−19z²−4z+32)). At the inherited energy reference both equal 1/39 but their derivatives differ: −7/117 versus −5/78. Therefore log(p0/p1)=z/6+2z²/9+O(z³). Under z=i omega the phase starts at omega/6 and log modulus at −2omega²/9. Real coefficients enforce conjugate symmetry and zero first-order modulus variation there. This is not BBP's linear phase–log cancellation. The coherent projection in §3 gives the exact algebra but does not establish it as an outward port response. The spectral reference is not yet the physical gravitational static limit.

## 6. Consequence for G

The BBP angular curvature measures a normalized information defect. The native exchange demonstrates how the two quadratures can exist without a new oscillator; it does not dynamically select their read, physical clock, or a cost. The proper-time action couples to energy, not to an arbitrary dimensionless information functional. Inserting a multiplier equal to the desired stiffness or identifying 16 with a gravitational action prefactor would be circular. The actual recursive inter-level metric work and physical reference must fix the invariant lapse susceptibility independently. No alpha^21, 17/13 or G derivation is claimed. A particularly useful next discriminant is whether a recursive child coupled through the existing eight face records can make this dark-sector quadrature observable in a time-reversal-even energy read without selecting an arbitrary projection. That has not been calculated here.

## Reproduction

`OPENBLAS_NUM_THREADS=1 python verify_bbp_native_rotation.py`

63 assertions passed (exact symbolic identities and six independent integrations of the existing two-amplitude nonlinear equations, with orbit and energy checks). Native Stage VII blocks rebuilt and dark eigenspace checked exactly; H36 rational port responses reused from the earlier verified boundary calculation. No full-network simulation, earlier-suite rerun, Lean proof, empirical validation or repository write.
