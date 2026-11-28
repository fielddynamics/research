# 08 · Research audit, reconciliation and proof roadmap

[Back to README](../README.md)

## What changed relative to the original AQUAL folder

| Topic | Consolidated position | Evidence |
|---|---|---|
| Exchange uniqueness | Endpoint + exchange closure + degree-one premise select the simple form after unit normalization; asymptotes alone do not | T conditional on premises |
| Three energy terms | Deep field follows from cancellation, not dominance of log | T |
| Source sign | Static Lagrangian has −ρΦ, not +ρΦ | T |
| AQUAL vs QUMOND | Legendre dual energies; generic physical fields not pointwise algebraically equivalent | T |
| Hessian | Positive transverse and longitudinal away from zero; degenerate at zero | T |
| Existence and uniqueness | At most one solution with specified boundary data; no general existence theorem claimed | T |
| Covariance of y | Acceleration norm of a unit time leg makes y ≥ 0; no independent scalar required in adopted lapse model | C |
| Matter coupling | Weak-field −ρΦ follows from minimal metric coupling if Φ is the lapse | T/C |
| Newtonian energy counting | Curvature supplies y, correction must be F−y | T in stated reduction; covariant prescription C |
| Stability and speed | Static convexity vs Lorentzian scalar vs khronon are distinct; earlier μ≤1 speed test insufficient | T/C |
| High acceleration | Fraction tends to zero but absolute residual tends to a₀; net-field ownership is necessary in this model | T/C |
| Net-field action | Fixed ownership sweep provides exact Poisson/AQUAL split; no arbitrary merging of overlapping closures | T/C |
| Closure boundary | Tidal/stagnation rationale for Jacobi surface; dynamical selection and shape not derived universally | C/O |
| Anisotropic shell | Centred spherical shell in constant SPD linear response gives no interior self-quadrupole; trace and ordinary tide remain | T/C |
| Interface | Potential continuous but derivative may jump; effective sheet. Relativistic moving-junction conditions open | T/C/O |
| Nested closure | Exact linear balayage composition under nesting; drained nonlinear parent extension open | T/O |
| Density | Bounded acceleration does not imply bounded effective central density (point-mass cusp) | T |
| Decoder | Spherical exact; arbitrary disk effective estimate. Other interpolation functions also allow decoders | T |
| Comparisons | Standard μ = x/√(1+x²); n-family μ = x/(1+xⁿ)^(1/n); McGaugh RAR specified in source z | T/reference |
| Hubble relation | Two distinct normalizations in archive; neither silently selected here | O |
| Microscopic saturation | Finite-capacity conjugate gives F exactly for prescribed read and cost law | C |

The source notes once flagged matter coupling and nonnegative covariant y as unresolved; the later P-sst and P-timeleg constructions address those under their premises. The older statements are retained as historical issues rather than silently repeated as current conclusions. The original AQUAL docs critique includes other useful warnings: shifting the acceleration unit can make competing laws cross at μ=1/2, so that crossing is not a uniqueness test. A positive F'' alone does not prove a ghost-free covariant theory; μ≤1 alone does not prove subluminality.

## Constants and scale discipline

The archive's electron-scale estimate is $a_0=K^2Gm_e/r_e^2$ with $K=4$ and classical electron radius $r_e$; it is around $1.225\times10^{-10}$ m/s² using standard constants. It depends on G and other dimensional constants. The archive uses both $a_0=cH/(2\pi)$ and $a_0=(cH/(2\pi))\sqrt{4/\pi}$. At $H=70.21$ km/s/Mpc they give roughly $1.086\times10^{-10}$ and $1.225\times10^{-10}$ m/s². They differ by about 12.8%; this must be reconciled, not treated as equal. The constant G in the static field equation is the chosen Newtonian gravitational coupling; a separate bare-versus-effective G conversion must be explicitly defined when using Paper VII or Proof 26. No new numerical constant has been fitted here.

## Priority proof program

1. **Native read and transduction.** Derive the acceleration of the physical time leg from the actual coherent vortex/Walsh read, with correct dimensions, locality, common-time reference and control of finite-resolution errors. Prove how the three resolution sweeps and reset give that read rather than imposing an external observer.
2. **Dynamical settlement.** Derive the finite-capacity rate or Hamiltonian equivalent, including the work conjugacy, origin of a₀, conservation/dissipation ledger and stability beyond fixed drive. Connect the vertex proof to AQUAL without identifying a normalized overlap with acceleration by assumption.
3. **Covariant ownership.** Formulate an action with the correct F−y correction and dynamically varied boundary/ownership variables. Prove moving interfaces preserve total stress–energy, clarify EM coupling and the foliation mode, and recover the fixed-surface limit.
4. **Drained closure composition.** Establish a boundary-data/current map for arbitrary drained children and drained parents. Prove or delimit associativity and compatibility across overlaps; include finite-size multipoles, time dependence and the effective surface layer. This is essential for galaxies and clusters to register at the same logical level as smaller objects.
5. **Observational differentiation.** Numerically solve non-spherical galaxies with a specified net-field prescription; compare full field and algebraic approximate RAR; then test binaries, clusters, lensing and solar-system interfaces with external-field and measurement systematics. Report predictive uncertainties and comparisons with MOND and ΛCDM without fitting per-object drive/brake ad hoc.
6. **Constants and closure rate.** Resolve the two Hubble/a₀ normalizations, and derive rather than select the elementary gain, attenuation observable and work stiffness in Proof 26. No assertion of zero free parameters replaces a derivation of the model premises.

## Reproducibility scope

The upstream Python and Lean checks are linked and pin-addressed. This package performs independent numerical and symbolic checks, including adversarial examples of the curl obstruction, central density cusp, nonzero high-acceleration tail, and the exact positive-definite linear shell theorem. It does not rerun upstream Lean, a full N-body solver, SPARC fits or the native H36 engine. The tests illustrate the theorems under their specified hypotheses; they do not prove empirical correctness or settle the open physical identifications.
