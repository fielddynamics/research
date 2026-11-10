# Pre-registration 2: does the 10/40 coincidence extend to torsion?

*Written and committed before any computation.*

## Background

In the registered junction-network model ([`NETWORK_MODEL_RESULT.md`](NETWORK_MODEL_RESULT.md)), det(B_s + E) = 0, 10, 40 at s = +1, 0, −1. Here E is the **symmetric** tree adjacency. The values 10 and 40 coincide with Letter 3's symmetric counts: per face 16 = **10** + 6, and in total 64 = **40** + 24 (Christoffel). That was noticed after the fact and is not claimed.

## Hypothesis

If the coincidence is structural, then the **antisymmetric** counterpart of the tree coupling should give the antisymmetric (torsion) counts.

## The variant (fixed in advance)

Everything as in [`NETWORK_MODEL_PREREG.md`](NETWORK_MODEL_PREREG.md), except that E is replaced by its antisymmetric form:
  E⁻ = E_down − E_up,
i.e. entry (child, parent) = +1 and entry (parent, child) = −1.
The blocks B_s and the node order are unchanged.

## Prediction and criteria

- **Success:** det(B₀ + E⁻) = 6 **and** det(B₋₁ + E⁻) = 24, exactly, with those signs and in that order.
- **Failure:** anything else.
- det(B₊₁ + E⁻) is reported, with no prediction.

## What a success would and would not mean

A success would make the 10/40 ↔ 6/24 pattern a registered result linking the junction network to Letter 3's Christoffel/torsion split. It would still not give 17/13. A failure retires the 10/40 observation as coincidence.
