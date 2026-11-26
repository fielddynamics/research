# The tetrad scheme, the two root sectors and the vertex

[Interactive HTML companion](interactive/geometry.html) — offline explorer of the existing results.

## 1. What the scheme proof actually says [inherited theorem]

The [scheme proof](../../../proofs/tetrad-scheme-two-bounded-regions/) fixes a nondegenerate metric g and solves g=eᵀηe. For η=diag(−1,1,1,1), κ=det(g)/det(η)>0. Any solution is invertible. With a chosen solution e₀, every other is Λe₀, where ΛᵀηΛ=η. The determinant equation is (det e)²=κ, and P=diag(1,−1,−1,−1) preserves η while reversing det e. Over the real numbers the two determinant pieces are open and closed in the solution space. The full real Lorentz group has four connected components (time orientation also matters); fixing the future time orientation leaves two. With the observer/time leg fixed the spatial group is O(3), split into SO(3) and P·SO(3). The scheme's algebraic connectedness statements over C use the cited group theorem, not a new Lean claim. The proof explicitly distinguishes determinant roots from individual tetrad matrices.

Thus the sign cannot change along a continuous path of nondegenerate tetrads. Along the explicit interpolation e(t)=[(1−t)I+tP]e₀, det e(t)=(1−2t)³ det e₀; the midpoint has rank one and a degenerate metric. This is not a valid path on the fixed-metric solution scheme. Any alternative continuous path changing sign also meets det e=0 by continuity. There is no third root at determinant zero.

## 2. A stronger algebraic formulation: two projectors [new deduction]

Set σ=det(e)/√κ in the real coordinate algebra of the fixed-metric scheme. Then σ²=1. The elements

$$p_A=(1+\sigma)/2,\quad p_B=(1-\sigma)/2$$

are orthogonal idempotents, p_A+p_B=1. Multiplication by any function on the scheme commutes with them. This is the exact algebraic separation: the coordinate algebra splits as the product of its two determinant pieces (Chinese remainder theorem). A root-blind quantity belongs to the parity-even part; parity interchanges the two idempotents. This is stronger than saying the two pictures look different.

To express physical transfer, introduce **amplitude records** in a direct sum V_A⊕V_B, with sign operator S=diag(I,−I). An operator L preserves each chamber iff [L,S]=0. An off-diagonal interaction does not commute with S, and can transfer occupation even though the underlying configuration domains remain disjoint. This is a construction of an interaction algebra, not a path of tetrads and not proof of quantum superselection in nature. If every physical observable and interaction were required to be block diagonal, transfer would be forbidden. That is a separate physical premise, which the GFD vertex rejects. The sign of an individual tetrad never continuously crosses zero in this construction.

For a scalar amplitude pair A,B, with N=|A|²+|B|²>0,

$$s_\mathrm{state}=(|A|^2-|B|^2)/N,\qquad s_\mathrm{state}^2+4|\bar A B|^2/N^2=1.$$

The sign operator has eigenvalues ±1, but its normalized expectation ranges continuously from −1 to +1. The symmetric state s_state=0 is a balanced **read**, not a zero determinant tetrad. For vector amplitudes the equality becomes an inequality by Cauchy–Schwarz. If one postulates s_state=(x−1)/(x+1), the shares become μ and 1−μ. The scheme alone does not establish this identification, nor that microscopic occupation is gravitational field strength. In particular the vertex exists independently of whether the scalar response has x=1.

## 3. Common interaction geometry is not a common spatial volume [model premise]

Use the intrinsic tetrahedral frame M with MᵀM=4I−J and the two realized solids S_A=conv(s_i), S_B=conv(−s_i). Their **images** in a common Euclidean representation intersect in the octahedron, exactly as Proof 25 proves. In that common embedding their interiors overlap; no shared original vertex/edge/face as simplicial cells does not imply a disjoint physical volume. We explicitly distinguish X_A and X_B as labelled disjoint domains, with realization maps into the common geometry. There is no continuous path in the topological disjoint union from X_A to X_B. Interaction is an additional map of their amplitude/read spaces. A single vertex connects the records without identifying points of X_A and X_B.

Neither the scheme nor the geometry forces that physical interpretation; it is the GFD architectural premise. A constant parity transformation also preserves coordinate torsion if the frame and connection are consistently transformed (see [two connections](../../two-connection-dual-chamber/) and [where the roots live](../../bimond-gfd/14_where_the_roots_live.md)). The metric's root blindness does not prove an independent physical sector, and the Christoffel/contorsion distinction is not a proof that TetB has no intrinsic metric of any kind. That would need a physical postulate about what is observable and how the vertex acts.

## 4. Why the time face matters [conditional geometric model]

A regular tetrahedron by itself has no preferred face. The scheme proof fixes the observer/frame axes; in those coordinates the uniform-sign face is distinguished. This is the GFD time-face convention, not a Lorentz-covariant dynamical selection. Once one face is designated, its stabilizer is S₃ (proper part C₃), not all S₄. The two time faces are separately addressed by the same four child labels: central child = distinguished face label, other three = corner labels. The inverted face has the same labels. Proof 23's complete medial depth-two refinement supplies 16 paired subaddresses. Inversion pairs labels but does not identify amplitudes. All four choices of time-face index transform covariantly under S₄; at a fixed choice only the stabilizer is required. A model claiming full S₄ with a fixed distinguished face must explain this.

We can now compare the chamber amplitude record (4×4 including the four central records) with this two-index time-face address space. The correspondence is an explicit intertwiner under the stabilizer. It is an algebraic capacity match, not proof of a physical propagation law. The detailed matrix factorization follows in the next note.
