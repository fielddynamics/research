# The Locked Bimetric Potential and the Constitutive Law

*Why the Hassan–Rosen lock β = (1, 0, 16, 0, 1) does not give the constitutive law μ(x) = x/(x + 1), and what a dual-chamber bridge would need · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`Hassan-Rosen` `bimetric-gravity` `Vainshtein` `Galileon` `exchange-symmetry` `constitutive-law` `MOND` `proof`

---

This folder holds a four-page proof and a script that checks every step (27 checks, exact algebra).

Papers VIII, IX and XII lock the Hassan–Rosen coefficients to β = (1, 0, 16, 0, 1). They state that the locked bimetric theory and the SST are two projections of one geometry. If so, the bimetric theory's quasi-static limit should give μ(x) = x/(x + 1). Papers VIII and IX list that match as open. This proof settles what can and cannot be shown.

## The answer

**No: Hassan–Rosen's two metrics are not GFD's two chambers, and the locked theory does not give μ(x).**

- **The standard reduction cannot give μ, for any coefficients.** Around a static mass the response depends on the enclosed mass only through M/r³. No function of M/r³ equals a function of x ∝ M/r² for all masses and radii, and on the branch that matches the linear solution the enhancement is capped below 1.71. The other real roots either weaken gravity or give a force growing like r whatever the mass. None has the deep-MOND form.
- **Letter 2 explains why.** TetA = e and TetB = Pe are two roots of one metric. A potential built from √(g⁻¹f) therefore takes the same value on either root (g⁻¹f = I) and cannot see the partition. Only the torsion sector can, and the Hassan–Rosen interaction has none.
- **A deformed frame reproduces the algebra, not the mechanism.** Deform one leg of a single frame by a ratio w. Every potential is then V = A + Bw, and the deformed leg's share is exchange-closed iff β₀ + 2β₁ = β₄ + 2β₃, giving exactly w/(1 + w). The lock gives V = 49(1 + w), with β₂ = 16 cancelling. But the two shares are parts of one frame, not TetA and TetB: on the actual roots the potential is 98 and 0. The deformation is also not a Hassan–Rosen reference metric.

The constitutive law's origin remains the two-root partition under exchange (Letter 2, the [exchange-symmetry proof](../constitutive-law-exchange-symmetry/)). Because Letter 2 locates the partition in torsion, a dual-chamber bridge would couple two connections, not two metrics. That is the subject of the research note [`research/two-connection-dual-chamber/`](../../research/two-connection-dual-chamber/).

## Results

| Theorem | Result |
|---|---|
| 1. The response depends on density | Decoupling-limit mixing coefficients (49, 32, 16, 0) for the lock, from an identity checked for general β. The static spherical equations are derived from the decoupling-limit Lagrangian here (all three are total derivatives), independently of the research note. The static π-equation is Q²s³ + 6Qs² + 6s − 2 = 0 with g_tot/g_N = 1 + s and Q ∝ M_enc/r³. d₂ = 16 keeps the cubic Galileon term, which Paper XII says vanishes |
| 2. The branches | Every real root is s = 2/D(v), Q = vD(v)/2, D = v² + 6v + 6. The branch matching the linear solution (s = 1/3, the vDVZ 4/3) is screened for Q > 0 and turns at Q* = 2 − 2√2 for Q < 0, where s = 1/√2: on it g_tot/g_N < 1.71. Where D < 0, g_tot/g_N ≤ 1/3. As D → 0⁺, s → ∞ with g_tot ∝ r, independent of the mass: unbounded, but not MOND |
| 3. No change of variable | Along M = Lr³ the density is fixed while x varies, so no function of M/r³ is 1/μ(x). Every root of the π-equation is a function of M/r³ alone, so this holds on every branch. The Vainshtein radius scales as M^{1/3}, the MOND radius as M^{1/2}. This holds for every β |
| 4. Parity and the polynomial | V(P) = β₀ − β₄ = 0 at GFD's parity configuration. On diag(1, s, s, s) the locked potential is 1 + 48s + 48s² + s³ (98, 1, 0), not the coupling polynomial 1 + 4s + 16s² (21, 17, 13) |
| 5. Hassan–Rosen is root-blind | TetA = e and TetB = Pe give the same metric while det e flips, so g⁻¹f = I and the potential takes the same value on either root. Only the vielbein form e⁻¹(Pe) = P sees TetB, where V(P) = 0. The two roots are the two square-root branches of g⁻¹f = I: P² = I, but P is not the principal root. This is Letter 2's Lemma applied to Hassan–Rosen, and it is why Theorems 1–4 come out negative |
| 6. Exchange closure on a deformed frame | On diag(1, 1, 1, w), V = A + Bw for every β. The share is exchange-closed iff A = B, i.e. β₀ + 2β₁ = β₄ + 2β₃. It is then exactly w/(1 + w) |
| Corollary 1 | The g ↔ f symmetry holds iff β is palindromic, and palindromic β satisfies the condition. The share is canonical: it is the elasticity w d ln V/dw. Then and V = (β₀ + 4β₁ + 3β₂)(1 + w). For the lock, V = 49(1 + w), with β₂ cancelling from the share. V/V(I) = det[(I + S)/2], the volume of the midpoint frame |
| Remark: not the two chambers | The shares w/(1+w) and 1/(1+w) sum to 1, have odds w and swap under w → 1/w, but they are the deformed leg and the three undeformed legs of one frame. On the roots V(I) = 98 and V(P) = 0; on the path between them V = (1+s)(s² + 47s + 1), with no exchange symmetry |
| 7. The time leg, and what V does not supply | With w = \|a\|/a₀ for the time leg's acceleration, w = x exactly in a static field (see [`../sst-covariant-time-leg/`](../sst-covariant-time-leg/)). The auxiliary energy E(u; y) = (1 − e^{−u})y − 2(sinh u − u), with u = ln(V/V₀), is stationary at V/V₀ = 1 + x, with value F(y) and slope μ. Its u-dependence contains no β: the potential supplies the variable, not the energy |

## What this means for the papers

- **The equivalence does not hold.** Papers VIII, IX and XII state that the locked theory and the SST are two projections of one geometry. In the standard reduction they are not (Theorems 1–3), Letter 2's Lemma shows why (Theorem 5), and no choice of β would change that.
- **The lock still fixes real bimetric physics:** the de Sitter background Λ = m²(1 + 48c²), the Fierz–Pauli mass, the Higuchi bound and the screening cubic. See [`research/bimetric-projection/`](../../research/bimetric-projection/).
- **The value 16 does not enter μ** in any construction here.

The papers themselves are not changed here.

## Contents

| File | What it is |
|---|---|
| [`bimetric_lock_constitutive_law.pdf`](bimetric_lock_constitutive_law.pdf) | The proof (4 pages) |
| [`bimetric_lock_constitutive_law.tex`](bimetric_lock_constitutive_law.tex) | LaTeX source (IOP class, [`iopjournal.cls`](iopjournal.cls)) |
| [`verify_bimetric_lock_constitutive_law.py`](verify_bimetric_lock_constitutive_law.py) | 27 checks, sympy exact algebra, including the decoupling-limit derivation |

The full decoupling-limit derivation (variation of the potential, reduced first integrals, the 23 checks of `verify_bimetric_projection.py`) is in [`research/bimetric-projection/`](../../research/bimetric-projection/).

## Running the checks

```
python verify_bimetric_lock_constitutive_law.py
```

It needs sympy, takes a few minutes, and ends with `27/27 checks passed`.
