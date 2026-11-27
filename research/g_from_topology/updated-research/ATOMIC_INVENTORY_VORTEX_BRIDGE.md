# Atomic inventory and fixed-geometry vortex response

November 2026. Research extension, not a numbered proof. [T] exact algebra, [D] conditional model, [E] physical interpretation.

## 1. Source reconciliation

The earlier Sierpiński walk note explicitly gives the 4×4×4 address ledger, face/channel/subchannel reads and maximum landmark count 1+4+16=21. The nuclear walk uses A (mass number), whereas the electronic configuration note uses electron occupancy, n and l; these are not the same inventory. Paper XIII uses a bidirectional bound law and a 64-position coupling sum, rather than the earlier landmark score. Its reported seven magic numbers and 95 keV mean binding-energy error are source claims, not independently rerun. The older valence note's polynomial contains a K²s² term, whereas the electron configuration and newer projective work use K²; do not equate them at s=0. The maximum count is common, but a landmark score is not a determinant. The SO(3) highest-irrep rule gives capacities 2,6,10,14, conditional on the representation and spin premises; the electronic resonance heuristic reports 80/83 configurations, with Ru, Ce, Pt unresolved. These are not independent validation of the native vortex Hamiltonian.

The Vortex Horizon proposes retained bound TetB inventory producing an outward electric vortex. Its radii use n and Clementi effective nuclear charges; they do not derive screening. Its atomic long-range logarithmic potential/1/r acceleration would require separate consistency with measured Coulomb fields, ionization and spectroscopy. The later preregistration of the one-directional screening law failed its primary test; the bound-law preregistration failed all four criteria. Do not use either as a verified microscopic law. The Overdetermined System propagates atomic radii and established relations into other properties; it is not a first-principles vortex energy derivation.

Matter Vortex and Charge supplies excess occupations n_A,n_B, signed q=n_B−n_A, and equal radial ports u_k=q/4 in a chosen reduced energy. The same note distinguishes signed radial response from axial circulation and uses a charge-even gravitational Green kernel as a premise. The electron closure note treats radial response as dynamical, and explicitly warns that the fixed 36-coordinate H contains no radius coordinate. Thus a changing vortex envelope is a candidate physical response, not a deformation of the address geometry.

## 2. Distinguish inventory from electric charge

Define abstract excess-register sum s=n_A+n_B and difference q=n_B−n_A. Chamber exchange sends (s,q)→(s,−q). These are model coordinates, not established baryon number, charge or mass. In atoms Z counts protons, N neutrons, A=Z+N, and the net charge of an atom/ion is e(Z−N_e). A neutral atom can have substantial internal electric fields and positive mass. Isotopes test the distinction: changing N at fixed Z changes mass and binding, but not nuclear charge or neutral electron count. Isotope shifts and nuclear-size effects can still alter spectra. Gravity must couple to total energy, including binding, rather than raw A or |q|. A charge-even response can depend on q²; charge-even does not mean independent of electromagnetic energy.

## 3. Exact symmetry-resolved fixed-geometry witness [D]

Let x be an exchange-even vortex coordinate and y an exchange-odd coordinate. Keep geometry and coefficients fixed. Use the illustrative reduced energy

E(x,y;s,q)= k_e/2 (x−β y²)² + k_o/2 y² − s x − q y.

For k_e>0 and d=k_o−2βs>0, complete the squares:

E= k_e/2 (x−βy²−s/k_e)² + d/2 (y−q/d)² − s²/(2k_e) − q²/(2d).

The unique global minimum is y*=q/d, x*=s/k_e+β q²/d². The settled energy is −s²/(2k_e)−q²/(2d). Both responses share one energy and fixed geometry. At q=0, x*=s/k_e can be nonzero while y*=0. At general q, x* is even, y* odd. On the symmetric branch the mixed linear response vanishes; the leading even response to signed drive is quadratic, ∂²x*/∂q²=2β/d². The Hessian determinant at equilibrium is k_e d>0. The inverse stiffness is exactly the Jacobian of (x*,y*) with respect to (s,q), since the sources are linear. This supplies a concrete nonlinear witness, not the native H36 action or proof of a physical even/odd observable. Chamber exchange symmetry of the native geometry does not guarantee the selected matter background retains it.

![Even and odd vortex responses](figures/atomic_even_odd_response.svg)

[Offline explorer](interactive/atomic_vortex_response.html).

## 4. Next native derivation

Use two independent perturbations of the fixed native Hamiltonian, one exchange-even and one odd. Project out phase and normalization modes; evaluate Hessian and source overlaps in the appropriate stationary background. At symmetric equilibrium the parity projectors block-diagonalize the linear susceptibility; at a matter-loaded equilibrium they need not. Identify the physical electric charge and total energy registers, demonstrate Maxwell and gravitational source normalization, and compare electronic configurations, isotopic shifts, charge-neutral mass response and binding energy. Do not infer gravitational acceleration from the scalar circulation magnitude alone. The physical source relation, determinant selection and α²¹ factor remain open. A fixed microscopic address operator also does not imply that the macroscopic metric is fixed.

## 5. Verification and provenance

Run `python verify_atomic_vortex_response.py`. Exact symbolic checks cover completion, stability, parity and response. No earlier test reruns, no physical validation, no numbered proof or repository changes. The interactive explorer implements the closed-form witness and is not a vortex simulation.

Sources inspected at repository snapshot 1d73ef8ad10000861a25e1c67e58ddcfc4f563ad:

- [Vortex Horizon](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/research/atom-vortex-horizon/gfd_vortex_horizon_synthesis.md)
- [Valence Shell Structure](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/research/matter/research/gfd_valence_shells_synthesis.md)
- [Electron Configurations](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/research/electron-configurations/gfd_electron_config_synthesis.md)
- [Overdetermined System](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/research/atomic-properties/gfd_overdetermined_synthesis.md)
- [Matter Vortex and Charge](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/research/hadamard-null-cone-vortex-flywheel/MATTER_VORTEX_CHARGE.md)
- [Electron Closure Settlement](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/research/hadamard-null-cone-vortex-flywheel/ELECTRON_CLOSURE_SETTLEMENT.md)
- [Paper XI](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/papers/11-nuclear-shells-tetrahedral-packing/letter.tex)
- [Paper XIII](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/papers/13-nuclear-binding-bidirectional-sst/letter.tex)
- [Screening preregistration](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/research/atomic-properties/PREREGISTRATION_screening.md)
- [Bound screening preregistration](https://github.com/fielddynamics/research/blob/1d73ef8ad10000861a25e1c67e58ddcfc4f563ad/research/atomic-properties/PREREGISTRATION_bound_screening.md)
