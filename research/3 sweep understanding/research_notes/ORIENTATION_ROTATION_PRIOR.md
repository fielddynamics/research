# Four rotating orientations of the I Ching closure read

Exact finite algebra and numerical native-model tests. No modification to Proof 26, no new physical parameters, no derivation of G. Reproduce with `OPENBLAS_NUM_THREADS=1 python verify.py` (NumPy, SciPy, SymPy). CSV records 333 evenly spaced trial phases per model, not a physical identification of the BBP clock.

## Inherited definitions

Sources in fielddynamics/research: research/exploratory/i-ching/ORIENTATION_CHARACTER_AND_SEED_DUAL.md, COMMON_MODE_AND_SHARED_ZONE_PROOF.md, SHARED_ZONE_WALSH_ROTATION.md; research/hadamard-null-cone-vortex-flywheel/NATIVE_WALSH_READ.md. Work on R-invariant hexagram orbit sums (dimension 22), R(a,b)=(b,a XOR b), a,b in F2^3. J exchanges a,b, W is the normalized symplectic Walsh involution. Heaven u=111. Q selects dependent pairs modulo span(u). The orientation gate S=Q+(I-Q)J, and P=(I+S)/2. N=(I-S)/2 is rank four. Both the physical trace coordinate e and the inherited common seed f are fixed by S and by the reflection cycle C=S W S W. For traces of the contrast response subtract one fixed common coordinate. These common coordinates are not identical.

## Exact continuous breathing law

The inherited reflection cycle C has C^3=I. Set M=(2I-C-C^2)/3 and A=(C-C^2)/sqrt(3). Then M is an orthogonal rank-four projector, A is skew, A^2=-M, AM=MA=A. C=I-3M/2+sqrt(3)A/2. Its canonical minimal-angle continuous lift is U(theta)=I+(cos(theta)-1)M+sin(theta)A. It is orthogonal, preserves the fixed common line, and tr on the contrast space is 17+4 cos(theta). At pi, pi/2, 0 the trace is 13,17,21. At the threefold rotation's own sample phases 0,2pi/3,4pi/3,2pi the trace is 21,15,15,21, not 13,17,21. The interpolation is canonical given the chosen angle branch, not a derived physical time law. In fact tr(C^k S) on contrasts is 13 for k=0,1,2. A 333-digit schedule does not establish the phase interpolation.

## Explicit Fano-plane mechanism

Exchange odd space is seven orientation-difference lines labeled by each nonzero plane normal n. Orient the triples by cyclic permutation of bit positions, starting with positive-minus-negative orbit order for n=1,3,7. In order 1,2,4 | 3,6,5 | 7, M=diag(B,B,0), B=I3-ones(3,3)/3; sqrt(3) A has blocks [[0,L,0],[-L^T,0,0],[0,0,0]], L=[[1,0,-1],[-1,1,0],[0,-1,1]]. L L^T=3B. Thus the two three-component groups each have one mean and two contrast directions. The Heaven orientation is fixed, as are all exchange-even directions. The negative orientation projector N and M commute, tr(NM)=2, so just two of the original four negative directions lie in the rotating plane. U(pi) is not S; the scalar traces agree but the operators differ. This is the new explicit spectral dictionary. The marked spatial rotation T commutes with C but is not thereby identified with C.

## Native test

The inherited isolated central cube has Hc=-sum_j X_j. Use signless Pauli coordinates (a,b)->tensor I,X,Z,Y, and orthogonal projection onto the R invariant operator space. The projected Liouville generator G=Q_R[-i Hc, .]Q_R has rank 2, G^3=-12 G, GN=GM=0. Indeed the twirled Hamiltonian is -sum_j(X_j+Y_j+Z_j)/3. Its eigenvalues -sqrt(3),-1/sqrt(3),1/sqrt(3),sqrt(3) in multiplicities 1,3,3,1; only the two extreme phases share a rotation eigenspace, and the projected generator rotates their coherence at 2sqrt(3). The desired A has rank 4, in a different subspace. This rules out identification of the instantaneous projected free generator with the read rotation, not all nonlinear or history-dependent mechanisms. H36 has the same core derivative when the initial density is supported on the core. Its finite-time compressed core propagator E^T exp(-itH36) E includes leakage. The CSV reports unnormalized compressed transfer traces, cross norms and Frobenius distance to S, not a closed-system energy. Neither tested model realizes the orientation gate in the sampled phases.

## Positivity discriminator

For rho=threefold Pauli twirl of (|000>+|001>)/sqrt(2), the candidate S read gives a 2x2 principal minor on rows 6,7 (zero based) [[1/8,1/12+i/24],[1/12-i/24,1/24]], determinant -1/288. Thus S is not a positive physical map of the invariant density algebra. C likewise fails positivity: the characteristic polynomial of C(rho) is l^3(2l-1)(6912l^4-3456l^3+288l^2+24l-1)/13824; its quartic is negative at zero and positive as l tends to minus infinity, giving a negative eigenvalue. This does not prevent S,C from acting as orthogonal changes of read coordinates, or being implemented with an enlarged register that preserves the actual physical state. The physical density interpretation of those coordinate operations is ruled out as stated. U(theta) is lossless, its determinant squared is 1, and cannot generate alpha^21 by itself.

## Next test

Derive the actual read-carrier dynamics on the two Fano contrast triples (or a physically meaningful extended register). Establish its clock from the BBP address sequence, and its work coupling to the common energy register. Do not insert the rotation into H36 or assume its trace equals a source. The exact finite algebra provides a stringent operator target, not merely a numerical match to the coupling polynomial. Native model geometry copied from the preceding local spectral research; no remote changes, Lean run or physical validation.
