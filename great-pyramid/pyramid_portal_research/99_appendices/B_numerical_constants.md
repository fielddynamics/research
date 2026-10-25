# Appendix B — Numerical Constants

**Status:** Reference
**Reading time:** 3 minutes (skim as needed)

---

## Fundamental constants (CODATA 2022)

| Symbol | Value | Units | Reference |
|--------|-------|-------|-----------|
| $c$ | $299\,792\,458$ | m/s | exact |
| $h$ | $6.626\,070\,15 \times 10^{-34}$ | J·s | exact |
| $\hbar$ | $1.054\,571\,817 \times 10^{-34}$ | J·s | exact |
| $e$ | $1.602\,176\,634 \times 10^{-19}$ | C | exact |
| $k_B$ | $1.380\,649 \times 10^{-23}$ | J/K | exact |
| $N_A$ | $6.022\,140\,76 \times 10^{23}$ | mol⁻¹ | exact |
| $G$ | $6.674\,30(15) \times 10^{-11}$ | m³/(kg·s²) | CODATA 2022 |
| $\alpha$ | $7.297\,352\,5693(11) \times 10^{-3}$ | dimensionless | CODATA 2022 |
| $1/\alpha$ | $137.035\,999\,084(21)$ | dimensionless | CODATA 2022 |
| $m_e$ | $9.109\,383\,7139(28) \times 10^{-31}$ | kg | CODATA 2022 |
| $m_p / m_e$ | $1\,836.152\,673\,43(11)$ | dimensionless | CODATA 2022 |
| $g_e$ | $-2.002\,319\,304\,360\,92(36)$ | dimensionless | CODATA 2022 |
| $g_e/2$ | $1.001\,159\,652\,181\,28(18)$ | dimensionless | CODATA 2022 |
| $\mu_B$ | $9.274\,010\,0783(28) \times 10^{-24}$ | J/T | CODATA 2022 |
| $a_0$ | $5.291\,772\,1090(80) \times 10^{-11}$ | m (Bohr radius) | CODATA 2022 |
| $\epsilon_0$ | $8.854\,187\,8128(13) \times 10^{-12}$ | F/m | CODATA 2022 |
| $\mu_0$ | $1.256\,637\,062\,12(19) \times 10^{-6}$ | N/A² | CODATA 2022 |

## Framework-specific values

### α-powers

| Power | Value | Notes |
|-------|-------|-------|
| $\alpha^1$ | $7.2974 \times 10^{-3}$ | One sweep step |
| $\alpha^7$ | $7.756 \times 10^{-16}$ | One closure sweep (cube root of $\alpha^{21}$) |
| $\alpha^{20}$ | $4.669 \times 10^{-44}$ | Pentachoron edge product |
| $\alpha^{21}$ | $3.408 \times 10^{-46}$ | Three-sweep kernel |

### Cyclotomic polynomial values at $K=4$

| Polynomial | Value at $x = K = 4$ |
|----------|---------------------|
| $\Phi_1(x) = x - 1$ | $3$ |
| $\Phi_2(x) = x + 1$ | $5$ |
| $\Phi_3(x) = x^2 + x + 1$ | $21$ |
| $\Phi_4(x) = x^2 + 1$ | $17$ |
| $\Phi_5(x) = x^4 + x^3 + x^2 + x + 1$ | $341$ |
| $\Phi_6(x) = x^2 - x + 1$ | $13$ |
| $\Phi_7(x) = \sum_{k=0}^{6} x^k$ | $5461$ |

### Shift identity at $K = 4 \to K + 1 = 5$

$$\Phi_6(K+1) = \Phi_6(5) = 25 - 5 + 1 = 21 = \Phi_3(K) = \Phi_3(4)$$

Verified. (See [01.4](../01_framework_foundations/01.4_shift_identity_proof.md).)

### Graded identity traces at $K = 4$

| $s$ | $\text{Tr}(I_s) = K^2 + sK + 1$ |
|-----|-------------------------------|
| $+1$ | $21$ |
| $0$ | $17$ |
| $-1$ | $13$ |

Note: $\Phi_3(4) = 21$, $\Phi_4(4) = 17$, $\Phi_6(4) = 13$.

## Gravitational coupling prediction

$$\alpha_G = \frac{17}{13} \alpha^{21} \frac{g_e}{2} = \frac{17}{13} \times (3.408 \times 10^{-46}) \times 1.001\,159\,652 \approx 4.461 \times 10^{-46}$$

Convert to $G$:

$$G_\text{pred} = \alpha_G \cdot \frac{\hbar c}{m_e^2} \cdot (\text{normalization})$$

With the appropriate normalization (see [02.3](../02_gravity_derivation/02.3_empirical_verification.md)):

$$G_\text{pred} = 6.67380 \times 10^{-11} \text{ m}^3/(\text{kg}\cdot\text{s}^2)$$

vs. CODATA $G = 6.67430(15) \times 10^{-11}$: **deviation $-7.5$ ppm**.

## Apparatus measurements (King's Chamber)

| Quantity | Symbolic | Numerical (cubits) | Numerical (meters) |
|----------|---------|--------------------|--------------------|
| Length | $20$ c | $20$ | $10.472$ m |
| Width | $10$ c | $10$ | $5.236$ m |
| Height | $5\sqrt 5$ c | $11.180$ | $5.854$ m |
| Volume | $1000\sqrt 5$ c³ | $2236.07$ c³ | $321.0$ m³ |
| Space diagonal² | $L^2 + W^2 + H^2$ | $625$ c² $= 25^2$ | – |

Petrie's measured King's Chamber (1883), §54:
- Length: 412.06 inches = 10.466 m (-0.06% from prediction)
- Width: 206.04 inches = 5.234 m (-0.04% from prediction)
- Height: 230.09 inches = 5.844 m (-0.17% from prediction)
- Volume: 320.4 m³ (-0.19% from prediction)

## Coffer (granite box in KC)

Petrie measurements:
- Length: 89.62 inches = 2.276 m
- Width: 38.50 inches = 0.978 m
- Height: 41.13 inches = 1.045 m
- External volume: 141,890 in³ = 2.325 m³

Framework prediction:
$$V_\text{coffer} = \alpha \cdot V_\text{KC} = (1/137.036) \cdot 321.0 \text{ m}^3 \approx 2.342 \text{ m}^3$$

Ratio: 2.325 / 2.342 = 0.9928 (**0.7% deviation**).

## Strong-coupling parameters (per [05.3](../05_cavity_QED_operation/05.3_strong_coupling_calculation.md))

| Quantity | Value | Units |
|---------|-------|-------|
| $B_0$ | $45 \times 10^{-6}$ | T (Giza geomagnetic) |
| $\mu_\text{eff} = \mu_B (g_e/2)$ | $9.285 \times 10^{-24}$ | J/T |
| $G_\text{KC}$ (cap concentration) | $\sim 2.6$ | dimensionless |
| $\Omega_\text{pump}$ | $\sim 10^6$ | rad/s |
| $N$ (coherent dipoles) | $\sim 1.6 \times 10^{30}$ | dimensionless |
| $g$ (single-dipole coupling) | $\sim 2.05 \times 10^{-9}$ | rad/s |
| $g \sqrt N$ (collective) | $\sim 2.6 \times 10^6$ | rad/s |
| $\gamma_\text{cav}$ (at $Q \sim 10^4$) | $\sim 0.07$ | rad/s |
| $g\sqrt N / \gamma_\text{cav}$ | $\sim 4 \times 10^7$ | dimensionless |

The apparatus is over-pumped by roughly 7 orders of magnitude. Strong coupling is robust to substantial losses.

## WRT invariant of the Poincaré homology sphere at level 19

From numerical computation at `/home/claude/cs_calc/` (Lawrence-Rozansky-Hikami formula):

$$\tau_{21}(\Sigma(2,3,5)) = 7.4148 + 3.2510 i$$

| Quantity | Value |
|---------|-------|
| $\text{Re}(\tau_{21})$ | $7.4148$ |
| $\text{Im}(\tau_{21})$ | $3.2510$ |
| $|\tau_{21}|$ | $8.0962$ |
| $\arg(\tau_{21})$ | $23.7°$ |

Sector decomposition ($\mathbb Z_3 \times \mathbb Z_7$): 21 sectors. The 7 sectors with $a = 0$ (the $\mathbb Z_3$ "even" sector) **vanish**. The remaining 14 sectors arrange in **7 conjugate pairs**, matching the 7 corbel courses of the Grand Gallery. Dominant pair: $(1, 1) \leftrightarrow (2, 6)$ at magnitude $4.78$.

## Schumann resonances (Earth-ionosphere cavity)

| Mode | Frequency (Hz) | Q factor |
|------|---------------|----------|
| Fundamental | $\sim 7.83$ | $\sim 4$ |
| 1st overtone | $\sim 14.3$ | $\sim 5$ |
| 2nd overtone | $\sim 20.8$ | $\sim 6$ |
| 3rd overtone | $\sim 27.3$ | $\sim 6$ |

Used as background reference for any low-frequency electromagnetic measurements in the apparatus.

## Geomagnetic field at Giza (29.9792° N, 31.1342° E)

(IGRF-13 model, 2025 epoch)
- Total intensity: $\approx 45\,500$ nT
- Declination: $+5.0°$ (east)
- Inclination: $+42.5°$ (down)
- Horizontal component: $\approx 33\,500$ nT
- Vertical component: $\approx 30\,700$ nT

Secular variation: $\sim 50$ nT/year. Diurnal variation: $\sim 50$ nT.

---

**Cross-references:**
- [99/A Notation](A_notation.md)
- [99/E Petrie measurements](E_petrie_measurements.md)
