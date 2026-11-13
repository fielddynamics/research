# Referee Review and Response

*Internal review of "The Null Directions of the Tetrad Frame Carry a Complete Boolean Basis" (first draft, commit 9beee7a), written as a journal referee would, with the change made for each point. The revised paper is retitled "Boolean Universality and the Null Cone of the Tetrad Frame".*

---

## Summary of the submission

The paper takes the eight null directions of the tetrad frame (Letter 1) and asks in what sense they form a universal Boolean operator. Its results:
- parity gates are not universal (Post);
- the Walsh matrix factors as H₈ = S D Sᵀ, with S the AND-monomial table;
- on the two-bit block, read as spinor indices, the null truth tables are exactly the separable gates, and those are universal.

The mathematics is correct and machine-checked. The concerns below are about novelty, framing, and two places where the text blurs distinct objects.

## Major points

**M1. Novelty and attribution.** Post's theorem, the algebraic normal form, NOR's universality and H₈ = S D Sᵀ are classical or elementary, and the draft does not say clearly enough which parts are new. More seriously, Theorems 1 and 2 hold for any set of eight points labelled by three bits. The null cone plays no role in them. A referee would read the title ("the null directions … carry a complete Boolean basis") as overclaiming, since any eight labelled points carry one.

*Response.* The paper is retitled *Boolean Universality and the Null Cone of the Tetrad Frame*. A new "Contributions and prior work" paragraph states:
- Theorems 1–2 are facts about the labelled Boolean cube;
- the null cone enters at exactly two places: the canonical labelling (Proposition 1) and the metric on the two-bit block (Lemma 1, Theorem 3);
- the identity H₈ = S D Sᵀ is elementary, and no novelty is claimed for it.

The abstract is rewritten to match.

**M2. Two different "null" objects are conflated.** Section 2 is about eight null *directions*, labelled by three-bit words: the inputs. Section 5 is about two-input *gates*, whose truth tables are 4-vectors: functions on a two-bit block. The draft moves from one to the other without saying so, and a reader could take Theorem 3 as a statement about the eight directions of Section 2.

*Response.* Section 5 now opens by naming its object: the two-bit block C² ⊗ C² of the frame, the 4-dimensional factor in H₈ = H₂ ⊗ H₄ (Paper C). Its vectors are functions of two bits. A sentence says explicitly that this is a different use of "null" from Section 2.

**M3. Why the determinant?** The spinor reading assigns X ↦ det X as the Minkowski norm, but the draft gives no reason for this metric on the two-bit block, so "null gate" could look like a definition chosen to fit.

*Response.* A new Lemma 1 proves that det is, up to scale, the only symmetric bilinear form on C² ⊗ C² that is invariant under independent SL(2) changes of basis on each bit. (This is checked by solving the invariance equations: the solution space is one-dimensional.) So the null cone of the two-bit block is canonical. The null/non-null split of the gates (rank ≤ 1, the Segre variety) is invariant under every change of basis X ↦ BXCᵀ. Only the finer split into real and complex light rays depends on which Hermitian structure is chosen. The paper now says so, with an example: re-reading one bit by a swap makes AND a complex null vector.

**M4. The claim "universality sits in the Sierpiński factor" is not yet a theorem.** Over the reals H₈ is invertible, so in one sense it "contains" everything, and the localisation claim needs a precise form.

*Response.* Theorem 2 gains part (v): over GF(2), H₈ ≡ J, the all-ones matrix of rank 1, while S is invertible (S² = I). The Hadamard sign pattern therefore carries no information mod 2, and the algebraic normal form lives entirely in S. This is the precise sense of the localisation.

## Minor points

**m1. Dependence on the labelling.** Proposition 1's identification of the directions with bits depends on choosing axes and signs. *Response.* A new remark says the labelling is fixed up to the 48 relabellings (permuting and negating bits). The affine class, the closures and the null/separable classification are invariant under all 48 (checked). An odd number of negations exchanges TetA and TetB.

**m2. The "half-turn per bit" wording.** On the 3-bit H₈, the factor e^{iπ|x|} is a phase. Its reading as a spatial rotation exists only on the two-bit (and four-bit) block. *Response.* The wording now says "a phase e^{iπ} per set bit", and the Lorentz reading is restricted to the two-bit block, citing the null-rotation proof.

**m3. What the null rotation does to a gate.** The draft says AND is fixed by the null rotation, but not what the null rotation does to truth tables. *Response.* New Proposition 3:
- mod 2, X ↦ AXAᵀ sends a gate's truth table to its algebraic-normal-form coefficients;
- over the reals its only fixed gates are FALSE and AND;
- mod 2 the fixed gates are FALSE, AND, XOR and OR, the gates equal to their own algebraic normal form.

**m4. Convention for functional completeness.** Whether constants are free affects which sets are complete. *Response.* The convention is now stated: a gate set is closed under composition with the projections, and constants are available only if they are in the set. Post's five classes are listed.

**m5. The octahedral node.** The draft explains the node's NAND output by its readout, without evidence in the paper. *Response.* This is now attributed to the archive's description of the node, and the paper makes no independent claim about the node.

**m6. Signature convention.** Letter 1 uses (−, +, +, +); the paper uses (+, −, −, −) through det X. *Response.* The change of convention is noted where it occurs.

**m7. References.** Reed (1954) is added alongside Muller (1954) for the Reed–Muller expansion. O'Donnell's *Analysis of Boolean Functions* is added for the Walsh basis. The standard facts used in Lemma 1 are attributed to Penrose–Rindler.

**m8. Self-containment.** The paper relies on archive documents that are not peer reviewed (Letter 1, the null-rotation proof). *Response.* Each result used from them is restated with its short proof, so the paper stands alone.

## Assessment after revision

The revised paper is a short, correct note. It clarifies a claim made in the archive, separates the generic results from the ones specific to the null cone, and proves the strong (gate) form of universality in a precise sense. Its physical interpretation (that light computes) is explicitly outside its scope. A suitable venue would be a mathematical-physics or foundations journal that publishes short notes, or a supplement to the tetrad letters.

## Checks

The verification script grows from 18 to 26 checks. It adds: H₈ ≡ J mod 2; invariance under the 48 relabellings; TetA ↔ TetB under a negation; the uniqueness of the invariant form; the reading-independence of the null set; the reading-dependence of real light rays; the null rotation as the algebraic-normal-form transform mod 2; and its fixed gates over the reals and mod 2.
