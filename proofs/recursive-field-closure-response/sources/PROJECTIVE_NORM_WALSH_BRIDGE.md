# Projective norm, inverse Walsh reconstruction and the 272/273 register

Research continuation, November 2026. [T] Exact finite algebra; [E] physical identification open. Based on the user's five-point Walsh/Sierpiński/finite-field synthesis and the inherited recursive and native-generator notes. No new oscillator or spatial TetA–TetB link. No change to Proofs 24/25.

## 1. Three grades of one Walsh filter [T]

Use F4 digits, a common zero digit, and grade n = last nonzero digit (zero-based). Let W=H64/8, H64=H4 tensor H4 tensor H4, and E_n the diagonal spectral masks. Their ranks are 3,12,48. The address-space projectors are D_n=W E_n W. Thus J=W diag(1,t_grade(a)) W=product_n [I+(t_n-1)D_n]. Orthogonality of the masks applies each gain exactly once. The three commuting full radix-four stages each contain 16 local transforms; the separate multiresolution inverse tree has 1,4,16 readers plus the within-grade mixing. Do not identify their operation counts. The bridge is not a lossless Hadamard transform when |t| differs from one. The unnormalized Boolean Sierpiński zeta matrix S=L^tensor m satisfies H=S diag((-2)^popcount) S^T by the subset binomial sum. Its determinant is one; H inverse is H/2^m. The normalized inverse Walsh read is W itself.

In the standard binary encoding, multiplication by omega cycles 1,2,3 and fixes 0. The Fourier dual action is the inverse transpose; the orbit average commutes with W. Each projective Walsh orbit yields the real-space sum of three Walsh characters, equal to 4 times the indicator of a 16-point linear plane minus one. These 21 functions have squared norm 192, zero mean and pairwise orthogonality. This is a particular invariant basis, not the shape of every invariant vector. The invariant sector also contains the common scalar. The nonzero orbit counts are 1,4,16. The restricted bridge has determinant t0 t1^4 t2^16; squared modulus alpha^21 if |t_n|^2=alpha. No identification of actual spatial rotation on corner-pair records or physical alpha is established.

## 2. One finite-field tower [T]

Let q=4, A=q^2+q+1=21, B=q^2-q+1=13, E=q^2+1=17. Work with F64=F4[b]/(b^3+b+1), F4096=F64[theta]/(theta^2+theta+omega). The quadratic is irreducible; its F16 subfield is F4[theta]. The field norm F4096 -> F64 is N(u+theta v)=u^2+uv+omega v^2. Because the norm sends F16* to F4*, it defines a map F4096*/F16* -> F64*/F4*. These multiplicative quotients have 273 and 21 elements. The map is surjective (on the embedded F64 it is squaring), with 13 points per fibre. The embedded PG(2,4) is a Baer subplane in PG(2,16); its 13 multiplicative translates partition PG(2,16). Each intersects each norm fibre exactly once. Indeed the embedded subgroup has order 21 and intersects the kernel of order 13 trivially. The line size of PG(2,16) is 17. The norm need not preserve projective incidence and is not assumed to be a native geometric propagation path.

The grade-preserving matrix space Acal=R direct sum M4(R) direct sum M16(R) has dimension 273. Its matrix-unit coordinates (u,v) with u,v projective representatives of the same last-nonzero grade map bijectively to projective classes of u+theta v: divide by 1+theta to normalize the common pivot to one. Each grade supplies 1,16,256 points. The diagonal u=v maps to the embedded Baer subplane, because 1+theta is a projective scalar. The diagonal is therefore a norm transversal. This pairing uses a chosen flag and basis; it is not an incidence-preserving or physical isomorphism of matrix multiplication.

## 3. Exact compression of the global trace constraint [T]

Let M be the 21-by-273 incidence matrix of the norm map in the matrix-unit basis. Each column has one entry one and each row has thirteen. Thus MM^T=13 I. Let d be the vector of the identity in the grade-preserving matrix space: one on the 21 diagonal matrix units, zero otherwise. The transversal property gives Md=1 and d^T d=21. For the Hilbert–Schmidt norm, the orthogonal projection onto the trace-zero subspace is P=I-dd^T/21, rank 272. Set R=M/sqrt(13). Then RR^T=I and

    Breg = R P R^T = I - J/(21*13).

The eigenvalues are one (20) and 12/13 (1), so Tr Breg=21-1/13=272/13. The trace loss is 1/13 rather than one because the global trace direction is supported on a Baer transversal. Dividing by the finest grade size 16 yields exactly 17/13. More generally for any prime power q, the same field tower, norm and flag-pair construction give Tr Breg / q^2 = (q^2+1)/(q^2-q+1), using A B-1=q^2 E. The proof works with any generator of the quadratic extension outside Fq and compatible Fq basis of Fq^3. The two subgroups are coprime because A and B are odd and any common divisor divides 2q.

This is not just a deletion of one matrix cell: the removed trace direction is the normalized full identity. It is natural for trace-preserving variations of a normalized matrix, or traceless generators, but the physical register has not been proved to impose that constraint. Norm averaging is an orthogonal compression, not an independently established native settlement operation. The factor 1/16 is finest-grade normalization, not the ordinary mean over 21 modes. The action must select this normalization. Also det Breg=12/13, not 17/13. Therefore a single ordinary determinant of Breg does not give G.

## 4. A discriminating response formula [T/E]

For T=t I on the invariant read space and a formal response parameter epsilon,

    d/d epsilon det[(T^* T)(I+epsilon Breg/16)] at epsilon=0
       = |t|^42 Tr(Breg)/16
       = |t|^42 (17/13).

The polynomial is |t|^42 (1+epsilon/16)^20 (1+12 epsilon/(13*16)). If |t|^2=alpha this is the target dimensionless tree coupling. This is a conditional construction of a single response derivative, not a derived microscopic observable. Epsilon is a bookkeeper, not a tuned finite coupling. It distinguishes a response of a collective volume from the volume itself, and supplies a target variation for the action.

## 5. Alternating shears [T]

U(-p)L(2p/(1+p^2))U(-p) = [[(1-p^2)/(1+p^2),-2p/(1+p^2)],[2p/(1+p^2),(1-p^2)/(1+p^2)]], with p=tan(theta/2). Same-direction shears add and have determinant one. The full rotation has determinant one; retention in one port gives cos theta. Neither finite geometry nor conservation selects theta. Even with alpha known, deriving this retained overlap, not setting theta by hand, remains essential.

## 6. Visual atlas and interactive explorer

Open [Projective norm and Walsh reconstruction](interactive/projective_walsh.html) offline after extraction. The explorer uses the verifier’s actual enumeration and explicitly evaluates the 64-coordinate Walsh transform. The static diagrams can be regenerated using `python make_projective_visuals.py`.

![Forward–bridge–inverse Walsh filter](figures/projective_01_walsh_filter.svg)

![Three recursive Sierpiński blocks](figures/projective_02_sierpinski_blocks.svg)

![Finite-field tower and norm](figures/projective_03_field_tower.svg)

![Exact 273-point Baer ledger](figures/projective_04_baer_ledger.svg)

![Trace compression and normalized response](figures/projective_05_trace_compression.svg)

![Alternating shear rotation](figures/projective_06_alternating_shears.svg)

## Verification

`python verify_projective_bridge.py` (NumPy and SymPy): 71 assertions. The verifier enumerates the fields, projective quotient, norm fibres, Baer partition and trace projection and checks the Walsh orbit basis and alternating-shear identity. It does not verify native dynamics, trace-source selection, kinetic metric, EM gain, or the one-loop correction. Older results preserved, not rerun. The current result is an abstract bridge with explicit maps and a precise remaining physical test.
