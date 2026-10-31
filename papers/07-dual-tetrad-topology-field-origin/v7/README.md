# Dual Tetrad Topology and the Field Origin: From Nuclear Decay to Galactic Dynamics

**Bidirectional Validation of a Zero-Parameter Gravitational Field Theory**

**Author:** Stephen Nelson
**Contact:** stephen@fielddynamics.org

`tetrad` `bimetric-gravity` `modified-gravity` `gravitational-constant` `nuclear-physics` `galaxy-rotation-curves` `theoretical-physics`

---

## Overview

This directory contains supplemental computational materials for the paper "Dual Tetrad Topology and the Field Origin: From Nuclear Decay to Galactic Dynamics."

The paper derives a zero-parameter covariant completion of modified gravity from dual tetrad field topology. All numerical claims are independently verifiable using the included Python scripts, which compute predictions from CODATA 2022 fundamental constants and the topological integer k = 4 from simplex packing in (3+1) dimensions. Section 8.3 establishes the scale-invariant foundation through the modified Poisson equation, demonstrating that both the normalization factor 4π and the coupling ratio 17/13 emerge from topological constraints, ensuring the same field equations govern gravitational fields from quantum (10⁻¹³ m) to cosmic (10²¹ m) scales.

---

**Revision notes.** [`REVISION_NOTES.md`](REVISION_NOTES.md) records a full reading of v7: what later letters strengthen, and what a revision should correct or reframe, with the numerical checks in [`revision_checks.py`](revision_checks.py).

---

## Included Files

### 1. **run_all_validations.py**

**Purpose:** Complete validation suite for all numerical claims in the paper.

**What it validates:**
- Gravitational constant G (0.12% tree-level, 0.001% one-loop)
- Fine-structure constant 1/α = 137.036 (0.00021% agreement)
- Acceleration scale a₀ (0.41% agreement)
- Electron mass mₑ (0.10% agreement)
- Schwinger one-loop correction and propagation to Hubble constant H
- Exponent sensitivity (±1 shifts G by 1/α = 137)
- Spin from face ratio
- Rotation curve predictions
- Bidirectional round-trip consistency

**Requirements:** Python 3.6+, standard library only

**Usage:**
```bash
python run_all_validations.py
```

**Expected output:** Summary table showing all validations passing with reported precision levels.

---

### 2. **run_all_covariant_predictions.py**

**Purpose:** Compute all 14 empirical tests plus 1 consistency check from Section X (Empirical Validation).

**What it computes:**
- **Tier 1 tests:** GW speed, LLR constraint on Ġ/G, neutron lifetime, Bullet Cluster offset
- **Tier 2 tests:** Gaia wide binaries, Milky Way rotation, expansion history E(z), binary pulsar
- **Tier 3 tests:** Cluster dynamics, cosmological evolution
- **Consistency check:** CMB Ωₘ/Ωᵦ (uses observed densities as input, not an independent prediction)

All predictions use zero adjustable parameters: only CODATA 2022 constants (G, c, ℏ, mₑ, α), k = 4, and Planck 2018 densities (Ωₘ, Ωᵣ).

**Requirements:**
- Python 3.6+
- numpy
- **Data file:** `sparc_tully_fisher_table.dat` (included, SPARC galaxy sample for Tully-Fisher tests)

**Usage:**
```bash
python run_all_covariant_predictions.py
```

**Expected output:** Detailed results for all 14 tests plus 1 consistency check with quantitative agreement metrics (percentage deviations, σ values).

---

### 3. **dark_matter_corrective_lens.py**

**Purpose:** Generate Figure 6 (The Dark Matter Corrective Lens)

**What it generates:**
Four-panel figure showing:
- **Top left:** Rotation curves (Newtonian vs topological vs deep-MOND asymptote)
- **Top right:** Correction factor μ(x) = x/(1+x) with regime shading
- **Bottom left:** Force law transition from 1/r² to 1/r (log-log)
- **Bottom right:** Apparent dark matter fraction vs radius

**Requirements:** Python 3.6+, numpy, matplotlib

**Usage:**
```bash
python dark_matter_corrective_lens.py
```

**Expected output:** `figure_6_dark_matter_corrective_lens.png` saved to current directory

---

### 4. **sparc_tully_fisher_table.dat**

**Purpose:** Observational data for Tully-Fisher relation tests (required by run_all_covariant_predictions.py)

**What it contains:**
- SPARC galaxy sample data
- Galaxy rotation velocities
- Baryonic masses
- Used for Tully-Fisher Baryonic Relation (BTFR) validation tests

**Location:** `sparc_tully_fisher_table.dat` (21 KB, included in package)

**Format:** Tab-delimited ASCII data table

**Note:** This file is automatically loaded by run_all_covariant_predictions.py. No manual intervention required.

---

### 5. **GRAVIS: Galactic Rotation from Field Dynamics**

**Purpose:** Interactive zero-parameter rotation curve prediction tool implementing the dual tetrad gravity framework.

**Repository:** [https://github.com/fielddynamics/gravis](https://github.com/fielddynamics/gravis)

**What it does:**
- Computes full galactic rotation curves from baryonic mass distributions alone (no dark matter, no free parameters)
- Solves the AQUAL field equation with the topological constitutive law mu(x) = x/(1+x)
- Provides forward prediction (mass -> velocity) and inverse inference (velocity -> mass)
- Includes a web-based interface and REST API
- Ships with six galaxies: Milky Way, Andromeda, NGC 3198, NGC 2403, M33, NGC 6503

**Requirements:** Python 3.6+, Flask, NumPy, SciPy

**Usage:**
```bash
git clone https://github.com/fielddynamics/gravis.git
cd gravis
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000 in your browser.

---

## Installation

All scripts use standard Python libraries except where noted. To install numpy (required for covariant predictions and figure generation):

```bash
pip install numpy matplotlib
```

---

## Running All Validations

To verify all numerical claims and predictions:

```bash
# 1. Validate fundamental constants and equations
python run_all_validations.py

# 2. Compute all empirical predictions
python run_all_covariant_predictions.py

# 3. Generate dark matter figure
python dark_matter_corrective_lens.py
```

---

## Key Results Summary

**From run_all_validations.py:**
- G derived to 0.12% (tree-level), 0.001% (one-loop)
- 1/α = 137.036 derived to 0.00021%
- mₑ derived to 0.10%
- All structural integers (1, 4, 7, 13, 16, 17, 21, 137) verified from topology

**From run_all_covariant_predictions.py:**
- 14 empirical tests spanning 36 orders of magnitude
- Nuclear decay: 1.084% predicted vs 1.081% observed (0.3% agreement)
- Milky Way rotation: 229 km/s predicted vs 229±5 km/s observed (exact)
- Gaia wide binary plateau: 0.39 km/s predicted vs 0.5±0.15 km/s observed
- GW speed: c exact to 10⁻¹⁵
- Zero adjustable parameters

**Bidirectional validation:** Same k = 4 constrains both nuclear physics (10⁻¹⁵ m) and galactic dynamics (10²¹ m).

---

## Technical Notes

### Precision
All calculations use full-precision CODATA 2022 fundamental constants. No intermediate rounding is applied. The scripts compute exactly what appears in the paper—no fitted parameters, no post-hoc adjustments.

### Dependencies
- **run_all_validations.py:** Standard library only (no external dependencies)
- **run_all_covariant_predictions.py:** Requires numpy for numerical integration; requires `sparc_tully_fisher_table.dat` (included)
- **dark_matter_corrective_lens.py:** Requires numpy and matplotlib for plotting

### Python Version
All scripts tested with Python 3.6+ on Windows, macOS, and Linux.

---

## Paper Reference

When citing this work, please reference:

**Nelson, S.** (2026). Dual Tetrad Topology and the Field Origin: From Nuclear Decay to Galactic Dynamics. *[Journal TBD]*.

---

## License

These computational materials are provided to verify the numerical claims in the associated paper. Free to use for academic and research purposes with appropriate citation.

---

## Contact

For questions about the computational methods or to report issues:

**Stephen Nelson**
Email: stephen@fielddynamics.org

---

**Last Updated:** February 2026
**Paper Version:** v7
