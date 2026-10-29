# Bound and Unbound Gravity

*How a gravity field becomes matter · Gravity Field Dynamics (GFD) · Field Dynamics Research*

---

What separates empty space from a grain of sand?

In most of physics the answer is a list of ingredients: fields here, particles there, forces between them. Gravity Field Dynamics gives a shorter answer. There is one field, the gravity field, and it can be in one of two states.

- **Unbound.** Most gravity fields are unbound. They respond to whatever sources them, they hold nothing, and together they form the background against which everything else moves. This is the regime of galaxies.
- **Bound.** A few have been driven through their own centre into the second chamber of their geometry, and they cannot get back out. These are bound fields, and a bound field is what we call matter. This is the regime of atomic nuclei.

The work in this folder follows a field from one state to the other, and asks whether the nuclear data carry the signature of the crossing.

## The story in four steps

**1. The ocean.** Every gravity field has the geometry of the stellated octahedron: two interlocking tetrahedral chambers, TetA and TetB, coupled at a central Field Origin. In an unbound field the TetB chamber is empty. The field couples one way, $x(1-\mu) = \mu$, the law that decodes galaxy rotation curves.

**2. The gate.** The Field Origin, at $x = 1$ and coupling value $f = 17$, is the only place where a field can cross from one chamber to the other.

**3. The valve.** Getting into TetB takes compression, because a field has to be pushed through the gate. Once inside, the field expands, pressing back against the gate it came through. Leaving would mean compressing it back through against its own expansion, so the field stays. Held between compression and expansion, a bound field obeys the same law with two directions in play:

$$x\,(1-\mu)^2 = \mu .$$

The exponent is not a fit. It counts directions.

**4. The pump.** Something has to do the compressing. The elements heavier than hydrogen were forged in stars (Burbidge, Burbidge, Fowler and Hoyle 1957), and GFD reads stellar nucleosynthesis as stellar compression packing gravity fields into the TetB cavity, with compression ratio $x = A^2$ for mass number $A$. Every stroke of the pump is harder than the last, which is the shape of the nuclear binding curve. When the TetB side is packed so tightly that its fields can no longer expand, retention fails and nuclei decay. Stability ends at lead-208.

## What the data say

- **The binding curve.** The bound law, with its energy scale fixed by the electron mass ($C = 17\,m_e c^2/4 = 2.172$ MeV), gives the rise of the binding curve to within about 5% from carbon to iron. With the sector structure of Paper XIII, the same law follows the turnover past iron down to lead, with a mean error of 0.12 MeV across 81 stable isotopes.
- **The magic numbers.** All seven nuclear magic numbers follow from $K = 4$ alone, including the 20 → 28 gap that standard nuclear physics attributes to spin–orbit coupling.
- **Two states, measurably different.** At the gate the bound law gives $\mu = 1/\varphi^2 \approx 0.382$, against $\tfrac12$ for the unbound law. Binding saturates as $1/A$, not $1/A^2$. Either difference could falsify the picture.
- **Honest limits.** A plain two-parameter fit matches the bound law's accuracy for light nuclei slightly better (0.379 against 0.388 MeV). Helium-4 binds far more tightly than predicted. A residual of up to 0.24 MeV builds through the heaviest stable nuclei, where electric repulsion is the natural candidate.

## Contents

| File | Contents |
|---|---|
| [`gfd_gravity_field_packing_synthesis.md`](gfd_gravity_field_packing_synthesis.md) | **Start here.** The full account: the two laws, the gate, retention and decay, stellar compression, the binding curve, the vortex reading of charge, the packing signatures, and an honest scorecard |
| [`gfd_gravity_field_packing_20.py`](gfd_gravity_field_packing_20.py) | Twenty tests in five groups: the gate, retention, the vortex, the packing, and adversarial challenges |

```bash
pip install scipy
python gfd_gravity_field_packing_20.py      # 20/20
```

## Related papers

- **Paper VII**, [*Dual Tetrad Topology and the Field Origin*](../../papers/07-dual-tetrad-topology-field-origin/): unbound and bound envelopes, Field Atoms and Field Objects, stellar compression.
- **Paper XI**, [*Nuclear Shell Structure and Binding Energies from Tetrahedral Packing at K = 4*](../../papers/11-nuclear-shells-tetrahedral-packing/): compression into the TetB cavity, $x = A^2$, the energy constant from the electron mass.
- **Paper XIII**, [*Nuclear Binding Energy from the Bidirectional Scalar-Tensor Transition*](../../papers/13-nuclear-binding-bidirectional-sst/): the self-consistent law, the full binding curve through sector crossings, the magic numbers, the end of stability at lead-208.

---

*This is a working research folder. The tests run against measured nuclear data and are fully reproducible. The physical reading of the bound state (retention, decay and the vortex) is GFD's interpretation, set out so that it can be tested.*
