# Referee Review

*Internal review of "Vortices of the Stellated Octahedron" (commit e2093f5), written as a journal referee would, with the change made for each point. The revised proof is five pages, and its script now runs 81 checks. The numerical probes behind the findings below are independent of the verification script (numpy, random real parameters) and are summarised with each point.*

---

## Summary of the submission

The paper studies real symmetric Hamiltonians with $T_d$ symmetry on two graphs built from the stellated octahedron: the 15-site pixel and the 33-tile Triforce pixel. It proves the following:
- winding states vanish on the symmetry axis, and their current through a half-plane bounded by the axis is well defined (Lemmas 1–4);
- in the pixel, about an octahedron axis, there are exactly three winding states per sign, at the roots of an explicit secular equation, with current $I = -(E - \Delta_f)\rho^2$ (Theorem 1);
- without the octahedron nothing circulates (Corollary 1);
- a vortex is a rotating standing wave (Proposition 1);
- in the Triforce pixel the winding space splits as $W \oplus W'$, with doubled energies on $W$ and six generic vortices on $W'$ (Theorem 2).

**What holds up.**
- The lemmas are correct.
- The secular-equation argument is correct, and so are the explicit exceptional set and the certificate logic of Theorem 2(iv). Because $W'$ is fixed, $\det G$ is a nonzero constant, so the resultants specialise correctly and one nonvanishing point suffices.
- All 72 checks pass.

**What needs fixing.**
- **A sign convention.** It reverses every stated current direction.
- **The bond set.** One corollary depends on which bonds are included, so it is not a property of the stellated octahedron.
- **Interpretation.** The time-reversal degeneracy and the "rotation" of a stationary state are presented more strongly than the mathematics supports.
- **Positioning.** The paper is not set against the standard ring-current literature.

## Major points

**M1. The current's sign convention is reversed relative to the paper's own time evolution.**

The definition sets $J_{ij} = 2\,\mathrm{Im}(\bar\psi_i H_{ij}\psi_j)$. Lemma 1's own computation gives $\sum_j J_{ij} = 2\,\mathrm{Im}(\bar\psi_i(H\psi)_i)$. Under $\psi(t) = e^{-iEt}\psi$ (Proposition 1), that sum is $d\lvert\psi_i\rvert^2/dt$, the net flow *into* site $i$. So $J_{ij}$ is the flow from $j$ to $i$.

Both parts of the verification script, and the figure and render scripts, count $J_{ij}$ as flow from $i$ to $j$. Measuring the physical flow, with the same half-planes and the same states, gives

$$I = +(E - \Delta_f)\,\lvert\rho\rvert^2 .$$

The two calculations agree in magnitude to machine precision and are opposite in sign, checked on all three states at random parameters. A three-site ring with hopping $-t$ confirms which sign is physical: the state $e^{2\pi ik/3}$ flows toward increasing $k$, as a $+k$ Bloch wave should, while the paper's convention says the opposite.

What it affects:
- the sign in (iii);
- which of $\lambda = \pm i$ (or $\omega^{\pm1}$) circulates in the right-handed sense;
- the absolute swirl sense in figures 1 and 2. Each figure is still a correct picture of the antivortex at the same energy.

What it does not affect: magnitudes, $I \neq 0$, the exceptional set, the empty axis, and Theorem 2's certificates, since $f \neq 0$ does not depend on sign.

*Recommendation.* Pick one of two fixes:
- define $J_{ij}$ as the flow from $i$ to $j$, $J_{ij} = 2\,\mathrm{Im}(\bar\psi_j H_{ji}\psi_i)$, and change (iii) to $I = (E - \Delta_f)\lvert\rho\rvert^2$; or
- keep the definition, say explicitly that it is the flow from $j$ to $i$, and fix the scripts' crossing orientation to match.

Then regenerate the figures, or relabel them as antivortices.

*Response.* The definition is now $J_{i\to j} = 2\,\mathrm{Im}(\bar\psi_j H_{ji}\psi_i)$, the flow from $i$ to $j$. Lemma 1 now states $d\lvert\psi_j\rvert^2/dt = \sum_i J_{i\to j}$. Formula (iii) now reads $I = (E - \Delta_f - 2h)\lvert\rho\rvert^2$, with M2's extension included. The changes elsewhere:
- **Script.** Both parts of the script use the physical orientation. A new convention check (CV) proves the continuity identity symbolically, and confirms on a three-site ring that a $+k$ Bloch state flows toward increasing $k$.
- **Figures.** The figure and render scripts now use the physical flow, and both images were regenerated.
- **Research notes.** The research notes in `vortex-theorem/` and `pixel-vortex/` carry a correction notice.

**M2. The bond set is not nearest-neighbour, and Corollary 1 depends on it.**

The abstract calls the models "the most general nearest-neighbour Hamiltonians". In the pixel, the distances are:

| Bond | Length | In $\mathcal P$? |
|---|---|---|
| Field Origin – octahedron vertex | 1 | yes |
| octahedron vertex – corner | $\sqrt2$ | yes |
| octahedron vertex – octahedron vertex (octahedron edges) | $\sqrt2$ | **no** |
| Field Origin – corner | $\sqrt3$ | yes |
| corner – corner (cube edges, each joining TetA to TetB) | 2 | **no** |

So the graph includes a $\sqrt3$ bond but leaves out a $\sqrt2$ bond. The results are properties of this graph, not of nearest-neighbour coupling on the stellated octahedron. The probes show:
- **Corollary 1 is an artefact of leaving out the cube edges.** With cube edges added and the octahedron removed, the two corner winding states carry $I \approx \pm 0.055$, so the corners circulate on their own. "Without the octahedron nothing circulates" holds only because $\mathcal P$ has no corner–corner bonds, which also makes the corollary nearly immediate.
- **With octahedron edges, Theorem 1(i)–(ii) survive and (iii) changes, exactly.** The 3×3 block is unchanged, because the ring terms carry $\lambda + \bar\lambda = 0$. So the energies, the secular equation and the locking are unchanged. The current gains the ring-edge term; with the physical sign, and $h$ the octahedron-edge matrix element,
  $$I = (E - \Delta_f + 2h)\,\lvert\rho\rvert^2 ,$$
  verified to $10^{-10}$ on twelve states. The exception in (iv) moves to $E = \Delta_f - 2h$.
- **With cube edges, the block gains a TetA–TetB entry,** and the secular equation itself changes. Vortices still exist at random parameters.

*Recommendation.*
- Replace "nearest-neighbour" with a precise description: "graph-local on the stated bonds". Justify the bond set from GFD (coupling through the Field Origin and across the octahedron's faces), or extend the class.
- The octahedron-edge extension costs one line and makes Theorem 1 stronger; include it.
- State Corollary 1 as conditional on there being no corner–corner bonds.
- Give the Triforce adjacency (edge-sharing tiles, plus the central tiles to $O$) the same justification.

*Response.* All four recommendations are adopted.
- **The class.** The Setting now has a paragraph, "The bond sets", saying the graphs are not nearest-neighbour graphs and that the results are about these graphs. The abstract no longer says "nearest-neighbour".
- **The octahedron's edges.** The pixel graph now includes the octahedron's twelve edges, with hopping $h$, so the class has 10 parameters. The text shows why $h$ leaves the block unchanged ($-h(\lambda + \bar\lambda) = 0$). Theorem 1(iii) gives $I = (E - \Delta_f - 2h)\lvert\rho\rvert^2$, with the ring-edge term derived by hand. The exception (iv) moves to $E = \Delta_f + 2h$, which reduces to the old condition at $h = 0$. Part I's certificates now run on the extended graph.
- **Corollary 1.** It is now stated for the bonds of $\mathcal P$. The text after it, and a new check (C1′), give the exact counterexample with the cube's edges: winding eigenstates with currents $\pm1/\sqrt5$.
- **The cube's edges.** A remark, "Other bonds", records that they give the block a TetA–TetB entry, and that Theorem 1 is not claimed for that graph.

**M3. Time reversal: every vortex level is degenerate, so the current depends on a choice of basis. "Persistent" and "rotates" are overstated.**
- **Every vortex energy is shared with its antivortex.** $H$ is real, so every energy in $V_{+i}$ also occurs in $V_{-i}$ (Lemma 3), and every vortex level is at least doubly degenerate. Within the level, the vortex, the antivortex and the zero-current standing wave (Proposition 1(iii)) are equally valid eigenbases.
- **Nothing in the theorems selects a vortex.** Any time-reversal-invariant mixed state, thermal or equilibrium, carries zero net current. A vortex is singled out only by an initial condition or by breaking time reversal (a flux, a rotation).
- **"Persistent current" is the wrong term.** In the literature it means an equilibrium current in a time-reversal-broken ring (Büttiker, Imry and Landauer 1983). That is not what is shown here.
- **Proposition 1(ii) describes a global phase in the quantum reading.** For an eigenstate, $\lvert\psi(t)\rvert^2$ and every $J_{ij}$ are constant in time, so nothing observable rotates. The statement $S\psi(t) = \psi(t - \pi/2E)$ is about a global phase. The delay $\pi/2E$ depends on the choice of energy zero and is undefined at $E = 0$.
- **The proposition is correct in a classical-wave reading.** Take a real field $u(t) = \mathrm{Re}(e^{-iEt}\psi)$, with $E > 0$ a frequency, as in the archive's coupled-oscillator node. Then $u$ is a pattern that genuinely rotates, and $u$ built from $\psi + \bar\psi$ is a standing wave. Read this way, $J_{ij}$ is proportional to the power flowing along the bond.

*Recommendation.*
- Drop "persistent".
- Add a remark on the degeneracy and on what would select a vortex.
- State Proposition 1 in the classical-oscillator reading, with $E > 0$ (or $\lvert E\rvert$), and say that in the quantum reading the rotation is a phase rotation only.
- Make the abstract match.

*Response.*
- **Persistent.** "Persistent" is gone.
- **Time reversal.** A remark, "Time reversal", after the lemmas now covers four things: every vortex level is shared with its antivortex; currents depend on the choice of eigenbasis within a level; a time-reversal-invariant mixed state carries no net current; and a vortex is selected only by an initial condition or by broken time reversal. It also says these are not persistent currents in the sense of Büttiker, Imry and Landauer.
- **Proposition 1.** It is now stated for the real field $u(t) = \mathrm{Re}(e^{-iEt}\psi)$ with $E > 0$. That is the coupled-oscillator reading, where $J$ is the power along a bond. The proposition contrasts this explicitly with the quantum reading, where the quarter turn is a global phase.
- **Checks.** The script checks both readings (P1).

**M4. Positioning: current-carrying states of symmetric real Hamiltonians are standard.**

That a real Hamiltonian with $C_n$ (or $S_n$) symmetry has complex eigenstates with nonzero winding, and that these carry ring currents, is textbook. Examples:
- the degenerate $m = \pm1$ orbitals of benzene and the ring-current model (London 1937; Pople 1956);
- orbital contributions to ring currents (Steiner and Fowler 2001).

The general lemmas (empty axis, conservation, antivortices) are this standard material on a new graph. What is new and specific is:
- the closed-form block and current for the pixel;
- the locking of the corners to the ring;
- the explicit exceptional set;
- the exact $W \oplus W'$ structure of the Triforce.

*Recommendation.* Cite the ring-current literature in one paragraph and state the contribution as the graph-specific results above. That also removes the impression that the existence of vortices is itself the discovery.

*Response.* The time-reversal remark now cites London (1937), Pople (1956) and Steiner and Fowler (2001). It calls the vortices the discrete analogues of the degenerate $m = \pm1$ orbitals behind aromatic ring currents. A new remark, "Positioning", states the contribution as the graph-specific results. The Steiner–Fowler reference was checked: *J. Phys. Chem. A* **105**, 9553 (2001).

## Minor points

**m1. Theorem 2(ii)–(iii) have a short hand proof, which would replace the symbolic computation.**

*Representation theory gives (ii).* The 33-tile representation of $T_d$ decomposes as $5A_1 \oplus 2E \oplus 2T_1 \oplus 6T_2$. The Field Origin and the central tiles carry only $A_1 \oplus T_2$. By Schur's lemma, the $E$ and $T_1$ isotypic parts never couple to them, for any $H$. So
$$W = V_\omega \cap (E \oplus T_1),$$
which has dimension $2 + 2 = 4$. This matches the probe exactly: the $T_d$-span of $W$ has character $2E + 2T_1$.

*A local structure gives (iii), in closed form.* The $E$ and $T_1$ vectors on the outer tiles sum to zero on each star point, since the four star-point sums of a chamber carry $A_1 \oplus T_2$. Two facts follow:
- every outer–outer bond between tiles of the same chamber lies inside one star point, so a zero-sum vector on the star point's triangle has eigenvalue $-1$ under its adjacency;
- each outer tile shares its octahedron edge with exactly one outer tile of the other chamber, a $T_d$-equivariant pairing.

So on $W$, $H$ acts as the same 2×2 matrix on the $E$ part and on the $T_1$ part:
$$\begin{pmatrix}\epsilon_{EA} - h_A & h_{AB}\\ h_{AB} & \epsilon_{EB} - h_B\end{pmatrix},$$
where:
- $\epsilon_{EA}, \epsilon_{EB}$ are the outer-tile energies;
- $h_A, h_B$ are the matrix elements on the bonds inside a star point;
- $h_{AB}$ is the matrix element on the TetA–TetB pairing bond.

The probe matched its eigenvalues to the doubled energies on $W$ to $10^{-9}$ at five random points. This explains the doubling, which the paper currently only verifies. It also makes the current form on $W$ explicit, so (iii)'s "definite at some points, indefinite at others" can be stated as an exact condition.

*Response.* Adopted as the proof of Theorem 2(ii)–(iii). The theorem now names the two parts: $W = V_\omega \cap (E \oplus T_1)$ and $W' = V_\omega \cap T_2$. The 2×2 matrix $M$ is displayed as equation (4). The script checks:
- the decomposition $5A_1 \oplus 2E \oplus 2T_1 \oplus 6T_2$;
- that the Field Origin and the central tiles carry no $E$ or $T_1$;
- the local structure: bonds within a star point, and a one-to-one pairing across the chambers;
- the closed form for $M$, in all 15 parameters.

The earlier symbolic checks of invariance and doubling remain as a cross-check.

**m2. "That ring turns" (Theorem 2(iv)) needs one more line.** The certificate $g(E) \neq 0$ shows that the ring has nonzero *weight*. The ring's three tiles form one orbit, so their bond currents are $\pm\sqrt3\,h_A\lvert r\rvert^2$, which is nonzero whenever $h_A \neq 0$. Add that line, and add $h_A \neq 0$ to the exceptional set.

*Response.* Added to the proof of Theorem 2(iv), and to the statement, with the magnitude $\sqrt3\,\lvert t_A\rvert\lvert r\rvert^2$. Checked symbolically.

**m3. $\rho$ is used in two senses.**
- In the proof, $w = (\rho, p, q)$ are coordinates in the *normalised* basis.
- In (ii) and (iii), $\rho$ is the amplitude on a ring site, half the coordinate.

Formula (iii) holds for the site amplitude, as checked numerically. Define $w$ as site amplitudes, which leaves all three row equations unchanged, and write $\lvert\rho\rvert^2$.

*Response.* $w = (\rho, p, q)$ are now defined as site amplitudes, and the formulas use $\lvert\rho\rvert^2$.

**m4. The proof of Theorem 1 should state the interlacing.** Monotonicity alone doesn't give "three distinct roots". The full argument is that the function decreases strictly from $+\infty$ to $-\infty$ on each of the three intervals cut by $\epsilon_A$ and $\epsilon_B$, so there is exactly one root in each. This also shows the energies interlace with the corner energies, which is worth stating.

*Response.* Theorem 1(i) now states one root per interval, and the proof gives the full argument: $F$ runs from $-\infty$ to $+\infty$ on each interval. A new check verifies the residues at the poles and the behaviour at infinity.

**m5. Derive the block (1) in a line.** For example, the ring vertex $\hat x$ meets the TetA corners $(1,1,1)$ and $(1,-1,-1)$, whose winding phases differ by $\lambda$, so $\lvert a\rvert^2 = c_A^2\lvert 1 + \lambda\rvert^2 = 2c_A^2$.

*Response.* Added before Theorem 1, including why the octahedron edges and the Field Origin drop out of the block.

**m6. Define the current through a half-plane precisely.** Lemma 2's wedge argument needs three things, which should be stated:
- bonds are embedded as straight segments;
- the half-plane is in general position, with no off-axis site on it;
- no bond between two off-axis sites meets the axis.

Each bond then sweeps less than $\pi$ about the axis, so the wedge argument holds. The script already enforces the general-position condition with an assertion.

*Response.* A "Half-planes" paragraph in the Setting states the three conditions. That no bond between two off-axis sites meets the axis was checked for both graphs. Lemma 2's proof now gives the wedge argument in full.

**m7. The first Remark uses an undefined $x$.**
- "Away from the ring $x = 1$" never defines $x$ (in the archive, $g/a_0$), and $x$ is also a coordinate in the paper.
- A plain $C_4$ symmetry needs *all* TetA and TetB parameters equal ($\epsilon$, $c$ and the $O$ couplings). The paper never links its parameters to $g/a_0$.
- At equal parameters, Theorem 1's hypothesis $\epsilon_A \neq \epsilon_B$ fails.

Restate the remark in terms of the parameters, or move the link to $x$ into the interpretation with a reference.

*Response.* The remark is now headed "GFD reading" and labelled as interpretation. It refers to $g/a_0 = 1$ by name. It says a plain quarter turn needs *all* TetA and TetB parameters equal, and that Theorem 1's hypothesis then fails.

**m8. The second Remark asserts a linking number of 0 without defining "strands" or proving it.** Define and prove it, or drop it.

*Response.* Dropped.

**m9. "Flywheel", "drives" and "the octahedron circulates" are interpretive.** The current through any half-plane runs ring vertex → corner → ring vertex, so the ring and the corners carry it jointly. The theorem proves locking (proportional amplitudes), not that one part drives the other. Label these as GFD interpretation in the Remark.

*Response.* "Drives" is gone from the paper, the figures and the README. The figure titles now say the corners and the ring "carry the current together" and are "locked". The flywheel image appears only in the GFD-reading remark.

**m10. Housekeeping.**
- The header reads "Supplementary Material" for a standalone proof.
- The bibliography lists NelsonGram and Coxeter but never cites them.
- The abstract's "every statement below holds for this whole class" should say "for this class, under the stated hypotheses".
- The phrase "three random rational points" would be clearer as "three fixed pseudo-random rational points". One point suffices for the certificates; three is a consistency check.
- Part II of the script uses sympy, so the all-parameter statements rely on computer algebra unless m1's hand proof is adopted. The abstract's "no computer algebra" applies to Part I only, and should say so.

*Response.*
- The header now reads "Proof".
- NelsonGram and Coxeter are cited in the Setting.
- The Setting says the statements hold "under the hypotheses stated with each".
- The Verification section says "fixed pseudo-random", and states that Part II uses sympy.
- The abstract says the no-computer-algebra certificates are the generic ones.
- Serre is cited for Schur's lemma.

## Assessment

The mathematics is sound once M1 is fixed, and Theorem 1 improves with M2's extension.

**Change before circulating:**
- the sign (M1);
- the class description and Corollary 1 (M2);
- the time-reversal remark and the reading of Proposition 1 (M3).

**Recommended but not blocking:**
- the hand proof of the Triforce split and doubling (m1);
- positioning against the ring-current literature (M4).

With those changes the paper makes a correct and modest claim: these symmetric pixel graphs carry exactly characterised circulating eigenstates, with explicit structure.

*Status after revision.* Every point above has been addressed. The revised proof states the correct sign, the extended pixel graph, and what the vortices do and do not imply. Its script passes 81/81.

## References added

- F. London, *J. Phys. Radium* **8**, 397 (1937): ring-current theory of aromatic molecules.
- J. A. Pople, *J. Chem. Phys.* **24**, 1111 (1956): proton magnetic resonance and ring currents.
- E. Steiner and P. W. Fowler, *J. Phys. Chem. A* **105**, 9553 (2001): orbital contributions to ring currents.
- M. Büttiker, Y. Imry and R. Landauer, *Phys. Lett. A* **96**, 365 (1983): persistent currents in rings.
- J.-P. Serre, *Linear Representations of Finite Groups* (Springer, 1977): Schur's lemma and isotypic components.


## Framework alignment (2026-11-15)

A later check of every concept against the framework's own documents changed wording, not results; the 81 checks are unchanged. The changes:
- **The Field Origin.** It is the central octahedron in which the chambers intersect, with centre $O$ (Coles notes). The proof called only the centre "the Field Origin". It now speaks of the Field Origin's centre and equator.
- **The bond set.** It is now justified by GFD's position that TetB is reached only through the Field Origin. Corollary 1 is read in that light.
- **The Triforce.** Its tiles are named as the archive's outer sub-channels (spatial coupling) and central sub-channels (gravitational coupling). The leg vortex's empty core is the gravitational coupling line.
- **"Power".** Proposition 1 no longer calls $J$ "power".
- **"Not claimed".** It now records that the Field Origin is nonlinear in GFD, and that flow along the axis, the hourglass's through-flow, is not fixed.
