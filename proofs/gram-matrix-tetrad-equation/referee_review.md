# Referee Review and Response

*Internal review of "The Gram Matrix of the Tetrad Equation" (revised version, commit ae58c6a), written as a journal referee would, with the change made for each point.*

---

## Summary of the submission

The note studies the Gram matrices of the two roots $M$ and $-M$ of the tetrad equation's spatial realisation. It proves:
- root-blindness of the self-coupling, sign reversal of the cross-coupling, and that Gram data resolve only the relative root;
- $M^TM = 4I - J$ from the Hadamard identity, with the eigenstructure;
- rigidity: the Gram matrix fixes $M$ up to $O(3)$, and the two roots differ by $-I$, hence only in orientation;
- the cube and parity-class description of TetA and TetB, and $\mathrm{Sym}(S) = \mathrm{Sym}(\mathrm{TetA}) \times \{\pm I\}$;
- the torsion-free condition as a projection from 64 to 40, and that for metric connections the torsion is the only place the roots can differ.

The algebra is correct and machine-checked. The concerns are about the setting, the scope of the connection-level conclusion, and how the index-grid reading is stated.

## Major points

**M1. Parity on the realisation is not justified as stated.** The draft takes the realisation from the forced-frame proof, where the columns represent all four legs $e_0, \dots, e_3$, and then says parity sends every $v_a \to -v_a$. But $P = \mathrm{diag}(1,-1,-1,-1)$ leaves the time leg unchanged. Read literally, $v_0$ should not flip, and $-M_1$ would not be the image of the frame under $P$.

*Response.* The Setting now uses the realisation of Letter 1 and the scheme proof: four directions in an observer's space, each a fixed linear combination of the spatial legs $e^1, e^2, e^3$. Their Gram matrix is forced as before. Because each direction is linear in the spatial legs, $e^i \to -e^i$ sends every $v_a \to -v_a$ (check R1). The scheme proof's caveat is added: $-e = PTe$ also reverses the time leg, so the identification of root with tetrahedron is for future-pointing frames.

**M2. The connection-level conclusion is necessary, not sufficient.** Theorem 3 shows a metric connection can distinguish the roots only through its torsion. A referee will ask whether it *does*. In the tetrad formalism $\Gamma = e^{-1}(\partial e + \omega e)$. If the spin connection is carried with the frame, $(e, \omega) \to (Pe, P\omega P)$, then $\Gamma$ is unchanged, torsion included. So torsion alone does not make a connection root-resolving. Letter 2's Proposition says "a torsionful connection depends on $e$ directly and is therefore root-resolving", and that "therefore" does not follow.

*Response.* Proposition 2 is added and makes the point exact:
- (a) carried covariantly, the connection is identical on both roots (proved, and checked exactly);
- (b) if both roots carry the same $\omega$, the two connections are compatible with the same metric and differ, exactly by a contorsion with nonzero torsion (rational example checked).

The Remark now says torsion is the *necessary* carrier, which is Letter 2's own word in its Corollary. Whether the field assigns connections covariantly or not is stated as a physical input, not a consequence of the tetrad equation. Letter 2's "therefore root-resolving" is not changed here. It is flagged for the author, since (a) is a counterexample to it as written.

**M3. The index-grid reading depends on the basis.** Upper and lower triangles depend on the order in which coordinates are listed. Reversing the order carries every upper entry into the lower triangle. Identifying the triangles with TetA and TetB is therefore a statement about a chosen ordered basis. In addition, $\tau$ (exchange of index slots) and $P$ (parity of the frame) are different operations, and the draft's Part III could be read as equating them.

*Response.* A "Two cautions" paragraph is added to Part III:
- the $40 + 24$ split and the condition $T = 0$ are coordinate-independent, because $\tau$ commutes with every relabelling and torsion is a tensor (checks R3);
- the $24 + 16 + 24$ split is a property of an ordered basis;
- $\tau$ and $P$ are distinct, and the only link between them proved here is Theorem 3(iii).

The framework's triangle reading is kept as a reading, cited to the original note and the chiral-holonomy proof. Letter 2's identity/parity-sector language for the $\tau$-even and $\tau$-odd sectors is cited as Letter 2's.

**M4. Novelty and prior work.** Gram rigidity, the $4 \times 4$ Hadamard matrix, $O_h = T_d \times \{\pm I\}$, the fundamental theorem of Riemannian geometry and the contorsion decomposition are all classical. *Response.* A "Contributions and prior work" section now says so, with citations added for Sylvester and for Hehl et al. on contorsion. What the note adds:
- the assembly on the two roots of the tetrad equation;
- the relative-versus-absolute root distinction, with orientation as the absolute invariant;
- the compound's symmetry as one root's, doubled by the exchange;
- the exact necessary-carrier statement, with the condition under which it is met (Proposition 2).

## Minor points

**m1. "Complete invariant" needs its hypotheses.** Rigidity needs rank 3 and labelled legs. *Response.* Stated after Lemma 5, and in the Setting ("the legs are labelled throughout").

**m2. TetA and TetB are congruent as point sets.** Theorem 2's "every element outside Sym(TetA) carries TetA onto TetB" includes rotations. For example, a quarter turn about a coordinate axis maps the TetA corners onto the TetB corners. A reader could take "TetA is not congruent to S" as saying more than it does. *Response.* That sentence is removed from the theorem. A paragraph after it says:
- 12 of the 24 exchanging symmetries are rotations;
- the roots are congruent as unlabelled sets but not as labelled frames (Proposition 1);
- this is the scheme proof's caution that they differ in leg order, not shape.

Checks R2 cover this.

**m3. Pointwise statements.** Theorem 3(ii) is linear algebra on difference tensors at a point. *Response.* "All statements are pointwise" is added to the proof.

**m4. Normalisation.** The draft fixes $|v_a|^2 = 3$, while the scheme proof uses unit vectors. *Response.* The Setting notes that every statement is invariant under a common rescaling.

**m5. The boxed inequality is a dimension count.** *Response.* Kept, since it is the original note's headline, but the theorem states the content: $\Pi_+$ has rank 40 and a 24-dimensional kernel, so it is not injective.

**m6. Abstract.** The draft said the discarded 24 are "the only place a connection can tell the roots apart" without the condition. *Response.* The abstract now adds that a connection carried covariantly with the frame does not tell them apart, and one that keeps its spin connection in general does, through its torsion.

## Points considered and not changed

- **The time leg in the Gram matrix.** One might ask for the full $4 \times 4$ metric rather than the spatial realisation. The note is about the realisation, and the full metric's root-blindness is stated in the Setting and checked (T4). Nothing further is needed.
- **The $(f(K,\pm1) - 1)/2$ identity.** The original verification script checks that the coupling polynomial reproduces 10 and 6. It is an identity in $K$ and is not used by any theorem here, so it is not added. The Coles Notes already record the counting caveat on the Letter 3 version.

## Assessment after revision

The algebra was sound. The revision makes the setting consistent with the scheme proof (M1). It turns the connection-level conclusion into an exact necessary-carrier statement, with the covariant counterexample and the non-covariant example (M2). It separates basis-dependent bookkeeping from invariant content (M3), and it places the note against prior work (M4).

Two things are stated as open, not proved: that the field assigns the roots non-covariantly related connections, and that their torsion is nonzero. One item is flagged for the author outside this note: Letter 2's "therefore root-resolving".

## Checks

`python verify_gram_matrix_tetrad_equation.py`: 66/66, exact rational arithmetic. Added for this review:
- R1, the realisation is linear in the spatial legs;
- R2, unlabelled congruence by a rotation versus labelled non-congruence;
- R3, ordering dependence of the triangles, $\tau$ commuting with all 24 relabellings, and torsion as a tensor;
- P2, Proposition 2 (a) and (b).
