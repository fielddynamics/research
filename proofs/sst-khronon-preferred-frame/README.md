# The SST Khronon: Preferred-Frame Effects of the Time Leg

*What the SST's preferred frame does, and why it is safe · Gravity Field Dynamics (GFD) · Field Dynamics Research*

[![Lean proof](https://github.com/fielddynamics/research/actions/workflows/lean-sst-khronon-preferred-frame.yml/badge.svg)](https://github.com/fielddynamics/research/actions/workflows/lean-sst-khronon-preferred-frame.yml)

`SST` `khronon` `preferred-foliation` `PPN` `alpha1` `alpha2` `stability` `net-field-rule` `proof`

---

This folder holds a four-page proof, a script that checks it (24 checks) and a Lean 4 formalisation (13 theorems). It answers the main question the [time-leg proof](../sst-covariant-time-leg/) left open.

## The question

The time-leg proof showed that the SST is a theory with a **preferred time direction**: the tetrad's time leg, normal to a foliation of spacetime (the "khronon"). Theories like that can make the motion of planets depend on how fast the solar system moves through the preferred frame. Experiments limit those effects, written α₁ and α₂, to below about 10⁻⁴ and 4 × 10⁻⁷. Does GFD pass?

## What we found, in plain terms

1. **The textbook formula gives nonsense for GFD, and that's a flaw in the formula.** Plugged into the published formula (Bonetti & Barausse 2015), α₂ comes out infinite, because the SST has no "expansion" or "shear" terms for the time leg. Flanagan (2023) showed that formula's method doesn't apply to theories built this way, and gave one that does.

2. **The preferred frame is the TetB share.** In Flanagan's method, the khronon's mass density is exactly GFD's phantom density, the TetB share. The preferred frame isn't a new ingredient: it is what carries the TetB share, as a conserved fluid.

3. **GFD's law is stable at every acceleration, which is rare.** Flanagan's stability test, read in GFD terms, says that neither μ nor the TetB share may decrease as the field gets stronger. For x/(x+1) the TetB share (in units of a₀) *is* μ, so the two conditions are one, and it holds everywhere. Flanagan argued that laws of this kind fail somewhere near a₀. GFD escapes because its f doesn't level off at high field.

4. **Stability forces the tail.** A law that is stable everywhere must leave every mass with a small leftover pull (the per-mass tail). Of the standard family x/(1+xⁿ)^{1/n}:
   - the "standard" MOND law (n = 2) is unstable above x ≈ 0.79;
   - laws with n < 1 leave a tail that grows without bound;
   - only n = 1, GFD's law, is stable everywhere with a bounded tail.

5. **The net-field rule turns the preferred frame off inside the solar system.** The khronon's inertia and density are both proportional to the TetB share. A drainless field (a star system) has none, so there the preferred-frame sector is empty: **α₁ = α₂ = 0**. Without the rule, the Sun would carry a khronon density about 20,000 times the ephemeris limit at Saturn's orbit. That is the same per-mass tail the rule already removes.

6. **Rotation curves are untouched, and there is a new prediction.**
   - A steadily rotating galaxy is stationary, so every SPARC and decoding-mass result is exact.
   - A changing system (a bar, an interaction) gets an order-unity khronon correction: the TetB share must be carried along and lags a moving pattern.

**In one sentence:** the preferred frame is GFD's TetB share; the law is stable because of the tail; and the net-field rule hides both inside a solar system.

In vortex terms, the frame flow has inertia only where there is TetB share for it to carry. Around a drain there is; in a drainless field there is nothing to move.

## Results

| Statement | Result | Checked |
|---|---|---|
| Theorem 1 | Bonetti–Barausse at β = λ = 0: α₁ = −4α finite, α₂ has a pole, c_s² = 0; their expansion does not apply there (Flanagan) | script A4–A6; Lean `bb_point` |
| Theorem 2 | GFD's f is Flanagan's f exactly; χ̄ = μ − 1; the khronon density is the phantom density (TetB share), conserved, carried by v_T = −∇π | script A1–A3 |
| Theorem 3 | Stability f′ ≤ af″ ≤ 0 ⟺ μ′ ≥ 0 and (x(1 − μ))′ ≥ 0; for x/(x+1) these coincide (x(1 − μ) = μ) and hold at every a | script B1–B4; Lean `stability_dictionary`, `share_eq_law`, `law_deriv`, `share_deriv`, `gfd_stable` |
| Theorem 4 | Stability everywhere ⇒ f ↛ constant ⇒ a per-mass tail; for GFD a₀μ → a₀. In x/(1+xⁿ)^{1/n} only n = 1 is stable with a bounded tail | script B5–B7; Lean `stability_forces_tail`, `no_constant_limit`, `share_limit`, `standard_law_turns_over` |
| Theorem 5 | Around a point mass the khronon density is positive and a mode oscillates at ω² = [2/(2 − μ)]Ω² = −dg/dr, the radial tidal frequency (Ω to √2 Ω); it does not propagate | script C1–C5; Lean `density_exponent`, `oscillation_frequency` |
| Theorem 6 | Khronon inertia, density and momentum ∝ TetB share; in a drainless field the sector is empty, α₁ = α₂ = 0; leakage ≤ 4 × 10⁻¹⁷ at 1 AU | script D1–D4; Lean `inertia_vanishes` |
| Proposition 7 | Stationary systems (steady discs) exact; non-stationary systems carry an O(1) khronon correction | script E1–E2 |

## Prior work

- Blanchet & Marsat, *Modified gravity approach based on a preferred time foliation*, arXiv:1107.5264: the theory.
- Bonetti & Barausse, *Post-Newtonian constraints on Lorentz-violating gravity theories with a MOND phenomenology*, Phys. Rev. D 91, 084053 (2015), arXiv:1502.05554: the khronometric parametrisation and its PPN parameters.
- Flanagan, *Khronometric theories of modified Newtonian dynamics*, arXiv:2302.14846: the slow-motion limit at β = λ = 0, the khronon fluid and the stability conditions.

What this note adds:
- their application to GFD's f;
- the stability conditions read as conditions on μ and the TetB share;
- the proof that GFD's f meets them everywhere, and why;
- the forced tail and the uniqueness of n = 1;
- the khronon frequency;
- the khronon sector under the net-field rule.

## What it leaves open

- **Stability in general geometry.** Flanagan's density condition is established for spherical, cylindrical and planar symmetry only.
- **The size of the non-stationary correction** in any particular system (bars, interactions). This is the natural next test.
- **The net-field mechanism itself.** Theorem 6 assumes the rule, and the leakage figure uses its kernel bound with ℓ = r_J.
- **Beyond the slow-motion limit.** Tensor modes travel at c; the khronon's coupling to radiating binaries is not computed.
- **The fourth term** (the electromagnetic coupling).

## Contents

| File | What it is |
|---|---|
| [`sst_khronon_preferred_frame.pdf`](sst_khronon_preferred_frame.pdf) | The proof (4 pages) |
| [`sst_khronon_preferred_frame.tex`](sst_khronon_preferred_frame.tex) | LaTeX source (IOP class, [`iopjournal.cls`](iopjournal.cls)) |
| [`verify_sst_khronon_preferred_frame.py`](verify_sst_khronon_preferred_frame.py) | 24 checks: sympy exact algebra, plus the solar-system numbers and the family scan |
| [`verify_output.txt`](verify_output.txt) | Its output |
| [`lean/KhrononPreferredFrame.lean`](lean/KhrononPreferredFrame.lean) | Lean 4 formalisation, 13 theorems, importing the [net-field rule](../net-field-rule/lean/) and the constitutive law |
| [`LEAN_AUDIT.md`](LEAN_AUDIT.md) | What the Lean proves and what is cited |

## Running the checks

```
python verify_sst_khronon_preferred_frame.py
cd lean && lake exe cache get && lake build
```

The script needs sympy and mpmath, takes a few seconds, and ends with `24/24 checks passed`.
