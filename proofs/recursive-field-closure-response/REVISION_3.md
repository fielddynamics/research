# Revision 3 — origin-centred projective read

This revision responds to the objection that Theorem 9 previously selected both a trace-free register and a divisor of 16. The original revision remains separately available.

- Theorem 9A derives the 17-line pencil and its 16-point fibres; the normalization of its incidence projector is forced by idempotence.
- Theorem 9B obtains the ratio of the pencil and Baer projector ranks, 17/13. This replaces the old normalized-trace construction as the primary geometric witness. The actual Baer/pencil intersection pattern is derived and verified for every projective centre.
- Theorem 9C compares point and trace exclusion and retains the older norm compression as an alternative. Equal traces and spectra do not imply equal operators.
- Theorem 10 uses a pencil-projector determinant perturbation with equal Baer-sector normalization. Its first derivative agrees with the old witness; its second derivative differs. The comparison is conditional on the same perturbation scale.
- The native action must still select the marked point, the two incidence reads, their rank ratio, the complete-frame source and the elementary electromagnetic gain. No physical trace-free premise is now required by the new construction. No claim of a uniquely forced physical normalization.

## Verification

532 prior exact assertions rerun; 568 new exact incidence assertions passed (including all 273 pencil centres and all 273 punctured Baer incidence signatures). Total 1,100 freshly counted checks. The finite-field source builder is also executed by the new verifier, but its own checks are not counted again. 1,352 historical inherited assertions preserved rather than rerun. No new Lean compilation or independent peer review.

Run `python verify_proof26.py` and `python verify_projective_pencil.py`. Run `python make_pencil_figure.py` to regenerate the exact incidence figure (requires matplotlib). The new interactive page presents the fixed incidence matrix and two response curves; it is not a native Hamiltonian simulation.

The new interactive page passed five JavaScript checks in a simulated DOM (row and column counts, reference state, distinct response values and generated ledger). Full browser rendering was not performed. The PDF was compiled twice, rendered and visually inspected; the source hashes remain unchanged.
