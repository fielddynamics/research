# AQUAL from Field Origin settlement — research extension

**Status:** exact conditional vector reduction, new obstruction tests, and independent numerical checks of the inherited native stationary branch. This is a research note, not a numbered physical proof, a derivation of the native SST action, or a claim of an independently established gravitational mechanism.

## 1. Starting points (existing repository)

- [AQUAL energy proof](https://github.com/fielddynamics/research/tree/main/proofs/aqual-energy-functional): F(y) = y − 2√y + 2 ln(1+√y).
- [Constitutive vertex](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/vertex-research/CONSTITUTIVE_VERTEX.md): scalar vacancy cost W(b) = −b − ln(1−b), nonlinear overlap gain, and the stability bound. This scalar duality is inherited, not a new result here.
- [Fixed geometry vortex response](https://github.com/fielddynamics/research/blob/main/proofs/recursive-field-closure-response/sources/FIXED_GEOMETRY_VORTEX_RESPONSE.md): exact native three-coordinate stationary sector and susceptibility.
- [Forced tetrahedral frame](https://github.com/fielddynamics/research/tree/main/proofs/forced-tetrahedral-frame), [Walsh modes](https://github.com/fielddynamics/research/tree/main/proofs/walsh-eigenmodes-of-the-cube), and [NET Field rule](https://github.com/fielddynamics/research/tree/main/proofs/net-field-rule).

## 2. Conditional vector completion

Write **x** = ∇Φ/a₀, x = |**x**|. The dimensionless target is

    A(x) = F(x²)/2 = x²/2 − x + ln(1+x).

For an internal response **p** in the open unit ball, choose the candidate work law

    E(**x**, **p**) = |**x**|²/2 − **x**·**p** + W(|**p**|),
    W(r) = −r − ln(1−r).

The scalar cost comes from the earlier work; its collective radial lift and the bilinear external work term are assumptions to test, not consequences of the native Hamiltonian. The vector is an auxiliary algebraic response, not an extra dynamical oscillator. Its physical identification with native coordinates remains open.

Since ∇_p W = **p**/(1−|**p**|), the unique minimizer is **p**_* = **x**/(1+x), with Hessian eigenvalues 1/(1−r) (twice) and 1/(1−r)². The boundary cost diverges as r → 1, ensuring the stationary minimum is interior. The reduced energy is A(x). Its derivative is

    ∇_x A = **x** − **p**_* = μ(x)**x**,    μ(x)=x/(1+x).

Note |**p**_*| = μ(x), but |**p**_*|/x = 1−μ(x) for x>0. The response is not directly the fractional chamber inventory. In physical acceleration units a₀**p**_* is the complementary acceleration vector in this gradient convention. Physical acceleration is −∇Φ.

For a fully open field, restore units in the functional

    I[Φ] = ∫ [a₀² A(|∇Φ|/a₀)/(4πG) + ρΦ] d³r.

Varying Φ with fixed boundary data yields div(μ∇Φ)=4πGρ. G and a₀ are inherited physical scales, not calculated here. This reduction does not select when the NET Field is fully open; a drainless residual requires a separate ownership/drain law.

Within the specified class of rotationally invariant potentials and bilinear work, the vacancy law is uniquely forced by the target. Indeed x=r/(1−r) fixes W'(r), and W(0)=0 fixes the constant. Equivalently W is the convex conjugate of L(x)=x−ln(1+x). This is inverse design/characterization from AQUAL, not an independent derivation of μ.

## 3. Tensor fingerprint and rank obstruction

With n=**x**/x, define P∥=nnᵀ and P⊥=I−P∥. At x>0,

    Dp_* = P⊥/(1+x) + P∥/(1+x)²,
    Hess A = I − Dp_*
           = [x/(1+x)]P⊥ + [x(x+2)/(1+x)²]P∥.

At x=0, Dp_*=I and Hess A=0. At x=1 the reduced response has eigenvalues (1/2,1/2,3/4). At nonzero x the ratio of longitudinal to transverse response is 2−μ.

For a stationary elimination with nonsingular internal Hessian H and affine drive, E(z,x)=|x|²/2 + U(z)−x·J(z),

    Hess E_eff = I − B H⁻¹ Bᵀ,  B = D_z J.

The required correction has rank 3 at every finite x, including zero. Hence any such realization needs rank(B)=3 and at least three independently driven real internal tangent directions. If H is positive definite, the correction is positive semidefinite. A scalar affine drive yields at most rank one, and a two-coordinate tangent at most rank two, regardless of nonlinearities of U. This is a local obstruction only for the stated bare Hessian, affine-drive and regular-branch assumptions. Direct field-dependent stiffness, a non-affine source or a singular branch could evade this particular argument. At x=0, every rank-deficient correction has spectral-norm error ≥1.

## 4. The native three-coordinate balanced sector

The inherited matrices M, C, metric Gm, stationary v, norm factor f and overlap χ* are copied exactly in the test file from the repository's verify_fixed_vortex_response.py. They are not refitted. The norm constraint gives two real fixed-orientation tangent coordinates. In the existing scalar drive H_j=H+2ju, the projected driving direction is P C v; it is one column. In the stable subcritical range the stationary overlap obeys

    du/dj = 2 k/(1−h k),   k=42815/290521,
    h(t)=2t/[χ*(1+t)],     χ*=59/308.

Five independent nonlinear stationary root solves recover this derivative by finite differences at t=0.1, 0.5, 1, 1.5, 1.8. They are in the subcritical range; the inherited branch is a local energy maximum on this tangent. Its envelope curvature is +2du/dj, the opposite sign from the AQUAL subtraction for the same Hamiltonian sign and affine external work. A physical action could have a different sign or additional response, but that must be derived. Stable maximum does not imply a positive minimum. Full space has more coordinates, and this test does not rule it out.

## 5. Four tetrahedral records supply a natural three-dimensional port

Let T have rows (1,1,1), (1,−1,−1), (−1,1,−1), (−1,−1,1), all divided by 2. Then TᵀT=I and TTᵀ=I−11ᵀ/4. Set q=T p, z=T x. Both have zero sum and the same norms as their three-vector preimages. Thus

    E(z,q) = |z|²/2 − z·q + W(|q|),  1ᵀq=0

is exactly the previous vector action in the inherited regular tetrahedral frame. A common scalar plus the three-dimensional contrast space is the existing 3+1 frame. This is an algebraic embedding, not evidence that the physical face records carry q. Tests cover all 24 face permutations.

A discriminating counterexample: four independent face costs Σ W(|q_i|), even with the zero-sum constraint, do NOT recover isotropic AQUAL. For small x, q=z+O(x²); their minimized energy has leading term Σ |z_i|³/3. For a unit coordinate axis this gives x³/6. For a unit body diagonal this gives 5x³/(12√3), whereas AQUAL gives x³/3 in every direction. Independent constrained numerical solves confirm anisotropy. Thus tetrahedral symmetry alone is insufficient: the required leading response must become collective/radial or recover isotropy by some other derived mechanism (e.g. a demonstrated averaging limit). No averaging is assumed here.

## 6. Deep-field nonanalyticity

Along any line **x**=t n the exact target is A=|t|³/3−t⁴/4+O(|t|⁵). It is C² but not C³ at zero. If a finite real-analytic microscopic energy has an isolated regular stationary branch (nonsingular constrained Hessian) at zero, the analytic implicit-function theorem gives an analytic reduced energy. Therefore exact AQUAL cannot arise at zero from that class. The radial vacancy potential itself contains the required nonanalytic |p|³ term; this is why the constructed model escapes the obstruction. Other potential escapes include a degenerate branch, a nonanalytic source, or a singular collective/continuum limit. No specific native escape is claimed.

## 7. Why a correct partition is not sufficient

The inherited knot analogy supplies the correct share by minimizing [x(1−b)²+b²]/2, yielding b=μ. But its on-shell energy is x/[2(1+x)], not L(x). The field equation depends on the work-conjugate derivative of the on-shell energy, not merely on the fraction at the stationary point. This tests a particular quadratic knot realization; it does not invalidate the earlier share theorem.

## 8. Next decisive native experiment

1. Construct the three directional work-conjugate port observables from the existing four time-face contrasts, using the native full vortex action. Keep the actual chamber exchange and symmetry representations; do not simply identify the exchange-even overlap with a physical share.
2. Compute the constrained Hessian H and three-column drive B at a zero-field and nonzero-field stationary background. Test rank and signs before any fit; distinguish true minima from stable maxima.
3. Compute the tensor BH⁻¹Bᵀ and compare directly with P⊥/(1+x)+P∥/(1+x)², including the x→0 cancellation and directional anisotropy. Derive the physical normalization x rather than equating it to the native overlap. A scalar fit or the x=1 witness is not enough.
4. Determine what supplies the nonanalytic deep-field limit and whether the collective mode has a genuine radial response. Test the full rather than fixed-z sector. Only then attempt the physical proof and its NET Field extension.

## Reproduction and scope

    python -m pip install -r requirements.txt
    python -m pytest -q

`verification.txt` records 75 passing pytest cases, including exact SymPy identities, 28 vector/radius cases, 16 numerical vector settlements, full tetrahedral permutation tests, explicit rank and deep-field checks, 5 native nonlinear stationary susceptibility cases, and 6 independent face-settlement comparisons. Cases contain multiple assertions; they are not 75 independent theorems. The first run revealed a scalar/array call error and a finite-difference step too large near the native curvature threshold; both test implementation issues were corrected before the final run. No new Lean compilation or full native-Hamiltonian simulation was performed; the source repo was read, not modified.
