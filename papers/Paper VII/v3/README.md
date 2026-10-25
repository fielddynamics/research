# Dual Tetrad Gravity And The Field Origin

**Deriving Fundamental Equations from Dual Tetrad Topology**

Author: Stephen Nelson
Date: February 2026

---

## Overview

This paper derives fundamental equations of classical, relativistic, and quantum physics from a single topological structure: the dual tetrad coupling topology (two tetrahedra with opposite orientations coupled at a shared center). Seven quantitative results are presented with zero free parameters:

1. **Gravitational constant G** - from the coupling hierarchy alpha^{1+4+16} (0.12% accuracy)
2. **Force hierarchy** - gravity/EM ~ alpha^20 ~ 10^{-43}
3. **Fine-structure constant** - 1/alpha = 137 + 1/28 = 137.036 (0.00021% accuracy)
4. **Dark matter correction** - mu(x) = x/(1+x) with a_0 = k^2 G m_e / r_e^2 (0.41% accuracy)
5. **Covariant completion** - all five beta_n coupling constants determined with zero free parameters
6. **Hubble constant** - H = 69.92 km/s/Mpc from the cosmological horizon relation
7. **Electron mass** - from two exactly determined closure equations (0.1% accuracy)

Topological interpretations of the inverse square law, mass-energy equivalence, spin hbar/2, energy quantization, wave-particle duality, and the energy-momentum relation are also developed. No particle-physics input is required; the Hubble constant H enters as a cosmological observable and is itself predicted by the topology.

---

## Files

| File | Description |
|------|-------------|
| `Dual_Tetrad_Gravity_And_The_Field_Origin.pdf` | The paper |
| `Deriving_the_Gravitational_Constant_from_Spacetime_Topology.pdf` | Supplementary: the preceding paper, which derives G and electron spin from the stellated octahedron |
| `Covariant_Complete_Dual_Tetrad_Gravity.pdf` | Supplementary: Covariant-Complete Dual Tetrad Gravity -- zero-parameter scalar-tensor action, field equations, and five falsifiable predictions |
| `run_all_validations.py` | Validates every numerical claim (Python 3.6+, standard library only) |
| `dark_matter_corrective_lens.py` | Generates Figure 6: dark matter resolution (requires numpy, matplotlib) |

---

## Validation Suite

### Requirements

- Python 3.6 or later
- Standard library only (no external dependencies)

### Running

```bash
python run_all_validations.py
```

This script validates **every** numerical equation in the paper using full-precision CODATA 2022 constants. Validations are organized by paper section:

**Section II -- Theoretical Foundations**
- Classical electron radius: Route 1 (EM stability)
- Gravitational electron radius: Route 2 (topological, 0.21% convergence)

**Section III -- The (3+1)^2 Foundation**
- Coupling hierarchy: f(k) = 1 + k + k^2 = 21
- Three structural states: f(k) at s = +1, 0, -1 giving 21, 17, 13
- Prefactor decomposition: 17/13 = (k^2+1)/(kd+1)
- Spin from face ratio: (2/8) x 2 hbar = hbar/2 (two independent routes)

**Section IV -- The (3+1) Equations**
- Result 1: G from tetrad topology (0.12%)
- G for arbitrary dimension d (only d=3 works)
- Exponent sensitivity (adjacent integers miss by factor 137)
- Result 4: Force hierarchy alpha^20 ~ 10^{-43}

**Section VI -- The Fine Structure Constant**
- Alpha as topological scale ratio: alpha = r_e / lambda_bar_C
- Integer 137 from interaction state counting: N = 1 + 2k(k^2+1)
- 28 face-channels: k(k+d) = 4 x 7 = 28
- Result 6: 1/alpha = 137 + 1/28 from topological breadth (0.00021%)
- Alpha from physical rates: f_closure / f_Compton (independent confirmation)

**Section VII -- Conclusion**
- Characteristic acceleration a_0 = k^2 G m_e / r_e^2 (0.41%)
- Cosmological connection: a_0 = cH/(2pi) sqrt(k/pi)
- Correction factor mu(x) = x/(1+x) (limits verified)
- Deep-MOND limit: g_eff = sqrt(g_N a_0) ~ 1/r
- Flat rotation velocity: v = (G M a_0)^{1/4} (Tully-Fisher)
- Apparent dark matter fraction: f_dark = 1/(1+x) (~85%)
- Corrective lens: M_actual = M_inferred x mu (recovers true mass)
- Aperture correction: sqrt(k/pi) = 1.128
- Hubble constant: H = 69.92 km/s/Mpc (between Planck and SH0ES)
- Rotation curves: 5 radii for a 10^11 solar mass galaxy
- Result 7: Electron mass from closure geometry (0.1%)
- Round-trip test: m_e -> H -> m_e bidirectional closure
- Precision table: all five derived quantities

### Sample Output

```
Total validations: 16
Average deviation: 0.16%
```

### Generating Figure 3

```bash
python dark_matter_corrective_lens.py
```

Requires `numpy` and `matplotlib`. Generates `dark_matter_corrective_lens.png`.

---

## Extended Validation Suite

A comprehensive validation suite with 813 tests across 16 categories is publicly available:

**Repository:** [https://github.com/fielddynamics/dfp-gravity-field-model](https://github.com/fielddynamics/dfp-gravity-field-model)

The extended suite verifies:

- All numerical predictions from this paper (G, 1/alpha, a_0, m_e, H)
- Exponent sensitivity (changing +/-1 shifts G by 1/alpha = 137)
- Spin from face ratio
- Rotation curve predictions and bidirectional round-trip consistency
- Mathematical foundation checks: exterior derivative nilpotency (d^2 = 0), Stokes theorem, Bianchi identity, and Noether current conservation on the stellated octahedron mesh
- Cross-domain structural consistency: 30+ integer coefficient decompositions across Kepler's laws, equipartition, gravitational-wave quadrupole formula, and wave mode counting

MIT-licensed. All tests are independently runnable with Python 3.10+ and no proprietary dependencies.

---

## Companion Papers

This paper extends results from "Deriving the Gravitational Constant from Spacetime Topology" (Nelson 2026), which established the dual tetrad topology and derived G to 0.12% accuracy with zero free parameters. That paper is included as supplementary material. The present paper asks what else the same topological structure determines, expanding the framework to seven quantitative predictions, the dark matter resolution, and topological interpretations across classical, relativistic, and quantum physics.

The broader series of companion papers:

1. "The Gravitational Constitutive Law" (Nelson 2026) -- derives mu(x) = x/(1+x) from closure constraints
2. "A Covariant Theory Without Dark Matter" (Nelson 2026) -- scalar-tensor covariant completion with five falsifiable predictions
3. "Field Closure and the Topology of Gravity" (Nelson 2026) -- derives k=4 and three-route convergence on r_e
4. "Deriving the Gravitational Constant from Spacetime Topology" (Nelson 2026) -- derives G and spin from the stellated octahedron (included as supplementary)

---

## Constants

All numerical values are computed from CODATA 2022 fundamental constants (Rev. Mod. Phys. 96, 025004, 2024):

| Constant | Symbol | Value | Source |
|----------|--------|-------|--------|
| Gravitational constant | G | 6.67430(15) x 10^{-11} m^3/(kg s^2) | CODATA 2022 |
| Electron mass | m_e | 9.1093837139(28) x 10^{-31} kg | CODATA 2022 |
| Classical electron radius | r_e | 2.8179403205(13) x 10^{-15} m | CODATA 2022 |
| Speed of light | c | 299792458 m/s | Exact (SI) |
| Planck constant | h | 6.62607015 x 10^{-34} J s | Exact (SI) |
| Fine structure constant | alpha | 7.2973525693(11) x 10^{-3} | CODATA 2022 |
| Elementary charge | e | 1.602176634 x 10^{-19} C | Exact (SI) |

---

## License

This work is submitted for publication in Physical Review D. All rights reserved by the author.

## Contact

Stephen Nelson
stephen@fielddynamics.org
ORCID: 0009-0008-6190-3269
