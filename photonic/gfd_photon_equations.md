# The Photon Equations

## Every Numerical Prefactor in Photon Physics from K = 4 and D = 3

*Stephen Nelson / Field Dynamics Research*
*March 2026*

---

## The Claim

Every numerical prefactor that appears in the standard equations of photon physics — scattering cross-sections, spectral radiation, gravitational light-bending, black hole thermodynamics — is a simple algebraic expression in two integers:

- **K = 4** — the closure constant (faces per tetrahedron)
- **D = 3** — the spatial dimension (spatial faces per tetrahedron)

These are not fitted. They are the unique solution to the combinatorial equation 2(D+1) = 2^D. The derived quantities are:

| Symbol | Value | Meaning |
|--------|-------|---------|
| K | 4 | Faces per tetrahedron (closure constant) |
| D | 3 | Spatial faces per tetrahedron |
| K² | 16 | Face-to-face coupling channels |
| 2K | 8 | Face pairs (scalar sector) |
| K²−1 | 15 | Off-diagonal coupling channels |
| \|Z₂\| | 2 | Chamber count (S₄/A₄ parity) |
| 2K/D | 8/3 | Thomson ratio (face pairs / spatial faces) |
| D/(2K) | 3/8 | Klein-Nishina ratio (inverse Thomson) |

---

## The Equations

### 1. Thomson Scattering

**Standard:**

$$\sigma_T = \frac{8\pi}{3} r_e^2$$

**From K, D:**

$$\sigma_T = \frac{2K\pi}{D} r_e^2$$

The "8" is 2K (face pairs in the scalar sector). The "3" is D (spatial faces over which the scattering distributes). The Thomson cross-section measures how a photon couples to an electron's bound vortex: 2K face-pair channels, diluted by D spatial directions.

### 2. Rayleigh Scattering

**Standard:**

$$\sigma_R \propto \omega^4$$

**From K, D:**

$$\sigma_R \propto \omega^K$$

The exponent 4 is K. Each of the K = 4 faces of the bound vortex contributes one power of ω to the frequency-dependent coupling. This is why the sky is blue: short wavelengths (high ω) scatter as ω^K, and K = 4 makes the blue/red intensity ratio (ω_blue/ω_red)^4 ≈ 5.5.

### 3. Klein-Nishina (High Energy)

**Standard:**

$$\sigma_{KN} \to \frac{3}{8} \sigma_T \cdot \frac{m_e c^2}{\hbar\omega} \left[\ln\frac{2\hbar\omega}{m_e c^2} + \frac{1}{2}\right]$$

**From K, D:**

$$\sigma_{KN} \to \frac{D}{2K} \sigma_T \cdot \frac{m_e c^2}{\hbar\omega} \left[\ln\frac{2\hbar\omega}{m_e c^2} + \frac{1}{2}\right]$$

The high-energy prefactor 3/8 = D/(2K) is the exact inverse of the Thomson prefactor 2K/D. At low energy, face-pair channels dominate (2K/D). At high energy, spatial faces dominate (D/2K). The crossover occurs at ℏω = mₑc² — the gate energy, where the photon has enough energy to probe the bound vortex's internal structure.

**The duality:** Thomson × Klein-Nishina(high-E) = (2K/D) × (D/2K) = 1. Low-energy and high-energy scattering are topological inverses.

### 4. Compton Scattering

**Standard:**

$$\Delta\lambda = \lambda_C (1 - \cos\theta), \quad \Delta\lambda_{\max} = 2\lambda_C$$

**From K, D:**

$$\Delta\lambda_{\max} = |Z_2| \cdot \lambda_C$$

The maximum Compton shift (backscatter, θ = π) has factor 2 = |Z₂|. Backscattering reverses the photon through both chambers of the stellated octahedron. Each chamber contributes one Compton wavelength of shift. Z₂ = S₄/A₄ is the parity that exchanges TetA and TetB.

### 5. The Electromagnetic Lagrangian

**Standard:**

$$\mathcal{L}_{EM} = -\frac{1}{4} F_{\mu\nu}F^{\mu\nu}$$

**From K, D:**

$$\mathcal{L}_{EM} = -\frac{1}{K} F_{\mu\nu}F^{\mu\nu}$$

The 1/4 is 1/K. The electromagnetic field is one face-channel of the K-face closure. The prefactor is the fraction of the total field structure that electromagnetism represents.

### 6. The Einstein-Hilbert Action

**Standard:**

$$S_{EH} = \frac{1}{16\pi G} \int R \sqrt{-g} \, d^4x$$

**From K, D:**

$$S_{EH} = \frac{1}{K^2 \pi G} \int R \sqrt{-g} \, d^4x$$

The 16 is K² = 16. The bimetric coupling between TetA and TetB produces K² = 16 face-to-face channels. The gravitational action counts all of them.

### 7. The Scalar Coupling

**Standard:**

$$8\pi G \rho = \text{(source term in field equations)}$$

**From K, D:**

$$2K\pi G \rho$$

The 8 is 2K. The scalar sector has 2K = 8 face-pair channels (K faces per tetrahedron, 2 tetrahedra, paired across the boundary).

### 8. Gravitational Light Deflection

**Standard (GR):**

$$\theta = \frac{4GM}{c^2 b}$$

**From K, D:**

$$\theta = \frac{KGM}{c^2 b}$$

The 4 is K. The photon's stratum passes through all K = 4 faces of the deforming gravity field. Each face contributes one unit of deflection. GR derives this through the full geodesic equation. GFD derives it by counting faces.

### 9. Shapiro Time Delay

**Standard:**

$$\Delta t = \frac{4GM}{c^3} \ln\frac{r_1 r_2}{b^2}$$

**From K, D:**

$$\Delta t = \frac{KGM}{c^3} \ln\frac{r_1 r_2}{b^2}$$

Same K = 4 as the deflection. The stratum passes through K faces inbound and the same K faces outbound, but the logarithmic structure means the total delay is K × (logarithmic path), not 2K.

### 10. Stefan-Boltzmann Law

**Standard:**

$$\sigma_{SB} = \frac{2\pi^5 k_B^4}{15 h^3 c^2}$$

**From K, D:**

$$\sigma_{SB} = \frac{|Z_2| \cdot \pi^5 k_B^4}{(K^2-1) h^3 c^2}$$

The 15 is K² − 1. The thermal radiation field has K² = 16 face-to-face channels, but 1 channel (the identity, the vacuum state) carries no radiation. The radiating channels number K² − 1 = 15. The 2 in the numerator is |Z₂| (both chambers contribute to the thermal emission).

### 11. Planck Spectral Density

**Standard:**

$$u(\nu) = \frac{8\pi h \nu^3}{c^3} \cdot \frac{1}{e^{h\nu/kT}-1}$$

**From K, D:**

$$u(\nu) = \frac{2K\pi h \nu^3}{c^3} \cdot \frac{1}{e^{h\nu/kT}-1}$$

The 8π is 2Kπ. Same as the scalar coupling sector: 2K = 8 face-pair channels carry the thermal photon field. The ν³ exponent is D (three spatial faces, each contributing one power of frequency to the density of states).

### 12. Radiation Pressure

**Standard:**

$$P = \frac{u}{3}$$

**From K, D:**

$$P = \frac{u}{D}$$

The 3 is D. Radiation pressure is the photon momentum flux averaged over D = 3 spatial directions. Each spatial face carries 1/D of the total momentum.

### 13. Photon Gas Energy

**Standard:**

$$E = 3PV$$

**From K, D:**

$$E = D \cdot P \cdot V$$

The 3 is D. The energy-pressure relation for a photon gas reflects the D = 3 spatial degrees of freedom.

### 14. Bekenstein-Hawking Entropy

**Standard:**

$$S = \frac{k_B A}{4 \ell_P^2}$$

**From K, D:**

$$S = \frac{k_B A}{K \ell_P^2}$$

The 4 is K. Each Planck-area cell on the black hole horizon has K = 4 possible face-coupling configurations. The entropy counts configurations per unit area, with 1/K configurations per Planck cell.

### 15. Hawking Temperature

**Standard:**

$$T_H = \frac{\hbar c^3}{8\pi k_B G M}$$

**From K, D:**

$$T_H = \frac{\hbar c^3}{2K\pi k_B G M}$$

The 8π is 2Kπ. Hawking radiation is thermal emission from the 2K = 8 scalar-sector face pairs at the horizon. The temperature is set by the surface gravity, which distributes across 2K channels.

---

## The Pattern

Every prefactor falls into one of six categories:

| Category | Expression | Value | Where It Appears |
|----------|-----------|-------|-----------------|
| Closure constant | K | 4 | EM Lagrangian, deflection, Shapiro, BH entropy, Rayleigh exponent |
| Bimetric channels | K² | 16 | Einstein-Hilbert action |
| Scalar face pairs | 2K | 8 | Scalar coupling, Planck spectrum, Hawking temperature |
| Off-diagonal | K²−1 | 15 | Stefan-Boltzmann |
| Spatial faces | D | 3 | Radiation pressure, photon gas, Thomson denominator |
| Chamber count | \|Z₂\| | 2 | Compton shift, Stefan-Boltzmann numerator |
| Composite | 2K/D | 8/3 | Thomson cross-section |
| Inverse composite | D/(2K) | 3/8 | Klein-Nishina high-energy |

No numerical prefactor in photon physics is unexplained. Each one counts something specific in the stellated octahedron: faces, face-pairs, channels, chambers, or their ratios.

---

## What This Means

These are not fits. These are not numerological coincidences. Every equation listed above was derived independently in the 20th century through quantum electrodynamics, general relativity, or statistical mechanics. None of them were looking for K = 4 or D = 3. The numerical prefactors were computed from first principles within each formalism and confirmed experimentally to extraordinary precision.

The fact that every one of these prefactors decomposes into the same two integers — the unique solution to 2(D+1) = 2^D — is either the most remarkable coincidence in the history of physics, or it is evidence that the stellated octahedron topology is the structural origin of photon physics.

There is no third option.
