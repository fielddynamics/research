# The Tiled Cube Read With Both Roots

*Field Dynamics Research, research note, 2026-11-22. Status: research, not a proof. Verification: `python3 verify_two_roots.py` (16 checks, exact).*

## Why this note exists

The proof [`proofs/tiled-cube-affine-connection/`](../../../proofs/tiled-cube-affine-connection/) built 64 couplings from TetA's faces alone and split them 40 + 24 with all 64 inside TetA. That contradicts what GFD has already established about the connection:

$$64 = 16 \text{ shared} + 24 \text{ TetA} + 24 \text{ TetB},$$

with TetA alone (one root, torsion-free) giving $16 + 24 = 40$. The proof is under revision. This note goes back to the established results, finds where the proof departed from them, and records what the tiling does and does not add.

## What GFD has already established

| Result | Where | What it says |
|---|---|---|
| The index grid | [Gram paper](../../../papers/gram-matrix-of-tetrad-equation/), Parts III–IV; [proof](../../../proofs/gram-matrix-tetrad-equation/) | Each slice $\Gamma^\lambda{}_{\mu\nu}$ (fixed $\lambda$) is 6 upper + 4 diagonal + 6 lower. Diagonal shared, one triangle TetA, the other TetB: $24 + 16 + 24$. Torsion-free keeps $16 + 24 = 40$ and drops TetB's 24. The proof version adds: the triangles depend on the ordering of the basis; what is invariant is that the lower-index swap $\tau$ fixes the diagonal and exchanges the two 24s. |
| Root-blindness | [Letter 2](../../../papers/letter-2-other-half-of-gravity-torsion/) | The metric cannot tell TetA from TetB, so neither can a torsion-free connection. Torsion is the connection's only carrier of the TetA/TetB distinction. |
| TetB's step is the transpose | [Chiral holonomy](../../../proofs/chiral-holonomy-closed-frame/) | Transport uses $R$ leaving a TetA corner and $R^T$ leaving a TetB corner. The transpose keeps the diagonal and swaps the triangles: the same exchange as the grid. |
| The lower pair lives on the TetA–TetB links | [Coupling algebra](../../coupling-algebra/), Result 10 | Send $(a, b)$ to the link from TetA's corner $v_a$ to TetB's corner $-v_b$. The diagonal goes to the 4 Field Origin links, the off-diagonal to the 12 cube edges, and **the swap $(a,b) \to (b,a)$ is exactly the exchange of roots** (the antipode). Kept by all 48 symmetries of the cube. |
| The 16 channels are the 16 links | Coupling algebra, Result 8 | TetA's face opposite $v$, slot $w$, goes to the link $w \to -v$: the 12 outer channels are the 12 cube edges (spatial), the 4 cores the 4 Field Origin links (gravitational). |
| Open | Coupling algebra, open direction 3 | The upper index has not been placed. Placing it "would put all 64 components on the cube". |

So the question the tiling proof should have answered was open direction 3: the lower pair is already placed, on the links, with the swap as the exchange of roots. What is the upper index?

## Where the proof went wrong

The proof's couplings were right. Its index roles were not.

- **It used the wrong pair as the antisymmetric pair.** It made the face the upper index and swapped the channel with the leg of the coupled cube. That swap keeps the face, so it never changes the TetB end of the link (check 3.1). It is a reflection inside TetA, not the exchange of roots. That is why all 64, torsion included, came out as TetA's.
- **The framework's pair is (slot, face).** A channel is slot $\mu$ of the face opposite $v_\nu$. It runs from TetA's corner $v_\mu$ to the piercing TetB corner $-v_\nu$. That is Result 10's link, and swapping $\mu$ and $\nu$ reverses the link: the exchange of roots (checks 1.1–1.4, 3.2).
- **The labelling question was a symptom.** Theorem 6's closure-versus-uniform result was trying to find TetB through which cubes a coupling reaches. In the framework, TetB enters through the link itself.
- **Underneath: not enough reading first.** Results 8 and 10 of the coupling algebra already placed the 16 channels and the lower pair, and named the upper index as the open step. The proof did not build on them.

The 64 couplings are the same objects in both readings. Reassigning the roles only permutes the index slots, so the counts and the representations are unchanged (check 3.3). What changes is which 24 is torsion.

## What the tiling adds, read correctly

1. **Each cube-edge link is a shared solid, and both chambers open onto it.** The octahedron on the edge from $v_\mu$ to $-v_\nu$ is the link. In each cube the edge wedge has two faces: TetA's channel and TetB's channel on that link. Both are held by the same 4 cubes (check 2.1). So the 12 spatial links are where TetA and TetB meet across the tiling.
2. **Each Field Origin link has TetA at one end and TetB at the other.** TetA's core reaches the cube and its 3 face neighbours on the $-v_a$ side. TetB's core reaches the cube and the 3 on the $+v_a$ side (check 2.2). This is the gravitational channel, the diagonal through the Field Origin.
3. **One formula gives the four cubes of every channel,** $c = -v_\nu + \varepsilon v_\lambda$ with $\varepsilon = +1$ iff $\lambda \in \{\mu, \nu\}$. So the four cubes of a link come one along each leg $\lambda$ (check 2.3). The leg $\lambda$ is the natural candidate for the upper index.
4. **With that reading the framework's count appears on the tiled cube** (checks 4.1–4.4):
   - **shared 16:** the Field Origin links (slot = face, the cores) × 4 cubes. The exchange of roots fixes them.
   - **24 + 24:** the 12 cube-edge links × 4 cubes = 48, paired by the exchange of roots into 24 pairs (a link and its antipode).
   - **per slice:** 4 + 6 + 6, the Gram grid.
   - **one root:** cannot tell a link from its antipode, so it identifies each pair: 16 + 24 = 40. Both roots: 64.

## What does not yet fit

**The upper index under the exchange of roots.** The exchange sends the coupling to cube $c$ through link $(\mu, \nu)$ to the coupling to cube $-c$ through link $(\nu, \mu)$. With the holder labelled by the formula, that cube is along a different leg: the exchange acts on the whole triple as the double transposition that swaps $\mu, \nu$ and the other two legs (check 5.1). Of the four labellings of holders by legs that respect TetA's symmetry, none is kept by the exchange (check 5.2).

So, with the holder as the upper index:
- the lower pair is exactly right: the swap is the exchange of roots, as Result 10 requires;
- but TetB's reading is the transpose of TetA's only up to a relabelling of the upper index that depends on the link.

This may not be a failure. [Note 14 of `bimond-gfd/`](../../bimond-gfd/14_where_the_roots_live.md) shows that the second root is read where the frame index is left free: the torsion $T^a{}_{\mu\nu}$ of the second root is $P^a{}_b T^b{}_{\mu\nu}$, so the exchange of roots *does* act on the upper index, as the frame parity (rank 1, odd). It also warns that in coordinate indices that sign cancels. So the right requirement is not "the upper index is unchanged" but "the exchange acts on the upper index as the frame parity". Whether the link-dependent relabelling of check 5.1 is that action, read on the legs, is the open test.

## Next steps

1. **Read the remaining sources on the upper index** before building anything: the torsion proof (how $S_4$ acts on the slice index), the rest of note 14 (its Results 4–5), Paper IX's time faces, and Letter 3's supplement.
2. **Test the candidates for the upper index** against the requirement from note 14: the exchange of roots acts as the swap of the lower pair, and on the upper index as the frame parity. Candidates are the holder leg (check 5.1 gives a link-dependent relabelling, to be compared with the frame parity), and the face or corner of TetA (Result 10's suggestion).
3. **Only then rewrite the proof.** Its geometric content (the honeycomb, the four cubes per channel, the formula) stands. Its sectors, torsion reading and Theorem 6 have to be rebuilt on the links.

## Run

```
python3 verify_two_roots.py      # 16/16
```
