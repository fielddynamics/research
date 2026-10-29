# Bound and Unbound: How a Gravity Field Becomes Matter

### One field, two states — a synthesis of the GFD gravity-field packing suite

*Field Dynamics Research · Gravity Field Dynamics (GFD), $K = 4$, $D = 3$*
*Test suite: [`gfd_gravity_field_packing_20.py`](gfd_gravity_field_packing_20.py), 20 of 20 passing · Related papers: VII, XI and XIII*

---

## The idea in one paragraph

In Gravity Field Dynamics there is only one field, the gravity field, and every gravity field has the same two-chambered geometry: the stellated octahedron, with its chambers TetA and TetB coupled at a central Field Origin. What distinguishes empty space from a grain of sand is not a different substance but a different **state** of the same field.

- **Unbound.** A field whose TetB chamber is empty is unbound. Unbound fields make up the long-range gravitational background, the mesh on which everything else sits.
- **Bound.** A field that has been pushed through its Field Origin, so that its TetB chamber is occupied, is bound. Bound fields are what we call matter.

This note explains how a field passes from one state to the other, why a bound field stays bound, what does the pushing, and what the nuclear data say about it.

## 1. The unbound field: a one-way coupling

An unbound gravity field couples to the matter around it in one direction only. It responds to a source but is not held by anything.

Let $x = g/a_0$ be the strength of the field in units of the acceleration scale $a_0$, and let $\mu$ be the fraction of the field's coupling capacity in use. In a one-way coupling, the response draws on whatever capacity remains, so the balance condition is

$$x\,(1 - \mu) = \mu \qquad\Longrightarrow\qquad \mu(x) = \frac{x}{x+1}.$$

This is the GFD constitutive law. It governs galaxies: at high field strength $\mu \to 1$ and Newtonian gravity is recovered, while at low field strength $\mu \to x$ and rotation curves flatten. In Paper VII's language, a field in this state corresponds to the massless spin-2 mode of bimetric gravity. Its TetB chamber is empty, and it carries no localised energy. It is the stage, not an actor.

## 2. The gate

Every gravity field has one special state: the Field Origin, where $x = 1$ and the coupling polynomial $f(K,s) = 1 + sK + K^2$ takes its central value $f = 17$. The capacity function $f(x) = (21x + 13)/(x+1)$ reaches 17 at exactly one point, $x = 1$. There is one gate, and only one.

A field that is pushed through the gate does not simply pass to the other side. Its TetB chamber becomes occupied, and it changes state. In Paper VII's language, it now corresponds to the massive spin-2 mode, whose nonlinear self-coupling confines it into a localised configuration. That is the same idea Wheeler had in 1955 when he showed that general relativity permits *geons*, configurations of pure field energy held together by their own gravity. GFD calls a bound field of this kind a **Field Atom**.

## 3. Why a bound field stays bound: the echo

The unbound law describes a one-way conversation: the field answers its source. A bound field is in a different situation. It is its own source. Paper XIII states the condition precisely:

1. In a bound pair, a fraction $\mu$ of the coupling capacity is used in one direction.
2. The remaining $(1 - \mu)$ carries the return coupling.
3. Self-consistency requires that the return coupling, acting as the effective source, reproduces exactly the $\mu$ it started from.

The field's own echo must regenerate the field. Substituting the return coupling for the source gives

$$x\,(1 - \mu)^2 = \mu .$$

The exponent is 2 because the coupling runs in two directions: out and back, compressed from both sides. **It is not an adjustable parameter.** It counts directions. A field in the one-way state obeys the law with exponent 1; a field that has crossed the gate and closed on itself obeys the law with exponent 2. There is no intermediate case, because a coupling cannot be one-and-a-half-directional.

**The golden ratio marks the crossing.** At the gate ($x = 1$), the bound law becomes $(1-\mu)^2 = \mu$. Writing $\nu = 1 - \mu$, this is $\nu^2 + \nu = 1$, so $\nu = 1/\varphi$ and $\mu = 1/\varphi^2 \approx 0.382$, where $\varphi$ is the golden ratio. The unbound law gives $\mu = \tfrac12$ at the same point. The two states differ by 31% at the gate itself, which makes the distinction observable in principle.

## 4. What does the pushing: stellar compression

Something has to drive fields through the gate. In GFD the first crossing is hydrogen: a single field, $A = 1$, sitting at the gate with no surplus binding. Everything heavier is built by compression.

This is where GFD meets one of the best-established results in astrophysics. The chemical elements heavier than hydrogen and helium were forged inside stars, by fusion in their cores and by the explosive and neutron-capture processes of stellar deaths (Burbidge, Burbidge, Fowler and Hoyle 1957). GFD reads that history geometrically. Stellar compression packs gravity fields into the TetB cavity of a host field. Paper XI identifies the compression ratio with the square of the number of packed fields,

$$x = A^2,$$

where $A$ is the mass number.

**The bicycle pump.** Compression gets harder with every stroke. Under the bound law, the unfilled capacity falls off as

$$1 - \mu \;\approx\; \frac{1}{\sqrt x} \;=\; \frac1A,$$

so each additional field adds less than the last. The unbound law would saturate far faster, as $1/A^2$, leaving almost no structure beyond the lightest nuclei. The bound law keeps real curvature across the whole periodic table:

| Nucleus | $A$ | Compression $x = A^2$ | Capacity in use $\mu$ | Unfilled $1 - \mu$ |
|---|---|---|---|---|
| Hydrogen | 1 | 1 | 0.382 (the gate) | 0.618 |
| Helium-4 | 4 | 16 | 0.779 | 0.221 |
| Carbon-12 | 12 | 144 | 0.920 | 0.080 |
| Iron-56 | 56 | 3,136 | 0.982 | 0.018 |
| Lead-208 | 208 | 43,264 | 0.995 | 0.005 |

**The binding curve.** For all but the lightest nuclei, the bound law gives a simple form for the binding energy per nucleon:

$$\frac{BE}{A} \;\approx\; C\,K\left(\frac{A-1}{A}\right)^2 .$$

Here $(A-1)/A$ is the fraction of fields beyond the first crossing (hydrogen contributes nothing), and the square comes from the two-directional compression. Paper XI fixes the energy constant from the electron mass and the topology, $C = 17\,m_e c^2/K = 2.172$ MeV.

Expanding the formula, $BE/A \approx CK\,(1 - 2/A + 1/A^2)$. The coefficients are locked together in the ratio $1 : -2 : +1$. They are a consequence of the law, not fitted.

Against measured binding energies (AME2020):

| Nucleus | Predicted $BE/A$ (MeV) | Measured (MeV) | Difference |
|---|---|---|---|
| Helium-4 | 4.89 | 7.07 | −31% |
| Carbon-12 | 7.30 | 7.68 | −5% |
| Oxygen-16 | 7.64 | 7.98 | −4% |
| Iron-56 | 8.38 | 8.79 | −5% |
| Lead-208 | 8.60 | 7.87 | +9% |

The formula captures the rise and saturation of the binding curve across the middle of the periodic table with no free parameter. Its two departures are both informative:
- **Helium-4** binds far more tightly than the formula predicts. It is the first complete tetrahedral unit ($A = K = 4$), and the suite finds its binding constant 47% above the mean: a closure resonance.
- **The heaviest nuclei** are over-predicted. That is the signature of electric repulsion growing with $Z^2$, which a single constant cannot capture (§5).

The full treatment, with sector crossings and shell structure, is in Paper XIII.

## 5. The vortex: why bound matter is charged

In the GFD picture, the two-directional compression of a bound field produces a vortex that spirals outward into ordinary spacetime, and that vortex is the electric field. The bound envelope together with its vortex is matter.

The suite tests the consequences of this reading against the data:

| Test | Finding |
|---|---|
| Coulomb inseparability | Subtracting the standard Coulomb term from the binding energies makes the fit *worse* (the spread of the binding constant rises by 37%). On the GFD reading, the electric repulsion is part of the same compression that binds, not a separate correction. |
| Repulsion tracks $Z^2/A$ | The residuals of the bound law correlate with $Z^2/A$ ($r \approx -0.72$): more charge, less effective binding. |
| Neutron ballast | The neutron-to-proton ratio of stable nuclei rises steadily with $Z$ ($r > 0.9$). More vortices repel more strongly and need more neutral fields to hold the envelope together. |
| Helium-4 closure | Helium-4's binding constant stands 47% above the mean: the first complete tetrahedral unit. |

The rise of the neutron-to-proton ratio is standard nuclear physics, where it is attributed to Coulomb repulsion. GFD gives it a geometric reading.

The same picture accounts for electrons. The vortex of a bound field illuminates surrounding unbound fields: $Z$ vortices light $Z$ fields, and charge neutrality follows from the geometry.

## 6. How bound fields pack

The structure of the packing carries further signatures:

- **The magic numbers.** All seven nuclear magic numbers, 2, 8, 20, 28, 50, 82 and 126, follow from $K = 4$ alone, and no other value of $K$ from 2 to 10 reproduces them (Papers XI and XIII).
- **The 20 → 28 gap.** In standard nuclear physics this gap requires a spin–orbit force (Mayer 1949; Haxel, Jensen and Suess 1949). In GFD it arises from a change in the packing geometry at the fourth shell.
- **The end of stability.** The packing has a finite address space, $K^K = 256$ positions. Paper XIII locates the end of stability more precisely: three ordinary sectors of $K^D = 64$ positions each, plus the gate sector, place the boundary at $3 \times 64 + 16 = 208$, which is lead-208, the heaviest stable nucleus. Bismuth-209, long counted as stable, does decay, with a half-life of about $2 \times 10^{19}$ years (de Marcillac et al. 2003).

## 7. From nucleus to object

A bound field is a Field Atom. Many of them together form a **Field Object**, which Paper VII describes through the example of an asteroid: some $10^{33}$ bound envelopes, each closing at its own Field Origin, together forming a single gravitational entity defined by the relations among its parts. Paper VII compares it to a chord in music. Change one note and the chord changes; remove part of it and it becomes a different chord.

> "The unbound envelopes, TetB chambers empty, form the mesh: the stage. The bound envelopes, TetB chambers occupied through stellar compression, move through that mesh: the actors. Atoms, asteroids, stars, and galaxies are not objects that 'have' gravitational fields. They *are* bound gravity field configurations." — Paper VII

## 8. An honest scorecard

| Question | Answer |
|---|---|
| Does the bound law fit better than the unbound law where the binding curve has shape? | Yes. For light nuclei ($A = 7$–19) the root-mean-square error is 0.38 MeV for the bound law against 1.25 MeV for the unbound law. |
| Does it beat a simple empirical fit? | Not quite. A two-parameter fit $c_0 + c_1/A$ reaches 0.379 MeV against the bound law's 0.388 MeV, with one parameter. The bound law achieves 97% of the accuracy with half the parameters and a physical mechanism. |
| Where does it fail? | Every nucleus from hafnium to bismuth is over-predicted, because electric repulsion grows with $Z^2$ and a single constant cannot follow it. |
| How many free parameters? | The suite fits one constant, $C \approx 2.156$ MeV, in six of its twenty tests. Paper XI fixes it from the electron mass, $C = 17\,m_e c^2/4 = 2.172$ MeV, within 0.7% of the fitted value, which leaves no free parameter. |
| What would falsify it? | Two predictions differ between the states: $\mu = 1/\varphi^2$ against $\tfrac12$ at the gate, and $1/A$ against $1/A^2$ saturation. If nuclear binding were shown to saturate as $1/A^2$, the packing picture would fail. |

## 9. The twenty tests

| Section | Tests | What they establish |
|---|---|---|
| **A. The gate** | A1–A4 | $x = 1$ is the unique crossing; nuclei sit far beyond it; hydrogen is the first crossing with zero surplus binding; the bound law gives $\mu = 1/\varphi^2$ at the gate |
| **B. Held** | B5–B9 | saturation as $1/A$, not $1/A^2$; the asymptotic form $K((A-1)/A)^2$ to better than 1% for $A \ge 7$; seven times the dynamic range of the unbound law from lithium to calcium; three times the accuracy for light nuclei; diminishing returns that grow with $A$ |
| **C. The vortex** | C10–C13 | Coulomb inseparability; repulsion tracking $Z^2/A$; neutron ballast; the helium-4 closure |
| **D. The packing** | D14–D17 | the seven magic numbers from $K = 4$; the $K^K = 256$ ceiling; the locked coefficients $1 : -2 : +1$; the shell inversion without spin–orbit coupling |
| **E. Adversarial** | E18–E20 | competition with a two-parameter fit; the documented failure for heavy nuclei; the falsifiable predictions |

```bash
cd research/bound-gravity-and-packing
python gfd_gravity_field_packing_20.py      # 20/20
```

## A note on the exponent

An earlier version of this suite scanned the exponent in $x(1-\mu)^n = \mu$ continuously, from $n = 1$ to $n = 3$, looking for the best fit. That framing treated the exponent as a dial, and it has been withdrawn. The exponent is the number of directions in which the coupling runs. It is 1 for a field answering a source, and 2 for a field that has crossed the gate and must regenerate itself. Nothing in between is physical.

---

## References

- Burbidge, E. M., Burbidge, G. R., Fowler, W. A. and Hoyle, F. (1957). Synthesis of the elements in stars. *Rev. Mod. Phys.* 29, 547.
- de Marcillac, P., Coron, N., Dambier, G., Leblanc, J. and Moalic, J.-P. (2003). Experimental detection of α-particles from the radioactive decay of natural bismuth. *Nature* 422, 876.
- Hassan, S. F. and Rosen, R. A. (2012). Bimetric gravity from ghost-free massive gravity. *JHEP* 02, 126.
- Haxel, O., Jensen, J. H. D. and Suess, H. E. (1949). On the "magic numbers" in nuclear structure. *Phys. Rev.* 75, 1766.
- Mayer, M. G. (1949). On closed shells in nuclei. II. *Phys. Rev.* 75, 1969.
- Wang, M., Huang, W. J., Kondev, F. G., Audi, G. and Naimi, S. (2021). The AME 2020 atomic mass evaluation (II). *Chinese Phys. C* 45, 030003.
- Wheeler, J. A. (1955). Geons. *Phys. Rev.* 97, 511.

**GFD papers:**
- Paper VII, [`07-dual-tetrad-topology-field-origin/`](../../papers/07-dual-tetrad-topology-field-origin/): unbound and bound envelopes, Field Atoms and Field Objects.
- Paper XI, [`11-nuclear-shells-tetrahedral-packing/`](../../papers/11-nuclear-shells-tetrahedral-packing/): stellar compression into the TetB cavity, $x = A^2$, the energy constant.
- Paper XIII, [`13-nuclear-binding-bidirectional-sst/`](../../papers/13-nuclear-binding-bidirectional-sst/): the self-consistent (bidirectional) law, the binding curve, the end of stability at lead-208.
