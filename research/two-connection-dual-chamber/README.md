# Two Connections and the Dual Chamber

*Working note, Field Dynamics Research, 2026-11-13. Status: research, not a paper. Verification: `python verify_two_connection.py` (13 checks) and `python verify_dual_chamber_bimetric.py` (16 checks), exact sympy.*

`teleparallel` `Weitzenböck` `torsion` `axial-torsion` `BIMOND` `dual-chamber` `TetA` `TetB` `research`

---

## Question

The [bimetric proof](../../proofs/bimetric-lock-constitutive-law/) showed that Hassan–Rosen's two metrics are not GFD's two chambers. The reason is Letter 2's Lemma:
- TetA = e and TetB = Pe are two roots of one metric.
- Anything built from the metric (including a potential in √(g⁻¹f)) cannot tell them apart.
- Only the torsion sector can.

Letters 2 and 3 add more:
- Christoffel plus contorsion corresponds to μ plus (1 − μ) (Letter 2, v2).
- The axial torsion reverses between TetA and TetB, and this chirality generates rotational closure (Letter 3's chiral-holonomy note).
- Exchange of the chambers inverts the odds Ω = μ/(1 − μ), which forces μ = x/(x + 1) (Letter 2's supplement).

So if a bimetric theory is to carry the dual chamber, it should couple **two connections**, not two metrics. This note starts that calculation. It works in the teleparallel (Weitzenböck) geometry of the tetrad, where gravity is carried by torsion, and asks four things:
1. What distinguishes the two roots.
2. Where the time leg's acceleration (the SST's y) sits.
3. What the chirality does.
4. What a two-connection theory built from the two roots looks like.

## Results

**1. The two roots have the same connection.** For any tetrad, the Weitzenböck connection Γ^λ_μν = e_a^λ ∂_ν e^a_μ is unchanged by a global Lorentz transformation, and spatial parity is one. So e and Pe have identical connections and identical torsion tensors, while det e flips sign (check 1.1).
- The connection difference of the two roots is zero, C = Γ(e) − Γ(Pe) = 0 (check 1.2).
- So the roots do not, by themselves, supply a "Christoffel + contorsion / Christoffel − contorsion" pair.
- What distinguishes them is **orientation**: det e, and anything built with the oriented ε tensor.

**2. The time leg's acceleration is torsion.** For a static tetrad, the torsion component T⁰ᵢ₀ = ∂ᵢ ln N is exactly the acceleration aᵢ of the time leg (check 1.3), the object whose square is the SST's y in the [covariant proof](../../proofs/sst-covariant-time-leg/). With flat spatial legs, the vector torsion v_i = T^λ_λi is exactly −a_i. In the weak field, c²vᵢ → −(∂ᵢΦ − 2∂ᵢΨ), so v·v matches the time leg's y only on Ψ = Φ (check 1.6).

However, y is **not** the teleparallel (TEGR) torsion scalar T:
- With flat spatial legs, T = 0 identically: the |∇Φ|² pieces cancel among its three terms (check 1.4).
- In the weak field, c⁴T → −(2|∇Ψ|² − 4∇Φ·∇Ψ). That is minus 16πG times the static Einstein–Hilbert part of Lemma 1 of the [quasi-static proof](../../proofs/sst-quasi-static-limit/), as R = −T + 2∇·v requires (checks 1.0 and 1.5).

So in teleparallel language the SST is "TEGR + a function of the vector-torsion norm along the time leg". This is a theory of the new-GR type (Hayashi–Shirafuji), in which the vector, axial and tensor parts of torsion carry separate coefficients.

**3. The chirality: zero when static, switched on by rotation, opposite on the two roots.**
- For any static tetrad the axial torsion vector A^μ = ε^{μνρσ}T_{νρσ}/6 vanishes, on both roots (check 2.1).
- For a tetrad whose spatial legs rotate at rate Ω about z, A = (0, 0, 0, 2Ω/3) on TetA and (0, 0, 0, −2Ω/3) on TetB (check 2.2).

This is Letter 3's chirality made explicit. It also sets a limit: **the chirality cannot be what fixes μ in rotation-curve data**, because the static (and quasi-static) field that SPARC tests has no axial torsion. If chirality has a role, it is in the rotating (vortex) sector.

**4. Two independent tetrads on opposite roots give BIMOND.** Let TetB be an independent tetrad ẽ on the negative root (det ẽ < 0), with its own lapse N̂. Then:
- The two Weitzenböck connections differ by C⁰₀ᵢ = ∂ᵢ ln(N/N̂) = ∂ᵢ(φ − φ̂)/c² (check 3.1). That is exactly Milgrom's BIMOND connection difference, now built from the two roots.
- It vanishes when TetB is the parity image of TetA, N̂ = N (check 3.2). The two chambers differ only when they carry different fields.
- The opposite sign of the second chamber comes from det ẽ < 0 with the same coupling. That is Lemma 1 of the [two-potential proof](../../proofs/bimetric-two-potential-energy/), and it gives α + β = 0.
- With α + β = 0, the two-potential proof's QUMOND limit splits the total field into **TetA field μg (Newtonian) plus TetB field (1 − μ)g**. The odds between them are x, the TetB field is a₀μ ≤ a₀, and the exchange x → 1/x swaps them (checks 4.1, 4.2).

**This is the dual-chamber composition, carried by two fields on the two roots:** TetA and TetB each hold their share, the shares sum to the total, and exchange inverts their odds. Unlike the deformed-frame construction in the bimetric proof, the two parts here are the two roots.

## A GFD-faithful bimetric algebra

*This section answers one question: what does Hassan–Rosen's two-chamber algebra have to become to reproduce GFD's μ(x)? Checks: `verify_dual_chamber_bimetric.py`.*

### Where we start

The [bimetric proof](../../proofs/bimetric-lock-constitutive-law/) established two things about Hassan–Rosen (HR) gravity with the locked coefficients β = (1, 0, 16, 0, 1):

- **The partition is right.** HR's potential V = Σ βₙeₙ(S), built from S = √(g⁻¹f), splits into a TetA part and a TetB part. Exchanging the two metrics inverts their odds Ω, so the TetB share is exactly Ω/(1 + Ω), the form of μ (its Theorem 8).
- **The variable is wrong.** μ(x) needs Ω to equal the acceleration ratio x = g/a₀. In standard HR the two metrics are nearly equal in any weak field, so Ω stays at 1 and the share at ½ (its Theorem 10).

So the task is to find a second chamber whose odds are x, and then see what else has to change.

### Step 1: a second chamber whose clock runs at the acceleration ratio

Take the second chamber's metric to be the first one with its clock rescaled along the time leg u:

  f = g − (y − 1) u u,  with y = x² and x = c²|a|/a₀,

where a is the acceleration of the time leg (the SST's covariant y; see the [time-leg proof](../../proofs/sst-covariant-time-leg/)). In words: TetB is the same space as TetA, but its proper time runs at rate x relative to TetA's. Algebraically f is a *disformal* transformation of g, the same kind of second metric that Bekenstein's disformal gravity and TeVeS use.

What follows, exactly (checks 1a–2d):
- **The odds become the acceleration.** S = √(g⁻¹f) = diag(x, 1, 1, 1): the time leg is stretched by x and nothing else changes. This is the principal square root, so HR's own metric form sees it. The two volume terms of V stand in the ratio 1 : det S = 1 : x, so Ω = x.
- **The dual-chamber share is GFD's μ.** The TetB share is Ω/(1 + Ω) = x/(1 + x). It equals the SST's own slope, F′(y) = μ.
- **Exchange and the ring.** Swapping the chambers sends x → 1/x and swaps the shares. At the ring x = 1, f = g: the two chambers coincide where the acceleration equals a₀.
- **The locked potential** on this second chamber is V = 49(1 + x).

### Step 2: TetB is a subspace

Rewrite the second metric with the spatial metric h = g + uu, which measures distances orthogonal to the time leg (checks 5a–5c):

  f = h − y u u.

- **TetB's space is the spatial subspace itself;** only its time direction carries the acceleration weight y.
- **In the deep field (y → 0) TetB collapses onto the subspace:** f becomes a rank-3 projector, while g stays rank 4.
- **On the pure subspace, S = diag(0, 1, 1, 1), the locked potential is V = 49.** That value, V₀ = 49, is the reference point of the energy in Step 3. At f = g it is 98.

Standard HR assumes the second metric is a full, independent, rank-4 metric. A second chamber that can degenerate onto a subspace is outside that set-up.

### Step 3: the vertex is nonlinear

With this second chamber, the SST's energy is a function of the HR potential (checks 3a–3b):

  F(y) − y = −2 D(V/V₀),  with D(w) = w − 1 − ln w and V₀ = 49.

D is a relative entropy: it measures how far V has moved from its subspace value V₀. So the SST's scalar term reads

  −(a₀²/8πG) F(y) = −(a₀²/8πG) [ y − 2 D(V/V₀) ]:

the curvature term's y, plus the relative entropy of the locked potential.

HR uses V linearly (√−g·V). The two pieces of D show why GFD cannot (checks 3c–3d):
- **The linear piece of D,** −2(V/V₀ − 1) = −2x, is exactly F's −2√y term. Alone, it gives a flux of fixed size a₀: the constant tail around every mass that is excluded in the solar system. *A linear HR vertex on this second chamber gives that tail and nothing else.*
- **The logarithm,** 2 ln(V/V₀), cancels the linear piece in the deep field. What survives is MOND's ⅔y^{3/2}, which gives flat rotation curves and Tully–Fisher.

So the nonlinearity of the vertex is not a detail. It is exactly what turns HR's partition into the constitutive law.

### The result, and what it does not yet do

**The unified statement.** GFD's SST is two-chamber gravity in which TetB is the spatial subspace with its clock running at the acceleration ratio x. HR's locked partition then gives μ(x) as TetB's volume share, and the SST's energy is the relative entropy of the locked potential measured from the subspace.

Compared with standard HR, three things change:

| | Standard Hassan–Rosen | GFD-faithful version | Status |
|---|---|---|---|
| The vertex | Linear in V | Nonlinear: the relative entropy D(V/V₀) | Shown (checks 3a–3d) |
| The second chamber | An independent full-rank metric, close to g in a weak field | Built on g's time leg; differs from g at order 1 in its clock; collapses onto the spatial subspace in the deep field | Shown (checks 1a–2d, 4b, 5a–5c) |
| Where the interaction acts | Everywhere in the bulk | Possibly at the Field Origin, the throat between TetA and the interior | Not attempted |

What remains open:
1. **An action that selects this second chamber.** f is built from g's first derivatives, not an independent field with its own Einstein–Hilbert term. The open step is an action whose second-metric equation has f = h − y uu as its solution.
2. **Ghost freedom.** HR's freedom from the Boulware–Deser ghost relies on the interaction being linear in the lapse. A logarithm of V is not, so whether this construction avoids the ghost has to be checked.
3. **The exchange symmetry of the energy.** The partition is symmetric under swapping the chambers, but the energy D is not (check 4a). That fits matter living in TetA, but the asymmetry has to come from the action.
4. **The interaction at the Field Origin.** The archive describes TetB as the interior reached only through the Field Origin, beyond a galaxy's central throat. That is a region, not only a tangent subspace. A faithful algebra may need the vertex at the throat, as a junction between two regions, closer to Einstein and Rosen's two sheets joined at a bridge than to HR's bulk potential.

## What is and is not shown

| Statement | Status |
|---|---|
| The two roots, as parity images, have the same connection; they differ only in orientation | Exact (checks 1.1, 1.2) |
| The time leg's acceleration is the torsion component T⁰ᵢ₀; the SST's y is a vector-torsion norm, not the TEGR scalar | Exact (checks 1.0, 1.3–1.6) |
| Axial torsion is zero for static fields and opposite on the two roots under rotation | Exact (checks 2.1, 2.2), for the tetrads tested |
| Two tetrads on opposite roots have BIMOND's connection difference; the det sign gives α + β = 0 | Exact in the static weak field (checks 3.1, 3.2) |
| The two fields compose the total as μg + (1 − μ)g, with odds x and exchange symmetry | Exact, **given** μ: the interaction function is fixed by requiring μ (two-potential proof), not derived |
| A second chamber f = g − (y − 1)uu = h − y uu gives Ω = x, the TetB share μ(x), and the SST's energy as the relative entropy of the locked potential, F − y = −2D(V/V₀) | Exact (`verify_dual_chamber_bimetric.py`) |
| A covariant action for the two-tetrad theory | Not written |
| μ derived from the exchange of the two tetrads | **Open: the central step** |

## The open steps, in order

1. **Write the action.**

   S = ∫ det(e) L_T(e) + ∫ det(ẽ) L_T(ẽ) + ∫ (interaction in C = Γ(e) − Γ(ẽ)) + matter on TetA,

   with det ẽ < 0 supplying the opposite sign. Vary it, and check that the static weak field gives BIMOND's two equations with α + β = 0.
2. **Supply Ω = x from an action.** The section above shows that a second chamber f = h − y uu gives Ω = x exactly, but f is built by hand. The task is an action whose equations select it, with the nonlinear (relative-entropy) vertex and without the Boulware–Deser ghost.
3. **Derive the interaction from exchange.** Exchanging e and ẽ inverts the odds of their fields. Show that requiring this symmetry of the action, as Letter 2's supplement requires it of the shares, fixes the interaction to the function M of the two-potential proof. That would derive μ from the two chambers instead of putting it in, and it is the step that would make the bridge a derivation.
4. **The vacuum.** When no matter is present, does the theory relax to ẽ = Pe (C = 0, one metric, two roots)? Matter would then pull the roots apart, which is how the dual chamber is described in the archive.
5. **The solar system.** The same net-field question as in the covariant proof: a local two-tetrad theory gives each star a TetB field up to a₀, which the archive excludes (Coles Notes §5.4).
6. **Rotation.** The axial torsion is the only root-odd torsion, and it switches on with rotation. Compute what it contributes for a rotating disk: whether it acts like the archive's drive and brake (the interior's active contribution, ΔM = M_phot − M_dec), and whether it is small enough not to disturb the static test.
7. **Local Lorentz invariance.** Teleparallel theories beyond TEGR, and theories with a preferred time leg, break it. Compute the preferred-frame parameters, as listed for the covariant SST.

## Files

| File | What it is |
|---|---|
| [`verify_two_connection.py`](verify_two_connection.py) | 13 checks: the Weitzenböck connection and torsion of both roots, the torsion scalar (validated against R), the vector and axial torsion, the two-tetrad connection difference, and the composition |
| [`verify_dual_chamber_bimetric.py`](verify_dual_chamber_bimetric.py) | 16 checks for the GFD-faithful bimetric algebra: the disformal second chamber and its eigenvalues, Ω = x and the share μ(x), the relative-entropy energy and its linear and logarithmic pieces, the exchange asymmetry of the energy, and TetB as the spatial subspace |

## References

- K. Hayashi and T. Shirafuji, New general relativity, *Phys. Rev. D* 19 (1979) 3524.
- R. Aldrovandi and J. G. Pereira, *Teleparallel Gravity: An Introduction*, Springer (2013).
- M. Milgrom, Bimetric MOND gravity, *Phys. Rev. D* 80 (2009) 123536, arXiv:0912.0790.
- S. F. Hassan and R. A. Rosen, Bimetric gravity from ghost-free massive gravity, *JHEP* 02 (2012) 126.
- J. D. Bekenstein, The relation between physical and gravitational geometry, *Phys. Rev. D* 48 (1993) 3641 (disformal metrics).
- J. D. Bekenstein, Relativistic gravitation theory for the MOND paradigm, *Phys. Rev. D* 70 (2004) 083509 (TeVeS).
- A. Einstein and N. Rosen, The particle problem in the general theory of relativity, *Phys. Rev.* 48 (1935) 73.
- Letters 1–3 and their supplements, in [`papers/`](../../papers/).
- Proofs: [bimetric lock](../../proofs/bimetric-lock-constitutive-law/), [two-potential energy](../../proofs/bimetric-two-potential-energy/), [SST time leg](../../proofs/sst-covariant-time-leg/), [exchange symmetry](../../proofs/constitutive-law-exchange-symmetry/).
