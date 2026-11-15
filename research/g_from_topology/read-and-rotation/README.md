# The Read and the Rotation

*Research toward a proof: G's three numbers 21, 17 and 13 are one identity read four ways. That identity splits into a root-blind part and a root-resolving part, and it is carried by the vortex–antivortex pairs of the cube's rotations · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`gravitational-constant` `coupling-polynomial` `cyclotomic` `rotation` `vortex` `root-blind` `research`

---

This note is research, not yet a proof. Each part below carries the status of its claims. The script [`verify_read_and_rotation.py`](verify_read_and_rotation.py) checks every statement exactly (50 checks, [output](verify_output.txt)).

The script tags each check in the same way as the coupling algebra's recertification:

| Tag | Meaning |
|---|---|
| CLASSICAL | standard mathematics, restated for this setting |
| NEW | a statement this note adds |
| AUTOMATIC | true for reasons that carry no information about GFD |
| OPEN | a step that is probed, not derived |
| READING | how an exact result matches the framework's assignments (interpretation) |
| COINCIDENCE | exact, but special to the values; not to be built on |

It builds on:
- [`../g_matrix_synthesis.md`](../g_matrix_synthesis.md): the graded operator and its traces.
- [Coupling algebra, Result 13](../../coupling-algebra/): the coupling polynomial is the characteristic polynomial of the cube's rotations, f(K, s) = det(K − R_θ) with s = −2 cos θ. That result also gives the crystallographic restriction and the class table of the cube's symmetries.
- [Vortices of the stellated octahedron](../../../proofs/vortices-of-the-stellated-octahedron/): the winding eigenvalues.

## The question

GFD's Newton constant is

$$G = \frac{(3+1)^2+1}{3(3+1)+1}\,\alpha^{1+(3+1)+(3+1)^2}\,\frac{\hbar c}{m_e^2} = \frac{17}{13}\,\alpha^{21}\,\frac{\hbar c}{m_e^2}$$

with K = 3 + 1 = 4, D = 3, and f(K, s) = 1 + sK + K² = 21, 17, 13 at s = +1, 0, −1. The archive reads these numbers in four ways, and has not shown that the four are one:
- as traces of the graded operator;
- as cyclotomic values;
- as points of the projective plane over 𝔽₄;
- as characteristic polynomials of the cube's rotations.

## A. The read is the rotation (CLASSICAL and NEW)

$$1 + K + K^2 = \frac{K^3 - 1}{K - 1} = (K - \omega)(K - \bar\omega) = \det(K - R_{120^\circ})$$

Each expression is a different reading of 21:

| Expression | Reading |
|---|---|
| 1 + K + K² | the depth-3 read: scalar, four legs, sixteen couplings |
| (K³ − 1)/(K − 1) | the number of points of PG(2, 4) |
| (K − ω)(K − ω̄) | the product over the nontrivial cube roots of unity |
| det(K − R₁₂₀°) | the characteristic polynomial at K of the 120° rotation, whose eigenvalues are ω and ω̄ |

The trace of the graded operator at TetA is the fifth reading. They agree for one reason: the read has D = 3 levels, and the closure rotation has order D = 3. That rotation is the one about a body diagonal, the time axis, which turns the three spatial legs.

## B. Why D = 3 gives exactly one winding pair (CLASSICAL and NEW)

Two standard facts combine:
- The depth-n read (Kⁿ − 1)/(K − 1) is a single cyclotomic factor exactly when n is prime.
- A cyclotomic factor is one conjugate pair of roots, one vortex–antivortex pair, exactly when φ(n) = 2, that is, n = 3, 4 or 6.

So the depth-D read is exactly one winding pair only for D = 3. That is also the solution of the uniqueness equation 2(D + 1) = 2^D. The note records the coincidence of the two conditions and claims no link between them (AUTOMATIC).

## C. The ring determinants (CLASSICAL and NEW)

On a ring of n sites, det(K − shift) = Kⁿ − 1. At K = 4:

| Ring | det | Factors | Winding pair |
|---|---|---|---|
| 3 | 63 | 3 × 21 | 21 |
| 4 | 255 | 3 × 5 × 17 | 17 |
| 6 | 4095 | 3 × 5 × 13 × 21 | 13 |

The factor K − 1 = 3 is the non-winding mode. Each structural number is the determinant on one winding pair. 63 is also the number of nonzero vectors of 𝔽₄³, so the archive's 64 = 3 × 21 + 1 is the same factorisation.

## D. The parity split (NEW)

$$f(K, s) = E + sO, \qquad E = 1 + K^2 = 17 \ \text{(scalar and couplings)}, \qquad O = K = 4 \ \text{(the legs)}.$$

Three facts follow:
- **The root exchange is K → −K.** f(−K, s) = f(K, −s), so TetB is TetA with the legs reversed, M → −M. E is even in K and O is odd.
- **The Field Origin is the average of the two roots.** f(K, 0) = (21 + 13)/2 = E: the legs cancel, as (M + (−M))/2 = 0. This is why 17 is the mean of the closure climb.
- **It is Letter 2's structure.** The frame flips with the root, and its Gram matrix 4I − J does not. That is checked.

## E. The winding eigenvalues on the cube's corners (NEW)

| Class | On the corners | \|K − λ\|² | The chambers |
|---|---|---|---|
| C₃, the closure rotation | ω, ω̄ (twice: two 3-cycles) | 21 | kept |
| S₄ and C₄, the 4-fold elements | i, −i (twice) | 17 | S₄ keeps them; C₄ exchanges them |
| S₆ = −C₃ | −ω, −ω̄ (once: one 6-cycle) | 13 | exchanged |

These are the vortex proof's winding eigenvalues:
- ω for the leg (Triforce) vortices, under C₃;
- i for the core vortices, under the rotoreflection S₄.

Both of those elements keep the chambers. S₆ and C₄ exchange them, so they are symmetries only when TetA and TetB are alike. With the chambers distinct, the vortices that exist are those of the 21- and 17-classes. The 13-class maps a TetA configuration onto a TetB one, the map between the roots.

Only rotations of orders 3, 4 and 6 have non-real eigenvalues, so only they can carry a circulating state; orders 1 and 2 (s = ±2) cannot. This is the crystallographic restriction.

## F. G in parity form and in vortex form (NEW)

$$\alpha_G = \frac{G m_e^2}{\hbar c} = \frac{E}{E - O}\,\alpha^{E+O} = \frac{|K - i|^2}{|K + \omega|^2}\,\alpha^{|K-\omega|^2}$$

In words, it is the root-blind read over TetB's read, times α to the power of TetA's full read. The exponent is the leg vortex's pair. The prefactor is the quarter-turn pair over the exchanged-leg pair.

The hierarchy exponent is E + O − 1 = K(K + 1) = 20. The tree-level value is 6.6665 × 10⁻¹¹, 0.12% below the measured value, as in the parent folder.

## H. The connection's split: the root label weights the lower-index swap (NEW)

The torsion-free condition is the swap τ of a connection's two lower indices: Christoffel is its symmetric part, torsion its antisymmetric part. On one face (the 16 components Γᵃ_bc at a fixed upper index) the symmetric part has dimension 10, the antisymmetric part 6, and Tr τ = K = 4. Then:

$$f(K, s) = 1 + \mathrm{Tr}_{\text{face}}(1 + s\,\tau) = 1 + \mathrm{Tr}_{\text{face}}\big[(1+s)\,P_{\text{Christoffel}} + (1-s)\,P_{\text{torsion}}\big].$$

| State | Value | What it reads |
|---|---|---|
| TetA (s = +1) | 21 = 1 + 2 × 10 | the Christoffel part, twice |
| TetB (s = −1) | 13 = 1 + 2 × 6 | the torsion, twice |
| Field Origin (s = 0) | 17 = 1 + 16 | the whole face, once |

So E = 1 + (the face) and O = Tr τ = (40 − 24)/K. The legs block's size is the swap's trace, the excess of the kept components over the set-aside ones per face. This is the operator statement behind Letter 3's per-face identity, 10 = (f(K, +1) − 1)/2 and 6 = (f(K, −1) − 1)/2.

*Reading.* It matches the framework's assignments:
- the Christoffel sector is general relativity, the TetA partition;
- the torsion carries the second root, TetB (Letter 3);
- the Field Origin's whole-face read is field closure, both parts active.

In connection terms,

$$\alpha_G = \frac{1 + (\text{face})}{1 + 2\,(\text{torsion per face})}\;\alpha^{\,1 + 2\,(\text{Christoffel per face})} = \frac{17}{13}\,\alpha^{21}.$$

Over the whole connection, (K + 64)/(K + 2 × 24) = 17/13 and (K + 2 × 40)/K = 21.

**Routes that fail, recorded:**
- **Weighting only the torsion by s.** Tr(P_sym + s P_anti) over the connection gives 64, 40, 16, a ratio of 5/2, not 17/13. The coupling polynomial weights the swap, not the torsion subspace.
- **Contracting the connection with the time direction.** This gives 16, 4 and 1 components, but the torsion vanishes in the 4-block by antisymmetry, so it can't send the torsion to the legs.
- **The swap on PG(2, 4).** It gives 21 = 13 + 8. The 13 is the coupling algebra's flagged coincidence, and 8 is 2K, not K (COINCIDENCE).

So no map sends the torsion to the legs block. What the split determines is the weight of the swap.

## I. Four coupled faces: the frame duplicated by four (NEW)

Over the four coupled faces the coupling polynomial multiplies out to the tetrad formalism's three objects:

$$K\,f(K, s) = K + s\,K^2 + K^3 = \underbrace{4}_{\text{legs}} + s\,\underbrace{16}_{\text{tetrad } e^a{}_\mu} + \underbrace{64}_{\text{connection}}, \qquad 84,\ 68,\ 52 = 4 \times (21, 17, 13).$$

The root sign sits on the tetrad, which flips with the root (M → −M). The connection's swap-fixed components Γᵃ_bb are indexed like the tetrad, and there are the same 16 of them, which is why part H's Tr τ and this term agree.

*Reading.* Per face, the four coupled faces share the read equally:
- the scalar 1 is the face's own leg (each face of a tetrahedron is opposite one leg);
- sK is the face's copy of the frame;
- K² is the face's 16 components.

So the division by K removes a fourfold duplication. It does not discard three faces.

**Self-similarity.** Four coupled faces, each with a full 21-read, joined at one root, give the four-level read:

$$1 + K + K^2 + K^3 = 1 + K\,f(K, +1) = (1 + K)(1 + K^2) = 85 = 5 \times 17.$$

The Field Origin's value comes out of the four-face read: E = (K⁴ − 1)/(K² − 1).

**Each state is a geometric read:**

| State | Read | Branching |
|---|---|---|
| TetA | (K³ − 1)/(K − 1) = 21 | K, over three levels |
| TetB | (K³ + 1)/(K + 1) = 13 | −K: the legs reversed |
| Field Origin | (K⁴ − 1)/(K² − 1) = 17 | K², the frame duplicated by four at each step, over two levels; the leg level is silent |

So

$$\alpha_G = \alpha^{(K^3-1)/(K-1)}\;\frac{(K^4-1)/(K^2-1)}{(K^3+1)/(K+1)} = \frac{17}{13}\,\alpha^{21}.$$

## G. Open steps

| Step | Status |
|---|---|
| Why each level costs one factor of α | The parent folder's single physical assumption. Not addressed here. |
| The combination rule α^{TetA} × (Field Origin / TetB) | The parity form rewrites it as α^{E+O} E/(E − O). It does not derive it: the rule was fitted after the fact among 21 candidates ([`../g_from_the_closure_climb.md`](../g_from_the_closure_climb.md)). |
| E/(E − O) from the connection's split 64 = 40 + 24 | Answered by parts H and I. With the root label as the weight of the lower-index swap, E, E + O and E − O come exactly from one face's Christoffel and torsion parts. Over the four coupled faces the read is legs + s·tetrad + connection. The scalar 1 is the face's own leg, and the division by K removes the fourfold duplication (a reading, in part I). |
| Why the faces read in parallel | Open. G's exponent is the per-face read 21, not the whole 84. |
| Why the read branches K ways per level | Algebraically, K is the base of the read, and the identity of part A turns that read into the characteristic polynomial at K. The archive's own reason is the four legs and their sixteen couplings. A mechanism is still needed. |
| The one-loop factor 1 + α/2π | The parent folder's split α/2π = (2/17)(17α/4π) reads as (2/E)(Eα/(Kπ)), but it holds for any E (AUTOMATIC). No E/O reading found. |

## What a proof would state

The exact content of parts A to F would make a proof:
- **One identity.** The five readings of 21 are one identity.
- **One pair.** The depth-D read is a single winding pair exactly for D = 3.
- **The parity split.** The three states are the parity split of one read, with the root exchange K → −K and the Field Origin as the root average.
- **The vortex pairs.** Each state's value is |K − λ|² for the winding eigenvalue of its cube symmetry class. These are the vortex proof's eigenvalues, and only the chamber-keeping classes act when TetA and TetB differ.
- **Four coupled faces.** K f(K, s) = legs + s·tetrad + connection. The four-face read is (1 + K)(1 + K²), which contains the Field Origin's value. Each state is a geometric read with branching K, −K or K².
- **The connection's split.** The root label is the weight of the lower-index swap: f(K, s) = 1 + Tr_face(1 + sτ), so TetA reads the Christoffel part twice, TetB the torsion twice, and the Field Origin the whole face.
- **G rewritten.** G is expressible in the parity, vortex and connection forms.

The proof would not claim the physical steps in G. Those stay as the parent folder states them.

## Files

| File | Contents |
|---|---|
| [`verify_read_and_rotation.py`](verify_read_and_rotation.py) | 50 exact checks in parts A to I, tagged |
| [`verify_output.txt`](verify_output.txt) | Output |

## Reproduce

```
python verify_read_and_rotation.py      # 50/50 (needs sympy)
```
