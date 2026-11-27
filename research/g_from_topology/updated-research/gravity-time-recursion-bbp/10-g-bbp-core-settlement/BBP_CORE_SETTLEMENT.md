# BBP core closure: phase, logarithmic response and recursive stiffness

Conditional research continuation; Proof 26 unchanged. Sources inspected: [BBP ladder](https://github.com/fielddynamics/research/tree/main/proofs/bbp-coupling-polynomial-ladder), [PI sweep gravity bridge](https://github.com/fielddynamics/research/blob/main/research/unified-closure-action/pi_sweep_extension/PI_SWEEP_GRAVITY_BRIDGE.md), [PI Walsh read](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/PI_WALK_FWHT.md). The inherited BBP proof selects a rational integrand using its stated pole, formula-class and closure premises; its other poles are not all octahedral lattice points.

## Exact decomposition

For x in a neighbourhood of [0,1] with x < sqrt(2), let S(x) be the integral from 0 to x of (4-2y^3-y^4-y^5)/(1-y^8/16). Exact cancellation gives S' = 16(x-1)/[(x^2-2)(x^2-2x+2)]. Integration yields

    S(x) = pi + 4 atan(x-1) + 2 ln R(x),
    R(x) = (2-x^2)/(x^2-2x+2).

At x=1, S=pi, S'=0, S''=-16, S'''=-64. The angular and logarithmic derivatives are +4 and -4, respectively. All of the second derivative comes from the logarithmic piece. Thus pi-S has a strict local minimum and expands as 8 e^2 + (32/3)e^3 + O(e^4), e=x-1. This is a dimensionless read curvature, not a physical energy Hessian. Multiplying by an arbitrary energy changes its physical stiffness.

Equivalently Z=(2-x^2)/(1+i(x-1))^2 has |Z|=R and continuous arg Z=-2 atan(x-1). Then S=pi+2 ln|Z|-2 arg Z. Z(1)=1 and Z'(1)=-2-2i. The first-order phase-amplitude cancellation is exact. This constructed complex transfer is not the native vortex propagator.

## Clock interpretation and test

The logarithmic lapse is u=ln N. A candidate N=R(x) would yield u'(1)=-2 and u''(1)=-8. Thus for positive small e the candidate clock slows. But x is the BBP integration variable, not a derived physical inventory variable; this identification is only a diagnostic. The total S itself is quadratic, so it cannot be a linear universal source around closure without a different variable or nonanalytic map. BBP alone supplies no stress-energy coupling or gradient stiffness.

## Nested geometry

For a physical perturbation whose normalized BBP coordinate error scales by the centroid factor 1/3, set x_n=1+3^(-n)e. The pulled-back read curvature of pi-S is 16*9^(-n). Consequently the leading error contracts by 1/9 per level. This is conditional on that error transport, not implied by the nested geometry. If read defects were independent additive energies with equal energy scales, their sum converges with factor 9/8. If energies instead scale inversely with radius, each term scales by 3^(-n), giving factor 3/2. Neither gives alpha^21. BBP base 16 digit shifts and spatial centroid contraction 1/3 are distinct operations.

## Physical next test

Use the actual central-face to child-port response to derive a physical coordinate whose amplitude/phase variation obeys the displayed identity, or demonstrate that it does not. The BBP poles are complex in an integration variable; the resolvent of the Hermitian native Hamiltonian has real spectral poles. They cannot be identical in the same variable. A discrete-time rotation, complex frequency map or other physical transduction must be derived, not chosen to match the integral. A clock interpretation additionally needs an invariant lapse gradient stiffness and energy source. No G derivation, no fit and no native network rerun are claimed.
