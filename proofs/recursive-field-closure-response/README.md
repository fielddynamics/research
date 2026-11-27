# Proof 26 candidate — Gravity as the response of recursive field closure

[![Lean proof](https://github.com/fielddynamics/research/actions/workflows/lean-recursive-field-closure-response.yml/badge.svg)](https://github.com/fielddynamics/research/actions/workflows/lean-recursive-field-closure-response.yml)

**Revision 4 — referee-aware research draft.** Its finite and algebraic theorems are machine-checked in Lean 4: 36 theorems, standard axioms only, importing Proof 23 ([Lean audit](LEAN_AUDIT.md)). The physical premises and the conditional G conclusion are not formalised. The previous topology calculation of G is taken as the target, not as evidence that the physical mechanism has been independently verified. The fixed Triforce/Hadamard architecture accounts for TetB inventory; compatible settlement responds to neighbors; the vortex is the variable state. The proposed collective determinant response reproduces the existing normalization under explicit additional premises.

## Read in order

1. [Inventory of the 25 prior proofs](PROOF_INVENTORY.md)
2. [Build plan](BUILD_PLAN.md)
3. [Proof manuscript](proof26.pdf) ([editable Markdown](PROOF_26.md), [portable LaTeX](proof26.tex))
4. [Referee-style audit](REFEREE_REVIEW.md) and [revision notes](REVISION_4.md) · [Revision 3 history](REVISION_3.md) · [Revision 2 history](REVISION_2.md)
5. [Source register](SOURCE_REGISTER.md)

![Architecture](figures/proof26_architecture.svg)

## Core results

- Theorems 1–2: information-dependent closure and exact susceptibility/Schur complement.
- Theorems 3–6: reversible Walsh read, Sierpiński factorization, invariant dimensions 1/4/16, inventory conservation.
- Theorems 7–8: signed recursive counts, inherited coupling ratio 17/13, conditional collective determinant response.
- Theorems 9–11: exact native fixed-geometry vortex susceptibility in a specified branch, recursive registration, and a conditional Newtonian Green-action completion.

Proof 23's physical pointing and pair-action obstructions are retained explicitly. The candidate is not a claim that P23, P24 or P25 already establish physical attenuation. The 21 is an invariant dimension, not a count of literal time steps or oscillators. The physical selection of the inherited ratio, gain, source vertex and long-wave action remain unproved. The [optional projective appendix](APPENDIX_PROJECTIVE_GEOMETRY.md) preserves all Revision 3 incidence and compression mathematics without requiring any of those operations in the physical model.

## Reproduce

`python verify_proof26.py` (Python 3.10+, NumPy and SymPy); [532 fresh exact assertions (including 40 new revision checks)](verification_output.txt). Run `python verify_projective_pencil.py` for [568 exact appendix incidence assertions](pencil_verification_output.txt). Both suites were rerun in Revision 4, making 1,100 counted checks across the main and optional material; verifier labels retain their historical numbering; the inherited finite-field builder also executes but its checks are not included in that total. In the first candidate revision, seven selected prior verifiers were run again from `sources/`, with outputs in `inherited-checks/`: 1,352 recorded assertions. Do not add the archived totals as fresh results. Use `pandoc PROOF_26.md -s -o proof26.tex` followed by `xelatex proof26.tex` to rebuild the PDF (from this directory). Revision 4 was rebuilt with XeLaTeX and rendered for layout inspection. The previous inherited verification outputs are preserved, not rerun for this revision. No new Lean build or full browser test.

## Visuals

- [Synthesis architecture](figures/proof26_architecture.svg)
- [Packing and Walsh read](figures/packing_walsh_bridge.svg), [Walsh filter](figures/projective_01_walsh_filter.svg)
- [Field tower](figures/projective_03_field_tower.svg), [Baer ledger](figures/projective_04_baer_ledger.svg), [trace compression (earlier witness)](figures/projective_05_trace_compression.svg), [origin-centred pencil incidence](figures/projective_pencil.svg)
- [Fixed vortex](figures/fixed_geometry_vortex.svg), [registration](figures/necessity_02_registration.svg), [Green response](figures/information_02_green.svg)
- Offline: [synthesis explorer](interactive/index.html), [packing](interactive/packing_walsh.html), [projective Walsh](interactive/projective_walsh.html), [vortex susceptibility](interactive/fixed_vortex_response.html). [Origin-centred pencil and response comparison](interactive/projective_pencil.html). These illustrate conditional models, not measured physics.
