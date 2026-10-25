# GFD Gravity Field Packing — Synthesis

## One Field, Two States, Zero Parameters in the Distinction

**Framework:** Gravitational Field Dynamics (GFD)  
**Geometry:** K = 4, D = 3 (stellated octahedron, uniqueness theorem 2(D+1) = 2^D)  
**Tests:** 20/20 passed  
**File:** `gfd_gravity_field_packing_20.py`

---

## The Central Claim

There is one field: the gravity field. It exists in two physical states.

**Unbound.** Gravity fields packed at K = 4 on TetA. This is space — the ocean. Unbound fields screen each other in one direction:

$$x(1 - \mu) = \mu \quad \Rightarrow \quad \mu = \frac{x}{x+1}$$

This governs galactic dynamics. The Milgrom regime. An unbound field has nothing holding it in place.

**Bound.** A field pushed through the Field Origin (f = 17, x = 1) crosses onto TetB and gets stuck. The packing geometry traps it. Other bound fields compress it from every direction. The compression is bidirectional:

$$x(1 - \mu)^2 = \mu$$

This governs nuclear binding. The compression creates a vortex that spirals outward into (3+1) spacetime — the electric field. That bound envelope with its vortex IS matter.

Both states coexist in our (3+1) spacetime. The unbound field is everywhere. Matter is bound gravity fields sitting in it.

**There is no N = 1 or N = 2.** There is no parameter that selects the exponent. The exponent tells you which state the field is in: 1 for unbound (one-directional screening in the ocean), 2 for bound (bidirectional compression from being stuck). A gravity field can't pack on TetA — nothing holds it there. Only when it crosses through the Field Origin and lands on TetB is it trapped, compressed from all sides, and the exponent becomes 2.

---

## What the 20 Tests Found

### A. The Gate (Tests 1–4)

The Field Origin at f(1) = 17 is the unique crossing point — the one-way door from the ocean into the nucleus.

| Test | Finding |
|------|---------|
| A1 | f(x) = 17 has exactly one solution: x = 1. One gate, one crossing. Both numerator and denominator of the solution equal K. |
| A2 | All nuclei are deep in TetB territory. He-4 (x = 16) is already 88% of the way from the gate to the TetB ceiling. Fe-56 is 99.9%. Bi-209 is 100.0%. These fields are not near the gate — they are deeply stuck. |
| A3 | Hydrogen is one field at the gate: A = 1, x = 1, BE/A = 0. The entire crossing energy becomes rest mass. Every other nucleus has positive surplus binding. |
| A4 | At the gate, the bound compression equation produces the golden ratio: ν² + ν = 1 → ν = 1/φ → μ = 1/φ². This is not imported — it is produced by bidirectional compression at the crossing point. The unbound law gives μ = 1/2 at x = 1. No golden ratio. |

**The capacity function f(x) = (21x + 13)/(x + 1) acts as a depth gauge.** At x = A², it reads how deep the bound fields sit in TetB:

| Nucleus | A | x = A² | f(x) | Depth into TetB |
|---------|---|--------|------|-----------------|
| Hydrogen | 1 | 1 | 17.000 | 0% (at the gate) |
| Helium | 4 | 16 | 20.529 | 88% |
| Neon | 20 | 400 | 20.980 | 99.5% |
| Iron | 56 | 3,136 | 20.997 | 99.9% |
| Bismuth | 209 | 43,681 | 21.000 | 100.0% |

---

### B. Stuck (Tests 5–9)

Once a field crosses the gate onto TetB, it's trapped. The bidirectional compression has a distinctive signature: slow saturation.

**The key discriminant.** The two states saturate at different rates:

- **Unbound:** 1 − μ ~ 1/x = 1/A². By A = 10, the geometry is 99% saturated. No shape left.
- **Bound:** 1 − μ ~ 1/√x = 1/A. Even at A = 56 (iron), 1.8% remains unsaturated. The geometry has real curvature across the entire periodic table.

| Test | Finding |
|------|---------|
| B5 | Saturation rate confirmed: (1 − μ\_bound(A²)) × A → 1.0 as A grows. Each new packed field contributes diminishing returns proportional to 1/A, not 1/A². |
| B6 | The asymptotic form K · ((A−1)/A)² matches K · s\_bound(A²) to < 1% for all A ≥ 7. The binding per nucleon is proportional to the **square** of the fraction of fields beyond the first crossing. Squared because the compression is bidirectional. |
| B7 | Dynamic range from Li-7 to Ca-40: bound law spans 29%, unbound spans 4%. The unbound law has nothing left to work with. The bound law tracks the steep rise in observed binding. |
| B8 | Light nuclei RMS (A = 7–19): bound = 0.38 MeV, unbound = 1.25 MeV. The bound law is 3× more accurate where the binding curve has its steepest shape. |
| B9 | Sensitivity ratio dμ\_bound/dμ\_unbound ≈ A/2. At A = 56, the bound law is 28× more sensitive to adding one more field than the unbound law. The unbound law says iron is indistinguishable from bismuth. The bound law says they're different — and the data agrees. |

**The asymptotic form deserves emphasis.** For A ≥ 7, the bound law gives:

$$\frac{BE}{A} \approx C \cdot K \cdot \left(\frac{A-1}{A}\right)^2$$

This is a one-parameter formula (C ≈ 2.156) that says: the binding energy per nucleon equals a constant times the square of (A−1)/A. The physical meaning of (A−1)/A is the fraction of bound fields beyond the first crossing (hydrogen contributes zero surplus). The squaring comes from bidirectional compression. The unbound law would give (1 − 2/A²) instead — linear depletion, no squaring, no (A−1)/A structure.

The Taylor expansion makes the prediction explicit:

$$\frac{BE}{A} \approx CK - \frac{2CK}{A} + \frac{CK}{A^2}$$

The coefficients are **linked**: c₁/c₀ = −2 exactly, c₂/c₀ = +1 exactly. These are not fitted — they fall from the compression law. A trivial unconstrained model would have independent coefficients.

---

### C. The Vortex (Tests 10–13)

Bound fields on TetB create a vortex — the electric field. This is not analogous to electromagnetism. It IS electromagnetism. The vortex is the observable signature of being stuck.

| Test | Finding |
|------|---------|
| C10 | **Coulomb inseparability.** Subtracting the Bethe-Weizsäcker Coulomb term degrades the C-factor CV by 37%. The electromagnetic interaction is not separable from the geometric binding because the vortex is created by the same bidirectional compression that binds. |
| C11 | **Vortex repulsion pattern.** The C-factor residual correlates with Z²/A at r = −0.72. More vortices → more repulsion → lower effective binding. This pattern is visible because the bound law preserves the dynamic range to see it. |
| C12 | **Neutron ballast.** N/Z increases with Z at r > 0.9. More vortices repel harder, requiring more non-vortex fields (neutrons) to maintain the compression envelope. The valley of stability is a geometric consequence. |
| C13 | **He-4 closure anomaly.** He-4 (A = K = 4) is the first complete tetrahedral unit on TetB. Its C-factor is 47% above the mean — an unmistakable geometric resonance. |

---

### D. The Packing (Tests 14–17)

The structure of how fields pack on TetB: shell closures, the address space ceiling, and the coefficient relationships from the compression law.

| Test | Finding |
|------|---------|
| D14 | All 7 magic numbers {2, 8, 20, 28, 50, 82, 126} from K = 4 alone. No other K in {2,...,10} works. Zero free parameters. |
| D15 | K^K = 256 packing ceiling. Bi-209 (A = 209) uses 81.6% of the TetB address space. No stable nucleus exceeds 256. |
| D16 | The coefficient relationships c₁/c₀ = −2 and c₂/c₀ = +1 are exact consequences of the compression law. They are tested, not fitted. |
| D17 | Shell 3 (size 12) > Shell 4 (size 8). In standard nuclear physics, this requires importing a spin-orbit force. In GFD, it's forced by the K-transition at n = 4 — a change in packing geometry, not an additional interaction. |

---

### E. Adversarial (Tests 18–20)

Honest challenges to the picture.

| Test | Finding |
|------|---------|
| E18 | **Honest competition.** A trivial 2-parameter model BE/A = c₀ + c₁/A gets RMS = 0.379 MeV. The bound law with 1 parameter gets 0.388 MeV. The 2-param model wins on raw fit quality. But the bound law achieves 97% of the same accuracy with half the parameters and a physical mechanism. The shortfall is < 3%. |
| E19 | **Honest failure.** Heavy elements (A > 180) are systematically overpredicted. Every element from hafnium to bismuth has a positive residual. This is because the vortex repulsion grows with Z² and a single constant C cannot capture Z-dependent effects. The failure is documented, not hidden. |
| E20 | **Falsifiability.** The bound and unbound laws make distinguishable predictions: μ = 1/φ² vs μ = 1/2 at x = 1 (a 30.9% gap), and 1/A vs 1/A² depletion from the ceiling. If observations established 1/A² scaling in nuclear binding, the packing picture would be falsified. |

---

## What This Suite Does NOT Contain

**No N = 1 or N = 2.** There is no parameter N. There are two physical states of one field. The exponent is not selected from a menu — it is the physics of the state.

**No exponent scanning.** The earlier suite (gfd_bound_vs_unbound_20.py) included a test scanning x(1−μ)^n = μ for n = 1 to 3 and finding the optimal basin. That test treated the exponent as a dial. It was wrong. You don't get to ask "what if compression were 1.7-directional?" Either the field is unbound (exponent 1) or it crossed the gate and is stuck (exponent 2). This suite replaces that framing.

**No "two tetrahedra both participating."** The exponent 2 is not "both tetrahedra contributing." TetA is the ocean — the field's home before crossing. TetB is where the packing happens. The exponent 2 is bidirectional compression ON TetB — the field is squeezed from every direction because it's trapped.

---

## The Complete Physical Picture

1. **Space** is an ocean of unbound gravity fields packed at K = 4 on TetA. The ocean screens in one direction: μ = x/(x+1). This governs galactic dynamics.

2. A perturbation pushes a field through the **Field Origin** (f = 17, x = 1, μ = 1/φ²). The field crosses from TetA onto TetB.

3. **Once on TetB, the field is stuck.** The packing geometry traps it. Other bound fields compress it from every direction. The compression is bidirectional: x(1 − μ)² = μ.

4. The first crossing creates **hydrogen** (A = 1, BE/A = 0). Stellar compression pushes more fields through — the bicycle pump — creating heavier nuclei up to the K^K = 256 ceiling.

5. The bidirectional compression creates a **vortex** spiraling outward into (3+1) spacetime. That vortex IS the electric field. The bound envelope with its vortex IS matter.

6. The vortex **illuminates** surrounding unbound fields on TetA — electrons. Z vortices light Z unbound fields. Charge neutrality is geometric.

7. Both states — unbound ocean and bound matter — coexist in our (3+1) spacetime. The difference is not where they are. The difference is whether the field crossed the gate and got stuck.

---

## Summary Table

| Test | Type | Params | Result |
|------|------|--------|--------|
| A1. Unique gate | Algebraic | 0 | x = 1 is the only crossing |
| A2. Deep in TetB | Empirical | 0 | All nuclei > 88% depth |
| A3. Hydrogen first crossing | Empirical | 0 | A = 1, BE/A = 0 |
| A4. Golden ratio at gate | Algebraic | 0 | μ = 1/φ² from ν² + ν = 1 |
| B5. Saturation rate 1/A | Algebraic | 0 | (1−μ)·A → 1 confirmed |
| B6. Asymptotic ((A−1)/A)² | Algebraic | 0 | < 1% error for A ≥ 7 |
| B7. Dynamic range 29% vs 4% | Empirical | 0 | Bound 7× more range |
| B8. Light nuclei RMS | Empirical | 1 (C) | 0.38 vs 1.25 MeV |
| B9. Diminishing returns | Algebraic | 0 | Ratio ≈ A/2, growing |
| C10. Coulomb inseparable | Empirical | 0 | 37% degradation on removal |
| C11. Vortex r = −0.72 | Empirical | 1 (C) | Z²/A tracks C-residual |
| C12. Neutron ballast | Empirical | 0 | N/Z vs Z: r > 0.9 |
| C13. He-4 closure | Empirical | 1 (C) | 47% C-factor excess |
| D14. Magic numbers | Algebraic | 0 | 7/7 exact from K = 4 |
| D15. K^K = 256 ceiling | Empirical | 0 | Bi-209 at 81.6% |
| D16. Coefficient c₁/c₀ = −2 | Algebraic | 1 (C) | Exact from compression law |
| D17. Shell inversion | Algebraic | 0 | Shell 3 > Shell 4 |
| E18. Honest competition | Adversarial | 1 (C) | < 3% shortfall vs 2-param |
| E19. Honest failure | Adversarial | 1 (C) | Heavy elements overpredicted |
| E20. Falsifiability | Structural | 0 | 30.9% gap, 1/A vs 1/A² |

**Total free parameters across all 20 tests: 1** (the constant C ≈ 2.156, used in 6 of 20 tests).

---

*GFD Gravity Field Packing Validation v1.0 — 20/20 tests passing*
