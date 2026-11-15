# Referee Review

*Internal review of "The Walsh Eigenmodes of the Pixel, and What Closure Reads" (commit a47ffac), written as a journal referee would, with each concept the proof introduces examined in turn. The proof has since been revised and renamed "The Walsh Eigenmodes of the Cube, and What Field Closure Reads", following the author's choice of "cube", the name used in the Hadamard cube frame proof. The response to each point is given under it. The numerical probes behind the findings below are independent of the verification script; each is summarised with its point.*

---

## Summary

The proof states four theorems about the eight Walsh functions on the cube's corners:
- they are the cube's eigenmodes (Theorem 1, known);
- under $T_d$ they pair, $1 \leftrightarrow xyz$ and grade 1 $\leftrightarrow$ grade 2, and are exact eigenmodes iff TetA and TetB are alike (Theorem 2);
- every $T_d$-equivariant linear direction readout of a tetrahedron is the frame readout, and scalar readouts see only $1$ and $xyz$ (Theorem 3);
- the oscillator node's $\mu$ is the TetA share, and its amplitude closure sees only total Walsh power (Theorem 4).

A corollary places the pixel's vortices in the direction modes, and a proposition shows $x + iy$ circulating on the cube.

**What holds.** The representation theory is correct, and the 34 checks pass. The corollary is clean and useful: the winding space takes one vector from each $T_2$ copy, so the uniform and parity modes never wind.

**What needs fixing.** Three of the proof's central concepts are each used in two senses, and the proof slides between them:
- **"Pixel".** It means the 8-corner cube in Theorem 2 and the 15-site pixel in the corollary.
- **"Closure".** It means Letter 1's $\sum v_i = 0$ in one place and the node's relaxation rule in another.
- **"TetA share".** It means an amplitude share in one place and a probability share in another.

The last of these changes the proposed test.

## The concepts, one by one

**1. Walsh functions as standing waves.** This is sound and correctly cited. A real eigenmode carries no current, and "standing wave" is its coupled-oscillator reading, the same reading the vortex proof uses.

**2. The sectors: "uniform and parity" and "direction modes".** The $A_1$ sector ($1$, $xyz$) is right. Calling all six of $x, y, z, yz, xz, xy$ "direction modes" is right only under $T_d$. The two grades are different kinds of object:

| | Grade 1 ($x, y, z$) | Grade 2 ($yz, xz, xy$) |
|---|---|---|
| Kind | a vector (p-like) | a quadratic form (d-like, $t_{2g}$) |
| Under inversion | odd | even |

$T_d$ has no inversion, so it cannot tell them apart, and both carry $T_2$. With full cube symmetry (TetA and TetB alike) they separate into $T_{1u}$ and $T_{2g}$. So grade 2 is a "direction" exactly when the two tetrahedra differ.

In chemical language, the cube's eight corners carry the angular characters s, p, d($t_{2g}$) and f($xyz$). Theorem 2's pairing is the corner-lattice form of a standard fact of tetrahedral chemistry: in $T_d$, s mixes with f$_{xyz}$ (both $A_1$), and p mixes with d($t_2$) (both $T_2$). This is the d–p mixing of tetrahedral complexes (Cotton, *Chemical Applications of Group Theory*). The paper should say so. That is a strength rather than a weakness, but it is not new.

*Response.* The proof now uses "T₂ modes" for the sector, "vector modes" for grade 1 and "quadrupole modes" for grade 2. The Setting gives the s, p, d and f characters. After Theorem 2 the paper says that the pairing is the cube's form of the s–f and p–d mixing of tetrahedral chemistry (Cotton), and that quadrupoles act as directions only because $T_d$ has no inversion.

**3. "The pixel holds the Walsh modes": the scope (major, W1).** Theorem 2 is proved for operators on the eight corners only. The abstract, title and README say "the pixel", and the corollary then uses the 15-site pixel. In the 15-site pixel the octahedron's own $T_2$ copy couples to both corner copies. So each eigenmode has its own grade-1/grade-2 mix, not the single angle (2) of a block:

| Probe | Result |
|---|---|
| $T_d$ parameters | the three $T_2$ levels have grade-1 shares 0.83, 0.007 and 0.98 |
| $O_h$ parameters | every eigenmode's corner part is a single grade, apart from an accidental degeneracy of grade 2 with $xyz$; neither couples to the Field Origin or the octahedron, so both sit at the bare corner energy, and a pure-grade eigenbasis still exists because they are different irreps |

*Recommendation.*
- Call the 8-corner object "the cube" throughout Theorem 2.
- Add a pixel statement. With full symmetry, a pure-grade eigenbasis exists (irreps: corners $A_{1g} \oplus A_{2u} \oplus T_{1u} \oplus T_{2g}$; Field Origin and octahedron $2A_{1g} \oplus E_g \oplus T_{1u}$). Under $T_d$, each eigenmode's mixing angle follows from an energy-dependent effective $2\times2$ block (the Schur complement of the octahedron and the Field Origin).
- Restrict the title, abstract and README claims accordingly.

*Response.* The proof is renamed to "the cube", matching the Hadamard cube frame proof. Theorem 2 is stated for the cube. A new Proposition 1 covers the pixel:
- **Alike (exact).** When TetA and TetB are alike, there is an eigenbasis whose corner parts are pure grades. The proof uses the four projectors $P_{A_1,T_2}(1 \pm P_{-I})/2$.
- **Different (numerical).** In general, each eigenmode's corner part is an eigenvector of $H_{\rm eff}(E) = H_{cc} + H_{cr}(E - H_{rr})^{-1}H_{rc}$. This operator is $T_d$-invariant, so it has the cube's block form with $E$-dependent entries, and the pairing holds mode by mode. The example shares 0.83, 0.007 and 0.98 are in the check.

**4. Two shares called "TetA share" (major, W2).** The node's $\mu = S_A/(S_A + S_B)$ is an *amplitude* share. The diamond-lattice result 9, $\mu = x/(1+x)$, is a *probability* share: the bonding orbital has amplitudes $(\sqrt g, \sqrt{a_0})$ and weight $g/(g+a_0)$ on the TetA end. These cannot both equal $x/(1+x)$:

| Reading | Condition on the $A_1$ eigenmode | Coupling condition | Other share |
|---|---|---|---|
| amplitude share $= x/(1+x)$ (Theorem 4(iii)) | $\tan\theta = 1/x$ | $\beta/(\alpha_A - \alpha_B) = x/(x^2-1)$ | probability share $x^2/(1+x^2)$ |
| probability share $= x/(1+x)$ | $\tan\theta = 1/\sqrt x$ | $\beta/(\alpha_A - \alpha_B) = \sqrt x/(x-1)$ | amplitude share $\sqrt x/(1+\sqrt x)$ |

The probability reading reproduces the diamond lattice's bond-orbital dictionary exactly. Polar energy $(\alpha_A - \alpha_B)/2$ plays the role of $V_3$, and $\beta$ the role of $V_2$, with $V_3/V_2 = (x-1)/(2\sqrt x)$ (checked symbolically). So Theorem 4(iii) is correct as an identity. But calling $\tan\theta = 1/x$ "the test linking the mixing angle to the constitutive law" picks the node's reading without saying so, and it contradicts the archive's earlier one. The same split already appeared in `pixel-lambda/`: a bright-state probability share $t_A^2/(t_A^2+t_B^2)$ versus a tiling share $t_A/(t_A+t_B)$.

Both readings pass the same sanity checks: at $x = 1$, $\theta = \pi/4$ and $\mu = \tfrac12$; as $x \to \infty$, $\mu \to 1$.

*Recommendation.* State both readings and both tests. Say that the node uses the amplitude share and the diamond-lattice work the probability share. Which one GFD's $\mu$ is, is a framework decision for the author, not something this proof can settle.

*Response.* Resolved from the framework's own text. Letter 3 states the partition as a division of the field: TetA carries $\mu$ of $g$ and TetB $1 - \mu$, and general relativity sees $\mu g = g_N$. In the linear reading, where corner values are field values, the bonding $A_1$ mode is proportional to $(g, a_0)$. Its chamber parts, scaled to total $g$, are then exactly $g^2/(g+a_0) = g_N$ and $ga_0/(g+a_0)$, the field equation's own split (new Proposition 3(ii), checked).

Every readout in the proof is linear in the corner values: the Walsh coefficients, the frames, and the node's $\mu$. So the linear reading is the consistent one for the cube.

The quadratic reading is kept as Proposition 3(iii). It is exactly the diamond lattice's bond-orbital dictionary, and it is the right reading when the field is the intensity of a lattice wave.

The proof states that the two agree only at $x = 1$. It also states that the choice between them concerns what a mode's amplitude represents, not $\mu$ itself, which is the same in both. The test is now stated as: compute a model's bonding $A_1$ mode and compare its angle with $a_0/g$.

**5. "Closure" (major, W3).** Two problems:
- **Two different closures share the name.** One is Letter 1's geometric closure $\sum v_i = 0$ (Theorem 3). The other is the node's dynamical relaxation rule (Theorem 4). The title and the "What has been proved" remark treat them as one.
- **The direction of the argument is reversed.** Theorem 3(ii) says the frame readout is blind to the uniform mode "exactly because of closure". But by Schur, every $T_d$-equivariant map to $\mathbb R^3$ kills $A_1$, and closure itself is forced by the same symmetry: the legs are a $T_d$-orbit, and $T_2$ has no invariant vector, so their sum is 0. Closure and blindness to the uniform mode are the same equation, and both are consequences of the symmetry. Neither causes the other.

"Must read" holds only for *linear* equivariant readouts. Quadratic invariants read every sector. Two examples:
- Parseval's total power, which drives the node's closure (Theorem 4(ii));
- the squared length of the frame readout, a scalar that reads the direction modes.

So "scalars read only $1$ and $xyz$" is a linear statement. The node's $\mu$ is nonlinear, but it is built from the two linear scalar readouts $S_A$, $S_B$, so it stays within the $A_1$ sector.

*Recommendation.*
- Name the two closures separately, for example frame closure ($\sum v_i = 0$) and the node's closure rule.
- Reword Theorem 3(ii) so that closure and blindness are one equation, both forced by $T_d$.
- Say in the final remark that the two-sector split is a property of linear readouts.

*Response.* Resolved using the framework's terms. The archive has a defined *field closure*, Letter 3's: both roots active, nothing held at zero. The proof now separates three things in its Setting:
- frame closure (Letter 1, $\sum v_i = 0$);
- field closure (Letter 3);
- the node's *closure rule*.

Theorem 3 is rebuilt around them:
- **(i)** uniqueness of the frame readout;
- **(ii)** frame closure is forced by the symmetry (the legs are one $T_d$-orbit, and $T_d$ fixes no nonzero vector), and is the same equation as the frame's blindness to the uniform mode;
- **(iii)** one root reads half of the spectrum, the collapse;
- **(iv)** field closure, $(S_A, S_B, R_A, R_B)$, is an invertible readout of all eight modes, and every equivariant linear readout factors through it; $\mu$ cannot be formed from TetA alone.

The text after the theorem says that the two-sector split is a property of linear readouts, with $\lvert R_A\psi\rvert^2$ as the counterexample. This answers the original question, whether field closure must read the Walsh modes, in its precise form: among linear symmetric readouts, field closure is what reads them all.

**6. The node's closure rule (minor, w3).** Theorem 4 covers only the amplitude update. The node's reconciliation step uses the closure rate for three updates:

| Update | Target | Spectrally blind? |
|---|---|---|
| amplitudes | the same for every corner | yes, proved |
| outward couplings | the same for every corner (1 in the bounded rule; $\min(r, 5)$ in the original) | yes |
| inward couplings | $c_k \leftarrow c_k + \kappa\,\mathrm{sign}(f_kb_k)(1 - \lvert c_k\rvert)$ | no: corner-local and signal-dependent |

The inward coupling never moves, only because it starts at its fixed point $c_k = 1$. A probe confirms this over 1,000 steps of random input and 1,000 steps of a pure-$x$ drive: all eight stay at 1. From any other starting value it can favour corners.

*Recommendation.* State all three updates. Prove the outward-coupling case too, and say that the inward-coupling update is inert only at its initial fixed point.

*Response.* Theorem 4 now states all three updates. A new check runs them on the node's code:
- amplitudes and outward couplings have one target for every corner;
- the inward couplings stay at their fixed point 1 over 800 steps;
- started at 0.5, the inward couplings spread across corners while relaxing to 1.

**7. The cube vortex (minor, w1).** Proposition 1 calls the grade-1 energy "doubly degenerate". It is triply degenerate ($x$, $y$, $z$). The rest is correct.

*Response.* Fixed: "triply degenerate grade-1 energy $t$ (spanned by $x, y, z$)".

**8. The corollary.** Correct. One clarification would help: "every vortex is built from direction modes" holds at the corners. The vortex also has its octahedron component, in the octahedron's own $T_2$ copy.

*Response.* Added: the vortex's octahedron part lies in the octahedron's $T_2$ copy.

**9. Range of $\mu$ (minor, w4).** For the other $A_1$ eigenmode ($\theta + \pi/2$), $\mu = 1/(1 - \cot\theta)$, which can fall outside $[0, 1]$; the node clamps it. Theorem 4(iii) should say it concerns the mode whose components have the same sign, the bonding mode.

*Response.* Proposition 3 is now stated for the bonding mode, $0 < \theta < \pi/2$, with the antibonding value $1/(1 - \cot\theta)$ given and checked.

## Assessment

The mathematics is correct. What needs care is the concepts.

**Change before circulating:**
- W1: scope the pairing theorem to the cube, and add the pixel statement.
- W2: state both shares and both tests.
- W3: separate the two closures, reverse the causal reading of Theorem 3(ii), and limit "must" to linear readouts.

**Minor fixes:**
- "triply degenerate" (w1);
- the s/p/d/f and d–p mixing positioning with a reference;
- all three of the node's updates (w3);
- which $A_1$ mode $\mu$ refers to (w4).

**What the proof contributes once these are fixed:**
- **A correct split.** Linear symmetric readouts divide the Walsh spectrum into a direction sector and an $A_1$ sector.
- **Vortices in the direction sector.** The pixel's vortices live there.
- **What the node's closure rule sees.** Total power and the $A_1$ ratio, and nothing else.
- **A sharpened open question.** The diamond-lattice probability reading and the node's amplitude reading give different tests, $\tan\theta = 1/\sqrt x$ and $\tan\theta = 1/x$. The framework has to say which share $\mu$ is.

*Status after revision.* Every point above has been addressed. The proof is now four pages, and its script passes 45/45.

## Reference added

- F. A. Cotton, *Chemical Applications of Group Theory*, 3rd ed. (Wiley, New York, 1990): orbital symmetries in $T_d$, and the mixing of p with d($t_2$).


## Framework alignment (2026-11-15)

A later check of every concept against the framework's own documents (the coupling algebra, the Coles notes, Letter 3, the field-closure and hourglass notes, the forced-frame proof) changed wording and scope, not results. One check was added for the metric's view of the grades, and one for the exchange $x \to 1/x$, giving 47 in all. The changes:
- **Prior work.** The coupling algebra already treats the cube under full symmetry, so it is cited, and the proof's new step is stated as keeping the chambers distinct.
- **Names.** The archive's names are used: constant mode, vector modes, bivector modes, chamber sign.
- **The Field Origin.** It is the central octahedron, with centre $O$.
- **Closure.** Letter 1's closure seals both chambers. Field closure keeps both roots. The forced-frame proof derives closure rather than assuming it.
- **One root.** One root reads time and space on the null cone, TetA's 3+1. The four modes it confuses with these are the four the metric cannot see.
- **The partition.** Proposition 3(ii) now states the TetA partition $g_s = \mu g_t$ (kinematic). It says the identical expression in the spherical field equation (dynamic) is a different statement, linked by the AQUAL identity.
- **Terms with GFD meanings.** "Drive" and "power" are replaced.
- **Scope.** The proof concerns the eight corner states, not the 64 transitions that field closure reads.
- **Nonlinearity.** The models are linear, while the Field Origin is nonlinear.
- **Metadata.** The PDF's title metadata is fixed.
