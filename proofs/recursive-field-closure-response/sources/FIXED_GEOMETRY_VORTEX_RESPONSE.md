# Fixed geometry, dynamical vortex response

**Status:** exact local response of the inherited balanced fixed-orientation stationary branch, with an explicitly introduced external overlap drive. Not a derivation of G or a new numbered proof.

## 1. Separate address geometry from state

The user proposes that closure changes the vortex, not the cube. Keep the Hadamard address operator W, the graph, the cross-chamber kernel C, and projective counts fixed. The vortex amplitudes ψ, registered overlap u=Re(A†CB), and nonlinear gain g(u)=F′(u)/2 evolve. A variable effective response does not require a variable combinatorial geometry. This does not rule out changes in physical metric or tetrad orientation; those are separate from address topology.

![Fixed geometry and moving state](figures/fixed_geometry_vortex.svg)

## 2. Native constrained stationary response

Use the existing CONSTITUTIVE_VERTEX.md and VERTEX_CURVATURE.md, not a new vortex. In the balanced fixed-z sector let x*=(1/3,1,−4/15), Gm=[[3,−1,0],[−1,3,0],[0,0,1]], f=225/1232, χ*=59/308, λ*=11/10. M=M_A+M_C and M_C are the inherited exact matrices in the verifier. L=M−λ*I; P projects Gm-orthogonally off x*. Let b=P M_C x* and A=−L+(I−P), positive definite. On the tangent the real Hessian (in the normalization of VERTEX_CURVATURE) is B_h=L+h f b bᵀGm, h=F″(χ*).

Introduce the external registered scalar drive j through H_j=H_t+2j u. This is a proposed work-conjugate coupling, not derived neighbor dynamics. In the rotating stationary equation the drive adds j M_C x. Differentiate the stationary equation and norm constraint at j=0. Projection removes the frequency derivative and gives B_h x′+b=0. Define k=f bᵀGm A⁻¹b=42815/290521. Sherman–Morrison yields

$$x'(0)=\frac{A^{-1}b}{1-hk},\qquad u'(0)=\frac{2k}{1-hk}.$$

Exact A⁻¹b=(−430,−296,−2960)/11319. In particular the central multiplicity coordinate changes, although every underlying geometric matrix is unchanged. The norm derivative is zero. This is a change in coherent amplitude, not a measured fluid throat radius or circulation. At h=308/59 (the constitutive example t=1), u′=5052170/3953719≈1.27783. The h=0 response is 85630/290521≈0.29475. At h_c=1/k=290521/42815 the branch has an additional soft direction and the linear response formula is singular; nonlinear analysis is required there.

![Response of the fixed kernel](figures/fixed_vortex_susceptibility.svg)

[Offline susceptibility explorer](interactive/fixed_vortex_response.html).

## 3. Closure force on this branch

For a differentiable branch at fixed norm the envelope identity is dH*/dj=2u*(j). If j=j(r), F_r=−2u*(j) j′(r) for this energy convention and a quasistatic conservative coupling. The curvature d²H*/dj²=2u′ is positive on this particular local **maximum** branch. Do not substitute a positive minimum-energy Green-action sign here. Attraction, distance dependence, coupling units and source normalization require the actual neighbor work term. Neither fixed cube nor a nonzero vortex response proves an inverse-square law or the determinant source α^21. No relaxation claim: the autonomous Hamiltonian can orbit rather than settle asymptotically. The calculation assumes a smoothly followed stationary branch in the specified sector.

## 4. Testable next distinction

Keep the underlying geometry identical and drive the vortex through the registered neighbor boundary state. Measure occupation, phase, overlap, circulation and work-conjugate response separately. A nonzero overlap response is established in this finite example; which vortex observable represents gravitational acceleration, whether a drain changes the throat, and whether an external drive preserves the collective sector are open. A physical read should derive j from the local field rather than prescribe it. The 1+4+16 Walsh counting remains fixed and is not a count of new physical vortices.

Run `python verify_fixed_vortex_response.py`. Prior verification suites are retained, not rerun.
