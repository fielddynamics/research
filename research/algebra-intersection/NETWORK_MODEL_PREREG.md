# Pre-registration: G as a closure amplitude on the junction network

*Written and committed before any computation. Nothing below may be changed after the results are seen; changes require a new registration.*

## Goal

Compute G's prefactor from an amplitude, rather than assembling it from traces. The test is whether the network produces 17/13 without it being put in.

## The model (fixed from existing archive structure only)

**Nodes.** The 21 junctions of the closure read: levels 0, 1, 2 with 1, 4, 16 nodes, indexed by base-4 digit strings of length 0, 1, 2. Source: `g_matrix_synthesis.md` (Ψ₀, Ψ₁, Ψ₂) and the 4 × 4 × 4 walk in `field-closure/tetb_64_walk_of_field_closure.html`.

**Within-level couplings.** The author's diagram (`g_from_topology/g_three_sierpinski_blocks.html`): blocks S₀ = [1], S₁ = L⊗L, S₂ = L⊗⁴, with L = [[1,0],[1,1]]. A level-2 node with digits (d₁, d₂) uses bits (d₁, d₂) in that order. The parity parameter s multiplies the level-1 block, as in I_s:
  B_s = S₀ ⊕ s·S₁ ⊕ S₂.

**Between-level couplings.** The tree of the walk: each node at level k is joined to its 4 children at level k+1. E is the symmetric 0/1 adjacency of that tree (read goes down and the response comes back up). Unit weight.

**Amplitude.** Every junction and every traversal costs one α. The network operator is A_s = α (B_s + E) on the 21 junctions. Closure is atomic, so its amplitude is the determinant, the sum over configurations that use every junction exactly once:
  Z(s) = det A_s = α²¹ · det(B_s + E).

**Pre-registered predictions.**
1. *Exponent.* The leading power of α in Z is the junction count, 21. (Forced by construction; recorded, not claimed as a result.)
2. *Prefactor (the test).* Using the archive's own combination rule, numerator s = 0 and denominator s = −1:
  P = det(B₀ + E) / det(B₋₁ + E).
  **Success** if P = 17/13 exactly. **Failure** otherwise.
3. *Look-elsewhere.* All six ratios det(B_a + E)/det(B_b + E) for a ≠ b in {+1, 0, −1} are reported, with how many equal 17/13.

**Out of scope, stated in advance.** The loop factor 1 + α/2π. This model is an integer matrix times α, so (Part VI) it cannot produce 1/2π. A model of the loop needs the rotation of the read and is a separate registration.

**Secondary variants, reported but not counted as success:**
- (a) E directed parent → child only;
- (b) E directed child → parent only;
- (c) symmetric Sierpiński blocks, S + Sᵀ − I.

If the primary model fails and a variant succeeds, that is a look-elsewhere result and is reported as such.
