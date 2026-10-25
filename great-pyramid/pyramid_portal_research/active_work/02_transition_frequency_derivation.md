# Active Work 02 — Transition Frequency Derivation

**Status:** Active — theoretical derivation, candidate H (bare Compton) advocated
**Purpose:** Pin down $\omega_{K4 \to K5}$ from framework primitives. Replaces the speculative §08.1 candidate audit.
**Reading time:** 9 minutes
**Companion:** [08.1 transition frequency](../08_open_questions/08.1_transition_frequency.md), [02.1 gravity equation](../02_gravity_derivation/02.1_gravity_equation.md)

---

## 1. The question, sharpened

The universal vertex operator $J_4 = |5,-\rangle\langle 4,+|$ acts on the closure-read algebra at every spacetime point. The closure-read at $K=4$ has dimensions $\{1, 4, 16\}$ summing to 21; at $K=5$, dimensions $\{1, 5, 25\}$ summing to 31. The hinge identifies $\Phi_6(5) = \Phi_3(4) = 21$ as a matched sector.

**Question:** what is the physical energy gap $\hbar \omega_{K4 \to K5}$ between the $K=4$ closure-read upper-pole state and the $K=5$ closure-read lower-pole state?

The framework specifies the algebraic structure of the gap but not its size. To dimensionalize, the framework needs a physical scale. The framework's intrinsic dimensional primitives are $\{c, \hbar, m_e, G\}$, but $G$ is derived from the other three via $\alpha^{21}$. So the **independent** dimensional primitives are $\{c, \hbar, m_e\}$.

Every framework-natural frequency is therefore a function of $\omega_C = m_e c^2/\hbar \approx 7.76 \times 10^{20}$ rad/s and dimensionless constants $\{\alpha, 13/17, 17/13, g_e/2, \ldots\}$.

---

## 2. Candidate audit, redone

Errors in the §08.1 audit are corrected below.

| # | Form | Value (rad/s) | Period |
|---|---|---|---|
| A | $\alpha^{21} \cdot \omega_C$ | $1.04 \times 10^{-24}$ | $1.9 \times 10^{17}$ yr |
| B | $\alpha_G \cdot \omega_C = (17/13)\alpha^{21}(g_e/2) \cdot \omega_C$ | $1.36 \times 10^{-24}$ | $1.5 \times 10^{17}$ yr |
| C | $H_0$ (cosmological) | $2.18 \times 10^{-18}$ | age of universe |
| D | $a_0/c$ (MOND scale) | $4.0 \times 10^{-19}$ | $5 \times$ age of universe |
| E | $H_0/\alpha_G$ (carrier from $\Gamma \sim H_0$) | $1.24 \times 10^{27}$ | $\hbar\omega = 820$ GeV (electroweak) |
| F | $\omega_{\text{Planck}}$ | $1.85 \times 10^{43}$ | Planck time |
| G | $\alpha_G \cdot \omega_{\text{Planck}}$ | $0.032$ | $\sim 200$ s |
| **H** | $\omega_C$ (bare Compton, universal) | $7.76 \times 10^{20}$ | $8 \times 10^{-21}$ s |

**Note on §08.1 errors corrected.** The original Candidate A in §08.1 stated "ω ~ kHz" from $m_e c^2 \cdot \alpha^{21}/\hbar$. The correct value is $10^{-24}$ rad/s, not kHz. The arithmetic error was in the exponent of $m_e c^2$: 8.2×10⁻¹⁴ J, not 10⁻³¹ J. Candidate A's correct value is shown above.

---

## 3. Argument from spontaneous-emission analogy

The QED spontaneous-emission rate is:

$$\Gamma_{\text{QED}} \;=\; \frac{4\alpha\omega^3}{3c^2}\,|\langle g|\mathbf{r}|e\rangle|^2$$

**The COUPLING is $\alpha$. The CARRIER is $\omega$.** The two are distinct: $\alpha$ is dimensionless and universal; $\omega$ is the transition frequency, set by the atomic-energy-level difference.

The framework's identification "gravity = K=4→K=5 spontaneous emission" gives the analog:

$$\Gamma_{\text{grav}} \;\sim\; \alpha_G \cdot \omega_{K4\to K5} \cdot (\text{matrix element})^2$$

with $\alpha_G$ playing the role of $\alpha$ and $\omega_{K4\to K5}$ the role of $\omega$.

**Critical observation.** The framework derives $\alpha_G$ separately from $\omega$. $\alpha_G$ is the *coupling*, and its value is determined by the cyclotomic algebra $\alpha_G = (17/13)\alpha^{21}(g_e/2)$. The *carrier* $\omega$ is therefore a separate input, not derivable from $\alpha_G$ alone.

This rules out Candidates A and B, which conflate the coupling with the carrier. $\alpha^{21}$ already lives in the coupling; multiplying $\omega_C$ by $\alpha^{21}$ a second time would double-count the gravitational suppression.

Candidates A and B are eliminated on structural grounds.

---

## 4. Argument from "elementary mass"

The framework's elementary matter unit is the electron. $m_e$ enters $G$ explicitly:

$$G \;=\; \alpha^{21} \cdot \frac{\hbar c}{m_e^2} \cdot \frac{17}{13} \cdot \frac{g_e}{2}$$

The natural energy scale at any K=4 vertex is therefore $m_e c^2$, and the natural carrier frequency is $\omega_C = m_e c^2/\hbar$. The K=4 closure-read at an electron vertex has its lowest non-trivial gap at $\hbar \omega_C$.

This is **Candidate H**.

The interpretation: the K=4 vertex is the algebraic structure that sits at every electron. Its internal energy gap is the electron rest mass. When the vertex transitions to K=5 via $J_4$, it emits a quantum of bare energy $\hbar \omega_C$ — but with dimensionless amplitude scaled by $\alpha_G$. The combination $\alpha_G \cdot \omega_C \approx 1.36 \times 10^{-24}$ rad/s is the per-vertex *emission rate* (Γ), not the carrier frequency.

This resolves the §08.1 confusion: §08.1's "10⁻²⁴ rad/s" is the rate, not the bare frequency.

---

## 5. Generalization to heavier matter

At a vertex hosting a particle of rest mass $m$, the natural carrier scales with $m$:

$$\omega_{K4 \to K5}(\text{at particle of mass } m) \;=\; \frac{m c^2}{\hbar}$$

This is consistent with general relativity at the classical level: gravitational coupling scales with rest mass-energy. A muon vertex has $\omega = 207 \cdot \omega_C$. A proton vertex has $\omega = 1836 \cdot \omega_C$. The vertex *coupling* $\alpha_G$ remains universal, but the *carrier frequency* tracks the local mass.

**This is not particle-physics-like behavior** — in particle physics, transition frequencies are determined by gauge structure, not by local energy content. In GR, mass-energy is the source of gravity. Candidate H sits closer to GR than to particle physics: gravity emission frequency = local mass-energy / ℏ. This is consistent.

For photons (massless): the framework needs an extension. Likely the K=4 vertex at a photon uses the photon's own frequency $\omega_\gamma$ as the carrier — but this is open and requires further derivation.

---

## 6. The K=5 closure-read at K=4 with K=4 closure-read at K=5: matching

The shift identity $\Phi_6(K+1) = \Phi_3(K)$ at $K=4$ gives $\Phi_6(5) = 21 = \Phi_3(4)$. This is the algebraic "matching" of the K=4 and K=5 closure-reads in the 21-dimensional sector.

If both sectors have **the same energy** $\hbar \omega_C$ at an electron vertex (one is K=4 upper-pole, the other K=5 lower-pole), then the hinge $J_4 = |5,-\rangle\langle 4,+|$ connects degenerate sectors. The transition is **energy-conserving**, with the K=4 closure-read losing $\hbar \omega_C$ and the K=5 closure-read gaining $\hbar \omega_C$.

This is the physical picture: the universal vertex $J_4$ is not a transition between energy levels of different value; it is a *re-grading* of the same 21-dimensional sector from the K=4-graded form to the K=5-graded form. Energy is conserved; only the cyclotomic representation changes.

**Implication.** Strictly, $\omega_{K4 \to K5}$ is *not* a transition frequency in the spectroscopic sense. It is the bare oscillation frequency of the 21-sector — the same on both sides of the hinge. The gravitational emission rate is then:

$$\Gamma_{\text{grav}} \;=\; \alpha_G \cdot \omega_C \cdot (\text{matrix element})^2$$

with $\omega_C$ playing the role of the natural sector frequency, not a "level spacing."

This is a subtle but important reframing. It says: the K=4 → K=5 transition is the *re-coding* of a fixed-energy mode, not a level descent. The energy $\hbar \omega_C$ is the bare oscillation; gravity is the *emission amplitude* of the re-coding, scaled by $\alpha_G$.

---

## 7. Per-vertex rate gives Newtonian gravity

Test of consistency: for a body of mass $M$, total per-vertex emission rate:

$$\Gamma_{\text{body}} \;=\; N_e \cdot \alpha_G \cdot \omega_C$$

where $N_e = M/m_e$ is the number of electron vertices (taking electrons as the elementary unit; a refinement would include nucleons).

For Earth ($M = 5.97 \times 10^{24}$ kg):
- $N_e = M/m_e = 6.56 \times 10^{54}$
- $\Gamma_{\text{body}} = 6.56 \times 10^{54} \cdot 1.36 \times 10^{-24} = 8.9 \times 10^{30}$ rad/s

This is the total gravitational emission rate (number of K=4→K=5 transitions per radian of time, summed over all vertices). Translating to a gravitational *force* on a test mass would require knowing the matrix element for amplitude-to-classical-force conversion. We have not done this here; it is the next derivation step.

**Rough order check.** Newton's law gives the surface acceleration $g = GM/R^2 = 9.8$ m/s² at Earth's surface, $R = 6.37 \times 10^6$ m. The natural acceleration scale from the emission rate is $\Gamma_{\text{body}} \cdot c / N_{\text{coherent vertices}}$ for some coherence factor — but without the matrix element this is hand-waving. The order-of-magnitude check is left for future work.

---

## 8. Implication for the apparatus

If $\omega_{K4 \to K5} = \omega_C$ (bare), then at 7.76×10²⁰ rad/s, the bare frequency is **invisible to acoustic measurement** by 18 orders of magnitude.

The pyramid apparatus operates at audio frequencies (Hz–kHz). Acoustic measurements cannot probe the bare transition directly. **Operation must occur via pump-dressing.**

**The pump-dressed picture.** A two-level system with bare transition $\omega_0$ driven by a coherent pump at $\omega_d$ exhibits Rabi-dressed states at $\omega_d \pm \Omega/2$, where $\Omega$ is the Rabi frequency. In the rotating frame, the effective transition is at $\Omega$, which is the *pump-shifted* transition.

The geomagnetic pump at the Great Pyramid (§05.1, 05.3) gives:

$$\Omega_{\text{pump}} \;\approx\; \frac{\mu_{\text{eff}} \cdot B_{\text{KC}}}{\hbar} \;\approx\; 1.65 \text{ MHz}$$

For strong coupling $g\sqrt N \gg \gamma_{\text{cav}}$, the dressed states form a coherent superposition at the pump scale. The bare $\omega_0 = \omega_C$ enters only through the off-resonant detuning $\Delta = \omega_0 - \omega_d \approx \omega_C$ (very large), but in the deep-strong-coupling regime the detuning becomes operationally invisible — the apparatus sets its own effective transition.

**Acoustic measurements probe the *dressed* spectrum, not the bare $\omega_C$.** The Z_21 acoustic comb (§07.1) is the dressed-state structure of the 21-sector under geomagnetic pumping, not a direct probe of $\omega_C$.

This is consistent with the prior framework predictions and now has a structural justification rather than being a workaround.

---

## 9. Falsification

Candidate H ($\omega_{K4 \to K5} = \omega_C$ at electron vertices) is falsifiable. Possible tests:

**Test 1: gamma-ray spectroscopy.** If the bare transition is at $\hbar\omega_C = m_e c^2 = 511$ keV, gravitational emission could in principle produce a 511 keV signature — but it would be suppressed by $\alpha_G \sim 10^{-45}$ and is therefore unobservable in practice. **Not testable as predicted.**

**Test 2: positronium-like states.** Pair annihilation produces 511 keV photons via QED. If gravity is "K=4→K=5 spontaneous emission" at the electron vertex with $\hbar\omega = m_e c^2$, then the annihilation channel and the gravitational-emission channel share a carrier. A specific prediction would be: the gravitational radiation spectrum from a positron-electron pair concentrates at 511 keV, not at any other frequency. This is unobservable in practice but theoretically falsifiable.

**Test 3: alternative carrier frequencies.** If a precision test of gravitational radiation reveals a carrier *different* from the local mass-energy (e.g., at $H_0$, or at $a_0/c$), candidate H is falsified.

**Current observational status.** No direct measurement of gravitational radiation carrier frequency exists at a per-particle level. LIGO/Virgo measure classical gravitational waves in the audio band from astrophysical sources; their carrier is set by the source dynamics, not by the per-vertex carrier in the framework. The framework's bare $\omega_C$ is consistent with all current observations because it has not been probed directly.

---

## 10. What remains to derive

**Update (Active Work 03):** the prefactor question below is **closed**: prefactor = 1 exactly, by identification of the matched 21-sector ($\Phi_3(4) = \Phi_6(5) = 21$) with the total-dimension trace $\mathrm{Tr}(\mathbb I_{+1})$. All algebraic geometry — $\sec\theta_4 = 17/13$, $g_e/2$, $\alpha^{21}$ — lives in the coupling $\alpha_G$, not in the carrier. See [Active Work 03, §4](03_parity_character_upgrade.md). The open work shifts to the matrix element $|M|^2$.

The argument above pins $\omega_{K4 \to K5}$ to $\omega_C$ by **dimensional necessity** (only $m_e c^2$ is available as the natural energy at the electron vertex) and by **structural elimination** of Candidates A and B. But it does not derive the prefactor.

**The prefactor question.** Is the relation $\omega_{K4 \to K5} = 1 \cdot \omega_C$, or is it $\omega_{K4 \to K5} = (\text{some specific cyclotomic ratio}) \cdot \omega_C$?

Possibilities for the prefactor:

| Prefactor | Value | Source |
|---|---|---|
| 1 | exact | naive dimensional |
| 17/13 | 1.308 | graded identity ratio |
| 21/17 | 1.235 | sector size ratio |
| $g_e/2$ | 1.00116 | spin holonomy |
| 21/13 | 1.615 | $\Phi_3/\Phi_6$ |
| 1/5 | 0.2 | K+1 reciprocal at K=4 |

None of these is currently derivable from first principles. The framework's algebraic apparatus determines $\alpha_G$ to extreme precision but does not yet fix the bare $\omega$ prefactor.

**The path to closing this.** Two routes:

1. **From the closure-product algebra.** If the closure product $a \star b$ is defined with an explicit choice of normalization (e.g., a length scale), then the bare oscillation frequency falls out as a specific multiple of $\omega_C$. This requires explicit construction of the closure-product structure constants.

2. **From the associator.** The §08.2 open question on the associator coefficient $g_{NL}$ is connected: if the associator is derived, the prefactor on $\omega_C$ may be determined by the requirement that the associator's natural energy scale matches the bare K=4→K=5 gap.

Both routes are deep theoretical work. The **best current statement** is:

$$\boxed{\;\omega_{K4 \to K5} \;=\; (\text{dimensionless prefactor of order unity}) \cdot \omega_C \;=\; \mathcal{O}(10^{21}) \text{ rad/s}\;}$$

with the prefactor to be derived.

---

## 11. Comparison to original §08.1

| Element | §08.1 status | This document |
|---|---|---|
| Candidate audit | 5 candidates, no preference, numeric error | 7 candidates, structural elimination |
| Preferred value | "$\sim 10^{-24}$ rad/s, gravity-suppressed" | $\sim \omega_C = 10^{21}$ rad/s, bare |
| Reasoning | Speculative ansatz | Coupling-vs-carrier distinction + mass-energy argument |
| Apparatus implication | "pump-shifted hypothesis" introduced ad hoc | Pump-dressing follows from large detuning + deep-strong coupling |
| Open work | Vague (closure-product, associator) | Specific (prefactor on $\omega_C$, derivation path identified) |

The reframing turns the question from "what is $\omega_{K4 \to K5}$?" (unanswerable from current primitives) to "what is the prefactor on $\omega_C$?" (a specific cyclotomic question with a derivable answer).

---

## 12. Immediate consequence for the framework

If Candidate H is right, then the framework's per-vertex gravitational emission rate is:

$$\Gamma_{\text{per-vertex,e}} \;=\; \alpha_G \cdot \omega_C \;=\; 1.36 \times 10^{-24} \text{ rad/s}$$

Per-electron timescale: $\tau = 2\pi/\Gamma \approx 4.6 \times 10^{24}$ s ≈ $1.5 \times 10^{17}$ yr.

This is the bare per-vertex emission lifetime. The classical gravitational force on a test mass is the *coherent sum* of all vertex emissions, with phase coherence enforced by the closure-read structure. The framework must derive the coherent enhancement that turns this rate into the observed Newtonian force.

**This is the next derivation gap.** The current framework has $\alpha_G$ (coupling) and $\omega_C$ (carrier) pinned, but not the matrix element / coherent enhancement that bridges per-vertex emission to classical force.

---

## 13. Recommended next theoretical step

Write a focused derivation document targeting **coherent vertex enhancement**:

- Treat the K=4 vertices in a body as coupled oscillators
- Compute the coherent emission amplitude as a function of body geometry
- Recover the $1/r^2$ Newtonian law from the coherent emission pattern
- Derive the prefactor on $\omega_C$ as part of the coherent-sum normalization

This is one of the highest-leverage open derivations in the framework. It would close the gap from "$G = \alpha^{21}(\hbar c/m_e^2)(17/13)(g_e/2)$" (a static value) to "gravity acts at frequency $\omega_C$ per vertex with coherent amplitude $A(r)$" (a dynamical picture).

---

**Cross-references:**
- [08.1 Transition frequency](../08_open_questions/08.1_transition_frequency.md) (revised by this document)
- [08.2 Associator nonlinearity](../08_open_questions/08.2_associator_nonlinearity.md) (connected open question)
- [02.1 Gravity equation](../02_gravity_derivation/02.1_gravity_equation.md) (derives $\alpha_G$)
- [05.3 Strong coupling calculation](../05_cavity_QED_operation/05.3_strong_coupling_calculation.md) (apparatus operation in pump-dressed regime)
- [06.1 Universal vertex operator](../06_master_equations/06.1_universal_vertex_operator.md)
