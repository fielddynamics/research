# Nuclear Binding Energy from the Bidirectional SST

## Pipeline: Reproducing the binding energy curve from one equation

This document describes the complete computational pipeline for reproducing
the nuclear binding energy curve from the SST quadratic. Every number is
traceable, every step is independently verifiable, and the accompanying
Python scripts reproduce all results exactly.

---

## Inputs

**One equation.** The SST quadratic (the bound-state partition of the scalar-tensor transition):

$$\mu_{\text{SST}}(x) = \frac{(2x+1) - \sqrt{4x+1}}{2x}$$

This is the self-consistent solution of the SST field equation when the
coupling must close on itself in a bound state. It is derived by requiring
that the return coupling $(1-\mu)$, acting as an effective source through the
SST, produces exactly $\mu$ as its output. The resulting self-consistency
condition $x(1-\mu)^2 = \mu$ is a quadratic in $\mu$; the physical root
(satisfying $0 < \mu < 1$ for $x > 0$) is the equation above.

**Two structural constants.** $K = 4$, $D = 3$. These are the unique integer
solution of the closure condition $2(D+1) = 2^D$. The Sierpinski walk has
$K^D = 64$ positions per sector, and the parent hierarchy has $K = 4$ sectors
for a total capacity of $4 \times 64 = 256$ positions.

**One experimental number.** $B/A(\text{Zn-64}) = 8.756$ MeV. The binding
energy per nucleon of zinc-64, which sits at $A = K^D = 64$, the unique
point where the walk fills one complete sector. This is the only contact
with experiment in the entire construction.

---

## Step 1. The coupling sum

Each walk position $i$ contributes coupling $\mu_{\text{SST}}(i^2)$ to
the collective binding. The argument $x = i^2$ maps walk position to
acceleration ratio (the Jacobian of the position-to-acceleration
transformation is $dx = 2i\,di$, so $x = i^2$ is the natural coordinate).

For any mass number $A$, define the coupling sum:

$$\Sigma_A = \sum_{i=1}^{A} \mu_{\text{SST}}(i^2)$$

At $A = 64$, every position on the first sector is filled and the sum
completes one full sector: $\Sigma_{64} = 59.928$.

Think of $\Sigma_A / \Sigma_{64}$ as a filling gauge: what fraction of
the sector's total coupling capacity has been collected. At $A = 12$ (carbon),
roughly a fifth. At $A = 64$ (zinc), the fraction is 1.

> **Note for verification.** The sum $\Sigma_{64} = 59.928$ can be computed
> in a single loop. Each $\mu_{\text{SST}}(i^2)$ value is independent and
> requires only the formula above. No recursion, no lookup tables.

---

## Step 2. The rising curve (SST₁)

For a nucleus with mass number $A$:

$$\text{SST}_1(A) = \frac{B}{A}(\text{Zn}) \cdot \frac{K^D}{A} \cdot \frac{\Sigma_A}{\Sigma_{K^D}}$$

Three terms, left to right:

- $B/A(\text{Zn}) = 8.756$ MeV is the **energy scale**. Converts the
  dimensionless coupling ratio to physical units. At $A = 64$ the formula
  returns 8.756 MeV by construction.

- $K^D / A$ is the **sharing factor**. The walk has 64 positions of coupling;
  these are shared among $A$ nucleons. At $A = 64$ this ratio is 1.
  At $A = 128$ the coupling is shared across twice as many nucleons.

- $\Sigma_A / \Sigma_{64}$ is the **coupling fraction**. What share of the
  sector's total coupling has been collected.

This curve rises from helium through iron and peaks at $A = 64$ (zinc).
It is the only curve computed directly. Every other curve in the
construction is a ceiling minus this one.

> **Note.** There is no opaque SCALE constant. The older formulation
> $B/A = (\text{SCALE}/A)\sum\mu_{\text{SST}}(i^2)$ is algebraically
> identical (SCALE $= 8.756 \times 64 / 59.928 = 9.351$ MeV), but the
> version above makes every term physically transparent.

---

## Step 3. Sector crossings

The Sierpinski hierarchy has $K = 4$ sectors at its parent level. The first
64 nucleons fill sector 0. At $A = 64$ that sector is complete. Additional
nucleons do not stop; the walk continues onto the next sector of the
hierarchy.

Crossing a sector boundary inverts the coupling profile. The SST reflects,
and the binding energy descends from a ceiling value. Each sector transition
produces a new descending curve because the field has already spent energy
filling the previous sector.

Every descending curve has the same shape as SST₁, flipped and subtracted
from a ceiling:

$$\text{SST}_n^{\,\text{inv}}(A) = \text{CEIL}_n - \text{SST}_{\text{local}}(A - A_n)$$

where $\text{SST}_{\text{local}}$ evaluates the walk from position 1 to
$(A - A_n)$ using the same formula as Step 2, and $A_n$ is the mass number
where sector $n$ begins. The ceiling values are derived in Step 5.

---

## Step 4. The sector-by-sector construction

**Sector 0** ($A \leq 64$). SST₁ rises from zero toward 8.756 MeV as the walk
fills. Its inverse, $\text{SST}_1^{\,\text{inv}} = \text{CEIL}_1 - \text{SST}_1$,
descends from CEIL₁. At $A = 64$ the two curves are equal, both giving
$B/A(\text{Zn})$. This fixes $\text{CEIL}_1 = 2 \times 8.756 = 17.512$ MeV.
For $A > 64$, the inverse falls below SST₁ and the descending curve governs.
The binding energy turns over.

**Sector 1** ($A > 64$). A new walk begins at $A = 64$, restarting from
position 1. At $A = 100$, this walk has filled 36 of its 64 positions.
At $A = 128$ it has filled all 64, completing a second sector. Its inverse,
$\text{SST}_2^{\,\text{inv}} = \text{CEIL}_2 - \text{SST}_{\text{local}}(A-64)$,
crosses below $\text{SST}_1^{\,\text{inv}}$ near $A \approx 110$ and governs
the descent from tin toward lead.

**Sector 2** ($A > 128$). A third walk begins at $A = 128$. Its inverse,
$\text{SST}_3^{\,\text{inv}} = \text{CEIL}_3 - \text{SST}_{\text{local}}(A-128)$,
governs the descent through the heavy elements.

**The gate sector.** The fourth sector (index 3) is the gate sector, the same
structural boundary that produces the $20 \to 28$ magic number anomaly.
At the top level of the hierarchy the gate sector contains $K^2 = 16$
positions. Total capacity: $3 \times K^D + K^2 = 192 + 16 = 208$. This
is lead-208, the heaviest stable nucleus. Beyond this point the cost of
extending into the gate sector exceeds the binding energy gain.

> **Note.** The gate mechanism operates at two scales. Within a single
> sector, the gate face excludes positions from the shell count, producing
> the magic numbers. At the parent level, the gate sector terminates
> nuclear stability at Pb-208. The same structural element, the same
> threshold $K$, both scales.

---

## Step 5. The ceiling sequence

Each sector's inverse begins at a sector boundary and descends from a
ceiling value. Every ceiling is set by one formula:

$$\text{CEIL} = \frac{B}{A}(\text{Zn}) + \frac{B}{A}\bigg|_{\text{boundary}} - \mu_{\text{SST}}(2) \left[\frac{B}{A}(\text{Zn}) - \frac{B}{A}\bigg|_{\text{boundary}}\right]$$

where $B/A|_{\text{boundary}}$ is the predicted binding energy at the
sector boundary from all previously established sectors, and

$$\mu_{\text{SST}}(2) = \frac{(2 \cdot 2 + 1) - \sqrt{4 \cdot 2 + 1}}{2 \cdot 2} = \frac{5-3}{4} = \frac{1}{2}$$

is the constitutive law at the bound-state field origin, the point where
the coupling splits remaining capacity equally between forward and return
directions.

The formula is applied identically at each sector boundary:

**Sector 0.** $B/A|_{\text{boundary}} = B/A(\text{Zn}) = 8.756$ MeV (the
walk has just filled; no prior sector). The $\mu_{\text{SST}}(2)$
correction is $\frac{1}{2}[8.756 - 8.756] = 0$. No impedance.
CEIL₁ = 8.756 + 8.756 - 0 = 17.512 MeV.

**Sector 1.** $B/A|_{\text{boundary}} = \text{SST}_1^{\,\text{inv}}(128)
= 17.512 - 9.003 = 8.509$ MeV (the field value at A = 128 from sector 0).
The $\mu_{\text{SST}}(2)$ correction is $\frac{1}{2}[8.756 - 8.509] = 0.124$
MeV. CEIL₂ = 8.756 + 8.509 - 0.124 = 17.141 MeV.

**Sector 2.** $B/A|_{\text{boundary}} = \text{CEIL}_2 - B/A(\text{Zn})
= 17.141 - 8.756 = 8.385$ MeV (the field value at A = 128 updated by
sector 1). The $\mu_{\text{SST}}(2)$ correction is $\frac{1}{2}[8.756 -
8.385] = 0.186$ MeV. CEIL₃ = 8.756 + 8.385 - 0.186 = 16.955 MeV.

| Sierpinski sector | B/A at boundary (MeV) | Correction (MeV) | Ceiling (MeV) |
|------|---------------|------------|---------|
| 0    | 8.756 | 0.000 (no impedance) | 17.512 |
| 1    | 8.509 | 0.124 | 17.141 |
| 2    | 8.385 | 0.186 | 16.955 |

The same constitutive law that shapes the binding curve also governs
the ceiling at every sector boundary.

> **Note for verification.** The `ceiling(prev)` function in the Python
> script implements this formula in one line. All three ceilings are
> computed by calling the same function with different `prev` values.
> There is no special case for any sector.

---

## Step 6. The envelope

At every mass number, the predicted binding energy is the minimum of all
active curves:

$$\frac{B}{A}(A) = \min\big(\text{SST}_1,\; \text{SST}_1^{\,\text{inv}},\; \text{SST}_2^{\,\text{inv}},\; \text{SST}_3^{\,\text{inv}}\big)$$

The curve rises because adding nucleons adds coupling. It peaks because
the first sector fills. It declines because each subsequent sector starts from
a lower ceiling. The entire shape (rise, peak, decline) is one field
closure filling progressively through the sectors of the Sierpinski hierarchy.

---

## Step 7. Verification

### Closure point accuracy

| Closure point | Element | Predicted (MeV) | Experimental (MeV) | Residual (keV) |
|---------------|---------|-----------------|--------------------|----|
| $K^D = 64$    | Zn-64   | 8.756           | 8.756              | 0 (calibration) |
| $2K^D = 128$  | Te-128  | 8.385           | 8.399              | 14 |
| $3K^D = 192$  | Os-192  | 8.138           | 8.167              | 29 |

### Mid-range accuracy

| Element | A   | Predicted (MeV) | Experimental (MeV) | Residual (keV) |
|---------|-----|-----------------|--------------------|----|
| Fe-56   | 56  | 8.693           | 8.790              | 97 |
| Sn-120  | 120 | 8.505           | 8.505              | 0  |

### Global statistics

| Region            | R²    | MAE (keV) |
|-------------------|-------|-----------|
| Round 1 (A ≤ 64)  | 0.90  | 97        |
| Post-64 (A > 64)  | 0.96  | 36        |
| Full (A = 4-208)  | 0.82  | 95        |

> **Reproducibility.** The Python script `gfd_binding_energy.py` generates
> the complete binding curve and all statistics from the equations above.
> Every function in the script maps directly to a step in this pipeline.
> The script requires only the Python standard library and numpy/matplotlib
> for plotting.

---

## Summary

The construction has four parts:

1. **One curve.** The SST quadratic summed along the walk, calibrated
   from zinc-64.

2. **One sector-crossing rule.** At each $K^D$ boundary, subtract the curve
   from a ceiling.

3. **One ceiling rule.** $\text{CEIL} = B/A(\text{Zn}) + B/A|_{\text{boundary}}
   - \mu_{\text{SST}}(2) \times [B/A(\text{Zn}) - B/A|_{\text{boundary}}]$.
   One formula, applied identically at every sector boundary.

4. **One envelope.** Take the minimum of all active curves.

One equation. One calibration point. One hierarchy. The entire binding
energy curve from helium to lead.

---

## What is NOT in this pipeline

The following are deliberately excluded from this construction:

- **No dark matter.** No halo profiles, no NFW parameters.
- **No spin-orbit coupling.** The $20 \to 28$ gap emerges from the gate
  face threshold, not from an added potential term.
- **No fitted coefficients.** The Bethe-Weizsacker formula uses five
  (volume, surface, Coulomb, asymmetry, pairing). This pipeline uses zero.
  The single calibration point (Zn-64) sets the energy scale, not a shape
  parameter.
- **No nuclear potential model.** The SST quadratic is a field equation,
  not a potential. It describes coupling capacity, not a force between
  nucleons.
- **No new particles or fields beyond the covariant action.** The SST
  quadratic is the bound-state partition of the same field equation that
  governs galaxy rotation curves.

---

## Cross-references

- Covariant action and SST derivation: [docs.fielddynamics.org/framework/md/covariant_completion](https://docs.fielddynamics.org/framework/md/covariant_completion/)
- Constitutive law: [docs.fielddynamics.org/framework/md/constitutive_law_mu_x](https://docs.fielddynamics.org/framework/md/constitutive_law_mu_x/)
- Validation tests: [docs.fielddynamics.org/tests](https://docs.fielddynamics.org/tests/)
- Python script: `gfd_binding_energy.py`

---

*Stephen Nelson, Field Dynamics Research. March 2026.*
