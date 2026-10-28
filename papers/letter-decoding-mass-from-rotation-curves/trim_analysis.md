# Letter trim analysis: bring refs onto page 5 (MNRAS 5-page limit)

**Goal:** Trim enough body text so that the reference list (currently spilling [8] Ellis, [9] Einstein, [10] Begeman onto page 6) fits on page 5. Typical need: ~8–15 lines of body text saved (one-column equivalent).

---

## 1. Highest impact, low risk (recommended first)

### A. Sec. "Where photometric and decoded mass differ" (line 152) — one long paragraph

**Current:** Single dense paragraph: definition of Delta M_eff, "Crucially...", "Figure 2 illustrates...", "We do not resolve...", "The relationship is analogous to a fluid vortex..."

**Trim:** Shorten the definition sentence and drop one redundant clause; shorten the vortex analogy.

- Replace the long sentence that defines Delta M_eff and explains "measures the difference... the additional gravitational field strength, sustained by the nontrivial spacetime topology including the throat interior, that is not accounted for by the baryonic mass alone" with:  
  "The mass deficit $\Delta M_{\mathrm{eff}}(r) = M_{\mathrm{phot}}(r) - M_{\mathrm{dec}}(r)$ (with $M_{\mathrm{dec}}$ from Eq.~\ref{eq:Mdec}) measures the difference between exterior baryonic mass and the effective mass inferred from the field: the additional field strength sustained by the interior topology."

- Replace "We do not resolve the interior dynamics in the present letter; we note that the framework defines this quantity operationally and that systematic study of galaxies across a range of morphologies and field strengths could map how the power output varies with structure and environment. The relationship is analogous to a fluid vortex, in which tracers on the surface faithfully follow the flow but do not determine the power output of the drain beneath."  
  with: "We do not resolve the interior dynamics here; the framework defines this quantity operationally. The relationship is analogous to a fluid vortex: tracers follow the flow but do not determine the power output of the drain beneath."

**Saves:** ~3–4 lines. Content preserved; only redundancy and wordiness removed.

---

### B. Topology sentence (line 150)

**Current:** "In general relativity, spacetimes with nontrivial topology (such as Ellis drainhole solutions \cite{Ellis73} or Einstein-Rosen bridges \cite{Einstein35}, structures whose astrophysical counterparts reside at the centers of spiral galaxies) permit an exterior gravitational field that is not uniquely determined by the exterior matter distribution."

**Trim:** "In general relativity, spacetimes with nontrivial topology (e.g. Ellis \cite{Ellis73}, Einstein-Rosen \cite{Einstein35}) permit an exterior gravitational field not uniquely determined by the exterior matter distribution."

**Saves:** ~1 line. Citations and meaning unchanged.

---

### C. Framework: sentence after Eq. 3–4 (line 85)

**Current:** "The algebraic form of $F(X)$ that produces Eq.~\ref{eq:transition} from the variational principle is determined by the theory. These relations are used in this letter for the inverse pipeline; the framework rests on these two equations and the constants $G$ and $a_0$, and no other gravitational parameters are introduced."

**Trim:** "The framework rests on these two equations and the constants $G$ and $a_0$; no other gravitational parameters are introduced."

**Saves:** ~1 line. (F from variational principle is already implied by "its form follows from the kinetic term F" earlier.)

---

### D. Inverse pipeline definition (line 92)

**Current:** Long sentence with parenthetical "(the mass that would produce this field through the SST and Poisson equations)" and "This is effective mass \emph{over the range where observed velocity data exist}; the pipeline returns $M_{\mathrm{dec}}(r)$ only at radii where $v(r)$ is measured or interpolated from measurements."

**Trim:** "The quantity $M_{\mathrm{dec}}(r)$ from this inverse is the \textbf{effective mass}: the mass-equivalent of the gravitational field strength at radius $r$ as experienced by an exterior observer. The pipeline returns $M_{\mathrm{dec}}(r)$ only at radii where $v(r)$ is measured; comparison to baryonic mass is the diagnostic. The rotation curve and the effective mass profile are two views of the same field: measure one, you infer the other."

**Saves:** ~1–2 lines. "Not a global or extrapolated quantity and is not assumed to be baryonic mass" dropped (covered by "comparison to baryonic mass is the diagnostic").

---

### E. Demonstration — Forward paragraph (line 103)

**Current:** Full component list with numbers (Hernquist bulge 1.5e10, scale 0.6 kpc; exponential disk 4.57e10, scale 2.2 kpc; gas 1.5e10; total ~7.6e10; M33 total ~7e9).

**Trim:** "We use published baryonic models from the literature~\cite{McMillan17,Corbelli00}: for the Milky Way, bulge, disk, and gas (total baryonic $\sim 7.6\times10^{10}\,M_\odot$); for M33, bulge, disk, and gas (total $\sim 7\times10^9\,M_\odot$). Applying Eqs.~\ref{eq:poisson} and \ref{eq:transition}, we obtain the predicted rotation curves (green dashed in Fig.~\ref{fig:1}, panels a and c). They track the observations without a dark matter halo and without any fitted gravitational parameters. For comparison, an NFW halo fit to each galaxy adds two or three parameters and achieves similar velocity agreement, but at the cost of a much larger mass budget (red dotted in panels a and c; the corresponding enclosed masses are in panels b and d)."

**Saves:** ~2 lines. Totals and citations kept; component detail moved to supplement or dropped.

---

### F. Discussion — SPARC parenthesis (line 136)

**Current:** "such as SPARC \cite{Lelli16} (175 disk galaxies with uniform photometry and measured rotation curves)"

**Trim:** "such as SPARC \cite{Lelli16} (175 disk galaxies)"

**Saves:** ~0.5 line.

---

## 2. Optional (if still over)

### G. Conclusions — vortex paragraph (line 177)

**Current:** Includes "A bathtub drain, a jet engine, a magnetic stirrer: each produces the same exterior flow with a different interior mechanism and a different power input; the tracers in the exterior cannot distinguish them."

**Trim:** Remove that sentence. The ping-pong ball analogy and quiet/active interior already make the point.

**Saves:** ~1 line. Slight loss of colour; logic intact.

---

### H. Inverse: velocity to mass (line 107)

**Current:** "The solid green curve in the velocity panels matches the data by construction (it is the round-trip of the observed $v$ through the equations and back). The physical result is in the mass panels."

**Trim:** "The velocity panels match by construction; the physical result is in the mass panels."

**Saves:** ~0.5 line.

---

## 3. Summary

| Item | Location        | Est. lines saved | Risk   |
|------|-----------------|------------------|--------|
| A    | Sec. deficit (152) | 3–4            | Low    |
| B    | Topology (150)     | 1              | Low    |
| C    | Framework (85)     | 1              | Low    |
| D    | Effective mass (92)| 1–2            | Low    |
| E    | Demonstration (103)| 2              | Low    |
| F    | SPARC (136)        | 0.5            | None   |
| G    | Conclusions (177)  | 1              | Optional |
| H    | Inverse (107)      | 0.5            | Low    |

**Recommended:** Apply A through F. That gives ~8–10 lines saved and should be enough to keep the reference list on page 5. If still over, add G and/or H.

---

## 4. What not to trim

- Abstract, Introduction, main equations, figure captions, Data and Code, Conclusions equation and galaxy narrative.
- Delta M_eff definition formula and "zero-parameter operational output"; only the long explanatory clause is shortened.
- Citations: all stay; only surrounding prose is shortened.
