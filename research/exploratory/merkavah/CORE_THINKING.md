# A Merkavah of Merkavot — Core Thinking

**Status:** core thinking, October 2026. Builds on [`PLAN.md`](PLAN.md) §2 and §4, and on the photonic-substrate notes in [`research/photonic/`](../../photonic/).
**Code:** [`python/transition_radius.py`](python/transition_radius.py); tests in [`python/tests/test_transition_radius.py`](python/tests/test_transition_radius.py) (5 passing)

---

## The thesis

In the photonic-substrate reading of GFD, **light is the fundamental merkavah**:

- **The photon** is a stellated octahedron, two tetrahedral chambers coupled at a Field Origin.
- **Gravity is how light packs.** $K^D = 64$ photonic stellated octahedra, coupled on their faces, form one gravity field. That field is again a stellated octahedron, because the form is a fixed point of the 64-fold tiling.
- **Matter is light that has crossed the Field Origin** and is held, as a bound vortex, on the TetB side.

We live in a lattice of light.

A human being is therefore a bound configuration of trapped light within that lattice. Like every mass, a human has a gravity field, and that gravity field is a merkavah: **a two-chambered vehicle that carries the body, composed of photonic merkavot**, nested within the Earth's merkavah, the Sun's and the galaxy's. Its form follows from the framework; its size does not yet (§3.2).

The texts arrive at the same picture from their side:
- light precedes the luminaries and matter (Genesis 1; *Ḥagigah* 12a);
- the chariot is described entirely in light (Ezekiel 1);
- the first human was clothed in garments of light (*Bereshit Rabbah* 20:12);
- the patriarchs *are* the chariot (*Bereshit Rabbah* 47).

## 1. Light as the substrate

The photonic notes develop the reading this programme rests on. Their status should be stated plainly: they are working notes with their own test suites, and not part of the published letters.

**The photon is the stellated octahedron.** Letter 1 derives the stellated octahedron from one input, the Lorentz signature, by way of the null cone, the set of directions along which light travels. The four isotropic directions it finds are four null directions, and their two bounded regions are TetA and TetB. [`g_matrix_synthesis.md`](../../photonic/g_matrix_synthesis.md) draws the conclusion: "The stellated octahedron that the letter derives is therefore the geometry of four photon directions. It IS a photon."

**Gravity is the packing of light.** In [`gfd_light_substrate_synthesis.md`](../../photonic/gfd_light_substrate_synthesis.md) and [`the-pixel-and-the-lattice.md`](../../photonic/the-pixel-and-the-lattice.md):

- Each photon closes with $K = 4$ faces. When photons pack on their faces, with three spatial faces coupling to neighbours and one time face coupling forward, the packing *is* the gravitational field. "Light is first. Gravity is emergent. The topology belongs to light. Gravity inherits it."
- **The road and the car.** The packed lattice is the road. Its coupled time faces align into strata, which are the rays along which light travels. Each photon is a car, its own stellated octahedron riding a stratum with a coupling of $1/K$ per hop.
- **Matter is trapped light.** A massive particle is a photon topology that has crossed the gate at the Field Origin ($f = 17$) and is held on TetB by compression from both sides. Its outward spiral is the electric field. Rest energy $mc^2$ is the circulation energy of the confined light.
- **The graviton is composite.** It is two photon topologies coupled at a face, so spin $1 + 1 = 2$.

**The vacuum is a crystal of light.** [`the_photonic_substrate_enterprise_full_thinking.md`](../../photonic/the_photonic_substrate_enterprise_full_thinking.md): "Gravity does not tile space. Light tiles space. Gravity is what happens when the tiling spins."

## 2. Merkavot all the way up

The hierarchy is set out in [`g_matrix_synthesis.md`](../../photonic/g_matrix_synthesis.md) and in the Grothendieck note ([`grothendieck_xray_stellated_octahedron.md`](../../../papers/letter-1-tetrad-frame-geometry/Supplementary/research/grothendieck_xray_stellated_octahedron.md), §§11–12):

| Level | Composition | What it is |
|---|---|---|
| 0 | one stellated octahedron, $K = 4$ directions | **the photon**: the elementary merkavah |
| 1 | $K^D = 64$ photonic merkavot, coupled | **a gravity field**: its 64 couplings are the 64 components of the affine connection, $K^3 = K^D$ only because $D = 3$ |
| 2 | 64 gravity fields | **a host** |
| … | ×64 at every level | |

**Each level is again a merkavah.** The Grothendieck note computes the motivic class of the stellated octahedron, $[M] = 8 - 12L + 8L^2$, and shows it is a fixed point of the 64-fold tiling, $T([M]) = [M]$. A gravity field is "geometrically isomorphic to a photon", and so is a host. The note continues: "The hierarchy has no floor". It is unbounded in both directions, and what selects a physical level is the coupling strength there: $\alpha$ selects the electromagnetic window and $a_0$ the gravitational one.

So the composite is not merely made *of* merkavot. It *is* a merkavah, of the same form as each of its parts. That is the precise sense of "a merkavah of merkavot".

## 3. The human merkavah

### 3.1 What a human is, in this picture

A human body is about $10^{28}$ bound vortices of trapped light (nucleons and electrons), held in the lattice of light. The body's gravity field is the region of the lattice that this matter organises around itself. By §2 it has the same form as the photon, and so it is a merkavah composed of photonic merkavot.

It is a **vehicle** in the plain sense of the word. In the road-and-car language of the photonic notes, a mass does not move through an inert background. It carries its own organised field with it, and that field couples it to everything else. The body rides in its merkavah.

### 3.2 Its size: what can and cannot be said

The merkavah of a gravity field is defined by its *form*, which is the same at every scale. Its *size* is a separate question, and the framework does not yet answer it for a human.

One length can be computed. Around an **isolated** mass $M$, the field falls to the acceleration scale $a_0$ at the transition radius

$$r_t = \sqrt{GM/a_0},$$

where $\mu = \tfrac12$, $s = 0$ and $f = 17$: the Field Origin state. For a 70 kg body, $r_t = 6.24$ m. It is tempting to call this the size of a human merkavah, and an earlier draft of this note did. **That is a stretch, for three reasons:**

1. **No human is isolated.** On Earth's surface a person sits in a field of $x \approx 8 \times 10^{10}$. The total field never falls to $a_0$ within 6.24 m, so the balance surface is not realised.
2. **Nothing observable marks it.** The human's own field at 6.24 m is $1.2 \times 10^{-10}$ m/s², about $10^{-11}$ of the Earth's field at that point. There is no measurement that would locate it.
3. **The radius belongs to the field's *strength*, not its form.** $r_t$ is set by $a_0$, the gravitational coupling window. In the photonic reading, the merkavah of a gravity field is the 64-fold composite of photonic merkavot (§2). Its extent is fixed by how that composite is organised, which the framework has not yet derived.

What $r_t$ does show is the scale invariance itself: the same construction, at every mass, with a radius growing as $M^{1/2}$.

| Body | $r_t = \sqrt{GM/a_0}$ | $r_t / R_{\text{body}}$ | $x = g/a_0$ at the body's surface |
|---|---|---|---|
| electron | 0.71 fm | 0.25 | 0.064 |
| proton | 30.5 fm | 36 | $1.3 \times 10^3$ |
| human (70 kg), if isolated | 6.24 m | 24 | 596 |
| Great Pyramid, if isolated | 57 km | 780 | $6.1 \times 10^5$ |
| Earth | 12.2 AU | $2.9 \times 10^5$ | $8.2 \times 10^{10}$ |
| Sun | 7000 AU | $1.5 \times 10^6$ | $2.3 \times 10^{12}$ |
| Milky Way (baryons) | 8.4 kpc | 0.56 | 0.31 |

(The human radius uses the sphere of equal volume, 0.26 m; the Milky Way's uses a characteristic radius of 15 kpc. With $a_0$ computed from the electron, $a_0 = K^2 G m_e / r_e^2$, the electron's radius is exactly $r_e/K$, which is an identity of that route.)

The balance surface is physically realised only where a body's own field dominates its surroundings out to $a_0$. That is true of galaxies, whose outer discs are the TetB regime of flat rotation curves. The table also shows that the electron and the galaxy, the smallest and largest bound structures, are the only bodies whose balance surface lies inside them. The size of a human merkavah, as distinct from its form, is left open (D6).

### 3.3 Nested merkavot

No merkavah stands alone. The human's sits inside the Earth's, the Earth's inside the Sun's, and the Sun's inside the galaxy's: pockets within pockets, as [`the-pixel-and-the-lattice.md`](../../photonic/the-pixel-and-the-lattice.md) puts it, all made of the same light. Because the field equation is nonlinear, the regime at any point is set by the total field there. On Earth's surface a human sits at $x \approx 8 \times 10^{10}$, deep in the Earth's TetA chamber, and the human's own balance surface is not realised as it would be in isolation.

How a nested merkavah keeps its own structure inside a stronger one is therefore a real question for the framework (D2). The Great Pyramid programme points to the answer's likely shape. Inside the pyramid the field is uniform to five parts in a hundred thousand, yet the structure's *form* fixes its local Field Origin at the King's Chamber floor ([`P0.1`](../great-pyramid/pyramid_portal_research/phase0/P0.1_field_model_results.md)). A body's own merkavah is carried by its form as well as by its field (D1).

### 3.4 The body's own Field Origin

The pyramid theorem ([`01.6`](../great-pyramid/pyramid_portal_research/01_framework_foundations/01.6_local_field_origin_theorem.md)) gives the local Field Origin of any body that tapers to an apex: $z^*/h = 1 - 1/\sqrt2$, independent of size. A human body does not taper to an apex, so the theorem must be generalised first. Two natural generalisations are the level that halves the body's projected area (Petrie's criterion for the King's Chamber) and the level that halves its boundary closure. Either can be computed from anthropometric body-scan data and compared with anatomical landmarks fixed in advance.

## 4. What the texts say

**Light comes first.** Light is made on the first day (Genesis 1:3), and the luminaries that carry it only on the fourth (1:14–19). The Talmud (*Ḥagigah* 12a) records Rabbi Eleazar's teaching that by the light of the first day "one could see from one end of the world to the other", and that God hid it, reserving it for the righteous in the time to come. In the tradition, light precedes the bodies that bear it. In the photonic reading, light precedes matter and gravity.

**The chariot is light.** Ezekiel describes almost nothing of the merkavah except in terms of light:

| Verse | Description |
|---|---|
| 1:4 | a cloud with flashing fire, brightness all around, and the gleam of *ḥashmal* (amber, electrum) from within the fire |
| 1:13 | the creatures' appearance like burning coals and torches; "the fire was bright, and out of the fire went forth lightning" |
| 1:14 | the creatures "ran and returned" like flashes of lightning |
| 1:27 | gleaming amber-coloured fire, radiating above and below |
| 1:28 | "as the appearance of the bow that is in the cloud on the day of rain, so was the appearance of the brightness round about" |

Fire, brightness, lightning, *ḥashmal* and the rainbow, the full spectrum of light, are the whole of its visible substance. The merkavah is a structure of light.

**The human is clothed in light.** Genesis 3:21 says God made Adam and Eve "garments of skin" (*kotnot ʿor*, with *ayin*). *Bereshit Rabbah* 20:12 records that the Torah of Rabbi Meir read "garments of **light**" (*kotnot or*, with *aleph*). The two words differ by one silent letter. Elsewhere the human soul is "the lamp of the Lord" (Proverbs 20:27), and Moses' face radiated light when he came down from Sinai (Exodus 34:29).

**The human is a chariot.** In *Bereshit Rabbah* 47, Resh Lakish reads "God went up from Abraham" (Genesis 17:22) as God being upon Abraham as a rider upon a chariot, and concludes *ha-avot hen hen ha-merkavah*: the patriarchs themselves are the chariot. The *Tanya* (chapters 23 and 34) explains that a chariot is "a vehicle submissive to the will of its pilot", and that any person, through study and the commandments, can become one.

**One structure across world, time and the body.** *Sefer Yetzirah* lays one letter structure across three domains:

| Letters | World | Year | Man |
|---|---|---|---|
| 3 mothers | fire, water, air | the three seasons | head, torso, body |
| 7 doubles | the seven planets | the seven days | the seven apertures of the head |
| 12 simple | the twelve diagonal boundaries; the zodiac | the twelve months | the twelve organs |

**Taken together**, the tradition holds that light precedes matter, that the chariot is made of light, that the first human was clothed in light, and that a human can be the chariot. The photonic reading of GFD holds that light is first, that the merkavah is light's own structure, that matter is light held in place, and that every gravity field, a human's included, is a merkavah of photonic merkavot.

The correspondence is structural and must be stated as such. In the rabbinic and Hasidic sources a person *becomes* a chariot by devotion. In GFD every bounded closure *is* one by its form. The two claims should be set side by side, not merged.

## 5. Register entries

Added to [`PLAN.md`](PLAN.md) §4.

| # | Textual feature | Source | GFD structure | Class | Match criterion |
|---|---|---|---|---|---|
| C11 | One structure laid across world, year and man | SY (Kaplan chs. 3–5) | One form at every scale | Structural | The counts must keep the same roles across domains |
| C12 | "The patriarchs are the chariot"; a person can become one | *Bereshit Rabbah* 47; *Tanya* 23, 34 | Every gravity field, a human's included, is a merkavah (§§2–3) | Framing | Record the will-based and form-based meanings side by side |
| C13 | The 12 simple letters as diagonal boundaries (world) and organs (man) | SY 5 | C1: the 12 edges as cube face diagonals | Control on C1 | Record whether the man-domain list carries any matching structure |
| C14 | A chariot is a vehicle submitted to its rider | *Tanya* 34 | The structure carries the coupling without altering it ([`01.5`](../great-pyramid/pyramid_portal_research/01_framework_foundations/01.5_universal_vertex_reframe.md)) | Interpretive | Low weight |
| C15 | Light made before the luminaries; the hidden first light | Gen 1:3, 1:14–19; *Ḥagigah* 12a | Light first; matter and gravity emergent | Structural | The order must be the same: light, then the bodies that carry it |
| C16 | The chariot described wholly in light | Ezek 1:4, 13, 14, 27, 28 | The merkavah as the photon's own structure | Structural | Count the descriptive terms of the vision; record the share that are terms of light, fire or radiance |
| C17 | Garments of light | *Bereshit Rabbah* 20:12 (R. Meir's Torah) | The human field as a composite of photonic merkavot | Interpretive | Record the textual variant and its classical readings |

## 6. Open items

- **D1 — the body's own Field Origin.** Generalise the pyramid theorem to bodies that do not taper to an apex, and compute the human case from body-scan data, with landmarks and tolerance fixed in advance.
- **D2 — nested merkavot.** Treat the external field explicitly. Find what a sub-closure keeps of its own two-chamber structure inside a stronger ambient field, and whether form (D1) carries it where field strength does not.
- **D3 — the photon, stated operationally.** Everything here rests on the photon being the elementary merkavah. PLAN Phase 3 moves first. It should set out what the photon's two chambers correspond to physically (its two helicities, its two transverse polarisations), what the 64-fold composition predicts that standard physics does not, and what observation would count against it.
- **D4 — continuity in living bodies.** In the pyramid, form locates and electrical continuity energises. Identify the continuous current paths of a living body and what they would be expected to do. This is a hypothesis to examine.
- **D6 — the size of a human merkavah.** Derive the extent of a gravity field's merkavah from the organisation of its photonic composite, rather than from $a_0$. Until then, no size is claimed.
- **D5 — depth of the hierarchy.** Count the 64-fold levels from the photon to a human. This needs a stated size or energy for the level-0 photon. Because any count can be fitted by choosing the unit, the unit must be fixed before counting.

## 7. What this note does not claim

- That the photonic-substrate reading is established. It is the framework's working hypothesis, developed in notes and test suites, and is stated here as such.
- That the texts *mean* the GFD geometry. The correspondence is between structures, and the meanings differ (§4).
- Any physiological or spiritual effect of a person's merkavah. D4 is a hypothesis about current paths, to be examined like the continuity hypothesis of the pyramid programme.

---

**Sources**

- GFD photonic notes: [`gfd_light_substrate_synthesis.md`](../../photonic/gfd_light_substrate_synthesis.md), [`the-pixel-and-the-lattice.md`](../../photonic/the-pixel-and-the-lattice.md), [`g_matrix_synthesis.md`](../../photonic/g_matrix_synthesis.md), [`the_photonic_substrate_enterprise_full_thinking.md`](../../photonic/the_photonic_substrate_enterprise_full_thinking.md); [`grothendieck_xray_stellated_octahedron.md`](../../../papers/letter-1-tetrad-frame-geometry/Supplementary/research/grothendieck_xray_stellated_octahedron.md)
- Ezekiel 1: [Complete Jewish Bible](https://www.biblestudytools.com/cjb/ezekiel/1.html)
- *Ḥagigah* 12a, the light of the first day: [TheTorah.com, "If the Sun Is Created on Day 4, What Is the Light on Day 1?"](https://thetorah.com/article/if-the-sun-is-created-on-day-4-what-is-the-light-on-day-1)
- *Bereshit Rabbah* 20:12, garments of light: [E. Kaunfer, "Clothed in Light"](https://jewelsofelul.com/?p=466)
- *Bereshit Rabbah* 47, the patriarchs as the chariot: [Yeshivat Har Etzion](https://etzion.org.il/en/node/44501)
- *Tanya*, chapters 23 and 34: [Chabad.org, ch. 34](https://www.chabad.org/library/tanya/tanya_cdo/aid/7913/jewish/Chapter-34.htm); [ch. 23](https://www.chabad.org/library/tanya/tanya_cdo/aid/7902/jewish/Chapter-23.htm)
- *Sefer Yetzirah*, world, year and man: [Jewish Encyclopedia](https://www.jewishencyclopedia.com/articles/13386-sefer-yezirah.html)
- Local Field Origin theorem and field model: [`01.6`](../great-pyramid/pyramid_portal_research/01_framework_foundations/01.6_local_field_origin_theorem.md), [`P0.1`](../great-pyramid/pyramid_portal_research/phase0/P0.1_field_model_results.md)
