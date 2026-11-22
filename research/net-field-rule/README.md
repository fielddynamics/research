# The Net-Field Rule

*Research folder, Field Dynamics Research, 2026-11-20. Status: proved as [`proofs/net-field-rule/`](../../proofs/net-field-rule/) (four-page proof, 122 checks, Lean). Tests: `python -m pytest -q test_net_field_rule.py` (122 tests, about 6 s; numpy, scipy, sympy, pytest).*

---

## The question

The [tug-of-war proof](../../proofs/constitutive-law-tug-of-war/) showed why the constitutive law is μ(x) = x/(x + 1). It left open which field the law acts on. Applied to every field, including each star's own, it fails in the solar system, and the [SST time-leg proof](../../proofs/sst-covariant-time-leg/) names this as the step still to be made precise. This folder makes it precise.

## The picture

A solar system is a rubber sheet with a bowling ball on it, sitting in the galaxy's net field. The ball, the Sun, has a TetB, enclosed in it and counted in its GM. The sheet, the solar system's field, has no drain. A galaxy's field is a funnel whose throat opens into occupied TetB, and that field has a drain (Stephen Nelson, 2026-11-20).

## Premises

- **(D) Drain criterion.** A drain belongs to a field, not to a body. Every body has its own TetB, enclosed within it and counted in its GM. A field carries a TetB share, and μ acts on it, only if the field itself has a drain. A galaxy's field has one; the field of a star system, a binary or a star cluster does not.
- **(N) Net field.** In a drained field, x = |g_net|/a₀ with g_net that field's own net field, coarse-grained on the tidal (Jacobi) scale ℓ = r_J of each bound system. The scale is motivated by elimination (Part 30), not derived.
- **(A) TetA is GR.** A drainless field is the TetA connection: Newton and GR with the bare G.

## The theorem in one line

μ acts only on a field with a drain. A drainless field is TetA with the bare G inside its Jacobi radius, its host reaches it only through free fall and a tide-level residual, and every body's TetB stays enclosed in its GM.

**In plain terms:** inside a star system, gravity is exactly Newton and GR, with the bare G. The galaxy's only influence is its tide, which every model shares. The alternatives that would change G or add a pull around the Sun are ruled out: Cassini rules out the extra pull, and globular clusters rule out a changed G.

## What the tests establish

The 29 parts of [`test_net_field_rule.py`](test_net_field_rule.py) fall into three groups.

**What the rule says, as algebra.**
- Four faces of "no drain" are one property: a linear law, an identity response (bare G), flux conserved across empty shells, and no TetB share. Each is a rational function of μ that vanishes only at μ = 1 (Parts 16–18, 20, 22).
- The flux exponent is s = 2(1 − μ)/(2 − μ), and f(u) = 2(1 − u)/(2 − u) is an involution, so beyond the baryons a rotation curve's slope alone gives μ, x and a₀. In the standard family μₙ = x/(1 + xⁿ)^{1/n} only n = 1 has this property (Parts 21, 26).

**Why it is consistent.**
- The split is an identity; outside a non-spherical sheet only its own quadrupole and higher multipoles remain, falling as r⁻⁴ (Part 29). Predictions well inside the sheet do not depend on the edge's shape (Part 30).
- The rubber sheet is the two-scale split g = F[g_N(Pρ)] + g_N(ρ − Pρ), an identity in which the rule decides which term goes through F. The pointer projection P is idempotent and nested, the sheet's own term has no monopole or dipole outside its edge (and vanishes there for a round sheet), the host's uniform field drops out in free fall, and the sheet's own pointer exerts no net force for any host response (Parts 4, 10, 13, 19, 23).
- The sheet's edge is the Jacobi radius, about 1.4 pc, where the residual is the tide's size by construction (Part 14).
- Every body's TetB is enclosed, screened to about 4 × 10⁻¹³ at the Sun's surface, dominant only in a micron-sized core at the centre, and bounded by the ephemerides' limit on changes in GM (Parts 1, 15, 28).

**What the data rule out, and what they confirm.**
- A drain around every star fails for every exchange-symmetric law with flat curves, with a pull of nearly a₀ at every planet and a quadrupole of 4.6 × 10⁻²⁶ s⁻², five times Cassini's bound (Parts 2, 3).
- The galactic tide that remains is about 8 × 10⁻³¹ s⁻², four orders below Cassini (Part 5).
- A host factor on G is invisible to orbits but not to globular clusters, which require the bare G at 8.9σ and 11.1σ (Parts 6, 7, 17).
- Cassini places the sheet's edge beyond about 12,000 AU, and binding caps it at 290,000 AU (Part 25).
- With ℓ = r_J, bound wide binaries are predicted Newtonian to within 0.53(s/ℓ)³, below 10⁻⁴ at 20 kAU; a boost growing as s³ would instead measure ℓ (Parts 11, 31).
- An a₀-free test of the law's shape on SPARC: the RAR's local slope matches 1/(2 − μ) to 0.053 rms, against 0.102 for the standard law, in 200 of 200 bootstraps (Part 27).

## Open

- An observable marker of a drained field that does not use its rotation curve. The four faces say what it must measure: flux growth across empty shells.
- ~~The covariant derivation of which time leg's acceleration enters μ.~~ Done in [`proofs/sst-mountain-scale/`](../../proofs/sst-mountain-scale/): the law's term read at the mountain's scale (each system's Jacobi radius) gives this split from the action.
- The slope test on SPARC's outer radii, which needs per-radius rotation curves.
- Whether the closure at the Field Origin and the zero flux at the sheet's edge are the same boundary condition.

## Related

- [`proofs/net-field-rule/`](../../proofs/net-field-rule/): the proof, its script and the Lean formalisation.
- [`research/bimetric-projection/`](../bimetric-projection/), Part 3: the first solar-system probes.
- [`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md): local systems are TetA only.
