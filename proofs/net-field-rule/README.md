# The Net-Field Rule: Where the Constitutive Law Acts

*Why the solar system obeys Newton and Einstein exactly while its galaxy obeys μ(x) = x/(x + 1), and what that rule predicts for star clusters, dwarf galaxies and wide binaries · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`net-field-rule` `constitutive-law` `MOND` `external-field-effect` `solar-system` `Cassini` `globular-clusters` `wide-binaries` `proof` `Lean`

[![Lean proof](https://github.com/fielddynamics/research/actions/workflows/lean-net-field-rule.yml/badge.svg)](https://github.com/fielddynamics/research/actions/workflows/lean-net-field-rule.yml)

---

This folder holds a four-page proof, a script that checks every statement in it (116 checks), and a Lean formalisation of its algebraic core. The working tests it grew from are in [`research/net-field-rule/`](../../research/net-field-rule/). The [tug-of-war proof](../constitutive-law-tug-of-war/) showed why the law has the form it does. This one answers the question that proof left open: which field the law acts on.

## The short version

Inside a star system, gravity is exactly Newton and general relativity, with the bare G. The galaxy reaches the system only through its tide, which every model of the galaxy shares. The alternatives that would change G or add a pull around the Sun are ruled out: Cassini rules out the extra pull, and globular clusters rule out a changed G.

## A bowling ball on a rubber sheet

Picture the solar system as a rubber sheet with a bowling ball on it, and the whole sheet sitting in a stream that runs gently downhill. The ball is the Sun. The dent it makes in the sheet is what the planets roll around in, and the stream is the galaxy's net field, carrying the sheet along with it.

Three things in that picture carry the whole rule. The ball has a TetB of its own, but the TetB is inside the ball, so from the sheet all you can see is how heavy the ball is, its GM. The sheet has no drain: it is a dent with a bottom, not a funnel with a hole, so nothing flows through it into a TetB chamber, and the constitutive law has nothing to act on. A galaxy's field is different, because it is a funnel whose throat opens into TetB, and it is there, and only there, that μ acts. The proof states this as its premise: **a drain belongs to a field, not to a body**.

## Why the obvious alternative fails

The simplest reading would apply μ to every field, including the Sun's own. The proof shows that this is not merely wrong for our law but wrong for every law of its kind. Exchange symmetry says that μ(1/x) = 1 − μ(x), and flat rotation curves say that μ(x) ≈ x when x is small. Put together, they force the TetB share far from a star to fall off as exactly 1/x, so that every star is surrounded by an extra pull of almost exactly a₀. That pull would act on every planet alike. It cannot be absorbed into the Sun's GM, because it does not fall off as 1/r², and in the galaxy's field it would distort the Sun's field into a quadrupole of about 4.6 × 10⁻²⁶ s⁻², five times what the Cassini spacecraft allows. This is the failure that has troubled the AQUAL form of MOND in the solar system. The net-field rule avoids it by never applying μ to a star's own field in the first place.

## Four ways of saying "no drain"

The proof's central theorem finds that four properties of a field, which look unrelated, are the same property. A field has no drain exactly when its law is linear, so that fields simply add; exactly when a body inside it responds with the bare G; exactly when its flux is conserved across empty space, which is Kepler's law; and exactly when it carries no TetB share. Each of the four is a simple function of μ alone, and each vanishes only at μ = 1. A drained field fails all four together: fields no longer add, a guest feels a boosted G, the flux grows outward as r^s with s = 2(1 − μ)/(2 − μ), and the extra flux is the mass that has been called dark matter.

The flux exponent has a property that surprised us. The map that sends μ to s, f(u) = 2(1 − u)/(2 − u), is its own inverse, so the same map sends a measured s back to μ. Beyond a galaxy's visible matter, the slope of its rotation curve therefore gives μ, then x, then a₀, with no mass model at all. Among the standard family of MOND laws, only x/(x + 1) has this property.

## The sheet in equations

The rubber sheet becomes exact when the field is split into two terms. The first is the galaxy's drained field, computed from the galaxy's mass with each star system replaced by a uniform ball of the same total mass, which we call its pointer. The second is the star system's own field minus its pointer, and it obeys the plain, linear law with the bare G. Newton's shell theorem makes this second term vanish identically outside the sheet, so nothing is counted twice and the galaxy sees each star system as a single mass at a single point. Every galactic prediction is unchanged by the split.

Inside the sheet, the galaxy's uniform pull drops out of every relative motion because the whole system falls together. The sheet's own pointer cannot push it, whatever form the galaxy's response takes, because its force sums to zero about the centre of mass. What remains is the galactic tide, the slight bending of the stream across the sheet, which is about 8 × 10⁻³¹ s⁻² at the Sun and about 10⁻¹⁸ m/s² at Saturn, four orders of magnitude below the Cassini bound. The tide is set by the Milky Way's rotation curve alone, so general relativity with a dark halo predicts the same number.

## Where the sheet ends

The data fix the sheet's edge from both sides. Cassini requires it to lie beyond about 12,000 AU, roughly 1.7 times the distance at which the Sun's own pull falls to a₀; a sheet that ended at that ring would be the per-star reading again. Binding caps it at the Jacobi radius, the distance at which the galaxy's tide takes over from the Sun, about 1.4 parsecs or 290,000 AU. The Jacobi radius is fixed by the galaxy alone and needs no free parameter. Because both limits grow as the cube root of the star's mass, the same window exists for every star at the Sun's distance from the galactic centre.

## What the data say

Orbits cannot tell the bare G from a G rescaled by the galaxy, because Kepler's law only ever measures the product GM. Star clusters can, because their masses come from counting starlight. The remote globular clusters Pal 14 and Pal 4 sit at accelerations around a tenth of a₀, where a rescaled G would make their stars move about three times faster. Their stars move as Newton predicts, within 1σ, and the rescaled version is excluded at 8.9σ and 11.1σ. The dwarf galaxy Crater II sits at the same low acceleration in the same host, yet its stars move 5.4σ faster than Newton allows and within 2.2σ of μ. No rule that depends only on acceleration fits the clusters and the dwarf together, while the drain criterion, which treats the clusters as closed and the dwarf as open, fits all three with no free parameter.

The rule makes a sharp prediction for wide binary stars. Every bound pair should be exactly Newtonian at every separation, including the widest pairs, whose own pull falls below a₀ beyond about 10,000 AU. Rules that depend only on acceleration predict a boost in the pull of 17 to 47 percent between 5,000 and 20,000 AU. The data on wide binaries are currently disputed, and the rule takes a clear side.

A second test checks the shape of the law itself. The local slope of the radial acceleration relation should equal 1/(2 − μ), and because both sides are measured, the test needs no value of a₀. On 163 SPARC galaxies, GFD's shape misses the measured slope by 0.053 and the standard MOND law's by 0.102, and GFD's wins in every one of 200 resamplings of the galaxies.

## What is proved, assumed and measured

The drain criterion and the net-field rule are the framework's premises, as stated in [`EINSTEIN_TETA_PARTITION.md`](../../EINSTEIN_TETA_PARTITION.md) and Part 3 of the [bimetric-projection note](../../research/bimetric-projection/). The proof derives their consequences exactly and tests them against the data they must meet. Three points remain open. The first is a way to recognise a drained field without using its rotation curve, and the four faces say exactly what such a marker must measure: growth of flux across empty space. The second is the covariant derivation of which time leg's acceleration enters μ, which the [SST time-leg proof](../sst-covariant-time-leg/) leaves open. The third is the dwarf Antlia 2, which no rule tested here fits, possibly because it is being tidally disrupted.

## Machine-checked in Lean

The [`lean/`](lean/) folder proves the proof's algebraic core in [Lean 4](https://lean-lang.org) with [Mathlib](https://github.com/leanprover-community/mathlib4), and it imports the constitutive law and the exchange from the [tug-of-war proof](../constitutive-law-tug-of-war/) rather than restating them. Twenty theorems are checked, each using only Lean's three standard axioms.

- **The four faces and the dictionary**: the drained law inverts as stated; every face is a function of μ that vanishes only at μ = 1; the drained law is strictly subadditive; a guest's two responses exceed 1 at every finite field; and the flux exponent is 2(1 − μ)/(2 − μ).
- **The involution**: f(f(u)) = u, and the corresponding map for the standard law is not an involution.
- **The forced failure**: the extra pull around a star lies between μa₀ and a₀, and for every exchange-symmetric law with the deep-field limit, x(1 − μ(x)) tends to 1.
- **The rubber sheet**: free fall, the centre of mass falling with the host, no self-force for any linear response, the sheet's own term vanishing outside its edge and continuous at it, Kepler's law absorbing a factor on G, the flat-curve tide and the Jacobi radius.
- **The Sun's TetB**: the screening law, the micron-sized core and the bound on the screened mass.

The Cassini quadrupole integral and the data tests are checked by the script. [`LEAN_AUDIT.md`](LEAN_AUDIT.md) is a referee's guide to the formalisation.

## Contents

| File | Contents |
|---|---|
| [`net_field_rule.pdf`](net_field_rule.pdf) | The proof (four pages, including references) |
| [`net_field_rule.tex`](net_field_rule.tex) | LaTeX source |
| [`verify_net_field_rule.py`](verify_net_field_rule.py) | 116 checks of every statement (numpy, scipy, sympy, pytest) |
| [`verify_output.txt`](verify_output.txt) | The script's output |
| [`lean/NetFieldRule.lean`](lean/NetFieldRule.lean) | The Lean 4 formalisation |
| [`lean/lakefile.toml`](lean/lakefile.toml), [`lean/lean-toolchain`](lean/lean-toolchain), [`lean/lake-manifest.json`](lean/lake-manifest.json) | Project files: Lean 4.36.0, Mathlib v4.36.0, and the seven formalisations it imports |
| [`LEAN_AUDIT.md`](LEAN_AUDIT.md) | Referee's guide to the formalisation |
| `iopjournal.cls` | Journal class file |

## Reproduce

```bash
python verify_net_field_rule.py

pdflatex -jobname=net_field_rule '\providecommand\ead[1]{\email{#1}}\input{net_field_rule.tex}'

# Lean (needs elan: https://github.com/leanprover/elan)
cd lean
lake exe cache get    # downloads Mathlib, already compiled
lake build            # checks every theorem, and the proofs it imports
```

The SPARC test reads [`papers/letter-radial-acceleration-relation-sparc/supplementary/sparc_rar.csv`](../../papers/letter-radial-acceleration-relation-sparc/supplementary/sparc_rar.csv) and is skipped if the file is absent.

## Related

- [The constitutive law as a tug of war](../constitutive-law-tug-of-war/): why the law is x/(x + 1); this proof says where it acts.
- [The SST covariant completion](../sst-covariant-time-leg/): the covariant form of y, and the per-mass tail this rule removes.
- [Einstein's equation as the TetA partition](../../EINSTEIN_TETA_PARTITION.md): local systems are TetA only.
- [Bimetric projection, Part 3](../../research/bimetric-projection/): the solar-system probes and the cluster–dwarf test.
- [The net-field research folder](../../research/net-field-rule/): the 116 tests in their working form.
