# Letter: Power output and photometric mismatch (revised)

## Goal

Make the "Where photometric and decoded mass differ" section sound like **known GR structure** (nontrivial topology, throat, interior), not like describing dark matter. The mismatch is **expected rather than anomalous**; the framework defines the mass deficit operationally with the **same equation** as before.

---

## At a glance: what goes in the letter

- **Where:** Discussion (Sec. 4), after the SPARC paragraph. New **subsection**: "Where photometric and decoded mass differ."
- **What:** Two paragraphs. Paragraph 1: mismatch exists; "This is expected rather than anomalous"; GR framing (nontrivial topology, throat, interior); baryons as tracer; vortex as one-sentence illustration. Paragraph 2: covariant defines the delta; **same equation** (see below); power output = contribution from nontrivial spacetime topology including throat interior; we do not resolve interior dynamics here.
- **Equation (letter):** Same as before. Include **only** the compact form, **inline** in paragraph 2 (no new numbered display equation):
  - **Plain:** Delta M_enc(r) = M_phot(r) - M_dec(r), with M_dec the velocity-decoded enclosed mass from Eq. (Menc) in the Framework.
  - **LaTeX for letter.tex:** `\Delta M_{\mathrm{enc}}(r) = M_{\mathrm{phot}}(r) - M_{\mathrm{dec}}(r)`, where `M_{\mathrm{dec}}` is the velocity-decoded enclosed mass from Eq.~\ref{eq:Menc}.
- **Do not add to letter:** The fully expanded form v_obs^4 / [G(a_0 + v_obs^2/r)]; that is for a follow-up.

---

## Textbook terminology (context)

- **Nontrivial topology:** Standard Visser / Morris–Thorne / Wheeler term for wormhole/throat structure.
- **Throat:** Minimal-area hypersurface (Hochberg & Visser 1997).
- **Interior:** Standard GR for the region beyond the horizon/throat.
- **Exterior region:** Standard GR for the observable 3+1 spacetime.
- **Power output of the galactic field:** Letter's term, defined by the equation; in revised draft = "the contribution from the nontrivial spacetime topology, including the throat interior, that is not captured by the baryonic tracer alone."
- **Baryonic tracer:** Standard astrophysics.

Goal: immediately signal "there is an interior, it's structural, it's known physics."

---

## Equation verification (unchanged)

**Takeaway:** Use **only** the compact inline equation in the letter. **Equation (plain):** Delta M_enc(r) = M_phot(r) - M_dec(r), with M_dec from Eq. (Menc). Do **not** add a new numbered equation or the expanded form.

**Definition in code:** In generate_fig2_galaxy.py, the power output / mass deficit is Delta_M = M_phot_on_decode - M_dec (line 216). The "GFD (with power output)" curve is M_dec + Delta_M = M_phot by construction.

**Independent verification:** The letter already defines velocity-decoded enclosed mass in Eq. (Menc) (Framework): M_enc(r) = r v^4 / [G(a_0 r + v^2)]. With v = v_obs(r) this is M_dec(r). The mass deficit is Delta M_enc(r) = M_phot(r) - M_dec(r), with M_dec(r) given by Eq. (Menc). Correct and consistent with the letter.

---

## Draft prose for the new subsection (revised — GR topology, same equation)

**Subsection title:** Where photometric and decoded mass differ

**Paragraph 1 (plain):**
In some galaxies the velocity-decoded mass falls below the photometric baryonic mass; the pipeline still yields a well-defined decoded profile, but it no longer matches the baryons to within a factor of order unity. This is expected rather than anomalous. In general relativity, a spacetime with nontrivial topology — a throat connecting an exterior region to an interior — permits dynamics in the exterior that are not fully determined by the visible matter alone; the interior can sustain or modify the field that drives the rotation. Baryons trace the resulting flow but do not uniquely set its strength, just as particles carried by a fluid vortex trace the rotation without determining the power of the flow that maintains it. A mismatch between tracer count and field strength is therefore generic to systems whose topology includes an interior that contributes to the observed dynamics.

**Paragraph 2 (plain; equation in bold):**
Because the covariant decodes enclosed mass from observed velocity with no mass model, the difference between photometric and velocity-decoded mass is well defined at each radius; a researcher can quantify it directly from velocity observations and the inverse pipeline, with no additional parameters. The mass deficit **Delta M_enc(r) = M_phot(r) - M_dec(r)**, where **M_dec** is the velocity-decoded enclosed mass from Eq. (Menc), measures the effective power output of the galactic field — the contribution from the nontrivial spacetime topology, including the throat interior, that is not captured by the baryonic tracer alone. We do not resolve the interior dynamics in the present letter; we note that the framework defines this quantity operationally and that systematic study of galaxies across a range of morphologies and field strengths could map how the power output varies with structure and environment.

---

## LaTeX-ready version (for letter.tex)

```latex
\subsection{Where photometric and decoded mass differ}

In some galaxies the velocity-decoded mass falls below the photometric
baryonic mass; the pipeline still yields a well-defined decoded profile,
but it no longer matches the baryons to within a factor of order unity.
This is expected rather than anomalous.  In general relativity, a
spacetime with nontrivial topology---a throat connecting an exterior
region to an interior---permits dynamics in the exterior that are not
fully determined by the visible matter alone; the interior can sustain or
modify the field that drives the rotation.  Baryons trace the resulting
flow but do not uniquely set its strength, just as particles carried by a
fluid vortex trace the rotation without determining the power of the flow
that maintains it.  A mismatch between tracer count and field strength is
therefore generic to systems whose topology includes an interior that
contributes to the observed dynamics.

Because the covariant decodes enclosed mass from observed velocity with
no mass model, the difference between photometric and velocity-decoded
mass is well defined at each radius; a researcher can quantify it
directly from velocity observations and the inverse pipeline, with no
additional parameters.  The mass deficit $\Delta M_{\mathrm{enc}}(r) =
M_{\mathrm{phot}}(r) - M_{\mathrm{dec}}(r)$, where $M_{\mathrm{dec}}$
is the velocity-decoded enclosed mass from Eq.~\ref{eq:Menc}, measures
the effective power output of the galactic field---the contribution from
the nontrivial spacetime topology, including the throat interior, that is
not captured by the baryonic tracer alone.  We do not resolve the
interior dynamics in the present letter; we note that the framework
defines this quantity operationally and that systematic study of galaxies
across a range of morphologies and field strengths could map how the
power output varies with structure and environment.
```

---

## Sentence-by-sentence logic

**Paragraph 1:**

| # | Sentence / role |
|---|------------------|
| 1 | "In some galaxies..." — Observation: mismatch exists. |
| 2 | "This is expected rather than anomalous." — Pivot: not a failure. |
| 3 | "In general relativity, a spacetime with nontrivial topology..." — Textbook grounding: throat + interior is known GR. |
| 4 | "Baryons trace the resulting flow..." — Analogy: vortex/tracer in one sentence. |
| 5 | "A mismatch between tracer count and field strength..." — Conclusion: mismatch is generic. |

**Paragraph 2:**

| # | Sentence / role |
|---|------------------|
| 1 | "Because the covariant decodes..." — Operational: delta is well defined. |
| 2 | "The mass deficit Delta M_enc = ..." — **Same equation** + interpretation: power output defined as contribution from nontrivial topology (throat interior). |
| 3 | "We do not resolve the interior dynamics..." — Scope: not settling it here; forward look. |

---

## Summary

| Item | Action |
|------|--------|
| Goal | Sound like known GR structure (throat, interior, nontrivial topology), not like describing dark matter. |
| Equation | **Same equation:** Delta M_enc(r) = M_phot(r) - M_dec(r), M_dec from Eq. (Menc). Inline only; no new numbered equation; no expanded form. |
| Draft | Revised two paragraphs: GR topology first, "expected rather than anomalous," vortex as one-sentence illustration; paragraph 2 includes same equation and "power output = contribution from nontrivial spacetime topology, including the throat interior." |
| Placement | Discussion, new subsection "Where photometric and decoded mass differ." |

No changes to figures or to the main result; this is an additive, forward-looking subsection only.
