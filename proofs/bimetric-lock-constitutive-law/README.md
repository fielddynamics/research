# The Locked Bimetric Potential and the Constitutive Law

*What the Hassan–Rosen lock β = (1, 0, 16, 0, 1) can and cannot give the constitutive law μ(x) = x/(x + 1) · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`Hassan-Rosen` `bimetric-gravity` `Vainshtein` `Galileon` `exchange-symmetry` `constitutive-law` `MOND` `proof`

---

This folder holds a three-page proof and a script that checks every step (18 checks, exact algebra).

Papers VIII, IX and XII lock the Hassan–Rosen coefficients to β = (1, 0, 16, 0, 1). They state that the locked bimetric theory and the SST are two projections of one geometry. If so, the bimetric theory's quasi-static limit should give μ(x) = x/(x + 1). Papers VIII and IX list that match as open. This proof settles what can and cannot be shown.

## The answer

**The standard reduction cannot give μ, for any coefficients.** In the decoupling limit around a static mass:
- **It depends on density.** The response depends on the enclosed mass only through M/r³.
- **No change of variable fixes it.** No function of M/r³ equals a function of x ∝ M/r² for all masses and radii.
- **Its boost is capped.** The enhancement is at most 4/3 in the linear regime and below 1.71 on every branch, while flat rotation curves need it to grow without bound.

**The constitutive law follows from the potential's exchange symmetry, on a different frame.** Deform the second frame along one leg by a ratio w. Every Hassan–Rosen potential is then V = A + Bw, and the deformed leg's share Bw/(A + Bw):
- obeys exchange closure, s(1/w) = 1 − s(w), **if and only if β₀ + 2β₁ = β₄ + 2β₃**;
- is then **exactly w/(1 + w)**.

Palindromic coefficients, which express the theory's g ↔ f symmetry, satisfy this. The locked set gives V = 49(1 + w), and β₂ = 16 cancels. With w = |a|/a₀, where a is the acceleration of the tetrad's time leg, the share is μ(x).

The correct statement is:

> An exchange-symmetric bimetric potential, evaluated on the frame deformed along the time leg's acceleration, carries the face share x/(x + 1). The standard Hassan–Rosen reduction does not.

## Results

| Theorem | Result |
|---|---|
| 1. The response depends on density | Decoupling-limit mixing coefficients (49, 32, 16, 0) for the lock. The static π-equation is Q²s³ + 6Qs² + 6s − 2 = 0 with g_tot/g_N = 1 + s and Q ∝ M_enc/r³. d₂ = 16 keeps the cubic Galileon term, which Paper XII says vanishes |
| 2. Bounded enhancement | s = 1/3 as Q → 0 (4/3, the vDVZ value). s → 0 as Q → ∞, screened to GR. The Q < 0 branch turns at Q* = 2 − 2√2, where s = 1/√2. So g_tot/g_N < 1.71 everywhere |
| 3. No change of variable | Along M = Lr³ the density is fixed while x varies, so no function of M/r³ is 1/μ(x). The Vainshtein radius scales as M^{1/3}, the MOND radius as M^{1/2}. This holds for every β |
| 4. Parity and the polynomial | V(P) = β₀ − β₄ = 0 at GFD's parity configuration. On diag(1, s, s, s) the locked potential is 1 + 48s + 48s² + s³ (98, 1, 0), not the coupling polynomial 1 + 4s + 16s² (21, 17, 13) |
| 5. Exchange closure fixes the share | On diag(1, 1, 1, w), V = A + Bw for every β. The share is exchange-closed iff A = B, i.e. β₀ + 2β₁ = β₄ + 2β₃. It is then exactly w/(1 + w) |
| Corollary 1 | Palindromic β (the g ↔ f symmetry) satisfies the condition, and V = (β₀ + 4β₁ + 3β₂)(1 + w). For the lock, V = 49(1 + w), with β₂ cancelling from the share. V/V(I) = det[(I + S)/2], the volume of the midpoint frame |
| 6. The time leg, and what V does not supply | With w = \|a\|/a₀ for the time leg's acceleration, w = x exactly in a static field (see [`../sst-covariant-time-leg/`](../sst-covariant-time-leg/)). The auxiliary energy E(u; y) = (1 − e^{−u})y − 2(sinh u − u), with u = ln(V/V₀), is stationary at V/V₀ = 1 + x, with value F(y) and slope μ. Its u-dependence contains no β: the potential supplies the variable, not the energy |

## What this means for the papers

- **The equivalence is overstated.** Papers VIII, IX and XII state that the locked theory and the SST are two projections of one geometry. In the standard reduction they are not (Theorems 1–3), and no choice of β would change that.
- **The lock still fixes real bimetric physics:** the de Sitter background Λ = m²(1 + 48c²), the Fierz–Pauli mass, the Higuchi bound and the screening cubic. See [`research/bimetric-projection/`](../../research/bimetric-projection/).
- **Where μ actually comes from.** The link between the lock and μ runs through exchange symmetry, the same principle as the [exchange-symmetry proof](../constitutive-law-exchange-symmetry/), on the time-leg frame. The value 16 does not enter μ.
- **The deformed frame is not an HR reference metric.** It is the single-metric time-leg structure, and deriving the deformation w = |a|/a₀ from an action is open.

The papers themselves are not changed here.

## Contents

| File | What it is |
|---|---|
| [`bimetric_lock_constitutive_law.pdf`](bimetric_lock_constitutive_law.pdf) | The proof (3 pages) |
| [`bimetric_lock_constitutive_law.tex`](bimetric_lock_constitutive_law.tex) | LaTeX source (IOP class, [`iopjournal.cls`](iopjournal.cls)) |
| [`verify_bimetric_lock_constitutive_law.py`](verify_bimetric_lock_constitutive_law.py) | 18 checks, sympy exact algebra |

The full decoupling-limit derivation (variation of the potential, reduced first integrals, the 23 checks of `verify_bimetric_projection.py`) is in [`research/bimetric-projection/`](../../research/bimetric-projection/).

## Running the checks

```
python verify_bimetric_lock_constitutive_law.py
```

It needs sympy and ends with `18/18 checks passed`.
