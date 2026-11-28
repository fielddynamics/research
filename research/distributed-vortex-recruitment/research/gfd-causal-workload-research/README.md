# GFD — Causal workload and temporal settlement: pre-proof research

**Status: research experiments; no numbered proof or physical validation.** The GPU/workload interpretation is a hypothesis. The goal is to identify a microscopic energy-to-clock source, a collective reconciliation flow, and a one-way causal threshold without simply inserting GR. No repo changes. All experiments use dimensionless model units; no gravitational constant fitted. Python test passes include explicit counterexamples.

## Research questions

1. Does conserved scalar/polar/axial norm uniquely fix a physical clock or flow?
2. Can retained internal energy source a gravitational channel when filtered optical ports cannot see it?
3. Can native continuous hopping or a slowed clock create a one-way causal horizon?
4. What minimum additional interaction is required to get a clock field?
5. How do the proposed results compare to AQUAL, Schwarzschild, Einstein–Rosen and information-capacity benchmarks?

## Results

### 1. Native Field Origin capacity (exact identity, sampled checks)
For the 3+1 complex origin state `z=(a,b)`, after choosing a common phase with real `a` and `b=u+iv`, define `n=|a|²+|b|²`, `P=2au`, `C=2u×v`. Then

`n²-|P|²-|C|²=(a²+|v|²-|u|²)²+4(u·v)²`, and `P·C=0`.

This is inherited from the spectral gravity read. It is a capacity inequality, not an identity relating the physical lapse and shift. Equal norms and even equal component magnitudes can give different polar currents when relative phases differ. If one **assumes** a clock amplitude and flow amplitude with squared occupations summing to one, `N²+v²/c²=1` follows. But neither the physical identification nor the function of load is forced. Explicit alternative allocations obey the same norm, and even identical weak-field slope and critical endpoint can conceal different intermediate clock laws.

### 2. Native H36 energy blindness (exact linear algebra plus numerical evolution)
The Stage IX geometry is independently reconstructed in `native_cell.py` using the existing 33 positions, 36 complex coordinates, 128 bonds, and original ports and weights. No new hopping edges or tuning. The eight filtered observation rows and powers through H^6 have a ten-dimensional invariant nullspace. SymPy certifies the kernel and the polynomial `H(H-2I)=0` on it; each eigenspace has dimension five. Normalized eigenstates at energies 0 and 2 have identical zero filtered histories, and even all four O coordinates are zero. The positive-energy modes remain exact flat localized modes in the two-cell filtered Bloch Hamiltonian. Native **linear** evolution does not excite the bright scalar band from them.

A clock perturbation supported on O, including the symmetric incident-bond derivative `{P_O,H}/2`, annihilates those dark modes. Thus simply modulating the centre in this way cannot source the field from hidden energy. More general nonlinear or nonlocal couplings are not ruled out.

### 3. Candidate energy-to-clock vertex (new conditional diagnostic)
Let `P_i` project onto the coordinates owned by cell i, and `D(N)=sum_i sqrt(N_i) P_i`. Consider `H(N)=D(N) H D(N)` (candidate, not inherited dynamics). At N_i=1,

`dH/dN_i = (P_i H + H P_i)/2`.

The work-conjugate read is `e_i = Re <psi|P_i H|psi>`. Each shared bond is counted once across the sum, `sum_i e_i=<H>`. The derivative resolves dark energy 0 versus 2 even when O alone cannot. Numerical finite differences verify the derivative on the native two-cell Hamiltonian and random systems. This is a symmetry-compatible example of a source operator, **not** a derived lapse dependence. A uniform energy offset leaves isolated unitary dynamics unchanged but changes absolute source under this coupling. A vacuum reference or independent energy normalization is required; differences are invariant under uniform offsets for equal norm. A local energy expectation need not be positive in the dimensionless hopping model.

### 4. Candidate feedback closure
A separate illustrative scalar field action `E(phi)=1/2 phi^T L phi+e^T phi`, with grounded positive graph Laplacian L, gives `phi=-L^-1 e`. Feeding the energy contrast of the native dark states to this action gives a negative, spatially varying clock potential, and negative pair cross energy for positive sources. Tests verify the field residual, symmetry, and cross energy. This is a **constructed feedback** using a chosen stiffness and work term, not native gravity. It shows the missing link precisely: the vertex and the independent dynamical field equation must both come from the actual time-face action. The spectral band has a positive long-wave stiffness D≈0.10509418 (filtered) or 0.12429467 (full), reproduced from the original 72-coordinate model. Its k^-2 pole supplies a candidate spatial Green response, but does not fix physical units, field normalization, propagation or source coupling.

### 5. Causality and horizon obstruction
A real symmetric continuous-time hopping Hamiltonian has reciprocal transition amplitudes. Local positive clock scaling DHD preserves that reciprocity; N_i=0 disconnects the chosen cell in **both** directions. This differs from a Schwarzschild horizon, where inward radial characteristics remain while outward ones cannot escape. Continuous-time nearest-neighbour hopping also has nonzero short-time tails at arbitrary finite graph distances (leading order t^d). This is not an exact light cone, even if an emergent continuum cone or Lieb–Robinson bound is possible. A physical causal completion requires more than changing the clock rate or cutting links. Directional characteristic transport is a discriminating target, not a justification for inserting nonreciprocal hopping ad hoc.

### 6. GR and information benchmarks (not GFD derivations)
With c=G=1, in a flat spatial slicing with unit lapse and inward radial shift v, the GR Hamiltonian constraint uses `K²-K_ij K^ij = 2 (r v²)'/r²`. It gives `v²=2M/r` outside spherical matter. The static clock rate is sqrt(1-v²) only outside the horizon; the PG slicing lapse itself is 1. Radial characteristics are `-v ± 1`, and the radial metric determinant remains -1 at v=1. Infalling normal worldlines remain timelike. The signed isotropic Schwarzschild Killing lapse `(u-1)/(u+1)` flips under u→1/u, while R/a=u+2+1/u is invariant with minimum 4. This matches GFD's Möbius algebra but does not identify acceleration ratio x with isotropic radius u. The horizon is not a curvature singularity; a classical bridge is nontraversable. No new universe or topological change is simulated or proven.

The ratio of the Bekenstein entropy-bound expression to the spherical black-hole area-entropy expression is `2GE/(Rc^4)`. Equality at Schwarzschild compactness one is an algebraic benchmark, not a generic theorem that arbitrary matter saturates either bound. Energy is not bit count: equally entropic finite-state systems can have different energy. The same mass at different radii has different compactness. Processing load alone without spatial scale is insufficient. Relativistic time dilation does not increase local proper-time capacity within a fixed external interval.

### 7. AQUAL and recursive accounting remain separate
The drained AQUAL response `J=x²/(1+x)` describes partition of an existing drive. Acceleration x falls as r^-2 in the Newtonian spherical limit, unlike compactness r^-1. Do not identify them. Static hierarchical Schur elimination composes with transformed sources; retaining the original alongside the replacement double counts. This does not establish that a horizon creates a new independent execution domain, only that exact effective source registration is possible in the prescribed graph model.

## Next research gates before a proof
- Derive the time-face work vertex from the native nonlinear vortex action, and test it against hidden energy states without assigning it by hand.
- Derive an energy reference/scale that includes binding energy and yields universal mass coupling.
- Derive a dynamical clock/shift degree of freedom with an actual causal principal symbol and source response, rather than only a static inverse Laplacian.
- Demonstrate a directional horizon and regular interior evolution without setting microscopic proper time to zero.
- Derive the relationship to GFD's tree-level G normalization and drained AQUAL versus drainless Newton/GR rule. No fit.

## Reproduce
Python 3 with numpy, scipy, sympy and pytest. Run `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m pytest -q`. `verification.txt` is the actual recorded run. Tests deliberately include counterexamples to overstrong claims; passing is not a claim of physical proof.

## Source register
- [Native coupled origins and H36 construction](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/verify_coupled_origins.py)
- [Dynamic tetrad observability and flat dark modes](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/DYNAMIC_TETRAD_SETTLEMENT.md)
- [Spectral gravity read](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/SPECTRAL_GRAVITY_READ.md)
- [Field Origin gravity read](https://github.com/fielddynamics/research/blob/main/research/hadamard-null-cone-vortex-flywheel/FIELD_ORIGIN_GRAVITY_READ.md)
- [Proof 26 and sources](https://github.com/fielddynamics/research/tree/main/proofs/recursive-field-closure-response)
- [AQUAL energy](https://github.com/fielddynamics/research/tree/main/proofs/aqual-energy-functional)
