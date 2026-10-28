# The Merkavah Programme — Research Plan

**Status:** plan, October 2026. Exploratory work, alongside the [I Ching](../i-ching/) and [Great Pyramid](../great-pyramid/) programmes.
**Theoretical basis:** Gravity Field Dynamics (GFD): [`llms.txt`](../../../llms.txt), [`docs/01-foundations/`](../../../docs/01-foundations/)

---

## 1. Purpose

GFD derives a single geometric object as the local structure of the gravitational field: the stellated octahedron, two regular tetrahedra of opposite orientation (TetA and TetB) sharing a centre (the Field Origin). The working notes go further and treat the photon as a complete instance of the same structure.

In Jewish tradition, the *merkavah*, the divine chariot of Ezekiel 1 and 10, is the central object of the oldest strand of Jewish mysticism. Its description is built on fourfold symmetry, nested wheels, motion along fixed directions and a "running and returning" exchange.

This programme asks one precise question:

> **Which structural features of the merkavah texts correspond to features of the GFD geometry, under criteria fixed in advance, and how much of that correspondence would be expected by chance?**

It is a comparative structural study of texts and a geometry. It makes no theological claim and no claim about the intentions of the texts' authors. The I Ching programme sets the precedent: a formal structure placed beside a historical text, with each correspondence stated precisely and tested on its own terms.

## 2. What GFD brings to the comparison

All of the following is fixed by $K = 4$ and $D = 3$ and stated in the documentation, before any text is consulted ([`10-stellated-octahedron.md`](../../../docs/01-foundations/10-stellated-octahedron.md), [`09-twenty-eight-geometric-elements.md`](../../../docs/01-foundations/09-twenty-eight-geometric-elements.md), [`08-face-structure-and-spin.md`](../../../docs/01-foundations/08-face-structure-and-spin.md), [`04-dual-tetrahedron-field-origin.md`](../../../docs/01-foundations/04-dual-tetrahedron-field-origin.md)):

| Element | Count | GFD reading |
|---|---|---|
| Chambers | 2 | TetA and TetB, exchanged by spatial parity |
| Faces per chamber | $K = 4$ | coupling channels; $3 + 1$ split into spatial and temporal |
| Sub-channels | $K^2 = 16$ | 4 per face, from the medial-triangle subdivision |
| Vertices | $2^D = 8$ | the cube $\{0,1\}^3$, split by parity into two groups of 4 |
| Edges | $K \cdot D = 12$ | 6 per chamber; **these are the 12 face diagonals of the cube** (verified) |
| Body diagonals | $K = 4$ | coupling axes through the Field Origin |
| Field Origin | 1 | centre; the octahedral core $\text{TetA} \cap \text{TetB}$ |
| Total elements | $28 = V + E + F = K(K + D)$ | |
| Polynomial states | $f(K,s) = 1 + sK + K^2$ | 21, 17, 13 |
| Exchange | bidirectional | TetA ↔ TetB through the Field Origin; the SST is invertible |

**The photon claim, and its status.** The statement that a photon *is* a stellated octahedron appears in working notes ([`research/photonic/the-pixel-and-the-lattice.md`](../../photonic/the-pixel-and-the-lattice.md); [`grothendieck_xray_stellated_octahedron.md`](../../../papers/letter-1-tetrad-frame-geometry/Supplementary/research/grothendieck_xray_stellated_octahedron.md)), not in the published letters. Its most formal basis is the exterior-algebra note ([`exterior_algebra_derivation.md`](../../../papers/letter-1-tetrad-frame-geometry/Supplementary/research/exterior_algebra_derivation.md)). That note shows that the graded exterior algebra of the four tetrad-derived directions, $\{1, 4, 6, 4, 1\}$, carries TetA at grade 1, its Hodge dual TetB at grade 3, and the octahedral core at grade 2, the fixed locus of the Hodge involution. An earlier draft ([`exterior_algebra_derivation-original.md`](../../../papers/letter-1-tetrad-frame-geometry/Supplementary/research/exterior_algebra_derivation-original.md)) calls the result "the algebraic skeleton on which any theory of the photon must be built"; the current version presents it more cautiously, as a companion interpretation. Phase 3 states this claim operationally before it is used in any comparison.

## 3. The sources, in three layers

The layers are kept separate throughout. Only Layers A and B are evidence. Layer C is reception history.

### Layer A — the biblical text

**Ezekiel 1** (with the parallel vision in **Ezekiel 10**):

| Feature | Verse |
|---|---|
| Four living creatures (*ḥayyot*) | 1:5 |
| Each with four faces and four wings | 1:6 |
| The faces: human, lion (right), ox (left), eagle | 1:10 (in 10:14 the ox is replaced by "the face of a cherub") |
| They went straight, without turning | 1:9, 1:12 |
| They "ran and returned" (*ratzo va-shov*) like lightning | 1:14 |
| A wheel (*ofan*) beside each creature | 1:15 |
| "A wheel within a wheel" | 1:16 |
| They moved in any of the four directions without turning | 1:17 |
| Rims full of eyes | 1:18 |
| "The spirit of the living creature was in the wheels" | 1:20–21 |
| The expanse (*raqia*) like ice, above the creatures | 1:22 |
| A throne like sapphire, with a human likeness upon it | 1:26 |
| The gleam of *ḥashmal* (amber or electrum) | 1:4, 1:27 |

### Layer B — the rabbinic and mystical tradition

- **Mishnah Ḥagigah 2:1.** The account of the chariot (*Ma'aseh Merkavah*) is not to be expounded even to one student "unless he is a sage who understands by his own knowledge". Whoever speculates on "what is above, what is below, what was before and what will be after" would have been better not born. The programme should state openly that it is working with a text the tradition guarded.
- **Hekhalot and Merkavah literature** (*Hekhalot Rabbati*, *Hekhalot Zutarti*, *Merkavah Rabbah*, *Ma'aseh Merkavah*, 3 Enoch). These are late-antique and early-medieval texts describing ascent (paradoxically, "descent", *yeridah*) through seven palaces to the chariot. Critical edition: Schäfer, *Synopse zur Hekhalot-Literatur* (1981).
- **Maimonides.** In *Mishneh Torah*, *Yesodei ha-Torah* 2:11 and 4:10, and the introduction to the *Guide*, he identifies *Ma'aseh Bereshit* (the account of creation) with natural science and *Ma'aseh Merkavah* with divine science, the science beyond physics. *Guide* 3:1–7 reads the creatures and wheels as the structure of the cosmos. This matters for framing. The most authoritative rationalist voice in the tradition already treated the chariot as a description of the structure underlying nature, not as a vehicle. That is the register in which a geometric comparison belongs.
- ***Sefer Yetzirah*** (date disputed; late antique to early medieval). It is the tradition's founding text on number and form:
  - 32 paths = 10 *sefirot* + 22 letters (1:1–2);
  - "running and returning" again (1:6, 1:8);
  - the six extremities of space sealed with the six permutations of the three letters YHV (1:13);
  - the 22 letters as 3 mothers, 7 doubles and 12 simple (1:2, 2:1, 5:3);
  - 231 gates, the pairings of 22 letters (2:4–5);
  - the 12 simple letters assigned to **"twelve diagonal boundaries"** (*gevulei alakhson*) of space (5:1–2).

  Critical edition: Hayman, *Sefer Yeṣira: Edition, Translation and Text-Critical Commentary* (2004). Standard English: Kaplan (1990).

### Layer C — reception history (context, not evidence)

- **The stella octangula.** Kepler named the compound in 1611 (*De Nive Sexangula*). It was drawn earlier by Pacioli (1509, *octaedron elevatum*) and Jamnitzer (1568).
- **The hexagram.** Seen along a body diagonal, the stella octangula projects to two opposed triangles, a hexagram, with both polar vertices landing on the centre (verified). The hexagram's history as a Jewish emblem is independent of the merkavah. It is attested on a 7th-century BCE seal from Sidon, used decoratively in antiquity and in magical amulets as *magen David* (the term first appears in the 14th-century kabbalistic *Sefer ha-Gevul*), and became an official emblem in Prague (1354). No causal link to the chariot is claimed.
- **The "Mer-Ka-Ba" star tetrahedron.** The modern identification of the *merkavah* with two interlocking tetrahedra of light comes from 1990s New Age writing (popularised by Drunvalo Melchizedek). It has no basis in Jewish texts and is criticised by Jewish writers as a distortion. The programme cites it only to separate it from Layers A and B.

## 4. Candidate correspondences

Each candidate is classified before testing:

- **Exact:** a count or relation in the text equals a GFD quantity fixed in §2.
- **Structural:** a relation in the text (duality, exchange, nesting) has a precise GFD counterpart.
- **Interpretive:** the match depends on a reading of the text, and competing readings exist.

| # | Textual feature | Source | GFD structure | Class | Match criterion |
|---|---|---|---|---|---|
| C1 | Twelve "diagonal boundaries" of space, carrying the 12 simple letters | SY 5:1–2 | The 12 edges of the stellated octahedron are exactly the 12 face diagonals of the cube | Exact + structural | The boundaries must be *diagonals* of a cube of six directions (SY 1:13). Competing readings are cube edges (P. F. Case) and octahedron edges (Townley). Only the stellated octahedron makes the twelve boundaries literal diagonals. Check *alakhson* in the Hebrew and in the classical commentators (Saadia Gaon, Donnolo, Eleazar of Worms). |
| C2 | Six extremities sealed by the 3! = 6 permutations of three letters | SY 1:13 | $D = 3$ axes, $\pm$ directions; 6 = edges per chamber = $\binom{K}{2}$; $S_3$ permutations of the axes | Structural | The permutation structure (3 letters → 6 orderings → 6 directions) must map onto the axis-permutation symmetry of the cube that carries the two tetrahedra. |
| C3 | "Running and returning" (*ratzo va-shov*) | Ezek 1:14; SY 1:6, 1:8 | Bidirectional exchange TetA ↔ TetB through the Field Origin; the invertible SST | Structural | Exchange must be two-way and symmetric, as in the text (the same verb pair, both directions). |
| C4 | Four creatures × four faces = 16 | Ezek 1:5–6, 1:10 | $K = 4$ faces; $K^2 = 16$ sub-channels | Exact (count) | Both factors must be 4 for the same reason ($K$). Caveat: four wings each also gives 16, so the count alone cannot choose between them. |
| C5 | Motion along four fixed directions, "without turning" | Ezek 1:9, 1:12, 1:17 | Four face normals; propagation along fixed directions without rotation of the frame | Interpretive | Four directions, no turning, and isotropy. Compare with the four body diagonals. |
| C6 | "A wheel within a wheel" | Ezek 1:16 | Nested duality: TetB within TetA, the octahedral core as their intersection; the Hodge involution | Interpretive | Record the classical readings (e.g. two wheels crossing at right angles) and check which, if any, has the nested-dual form. |
| C7 | "The spirit of the creature was in the wheels" | Ezek 1:20–21 | Coupling between the chambers through the Field Origin | Interpretive | Low weight; record only. |
| C8 | 3 mothers, 7 doubles, 12 simple (22 letters) | SY 1:2 | $D = 3$; $K + D = 7$; $K \cdot D = 12$; and $28 = K(K + D)$ | Exact (count) | See §5: counts of this kind carry little weight unless the GFD expression is fixed beforehand. $K\cdot D = 12$ is fixed in §2; $K + D = 7$ appears in §2 only as a factor of 28. |
| C9 | Chariot = the structure beneath nature | Maimonides, MT YT 2:11, 4:10; *Guide* intro, 3:1–7 | GFD's claim that the stellated octahedron underlies physical law | Framing | Not a correspondence. It sets the register of the study. |
| C10 | Ezekiel 10:14 changes the ox to a cherub | Ezek 10 | None expected | Control | Any correspondence built on the four face identities must survive the variant, or be dropped. |

Four further entries (C11–C14), on scale invariance and the human chariot, are set out in [`CORE_THINKING.md`](CORE_THINKING.md) §6: one structure across world, year and man in *Sefer Yetzirah*; "the patriarchs are the chariot" (*Bereshit Rabbah* 47); the twelve simple letters in the world and in man, as a control on C1; and the chariot as a vehicle submitted to its rider.

Features with no GFD counterpart are recorded rather than discarded: the eyes on the rims, the expanse, the throne and human likeness, *ḥashmal*, the 32 paths, the 231 gates and the seven palaces. A credible correspondence register shows what does not fit.

## 5. Method and controls

1. **Fix the GFD side first.** Only quantities stated in §2, which are taken from the documentation before the texts were read, may be used in a correspondence. No new expressions in $K$ and $D$ are built to match a textual number.
2. **Look-elsewhere control.** With the constants 1 and 2 and at most two operations, every integer from 1 to 30 can be written in terms of $K = 4$ and $D = 3$ (checked). A bare count match such as 3, 7 or 12 therefore carries almost no evidential weight. Count matches score only if the GFD expression is in §2 *and* the textual context matches its geometric role, as in C1, where twelve *diagonals* are matched with twelve diagonals.
3. **Primary texts in Hebrew.** Every textual claim is checked against the Hebrew and a critical edition: BHS for Ezekiel, Hayman for *Sefer Yetzirah*, Schäfer's *Synopse* for Hekhalot. Translations are cited by name.
4. **Competing readings.** For every interpretive item, the classical commentators' readings are recorded beside the GFD reading.
5. **Score and publish everything.** The register lists every candidate examined, with its class and outcome, including failures.
6. **Review.** The synthesis is offered for comment to scholars of early Jewish mysticism before it is presented as a result.

## 6. Phases

| Phase | Work | Deliverable |
|---|---|---|
| **0. Sources** | Source register; verse tables for Ezekiel 1 and 10 and *Sefer Yetzirah* 1, 2 and 5 with Hebrew key terms (*ḥayyot*, *ofanim*, *ratzo va-shov*, *alakhson*, *gevulim*); commentators for C1 and C6 | `00_sources/SOURCES.md` |
| **1. Geometry** | `merkavah_geometry.py` with tests: the §2 inventory; the 12 edges as cube face diagonals; the hexagram projection along a body diagonal; the $S_3$ axis permutations and the six directions; $4 \times 4$ channel counts | `python/` + tests |
| **2. Register** | Correspondence register C1–C10 with criteria, class, competing readings and outcome; the look-elsewhere computation | `01_correspondences/REGISTER.md` |
| **3. The photon** | State "the photon is a stellated octahedron" operationally from the exterior-algebra note: what corresponds to the two polarisations and the two chambers, what is predicted, what would count against it | `02_photon/PHOTON_STRUCTURE.md` |
| **2b. Scale** | Every closure a merkavah: the form chariot (P1 generalised to non-apex bodies, the human case) and the field chariot ($r_t = \sqrt{GM/a_0}$, from the electron to the galaxy); embedding in an external field | [`CORE_THINKING.md`](CORE_THINKING.md); `python/transition_radius.py` (started) |
| **4. Synthesis** | One document: what corresponds exactly, what corresponds structurally, what is interpretive, what does not fit | `MERKAVAH_SYNTHESIS.md`, linked from the exploratory README |

The strongest single item is **C1**, so Phases 0–2 begin there. It is a textual claim about twelve *diagonal* boundaries, it has a long and contested interpretive history, and the GFD geometry offers a reading in which the word is meant literally.

## 7. What the programme will not claim

- That the authors of Ezekiel or *Sefer Yetzirah* knew GFD, or encoded physics deliberately.
- That the modern "Mer-Ka-Ba" image is a Jewish teaching.
- Any theological conclusion, or any statement about Judaism's beliefs. The study is of texts and a geometry, and its results are correspondences, classified and scored.

## 8. Folder layout (proposed)

```
research/exploratory/merkavah/
├── README.md                    programme summary and findings (after Phase 2)
├── PLAN.md                      this document
├── CORE_THINKING.md             every closure a merkavah: form and field chariots
├── 00_sources/SOURCES.md
├── 01_correspondences/REGISTER.md
├── 02_photon/PHOTON_STRUCTURE.md
├── python/merkavah_geometry.py
├── python/transition_radius.py
├── python/tests/test_merkavah_geometry.py
└── MERKAVAH_SYNTHESIS.md
```

---

## Sources

**Texts**
- Ezekiel 1 and 10, verse by verse: [Complete Jewish Bible, Ezekiel 1](https://www.biblestudytools.com/cjb/ezekiel/1.html); [Steinsaltz, Ezekiel 1](https://steinsaltz-center.org/portal/library/Nakh/Ezekiel/chapter/1); [My Jewish Learning, "Ezekiel's Vision"](https://www.myjewishlearning.com/article/ezekiels-vision/)
- Mishnah Ḥagigah 2:1: [Center for Online Judaic Studies](https://cojs.org/Mishnah_Hagigah_2-1-_Teaching_the_Secrets_of_the_Torah/)
- *Sefer Yetzirah*: [Kaplan translation (short version)](https://www.psyche.com/psyche/yetsira/kaplan_sy_short.html); [Westcott translation](https://www.jasoncolavito.com/sepher-yetzirah.html); A. P. Hayman, *Sefer Yeṣira: Edition, Translation and Text-Critical Commentary* (Mohr Siebeck, 2004); A. Kaplan, *Sefer Yetzirah: The Book of Creation* (1990)
- Maimonides on *Ma'aseh Merkavah*: [TheTorah.com, "The Secret of the Ma'aseh Merkava According to Maimonides"](https://www.thetorah.com/article/the-secret-of-the-maaseh-merkava-according-to-maimonides)

**Scholarship on Merkavah and Hekhalot mysticism** ([bibliography](https://www.digital-brilliance.com/contributed/Karr/Biblios/mmhie.pdf))
- G. Scholem, *Major Trends in Jewish Mysticism* (1941); *Jewish Gnosticism, Merkabah Mysticism, and Talmudic Tradition* (1960)
- I. Gruenwald, *Apocalyptic and Merkavah Mysticism* (1980; 2nd ed. 2014)
- P. Schäfer, *Synopse zur Hekhalot-Literatur* (1981); *The Hidden and Manifest God* (1992); *The Origins of Jewish Mysticism* (2009)
- D. J. Halperin, *The Faces of the Chariot* (1988)
- M. D. Swartz, *Mystical Prayer in Ancient Judaism* (1991); *Scholastic Magic* (1996)
- J. R. Davila, *Descenders to the Chariot* (2001)
- R. Elior, *The Three Temples* (2004)

**Reception history**
- Stella octangula: [MathWorld](https://mathworld.wolfram.com/StellaOctangula.html)
- The hexagram as a Jewish symbol: [Jewish Virtual Library, "Magen David"](https://www.jewishvirtuallibrary.org/magen-david)
- The "Cube of Space" readings of *Sefer Yetzirah* 5: [Wikipedia, "Cube of Space"](https://en.wikipedia.org/wiki/Cube_of_Space)
- A Jewish critique of the "Mer-Ka-Ba" image: [B. Ashe, "On teaching the Merkabah", *Times of Israel*](https://blogs.timesofisrael.com/on-teaching-the-merkabah/)
