# The I Ching and the Stellated Octahedron

*Exploratory programme, Gravity Field Dynamics (GFD) · Field Dynamics Research*

`i-ching` `trigrams` `hexagrams` `binary` `combinatorics` `history-of-mathematics` `stellated-octahedron`

---

On 1 April 1703, Gottfried Wilhelm Leibniz received a letter from Peking. Its author, the Jesuit mathematician Joachim Bouvet, enclosed a woodcut of the 64 hexagrams of the *I Ching* in the arrangement attributed to the legendary sage Fu Xi. Leibniz had been developing binary arithmetic for two decades. In the diagram he recognised his own numbers, 0 to 63, written in broken and unbroken lines. Within a week he sent his *Explication de l'arithmétique binaire* to the Paris Academy, citing the hexagrams as an ancient anticipation of the binary system.

Leibniz saw that the *I Ching* counts. This folder asks a further question: **what geometry does it count?**

Gravity Field Dynamics derives a single geometric object as the local structure of the gravitational field: the stellated octahedron, two regular tetrahedra of opposite orientation (TetA and TetB) inscribed in a cube and sharing a centre, the Field Origin. Its eight vertices are the eight points of three-bit binary space. The notes and code collected here show that the classical organisation of the trigrams, including their division into a family of two parents and six children and their arrangement into opposing pairs, reproduces the geometry of that object exactly.

> **The source paper.** The material in this folder began as a section of Paper IX, *Complete Field Closure from Stellated Octahedron Topology*. The full manuscript, including that section ("Historical Correspondence"), is preserved here as [`Nelson_2026_GFD_Complete_Field_Closure_from_Stellated_Octahedron_Topology.pdf`](Nelson_2026_GFD_Complete_Field_Closure_from_Stellated_Octahedron_Topology.pdf). The version deposited on Zenodo ([`papers/09-complete-field-closure/`](../../../papers/09-complete-field-closure/)) omits the I Ching section, so that the published argument rests on the topology and the closure condition alone. The historical correspondence is offered here as independent corroboration, for readers who wish to examine it, and its checks are retained as Section 13 of [`run_all_validations_with_i-ching-intact.py`](run_all_validations_with_i-ching-intact.py).

## 1. The trigrams are the vertices of the cube

A trigram is three lines, each broken (yin, 0) or unbroken (yang, 1). Reading the lines from the bottom up as three binary digits places each trigram at a vertex of a cube, one bit per spatial axis. The correspondence is a bijection between the eight trigrams and the group $\mathbb Z_2^3$.

Dividing the vertices by the parity of their bit count (odd or even numbers of yang lines) splits the cube into two groups of four. Within each group every pair of vertices differs in exactly two bits, so each group is a regular tetrahedron. These are TetA and TetB, and together they form the stellated octahedron.

The classical texts already make this division. The *Shuo Gua* (*Discussion of the Trigrams*) arranges the trigrams as a family:

| Trigram | Name | Binary (bottom → top) | Family role | Chamber | Opposite |
|---|---|---|---|---|---|
| ☰ | Heaven (*Qian*) | 111 | Father | TetA | Earth |
| ☳ | Thunder (*Zhen*) | 100 | Eldest son | TetA | Wind |
| ☵ | Water (*Kan*) | 010 | Middle son | TetA | Fire |
| ☶ | Mountain (*Gen*) | 001 | Youngest son | TetA | Lake |
| ☷ | Earth (*Kun*) | 000 | Mother | TetB | Heaven |
| ☴ | Wind (*Xun*) | 011 | Eldest daughter | TetB | Thunder |
| ☲ | Fire (*Li*) | 101 | Middle daughter | TetB | Water |
| ☱ | Lake (*Dui*) | 110 | Youngest daughter | TetB | Mountain |

Three exact correspondences follow:

1. **The family is the parity partition.** The father and three sons have odd numbers of yang lines and form TetA. The mother and three daughters have even numbers and form TetB. The traditional yang and yin families are the two tetrahedra.
2. **The opposites are the body diagonals.** In the Fu Xi ("Earlier Heaven") arrangement the trigrams stand in four opposing pairs: Heaven–Earth, Thunder–Wind, Water–Fire, Mountain–Lake. Each pair is a vertex and its bitwise complement, the two ends of one of the cube's four body diagonals. All four diagonals cross at the centre, the Field Origin, and every pair joins a vertex of TetA to a vertex of TetB.
3. **The hexagrams are the complete state space.** A hexagram is an ordered pair of trigrams, so there are $8 \times 8 = 64 = 2^6 = 4^3 = K^D$ of them. They divide evenly by chamber: 16 TetA→TetA, 16 TetA→TetB, 16 TetB→TetA and 16 TetB→TetB. That gives 32 transitions within a chamber and 32 across the Field Origin.

The vierbein itself appears in the same table. The four face normals of TetA, written as sign patterns on the three axes, are $(+,+,+)$, $(+,-,-)$, $(-,+,-)$ and $(-,-,+)$: Heaven, Thunder, Water and Mountain. Their negations are Earth, Wind, Fire and Lake. The four fundamental dualities of the *I Ching* are the four directions of the tetrad and their reversals.

## 2. The closure walk

The second part of the work sets the trigram geometry in motion.

**The walk.** Write $\pi$ in base 8. Each digit, 0 to 7, is three bits and so names a trigram. A walker on the cube moves to the vertex given by the running sum of the digits modulo 8. Each consecutive pair of positions is a hexagram.

**Closure.** The walk is said to *close* when every one of the 64 hexagrams has occurred. For $\pi$ this happens at step 332, after 333 digits, with all 32 cross-chamber and all 32 within-chamber transitions realised. The walk then continues, and successive closures take 303, 250 and 277 further digits.

**The coupling polynomial as a clock.** The notes read the progress of each closure through the GFD coupling polynomial $f(K,s) = 1 + sK + K^2$. As the count of distinct hexagrams rises from 0 to 64, the state coordinate $s$ runs from $-1$ to $+1$. The capacity therefore climbs from 13 (TetB) through 17 (the Field Origin, reached at 32 hexagrams) to 21 (TetA), then resets. Over successive closures the result is a sawtooth between 13 and 21, which the notes describe as the field's breath, from vortex core to horizon and back ([`coupling_channel_analysis.html`](coupling_channel_analysis.html)).

## 3. The bridge to the BBP formula

The deepest claim in the folder concerns where the digits of $\pi$ come from. In 1995 Bailey, Borwein and Plouffe discovered the series

$$\pi \;=\; \sum_{k=0}^{\infty} \frac{1}{16^k}\left[\frac{4}{8k+1} - \frac{2}{8k+4} - \frac{1}{8k+5} - \frac{1}{8k+6}\right],$$

which allows any hexadecimal digit of $\pi$ to be computed without the digits before it.

The derivation in [`why_pi_formal_derivation.md`](why_pi_formal_derivation.md) gives every element of this series a meaning in the stellated octahedron:

| Element of the BBP series | Value | Reading in the geometry |
|---|---|---|
| Base | $16 = K^2$ | the sixteen sub-channels into which each face divides |
| Terms per orbit | $4 = K$ | one reading per face of the tetrahedron |
| Denominator step | $8 = 2K$ | one sector per vertex of the cube |
| Denominator offsets | 1, 4, 5, 6 | the running sum of the $z$-axis face-normal pattern $[3,1,1,3]$, starting from 1 |
| Numerator magnitudes | 4, 2, 1, 1 | a weighting of the $x$- and $y$-axis patterns $[3,3,1,1]$ and $[3,1,3,1]$ |
| Numerator signs | $+, -, -, -$ | one temporal and three spatial faces, the $3+1$ structure |
| Numerator sum | 0 | closure: the face normals sum to zero |

The three axis patterns are the columns of the face-normal table with $+$ read as $D = 3$ and $-$ as 1. Each is a permutation of $[D, D, 1, 1]$ and sums to $2K = 8$.

On this reading, $\pi$ is not imported into the framework from the geometry of circles. It is the value of a series whose every coefficient is a count on the stellated octahedron, so that the field's own face structure, read orbit by orbit, generates the digits that drive the walk. The identification with the BBP series is exact term by term, and [`why_pi_verification.py`](why_pi_verification.py) checks it over 40 terms. Of the entries in the table, the base, the term count, the denominator step and the closure of the numerators follow directly from $K$ and $D$. The numerator weights rest on a stated rule for combining the $x$- and $y$-axis patterns, which the derivation sets out explicitly.

## 4. What the numbers show

Two observations help place the results.

**The geometric correspondences are exact.** The trigram–vertex bijection, the family as the parity partition, the Fu Xi opposites as body diagonals and the 64 hexagrams as $K^D$ are identities. They depend on no data and no fitting.

**The closure step reflects the statistics of $\pi$.** A walk driven by independent, uniformly random base-8 digits covers all 64 transitions after 301 steps on average, with a standard deviation of about 78. Roughly 29% of such walks need 332 steps or more (5000 simulated walks). $\pi$'s closure at step 332, and the later closures at 303, 250 and 277 digits, are what a well-mixed digit sequence does. This agrees with the expectation, widely supported though unproven, that $\pi$ is normal in base 8. The count of 333 digits is therefore a property of $\pi$'s statistics. The structural content of the walk lies in the space it explores, which is the $8 \times 8$ transition space of the stellated octahedron, and in the BBP bridge that ties the source of the digits to the same geometry.

## 5. Contents

| File | Contents |
|---|---|
| [`circular_closure_walk_synthesis.md`](circular_closure_walk_synthesis.md) | **Start here.** The full argument in one document: the trigram geometry, the three axis vectors, the reading mechanism, the hexagram walk and the dual-source verification |
| [`why_pi_formal_derivation.md`](why_pi_formal_derivation.md) | The derivation of the BBP series from six constraints on the closure walk |
| [`closure_vortex_synthesis-1.md`](closure_vortex_synthesis-1.md), [`closure_vortex_synthesis-2.md`](closure_vortex_synthesis-2.md) | Two versions of the vortex synthesis: the coupling polynomial as the radial profile of closure, the sawtooth, the last-hexagram gaps and the fine-structure correspondence |
| [`closure_walk_proof_iching.py`](closure_walk_proof_iching.py) | Dual-source verification: $\pi$ in base 8 from mpmath and from the three-axis mechanism, matched digit for digit, with the walk closing at step 332 |
| [`why_pi_verification.py`](why_pi_verification.py) | Tests of each of the six constraints and the term-by-term identity with the BBP series |
| [`run_all_validations_with_i-ching-intact.py`](run_all_validations_with_i-ching-intact.py) | The validation suite of Paper IX with its I Ching section intact: 46 checks across 16 sections, from dimensional uniqueness to the complete derivation chain |
| [`traversal_analyzer.py`](traversal_analyzer.py), [`tetragram_analyzer.py`](tetragram_analyzer.py) | Analysis engines: a step-by-step ledger of the walk (faces, orbits, macro-cycles, chamber crossings) and its resolution into the 32 corner and central sub-channels of the eight faces |
| [`coupling_channel_analysis.html`](coupling_channel_analysis.html) | Interactive chart of the coupling-polynomial sawtooth over four closure cycles |
| [`element_closure_is_iching.html`](element_closure_is_iching.html) | Interactive map of the closure walk applied to the 83 stable elements and their binding curve |
| [`Nelson_2026_GFD_Complete_Field_Closure_from_Stellated_Octahedron_Topology.pdf`](Nelson_2026_GFD_Complete_Field_Closure_from_Stellated_Octahedron_Topology.pdf) | The full manuscript of Paper IX, including the I Ching section ("Historical Correspondence") omitted from the version deposited on Zenodo; the published version is in [`papers/09-complete-field-closure/`](../../../papers/09-complete-field-closure/) |
| [`ichingyching/`](ichingyching/) | An earlier copy of the synthesis and proof script |

**Reproduce:**

```bash
pip install mpmath
cd research/exploratory/i-ching
python closure_walk_proof_iching.py                  # dual-source proof; closure at step 332
python why_pi_verification.py                        # the six constraints and the BBP identity
python run_all_validations_with_i-ching-intact.py    # 46 checks
```

## A note on scope

This is exploratory work. Its first part is mathematics: the trigrams of the *I Ching* are the vertices of the cube, and their classical family and their Fu Xi opposites are the two tetrahedra of the stellated octahedron and its four body diagonals. Its second part is an interpretation: a reading of the hexagram walk and of the BBP series as the field reading its own faces.

No claim is made that the authors of the *I Ching* knew this geometry. The claim is that a system built three thousand years ago to describe change is, in its structure, the complete state space of the object that GFD places at the heart of the gravitational field. Leibniz found binary arithmetic in the hexagrams. The stellated octahedron is the geometry that arithmetic draws.

---

**Sources**

- Leibniz receives Bouvet's letter and publishes the *Explication de l'arithmétique binaire*: [History of Information](https://www.historyofinformation.com/detail.php?entryid=454); the Leibniz–Bouvet correspondence, annotated: [Swarthmore College](https://archive.swarthmore.edu/leibniz-bouvet/index.html)
- *Shuo Gua*, the family of the trigrams and the Earlier Heaven opposites: R. Wilhelm, *The I Ching or Book of Changes*, trans. C. F. Baynes (Princeton University Press, 1950), *Shuo Kua* chs. 3 and 10
- D. H. Bailey, P. B. Borwein and S. Plouffe (1997). On the rapid computation of various polylogarithmic constants. *Math. Comp.* 66, 903–913. [AMS](https://www.ams.org/mcom/1997-66-218/S0025-5718-97-00856-9/)
- GFD geometry: [`docs/01-foundations/04-dual-tetrahedron-field-origin.md`](../../../docs/01-foundations/04-dual-tetrahedron-field-origin.md), [`10-stellated-octahedron.md`](../../../docs/01-foundations/10-stellated-octahedron.md); Paper IX, [`papers/09-complete-field-closure/`](../../../papers/09-complete-field-closure/)
