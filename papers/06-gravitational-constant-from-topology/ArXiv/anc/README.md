# Paper VI Ancillary Files

Supplementary materials for: **Deriving the Gravitational Constant from Spacetime Topology**

`gravitational-constant` `fine-structure-constant` `topology` `tetrad` `theoretical-physics` `numerical-validation`

## Overview

This folder contains ancillary files for Paper VI:

1. **Numerical validation** — Python script validating all calculations
2. **Interactive visualization** — 3D visualization of the dual tetrahedral structure

The key insight is that all results derive from a single foundational input: **spacetime is (3+1) dimensional**.

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Usage

```bash
python run_all_validations.py
```

## What It Validates

### 1. Gravitational Constant (G)

The formula:

```
G = [(3+1)² + 1] / [3(3+1) + 1] × α^[1+(3+1)+(3+1)²] × ℏc/m_e²
```

- **Predicted:** 6.666 × 10⁻¹¹ m³/(kg·s²)
- **Measured:** 6.674 × 10⁻¹¹ m³/(kg·s²)
- **Agreement:** 0.12% with zero adjustable parameters

### 2. Electron Spin (S)

From the dual tetrahedral face structure:

```
S = (N_TIME / N_total) × L_total = (2/8) × 2ℏ = ℏ/2
```

- **Calculated:** ℏ/2
- **Measured:** ℏ/2
- **Match:** EXACT

### 3. Coupling Hierarchy (1 + D + D²)

Where D = (3+1) = 4:

| Term | Value | Physical Origin |
|------|-------|-----------------|
| 1 | 1 | Time — the dimension that makes 3D into spacetime |
| D | 4 | Spacetime dimension (3+1) |
| D² | 16 | Coupled spacetime — dual tetrahedra interaction |
| **Total** | **21** | Full coupling hierarchy |

### 4. Fine Structure Constant (Speculative)

An empirical observation (not a derivation):

```
1/α = 2³ × 17 + 1 + 1/28 = 137.0357...
```

Agreement to 5 significant figures. Presented for completeness; theoretical basis remains to be established.

## The (3+1) Foundation

The script demonstrates the logical chain:

```
GR (3+1 dimensional) 
    → Tetrad (4 legs)
        → Tetrahedron (4 faces)
            → Dual tetrahedra (coupled structure)
                → G, Spin
```

Every topological factor traces to the single input: d = 3 spatial dimensions.

## Physical Constants

All calculations use CODATA 2018 values:

| Constant | Symbol | Value |
|----------|--------|-------|
| Fine structure constant | α | 1/137.036 |
| Reduced Planck constant | ℏ | 1.0546 × 10⁻³⁴ J·s |
| Speed of light | c | 2.9979 × 10⁸ m/s |
| Electron mass | m_e | 9.1094 × 10⁻³¹ kg |

## Output

The script prints detailed results for each validation and exits with:
- Code 0: All validations passed
- Code 1: One or more validations failed

## File Structure

```
anc/
├── README.md                              # This file
├── run_all_validations.py                 # Numerical validation script
└── dfp_gravity_field_dynamics_visual.html # Interactive 3D visualization
```

## Interactive Visualization

The `dfp_gravity_field_dynamics_visual.html` file provides an interactive 3D visualization of the dual tetrahedral structure described in the paper.

### Features

- **Stellated octahedron** — the two interlocking tetrahedra (blue and yellow)
- **8 coupling ports** — 4 per tetrahedron (2 TIME + 6 SPATIAL)
- **Field closure cycles** — animated closure driven by Pi digits (base 8)
- **Port aperture boundaries** — Voronoi domains shown on the enclosing sphere
- **Field Origin** — central glow where the two tetrahedra couple

### Usage

Open the HTML file directly in any modern web browser (Chrome, Firefox, Safari, Edge). No installation or server required — the visualization uses Three.js loaded from CDN.

### What It Shows

The visualization demonstrates the key structural insight of Paper VI: gravity requires **dual tetrahedra** with opposite orientations, coupled at a central Field Origin. The animated field closure cycles show how all 8 faces activate exactly once per cycle, reflecting the (3+1) structure of spacetime.

## License

This validation code accompanies Paper VI and is provided for reproducibility.

## Contact

Stephen Nelson  
stephen@fielddynamics.org  
ORCID: 0009-0008-6190-3269
