# Gravity Field Dynamics — Documentation

`gravity` `general-relativity` `modified-gravity` `tetrad` `theoretical-physics` `cosmology` `documentation`

These pages are the written documentation of the Gravity Field Dynamics (GFD) framework, by Stephen Nelson, Field Dynamics Research. They were originally published at docs.fielddynamics.org and are reproduced here as plain Markdown so they remain readable on GitHub whether or not that site is online. Equations are written in LaTeX and render directly on GitHub.

Only completed pages are included. The documentation site also planned pages on nuclear physics, gauge and particle physics, quantum theory and cosmology, and several further gravitation topics; those exist only as outlines in the documentation repository and are not reproduced here. The research behind many of them is in [`research/`](../research/) and [`papers/`](../papers/).

## Contents

### Foundations

1. [The Gravity Field](01-foundations/01-the-gravity-field.md)
2. [Field Closure Principle](01-foundations/02-field-closure-principle.md)
3. [Why K = 4 and D = 3](01-foundations/03-why-k4-d3.md)
4. [Dual Tetrahedron and Field Origin](01-foundations/04-dual-tetrahedron-field-origin.md)
5. [Propagation Requires Neighbors](01-foundations/05-propagation-requires-neighbors.md)
6. [Field Closure in GR](01-foundations/06-field-closure-in-gr.md)
7. [The Characteristic Scale](01-foundations/07-characteristic-scale.md)
8. [Face Structure and Spin](01-foundations/08-face-structure-and-spin.md)
9. [The 28 Geometric Elements](01-foundations/09-twenty-eight-geometric-elements.md)
10. [The Stellated Octahedron](01-foundations/10-stellated-octahedron.md)

### Gravitation

1. [Coupling Polynomial and Structural States](02-gravitation/01-coupling-polynomial-structural-states.md) · [derivation](02-gravitation/01-coupling-polynomial-structural-states-derivation.md)
2. [The Field Equation](02-gravitation/02-field-equation.md)
3. [Constitutive Law μ(x)](02-gravitation/03-constitutive-law-mu-x.md)
4. [G from Topology](02-gravitation/04-g-from-topology.md)
5. [Poisson Equation and Scale Invariance](02-gravitation/05-poisson-scale-invariance.md)
6. [Covariant Completion](02-gravitation/06-covariant-completion.md)

### Fundamental Constants

1. [Fine Structure Constant α](03-fundamental-constants/01-fine-structure-constant-alpha.md)
2. [Electron Mass](03-fundamental-constants/02-electron-mass.md)
3. [Electron Spin](03-fundamental-constants/03-electron-spin.md)
4. [Inverse Square, E = mc², Force Hierarchy](03-fundamental-constants/04-inverse-square-emc2-force-hierarchy.md)
5. [H0 Prediction](03-fundamental-constants/05-h0-prediction.md)
6. [Capstone Constants Suite](03-fundamental-constants/06-capstone-constants-suite.md)

### Galactic Dynamics

1. [Rotation Curves](04-galactic-dynamics/01-rotation-curves.md)
2. [Decoded Velocity to Effective Mass](04-galactic-dynamics/02-decoded-velocity-to-effective-mass.md)
3. [Radial Acceleration Relation](04-galactic-dynamics/03-radial-acceleration-relation.md)

### API Reference

1. [Rotation Curves](05-api-reference/01-api-rotation-curves.md)
2. [Galaxy Catalog](05-api-reference/02-api-galaxy-catalog.md)
3. [Cosmology](05-api-reference/03-api-cosmology.md)

## The full documentation site (Flask app)

The complete documentation site is available as a separate repository, **[fielddynamics/docs](https://github.com/fielddynamics/docs)**. It is a small Flask application that renders these pages with section navigation, interactive figures and the per-page validation scripts (`tests/validate.py`), and it serves the machine-readable `llms.txt`. To run it locally:

```bash
git clone https://github.com/fielddynamics/docs
cd docs
pip install -r requirements.txt
python app.py
```

Then open <http://localhost:5000/framework/>.

The pages in this folder are a copy of the completed pages in that repository, taken in October 2026. If the two differ, the docs repository holds the source; changes made there are not synchronised here automatically.
