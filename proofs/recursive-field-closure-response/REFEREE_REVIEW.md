# Internal referee guide — revision 4

The purpose of this guide is to make the manuscript easy to assess on its own merits. The algebra can be checked separately from the proposed physical interpretation. These are internal review questions and responses, not an external referee report.

| Challenge | Resolution / remaining gate |
|---|---|
| Closure itself forces a read? | Only when no common feasible state exists, or a unique selected state depends on environment. Theorem 1 gives exact iff conditions. |
| 21 means 21 physical operations? | No: tree has 21 readers with three contrasts each; full Walsh has three stages of 16 four-point transforms. Invariant detail rank is 21. |
| Same dimension implies equivariance? | No: P23 actual Triforce action has 22 invariants; ordered cube-pair action 24. Explicit compressed pointing spectrum is incompatible with abstract depth sign. |
| Sierpiński alone gives alpha? | No: determinant of the unipotent blocks is one. Three alternating shears may implement a rotation of arbitrary angle. |
| Tetrahedral symmetry forces diagonal bridge? | No. Commuting XOR translations would force character diagonality, but this is a new physical symmetry requirement. |
| Scalar symmetry implies invariant averaging is sufficient? | No. Noninvariant squared norm is invariant yet discarded. Need physical sufficiency of selected read. |
| Closure score equals determinant? | No. Older nuclear landmark score and invariant dimension share counts but not observable. Packing order differs in certain incomplete blocks. |
| Full packing eliminates mass? | No. The contrast disappears, common mode survives. Physical energy also needs binding corrections. |
| 273 is a matrix rank? | It is full within-grade matrix-unit capacity, not an established physical rank. Sierpiński support is only 91. |
| 17/13 forced by the new incidence register? | The punctured pencil has 17 rows of 16 points; the Baer register has 13 rows. Orthogonal projection fixes the line normalization 1/16 and the rank ratio is 17/13. The physical selection of the pencil, equal-sector normalization and rank-ratio observable remains open. |
| Does a complete frame force its determinant as a source? | No. Multi-affinity and vanishing on every blocked direction would uniquely give the intensity product. Ordinary quadratic read scales as intensity, not intensity^21. |
| Does vortex susceptibility establish physical gravity? | No. Exact tangent response uses a candidate overlap drive in a local maximum sector. Native Hamiltonian weights are chosen witnesses; no attraction sign or physical source follows. |
| Does changing vortex require changing the cube? | No in the stipulated graph. This does not rule out metric/observer changes in physical spacetime. |
| Why inverse square? | Theorem 11 proves the result from a chosen positive isotropic gradient action and universal source; deriving that action is open. |
| Does static read imply instantaneous causal exchange? | No. Causality, propagation, full stress-energy coupling and equilibration are not proved. |
| Is G now derived from geometry alone? | No. Theorem 8 establishes the determinant identity and states the conditional source; T11 establishes its conditional macroscopic completion. Neither chooses the gain nor proves native source selection. Loop correction is separate. |

## Additional questions raised by revision 2

| Referee question | Response in the revised manuscript |
|---|---|
| Is a necessary read already assumed in P1? | No. P1 now assumes only existence of a compatible selected state for each admissible environment. Theorem 1 states the additional condition under which no blind solution exists. |
| Does an information factorization establish a causal or continuous physical read? | No. Theorem 1 is set-theoretic; smooth rank results require differentiable maps, while locality and dynamical accessibility are separate. |
| Is the determinant forced by basis independence and requiring all directions? | No. The normalized trace and determinant are both invariant under independent left and right orthogonal/unitary basis changes. Even a determinant times a normalized trace-dependent factor obeys all-directions blocking. |
| What would make the exponent a genuine prediction? | Independent intensity variables and analytic blocked-direction identities force the product of all 21 intensities as a factor. A nonzero constant residual yields leading order 21; higher terms and the coefficient still need proof. Multi-affinity and normalization give the exact product. |
| Is a positive susceptibility an attractive force? | No. The envelope identity gives a force only through a specified separation-dependent work coupling, with sign and units fixed by the physical action. The inherited stationary branch is a local maximum in the real tangent sector. |
| Is the gravitational potential identified with a dimensionless coupling? | No. The scalar field in T13 has inverse-length units; its physical potential is Φ = (ℏc g/m_e)φ. This verifies the Poisson normalization, conditional on the action. |

## Decisive follow-up calculation

The best next test is to construct the work-conjugate source from the native fixed-geometry vortex Hamiltonian, rather than introduce further counting identities. In a consistent 64-address refinement, determine whether the independent intensity directions are physical; calculate the source as those intensities vary; test every blocked-direction identity and any lower-order symmetry-allowed term. Then determine whether the action selects the inherited ratio as a work-coupling normalization. Only compare the optional projective witnesses if independently motivated by the native dynamics. A nonzero lower-order contribution would contradict the proposed leading exponent unless a separate symmetry or cancellation removes it. This is a discriminating test, not a promise that the mechanism is correct.

## Release status

11 main numbered theorems and five optional appendix results (A1–A5), plus selection propositions and explicit counterexamples. Fresh exact verifier: 532 retained assertions plus 568 optional incidence assertions, 1,100 total. The new verifier also invokes the inherited finite-field builder, whose assertions are not included in this total. Seven inherited suites rerun in revision 1, preserved here: 1,352 assertions (some numeric checks in the recursive-generator suite; counts are assertions, not independent theorems). No previous numbered proof modified; no upstream Lean compilation rerun. Lean/lake executable not available on PATH, hence no new Lean certificate is claimed. A formalization should import P23/P25 and prove finite orthogonality, rank counts and compression separately from the real-analysis and physical premises. Before promoting from candidate, obtain native source coupling and investigate all symmetry-allowed lower-order terms; then undertake external review. Mathematical correctness is subject to normal review, not guaranteed by the number of tests.

## Optional appendix — historical Revision 3 response to the normalization objection

| Question | Resolution / remaining obligation |
|---|---|
| Why divide by 16? | In the pencil incidence projector the normalization is uniquely fixed by idempotence; the main formula uses ranks, not a chosen finest-grade divisor. |
| Why remove the identity? | The new construction excludes a distinguished point, not the identity vector. No trace-free physical generator is assumed. The old trace projection remains an alternative witness. |
| Why this point? | The specified ordered flag has a singleton point. The unmarked plane and scalar rotation do not select it. A native Field Origin-to-point correspondence must be proved. |
| Why divide by 13? | It is the rank of the Baer incidence projector. Equal-sector normalization and the use of a rank ratio in the physical source are still explicit assumptions. |
| Are the pencil, norm, and Baer reads the same? | No. The incidence signature is verified on every centre. Norm point- and trace-exclusion have the same spectrum but distinct exceptional eigendirections. |
| Does convergence with the winding Schur complement and Paper VI establish the mechanism? | No. They agree algebraically at D=K−1, but need an independent physical bridge. |
| How can the new mechanism be falsified? | Test the point identification, five central secants and one external secant per Baer sector, and the native second derivative (1355/832 for the old witness versus 272/169 for the pencil witness, at unit transmission and the specified perturbation scale). |

The original objection is answered within the optional incidence model, not for the physical mechanism. The main proof no longer derives its normalization from either projection or trace removal. Instead it inherits the polynomial ratio, and explicitly leaves the physical source coefficient unproved. No new operation is required merely to reproduce an existing arithmetic result.
