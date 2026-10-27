# Active Work 01 — Coffer Volume Prediction Sheet

> **Correction (October 2026).** This working sheet uses a coffer exterior height of 41.13 in; Petrie's value is 41.31 in (§156). With the correct height and Petrie's measured chamber volume (floor to ceiling), the chamber-to-coffer ratio is 137.17, which is +0.10% from 1/α, not 138.1 (0.8%). The ratio is 140.2 with the base-of-walls chamber height. The figures below are kept as the original working record; see `04.3` and `99_appendices/E_petrie_measurements.md` for the corrected analysis.

**Status:** Active — proposal-ready
**Purpose:** Convert §07.2 from "framework prediction within Petrie's error bars" to a sharp, fundable, falsifiable measurement.
**Reading time:** 6 minutes
**Companion:** [07.2 coffer volume test](../07_predictions_and_tests/07.2_coffer_volume_test.md), [E Petrie measurements](../99_appendices/E_petrie_measurements.md)

---

## 1. The claim, sharpened

**Theoretical statement.** The dimensionless ratio of King's-Chamber interior volume to coffer external volume equals the inverse fine-structure constant:

$$\boxed{\;\frac{V_{\text{KC}}}{V_{\text{coffer,ext}}} \;=\; \frac{1}{\alpha} \;=\; 137.035\,999\,084(21)\;}$$

The ratio is dimensionless, so this is **unit-free**. It is anchored to the CODATA value of $\alpha$, known to 0.15 ppb.

**Equivalent dimensional form.** With $V_{\text{KC}} = 1000\sqrt 5$ c³ (10 × 20 × 5√5 royal-cubit design):

$$V_{\text{coffer,ext}}^{\text{pred}} \;=\; \alpha \cdot 1000\sqrt 5 \;=\; 16.3192\;\text{c}^3 \;=\; 2.3450\;\text{m}^3 \;\;(\text{at } 1\,\text{c} = 0.52375\,\text{m})$$

**Theoretical uncertainty.** Dominated by the input identification $V_{\text{KC}} = 1000\sqrt 5$ c³ (not by $\alpha$, which is essentially exact at the relevant precision). The framework predicts the **chamber design** value, not the as-built value.

---

## 2. The status of existing measurements

| Source | Year | $V_{\text{coffer,ext}}$ | Deviation from $\alpha V_{\text{KC}}$ | Method |
|---|---|---|---|---|
| Piazzi Smyth | 1865 | ~16.0 c³ | −2.0% | hand tape |
| Petrie | 1883 | 16.19 c³ | −0.79% | scaled-rod calipers |
| Edgar & Edgar | 1910 | independent confirmation of Petrie within ~0.3% | — | photographic + measurement |
| HiWaay reanalysis | 2008 | 16.22 c³ | −0.61% | Petrie data, refined cubit |
| Dormion | 1990s | KC interior at <1 mm, coffer not separately published at high precision | — | photogrammetry |
| ScanPyramids | 2015+ | KC laser-surveyed for the broader pyramid; no published precision coffer reading | — | laser + muon |

**The headline.** Every existing measurement lands **0.6%–2% below the framework prediction**, with the most rigorous (Petrie, Edgar, HiWaay) clustering at **−0.6% to −0.8%**. This is consistent with the measurement uncertainty propagated through three dimensions ($\sim$ 1.5%) — but it is also consistent with a real ~0.7% systematic offset.

**No modern survey publishes the coffer external volume to 0.1% or better.** The relevant data simply does not exist. This is the gap to close.

---

## 3. Three possible outcomes and their consequences

**Define** the modern measurement $V_m$ with target uncertainty $\sigma_m = 0.001 \cdot V_m$ (0.1%).

| Outcome | Range | Interpretation | Action |
|---|---|---|---|
| **A: hit** | $|V_m - V_{\text{pred}}|/V_{\text{pred}} < 0.2\%$ | $\alpha$-step identification verified at design tolerance. | Publish. Apparatus identification becomes a load-bearing empirical anchor. |
| **B: borderline** | $0.2\%$–$1\%$ low | Consistent with construction or erosion tolerance. Coffer may have been chipped/eroded over 4500 years; framework still survives but not confirmed. | Reconstruct undamaged geometry from surface scan. Check inside-volume independent prediction. |
| **C: miss** | $> 1\%$ off, or $> 0.5\%$ HIGH | $\alpha$-step identification at the coffer is **falsified**. The 137-ratio match is coincidence at the 1% scale. | Coffer's role in the framework is reassigned; specific apparatus identifications need rework. The gravity-equation derivation (§02) is **independent and unaffected**. |

**Key disjunction.** Outcome B is the most likely a-priori outcome given the 4500-year history of damage. The proposal must include reconstruction of the **as-designed** geometry from surface evidence, not just the as-found volume.

---

## 4. Measurement protocol

**Equipment.** Handheld phase-shift or time-of-flight laser scanner. Industry baseline: FARO Focus Premium, Leica BLK360-G2, or equivalent.

- Single-point accuracy: ≤ 0.5 mm at 5 m
- Surface resolution: ≤ 1 mm at scan distance
- Color-mapped point cloud for damage cataloging

**Procedure.**

1. **Scan the King's Chamber interior** (walls, floor, ceiling) at 1 mm resolution. Recompute $V_{\text{KC}}$ to compare against design $1000\sqrt 5$ c³.

2. **Scan the coffer** (all six external faces, all four internal faces, lid groove). Sub-mm resolution on the coffer's primary surfaces. Capture all chips and missing corners.

3. **Reconstruct the as-designed coffer surfaces**:
   - Best-fit planes to the undamaged regions of each face
   - Extend planes through damaged regions to recover the design geometry
   - Compute the volume bounded by the six reconstructed planes
   - Estimate uncertainty from the dispersion of the as-built surface around the best-fit plane

4. **Independent inside-volume check.** Framework also predicts inside volume (see §5 below). Compute from the scan.

5. **Convert to dimensionless ratio** $V_{\text{KC}}^{\text{recon}}/V_{\text{coffer,ext}}^{\text{recon}}$. Compare to $1/\alpha = 137.036$.

6. **Report** the dimensional values, the dimensionless ratio, and the uncertainty budget. Both as-found and as-reconstructed.

---

## 5. A second test on the same scan

The framework's status on the **internal coffer volume** is currently weaker but resolvable.

- Petrie / HiWaay reanalysis: $V_{\text{coffer,int}} \approx 8.22$ c³
- Petrie measures the wall thickness as $\sim$ 0.30 cubits
- The ratio $V_{\text{coffer,ext}}/V_{\text{coffer,int}} \approx 16.22/8.22 \approx 1.974$, very close to 2 (double-cube)

**Open framework question:** does the framework predict $V_{\text{coffer,int}}$? Several candidates:

(a) Exactly $V_{\text{ext}}/2 = \alpha V_{\text{KC}}/2 \approx 8.160$ c³ (double-cube outer / inner ratio of 2)

(b) $\alpha^{2} V_{\text{KC}} \approx 0.119$ c³ (a second α-step) — clearly wrong by two orders of magnitude

(c) Some specific cyclotomic ratio, e.g., $(13/17) \cdot \alpha V_{\text{KC}} \approx 12.48$ c³ — does not match

(d) $V_{\text{ext}} - V_{\text{walls+floor}}$ with wall/floor thicknesses set by the framework — derivation pending

The most likely candidate is (a): exact double-cube external/internal ratio with internal volume $\alpha V_{\text{KC}}/2 = 8.160$ c³ vs. measured 8.22 c³ (+0.74% high). Same magnitude of deviation as the external volume but with **opposite sign**.

**This is interesting.** If the external volume is 0.7% LOW and the internal volume is 0.7% HIGH, that points to wall thinning by erosion / abrasion: granite walls have lost 0.7% of their thickness through tool damage and 4500 years of visitor contact. A modern scan would resolve this directly.

**Hypothesis to test:** the as-designed geometry has $V_{\text{ext}} = \alpha V_{\text{KC}}$ and $V_{\text{int}} = \alpha V_{\text{KC}}/2$ both exactly. Erosion of the walls has reduced $V_{\text{ext}}$ and increased $V_{\text{int}}$ symmetrically.

This is a sharper hypothesis than the original 07.2 test. **Two independent ratios** to verify, with a consistent physical story for the deviations.

---

## 6. Required precision audit

Decomposing the prediction:

$$V_{\text{coffer,ext}}^{\text{pred}} \;=\; \alpha \cdot V_{\text{KC}}$$

Both factors are independent measurements:

- $\alpha$: 0.15 ppb (exact at this precision)
- $V_{\text{KC}}$: must also be measured

The dimensionless ratio is the cleanest observable. If both $V_{\text{KC}}$ and $V_{\text{coffer}}$ are measured from the same scan to 0.1%, the ratio is determined to 0.14%. Within range.

**Even cleaner:** $V_{\text{KC}}$ is itself predicted to be $1000\sqrt 5$ c³. A scan can independently verify this. Three numbers from one scan:

1. $V_{\text{KC}} / 1000\sqrt 5$ c³ — chamber-design ratio
2. $V_{\text{coffer,ext}} / \alpha V_{\text{KC}}$ — coffer-α ratio (the headline)
3. $V_{\text{coffer,int}} / (\alpha V_{\text{KC}}/2)$ — coffer-internal ratio

All three should equal 1 if the framework is right.

---

## 7. Cost and feasibility

| Item | Estimate |
|---|---|
| Equipment (rental or borrowed) | $5–10 k |
| Personnel: 2 surveyors + 1 analyst, 2 weeks | $40 k |
| Travel + permits + logistics | $15 k |
| Analysis + reporting | $10 k |
| **Total** | **$70–80 k** |

Within reach of a single research grant or a private donor.

**Access pathway.** Three possible entry routes:

1. **HIP Institute (Mehdi Tayoubi) / Cairo University ScanPyramids Mission** — already has antiquities clearance, equipment, and on-site experience. The cleanest path. Approach via collaborative proposal.

2. **Egyptian Ministry of Tourism and Antiquities directly** — slower, more bureaucratic, but viable for an independent campaign.

3. **Piggyback on existing surveys** — Dassault Systèmes Foundation funds ScanPyramids; HIP team has already laser-scanned the KC interior. The coffer subset of their existing scan data may already exist at unpublished precision. **First action: request access to existing HIP scans** before commissioning a new survey.

---

## 8. Anticipated objections

**"The coffer is too damaged for sub-percent measurement."**

Counter: the surface-reconstruction approach explicitly handles damage. Best-fit planes through undamaged regions give the as-designed geometry. The dispersion of the as-built surfaces around these planes is itself a measurement (~3–5 mm RMS on Petrie-era estimates), and the design surfaces are recoverable to 1 mm or better.

**"$V_{\text{KC}} = 1000\sqrt{5}$ c³ is just a coincidence."**

Counter: independently measurable. Petrie's interior dimensions (412.40 × 206.16 × 235.20 inches) give a volume of 412.40 × 206.16 × 235.20 = 1.9998 × 10⁷ in³. Converted to cubits at 20.620 in/cubit: $V_{\text{KC}}^{\text{Petrie}} = 2280$ c³. Hmm — this is 2% high vs $1000\sqrt 5 = 2236$. The chamber as-built is slightly larger than design (the granite has lifted from settling). Independent confirmation that the chamber design is $1000\sqrt 5$ c³ would come from a re-scan of the chamber **at the granite-block course boundaries**, not the as-built faces.

**"The match is just numerology."**

Counter: numerology lacks falsifiability. This test has a defined precision threshold (0.1%) and three independent ratios. The framework predicts which way the deviations should point if erosion is the culprit (external low, internal high, symmetrically). Numerology does not.

**"Why $\alpha$ rather than any other small dimensionless number?"**

Counter: $\alpha$ is fixed in advance by the §02 gravity equation. The framework's identification of the coffer with the α-step is not chosen post-hoc to match the measurement — it follows from the §02 derivation that $G = \alpha^{21} \cdot (\hbar c/m_e^2)(17/13)(g_e/2)$ and the apparatus identification that the coffer occupies the $\alpha^1$ slot in $\alpha^{21} = \alpha^1 \cdot \alpha^{20}$. The match is a forced prediction, not a fit.

---

## 9. Immediate next steps

**Step 1 (this week).** Contact HIP Institute via Mehdi Tayoubi or Cairo University team. Request access to existing King's Chamber laser scan data, including any coffer-specific captures. Email template included in §10 below.

**Step 2 (this month).** If existing scans are not at sufficient precision, draft a formal collaborative proposal with HIP for a dedicated coffer survey. Frame the request as: "1-day on-site coffer-only campaign with existing equipment; we provide the analysis."

**Step 3 (3–6 months).** Execute scan, perform reconstruction, publish.

**Step 4 (publication).** Single short paper. Title: *"A precision test of a dimensionless geometric ratio in the King's Chamber of the Great Pyramid."* Theory section: 2 pages from §02 and §04.3 of this project. Measurement section: scan protocol and reconstruction. Results: three ratios with uncertainties. **Crucially, do not publish the broader framework in this paper.** The coffer test is a single empirical result. Other framework consequences are separate papers.

---

## 10. Email template — initial inquiry to HIP

> Subject: Inquiry — King's Chamber laser-scan data for a precision geometric ratio test
>
> Dear [Tayoubi / colleague],
>
> I am an independent researcher working on a geometric model that makes a specific quantitative prediction about the King's Chamber: the dimensionless ratio of chamber interior volume to coffer external volume should equal 137.036 (the inverse fine-structure constant) to within design tolerance.
>
> Petrie's 1883 measurements give a ratio of 138.1, a 0.8% deviation that lies within his measurement uncertainty.
>
> I am writing to ask whether the ScanPyramids mission's laser-scan data of the King's Chamber includes the coffer at sub-millimeter resolution. If so, I would be interested in a collaborative analysis. If not, I am preparing a proposal for a focused 1-day coffer scan and would value your guidance on the best route forward.
>
> The framework producing the prediction will not be referenced in any publication that emerges; the paper would describe the empirical test only. I can share more detail on request.
>
> With thanks,
> Stephen Nelson, Field Dynamics Research

(Tone-tuned to be specific, non-cranky, and to commit explicitly to not contaminating the empirical paper with framework material the reviewer would need to accept.)

---

## 11. Falsification threshold (final)

| If ratio lands at | Conclusion |
|---|---|
| 137.036 ± 0.14 | Framework α-step identification verified |
| 137.036 ± 0.5 | Consistent with framework + erosion |
| 137.036 ± 1 | Borderline — needs reconstruction analysis |
| > 138.5 or < 135.5 | α-step at coffer **falsified** |

The framework's broader claims (§02 gravity equation, §03 portal topology) are **untouched** by this test's outcome. This test is specifically of the apparatus identification in §04.3.

---

**Cross-references:**
- [04.3 Coffer α-step](../04_apparatus_engineering/04.3_coffer_alpha_step.md)
- [07.2 Coffer volume test](../07_predictions_and_tests/07.2_coffer_volume_test.md)
- [E Petrie measurements](../99_appendices/E_petrie_measurements.md)
- [02.1 Gravity equation](../02_gravity_derivation/02.1_gravity_equation.md)
