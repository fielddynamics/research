# Audit of the legacy antenna files

The two original files are preserved byte-exact in `../legacy/`. This audit says which of their claims stand, which are analogies, and which conflict with the framework's own positions or with the literature. Nothing here changes the legacy files.

## `resonant_coupling_field_origin.md`

| Claim | Verdict |
|---|---|
| 64 addresses, gate-depth counts 27/27/9/1 | **Stands [T].** Binomial C(3,d)·3^(3−d), sum 4³ (tested). |
| Gasket keeps 3 of 4 children, but the address space counts 4ⁿ | **Clarify.** The physical gasket (3ⁿ) and GFD's complete ledger (4ⁿ, gate kept) are distinct constructions (tested). |
| Inner octahedron has 9 edges (6 vertical + 3 equatorial) | **Incorrect.** A regular octahedron has 12 edges (V−E+F=2 with V=6, F=8). The E(3)+B(3) wiring argument cannot rest on this count. |
| 64 subchannels are 64 photons; 128 photonic states | **Open [H].** The framework has not settled whether the gravity stellated octahedron holds 64 photons. |
| s(x) = (x−1)/(x+1) is the sector state; x→0 is TetB | **Conflicts with the framework.** s is a discrete state label (s=−1 is TetB). The continuous share difference (x−1)/(x+1) tending to −1 in the deep field is not TetB. The deep-field regime must not be equated with TetB. |
| μ(x) = (f(x)−13)/8 = x/(x+1); μ(x)+μ(1/x)=1; x(1−μ)=μ | **Algebra stands [T].** Read as the kinematic TetA partition, not as a passage of a signal through the origin. |
| "The field origin emerges in the electromagnetic space between" two separated structures | **Superseded.** The current position is non-spatial: the Field Origin is a nonlinear vertex, not a region of space between structures. See `NONSPATIAL_RESONANCE_FIELD_ORIGIN.md`. |
| 1/α = 128 + 9 + 1/28 | **Candidate, not derived.** Depends on the 9-edge count above. |
| Bands f_n = 2ⁿ f₀, f₀ = c/(2a√ε) | **Bands stand as engineering fact** (dyadic log-period on real gaskets). The f₀ formula is a generic half-wave estimate, not a GFD result. |
| m+n+l=0, fundamental (1,0,−1), k = 4π/(3a) | **Properties of a triangular resonator's modes.** k = 4π/3a equalling Kπ/D only says K/D = 4/3. |
| Möbius function μ(n) values ↔ three polynomial states | **Analogy only.** |
| BBP / 333-digit walk | Covered more carefully in `research/3 sweep understanding/`. |

## `twenty_antenna_tests.py`

The script runs and prints 20 PASS lines. Most "tests" compare a constant with itself, so they cannot fail:

| Tests | What they actually check |
|---|---|
| 1, 2, 4, 9, 14, 16, 19 | Assigned constants equal assigned constants (e.g. `2 == 2`). Not tests of the claim. |
| 3 | 4 = 1 + 3. The paper's choice of C0–C3 is a design choice; Puente's monopole used five iterations. |
| 5–8, 18 | **True identities** of the gasket (3ⁿ, 4ⁿ, (3/4)ⁿ, (1/2)ⁿ, perimeter growth). |
| 10 | 2³ = 8. True; the band span depends on the number of iterations built. |
| 11 | μ(x) is in (0,1). True, but unrelated to antenna bandwidth; Sierpiński antennas are multiband, not broadband. |
| 12 | 1/4ⁿ decreases. True; not derived from antenna physics. |
| 13 | Asserts `0 == 0`. Also, the face normals that sum to zero are four, not three. |
| 15 | 4π/3 = 4π/3. |
| 17 | Asserts 64 photons (see above). |
| 20 | 1+4+16 = 21. True; the mapping to feed/faces/channels is an analogy. |

**Kept for record, superseded by** `tests/test_antenna_engine.py`, where every test can fail.

## Related file outside this folder

`research/g_from_topology/read_sweep_synthesis.md` says 2/17 "has been measured" in the Sierpiński antenna. No such measurement was found (see `SIERPINSKI_ANTENNA_LITERATURE.md` §6). The framework treats 2/17 as an estimate of the screening filter. That file is left unchanged; this is flagged here only.
