# The Great Pyramid as a Field Resonator

*Exploratory programme, Gravity Field Dynamics (GFD) · Field Dynamics Research*

---

> "The design of the level of the King's Chamber was the halving of the vertical area of the Pyramid."
> — W. M. Flinders Petrie, *The Pyramids and Temples of Gizeh* (1883)

Petrie surveyed the Great Pyramid with a precision no one had attempted before, and he noticed something he could describe but not explain. The floor of the King's Chamber, the only room in the monument built entirely of granite, lies at the height that divides the pyramid's vertical cross-section into two equal areas.

Gravity Field Dynamics gives that height a physical meaning. In GFD, every closed structure carries the same two-chambered field geometry at every scale. The point where its two chambers balance is the **Field Origin**, where the constitutive law gives $\mu = \tfrac12$. For any body that tapers to an apex, the theory places that point at a fixed fraction of the height, independent of size or shape:

$$\frac{z^*}{h} \;=\; 1 - \frac{1}{\sqrt2} \;=\; 0.29289\ldots$$

For the Great Pyramid, that is the floor of the King's Chamber.

This folder develops what follows from taking that coincidence seriously: a structure whose form places its granite chamber at its own Field Origin, and whose other architectural elements can be read, and tested, as the parts of a resonant antenna.

## The central result

| Quantity | Value | Source |
|---|---|---|
| Height of the pyramid | 5776.0 ± 7.0 in (280 royal cubits) | Petrie, §144 |
| Predicted Field Origin, $h(1 - 1/\sqrt2)$ | **1691.8 ± 2.1 in** | Theorem, [`01.6`](pyramid_portal_research/01_framework_foundations/01.6_local_field_origin_theorem.md) |
| King's Chamber floor (measured) | **1691.4–1693.7 ± 0.6 in** | Petrie, §148 |
| Half-flux plane of the full field model | 0.82 in below the floor | Phase 0, [`P0.1`](pyramid_portal_research/phase0/P0.1_field_model_results.md) |

Three steps stand behind the table.

1. **The theorem** ([`01.6`](pyramid_portal_research/01_framework_foundations/01.6_local_field_origin_theorem.md)). If closure is carried across a body's level sections in proportion to their area, the Field Origin of any apex body lies at $z^*/h = 1 - 1/\sqrt2$. Petrie's half-area criterion selects the same plane.
2. **The derivation** ([`01.7`](pyramid_portal_research/01_framework_foundations/01.7_areal_closure_from_action.md)). That areal law is not assumed. It follows from the GFD action: the closure current is the Noether current of the scalar sector, $\mathbf J = \mu\nabla\Phi/4\pi G$, and the divergence theorem makes it areal in a uniform field.
3. **The field model** ([`P0.1`](pyramid_portal_research/phase0/P0.1_field_model_results.md)). A numerical model of the closure current threading the real structure, including the Earth's field, its gradient and the pyramid's own gravity, places the half-flux plane within 0.82 in of the chamber floor. The test was set in advance: confirmation within ±3 in, falsification beyond 10 in. It passed.

No parameter was adjusted to reach the chamber. The only inputs are the pyramid's height and the geometry of a tapering body.

## An antenna in stone

If the King's Chamber sits at the Field Origin, the rest of the architecture invites a functional reading. The companion letter, [*The Great Pyramid as a Dual-Tetrad Resonant Antenna*](great_pyramid_antenna_theory.md), assigns each element a role in a resonant structure:

| Element | Proposed role | What can be computed or measured |
|---|---|---|
| Gilded capstone | input coupler to the Earth–atmosphere field | apex field enhancement; the continuous current drawn from the atmosphere |
| Limestone body | passive propagation medium | permittivity and loss; the resonances of the whole body |
| Granite King's Chamber | transducer at the Field Origin | cavity modes (lowest near 29 MHz); acoustic spectrum and Q |
| Five relieving chambers | coupled-cavity band-pass filter | the cavity frequencies of each chamber and how they step |
| Sealed Queen's Chamber shafts | resonant stubs that select frequency | standing-wave modes from the surveyed lengths |
| Open King's Chamber shafts | directional waveguides | cutoff near 0.68 GHz for their ~22 cm bore |
| Subterranean chamber | ground return in the bedrock | the conductive path from apex to bedrock |

**The choice of materials fits the reading.** Limestone is made of calcite, a crystal with a centre of symmetry, and such crystals cannot be piezoelectric. Granite is rich in quartz, which is. The architecture therefore sets its one electromechanically active material at the coupling point, inside a body that is electrically passive.

**The energy scale is small, and the requirement is continuity.** The phase 0 model finds that an earthed, capstone-tipped structure carries a steady current of about 0.22 µA from the fair-weather atmosphere, gathered over about $1.1 \times 10^5$ m². The scalar field energy stored in the whole volume is of order a microjoule. On this reading the pyramid is not a store of energy but a conduit. What it needs is a closed electrical path from capstone to ground.

**The field that locates is not the field that energises.** The same model separates two roles. The gravitational closure current puts the Field Origin at the chamber floor. The atmospheric electric field, which supplies the current, balances 18 m higher and plays no part in setting the location.

**An independent study points the same way.** Balezin and colleagues (*J. Appl. Phys.*, 2018) modelled the pyramid's response to radio waves 200–600 m long. They found that its internal chambers act as resonators that concentrate electromagnetic energy. That band contains the structure's natural quarter-wave resonance as a monopole over the ground, $\lambda \approx 4h \approx 586$ m.

## What is established, and what is open

| Established | Open: the programme's pre-registered measurements |
|---|---|
| The Field Origin theorem and its derivation from the action | **H1:** chamber-to-coffer volume ratio equal to $1/\alpha$ (Petrie's figures give 137.17) |
| The chamber floor on the predicted plane, to within measurement | **H2–H3:** the chamber's acoustic spectrum and its quality factor |
| The field model's confirmation of the location | **H4:** gold on the summit stones and apex casing (non-destructive XRF) |
| The continuous atmospheric current through an earthed capstone | **H5–H6:** coupling to the geomagnetic field; a granite electromechanical response |
| The historical record of a gilded pyramidion (Sahure's causeway reliefs) | **H7:** a gravity residual in the chamber against the mass model |
| | **H8:** the three-dimensional geometry of the shafts |
| | **H9:** cast versus cut blocks |

Each hypothesis has a stated confirmation and falsification criterion in [`PROGRAMME.md`](pyramid_portal_research/PROGRAMME.md). The natural next step for the antenna reading is to compute the frequencies in the table above, starting with the relieving chambers, the sealed shafts and the King's Chamber cavity, and to ask with a criterion fixed in advance whether they form a designed set.

## How to read this folder

| Path | Contents |
|---|---|
| [`pyramid_portal_research/`](pyramid_portal_research/) | **The research programme.** Start with its [key findings](pyramid_portal_research/README.md#key-findings) and the [programme definition](pyramid_portal_research/PROGRAMME.md). Then read the Field Origin derivation ([`01.6`](pyramid_portal_research/01_framework_foundations/01.6_local_field_origin_theorem.md), [`01.7`](pyramid_portal_research/01_framework_foundations/01.7_areal_closure_from_action.md)), the Phase 0 field model ([`P0.1`](pyramid_portal_research/phase0/P0.1_field_model_results.md)), and how the Field Origin is realised in the chamber ([`FIELD_ORIGIN_KINGS_CHAMBER.md`](pyramid_portal_research/FIELD_ORIGIN_KINGS_CHAMBER.md)). |
| [`great_pyramid_antenna_theory.md`](great_pyramid_antenna_theory.md) | The companion letter: the pyramid as a dual-tetrad resonant antenna, element by element, with the energy-functional analysis. |
| [`field_origin_geometry/`](field_origin_geometry/) | Tests of the Field Origin's geometry: centrality, the medial-triangle subdivision of each face, symmetry. Several import `gravity_field_model` from the companion model repository. |
| [`test_historical_binary_system.py`](test_historical_binary_system.py) | Tests of the binary vertex encoding, the parity partition of the cube's eight vertices into the two tetrahedra. |
| [`../../antenna theory/`](../../antenna%20theory/) | Background notes on Sierpiński antennas and resonant coupling through the Field Origin. |

**Reproduce the central results:**

```bash
cd research/exploratory/great-pyramid/pyramid_portal_research
python -m pytest python/tests                  # theorem, areal closure and field-model tests
python -m python.phase0_field_model            # the full Phase 0 field model (~1 minute)
```

## A note on scope

This is exploratory work. It carries GFD into a domain where the framework makes definite, checkable statements about an existing structure. The Field Origin result is derived and matched to the survey record. The functional reading of the other elements is a hypothesis, set out so that each part can be computed, measured and, if the numbers say so, rejected. No claim is made here about the builders' intentions beyond what the measurements can support.

---

**Sources**

- W. M. F. Petrie (1883). *The Pyramids and Temples of Gizeh*, §§144, 148. [Online text](https://www.ronaldbirdsall.com/gizeh/petrie/c21.html)
- M. Balezin, K. V. Baryshnikova, P. Kapitanova and A. B. Evlyukhin (2018). Electromagnetic properties of the Great Pyramid: first multipole resonances and energy concentration. *J. Appl. Phys.* 124, 034903. [ADS](https://ui.adsabs.harvard.edu/abs/2018JAP...124c4903B/abstract)
- Piezoelectricity and crystal symmetry: *International Tables for Crystallography*, Vol. D, §1.1.4.4. [IUCr](https://it.iucr.org/Da/ch1o1v0001/sec1o1o4o4/)
- Z. Hawass and M. Verner (1996), on the gilded pyramidion in the reliefs of Sahure's causeway; see [`05.2`](pyramid_portal_research/05_cavity_QED_operation/05.2_material_specification.md) and [`PROGRAMME.md`](pyramid_portal_research/PROGRAMME.md).
