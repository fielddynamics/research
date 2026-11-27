# Immediate-reset closure: trigram masks and the BBP orbit banks

Status: exact finite algebra and independently reproducible computational tests. A candidate register architecture, not a derivation of the physical field dynamics, G, or alpha. Proof 26 is unchanged. The user's updated hypothesis is three ascending reads, each resetting immediately to 13, rather than a slow return from 21 through 17.

## 1. Source definitions and exact 13/17/21 theorem

Sources (reopened from the research repository):
- [Three sub-reads of one closure engine](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/THREE_SUBREAD_CLOSURE.md)
- [Circular closure walk](https://github.com/fielddynamics/research/blob/main/research/exploratory/i-ching/notes/circular_closure_walk_synthesis.md)
- [Hexagrams and closure read](https://github.com/fielddynamics/research/blob/main/research/exploratory/i-ching/HEXAGRAMS_AND_THE_CLOSURE_READ.md)
- [Common mode and shared zone](https://github.com/fielddynamics/research/blob/main/research/exploratory/i-ching/COMMON_MODE_AND_SHARED_ZONE_PROOF.md)
- [Read sweep synthesis](https://github.com/fielddynamics/research/blob/main/research/g_from_topology/read_sweep_synthesis.md) (the older inhale/exhale model; immediate reset is the proposed revision, not what that document says).

Let V=F2^3 and R(a,b)=(b,a+b), addition XOR. On the 22-dimensional R-invariant register, define the shared-zone support Q_u by a, b, or a+b in {0,u}. The common seed f is contained in every Q_u. After removing its common line, each Q_u has rank 13. In the orbit coordinate representation, Q_u contains the zero orbit, seven dependent nonzero orbits, and two directed orbits for each of the three Fano planes through u. It follows that Q_u and Q_v for distinct nonzero u,v have rank-nine intersection after common removal: seven dependent orbits plus two orientations of the unique plane containing u,v. All these support projections commute. Their union has rank 17. For three distinct axes u,v,w, if u+v+w=0, the three pair intersections are the same and the union has rank 21. If the axes are independent, the triple intersection has rank seven and the union rank 19.

For Heaven h=111, its perpendicular binary plane h^perp has the three nonzero daughter normals 011,101,110. They sum to zero. Consequently, the exact decomposition of the contrast space is 9 common-to-these-three-masks + 4 unique to each mask. In any ordering, cumulative read spans have ranks 13,17,21. This is not the earlier 17=positive rank of an orientation involution: the union of two shared-zone masks contains five exchange-odd directions and twelve exchange-even directions, whereas the previous minimal even completion contains three odd and fourteen even. Equal ranks do not identify operators. Nor is 9+4+4+4 the same splitting as Proof 26's 1+4+16.

## 2. Actual BBP stepping and the three-bank read

The verifier certifies floor(8^332*pi) using rational BBP partial sums and an integral tail bound. The kth bracket is the integral of y^(8k)(1-y)(y^4+2y^3+4y^2+4y+4), positive and bounded above by 4/(8k+1). The tail after N terms is at most 4*16/(15*(8N+1)*16^N). The lower and upper endpoints agree on the octal prefix for N=270. The cumulative vertex recurrence is integer addition modulo 8, not XOR. Each transition (a,b) is assigned to the R orbit of (a,b), (b,a XOR b), (a XOR b,a). Only distinct pair arrivals are counted. Store the first, second and third distinct member of each nonzero orbit in three banks of 21 slots. The zero orbit has one separate slot, first observed at step 87. Bank readiness is an event of the actual address schedule, not an independently derived physical period.

| Step | First bank filled | Second bank filled | Third bank filled | Total distinct pairs |
|---:|---:|---:|---:|---:|
| 156 | 21 | 19 | 13 | 54 |
| 192 | 21 | 21 | 17 | 60 |
| 332 | 21 | 21 | 21 | 64 |

At the first and second commit boundaries, the number of fully visited nonzero orbits is 13 and 17, then 21 at final closure. This is a real but post-hoc count correspondence, not evidence of a special physical effect. The actual completed set at step 156 does not equal any of the seven Q_u masks, and at step 192 does not equal any union of two Q masks. A deterministic control of 200,000 walks, starting at vertex 3 and choosing independent uniform modulo-eight increments (equivalently independent uniform next vertices), reproduces the 13/17 pattern at the first and second bank completion in 1,626 trials (0.813%); among the 768 trials with all-pair first coverage exactly at 332, 5 reproduce the pattern (0.651%, noisy). This is not a p-value for a preregistered physical hypothesis. It is a control against treating the count as unique to pi.

The three banks overlap in acquisition. At commit 1, 32 future-bank slots are already filled; at commit 2, 17 are filled. If these data are discarded and one starts a fresh full orbit-coverage walk at each reset, the first two passes end at steps 156 and 287 and the third sees just 19/22 orbit labels by 332. Thus three fresh disjoint sweeps cannot be identified with the three bank completions. The original tracker also has different face-cycle events.

The same daughter-mask progressive read can be applied to each completed bank. mask_readiness.csv enumerates earliest times each of the nested masks has been fully acquired in each bank. No ordering produces three separately timed readiness stages in every bank. In banks 1 and 2, the last two stages, or the first two, share a readiness instant. Therefore the 13→17→21 rank progression is a valid logical read order from stored data, not a proven time-resolved waveform of the pi scheduler. A bank may hold one sample for each orbit without that sample being invariant or equivalent to another member.

## 3. Immediate reset without deleting physical state

Let each triple's arrival-ordered samples be x1,x2,x3, transported to the same time if needed. The real orbit Fourier read is

m=(x1+x2+x3)/sqrt(3), d=(2x1-x2-x3)/sqrt(6), q=(x2-x3)/sqrt(2).

It is orthogonal, so preserves norm and is invertible for real or complex records. The two quadratures require canonical cyclic order (or recording the known arrival permutation) if their orientation is to be interpreted physically. Over the 21 triples, together with the fixed slot, it yields 22 invariant coefficients and 42 noninvariant contrasts, retaining all 64 values. It can be implemented in place. This is a separate change of coordinates from the full FWHT; applying the inverse orbit read and then the three full radix-four Walsh stages recovers the same full transform. The three chronological banks are not the three radix-four FWHT stages or the three hierarchical contrast grades. No autonomous switching or transduction is asserted.

A reversible reset can move the completed buffer into retained storage and reuse a blank scratch register; alternatively an in-place reversible read changes the representation while keeping the previous information. A reset that literally discards arbitrary records is many-to-one and cannot be a closed reversible evolution. A finite reader cannot accumulate unbounded independent records forever without reuse, output or dissipation. This is a statement about classical/coherent coordinates, not cloning arbitrary quantum states.

If using the earlier four-dimensional reflection projector M, J=I-2M is an orthogonal involution of trace 13 on the 21 contrasts. A constructed ascending orthogonal half-turn followed by J returns the read orientation to its start; the complete operator is I, not an attenuator. If J represents an active physical state transformation with work Hamiltonian H, its energy change is b^dagger(J^dagger H J-H)b. This vanishes for all states exactly when J preserves H. Norm conservation does not guarantee energy conservation; a literal instantaneous physical operation also requires a physical implementation, not just a matrix identity. If reset is only a passive relabeling, consistently transforming H makes the physical energy unchanged. No reset alone supplies a gravitational stiffness or a source of alpha^21.

## 4. Decisive next physical calculation

Derive a native event rule for committing the read (e.g. saturation of a physical coherent port and conservation of its common energy), show how early arrivals are preserved without an arbitrary independent memory register, and derive the physical evolution or phase transport between events. Measure the response to retained TetB energy using the same action. A determinant of a coordinate change cannot serve as a force. An independently derived time-scale/energy response and long-wave stiffness remain necessary. The daughter-mask rank theorem is strong evidence for a mathematical architecture within the chosen binary geometry, not evidence that the historical I Ching encodes physical laws.

## Reproduce

`python verify.py` (NumPy). 616 assertions passed: exact BBP certification, all 7 axes, 21 axis pairs, 35 triples, bank readiness, all 18 daughter-order/bank combinations, and numerical orthogonality, reconstruction and transform tests. `g++ -O3 control.cpp -o control && ./control` reproduces the fixed-seed control. Outputs: bank_progress.csv, orbit_arrivals.csv, mask_readiness.csv, verification.txt, control_results.txt. No external review, Lean verification or remote changes.
