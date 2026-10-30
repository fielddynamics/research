# The Twenty-Four That Were Set Aside

### Field Closure of the Tetrad Frame, told in two pictures

**A reader's guide to Letter 3: S. Nelson, *Gravity Field Dynamics: Field Closure of the Tetrad Frame* (Field Dynamics Research, 2026, preprint).**
Paper, sources and supplementary material: [`papers/letter-3-field-closure-of-tetrad-frame/`](papers/letter-3-field-closure-of-tetrad-frame/) ([PDF](papers/letter-3-field-closure-of-tetrad-frame/letter.pdf)). Companion reading: [Einstein's Equation as the TetA Partition](EINSTEIN_TETA_PARTITION.md), on why the tetrad equation's second root cannot be removed.

---

## A decision made in 1915

Every theory of gravity has to say how a direction is carried from one point of spacetime to the next. The object that does this is called the *connection*, and in four dimensions it has 64 components.

In 1915, general relativity made a quiet bookkeeping decision about them. It required the connection to be *torsion-free*, and that single condition sets 24 of the 64 to zero. The decision has served physics extraordinarily well. Planets, light bending around the Sun, gravitational waves, the clocks in GPS satellites: all of it works with the 40 that remain.

So it is natural to ask what the other 24 were, and whether anything in the universe would look different if they were given back.

Letter 3 answers with two pictures. The first shows *which* components were set aside. The second shows *where* in a galaxy they would carry the field. This guide walks through both, slowly, and then follows them to the action the theory is built on.

---

## Picture one: sixty-four numbers, and the twenty-four set aside

![A four-by-four grid labelled t, x, y, z on both axes. The four diagonal cells (tt, xx, yy, zz) are purple and marked shared. The six cells above the diagonal are blue and marked kept. The six cells below the diagonal are red and marked discarded.](papers/letter-3-field-closure-of-tetrad-frame/fig1_matrix.png)

*Figure 1 of Letter 3. One slice of the connection: the lower index pair $(\mu, \nu)$ for a single value of the upper index $\lambda$.*

### Reading the grid

The connection is written $\Gamma^\lambda_{\mu\nu}$. It has three indices, and each runs over the four directions of spacetime, $t, x, y, z$. That makes $4 \times 4 \times 4 = 64$ numbers. Fix the first index $\lambda$, one of four "observation faces", and the remaining pair $(\mu, \nu)$ fills the sixteen cells of the grid above. The same grid appears four times, once for each face.

The sixteen cells fall naturally into three groups:

- **The diagonal (purple, 4 cells).** Entries such as $tt$ and $xx$ have no partner. Swap the two indices and nothing changes.
- **The mirror pairs (12 cells, 6 pairs).** Every off-diagonal cell has a twin across the diagonal: $tx$ with $xt$, $xy$ with $yx$, and so on.
- **What the torsion-free condition does.** It demands $\Gamma^\lambda_{\mu\nu} = \Gamma^\lambda_{\nu\mu}$. Each mirror pair keeps its symmetric combination, the sum, and loses its antisymmetric combination, the difference. The figure shows this by colouring one cell of each pair blue (kept) and its twin red (set aside). Strictly, every pair contributes one of each; the colouring makes the count visible.

Per face, that leaves 4 + 6 = **10 kept** and **6 set aside**. Across the four faces: **40 kept, 24 set aside**. The 40 are the Christoffel symbols found in every textbook of general relativity. The 24 are the torsion.

### The same count, hiding in a polynomial

Gravity Field Dynamics is built on one short polynomial,

$$f(K, s) = 1 + sK + K^2, \qquad K = 4,$$

which takes three values: 21 at $s = +1$ (the tetrahedron TetA), 17 at $s = 0$ (the Field Origin) and 13 at $s = -1$ (the tetrahedron TetB). Letter 3 points out that the grid's count was inside this polynomial all along:

$$\text{kept per face} = \frac{f(K, +1) - 1}{2} = \frac{20}{2} = 10, \qquad \text{set aside per face} = \frac{f(K, -1) - 1}{2} = \frac{12}{2} = 6 .$$

Remove the 1 (the diagonal, which belongs to both), halve for the mirror pairs, and the polynomial's two opposite states give the grid's two halves. What separates 10 from 6 is the $\pm K$ term, the only term that changes sign between the two tetrahedra.

### Whose twenty-four?

The tetrad equation, which builds the metric of spacetime from the frame, is quadratic. Like $y = x^2$, it has two roots, here related by spatial parity, and Letters 1 and 2 identify them with the two interlocking tetrahedra of the stellated octahedron: TetA ($s = +1$) and TetB ($s = -1$).

The two roots give exactly the same metric. A torsion-free connection is built from the metric alone, so it cannot tell them apart. Only the antisymmetric part, the torsion, can.

That is the message of the first picture: **the 24 components set aside in 1915 are the ones that carry the second root.** Give them back and each face returns to its full 16 cells, and the connection to its full 64. Letter 3 calls this *field closure*: both roots active, and nothing held at zero by constraint.

---

## Picture two: where the second root carries the field

![Three views of two surfaces of revolution. Blue: a broad disk with a raised centre. Red: a mirrored surface beneath it. A white ring marks where the two surfaces cross. The lower two views show the same pair from the side.](papers/letter-3-field-closure-of-tetrad-frame/fig2_tetrad_partition.png)

*Figure 2 of Letter 3. The constitutive law $\mu(x) = x/(x+1)$, drawn over radius. Blue: the TetA share $\mu$, the part general relativity keeps. Red: the TetB share $1 - \mu$, the part the torsion-free condition sets aside. You can turn it in your hands with the interactive version, [`figure2_tetrad_partition.html`](papers/letter-3-field-closure-of-tetrad-frame/Supplementary/figure2_tetrad_partition.html).*

### What you are looking at

The first picture said which components belong to which root. The second says how much of the field each root carries, and where.

Start at the centre of a bound system, a star or a galaxy, and move outward. The gravitational acceleration $g$ weakens as you go, and so does $x = g/a_0$, the acceleration measured in units of the transition scale $a_0 \approx 1.2 \times 10^{-10}$ m/s². At every step the field is shared between the two roots:

$$\text{TetA (blue)}: \; \mu(x) = \frac{x}{x+1}, \qquad \text{TetB (red)}: \; 1 - \mu(x) = \frac{1}{x+1} .$$

The two shares always add up to one. Nothing is added to the field; it is divided. Three things follow, and each can be seen in the figure:

- **The surfaces are exact mirrors.** Wherever blue rises, red falls by the same amount.
- **They cross on the white ring**, at $x = 1$, where each carries exactly half. This is the transition scale of galaxy dynamics that Milgrom identified from observations in 1983. Here it is not fitted. It is simply the midpoint of the partition.
- **Inside the ring, blue leads; outside, red does.** A theory that keeps only the 40 Christoffel components sees only the blue surface.

### How the two discs are made

Each disc is a **surface of revolution**: one curve, spun a full turn about a vertical axis, the way a potter's wheel turns a profile into a bowl. The figure is made in four steps.

1. **Choose a system and a natural ruler.** Take a single central mass $M$ and measure distance in units of its *transition radius*, $r_M = \sqrt{GM/a_0}$: the distance at which its own pull has weakened to $a_0$. For the Sun, that is about 7,000 times the Earth–Sun distance. With this ruler, the Newtonian acceleration $g = GM/r^2$ becomes simply

   $$x = \frac{g}{a_0} = \frac{1}{r^2} .$$

2. **Work out the two shares at each radius.** Putting $x = 1/r^2$ into the constitutive law gives two strikingly simple curves:

   $$\text{blue (TetA)}: \; \mu = \frac{1}{1 + r^2}, \qquad \text{red (TetB)}: \; 1 - \mu = \frac{r^2}{1 + r^2} .$$

   | Radius $r$ (units of $r_M$) | 0 | 0.5 | 1 | 2 | 5 |
   |---|---|---|---|---|---|
   | Blue height $\mu$ | 1 | 0.80 | 0.5 | 0.20 | 0.04 |
   | Red height $1-\mu$ | 0 | 0.20 | 0.5 | 0.80 | 0.96 |

   Blue starts at full height in the centre and falls away: a dome. Red starts at zero and climbs toward full height at the rim: a bowl. At every radius, dome plus bowl equals one.

3. **Spin each curve about the vertical axis.** The law depends only on how strong the acceleration is, not on which way it points, so the curve is identical in every direction from the centre. Sweep it through 360° and the dome and the bowl appear. The figure draws both out to five transition radii.

4. **Mark where they meet.** The curves cross at $r = 1$, at height ½. Spun around the axis, that single crossing point becomes a circle of radius $r_M$: the white ring.

The spiral lines on the surfaces are there only to help the eye follow their curvature in three dimensions. They are not derived from the law; only the heights carry physical meaning.

The figure shows the simplest case, one central mass. In a real galaxy the mass is spread through a bulge and a disk, so the acceleration profile $g(r)$ follows that distribution instead of $GM/r^2$. The shares are still $\mu(x)$ and $1 - \mu(x)$, now with the galaxy's own $x(r)$. The shapes stretch or sharpen; the dome, the bowl and the ring at $x = 1$ remain.

> **An aside: two roots of one quadratic.** A picture of two roots drawn as two sheets brings to mind a Riemann surface, the object complex analysis uses for a function with two values, such as $\sqrt{z}$. The resemblance runs deeper than it looks. The two heights are the two roots of a single quadratic,
>
> $$t^2 - t + \mu(1-\mu) = 0, \qquad t = \mu \;\text{ or }\; 1 - \mu ,$$
>
> whose roots sum to one and multiply to $\mu(1-\mu)$. Its discriminant is
>
> $$1 - 4\mu(1-\mu) = (1 - 2\mu)^2 = \left(\frac{x - 1}{x + 1}\right)^2 ,$$
>
> which vanishes only at $x = 1$, so the two roots meet exactly on the white ring. On a Riemann surface such a meeting point is a *branch point*, where the sheets join and swap. Here the discriminant is a perfect square, so there is no branching: the roots stay separate, $x/(x+1)$ and $1/(x+1)$, and the two sheets pass through each other on the ring. The figure is two surfaces of revolution, one for each root, meeting along the circle where the quadratic has a double root.

### A journey outward from the Sun

The partition becomes vivid when you follow it outward from home. Every row below comes from the same two formulas:

| Where you are | $x = g/a_0$ | TetA share $\mu$ | TetB share $1-\mu$ | Observed ÷ visible-matter acceleration |
|---|---|---|---|---|
| Mercury's orbit | $3 \times 10^{8}$ | 0.999 999 997 | $3 \times 10^{-9}$ | 1.000 000 003 |
| Earth's orbit | $5 \times 10^{7}$ | 0.999 999 98 | $2 \times 10^{-8}$ | 1.000 000 02 |
| Neptune's orbit | $5.5 \times 10^{4}$ | 0.999 98 | $1.8 \times 10^{-5}$ | 1.000 02 |
| The Sun's own ring, about 7,000 AU out | 1 | 0.5 | 0.5 | 2 |
| The Sun's orbit in the Milky Way | about 1.7 | 0.64 | 0.36 | 1.6 |
| A galaxy's outer disk | 0.1 | 0.09 | 0.91 | 11 |
| A faint galaxy's edge | 0.01 | 0.01 | 0.99 | 101 |

Read down the first rows and you see why general relativity has never failed a test in the solar system. At Earth, the second root carries two parts in a hundred million of the field; even at Neptune, less than two parts in a hundred thousand. Every planetary measurement sits high on the blue dome, far inside the ring.

Read down the last rows and the picture changes. A galaxy spans the whole figure: a core where blue carries nearly everything, the ring, and an outer disk where red carries most of the field. Out there the observed acceleration is 10 or 100 times what the visible matter can supply, and a theory that keeps only the blue surface has to explain the difference as unseen mass.

Two details keep the journey honest. The Sun does not sit in empty space: the Milky Way's own field at the Sun's position is already about $1.7\,a_0$, so the solar system's outskirts are never isolated, an effect Paper I treats as the external field effect. And the region beyond a few thousand AU is being tested right now, with wide binary stars tracked by the Gaia satellite. The published analyses currently disagree (Chae 2023; Banik et al. 2024), which makes it one of the most interesting places to watch.

### A galaxy, drawn by default

Nothing in Figure 2 was shaped to look like a galaxy. The profile is what the split of $\mu(x)$ between TetA and TetB produces on its own, for any bound system.

Every bound system pulls hardest at its centre and more gently further out; for any concentrated mass, this is Gauss's law. Because $\mu$ rises steadily with $x$, the partition then sorts every system in the same way: a concentrated interior where TetA carries the field, an extended exterior where TetB carries it, and a boundary between them on the ring at $x = 1$, whatever the system's mass. The round symmetry needs no assumption either: the law cares only about the strength of the acceleration, so each share is the same at every angle around the centre. Neither surface makes this structure alone. TetA by itself is a steady decline, and TetB by itself is a flat plateau. The interior, the exterior and the ring between them are the closed partition $\mu + (1 - \mu) = 1$, made visible.

This is the structure astronomers find in real galaxies. Visible matter accounts for the motions of stars and gas in the inner regions, where the acceleration exceeds $a_0$, and falls short in the outer regions, where it is below $a_0$ (McGaugh 2004). When rotation curves are split into a disk contribution and a dark-halo contribution, the two trade places smoothly, with no visible seam. Van Albada and Sancisi (1986) gave this a memorable name: the *disk–halo conspiracy*. In a dark-matter picture it is a coincidence that every galaxy's halo must somehow reproduce. In the partition it is no coincidence at all. The inner and outer shares are two halves of one closed quantity, so they cannot fail to hand over smoothly, and the handover is centred on $x = 1$ in every galaxy.

In the Milky Way, which rotates at about 230 km/s, the ring lies near 14 kpc from the centre, beyond the Sun's orbit at 8 kpc. The TetA interior holds the bulge and most of the stellar disk; the TetB exterior is the outer disk and beyond, the region conventionally assigned to the dark halo.

### Cored centres, not cusps

The same formula settles what happens at the very centre. The TetB share $1/(x+1)$ can never exceed one, so the acceleration it carries, $(1-\mu)\,g = a_0\,x/(x+1)$, can never exceed $a_0$. Cold-dark-matter halos of the standard Navarro–Frenk–White form have densities that climb without limit toward the centre, a long-standing tension with the flat cores seen in many galaxies. The partition has no such divergence, and it needs no extra physics to avoid one.

### The handover at the ring

How quickly does the field pass from one root to the other? The partition obeys a logistic law,

$$x\,\frac{d\mu}{dx} = \mu(1 - \mu),$$

the same equation that describes any smooth two-way transition. The rate $\mu(1 - \mu)$ is greatest, at exactly ¼, on the ring, where both tetrahedral chambers are equally present. The ring is where the handover happens.

### The relation every galaxy obeys

Write the partition as a relation between the acceleration supplied by visible matter and the acceleration actually observed:

$$g_{\text{bar}} = \mu\, g_{\text{obs}} = \frac{g_{\text{obs}}^2}{g_{\text{obs}} + a_0} .$$

At high acceleration this is Newton and Einstein. At low acceleration it gives flat rotation curves. It is the radial acceleration relation that McGaugh, Lelli and Schombert measured in 2016 across 175 galaxies, with a scatter of only 0.057 dex, here with no free parameter.

---

## From two pictures to one action

A partition describes how the field is shared. A complete theory also needs an *action*, the single expression from which the field equations follow. Letter 3 gets there in one step, using the identity Bekenstein and Milgrom introduced in 1984: the response function is the derivative of an energy. Integrating $\mu$ gives

$$F(y) = y - 2\sqrt{y} + 2\ln\!\left(1 + \sqrt{y}\right), \qquad y = x^2 .$$

Where do its three terms come from? Polynomial long division, the kind taught in school, answers that. With $u = \sqrt{t}$, the integrand splits as

$$\frac{u^2}{u+1} = u - 1 + \frac{1}{u+1} .$$

Each piece integrates to one term of $F$, and each matches one level of the coupling polynomial: $u$ gives the $y$ term (the $K^2$ face level); $-1$ gives the $-2\sqrt{y}$ term (the $sK$ level, the one that changes sign between the tetrahedra); and $1/(u+1)$ gives the logarithm (the $K^0$ Field Origin). That last piece, $1/(u+1)$, is exactly $1 - \mu$: the red surface. The logarithm in the action is the TetB share, integrated.

The two limits of $F$ recover the two ends of the journey. At high acceleration, $F \to y$ and the action becomes general relativity. At low acceleration, $F \to \tfrac23 y^{3/2}$, which gives the baryonic Tully–Fisher relation, $v^4 = GMa_0$. In the full covariant action, $F$ fixes the scalar sector with no free function. Light bends by the amount general relativity predicts ($\gamma = 1$, as the Cassini spacecraft requires), and gravitational waves travel at the speed of light, as GW170817 confirmed.

---

## Adding something, or restoring something

| Approach | What it changes | Torsion |
|---|---|---|
| General relativity | Nothing: 40 of the 64 connection components | Set to zero |
| Einstein–Cartan theory | Restores torsion and ties it to the spin of matter | Present only inside spinning matter; zero in empty space |
| Cold dark matter | Adds an unseen mass component to every galaxy | Set to zero |
| AeST (Skordis and Złośnik 2021) | Adds new vector and scalar fields to reproduce MOND | Set to zero |
| Gravity Field Dynamics | Restores the 24 components as the second root, carrying $1-\mu(x)$ | Present wherever $x$ is finite, including empty space |

The difference is between adding something and restoring something. Dark matter adds mass. AeST adds fields. Letter 3 adds nothing to the matter of the universe. It returns 24 components that were part of the connection all along.

---

## What is proven, and what is proposed

| Statement | Status |
|---|---|
| The connection has 64 components; the torsion-free condition keeps 40 and removes 24 | Standard differential geometry |
| The per-face count 10 + 6 equals $(f(K,\pm1) - 1)/2$ | Exact identity, verified |
| The tetrad equation has two roots that give the same metric, so a torsion-free connection cannot tell them apart | Exact algebra (Letter 2 and the Gram-matrix note) |
| The partition $\mu = x/(x+1)$ reproduces the radial acceleration relation and gives $F(y)$, general relativity at high acceleration and Tully–Fisher at low | Exact consequences of the law, verified |
| The 24 removed components are the second root, carrying the share $1 - \mu$ attributed elsewhere to dark matter | The GFD claim of Letter 3 |
| A TetA interior, a TetB exterior and a seamless handover at $x = 1$ follow from the closed partition, as seen in the disk–halo transition of real galaxies; centres stay cored | Consequence of the partition; the GFD reading is the claim of Letter 3 |

---

## Check it yourself

```bash
python papers/letter-3-field-closure-of-tetrad-frame/Supplementary/run_all_validations.py
```

The script checks every numerical claim in Letter 3, and all 52 pass: the 64 = 40 + 24 count, the polynomial identity, the partition and its logistic law, the radial acceleration relation and both limits of $F(y)$. The polynomial identity is proved step by step in [`proof_polynomial_40_24.tex`](papers/letter-3-field-closure-of-tetrad-frame/Supplementary/proof_polynomial_40_24.tex), and the full covariant action is derived in [`supplementary_covariant_completion.tex`](papers/letter-3-field-closure-of-tetrad-frame/Supplementary/supplementary_covariant_completion.tex).

---

## References

- S. Nelson, *Gravity Field Dynamics: Field Closure of the Tetrad Frame*, Field Dynamics Research (2026), preprint. Letter 3 of the tetrad series, with Letter 1, *The Coordinate-Space Geometry of the Tetrad Frame*, and Letter 2, *The Other Half of Gravity*.
- Banik, I. et al. (2024). Strong constraints on the gravitational law from Gaia DR3 wide binaries. *Mon. Not. R. Astron. Soc.* 527, 4573.
- Bekenstein, J. and Milgrom, M. (1984). Does the missing mass problem signal the breakdown of Newtonian gravity? *Astrophys. J.* 286, 7.
- Chae, K.-H. (2023). Breakdown of the Newton–Einstein standard gravity at low acceleration in internal dynamics of wide binary stars. *Astrophys. J.* 952, 128.
- Hehl, F. W., von der Heyde, P., Kerlick, G. D. and Nester, J. M. (1976). General relativity with spin and torsion: foundations and prospects. *Rev. Mod. Phys.* 48, 393.
- McGaugh, S. S. (2004). The mass discrepancy–acceleration relation: disk mass and the dark matter distribution. *Astrophys. J.* 609, 652.
- McGaugh, S. S., Lelli, F. and Schombert, J. M. (2016). Radial acceleration relation in rotationally supported galaxies. *Phys. Rev. Lett.* 117, 201101.
- Milgrom, M. (1983). A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypothesis. *Astrophys. J.* 270, 365.
- Navarro, J. F., Frenk, C. S. and White, S. D. M. (1996). The structure of cold dark matter halos. *Astrophys. J.* 462, 563.
- Skordis, C. and Złośnik, T. (2021). New relativistic theory for modified Newtonian dynamics. *Phys. Rev. Lett.* 127, 161302.
- van Albada, T. S. and Sancisi, R. (1986). Dark matter in spiral galaxies. *Phil. Trans. R. Soc. Lond. A* 320, 447.

Related: [Einstein's Equation as the TetA Partition](EINSTEIN_TETA_PARTITION.md) · [the published papers and letters](README.md#published-papers-zenodo)
