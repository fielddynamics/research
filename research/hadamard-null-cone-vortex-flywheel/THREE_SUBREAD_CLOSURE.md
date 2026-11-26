# Three sub-reads of one closure engine

*GFD Standard Field Model · November 2026*

**Status:** [T] exact finite-dimensional identities; [D] consequences of the specified candidate Hamiltonian and read operations; [E] autonomous implementation, physical grading, attenuation and gravitational registration. No new physical constants or fitted G. SST denotes only the full covariant action. One whole stellated octahedron per field.

## 1. Face, subface, subchannel

The primary candidate is the [recursive Triforce geometry](../recursive-triforce-geometry/): four coupled face directions, four medial tiles per face and four medial children per tile, including the central child. This supplies 64 paired geometric addresses. The specified Flower lattice permits at most two complete dyadic subdivisions; whether dynamics require this lattice and occupy the maximal depth remains open. The two chambers retain distinct surfaces, and the refined addresses do not replace the 36 complex microscopic coordinates. Address downward and aggregate upward.

![Recursive Triforce geometry and depth rule](../recursive-triforce-geometry/recursive_triforce.svg)

![Three nested sub-reads and terminal addresses](figures/44_three_subread_tree.svg)

Let the coherent address ledger be x[a,b,c], a,b,c in {0,1,2,3}. Use h=H4/2, the orthogonal four-point Walsh matrix. At each node retain its common mode and three differences. The first aggregation acts on c in all 16 subfaces, retaining 48 fine details. The second acts on b in the four common-mode branches, retaining 12 intermediate details. The third acts on a and retains 3 coarse details and the final scalar. Thus there are 21 four-way readers, 63 differences and one scalar. This is an exact reversible multiresolution transform B, not merely a count:

$$64=1+3+12+48=1+3(1+4+16).$$

The common scalar is the sum of all 64 records divided by 8. Every address can be reconstructed with B transpose. An ideal static snapshot or coherent reference to a single time is required; the pi walk cannot simply combine evolving records from unrelated times. The addressing direction is face → subface → subchannel; the mathematical return read is subchannel → subface → face. This does not identify three physical time intervals or a Compton clock.

## 2. Exact relationship with full FWHT [T]

![Tree transform, detail mixer and full Walsh operator](figures/45_three_subread_factorization.svg)

Define B1=h on every last digit; B2=h on the b digit only where the last digit is zero; B3=h on the a digit only where both following digits are zero. B=B3 B2 B1 is orthogonal. Let D act as h tensor h on the first two digits at every nonzero last digit, and h on the first digit for nonzero middle digit with last zero. The exact relation, verified entry by entry, is

$$H_{64}/8=(h\otimes h\otimes h)=DB.$$

D only mixes detail coordinates within a scale; it is not an extra physical closure cycle. The tree alone requires 21 four-way transforms, whereas the full radix-four Walsh transform requires 16 transforms in each of three stages (48 total). Do not confuse the internal-reader count with the total number of FWHT arithmetic operations.

## 3. Threefold symmetry of the recursive geometry [T]

Under the actual spatial $120^\circ$ rotation there is one fixed face; on that face the central child is fixed and the other three cycle, at both refinement levels. Every prefix partition is preserved. The invariant dimensions of the prefix-constant spaces at depths 0, 1, 2, 3 are $(4^k+2)/3=1,2,6,22$; subtracting adjacent ranks gives contrast dimensions 1, 4, 16. The 21 internal readers and 21 invariant contrasts are different structures, not individually identified modes.

Separately, the [projective corner-pair construction](PROJECTIVE_WALSH_G_BRIDGE.md) uses a simultaneous XOR digit cycle $M$, with $Q=(I+M+M^2)/3$. Its Walsh operator satisfies $FM=M^TF$ and $FQ=QF$; the tree detail strata also have invariant dimensions 1,4,16. This is an exact identity for the computational representation, not proof that it represents the physical rotation on corner pairs. Spatial rotation on corner pairs has invariant dimension 24, versus 22 for recursive triangles. No direct equivariant relabelling exists. The projective time-adapted flag is described in the [root-exchange note](../g_from_topology/read-and-rotation/ROOT_EXCHANGE_ON_THE_ADDRESS_TREE.md); it does not select the physical chamber-sensitive operator. Preserve the zero/mean mixing of the projective FWHT.

For the recursive geometry, the pointing operator $J\otimes J$ has 10/6 signs per face, but the uniform-mean-zero invariant compression has spectrum $+1$ (13), $-1$ (7), $-1/4$ (1). Thus it is not the assumed $+,-,+$ contrast grading. See [recursive Triforce geometry](../recursive-triforce-geometry/).

## 4. Native core operator coordinates (a separate mathematical observable) [T/D]

![Native coherent read and three-axis operator resolution](figures/48_native_recursive_read.svg)

The [native Walsh study](NATIVE_WALSH_READ.md) reconstructs the eight complex central triangle amplitudes z from four coherent port histories of the existing H36. This extension reuses seven samples spaced by dimensionless 0.9, with spectral-norm core reconstruction residual 3.57e-15. Phase-neutral closure can form rho=zz†. For each axis the elementary four observables are (I,X,Z,Y), and the complete operator basis is their three tensor factors. Write

$$p_{abc}=\operatorname{Tr}[(P_a\otimes P_b\otimes P_c)\rho],\qquad \rho=\tfrac18\sum_{abc}p_{abc}P_a\otimes P_b\otimes P_c.$$

For one 2x2 dyadic block the four outputs are diag sum, offdiag sum, diag difference and i times the offdiag difference. After dividing by sqrt(2), this is a unitary coordinate conversion of the four complex entries, implemented algebraically by two two-channel Hadamard butterflies, permutation and phase. Repeating along each paired bit gives the full 64-coordinate Pauli read. This is a **different transform from the real address FWHT**, though both use four-way factorizations. Six fresh trials reconstruct the exact core Pauli ledger from the seven coherent histories of arbitrary 36-coordinate initial states. This is a postprocessed coherent read, not an autonomous measurement circuit. It requires known H and coherent sample access. A pure core density has only 14 normalized real degrees of freedom (15 with variable norm), so the 64 ledger entries are not independently adjustable; a general mixed Hermitian matrix has 64 real coordinates. Neither ledger has yet been identified with the physical affine connection.

## 5. What rotates? [T/D]

![Internal Pauli cycle and spatial rotation obstruction](figures/46_pauli_cycle_obstruction.svg)

For one binary axis define U=(I+i(X+Y+Z))/2. U is unitary, U³=-I, and conjugation cycles X→Z→Y→X with no signs. Applying U3=U tensor U tensor U implements precisely M on the 64 Pauli labels, including all 21 nonzero triples. Its eigenphase multiplicities are 2,3,3; its commuting operator space therefore has dimension 2²+3²+3²=22. The orbit average of rho is a genuine positive, trace-preserving operation:

$$\mathcal T(\rho)=\tfrac13\sum_{k=0}^2 U_3^k\rho(U_3^k)^\dagger.$$

For pure rho this mixture has rank at most 3. Its Pauli ledger is Qp. This is not an assertion that gravity performs irreversible dephasing; an actual coherent group read must retain the other 42 coordinates if full information is needed.

A physical 120-degree rotation of the stellated cube around a body diagonal has two fixed corners and two three-cycles. Its conjugation on the 64 core operators has invariant dimension (64+2*2²)/3=24, **not 22**. The Triforce's visible threefold rotation alone is insufficient to generate the proposed Pauli orbit symmetry.

The inherited H36 commutes with geometrical inversion; on its core inversion is XXX. U3 sends XXX to ZZZ, so U3 does not commute with inversion. Any compression of native free evolution to the core still commutes with inversion. Hence it cannot equal U3 for arbitrary inputs, even up to global phase. This is an exact obstruction, not a failure of numerical optimization.

A controlled realization on the actual 12 cube bonds is possible: set K3=-sum_j(X_j+Y_j+Z_j), with j over the three axes. These generators commute across axes; a single dimensionless pulse of duration pi/(3 sqrt(3)) produces U3. X and Y use existing bonds (Y requires oriented complex hopping), Z requires opposite on-site phase potentials. Isolating the core and implementing these controls gives zero leakage in the constructed pulse. This is [D] a candidate controlled implementation, not native dynamics. The next physical task is deriving the phase-odd hopping and onsite terms from vortex circulation or a dynamical reference frame while conserving the full engine energy. A state-selected rotation could break inversion in a sector without breaking symmetry of the underlying theory, but no such solution has been proved.

## 6. Why 21 attenuation factors could arise [D/E]

![Raw versus invariant contrasts and different optical attenuations](figures/47_three_subread_attenuation.svg)

A specific symmetry-preserving optical contraction can be constructed without assigning different fitted coefficients to the 21 levels. Preserve the common scalar and multiply every orthogonal detail amplitude by t=sqrt(alpha). In input coordinates, with normalized common vector e=(1,...,1)/8,

$$J_\alpha=t I+(1-t)ee^T.$$

This commutes with Q. On all 64 records its eigenvalues are one and 63 copies of t. On the 22-dimensional invariant sector they are one and 21 copies of t. Therefore the squared determinant is alpha^21 on the reduced sector, versus alpha^63 on the full sector. Ordinary normalized contrast transmission is just alpha. A different, independently attenuated three-stage serial path would give alpha^3; that is not the operation calculated here. The contraction has an exact lossless orthogonal dilation with complementary reflected modes; no probability vanishes in the combined model.

The abstract coupling polynomial can be represented by signed traces of three invariant contrast blocks (1,4,16) **if** the middle grade is selected. This is not the physical pointing-parity operator, and the projective flag does not derive that selection for the recursive face geometry. Negative s would entail gain if interpreted as a passive optical exponent. The physical selection of a determinant rather than ordinary transmission, the per-contrast alpha coupling, the middle-grade assignment and the 17/13 normalization remain open. The inherited conditional target remains

$$G=(17/13)\alpha^{21}\hbar c/m_e^2,$$

with the proposed upstream loop factor 1+alpha/(2 pi). The electron closure equations and boundary register are retained, not re-derived here. An invariant contrast determinant is a collective volume (exterior-power) read, not a generic force amplitude. The figure deliberately distinguishes these.

## 7. Pi addressing and next derivation

The [pi walk](PI_WALK_FWHT.md) addresses ordered corner pairs by modular addition, not XOR. Its 332-digit coverage and 156-digit projective quotient coverage are exact properties of the supplied schedule, not physical periods. Treat this as a candidate computational addressing procedure; no rotation-equivariant relabelling to recursive face addresses exists, and no native transduction law or BBP generator is established. The core Pauli coefficients are a separate observable, not a second physical closure ledger. First derive actual subchannel boundaries, lattice selection, a fine-scale Hamiltonian compatible with H36 and a physical registration law. Only then test whether a Walsh or pi read realizes that geometry and whether the source selects the collective contraction.

## Verification

Run `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_three_subreads.py`. See [log](three_subreads_verification_output.txt). 91 fresh assertions, 5,417 earlier recorded assertions preserved but not rerun, 5,508 cumulative recorded (not independent theorems). All five figures are generated by the verifier in SVG and PNG. No remote repository changes, empirical tests or new physical constants.
