# Dual Tetrad Gravity And The Field Origin

**Deriving Fundamental Equations With (3+1)^2 Topology**

Author: Stephen Nelson
Date: February 2026

---

## Abstract

This paper derives fundamental equations of classical, relativistic, and quantum physics from a single geometric structure: the (3+1)^2 dual tetrad topology. Four quantitative results are presented with zero free parameters: the gravitational constant G (0.12% accuracy), the force hierarchy (alpha^20 ~ 10^{-43}), the dark matter correction factor mu(x) = x/(1+x), and the electron mass m_e (0.1% accuracy). Geometric interpretations of the inverse square law, mass-energy equivalence, spin, the uncertainty principle, energy quantization, and the fine structure constant are also developed. The only external input is the Hubble constant H.

---

## Files

### Core Paper

| File | Description |
|------|-------------|
| `Dual_Tetrad_Gravity_And_The_Field_Origin.tex` | Main LaTeX source (REVTeX 4.2) |
| `Dual_Tetrad_Gravity_And_The_Field_Origin.pdf` | Compiled paper |
| `dark_matter_corrective_lens.png` | Figure 3: Dark matter resolution (4-panel) |

### Complementary Technical Notes

| File | Description |
|------|-------------|
| `Covariant_Complete_Lagrangian_From_(3+1)^2_Topological_Field_Closure.tex/.pdf` | Zero-parameter scalar-tensor action, field equations, and five predictions |
| `Every_Integer_In_G_Counted_From_Bimetric_Gravity.tex/.pdf` | Term-by-term counting of every integer in G from GR and bimetric gravity |
| `Why_the_Fine-Structure_Constant_Governs_Gravitational_Coupling.tex/.pdf` | Why alpha governs gravity, and derivation of mu(x) = x/(1+x) from topology |

### Validation

| File | Description |
|------|-------------|
| `run_all_validations.py` | Validates all numerical claims in the paper |
| `dark_matter_corrective_lens.py` | Generates Figure 3 and rotation curve data |

---

## Compilation

### Requirements

- LaTeX distribution with `pdflatex` (MiKTeX, TeX Live, or MacTeX)
- REVTeX 4.2 document class (included in standard distributions)
- Packages: `graphicx`, `amsmath`, `amssymb`, `bm`, `hyperref`, `xcolor`, `booktabs`, `multirow`, `float`, `tikz`

### Build

```bash
pdflatex Dual_Tetrad_Gravity_And_The_Field_Origin.tex
pdflatex Dual_Tetrad_Gravity_And_The_Field_Origin.tex
```

Two passes are required to resolve cross-references and citations.

---

## Validation

### Requirements

- Python 3.6 or later
- Standard library only (math module)

### Running

```bash
python run_all_validations.py
```

This script validates every numerical claim in the paper using full-precision CODATA 2022 constants. It covers:

- **Result 1:** G from tetrad topology (0.12% match)
- **G in terms of d:** Demonstrates only d=3 yields a physical G
- **Exponent sensitivity:** Adjacent integers (20, 22) miss by factor 137
- **Classical electron radius:** Route 1 (electromagnetic)
- **Gravitational electron radius:** Route 2 (topological, 0.21% match)
- **Spin:** Face ratio (2/8) x 2*hbar = hbar/2 (exact)
- **Coupling hierarchy:** 1 + 4 + 16 = 21 (exact)
- **Force hierarchy:** alpha^20 ~ 10^{-43}
- **Fine structure constant:** f_closure / f_Compton = 2*pi/alpha (algebraic identity)
- **Characteristic acceleration:** a_0 = k^2 * G * m_e / r_e^2 (0.41% match)
- **Correction factor:** mu(x) = x/(1+x) limits verified
- **Aperture correction:** sqrt(k/pi) = 1.128
- **Hubble constant:** H = 69.92 km/s/Mpc (0.11% from GW170817)
- **Rotation curves:** 5 radii for a 10^11 solar mass galaxy
- **Electron mass (Result 10):** r = 2.82 fm, m = 9.11e-31 kg (0.1% match)
- **Round-trip test:** m_e -> H -> m_e closure (0.10%)
- **Precision table:** All four derived quantities

### Generating Figure 3

```bash
python dark_matter_corrective_lens.py
```

Requires `numpy` and `matplotlib`. Generates `dark_matter_corrective_lens.png`.

---

## Complementary Technical Notes

Three self-contained technical notes accompany this paper, developing extended aspects of the framework:

1. **Covariant-Complete (3+1)^2 Gravity** -- Presents the zero-parameter action, its field equations, and five predictions spanning five domains
2. **The Origin of Every Integer in G** -- Traces each integer in G to its GR/bimetric origin with a translation table and sensitivity analysis
3. **Why the Fine-Structure Constant Governs Gravitational Coupling** -- Establishes why alpha governs gravity and derives mu(x) from the stellated octahedron

## Companion Papers

This paper builds on results established in:

1. "The Gravitational Constitutive Law" (Nelson 2026) -- derives mu(x) = x/(1+x) from closure constraints
2. "A Covariant Theory Without Dark Matter" (Nelson 2026) -- scalar-tensor covariant completion
3. "Field Closure and the Topology of Gravity" (Nelson 2026) -- derives k=4 and three-route convergence on r_e
4. "Deriving the Gravitational Constant from Spacetime Topology" (Nelson 2026) -- derives G and spin from the stellated octahedron

---

## Constants Used

All numerical values are computed from CODATA 2022 fundamental constants (Rev. Mod. Phys. 96, 025004, 2024):

| Constant | Symbol | Value | Source |
|----------|--------|-------|--------|
| Gravitational constant | G | 6.67430(15) x 10^{-11} m^3/(kg*s^2) | CODATA 2022 |
| Electron mass | m_e | 9.1093837139(28) x 10^{-31} kg | CODATA 2022 |
| Classical electron radius | r_e | 2.8179403205(13) x 10^{-15} m | CODATA 2022 |
| Speed of light | c | 299792458 m/s | Exact (SI) |
| Planck constant | h | 6.62607015 x 10^{-34} J*s | Exact (SI) |
| Fine structure constant | alpha | 7.2973525693(11) x 10^{-3} | CODATA 2022 |
| Elementary charge | e | 1.602176634 x 10^{-19} C | Exact (SI) |

---

## License

This work is submitted for publication in Physical Review D. All rights reserved by the author.

## Contact

Stephen Nelson
stephen@fielddynamics.org
ORCID: 0009-0008-6190-3269
