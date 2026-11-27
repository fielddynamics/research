# Gravity, time faces, recursive Field Origin and BBP

*Gravity Field Dynamics (GFD) · Field Dynamics Research · November 2026*

Twelve research continuations on how G arises from the Field Origin: the native settlement vertex, the coupled time faces and the lapse, the nested stellated octahedron inside the Field Origin, and the BBP read of π at the core. They follow on from the eleven notes in the [parent folder](../README.md).

These are conditional finite-domain mathematics, not numbered proofs. Each note separates exact finite-model statements from candidate physical premises. They do not complete a derivation of G. Proof 26 and the covariant action are unchanged.

## Why this matters

How G is constructed is known (21/17/13 from the coupling polynomial, α²¹ over the 1 + 4 + 16 contrast grades). What is still open is how settlement and the read realize it. These notes test concrete routes for that: whether the read acts on the physical clock (the lapse N, with u = ln N), whether a recursive core can carry the source, and what the BBP closure at the Field Origin contributes. Each route ends in either an exact result or a stated obstruction, so the open steps are narrowed rather than assumed.

## Reading order

| # | Folder | Note | Checks |
|---|---|---|---:|
| 1 | [01-g-native-settlement-vertex](01-g-native-settlement-vertex/) | [G from native settlement: port-gain obstruction and the collective source vertex](01-g-native-settlement-vertex/G_NATIVE_SETTLEMENT_VERTEX.md) | 25 |
| 2 | [02-g-time-face-lapse](02-g-time-face-lapse/) | [G from coupled time-face clock susceptibility](02-g-time-face-lapse/G_TIME_FACE_LAPSE.md) | 21 |
| 3 | [03-g-native-clock-universality](03-g-native-clock-universality/) | [Native Field Origin clock universality and the G normalization](03-g-native-clock-universality/G_NATIVE_CLOCK_UNIVERSALITY.md) | 33 |
| 4 | [04-g-time-face-constraint](04-g-time-face-constraint/) | [Coupled time-face constraint: recursive clock susceptibility and G](04-g-time-face-constraint/G_TIME_FACE_CONSTRAINT.md) | 23 |
| 5 | [05-g-clock-constraint-audit](05-g-clock-constraint-audit/) | [Coupled time faces: metric constraint, susceptibility and a test of G](05-g-clock-constraint-audit/G_CLOCK_CONSTRAINT_AUDIT.md) | 32 |
| 6 | [06-g-native-inventory-response](06-g-native-inventory-response/) | [Native inventory response of the coupled time faces](06-g-native-inventory-response/G_NATIVE_INVENTORY_RESPONSE.md) | 43 |
| 7 | [07-g-native-phase-and-lapse](07-g-native-phase-and-lapse/) | [Native phase dynamics and the static lapse obstruction](07-g-native-phase-and-lapse/G_NATIVE_PHASE_AND_LAPSE.md) | 29 |
| 8 | [08-g-recursive-origin-clock](08-g-recursive-origin-clock/) | [Recursive Field Origin: geometric refinement and the lapse response](08-g-recursive-origin-clock/RECURSIVE_ORIGIN_CLOCK.md) | 38 |
| 9 | [09-g-recursive-native-boundary](09-g-recursive-native-boundary/) | [Recursive native Field Origin: boundary antiresonance and the clock read](09-g-recursive-native-boundary/RECURSIVE_NATIVE_BOUNDARY.md) | 56 |
| 10 | [10-g-bbp-core-settlement](10-g-bbp-core-settlement/) | [BBP core closure: phase, logarithmic response and recursive stiffness](10-g-bbp-core-settlement/BBP_CORE_SETTLEMENT.md) | 27 |
| 11 | [11-g-bbp-native-rotation](11-g-bbp-native-rotation/) | [BBP, native exchange and the information curvature of recursive settlement](11-g-bbp-native-rotation/BBP_NATIVE_ROTATION.md) | 63 |
| 12 | [12-g-five-physics-approaches](12-g-five-physics-approaches/) | [Five algebraic investigations of the recursive BBP Field Origin](12-g-five-physics-approaches/FIVE_PHYSICS_APPROACHES.md) | 52 |

Total: 442 checks, all passing.

Folder 12 also keeps the snapshots of notes 9 and 11 that it was written against (identical copies), so it stands on its own.

## Reproduce

Each verifier runs from its own folder and writes its log there (`verification.txt`, or `verification_output.txt` in folder 08). Requires numpy, scipy, sympy, mpmath and matplotlib.

```
cd 01-g-native-settlement-vertex && OPENBLAS_NUM_THREADS=1 python verify_native_settlement.py > verification.txt
```

The same pattern applies to each folder's `verify_*.py`. Some verifiers also regenerate their figures. `SHA256SUMS.txt` lists the checksums of every file as added.
