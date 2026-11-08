# The I Ching and the Stellated Octahedron

*Exploratory programme, Gravity Field Dynamics (GFD) · Field Dynamics Research*

`i-ching` `trigrams` `hexagrams` `binary` `combinatorics` `history-of-mathematics` `stellated-octahedron` `bbp-formula`

---

On 1 April 1703, Gottfried Wilhelm Leibniz received a letter from Peking. Its author, the Jesuit mathematician Joachim Bouvet, enclosed a woodcut of the 64 hexagrams of the *I Ching* in the arrangement attributed to the legendary sage Fu Xi. Leibniz had been developing binary arithmetic for two decades. In the diagram he recognised his own numbers, 0 to 63, written in broken and unbroken lines. Within a week he sent his *Explication de l'arithmétique binaire* to the Paris Academy, citing the hexagrams as an ancient anticipation of the binary system.

Leibniz saw that the *I Ching* counts. This folder asks a further question: **what geometry does it count?** The answer it develops is the stellated octahedron, the object GFD places at the centre of the gravitational field, and through it the Bailey–Borwein–Plouffe (BBP) formula for π.

---

## How to read this folder

The folder holds two layers of work, written at different times.

1. **The result.** [`BOOK_OF_CHANGES_AND_PI.md`](BOOK_OF_CHANGES_AND_PI.md) is the current, tested account. It shows that the trigrams are the stellated octahedron, that π's base-16 formulas form exactly one family, and that silence on the TIME axis (father and mother) selects the BBP formula from that family. Every statement in it is checked by script. **Start here.**
2. **The original notes.** The files in [`notes/`](notes/), [`scripts/`](scripts/) and [`interactive/`](interactive/) are the exploratory work from March 2026 that led to the result. They are kept as they were written. Some of their claims were later sharpened or corrected by testing; the [status table](#status-of-the-original-claims) below says which.

```
i-ching/
├── README.md                     this guide
├── BOOK_OF_CHANGES_AND_PI.md     the result: start here
├── figures/                      the figure for the write-up, and the script that draws it
├── notes/                        the original syntheses and the six-constraint derivation
├── scripts/                      the original verification scripts and analysis engines
├── interactive/                  two interactive HTML charts
└── paper/                        the full Paper IX manuscript, with its I Ching section
```

The proofs and the full test suite live in the model repository, in [`bbp_structure/`](https://github.com/fielddynamics/dfp-gravity-field-model/tree/test/bbp-octahedron-hypothesis/gravity_field_model/engine_core/field_closure/bbp_structure) (`PROOF.md`, 17 core tests and 26 extensions).

---

## Contents

### The result

| File | Contents |
|---|---|
| [`BOOK_OF_CHANGES_AND_PI.md`](BOOK_OF_CHANGES_AND_PI.md) | The I Ching as the stellated octahedron; π's formulas as one family; the TIME axis selecting BBP; where π enters; the reading of BBP in the trigram lines; the ladder into base 8; what is not claimed; a sense of rotation; what a particle physicist would ask |
| [`figures/bbp_octahedron.png`](figures/bbp_octahedron.png) | The trigrams on the cube with the four BBP corners, and four members of π's formula family shown corner by corner |
| [`figures/plot_bbp_octahedron.py`](figures/plot_bbp_octahedron.py) | Draws the figure |

### The original notes ([`notes/`](notes/))

Read in this order:

| File | Contents |
|---|---|
| [`circular_closure_walk_synthesis.md`](notes/circular_closure_walk_synthesis.md) | The first full synthesis: the trigram geometry, the three axis vectors, the reading mechanism, the hexagram walk and the dual-source verification |
| [`why_pi_formal_derivation.md`](notes/why_pi_formal_derivation.md) | The derivation of the BBP series from six constraints on the closure walk (also kept in [`research/field-closure/`](../../field-closure/)) |
| [`closure_vortex_synthesis-1.md`](notes/closure_vortex_synthesis-1.md), [`closure_vortex_synthesis-2.md`](notes/closure_vortex_synthesis-2.md) | Two versions of the vortex synthesis: the coupling polynomial as the radial profile of closure, the sawtooth, the last-hexagram gaps and the fine-structure correspondence |

### The original scripts ([`scripts/`](scripts/))

| File | Contents |
|---|---|
| [`closure_walk_proof_iching.py`](scripts/closure_walk_proof_iching.py) | π in base 8 from mpmath and from the three-axis (BBP) mechanism, matched digit for digit; the walk closes at step 332 |
| [`why_pi_verification.py`](scripts/why_pi_verification.py) | Each of the six constraints, and the term-by-term identity with the BBP series |
| [`run_all_validations_with_i-ching-intact.py`](scripts/run_all_validations_with_i-ching-intact.py) | The validation suite of Paper IX with its I Ching section (Section 13) intact: 46 checks in 16 sections |
| [`traversal_analyzer.py`](scripts/traversal_analyzer.py), [`tetragram_analyzer.py`](scripts/tetragram_analyzer.py) | Analysis engines: a step-by-step ledger of the walk (faces, orbits, macro-cycles, chamber crossings) and its resolution into 32 sub-channels. Copies of the modules in the model repository's `engine_core/common/`, where they run; they import its `gravity_field_model` package |

### Interactive charts ([`interactive/`](interactive/))

| File | Contents |
|---|---|
| [`coupling_channel_analysis.html`](interactive/coupling_channel_analysis.html) | The coupling-polynomial sawtooth over four closure cycles |
| [`element_closure_is_iching.html`](interactive/element_closure_is_iching.html) | The closure walk applied to the 83 stable elements and their binding curve |

### The source paper ([`paper/`](paper/))

The material here began as a section of Paper IX, *Complete Field Closure from Stellated Octahedron Topology*. The full manuscript, including that section ("Historical Correspondence"), is [`paper/Nelson_2026_GFD_Complete_Field_Closure_from_Stellated_Octahedron_Topology.pdf`](paper/Nelson_2026_GFD_Complete_Field_Closure_from_Stellated_Octahedron_Topology.pdf). The version deposited on Zenodo ([`papers/09-complete-field-closure/`](../../../papers/09-complete-field-closure/)) omits the I Ching section, so that the published argument rests on the topology and the closure condition alone.

---

## The background in brief

### The trigrams are the vertices of the cube

A trigram is three lines, each broken (yin, 0) or unbroken (yang, 1). Reading the lines as three binary digits places each trigram at a vertex of a cube, one bit per spatial axis. Dividing the vertices by the parity of their yang count splits the cube into two regular tetrahedra, TetA and TetB, which together form the stellated octahedron. The classical texts already make this division. The *Shuo Gua* (*Discussion of the Trigrams*) arranges the trigrams as a family:

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

- **The family is the parity partition.** Father and sons form TetA, mother and daughters TetB.
- **The opposites are the body diagonals.** The four Fu Xi pairs are a vertex and its complement, meeting at the centre, the Field Origin.
- **The hexagrams are the complete state space.** There are $8 \times 8 = 64 = K^D$ of them, 32 within a chamber and 32 across the Field Origin.
- **The ranks fix the coordinates.** Each child's rank (eldest, middle, youngest) is the position of its distinctive line from the bottom. That holds only if the bottom line is the most significant bit, as in the table.

### The closure walk

Write π in base 8; each digit names a trigram. A walker moves to the vertex given by the running sum of the digits modulo 8, and each consecutive pair of positions is a hexagram. The walk *closes* when all 64 hexagrams have occurred: for π at step 332. The notes read each closure through the coupling polynomial $f(K,s) = 1 + sK + K^2$, which climbs from 13 (TetB) through 17 (the Field Origin) to 21 (TetA) and resets: a sawtooth the notes call the field's breath.

### The bridge to BBP

The BBP formula is
$$\pi = \sum_{k\ge0} \frac{1}{16^k}\left[\frac{4}{8k+1} - \frac{2}{8k+4} - \frac{1}{8k+5} - \frac{1}{8k+6}\right].$$
The six-constraint derivation reads its base, its period and its coefficients from the face normals of the tetrahedron. The write-up takes this further: within the octahedron's own conditions, BBP is the only formula of its kind for π (proof by Baker's theorem), and the reading rules are recovered without assuming π.

---

## Status of the original claims

Testing in the model repository sorted the notes' claims into three groups.

| Claim in the notes | Status | Where |
|---|---|---|
| Trigrams = cube vertices; families = the two tetrahedra; opposites = body diagonals; 64 hexagrams = $K^D$ | **Established** (identities, any encoding) | Write-up, "The book is a cube" |
| The bottom line is the most significant bit | **Established**, fixed by the *Shuo Gua*'s ranks and Shao Yong's numbering; the synthesis's three geometric reasons hold under every encoding | Write-up; `test_iching_encoding_selection.py` |
| BBP is the octahedron's formula for π | **Established, and strengthened**: π's formulas of this kind form one family, and only BBP leaves the TIME axis silent | Write-up; `PROOF.md`, Theorems 2–3 |
| The geometry leaves "no freedom" for the coefficients | **Corrected.** The order of the children is free; only the *I Ching*'s rank order gives π | `test_reading_symmetry.py` |
| The numerators come from an "agreement rule" | **Corrected.** No agreement rule gives π; the rule is ordered (first child doubles, last child sets the step) | `test_reading_weight_rule.py`; `PROOF.md`, Theorem 6 |
| Closure at step 332 reflects the structure | **Corrected.** Random digits close at about 304 on average; π's 332 is typical, and its pre-closure walk shows no signal after a trials factor | `test_hexagram_closure_null.py`; extension test 24 |
| The "dual-source" proof: two independent sources of π's digits | **Clarified.** The three-axis mechanism is the BBP series term by term, so both sources compute π; they agree, as they must | `scripts/why_pi_verification.py` |
| Coupling-polynomial sawtooth, vortex breath, fine-structure correspondence | **Interpretation**, not tested here | `notes/closure_vortex_synthesis-*.md` |

---

## Reproduce

The original scripts need only `mpmath`:

```bash
pip install mpmath
cd research/exploratory/i-ching/scripts
python closure_walk_proof_iching.py                  # dual-source check; closure at step 332
python why_pi_verification.py                        # the six constraints and the BBP identity
python run_all_validations_with_i-ching-intact.py    # 46 checks
```

The proofs and tests behind the write-up are in the model repository:

```bash
python -m gravity_field_model.engine_core.field_closure.bbp_structure.test_bbp_completeness_proof
```

---

## A note on scope

The first part of this work is mathematics: the trigrams of the *I Ching* are the vertices of the cube, their family and their opposites are the stellated octahedron's two tetrahedra and four body diagonals, and the octahedron's TIME axis selects the BBP formula for π. The second part, the walk as the field reading its own faces, is interpretation.

No claim is made that the authors of the *I Ching* knew this geometry. The claim is structural: a system built three thousand years ago to describe change is, in its organisation, the complete state space of the object GFD places at the heart of the gravitational field. Leibniz found binary arithmetic in the hexagrams. The stellated octahedron is the geometry that arithmetic draws.

---

**Sources**

- Leibniz receives Bouvet's letter and publishes the *Explication de l'arithmétique binaire*: [History of Information](https://www.historyofinformation.com/detail.php?entryid=454); the Leibniz–Bouvet correspondence, annotated: [Swarthmore College](https://archive.swarthmore.edu/leibniz-bouvet/index.html)
- *Shuo Gua*, the family of the trigrams and the Earlier Heaven opposites: R. Wilhelm, *The I Ching or Book of Changes*, trans. C. F. Baynes (Princeton University Press, 1950), *Shuo Kua* chs. 3 and 10
- D. H. Bailey, P. B. Borwein and S. Plouffe (1997). On the rapid computation of various polylogarithmic constants. *Math. Comp.* 66, 903–913. [AMS](https://www.ams.org/mcom/1997-66-218/S0025-5718-97-00856-9/)
- GFD geometry: [`docs/01-foundations/04-dual-tetrahedron-field-origin.md`](../../../docs/01-foundations/04-dual-tetrahedron-field-origin.md), [`10-stellated-octahedron.md`](../../../docs/01-foundations/10-stellated-octahedron.md); Paper IX, [`papers/09-complete-field-closure/`](../../../papers/09-complete-field-closure/)
