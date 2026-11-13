# Referee Review and Response

*Internal review of "G's Graded Operator Is a Null Rotation" (Theorems 1–8, commit 9beee7a), written as a journal referee would, with the change made for each point. The revised proof is retitled "The Sierpiński Blocks of G's Graded Operator Are a Null Rotation".*

---

## Summary of the submission

The proof takes the three blocks of G's graded operator, drawn in the archive as Sierpiński triangles. It shows that:
- G reads only their diagonal;
- with the two bits of the 4-block read as spinor indices, the 4-block is a null rotation;
- the Walsh–Hadamard read factors as null rotation × boost × reverse null rotation;
- K = 4 is the trace of a null rotation on a 4-vector;
- the Jordan chains split 16 into the pieces of a metric and a 2-form;
- the archive's tetrad frame is a Newman–Penrose null tetrad in the spinor reading.

The algebra is correct and machine-checked. The concerns are with the headline claim, one place where the statement is stronger than the proof, and positioning.

## Major points

**M1. The title and abstract overclaim: the operator is a null rotation only at s = +1.** M_s = S₀ ⊕ s S₂ ⊕ S₄ depends on s.
- **s = +1 (TetA).** It is exactly the null rotation acting on scalar, vector and rank-2 tensor.
- **s = −1 (TetB).** S₂ becomes −S₂, which is not a null rotation.
- **s = 0 (Field Origin).** The operator is singular, so it is not a Lorentz transformation at all.

The draft's title ("G's graded operator *is* a null rotation") and its abstract ("the character of a null rotation") hide this.

*Response.* The title is now "The Sierpiński Blocks of G's Graded Operator Are a Null Rotation". Theorem 5 now states the exact structure, verified exactly:
- **TetA:** M₊₁ = ρ(Λ_A), the null rotation on scalar ⊕ vector ⊕ tensor.
- **TetB:** M₋₁ = ρ(−Λ_A), the null rotation composed with the total inversion −1 (PT). PT is −1 on vectors and +1 on tensors, which is exactly the sign pattern of s.
- **Field Origin:** M₀ = ½(M₊₁ + M₋₁) = ρ(Λ_A)Π₊, where Π₊ projects onto the part even under −1. That is why 17 = (21 + 13)/2.

**M2. Which inversion is TetB?** The archive associates TetB with the parity image of TetA. On 4-vectors, spatial parity P = diag(1, −1, −1, −1) gives Tr(PΛ_A) = −1, and the graded trace of PΛ_A is 1, not 13. Only the total inversion −1 reproduces 13.

*Response.* This is now stated in Theorem 5 and in the Scope section as an open interpretive point. On the vector block, the sign s acts as PT, not as spatial parity. Whether GFD's TetA ↔ TetB exchange should be read as PT on the frame's vector block is not settled here.

**M3. "χ = 4 marks the null rotations" is too strong.** The draft says rotations have χ ≤ 4, boosts χ ≥ 4, and "the null rotations lie on the boundary χ = 4". But χ = |Tr M|² = 4 also holds for loxodromic elements (a boost combined with a rotation) with |Tr M| = 2 and Tr M ≠ ±2. Example: Tr M = 2e^{iπ/3}.

*Response.* Theorem 5 now gives the exact statement, using the standard classification of SL(2, ℂ) by trace (Beardon):
- among elements whose trace is real, χ = 4 holds exactly for ±1 and the null rotations (Tr = ±2);
- elements with |Tr| < 2 are conjugate to rotations (χ < 4);
- elements with real |Tr| > 2 are conjugate to boosts (χ > 4);
- the loxodromic counterexample is in the checks.

**M4. Novelty and prior work.** The spinor–vector correspondence, null rotations, the triangular factorisation of the Hadamard matrix, the Jordan structure of a principal nilpotent of 𝔰𝔩₂ (Clebsch–Gordan) and null tetrads from spin dyads are all standard. The draft says so only in its Scope section, and it attributes the triangular factorisation to Sylvester.

*Response.* A "Contributions and prior work" paragraph now opens the proof and says what is classical. The new content is identifying these structures with the blocks of G's operator and with the archive's tetrad frame, and the exact s-structure of M1. The factorisation is described as elementary; Sylvester is cited only for the matrix. References added: Lucas (1878) for the entry rule; Fulton–Harris for 𝔰𝔩₂ and Clebsch–Gordan; Beardon for the classification by trace.

## Minor points

**m1. The value 1 in A is a convention.** Every null rotation A(τ) about k with τ > 0 is conjugate to A(1) by a boost along k: B(η)A(τ)B(η)⁻¹ = A(τe^{−η}). *Response.* This is now a remark after Theorem 3. It strengthens the result: the Sierpiński block is *the* null-rotation class, not a particular one.

**m2. Figure caption.** The caption said the Sierpiński block "carries every other light ray towards" k. That describes the one-parameter group A(τ) as τ → ∞, not the single matrix A(1). *Response.* The caption now says so (a limit is checked).

**m3. The "area" comparison.** Nobody proposed reading G from the filled area, so 1 + 9 + 81 = 91 is a straw man. *Response.* It is kept, but moved out of Theorem 2 into a remark, where it serves only to show that G reads the diagonal.

**m4. The Newman–Penrose normalisation.** ε(h₀, h₁) = −2, so the tetrad of Theorem 8 is the Newman–Penrose tetrad up to a factor 2. *Response.* This is now stated.

**m5. The archive's diagram as a source.** Theorem 1 depends on an HTML file. *Response.* The theorem now defines the blocks mathematically. The cell-by-cell comparison with the diagram is a check, not the definition.

## Assessment after revision

The revised proof is correct and states its claims at their true strength:
- the Sierpiński blocks are a null rotation at TetA;
- TetB adds the total inversion;
- the Field Origin is the even projection;
- K = 4 is the null rotation's character, which the identity and some loxodromic elements share.

It identifies the operator G is read from; it does not derive G or K. Its most useful new finding is M2: on the vector block, the TetB sign behaves as PT, not as spatial parity. That is a definite question for the framework.

## Checks

The verification script grows from 33 to 41 checks, adding:
- M₊₁ = ρ(A ⊗ A);
- M₋₁ = ρ(−A ⊗ A) and M₀ = ρ(A ⊗ A)Π₊;
- the parity trace 1 versus 13;
- the loxodromic element with χ = 4;
- the classification of real-trace elements;
- the boost conjugation of A(τ);
- the limit of the light-ray flow;
- the dyad normalisation.
