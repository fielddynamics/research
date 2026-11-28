# Source register — pinned research repository

[Back to README](README.md)

Repository: [fielddynamics/research](https://github.com/fielddynamics/research), revision [`3a13b00666b90bbc63d54d33094cab7cc13986c7`](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7). The paths below refer to that revision. This is an annotated cross-repository reading, not a republication of all documents. The original folder is [research/aqual](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/research/aqual). Its six exact blob identifiers are in `upstream/original_manifest.json`; use `restore_upstream.py` to make a local copy. The new package chapters incorporate the main relevant mathematical results, not every line of the entire repository. No claim is made to have read every unrelated paper, script, binary or historic revision.

## Formal proof chain

| Key | Pinned original | Role | Reported upstream checks (not rerun) |
|---|---|---|---:|
| P-exchange | [Constitutive law from exchange](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/constitutive-law-exchange-symmetry) | Conditional uniqueness | 34 |
| P-aqual | [AQUAL energy functional](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/aqual-energy-functional) · [Lean audit](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/aqual-energy-functional/LEAN_AUDIT.md) · [Lean code](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/aqual-energy-functional/lean/AqualEnergy.lean) | Primitive, limits, convexity, ellipticity, uniqueness | 24 |
| P-tug | [Tug of war](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/constitutive-law-tug-of-war) | Strength interpretation and decoder | 42 |
| P-bimond | [Two-potential energy](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/bimetric-two-potential-energy) | Legendre dual | 39 |
| P-lock | [Bimetric lock](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/bimetric-lock-constitutive-law) | Lock alone does not fix acceleration odds | 64 |
| P-sst | [Quasi-static SST](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/sst-quasi-static-limit) | Source, lapse slip, static response, double-counting | 26 |
| P-timeleg | [Covariant time leg](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/sst-covariant-time-leg) | Nonnegative covariant y | 16 |
| P-khronon | [Preferred-frame effects](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/sst-khronon-preferred-frame) | Selected stability inequalities and net-field frame | 32 |
| P-netfield | [NET Field rule](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/net-field-rule) | Which field receives μ | 122 |
| P-mountain | [Mountain-scale action](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/sst-mountain-scale) | Ownership, shell, interface, nested sweeps | 36 |
| P-closure | [Closure surface](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/closure-surface) | Tidal/stagnation boundary | 16 |
| P-response | [Proof 26: recursive response](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/proofs/recursive-field-closure-response) | Signed counts and conditional G expression | 532 (+568 appendix) |

Counts above are as recorded in the [Coles Notes](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/GFD_COLES_NOTES.md), not summed into a new verification claim. Read each audit for scope and cited mathematical steps.

## Research notes and explanatory papers

| Pinned location | Integration into this folder |
|---|---|
| [Original AQUAL algebra](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/research/aqual/aqual_algebra_further.md) | Ch. 1–4: logistic family, exchange, hyperbolic forms, density, operator traces |
| [Original docs critique](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/research/aqual/docs_and_the_energy_functional.md) | Ch. 8: audit and later resolutions |
| [Einstein as TetA partition](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/EINSTEIN_TETA_PARTITION.md) | Ch. 1, 5, 6: roots, 40/24, local law |
| [Closure of Closures](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/CLOSURE_OF_CLOSURES.md) | Ch. 6–7: recursive registration, Newtonian scope and drained gap |
| [Constitutive-law research](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/research/constitutive-law-u(x)) | Supplementary test and visualization location |
| [Bound gravity](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/research/bound-gravity-and-packing) | Ch. 4: bound law and binding interpretation |
| [BIMOND–GFD comparison](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/research/bimond-gfd) | Ch. 4: duality and first-order vs gradient auxiliary |
| [Two connections / dual chamber](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/research/two-connection-dual-chamber) | Ch. 4: deformed leg, odds and missing physical dynamics |
| [READ–SETTLE–REGISTER bridge](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/research/read-settle-register-bridge/READ_SETTLE_REGISTER_BRIDGE.md) | Ch. 7: finite capacity, auxiliary torsion and drained-child junction |
| [Constitutive vertex](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/research/hadamard-null-cone-vortex-flywheel/vertex-research/CONSTITUTIVE_VERTEX.md) | Ch. 7: conditional finite Hamiltonian saturation |
| [Three-sweep algebra](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/research/3%20sweep%20understanding) | Ch. 1, 7: structural count vs read schedule |
| [RAR letter](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/papers/letter-radial-acceleration-relation-sparc) | Ch. 3: reported SPARC recipe and scatter |
| [Mass decoding letter](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/papers/letter-decoding-mass-from-rotation-curves) | Ch. 3: inverse and residual |
| [Constitutive law letter](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/papers/letter-constitutive-law-tetrad-geometry) | Ch. 1: three derivation routes (indexed by original README) |
| [Closed-form AQUAL paper](https://github.com/fielddynamics/research/tree/3a13b00666b90bbc63d54d33094cab7cc13986c7/papers/closed-form-aqual-energy-functional) | Ch. 2: earlier integral, corrected by P-aqual |
| [Docs: field equation](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/docs/02-gravitation/02-field-equation.md) · [constitutive law](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/docs/02-gravitation/03-constitutive-law-mu-x.md) | Ch. 1, 3, 8 |
| [Docs: Poisson](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/docs/02-gravitation/05-poisson-scale-invariance.md) · [covariant completion](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/docs/02-gravitation/06-covariant-completion.md) | Ch. 2, 5, 6 |
| [Characteristic scale](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/docs/01-foundations/07-characteristic-scale.md) · [H₀](https://github.com/fielddynamics/research/blob/3a13b00666b90bbc63d54d33094cab7cc13986c7/docs/03-fundamental-constants/05-h0-prediction.md) | Ch. 8: two normalizations |

Related paper directories (mapped from original README, not independently read in full): Paper VII v7 dual tetrad topology; Paper VIII bimetric gravity; Paper XIII bidirectional SST; Letter 3 field closure of the tetrad frame. The external docs-site test audit is taken from the original notes; the separate docs repository has not been rescanned in this session.

## Foundational literature referenced by the repository

- Bekenstein & Milgrom, 1984, *Does the missing mass problem signal the breakdown of Newtonian gravity?*, ApJ 286, 7. AQUAL.
- Milgrom, 1983, MOND series, ApJ 270; Milgrom, 2010, QUMOND, MNRAS 403, 886.
- Famaey & Binney, 2005, *Modified Newtonian dynamics in the Milky Way*, MNRAS 363, 603. Simple interpolating function.
- Milgrom, 2009, bimetric MOND, [arXiv:0912.0790](https://arxiv.org/abs/0912.0790).
- Blanchet & Marsat, 2011, preferred time foliation, [arXiv:1107.5264](https://arxiv.org/abs/1107.5264).
- McGaugh, Lelli & Schombert, 2016, RAR, PRL 117, 201101.

These are literature references identified through the repository and standard mathematical context, not a separate literature systematic review.
