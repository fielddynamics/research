# Unified closure action: illustrated research

This folder collects three stages of research on geometric π addressing, closure settlement and the gravitational read. The current [recursive Triforce geometry](../recursive-triforce-geometry/) supplies the primary candidate geometric hierarchy; the stage Markdown documents are corrected in place to distinguish it from the ordered-pair and Pauli representations. Historical numerical outputs, figures and generated HTML snapshots are retained; the corrected Markdown takes precedence.

| Stage | What it adds | Main document | Verifier |
|---|---|---|---|
| I. Three-subcycle settlement | Three-level address geometry, weighted boundary conservation, 21 contrast modes, conditional gravitational and electron closure; H36 spectral stiffness, the 21/17/13 exchange traces, the balanced face-pair read and Walsh invariance | [`research/WEIGHTED_CLOSURE_SETTLEMENT.md`](research/WEIGHTED_CLOSURE_SETTLEMENT.md) and [`research/MICROSCOPIC_STIFFNESS_DERIVATION.md`](research/MICROSCOPIC_STIFFNESS_DERIVATION.md) | `verification/verify_weighted_closure.py`, `verification/verify_microscopic_stiffness.py` |
| II. Unified closure action | Three commuting subcycles whose invariant determinants give α, α⁴ and α¹⁶ (product α²¹), one odds variable for both constitutive responses, a common static generating action, recursive registration with exact charge composition, and the causality and coupling problems still open | [`unification/UNIFIED_CLOSURE_ACTION.md`](unification/UNIFIED_CLOSURE_ACTION.md) | `unification/verify_unified_closure.py` (43 checks) |
| III. Octal π sweep and gravity | The BBP circular transfer function, circular addressing and binary phase operations, exact settlement after address coverage, angular averaging to the first surviving multipole, and three circular sweeps as projection operators | [`pi_sweep_extension/PI_SWEEP_GRAVITY_BRIDGE.md`](pi_sweep_extension/PI_SWEEP_GRAVITY_BRIDGE.md) | `pi_sweep_extension/verify_pi_sweep.py` (70 checks) |

## Reading order

1. [`COMPLETE_ILLUSTRATED_RESEARCH.md`](COMPLETE_ILLUSTRATED_RESEARCH.md) (or its offline [HTML edition](COMPLETE_ILLUSTRATED_RESEARCH.html)) brings all three stages together in one illustrated document: Part I is stage I, Part II is stage II, Part III is stage III, and Part IV adds further visuals.
2. The stage documents in the table above, for the full derivations.
3. [`VISUAL_MATHEMATICAL_COMPANION.md`](VISUAL_MATHEMATICAL_COMPANION.md) (or its offline [HTML edition](VISUAL_MATHEMATICAL_COMPANION.html), with the interactive closure-balance slider) is the original stage I companion.
4. [`START_HERE_UNIFICATION.md`](START_HERE_UNIFICATION.md) is the stage II entry note.

## Figures

[`VISUAL_ATLAS.html`](VISUAL_ATLAS.html) shows all 27 numbered diagrams. Each is an SVG with a PNG copy:

- `diagrams/` (01–09): the stage I engine, address tree, attenuation, solid angles, face-pair exchange, closure balance and stiffness.
- `unification/` (10–14): unified response, scalar causality, three-grade closure, common generator and architecture.
- `pi_sweep_extension/` (15–17): π transition ledger, three-sweep isotropization and the BBP circular clock.
- `additional_visuals/` (18–27): I Ching trigram cube and hexagram wheel, paired binary reads, three-axis sector sweeps, binary carry circuit, angular averages, time-axis quotient, recursive boundary registration, π–Walsh feedback and phase sweep.

Redraw scripts: `diagrams/regenerate_diagrams.py`, `unification/regenerate_architecture.py` and `additional_visuals/regenerate_additional_visuals.py`.

The diagrams are reconstructions of concepts, not screenshots. The stage I reference photograph (the 2008 Barbury Castle π crop formation) is third-party and is not reproduced here. The three-circle interpretation of it is a GFD hypothesis, not evidence of a physical field mechanism.

## Reproduce

With Python 3 and NumPy, from this folder:

```sh
python verification/verify_weighted_closure.py
python verification/verify_microscopic_stiffness.py
python unification/verify_unified_closure.py
python pi_sweep_extension/verify_pi_sweep.py
```

All four pass and match their recorded logs (`verification/*_output.txt`, `unification/verification_output.txt`, `pi_sweep_extension/verification_log.txt`). They verify the stated mathematical constructions, not independent empirical predictions.

## Status

The coupling polynomial gives the 17/13 trace ratio that G's combination rule uses; reading it as a physical stiffness ratio in this model is not independently derived. The [root-exchange note](../g_from_topology/read-and-rotation/ROOT_EXCHANGE_ON_THE_ADDRESS_TREE.md) determines a time-adapted flag for the computational projective representation, not the sign grading of the recursive geometry. The [recursive Triforce geometry](../recursive-triforce-geometry/) has a conditional fixed-lattice depth of two, a 40/24 pointing split, a symmetry obstruction to direct corner-pair identification and a corrected radial solid-angle quadrature. Keep geometric addresses, structural traces, source weighting and attenuation distinct.

Exact identities, conditional constructions and open physical proof obligations are labelled throughout. Still open: native physical selection of the balanced π walk, the attenuation, dimensional normalization, the native H36 dynamics, physical charge, spin-2 and the full covariant completion. The related syntheses are in [`../3 sweep understanding/`](<../3 sweep understanding/>) and the vortex-flywheel model in [`../hadamard-null-cone-vortex-flywheel/`](../hadamard-null-cone-vortex-flywheel/).
