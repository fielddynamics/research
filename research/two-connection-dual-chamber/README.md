# Two Connections and the Dual Chamber

*Working note, Field Dynamics Research, 2026-11-13. Status: research, not a paper. Verification: `python verify_two_connection.py` (13 checks), `python verify_dual_chamber_bimetric.py` (16 checks) and `python verify_three_routes.py` (25 checks), exact sympy.*

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

## Three routes tested

*The previous section built the second chamber by hand. This section tries three ways to understand it: what its logarithm is, how to put it in an action, and what it means physically. Checks: `verify_three_routes.py`. Throughout, x = g/a₀, μ = x/(1 + x), and Z = V/V₀ = 1 + x on the second chamber of the previous section.*

### Route 1: the two chambers as a two-state system (what the logarithm is)

Treat TetA and TetB as two states with statistical weights 1 and x. Their partition function is

  Z = 1 + x,

which is exactly V/V₀, the locked potential on the second chamber divided by its subspace value (checks 1a–1c).
- **TetB's occupation is μ.** The fraction of the system in TetB, d ln Z/d ln x, is x/(1 + x).
- **The SST's logarithm is ln Z.** The energy is F = y − 2(Z − 1) + 2 ln Z. The logarithm appears because F adds up TetB's occupation as the field grows, F(y) = ∫ μ dy, and partial fractions of that integral produce ln Z.

Three algebraic facts sharpen this (checks 1g–1i):
- **In the log-odds λ = ln x,** ln Z = ln(1 + e^λ) and its slope is the logistic share. Its Legendre dual is the mixing entropy of the two chambers, μ ln μ + (1 − μ) ln(1 − μ). So the shares μ and 1 − μ are the maximum-entropy split for given log-odds.
- **The time-leg energy is a Gaussian relative entropy:** F − y = −4 KL(𝒩(0, Z) ‖ 𝒩(0, 1)), with Z = 1 + x.
- **What sets the weights.** If each chamber's weight is a horizon temperature (TetA's set by a₀, TetB's the Unruh temperature of the local acceleration, T_U = ħg/2πck), the odds are g/a₀ and the TetB share is g/(g + a₀) = μ (check 1d).

Two cautions (checks 1e–1f):
- **It is not a Boltzmann factor.** A single temperature with a fixed energy gap gives odds below 1 only, so it cannot reach x > 1. The weights are a ratio of temperatures, linear in x.
- **It differs from Milgrom's 1999 vacuum idea.** Milgrom subtracts the two temperatures, which gives (√(1 + x²) − 1)/x, going as x/2 in the deep field. The additive two-state weighting is what gives GFD's μ.

**What it explains, and what it does not.** It explains why the vertex is a logarithm: ln Z is the log-partition function of two chambers. It does not explain why the weights are temperatures, or derive a₀ as one.

### Route 2: TetB's clock rate as a field (how to put it in an action)

Make TetB's clock factor w a field of its own, with no derivatives (checks 2a–2e). Write the SST's time-leg term as

  F(y) − y = max over w of [ −y/w − w + 1/w + 2 ln w ].

- **The w-equation is algebraic** and gives w = 1 + x exactly. The value there is exactly F − y, and the point is a maximum.
- **For fixed w the field equation is linear,** as in Milgrom's QUMOND. Its conductivity is 1 − 1/w = 1 − V₀/V, the TetB volume share, which equals μ at w = 1 + x.
- **The SST is recovered.** Treating w as an independent field gives the same equation for Φ as the SST (by the envelope theorem).

The covariant form is

  √−g [ R/16πG + (a₀²/8πG)(y/w + w − 1/w − 2 ln w) ], y = c⁴a·a/a₀².

Because w has no derivatives it adds no propagating mode. The worry that a logarithm of V breaks Hassan–Rosen's ghost freedom therefore reduces to the stability of the time-leg (khronon) mode.

Going one step further, write the same thing in terms of the share itself, μ = 1 − 1/w (checks 2f–2h):

  F(y) = max over μ of [ μ y − K(μ) ],  K = Z − 1/Z − 2 ln Z = 2(sinh u − u), u = ln Z, Z = 1/(1 − μ).

- **The constitutive law is the stationarity condition.** K′(μ) = (μ/(1 − μ))² = Ω², so maximising sets y = Ω², i.e. the odds equal x.
- **The pair is conjugate.** K is convex, so the maximum is unique and F is K's Legendre transform: the share μ and the field variable y are conjugate variables.

**What it explains, and what it does not.** It gives the hand-built second chamber an action with no new propagating mode, and shows the constitutive law as the condition that the share be optimal. It does not explain where the cost K comes from; K = 2(sinh u − u) is the orientation-odd part of e^u − 1 − u, which matches the odd channel sK of the coupling polynomial, but that link is a reading, not a derivation.

### Route 4: TetB as a channel through the throat (what it means physically)

Read TetB as the interior reached through the Field Origin, and the TetB field as a channel through a throat that can carry at most a₀ (checks 4a–4d):

  1/g_B = 1/g + 1/a₀,  g = g_N + g_B.

- **The channel is a series combination,** like two resistances in series: the local field g and the throat capacity a₀. So g_B = a₀μ = (1 − μ)g, which is never more than a₀.
- **The spherical field equation follows exactly:** g_N = g²/(g + a₀).
- **The two channels have odds x:** TetA carries μ, TetB carries 1 − μ.
- **In the limits,** the throat dominates in strong fields (g_B → a₀, the a₀ tail) and the local field dominates in weak ones (TetB carries nearly all of it).

Further (checks 4e–4h):
- **As a product rule:** g·g_B = a₀·g_N. The total field times the TetB field equals a₀ times the Newtonian field.
- **The archive's family of laws is a family of channels.** x(1 − μ)^N = μ is the channel law g_B^N = a₀ g_N g^(N−2). N = 1 is the series law above. N = 2, the bound law of Papers XI and XIII, is g_B = √(a₀ g_N), the geometric mean of the throat capacity and the Newtonian field.
- **An area law.** Since g_B < a₀ always, the TetB (phantom) mass inside radius r is bounded, M_B = r²g_B/G < a₀r²/G. In the deep field it grows like r, the isothermal halo.
- **Beyond spherical symmetry the picture is QUMOND, not AQUAL.** Read the other way, the law is g = ν(g_N/a₀) g_N with ν(z) = (1 + √(1 + 4/z))/2, Milgrom's QUMOND form. A channel running along the field is QUMOND's construction. The SST is AQUAL-type. The two agree in spherical, cylindrical and planar symmetry and differ slightly elsewhere.

**What it explains, and what it does not.** This is the most physically suggestive route: it reads the field equation as flux through a throat of fixed capacity, takes "TetB is reached through the Field Origin" literally, and contains the bound law as the two-channel case. It is a flux law, not yet a field theory: what is missing is a junction condition at the throat that produces the series law, and a decision between its QUMOND form and the SST's AQUAL form away from symmetry.

### What the three routes say together

They describe one structure from three sides:

| Route | What it gives | What it still needs |
|---|---|---|
| 1. Two-state system | The logarithm is the log-partition function of the two chambers; the shares are maximum-entropy; the energy is a Gaussian relative entropy | Why the weights are temperatures (TetA's at a₀, TetB's Unruh at g) |
| 2. Auxiliary field | An action, with no new propagating mode; the constitutive law as the stationarity of the share; F and K as a conjugate pair | Where the cost K = 2(sinh u − u) comes from; the khronon's stability |
| 4. Throat channel | The spherical field equation as a series law with throat capacity a₀; the bound law as the two-channel case; an area bound on TetB mass | A junction condition that yields the series law; QUMOND versus AQUAL away from symmetry |

## What is and is not shown

| Statement | Status |
|---|---|
| The two roots, as parity images, have the same connection; they differ only in orientation | Exact (checks 1.1, 1.2) |
| The time leg's acceleration is the torsion component T⁰ᵢ₀; the SST's y is a vector-torsion norm, not the TEGR scalar | Exact (checks 1.0, 1.3–1.6) |
| Axial torsion is zero for static fields and opposite on the two roots under rotation | Exact (checks 2.1, 2.2), for the tetrads tested |
| Two tetrads on opposite roots have BIMOND's connection difference; the det sign gives α + β = 0 | Exact in the static weak field (checks 3.1, 3.2) |
| The two fields compose the total as μg + (1 − μ)g, with odds x and exchange symmetry | Exact, **given** μ: the interaction function is fixed by requiring μ (two-potential proof), not derived |
| A second chamber f = g − (y − 1)uu = h − y uu gives Ω = x, the TetB share μ(x), and the SST's energy as the relative entropy of the locked potential, F − y = −2D(V/V₀) | Exact (`verify_dual_chamber_bimetric.py`) |
| Three readings of that structure: a two-state partition function (the logarithm), an auxiliary-field action with no new mode (the share as the conjugate of y), and a throat channel of capacity a₀ (the field equation as a series law) | Exact (`verify_three_routes.py`); each still needs the item listed in its row above |
| A covariant action for the two-tetrad theory | Not written |
| μ derived from the exchange of the two tetrads | **Open: the central step** |

## The open steps, in order

1. **Write the action.**

   S = ∫ det(e) L_T(e) + ∫ det(ẽ) L_T(ẽ) + ∫ (interaction in C = Γ(e) − Γ(ẽ)) + matter on TetA,

   with det ẽ < 0 supplying the opposite sign. Vary it, and check that the static weak field gives BIMOND's two equations with α + β = 0.
2. **Supply Ω = x from an action.** A second chamber f = h − y uu gives Ω = x exactly, but it is built by hand. Route 2 gives it an auxiliary-field action with no new mode; what remains is to derive that action (its cost K) from the two chambers, and to settle the time-leg mode's stability. Route 4's open step, a junction condition at the throat that yields the series law, is the alternative.
3. **Derive the interaction from exchange.** Exchanging e and ẽ inverts the odds of their fields. Show that requiring this symmetry of the action, as Letter 2's supplement requires it of the shares, fixes the interaction to the function M of the two-potential proof. That would derive μ from the two chambers instead of putting it in, and it is the step that would make the bridge a derivation.
4. **The vacuum.** When no matter is present, does the theory relax to ẽ = Pe (C = 0, one metric, two roots)? Matter would then pull the roots apart, which is how the dual chamber is described in the archive.
5. **The solar system.** The same net-field question as in the covariant proof: a local two-tetrad theory gives each star a TetB field up to a₀, which the archive excludes (Coles Notes §5.4).
6. **Rotation.** The axial torsion is the only root-odd torsion, and it switches on with rotation. Compute what it contributes for a rotating disk: whether it acts like the archive's drive and brake (the interior's active contribution, ΔM = M_phot − M_dec), and whether it is small enough not to disturb the static test.
7. **Local Lorentz invariance.** Teleparallel theories beyond TEGR, and theories with a preferred time leg, break it. Compute the preferred-frame parameters, as listed for the covariant SST.

## Files

| File | What it is |
|---|---|
| [`verify_two_connection.py`](verify_two_connection.py) | 13 checks: the Weitzenböck connection and torsion of both roots, the torsion scalar (validated against R), the vector and axial torsion, the two-tetrad connection difference, and the composition |
| [`verify_three_routes.py`](verify_three_routes.py) | 25 checks for the three routes: the two-state partition function, its entropy dual and the Gaussian relative entropy; the auxiliary-field action and the share-cost conjugate pair; the throat channel, the family of channel laws, the area bound and the QUMOND form |
| [`verify_dual_chamber_bimetric.py`](verify_dual_chamber_bimetric.py) | 16 checks for the GFD-faithful bimetric algebra: the disformal second chamber and its eigenvalues, Ω = x and the share μ(x), the relative-entropy energy and its linear and logarithmic pieces, the exchange asymmetry of the energy, and TetB as the spatial subspace |

## References

- K. Hayashi and T. Shirafuji, New general relativity, *Phys. Rev. D* 19 (1979) 3524.
- R. Aldrovandi and J. G. Pereira, *Teleparallel Gravity: An Introduction*, Springer (2013).
- M. Milgrom, Bimetric MOND gravity, *Phys. Rev. D* 80 (2009) 123536, arXiv:0912.0790.
- S. F. Hassan and R. A. Rosen, Bimetric gravity from ghost-free massive gravity, *JHEP* 02 (2012) 126.
- J. D. Bekenstein, The relation between physical and gravitational geometry, *Phys. Rev. D* 48 (1993) 3641 (disformal metrics).
- J. D. Bekenstein, Relativistic gravitation theory for the MOND paradigm, *Phys. Rev. D* 70 (2004) 083509 (TeVeS).
- A. Einstein and N. Rosen, The particle problem in the general theory of relativity, *Phys. Rev.* 48 (1935) 73.
- M. Milgrom, The modified dynamics as a vacuum effect, *Phys. Lett. A* 253 (1999) 273, arXiv:astro-ph/9805346.
- M. Milgrom, Quasi-linear formulation of MOND, *Mon. Not. R. Astron. Soc.* 403 (2010) 886, arXiv:0911.5464.
- Letters 1–3 and their supplements, in [`papers/`](../../papers/).
- Proofs: [bimetric lock](../../proofs/bimetric-lock-constitutive-law/), [two-potential energy](../../proofs/bimetric-two-potential-energy/), [SST time leg](../../proofs/sst-covariant-time-leg/), [exchange symmetry](../../proofs/constitutive-law-exchange-symmetry/).
