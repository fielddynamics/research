# Active Work 07 — Maxwell's Theory in the Framework

**Status:** Active — structural identification of EM in the K=4 closure-read
**Purpose:** Push on Maxwell using the framework's existing algebra: the parity-character of $T_{\le 2}(V)$, the three readings at $K=4$, Coulomb attenuation, Sierpinski hierarchy, TetA/TetB.
**Reading time:** 12 minutes
**Companion:** [02.1 gravity equation](../02_gravity_derivation/02.1_gravity_equation.md), [03 parity-character upgrade](03_parity_character_upgrade.md), [04 core theory integration](04_core_theory_integration.md)

---

## 1. Result

The electromagnetic field tensor $F^{\mu\nu}$ lives in the antisymmetric subsector $\Lambda^2 V$ of $V \otimes V$ at $K=4$. Its 6 components are the 6 edges of the tetrahedron $K_4$. The three perfect matchings of $K_4$ give the standard self-dual / anti-self-dual decomposition of $F$ into $3 + 3$ complex components. The two-tetrahedra structure of the stellated octahedron gives a natural geometric setting for the dual Maxwell theory with magnetic monopoles, with $\nabla \cdot B = 0$ in our universe identified as the empirical statement that the TetB magnetic-charge sector is empty.

The framework's $\alpha^{21}$ gravity equation already establishes EM ($\alpha^1$) as the primitive coupling and gravity as a 21-fold composition. This document extends the identification to the full structure of Maxwell's theory.

---

## 2. The K=4 closure-read decomposition

At $K=4$ with $V$ the 4-vector index space, the closure-read is:

$$\mathcal{C}_4 \;=\; \Lambda^4 V \,\oplus\, V \,\oplus\, V \otimes V \;=\; \mathbf{1} \,\oplus\, \mathbf{4} \,\oplus\, \mathbf{16}$$

The tensor square $V \otimes V$ at $K=4$ has dimension 16. Under $\mathrm{GL}(4)$ or $\mathrm{SO}(3,1)$, it decomposes as:

$$V \otimes V \;=\; \mathrm{Sym}^2 V \,\oplus\, \Lambda^2 V \;=\; \mathbf{10} \,\oplus\, \mathbf{6}$$

- **$\mathrm{Sym}^2 V$ (10 components)** — symmetric rank-2 tensor sector
  - trace (scalar): 1 component
  - traceless symmetric: 9 components — **the metric perturbation $h_{\mu\nu}$ sector, gravity**
- **$\Lambda^2 V$ (6 components)** — antisymmetric rank-2 tensor sector
  - **the electromagnetic field tensor $F^{\mu\nu}$**

**Both gravity and electromagnetism inhabit the same closure-read at $K=4$.** Gravity sits in the symmetric subsector; electromagnetism sits in the antisymmetric subsector. Together they exhaust the 16-dimensional tensor-square sector.

The full closure-read accommodates also:
- The volume form $\Lambda^4 V$ (1 component) — orientation / determinant of the metric
- The 4-vector sector $V$ (4 components) — 4-current $J^\mu$ or gauge potential $A_\mu$

These last two are not algebraically tied to gravity or EM individually but provide the source content and gauge structure.

---

## 3. EM as the tetrahedral edges

$\Lambda^2 V$ at $K=4$ has basis $\{e_i \wedge e_j : 0 \le i < j \le 3\}$, six elements. Identifying $\{e_0, e_1, e_2, e_3\}$ with the four vertices of the tetrahedron $K_4$:

$$\Lambda^2 V \;\cong\; \text{edge space of } K_4$$

The 6 $F^{\mu\nu}$ components are the 6 edges:

| Edge | $F^{\mu\nu}$ component | E/B identification |
|:---:|:---:|:---:|
| $e_0 \wedge e_1$ | $F^{01}$ | $E_x / c$ |
| $e_0 \wedge e_2$ | $F^{02}$ | $E_y / c$ |
| $e_0 \wedge e_3$ | $F^{03}$ | $E_z / c$ |
| $e_1 \wedge e_2$ | $F^{12}$ | $-B_z$ |
| $e_1 \wedge e_3$ | $F^{13}$ | $+B_y$ |
| $e_2 \wedge e_3$ | $F^{23}$ | $-B_x$ |

**Pattern.** The three time-space edges ($i=0$) carry the electric field components. The three space-space edges (the "triangular face" of the tetrahedron opposite the time vertex) carry the magnetic field components. The $E$/$B$ split is the **time-vs-space edge split** of the tetrahedron.

This is a clean geometric identification: the electromagnetic field is the **edge content** of the K=4 tetrahedron, partitioned by incidence with the time vertex.

---

## 4. The self-dual / anti-self-dual decomposition

On $\Lambda^2 V$ in 4D Lorentzian signature, the Hodge star satisfies $\ast \ast = -1$ (signature $-+++$). The complex decomposition:

$$F \;=\; F_+ + F_-, \qquad \ast F_\pm \;=\; \pm i F_\pm$$

splits the 6-dimensional $\Lambda^2 V$ into two 3-dimensional complex subspaces. $F_+$ is the self-dual part; $F_-$ is the anti-self-dual part.

**Tetrahedral identification.** The 6 edges of $K_4$ admit exactly **3 perfect matchings** — three ways to pair the edges into non-adjacent triples. Each perfect matching is a triple of opposite edges:

| Matching | Opposite edge pair |
|:---:|:---:|
| 1 | $(0,1) \leftrightarrow (2,3)$ — temporal-$x$ / spatial-$yz$ |
| 2 | $(0,2) \leftrightarrow (1,3)$ — temporal-$y$ / spatial-$xz$ |
| 3 | $(0,3) \leftrightarrow (1,2)$ — temporal-$z$ / spatial-$xy$ |

Each matching pairs one $E$ component with one $B$ component. The three matchings are the three "axes" of the tetrahedron, and they give the three components of $F_+$ and $F_-$:

$$F_\pm^{(k)} \;=\; \frac{1}{2}\left( E^k \pm i c B^k \right), \qquad k = x, y, z$$

The 3+3 split of $F$ is the framework's $\Lambda^2 V$ split along the three perfect matchings of $K_4$.

**This connects directly to the framework's algebraic structure.** The $\Phi_3(K) = 21$ at $K=4$ counts the closure-read total. The $\Phi_4(K) = 17$ counts the even sector. The $\Phi_6(K) = 13$ counts the parity-graded reading. In the EM sector specifically:

- $\dim \Lambda^2 V = 6 = 3 + 3$ — the F's complex decomposition
- The 3 corresponds to $K - 1$ at $K=4$, the count of "self-axis" projections
- $\dim \Lambda^4 V = 1$ — the volume form, the framework's "scalar" reading

---

## 5. TetA and TetB: two F-fields, one stellated octahedron

The framework's stellated octahedron compound has two interpenetrating tetrahedra:
- **TetA** with 4 vertices, 6 edges, 4 faces
- **TetB** with 4 vertices, 6 edges, 4 faces
- Together: 8 vertices (cube), 12 edges (octahedron edges), 8 faces

Each tetrahedron carries its own $\Lambda^2 V$ — its own 6-dimensional edge sector. Two tetrahedra give:

$$\Lambda^2 V_{\text{TetA}} \,\oplus\, \Lambda^2 V_{\text{TetB}} \;=\; \mathbf{6} \,\oplus\, \mathbf{6} \;=\; \mathbf{12}$$

The 12 edges form the octahedron inscribed in the compound. There are two natural identifications.

**Identification 1.** TetA carries the electric field tensor $F_e$; TetB carries the magnetic-dual field tensor $F_m = \ast F$. Each tetrahedron carries one "half" of the full Maxwell structure. Standard Maxwell only sees $F_e$ because the universe's TetB-charge sector is empty (see §6).

**Identification 2.** TetA and TetB carry the self-dual and anti-self-dual parts of a single $F$. The 3+3 split of §4 is realized geometrically as TetA's 6 edges projected to its 3 perfect matchings.

The two identifications are related by Hodge duality: in identification 1, the field on TetB is the Hodge dual of the field on TetA; in identification 2, the two tetrahedra carry the self-dual and anti-self-dual decomposition of the same field.

The framework's TetA $\leftrightarrow$ TetB exchange symmetry maps to the **electric-magnetic duality** $F \leftrightarrow \ast F$ of Maxwell's theory. This is consistent with the parity-character structure: the framework's $\mathbb{Z}/2$-grading is the algebraic statement of an exchange symmetry, and EM has an exchange symmetry that fits exactly.

---

## 6. $\nabla \cdot B = 0$ as an empirical TetB-charge statement

Standard Maxwell has $\nabla \cdot E = \rho_e / \varepsilon_0$ and $\nabla \cdot B = 0$. The asymmetry is empirical: electric charges exist; magnetic monopoles have not been observed.

In the framework's two-tetrahedra picture, the natural Maxwell theory is **fully dual**:

$$\partial_\mu F_e^{\mu\nu} \;=\; J_e^\nu / \varepsilon_0 c^2$$
$$\partial_\mu F_m^{\mu\nu} \;=\; J_m^\nu / \varepsilon_0 c^2$$

with $F_e$ on TetA, $F_m = \ast F_e$ on TetB, electric current $J_e$ on TetA, and magnetic current $J_m$ on TetB.

The empirical observation $\nabla \cdot B = 0$ is the statement that $J_m = 0$ in our sector — **TetB carries no magnetic charges** in the regime we observe. This is the EM analog of the gravity case where $\mu(x) \approx 1$ at solar-system scales: the TetB sector is dynamically suppressed, and Maxwell appears as a single-tetrahedron theory.

**Predicted asymmetry.** Gravity's TetB sector is dynamically active at low accelerations ($g \ll a_0$) and produces what is empirically observed as MOND or dark matter. EM's TetB sector should have an analogous activation regime — a low-field-strength scale where magnetic monopole effects would emerge. The framework predicts a scale $F_m \sim $ Schwinger-like critical field at which TetB-magnetic activates. Above this scale, $\nabla \cdot B = 0$; below it, $\nabla \cdot B \ne 0$ from TetB-magnetic monopole creation.

**The Dirac quantization condition** $e \cdot g = n \hbar c / 2$ takes a natural framework form: the product of TetA-electric charge and TetB-magnetic charge is a multiple of the closure-read fundamental quantum.

---

## 7. The α^1 Coulomb step as the framework's primitive

The framework's gravity equation derives $G$ from $\alpha^{21}$. The exponent 21 = three sweeps × seven levels per sweep at $K=4, D=3$ ($K + D - 1 = 7$). Each sweep is an $\alpha^7$ attenuation through one parity-character reading.

A **single Coulomb step** in QED is a single photon exchange between two charged particles, with amplitude proportional to $\alpha = e^2/(4\pi\varepsilon_0 \hbar c) \approx 1/137.036$. The Coulomb potential between two electrons:

$$V_{\text{Coulomb}}(r) \;=\; -\frac{\alpha \hbar c}{r}$$

contains one factor of $\alpha$. In framework language: one Coulomb step = $\alpha^1$ = the framework's primitive coupling step.

The gravity equation is then a composition:

$$\alpha_G \;\sim\; \alpha^{21} \;=\; \underbrace{\alpha^7}_{\text{first sweep}} \cdot \underbrace{\alpha^7}_{\text{second sweep}} \cdot \underbrace{\alpha^7}_{\text{third sweep}}$$

Each sweep is seven Coulomb steps. Three sweeps give 21 Coulomb steps. Gravity is the composition of 21 Coulomb exchanges, organized into three parity-character readings.

This puts EM as the **fundamental** force in the framework, and gravity as a derived 21-step composition. The hierarchy:

| Level | Coupling | Coulomb steps |
|:---:|:---:|:---:|
| 1 | EM | 1 |
| 7 | first sweep | 7 |
| 14 | second sweep | 14 |
| 21 | gravity | 21 |

The number 7 has the framework interpretation $K + D - 1$ at $K=4, D=3$: seven non-trivial spatial modes per parity sweep.

---

## 8. Maxwell's equations parity-graded

The four Maxwell equations couple $F$ (even sector, in $\Lambda^2 V \subset V \otimes V$) to $J$ (odd sector, in $V$):

$$\partial_\mu F^{\mu\nu} \;=\; \mu_0 J^\nu \qquad\text{(sourced equations, Gauss + Ampère)}$$
$$\partial_{[\mu} F_{\nu\rho]} \;=\; 0 \qquad\text{(Bianchi identity, source-free equations)}$$

In framework terms:

- **Sourced Maxwell**: even-sector field ($F$) couples to odd-sector current ($J$). This is an even-to-odd coupling, the parity-graded statement of "field sourced by current."
- **Bianchi identity**: pure even-sector constraint. No coupling to the odd sector. The closure of the parity-even subspace under exterior derivative.

The framework's three readings on Maxwell's equations:

| Reading | $s$ | Operator on $\mathcal{C}_4$ | What it sees |
|:---:|:---:|:---|:---|
| $\mathbb{I}_{+1}$ | $+1$ | identity | full Maxwell content: $F + A + \det g$ (21 components) |
| $\mathbb{I}_{0}$ | $0$ | even-projector | field strength + scalar (17 components, drops $A_\mu$) |
| $\mathbb{I}_{-1}$ | $-1$ | parity operator | parity-graded reading (13 components, subtracts $A_\mu$) |

The $\mathbb{I}_0$ reading is **gauge-invariant**: it drops the 4-potential $A_\mu$ (the odd-sector content that has gauge ambiguity) and retains only the field strength $F$ and the scalar volume form. This is structurally meaningful: the parity-even closure-read at $K=4$ is the **gauge-invariant** content of Maxwell's theory.

This identifies a structural role for the parity-even reading: it is the projection onto gauge-invariant content. The "even-dimension trace" $\Phi_4(4) = 17$ counts the gauge-invariant degrees of freedom of Maxwell + scalar at $K=4$.

---

## 9. Resonance: cavity modes at Niven angles

A resonant EM cavity (rectangular box, dimensions $a \times b \times c$) has modes:

$$\omega_{mnp} \;=\; c \sqrt{(m\pi/a)^2 + (n\pi/b)^2 + (p\pi/c)^2}$$

In the framework's parity-character language (Active Work 04), the closure-read reads at three Niven-quantized angles $\theta \in \{\pi/3, \pi/2, 2\pi/3\}$ — the only finite-order rotations giving degree-2 cyclotomic polynomials.

A cavity designed with internal phase content at the three Niven angles would have its mode spectrum **lock** to the closure-read structure. Specifically:

- A cavity with $\theta = \pi/3$ phase content reads at $\Phi_3$ — 21-mode structure (Grand Gallery-like spectrum)
- A cavity with $\theta = \pi/2$ phase content reads at $\Phi_4$ — 17-mode structure
- A cavity with $\theta = 2\pi/3$ phase content reads at $\Phi_6$ — 13-mode structure

The King's Chamber's Z_21 = Z_3 × Z_7 acoustic spectrum (§07.1 of the main project) is the apparatus realization of the Niven $\Phi_3$ reading at $K=4$. The framework's general claim: **EM cavities with internal $\theta = \pi/3$ phase structure have parity-character-locked mode spectra at the 21-comb**.

Specific testable prediction: a cavity with three-fold rotational symmetry (e.g., a triangular waveguide, or a 3-electrode coaxial structure) should exhibit mode clustering at the $\Phi_3$ pattern, not the standard rectangular-cavity $m^2 + n^2 + p^2$ spectrum.

This is the framework's structural claim about EM resonance: the resonance spectrum locks to the cyclotomic structure when the cavity's internal phase content matches a Niven angle.

---

## 10. Coulomb decay through Sierpinski hierarchy

The framework's Sierpinski packing hierarchy generates nested tetrahedral structures: at level $n$, the packing has $4^n$ small tetrahedra arranged in a self-similar pattern. The scale-fusion identity $\Phi_3(K) \cdot \Phi_6(K) = \Phi_3(K^2)$ (Theorem 5 of Active Work 04) lifts the closure-read structure from $K=4$ to $K=16$ to $K=256$ and so on.

**For Coulomb-like potentials**, this implies a hierarchy of effective coupling at different length scales:

- $K=4$ closure-read: bare Coulomb $V \sim \alpha/r$ at the elementary scale
- $K=16$ closure-read (second-order): composite Coulomb at the Sierpinski-level-1 scale
- $K=K^2$ closure-read (nth-order): composite Coulomb at the Sierpinski-level-$n$ scale

The composite Coulomb potentials might have effective fall-off laws that differ from $1/r$ at intermediate scales. The framework predicts the specific scale dependence comes from the closure-read structure at each Sierpinski level.

**Note on speculation.** This is the most speculative section of this document. The Sierpinski hierarchy is established in the framework's nuclear binding energy work (where it gives $BE(64) = 16 \cdot BE(4) + 4\epsilon_1 + \epsilon_2$), but its application to Coulomb-scale physics is not currently developed in detail. The structural claim — scale-fusion lifts to composite couplings — follows from the existing algebra but the specific predictions require more work to make falsifiable.

---

## 11. The constitutive law for EM: candidate forms

The gravitational partition $\mu_{\text{grav}}(x) = x/(x+1)$ with $x = g/a_0$ governs the TetA/TetB share of the gravitational field. For EM, the candidate analog requires identifying the EM-analog of $x$ and $a_0$.

**Three candidates for the EM partition variable.**

(a) **Field strength ratio.** $x_{\text{EM}} = F^2 / F_S^2$, with $F_S$ the Schwinger critical field $\approx 1.32 \times 10^{18}$ V/m. Below this scale, EM is linear (TetA-dominant); above this scale, vacuum polarization activates a TetB-like response.

(b) **Coupling-strength ratio.** $x_{\text{EM}} = \alpha / \alpha_{\text{ref}}$ for some reference coupling. Since $\alpha$ itself is the framework's primitive coupling, this is a self-referential identification that doesn't immediately produce a partition.

(c) **Charge-density ratio.** $x_{\text{EM}} = \rho_e / \rho_{e,\text{crit}}$ for a critical charge density. This is most analogous to the gravity case, where $a_0$ is a critical acceleration scale.

**The empirical observation.** Standard Maxwell is linear to extreme precision over many decades of field strength. There is no observed EM-MOND transition. Either:

1. The EM partition $\mu_{\text{EM}}$ is fixed at 1 (or 0) in our regime, with no observable deviation.
2. The transition scale is far outside currently-probed regimes (e.g., at the Schwinger field, $\sim 10^{18}$ V/m, only reached in heavy-ion collisions or near-horizon black holes).

The framework's structural prediction: if magnetic monopoles existed in our sector (a TetB-charge population), the EM partition would have a non-trivial $\mu_{\text{EM}}(x)$ analogous to gravity's. The absence of observed EM-MOND deviation is the empirical evidence that magnetic monopoles are absent or vanishingly rare in our universe.

**This is consistent with §6** and gives an independent line of reasoning for the same conclusion: empirical EM linearity ↔ empirical $\nabla \cdot B = 0$ ↔ TetB-magnetic sector empty in our regime.

---

## 12. Summary table — what the framework gives Maxwell

| Question | Framework answer |
|---|---|
| Where does $F^{\mu\nu}$ live algebraically? | $\Lambda^2 V$ at $K=4$ — the 6 edges of the tetrahedron $K_4$ |
| What is the $E$/$B$ split? | Time-space edges vs space-space edges of $K_4$ |
| What is the self-dual / anti-self-dual decomposition? | The three perfect matchings of $K_4$ |
| Where does gravity live? | $\mathrm{Sym}^2 V$ at $K=4$ — the 10 symmetric-tensor components |
| Why are EM and gravity related? | Both inhabit $V \otimes V$ at $K=4$; gravity is the 21-fold composition of EM via the three-sweep kernel |
| What is the EM coupling step? | $\alpha^1$ — the framework's primitive |
| What is the gauge-invariant content of Maxwell? | $\Phi_4(4) = 17$ — the parity-even reading of the closure-read |
| Where does TetB enter? | Magnetic-dual sector; ∇·B = 0 ↔ TetB-magnetic empty in our regime |
| Why no observed EM-MOND? | TetB-magnetic charge density vanishes; the EM partition is asymptotic |
| What is electric-magnetic duality? | The framework's TetA $\leftrightarrow$ TetB exchange symmetry restricted to $\Lambda^2 V$ |

---

## 13. Testable predictions

**P1. Cavity-mode locking at Niven angles.** A resonator with three-fold rotational symmetry (or other geometry imposing internal $\theta = \pi/3$ phase content) should show mode clustering at the $\Phi_3(4) = 21$ comb, not the standard rectangular spectrum. Specific signature: a 3 × 7 mode pattern.

**P2. Schwinger-regime magnetic structure.** If magnetic monopoles exist anywhere in our universe, the framework predicts they activate at field-strength scales near the Schwinger critical field $F_S$. Heavy-ion collision experiments at $F \approx F_S$ should look for deviations from $\nabla \cdot B = 0$.

**P3. Gauge-invariant degree-of-freedom count.** Maxwell's gauge-invariant content at $K=4$ should be 17 dimensions: 1 (scalar) + 6 ($F^{\mu\nu}$) + 9 (the gravitational sector's traceless symmetric, sometimes grouped with Maxwell in unified treatments) + 1 (volume form). Verify by detailed accounting of gauge-fixed Maxwell + linearized gravity coupled system.

**P4. Sierpinski-level composite couplings.** At the second Sierpinski level (scale-fusion $K=4 \to K=16$), the effective Coulomb-like coupling should be $\alpha^{21} \cdot \alpha^{13}$ = $\alpha^{273}$ for the composite gravitational interaction at the next scale. This is the framework's prediction for an iterated gravitational ladder.

---

## 14. Open derivations

1. **Derivation of $\alpha$ from the framework.** Currently $\alpha$ is the framework's primitive coupling, input from experiment. A derivation from a deeper structural principle would complete the picture.

2. **The detailed Bianchi identity in framework form.** The pure-even-sector closure of $\partial_{[\mu} F_{\nu\rho]} = 0$ should follow from the framework's parity structure. Working this out explicitly would tighten the parity-graded reading of §8.

3. **The EM constitutive law $\mu_{\text{EM}}(x)$.** Identifying the correct EM analog of $\mu(x) = x/(x+1)$, with explicit identification of the critical scale (Schwinger field, or otherwise), would extend the framework's gravity-partition structure to EM symmetrically.

4. **The Sierpinski-hierarchy connection to EM.** The Sierpinski packing currently lives in the nuclear-binding-energy work and the gravity-equation derivation. Its specific application to EM scale-dependent couplings is suggestive but not yet developed.

---

**Cross-references:**
- [02.1 Gravity equation](../02_gravity_derivation/02.1_gravity_equation.md) (the $\alpha^{21}$ derivation that establishes EM = $\alpha^1$ primitive)
- [03 Parity-character upgrade](03_parity_character_upgrade.md) (parity-character framing)
- [04 Core theory integration](04_core_theory_integration.md) (scale fusion, Niven rigidity)
- [05 Niven and μ-partition](05_niven_and_mu_partition.md) (the partition reading used in §11)
