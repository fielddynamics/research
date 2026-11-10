# Result: the pre-registered junction-network model

*Model and success criterion: [`NETWORK_MODEL_PREREG.md`](NETWORK_MODEL_PREREG.md), committed before computing (0b677cc). Computation: [`network_model.py`](network_model.py), exact integer arithmetic.*

## Outcome: failure

| Quantity | Result |
|---|---|
| det(B_s + E) at s = +1, 0, −1 | **0, 10, 40** |
| Prefactor P = det(B₀ + E)/det(B₋₁ + E) | **1/4**, not 17/13: **the registered test fails** |
| Ratios among the six equal to 17/13 | none |
| Closure amplitude at s = +1, Z = α²¹ det(B₊₁ + E) | **0**: the model does not even produce α²¹ for the TetA read |
| Variant (a), tree edges down only | dets 1, 0, 1: no 17/13 |
| Variant (b), tree edges up only | dets 1, 0, 1: no 17/13 |
| Variant (c), symmetric Sierpiński blocks | dets 0, 0, 0: no 17/13 |

## What the failure says

The most direct network built from the archive's own structure was tried:
- nodes: the 21 junctions;
- couplings: the author's Sierpiński blocks plus the tree of the 64-channel walk;
- one α per junction and per traversal;
- closure read as a determinant.

It does not produce G's prefactor, and at s = +1 it cancels completely. So:

1. **17/13 has no mechanism in this network.** In the archive it remains what `g_from_the_closure_climb.md` says it is: a ratio of counts chosen by a combination rule, not an amplitude.
2. **The determinant reading of atomic closure is not automatically consistent with the coupling structure.** Once the levels are coupled to each other, the s = +1 configuration has zero amplitude. Any future mechanism has to explain why the levels act as independent blocks, which is the only arrangement in which the traces 21, 17, 13 survive.
3. Together with Part VI (only the diagonal reaches G) and Part VII (the loop factor needs the rotation), this narrows what a derivation of G could look like. The three integers survive only if the 1, 4 and 16 blocks do not talk to each other.

## A post-hoc observation, recorded and not claimed

The two non-zero determinants are 10 and 40. These are the per-face symmetric count and the Christoffel count of Letter 3 (16 = 10 + 6 per face; 64 = 40 + 24). This was noticed **after** the computation, and nothing in the registration predicted it. By the standard this work has used throughout, it counts for nothing unless a new registration predicts it in advance, for example the torsion counts 6 and 24 from a stated variant.

---

## Pre-registration 2: the torsion variant ([`NETWORK_MODEL_PREREG_2.md`](NETWORK_MODEL_PREREG_2.md), committed c461a96 before computing)

| Quantity | Predicted | Result |
|---|---|---|
| det(B₀ + E⁻) | 6 | **10** |
| det(B₋₁ + E⁻) | 24 | **0** |
| det(B₊₁ + E⁻) | (no prediction) | 40 |

**Outcome: failure.** The 10/40 observation is retired as a coincidence.

**Why the numbers come out mirrored.** Exactly,
  det(B_s + E⁻) = det(B₋ₛ + E) = (1 + s)(s³ + 4s² + 5s + 10).
Every parent–child loop in the tree passes through the level-1 block, so reversing the sign of the return edges is equivalent to s → −s. This is a property of the network's shape, not a physical statement. The polynomial is not the coupling polynomial 1 + sK + K².

## Where this leaves the network approach

Two pre-registered tests, two failures. A determinant on the junction network, built from the archive's own structure, carries neither G's prefactor nor Letter 3's counts. Varying the network further would be fitting, so this family of models is closed here.
