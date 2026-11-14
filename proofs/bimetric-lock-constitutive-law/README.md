# The Locked Bimetric Potential and the Constitutive Law

*What the Hassan–Rosen lock β = (1, 0, 16, 0, 1) establishes about the stellated octahedron, and why it still does not give the constitutive law μ(x) = x/(x + 1) · Gravity Field Dynamics (GFD) · Field Dynamics Research*

`Hassan-Rosen` `bimetric-gravity` `stellated-octahedron` `exchange-symmetry` `constitutive-law` `Vainshtein` `MOND` `proof`

---

This folder holds a four-page proof and a script that checks every step (64 checks, exact algebra).

## Background

Hassan–Rosen (HR) bimetric gravity couples two metrics through a potential with five free coefficients β₀ … β₄. Papers VIII and XII fix them from the stellated-octahedron geometry:
- the two tetrads of the theory are the two tetrahedra;
- β₂ = 16 gives one unit of weight to each of the 16 boundary channels;
- exchanging the two metrics gives β₀ = β₄;
- an orientation argument gives β₁ = β₃ = 0.

That is **the lock**, β = (1, 0, 16, 0, 1). Paper XII then adds a further claim: that the locked theory and the SST are "two projections of one geometry". If so, HR gravity should reproduce μ(x) = x/(x + 1). This proof tests both.

## The answer in one paragraph

**The lock largely holds as geometry, and it even contains μ, but in the wrong variable.** Reading HR's two metrics as TetA (g) and TetB (f), each its own chamber, the potential splits into a TetA part and a TetB part. Exchanging the two metrics inverts their odds Ω (TetA : TetB), so TetA's share is exactly Ω/(1 + Ω) and TetB's is 1/(1 + Ω): the form of μ and 1 − μ. But μ(x) needs those odds to *be the acceleration*, Ω = x = g/a₀. HR's potential has no derivatives, so in any weak field its odds stay at 1. Deriving μ therefore takes two steps:
1. **Exchange symmetry of the partition gives μ(Ω).** HR contains this.
2. **The odds equal the acceleration, Ω = x.** HR cannot supply this; the SST supplies it through the acceleration of the tetrad's time leg.

## What holds

- **The exchange symmetry is exact.** The g ↔ f symmetry holds if and only if β is palindromic (β₀ = β₄, β₁ = β₃).
- **The odd coefficients vanish by total inversion, not parity.** β₁ = β₃ = 0 is exactly the condition V(−S) = V(S): flip the second tetrad completely, time leg included. Under spatial parity alone the locked potential is not symmetric: V(I) = 98, V(−I) = 98, but V(P) = 0.
- **The partition carries μ.**
  - The two volume terms (four TetA legs; four TetB legs, = det S) stand in the ratio 1 : det S.
  - Weighting every term by its number of TetB legs gives the same structure.
  - In both cases TetA's share is exactly Ω/(1 + Ω) and TetB's is 1/(1 + Ω), with Ω the TetA : TetB odds (1/det S for the volume terms) and the metric exchange inverting Ω. The value 16 plays no part.
- **The stellated octahedron sits at the pole.** In HR's language the compound is S = P, with odds Ω = 1/det P = −1, where Ω/(1 + Ω) has its pole. Its two volume terms cancel (1 − 1 = 0), and that is exactly why V(P) = 0. The total-inversion image −I sits at Ω = 1, the ring x = 1.
- **The exchange is the metric swap.** In the potential, the operation that inverts the odds is the exchange of the two metrics (S → S⁻¹). Spatial parity negates the odds instead (Ω → −Ω), and the compound P is its own inverse, a fixed point of the exchange. The null-rotation proof found the same distinction: TetB's count of 13 comes from total inversion, not parity.
- **β₂ = 16 is supported, not forced.** The Hessian of e₂ over the 16 entries of S has rank 16 (spectrum +3, +1 ×6, −1 ×9), as Paper XII states, but Paper XII takes β₂ = 16 as an axiom and it drops out of μ. What it does fix: the background, the graviton mass and the Higuchi margin.

## What does not hold

- **The odds are not the acceleration.** For two static weak-field metrics the volume odds are the inverse lapse ratio N/N̂ = 1 + O(Φ/c²), so the shares stay at ½: μ is reached only at x = 1. By leg count it is worse: the locked odds are (24n + 25)/(25n + 24), confined to [24/25, 25/24].
- **The standard reduction gives a density law, for any β.** Around a static mass the response depends on the enclosed mass only through M/r³, on every branch. No function of M/r³ equals a function of x ∝ M/r² for all masses and radii. On the branch that matches the weak-field solution the enhancement is below 1.71; the other roots weaken gravity or give a mass-independent force growing like r. None is MOND.
- **HR cannot see the two roots.** By Letter 2's Lemma, TetA = e and TetB = Pe have the same metric, so HR's g⁻¹f = I on either root. The two roots are the two square-root branches of the identity, and HR's metric form uses only the principal one.
- **A hand-built frame supplies Ω = x, but it is not HR.** Deforming one leg of a single frame by w = |a|/a₀ gives V = 49(1 + w) and the share w/(1 + w) = μ(x). It works only because it builds step 2 in by hand: the deformation is not an HR metric, its two shares are not the two roots, and the energy F is not HR's linear vertex: it is a nonlinear function of V, F − y = −2D(V/V₀), the relative entropy of the potential (see the research note).

**What remains open** is an action that supplies Ω = x from the two chambers themselves. Letter 2 places the partition in the torsion sector, where the time leg's acceleration is the torsion component T⁰ᵢ₀. That is the subject of the research note [`research/two-connection-dual-chamber/`](../../research/two-connection-dual-chamber/). Its section *A GFD-faithful bimetric algebra* shows what Hassan–Rosen has to become to reproduce μ(x): a second chamber whose clock runs at the acceleration ratio (TetB as the spatial subspace, f = h − y uu), giving Ω = x, with a nonlinear vertex, the relative entropy of the locked potential, in place of Hassan–Rosen's linear one.

**What that construction's second chamber is not.** The research note's second metric is built along TetA's time leg, with det S > 0. It is not TetB. In the archive TetB is its own chamber, the parity component of the tetrad equation reached through the Field Origin (det S = −1), not a time leg and not reverse time (Coles Notes, naming table; `EINSTEIN_TETA_PARTITION.md`). The time-leg metric is an auxiliary device that shows what Hassan–Rosen's algebra would need in order to carry the acceleration; the deformed family never reaches TetB's root (Theorem 9, check D18).

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
| 8. The partition carries μ | For palindromic β, the volume terms split 1 : det S, and the leg-weighted share has the same structure. In both TetA's share is Ω/(1 + Ω) and TetB's 1/(1 + Ω), with Ω the TetA : TetB odds; the metric exchange inverts Ω, and total inversion fixes it |
| 9. Which operation exchanges the chambers | β₁ = β₃ = 0 iff V(−S) = V(S). Spatial parity negates the odds; only the metric exchange inverts them. S = P sits at Ω = 1/det P = −1, the pole, which is why V(P) = 0; −I sits at Ω = 1, the ring |
| 10. The odds are not the acceleration | For two static weak-field metrics the volume odds are N/N̂ → 1 and the locked leg odds are (24n + 25)/(25n + 24) ∈ [24/25, 25/24]. μ across all x needs Ω = g/a₀, the deformed frame |
| Corollary 2: β₂ | The Hessian of e₂ has rank 16 (spectrum +3, +1 ×6, −1 ×9); β₂ drops out of μ(Ω) and is an axiom in Paper XII |

## Further checks (Part D of the script)

Twenty-one further checks test consequences and limits, not restatements:
- **The linear regime, from the derived equations.** λ = −q/(6Ma₁) and g_tot/g_N = 4/3 for any a₂, a₃. The two potentials differ there, with PPN γ = 1/2, so unscreened light bending would be 3/4 of GR (the vDVZ problem).
- **Screening and the radii.**
  - Strong screening goes as s ~ 2^{1/3}Q^{−2/3}.
  - The physical Q > 0 branch is monotone.
  - The end of the physical branch scales as M^{1/3}, the MOND radius as M^{1/2}, their ratio as M^{−1/6}.
  - Numerically r_V ≈ 256 kpc against r_M ≈ 3.3 kpc at 10¹⁰ M☉.
- **The parity configuration.**
  - V(P) = β₀ − 2β₁ + 2β₃ − β₄ in general, zero for every palindromic set.
  - The stress there is diag(49, −15, −15, −15), not a vacuum.
  - On the cube of sign flips the potential is 98, −30, and 0 on all four det S < 0 vertices, for every palindromic odd-free set.
- **What the lock does fix.** The proportional-background condition and its range 1/48 < α² < 48, the Fierz–Pauli combination 32c², the Higuchi identity m_FP²/H² − 2 = 4606c²/((c² + 48)(48c² + 1)) > 0 with maximum 192/49 at c = 1, and d₀ = V(I)/2.
- **The deformed frame, further.**
  - The share obeys Letter 3's logistic identity, equals 1/2 on the ring, and has odds w.
  - V is symmetric in the eigenvalues, so it does not single out the time leg.
  - The family never reaches det < 0, so it never reaches the second root.
  - The auxiliary energy's stationary point is a maximum, so F(y) = max_u E (Legendre-type), and F is convex, F″ = 1/(2√y(1 + √y)²).

## What this means for the papers

- **The geometric lock stands, with one correction.** Its exchange symmetry and palindrome are exact, and its partition carries μ(Ω) (Theorems 8–9). The correction: the odd terms vanish by total inversion, not by the spatial parity the papers cite.
- **The equivalence does not hold.** Papers VIII, IX and XII state that the locked theory and the SST are two projections of one geometry. The locked theory supplies μ only in its own odds, which stay at 1 in any weak field (Theorem 10); in the standard reduction it gives a density law (Theorems 1–3); and it cannot see the two roots (Theorem 5).
- **The lock still fixes real bimetric physics:** the de Sitter background Λ = m²(1 + 48c²), the Fierz–Pauli mass, the Higuchi bound and the screening cubic. See [`research/bimetric-projection/`](../../research/bimetric-projection/).
- **The value 16 does not enter μ** in any construction here.

The papers themselves are not changed here.

## Contents

| File | What it is |
|---|---|
| [`bimetric_lock_constitutive_law.pdf`](bimetric_lock_constitutive_law.pdf) | The proof (4 pages) |
| [`bimetric_lock_constitutive_law.tex`](bimetric_lock_constitutive_law.tex) | LaTeX source (IOP class, [`iopjournal.cls`](iopjournal.cls)) |
| [`verify_bimetric_lock_constitutive_law.py`](verify_bimetric_lock_constitutive_law.py) | 64 checks, sympy exact algebra: Part A (the standard reduction, derived from the decoupling-limit Lagrangian), Part B (the deformed frame), Part D (further checks), Part E (what the lock establishes) |

The full decoupling-limit derivation (variation of the potential, reduced first integrals, the 23 checks of `verify_bimetric_projection.py`) is in [`research/bimetric-projection/`](../../research/bimetric-projection/).

## Running the checks

```
python verify_bimetric_lock_constitutive_law.py
```

It needs sympy, takes a few minutes, and ends with `64/64 checks passed`.
