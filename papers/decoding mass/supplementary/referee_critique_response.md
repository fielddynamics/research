# Referee Critique Response: Letter Acceptance Odds

Internal note on the three main criticisms and how to address them.

**Paper scope (silo):** No other papers need to be mentioned in the letter or the Supplemental Material. The supplement is self-contained; we do not cite Paper I, Paper II, or Zenodo. We can silo the response. The Tully-Fisher velocity evolution paper is internal and can be provided as additional supplementary material only if referees request it.

**Stand-alone rule:** Paper I and Paper II are only on Zenodo; the letter and the Supplemental Material must not cite them. We pull material from those sources (and from Dual Tetrad) and write the supplement so it stands on its own. **Submission:** The supplement is submitted as **Supplemental Material (for referees)** so referees see the derivation and uniqueness argument; the letter says "See Supplemental Material for the derivation and uniqueness argument." That is standard journal workflow and avoids an "uncited private memo" vibe. The TF velocity evolution paper is internal (not yet submitted); it can be offered as additional supplementary document if need be.

---

## 1. Novelty vs MOND: "Where is the unique theoretical content?"

**Criticism:** The letter uses \(\mu(x) = x/(1+x)\) and says it is "determined by the action rather than chosen," but the derivation is out of scope. Referee may say: "This looks like MOND (simple \(\mu\)) repackaged."

**Material to pull from (internal only, not cited):**

- **Paper I (DFP Gravitational Constitutive Law):** Derives \(\mu(x) = x/(1+x)\) as a **uniqueness theorem** within the "Minimal Single-Channel Saturating Closure (MSC)" class. Three postulates (local closure, lossless, single calibration state at the closure boundary \(\Sigma\)) plus the minimal closure class **uniquely** fix this form; alternatives (e.g. \(\mu = x/\sqrt{1+x^2}\)) correspond to different closure classes.
- **Dual Tetrad / Paper II:** The covariant scalar-tensor action comes from the dual tetrahedron topology and field closure; the constitutive law is what that closure imposes.

**Minimal letter fix (no external refs):**

- In the letter use: *"See Supplemental Material for the derivation and uniqueness argument."* (Standard journal workflow; supplement is visible to referees.) Optionally add a short footnote: *"This form is unique within the minimal closure class under postulates A1--A3 (Supplemental Material)."* No citation to Zenodo papers.

**Precise claim (strongest "not just MOND" point):**

- **Functionally:** The end result \(\mu(x)=x/(1+x)\) is the same shape as MOND's "simple" interpolating function (commonly used in phenomenological MOND fits). Do not claim "we have a different \(\mu\) than MOND."
- **Theoretically / logically:** The constitutive law is **different in status**. In MOND, \(\mu\) is typically a **model choice** (picked from a family). In the DFP/MSC framing it is a **uniqueness theorem** within a declared closure class (local + lossless + single calibration state at \(\Sigma\)).
- **Correct claim:** "We explain *why* MOND's successful 'simple' \(\mu\) is the unique equilibrium law under minimal closure assumptions."

**Referee-proof sentence (use in Supplemental Material or letter if space allows):**

"Our constitutive law coincides with the commonly used 'simple' MOND interpolant, but here it is **not an ansatz**: it is **uniquely fixed** as the equilibrium solution within the Minimal Single-Channel Saturating Closure (MSC) class derived from field-closure constraints at \(\Sigma\)."

**Tightening (avoid overclaim):** Keep the core claim **conditional** and referee-safe: "**Unique within MSC under postulates A1--A3.**" In the letter, do **not** say "metric exchange symmetry sends \(x \to 1/x\)" unless \(x\) is defined as a symmetry-covariant variable in 1--2 lines; otherwise it reads like a leap. In the **supplement** it is fine to give the exchange-symmetry argument, but **show the mapping** (define \(x = g/a_0\), state that under TetA\(\leftrightarrow\)TetB exchange the dimensionless acceleration transforms as \(x \to 1/x\), then \(\mu(x)+\mu(1/x)=1\) forces \(n=1\) in \(\mu(x)=x/(n+x)\)).

**Optional (retrospective):** "This result retrospectively explains why the 'simple' interpolant performs well: it is the minimal closure fixed point."

---

### Uniqueness Capsule (letter-compatible, 4--6 lines)

**Option A (minimal):** Add: "See Supplemental Material for the derivation and uniqueness argument." Optional footnote: "This form is unique within MSC under postulates A1--A3 (Supplemental Material)."

**Option B (if a few lines available):** In the Framework, replace "Here it is determined by the action rather than chosen" with:

*"Here it is not an ansatz: it is uniquely fixed as the equilibrium solution in the Minimal Single-Channel Saturating Closure (MSC) class from field-closure constraints at \(\Sigma\) (see Supplemental Material). This result explains why the 'simple' interpolant performs well in fits: it is the minimal closure fixed point."*

Then continue with "Thus" into the displayed Eqs. 3--4.

**Option C (full capsule, if space):** Use the referee-proof sentence in full, ending with "(see Supplemental Material)."

**Risk:** If the letter does not contain the proof and does not cite an external derivation, a referee can say "This is asserted. Where is the uniqueness demonstrated?" The solution is **only** valid if the Supplemental Material is submitted and visible to referees.

---

## 2. Tetrad + bimetric motivation under-supported

**Criticism:** The letter names tetrad GR and ghost-free bimetric gravity but the working machinery is Poisson + SST transition in spherical symmetry. Referee may say: "These are name-dropped; the letter actually uses a scalar-tensor MOND-like relation plus Poisson."

**Material to pull from (internal only, not cited):**

- **Dual Tetrad:**  
  - Tetrad: \(g_{\mu\nu} = \eta_{ab} e^a_\mu e^b_\nu\); four legs \(\to\) tetrahedron at each node; field closure = non-degeneracy \(\det(g)\neq 0\).  
  - Bimetric: two tetrads (e.g. \(E\), \(L\)) coupled; ghost-freedom requires opposite orientations; the coupling polynomial \(f(k)=1+k+k^2\) with \(k=4\) gives the structure (21, 17, 13) that fixes \(G\) and the constitutive response.  
  - The **limit** that yields the letter’s equations: the covariant scalar-tensor action derived from this coupling hierarchy; in **spherical symmetry** the kinetic term \(F(|\nabla\Phi|^2/a_0^2)\) reduces to the single relation between \(g_{\mathrm{s}}\) and \(g_{\mathrm{t}}\), i.e. Eqs. (3)–(4).

- **Paper II:** Same topology; covariant theory reduces to the equations used in the letter.

**Minimal letter fix (no external refs):**

- Optional one-line in the existing "derivation beyond scope" sentence: *"...their derivation from the full covariant theory is beyond the scope of this letter (see Supplemental Material)."* The supplement then states the link in self-contained form.

**Supplement wording (avoid numerology):** Use "appears as" not "represents." Instead of "The '1' represents the Field Origin," use: "In the SST reduction, the closure/origin condition contributes an additive constant in the constitutive denominator." If mentioning 21, 17, 13, **show one explicit equation** where they enter (e.g. \(G\) or the Poisson prefactor \(4\pi \times (17/13)\)), otherwise a referee may call it unsupported. **Keep the supplement focused on two deliverables only:** (a) Why \(\mu\) is unique in MSC (short derivation). (b) How the SST action reduces to the spherical algebraic relation used in the letter. Everything else (full fingerprint, 21/17/13 story) is optional and can move to the full paper.

---

## 3. Uncertainty and robustness

**Criticism:** Smoothing is 6.2% of radial span. Referees will ask: Why 6.2%? How sensitive are \(M_{\mathrm{dec}}\) conclusions to that choice? Where are uncertainty bands on \(M_{\mathrm{dec}}(r)\)?

**What we have:**

- Figure script uses a fixed `frac=0.062` (6.2%) for all galaxies; comment says "identical for every galaxy, not tuned."
- No sensitivity sweep or uncertainty band is currently in the letter or figures.

**Minimal letter fix:**

- In the **Inverse** paragraph (Demonstration), add **one sentence** on robustness, after the sentence that mentions "Gaussian of width 6.2% of the radial span":

  *"Decoded mass profiles and the comparison to baryonic mass are stable for smoothing fractions in the range [e.g. 4\%--10\%]; we use 6.2\% as a single fixed value for all galaxies."*

  **Real sensitivity numbers** (from pipeline runs with frac \(\in \{0.04, 0.062, 0.10\}\)): Milky Way \(M_{\mathrm{dec}}(25\,\mathrm{kpc})\): 6.34e10, 6.58e10, 6.95e10 \(M_\odot\) (range \(\sim\)+9.6\%). Milky Way \(M_{\mathrm{dec}}(50\,\mathrm{kpc})\): 5.80e10, 5.91e10, 6.10e10 \(M_\odot\) (range \(\sim\)+5.2\%). M33 \(M_{\mathrm{dec}}(17\,\mathrm{kpc})\): 1.393e10, 1.381e10, 1.351e10 \(M_\odot\) (range \(\sim\)\(-\)3.1\%). **Suggested sentence for letter or supplement:** "Varying the smoothing fraction from 4\% to 10\% shifts the decoded masses by \(\le\)10\% (MW) and \(\le\)3\% (M33) at the reference radii." **Extra one-liner for supplement:** At the outermost points, the decoded mass remains 6.4\(\sigma\) (MW, 50 kpc) and 17.2\(\sigma\) (M33, 17 kpc) below the \(\Lambda\)CDM enclosed mass.

**Optional but high leverage:**

- **Sensitivity check in code:** In `generate_letter_figures.py`, add a short block that computes \(M_{\mathrm{dec}}\) at 25 kpc (MW) and 17 kpc (M33) for `frac in [0.04, 0.062, 0.10]` and prints them; then the letter can state the actual range over which results are stable.
- **Uncertainty band on \(M_{\mathrm{dec}}(r)\):** Propagate the reported velocity errors through Eq. (5) (e.g. \(v \to v\pm \sigma_v\) at each \(r\)) to get an envelope \(M_{\mathrm{dec}}(r)^{+/-}\). Plot a light shaded band in the mass panels. Even a rough band (e.g. using the nominal \(\sigma_v\) at each point) would address the referee concern.

**Context: two different 6.2\% (letter vs TF/Hubble):**

- **In the letter:** 6.2\% is the **smoothing fraction** (Gaussian width = 6.2\% of the radial span) applied to observed velocities before decoding. It reduces point-to-point scatter because \(v^4\) in Eq. (5) amplifies noise. The value is fixed for all galaxies and not tuned per object.
- **In TF velocity evolution and Hubble tension:** A **different** 6.2\% appears as the **topological scatter factor** \((k/\pi)^{1/4} = 1.062\), i.e. \(\pm 6.2\%\). It comes from the geometric mismatch between the flat tetrahedral local frame (\(k = 4\)) and the curved cosmological boundary (\(\pi\)). In `tf_velocity_evolution.tex`: "The ratio \(k/\pi\) quantifies the geometric mismatch ... For the velocity scatter, \(n = 1/4\), giving \((k/\pi)^{1/4} = 1.062\), corresponding to \(\pm 6.2\%\). This is the same aperture throughput that bounds the Hubble tension." So in the TF paper, the \(\pm 6.2\%\) band around the GFD prediction is the *topological measurement cage*; in `hubble-tension.md`, the same factor defines the predicted scatter in \(H_0\) (66.2--74.7 km/s/Mpc around 70.29).
- **Link (if intended):** If the letter's smoothing fraction 6.2\% is **chosen to match** the topological factor \((k/\pi)^{1/4}\), then "why 6.2\%?" has a principle-based answer: we use the topology-derived scatter scale as the smoothing scale, so it is not arbitrary. The Supplemental Material can state: "The smoothing fraction is set to the topological scatter factor \((k/\pi)^{1/4} = 6.2\%\), the same geometric factor that bounds the Hubble tension and the TF velocity evolution uncertainty band, so it is fixed by the field topology rather than tuned." If the match was coincidental, the note can still mention that the same factor appears elsewhere (TF, Hubble) as context; sensitivity (stability over a range of smoothing fractions) remains the main robustness answer.

**Sources:** `papers/tf_velocity_evolution.tex` (internal; not yet submitted; can be offered as additional supplementary document if needed). Section 3: \((k/\pi)^{1/4}\); Section 4 Hubble. `docs/hubble-tension.md`: aperture, scatter 1.062, measurement cage. Figure: `papers/tf-evolution.png`.

---

## Summary table

| Critique | Material to pull from (internal) | Minimal letter change |
|----------|----------------------------------|------------------------|
| 1. Novelty vs MOND | Paper I: uniqueness in MSC (A1--A3) | "See Supplemental Material for the derivation and uniqueness argument." |
| 2. Tetrad/bimetric | Dual Tetrad, Paper II: limit + closure | Optional "(see Supplemental Material)" in "derivation beyond scope" sentence |
| 3. Uncertainty/robustness | Pipeline sensitivity (4--10\%); \(\sigma\) below \(\Lambda\)CDM | Sentence: \(\le\)10\% (MW), \(\le\)3\% (M33) at reference radii; supplement: 6.4\(\sigma\), 17.2\(\sigma\) below \(\Lambda\)CDM |

---

## Implementation order

1. **Critique 1:** In the letter add "See Supplemental Material for the derivation and uniqueness argument." Write the supplement so it states the uniqueness argument in full (postulates A1--A3; in supplement show the \(x \to 1/x\) mapping if using exchange symmetry), with no citation to Zenodo.
2. **Critique 2:** Optional "(see Supplemental Material)" in the letter; supplement delivers (a) why \(\mu\) is unique in MSC, (b) how SST reduces to spherical algebraic relation. Use "appears as" language; if citing 21, 17, 13, give one explicit equation.
3. **Critique 3:** Insert the real sensitivity numbers and the sentence "Varying the smoothing fraction from 4\% to 10\% shifts the decoded masses by \(\le\)10\% (MW) and \(\le\)3\% (M33) at the reference radii." In the supplement add the one-liner: at the outermost points the decoded mass remains 6.4\(\sigma\) (MW, 50 kpc) and 17.2\(\sigma\) (M33, 17 kpc) below the \(\Lambda\)CDM enclosed mass.

The Supplemental Material stands on its own: no references to Paper I, Paper II, or Zenodo.

---

## Page limit: use Supplemental Material (for referees)

The letter is already at the 5-page limit. **Solution: keep the letter at 5 pages and submit the referee-proofing material as Supplemental Material (for referees).** Use the standard phrase in the letter: "See Supplemental Material for the derivation and uniqueness argument." That is standard journal workflow and avoids an "uncited private memo" vibe.

### How to use the Supplemental Material

- **At initial submission:** Submit as **Supplemental Material** so referees see it. The supplement explains novelty vs MOND (uniqueness in MSC), the covariant limit (SST \(\to\) spherical relation), and uncertainty/robustness (sensitivity numbers, \(\sigma\) below \(\Lambda\)CDM).
- **At revision:** Cite specific paragraphs in "Response to referees" ("As explained in the Supplemental Material, ...").

### What stays in the letter (minimal or zero word cost)

- **Critique 1 (novelty):** "See Supplemental Material for the derivation and uniqueness argument." Optional footnote: "This form is unique within MSC under postulates A1--A3 (Supplemental Material)."
- **Critique 2 (tetrad/bimetric):** Optional: "...their derivation from the full covariant theory is beyond the scope of this letter (see Supplemental Material)."
- **Critique 3 (robustness):** "Varying the smoothing fraction from 4\% to 10\% shifts the decoded masses by \(\le\)10\% (MW) and \(\le\)3\% (M33) at the reference radii; we use 6.2\%." Or move the full sentence to the supplement if space is tight.

### What goes in the Supplemental Material (self-contained, no Zenodo refs)

Two main deliverables; everything else optional (can move to full paper).

- **Section 1 (Uniqueness):** Why \(\mu(x)=x/(1+x)\) is unique in MSC under postulates A1--A3 (short derivation). If using exchange symmetry, define \(x = g/a_0\) and show the mapping \(x \to 1/x\) under TetA\(\leftrightarrow\)TetB so \(\mu(x)+\mu(1/x)=1\) forces \(n=1\). Keep core claim conditional: "Unique within MSC under A1--A3."
- **Section 2 (Limit):** How the SST action reduces to the spherical algebraic relation (Poisson + transition) used in the letter. Use "appears as" / "contributes an additive constant" language; if mentioning 21, 17, 13, include one explicit equation where they enter.
- **Section 3 (Robustness):** Why 6.2\%; sensitivity (real numbers: \(\le\)10\% MW, \(\le\)3\% M33); one-liner: 6.4\(\sigma\) (MW), 17.2\(\sigma\) (M33) below \(\Lambda\)CDM at outermost points.

The supplement can be 1--2 pages. The TF velocity evolution paper is internal (not submitted) and can be offered as additional supplementary document if needed.

---

## Plan: Full content for the Supplemental Material

The following is synthesized from Paper I (Constitutive Law), Paper II (Covariant Theory), and Dual Tetrad Gravity. Inline into the **Supplemental Material** so it stands on its own. Do not cite those documents. **Focus:** two main deliverables (uniqueness in MSC; SST reduces to spherical relation); rest optional.

---

### Section 1 (Novelty vs MOND): Why \(\mu(x) = x/(1+x)\) is unique, not chosen

**1.1 Uniqueness from minimal closure (Paper I, inlined).**  
Within the class of **minimal single-channel saturating closure (MSC)**, the constitutive law \(\mu(x) = x/(1+x)\) is the unique solution under three postulates: (i) **local closure** at the field boundary \(\Sigma\), (ii) **lossless** transmission (no extra dissipation channel), and (iii) **single calibration state** at \(\Sigma\) (one scale fixes the response). Other interpolating functions (e.g. \(\mu = x/\sqrt{1+x^2}\), the "standard" MOND form) correspond to different closure assumptions (non-minimal or multi-channel closure) and are testable against data. So \(\mu\) is not a fitted choice; it is the unique form in the minimal closure class.

**1.2 Uniqueness from detailed balance and exchange symmetry (Dual Tetrad, inlined).**  
At the closure boundary, the field partitions into a **resolved** fraction \(\varepsilon\) (transmitted) and **unresolved** \((1-\varepsilon)\) (saturated). **Detailed balance:** resolution rate \(\propto x(1-\varepsilon)\), relaxation rate \(\propto \varepsilon\); at equilibrium \(\varepsilon = x/(1+x)\). So \(\mu(x) \equiv \varepsilon(x) = x/(1+x)\).  
Why "1" and not "4" or "16"? In the **supplement** (not in the letter unless \(x\) is defined there): define \(x = g/a_0\). The stellated octahedron is symmetric under exchange of the two tetrahedra (TetA \(\leftrightarrow\) TetB); in bimetric language \(g \leftrightarrow f\) sends the dimensionless acceleration \(x \to 1/x\). So TetA resolves \(\mu(x)\), TetB resolves \(\mu(1/x)\), and total capacity is unity: \(\mu(x) + \mu(1/x) = 1\). For \(\mu(x) = x/(n+x)\), this holds **if and only if \(n = 1\)**. In the supplement use "appears as" language: "In the SST reduction, the closure/origin condition contributes an additive constant in the constitutive denominator" rather than "The '1' represents the Field Origin."

**1.3 Referee-proof formulation for the supplement.**  
- **Keep the core claim conditional:** "**Unique within MSC under postulates A1--A3.**" That is referee-safe.
- **Do not claim** "we have a different \(\mu\) than MOND." **Do claim** "we explain why MOND's successful 'simple' \(\mu\) is the unique equilibrium law under minimal closure assumptions."
- **Core sentence:** "Our constitutive law coincides with the commonly used 'simple' MOND interpolant, but here it is **not an ansatz**: it is **uniquely fixed** as the equilibrium solution within the MSC class derived from field-closure constraints at \(\Sigma\)."
- **Optional closing:** "This result retrospectively explains why the 'simple' interpolant performs well: it is the minimal closure fixed point."
- In the letter, avoid "metric exchange symmetry sends \(x \to 1/x\)" unless \(x\) is defined as a symmetry-covariant variable in 1--2 lines. In the supplement, show the mapping explicitly.

---

### Section 2 (Tetrad/bimetric to letter equations): What limit yields Eqs (1) and (3)–(4), and what is the fingerprint

**2.1 Tetrad and field closure.**  
General relativity in **tetrad form**: \(g_{\mu\nu} = \eta_{ab}\, e^a_\mu\, e^b_\nu\). The four tetrad legs at each point span the tangent space; in \((3+1)\) the spatial triad defines a **tetrahedron** at each field node. **Field closure** is the requirement that the metric be non-degenerate everywhere: \(\det(g) \neq 0\). In tetrad language this is \(\det(e) \neq 0\): the four legs must span completely. So field closure is what GR already enforces (non-degeneracy).

**2.2 Why two tetrads (bimetric) and the stellated octahedron.**  
Self-consistency requires **two** tetrahedral field sectors (spinor double cover, Ashtekar chiral decomposition, ghost-free bimetric gravity, stability). The two tetrads have **opposite orientations** and couple at a single point: the **Field Origin**. The minimal topology that satisfies this is the **stellated octahedron**: two tetrahedra sharing a center.

**2.3 Coupling polynomial and zero free parameters.**  
The coupling structure is \(f(k) = 1 + k + k^2\) with \(k = 4\) (simplex packing in 3+1 dimensions). The three terms are: Field Origin (1), vierbein face propagation (4), and full bimetric coupling (16). Evaluating at structural states: \(f(4) = 21\), \(f(4)|_{s=0} = 17\), \(f(4)|_{s=-1} = 13\). These integers fix \(G\) and the constitutive response. The **bimetric potential** is fully determined: \(V(\mathcal{S}) = e_0 + 16\,e_2 + e_4\) (i.e. \(\beta = (1, 0, 16, 0, 1)\)). **Zero free parameters** remain.

**2.4 Scalar-tensor action and constitutive law.**  
The **covariant scalar-tensor action** (letter Eq. 2) is \(S_{\mathrm{ST}} = \int d^4 x \sqrt{-g}[ R/(16\pi G) - a_0^2/(8\pi G)\, F(|\nabla\Phi|^2/a_0^2) + \ldots ]\). The kinetic function \(F\) is fixed by the constitutive law: \(\mu(\sqrt{y}) = dF/dy\) with \(y = |\nabla\Phi|^2/a_0^2\) gives \(F(y) = y - 2\sqrt{y} + 2\ln(1+\sqrt{y})\). The three terms correspond to the three levels of \(f(k)\): \(k^2\), \(k\), and \(k^0\). In the supplement use "appears as" language; if mentioning 21, 17, 13, show one explicit equation (e.g. \(G = (17/13)\,\alpha^{21}\,\hbar c/m_e^2\) or Poisson prefactor \(4\pi \times (17/13)\)).

**2.5 Spherical limit and the letter equations.**  
In **spherically symmetric** situations (rotation curves), the scalar-tensor field equation reduces to: (i) the **Poisson equation** \(\nabla^2\Phi = 4\pi G\rho\) (letter Eq. 1), which defines the **source acceleration** \(g_{\mathrm{s}}\) from the mass distribution; and (ii) a **single algebraic relation** between \(g_{\mathrm{s}}\) and the **total acceleration** \(g_{\mathrm{t}}\) that governs circular orbits. That relation is exactly the constitutive law \(\mu(g_{\mathrm{t}}/a_0)\) and yields the letter transition (Eqs. 3–4). So the **spherically symmetric limit** of the covariant theory (tetrad + ghost-free bimetric field closure, coupling hierarchy \(f(k)\), scalar-tensor completion) is the pair: Poisson + transition. No extra gravitational parameters beyond \(G\) and \(a_0\).

**2.6 Bimetric/tetrad fingerprint.**  
The "fingerprint" is: (a) the **form of the transition** is fixed by field closure (detailed balance and exchange symmetry), not by choosing an interpolating function; (b) the **coupling hierarchy** \(f(k)=1+k+k^2\) with \(k=4\) determines the kinetic term \(F\) and the single scale \(a_0\); (c) the letter equations are the **spherical limit** of that covariant theory. So the working machinery (Poisson + SST transition) is not disconnected from tetrad/bimetric; it is the limit.

**2.7 Poisson from field closure (optional short sentence).**  
In the full theory, the Poisson equation also derives from field closure: the normalization \(4\pi = k\times\pi\) with \(k=4\) and the ratio \(17/13 = f(k)|_{s=0}\,/\,f(k)|_{s=-1}\) yield the scale-invariant Poisson equation. For the letter, the standard form \(\nabla^2\Phi = 4\pi G\rho\) suffices.

---

### Section 3 (Uncertainty and robustness)

**3.1 Why 6.2\% smoothing.**  
The inverse pipeline uses \(M_{\mathrm{dec}}(r) = r v^4 / (G(a_0 r + v^2))\). The \(v^4\) factor amplifies measurement noise in \(v\). A single fixed **Gaussian smoothing** (width 6.2\% of the radial span) is applied to the observed velocities before decoding; this value is **identical for all galaxies**, not tuned per object.  
**Optional (if the choice is principled):** The same topology that yields the letter equations gives a natural scatter scale \((k/\pi)^{1/4} = 1.062\) (\(\pm 6.2\%\)), from the geometric ratio between the flat tetrahedral frame (\(k=4\)) and the curved boundary (\(\pi\)). That factor bounds the Hubble tension (predicted \(H_0\) scatter) and the Tully-Fisher velocity evolution uncertainty band. If the smoothing fraction is set to this topological scale, state in the note: "The smoothing fraction is the topology-derived scatter factor \((k/\pi)^{1/4} = 6.2\%\), so it is fixed by the field geometry rather than chosen."

**3.2 Sensitivity to smoothing (use real numbers).**  
**Pipeline results** (frac \(\in \{0.04, 0.062, 0.10\}\)): MW \(M_{\mathrm{dec}}(25\,\mathrm{kpc})\): 6.34e10, 6.58e10, 6.95e10 \(M_\odot\) (range \(\sim\)+9.6\%). MW \(M_{\mathrm{dec}}(50\,\mathrm{kpc})\): 5.80e10, 5.91e10, 6.10e10 \(M_\odot\) (range \(\sim\)+5.2\%). M33 \(M_{\mathrm{dec}}(17\,\mathrm{kpc})\): 1.393e10, 1.381e10, 1.351e10 \(M_\odot\) (range \(\sim\)\(-\)3.1\%). **Sentence for letter or supplement:** "Varying the smoothing fraction from 4\% to 10\% shifts the decoded masses by \(\le\)10\% (MW) and \(\le\)3\% (M33) at the reference radii." **One-liner for supplement:** At the outermost points, the decoded mass remains 6.4\(\sigma\) (MW, 50 kpc) and 17.2\(\sigma\) (M33, 17 kpc) below the \(\Lambda\)CDM enclosed mass.

**3.3 Uncertainty band (optional).**  
Propagate the reported velocity errors through Eq. (5) to obtain an envelope \(M_{\mathrm{dec}}(r)^{\pm}\). A sentence in the supplement (or a figure) that such bands can be computed from the figure script or included in extended work suffices.

---

### Implementation checklist

1. **Draft the Supplemental Material** using Sections 1–3 above (in prose). Two deliverables: (a) uniqueness in MSC under A1--A3, with \(x \to 1/x\) mapping shown in supplement; (b) how SST reduces to spherical relation. Use "appears as" language; if citing 21, 17, 13, give one explicit equation. No references to Paper I, Paper II, Zenodo, or Dual Tetrad by name.
2. **Letter:** (i) "See Supplemental Material for the derivation and uniqueness argument." Optional footnote: "Unique within MSC under postulates A1--A3 (Supplemental Material)." (ii) Optional: "(see Supplemental Material)" in "derivation beyond scope" sentence. (iii) "Varying the smoothing fraction from 4\% to 10\% shifts the decoded masses by \(\le\)10\% (MW) and \(\le\)3\% (M33) at the reference radii; we use 6.2\%." Or move to supplement if tight.
3. **Supplement Section 3:** Insert the real sensitivity numbers and the 6.4\(\sigma\) / 17.2\(\sigma\) one-liner. TF velocity evolution paper is internal; can be offered as additional supplementary document if needed.
